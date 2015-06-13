#! /usr/bin/env python
##############################################################################
#
# m2k2 1.4.2: an interpreter for m2k2 language
# Copyright (C) 2015 Angel Ivan Castell Rovira
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Any questions regarding this software should be directed to:
#
#   Angel Ivan Castell Rovira <al004140@gmail.com>
#
##############################################################################
# Modulo: sintactico
#
# Proposito: implementa el analizador sintactico del interprete.

#
##############################################################################
# Clases definidas:
#     SynAnalyser : el analizador sintactico
#     SynError    : construye los mensajes para errores sintacticos
##############################################################################

from sys       import stderr
from semantico import *

##############################################################################
# Class SynAnalyser
#
# Implementa los siguientes metodos:
#
# __init__         : es el constructor de la clase. Tiene los
#                    siguientes parametros
# parse_Linea      : comienza analisis sintactico de la linea actual
# parse_DeclVar    : analiza <DeclVar>    sintacticamente
# parse_Tipo       : analiza <Tipo>       sintacticamente
# parse_ListaIds   : analiza <ListaIds>   sintacticamente
# parse_Sentencia  : analiza <Sentencia>  sintacticamente
# parse_Asignacion : analiza <Asignacion> sintacticamente
# parse_Expresion  : analiza <Expresion>  sintacticamente
# parse_Termino    : analiza <Termino>    sintacticamente
# parse_Factor     : analiza <Factor>     sintacticamente
# parse_Rango      : analiza <Rango>      sintacticamente
##############################################################################

class SynAnalyser:

  def __init__(self, LexAnalyser):

    self.LA = LexAnalyser
    self.a = self.LA.getNextToken()
  # __init__
  #


  def parse_Linea(self):

    DeclVar   = Attributes()
    Sentencia = Attributes()

    # <Linea> -> <DeclVar> tkEOL
    if self.a.cat in ["tkTpoEnter", "tkTpoReal"]:
      if self.parse_DeclVar(DeclVar) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <DeclVar>")
      if self.a.cat not in ["tkEOL"]:
        raise SynError, SynError(self.LA, self.a, "expected tkEOL")
      return DeclVar.ast

    # <Linea> -> <Sentencia> tkEOL
    elif self.a.cat in ["tkIdent", "tkNrEnter", "tkNrReal", "tkOpTorio", "tkAbrPar", "tkMas", "tkMenos", "tkNo"]:
      if self.parse_Sentencia(Sentencia) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Sentencia>")
      if self.a.cat not in ["tkEOL"]:
        raise SynError, SynError(self.LA, self.a, "expected tkEOL")
      return Sentencia.ast

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Linea>")

    return 1
  # parse_Linea
  #


  def parse_DeclVar(self, DeclVar):

    Tipo     = Attributes()
    ListaIds = Attributes()

    # <DeclVar> -> <Tipo> <ListaIds>
    if self.a.cat in ["tkTpoEnter", "tkTpoReal"]:
      if self.parse_Tipo(Tipo) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Tipo>")
      if self.parse_ListaIds(ListaIds) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <ListaIds>")

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <DeclVar>")

    DeclVar.ast = node_Declaracion( Tipo.t, ListaIds.l )
    return 1
  # parse_DeclVar
  #


  def parse_Tipo(self, Tipo):

    # <Tipo> -> tkTpoEnter
    if self.a.cat in ["tkTpoEnter"]:
      self.a = self.LA.getNextToken()
      Tipo.t = "enter"

    # <Tipo> -> tkTpoReal
    elif self.a.cat in ["tkTpoReal"]:
      self.a = self.LA.getNextToken()
      Tipo.t = "real"

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Tipo>")

    return 1
  # parse_Tipo
  #


  def parse_ListaIds(self, ListaIds):

    # <ListaIds> -> tkIdent (tkComa tkIdent)*
    l = []
    if self.a.cat in ["tkIdent"]:
      l = l + [self.a.lex]
      self.a = self.LA.getNextToken()
      while self.a.cat in ["tkComa"]:
        self.a = self.LA.getNextToken()
        if self.a.cat not in ["tkIdent"]:
          raise SynError, SynError(self.LA, self.a, "expected tkIdent" )
        l = l + [self.a.lex]
        self.a = self.LA.getNextToken()
      # si a no pertenece a siguientes de p*
      if self.a.cat not in ["tkEOL"]:
        raise SynError, SynError(self.LA, self.a, "expected tkEOL")

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <ListaIds>")

    ListaIds.l = l
    return 1
  # parse_ListaIds
  #


  def parse_Sentencia(self, Sentencia):

    Expresion  = Attributes()
    Asignacion = Attributes()

    # <Sentencia> -> <Expresion> <Asignacion>
    if self.a.cat in ["tkIdent", "tkNrEnter", "tkNrReal", "tkOpTorio", "tkAbrPar", "tkMenos", "tkMas", "tkNo"]:
      if self.a.cat == "tkIdent":
        leftIdent = self.a.lex
      if self.parse_Expresion(Expresion) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Asignacion.leftisident = Expresion.isident
      if self.parse_Asignacion(Asignacion) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Asignacion>")

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Sentencia>")

    # se construye un nodo de asignacion o un nodo de expresion
    if Asignacion.isnotempty:
      Sentencia.ast = node_Asignacion( leftIdent, Asignacion.ast )
    else:
      Sentencia.ast = node_Expresion( Expresion.ast )

    return 1
  # parse_Sentencia
  #


  def parse_Asignacion(self, Asignacion):

    Expresion = Attributes()

    # <Asignacion> -> tkAsign <Expresion>
    if self.a.cat in ["tkAsign"]:
      Asignacion.isnotempty = 1
      if not Asignacion.leftisident:
        raise SynError, SynError(self.LA, self.a, "left side of an assignment must be tkIdent")
      self.a = self.LA.getNextToken()
      if self.parse_Expresion(Expresion) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Asignacion.ast = Expresion.ast

    # <Asignacion> -> lambda
    elif self.a.cat in ["tkEOL"]:
      Asignacion.isnotempty = 0

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Asignacion>")

    return 1
  # parse_Asignacion
  #


  def parse_Expresion(self, Expresion):

    Termino = Attributes()

    # <Expresion> -> <Termino> ( (tkMas|tkMenos|tkO) <Termino> )*
    if self.a.cat in ["tkIdent", "tkNrEnter", "tkNrReal", "tkOpTorio", "tkAbrPar", "tkMenos", "tkMas", "tkNo"]:
      if self.parse_Termino(Termino) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Termino>")
      Expresion.isident = Termino.isident
      Expresion.ast = Termino.ast
      while self.a.cat in ["tkMas","tkMenos","tkO"]:
        Expresion.isident = 0
        cat = self.a.cat
        self.a = self.LA.getNextToken()
        if self.parse_Termino(Termino) == 0:
          raise SynError, SynError(self.LA, self.a, "expected <Termino>")
        if cat == "tkMas":
          Expresion.ast = node_MasBinario( Expresion.ast, Termino.ast )
        if cat == "tkMenos":
          Expresion.ast = node_MenosBinario( Expresion.ast, Termino.ast )
        if cat == "tkO":
          Expresion.ast = node_O( Expresion.ast, Termino.ast )

      # si a no pertenece a siguientes de p*
      if self.a.cat not in ["tkAsign", "tkEOL", "tkCiePar", "tkPtoPto", "tkComa"]:
        raise SynError, SynError(self.LA, self.a, "expected tkAsign, tkEOL, tkCiePar, tkPtoPto or tkComa")

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Expresion>")

    return 1
  # parse_Expresion
  #


  def parse_Termino(self, Termino):

    Factor = Attributes()

    # <Termino> -> <Factor> ( (tkMul|tkDiv|tkY|tkPorCien|tkCmp) <Factor> )*
    if self.a.cat in ["tkIdent", "tkNrEnter", "tkNrReal", "tkOpTorio", "tkAbrPar", "tkMenos", "tkMas", "tkNo"]:
      if self.parse_Factor(Factor) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Factor>")
      Termino.isident = Factor.isident
      Termino.ast = Factor.ast
      while self.a.cat in ["tkMul","tkDiv","tkY","tkPorCien","tkCmp"]:
        Termino.isident = 0
        tk = self.a
        self.a = self.LA.getNextToken()
        if self.parse_Factor(Factor) == 0:
          raise SynError, SynError(self.LA, self.a, "expected <Factor>")
        if tk.cat == "tkMul":
          Termino.ast = node_Mul( Termino.ast, Factor.ast )
        if tk.cat == "tkDiv":
          Termino.ast = node_Div( Termino.ast, Factor.ast )
        if tk.cat == "tkY":
          Termino.ast = node_Y( Termino.ast, Factor.ast )
        if tk.cat == "tkPorCien":
          Termino.ast = node_PorCien( Termino.ast, Factor.ast )
        if tk.cat == "tkCmp":
          Termino.ast = node_Cmp( Termino.ast, tk.lex, Factor.ast )

      # si a no pertenece a siguientes de p*
      if self.a.cat not in ["tkMas", "tkMenos", "tkO", "tkAsign", "tkEOL", "tkCiePar", "tkPtoPto", "tkComa"]:
        raise SynError, SynError(self.LA, self.a, "expected tkMas, tkMenos, tkO, tkAsign, tkEOL, tkCiePar, tkPtoPto or tkComa")

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Termino>")

    return 1
  # parse_Termino
  #


  def parse_Factor(self, Factor):

    Rango     = Attributes()
    Expresion = Attributes()

    # <Factor> -> tkIdent | tkNrEnter | tkNrReal
    if self.a.cat in ["tkIdent"]:
      Factor.isident = 1
      Factor.ast = node_Ident( self.a.lex )
      self.a = self.LA.getNextToken()

    elif self.a.cat in ["tkNrEnter", "tkNrReal"]:
      Factor.isident = 0
      if self.a.cat == "tkNrEnter":
        Factor.ast = node_NrEnter( self.a.val )
      if self.a.cat == "tkNrReal":
        Factor.ast = node_NrReal( self.a.val )
      self.a = self.LA.getNextToken()

    # <Factor> -> tkOpTorio tkAbrPar tkIdent tkComa <Rango> tkComa <Expresion> tkCiePar
    elif self.a.cat in ["tkOpTorio"]:
      optor = self.a.lex
      self.a = self.LA.getNextToken()
      if self.a.cat not in ["tkAbrPar"]:
        raise SynError, SynError(self.LA, self.a, "expected tkAbrPar")
      self.a = self.LA.getNextToken()
      if self.a.cat not in ["tkIdent"]:
        raise SynError, SynError(self.LA, self.a, "expected tkIdent")
      id = self.a.lex
      self.a = self.LA.getNextToken()
      if self.a.cat not in ["tkComa"]:
        raise SynError, SynError(self.LA, self.a, "expected tkComa")
      self.a = self.LA.getNextToken()
      if self.parse_Rango(Rango) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Rango>")
      # se dispone ya de los atributos sintetizados Rango.ast1 y Rango.ast2
      if self.a.cat not in ["tkComa"]:
        raise SynError, SynError(self.LA, self.a, "expected tkComa")
      self.a = self.LA.getNextToken()
      if self.parse_Expresion(Expresion) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Factor.ast = node_OpTorio( optor, id, Rango.ast1, Rango.ast2, Expresion.ast )
      if self.a.cat not in ["tkCiePar"]:
        raise SynError, SynError(self.LA, self.a, "expected tkCiePar")
      self.a = self.LA.getNextToken()
      Factor.isident = 0

    # <Factor> -> tkAbrPar <Expresion> tkCiePar
    elif self.a.cat in ["tkAbrPar"]:
      Factor.isident = 0
      self.a = self.LA.getNextToken()
      if self.parse_Expresion(Expresion) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Factor.ast = Expresion.ast
      if self.a.cat not in ["tkCiePar"]:
        raise SynError, SynError(self.LA, self.a, "expected tkCiePar")
      self.a = self.LA.getNextToken()

    # <Factor> -> (tkMenos | tkMas | tkNo ) <Factor>
    elif self.a.cat in ["tkMenos", "tkMas", "tkNo"]:
      cat = self.a.cat
      self.a = self.LA.getNextToken()
      if self.parse_Factor(Factor) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Factor>")
      if cat == "tkMenos":
        Factor.ast = node_MenosUnario( Factor.ast )
      if cat == "tkMas":
        Factor.ast = node_MasUnario( Factor.ast )
      if cat == "tkNo":
        Factor.ast = node_No( Factor.ast )
      Factor.isident = 0

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Factor>")

    return 1
  # parse_Factor
  #


  def parse_Rango(self, Rango):

    Expresion1 = Attributes()
    Expresion2 = Attributes()

    # <Rango> -> <Expresion> tkPtoPto <Expresion>
    if self.a.cat in ["tkIdent", "tkNrEnter", "tkNrReal", "tkOpTorio", "tkAbrPar", "tkMenos", "tkMas", "tkNo"]:
      if self.parse_Expresion(Expresion1) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Rango.ast1 = Expresion1.ast
      if self.a.cat not in ["tkPtoPto"]:
        raise SynError, SynError(self.LA, self.a, "expected tkPtoPto")
      self.a = self.LA.getNextToken()
      if self.parse_Expresion(Expresion2) == 0:
        raise SynError, SynError(self.LA, self.a, "expected <Expresion>")
      Rango.ast2 = Expresion2.ast

    # otro
    else:
      raise SynError, SynError(self.LA, self.a, "expected <Rango>")

    return 1
  # parse_Rango
  #


##############################################################################
# Class SynError
#
# Construye un mensaje de error sintactico para imprimir por stderr
#
# Implementa los siguientes metodos:
#
# __init__ : es el constructor de la clase. Tiene los siguientes
#            parametros:
#             - LA      : analizador lexico de la linea actual
#             - token   : token en el que se ha roto el parsing
#             - message : el mensaje de error
# __str__  : construye la cadena que se imprime por stderr
##############################################################################
class SynError:

  def __init__(self, LA, token, message):

    self.fis  = LA.fis
    self.s    = LA.s
    self.sNr  = LA.sNr
    self.chr1 = token.chr1
    self.cat  = token.cat
    self.msg  = message
  # __init__
  #


  def __str__(self):

    s = ""
    s = s + "File \"<" + self.fis + ">\", line " + str(self.sNr) + '\n'
    s = s + self.s
    for i in range (self.chr1):
      s = s + ' '
    s = s + '^' + '\n'
    s = s + "Syntax Error: "
    s = s + self.cat + " unexpected; "
    s = s + self.msg + '\n\n'
    return s
  # __str__
  #

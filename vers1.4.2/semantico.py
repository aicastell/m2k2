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
# Modulo: semantico
#
# Proposito: implementa la tabla de simbolos y todos los nodos
#            necesarios para la construccion del AST. Con ayuda
#            del AST se realizan las comprobaciones semanticas
#            y la posterior interpretacion.
#
##############################################################################
# Variables:
#     symTable : la tabla de simbolos (global en este modulo)
#
# Clases definidas:
#     SymbolTable       : la tabla de simbolos
#     Attributes        : clase vacia
#     node_Declaracion  : declaracion de variables
#     node_Asignacion   : asignacion de una expresion a un ident.
#     node_Expresion    : su interpretacion se imprime por stdout
#     node_MasBinario   : suma de dos operadores
#     node_MenosBinario : resta de dos operadores
#     node_O            : OR entre dos operadores
#     node_Mul          : multiplicacion de dos operadores
#     node_Div          : division de dos operadores
#     node_Y            : AND entre dos operadores
#     node_PorCien      : resto entre dos operadores
#     node_Cmp          : <,>,<=,>=,=,!=,<> entre dos operadores
#     node_Ident        : identificador
#     node_NrEnter      : numero entero
#     node_NrReal       : numero real
#     node_MasUnario    : signo positivo
#     node_MenosUnario  : cambio de signo
#     node_No           : invertir logica
#     node_OpTorio      : operatorio
#     SemError          : construye mensajes para errores semanticos
##############################################################################

from sys  import stdout, stderr

##############################################################################
# Class SymbolTable
#
# Construye la tabla de simbolos y todos los metodos necesarios para
# su correcta gestion
#
# Implementa los siguientes metodos:
#
# __init__       : es el constructor de la clase. No tiene parametros.
# declare        : declara variable en la tabla de simbolos:
#                  self.buffer[id] = [type, value]
#                   - type  : tipo de la variable (enter o real)
#                   - value : valor de la variable (default enter 0 y default real 0.0)
# isdeclared     : devuelve cierto si id ha sido previamente declarado
# gettype        : devuelve el tipo del id
# getvalue       : devuelve el valor del id
# putvalue       : asigna un valor al id
# setsilent      : establece a id como variable muda
# setnotsilent   : id deja de ser variable muda
# issilent       : devuelve cierto si id es muda en el momento de la consulta
# clearallsilent : despues de su llamada toda variable deja de ser muda
##############################################################################
class SymbolTable:

  def __init__ (self):

    self.buffer={} # tabla de simbolos
    self.silent=[] # variables que actuan como mudas en un momento dado
  # __init__
  #


  def declare(self, type, id):

    if type == "enter":
      self.buffer[id] = [type, 0]

    if type == "real":
      self.buffer[id] = [type, 0.0]
  # declare
  #


  def isdeclared(self, id):

    return self.buffer.has_key(id)
  # isdeclared
  #


  def gettype(self, id):

    return self.buffer[id][0]
  # gettype
  #


  def getvalue(self, id):

    return self.buffer[id][1]
  # getvalue
  #


  def putvalue(self, id, v):

    idtype = self.gettype( id )
    if idtype == "enter":
      self.buffer[id][1] = int(v)
    if idtype == "real":
      self.buffer[id][1] = float(v)
  # putvalue
  #


  def setsilent(self, id):

    self.silent = self.silent + [id]
  # setsilent
  #


  def setnotsilent(self, id):

    del self.silent[self.silent.index(id)]
  # setsilent
  #


  def issilent(self, id):

    if id in self.silent:
      return 1
    return 0
  # issilent
  #


  def clearallsilent(self):

    self.silent=[]
  # clearallsilent
  #


# se crea la tabla de simbolos (global) a este modulo
#
symTable = SymbolTable()


##############################################################################
# Class Attributes
#
# Construye una clase vacia. De esta manera se permite anyadir
# atributos a ella sobre la marcha.
#
# No implementa ningun metodo
##############################################################################
class Attributes:
  pass


##############################################################################
# Class node_Declaracion
#
# Construye un nodo para la declaracion de variables
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la declaracion de las variables
##############################################################################
class node_Declaracion:

  def __init__(self, type, idList):

    self.type      = type
    self.idList    = idList
  # __init__
  #


  def check(self):

    global symTable

    localTable = SymbolTable()
    for id in self.idList:
      # id esta redeclarada en la tabla de simbolos?
      # se comprueba si existe en la tabla de simbolos
      if symTable.isdeclared( id ):
        raise SemError, SemError(id + " previously declared")
      # hay dos variables iguales en esta declaracion?
      # se comprueba si existe en la tabla de simbolos local
      if localTable.isdeclared( id ):
        raise SemError, SemError("multiple " + id + " redeclaration")
      # si no existe en la tabla de simbolos local, se inserta
      localTable.declare( self.type, id )
  # check
  #


  def interpret(self):

    global symTable

    for id in self.idList:
      symTable.declare( self.type, id )
  # interpret
  #


##############################################################################
# Class node_Asignacion
#
# Construye un nodo para la asignacion de una expresion
# a un identificador
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la asignacion
##############################################################################
class node_Asignacion:

  def __init__(self, id, expr):

    self.id = id
    self.expr = expr
  # __init__
  #


  def check(self):

    global symTable

    if not symTable.isdeclared( self.id ):
      raise SemError, SemError(self.id + " undeclared identifier")
    if symTable.gettype( self.id ) == "enter":
      if self.expr.check() == "real":
        raise SemError, SemError( "incorrect typecast in assignment, real " + self.id + " expected" )
  # check
  #


  def interpret(self):

    global symTable

    symTable.putvalue( self.id, self.expr.interpret() )
  # interpret
  #


##############################################################################
# Class node_Expresion
#
# Construye un nodo para la evaluacion de una expresion
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de la expresion
##############################################################################
class node_Expresion:

  def __init__ (self, expr):

    self.expr  = expr
  # __init__
  #


  def check(self):

    return self.expr.check()
  # check
  #


  def interpret(self):
    # se calcula el valor de la expresion y se imprime por stdout
    stdout.write( str(self.expr.interpret()) + '\n' )
  # interpret
  #


##############################################################################
# Class node_MasBinario
#
# Construye un nodo suma (operacion binaria)
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de suma binaria
##############################################################################
class node_MasBinario:

  def __init__(self, term1, term2):

    self.term1 = term1
    self.term2 = term2
  # __init__
  #


  def check(self):

    type1 = self.term1.check()
    if type1 == "real":
      return "real"
    type2 = self.term2.check()
    if type2 == "real":
      return "real"
    return "enter"
  # check
  #


  def interpret(self):

    return( self.term1.interpret() + self.term2.interpret() )
  # interpret
  #


##############################################################################
# Class node_MenosBinario
#
# Construye un nodo resta (operacion binaria)
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de la resta binaria
##############################################################################
class node_MenosBinario:

  def __init__(self, term1, term2):

    self.term1 = term1
    self.term2 = term2
  # __init__
  #


  def check(self):

    type1 = self.term1.check()
    if type1 == "real":
      return "real"
    type2 = self.term2.check()
    if type2 == "real":
      return "real"
    return "enter"
  # check
  #


  def interpret(self):

    return( self.term1.interpret() - self.term2.interpret() )
  # interpret
  #


##############################################################################
# Class node_O
#
# Construye un nodo disyuncion
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del OR
##############################################################################
class node_O:

  def __init__(self, term1, term2):

    self.term1 = term1
    self.term2 = term2
  # __init__
  #


  def check(self):

    type1 = self.term1.check()
    if type1 == "real":
      raise SemError, SemError("expected enter operands in binary \'|\' operator")
    type2 = self.term2.check()
    if type2 == "real":
      raise SemError, SemError("expected enter operands in binary \'|\' operator")
    return "enter"
  # check
  #


  def interpret(self):

    v1 = self.term1.interpret()
    if v1 != 0:
      return 1
    v2 = self.term2.interpret()
    if v2 != 0:
      return 1
    return 0
  # interpret
  #


##############################################################################
# Class node_Mul
#
# Construye un nodo multiplicacion
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de la multiplicacion
##############################################################################
class node_Mul:

  def __init__(self, factor1, factor2):

    self.factor1 = factor1
    self.factor2 = factor2
  # __init__
  #


  def check(self):

    type1 = self.factor1.check()
    if type1 == "real":
      return "real"
    type2 = self.factor2.check()
    if type2 == "real":
      return "real"
    return "enter"
  # check
  #


  def interpret(self):

    return( self.factor1.interpret() * self.factor2.interpret() )
  # interpret
  #


##############################################################################
# Class node_Div
#
# Construye un nodo division
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de la division
##############################################################################
class node_Div:

  def __init__(self, factor1, factor2):

    self.factor1 = factor1
    self.factor2 = factor2
  # __init__
  #


  def check(self):

    type1 = self.factor1.check()
    if type1 == "real":
      return "real"
    type2 = self.factor2.check()
    if type2 == "real":
      return "real"
    return "enter"
  # check
  #


  def interpret(self):

    return( self.factor1.interpret() / self.factor2.interpret() )
  # interpret
  #


##############################################################################
# Class node_Y
#
# Construye un nodo conjuncion
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del AND
##############################################################################
class node_Y:

  def __init__(self, factor1, factor2):

    self.factor1 = factor1
    self.factor2 = factor2
  # __init__
  #


  def check(self):

    type1 = self.factor1.check()
    if type1 == "real":
      raise SemError, SemError("expected enter operands in binary \'&\' operator")
    type2 = self.factor2.check()
    if type2 == "real":
      raise SemError, SemError("expected enter operands in binary \'&\' operator")
    return "enter"
  # check
  #


  def interpret(self):

    v1 = self.factor1.interpret()
    if v1 == 0:
      return 0
    v2 = self.factor2.interpret()
    if v2 == 0:
      return 0
    return 1
  # interpret
  #


##############################################################################
# Class node_PorCien
#
# Construye un nodo para las comparaciones
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del resto
##############################################################################
class node_PorCien:

  def __init__(self, factor1, factor2):

    self.factor1 = factor1
    self.factor2 = factor2
  # __init__
  #


  def check(self):

    type1 = self.factor1.check()
    if type1 == "real":
      raise SemError, SemError("expected enter operands in binary \'%\' operator")
    type2 = self.factor2.check()
    if type2 == "real":
      raise SemError, SemError("expected enter operands in binary \'%\' operator")
    return "enter"
  # check
  #


  def interpret(self):

    return ( self.factor1.interpret() % self.factor2.interpret() )
  # interpret
  #


##############################################################################
# Class node_Cmp
#
# Construye un nodo para las comparaciones
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion de las comparaciones
##############################################################################
class node_Cmp:

  def __init__(self, factor1, cmp, factor2):

    self.factor1 = factor1
    self.factor2 = factor2
    self.cmp = cmp
  # __init__
  #


  def check(self):

    self.factor1.check()
    self.factor2.check()
    return "enter"
  # check
  #


  def interpret(self):

    if self.cmp in ["="]:
      return self.factor1.interpret() == self.factor2.interpret()
    if self.cmp in ["!=", "<>"]:
      return self.factor1.interpret() != self.factor2.interpret()
    if self.cmp in ["<"]:
      return self.factor1.interpret() <  self.factor2.interpret()
    if self.cmp in [">"]:
      return self.factor1.interpret() >  self.factor2.interpret()
    if self.cmp in ["<="]:
      return self.factor1.interpret() <= self.factor2.interpret()
    if self.cmp in [">="]:
      return self.factor1.interpret() >= self.factor2.interpret()
  # interpret
  #


##############################################################################
# Class node_Ident
#
# Construye un nodo suma
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del identificador
##############################################################################
class node_Ident:

  def __init__(self, id):

    self.id = id
  # __init__
  #


  def check(self):

    global symTable

    if not symTable.isdeclared( self.id ):
      raise SemError, SemError(self.id + " undeclared identifier")
    return symTable.gettype( self.id )
  # check
  #


  def interpret(self):

    global symTable

    return symTable.getvalue( self.id )
  # interpret
  #


##############################################################################
# Class node_NrEnter
#
# Construye un nodo para los numeros enteros
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del numero entero
##############################################################################
class node_NrEnter:

  def __init__(self, nr):

    self.nr = nr
  # __init__
  #


  def check(self):

    return "enter"
  # check
  #


  def interpret(self):

    return self.nr
  # interpret
  #


##############################################################################
# Class node_NrReal
#
# Construye un nodo para los numeros reales
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del numero real
##############################################################################
class node_NrReal:

  def __init__(self, nr):

    self.nr = nr
  # __init__
  #


  def check(self):

    return "real"
  # check
  #


  def interpret(self):

    return self.nr
  # interpret
  #


##############################################################################
# Class node_MasUnario
#
# Construye un nodo para conservar el signo del factor. Se podria
# hacer esto sin hacer uso de este nodo, aunque se hace asi para
# mantener un codigo homogeneo, quizas mas claro de entender.
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : lleva a cabo la interpretacion del signo positivo
##############################################################################
class node_MasUnario:

  def __init__(self, factor):

    self.factor = factor
  # __init__
  #


  def check(self):

    return self.factor.check()
  # check
  #


  def interpret(self):

    return( self.factor.interpret() )
  # interpret
  #


##############################################################################
# Class node_MenosUnario
#
# Construye un nodo para cambiar el signo del factor
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : realiza el cambio de signo
##############################################################################
class node_MenosUnario:

  def __init__(self, factor):

    self.factor = factor
  # __init__
  #


  def check(self):

    return self.factor.check()
  # check
  #


  def interpret(self):

    return( - self.factor.interpret() )
  # interpret
  #


##############################################################################
# Class node_No
#
# Construye un nodo para invertir la logica del factor
#
# Implementa los siguientes metodos:
#
# __init__     : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : invierte la logica del factor
##############################################################################
class node_No:

  def __init__(self, factor):

    self.factor = factor
  # __init__
  #


  def check(self):

    type = self.factor.check()
    if type == "real":
      raise SemError, SemError("expected enter operand in unary \'!\' operator")
    return "enter"
  # check
  #


  def interpret(self):

    return( not self.factor.interpret() )
  # interpret
  #


##############################################################################
# Class node_OpTorio
#
# Construye un nodo para el operatorio
#
# Implementa los siguientes metodos:
#
# __init__  : es el constructor de la clase
# check     : realiza las comprobaciones semanticas
# interpret : invierte la logica del factor
##############################################################################
class node_OpTorio:

  def __init__(self, optor, id, expr1, expr2, expr3):

    self.optor = optor
    self.id    = id
    self.expr1 = expr1
    self.expr2 = expr2
    self.expr3 = expr3
  # __init__
  #


  def check(self):

    global symTable

    if not symTable.isdeclared( self.id ):
      raise SemError, SemError(self.id + " undeclared silent identifier in \'" + self.optor + "\' operatory")

    if symTable.gettype( self.id ) == "real":
      raise SemError, SemError( "expected enter type for " + self.id + " silent identifier in \'" + self.optor + "\' operatory")

    type1 = self.expr1.check()
    if type1 == "real":
      raise SemError, SemError("expected enter type for expr1 in \'" + self.optor + "\' operatory")

    type2 = self.expr2.check()
    if type2 == "real":
      raise SemError, SemError("expected enter type for expr2 in \'" + self.optor + "\' operatory")

    if symTable.issilent( self.id ):
      raise SemError, SemError( "silent identifier \'" + self.id + "\' inside \'" + self.optor + "\' operatory is already in use")

    symTable.setsilent(self.id)
    type3 = self.expr3.check()
    symTable.setnotsilent(self.id)

    if self.optor in ["(+)", "(-)", "(*)", "(/)"]:
      return type3
    if self.optor in ["(%)", "(&)", "(|)"]:
      if type3 == "real":
        raise SemError, SemError("expected enter type for expr3 in \'" + self.optor + "\' operatory")
      return "enter"
  # check
  #


  def interpret(self):

    global symTable

    e1 = self.expr1.interpret()
    e2 = self.expr2.interpret()

    symTable.putvalue( self.id, e1 )
    res = self.expr3.interpret()
    for i in range( e1+1, e2+1 ):
      if self.optor == "(+)":
        symTable.putvalue( self.id, i )
        res = res + self.expr3.interpret()
      if self.optor == "(-)":
        symTable.putvalue( self.id, i )
        res = res - self.expr3.interpret()
      if self.optor == "(*)":
        symTable.putvalue( self.id, i )
        res = res * self.expr3.interpret()
      if self.optor == "(/)":
        symTable.putvalue( self.id, i )
        res = res / self.expr3.interpret()
      if self.optor == "(%)":
        symTable.putvalue( self.id, i )
        res = res % self.expr3.interpret()
      if self.optor == "(&)":
        if res == 0:
          break
        symTable.putvalue( self.id, i )
        res = res and self.expr3.interpret()
      if self.optor == "(|)":
        if res != 0:
          break
        symTable.putvalue( self.id, i )
        res = res or self.expr3.interpret()

    if self.optor in ["(&)", "(|)"]:
      if res != 0:
        res = 1

    return res
  # interpret
  #


##############################################################################
# Class SemError
#
# Construye un mensaje de error semantico para imprimir por stderr
#
# Implementa los siguientes metodos:
#
# __init__ : es el constructor de la clase. Tiene el siguiente
#            parametro:
#             - message : el mensaje de error
# __str__  : construye la cadena que se imprime por stderr
##############################################################################
class SemError:

  def __init__(self, message):

    global symTable

    symTable.clearallsilent()
    self.msg  = message
  # __init__
  #


  def __str__(self):

    s = ""
    s = s + "Semantic Error: "
    s = s + self.msg + '\n\n'
    return s
  # __str__
  #

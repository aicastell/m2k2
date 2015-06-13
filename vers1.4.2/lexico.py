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
# Modulo: lexico
#
# Proposito: implementa el analizador lexico del interprete
#
#
##############################################################################
# Variables globales:
#     movement : los movimientos posibles de q con c
#     final    : los estados finales
#     action   : el estado emite u omite?
#     category : las categorias lexicas de cada estado final
#
# Clases definidas:
#     Token       : los tokens que se pasan al analizador sintactico
#     LexAnalyser : el analizador lexico
#     LexError    : construye los mensajes para errores lexicos
##############################################################################

from string import lower,  atoi,  atof
from sys    import stdout, stderr

# se carga la tabla de movimientos de la MDD
# movement [ (estado, caracter) ] = estado
movement = {}

# desde 0 lectura de [a-zA-Z]
#
ascii=ord('a')
while ascii<=ord('z'):
  movement[ (0,chr(ascii)) ] = 1
  ascii=ascii+1

ascii=ord('A')
while ascii<=ord('Z'):
  movement[ (0,chr(ascii)) ] = 1
  ascii=ascii+1

# desde 1 lectura de [a-zA-Z0-9_]
#
ascii=ord('a')
while ascii<=ord('z'):
  movement[ (1,chr(ascii)) ] = 1
  ascii=ascii+1

ascii=ord('A')
while ascii<=ord('Z'):
  movement[ (1,chr(ascii)) ] = 1
  ascii=ascii+1

ascii=ord('0')
while ascii<=ord('9'):
  movement[ (1,chr(ascii)) ] = 1
  ascii=ascii+1

ascii=ord('_')
movement[ (1,chr(ascii)) ] = 1

# desde 0 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (0,chr(ascii)) ] = 2
  ascii=ascii+1

# desde 2 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (2,chr(ascii)) ] = 2
  ascii=ascii+1

# desde 2 lectura de .
#
ascii=ord('.')
movement[ (2,chr(ascii)) ] = 3

# desde 3 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (3,chr(ascii)) ] = 4
  ascii=ascii+1

# desde 4 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (4,chr(ascii)) ] = 4
  ascii=ascii+1

# desde 4 lectura de [eE]
#
ascii=ord('e')
movement[ (4,chr(ascii)) ] = 5
ascii=ord('E')
movement[ (4,chr(ascii)) ] = 5

# desde 5 lectura de [+-]
#
ascii=ord('+')
movement[ (5,chr(ascii)) ] = 6
ascii=ord('-')
movement[ (5,chr(ascii)) ] = 6

# desde 5 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (5,chr(ascii)) ] = 7
  ascii=ascii+1

# desde 6 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (6,chr(ascii)) ] = 7
  ascii=ascii+1

# desde 7 lectura de [0-9]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (7,chr(ascii)) ] = 7
  ascii=ascii+1

# desde 0 lectura de #
#
ascii=ord('#')
movement[ (0,chr(ascii)) ] = 8

# desde 8 lectura de [0-9a-fA-F]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (8,chr(ascii)) ] = 9
  ascii=ascii+1

ascii=ord('a')
while ascii<=ord('f'):
  movement[ (8,chr(ascii)) ] = 9
  ascii=ascii+1

ascii=ord('A')
while ascii<=ord('F'):
  movement[ (8,chr(ascii)) ] = 9
  ascii=ascii+1

# desde 9 lectura de [0-9a-fA-F]
#
ascii=ord('0')
while ascii<=ord('9'):
  movement[ (9,chr(ascii)) ] = 9
  ascii=ascii+1

ascii=ord('a')
while ascii<=ord('f'):
  movement[ (9,chr(ascii)) ] = 9
  ascii=ascii+1

ascii=ord('A')
while ascii<=ord('F'):
  movement[ (9,chr(ascii)) ] = 9
  ascii=ascii+1

# desde 0 lectura de (
#
ascii=ord('(')
movement[ (0,chr(ascii)) ] = 10

# desde 10 lectura de [+-*/%&|]
#
ascii=ord('+')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('-')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('*')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('/')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('%')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('&')
movement[ (10,chr(ascii)) ] = 11
ascii=ord('|')
movement[ (10,chr(ascii)) ] = 11

# desde 11 lectura de )
#
ascii=ord(')')
movement[ (11,chr(ascii)) ] = 12

# desde 0 lectura de )
#
ascii=ord(')')
movement[ (0,chr(ascii)) ] = 13

# desde 0 lectura de .
#
ascii=ord('.')
movement[ (0,chr(ascii)) ] = 14

# desde 14 lectura de .
#
ascii=ord('.')
movement[ (14,chr(ascii)) ] = 15

# desde 0 lectura de [ \t]
#
ascii=ord(' ')
movement[ (0,chr(ascii)) ] = 16
ascii=ord('\t')
movement[ (0,chr(ascii)) ] = 16

# desde 0 lectura de ,
#
ascii=ord(',')
movement[ (0,chr(ascii)) ] = 17

# desde 0 lectura de \n
#
ascii=ord('\n')
movement[ (0,chr(ascii)) ] = 18

# desde 0 lectura de +
#
ascii=ord('+')
movement[ (0,chr(ascii)) ] = 19

# desde 0 lectura de -
#
ascii=ord('-')
movement[ (0,chr(ascii)) ] = 20

# desde 0 lectura de *
#
ascii=ord('*')
movement[ (0,chr(ascii)) ] = 21

# desde 0 lectura de /
#
ascii=ord('/')
movement[ (0,chr(ascii)) ] = 22

# desde 0 lectura de %
#
ascii=ord('%')
movement[ (0,chr(ascii)) ] = 23

# desde 0 lectura de &
#
ascii=ord('&')
movement[ (0,chr(ascii)) ] = 24

# desde 0 lectura de |
#
ascii=ord('|')
movement[ (0,chr(ascii)) ] = 25

# desde 0 lectura de !
#
ascii=ord('!')
movement[ (0,chr(ascii)) ] = 26

# desde 0 lectura de >
#
ascii=ord('>')
movement[ (0,chr(ascii)) ] = 27

# desde 0 lectura de <
#
ascii=ord('<')
movement[ (0,chr(ascii)) ] = 28

# desde 0 lectura de =
#
ascii=ord('=')
movement[ (0,chr(ascii)) ] = 29

# desde 26 lectura de =
#
ascii=ord('=')
movement[ (26,chr(ascii)) ] = 29

# desde 27 lectura de =
#
ascii=ord('=')
movement[ (27,chr(ascii)) ] = 29

# desde 28 lectura de [>=]
#
ascii=ord('>')
movement[ (28,chr(ascii)) ] = 29
ascii=ord('=')
movement[ (28,chr(ascii)) ] = 29

# desde 28 lectura de -
#
ascii=ord('-')
movement[ (28,chr(ascii)) ] = 30

# se carga la tabla de acciones de la MDD
# action[ estado ] = accion
action={}
action[ 1 ]  = "emitir"
action[ 2 ]  = "emitir"
action[ 3 ]  = "emitir"
action[ 4 ]  = "emitir"
action[ 5 ]  = "emitir"
action[ 6 ]  = "emitir"
action[ 7 ]  = "emitir"
action[ 8 ]  = "emitir"
action[ 9 ]  = "emitir"
action[ 10 ] = "emitir"
action[ 11 ] = "emitir"
action[ 12 ] = "emitir"
action[ 13 ] = "emitir"
action[ 14 ] = "emitir"
action[ 15 ] = "emitir"
action[ 16 ] = "omitir"  ## solo se omite este
action[ 17 ] = "emitir"
action[ 18 ] = "emitir"
action[ 19 ] = "emitir"
action[ 20 ] = "emitir"
action[ 21 ] = "emitir"
action[ 22 ] = "emitir"
action[ 23 ] = "emitir"
action[ 24 ] = "emitir"
action[ 25 ] = "emitir"
action[ 26 ] = "emitir"
action[ 27 ] = "emitir"
action[ 28 ] = "emitir"
action[ 29 ] = "emitir"
action[ 30 ] = "emitir"

# se carga la tabla de estados finales de la MDD
# final[ estado ] = [01]
final={}
final[ 0 ]  = 0
final[ 1 ]  = 1
final[ 2 ]  = 1
final[ 3 ]  = 0
final[ 4 ]  = 1
final[ 5 ]  = 0
final[ 6 ]  = 0
final[ 7 ]  = 1
final[ 8 ]  = 0
final[ 9 ]  = 1
final[ 10 ] = 1
final[ 11 ] = 0
final[ 12 ] = 1
final[ 13 ] = 1
final[ 14 ] = 0
final[ 15 ] = 1
final[ 16 ] = 1
final[ 17 ] = 1
final[ 18 ] = 1
final[ 19 ] = 1
final[ 20 ] = 1
final[ 21 ] = 1
final[ 22 ] = 1
final[ 23 ] = 1
final[ 24 ] = 1
final[ 25 ] = 1
final[ 26 ] = 1
final[ 27 ] = 1
final[ 28 ] = 1
final[ 29 ] = 1
final[ 30 ] = 1

# se carga la tabla de categoria lexicas
# category[ estado ] = categoria lexica
category={}
category[ 1 ]  = "tkIdent"
category[ 2 ]  = "tkNrEnter"
category[ 4 ]  = "tkNrReal"
category[ 7 ]  = "tkNrReal"
category[ 9 ]  = "tkNrEnter"
category[ 10 ] = "tkAbrPar"
category[ 12 ] = "tkOpTorio"
category[ 13 ] = "tkCiePar"
category[ 15 ] = "tkPtoPto"
category[ 16 ] = "tkSpc"
category[ 17 ] = "tkComa"
category[ 18 ] = "tkEOL"
category[ 19 ] = "tkMas"
category[ 20 ] = "tkMenos"
category[ 21 ] = "tkMul"
category[ 22 ] = "tkDiv"
category[ 23 ] = "tkPorCien"
category[ 24 ] = "tkY"
category[ 25 ] = "tkO"
category[ 26 ] = "tkNo"
category[ 27 ] = "tkCmp"
category[ 28 ] = "tkCmp"
category[ 29 ] = "tkCmp"
category[ 30 ] = "tkAsign"


##############################################################################
# Class token
#
# Implementa los siguientes metodos:
#
# __init__ : es el constructor de la clase. Tiene los siguientes
#            parametros:
#
#             - cat  : categoria lexica de este token
#             - lex  : lexema de este token
#             - chr1 : caracter de la linea en el q empieza el token
##############################################################################
class Token:

  def __init__(self, cat, lex, chr1):

    self.cat  = cat
    self.chr1 = chr1

    # Se asigna el lexema a los tokens que lo necesitan
    # Es necesario conocer el lexema de un tkIdent (obviamente)
    # El lexema de tkCmp y de tkOpTorio se almacena porque al agrupar
    # varios operadores en un solo token, la unica forma de saber cual
    # es el operador que se aplica es a traves de su lexema.
    if self.cat in ["tkIdent", "tkCmp", "tkOpTorio"]:
      self.lex = lex

    # se distingue identificador de palabra reservada
    if self.cat == "tkIdent":
      if lower(self.lex) == "enter":
        self.cat = "tkTpoEnter"
      if lower(self.lex) == "real":
        self.cat = "tkTpoReal"

    # se calcula el atributo val(or) para los enteros y para los reales
    if self.cat == "tkNrEnter":
      if lex[0]=='#':
        self.val = atoi("0x"+lex[1:], 16)
      else:
        self.val = atoi(lex)
    if self.cat == "tkNrReal":
      self.val = atof(lex)
  # __init_
  #


##############################################################################
# Class LexAnalyser
#
# Implementa los siguientes metodos:
#
# __init__          : es el constructor de la clase. Tiene los
#                     siguientes parametros:
#                      - fis        : nombre del file input stream
#                      - sentence   : linea analizada
#                      - sentenceNr : numero de linea analizada
# getCurrentChar    : devuelve el caracter actual de la entrada
# pointNextChar     : avanza un caracter en la entrada
# pointPreviousChar : devuelve un caracter a la entrada
# getNextToken      : devuelve el siguiente token de la entrada
##############################################################################
class LexAnalyser:

  def __init__(self, fis, sentence, sentenceNr):

    self.s    = sentence      # sentencia analizada
    self.s    = self.s + '\n' # permite finalizacion con ctrl+D !?
    self.sNr  = sentenceNr    # numero de la Sentencia analizada
    self.fis  = fis           # nombre del fichero de entrada
    self.cPtr = 0             # puntero al Caracter actual analizado
  # __init__
  #


  def getCurrentChar(self):

    return self.s[self.cPtr]
  # getCurrentChar
  #


  def pointNextChar(self):

    if (self.cPtr+1) < len(self.s):
      self.cPtr = self.cPtr+1
  # pointNextChar
  #


  def pointPreviousChar(self):

    if self.cPtr > 0:
      self.cPtr = self.cPtr - 1
  # pointPreviousChar
  #


  def getNextToken(self):

    global movement
    global action
    global final
    global category
    undefined = -1
    q0        = 0                     # estado inicial
    q         = q0                    # estado actual
    l         = ""                    # lexema
    uf        = undefined             # ultimo estado final
    ul        = ""                    # lexema leido hasta uf
    c         = self.getCurrentChar() # siguiente caracter
    chr1      = self.cPtr             # primer caracter del token

    while 1:
      if movement.has_key( (q,c) ): # si movement[q,c] <> undefined
        l = l + c
        q = movement[ (q, c) ]
        self.pointNextChar()
        c = self.getCurrentChar()
        if final[q]:
          uf = q
          ul = l
      else:
        # si no hay movimiento posible y se ha pasado por algun estado final
        if uf != undefined:
          # se devuelven los caracteres leidos sobrantes a la entrada
          for i in range(len(l)-len(ul)):
            self.pointPreviousChar()

          if action[uf] == "omitir":
            # se inicializa todo para iniciar la captura de un nuevo token
            # en la siguiente iteracion.
            q  = q0
            l  = ""
            uf = undefined
            ul = ""
            chr1 = self.cPtr
          else:
            # emitir
            return Token( category[uf], ul, chr1 )
        else:
          # tratar error (lectura de un solo '.', de una 'enye', de un ':', etc.).
          # Se lanza una excepcion que es capturada en el main (m2k2.py)
          raise LexError, LexError(self.fis, self.s[:-2], self.sNr, self.cPtr, "invalid syntax")
  # getNextToken
  #


##############################################################################
# Class LexError
#
# Construye un mensaje de error lexico para imprimir por stderr
#
# Implementa los siguientes metodos:
#
# __init__ : es el constructor de la clase. Tiene los siguientes
#            parametros:
#             - fis        : nombre del file input stream
#             - sentence   : linea analizada
#             - sentenceNr : numero de linea analizada
#             - chr1       : caracter d sentence en el q ocurre error
#             - message    : el mensaje de error
# __str__  : construye la cadena que se imprime por stderr
##############################################################################
class LexError:

  def __init__(self, fis, sentence, sentenceNr, chr1, message):

    self.fis  = fis
    self.s    = sentence
    self.sNr  = sentenceNr
    self.chr1 = chr1
    self.msg  = message
  # __init__
  #


  def __str__(self):

    s = ""
    s = s + 'File \"<' + self.fis + '>\", line ' + str(self.sNr) + '\n'
    s = s + self.s + '\n'
    for i in range(self.chr1):
      s = s + ' '
    s = s + '^' + '\n'
    s = s + "Lexic Error: "
    s = s + self.msg + '\n\n'
    return s
  # __str__
  #

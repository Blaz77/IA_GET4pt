from interfaz import Interfaz


if 64 - 64: i11iIiiIii
from constantes import *
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
class Tablero ( object ) :
 """Clase que representa el tablero de juego."""
 if 73 - 73: II111iiii
 if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i

 def __init__ ( self , continentes , limitrofes ) :
  """Crea un tablero desde un diccionario de continentes con su
  lista de paises, y un diccionario de paises y su lista de
  limitrofes."""

  if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
  if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
  if 46 - 46: ooOoO0o * I11i - OoooooooOO
  if 30 - 30: o0oOOo0O0Ooo - O0 % o0oOOo0O0Ooo - OoooooooOO * O0 * OoooooooOO
  self . continentes = continentes
  self . limitrofes = limitrofes
  if 60 - 60: iIii1I11I1II1 / i1IIi * oO0o - I1ii11iIi11i + o0oOOo0O0Ooo
  self . _paises = { }
  for ooO0oo0oO0 in limitrofes . keys ( ) :
   self . _paises [ ooO0oo0oO0 ] = None
   if 100 - 100: i1IIi

 def ocupar_pais ( self , pais , color , ejercitos = 1 ) :
  """Ocupa el pais indicado con ejercitos del color."""

  self . _paises [ pais ] = ( color , ejercitos )
  if 27 - 27: IiII * OoooooooOO + I11i * ooOoO0o - i11iIiiIii - iII111i
  if 30 - 30: iIii1I11I1II1 * iIii1I11I1II1 . II111iiii - oO0o

 def asignar_ejercitos ( self , pais , ejercitos ) :
  """Suma o resta una cantidad de ejercitos en el pais indicado."""

  self . _paises [ pais ] = ( self . _paises [ pais ] [ 0 ] , self . _paises [ pais ] [ 1 ] + ejercitos )
  if 72 - 72: II111iiii - OoOoOO00
  if 91 - 91: OoO0O00 . i11iIiiIii / oO0o % I11i / OoO0O00 - i11iIiiIii
  if 8 - 8: o0oOOo0O0Ooo * I1ii11iIi11i * iIii1I11I1II1 . IiII / IiII % IiII

 def actualizar_interfaz ( self , agregados = None ) :
  """Redibuja interfaz grafica. Puede recibir un diccionario de
  paises y numero de ejercitos que se adicionan o sustraen a los
  que estan ubicados en el tablero.
  Por ejemplo, si el diccionario fuera
  {'Argentina': -1, 'Brasil': 1}, el tablero se dibujaria con un
  ejercito menos en Argentina y uno mas en Brasil."""

  i11 = { }
  if 41 - 41: I1Ii111 . ooOoO0o * IiII % i11iIiiIii
  if 74 - 74: iII111i * IiII
  if 82 - 82: iIii1I11I1II1 % IiII
  if 86 - 86: OoOoOO00 % I1IiiI
  if 80 - 80: OoooooooOO . I1IiiI
  if 87 - 87: oO0o / ooOoO0o + I1Ii111 - ooOoO0o . ooOoO0o / II111iiii
  for ooO0oo0oO0 in self . _paises :
   if agregados and ooO0oo0oO0 in agregados :
    i11 [ ooO0oo0oO0 ] = ( self . _paises [ ooO0oo0oO0 ] [ 0 ] , self . _paises [ ooO0oo0oO0 ] [ 1 ] + agregados [ ooO0oo0oO0 ] )
   else :
    i11 [ ooO0oo0oO0 ] = self . _paises [ ooO0oo0oO0 ]
  # chin chun i11 yen yuan
  Interfaz.actualizar2(i11)
  return i11
  if 11 - 11: I1IiiI % o0oOOo0O0Ooo - Oo0Ooo

 def color_pais ( self , pais ) :
  """Devuelve el color de un pais."""

  return self . _paises [ pais ] [ 0 ]
  if 58 - 58: i11iIiiIii % I1Ii111
  if 54 - 54: OOooOOo % O0 + I1IiiI - iII111i / I11i

 def ejercitos_pais ( self , pais ) :
  """Devuelve la cantidad ejercitos en un pais."""

  return self . _paises [ pais ] [ 1 ]
  if 31 - 31: OoO0O00 + II111iiii
  if 13 - 13: OOooOOo * oO0o * I1IiiI

 def paises ( self , continente = '' ) :
  """Devuelve la lista de paises en un continente, o todos
  los paises si continente es vacio"""

  if continente :
   if 55 - 55: II111iiii
   return self . continentes [ continente ]
  return self . _paises . keys ( )
  if 43 - 43: OoOoOO00 - i1IIi + I1Ii111 + Ii1I

 def paises_limitrofes ( self , pais ) :
  """Devuelve la lista de paises limitrofes de un pais."""

  return self . limitrofes [ pais ]
  if 17 - 17: o0oOOo0O0Ooo
  if 64 - 64: Ii1I % i1IIi % OoooooooOO

 def es_limitrofe ( self , pais1 , pais2 ) :
  """Informa si dos paises son limitrofes."""

  return pais1 in self . limitrofes [ pais2 ]
  if 3 - 3: iII111i + O0
  if 42 - 42: OOooOOo / i1IIi + i11iIiiIii - Ii1I

 def cantidad_paises ( self ) :
  """Informa la cantidad de paises totales."""

  return len ( self . _paises )
  if 78 - 78: OoO0O00
  if 18 - 18: O0 - iII111i / iII111i + ooOoO0o % ooOoO0o - IiII

 def cantidad_paises_continente ( self , continente ) :
  """Informa la cantidad de paises en continente."""

  return len ( self . continentes [ continente ] )
  if 62 - 62: iII111i - IiII - OoOoOO00 % i1IIi / oO0o
  if 77 - 77: II111iiii - II111iiii . I1IiiI / o0oOOo0O0Ooo

 def continente_pais ( self , pais ) :
  """Informa el continente de un pais."""

  for i1iIIIiI1I in self . continentes :
   if 70 - 70: Oo0Ooo % Oo0Ooo . IiII % OoO0O00 * o0oOOo0O0Ooo % oO0o
   if pais in i1iIIIiI1I :
    return i1iIIIiI1I
    if 23 - 23: i11iIiiIii + I1IiiI

 def paises_color ( self , color ) :
  """Devuelve la lista de paises con ejercitos del color."""

  i11 = [ ]
  if 68 - 68: OoOoOO00 . oO0o . i11iIiiIii
  for ooO0oo0oO0 in self . _paises :
   if self . _paises [ ooO0oo0oO0 ] [ 0 ] == color :
    i11 . append ( ooO0oo0oO0 )
  return i11
  if 40 - 40: oO0o . OoOoOO00 . Oo0Ooo . i1IIi
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3

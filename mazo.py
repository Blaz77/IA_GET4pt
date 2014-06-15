if 64 - 64: i11iIiiIii
from constantes import *
import random
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
class Tarjeta ( object ) :
 if 73 - 73: II111iiii
 if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
 def __init__ ( self , pais , tipo ) :
  self . pais = pais
  if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
  self . tipo = tipo
  if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
 def __repr__ ( self ) : return str ( self )
 if 46 - 46: ooOoO0o * I11i - OoooooooOO
 def __str__ ( self ) :
  return "(%s, %s)" % ( self . pais , NOMBRE_TARJETAS [ self . tipo ] )
  if 30 - 30: o0oOOo0O0Ooo - O0 % o0oOOo0O0Ooo - OoooooooOO * O0 * OoooooooOO
  if 60 - 60: iIii1I11I1II1 / i1IIi * oO0o - I1ii11iIi11i + o0oOOo0O0Ooo
class Mazo ( object ) :
 if 94 - 94: i1IIi % Oo0Ooo
 if 68 - 68: Ii1I / O0
 def __init__ ( self , paises_por_tarjeta ) :
  self . devueltas = [ ]
  if 46 - 46: O0 * II111iiii / IiII * Oo0Ooo * iII111i . I11i
  if 62 - 62: i11iIiiIii - II111iiii % I1Ii111 - iIii1I11I1II1 . I1ii11iIi11i . II111iiii
  if 61 - 61: oO0o / OoOoOO00 / iII111i * OoO0O00 . II111iiii
  self . tarjetas = [ ]
  for Ii1IIii11 in paises_por_tarjeta :
   for Oooo0000 in paises_por_tarjeta [ Ii1IIii11 ] :
    self . tarjetas . append ( Tarjeta ( Oooo0000 , Ii1IIii11 ) )
    if 22 - 22: Ii1I . IiII
  random . shuffle ( self . tarjetas )
  if 41 - 41: I1Ii111 . ooOoO0o * IiII % i11iIiiIii
 def sacar_tarjeta ( self ) :
  if not self . tarjetas :
   if 74 - 74: iII111i * IiII
   if 82 - 82: iIii1I11I1II1 % IiII
   if 86 - 86: OoOoOO00 % I1IiiI
   self . tarjetas = self . devueltas
   random . shuffle ( self . tarjetas )
   self . devueltas = [ ]
   if 80 - 80: OoooooooOO . I1IiiI
  return self . tarjetas . pop ( )
  if 87 - 87: oO0o / ooOoO0o + I1Ii111 - ooOoO0o . ooOoO0o / II111iiii
 def devolver_tarjeta ( self , tarjeta ) :
  self . devueltas . append ( tarjeta )
  if 11 - 11: I1IiiI % o0oOOo0O0Ooo - Oo0Ooo
  if 58 - 58: i11iIiiIii % I1Ii111
  if 54 - 54: OOooOOo % O0 + I1IiiI - iII111i / I11i
  if 31 - 31: OoO0O00 + II111iiii
 def cantidad_tarjetas ( self ) :
  return len ( self . tarjetas ) + len ( self . devueltas )
  if 13 - 13: OOooOOo * oO0o * I1IiiI
  if 55 - 55: II111iiii
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3

import random
import time
import math
if 64 - 64: i11iIiiIii
from constantes import *
from mazo import Mazo
from tablero import Tablero
from dados import Dados
import paises as paises
import partida
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
import sys
if '-t' in sys . argv :
 from interfaz_texto import Interfaz
else :
 from interfaz_tk import Interfaz
 if 73 - 73: II111iiii
 if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
 if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
 if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
if '-s' in sys . argv :
 i1I1ii1II1iII = int ( sys . argv [ sys . argv . index ( '-s' ) + 1 ] )
else :
 import time
 i1I1ii1II1iII = int ( time . time ( ) )
random . seed ( i1I1ii1II1iII )
print 'Usando la semills %d' % ( i1I1ii1II1iII , )
print 'Para repetir la simulacion ejecutar el comando: python teg.py -s %d %s' % ( i1I1ii1II1iII , '-t' if '-t' in sys . argv else '' )
print
if 86 - 86: ooOoO0o
class i1ii1iIII ( object ) :
 def __init__ ( self ) :
  if 59 - 59: i1IIi * i1IIi % OOooOOo + II111iiii
  self . usadas = { }
  self . todas = { }
  self . canjes = 0
  if 32 - 32: OoOoOO00 . ooOoO0o * i1IIi . I1Ii111 / IiII
 def por_tipo ( self ) :
  if 88 - 88: iII111i . oO0o % ooOoO0o
  if 66 - 66: iII111i
  if 30 - 30: iIii1I11I1II1 * iIii1I11I1II1 . II111iiii - oO0o
  ooO00oOoo = { }
  for O0OOo in NOMBRE_TARJETAS :
   ooO00oOoo [ O0OOo ] = [ II1Iiii1111i for II1Iiii1111i in self . todas . values ( ) if II1Iiii1111i . tipo == O0OOo ]
  return ooO00oOoo
  if 25 - 25: Ii1I
class oo00000o0 ( object ) :
 def __init__ ( self ) :
  if 34 - 34: IiII % II111iiii % iIii1I11I1II1 % IiII * iII111i / OoOoOO00
  self . mazo = Mazo ( paises . paises_por_tarjeta )
  self . dados = Dados ( )
  self . tablero = Tablero ( paises . paises_por_continente , paises . paises_limitrofes )
  self . tarjetas = { }
  Interfaz . iniciar ( paises . coordenadas_de_paises , paises . archivo_tablero , paises . color_tablero )
  self . jugadores = [ ]
  if 31 - 31: i11iIiiIii / I1IiiI / ooOoO0o * oO0o / Oo0Ooo
 def configurar_el_juego ( self , jugadores ) :
  if 99 - 99: iIii1I11I1II1 * OoooooooOO * II111iiii * iIii1I11I1II1
  if 44 - 44: oO0o / Oo0Ooo - II111iiii - i11iIiiIii % I1Ii111
  Interfaz . setear_titulo ( 'Configurando el juego' )
  if 54 - 54: OOooOOo % O0 + I1IiiI - iII111i / I11i
  for iIiiI1 in jugadores :
   self . jugadores . append ( iIiiI1 )
   self . tarjetas [ iIiiI1 ] = i1ii1iIII ( )
   if 68 - 68: I1IiiI - i11iIiiIii - OoO0O00 / OOooOOo - OoO0O00 + i1IIi
 def repartir_paises ( self ) :
  if 48 - 48: OoooooooOO % o0oOOo0O0Ooo . I1IiiI - Ii1I % i1IIi % OoooooooOO
  if 3 - 3: iII111i + O0
  if 42 - 42: OOooOOo / i1IIi + i11iIiiIii - Ii1I
  Interfaz . setear_titulo ( 'Repartiendo paises iniciales' )
  if 78 - 78: OoO0O00
  Iii1I111 = self . mazo . cantidad_tarjetas ( )
  OO0O0O00OooO = len ( self . jugadores )
  if 77 - 77: II111iiii - II111iiii . I1IiiI / o0oOOo0O0Ooo
  for iIiiI1 in self . jugadores * ( Iii1I111 / OO0O0O00OooO ) + random . sample ( self . jugadores , Iii1I111 % OO0O0O00OooO ) :
   if 14 - 14: I11i % O0
   if 41 - 41: i1IIi + I1Ii111 + OOooOOo - IiII
   II1Iiii1111i = self . mazo . sacar_tarjeta ( )
   self . tablero . ocupar_pais ( II1Iiii1111i . pais , iIiiI1 . color , 1 )
   self . mazo . devolver_tarjeta ( II1Iiii1111i )
   if 77 - 77: Oo0Ooo . IiII % ooOoO0o
 def agregar_ejercitos_inicial ( self , inicia_ronda ) :
  if 42 - 42: oO0o - i1IIi / i11iIiiIii + OOooOOo + OoO0O00
  if 17 - 17: oO0o . Oo0Ooo . I1ii11iIi11i
  Interfaz . setear_titulo ( 'Incorporando ejercitos' )
  if 3 - 3: OoOoOO00 . Oo0Ooo . I1IiiI / Ii1I
  IiiiI1II1I1 = int ( math . ceil ( self . tablero . cantidad_paises ( ) / 10.0 ) )
  oo = int ( math . ceil ( self . tablero . cantidad_paises ( ) / 20.0 ) )
  if 13 - 13: i1IIi - Ii1I % oO0o / iIii1I11I1II1 % iII111i
  for ooO0o0Oo in ( IiiiI1II1I1 , oo ) :
   for Oo00OOOOO in range ( len ( self . jugadores ) ) :
    iIiiI1 = self . jugadores [ ( inicia_ronda + Oo00OOOOO ) % len ( self . jugadores ) ]
    O0O = iIiiI1 . agregar_ejercitos ( self . tablero , { "" : ooO0o0Oo } )
    assert sum ( O0O . values ( ) ) == ooO0o0Oo
    for O00o0OO in O0O :
     assert ( self . tablero . color_pais ( O00o0OO ) == iIiiI1 . color )
     self . tablero . asignar_ejercitos ( O00o0OO , O0O [ O00o0OO ] )
     if 44 - 44: IiII / O0 % i1IIi * oO0o + Oo0Ooo
 def realizar_fase_ataque ( self , jugador ) :
  if 3 - 3: i1IIi / I1IiiI % I11i * i11iIiiIii / O0 * I11i
  if 49 - 49: oO0o % Ii1I + i1IIi . I1IiiI % I1ii11iIi11i
  if 48 - 48: I11i + I11i / II111iiii / iIii1I11I1II1
  if 20 - 20: o0oOOo0O0Ooo
  Interfaz . setear_titulo ( '%s ataca' % jugador )
  oO00 = [ ]
  while True :
   ooo = jugador . atacar ( self . tablero , oO00 )
   if not ooo :
    break
   ii1I1i1I , OOoo0O0 = ooo
   if 41 - 41: oO0o
   assert ( self . tablero . es_limitrofe ( ii1I1i1I , OOoo0O0 ) )
   assert ( self . tablero . ejercitos_pais ( ii1I1i1I ) > 1 )
   if 6 - 6: I1ii11iIi11i
   self . dados . lanzar_dados ( self . tablero . ejercitos_pais ( ii1I1i1I ) , self . tablero . ejercitos_pais ( OOoo0O0 ) )
   self . tablero . asignar_ejercitos ( ii1I1i1I , - self . dados . ejercitos_perdidos_atacante ( ) )
   self . tablero . asignar_ejercitos ( OOoo0O0 , - self . dados . ejercitos_perdidos_atacado ( ) )
   if 31 - 31: Ii1I . Ii1I - o0oOOo0O0Ooo / OoO0O00 + ooOoO0o * I1IiiI
   if self . tablero . ejercitos_pais ( OOoo0O0 ) == 0 :
    oO00 . append ( OOoo0O0 )
    O0ooOooooO = jugador . mover ( ii1I1i1I , OOoo0O0 , self . tablero , oO00 )
    assert 1 <= O0ooOooooO <= 3
    self . tablero . asignar_ejercitos ( ii1I1i1I , - O0ooOooooO )
    self . tablero . ocupar_pais ( OOoo0O0 , jugador . color , O0ooOooooO )
    if 60 - 60: I11i / I11i
  return oO00
  if 46 - 46: Ii1I * OOooOOo - OoO0O00 * oO0o - I1Ii111
 def realizar_fase_reagrupamiento ( self , jugador , paises_ganados ) :
  if 83 - 83: OoooooooOO
  if 31 - 31: II111iiii - OOooOOo . I1Ii111 % OoOoOO00 - O0
  Interfaz . setear_titulo ( '%s reagrupa' % jugador )
  iii11 = jugador . reagrupar ( self . tablero , paises_ganados )
  if 58 - 58: OOooOOo * i11iIiiIii / OoOoOO00 % I1Ii111 - I1ii11iIi11i / oO0o
  if 50 - 50: I1IiiI
  Ii1i11IIii1I = { }
  for OOOoO0O0o , O0o0Ooo , ooO0o0Oo in iii11 :
   assert ( self . tablero . es_limitrofe ( OOOoO0O0o , O0o0Ooo ) )
   assert ( self . tablero . color_pais ( OOOoO0O0o ) == jugador . color )
   assert ( self . tablero . color_pais ( O0o0Ooo ) == jugador . color )
   Ii1i11IIii1I [ OOOoO0O0o ] = Ii1i11IIii1I . get ( OOOoO0O0o , 0 ) + ooO0o0Oo
  for O00o0OO in Ii1i11IIii1I :
   assert ( self . tablero . ejercitos_pais ( O00o0OO ) > Ii1i11IIii1I [ O00o0OO ] )
   if 56 - 56: ooOoO0o . OoOoOO00 * iII111i . OoOoOO00
   if 72 - 72: iII111i / i1IIi * Oo0Ooo - I1Ii111
  for OOOoO0O0o , O0o0Ooo , ooO0o0Oo in iii11 :
   self . tablero . asignar_ejercitos ( OOOoO0O0o , - ooO0o0Oo )
   self . tablero . asignar_ejercitos ( O0o0Ooo , ooO0o0Oo )
   if 51 - 51: II111iiii * OoO0O00 % o0oOOo0O0Ooo * II111iiii % I1ii11iIi11i / ooOoO0o
 def manejar_tarjetas ( self , jugador , paises_ganados ) :
  if ( self . tarjetas [ jugador ] . canjes < 3 and paises_ganados ) or ( self . tarjetas [ jugador ] . canjes >= 3 and len ( paises_ganados ) > 1 ) :
   if 49 - 49: o0oOOo0O0Ooo
   if 35 - 35: OoOoOO00 - OoooooooOO / I1ii11iIi11i % i1IIi
   if 78 - 78: I11i
   if 71 - 71: OOooOOo + ooOoO0o % i11iIiiIii + I1ii11iIi11i - IiII
   if 88 - 88: OoOoOO00 - OoO0O00 % OOooOOo
   if 16 - 16: I1IiiI * oO0o % IiII
   if 86 - 86: I1IiiI + Ii1I % i11iIiiIii * oO0o . ooOoO0o * I11i
   if 44 - 44: oO0o
   if 88 - 88: I1Ii111 % Ii1I . II111iiii
   if 38 - 38: o0oOOo0O0Ooo
   II1Iiii1111i = self . mazo . sacar_tarjeta ( )
   self . tarjetas [ jugador ] . todas [ II1Iiii1111i . pais ] = II1Iiii1111i
   jugador . tarjeta_recibida ( II1Iiii1111i . pais )
   if 57 - 57: O0 / oO0o * I1Ii111 / OoOoOO00 . II111iiii
  for O00o0OO in self . tarjetas [ jugador ] . todas :
   if O00o0OO not in self . tarjetas [ jugador ] . usadas and self . tablero . color_pais ( O00o0OO ) == jugador . color :
    self . tarjetas [ jugador ] . usadas [ O00o0OO ] = True
    jugador . tarjeta_usada ( O00o0OO )
    self . tablero . asignar_ejercitos ( O00o0OO , 2 )
    if 26 - 26: iII111i
 def canjear_tarjetas ( self , jugador ) :
  ooO00oOoo = self . tarjetas [ jugador ] . por_tipo ( )
  if 91 - 91: OoO0O00 . I1ii11iIi11i + OoO0O00 - iII111i / OoooooooOO
  for O0OOo in ( TARJETA_GALEON , TARJETA_GLOBO , TARJETA_CANON , 'mix' ) :
   if O0OOo == 'mix' :
    iII1 = ( ooO00oOoo [ TARJETA_COMODIN ] + ooO00oOoo [ TARJETA_GALEON ] [ - 1 : ] + ooO00oOoo [ TARJETA_GLOBO ] [ - 1 : ] + ooO00oOoo [ TARJETA_CANON ] [ - 1 : ] ) [ - 3 : ]
   else :
    iII1 = ( ooO00oOoo [ TARJETA_COMODIN ] + ooO00oOoo [ O0OOo ] ) [ - 3 : ]
   if len ( iII1 ) != 3 :
    continue
   jugador . tarjetas_canjeadas ( [ II1Iiii1111i . pais for II1Iiii1111i in iII1 ] )
   for II1Iiii1111i in iII1 :
    self . tarjetas [ jugador ] . usadas . pop ( II1Iiii1111i . pais , None )
    self . tarjetas [ jugador ] . todas . pop ( II1Iiii1111i . pais , None )
    self . mazo . devolver_tarjeta ( II1Iiii1111i )
   self . tarjetas [ jugador ] . canjes += 1
   IiI11iII1 = self . tarjetas [ jugador ] . canjes
   IIII11I1I = { 1 : 4 , 2 : 7 }
   OOO0o = IIII11I1I [ IiI11iII1 ] if IiI11iII1 in IIII11I1I else ( IiI11iII1 - 1 ) * 5
   return OOO0o
  return 0
  if 30 - 30: iIii1I11I1II1 / ooOoO0o - I1Ii111 - II111iiii % iII111i
 def agregar_ejercitos ( self , inicia_ronda ) :
  Interfaz . setear_titulo ( 'Incorporando ejercitos' )
  if 49 - 49: I1IiiI % ooOoO0o . ooOoO0o . I11i * ooOoO0o
  if 97 - 97: Ii1I + o0oOOo0O0Ooo . OOooOOo + I1ii11iIi11i % iII111i
  if 95 - 95: i1IIi
  if 3 - 3: I1Ii111 - O0 / I1Ii111 % OoO0O00 / I1Ii111 . I1IiiI
  if 50 - 50: IiII
  if 14 - 14: I11i % OoO0O00 * I11i
  if 16 - 16: OoOoOO00 . ooOoO0o + i11iIiiIii
  if 38 - 38: IiII * OOooOOo . o0oOOo0O0Ooo
  if 98 - 98: OoooooooOO + iII111i . OoOoOO00
  if 67 - 67: i11iIiiIii - i1IIi % I1ii11iIi11i . O0
  if 77 - 77: IiII / I1IiiI
  if 15 - 15: IiII . iIii1I11I1II1 . OoooooooOO / i11iIiiIii - Ii1I . i1IIi
  if 33 - 33: I11i . o0oOOo0O0Ooo
  if 75 - 75: o0oOOo0O0Ooo % o0oOOo0O0Ooo . I1Ii111
  if 5 - 5: o0oOOo0O0Ooo * ooOoO0o + OoOoOO00 . OOooOOo + OoOoOO00
  for Oo00OOOOO in range ( len ( self . jugadores ) ) :
   iIiiI1 = self . jugadores [ ( inicia_ronda + Oo00OOOOO ) % len ( self . jugadores ) ]
   if 91 - 91: O0
   oOOo0 = self . canjear_tarjetas ( iIiiI1 )
   if 54 - 54: O0 - IiII % OOooOOo
   ooO0o0Oo = {
 "" : max ( 3 , oOOo0 + len ( self . tablero . paises_color ( iIiiI1 . color ) ) / 2 )
 }
   for OOoO , iII in paises . paises_por_continente . iteritems ( ) :
    if all ( self . tablero . color_pais ( p ) == iIiiI1 . color for p in iII ) :
     ooO0o0Oo [ OOoO ] = paises . ejercitos_por_continente [ OOoO ]
     if 38 - 38: I1Ii111
   O0O = iIiiI1 . agregar_ejercitos ( self . tablero , ooO0o0Oo )
   if 7 - 7: O0 . iII111i % I1ii11iIi11i - I1IiiI - iIii1I11I1II1
   assert sum ( O0O . values ( ) ) == sum ( ooO0o0Oo . values ( ) )
   if 36 - 36: IiII % ooOoO0o % Oo0Ooo - I1ii11iIi11i
   if 22 - 22: iIii1I11I1II1 / Oo0Ooo * I1ii11iIi11i % iII111i
   for OOoO in ooO0o0Oo :
    if OOoO == "" :
     continue
    OOOo00oo0oO = sum ( cant for O00o0OO , cant in O0O . items ( ) if O00o0OO in paises . paises_por_continente [ OOoO ] )
    assert OOOo00oo0oO >= paises . ejercitos_por_continente [ OOoO ]
    if 1 - 1: OoO0O00 - oO0o . I11i . OoO0O00 / Oo0Ooo + I11i
   for O00o0OO in O0O :
    if 78 - 78: O0 . oO0o . II111iiii % OOooOOo
    assert ( self . tablero . color_pais ( O00o0OO ) == iIiiI1 . color )
    self . tablero . asignar_ejercitos ( O00o0OO , O0O [ O00o0OO ] )
    if 49 - 49: Ii1I / OoO0O00 . II111iiii
 def jugador_es_ganador ( self , jugador ) :
  return len ( self . tablero . paises_color ( jugador . color ) ) == self . tablero . cantidad_paises ( )
  if 68 - 68: i11iIiiIii % I1ii11iIi11i + i11iIiiIii
  if 31 - 31: II111iiii . I1IiiI
  if 1 - 1: Oo0Ooo / o0oOOo0O0Ooo % iII111i * IiII . i11iIiiIii
 def jugador_esta_vivo ( self , jugador ) :
  return len ( self . tablero . paises_color ( jugador . color ) ) != 0
  if 2 - 2: I1ii11iIi11i * I11i - iIii1I11I1II1 + I1IiiI . oO0o % iII111i
  if 92 - 92: iII111i
  if 25 - 25: Oo0Ooo - I1IiiI / OoooooooOO / o0oOOo0O0Ooo
 def jugar ( self , jugadores ) :
  if 12 - 12: I1IiiI * iII111i % i1IIi % iIii1I11I1II1
  if 20 - 20: OOooOOo % Ii1I / Ii1I + Ii1I
  if 45 - 45: oO0o - IiII - OoooooooOO - OoO0O00 . II111iiii / O0
  self . configurar_el_juego ( jugadores )
  if 51 - 51: O0 + iII111i
  if 8 - 8: oO0o * OoOoOO00 - Ii1I - OoO0O00 * OOooOOo % I1IiiI
  self . repartir_paises ( )
  Interfaz . actualizar ( self . tablero )
  if 48 - 48: O0
  if 11 - 11: I11i + OoooooooOO - OoO0O00 / o0oOOo0O0Ooo + Oo0Ooo . II111iiii
  i1Iii1i1I = 1
  OOoO00 = random . randrange ( len ( self . jugadores ) )
  IiI111111IIII = self . orden_ronda ( OOoO00 )
  for i1Ii in self . jugadores :
   i1Ii . ronda_iniciada ( self . tablero , i1Iii1i1I , IiI111111IIII )
   if 14 - 14: iII111i
  Interfaz . setear_texto ( "Ronda: %s" % self . texto_ronda ( OOoO00 ) )
  if 11 - 11: IiII * I1IiiI . iIii1I11I1II1 % OoooooooOO + iII111i
  if 78 - 78: OoO0O00 . OOooOOo + OoO0O00 / I11i / OoO0O00
  self . agregar_ejercitos_inicial ( OOoO00 )
  if 54 - 54: OoOoOO00 % iII111i
  if 37 - 37: OoOoOO00 * Oo0Ooo / ooOoO0o - iII111i % II111iiii . oO0o
  while Interfaz . esta_corriendo ( ) :
   if 88 - 88: iII111i . II111iiii * II111iiii % I1Ii111
   for Oo00OOOOO in range ( len ( self . jugadores ) ) :
    iIiiI1 = self . jugadores [ ( OOoO00 + Oo00OOOOO ) % len ( self . jugadores ) ]
    if not self . jugador_esta_vivo ( iIiiI1 ) :
     continue
    oO00 = self . realizar_fase_ataque ( iIiiI1 )
    if self . jugador_es_ganador ( iIiiI1 ) :
     break
    self . realizar_fase_reagrupamiento ( iIiiI1 , oO00 )
    self . manejar_tarjetas ( iIiiI1 , oO00 )
    if 15 - 15: i1IIi * I1IiiI + i11iIiiIii
    if 6 - 6: ooOoO0o / i11iIiiIii + iII111i * oO0o
    if 80 - 80: II111iiii
   for Oo00OOOOO , i1Ii in enumerate ( self . jugadores [ : ] ) :
    if not self . jugador_esta_vivo ( i1Ii ) :
     Interfaz . alertar ( 'Uno menos!' , 'El jugador %s ha quedado eliminado luego de %d rondas' % ( i1Ii , i1Iii1i1I ) )
     self . jugadores . remove ( i1Ii )
     if OOoO00 >= Oo00OOOOO :
      OOoO00 -= 1
      if 83 - 83: I11i . i11iIiiIii + II111iiii . o0oOOo0O0Ooo * I11i
   for i1Ii in self . jugadores :
    if self . jugador_es_ganador ( i1Ii ) :
     Interfaz . alertar ( 'Hay ganador!' , 'El jugador %s ha ganado el juego luego de %d rondas' % ( i1Ii , i1Iii1i1I ) )
     Interfaz . actualizar ( self . tablero )
     return
     if 53 - 53: II111iiii
     if 31 - 31: OoO0O00
   i1Iii1i1I += 1
   OOoO00 = ( OOoO00 + 1 ) % len ( self . jugadores )
   IiI111111IIII = self . orden_ronda ( OOoO00 )
   for i1Ii in self . jugadores :
    i1Ii . ronda_iniciada ( self . tablero , i1Iii1i1I , IiI111111IIII )
    if 80 - 80: I1Ii111 . i11iIiiIii - o0oOOo0O0Ooo
   Interfaz . setear_texto ( "Ronda: %s" % self . texto_ronda ( OOoO00 ) )
   if 25 - 25: OoO0O00
   if 62 - 62: OOooOOo + O0
   self . agregar_ejercitos ( OOoO00 )
   if 98 - 98: o0oOOo0O0Ooo
   Interfaz . actualizar ( self . tablero )
   if 51 - 51: Oo0Ooo - oO0o + II111iiii * Ii1I . I11i + oO0o
 def orden_ronda ( self , inicia_ronda ) :
  return [ i1Ii . color for i1Ii in self . jugadores [ inicia_ronda : ] + self . jugadores [ : inicia_ronda ] ]
  if 78 - 78: i11iIiiIii / iII111i - Ii1I / OOooOOo + oO0o
  if 82 - 82: Ii1I
 def texto_ronda ( self , inicia_ronda ) :
  return ', ' . join ( [ str ( ii ) for ii in self . jugadores [ inicia_ronda : ] + self . jugadores [ : inicia_ronda ] ] )
  if 5 - 5: ooOoO0o - II111iiii - OoooooooOO % Ii1I + I1IiiI * iIii1I11I1II1
  if 37 - 37: IiII % ooOoO0o + OoOoOO00 + o0oOOo0O0Ooo * I11i % O0
  if 61 - 61: I1IiiI - OOooOOo . oO0o / OOooOOo + Oo0Ooo
if __name__ == '__main__' :
 II1Iiii1111i = oo00000o0 ( )
 II1Iiii1111i . jugar ( partida . jugadores )
 if 5 - 5: ooOoO0o + ooOoO0o / O0 * Oo0Ooo - OOooOOo % ooOoO0o
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3

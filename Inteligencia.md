Inteligencia artificial del jugador
***********************************

A continuación se detallan las características del comportamiento del jugador inteligente.

***

*Reglas generales*

- El jugador debe poder mutar ligeramente de personalidad, para adaptarse al comportamiento y los defectos del otro jugador (Podriamos hacer que detectase el comportamiento erratico del JugadorSuicida y que lo ignore; podria hacerlo menos eficiente en el torneo)
- Debe conocer el nivel de seguridad de cada uno de sus paises, para reforzar los más expuestos (LISTO :D)
- Debe tener en cuenta si el oponente puede agregar más ejercitos que él.
- Debe cambiar su comportamiento si en la partida hay más de 2 jugadores (Aunque también depende de la agresividad de los oponentes)


***

*Inicio de la partida*

Al comenzar, los paises repartidos son aleatorios y hay que agregar ejercitos. Es decisivo elegir bien los paises para capturar continentes rápido.
Órden de prioridades.
-- America del Norte
-- America del Sur
-- Oceania
-- Europa
-- Africa
-- Asia

Las prioridades se basan en la cantidad de ejercitos que dan de bonus y la dificultar para defenderlos.

***

*Ataque*

La agresividad del jugador depende varios factores:
-- Agresividad del oponente
-- Si ya puede tomar tarjeta

El jugador en la ronda de ataque recorre todos sus países y busca la combinación de paises más favorable.
Luego hay que evaluar las probabilidades de victoria de ese combate.
El jugador ataca si las probabilidades son aceptables. Si el nivel de agresividad es alto, atacará a pesar de que las probabilidades no den mucha ventaja.
Y se repite el proceso hasta que no haya buenas chances para ningún país.

***

*Reagrupación*

- Los países más expuestos deben tener mayor cantidad de ejércitos.
- - Un pais de orden 2 solo puede ser atacado con 3 ejercitos (2 dados). Con 1 ejercito, sus chances de perder son de 75.4%, con 2, 36.2%, con 3, 12% y con 4, 5%. Deberemos tomar un criterio sobre cuantos dejarle.
- Los países de orden 4 o superior deben quedar con 1 ejercitos, y reagrupar tratando de enviar sus ejercitos a alguien de menor orden (si puede detectar quien los necesita mas, mejor)
-- Para el resto...

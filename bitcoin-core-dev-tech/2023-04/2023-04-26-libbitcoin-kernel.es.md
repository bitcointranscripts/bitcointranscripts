---
title: Libbitcoin kernel
translation_by: Blue Moon
tags:
  - bitcoin-core
  - build-system
date: 2023-04-26
speakers:
  - thecharlatan
---
## Preguntas y respuestas

Q: bitcoind y bitcoin-qt vinculado contra el núcleo de la biblioteca en el futuro?

- presentador: sí, ese es un / el objetivo

P: ¿has mirado una implementación de electrum usando libbitcoinkernel?

- audiencia: sí, ¡estaría bien tener algo así!
- audiencia: ¿también podría hacer el largo índice de direcciones propuesto con eso?
- audiencia: no solo indice de direcciones, otros indices tambien.

P: Otros casos de uso:

- público: poder ejecutar cosas en iOS

P: ¿Debería estar el mempool en el kernel?

- presentador: hay algunos archivos mempool en el kernel
- audiencia: No, no debería
- audiencia: ¿Por qué no? ¿Debería la gente implementar los suyos propios?
- audiencia: es política, no consenso
- audiencia: ¿tal vez libbitcoinmempool...? ¿también libs para addrman, p2p, ..?
- audiencia: ¿qué intentamos conseguir? ¿evitar divisiones en la red entre diferentes implementaciones?
- audiencia: ¿incluir una impl de mempool por defecto pero posibilidad de usar mempool propio/personalizado?
- audiencia: depende de lo que la gente necesite. Algunos lo quieren. Tal vez terminar este proyecto y luego mirar desde allí.
- audiencia: ¿queremos mantener libmempool u otras librerias?
- audiencia: si lo usamos nosotros mismos no deberia ser un problema
- audiencia: ayudara con la separacion de repos en el futuro si tenemos multiples libs
- audiencia: sí, ayudará enormemente al mantenimiento. Acabar con el monolito. la gente puede construir sobre librerías y no necesita contaminar el repositorio de bitcoin.
- audiencia: bitcoin (Core) necesita esto a largo plazo
- audiencia: permite mover, por ejemplo, RPCs a muchas herramientas más pequeñas que acceden a una librería del núcleo en ejecución.
- audiencia: ¿se revisarán menos las librerías múltiples? En realidad, no.

P: Presentador: ¿Opiniones sobre el enfoque de crear una PoC más pequeña en privado para averiguar cómo puede ser la API?

- (sin respuestas)

P: Muchos lugares que llaman a shutdown. Los errores deberían aparecer con "esta función llama a shutdown".

- audiencia: Para hacer esto, tendríamos que cambiar mucho código - gran diferencia.
- audiencia: podemos usar un scripted-diff que facilite la revisión.
- audiencia: la alternativa es capturar excepciones: p.e. UTXO set corrupto, disco lleno
- audiencia: el usuario de la lib deberia tomar estas decisiones. parece terrible revisar todo el codigo.

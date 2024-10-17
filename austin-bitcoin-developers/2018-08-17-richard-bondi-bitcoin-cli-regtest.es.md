---
title: Bitcoin CLI y Regtest
speakers:
  - Richard Bondi
date: 2018-08-17
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - bitcoin-core
  - developer-tools
media: https://www.youtube.com/watch?v=sbupEpL6-J4
---
Clone este repositorio para seguir el proceso: <https://github.com/austin-bitcoin-developers/regtest-dev-environment>

<https://twitter.com/kanzure/status/1161266116293009408>

## Introducción

Así que el objetivo aquí como Justin dijo es conseguir el entorno regtest configurado. Las ventajas que mencionó, también existe la ventaja de que usted puede minar sus propias monedas a voluntad por lo que no tiene que perder el tiempo con grifos testnet. También puedes generar bloques, así que no tienes que esperar seis confirmaciones o lo que sea, ni siquiera los diez minutos. Las confirmaciones llegan enseguida y esa es una de las cosas que vamos a ver con Bitcoin Core que es lo que vamos a utilizar. ¿Alguien no lo tiene instalado todavía? Vamos a ir a través de ello y voy a mostrar todo con mi configuración que tengo aquí. Usted puede seguirme a lo largo del proceso. También esta este repositorio aquí, usted puede descargar este repositorio que sería útil. Una vez que tengas Bitcoin Core configurado, ejecuta algunos scripts que configurarán tres nodos en modo regtest. Así que vas a ejecutar tres nodos en tu portátil que comienza con cero bloques. Tienes un blockchain limpio y si empieza... puedes borrarlo. Realmente no tienes que preocuparte por los recursos. Es una de las ventajas de regtest. Supongo que podemos empezar a clonar el repo. ¿Me zambullo y empiezo a demostrar?

## Demostración

En el repositorio tenemos algunos scripts. En primer lugar queremos hacer el script de ejecución que nos pondrá en marcha y obtener los tres nodos si tenemos nuestras configuraciones establecidas. Voy a ponerlo en marcha aquí. Si ustedes están listos pueden tratar de arrancarlo. Si tienen problemas podemos parar y tratar de averiguar cuales son.

`./run.sh`

Mostraremos los scripts a medida que avancemos, es una buena idea.

P - ¿Es como un script bash?

R - Sí. Si estás en Windows puedes cambiarlo a .bat. Es sólo una línea de comandos. Esto es asumiendo que tienes bitcoind en tu PATH. El número de versión de Bitcoin, como sea que lo configures, si haces la instalación por defecto va a ser bitcoin, el número de versión, .bin. Si lo tienes en tu PATH lo tendrás funcionando.

P - Para aquellos que no lo sepan, ¿qué es bitcoind?

R - bitcoind es el demonio de Bitcoin que es la implementación del nodo. Es una especie de caja negra que se comunica con los otros nodos y envía transacciones, recibe transacciones, es tu nodo completo.

P - ¿Se puede pensar en él básicamente como el cliente que vería en Bitcoin Core pero sin cabeza? Simplemente se ejecuta en el servidor.

R: Sí.

P - ¿Qué hacen estos comandos?

R - El -regtest es obviamente regtest lo que significará que no te conectas a mainnet o testnet. Tienes tu propio entorno local. El -daemon al final significa que se ejecutará en segundo plano. Usted ve el servidor Bitcoin iniciándose y yo todavía tengo mi símbolo del sistema. Si intentas usar esto sin el demonio estarías bloqueado ahí y tu consola estaría bloqueada.

P - ¿Qué pasa con el datadir?

R - Tenemos Alice y luego tenemos un directorio de datos de Bob. El de arriba no tiene porque va al que viene por defecto. Siempre que lo instalas debería ser home/usuario/.bitcoin/bitcoin.conf Por eso no hay uno ahí. Alice, vamos a verla. Contraseñas muy seguras, no intentes robarle dinero a Alice aquí. Configuramos algunos puertos únicos para ella y le añadimos nodos para que pueda hablar con Bob y pueda hablar con el nodo regtest por defecto.

P - ¿Así que esto es sólo un archivo de configuración bitcoind?

R - Es bitcoin.conf para bitcoind. O si ejecutas Bitcoin-Qt mirará el mismo.

P - ¿En qué se diferencian Alice y Bob?

R - Tienen puertos diferentes. Estos son sólo números aleatorios, sólo tenían que ser únicos. Así que puedes ver que Bob es 18446, el puerto por defecto para regtest es 18444, este es 18445. Y lo mismo para los puertos RPC. Hay uno por defecto de 18443, hay esta cosa aleatoria que Justin inventó y luego Bob tiene otra cosa aleatoria que Justin inventó.

P - Ok, entonces cuando dice `puerto=` eso es lo que Alice esta ejecutando y luego los otros dos son como conectarse a estos otros dos peers? ¿Es una forma de arrancar nuestra pequeña mini red de 3?

A - Correcto.

Así que si vuelvo a mi símbolo del sistema. Ya estoy en marcha.

P - En realidad solo necesitas añadir uno de ellos y ya descubrirás los otros peers, `addnode` es un lujo?

R - No hay descubrimiento de pares en regtest. Eso es cierto si estás en testnet pero no en regtest. No hay descubrimiento de pares, esa es una de las limitaciones. Cambias poder minar monedas a voluntad por no tener descubrimiento de pares. Tienes casi todas las otras características, puede que falten algunas.

P - ¿También puedes ahora mismo confirmar que está funcionando mirando en los directorios de Alice y Bob? Tendrás chainstate...

R - Claro. Tengo un directorio regtest que arrancó. Los borré antes de empezar. Pero lo que realmente queremos hacer es verificar a través de la CLI o a través de algunas de estas otras herramientas que queremos mirar.

Tenemos aliases.sh, es un script conveniente. No tenemos que escribir el puerto 99 lo que sea para Alice y el puerto 99 lo que sea para Bob. Podemos crear estos alias. Ahora mismo tengo el predeterminado. El -regtest nos pone en la red y quiero poner un comando.

`bitcoin-cli -regtest getpeerinfo`

P - ¿También puedes ahora mismo confirmar que está funcionando mirando en los directorios de Alice y Bob? Tendrás chainstate...

R - Claro. Tengo un directorio regtest que arrancó. Los borré antes de empezar. Pero lo que realmente queremos hacer es verificar a través de la CLI o a través de algunas de estas otras herramientas que queremos mirar.

Tenemos aliases.sh, es un script conveniente. No tenemos que escribir el puerto 99 lo que sea para Alice y el puerto 99 lo que sea para Bob. Podemos crear estos alias. Ahora mismo tengo el predeterminado. El -regtest nos pone en la red y quiero poner un comando.

Eso fue desde tu punto de vista por defecto. También queremos tener un punto de vista de Alice y Bob. Ahí es donde entran los alias. Permítanme sacar eso. El Bitcoin CLI, ahí está tu puerto, ahí está tu directorio de datos. El puerto en este es su puerto RPC. Ahora puedes escribir `alice-cli` en lugar de escribir `bitcoin-cli -port=9334 -datadir=alice` cada vez, tenemos un atajo.

`source aliases.sh`

Ahora puedo hacer lo mismo.

`alice-cli getpeerinfo`

Ahora tengo el punto de vista de Alice sobre la red. Lo mismo para Bob.

`bob-cli getpeerinfo`

Es realmente difícil de seguir en la CLI pero tenemos una solución para eso, no te preocupes. Así que vamos a ver cómo vamos de efectivo.

`bitcoin-cli -regtest getbalance`

Ok no hay dinero, triste estado de cosas. Pero no tenemos que meternos con los grifos de testnet, podemos generar los nuestros. Hay un comando llamado generar así que usamos eso y luego el número de bloques que desea generar.

`bitcoin-cli -regtest generate 1`

Así que generamos un bloque. Ahí está el hash del bloque que generamos. Es poco emocionante, no hay nada más que una base de monedas, pero así es como funcionan las cosas.

P - Ojalá encontrara la forma de colarlo en la cadena real.

R - No, tengo algo. Agárrate fuerte, te tengo cubierto. No necesitas una cadena de verdad, de eso se trata. Si pudieras ponerte en marcha así de rápido, pero el mundo no funciona así.

Así que generé un bloqueo, quiero recuperar mi equilibrio.

`bitcoin-cli -regtest getbalance`

Oh no, sigo sin dinero. ¿Qué ha pasado? Necesitas 100 bloques antes de poder reclamar tus monedas minadas. Estamos simulando la minería, seguimos simulando de la misma manera. Quiero generar otros 100.

`bitcoin-cli -regtest generate 100`

Ahora tengo un montón de bloques muy emocionantes con sólo una transacción coinbase pero ahora tengo un saldo de 50. El primero maduró más de 100 bloques así que estamos listos. Así que listo para empezar a difundir la riqueza aquí. Así que estoy consiguiendo una dirección para Alice para que pueda enviar Alice algunas monedas.

`alice-cli getnewaddress`

P - ¿Las direcciones Regtest empiezan por 2?

R - Empiezan por m o n si se trata de la antigua dirección heredada. Empiezan con 2 si es una dirección SegWit. Si es una bech32 empieza por btr creo que fir regtest mode.

Así que tenemos una dirección para Alice, queremos gastar Alice algunas monedas.

P - ¿Cuál es su saldo?

R - Claro, por qué no. Sabemos que es cero pero es bueno confirmarlo.

`alice-cli getbalance`

Necesito una dirección y una cantidad, vamos a darle 10.

`bitcoin-cli -regtest sendtoaddress [insert address] 10`

Así que hay un hash de transacción que vuelve de ese comando. Comprobemos el saldo de Alice.

`alice-cli getbalance`

Es cero. ¿Por qué? No ha habido minería. Sin embargo, podemos decir que ocurrió.

`alice-cli listunspent 0`

El primer parámetro es el número mínimo de confirmaciones. Así que si decimos cero podemos verificar que Alice recibió esa transacción, sólo que no está disponible. ¿Ves las cero confirmaciones? Vemos el mismo ID de transacción, vemos los mismos 10 Bitcoins que le enviamos.

P - ¿Qué está consultando para averiguar cuál es su unspent con cero confirmaciones?

R - listunspent era el comando. Si haces listunspent sin ningún parámetro no va a incluir las cero confirmaciones. Así que tienes varios parámetros. Tienes confirmaciones mínimas, confirmaciones máximas, puedes filtrar por direcciones. Donde dice seguro en la parte inferior se puede incluir inseguro que por defecto a true creo de todos modos. Puedes pasarle otro objeto para obtener la cantidad mínima, quiero ver todas las transacciones no gastadas de más de 2 Bitcoin o quiero ver todas las transacciones no gastadas de menos de 5 Bitcoin o lo que sea.

P - ¿Cuál es el almacén de datos donde se guarda eso? ¿Para los no gastados? ¿Lo no gastado no estaría en la blockchain?

R - Todo está en la cadena de bloques. Desde la perspectiva de Alice, el demonio Bitcoin tiene un monedero incorporado y la lista de no gastados está mirando el monedero de Alice.

P - ¿Así que ella está mirando su mempool local?

R - Sería su mempool local pero sería cualquier dirección en su monedero que tenga salidas en ese mempool. Una vez minado, no está en el mempool, forma parte de la cadena de bloques.

Así que generemos 1.

`bitcoin-cli -regtest generate 1`

Ahora Alice puede conseguir su equilibrio.

`alice-cli getbalance`

Tiene 10 monedas.

P - ¿Por defecto debería tener 100?

R - Tenía 50 y envió 10. Debería tener 40 menos una comisión, así que 39,9 algo.

P - ¿Pero tenemos un nuevo bloque maduro?

R - Es cierto, más las 50. Es cierto.

`bitcoin-cli -regtest getbalance`

Los 50 originales, los 50 recién acuñados menos los 10 enviados a Alice menos una comisión por transacción.

P - ¿La comisión es autogenerada? ¿Quién genera la comisión de transacción en este ensayo?

R - Cada uno tiene su monedero. Regtest tiene una cartera, Alice tiene una cartera, Bob tiene una cartera.

P - ¿Es una tarifa por defecto?

R - Cada monedero tiene su propia tarifa. Es demasiado pronto para optimizar las comisiones. No sé cuál es el número exacto cuando se alcanzan los mil bloques o lo que sea.

P - ¿Quién recibe la comisión?

R: El minero.

P - ¿El minero es el que cobra por defecto en este caso o hay una cuarta parte?

R - Tiene razón. Tengo que esperar 100 bloques para recuperarlo. Si minamos 100 bloques deberíamos tener un número par.

Si generamos 100 bloques.

`bitcoin-cli -regtest generate 100`

Número par, así que tienen la cuota. Eso es lo que buscamos.Esa es la belleza de regtest, usted no tiene que preocuparse por eso. Sólo hacer más, estamos peor que la Fed aquí.Eso es bastante básico y poco emocionante.P - ¿Puedes enviar más monedas a Alice, enviarle como 10 más y ejecutar esa consulta con un mínimo de cero confirmaciones? ¿Sumaría el mempool y la cantidad en el blockchain? ¿El total incluiría las 10 monedas que no han sido minadas?

R - Sí. Hagámoslo.

Necesito otra dirección de Alice.

`alice-cli getnewaddress`

Vamos a enviar otros 10.

`bitcoin-cli -regtest sendtoaddress  [insert address] 10`

Así que tengo una transacción.

`alice-cli listunspent`

Si hago eso no voy a conseguir el nuevo 10. Ahora sólo tengo una transacción con 101 confirmaciones. Pero si hago el mínimo con un cero...

`alice-cli listunspent 0`

Tengo las dos transacciones.

`nodes-debug`

Apareció en esta pantalla, es tan pequeño que no puedo verlo. Lo que hice fue desarrollar una herramienta que le permite conectarse a múltiples nodos y tiene algunas características convenientes para trabajar con los comandos para que no tenga que ser torpe trabajando con la CLI. Podemos hacer algunas de las mismas cosas.

P - ¿Todos deberíamos obtener exactamente los mismos resultados que tú hasta en las firmas? Mis ID de transacción no coinciden con los suyos. En la salida de la línea de comandos, es determinista, ¿deberíamos estar obteniendo los mismos resultados? Creo que Bitcoin Core utiliza valores k deterministas ahora, así que las firmas deberían estar duplicadas.

R - Tenemos tres configuraciones diferentes. Yo no esperaría los mismos resultados pero puede que tengas razón. Si instalaste en mainnet no vas a generar desde la misma semilla.

P - ¿Qué hace regtest por la minería? ¿Hay alguna dificultad?

R - No, es instantáneo. Si genero 100 ya has visto lo rápido que ha salido. Es una simulación, no es real.

P - ¿Se puede obtener la prueba, la cadena que se hash? Incluso la dificultad cero en realidad tiene alguna dificultad. Satoshi hizo una elección realmente extraña. Pero es trivial.

Viste como estaba luchando con los comandos. Escribí esto para obtener algo de autocompletado y obtienes algo de ayuda con los parámetros.

`getbestblockhash`

P - ¿Puedes sacar el repositorio de GitHub rápidamente?

R - Está en el [README.](https://github.com/rsbondi/nodes-debug.git)

Voy a buscar ese bloque.

`getblock [insert block hash]`

P - ¿A la izquierda se ejecutan los comandos y a la derecha se obtienen los resultados?

Queremos fijarnos en el bloque, en la dificultad, en el encadenamiento. Es realmente difícil, mira todos esos ceros. Es falso, no significa nada.

P - Justo encima de esa línea aparece la dificultad, ¿e^(-10)?

R - Entonces es muy fácil. ¿Por qué tiene todos los ceros? Esa es la cantidad de trabajo, no el hash. Debería ser bastante fácil, se generan instantáneamente.

Haremos lo mismo aquí. Vamos a volver a Alice y la lista de los no gastados. No tengo que escribir en orden, puedo usar el atajo `lisu` que salta a la `listunspent`. Lo hace un poco más fácil. ¿Cuáles son mis parámetros? Mira eso, el primero es min confirmaciones, puse un cero allí. El siguiente es max confirmaciones, 9999. El último, `query_options`, no nos dice mucho al respecto. Pero usted no tiene que ir a la ayuda que acaba de pasar el cursor sobre él. Ahora tienes la ayuda completa. Todo esto está señalado en el servidor RPC. Sea cual sea la versión en la que estés esto va a funcionar. Es opcional, úsalo si quieres. Yo lo hice porque me ayudo mucho, solo para no tener que ir de un lado a otro buscando cosas. Enviémosle dinero a Bob. Ha sido abandonado aquí. Bob necesita conseguir una dirección primero.

`getnewaddress`

`sendtoaddress “[insert address]” 5`

Es un poco diferente aquí de la CLI, las cadenas que no necesita las comillas. Aquí lo haces porque es Javascript y no quería averiguar cómo analizarlo. ¿Cuánto queremos enviar Bob, vamos a enviar 5, vamos a mantener la mayor parte de la riqueza a nosotros mismos. Tenemos esa transacción, podemos mirar eso si queremos. ¿Alguien me dice cómo puedo ver que esa transacción llegó a Bob?

`listunspent 0`

Ya está, cero confirmaciones.

P - ¿Cómo has añadido a Alice y Bob? Recibí un mensaje de error cuando intenté añadirlos. ¿Hay alguna manera fácil de añadirlos?

R - Ya los tenía configurados. Tienes el botón Añadir Nodo aquí. Necesitas el archivo de configuración porque son tus credenciales de usuario. Lo extrae de ahí.

P - ¿Podría intentar borrar uno y añadir otro en tiempo real?

R - Claro, por qué no. Veamos primero la configuración de Bob. Edita el Nodo y luego copia esto. Voy a borrar a Bob y añadirlo de nuevo. Pon la ruta de configuración. Se que no necesitamos el host, no creo que necesitemos el puerto tampoco. Debería obtenerlo de la configuración. Ahi esta, esta arriba y hablando.

P - ¿No tuviste que poner el puerto?

R - No, porque eso está en la configuración. Si tienes la configuración y lo tienes configurado ahí y no lo estás sacando de la línea de comandos, bitcoind, ya está ahí. Siempre necesitas la configuración porque ahí es donde están tus credenciales.

Ok lo que hemos hecho es bastante aburrido, enviar a la dirección, la dirección y la cantidad. Vamos a hacerlo a mano. Usaré la misma dirección. No es una buena práctica pero está bien. Crear transacción en bruto, ¿qué parámetros necesito aquí? Necesito salidas no gastadas. ¿Por qué Alice no tiene dinero? Necesitamos minar el bloque. Ella envió algo de dinero y envía todo el Bitcoin no parte de él. Vamos a generar uno. Fíjate que llamé a este Regpool, ese es mi nodo minero.

Regpool - `generate 1`

Alicia - `listunspent`

Alice tiene dinero otra vez. Tomemos el primero. Necesito un array de un objeto y necesito un txid y un vout. Los tomaré de aquí.

P - ¿Así que estás construyendo una transacción a partir de entradas de transacciones?

R - A partir de salidas no utilizadas. Le estoy diciendo que para mi entrada quiero usar esa transacción, índice número 0, debería ser la de arriba con las 10 monedas dentro.

Otra cosa, puedo hacer líneas múltiples, sólo que no puedo tener espacios entre las líneas múltiples. Ese es mi primer parámetro. Ahora necesito a alguien a quien enviárselo. Vamos a buscar a Bob, un objeto con una dirección y una cantidad.

Bob - `getnewaddress`

Enviaremos 5 de nuevo. Ahí está nuestra transacción que hemos creado.

Regpool - `createrawtransaction [{“txid”: “[add transaction ID]”, “vout”: 0}] {“[add address]”: 5}`

¿Qué crees que ocurrirá si intento enviarlo?

P - Has generado una nueva dirección para Bob y la has conectado como salida, ¿verdad?

R - Si

No, no va a funcionar porque no hemos firmado la transacción. Esto te dará más flexibilidad si estás creando transacciones y quieres crearlas a mano. Esta es la forma de hacerlo. Tienes más flexibilidad que simplemente enviar a la dirección, puedes incluir tus propios scripts y todo tipo de cosas. No creo que vayamos a entrar en eso hoy. Quiero firmar la transacción.

`signrawtransaction “[add result hex string]”`

Así que ahora tengo una transacción firmada. Vamos a enviar ese bebé. Lo siguiente es `sendrawtransaction` y entonces todo lo que realmente necesitas es una cadena.

`sendrawtransaction “[add result hex string]”`

R - ¿La `createrawtransaction` tiene una entrada y luego la segunda cosa es una salida?

A - Correcto. La salida es la dirección a la que estoy enviando y la cantidad, es un objeto. Puedo tener varias direcciones. La dirección es la clave y la cantidad es el valor. Es un objeto JSON, una clave-valor, dirección-importe.

P - ¿La salida de la transacción no gastada es 10?

R - Correcto. Podemos gastarlo, vamos a tirar 5 monedas como comisión. ¿O no? Cuota absurdamente alta, no me deja hacerlo. Gracias Bitcoin RPC, me acabas de ahorrar 5 Bitcoin.

P - ¿Puedes mostrar una transacción completa en JSON? ¿Puede decodificar rawtx?

R - Claro. Esta es la que intentamos enviar.

`decoderawtransaction  “[add result hex string]”`

Esto es lo que parece decodificado. La firma está en los datos del testigo.

Así que lo que Alice necesita hacer es obtener un cambio de dirección, `getrawchangeaddress` sin parámetros.

`getrawchangeaddress`

Por eso casi todas las transacciones tienen dos salidas. Es porque la probabilidad de que vayas a gastar exactamente cualquier salida es muy baja por lo que 224 bytes es lo normal.

He añadido el resto de los 10 menos una tasa de minero. Ahora puedo recrear una transacción.

Alicia - `createrawtransaction [{“txid”: “[add transaction ID]”, “vout”: 0}] {“[add address_1]”: 5, “[add address_2]”: 4.99999 }`

P - ¿Entonces la segunda dirección es Alice?

R - Ese es el cambio de Alice. 5 van a Bob, 4.99999 vuelven a Alice, a su nueva dirección de cambio que acabamos de crear.

No estoy seguro de cuál es la diferencia entre dirección de cambio y dirección. Sé que en HD es m/0/0/0/1 para la dirección de cambio y m/0/0/0/0 para la dirección principal.

R - ¿Tiene `getrawchangeaddress` un HD diferente?

R - No conozco bien la implementación de Bitcoin Core pero si estás usando la característica HD de Bitcoin Core no usa el BIP32 por defecto. Utiliza derivación endurecida para cada dirección, no es compatible con tu Trezor o lo que sea.

Si tuvieras un monedero HD como dije esa ruta de derivación terminaría en 0 y 1 para la dirección de cambio.

Estoy creando la transacción, quiero firmarla.

`signrawtransaction “[add result hex string]”`

Ahí está mi transacción firmada, quiero enviarla como una transacción sin procesar.

`sendrawtransaction “[add result hex string]”`

Ahí está mi identificación de transacción. Supongo que seguiré. También tengo un script de simulación (simulate.js) aquí. Lo que hace es crear aleatoriamente transacciones de cantidades aleatorias desde tu nodo principal regtest. Lo he puesto a cinco minutos, creo que lo bajaré para mostrar que minará un bloque en cinco minutos.

`node simulate.js`

Acabo de crear una transacción, ha creado algunas transacciones aleatorias. Si también quieres ejecutar este script estarás generando transacciones. Vamos a ir más de cinco minutos, eso está bien. Generando al azar, vamos a minar cada cinco minutos. Así que vas a conseguir más de una simulación del mundo real donde hay muchas más transacciones y vas a analizar mucho mejor. Te voy a mostrar. Aquí hay un script que escribí para conectarse directamente a la red. No estoy pasando por el RPC, estoy TCP/IPing en uno de los nodos, haciendo una conexión, haciendo el handshake, versión, verack, mensaje de inventario y todo eso. Usted será capaz de ver que aquí, esto es sólo para fines de demostración.

`node peers.js`

Me conecté, hice mi apretón de manos, ahora estoy esperando. Tengo el otro funcionando en segundo plano. Eventualmente debería ver transacciones entrando. Envié un comando `getdata`, recibí un mensaje de inventario diciendo que hay una transacción. Dije que no tengo esa envíamela. Envié el comando `getdata` y luego recibí una respuesta. Si estás desarrollando y conectando es útil para eso. Si vuelvo a Regpool ahora tengo un par adicional. Puedo solucionar problemas de mi código ahora que mi versión está funcionando. Si estás escribiendo código para conectarte a un peer es una forma práctica.

P - ¿Hacen el apretón de manos en hexágono crudo?

R - Sí. Todo esto es Javascript. Acabo de revisar la especificación y dice que aquí está el handshake. Todos los mensajes tienen los bytes mágicos, luego tiene la cabecera del mensaje que siempre está en el mismo formato. Luego tiene una carga útil. Me limité a leer todo eso, experimentar y ver qué salía.

P - Lo hicimos en la clase de Jimmy Song.

R - He estado leyendo su libro y haciendo todo en Javascript para poder hacerlo en lugar de copiar el código de Python y modificarlo. Javascript no sería mi primera opción, pero es lo que conozco y era la forma más rápida de aprender.

Eso es parte del entorno de desarrollo. Quería que lo configuraras, es opcional. Puedes ver cómo entran las transacciones.

P - ¿Qué archivo es ese en el repositorio?

R - Es una repo diferente, la que realmente se está conectando directamente. La idea es simular. Si te conectaras directamente y no hubiera simulación estarías sentado en una pantalla en blanco. Tendrías un ping, tendrías un pong. Eso es un montón de cosas al azar que hago para mi propia educación. Quería compartirlo. Si las cosas funcionan para mí y prefieres Javascript sobre Python. Si no eres un tipo de Python y prefieres Javascript hay otra alternativa. Usted puede ir a través y leer eso. Usted puede tratar de ejecutar estos scripts sólo para jugar con ellos y ajustar un poco. O simplemente para ver la red. Puedes poner puntos de interrupción en tu código y ver que algo no sucedió. La idea es tener una herramienta de solución de problemas.

Volvamos a este tipo. Estoy bastante seguro de que ya miné un bloque. Averigüémoslo.

Regpool - `getblock [add getbestblockhash result]`

Han pasado más de cinco minutos. Ahora tengo un bloque que se parece más a un bloque, no es sólo una transacción de Coinbase. Así que ahora si quiero empezar a analizar bloques tengo algo con lo que trabajar. Tengo otro script de prueba, sólo yo jugando por aquí. Está haciendo un montón de cosas, pero una de las cosas es el cálculo de una raíz de Merkle, voy a dejar que al final. Aquí tengo un ejemplo del libro de Andreas. Puedo volver al bloque que acabo de crear. Aquí está lo que debería ser la raíz de Merkle. Pondré eso ahí. Sólo estoy console.loging a cabo. Estoy calculando una raíz e imprimir lo que es y debe coincidir. Tomaré todos estos tipos y los pegaré allí. Tomaré la muestra de Andreas y la pondré ahí. Ahora si voy y ejecuto eso.

`node main.js`

Está haciendo un montón de otras cosas. Tengo algunas cosas que debería haber comentado. Estoy experimentando con bloques compactos, hay algo después de la raíz Merkle. Parece que coincide. Esa es otra ventaja de la simulación. Puedes tener bloques con datos en ellos. Te llevaría un rato escribir Alice enviando a Bob y Bob enviando a Alice y hacer eso todo el día y luego intentar generar un bloque. Es una herramienta más para ayudarte. De eso se trataba. Para tener un entorno local útil donde no estás en la blockchain, no tienes que preocuparte de sincronizar cada vez, cada vez que cierras tu portátil y vuelves a subir.

## PREGUNTAS Y RESPUESTAS

P - ¿Cómo funciona el simulador aleatorio?

R - Simplemente está hablando con el servidor RPC y está enviando comandos, ese simple `sendtoaddress`. Elige una cantidad aleatoria y la crea.

P - ¿Son todas las transacciones válidas?

A - Sí. Déjame sacar el código (simulate.js). Voy a generar una cantidad aleatoria entre 0 y 2 y obtendremos una nueva dirección. Estoy en mi propio entorno local. Estoy enviando todo el dinero a mí mismo. Desde la perspectiva de Bob y Alice no saben eso. Parece como si alguien creara transacciones y las enviara por la red. Obtengo una nueva dirección, envío a la dirección y luego le doy esa cantidad aleatoria. Luego envío. Tengo un temporizador aquí para que cada cinco minutos vaya a la mía.

P - ¿Tienes transacciones que estás escupiendo y tienes bloques que estás escupiendo?

R: Sí. Si estuvieras haciendo Bob y Alice mientras se ejecuta, también estarían ahí. Pero de esta forma tienes una cosa minera. Es más parecido al mundo real.

P - ¿Puede regtest abrirse a la red? ¿Puede hacer que un puerto esté disponible en Internet y luego simplemente conectarse a un montón...

R - Usted tiene los bytes mágicos, que determinan su red. Eso es lo primero de cada mensaje. Así que cada mensaje comienza con los bytes mágicos. Hay tres diferentes.

P - ¿Si Michael y yo quisiéramos estar en la misma red regtest? ¿Es probablemente un reto de red?

R - ¿Podrías simplemente abrir un puerto? No se. Sería una buena idea pero no lo sé. No tendrías que descargar testnet.

Podrías probar la interfaz de usuario y esas cosas. Podrías tener desarrollo cooperativo y tener lo mismo... Realmente no necesitas hacer eso. Puedes ejecutarlos por separado, no tienes que ver exactamente los mismos números.

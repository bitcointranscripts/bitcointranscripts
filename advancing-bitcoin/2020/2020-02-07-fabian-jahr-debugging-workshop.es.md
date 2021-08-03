---
title: Fabian Jahr - Taller de depuración (2020-02-07)
transcript_by: Michael Folkson
translation_by: Blue Moon
categories: ['taller']
tags: ['bitcoin core']
---

Nombre: Fabian Jahr

Tema: Taller de depuración de Bitcoin Core 

Localización: El avanece de Bitcoin

Día: 7 de febrero de 2020

Vídeo: No se ha publicado ningún vídeo en Internet 

Presentación de Fabian en el Bitcoin Edge Dev++ 2019: https://btctranscripts.com/scalingbitcoin/tel-aviv-2019/edgedevplusplus/debugging-bitcoin/

Depuración de Bitcoin Core doc: https://github.com/fjahr/debugging_bitcoin

Taller de depuración de Bitcoin Core: https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386

# Introducción

En primer lugar bienvenido al taller de depuración de Bitcoin Core. Todo lo que sé más o menos sobre el uso de un depurador para aprender de Bitcoin Core y para solucionar problemas en Bitcoin Core. No he ido con diapositivas tradicionales porque quiero enseñarte a usar esta herramienta, el depurador, en el contexto de Bitcoin Core. Puede que no lo necesites en la próxima semana pero quizás lo necesites en tres semanas. Si has olvidado lo que hicimos aquí espero que puedas volver a este documento, mirarlo y usar estas instrucciones de nuevo. Por eso lo he estructurado como un gist. [Este](https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386) se mantendrá y será algo que podrás utilizar más adelante. Aprenderemos a usar estas herramientas. Personalmente estoy usando lldb porque estoy en MacOS. La gente en Linux puede instalar lldb pero puede que no sea tan bueno. gdb también está disponible, ha existido mucho más tiempo que lldb. Se supone que es una versión mejorada de éste. Estoy mostrando diferentes versiones de los comandos para que puedas seguir usando gdb de la misma manera. Yo estoy usando lldb pero si estás usando gdb y te encuentras con algún problema me acercaré y te ayudaré. Intentaremos solucionarlo. Te mostraré algunos comandos básicos y cómo usarlos en el contexto de Bitcoin Core. Luego tengo ejercicios. Estos ejercicios son más bien simulacros, no son súper emocionantes. El punto es que estás usando las herramientas. Te voy a dar un ejercicio en el que podrías encontrar la respuesta a este ejercicio con sólo mirar el archivo en el código. Pensé que si edito el código y te doy una versión específica que tienes que arreglar estaríamos todos sentados y compilando mucho. Realmente no quería hacer eso porque es normalmente donde el taller se rompe y todo el mundo está sentado compilando, diferentes cosas pasan para diferentes personas. Todos haremos esto en el master y miraremos el código. Al mismo tiempo, si tienes algo que crees que es más interesante que el ejercicio que te doy, si tienes algo que quieres depurar, una parte diferente del código, por favor sigue adelante y explora. Yo seguiré viniendo y ayudándote si tienes algún problema. He estructurado para esto dos horas. Ahora tenemos tres horas, así que hay mucho más tiempo para cavar en las cosas tanto como quieras. Nos mantenemos en un nivel alto. Puedes usar depuradores para profundizar mucho más en el código.

# ¿Por qué depurar con lldb y gdb? 

En primer lugar, ¿qué es un depurador? Un depurador es una aplicación que se utiliza para depurar otra aplicación. Realmente no hay mucho más que eso. Se trata de recorrer el código. Lo haces estableciendo puntos de interrupción en los que se detiene la ejecución del programa. Entonces puedes ir a través de la ejecución del programa paso a paso. Usted puede evaluar las cosas que están sucediendo. Puedes mirar las variables, cuál es su contenido. Puedes ejecutar expresiones, añadir variables si quieres. Puedes mirar a través del backtrace, el backtrace es el conjunto de funciones que se están ejecutando en ese momento. ¿Por qué me importa esto? Vengo de lenguajes de programación de mayor nivel que C++. Mi primer trabajo profesional como programador fue usando Ruby. Allí era típico saltar a pry. Pry era el depurador. También tienes que interactuar con el shell interactivo de Ruby. pdb es la herramienta comparable en Python. Lo usaba casi todos los días mientras averiguaba cosas en Ruby. Cuando entré en C++, principalmente motivado por Bitcoin Core, sentí que no había ninguna herramienta. Entonces descubrí gdb y lldb. La mayoría de la gente no está usando eso en la medida que yo hubiera pensado en el desarrollo de Bitcoin Core. He conocido a bastantes personas que están contribuyendo a Bitcoin Core y piensan que es demasiado trabajo usar estas herramientas. No las usan muy a menudo. Prefieren confiar en las declaraciones de impresión o algo así. O se quedan mirando el código hasta que se renderiza. Eso es válido, estas personas siguen siendo productivas, pero para mí quería tener esta herramienta en mi cadena de herramientas. No es algo que use todos los días, pero lo uso con bastante frecuencia, sobre todo cuando me quedo atascado. Si puedo resolver un problema en pocos minutos mirando el código y leyendo a través de él, pero a menudo me quedo confundido sobre el código. Saltar al depurador es otra forma de explorarlo y entender mejor lo que está pasando. Por eso es una herramienta muy útil. Definitivamente me ha ayudado en diferentes situaciones. Tanto si eres un completo principiante, como si nunca has contribuido con código a Bitcoin Core o si ya tienes algunas contribuciones pero no utilizas un depurador muy a menudo, esto te ayudará a adoptarlo.

# ¿Por qué utilizar la interfaz CLI simple? 

Utilizaremos lldb y gdb con la interfaz CLI simple. Yo personalmente también hago esto. La razón de esto es que generalmente me gusta estar en la línea de comandos. También trato de mantener mi configuración lo más simple posible. Me gusta que sea portátil. Si estoy en una máquina que no he configurado yo mismo y que he personalizado mucho, normalmente podré encontrar mi camino. También uso Vim, que está en casi todas las máquinas. Tengo algunos comandos personalizados pero intento mantenerlos al mínimo porque me gusta poder saltar a la máquina de otras personas y me gusta la programación en pareja. Cuando tengo la oportunidad de colaborar con alguien, usando su teclado, todavía es posible. Hay algunos GUIs para lldb y gdb que presentan el contenido de una forma más agradable. He mirado en estos pero no había ninguna primera opción obvia que saltó a mí. La mayoría de los productos que vi allí, no había commits para varios años. Pensé que me quedaría con la versión más simple que se me ocurrió. Eso es lo que vamos a utilizar hoy. Sin embargo fuera de la caja lldb y gdb también ofrecen un modo GUI. Este muestra las cosas de manera un poco diferente. No puedes ejecutar los mismos comandos allí. Hay una visión general de la información que se esconde detrás de los comandos. Lo mostraré brevemente y puedes jugar con él también. En lldb sólo tienes que escribir `gui`. Lo mostraré pero no me ha sido tan útil. Los preparativos que espero que todo el mundo haya hecho ya.

`./configure --enable-debug` aka `-O0 -ggdb3`

Usted construye Bitcoin Core de la misma manera que se describe en la documentación. Pero tienes que configurar con esta opción `--enable-debug`. Lo que esto significa es que pasas las banderas `-O0` y `-ggdb3` al compilador. No hay optimizaciones. `-O0` significa dejar fuera las optimizaciones. Típicamente se compila con `-O2` creo. ¿Por qué no queremos optimizaciones? Porque el compilador elimina información del código y también reestructura el código de una manera que hace más eficiente su ejecución en un sentido general. Si ejecutaras este `--enable-debug` como un nodo completo verías un rendimiento degradado. Lo que queremos hacer es mirar el código. Por eso quieres tener tanta información disponible como sea posible. Ponemos las optimizaciones a cero y esta otra instrucción mantiene alrededor alguna información adicional a la que puedes acceder cuando estás haciendo la depuración.

# Comandos útiles 

https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386#useful-commands

Te hablaré de un par de comandos. Estos son los comandos que he estado utilizando principalmente. Los he presentado en esta [tabla comprimida](https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386#useful-commands). Hay muchos más comandos disponibles en lldb y gdb. Al final tengo un mapa completo de comandos que lista los comandos que están disponibles en gdb y lldb al mismo tiempo. Puedes explorarlos también. Para los ejercicios y para empezar esta lista será suficiente. Mostraré algunas cosas demostrándolo. Luego puedes volver a esta lista y usarlas. En primer lugar, cuando haces cosas con el depurador, primero tienes que cargar el programa que quieres inspeccionar. Lo hacemos en la línea de comandos escribiendo:

`lldb /path/to/foo.app`

Le proporcionas la ruta del ejecutable que estás utilizando. Si estás en la carpeta de Bitcoin Core sería `src/....` Luego interactúas con los puntos de interrupción. Como he mencionado, un punto de interrupción es un punto que se establece en el código. Puede estar en una función pero también puede estar en una línea específica. Hay diferentes maneras de hacerlo. Puedes establecerlos con diferentes comandos. Después de suministrar este comando `lldb /ruta/al/foo.app` estarás en un shell interactivo que te permite interactuar con lldb y establecer puntos de interrupción. Si ya ha establecido algunos puntos de interrupción, puede utilizar el comando `breakpoint list` para obtener una lista de todos los puntos de interrupción que se establecieron. Puede establecer puntos de interrupción proporcionando el nombre del archivo. `breakpoint set -f foo.c -l 12` foo.c es sólo un ejemplo estúpido y luego la línea, esto significa que se establece un punto de interrupción en esta línea específica en ese archivo específico. Esta es la forma más precisa. También puedes establecer un breakpoint en un nombre. `breakpoint set -n foo` Eso sería típicamente el nombre de una función o algo así. Yo hago esto por conveniencia bastante a menudo. Es peligroso porque esto lo establecerá en cada función que tenga ese nombre en todo el código base. Si quieres ser preciso debes ir con la otra opción, pero si sabes que sólo hay un nombre o estás ejecutando lldb en un entorno controlado y sabes que no vas a golpear ninguna otra función haciendo otras cosas, entonces puedes usarlo. Hay otras tres o cuatro formas de establecer puntos de interrupción en esa tabla. También puedes eliminar puntos de interrupción. `breakpoint delete 1`. También puedes desactivar y volver a activar los puntos de interrupción. Yo no hago mucho esto porque normalmente establezco un punto de interrupción, lo golpeo, miro alrededor y luego cierro el proceso. Tomo algo de código, tal vez lo recompilo y luego vuelvo a empezar. Las opciones están ahí para hacer una investigación mucho más amplia. Usar diferentes puntos de interrupción, listarlos, habilitarlos, deshabilitarlos. Yo no he hecho esto extensivamente. Esto es interesante pero tampoco lo he usado mucho. `watch set var global` Puedes establecer puntos de interrupción. Esto es un punto de interrupción que se activa si se escribe en una variable específica. Si estás interesado en saber cuándo cambian las globales, cuándo se escriben en ellas, puedes establecer puntos de control en las globales. Entonces, después de haber establecido diferentes puntos de interrupción y cualquier punto de vigilancia, se ejecutará el ejecutable. Hasta este punto el proceso bitcoind que iniciaste, el programa que cargaste aquí, no se ha ejecutado. `run` es el comando que se utiliza para iniciar el proceso. Este es también el punto en el que añades argumentos a ese proceso bitcoind en ejecución. Hay diferentes maneras de suministrar los argumentos. Esta es la que yo utilizo, nombrándolos igual que cuando ejecutas bitcoind en general, nombrándolos aquí después de `run`. Otra forma de cargar un programa es adjuntándolo a programas ya en ejecución. Esto será interesante cuando veamos cómo adjuntar a un bitcoind que está siendo ejecutado por una aplicación funcional. Esto es súper útil. Algo que aún no he usado pero que es súper interesante es que puedes nombrar el proceso y luego dejar que lldb lo espere. Esto puede ser interesante si tienes una aplicación de terceros que está lanzando bitcoind para ti de una manera específica. Existen proyectos como Node Launcher de Pierre Rochard que lanzan Bitcoin por ti y lo gestionan por ti. En este contexto esto puede ser algo útil para usar. Cuando se llega a un punto de interrupción se puede inspeccionar un programa. Tengo más instrucciones al respecto aquí abajo. Cuando hayas terminado de inspeccionar entonces usarás `continue` para dejar que tu programa se ejecute si estás interesado en ello. Tenemos diferentes instrucciones `step`. Hay diferentes nombres para estos. Stepping in significa que si estás en una línea que tiene una llamada a una función, entonces entrarás en esa función. Estás en la función foo y eso tiene una función bar, estás en esa línea. Si pisas en ese contexto entrarás en la función bar. Cuando `step-over` o `next` entonces sólo irás a la siguiente línea de la función foo y no entrarás en la función bar.

P - ¿Ejecutará la función hasta el final? ¿Si se hace un `step-over` ejecutará esas líneas o simplemente las ignorará?

R - Ejecutará la barra completamente.

P - Hay mejores herramientas hoy en día, basadas en GUI. ¿Por qué utiliza cosas tan primitivas?

R - He intentado explicarlo al principio. No he encontrado ninguna herramienta que me haga feliz que esté basada en GUI. ¿Qué herramientas te gusta utilizar?

P - Visual Studio

P - ¿Es de código abierto?

R - No he encontrado ninguna que me haga feliz en poco tiempo. Me gustan estas herramientas sencillas. No le estoy diciendo a nadie que siga ese camino. Esta es la forma en que yo trabajo y al mantener el taller de la misma manera todo el mundo no tiene que instalar estas herramientas.

P - ¿Cuáles son las ventajas además de ser una GUI?

R - Con una GUI puedo pasar el ratón por encima y ver su valor. Puedo hacer todo lo que se describe allí mucho más rápido cuando tengo herramientas diseñadas para un humano. Por eso se inventaron las GUI.

Si hacemos `step-over` entonces la función `bar` se ejecutará normalmente pero luego bajará a la siguiente línea. También tenemos `step-out` o `finish` que significa que dejaremos `foo` y entraremos en la función que estaba llamando a `foo`. Este es un buen ejemplo para mostrar la diferencia entre lldb y gdb. gdb ha existido por mucho tiempo pero es un poco inconsistente con estos comandos. Utiliza el comando `step` para entrar, el comando `next` para salir y el comando `finish` para salir. Me gustan y los uso en lldb porque son alias en lldb. Pero al mismo tiempo no son muy precisos. Por eso se creó lldb, para limpiar esto. lldb tiene comandos primarios `thread step-in`, `thread step-over` y `thread step-out` que son mucho más precisos. Muestran lo que hacen pero también tienes los alias de gdb en lldb. En este caso los prefiero y los uso. Luego interactuar con hilos, no hay muchos puntos en los que haya interactuado con hilos. Lamentablemente esto también me ha creado algunos problemas. En uno de los ejercicios te voy a dar una pista en la que pisas algo porque la razón por la que hay algunos problemas con los hilos es que Boost los usa como librería y creo que esto está confundiendo el proceso de depuración. Puedes mirar los diferentes hilos y puedes saltar entre ellos pero no es algo que vaya a tocar. Hay diferentes comandos en la lista completa.

P - Acabo de intentar compilar con el parámetro `-O0` y dice que es una opción no reconocida.

R - ¿Has ejecutado `./config --enable-debug aka -O0 -ggdb3`? Esto es para explicar lo que hace `enable-debug` en el proceso de configuración.

P - ¿Son parámetros para `enable-debug`?

R - El resto es sólo una explicación de lo que significa. Lo que hace `enable-debug` es establecer banderas para el compilador que son las optimizaciones `0` y `gdb3`. Eso es lo que se usa internamente. Sólo lo puse como una explicación de lo que realmente está pasando, lo que este `enable-debug` está haciendo. Sólo necesitas `enable-debug` cuando lo ejecutas.

Puede imprimir variables, que es una de las principales cosas que probablemente va a hacer cuando está utilizando un depurador. En lldb tienes que hacer una distinción entre una variable de marco de pila y una variable global. Mientras que con gdb no hay distinción. Usas `p` para ambas. Puedes interactuar con variables de entorno, yo no lo he usado mucho. Puedes evaluar expresiones. Esto es algo que uso mucho. Si quieres ejecutar una función y ver lo que la función devuelve o si quieres establecer una variable a un valor específico eso es lo que haces con `expr`. Significa que ejecutas esta línea de código ahora mismo y luego sigues. También puedes buscar información de símbolos si tienes problemas con variables que vienen de otras bibliotecas.

# Varios consejos 

Luego tengo algunos consejos generales. Si está ejecutando lldb y encuentra que estos comandos son un poco demasiado para escribir, puede abreviarlos y efectivamente hacer una coincidencia regex en él. La coincidencia más corta con estos comandos puede ser la que usted desee. Si quieres establecer un punto de interrupción también puedes hacer `br s` y hará lo mismo. Me gusta escribirlos pero si quieres optimizar tu flujo de trabajo y no escribir tanto puedes hacer esto. Puedes poner un archivo `/.lldbinit` si quieres. Así es como se personaliza el entorno. Por ejemplo puedes personalizar como se imprimen las variables. No lo he usado todavía pero es algo que puedes investigar si te encuentras usando el depurador cada vez más y quieres personalizar tu entorno. Un detalle que me irritó cuando empecé a usar el depurador es que si entras en un bucle y el bucle es muy largo no hay instrucciones claras de cómo salir de ese bucle. No hay un comando de salida de bucle en lldb o gdb. La forma en que resolvemos esto es que si tienes un punto de interrupción en ese bucle, primero estableces un punto de interrupción detrás de ese bucle y luego sales de ese punto de interrupción.

# Ejercicios

Ahora estamos finalmente en los ejercicios. Haré una pequeña demostración de cómo iniciar un depurador para este primer ejercicio. Puedes explorar esto tanto como quieras. Luego, después de algún tiempo, caminaré por ahí. Luego haremos la segunda parte que es donde usamos el depurador con pruebas funcionales.

Sólo quiero bitcoind de una manera muy estándar y luego interactuar con él a través de la RPC. Haré `lldb src/bitcoind`. El programa se ha cargado. He configurado mis parámetros en mi archivo de configuración para no tener que cambiar nada. Ya está configurado para ser regtest. Si no tienes regtest configurado puedes poner `-regtest`. Hago `run`, se ejecuta y se obtiene la salida de la manera estándar. Aquí puedo interactuar con él. Voy a establecer un punto de interrupción.

`breakpoint set -name getblockchaininfo`

Esto es un poco descuidado. No estoy utilizando el archivo y la línea en este momento, sólo para fines de demostración. Lo ejecuto. El proceso se está ejecutando ahora y el punto de interrupción se establece, pero nada va a suceder todavía.

`bitcoin-cli getblockchaininfo`

Ahora se va a ejecutar en el punto de interrupción y estoy en el comienzo de `getblockchaininfo`. Ahora puedes interactuar con él. Mira estos ejercicios. Te he dado algunas pequeñas ideas para mirar, probar y profundizar.

P - Has alcanzado el punto de ruptura y estás en una línea del código. Quiero ver el código alrededor de esa línea.

R - Aquí ves una ventana muy pequeña. Lo que tal vez necesites es la GUI que mencioné. Para ir a la GUI sólo tienes que escribir `gui`. Aquí no puedes interactuar con ella. Puedes ejecutar expresiones aquí. Por eso no lo uso. Vuelvo a una ventana donde tengo el código abierto de todos modos. Lo tengo en una ventana paralela.

P - ¿Si usted `enable-debug` y está en MacOS usará automáticamente lldb?

R - lldb es sólo un programa. No tiene nada que ver con Bitcoin. Puedes seguir ejecutando lldb en bitcoind sin `enable-debug`, sólo que la salida no va a ser muy útil.

Primero voy a iniciar bitcoind con lldb.

`lldb src/bitcoind`

He visto muchos de usar `-name` así que esta vez voy a utilizar el archivo y la línea. Si tienes una buena idea de dónde estás y a dónde quieres ir yo usaría el archivo y la línea. Estoy aquí en el archivo RPC `blockchain.cpp` y quiero entrar en esta función `getblockchaininfo`.

P - ¿Cuál es tu editor?

R - Vim

Quiero estar en esta línea. Las siguientes líneas son interesantes para mí.

`breakpoint set -f rpc/blockchain.cpp -l 1255`.

Ahora puedo `run`.

P - ¿Cuál es el comando de gdb para `breakpoint`? Dice comando indefinido.

R - `break`.

Ahora llamo a `getblockchainfo`. Uso `step-over` para llegar a una línea que me interese. Digamos que quiero ir a `getblockhash`. Aquí abajo haría `step-in` porque quiero ver de dónde viene esto. Aquí haría `step` y me meto en `getblockhash`. Puedo ver que estoy en `CBlockIndex` y esto está devolviendo `phashBlock` desde dentro de esa clase. Esto es todo lo que quería que hicieras para este primer ejercicio. Usando `step-over` para ir a través de diferentes líneas en `getblockchaininfo` y luego entrar en algunas de esas funciones que hice allí, paso más adentro para ver de dónde vienen los valores. Sólo para acostumbrarse a esta navegación con lldb.

P - Cada vez que llegas a un punto de interrupción, ¿sólo estás escaneando con tus ojos para ver si hay una palabra clave que sea interesante?

R - Cuando te metes en problemas en los que ya no entiendes lo que está pasando en el código simplemente leyendo el código es cuando puedes usar el depurador. Es difícil crear ejercicios de forma artificial... Lo descubrirás simplemente navegando por los archivos.

P - ¿Cómo puedo ver el valor de una variable?

R - `target variable` es para las globales y `frame variable` es para el marco de la pila.

Así que esto es bastante básico lo que hemos hecho hasta ahora. Manejando el bitcoind a través de interacciones con bitcoin-cli. Hay muy pocos casos en los que haría esto porque suelen ser cosas muy básicas que están sucediendo. Se pone mucho más interesante si usted está utilizando las pruebas y desea inspeccionar lo que está pasando.

# Uso de la depuración con pruebas unitarias 

Las pruebas unitarias funcionan básicamente de la misma manera en cuanto al uso del depurador. Pero con las pruebas funcionales es mucho más interesante. Con las pruebas unitarias inicias el depurador de la misma manera que lo hacías aquí arriba con el CLI. Lo único que hay que tener en cuenta es que los tests tienen su propio ejecutable. En lugar de bitcoind tienes que proporcionar este archivo `test_bitcoin`. Ahí es donde se construyen las pruebas unitarias. Puedes establecer puntos de interrupción en cualquier parte de las pruebas unitarias exactamente igual que lo hacías con bitcoind. Las pruebas se ejecutarán. Si quieres ejecutar una prueba específica, que suele ser el caso, puedes certificarlo con este parámetro `--log_level=all --run_test=*/lthash_tests`. Puedes ir a la [documentación de las pruebas unitarias](https://github.com/bitcoin/bitcoin/tree/master/src/test) sobre cómo ejecutar las pruebas. No es tan diferente de bitcoind e interactuar con el CLI.

# Uso de la depuración con pruebas funcionales 

Lo que es mucho más interesante son las pruebas funcionales, lo que estoy depurando con más frecuencia. Por lo general, cuando estás investigando cosas en Bitcoin no son sólo cosas que son muy simples es que hay pasos muy complejos que sucedieron antes y se llega a un estado que se quiere investigar. Miramos el regtest y generamos 100 bloques, eso no es tan interesante. Lo que es mucho más interesante es si tienes una gran red P2P y quieres ver cómo los nodos están interactuando entre sí. Si tienes un mempool lleno y las transacciones son desalojadas del mempool no quieres tener que escribir un script para que tu nodo Bitcoin llegue a su punto. Por suerte ya hay pruebas funcionales que hacen eso por ti. Si quieres inspeccionar el estado del sistema entonces te recomendaría que encontraras la prueba funcional que está llevando al sistema a ese punto y luego inspeccionar el sistema cuando está siendo ejecutado por esa prueba funcional.

P - ¿Las pruebas funcionales son pruebas de integración?

R - Se denominan pruebas funcionales en Bitcoin.

Las pruebas funcionales están escritas en Python. Está en `/tests` en el repo. Usted encontrará un montón de pruebas de Python. También está el marco de pruebas. Ese es el primer paso que haremos juntos porque es algo que tienes que hacer si quieres hacer algo con estas pruebas funcionales. Está este archivo `test/functional/test_framework/test_framework.py`. Allí, en la línea 99, se especifica un tiempo de espera RPC. Lo que sucede es que este marco de pruebas cuando está ejecutando las pruebas, las está escribiendo en el RPC como lo haría un usuario y hay un tiempo de espera especificado. Normalmente, cuando se ejecutan las pruebas funcionales, se ejecuta todo el conjunto de pruebas. Hay más de 100 pruebas. No quieres tener esta prueba ejecutándose para siempre. Hay un tiempo de espera de 60 segundos, ninguna prueba se ejecutará más de 60 segundos. Lo que vamos a hacer es detener la prueba funcional de la ejecución, a continuación, vaya en el nodo que está bajo la prueba y hacer algunas cosas allí. Probablemente no vamos a ser capaces de hacer eso en 60 segundos. Es por eso que tenemos que extender ese tiempo de espera. Me gustaría que usted vaya a la estructura de prueba funcional y cambiar este parámetro. Lo he cambiado a 6000. Por favor, actualízalo a un número más alto porque no quieres que la prueba se agote. Entonces su nodo se bloqueará y tendrá que empezar de nuevo.

He mencionado que tenemos estas pruebas funcionales de Python. Estos son la conducción de los nodos a través de la RPC al igual que un usuario lo haría. Lo que queremos hacer es inspeccionar estos nodos que se están ejecutando a través de la prueba de Python y ser capaz de depurar dentro. Lo principal que tenemos que hacer es acceder a ese proceso bitcoind que está siendo ejecutado por la prueba funcional. La prueba funcional no nos está esperando por sí misma, tenemos que detener la prueba funcional primero. No va a terminar antes de que podamos conectarnos a ese proceso bitcoind. La forma en que vamos a hacer eso es insertar esta línea `import pdb; pdb.set_trace()` que va a importar pdb y luego usar `set_trace` para establecer un punto de interrupción en esta prueba funcional. Es como el inicio. Primero estamos estableciendo un punto de interrupción en el programa de Python con el fin de detenerlo para que luego podamos establecer un punto de interrupción en bitcoind. Voy a hacer una demostración en un momento. Primero insertas esta línea en la prueba de Python que quieres inspeccionar. A continuación, ejecutar esa prueba manualmente, ejecutar ese archivo. Ese archivo se detendrá en la línea donde has insertado esta declaración `import pdb`. Entonces tienes un shell interactivo allí y puedes interactuar con la prueba. El test debería tener ya nodos que están dentro de este test y usando `process.pid` puedes llegar al proceso de ese nodo específico. Por favor, recuerda que si tienes varios nodos que están siendo probados en, por ejemplo, una prueba P2P, estarán bajo diferentes números. Tendrás un array con tal vez cinco o seis nodos y tienes que mirar la prueba y ver cuál es el nodo al que quieres adjuntar, al que quieres mirar para observar las cosas que te interesan. Ahora tenemos el ID del proceso en este punto. Ahora podemos iniciar lldb y luego podemos adjuntar a este ID de proceso que hemos visto corriendo allí. El ejemplo es `12345`. Entonces podemos hacer lo que queramos hacer allí. Podemos establecer puntos de interrupción. Usted estará familiarizado con lo que está viendo porque se verá igual que antes. Puedes establecer un punto de interrupción y luego dejar que el proceso continúe. En ese momento quizás esperas que pase algo pero no va a pasar nada porque el proceso sigue parado desde la prueba funcional. También tienes que te

Esta es una de las pruebas funcionales. Voy a probar `getblockchaininfo` de nuevo. Aquí hay una prueba funcional para `getblockchaininfo`. Hay una configuración específica en esta prueba y quiero ahorrarme hacerla manualmente. Aquí especificaría la línea que he descrito antes. He editado manualmente este archivo Python aquí, muy simple. Ahora voy a ejecutar ese archivo desde la consola. Debería pararse en algún momento. Ahora nos encontramos con el punto de interrupción de la pdb que establecí hace un segundo. Puedo buscar aquí el PID del nodo. Esto es un array. Si va a haber varios nodos que se están probando esta matriz tendrá más de un objeto en ella. Este es simple, solo tiene uno. Voy a hacer `process.pid` y esto me va a dar el PID del proceso que se está ejecutando en el fondo que está siendo ejecutado por la prueba. Tomo este PID y lanzo lldb. Quiero adjuntar a este nodo que se está ejecutando allí. `attach --pid 12345` Ahora hemos cargado este proceso bitcoind que se está ejecutando en segundo plano. Ahora puedo establecer mi punto de interrupción. `breakpoint set -name getblockchaininfo` Entonces voy a `continue`. En este punto el proceso se detiene dos veces. Una vez se detiene en Python y otra en C++ o lldb. Hago `continue`. Sigue parado en Python lo que me confundió como diez veces al principio. Vuelvo a teclear `continue` y ahora estamos en el punto de interrupción que he puesto. Este nodo está siendo ejecutado por la prueba funcional. Si hubo un millón de pasos antes en la prueba funcional este será el nodo que pasó por el millón de pasos. Ahora puede interactuar con el nodo. Esta es la magia. Son muchos pasos. A no ser que tengáis preguntas ahora dadle una oportunidad. Los pasos están en el documento y si te quedas atascado en cualquier lugar házmelo saber.

P - ¿Tiene 6000 segundos para averiguar qué está mal?

R - Usted tiene 6000 segundos desde el punto en que se inicia la prueba funcional, el archivo de Python. Es una restricción general que el marco de pruebas establece en las pruebas funcionales. Nadie debería querer nunca ejecutar una prueba funcional que tarde más de 60 segundos o un número arbitrario. No queremos que eso restrinja nuestra depuración.

P - ¿Importa qué archivo específico establecería el `import pdb`?

R - Quería probar `getblockchaininfo`. Las pruebas funcionales son instrucciones sobre lo que se ejecuta en este archivo pdb. Normalmente tendrás alguna pregunta sobre el estado específico o algo que ocurre en Bitcoin. Entonces te sugeriría que busques una prueba funcional que lleve al nodo a ese estado. Quizás quieras probar el desalojo del mempool. Para eso necesitas tener un mempool lleno para que la transacción más barata sea expulsada del mempool. Para hacerlo manualmente tendrías que escribir un montón de scripts o escribir mucho en la consola. Puedes buscar una prueba que esté haciendo exactamente eso por ti y luego detener esa prueba e insertar la parada pdb allí y ejecutar esa prueba. También podría ejecutar el conjunto de pruebas funcionales completo, pero tendría que esperar más tiempo.

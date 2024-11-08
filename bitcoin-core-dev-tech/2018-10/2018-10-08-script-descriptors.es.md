---
title: Descriptores de guiones (2018-10-08)
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - wallet
aliases:
  - /es/bitcoin-core-dev-tech/2018-10-08-script-descriptors/
---
2018-10-08

# Descriptores de guiones

Pieter Wuille (sipa)

<https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md>

Me gustaría hablar de los descriptores de guiones. Hay varios proyectos en los que estamos trabajando y todos están relacionados. Me gustaría aclarar cómo encajan las cosas.

Nota: hay una transcripción anterior que no ha sido publicada (necesita ser revisada) sobre los descriptores de guiones.

# Agenda

* Historia de los descriptores de guiones y cómo llegamos a esto.
* Lo que hay actualmente en Bitcoin Core v0.17
* Integración de la cartera
* DESCRIPCIÓN

# Sobre los descriptores de guiones

El problema que quería abordar era que actualmente en el monedero de Bitcoin Core tenemos un montón de claves públicas y claves privadas y cadenas de HD y scripts y un montón de otros metadatos y keypools. Todos ellos se alimentan entre sí y afectan de manera diferente a lo que se puede firmar y a lo que consideramos nuestro. La lógica que existe actualmente sobre cómo determinar qué resultados son nuestros es una especie de copia de la lógica de firma que dice "puedes firmar esto". Pero con la advertencia de que, para la firma múltiple, necesitamos que todas las claves privadas estén ahí. En varios niveles, siempre que a través de la recursividad de los diferentes scripts involucrados si hay algo que se considera algo "watchonly" que es un conjunto separado de scripts, entonces también lo consideramos nuestro. Hay una distinción entre lo que es solucionable y lo que es vigilado. Resoluble significa, que seríamos capaces de firmar esto ignorando que no tenemos las claves. Solvability significa que podemos determinar el tamaño del gasto, útil para la estimación de la tarifa, la transacción de fondos, la selección de monedas y ese tipo de cosas. No está muy claro cuál es el razonamiento entre los datos que hay en tu cartera y cómo afecta a la solvencia y a la capacidad de gasto, y lo hemos empeorado involuntariamente en la v0.17.

Los descriptores de script son un lenguaje simple para describir las condiciones de gasto. Es un lenguaje para computar scriptspubkeys, scripts de salida, junto con toda la información necesaria para gastarlo. El descriptor más simple sería PKH(0302....), una pubkey hexagonal con PKH alrededor significa pay-to-pubkeyhash para esa clave pública. Esto contiene más información que sólo la dirección porque te dice la pubkey real involucrada. Como mínimo, te dice si es una clave comprimida o no, lo que importa para la solvencia.

También puedes hacer cosas como SH(multi(2,02..., 04..., 05...)) esto significa p2sh de un multisig de `3` de estos `3`. El lenguaje puede hacer todo tipo de construcciones multisig al menos las basadas en checkmultisig. Todo esto está en Bitcoin Core v0.17 pero sólo está expuesto a través de un único RPC.

Hay laso WPKH() que es la versión testigo de PKH(). También está WSH() que es la versión de pago a testigo-scripthash. También puedes usar estos recursivamente como SH(WSH(PKH(...))) y esto funcionará; no lo hagas, es una tontería. Pero funciona. Sólo muestra la capacidad de composición disponible. Además, puedes usar PK() para una pubkey simple. Eso también funciona.

En cualquier lugar donde escribas una clave pública, puedes también escribir un xpub con una ruta de derivación y puedes opcionalmente terminarlo con una estrella de barra que significa todos los hijos directos de esta clave. No se refiere a una sola scriptpubkey sino a una serie no muy infinita. La persona que llama debe tener en cuenta un rango o un límite de espacio. Conceptualmente, un descriptor de este tipo se refiere a todos los hijos en un determinado orden.

El objetivo era reemplazar la lógica de ismine en la cartera de Bitcoin Core. En lugar de importar pubkeys, scripts y todas estas cosas, importarías uno o dos descriptores y dirías este es del que saco mis direcciones y este es del que saco mi cambio. Podría haber algunos metadatos junto con un descriptor, como de dónde viene, si necesito un monedero de hardware, si es sólo de vigilancia, cuál es la fecha de nacimiento, y todas estas cosas se convierten en metadatos para el descriptor en lugar de para las claves individuales. Esto aún no se ha hecho.

P: ¿Qué se ha hecho hasta ahora?

Hay un módulo que implementa los descriptores. Los analiza, puede exportarlos, hay pruebas en torno a ellos. Sólo se exponen a través de scantxoutset RPC. Puedes darle un descriptor y recorrerá todo el conjunto de UTXO y encontrará salidas para todo lo que coincida con el descriptor.

Una cosa desagradable en particular que espero que esto resuelva es la confusión sobre "bueno, di una dirección segwit y alguien la convirtió en una dirección p2pkh y no puedo distinguir entre... no puedo decirle a mi billetera que sólo vea una versión de ella". Tal vez tengo una billetera de hardware que sólo puede firmar una de ellas y no quiero confundirme pensando que me pagan por algo que no puedo gastar. Los descriptores pretenden estar bien definidos. Podemos añadir extensiones a las construcciones que se soportan, pero la idea es que lo que se soporta nunca cambia a qué scriptpubkey se refiere. Dada una cadena de descriptor, está bien definido a qué scriptpubkey se refiere, y se pretende que nunca cambie.

En lo que me gustaría trabajar a corto y medio plazo es en cambiar la lógica de ismine en la propia cartera para que se puedan importar registros (en combinación con un descriptor y metadatos). Tal vez convertir todo el material antiguo en este nuevo modelo, porque es más compacto y más fácil de razonar. Pero hay que tener en cuenta los problemas de compatibilidad.

P: ¿Cuáles son los problemas de compatibilidad?

Bueno, no puedes hacer un downgrade después de hacer esto si conviertes una cartera existente.

P: También podrías hacerlo en el momento de la carga.

Esta no es una operación simple, para convertir. Tienes que iterar a través de todos los scripts que podrías ver y alimentarlos a través de la lógica existente. He implementado esto, pero incluso para una cartera simple, es menos de un segundo pero es doloroso. Hay muchas combinaciones para probar. Sí, seguro que podrías hacerlo en tiempo de carga, pero no es tan interesante, creo.

P: ¿Y si mantenemos la antigua lógica de ismine para los monederos antiguos? Eso es doloroso. Tenemos que mantener dos vías paralelas.

Sí, pero creo que se puede encapsular el nuevo material muy bien donde se dice aquí están los datos, aplicar ismine a ella. Hay diferentes consideraciones allí. No sé cuál es la mejor solución allí.

# DESCRIPCIÓN

Quiero hablar de algunos de los trabajos en los que hemos estado trabajando, Andrew y yo y otras personas en Blockstream. Queremos tratar, bueno, ¿qué pasa si quieres hacer cosas más complejas con los scripts? Tenemos cosas internas que utilizan scripts más complejos, tenemos scripts relacionados con los rayos, ¿qué pasa si quiero hacer algo como un multisig que después de algún tiempo se degrada en un multisig más débil? Como un `2` de `3` pero después de un año puedo pasarlo con sólo una de esas claves y cosas así. ¿Cómo se pueden construir políticas componibles en Script? Script es un lenguaje de ejecución basado en la pila que es realmente difícil de razonar. En la práctica, la gente simplemente hace coincidir un patrón con una cosa determinada y entonces, oh, sé cómo firmar multisig, o p2sh multisig, o sé cómo firmar multisig incrustado en el testigo... pero generalizar esto es una especie de dolor.

Una cosa que se nos ocurrió es lo que estamos llamando DESCRIPT es un subconjunto del lenguaje de scripting de bitcoin. Sólo está algo relacionado con los descriptores de scripts. Permítanme hablar de esto primero y luego los conectaré. Es un subconjunto de script que puede encarnar AND, OR y umbrales (aquí hay un número de subexpresiones y k de ellas necesitan ser satisfechas). Es una generalización de multisig, pero no sólo multisig. Por ejemplo, la situación en la que hago un escrow de `2`-de-`3` pero uno de los participantes está utilizando una cartera de hardware por lo que es un `2`-de-`3` donde una de las claves es realmente un `2`-de-`2` o algo así. Y, O, umbrales, controles de pubkey, hashlocks y timelocks. Creo que esto encarna todo lo que la gente utiliza el script, hoy en día. Todo es una combinación de esas cosas.

Encontramos un subconjunto de script que es componible en el que sólo dices que AND se traduce en esta secuencia de instrucciones y en este lugar sólo sustituyes otra cosa que puede ser cualquier cosa y en este otro puedes sustituir cualquier cosa y así sucesivamente. Hemos investigado varias construcciones para esto. Tenemos como cinco formas diferentes de escribir una construcción OR en el script de bitcoin. Los experimentos mostraron que todos ellos son útiles a veces. Cuál es la mejor depende del contexto, la probabilidad, la complejidad de las declaraciones dentro.

Tenemos un compilador DESCRIPT que toma algo que estamos llamando un lenguaje de políticas (AND, OR, umbral, clave pública, hashlock, timelock) junto con probabilidades para cada OR para decir si es `50/50` o si un lado de la OR es más probable que el derecho, y no encontrará el script óptimo sin suerte sino el script óptimo en este subconjunto de script que hemos definido.

P: ¿Podéis hacer que vuestro compilador produzca los guiones de los rayos?

R: Todavía no lo hemos probado.

P: ¿Manejan la maleabilidad de los testigos?

Los scripts que salen no son maleables según las reglas actuales de estandarización. Hacer las cosas completamente no maleables bajo las reglas de consenso es doloroso. No se puede hacer un rayo porque hay que comprobar si las firmas no están vacías si fallan. Creo que todo lo que es no maleable hoy en día se basa en las reglas de estandarización. Lightning es lo suficientemente simple como para que no haya firmas que fallen. Lightning tiene una construccion especifica en algunos lugares, como la bifurcacion basada en el tamano de la entrada como una forma de que sea una firma o una preimagen de hash, y eso es una solucion de maleabilidad. Bien, podemos extender DESCRIPT, podemos extenderlo con más construcciones si es necesario. Hemos tenido en cuenta la maleabilidad.

P: ¿La idea aquí es que esto sea algo que pruebe el monedero en el futuro, de modo que si alguien utiliza un script en el futuro, su antiguo monedero pueda ser hecho para reconocer el script?

El objetivo es que podamos ampliar el lenguaje DESCRIPT para que responda también a estos scripts. Podrías importarlos a tus carteras como watchonly o más general. Incluso sin la parte del descriptor, puedes tener una lógica de firma que funcione con cualquiera de estos scripts y que no necesite entenderlo. En particular, cuando hablamos de operaciones de transacciones bitcoin parcialmente firmadas (PSBT), puedes tener un actualizador - en realidad ni siquiera necesitas el actualizador, el actualizador puede simplemente reconocer que este es el script que estamos tratando de gastar y sé cómo gastarlo, sin que se le diga información adicional sobre esta es la semántica del script o lo que sea. Puedo entrar en cómo compila las cosas pero no sé hasta qué punto hay interés en eso.

P: ¿Y un ejemplo de multisig entre dos carteras?

R: Es sólo PSBT. No ha cambiado nada.

P: ¿Cuáles son los cinco tipos de OR?

Los OR más simples que puedes imaginar son aquellos en los que tienes un subíndice A y un subíndice B y utilizas un BOOLOR. Pero B necesita ser envuelto porque A está tomando sus argumentos de la pila. El problema es que se espera que A sea una expresión que ponga `0` o `1` en la pila en función del éxito. B debe omitir el 0 o el 1 que produce A. Así que tenemos diferentes convenciones de llamada para diferentes subexpresiones, tenemos seis convenciones de subexpresiones. La convención de llamada E es "tomar sus elementos de la pila y poner `0` o `1` en la pila". W es la versión envuelta y comienza con 00x y pone en la pila x y luego `0` o `1`. Compilas A en modo E y B en modo W. Así que ahora las dos cosas en tu pila son el resultado del éxito y usas un BOOLOR y esto en general es una expresión E.

Otro modo es lo que llamamos un CASCADE OR, que es ejecutar A y sólo cuando falla ejecutarás B. A DUP NOTIF B ENDIF. Aquí, B puede ser compilado como una "F" (forzada). Podrías satisfacer A, pone `1` en la pila, quita `1` en la pila y terminas con `1` en la pila. Tienes un 0 entrando en B por lo que está mal... OK, tiene que ser un IFDUP, que sólo se duplica si es `1`. Sin embargo, es un interruptor-izquierda. ....... Bien, tenemos que buscar esto. IFDUP NOTIF B ENDIF. IFDUP duplica si es verdadero. Si es verdadero, entonces notif fallará. Si es cero, sigue siendo cero, lo quitas y ejecutas B. El problema con esta construcción es que si quieres hacer que todo falle, entonces vas a satisfacer A y B, entonces esto es maleable-- no es maleable-- este es un mal ejemplo. Bien, lo que estamos demostrando aquí es por qué es necesario un compilador. Este es un estilo diferente de escribir un OR que tiene la ventaja de que si A se satisface entonces B ni siquiera se ejecuta, lo que tiene sentido si tanto B es probable que falle y caro que falle.

Puedes ir aún más lejos y tener un interruptor E directo donde tienes IF A ELSE B ENDIF. Esto toma una entrada adicional y te dice cuál de las dos ramas va a tener éxito, y el problema con esto es que es maleable. Cuando toda la cosa va a fallar, y si el IF select A va a fallar, entonces puedes modificarlo para que el IF tome la rama B y falle B. Asumimos que construir una insatisfacción es fácil. La forma en que resolvemos esto es introduciendo otro modo de compilación similar a una E pero tiene que tener éxito y ese es el modo "F" para forzar. Si falla, matará el script. Su único modo de fallo es abortar, y siempre tiene éxito poniendo un valor verdadero en la pila.

Entonces hay otras cosas que puedes hacer como en el nivel superior no requerimos realmente que un script ponga el cero en la pila para fallar. Puede abortar. Tenemos una versión que tiene éxito poniendo true en la pila, o falla poniendo 0 en la pila o abortando. Luego hay una versión que... es "T", de nivel superior. Tiene que poner TRUE en la pila pero no `1` en la pila. F sí tiene que poner 1 en la pila. ¿No tenemos nuevos nombres para estos que no son letras? Abortar o `1`. Entonces T es fail o `0`, o true (no cero). Esta es la razón por la que se compilan las construcciones de nivel superior como... tienes más libertad si se te permite fallar abortando. Un AND de nivel superior es simplemente concatenar dos cosas, si haces la primera... V, que es o nada o fallar.

Un AND en un nivel superior es una V más una T donde ejecutas la primera, si tiene éxito no hace nada y luego ejecuta la segunda. Si el primero falla entonces se aborta inmediatamente. Esto permite utilizar la versión de verificación de ciertos opcodes.

La sexta es la conveción de llamada "K" que es algo que falla, o pone una pubkey en la pila.  La razón de esto es que de otra manera terminas con construcciones IFTHEN ELSE donde ambas ramas terminan con un checksig lo cual es tonto, quieres el checksig fuera del IF. Para hacer esto, puedes compilar ambas ramas como la versión K que garantiza poner una pubkey en la pila, luego la conviertes en una T añadiendo un checksigverify después de eso.

Hay un número de piezas aquí. Estamos escribiendo una descripción de este subconjunto de script llamado DESCRIPT con su semántica y cómo firmarlo. Esto es ortogonal a todas las cosas de la cartera, realmente. Podemos escribir una descripción de DESCRIPT, y luego podemos escribir la lógica de la firma para cualquiera de estos scripts, porque hay una simple conversión de la notación de tipo descriptor al script, pero también el camino de vuelta, utilizando un simple analizador LR para mirar el script y averiguar la estructura. Es como un lookahead de un token. Es incluso más simple que el lookahead de un símbolo, es el lookahead de un token, siempre se sabe y no es exponencial en complejidad. Sin embargo, los analizadores LR son lineales. Investiga. Puedes hacerlo de forma lineal; sin embargo, la versión recursiva decente es exponencial. No necesitas un decente recursivo, puedes usar un parser lookahead. Puedes hacerlo incluso más simple... no necesitas leer ningún documento sobre el parsing, lo obvio es que sea lineal.

DESCRIPT es un subconjunto de script con el que puedes hacer algunas cosas. Puedes convertirlo de nuevo en una forma de árbol, y dada la forma de árbol puedes firmarlo y sabes cómo firmarlo. Entonces podemos añadir extensiones al lenguaje descriptor para este subconjunto de script. Así que podría haber diferentes tipos de Y, O con él. Luego está la importación a la cartera. La última pieza es un compilador desde un lenguaje de políticas de alto nivel hasta la forma del descriptor.

Que alguien me dé una política. `2-de-2` multisig, o después de un mes es cualquiera de las firmas. Así que esto sería AOR(MULT(2,A,B)) y esto es un OR asimétrico donde la rama de la izquierda es mucho más probable que la rama de la derecha, y entonces necesitas el otro lado, así que AOR(MULT(2,A,B),AND(CSV(1 mes), MULTI(1,A,B)). Podrías escribir A como una clave privada, si quieres hablar de la integración de la cartera. En la cartera, es la forma compilada. La compilación es algo lenta. El compilador va de la política a la versión compilada del script. La conversión entre la política y la versión compilada es una biyección, nunca cambia.

Se compila hasta un CASCADE OR, y luego hay una rama MULTI, y luego hay un.... el CASCADE OR es un estilo de ejecución T... la rama multi es una E, ... luego hay una rama AND.  Estás compilando en un descriptor. El lenguaje de políticas es algo que no hemos especificado aún. Hace cosas como las probabilidades. Así que cómo ir de un descriptor a un script, eso es una biyección. Es una cosa eficiente en ambas direcciones.

El compilador del lenguaje de políticas al descriptor no es trivial. Escribimos dos versiones con diferentes métodos, y luego comparamos los dos compiladores y averiguamos cuál producía las mejores versiones y lo optimizamos por esa vía. Usamos la pareja de primeros millones de scripts y compilamos a lo mismo. Cuando estás desarrollando tu aplicación, ejecutas el compilador una vez. Lo de AOR es la capa de políticas. Hay tres pasos, sí. Lo que es el nombre de la traducción de DESCRIPT a raw script es sólo una codificación. Es sólo una codificación.

Una de las cosas es la subexpresión común; si escribes una clave pública varias veces, esa clave acaba en el script varias veces. Esto podría mejorarse.

Ivy es un intento de hacerlo. Es un lenguaje tanto de nivel superior como inferior. Es más general. Utiliza variables explícitas. Dice que escriba un script que tome tres entradas, la primera, la segunda y la tercera y la primera entrada es la que va a esta clave pública. Esto no hace eso, sin embargo, esto trata las entradas como una cosa abstracta y usted acaba de escribir una política. Aquí dirías, timelock y multisig y no hay ninguna parte en este langugae que no aparezca ninguna firma. Sólo hay claves públicas. En Ivy, tratas las firmas como variables explícitas que se pasan.

El BIP dirá, esta cosa se firma de esta manera, esta otra cosa se firma de esta otra manera.

Nunca tratas con scripts crudos en la cartera; eso es lo que queremos eliminar. Usted importa un descriptor en su cartera, y eso es todo. Y ahora tiene toda la información para reconocerlo y gastarlo. Generas la escritura sobre la marcha, pero sólo almacenas el descriptor. Obtienes la dirección cuando la necesitas.

DESCRIPT es la venganza de los eltoo por razones de nombre. Yo llamaría al script existente FOOTGUN. Tal vez esto es DOBLEBARREL.

El descriptor se pone en la cartera. El lenguaje de la política puede ser compilado en un descriptor, y los descriptores corresponden al subconjunto de script llamado DESCRIPT. La política es la cosa asimétrica OR. El descriptor es la cosa del árbol de sintaxis abstracta... el descriptor puede convertirse en un script, y específicamente en un subconjunto llamado DESCRIPT. Si la cartera tiene el descriptor, ¿sabe cuál es la política? No se puede volver de un descriptor a una política, porque se pierde la información de probabilidad. Así que es posible que quieras mantener esos metadatos.

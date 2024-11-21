---
title: R&D Goals & Challenges
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - research
  - bitcoin-core
speakers:
  - Patrick Murck
  - Gavin Andresen
  - Cory Fields
---
A menudo vemos gente diciendo que están probando las aguas, que han corregido un error tipográfico, que han hecho una pequeña corrección que no tiene mucho impacto, que se están acostumbrando al proceso. Se están dando cuenta de que es muy fácil contribuir a Bitcoin Core. Codificas tus cambios, envías tus cambios, no hay mucho que hacer.

Hay una diferencia, y las líneas son difusas e indefinidas, y puedes hacer un cambio en Core que cambie un error ortográfico o un cambio en la política o en las reglas de consenso, para esas cosas de alto nivel, para las cosas a nivel de ecosistema, hay varias listas de correo, la lista de desarrollo es la que tiene más tráfico. Las cosas se debaten allí, se debaten en las redes sociales. Así que todo se reduce a qué cambios buscas, así que si estás añadiendo funcionalidad al propio programa es fácil hacerlo siempre que no sea controvertido.
º
Tocando lo que Gavin dijo, estamos trabajando en hacer las cosas mucho más modular. Tenemos confusión sobre el hecho de que tenemos pull requests para la tubería, así como los cambios de política, todo en la misma tubería, como cosas como la cartera o cosas como el minero comienzan a ser desglosado, no tenemos que preocuparnos de esos ethings, tenemos sólo el núcleo más central de grandes cambios divertidos. Es una manera de eliminar parte del ruido. Es una de las cosas en las que estoy trabajando actualmente. En cuanto a la contribución, yo diría que en realidad tenemos una barrera de entrada muy baja para cualquiera que realmente tenga algunos cambios funcionales que quiera hacer.

Estupendo. Así que de nuevo queremos hacer esto más de una conservación abierta para que no tenga que monopolizar el tiempo de Cory y Gavin. Más importante aún, vamos a abrir el turno de preguntas.

P: Gavin creo que dijiste que el monedero podría mejorarse mucho o eliminarse como requisito antes de la versión 1.0, y que sería decisión de la comunidad o algo así. ¿Consideras que el monedero tiene que ir a un repositorio separado antes de que Bitcoin Core pueda llegar a un sello de aprobación 1.0? ¿Podría ser mejorado de alguna manera, plausible liberarlo todo como 1.0?

R: Yo llamo a Bitcoin Core una implementación de referencia. Una buena forma de hacer un monedero para hacerlo está bien. Ahora mismo el monedero no es una buena implementación de referencia. No utiliza claves HD, y debería hacerlo. Hacerlo es básicamente una reescritura. Todavía utiliza BerkeleyDB, que no nos gusta por muchas razones. Preferiríamos una forma diferente de almacenar claves en el monedero. Debería interactuar con el hardware de almacenamiento de claves de alguna manera. Ahora mismo no lo hace. Si estuviera pensando en qué monedero sería un buen monedero de implementación de referencia, si tuviéramos eso creo que estaría bien si fuera parte de Bitcoin Core, y ahora mismo no lo tenemos.

P: ¿Pero quiere modularizarlo?

R: Puedes compilar Bitcoin Core sin el monedero. No me importa si es un repositorio separado o no. Si enviamos un Bitcoin Core 1.0 con el código del monedero, debería ser algo que pudiéramos señalar y decir que es la mejor práctica.

He visto otra mano, ¿quién será la próxima víctima?

P: ¿Quién se espera que ejecute un nodo de validación completo? El consumidor medio, las empresas, ¿quién esperaría que lo hiciera?

R: Um. Satoshi escribió sobre esto. Hay otra parte de la cita en la que se imagina que sólo las personas con máquinas en centros de datos estarían ejecutando nodos en el futuro, y todo el mundo estaría simplificando los nodos de verificación de pagos. Creo que a mucha gente no le gusta la idea de tener que alquilar un servidor en un centro de datos para manejar el volumen de transacciones de Bitcoin. Aunque personalmente estaría de acuerdo con eso, esperando que alguien pagara 100 o 200 dólares al año, creo que estoy en minoría aquí. Creo que la gente encuentra importante ejecutar nodos completos en sus ordenadores domésticos. Hoy en día solemos tener conexiones de red rápidas, y tener ordenadores rápidos en casa está bien. Creo que en el futuro podemos escalar con el volumen de transacciones que vamos a conseguir corriendo mi frase es una especie de la del aficionado geek, por lo que alguien con un ordenador bastante rápido y una conexión a Internet bastante buena debe seguir siendo capaz de ejecutar un nodo completo en casa. Los frikis como nosotros que tenemos ordenadores personales bastante buenos y conexiones a internet bastante buenas podemos seguir participando como nodo completo. No sé. Si hubiera una oleada de "no, tenemos que escalarlo mucho más rápido que eso", bueno, en realidad preferiría eso. No veo que se pueda conseguir el consenso de que hay que alquilar un servidor para participar como nodo completo.

Cory: Estoy de acuerdo en su mayor parte. Creo que en el futuro inmediato cualquier usuario potente debería poder ejecutar un nodo completo. Puede que no le haga ningún bien a la red.

Gavin: Hay gente que se queja de no poder ejecutar un nodo completo en su Raspberry Pi. Bueno, vale. ¿Por qué querrías hacerlo? ¿Y qué bien le haría a alguien?

Cory: Si llega un punto en el que una persona con un ancho de banda y una potencia razonables ya no pueda ejecutar un nodo completo, creo que es algo que debería estudiarse. Creo que eso sucederá de forma orgánica, y no veo mucha necesidad de preocuparse por los requisitos a medida que crezcan.

P: ¿Tiene alguna idea sobre la centralización de la minería? ¿Existe un futuro en el que el ciudadano de a pie pueda crear un minero? Sé que mencionaste la prueba de participación en tu otra presentación y que no era una buena forma de asegurar la cadena de bloques. ¿Existe una versión híbrida que pueda ser viable?

Gavin: Um. Um. Esa es una charla totalmente diferente. Como ordenar mis pensamientos.. Voy a empezar por decir algo que he dicho durante mucho tiempo que nadie cree. Creo que la centralización minera fluirá y refluirá. Como acabamos de ver. Enorme concentración de poder minero en manos de un pequeño número de personas. Creo que leí en reddit que hay un grupo trabajando en computación de alta temperatura donde puedes correr tus chips a 250 grados Celsius que es suficiente para hervir agua. Si puedes hervir agua y crear Bitcoin al mismo tiempo, eso se vuelve realmente interesante y acciona turbinas y calor de vapor y así sucesivamente. Eso podría ser una gran fuerza descentralizadora porque no quieres todo ese calor en una fábrica en China. Así que puedes imaginar un futuro en el que los edificios de apartamentos de todo el mundo minen Bitcoin y se calienten a sí mismos básicamente de forma gratuita. He tuiteado que quiero una manta eléctrica de minería Bitcoin para mantenerme caliente por la noche. produciendo calor, por qué no producir algo de Bitcoin al mismo tiempo. Creo que es difícil para la gente pensar en esto, cuando ven que el 40% de la potencia minera pertenece a GHash.io o lo que sea. Creo que esas fuerzas de descentralización acabarán imponiéndose. Creo que hay otras fuerzas que descentralizarán la minería. El hecho de que las transacciones se creen en todo el mundo, es un fenómeno global, justo eso, el acceso temprano a las transacciones en bloques podría ser un factor descentralizador para que no tengamos un país o un hemisferio que monopolice la minería.

Gavin: Otra cosa en la que he estado pensando recientemente es que estamos sobreprotegidos con la minería. Creo que hay un futuro posible. La minería tiene dos razones. Una es la introducción inicial de monedas, es una forma justa de distribuir Bitcoin. Haz algo de trabajo en forma de minería, obtén monedas. Mi problema fundamental con los proof of stake es que no tienen una solución para introducir monedas de forma justa. Las premian y las venden, y luego se escudan en los problemas de la SEC. ¿Por qué tienes que decidir quién recibe tus monedas? También hay todo tipo de razones legales. Así que la distribución inicial de las monedas es importante. ¿Se puede hacer una prueba de trabajo para distribuir, y luego utilizar la prueba de participación? Probablemente sí. Podrías usar algo más para asegurar. Tal vez la prueba de participación tendría sentido porque entonces tienes esa prueba de anclaje de trabajo. Aunque... hay todo tipo de problemas teóricos, ya sabes, si se convierte en costless para reescribir la blockchain, o muy bajo costo, entonces te encuentras con problemas. Pero si lo que quieres es proteger contra el doble gasto, probablemente haya formas de proteger contra el doble gasto sin descentralización. Tal vez no tengamos minería, pero tendremos una cadena de bloques segura contra el doble gasto. Creo que pronto escribiré un artículo sobre los ataques del 51% y que deberíamos ser más específicos cuando hablamos de ataques del 51%. Hay seguridad contra el doble gasto, y luego seguridad contra la censura de bloques. Eso es más o menos lo que puedes hacer en un ataque del 51%... puedes duplicar el gasto o puedes impedir que aparezcan determinadas transacciones. La seguridad contra el doble gasto, no necesitamos una gran cantidad de minería para eso, la seguridad contra la censura probablemente necesite una gran cantidad de minería potencial al margen lista para actuar si alguien está tratando de censurar bloques. Espero que no haya sido demasiado largo.

P: Hay una especie de batalla entre cómo se distribuyen las monedas. Hay algunos acérrimos que defienden el almacenamiento en frío, mi clave, nadie debería tocarla nunca, y luego están los servicios que guardan claves privadas, y luego está multisig, que es una especie de híbrido intermedio. ¿Cree que estos tres modelos tienen su lugar? ¿Alguno es realmente malo?

R: Todo depende de la conveniencia de la seguridad. Creo que alguna empresa descubrirá cuál es el punto óptimo. Creo que las empresas tendrán un modelo de seguridad de sus monedas muy diferente al de los particulares. No creo que sea una cosa o la otra. Creo que será todo lo anterior.

Cory: Creo que las prácticas y los modelos evolucionarán. Diferentes empresas y diferentes casos de uso utilizarán el más seguro con la usabilidad del mundo real. Desde el punto de vista técnico no importa, lo más perfecto será lo más utilizable.

Gavin: Creo que llegaremos a un punto en el que tendremos un monedero multisig con millones de dólares y alguien en la nube firmará las transacciones. Tal vez si tienes mil millones de dólares en BTC deberías usar cámaras frigoríficas en Suiza o en algún otro lugar donde te preocupe que una guerra nuclear acabe con tu BTC, creo que la tendencia será aumentar la seguridad y la cantidad de dinero que almacenas en un monedero caliente... Yo solía decirle a la gente que no guardara en su monedero caliente más de lo que guardaría en su monedero trasero. Creo que esto aumentará a medida que mejoremos la seguridad.

Creo que estamos asistiendo a la democratización del control bancario del tesoro, tanto si eres una cooperativa que funciona con 100 dólares al mes como si eres un banco que posee un billón de dólares. Eso es genial. Es el mismo costo, o lo será en el futuro. Creo que eso es parte de ella, la democratización de la gestión de tesorería que es genial.

Andy (Armería): Tengo una pregunta acerca de la inevitabilidad de un hard fork, o ¿cuáles son los beneficios y riesgos de eso?

Gavin: Creo que necesitamos un hard fork para aumentar el tamaño del bloque. Actualmente tenemos un tamaño de bloque de un megabyte. Si tomamos el tamaño de una transacción media de BTC, el resultado es de menos de 3 transacciones por segundo, lo cual es patético para una red de pagos. La gente tiene todo tipo de ideas con respecto a no aumentar el tamaño del bloque, y hacer alguna otra cosa compleja para aumentar las transacciones. El ingeniero que hay en mí dice que hay que hacer lo más sencillo posible a menos que haya una razón de peso para no hacerlo. Aumentar el tamaño de bloque es muy sencillo conceptualmente. Hice algunas pruebas de bloques mucho más grandes con nuestro código actual, nuestro código actual puede manejar bloques más grandes sin problemas. He estado pensando en bloques de 1 gigabyte, ¿podríamos teóricamente manejar eso en el futuro? Creo que hay un camino claro para llegar desde aquí hasta allí. Hay algunos argumentos económicos sobre, creo que la mayoría de los argumentos, mos tof the problems that people have with economics of increasing the block size. Están buscando un tamaño de bloque infinito, sin límite. Creo que todo iría bien, pero no voy a proponer eso. Creo que hay buenas razones para no proponer tamaños de bloque infinitos. Los bloques deberían ser lo suficientemente pequeños como para que la gente con conexiones razonablemente rápidas y máquinas razonables en casa pudiera participar en nodos completos y luego ir creciendo con el tiempo a medida que la tecnología escala. Creo que el único argumento racional que tiene algo de sentido es la preocupación de que aumente la centralización de la minería. Bloques más grandes pueden hacer que los mineros aumenten los costes y quizá eso signifique que participen menos mineros. Me gustaría que alguien lo explicara mejor para entenderlo mejor. Ya hemos experimentado la centralización de la minería, y no entiendo cómo bloques más grandes podrían facilitarla aún más. Así que necesitas encontrar a alguien que argumente lo contrario. Así que si puedo conseguir suficiente consenso para que se produzca un hard fork, ya veremos. Voy a pedir ayuda a la gente. Así que si tienes un negocio que crees que necesita más de 3 transacciones por segundo en la cadena de bloques, habla, empieza a presionar, dinos que necesitamos escalar. Creo que cometeríamos un gran error en este momento si no hiciéramos todo lo posible para allanar el camino hacia la adopción generalizada. Creo que existe el riesgo de que, de lo contrario, Bitcoin sea superado o aplastado por gobiernos a los que no les guste. Sólo hay un millón de personas en EE.UU. a las que les gusta, intentaremos aplastarlo porque está bien hacer infelices a un millón de personas. Tendríamos una posición mucho mejor si 100 millones de personas hubieran utilizado Bitcoin en Estados Unidos y les hubiera gustado. Es difícil para un gobierno aplastar algo que es ampliamente utilizado y popular. Creo que debemos hacer todo lo posible para que lo utilice el mayor número de personas. Tenemos que hacer que las transacciones sean lo menos costosas posible. Deberíamos hacer todo lo posible para que las empresas tengan éxito para quienes intentan utilizar la blockchain para cosas interesantes.

P: Antes podías minar con tu propia CPU. Ahora no se puede minar con nada que no sea un ASIC. Parte de todo el blockchain es que la gente está minando nodos, y la recompensa es cada vez menor, pero se está gastando más potencia de cálculo para mantener el blockchain, y se está hablando de bloques más grandes, ¿y se necesitará más velocidad de procesamiento? ¿O no? Una más, y seguimos hablando de Bitcoin como la moneda... si empezamos a construir estos otros negocios en el protocolo, como la prueba de contratos, identidad, bienes raíces, infraestructura increíble sobre todo construido en este blockchain, es que, ¿hay paralelo a las personas que mantienen el nodo, la solución de estos bloques si se están construyendo estructuras en la parte superior de la misma? ¿No tendrás CEX o uno o dos manteniendo el blockchain porque nadie querrá freír su ordenador con ello?

Gavin: Así que la prueba real de trabajo es en realidad independiente del número de transacciones en el bloque. Así que los mineros tratan de encontrar un hash de una cabecera de bloque de 80 bytes. Así que no importa cuántas transacciones haya, todas se combinan por la raíz merkle que está en la cabecera del bloque. El tamaño del bloque es independiente de la migración ASIC/GPU. Es realmente irrelevante. Armar un bloque, vigilar la red en busca de transacciones y decidir qué transacciones poner en el bloque, eso se puede hacer en la Raspberry Pi ahora mismo, ese es el nivel de potencia de CPU que se necesita para hacerlo. Propongo que lo ampliemos para que necesites un ordenador doméstico razonable para poder hacerlo. No creo que sea un requisito irrazonable para los mineros. Creo que los mineros deberían comprar un nuevo ordenador Dell cada uno o dos años para conectarlo a su red y procesar bloques. Creo que es un gasto perfectamente razonable. Creo que escalar al volumen de transacciones de Visa requeriría un volumen de transacciones, pero si escalamos a eso en 10 o 15 años cuando nuestros ordenadores personales sean pequeños centros de datos que puedan manejar ese volumen de transacciones, claro. ¿Tiene sentido?

P: En algún momento, la mayoría de la gente va a abandonar la minería... en 6 o 7 años...

Gavin: Creo que algunos dirán que eso ya ha ocurrido. Creo que veremos regresar a poca gente. Puede que me equivoque. No puedo predecir el futuro. Me molesta que la gente relacione el tamaño de los bloques con la minería, porque no veo la relación entre bloques y minería.

P: Este fin de semana he hablado con un gran minero. Los mineros se están viendo muy afectados por los precios. Han invertido demasiado en equipos y todo eso. Estaba pensando en crear una coalición minera para imponer tarifas por transacción. La mayor parte de sus ingresos han sido las recompensas de Coinbase. ¿Crees que una tasa del 1% podría tener un impacto serio en la adopción o el éxito de la red si los mineros empiezan a exigir tasas de transacción?

Gavin: No he oído que los mineros hagan eso.

Murck: Creo que una coalición no suele ser algo bueno. La idea de la descentralización es que no deberías tener eso.

Cory: Esas cosas van y vienen. Es una progresión lógica. ¿Qué pasa si acabas teniendo dos coaliciones que compiten por sus tarifas?

Gavin: ¿Bloque pequeño tarifa baja, bloque grande tarifa alta? Creo que la competencia hará que las tarifas de las transacciones acaben donde acaben. Creo que será interesante ver si pueden formar una coalición para producir bloques pequeños con transacciones de tarifa alta. Eso me parecerá bien. Bitcoin es un experimento. Es un mercado libre de comisiones. El año pasado trabajé en tasas de transacción flotantes para que no tengamos tasas hardcoded, esto será en 0.10 así que será interesante ver qué pasa con las tasas de transacción medias. Si hay una coalición de mineros que deciden aceptar sólo transacciones con tasas altas, deberíamos ver que las tasas de transacción suben de media. No sé lo que ocurrirá.

Murck: Habría un fuerte incentivo para abandonar e ir al 0,99% y tomar todas las transacciones jugosas que están justo debajo. Sería muy tentador, a medida que la economía cambia, ver cómo esa coalición se mantendría unida. Sí, sin duda.

P: Una vez acuñadas todas las monedas, ¿habrá comisiones?

Gavin: No. Nada. Un posible futuro es que todas las transacciones sean gratuitas y la minería se pague de alguna otra forma... como BitPay y Circle quieren poner en marcha granjas de minería para que sus transacciones se realicen, puede que no pongan tasas en sus transacciones, no hay nada en el protocolo que obligue a una tasa de transacción concreta en ningún momento.

Murck: Hay una especie de suposición. Si las transacciones no están subvencionadas por la recompensa por bloque, si no hay una externalidad como la que has descrito, entonces lo lógico sería cobrar tasas por la capacidad de procesamiento. Creo que eso es lo que la gente predice. A medida que la recompensa por bloque disminuye, algo tiene que hacerse cargo de ella, ya sean tarifas ocultas, que es lo que Gavin ha mencionado, si la gente decide hacerlo por alguna otra razón, o tarifas visibles, o cobrando por las transacciones que pasan por la red.

P: Tengo una pregunta sencilla. ¿Cómo describirías el sistema Bitcoin a un niño de cinco años?

Gavin: No es una pregunta sencilla.

P: Usted conoce Bitcoin a fondo. La gente intenta explicar Bitcoin con diferentes historias. ¿Cuál es la mejor historia para explicarlo?

Gavin: Pedir a los geeks que expliquen las cosas con claridad, probablemente sea un error. Pregúntele a una persona de marketing.

Murck: Eso sería un buen concurso con una recompensa. Encontrar a un niño de cinco años, y una vez que lo entienda, pagar la recompensa.

Gavin: Creo que los niños de cinco años aún no entienden el dinero.

P: Vale, de 10 años.

Gavin: Tal vez. Eh.

Cory: No entender de dinero casi ayuda en cierto modo. La gente siempre se queda atrapada en las cosas que conoce. La gente tiene un concepto muy confuso de la minería. Así que cuando tratas de explicar Bitcoin, llegas a la mitad de un discurso que crees que es una buena explicación, y luego saltan con "¿Qué pasa con los mineros? ¿Qué hacen?" Y eso es importante, pero la minería es casi un tema diferente por sí mismo. Es casi una distracción de una explicación de lo que es la cosa a un nivel básico. Me ha resultado difícil explicárselo a algunos que tienen conocimientos básicos, porque los conocimientos preconcebidos tienden a acercarse a cómo funciona una parte, pero no a toda la explicación.

Murck: Así que durante un tiempo, yo estaba explicando Bitcoin a los reguladores y responsables políticos que es algo así como explicar a un niño de 10 años. En lugar de tratar de convencer a la gente acerca de las raíces de Merkle, nadie entiende eso. Gavin puede, yo no. Tampoco entiendo muy bien cómo funcionan las transacciones SWIFT, o cómo funciona la red ACH o la red SEPA o lo que sea. Cada vez que empiezas a hablar de cómo se mueve el dinero por el mundo. No sé si alguien ha escrito ya ese libro. Intenta conocer a gente con eso. Si hablas con un niño de 10 años, intenta hablarle de comprar un juguete alrededor del mundo. O a una abuela sobre pasar una escritura a sus nietos, aquí hay una forma genial de hacerlo ahora en el ordenador. Descríbeles algo útil. El otro mejor recurso que hay, sinceramente, y esto no es sólo porque esté Andreas, los dos primeros capítulos son excelentes descripciones accesibles.

¿Una última? Una o dos muy rápidas.

P: Pregunta en dos partes. Con las bifurcaciones duras, ¿sientes alguna, ...

Gavin: La razón por la que estoy impulsando la bifurcación dura ahora es que tiene que ser programada. Dentro de seis meses o un año, podríamos llegar al límite de bloques de 1 megabyte si tenemos otra burbuja de subida. No me preocupa que sea más difícil en el futuro. Creo que puede ser más fácil en el futuro si tenemos un buen proceso de estándares. Pasar un hard fork por algún proceso estándar. Sería más fácil que discutir en bitcoin-dev sin parar. Creo que puede ser más fácil de hacer en el futuro. Quiero hacerlo ahora sólo porque estoy preocupado por otra burbuja y un límite duro de volumen de transacciones.

P: Hace unos minutos hablábamos de la estructura de tarifas. Creo que, obviamente, la tasa y la priorización de las transacciones son necesarias para evitar el "penny flooding", pero en términos de hacer de esta una tecnología amigable para los usuarios, es confuso para ellos tener que pagar una tasa. Me preguntaba si va a haber algo en bitcoin 0.10 para hacer frente a eso, o cualquier protocolo. ¿O quizás BIP 70?

Gavin: Creo que los comerciantes quieren eso. Creo que sería una extensión trivial del protocolo de pago. Quizá en la versión 0.11.

P: ¿Un protocolo de pago en torno a eso?

Gavin: El problema de que el niño pague por el padre es que necesitas que ambas transacciones se envíen al mismo tiempo. Si envías una transacción gratuita que no se retransmite a través de la red, necesitas que ambas se envíen al mismo tiempo, y para empezar, más te valdría utilizar el protocolo de pago.

P: ¿Y coinjoin para la privacidad?

Gavin: Exacto, hay todo tipo de razones.

Gracias por su participación.

---
title: Drivechain
speakers:
  - Paul Sztorc
date: 2019-05-27
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - sidechains
media: https://www.youtube.com/watch?v=BH-qZhEZSrg
---
Drivechain: Una capa de interoperabilidad-2, descrita en términos de la red lightning - algo que ya entiendes

<https://twitter.com/kanzure/status/1133202672570519552>

# Sobre mí

Bien, aquí hay algunas cosas sobre mí. He sido un bitcoiner desde 2012. He publicado investigaciones sobre bitcoin en el blog truthcoin.info. He presentado en Scaling Bitcoin 1, 2, 3, 4, tabconf, y Building on Bitcoin. Mi formación es en economía y estadística. Trabajé en el Departamento de Economía de Yale como estadístico durante 2,5 años. Mi jefe de entonces ganó un premio Nobel a principios de este año.

# Tema: Drivechain

Intento llamar a esta capa 1.5 en lugar de la capa 2. Se cuela entre la red de lightning y la capa 1. Puedes tener la red lightning encima de esto. Porque cada pieza de software que es una cadena lateral va a ser la capa 1 de su propia cadena de bloques. Así que esto encaja en el medio.

El objetivo de drivechain es proporcionar interoperabilidad, principalmente. Se puede desplegar por soft-fork. Muy lentamente se le está asignando un número de bip... BIP300 y BIP301. El sitio web del proyecto es drivechain.info. Si eres técnico, los BIPs son realmente buenos ahora. Son bonitos, cortos y claros. Tienes que encontrarlos por su pull request porque sólo al 301 se le ha asignado un número y Luke-Jr dijo que llegaría a asignar el 300 en algún momento cuando se ponga a ello. Tengo enlaces en drivechain.info para encontrar los pull requests.

# En una diapositiva

Esta es la idea en una diapositiva. El problema es el metaconsenso. El consenso sería conseguir que todos los nodos se vean de la misma manera. Ya sabemos cómo hacer eso, Satoshi lo descubrió. El metaconsenso consiste en que los humanos se pongan de acuerdo sobre lo que esos nodos deben acordar. Es un consenso sobre el consenso. Un buen ejemplo es el debate sobre el tamaño de los bloques. Sea cual sea el tamaño de los bloques, al menos en teoría se puede conseguir que todos los nodos se pongan de acuerdo en el historial de bloques dados esos parámetros. Pero no estamos seguros de qué hacer con el hecho de que diferentes personas tengan diferentes ideas sobre lo que los nodos podrían hacer. Cada cambio hipotético en bitcoin también, incluyendo los scripts de turing-completo o mimblewimble, son todas cosas que podríamos hacer que bitcoin hiciera pero no estamos seguros de si deberíamos. Sabemos cómo hacer que los nodos se pongan de acuerdo, pero no estamos seguros de cómo hacer que los humanos se pongan de acuerdo.

La solución es tener un token que viaje entre muchas blockchains. Hay 21 millones de BTC. Pero hay muchos programas que las monedas podrían utilizar. Esta idea solía llamarse sidechains, pero desafortunadamente esa palabra no tiene tanto significado porque la palabra se usa para describir cosas que ni siquiera son blockchain. Originalmente se usaba para cosas específicas de blockchain. Pero me preocupa que en este momento cause confusión.

La razón por la que esto es importante es porque... ¿por qué competir para ganar? Cuando puedes simplemente jugar todas las manos. Puedes hacer todo a la vez. Entonces definitivamente no puedes perder. Entonces no puedes perder incluso si alguien tiene alguna idea tonta; no importa, estás haciendo todas las cosas.

# Interoperabilidad

La interoperabilidad es algo fácil de entender, pero aquí hay algunas diapositivas sobre ella. Es el trabajo en equipo más las diferencias. El equipo va a estar de acuerdo en el número mínimo de cosas en las que tienen que estar de acuerdo, pero luego van a estar en desacuerdo sobre otras cosas. En drivechain, todos van a estar de acuerdo sobre el límite de 21 millones de monedas y todos van a estar de acuerdo en qué pieza de software están esas monedas.

Tuve esta idea aquí, esta es una representación de eso. Este es un límite de 21 millones de monedas aquí, y algunos que no son minados por lo que son 16 millones flotando alrededor. En un mundo con drivechain, probablemente la mayoría de ellas estarían en Bitcoin. Pero algunos de ellos probablemente estarán en algunos otros sistemas divertidos como mimblewimble o firmas de anillo o sistemas que utilizan otras cosas. Podrían ser algunas ideas realmente tontas también, y tal vez alguien pone 50 BTC en él. Es sólo la idea de interoperabilidad.

# Cómo funciona drivechain

Voy a llegar a cómo funciona drivechain. Este soft-fork permite un nuevo tipo de salida, que yo llamo "hashrate escrow". Cualquiera puede poner bitcoin en ella, pero el dinero sólo puede sacarse de ella en un proceso deliberadamente lento y cerrado por los mineros. Esto es más una maldición que una bendición para los mineros. Sólo pueden extraer dinero de forma lenta y transparente. Así que en lugar de enviar dinero a una persona, lo envían a través de este proceso. Los escrows son una prisión en la que se recompensa a los mineros; puedes elegir entrar en cualquier momento, pero es difícil salir. Es una metáfora de la prisión.

Esto es difícil de explicar. Después de meses de intentarlo, voy directamente a un ejemplo.

# Ejemplo: Una cadena lateral de pagos similar a la del lightning.

Digamos que empiezas con bitcoin. Este es el aspecto del software. Luego agregas, esto es con bip300 y bip301. Luego lo agregas... el tipo que más trabaja en esto es... le gusta mucho Qt. Así que hizo todos estos temas, tiene este tema Qt oscuro. Añade una pestaña en la parte superior de la interfaz gráfica de Bitcoin Core.

Entonces tienes el problema del metaconsenso... donde Roger Ver se queja de las tarifas de las transacciones, y supongamos que quiere que las cosas funcionen de forma diferente a como funcionan. Si Roger ejecuta Bitcoin Core entonces tiene que estar de acuerdo con los otros nodos de Bitcoin Core. Si no le gusta Bitcoin entonces tiene que usar alguna otra cosa que es el problema.

Así que Roger va a buscar miembros de la comunidad con ideas afines, para crear un nuevo blockchain usando una plantilla de drivechain. Esto es Bitcoin Core con bip300 y bip301. Luego hay una plantilla sidechain fork de Bitcoin Core también. Así que cada sidechain tiene una nueva pieza de software y en ese software puedes hacer lo que quieras. Hay dos piezas de software que tienes que pensar - Bitcoin Core y bitcoin después de este soft-fork, y el número dos lo que está sucediendo en el software sidechain que se puede hacer lo que quieras que es el punto entero.

Roger y sus amigos van a bifurcar esto y a cambiarle el nombre. Antes se llamaba "testchain", pero van a llamarlo "Bitcoin Payments". Así que pueden cambiar los límites de sigop, el tamaño de los bloques, lo que sea. Este software es como la capa 2, u otras cosas, donde para que este software funcione realmente necesita un nodo de Bitcoin Core. Todas las cadenas laterales necesitan a todos los nodos por debajo de ellas, por así decirlo. Esto es como la capa 1.5. Este software va a necesitar tener Bitcoin Core funcionando en segundo plano de la misma manera que lo hace un nodo de la red lightning.

Roger y sus amigos van a necesitar entonces añadir un nuevo hashrate escrow, una nueva prisión, en Bitcoin. Entonces necesitan atar los pagos a su sidechain. Esto es lo que sucede si abres esa pestaña en la GUI. Una de las cosas en esa pestaña es un pequeño menú para añadir nuevos depósitos o nuevas prisiones, por así decirlo. Así que puedes ver que hay algunos campos aquí. No hay manera de saber si la persona está haciendo esto de manera inteligente o correcta, pero sin embargo se recomiendan. Esta es su oportunidad de atar la prisión a una pieza de software, así que añadimos esos campos.

Así que de todos modos, sólo repasando los detalles, y suponiendo que hace clic en este botón y hace todas estas cosas correctamente. Usted tiene este nuevo fideicomiso abierto. Roger depositará una gran cantidad de BTC dentro. En la capa 1, aparece aquí. Puedes ver lo que sucede en la capa 1 y lo que sólo sucede en la capa 1.5. Pero de todos modos, lo primero que sucede es que Roger pone un montón de dinero allí. Para divertirme, decidí que Brian Armstrong pusiera también algo de dinero en la plica. En la capa 1, parece que 1 UTXO está acumulando muchos BTC. Si quieres que el número baje, activas una rama de código completamente diferente.

P: ¿Qué tiene de especial la salida del depósito?

R: Se identifica cuando se crea esta cadena lateral. Se crea explícitamente.

P: ¿Qué tiene de diferente con respecto a... alguien que sólo mira la blockchain? ¿Cómo se puede saber?

R: El objetivo es poder saberlo. Así que si ejecutas el software, entonces te los enumerará. Hay un tipo de script diferente. No estoy exactamente seguro, ya que lo hemos cambiado varias veces. Sin embargo, no estoy seguro de que eso sea relevante. Sería interesante si pudiera abrir... la salida en sí está cambiando todo el tiempo, pero mantenemos un registro de la más reciente. Se convierte en otra cosa cuando alguien deposita monedas en el depósito de nuevo. El software lleva la cuenta de qué "hilo" es el más reciente de la plica. No estoy seguro de si eso responde a tu pregunta o no. Se identifica explícitamente al principio.

P: ¿Qué aspecto tiene el script? Si estoy en el código y quiero componer un script que actualice el balance de la cadena lateral.

R: Ah, esto es una diferencia entre cómo funciona esto y cómo funcionan todos los soft-fork anteriores en bitcoin. La mayoría de las veces, las transacciones entran en el intérprete del script y entonces es verdadero o falso y entonces una transacción o bloque es válido o inválido. Pero en drivechain, las transacciones tienen que permanecer. Los retiros tienen que quedarse. Están en un estado ambiguo de ser válidas por un tiempo, y luego por defecto son inválidas, pero podrían llegar a ser válidas durante mucho tiempo, lo cual voy a explicar. No estoy seguro de entender la pregunta. La forma en que esto funciona, no hay sólo una especie de opcode. Eso owuldn't trabajo, porque en última instancia, tiene que mantener un seguimiento de la salida en el tiempo como usted verá. No he explicado esa parte todavía. Esto no es como si OP\_NOP2 se redefiniera como CHECKLOCKTIMEVERIFY o lo que sea. De todos modos, se identifican fácilmente. La primera salida se crea explícitamente. Tienes que hacer esta rosca, o es inválida. Esto es sólo una tonelada de reglas de validez de bloques. No hay tantas reglas de transacción, como reglas de validez de bloque. ¿Tiene sentido? No se trata tanto de transacciones individuales como de este proceso que va a través de diferentes blockchains y entre piezas de software. Estás tratando de mantenerlos sincronizados. No sé, ¿eso ayuda en algo? No sé si eso ayuda.

P: Estás acumulando valor en una salida, y rastreando esa salida.

R: Sí, hasta ahora esto es como un hotel de cucarachas: sólo hay una forma de entrar. Si no lo haces, la transacción no es válida.

P: ¿Cómo se identifica esa salida?

R: Se identifica por la primera salida, se da explícitamente a todos los usuarios.

P: Si estoy escaneando la blockchain y quiero identificar todos los UTXOs en custodia y todas las sidechains, ¿cómo lo haría?

R: Tenemos tablas en la cosa. La interfaz gráfica de usuario la rellenará y hará un seguimiento de cuántos depósitos hay y cuál es el resultado. Siempre lo muestra para usted. Hay un comando RPC para eso, como listsidechainunspentoutputs o algo así. No creo que sea tan importante. Es de importancia crítica, supongo. Es algo tan importante que ya está en la tabla de la GUI.

P: ¿Y si quisiera hacer mi propia GUI?

R: Sólo tendrías que mirar el código de la nuestra y arrancar lo que te guste. No sé la línea exacta de código de la parte superior de mi cabeza.

P: Si no conociera su interfaz gráfica de usuario y estuviera mirando la cadena de bloques, ¿cómo podría saber cuántos existen?

R: Mirarías... hay un mensaje diferente. Hay un mensaje de blockchain para crear uno. Luego hay reglas de validez del bloque para saber si se han creado con éxito o no. Está mucho más claro en el BIP. Los BIPs son muy cortos ahora. Definitivamente recomendaría abrirlos.

Hay como 256 huecos. Entonces la gente se quejaba de que si queríamos más de 256 sidechains, cosa que no creo que ocurra nunca. Pero puedes tener un sidechain en un sidechain. Puedes hacer un soft-fork de una drivechain y tener otra cabecera de 256 bytes y luego tener más.... Me niego a poner bip301 primero porque luke-jr realmente necesita fusionar bip300 primero.

<https://github.com/bitcoin/bips/pulls/642>

Lo desglosé en estos mensajes: proponer nueva plica, ACK propuesta de plica, proponer retiro, ACK retiro (implícito), ejecutar depósito y ejecutar retiro. Aquí están todos los campos que se utilizan en un mensaje. Aquí está exactamente lo que son y cómo se construyen los mensajes. Aquí hay una pequeña cabecera. También hay una cabecera de compromiso y un hash de compromiso. Si los mineros no se preocupan, entonces la propuesta expira. Por defecto, es un pulgar hacia abajo. Esta parte no es automática, es por defecto no aprobada. Todos los demás tienen que ACKarlo, como los bits de la versión bip9. Si consigue el umbral del 95% de pulgares hacia arriba durante un cierto número de bloques, entonces se activa.

Lo único que hay que tener en cuenta es la salida crítica. Lo llamamos CTIP aunque, es la punta de su propia cadena de transacciones. Mantiene un seguimiento de exactamente lo que el - donde este dinero es. Así que cuando se deposita en el hashrate escrow, esto podría ser recalculado por nodos honestos y si no tienen algo que coincida entonces ..... hay una tabla de seguimiento de esto muy específicamente. Probablemente, no sé si esto es útil o no, pero espero que lo sea. Probablemente sería mejor... No recuerdo, donde sea posible, añadimos enlaces al código. No sé dónde está el más cercano por aquí. En cambio, puedo volver a subir.

P: Básicamente, los nodos que se preocupan por lo que ocurre en las cadenas laterales, ¿llevan la cuenta de los OP\_RETURNs que tienen este formato y luego los actualizan cuando cambian?

R: Sí. Estas cosas son nuevas en la transacción de coinbase, o nuevas cosas en la blockchain. Así que todo este material comienza en la capa 1, por supuesto.

El tercer y cuarto mensaje proponen un retiro, pero luego el quinto y el sexto son sobre la ejecución de un depósito y la ejecución de un retiro. Así que todos estos mensajes están definidos en el BIP a nivel de bytes. Pero esto responde a la pregunta, sobre cómo encontrar si las cadenas laterales han sido creadas o no. Entonces se sabrá por estos mensajes si las sidechains fueron agregadas o no. Añadimos la tabla a la GUI porque la gente tenía curiosidad.

Roger pone su dinero, y también lo hace Brian. Sólo hay una salida. Son 32 bytes. No son 32 bytes, son 36 por supuesto. Porque es un txid más la cosa del contador de 4 bytes. Así que son 36 bytes. Pero el punto es que, está siendo rastreado por todos los nodos y saben que este es un hilo especial que pueden dejar que cualquiera gaste dinero en él. La cantidad de dinero que entra en el hilo está subiendo, entonces siempre es válido. Pero si está bajando, entonces es una retirada y tienen que comprobar algunas cosas.

Ahora Roger está yendo por todo el mundo y está regalando bitcoin gratis, haciendo las cosas que hace, está corriendo su cartera y regalando 5 dólares de BTC a todos en la multitud. Él está haciendo su shtick o algo así. Pero a diferencia del Lightning, nada de esto se mostraría en la capa 1. Hay muchas cosas que suceden en la plica, pero no aparecen en la capa 1. Esto es como una fábrica de canales súper agresiva, donde la gente está incorporando a la gente en la capa 1.5 sin que nada suceda en la capa 1. Ellos pueden ser incorporados, y luego hacer pagos de ida y vuelta a cada uno.

Hay algo interesante aquí donde voy a explicar una segunda cosa, que es la minería fusionada ciega. Hay mucho que explicar aquí antes de volver a explicar el drivechain.

# Minería fusionada a ciegas

Hay transacciones dentro del escrow, y generan ingresos por tasas de transacción para los mineros de la capa 1, incluso si no las ven. Así que van a tratar de obtener el 100% de las tasas de transacción generadas en otras piezas de software, incluso si no ven las transacciones. ¿Cómo es eso posible?

El truco es que asumo que entre toda la gente que usa la sidechain, que espero que sea un buen número de personas, todos los que usan la sidechain también tienen que usar la mainchain porque este requisito de la capa 2. Es como lightning, donde no puedes usar lightning sin usar bitcoin. Toda la gente que use la sidechain usará tanto la mainchain como la sidechain. Asumo que los bloques de la sidechain, sus tarifas de transacción... pero hay alguien que resulta poseer una buena cantidad de monedas de la mainchain, y es la misma persona. Así que se confían completamente. Ese es el truco. Van a pagarse a sí mismos las tasas de transacción de la cadena lateral. Van a ensamblar bloques - los nodos de sidechain - ya están ejecutando un nodo de sidechain porque son un usuario de sidechain. Tienen que marcar un botón para hacerlo. Ya están ejecutando un nodo sidechain, y van a actuar como si fueran mineros donde ensamblan bloques y se pagan a sí mismos las tasas de transacción, a pesar de que no tienen hashrate. Lo que van a hacer es sobornar al minero de la capa 1 de la cadena principal. Van a pagar a esos mineros de la mainchain fondos para que pongan la coinbase a una cierta cosita que minará el bloque de la sidechain. Van a ganar BTC en la cadena lateral porque van a minar bloques de la cadena lateral. A medida que recaudan dinero en la sidechain, el dinero va a ellos. Fuera de la prisión, estarán pagando fondos a Jihan Wu o a quien sea que mine la blockchain de bitcoin en estos días.

El resumen es que el acto de encontrar un bloque que se encuentra con la minería de fusión ciega, el acto de encontrar un bloque minado con fusión ciega se reduce y se transforma por completo, simplemente incluyendo una nueva transacción de capa 1. Así que un montón de cosas están sucediendo en el sidechain, y los usuarios sólo están ofertando. Hay algunos bytes importantes aquí, en la coinbase, y todos quieren que su bloque acordado sea el que se encuentre. Se están pagando a sí mismos las tasas de transacción, por lo que quieren que su bloque se encuentre porque la sidechain tiene cierta cantidad de BTC en tasas de transacción y todo el mundo lo quiere para sí mismo. Si el mainchain coinbase incluye un cierto conjunto de bytes, entonces ganarán el BTC que minaron. Así que la misma persona va a decir mira a los mineros, te pagaré alguna cantidad de BTC si pones estos bytes en un determinado campo. La gente también puede pujar por esto. Es un concurso. En lugar de que el minero haga todo el trabajo, ellos no hacen nada y entonces sólo ven cuál es la mejor oferta que obtienen.

Q: Going back to the prison analogy, you have bitcoin being generated by miners on the mainchain, and you also have this escrow here. You have all these people on this sidechain-thing which are trading on top of that escrow and creating blocks.

A: Yes. This is not necessarily the case, but I just assume the stuff in the escrow be its own blockchain. But it could be something really strange, like an exchange but they shouldn't want to do that because it's pointless. It could be something weird. It could be something like Liquid with a paxos-signature thing. Or it could be an R3 Corda-esque thing. It could be anything, people just want to put in money into this process because they think miners will gate it the right way.

P: Pero, simplificando, suponiendo que haya bloques, en algún momento dicen que tienen que incluir esto en la cadena principal e intentan sobornar a los mineros para que lo hagan.

R: Son dos cosas distintas. Drivechain y la minería combinada ciega son dos cosas distintas, por eso lo dividí en dos BIP. La minería fusionada ciega fue algo que se escribió para facilitar a los mineros la minería de las cadenas laterales porque ya no necesitan ejecutar un nodo completo de cadena lateral. En la práctica, me imagino que ejecutarán un nodo sidechain. Así es como ha evolucionado la minería. Tienes todos estos hashers, y tienen sus chips ASIC, y luego simplemente marcan a algún operador de la piscina y el operador de la piscina llama a los disparos. Esto es lo que la gente parece preferir, porque es más especialización. El operador de la piscina minera, simplemente ejecutando algún software adicional es una pequeña cantidad de gastos generales. Es difícil para mí imaginar una cadena lateral o cualquier pieza de software que sea tan gravosa que un minero de bitcoin no quiera ejecutarla, o que el operador del pool no esté interesado en ello.

P: ¿Están tratando de llevar algo desde dentro de la plica, a la mainnet?

R: Sí. Calcularán cuál creen que debe ser el siguiente bloque de la sidechain y cuál debe ser la cabecera de la sidechain. La gente puede escribir sidechains que están horriblemente diseñadas y no tienen cabeceras o bloques, pero no deberías hacer eso. Fork la plantilla, que es un fork de Bitcoin Core. Entonces calculas la cabecera, el hash de la cabecera, y eso es lo que necesitan... más el número de sidechain y otros.

P: ¿Así que sólo es un punto de control?

R: Sí, creo que sí. Es muy parecido a Counterparty. En lugar de incluir todos los mensajes de Counterparty, sólo se incluye uno por bloque que los hace saltar todos juntos.

P: Tengo curiosidad por saber cómo es posible que se decida el siguiente bloque de la sidechain y se incluya en la mainnet. Los mineros están ganando dinero tanto de los fondos en custodia como de la minería del siguiente bloque. ¿Qué impide que dos facciones opuestas dentro de esa sidechain o contrato de depósito en garantía digan que éste es el siguiente bloque y que ambos sean aceptados?

R: Esa es una buena pregunta. Hay reglas. Tanto el bip301 como el bip300 son soft-forks diferentes. El bip301 impone el formato de los mensajes de transacción de Coinbase, y a los mineros de la cadena principal sólo se les permite cegar los minados fusionados... es una cierta parte de los bienes inmuebles en el bloque que está definida, y es un bien inmueble mágico. Se define de una manera determinada. Estos próximos bytes son bytes mágicos y los primeros 37 serían para la cadena lateral 1, los siguientes 37 bytes para la cadena lateral 2, y así sucesivamente. Esos bytes son algo. Entonces la otra pieza del rompecabezas es, para hacerlo sin confianza, es que esta persona emitirá un mensaje en la blockchain y dirá mira si haces esos bytes exactamente como yo digo que deben ser entonces te pagaré alguna cantidad de BTC. Así que de acuerdo con los mineros, si nadie ha enviado un mensaje como este, esta es una transacción que está pagando una alta tasa de transacción de bitcoin por lo que definitivamente incluirán esa y establecerán los bytes en el encabezado a ese valor. Hay algunas otras reglas... como que sólo pueden incluir uno de esos mensajes, de lo contrario pueden recoger las pujas de todos. Hay reglas adicionales, pero afortunadamente son bastante simples. Si lo hacen más de una vez, el bloque no es válido.

P: Así que si alguien encuentra un bloque de bonificación, entonces..

R: Probablemente esa sea una palabra mejor para definirlo. El onus está en el usuario de la sidechain, este tipo, cuando monta el bloque de la sidechain, quiere que sea un bloque válido de la sidechain y tampoco quiere que se reoriente. Está preocupado. El tipo de la mainchain cobra sin importar lo que pase, siempre y cuando ponga los bytes bien. Los bytes pueden establecerse en bloques no válidos en la cadena lateral. La gente que maneja los nodos del sidechain verá esto. El hecho de que se fije esta propiedad especial, es el equivalente a que se cumpla el requisito de dificultad - no significa que el bloque de la sidechain sea válido, sólo que se ha difundido. La gente puede decir que este es el siguiente bloque de la cadena lateral, pero todavía tienen que validar ese bloque de la cadena lateral.

P: ¿Quién da el visto bueno para decir... qué pasa si el pool mina un bloque en el que recibe alguna recompensa adicional? ¿Quién es la autoridad en este caso? ¿Cómo se decide? Hay mucha gente que utiliza esta cadena lateral. ¿Quién es el que propone este bloque y quién es el que ofrece esta recompensa a los mineros?

R: Se difunde por toda la red como cualquier otra transacción. Es un concepto bastante diferente. De hecho, incrementamos el número de versión de la transacción. Se trata de fondos de capa 1, sí.

P: De nuevo, ¿estos mineros están recibiendo su recompensa de bloque normal más algo extra que finalmente se retirará?

R: No. Esa es la distinción, como intentaba decir en el bip300 (drivechain), que va de un lado a otro en la plica. Esto no es lo mismo. Debería haber una imagen con una flecha como esta, de hecho hice eso y me pregunté por qué necesitaba eso. Tendrías un gancho rojo dentro de una plica, y luego otro fuera donde son dos cosas fuera y están vinculadas porque son controladas por la misma persona (confianza infinita). Están emitiendo mensajes, y cada uno está pagando una tasa de transacción.

P: Los mineros de la mainnet son los que montan los bloques en la sidechain. Así que están enrutando el mensaje de coinbase a ellos mismos. Así que están ganando dinero en ambos lados. Fue confuso cuando dijiste que hay pujas.

R: Es la persona que hace la puja. El minero puede ser otra persona. Es la persona que puja. Es necesario que haya al menos dos.

P: Entonces, si el minero fuera un participante de la cadena lateral, no habría puja.

R: Sí. Se supone que esto es como la minería merge normal, que ya es algo que probablemente sólo entienden 40 personas en todo el planeta, más algunos retoques. Con la minería merge normal, los mineros tienen que gestionar un nodo y se les paga en namecoin. Hubo preocupaciones sobre, ¿qué pasa si alguien hace una sidechain extraña que también es muy popular, y no se puede ejecutar fácilmente la sidechain? Este argumento es en realidad inválido, pero sin embargo ayudé a diseñar esto para abordar este argumento, incluso si no tiene sentido. Es algo así. Tienes esta gigantesca blockchain súper popular y se convirtió en obligatoria de facto porque era mucho dinero y la única manera de poder minar era teniendo una gran granja de servidores y eso era sólo 3 mineros. Así que ahora cerramos el bitcoin. El argumento no tiene realmente sentido, por el hecho de que la gente podría... lo que implica es que puedes simplemente cerrar bitcoin pagando lo que fuera el valor de la cadena lateral, a través de alguna otra forma como hacer que el gobierno de los Estados Unidos corte un cheque a los mineros... en ese punto el adversario sería un minero. Había otras cosas que no tenían sentido; si se cerraba la granja de servidores, entonces se podía seguir minando bitcoin antes sin la sidechain. Así que el peor escenario sería que no tuviera ningún efecto. La única razón por la que traigo a colación este confuso párrafo de ensalada de palabras es porque esta persona se ha decantado por las comodidades, que es que no necesita ejecutar la sidechain si no quiere, y que se le puede pagar en BTC de la mainchain inmediatamente.

Creo que el panorama minero moderno es uno en el que un par de personas dirigen pools, y mucha gente tiene poder profesional y especialización. No estoy seguro, creo que los operadores de los pools seguirán dirigiendo los nodos de sidechain en un futuro próximo. Me resulta difícil imaginar un caso de desastre en el que el funcionamiento del hardware sea tan rentable que sientan que deben hacerlo, y a la vez sea tan perjudicial que sientan que dañaría la red. La razón principal por la que encuentro esto imposible de creer es porque los usuarios regulares tienen que ejecutar el nodo completo de forma gratuita, y no son compensados en absoluto. Se trata de un nodo que hay que utilizar en un centro de datos, pero hay toda una red de usuarios que lo utilizan de forma concertada para pagar las tarifas de las transacciones. No sé si me creo nada de eso. Los usuarios no obtienen nada, los mineros al menos obtienen algunas tasas de transacción para compensar el coste. El verdadero problema es que los usuarios no reciben ninguna compensación. Si el nodo es tan difícil de manejar, entonces me imagino que la red colapsaría porque la gente no lo está usando.

Si no manejas un nodo, te será imposible averiguar si los mineros están robando o no cuando retiran dinero. Va a ser imposible averiguar qué está pasando cuando se retira dinero.

P: ¿Cuál es la principal ventaja de esto sobre el lightning?

R: Voy a llegar a eso.

P: Esperemos. Continúe, por favor.

R: Bien, es un voto para continuar.

Hice un pequeño desvío en nuestra historia para hablar de la minería fusionada a ciegas. Intenté hacerlo rápidamente. De todos modos, genera valor para los mineros. Es tanto directo como indirecto.

# Desplazamiento lateral, desplazamiento de forma, intercambios atómicos, etc.

Cuando los laicos quieren liquidar sus monedas de vuelta a la capa 1, dejando el contrato de custodia, van a utilizar Shapeshift o Sideshift, que cobran el 1%, pero se sale de la custodia inmediatamente. Es una especie de intercambio de prisioneros. Dentro del escrow, habrá una transacción en la que Andreas posee algunas monedas en el escrow pero a cambio en la capa 1 va a pagar a algún tipo Jeff. Andreas va a pagar al cliente en la capa 1. Así que tenemos una nueva transacción de capa 1. Podría haber habido 10 trillones de transacciones en la cadena lateral pero hasta ahora la capa 1 sólo ha visto los depósitos y esta diferente que es una transacción de tipo swap atómico. Esto ni siquiera es una transacción de drivechain, es sólo un acuerdo del tipo "oye si el hash se revela". Pero en la práctica, ya que a la gente no parece importarle eso, en el mundo real lo que sucedería es que Andreas tendría un -- la gente le enviaría dinero en el depósito, y sólo se vería como transacciones normales. A la mayoría de los legos no les importa, así que habrá esta confianza fluida, es mucho mejor que el intercambio, por ejemplo. Así que esto plantea la pregunta, ¿cómo saca Andreas su dinero? Aunque haya especialización y un tipo pague a la gente a cambio del 1%. ¿Cómo saca Andreas su dinero? Emitirá un mensaje dentro del software de la cadena lateral diciendo "Quiero sacar estas monedas". Esta es la transacción de retirada. El software agrega todos estos mensajes. Esto es lo que hace la plantilla de sidechain del fork de Bitcoin Core que escribimos. Eres libre de hacer las locuras que quieras, pero creo que esto es lo óptimo. El software va a mirar estas solicitudes de retiro y decir, ¿qué transacción necesitamos para hacer que suceda? Entonces vamos a hacer que suceda. Qué necesitamos, y la transacción será definida por un txid de 32 bytes y estos 32 bytes van a ser muy importantes. Hay un paso... mientras tanto puede haber nuevos depósitos en la plica, que puede estar cambiando htis. Se hace de manera inteligente, para que ciertos bytes se pongan a cero y todavía se puedan hacer depósitos a esto.

Esta es una vista de la plantilla de la cadena lateral dentro de la hipotética cadena lateral de Bitcoin Payments. Este es un comando getblockheader. Los 32 bytes van a estar aquí, en este momento era 0s porque esto es sólo un ejemplo y no hay nada. El punto de esta diapositiva es que los nodos completos de la cadena lateral van a saber cuáles son los 32 bytes, y entonces van a gritar esos bytes en las cabeceras de cada bloque. Vamos a promover estos 32 bytes a una tremenda saliencia. Van a estar en la cabecera durante todo el tiempo que sea necesario, ya sea que la retirada falle o tenga éxito.

En la capa 1, alguien pondrá este mensaje de 32 bytes, propondrá un retiro en un mensaje de coinbase de capa 1. Comienza aquí. Una vez por bloque, puede seguir adelante, quedarse donde está, o retroceder. Tiene 6 meses para hacerlo, o expira. Esto ya es una metáfora extraña en este punto. Si llega hasta el final, entonces la transacción que coincide con este ID puede ser incluida en la capa 1. Si no, no puede. Así que los 32 bytes logran salir, están fuera. Eso significa que puedes incluir esto en la capa 1. Usted todavía tiene uno que tiene todo el dinero restante en el depósito de hashrate. Pero los otros fueron pagados.

P: ¿El mecanismo que ve la capa 1 para saber que son 3 meses es porque todos están bloqueados por tiempo?

R: El bloqueo de tiempo implica que .... puede que no lo implique, pero creo que el campo de tiempo de bloqueo está en la transacción. Pero en este modelo, esto es diferente de... normalmente, una transacción va a un intérprete de scripts y entonces será un pulgar hacia arriba o hacia abajo. Es una línea de ensamblaje y simplemente pasa. Si todas las transacciones pasan por la línea de montaje, entonces son y el bloque es válido. Pero en drivechain, hacemos un bucle de vuelta a través de él cada vez y tiene una puntuación. Se acumula una puntuación. La puntuación puede... las reglas de validez del bloque permiten que la puntuación suba, baje o se quede donde está. Hay un poco más que decir sobre eso, pero no hay mucho tiempo. No sé qué pasaría si tratara de hacer una presentación sobre todas las cosas. Las reglas sólo dicen, hay una especie de nueva base de datos que dice, ¿qué valor se permite tomar esta base de datos? Esta cosa está recibiendo una puntuación, y está subiendo o bajando o permaneciendo igual. Si se pone lo suficientemente alto, entonces la transacción que coincide puede ser incluida en la capa 1. No están bloqueados en el tiempo. Esto no es una transacción en absoluto, son sólo 32 bytes. Es parte de un mensaje especial en una transacción de Coinbase. No tiene nada que ver con el mensaje minero fusionado a ciegas, que es una cosa diferente. Esto es sólo 32 bytes y no es una transacción en absoluto. No hay timelock, no hay nada, son sólo 32 bytes de aspecto aleatorio.

P: ¿El mecanismo que ve la capa 1 para saber que son 3 meses es porque todos están bloqueados por tiempo?

P: Pero el minero que lo incluye, ellos...

R: Lo incluyen una vez.

P: Pero el minero cuando resuelve el bloque cuando aparece, como si fuera 3 meses después, y es aprobado, ¿cómo sabes que no es el mismo minero resolviendo ese bloque?

R: No es necesario. El primer tipo va a incluir un mensaje. Más tarde, hay un mensaje mucho más pequeño a medida que se mueve hacia adelante y hacia atrás, y una vez que está fuera, se puede incluir esta gran transacción en la capa 1 aquí. La forma en que configuro esto en la plantilla de sidechain es que pagas dos tarifas de transacción - pagas una tarifa de transacción a la gente para incluir estos mensajes, pero luego tienen una tarifa de transacción esperando aquí en la capa 1. Cuando la transacción finalmente llega, es sólo una transacción normal de bitcoin como cualquier otra. El único mensaje que puede sacar dinero de aquí son los...

P: Estas transacciones de retirada no están firmadas, ¿verdad?

R: Oh, ese es un buen punto. Creo que están firmadas, pero eso es sólo porque las usamos para hacer un seguimiento... eran sólo de vigilancia y esa era la forma más conveniente de que los nodos las rastrearan. Pero la clave privada que lo firma es conocida públicamente por todos. Así que firma como una ceremonia pero no significa nada. No hay nada más que bloquee este dinero, el dinero está abierto para que todo el mundo lo coja. Cualquiera puede intentar sacar dinero, pero si hace que el número baje, entonces el txid tiene que coincidir con este valor de 32 bytes. Pero no están firmados en ningún sentido real.

P: Así que alguien todavía tiene que publicar una transacción una vez que termine ese tiempo. Así que podría hacerlo después de los 3 meses.

R: Sí. Eventualmente expirará en 6 meses. Si eres muy lento, o es como lo que sea y no llegas a hacerlo. Solo tienes 1 o 2 bloques para entrar, antes de que esto desaparezca. En realidad sólo va a prestar atención al líder en cualquier sidechain. Si usted tiene un montón de gente tratando de hacer esto todos a la vez o después de uno tras otro. Por fideicomiso. Dentro de ellos, puedes mover cualquiera de los 32 bytes, si mueves uno hacia adelante entonces los otros automáticamente se mueven hacia atrás. Puedes hacer lo que quieras, pero sólo puedes tener un campeón moviéndose hacia adelante al final. El objetivo de este proyecto es minimizar la auditoría. No es bueno hacer un hard-fork y que la gente audite a Bitcoin Cash porque eso desvirtúa todo el objetivo. Pero también quieres hacer lo contrario... lo que quieres, es difícil de explicar..... cuando esa transacción se ensambla, debería pagar de más las tasas de transacción de la capa 1 porque es como un Lightning en el que no sabes cuáles van a ser las tasas en el futuro.

P: ¿La transacción de retirada tiene alguna variabilidad, o enmascaramiento, o es sólo una transacción absoluta?

R: Bueno, la salida del depósito cambia, así que hay algunos bytes que se ponen a cero. Es difícil hacer la tasa de transacción, porque la suma también cambia. La tasa de transacción es sólo una salida que los mineros pueden gastar. Hay estructura, excelente pregunta. Hay estructura impuesta en la transacción de retirada. Muchas cosas pueden ir mal, el dinero se lanza al aire, y el software tiene que ser capaz de enviarlo a cualquier parte. Prácticamente cada parte de esto está controlada por cosas raras.

P: ¿Y si hay una reorganización?

R: Excelente pregunta. Reorgs... depende de .... con los reorgs se retrocede en el tiempo. La gente que hizo la reorganización podría volver a avanzar en esos bloques de reorganización, o podrían hacer otra cosa. Por otro lado, ¿qué hacen con los bloques fusionados de la cadena lateral? Podrían mantenerlos igual, en cuyo caso la historia de la cadena lateral sería la misma. O podrían hacerlos diferentes, en cuyo caso se reorganizarían. Pero esto es mucho más seguro de reorgs que una transacción típica. Avanza como en 2-3 meses. Hace que parezca que un pool representativo de hashrate realmente quiere meter esta transacción y cobrar sus honorarios. Depende de lo que haga el diseñador de la reorg. Los reorgers podrían decidir avanzarlo, o no. Tal vez la transacción lo haga, pero entonces se reorgera en algún lugar del pasado. Todas las sidechains en la capa 2, cuando la mainchain la reorgs, la sidechain dirá que este dinero... porque cuando la retirada es a través de, la sidechain borra el dinero porque la sidechain dice que lo retiró en la capa 1 por lo que ahora se elimina. Andreas y Erik dicen que quieren sacar este dinero, y cuando finalmente lo hacen el sidechain dice oh bueno lo hiciste y el ndeletes el dinero y se ha ido. Si se reorganiza, se deshace.

P: ¿Qué pasa con los UTXOs en custodia? ¿No estarán desincronizados?

R: Si la gente está depositando en esto, está cambiando y volverá al estado en el que se ramificó la reorg. Esto está cambiando mucho. Esa parte se pone a cero en la transacción txid de 32 bytes. No es un txid exactamente, es inteligente, no mira los bytes para esta salida de custodia. Esos pueden ser cualquier cosa, los anula con ceros. Pero esto puede cambiar como resultado de un reorg o cualquier tipo de depósito al azar en él. Cualquier cosa que pase, no es nada que no pudiera haber pasado originalmente. Un pago regular en un reorg de 20 bloques, no sabes si tu pago será incluido de nuevo. Pero si lo tuyo ya se hizo 2 de los 3 meses, entonces probablemente se producirá. Es menos riesgo que un pago regular realmente. Los casos en los que la retirada se llevó a cabo, pero la reorganización nos llevó a un mundo en el que no se llevó a cabo, pero esto probablemente no ocurrirá porque en todos los mundos en los que se llevó a cabo hubo un tremendo esfuerzo para que se llevara a cabo.

P: ¿Se trata realmente de una minería fusionada?

R: En realidad no. ¿La terminología de la minería combinada ha tenido alguna vez sentido?

P: No.

R: Elijo nombres terribles para las cosas y la gente se burla constantemente de los nombres. Pensé que escrow era una gran mejora sobre sidechain. Pero, es difícil de decir porque... tú, ¿qué consideras que es Counterparty? ¿Es minería fusionada? Más o menos lo es. Cada mensaje es un nuevo bloque. Counterparty tenía muchos bloques que tenían cada uno una transacción.

P: Counterparty tenía mensajes especiales de bitcoin.

R: Esto también.

P: Pero Counterparty no requería que los mineros de bitcoin o los operadores de pool ejecutaran otro software.

R: ¿Es realmente minería fusionada? Otra diferencia es que con la minería fusionada, podrías minar el bloque sin meterte con el bitcoin en absoluto. En namecoin, podrías hacer hash en un mundo separado. Así que veo que eres una de esas 40 personas. Pero aquí, decidí que no se puede, está vinculado directamente y hacer que sea mucho más como la red relámpago donde es absolutamente necesario que se ejecute y supervisar la capa 1. Esto ayuda con reorgs, de lo contrario sería bastante extraño. Así que con esto, sólo digo que si usted desencadena esto entonces usted está desencadenando toda la actividad sidechain también. Sí. Son ligeramente diferentes. Creo que la terminología puede ser confusa, pero no sé qué hacer al respecto. Lo curioso es que, en general, la terminología en bitcoin es terrible. Todo el material es una locura.

P: ¿Cómo se firman las retiradas?

P: Hay una firma, es de los últimos 5.000 bloques y de la minería.

R: Estoy de acuerdo, así es como lo pienso. Las personas que construyen el libro mayor están en una membresía dinámica. Es lo mismo que la estructura DMMS del libro blanco de Blockstream. Están construyendo lentamente una firma sobre 13.000 bloques. Es como chispear algo en una estatua o losa de mármol. Aparte de esta puerta, no hay ningún otro requisito en estas transacciones de retirada. No hay ninguna transacción que simplemente aparezca en el intérprete del script y luego el intérprete del scrpit le dé el visto bueno. No. Pasa por este proceso de puerta y luego al final obtienes tus monedas.

# Costes y riesgos

Aquí es donde empiezo a compararlo con la red lightning. Con Lightning, no necesariamente tienes que usar Lightning.

P: ¿Qué hace que esta sea la capa 1.5 y lightning sea la capa 2?

R: Puedes tener una cadena lateral que tenga su propia red lightning y que sea interoperable.

P: ¿Pero se puede tener un sidechain en el propio lightning?

R: No creo que se pueda. Lightning es todo lo que podría ser arrastrado a la capa inferior en cualquier momento.

P: Es lo mismo que con una drivechain, es un montón de cosas que podrían ser arrastradas a la capa 1 en cualquier momento.

R: Sólo a través de Shapeshift o Sideshift. Así que creo que no. Lo que estoy imaginando es que tienes la capa 1, tienes el Lightning a través, y cualquiera de ellos puede ser arrastrado a su blockchain. Siento que se cuela. Lightning ya tomó la capa 2, fueron maleducados sobre la existencia de capas entre ellos y la capa 1, y no había más espacio, así que así es como colonizo la capa 1.5.

Hay una nueva consideración de seguridad. Esta es una diapositiva que usé en Consensus. Era para gente mucho más tonta. Para la red de relámpagos, necesitas ser capaz de notar el fraude a tiempo, necesitas hacer una transmisión de emergencia a la capa 1 si alguien te está defraudando, y también necesitas no ser una carga demasiado pesada si te ausentas por el periodo de custodia. Necesitas estar en línea. Eso es diferente. Depende del caso de uso. Para muchos casos de uso, eso no importará, pero para otros, estas cuestiones sí importarán.

Para los contratos de escrow de hashrate, lo que realmente quieres saber es, ¿cuánto dinero es... cómo están invertidos los mineros en todo este esquema? Quieres que los escrows sean realmente populares. Eso es realmente lo que quieres. No es tan diferente filosóficamente de cuando se utiliza cualquier otra pieza de software seguro, usted quiere un montón de ojos en él y cosas por el estilo.

En lightning y sideshift, las tarifas se basan en el porcentaje. Y también tienes al menos 3 tasas de capa 1. En Lightning, no se puede incorporar a los usuarios sin la capa 1. En lightning, tienes que estar en línea y tienes que tener tu clave privada alrededor, así que es como una cartera caliente y eso es bastante molesto. En el futuro estoy seguro de que será mejor pero por ahora no es genial. Lightning es mejor porque se liquida inmediatamente, especialmente si el comprador y el vendedor están en línea, como si quieres entrar en una tienda y comprar algo. Lightning no es inmune a los ataques de griefing o routing. ¿No es el problema de la opción libre en los swaps atómicos?

Tadge Dryja se hizo temporalmente famoso en twitter porque dijo que lightning no es útil para los micropagos porque cuando se enruta a través de los contratos de hashlock, expande la transacción en 40 bytes y la tarifa tendría que expandirse en mucho más que eso y no funcionará para micropagos súper diminutos. Todavía funcionaría en los canales, es mi entendimiento, no veo por qué no lo haría. Así que eso es ligeramente diferente.

# Robo de mineros

Ya he explicado lo que ocurre cuando todo va mal: digamos que Jihan Wu va a robar todo el dinero de Roger. Él imagina, ¿qué transacción necesito para robar el dinero? Calcula los "malvados 32 bytes", y lo pasa por las puertas, y durante 3 meses los nodos de la sidechain van a flipar y decir que esto no coincide. Debido a la existencia de twitter, todos los demás también lo sabrán. Todos los que usen la cadena lateral lo sabrán inmediatamente. Otras personas que usen una sidechain diferente se interesarán por esto porque pensarán "oh, tal vez yo seré el siguiente" o tal vez serán personas que señalen y se rían de la situación. Se correrá la voz rápidamente. Si lo lleva a cabo, puede realizar esa transacción y luego robar todo el dinero.

La gran arma es el UASF (user activated soft-fork). Pero no quiero confiar en esto porque podrías usar un UASF para asegurarte de que el fraude se lleva a cabo. El UASF se sale del código y se limita a afirmar un consenso. Es un razonamiento circular. No es una regresión infinita completa. El punto de hablar de los 3 meses incómodos es que debería ser obvio, algo deshonesto está sucediendo. Tienes mucho tiempo, cualquiera que dirija la cadena principal. Cualquiera que ejecute la cadena principal verá esta propuesta ahí, y odio usar esta terminología, pero puedes hacer clic con el botón derecho y no dejarás que esa transacción entre en el bloque de la cadena principal nunca. No hay ningún problema de coordinación aquí. Esto es estrictamente superior a varios incidentes anteriores, como situaciones en las que ha habido una coordinación de emergencia. Como el incidente de desbordamiento en 2011, la división de la cadena de marzo de 2013, y luego hubo- Yo diría que el UASF segwit fue un ejemplo de esto, pero mucho más lento. Es probablemente un ejemplo más nbetero porque tomó varios meses. En el primer incidente, se crearon 140 mil millones de bitcoins de la nada. Lo que había que hacer era tener gente inteligente que tenía que averiguar qué hacer, y luego hacer que todo el mundo se actualizara para arreglarlo. Eso ocurrió en pocas horas. Del mismo modo, en marzo de 2013, usted no tenía ninguna advertencia de antemano en absoluto, y se fijó con un montón de trabajo creativo especialista que hizo esta cosa compleja para arreglarlo y luego todo el mundo siguió con el plan para arreglar esta cosa. En todos estos ejemplos anteriores, todas las reglas del código se seguían al pie de la letra -lo cual era el problema porque el código estaba mal- y lo único que hacía que la gente cambiara era su deseo de tener un protocolo más útil. En el caso de la UASF también fue así. No había nada malo en las normas anteriores en ningún sentido técnico, pero la gente quería que fueran diferentes, así que se coordinaron durante meses para conseguir lo que querían.

Si esto se convierte en un esquema popular, entonces lo que los mineros van a hacer cuando roben es que van a destruir sus ingresos por tasas de transacción de ese depósito porque ya no va a pasar nada allí y la gente va a renunciar a ello. Probablemente no podrán recaudar ningún ingreso por tasas de transacción, y esto será el fin del experimento de las sidechains. La forma en que la interoperabilidad debe funcionar creo que es que sólo hay tres posibilidades: o tienes altcoins, que nadie quiere realmente, pero algunas personas piensan que es tolerable... pero podrías hacer que todo sea obligatorio en bitcoin y podrías decir que bitcoin lo hará todo, y entonces este es el toque ligero por así decirlo, pero es la prueba SPV. Se comprueba el trabajo pero no todo lo demás. Probablemente hay algunas otras opciones en el medio. Pero en última instancia, depende de si la gente viene con un nuevo software fresco que hace algo útil. Si todas las altcoin que existen hoy y que existirán en el futuro son inútiles, entonces este proyecto también es inútil e inseguro.

La otra cosa que hay que decir es que sólo son 3 meses si hay un 100% de hashrate. Si hay un 51%, entonces tomará los 6 meses completos nad más tiempo. La otra cosa que se puede hacer es que diferentes mineros pueden moverlo hacia atrás y pueden moverlos todos hacia atrás. Podrían decir que algo sospechoso está sucediendo, y pueden pulsar una alarma. Si tienes el 25% de los mineros diciendo "Mira, no sé lo que está pasando, pero algo loco está pasando" ..... Además ya tenemos esta suposición de que no hay un malvado 51% deshonesto en bitcoin de todos modos.

Bloquear el UASF no cuesta casi nada. No hay necesidad de que este proceso... en esos tres ejemplos anteriores, necesitabas un montón de trabajo creativo de especialistas para sacar esos arreglos. Necesitabas que se hiciera algo complicado. Pero con esto, no necesitas que se haga nada complicado. Y la otra gran diferencia es que los dos primeros ocurrieron sin previo aviso, pero esto se anunciará con al menos 2 meses de antelación para que la gente piense qué quiere hacer al respecto. El gran problema es que no puede ser accidental, y el minero no puede decir "oh tenía algo configurado". Es algo muy lento. Es como el UASF. Es una lectura lenta de lo que quieren los mineros. Si quieren matar a la gallina de los huevos de oro, entonces significa que sería el fin de este experimento y el token sólo podrá hacer lo que puede hacer el bitcoin de capa 1. Sí se puede UASF y hard-fork tal vez cambiar la prueba de trabajo y tratar de continuar. Pero es deseable que sea posible y fácil robar dinero de esta cosa, porque eso es lo que lo hace opcional. De lo contrario, no sería tan útil. Quieres que todo el mundo en la capa 1 sea capaz de ignorar todo esto. Si alguien hace algún sidechain raro, quieres que todos los demás puedan decir mira, .... Creo que tengo algo así en el apéndice. Esto es algo que traté de explicar en Lisboa cuando di una charla. Es básicamente esto, que es .... con otros cambios de protocolo, como, cuando añadimos CLTV o CSV, los NOP cambiaron a cosas reales, esta es otra forma de hacer interoperabilidad porque son soft-forks. Los soft-forks garantizan la interoperabilidad, lo que no ocurre si un nodo rechaza el bloque, pero si un nodo acepta el bloque, en teoría todos los demás nodos deberían aceptarlo. Esto te deja en un estado de confusión porque con el tiempo quizás no te has actualizado al último protocolo pero otras personas sí, y quizás alguien te ha pagado dinero y ha llegado a través de un tipo de transacción que no entiendes... ahora no estás seguro de si realmente has recibido dinero. Parece que te han pagado, pero no lo sabes realmente. Así que estás en un estado de confusión permanente hasta que te actualices. Pero con drivechain es un poco mejor, porque sigue habiendo un concepto de finalidad de la liquidación que es independiente de si son los 32 bytes buenos o malos. Las reglas son las reglas, básicamente. Una vez que se introduce el UASF para todas las maniobras raras, entonces ese péndulo vuelve a oscilar hacia el otro lado.

P: ¿No necesitaría una sola persona para... contar con todos para prohibir esa transacción?

R: Sí.

P: ¿Cree que esto funcionará repetidamente? ¿Se puede contar con esta técnica 10 veces?

R: No quiero contar con ello en absoluto. El UASF es como un extraño razonamiento circular. No es una entrada completa e infinita. Es como ir a un tribunal, donde reúnes todos tus documentos por adelantado, luego los llevas al tribunal organizados y si no lo haces entonces la jueza Judy te gritará que te pierdas o algo así. Así que tienes que hacer todo este trabajo para preparar este ataque por adelantado. La gente puede derribarlo 2 semanas antes, pueden haber estado de vacaciones y el nthey sólo UASF 10 días antes. En el último día, el minero tiene que decidir si quiere incluir esto o no. Los usuarios de la cadena principal no tienen que... tienen mucho tiempo para decidir si quieren hacer algo. Podrían decir, no quiero ejecutar ninguna sidechains porque son estúpidas. Pero digamos que alguien intenta hacer un robo, tal vez un usuario se interesaría de repente porque quiere usar una sidechain en el futuro, así que quiere proteger esto y unirse a la UASF y hacer presión política. Tienes que hacer todo este trabajo por adelantado para poder hacer el ataque, y es trivial hacer clic con el botón derecho del ratón y sacarlo de la UASF. Tengo una charla diferente sobre los mercados de predicción y la organización de los votos y el uso de la pereza para arreglar todo. Esa es mi charla favorita para dar. El nodo sidechain va a ser sharding en modo SPV con todas las cabeceras. Pero una cosa que podrías hacer, una persona maliciosa puede falsificar las cabeceras o podrían... realmente no pueden porque.... no se sabe si las cabeceras son realmente una sidechain válida, así que podrían tener un bloque sidechain inválido que les paga correctamente todos los fondos. Lo que podrías hacer es que si hay una disputa real, tienes 3 meses para resolver esto, así que déjame ejecutar el software de sidechain y conseguirlo. Sólo necesitas 6 meses de historia, digamos, no necesitas toda la historia del sidechain porque puedes dar por sentado que los últimos retiros que pasaron fueron correctos porque no hubo disputas sobre ellos, así que sólo tienes que validar los bloques que pasaron en el sidechain desde entonces.

P: Parece que, en el peor de los casos, todo el mundo en la capa 1 tiene que hacer todo eso de mirar y descargar software.

R: Sí, esa es la paradoja. Pero la gente no tiene por qué hacerlo. De hecho, es bueno que sea posible el robo de fondos. Ese detalle es el que hace que todo sea finalmente ignorable.

P: Ésa es la única forma de escalar, descargar la verificación a los usuarios. En los canales de pago, los usuarios que depositan fondos tienen que verificar todo entre ellos. Casi están creando sus propios bloques. Esta es la única forma de escalar.

P: Al menos eso es algo que están utilizando directamente. Pero los usuarios de la capa 1 no están necesariamente participando en las sidechains.

R: No requiere su propio hashrate, debido a la idea de la minería fusionada ciega. Son una especie de... plugins, o bloques extra. Es un préstamo... por alguna razón la gente se empeña en decir, oh la sidechain puede tener proof-of-stake... la gente hace preguntas, y muchas de ellas son posibles, pero no veo por qué alguien no usaría la plantilla de minería blind merged tal y como está... Hay un montón de posibilidades extrañas, como tener una segunda prueba de trabajo y que se altere o algo así. Pero en última instancia no quieres que la sidechain tenga su propio hashrate porque la sidechain no está acuñando sus propias monedas. La cadena lateral está recibiendo las tasas, así que sí podría ser un mercado de tasas. Pero podrías tener una desagradable correlación en la que tal vez sean las 4 de la mañana EST o algo así y las tasas de transacción caigan a cero temporalmente. Ahora, no hay ningún incentivo para minar el bloque. Así que si tuvieras tu propio hashrate, entonces esto sería incómodo porque tendrías que esperar o algo así y sería extraño y podría llevar al pánico donde la gente dice no quiero usar la sidechain porque qué pasa si mañana a las 4am esto sucede de nuevo y entonces todo el mundo abandonará la sidechain y no habrá usuarios, ni tarifas de transacción ni hashrate. Mientras que en cambio, se podría obtener el 100% del hashrate de bitcoin con la minería fusionada de forma gratuita, y no se pierde ningún supuesto de seguridad. La forma en que esto funciona, si el 51% de los mineros están en contra de ti, ya tienen muchas maneras de bloquear las transacciones o de estropear los retiros. No hay pérdida de seguridad en absoluto, realmente. Los mineros sólo se impiden a sí mismos ganar más dinero. Es esta cosa que es simplemente gratis, el 100% del hashrate de bitcoin realmente gratis, y no veo por qué la gente haría otra cosa. Sigo recibiendo correos electrónicos extraños de personas que quieren cosas como bloques pares e impares y otras cosas locas.

# Resumen

Esto proporciona una nueva fuente de beneficios e ingresos para los mineros. Los mineros pueden elegir entre reclamar los ingresos o destruirlos. También hay una alta auditabilidad: puede reducir todas las transacciones a "transferencias netas". Puedes reducir todas las transferencias a 32 bytes. Una transferencia a la vez, y las transferencias tardan 3 meses en liquidarse.º

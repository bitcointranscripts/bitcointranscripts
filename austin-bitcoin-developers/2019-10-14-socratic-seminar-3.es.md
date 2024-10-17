---
title: Seminario Socrático 3
date: 2019-10-14
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - miniscript
  - taproot
---
Seminario socrático de desarrolladores de Bitcoin de Austin 3

<https://www.meetup.com/Austin-Bitcoin-Developers/events/265295570/>

<https://bitdevs.org/2019-09-16-socratic-seminar-96>

Hemos hecho dos reuniones en este formato. La idea es que en Nueva York hay BitDevs que es una de las reuniones más antiguas. Esto ha estado sucediendo durante cinco años. Tienen un formato llamado socrático donde tienen un tipo talentoso llamado J que los conduce a través de algunos temas y tratan de conseguir un poco de discusión en marcha y tirar de la experiencia en la audiencia. Somos facilitadores, pero no expertos, así que no esperen que lo sepamos todo. Todo el mundo está aquí para aprender. Hagamos una ronda de presentaciones para decir su nombre y cuál es su papel.

# Miniscript

Empecemos con el miniscript. Ni siquiera voy a intentar explicarlo. ¿Andrew? ¿Cuál es el problema que miniscript va a resolver? Miniscript es un esquema para escribir scripts de bitcoin de forma estructurada. El problema con bitcoin script es que... mucha gente no es consciente de que bitcoin tiene un sistema de scripts. Es posible hacer más cosas que asignar monedas a un ke. Puedes tener conjuntos arbitrarios de firmantes, preimágenes de hash que es como funcionan los HTLCs de lightning, y conjuntos arbitrarios de timelocks y puedes combinarlos de la manera que quieras. El sistema de scripts no está realmente diseñado para hacer un razonamiento automatizado.Para llegar a la secuencia de comandos, usted necesita para obtener un experto bitcoin que escribirá el código de propósito especial para la estimación de la tasa y el análisis de seguridad ad hoc de una sola vez para convencerse de que la secuencia de comandos está haciendo lo que usted espera que y no va a hacer cosas que usted no espera que haga.

((cambió a un teclado realmente utilizable))

Si tu usuario quiere hacer todo tipo de cosas raras, apesta ser ellos porque no puedes darles soporte con tu infraestructura porque necesitas saber que el script con el que te estás acercando es el que realmente es un firmante. Sin miniscript, esto es imposible. Sin miniscript, tendrías que escribir la mancha en la parte inferior. La cosa roja en la parte superior es algo genial. Tomas todos los opcodes de la parte inferior y los decodificas en la cosa roja. La cosa de arriba es una lista de condiciones de gasto y cómo se combinan. La cosa de abajo es un montón de opcodes de ejecución de máquina para una máquina de pila que sólo representa incidentalmente condiciones de gasto y opera sobre datos opacos que a veces son enteros a veces firmas y que realmente deberías asegurarte de que son correctos. Esto es normalmente difícil de leer porque es hexadecimal, o incluso en esta representación de opcode es difícil de leer. También se obtiene un beneficio de legibilidad. La gran cosa es que tiene una estructura de condiciones de gasto.

P: ¿Podría combinarse con el PSBT?

R: El PSBT es sencillo en su esencia. Es un formato estandarizado para las transacciones de bitcoin. Son datos de salida etiquetados. PSBT como protocolo define un montón de roles como el firmante como una cartera de hardware que inspecciona la transacción y produce una firma. Es sencillo y no necesita entender mucho. El creador es una herramienta que toma una transacción sin firmar y toma algunos datos. Hay un papel llamado actualizador que dice oh, estos resultados son míos y aquí hay algún script que los gasta, aquí hay una ruta de derivación para mis claves y eso es sencillo. La parte más crítica de PSBT es un finalizador que tiene el trabajo donde para cada entrada toma todas las firmas adjuntas a todas las claves, y todos los datos involucrados, y ensambla eso en una transacción completa. Toma los datos estructurados de PSBT que tienen datos apropiadamente asociados, y luego necesita ensamblar un testigo con las firmas correctas en el orden óptimo e inserta 1's y 0's para elegir diferentes ramas de script. El trabajo del finalizador es muy complicado. Necesita hacer muchas cosas para construir una transacción a partir de estos datos. Un finalizador es típicamente algo que los desarrolladores de carteras necesitan escribir por su cuenta, pero miniscript le permite escribir un finalizador totalmente general que puede trabajar con muchas carteras diferentes y puede ser una herramienta lista para usar que puede obtener interoperabilidad. Miniscript codifica como script; tu script ya está en el PSBT, y miniscript te permite parsear el script en esta cosa estructurada. Puedes parsear los scripts existentes en miniscript, hacer el análisis y luego averiguar qué claves y firmas necesitas.

P: ¿Cómo interoperará esto con taproot?

R: Básicamente necesitaremos duplicar el tamaño de miniscript para taproot. Miniscript está diseñado para codificar como bitcoin script; taproot tiene una nueva versión de bitcoin script, con algunos cambios sutiles muchos de los cuales fueron diseñados para hacer miniscript más fácil de implementar. Tapscript, que es la parte de script de taproot, necesitaríamos añadir algunos opcodes más a miniscript como lo de las ramas podadas merkleizadas y también la nueva forma de hacer multifirma en tapscript.

P: ¿Cuáles son las principales diferencias entre miniscript y otros intentos como Ivy y Simplicity?

R: La simplicidad está en su propia categoría, que es todo un lenguaje de sustitución. Sin embargo, Ivy es un buen ejemplo. Miniscript no se compila. No se trata de escribir en un lenguaje de alto nivel y confiar en que la salida coincida con la entrada. Miniscript es sólo una codificación de scripts, lo que significa que, en primer lugar, no es necesario confiar en que la salida coincida con la entrada, ya que se puede comprobar por sí mismo mediante la eliminación de datos. Además, puedes ir hacia atrás desde el script hasta la política. Miniscript no es un lenguaje de nivel superior, es sólo una versión mejor estructurada al mismo nivel. Esto es lo que debería haber sido el script.

WT: ¿Qué seguridad tienen los desarrolladores de que el consenso es el comportamiento que esperan?

R: Muy seguro, por dos razones. En la pantalla hay 26 fragmentos y todos son pequeños y sencillos. Y además no usamos los somáticos raros, salvo que OP\_CSV toma un número de 5 bytes donde los otros toman números de 4 bytes.

# Boletín de Bitcoin optech

Una cosa genial es el boletín de bitcoin optech. Voy a omitir algunos. Hicieron una matriz de compatibilidad de billeteras. Ellos están presionando para el uso de segwit. Cualquiera que sea el monedero que estés usando, puedes recorrerlo y ver qué características superan. Esto es útil a la hora de elegir un intercambio o algo así. Tuvieron una serie de 27 semanas en las que el boletín de cada semana incluía una sección sobre segwit, como por ejemplo cómo implementarlo y por qué implementarlo. Cualquiera que sienta curiosidad por segwit lo encontrará útil y podrá volver a hojearlos. Son lecturas bastante cortas.

P: ¿Hay alguna gran sorpresa en esa matriz de compatibilidad, como alguien que no lo haga tan bien o alguien que lo haga realmente bien?

R: La verdad es que no. Una cosa que me pareció genial es que a veces ves cosas como la cartera Wasabi, que tiene todas las cosas buenas, pero las nuevas carteras ni siquiera se molestan en codificar las cosas heredadas, lo que es un poco molesto si quieres recibir fondos en una dirección heredada en - como recibir segwit nativo envuelto. Usted puede enviar a ellos, sin embargo. Sólo quieren que sientas el dolor si estás recibiendo desde una cartera antigua, y obligarles a actualizar. Eso es bueno; no los culpo.

... muchos de ellos soportan pay-to-pubkey-hash que es algo así como el single sig, sólo que usando una cartera de hardware. ... También hay algunas restricciones extrañas en la longitud de las direcciones. Algunos de ellos soportan bech32. Algún comentario sobre esto o experiencias con la adopción de segwit-- ¿tu cartera lo utiliza? ¿Alguna opinión al respecto? Bien, podemos seguir avanzando.

# Cambios notables en el código

Aquí hay un cambio de código notable que me pareció interesante. Nicolas Dorier hizo btcpay. Tiene un pull request abierto para permitir una lista blanca para los filtros bloom. Si tienes un cliente lite, como en tu teléfono móvil, tienen una característica de lista blanca donde básicamente puedes permitir -- es otra forma de usar tus nodos completos y hablar con clientes lite. ¿Alguna idea sobre esto?

P: ¿Por qué un filtro de floración en lugar de preguntar a los amigos?

R: Fue uno de los primeros intentos de hacer un cliente lite para que pudieras ejecutar un monedero y verificar tus transacciones sin tener que tener un blockchain completo de datos. Así que enviarías filtros de florecimiento a un nodo completo que soporta esta característica.

Si sabes cómo funcionan los filtros bloom, se hizo en su día como una forma de que los clientes lite no sincronizaran todo el blockchain, pero tiene grandes inconvenientes tanto de privacidad como de seguridad, ya que un filtro bloom como usuario final no es realmente un usuario de bitcoin, no estás verificando nada por ti mismo y confiando en que el servidor con el que hablas te está diciendo la verdad y no está registrando todos los filtros que le pides... es básicamente como si le dieras todas tus direcciones. Así que este tipo de cartera se ha vuelto cada vez menos importante con el tiempo. La otra razón además de ser mala para tu privacidad y seguridad, también fue muy mala para los nodos de bitcoin. Abrió los nodos de bitcoin completos a un ataque DoS trivial. Ataque DoS trivial de bajo ancho de banda. Con un ancho de banda extremadamente bajo, podrías paralizar la mayoría de los nodos de todo el mundo. Como resultado, mucha gente ha desactivado bloom desde hace muchos años, por defecto. Desde entonces, existe bip158 neutrino, que no ayuda a la privacidad, pero al menos no es un vector de DoS para los nodos completos. Algunas personas lo califican de controvertido porque fomenta el uso de bitcoin sin verificar nada por uno mismo; pero otras personas lo llamarían un mal necesario. Pero entonces deberías aprender sobre assumeutxo.... así que hay mucho en esta historia. Al tener la capacidad de hacer una lista blanca o negra de bloom, ni siquiera sabía que alguien tenía un pull request para esto. Es realmente bueno. Bloom es la mejor manera de conectarse a tu propio nodo completo, preferiblemente sobre un nodo completo, porque confías en ti mismo para indexar completamente, así que tu cliente telefónico usando tu propio nodo completo también es soberano. Pero sí, podrías usar RPC. Si tienes habilitado el bloom, toda la red podría quedar paralizada a muy bajo coste.

P: ¿Cómo se ha fusionado esto?

R: ¿Quieres la respuesta amable o no? Algunas personas priorizan la adopción por parte del usuario sobre la privacidad y la seguridad. Hay una compensación cuando lo haces de manera imprudente, tal vez. Bloom es mucho menos ancho de banda y más rápido si lo usas de forma segura para tu propio nodo, que el neutrino. Así que sigue siendo útil. Sólo que yo no lo habilitaría por defecto, a menos que aceptes el riesgo de que tu nodo sea DoSed.

P: ¿Por qué no hemos visto un ataque DoS? Con el bip66, hubo una amplia difusión del valor de la s y fue un caos.

R: los nodos p2p no están usando bloom para hablar entre ellos. Hay un ataque de agotamiento de memoria; creo que fue arreglado antes de que fuera público. Nunca se arregló del todo. Bloom se añadió por primera vez en la v0.7 o v0.8. Desde entonces, han añadido más y más mitigaciones a Core que reducirían la capacidad de paralizar el nodo, pero nunca está totalmente protegido. La otra razón para no usarlo, especialmente en las conexiones p2p normales sin encriptar y sin autenticar, es que no hay manera de saber que estás siendo mitigado. Así que alguien podría interceptarlo trivialmente y espiarte, filtrarte o mentirte. Así que esa es otra razón... hay muchas razones para querer... no sé si se le dio oficialmente un número, pero bip324 era un reemplazo para bip150 y bip151 que era la encriptación y la autenticación como una opción para las conexiones p2p. Generalmente se quiere eso por todo tipo de razones. Deberías animar a los desarrolladores a trabajar en eso como una opción para el futuro de las conexiones p2p.

# Signet

Regtest es una versión en miniatura de una red que puedes poner en marcha en tu ordenador como prueba. Ahora hay una nueva cosa de signet. ¿Alguien ha utilizado signet? ¿Podría dar un tldr sobre él?

<https://btctranscripts.com/scalingbitcoin/tel-aviv-2019/edgedevplusplus/signet/>

# SNICKER

SNICKER es como esta interesante propuesta de coinjoin. Básicamente, si puedes averiguar quién es el propietario, dada una clave pública en el blockchain de bitcoin, puedes preparar un montón de coinjoins y ellos podrían elegir hacerlo. Así que se lo envías a ellos, y ellos podrían optar por aceptarlo. Podría volverse más popular cuando llegue taproot, porque taproot es mayormente pay-to-pubkey así que las pubkeys serán un poco más visibles. No necesitas saber quién es el dueño, y es más barato que el coinjoin normal, y no hay interacción.

Coinjoin es un mecanismo de privacidad en bitcoin en el que un grupo de personas deciden combinar transacciones y luego dar un montón de salidas con todas las mismas cantidades y puede ocultar de dónde vino su BTC. Sin embargo, no sabes quién es el creador de esta transacción. SNICKER tiene mejores garantías de privacidad y es más barato.

# Cosas rápidas al azar

Aquí hay un script de python genial que alguien hizo, que puede imprimir un gráfico de quién estaba minando en un momento dado. Podrías hacer una animación, supongo.

Aquí hay un nuevo explorador de bloques que no había visto antes; hace un mapeo de entradas y salidas. Todavía no entiendo bien esta cosa, KYCP, pero parece bastante interesante. Hay algún análisis de Boltzmann para cuantificar cómo algunas medidas de privacidad, no estoy muy seguro. Lo probé una vez. Conoce la privacidad de tu moneda. El objetivo de este explorador de bloques es mostrar cuánto es visible y revelable en una transacción determinada. Así que la mayor parte de esto se centra en su privacidad. Hace que sea fácil volver atrás en el tiempo y mirar. Creo que es una de las personas de Samurai. ¿Creo que es Chainalysis? No, es blockchain.info. De acuerdo, seguimos.

Este es projectmempool.space que tiene un montón de gráficos interesantes, como la utilización del mempool. Estas son las transacciones que están esperando ser confirmadas. Esta es la tasa que la gente está pagando para entrar en el blockchain, graficada en el tiempo.

# Inmersión en el código de Bitcoin

Esto es hacer algunos análisis sobre la actividad en el repo de Bitcoin Core. En algunos días de la semana hay mucha actividad, pero no en los fines de semana. También muestra el número de commits; está aumentando con el tiempo en general. Aquí está el análisis de cuánto tiempo permanece el código creo. Creo que eso es lo que es. ¿Qué es el análisis de burndown? Realmente no tiene sentido sin embargo... ¿así que esto desapareció inmediatamente?

# Fuego rápido de nuevo

Chainalysis menciona que la mayoría de los bitcoin mixtos no se utilizan con fines ilícitos. Este fue un interesante artículo en Bitcoin Magazine. Wasabi Wallet ha recibido 250 millones de dólares en lo que va de año y va en vertical. Así que eso es genial. Luego hay un análisis de este mercado de fabricantes, un sucesor de la ruta de la seda. Bitcoin sigue siendo el principal modo de pago, y Monero no lo es. Es el método de pago dominante, así que eso es interesante.

Esto es un hackeo en EOS. Había un contrato inteligente que utiliza un generador de números aleatorios en la cadena basado en la altura del bloque, y alguien fue capaz de robar una cantidad impía de dinero del contrato inteligente porque estaban utilizando un RNG basado en la cadena de bloques. ¿Algún comentario al respecto?

Aquí hay algunas cosas nuevas en la GUI de Bitcoin Core. Esta permite deshabilitar las claves privadas para un monedero de vigilancia. PR 15450. Eso es genial. Aquí hay una nueva GUI para Bitcoin Core que utiliza la poda y reduce la cantidad de bloques históricos que almacena. También hay un montón de transcripciones de la conferencia Bitcoin Edge Dev++.

Algunos de nosotros también fuimos al taller optech de bitcoin taproot, el editor del boletín optech. Fue genial. Era un montón de código python en cuadernos jupyter. Instalas una versión de Bitcoin Core con el código taproot bip ejecutado, y eres capaz de escribir transacciones contra eso y puedes aprender cómo funciona taproot contra eso. Hay ejemplos muy profundos hechos por la gente de residencia de Chaincode Labs. Podrían estar interesados en hacer un seminario o taller de taproot de un día.

# Cosas de Lightning

La sección de lightning es algo pequeña esta vez. Hay algunas cosas que he estado leyendo también, tangencialmente relacionadas. Una cosa que me pareció interesante y que Justin tocó y que no está en esta lista, pero que de todos modos la traigo a colación, es la discusión en la lista de correo de bitcoin-dev sobre la nomenclatura del uso de la palabra dirección. Pensé que era un punto interesante para la discusión.

P: ¿Qué tiene de malo una dirección?

R: La palabra "dirección" fomenta la reutilización de direcciones. La gente piensa que es una cuenta bancaria o una dirección postal o de correo electrónico. Pero en realidad las direcciones no deberían reutilizarse. Tiene problemas de seguridad y privacidad.

Otra cuestión es que la gente piensa en las monedas a partir de las direcciones, lo que provocó muchas pérdidas de dinero, ya que desde que se creó el bitcoin hubo confusión al respecto. Una cosa de la que hablábamos antes con Wasabi, es que te obliga a pensar en cada transacción que recibes. No te dejan reutilizar las direcciones, y te obliga a etiquetar cada transacción que recibes. Las direcciones también ocultan lo que sucede con los UTXO. Cada vez que recibes una transacción, tienes que gastar toda esa salida. Lo que Wasabi pensando en ello y bcoin tiene esto en el código al menos, pensando en ello más como monedas. Cada vez que recibes algo, es una moneda. Para hacer una nueva transacción tienes que combinar monedas y hacer monedas. Sugirieron IDs de factura, tokens de pago, factura bitcoin, dirección en paréntesis para no confundir demasiado a la gente. Ruta de la factura Bitcoin. La bulla es algo de lo que alguien habló. Era una antigua forma de dinero en la que se ponía una cosa de valor en un recipiente de arcilla y se estampaba lo que había en el recipiente en el exterior de la arcilla, y la única forma de canjearlo realmente era rompiéndolo. Es algo parecido a un UTXO. Sólo se puede gastar destruyéndolo y haciendo un nuevo UTXO. Sin embargo, nadie sabría lo que es una bulla. (En broma, tal vez Wasabi se lleve las monedas cuando hagas la reutilización de la dirección, como cuota de servicio de seguridad).

P: ¿Y si se dice "envíalo a esta moneda" o "a este bloqueo"? Alguien sugiere "enviarlo a esta cosa".  Desgraciadamente, "bloqueo" suena demasiado cerca del bloqueo.

Los UTXOs son cosas realmente nuevas en lo que se refiere al intercambio de dinero. No hay una analogía real. La gente encuentra esto confuso sobre bitcoin; que es una escritura y un cierre. Tal vez sea mejor para la adopción hacer un nuevo nombre, para que la gente tenga algo a lo que agarrarse.

# Conciliación de la cadena y fuera de la cadena con eltoo

Intentaré explicar brevemente qué es eltoo. ¿Todos saben lo que es lightning? Sí. Lightning actualmente utiliza este formato de escritura en las transacciones de bitcoin para crear este mecanismo fuera de la cadena. Estos se llaman HTLCs, hashed timelock contracts. Es similar a lo que estábamos viendo antes, como miniscript, no exactamente, son scripts más complejos que no sólo pagan a una clave pública que codifica las condiciones actuales. Una de las formas en que Lightning permite este protocolo fuera de la cadena es que usted tiene dos partes que entran en un contrato multisig y ambos tienen que estar de acuerdo desbloquearlo. Cuando se pagan el uno al otro, son sólo dos personas, y básicamente están de acuerdo en reequilibrar el pago de ese contrato. Uno de los problemas es que lo que sucede cuando no se confía en la otra parte. Así que digamos que la otra persona toma una versión acordada más antigua de su contrato... Hay un mecanismo de castigo, donde existe la posibilidad de robar todo el valor del contrato.

Eltoo es otra propuesta de lightning.. es confuso, si se habla de esquemas de nomenclatura. Eltoo es otra forma de hacer canales de pago sin tener que llevar la cuenta de cada estado intermedio. Lo que hace es que la propuesta original da una nueva forma de actualizar el acuerdo sobre el estado del canal. En lugar de tener este mecanismo de penalización, lo que haría en su lugar es introducir SIGHASH\_NOINPUT --- y el sighash es el hash de la firma, y cuando estás firmando para liberar un UTXO, es un descriptor en tu firma sólo un byte que dice aquí es lo que estoy firmando en la transacción. Es lo que estás bloqueando o comprometiendo. NOINPUT dice que estás comprometiendo un montón de cosas en la transacción que no incluye el id de entrada. En circunstancias normales, esto es muy arriesgado porque estás permitiendo que cualquiera introduzca una entrada válida que coincida con tu firma y diga que con esta entrada esta transacción es válida. Puedes firmar una transacción y cualquiera puede actualizar las entradas. Esto es útil para un protocolo fuera de la cadena como el de relámpago porque lo que podemos hacer es en lugar de confiar en el mecanismo de castigo donde tengo que hacer un seguimiento de los estados, cada vez que actualizamos actualizamos un número en la transacción y decimos que pasamos del estado 3 al estado 4, pero no estamos comprometiendo a la entrada.

P: ¿Sólo se puede reaccionar antes de que se comprometa en un bloque? ¿O hay un bloqueo?

El mecanismo subyacente aquí es que cada actualización de estado es capaz de gastar las monedas de cualquier estado anterior. Así que si alguien intenta robar publicando el estado 2, y el estado 4 existe, el estado 4 es capaz de encadenar las monedas originales como debería, o cualquiera de los estados anteriores. Cualquiera que llegue a la cadena, puede publicar el estado 4. Los estados son números de secuencia. Eltoo utiliza OP\_CSV y mira el número de secuencia. Así que la salida del estado 4 dice que cualquier cosa superior puede pasar esto. OP\_CSV tamaño más grande es de 4 bytes. Una parte se utiliza para el bloqueo de tiempo. Hay un rango de números que puede usar para este mecanismo.

Lo interesante de esto es que, cdecker que es uno de los autores del documento de eltoo, hace esta conexión de modelo mental entre eltoo este tipo de mecanismo de actualización y el mecanismo utxo que ya utilizamos en la cadena. Y él, no creo que haya propuesto nada concreto, pero básicamente dice que se pueden re-duplicar los mecanismos tipo bitcoin usando eltoo porque si lo piensas cuando hablamos de un UTXO estamos hablando de un estado previo que se destruye y vamos a moverlo a este nuevo estado que acordamos. Sugiere que usando este mecanismo, puedes reconciliar modelos dentro y fuera de la cadena con eltoo. Así que eso está muy bien.

También hay una implementación en python de eltoo por Richard Myers que trabaja en gotenna. Es bastante interesante.

A algunas personas les preocupa que SIGHASH\_NOINPUT no pueda considerarse seguro porque los usuarios podrían ser estúpidos y utilizarlo en situaciones inapropiadas. Pueden darse situaciones de doble gasto si los usuarios no tienen cuidado. ¿Hasta qué punto son responsables los desarrolladores del protocolo de proteger a los usuarios de los malos diseñadores de carteras? No creo que haya una respuesta correcta. Hay gente en dos bandos. Esto ha introducido algunas discusiones más como, deberíamos llamarlo SIGHASH\_NOINPUT\_UNSAFE. O tal vez las firmas de acompañamiento donde usted tiene que optar por, y también el etiquetado de salida que es otra manera de bloquear y ser explícito al respecto. Así que es una idea interesante. No sé si alguien tiene alguna aportación u opinión sobre cuánto deberíamos proteger a los usuarios tontos de hacer cosas tontas. Ni siquiera se trata de proteger a los usuarios tontos; tienen que hacerlo los diseñadores de carteras. Un usuario tendría que optar por usar una cartera que ha decidido utilizar esta característica insegura. Mi opinión personal es que lo uses bajo tu propio riesgo. Hay todo tipo de formas de que las billeteras roben tu dinero. Pero esto no es un problema hipotético; ha habido diseñadores de monederos tontos en bitcoin así como en shitcoins.

Se podrían hacer sistemas tipo bóveda con NOINPUT. Existe la preocupación de que la gente sea demasiado experimental. Pero de nuevo, úsalo bajo tu propio riesgo.















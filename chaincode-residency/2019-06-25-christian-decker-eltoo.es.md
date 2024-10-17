---
title: Eltoo - El (lejano) futuro de lightning
transcript_by: Michael Folkson
translation_by: Francisco Calderon
tags:
  - eltoo
  - lightning
date: 2019-06-25
speakers:
  - Christian Decker
media: https://www.youtube.com/watch?v=3ZjymCOmn_A
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-christian-decker-eltoo.es/
---
Tema: Eltoo: El (lejano) futuro de lightning

Lugar: Chaincode Labs

Diapositivas: https://residency.chaincode.com/presentations/lightning/Eltoo.pdf

Eltoo white paper: https://blockstream.com/eltoo.pdf

Artículo de Bitcoin Magazine: https://bitcoinmagazine.com/articles/noinput-class-bitcoin-soft-fork-simplify-lightning

# Intro

¿Quién nunca ha oído hablar de eltoo?  Es mi proyecto favorito y estoy bastante orgulloso de él. Intentaré que esto sea breve. Me dijeron que todos vieron mi presentación sobre la [evolución de los protocolos de actualización](https://www.youtube.com/watch?v=HauP9F16mUM). Probablemente iré bastante rápido. Quiero darles a todos la oportunidad de hacer preguntas si tienen alguna.

# Protocolos fuera de la cadena (off-chain)

Ya vimos esto ayer.  Básicamente, el mecanismo de actualización es que algunas personas se encuentran, bloquean su estado en la cadena, luego van y negocian fuera de cadena sobre qué hacer con este estado. Pueden renegociar una y otra vez. El protocolo de actualización asegura que todos los estados invalidados ya no sean aplicables. El mecanismo de penalización de lightning hace esto al penalizar a quien se está portando mal. Los canales de micropagos dúplex y eltoo lo hacen anulando los efectos a los que estaba tratando de portarse mal.

# Mecanismo de actualización de eltoo

Eltoo, solo una anotación rápida. Yo represento las salidas como círculos y las transacciones como cuadrados. A esto se le llama transacción de financiación. Básicamente, toma fondos del usuario verde, llamémosla Alice, y crea una salida multifirma que está controlada tanto por Alice como por Bob, siendo Bob el tipo azul. A partir de ahí, todos los cambios en el estado de esta salida deben negociarse entre los dos.

Lo que hacemos en Eltoo es básicamente adjuntamos a esta salida una transacción de asentamiento llamada `Settle 0` que refleja el estado inicial. En realidad, podríamos dejar esto y queda como que Alice crea un canal, luego líquida el canal y Alice obtiene su bitcoin de 5 bitcoin. Este timelock que está representado por este reloj aquí garantiza que durante este tiempo de espera podemos entrar y crear una actualización (`update tx`). Si hacemos eso, creamos esta actualización (`update 1`) que tiene esta salida y crea un nuevo lugar para adjuntar un nuevo asentamiento (`settle 1`) que refleja el nuevo estado.  En este caso, hemos transferido 1 Bitcoin de Alice a Bob. Este tipo (`Settle 0`) se convierte en doble gasto y podemos olvidarnos de esto. Actualmente estamos reproduciendo esto onchain, pero podemos levantar esto offchain con bastante facilidad más adelante. Podemos repetir esto una y otra vez y básicamente ya es todo el mecanismo. Cuando queremos crear una nueva actualización, hacemos un doble gasto de esta salida, esto se vuelve inválido, nunca más podrá alcanzar la cadena de bloques. `Update 2` acelera esto y abre un punto donde podemos adjuntar `Settle 2`, y podemos hacer esto las veces que queramos.

P: Para tus actualizaciones, cuando dices que avanza, ¿cuál es esa transacción, `Update 1`? ¿Eso es gastar en una nueva multifirma 2 de 2?

R: Exáctamente. Esta es la multifirma que comparten Alice y Bob que contiene esos 5 Bitcoin. Ahora tomamos esta transacción de actualización, gastamos esta salida y creamos una nueva salida que también contiene 5 Bitcoin, propiedad de Alice y Bob. Siendo la única diferencia lo que podemos adjuntarle. A esto podemos adjuntarle `Settle 1` pero no `Settle 0`. Lo otro que es particular de este es que podemos adjuntar `Update 2` pero no `Update 1`.

Hemos jugado este juego en la cadena de bloques. Hicimos esto en la cadena de bloques y es realmente malo. Cada vez que hacemos una actualización, creamos una transacción onchain lo cual probablemente no sea lo que queremos porque pagamos comisiones cada vez. Esperamos confirmaciones cada vez. No tendríamos que esperar por confirmaciones porque estos tiempos de espera se eligen de tal manera que siempre tengan prioridad sobre esto. Podemos asegurar que si estos dos están afuera `Settle 0` se confirmaría porque `update 1` tiene prioridad.

P: Si el tiempo de espera expira y no has transmitido `Update 1` entonces puedes transmitir `Settle 0`. que pasa si tienes un canal que no tiene mucha acción en eso?

R: En el caso onchain donde comenzamos este tiempo de espera inmediatamente con la creación de la salida de financiamiento. en ese caso si, esto tiene un tiempo de vida limitado a lo que tu te sientas cómodo esperando. Si esto es una semana, probablemente luego de seis días debas difundir esto. Con la construcción actual de eltoo podemos introducir una transacción de activación aquí que es una actualización sin asentamiento. En este caso, esto permanecerá allí y solo cuando transmitamos una transacción de activación, el tiempo de espera comenzará a correr. Así es como podemos convertir una vida limitada en una vida indefinida.

P: ¿Tu darías una transacción `Update 1 `después de transmitir la salida de financiamiento onchain?

R: La transacción de activación es en realidad idéntica a la `Update 1`, no tenemos un `Settle 0`. Esa es exactamente la idea, sí.

Ahora tenemos esta enorme huella en la cadena que es realmente mala. Eliminamos este protocolo y tomamos todas estas transacciones que no están bloqueadas y las guardamos en la memoria. Lo que hacemos es básicamente que queremos que `Update 3` se pueda adjuntar a un acuerdo, pero realmente no podemos hacer eso porque `Update 1` podría estar disponible y no tenemos forma de adjuntar `Update 3` a `Update 1` y la funding output. Lo que propusimos y el jurado aún está deliberando sobre si la gente realmente quiere esto en Bitcoin, es tener una nueva bandera SIGHASH. ¿Probablemente ustedes estudiaron las banderas SIGHASH la semana pasada? ¿Quién no sabe lo que hacen las banderas SIGHASH? Excelente. SIGHASH_NOINPUT tomaría una transacción y dejaría en blanco la referencia a la salida que está gastando. Lo que hace esto es eliminar el compromiso directo con los fondos que estamos gastando y lo hacemos reescribible. Puedo tomar `Update 3` y reescribirla para que apunte al resultado de la financiación, por ejemplo. Omitimos `Update 1` y `Update 2` y vamos directamente a `Update 3` al redirigir este puntero aquí. La firma sigue siendo válida porque borramos antes de firmar y borramos antes de verificar la firma. Ya no nos comprometemos con los inputs que gastamos. Tenemos esta situación en la que tenemos `Update 3` que se puede adjuntar a la transacción de financiación, se puede adjuntar a la salida de `Update 1` y también se puede adjuntar a `Update 2`. Estamos en este caso aquí (`Settle 2`) donde Bob tiene 3 Bitcoin y Alice tiene 2 Bitcoin. Soy Alice, me gustaría resolver este (`Settle 1`) o incluso mejor este (`Settle 0`). Enviaré `Update 1` porque eso inicia el cierre con el efecto deseado que quiero. Bob entra y ve que Alice está haciendo trampa aquí, ella está tratando de llegar aquí (`Settle 1`). Bob toma `Update 3` y la reescribe internamente para señalar `Update 1`. `Update 1` se confirma porque Alice esperaba obtener este resultado (`Settle 1`). Pero Bob ha acelerado esto y lo ha gastado dos veces (`Settle 1`). Al tener este movimiento hacia adelante hacia el estado posterior que acordamos, podemos asegurarnos de que cualquier efecto anterior pueda ser reemplazado por un estado posterior. Lo que eso significa para nosotros es que un jugador honesto siempre debería poder reaccionar ante cualquier cosa que suceda, ya sea solo la salida de fondos o alguien publicó `Update 0` o lo que sea. Manteniendo la última actualización y el último asentamiento, siempre puedo reaccionar a lo que suceda en la cadena.

P: En el peor de los casos, donde puede tener múltiples actualizaciones transmitidas en la cadena, ¿es peor que la forma actual con la revocación?

A - Por supuesto. Con Lightning, el cierre unilateral de un canal es siempre un proceso de dos pasos. Publicamos el compromiso y barremos los fondos. Termina ahí. Con eltoo puede suceder que volvamos a reproducir `Update 1`, `Update 2`, `Update 3` y luego seguimos y seguimos porque siempre es el otro tipo el que tiene una mejor situación. Un truco realmente genial que descubrió Rusty es que se trata de transacciones de entrada única y de salida única. Entonces podemos firmarlos usando SIGHASH_SINGLE lo que significa que después del hecho podemos adjuntar una nueva entrada y una nueva salida. De esa forma pagamos las tarifas. Siempre tienes que pagar las tarifas. Si todo esto fuera gratis, podríamos reproducir todos los estados. Pero es probable que hayamos dado diez pasos y me estoy aburriendo porque estoy pagando tarifas y no obtengo el efecto que quiero. Salto al último estado y he terminado. Quiero que esto se resuelva, no voy a pagar más tarifas. Así es como penalizamos el mal comportamiento en la red, pero no lo penaliza de una manera tan mortal como en Lightning Penalty, donde se pierden todos sus fondos. A menudo lo comparo con una muerte por mil cortes en comparación con una muerte por decapitación. Créeme, quiero mil cortes.

P: …

R: Eso es algo que nos tomó un tiempo darnos cuenta. Podemos tener una forma de que `Update 2` solo se pueda adjuntar a cualquier cosa que tenga un número de estado más bajo. La forma en que lo hacemos es que cada uno de ellos tenga una operación CLTV como lo primero. Este tipo (`Update 1`) obtiene un tiempo de bloqueo que está en algún lugar del pasado, por lo que en realidad no tenemos un tiempo de bloqueo, pero aún podemos compararlo con el número de estado actual. Lo que hace este tipo (`Update 2`) al ejecutar el Script es extraer mi propio tiempo de bloqueo y compararlo con el número de estado que ya está en la pila del anterior. Solo si ese tiempo de bloqueo es mayor que el número de estado que el anterior empujó en la pila, será válido. La razón por la que usamos tiempos de bloqueo en el pasado es porque en realidad no queremos un tiempo de bloqueo, solo queremos tener esta comparación entre dos números. Los tiempos de bloqueo en el pasado son inmediatamente válidos.

P: …

R: Y marcas de tiempo. La semántica del tiempo de bloqueo cambia de alturas de bloque a marcas de tiempo a una altura de bloque de 5 millones. Tenemos un rango entre 5 millones y la marca de tiempo UNIX actual, que es de aproximadamente mil millones. Tenemos alrededor de mil millones de actualizaciones que podemos realizar con este mecanismo con todos los tiempos de bloqueo en el pasado. Y nuestra rango crece con el tiempo, así que eso es bueno. Mil millones es más de lo que ha hecho ningún canal.

P: …

R: este es un bloqueo de tiempo relativo, de modo que solo cuando se crea esta salida, este tiempo de espera comienza a funcionar. Tenemos cronologías absolutas para asegurarnos de no adjuntar `Update 1` a `Update 3`.

P: …

R: El problema de tener el número de estado en el script de entrada es que el script de entrada no está comprometido en la firma. Podría seguir adelante y crear una secuencia de comandos de entrada con cualquier número de estado que sea más alto que el que estoy tratando de reemplazar. El tiempo de bloqueo está comprometido en una firma. Eso fue todo un dolor de cabeza. No estoy seguro de que Russell O'Connor lo llamaría convenios. Usualmente te ríes de mis intentos de crear convenios. Toda la discusión de SIGHASH_NOINPUT ha comenzado y es una discusión sin fin. Estoy tratando de mantenerme al margen tanto como sea posible. Solo quiero mis herramientas divertidas y no me importa la implementación real. A la gente le gusta teorizar sobre cómo hacerlo más seguro.

P: …

R: Tan pronto como toquemos la cadena de bloques podemos restablecer todo el estado. No es necesario que transfiramos el estado de una instancia de este protocolo a la siguiente. Si finalmente voy y uso `Settle 1`, puedo reutilizar esta salida nuevamente para crear una nueva instancia de esto. Pero dado que cualquier cosa que se construya sobre esto aquí nunca se puede adjuntar a nada aquí porque eso ya está resuelto, ya no tengo que preocuparme por eso. En la nueva instancia aquí estaríamos usando nuevas claves. Una de las desventajas de SIGHASH_NOINPUT es que en realidad hace posible la reproducción. Puedo tomar cualquier transacción que tenga una entrada que se ajuste a alguna salida en la cadena de bloques, puedo adjuntarla. Llamo a este enlace a través de compatibilidad de scripts en lugar de enlace a través de un compromiso explícito con una salida que está gastando. Nos da mucha flexibilidad, en realidad permite todo esto. Pero tiene el costo de que su uso podría resultar peligroso. Algunas de las propuestas en la lista de correo se dirigen a llamarlo SIGHASH_NOINPUT_DANGEROUS, lo cual me parece gracioso, pero estoy totalmente de acuerdo.

P: …

R: Supongamos que su billetera crea todas las firmas con SIGHASH_NOINPUT. Tiene dos salidas que son 5 Bitcoin cada una en la misma dirección. Quieres enviarme 5 Bitcoin. Creas una transacción haciendo eso. Obtengo mis 5 Bitcoin usando su única salida, pero puedo tomar esta transacción, reescribirla y adjuntarla a la otra salida también. De repente, obtuve 10 bitcoins mientras que tú solo querías enviarme 5. Así es como volvemos a jugar en este caso. Hay un par de salvaguardas que intentamos utilizar aquí. Si cambia las claves públicas o las direcciones que usa, esta vinculación a través de la compatibilidad de scripts se rompe. Por lo tanto, no puedo aceptar ninguno de los otros fondos que no tengan la misma dirección o Script. La otra salvaguarda es que nos comprometemos con el valor. Todos estos son siempre 5 Bitcoin y aún nos comprometemos con el valor de salida que está tratando de gastar. Si tiene una salida de 10 y 5 y me envía 5, no puedo volver a vincularlo a 10. Eso es simplemente porque no pude encontrar una buena razón para hacer una revinculación que no cambie la transacción y todo un repentinamente la tarifa cambia. Las salidas todavía tienen 5 Bitcoin, pero ahora está gastando 10, entonces, ¿5 se convierte en tarifa? Eso es un poco extraño.

P: …

R: No deben usar SIGHASH_NOINPUT. Es una herramienta muy peligrosa, pero es una herramienta muy específica que no debe usar si no la necesita. Todas estas discusiones giran en torno a eso.

# Eltoo o no eltoo

Es algo simple comparado con el tipo de "Yo tengo esta información, tú tienes esta información" y nunca podremos compartir esa información. Es completamente simétrico. Todo el mundo tiene la misma información. No hay información tóxica que pueda llevarlo a perder fondos. No tenemos penalización como tal. Solo tenemos un pequeño costo si alguna vez publicas una versión anterior que permite los retrocesos.

P: …

A - La desventaja de introducir sanciones a un nivel superior. Créanme, lo intenté porque la pena aparece a menudo. A la gente le gusta penalizar a los demás por cierto. Si alguna vez quieres penalizar a alguien por portarse mal, debes reintroducir esta simetría en el estado. Debe haber algo por lo que pueda identificar que fuiste tú el que se portó mal. Esto se mezcla con este mecanismo de penalización por rayos donde tenemos información diferente. El poder de eltoo proviene de que todo este estado es completamente simétrico y no hay información privilegiada que yo deba saber y tú no. Intenté reintroducir sanciones a un nivel superior. No he encontrado una buena manera de hacerlo, así que suelo seguir con la excusa de que las tarifas son un castigo suficiente.

P: …

R: Podemos reintroducir simetrías en el paso del asentamiento, eso es cierto. Tenemos dos transacciones de liquidación, una para usted y otra para mí. Tenemos una construcción. Con una SHAchain podemos tener secretos de revocación que podemos generar a nuestro antojo básicamente. También tiene una separación de capas más limpia. Lo que me entusiasma es que, además de poder volver a poner eso en Lightning, podemos crear canales multipartitos donde nosotros, como una sala completa, por ejemplo, administramos un conjunto de fondos y podemos moverlos libremente entre cualquiera de nosotros sin tener que abrir canales o tener multihops entre nosotros. Es solo un grupo de fondos que podemos reorganizar como queramos. Luego entramos en las fábricas de canales y todo eso, pero hablaré más sobre eso el jueves.

Las desventajas son que no hay una penalización y necesitamos un cambio en el protocolo de Bitcoin que ha demostrado ser un poco más difícil de lo que anticipé. Ese es siempre el caso. Pasé todo mi doctorado proponiendo cosas y nunca nadie las usó. Hablamos de las propuestas en Core Dev. Hay dos o tres variantes.

# ¿Cuándo a la luna?

En [Core Dev](/bitcoin-core-dev-tech/2019-06-06-noinput-etc/) discutimos las diferentes variantes que podríamos tener. Una variante es que agregamos una firma adicional a un script usando SIGHASH_NOINPUT llamada firma de acompañante. La idea es que su transacción solo sea válida si esa transacción también tiene una firma que no sea SIGHASH_NOINPUT. De esa manera, si somos participantes de una offchain, generaríamos una clave privada y la compartiríamos entre nosotros. Podemos aprobar las versiones de rebote, pero nadie más puede hacerlo. Eso es una protección contra la maleabilidad de terceros. El argumento a favor es que no se desea la maleabilidad de terceros. Puede ser extraño si alguien puede reescribir transacciones que usted no sabía que era posible. El argumento en contra es que es más grande, es más costoso. Necesitamos agregar una clave pública adicional, necesitamos agregar una operación CHECKSIG adicional y necesitamos agregar una firma adicional. Pero tampoco queremos animar a las personas a utilizar SIGHASH_NOINPUT a menos que necesiten esta flexibilidad. Hay una diferencia entre agarrarse de la mano hasta el final o dar una advertencia justa y dejar que las personas toquen el plato caliente y aprendan por sí mismas. Estoy más en el segundo campo. La otra variante es que deberíamos usar una versión de script SegWit diferente, una que no sea serializable en bech32. De modo que, incluso si solo quisiera usar SIGHASH_NOINPUT, no podría crear una dirección a la que enviar. En todas estas construcciones siempre estamos trabajando directamente con scripts y no estamos usando direcciones en nada de esto. Al hacer que un destino SIGHASH_NOINPUT no sea accesible, lo hacemos para que las personas no puedan enviar dinero accidentalmente. Eso es lo segundo. La tercera variante es cambiar el nombre a \_PELIGROSO que me gusta mucho. Deberíamos hacer eso.

P: …

R: Hay un argumento a favor de la fungibilidad que debe hacerse. Es intercambiar lo que más te importa. ¿Se trata de personas que usan carteras que están mal escritas o se trata de que usted no pueda diferenciar las salidas entre sí? En un cierre unilateral se podría decir que hubo un cierre unilateral. En un cierre no unilateral lo harías. El caso malo puede detectarse, poco podemos hacer al respecto.

P: …

R: La sensación que tuve fue que la mayoría de la gente quiere esta funcionalidad porque la gente está muy emocionada de construir cosas encima. Russell O’Connor está proponiendo nuevos convenios interesantes que podríamos hacer y todo el mundo le está diciendo que no lo haga. La flexibilidad que obtenemos, por lo que siento, está siendo vista como positiva. Al menos las personas que estaban presentes y discutiendo allí, nadie tenía sentimientos fuertes por ninguna de las versiones complicadas. Así que puede que eventualmente lo consigamos, quizás.

P: …

R: Eso es cierto. Existe una propuesta alternativa que toma esto y mezcla las diferentes variantes. Esto no se compromete con la secuencia de comandos anterior porque la secuencia de comandos en realidad cambia con el tiempo. Tenemos este número de estado que comparamos con el tiempo de bloqueo, por lo que no podemos comprometernos con el script. Existe la otra variante, que se llama SIGHASH_ANYPREVOUTANYSCRIPT. La otra variante es solo SIGHASH_ANYPREVOUT. Eso todavía se compromete con el Script. Esas son dos variantes propuestas por AJ Towns. Esa es una propuesta competitiva pero me da mi funcionalidad, así que estoy feliz. ANYPREVOUT es un mejor nombre para esto, por lo que probablemente deberíamos usarlo.

P: …

R: Ambos proponen un aumento de la versión de SegWit Script porque estamos redefiniendo un nuevo sighash y los sighash desconocidos son un fracaso inmediato si no los comprende.

P: …

R: El objetivo del gráfico de torta multicolor apilable que mostré al principio es mostrar que estas son capas distintas que podemos reemplazar individualmente. No tenemos que romper la compatibilidad con el resto de la red. Este es solo nuestro mecanismo de actualización. Si los dos aceptamos usar eltoo en lugar del mecanismo de penalización Lightning, podemos comenzar a usarlo. Todo lo que sea de múltiples saltos que vaya más allá de nuestro propio alcance, el alcance de nuestro canal, es decir, los HTLC y la cebolla, siguen siendo idénticos. En realidad, el mecanismo de actualización es solo una forma de negociar la adición y eliminación de salidas a la transacción de liquidación. Entonces, cuáles son esas salidas, ya sean HTLC o canales adicionales, eso es todo para las capas superiores. Esta separación limpia de capas nos permite intercambiar piezas individuales. De hecho, señalaríamos nuestra disponibilidad de eltoo en bits de características tanto en el inicio como potencialmente en el anuncio del nodo, de modo que si solo implemento eltoo podría conectarme selectivamente a pares que también admitan eltoo.

P: …

R: Por supuesto que sí. Implementando eltoo y usándolo solo entre nosotros dos. Por cierto, actualizar es una mala palabra en Bitcoin. Al decidir usar eltoo en saltos individuales, aún mantenemos la capacidad de que los pagos de múltiples saltos permanezcan idénticos y sin romper la compatibilidad en esas capas en absoluto.

P: …

R: Se están discutiendo. No los agregué al BIP en sí porque los BIP son algo estáticos y no quería rastrear todas las diferentes propuestas porque ya ha habido bastantes. Podría escribir una actualización o agregar una página de discusión donde resumiera los pros y los contras de las propuestas individuales. También debo mencionar que tuvimos una reunión en noviembre en Adelaide con algunos de nosotros aquí. Presentamos la hoja de ruta para la especificación de la versión 1.1 y, a propósito, eltoo no se agregó a esa hoja de ruta. No tenemos una buena estimación de si esto va a suceder y cuándo. No queríamos retrasar la versión 1.1 de la especificación por algo que podría llevar algunos meses. Este es realmente el futuro lejano de Lightning y no me hago ilusiones de que esto vaya a suceder este año o pronto. Pero sería genial. Ok, Este soy yo. Si tienen alguna pregunta sobre eltoo, estaré cerca. Señalaré cualquier punto en el que eltoo sea más flexible y más utilizable hasta que alguien me diga que me calle. Gracias.

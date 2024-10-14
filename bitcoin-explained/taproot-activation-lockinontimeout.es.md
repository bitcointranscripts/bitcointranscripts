---
title: Activación de Taproot y LOT=true vs LOT=false
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
  - soft-fork-activation
date: 2021-02-26
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
media: https://www.youtube.com/watch?v=7ouVGgE75zg
episode: 29
aliases:
  - /es/bitcoin-magazine/2021-02-26-taproot-activation-lockinontimeout
---
BIP 8: https://github.com/bitcoin/bips/blob/master/bip-0008.mediawiki

Argumentos para LOT=true and LOT=false (T1-T6 and F1-F6): https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-February/018380.html

Argumento adicional para LOT=false (F7): https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-February/018415.html

Artículo de Aaron van Wirdum en LOT=true or LOT=false: https://bitcoinmagazine.com/articles/lottrue-or-lotfalse-this-is-the-last-hurdle-before-taproot-activation

## Introducción

Aaron van Wirdum (AvW): En directo desde Utrecht, este es el van Wirdum Sjorsnado. Sjors, haz el juego de palabras.

Sjors Provoost (SP): Tenemos "mucho" que hablar.

AvW: Tenemos "mucho" que hablar. En este episodio vamos a discutir el proceso de activación de Taproot y el debate que lo rodea en el lote de parámetros, lockinontimeout que se puede establecer en true y false.

SP: Tal vez como un recordatorio para el oyente hemos hablado de Taproot en general varias veces, pero especialmente en [Episodio 2](https://www.youtube.com/watch?v=G3tXgN7oxaY). Y hemos hablado de la activación de Taproot, de la activación de las horquillas suaves en general en el [Episodio 3](https://www.youtube.com/watch?v=mT0t8Jm0m5E), así que puede que nos saltemos algunas cosas.

AvW: En el Episodio 3 hablamos de todo tipo de propuestas diferentes para activar Taproot, pero ha pasado más de medio año al menos, ¿no?

SP: Eso fue el 25 de septiembre, así que unos cinco meses, sí.

AvW: Ha pasado un tiempo y ahora la discusión ha llegado a su fase final, diría yo. En este momento la discusión es sobre el parámetro del lote, true o false. En primer lugar, para recapitular muy brevemente, Sjors, ¿puedes explicar qué estamos haciendo aquí? ¿Qué es una bifurcación suave?

## ¿Qué es una bifurcación suave?

SP: La idea de una bifurcación suave es que haces las reglas más estrictas. Eso significa que desde el punto de vista de un nodo que no se actualiza nada ha cambiado. Sólo ven las transacciones que son válidas para ellos de los nodos que sí se actualizan. Debido a que tienen reglas más estrictas se preocupan por lo que sucede. Lo bueno de las bifurcaciones suaves es que como usuario de un nodo puedes actualizar cuando quieras. Si no te importa esta característica, puedes actualizar cuando quieras.

AvW: Una bifurcación suave es una actualización del protocolo compatible con el pasado y lo bueno es que si la mayoría de los mineros aplican las reglas, eso significa automáticamente que todos los nodos de la red seguirán la misma cadena de bloques.

SP: Así es. Los nodos más antiguos no conocen estas nuevas reglas, pero sí saben que seguirán la cadena con más pruebas de trabajo, siempre que sean válidas. Si la mayoría de los mineros siguen las nuevas reglas, entonces la mayoría de las pruebas de trabajo seguirán las nuevas reglas. Y por lo tanto, un nodo antiguo seguirá eso por definición.

AvW: Lo bueno de las bifurcaciones suaves es que si la mayoría del poder de hash aplica las nuevas reglas, la red permanecerá en consenso. Por lo tanto, las últimas bifurcaciones suaves se activaron mediante la coordinación del poder de hash. Eso significa que los mineros podían incluir un bit en los bloques que minaban señalando que estaban listos para la actualización. Una vez que la mayoría de los mineros, el 95% en la mayoría de los casos, indicaban que estaban preparados, los nodos lo reconocían y aplicaban la actualización.

SP: Así es. Un nodo comprobaría, por ejemplo cada dos semanas, cuántos bloques señalaron esta cosa y si es así, entonces dice "Ok la bifurcación suave está ahora activa. Voy a suponer que los mineros van a aplicar esto".

## La capacidad de los mineros para bloquear una actualización de la bifurcación suave

AvW: Correcto. El problema con este mecanismo de actualización es que también significa que los mineros pueden bloquear la actualización.

SP: Sí, ese es el inconveniente.

AvW: Incluso si todo el mundo está de acuerdo con la actualización, por ejemplo en este caso Taproot, parece tener un amplio consenso, pero a pesar de ese amplio consenso los mineros podrían bloquear la actualización, que es lo que ocurrió con SegWit hace un par de años.

SP: Por aquel entonces hubo mucho debate sobre el tamaño del bloque y muchas propuestas de hard fork y muchos sentimientos heridos. Al final fue muy difícil conseguir que se activara SegWit porque los mineros no estaban señalando para ello, probablemente en su mayoría de forma intencionada. Ahora también puede ocurrir que los mineros simplemente ignoren una actualización, no porque no les guste, simplemente porque están ocupados.

AvW: Sí. En el caso de SegWit eso se resolvió al final a través de UASF, o al menos eso fue parte de ello. No vamos a entrar en eso en profundidad. Eso significó básicamente que un grupo de usuarios dijo "En este día (alguna fecha en el futuro, fue el 1 de agosto de 2017) vamos a activar las reglas de SegWit sin importar el poder del hash que lo soporte."

SP: Correcto, al mismo tiempo y tal vez como consecuencia de eso, un grupo de mineros y otras empresas acordaron que comenzarían a señalar para SegWit. Hubo un montón de otras cosas que sucedieron al mismo tiempo. Lo que ocurrió el 1 de agosto, la cosa se activó, o un poco antes creo.

## El parámetro lockinontimeout (LOT)

AvW: Ahora nos adelantamos en el tiempo, han pasado cuatro años y ahora la actualización de Taproot está lista para salir. Lo que ocurrió hace un par de años está provocando un nuevo debate sobre la actualización de Taproot. Eso nos lleva al parámetro lockinontimeout (LOT) que es un parámetro nuevo. Aunque está inspirado en cosas de ese periodo de actualización de SegWit.

SP: Es básicamente una opción incorporada en el UASF que puedes decidir utilizar o no. Ahora hay una manera formal en el protocolo de hacerlo para activar un soft fork en una fecha límite.

AvW: LOT tiene dos opciones. La primera opción es falsa, LOT es false. Eso significa que los mineros pueden señalar la actualización durante un año y luego en ese año si se cumple el umbral del 90 por ciento para la actualización se activará como acabamos de explicar. Por cierto, 1 año y 90 por ciento no es algo fijo, pero es lo que la gente parece establecer. Por conveniencia es lo que voy a usar para discutir esto. Los mineros tienen 1 año para activar la actualización. Si después de ese año no han actualizado la actualización de Taproot expirará. Simplemente no ocurrirá, esto es LOT es false.

SP: Y por supuesto siempre está la opción entonces de enviar una nueva versión, intentándolo de nuevo. No es un "no", es que no pasa nada.

AvW: Exactamente. Luego está LOT=true que, de nuevo, los mineros tienen 1 año para señalar su apoyo (disposición) a la actualización. Si se alcanza un umbral del 90 por ciento, la actualización se activará. Sin embargo, la gran diferencia es lo que ocurre si los mineros no alcanzan este umbral. Si no dan la señal para la actualización. En ese caso, cuando el año esté a punto de terminar, los nodos que tengan LOT=true empezarán a rechazar todos los bloques que no señalen la actualización. En otras palabras, sólo aceptarán bloques que señalen para la actualización, lo que significa, por supuesto, que se cumplirá el umbral del 90 por ciento y, por tanto, se activará Taproot, o cualquier otra bifurcación suave de este mecanismo.

SP: Si se producen suficientes bloques.

AvW: Si se producen suficientes bloques, sí, es cierto. Un pequeño matiz para los que lo encuentren interesante, incluso los nodos LOT=true aceptarán hasta un 10% de bloques que no señalicen. Eso es para evitar escenarios extraños de división de la cadena.

SP: Sí. Si se activa de forma normal, sólo el 90% tiene que señalar. Si se ordena la señalización, sería raro tener un porcentaje diferente de repente.

AvW: Van a aceptar el primer 10% de los bloques que no emitan señales, pero después se rechazarán todos los bloques que no emitan señales. Así que el umbral del 90% se alcanzará sin duda. La gran razón para LOT=-true, para ponerlo en true, es que de esta manera los mineros no pueden bloquear la actualización. Incluso si intentan bloquear la actualización, una vez que el año ha terminado los nodos seguirán aplicando Taproot. Así que está garantizado que se produzca.

SP: Si se producen suficientes bloques. Podemos entrar en algunos de los riesgos de esto, pero creo que quieres seguir explicando un poco.

AvW: La razón por la que a algunas personas les gusta LOT=true es porque así los mineros no tienen veto. El contraargumento, que ya has sugerido, es que los mineros no tienen un veto de todos modos, incluso si usamos LOT=false la actualización expirará después de un año, pero después de ese año podemos desplegar un nuevo mecanismo de actualización y un nuevo período de señalización. Esta vez tal vez usar LOT=true.

SP: O incluso mientras esto se lleva a cabo. Podrías esperar medio año con LOT=false y medio año después decir "Esto está tardando demasiado. Arriesguémonos un poco más y pongamos LOT=true". O bajar el umbral o alguna otra permutación que aumente ligeramente el riesgo pero también la probabilidad de activación.

AvW: Sí, tienes razón. Pero en realidad ese es también uno de los argumentos contra el uso de LOT=false. Los defensores de LOT=true dicen que, como tú has sugerido, podemos hacerlo después de 6 meses, pero hay otro grupo de usuarios que podría decir "No. Primero hay que esperar a que pase el año y luego volveremos a desplegar". Digamos que después de 6 meses Taproot no se ha activado. Ahora, de repente, se produce una nueva discusión entre la gente que quiere empezar a desplegar los clientes LOT=true de inmediato y los grupos de usuarios que quieren esperar hasta que termine el año. Se reintroduce la discusión que tenemos ahora, salvo que para entonces sólo tenemos 6 meses para resolverla. Es una especie de bomba de relojería.

SP: En realidad, no para resolverla. Si no se hace nada durante 6 meses, sólo queda una opción, que es volver a intentarlo con un nuevo bit de activación.

AvW: Pero entonces hay que acordar cuándo se va a hacer eso. ¿Van a hacerlo después de 6 meses o van a hacerlo más tarde? La gente podría no estar de acuerdo.

SP: Entonces volveríamos a estar como ahora, salvo que sabríamos un poco más porque ahora sabemos que los mineros no estaban señalizando.

AvW: Y no tienes mucho tiempo para resolverlo porque después de 6 meses podría pasar. Algún grupo de usuarios podría ejecutar LOT=true o....

SP: De lo que hablas aquí es de la posibilidad de, digamos, la anarquía en el sentido de que no hay consenso sobre cuándo activar esta cosa. Un grupo, creo que lo discutimos ampliamente en el tercer episodio, se pone muy agresivo y dice "No, vamos a activar esto antes". Entonces nadie sabe cuándo va a ocurrir.

AvW: Permítanme expresarlo de otra manera. Si ahora mismo decimos "Si después de 6 meses los mineros no han activado Taproot, entonces simplemente actualizaremos a los clientes de LOT=true", entonces los defensores de LOT=true dirán "Si ese es el plan de todos modos, hagámoslo ahora. Es mucho más fácil. ¿Por qué tenemos que hacerlo a medias?". Ese es el contraargumento del contraargumento.

SP: Lo entiendo. Pero, por supuesto, también está el escenario en el que nunca hacemos esto, Taproot simplemente no se activa. Depende de lo que la gente quiera. Hay algo que decir sobre el sesgo del statu quo en el que no se hace nada si es demasiado controvertido por la razón que sea. Hay otro caso secundario que es útil tener en cuenta. Puede haber una muy buena razón para cancelar Taproot. Puede haber un error que se revele después.

AvW: Te estás adelantando. Hay un montón de argumentos a favor de LOT=false. Un argumento es que ya hemos hecho LOT=false un montón de veces, el minero anterior activó las bifurcaciones suaves, y la mayoría de las veces salió bien. Sólo hubo una vez con SegWit en medio de una gran guerra, ahora no tenemos una gran guerra. No hay razón para cambiar lo que hemos estado haciendo con éxito hasta ahora. Ese es un argumento. El contraargumento sería, por ejemplo, "Sí, pero si eliges LOT=false ahora eso podría atraer la controversia en sí mismo. Podría utilizarse para abrir una brecha. Ahora mismo no estamos en guerra, pero podría provocar una guerra".

SP: No veo cómo ese argumento no se aplica a LOT=true. Cualquier cosa puede causar controversia.

AvW: Probablemente sea justo. Estoy de acuerdo con eso. El otro argumento a favor de LOT=false es que los mineros, y especialmente los pools de minería, ya han indicado que apoyan a Taproot, lo activarán. No es necesario hacer lo de LOT=true por lo que se ve. El tercer argumento es el que acabas de mencionar. Es posible que alguien encuentre un error con Taproot, un error de software o algún otro problema es posible. Si haces LOT=false es bastante fácil dejar que expire y los usuarios no tendrán que actualizar su software de nuevo.

SP: Lo único que hay es que habría que recomendar a los mineros que no instalen esa actualización. Vale la pena señalar, creo que lo señalamos en el Episodio 3, que la gente no siempre revisa las cosas muy pronto. Mucha gente ha revisado el código de Taproot, pero otros pueden no molestarse en revisarlo hasta que el código de activación esté ahí porque simplemente esperan al último minuto. No es inverosímil que alguien muy inteligente comience a revisar esto muy tarde, tal vez algún intercambio que esté a punto de desplegarlo.

AvW: Algo así ocurrió con [P2SH](https://bitcoinmagazine.com/articles/the-battle-for-p2sh-the-untold-story-of-the-first-bitcoin-war), el predecesor de P2SH. OP_EVAL estaba a punto de ser desplegado y entonces se encontró un bug bastante horrible.

SP: También lo hemos visto con ciertas altcoins, justo antes de su despliegue la gente encuentra días cero, ya sea porque fueron... o simplemente porque el código fue enviado con prisa y nadie lo revisó. Definitivamente siempre hay un riesgo, sea cual sea el mecanismo de soft fork que utilices, de que se descubra un bug en el último minuto. Si se tiene muy mala suerte, es demasiado tarde, se despliega y se necesita un hard fork para deshacerse de él, lo que sería muy, muy malo.

AvW: No creo que eso sea cierto. Hay otras formas de deshacerse de él.

SP: Dependiendo de cuál sea el fallo, se puede hacer una bifurcación suave.

AvW: Hay formas de arreglarlo incluso en ese caso. El otro contraargumento a ese punto sería: "Si no estamos seguros de que no tiene errores y no estamos seguros de que esta actualización es correcta, entonces no debería desplegarse de ninguna manera, LOT=true o LOT=false o lo que sea. Tenemos que estar seguros de eso de todos modos".

SP: Sí, pero como dije, algunas personas no revisarán algo hasta que sea inevitable.

AvW: I am just listing the arguments. Fourth argument against LOT=true is that LOT=true could feed into the perception that Bitcoin and especially Bitcoin Core developers control the protocol, have power of the protocol. They are shipping code and that necessarily becomes the new protocol rules in the case of Taproot.

SP: Podría haber una futura bifurcación suave en la que realmente nadie en la comunidad se preocupe por ello, sólo un puñado de desarrolladores de Bitcoin Core lo hacen, y lo imponen a la comunidad. Entonces se produciría un montón de caos. Lo bueno de tener al menos la señal de los mineros es que son parte de la comunidad y al menos están de acuerdo con ello. El problema es que no refleja lo que otras personas de la comunidad piensan al respecto. Sólo refleja lo que ellos piensan al respecto. Hay un montón de mecanismos. Hay discusiones en la lista de correo, se ve si la gente tiene problemas. También está la señalización de los mineros, que es una buena indicación de que la gente está contenta. Se ve que hay el mayor número posible de personas que consienten. Sería bueno que hubiera otros mecanismos, por supuesto.

AvW: El otro punto que los desarrolladores de Bitcoin Core, mientras deciden qué código incluyen en Bitcoin Core no deciden lo que los usuarios realmente terminan ejecutando.

SP: Puede que nadie lo descargue.

AvW: Exactamente. En realidad no tienen poder sobre la red. En ese sentido el argumento es false, pero podría alimentar la percepción de que sí lo tienen. Incluso esa percepción, si se puede evitar, es mejor. Ese es un argumento.

SP: Y el precedente. ¿Qué pasa si Bitcoin Core se ve comprometido en algún momento y envía una actualización y dice "Si no lo paras, se va a activar". Entonces es bueno que los mineros puedan decir "No, no lo creo".

AvW: Los usuarios también podrían decir eso al no descargarlo como has dicho. Ahora llegamos al quinto argumento. Aquí es donde la cosa se pone bastante compleja. El quinto argumento contra LOT=true es que podría causar todo tipo de inestabilidad en la red. Si sucede que el año se acaba y hay clientes LOT=true en la red es posible que se separen de la cadena principal y podría haber re-orgs. La gente podría perder dinero y los mineros podrían minar un bloque inválido y perder su recompensa de bloque y todo ese tipo de cosas. Los defensores de LOT=true argumentan que ese riesgo se mitiga mejor si la gente adopta LOT=true.

SP: Soy escéptico, eso suena muy circular. ¿Quizás sea útil explicar cómo son esos malos escenarios? Entonces otros pueden decidir si a) creen que vale la pena arriesgarse a esos malos escenarios y b) cómo hacerlos menos probables. Algo de eso es casi político. En la sociedad se discute si la gente debe tener armas o no, cuáles son los incentivos, y puede que nunca se resuelva. Pero podemos hablar de algunos de los mecanismos aquí.

AvW: Para ser claros, si de alguna manera hubiera un consenso completo en la red sobre LOT=true, todos los nodos ejecutan LOT=true, o todos los nodos ejecutan LOT=false, entonces creo que estaría totalmente bien. De cualquier manera.

SP: Sí. La ironía es, por supuesto, que si hay un consenso total y todo el mundo ejecuta LOT=true, entonces nunca se utilizará. En teoría tienes razón. No veo un escenario en el que los mineros digan "Estamos contentos con LOT=true pero deliberadamente no vamos a señalar y luego señalamos en el último momento".

AvW: Tienes razón, pero estamos divagando. La cuestión es que los escenarios realmente complicados surgen cuando algunas partes de la red tienen LOT=true, algunas partes de la red tienen LOT=false o algunas partes de la red no tienen ninguna de las dos cosas porque no se han actualizado. O una combinación de estos, la mitad de la red tiene LOT=true, la mitad de la red no tiene ninguno. Ahí es donde las cosas se complican mucho y Sjors, tú has pensado en ello, ¿qué piensas? Dime cuáles son los riesgos.

## El escenario de división de la cadena

SP: Pensé en estas cosas durante la debacle de SegWit2x, así como la debacle de UASF, que fueron similares en cierto modo, pero también muy diferentes debido a quién estaba explicando y si era un hard fork o un soft fork. Digamos que estás ejecutando la versión LOT=true de Bitcoin Core. La descargaste, tal vez fue liberada por Bitcoin Core o tal vez la autocompilaste, pero dice LOT=true. Usted quiere que Taproot se active. Pero el escenario aquí es que el resto del mundo, los mineros no están haciendo esto. Llega el día y ves un bloque, no está señalando correctamente, pero quieres que señale correctamente, así que dices "Este bloque es ahora inválido. No voy a aceptar este bloque". Voy a esperar hasta que otro minero venga con un bloque que sí cumpla mis criterios. Tal vez eso ocurra una vez cada 10 bloques, por ejemplo. Estás viendo nuevos bloques, pero están llegando muy, muy lentamente. Así que alguien te envía una transacción, quieres Bitcoin de alguien, te envían una transacción y esta transacción tiene una tarifa y probablemente va a estar mal. Digamos que estás recibiendo una transacción de alguien que está ejecutando un nodo con LOT=false. Están en una cadena que va diez veces más rápido que tú, en este estado intermedio. Sus bloques pueden estar apenas llenos, sus tarifas son bastante bajas, y tú la estás recibiendo. Pero tú estás en esta cadena más corta y de movimiento más lento, así que tu mempool está realmente lleno y tus bloques están completamente llenos, así que esa transacción probablemente no se confirmará en tu lado. Simplemente va a estar sentado en el mempool, que es una complejidad. En realidad es un escenario relativamente bueno porque no aceptas transacciones no confirmadas. Tendrás un desacuerdo con tu contraparte, dirás "No se ha confirmado" y ellos dirán "Se ha confirmado". Entonces por lo menos te darás cuenta de lo que está pasando, leerás sobre la guerra de LOT o lo que sea. Así que ese es un escenario. El otro escenario es cuando de alguna manera se confirma en tu lado y también se confirma en el otro lado. Eso es bastante bueno porque entonces estás a salvo de cualquier manera. Si se confirma en ambos lados, entonces, pase lo que pase en una futura reorganización, esa transacción está realmente en la cadena, tal vez en un bloque diferente. Otro escenario podría ser porque hay dos cadenas, una cadena corta y otra larga, pero son diferentes. Si usted está recibiendo monedas que se envían de una transacción de coinbase en un lado o en el otro, entonces no hay manera de que pueda ser válido en su lado. Esto también puede ser una característica, se llama la protección de repetición esencialmente. Recibes una transacción y ni siquiera la ves en tu mempool, llamas a la otra persona y dices "Esto no tiene sentido". Eso es bueno. Pero ahora, de repente, el mundo cambia de opinión y dice "No, sí queremos Taproot, sí queremos LOT=true, ahora somos incondicionales de LOT=true" y todos los mineros empiezan a minar encima de tu cadena más corta. Tu cadena corta se convierte en la cadena muy larga. En ese caso estás bastante contento en la mayoría de los escenarios que hemos discutido.

AvW: Me parece bien.

SP: Tenías una transacción que estaba tal vez en tu décimo bloque y en el otro lado estaba en el primer bloque. Sigue siendo tuya. Hubo algunas transacciones flotando en el mempool durante mucho tiempo, finalmente se confirman. Creo que estás bastante contento. Estábamos hablando del nodo LOT=true. Como usuario del nodo LOT=true, en estos escenarios estás contento. Tal vez no si pagas a alguien.

AvW: Estás empezando a hacer el caso de LOT=true Sjors, sé que no es tu intención pero estás haciendo un buen trabajo en ello.

SP: Para el usuario de nodo completo que sabe lo que está haciendo en general. Si eres un usuario de nodo completo y sabes lo que estás haciendo entonces creo que vas a estar bien en general. Esto no es tan malo. Ahora digamos que eres un usuario LOT=false y digamos que no sabes lo que estás haciendo. En el mismo escenario estás en la cadena más larga, estás recibiendo monedas de un exchange y has visto estas cabeceras por ahí para esta cadena más corta. Puede que los hayas visto, depende de si te llegan o no. Pero es una cadena más corta y es válida según tú porque es un conjunto de reglas más estricto. Estás bien, esta otra cadena tiene Taproot y tú probablemente no. Estás aceptando transacciones y eres un campista feliz pero de repente porque el mundo cambia todo desaparece de debajo de ti. Todas las transacciones que has visto confirmadas en un bloque están ahora de vuelta en el mempool y puede que se hayan gastado dos veces incluso.

AvW: Sí, la razón es que estamos hablando de una división de cadena que ha ocurrido. Tienes un nodo LOT=false pero en cualquier momento la cadena LOT=true se convierte en la cadena más larga, entonces tu nodo LOT=false seguiría aceptando esa cadena. La consideraría válida. Lo contrario no es cierto. Pero el nodo LOT=false siempre considerará válida la cadena LOT=true. Así que en tu escenario en el que estás usando Bitcoin en la cadena más larga, en la cadena LOT=false, estamos contentos, hemos recibido dinero, hemos hecho un duro día de trabajo y hemos recibido nuestro cheque al final, pagado en Bitcoin. Pensamos que estamos a salvo, recibimos un montón de confirmaciones pero de repente la cadena LOT=true se alarga lo que significa que tu nodo cambia a una cadena LOT=true. Ese dinero que recibiste en la cadena LOT=false que pensabas que era la cadena Bitcoin simplemente desaparece. Puf. Ese es el problema del que hablas.

SP: Exactamente.

AvW: Voy a añadir algo a esto muy brevemente. Creo que es un problema aún mayor para los nodos no actualizados.

SP: Estaba a punto de llegar a eso. Ahora estamos hablando de la gente de LOT=false. Todavía se podría decir "¿Por qué descargaste la versión LOT=false?" Porque no lo sabías. Ahora estamos hablando de un nodo sin actualizar. Para el nodo no actualizado no existe Taproot, así que no tiene preferencia por cuál de las cadenas, simplemente elegirá la más larga.

AvW: Es alguien en Corea, no sigue la discusión.

SP: No seamos malos con Corea.

AvW: Elige un país donde no hablen inglés.

SP: Corea del Norte.

AvW: Alguien no se mantiene al día en los foros de discusión de Bitcoin, tal vez no lee en inglés, realmente no le importa. Simplemente le gusta esto del Bitcoin, se descargó el software hace un par de años, puso su duro trabajo, le pagan y el dinero desaparece.

SP: O su nodo puede estar en un búnker nuclear en el que lo puso hace 5 años bajo 15 metros de hormigón, con un tapón de aire, y de alguna manera puede descargar bloques porque está viendo el satélite Blockstream o algo así, pero no se puede actualizar. Y no sabe de esta actualización. Lo que sería extraño si te gustan los búnkeres nucleares y los nodos completos. De todos modos alguien está ejecutando un nodo anticuado, en Bitcoin tenemos la política de que no tienes que actualizar, no es algo obligatorio. Debería ser seguro, o al menos relativamente seguro, ejecutar un nodo no actualizado. Estás recibiendo un salario, el mismo que la persona LOT=false, y de repente hay un gigantesco re-org que sale de la nada. No tienes ni idea de por qué la gente se molesta en reorganizar porque no sabes nada de este cambio de reglas.

AvW: Alguien no se mantiene al día en los foros de discusión de Bitcoin, tal vez no lee en inglés, realmente no le importa. Simplemente le gusta esto del Bitcoin, se descargó el software hace un par de años, puso su duro trabajo, le pagan y el dinero desaparece.

SP: O su nodo puede estar en un búnker nuclear en el que lo puso hace 5 años bajo 15 metros de hormigón, con un tapón de aire, y de alguna manera puede descargar bloques porque está viendo el satélite Blockstream o algo así, pero no se puede actualizar. Y no sabe de esta actualización. Lo que sería extraño si te gustan los búnkeres nucleares y los nodos completos. De todos modos alguien está ejecutando un nodo anticuado, en Bitcoin tenemos la política de que no tienes que actualizar, no es algo obligatorio. Debería ser seguro, o al menos relativamente seguro, ejecutar un nodo no actualizado. Estás recibiendo un salario, el mismo que la persona LOT=false, y de repente hay un gigantesco re-org que sale de la nada. No tienes ni idea de por qué la gente se molesta en reorganizar porque no sabes nada de este cambio de reglas.

AvW: No ves la diferencia.

SP: Y puf, tu sueldo ha desaparecido.

AvW: Eso es malo. Creo que ese es el peor escenario que nadie quiere.

SP: Sí. Esto se puede trasladar también a las personas que utilizan un software de cartera de hardware que no se ha actualizado, que utilizan nodos remotos o que utilizan nodos SPV que no comprueban las reglas sino que sólo comprueban el trabajo. Tendrán experiencias similares en las que, de repente, la cadena más larga cambia, por lo que su monedero SPV, que explicamos en un episodio anterior, su historia desaparece. Al menos para los nodos ligeros podrías hacer algo de victim shaming y decir "Deberías estar ejecutando un nodo completo. Si pasan cosas malas deberías haber ejecutado un nodo completo". Pero sigo pensando que eso no es una buena ingeniería de seguridad, decirle a la gente "Si no usas el cinturón de seguridad en la posición correcta el coche puede explotar". Pero al menos para el nodo completo no actualizado es un caso explícito que los Bitcoiners quieren apoyar. Quieren apoyar que la gente no se actualice y no pierda repentinamente sus monedas en una situación como esta. Por eso no soy una persona LOT=true.

## Evitar un escenario de ruptura en cadena

AvW: Eso es lo que quiero conseguir. Todo el mundo está de acuerdo, o al menos ambos estamos de acuerdo, y creo que la mayoría de la gente estaría de acuerdo en que este escenario que acabamos de pintar es horrible, no queremos eso. Así que la siguiente pregunta es ¿cómo evitar este escenario? Esa es también una de las cosas en las que las personas de LOT=true y LOT=false difieren en sus opiniones. Los defensores de LOT=false, como tú, argumentan en contra de LOT=true porque la ruptura de la cadena fue causada por LOT=true y, por lo tanto, si no queremos rupturas en cadena, no queremos LOT=true y lo que acabamos de describir no ocurrirá. El peor escenario es que no tengamos Taproot, simplemente expirará. Eso no es tan malo como que este pobre coreano pierda su honesto día de trabajo.

SP: Exactamente y puede que tengamos Taproot más adelante.

AvW: Los defensores de LOT=true argumentarán que Bitcoin es una red abierta y que cualquier peer puede ejecutar el software que quiera. Para bien o para mal LOT=true es algo que existe. Si queremos evitar una ruptura de la cadena, la mejor manera de evitarlo es asegurarse de que todo el mundo utiliza LOT=true o al menos la mayoría de los mineros se actualizan a tiempo y LOT=true es la mejor manera de asegurar eso. Conseguir una masa crítica para LOT=true es en realidad la opción más segura a pesar de que LOT=true también introdujo el riesgo. Si quiero hacer una analogía, es como si el mundo fuera un lugar más seguro sin armas nucleares, pero hay armas nucleares. Parece que es más seguro tener una en ese caso.

SP: Creo que esa analogía se rompe rápidamente, pero sí, entiendo la idea.

AvW: No es una analogía perfecta, estoy seguro. La cuestión es que LOT=true existe y ahora tenemos que lidiar con ello. Podría ser un mundo mejor, un lugar más seguro, si LOT=true no existiera, si los UASF no existieran. Pero existe y ahora tenemos que enfrentarnos a ese hecho. Se puede argumentar que asegurarse de que la bifurcación suave tenga éxito es en realidad la mejor manera de salvar a ese pobre coreano.

SP: Siempre soy muy escéptico con este tipo de teoría del juego porque suena retóricamente bien pero no estoy seguro de que sea realmente cierto. Uno de los problemas obvios es cómo sabes que has llegado a toda la comunidad Bitcoin. Hablamos de esta hipotética persona en este otro país que no está leyendo Twitter y Reddit, no tiene ni idea de que esto está pasando y mucho menos la mayoría de los usuarios de carteras ligeras. El número de personas que usan Bitcoin es mucho, mucho mayor que el número de personas que están siquiera remotamente interesadas en estas discusiones. Además, explicar el riesgo a esas personas, incluso si pudiéramos llegar a ellas, para explicarles por qué deberían actualizarse, es un reto bastante grande. En este episodio tratamos de explicar a grandes rasgos qué es lo que saldría mal si no se actualiza. No podemos decirles simplemente que deben actualizarse. Eso viola la idea de que hay que persuadir a la gente con argumentos y dejar que decidan lo que quieren hacer en lugar de decírselo basándose en la autoridad.

AvW: Ten en cuenta que al final todo esto se evita si la mayoría del poder de hash se actualiza. Con LOT=true en realidad cualquier mayoría estaría bien al final. Si los propios mineros utilizan LOT=true entonces seguro que consiguen la cadena más larga al final del año.

SP: La teoría del juego se reduce a decir que quieres convencer a los mineros de que lo hagan. Sin embargo, el problema es que si falla acabamos de explicar el desastre que ocurre. Entonces la pregunta es ¿cuál es ese riesgo? ¿Puedes poner un porcentaje en eso? ¿Se puede simular de algún modo el mundo y averiguar qué ocurre?

AvW: Yo no me decido a hacerlo. Veo argumentos convincentes en ambos lados. Al principio me inclinaba por lot=false, pero cuanto más lo pienso... El argumento es que si incluyes lot=true en Bitcoin Core entonces eso prácticamente garantiza que todo irá bien porque la mayoría económica casi seguro que lo ejecutará. Los intercambios y la mayoría de los usuarios.

SP: Ni siquiera estoy seguro de que eso sea cierto. Eso supone que esa mayoría económica se apresure a actualizar y no ignore las cosas.

AvW: Al menos dentro de un año.

SP: Es posible que haya empresas que estén ejecutando nodos de 3 o 4 años de antigüedad porque tienen 16 s\*\**coins diferentes. Incluso eso, yo no lo asumiría. Sabemos por la red en general que mucha gente no actualiza los nodos y un año es muy poco. No se puede saber por los nodos si son la mayoría económica o no. Puede que sean unos cuantos jugadores críticos los que se encarguen de ello.

AvW: Sí, no puedo estar seguro. No estoy seguro. Estoy especulando, estoy explicando el argumento. Pero lo contrario también es cierto, ahora que existe lot=true es casi seguro que algún grupo de usuarios lo ejecutará y eso introduce quizás mayores riesgos que si se incluyera en Core. Eso aumentaría las posibilidades de éxito de LOT=true, la mayoría actualizándose.

SP: Realmente depende de quién sea ese grupo. Porque si ese grupo son personas al azar que no son económicamente importantes, entonces ellos experimentan los problemas y nadie más se da cuenta de nada.

AvW: Eso es cierto. Si se trata de un grupo muy pequeño puede ser cierto, pero la cuestión es cuán pequeño o cuán grande tiene que ser ese grupo para que se convierta en un problema. Tienen una asimetría, esta ventaja, porque su cadena nunca puede ser reordenada, mientras que la cadena LOT=false puede ser reordenada.

SP: Pero su cadena puede no crecer nunca, así que eso también es un riesgo. No es una ventaja estricta.

AvW: Creo que es definitivamente una ventaja estricta.

SP: La ventaja es que no se puede volver a forjar. La desventaja es que tu cadena podría no crecer nunca. No sé cuál de las dos...

AvW: Probablemente crecería. Depende de lo grande que sea ese grupo de nuevo. Eso no es algo que podamos medir objetivamente. Supongo que a eso se reduce todo.

SP: Ni siquiera con carácter retroactivo podemos. Todavía no sabemos qué causó realmente la activación de SegWit, incluso cuatro años después. Eso te da una idea de lo difícil que es saber cuáles son realmente estas fuerzas.

AvW: Sí, en eso estamos de acuerdo. Es muy difícil saber de qué manera. Estoy indeciso al respecto.

SP: Lo más seguro es no hacer nada.

AvW: Ni siquiera eso. Todavía podría haber una minoría o incluso una mayoría que podría pasar.

SP: Otro experimento mental interesante es decir: "Siempre va a haber un grupo LOT=true para cualquier bifurcación suave. ¿Qué pasa con una bifurcación suave que no tiene el apoyo de la comunidad? ¿Qué pasa si un grupo arbitrario de personas decide llevar a cabo su propio soft fork porque quiere? Tal vez alguien quiere reducir la oferta de monedas. Poner la emisión de monedas a cero mañana o reducir el tamaño del bloque a 300 kilobytes". Podrían decir "Porque es un soft fork y porque yo corro un nodo LOT=true, podría haber otros que corran un LOT=true. Por lo tanto, debe activarse y todo el mundo debería ejecutar este nodo". Eso sería absurdo. Esta teoría del juego tiene un límite. Siempre se puede pensar en alguna bifurcación suave y en alguna pequeña comunidad que dirá esto y fracasará por completo. Tienes que estimar lo grande y lo potente que es esta cosa. Ni siquiera sé cuál es la métrica.

AvW: Pero también cómo de dañina es la actualización, porque yo diría que esa es la respuesta a tu punto. Si la mejora en sí se considera valiosa, a la gente le costará muy poco pasarse a la otra cadena, la que no se puede volver a forjar y que tiene la mejora que es valiosa. Esa es una muy buena razón para cambiar. Mientras que cambiar a una cadena, incluso si no se puede volver a forjar, que jode el límite de monedas o ese tipo de cosas, es un desincentivo mucho mayor y también un desincentivo para que los mineros cambien.

SP: Algunas personas podrían decir que un tamaño de bloque más pequeño es más seguro.

AvW: Son libres de bifurcarse, eso también es posible. Ni siquiera hemos hablado de eso, pero es posible que la división de la cadena sea duradera, que sea para siempre una cadena minoritaria LOT=true y una cadena mayoritaria LOT=false. Entonces tenemos la división de Bitcoin, Bitcoin Cash o algo así. Sólo tenemos dos monedas.

SP: Con la gran y temible espada de Damocles colgando encima.

AvW: Entonces quizá habría que incluir un punto de control en la cadena mayoritaria, lo que sería muy feo.

SP: Se podría idear algún tipo de bifurcación suave incompatible para evitar una reorganización en el futuro.

AvW: Vamos a trabajar hacia el final de este episodio.

SP: Creo que hemos cubierto muchos argumentos diferentes y hemos explicado que esto es bastante complicado.

AvW: ¿Qué cree que va a pasar? ¿Cómo cree que se desarrollará todo esto?

SP: Empecé a mirar un poco el meollo, [uno](https://github.com/bitcoin/bitcoin/pull/19573) de los pull requests que Luke Dashjr abrió para implementar BIP 8 en general, no específicamente para Taproot creo. Ya hay complejidad con esto de LOT=true comprometido porque hay que pensar en cómo debe comportarse la red peer-to-peer. Desde un principio de mínima acción, lo que es el menor trabajo para los desarrolladores, establecer LOT a false probablemente resulta en un código más fácil que se fusionará antes. E incluso si Luke es como "Sólo haré esto si se establece como true", entonces alguien más hará una solicitud de extracción que lo establece como false y se fusiona antes. Creo que desde un punto de vista de lo que sucede cuando la gente perezosa, quiero decir perezosa en la forma más respetuosa, ¿cuál es el camino de menor resistencia? Probablemente sea LOT=false, sólo desde el punto de vista de la ingeniería.

AvW: Así que LOT=false en Bitcoin Core es lo que se esperaría en ese caso.

SP: Sí. Y alguien más implementaría LOT=true.

AvW: En algún cliente alternativo seguramente.

SP: Sí. Y eso podría no tener revisión de código.

AvW: Es sólo una configuración de parámetros, ¿verdad?

SP: No, es más complicado porque cómo va a interactuar con sus pares y qué va a hacer cuando haya una división de la cadena, etc.

AvW: ¿Qué opinas de este escenario que tampoco se implementa en Bitcoin Core? ¿Ves que eso ocurra?

SP: Ninguna de las dos cosas. ¿LOT=null?

AvW: Simplemente no hay mecanismo de activación porque no hay consenso para uno.

SP: No, creo que estará bien. No puedo predecir el futuro, pero creo que un LOT=false no será tan objetado como algunos podrían pensar.

AvW: Entonces ya veremos, supongo.

SP: Sí, ya veremos. Puede que esta sea la cosa más tonta que he dicho nunca.

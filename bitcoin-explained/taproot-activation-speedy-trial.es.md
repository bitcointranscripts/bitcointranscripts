---
title: Taproot Activación con Speedy Trial
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
  - soft-fork-activation
date: 2021-03-12
episode: 31
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
media: https://www.youtube.com/watch?v=oCPrjaw3YVI
aliases:
  - /es/bitcoin-magazine/2021-03-12-taproot-activation-speedy-trial
---
Propuesta Speedy Trial: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-March/018583.html
## Introducción

Aaron van Wirdum (AvW): En directo desde Utrecht este es el van Wirdum Sjorsnado. Sjors, ¿cuál es tu juego de palabras de la semana?

Sjors Provoost (SP): En realidad te pedí un juego de palabras y me dijiste "Corta, reedita. Vamos a hacerlo de nuevo". No tengo un juego de palabras esta semana.

AvW: Los juegos de palabras son lo tuyo.

SP: La última vez intentamos esto de LOT.

AvW: Sjors, vamos a hablar mucho esta semana.

SP: Nos van a bloquear por esto.

AvW: Hablamos mucho [hace dos semanas](https://diyhpl.us/wiki/transcripts/bitcoin-magazine/2021-02-26-taproot-activation-lockinontimeout/). LOT fue el parámetro que discutimos hace dos semanas, LOT=true, LOT=false, sobre la activación de Taproot. Llevamos dos semanas y ahora parece que la comunidad está llegando a un cierto consenso sobre una solución de activación llamada "Speedy Trial". Eso es lo que vamos a discutir hoy.

SP: Así es.

## Propuesta de Speedy Trial

Propuesta de Speedy Trial: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-March/018583.html

Propuesta de calendario: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-March/018594.html

AvW: ¿Empezamos con Speedy Trial, qué es Speedy Trial Sjors?

SP: Creo que es una buena idea. Con las propuestas de las que hablamos la última vez para activar Taproot, básicamente Bitcoin Core liberaría algún software, tal vez en abril o algo así, y luego los mineros empezarían a señalar usando ese software en, creo, agosto o algo así. Entonces pueden señalar durante un año y al final del año todo termina.

AvW: Eso era LOT=true o LOT=false. El debate era sobre si debía terminar con la señalización forzosa o no. Eso es lo de LOT=true, LOT=false.

SP: Lo que hay que tener en cuenta es que la primera señalización, pasaría un tiempo antes de que empiece a suceder. Hasta ese momento realmente no sabemos esencialmente. Lo que propone el Speedy Trial es decir "En lugar de discutir si va a haber o no señalización y tener muchas discusiones al respecto, vamos a probarlo muy rápidamente". En lugar de eso, habría un lanzamiento tal vez alrededor de abril, por supuesto no hay nadie a cargo de los plazos reales. En ese caso la señalización [comenzaría](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-March/018594.html) mucho antes, no estoy del todo seguro de cuándo, tal vez en mayo o bastante temprano. La señalización sólo duraría 3 meses. Al final de los 3 meses se abandonaría.

AvW: Terminaría en LOT=false básicamente.

SP: Sí. Es el equivalente a LOT=false o como solía ser con las horquillas blandas. Señala pero sólo durante un par de meses.

AvW: ¿Si no se activa en esos meses por la potencia de hash, que probablemente será del 90 por ciento de la potencia de hash? Se necesitará un 90% de potencia de hachís para activar Taproot. Si no lo hace, la propuesta caduca y cuando caduque podremos seguir discutiendo sobre cómo activar Taproot. ¿O si se activa entonces qué pasa?

SP: La cuestión es que como todavía se quiere dar a los mineros el tiempo suficiente para actualizar realmente su software, las reglas reales de Taproot no entrarán en vigor hasta septiembre o agosto.

AvW: Mineros y usuarios reales de Bitcoin.

SP: Sí. Se quiere dar a todo el mundo tiempo suficiente para actualizarse. La idea es que comencemos la señalización muy rápidamente. Además, los mineros pueden señalar sin instalar el software. Una vez que se haya alcanzado el umbral de señalización, la bifurcación suave será inamovible. Va a suceder, al menos si la gente ejecuta los nodos completos. Entonces todavía hay tiempo para que la gente se actualice y para que los mineros realmente se actualicen y ejecuten ese nuevo software en lugar de simplemente señalarlo. Podrían ejecutar ese software, pero podrían no hacerlo. Por eso está bien lanzarlo un poco antes.

AvW: ¿Deberían ejecutar realmente el software si están señalando?

AvW: Por ahora, para recapitular muy brevemente, Speedy Trial significa liberar el software bastante rápido y rápidamente después de ser liberado iniciar el período de señalización durante 3 meses, que es relativamente corto para un período de señalización. Ver si el 90 por ciento de los mineros están de acuerdo, si lo hacen Taproot se activa 6 meses después de la liberación inicial del software. Si el 90 por ciento de los mineros no se activa en 3 meses la propuesta expira y podemos continuar la discusión sobre cómo activar Taproot.

SP: Volvemos entonces a donde estábamos hace unas semanas pero con más datos.

## La evolución de la propuesta de Speedy Trial

AvW: Exactamente. Quiero referirme brevemente a cómo hemos llegado hasta aquí. Discutimos todo el asunto de LOT=true y LOT=false y parecía haber un bloqueo. Algunos no querían LOT=true, otros no querían LOT=false y entonces entró en juego una tercera propuesta. No era nueva, pero no era una parte importante de la discusión, un simple día de la bandera. Un simple día de bandera habría significado que el código de Bitcoin Core habría incluido una fecha en el futuro o una altura de bloque en el futuro, momento en el que la actualización de Taproot se activaría independientemente de la potencia de hash hasta ese momento.

SP: Me parece una idea aún peor. Cuando hay mucho debate la gente empieza a proponer cosas.

AvW: Creo que la razón por la que hemos llegado a esta situación de estancamiento en la que la gente tiene ideas muy diferentes tiene mucho que ver con lo que ocurrió durante la actualización de SegWit. Ya lo hemos discutido antes, pero la gente tiene ideas muy diferentes de lo que realmente ocurrió. Algunas personas creen firmemente que los usuarios mostraron sus músculos. Los usuarios reclamaron su soberanía, los usuarios reclamaron el protocolo y básicamente forzaron a los mineros a activar la actualización de SegWit. Fue una gran victoria para los usuarios de Bitcoin. Por otro lado, otras personas creen firmemente que Bitcoin se acercó a un completo desastre con una red fracturada y gente perdiendo dinero, un gran desastre. Al primer grupo de gente le gusta mucho hacer un UASF de nuevo o empezar con LOT=false y cambiar a LOT=true o quizás sólo empezar con LOT=true. La gente que piensa que fue un gran lío, prefiere usar un día de bandera esta vez. Bonito y seguro en cierto modo, utilizar un día de bandera, nada de esta señalización de los mineros, los mineros no pueden ser obligados a señalar y todo eso. Estos diferentes puntos de vista sobre lo que realmente sucedió hace un par de años ahora significa que la gente no puede realmente estar de acuerdo en una nueva propuesta de activación. Después de muchas discusiones, todas las facciones estaban dispuestas a llegar a un acuerdo sobre el Speedy Trial, aunque a nadie le gusta realmente por un par de razones en las que entraremos. La gente de la UASF está de acuerdo con el Speedy Trial porque no se interpone en el camino de la UASF. Si el Speedy Trial fracasa, seguirán haciendo el UASF el año que viene. La gente del día de la bandera está de acuerdo porque los 3 meses no permiten una ventana suficientemente grande para hacer el UASF probablemente. La gente del UASF ha dicho que eso es demasiado rápido y que hagamos el Speedy Trial.

SP: También está el LOT=false, hagamos las bifurcaciones suaves de la forma en que las hemos hecho antes, en las que simplemente pueden expirar. Un grupo de personas que seguía trabajando en silencio en el código real que podría hacer eso. Sólo a partir de las listas de correo y de Twitter es difícil calibrar lo que realmente está pasando. Es una escala de tiempo muy corta.

AvW: La gente de LOT=false, esto es básicamente LOT=false sólo que en una escala de tiempo más corta. Todo el mundo está dispuesto a aceptarlo, aunque a nadie le guste.

SP: Desde el punto de vista que estoy viendo, realmente estoy mirando el código que se está escribiendo, lo que he notado es que una vez que el Speedy Trial salió más gente salió de la carpintería y comenzó a escribir el código que realmente podría hacer esto. Mientras que antes era sobre todo Luke, creo que escribiendo ese [pull request](https://github.com/bitcoin/bitcoin/pull/19573).

AvW: ¿BIP 8?

SP: Sí, el BIP 8. Supongo que podemos entrar en los detalles técnicos, lo que estoy tratando de decir es que una cosa que muestra que el Speedy Trial parece una buena idea es que hay más desarrolladores de diferentes ángulos cooperando en él y haciendo las cosas un poco más rápido. Cuando hay algún desacuerdo, la gente empieza a procrastinar, a no revisar las cosas o a no escribirlas. Eso es un vago indicador de que esto parece estar bien. La gente está trabajando en ello rápidamente y está progresando, así que eso es bueno.

AvW: ¿Algún detalle técnico en el que quieras entrar?

## Diferentes enfoques de la aplicación de Speedy Trial

Intercambio de información sobre la altura de los bloques frente a la combinación de la altura de los bloques y el MTP: https://bitcoin.stackexchange.com/questions/103854/should-block-height-or-mtp-or-a-mixture-of-both-be-used-in-a-soft-fork-activatio/

PR 21377 sobre la implementación de una combinación de altura de bloque y MTP: https://github.com/bitcoin/bitcoin/pull/21377

PR 21392 implementando la altura del bloque: https://github.com/bitcoin/bitcoin/pull/21392

SP: La idea del Speedy Trial puede implementarse de dos maneras diferentes. Se puede utilizar el sistema BIP 9 que ya tenemos. El argumento para eso sería que es mucho menos código porque ya funciona. Es sólo para 3 meses, así que ¿por qué no utilizar el antiguo código del BIP 9?

AvW: ¿El BIP 9 utiliza fechas en el futuro?

SP: Sí. Se puede saber cuándo podría empezar la señalización, cuándo se agota la señalización. Hay algunos casos extremos molestos en los que si se termina justo en la fecha límite pero luego hay una reorganización y termina justo antes de la fecha límite, el dinero de la gente podría perderse si intentan entrar en el primer bloque de Taproot. Esto es difícil de explicar a la gente.

AvW: La cuestión es que la señalización se produce por periodo de dificultad de los bloques de 2016. Al menos hasta ahora el 95% de los bloques necesitaban señalización de apoyo. Pero estos dos periodos de bloques, no se ajustan a fechas exactas ni nada por el estilo. Simplemente ocurren. Aunque el periodo de señalización sí empieza y termina en fechas concretas, por eso se pueden dar casos extraños.

SP: Hagamos un ejemplo, es divertido ilustrarlo. Digamos que la fecha límite de esta bifurcación suave es el 1 de septiembre, elige una fecha, para la señalización. El 1 de septiembre a medianoche UTC. Un minero mina el bloque número 2016 o algún múltiplo de 2016, que es cuando termina la votación. Minan este bloque un segundo antes de la medianoche UTC. Señalan "Sí". Todos los que ven ese bloque dicen "Ok tenemos el 95% o lo que sea y justo antes de la medianoche Taproot está activo". Tienen este script automático que dice "Ahora voy a poner todos mis ahorros en una dirección de Taproot porque quiero estar en el primer bloque y me siento imprudente, me encanta ser imprudente". Luego hay otro minero que mina 2 segundos después porque no vio ese bloque reciente. Puede haber bloques rancios. Su bloque llega un segundo después de la medianoche. También vota positivo, pero es demasiado tarde, por lo que la bifurcación suave no se activa porque la señalización no se hizo antes de la medianoche, la fecha límite. Esa es la sutileza que se obtiene con el BIP 9. Normalmente no es un problema, pero es difícil explicar estos casos extremos a la gente.

AvW: ¿Es un problema mayor también con periodos de señalización más cortos?

SP: Sí, por supuesto. Si hay un periodo de señalización más largo, es menos probable que la señal llegue al final de un periodo.

AvW: El umbral, ¿creía que iba a ser del 90% esta vez?

SP: Eso es algo distinto. Primero vamos a hablar, independientemente del umbral, de estos dos mecanismos. Uno se basa en el tiempo, es el BIP 9, fácil porque ya tenemos el código para ello, el inconveniente son todas estas cosas raras que tienes que explicar a la gente. Hoy en día las bifurcaciones suaves en Bitcoin son tan importantes, tal vez la CNN quiera escribir sobre ello, es agradable si realmente puedes explicarlo sin sonar como un completo nerd. Pero la alternativa es decir "Vamos a utilizar este nuevo BIP 8 que se propuso de todos modos y utiliza la altura". Ignoramos todo lo de LOT=true pero lo de la altura es muy útil. Entonces es mucho más sencillo. A partir de esta altura del bloque es cuando termina la señalización. Esa altura está siempre en el límite de estos periodos de retargeting. Eso es más fácil de razonar. Estás diciendo: "Si la señalización se alcanza en el bloque 700.321, entonces sucede, o no sucede". Si hay un reorg, que por cierto podría seguir siendo un problema, podría haber un reorg a la misma altura. Pero entonces la diferencia sería que se activaría porque acabamos de hacer precisamente el 95%. Entonces hay una reorganización y ese minero vota no y entonces no se activa. Es un caso límite.

AvW: Eso también es cierto con el PIF 9. Si se elimina un caso límite, se tiene un caso límite menos, lo que es mejor.

SP: Correcto, con el BIP 9 podrías tener el mismo escenario, exactamente un voto, si es justo en el borde un voto minero. Pero el problema mucho mayor con el BIP 9 es que si la hora del bloque es 1 segundo después de la medianoche o antes esto importa. Incluso si están muy por encima del umbral. Pueden tener el 99,999% pero ese último bloque llega demasiado tarde y por tanto todo el periodo queda descalificado. En unas elecciones se miran todos los votos. Se dice: "Tiene un 97% de apoyo, va a pasar" y entonces ese último bloque llega demasiado tarde y no pasa. Es difícil de explicar, pero no tenemos este problema con la activación basada en la altura.

AvW: Supongo que la mayor desventaja de usar BIP 8 es que supone un cambio mayor en cuanto a código.

SP: Sí, pero ayer revisé ese código y escribí algunas pruebas para él. Andrew Chow y Luke Dashjr ya han implementado gran parte de él. Ya ha sido revisado por la gente. En realidad no está tan mal. Parecen 50 líneas de código. Sin embargo, si hay un error en él es muy, muy malo. Sólo porque se trata de unas pocas líneas de código, podría ser más seguro utilizar algo que ya existe. Pero no estoy terriblemente preocupado por ello.

## El umbral de potencia del hash

AvW: Luego está el umbral de potencia de hash. ¿Es 90 o 95?

SP: Lo que se está implementando ahora en Bitcoin Core es el mecanismo general. Está diciendo "Para cualquier soft fork que se llame Speedy Trial se podría, por ejemplo, utilizar el 90 por ciento". Pero para Taproot el código para Taproot en Bitcoin Core, sólo dice "Nunca se activa". Esa es la forma de indicar que este soft fork está en el código pero no va a ocurrir todavía. Estos números son arbitrarios. El código soportará el 70 por ciento o el 95 por ciento, siempre que no sea un número imaginario o más del 100 por ciento.

AvW: Cabe señalar que al final siempre es el 51 por ciento de forma efectiva porque el 51 por ciento de los mineros siempre puede decidir dejar huérfanos los bloques que no son de señalización.

SP: Y crear un lío. Pero podrían hacerlo.

AvW: Hay que tener en cuenta que los mineros siempre pueden hacer eso si lo deciden.

SP: Pero el principio general que se está construyendo ahora es que al menos podríamos hacer un umbral ligeramente más bajo. Puede que todavía se discuta si eso es seguro o no.

AvW: ¿Todavía no está decidido? ¿Por lo que usted sabe, 90 o 95?

SP: No lo creo. Podríamos tener algunos argumentos a favor, pero ya lo veremos en la sección de riesgos.

AvW: O podemos mencionar muy brevemente que el beneficio de tener el umbral más alto es un menor riesgo de bloqueos huérfanos después de la activación. Esa es la razón principal.

SP: Pero como estamos haciendo una activación retardada, pasa mucho tiempo entre la señalización y la activación, mientras que normalmente se señala y se activa inmediatamente, o al menos en dos semanas. Ahora puede tardar mucho, mucho más. Eso significa que los mineros tienen más tiempo para actualizar. Hay un poco menos de riesgo de orfandad incluso si tienes un umbral de señalización más bajo.

## Activación retardada

AvW: Cierto. Creo que ese era el tercer punto al que querías llegar de todos modos. La activación retardada.

SP: Lo que ocurre normalmente es que se cuentan los votos en el último periodo de dificultad. Si supera el umbral, el estado de la bifurcación suave pasa de [STARTED](https://github.com/bitcoin/bips/blob/master/bip-0008.mediawiki#state-transitions), es decir, lo sabemos y lo estamos contando, a LOCKED_IN. El estado LOCKED_IN durará normalmente 2 semanas o un periodo de retargeting, y entonces las reglas entrarán realmente en vigor. Lo que ocurre con el Speedy Trial, la parte de activación retardada, es que este estado LOCKED_IN durará mucho más tiempo. Puede durar meses. Está BLOQUEADO_IN durante meses y luego las reglas entran realmente en vigor. Este cambio es sólo dos líneas de código que es bastante agradable.

## Inconvenientes y riesgos de esta propuesta

AvW: Bien, ¿pasamos a algunos de los inconvenientes de esta propuesta?

SP: Algunos de los riesgos. El primero lo hemos mencionado brevemente. Debido a que esta cosa se despliega con bastante rapidez y a que está muy claro que la activación de las reglas se retrasa, existe un incentivo para que los mineros se limiten a dar señales en lugar de instalar realmente el código. Entonces podrían procrastinar la instalación real del software. Eso está bien, a menos que lo pospongan tanto que se olviden de aplicar realmente las reglas.

AvW: Lo cual me parece bastante mal, Sjors.

SP: Sí. Eso es malo, estoy de acuerdo. Siempre es posible que los mineros se limiten a dar señales y no apliquen realmente las reglas. Este riesgo existe con cualquier despliegue de soft fork.

AvW: Sí, los mineros siempre pueden hacer señales, falsas señales. Eso ha ocurrido en el pasado. Hemos visto señales falsas. En la bifurcación suave del BIP 66 nos dimos cuenta más tarde de que los mineros estaban emitiendo señales falsas porque vimos grandes reorganizaciones en la red. Eso es algo que definitivamente queremos evitar.

SP: Creo que lo hemos explicado brevemente antes, pero podemos volver a explicarlo. Bitcoin Core, si lo usas para crear tus bloques como minero, hay algunos mecanismos de seguridad para asegurar que no creas un bloque que no es válido. Sin embargo, si otro minero crea un bloque que no es válido, usted minará encima de él. Entonces tienes un problema porque los nodos completos que están aplicando Taproot rechazarán tu bloque. Presumiblemente la mayoría del ecosistema, si esta señalización funciona, se actualizará. Entonces te metes en esta situación muy aterradora en la que realmente esperas que sea verdad. No una parte masiva de la economía es demasiado perezosa para actualizar y obtienes un completo desastre.

AvW: Sí, correcto.

SP: Creo que el término del que hablamos es la idea de un troll. Podrías tener un usuario troll. Digamos que soy un usuario malvado y voy a crear una transacción que parece una transacción de Taproot pero que en realidad no es válida según las reglas de Taproot. La forma en que funciona, el mecanismo en Bitcoin para hacer bifurcaciones suaves es que usted tiene este número de versión en su transacción SegWit. Dices "Esta es una transacción SegWit versión 1". Los nodos saben que cuando ves una versión SegWit superior que no conoces...

AvW: ¿Versión Taproot?

SP: Versión de SegWit. La versión actual de SegWit es la versión 0 porque somos unos frikis. Si ves una transacción de la versión SegWit con 1 o superior asumes que cualquiera puede gastar ese dinero. Eso significa que si alguien está gastando desde esa dirección no te importa. No consideras el bloque inválido como un nodo antiguo. Pero un nodo que conozca la versión comprobará las reglas. Lo que podrías hacer como troll es crear una firma Schnorr rota, por ejemplo. Tomas una firma Schnorr y cambias un byte. Entonces si eso es visto por un nodo antiguo dice "Esto es SegWit versión 1. No sé lo que es. Está bien. Cualquiera puede pasar esto así que no voy a comprobar la firma". Pero los nodos Taproot dirán "Hey, espera un minuto. Esa es una firma inválida, por lo tanto es un bloque inválido". Y tenemos un problema. Hay un mecanismo de protección para que los mineros normales no minen transacciones SegWit que no conocen. No minarán la versión 1 de SegWit si no están actualizados.

AvW: ¿No ocurre también que los nodos normales simplemente no reenviarán la transacción a otros nodos?

SP: Así es, es otro mecanismo de seguridad.

AvW: Hay dos mecanismos de seguridad.

SP: Básicamente dicen "Oye, otro nodo, no creo que quieras regalar tu dinero". O bien "Estás intentando hacer algo súper sofisticado que no entiendo", algo que se llama normalidad. Si estás haciendo algo que no es estándar no voy a transmitirlo. Eso no es una norma de consenso. Es importante. Significa que puedes compilar tu nodo para retransmitir esas cosas y puedes compilar tu minero para minar esas cosas, pero es un arma de pie si no sabes lo que estás haciendo. Pero no está en contra del consenso. Sin embargo, cuando una transacción está en un bloque, entonces estás tratando con reglas de consenso. Eso significa de nuevo que los nodos antiguos lo mirarán y dirán "no me importa. No voy a comprobar la firma porque es una versión superior a la que conozco". Pero los nodos actualizados dirán "Eh, espera un momento. Este bloque contiene una transacción que no es válida. Este bloque no es válido". Y así un usuario troll no tiene realmente la oportunidad de hacer mucho daño.

AvW: Porque la transacción no llegará a través de la red peer-to-peer e incluso si lo hace sólo llegaría a los mineros que aún la rechazarán. Un usuario troll probablemente no pueda hacer mucho daño.

SP: Nuestro ejemplo del troll de un usuario que intercambia un byte en una firma Schnorr, intenta enviar esta transacción, la envía a un nodo que está actualizado. Ese nodo dirá "Eso no es válido, vete. Voy a banearte ahora". Tal vez no lo prohíba, pero definitivamente se enfadará. Pero si lo envía a un nodo que no está actualizado, ese nodo dirá "No sé nada de esta nueva versión de SegWit tuya. Vete. No me envíes estas cosas modernas. Soy de la vieja escuela. Envíame cosas viejas". Así que la transacción no va a ninguna parte, pero tal vez de alguna manera termina con un minero. Entonces el minero dice "No voy a minar esta cosa que no conozco. Es peligroso porque podría perder todo mi dinero". Sin embargo, podrías tener un minero troll. Eso sería un trolling muy, muy caro, pero tenemos multimillonarios en este ecosistema. Si minan un bloque que no es válido les va a costar unos cuantos cientos de miles de euros, creo que a los precios actuales, quizá incluso más.

AvW: Sí, 300.000 y pico.

SP: Si tienes 300.000 euros para quemar, podrías hacer un bloque así y desafiar al ecosistema, decir "Oye, aquí tienes un bloque. Déjame ver si lo verificas". Entonces, si ese bloque va a nodos que están actualizados, estos lo rechazarán. Si ese bloque va a nodos que no están actualizados, está bien, es aceptado. Pero si alguien mina sobre él, si ese minero no se ha actualizado no lo comprobará, construirá sobre él. Al final, el ecosistema probablemente rechazará toda la cadena y se convertirá en un desastre. Entonces realmente, realmente, realmente quieres que una gran mayoría de mineros compruebe los bloques, no sólo minar a ciegas. En general, ya hay problemas con los mineros que minan a ciegas encima de otros mineros, incluso durante unos segundos, por razones económicas.

AvW: Esa fue una larga tangente sobre los problemas de la falsa señalización. ¿Todo esto sólo ocurriría si los mineros hicieran señales falsas?

SP: Para que quede claro, la señalización falsa no es un acto malintencionado, sólo es algo perezoso y conveniente. Dices "No te preocupes, haré mis deberes. Te enviaré ese memorándum a tiempo, no te preocupes".

AvW: Todavía no me he actualizado, pero lo haré. Ese es el riesgo de la falsa señalización.

SP: También podría ser deliberado, pero tendría que ser una conspiración bastante grande.

AvW: Otra preocupación, un riesgo que se ha mencionado es que el uso de LOT=false en general podría ayudar a los usuarios a lanzar un UASF porque podrían ejecutar un cliente UASF con LOT=true e incentivar a los mineros a hacer señales, como acabamos de mencionar. Eso no sólo significaría que ellos mismos se bifurcarían a su propia bifurcación suave, sino que básicamente activarían una bifurcación suave para toda la economía. Eso no es un problema en sí mismo, pero algunas personas lo consideran un problema si los usuarios son incentivados a intentar un UASF. ¿Entiende usted ese problema?

SP: Si optamos por este enfoque del BIP 8, si pasamos a utilizar la altura de los bloques en lugar de las marcas de tiempo...

AvW: O el día de la bandera.

SP: El Speedy Trial no utiliza un día de bandera.

AvW: Lo sé. Lo que digo es que si se hace un día de bandera no se puede hacer un UASF que desencadene otra cosa.

SP: Tal vez se pueda, ¿por qué no?

AvW: ¿Qué activaría?

SP: Hay un día de bandera por ahí, pero se despliega un software que requiere señalización.

AvW: Eso es lo que ejecutaría la gente de la UASF.

SP: Pueden ejecutarlo de todos modos. Incluso si hay un día de bandera, pueden decidir ejecutar un software que requiera señalización, aunque probablemente nadie lo haría. Pero podrían hacerlo.

AvW: Absolutamente, pero no pueden "cooptar" para llamarlo que LOT=nodos falsos si sólo hay un día de bandera por ahí.

SP: Eso es cierto. Exigirían la señalización, pero los nodos del día de la bandera que están ahí fuera serían como "no sé por qué no aceptan estos bloques. No hay señal, no hay nada que activar. Sólo está mi día de bandera y voy a esperar a mi día de bandera".

AvW: No quiero meterme demasiado en la maleza, pero si no hay nodos LOT=false para "cooptar", entonces los mineros podrían simplemente emitir una señal falsa. Los nodos UASF están activando Taproot pero el resto de la red todavía no tiene Taproot activado. Si los nodos UASF envían monedas a una dirección Taproot van a perder sus monedas al menos en el resto de la red.

SP: Y no conseguirían esa ventaja de reorganización que creen tener. Esto parece aún más complicado que lo que hablamos hace dos semanas.

AvW: Sí, por eso mencioné que me estoy metiendo un poco en la maleza ahora. Pero, ¿entiendes el problema?

SP: ¿Es un argumento a favor o en contra del día de la bandera?

AvW: Depende de tu perspectiva, Sjors.

SP: La de alguien que no quiere que Bitcoin implosione en un gran incendio y que le gustaría que se activara Taproot.

AvW: Si no te gustan los UASF, si no quieres que la gente haga UASF, entonces tampoco querrás que haya nodos LOT=false.

SP: Sí, vale, estás diciendo "si realmente quieres que no existan los UASF". No estoy terriblemente preocupado por la existencia de estas cosas. De lo que hablé hace 2 semanas, no voy a contribuir a ellas probablemente.

AvW: Sólo quería mencionar que ese es un argumento contra LOT=false que he visto por ahí. Tampoco es un argumento con el que yo esté de acuerdo, pero he visto el argumento.

SP: Lo que está diciendo exactamente es que es un argumento para no utilizar la señalización, pero sí un día de bandera.

AvW: Sí. Incluso el Speedy Trial utiliza la señalización. Aunque es más corto, puede ser lo suficientemente largo como para lanzar un UASF contra él, por ejemplo.

SP: Y es compatible con eso. Como utiliza la señalización, es perfectamente compatible con que alguien despliegue un sistema LOT=true y haga mucho ruido al respecto. Pero supongo que en este caso, incluso los defensores más firmes de LOT=true, uno de ellos al menos, argumentaron que sería completamente imprudente hacer eso.

AvW: Ahora mismo no hay ningún defensor de la UASF que piense que es una buena idea. Que yo sepa, al menos.

SP: Hasta ahora no los hay. Pero ya hablamos, en septiembre creo, de esta teoría de los vaqueros. Estoy seguro de que hay alguien por ahí que intentará un UASF incluso en el Speedy Trial.

## ¿Speedy Trial como plantilla para futuras activaciones de soft fork?

AvW: No se puede excluir la posibilidad al menos. Hay otro argumento en contra del Speedy Trial, encuentro este argumento bastante convincente en realidad, que es que salimos de 2017 con mucha incertidumbre. Acabo de mencionar la incertidumbre al principio de este episodio, parte de ella al menos. Algunos pensaron que la UASF fue un gran éxito, otros pensaron que fue una imprudencia. Ambas cosas son parcialmente ciertas, hay verdad en ambas. Ahora tenemos un soft fork, Taproot, que parece gustar a todo el mundo, a los usuarios, a los desarrolladores, a los mineros, a todos. Lo único que tenemos que hacer es actualizarlo. Ahora podría ser una muy buena oportunidad para limpiar el desorden de 2017 en cierto modo. Acordar qué son exactamente las bifurcaciones suaves, cuál es la mejor manera de desplegar una bifurcación suave y luego usar eso. De esta manera se convierte en una plantilla que podemos utilizar en tiempos más polémicos en el futuro cuando tal vez hay otra guerra civil en marcha o hay más FUD siendo lanzado en Bitcoin. Parece que estamos en aguas tranquilas ahora mismo. Tal vez este sea un buen momento para hacerlo bien, lo que nos ayudará a avanzar en el futuro. Mientras que Speedy Trial, nadie piensa que este sea realmente el camino correcto. Está bien, necesitamos algo así que hagámoslo. Podría decirse que es una patada a la lata de la discusión realmente grande que necesitamos tener en el camino.

SP: Sí, tal vez. Un escenario que podría ver es que el Speedy Trial pase, se active con éxito y el despliegue de Taproot pase y todo esté bien. Entonces creo que eso eliminaría ese trauma. La siguiente bifurcación suave se haría en el bonito y tradicional LOT=false BIP 8. Lanzaremos algo y varios meses después los mineros empezarán a dar señales y se activará. Así que tal vez sea una forma de superar el trauma.

AvW: ¿Crees que es una forma de superar el trastorno de estrés postraumático? Que todo el mundo vea que los mineros pueden activarse realmente.

SP: Puede que sea bueno deshacerse de esa tensión, porque el inconveniente de liberar el mecanismo regular, digamos BIP 8 LOT=false, es que van a ser 6 meses de esperar que los mineros señalen y luego, con suerte, sólo 2 semanas y ya está. Esos 6 meses en los que todo el mundo lo está anticipando, la gente se va a volver aún más loca de lo que está ahora quizás. Supongo que es una buena manera de decir "Acabemos con este trauma", pero creo que hay desventajas. Por un lado, ¿qué pasa si en los próximos 6 meses encontramos un error en Taproot? Tenemos 6 meses para pensar en algo que ya está activado.

AvW: Podemos hacer un soft fork.

SP: Si se trata de un error que se puede arreglar en un soft fork, sí.

AvW: Creo que cualquier Taproot, podría simplemente quemar ese tipo.

SP: Supongo que se podría añadir un soft fork que diga "No se pueden minar direcciones de la versión 1".

AvW: Sí, exactamente. Creo que eso debería ser posible, ¿verdad?

SP: Sí. Supongo que es posible anular Taproot, pero sigue dando miedo porque los nodos antiguos pensarán que está activo.

AvW: Esto es una preocupación menor para mí.

SP: Lo es y no lo es. Los nodos antiguos, los nodos que se liberan ahora básicamente y que conocen este Speedy Trial, pensarán que Taproot está activo. Podrían crear direcciones de recepción y enviar monedas. Pero sus transacciones no se confirmarán o se confirmarán y luego se desconfirmarán. No se dejarán arrastrar porque la bifurcación suave dirá "No puedes gastar este dinero". No es "cualquiera puede gastar", es "no puedes gastar esto". Está protegido en ese sentido. Supongo que hay formas de salir del lío con el soft fork, pero que no son tan bonitas como decir "Aborta, aborta, aborta. No hagas la señal". Si utilizamos el mecanismo normal del BIP 8, hasta que los mineros empiecen a señalar puedes decir simplemente "No señalar".

AvW: Claro. ¿Alguna reflexión final? ¿Cuáles son sus expectativas? ¿Qué va a ocurrir?

SP: No lo sé, estoy contento de ver avances en el código. Al menos tenemos el código real y luego decidiremos qué hacer con él. Gracias por escuchar el van Wirdum Sjorsnado.

AvW: Ahí lo tienes.

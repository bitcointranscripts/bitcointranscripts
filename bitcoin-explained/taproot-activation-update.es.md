---
title: Actualización de la activación de Taproot
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-04-23
episode: 36
media: https://www.youtube.com/watch?v=SHmEXPvN6t4
aliases:
  - /es/bitcoin-magazine/2021-04-23-taproot-activation-update
---
Tema: Actualización de la activación de Taproot: Speedy Trial y el cliente LOT=true

Ubicación: Bitcoin Magazine (en línea)

Fecha: 23 de abril de 2021

Episodio anterior en lockinontimeout (LOT): <https://btctranscripts.com/bitcoin-magazine/2021-02-26-taproot-activation-lockinontimeout/>

Episodio anterior sobre Speedy Trial: <https://btctranscripts.com/bitcoin-magazine/2021-03-12-taproot-activation-speedy-trial/>

Aaron van Wirdum en "Ahora hay dos clientes de activación de Taproot, aquí está el porqué": <https://bitcoinmagazine.com/technical/there-are-now-two-taproot-activation-clients-heres-why>

Transcripción por: Michael Folkson

# Introducción

Aaron van Wirdum (AvW): En directo desde Utrecht este es el van Wirdum Sjorsnado.

Sjors Provoost (SP): Hola

AvW: Sjors, hoy tenemos mucho más que discutir.

SP: Ya hemos hecho este juego de palabras.

AvW: Creo que ya lo hemos hecho dos veces. No importa. Hoy vamos a hablar de los últimos detalles de la implementación del Speedy Trial. Ya hemos hablado de Speedy Trial en un episodio [anterior](https://btctranscripts.com/bitcoin-magazine/2021-03-12-taproot-activation-speedy-trial/). Esta vez también vamos a contrastarlo con el cliente LOT=true que es una alternativa que ha sido lanzada por un par de miembros de la comunidad. Vamos a discutir cómo se comparan.

SP: Me parece una buena idea. También hablamos de las opciones de activación de Taproot en general en un episodio anterior.

AvW: ¿Uno de los primeros?

SP: También hablamos de esta idea de esta mentalidad de vaquero en la que alguien acabaría lanzando un cliente LOT=true hagas lo que hagas.

AvW: En eso estamos.

SP: También predijimos correctamente que habría un montón de motos.

AvW: Sí, esto también es algo en lo que vamos a entrar. En primer lugar, como breve resumen, estamos hablando de la activación de Taproot. Taproot es una propuesta de actualización del protocolo para contratos inteligentes compactos y potencialmente preservadores de la privacidad en el protocolo Bitcoin. ¿Es un buen resumen?

SP: Sí, creo que sí.

AvW: El debate sobre la forma de actualizar ya lleva un tiempo. El reto es que en una red abierta y descentralizada como Bitcoin, sin un dictador central que diga a todo el mundo qué debe ejecutar y cuándo, no vas a conseguir que todo el mundo se actualice al mismo tiempo. Pero queremos mantener la red en consenso de una forma u otra.

SP: Sí. La otra cosa que puede funcionar cuando se trata de un sistema distribuido es algún tipo de convenciones, formas en las que estás acostumbrado a hacer las cosas. Pero, por desgracia, la convención que teníamos se topó con problemas con el despliegue de SegWit. Entonces la pregunta es: "¿Debemos probar otra cosa o ha sido un accidente fortuito y debemos volver a intentar lo mismo?".

AvW: Creo que el último preámbulo antes de que empecemos a hablar de Speedy Trial, me gustaría señalar que la idea general con una bifurcación suave, una actualización compatible hacia atrás que es Taproot, es que si la mayoría del poder de hash está aplicando las nuevas reglas eso significa que la red permanecerá en consenso.

SP: Sí. Podemos repetir que si sigues haciendo transacciones que son anteriores a Taproot, esas transacciones siguen siendo válidas. En ese sentido, como usuario puedes ignorar las bifurcaciones suaves. Desgraciadamente, si hay un problema, no puedes ignorarlo como usuario aunque tus transacciones no utilicen Taproot.

AvW: Creo que todo el mundo está de acuerdo en que es muy bueno que una mayoría de poder de hash haga cumplir las reglas. Existen mecanismos de coordinación para medir cuántos mineros están de acuerdo con una actualización. Así es como se puede coordinar un soft fork bastante seguro. Eso es algo en lo que todo el mundo está de acuerdo. Donde la gente empieza a discrepar es en lo que ocurre si los mineros no cooperan realmente con esta coordinación. No vamos a repetir todo eso. Hay episodios anteriores sobre eso. Lo que vamos a explicar es que al final la comunidad de desarrollo de Bitcoin Core se decantó por una solución llamada "Speedy Trial". Ya lo mencionamos también en un episodio anterior. Ahora está finalizado y vamos a explicar cuáles son los parámetros finalizados para esto.

SP: Hubo un pequeño cambio.

AvW: Vamos a escucharlo Sjors. ¿Cuáles son los parámetros definitivos para el Speedy Trial? ¿Cómo va a actualizar Bitcoin Core a Taproot?

# Parámetros de activación finalizados de Bitcoin Core

Notas de lanzamiento de Bitcoin Core 0.21.1: <https://github.com/bitcoin/bitcoin/blob/0.21/doc/release-notes.md>

Parámetros de activación de Speedy Trial fusionados en Core: <https://github.com/bitcoin/bitcoin/pull/21686>

SP: A partir de creo que es este domingo (25 de abril, medianoche) la primera vez que se reajusta lo difícil, eso ocurre cada dos semanas, probablemente una semana después del domingo...

AvW: Es el sábado

SP: ... comienza la señalización. En unas dos semanas comienza la señalización, no antes de una semana.

AvW: Para que quede claro, eso es lo más pronto que puede empezar.

SP: Lo más pronto que puede empezar es el 24 de abril, pero como sólo empieza en un nuevo periodo de ajuste de la dificultad, un nuevo periodo de retargeting, probablemente no empezará hasta dentro de dos semanas.

AvW: Comenzará en el primer nuevo periodo de dificultad después del 24 de abril, que se calcula que será a principios de mayo. El 4 de mayo, que el cuarto esté contigo Sjors.

SP: Esa sería una fecha genial. Es cuando comienza la señalización y ésta se produce en rondas de votación, por así decirlo. Una ronda de votaciones son dos semanas o un período de ajuste de la dificultad, un período de retargeting. Si el 90% de los bloques en ese período de votación señalan el bit número 2, si eso sucede Taproot está bloqueado. Bloqueado significa que va a suceder, imagina el pequeño gif con Ron Paul, "Está sucediendo". Pero las reglas reales de Taproot no entrarán en vigor inmediatamente, lo harán en el bloque número 709632.

AvW: ¿Que se estima que se minará cuando?

SP: Será el 12 de noviembre de este año.

AvW: Eso va a variar un poco, por supuesto, en función de la rapidez con la que se minen los bloques en los próximos meses. Será en noviembre, casi con toda seguridad.

SP: Lo que supondría 4 años después de la implosión del esfuerzo de SegWit2x.

AvW: Sí, un buen momento en ese sentido.

SP: Todas las fechas son buenas. Eso es lo que hace el Speedy Trial. Cada dos semanas hay una votación, si se alcanza el 90% de los votos, esa es la fecha de activación. No ocurre inmediatamente y como es un "Speedy Trial" también podría fallar rápidamente y eso es en agosto, alrededor del 11 de agosto. Si el periodo de dificultad después de eso o antes, siempre se me olvida, no llega a la meta, creo que es después...

AvW: El periodo de dificultad debe haber terminado el 11 de agosto ¿no?

SP: Cuando pasa el 11 de agosto todavía podría activarse pero luego el siguiente periodo de dificultad, no puede. Creo que la regla es que al final del periodo de dificultad se empieza a contar y si el resultado es un fracaso entonces si es después del 11 de agosto se abandona pero si todavía no es el 11 de agosto se entra en la siguiente ronda.

AvW: Si el primer bloque de un nuevo periodo de dificultad se mina el 10 de agosto, ¿ese periodo de dificultad seguirá contando?

SP: Así es. Creo que es uno de los cambios sutiles que se han hecho en el PIF 9 para que sea más fácil razonar sobre él. Creo que antes era al revés, cuando primero se comprobaba la fecha, pero si era pasada la fecha se abandonaba, pero si era antes de la fecha seguía contando. Ahora creo que es al revés, es un poco más sencillo.

AvW: Ya veo. Va a haber una ventana de señalización de unos 3 meses.

SP: Así es.

AvW: Si en cualquier periodo de dificultad dentro de esa ventana de señalización de 3 meses se alcanza el 90% de la potencia de hachís, Taproot se activará en noviembre de este año.

SP: Sí.

AvW: Creo que eso cubre el Speedy Trial.

SP: El umbral es el 90%, como hemos dicho. Normalmente, con el PIF 9 es del 95%, pero se ha rebajado al 90%.

AvW: ¿Qué ocurre si no se alcanza el umbral?

SP: Nada. Lo que significa que podría pasar cualquier cosa. La gente podría desplegar nuevas versiones de software, probar otro bit, etc.

AvW: Sólo quería aclarar eso.

SP: No significa que Taproot esté cancelado.

AvW: Si no se alcanza el umbral, este cliente de software específico no hará nada, pero los desarrolladores de Bitcoin Core y el resto de la comunidad de Bitcoin pueden seguir ideando nuevas formas de activar Taproot.

SP: Exactamente. Es un experimento de bajo coste. Si gana tendremos Taproot. Si no, entonces tenemos más información sobre por qué no...

AvW: También quiero aclarar. Todavía no sabemos cómo va a ser. Eso habrá que averiguarlo entonces. Podríamos empezar a calcularlo ahora, pero aún no se ha decidido cómo será el despliegue.

# Alternativa a Bitcoin Core (Cliente Taproot basado en Bitcoin Core 0.21.0)

Actualización de las versiones de activación de Taproot: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-April/018790.html>

AvW: También se lanzó otro cliente. Hay mucho debate sobre el nombre. Vamos a llamarlo cliente LOT=true.

SP: Eso me parece bien.

AvW: Se deriva de esta diferencia técnica y filosófica sobre cómo deben activarse los soft forks en primer lugar. Este cliente utiliza, lo has adivinado, LOT=true. LOT=true significa que si la ventana de señalización se acaba, al final de la misma los nodos empezarán a rechazar cualquier bloque que no señale. Sólo aceptan los bloques que señalan. Esta es la principal diferencia. Entremos en los detalles del cliente LOT=true.

SP: En principio es lo mismo, en principio es lo mismo. Hay una posibilidad teórica de que no lo sea si los mineros hacen algo realmente loco. Empieza a una cierta altura de bloque...

AvW: Acabamos de mencionar que Bitcoin Core 0.21.1 comienza su ventana de señalización en el primer periodo de dificultad después del 24 de abril. Este cliente LOT=true también comenzará en la práctica su ventana de señalización en el primer periodo de dificultad después del 24 de abril, excepto que el 24 de abril no se especifica específicamente. Simplemente eligieron la altura del bloque específico que se espera que sea el primero después del 24 de abril.

SP: Exactamente, eligieron el bloque 681.408.

AvW: Se especifica como una altura de bloque en lugar de hacerlo indirectamente mediante el uso de una fecha.

SP: Pero lo más probable es que sea exactamente el mismo momento. Tanto el Speedy Trial (Core) como el cliente LOT=true iniciarán la señalización, los periodos de votación al mismo tiempo. Los periodos de votación en sí, votan en el mismo bit. Ambos votan en el bit 2. Ambos tienen un umbral del 90%. Además, si el voto es verdadero, también tiene una activación retardada. La activación retardada es una altura de bloque en ambos escenarios, tanto en el Speedy Trial (Core) como en la variante LOT=true.

AvW: Botha son el 12 de noviembre, una activación de noviembre de todos modos. Si los mineros señalan que están preparados para Taproot dentro del periodo de Speedy Trial, ambos clientes activarán Taproot en noviembre en esa misma fecha, exactamente en el mismo bloque.

SP: Así que en ese sentido son idénticos. Pero también son diferentes.

AvW: Entremos en la primera gran diferencia. Ya hemos mencionado una diferencia, que es la diferencia muy sutil entre empezar en la altura, lo que acabamos de mencionar. Entremos en una diferencia mayor.

SP: También hay una altura para un tiempo de espera en este LOT=true y eso también es un bloque. Pero no sólo es un bloque, eso podría ser una pequeña diferencia especialmente cuando es un periodo de tiempo largo. Al principio si se usa la altura del bloque o la hora, la fecha se puede adivinar con mucha precisión pero si es un año por delante entonces no se puede. Pero esto es casi dos años por delante, esta altura de bloque (762048, aproximadamente el 10 de noviembre de 2022) que tienen allí. Va mucho más allá.

AvW: De aquí a dos años quieres decir, bueno uno y medio.

SP: Exactamente. En ese sentido, no importa realmente que utilicen la altura porque, de todos modos, la diferencia es muy grande. Pero esto es importante. Mantendrán la señalización durante mucho más tiempo que en el Speedy Trial. Podemos entrar en las implicaciones más adelante, pero básicamente señalarán mucho más tarde.

AvW: Vamos a ceñirnos a los hechos primero y a las implicaciones después. El Speedy Trial (Bitcoin Core), durará 3 meses. Y éste, el cliente LOT=true permitirá la señalización durante 18 meses.

SP: La otra gran diferencia es que al final de esos 18 meses, donde el Speedy Trial simplemente se dará por vencido y continuará, el LOT=true esperará a los mineros que sí señalicen. Esto podría ser nadie o podría ser todo el mundo.

AvW: Sólo aceptarán bloques de señalización después de esos 18 meses. Para los que están al tanto de toda la guerra del tamaño de los bloques, es un poco como el cliente BIP 148.

SP: Es más o menos lo mismo con una tolerancia ligeramente mayor. El cliente UASF requería cada uno de los bloques para señalar, mientras que éste requiere el 90% para señalar. En la práctica, si los mineros están en el último 10% de esa ventana, tienen que prestar un poco más de atención. Aparte de eso, es lo mismo.

AvW: Por eso algunos lo llaman el cliente UASF. El cliente BIP 148 era el cliente UASF para SegWit, este es el cliente UASF para Taproot. Sé que, por ejemplo, a Luke Dashjr, que ha contribuido a este cliente, no le gusta el término UASF en este contexto porque hay 18 meses de señalización regular de mineros.

SP: También el UASF. Es un poco más paciente que el UASF.

AvW: Hay mucha discusión sobre el nombre del cliente y sobre cómo debería llamarlo o no. En general, algunas personas lo han llamado cliente UASF y esta es la razón.

SP: Podrías llamarlo "UASF lento" o algo así.

# Implicaciones de tener dos clientes alternativos

AvW: También he visto el nombre User Enforced Miner Activated Soft Fork (UEMASF). A la gente se le ocurren nombres. Los hechos básicos están claros ahora, espero. Entremos en las implicaciones. Hay algunas incompatibilidades potenciales entre estos dos clientes de activación. Todo el mundo está de acuerdo en que Taproot es genial. Todo el mundo quiere Taproot. Todo el mundo está de acuerdo en que sería preferible que los mineros lo activaran. Lo único en lo que hay cierto desacuerdo es en cuál es el plan de respaldo. Ahí es donde entran las incompatibilidades. ¿Está usted de acuerdo?

SP: Creo que sí.

AvW: ¿Cuáles son las incompatibilidades? En primer lugar, y ya lo he mencionado, para enfatizar esto, si Speedy Trial activa Taproot no hay incompatibilidades. Ambos clientes utilizan felizmente Taproot a partir de noviembre. Esto parece bastante probable porque el 90 por ciento de los pools de minería ya han indicado que soportan Taproot. Es probable que no haya un gran problema aquí, todo saldrá bien. Si Speedy Trial no consigue activar Taproot es cuando entramos en una fase en la que vamos a empezar a buscar posibles incompatibilidades.

SP: Por supuesto. Imagínate un escenario en el que Speedy Trial fracase. Probablemente la gente de Bitcoin Core pensará en eso durante un tiempo y pensará en otras posibilidades. Por alguna razón, los mineros se entusiasman justo después de que Speedy Trial fracase y empiezan a dar señales al 90%. En lo que respecta a Bitcoin Core, Taproot nunca se activó. En lo que respecta al cliente UASF o LOT=true Taproot se acaba de activar.

AvW: Digamos que en el mes 4, tenemos 3 meses de Speedy Trial y entonces en el mes 4 los mineros de repente señalan que están listos para Taproot. A Bitcoin Core ya no le importa, Bitcoin Core 0.21.1 ya no mira la señalización. Pero el cliente LOT=true sí. En el cliente LOT=true Taproot se activará en noviembre mientras que en este cliente Bitcoin Core no lo hará.

SP: Entonces, por supuesto, si estás usando ese cliente LOT=true y empiezas inmediatamente a usar Taproot en ese momento porque estás muy emocionado, ves todos estos bloques entrando, puedes o no perder tu dinero. Cualquiera que esté ejecutando el cliente normal de Bitcoin Core aceptará esos robos de las direcciones de Taproot esencialmente.

AvW: En este caso también importa lo que los mineros están haciendo. Si los mineros señalan que están preparados porque realmente están listos y van a aplicar Taproot, entonces está bien. No hay ningún problema porque aplicarán el soft fork e incluso los nodos de Bitcoin Core 0.21.1 seguirán esta cadena. El cliente LOT=true se aplicará y todo el mundo estará contento en la misma cadena. El único escenario en el que esto es un problema, lo que acabas de describir, es si los mineros señalan la disponibilidad pero no van a hacer cumplir las reglas de Taproot.

SP: El problema es, por supuesto, en general con las bifurcaciones suaves, pero especialmente si todo el mundo no está exactamente en la misma página sobre cuáles son las reglas, sólo se sabe que se aplica cuando realmente se aplica. No se sabe si se va a aplicar en el futuro. Esto creará un dilema para todos los demás porque entonces la pregunta es ¿qué hacer? Una cosa que podrías hacer en ese momento es decir "Obviamente Taproot está activado, así que vamos a lanzar una nueva versión de Bitcoin Core que sólo diga retroactivamente que está activado". Podría ser simplemente un soft fork de BIP 9 repitiendo el mismo bit pero un poco más tarde o podría decir simplemente "Sabemos que se activó. Simplemente codificaremos la fecha de la bandera".

AvW: Podría ser simplemente una segunda prueba rápida. ¿Todo funcionaría en ese caso?

SP: Hay un problema con la reutilización del mismo número de bits en un corto período de tiempo. (Nota: AJ Towns declaró en el IRC que esto sólo sería un problema si se desplegaran múltiples horquillas suaves en paralelo). Debido a que sería exactamente la semana después en el escenario que hablamos puede no ser posible utilizar el mismo bit. Entonces tendrás un problema porque no puedes comprobar ese bit específico pero no hay señal en ninguno de los otros bits. Eso crearía un poco de dolor de cabeza. La otra solución sería muy sencilla, decir que aparentemente está activado, así que simplemente codificaremos la fecha del bloque y lo activaremos entonces. El problema es qué pasa si entre el momento en que la comunidad decide "Vamos a hacer esto" y el momento en que el software se libera y se despliega un poco ampliamente uno o más mineros dicen "En realidad vamos a empezar a robar estas monedas Taproot". Se obtiene un clusterf\*\* \* en términos de acuerdo en la cadena. Ahora los mineros no estarán incentivados a hacer esto porque ¿por qué crearías deliberadamente un caos total si acabas de dar la señal de una bifurcación suave? Pero es una situación que da mucho miedo y puede hacer que dé miedo hacer la liberación. Si se hace el lanzamiento pero los mineros empiezan a hacer estas travesuras, ¿qué se hace entonces? ¿Aceptas una enorme reorganización en algún momento? ¿O te rindes y consideras que no se ha desplegado? Pero entonces la gente pierde su dinero y has liberado un cliente del que ahora tienes que hacer un hard fork técnico. No es un buen escenario.

AvW: Se complica en escenarios como éste, también con la teoría de juegos y la economía. Incluso si los mineros decidieran robar, se arriesgan a robar monedas en una cadena que podría reagruparse. Acaban de minar una cadena que podría ser reordenada si otros mineros aplican estas reglas de Taproot. Es extraño, es una discusión sobre los incentivos económicos y la teoría del juego en ese escenario. Personalmente creo que es bastante improbable que algo así ocurra, pero al menos es técnicamente posible y es algo a tener en cuenta.

SP: Hace que uno se pregunte si como minero es inteligente señalar inmediatamente después de este Speedy Trial.  Este cliente LOT=true permite dos años de todos modos. Si la única razón por la que estás señalando es porque este cliente existe, entonces yo sugeriría fuertemente no hacerlo inmediatamente después del Speedy Trial. Tal vez esperar un poco hasta que haya algún consenso sobre lo que hay que hacer a continuación.

AvW: Una cosa que has mencionado y que quiero abordar rápidamente, este riesgo siempre existe para cualquier soft fork. Los mineros siempre pueden dar falsas señales, podrían haberlo hecho con SegWit por ejemplo, dar falsas señales y luego robar monedas de las salidas de SegWit. Los nodos antiguos no notarían la diferencia. Eso siempre es un riesgo. Creo que la diferencia aquí es que los usuarios de Bitcoin Core 0.21.1 en este escenario podrían pensar que están ejecutando un nuevo nodo, desde su perspectiva están ejecutando un nodo actualizado. Están corriendo los mismos riesgos que antes sólo corrían los nodos desactualizados.

SP: Yo estaría más preocupado por los potenciales usuarios de la 0.21.2 que están instalando el sucesor de Speedy Trial que retroactivamente activa Taproot quizás. Ese grupo está muy inseguro de cuáles son las reglas.

AvW: ¿De qué grupo se trata?

SP: Si el Speedy Trial falla y luego es señalado, podría haber una nueva versión y la gente instalaría esa nueva versión, pero entonces no está claro si esa nueva versión sería segura o no. Esa nueva versión sería la única que realmente pensaría que Taproot está activo, así como el cliente LOT=true. Pero ahora no sabemos qué están ejecutando los mineros y no sabemos qué están ejecutando los intercambios porque esto es muy nuevo. Esto se haría en un periodo de semanas. Ahora mismo tenemos un plazo de 6 meses... Supongo que la fecha de activación seguiría siendo noviembre.

AvW: Seguiría siendo noviembre, así que todavía hay margen para prepararse en ese caso.

SP: Vale, entonces supongo que lo que he dicho antes no tiene sentido. La solución más fácil sería hacer una fecha de bandera en la que la nueva versión dijera "Se va a activar el 12 de noviembre o lo que sea la altura del bloque sin ninguna señalización". La señalización existe, pero la gente tiene diferentes interpretaciones al respecto. Esa podría ser una forma.

# Recapitulación

AvW: Sigo teniendo muy claro de qué estamos hablando aquí, pero no estoy seguro de que nuestros oyentes se estén poniendo al día en este momento. ¿Recapitulamos? Si los mineros se activan durante el Speedy Trial entonces todo está bien, todo el mundo está en consenso.

SP: Y las nuevas reglas entran en vigor en noviembre.

AvW: Si los mineros se activan después del periodo de Speedy Trial entonces existe la posibilidad de que el cliente LOT=true y el cliente Bitcoin Core 0.21.1 no estén en consenso si un bloque Taproot inválido es minado alguna vez.

SP: No tienen señalización forzada, tienes razón. Si una transacción Taproot inválida aparece después del 12 de noviembre....

AvW:.... y si se mina y se hace cumplir por una mayoría de mineros, una mayoría de mineros debe tener señalización falsa, entonces los dos clientes pueden salir del consenso. Técnicamente esto es cierto, personalmente creo que es bastante improbable. No me preocupa demasiado, pero al menos es técnicamente cierto y es algo que la gente debería tener en cuenta.

SP: Ese escenario podría prevenirse diciendo "Si vemos esta señalización "falsa", si vemos esta señalización masiva una semana después del Speedy Trial entonces podrías decidir lanzar un cliente de fecha de bandera que simplemente diga que vamos a activar este 12 de noviembre porque aparentemente los mineros quieren esto. De lo contrario, no tenemos ni idea de qué hacer con esta señal".

AvW: Me parece muy difícil predecir lo que los desarrolladores de Bitcoin Core van a decidir en este caso.

SP: Estoy de acuerdo, pero esta es una posibilidad.

# Una posibilidad más probable es que los dos clientes sean incompatibles.

AvW: Esa es una de las formas en que los dos clientes pueden ser potencialmente incompatibles. Hay otra forma que tal vez sea más probable o al menos no es tan complicada.

SP: La otra es "Imaginemos que el Speedy Trial falla y la comunidad no tiene consenso sobre cómo proceder a continuación". Los desarrolladores de Bitcoin Core pueden ver eso, hay una discusión continua y nadie se pone de acuerdo. Tal vez los desarrolladores de Bitcoin Core decidan esperar y ver.

AvW: Los mineros no están señalando...

SP: O de forma errática, etc. Los mineros no están señalando. La discusión continúa. No pasa nada. Entonces este mecanismo LOT=true entra en acción...

AvW: Después de 18 meses. Estamos hablando de noviembre de 2022, queda mucho tiempo, pero en algún momento el mecanismo LOT=true entrará en acción.

SP: Exactamente. Entonces esos nodos, suponiendo que los mineros sigan sin dar señales, dejarán de...

AvW: Eso es si literalmente no hay bloques de señalización LOT=true.

SP: En el otro escenario en el que los mineros sí empiezan a señalar masivamente, ahora volvemos a ese escenario anterior en el que de repente hay mucha señalización de mineros en el bit 2. Puede que la bifurcación suave esté activa pero ahora no hay retraso. Si la señalización ocurre en cualquier lugar después del 12 de noviembre el cliente LOT=true activará Taproot después de un periodo de ajuste.

AvW: No estoy seguro de haberte entendido.

SP: Digamos que en este caso en diciembre de este año los mineros empiezan a señalizar de repente. Después de la altura mínima de activación. En diciembre todos empiezan a señalar. El cliente Bitcoin Core lo ignorará pero el cliente LOT=true dirá "Ok Taproot está activo".

AvW: ¿Es el mismo escenario que acabamos de discutir? Sólo hay un problema si hay una señalización falsa. Por lo demás, no hay ningún problema.

SP: Hay un problema si hay una señalización falsa, pero es más complicado resolverlo porque esa opción de simplemente lanzar un nuevo cliente con un día de bandera en él que esté lo suficientemente lejos en el futuro, eso ya no existe. Es potencialmente activo inmediatamente. Si haces un lanzamiento pero de repente un minero empieza a no aplicar las reglas, obtienes esta confusión de la que hablamos antes. Entonces podemos solucionarlo haciendo simplemente una fecha de bandera. Esto sería aún más confuso. Tal vez también sea aún menos probable.

AvW: Es bastante similar al escenario anterior, pero un poco más difícil, menos obvio cómo resolver esto.

SP: Creo que es más complicado porque es menos obvio cómo hacer un lanzamiento del día de la bandera en Bitcoin Core en ese escenario porque se activa inmediatamente.

AvW: No es ahí donde quería ir con esto.

SP: ¿Querías ir a un escenario en el que los mineros esperan hasta el final hasta que empiezan a señalar?

AvW: Sí, eso es lo que quería.

SP: Aquí es donde entra en juego la señalización obligatoria. Si no hay señalización obligatoria, los nodos LOT=true se detendrán hasta que alguien mine un bloque que le gustaría ver, un bloque que señale. Si ven este bloque que señala estamos de vuelta en el ejemplo anterior donde de repente los nodos regulares de Bitcoin Core ven esta señalización pero la ignoran. Ahora hay un grupo de nodos que creen que Taproot está activo y hay un grupo de nodos que no. Entonces alguien tiene que decidir qué hacer con él.

AvW: ¿Sigue hablando de falsa señalización aquí?

SP: Even if the signaling is genuine you still want there to be a Bitcoin Core release, probably, that actually says “We have Taproot now.” But the question is when do we have Taproot according to that release? What is a safe date to put in there? You could do it retroactively.

AvW: Cuando quieran. La cuestión es que si los mineros hacen cumplir las nuevas reglas, la cadena se mantendrá unida. Depende de Bitcoin Core implementarlas cuando les apetezca.

SP: El problema con esta señalización es que no sabes si está activa hasta que alguien decide intentar romper las reglas.

AvW: Mi suposición era que no había señalización falsa. De todos modos, crearán la cadena más larga con las reglas válidas.

SP: El problema con eso es que no se puede saber.

AvW: El escenario al que realmente quería llegar Sjors es el escenario muy simple en el que la mayoría de los mineros no señalan cuando se cumplen los 18 meses. En ese caso van a crear la cadena más larga que los nodos de Bitcoin Core 0.21.1 van a seguir mientras que los nodos LOT=true sólo van a aceptar los bloques que sí señalen, que pueden ser cero o al menos menos menos. Si es una mayoría entonces no hay división. Pero si no es una mayoría entonces tenemos una división.

SP: Y esa cadena se retrasaría cada vez más. El incentivo para hacer un lanzamiento que tenga en cuenta eso sería bastante pequeño, creo. Depende, aquí es donde entra la teoría del juego. Desde el punto de vista de la seguridad, si ahora haces un lanzamiento que diga "Por cierto, consideramos activo Taproot con carácter retroactivo", eso provocaría una reorganización gigantesca. Si sólo lo activas, eso no causaría una reorganización gigante. Pero si se dice "Por cierto, vamos a ordenar retroactivamente esa señalización que a ustedes les interesa", eso causaría una reorganización masiva. Esto sería inseguro, eso no sería algo que se liberaría probablemente. Es una situación muy complicada.

AvW: Hay escenarios potenciales desordenados. Quiero recalcar a nuestros queridos oyentes que nada de esto va a ocurrir en los próximos dos meses.

SP: Y espero que nunca. Vamos a lanzar algunos otros malos escenarios y luego supongo que podemos pasar a otros temas.

AvW: Quiero mencionar rápidamente que la razón por la que no me preocupan demasiado estos malos escenarios es porque creo que si parece mínimamente probable que haya una división de monedas o algo así, probablemente habrá mercados de futuros. Estos mercados de futuros probablemente dejarán muy claro a todo el mundo la cadena alternativa que tiene una oportunidad, lo que informará a los mineros sobre lo que deben minar y evitará una división de esa manera. Tengo bastante confianza en la sabiduría colectiva del mercado para advertir a todo el mundo sobre los posibles escenarios, así que probablemente funcionará bien. Esa es mi percepción general.

SP: El problema con este tipo de cosas es que si no sale bien es muy, muy malo. Entonces podemos decir con carácter retroactivo "Supongo que no ha salido bien".

# Proceso de desarrollo de LOT=true cliente

AvW: Quiero plantear algo antes de que plantees lo que querías plantear. He visto algunas preocupaciones por parte de los desarrolladores de Bitcoin Core sobre el proceso de desarrollo del cliente LOT=true. Creo que esto se reduce a la construcción de Gitian, la firma de Gitian que también discutimos en otro [episodio](https://www.youtube.com/watch?v=_qdhc5WLd2A).

SP: Hemos hablado de la necesidad de que el software sea de código abierto, de que sea fácil de auditar.

AvW: ¿Puede dar su opinión al respecto en este contexto?

SP: El cambio que hicieron en relación con el cliente principal de Bitcoin Core no es enorme. Se puede ver en GitHub. En ese sentido, esa parte del código abierto es razonablemente factible de verificar. Creo que ese código ha tenido menos revisión pero no cero revisión.

AvW: ¿Menos que el de Bitcoin Core?

SP: Exactamente, pero mucho más que el de UASF, mucho más que el de 2017.

AvW: ¿Más que eso?

SP: I would say. The idea has been studied a bit longer. But the second problem is how do you know that what you are downloading isn’t malware. There are two measures there. There is release signatures, the website explains pretty well how to check those. I think they were signed by Luke Dashjr and by the other developer. You can check that.

AvW: Bitcoin Mechanic es el otro desarrollador. En realidad, lo publican Bitcoin Mechanic y Shinobi y Luke Dashjr es el asesor, el colaborador.

SP: Normalmente hay un archivo binario que se descarga y luego hay un archivo con sumas de comprobación y ese archivo con sumas de comprobación también está firmado por una persona conocida. Si tienes la clave de Luke o de quien sea, su clave y la conoces, puedes comprobar que al menos el binario que has descargado no procede de un sitio web pirateado. Lo segundo, es que tienes un binario y sabes que lo han firmado, pero ¿quiénes son? La segunda cosa es que quieres comprobar que este código coincide con el binario y ahí es donde entra la construcción Gitian de la que hablamos en un [episodio] anterior (https://www.youtube.com/watch?v=_qdhc5WLd2A). Básicamente, las construcciones deterministas. Toma el código fuente y produce el binario. Múltiples personas pueden entonces firmar que, de hecho, según ellos este código fuente produce este binario. Cuantas más personas lo confirmen, más probable es que no haya colusión. Creo que sólo hay dos firmas de Gitian para esta otra versión.

AvW: Así que el software de Bitcoin Core está siendo firmado por Gitian...

SP: Creo que 10 o 20 personas.

AvW: Muchos de los desarrolladores experimentados de Bitcoin Core que han estado desarrollando el software de Bitcoin Core durante un tiempo. ¿Incluido usted? ¿Lo firmó usted?

SP: La versión más reciente, sí.

AvW: Usted confía en que no están todos confabulados y difundiendo malware. Para la mayoría de la gente, todo se reduce a la confianza en ese sentido.

SP: Si realmente estás pensando en utilizar este software alternativo, deberías saber lo que estás haciendo en términos de todos estos escenarios de reorganización. Si ya sabes lo que estás haciendo en esos términos, entonces simplemente compila la cosa desde el código fuente. ¿Por qué no? Si no eres capaz de compilar las cosas desde el código fuente, probablemente no deberías ejecutar esto. Pero eso depende de ti. No me preocupa que estén enviando malware, pero en general es sólo cuestión de tiempo antes de que alguien diga "Tengo una versión diferente con LOT=happy y por favor descárguela aquí" y le robe todo su Bitcoin. Es más el precedente que está sentando esto lo que me preocupa que esta cosa pueda realmente tener malware.

AvW: Eso es justo. ¿Tal vez firmarlo Sjors?

SP: No, porque no creo que sea una cosa sana para publicar.

AvW: Me parece justo.

SP: Es sólo mi opinión. Cada uno es libre de publicar lo que quiera.

AvW: ¿Había algo más que quisieras comentar?

# ¿Qué lanzaría Bitcoin Core si Speedy Trial no se activara?

SP: Sí, hablamos sobre la señalización verdadera o falsa en el bit 1, pero una posibilidad muy real creo que si esta activación falla y queremos probar algo más, entonces probablemente no queramos usar el mismo bit si es antes de la ventana de tiempo de espera. Eso podría crear un escenario en el que podrías empezar a decir "Vamos a usar otro bit para hacer la señalización". Entonces podrías tener alguna confusión donde hay una nueva versión de Bitcoin Core que se activa usando el bit 3 por ejemplo pero la gente de LOT=true no lo ve porque están mirando el bit 1. Eso puede o no ser un problema real. La otra cosa es que podría haber todo tipo de otras formas de activar esta cosa. Una podría ser un día de bandera. Si Bitcoin Core lanzara un día de bandera entonces no habrá ninguna señalización. El cliente LOT=true no sabrá que Taproot está activo y exigirá la señalización en algún momento aunque Taproot ya esté activo.

AvW: Tu punto es que no sabemos lo que Bitcoin Core lanzará después de Speedy Trial y lo que podrían lanzar no necesariamente sería compatible con el cliente LOT=true. Eso funciona en ambos sentidos, por supuesto.

SP: Claro, sólo estoy razonando desde un punto. También diría que en el caso de que Bitcoin Core lance algo más que tenga un apoyo bastante amplio por parte de la comunidad, me imagino que la gente que está ejecutando los clientes BIP 8 no está sentada en una cueva en algún lugar. Probablemente son usuarios relativamente activos que pueden decidir "voy a ejecutar esta versión de Bitcoin Core de nuevo porque hay un día de bandera en él que es anterior a la señalización forzada". Podría imaginar que decidirían ejecutarla o no.

AvW: Eso también funciona en ambos sentidos.

SP: No, en realidad no. Me preocupan mucho más las personas que no siguen este debate y que simplemente se limitan a utilizar la versión más reciente de Core. O no se actualizan en absoluto, todavía están ejecutando, digamos, Bitcoin Core v0.15. Estoy mucho más preocupado por ese grupo que por el grupo que toma activamente una posición en este asunto. Si usted toma activamente una posición mediante la ejecución de otra cosa, entonces usted sabe lo que está haciendo. Depende de ti estar al día. Pero tenemos un compromiso con todos los usuarios de que si todavía estáis ejecutando en vuestro búnker la versión 0.15 de Bitcoin Core que no os pase nada malo si seguís la mayor parte de las pruebas de trabajo dentro de las reglas que conocéis.

AvW: Eso también podría significar hacerlo compatible con el cliente LOT=true.

SP: No, en lo que respecta al nodo v0.15 no hay ningún cliente LOT=true.

AvW: ¿Queremos entrar en todo tipo de escenarios? El escenario que más me preocupa es el de la cadena LOT=true por llamarlo de alguna manera, que si alguna vez se produce una escisión ganará pero sólo después de un tiempo porque se obtienen reorgs largos. Esto vuelve a la discusión LOT=true versus LOT=false en primer lugar.

SP: Sólo veo que eso ocurra con un colapso masivo del precio del propio Bitcoin. Si se da el caso de que LOT=true empiece a ganar después de un retraso que requiera una gran reorganización... si es más probable que gane, su precio relativo subirá porque es más probable que gane. Pero como un re-org más grande es más desastroso para Bitcoin cuanto más largo sea el re-org más bajo será el precio de Bitcoin. Ese sería el escenario malo. Si hay una reorganización de 1000 bloques o más, entonces creo que el precio de Bitcoin se derrumbará a algo muy bajo. Realmente no nos importa si el cliente LOT=true gana o no. Eso ya no importa.

AvW: Estoy de acuerdo con eso. La razón por la que no me preocupa es lo que he mencionado antes, creo que estas cosas las resolverán los mercados de futuros mucho antes de que ocurra realmente.

SP: Supongo que el mercado de futuros predeciría exactamente eso. Eso no sería bueno. Dependiendo de tu confianza en los mercados de futuros, que para mí no es tan sorprendente.

# Altura del bloque frente a MTP

<https://github.com/bitcoin/bitcoin/pull/21377#issuecomment-818758277>

SP: Podríamos seguir hablando de esta diferencia de fondo entre la altura de los bloques y el tiempo de los bloques. Hubo un fiasco pero no creo que sea una diferencia interesante.

AvW: También podríamos mencionarlo.

SP: Cuando describimos por primera vez el Speedy Trial asumimos que todo se basaría en la altura de los bloques. Habría una transformación de la forma en que funcionan ahora las horquillas suaves, que se basa en estos tiempos medios, a la altura de los bloques, que es conceptualmente más sencilla. Más tarde hubo alguna discusión entre la gente que estaba trabajando en eso, considerando que tal vez la única diferencia del Speedy Trial debería ser la altura de activación y ninguno de los otros cambios. Desde el punto de vista de la base de código existente es más fácil hacer que el Speedy Trial ajuste un parámetro que es una altura de activación mínima frente al cambio donde se cambia todo en alturas de bloque que es un cambio mayor del código existente. Aunque el resultado final sea más fácil. Un enfoque basado puramente en la altura de los bloques es más fácil de entender, más fácil de explicar lo que va a hacer, cuando lo va a hacer. Algunos casos extremos también son más fáciles. Pero permanecer más cerca de la base de código existente es algo más fácil para los revisores. La diferencia es bastante pequeña, así que creo que algunas personas decidieron lanzar una moneda al aire y otras creo que estuvieron de acuerdo sin lanzarla.

AvW: Hay argumentos en ambos lados pero parecen ser bastante sutiles, bastante matizados. Como hemos dicho, el Speedy Trial va a empezar en la misma fecha, así que no parece importar mucho. En algún momento algunos desarrolladores estaban considerando seriamente decidir mediante un lanzamiento de moneda usando la cadena de bloques de Bitcoin para ello, eligiendo un bloque en el futuro cercano y viendo si termina con un número par o impar. No sé si eso fue literalmente lo que hicieron pero sería una forma de hacerlo. Creo que sí hicieron el lanzamiento de la moneda, pero luego los defensores de ambas soluciones terminaron poniéndose de acuerdo de todos modos.

SP: Estuvieron de acuerdo en lo mismo que dijo la moneda.

AvW: El principal discrepante fue Luke Dashjr, que se siente fuertemente comprometido con el uso de las alturas de los bloques de forma consistente. También es de la opinión de que la comunidad ha llegado a un consenso al respecto y que el hecho de que los desarrolladores de Bitcoin Core no lo utilicen es un retroceso o una ruptura del consenso de la comunidad.

SP: Esa es su perspectiva. Si miras a la persona que escribió el pull request original que se basaba puramente en la altura, creo que fue Andrew Chow, cerró su propio pull request a favor de la solución mixta que tenemos ahora. Si la persona que escribe el código lo elimina él mismo, creo que está bastante claro. Desde mi punto de vista la gente que está poniendo más esfuerzo debería decidir cuando es algo tan trivial. No creo que importe tanto.

AvW: A mí me parece un punto menor, pero está claro que no todo el mundo está de acuerdo en que sea un punto menor.

SP: De eso se trata el bikeshedding, ¿no? No sería bikeshedding si todo el mundo pensara que es irrelevante el color del cobertizo para bicicletas.

AvW: Dejemos el tema de la moneda y la hora, la altura de la cuadra detrás de nosotros Sjors porque creo que cubrimos todo y tal vez no deberíamos insistir en este último punto. ¿Ya está? Espero que haya quedado claro.

SP: Creo que aún podemos intercalar muy brevemente una cosa que se ha planteado, que es el ataque en el tiempo.

AvW: No lo hemos mencionado, pero es algo relevante en este contexto. Un argumento contra el uso de la hora de los bloques es que abre la puerta a los ataques de timewarp, en los que los mineros falsifican las marcas de tiempo de los bloques que minan para fingir que se trata de una hora y una fecha diferentes. De este modo, pueden, por ejemplo, saltarse el periodo de señalización, si se confabulan para hacerlo.

SP: Eso parece una cantidad enorme de esfuerzo sin una buena razón, pero es un escenario interesante. Hicimos un episodio sobre el ataque de timewarp hace mucho tiempo, cuando yo lo entendía. Hay una propuesta de bifurcación suave para deshacerse de él que no creo que nadie haya objetado, pero tampoco nadie se ha molestado en poner en práctica. Una manera de lidiar con este hipotético escenario es que si ocurriera entonces desplegamos el soft fork contra el ataque timewarp primero y luego intentamos la activación de Taproot de nuevo.

AvW: El argumento en contra de alguien como Luke es que, por supuesto, se puede arreglar cualquier fallo, pero también se puede simplemente no incluir el fallo en primer lugar.

SP: Es bueno saber que los mineros estarían dispuestos a utilizarlo. Si sabemos que los mineros están realmente dispuestos a explotar el ataque de timewarp es una información increíblemente valiosa. Si tienen una manera de confabularse y una motivación para usar ese ataque... El coste de ese ataque sería bastante bajo, sería retrasar Taproot unos meses pero tendríamos esta conspiración masiva desvelada. Creo que eso es una victoria.

AvW: La forma en que Luke lo ve es que ya había consenso en todo tipo de cosas, usando el BIP 8 y esta cosa de LOT=true, vio esto como una especie de esfuerzo de consenso. En su opinión, el uso de los tiempos de bloqueo está frustrando eso. No quiero hablar por él, pero si trato de canalizar un poco a Luke o explicar su perspectiva sería eso. En su opinión, el consenso ya se estaba formando y ahora es un camino diferente.

SP: No creo que este nuevo enfoque bloquee tanto lo de LOT=verdad. Hemos pasado por todos los escenarios y la confusión no estaba en torno a la altura de los bloques frente al tiempo, sino en todo tipo de cosas que podrían salir mal dependiendo de cómo evolucionaran las cosas. Pero no esa cuestión en particular. En cuanto al consenso, el consenso está en el ojo del que mira. Yo diría que si varias personas no están de acuerdo, entonces no hay consenso.

AvW: Eso también funcionaría al revés. Si Luke no está de acuerdo, utiliza el tiempo en bloque.

SP: Pero no puede decir que haya habido consenso en algo. Si la gente no está de acuerdo, por definición no hubo consenso.

AvW: Mi impresión es que no hubo consenso porque la gente no está de acuerdo. Terminemos. Para nuestros oyentes que están confundidos y preocupados voy a enfatizar que los próximos 3 meses la prueba rápida va a funcionar en ambos clientes. Si los mineros se activan a través de Speedy Trial vamos a tener Taproot en noviembre y todo el mundo va a ser feliz. Continuaremos la discusión del soft fork con el próximo soft fork.

SP: Volveremos a tener las mismas discusiones porque no hemos aprendido absolutamente nada.

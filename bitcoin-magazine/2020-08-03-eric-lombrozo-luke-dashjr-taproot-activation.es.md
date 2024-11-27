---
title: Cómo activar un nuevo Soft Fork
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
  - soft-fork-activation
date: 2020-08-03
speakers:
  - Eric Lombrozo
  - Luke Dashjr
media: https://www.youtube.com/watch?v=yQZb0RDyFCQ
---
Location: Bitcoin Magazine (en línea)

Aaron van Wirdum Aaron van Wirdum en Bitcoin Magazine sobre el BIP 8, el BIP 9 o la activación del Soft Fork moderno: https://bitcoinmagazine.com/articles/bip-8-bip-9-or-modern-soft-fork-activation-how-bitcoin-could-upgrade-next

David Harding sobre las propuestas de activación de Taproot: https://gist.github.com/harding/dda66f5fd00611c0890bdfa70e28152d

## Introducción

Aaron van Wirdum (AvW): Eric, Luke bienvenido. Feliz Día de la Independencia de Bitcoin. ¿Cómo están?

Eric Lombrozo (EL): Estamos muy bien. ¿Cómo están ustedes?

AvW: Estoy bien, gracias. Luke, ¿cómo estás?

Luke Dashjr (LD): BIEN. ¿Cómo estás tú?

AvW: Bien, gracias. Es genial teneros en el Día de la Independencia del Bitcoin. Obviamente, ambos habéis jugado un gran papel en el movimiento UASF. Fuisteis tal vez dos de los partidarios más prominentes e influyentes. Este Día de la Independencia de Bitcoin, esta cosa del 1 de agosto de hace un par de años, se trataba de la activación de SegWit, la activación del soft fork. Esto está siendo relevante de nuevo porque estamos viendo una nueva bifurcación suave que podría estar llegando, Taproot. En general, la conversación sobre cómo activar las bifurcaciones suaves está empezando de nuevo. Así que lo que sucedió hace un par de años se está volviendo relevante de nuevo.

EL: No queremos repetir lo que ocurrió hace unos años. Queremos hacerlo mejor esta vez.

#Activaciones anteriores de la bifurcación suave

AvW: Eso es lo que quiero discutir con ustedes y por qué es genial tenerlos aquí. Empecemos con eso Eric. Hace un par de años, aparentemente algo salió mal. En primer lugar, mencionaremos brevemente que hubo un proceso llamado [BIP 9](https://github.com/bitcoin/bips/blob/master/bip-0009.mediawiki). ¿Quieres explicar muy brevemente lo que era y luego se puede entrar en por qué era un problema o lo que salió mal?

EL: Las [primeras bifurcaciones suaves](https://blog.bitmex.com/bitcoin-softfork-activation-methodology/) que se activaron fueron con fecha de bandera, simplemente escritas en el código. Más tarde, para hacer la transición más suave, se incorporó la señalización de los mineros. Entonces el BIP 9 fue esta propuesta que permitía que varias bifurcaciones suaves estuvieran bajo activación al mismo tiempo con la idea de que habría extensibilidad al protocolo y habría todo este proceso que podríamos usar para añadir nuevas características. Pero resultó ser muy desordenado y no estoy seguro de que ese proceso sea sostenible.

AvW: Para que quede claro, la idea de BIP 9 era que hubiera una bifurcación suave, que hubiera un cambio en el protocolo, y que el reto fuera conseguir que la red se actualizara a ese cambio sin dividir la red entre los nodos actualizados y los no actualizados. La idea era dejar que la coordinación de la activación dependiera del hashpower. Una vez que suficientes mineros hayan señalado que se han actualizado la red lo reconoce, todos los nodos actualizados lo reconocen y empiezan a aplicar las nuevas reglas. La razón por la que esto es una buena idea es porque si la mayoría de los mineros hacen esto no hay riesgo de que la cadena se divida. Incluso los nodos no actualizados seguirán la versión "actualizada" de la cadena de bloques.

EL: Sería la cadena más larga. Por defecto, todos los demás clientes seguirían esa cadena automáticamente.

AvW: Esa es la ventaja. Pero parece que algo salió mal. O, al menos, eso cree usted.

EL: Las primeras bifurcaciones suaves no fueron realmente políticas en absoluto. No hubo ninguna disputa. SegWit fue la primera bifurcación suave que realmente generó cierta controversia debido a todo el asunto del tamaño de los bloques que ocurrió antes. Fue un momento realmente polémico en el espacio de Bitcoin. La activación se politizó, lo cual fue un problema muy serio porque el BIP 9 no fue diseñado para tratar con la política. Fue diseñado para lidiar con la activación por señalización de los mineros sólo por lo que estabas hablando, para que la red no se dividiera. Es realmente un proceso técnico para asegurarse de que todo el mundo está en la misma página. La idea era que todo el mundo estuviera ya a bordo de esto antes del lanzamiento sin ninguna política. No era ningún tipo de sistema de votación ni nada parecido. No se diseñó ni se pretendió que fuera un sistema de votación. Algunas personas lo malinterpretaron así y algunas personas se aprovecharon de la confusión para hacer que pareciera un proceso de votación. Se abusó mucho de ello y los mineros empezaron a manipular el proceso de señalización para alterar el precio del Bitcoin y otras cosas. Se convirtió en algo muy, muy complicado. No creo que queramos hacerlo así esta vez.

AvW: Este mecanismo de coordinación, básicamente se concedió a los mineros en cierto modo para que las actualizaciones se hicieran sin problemas. Su perspectiva es que empezaron a abusar de este derecho que se les concedió. ¿Es un buen resumen?

EL: Sí. Tenía un umbral del 95 por ciento, que era algo bastante razonable antes, cuando se trataba sobre todo de mejoras técnicas que no estaban politizadas en absoluto. Era un umbral de seguridad en el que si el 95 por ciento de la potencia de la red está señalizando, entonces es casi seguro que la red no se va a dividir. Pero en realidad sólo se necesita más de la mayoría del hashpower para que la cadena sea la más larga. Se podría bajar ese umbral y aumentar ligeramente el riesgo de que la cadena se divida. El umbral del 95 por ciento, si más del 5 por ciento de los hashpower no lo señalan, obtendrían un veto. Podían vetar toda la activación. Le dio a una minoría muy pequeña la capacidad de vetar una bifurcación suave. Por defecto, si no se activaba, simplemente no se bloqueaba y fallaba. Esto era un problema porque estaba en medio del asunto del tamaño de los bloques y todo el mundo quería una resolución para esto. El fracaso no era realmente una opción.

AvW: Luke, ¿estás de acuerdo con este análisis? ¿Es así como lo ves?

LD: Más o menos sí.

## SegWit y BIP 148

AvW: En algún momento hubo una solución para salir del estancamiento que era un UASF. Esto finalmente tomó forma en el [BIP 148](https://github.com/bitcoin/bips/blob/master/bip-0148.mediawiki). Luke, creo que usted participó en el primer proceso de decisión. ¿Cuál era la idea que había detrás del PIF 148?

LD: En realidad no participé tan pronto. De hecho, en un principio me opuse a ella.

AvW: ¿Por qué?

LD: Realmente no analicé las implicaciones en su totalidad.

AvW: ¿Puede explicar qué hizo el PIF 148 y por qué se diseñó de la forma en que se diseñó?

LD: Esencialmente, devolvió la decisión a los mineros. "El 1 de agosto vamos a empezar el proceso de activación de esto y eso es todo".

AvW: Creo que la forma específica en que lo hizo fue que los nodos del BIP 148 empezaran a rechazar los bloques que no señalaran realmente la compatibilidad con SegWit. ¿Es eso cierto?

LD: Sí. Así es como se han desplegado anteriormente la mayoría de las bifurcaciones suaves activadas por el usuario. Si los mineros no señalaban la nueva versión, sus bloques serían inválidos.

AvW: Hay una diferencia de matiz entre la activación de SegWit y la aplicación de SegWit o la señalización de SegWit, ¿verdad?

LD: Las anteriores bifurcaciones suaves habían hecho prácticamente ambas cosas todo el tiempo. Antes de BIP 9 era un número de versión incremental. Los mineros tenían que tener el número de versión correcto o sus bloques eran inválidos. Cuando se lanzó la versión 3, todos los bloques de la versión 2 y anteriores dejaron de ser válidos.

AvW: ¿En algún momento empezaron a apoyar el BIP 148? ¿Por qué fue así?

LD: En un momento dado había un número suficiente de miembros de la comunidad que decían: "Vamos a hacer el BIP 148 sin importar cuántos otros estén a bordo". A partir de ese momento, una vez que fue una minoría considerable, la única manera de evitar una ruptura en cadena era ir a por todas.

EL: En ese momento era todo o nada.

AvW: ¿Qué tamaño debe tener una minoría así? ¿Existe alguna forma de medirlo, pensarlo o razonarlo? ¿Qué les hizo darse cuenta de que había suficientes usuarios que apoyaban esto?

LD: It really comes down to not so much the number of people but their relevance to the economy. All these people that are going to do BIP 148, can you just ignore them and economically pressure them or cut them off from everyone else? Or is that not viable anymore?

AvW: ¿Cómo se toma esa decisión? ¿Cómo se distingue entre lo inviable y lo viable?

EL: En ese momento lo que hicimos fue intentar hablar con muchas bolsas y con muchas otras personas del ecosistema para evaluar su nivel de apoyo. Muchos usuarios estaban muy a favor, pero cuando se hizo más evidente que muchos de los grandes nodos económicos del sistema iban a utilizar el BIP 148, quedó claro que era hacerlo o morir, era todo o nada. En ese momento había que conseguir que todo el mundo se subiera a bordo o esto no iba a funcionar.

LD: Irónicamente, uno de los primeros partidarios del BIP 148 fue BitPay, que por aquel entonces era importante.

AvW: ¿Lo eran?

LD: Creo que perdieron relevancia poco después. Pero por aquel entonces eran más importantes.

AvW: Has mencionado esta situación de "hazlo o muérete", ¿cuáles son los riesgos de morir? ¿Qué podría salir mal con algo como el BIP 148?

EL: En ese momento estábamos bastante seguros de que si la gente quería bifurcarse, lo iba a hacer. Hubo un gran empuje al asunto del BCH. Era "Vale, si la gente quiere bifurcarse, que se bifurque". Dondequiera que la economía vaya es hacia donde la gente va a gravitar. Nosotros creíamos que gravitarían hacia el uso del BIP 148, insistiendo en que todos los demás lo hicieran porque eso era lo mejor para los intereses económicos de todos. Eso es lo que ocurrió. Era un riesgo, pero creo que era un riesgo calculado. Creo que habría habido una ruptura en cadena de todas formas. La cuestión era cómo asegurarnos de que la ruptura de la cadena tuviera la menor cantidad de repercusiones económicas para las personas que querían permanecer en la cadena SegWit.

AvW: Para que quede claro, el BIP 148 también podría haber provocado una división de la cadena y, posiblemente, una reordenación. Era un riesgo en ese sentido.

EL: Claro que estábamos en un territorio desconocido. Creo que la teoría era bastante sólida, pero siempre hay un riesgo. Creo que, en este punto, el hecho de que hubiera un riesgo formaba parte de la motivación para que la gente quisiera ejecutar el BIP 148, porque cuantas más personas lo hicieran, menor sería el riesgo.

AvW: Esa era una interesante ventaja teórica del juego que tenía este BIP. Hasta el día de hoy existe un desacuerdo al respecto, ¿qué creen ustedes que hizo realmente el PBI 148? Algunos dicen que al final no hizo nada. Los mineros sólo fueron los que actualizaron el protocolo. ¿Cómo lo ve usted?

LD: Fue claramente el BIP 148 el que consiguió que se activara SegWit. Si no hubiera sido así, todo el mundo lo habría tenido muy claro porque los bloques habrían sido rechazados por los nodos del BIP 148. No hay forma de tener un 100% de señalización de mineros sin el BIP 148.

AvW: Eric, ¿estás de acuerdo con eso?

EL: Creo que el BIP 148 desempeñó un gran papel, pero creo que hubo muchos factores que fueron muy importantes. Por ejemplo, el hecho de que SegWit2x estuviera en marcha y todo el acuerdo de Nueva York. Creo que eso impulsó a la gente a querer apoyar una bifurcación suave activada por el usuario aún más. Es un poco irónico. Si todo el asunto de SegWit2x no hubiera estado ocurriendo la gente podría haber sido más complaciente y haber dicho "Vamos a aguantar un poco y esperar a ver qué pasa". Creo que esto presionó a todo el mundo para pasar a la acción. Parecía que había una amenaza inminente, así que la gente tenía que hacer algo. Ese fue el momento en el que creo que la teoría del juego empezó a funcionar de verdad, porque entonces sería posible cruzar ese umbral en el que es hacer o morir, el punto de no retorno.

AvW: Permítanme reformular un poco la pregunta. ¿Creen ustedes que SegWit se habría activado si el PIF 148 no hubiera ocurrido? ¿Tendríamos SegWit hoy?

EL: Es difícil de decir. Creo que al final podría haberse activado. En ese momento la gente lo quería y era un momento decisivo en el que la gente quería una resolución. Cuanto más se alargaba, más incertidumbre había. La incertidumbre en el protocolo no es buena para la red. Podrían haber surgido otros problemas. Creo que el momento fue el adecuado, el lugar adecuado y el momento adecuado para que esto ocurriera. ¿Podría haber ocurrido más tarde? Posiblemente. Pero creo que habría sido mucho más arriesgado,

LD: Esta conferencia de hoy probablemente estaría celebrando la activación final de SegWit en lugar de Taproot.

AvW: Una última pregunta. Para resumir esta parte de la historia de Bitcoin, ¿cuáles fueron las lecciones de este episodio? ¿Qué nos llevamos de este periodo de la historia de Bitcoin hacia adelante?

EL: Creo que es muy importante que intentemos evitar politizar este tipo de cosas. Lo ideal es que no queramos que la capa base del protocolo cambie mucho. Cada vez que se produce un cambio, se introduce un vector de ataque. Enseguida la gente podría intentar insertar vulnerabilidades o exploits o intentar dividir a la comunidad o crear ataques de ingeniería social o cosas así. Cada vez que se abre la puerta a cambiar las reglas, se está abriendo a los ataques. Ahora estamos en un punto en el que es imposible actualizar el protocolo sin tener algún tipo de proceso. Pero cuanto más intentamos ampliarlo, más tiende a convertirse en algo político. Espero que Taproot no cree el mismo tipo de contención y no se politice. No creo que sea un buen precedente que estas cosas sean controvertidas. Al mismo tiempo, no quiero que esto sea un proceso habitual. No quiero convertir en un hábito la activación de las horquillas blandas todo el tiempo. Creo que Taproot es una adición muy importante a Bitcoin y parece tener mucho apoyo de la comunidad. Sería muy bueno incluirlo ahora. Creo que si esperamos va a ser más difícil activarlo más adelante.

## BIP 8 como una posible mejora de BIP 9

AvW: Has mencionado que en 2017 se produjo este periodo de controversia, la guerra civil del escalado, como quieras llamarlo. ¿Hubo realmente un problema con el PIF 9 o solo fue un periodo de controversia y a estas alturas el PIF 9 volvería a estar bien?

EL: Creo que el problema del PIF 9 fue que era muy optimista. La gente jugaría bien y que la gente cooperaría. El PIF 9 no funciona en absoluto bien en un escenario no cooperativo. Por defecto, fracasa. No sé si es algo que queremos hacer en el futuro porque si falla significa que todavía hay controversia, que no se ha resuelto. El PIF 8 tiene una fecha límite en la que tiene que activarse a una hora determinada. Por defecto se activa, mientras que el BIP 9 no se activa por defecto. Elimina el poder de veto de los mineros. Creo que el BIP 9 es muy problemático. En el mejor de los casos podría funcionar, pero es demasiado fácil de atacar.

LD: Y crea un incentivo para ese ataque.

AvW: Lo que está diciendo es que incluso en un periodo en el que no haya una guerra civil, ni una gran controversia, utilizar algo como el BIP 9 invitaría a la controversia. ¿Es eso lo que le preocupa?

EL: Posiblemente sí.

LD: Porque ahora los mineros pueden tener como rehén el soft fork que presumiblemente ya ha sido acordado por la comunidad. Si no ha sido acordado por la comunidad no deberíamos desplegarlo con ninguna activación, y punto.

AvW: Luke has estado trabajando en el [BIP 8](https://github.com/bitcoin/bips/blob/master/bip-0008.mediawiki) que es una forma alternativa de activar las bifurcaciones suaves. ¿Puedes explicar en qué consiste el BIP 8?

LD: Más que una alternativa, lo veo como una forma de tomar el BIP 9 y arreglar los errores que tiene.

AvW: ¿Cómo se solucionan los errores? ¿Qué hace la BIP 8?

LD: El error más obvio fue el hecho de que uno de los problemas del BIP 9 cuando fuimos a hacer el BIP 148 era que originalmente se había fijado para la activación en noviembre, no en agosto. Entonces la gente se dio cuenta de que si el hashpower es demasiado bajo podríamos forzar la señalización durante noviembre y seguiría sin activarse porque el tiempo transcurriría demasiado rápido. Esto se debe a que el BIP 9 utilizaba marcas de tiempo, tiempo del mundo real, para determinar cuándo expiraría el BIP.

AvW: Porque los bloques se pueden minar más rápido o más lento, así que el tiempo del mundo real puede darte problemas.

LD: Si los bloques se minan demasiado despacio, el tiempo de espera se produce antes de que termine el periodo de dificultad, que era uno de los requisitos para la activación. El error más obvio que arregló el BIP 8 fue utilizar alturas en lugar de tiempo. De esta forma, si los bloques se ralentizaban, el tiempo de espera también se retrasaba. El BIP 148 solucionó esto adelantando el periodo de señalización obligatoria a agosto, que era muy rápido. Creo que todo el mundo estaba de acuerdo con eso. Fue una necesidad desafortunada debido a ese fallo. La otra es, como estábamos hablando, que crea un incentivo para que los mineros bloqueen la bifurcación suave. Si se activa después del tiempo de espera, ese incentivo desaparece. Hay riesgos si se encuentra un error. No podemos echarnos atrás una vez que se ha establecido la activación. Por supuesto, deberíamos encontrar errores antes de establecer la activación, así que esperamos que eso no importe.

AvW: ¿Es posible configurar el BIP 8? Se puede forzar la señalización al final o no. ¿Cómo funciona esto exactamente?

LD: Ese fue un cambio más reciente, ahora que hemos vuelto a poner en marcha el tema de la activación. Está diseñado para que puedas desplegarlo con una activación que haga timeout y aborte y luego cambiar esa bandera a un UASF. Si el UASF se establece más tarde, siempre y cuando tenga suficiente apoyo de la comunidad para hacer el UASF, todos los nodos que fueron configurados sin el UASF seguirán con él.

AvW: ¿Quién establece esta bandera? ¿Está integrada en una versión del software o es algo que los usuarios pueden hacer manualmente? ¿O es algo que se compila?

LD: Eso es un detalle de implementación. Al fin y al cabo, los usuarios pueden modificar el código o alguien puede proporcionar una versión con esa modificación.

AvW: ¿Cómo lo harías? ¿Cómo le gustaría que se utilizara el BIP 8?

LD: Como no deberíamos desplegar ningún parámetro de activación sin el suficiente apoyo de la comunidad, creo que deberíamos establecerlo por adelantado. Había un UASF de Bitcoin Core con el código del BIP 148 en él. Creo que sería mejor hacer todas las bifurcaciones suaves de esa manera a partir de ahora y dejar las versiones vanilla de Bitcoin Core sin ninguna activación de bifurcación suave.

AvW: Esa es una perspectiva interesante. ¿Podría Bitcoin Core no incluir ningún tipo de activación de BIP 8? ¿Está completamente integrado en clientes alternativos como el cliente BIP 148 y no en Bitcoin Core en absoluto? ¿Con el UASF esta es la forma de hacerlo a partir de ahora?

LD: Creo que sería lo mejor. Antes de 2017 habría dudado de que la comunidad lo aceptara, pero ha funcionado bien con el BIP 148, así que no veo ninguna razón para no continuarlo.

AvW: ¿No debería Bitcoin Core en ese caso incluir al menos el BIP 8 sin señalización forzada para que siga aplicando la bifurcación suave y siga adelante?

LD: Posiblemente. También hay un punto intermedio en el que podría detectar que se ha activado.

AvW: ¿Y entonces qué? ¿Los usuarios saben que deben actualizarse?

LD: Puede activarse en ese momento.

AvW: ¿Cuál es la ventaja de detectar que se ha actualizado?

LD: Para que pueda activar las reglas y seguir siendo un nodo completo. Si no está aplicando las horquillas suaves más recientes, ya no es un nodo completo. Eso puede ser un problema de seguridad.

AvW: That is what I meant with BIP 8 without forced signaling. I thought that was the same thing.

LD: There is a pull request to BIP 8 that may make the same thing. I would have to look at that pull request, I am not sure it is identical quite yet.

#Activación a través de clientes alternativos

AvW: Eric, ¿qué opinas de esta idea de activar las bifurcaciones suaves a través de clientes alternativos como hizo el BIP 148?

EL: Probablemente es una buena idea. Creo que es mejor que Bitcoin Core se mantenga al margen de todo el proceso. Cuanto menos político sea Bitcoin Core, mejor. La gente que ha trabajado en estos BIPs en su mayoría no quiere involucrarse demasiado en estas cosas públicas. Creo que es lo mejor. Creo que sentaría un precedente realmente horrible para Bitcoin Core el estar desplegando cambios de protocolo por sí mismo. Es muy importante que el apoyo de la comunidad esté ahí y se demuestre fuera del proyecto Bitcoin Core y que sea decisivo. Que no se politice una vez desplegado. Creo que es importante que haya suficiente apoyo antes del despliegue y es bastante seguro que va a suceder. En ese momento no hay que tomar más decisiones ni nada por el estilo, porque cualquier otra decisión que se añada al proceso no hace más que añadir más puntos potenciales en los que la gente podría intentar añadir polémica.

AvW: ¿Cuál es el problema si Bitcoin Core activa las bifurcaciones suaves o las bifurcaciones suaves se implementan en el cliente de Bitcoin Core?

EL: Sienta un precedente realmente malo porque Bitcoin Core se ha convertido en la implementación de referencia. Es el software de nodo más utilizado. Es muy peligroso, es una especie de separación de poderes. Sería realmente peligroso para Bitcoin Core tener la capacidad de implementar este tipo de cosas y desplegarlas especialmente bajo el radar, creo que sería realmente peligroso. Es muy importante que estas cosas sean revisadas y que todo el mundo tenga la oportunidad de verlas. Creo que ahora mismo la gente que está trabajando en Bitcoin Core puede ser buena, gente honesta y fiable, pero eventualmente podría ser infiltrada por gente o por otras personas que podrían no tener las mejores intenciones. Podría llegar a ser peligroso en algún momento si se convierte en un hábito hacerlo así.

AvW: O los desarrolladores de Bitcoin Core podrían ser coaccionados o recibir llamadas de agencias de tres letras.

LD: Especialmente si hay un precedente o incluso una apariencia de este supuesto poder. Va a provocar que la gente malintencionada piense que puede presionar a los desarrolladores e intente hacerlo aunque no funcione.

AvW: El inconveniente obvio es que si no hay suficiente gente que se actualice a este cliente alternativo en este caso podría dividir la red. Podría dividir la red, podría provocar el caos del que hablábamos antes con las reorganizaciones en cadena. ¿No es este un riesgo que le preocupa?

EL: Si no tiene suficiente apoyo previo, probablemente no debería hacerse. El apoyo debe estar ahí y debe quedar muy claro que hay un acuerdo casi unánime. Una gran parte de la comunidad lo quiere antes de que se despliegue el código. En el momento en que se despliegue el código, creo que sería bastante razonable esperar que la gente quiera ejecutarlo. De lo contrario, no creo que deba hacerse en absoluto.

AvW: Pero pone una fecha límite para que la gente actualice su software. La gente no puede ser demasiado perezosa. La gente tiene que hacer algo, de lo contrario surgirán riesgos.

LD: Eso es cierto, independientemente de la versión en la que se encuentre.

AvW: Entonces quiero plantear una hipótesis. Digamos que se elige esta solución. Existe este cliente alternativo que incluye la bifurcación suave con activación forzada de una u otra manera. No obtiene el apoyo que ustedes predicen que obtendrá o esperan que obtenga y provoca una ruptura de la cadena. ¿Qué versión es Bitcoin en ese caso?

LD: La comunidad tendría que decidirlo. No es algo que una persona pueda decidir o predecir. O el resto de la comunidad se actualiza o la gente que sí se actualizó no tendrá más remedio que revertir.

EL: En ese punto nos encontramos en un territorio desconocido en muchos sentidos. Tenemos que ver si los incentivos se alinean para que un número suficiente de personas quiera realmente apoyar una versión concreta de Bitcoin o no. Si hay un riesgo significativo de que pueda dividir la red permanentemente de una manera que no conduzca a un resultado decisivo, entonces no lo apoyaría. Creo que es importante que haya una alta probabilidad teórica de que la red tienda a converger. Los nodos económicos fuertes tenderán a converger en una blockchain concreta.

LD: También hay que tener en cuenta que no basta con no actualizar con algo así. Habría que bloquear explícitamente un bloque que rechace Taproot. De lo contrario, se correría el riesgo de que la cadena de Taproot superara su cadena y la sustituyera.

AvW: ¿Qué tipo de cronograma cree usted en este sentido? Luke, creo que te he visto mencionar un año. ¿Es eso cierto?

LD: Es importante que todos los nodos se actualicen, no sólo los mineros. Desde la fecha en que se hace el primer lanzamiento creo que tiene que haber al menos 3 meses antes de que pueda empezar la señalización. Una vez que comience, creo que un año estaría bien. Ni muy largo ni muy corto.

EL: Creo que un año podría ser un poco largo. Evidentemente, hay una contrapartida. Cuanto más corto sea el plazo, mayor será el riesgo de que no haya tiempo suficiente para que la gente se actualice. Pero, al mismo tiempo, cuanto más tiempo pase, mayor será la incertidumbre y eso también causa problemas. Es bueno encontrar el equilibrio adecuado. Creo que un año podría ser demasiado tiempo, no creo que vaya a tardar tanto. Preferiría que fuera más rápido. En realidad, me gustaría que esto ocurriera lo más rápido posible y que no causara una ruptura de la cadena o que redujera el riesgo de una ruptura de la cadena. Esa sería mi preferencia.

LD: No hay que olvidar que los mineros pueden señalar todavía y activarlo antes de un año.

EL: Claro, pero también está el tema del veto y la posibilidad de que la gente utilice la incertidumbre para jugar con los mercados u otras cosas por el estilo.

LD: No sé si hay un incentivo para intentar vetar cuando sólo se va a retrasar un año.

EL: Sí.

## Activación de la horquilla suave moderna

AvW: La otra perspectiva en este debate sería, por ejemplo, la de Matt Corallo [Modern Soft Fork Activation](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-January/017547.html). Supongo que lo conoce. Yo mismo lo explicaré rápidamente. Modern Soft Fork Activation, la idea es que básicamente se utiliza el proceso de actualización del BIP 9 a la vieja usanza durante un año. Deja que los mineros lo activen durante un año. Si no funciona entonces los desarrolladores lo reconsiderarán durante 6 meses, verán si después de todo había un problema con Taproot en este caso, algo que se les había pasado por alto, alguna preocupación que los mineros tenían con él. Revisarlo durante 6 meses, si después de los 6 meses se encuentra que no había ningún problema real y los mineros estaban retrasando por cualquier razón, entonces la activación se vuelve a desplegar con un plazo duro de activación a los 2 años. ¿Qué opina de esto?

LD: Si es posible que haya un problema, ni siquiera deberíamos llegar a ese primer paso.

EL: No soy muy partidario de esto porque creo que se plantean demasiadas preguntas. Si no parece que sea decisivo y no hay una decisión tomada, la gente va a estar totalmente confundida. Es causar mucha incertidumbre. Creo que es algo en lo que tenemos que ser muy agresivos y conseguir que todo el mundo se suba al carro y sea decisivo y diga "Sí, esto va a pasar" o no vale la pena hacerlo. No me gusta la idea de ver qué pasa en 6 meses o lo que sea. O decidimos de inmediato que sí lo vamos a hacer o no.

LD: Es una especie de invitación a la controversia.

AvW: Sin embargo, la idea es que, al establecer el plan de esta manera, sigue existiendo la garantía de que al final se activará. Puede que tarde algo más de un año, pero al final se activará.

LD: Eso es lo que se puede hacer con el BIP 8, sin fijar el tiempo de espera. Luego, si se decide, se puede fijar el tiempo de espera.

AvW: Hay variaciones. Hay diferentes maneras de pensar en esto. La verdadera pregunta a la que quiero llegar es ¿cuál es la prisa? ¿No estamos en esto a largo plazo? ¿No estamos planeando construir algo que estará aquí durante 200 años? ¿Qué importan uno o dos años más?

EL: Creo que para las pruebas y la revisión de la propuesta real de Taproot debería haber tiempo suficiente. No deberíamos precipitarnos. No deberíamos intentar desplegar nada hasta que los desarrolladores que están trabajando en ello y lo están revisando y probando estén seguros de que está a un nivel en el que es seguro desplegarlo, independientemente de todo el tema de la activación. Sin embargo, creo que la activación debería ser rápida. No creo que se tarde tanto en incorporar a la gente. Estamos hablando de un par de meses como máximo para que todo el mundo se suba a bordo, si es que va a suceder. Si se tarda más tiempo, lo más probable es que no tenga suficiente apoyo. Probablemente no deberíamos hacerlo en primer lugar. Si la gente no puede hacerlo tan rápido, creo que todo el proceso es cuestionable. Cuantas más variables añadamos al proceso, más se invitará a la controversia y más se confundirá la gente y pensará que es más incierto. Con este tipo de cosas, creo que la gente busca la decisión y la resolución. Mantener la incertidumbre y la espera durante un largo periodo de tiempo no es saludable para la red. Creo que la parte de la activación debería ser rápida. El despliegue debería llevar el tiempo necesario para asegurarse de que el código es realmente bueno. No deberíamos desplegar un código que no haya sido completamente probado y revisado. Pero una vez que decidamos que "sí, esto es lo que hay que hacer", creo que en ese momento debería ser rápido. De lo contrario, no deberíamos hacerlo en absoluto.

LD: La decisión, por supuesto, la toma la comunidad. Estoy de acuerdo con Eric.

AvW: Otro argumento a favor de la perspectiva de Matt es que el código debería ser bueno antes de desplegarlo, pero quizás en la realidad, en el mundo real, mucha gente sólo empezará a mirar el código, sólo empezará a mirar la actualización una vez que esté ahí fuera. Una vez que haya una versión de software que la incluya. Al no imponer inmediatamente la activación, se dispone de más tiempo para la revisión. ¿Qué opina usted?

LD: Creo que si la gente tiene algo que revisar debería hacerlo antes de que llegue a ese punto, antes de que se establezca la activación. Idealmente, antes de que se fusione.

AvW: Eric, ¿ves algún mérito en este argumento?

EL: Sin duda, cuantos más ojos lo miren, mejor, pero creo que es de suponer que nada se fusionará y se desplegará o se liberará hasta que al menos haya suficientes ojos competentes en esto. Ahora mismo creo que la gente más motivada es la que está trabajando en ello directamente. Puede que haya más ojos que lo miren después. Seguro que una vez que esté ahí fuera y una vez que se haya establecido la activación, recibirá más atención. Pero no creo que ese sea el momento en que la gente deba empezar a revisar. Creo que la revisión debería tener lugar antes.

LD: En ese momento, si se encuentra un problema, habrá que preguntarse: "¿Merece la pena volver a hacer todo esto sólo para solucionar ese problema o deberíamos seguir adelante de todas formas?". Si el problema es lo suficientemente grave, los mineros podrían activarse simplemente por el problema porque quieren aprovecharse de él. No queremos que se active si hay un gran problema. Tenemos que estar completamente seguros de que no hay problemas antes de llegar a la fase de activación.

## BIP 8 con señalización forzada

AvW: Déjame lanzar otra idea que ha estado circulando. ¿Y si hacemos un BIP 8 con señalización forzada hacia el final pero le damos un tiempo largo? Después de un tiempo siempre se puede acelerar con un nuevo cliente que incluya algo que obligue a los mineros a señalar antes.

LD: Con el BIP 8 actual no se puede hacer eso, pero Anthony Towns tiene un [pull request](https://github.com/bitcoin/bips/pull/950) que, con suerte, lo arreglará.

AvW: ¿Considera que esto tiene sentido?

EL: No creo que sea una buena idea. Cuanto más podamos reducir las variables una vez que se haya desplegado, mejor. Creo que deberíamos intentar solucionar todo esto antes. Si no se ha hecho antes, es que alguien no ha hecho bien su trabajo, es mi forma de verlo. Si las cosas se hacen bien, en el momento de la activación no debería haber ninguna controversia. Debería ser: "Saquemos esto y hagámoslo".

LD: Esa podría ser una razón para empezar con un plazo de 1 año. Luego podemos pasarlo a 6 meses si resulta ser demasiado tiempo.

EL: Then we are inviting more controversy potentially. Last time it was kind of a mess with having to deploy BIP 148 then [BIP 91](https://github.com/bitcoin/bips/blob/master/bip-0091.mediawiki) and then all this other stuff to patch it. The less patches necessary there the better. I think it sets a bad precedent if it is not decisive. If the community has not decided to do this it should not be done at all. If it has decided to do it then it should be decisive and quick. I think that is the best precedent we can set. The more we delay stuff and the more there is controversy, it just invites a lot more potential for things to happen in the future that could be problematic.

AvW: I could throw another idea out there but I expect your answer will be the same. I will throw it out there anyway. I proposed this idea where you have a long BIP 8 period with forced signaling towards the end and you can speed it up later if you decide to. The opposite of that would be to have a long BIP 8 signaling period without forced signaling towards the end. Then at some point we are going to do forced signaling anyway. I guess your answer would be the same. You don’t like solutions that need to be patched along the way?

EL: Yeah.

## Protocolo de osificación

AvW: La última pregunta, creo. A mucha gente le gusta la osificación del protocolo. Les gusta que Bitcoin, al menos en algún momento del futuro, no pueda actualizarse.

EL: Eso me gustaría.

AvW: ¿Por qué le gustaría eso?

EL: Porque eso elimina la política del protocolo. Mientras se puedan cambiar las cosas, se abre la puerta a la política. Todas las formas constitucionales de gobierno, incluso muchas de las religiones abrahámicas, se basan en esta idea de que tienes esta cosa que es un protocolo que no cambia. Cada vez que hay un cambio hay algún tipo de cisma o algún tipo de ruptura en el sistema. Cuando se trata de algo en lo que el efecto de red es un componente tan grande de todo esto y las divisiones pueden ser problemáticas en términos de que la gente no pueda comerciar entre sí, creo que cuanto menos política haya involucrada, mejor. La gente va a hacer política al respecto. Cuanto más se juegue, más se querrá atacar. Cuantos menos vectores de ataque haya, más seguro será. Estaría bien que pudiéramos conseguir que no hubiera más cambios en el protocolo en la capa base. Siempre va a haber mejoras que se pueden proponer porque siempre aprendemos a posteriori. Siempre podemos decir "podemos mejorar esto. Podemos hacer este tipo de cosas mejor". La cuestión es dónde ponemos el límite. ¿Dónde decimos "ya está bien y no hay más cambios a partir de ahora"? ¿Se puede hacer eso realmente? ¿Es posible que la gente decida realmente que el protocolo va a ser así? Además, hay otra cuestión: ¿qué pasa si más adelante se descubre algún problema que requiera algún cambio en el protocolo para solucionarlo? Algún tipo de error catastrófico o alguna vulnerabilidad o algo así. En ese momento podría haber una medida de emergencia para hacerlo, lo que podría no sentar precedente para que este tipo de cosas se conviertan en algo habitual. Cada vez que se invoca cualquier tipo de medidas de emergencia se abre la puerta a los ataques. No sé dónde está ese límite. Creo que es una cuestión realmente difícil.

AvW: Creo que Nick Szabo lo ha descrito como escalabilidad social. A eso se refiere. Cree que la osificación beneficiaría a la escalabilidad social.

LD: Creo que en un futuro lejano se puede considerar, pero en la etapa actual de Bitcoin, en la que se encuentra, si Bitcoin deja de mejorar eso abre la puerta a que las altcoins lo sustituyan y Bitcoin acabe siendo irrelevante.

AvW: ¿Dices que quizás en algún momento en el futuro?

LD: En un futuro lejano.

EL: Es demasiado pronto para decirlo.

AvW: ¿Tiene alguna idea de cuándo se hará?

EL: Creo que cualquiera que esté seguro de algo así está lleno de s\*\*. No creo que nadie entienda aún bien este problema.

LD: Hay demasiadas cosas que no entendemos sobre cómo debería funcionar Bitcoin. Hay demasiadas mejoras que se podrían hacer. En este momento parece que debería estar fuera de toda duda.

AvW: ¿Por qué sería un problema? Digamos que esta bifurcación suave falla por alguna razón. No se activa. Nos enteramos en los próximos 2 años que Bitcoin no puede actualizarse más y esto es todo. Esto es con lo que vamos a vivir. ¿Por qué es esto un problema? ¿O es un problema?

EL: Hay ciertos problemas que existen con el protocolo ahora mismo. La privacidad es uno de los más importantes. Podría haber otras mejoras potenciales en la criptografía que permitan una compresión mucho más sofisticada o más privacidad u otro tipo de cosas que serían significativamente beneficiosas. Si alguna otra moneda es capaz de lanzarse con estas características, tiene el problema de no tener el mismo tipo de historia fundacional que Bitcoin y ese tipo de mito creo que es necesario para crear un movimiento como este. Crea incentivos para los primeros jugadores... Lo que ha sucedido con las altcoins y todas estas ICOs y cosas así, los fundadores básicamente terminan teniendo demasiado control sobre el protocolo. Ese es un tema en el que creo que Bitcoin realmente mantiene su efecto de red sólo por eso. Pero podría haber alguna mejora técnica en algún momento que sea tan significativa que realmente Bitcoin estaría como una seria ventaja si no incorporara algo así.

LD: En este momento creo que es un hecho que lo habrá.

AvW: Has empezado mencionando la privacidad. ¿No es algo que crees que podría resolverse bastante bien en segundas capas tal y como está el protocolo ahora mismo?

EL: Posiblemente. No estoy seguro. No creo que nadie tenga una respuesta completa a esto, por desgracia.

LD: La definición de "suficientemente bueno" puede cambiar a medida que mejore la tecnología que invade la privacidad. Si los gobiernos, ni siquiera los gobiernos, cualquiera mejora en la invasión de la privacidad de todos lo que tenemos que proteger contra eso podría muy bien subir el listón.

## Taproot

AvW: Podemos hablar un poco de Taproot. ¿Es una buena idea? ¿Qué tiene de bueno Taproot? ¿Por qué lo apoya si lo apoya?

LD: Simplifica significativamente lo que tiene que ocurrir en la cadena. Ahora mismo tenemos todas estas capacidades de contratos inteligentes, que tenemos desde 2009, pero en la mayoría de los casos no es necesario tener el contrato inteligente si ambas partes ven que va a terminar de una determinada manera. Ambas partes pueden firmar una sola transacción y evitar todo lo relacionado con los contratos inteligentes. Este es el principal beneficio de Taproot. Puedes evitar todo el contrato inteligente en la mayoría de los casos. Entonces todos los nodos completos, tienen una verificación más barata, muy poca sobrecarga.

EL: Y todas las transacciones tendrían el mismo aspecto, por lo que nadie podría ver cuáles son los contratos. Todos los contratos se ejecutarían fuera de la cadena, lo que supondría una mejora significativa para la escalabilidad y la privacidad. Creo que es una victoria para todos.

LD: En lugar de que todo el mundo ejecute el contrato inteligente, son sólo los participantes.

EL: Que es la forma en que debería haber sido al principio, pero creo que tomó un tiempo hasta que la gente se dio cuenta de que eso es lo que el script debería estar haciendo. Al principio se pensó que podíamos tener estos scripts que se ejecutan en la cadena. Esta es la forma en que se hizo porque no creo que Satoshi pensó en esto completamente. Él sólo quería lanzar algo. Ahora tenemos mucha retrospectiva que no teníamos entonces. Ahora es obvio que realmente el blockchain se trata de autorizar transacciones, no se trata de procesar las condiciones de los contratos en sí. Todo eso se puede hacer offchain y se puede hacer muy bien offchain. Al final lo único que hay que hacer es que los participantes firmen que ha ocurrido y ya está. Eso es todo lo que le importa a todo el mundo. Todo el mundo está de acuerdo, así que ¿cuál es el problema? Si todo el mundo está de acuerdo, no hay ningún problema.

AvW: ¿No parece haber ningún inconveniente en Taproot? ¿Hay algún inconveniente, ha oído hablar de alguna preocupación? Creo que hubo un [email](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-February/017618.html) en la lista de correo hace un tiempo con algunas preocupaciones.

LD: No se me ocurre ninguna. No hay ninguna razón para no desplegarlo, al menos no se me ocurre ninguna razón para no usarlo. Sí que arrastra el sesgo de SegWit hacia los bloques más grandes, pero eso es algo que hay que considerar independientemente. No hay ninguna razón para vincular las características al tamaño del bloque.

AvW: Los bloques deberían seguir siendo más pequeños, Luke, ¿sigue siendo esa su postura?

LD: Sí, pero eso es independiente de Taproot.

AvW: ¿Hay alguna otra bifurcación suave que os entusiasme o que podáis ver desplegada en Bitcoin en los próximos dos años?

LD: Está ANYPREVOUT, que antes se llamaba NOINPUT, y creo que está progresando mucho. También está CHECKTEMPLATEVERIFY, al que todavía no he prestado demasiada atención, pero que parece contar con un importante apoyo de la comunidad. Una vez que Taproot se despliegue, probablemente habrá un montón de otras mejoras además de eso.

EL: Después de la última bifurcación suave, la activación de SegWit, estaba muy quemado por todo el proceso. Este asunto fue realmente un proceso de más de dos años. En 2015 fue cuando todo esto empezó y no se activó hasta el 1 de agosto de 2017. Eso es más de dos años de este tipo de cosas pasando. No sé si tengo ganas de una batalla muy prolongada con esto en absoluto. Quiero ver lo que sucede con Taproot primero antes de sopesar otros tenedores suaves. Taproot es el que parece tener el mayor apoyo en este momento en cuanto a algo que es una obviedad, esto sería bueno tener. Me gustaría ver eso primero. Una vez que se active, tal vez tenga otras ideas sobre qué hacer a continuación. Ahora mismo no lo sé, es demasiado pronto.

AvW: ¿Cuál es su opinión final sobre la activación de la horquilla suave? ¿Qué quiere decir a nuestros espectadores?

EL: Creo que es realmente importante que establezcamos un buen precedente. He hablado de tres categorías diferentes de riesgos. La primera categoría de riesgo es sólo la técnica, asegurándose de que el código no tiene ningún error y cosas así. La segunda es la metodología de activación y asegurarse de que la red no se divide. La tercera es con los precedentes. Invitando a posibles ataques en el futuro por parte de gente que explote el propio proceso. La tercera parte es la que creo que se entiende menos. La primera parte es la que más se entiende incluso en 2015. La segunda categoría es la que toda la activación de SegWit nos enseñó muchas cosas aunque estuviéramos hablando de BIP 8 y BIP 9. Los riesgos de la categoría 3 ahora mismo creo que son muy desconocidos. Esa es mi mayor preocupación. Me gustaría ver que no hay ningún tipo de precedente establecido donde este tipo de cosas podrían ser explotadas en el futuro. Es muy difícil trazar la línea exacta de lo agresivos que debemos ser con esto y si eso prepara algo para que alguien más en el futuro haga algo malo. Creo que sólo podemos aprender haciéndolo y tenemos que correr riesgos. Con el Bitcoin ya estamos en un territorio desconocido. Bitcoin ya es una propuesta arriesgada para empezar. Tenemos que asumir algunos riesgos. Deben ser riesgos calculados y debemos aprender sobre la marcha y corregirnos lo antes posible. Aparte de eso, no sé exactamente cómo acabará siendo el proceso. Estamos aprendiendo mucho. En este momento, creo que la categoría 3 es la clave que vamos a ver si esto ocurre realmente. Es muy importante tenerlo en cuenta.

AvW: ¿Luke, alguna reflexión final?

LD: La verdad es que no.

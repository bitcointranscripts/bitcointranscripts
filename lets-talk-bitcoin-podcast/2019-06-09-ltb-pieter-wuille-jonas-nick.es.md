---
title: The Tools and The Work
transcript_by: Michael Folkson
tags:
  - taproot
  - schnorr-signatures
speakers:
  - Pieter Wuille
  - Jonas Nick
date: 2019-06-09
---
<https://twitter.com/kanzure/status/1155851797568917504>

Parte 1: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-400-the-tools-and-the-work>

Parte 2: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-401-the-tools-and-the-work-part-2>

Borrador de BIP-Schnorr: <https://github.com/sipa/bips/blob/bip-schnorr/bip-schnorr.mediawiki>

Borrador de BIP-Taproot: <https://github.com/sipa/bips/blob/bip-schnorr/bip-taproot.mediawiki>

Borrador de BIP-Tapscript: <https://github.com/sipa/bips/blob/bip-schnorr/bip-tapscript.mediawiki>

## Parte 1

Adam: En este episodio vamos a adentrarnos en uno de los cambios más importantes que llegarán pronto al protocolo de Bitcoin como BIPs o Propuestas de Mejora de Bitcoin (“Bitcoin Improvement Proposals”), con foco en Taproot, Tapscript y firmas Schnorr. Si nos sintonizas regularmente esta no va a ser la primera vez que escuches la mayoría de estas ideas generales, pero hoy queremos analizarlas en profundidad. Debido a eso es que estamos muy complacidos de tener con nosotros en la sesión de hoy a los desarrolladores de Bitcoin Pieter (mejor conocido como Sipa) y a Jonas Nick. Caballeros, muchas gracias por su tiempo y por estar hoy con nosotros.

Stephanie: Quiero sumarme a lo dicho por Adam. Muchas gracias por estar en el show con nosotros. Es realmente maravilloso discutir estas propuestas de mejora para Bitcoin y hablar con personas que realmente conocen el tema porque, de hecho, están involucradas en su desarrollo. Sinceramente les agradecemos por su tiempo. Para empezar quisiera preguntarles a ambos, Pieter y Jonas, ¿cómo fue la primera vez que escucharon sobre Bitcoin? ¿Cómo fue que se volvieron desarrolladores de Bitcoin? ¿Y por qué están interesados en estas propuestas en particular? Pieter, ¿quieres empezar tú?

Pieter: Creo que me topé con Bitcoin por primera vez a fines del 2010 en un canal de IRC acerca del lenguaje de programación “Haskell”, donde los participantes estaban hablando acerca del tema, y luego comencé a investigar por mi cuenta. Me dí cuenta de que en aquel tiempo tenía una placa de video en mi computadora que era capaz de minar Bitcoins. Fue divertido. En un principio solo me fijé en eso. El precio estaba muy bajo en aquel momento. Valía alrededor de veinte centavos.

Stephanie: ¿Y qué te entuciasmó de Bitcoin en aquel momento?

Pieter: Fue la lidea de que se podía tener una moneda definida por internet, por nada más que software. Siempre fue su tecnología lo que me atrajo, y su potencial de cambiar la manera en que pensamos el dinero.

Stephanie: ¿Y cuándo empezaste a desarrollar para Bitcoin?

Pieter: Creo que empecé a mirar el código a inicios del 2011. Creo que fue en el mismo momento en que SlushPool estaba empezando y estaban buscando realizar unos cambios en el código. Así que pensé, ¿por qué no echarle un vistazo? Un poco más tarde, en el foro de bitcointalk que en aquel momento creo que solo estaba en bitcoin.org, Hal Finney publicó un desafío: “Esta es una dirección de Bitcoin. En ella hay 5 Bitcoins (eran un puñado de dólares en ese momento). Y una clave privada. Cualquiera que pueda reclamar esos Bitcoins con esa clave privada se los puede quedar”.

Stephanie: ¿Ganaste?

Pieter: No, no gané. En aquel entonces el software existente para Bitcoin no permitía importar o exportar claves privadas, así que eso era algo nuevo. Empecé a pensar, ¿cómo podría incluir esta funcionalidad en el software de Bitcoin? Me tomó más tiempo que a otras personas que estaban intentando lograr lo mismo en Java o Python. Pero al final logré tener un parche para importar claves privadas en Bitcoin. Intenté integrarlo porque parecía una funcionalidad interesante. En ese momento comencé a hablar con Gavin Andresen, quien recientemente había asumido como persona a cargo del soporte del proyecto. Me parece que pasó medio año hasta que el parche fue integrado. Pero antes de que eso sucediera ya me habían pedido contribuir y empezar a revisar los parches de otras personas.

Stephanie: Eso es fascinante. Me gusta mucho tu historia. ¿Has estado desarrollando activamente durante todo este tiempo? ¿Y cómo fue que te interesaste por Taproot, Tapscript y las firmas Schnorr?

Pieter: Sí, he estado desarrollando todo este tiempo. Inicialmente sólo lo hacía en mi tiempo libre y luego, tan pronto me uní a Blockstream en 2014 pude hacerlo a tiempo completo. Desde entonces he trabajado en muchas cosas. Taproot y las demás cosas relacionadas son una continuación de la iniciativa sobre “Segregated Witness” que inició hace un par de años.

Stephanie: ¿Estás interesado en la escalabilidad y en la seguridad?

Pieter: Sí, por supuesto. La ventaja principal aquí es mejorar las cosas que iniciamos con “Segregated Witness”. Con esto en particular mejoramos el potencial de fungibilidad o intercambio, haciendo que todas las transacciones o al menos una gran parte de ellas sean más parecidas entre sí, siendo menos visible para el público en general qué es lo que realmente hacen las transacciones. Al mismo tiempo hay mejoras de escalabilidad. Son mejoras menores para las transacciones típicas. Tienen mayor impacto en transacciones más complejas, como transacciones multi-firma (“Multisig”) o contratos inteligentes.

Stephanie: Vamos a hablar de los detalles técnicos en un rato. Muchas gracias por la introducción y por relatarnos tu experiencia. Ahora vamos con Jonas. ¿Cuándo fue la primera vez que escuchaste sobre Bitcoin y cómo fue que te involucraste como desarrollador Bitcoin?

Jonas: La primera vez que escuché sobre Bitcoin fue a inicios del 2011. Sucedió una burbuja, creo que alrededor de los 30 USD, y al instante estuve muy interesado en esta idea de utilizar una moneda con la cual nadie pueda detenerme y al mismo tiempo, mantener un cierto grado de privacidad al usarla. De hecho, en 2013 y 2014 yo escuchaba tu podcast regularmente. Allí escuché por primera vez hablar sobre cadenas paralelas y Blockstream. Lo busqué, fue en el [Episodio 99](https://letstalkbitcoin.com/e99-sidechain-innovation) con Adam Back y Austin Hill. Fue una gran influencia en aquel momento.

Stephanie: Es una historia genial.

Adam: Recuerdo aquella entrevista. Sin dudas presentaron ideas muy interesantes en aquellos inicios.

Stephanie: Y dinos Jonas, ¿cómo te iniciaste como desarrollador?

Jonas: Comencé a contribuir cuando estaba en la universidad. Ese mismo año estudié ciencias de la computación. Luego de eso, en 2015, me uní a Blockstream.

Stephanie: En este punto quisiera pasar a los detalles técnicos. Vamos a hacerles muchas preguntas. Creo que deberíamos iniciar por definir exactamente a qué nos referimos cuando decimos Taproot, Tapscript o firmas Schnorr. Hemos decidido iniciar con las firmas Schnorr y el motivo por el cual son importantes.

Pieter: Actualmente Bitcoin utiliza firmas ECDSA para permitir que las claves firmen las transacciones. Una dirección, al menos cuando es una generada con una sola clave, realmente es solo un hash de una clave pública ECDSA. Y cuando recibes monedas en esa dirección y deseas gastarlas, necesitas firmar usando la correspondiente clave privada ECDSA. El algoritmo ECDSA tiene una historia interesante, es el esquema de firmas DSA que es bastante común, migrado al mundo de la criptografía de curvas elípticas. El esquema de firmas DSA fue diseñado originalmente en gran medida como una manera de evitar la patente existente sobre las firmas Schnorr. Las firmas Schnorr fueron inventadas por Claus-Peter Schnorr creo. Con el correr del tiempo las personas fueron encontrando propiedades interesantes y cosas que se podían hacer con ellas. Pero lamentablemente él patentó la idea. Como resultado el mundo intentó estandarizar una alternativa que no estuviera patentada, que fue DSA. Luego vino ECDSA, y Bitcoin en sus inicios aparentemente tomó esta implementación. Así es que, en esencia, las diferencias entre ECDSA y la curva elíptica Schnorr no son grandes.

Stephanie: ¿Quieres decir que es una forma distinta de firmar transacciones?

Pieter: Correcto. Es incluso algo de más bajo nivel, es la primitiva que se usa para producir la firma. Sin embargo, existen un número de propiedades de estos esquemas de firma en las que estamos interesados. Una de ellas en particular es que estas firmas son lineales. Lo que esto significa en la práctica es que podrías tomar a un grupo de personas, tomar sus claves públicas, combinarlas en una única clave pública, y ahora aquellos participantes de quienes tomaste las claves públicas pueden, en conjunto, producir una firma para la clave pública combinada. Esta es una forma muy compacta de hacer lo que en Bitcoin denominamos “firmas múltiples” (“Multisignatures”). En particular las que son n-de-n. Tienes un grupo de tres firmantes y deseas que los tres firmen algo. En lugar de necesitar colocar tres claves públicas en la blockchain, simplemente pones una. Y en lugar de tener una firma por cada uno, solo tienen una.

Stephanie: No solo parece más eficiente, sino también y más importante, más privado porque se expone menor cantidad de información.

Pieter: Exacto. En general cuando se expone menos información se revela menos. Pero en particular lo que se gana aquí es que tu expones menos acerca de tu política al mundo. Imagina una billetera nueva (hardware o software) que sale al mercado, y son los único en el mundo que usan multifirmas 5-de-7. Si usas ese software va a ser muy obvio para todo el mundo cuáles son las transacciones que se crearon con esa nueva billetera. Lo que se intenta es reducir la cantidad de información que se expone transformando casi todo en una sola firma. Hasta ahora sólo he hablado acerca de las firmas n-de-n pero hay formas de obtener mejoras similares, no tan grandes pero similares, para firmas k-de-n u otras políticas también.

Stephanie: ¿Qué es k-de-n?

Pieter: k-de-n es por ejemplo 2 de 3, donde k es distinto de n.

Andreas: Eso es lo que solemos llamar m-de-n.

Stephanie: Es decir que solo estamos usando otra letra. Eso me confundió.

Pieter: m y n suenan muy parecido, por lo que empecé a usar k y n.

Stephanie: Muy ingenioso, gracias. Por favor, continúa.

Pieter: Cuando hablamos de k-de-n o límites, se tienen un número de participantes que se espera que firmen, pero solo se necesita de un subgrupo para firmar. Cuando hablamos de multifirmas o n-de-n se trata de un grupo de participantes y todos ellos tienen que firmar. Las firmas Schnorr permiten hacer n-de-n de una manera muy eficiente porque todo se traduce en una clave única con una firma única. De todas maneras se pueden hacer mejoras similares usando técnicas más avanzadas para k-de-n.

Jonas: Habría que destacar que hay investigaciones recientes que demuestran que se pueden hacer algunas de estas cosas con ECDSA también, en particular n-de-n. En la práctica son difíciles de implementar y requieren nuevas suposiciones. En particular si se pretende tener una implementación que sea resistente a un ataque de canal lateral (“side-channel”), eso es complicado de lograr con estos esquemas ECDSA.

Pieter: Exacto Jonas. Estas cosas se pueden hacer con ECDSA también pero en el caso de las firmas Schnorr, gracias a la propiedad de linealidad es mucho más sencillo. Para ser más correcto, es más sencillo y más eficiente, y la sobrecarga de protocolo es menor.

Andreas: Una pregunta sobre ese tema. En base a lo que leí entiendo que existe una forma de producir una prueba formal de algunas de las propiedades de seguridad de Schnorr que es de un valor particular para una solución como Bitcoin.

Pieter: Si, las firmas Schnorr pueden ser comprobadas como seguras bajo la suposición de que internamente usa un hash. Si modelamos el hash como un oráculo al azar y asumimos que el problema de logaritmo discreto en grupos de curvas elípticas es complejo, con eso se puede probar que las firmas Schnorr son seguras. Lo mismo no aplica a ECDSA. Algunas personas han intentado y creo que no existe una duda razonable de que será hackeado, pero es bueno tener una prueba formal para estas cosas.

Stephanie: ¿Qué pasó con la patente que se había obtenido originalmente sobre esto? Al inicio dijiste que esta tecnología estaba patentada y no se pudo incorporar a Bitcoin.

Pieter: En realidad se podría haber incorporado, la patente venció en 2008. Lo que la patente causó es que la gente no usara firmas Schnorr y se estandaricen otras tecnologías en su lugar. El creador de Bitcoin solo eligió lo que estaba disponible y ECDSA era el estándar, lo suficientemente pequeño y rápido, con lo que al cumplir con todos los requerimientos fue la opción obvia.

Stephanie: ¿Schnorr cambió de idea al respecto de la patente?

Pieter: Hasta donde yo sé él siempre sostuvo que DSA en realidad infringía su patente.

Jonathan: Esta siempre fue una pregunta que me hice. Escucho que Bitcoin es descentralizado y siempre intento entender lo que eso implica y lo que no. Uno escuchó hablar sobre quién tiene el control de Bitcoin y quién está realmente a cargo y es responsable por el proyecto. Escuchamos todas las protecciones que los contribuyentes a Bitcoin Core toman respecto de la libre opinión por contribuir al repositorio pero aclarando que no son los actores comerciales que participan en las actividades, que es por lo que existen fuertes protecciones para las contribuciones de código abierto (open source). ¿Por qué algo como una patente supondría un freno para que una tecnología superior sea implementada en un repositorio de un proyecto descentralizado y de código abierto? No entiendo dónde está el factor limitante. ¿Fue sólo debido a que las bibliotecas no eran estándares como mencionaste antes?

Pieter: Para ser claro, la razón por la que Bitcoin no eligió Schnorr desde el inicio es simplemente porque no estaba estandarizado. Y no estaba estandarizado porque anteriormente estaba patentado. Si te refieres a ahora, ¿sería posible incorporar tecnología patentada en Bitcoin o en sus implementaciones? No soy un abogado pero pienso que sería al menos una preocupación, incluso si no existe un problema legal al hacerlo. Y uno no quiere que los usuarios se tengan que preocupar acerca de si pueden o no usar el software. La pregunta no es solo si esta es la tecnología apropiada, también hay que preguntarse: ¿esperas que el ecosistema la adopte? Cuando hay trabas como ser patentes la pregunta es mucho más compleja.

Adam: Se torna más controversial si se pretende incluir algo como eso porque tendrías que responder esa pregunta. En cambio la forma en que está el protocolo ahora no presenta ninguna duda acerca de si infringe patentes.

Andreas: La pregunta sobre la estandarización es interesante, me gustaría explorarla un poco más. Por lo que yo entiendo, la implementación de Schnorr en Bitcoin, la implementación de Schnorr propuesta lleva a estandarizar no sólo cómo se codifican las firmas Schnorr, cómo se representan, sino que también hubo mucho desarrollo alrededor de las multifirmas con Schnorr en un protocolo llamado Musig en el que también participaste. ¿Bitcoin está marcando el camino para la estandarización con Schnorr?

Pieter: Existen un número de esquemas de firma que en esencia están basados en Schnorr pero no tienen ese nombre. Uno de ellos es ed25519.

Andreas:  ¿Que es el de Apple?

Pieter: No tengo idea, pero no me sorprendería. En esencia es también una especialización de un esquema basado en Schnorr en un estándar práctico. No podemos usar ed25519 por varias razones. Una de ellas es que queremos mantener compatibilidad con el sistema actual de clave pública que tenemos, de modo tal que cosas como BIP32 y todo lo que se construyó sobre eso no quede invalidado. No sería algo terrible, pero es lo suficientemente sencillo mantener la compatibilidad así que definimos una firma Schnorr sobre la curva secp256k1 que es la misma curva sobre la cual está actualmente definido el esquema ECDSA de Bitcoin.

Andreas: La curva no cambia, lo que significa que el espacio de clave privada tampoco cambia. ¿Mantiene el mismo orden primario?

Pieter: Las claves públicas permanecen iguales.

Andreas: ¿Y es por eso que podemos reusar las codificaciones actuales y, de hecho, derivar claves privadas, públicas y firmas con el mismo conjunto de tecnologías estándares que tenemos? Por ejemplo, las semillas mnemónicas basadas en BIP39 y billeteras jerárquicas determinísticas con BIP32, etc. Esa es una ventaja enorme.

Stephanie: ¿Significa eso que se requiere un soft fork para incorporar el cambio?

Pieter: Si, así sería.

Andreas: Es decir que por la introducción de las versiones de script en v0 de SegWit, estas propuestas ahora serían … v1 SegWit, la segunda edición de SegWit en esencia.

Pieter: Correcto. Debido al mecanismo de versionamiento de script podemos hacer propuestas que cambian por completo el sistema de script o cualquier otra cosa en ese contexto y todo se mantendría como un simple soft fork. De lo contrario habría que intentar amoldarlo de alguna forma para meterlo dentro de los códigos OP existentes (como tuvimos que hacer en el pasado).

Andreas: Hace dos años cuando comenzamos a hablar de SegWit predijimos que ese sería uno de los principales beneficios porque provee una gran flexibilidad para realizar actualizaciones usando soft forks. Las otras dos propuestas que se presentaron, Tapscript y Taproot que también incorpora MAST, los Árboles de Sintaxis Abstractos de Merkel (Merkelized Abstract Syntax Trees - MAST), también se están proponiendo como soft forks. Una de las cosas que me parece muy interesante es que se están proponiendo como un conjunto, es decir al mismo tiempo. Eso está muy relacionado con la combinación de funcionalidades que proveen el mejor conjunto de funcionalidades de privacidad para que no sea evidente que se están usando nuevas técnicas de privacidad. ¿Podrías hablar un poco más sobre lo que es Taproot y cómo se relaciona con Schnorr and MAST? ¿Y por qué se presentan como un conjunto de propuestas unificadas?

Pieter: Con gusto. Si arrancamos desde la perspectiva de las reglas de consenso, se necesita iniciar con Taproot. BIP-Taproot propone semánticas para SegWit v1. La forma de mirar a Taproot es que se trata de una generalización que combina las políticas de pagar-a-clave pública (pay-to-publickey) o pagar-a-única clave pública (pay-to-publickey single key) y pagar-a-hash de script (pay-to-scripthash). En cierto sentido toda salida se convierte en ambas. Todo se convierte en una combinación de una clave o un script. Es decir que cuando le pagas a alguien, cuando obtienes una dirección ya no será posible ver si los fondos van a una clave o a un script. Podría ser cualquiera de los dos, y a la persona que envía no le interesa, a la red no le interesa, nadie lo ve. Cuando deseas gastar esa salida tienes dos opciones. O demuestras que conoces la clave privada asociada y luego puedes gastar los fondos, o demuestras que realmente era una dirección que fue derivada de un script. Provees el script, lo demuestras y luego lo dejas a un lado. La cualidad maravillosa que se obtiene es que nunca se revela cuál de estas opciones se usó. Todavía se podrá tener salidas que son sólo a una clave o sólo a un script y no se podrán distinguir entre ellas. Cuando se gastan los fondos no se revela si la otra opción existió en primer lugar o si ambas existieron. Como resultado, si tienes una salida a una clave o a un script complejo pero ahora la gastas usando la clave, eso se ve completamente idéntico a un pago estándar de clave única que se está gastando.

Andreas: Veamos un ejemplo práctico que se me acaba de ocurrir. Uno de los ejemplos donde podrías utilizar esto en el futuro es tener un contrato inteligente complejo que implica colaboración entre partes como un canal Lightning. Los canales Lightning son 2-de-2 multifirmas. Cuando se cierran cooperativamente entre las dos partes (lo que sucede la mayor parte del tiempo, así es como debería ser), en lugar de decirle al mundo “este es un canal” liberando un script largo y explícito a la cadena cuando se realiza el gasto para cerrar el canal, las dos partes que ya se encuentran en comunicación en la red persona-a-persona de Lightning podrían simplemente crear una firma Schnorr compuesta y gastar usando la clave pública sin revelar que se trataba de un canal. Se vería como que alguien simplemente gastó un pago, nadie sabe que se trataba de un canal Lightning originalmente. Aquí es donde se usa una multifirma cooperativa n-de-n donde todas las partes firman. ¿Es correcto?

Pieter: Totalmente correcto. Esa es también la razón por la cual Schnorr se integró en esto. Estamos asumiendo que la mayoría de los contratos pueden tener esta alternativa cooperativa que simplemente consta de un número o de la totalidad de los participantes del contrato estando de acuerdo. Gracias a la propiedad lineal de las firmas Schnorr esas cosas se pueden transformar en una clave única. Tan pronto como se transforma en una clave única, Taproot logra que todo sea más eficiente haciéndolo ver en la cadena como una firma única.

Andreas: ¿Es esto una ventaja tanto en la privacidad como en la escalabilidad?

Pieter: Es una ventaja en los dos aspectos. Todo lo que se ve en la cadena es una clave pública única cuando se realiza el pago, y una clave única cuando se gasta, eso es todo. Esto se relaciona con tu pregunta sobre agrupamiento. Aquí participan un conjunto de tecnologías. Ya hemos mencionado dos, la construcción Taproot y Schnorr. Schnorr por sí mismo sólo provee multifirmas un poco mejores, y Taproot por sí mismo no hace mucho, a menos que tengas esta rama cooperativa que suponemos va a ser utilizada la mayor parte del tiempo. Pero juntas son mucho más poderosas. A ellas se le agregan algunas cosas más. Los árboles Merkle son una ventaja obvia. Agregar los árboles Merkle mientras se están incluyendo los otros cambios es muy sencillo. Y significa que ahora ya no son dos alternativas, tener una clave o un script, sino que pasamos a tener una clave o uno de muchos posibles scripts. Sigue siendo eficiente incluso cuando se tienen miles, incluso millones de posibles pequeños scripts. La ventaja en este caso es similar: se revela menos información al mundo acerca de lo que cada uno está haciendo. Se sigue revelando el script que se usa pero no todos los demás scripts que podrían estar involucrados en el contrato.

Adam: Para resumir, en el modo anterior tenemos métodos específicos para distintos tipos de usuarios y usos. Debido a eso es posible o incluso es sencillo detectar una transacción normal de algo como una multifirma o simplemente un contrato inteligente. Con el nuevo modo tenemos un único método unificado con el cual, debido a que todo se ve idéntico, se mejora la privacidad de forma dramática al mismo tiempo que se obtienen los demás beneficios de los que estuvimos hablando.

Pieter: Sí, es correcto.

## Parte 2

Pieter: Hay algunas cosas más que Taproot intenta lograr. Una de ellas es una mayor eficacia en la verificación porque existe otra característica de las firmas Schnorr que es la posibilidad de realizar verificaciones en lote. Esta es una manera de, si te dan mil firmas cada una con su respectiva clave pública y el mensaje que quieres verificar, puedes determinar si todas ellas son válidas más rápido que verificar cada una individualmente. La desventaja es que si la verificación en lote falla no tienes idea cuáles firmas eran inválidas. En general en los bloques de Bitcoin no nos importa eso. Lo que nos importa es si el bloque en su totalidad es válido o no. Esta propiedad de la verificabilidad en lotes que es de un factor 2, 3, 4 a veces, dependiendo de cuántas cosas se combinan juntas, queríamos mantener esa propiedad incluso luego de integrarlo al sistema de script. Con esto en mente hay algunos códigos OP en el lenguaje de scripting que son incompatibles con esta funcionalidad. Uno de ellos es CHECKMULTISIG. Es interesante que tenemos mejores formas de hacer multifirmas ahora, pero incluso sin ellas el código OP CHECKMULTISIG no puede mantenerse en su forma actual. Se han dado un número de claves públicas y un número de firmas y el verificador tiene que intentar determinar qué clave pública corresponde a qué firma, y no podemos procesar en lote ese ejercicio de prueba y error. Así que nos vimos forzados a hacer unos pequeños cambios al lenguaje de scripting para mantener la compatibilidad con la verificación por lotes. Así surgió Tapscript. Tapscript es la modificación al lenguaje de scripting para los scripts de Taproot. Creo que es un documento separado por dos motivos. Uno, BIP-taproot se estaba tornando muy extenso. Además, y esto considero que es otra característica importante, BIP-Taproot se enfoca en la flexibilidad. En el árbol Merkle de BIP-Taproot cada hoja es un script combinado con lo que llamamos una versión hoja. Este es un esquema de versionamiento muy similar al sistema de versionamiento de script de SegWit salvo por el hecho de que éstas no son reveladas al momento del pago. Sólo se revelan al momento del gasto. Y todavía más interesante es que cada hoja puede tener diferentes versiones y sólo se revela la que se está utilizando. Se obtiene una ventaja potencial de privacidad porque, por ejemplo, si se realiza una mejora de script que solo es necesaria en una rama del contrato, esta información no se va a revelar a menos que se utilice dicha rama. Tapscript es la versión 0 propuesta para la versión de hoja bajo Taproot. Como en un futuro podrían existir nuevas y distintas es que se crea un documento separado. Si es la versión 0 hay que leer BIP-Tapscript. Si es otra cosa por ahora no tiene trabas, pero propuestas futuras podrían redefinir esto. ¿Tiene sentido?

Andreas: Por supuesto, al menos para mi. Entonces Pieter, en términos de verificabilidad por lotes, lo que entiendo es que hay tres o más niveles diferentes de verificabilidad por lotes. Se pueden verificar múltiples firmas en un solo script, se pueden verificar muchas firmas a través de las entradas de una única transacción y luego se pueden verificar firmas a través de muchas entradas provenientes de múltiples transacciones, incluso tal vez hasta un bloque entero. ¿De cuál nivel de verificabilidad por lotes estamos hablando?

Pieter: De todos ellos. Estos niveles incrementales que mencionaste, son cada uno más complicado de integrar en el software que el otro, pero no hay nada que impida que la verificabilidad por lotes verifique toda la cadena en una sola operación.

Adam: Verificar en lote toda la cadena tendría como resultado confirmar efectivamente que la cadena completa es válida y si existen transacciones o acciones dentro de él que son inválidas entonces todo el conjunto sería inválido. En teoría podrías hacer eso y debería funcionar incluso a esa escala.

Pieter: Es correcto. Probablemente no sea algo que desees hacer a medida que se reciben los bloques individuales, pero para verificar la historia sí podría ser útil. Andreas, tengo que destacar que estamos hablando de verificabilidad por lote. Existe otra propiedad llamada agregación, y ahí las cosas son distintas. Cuando hablamos de verificabilidad por lotes todas las transacciones, todas las firmas, todas las claves públicas individualmente todavía forman parte de la cadena. Es solo una forma más rápida de verificarlas a todas al mismo tiempo.

Andreas: ¿Esto es básicamente una optimización de la utilización de CPU y memoria en el cliente que está verificando la cadena?

Pieter: Sí, totalmente. Es justamente eso, y la implementación de referencia ni siquiera hace eso en este momento. La propuesta en su totalidad fue diseñada para hacer posible esta optimización. En contraste con eso existe la agregación de firmas que es una tecnología con la cual se reduce efectivamente el número de firmas que forman parte de una transacción o un bloque. Por ahora BIP-Taproot y Tapscript como están solo soportan formas de agregación para inputs simples, múltiples claves dentro de un solo input. Uno es a través de Musig, una construcción donde se descartan las claves públicas, se combinan todas y se obtiene una única firma. Existen formas más avanzadas de habilitar una mayor agregación pero no están incluidas.

Andreas: Pero tampoco se evitan con lo cual existe una posibilidad de que en el futuro se pueda tener tal vez una transacción con tres o cuatro inputs y se pueda tener agregación de firmas de forma tal que se use una sola firma para toda la transacción. Y luego tal vez incluso más adelante todas las firmas en un bloque sean de ese estilo, que incluso se pueda agregar un bloque entero en una sola firma.

Pieter: Si, no se evita eso, pero requerirá un sucesor de Taproot. La agregación transversal a varios inputs probablemente no sea parte de BIP-Taproot.

Andreas: En términos de adopción no tenemos un cronograma para el soft fork que introducirá estos BIPs en la mainnet. Pero asumamos que fueron puestos en la versión oficial (en un futuro). Obviamente esto sería una cadena híbrida donde ECDSA, que por supuesto todavía existe, uno de los principios en Bitcoin es que nadie invalida UTXOs antiguos que todavía están pendientes. Cualquiera puede traer cualquier cosa desde el mismísimo primer bloque y debería ser posible de gastar. En el punto en que ECDSA y Schnorr ya están coexistiendo en los bloques, tal vez incluso en transacciones simples, algunos inputs podrían ser ECDSA, algunos podrían ser Schnorr, otros podrían ser mixtos. ¿Cómo afecta eso la verificación en lotes, digamos desde el punto de vista de una transacción? ¿Se realiza simplemente una verificación en lote de las firmas Schnorr y luego por separado se verifican las firmas ECDSA?

Pieter: Sí, así es exactamente como funciona. Se obtienen las mejoras pero solo aplican a las firmas Schnorr.

Andreas: ¿Y así cuanto más adopción haya de las firmas Schnorr, cuanto más billeteras migradas y cuanto mayor sea la cantidad de nuevos UTXOs que tengan Schnorr, mayor es el beneficio que obtiene la red en su totalidad?
Stephanie: Igual que SegWit.
Pieter: La diferencia aquí por supuesto es que no hay beneficios reales para el usuario en la verificabilidad por lotes. No hay un descuento por habilitarlo más allá del hecho de que las firmas Schnorr son un poco más pequeñas. Yo espero que haya suficientes incentivos cuando las firmas Schnorr sean adoptadas en forma masiva para aportar una mejor significativa, aunque esto puede llevar un tiempo prolongado claro está.

Jonas: Con las firmas Schnorr y las firmas ECDSA, si no se considera la verificación por lotes, son similares en cuanto a la rapidez. Ahora teniendo en cuenta la verificación por lotes las firmas Schnorr se tornan más rápidas. Si miro los números aquí, si tienes 10 firmas las puedes validar 1,5 veces más rápido por ejemplo. O si tienes el número de firmas en el orden de un bloque, por ejemplo un par de miles, entonces obtienes una mejora de 2,5 veces respecto de validarlas todas una por una. Haciendo lo que la implementación define, cuando ves una transacción puedes intentar realizar una verificación en lote. Pero si una verificación en lote falla no puedes saber qué firma en particular es la que falló. Creo que esto es solo un desafío de ingeniería: decidir cuándo usar la validación por lotes y cuándo no.

Andreas: Asumo que uno de los grandes beneficios, especialmente en el largo plazo, es mantener el tiempo de descarga de bloque inicial (IBD - iniciales en inglés de "Initial Block Download"). Así se llama al proceso que se realiza cuando se crea un nodo nuevo y hay que iniciar a descargar y verificar desde el bloque génesis en adelante. Siempre es deseable poder lograr que dicho tiempo no crezca. Cuanto más transacciones, más bloques, y más tarda el proceso. Bitcoin Core ha podido a lo largo de los últimos años parar el reloj agregando optimizaciones tan rápido como el número de bloques crecía, de manera tal que la descarga inicial no tome mucho más tiempo. En algunos casos es incluso más rápido que lo que era en el pasado. Con la verificación por lotes que permite Schnorr, cuando se verifican bloques que ya habían sido minados donde las transacciones son supuestamente válidas a menos que se esté evaluando una cadena de bloques fraudulenta, ¿sería esto una mejora significativa para la escalabilidad del proceso de IBD?

Pieter: Es otro factor que se agrega. Siempre hasta el punto donde el proceso de IBD se compone principalmente de la validación de firmas. En la mayoría de los sistemas creo que en realidad la mayor parte del proceso se dedica a acceder al conjunto de transacciones no gastadas (UTXO).

Adam: ¿IBD? Por favor, ¿qué significa?

Stephanie: Enfermedad de Colon Irritable (del inglés Irritable Bowel Disease)

Andreas: Descarga de Bloques Inicial

Stephanie: Perdón, es mi formación en medicina.

Andreas: Si tu nodo tiene una cantidad insuficiente de RAM sucede lo mismo.

Adam: ¿Entonces básicamente lo que dices es que la ventaja de la que estábamos hablando, que se puede descargar la cadena de bloques completa y que podrías potencialmente verificar, sólo tendría lugar cuando hablamos de firmas Schnorr?

Pieter: Si.

Adam: Durante ese período de transición donde tenemos muchas firmas Schnorr pero también tenemos muchas firmas no Schnorr en el mismo bloque, ¿es posible verificar en lote dicho bloque o sólo estarías verificando en lote las transacciones con firmas Schnorr de dicho bloque?

Pieter: Exacto. Sólo se podrían verificar en lote las firmas Schnorr.

Andreas: En el pasado cuando hablamos de estos próximos BIPs una de las funcionalidades que se ha discutido bastante es lo que se conoce como SIGHASH_NOINPUT. Para recordarle a nuestros oyentes que hay algunas propuestas en la red Lightning para cambiar la manera en que trabaja el protocolo en una formulación llamada “eltoo” que simplifica en gran medida el uso de los canales de Lightning haciendo innecesario el uso de los cierres por penalidad en el caso de intentar hacer trampa mediante la transmisión de un estado anterior que ya fue invalidado. Eso requiere un cambio en el script de Bitcoin y especialmente en la manera en que las firmas se aplican a las transacciones, lo que se denomina el sistema SIGHASH, de manera que te permite a ti reasociar la transacción a un input diferente. Eso es lo que se denominó SIGHASH_NOINPUT, y tiene otros nombres porque hay varias formulaciones que se han propuesto. ¿Se ha incluido eso como parte de Tapscript?

Pieter: No.

Andreas: ¿Se ha propuesto o discutido su potencial inclusión?

Pieter: BIP-Tapscript incluye un número de mejoras al esquema de sighashing pero no incluye SIGHASH_NOINPUT. El motivo es que hubo muchas discusiones sobre varias alternativas de implementación, varias formas de lograrlo de forma segura. Toca algunas cosas esenciales de la manera en que las transacciones firman datos previos, de dónde vienen las cosas. El potencial de romper eso es aterrador. Entonces nos dimos cuenta que en lugar de incluirlo directamente podemos incluir un número de mecanismos de flexibilidad en Taproot y Tapscript que nos permitirían hacer cosas como esta en el futuro sin ningún riesgo. En particular, los tipos de flexibilidad que existen creo que se están versionando como mencioné antes. Otro es OP_SUCCESS. Dentro de Tapscript una gran parte de los códigos de operación (OP codes) que antes eran inusables pasan de ser un “retornar falso” a ser un “retornar verdadero”. En cualquier lugar donde alguno de esos códigos de operación aparece dentro de tu script, representarían que puedes gastar esos outputs sin ninguna condición, exactamente igual que futuras versiones de SegWit o futuras versiones de hojas. La ventaja práctica de esto es que se puede redefinir dichos códigos de operación para ser cualquier otra cosa, no necesitan ser compatibles hacia atrás con un OP_NOP, que es lo que sucede ahora. Un tercer mecanismo es que podemos introducir nuevos tipos de esquemas de firma pero también nuevos esquemas de sighash sin tener que agregar nuevos códigos de operación de CHECKSIG para cada uno que se agrega. La idea es que cosas como NOINPUT pueden luego incluirse sin costo como una nueva versión de clave pública.

Andreas: Entonces estas están esencialmente dentro de Tapscript, son mecanismos para poder hacer upgrades a futuro. Hay un gran número de ellos. Existen tres maneras diferentes en que puedes aplicar mejoras al script en el futuro. Si cambias la versión de Tapscript y la hoja, entonces modificas las semánticas de algo que actualmente es un OP_SUCCESS que clientes antiguos que no fueron actualizados verán como un script válido y este prefijo sighash de clave pública en Lightning no tendría que ser necesariamente una piedra en el camino de la implementación de estos tres BIPs: Taproot, Tapscript y Schnorr. Podemos continuar la conversación acerca de cómo implementarlos exactamente.

Pieter: En algún punto de esa discusión notamos que la discusión acerca de SIGHASH_NOINPUT estaba demorando nuestro progreso en otras cosas. Así que decidimos tener esta flexibilidad y publicar los BIPs sin ello. Pero por supuesto que eso no significa que si alguna de las propuestas para NOINPUT obtiene suficiente tracción y una implementación, no pueda ser activado al mismo tiempo que las otras. Como bien dijiste ya no existen piedras que interfieran en la conversación acerca de Taproot.

Andreas: Es muy salomónico. Qué gran manera de resolver un potencial problema de inanición (deadlock) y avanzar con funcionalidades que en estos momentos cuentan con mucho empuje en la comunidad de desarrolladores. Habiendo dicho eso, la discusión sobre SIGHASH_NOINPUT generó hoy alrededor de la mitad del contenido de mi bandeja de entrada. Se dio una discusión particularmente agitada al respecto. Muchas alternativas diferentes de obtenerlo de manera segura o si en realidad necesita hacerse de forma segura y se están discutiendo varios mecanismos, como las firmas de acompañante (chaperone signatures). Asumiendo que se el debate acalorado continúa, ¿cómo creés que estos BIPs podrían ser implementados? Los tres BIPs ignorando SIGHASH_NOINPUT y cualquier controversia en torno a ese tema.

Pieter: Por el momento espero recibir comentarios y revisiones por parte de la comunidad de desarrolladores, obtener una apreciación de cuánta aceptación tiene. Hasta el momento ha sido muy positivo, pero no puedo decir mucho sobre los pasos a seguir luego. En algún momento habrá una implementación de referencia. Vamos a esperar a tener una referencia acerca de si es suficientemente aceptable para la comunidad para luego incluirlo en Bitcoin Core y, potencialmente, otras implementaciones de nodos completos. Posteriormente se puede iniciar una conversación sobre el proceso de activación, y ahí veremos cómo continuar.

Andreas: Creo que es muy acertado no intentar hacer predicciones acerca de cuándo y cómo será activado. Una de las cosas que ha sido más sorprendente para muchos desarrolladores fue la controversia que se desató alrededor de SegWit cuando parecía que todo el mundo estaba de acuerdo y se terminó politizando mucho. Eso no es realmente relevante en esta discusión. En términos de la implementación de referencia como un mecanismo para proceder, yo pensaba que ya habías publicado una implementación de referencia en un fork de Bitcoin Core y afectaba alrededor de 500 líneas de código del protocolo de consenso.

Pieter: Sí, algo así. Quiero destacar que eso es más una demostración de propósito que otra cosa. Quiero mostrar lo poco que se afecta con este cambio. Antes de que el código se pueda incluir vamos a necesitar una versión mucho más revisada y preparada para producción, con más tests. También creo que habrá cambios menores y posiblemente también mayores que vamos a querer hacerle a la propuesta como resultado de la discusión pública. La versión lista para producción es algo que surge luego de todas esas discusiones.

Andreas: ¿Podrías alguien en esta etapa descargarse el fork, ejecutar una blockchain de prueba en su propia laptop y jugar hoy con todas estas funcionalidades?

Pieter: Es correcto. Debería agregar que esta implementación de referencia incluye sólamente las reglas de consenso y nada más, es decir que por ejemplo no hay ninguna integración con la billetera de Bitcoin Core, que todavía no tiene la capacidad de producir el nuevo tipo de transacciones.

Andreas: ¿Ni siquiera la infraestructura de RPC o alguna otra cosa? ¿Para invocar a los componentes de la biblioteca habría que escribir código?

Pieter: Sí. Estamos trabajando en un conjunto de cosas para hacer más fácil la integración de scripts más complejos en la billetera de Bitcoin Core y en la lógica de firmas, y posiblemente algún otro software, llamado miniscript. Pero cómo se terminarán integrando se verá más adelante. El punto es que para la inclusión en el protocolo no se necesita soporte de la billetera. Si estuviera presente sería una gran manera de mostrar las ventajas, pero no es necesario como primer paso. Y eso simplifica mucho la revisión que se necesita.

Andreas: Con las propuestas y los cambios a nivel de funcionalidades de protocolo como éstas y funcionalidades de la capa de consenso sucede que no pasan a ser parte de la experiencia del usuario o llegan a producción hasta que las billeteras los implementan también. Bitcoin Core y otras billeteras también. Estamos ahora a 18 meses de la llegada del soft fork de SegWit a la mainnet y la introducción de las direcciones bech32 y todavía hay billeteras que no han implementado el cambio. Es complicado para los equipos de mantenimiento de las billeteras mantenerse al día con los cambios e implementarlos al nivel de de la interfaz de usuario. ¿Cómo caracterizarías la implementación de Taproot, Tapscript, firmas Schnorr y estas funcionalidades con respecto al nivel de dificultad para los desarrolladores de billeteras de incorporar los cambios?

Pieter: Es una pregunta complicada porque depende mucho de lo que se quiere hacer con los cambios. Dada la flexibilidad y opciones en general que ofrecen Taproot, Tapscript y las firmas Schnorr es relativo. Si todo lo que buscas es cambiar las direcciones de recepción P2WPKH a algo basado en Taproot, el cambio es bastante trivial. Yo creo que el cambio en el algoritmo de hashing de las firmas es un tanto … por supuesto que necesitarás algo que pueda realizar firmas Schnorr en lugar de firmas ECDSA pero ya existen varias implementaciones para eso y cómo se calcula tu dirección va a cambiar un poco. Por otro lado si estás hablando acerca de integrar algo donde utilices el árbol Merkle con varias ramas, algunas usando las funcionalidades nuevas, si quieres usar Musig para combinar múltiples claves públicas en una, todas esas cosas llevan a más opciones. Sin dudas existe una complejidad de implementación allí pero estas funcionalidades no son necesarias para todos los que desean utilizarlo.

Andreas: Yo estoy pensando más en que si deseo esconderme en el bosque voy a querer que todos los demás planten un árbol también. No se trata realmente de que las personas utilicen una billetera llamativa, sino más bien que las personas que están utilizando P2PKH, P2WPKH, el pago a una clave pública, cambien también a Schnorr para que los scripts más complejos tengan un lugar uniforme donde esconder sus funcionalidades que mejoran la privacidad.

Pieter: Sí, pienso que es un cambio significativamente más chico que lo que fue SegWit porque no hay cambios en el protocolo peer-to-peer ni cambios a la estructura de las transacciones o de los bloques, pero sí se tiene el tema de Schnorr versus ECDSA.

Andreas: Continuando con el tema, con SegWit se dio un nuevo formato de dirección, bech32, la dirección nativa de SegWit que empieza con bc1. ¿Va a haber un nuevo formato de dirección o se va a incorporar todo en las direcciones bech32?

Pieter: Ya está incorporado porque BIP173, que define las direcciones bech32 para Bitcoin en realidad especifica un formato de dirección para cada salida SegWit, no solo para las v0. De forma tal que las salidas SegWit v1 ya se pueden codificar usando direcciones bech32. Puede haber algunos problemas de compatibilidad, como por ejemplo que el software de envío todavía solo permita salidas testigo bech32 v0. Si ese fuese el caso sería necesario un cambio muy sencillo para permitir v1 también.

Andreas: Entonces no habrá nuevos formatos de direcciones, y estoy seguro de que es un alivio para todos los que están intentando aprender todos los formatos.

Pieter: Sí. De hecho el cuarto caracter en una dirección BIP173 es siempre una “q” para v0, es bc1q, para v1 será bc1p.

Andreas: Muy bien, no me había percatado de eso.

Adam: Chicos, muchas gracias por hablar durante todo este tiempo con nosotros. Esta fue una conversación muy interesante y creo que termino entendiendo mucho más sobre estos problemas de lo que entendía antes, aunque todavía mi entendimiento es deficiente.

Stephanie: Yo también Adam. Creo que la información irá permeando en nosotros cuando escuchemos de nuevo el podcast. Dejando las bromas de lado, realmente les agradezco también. Siento que entiendo más también.

Adam: Hemos estado hablando de cosas que son muy reales y aunque por ahora no tenga un plan inmediato parece que están en camino hacia la integración y existe un consenso amplio, al menos en la comunidad de desarrolladores, sobre las partes menos controversiales. Retrocediendo un poco desde esta nueva versión de la tecnología, lo que realmente me gustaría escuchar de alguno de ustedes o de ambos es qué tecnologías o incluso ideas por las que están muy entusiasmados o que crean que serán muy importantes para el protocolo de Bitcoin en adelante pero que tal vez nosotros no hayamos escuchado todavía o que podríamos pensar que no es importante. ¿Existen tecnologías o ideas que los entusiasmen y que vendrían en los próximos años luego de lo que ya discutimos?

Jonas: Todo esto de Taproot es una idea muy nueva de manera que es muy difícil predecir lo que producirá en cuanto a ideas para los próximos cinco años porque las cosas cambian todo el tiempo. Ahora que este BIP ha sido propuesto, en realidad no ha sido propuesto formalmente todavía considerando el proceso oficial para los BIPs. Por ahora solo está en la lista de correos electrónicos. Pero el trabajo está lejos de terminar porque necesita ser pulido y tal vez haya que introducir algunas mejoras, mejoras menores, algunas mayores, como mencionó Pieter. Yo ahora me concentro en construir algunas de las bibliotecas que se usan en las implementaciones de billeteras o en Bitcoin Core. Por ejemplo, se va a necesitar una implementación para las firmas Schnorr, y eso ya lo tenemos. Ha recibido bastantes revisiones, pero después también queremos una implementación de Musig así que tenemos un PR (Pull Request) para eso también pero necesita más revisión. Más adelante también vamos a trabajar en las firmas con umbral (threshold signatures) por ejemplo. Ya que estas cosas son relativamente nuevas incluso para los desarrolladores de Bitcoin y requieren interacciones entre múltiples participantes del protocolo, queremos hacer estas bibliotecas fáciles de utilizar y seguras en primer lugar. Pienso que esto va a requerir mucho trabajo y es algo en lo que me estoy concentrando pero también estoy muy entusiasmado por ver todo esto hecho realidad, con suerte en algún momento en los próximos dos años o el año que viene. Ya veremos.

Pieter: Sí, creo que ese es un muy buen punto. Hay muchas opciones que se crean por cosas como Taproot y Schnorr que seguramente aún ni hemos considerado. Recientemente sucedió el [CHECKOUTPUTSHASHVERIFY](https://github.com/JeremyRubin/bips/blob/op-checkoutputshashverify/bip-coshv.mediawiki) que propuso Jeremy Rubin por ejemplo, que se torna mucho más sencillo por Taproot. Creo que veremos más ideas de cosas que la gente no ha pensado y que pueden ser construidas sobre estas herramientas ya sea como cambios menores en el mecanismo de consenso o cosas como canales de pago puramente del lado de las billeteras. Más allá de esto estoy muy entusiasmado por la agrupación de ingresos cruzados. Esto significa aquella idea de transformar potencialmente todas las firmas por transacción en una sola firma de manera que se tendría solo una firma por transacción, al menos cuando todos están cooperando en un proceso de coinjoin o algo similar. Este concepto ha demostrado interactuar con muchas partes del sistema, por lo que lo dejamos fuera de BIP-Taproot pero irónicamente esa funcionalidad fue lo que nos llevó a investigar las firmas Schnorr y todas las formas en las que interactúa en primer lugar así que espero que podamos volver a trabajar sobre eso en alguna etapa posterior. También cosas como Graftroot y G’Root que son mejoras y generalizaciones sobre Taproot. Si hablamos sobre cosas completamente no relacionadas con el scripting de Bitcoin, otras tecnologías por las que estoy entusiasmado, por ejemplo estuvimos trabajando durante un tiempo en un [mejor protocolo de distribución de transacciones](https://arxiv.org/abs/1905.10518), Gleb Naumenko, Greg Maxwell y yo. Escribimos una biblioteca minisketch para realizar una reconciliación entre conjuntos eficiente en lugar de notificar las mismas transacciones una y otra vez, y estoy muy ansioso por eso.

---
title: Bitcoin's Security Model - A Deep Dive
translation_by: Julien Urraca
tags: ['security']
date: 2016-11-13
speakers: ['Jameson Lopp']
---

Texto original: <https://www.coindesk.com/markets/2016/11/13/bitcoins-security-model-a-deep-dive/>

# El modelo de seguridad de Bitcoin: una profunda inmersión
#### CoinDesk echa un vistazo bajo el capó para entender qué funciones de seguridad ofrecen y qué no ofrecen bitcoin.

Cuando se discuten los mecanismos de consenso para diferentes criptomonedas, un tema que a menudo causa argumentos es la falta de comprensión (y definición) del modelo de seguridad que proporcionan para los datos históricos del libro mayor. Si bien cada modelo de consenso tiene como objetivo evitar varios ataques teóricos, es importante comprender los objetivos del modelo.

Cada modelo de seguridad tiene dos partes principales: suposiciones y garantías. Si las hipótesis utilizadas como entradas se mantienen verdaderas, entonces también deberían existir las garantías que emite el modelo.

Vamos a profundizar en el modelo de seguridad que parece ofrecerse a los usuarios de bitcoin que ejecutan un nodo completo.

## En busca de la verdad
> «Una de las fortalezas de bitcoin, la más importante en mi opinión incluso, es el bajo grado de confianza que necesitas en los demás». — Pieter Wuille

El objetivo de los libros contables distribuidos es proporcionar un historial ordenado de eventos, porque en los sistemas distribuidos no se puede confiar simplemente en una marca de tiempo.

Cuando un nuevo participante de una red basada en blockchain se une, descarga los bloques disponibles y considera cada serie válida de bloques que ve, a partir de un bloque de génesis codificado de forma rígida.

Una de las mayores suposiciones del modelo de seguridad de bitcoin es que la mayoría de los mineros son honestos: que están trabajando para proteger la blockchain en lugar de intentar socavarla. En la práctica, esto se ha mantenido cierto a lo largo de la historia de bitcoin debido a los incentivos mineros, aunque algunos se preguntan si seguirá siendo cierto en el futuro.

Teniendo en cuenta este supuesto, los operadores de nodos completos pueden estar completamente seguros de varios hechos:

- Nadie ha inflado la oferta monetaria excepto los mineros, y solo según un calendario bien definido.
- Nadie gastó dinero sin tener la (s) clave privada (s) apropiada (s).
- Nadie gastó el mismo dinero dos veces.

Los operadores de nodos completos pueden estar razonablemente seguros de otras cosas. Existe una sólida garantía de que:

- Cualquier bloque de la cadena se creó aproximadamente dos horas después de la marca de tiempo del bloque.
- Están sincronizando la «verdadera» historia de la blockchain.

A un nivel más técnico, esto requiere multitud de comprobaciones:

- Todos los bloques siguen las reglas de consenso:
- Cada bloque es encadenado a un bloque padre
- Cada bloque cumplió su objetivo de dificultad y cuenta con prueba de trabajo suficientes
- Las marcas de hora de bloques caen en una ventana en relación con los bloques recientes
- La raíz de Merkle coincide con las transacciones del bloque
- Ningún bloque era mayor que el tamaño máximo permitido
- La primera (y la única primera) transacción de cada bloque es una transacción coinbase
- Los resultados de Coinbase no pagan más que la recompensa en bloque adecuada
- Ningún bloque contenía más que las operaciones de firma permitidas

Todas las transacciones siguen las reglas de consenso:

- Los valores de entrada y salida son correctos
- Las transacciones solo gastan salidas no utilizadas
- Todas las entradas que se gastan tienen firmas válidas
- No se gastaron resultados de transacciones de coinbase dentro de los 100 bloques posteriores a su creación.
- Ninguna transacción gasta entradas con un tiempo de bloqueo antes del bloque en el que se confirman.

Muchas otras reglas que tardarían demasiado en cubrirse aquí.

## Seguridad termodinámica

Una vez confirmada una transacción en un bloque, no se puede revertir sin que alguien gaste una cantidad mínima de energía para reescribir la cadena.

Mientras ningún atacante tenga más del 50% de la potencia computacional de la red y los nodos honestos puedan comunicarse rápidamente, la probabilidad de que una transacción se revierta disminuye exponencialmente con el número de confirmaciones que ha recibido. Hay otros ataques, como la minería egoísta, que pueden reducir este requerimiento de energía, aunque parecen difíciles de perpetrar.

![thermodynamic](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/3TARMFYIURBUBAB4EFQTH6KLUY.png)
Fuente: «El modelo de seguridad de Bitcoin revisado» por Yonatan Sompolinsky1 y Aviv Zohar

Analizando el trabajo acumulado actual realizado por los mineros de bitcoin, se necesitarían casi 1026 hashes para construir una blockchain alternativa a partir de génesis con una mayor prueba acumulativa de trabajo que los nodos completos considerarían la cadena «verdadera».

Para reducir algunos números sobre el costo que implica un ataque de este tipo:

Un Antminer S9 funciona a 0,1 joules por GH (109 hashes)

1026 hashes * 0,1 J/109 hashes = 1015 joules

1015 joules = 2.777.777.778 kw horas * 0,10 USD kw/hora = 277.777.778 dólares en electricidad para reescribir toda la blockchain

Mientras que en el momento de redactar este informe, un solo bloque debe alcanzar un objetivo de dificultad de 253.618.246.641, lo que requeriría aproximadamente:

253.618.246.641 * 248/65535 = 1,09 * 1021 hashes

1,09 * 1021 hashes * 0,1 J/109 hashes = 1,09 * 1011 joules

1,09 * 1011 joules = 30.278 kw horas * 0,10 USD kw/hora = electricidad por valor de 3.028 dólares por bloque

Es por eso que podemos afirmar que el bitcoin es probablemente seguro termodinámicamente.

Hay algunas variables que puede modificar en el cálculo anterior para reducir el costo, pero podemos estar seguros de que requerirá electricidad por un valor de muchos millones de dólares solo para reescribir toda la blockchain. Sin embargo, un atacante con tanto poder hash podría, en el peor de los casos, revertir las transacciones hasta 2014; en breve profundizaremos en la razón de esto.

Tenga en cuenta también que esto no tiene en cuenta los costes necesarios para obtener y operar equipos mineros suficientes para llevar a cabo dicho ataque.

## Resistencia Sybil

Debido a que el protocolo bitcoin considera que la verdadera cadena es la que tiene la prueba de trabajo más acumulada (no es la cadena más larga, como suele decirse incorrectamente), el resultado es que un nuevo par que se une a la red solo necesita conectarse a un único par honesto para encontrar la verdadera cadena.

Esto también se conoce como «resistencia Sybil», lo que significa que alguien no puede lanzar un ataque contra un nodo creando muchos compañeros deshonestos que le dan información falsa.

![Nodos](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/PE42K6GDLVHM3EAWNFWKQTKMXU.png "nodos")

Aquí se muestra un escenario casi en el peor de los casos en el que su nodo está siendo atacado masivamente Sybil, pero aún tiene una única conexión con un nodo honesto que está conectado a la verdadera red bitcoin. Mientras un único par honesto pase los datos reales de la blockchain a su nodo completo, quedará bastante claro que cualquier atacante de Sybil está intentando engañarlo y su nodo los ignorará.

## Consenso en tiempo real

El protocolo bitcoin crea una serie de otros atributos interesantes con respecto al mantenimiento del consenso en toda la red una vez que su nodo se encuentra en la punta de la blockchain.

Los autores de «Perspectivas y desafíos de investigación para Bitcoin y criptomonedas» señalan las siguientes propiedades que son importantes para la estabilidad de una criptomoneda:

- Consenso eventual. En cualquier momento, todos los nodos conformes acuerdan un prefijo de lo que se convertirá en la eventual blockchain «verdadera».

- Convergencia exponencial. La probabilidad de una fork de profundidad n es O (2−n). Esto proporciona a los usuarios una gran confianza en que una regla simple de «k confirmaciones» garantizará que sus transacciones se liquiden de forma permanente.

- Vivacidad. Se seguirán añadiendo nuevos bloques y las transacciones válidas con tarifas apropiadas se incluirán en la blockchain en un plazo razonable de tiempo.

- Correctitud. Todos los bloques de la cadena con la prueba de trabajo más acumulada incluirán únicamente transacciones válidas.

- Imparcialidad. Un minero con un X% de la potencia computacional total de la red extraerá aproximadamente el X% de bloques.

Los autores del artículo señalan que el bitcoin parece tener estas propiedades, al menos bajo el supuesto de que la mayoría de los mineros siguen siendo honestos, que es lo que el bloque recompensa junto con la prueba de trabajo intenta incentivar.

Hay muchos otros algoritmos que se pueden utilizar para mantener el consenso en sistemas distribuidos, tales como:

- Prueba de participación
- Prueba de edad de la moneda
- Prueba de depósito
- Prueba de quemadura
- Prueba de actividad
- Prueba de tiempo transcurrido
- Consenso federado
- Tolerancia de falla bizantina

Estos crean diferentes modelos de seguridad: la diferencia más obvia con respecto a la prueba de trabajo es que cada uno de los sistemas alternativos consenso se impulsa a expensas de los recursos internos (monedas o reputación) en lugar de recursos externos (electricidad). Esto crea un conjunto muy diferente de incentivos para validadores (y confianza en) de la red, lo que cambia drásticamente el modelo de seguridad.

## Malentendidos del modelo de seguridad

Una suposición errónea común es que existe un modelo de seguridad bien definido para bitcoin.

En realidad, el protocolo bitcoin se estaba construyendo y se está construyendo sin una especificación o modelo de seguridad definidos formalmente. Lo mejor que podemos hacer es estudiar los incentivos y el comportamiento de los actores dentro del sistema para entenderlo e intentar describirlo mejor.

Dicho esto, hay algunas propiedades del protocolo bitcoin que a menudo se analizan incorrectamente.

Algunas blockchains han sufrido lo suficiente por los ataques que los desarrolladores agregan puntos de control firmados transmitidos centralmente al software del nodo, diciendo esencialmente que «el bloque X ha sido validado por los desarrolladores como en la cadena histórica correcta». Este es un punto de extrema centralización.

Vale la pena señalar que bitcoin tiene 13 puntos de control codificados, pero no cambian el modelo de seguridad como lo hacen los puestos de control emitidos. El último punto de control se agregó al Bitcoin Core 0.9.3 y se encuentra en el bloque 295000, que se creó el 9 de abril de 2014. Este bloque tenía una dificultad de 6.119.726.089, lo que requeriría aproximadamente:

6.119.726.089 * 248/65535 = 2,62 * 1019 hashes

2,62 * 1019 hashes * 0,1 J/109 hashes = 2,62 * 109 joules

2,62 * 109 joules = 728 kw horas * 0,10 USD kw/hora = 73 dólares de electricidad para generar

Por lo tanto, si un atacante de Sybil rodeaba por completo un nuevo nodo que se sincronizaba desde cero, podría crear algunas blockchains cortas a bajas alturas casi sin costo, pero solo hasta los distintos bloques marcados.

Si particionaba un nodo fuera de la red que se había sincronizado más allá del bloque 295.000, podría comenzar a alimentar bloques falsos a un costo de 73 USD por bloque, al menos hasta que se produzca un reajuste difícil. Sin embargo, cuanto más lejos se haya sincronizado el nodo de la víctima, mayor será el costo para el atacante crear una cadena con más trabajo acumulado.

Tanto Greg Maxwell como Pieter Wuille han afirmado que esperan eliminar por completo algún día los puestos de control. El mantenedor principal de Bitcoin Core, Wladimir van der Laan, señaló que los puestos de control son una fuente constante de confusión para las personas que buscan entender el modelo de seguridad de bitcoin.

Se podría argumentar que esto significa que un nodo completo está «confiando» en los desarrolladores Core con respecto a la validez del historial de blockchain hasta el 9 de abril de 2014, pero el nodo aún comprueba los hash de Merkle en el encabezado de cada bloque, lo que significa que la solidez del historial de transacciones sigue protegida por prueba de trabajo. Estos antiguos puntos de control permiten aumentar el rendimiento (omitir la verificación de firma) al sincronizar inicialmente la blockchain histórica, aunque la introducción de libsecp256k1 ha hecho que la diferencia de rendimiento sea menos significativa.

Los puntos de control permanecen en vigor para tres fines:

1) Para evitar que los nodos se llenen la memoria con encabezados de bloque válidos pero de baja prueba de trabajo
2) Omitir firmas en bloques anteriores (mejora del rendimiento)
3) Para estimar el progreso de la sincronización

Mientras se escribía este artículo, Greg Maxwell propuso reemplazar los puntos de control por una comprobación de trabajo acumulada en su lugar. Una vez que un nodo tiene una cadena que contiene más de 5,4 * 1024 hash ejecutados, se rechazarán las cadenas con menos trabajo acumulado. Esto coincide con la cantidad de trabajo realizada hasta aproximadamente 320.000 en septiembre de 2014, momento en el que los bloques individuales tuvieron una dificultad aproximada de 27,000.000.000.

![Difficulty](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/TZUAX54OIFHJ3J7D2JTOSVSXYY.png)

Los bloques mineros con una dificultad de 27.000.000.000 requerirían aproximadamente

27.000.000.000 * 248/65535 = 1,16 * 1020 hashes

1,16 * 1020 hashes * 0,1 J/109 hashes = 1,16 * 1010 joules

1,16 * 1010 joules = 3.222 kw horas * 0,10 USD kw/hora = electricidad por valor de 322 dólares por bloque

Así, con este cambio propuesto, si un atacante Sybil rodeaba por completo un nuevo nodo que se sincronizaba desde cero, podría comenzar a alimentar bloques falsos a partir de cualquier bloque tras génesis sin costo alguno. Si un atacante de Sybil rodeaba por completo un nodo que se sincronizó más allá del bloque ~ 320.000, podría comenzar a alimentar una cadena falsa desde ese punto a un costo de 322 USD por bloque.

En resumen, cualquiera de las comprobaciones para asegurar la sincronización inicial de un nodo es relativamente económico de atacar si una entidad puede obtener el control total de la conexión a Internet de su nodo; si no puede, el nodo descartará fácilmente los bloques del atacante.

En una nota relacionada, cada sistema blockchain tiene su bloque de génesis codificado en el software del nodo. Se podría argumentar que hay un contrato social para la «historia compartida» que es el libro mayor: una vez que un bloque tiene la edad suficiente, todos los miembros de la red comprenden que nunca se revertirá. Como tal, cuando los desarrolladores toman un bloque muy antiguo y crean un punto de control, se hace más como una comprobación de cordura acordada en lugar de como un dictado de la historia.

Además de los puntos de control, también está la cuestión de cómo se arranca un nodo a sí mismo. El proceso actual para los nodos bitcoin es comprobar si tiene una base de datos local de pares de la que ha aprendido anteriormente. Si no es así, consultará un conjunto de «semillas DNS» codificadas en el software. Estas semillas mantienen una lista de nodos bitcoin bien conectados que devuelven a su nodo.

Como podemos ver en el código, Bitcoin Core 0.13 utiliza actualmente DNS Seeds administrado por Pieter Wuille, Matt Corallo, Luke Dashjr, Christian Decker, Jeff Garzik y Jonas Schnelli. Cualquiera puede ejecutar una semilla de DNS utilizando el software sembrador de bitcoins de Pieter Wuille o el software de Matt Corallo, aunque para que los nuevos nodos lo utilicen, tendría que convencer a los desarrolladores de una de las implementaciones de nodos completas para que agregue su host inicial DNS a su software.

Puede parecer una vez más un punto de centralización extrema que el proceso de arranque de un nuevo nodo dependa de solo seis semillas DNS. Recuerda que el modelo de seguridad de bitcoin solo requiere que te conectes a un único par honesto para poder resistir los ataques de Sybil.

Por lo tanto, un nuevo nodo solo necesita poder conectarse a un único semilla DNS que no esté comprometido y devuelva las direcciones IP de los nodos honestos. Sin embargo, hay un respaldo si, por algún motivo, no se puede acceder a todas las semillas de DNS: una lista codificada de direcciones IP de nodos fiables que se actualiza para cada versión.

El modelo de seguridad para estos diversos parámetros de inicialización no es que el operador de nodo completo confía en las semillas de X DNS o en los desarrolladores de Y Core para que les proporcionen datos honestos, sino que al menos 1/ X DNS semillas no se ven comprometidas o los desarrolladores de 1/Y Core son honestos al revisar la validez de los pares codificados de forma rígida cambios.

## Nada está perfectamente seguro

A un nivel aún más profundo, cuando ejecuta un nodo completo, probablemente confíe en el hardware y el software que está ejecutando hasta cierto punto.

Existen métodos para verificar el software comprobando las firmas de su binario con las de van der Laan, pero es poco probable que muchas personas se molesten en pasar por este proceso. En cuanto al hardware confiable, es un problema difícil. Lo más cerca que probablemente llegarás a una solución de hardware segura es algo como ORWL, que garantiza «autodestruirse» si alguien intenta manipularla.

![Hardware ORWL](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/CK62BL75RRCT5NVO67M7C7GQHE.png)

Sin embargo, dado que las arquitecturas de hardware para CPU, RAM y otro hardware importante tienden a ser propietarias, nunca podrá estar 100% seguro de que no se ven comprometidos.

## Equilibrio de poder de Bitcoin

Las aguas se vuelven aún más turbias cuando se empieza a investigar la relación entre los diferentes participantes del sistema.

El propósito de ejecutar un nodo completo es proteger su soberanía financiera. Por lo general, esto significa que al instalar y ejecutar una versión específica del software, está suscribiendo un acuerdo de que cumplirá las reglas de ese software y que todos los demás que utilicen la red también deben cumplirlas.

Por lo tanto, si la gente quiere cambiar las reglas de forma que no sean compatibles con versiones anteriores, debe aceptar explícitamente el cambio de regla ejecutando una nueva versión del software. Por otro lado, los cambios de reglas compatibles con versiones anteriores se pueden implementar y hacer cumplir sin su consentimiento.

Una descripción muy simplificada de la dinámica de potencia en bitcoin:
[embed] https://twitter.com/lopp/status/786241843436544002[/embed]

Es importante tener en cuenta que el software de nodo completo no se actualiza automáticamente, y esto es por diseño. Las actualizaciones automáticas cambiarían enormemente el equilibrio de poder de los desarrolladores, lo que les permitiría forzar cambios de reglas en nodos y mineros sin su permiso.

Lamentablemente, si bien un cambio de reglas puede ser técnicamente compatible con versiones anteriores, hemos aprendido a lo largo de los años que las bifurcaciones flexibles suficientemente creativas pueden implementar cambios que están claramente fuera de la intención de la versión anterior de las reglas. Vitalik Buterin lo demostró con una descripción de una forma de soft fork el tiempo de bloqueo de bitcoin de 10 minutos a 2 minutos, lo que, por supuesto, también aceleraría el calendario de emisiones de nuevos bitcoins.

Hay una carta de triunfo que tienen los nodos completos para luchar contra las bifurcaciones blandas no deseadas es alejarse de los mineros que implementaron la soft fork. Esto es difícil de realizar (por diseño) y plantea muchas preguntas sobre la medición del consenso y la búsqueda de nodos de importancia económica.

Técnicamente, podría hacerse cambiando el algoritmo minero de doble SHA256 a una función hash diferente, haciendo que todos los ASIC SHA256 sean inútiles para minería de bitcoins. Por esta razón, los operadores de nodos deben permanecer atentos a los cambios en el ecosistema y recordar a los mineros que pueden ser reemplazados si superan su autoridad.

Mucha teoría de juegos está involucrada en discutir las operaciones mineras y su amenaza a la seguridad de bitcoin, y especulé sobre cómo puede cambiar el ecosistema minero en un artículo anterior. Si bien la minería de bitcoins está más centralizada de lo que la mayoría de nosotros nos gustaría, parece funcionar bien porque los mineros de bitcoin tienen mucho capital invertido; no pueden arriesgarse a destruir su inversión actuando maliciosamente en un sistema en el que todos están observando.

## Seguridad SPV

Muchos usuarios de bitcoin emplean un cliente ligero para acceder a la red en lugar de un nodo completo, ya que requiere muchos menos recursos y, al mismo tiempo, proporciona una seguridad sólida.

Un cliente que utiliza Verificación de pago simplificada (SPV) descarga una copia completa de los encabezados de todos los bloques de toda la cadena. Esto significa que los requisitos de descarga y almacenamiento se escalan linealmente con el tiempo transcurrido desde que se inventó el bitcoin. Esto se describe en la sección 8 del documento técnico de bitcoin.

![Proof-of-work-chain](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/DK3XSU4EENDZLHQP2CUQAIFNFE.png)

Satoshi escribió que un cliente SPV «no puede verificar la transacción por sí mismo, pero al vincularla a un lugar de la cadena, puede ver que un nodo de red la ha aceptado y los bloques añadidos después de confirmar que la red la ha aceptado». SPV asume que una transacción X bloquea en profundidad será costoso falsificar.

SPV parece ofrecer garantías similares a la seguridad de los nodos completos, pero con un supuesto adicional de que cualquier bloque con un encabezado válido y una prueba de trabajo siempre contiene transacciones válidas. Dado que los clientes SPV no comprueban todas las reglas de consenso indicadas en la primera sección de este artículo, suponen que los nodos desde los que solicitan transacciones están comprobando las reglas de consenso.

Una diferencia de seguridad adicional y menor implica que los compañeros le oculten información. Cuando ejecuta un nodo completo, los pares pueden retener transacciones y bloqueos no confirmados. Sin embargo, una vez que recibas un bloque de cualquier par, nadie puede retener las transacciones en ese bloque. Por otro lado, es posible que un par dé un encabezado de bloque a un cliente SPV y luego retenga información sobre las transacciones en ese bloque.

Los clientes de SPV pueden realizar una consulta para obtener información sobre las transacciones que afectan a una determinada dirección y, si bien sería costoso que los compañeros les mintieran sobre la existencia de transacciones confirmadas falsas (requeriría extraer un bloque con suficiente POW), podrían mentir por omisión afirmando que no hubo resultados. para el filtro de floración que utilizó para consultar transacciones. También vale la pena señalar que el SPV está terriblemente roto desde el punto de vista de la privacidad debido a defectos con los filtros de floración.

BitcoinJ tiene una excelente redacción del modelo de seguridad SPV. En cuanto a las transacciones no confirmadas, señalan:
«En el modo SPV, la única razón por la que tienes que creer que la transacción es válida es el hecho de que los nodos a los que te conectaste retransmitieron la transacción. Si un atacante pudiera asegurarse de que estabas conectado a sus nodos, esto significaría que podría enviarte una transacción completamente inválida (dinero inexistente gastado) y que aún se aceptaría como si fuera válida».

La seguridad SPV probablemente sea «lo suficientemente buena» para el usuario promedio, aunque podría mejorarse con las pruebas de fraude SPV. Se ha discutido un poco este concepto pero no se han implementado propuestas para incorporarlo al protocolo.

## No hay lugar como 127.0.0.1

Si no está ejecutando un nodo completo (y lo usa para validar transacciones), externalizará al menos cierto nivel de confianza a terceros, lo que da como resultado un modelo de seguridad diferente para el uso de bitcoin. Tenga en cuenta que esto no hace falta que todos los usuarios y empresas creen su software directamente sobre la API RPC de Bitcoin Core.

Algunas configuraciones de infraestructura alternativas pueden incluir, pero no se limitan a:

1) Utilizar una cartera móvil como Bitcoin Wallet para Android, GreenAddress o Stash que le permite configurar la billetera para que solo consulte su propio nodo completo.

![btc-security-graphic](https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/MRJOS27KXNEVLHTOGQJIGPT43M.png)

2) Crear aplicaciones sobre bibliotecas de nodos SPV como BitcoinJ y configurarlas para que solo se conecten a los nodos completos que opera. En BitcoinJ, esto se puede lograr definiendo sus propios SeedPeers que pasa a su PeerGroup durante la inicialización. Con libbitcoin puedes definir una conexión de red a un nodo específico utilizando este ejemplo.

3) Crear un servidor proxy compatible con la API JSON-RPC de Bitcoin Core que envía algunas llamadas a servicios de terceros, pero también verifica automáticamente los datos que devuelven haciendo llamadas a un nodo completo local. Para ver un ejemplo, consulte el software BitGod de BitGo. Este modelo híbrido puede ofrecerle lo mejor de ambos mundos: puede aprovechar las funciones avanzadas que ofrecen terceros sin dejar de conservar su soberanía financiera.

## Nodos completos para la libertad

Está claro que ejecutar su propio nodo completo ofrece una seguridad superior con el menor número de suposiciones requeridas. Dado que puede construir una computadora capaz de ejecutar un nodo completo confiable por solo unos pocos cientos de dólares, haga los cálculos y determine si garantizar su soberanía financiera vale la pena.

Gracias a Kristov Atlas, Eric Martindale, Andrew Miller y Kiara Robles por revisar y proporcionar comentarios sobre este artículo.

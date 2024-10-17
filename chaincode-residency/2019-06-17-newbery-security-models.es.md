---
title: Security Models
transcript_by: Caralie Chrisco
translation_by: Julien Urraca
speakers:
  - John Newbery
tags:
  - security
  - taproot
  - cryptography
date: 2019-06-17
media: https://youtu.be/6gGcS4N5Rg4
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-17-newbery-security-models.es/
---
Texto original: <https://btctranscripts.com/chaincode-labs/chaincode-residency/2019-06-17-john-newbery-security-models/>

Transcripción de: Caralie Chrisco

Ubicación: Residencia de Chaincode Labs 2019

Diapositivas: https://residency.chaincode.com/presentations/bitcoin/security_models.pdf

John Newbery: Muy bien, modelos de seguridad. Esto va a ser como un recorrido rápido de varias cosas, vista de muy alto nivel. Empezaré dándote algún tipo de marco para pensar en las cosas. Así que en criptografía, a menudo hablamos de pruebas de seguridad en términos de esquemas existentes, hablamos de suposiciones.

Así que, por ejemplo... Si puedes romper el nuevo esquema B, entonces también podrás romper el antiguo esquema A. Así es como hacemos pruebas de seguridad. Así, por ejemplo, bajo el modelo de oráculo aleatorio, así que si tenemos una función hash que modelamos como aleatoria. Si puede romper la raíz, puede romper el problema de registro discreto sobre la curva eclíptica en general.

El contrapositivo es cierto que si el antiguo esquema A es seguro, el nuevo esquema B es seguro. Si puede romper el nuevo esquema B, puede romper el antiguo esquema A. Entonces, ¿por qué creemos que el problema de registro discreto es difícil sobre las curvas elípticas?

Elichai: Porque exponenciar es muy fácil pero hacer logaritmos es muy difícil. No conocemos ningún algoritmo que pueda hacer logaritmos de manera eficiente, así que en el segundo que tengas grandes números, estás atascado.

John: Sí, porque aún no lo hemos roto. Es un marco interesante para pensar en estas cosas cuando hablas de modelos de seguridad, tienes que preguntar, ¿en comparación con qué? Así que eso es lo que podemos empezar. Vamos a empezar con el estándar oro, que es el nodo completo, y hablaremos de otros esquemas, y diremos ¿cómo se compara esto con un nodo completo?

Muchas de estas cosas se refieren a reducir el costo de poder interactuar con la red Bitcoin. Todos lo están. Ejecutar un nodo completo es costoso en términos de ancho de banda y memoria informática. Entonces, ¿cómo podemos permitir que las personas interactúen con la red mientras se permite mantener un nivel de seguridad aceptable? Habrá compensaciones aquí, y de eso vamos a hablar.

Así que los nodos llenos y podados son donde vamos a empezar. Vamos a hablar de clientes ligeros, por supuesto, SPV. Vamos a tocar puntos de control, asumiválidos, asumeutxo, de lo que supongo que todos habéis oído hablar. Luego vamos a hablar de algunas propuestas alternativas de conjunto UTXO. Luego, un poco más de lectura.

## Nodos completos

Entonces, ¿qué hace un nodo completo? También es una pregunta. ¿Qué hace un nodo completo?

Varios miembros de la audiencia: validar, transmitir y almacenar transacciones para toda la blockchain.

John: Así que descarga todos los encabezados y bloques, valida y transmite transacciones en esos bloques de la cadena de mayor trabajo. Pueden validar y transmitir transacciones no confirmadas. ¿Qué opinas de eso? Si tengo un nodo completo que no valida transacciones no confirmadas, ¿es un nodo completo?

Miembro del público: Desde la perspectiva de la persona que quiere verificar la transacción, supongo que lo sería.

Miembro del público: Si una transacción no está confirmada, no está confirmada, ¿verdad? Si solo te importaban las transacciones confirmadas y has descargado todos los bloques, es posible que no tengas que retransmitir o validar sin confirmar.

John: Sí, creo que es útil pensar en la red de retransmisión de transacciones por separado de la red de propagación de bloques. Llamaría a un nodo completo algo que está en la red de propagación y está validando la blockchain, y luego, además de eso, también puede tener un mempool con transacciones de retransmisión. Se trata de dos funciones distintas y dos redes separadas. Resulta que comparten el mismo modo de transporte ahora mismo. Pero eso no es necesario. ¿Lucianna?

Lucianna: Desde el punto de vista de la seguridad, los nodos completos simplemente son transacciones válidas. ¿Los nodos completos solo le enviarían transacciones válidas? (inaudible...)

John: Puede ejecutar un nodo completo que no retransmita transacciones no confirmadas, utilice solo bloques como opción y no tenga un mempool básicamente, sí, pero no lo rellenará de sus pares y no lo transmitirá.

Miembro del público: Así que no hay garantía de validez, ¿verdad?

John: Bien.

Miembro del público: Alguien podría estar ejecutando un nodo diferente. No hay garantía de que haya consenso, dado el mismo conjunto de reglas, haya una eventual coherencia, pero no hay garantía de que en un momento dado me haya puesto al día.

John: Solo estoy hablando de la diferencia entre retransmitir transacciones no confirmadas y sincronizar la blockchain. Tienes razón en que no hay garantía de eso: tenemos, como una suposición de que estás conectado a al menos un par honesto, y si lo estás, te sincronizarás con la blockchain que más funciona.

## Nodos podados

Vale, así que nodos podados. ¿Qué hace un nodo podado?

Antoine: Los bloques están validados y solo tienes que mantener el rango del último bloque cerca de la punta.

Miembro del público: Para ahorrar espacio.

John: Sí, descarga y valida todos los bloques y encabezados y descarta todos los archivos de bloque que superen un determinado límite de almacenamiento. ¿Sigue siendo un nodo completo?

Antoine: Sí.

John: ¿Lucianna?

Lucianna: Pregunta, también la respuesta sería no si la reorganización es mayor que cuánto han almacenado. ¿Mantienen los encabezados o simplemente descartan los cuerpos o descartan los datos completos?

John: Descarta los datos completos, el bloque serializado completo. Mantienes la blockchain segura, que es tu visión de la cadena de mayor trabajo. Descarta todos los datos serializados.

Miembro del público: También conservas todos los archivos de deshacer. Así que puedes deshacer un bloque de manera eficiente.

John: Deshazte de todos los archivos de bloque completo y todos los archivos de deshacer por un límite determinado. Así que Lucianna planteó un punto interesante, si hay una reorganización demasiado profunda, entonces no se puede reorganizar de nuevo a la cadena más trabajadora. Esta es una diferencia en las hipótesis de seguridad. Pero el valor predeterminado aquí es... 550 megabytes. Así que la idea es que tengas al menos cierta cantidad de reorganización a la que puedes volver.

Miembro del público: ¿Qué hará el nodo completo podado si hay una reorganización profunda?

John: Creo que se detendrá.

Miembro del público: ¿Dejar de trabajar?

John: Sí.

Miembro del público: ¿No pedirá bloques a otros?

John: No. No hay ningún mecanismo para conseguir bloques viejos y reorganizar eso. Necesitas los datos de deshacer. Necesita conocer las transacciones que se gastaron en el bloque y no puede obtenerlas a través de la red peer-to-peer.

Miembro del público: ¿Así que 550 megabytes dijiste?

John: Así es.

Miembro del público: Eso es lo que, como 200, 300 bloques, 400, ¿verdad?

Charla cruzada del público...

John: Sí, necesitas, creo que es un día, un día o dos bloques más datos de deshacer porque los datos de deshacer tienen aproximadamente el mismo tamaño, de nuevo un bloque es de 1,5 megabytes.

Miembro del público: Es un límite más bajo.

John: Sí, debería haber buscado cuál es el valor predeterminado, creo que es 550.

Miembro del público: El mínimo es de 550.

Charla cruzada del público...

Miembro del público: Nunca hemos tenido la oportunidad de probar si este número es el correcto.

John: Hay una prueba funcional que...

Miembro del público: Me refiero a un escenario real.

John: Bien, así que la suposición aquí es que no vas a reorganizar más de un día o una semana o lo que sea.

Miembro del público: Es una gran suposición.

John: ¿Es una suposición justa? ¿Qué te parece?

Miembro de la audiencia: Si tienes que reorganizar tanto, creo que bitcoin está roto.

Miembro del público: ¿No 500 megabytes, sino uno o dos días?

Miembro del público: Hubo una reorganización de día completo en testnet.

John: Bien, eso es una red de prueba.

Miembro de la audiencia: Pero lo que estoy diciendo - La razón por la que hubo debido al error de la inflación. También podría haber ocurrido en la red principal si los mineros no hubieran actualizado a tiempo. No creo que esté tan lejos de la realidad.

[ruido de grupo]

Antoine: ¿Cuánto duró la reorganización?

Miembro del público: 24 cuadras.

John: Sí, algo así.

Jon: Me estoy asegurando de entenderlo. En la prueba de poda funcional, hay un valor mágico de 550, y está en toda la prueba. Reescribí la prueba, pero luego pensé que era demasiado trivial para enviar una solicitud de extracción. Pero siempre me he preguntado, ¿por qué 550? ¿Así que esa es la explicación?

John: La explicación es cierta cantidad de profundidad a la que desea poder reorganizar más un poco de búfer, y eso es lo que se eligió.

Miembro del público: Suponiendo que el futuro es incognoscible, ¿verdad? Podemos especular sobre las profundidades de la reorganización, pero cada vez que cambiamos los bloques de nodos...

John: ¿Bloques de nodos?

Miembro del público: ¿Cómo los llamas?

John: ¿Puntos de control?

Miembro del público: Así que tenemos puntos de control y no lo validamos hasta que se bloqueen los nodos.

John: Vamos a hablar de eso. Eso supone que es válido.

Miembro del público: Lo siento, pero eso implica en cierto sentido...

John: Hablaremos de cuáles son los supuestos en torno a los puestos de control. La suposición adicional aquí es que no tenemos una reorganización profunda, y podríamos debatir si es una buena suposición que podemos hacer sobre Bitcoin y qué otras cosas se romperían si tuviéramos una reorganización profunda.

Miembro de la audiencia: Pregunta: ¿Puede saber que un par es un nodo completo frente a un nodo podado si actúa igual que un nodo completo?

John: Sí, hay un poco de servicio.

Miembro del público: ¿La red de nodos?

John: Sí, la red de nodos que podría servirle bloques antiguos, los nodos de poda no lo harán.

Miembro del público: Pero puedes mentir sobre ello.

John: Puedes mentir sobre ello, y luego tus compañeros te pedirán todos los bloques, y no los tienes.

Miembro del público: O puedes mentir sobre ser un nodo podado, pero en realidad tienes todos los nodos de bloque.

John: No lo llamaría mentira. Solo dice: «No te voy a dar esos datos».

Miembro de la audiencia: ¿Los nodos podados pueden transmitir nuevos bloques?

John: Sí. Y hay una propuesta para permitir que un nodo podado sirva bloques hasta cierto nivel de profundidad. Jonas Schnelli tiene parte de eso fusionado con Bitcoin Core, pero no está completamente fusionado.

## Nodos SPV

Muy bien, nodos SPV. El término SPV se introdujo en este documento, que es el libro blanco de Bitcoin, y Satoshi dijo: «Es posible verificar los pagos sin ejecutar un nodo de red completo. Un usuario solo necesita guardar una copia de los encabezados de bloque de la cadena de prueba de trabajo más larga, que puede obtener consultando nodos de red hasta que esté convencido de que tiene la cadena más larga, y obtener la rama Merkle que vincula la transacción con el bloque en el que está marcado la hora. No puede comprobar la transacción por sí mismo, pero al vincularla a un lugar de la cadena, puede ver que un nodo de red lo ha aceptado y los bloques añadidos después de confirmar que la red la ha aceptado.

Por lo tanto, la verificación es fiable siempre que los nodos honestos controlen la red, pero es más vulnerable si un atacante supera la red. Si bien los nodos de red pueden verificar las transacciones por sí mismos, las transacciones fabricadas por un atacante pueden engañar al método simplificado mientras el atacante pueda seguir dominando la red. Una estrategia para protegerse contra esto sería aceptar alertas de nodos de red cuando detectan un bloque no válido, lo que pide al software del usuario que descargue el bloque completo y alerten a las transacciones para confirmar la incoherencia. Es probable que las empresas que reciban pagos frecuentes sigan queriendo ejecutar sus propios nodos para una seguridad más independiente y una verificación más rápida».

¿Alguna respuesta o reacción a eso?

Miembro del público: ¿Cuándo prueba de fraude?

[Risa]

John: Cuando prueba de fraude. ¿Qué es a prueba de fraude? ¿Alguien?

Miembro de la audiencia: Verificando un bloque, supongo, sin tener que comprobar la cadena desde el primer bloque. Alguien podría demostrártelo sin que pases toda la cadena. Eso sería válido a prueba de fraude.

John: Si alguien pudiera presentar una prueba breve y fácil de verificar, de que un bloque no es válido sin tener que validar todo el bloque.

Miembro de la audiencia: El desafío de las pruebas de fraude es que el envío no tiene costo alguno, por lo que se puede utilizar como vector de ataque. Podrías enviar spam a toda la red con: «Oye, esto no es válido, no es válido, no es válido».

John: Esta idea de tener alertas de nodos de red, no hay protección DoS contra eso. Esto ni siquiera habla de pruebas de fraude. Esto es decir, si alguien pretende enviarte un bloque válido, otra persona puede decir que el bloque no es válido y luego lo descargas y lo validas. En realidad no funciona.

Miembro del público: Pregunta - ¿Qué forma de decir que un bloque no es válido, que no podemos decir ya? Si sabemos que se crearon bitcoin adicionales aparte de las transacciones de coinbase, podemos decir que el bloque ya no es válido con solo mirar el bloque.

John: Tienes que validar todo el bloque. La idea con la prueba de fraude sería una prueba compacta en la que no necesitarías validar todo el bloque, pero aún así podrías saber que no es válido.

Miembro del público: Dices validar todo el bloque, porque si te muestro un bloque con cierta altura en el futuro, y digo: «oh mira, esto es 50 bitcoin». Podría ser que hubiera 50 bitcoin de comisiones en todas las transacciones. Para verificarlo, tienes que descargar todos los bloques y toda la cadena porque no tienes los valores de entrada. Ahora, con SegWit, puede verificar que los valores de entrada no se están mintiendo porque los valores de entrada están firmados. Pero antes, no había forma de verificar que no reclamabas más tarifas de las que deberías tener.

John: Aún necesitas esos datos antiguos si estás validando, ¿verdad?

...

John: Bien, ¿qué puede hacer un nodo SPV? ¿Carla?

Carla: Pueden recoger cuando recibes transacciones, pueden transmitir transacciones...

John: Sí, para que puedan verificar que la transacción ha sido confirmada por una cierta cantidad de trabajo. Es de suponer que están sincronizando la cadena de encabezados, por lo que saben cuál es la cadena de trabajo más acumulada. Así que saben que hay trabajo allí, no saben que es válido o tiene bloques válidos.

Miembro del público: Pregunta: ¿Saben que es un trabajo valioso?

John: Saben que es un trabajo válido. No puedes fingir trabajo. Si está sincronizando los encabezados, conoce las marcas de tiempo y los bits finales, por lo que sabe cuánto trabajo debe incluir un encabezado mirando el hash.

Miembro del público: No pueden verificar si la oferta monetaria se ha inflado. Podría haber un bloque en el pasado que se ha inflado, pero no lo sabrían.

John: Correcto. Entonces, ¿qué pueden hacer? Así que cuando la cadena de transacciones del bloque sea válida. Así que cuando digo cadena de transacciones, me refiero a la transacción o a su antepasado, volviendo a la coinbase de monedas donde se acuñaron esas monedas, a menos que tengas una prueba de Merkle por cada paso.

## A prueba de fraude

Hablábamos de pruebas de fraude. En general, son bastante difíciles. Esta es una publicación de Luke en la lista de correo. El caso generalizado de pruebas de fraude es probablemente imposible, pero tuvo una implementación de un esquema a prueba de fraude que mostraba que el bloque no supera cierto tamaño. Esto ocurrió durante el doble período de tiempo. A la gente le preocupaba que una cadena 2x engañara a los clientes SPV. Esta sería una forma de decirle a un cliente SPV que este encabezado que tienes se está comprometiendo a un bloque que es mayor que un tamaño determinado. Y no necesitas descargar todo el bloque. Es un ejemplo estrecho de prueba de fraude.

Miembro del público: ¿Le protege esta solución contra el vector de ataque DoS?

John: ¿Que la gente puede enviarte pruebas falsas de fraude? Puedes prohibirlos o simplemente desconectarlos.

Miembro de la audiencia: El punto es que no tienes que revisar el bloque si la prueba es una prueba real.

Miembro del público: Supongo que me cuesta entender que el costo de la validación es qué? IBD es un gran fragmento, el ancho de banda es un fragmento grande, subvierte un nodo SPV, podría suponer un cierto conjunto utxo y luego, a partir de ahí, ¿solo porque un solo bloque no es costoso de validar?

John: Bueno, los costos continuos pueden ser bastante altos en términos de ancho de banda si intentas ejecutar un nodo completo en una red limitada, como una red móvil.

Miembro del público: Me parece que el gran costo sería la EII y el ancho de banda, y esto está atacando una parte que no lo es.

John: Estoy de acuerdo, supongo que esto fue implementado por Luke, y por lo que sé, no se incorporó a muchos proyectos, pero lo he incluido como ejemplo de una prueba de fraude ilimitada.

Miembro de la audiencia: ¿Podemos retroceder un poco y hablar sobre la protección DoS y tal vez, en este tipo de escenario, parecería tener compañeros salientes en los que confías, sobre los que tienes control, con los que no te preocuparía tanto la protección de DOS? En términos de, si ese es el gran bloqueador de las pruebas de fraude, ¿por qué no recurrimos al tipo de relaciones en las que confiamos con nuestros nodos?

John: Bueno, el gran bloqueador de las pruebas tontas es que no existen. No tenemos una forma compacta de decir que este bloque no es válido según estas reglas de consenso. Puedes imaginar algún tipo de sistema SNARK o ZK donde puedas. No sé qué aspecto tendría eso. No soy experto en criptografía.

Miembro del público: ¿Son diferentes de los acumuladores y pertenecen a un conjunto y cosas así? ¿No están relacionados?

John: No están emparentados, no creo. Lo que quieres es una prueba en la que alguien pueda presentarte un pequeño fragmento de datos, y esos datos prueban que ha validado el bloque de acuerdo con las reglas que quieres validar según el bloque. Y puedes mirar esa prueba y no tener que validarla en sí y saber que ha sido validada. Este es un ejemplo muy estrecho de ello. Tal vez no quieras que los bloques sean superiores a un megabyte, y puedes obtener una prueba que demuestre que no son más de un megabyte. No te dice que no se está produciendo un nuevo bitcoin o que se haya roto alguna otra regla de consenso. Para ese caso generalizado, probablemente sea imposible, y no lo sabemos.

Miembro del público: Tengo mucha curiosidad por cómo implementamos esto porque incluso para pruebas de fraude válidas, hacemos sonar la alarma cuando algo va mal, pero la pregunta es, ¿cuánto tiempo hacemos sonar esta alarma? Puedes seguir sonando esa alarma durante una semana. Nadie me dice que pare, así que sigo haciendo sonar esta alarma. Así que también podría ser un ataque de DOS, ¿verdad? Una prueba de fraude le avisa sobre un evento o una instantánea en la red. Pero, ¿cómo sigues transmitiendo esta prueba de fraude?

John: La diferencia entre una prueba de fraude y lo que decía el libro blanco es que el documento técnico decía que sus compañeros podrían alertarlo sin dar una prueba. Así que solo dicen que este bloque es malo, y lo descargas y lo compruebas tú mismo. Es caro para ti hacerlo.

Miembro del público: Mi pregunta es, ¿cuánto tiempo hace eso? Cuidado con este bloque, no es válido.

John: No lo sé, tal vez siempre y cuando tenga más trabajo en ello.

Miembro del público: Puedo echarle un vistazo a eso.

John: Por lo tanto, los nodos SPV no pueden determinar si un bloque es válido, no pueden aplicar reglas de consenso. En general, la mayoría de nosotros usamos las mismas reglas de consenso que aprendimos en Bitcoin. En algunas circunstancias, puede que le importe que sus reglas de consenso sean reglas específicas de consenso. Un ejemplo de ello es la fork 2x, donde los autores de los componentes de la fork 2x la anunciaron como una característica, pero cambiar el tamaño del bloque no afecta a los clientes ligeros. Así que si pensaras que SegWit 2x no era bitcoin, verías esto como un ataque al cliente SPV porque estás enviando algo que no es un bloque de bitcoin, pero lo perciben como un bloque de bitcoin. ¿Tiene sentido eso? Los clientes SPV no aplican reglas de consenso.

De nuevo, los clientes de SPV no pueden garantizar que se aplique su política monetaria preferida. Es una regla de consenso. Así que todos podríamos creer que 21 millones de bitcoins es el número total de bitcoin. Si ejecuta un nodo SPV, no lo está aplicando en ningún lado. Esto es especialmente importante si piensa en una red en la que todos los usuarios ejecutan un nodo SPV. Si resulta demasiado costoso ejecutar un nodo totalmente validado y solo los mineros ejecutan nodos totalmente validadores, ahora confiamos a los mineros la política monetaria.

Miembro del público: ¿Tenemos algún tipo de idea de la proporción?

John: No lo sé

Miembro del público: Algún orden general de proporciones.

Miembro del público: Para aquellos que aceptan conexiones entrantes, es como el 95 por ciento.

Miembro de la audiencia: 95 por ciento?

Miembro del público: No poda.

Miembro de la audiencia: Tiene sentido si tienes conexiones entrantes, es mejor que quieras servirles toda la blockchain. No lo sé. No tengo estadísticas para los nodos salientes.

Miembro del público: No he pensado demasiado en esto, pero ¿cuál es el incentivo económico para dirigir un nodo público? Como entrante, ¿por qué me importa?

Miembro del público: Quieres difundir el evangelio, ¿verdad?

[Risa]

Miembro del público: Proteja la red.

Miembro del público: ¿Existe alguna regla para eso? Si solo acepta bloques, pero nunca transmite a otros, ¿está fuera de la red? Sería una especie de incentivo.

Miembro del público: Una vez que estoy conectado, la conexión sigue siendo la misma. ¿Por qué necesito abrir puertos? ¿Por qué me importa?

Miembro del público: ¡Quieres que la red funcione porque tienes bitcoins!

Miembro del público: Pero, de nuevo, ¿si quiero optimizar solo para mí?

Miembro del público: Hay algunas cosas que tienen sentido a nivel individual.

Miembro del público: Es como votar, ¿por qué votas?

Miembro del público: Sí. Es teoría de juegos. Eso es equilibrio nash, el dilema de la prisión. Es lo mismo. Lo que es bueno para ti será malo para ti si todos hacen lo mismo. Es un gran problema en la teoría de juegos. No sé dónde está el equilibrio nash en la red peer-to-peer. Hay un equilibrio en alguna parte.

Miembro del público: Existe un argumento sobre si ni siquiera deberías ejecutar un nodo completo si lo usas como nodo económico.

Miembro del público: Me gusta aceptar pagos.

Miembro del público: Pero, de nuevo, no necesito aceptar entrantes. Puedo encender mi nodo, validar mi transacción y desaparecer, si soy realmente egoísta.

Miembro del público: ¿Qué pierdes al aceptar entrantes?

Miembro del público: Costo.

Miembro del público: ¿Ancho de banda?

Miembro del público: No solo ancho de banda, sino costo.

Miembro del público: No estoy de acuerdo. Aún quieres que bitcoin funcione porque eres dueño de bitcoins. ¿Qué es lo egoísta? No creo que sea tan sencillo.

John: Hablaremos de esto un poco más tarde. Creo que Lucianna tiene un último punto.

Lucianna: Iba a decir que si te conectas, revisas la transacción y te vas, no sabes realmente lo que pasa cuando no estás en línea. Hay un motivo egoísta en la red de la red en el que tienes interés cuando te vas.

Miembro del público: Punto justo.

Miembro del público: ¿Qué era esa estadística? ¿Porcentaje de entrada?

Miembro del público: No lo sé, pero 10.500 aceptan conexiones entrantes.

Miembro del público: ¿En bitnodes?

Miembro del público: En bitnodes.

John: Vamos a seguir adelante, hemos tenido media hora, y no estoy muy lejos en mis diapositivas. Los nodos SPV tampoco pueden proporcionarle el mismo tipo de privacidad. Hay cosas que podemos hacer para mejorar la privacidad de los clientes ligeros, pero de nuevo, el estándar oro está ejecutando un nodo completo. ¿Queremos hablar de eso? ¿Alguna idea?

Miembro del público: Esto está agrupado con los filtros de floración, ¿verdad?

John: Sea cual sea su estrategia para descargar las transacciones que le interesan, incluso si está descargando un subconjunto de datos, está filtrando algo. No puede ser la información, teóricamente, perfectamente privada a menos que esté validando la blockchain completa.

John: Y de nuevo, los nodos SPV no pueden detectar falsos negativos. Un par que te está sirviendo, si eres un cliente ligero, puede mentir por omisión; simplemente no puede darte datos.

Vale, ¿qué pasa con la visión de Satoshi?

[Risa]

Miembro del público: Rápidamente en ese último punto, así que el hecho de que no puedas detectar un falso negativo, eso tiene consecuencias para la red Lightning, ¿verdad?

John: Sí. Con filtros bloom, sí. Con BIP 157/158, un modelo ligeramente diferente, porque estás descargando todos tus filtros...

No mencioné la estimación de tarifas. La forma en que funciona la estimación de tarifas en Bitcoin Core es que miramos el mempool. Felix va a hablar más sobre la estimación de tarifas esta tarde. Pero si no tienes un mempool, si no estás utilizando transacciones no confirmadas, no tienes forma de estimar las tarifas. Puedes mirar bloques, pero eso no es un salvavidas.

Miembro del público: ¿Cómo hacen las billeteras SPV la estimación de tarifas?

Miembro del público: ¿API públicas?

Miembro del público: Alguien ejecuta el servidor y te lo dice.

Miembro del público: La mayoría de las billeteras Android, la estimación de tarifas es tan mala.

Miembro del público: Al igual que Samouri Wallet, esa es una de las características de su servidor. Están cumpliendo sus propias estimaciones de honorarios.

...

John: Vamos a pausar este hasta esta tarde. Hablemos de las estimaciones esta tarde.

Así que esto es un poco de lengua en mejilla. Algunas personas hablan de que todos los nodos son nodos SPV. ¿De qué sirve ejecutar nodos completos? Satoshi y el libro blanco dijeron: «Si la red se vuelve muy grande, como más de 100.000 nodos, esto es lo que usaremos para permitir que los usuarios comunes realicen transacciones sin ser nodos completos. En ese momento, la mayoría de los usuarios deberían empezar a ejecutar software exclusivo para clientes, y solo las granjas de servidores especializadas siguen ejecutando nodos de red completos, algo así como cómo se ha consolidado la red de uso».

Esto ocurrió en 2010, pero también en el libro blanco se afirma que «las empresas que reciben pagos frecuentes probablemente querrán ejecutar sus propios nodos para una seguridad más independiente y una verificación más rápida».

Así que esta conversación se ha mantenido durante diez años, pero el libro blanco, incluso en 2009, dice que el nodo completo es el estándar oro y los nodos SPV son, diría, ciudadanos de segunda clase.

## Filtros Bloom

Vale, hablaremos de los filtros Bloom. Solo voy a tocar esto brevemente porque creía que Amiti habló de esto la semana pasada. Se definen en el BIP 37, implementado en Bitcoin Core en agosto de 2012. Permiten a los clientes ligeros solicitar sus transacciones sin revelar todo sobre sus direcciones. Están utilizando filtros probabilísticos, por lo que solicita más datos de los que necesita y eso debería proporcionarle cierto nivel de privacidad. Pero, de hecho, no son muy buenos para dar privacidad.

Esta es la implementación. Un cambio bastante importante en ese PR.

Luego, esta publicación de blog de Jonas Nick habla de cómo la billetera Android que utiliza filtros Bloom casi no te dio privacidad debido a la forma en que se construyó el filtro.

Y otro artículo de Arthur Gervais de ETH habla de los filtros Bloom.

«Mostramos que un único filtro Bloom filtra información considerable sobre los usuarios que poseen un número modesto de direcciones Bitcoin en los clientes SPV existentes.

Demostramos que un adversario puede vincular fácilmente diferentes filtros Bloom, que incorporan los mismos elementos, independientemente de la tasa de falsos positivos objetivo. Esto también permite al adversario vincular, con gran confianza, diferentes filtros Bloom que pertenecen al mismo autor.

Demostramos que un número considerable de direcciones de los usuarios se filtran si el adversario puede recopilar al menos dos filtros Bloom emitidos por el mismo cliente SPV, independientemente de la tasa de falsos positivos objetivo y del número de direcciones de usuario».

En términos de lograr su objetivo, los filtros Bloom no te dan muy buena privacidad. ¿Alguna idea sobre eso?

Miembro del público: Al final, acabamos de escribir algo muy complicado que no nos dio nada.

John: ¿Tal vez? Sí.

Miembro de la audiencia: Así que hablé de esto el otro día, ¿hay algún proceso para cambiar la redacción de los cambios? Si sabemos con certeza que no ayuda, ¿por qué guardarlo en la base de código?

Charla cruzada del público...

John: Responderé a eso en un segundo. La pregunta es, ¿hay alguna forma de revertir esto? Vamos a echar un vistazo.

Antes de hacerlo, en primer lugar, no es muy bueno preservar la privacidad y también carga en el servidor. Así que si eres un servidor que sirve estos filtros Bloom, estás haciendo el trabajo de cómputo para crear un nuevo filtro Bloom para cada cliente que se conecte a ti.

Miembro del público: Y tienes que correr por todos los bloques, ¿no?

John: Tienes que correr por cada cuadra. Sí. Volviendo a tu pregunta sobre el altruismo y el egoísmo. Creo que lo separaría de la propagación de bloques y transacciones, ya que al margen de la propagación de transacciones, probablemente no lo harías si no fueras del todo egoísta, pero hay un bien global.

A nivel local es altruista, pero a nivel mundial obtenemos un beneficio compartido de ello. Mientras que esto a nivel local es totalmente altruista, pero no hay ningún beneficio compartido global. Así que los filtros Bloom son mucho peores en la propagación de bloques de transacciones en términos de egoísmo. Y la propagación de transacciones y bloques tienen dentro de ellos algún tipo de protección DoS, como el bloque debe contener trabajo, la transacción debe contener una tarifa. Mientras que construcciones como esta, no hay protección DoS en absoluto.

Miembro del público: ¿Se han atacado grandes DoS en la red, utilizando filtros bloom?

John: No sé nada de eso.

Charla cruzada...

John: Sé que hay un repositorio de GitHub de Peter Todd llamado bloom-io-attack, así que tal vez puedas probarlo en casa si quieres. Sin embargo, «una única cartera de sincronización provoca 80 GB de lecturas de disco y una gran cantidad de tiempo de CPU para procesar estos datos». [fuente] Así que parece trivial para DoS.

Miembro del público: Muy asimétrico.

John: Muy asimétrico.

Miembro de la audiencia: Este problema surgió cuando estaba investigando /BIP 21/70... No siempre es tan sencillo como deshacerme del código incorrecto.

John: Así que BIP 70 es capa de aplicación. En realidad depende de la aplicación o del cliente. Esto es p2p, así que de nuevo depende del cliente. No es consenso en absoluto. Por lo tanto, los clientes individuales pueden decidir no participar en los filtros bloom.

La semana pasada hubo una pregunta sobre SegWit, y la respuesta es que no funciona con Segwit porque si el pubkey está en el testigo, eso no está incluido en el filtro bloom. Creo que intencionalmente, no actualizamos los filtros bloom para admitirlo. En general, no se aconseja. Si estás ejecutando un nodo completo, probablemente se deshabilitará en la próxima versión de Bitcoin Core.

...

John: Lo siento, he hablado mal. Deshabilitado de forma predeterminada.

Miembro del público: ¿No sería bueno tenerlo todavía, pero usando la autenticación cifrada de Jonas Schnelli? Así que si uso mi billetera Android, puedo autenticarme en mi propio nodo.

John: Sí, y Nicolas Dorier también quiere eso para BTC Pay Server donde te conectas a un nodo de confianza, y el nodo de confianza te sirve filtros Bloom.

Amiti: No lo entiendo. ¿Por qué quieres un filtro Bloom si es un nodo de confianza?

Miembro del público: No puedes filtrar la privacidad porque es tu nodo.

Amiti: Pero si confías en ello.

Miembro de la audiencia: ¿No puede su nodo de confianza tener un -

Miembros de la audiencia: No creo que haya en Bitcoin una forma totalmente segura de comunicarse con un nodo completo. La única forma es con el servidor electrum, no parte de Bitcoin Core. Luke está intentando implementarlo.

...

John: Así que aquí está Nicolas Dorier, mantiene Bitcoin Pay Server y dice que no hay razón para no usar filtros Bloom para pares incluidos en la lista blanca. Por lo tanto, si preconfigura la dirección IP de su par, debería poder hacerlo.

John: Esto fue en respuesta a las relaciones públicas de BlueMatt.

Miembro del público: Entonces, en esas estadísticas, ¿cuántos nodos lo tienen habilitado?

Miembro del público: Casi todos, como el 90%.

John: Muy bien, hablamos sobre los problemas de incentivos, los problemas de ataque DOS y los filtros Bloom generalmente no son fantásticos. Una propuesta más reciente son los filtros de bloque compactos, tal como se definen en BIP 157/158. De nuevo, no voy a hablar mucho porque Fabian habló de esto la semana pasada.

Esto cambia la propuesta BIP 37, por lo que en lugar de que el cliente solicite el filtro, el servidor crea un filtro basado en el bloque y puede servirlo a todos los clientes. Utiliza codificación Golomb-Rice en lugar de filtros Bloom, y se implementa por primera vez completamente en btcd, que es una implementación GO. Hay BIP157, en el fork de rosado inicialmente, pero ahora se fusiona aguas arriba con btcd. En Bitcoin Core, tenemos la construcción del filtro de bloques y tenemos un índice, y la parte P2P de eso es un trabajo en progreso.

Miembro del público: ¿Cómo funcionan estas transacciones con SegWit?

Miembro del público: ¿Cómo se crea un filtro que incluya SegWit? Direcciones, supongo.

Miembro del público: Hay diferentes tipos de filtros. Básicamente puedes poner todo lo que quieras en los filtros. Solo necesitas usar un tipo de filtro diferente. Puede crear un tipo de filtro que solo tenga TXID o cualquier otra cosa.

Miembro de la audiencia: ¿Está diciendo que la función hash tiene que cubrir los datos de los testigos de alguna manera cuando se calcula el TXID?

John: Creo que estos cubren el script pubkey.

Miembros del público: No creo que el testigo esté conmutado.

Creo que está hecho hash, es suficiente.

No hay compromiso con el agente testigo con el txid. Por eso es tan maleable. Estás filtrando con UTXIE. Puedes filtrar con cualquier otra cosa.

Fabian: Sí, pero básicamente puedes filtrar por cualquier cosa. Puedes tirar cualquier dato ahí que quieras... Es súper flexible.

John: Creo que el que se usa incluye todos los script pubkeys que se han creado y gastado en el bloque. ¿Es correcto? Y eso cubriría las direcciones si estás buscando una dirección.

Miembro del público: ¿Es como neutrino?

John: Esto es lo mismo. Neutrino es una implementación del BIP 157/158, y a menudo la gente llama neutrino del protocolo.

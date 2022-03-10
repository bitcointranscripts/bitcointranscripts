--
title: The Onion Model of Blockchain Security - Hasu
translation_by: AWS Translate
edited_by: Julien Urraca
tags: ['security']
---

Texto original: https://insights.deribit.com/market-research/the-onion-model-of-blockchain-security-part-1/

## El modelo cebolla de la seguridad de blockchain — Parte 1

11 de abril de 2020 | Investigación de mercado

Las blockchains públicas son empíricamente seguras. Durante la mayor parte de su historia (ciertamente corta) hicieron lo que estaban diseñados para hacer, procesando transacciones sin ningún contratiempo. Eso lo podemos observar. Es más difícil llegar a una teoría de por qué es así.

Las personas suelen explicar la seguridad de su proyecto favorito con lo que más entienden y valoran personalmente. Dependiendo de a quién se le pregunte, una blockchain pública está asegurada por incentivos económicos, por un poder de hash distribuido globalmente, por nodos completos o por una comunidad rabiosa que defiende un conjunto de valores compartidos. No es del todo sorprendente: la [ley del instrumento](https://es.wikipedia.org/wiki/Martillo_de_oro) sugiere que dependemos demasiado de herramientas que ya nos son familiares. Si tu única herramienta es un martillo, tiende a tratar todo como un clavo.

No creo que ninguno de los factores anteriores pueda explicar el fenómeno por sí solo. Es demasiado fácil crear ataques que tengan éxito a pesar de la protección perfecta en un área en particular. Por ejemplo, en una red donde todos los usuarios ejecutan un nodo completo, un minero aún podría reemplazar toda la blockchain por una alternativa en la que controle todas las monedas. Por lo tanto, debe ser la combinación y la interacción de las diferentes partes las que generan la cantidad de seguridad necesaria para un sistema de efectivo digital sin permiso.

##### El modelo cebolla de la seguridad blockchain

El modelo que propongo espera sintetizar los elementos individuales de seguridad en una imagen coherente. El objetivo es analizar la blockchain pública de manera más integral, detectar fortalezas y debilidades y permitir la comparación de diferentes blockchains.

La seguridad de una blockchain pública se parece a una cebolla, donde cada capa agrega seguridad adicional:

![onion](https://insights.deribit.com/wp-content/uploads/2020/04/onion-model-1.png)

Para destruir permanentemente una blockchain pública, es necesario destruir la fe de los usuarios en su estado de registro (la lista de propiedad), así como la capacidad de actualizar de manera confiable ese estado en el futuro. Todas las capas superiores sirven para evitar que esto suceda.

![funnel](https://insights.deribit.com/wp-content/uploads/2020/04/space-of-possible-attack.png)

Los ataques tienen que atravesar este embudo de capas defensivas antes de tocar el núcleo. Ahora discutimos las capas una por una.

#### Garantías criptográficas

El escudo más externo lo proporcionan las garantías criptográficas. La criptografía ofrece la forma de garantía más confiable, por lo que queremos que haga el trabajo pesado y evite la mayoría de los ataques desde el principio. La criptografía garantiza, entre otras cosas:

 - No imprimir monedas de la nada: todos los bloques (y, por lo tanto, todas las recompensas de bloques) deben tener una prueba suficiente de trabajo adjunta.
 - No gastar las monedas de otras personas: los esquemas de firma digital garantizan que solo el propietario válido de una moneda pueda gastarla.
 - No se puede cambiar retroactivamente el contenido de los bloques antiguos: los punteros hash aseguran que un atacante tenga que cambiar todos los bloques construidos sobre cualquier bloque antiguo que quiera cambiar.

Todos estos ataques son rechazados por el primer filtro:

Pero si bien la criptografía es muy poderosa, hay otras garantías que no puede proporcionar. Por ejemplo, no puede decidir cuál de dos blockchains igualmente largas es la «correcta» (eso requeriría conocimiento sobre el mundo real, como «a cuál de ellas cambiarán otras personas» y «cuál de ellas tiene el mayor valor de mercado a largo plazo»). Tampoco puede obligar a los mineros a extraer en un bloque específico, publicar un bloque una vez que lo encuentran o incluso asegurarse de que incluyan transacciones específicas.

#### Garantías consenso

Algunos de los ataques que pasan la primera capa se detendrán en el proceso de consenso. En el consenso de Nakamoto, los nodos observan constantemente la red y cambian automáticamente a la cadena más larga (más cara). A los mineros solo se les paga si sus bloques terminan formando parte de esa cadena más larga, por lo que deben converger con los demás mineros. Como resultado, existe un fuerte sesgo para que los mineros trabajen en la punta de la blockchain porque ahí es donde es más probable que todos los demás reconozcan su bloque.

Si un minero deshonesto quisiera minar en un bloque anterior, entraría en una condición de carrera con el reel primero de los mineros que siguen trabajando en la punta de la cadena. Solo si encuentra varios bloques más rápido que todos los demás combinados, puede alcanzarlos y luego seguir adelante. Pero dependiendo de su cuota de poder de hash, es muy poco probable que tenga éxito incluso con una reorganización muy superficial.

![consensus](https://insights.deribit.com/wp-content/uploads/2020/04/consensus-guarantee.png)

Para que un ataque funcione de manera confiable, el atacante primero debe obtener el control sobre la capa de consenso. Eso significa controlar > 50% del poder de hash en la prueba de trabajo, > 33% de la participación en la prueba de participación basada en BFT o > 50% de la participación en la prueba de participación basada en la cadena más larga.

La dificultad operativa de esto a menudo se subestima. Por ejemplo, los grandes gobiernos suelen ser vistos como el mayor riesgo para las blockchains públicas. Sin embargo, si quisieran comprar el hardware necesario en los mercados primarios, rápidamente descubrirían que la producción anual está limitada por las fundiciones de chips en China, Taiwán y Corea del Sur. Y su capacidad se ve limitada aún más por la minería de tierras raras en Australia, la producción de obleas en Asia y África, etc. Solo hay una cantidad limitada de capacidad disponible cada año, incluso para un comprador muy motivado. Adquirir el hardware necesario de esa manera podría llevar al menos 2-3 años y no pasaría desapercibido.

Solo China podría alcanzar el 50% de poder de hash confiscando el hardware existente o posiblemente coaccionando a los propietarios de las pools para que lanzaran un solo ataque. Esto podría funcionar, pero solo hasta que los mineros individuales comiencen a notar y dirigir su poder de hash a otra parte. Si bien es muy poco probable que un ataque como este funcione en contra de Bitcoin en el corto plazo, las redes más pequeñas controlan, respectivamente, acciones más pequeñas de potencia de hash o participación. En ese caso, el espacio de posibles atacantes puede incluir gobiernos más pequeños (deshonestos), así como a todo el sector privado.

#### Garantías económicas

Anteriormente he argumentado que, gracias a las garantías económicas, las blockchains no se rompen de inmediato si una sola entidad controla la capa de consenso. Al establecer los incentivos correctos, las blockchains pueden asociar un costo del mundo real con el mal comportamiento. La capacidad de pagar eso proviene del token nativo, introduciendo un concepto de escasez digital (y, por lo tanto, de valor) que puede recompensar el buen comportamiento (con recompensas y tarifas en bloque) y castigar el mal comportamiento (ya sea recortando los depósitos de seguridad o reteniendo recompensas futuras).

El tamaño de estos incentivos varía con el nivel de control que un actor tiene sobre la capa de consenso. Un actor que controla mucho poder de hash (incluso la mayoría) tiene proporcionalmente más que perder al destruir el sistema. De este modo, se desalientan los ataques con un castigo económico para el atacante.

Si un minero deshonesto quisiera minar en un bloque anterior, entraría en una condición de carrera con el resto de los mineros que continúan trabajando en la punta de la cadena. Solo si encuentra varios bloques más rápido que todos los demás combinados, puede alcanzarlos y luego seguir adelante. Pero dependiendo de su cuota de poder de hash, es muy poco probable que tenga éxito incluso con una reorganización muy superficial.

![economic](https://insights.deribit.com/wp-content/uploads/2020/04/economic-guarantees.png)

No todos los incentivos económicos son iguales. Una red con una recompensa de bloque mayor en relación con el valor de la red es más segura porque obliga a los mineros a tener más piel en el juego. (Esta es la razón por la que la disminución del subsidio en bloque representa un riesgo para la seguridad de Bitcoin).

Los mineros también tienen más piel en el juego cuando el hash requiere hardware especializado (los llamados ASIC) que no se puede reutilizar si la red desaparece. No es casualidad que todos los ataques mineros hasta la fecha hayan ocurrido en redes más pequeñas que se suscriben a una falacia llamada resistencia a ASIC, donde el control se puede adquirir con poca o incluso ninguna piel en el juego (por ejemplo, alquilando potencia de hash).

#### Garantías sociales

Anteriormente dijimos que para destruir permanentemente una blockchain pública, es necesario destruir la fe de los usuarios en su estado de registro (la lista de propiedad), así como la capacidad de actualizar de manera confiable ese estado en el futuro.

Esto es necesario porque las blockchains no son el fin en sí. No hay razón para empacar y volver a casa porque algunas partes fallaron temporalmente. Una blockchain es merely un medio para automatizar el proceso de establecer un consenso social entre sus participantes, una herramienta para mantener y actualizar una base de datos compartida. El estado de esa base de datos tiene valor para los participantes, y se les incentiva fuertemente a restaurar el sistema cuando se rompe.

Por ejemplo, si la función hash criptográfica se rompe, la capa social puede llegar a un consenso manual (guiado por expertos técnicos) para reemplazar la parte rota:

![social](https://insights.deribit.com/wp-content/uploads/2020/04/ecdsa-breaks.png)

Del mismo modo, si un ataque de consenso supera la etapa de garantías económicas, la capa social aún puede rechazarlo manualmente. Si un atacante con poder de hash mayoritario comenzara a hacer DOS la red extrayendo bloques vacíos, en plena aceptación del daño económico para sí mismo, entonces los usuarios podrían decidir cambiar la función PoW y, por lo tanto, eliminar el control de ese minero manualmente.

![reject](https://insights.deribit.com/wp-content/uploads/2020/04/social-guarantees.png)

Como podemos ver, la única forma de acabar con una blockchain para siempre es hacer que los usuarios pierdan interés en el estado del libro mayor o dañar el sistema hasta un punto que no pueda repararse.

![kill](https://insights.deribit.com/wp-content/uploads/2020/04/attacks-are-dangerous.png)

Los ataques son peligrosos cuando pueden perforar todas las capas y, en última instancia, desgastar el núcleo social del sistema hasta que ya no pueda anular el daño a las capas superiores y sanar.

Para que la sanación y la intervención manual funcionen, las comunidades de cada proyecto necesitan convenciones sociales sólidas en torno a las principales propiedades de su proyecto. En el caso de Bitcoin, estos valores fundamentales son la irreversibilidad de las transacciones, la resistencia a la censura, la ausencia de cambios incompatibles con versiones anteriores y el límite máximo de tokens de 21 millones. Sirven como planes de acción para cuando la intervención social se hace necesaria y crean puntos de Schelling en torno a lo que debe corregirse y lo que no.

Estos valores fundamentales de un proyecto se renegocian permanentemente y no todos los usuarios están de acuerdo en todas las propiedades. Sin embargo, cuanto más fuerte sea el acuerdo en torno a un valor en particular, mayor será la probabilidad de que se mantenga en tiempos de dificultades.

Si consideramos la capa social como la zona cero de cualquier blockchain, podemos ver que los ataques de ingeniería social son una gran amenaza. Las capas más altas se vuelven más vulnerables si los desarrolladores deshonestos pueden introducir cambios de código perjudiciales sin supervisión, particularmente en proyectos con políticas de bifurcación dura frecuentes (se recomienda leer sobre el tema).

#### Conclusión y partes futuras

Me parece útil el modelo cebolla para ver cómo las capas individuales de una blockchain pueden crear un todo seguro. En cierto modo, se basa en mi artículo anterior sobre el contrato social de Bitcoin: cualquier blockchain pública parte de un conjunto de valores compartidos en el núcleo, un plan de lo que el sistema espera lograr.

Ese conjunto de valores debe traducirse en reglas de comportamiento interpersonal (¡el protocolo!). Luego aplicamos estas reglas automáticamente, creando diferentes tipos de garantías: económicas, de consenso y criptográficas. Al restringir el comportamiento de sus participantes, el sistema se vuelve socialmente escalable, lo que permite la cooperación y, por lo tanto, la creación de riqueza en entornos de baja confianza.

Mantente atento a las partes futuras, donde comenzamos a aplicar el modelo a proyectos específicos, empezando por Bitcoin.

AUTOR (S)

Hasu

GRACIAS A

Su Zhu, Mike Co, Tarun Chitra, David Vorick, Georgios Konstantopoulos, John Adler, Eric Wall y Joe Kendzicky

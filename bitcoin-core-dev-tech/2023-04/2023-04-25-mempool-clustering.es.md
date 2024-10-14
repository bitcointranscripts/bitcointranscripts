---
title: Agrupación de Mempool
translation_by: Blue Moon
tags:
  - cluster-mempool
date: 2023-04-25
speakers:
  - Suhas Daftuar
  - Pieter Wuille
---
## Problemas Actuales

Muchos problemas en el mempool

1. El desalojo está roto.
2. El algoritmo de minería es parte del problema, no es perfecto.
3. RBF es como totalmente roto nos quejamos todo el tiempo, a veces hacemos/no RBF cuando deberíamos/no deberíamos.

## Desalojo

- El desalojo es cuando mempool está lleno, y queremos tirar el peor tx.
- Por ejemplo, pensamos que un tx es el peor en mempool pero es descendiente de un tx "bueno".
- El desalojo de mempool es más o menos lo contrario del algoritmo de minería.
- Por ejemplo, lo primero que desalojarías podría ser el primer tx que minarías.
- La primera cosa que desalojarías es el padre de tasa pequeña, pero su tasa descendiente es deseable para la minería.

## El algoritmo de minería tiene problemas

- El algoritmo de minería es algo que no podemos ejecutar a la inversa.
- Lo que quieres hacer es ejecutar el algoritmo de minería en todo el mempool - mira arriba para bloques, abajo para desalojos, pero esto no funcionará debido al tiempo de procesamiento.

- No sabemos qué tasa tx se incluirá en los bloques.
- El algoritmo de minería actual es cuadrático - inviable para el desalojo del mempool.

## RBF

- Comparar la tasa de entrada tx con la conflictiva tx.
- NO miramos las tarifas de los tx hijos.
  - PR [#26451](https://github.com/bitcoin/bitcoin/pull/26451) empieza a arreglar esto.
- Las reglas del BIP125 son un poco tontas (por ejemplo, no hay nuevos padres no confirmados).
- Ninguna de las tasas de las que hablamos en mempool nos dice dónde acabará una tx en un bloque.

"Así que hagámoslo"

## Pedido Total 

- Estas son las mejoras a la minería de bloques también mejorará entonces mempool desalojo, etc
- Esto debería hacer RBF mucho mucho mejor
- Elimina la incertidumbre sobre lo bueno que es un tx.
- Podemos comparar 2 txs y decidir cuál es mejor.
- No solucionará totalmente el bloqueo, la regla de tarifa total sigue siendo un problema, la retransmisión v3 lo soluciona.

- Solución "obvia" - en todos los puntos en el tiempo, ordenar mempool.
- Ancestro tasa solución ya es n^2, algoritmo óptimo es claramente exponencial, por lo que no funcionaría para ejecutar en todo mempool.

- ¿Por qué no limitamos el tamaño de los componentes conectados del mempool?
- Imagina que el mempool es un grafo, con aristas entre txs padres e hijos.
- Ordena cada componente conectado por separado, y luego haz algo sencillo para unirlos.

- Los clusters no pueden afectarse entre sí porque no están conectados
- Ejecuta el algoritmo cuadrático en cada componente conectado del mempool

- Esto introduce una nueva regla de política
- Hoy no hay límite de clusters, todo el mempool puede ser un cluster enorme.

- "Presentación": límite de tamaño del clúster. ¿Es algo con lo que los usuarios puedan lidiar?
- Podría significar que personas no relacionadas tienen txs relacionados por cluster.

- Ahora mismo hay un máximo de 25 antepasados.
- Es probable que sigamos necesitando un límite de antepasados, pero quizá ya no sea necesario un límite de descendientes.
- Puede que necesitemos algún tipo de excepción como la CPFP.

## Definiciones

- Cluster: conjunto de txs conectados en grafo.
- Linealización: cualquier ordenación topológicamente válida de txs en mempool.

- Normalmente hablamos dentro de un cluster.
- La construcción de bloques también es linealización.
- Hay muchas formas de hacerlo (el algoritmo basado en el feerato de antepasados es el que usamos hoy en día).

- f(cluster) -> linealización.
- Esto te dice en qué orden incluir las cosas.

## Pasos:

1. Identificar clusters en mempool.
2. linealizar cada cluster.
3. ¿?

- La parte difícil está hecha, hemos averiguado la mejor estrategia para todas las dependencias.
- Plantilla de bloques - usar esa información para sacar las mejores partes de tasa de cada cluster hasta que el bloque esté lleno.

## Trozos

Dada una linealización, podemos calcular dónde están los chunk breaks, dónde elegimos txs dentro del bloque. Empezamos siempre por el principio, pero sólo hasta donde queramos para maximizar la tasa. Mira todos los prefijos para elegir la tasa mas alta, todo es seguro para cortar, pero donde es el punto de corte mas optimo... siempre empieza por la izquierda.

## Ejemplo de trozo

- ¿De dónde puede haber salido esta linealización?
- Una vez que tienes la linealización, el gráfico original ya no importa.
- La función de linealización añade dependencias redundantes.

## Cómo calculamos los trozos

Empezando por la izquierda, se calcula la tarifa a medida que se avanza en el bloque (hacia la derecha), las tarifas suben y luego bajan (se detienen en el punto máximo). Para cada prefijo, se calcula la tarifa de cada prefijo y ver qué prefijo tiene la tarifa más alta (son n valores, no 2^n valores porque respetamos la ordenación de linealización).

Se ha seleccionado el primer trozo, ahora miramos las tasas de los txs posteriores al primer trozo. "El ejemplo parece cuadrático, pero en realidad es un algoritmo lineal".

## Volver a la Minería

- Obtenemos nuestros clusters, linealizamos los clusters.

- (¡¿Qué haces cuando violas el límite de sigops?!) necesitamos una heurística para evitar que eso ocurra, es decir, usar un modificador para multiplicar * el tamaño del tx si pensamos que el tx tiene más sigops de los que creemos que debería tener. Es mucho más difícil incluir sigops porque entonces estás optimizando para dos valores, no sólo para uno.

- El problema se complica hacia el final, tal vez se deban usar paquetes pequeños en relación con el bloque.

- De todos modos, el desalojo es ahora EXACTAMENTE lo contrario del algoritmo de minería.

- Las tarifas de los grupos suelen ser descendentes, ya que si no lo fueran, se habrían fusionado en un solo grupo. El primer chunk tendrá la tasa más alta del cluster. Así que para el desalojo, mira el último chunk en cada cluster, por lo tanto desalojamos las últimas cosas que minaríamos.

- El mempool siempre organiza los chunks, la minería escoge los chunks superiores, el desalojo escoge los chunks inferiores.Dentro de un cluster, los chunks son siempre de tasa decreciente. Podemos pensar en el mempool como una lista gigante de chunks. Mantenemos la estructura de datos en mempool todo el tiempo, a medida que llegan nuevos txs.

## Política de RBF 

- Nos aseguramos de que el chunk feerate de lo nuevo es mejor que el chunk fee rate de todo lo que sería desalojado. Al hablar de tasa de chunk fee, estamos usando la misma puntuación que usa el algoritmo de minería. Para una nueva tx, se mira si tiene padres y se cogen todos los clusters. Un nuevo tx puede fusionar clusters. Echa el nuevo tx en el cluster, ordénalo, averigua en que chunk estaría el nuevo tx, entonces ya tienes las puntuaciones mineras de todo lo que está a punto de ser desalojado.

- Así que podemos crear un nuevo mini mempool (sólo un falso cluster virtual) para cada nuevo tx entrante para probar sus propiedades de cluster.

## "¿Qué pasa con RBF reducido?"

- El cluster virtual también se ve afectado por el límite de tamaño del cluster. Cada nueva tx entrante podría fusionar clusters en un cluster demasiado grande.

- A mayor tasa, mayor tasa total, seguimos necesitando estas reglas para el DoS de la red
- Cuando se desaloja algo, es necesario volver a linealizar el clúster. Todavía necesitamos algún tipo de límite para no tener que reordenar todo el mempool cuando ocurre RBF. Los clusters no tienen un orden entre sí. Sólo ordenamos los clusters durante el minado o el desalojo, pero quizás podamos optimizar el seguimiento del mejor chunk de cada cluster.

- Cada tx tiene su propia tasa de tasa de chunk basada en el chunk en el que aparece en función del cluster en el que se encuentra. Esta es su puntuación individual, utilizada para RBF.

## Revisando Nuestros Problemas

- Ya no tenemos asimetría entre la minería y el desalojo.
- Si limitamos el tamaño del clúster lo suficiente tal vez podríamos ejecutar el algoritmo de minería en el clúster.

- ¿"Si quieres que minen tus tx, no hagas un cluster"?
- Ya no es tan sencillo hacer RBF con tus txs. Pero no importa, la gente sigue reglas simples: "si pagas más será elegido". Así que... los algoritmos de linealización deberían permitir lo que la gente suele hacer, quizás CPFP con unos pocos hijos. Después de eso, es sólo acerca de la prevención de ataques. ¿Puede un atacante crear un cluster que desencadene un comportamiento no compatible con el incentivo? Un atacante puede lanzar su tx en un gran cluster.

## Preguntas abiertas I

- BIP 125 eran reglas y términos que los usuarios podían entender, que producen resultados deterministas. Se podía saber de antemano qué funcionaría, pero sí se necesitaba un mempool para hacerlo. Este nuevo enfoque es más opaco, ejecutar un algoritmo caro en el cluster, ordenar, etc - convierte el algoritmo en una caja negra. Podríamos tener un RPC que devuelva las puntuaciones... BIP125 ya es demasiado difícil de modelar, y no es compatible con incentivos. Lo que hace la gente: "bumpfee, bumpfee, bumpfee" hasta que se retransmite.

- "¿Cuál es el coste del uso de memoria para este algoritmo?"
  - No lo sabemos, probablemente insignificante.

- Sólo porque veamos grandes clusters no significa que alguien realmente los necesite. Probablemente esté bien dividir los clusters entre bloques. Un límite de clusters es peor que un límite de descendientes, pero si te arriesgas a toparte con uno, te arriesgas a toparte con el otro.

- Puede que un usuario quiera hacer "fee-bump" en dos txs separados, pero al hacer "bump", une dos clusters, lo que ahora viola el límite. (pregunta abierta).

- Tal vez el límite de clusters sea de 50 o 100, sustituyendo el límite de descendientes de 25.

## Preguntas abiertas II

- Límite de hermanos
- Simple: rechazar cualquier cosa que rompa el límite de clusters
- Por ahora estamos descartando el desalojo de hermanos - podría ser otro ataque de pinning donde el atacante puede desalojar tu tx fusionando clusters, y todavía tenemos que gestionar la cuota total de retransmisión.

"Tasa de comisión del siguiente bloque" también puede ser confuso ahora, y la selección de monedas se hace más difícil si estás gastando monedas no confirmadas:

- Wallet tiene que averiguar en qué grupo está cada moneda.
- La elección de la moneda A podría volver a puntuar la moneda B que también podría querer usar.
- Ese grupo está lleno, así que no puedes gastar nada de él", etc.

Los terceros no pueden empeorar la puntuación de tu tx, sólo mejorarla.

- Al añadir más hijos, el tx padre sólo puede obtener mejor puntuación (hasta que se alcance el límite del clúster).

Ordenación óptima frente a ordenación por antepasados.

- Puede que los clusters de distinto tamaño se repartan de forma diferente
- Puede que los mineros optimicen la clasificación de los grupos mejor que los nodos de retransmisión.

¿Podría haber un problema al introducir el no determinismo en la red?

- ¿Vamos a romper más cosas?
- El no determinismo no importa, lo que importa es la línea de base de lo que garantizamos:
- Por ejemplo, ejecutamos el algoritmo antepasado siempre, y a veces hacemos más...
- Entonces ningún caso de uso real puede depender de algo más alto que esa barra.

Nos ha costado encontrar ejemplos en los que nuestros algoritmos de minería no hagan lo correcto.

Tal vez podamos incluso retransmitir clusters ordenados, tal vez alguien tenga una ordenación mejor que la tuya, compartámosla.

Un nuevo tx entra, podríamos simplemente lanzarlo al final de su cluster y luego re-linealizar más tarde. es decir, tener múltiples linealizaciones para el mismo cluster, y luego fusionarlas.

## Preguntas abiertas III

- Tomamos el peor chunk de todos los clusters y lo desalojamos.
- El "problema de la retransmisión libre" - si puedes desalojar un chunk usando sólo un nuevo tx entrante, eso es malo.
- Quizás necesitemos un límite de tamaño de chunk y un límite de tamaño de cluster.
- ¿Todavía necesitamos un límite de tamaño de ancestro actualmente es 101 kvb?

## Trabajo futuro

- Resolver los límites de tamaño de los clústeres.
- Efectos descendentes: impacto positivo en la retransmisión y validación de paquetes.
- Quizá haya que reconsiderar la estimación de tasas en general (la estimación de tasas no funciona debido a la CPFP).

## Tiempo DEMO

eje y: tarifa total acumulada
eje x: vBytes totales
"¡Alguien está pagando unas tasas enormes ahora mismo, estropeando el gráfico!"

`getblocktemplate` es mucho más rápido con esto.

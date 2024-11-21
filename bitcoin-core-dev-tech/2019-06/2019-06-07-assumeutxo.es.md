---
title: AssumeUTXO
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - assumeutxo
  - bitcoin-core
date: 2019-06-07
speakers:
  - James O'Beirne
---
<https://twitter.com/kanzure/status/1137008648620838912>

## Por qué assumeutxo

assumeutxo es la continuación espiritual de assumevalid. ¿Por qué queremos hacer esto en primer lugar? En la actualidad, la descarga inicial de bloques tarda horas y días. Varios proyectos en la comunidad han estado implementando medidas para acelerar esto. Casa creo que incluye datadir con sus nodos. Otros proyectos como btcpay tienen varias formas de agrupar esto y firmar las cosas con claves gpg y estas soluciones no son del todo a medias, pero probablemente tampoco son deseables. La idea aquí es que queremos hacer algo análogo y hacerlo bien y relativamente seguro. Técnicamente hay un ligero cambio en el módulo de seguridad.

## Qué es assumeutxo

Obtiene una instantánea serializada del conjunto UTXO obtenida por un peer. Todo depende de un hash basado en el contenido del conjunto UTXO. El peer obtiene la cadena de cabeceras, se asegura de la base de la instantánea en la cadena, carga la instantánea. Quieren verificar que la base de la instantánea o el blockhash está en la cadena de cabecera. Cargamos el snapshot que deserializa un montón de monedas y lo carga en memoria. Entonces falsificamos un blockchain; tenemos un chainstate pero no bloques en disco, así que es casi como una gran cadena podada. A continuación, validamos que el hash del conjunto UTXO coincide con lo que esperábamos a través de algunos  assumeutxo codificado. Este es un valor de parámetro compilado, no puede ser especificado en tiempo de ejecución por el usuario, lo cual es muy importante. En ese momento, sincronizamos la punta y que será un delta similar a lo que sería assumevalid ahora, tal vez más frecuentes porque eso sería bueno. Crucialmente, comenzamos la verificación en segundo plano usando un chainstate separado donde hacemos la descarga inicial regular de bloques, bnackfill que hasta la base de la instantánea, y comparamos eso con el hash del inicio de la instantánea y verificamos eso.

La fakechain es un objeto CChainState sin ningún blockdata. Es una cadena de encabezados ordenados. Es algo así como una cadena podada. Cargamos en la instantánea, deserializamos todo en un CCoinsView y luego tenemos que construir un objeto de cadena para ir con eso a pesar de que no tenemos ningún dato de bloque. Estamos avanzando rápidamente una cadena de cabecera hasta la base de la cadena. Tenemos que pensar en algunas cosas como ntx y chaintx para obtener una estimación precisa del tiempo de verificación restante hasta la punta. Hay algunas cosas que tenemos que hackear ahí.

P: ¿Qué pasa con los reorgs?

R: No tenemos en cuenta los reorgs que entran en la instantánea. La idea es que la instantánea tenga al menos una semana de antigüedad. No habrá ninguna reorganización que lo haga, y si lo hacemos tendremos problemas mayores.

## Demostración

Hay una demostración de assumeutxo. Aquí hay una demostración. Esta demostración es un nodo servidor que he pre-poblado hasta una altura de como 30.000. Básicamente vas a ver esta sincronización a punta. Esta cosa es sólo 4000 bloques por delante de la instantánea. Luego se cambiará a la validación de fondo, y luego ves la cadena de validación de fondo desaparecer. Todo esto es a través de algún hacky llamada RPC que he creado.

## Uso del monedero durante la descarga inicial de bloques

Una vez que el usuario obtiene la punta de red puede empezar a utilizar la cartera. Una advertencia es que si la cartera tiene una última altura actualizada por debajo de la base de la instantánea, bueno, no podemos hacer eso hasta que podamos volver a escanear, así que simplemente no lo permitimos.

## Objeciones

Esto es más fácil de atacar que assumevalid. Con assumeutxo, todo lo que tienes que hacer es serializar un conjunto UTXO malo, darle a alguien un hash malo y conseguir que alguien acepte ese hash malo y entonces le convences de que quizás sus monedas no existen o lo que sea. La seguridad aquí depende de usar el binario correcto. El argumento es que si estás usando el binario equivocado, hay un millón de maneras diferentes de joderte muy fácilmente de todos modos.

Alguien planteó la cuestión de que si estamos de acuerdo con aceptar este modelo de seguridad instantánea mientras estamos validando, entonces tal vez la descarga inicial de bloques en segundo plano no tenga sentido. ¿Qué pasa en esta implementación si el resultado de la IBD en segundo plano no coincide con esto? Nos volvemos locos y cerramos. Así que te estás acercando a la punta de todos modos, por lo que sólo podría sobrescribir ... podríamos reorg. Podrías invalidar el bloque del assumeinvalid y luego sigues adelante. Gritar y cerrar parece lo correcto. Necesitan saber que su binario está roto. Así que cerramos. O los desarrolladores son corruptos. O hay un error. Lo que realmente debería hacer es borrar el binario de Bitcoin Core cuando eso ocurra ((risas).

En el mejor de los casos, significa que hay que recuperar medio año de bloques porque hacemos lanzamientos cada 6 meses. Así que hay una aceleración máxima que esto puede hacer. Cuando miré las opciones para las alternativas de casa hodl, o está listo inmediatamente que es lo que un usuario quiere, o esperan. Que esperen 6 horas o 2 días es diferente, pero es muy diferente esperar medio minuto que esperar una hora. Básicamente hay una preferencia de experiencia de usuario. Me parece estupendo, pero no creo que resuelva el problema de que un usuario lo quiera inmediatamente.

P: ¿Cómo se construye el hash del conjunto UTXO? Llevo un año trabajando en ello.

R: Buena pregunta. Por ahora, es un hash ingenuo del contenido del conjunto UTXO. Eso depende de cómo queramos transmitirlo, de cuáles sean los contenidos. Una opción es que sea una raíz merkle. Creo que vamos a querer hacer algún esquema donde bech-codificar esta cosa y dividirlo en un montón de diferentes trozos. La estructura de compromiso, no estoy muy seguro todavía).

Sería útil si sipa está rodando hash, y podemos eventualmente hacer un compromiso. Podemos hacer assumeutxo primero, y luego más tarde, podríamos hacer.... Es como el problema del huevo y la gallina. Hay un montón de fruta madura que se puede arreglar con utreexo. Ya puedes verificar incrementalmente; puedes preguntar por UTXOs en el set; no tienes que descargar 4 GB de una vez para ver. Usted podría decir, el uso de recursos de chainstate duplicado es significativo, pero en utreexo usted podría decir que voy a hardcode un centenar de diferentes raíces UTXO y se puede validar en paralelo, como imaginar 80 núcleos no sólo 4 núcleos o algo así. Son conjuntos UTXO sugeridos, y puedes validarlos todos y ver si se enlazan.

En assumeutxo, si obtienes un set falso entonces podría haber algunas monedas que no existen. Pero si tu utreexo es falso, entonces detectarás dentro de algunos bloques que es falso. Otra cosa que podrías hacer es codificar puntos de control separados y luego dependiendo de cuando se creó el monedero, puedes tomar el que era anterior a cuando se creó el monedero y partir de ahí. La validación la haces después.

## Cómo assumeutxo

He dividido esto en fases. La primera fase es permitir el uso de instantáneas a través de RPC, y ningún mecanismo de distribución. Sólo los usuarios sofisticados harán esto. No importa de donde lo obtengan. Tal vez poner el hash en un CDN, pero no queremos hacer esto a largo plazo. Podríamos usar bittorrent, IPFS, lo que sea. La segunda fase es más especulativa, pero es construir una capa de distribución en la red p2p, con trozos codificados FEC. Podríamos dividir las instantáneas en códigos Reed-Solomon y códigos fuente para que no sea sólo un striping ingenuo de datos que sería vulnerable al DoS. Pero con Reed-Solomon tienes que hablar con n pares únicos y luego juntar las piezas a partir de ahí.

Para la fase uno, tenemos que hacer un montón de refactorización porque en el código asumimos que sólo hay un único estado de la cadena. Se han fusionado algunos pull requests relacionados con esto. Hay alguna lógica de creación/activación de instantáneas. Hay algunos cambios menores en net_processing. Tenemos que pensar en cómo afecta esto a la poda y a la gestión de la caché, e introducir algunos RPC nuevos.

Debemos asumir que no va a haber un soft-fork para assumeutxo. Deberíamos intentar hacerlo funcionar sin uno. Si conseguimos un soft-fork para ello, entonces genial. Si hacemos assumeutxo entonces tendremos una intuición de cuál debería ser la estructura de compromiso en el soft-fork. La razón por la que no tenemos compromisos UTXO conjunto es que se ha discutido lo que debería ser cada vez que ha surgido. Así que un assumeutxo de trabajo podría darnos alguna evidencia o experiencia con esto y ser capaz de tomar una mejor decisión acerca de un soft-fork para UTXO conjunto de compromisos.

## Detalles de refactorización

Ahora mismo, el modus operandi es tratar con la interfaz que te da validation.h, y esta opera sobre un chainstate global. En su lugar, se ha hecho pública la interfaz CChainState, que ya está fusionada. Ponemos toda la funcionalidad global en los métodos CChainState y puedes pasar estos objetos. Dividimos los datos de los bloques compartidos en una nueva clase, BlockManager. Todas las vistas CCoins son propiedad de una instancia CChainState dada. Todos los callbacks de la interfaz de validación ahora necesitan saber con qué chainstate están tratando.

`g_chainmain` es el gestor de chainstate y abstrae el tratamiento de múltiples chainstates, actúa como una fábrica para la creación de chainstates. Hace un montón de cosas.nts.

## Detalles de la cartera

No vamos a volver a escanear si la cartera se actualizó antes de la base de instantáneas. La solución a esto podrían ser los filtros de bloque, podríamos usarlos también aquí. Sí, definitivamente.

## Detalles de la caché

La ventaja de tener una caché grande sólo entra en juego cuando estás haciendo mucha validación. Yo asigno la mayor parte de la caché a la validación en segundo plano de chainstate, y después la vuelvo a asignar a la otra. Una vez que llegas a la punta, entonces comienza la validación en segundo plano.

## Detalles de la poda

La poda puede realizarse de forma agresiva para la validación en segundo plano del estado de la cadena, ya que no esperamos reorgs (dentro de 1 bloque de la punta). Un poco marginal debido a los 3 GB extra de chainstate.

## Cosas de utreexo

Si desea assumeutxo que es la misma estructura que utreexo, usted puede hacer eso sin preocuparse de cualquier almacenamiento en caché porque el punto no es tener un pequeño nodo el punto es para que yo pueda descargar incrementalmente todo el conjunto UTXO y luego ir de allí como un nodo normal. Así que eso es como usar una pequeña parte de utreexo, es básicamente algunos árboles merkle en algún punto. No te importan las transiciones en el estado del acumulador, sólo tienes un único estado del acumulador y quieres verificar UTXOs allí. Usted no quiere perder ningún UTXOs, ya sea, pero eso es sencillo.

¿Tiene ventajas validar hacia atrás? ¿Si una moneda termina en un OP_RETURN entonces no tienes que verificar las firmas en el pasado? Bueno, sigues queriendo estar en sintonía con los demás. No sé si lo de las 10 validaciones paralelas diferentes es útil, parece que no pero puede ser. Usted puede simplemente establecer que el número de núcleos que tiene. Bueno, se hardcode como 100 de ellos, y luego se utiliza como muchos hasta el número de núcleos de su CPU tiene.

## Otros cambios

En algunos lugares, en lugar de actuar sobre un único estado de cadena, obtenemos todos los estados de cadena relevantes del gestor de cadenas. La diferencia real en net_processing es mínima. Luego hay algunas cosas de init/shutdown, algo de serialización de metadatos sobre si tenemos a o no... realmente no hay mucho.

El formato de las llamadas RPC, sólo escribe bytes serializados. Está reutilizando lo mismo que usamos para getutxosetstats. Sólo vamos en orden, para cada uno en el leveldb. Creo que esto funciona.

## Sobre la fase 2

Los nodos almacenarían cierto número de trozos codificados FEC a través de n instantáneas históricas. En esta versión, assumeutxo no es un escalar, sino una lista de pares altura-hash. ¿Cómo generamos instantáneas antes de que assumeutxo se actualice? ¿Cuántas instantáneas guardamos de todos modos? Tal vez digamos que cada 40.000 bloques generamos una instantánea o algo así. No he pensado en ello.

La codificación FEC resuelve el problema de que, para cada nodo, queremos que cada nodo almacene unas cuantas versiones de la instantánea, pero la carga de almacenamiento podría ser alta. No quieres recuperar tu instantánea de un único nodo. Es que no quieres recuperarla de un único peer, no que no quieras almacenarla. Si no utilizas el código de borrado, alguien podría hacer DoS en la red y eliminar todos los nodos que ofrecen una instantánea específica de datos. Pero en mi mente, ¿por qué no todos los nodos tendrían estos datos de todos modos?

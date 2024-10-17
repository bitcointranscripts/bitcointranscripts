---
title: El futuro de Lightning
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - lightning
speakers:
  - Elizabeth Stark
---
El futuro de lightning

El año del #craeful y el futuro de lightning

<https://twitter.com/kanzure/status/1043501348606693379>

Es estupendo estar de vuelta aquí en Riga. Demos un aplauso a los organizadores del evento y a todos los que nos han traído aquí. Este es el momento más cálido que he vivido en Riga. Ha sido genial. Quiero volver en los veranos.

# Introducción

Estoy aquí para hablar de lo que ha ocurrido en el último año y del futuro de lo que vamos a ver con los rayos. Un segundo mientras conseguimos que el clicker funcione. La tecnología nunca funciona en los eventos tecnológicos. No es la primera vez. Vale, genial. Vale, a veces funciona.

Hace un año, en realidad menos, hace unos 10 meses, estuve en el Baltic Honeybadger. Al final de mi charla, mencioné lo emocionado que estaba por todas las cosas geniales que vendrían en 2018. Y ahora aquí estamos. Necesitamos micropagos para que pueda usar un micropago para poner en marcha mis diapositivas aquí en lightning.

Creo que ahora estamos bien con el clicker. Crucemos los dedos.

# Historia

Para aquellos que no hayan estado siguiendo las últimas novedades de lightning.... el año es 2008 y hay una persona con seudónimo que se llama Satoshi Nakamoto y publica un libro blanco al mundo con poca o ninguna fanfarria y básicamente a nadie le importó. El décimo aniversario de este documento es el 31 de octubre de este año. Estamos súper emocionados por esto. Sí. Creo que vamos a tener algunas grandes fiestas de Halloween.

La primera respuesta, unos días más tarde, fue básicamente "este sistema suena muy bien, pero no creo que se adapte al tamaño requerido", así que básicamente "la historia es genial, hermano, pero no se adapta". Esto se reconoció muy pronto. Cuando tienes un sistema de consenso global descentralizado, hay problemas de escalabilidad.

Avanzando rápidamente hasta 2015 hay un documento que ayudé a editar... llamado Lightning Network. Es una serie de contratos inteligentes que operan sobre bitcoin, un protocolo de capa 2 que utiliza el consenso local.

# Resumen de la red Lightning

Alice y Bob celebran un contrato multisig de 2 en 2 Alice y Bob celebran un contrato multisig de 2 en 2 para entrar en un lightning. Ambos ponen algo de dinero y luego actualizan el estado entre ellos. Estas son transacciones reales de bitcoin. Por cierto, no hay ninguna ICO de Lightning. Lo sé. Utiliza transacciones reales de bitcoin. Alice y Bob actualizan su estado cuando envían dinero entre ellos. Cada vez que actualizan el estado, firman un nuevo estado y revocan el anterior para que no puedan robarse mutuamente faltando a su palabra. El cierre cooperativo puede hacerse en 10 minutos.

# Pagos como paquetes

Puede que Alice y Bob sólo se vean una vez en una luna azul. Se puede tener una red y los pagos se pueden enrutar a través de otros nodos. Para ello se pueden utilizar contratos multisaltos y contratos hash de bloqueo de tiempo (HTLC). La forma en que funciona el reenvío en lightning es que los nodos intermedios pueden recibir fondos sólo si va atómicamente al remitente. En la gran mayoría de los casos, se transacciona instantáneamente y va al final de la ruta. También tenemos el enrutamiento cebolla, que consiste en que los nodos intermedios sólo conocen los nodos anteriores y posteriores, pero no la ruta completa.

Eliminamos el riesgo de contrapartida. No tienes que confiar en Alice o Bob o cualquier otra persona en el sistema.

# Si Alice se desconecta...

Tal vez Alice esté harta del twitter de bitcoin y se vaya a una isla desierta... ¿qué pasa con Bob? Bob puede emitir una transacción a la cadena y espera un tiempo determinado y luego recupera su dinero. Alice recupera su dinero cuando se conecta de nuevo y todo el mundo está completo.

# Si Bob trata de hacer trampa...

No se puede inventar un estado que no existe, pero se puede transmitir un estado anterior. Si Alice está desconectada, tal vez una torre de vigilancia estaba monitoreando y vio que Bob estaba tratando de hacer trampa. Esto puede ser aplicado en la cadena de bloques usando contratos pre-firmados. Bob no debería tratar porque si lo intenta, perderá todo su dinero.

# Eliminación del intermediario financiero de confianza

No hay que confiar en Alice o Bob. La cadena de bloques funciona como un juez o mecanismo de resolución de disputas. Puedes pensar en los contratos de la cadena de bloques como en los contratos. No todos los contratos van a los tribunales. La gran mayoría de las transacciones relámpago no irán a la cadena de bloques. No se puede sobornar. Estas transacciones están pre-firmadas y sabemos exactamente lo que va a pasar y cómo se va a cumplir. Esto se basa, por supuesto, en la seguridad de la cadena de bloques, y bitcoin es la cadena de bloques más segura y con más hashrate que la respalda.

# Lightning para muchas cadenas de bloques

Lightning también funciona con litecoin, que activó segwit. Hay un concepto de intercambio atómico entre cadenas de Lightning. Bob y Alice están en dos monedas diferentes y pueden ser dirigidos a través de un intermediario y hacer un intercambio atómico entre los dos. En noviembre de 2017 se produjo el primer swap atómico de cadena cruzada de relámpagos. Esto es algo emocionante en progreso.

# Lanzamiento de lightning

Esta es la recapitulación para las personas que hayan estado bajo una roca durante el último año. Como es el caso en la comunidad bitcoin, toda esta tecnología es de código abierto. Implementamos algo llamado lnd, lightning network daemon. Tenemos casi 3k estrellas de github, así que eso es emocionante. Recomiendo encarecidamente que compruebes el código fuente. Este año pasado ha sido un viaje salvaje. En enero de 2017 anunciamos la alfa para lnd y tuvimos una increíble comunidad de personas construyendo y probando.

La gente no dejaba de preguntar cuándo mainnet cuando mainnet. En marzo de 2017, anunciamos la primera beta para la red lightning. Esto fue algo enorme. No dormimos durante una semana en nuestro equipo. Lo pusimos a disposición del mundo, lo cual fue súper emocionante. Este fue un gran hito en el año pasado. La cantidad de progreso que hemos visto desde entonces ha sido alucinante.

La semana pasada, anunciamos la beta de lnd 0.5. Esto incluye mejoras en el cliente neutrino lite, mejor soporte telefónico, mejor soporte de privacidad, más soporte de tor, mejoras en la fiabilidad, mejor pathfinding. Para aquellos que ejecutan lnd, por favor actualicen si aún no lo han hecho.

# Interoperabilidad

Hay Blockstream c-lightning y ACINQ eclair client, y rust-lightning por BlueMatt, y algunas implementaciones de alguien en Japón. Todos hemos trabajado a partir de una especificación común. Sólo hay una red lightning, como Internet. Queremos que todo sea interoperable. Aquí está el repositorio de especificaciones de BOLTs. En diciembre de 2017, anunciamos que se habían completado las pruebas de interoperabilidad entre las 3 principales implementaciones. Así que creamos una red lightnings interoperable. Sé que mucha gente está entusiasmada con eso.

# Desarrolladores, desarrolladores, desarrolladores, desarrolladores

Es importante conseguir desarrolladores y construir una aplicación utilizable. La semana pasada, en Lightning Labs, lanzamos una nueva versión de nuestra aplicación de escritorio Lightning. Tenemos este hermoso diseño con colores frescos. Nuestro objetivo era hacer que la gente use e interactúe con Lightning de forma sencilla. Está en modo de prueba. Ahora mismo es una versión de prueba de la red. La versión mainnet depende de neutrino.

En este vídeo, nuestro principal desarrollador de aplicaciones es... por favor, trabaja. ¿Tengo que pulsar algo? ¿No? Muy bien. Tankred es de Alemania y es nuestro principal desarrollador de aplicaciones. El equivalente alemán del café es... usó nuestra aplicación de escritorio para comprar una cerveza. Pensó que lo del café era divertido pero que una cerveza sería mejor. Ahora mismo es el Oktoberfest en Alemania.

# lnd 0.5

Neutrino ha logrado un gran hito. Neutrino es una implementación de cliente lite que usamos en Lightning Labs junto con Jim Posen de Coinbase han diseñado eso. BlueMatt ha estado involucrado en eso. Incluye bip157 y bip158. Es sustancialmente más privado y no filtra varios datos del usuario y la información de las transacciones. Esto es algo muy grande.

# Torres de vigilancia

La gente ha estado preguntando sobre la aplicación de escritorio... ¿cuándo móvil? Uno de los aspectos importantes de la compatibilidad con los teléfonos móviles no es sólo neutrino porque no quieres ejecutar un nodo completo en tu teléfono, sino que tenemos torres de vigilancia que son importantes. Puedes estar de viaje durante una semana y queremos asegurarnos de que hay torres de vigilancia que controlan si hay trampas en la red.

# Una plataforma para comerciantes

Por alguna razón, a la gente le gusta hablar de comprar café con bitcoin. Tenemos una plataforma para comerciantes de alto rendimiento donde se puede comprar... ¿está bitrefill? Tenían soporte de mainnet cuando lanzamos la beta de lnd. La gente estaba comprando cosas reales con bitcoin real usando Lightning. De hecho, al día siguiente, nosotros en Lightning Labs dio una charla en Airbnb, de nuevo no tenía idea de que sería el día después de la beta y laolu demostró esto conmigo y compramos minutos de teléfono celular con bitcoin. Habíamos estado trabajando en esto durante tanto tiempo, y la mierda que realmente funcionó. Así que fue increíble ver eso.

También tuvimos btcpay para aquellos que no saben que es una versión de código abierto de software de procesamiento de pagos comerciales. NicolasDorier y algunos otros desarrolladores han estado trabajando en esto durante un tiempo y se sintieron frustrados con otras tecnologías en este espacio, por lo que crearon el suyo propio. Tienen soporte para Lightning. Si desea ejecutar el procesamiento de los comerciantes, echa un vistazo a btcpay.

GloBee ha habilitado el procesamiento de pagos lightning.

Creo que tenemos a Coingate aquí en la conferencia. No podíamos creerlo, son 4000 comerciantes los que ahora aceptan Lightning. Ha sido increíble ver cómo ha evolucionado esto en el último año.

# Una capa de aplicación para bitcoin

No sólo es lightning una tecnología para las transacciones de alto volumen en bitcoin, también es una plataforma de desarrollo de aplicaciones para bitcoin. Tenemos yalls.org, mi cofundador laolu nombrado esto. Un sitio similar con un nombre similar no estaba utilizando relámpago. Así que yalls es un sitio de micropagos de artículos donde puedes usar lightning para pagar artículos, o puedes comprar cervezas o un emoji de cerveza.

Tenemos zap, que es una aplicación y una interfaz de usuario para bitcoin y litecoin. Estoy seguro de que tenemos algunas personas en la sala han utilizado eso. ¿Cuántas personas en esta sala han enviado una transacción con Lightning? Bien, genial. ¿Cuántos planean hacer una transacción Lightning en el próximo año?

# Satoshi's Place

En junio de 2018 hubo un sitio web que se puso en línea... Tomé una captura de pantalla, estaba pensando que necesito mostrar una captura de pantalla de esto para Baltic Honeybadger. Solía haber una página web de un millón de dólares y pagabas por píxel. En algunas versiones, no podías sobreescribir los píxeles. Esta es principalmente una versión segura para el trabajo... Tengo algunas orejas de diablo puestas, pero no es tan malo. Estoy agradecido a mis amigos y al equipo por restaurar mi imagen en esto, gracias. Esto estuvo en la portada de reddit y se hizo viral. Se trataba de una aplicación en la que se podía enviar 1 satoshi por píxel. Este fue un momento importante para el lightning que a pesar de que esto podría ser un sitio web tonto donde estamos manteniendo bitcoin raro ... advertencia, si usted va allí ahora, podría no ser seguro para el trabajo.

Hubo guerras de píxeles .. Tuve que ir al scrollback en youtube. Yo estaba en el sitio de satoshi y tratando de averiguar lo que pasó, pero alguien puso el sitio oculto FBI incautado. El creador de este sitio gana 60-70 dólares cada vez que hacen esto. Por suerte la comunidad había guardado los estados anteriores y se revirtió. Hay estas guerras de píxeles aquí. Así que ¿por qué no hacer algunos futuros de píxeles y tener un mercado para eso?

# Tareas de Lightning

lnd.work es un sitio mecánico para lightning. Puedes pagar pequeños micropagos para hacer pequeñas cantidades de trabajo. Compruébalo, publica algunas tareas también.

# Primera vez

El año pasado tuvimos muchas primicias. Por ejemplo, aquí se compró el primer libro con lightning, el estándar de bitcoin. Sé que estamos escuchando sobre eso aquí hoy. No podemos estar al día con todo lo que está pasando, es sorprendente e increíble. La gente puede comprar cosas con lightning aquí. Gran trabajo para los que lo pusieron ahí. Alguien compró el primer sándwich con un rayo. No quedan muchas más primicias, como la primera champaña o el primer zapato, entonces será mejor que lo hagan pronto porque las primicias se están acabando.

# Construyendo la red

Cuando estuve aquí en noviembre pasado, estábamos en testnet pero no había nada en mainnet. Pero en febrero de 2018 esto es lo que la gente estaba haciendo en testnet: había mucho compromiso. Vimos cómo se desarrollaba el mapa de la red y cómo la gente ponía en marcha nodos y los hacía funcionar. Este es el estado de testnet en aquel entonces. En enero de 2018 solo había 46 canales de la red de lightning. En septiembre de 2018, hay más de 12.000 canales. Es increíble ver este crecimiento. Los exploradores no son canónicos y es posible que tengan vistas anticuadas de la red, y puede que algunos de los canales ya no estén activos. En términos de orden de magnitud, definitivamente hemos visto un crecimiento increíble. Advertimos a todo el mundo cuando lanzamos la beta, "ser precavidos".  Tenemos un límite de BTC y demás. No pongas los ahorros de tu vida en un lightning.

Aquí está el mapa de romport de la red lightning. Creo que hay unos 107 BTC en la red. Esto es mucho. No pongas mucho dinero en lightning. Veremos por qué en un segundo. Ha sido salvaje ver cómo evoluciona esto.

# Craeful

John Olivier hizo este increíble segmento en marzo donde dijo a la gente en lugar de estar en hodlgang, usted debe ser craeful. No pongas más dinero en la red de rayos de lo que estás dispuesto a perder. Le dije a la gente que pusiera 20 dólares o algo no muy grande.

# shitcoin.com no puede comprar nodos de lightning

Puso un artículo que va a comprar todos los nodos. Pero ni siquiera se puede comprar nodos. No es así como funciona. Puso 40 BTC en la red. Hubo límites de nodos y de transacciones. Abrió un montón de canales. Alex Bosworth, recientemente contratado en Lightning Labs, dirige yalls.org y una variedad de otras cosas... Alex tenía alrededor de 1 BTC y Andreas tenía 44 BTC pero resulta que Alex hizo más dinero con su 1 BTC que Andreas con sus 44 BTC. Ganó 40 veces más con estas comisiones.

Nick Bhatia ha estado haciendo un gran blog sobre el valor temporal del bitcoin. El rendimiento anualizado de Alex en su BTC fue 80 veces mayor que el de Andreas. Alex abría manualmente canales a nodos específicos que le gustaban. Andreas recuperó todos sus fondos en el evento, esperemos que no lo haga hasta que LN esté más avanzada. Se trata de optimizar sobre dónde te conectas en la red.

# Casa

Hay un nodo de lightning Casa.

# Comunidad

Hemos estado haciendo hackdays de lightning en Berlín. Alguien instaló una máquina de caramelos de rayo allí también. Alguien decidió tomar una foto de mí mientras yo estaba hablando y luego lo puso en twitter y el lugar de satoshi mientras yo estaba hablando mientras yo estaba en el hackday de lightning en Berlín. Amir Taaki tuiteó sobre lo comprometida que estaba la comunidad. Tuvimos 150 personas de toda Europa que vinieron a participar. Nos sorprendieron las preguntas y lo avanzado que estaba todo el mundo y ver el compromiso de la comunidad. Estamos viendo cómo surgen en otros lugares y eso es increíble, uno en Nueva York y otro en Madrid.

# El año que viene

Estamos trabajando en las torres de vigilancia. Neutrino tendrá más actualizaciones. lnd 0.5 tenía neutrino sólo para testnet. Queremos un software seguro. Creemos que debemos tener un software financiero seguro. La mainnet de Neutrino llegará pronto, lo que permitirá las aplicaciones móviles de lnd. Y las aplicaciones de escritorio no tendrán que sincronizar todo la cadena de bloques. También estamos interesados en los pagos atómicos multitrayecto, en los que se dividen los pagos de 10 dólares en 5 pagos de 2 dólares. Irían atómicamente por la red y llegarían al destino totalmente completos o volverían al remitente. Esto es importante para la liquidez y el flujo. El empalme es donde se pueden añadir fondos a un canal. También se puede enviar una transacción desde un canal, lo que se denomina "splice out".  Alex Bosworth habilitó manualmente los canales. Cuando tenemos cosas en marcha, queremos enrutar y encontrar caminos manualmente que Alex estaba haciendo manualmente.

Jameson nos recordó, y quiero transmitirlo, que queremos que esta tecnología sea privada y que habrá canales privados. Estos sitios web del explorador de canales comenzarán a ser inexactos porque no podrán ver la mayoría de los canales. No te fijes sólo en el número de nodos. El recuento de nodos crecerá, pero no será rastreable.

# Comunidad

Una cierta comunidad en línea que permanecerá sin nombre y tiene tres letras... decidió que yo era el CEO de la red de lightning. Pero no, hay otras implementaciones y somos una comunidad de código abierto. Todos somos CEO de la red relámpago, excepto Craig Wright. Por favor, revisa CryptoGraffiti. Él hace un gran botín.

# Conclusión

Ha sido realmente un año increíble hasta ahora. Alguien tuiteó esto en enero - en diciembre de 1969, sólo había unos pocos nodos de Internet. Desde entonces, mucho ha cambiado en el mundo. Creo que es lo mismo para bitcoin y lightning. Esto es el comienzo y no puedo esperar a ver lo que pasa después. Muchas gracias.

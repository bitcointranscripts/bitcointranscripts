---
title: Seminario Socrático 5
date: 2020-01-21
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - lightning
---
<https://www.meetup.com/Austin-Bitcoin-Developers/events/267941700/>

<https://bitdevs.org/2019-12-03-socratic-seminar-99>

<https://bitdevs.org/2020-01-09-socratic-seminar-100>

<https://twitter.com/kanzure/status/1219817063948148737>

# LSATs

Así que solemos empezar con una demostración de un proyecto basado en un rayo en el que ha estado trabajando durante unos meses.

Esta no es una idea original para mí. Fue presentada por roasbeef, cofundador de Lightning Labs en la conferencia Lightning del pasado octubre. Trabajé en un proyecto que hacía algo similar. Cuando presentó esto como una especificación más formalizada, tuvo mucho sentido basado en lo que yo estaba trabajando. Así que acabo de terminar una versión inicial de una herramienta que pone esto en práctica y permite a la gente construir sobre esto. Voy a dar un breve resumen de lo que puede hacer con esto.

Un resumen rápido. Voy a hablar de las claves de la API y el estado de la autenticación hoy en día. A continuación, lo que son los macarrones, que son una gran parte de cómo funcionan las LSATs.

LSAT es un token de autentificación del servicio lightning..

Luego hablaremos de casos de uso y de algunas herramientas como lsat-js y otra. Esperemos que puedas usarlas. Gran parte del contenido aquí, se puede ver la presentación original que Laolu (roasbeef) dio y puso juntos. Algunos de los contenidos están inspirados en esa presentación.

Estado de la autenticación hoy en día: Cualquiera que esté en Internet debería estar familiarizado con nuestros problemas de autenticación. Si estás haciendo login y autenticación, probablemente estás haciendo contraseñas de correo electrónico o OAUTH o algo así. Es asqueroso. También puedes tener claves de API más generales. Si creas una cuenta de AWS o si quieres usar una API de Twilio, entonces obtienes una clave y esa clave va en la solicitud para mostrar que estás autenticado.

Las claves API no tienen realmente ninguna resistencia sibilina incorporada. Si obtienes una clave API, entonces puedes usarla en cualquier lugar, dependiendo de las restricciones del lado del servicio. Añaden restricciones sibilinas al tener que iniciar sesión a través del correo electrónico o algo así. La clave en sí no tiene resistencia sibilina, es sólo una cadena de letras y números y eso es todo.

Las claves de API y las cookies también -que era una forma inicial de lo que son los macarrones- no tienen la capacidad de delegar. Si tienes una clave de API y quieres compartir esa clave de API y compartir tu acceso con alguien, ellos tienen acceso completo a lo que esa clave de API proporciona. Algunos servicios te darán una clave de API de sólo lectura, una clave de API de lectura-escritura, una clave de API de nivel de administrador, etc. Es posible, pero tiene algunos problemas y no es tan flexible como podría ser.

La idea de iniciar sesión y obtener tokens de autenticación es engorrosa. La tarjeta de crédito, el correo electrónico, la dirección postal... todo esto no es tan bueno cuando sólo se quiere leer un artículo del WSJ o del NYT. ¿Por qué tenemos que dar toda esta información sólo para tener acceso?

Así que alguien puede estar utilizando algo que parece las formas correctas ... como HTTPS, la commnication está encriptada, eso es genial .. Pero una vez que les das información privada, no tienes forma de auditar cómo almacenan esa información privada. Vemos grandes hacks en grandes almacenes y sitios web que filtran información privada. Un atacante sólo necesita atacar el sistema más débil que contenga tu información personal privada. Este es el origen del problema. Que Ashley Madison se entere de tu aventura no es un gran problema, pero que alguien piratee y exponga esa información es realmente malo.

Recomiendo encarecidamente leer sobre los macarrones. La idea básica es que los macarrones son como las cookies, para cualquiera que trabaje con ellas en el desarrollo web. Codifican cierta información que comparte con el servidor, como los niveles de autenticación y los tiempos de espera y cosas por el estilo, al siguiente nivel. lnd habla mucho de macaroons, pero esto no es algo específico de lnd. lnd simplemente utiliza esto, para la autenticación delegada a lnd. Ellos están usando macarrones, estas herramientas están usando macarrones. Están utilizando macarrones en su servicio de bucle de una manera totalmente diferente a su servicio de bucle. Estas podrían ser usadas en lugar de las cookies, es triste que casi nadie las esté usando.

Funciona en base a HMACs encadenados. Cuando creas un macarrón, tienes una clave de firma secreta, igual que cuando haces cookies. Firmas y te comprometes con una versión de un macarrón. Esto se relaciona con la delegación... puedes añadir lo que se llama advertencias y firmar usando una firma anterior y eso bloquea la nueva advertencia. Nadie que reciba la nueva versión del macarrón con una advertencia que ha sido firmada con una firma anterior, puede cambiarla. Es como una cadena de bloques. Simplemente no se puede revertir. Es muy chulo.

El transporte de pruebas cambia la arquitectura en torno a la autenticación. Estás poniendo la autorización en el propio macarrón. Así que estás diciendo qué permisos tiene alguien que tiene este macarrón, en lugar de poner un montón de lógica en el servidor. Así que si presentas este macarrón y es verificado por el servidor para ciertos niveles de acceso, entonces esto simplifica la autenticación y la autorización del backend mucho más. Desacopla la lógica de la autorización.

lsat es para los tokens de autentificación del servicio lightning. Esto podría ser útil para la facturación de pago por uso (no más suscripciones), no se requiere información personal, es comerciable (con la ayuda de un proveedor de servicios) - esto es algo que roasbeef ha propuesto. Puedes hacer que sea comerciable; a menos que lo hagas en una cadena de bloques, necesitas un servidor central que lo facilite. También está la autenticación de máquina a máquina. Debido a la resistencia sibilina incorporada que no está ligada a la identidad, puedes tener máquinas que paguen por el acceso a otras cosas sin tener tu número de tarjeta de crédito en el dispositivo. También puedes atenuar los privilegios. Puedes vender privilegios.

Voy a introducir algunos conceptos clave para hablar de cómo funciona esto. Hay códigos de estado - cualquiera que haya navegado por la web está familiarizado con el HTTP 404 que es para el recurso no encontrado. Hay un montón de estos números. HTTP 402 se supone que es para "pago requerido" y les tomó décadas para hacer esto a nivel de protocolo sin un dinero nativo de Internet. Así que LSAT aprovechará esto y utilizará HTTP 402 para enviar mensajes a través del cable.

Hay mucha información en las cabeceras HTTP que describen las peticiones y las respuestas. Aquí es donde vamos a establecer la información para LSAT. En la respuesta, tendrá un desafío emitido por un servidor cuando hay un pago HTTP 402 requerido. Esta es una cabecera WWW-Authenticate. También hay otro Authorized-request: autorización. La única cosa única es cómo vas a leer los valores asociados a estas claves de cabecera HTTP. Después de obtener el reto, envías una autorización que satisface ese reto.

Usted paga una solicitud de factura relámpago utilizando un determinado BOLT. Esto se pone en el desafío WWW-Authenticate. La preimagen es una cadena aleatoria de 32 bytes que se genera y forma parte de cada pago relámpago, pero se oculta hasta que el pago ha sido satisfecho. Así es como se puede confiar en los pagos de segunda capa de forma instantánea. Luego hay un hash de pago. Cualquier persona que haya recibido una factura de pago tiene este hash de pago. La preimagen se revela después de pagar. Esto básicamente, el hash de pago generado a partir del hashing de la preimagen... lo que significa que no puedes adivinar la preimagen, a partir del hash de pago. Pero una vez que tienes la preimagen, puedes probar que sólo esa preimagen pudo generar ese hash de pago. Esto es importante para la validación del LSAT.

Digamos que el cliente quiere acceder a algún contenido protegido. Digamos que el servidor entonces dice... que no hay autenticación asociada a esta petición. Voy a hornear un macarrón, y va a tener información que indicará lo que se requiere para el acceso. Esto va a incluir la generación de una factura de pago relámpago. Entonces enviamos un reto WWW-Autenticado de vuelta. Una vez que se paga una factura, se obtiene una preimagen a cambio, que se necesita para satisfacer el LSAT porque cuando se envía el token de vuelta es el macarrón y luego dos puntos y luego esa preimagen. Porque lo que sucede es que la información de la factura, el hash del pago está incrustado en el macarrón. Así que el servidor busca el hash de pago, y la preimagen, y luego comprueba H(preimagen) == hash de pago boom está hecho.

Dependiendo de las limitaciones que quieras poner en el muro de pago, se trata de una verificación de estado. Sabes que la persona que tiene esa preimagen tuvo que haber pagado la factura asociada a ese hash. El hash está en el token del macarrón.

Esto ayuda a desvincular el pago de la autorización. El servidor podría saber que el pago fue satisfecho usando lnd o algo así, pero esto ayuda a desacoplarlo. También ayuda a otros servicios a comprobar la autorización.

La versión actual de LSATs tiene un identificador de versión en los macarrones que genera. La forma en que el equipo de Lightning Labs ha hecho es que tienen un número de versión y se incrementará como la funcionalidad se añade a ella.

En mi herramienta, tenemos configuraciones de pre-construcción para añadir vencimientos. Así que puedes obtener 1 segundo de acceso por cada satoshi pagado, o algo así. Los niveles de servicio es algo en lo que el equipo de Loop ha estado trabajando.

La firma se hace en el momento de la cocción del macarrón. Así que tienes una clave secreta, se asigna un macarrón, y la firma se pasa con el macarrón.

Esto permite que las facturas de máquina a máquina sean resistentes a los sibilinos. Las facturas HODL son algo que he implementado. Las facturas HODL son básicamente una forma de pagar una factura sin que se liquide inmediatamente. Es un servicio de custodia construido con lightning, pero crea algunos problemas en la red de lightning. Hay formas de utilizarlas que no entorpecen la red, siempre que no se utilicen durante largos periodos de tiempo. Yo usaba esto para los tokens de un solo uso. Si tratas de acceder a ellos, y una factura está siendo retenida pero no liquidada, entonces tan pronto como se liquida entonces ya no es válida.  También hay una manera de dividir los pagos y pagar una sola factura, pero entonces tienes algunos problemas de coordinación. Creo que esto es similar a la liberación del pararrayos que hizo Reese, que era para los pagos fuera de línea. Tienen un servicio en el que puedes hacer pagos de terceros sin confianza.

Hice lsat-js que es una biblioteca del lado del cliente para interactuar con los servicios de LSAT. Si tienes una aplicación web que tiene esto implementado, entonces puedes decodificarlos, obtener el hash de pago, ver si hay algún vencimiento en ellos. Luego está BOLTWALL donde añades una sola línea a un servidor, y lo pones alrededor de una ruta para la que quieres requerir el pago, entonces BOLTWALL lo coge cuando recibes una petición. Es sólo un middleware nodejs, por lo que podría funcionar con balanceadores de carga.

NOW-BOLTWALL es un marco sin servidor para desplegar sitios web y funciones normales sin servidor; esta es una herramienta CLI que lo configurará. La forma más fácil de hacerlo es btcpay y usar el despliegue con luna node por $8/mes, y luego puedes configurar NOW-BOLTWALL. Luego usando zyke que tienen un nivel gratuito, puedes desplegar un servidor por ahí y ellos mismos están ejecutando balanceadores de carga. Puedes pasarle una url que quieras protocolizar. Así que si usted tiene un servidor en otro lugar, sólo puede desplegar esto en la línea de comandos.

Y luego está lsat-playground, que voy a demostrar rápidamente. Esto es sólo la UX que puse juntos.

LSAT sería útil para un proveedor de servicios que aloja blogs de diferentes autores, y el autor puede estar convencido de que el usuario pagó y obtuvo acceso al contenido - y que el usuario pagó específicamente ese autor, no el proveedor de servicios.

Pondré algunas diapositivas en la página de la reunión.

# Seminario socrático

Esto va a ser un repaso rápido de las cosas que están sucediendo en el desarrollo de bitcoin. Yo facilitaré esto y hablaré de los temas, y sacaré algo de conocimiento de la audiencia. Sólo entiendo como el 10% de esto, y algunos de ustedes entienden mucho más. Así que interrúmpeme y salta, pero no des un discurso.

Nos perdimos un mes porque tuvimos el taller de taproot el mes pasado. BitDevsNYC es un meetup en NYC que publica estas listas de enlaces sobre lo que pasó ese mes. He leído algunos de ellos.

## OP\_CHECKTEMPLATEVERIFY

<https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-November/017494.html>

Este es el trabajo de Jeremy Rubin. La idea es que es una propuesta de pacto para bitcoin. La idea es que el UTXO sólo puede... ((bryan tomó esta)). Este taller va a ser a finales de mes. Dice que va a patrocinar a la gente, así que si estás en esto entonces considéralo. Debido a que puede ser auto-referencial, puedes tener una completitud de turing accidental. La versión inicial tenía este problema. También podría ser utilizado por los intercambios en las transacciones de retiro para prevenir o lista negra de sus futuras transacciones.

## Atalaya BOLT

Es bastante interesante. Estuve en Londres y me reuní con estos tipos. Tienen una implementación completa de esto en python. Era agradable y simple, no estoy seguro si es de código abierto todavía. Hay como tres implementaciones de watchtower ahora, y deben ser estandarizadas.

## Estafa de PlusToken

ErgoBTC hizo algunas investigaciones sobre la estafa PlusToken. Fue una estafa en China que obtuvo como 200.000 BTC. La gente que la dirigía no era sofisticada. Así que trataron de hacer alguna mezcla... pero barajaron sus monedas de mala manera. Los atraparon. Algún whitehat lo descubrió y fue capaz de rastrear dónde salían los fondos de un intercambio y demás. Aquí hay un hilo de Twitter que habla de cómo el movimiento de estos BTC podría haber afectado al precio. Hace un mes, algunos de los chicos fueron atrapados. La teoría de este tipo es que detuvieron a los subordinados, y el que tenía las llaves no fue detenido. Así que la mezcla continuó, claramente este otro tipo tiene las llaves. También tenían un montón de ETH y fue movido como hace un mes, y el mercado se asustó- el precio de ETH cayó. Así que tal vez tomó una gran posición corta, y luego movió las monedas, en lugar de vender. 200.000 BTC es mucho, realmente se puede mover el precio con esto.

PlusToken estafó 1.900 millones de dólares en todas las monedas, con una página de aterrizaje. Tenían gente en las calles yendo a estos chinos diciendo que compraran bitcoin y lo multiplicaran, es esta nueva cosa de la minería. MtGox era como 500.000 BTC, que era el 7% de la oferta en circulación en el momento. Así que esto podría ser el 2-3% de la oferta.

El tipo también apareció en un podcast donde habló de las herramientas que utilizó para averiguar esto. Este es un tema interesante. Los coinjoins van a ser un tema en muchos de estos. Esta es sólo una cara de coinjoin.  Obviamente, el coinjoin que estaba usando era imperfecto.

## txstats.com

Este es un visualizador de estadísticas de transacciones de la investigación de BitMex.

Aquí está Murch informando sobre un poco de dumping de intercambio. Él hace el desarrollo de la cartera para bitgo. A menudo habla de cosas de consolidación de UTXO. Alguien volcó 4 MB de transacciones a 1 sat/vbyte. Alguien estaba consolidando un montón de polvo cuando las tarifas eran realmente baratas.

Aquí hay un sitio de datos de rayos. Pierre tenía el nodo número uno. Tiene capacidad, diferentes tipos de canal se cierra. BitMex escribió un artículo informando sobre los cierres no cooperativos, porque puedes ver las operaciones de cierre forzado en el blockchain.

Jameson Lopp tiene algunas comparaciones de implementación de bitcoin. Esto es un análogo. Se trata de las diferentes versiones de Bitcoin Core como la v0.8 y siguientes. A continuación, analiza cuánto tiempo tarda la descarga del bloque inicial, para el blockchain actual.  Hay otro para el tiempo que tarda en sincronizarse con el blockchain en la fecha en que fue lanzado. Hubo una gran caída cuando cambiaron de openssl a libsecp256k1. Entonces era enormemente más performante.

## Atajos inseguros en MuSig

Se trata de parte de la interactividad en Schnorr MuSig. Hay tres rondas en este protocolo. En este artículo, él está discutiendo todas las maneras que usted puede estropear con él. MuSig es bastante complejo y hay un montón de armas de pie, que es el resumen aquí supongo.

## ZenGo firma umbral basada en el tiempo

Multisig en el concepto es conseguir algunas entidades diferentes, donde se puede hacer en la cadena multisig o fuera de la cadena multisig donde se agregan las firmas juntos y se unen. Estos chicos tienen algo así, pero las claves rotan con el tiempo. Puedes tener un escenario en el que todas las partes pierden una clave durante un año determinado, pero como las claves son rotativas, ninguna de ellas pierde una cantidad mínima por encima de una determinada cantidad. Así que el monedero seguiría conservándose aunque todas las personas hayan perdido sus claves. Esto se llama "compartir el secreto proactivamente". Parece que sería más práctico hacer 3-de-5 y simplemente configurar un nuevo 3-de-5 cuando 1-de-5 lo pierde. A Binance le gusta esto porque es la compatibilidad de shitcoin que les gusta. Ledger también.

## Ataque a la tarjeta fría

La forma en que este ataque funciona es que puedes engañarlo para que genere una dirección de cambio en algo como esto... una ruta de derivación en la que tomas el hijo número 44, 0 endurecido, y luego el último es un número enorme. Entonces lo pones en una hoja muy al borde de la clave privada, de tal manera que sería difícil encontrarla de nuevo si la buscas. Técnicamente sigues siendo dueño de las monedas, pero sería difícil gastarlas. Así que era un exploit inteligente. Básicamente, un atacante puede convencer a tu tarjeta fría de que está siendo enviada a "tu" dirección, pero en realidad es una ruta bip32 aleatoria o algo así. Ningún monedero de hardware actualmente rastrea las direcciones de cambio que dan. Así que la idea es restringirlo a alguna brecha de búsqueda... no ir más allá de la brecha o algo así. O podría estar en un sitio web generando un montón de direcciones, por adelantado, para los usuarios o los pagos o algo así. También había algo sobre 32 bits + 1 o algo así, más allá del valor MAX.

## Error de Trezor

Trezor tenía un error en el que si tenías una... si estabas tratando de hacer una salida single-sig, y luego tenías una entrada multi-sig y luego un cambio multi-sig, podías inyectar tu propia dirección de cambio multisig o algo así. Tu máquina anfitriona podría hacer esto. Esto fue como hace un mes o un mes y medio. No muestran el cambio, si es que lo tienes. En este escenario, la dirección de cambio de multisig es algo que no posees, y debería tratar eso como un gasto doble o algo así. Esto era un exploit remoto. Trató la dirección multisig de otra persona como tu dirección. Simplemente no se incluyó en el cálculo de la tarifa o algo así.

## Hilo de Monero

Alguien tiene un hash malo en su software. Así que es una historia de detectives tratando de averiguar lo que salió mal, como si el sitio web es malo o algo así. Resulta que el binario era malicioso. Puedes ver el trabajo de detective en tiempo real. Alguien fue capaz de conseguir el binario y hacer algunos análisis. Se añadieron dos funciones; una de ellas enviaría su semilla al atacante. Así que si ejecutas este binario y tienes algún monero, entonces el atacante ahora tiene ese monero. Es bastante fascinante. El binario llegó al sitio web de Monero. Eso es bastante aterrador. Este es un buen ejemplo de por qué necesitas comprobar las firmas y los hashes cuando descargas una cartera. Monero estaba sirviendo esto a la gente que estaba descargando el software. Era getmonero.org que estaba sirviendo el malware. Es interesante que tuvieran acceso al sitio, y no actualizaran los hashes md5 o algo así. Bueno, tal vez pensaron que los usuarios comprobarían el sitio web y no el binario que realmente descargaron.

## Detenciones de intercambiadores de SIM

Esto era sólo un artículo de noticias. El SIM swapping es cuando entras en una tienda de Verizon y dices que tienes un número, y entonces ponen tu número de teléfono en tu teléfono y entonces puedes robar el bitcoin de alguien o lo que sea. Utilizan las preguntas habituales como cuál es tu nombre de soltera y otra información pública.

## Ataque de Vertcoin 51%

Esto ha sucedido ya dos veces. Tuvimos una discusión cuando esto ocurrió hace seis meses. De alguna manera esta moneda sobrevive a los ataques del 51%. ¿Por qué sobreviven? Tal vez es tan especulativo que la gente se encoge de hombros. ¿Qué pasa con el bitcoin o el ethereum que son atacados en un 51%? Así que tal vez todo es comercio especulativo, o los usuarios son demasiado estúpidos o algo así.

## El papel del enrutamiento del diente de león en "romper el modelo de privacidad de mimblewimble"

## Bitcoin Core 0.19.1

Hubo algún tipo de problema justo después de la v0.19.0, y luego salió la v0.19.1. Hay algunos nuevos comandos RPC. getbalance es mucho mejor. Un montón de correcciones RPC. Eso es genial, así que descárgalo.

## Eliminar OpenSSL

OpenSSL fue eliminado por completo. Comenzó en 2012. Mucho de esto aceleró la descarga inicial de bloques. Lo curioso es que a gavinandresen no le gustaba la idea. Pero se convirtió en una gran mejora. Se tardó unos años en eliminar completamente OpenSSL, porque estaba suministrando todas las primitivas criptográficas para firmas, hashing, claves. Se tardó 10 años en eliminar openssl. Lo último que lo necesitaba era bip70. Lo necesitaban para algo.

## Selección de monedas por rama y por límite

Es una mejor manera de hacer la selección de monedas al componer las transacciones. Quiere optimizar las comisiones a largo plazo. Así que escribió su tesis para demostrar que esta sería una buena forma de hacerlo. Murch también señaló que la selección aleatoria de monedas era realmente mejor que la solución de aproximación estocástica.

## joostjager - enrutamiento permitir ruta ...

Puedes pagar a alguien incluyéndolo en una ruta, sin que tenga que darte una factura. Alex Bosworth creó una biblioteca para hacer esto. Tienes que estar directamente conectado a ellos; así que puedes dirigirte a ti mismo a una persona con la que estés conectado.

## Último salto opcional a los pagos

Así que aquí puedes decir, puedes definir una ruta diciendo quiero pagar a esta persona y el último salto tiene que ser del punto n-1 al n. Así que si por alguna razón quieres, como si no confiaras en alguien... Entonces quería pagarle, pero quería elegir quién era el último salto. Aunque no sé por qué querrías hacer eso.

## lnrpc y otros comandos rpc para lnd

## joinmarket-clientserver 0.6.0

¿Alguien usa realmente joinmarket? Si lo hiciera, no te lo diría. ¿Qué?

Hay mucho trabajo en joinmarket. Hay muchos cambios allí. Lo que realmente mola de joinmarket- nunca lo he usado- parece que ofrece la promesa de tener una cartera caliente pasiva sentada ahí ganando un rendimiento de tu bitcoin. Joinmarket tiene tasas de fabricante y tomador. Me alegro de que la gente esté trabajando en esto.

## Reunión de la organización de estándares de carteras

Esta fue una transcripción que Bryan hizo de una reunión anterior de desarrolladores de Austin Bitcoin.

## Lightning en el móvil: Neutrino en la palma de la mano

Mostró cómo crear una aplicación react-nativa que pudiera hacer de neutrino. Quiere que un usuario móvil no custodio y participante de pleno derecho sea un participante de pleno derecho en la red sin descargar 200 GB de cosas. Creo que la principal innovación no es neutrino, sino que en lugar de tener que escribir a medida para construir el binario de lnd para el móvil, es un SDK en el que sólo tienes que escribir "importar lnd" y eso es todo lo que necesitas para ir.

## Nueva lista de correo para el desarrollo de lnd que roasbeef anunció

Probablemente relacionada con la migración de la Fundación Linux...

## Derivados de Hashrate

Jeremy Rubin tiene otro proyecto que es una plataforma de derivados de hashrate. La idea es que puedes bloquear las transacciones en minutos o en bloques, y el que llegue más rápido se lleva el pago. Es una forma interesante de implementar un derivado. Es básicamente DeFi. Así que probablemente podrías jugar con esto si tuvieras alguna capacidad de minería de bitcoins. En un mes... Uh, bueno el mercado le pondrá precio. Ese es un buen punto.

## Nuevo protocolo stratum para pools de minería (stratum v2)

Aquí se habla de marketing sobre stratum v2.

Lo más interesante es este hilo de reddit. La gente de slushpool está en este hilo con petertodd y bluematt. Algunos de los beneficios son que te ayudará a operar en conexiones de internet menos que ideales. Obtienes bloques y cosas más rápido creo. Una de las cosas interesantes que señaló bluematt es que si estás minando no estás seguro si tu ISP está robando parte de tu hashrate porque no hay autenticación entre tú y el pool y los mineros.

El protocolo ahora enviará plantillas de bloques por adelantado. Entonces, cuando se observan nuevos bloques, sólo enviarán el campo previoushash. Tratan de cargar la plantilla de bloques antes de tiempo, y luego envían 64 bytes para rellenar la cosa para que puedas empezar a minar inmediatamente. Es una optimización interesante. Es un hilo genial si quieres aprender más sobre la minería.

## lnurl

Esta es otra forma de codificar las facturas HTTP en las cadenas de consulta HTTP.

## BOLT-android

## Algunos hackathons de LN

## Retiros de LN en Bitfinex

## Análisis del bug bech32

Un solo error tipográfico puede acarrear muchos problemas. Una de las cosas interesantes es que cambiando una constante en la implementación de bech32 se arregla el problema. ¿Cómo encontró ese tipo ese error? ¿No estaba Blockstream haciendo pruebas fuzz para prevenir esto? Millones de dólares de presupuesto en pruebas fuzz.

## Coinjoins desiguales

Un tipo se retiró de Binance y se retiró y luego hizo coinjoins en Wasabi. Binance lo prohibió. Así que en el mundo de los coinjoins, hay una discusión sobre cómo lidiar con eso. El hecho de que los coinjoins son muy reconocibles. Si sacas dinero de un intercambio y haces un coinjoin, el intercambio lo va a saber. Entonces, ¿qué hay de hacer coinjoins con valores no iguales? Ahora mismo los coinjoins utilizan valores iguales, lo que los hace muy reconocibles. Sólo tienes que buscar estas transacciones no naturales y ya está. Pero, ¿qué pasa con hacer coinjoins con cantidades no iguales para que pueda parecer una transacción de intercambio por lotes o hacer pagos a los usuarios? Los coinjoiners están siendo discriminados. La persona a la que le han dado un tirón de orejas estaba retirando directamente en un coinjoin. No me malinterpretes, no les gustan los coinjoins, pero tampoco seas estúpido. No envíes directamente a un coinjoin. Al mismo tiempo, muestra una debilidad de este enfoque.

Wasabi organizó un club de investigación. Justo después de la cuestión de coinjoin-binance, una semana después Wasabi estaba haciendo algunas cosas alojadas en youtube para desenterrar viejas investigaciones sobre coinjoin de cantidades desiguales. Este es un tema interesante. Alguien tiene una implementación de referencia en rust, y el código es muy legible. Hay una discusión de una hora y media en la que Adam lo interroga. Es bastante bueno. Encontró un error en uno de los documentos... nunca pudo conseguir que su implementación funcionara, y entonces se dio cuenta de que había un error en la especificación del documento, lo arregló y consiguió que funcionara.

## Minería fusionada a ciegas con pactos y OP\_CTV

Esto es básicamente de lo que hablaba Paul Sztorc cuando nos visitó hace unos meses. Se trata de tener otra cadena asegurada por bitcoin de la que bitcoin no sería consciente, y habría algún token involucrado. La propuesta de Rubén es interesante porque se trata de minería ciega fusionada, que es lo que necesita Paul para sus cosas de truthcoin. Así que se consigue otra cosa gratis si conseguimos OP\_CTV.

Un argumento que algunas personas hacen para cualquier nueva característica en bitcoin es que no sabemos qué más podríamos ser capaces de llegar, para usar esto. Como la versión original OP\_SECURETHEBAG con la que resultó que se puede hacer turing completo. Tal vez es un caso de uso que queremos; pero mucha gente piensa que la minería fusionada a ciegas no es lo que queremos - no recuerdo por qué. Se ha pensado mucho en si los soft-forks deberían entrar.

## ZmnSCPxj en la privacidad del camino

No estoy muy seguro de cómo pronunciar su nombre. ¿Zeeman? Es ZmnSCPxj. Puedes deducir mucha información sobre lo que pasó en la ruta de pagos. La primera parte del correo electrónico es como se puede utilizar esto para averiguar cosas. Así que habla de una vigilancia maligna en un nodo a lo largo de la ruta, pero si lo que si son dos nodos alrededor de la ruta. Puedes desarrollar tablas de enrutamiento inverso si tienes suficiente influencia en la red. Entra a hablar de algunas de las cosas que sucederán con Schnorr, como la descorrelación de la ruta y demás.

## ZmnSCPxj en taproot y lightning

Esto es una locura. Esta fue una buena.

## Boletines de Bitcoin Optech

c-lightning pasó de estar por defecto en testnet a estar por defecto en mainnet. Han añadido soporte para los secretos de pago. Puedes hacer esta cosa, el sondeo, donde tratas de enrutar pagos falsos a través de un nodo y tratar de evaluar y averiguar lo que puede hacer. Puedes generar preimágenes aleatorias y luego crear un hash de pago a partir de esa preimagen aunque sea inválida. Supongo que esto es una mitigación para eso.

Aquí hay un hilo sobre lo que las torres de vigilancia tienen que almacenar, en eltoo. Una de las ventajas de eltoo es que no tiene que almacenar el historial completo del canal, sólo la actualización más reciente. Entonces, ¿tienen que almacenar la última actualización, o también la transacción de liquidación? ¿Algún comentario al respecto? La verdad es que no conozco demasiado bien elto como para especular sobre eso.

c-lightning agregó métodos RPC de createonion y spendonion para permitir mensajes LN encriptados que el nodo mismo no tiene que entender. Esto permite que los plugins usen la red de rayos de forma más arbitraria para enviar mensajes de algún tipo, y son mensajes encriptados por Tor.

whatsat es una aplicación de texto/chat. Están tratando de conseguir la misma funcionalidad sobre c-lightning.

Las tres implementaciones de LN tienen ahora pagos de rutas múltiples. Esto te permite... digamos que tienes un bitcoin en tres canales diferentes. Aunque tengas 3 BTC, sólo puedes enviar 1 BTC. Multipath te permite enviar tres misiles al mismo objetivo. lnd, eclair y c-lightning soportan esto ahora en algún estado. ¿Se puede usar esto en mainnet? ¿Debería hacerlo? La implementación de lnd lo tiene en el código, pero sólo permiten especificar una ruta de todos modos. Así que en realidad no lo han probado en algo que la gente pueda ejecutar enviando múltiples rutas, pero el código ha sido refactorizado para permitirlo.

Andrew Chow dio una buena respuesta sobre la profundidad máxima de bip32, que es de 256.

Bitcoin Core añadió una arquitectura powerpc.

Ahora hay una lista blanca de rpc. Si tienes credenciales para hacer RPC con un nodo, puedes hacer básicamente cualquier cosa. Pero este comando te permite poner en la lista blanca ciertos comandos. Digamos que quieres que tu nodo lightning no añada nuevos peers en el nivel p2p, lo que te permitiría ser atacado por eclipse. Lightning sólo debe ser capaz de hacer consultas de monitoreo de blockchain. Nicolas Dorier dice que mi explorador de bloques sólo se basa en sendrawtransaction para la difusión. Así que usted quiere a la lista blanca, esto es por credencial de usuario. ¿Tienen múltiples credenciales de usuario para bitcoin.conf?

Esta es la razón por la que lnd utiliza macarrones. Resuelve este problema. No necesitas tener una lista de personas en el archivo de configuración, puedes simplemente tener personas que tengan macarrones que les den ese acceso.

Aquí está lo que Bryan estaba hablando, que es la revisión de fin de año. Te animo a que leas esto, si vas a leer sólo una cosa es el boletín de revisión de fin de año 2019 de Bitcoin Optech. Cada mes del año pasado ha habido alguna gran innovación. Es realmente una locura leer esto. Erlay es realmente grande también, como una reducción del 80% del ancho de banda.

Gleb Naumenk dio una bonita charla en London Bitcoin Devs sobre erlay. Habló de cosas de la red p2p. Te animo a comprobarlo si estás interesado.

El lenguaje descriptor de scripts es como una versión mejor de las direcciones para describir un rango de direcciones. Se parecen a un código con paréntesis y demás. Chris Belcher ha propuesto codificarlo en base64, porque ahora mismo si intentas copiar un descriptor de script por defecto no se resalta. Esto hace que los descriptores de script sean más ergonómicos para la gente que no sabe lo que significan.

## Herramienta LN de BitMex

Esta es una herramienta de BitMex que es un sistema de alerta en vivo para los canales. Este era el monitor de horquillas de BitMex.

## Caravana

La caravana de Unchained recibió un saludo.

## Transacciones anónimas de coinjoin con

Este es un documento que wasabi desenterrado de hace como 2 años.

## Luke-jr's full node chart

El script para producir esto es de código cerrado, por lo que no se puede jugar con él. Pero hay múltiples implementaciones por ahí. Yo sospechaba de esto porque luke-jr está un poco loco, pero gleb parece pensar que es correcto. Estamos en el mismo número de nodos completos que a mediados de 2017. Así que eso es interesante. La línea superior es el número total de nodos completos, y la línea inferior es el número de nodos de escucha que te responderán si intentas iniciar una conexión con ellos. Probablemente quieras ser inalcanzable por razones egoístas, pero necesitas estar localizable para ayudar a la gente a sincronizarse con el blockchain. Mediados de 2017 podría ser el pico de segwit cuando la gente estaba girando nodos, o podría estar relacionado con el precio del mercado.  También hubo un pico de precios en junio. Tal vez algunos de estos son para los nodos de relámpago. Apuesto a que mucha gente ya no lo hace.

## El tablero de Clark Moody

El dashboard de Moody tiene un montón de estadísticas en tiempo real que puedes ver actualizadas en tiempo real.

## Revisión de fin de año de Bitcoin Magazine

Tuvimos un crecimiento del 10% en el número de commits, un aumento del precio del 85%, el dominio de bitcoin subió un 15%, nuestra tasa de inflación es del 3,8%. El volumen diario subió. Segwit pasó del 32% al 62%. El valor de las transacciones diarias subió. El tamaño de la cadena de bloques creció un 29%. El recuento de nodos de Bitcoin se desplomó, bajó, lo que no es tan bueno. Puede ser porque mucha gente tenía sólo discos duros de 256 GB, tal vez por eso se retiraron... sí, ¿pero podar?

## arxiv: nueva construcción del canal manuscrito

## Lista de ataques a carteras de hardware (de Shift Crypto)

Es una lista bastante interesante. Esta es la razón por la que haces multisig de múltiples vendedores, tal vez. Esto es bastante aterrador.

## Las trampas de multisig cuando se usan carteras de hardware

Una de las ideas que la gente no se da cuenta es que si usas multisig y pierdes los redeemSripts o la capacidad de computarlos, pierdes la capacidad de multisig. Necesitas hacer una copia de seguridad de algo más que tu semilla si estás haciendo multisig. Necesita hacer una copia de seguridad de redeemScripts. Algunos proveedores intentan mostrar todo en la pantalla, y otros infieren cosas. Los fabricantes no quieren tener un estado, pero el multisig requiere que mantengas un estado como el de no cambiar a otros participantes del multisig o el de intercambiar información por debajo de ti. Si estás pensando en implementar multisig, mira el artículo

## charla de bunnie sobre hardware seguro

El gran punto de esta charla fue: no se puede hacer hash del hardware. Puedes hacer hash de un programa de ordenador y comprobarlo, pero no puedes hacerlo con el hardware. Así que, básicamente, tener hardware de código abierto no lo hace más seguro necesariamente. Él va a través de este gran todas las ramificaciones de que y lo que puede hacer. Él tiene un dispositivo, un teléfono de mensajes de texto que es tan seguro como él puede hacerlo, y lo interesante es que usted podría convertirlo en un hardware.

## Conferencia y charlas de la CCC

## SHA-1 colisión

Por 70k dólares fueron capaces de crear dos claves PGP, usando la versión heredada de PGP que usa sha-1 para el hash, y fueron capaces de crear dos claves que tenían diferentes ids de usuario con certificados que colisionaban.

## Pruebas de falsificación de Bitcoin Core

Hay una página de estadísticas de fuzz testing, y luego un grupo de revisión de Bitcoin Core PR.

## lncli + facturas - modo de envío experimental de llaves

Es sólo una manera de enviar a alguien, puede enviar a otra factura. Tuvieron esta función como un año y finalmente se fusionó.






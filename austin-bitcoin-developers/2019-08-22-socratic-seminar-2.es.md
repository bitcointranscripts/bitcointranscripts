---
title: Seminario Socrático 2
date: 2019-08-22
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - research
  - hardware-wallet
---
<https://twitter.com/kanzure/status/1164710800910692353>

# Introducción

Hola. La idea era hacer una reunión de estilo más socrático. Esto fue popularizado por Bitdevs NYC y se extendió a SF. Lo intentamos hace unos meses con Jay. La idea es que recorremos las noticias de investigación, los boletines, los podcasters, hablamos de lo que ha pasado en la comunidad técnica de bitcoin. Vamos a tener diferentes presentadores.

Mike Schmidt hablará de algunos boletines de optech a los que ha contribuido. Dhruv hablará sobre el intercambio de secretos Hermit y Shamir. Flaxman nos enseñará cómo configurar una cartera de hardware multisig con Electrum. Nos mostrará cómo se puede hacer esto y algunas de las cosas que hemos aprendido. Bryan Bishop hablará sobre su propuesta de bóvedas que se hizo recientemente. Lo ideal es que cada uno de estos temas dure unos 10 minutos. Sin embargo, es probable que se extiendan un poco. Vamos a tener un montón de participación de la audiencia y realmente interactivo.

# Boletines de Bitcoin Optech

No tengo nada preparado, pero podemos abrir algunos de estos enlaces y presentar mi perspectiva o lo que yo entiendo. Si la gente tiene ideas o preguntas, sólo tiene que hablar.

# Boletín 57: Coinjoin y joinmarket

<https://bitcoinops.org/en/newsletters/2019/07/31/>

<https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-July/017169.html>

Bonos de fidelidad para proporcionar resistencia sibilina a joinmarket. ¿Alguien ha utilizado joinmarket antes? ¿No? ¿Nadie? Buen intento... Bien. Así que, joinmarket es un monedero que está diseñado específicamente para hacer coinjoins. Un coinjoin es una manera de hacer un poco de mezcla o volteo de monedas para aumentar la privacidad o fungibilidad de sus monedas. Hay algunas opciones diferentes para ello. Esencialmente utiliza chatbots de IRC para solicitar creadores y tomadores. Así que si realmente quieres mezclar tus monedas, eres un tomador, y un creador en el otro lado pone fondos para mezclar con tus fondos. Así que hay este modelo de creador/tomador que es interesante. No lo he usado, pero parece ser facilitado por el chat IRC. El creador, la persona que pone el dinero, no necesariamente necesita privacidad, gana un pequeño porcentaje de su bitcoin. Todo se hace con contratos inteligentes, y sus monedas no corren peligro en ningún momento, salvo en la medida en que se almacenan en un monedero caliente para interactuar con el protocolo. La resistencia sibilina que están hablando aquí es que, por lo que, Chris Belcher tiene una gran entrada de privacidad en el wiki bitcoin así que echa un vistazo a eso en algún momento. Él es uno de los desarrolladores de joinmarket. Se da cuenta de que cuesta muy poco inundar la red con un montón de creadores si eres un actor malicioso, y esto rompe la privacidad porque las posibilidades de que te encuentres con una empresa maliciosa o fraudulenta del tipo chainalysis, no es que puedan tomar tus monedas, pero estarían invadiendo tu privacidad. El coste de que lo hagan es bastante bajo, por lo que las posibilidades de que lo hagan son bastante altas.

Al igual que la minería de bitcoin, se trata de una resistencia sibilina mediante la quema de energía para la prueba de trabajo. Hay dos tipos de potenciales para la prueba de trabajo en este escenario contra la resistencia sibilina. Una es que puedes quemar bitcoin, y la otra es que puedes bloquear bitcoin, ambas son pruebas de que tienes algo de piel en el juego. Así que puedes probar ambas cosas en la cadena y es una forma de asociar que has bloqueado estas monedas y las has bloqueado una vez por este nick de IRC y esto te da credibilidad para comerciar como una persona normal. Así que no puedes tener 1000 chatbots para fisgonear... Son de 30 a 80.000 BTC. Eso sería el bloqueo. Se trata de bloquear esta cantidad de BTC para ocupar una parte de la capacidad total de la situación del mercado de la unión. No sería peor que la situación actual, donde tienen la capacidad de hacerlo de todas formas, así que esto lo hace más caro. También lo hace más caro para el usuario medio, que es la parte negativa. El coste de que los fabricantes legítimos apunten o bloqueen o quemen sus monedas se va a trasladar a los tomadores. En la forma en que está configurado ahora, la cuota de la minería es sustancialmente más de lo que estos fabricantes están haciendo por hacer la fijación, por lo que la teoría de acuerdo con Chris es que la gente estaría dispuesta a tomar una cuota más alta para la mezcla, porque ya están pagando 10x para las tasas de minería. No sé cuántos coinjoins se pueden hacer en un día, pero hay listas públicas de los fabricantes y lo que van a cobrar y cuál es su capacidad. Hay gente que pone 750 BTC y puedes mezclar con ellos, y cobran un 0,0001% o algo así. El costo más alto es para la protección sibilina, es una tasa natural. Si estás pagando 10 veces más para procesar la transacción en la red bitcoin, entonces tal vez estés dispuesto a poner unos cuantos sats más para pagar por esta resistencia sibilina.

Los equipos de los monederos Samurai y Wasabi tuvieron algunas discusiones interesantes. Estuvieron hablando sobre la reutilización de direcciones y cuánto reduce realmente la privacidad. No creo que sea un tema resuelto, ambos siguen yendo y viniendo atacándose mutuamente. Para cualquiera de estos coinjoins, todos están expuestos en cierta medida a coinjoin. Así que siempre hay compensaciones. Mayor coste, algo de protección, aún no es perfecto, una empresa podría estar dispuesta a bloquear esas monedas. Una cosa interesante sobre esto es que aumenta el coste de los servicios de Chainalysis - tendrán que cobrar más a sus clientes; así que esto reduce sus márgenes y tal vez podamos sacarlos del negocio.

# Boletín de noticias 57: signmessage

<https://github.com/bitcoin/bitcoin/issues/16440>

<https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki>

Bitcoin Core tiene la capacidad de hacer signmessage, pero esta funcionalidad era sólo para single key pay-to-pubkeyhash (P2PKH). Kallewoof ha abierto un pull request que permite tener esa misma funcionalidad con otros tipos de direcciones. Así que para segwit, P2SH etc., ... Creo que es interesante, y es compatible hacia adelante con futuras versiones de segwit, por lo que taproot y Schnorr están incluidos, tendrían la capacidad de firmar las secuencias de comandos con estas claves, y es compatible hacia atrás porque tiene la misma fnuccionalidad para firmar una sola clave. Sí, podría ser utilizado para una prueba de reserva. Steven Roose hizo la salida falsa con el mensaje, esa es su herramienta de prueba de reserva. Construye una transacción inválida para hacer una prueba de reserva. Si Coinbase quisiera probar que tiene las monedas, podría crear una transacción que se parezca mucho a una transacción válida pero que sea técnicamente incorrecta, pero aún así con firmas válidas. bip322 sólo está firmando el mensaje.

Todo lo que puedes hacer con la firma es demostrar que en algún momento tuviste esa clave privada. Si alguien te roba las claves privadas, puedes seguir firmando con tu clave privada, pero ya no tienes las monedas. Tienes que demostrar que no la tienes; o que otra persona no la tiene. O que, en la altura de bloque actual, tenías los fondos. Ese es el verdadero reto de la prueba de reservas, la mayoría de las propuestas tratan de mover los fondos.

# Boletín 57: debate sobre el filtro Bloom

<https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-July/017145.html>

<https://github.com/bitcoin/bitcoin/issues/16152>

Hubo alguna consternación aquí sobre la desactivación del filtro bloom por defecto en Bitcoin Core. Ahora mismo si estás usando un monedero o cliente SPV, como Breadwallet que usa SPV... La discusión fue que en la semana anterior, hubo un pull request fusionado que deshabilita los bloom filters por defecto. Una nueva versión de Bitcoin Core ya no serviría estos filtros bloom a los clientes lite. Mi Breadwallet no podría conectarse a los nodos de Bitcoin Core y hacer esto por defecto, pero de nuevo alguien podría volver a activarlo.

Alguien argumentó que Chainalysis ya está ejecutando todos estos nodos de filtro de floración de todos modos, y continuarán recogiendo esa información. Muchos nodos de Bitcoin Core están ejecutando nodos que tienen más de un año de antigüedad, por lo que no van a ir a ninguna parte pronto. Todavía podrás ejecutar algunos clientes lite. Creo que Breadwallet ejecuta algunos nodos también. Siempre se puede ejecutar sus propios nodos también, y servir a los filtros de floración a ti mismo.

¿Alguien utiliza un monedero o es consciente de que está utilizando un monedero que es un cliente SPV lite? Electrum no hace los filtros bloom de bip37, utiliza un modelo de confianza.

¿La idea es que bip57 esté activado por defecto, para sustituirlo? ¿Va a estar Neutrino activado por defecto? Lo está para btcd. Me imagino que bitcoind tendrá algo similar. Son sólo comandos de red. Se almacena un poco más localmente, con los filtros de Neutrino. Tienes que hacer un seguimiento. Si hay un compromiso de coinbase o lo que sea, vas a tener que revisar eso también. Eso tendría que ser un soft-fork.

# Noticias de Lightning (Buck Perley)

Voy a repasar los temas lightning de la lista del seminario socrático. Ayer estuve en un avión durante unas horas, así que preparé algunas preguntas y espero que podamos suscitar algunas cuestiones en torno a ellas.

## Torres de vigilancia

<https://blog.bitmex.com/lightning-network-part-4-all-adopt-the-watchtower/>

Bitmex tenía algo sobre la ejecución de torres de vigilancia. Lo bueno de su artículo es que repasan los diferentes escenarios cuando estás ejecutando lightning y lo que hace que se cumpla el buen comportamiento en lightning. Si nos fijamos en la transacción de la justicia - en lightning, cuando usted tiene dos partes que entran en el canal y reequilibrar los fondos constantemente sin tener que publicar una transacción, la forma de hacer cumplir la no publicación del estado anterior es por una pena o transacción de la justicia. Si alguien intenta publicar un estado antiguo, puedes robar todos los fondos del canal como forma de castigarlo. Esto se llama transacción de justicia. Uno de los problemas con esto, y con lightning sobre todo, es que tu nodo tiene que estar en línea todo el tiempo porque la única manera de publicar la transacción de justicia es si estás en línea y tu nodo se da cuenta de que el estado incorrecto ha sido publicado.

Recientemente se ha publicado la versión 0.7 de lnd con torres de vigilancia disponibles. Lo que una torre de vigilancia es, es que te permite estar fuera de línea. Básicamente, si estás desconectado, puedes contratar a otro nodo para que vigile la blockchain por ti y publicará la transacción de justicia en tu nombre. Hay algunas construcciones interesantes en las que puedes pagar a la torre de vigilancia para que puedas dividir los fondos de la transacción de castigo que están en esa transacción. No hablan de eso aquí en el artículo.

Una de las cosas que es interesante es comparar las transacciones de justicia con eltoo donde tienen SIGHASH\_NOINPUT. Me pareció un punto de discusión interesante.

P: He actualizado mi nodo para poder utilizar esa funcionalidad. ¿Cómo se realiza la transacción con otros nodos y se les configura para que sean una torre de vigilancia? No me queda claro cómo funciona.

R: Básicamente tienes que encontrar uno, y apuntar tu nodo hacia él y decir que este va a ser mi nodo de vigilancia. Esto añade un aspecto interesante en cuanto a cómo la economía de Lightning se refiere: .... los incentivos de la gente para enrutar los nodos, y enrutar los fondos y ganar honorarios sólo por tener un buen tiempo de actividad. Casa publicó su cosa de latido del nodo donde recompensan activamente a la gente. Olvidé la mecánica de cómo los mantienen honestos. Así que les dan actualizaciones de la transacción de justicia; ahora mismo hay un compromiso de privacidad. Sin eltoo, tienen que tener cada actualización de estado en el canal. Lo bueno de eltoo es que no, básicamente no tienes que almacenar todo el estado. Con eltoo, no necesitas recordar los estados intermedios, sólo el último.

P: Así que los otros nodos me están proporcionando servicios de torre de vigilancia; y a menos que yo actualice mi nodo para tener la torre de vigilancia, entonces otras personas pueden hacer lo mismo. ¿Hay que abrir un canal?

R: No, sólo les das la transacción en bruto.

P: ¿Están encriptando la transacción de justicia?

R: No estoy seguro. Se discutieron mecanismos para dividirlo aún más. La idea era que la torre de vigilancia sólo tuviera conocimiento de tu transacción una vez publicada; no podrían saber los detalles de la transacción, de antemano. Estarían constantemente vigilando la transacción e intentarían desencriptarla todo el tiempo.

P: ¿Ha intentado alguien comercializar algo de esto?

R: Bueno, nadie ha sido capaz de comercializar nada de Lightning. lnbig ha asegurado 5 millones de dólares en la red Lightning y está ganando 20 dólares al mes. En este punto, sólo lo está haciendo por razones altruistas.

P: Uno de los argumentos es que si las tasas del bitcoin suben mucho, tienes la ventaja de tener estos nodos y canales de enrutamiento ya configurados.

R: Sí, pero ahora mismo no es un negocio viable. Podría serlo en el futuro. Ahora mismo, mi sensación es que no estás ganando dinero con las tarifas, pero estás creando liquidez y esto hace que sea más viable para vuestros clientes utilizar Lightning. Así que realmente su modelo de negocio es más acerca de la creación de liquidez y ayudar a la utilidad en lugar de hacer dinero. La idea es que la gente gane cuotas como torres de vigilancia, cuotas de enrutamiento, aumentando la liquidez, y hay otro modelo de negocio donde la gente puede pagar por la liquidez entrante. Esos son los tres principales modelos de negocio de la red de rayos que conozco.

## Modelo de estado estacionario para LN

<https://github.com/gr-g/ln-steady-state-model>

## LN guía

<https://blog.lightning.engineering/posts/2019/08/15/routing-quide-1.html>

¿Hay alguien aquí que tenga un nodo de lightning? Bueno, unos cuantos. Uno de los grandes guiños a los lightning es que no son súper utilizables. Parte de eso es que están tratando de ayudar en el lado de la ingeniería con torres de vigilancia y el piloto automático y las nuevas interfaces gráficas de usuario. Otra gran parte es simplemente, guías sobre cómo ejecutar un nodo de lightning. Ellos van a través de las banderas útiles que se puede activar. Si alguna vez se ejecuta la ayuda de lndcli, es un enorme menú de cosas a tener en cuenta. ¿Alguna historia de horror de los dolores de cabeza de tratar con el lightning y las cosas que sería útil?

P: Más liquidez entrante.

R: ¿Qué cree que podría ayudar a ello? ¿Hay algo en proyecto que pueda ser útil?

P: Grease. Si te descargas su cartera, te dan 100 dólares de liquidez. Cuando se te acaba, tienes que conseguir más canales. Es una especie de extraño problema de incentivos. Es como una línea de crédito. Encerrar los fondos es costoso en el otro extremo, así que necesitan una buena razón para pensar que deben hacerlo.

Uno de los problemas de lightning es que hay que bloquear los fondos. Para recibir fondos, necesitas tener un canal donde alguien tenga sus propios fondos bloqueados. De otra manera, tu canal no puede ser rebalanceado cuando ganas más en tu lado. Si Jimmy tiene $100 de bitcoin en su lado del canal, y yo tengo $100 en mi lado, alguien puede pagarle a Jimmy hasta $100 a través de mí. Una vez que haya ganado 100 dólares y nuestro canal se haya reequilibrado, ya no podrá recibir más dinero. En el caso de los pagos en cadena, cualquiera puede pagarle inmediatamente, y en lightning eso no es lo mismo. La liquidez es un gran problema.

Tienen un servidor de Loop. Es básicamente swaps submarinos. Es una herramienta que aprovecha los swaps submarinos, construida por Lightning Labs, es una forma de tomar fondos por tu cartera lightning fuera de la cadena. Usted hace un bucle enviando a otro monedero que le enviará fondos en la cadena y esto le dará liquidez de entrada. O puedes pagar a tu propia cartera lightning desde los fondos on-chain. Si has visto esas interfaces de tiendas en las que puedes pagar con lightning, o pagar con bitcoin on-chain al lightning wallet, para eso están usando swaps submarinos. Tampoco es barato, porque hay comisiones asociadas. Usted recibe esos fondos de vuelta en la cadena, pero usted tiene que pagar las tasas de transacción en ese punto. Y luego hay cargos asociados con - el servidor Loop está cobrando honorarios por este servicio, que es otro modelo de negocio.

Tienen un mecanismo llamado Loopty Loop en el que se continúa recursivamente el bucle de salida. Se sacan fondos en bucle, se obtienen fnuds encadenados, se sacan en bucle y se vuelven a sacar en bucle. Puedes seguir haciendo eso y obtener liquidez entrante, pero de nuevo no es barato, y no es instantáneo. Así que estás perdiendo algunos de los beneficios de la lightning.

## Copias de seguridad de los canales estáticos

Lightning Labs hablaba ahora de su aplicación móvil. Una de las cosas interesantes de esta actualización es que tienen copias de seguridad de canales estáticos en iCloud. Tenía curiosidad por saber si alguien tenía alguna opinión al respecto. Creo que es genial que se pueda hacer una copia de seguridad en la nube para estos. Almacena el estado del canal, incluyendo cuál es el saldo. Si tu nodo bitcoin se cae, y sólo tienes tu mnemónica, no pasa nada. Pero con LN, tienes estados fuera de la cadena donde no hay registro de ello en la blockchain. El único registro es la contraparte, pero no quieres confiar en ella. Si no tienes copias de seguridad de tu estado, tu contraparte podría publicar una transacción de robo y tú no lo sabrías. También podrías publicar accidentalmente un estado antiguo, lo que daría a tu contraparte la oportunidad de robar todos los fondos del canal, lo que es otra cosa que eltoo puede evitar. Si tienes la aplicación en iOS, estas cosas se actualizan automáticamente y no tienes que preocuparte por ello, pero estás confiando en Apple iCloud.

## Bits de seguridad playground

Esto es... esto te permite pagar micropagos por relámpagos, puedes pagar por precios al contado, o por estadísticas de la NBA, y si fuera a pulsar algo... básicamente, es pagar por una llamada a la API para pequeñas peticiones. Así que sería como casi un AWS en la demanda, así es como lo pienso.

## Boltwall

<https://github.com/Tierion/boltwall>

En el tema de las cosas de la API, esto era algo que recientemente he construido y publicado llamado boltwall. Se trata de un middleware basado en nodejs express que se puede poner delante de las rutas que quieras proteger. Es simple de configurar. Si tienes tu nodo lightning configurado, entonces puedes pasar la configuración necesaria. Estas configuraciones solo se almacenan en tu servidor. El cliente nunca ve nada de esto. O puedes usar opennode, que para los que no lo han usado, es un sistema de lightning custodiado donde ellos manejan el nodo LN y tu pones tu clave API en boltwall. Creo que es lo mejor para los pagos de máquina a máquina.

He utilizado macarrones como parte del mecanismo de autorización. Los macarrones se utilizan en lnd para su autorización y autenticación. Los macarrones son básicamente cookies con mucho más detalle. Las cookies de la web son normalmente un blob json que dice aquí están tus permisos y está firmado por el servidor y tú autentificas la firma. Lo que se hace con las macaroons, es que son básicamente HMACs, así que puedes tener cadenas de macaroons firmadas que están conectadas entre sí. Tengo uno construido aquí que es un macarrón basado en el tiempo donde puedes pagar un satoshi por un segundo de acceso. Cuando pienso en el lightning, hay un montón de puntos de dolor a nivel de consumidor involucrados.

P: ¿Por qué se basa en el tiempo, en lugar de pagar por una solicitud?

R: Depende del mercado. En lugar de decir que pago por una sola solicitud, podrías decir que en lugar del apretón de manos de ida y vuelta, obtienes acceso durante 30 segundos y terminas hasta que el tiempo expira. Construí una aplicación de prueba de concepto que es como un yalls (que es como un medium.com) para la lectura de contenido donde en lugar de pagar una cantidad a granel para un pedazo de contenido, usted dice oh voy a pagar por 30 segundos y ver si desea seguir leyendo sobre la base de eso. Permite mecanismos de precios más flexibles en los que puedes tener una discriminación de precios mucho más fina basada en la demanda.

# Desvarío de la cartera de hardware

<https://stephanlivera.com/episode/97/>

Últimamente he estado hablando de multisig en carteras de hardware. Vamos a empezar con algo que es malo, y luego mostrar algo mejor. Adelante, encienda electrum. Pasa la bandera --testnet. No vamos a hacer lo del servidor personal.

<https://github.com/gwillen/bitcoin/tree/feature-offline-v2>

<https://github.com/gwillen/bitcoin/tree/feature-offline-v1>

<https://github.com/gwillen/bitcoin/tree/feature-offline>

Tenemos un nodo completo de Bitcoin Core aquí. Tenemos QT ahora mismo, pero puedes usar el cli. Hay un componente gastable, y eso no es nada porque todo lo que tengo es watchonly. Estoy usando Bitcoin Core para mis reglas de consenso, pero no lo estoy usando como cartera. Sólo estoy viendo las direcciones, haciendo un seguimiento del historial de transacciones, los saldos, ese tipo de cosas. Así que tenemos el servidor personal de electrum corriendo y el núcleo de bitcoin corriendo. Así que arranco electrum y ejecutarlo en testnet. También puse una bandera para decir, no se conecte accidentalmente a otra persona y decirles lo que todas mis direcciones son. Pones esto en el archivo de configuración, y también en la línea de comandos de nuevo sólo para estar seguro ... Sí, también podrías usar reglas de firewall que podrían ser inteligentes en el futuro.

Podemos mirar una transacción en electrum, por lo que está diciendo que tengo este bitcoin que podemos ver que tengo aquí y mis transacciones recientes y ver que lo he recibido. Ahora bien, si voy a recibir más bitcoin, hay este genial botón de "mostrar en trezor". Si le doy a esto, aparece en trezor y lo muestra. Esta es una parte esencial de la recepción de bitcoin; no preguntas por tu dirección de recepción en tu ordenador infectado con malware. Quieres hacer esta comprobación en un quórum de carteras de hardware. ¿Realmente quieres ir a 3 ubicaciones diferentes de monederos hardware antes de recibir los fondos? Si estás recibiendo 100 millones de dólares, entonces sí quieres. Si estás haciendo 3 de 5, y sólo confirmas en 2 de 5, entonces el atacante podría tener 3 de 5 pero los 2 de 5 han confirmado que son los participantes. Coldcard hará una cosa en la que registre el grupo de pubkeys para que sepa que estamos todos en esto... Coldcard tiene como 3 opciones, una es subir un archivo de texto con las pubkeys. Otra es que cuando le envíes una salida multisig, te ofrecerá crearla y te mostrará los xpubs, y te preguntará si quieres registrarla; y la tercera es confiar que es lo que hacen los demás. Casa te da todos los xpubs... es otra forma en que esto funciona; puedes poner esos en un cliente de electrum offline airgapped nunca toca el internet, y puede generar direcciones de recepción. Asi que puedes decir, bueno, esta maquina que nunca ha tocado internet dice que estos xpubs me daran estas direcciones, asi que 2-de-5 mas electrum offline entonces quizas estoy dispuesto a seguir adelante. Hay códigos QR incorporados para configurar estos.

No me gusta cuando el trezor está conectado a esta máquina, porque creo que la máquina puede estar infectada de malware. Pero este dispositivo podría ser un falso trezor, podría ser un teclado que instala malware o algo así y ni siquiera veo que escriba las urls de malware. Si tenemos tres dispositivos de hardware diferentes, quiero cuatro portátiles. Uno que está conectado a la red bitcoin; y cada uno de los otros tres portátiles están conectados a la cartera de hardware. Les paso las transacciones de bitcoin por código QR. Todo ese ecosistema de ordenador y monedero hardware puede estar eternamente en cuarentena y nunca conectado a internet. Así que podemos construir un airgap de hardware en esto.

Recomiendo un portátil porque tienen cámaras web y baterías. En esta demostración, tenemos que recoger los portátiles y apuntar las pantallas a las cámaras. Una buena cartera de hardware portátil con un escáner de código QR, tienes que recogerlos o algo así, eso estaría bien. Con los ordenadores de sobremesa, esto va a ser doloroso porque tienes que arrastrar tu ordenador a la caja de seguridad. Ten en cuenta que muchos bancos no tienen tomas de corriente en sus cajas fuertes, así que necesitas una batería. En realidad, cualquier máquina de 64 bits debería estar bien. Históricamente, he utilizado 32-bits, pero tails ya no es compatible con eso y algunas versiones de Ubuntu se quejan. En este demo, vamos a usar segwit nativo, y es una configuración multisig así que elige esa opción.

Electrum es muy quisquilloso. Le di al botón de retroceso. Volví a ver si este era el correcto y entonces perdí todo. Estoy usando una cartera de hardware con derivación de clave determinista, así que puedo volver a eso. El botón de retroceso debería preguntarte si realmente quieres deshacer todo este trabajo. La gran advertencia es que no se debe pulsar el botón de retroceso.

Es posible que hayas visto mis hilos de Twitter. Yo aceptaría un monedero de hardware muy malo, si permitiera multisig. Añadir un segundo monedero de hardware es sólo aditivo y puede ayudar a proteger contra los errores del monedero de hardware. En twitter, los fabricantes de carteras dijeron que no era un gran problema. Hay tres grandes problemas con Ledger. No soporta testnet. Toman la clave pública y muestran la representación en mainnet, y te preguntan si quieres enviar allí. No es que no lo apoyen; lo apoyaron en el pasado, y luego dejaron de apoyarlo. Así que no hay testnet. Tampoco tienen un mecanismo para verificar una dirección de recepción. Sólo si quieres usarlo de forma insegura te lo mostrará. El tercer problema es que tampoco soportan el envío, porque no hacen lo de la suma de las entradas y la suma de las salidas. No validan lo que es el cambio y lo que va a otra persona. Sólo te muestran un montón de salidas y te preguntan si parecen correctas, pero como humano no tienes ni idea de saber cuáles son todas las entradas y salidas, a menos que seas extremadamente cuidadoso y tomes notas. De lo contrario, podrían estar enviando cambios a tu atacante o algo así. Trezor no puede verificar que la dirección multisig pertenece a la misma cadena bip32; no puede verificar el quórum, pero puede verificar su propia clave. Así que digamos que es 3 de 5, puedes ir en 3 dispositivos que dirán que sí soy uno de los cinco de este 3 de 5, pero tienes que firmar en 3 dispositivos diferentes para que ahora sepas que eres 3 de esos 5. Siempre se puede demostrar que un monedero es miembro del quórum, excepto en Ledger. Antes exportaban los datos sin decirte cuál era la ruta de bip32, lo cual es un gran agujero. La mayoría de los monederos pueden demostrar que están en un quórum... ¿entienden que una de las salidas está en el mismo quórum que la entrada? Por lo que puedo entender, es sólo Coldcard que entiende que hoy en día. Trezor sabe que es una parte, pero no saben qué parte. Así que si estás firmando con un quórum de dispositivos que controlas con Trezor entonces no estás en riesgo, pero si tienes una tercera parte de confianza refrendando entonces se pone un poco raro porque podrían estar aumentando el número de claves que tiene una tercera parte de confianza. El segwit nativo nos habría permitido hacer los xpubs fuera de orden.

Bitcoin Core puede mostrar un código QR, pero no puede escanearlos. El problema ha estado abierto durante unos 2 años.

El 2-de-2 es malo porque si hay un error en cualquiera de ellos (ni siquiera en ambos) entonces tus fondos se pierden para siempre y no puedes recuperarlos. Un atacante también podría hacer un ataque al estilo Cryptolocker contra ti, y obligarte a darle alguna cantidad de los fondos para recuperar lo que negocies.

Cada uno de estos monederos de hardware tienen firmware, reglas udev, y cosas del lado de la computadora. Algunos de ellos son torpes como, conectarse a un navegador web e instalar alguna mierda. Oh Dios, ¿mi monedero hardware está conectado a internet? Bueno, instálalo una vez, y luego úsalo sólo en el airgap.

Tienes que verificar tu dirección de recepción en los monederos hardware. No te limites a comprobar los últimos caracteres de la dirección en la pantalla del dispositivo de hardware.

Al verificar la transacción en el dispositivo Ledger, la cartera electrum tiene una ventana emergente que ocluye la dirección. El monedero Ledger tampoco muestra el valor en la versión de la dirección de testnet, está mostrando una dirección de mainnet. Tendría que escribir un script para comprobar si esta dirección es realmente la misma dirección de testnet.

De todos modos, Chainalysis probablemente está ejecutando todos los nodos de electrum para testnet.

Me gustaría decir que fue fácil, pero no lo fue. Mucho de esto fue un costo de configuración de una sola vez. No es perfecto. Tiene errores. Tiene problemas. Pero técnicamente funciona. Al final del día, usted tiene que obtener las firmas de dos piezas diferentes de hardware. Puedes ser bastante tranquilo sobre cómo configurar las cosas.

P: Si se utiliza coldcard, ¿se puede obtener el xpub sin tener que enchufar la coldcard?

R: Creo que puedes escribir xpubs en la tarjeta sd.

R: Lo que realmente quiero es... parece que hay algunas cosas como mostrar una dirección, que sólo puedes hacer si la conectas. Muchas de las opciones están enterradas en los menús. La Coldcard es definitivamente mi favorita.

P: El Trezor sólo mostraba una salida porque la otra era de cambio, ¿verdad? Así que si usted estaba creando tres salidas, dos que iban a direcciones que no pertenecían al trezor o al quórum multisig, ¿mostraría las dos salidas en el trezor?

R: Creo que sí. Pero la única manera de saberlo es haciéndolo.

R: Estuve hablando con instagibbs que ha estado trabajando en HWI. Él dice que el trezor recibe una plantilla para lo que es la dirección de cambio; no hace ninguna verificación para definir lo que es el cambio, sólo confía en lo que el cliente dice. Así que puede que no sea mejor que un Ledger. Sólo confía en lo que la máquina caliente sabía. Ledger parece hacer un mejor trabajo porque-- el trezor podría estar ocultando el--- Coldcard está claramente haciendo el mejor trabajo, así que puedes enseñarle sobre los xpubs y puede hacer la afirmación por sí mismo sin tener que confiar en otros.

# Bóvedas (Bryan Bishop)

Genial, gracias por describirlo.

<https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-August/017229.html>

<https://www.coindesk.com/the-vault-is-back-bitcoin-coder-to-revive-plan-to-shield-wallets-from-theft>

<https://bitcoinmagazine.com/articles/revamped-idea-bitcoin-vaults-may-end-exchange-hacks-good>

# Ermitaño

<https://github.com/unchained-capital/hermit>

Al principio, en Unchained empezamos usando Electrum. En ese momento, no estábamos haciendo custodia colaborativa. Teníamos todas las claves, era multisig. Así que, en teoría, teníamos empleados y equipos de firmas usando electrum, y era una experiencia terrible. Era todos los días usando electrum, siempre eran experiencias raras. Tampoco me gusta cómo Electrum construye estas direcciones.

Hoy no voy a hablar de multisig, sino que me voy a centrar en esta nueva herramienta llamada Hermit. Quiero dar una pequeña demostración. Haré algunas diapositivas. Es un monedero sharded de línea de comandos para despliegues de airgap. Tiene cierta similitud con los monederos airgap de código QR. En Unchained, nos centramos en la custodia colaborativa donde tenemos algunas de las claves y los clientes también tienen algunas de las claves. Esto no funcionaría si utilizáramos Electrum nosotros mismos, sería demasiado doloroso. Tuvimos que crear un software que lo agilizara para nosotros. El resultado neto es que estamos protegiendo las claves. Hay una gran diferencia entre una organización que protege las claves y un individuo que las protege.

En particular, para nosotros, no somos una empresa orientada a la cartera caliente. Nuestras transacciones son como mínimo de semanas, si no de meses o años, y se planifican con antelación. Nos gusta mantener todo en multisig y con almacenamiento en frío. Nos gustan los airgaps. Los monederos de hardware tienen un espacio de aire temporal, que puede ser agradable. No queremos gastar miles de dólares en HSMs para mantener un número secreto. Desde nuestro punto de vista, tenemos muchos dispositivos repartidos por la empresa para hacer pruebas, etc. Cada desarrollador tiene muchos dispositivos diferentes de cada tipo. Estas carteras de hardware no pueden costar más de 100 dólares cada una, de lo contrario es demasiado caro confiar en los nuevos productos. No nos gusta Trezor Connect, donde saben la transacción que estamos firmando, eso es profundamente frustrante. De nuevo, no somos individuos aquí, esto es una organización. Somos una empresa. Tenemos que escribir algunas cosas explícitamente o de lo contrario se perderá. Como persona, puede que te acuerdes, pero también debes anotarlo. También como organización, tenemos que coordinar. Como persona, recuerdas las llaves, las ubicaciones, cosas así. No necesitas enviarte un correo electrónico para avisar de que tienes que dar el paso 2 en el proceso, mientras que la empresa tiene este requisito. La mayoría de las empresas tienen rotación de empleados, nosotros parece que no, pero podríamos. También hay mucha información sobre nosotros que es pública, como la dirección de este edificio comercial. Tenemos un montón de carteras de hardware aquí en esta ubicación, pero ninguno de ellos importa. También hay problemas de programación, como gente que se va de vacaciones y otras cosas. Una sola persona no puede atender todas las solicitudes de firma, se quemaría. Así que tenemos que rotar, y tener tiempo de actividad, y así sucesivamente.

¿Cuáles son las opciones? Bueno, los monederos de hardware. Queremos animar a los clientes a utilizar carteras de hardware, y esperamos que haya mejores carteras de hardware en el futuro. Son mejores que los monederos de papel. Debido al producto multisig que ofrecemos, creemos que incluso los monederos malos cuando se juntan tienen un efecto multiplicador en la seguridad.

Hoy en día, no creo que sea razonable tener clientes que usen Hermit es demasiado para ellos. Probablemente utilizarán carteras de hardware en el futuro inmediato. Hemos estado utilizando carteras de hardware y nos gustaría pasar a algo como Hermit. Un candidato que miramos y que nos gustó mucho fue un proyecto llamado Subzero en Square, que pretendía ser una herramienta de airgapped y servir como almacenamiento en frío. Es un producto realmente bueno, pero no era suficiente para nosotros. Necesitábamos algo un poco más complejo.

Aquí muestro un diagrama de dos formas diferentes de pensar en la protección de una clave como multisig y Shamir secret sharing. ¿Se puede conseguir algo de redundancia sin usar multisig? Claro que sí, puedes utilizar la compartición de secretos de Shamir. Hay algunas propiedades interesantes como que se requiere que 2 de 3 acciones se combinen juntas en el mismo lugar. Un aspecto sorprendente de este esquema es que si tienes un fragmento, tienes precisamente cero piezas de información. Es un salto discreto en el que en cuanto tienes n fragmentos, lo consigues. No es sólo cortar trozos de una mnemotecnia o lo que sea, y reduce el espacio de búsqueda para un atacante. No es así como funcionan las acciones secretas.

SLIP 39 hace que sea más conveniente hacer fragmentos de Shamir encriptados con mnemónicos. SLIP 39 fue sacado por la gente de Trezor. Por mucho que nos caguemos en las carteras de hardware, tengo que saludar al equipo de SatoshiLabs por adelantarse a todo el mundo y liberar código fundacional como bip32 e implementarlo y hacerlo de una manera de código abierto. Leyendo su código fue como entendí algunas de sus ideas. Otra cosa que han hecho es liberar un sistema de fragmentos Shamir de 2 niveles. Quieren crear una forma de hacer sharding secreto Shamir, sin que todos los shards sean iguales. Puedes distinguir shards más o menos valiosos o distribuirlos a gente de confianza más o menos en función del nivel de seguridad de cada persona o de cada grupo. Así que puedes tener un secreto 1-de-3, y el segundo grupo puede tener una configuración diferente como 3-de-5. Esto no es multisig... donde puedes hacer esto de forma asíncrona en diferentes lugares y nunca estás obligado a estar en un lugar con todas tus claves. Esto no es eso, pero te da flexibilidad.

Voy a hacer una demostración rápida de cómo es el Ermitaño.

* [Creación de una familia de fragmentos](https://www.youtube.com/watch?v=tOc0GBjIK8Y&feature=youtu.be)
* [Exportación/importación de fragmentos](https://www.youtube.com/watch?v=usBk-X3a4Qo&feature=youtu.be)
* [Exportar una clave pública](https://www.youtube.com/watch?v=ut9ALBqjZbg&feature=youtu.be)
* [Firmar una transacción en bitcoin](https://www.youtube.com/watch?v=NYjJa0fUxQE&feature=youtu.be)

Hermit es un software de código abierto. Es "compatible con los estándares" pero es un nuevo estándar. SLIP 0039 no está realmente revisado criptográficamente todavía. Hemos contribuido no sólo con Hermit como una aplicación que utiliza SLIP 39, sino que hemos estado impulsando el código en la capa para decir que esta es la implementación de Shamir que... hasta ahora esta es la que la gente parece estar eligiendo, lo cual es emocionante. Está diseñada para despliegues en el aire, lo cual es bueno.

Hermit no es multisig. Multisig y shard son complementarios. Para un individuo, en lugar de gestionar shards, tal vez gestionar más de una clave. Para nosotros, ya estamos en un contexto de multisig aquí en Unchained, y queremos ser capaces de hacer un mejor trabajo y tener mejores controles de gestión de claves. Hermit tampoco es un monedero online. ¿Cómo supo qué poner aquí? No tiene ni idea. Algo más tiene que producir el código QR con bip174 PSBTs. El mes que viene, estoy emocionado de tener tiempo para presentar lo que creemos que es la otra mitad de esto, una herramienta para los monederos. Un monedero online está produciendo estos PSBTs y honestamente, sugiero imprimirlos. Imprima todos los metadatos, y venga a la sala y luego firme.

Hermit no es un HSM. Es una pieza de software python que se ejecuta en un ordenador portátil básico, que no es un HSM. El Ledger es un pequeño cónclave de alta seguridad que vive en el dispositivo electrónico y tiene propiedades interesantes. En particular, las formas de comunicarse dentro y fuera de él son realmente restrictivas y nunca revelará la clave. Si lo piensas, eso es lo que es una instalación Hermit. Tú controlas el hardware, es completamente de código abierto. Esto es básicamente lo que querías de un HSM, especialmente si lo ejecutas en un contexto que es extremadamente seguro. Sin embargo, los HSM son presumiblemente seguros incluso si los conectas a un portátil infectado con malware.

P: ¿Así que se celebra una ceremonia de firma y los propietarios de los fragmentos entran en la sala, introducen su parte y siguen adelante?

R: Sí, esa es una forma de hacerlo.

P: Así que para producir una firma de bitcoin, se necesita un quórum de fragmentos de cada grupo.

R: Correcto, es desbloquear todos los fragmentos juntos en la memoria en un lugar y luego actuar con eso. Lo que nos gusta de esto es que es una buena mezcla para nosotros porque podemos crear equipos de firma adversarios que se vigilan mutuamente y limitan las oportunidades de colusión. El uso de SLIP 39 es realmente agradable y flexible para las organizaciones.

Trezor afirma que soportará SLIP 39 a finales de verano, lo cual es realmente interesante porque puedes recuperar fragmentos de uno en uno en un Trezor y simplemente caminar hacia cada fragmento y recogerlos y obtener el secreto completo.

# Jimmy stuff

Por último, pero no menos importante, Jimmy tiene algo que vendernos. Este es El pequeño libro de bitcoin. Está disponible en Amazon ahora mismo. Tuve siete coautores en esto. Escribimos el libro en cuatro días, lo que fue una experiencia muy divertida. Está pensado para alguien que no sabe nada de bitcoin. Es una lectura muy corta, de 115 páginas. Unas 30 páginas son de preguntas y respuestas. Otras 10 son glosario y cosas por el estilo. Así que son más bien 75 páginas que se pueden leer muy rápidamente. Teníamos en mente a una persona que no sabe nada de bitcoin. Le he dado este libro a mi esposa, que no sabe mucho sobre lo que está pasando; está destinado a ser ese tipo de libro que es entendible. El primer capítulo es "¿qué pasa con el dinero hoy en día?" y ¿qué pasa con el sistema actual? No menciona el bitcoin ni una sola vez, y luego pasa a lo que es el bitcoin. Se cuenta la historia del banco Lehman y se habla de lo que llevó a Satoshi a crear bitcoin. El otro capítulo es sobre el precio y la volatilidad. Preguntamos a mucha gente que conocíamos y que no sabía nada de bitcoin, se preguntan ¿con qué está respaldado? ¿Por qué tiene un precio de mercado? El capítulo cuatro es sobre por qué el bitcoin es importante para los derechos humanos y esto es sólo hablar de ello a nivel mundial y por qué es importante en este momento. Hay una perspectiva muy centrada en Silicon Valley sobre el bitcoin que es que va a interrumpir o lo que sea, pero hay personas reales en este momento que se están beneficiando de bitcoin que no tenían herramientas financieras o cuentas bancarias disponibles antes. Ahora mismo hay gente que escapa de Venezuela por el bitcoin. Hay un descuento de bitcoin en Colombia ahora mismo, porque hay muchos refugiados que salen de Venezuela con su riqueza en bitcoin y lo venden inmediatamente en Colombia para empezar su nueva vida. Hay taxistas en Irán que me preguntan por el bitcoin. Esto es algo real, chicos. Conseguir esa perspectiva global es un gran objetivo de este libro. El capítulo cinco es una historia de dos futuros y aquí es donde especulamos sobre cómo sería el futuro sin bitcoin, y luego cómo sería el futuro con bitcoin. Por último, aquí es donde termina el libro, y luego tenemos un montón de preguntas y respuestas y cosas que usted puede querer saber. Hay preguntas como, ¿quién es Satoshi? ¿Quién controla el bitcoin? ¿No es demasiado volátil? ¿Cómo se puede confiar en él? ¿Por qué se han pirateado tantos intercambios? Hay toda una sección sobre la cuestión energética. Todo tipo de cosas por el estilo. Recursos adicionales, como la página de Lopp, podcasts, libros, sitios web, cosas así. Probablemente voy a enviar esto con mis tarjetas de Navidad o algo así. La mitad de mis amigos no tienen ni idea de lo que estoy haciendo aquí. Esta es mi manera de informarles. Es el número en Amazon para la categoría de monedas digitales.

---
title: BIP324 - Versión 2 del protocolo de transporte cifrado p2p
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - v2-p2p-transport
  - bitcoin-core
date: 2022-10-10
aliases:
  - /es/bitcoin-core-dev-tech/2022-10-10-p2p-encryption/
---
# Intervenciones anteriores

<https://btctranscripts.com/scalingbitcoin/milan-2016/bip151-peer-encryption/>

<https://btctranscripts.com/sf-bitcoin-meetup/2017-09-04-jonas-schnelli-bip150-bip151/>

<https://btctranscripts.com/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/>

<https://btctranscripts.com/breaking-bitcoin/2019/p2p-encryption/>

# Introducción y motivación

¿Podemos apagar las luces? "A oscuras" es un bonito tema para la charla. También tengo café oscuro. De acuerdo.

Vamos a hablar un poco sobre [bip324](https://bip324.com/). Este es un BIP que ha tenido una larga historia. Incluso tenemos una página sobre la historia. Todo empezó hace más de 6 años... El tráfico Bitcoin p2p no está encriptado. Siempre lo ha estado. Nos gustaría cambiar eso. El argumento de por qué queremos eso es más sutil que en muchos otros entornos. En Bitcoin, por naturaleza, todos los datos que se intercambian entre nodos son datos públicos. O al menos en algún momento serán datos públicos. Cada transacción que se retransmite con suerte termina en la cadena de bloques, y así sucesivamente. Así que la cuestión de por qué querríamos encriptación o privacidad en la red p2p en general es más una cuestión de metadatos en el sentido de que, por ejemplo, un observador global que puede ver muchas conexiones puede inferir el origen de la transacción viendo picos de ancho de banda en un lugar que se propagan más allá. Ahora pueden mirar los datos y ver que la transacción va a todas partes; podrían identificar dónde están los mineros en la topología de la red viendo dónde se originó un bloque al principio. Esto conduce a más efectos de segundo orden, y si estás dispuesto a llevar a cabo un ataque eclipse en la red, entonces puedes extraer más información, o privacidad sobre quién está ejecutando qué versión o quién está realizando transacciones con quién.

Esto, por supuesto, enlaza con la cuestión de la autenticación, en la que los nodos bitcoin no tienen una identidad hoy en día y no queremos cambiar eso. Pero por su propia naturaleza, los nodos no tienen realmente un sistema de reputación. Todos los nodos son iguales y realmente no podemos hablar de mientras hablan el protocolo y hacer las cosas que no podemos hablar de un atacante o no. Pero al mismo tiempo, es cierto que mucha gente utiliza conexiones deliberadas en las que tengo dos nodos y los conecto o tengo un monedero en mi teléfono y quiero conectarme a mi propio nodo porque obviamente confío más en mi propio nodo que en otros nodos. Hoy en día, el sistema de identidad utilizado para eso son las direcciones IP. Claro, puedes configurar una VPN, pero esto es molesto.

La mayoría de las veces no nos importa la autenticación, por eso no forma parte de bip324. Pero ahora la pregunta es, ¿tiene sentido cifrar si no tienes autenticación? Como la mayoría de la gente sabe, si no tienes autenticación no puedes hacer canales seguros porque siempre puedes tener un atacante "man-in-the-middle". Y lo que es más importante, el hecho de que un atacante pueda simplemente hacer girar nodos hace que toda la cuestión de, bueno, un atacante sea difícil de definir incluso sin una noción de identidad.

Nuestra respuesta es que sí, que merece la pena cifrar aunque no tengamos autenticación. Aumenta el coste de un ataque. Realizar ataques de vigilancia global en la red, aunque sólo sea para analizar metadatos, es mucho más complejo si se necesita un estado de cifrado y, o bien hay que crear millones de nodos, o bien conseguir que otros se conecten a los nuestros, o bien interceptar las conexiones existentes, lo que es mucho más caro que limitarse a examinar el tráfico. Si tienes que MiTM todas las conexiones existentes en el mundo, entonces eso no es realmente factible; si MiTM algunas de las conexiones en el mundo, entonces es de esperar que algunas personas en algún lugar del mundo se daría cuenta.

Así que se trata de aumentar los costes de tal atacante, y es barato aumentar estos costes. También queremos construir un sistema en el que se puedan incluir mecanismos de autenticación opcionales. No están incluidos en la propuesta bip324. Tenemos un esquema criptográfico genial en el que también estamos trabajando, pero eso es para más adelante.

No queremos identidades globales en la red. La mayoría de las conexiones no serán autenticadas. En ese punto, ni siquiera está claro si la gente querría alguna forma de autenticación. Digamos que tienes dos nodos y quieres conectarlos directamente. En ese caso, puede que quieras autenticación. Pero incluso en ese caso, no está claro qué información querrías revelar allí y qué información no querrías revelar.

Hacemos una distinción entre la red que consiste en un montón de conexiones automáticas aleatorias en las que a los pares realmente no les importa a quién se están conectando, y las conexiones manuales deliberadas en las que te conectas a un nodo específico en el que tienes alguna noción de identidad. Lo que hace esta propuesta de cifrado es que, incluso si sólo las deliberadas empiezan a utilizar en algún momento un mecanismo de autenticación, deberían ser indistinguibles porque todas las conexiones que queremos están cifradas. Algunas estarán autenticadas, pero un atacante no podría saberlo.

¿Tiene sentido cifrar sin autenticación? Sí, porque aumenta el coste de un ataque para el atacante y ocultará información de metadatos en la red. Nuestra visión es que todas las conexiones estén cifradas y que, si la gente quiere utilizar autenticación, también puedan hacerlo, algo que no se incluye en esta propuesta, aunque hay una interfaz para que las propuestas de autenticación posteriores utilicen esta plataforma.

Hay una autenticación incluida en bip324 que es que los operadores de nodo pueden fuera de banda comparar el ID de sesión... es algo así como... puede ser suficiente para detectar un ataque MiTM. Para ejecutar tu propio nodo con conexiones autenticadas entre dos de tus nodos, esto probablemente sería factible. Es una defensa contra ataques MiTM. Si sabes que algunos nerds están haciendo esta comparación, entonces el atacante no puede simplemente MiTM todas las conexiones.

P: jonaschnelli estaba diciendo que esto no debería ser referido como encriptación sino más bien como un formato de mensaje p2p v2 debido a todas las otras actualizaciones, que también podrían incluir un id de sesión de encriptación.

R: Sí. Los mensajes son 3 bytes más cortos ahora en esta propuesta. Al final, los mensajes serán más cortos. No me preocupa este argumento, porque ya lo tuvimos en los debates sobre TLS hace 20 años, cuando algo suponía medio porcentaje más de utilización de la CPU y otros argumentaban que era demasiado caro.

El razonamiento es más como, estamos proponiendo una actualización de la red p2p y su principal característica es que hace el cifrado oportunista. Al mismo tiempo, no empeora el ancho de banda ni el tiempo de CPU. O al menos no de forma apreciable. Realmente no supone ningún coste en comparación con lo que existe porque la red existente es realmente ineficiente.

P: ...

R: Hay dos informaciones distintas que pretendemos ocultar. Una es, ¿hay un nodo bitcoin funcionando aquí? Ahí damos algunos pasos. La otra es ocultar los datos que se están transfiriendo. Ninguno de estos tenemos éxito en ocultar perfectamente, lo único que hacemos es aumentar los costos. Un atacante puede ejecutar un nodo él mismo o MiTM la conexión o lo que sea y todavía ver lo que está pasando por allí. Todavía pueden hacer análisis de tráfico, incluso si no leen los bytes encriptados pueden ver picos. Proporcionamos mecanismos para ocultar esa información, pero la forma de utilizarlos no forma parte de bip324.

P: ¿Cómo se cuantifica esto... y debido a este análisis de tráfico... ¿Cuál es el atacante pasivo global si...

R: Mira todas las conexiones y mira dónde apareció por primera vez una transacción bitcoin y entonces sabrías qué nodo la creó. Se trata específicamente de ocultar los flujos de transacciones.  Todavía es posible con el análisis de tráfico, pero el análisis de tráfico se vuelve más difícil que simplemente ver la transacción en el cable. Una vez que la retransmisión de transacciones está encriptada, puedes rellenar las transacciones para que tengan el mismo tamaño con algunos bytes extra, lo que es inútil ahora mismo porque las transacciones no están encriptadas en absoluto.

El análisis del tráfico se vuelve menos fácil o menos posible. Algunos tipos de transacciones son fáciles de mapear, como las basadas en el tamaño del conjunto UTXO. Fundamentalmente hace que sea más difícil de entender lo que es porque las propiedades son diferentes y hay más fuentes posibles. Eso es cierto si sólo eres un observador pasivo que sólo obtiene datos de tráfico, frente a obtener los datos pinchando el cable. El atacante también puede MiTM la conexión, pero eso es mucho más costoso. No es la misma clase de ataque. Con este tipo de cosas, encontrarás que los atacantes activos globales tienen mucho más difícil ir y hacer sus ataques, especialmente si hay más de uno de ellos.

P: ¿Pero puedo seguir mirando el tamaño del cifrado?

R: Sí, pero las transacciones pequeñas tienen aproximadamente el mismo tamaño. ....

P: Dado que otros métodos son cada vez más costosos, ... ¿qué tal si nos conectamos a cada uno de los nodos e intentamos hacerlo de esa manera?

R: Ya lo están haciendo.

P: ¿Pero esto no animaría a más gente a hacerlo?

R: Es una buena pregunta. Va en la línea de lo que acabamos de describir. Creo que lo decimos literalmente en alguna parte. Queremos obligar a los atacantes a activarse si realmente quieren atacar. Es una buena pregunta si esto sería malo para la red. El contraargumento sería que deberíamos simplemente volcarles todos los datos para que no ataquen la red. No estoy seguro de que eso sea mejor. Recibimos peticiones de personas que investigan el análisis p2p: "¿por qué no proporcionáis un mensaje p2p para preguntar a los nodos con quién están conectados, sería una información muy valiosa?" Sí, también sería muy valioso para los atacantes. Es una escalada mutua....

¿Alguna pregunta más sobre la motivación o la configuración? Podríamos entrar en la historia.  Una información que queremos ocultar es si estamos ejecutando el protocolo bitcoin. Una forma de verlo es simplemente intentar hacer una conexión. El protocolo v1 literalmente comienza con el envío de la magia de red seguida de la versión. Son 12 bytes muy reconocibles que probablemente nada más en el mundo envía. Así que hacemos un intento de tener un poco de resistencia a la censura; por el momento, es muy fácil para los cortafuegos mirar los primeros 12 bytes y ver que se trata de una conexión bitcoin. También pueden mirar información más simple como los números de puerto, por supuesto. Pero queremos proporcionar un protocolo básico que se pueda utilizar en el futuro para realizar trabajos más avanzados.

Se trata, de nuevo, de aumentar los costes. Una respuesta obvia a un posible censor de bitcoin p2p es, bueno, ahora tienen que bloquear todo excepto una lista blanca de protocolos permitidos que probablemente tiene muchos más daños colaterales en lugar de sólo bloquear bitcoin p2p. Este es siempre el juego de la resistencia a la censura. Cuando lo defines, no se trata de la capacidad de conectarse, porque tu ISP siempre puede desconectarte. En realidad, se trata de los daños colaterales que causarían si desconectaran el servicio por completo.

P: Si quiero diseñar mi propio protocolo p2p, y sigo esto, ¿sería indistinguible de bitcoin?

R: Sí. Para un atacante pasivo, el flujo de bytes de una conexión bip324 es uniformemente aleatorio. Cada byte que pasa por él, no tiene ningún patrón estadístico. Este es un denominador común muy agradable que cualquier cosa como, ni siquiera es necesario utilizar el mismo tipo de criptografía ... hay otros tipos de protocolos como tor, u otros. También puedes meterlo en otros protocolos, podrías escribir una envoltura HTTP. Eso sería un objetivo mucho más ambicioso que tratar de disfrazar el tráfico bitcoin p2p como tráfico HTTPS o ssh, lo cual es difícil porque no estamos corriendo en un puerto HTTPS estándar que ya lo delata. HTTPS tiene otro problema. Pero al menos se hace más fácil construir sobre una construcción uniforme como bip324.

La manipulación también se vuelve más compleja. Ahora mismo, un atacante puede simplemente voltear bytes en un mensaje y darse cuenta inmediatamente y terminar la conexión. Incluso para un atacante activo, por ejemplo, cambiar un bit de superficie en el mensaje de versión es muy barato, basta con hacer coincidir el patrón y cambiarlo. Una vez que tienes una conexión cifrada autenticada, y en este punto debo decir que la autenticación en el contexto de las conexiones cifradas tiene dos significados completamente diferentes. Uno es si estoy hablando con quien tengo la intención de hablar con respecto a alguna identidad, que no hacemos en bip324. Pero tenemos un esquema de encriptación autenticado, lo que significa que sabemos que cada mensaje, una vez desencriptado correctamente, procede del otro lado. No sabemos quiénes son, pero sabemos que ningún atacante MiTM entró y lo cambió. Obtenemos una identidad efímera al principio del protocolo y si más tarde el atacante quiere cambiar algo, entonces nos damos cuenta. O haces un ataque MiTM completo, o no puedes cambiar las cosas.

Si utilizáramos un cifrado no autenticado, que es lo que no hacemos, entonces un atacante podría ser capaz de adivinar: "oh, este es probablemente el mensaje de versión y este es el bit de servicio", incluso sin saber cuál es el bit, puede voltear ese bit. Esto se evita con el cifrado autenticado.

¿Por qué un bytestream pseudoaleatorio? Análisis de tráfico... sí, entramos en eso. Puedes mirar el tiempo, los tamaños, y un interceptor inteligente puede mirar los mensajes más grandes y si obtienes un bloque cada 10 minutos entonces tal vez sea el protocolo bitcoin. Pero es mucho más difícil que simplemente hacer coincidir patrones en bytes exactos.

¿Por qué no usar un protocolo de túnel seguro? ¿Por qué no usar Tor para todo? ¿O VPN? Realmente la respuesta es que queremos algo que funcione para todas las conexiones. Lo queremos ubicuo y también queremos poder definir extensiones más adelante, como para la autenticación. No queremos que se distingan las autenticadas de las no autenticadas. Esto tiene que funcionar en todas partes. Hacerlo sobre Tor funcionaría, pero tendría un gran coste.

Tor es una red centralizada. Tiene un conjunto de 16 nodos que controlan todo. Mucha gente olvida esto. Así que desde el principio, no podemos decir simplemente usa Tor. También la latencia es mucho mayor, y los costos de ancho de banda son mucho más altos. Controlar un montón de direcciones IP es más difícil que conseguir miles de nuevas identidades tor porque son sólo claves públicas. Los ataques Eclipse sólo en Tor son mucho más baratos que en la Internet real.

VPNs o wireguard o lo que sea, sí se podría hacer esto, pero está construido para la configuración manual. VPNs requi eren configuración. Queremos algo que funcione para conexiones automáticas que esté habilitado por defecto.

Otra cosa que podrías hacer es que hay protocolos de canal seguro de propósito general como TLS y Noise, Noise es en realidad un framework para definir tu propio protocolo. Podrías hacerlo, pero realmente no encaja en nuestro caso de uso porque se centra en la autenticación. A menudo quieres encriptación con autenticación. Todos estos protocolos se centran en eso... sus propiedades se rompen o introducen una enorme cantidad de complejidad sólo por tener autenticación. En su lugar, queremos algo muy simple que sólo haga encriptación pero que sea lo suficientemente modular como para que puedas construir algo con autenticación encima. La desventaja es que esto probablemente dará lugar a un protocolo con más viajes de ida y vuelta, pero no nos importan los viajes de ida y vuelta porque las conexiones bitcoin p2p duran minutos, días, horas, semanas, a veces más.

P: Entonces, ¿estás utilizando un cifrado autenticado pero no estás autenticando el otro punto final?

R: Correcto.

P: ¿Podemos utilizar otra palabra que no sea autenticación?

R: Yo propuse "integridad", pero es mala idea porque la comunidad criptográfica ya ha establecido estos términos, así que crearía más confusión.

Sin embargo, existe una clave pública. Sólo que no está identificada. Existe la autenticación y el cifrado autenticado. El cifrado de disco duro suele ser un cifrado no autenticado. La definición ya está en el BIP. Tenemos una nota a pie de página. Así que léete el BIP.

Si desea ejecutar TLS sin autenticación, puede hacer cosas como certificados autofirmados, pero introducir eso en Bitcoin Core realmente no tiene sentido. Nadie quiere eso. Tenemos algunas otras razones, como que queremos un protocolo basado en mensajes y no en flujos. Esto en sí mismo introduce propiedades de privacidad que queremos introducir. TLS y Noise están basados en cadenas y no tienen noción de ocultar información de paquetes. Todavía necesitaríamos construir algo para eso y deshacer ese daño si hiciéramos eso.

Otra razón es que queremos usar la curva secp256k1, pero la razón para usar protocolos estándar desaparecería porque no lo hacen. Así que al final, usar algo que ya existe no tiene sentido. Además, tenemos conexiones de larga duración. No nos importa demasiado la latencia de las conexiones. Esto significa que los viajes de ida y vuelta están bien. Digamos que empezamos cifrando y luego, si quieres hacer la autenticación, puedes hacerlo más tarde, dentro de la conexión cifrada. En otros protocolos, intentan hacer esto al principio de sus protocolos para ahorrar viajes de ida y vuelta. La ingeniería moderna de TLS hace que funcione con la mitad de las idas y vueltas o, en algunos casos, sin ninguna ida y vuelta. Pero en realidad no tenemos esos requisitos.

Lo bueno de un bytestream pseudoaleatorio es que no importa qué criptografía utilices, todas son indistinguibles unas de otras, modulo tiempo y toda la criptografía rota.

# Objetivos

Queremos confidencialidad contra ataques pasivos. Como atacante pasivo, no deberías poder leer los datos que se envían.

Observabilidad de ataques activos: ahora que los ataques pasivos no funcionan, tienes que volverte activo. Así que lo mínimo que se podría hacer es comparar el ID de sesión.

Quieres un bytestream pseudoaleatorio porque cada byte tiene que parecerse a un byte aleatorio. Sin identificadores de versión y sin prefijos o claves públicas, nada.

Queremos tener un bytestream moldeable. Ese es el relleno al que nos referimos. El protocolo tiene la capacidad de rellenar mensajes arbitrariamente, así que puedes hacer algo como definir una extensión o tener una implementación que diga que cada segundo envío 10 kilobytes como un reloj. Si tengo más que enviar, va a un búfer y sólo envío 10 kilobytes cada segundo. Si mi buffer está vacío, lo relleno con basura para seguir enviando 10 kilobytes. Ahora su información de fragmentación temporal no revela nada. Nuestro BIP no especifica cómo hacerlo, sólo proporciona el mecanismo para hacerlo.

Queremos secreto hacia adelante. Hay diferentes nociones de forward secrecy. En nuestro caso significa que si un fisgón ataca el bytestream cifrado y más tarde compromete un nodo con los secretos de sesión, entonces no debería ser capaz de descifrar el tráfico de sesión pasado. Tal vez los últimos bytes, pero no todo el tráfico anterior. Hay una ventana de tiempo limitada de lo que puedes ver.

Tenemos una clave de encriptación simétrica, y cada pocos paquetes hacemos un hash de la clave en... si robas la nueva clave, no puedes volver atrás, la función hash protege contra eso. Esto no se ha utilizado en la práctica, curiosamente, pero es barato y simple y funciona.

Hay una noción de construcción de doble trinquete en Noise y otros protocolos de mensajes. Incluso los hay en los que cada mensaje que envías requiere una nueva negociación de claves. El secreto hacia adelante puede significar diferentes cosas. A menudo significa, como en TLS, que tienes una conexión TLs y se termina, pero ahora robas la clave secreta del servidor y no debería ser capaz de descifrar el tráfico pasado. Eso está relacionado con los secretos a largo plazo; pero aquí no tenemos secretos a largo plazo porque cada secreto es sólo de sesión. Así que aquí tenemos forward secrecy dentro de la sesión.

Si alguien añade la autenticación de identidad, esto no compromete el secreto hacia adelante porque el secreto hacia adelante comenzó con una clave y sólo .... esta propiedad en el lado de la encriptación permanece. Obviamente, podrían ser capaces de falsificar identidades cuando obtengan las claves secretas de identidad.

Capacidad de actualización: tenemos un mecanismo de versión. Esto es importante. Es importante tener esto. Creemos que el paso de ir a un protocolo uniformemente aleatorio es que, no hay ninguna característica identificable para un observador pasivo, lo que significa que hemos eliminado la capacidad del futuro en .... no podemos hacer una v3 o... podríamos, pero necesitarías señalización fuera de banda para determinar cuál de las dos versiones usar. Así que creemos que es importante que el propio protocolo tenga un medio para decir que una vez negociada la sesión cifrada, podemos seguir negociando y ahora cambiar a v3 y ahora cambiar a v4. Así, para un observador que no pueda romper el cifrado o la criptografía v2, no podrá saber qué versión estás utilizando. Podrías actualizar a la autenticación opcional o al handshake criptográfico post-cuántico, y esto es más complejo en este escenario tendrías algo como... digamos que Diffie-Hellman está roto y quieres hacer criptografía post-cuántica, entonces harías el handshake normal como ahora y quizás un atacante pueda leer esto, y eso está bien, pero entonces actualizaríamos con un handshake post-cuántico dentro de él. Probablemente sería un largo tiempo durante el cual secp no está realmente roto, y mientras ese sea el caso, un atacante no puede ver nada. Además, si se rompe, la red p2p no es el mayor problema.

Compatibilidad: los clientes v2 permitirán conexiones entrantes v1 porque no queremos particionar la red. Esto será muy oportunista si cualquiera de los dos lados no soporta v2 será simplemente una conexión v1. ¿Y si tenemos diferentes números de puerto y los anunciamos por separado? No. En primer lugar, usar números de puerto fijos es algo imposible, tener números de puerto predefinidos es una contradicción con ocultar el funcionamiento de un nodo bitcoin. Desde la anterior versión principal de bitcoin, ya no tiene una fuerte preferencia por el puerto 8333. ... Podrías anunciar dos identidades separadas y dos puertos separados. Empezamos a tratar diferentes puertos en la misma IP como un separado.... hmm. Empezamos a tratar diferentes puertos en la misma IP como diferentes entradas addrman; totalmente podríamos hacer eso.

¿Cómo funcionaría eso con la siembra DNS? Buena pregunta. La verdad es que no. Creo que el futuro a largo plazo de las semillas DNS es que se conviertan en nodos p2p a los que te conectas con una conexión única. Pero ahora esto significa que las semillas DNS tendrían visibilidad sobre quién les está pidiendo pares. Pero la ventaja es que tu semilla DNS no lo sabría; ahora sólo lo saben los servidores PDNS del medio. Podríamos imaginar algo así como tener semillas DNS que utilicen un nombre diferente para las que están habilitadas para v2, pero aún así se necesita un medio para comunicar el número de puerto. Creo que, de momento, habrá que mantenerlos en un puerto estándar.

P: ¿Por qué no utilizamos registros SRV?

Históricamente, la razón fue que lo investigamos, creo que hace 10 años, no lo sé, y la dificultad radicaba básicamente en que necesitábamos implementar nuestro propio resolvedor DNS porque no se puede utilizar el resolvedor de nombres del sistema operativo, ya que su interfaz sólo devuelve una dirección IP. Pero sí que es una solución.

Algunos ISPs sus DNS resolvers están rotos y no devuelven los registros SRV correctamente.

Otra desventaja de usar diferentes puertos es que en algún punto el argumento se vuelve confuso pero es aún más fácil de bloquear. En algún momento un cortafuegos puede simplemente permitir o denegar puertos, por lo que sería muy fácil bloquear conexiones v2 y permitir conexiones v1.

Podrías argumentar que para esta actualización podrías tener puertos separados. Pero en el futuro, todos los protocolos deberían usar el mismo puerto. A largo plazo, esperamos que todo use bip324. Este es el futuro a largo plazo. Debería convertirse en omnipresente.

¿Prohibirá v2 a v1 enviar basura? Resolvemos esto añadiendo una frase en bip324. Si te encuentras con una desconexión inmediata, se te anima a que te vuelvas a conectar inmediatamente como v1. No creo que te baneen inmediatamente por esto en esta etapa porque es sólo un desajuste de la magia de la red y se desconectará.

Si fuera tan fácil ir y ser baneado, entonces podrías ir a particionar la red. Tendríamos un gran problema si tu nodo pudiera ser baneado sólo por eso.

El último objetivo aquí es la baja sobrecarga. Ya hemos hablado de ello. No debería aumentar sustancialmente el coste computacional o el ancho de banda de los nodos. Es un poco menos ancho de banda que v1 p2p, y es un poco menos CPU si tienes una implementación CPU pura de sha256. Si se utiliza sha256 acelerado por hardware, es muy difícil superarlo.

P: ¿La nueva suma de comprobación tiene corrección de errores?

No. Algo a hacer en una capa diferente.

# Historia

Esta propuesta ha tenido una larga historia. Comenzó en 2016 por Jonas Schnelli. La idea inicial eran dos bips: bip151 y bip150 que harían encriptación y autenticación. Tenían un enfoque muy diferente a lo que tenemos ahora, que es la razón por la que es un número bip diferente. Bip151 empezaba como una conexión v1 y enviaba un mensaje a nivel de aplicación diciendo "me gustaría actualizar a v2" y la otra parte respondía "sí, ahora somos v2". Esto tiene algunas desventajas obvias: entre otras, has enviado un mensaje de versión en claro antes de que cualquier negociación de encriptación tuviera lugar. Esto no oculta la conexión en curso. Podría incluso ser peor para la autentificación porque usted puede ser que desee hablar solamente con cierto nodo, y después de enviar algunos mensajes del texto claro usted entendería eso, .. había tentativas en aislamiento allí pero eran más débiles. En algún momento pensamos que si queríamos conexiones encriptadas, toda la conexión debería estar encriptada, y fue entonces cuando comenzó el proyecto bip324 sin autenticación. Pensamos que era más modular y que podría hacerse más tarde o por separado. Esto pasó por una serie de iteraciones. Hasta 2019, Jonas estaba trabajando en esto, pero sólo de vez en cuando.  Dhruv se interesó y nos mantuvo ocupados. Nos seguía enviando mensajes sobre el progreso. Enhorabuena a Dhruv.

P: ¿Recuerda [refrendo][refrendo-sección-en-otra-transcripción]?

Es el protocolo de autenticación privada en el que estamos pensando. Se trata de un novedoso esquema criptográfico sobre el que queremos una redacción y revisión académicas o más formales antes de plantearnos siquiera proponerlo. No está claro qué tipo de autenticación querrá la gente en el futuro. No es necesariamente el único esquema de autenticación; podría haber múltiples esquemas. Es modular. Todo tiene un cifrado de base, así que no importa lo que la gente haga encima en términos de autenticación.

¿Alguna pregunta sobre motivación, objetivos, historia o diseño? Creo que podemos entrar en algunos de los aspectos más técnicos sobre cómo logramos estos objetivos.

P: ¿Por qué es necesario el bit de servicio? ¿Probamos primero la v2 y luego la v1?

R: La idea es que nuestra propuesta tenga un bit de superficie que indique al iniciador de una conexión si debe probar v2 o no. La razón por la que queremos eso es que la alternativa es que un nodo v2 básicamente intente conectarse siempre a v2 e intente bajar de nivel. Creemos que el coste de latencia durante el despliegue, como cuando esta propuesta es nueva, casi todos los respondedores no soportarán v2 y el coste de necesitar dos conexiones es demasiado grande para un despliegue temprano. Tal vez podamos pensar en ello más adelante, cuando v2 se convierta en la opción por defecto.

P: ¿Es mucho más costoso que otro viaje de ida y vuelta?

R: ... además tienes problemas como que los nodos tienen un número limitado de ranuras de conexión entrante. Estás en desventaja como un nodo v2 tratando de hacer una conexión porque si al mismo tiempo alguien más puede... conseguirlo en el primer intento, entonces tú en el segundo.. pero.. por supuesto, un atacante en la red que ORs el bit de servicio v2 en cada otro mensaje puede probablemente desencadenar esto en la red a un coste bastante bajo de todos modos. Pero tal vez no.

P: ¿Es posible o práctico soportar otros protocolos en el mismo puerto? Por ejemplo, si sólo tuviera el puerto 443 con un servidor web seguro.

R: Creo que sí, que es posible. SSL es bastante identificable. Podrías tener un multiplexor de protocolos que dijera que parece SSL, así que lo reenviaría a mi servidor web, y si no parece SSL, lo reenviaría a bitcoin. Ya que es uniforme, necesitas algo donde todo lo demás coincida con algún fallback.

Eso es interesante, podrías ejecutar otro protocolo en paralelo. Especialmente si ambos son uniformemente aleatorios.

P: He notado que muchas VPNs permiten un numero de un digito de puertos en los cuales puedes escuchar.

Para ser claros, esto está diseñado como un esquema encriptado a nivel de paquetes. No lo es, esto no es un flujo encriptado. No es una interfaz basada en flujos. La interfaz de la aplicación son paquetes. Pero sólo estás pensando en ejecutar esto en TCP hasta ahora. Tenemos esta shapeability, por lo que tiene una capacidad como una aplicación para fragmentar sus paquetes arbitrariamente o rellenarlos con basura. Así se puede evitar que TCP tenga longitudes observables a nivel de cable.

P: ¿Han pensado qué forma de comparación utilizaría el identificador de sesión seguro? ¿Necesita un canal lateral seguro para evitar manipulaciones?

Se hace fuera de banda. Tengo dos nodos. Ejecuto getpeerinfo en ambos y luego comparo el ID de sesión. No hay protocolo. Si queremos un protocolo, entonces es un protocolo de autenticación. Pero este es un mecanismo que cualquier protocolo de autenticación usaría, al final compararía los IDs de sesión de una manera criptográficamente segura.

# Especificación: capa de transporte

Como dice, cuando se establece una conexión v2, y no se envía nada más. No hay paquetes, no hay mensajes v1 intercambiados ni nada. Lo primero que se transmite es .... la especificación tiene una capa de transporte, que es el grueso del BIP es ¿cómo establecemos claves de encriptación? ¿Cómo creamos mensajes cifrados? ¿Cómo los verificamos? Casi todo está ahí. Luego, la capa de aplicación es cómo enrutamos los comandos de los mensajes bitcoin a través de esa capa de transporte. La señalización es entonces sólo usando el bit de servicio. Casi todo de lo que hablaremos está en la capa de transporte. Ahí es donde está la criptografía.

Hay dos partes. Las llamamos iniciador y respondedor. Empezamos con un intercambio de claves. Lo primero que pasa por el cable no es exactamente una clave pública; no es una clave pública con una codificación normal. Si envías una clave pública, serías capaz de reconocerla. Incluso si sólo envías la coordenada x de un punto de la curva elíptica, podrías comprobar si está en la curva o no. Incluso el hecho de que, un atacante puede observar; "bueno, he visto 30 conexiones salir de este nodo y los primeros 32 bytes de ellos son siempre coordenadas x válidas en la curva secp, que sólo tiene una probabilidad de 1 entre mil millones". Derrotamos eso usando un esquema llamado [Elligator Swift][Elligator-swift-paper] que es un documento reciente que salió pero es una forma de codificar claves públicas en 64 bytes uniformemente aleatorios. Hay una representación sobrecompleta. Cada secuencia de 64 bytes codifica una clave pública secp. Mientras puedas decodificarlos, está bien. Esto es bastante nuevo y no estaba en el BIP original. bip324 usaba originalmente claves públicas sólo x. Cambiamos a ElligatorSwift para dificultar su identificación.

Además, queremos evitar el patrón de 64 bytes y luego esperas. Así que queríamos un mecanismo para stuff-padding las claves públicas también. Para el esquema de encriptación posterior, una vez que se establezca un canal que será más fácil. Pero durante el hanshake se necesita algo especial.

P: A alto nivel, ¿cuál es el beneficio de ElligatorSwift sobre el anterior?

R: Es más rápido de codificar y más rápido de descodificar. Implementó el primero y luego salió ElligatorSwift. Encontré algunas optimizaciones e informé a los autores. Utilizaron algunas de ellas en ElligatorSwift. Es significativamente más simple, y es más rápido.

Para vencer este patrón de 64 bytes y 64 bytes y luego empieza; a ambas partes se les permite añadir a su clave pública hasta 4 kilobytes de datos basura. Después de esa basura, envían lo que llamamos un "terminador de basura". El terminador de basura se deriva de la clave compartida. La idea es que ahora puedo enviar mi clave pública y mi basura, y aún no he recibido la clave pública de la otra parte, así que aún no puedo enviar mi terminador. De hecho, aún no sé cuál será el terminador. El terminador tendrá que ser un secreto compartido porque, de lo contrario, el atacante puede calcularlo y verlo. Así que el terminador de basura es un fijo de 16 bytes y escanear el bytestream hasta que lo encuentres. Pero se deriva del secreto compartido. Estamos buscando una cadena calculada fija en la basura. Puedo enviar mi basura, y ni siquiera sé cuál será el terminador. Obtengo la clave pública del otro lado, y ahora puedo enviar un terminador. Ambas partes pueden hacer esto y rompes la propiedad de que ninguna parte... así que sin esto, tendríamos la propiedad de que ninguna parte puede enviar más de 64 bytes antes de haber visto 64 bytes. Pero con esto, cada parte puede enviar hasta 4 kilobytes sin haber visto 64 bytes.

P: ¿Recomienda enviar más basura antes de enviar el terminador?

R: Podría, pero en realidad no es necesario. En cuanto hayas establecido las claves, puedes utilizar nuestro otro mecanismo de conformación, que es mucho más flexible. Pero podría, sí. De hecho, una versión anterior lo utilizaba antes de que reconociéramos que era innecesario.

P: ¿Entonces el respondedor tiene la libertad de enviar más basura? Sólo el iniciador... ¿el respondedor ya tiene ambas claves?

R: Buena observación. Tal y como está escrito el bip, en realidad no hay razón para que el respondedor utilice el mecanismo de la basura. Tan pronto como el respondedor responde, tiene una clave compartida. Inicialmente teníamos esto sólo para el inititaor, sin embargo consideramos la posibilidad de tener más tarde relajar parte del flujo de bytes y permitir al inititaor enviar menos de 64 bytes inicialmente e introducir activamente más rondas en la negociación. Para que eso sea posible, necesitamos que ahora el respondedor pueda responder antes de haber visto la clave pública completa del iniciador y por eso también por razones de simetría es un poco más fácil hacerlo en ambos lados. Nos permitiría actualizar este protocolo o tener una extensión retrocompatible en la que enviáramos 20 bytes como mi clave pública o algo así. Pensamos que la complejidad adicional está bien porque la tenemos en el lado del iniciador de todos modos, y ahora está en el lado del respondedor.

El número de 4095 bytes se establece básicamente por razones de DoS. Puede ocultar el número 64. También es un cuadrado. En el futuro, quizás los paquetes grandes podrían ser un valor por defecto. Pero seguramente esto es mucho más grande de lo que el paquete medio puede ser en el enlace medio.

Así que ambas partes envían una clave pública. Ambas partes esperan la clave pública. Como respondedor, si ves la magia v1, .. ves que el protocolo v1 comienza con los 12 bytes y es suficiente. Son 4 bytes de magia de red, seguidos por la versión y un byte 0, .. ¿no es eso observable? ¿Que el respondedor actúa así, sólo responde si hay un byte que no coincide con el...? En teoría sí, pero son 2^(-96) los que coincide lo cual es tan bajo que no merece la pena tenerlo en cuenta. La cuestión sin embargo es que podrías mirar algunas acciones del respondedor y ver mirando los primeros bytes que recibió y cuando responde. Sí, pero normalmente, el iniciador envía 64 bytes de clave pública más basura, todo al mismo tiempo. Un fisgón no puede saber oh empezaste a enviar en cuanto viste este byte porque el receptor recibe todo el paquete a la vez y reacciona o no reacciona. Un atacante activo también puede ir byte a byte.

Así que ambos reciben la clave pública completa de 64 bytes... usan ECDH sólo x porque es más rápido, pero ha habido mucha discusión sobre las claves sólo x cuando se trata de firmas Schnorr, pero para ECDSA es otra historia. No añade más seguridad hacer más que x-only. Así que derivamos un montón de claves de cifrado, dos en cada dirección, los terminadores de basura.... Esto es lo que el terminador de basura se vería en la naturaleza, gracias a Greg y su configuración de difusión estable para hacer esto. Creo que le llevó 15 minutos. Es una ilustración de un terminador de basura criptográfico. Tal vez cambió el mensaje para incluir bitcoin, pero no lo creo. Trending en Art Station.

Usamos HKDF-SHA256. Es un mecanismo muy estándar de convertir un montón de entropía en claves privadas. No es el más rápido del mundo, pero es robusto.

A continuación, envían su terminador de basura, y luego la otra parte espera por eso. Queríamos una propiedad que cualquier byte que un atacante activo cambie en el cable cause desconexión o pueda ser detectado. La basura se envía antes de que haya un secreto compartido. Nuestra solución es que después de que se haya enviado la basura, ambas partes se comprometan con la basura que han enviado para asegurarse de que todo el mundo está de acuerdo. Así, incluso si el atacante cambia un bit en la basura, la conexión terminará. Por razones similares, la codificación ElligatorSwift de las claves públicas va en la derivación de la clave compartida de modo que incluso si un atacante va huh me pregunto si esto es ElligatorSwift y lo decodifica en una clave pública y lo codifica en otro ElligatorSwift para la misma clave pública que todavía causará la desconexión por la misma razón.

En este punto, ambas partes tienen las mismas claves, y toda la comunicación posterior adopta la forma de paquetes cifrados.

P: ¿Podrías eliminar el paquete de autenticación utilizando la basura como parte de la derivación? Sé qué basura te envié, así que estaría esperando algo.... Ambas partes saben qué basura se envió y cuál recibieron, y si la utilizan en la derivación de sus claves, podrías utilizarla como autenticador. El problema es que esto necesita dos pasos: para enviar el terminador de basura, necesitas ambas claves públicas. Quiero decir, la derivación de las claves de encriptación después, sin embargo. La derivación del terminador basura, eso sería menos eficiente porque por cada byte necesitarías ..... Pero si lo usas para las claves de cifrado que derivas, creo que esto es lo que estás preguntando, esto funciona. Argumenté que lo que hacemos es un poco más limpio desde el punto de vista de la estructura criptográfica pero creo que funcionaría sí.

Un diseño un poco anterior era que no teníamos el paquete basura, pero actualizaríamos las claves de encriptación después de hashing ambas identidades.

Una ventaja de eso es que si hay un error en el código que realmente verifica esto, creo que te darías cuenta si es una actualización o un paso que alguien tiene que implementar para hacerlo bien. Una sutil diferencia. Desde un punto de vista de ingeniería criptográfica, creo que esto es más claro porque ya tienes claves compartidas y tienes un mecanismo de autenticación así que por qué no usar este mecanismo de autenticación.

¿La desconexión inmediata tras una infracción revela algo? Posiblemente. Hay una señal en la desconexión y cuándo hacerlo. Pero es lo mejor que podemos hacer; queremos la propiedad de que en cuanto un atacante se meta con la conexión, la desconectemos. Podríamos seguir enviando datos basura. Así es como esperamos que funcione la autenticación: si quiero hacer una conexión deliberada a un determinado nodo y falla la autenticación, entonces probablemente deberíamos tratarlo como un nodo aleatorio, o no ofrecerle servicios extra, o dar al usuario una advertencia. Podemos mantener la conexión, porque no es peor, así que tal vez. Es natural, sin embargo, terminar las conexiones y no enviar datos. Sin embargo, un atacante activo siempre puede aprender algo. Si modificas un bit en la basura, la conexión sólo terminará después de que los terminadores de basura hayan sido enviados. Podrías ser capaz de aprender la longitud del último mensaje que se envía.

P: ¿El paquete de autenticación basura tiene toda la basura en él?

R: Se compromete a ello. Usamos el ADA y sus datos asociados. Es un paquete vacío con los datos adicionales que se autentican.

# Fase de negociación de la versión

La especificación es que ambas partes envían un mensaje vacío. Reciben un paquete de la otra parte, y luego lo ignoran. Esto me sorprende que sea suficiente. Pero realmente la noción es que pensamos en este paquete como si codificara un número de versión. La versión que se utiliza es la más baja enviada por ambos. Codificamos cero como vacío, y como sólo admito cero, lo que envíe la otra parte también será cero. Así que la especificación es que envías un paquete vacío, y recibes un paquete y lo ignoras. La semántica para futuras versiones puede cambiar si el otro lado envía algo que no esté vacío.

¿Lo que esto implica es que realmente esperas que las actualizaciones de versión sean algo lineal? No necesariamente. Al no especificar cuál sería la codificación de ese número de versión, entonces es igualmente posible interpretar este mensaje como un fac.... aplazamos cómo funciona eso para el futuro, donde puede o no ser necesario.

Además, aquí se puede optimizar combinando uno de estos con el paquete de autenticación basura. En la práctica, toda la configuración de negociación de clave, basura, y autenticación basura y negociación de versión es de 1,5 viajes de ida y vuelta si combinas todo lo que puedas.

# Fase de aplicación

En la fase de aplicación, cualquier mensaje futuro enviado después del descifrado es entregado a una aplicación e interpretado como mensajes bitcoin p2p. Nos saltamos los paquetes señuelo aunque.... en cuanto se establecen las claves de encriptación, todo lo que se envía toma la forma de un paquete encriptado. Hablaremos de lo que sigue. Un paquete encriptado es un cifrado de una cadena de bytes de longitud variable, con una bandera booleana para ignorar. Si tiene la bandera de ignorar, entonces el receptor simplemente lo desecha. A estos paquetes los llamamos "paquetes señuelo". Curiosamente, esto ocurre antes de la fase de negociación de la versión. Incluso durante la negociación de la versión, la gente puede enviar paquetes señuelo para rellenar sus datos. No especificamos cómo y cuándo enviar paquetes señuelo, pero sí que un receptor tiene que ignorarlos. El tamaño mínimo de un paquete señuelo es de 20 bytes.

P: ¿Se puede introducir otro protocolo en los paquetes señuelo?

R: Posiblemente.

P: ¿Tamaño máximo de un paquete?

El tamaño máximo del paquete es de 16 megabytes (¿60 megabytes?). En una versión anterior, este bit de ignorar y la longitud se enviaban simultáneamente en un único campo de 24 bits, por lo que sólo había 23 bits para la longitud. El bit de ignorar no forma parte de la longitud, por razones de seguridad. En realidad, sólo debería figurar la longitud. Podemos llegar hasta 16 megabytes, pero en realidad no debería hacerse.

P: En la negociación de versiones, ¿se aplica también a la capa de aplicación?

R: Sólo a la capa de transporte.

P: Entonces, ¿puede haber otra negociación de versiones en la capa de aplicación?

R: La noción de versión o verACK no cambia. Lo único que tenemos es que el mensaje de comando a los 12 bytes se abrevia a 1 byte al tener una tabla que especifica un mapeo para los comunes.

P: ¿Entonces la distribución de la longitud del paquete es controlada por la aplicación por la basura?

R: La basura es sólo para las claves públicas. Es algo que se configura una sola vez. Después de los primeros 64 bytes, hay hasta 4 kilobytes. Después de eso, hay mensajes señuelo que puedes usar en lugar de variar la longitud.

P: ¿Hay alguna razón para usar paquetes señuelo en lugar de tener bytes extra que ignorar después de cada paquete?

R: Es similar.

P: ¿Podría usarse el señuelo para dejar una señal como si quisieras envenenar estos canales?

R: De hecho, puedes... el mecanismo de cifrado que utilizamos permite elegir el texto cifrado si no te importa cuál es el texto plano correspondiente. Esto puede ser un beneficio, o una maldición. Así que alguien podría usarlo para hacer que el protocolo parezca otra cosa. El beneficio es que alguien podría usarlo para hacer que el protocolo se parezca a algo. Creemos que puede ser posible crear un flujo TLS v1.3 válido pero algo extraño que sea en realidad bip324. Sería criptográficamente indistinguible de TLS v1.3. Parecería una conexión TLS v1.3 potencialmente válida. Para emular TLS, una cosa que usted podría hacer es simplemente correr con TLS, pero eso viene con todas las desventajas de todos los certificados y tal.

# Visión general del cifrado de paquetes

Una característica especial de nuestro protocolo comparado con otros protocolos de canal seguro es que queremos este bytestream completamente pseudoaleatorio. En otros protocolos, normalmente tienen la longitud del paquete en el cable. Cuando empiezas a enviar el paquete, el receptor no sabe cuándo parar de leer y descifrar. Necesitas un medio para comunicar al otro lado dónde termina mi paquete. Si te fijas en TLS, envían un prefijo de longitud y luego el texto plano. Una alternativa es enviar la longitud cifrada y autenticar la longitud. Creo que esto es lo que utiliza el protocolo lightning. Esto es bastante caro porque ahora estás enviando un par de bytes para codificar una longitud, y luego una etiqueta de autenticación de 16 bytes sobre ella. Argumentamos que debido a la naturaleza del protocolo bitcoin p2p que se basa en gran medida en la consulta-respuesta, muchos de los mensajes en el protocolo p2p provocará una respuesta instantánea de la otra parte, y así tratamos de argumentar que la autenticación de la longitud no ayuda .... Bueno, primero, autenticar la longitud no es necesario como lo hace lightning porque de todas formas la longitud se autentica visiblemente. Si envías un paquete de longitud que dice que el siguiente paquete encriptado y autenticado es de 16 bytes; si lo modificas a 15 bytes lo leerían, intentarían desencriptarlo y fallarían, así que está implícitamente autenticado, por lo que no necesitas añadir autenticación a la longitud.

De todos modos, ¿qué esperamos conseguir cifrando la longitud? Desde la perspectiva de un atacante pasivo, es sencillo. Queremos algo que sea uniformemente aleatorio. No necesita ningún tipo de autenticación porque un atacante pasivo no puede modificar eso. Pero, ¿qué intentamos ocultar a un atacante activo? Podemos esconder longitudes de un atacante activo. Un atacante activo, incluso uno que no cambie ninguno de los bytes, podría filtrarlos, como recibir un paquete de un lado y luego cada segundo liberar un byte de él y esperar hasta que llegue una respuesta, y una respuesta llegará tan pronto como el paquete haya terminado. Así es como un atacante activo puede averiguar la longitud. Nuestra postura es que es imposible evitar que un atacante activo se entere de la longitud de los paquetes.

P: En algo basado en UDP, cuando se dice que hay que filtrar el paquete byte a byte, lo que se está diciendo es que hay que tomar los paquetes TCP y reorganizarlos. Esta discusión podría ser diferente en UDP.

R: Es cierto.

P: ¿Y si en lugar de los paquetes señuelo, tenemos la longitud extra y esperamos hasta que se reciba esa longitud extra para evitarlo?

R: Creo que lo que sugieres es que cada paquete tenga dos campos de longitud. Uno de longitud legítima y el otro de longitud de relleno. Entonces sólo se respondería después de haber recibido y autenticado ambos. La desventaja de esto es que para alguien que no quiere usar señuelos, estos son datos extra. Para alguien que quiere usar señuelos, es menos porque ahora puedes tener señuelos de tan sólo 3 bytes o incluso 1 byte en lugar de 20 bytes. Y potencialmente al principio puedes negociar si quieres usar los señuelos. Hay muchas otras posibilidades como, por ejemplo, podría imaginar una extensión en la que tienes una función de solicitud-declamo en la que yo envío los paquetes que piden a la otra parte que envíe el señuelo a cambio. Precisamente porque el protocolo se basa en la consulta-respuesta, esto tiene grandes riesgos, ya que se necesitan fuertes protecciones contra el envío constante de un megabyte de datos señuelo a tu nodo.

P: ¿Hay alguna situación en la que el atacante está buscando una respuesta a un paquete, siempre se puede enviar un señuelo en primer lugar, y una vez que se filtra a través de entonces ir y actuar en consecuencia. A veces puede que quieras enviar un señuelo sin un paquete. Yo podría enviar un señuelo y luego fingir que respondo.

R: Sí, ése es un buen argumento para no querer que los señuelos se asocien sólo con paquetes legítimos. Porque a veces sólo quieres enviar un señuelo. Pero lo que podrías hacer es enviar un paquete con longitud exterior 20 y longitud interior y decir... 0 es ignorado. Sí, eso es justo. Es sólo una generalización del mecanismo de ignorar. Pero tiene un coste extra de dos bytes. Es una idea interesante.

Nuestro diseño se basa en gran medida en el cifrado ChaCha20Poly1305 de OpenSSH. Tomas ChaCha20Poly1305 del RFC. Muchos protocolos lo usan. Lo usas para... hay un byte de cabecera que incluye el byte de ignorar y algunos bits reservados, y luego la carga útil. Entonces tomamos esta cosa, y le ponemos un prefijo con una longitud, con una longitud encriptada independientemente. Y también una clave derivada de forma independiente sólo para asegurarse de que si usted está creando un oráculo de descifrado de esto, porque no es perfectamente..... La mayor prioridad es la confidencialidad para todos los datos enviados por el cable. Noise lo utiliza. WireGuard lo utiliza exclusivamente. TLS la utiliza. SSH utiliza el truco de las dos claves diferentes, pero no TLS. Puedes usar una clave separada para el cifrado de longitud, tomamos esa idea de SSH pero la modificamos un poco. Lo que hacen es tomar dos claves de cifrado .... pero luego su etiqueta de autenticación se calcula utilizando la clave de contenido, pero cubre la otra por lo que no tienen esta separación perfecta y para nuestro diseño podemos argumentar que se puede pensar en esto como dos capas separadas. La primera capa es para cifrar el contenido con un contenido completamente estándar de cifrado autenticado, y luego el prefijo de las longitudes de cifrado a la misma. Por eso generamos las dos claves al principio. Otra cosa es que su protocolo es más pequeño porque para el cifrado de longitudes usan una llamada ChaCha entera. Así que generan 64 bytes de bytestream aleatorio y toman 4 bytes de él, que en nuestro caso serían 3 bytes y tiran los otros bytes, lo que no es un uso muy eficiente de los bytes aleatorios.

P: Así que comparado con el BIP original, el cripto fusionado hace unos 2 años no ha cambiado. ¿No hay criptografía nueva?

R: Bueno, sí especificamos lo que ha cambiado... el cifrado de longitud ha cambiado. Pero ya hemos fusionado ChaCha20Poly1305. No estoy seguro de lo que hay en el código base de Bitcoin Core. AEAD fue fusionado. Todavía los tenemos. Había capas encima de las que solían estar ahí y esas capas adicionales han cambiado.

# Más

Hay un bonito diagrama para todo el protocolo handshake. Aquí tenemos el algoritmo XElligatorSwift. Así es como derivamos los secretos. También tenemos una implementación ingenua en python. La especificación entra en las decisiones de diseño sin especificar todo al nivel de byte, pero el pseudocódigo maneja todos los detalles.

# Application layer message encoding

# Codificación de mensajes de la capa de aplicación

En lugar de enviar cadenas ASCII como "version" u otras cosas, tenemos esta tabla para identificadores de tipo de mensaje. Enviamos un byte y si ese byte tiene un valor de 1 a 12 entonces... si el valor del primer byte está entre 1 y 12 inclusive, entonces tratamos todos los bytes que siguen como una cadena ASCII porque alguien podría necesitar enviar algo que no está en nuestra tabla. Otro BIP podría introducir un nuevo mensaje. Esto podría añadir otro byte en la tabla. Entonces, ¿por qué ASCII? Podríamos suprimirlo por completo... pero es por compatibilidad con ..... Hay una cuestión de coordinación. ¿Seremos capaces, para cada PIF futuro que introduzca nuevos mensajes, de asignar de forma única un ID de un solo byte sin problemas de coordinación? Creo que es probable que podamos hacerlo, aunque no estoy convencido. Existe un mecanismo alternativo: si alguien tiene una extensión privada a la que no se le ha asignado un número o lo que sea, puede seguir utilizándola. Me parece que se podría definir un byte como que significa eso, de modo que se pueden ahorrar 11 bytes. Usted podría hacer eso. Si ves este 1 byte, entonces lee la longitud y luego lee el mensaje ASCII. Otro enfoque es enviar tu tabla. Para los bits de servicio, podrías definir un rango de bits de servicio para experimentos y si eliges algo esperar que funcione. Dejamos la tabla de mensajes por si acaso. Podrias notar que la tabla de mensajes esta mayormente ordenada alfabeticamente excepto los bips que fueron agregados mas tarde si te fijas.. Tal vez el tipo de mensaje debería depender de la longitud del mensaje. Podríamos hacer eso, ese es el truco de PHP, ¿verdad? La tabla de búsqueda basada en el byte y el último byte basado en la longitud del comando que es por lo que los primeros comandos PHP son raros. Es cierto que funciona, y podríamos hacer que la tabla de búsqueda se basara en el byte de codificación y la longitud.

P: Establecer un canal que esté encriptado y autenticado suena como una idea simple, pero históricamente esto suele salir mal. Estos otros protocolos suelen tener una autenticación real que sólo es efímera, pero también tienes este requisito adicional de que quieres que el flujo de bytes sea indistinguible del aleatorio. ¿Por qué crees que todo eso funciona? ¿Deja claro el BIP qué partes son estándares y quizás incluso tienen una prueba de seguridad y demás, y qué partes son personalizadas?

R: Quizá sea más fácil responder primero a la segunda pregunta. Creo que el material estándar, todo el material simétrico es muy estándar. El núcleo del cifrado. La derivación de claves es estándar. Excepto el cifrado de longitud. Aquí argumentamos que si esto falla, todavía tenemos la parte interna, y es bastante fácil argumentar sobre que no hemos escrito una prueba pero otras personas han mirado en ocultar la longitud. Hay literatura sobre esto llamado "bondable hiding" sobre ocultar el número de paquetes en un flujo. Esto de openssh se ha demostrado seguro, y nos desviamos de ello, y argumentamos que la desviación es minúscula. Nos gustaría ver más investigación sobre eso, pero estoy lo suficientemente seguro de que nuestras modificaciones están bien allí. Es bueno saber que las cosas openssh se sabe que es seguro.

La otra parte en la que tenemos cosas nuevas es como la de Elligator. La única propiedad de seguridad real son los bytes pseudoaleatorios.. si esto realmente falla entonces fallamos en establecer bytes pseudoaleatorios, lo cual es malo pero no es el fin del mundo. La otra propiedad de ElligatorSwift es que es una codificación correcta. No necesitas una prueba de seguridad para esto, puedes simplemente escribir pruebas. Toma las ecuaciones para la codificación y sustitúyelas para la decodificación y verás si funciona.

Sobre la parte de la uniformidad... El documento ElligatorSwift tiene una prueba que establece un límite en lo uniforme que es. Hice pruebas exhaustivas para pequeñas curvas para verificar su límite. Y funciona. Es mucho mejor de lo que su límite dice que debería ser. También es mejor que ElligatorSquare. Esto es difícil de hacer formal, pero es una función de 64 bytes de asignación a una sola coordenada x. Así que es el mapeo de 64 bytes a 32 bytes en un polinomio no trivial racional funcional manera. Sería extremadamente difícil que no fuera uniforme. Incluso si tal vez no fuera tan uniforme como el documento lo demuestra, incluso si su prueba es ... Me costaría mucho convencerme de que no es uniforme porque mapear algo real más grande a algo más pequeño....

¿Escoges 64 bytes al azar y obtienes una clave, o escoges una clave y luego obtienes 64 bytes? No, eliges los primeros 32 bytes y deduces los segundos 32 bytes de tal forma que codifique tu clave objetivo. Como empiezas con menos de 64 bytes, supongo que hay algún ataque computacional en el que puedes hacer un ataque de búsqueda de cada clave. Es una tabla 2^512... pero desde un punto de vista criptográfico teórico, esto es una vulnerabilidad. No. Estás mapeando 32 bytes a 64. Hay aleatoriedad adicional en ello, sin embargo. Dada una clave pública uniformemente aleatoria como entrada, la salida del algoritmo es en realidad 64 bytes uniformemente aleatorios. ¿Porque estás añadiendo más aleatoriedad? Así que no es un protocolo determinista. Vale, está bien. Pero podría serlo. Podrías usar la clave privada como tu aleatoriedad para el codificador, y curiosamente sólo hay 2^32 codificaciones pero sigue siendo computacionalmente indistinguible de uniforme.

Hay protocolos de canal seguro que históricamente han fallado. Hay un montón de lugares, como tal vez en el cifrado autenticado. Espero que la comunidad literaria haya entendido que ya sabemos cómo hacer cifrado autenticado. Otro lugar donde esos fallan es mucha complejidad de estado y muchas máquinas de estado como el estado incorrecto de la conexión o algo así. Aquí, mira el protocolo y convéncete de que es simple. Tratamos de evitar tener alta complejidad de TLS como donde puede hacer la reanudación de sesión y diferentes formas de autenticación. No tenemos noción de suites de cifrado porque eso es una enorme fuente de ataques de frontera. No hay agilidad criptográfica. Algunas de estas cuestiones se vuelven más relevantes una vez que se añaden extensiones; digamos que se ha añadido la negociación de clave post-cuántica y ahora quizá haya que preguntarse por un atacante que pueda provocar una degradación para que no se haga. Ahora mismo no hay espacio para la negociación de parámetros de conexión.

# Añadir autenticación

P: ¿Podría explicar brevemente cómo añadiría la autenticación?

R: Quizá deberíamos hacerlo más tarde, después de la sesión. Ésta ha sido una sesión larga.

P: ¿Está definido cómo tratan los clientes y los pares los tipos de mensajes indefinidos?

R: Es lo mismo que... ahora mismo se discute cómo se maneja. La gente de libbitcoin termina la conexión. Nuestro BIP no se ocupa de esto. Lo trata como un mensaje que no se sabe. Tal vez debería lanzar un mensaje diciendo que los tipos de mensajes desconocidos deben ser ignorados. Bitcoin Core los ignora, libbitcoin no. Hay alguna disputa al respecto. btcd desde hace poco creo... lo cambiaron a por lo menos antes de la verACK ahora ignoran los mensajes desconocidos. Alguien acaba de escribir un BIP para ignorar todo antes de verACK. btcd lo ignorará porque es un mensaje desconocido. Los bloques compactos no estan implementados en btcd.

No creo que debamos entrar en eso, la verdad. La cuestión de cómo manejarlos parece depender de si estás antes o después del verACK. Creo que nuestro BIP de encriptación de transporte no debería tener una noción de una vez que lo pasamos a la capa de aplicación.... pero antes de que puedas pasarlo, si obtienes un número de tipo de mensaje indefinido, ¿cómo traducirías eso a la capa de aplicación? Ah, eso es justo. Probablemente deberíamos especificar cómo al menos con respecto a, la posibilidad sería tratada como un mensaje desconocido, o desconectar, o ignorar. Esa es de hecho una pregunta separada de cómo se manejan los mensajes desconocidos en general.

Creo que esta cuestión realmente no debería ser una preocupación de este BIP. Los cambios que hacemos aquí en la tabla de tipos de mensajes... si cambias todo lo subyacente, tiene sentido poner el cambio encima porque necesitas otro mecanismo de negociación para cambiar a algo así.

P: Podría ayudar si este BIP pudiera dividirse en un esquema genérico de retransmisión de paquetes, y luego las partes de bitcoin. Alguien debería escribir una librería rust que sólo expusiera esta interfaz y absolutamente nada más.

R: La única razón para no hacerlo es porque la parte de la aplicación es tan pequeña que sería un BIP muy delgado. Sin embargo, no me opongo a dividirlo.

P: ¿Puede llevar mensajes para diferentes aplicaciones?

R: Lloyd, que participó anteriormente en el proceso de diseño, quería esa propiedad... no la tenemos, pero sería fácil añadirla porque ahora tenemos este byte de cabecera en el que se puede definir un bit en el byte de cabecera y decir que es ..... La propiedad que quería era que pudieras tener una conexión y luego multiplexar mensajes de múltiples aplicaciones a través de ella. Eso es relativamente fácil de hacer con este mecanismo de byte de cabecera donde se puede definir un bit.

P: Si tienes una conexión totalmente autenticada, podrías querer hacer JSON-RPC sobre la misma conexión.

R: Creo que hay razones por las que no querrías hacer eso porque JSON-RPC nunca querrías hacerlo sin autenticar. Si está autenticado persistentemente, vale, es justo.

[refrendar-sección-en-otro-transcripción]: https://btctranscripts.com/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/#countersign-a-secret-authentication-protocol
[Elligator-swift-paper]: https://eprint.iacr.org/2022/759.pdf

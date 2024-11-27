---
title: Cifrado P2P
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - v2-p2p-transport
  - bitcoin-core
date: 2019-06-07
aliases:
  - /es/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/
---
Cifrado p2p

<https://twitter.com/kanzure/status/1136939003666685952>

<https://github.com/bitcoin-core/bitcoin-devwiki/wiki/P2P-Design-Philosophy>

"Elligator al cuadrado: Puntos uniformes en curvas elípticas de orden primo como cadenas aleatorias uniformes" <https://eprint.iacr.org/2014/043>

# Introducción

Esta propuesta lleva años en marcha. Muchas ideas de sipa y gmaxwell fueron a parar al bip151. Hace años decidí intentar sacar esto adelante. Hay bip151 que de nuevo la mayoría de las ideas no son mías sino que vienen de sipa y gmaxwell. La propuesta original fue retirada porque descubrimos formas de hacerlo mejor. Desde que la gente ha empezado a implementar el bip151, decidí no alterar esa propuesta porque acabaría con la confusión.

Así que he propuesto un protocolo de transporte de mensajes v2 para la red p2p. Esta es una oportunidad única para hacer las cosas mejor, creo. No quiero volver a llamarlo "encriptación p2p" porque tiene la oportunidad de hacer mucho más que añadir encriptación.

# Objetivos

Los objetivos son, de nuevo, añadir el cifrado oportunista; a veces me arrepiento de no haber añadido un esquema de autenticación en esa propuesta porque la gente todavía no está muy contenta con la posibilidad de ataques del hombre en el medio. Pero es un bloque de construcción, e incluir todo en una propuesta lo hace demasiado complejo y podría haber múltiples esquemas de autenticación y tal vez elegir uno no sea la mejor idea.

También es una oportunidad para optimizar el protocolo. El objetivo no es como la resistencia a la censura.  Es una encriptación oportunista, no para la resistencia a la censura. Tiene algunas buenas propiedades para resolver los observadores pasivos, pero aparte de eso es más bien un bloque de construcción. Además, elimina la manipulación de mensajes no detectables.

# Apretón de manos

Repasemos cómo funciona. Este es el resumen simple. La propuesta actual es que un iniciador envía una pubkey de `32` bytes sin ninguna cabecera de mensaje ni nada más, son sólo `32` bytes puros al respondedor. El respondedor lee los `32` bytes y luego detecta si se trata de un mensaje mágico de la versión `1`, y comienza con la versión de la magia. Si es así, entonces es un handshake del protocolo `v1`, entonces continúa con v1 porque todavía queremos usar `v1`. Si no contiene la magia en la versión, entonces trata los `32` bytes como un handshake. Entonces hace un `ECDH`, entonces él envía de vuelta su clave pública, y luego en el otro lado hacemos `ECDH` y tenemos un secreto compartido.

P: ¿Las claves públicas no son de `33` bytes?

R: Sí, son de `33` bytes en general. Sin embargo, sólo utilizamos pubkeys impares. ¿Por qué? Es una buena pregunta. La resistencia a la censura no es una propiedad. Creo que a gmaxwell se le ocurrió la idea de decir que si usamos `32` bytes sólo en las pubkeys, entonces parece aleatorio, no es aleatorio pero parece aleatorio. No es tan fácil de identificar. Ya no se puede hacer un análisis de tráfico ingenuo. Podrías hacer un análisis de tráfico más avanzado, pero no es sólo "coincide con estos bytes, oh es probablemente bitcoin". De lo contrario, el apretón de manos siempre sería obvio para los observadores.

P: ¿Cuál es el análisis de tráfico más avanzado?

R: Podrías ver si hay muchas conexiones desde una sola IP, y quizás todos los `32` bytes son buenas coordenadas x de la curva `ECDSA`, y si todas son coordenadas válidas entonces es más probable que esté usando este protocolo.

Además, no se permite que las pubkeys comiencen con magia, de lo contrario romperíamos la compatibilidad hacia atrás. Hacemos el handshake, y luego se utiliza el cifrado simétrico. `ECDH` es también algo que ya está disponible en `libsecp256k1`. Hacemos `ECDH` con nuestra curva `secp256k1` actual. No es una criptografía nueva en ese sentido.

P: En lugar de enviar una coordenada x, ¿sólo enviar aleatoriedad y hacer un hash?

R: Puedes codificar una clave pública en 64 bytes y entonces sí que parece aleatoria. No estoy seguro de que merezca la pena hacerlo, pero podría hacerse. Asignadores, ¿verdad? Sí. Vamos a hablar de eso más tarde. Probablemente no merezca la pena porque hay muchas otras cosas de análisis de tráfico que puedes hacer que son triviales para identificar el tráfico de bitcoins, como que todos los mensajes sean más o menos del mismo tamaño o tamaños predecibles. Tendrías que enviar un flujo constante de datos o algo así. El mayor análisis de tráfico es mirar el tamaño de los paquetes y la sincronización y correlación de los paquetes entre los nodos. A menos que vayamos a añadir paquetes basura para que el ancho de banda parezca constante, entonces no hay mucho que se pueda hacer ahí. Esto no es algo que estaría en el Bitcoin Core, pero tal vez algo más en la parte superior de Bitcoin Core. Bueno, entonces seríamos la única aplicación con un ancho de banda constante...

# Construcción personalizada de AEAD

Una vez que se tiene un secreto compartido después del apretón de manos, la propuesta es utilizar `ChaCha20Poly1305` para el cifrado simétrico, una construcción `AEAD` personalizada. ChaCha20 es el cifrado de flujo, y `Poly1305` es el MAC. Además, algunos dispositivos tienen elementos de hardware que realizan estas instrucciones. `ChaCha20` está fusionado en Bitcoin Core y `Poly1305` está fusionado.

# Tamaño del mensaje

P: ¿Qué hay del rendimiento entre eso y el hash del mensaje completo?

R: Esa es una buena pregunta, pasemos a eso. Recogí algo de tráfico durante un periodo de 24 horas en un nodo estándar, es decir, sirviendo bloques. Sin cambios en los parámetros de configuración. Ahí podemos ver que casi más de 1/3 de los mensajes enviados están por debajo de los `64` bytes. Lo que quiero decir con esto es que la mayoría de los mensajes son muy pequeños, y más de un tercio está por debajo de `64` bytes. Así que vale la pena optimizar los mensajes pequeños. Los pares de poda son un poco menos. ¿Esto se debe a que los nodos podados no sirven pruebas merkle? El INV sólo se dispara... por ahora. Eso es sólo btcflood.

¿Por qué es blocktxn tanto para Bitcoin Core enviar bytes de mensajes con prune durante un azar 9 horas? Este era un nodo de Bitcoin Core de larga duración. Esto es bytes enviados. Así que podría estar hablando con un peer que no tiene un buen mempool. La reconstrucción de bloques falla todo el tiempo, y si falla entonces van a ser muchos bytes más que bloques compactos, así que esa proporción podría tener sentido.

¿Tenemos estos números en getnetworkinfo? Si se desconecta de un peer, simplemente desaparecen. Esto es del registro de depuración.

Entonces, está claro que tenemos muchos mensajes pequeños.

# Rendimiento de AEAD

Hay una propuesta del IETF de `ChaCha20Poly1305` que es buena, pero luego OpenSSH tomó esa propuesta y la mejoró encriptando el campo de longitud. La propuesta del `IETF` tiene la longitud sin cifrar y es muy fácil identificar los paquetes. No se puede rellenar con datos aleatorios, es un poco más sencillo. Así que OpenSSH lo cambió un poco e hizo que el cifrado de la longitud fuera parte del campo AD. Tomamos eso y lo optimizamos aún más para los mensajes pequeños, que es sólo un ligero cambio. El cambio es visible aquí....  Esta es la versión openssh, hay un handshake, hay dos claves del handshake, hay una ronda `ChaCha20`, y luego derivamos la clave Poly1305, y luego hacemos n rondas `ChaCha20` para cifrar la carga útil. Una ronda `ChaCha20` es siempre de `64` bytes, por lo que hay que hacerla de todos modos. Así que se desechan `32` bytes de la clave `Poly1305`... pero para cada mensaje, hacemos una ronda `ChaCha20` para cifrar sólo `4` bytes de longitud. Así que no usamos `60` bytes de una parte computacional, son `4` bytes AD. En Bitcoin Core, reutilizamos ese flujo, por lo que podemos reducir una ronda `ChaCha20` para un mensaje de `64` bytes, o sólo tenemos que hacerlo una vez cada 21 veces. Lo raro en la salida de `ChaCha20` es que tiene un número variable de blobs de longitud variable que salen. Hay un IV que cuenta qué mensaje quiere, y luego hay un contador para los bytes dentro de eso. Parece que en el `ChaCha20Poly1305` de OpenSSH, básicamente no utilizan el hecho de que todos estos mensajes son de longitud variable, simplemente generan el nuevo mensaje y utilizan los primeros bytes. Parece más sencillo tratar `ChaCha20` como un cifrado de flujo y utilizar los bytes que salen. El cifrado de flujo es agradable, sólo almacena la posición de la cadena real del texto plano y podrías calcularlo por adelantado cuando no estés usando la CPU y luego almacenarlo cuando quieras cifrar. Puedes usar el tiempo de CPU no utilizado. Esta es la versión optimizada.

Entonces, ¿cuáles son los números? De nuevo, no he hecho miles de consultas. Es sólo una. Usé un `x86 i7-8700`, y otro en `AARCH64`. Comparé el hash (el doble hash existente), bitcoin, y OpenSSH. La versión actual es de `4` bytes de suma de comprobación en cada mensaje, y la suma de comprobación se calcula por doble hash sobre todo el mensaje y luego truncar todo a `4` bytes que no es super rápido. Por eso podemos hacer el protocolo más rápido añadiendo encriptación, lo cual es difícil de entender. Pero no siempre es más rápido.

Hacer hash de un mensaje de un megabyte lleva más del doble de tiempo. Así que son `3,8` milisegundos. ¿Qué es lo que reporta el banco, segundos? Hacer hash de un megabyte debería estar en un rango de milisegundos, sí. Concéntrate en la diferencia relativa en lugar de los números reales. Cifrar un mensaje de un megabyte lleva menos tiempo que usar el método de hash. En un mensaje grande, no nos beneficiamos contra OpenSSH. Pero en un mensaje de `256` bytes hay una diferencia, y un mensaje de `64` bytes tiene una diferencia aún mayor con OpenSSH y ambos son más rápidos que el método de doble hash.

La propuesta alternativa sería, no encriptar y dejar de lado `sha256.` No creo que sea una buena idea. Sin embargo, ha estado flotando en la lista de correo.

Para el rendimiento, se puede almacenar en caché `2` MB de flujo, para la propagación de bloques. Creo que en general el uso de `ChaCha20` tiene mucho potencial de optimización en el futuro.

# Estructura de mensajes v1 vs v2

Mensaje v1: `4` bytes de magia de red, `12` bytes de comando de mensaje, `4` bytes de longitud, `4` bytes de suma de comprobación `doble-sha256`, bytes variables de carga útil, y son al menos `24` bytes en total.

Mensaje v2: `3` bytes de longitud encriptada, `1-13` bytes de comando de mensaje, bytes de longitud variable de carga útil, `16` bytes de MAC (código de autentificación del mensaje), y son al menos `20` bytes en total.

Si quieres enviar con v2 algo que sea mayor de 8 MB, entonces tienes que dividirlo en paquetes, lo que sería una buena idea de todos modos. Hay que hacerlo de todos modos. Así que los bloques de gigameg, los troceamos. También nos alejamos del comando de mensaje de `12` bytes y utilizamos un único byte cero-12 que identifica la longitud, así que si el primer byte está entre 0 y `12` entonces significa una longitud y el resto es un valor codificado de longitud variable estándar. Si está por encima de `12`, entonces lo identificamos como un id corto, por lo que `13` podría ser INV, etc, pero esa tabla todavía tiene que ser hecha. Podemos usar un solo byte para enviar un comando en lugar de una cadena. Esta es una optimización general que no tiene nada que ver con la codificación.

Es `1` byte o `12` bytes. No queremos eliminar los comandos basados en cadenas. Si ya vas a tener la optimización para que la mayoría de los mensajes sean de un byte, por qué no tener un byte que diga que los siguientes `12` bytes son de comando.  Es un poco diferente. Eso significaría que siempre tienes que enviar `12` bytes... No, en realidad nunca harías eso a menos que estés enviando un mensaje personalizado. ¿No podemos añadir más cosas de longitud variable? ¿Qué tiene de malo la longitud variable? Esto reserva `212` IDs cortos. Añadir cosas de longitud variable es una mierda, en general, en cualquier protocolo. Es una optimización que no vas a utilizar nunca, lo que añade complejidad al protocolo. Así que podrías decir que `255` significa que los siguientes `12` bytes son de comando de mensaje... No vale la pena discutir esto. No quiero un parser que incluya cadenas de comandos de longitud variable. No quiero implementar eso. Realmente no lo quiero. Veo el punto, es razonable. Podemos discutirlo más adelante.

Usando el protocolo de mensajes v2, significa que los mensajes no son más grandes, incluso podrían ser más grandes debido al ID de comando corto.

P: ¿Realmente necesitamos una MAC de `16` bytes? ¿Podemos reducirla?

R: No deberíamos. Yo preferiría una MAC de `32` bytes. `Poly1305` es una MAC bien estudiada y tiene salidas de `16` bytes.

P: Bueno, yo no sé nada de criptografía.

R: Yo tampoco. ¡Enviémoslo dos veces! ((risas))

Podríamos decir que la versión 2 sólo admite INVs o algo así. Pero esto trae consigo una planificación especial. Lo bueno de las cadenas es que es menos probable que se produzcan colisiones. Alguien tiene que mantener la tabla de todos los mensajes p2p. Ya tenemos un apretón de manos y una negociación de versiones. No importa si alguien está haciendo otros mensajes p2p. De todos modos, no vamos a conectarnos a esos nodos raros, ¿verdad? Si usamos sólo bytes, entonces todo el mundo tiene que actualizar el BIP.

¿La longitud incluye la suma de comprobación y el tipo y todo eso? ¿O sólo el nombre del comando? La longitud sólo contiene la carga útil, sólo la carga útil. Así que tendrás que entender cómo analizar el tipo porque no puedo omitirlo. ¿Correcto? Tienes que leer el primer byte, y luego puedes omitir el resto. También tengo que apoyar el tipo de longitud variable. Necesitas leer los primeros `4` bytes para saber cuántos bytes saltar. La longitud encriptada puede necesitar ser el tamaño de todo el paquete, pero hay preocupaciones por tener un oracle..... de relleno. Esa es la razón por la que la longitud se cifra con un cifrado diferente, para evitar que la gente pueda inferir información de ella observando cómo respondes a los mensajes no válidos. Tenemos que pensar en eso. En la versión openssh, la MAC no está incluida en la longitud... claro, eso es fácil, pero para las cosas variables... Esa es una buena pregunta. Debería incluir el tamaño del comando del mensaje también. La MAC no importa, es de tamaño constante. Pero creo que la longitud debe incluir todo lo de tamaño variable. Así puedes empaquetar tu flujo descifrando los campos de longitud y no mirando nada más. Debe cubrir la longitud variable. Podrías encriptar los primeros cuatro bytes con un cifrado especial pero esto no es lo ideal.

En v1, INV es un mensaje de `61` bytes, y en v2 INV es de `57` bytes.

`3` bytes para la longitud, lo que da `24` bits. El bit más significativo se utiliza para desencadenar una nueva clave. Así que sólo podemos utilizar `23` bits. El único bit reservado desencadena una nueva clave, lo que significa que tenemos que utilizar la siguiente clave para el cifrado simétrico.

Los mensajes más largos podrían utilizar mensajes de varias partes, como gigabloques o lo que sea.

P: ¿Habéis hecho algún tipo de evaluación comparativa sobre la construcción del MAC?

R: Está en el código, si ejecutas el bench, te da las pruebas de `Poly1305`.

P: ¿Así que los gráficos que mostró incluían `Poly1305`?

R: Incluían dos rondas de `ChaCha20`. No es sólo `ChaCha20`, es todo, todo el cifrado de flujo. Compara el doble sha con la construcción AEAD.

P: ¿La MAC cubre el resto del paquete?

R: El AEAD es sólo la longitud encriptada, y el MAC va sobre todo, incluyendo el id. Es la carga útil y el comando, pero sí.

# Preguntas abiertas

Esta es una oportunidad para cambiar el protocolo. Si hay otras ideas, deberíamos incluirlas en la propuesta. Creo que deberíamos llamar a esto "protocolo de transporte v2" en lugar de llamarlo encriptación. La pregunta que Tim planteó ayer es, ¿qué necesitamos considerar ahora para no romper las futuras mejoras en términos de cuando se rompe la criptografía? ¿O los ataques a la baja? Aquí, empezamos enviando una clave pública, pero si es una cadena simétrica entonces retrocedemos a la v1, pero ahora lo primero que enviamos es básicamente aleatorio, así que qué pasa si en algún momento en el futuro queremos la v3. ¿Cómo hacemos esa actualización? Por el momento no es posible; ¿enviar claves pares? Si queremos añadir otro handshake, podríamos hacer ese handshake primero y luego hacer un segundo handshake. También tenemos la bandera de servicio. Podríamos añadir otro puerto. Ya soportamos la vinculación de múltiples sockets de escucha. La forma de hacerlo como una actualización es que si quieres hacer esta cosa v3, entonces primero haces el handshake v2, luego negocias usando mensajes v2 para hacer el handshake v3.

Por el momento, la propuesta parece un entre querer encriptación y debe parecer datos aleatorios pero no demasiado porque no queremos invertir demasiado ancho de banda. Normalmente los protocolos empiezan con lo que tenemos en este momento, como una cadena mágica, algún número de versión, y ahora hemos optimizado eso para que parezca aleatorio, y ciframos la longitud para que parezca aleatorio. El IETF no encripta la longitud porque asume que la longitud del mensaje debe ser visible o no necesita ser confidencial. Al principio enviamos una coordenada x, que todavía podría ser distinguida. Creo que deberíamos optar por claves públicas de `64` bytes para que sean realmente... entonces todo el protocolo parece datos aleatorios, excepto que se puede hacer un análisis de tráfico como el tiempo y la longitud. O acolchamos las cosas. O decimos que esto no es un objetivo, y podemos tener otra cadena mágica, y no tenemos que cifrar la longitud, y tener un número de versión. Deberíamos elegir cuáles son los objetivos.

Definitivamente hay algo intermedio... hay una diferencia entre poder hacer un análisis de tráfico trivial en el que coincides con los primeros cinco bytes y sabes lo que es, frente a tener que poner cierta cantidad de CPU para averiguar si se trata de tráfico de bitcoins. Esta es una gran diferencia para muchas aplicaciones prácticas.

Hay algunas cohones. Tal vez no nos interese el análisis del tráfico, tal vez todo sea aleatorio, y tal vez le parezca aleatorio a un observador con restricciones de CPU. Creo que el observador limitado por la CPU es el modelo de amenaza más importante. Tan pronto como se realiza el intercambio de claves, todo parece realmente aleatorio, así que ¿por qué no coger esta fruta fácil de añadir más bytes en el apretón de manos? Bueno, podrían simplemente ver que tu tráfico se dispara después de recibir un bloque de bitcoin y, por lo tanto, que estás ejecutando bitcoin.

En términos de actualización, no subestimes hacer un nuevo puerto y que ese sea el nuevo protocolo. De lo contrario, estarás haciendo TLS y empezarás con TLS. En bitcoin, no hay razón para no seguir vinculando nuevos puertos para cada protocolo que queramos. Podríamos decir `8336` asumimos que es v2... ¿Qué pasa si la gente quiere usar un puerto diferente? No hay razón para no usar un puerto diferente. Si no puedes enlazar el `8336`, no puedes enlazar otra cosa. Si un país bloquea el `8333`, no puedes iniciar un nuevo nodo. Haces una semilla DNS, todo es `833x`, no puedes conectarte.

Puedes hacer un DDoS anunciando un montón de servicios, entonces todos los nodos intentan conectarse y hacen conexiones aleatorias a ese servicio. Yo tengo un nodo bitcoin que usa un puerto no estándar, y literalmente nunca ha recibido una conexión legítima de un nodo Bitcoin Core. Si usas el mismo puerto, entonces todo esto del análisis del tráfico no sirve de nada. Tienes que permitir números de puertos únicos.

¿Sería útil reutilizar los `32` bytes superiores de esa ronda `Poly1305`? ¿Para encriptar la carga útil? Sólo para crear la clave `Poly1305.` Siempre tiramos esos `32` bytes. Siempre y cuando no lo mezcles con la otra clave; tienes que mantener las dos cosas separadas. `ChaCha20` solo te da todos los números aleatorios que quieras. La propuesta de openssh es una estupidez al tirar esas cosas... Creo que fue una elección de implementación que redujo un par de bytes de estado que habrían tenido que seguir, es un contador para un mensaje y eso es todo lo que necesitas. Lo hizo un poco más rápido, pero no sustancialmente. Puede que intente implementar algo ahí.

# Próximos pasos

`ChaCha20` ha sido fusionado. `Poly1305` ha sido fusionado. La construcción AEAD ha sido solicitada. Tiene vectores de prueba, tiene banco, es estable. Necesita una revisión total por parte de la gente de criptografía. No es una criptografía nueva, pero es una construcción nueva. No es como caminar en un lago congelado, pero sigue siendo similar a caminar en el hielo. Necesita más revisión y coger impulso. Tiene una implementación completa. Funciona, aunque no es buena.

Después del apretón de manos de la versión, se envía el mensaje de la versión. Después del mensaje criptográfico, sí.

Como alternativa al uso de la construcción elegator square de `64` bytes, se podría permitir enviar un número de coordenadas x no válidas antes de la coordenada x real y entonces se utiliza una distribución de poisson para esto. Lees `32` bytes, si es una coordenada x válida, yay go, y si no la saltas y continúas. Creo que esto realmente parece aleatorio. Lo triste de esto es que terminas con cosas en los límites de `32` bytes que también son identificables. ¿Por qué no elegator al cuadrado?

Una de las propiedades debería ser que tenemos una dependencia en términos de tener bibliotecas externas o algo..... No creo que eso sea necesario, y además complica.. no todos los proyectos que quieren implementar protocolos p2p tienen los mismos recursos para desarrollar. Lo añadiríamos a libsecp256k1 si hacemos eso.. Sí, eso es cierto. Hay más preocupaciones que sólo "podemos implementarlo".

Hacer que parezca aleatorio no es un objetivo tan importante, especialmente si nos esforzamos y dejamos el puerto igual. Parece claramente una jugada descabellada. Esto es lo que se detecta ahora. Si corres en ese puerto, recibes correos electrónicos. Esto es lo que se detecta para "Quiero identificar a la gente que ejecuta Bitcoin pero no estoy tratando de bloquear a la gente que ejecuta Bitcoin". Este es un paso muy fácil, sólo tienes que bloquear el puerto `8333` entrante. Si alguien está tratando de meterse con Bitcoin, eso es lo que haces el primer día, no el quinto. Bien, necesitamos tener algo más, entonces bloquearlo simplemente funciona. Si nos importa el análisis del tráfico en absoluto, entonces lo primero que hay que hacer es aleatorizar los puertos.

Bien, entonces hablemos de aleatorizar los puertos.

Tor es un buen ejemplo. Resuelve la resistencia a la censura para un montón de aplicaciones. No creo que queramos incluir técnicas de resistencia a la censura. Es una violación de las capas. Pero lo haremos, hasta cierto punto. Si hay fruta colgante baja, entonces podemos hacerlo. Pero cambiar el puerto es una fruta al alcance de la mano. Bueno, entonces deberíamos tener un campo de versión real o una cadena de bytes mágica, esto hace que sea mucho más fácil actualizar a futuras versiones. Ya veo, es un buen punto. Esta fue toda la historia de la tristeza de la actualización de TLS y tienes que convencer a la persona que estás hablando en el nuevo protocolo e ir a enormes longitudes para hacer que los mensajes parezcan compatibles o incompatibles con ciertas versiones. Tener un campo de versión puede resultar en un ataque de downgrade si no lo haces de la manera correcta.

Alguien ha preguntado, si vemos un ataque, ¿se aleatoriza el puerto? Bueno, tal vez no hay que dar el último paso, pero hay que hacer que esté disponible fácilmente, como hacer que sea una opción. Si soy un gateway de internet y quiero bloquear el tráfico de internet. Simplemente bloqueo todos los puertos de escucha ipv4. La randmización de puertos no te ayuda cuando tienes una red pequeña. Necesitas nombrar al atacante. ¿Qué estás tratando de mitigar? Comcast enviando emails a la gente porque hey tienes el puerto `8333` abierto.. He recibido emails del MIT sobre que estoy ejecutando algo en el puerto `8333`.

No queremos tener un nuevo número de puerto para esta cosa específica porque la gente tiene que actualizar su router para permitir el reenvío de puertos. Deberíamos mantener el puerto que están usando actualmente, porque es difícil conseguir que la gente lo abra. Pero deberíamos tener una función para la aleatorización que se utilizará en el futuro.

¿Cuántos nodos están detrás de NAT? ¿Qué porcentaje de nodos están detrás de NAT? La mayoría de la gente cuando ejecuta Bitcoin Core no abre el puerto y desactivamos UPNP hace mucho tiempo. Luke-jr tiene algunos análisis de los nodos que escuchan y no escuchan. ¿No se puede usar ipv6 para esto? Europol dijo que les gustaría mucho usar ipv6 para poder atribuir la infracción de derechos de autor a dispositivos específicos en lugar de sólo "en algún lugar de esta casa". Sí, fue mi refrigerador.

¿Cuándo se hace el paso de rekeying bit? La AEAD con `ChaCha20` en general se supone que nunca debes reutilizar la misma clave con el mismo nonce. Tienes que volver a teclear cuando el nonce llega al límite y empieza a desbordarse. Ese es el máximo. Para estar seguros y seguir otras prácticas de protocolo, normalmente se reintroduce la clave después de 1 gigabyte de datos. En nuestro caso, también depende del cliente. El cliente puede desencadenar o iniciar un rekey enviando ese bit. Eso significa que ambas partes vuelven a hacer un hash de la clave simétrica actual, por lo que el secreto hacia adelante es perfecto. Cuando un atacante intenta obtener la clave por varias razones, entonces ....

Si el cliente no hace rekeying, ¿qué hace el receptor? Si se voltea el bit, entonces significa que debe volver a teclear. Así que si no lo hacen, entonces necesitas desconectarte inmediatamente. Si el rekey aparece en cada mensaje debido a un ataque de la CPU, entonces también hay que desconectarse.

P: ¿Por qué quitar la autenticación de esto?

R: Hay una forma de autenticación en la propuesta. La propuesta establece que los clientes o las implementaciones que siguen la propuesta deben mostrar el identificador de sesión. El identificador de sesión es actualmente un secreto ECDH convertido en una forma especializada en una cadena. Esto es después de que el apretón de manos se ha hecho. Cada parte puede comparar el identificador de sesión. Esto es la autenticación, aunque no es práctico, y es necesario hacerlo después de cada intercambio de información con cada compañero, lo que no es práctico.

P: ¿Sería práctico leer estas pubkeys que presentas, como si dada esta pubkey supieras que estás hablando con este tipo?

R: Eso es la autenticación. Todavía existe el `bip150`, que es un esquema de autenticación que sigue siendo válido con esta propuesta. El problema es que hay que entender cómo se produce la autenticación actual. Una de las formas en que hacemos la autenticación en Internet son las autoridades de certificación, como las cosas de TLS. Esto no funciona para bitcoin. La segunda es la forma SSH, que se basa en el primer uso. Creo que tampoco es algo que debamos hacer. En Ethereum, los nodos tienen un identificador público. SSH hace el modelo de confianza en el primer uso. Te conectas, obtienes la huella digital, fijas la huella digital. Si tienes un atacante durante esa primera conexión entonces estás jodido, supongo. Lightning publica su propia clave pública. En lightning, los nodos tienen una identidad, pero en bitcoin no. Tienes que demostrar la propiedad de un viaje. Electrum es confianza en el primer uso, también.

Podríamos tener múltiples esquemas de uatenticación. Uno de ellos es la comparación de los identificadores de sesión, que es un poco estúpido. Otro es `bip150` en el que se comparten las claves fuera de banda. Luego está el esquema que Pieter ideó una vez y del que lamentablemente ya no puedo encontrar el enlace. Es impresionante. De todos modos, hay muchos esquemas potenciales de autenticación.

Sería interesante utilizar el sistema de cotilleo de lightning para conectar los nodos de bitcoin. Es una abstracción de mezcla. Puedes suministrar tu propia autoridad como, -- podría ser externa.

La gente se queja de que no es seguro para el hombre en el medio, lo cual es cierto. Pero no podemos construir todo a la vez. Pero esto es más complicado que eso; en bitcoin, generalmente estamos hablando no sólo de conexiones autenticadas sino también de un sistema sin identidad. Si asumes que tu atacante puede crear sus propios nodos que tienen tanta identidad como aquello a lo que estás intentando conectarte, entonces puede espiarte. El argumento de la encriptación es débil: descarta ciertos tipos de ataques, pero deberíamos tener cuidado al afirmar cuáles son sus ventajas por sí solas. Me gusta cómo hablas de que es un bloque de construcción, no algo que resuelve inmediatamente los otros problemas. También me gusta que sea una mejora del rendimiento, aunque ese es un listón bajo.

Los datos de la cadena de bloques son públicos, pero el tráfico no está destinado a ser público. Esta propuesta no lo hace privado, pero está en camino. Un ataque sencillo es que tu ISP escuche tus transacciones. El ISP puede hacer man-in-the-middle pero eso es un trabajo extra y tal vez detectable o algo así.

El cifrado oportunista, si eres un ISP haciendo man-in-the-middle escuchando una conexión, puedo escuchar sin que el usuario tenga la oportunidad de detectarlo. Pero después de eso, hay identificadores de sesión. El ISP debe asumir el riesgo de que su manipulación pueda ser identificada. Sólo el riesgo de identificabilidad les convencerá de no hacerlo. Pero para hacer ese argumento, hay que hablar de autenticación. Si sólo haces encriptación y nada más, el argumento no se sostiene. Tienes que incluir la autenticación, o al menos la opción de la autenticación, en el ámbito de "por qué es útil el cifrado". El mínimo absoluto para eso es un identificador de sesión, y eso es suficiente para que un investigador de seguridad sorprenda a un gran ISP haciéndolo. Además, los ISP deben calcular que puede haber una forma de autenticación encubierta no publicada porque obviamente queremos detectar a los ISP que hacen las cosas mal.

La mayor amenaza en Internet hoy en día es la vigilancia generalizada, y el cifrado hace que sea razonablemente difícil para los atacantes que utilizan la CPU. Si estás ejecutando un servicio que está usando un socket encriptado, puedo simplemente conectarme a ti y ahora soy tu compañero de todos modos.... Esto hace que el análisis del tráfico suponga un esfuerzo real.

Para el cifrado, tienes que estar en el medio. El monitoreo perasivo generalmente significa que no estás en el medio, sólo estás monitoreando paquetes. Sólo puedes descifrar si eres el par o estás en el medio. Si eres un ISP, puedes instalar algo en el router para escuchar el tráfico, manipular paquetes, observar paquetes, sin coste, sin handshake nada. Pero si quieres interceder en este protocolo, necesitas interceptar activamente el apretón de manos y arreglar las claves, rastrear a cada compañero, es mucho más complejo de hacer. Imagina que eres una entidad de vigilancia donde lo que obtienes es un volcado en vivo de paquetes a través de Internet.

# Firma: un protocolo de autenticación secreta

<https://gist.github.com/sipa/d7dcaae0419f10e5be0270fada84c20b>

La red bitcoin está formada en su mayoría por pares sin identidad. Pero existe la identidad en forma de "tengo un compañero de confianza con esta dirección IP". Esa es una forma de identidad. Es una forma horrible y fácilmente falsificable, pero se utiliza. Como que tengo un VPS en mi teléfono y voy a configurarlo para que se conecte a esa dirección IP porque es un nodo en el que confío. Lo bueno que podrías hacer si tuvieras un mecanismo de autenticación en el que pudieras preguntar a alguien "¿eres la identidad `x`?" sin decirles qué es `x`, y así, no saben por qué se les está preguntando y no saben si tienen éxito en la autenticación. Es posible. Parece imposible, pero de hecho es posible. Lo que se hace es ejecutar siempre este protocolo de autenticación en cada conexión. Si no te importa quién es el otro peer, entonces en el `99%` de los casos, dices que ejecutas el protocolo con una clave aleatoria y él no sabrá lo que se le pide y responde de una manera y te enteras de que por supuesto no lo es porque hiciste una clave pública aleatoria y lo ignoras. Pero cuando quieres la autenticación, consultas la clave correcta, todavía no saben si lo son, pero aprendes sip estoy conectado al nodo que quiero. Lo bueno es que un hombre en el medio no puede distinguir entre estos dos escenarios. No pueden saber si la otra parte es... bueno, pueden saberlo después de desconectarse porque tenían la clave equivocada. Tal vez no deberías desconectarte. Depende. Generalmente quieres mantener una conexión abierta y tratarla como una conexión aleatoria. El hombre en el medio siempre tiene la capacidad de ver bien, si la autenticación es opcional en absoluto, sólo vamos a ejecutar el protocolo de autenticación algunas veces, el MITM puede decir simplemente voy a interceptar cada conexión y cuando veo un intento de autenticación voy a desconectar y poner en la lista negra estas dos direcciones IP y no interferir más y esto probablemente no será detectado. Pero si siempre se ejecuta el protocolo, sólo tienen la opción de abandonar cada conexión o ser detectados. Usted conoce la clave de identidad de su servidor, así que puede configurarlo en su teléfono para conectarse a ese. Pero no hay una identidad observable para ese servidor. Simplemente no publicas la clave pública. El otro compañero la conoce. Es inobservable. No es posible filtrarla a menos que le des la clave a alguien. Además, no deberías reutilizar las claves de identidad... bueno, no debería importar porque sólo estás usando este protocolo para ti mismo, no para conectarte a los pares. Es un protocolo de conocimiento cero, un observador no aprende nada. Esto no es bip150. En bip150, si tienes una conexión fallida y más tarde aprendes la clave pública a la que podrías haberte conectado, puedes correlacionar esas conexiones fallidas con esa clave pública. Pero aquí en esta propuesta no se aprende nada. Es una consulta, eres la clave `x`, pero es una aleatoriedad... son dos puntos que pasan por el cable y parecen aleatorios, y hay una respuesta que es que tomas esos dos puntos y tu clave privada y obtienes dos puntos de vuelta que parecen aleatorios para todo el mundo excepto para alguien que tiene la clave pública correspondiente.

# Post-quantum

Creo que PQ es demasiado para esta propuesta. Creo que añadir el post-cuántico no tiene sentido. Tiene sentido para tor porque si comunico algo hoy podría seguir siendo secreto en 20 años. Probablemente haya gente que esté recopilando muchos datos de tor ahora con la esperanza de desencriptarlos dentro de 20 años. Si hay una forma fácil y obvia de añadir post-cuántica entonces deberías hacerlo. Si estás limitado por la CPU, haces análisis de tiempo y ancho de banda de todos modos, así que no ganas mucho al añadir post-cuántica.

Una cosa que sería útil es un campo de versión o alguna manera de actualizar para post-cuántica en el futuro, incluso si una solución no se incluye en la propuesta. Si añadimos post-cuántica ahora, no hay manera de hacer que se vea totalmente al azar por lo que yo sé. Puede que haya una forma de hacerlo. Tal vez se pueda, no lo sé.

# Charlas previas

<https://btctranscripts.com/sf-bitcoin-meetup/2017-09-04-jonas-schnelli-bip150-bip151/>

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/bip151-peer-encryption/>



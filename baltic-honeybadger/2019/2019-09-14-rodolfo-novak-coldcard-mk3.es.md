---
title: Coldcard Mk3 - Security in Depth
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - security
  - hardware-wallet
date: 2019-09-14
speakers:
  - Rodolfo Novak
media: https://youtu.be/2IpZWSWUIVE?t=23739
---
## Intriduccióno

Mi nombre es Rodolfo, he estado alrededor de Bitcoin por un tiempo. Hacemos hardware. Hoy quería entrar un poco en cómo hacer una billetera de hardware segura en términos un poco más legos. Ir a través del proceso de conseguir que se haga.

## ¿Cuáles fueron las opciones?

Cuando cerré mi última empresa y decidí buscar un lugar para almacenar mis monedas, no pude encontrar un monedero que satisficiera dos cosas que necesitaba. Que era la seguridad física y el código abierto. Hay dos carteras en el mercado. Uno es físicamente seguro pero es de código cerrado. La otra no es físicamente segura pero es de código abierto. No podía soportar eso, así que creé uno nuevo. Coldcard Mk3 logra eso.

## MCU + SE

Una cosa que es interesante es que hay una retórica sobre cómo realmente no se puede hacer carteras de hardware de código abierto con un elemento seguro. Eso no es cierto. Puedes crear firmwares de código abierto utilizando elementos seguros. Los elementos seguros son un chip muy especializado que hace que las cosas sean seguras. Nosotros lo hicimos. Por cierto, tampoco existe un elemento seguro de código abierto o un chip de código abierto en general. Hay algunos proyectos de aficionados, pero todo el hardware es esencialmente de código cerrado. Sólo el software que se ejecuta en él es de código abierto. Mientras no utilices la criptografía que tal vez sea de código cerrado en el chip estás bien. Si usas la tuya propia, es de código abierto y la gente puede verificarla.

## Seguridad en profundidad

Jugamos con este tema de que la seguridad en profundidad es esencialmente cómo aumentar el coste de un ataque para que sea completamente asimétrico para el atacante. Quieres que sea muy caro y que cueste mucho dinero para que el atacante se sienta así.

Lo que hacemos es crear muchas capas. Cada capa hace que cueste más. La primera capa para nosotros es un monedero totalmente airgapped si usted quiere que sea. Con Coldcard no tienes que conectarte nunca a un ordenador si no quieres que esté conectado a un ordenador. Esto disminuye el vector de ataque significativamente porque la mayoría de los ataques requieren que usted interactúe de alguna manera con el dispositivo para tratar de sacar las cosas del dispositivo. Tenemos formas de evitar eso.

## Empezando por lo básico: La cadena de suministro local

Lo primero que hay que hacer es controlar la cadena de suministro. Nosotros fabricamos nuestros dispositivos en Canadá. La fábrica está a unos 30 minutos de mi casa. Los micros se fabrican en Singapur, de un importante proveedor de microchips que lo hace para todos los coches que conduces, serían los mismos chips. Pero los probamos en nuestras propias instalaciones.

#Simplicidad de embalaje: ¡Sin cable USB! Bolsa a prueba de manipulaciones + Número de serie en SE

Entonces pasamos a la siguiente etapa. ¿Cómo puedo enviar desde mi fábrica hasta usted y evitar alguna manipulación en el medio? Hemos contratado a una empresa que fabrica bolsas para que los bancos depositen el dinero en su interior. Así, si se intenta abrirla y manipularla en la aduana o algo así, se verá si está anulada. Entonces lo que hacemos es obtener el número de serie de la bolsa para evitar que la fábrica se meta contigo. Lo programamos dentro del elemento seguro de la cartera. Incluso si se las arregló para hacer las bolsas exactamente lo mismo que usted todavía necesita saber el número de serie de la bolsa y no se puede manipular que dentro del elemento seguro.

## Caso claro: Inspección de dispositivos

La siguiente etapa es: "Bien, tengo la cartera. Compruebo la cartera, compruebo el número de serie de la cartera". Proporcionamos fotos de alta resolución del dispositivo en nuestro sitio web y la carcasa es transparente para que puedas mirar realmente dentro y ver que no hay cosas raras ahí dentro. Muchos ataques requerirían que se modificara el hardware para intentar quitarte las monedas. Digamos que todo parece exactamente como se supone, genial.

¿Cómo aseguramos los chips? El elemento seguro está aquí. Es este pequeño tipo. Está conectado directamente a los LEDs por una razón que explicaré más tarde. Ponemos epoxi en la parte superior de eso. Incluso si quieres tratar de romper la cartera, sacar el elemento de seguridad, tratar de leerlo de alguna manera, probablemente vas a romperlo tratando de sacarlo de allí. Ya has tenido que romper la carcasa para eso. También pusimos un poco de epoxi en los contactos la materia del otro microchip con el que habla.

## Pelando las capas

Entonces tenemos este sistema donde queremos ser capaces de atestiguar el hardware sin tener que hablar con el software real. Nuestro elemento seguro está conectado directamente al LED rojo y hay epoxi sobre esa conexión. No es imposible que alguien llegue allí, pero es una característica más que hay que atravesar. Empieza a costar mucho dinero para superar todo. Pero si tu dispositivo es genuino, ahí lo tienes, obtienes una luz verde después de iniciar sesión y estás listo para ir.

## Split PIN con anti phishing 2 palabras ie Evil Maid: Intercambio de dispositivos/intercambio de piezas

Ahora digamos que tienes un problema donde dejaste el dispositivo desatendido en tu casa o en un hotel. Usted podría tener una criada malvada y la criada malvada podría tratar de intercambiar su dispositivo. Esto es en realidad un ataque que ocurre, no tanto para carteras de hardware todavía, no al menos conocido, pero es uno común. Esencialmente un atacante reemplazaría tu dispositivo con un dispositivo ficticio porque no vas a inspeccionar todo de nuevo. Estará en la otra habitación por ejemplo con tu dispositivo real. Pero el suyo en realidad está transmitiendo que usted escribe el PIN a él. Así que él puede entrar y sacar el dinero. Lo que hacemos es dividir el PIN en dos. Hay esencialmente dos PINs, El primer PIN, va a desbloquear estas dos palabras. Estas dos palabras son únicas para ti y el dispositivo. Entonces, una vez que usted mira el dispositivo después de poner su primera parte del PIN se ven estas dos palabras. Si las dos palabras son incorrectas significa que ese dispositivo no es tu dispositivo. Realmente no pueden cambiar eso dentro del elemento seguro. Hay unos 4 millones de combinaciones. Si las palabras están bien, entonces escribes la segunda parte del PIN. Incluso si obtuvieron la primera parte del PIN porque se transmitió a la otra habitación, ahora tienes la segunda parte del PIN protegiendo tu riqueza allí.

## Generación de semillas en el aire + opción de tirar los dados

Un gran problema con los monederos de hardware o cualquier tipo de criptografía en general, es que necesitas tener una semilla sólida o una clave privada. Para generar eso, los monederos usarían el generador de números aleatorios dentro de su elemento seguro. Si son buenos, tendrán verdaderos RNGs. El problema es que sigues confiando en el silicio de los chips. No puedes confiar en eso, porque si alguien tiene una puerta trasera en el chip, te vuelven a quitar tus monedas. Lo que hacemos es usar dados. Puedes lanzar los dados y se puede demostrar que estás introduciendo tu propia entropía. Te guiamos en la pantalla del dispositivo. Solo tienes que tirar unos dados y vas a obtener una clave privada sólida, es bastante demostrable matemáticamente. Lo haces completamente airgapped. La Coldcard puede funcionar sólo con una batería. Puedes conectarla a tu ordenador y tener una forma tradicional muy bonita de usar un monedero hardware, digamos para tus fondos calientes. Pero para tus cosas profundas, tu almacenamiento en frío profundo, este dispositivo hasta ahora no ha tocado una computadora. Puedes ir dentro de tu jaula de Faraday, puedes tener a Michael Flaxman haciendo guardia fuera de ella, puedes llevar tu sombrero de papel de aluminio. Puedes hacer todo este proceso sabiendo que nadie está interceptando nada.

## Configuración Multi-Sig también Air-Gap

Entonces puedes pasar al siguiente nivel. Puedes hacer multisig. Lo que hacemos es que puedes crear el quórum multisig, el M-de-N de tu cartera multisig sin volver a tocar un ordenador. Vas a la primera y dices "Quiero crear un multisig". Te va a preguntar cuántos de cuántos. Luego pones la segunda, la tercera, la tarjeta microSD pasando y luego vuelve a la primera, ya tienes todo listo. Sólo tienes que cargar ese archivo en digamos Electrum y tienes una configuración multisig sin tocar nunca un ordenador. Es muy importante.

## Tu semilla está encriptada en un elemento seguro con un pad de un solo uso

Digamos que el dispositivo fue interceptado por alguna agencia con muchos recursos y decidieron que querían tus monedas. Definitivamente tendrán acceso físico a él. La seguridad física es muy importante, así que ¿qué hacemos? En realidad encriptamos tu clave privada dentro del elemento seguro con la almohadilla de un solo uso. La almohadilla de un solo uso es esencialmente la única criptografía demostrable e irrompible que puedes hacer para que sea secreta. Incluso si alguien envía tu dispositivo a alguna instalación, pueden pelar el chip que está sirviendo al elemento seguro. Ahora ya estamos costando cientos de miles de dólares para hacer este ataque. Se las arreglan para pelar el chip, utilizan su electro microscopio para mirar las puertas dentro de su chip y de alguna manera se las arreglan para sacar los datos. No pueden romperlo, sería muy difícil.

## SE impone un máximo de 13 intentos de PIN, PIN "Brick Me" definido por el usuario

Así que dejaste tu dispositivo en tu casa y no es esa agencia la que quiere tus monedas, es tu mal empleado o algo así. Ellos tratarán de externalizar algo de eso, tratarán de romper el PIN o algo así sin pasar por todo el esfuerzo de pelarlo. En esta nueva versión usamos contadores monotónicos. Se trata de contadores unidireccionales dentro del chip que no pueden ser invertidos. Este es un elemento seguro que está diseñado para eso. Si escribes el PIN mal 13 veces es puf. La cosa se convierte en un ladrillo. Es tan bueno como la basura. Esperemos que tengas una copia de seguridad de tu semilla y puedas hacer tu nuevo dispositivo en otro lugar. No creemos en los restablecimientos de fábrica. Un restablecimiento de fábrica podría ser utilizado como una puerta trasera. No queremos abrirnos a nada, preferimos simplemente tirar a la basura un dispositivo de 100 dólares. No tiene sentido tratar de salvarlo.

Entonces la copia de seguridad, la copia de seguridad es súper importante. Usted va a tener su semilla en uno de estos dispositivos de metal o de papel. Pero una cosa muy importante es tener algunas copias de seguridad que son realmente más fácil y más seguro para restaurar. Hacemos eso con las tarjetas micro SD, tarjetas SD de grado industrial, tarjetas SLC. Esencialmente encriptamos la copia de seguridad y alguna información extra para ti del monedero, dentro del dispositivo en el que ya confías con tu clave privada que es tu monedero de hardware. Te damos 12 palabras que aseguran eso. Realmente puedes mantener todo esto sin tocar nunca un ordenador. Esa es la forma en que hacemos esto.

## Transacciones con firma (PSBT)

Eventualmente tienes que gastar Bitcoins y no estás tocando una computadora en este escenario perfecto. Así que lo que haces es elegir el USB. Tenemos algunas protecciones para eso, el protocolo está encriptado, pero esa no es la mejor manera de hacerlo. La mejor manera de hacerlo es que tengas tu Electrum o tu HWI en Core o eventualmente tu nodo Casa y crees tu transacción allí. Lo guardas en una tarjeta micro SD. Esa tarjeta micro SD, puedes llevarla a la caja de seguridad de tu banco donde guardas esa Coldcard. Vas allí, conectas una batería, la firmas y la guardas en esta tarjeta micro SD. Puedes ir y emitir la transacción en otro lugar. O simplemente la conectas, la firmas y la envías. Pero ser capaz de hacer SneakerNet y no tocar nunca un ordenador es un gran problema. Así es como se intentarán la mayoría de los ataques. Otra cosa que hacemos mucho es que hacemos un análisis muy cuidadoso en las salidas de cambio. Muchos ataques en cualquier cosa de Bitcoin, van a tratar de obtener el dinero que estás devolviendo. En Bitcoin cuando envías una moneda no hay manera de romper eso. Esencialmente le das al sistema la dirección que quieres que reciba el cambio de esa transacción. Los otros 10 de los 100 dólares que enviaste porque querías pagar 80. Nos dimos cuenta de que muchos monederos no comprueban las salidas de cambio, no se aseguran de que esa salida sea parte de tu clave privada. Podrías perder fondos de esa manera y ellos simplemente YOLO.

Este es un resumen masivo, sólo quería añadirlo ahí. Planeamos añadir Shamir's Secret y hacer un montón de otras cosas. Pensé en hacer un Q&A y responder a algunas preguntas sobre carteras de hardware y seguridad si alguien está interesado.

## PREGUNTAS Y RESPUESTAS

P - .....

R - Va a depender. Esa biblioteca, es muy intensiva en memoria. No estoy seguro de que haya suficiente espacio en la memoria de las versiones anteriores. Con esta nueva versión hemos añadido más memoria, más seguridad para poder hacer más cosas. Por eso también es un poco más cara.

P - Has hablado de un contador monotónico para imponer 13 intentos para el PIN. ¿Se reinicia cuando se acierta?

R - No es como un dispositivo que muere, así que cada vez que te equivocas. De hecho, elegimos el 13 a propósito porque en muchos países es un número malo. Cada vez que se acierta el PIN se reinicia el contador.

P - Dado que podemos utilizarlo para el almacenamiento en frío a largo plazo, ¿cuál es su estrategia para las actualizaciones de firmware a largo plazo? No sólo para el Mk3 sino también para los dispositivos anteriores que alguien pueda tener.

R - Intentamos dar soporte hacia atrás en la medida de lo posible. Algunas características simplemente no pueden porque necesitan el nuevo hardware. Lo que yo sugeriría es simple. Si no se trata de una actualización de seguridad por nuestra parte y no necesitas la función, no la actualices. No entres en tu área de seguridad para actualizar tu dispositivo si no lo necesitas. Es por eso que mi iPhone tiene un montón de aplicaciones que nunca se han actualizado. Si no lo necesito y sigue funcionando no lo actualizo. Pero si es una actualización de seguridad y tiene sentido que la haga, documentamos bastante bien nuestras actualizaciones.

P - ¿Habéis firmado un ND para conseguir el elemento de seguridad?

R - Sí, firmamos un acuerdo de confidencialidad para el 508a. Luego el fabricante abrió las especificaciones para todo el mundo, lo cual es genial. Ahora estamos trabajando con el 608 que estamos trabajando para que lo abran. Pero realmente no importa porque, en primer lugar, las especificaciones se filtran en todas partes de todos modos. Dos, el firmware es totalmente abierto, así que puedes comprar todas las piezas que usamos, puedes construir tu propio dispositivo y cargar nuestro firmware. Puedes probarte a ti mismo que el dispositivo es seguro. No usamos ninguna de las características de código cerrado del chip, ninguno de los criptoaceleradores para nada relacionado con Bitcoin.

P - Has dicho que la semilla está encriptada y almacenada en el elemento seguro y encriptada con la almohadilla de un solo uso. ¿Dónde se almacena la almohadilla de un solo uso? ¿Es la MCU?

R - Es una mezcla del PIN en el elemento seguro y la MCU.

P - ¿Su implementación de Shamir's Secret será compatible con Trezor?

R - No lo sé, tengo esperanzas. No lo hemos revisado, así que no puedo prometer que vayamos a utilizarlo. Todo el mundo tiene sus opiniones. Siempre se necesita una norma más para que sea la norma de todas las normas. Vamos a intentarlo porque queremos ser compatibles con todo.

P - Puedes explicarte un poco más, has mencionado que si introduces el PIN varias veces mal y luego lo introduces correctamente se resetea. Pero antes ha dicho que no se puede reiniciar. ¿Se puede simular ese restablecimiento de alguna manera para probar infinitamente muchos PINs?

R - Eso es lo que te proporciona un elemento seguro. Si un monedero no tiene un elemento seguro no puede hacer esto, no tiene remedio. Por eso hemos creado esto. Necesitas un contador monotónico. Es algo así como una función de contador que puede invertirse. Pero entonces puedes tener algo que pretenda ser eso. El elemento seguro te proporciona el tipo de memoria que necesitas que no puede ser cambiada, punto. Simplemente no puede. Podemos evitar que eso sea un intento. Luego, una vez que se resetea, reinicia el contador monotónico.

P - ¿Cuál es el secreto de su genialidad? Específicamente la genialidad de Twitter, si puede explicarlo.

R - La toxicidad.

P: En un par de diapositivas tiene algunas características para facilitar el uso de esto como una solución más cálida. ¿Cuánta presión está recibiendo del mercado, de los líderes de su empresa que están tratando de decirle qué construir para hacer estas cosas un poco más accesibles o más fáciles de usar?

R - Realmente no nos importa. Construimos esto para mí. Todo el mundo tiene un viaje diferente en Bitcoin, pero todo el mundo llega al final. Hay un límite de abstracción que puedes hacer sin confiar en alguien más. Con cada capa de abstracción se confía en algo más. Es muy importante que la gente llegue allí. Intentamos hacerlo fácil y probablemente también podemos hacerlo más fácil. Por eso también soportamos los USBs para que puedas estar caliente con una forma más tradicional de usarlo. Pero hay cosas que nunca haremos. Nunca tendremos un monedero web para que esto se conecte a través de USB porque eso es una locura. Nunca haremos que verifiques tu dispositivo con nuestros servidores para que puedas usar ese dispositivo porque esencialmente te estás doxando a ti mismo. Incluso si somos amables no sabemos quién está escuchando. Esencialmente la filosofía de este dispositivo es que nadie sabe que lo tienes, no toca nada y no sabemos que lo tienes. Realmente va por el camino de la privacidad en el manejo de las cosas. Por eso obtienes gratis la forma de hacer las cosas del airgap. Piensa en Stuxnet. El esfuerzo que esos tipos hicieron para conseguir el malware dentro de la instalación. Se trata de crear eso y mantenerlo. Si quieres un monedero mucho más fácil de usar que te proporcione algunas de las características que nosotros no haríamos, te enviaré a la página web de mis competidores y podrás comprarles a ellos.

P - ¿Podemos enumerar una vez más todo lo que se hace en el elemento seguro? Se almacena la semilla mnemónica, se gestiona el contador monotónico y la clave privada para la atestación está ahí. ¿Hay algo más que haga el elemento seguro?

R - Utilizamos un TRNG para parte de la comunicación entre la MCU y el elemento seguro. Se necesita esa aleatoriedad, que es razonable para que los dos hablen juntos porque hay un token de una sola vez en la MCU. Usamos la aleatoriedad, usamos sus características para hacer la comunicación de forma segura entre los dos, no usamos ningún acelerador criptográfico de código cerrado para hacer cualquier cosa de Bitcoin. Todas las operaciones de Bitcoin se hacen con una biblioteca criptográfica de código abierto que compartimos con otros monederos de hardware. Hay muchos ojos en eso. No sé si ese es el origen de la pregunta. No se utiliza ninguna criptografía oscura. Las librerías de proveedores para incrustados es realmente un cúmulo de basura. No las usas. Tienes tus propias cosas y luego para toda la criptografía que está relacionada con Bitcoin tienes bibliotecas que son abiertas y mantenidas por más de una persona así que hay un montón de ojos allí.

P - ¿Podemos enumerar una vez más todo lo que se hace en el elemento seguro? Se almacena la semilla mnemónica, se gestiona el contador monotónico y la clave privada para la atestación está ahí. ¿Hay algo más que haga el elemento seguro?

P - ¿Es posible obtener la clave pública maestra?

R - Sí, es HD. Puedes simplemente exportar la xpub, zpub, soportar un montón de rutas de derivación diferentes, todo es tu elección.

P - Si genero mi propia aleatoriedad, ¿puedo hablar de cómo la introduzco y de lo que produce?

R - Es bastante divertido. Matt Odell está por aquí, hizo un bonito [vídeo](https://www.youtube.com/watch?v=sM2uhyROpAQ) sobre esto. Esencialmente, en el menú de generación de claves te va a preguntar si quieres hacer dados. Vas a Amazon y compras tus dados de casino. Luego eliges qué nivel de paranoia quieres tener. Puedes añadir un poco, puedes hacer la mitad o puedes ir todo el 99 que necesites. Luego sólo tienes que lanzar los dados y pulsar qué resultado obtuviste. Tira el dado, presiona el resultado que obtuviste. Hasta que hayas llenado la entropía que necesitas. Todo eso es demostrable, aquí hay [documentación](https://coldcardwallet.com/docs/verifying-dice-roll-math) sobre eso.

P - Me encanta el producto Mk3, ya he pedido uno. ¿Qué opina de que el Mk4 pueda tener un lector de códigos QR?

R - Los códigos QR son complicados por un par de razones. Una es que no se puede tener un lector de módulos QR estándar. Eso es demasiado caro para que yo pueda hacer una cartera de hardware que pueda vender a usted. Va a ser demasiado caro. Dos, hay una complejidad añadida a la cartera que no quiero incluir porque hay más bugs en esas cosas. Tres, las pantallas son demasiado pequeñas por lo que no se pueden hacer transacciones a través de códigos QR. Se van a necesitar cientos de códigos QR para que puedas sacar todos los datos. En mi opinión personal no creo que haya una seguridad añadida allí sobre la tarjeta micro SD. Es muy poco probable. Me gusta para los pagos. Si estoy haciendo un monedero que está orientado a los pagos, entonces sí es fantástico para meter una dirección. Pero para las transacciones no creo que haya una ganancia masiva.

P - Mi principal problema con la tarjeta es el impuesto de importación desde Canadá.

R - Permitimos que la gente revenda nuestro material, pero nunca vamos a responder por un revendedor porque eso es un gran riesgo de seguridad. Con toda honestidad, por los pocos dólares que vas a pagar en impuestos, al menos sabes que lo estás recibiendo directamente de nosotros. Creo que ahorrarse unos cuantos dólares por algo que va a almacenar tu riqueza, no es la preferencia de tiempo correcta.

P - ¿Habéis traído alguno?

R - No. El Mk3 empieza a enviarse a finales de octubre, principios de noviembre.

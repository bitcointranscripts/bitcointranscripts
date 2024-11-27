---
title: Taproot Lightning
speakers:
  - Antoine Riard
date: 2020-02-06
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
  - lightning
  - ptlc
media: https://www.advancingbitcoin.com/video/a-schnorr-taprooted-lightning,11/
---
Tema: A Schnorr-Taproot’ed Lightning

Diapositivas: https://www.dropbox.com/s/9vs54e9bqf317u0/Schnorr-Taproot%27ed-LN.pdf

# Introducción

Hoy Schnorr y Taproot para Lightning, es un tema realmente apasionante.

# Arquitectura Lightning

La arquitectura Lightning para aquellos que no están familiarizados con ella. Usted tiene el blockchain como la capa subyacente. Encima de ella vas a construir un canal, tienes un HTLC y la gente va a gastar capas hacia ti. Si quieres que te paguen vas a enviar una factura al remitente.

# ¿Para qué debemos diseñar Lightning?

¿Para qué deberíamos diseñar Lightning? Cuando hacemos la especificación del diseño de Lightning, estamos invirtiendo mucho en ello y todo el mundo tiene una visión diferente de lo que debería ser Lightning. ¿Debe ser Lightning un sistema de transacciones de pago rápido? ¿Debería Lightning estar optimizado para las microtransacciones? ¿Es Lightning realmente genial porque obtienes la finalidad instantánea de tus transacciones? ¿Es la privacidad la razón por la que estamos haciendo Lightning? Lightning puede tener mejores propiedades de privacidad. Cuando hablamos de privacidad para Lightning sería mejor tener en cuenta la privacidad de la capa base. En la capa base se van a difundir las transacciones. Hay una cantidad, no está encriptada. Hay una dirección, no está encriptada. Vas a enlazar entradas y salidas en el gráfico UTXO.

# ¿Cuál es la privacidad de la capa base?

La privacidad para la capa base no es tan grande que hoy. El rayo puede ser una forma de resolver la privacidad.

# ¿Cuál es la privacidad de Lightning?

Pero en Lightning hay una vía de pago. Los nodos de Lightning tienen pubkeys atadas a ellos y eso es un vector de identidad. Con los HTLCs puedes reutilizar un hash, hay muchos vectores de privacidad diferentes. La privacidad es, en mi opinión, muy importante si quieres dinero resistente a la censura.

# ¿Por qué debemos centrarnos en la privacidad?

"La criptografía reordena el poder, configura quién puede hacer qué, a partir de qué" [El carácter moral del trabajo criptográfico](https://web.cs.ucdavis.edu/~rogaway/papers/moral-fn.pdf) (Rogaway)

Si no tienes privacidad, puedo sobornarte o chantajearte porque sé cómo estás usando esta tecnología. Ese es un enorme vector de ataque. Hay un documento impresionante de Philip Rogaway. Animo a todo el mundo a leerlo.

# EC-Schnorr: esquema de firma eficiente

`Par de claves = (x,P) con P= xG y par de claves efímeras (k,R) con R = kG`

`Hash del mensaje = e = hash(R | m) y Firma = (R,s) con s = k + ex`

`Verificación = sG = R + eP`

Puedes ver a Schnorr y Taproot como un impulso a la privacidad. La razón para modificar la capa base del consenso, que es mucho trabajo, hay mucha gente involucrada, tiene que haber una buena motivación para hacer esto. Schnorr es un reemplazo para ECDSA. Originalmente Satoshi no introdujo Schnorr en Bitcoin porque había algunos problemas de patentes. Schnorr es realmente impresionante porque hay linealidad en la ecuación de verificación de Schnorr. Linealidad significa que es fácil sumar componentes. Es fácil sumar firmas, es fácil sumar pubkeys y es fácil sumar nonces entre diferentes partes.

# Taproot: árbol de guiones que preserva la privacidad

`Taproot pubkey: Q = P + tG con Q y P puntos de curva`

`t es la raíz de un árbol Merkle donde cada hoja es un hash de un script`

`El testigo de gasto proporciona la prueba Merkle y el script`

La otra gran propuesta de actualización de consenso, nada ha sido aún adoptado por la red, Taproot es la idea de construir un árbol de Merkle de cada hoja del árbol de Merkle va a ser un script. Va a comprometer la raíz del árbol de Merkle dentro de la pubkey. Eso es genial. Ahora, cuando usted va a gastar una salida Taproot usted tiene dos opciones. La primera opción es usar un keypath spend. La otra opción es revelar uno de los scripts más una prueba Merkle. Esta prueba Merkle permite a la red verificar que este script ha sido comprometido con el compromiso inicial del scriptPubKey, la pubkey del gasto de la transacción.

# Nuevas propiedades de consenso

¿Cuáles son las nuevas propiedades de consenso de esta actualización? La linealidad es la que vamos a utilizar para esta charla. Con Taproot tenemos guiones complejos baratos. Otra ventaja es que bajo el supuesto de Taproot, si todos están de acuerdo, no tienes un desacuerdo, pueden gastar una salida de Taproot de forma cooperativa para que el script no sea visto por ningún observador externo.

# Más recursos de Schnorr-Taproot

Hay números BIP para [Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki), [Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) y [Tapscript](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki). Te animo a que leas los BIPs. También hay más recursos en el [repo] de AJ Town en GitHub(https://github.com/ajtowns/taproot-review).

# Canal: "Plaintext" cierre

`Salida de P2WSH: 0 <32-byte-hash>`

`Script de testigo: 2 <pubkey1> <pubkey2> 2 OP_CHECKMULTISIG`

En este momento se va a emitir una transacción de financiación onchain. Esta transacción de financiación va a ser un pay-to-witness-script-hash (P2WSH). Cuando cierres el canal todos los pares de la red van a ver que fue un 2 de 2. Al revelar el script vas a filtrar que estabas usando Lightning. ¿Cómo podemos resolver esto?

# Schnorr Taproot -Canal: Cierre "discreto"

`Salida de taproot: 1 <32-byte-pubkey>`

`Script de testigo: <MuSig-sig>`

Podemos incrustar el script en una salida de Taproot. De esta manera si ambas partes acuerdan hacer un cierre mutuo no va a poder disociar esta salida de Taproot de financiación del rayo de otra salida de Taproot.

# Canal: El peor caso de cierre

Yendo más allá, aunque no estemos de acuerdo, lo ideal sería que el canal no fuera visto por ninguna de las partes. El blockchain se preocupa por la ejecución fiel del contrato, pero lo ideal sería que no se enterara de las cantidades porque éstas forman parte del contrato.

# Schnorr Taproot -Canal: Compromiso compartido

Creo que se puede ir más allá con esta idea. Puedes codificar la transacción de compromiso en su propio Taptree y cada Tapscript sería un HTLC. Este Tapscript pasaría a una transacción de 2ª etapa. Esta transacción de segunda etapa tendría dos salidas. Una salida pagando al HTLC y la otra pagando al Taptree menos el gasto del Tapscript. Creo que tal vez SIGHASH_NOINPUT sería un mejor ajuste para esta construcción, pero hay una manera de hacer el canal discreto. El blockchain no debería enterarse de que estás haciendo algún tipo de construcción offchain.

# HTLC: correlación de hash de pago

Cada parte de HTLC de la ruta de pago reutiliza el mismo Script hashlock es decir

`OP_HASH160  <RIPEMD160(payment_hash)>  OP_EQUALVERIFY`

En este momento estamos utilizando un hash de pago. Cualquier parte HTLC de la ruta de pago está reutilizando el mismo hash. Si eres una empresa de Chainalysis y tienes nodos espías en la red o tienes grandes nodos de procesamiento y estos nodos son parte de la misma ruta de pago, van a ser capaces de adivinar la "cercanía del gráfico" del emisor y del receptor. Eso es realmente malo porque ahora mismo las rutas de pago son bastante cortas dada la topología actual. Lo ideal sería utilizar un hashlock diferente para cada salto.

# Schnorr-Taproot: Contrato por tiempo determinado

`partial_sig = sG = R + H(P | R | m)P`

`adaptor_sig = s’G = T + R + H(P | R | m)P with the T the nonce tweak`

`secret t = adaptor_sig - partial_sig`

Hay una idea genial de los scripts sin guión de Andrew Poelstra, que ha hablado hoy mismo. Con un script sin guión vas a retocar la pubkey nonce con un secreto. Cuando una de las partes está lista para reclamar el secreto tiene que revelarlo para desbloquear la salida.

# Protocolo de PTLC: fase de preparación

(Ver diagrama en las diapositivas)

El protocolo funciona así. Se va a construir una pubkey agregada de 2-de-2. Una de las partes va a enviar una pubkey nonce modificada. Alice va a enviar un sig parcial a Bob. Bob va a enviar su sig parcial... Cuando Bob está listo para reclamar la salida tiene que revelar el secreto. Esta es una forma de intercambiar atómicamente fondos contra un secreto. Puedes reutilizar esta primitiva para construir un mundo como las rutas de pago de Lightning. PTLC, point timelocked contracts, debería ser el sustituto de HTLC. Habrá tres fases. La primera fase, configuración, se envía un punto de curva a cada parte de la ruta de pago.

# Protocolo PTLC: fase de actualización

(Ver diagrama en las diapositivas)

La segunda fase es la de actualización. Vas a intercambiar sigs parciales entre cada salto de la ruta de pago.

# Protocolo PTLC: fase de asentamiento

(Ver diagrama en las diapositivas)

La última fase es la del acuerdo. Dave va a revelar el secreto que permite a Carol conocer su propio secreto que va a permitir a Bob conocer su propio secreto. Bob va a reclamar el PTLC a Alice. Alice va a aprender el secreto final. Este secreto final puede ser reutilizado para resolver otros problemas.

# Facturas: comprobantes de pago

En este momento, cuando vayas a realizar un pago en la red, aprenderás la preimagen. La preimagen se puede utilizar como prueba de pago. Pero no te dice quién es el remitente original. Cada salto de la ruta de pago puede afirmar ante un juez "Yo fui el que hizo el pago. Tengo la preimagen". Si se puede presentar también la factura, no se puede asociar entre las partes de la ruta de pago.

# Facturas de Schnorr Taproot: comprobante de pago

Reutilizando el valor z (zG ha sido firmado por el receptor) del protocolo PTLC, podrá tener este valor secreto único. Este valor secreto único sólo va a ser aprendido por el remitente original. Esto podría ser genial porque podrías usar esto para activar un contrato de segunda etapa o algún tipo de custodia de protección al consumidor, algo así.

# Onion-packet: pago simple o MPP

El MPP ha sido presentado por Joost. En este momento el MPP es genial para resolver los problemas de liquidez, pero puede ser una debilidad para la privacidad porque puede ser capaz de hacer la intersección de las rutas de pago entre los diferentes MPP utilizados si un nodo de espionaje de parte de todas las rutas de pago MPP. Lo ideal es utilizar un valor diferente para esta ruta de pago.

# Paquete de cebollas Schnorr Taproot: Tronco discreto AMP

Existe la idea de utilizar el mismo truco criptográfico de la linealidad de Schnorr. Antes de establecer la ruta de pago Alice el remitente compensará el punto de curva recibido de Dave, el último salto de la ruta de pago, por su propio secreto. Va a enviar fragmentos del secreto a través de cada parte de la cebolla de la ruta de pago atómica. Sólo cuando todos ellos estén bloqueados en el último salto, será posible combinar los fragmentos del secreto y reclamar el pago.

# HTLC: pagos atascados

Ahora mismo hay otro problema que se está discutiendo en la [lista de correo](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2019-June/002029.html). Si envías un pago, uno de los saltos en la ruta de pago va a estar fuera de línea o no va a estar disponible. Para cancelar el pago y esperar a enviar otro tienes que esperar primero a que el bloqueo de tiempo de HTLC expire para que los fondos vuelvan al remitente original. Lo ideal sería que el remitente pudiera cancelar el pago sin tener que esperar.

# Schnorr Taproot HTLC: pagos cancelables

Puede volver a hacerlo gracias a la construcción del PTLC. El último secreto sólo va a ser revelado por Alice cuando Dave, el receptor de los fondos, va a reconocer que recibió cada paquete de pago. Si haces esto es realmente genial porque puede permitirte construir protocolos de nivel superior, algún tipo de corrección de errores hacia adelante. La idea es que vas a enviar más paquetes de los necesarios para cumplir con el pago. Gracias a esto va a mejorar la UX porque si uno de los paquetes falla todavía tienes más paquetes para pagar al beneficiario.

# HTLC: contrato simple con bloqueo de tiempo de hash

La última cosa que también podemos construir gracias a Schnorr... Ahora mismo los HTLCs son bastante geniales pero son bastante simples. Sólo hay un timelock, sólo hay un hash. Quizás la gente esté interesada en tener diferentes hashes. Uno de los hashes es presentado por un árbitro. Puede ser un árbitro en cualquier contrato. Soy Alice, estoy interesada en conseguir un envío de algunas mercancías. Hoy estoy financiando un pago pero nunca he recibido la mercancía. Usted puede insertar una plica en su HTLC. Haciendo esto significaría que cada parte de salto de la ruta de pago tiene que soportar el HTLC avanzado. Peor aún, va a aprender la semántica del contrato.

# Schnorr Taproot: contratos de punto de pago de extremo a extremo

Lo que puedes hacer en lugar de esto es tener construcciones de puntos de pago. La idea es que sigas utilizando scripts sin guión pero que añadas otras primitivas gracias a la agregación de claves o al ECDH. También puedes hacer DLCs, que no es más que un punto de curva. Es posible que podamos construir una clase más amplia de paquetes HTLC o paquetes de pago condicional. Preveo que en unos años la gente hará futuros u opciones sobre Lightning. Esta clase de pagos va a ser confidencial. Sólo los puntos finales van a saber de esto.

# Protocolo-marco, no hay bala de plata, un montón de trucos

Schnorr y Taproot, no es una bala de plata. Hay un montón de otras fugas como cuando usted está haciendo anuncios de canal en Lightning ahora usted está doxing a sí mismo mediante la vinculación de una identidad pubkey Lightning y onchain UTXO. Dentro de unos años la gente se va a despertar y dirá "Esta pubkey de Lightning estaba vinculada a un nombre de dominio". Entonces se podrá enlazar entre un nombre de dominio y un UTXO onchain lo cual es realmente malo. Incluso si hacemos PTLC para la ruta de pago todavía tenemos problemas con el delta CLTV que es el mismo en cada salto. Además, el importe sigue siendo el mismo menos las tasas de Lightning en cada salto. Lo ideal sería implementar otros trucos, como algoritmos de enrutamiento aleatorio de la delta de CLTV o rellenar la ruta de pago para utilizar siempre 10 o 20 saltos, aunque sea más costoso. Eso puede ser mejor para la privacidad. Ahora mismo la gente está trabajando en canales de doble financiación para Lightning. Es posible que hagamos Coinjoin para cada transacción de financiación, lo que sería realmente genial. Schnorr y Taproot van a tardar más de un año en integrarse en Lightning. Esto será sólo el comienzo para construir una privacidad realmente consistente para Lightning.

# El lado de la aplicación, la construcción de las primeras aplicaciones privadas

La privacidad va a ser el valor por defecto de Lightning, eso espero. Si vas a construir aplicaciones sobre esto deberías tener este enfoque holístico y pensar "Tengo este protocolo Lightning que me proporciona mucha privacidad. Intentaré no romper la privacidad de los usuarios de mi aplicación". Deberías pensar en la integración con Tor, el inicio de sesión sin identidad o los tokens sin identidad, ese tipo de cosas. Creo que es un reto para los desarrolladores de aplicaciones que construyen sobre Lightning, pero creo que vale la pena. Estoy emocionado, Schnorr y Taproot han sido propuestos como BIPs y deberían ser soft forked en el protocolo si la comunidad lo apoya. Si estás interesado en contribuir a Lightning eres realmente bienvenido.

# Gracias a Chaincode

Gracias a Chaincode por apoyar este trabajo. Gracias a avanzando con Bitcoin.

# PREGUNTAS Y RESPUESTAS

P - ¿Cómo ves la implementación de Taproot en Lightning? ¿Sigue siendo Lightning?

R - Hay varias maneras. Primero puede integrar Taproot para la salida de fondos. Luego puede utilizar Taproot para la parte de salida HTLC de la transacción de compromiso. También puede utilizar Taproot para la salida de la transacción HTLC de la segunda etapa. Hay por lo menos múltiples salidas que se puede tratar de Rayo. Creo que la primera es arreglar la salida de la financiación porque si se hace esto nos beneficiaremos de la suposición de Taproot. Usando Taproot para las transacciones de compromiso todavía va a filtrar que está utilizando Lightning. Tal vez podríamos utilizar la construcción de la piscina que estaba hablando, pero eso es algo más difícil. Yo perseguiría esto primero.

P - Has dicho que Lightning tiene garantías de privacidad en su protocolo pero que los desarrolladores deben asegurarse de no arruinar las garantías de privacidad sobre el protocolo base de Lightning. ¿Ve usted una tendencia a que las aplicaciones tomen atajos en Lightning y arruinen la privacidad?

R: Sí. Ahora mismo existe esta idea de [enrutamiento de trampolín](https://btctranscripts.com/lightning-conference/2019/2019-10-20-bastien-teinturier-trampoline-routing/) que quizás sea genial para la experiencia del usuario pero en el lado de la privacidad está roto. Lo que nos da mucha privacidad en Lightning es el enrutamiento de origen. Ir al enrutamiento de trampolín significa que la persona que hace el enrutamiento de trampolín para ti va a saber quién eres si estás usando un salto y peor va a saber a quién estás enviando fondos. Existe el enrutamiento trampolín, si no estás usando clientes Lightning que preserven la privacidad... Nadie ha hecho un verdadero estudio de privacidad en los clientes Lightning. Neutrino, filtros bloom, nadie ha hecho una investigación real. No son geniales, hay fugas de privacidad si los usas. Hay problemas de privacidad de Lightning y hay problemas de privacidad de la capa base. Si estás construyendo una aplicación deberías tenerlos todos en cuenta. Es realmente difícil. Usar la pubkey del nodo no creo que sea genial. Me gustaría que [rendez-vous routing](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2018-November/001498.html) se hiciera en Lightning para evitar anunciar mi pubkey, tener mi factura ligada a mi pubkey y que mi pubkey sea parte de Lightning. Y el anuncio del canal por supuesto. Espero que en algún momento tengamos algún tipo de prueba de propiedad para poder demostrar que soy dueño de este canal sin revelar de qué UTXO soy dueño.

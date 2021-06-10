---
title: LTB - Pieter Wuille, Jonas Nick (2019-06-09)
transcript_by: Michael Folkson
translation_by: Abel Armoa
categories: ['podcast']
tags: ['taproot', 'schnorr']
---

# Hablemos de Bitcoin<sup id="a1">[1](#f1)</sup> con Pieter Wuille y Jonas Nick – 9 de Junio de 2019

<https://twitter.com/kanzure/status/1155851797568917504>

Parte 1: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-400-the-tools-and-the-work>

Parte 2: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-401-the-tools-and-the-work-part-2>

Borrador de BIP-Schnorr: <https://github.com/sipa/bips/blob/bip-schnorr/bip-schnorr.mediawiki>

Borrador de BIP-Taproot: <https://github.com/sipa/bips/blob/bip-schnorr/bip-taproot.mediawiki>

Borrador de BIP-Tapscript: <https://github.com/sipa/bips/blob/bip-schnorr/bip-tapscript.mediawiki>

## Parte 1

Adam: En este episodio vamos a adentrarnos en uno de los cambios más importantes que llegarán pronto al protocolo de Bitcoin como BIPs o Propuestas de Mejora de Bitcoin<sup id="a2">[2](#f2)</sup>, con foco en Taproot, Tapscript y firmas Schnorr. Si nos sintonizas regularmente esta no va a ser la primera vez que escuches la mayoría de estas ideas generales, pero hoy queremos analizarlas en profundidad. Debido a eso es que estamos muy complacidos de tener con nosotros en la sesión de hoy a los desarrolladores de Bitcoin Pieter (mejor conocido como Sipa) y a Jonas Nick. Caballeros, muchas gracias por su tiempo y por estar hoy con nosotros.

Stephanie: Quiero sumarme a lo dicho por Adam. Muchas gracias por estar en el show con nosotros. Es realmente maravilloso discutir estas propuestas de mejora para Bitcoin y hablar con personas que realmente conocen el tema porque, de hecho, están involucradas en su desarrollo. Sinceramente les agradecemos por su tiempo. Para empezar quisiera preguntarles a ambos, Pieter y Jonas, ¿cómo fue la primera vez que escucharon sobre Bitcoin? ¿Cómo fue que se volvieron desarrolladores de Bitcoin? ¿Y por qué están interesados en estas propuestas en particular? Pieter, ¿quieres empezar tú?

Pieter: Creo que me topé con Bitcoin por primera vez a fines del 2010 en un canal de IRC acerca del lenguaje de programación “Haskell”, donde los participantes estaban hablando acerca del tema, y luego comencé a investigar por mi cuenta. Me dí cuenta de que en aquel tiempo tenía una placa de video en mi computadora que era capaz de minar Bitcoins. Fue divertido. En un principio solo me fijé en eso. El precio estaba muy bajo en aquel momento. Valía alrededor de veinte centavos.

Stephanie: ¿Y qué te entuciasmó de Bitcoin en aquel momento?

Pieter: Fue la lidea de que se podía tener una moneda definida por internet, por nada más que software. Siempre fue su tecnología lo que me atrajo, y su potencial de cambiar la manera en que pensamos el dinero.

Stephanie: ¿Y cuándo empezaste a desarrollar para Bitcoin?

Pieter: Creo que empecé a mirar el código a inicios del 2011. Creo que fue en el mismo momento en que SlushPool estaba empezando y estaban buscando realizar unos cambios en el código. Así que pensé, ¿por qué no echarle un vistazo? Un poco más tarde, en el foro de bitcointalk que en aquel momento creo que solo estaba en bitcoin.org, Hal Finney publicó un desafío: “Esta es una dirección de Bitcoin. En ella hay 5 Bitcoins (eran un puñado de dólares en ese momento). Y una clave privada. Cualquiera que pueda reclamar esos Bitcoins con esa clave privada se los puede quedar”.

Stephanie: ¿Ganaste?

Pieter: No, no gané. En aquel entonces el software existente para Bitcoin no permitía importar o exportar claves privadas, así que eso era algo nuevo. Empecé a pensar, ¿cómo podría incluir esta funcionalidad en el software de Bitcoin? Me tomó más tiempo que a otras personas que estaban intentando lograr lo mismo en Java o Python. Pero al final logré tener un parche para importar claves privadas en Bitcoin. Intenté integrarlo porque parecía una funcionalidad interesante. En ese momento comencé a hablar con Gavin Andresen, quien recientemente había asumido como persona a cargo del soporte del proyecto. Me parece que pasó medio año hasta que el parche fue integrado. Pero antes de que eso sucediera ya me habían pedido contribuir y empezar a revisar los parches de otras personas.

Stephanie: Eso es fascinante. Me gusta mucho tu historia. ¿Has estado desarrollando activamente durante todo este tiempo? ¿Y cómo fue que te interesaste por Taproot, Tapscript y las firmas Schnorr?

Pieter: Sí, he estado desarrollando todo este tiempo. Inicialmente sólo lo hacía en mi tiempo libre y luego, tan pronto me uní a Blockstream en 2014 pude hacerlo a tiempo completo. Desde entonces he trabajado en muchas cosas. Taproot y las demás cosas relacionadas son una continuación de la iniciativa sobre “Segregated Witness” que inició hace un par de años.

Stephanie: ¿Estás interesado en la escalabilidad y en la seguridad?

Pieter: Sí, por supuesto. La ventaja principal aquí es mejorar las cosas que iniciamos con “Segregated Witness”. Con esto en particular mejoramos el potencial de fungibilidad o intercambio, haciendo que todas las transacciones o al menos una gran parte de ellas sean más parecidas entre sí, siendo menos visible para el público en general qué es lo que realmente hacen las transacciones. Al mismo tiempo hay mejoras de escalabilidad. Son mejoras menores para las transacciones típicas. Tienen mayor impacto en transacciones más complejas, como transacciones multi-firma<sup id="a3">[3](#f3)</sup> o contratos inteligentes.

Stephanie: Vamos a hablar de los detalles técnicos en un rato. Muchas gracias por la introducción y por relatarnos tu experiencia. Ahora vamos con Jonas. ¿Cuándo fue la primera vez que escuchaste sobre Bitcoin y cómo fue que te involucraste como desarrollador Bitcoin?

Jonas: La primera vez que escuché sobre Bitcoin fue a inicios del 2011. Sucedió una burbuja, creo que alrededor de los 30 USD, y al instante estuve muy interesado en esta idea de utilizar una moneda con la cual nadie pueda detenerme y al mismo tiempo, mantener un cierto grado de privacidad al usarla. De hecho, en 2013 y 2014 yo escuchaba tu podcast regularmente. Allí escuché por primera vez hablar sobre cadenas paralelas y Blockstream. Lo busqué, fue en el [Episodio 99](https://letstalkbitcoin.com/e99-sidechain-innovation) con Adam Back y Austin Hill. Fue una gran influencia en aquel momento.

Stephanie: Es una historia genial.

Adam: Recuerdo aquella entrevista. Sin dudas presentaron ideas muy interesantes en aquellos inicios.

Stephanie: Y dinos Jonas, ¿cómo te iniciaste como desarrollador?

Jonas: Comencé a contribuir cuando estaba en la universidad. Ese mismo año estudié ciencias de la computación. Luego de eso, en 2015, me uní a Blockstream.

Stephanie: En este punto quisiera pasar a los detalles técnicos. Vamos a hacerles muchas preguntas. Creo que deberíamos iniciar por definir exactamente a qué nos referimos cuando decimos Taproot, Tapscript o firmas Schnorr. Hemos decidido iniciar con las firmas Schnorr y el motivo por el cual son importantes.

Pieter: Actualmente Bitcoin utiliza firmas ECDSA para permitir que las claves firmen las transacciones. Una dirección, al menos cuando es una generada con una sola clave, realmente es solo un hash de una clave pública ECDSA. Y cuando recibes monedas en esa dirección y deseas gastarlas, necesitas firmar usando la correspondiente clave privada ECDSA. El algoritmo ECDSA tiene una historia interesante, es el esquema de firmas DSA que es bastante común, migrado al mundo de la criptografía de curvas elípticas. El esquema de firmas DSA fue diseñado originalmente en gran medida como una manera de evitar la patente existente sobre las firmas Schnorr. Las firmas Schnorr fueron inventadas por Claus-Peter Schnorr creo. Con el correr del tiempo las personas fueron encontrando propiedades interesantes y cosas que se podían hacer con ellas. Pero lamentablemente él patentó la idea. Como resultado el mundo intentó estandarizar una alternativa que no estuviera patentada, que fue DSA. Luego vino ECDSA, y Bitcoin en sus inicios aparentemente tomó esta implementación. Así es que, en esencia, las diferencias entre ECDSA y la curva elíptica Schnorr no son grandes.



<sup id="a1">[1](#f1)</sup>


<a id="f1">[1]</a> "Let's Talk Bitcoin" [↩](#a1)
<a id="f2">[2]</a> “Bitcoin Improvement Proposals” [↩](#a2)
<a id="f3">[3]</a> “Multisig” [↩](#a3)

---
title: Seminario Socrático 6
date: 2020-02-24
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - taproot
---
<https://www.meetup.com/Austin-Bitcoin-Developers/events/268812642/>

<https://bitdevs.org/2020-02-12-socratic-seminar-101>

<https://twitter.com/kanzure/status/1232132693179207682>

# Introducción

Muy bien, vamos a empezar. Reúnanse. A Phil le vendría bien algo de compañía. A nadie le gusta la primera fila. Tal vez los bancos.  Así que tengo un formato un poco diferente de cómo quiero hacerlo esta semana. Normalmente cubro una amplia serie de temas que robo de la lista de reuniones de Nueva York. Revisando eso, pensé que había algo que parecía interesante que era las nuevas propuestas de taproot que finalmente fueron publicadas por Pieter Wuille.

Mi experiencia con los PBI es que pueden ser muy informativos porque son una especificación exacta, motivación y descripción de los cambios en el protocolo. Pero pueden ser muy densos y difíciles de leer, difíciles de entender, especialmente si eres un poco más nuevo. Siempre he pensado que estaría bien poder discutir estas cosas en grupo. La primera vez que te acercas a un BIP, eso sería mejor que tratar de entenderlo por ti mismo.

Eventualmente podríamos repasar los BIPs de segwit o los bips de cartera como bip32 los realmente importantes. Esta es una buena prueba. Tengo las cosas normales en cola aquí, así que si encontramos esto demasiado aburrido, entonces podríamos cambiar a eso. Háganme saber. Podríamos querer la pizarra. Si pudieras desplegar eso... podríamos encontrarlo útil.

# Presentaciones

((se omitio))

# bip340

<https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki>

La transcripción aquí puede ser aburrida porque sólo voy a leer el BIP. Hay tres BIPs: bip340 (bip-schnorr), bip341 (bip-taproot), bip342 (bip-tapscript). El último es el más corto, es cambios de script para taproot.

P: ¿Por qué? ¿Cuál es la razón breve de todo esto?

R: Hay una sección de motivación aquí. "Esta propuesta pretende mejorar la privacidad, la eficiencia y la flexibilidad de las capacidades del lenguaje de scripting de bitcoin sin añadir nuevos supuestos de seguridad. Intenta minimizar la fuga de información que tiene. Y permite las actualizaciones".

Bitcoin utiliza firmas ECDSA. Las firmas Schnorr tienen algunas ventajas. Tienen seguridad demostrable. Hay una prueba de seguridad de que no se pueden falsificar las firmas bajo un cierto conjunto de supuestos. Para dar una prueba equivalente en ECDSA necesitas suposiciones más fuertes. Hay una prueba matemática mejor de que las firmas no pueden ser falsificadas.  Es mejor tener una prueba de que algo no puede ocurrir.

Otro aspecto es la no maleabilidad. Hemos tenido problemas con la maleabilidad en el pasado. ¿Cuál es una buena manera de describir la maleabilidad? ((bryan explica)) Parece que es bueno tener no maleabilidad, pero ¿el principal beneficio es el antispam, o es que intentas demostrar que no tienes una clave privada... asumimos que la no maleabilidad es buena? Bueno, la maleabilidad dificulta tu contabilidad. Esto es lo que MtGox afirma que sucedió. Dijeron que la maleabilidad dificultaba que su sistema contabilizara los retiros duplicados, por lo que poco a poco fueron desangrándose los fondos durante meses, hasta llegar a las 8 cifras y nadie se dio cuenta. Así que otra razón es la simplicidad. Segwit resuelve la maleabilidad para el rayo. Si quiero firmar una transacción de reembolso por algo que aún no ha sucedido, te gustaría vivir en un mundo donde las firmas no afecten a los ID de las transacciones.

    17:30 < kanzure> en el bip de taproot, la no maleabilidad es una motivación: ¿por qué? segwit lo soluciona ¿no? me gusta la no maleabilidad por supuesto.
    17:41 < aj> kanzure: wtxid la maleabilidad sigue siendo agradable de evitar, al igual que el hecho de tener diferentes tamaños de datos de los testigos, lo que podría permitir a la gente malear su tarifa sobre p2p?
    17:48 < sipa> también la propagación de la tx se ve perjudicada por la maleabilidad, lo que contribuye indirectamente a la propagación de bloques en bloques compactos & co
    18:00 < kanzure> Gracias. Estamos en un seminario socrático en este momento :).

La linealidad (agregación de pubkeys) también es muy buena. Pero taproot no motiva realmente la agregación de claves por sí misma. Taproot podría utilizar multifirmas ECDSA dentro de cada rama.

Codificación de la firma - la gente tiene que poner bytes en la cadena de bloques y serializarla. ECDSA tiene esta codificación DER. Son 72 bytes. Podemos bajar a 64 bytes para las firmas Schnorr. Una clave pública es un par de números - son sólo 32 bytes. Sólo almacenamos esos dos números y nada más. Nos ahorramos al menos 8 bytes, eso es bastante bueno, mejor que el 10%.

En lugar de utilizar codificaciones comprimidas de 33 bytes de los puntos de la curva elíptica, en esta propuesta las claves públicas se codifican en 32 bytes. Es la coordenada x o y. Aquí sólo elegimos una de ellas. Es el par.

También están normalizando la forma de hacer la verificación de los lotes.

Completamente especificado- es determinista. Con ECDSA hay algunos problemas, como ver bip66.

El último punto es que bip-schnorr utiliza la misma matemática de curva elíptica secp256k1 para hacer las firmas y la verificación. También las mismas funciones hash. Podemos conservar los métodos existentes para los secretos y las claves públicas. No necesitamos nuevas formas de producir secretos o claves públicas, ni necesitamos nuevas suposiciones. Es la misma matemática detrás, sólo una forma diferente de aplicarla. ¿Alguna pregunta?

## Diseño bip340

Resumen de la firma Schnorr: <https://www.youtube.com/watch?v=FU-rA5dkTHI&t=18m40s>

diapositivas (diapositiva 21?): <https://docs.google.com/presentation/d/1QXZBtELcVMoCq6wx-rJr31KvtsqxxcWIewMvuSTpsa4/edit#slide=id.g24158d2d92_0_15>

((gracias tadge esto salvó nuestros culos colectivos aquí))

Este sistema criptográfico tiene unas cuantas funciones: generar la clave, firmar el mensaje, verificar el mensaje dada una firma y un mensaje. Así que Schnorr existe desde hace décadas; la cuestión es qué formato serializar esto para bitcoin.

Las firmas Schnorr pueden verificarse por lotes. La verificación por lotes aprovecha la propiedad de linealidad de schnorr. Esto hará que la descarga del bloque inicial sea un poco más rápida. El IBD todavía está limitado por la entrada y salida. No lo hará más lento, eso es seguro. "Elegimos la opción R porque soporta la verificación por lotes".

No entiendo la prefijación de la clave y los ataques relacionados con la clave. Vamos con retraso, así que vamos a saltarnos esta sección.

Hay varias formas de codificar el nonce temporal y el nonce público. Hay algunas formas diferentes. La primera es un poco más eficiente para la verificación, la tercera es más pequeña y resulta en un directorio de datos de bitcoin más pequeño, así que eligen la tercera opción. La contrapartida es que en lugar de ser rápido en la verificación, es más lento pero son menos datos los que tienen que mantener alrededor. Lo hacen incluyendo sólo la coordenada x.

También hay otra información sobre la serialización de las diferentes primitivas involucradas en las firmas Schnorr, incluyendo el residuo cuadrático.

Etiquetado como hashes...

    18:04 < kanzure> para los hashes etiquetados, ¿en qué situación se espera la reutilización del nonce? como los nonces de baja entropía...?
    18:04 < aj> ¿se refiere a la reutilización de etiquetas?
    18:05 < kanzure> "Por ejemplo, sin el hashing etiquetado, una firma BIP340 podría ser también válida para un esquema de firma en el que la única diferencia es que los argumentos de la función hash están reordenados. Peor aún, si la función de derivación del nonce de BIP340 fue copiada o creada independientemente, entonces el nonce podría ser reutilizado accidentalmente en el otro esquema filtrando la clave secreta".
    18:05 < kanzure> esto sólo sería cierto para los nonces de baja entropía, ¿verdad?
    18:05 < aj> o si el nonce es determinista
    18:06 < kanzure> Oh, ya veo, puedo ver formas en que los nonces deterministas entrarían en conflicto.

Pasemos a las aplicaciones. Firmas de adaptadores.... útiles para la privacidad en los relámpagos para que cada salto no revele las preimágenes o deje que los observadores sepan qué protocolo estaba ocurriendo realmente una vez que las cosas se encadenan. Bien, entonces sí. Genial.

Hay algunas cosas para firmas ciegas, es decir, protocolos en los que eres capaz de firmar algo sin saber cuál es el mensaje. Otro ejemplo es wasabi y samourai coinjoins donde no les das tus entradas, les das una versión encriptada de la misma, la firman, luego la revelas después de que la firmen. No saben quién registró cada entrada.

Tienen vectores de prueba y una implementación en python de esto. Esto es legible. Son 120 líneas. Es bastante loco, tal vez deberíamos haber leído esto en lugar de bip340.

Eso fue un BIP completo. No creo que haya ido muy bien. Lo admito. No sé si este es el mejor formato. ¿Qué piensan ustedes? Nos empantanamos un poco. Había una cosa que quería repasar. Estaba un poco confundido en ese momento. Una cosa que es interesante es que si buscas terrylab schnorr... es este interesante artículo que da ejemplos de rust-bitcoin para muchas de estas cosas. Este es un ejemplo de agregación de firmas. Si tienes dos pubkeys, puedes tomar la suma de ellas.....  La firma agregada se puede construir, es igual a la suma de las dos firmas. Esto es lo de la agregación de firmas. El problema de hacer esto es que básicamente hay un... puedes componer, estás haciendo algo con gente en la que no confías... si su pubkey .... el problema es que les dices que tu pubkey es la tuya menos la suya y eres capaz de restar tu clave pública. Musig ha resuelto este problema. Hay que ser inteligente en la forma de hacerlo. Musig es un intento de cómo resolver esto. La linealidad tiene algunas armas de pie.

# bip341

<https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki>

¿Quieres repasar el taproot? El bip de schnorr tardó mucho más de lo que esperaba. Taproot es un BIP más grande. Es realmente duro. Podríamos hacer un resumen ejecutivo tal vez. Hagamos motivaciones y aplicaciones.

Ya hemos leído la sección de motivación. Venden taproot como un intercambio que implementa algunas cosas anteriores (como bip114, bip117, etc, para MAST) y también algunas otras cosas como graftroot, g'root, etc.

Hay dos formas... tapscript puede ser dos cosas: puede ser como, estas pubkeys sumadas y hacer una firma con estas o puedes tener este árbol de diferentes condiciones de ejecución y eliges uno de estos caminos a lo largo del árbol y proporcionas una prueba o lo que sea. Esto ayuda a preservar la privacidad de tus otras condiciones de gasto. Tus tres primitivas son hashes, firmas o timelocks. Con esas tres cosas puedes construir cualquier árbol de condiciones que se te ocurra. Sin embargo, esas son las tres cosas con las que tienes que construir.

Introdujeron el anexo en el testigo, aún no se usa, pero podría usarse eventualmente. También se compromete con otra información en el sighash. Siempre se compromete con el scriptpubkey que supongo que no se utiliza en segwit bip141. La pubkey se incluye directamente en la salida. Este es un material bastante denso.

"Se dice que los hashes de clave pública protegen contra los adversarios cuánticos, pero la protección es muy débil. La resistencia real a estos sistemas puede ser introducida al basarse en diferentes supuestos criptográficos." Todas las monedas de Satoshi son de pago por clave pública, así que eso es interesante. Hay un montón de mejoras que se pueden hacer. Pay-to-pubkey puede ser utilizado como una identidad de comunicación en tor. Eso es interesante, no he escuchado eso. Esto cambia la narrativa que pay-to-pubkey no es necesariamente una cosa mala. Los ordenadores cuánticos van a romper esto de todos modos, así que hasta que tengamos algo mejor, deberíamos probar una variedad de criptosistemas.

No tendrás direcciones heredadas aquí. No puedes tener direcciones taproot heredadas. El uso de salidas envueltas en P2SH proporciona sólo 80 bits de seguridad contra colisiones debido al uso de un hash de 160 bits. La principal preocupación es que si es multipartita... si tienes una persona, si tienes 2 de 2, .... ellos tendrán la mitad del script de su pubkey. Todo esto es realmente en la maleza.

"¿Por qué el mensaje que firma incluye el scriptPubKey?" Esto evita que se mienta a los dispositivos de firma fuera de línea sobre la salida que se gasta. Esto demuestra a un monedero de hardware qué rutas de ejecución no utilizadas existen.

# bip342

<https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki>

Este incluye cambios en el sistema de scripts. Vamos a repasar esto rápidamente y luego iremos a por una barbacoa. Una de las cosas interesantes es que han reemplazado OP\_CHECKMULTISIG y OP\_CHECKMULTISIGVERIFY.. En la descripción no se decía nada de incompatibilidad con ECDSA, sólo se decía que es ineficiente y que este nuevo es batchable. ¿Podemos ver un ejemplo de OP\_CHECKSIGADD y verificación por lotes?

Usas CHECKSIGADD para obtener los 1's y 0's y los sumas para ver si los CHECKSIGs suman algún número. Después puedes hacer NUMEQUAL. Puedes hacer un lote de firmas y ver si el umbral es suficiente. Si tuvieras un 2 de 3 y un 2 de 3, sumarías las seis y verías si son cuatro. No estoy seguro de que la explicación es lo suficientemente fuerte en bip342 de cómo se supone que esto funciona frente a cómo solía funcionar.

Musig es cuando se suman firmas y pubkeys. Musig requiere 3 rondas de interacción. Puedes hacer k-de-n de forma asíncrona. Con musig, todo el mundo necesita comprometer nonces, y luego todos revelamos nuestros nonces y luego todos firmamos. Musig es el siguiente. Con musig sólo tienes una pubkey que representa todo y una firma al final, pero a costa de un protocolo complejo. En este, obtienes guiones más grandes pero no tienes interactividad.

La última es la firma nativa del umbral de Schnorr, pero se necesita un protocolo interactivo. Algunos de estos protocolos como Musig parecen realmente complicados.

Lamento que esto haya sido un poco desorganizado. Tal vez no utilicemos este formato en el futuro.


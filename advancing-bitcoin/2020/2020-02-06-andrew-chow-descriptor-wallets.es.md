---
title: 'Repensar la arquitectura de las carteras: Carteras de descriptores nativos'
speakers:
  - Andrew Chow
date: 2020-02-06
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - wallet
media: https://www.youtube.com/watch?v=xC25NzIjzog
---
Diapositivas: https://www.dropbox.com/s/142b4o4lrbkvqnh/Rethinking%20Wallet%20Architecture_%20Native%20Descriptor%20Wallets.pptx

Soporte para descriptores de salida en Bitcoin Core: https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md

Bitcoin Optech en los descriptores de la secuencia de comandos de salida: https://bitcoinops.org/en/topics/output-script-descriptors/

Bitcoin Core dev wiki sobre los cambios en la estructura de la cartera: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Wallet-Class-Structure-Changes

# Introducción

Hola a todos. Soy Andrew Chow, soy ingeniero en Blockstream y también colaborador de Bitcoin Core, trabajando principalmente en el monedero de Bitcoin Core. Hoy voy a hablar de repensar la arquitectura de los monederos con monederos descriptivos nativos. Pero primero para entender por qué necesitamos repensar la arquitectura de los monederos tenemos que entender lo que hace el monedero actual o lo que hacía antes supongo.

# Arquitectura de carteras antiguas

¿Cuál es la antigua arquitectura de carteras, al menos en Bitcoin Core? Tenemos una cosa que yo llamo el modelo de "bolsa de llaves". El monedero tiene un montón de llaves y hace un montón de cosas con esas llaves. Todo se centra alrededor de esas llaves y muchos monederos siguen lo mismo sólo que con un poco de variación de lo que producen con esas llaves. Lo que hacemos con esas claves es que tomamos una clave y las convertimos en direcciones y scriptPubKeys. Se toma una clave y se envuelve en un script para hacer un P2PKH scriptPubKey, hacer esa dirección y entregarla al usuario. Eso es lo que hacemos ahora. Pero el problema con esto, además de que una llave tenga múltiples direcciones, es que no es muy expansivo. No podemos usar una sola llave para hacer multisigs. No podemos dar direcciones multisig. Y no podemos dar direcciones que correspondan a scripts arbitrarios que hagan esa cosa rara del contrato que realmente quieres hacer. Así que la forma en que vamos a resolver esto es mediante el uso de las carteras descriptoras. Para ello tenemos que rediseñar la arquitectura de la cartera.

# Carteras de descriptores nativos

First what are native descriptor wallets? As the name suggests they store descriptors. What are descriptors? I will get to that in a minute or two. The thing with native descriptor wallets is they can store any kind of descriptor including multisig descriptors or in the future Miniscript. With native descriptor wallets we can have a wallet that hands out addresses for multisigs, for arbitrary scripts, basically whatever you want without the wallet software having to hardcode in what to do with keys or what kind of scripts to produce. We also use a specific type of descriptor called a range descriptor that lets us generate multiple things from a single descriptor.

# Output Script Descriptors

Ahora hablemos de los descriptores de salida propiamente dichos. Los descriptores de scripts de salida se llaman como sugieren, describen los scripts de salida. Pero también describen scripts de salida junto con todo lo que necesitas para resolverlos. Resolver es algo específico de Core, un término que definimos en Core. Significa que si tenemos firmas válidas o tenemos las claves privadas relacionadas con un script podemos producir un scriptSig de entrada válido. Esto significa que tenemos todos los scripts de redención y todos los scripts testigos que necesitamos para producir ese scriptSig. El descriptor de script de salida nos dirá toda esta información, no sólo cuál es ese script de salida. Los descriptores de scripts de salida también son legibles para los ingenieros. Un poco menos legibles que los humanos porque el usuario medio probablemente no será capaz de leerlos. Pero si entiendes la terminología de Bitcoin, el descriptor te dirá todo lo que necesitas saber. Si realmente quiere profundizar en los detalles específicos de los descriptores hay un [documento](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md) en el repo de Bitcoin Core que puedes ir a ver. Allí se explica todo con mucho más detalle.

# Ejemplos de descriptores

Estos son algunos descriptores. Pueden parecer muy confusos y puede ser un poco difícil de ver. Si te fijas bien al principio de cada uno tenemos cosas que son legibles como `pk` o `pkh` y `wpkh`. Para aquellos que conozcan la terminología de Bitcoin se darán cuenta de que significan clave pública o hash de clave pública y hash de clave pública de testigo. Es similar a P2PK y P2PKH. Simplemente eliminamos la parte P2 porque es un ruido extra. Realmente un descriptor es una función. Tenemos un nombre de función y la función del descriptor devuelve un script y toma algunos argumentos como lo harías en cualquier lenguaje de programación como C o Python. Los argumentos pueden variar. Algunos de ellos toman claves públicas, otros toman scripts, otros toman múltiples claves públicas, lo que sea. Vamos a entrar en un poco de detalle en uno de estos descriptores.

`￼pkh(02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7aba
c09b95c709ee5)#8fhd9pwu`

Este es un descriptor muy simple. Al principio ves que dice "pkh". Esto significa pubkey hash, es sólo el nombre de la función que devuelve. Esto te dice que devuelve un script de hash de clave pública. El argumento de esto es una clave pública, sólo una clave pública, nada especial. Al final tenemos una suma de comprobación. Esta suma de comprobación al final se basa en bech32. Esto significa que hay alguna detección y corrección de errores en caso de que, por alguna razón, usted esté escribiendo esto a mano. Aunque no estoy seguro de por qué querrías hacer eso. A partir de este descriptor ahora conocemos el scriptPubKey. Es esta cosa.

`76a91406afd46bcdfd22ef94ac122aa11f241244a37ecc88ac`

Y conocemos la dirección que está ahí arriba también.

`1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP`

Estos son correctos, los he calculado. Pero además de conocer este script de salida también sabemos lo que necesitamos para producir esa firma válida. Necesitamos tener esa pubkey y necesitamos tener la clave privada de esa pubkey. Como sabemos que tenemos esa pubkey, es posible resolverlo. Aquí hay un ejemplo un poco más complicado.

`pkh([d34db33f/44'/0'/0']xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS
1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGR
jaDMzQLcgJvLJuZZvRcEL/1/*)#ml40v0wf`

Este tipo de descriptor es el que vamos a incluir en nuestra cartera. Este, al igual que el ejemplo anterior es `pkh`. Pero notarás que el argumento de la clave pública es mucho más largo y complicado. Primero tenemos esta cosa de corchetes. Esto es para la información del origen de la clave. Hablaré de eso un poco más tarde. Luego tenemos un xpub con el que estoy seguro que muchos de ustedes están familiarizados. Luego tenemos una cosa al final que es en realidad alguna información de derivación. Y, por supuesto, la suma de comprobación. ¿Qué es esta información de origen de la clave en nuestros corchetes? Se basa en las rutas de derivación. Se parece mucho a una. En lugar de la m al principio, como verías en una ruta de derivación, tenemos esta cosa llamada huella digital. La huella digital es sólo los primeros cuatro bytes del hash160 de la clave pública maestra. En este ejemplo es `d34db33f`. Eso es sólo un identificador de la clave pública maestra. Después está el resto de la ruta de derivación `44'/0'/0'`. Lo que esto nos dice es que este xpub se deriva de una clave pública maestra con la huella digital `d34db33f` en la ruta de derivación `m/44'/0'/0'`. Después de nuestro xpub hay más información de derivación. El descriptor `/1/*` nos dice dónde derivar más claves. Lo que este descriptor nos está diciendo es que aunque le hayamos dado una sola clave, en realidad podemos producir una tonelada más de claves a partir de ella y por lo tanto muchos, muchos scriptPubKeys a partir de ella. Los scripts resultantes que obtengamos tendrán claves públicas derivadas de d34db33f en m/44'/0'/0'/1/i que si estás familiarizado con BIP 44 es una ruta de derivación estándar de BIP 44. Los llamamos descriptores de rango. Los más astutos habrán notado que esto sólo produce un tipo de scriptPubKey. Sólo produce `pkh`. También sólo produce claves en una cadena de derivación específica. Esto no cubre tus direcciones de cambio y si quisieras usar SegWit no puedes hacerlo con este descriptor en particular. En nuestras carteras descriptoras hicimos el enfoque perezoso y sólo tenemos seis de ellas.

# Descriptores almacenados

Hay uno para cada tipo de dirección. Hay una `pkh`, una `sh(wpkh)` y una `wpkh`. Y uno de cada uno de esos tres para cambiar y recibir direcciones. Pero lo bueno aquí es que no estamos limitados a estos tres tipos de descriptores. Puedes reemplazar, por ejemplo, el `wpkh` por `wsh(multi)` si quieres tener direcciones bech32 multisig.

# Ventajas de los monederos de descriptores

Esa es una de las cosas buenas de las carteras de descriptores. Son ampliables, podemos cambiar uno de los descriptores por otro diferente y podemos seguir obteniendo direcciones para ello. El monedero en sí mismo no necesita saber cómo firmar ese multisig que has puesto ahí porque el descriptor te dice cómo firmarlo. Otra cosa sobre los monederos con descriptor es que esos descriptores son completamente inequívocos en cuanto a las rutas de derivación que estás usando y qué tipo de dirección estás produciendo. Esto significa que si quieres importar un descriptor a otro monedero no tienes que adivinar qué ruta de derivación va a utilizar y no tienes que adivinar qué tipo de dirección va a utilizar. El descriptor te dice exactamente lo que va a producir. Eso significa que podemos deshacernos de [walletsrecovery.org](https://walletsrecovery.org/). Eso facilita las copias de seguridad. Tenemos todo lo que necesitamos en una sola cadena o supongo que en un par de cadenas que puedes juntar. Esa suma de comprobación también los hace portátiles en caso de que decidas escribirlos a mano por alguna razón.

# Implementación de carteras de descriptores

¿Cómo conseguimos monederos con descriptor en Bitcoin Core? En Bitcoin Core todavía tenemos este modelo de bolsa de llaves y la forma en que se implementa está muy ligada a la cartera. Es difícil separarlo. Durante los últimos meses he estado trabajando en un proyecto dentro de Core para abstraer primero algunas partes del monedero. Específicamente hemos estado abstrayendo esta clave y la gestión de scriptPubKey en un nombre muy obvio [ScriptPubKeyMan](https://github.com/bitcoin/bitcoin/pull/17261). Esta abstracción significa que tomamos todas las claves y la forma en que se producen las scriptPubKeys y las metemos en su propia caja donde puede hacer sus propias cosas y donde podemos cambiar cómo se producen las scriptPubKeys. En realidad, lo que le interesa a la cartera son las scriptPubKeys, no las claves en sí. Las claves son sólo datos extra que están relacionados con las scriptPubKeys. Así que lo que este modelo significa es que nos estamos alejando del "Toma una llave y haz un script con ella". Estamos cambiando a "Aquí hay un script. ¿Qué necesitamos para firmarlo?" Con esta refactorización nuestra clase principal de cartera `CWallet` sólo contendrá gestores de scriptPubKey y pedirá a los gestores de scriptPubKey nuevas scriptPubKeys. Cuando necesite firmar una transacción, simplemente se la pasará al gestor de scriptPubKey y éste averiguará lo que hay que hacer para firmar las scriptPubKeys. Esto significa, por supuesto, que podemos cambiar lo que hay dentro. Obviamente tenemos la cosa vieja que hacemos, metida en su propia cosa que llamamos `LegacyScriptPubKeyMan` porque es código heredado. Y tenemos una cosa nueva para los descriptores de script de salida. Tendremos un script de salida `DescriptorScriptPubKeyMan`. Este gestor de scriptPubKey de salida utilizará nuestros descriptores para producir scriptPubKeys. Nuestros descriptores nos dicen cómo firmar, así es como el gestor scriptPubKey sabe cómo firmar todo. Si estás interesado en más detalles, hay un [documento](https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Wallet-Class-Structure-Changes) en la [wiki](https://github.com/bitcoin-core/bitcoin-devwiki/wiki) de desarrolladores de Bitcoin Core que nadie sabe que existe.

# Estado actual de las carteras de descriptores

Entonces, ¿en qué punto estamos ahora con la incorporación de todo esto en Core? Por lo que sé, ningún monedero utiliza aún los descriptores, lo que es una pena. Core lo está consiguiendo poco a poco, pero requiere mucho trabajo. Creo que algunos otros monederos también lo tienen en su hoja de ruta, pero hasta ahora nadie utiliza descriptores todavía. Pero en Core hemos hecho esta refactorización así que nos estamos acercando bastante. La refactorización en `CWallet` y `LegacyScriptPubKeyMan` fue [fusionada](https://github.com/bitcoin/bitcoin/pull/17261) la semana pasada después de haber escrito estas diapositivas. Pero bueno, se fusionó. Hay un [PR](https://github.com/bitcoin/bitcoin/pull/16528) abierto que introduce nuestro `DescriptorScriptPubKeyMan`. Esperamos que se fusione dentro de unos meses. Tal vez a finales de este año tendremos carteras de descriptor. Aunque parece que esto es lo más cercano a los monederos con descriptor en el espacio de Bitcoin, espero que alguien más se ponga al día y llegue a esto antes que nosotros en Core. Pero, al menos, los monederos con descriptor y nuestra refactorización completa convertirán a Core en un monedero más moderno y se pondrá al día con el resto de monederos. También nos permitirá avanzar más rápido en el futuro.

# Preguntas y respuestas

P - Aprecio que sea legible por los ingenieros, pero me preguntaba si han pensado en proporcionar también la codificación bech32 o la codificación para pasar de una cartera a otra. Podría ser más fácil codificar en un código QR o para moverse. ¿Tendría sentido codificar todo el descriptor como dirección bech32?

R - Se ha hablado de codificarla de alguna manera. Específicamente bech32, no creo que tenga sentido allí porque bech32 no está optimizado para este tipo de cadena. Por eso tenemos una suma de comprobación al final. Eso se basa en bech32 y esa suma de comprobación está optimizada para los propios descriptores. Hubo una sugerencia de codificar en base64 todo el descriptor y llamarlo alguna cadena mágica y entregarlo a los usuarios si querían importarlo.

P - Dentro de los monederos HD en los BIPs correspondientes hay una descripción de un lookahead de 20 llaves. Cuando un monedero intenta reconstruir la estructura después de haber encontrado esa cantidad de llaves sin dinero, se rinde. ¿Hay algo más inteligente que los descriptores puedan añadir a eso?

R - No.

P - En BTCPay cuando lo empecé el concepto de descriptores de salida no existía así que escribí el mío propio que llamé DerivationScheme. Estoy considerando tratar de alejarse de esto y más en este lenguaje descriptor de salida. Pero el principal problema que tengo es que como no está fusionado y mucha gente no confía en él, significa que si lo hago ahora hay muchas posibilidades de que el lenguaje evolucione. Si evoluciona, podría romper mis cosas de forma muy grave. Esa es la razón por la que todavía no voy a entrar en esto. ¿Crees que ahora mismo es lo suficientemente estable y estás seguro de que no se moverá y romperá pronto?

R - Todo lo que está implementado actualmente es muy poco probable que cambie aunque no haya un BIP para ello ni nada. Lo que existe ahora, los ejemplos que he mostrado, probablemente no van a cambiar en absoluto. Pero los descriptores serán mejorados. Se añadirán cosas como Miniscript. Se añadirán más funciones, pero las cosas tal y como están ahora no van a cambiar.

P - ¿Por qué no hay un hash del chaincode en el xpub?

R - El xpub incluye un código de cadena.

P - El hash de la pubkey, ¿es sólo para verificar o hacer una doble comprobación?

R - Lo de la huella digital, me refería al hash de la pubkey. Eso está ahí como identificador. Es especialmente útil en los PSBTs, porque un PSBT tiene que contener la huella digital de la clave pública maestra para identificar al firmante. Lo hemos añadido a los descriptores porque es útil.

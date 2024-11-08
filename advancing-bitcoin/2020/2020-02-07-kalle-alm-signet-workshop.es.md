---
title: Taller Signet
speakers:
  - Kalle Alm
date: 2020-02-07
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - taproot
  - signet
---
# Preparémonos

```
mkdir workspace
cd workspace
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git remote add kallewoof https://github.com/kallewoof/bitcoin.git
git fetch kallewoof
git checkout signet
./autogen.sh
./configure -C --disable-bench --disable-test --without-gui
make -j5
```

Cuando intentes ejecutar la parte de configuración vas a tener algunos problemas si no tienes las dependencias. Si no tienes las dependencias busca en Google tu sistema operativo y "Bitcoin build". Si tienes Windows no tienes suerte.

```
cd ..
git clone https://github.com/kallewoof/btcdeb.git
cd btcdeb
git checkout taproot
./autogen.sh
./configure -C --enable-dangerous
make -j5
```
En tu carpeta src deberías tener bitcoind, bitcoin-cli y un par de binarios. Si ya has terminado con esta parte, puedes ir a tu carpeta src y escribir `./bitcoind -signet` y pulsar enter.

Si has conseguido sincronizar Signet hazlo:

`./bitcoin-cli -signet getnewaddress`

Deberías obtener una dirección `sb1...`. Publica esta dirección en el grupo de Telegram.

P - ¿Hay que estar totalmente sincronizado para obtener una nueva dirección?

R - No es así.

`./bitcoin-cli -signet getbalance`

`ssh gcog`

`cd workspace/signet/src`

`./bitcoin-cli -datadir=$HOME/signet-sgniii getrawtransaction 4b9911….88c7 1`

`bitcoin-cli -datadir=$HOME/signet-sgniii sendtoaddress sb1…5spr 100`

`cd contrib/signet`

`./mkblock.sh ../../src/bitcoin-cli -datadir=$HOME/signet-taproot`

`./bitcoin-cli -signet getbalance`

`./bitcoin-cli -signet getunconfirmedbalance`

Alguna persona por ahí montó su propio Signet así que estamos recibiendo bloques para ello.

`./bitcoin-cli -signet getconnectioncount`

`./bitcoin-cli-signet getblockcount`

`./bitcoin-cli-signet getpeerinfo`

Ahora mismo tengo una red que funciona con Signet Taproot. Al final nos cambiaremos a ella. Si vas a ir al taller de hardware de Stepan Snigirev esta tarde, lo cual te recomiendo que hagas, entonces podrás seguir usando la configuración de Signet Taproot que tienes con monedas y todo en su taller con una cartera de hardware.

`./bitcoin-cli -signet settxfee 0.00001`

`./bitcoin-cli -signet sendtoaddress sb1….8mg 1`

Estoy enviando a todos 1 Signet Bitcoin. Si vas al [explorador de bloques de Signet](https://explorer.bc-2.jp/) copia la cadena de texto `AddToWallet` y ponla en el explorador de bloques. Deberíais ver que está sin confirmar, las tarifas, etc.

# btcdeb

Voy a pasar a la parte de btcdeb. Este es el depurador de Bitcoin que mantengo. Tiene soporte experimental para Taproot así que me imaginé que podíamos usarlo.

```
cd ..
git clone https://github.com/kallewoof/btcdeb.git
cd btcdeb
git checkout taproot
./autogen.sh
./configure -C --enable-dangerous
make -j5
```

P - Tengo un problema con un archivo de configuración.

R - Es posible que tenga que eliminar la bandera -C.

P - ¿Qué hace la bandera -C?

R - Acelera la configuración cuando se ejecuta varias veces porque se almacenan en caché todas las salidas. Pero creo que hay un problema con libsecp que hace que esto sea un problema la primera vez. Puedes prescindir de -C.

# Controles remotos

Su bifurcación de Bitcoin Core git@github.com:user/bitcoin.git

Upstream https://github.com/bitcoin/bitcoin.git

Función de control remoto https://github.com/owner/bitcoin.git

```
origin git@github.com:kallewoof/bitcoin.git (fetch)
origin git@github.com:kallewoof/bitcoin.git (push)
sipa https://github.com/sipa/bitcoin.git (fetch)
sipa https://github.com/sipa/bitcoin.git (push)
upstream https://github.com/bitcoin/bitcoin.git (fetch)
upstream https://github.com/bitcoin/bitcoin.git (push)
```

Ahora mismo Signet no está en Bitcoin Core, lo que causa complicaciones. El [Signet PR](https://github.com/bitcoin/bitcoin/pull/18267) está en la categoría de [bloqueadores de alta prioridad](https://github.com/bitcoin/bitcoin/projects/8) por lo que esperamos que esté en la versión 0.20 que se supone que será lanzada en mayo. Hasta entonces tenemos que hacer malabares con los repositorios de GitHub. Eventualmente podrás usar el Signet por defecto con cualquier característica personalizada soportada. Con Taproot o OP_CHECKTEMPLATEVERIFY o cualquier bifurcación suave potencial, en el futuro si hay cualquier bifurcación suave, tan pronto como se agregan al minero Signet que es sólo una máquina, cualquiera puede activar y desactivar estos como quiera. Si quieres minar Taproot puedes coger la rama Taproot. Puedes enviar transacciones de Taproot y puedes recibirlas. Ahora mismo es un poco manual. Intentaremos crear un Signet personalizado para la gente de aquí. Escogeremos una persona que sea el minero o un par de personas. Podríamos hacer uno de todos aquí si quisiéramos. Yo diría que sólo elija un minero. No sé si usted está familiarizado con el uso de GitHub, pero hay algo que se llama un remoto. Por defecto sólo hay un remoto, se llama origen. Es lo que escribes después de git clone. Pero puedes añadir remotos. Puedes hacer `git remote add name URL` y entonces tendrás otro remoto.  Puedes hacer `git fetch remote-name` y lo obtendrás. En este caso estoy creando una red Taproot Signet. Tengo mi origen que es mi repositorio de Bitcoin. Debido a que estoy usando `git@github` aquí soy capaz de utilizar claves RSA en lugar de tener que introducir una contraseña todo el tiempo. Estoy añadiendo este remoto sipa porque sipa es la persona que está haciendo el trabajo en progreso Taproot [pull request](https://github.com/bitcoin/bitcoin/pull/17977). No tienes que añadir esto, podrías tirar directamente del pull request pero esto es en cierto modo más fácil. Usted puede tirar directamente. Upstream es Bitcoin, realmente no necesitas upstream en este caso. En tu caso sustituirías el origen kallewoof por tu nombre.

# Ramass

Debido a que Signet no está fusionado todavía, hay una rama `signet`. Tan pronto como se fusione con Bitcoin Core ya no tendremos eso. En nuestro GitHub creamos una rama de Signet y luego creamos una rama `signet-vanilla-taproot` (signet y parámetros de red). Tenemos una rama `taproot` que es la de sipa. Luego creamos una rama `signet-taproot`. Esta es la característica (`taproot`) fusionada sobre `signet-vanilla-taproot`.

# Ramas (después de la fusión de firmas)

Una vez que se fusione no tendremos una rama `signet`.

# Ramas (futuro)

En el futuro sólo tendremos una rama de característcas (`taproot`) (característica de los parámetros de signet). Hoy en día va a ser un poco quisquilloso, pero vamos a ver hasta dónde llegamos.

# La rama signet

Nosotros ya hemos hecho esta parte y tú ya deberías haber construido esta rama.

(Puede añadir https://github.com/kallewoof/bitcoin.git como remoto y luego recuperarlo y simplemente comprobar la rama de signet)

```
git remote add kallewoof https://github.com/kallewoof/bitcoin.git
git fetch kallewoof
git checkout signet
```

(También puedes obtener la solicitud de extracción directamente desde el sitio web de Bitcoin)

```
git fetch upstream pull/16411/head:signet
git checkout signet
```

# La rama signet-vanilla-feature

(Creamos esto una vez y luego basamos nuestra rama signet-feature en ella. Si acabamos queriendo reajustar signet-feature lo hacemos recreando en base a esta rama).

Desde la rama signet hazlo

`git checkout -b signet-vanilla-taproot`

(Y luego ajustar el archivo chainparams.cpp (lo hacemos más tarde)

Ahora mismo estamos en la rama signet. Lo que queremos hacer es cambiar un poco los parámetros de la cadena. Si usamos signet justo después de esto va a usar todo el signet que no tiene soporte de Taproot. Si vamos a crear un Signet personalizado para la característica propia, o la característica de sipa, necesitamos primero ajustar algunos parámetros de la cadena. Creamos esta rama aquí `signet-vanilla-taproot`.

P - ¿Esto está en el repo de Bitcoin?

R - Sí. btcdeb ya está configurado para trabajar con esto.

Si lo has hecho, ahora deberías tener una rama llamada `signet-vanilla-taproot`. No vamos a hacer nada con ella ahora, pero sí vamos a cambiar los parámetros de la cadena más adelante.

# La rama de características

(Mantenemos esto idéntico al propietario (aquí "sipa") y nunca divergimos:

```
git remote add sipa https://github.com/sipa/bitcoin.git
git fetch sipa
git checkout taproot
git pull
git reset --hard sipa/taproot
```

sipa es Pieter Wuille, por cierto.

P - ...

R - Algún otro Signet estaba técnicamente conectado a nosotros. Puedes salir si quieres o puedes mantenerlo en funcionamiento por ahora.

`git checkout signet-vanilla-taproot`

Ya hemos creado esta rama `signet-vanilla-taproot`, compruébala. No creo que vayamos a tener tiempo de hacer nuestra propia cadena así que vamos a utilizar una que ya he hecho. En el Telegram publiqué este fragmento de código de chainparams.cpp. En el editor que quieras si abres este archivo (chainparams.cpp) y luego bajas a buscar la clase llamada `SigNetParams`. Hay este caso si aquí y dentro de aquí son los parámetros por defecto de Signet. Quieres borrar todo eso y luego poner esto en su lugar. Lo he puesto en el Telegram para que no tengas que escribirlo manualmente.

```
LogPrintf("Using default taproot signet network\n");
bin = ParseHex("512103ad5e0edad18cb1f0fc0d28a3d4f1f3e445640337489abb10404f2d1e086be430210359ef5021964fe22d6f8e05b2463c9540ce96883fe3b278760f048f5189f2e6c452ae");
genesis_nonce = 280965
vSeeds.push_back("178.128.221.177");
```

P - ¿En qué rama está esto?

R - signet-vanilla.

Voy a repasar rápidamente lo que es esto. La parte `bin` es el reto. Probablemente lo reconozcas. Parece un script normal de Bitcoin. Lo que hace es un 1 y un push de 33 bytes y una pubkey y un 1 y un CHECKMULTISIG. Es un MULTISIG 1-de-1. La segunda parte es un genesis nonce, ya hablaré de eso. La tercera parte es una semilla, el ordenador que está ejecutando esta versión de Signet.

`git commit -am “new signet parameters”`

Debe confirmar su repositorio signet-vanilla-taproot con sus nuevos parámetros. Una vez que tenga eso puede fusionar esto con taproot. Cuando lo ejecutamos deberíamos ser capaces de usar Taproot.

Q - ...

R - No es necesario compilar ahora mismo. Si quieres compilar es probablemente una buena idea para asegurarte de que no tienes ningún error.

Comprobamos que el sello de la raíz.

`git checkout -b signet-taproot`

Y luego hacemos el `git merge taproot`. Si ya has hecho `git checkout -b signet-taproot` es posible que quieras hacer `git merge signet-vanilla-taproot` primero. Cuando lo hayas hecho, haz `git merge taproot`.

(Combinamos taproot sobre signet-taproot)

Cuando hagas el `git merge taproot` vas a tener conflictos. Necesitas ambas partes, pero elimina el programa testigo de verificación en la primera parte.

La razón por la que te estoy haciendo pasar por esto es porque esto es exactamente lo que vas a tener que hacer si alguna vez tienes una característica que quieres fusionar. Tendrás estos conflictos de fusión que aparecen. Ahora estamos en la parte donde nuestro Signet está trabajando. Si consigues compilar esto y ejecutarlo, se bloqueará. La razón por la que se bloquea es porque se está ejecutando un Signet antiguo. Usted quiere borrar la carpeta de Signet en su Data. Vamos a hacer eso. Detenga su bitcoind en ejecución.

`rm -rf ~/.bitcoin/signet`

Para Macs:

`rm -rf ~/Library/Application\ Support/bitcoin/signet`

Elimina esa carpeta. Debería estar en la rama `signet-taproot`.

`make`

Una vez que haya terminado de hacer:

`./bitcoind -signet`

Si te acordaste de borrar la carpeta de Signet en tus datos ahora debería conectarse a un Signet diferente que tiene Taproot. Este comenzó en enero de 2020. Si usted estaba de vuelta en 2019 que está utilizando el anterior Signet.

`./autogen.sh`

`./configure -C --disable-test --disable-bench --without-gui`

Si te encuentras con errores de compilación es posible que tengas que `./autogen.sh` y `./configure` de nuevo y luego `make clean`.

# btcdeb

Mientras esperamos algunas cosas del compilador tomemos los últimos minutos para ver si podemos hacer algo con esto. Tenemos la carpeta btcdeb.

`cd btcdeb`

Hay un hombre `tap` aquí que tiene un montón de características.

`./tap`

La tarea es usar a este hombre para crear una dirección de Taproot y enviármela. Si me la envías, te enviaré algunas monedas. Todo esto es experimental y nuevo. Si haces esto y te encuentras con problemas, tienes bugs lo que sea, eso es invaluable para la comunidad Bitcoin. Te animo a que lo hagas. Incluso puede ser capaz de hacer una contribución al actual [pull request](https://github.com/bitcoin/bitcoin/pull/17977), el trabajo en progreso Taproot pull request en el repositorio de Bitcoin Core. Si la gente juega con este material y lo rompe, entonces podemos mejorar ese pull request. Pero todo es muy nuevo y experimental. Puedo mostrarte un ejemplo. No sé si has usado btcdeb antes. Esta versión de btcdeb puede manejar los gastos de BIP-Taproot.

`./btcdeb --txin=$txin --tx=020000…`

Lo que estoy haciendo es decir "Esta es la transacción de entrada aquí y luego esta es la transacción y dime qué pasa". Dice que esta es una transacción SegWit y da los datos de la transacción. Entonces aquí llegamos al `Taproot commitment`. Esto tiene el objeto `control`. ¿Has oído hablar de MAST? Esto es MAST implementado en Taproot. Lo que hace Taproot es usar MAST para probar que un script particular, este `script`, fue realmente añadido a la dirección en el momento de la creación. Cuando creas la dirección puedes insertar cualquier cantidad de scripts que quieras pero nadie va a ver los scripts a menos que los uses para gastar. En este caso estoy usando este para gastar la transacción. El objeto `control` está diciendo que usas estos datos para derivar la raíz del árbol de Merkle. Si tienes una raíz del árbol de Merkle y coincide, entonces ese script fue comprometido. El objeto `control` tiene un byte de versión y luego es seguido por una pubkey. Las pubkeys en Taproot son de 32 bytes. Si está acostumbrado a las pubkeys en Bitcoin en general son de 33 bytes. Tienen 02 o 03 seguido de un valor hexadecimal. Quitamos el 02 o 03 y se asume que son de un tipo particular. Luego hay un `program`. Hay `p` y `q`. `p` es la pubkey interna utilizada para crear este gasto de Taproot. Luego hay algunas cosas de la raíz de Merkle que se van. Lo que btcdeb hace aquí es pasar por esta fase de compromiso. Hay esta `final k` aquí y luego hay un `TapTweak`. Hay un `CheckPayToContract` aquí. Este script sólo tiene una entrada por lo que no tiene un árbol de Merkle en absoluto. Una vez que esto termina con la comprobación del compromiso de Taproot vemos que el script se ejecuta. Es OP_SHA256, OP_EQUALVERIFY y luego hay una pubkey y un OP_CHECKSIG. Esto es como lo normal.

`btcdeb> step`

Este es el resultado del OP_CHECKSIG. Puedes ver algunas cosas aquí. Es una pubkey de 32 bytes por lo que es un `schnorr sig check`. Esta pubkey es diferente de la pubkey interna que dimos. Esto es parte del script, esta es la pubkey de Alice. La pubkey interna es la pubkey de todos que comparten. Hacemos el `VerifySchnorrSignature` y eso funciona. Hay un [documento](https://github.com/bitcoin-core/btcdeb/blob/taproot/doc/tapscript-example-with-tap.md) donde voy a través de un ejemplo que tiene dos scripts diferentes. [Este](https://github.com/bitcoin-core/btcdeb/blob/taproot/doc/tapscript-example-with-tap.md) es el script normal de Bitcoin. En lugar de hacer esta cosa OP_IF OP_ELSE OP_ENDIF tomamos esto y el CHECKSIG como un script y tomamos esto y el CHECKSIG como el otro script. Cuando lo pasamos no tenemos que mostrar al mundo todo esto. Solo probamos que esto era una posibilidad y lo satisfacemos.


P - ¿Esta es la parte del árbol de Merkle? No proporcionas todo el script, sólo proporcionas la ruta que estás ejecutando..

R - Sí. Esto funciona exactamente como la raíz Merkle dentro de las transacciones, excepto que hay algunos ajustes con los bytes de versión y otras cosas.

Si lo miras así, no estás ahorrando mucho espacio, pero tienes que recordar que estas cosas son todos blobs grandes, valores de 32 bytes. Si miras aquí ves que esta cosa es bastante grande. Si no tienes que mostrar uno de estos estás ahorrando espacio y ahorrando tasas. Es una gran mejora. Si todo el mundo está de acuerdo puedes gastarlo como si fuera una pubkey normal. Eso es un gran ahorro de privacidad y de tasas. Nadie va a poder separar tus cosas personalizadas con una pubkey normal si todos están de acuerdo. Piensa en un canal de pago en Lightning, ¿cuántas veces la otra persona no está de acuerdo en cerrar un canal? Por lo general, son como "Ok". Normalmente se utiliza la clave pública y se acaba con ella. En este ejemplo yo tengo la clave privada, normalmente no la tienes. La forma de hacerlo es usar MuSig o algo así para crear la clave privada interna. De esta manera nadie sabe realmente la clave privada, pero todavía se puede gastar. No llegué tan lejos como esperaba pero espero que al menos tengas un comienzo.


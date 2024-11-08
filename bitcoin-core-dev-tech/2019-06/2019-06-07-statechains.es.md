---
title: "Cadenas de estado ciegas: Transferencia de UTXO con un servidor de firmas ciegas"
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags: ['statechains', 'eltoo', 'channel-factories']
date: 2019-06-07
speakers: ['Ruben Somsen']
---
<https://twitter.com/kanzure/status/1136992734953299970>

Formalización de Blind Statechains como servidor de firma ciega minimalista <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-June/017005.html>

Visión General: <https://medium.com/@RubenSomsen/statechains-non-custodial-off-chain-bitcoin-transfer-1ae4845a4a39>

Documento statechains: <https://github.com/RubenSomsen/rubensomsen.github.io/blob/master/img/statechains.pdf>

Transcripción anterior: <http://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/statechains/>

## Introducción

Voy a hablar casualmente de todo el asunto de las cadenas de estados. Si quieres intervenir, por favor hazlo. Voy a empezar. La idea actual es hacerlo completamente ciego. Es blinded statechains. El objetivo es permitir a la gente transferir un UTXO sin cambiar nada en la cadena. El concepto que utilizo para describirlo es un servidor de firma ciega. La idea es que el servidor sólo tiene dos funciones: puedes generar una nueva clave para un usuario, que es algo así como generar un nuevo llavero y es una cadena lineal que sólo va en una dirección y no puedes dividir las monedas, y puedes solicitar al servidor una firma ciega y apuntar al siguiente usuario que obtiene el siguiente usuario solicitado que es como llega a ser una cadena.

El usuario hace el trabajo pesado. El servidor sólo firma las cosas. Podría haber un usuario con una sola clave, pero esa clave podría ser una firma umbral y ser una federación. En lugar de 2-de-3, podría ser 3-de-5 más una persona más que siempre tiene que firmar.

## Ejemplo

sigUserB(blindedMessageB, userC) es el usuario que pone una firma en un mensaje cegado y en el siguiente usuario que llegará a solicitar el siguiente mensaje. El mensaje cegado es firmado por el servidor, con la clave. Devuelve firma ciegaB. El dinero va de A a B. Lo repites para llegar de C a D usando sigUsuarioC(mensajeciegoC, usuarioD). Es un servidor simple donde estás creando... es sólo una cadena de firmas. Es una lista enlazada ECC, básicamente.

Es como transferir derechos de firma. La clave es cómo solicitan una firma con, y se llega a transferir quién llega a solicitar la siguiente firma. El servidor firma algo en nombre de un usuario, luego en nombre de otro usuario.

## Propiedad conjunta de la clave con el servidor

Si el segundo usuario crea otra clave, y la llamamos clave transitoria porque se la vamos a dar a otra persona. Puede utilizar musig para crear otra clave que es una multisig 2-de-2 entre A y X. Para firmar con AX y utilizar este servidor, solicita una firma ciega a A, luego completa la firma firmando con esta clave X. Si desea transferir la propiedad de la clave AX, le da la clave privada X a alguien y le dice al servidor que transfiera los derechos de firma.

## Un ejemplo más concreto

En la cadena de estados, digamos que tenemos al usuario B que controla lo que el servidor llega a firmar. El usuario B solicita una firma eltoo en esta transacción fuera de la cadena. Digamos que el dinero va a AX o después de un tiempo de espera a B. Así que esto es básicamente un relámpago básico en el sentido de que si hay un tiempo de espera entonces el dinero vuelve a B. Así que ahora que B tiene esa garantía, ahora envía dinero en la blockchain bitcoin a esto. Él ya tiene la firma, por lo que está garantizado para ser capaz de redimir el dinero en la cadena sin la ayuda del servidor. Si quiere transferir el dinero, solicita otra firma al servidor. Se trata de otra transacción de actualización de eltoo con otro número de estado. En lugar de que B consiga firmar, ahora es el usuario C el que consigue firmar. Podemos seguir así. Cambias las transacciones de actualización de eltoo, y básicamente así es como transfieres dinero fuera de la cadena.

En eltoo, puedes gastar una salida con una transacción. Incluso esto va a una blockchain, puedes enviar la transacción actualizada a la blockchain. Esto se debe a NOINPUT y a la imposición del número de secuencia y los timelocks en eltoo.

Sigue siendo seguridad reactiva, sí. Si no prestas atención, es lo mismo que un rayo. Tienes que prestar atención a la cadena de bloques y saber cuándo alguien está emitiendo una transacción para cerrar el canal.

## Resultados prácticos

Podemos cambiar la propiedad de UTXO sin cambiar la clave. El servidor no conoce X, por lo que no tiene control total. Si el servidor desaparece, se puede canjear on-chain. Como estás haciendo firmas ciegas sobre todo, el servidor no sabe que está firmando algo como bitcoin. Sólo pone una firma ciega en algo, no verifica ningún dato de la transacción ni nada. No es consciente de ello. Son los usuarios los que tienen que descifrar y verificar estas transacciones.

P: ¿Qué verifica el servidor antes de realizar una firma ciega?

R: No verifica nada. Le das un mensaje y lo firma. El usuario desbloquea las firmas y puede elegir no aceptar una transacción. Esto es similar al trabajo de validación del lado del cliente de Peter Todd.

P: ¿No es necesario que el servidor garantice que no creará una firma para B después de que se haya transferido a C?

R: Sí, sólo firmará una vez para el usuario. Impone para quién firma y que sólo firma una vez.

P: ¿Es necesario comprobar que los números de secuencia aumentan?

R: Eso lo comprueba el receptor.

P: Pero no sabe cuáles eran los números de secuencia anteriores.

R: Todas las firmas ciegas anteriores que haya firmado el servidor llegarán al usuario receptor.

P: ¿Así que tiene un paquete de propiedad que crece linealmente?

R: Sí, es lo mismo que ocurre con las propuestas de validación del lado del cliente de Peter Todd. El descifrado es el mismo secreto que se ha pasado de un usuario a otro. Puedes hacer un hash de la clave privada y esos son los secretos que usas para cegar. Necesitas dos secretos para cegar. Puedes pasar las versiones no cegadas de las transacciones, eso podría ser suficiente. Depende de lo que quieras hacer. Las firmas cegadas podrían venir del servidor o los usuarios podrían pasarlas. Tal vez prefieras que el servidor guarde los mensajes cegados, tú los descargas y los descifras. Pasas X y lo que obtienes del servidor. Cualquiera de los dos métodos funciona.

Un usuario pide una firma, y dice que el receptor la reciba la próxima vez. Cuando ese próximo usuario pide una firma ciega, entonces el servidor conoce la cadena de transferencias. Eso es correcto. Pero no conoce la identidad de los propietarios de la clave pública. Pero definitivamente hay historia. La ruta es conocida, sí. Sin embargo, no sabe qué UTXO es. Pero sabe que si es un UTXO, el siguiente destinatario es el propietario actual. Es un token de un solo uso. El receptor podría ser la misma persona que el gastador, el servidor realmente no lo sabría.

Podrías hacer que la ruta no se conozca si usas tokens de ecash. Cambias el token por una firma y obtienes un nuevo token de vuelta, como chaumian ecash. Bien, hablaremos de eso.

Con eltoo puedes hacer corte de transacciones al UTXO final o a quien tenga la transacción final. Todo esto es ciego. La cadena de estados solo ve una cadena de solicitudes de usuarios relacionados pero no sabe que.

## El papel del servidor

Confías en que el servidor sólo coopere con el último propietario. El servidor promete que sólo cooperará con el último propietario. Confías en que el servidor haga esto. El servidor es una federación, es una firma umbral Schnorr usando musig o algo así. Debe publicar todas las peticiones de firma ciega (la statechain). De esta manera la gente podría auditar el servidor y ver que nunca firmó dos veces. Asegúrate de que el servidor firma sólo para las peticiones de los usuarios, y asegúrate de que el servidor nunca firma dos veces para un usuario.

Esto es un blockchain público o statechains público. Está centralizado, así que no es un gran problema usar HTTPS, json-rpc, lo que sea.

## Atomicidad mediante firmas de adaptadores

Una vez que ves una firma, aprendes un secreto. La firma tiene que dar o todas las firmas o ninguna de las firmas. Si intenta dar la mitad, entonces no funciona porque serías capaz de completar las otras firmas. Usamos esto para hacer posible la transferencia de múltiples monedas en múltiples de estas statechains. Si tienes una cadena con un bitcoin y otra cadena con un bitcoin y otra con dos bitcoin, puedes intercambiarlas. Estos intercambios atómicos también se pueden hacer entre monedas.

Para intercambiar a valores más pequeños... el servidor tiene todas las firmas de todo el mundo, excepto los secretos del adaptador. Una vez que recibe todos los secretos de todos, puede completar todas las firmas y puede publicarlas todas. Si decide publicar sólo la mitad de ellas, entonces los usuarios también tienen las firmas de sus adaptadores.

## Comparación con las cadenas laterales federadas

No es divisible, sólo para UTXOs completos. Es casi el mismo modelo de turst que las sidechains federadas. Es no-custodial porque 2-de-2 y off-chain eltoo. Se necesita una torre de vigilancia o un nodo completo para vigilar las transacciones cercanas. No es un transmisor de dinero porque es sólo firma ciega que podría ser cualquier cosa. No me culpes, básicamente. Sigue siendo una federación. Lightning es más seguro. Si la federación realmente lo intentara, podrían conseguir tu clave privada como haciendo el intercambio y ellos son uno de los usuarios. Si consiguen una de las claves transitorias entonces pueden conseguir tu dinero.

Aquí, usted puede enviar a la gente bitcoin en un statechain- tendrían que confiar en el statechain, y tendrían que como bitcoin, pero no hay ningún gravamen y no es como relámpago en ese aspecto.

## Peores escenarios

El servidor obtiene un puñado de claves transitorias, desenmascara las firmas, se da cuenta de las transacciones de bitcoins, procede a robar de forma demostrable las monedas, todos los demás usuarios (claves no robadas) se retiran en cadena como resultado. Pero esto es inofensivo sin las claves transitorias. Orden judicial de congelar o confiscar monedas, realmente no pueden cumplirla.

## Microtransacciones

No puedes enviar nada más pequeño que un UTXO económicamente viable. Nunca podrían canjearlo en la cadena. Así que en realidad estás limitado por las tasas de transacción en la cadena. Como statechain, quieres cobrar comisiones, y esto es necesario cuando se intercambia entre monedas. Habrá algunas cantidades fraccionarias al intercambiar entre altcoins. Tiene que haber algún método para pagar, que sea más pequeño que los UTXOs que estás transfiriendo. Podrías darle a la statechain uno de estos UTXOs, bueno, podrías pagar con lightning o una tarjeta de crédito. O API satélite con tokens chaumian para pagos, supongo que eso no está desplegado todavía.

## Relámpagos en las cadenas de estados: eltoo y las fábricas de canales

Si tienes una fábrica de canales, puedes añadir y eliminar participantes. Eltoo admite cualquier número de participantes. ¿No es eso una fábrica? La idea de una fábrica es que tienes un protocolo secundario funcionando además de eltoo. Pero en eltoo es esta cosa plana donde puedes reorganizar fondos entre participantes individuales y no necesitas esta segunda capa de segundas capas hasta el final. Deberíamos haberlo llamado tortuga.

El servidor puede estar dentro de un statechain sí mismo sin saber.

Canal actualizado junto con multi atomic swap. Cierre no cooperativo similar al eltoo regular. Las statechains usan una versión simplificada de eltoo, donde sólo tienes transacciones de actualización y tienes transacciones de liquidación de otra manera. Si quieres reequilibrar tu canal, puedes añadir un bitcoin al canal haciendo swap y luego moviéndote por el canal. Todo esto es posible. Acabamos de hablar de las fábricas de canales para añadir/eliminar miembros también.

Lightning tiene un rendimiento limitado; tienes rutas y sólo puedes enviar tanto dinero a través de él. Es divisible y puedes enviar cantidades fraccionarias sin problema. En statechains, hay un rendimiento infinito, pero no es divisible. Si combinas los dos, suponiendo que aceptas los supuestos de confianza, tienes una mezcla perfecta de poder enviar cualquier cosa sin fricción.

Nadie tiene que poner dinero para apoyar el protocolo. Podría tener una cuota fija. Las cuotas de eltoo dependen de los usuarios. En lightning, los únicos que pagan son los intermediarios y aquí no hay intermediarios. Los incorporas a tu propio grupo y les pagas directamente. Todos tenéis que estar conectados para hacerlo. Esto no se aplica sin statechains, nos permite tener membresía dinámica de instancias de eltoo, que es realmente genial.

Podrías hacer que el servidor fuera parte del canal relámpago y luego pagarles. Sí, claro. Asumamos que confiamos en el servidor, entonces estamos bien. Si una de las partes desaparece y deja de cooperar, estás forzado a entrar en la cadena. Así que aumentas tu riesgo en la cadena a medida que añades más miembros. Esa es la compensación. Pero ese es siempre el caso, incluso sólo con eltoo, tienes que saber que están en línea cuando llega el momento de firmar. Si añades el servidor a tu canal de eltoo, entonces conocen el UTXO y sigue siendo algo ciego, pero tienen más información. Podrías tener un canal para el servidor, exponer ese canal a ellos y pagarles a través de ese canal. Pero no a través de los demás canales.

A medida que aumenta el número de miembros en la cadena de estados, la cooperación se vuelve más cara, así que quizá quieran ganar dinero por ello.

Si confías en unos servidores y otro usuario confía en otros servidores de una federación diferente, ¿es algo posible? No puedes aumentar la seguridad, sólo puedes reducirla. Puedes tener firmas de umbral para hacer esto. Pero podríamos tener un paso intermedio que termine en la cadena, si lo haces en la cadena está bien. Tendríamos que repetirlo en la cadena de todos modos, correcto. Bueno, eso es desafortunado.

## Casos de uso

Podrías hacer transferencia de valor fuera de la cadena, canales relámpago (balanceo), canales de apuestas (usando contratos multisig o de registro discreto), o tokens RGB no fungibles (usando sellos de un solo uso). Usas pay-to-contract para poner una moneda de color en un UTXO y pones el UTXO en la statechain, y ahora puedes mover este token no fungible fuera de la cadena. Eso lo soluciona.

Requiere más confianza porque el concepto de transacción fuera de la cadena no es algo que se pueda emular sin blockchain. Para los casos de uso que no son bitcoin, es extraño pensar en ello, pero hasta ahora si alguien tenía una clave privada, se suponía que no podía dársela a otra persona sin que ambos la tuvieran, pero el servidor les permite hacerlo y la suposición se rompe. Si ves una clave privada, se la puedes dar a otra persona. La propiedad puede cambiar moviendola a traves de la cadena de estados.

## Otros temas

Puedes utilizar módulos de seguridad de hardware para transferir claves transitorias, como la atestación. Tienes una clave privada dentro de un HSM o un monedero hardware. Tienes otro dispositivo de hardware y quieres transferir la clave privada. Mientras la clave privada no salga del dispositivo, puedes hacer transferencia de dinero fuera de la cadena. Esto es como teechan, sí. Los HSM son terribles, pero la cosa es que estamos transfiriendo la clave transitoria de una manera que es incluso menos segura que eso. Si estás añadiendo un HSM entonces es más seguro, y si el HSM se rompe entonces estás de vuelta al modelo que tenemos ahora. El usuario podría confabularse con la federación para robar dinero... Todo el mundo tendría su propio dispositivo hardware monedero, y mi dispositivo habla con tu dispositivo, y mi clave transitoria está dentro de él, y nunca sale, o si sale entonces se niega a transferirse a tu dispositivo hardware. Esto requiere confianza en el HSM, por supuesto. Podrías ejecutar un programa por el servidor que atestigüe que no firma estados antiguos. No sé si eso sería equivalente o mejor seguridad, pero sí que es un buen punto. Al menos puedes compartir la confianza, dividir la confianza entre el desarrollador del hardware y el servidor, en lugar de confiar sólo en el servidor.

¿Qué pasa si el opendime tenía una clave transitoria, y podría firmar. Podrías entregarla físicamente. Sí, déjame pensarlo. No estoy seguro. Creo que debería funcionar siempre y cuando pueda hacer transacciones bitcoin parcialmente firmadas. No veo cómo no funciona, así que eso es interesante. Muy literalmente, esa es la única copia de la clave si es un opendime. Estoy seguro de que podrías diseñar algo así con propiedades similares a las del opendime, donde hay algunas garantías de seguridad en torno a que nadie ha visto realmente la clave privada. La información cegada puede estar en ese chip también, y quizás una cabecera de verificación. Esto añade una suposición adicional de que, si usted no va en línea en absoluto, hay una cosa adicional. Sí, sólo confía en mí, conecta esto al USB. Te estoy dando dinero, sólo confía en mí ... claro, eso es lo que está pasando.

También podrías hacer graftroot withdrawal, que permite canjear forks o un ETF. En lugar de retirar de la statechain por- la retirada cooperativa sería una firma ciega donde el dinero sólo va a usted en la cadena, sin la tontería eltoo y tirar eso. Pero si puedes retirar a través de graftroot, entonces suponiendo que tuviéramos graftroot, suponiendo que después de graftroot ocurriera algún hard-fork entonces ahora tienes una clave graftroot con la que podrías sacar todas las monedas hard-fork. Porque la suposición es que hay algún tipo de protección de repetición, pero graftroot es lo mismo. Tu clave graftroot funcionará en todas las cadenas hard-forked pero necesitas crear una transacción diferente en esa otra cadena. Si retiras a través de graftroot, puedes retirar de todas las cadenas. Suponiendo que soporten graftroot. La suposición es que se trata de una bifurcación bitcoin y graftroot ya está ahí y que acaba de copiar esas características y soft-forks.

Esto también podría ser utilizado para un ETF. Con un ETF, el problema con un hard-fork es qué monedas te van a dar, bueno con graftroot te podrían dar todas las monedas sin saber los hard-forks o cuántas. Podrías tener un utxo con más hard-forks y tener un valor diferente o algo así. Pero de todas formas este puede ser el caso ahora mismo.

Un problema abierto es que podrías verificar sólo el historial de las monedas que posees o recibes. Pero necesitas algún tipo de garantía de que no hay dos historias. Así que necesitas almacenar y retransmitir sucintamente la historia de la cadena de estados. Necesitas ser capaz de conocer todas las cadenas que existen y saber que la tuya es única... una clave del servidor que sólo está firmando esto. ¿Pero cómo pruebas un negativo? Tiras un árbol merkle ahí. Hay varias maneras. Hubo una propuesta sobre prevenir el doble gasto forzando a firmar con la misma k dos veces, entonces si alguna vez firman algo dos veces pierden dinero o algo así. El castigo no importa, ya está ahí: si firman dos veces, la reputación se hace añicos. Ya están castigados, sólo hay que detectarlo. Una forma sería conocer todas las claves con las que se está firmando y obtener una lista de ellas y asegurarnos de que hay, sólo hay una vez. Otra forma es un árbol de Merkle disperso que no he mirado.

En el mejor de los casos se puede hacer pruebas de fraude más fácil de hacer y probar, pero ¿por qué iban a querer dar datos suficientes para demostrar que se produjo un fraude. ¿Cómo sabes que no hay dos historiales? Bueno, en la cadena sólo puede haber un historial. Una vez que la gente se entera, toda la reputación se viene abajo. Fuera de la cadena se puede inflar, pero una vez dentro de la cadena sólo se escribe uno de los historiales. El servidor firma una historia específica del statechain y te la da. Si tienes toda la lista de claves que ha dado, y tu clave sólo está ahí una vez, creo que es prueba suficiente.

## Ver también

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/statechains/>

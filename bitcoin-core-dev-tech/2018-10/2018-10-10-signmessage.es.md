---
title: Mensaje de señalización
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - wallet
speakers:
  - Kalle Alm
date: 2018-10-10
---
kallewoof and others

<https://twitter.com/kanzure/status/1049834659306061829>

Estoy tratando de hacer un nuevo signmessage para hacer otras cosas. Sólo tiene que utilizar el sistema de firma dentro de bitcoin para firmar un mensaje. Firmar un mensaje que alguien quiere. Puedes usar proof-of-funds o lo que sea.

Usted podría simplemente tener una firma y es una firma dentro de un paquete y es pequeño y fácil. Otra opción es tener un .. que no es válido de alguna manera. Haces una transacción con alguna entrada, donde el txid es el hash del mensaje o algo así. Podríamos tener OP_MESSAGEONLY, que es que si te encuentras con eso en una firma para una transacción entonces fallas inmediatamente, y si es un mensaje entonces lo ignoras. Puedes tener una pubkey de mensaje de firma y una pubkey de gasto y están separadas.

Es posible que tengas un monedero compartido y que esos UTXOs representen fondos que posee otra persona. La complicación de probar los fondos disponibles es ¿qué hacer con las carteras frías frente a las carteras calientes? ¿Utilizas los mismos UTXOs para probar esos fondos?

Greg Sanders quiere que se utilice un fork id para signmessage o proof-of-funds y luego sólo utilizarlo para firmar, lo que significa que no sería válido en bitcoin. Asegurarse de que las altcoins no utilizan esto también; pero ¿qué pasa cuando se adelantan y lo hacen? Tal vez cualquier fork id significa que es un signmessage y toda la protección de repetición se va por la ventana ((risas)).

La gente está pidiendo una extensión simple para signmessage que funcione con segwit. Convertirlo en un nuevo tipo de transacción o lo que sea parece algo que vale la pena resolver, pero es un problema diferente. Para aquellos que sólo quieren ser capaces de firmar un mensaje con una dirección, tener toda esta complicación acerca de bien, estoy esperando una firma de usted y usted me está dando una firma de una transacción, pero tiene 100 entradas y está haciendo otras cosas. ¿Qué se supone que tiene que hacer mi verificador con eso? La API es realmente complicada. Estás comparando toda la complejidad de lo que una transacción puede hacer en una simple función de verificación de mensajes.

¿Para qué quiere la gente esto? ¿Prueba de fondos, auditoría, airdrops, ...?

Para simplemente firmar un mensaje con una dirección segwit, ya hay una cosa electrum/trezor que está añadiendo una bandera a la firma existente. Es sólo una extensión del esquema de firma existente. Podríamos hacerlo. Sin embargo, parece complicado. No es fácilmente extensible a cualquier cambio futuro.

Podrías tomar el sistema de escritura existente pero el sighash o en lugar de firmas ECDSA con un sufijo que indique qué hash, en cualquier lugar donde se espera una firma firmas el mensaje con esa clave pública. Y el mensaje recibe algún prefijo para asegurarse de que no colisiona accidentalmente con alguna transacción o algo así. Al igual que un prefijo como «bitcoin mensaje:» más el mensaje. No necesitas incluir el mensaje en la firma. Es sólo un scriptsig y un testigo de escritura.

La razón por la que la gente quiere la versión de transacción de esto es que entonces usted puede conseguir mimblewimble lo que sea más tarde.. tal vez debería tirar la prueba de fondos cosas y mantener la parte signmessage. ¿La gente está firmando una dirección para probar? ¿Lo usan como sustituto de PGP o para demostrar fondos? A veces se comprometen previamente a un contrato antes de que se les pague, lo que no es muy común, pero eso es lo que hace.

En transacciones confidenciales, tienen una llave cegadora, y... hacen alguna desencriptación. No creo que esté relacionado con esto.

Yo uso signmessage para firmar entradas en mi billetera. Hago esto para la prueba de fondos para demostrar que cualquier entrada en mi cartera es algo que realmente controlo.

Esto es bip322.

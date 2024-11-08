---
title: El futuro de los contratos inteligentes de Bitcoin
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - contract-protocols
speakers:
  - Max Keidun
---
El futuro de los contratos inteligentes de Bitcoin

<https://twitter.com/kanzure/status/1043419056492228608>

Hola chicos, la próxima charla en 5 minutos. En cinco minutos.

# Introducción

Hola a todos. Si están caminando, por favor háganlo en silencio. Estoy un poco nervioso. Estuve muy ocupado organizando esta conferencia y no tuve tiempo para esta charla. Si tenían grandes expectativas para esta presentación, entonces por favor bájenlas durante los próximos 20 minutos. Iba a hablar de los modelos tradicionales de capital riesgo y de por qué no funcionan en la industria del bitcoin. No funcionan, y nada ha cambiado en los últimos 3 meses, así que ¿por qué perder nuestro tiempo en VCs? Ellos no entienden una mierda sobre cripto.

Mi tema de hoy y me sentaré, es el futuro de los contratos inteligentes de bitcoin. Los contratos inteligentes son uno de los términos o palabras de moda que todo el mundo lanza alrededor, pero no todo el mundo entiende. Estoy seguro de que aquí, la audiencia es más sohpisticated en bitcoin que el público en general. Pero sigue siendo un problema. Para mucha gente, sigue siendo una pregunta. ¿Cómo funcionan los contratos inteligentes de bitcoin? ¿Cómo se pueden utilizar en la vida real? ¿Cómo se pueden utilizar en la economía real?

# Multisig

Multisig -del que hablaremos hoy- es un tipo de contrato inteligente. No es nada nuevo. Quiero hablar exactamente de multisig. El propósito de la charla es dar ideas a la gente que se pregunta qué construir encima de bitcoin.

Obviamente, Hodl Hodl está utilizando contratos inteligentes. Esta charla no es sobre nuestra empresa. En realidad, no podemos trabajar en demasiados contratos inteligentes. Como empresa, tratamos de inspirar o estamos contentos tanto como otras personas, para construir algo nuevo y construir soluciones de contratos inteligentes en la parte superior de bitcoin porque no tenemos suficiente tiempo para hacerlo nosotros mismos. Quería compartir algunas ideas. Si tienes alguna pregunta después, no dudes en dirigirte a mí o a Roman Snitko.

# Contratos inteligentes

¿Qué son los contratos inteligentes? En lugar de una definición, vamos a utilizar un ejemplo que utilizamos en nuestra bolsa. También hablaré de los casos de uso. El ejemplo clásico es el de Alice y Bob. Como puedes ver en la diapositiva, están Alice y Bob, dos partes separadas. Ambos tienen llaves para liberar fondos desde una dirección especial de p2sh. El contrato inteligente dice que requiere las claves de Alice y Bob para liberar fondos de ese depósito. Esto es lo que se conoce como multisig. Requiere varias claves para firmar la transacción de liberación. Esta dirección se convierte en una cuenta de custodia multisig o cartera. No importa quién envía los fondos a esta dirección escrow; lo único que importa es si ambas partes los liberan o quién es el dueño de las claves.

En nuestro intercambio, utilizamos el escrow para permitir a los usuarios intercambiar moneda fiduciaria y bitcoin y viceversa. Así se evita tener bitcoin en los monederos de Hodl Hodl. Como intercambio, nosotros tenemos una clave y el vendedor otra. No hace falta mucha imaginación para ver cómo este enfoque multisig de 2 en 2 puede utilizarse en otros casos de negocio fuera de las criptomonedas.

Supongamos que quiere alquilar un apartamento; normalmente el propietario le pedirá una fianza. Normalmente esta fianza la retiene directamente el arrendador. Lo justo sería que estuviera en una plica y pudiera devolverse posteriormente cuando ambas partes se pusieran de acuerdo. El mismo mecanismo de custodia puede aplicarse a los autónomos de todo tipo; supongamos que quiere contratar a un desarrollador de otro país para que trabaje en su software. Entonces, por ejemplo, puedes guardar un dinero en custodia.

Otro ejemplo interesante es crear un equivalente en bitcoin para un contrato futuro, y la liquidación se hace en bitcoin. Esto permitiría una especie de futuros p2p donde dos partes apuestan por un resultado. Los fondos apostados en este contrato se almacenan en una dirección multisig y no en un tercero. Hace un mes, Bitmex tuvo un problema en el que los cortos se cerraban masivamente y la gente estaba decepcionada. Este esquema resuelve eso, porque nadie puede afectar a tus futuros y acuerdos.

Podría seguir y seguir, pero este enfoque de 2 de 2 multisig se puede utilizar en muchos lugares fuera de la criptografía.

# Situación de disputa

Muchas personas, cuando escuchan cómo funciona el escrow 2-de-2, se preguntan: ¿qué pasa si una de las partes decide no liberar los fondos de esta cuenta de escrow? ¿El dinero permanece bloqueado para siempre? Y si es así, ¿qué ocurre? ¿Quién controla la dirección de destino de la transacción bloqueada? ¿Cuál es el caso por defecto cuando ambas partes no están de acuerdo? Siempre hay que utilizar el tiempo de bloqueo.

Ninguna parte tiene incentivos para mantener los fondos bloqueados para siempre. Diferentes factores influyen en la decisión de desbloquear los fondos. El bloqueo para siempre puede ser un resultado más beneficioso. El 2 de 2 es un modelo de custodia que puede aplicarse a algunos casos, pero no a todos. Hay que tener en cuenta las influencias del mercado y todas las demás cosas de su negocio.

# n-de-m multisig

2-de-2 es un caso especial de n-de-m multisig. Podría tener un número variable de claves necesarias para liberar los fondos. Considere 2-de-3 multisig, para los pagos de los autónomos. Supongamos que ha completado el trabajo, pero el empleador no quiere liberar los fondos. También podría haber un mediador en la cuenta de depósito. Hemos implementado el multisig 2-de-3 en Hodl Hodl para la bolsa, principalmente para las grandes operaciones OTC, pero también los inversores minoristas y los comerciantes minoristas pueden utilizarlo también.

Hay un caso de uso más complejo en el que se requieren más firmas con diferentes niveles de complejidad. Puedes tener algo como 5-de-12 multisig que podría tener más sentido.

# Implementación de Multisig

Como ya he mencionado, el problema ahora mismo es que los multisig no son fáciles de usar para los consumidores. Los intercambios los utilizan principalmente para almacenar los fondos de los usuarios. Los usuarios medios se van a frustrar averiguando cómo utilizar multisig. Tiene que hacer que sus cerebros no exploten.

Una forma de hacerlo es implementar todo en un navegador, que es lo que hizo Hodl Hodl. El frontend puede crear claves y almacenarlas sin enviarlas al backend. Esto es propenso a ciertos problemas de seguridad y tipos de ataques. Sería más seguro generar una segunda clave en una aplicación de smartphone o en un dispositivo especializado como un Trezor o algún monedero de hardware.

Vamos a operar un mercado con la solución simplificada con generación de claves en el frontend, pero también con más sofisticación con dispositivos independientes como otra opción.

Quiero señalar específicamente que el multisig no es algo excepcional o novedoso. Hodl Hodl no es nada nuevo bajo el sol. En realidad, no innovamos. Cuando le planteo nuevas ideas, suele mirarme así. Multisig ha existido durante mucho tiempo. Pero no es fácil de usar. Digamos que quieres un nuevo contrato multisig; ¿alguno de vosotros sabe cómo configurarlo y hacerlo?

# ¿Cómo llevar la multisig a los consumidores?

No hay una solución inmediata para la multisig. Es necesario que haya un mercado en línea para los participantes en multisig. Hay que centrarse en los mercados de servicios más que en la colocación de productos.

Openbazaar lo utiliza para los productos, pero no tenemos un mercado para los servicios multisig. Aquí no hay innovación en multisig. Nadie se ha molestado en reunirlo de forma que la gente pueda utilizarlo. No por diversión o sólo para señalar que bitcoin podría hacerlo, sino porque es útil.

# Anuncios

Estamos introduciendo una mesa de operaciones OTC en Hodl Hodl para grandes operaciones utilizando 2-de-3 multisig. Tenemos un enfoque no custodial que hemos estado desarrollando desde el principio para nuestro intercambio. El segundo anuncio es la idea de que lanzaremos futuros de bitcoin. Actualmente estamos trabajando en esto, y se lanzará pronto. Permitirá a la gente apostar con bitcoin sobre el resultado de otras cosas, y en otras palabras es un mercado de predicción. El contrato futuro se denominará en bitcoin, y es peer-to-peer. Mantente atento a nuestro twitter.

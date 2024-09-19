---
title: The Incomplete History of Bitcoin Development
translation_by: Julien Urraca
tags: ["history"]
date: 2019-08-04
speakers: ['0xB10C']
---

Autor: 0xB10C
Texto original: <https://b10c.me/blog/004-the-incomplete-history-of-bitcoin-development/>

# La historia incompleta del desarrollo de Bitcoin

Para comprender plenamente la justificación del estado actual del desarrollo de Bitcoin, el conocimiento de los eventos históricos es esencial. Esta publicación de blog destaca eventos históricos seleccionados, versiones de software y correcciones de errores antes y después de que Satoshi abandonara el proyecto. Además, contiene una sección sobre el estado actual del desarrollo de Bitcoin. La cronología vinculada proporciona detalles adicionales para cada evento.

No estaba siguiendo el espacio Bitcoin cuando ocurrió la mayoría de estos eventos. Una gran parte de la cronología se adapta de una charla que John Newbery dio sobre la Historia y la Filosofía del Desarrollo de Bitcoin. Se supone que el título de esta publicación de blog te recuerda que no puede ni incluye todos los eventos. La historia está en el ojo del espectador. La historia evoluciona. Si tienes alguna sugerencia sobre algo que falta o quieres proponer un cambio, crea un problema en el historial de desarrollo de bitcoin del proyecto de código abierto, que se utiliza para generar la cronología adjunta.

imagen de la cronología a partir de 2007:
A principios de 2007: Satoshi empieza a trabajar en Bitcoin. Satoshi comienza a escribir código para Bitcoin. Esto se basa en un correo electrónico enviado a la lista de correo de Criptografía donde Satoshi escribi el 17 de Noviembre, 2008: "Creo que he trabajado en todos esos pequeños detalles durante el último año y medio mientras lo codificaba."

### Con Satoshi

La cronología narra una historia que comienza a principios de 2007. Satoshi Nakamoto comienza a trabajar en Bitcoin. El sistema de efectivo electrónico peer-to-peer sin terceros de confianza. Sistema controlado únicamente por el software que ejecutan sus usuarios.

Desde el principio, los colaboradores se unen a Satoshi trabajando en Bitcoin. Estos nuevos colaboradores añaden, junto a muchas otras cosas, soporte para Linux y macOS al proyecto. Durante el verano de 2010, Satoshi crea algunos cambios críticos en el software. Por ejemplo, los puestos de control se introducen como salvaguardia contra pares malintencionados que transmiten cadenas de baja dificultad. Un nodo que aplica estos puntos de control rechaza las cadenas que no incluyen hash de bloque específicos a alturas específicas. Los puntos de control están codificados por sí solo por Satoshi, lo que en teoría permite a Satoshi controlar qué cadena sigue la red.

Unos días después de agregar puntos de control, Satoshi publica el primer cambio de consenso en la versión v0.3.3. Satoshi insta a los usuarios a actualizar. Durante el mes siguiente, se publican varias versiones secundarias. Uno de ellos corrige un error de desbordamiento crítico. Este error se explotó para crear dos UTXOS de alto valor. Satoshi aconseja a los mineros que reorganicen la cadena que contiene los bloques con las transacciones maliciosas.

Una semana después, Satoshi introduce un sistema de alerta para informar a los operadores de nodos sobre errores y problemas similares en la red. El sistema de alerta incluye un modo seguro. El modo seguro, una vez activado, deshabilita todos los métodos RPC de gestión de dinero en toda la red. Solo Satoshi puede crear alertas de red válidas firmándolas con una clave privada. Algunos usuarios plantean la pregunta de qué podría suceder cuando un segundo partido, por ejemplo, un gobierno, tiene acceso a esta clave.

Satoshi tiene mucho poder sobre la red Bitcoin en este momento. La principal preocupación aquí no es que Satoshi se convierta en el mal e intente destruir la red, sino que no debería haber un solo punto de fracaso en un sistema descentralizado.

En diciembre de 2010, Satoshi abre su último hilo en bitcointalk anunciando la eliminación del modo seguro. Satoshi escribe en uno de sus últimos correos electrónicos:» He pasado a otras cosas. Está en buenas manos con Gavin y todos. «Algunos podrían argumentar que Satoshi alejarse de Bitcoin es una de sus mayores contribuciones.

### Sin Satoshi

Alrededor del mismo tiempo, el proceso de desarrollo pasa de SVN a GitHub, lo que lleva a colaboradores desde hace mucho tiempo como BlueMatt, sipa, laanwj y gmaxwell a unirse al proyecto. A mediados de 2011 se introdujo el proceso BIP para las propuestas de mejora de Bitcoin. En el último trimestre de 2011 y en los primeros meses de 2012, la comunidad discute varias propuestas que permitirían al receptor de una transacción especificar el script necesario para gastarlo. Fuera de ellos, P2SH se fusiona.

En otoño de 2012 se anuncia la Fundación Bitcoin. La Fundación Bitcoin espera lograr para Bitcoin lo que Linux Foundation hace por Linux. Algunas personas plantean el temor a la centralización del desarrollo en el hilo del anuncio.

La versión de Bitcoin v0.8.0 se lanza en la primavera de 2013. Dos semanas después del lanzamiento, una bifurcación inesperada divide la red en nodos que se han actualizado y aún no se han actualizado. La bifurcación dura se resuelve con bastante rapidez. Diferentes mineros reaccionan cambiando su poder hash a la cadena válida tanto para nodos mejorados como para nodos mejorados.

A finales de 2013, el software Bitcoin se cambió de marca a Bitcoin Core. Al año siguiente se fundaron empresas como Chaincode y Blockstream. Más tarde, la Iniciativa de Moneda Digital del MIT se une a Chaincode y Blockstream pagando a desarrolladores e investigadores para que trabajen en Bitcoin. En febrero de 2015 Joseph Poon y Tadge Dryja publican el primer borrador del Libro Blanco de Lightning. Al año siguiente, Luke Dashjr revisa el proceso BIP con BIP 2 y la versión de Bitcoin Core v0.13.0 incluye SegWit como softfork. En noviembre de 2016, el sistema de alerta se retira y en agosto de 2017 se activa SegWit. El año 2019 trae una nueva empresa, Square Crypto, que patrocina el desarrollo de Bitcoin. En mayo, Pieter Wuille propone un trote BIP.

### El estado actual del desarrollo de Bitcoin

A lo largo de los años, la cultura de desarrollo de Bitcoin se volvió más descentralizada, bien definida y rigurosa. Actualmente hay seis mantenedores de Bitcoin Core, distribuidos en tres continentes. Solo ellos pueden fusionar confirmaciones de los colaboradores. Sin embargo, antes de que las confirmaciones se fusionen, tienen que pasar por un proceso de revisión, que se ha vuelto mucho más estricto.

Por ejemplo, una propuesta competidora, para el P2SH mencionado anteriormente, fue OP_EVAL. La solicitud de extracción que implementó OP_EVAL se fusionó a finales de 2011. Solo tenía un revisor, aunque cambia el código crítico para el consenso. Russell O'Connor abrió un tema criticando partes de la implementación y que un cambio tan grande y crítico para el consenso debería haber tenido muchas más revisiones y pruebas.

Esto impulsó un debate continuo sobre cómo garantizar una mayor calidad del código mediante más pruebas y revisiones. Hoy en día, cada solicitud de extracción debe ser revisada por lo menos por varios desarrolladores. Si un cambio afecta al código crítico de seguridad o incluso de consenso, el proceso de revisión necesita muchos revisores, muchas pruebas y, por lo general, se extiende durante varios meses. John Newbery, un colaborador activo de Bitcoin Core, me dijo que «no hay posibilidad de que hoy se fusione un cambio de consenso con un único revisor».

Se trabajó mucho en las pruebas automatizadas. Hay pruebas unitarias escritas en C++ y pruebas funcionales escritas en Python. Cada cambio no trivial debe actualizar las pruebas existentes o agregar otras nuevas a los marcos. Además de las pruebas unitarias y funcionales, hay una iniciativa para realizar pruebas de fuzz en Bitcoin Core y un marco de evaluación comparativa para monitorear el rendimiento del código. El sitio web bitcoinperf.com, por ejemplo, ofrece una interfaz Grafana y una interfaz de velocidad de código que muestran resultados periódicos de evaluación comparativa.

A lo largo de los años se ha creado un proceso de lanzamiento bien definido. Las principales versiones de Bitcoin Core se programan cada seis meses. La programación incluye un proceso de traducción, una congelación de funciones y, por lo general, varios candidatos de lanzamiento. Los recientes esfuerzos de Cory Fields y Carl Dong tienen como objetivo aumentar la seguridad del sistema de construcción de Bitcoin Core con compilaciones deterministas y arrancables. Es posible que el nuevo sistema de compilación no esté completamente listo para la versión 0.19.0 de Bitcoin Core este otoño, pero podría proporcionar una mayor seguridad de compilación en el futuro.

### Conclusión

En los últimos diez años, la cultura de desarrollo de Bitcoin ha cambiado mucho. Pasando de estar muy centralizado alrededor de Satoshi a estar más descentralizado con más de mil colaboradores de GitHub en 2018. Ha quedado claro que se necesitan altos estándares de revisión de código, calidad del código y seguridad. Estas normas se siguen y mejoran constantemente.

Creo que para entender completamente la justificación del estado actual del desarrollo de Bitcoin, el conocimiento sobre los acontecimientos históricos es esencial. Hay una cronología con más eventos adjuntos a continuación. Algunos sugirieron que la lectura adicional podría ser The Tao Of Bitcoin Development escrita por Alex B., The Bitcoin Core Merge Process escrito por Eric Lombrozo y la publicación del blog de Jameson Lopp: ¿Quién controla Bitcoin Core?

### Agradecimientos

Estoy agradecido por que John Newbery me haya ayudado a dar forma y revisar esta publicación de blog. Hizo muchas de las investigaciones históricas de su charla Historia y Filosofía del Desarrollo de Bitcoin, en la que se basa esta publicación de blog. También estoy muy agradecido por que Chaincode Labs me haya invitado a su Residencia de Verano 2019, donde conocí a mucha gente increíble, aprendí mucho y empecé a trabajar en esta publicación de blog y en la línea de tiempo.

---
title: Custodia de Bitcoin
transcript_by: Bryan Bishop
translation_by: Blue Moon
speakers:
  - Bryan Bishop
tags:
  - regulation
media: https://www.youtube.com/watch?v=D2WXxgZ8h-0&t=22160s
---
<https://twitter.com/kanzure/status/1048014038179823617>

Custodia de Bitcoin

Conferencia de Bitcoin del Báltico Honey Badger 2018, Riga, Letonia, Día 2

Schedule: https://bh2018.hodlhodl.com/

Transcripción

Hora de inicio:  6:09:50

Mi nombre es Bryan Bishop, voy a hablar de la custodia de bitcoin. Aquí está mi huella digital PGP, deberíamos hacer eso. Así que quién soy, tengo un fondo de desarrollo de software, no solo escribo transcripciones. En realidad ya no estoy en LedgerX desde el viernes (21 de septiembre de 2018) que vine aquí.  Eso es el final de 4 años, así que están viendo a un hombre libre. [Aplausos] Gracias.

¿Qué es la custodia? Algunas de estas diapositivas tratarán sobre la normativa y la custodia. Según la SEC y el código de regulación federal 17 CFR Parte 275. La regla de la custodia es realmente mal llamada. La regla de la custodia es que está prohibido que usted tenga la custodia de los activos. Así que la regla de la custodia es que no se puede tener la custodia. La custodia se define como cosas como la posesión, el acceso, la autorización y la propiedad legal, otras cosas por el estilo.

Así que todas estas cosas deben evitarse en determinadas situaciones según el regulador de valores de Estados Unidos.  Sin embargo, esto es contrario a bitcoin, porque en bitcoin básicamente los terceros están diseñados para ser agujeros de seguridad y no deberías usarlos. La intención de la regla de custodia, o al menos una de las intenciones, es que se trata de la presentación de informes y los requisitos en torno a cosas como, usted no quiere que la persona que gestiona sus fondos para robar todo el dinero por lo que tiene que ir con custodio calificado que se definen como los bancos, los futuros comisionistas, corredores de bolsa, o ambiguamente instituciones financieras extranjeras. Pero con bitcoin se puede decir aquí está la clave pública y vamos a mantener las cuentas segregadas y tal vez es bip32 o algo así y esto parece una forma más segura de hacer la custodia y el almacenamiento, especialmente para comprar y mantener los escenarios, que bajo las regulaciones si usted va a trabajar con alguien en un fondo que está haciendo sólo comprar y mantener que tiene que ser un custodio calificado, pero en mi opinión podría ser considerado un agujero de seguridad de terceros.

Así que para la regulación en particular, mientras que es una idea maravillosa decir que sólo hay que trabajar alrededor de los reguladores y no hacer nada de eso, también sería bueno darles un consejo realista sobre cómo funciona bitcoin y hacer buenas propuestas e intentos de buena fe para decirles cómo funciona bitcoin y lo que deberían exigir. Esto a menudo significa que hay que dar ejemplos reales a los reguladores sobre cómo funcionan las cosas, no sólo decir que usen multisig.

Recientemente redacté, junto con algunos coautores, una carta a la SEC sobre los fondos de inversión en bitcoin y cosas como animarles a utilizar la auditoría pública con claves públicas o incluso cosas como formas seguras de transferir bitcoin a los inversores si quieren rescatar sus tenencias de bitcoin del fondo.

En LedgerX fui un desarrollador de pila completa y también su experto en bitcoin. Les ayudé a diseñar su solución de custodia de bitcoins y una serie de otras cosas.  Están regulados por la CFTC, dirigen una cámara de compensación de bitcoin y un intercambio de opciones de bitcoin, cosas así.  La lección que aprendí rápidamente es que la automatización es muy buena, pero a veces no es necesaria. Usted puede gastar mucho tiempo y recursos y los costos de desarrollo de software de automatización, pero a menudo es mejor hacer manualmente las transacciones de bitcoin, especialmente en este caso porque su proceso de retiro es muy específico y no es de alto volumen en términos de la cantidad de datos que pasan por ella.

Además, no existe una solución de seguridad de hardware de extremo a extremo. Voy a hablar de eso un poco más en unos minutos. En realidad sabemos mucho sobre esto, esto es sólo formas de almacenar bitcoin.

Así que cuando estás diseñando una forma de almacenar bitcoin, ya sea para ti o para una empresa, tienes que pensar en lo que es apropiado. Esto se basa en el tipo de amenazas de las que tienes que protegerte y también tienes que tener muy claro cómo funciona. Probablemente nadie en tu familia sabrá cómo recuperar tu bitcoin cuando mueras.  Así que ese es un problema realmente serio.

La forma de arreglar esto y la forma de hacerlo en las empresas es un montón de listas de comprobación y documentación. No se pueden tener suficientes listas de comprobación. Tal vez al final, cuando tengas 20 páginas de listas de control, una de las casillas puede ser para eliminar algunas casillas, pero no hasta entonces.
En particular, para las empresas que almacenan bitcoin, recomiendo un ritual de firma o una ceremonia de firma. El ritual de la firma es un proceso definido que está bien documentado con listas de control, posiblemente con la vigilancia de vídeo y esto es cosas como el acceso al módulo de seguridad de hardware o las carteras de hardware o la combinación de las carteras de hardware o por separado ir a las carteras de hardware en diferentes lugares y ubicaciones.  Y tener un proceso real y la formación en torno a esto. Y probablemente tendrás que formar a los miembros no técnicos de tu empresa o familia o a quien sea que estés trabajando para que sean capaces de hacer esto. Un ejemplo público que es probablemente el ejemplo público más elaborado de una ceremonia de firma es una ceremonia de firma de claves DNSSEC.  Alguien también me mencionó que Verisign tuvo una ceremonia de firma de claves muy temprana y que incluso utilizaron una cinta VHS para grabar todo el asunto en su día. E incluso tenían procedimientos de transferencia específicamente para manejar la cinta. Pero eso no era público. Esta es probablemente la más pública que verás. Son como 4 horas de ritual y puedes verlo, lo más emocionante que verás en internet.

Si usted fuera a construir para almacenar bitcoin hay tres temas principales para mirar. Uno de ellos es el riesgo, lo que sucede con el material clave, lo que sucederá en el mundo de bitcoin, debes considerar todo esto y escribirlo. También hay un modelo de amenaza: contra qué intentan protegerse los adversarios. Hay cosas de las que no puedes defenderte, como los actores de un estado nacional, pero probablemente puedes defenderte de adversarios menos hábiles y ladrones de poca monta.

Si usted está eligiendo para utilizar un tercero por cualquier razón relacionada con bitcoin incluso es un agente de custodia, o alguien en dos o tres multisig, o incluso si son coinbase.com donde tienen todo el control de su biticon, es necesario preguntar quiénes son, que está trabajando para ellos, ¿cuáles son sus experiencias, están calificados. A menudo he preguntado a las empresas si tienen desarrolladores de bitcoin y a menudo dicen que no, pero afirman ser una empresa de bitcoin, así que ¿cómo saben cómo funcionan los sistemas si en realidad no tienen el talento dentro de la empresa.

A continuación, desea poner juntos la custodia en algo que puede utilizar. Hablamos mucho sobre las carteras de hardware, no voy a repetir esto mucho, esperar a que las pantallas. Los monederos de hardware deben tener pantallas en ellos, esto es muy útil, lo que es el dispositivo de hardware a punto de firmar si le permite firmar.

También hay un segmento del mercado llamado módulos de seguridad de hardware, pero creo que es una forma falsa de diseccionar el mercado o de perfilarlo.  Realmente debería ser el mismo hardware para ambos segmentos del mercado. Además, hay un mayor avance de las carteras de hardware que es ya sea para los intercambios o incluso para uso personal como los nodos de relámpago, usted quiere tener una cartera de hardware que puede firmar rápidamente, especialmente si es capaz de demostrar que aumenta estrictamente los saldos personales. Que son las transacciones por lo general debe estar bien con él, Es útil para el rayo, conjoin y otros fines. Otra forma de tener carteras de hardware es algo que llamo un multisig criptográfico como no bitcoin multisig. Puede tener proceso ritual de firma en lugar de iniciar sesión en su billetera de hardware tal vez usted tiene otros dispositivos de hardware criptográficos necesarios para acceder a ese dispositivo y esto es una capa adicional de seguridad en la parte superior de bitcoin multisig.

Ahora en algunos detalles técnicos, las transacciones de bitcoin parcialmente firmadas hablé de eso hoy temprano en un panel, sólo un formato de serialización, pero hace más fácil la transferencia de datos de las billeteras de bitcoin a los dispositivos de hardware.

Es el bip 174 creo que ya está implementado y fusionado en el núcleo de bitcoin. Las transacciones pre-firmadas son una técnica interesante. Este es el concepto en el que si tienen un proceso elaborado donde tienen que volar alrededor del mundo para acceder a su bitcoin considerar la realización de transacciones por firmado al mismo tiempo. Si el envío de dinero en algún lugar como parte del mantenimiento de las finanzas también puede firmar las transacciones no tienen la intención de enviar.excepto bajo ciertas circunstancias y se puede cifrar los y almacenar los en algún lugar seguro. Usted puede cifrar los y almacenar en algún lugar seguro. En el caso de que usted pierda el acceso a su hardware o el fin del mundo ocurre, puede enviar las transacciones pre-firmadas para cualquier propósito.  Otro método similar a este es una forma de aplicar un sistema similar a las bóvedas de bitcoin. Y esta es una idea en la que envías bitcoin a una dirección y luego con la clave privada para esa dirección que creas especialmente para este propósito firmas una transacción que tiene un bloqueo de tiempo enviándola a otra dirección, luego borras esa clave privada para que sólo firme una transacción de bitcoin en toda su vida. Y esto asegura que el bloqueo de tiempo se hará cumplir. Los adversarios no pueden obtener la clave si se borra.

Creo que deberíamos decir a los reguladores que todo el mundo debería utilizar carteras de hardware o usar carteras de hardware. En general, es bueno decirle a la gente que lo haga. Aunque, curiosamente, en el espacio de bitcoin, muchos de los primeros empresarios eran muy tolerantes al riesgo, por lo que se metieron en bitcoin, que es muy arriesgado, y luego crearon empresas, que también es arriesgado, y estaban muy contentos de ignorar a los reguladores, que es otra capa de riesgo, por lo que deben tener mucho cuidado con las empresas que tratan y averiguar lo que están haciendo realmente.

Y esta es una idea que se me ocurrió, no es particularmente novedosa, en una de mis primeras diapositivas hablaba de que si no se permite tener la custodia de bitcoin si se negocia o se almacena, incluso bajo el pretexto de un propósito financiero más allá de 150 millones de dólares, esta idea es que en lugar de mantener el dinero tienes los inversores o los titulares de bitcoin mantenerlo en sus máquinas, a continuación, se envían instrucciones a sus máquinas y pueden optar por firmar en tales como las operaciones. Resulta que hay una empresa regulada por la SEC llamada New Wave. New Wave hace algo así, excepto que lo guardan todo ellos mismos. Puede que ni siquiera necesiten utilizar una tecnología como ésta.

Otra cosa interesante que se está llevando a cabo es que Christopher Allen y yo y algunos otros estamos organizando un taller de custodia inteligente en San Francisco en el que hablaremos de todos estos temas y analizaremos ejemplos específicos de riesgos de custodia y amenazas y cartera, y también mostraremos cómo utilizar carteras de hardware. Si está interesado puede ir a smartcustody.com

Es sobre todo para las oficinas y las personas que manejan grandes cantidades de dinero, así que ir a la página web o envíenos un correo electrónico.  Deberíamos tener productos de custodia fuera de la estantería, no me refiero sólo al hardware, sino a la formación y a la documentación en vídeo y tener gente que vuele para armarla. No es suficiente con entregar una cartera de hardware, tiene que ser una solución de formación completa y eso es todo lo que tengo.

Hora de finalización: 6:23:21

¿Tengo tiempo para preguntas?

Siguen las preguntas.

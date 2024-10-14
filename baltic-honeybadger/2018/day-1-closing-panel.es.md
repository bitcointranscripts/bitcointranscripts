---
title: Panel de clausura del primer día
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - lightning
speakers:
  - Elizabeth Stark
  - Peter Todd
  - Jameson Lopp
  - Eric Voskuil
  - Alex Petrov
  - Roman Snitko
---
Panel de cierre

<https://twitter.com/kanzure/status/1043517333640241152>

RS: Gracias chicos por unirse al panel. Sólo necesitamos una silla más. Voy a presentar a Alex Petrov aquí porque todos los demás estaban en el escenario. El panel de cierre va a ser una visión general de lo que está sucediendo en bitcoin. Quiero empezar con la pregunta que empecé el año pasado. ¿Cuál es el estado actual de bitcoin en comparación con el año pasado? ¿Qué ha sucedido?

ES: El año pasado, estaba sentado al lado de Craig Wright. Su etiqueta decía "Craig Wright". Era petertodd. He estado en la maleza del mundo del rayo. Está el concepto de hodl a buidl. Hemos visto tantos desarrolladores que llegan a la comunidad con tanto entusiasmo diciendo que estaban interesados en bitcoin y la construcción de aplicaciones y el desarrollo web y relámpago era algo que los hizo interesarse en bitcoin. Conseguir que la gente se entusiasme con estas cosas ha sido increíble para mí en el último año. Además, este año fue mucho menos dramático. ¿Recuerdan que hace un año Breaking Bitcoin Paris fue el punto álgido de todo lo que pasó con No2X y la comunidad prevaleció. Bitcoin no fue atacado con éxito al final del día. Bitcoin no está gobernado por ninguna parte y no será atacado con éxito por gente en una habitación de hotel tratando de hacer tratos. Hay nuevas tecnologías geniales como graftroot y taproot. Este ha sido un año de construcción de tecnología.

JL: Los mercados bajistas son excelentes para los promotores.

ES: Estoy de acuerdo.

JL: Recuerdo que el último mercado bajista fue cuando entré a tiempo completo en Bitgo. Fue poco después de la caída de MtGox y hubo desesperación allí. Yo no tenía dinero allí, por suerte. La gente se preguntaba si el bitcoin seguiría existiendo dentro de unos años, y si esto era el final y estábamos cayendo en la nada. Este mercado bajista tiene su parte justa de desesperación y poca gente que puede venir con varias razones para creer que habrá otra gran burbuja de nuevo y lo que no... pero con el último ciclo de hype hemos captado mucho interés y la gente se ha quedado y la gente que ha mirado más allá del precio y el tipo de cambio se ha dado cuenta de que hay muchas cosas en marcha. El impulso de los desarrolladores ha continuado o se ha acelerado, al menos en parte, a los rayos y el ecosistema de crecimiento y puestos de trabajo. Uno de nuestros mayores retos en Casa va a ser la contratación.

EV: Hace un año, la gente hablaba de divisiones y bifurcaciones y de cómo se iba a producir un caos si alguien iba a ejecutar su nodo de forma diferente y obligar a los demás a hacer lo mismo. Pero ahora podemos seguir escribiendo código.

PT: Probablemente en la última hora, entre la última vez que estuve en el escenario y hace una hora, he hecho más transacciones de bitcoin que en todo el año pasado. Estaba sentado en yalls.org leyendo artículos y pagando con lightning y es mágico. Es una experiencia nueva. Está a la altura de muchas de las expectativas que la gente va a tener. Hay otros aspectos de lightning que considero peligrosos para el bitcoin. Pero el aspecto de la experiencia del usuario funciona, y es increíble ver que algo pase de ser un prototipo a algo que realmente se puede ejecutar en un teléfono y es realmente instantáneo. Demuestra lo que se puede hacer cuando se construye sobre bitcoin. Creo que bcash es maravilloso para bitcoin porque se ha dividido y ahora toda esta gente puede irse. Es un resultado maravilloso. Que hagan lo suyo y no nos molesten. Pueden decir lo que quieran en r/btc y bcash twitter y realmente no es nuestro problema.

AP: Me gustaría ser breve. Primero, te ignoran. Luego... luego intentan luchar contra ti, y luego ganas. ¿En qué estado estamos? Creo que estamos entre la lucha y la victoria. Hay 75 bifurcaciones ahora mismo de bitcoin. Ninguno de ellos tiene valor. Las bifurcaciones ofrecen diferentes soluciones. Intentan demostrar que son más capaces y más rápidos. Bitcoin sigue siendo el número uno. Comprueba el código fuente de la mayoría de las altcoins: todas copian directamente a bitcoin. Intentan conseguir transacciones más rápidas y hacer un montón de cosas, pero lo que les falta a la mayoría es el brillante equilibrio de lo que es bitcoin. Bitcoin existe desde tres puntos diferentes: es una solución técnica, una solución económica y un equilibrio social. Está construyendo una dimensión absolutamente nueva de cómo funciona la economía. Prácticamente está cambiando el viejo estilo de economía de dos a tres dimensiones. Esta es la razón por la que muchos tipos dimensionales están cometiendo sus errores; tratan de hacer una analogía, pero bitcoin no tiene analogía. Es una herramienta monetaria evolutiva.

RS: Quiero hablar de lightning. Elizabeth, has hablado positivamente de todos los cambios y de la adopción que se está produciendo. ¿Cuáles son los cambios actuales con lightning? ¿Hay algún problema que crees que es importante y difícil de resolver tal vez en este momento?

ES: Cuando lanzamos la beta de mainnet, intencionadamente no teníamos una interfaz de usuario para ello porque sabíamos que era una beta temprana y que no estaba terminada. Jameson tuvo un buen tuit sobre esto: ¿cuándo estará listo lightning? Mientras bitcoin esté en beta, lightning seguirá en beta. Esto no está hecho, es un proceso en curso. Ha habido errores. Hemos tenido pruebas increíbles de la comunidad. Por favor, no pongan 325.000 dólares en la red de sus propios bolsillos. Algunas personas han tuiteado que Lightning es inutilizable y que nadie lo usaría, pero resulta que ya lo están usando. Uno de los problemas es la entrada y salida de fondos de Lightning. Si el blockchain es un banco descentralizado, lightning es como una cuenta corriente descentralizada con pagos instantáneos. Con las aplicaciones típicas de lightning, excepto htlc.me, es que no tienen custodia, y hay un problema de gestión de claves. Si queremos conseguir usuarios que no estén familiarizados con estos conceptos, tenemos que trabajar en esos retos y en la intersección entre seguridad y usabilidad. Además, hay que eliminar el concepto de canales para las interfaces de usuario. Si eres avanzado, puedes entrar en el modo avanzado y ver tus canales. Todavía no estamos ahí. Es increíble que Petertodd esté usando una aplicación y comprando en las suyas. Todavía no tenemos torres de vigilancia, sólo puedes recibir, no enviar. Somos muy precoces, estamos a mediados de los 90 del mundo de internet, aún no hemos tenido la llegada del teléfono móvil en 2007. Creo que mucho de esto va a ser un trabajo duro, poner en marcha las torres de vigilancia, conseguir una buena interfaz de usuario, y queda mucho trabajo desafiante. Creo que lo conseguiremos. Llevará tiempo. La gente quiere que ya esté hecho. Pero no lo hemos conseguido.

PT: He optado deliberadamente por utilizar eclair con la configuración por defecto exactamente igual que la que utilizarían otros usuarios. No estoy usando lightning a través de un nodo que dirijo. No estoy usando eclair con mi propia configuración de canales de pago. Quiero lo más obvio. Quiero ver esa experiencia.

RS: Dijiste que la cartera de lightning era inutilizable, luego pasaron algunos meses y se volvió utilizable. ¿Ves que ese progreso continúa todo el tiempo?

PT: No sólo pasó de ser completamente inutilizable a algo que funciona.... sino que la última vez que probé eclair, todos los pagos funcionaron al instante.

RS: Puede que le interese saber que hay una máquina de rayos en Kiev que acepta pagos con rayos. Tienes alguna opinión sobre la red lightning y si es utilizable?

AP: Para crear una adopción y uso masivos, se necesita documentación. A Bitcoin y a Lightning todavía les falta documentación. Hay una razón por la que no tiene documentación, todavía está en desarrollo. ¿Por qué hay una máquina de café en Kyv? Son desarrolladores. Pueden entenderlo. Saben lo que hay que cambiar para que sea realmente útil. Sienten que lo entienden. Pero también necesitan crear más desarrolladores. Sin desarrolladores, es muy difícil adoptar cualquier tecnología. Necesitan una buena documentación. Tenemos que autoorganizarnos y crear la base, tal vez una comunidad separada, que forme constantemente en el uso de la tecnología y cree constantemente la documentación.

RS: Tengo algunas preguntas sobre lightning. ¿Ayuda Lightning a mantener el anonimato y a resistir a los actores estatales y a que el bitcoin sea dinero del mercado negro? ¿Ayuda o no ayuda?

JL: Ayuda porque Lightning tiene privacidad por defecto. Es posible mantener la privacidad en la red principal de Bitcoin, pero requiere mucho trabajo. Mientras que lightning no, aunque bitcoin se pensó originalmente como este dinero anónimo, no creo que se desarrollara realmente con eso en mente. Siempre ha sido un seudónimo. Lightning ha sido desarrollado con una fuerte privacidad en mente. Probablemente todavía habrá consideraciones de privacidad en términos de privacidad en la cadena frente a los canales de cierre abierto... esperemos que se aproveche la privacidad en la cadena, especialmente a medida que consigamos mejores coinjoins y firmas agregadas incorporadas a la cadena de bloques. Espero ver la fusión de una mejor privacidad en la cadena para complementar la privacidad fuera de la cadena.

EV: Suelo no trabajar con lightning y no quiero comentar sobre protocolos que no he implementado. En general, desde el punto de vista de la criptoeconomía, creo que la estratificación tiene sentido. Lo que se quiere evitar al escalar es reducir la seguridad de la capa base. Al permitir que la gente haga un intercambio de seguridad local, una transacción de persona a persona puede hacerse con menos seguridad y, por tanto, con más rendimiento. No estás destruyendo la seguridad de la capa base. Supongo que Lightning está haciendo esa compensación de forma razonable.

RS: Creo que algunas personas han venido aquí para aprender a utilizar el bitcoin en su propio negocio. La mayoría de la gente aquí es de Estados Unidos. Alex no lo es.

ES: Peter es canadiense.

EV: El estado 51.

RS: ¿Cuál es la mejor ubicación para iniciar una empresa de bitcoin hoy en día?

PT: Hice una charla sobre esto. Hay que empezar cerca de la Tierra, porque si no, a medida que te alejas, la dilatación del tiempo jode todo lo demás. Pero, en serio, no hay muchos gobiernos que estén en contra del bitcoin. Sólo hay que arriesgarse y tener cuidado con quién se trata.

ES: Venezuela sin embargo.

PT: Hay unos cuantos lugares que están jodidos. Probablemente la mayoría de la gente en la audiencia está en un buen lugar para empezar un negocio de bitcoin. Yo preferiría centrarme en lo que realmente estás haciendo. ¿Cuál es tu plan de negocios real? Tendrás que hablar con los legos. ¿Tienes una comunidad real y puedes ir a conocer gente? Nadie en mi ciudad hace muchas cosas de bitcoin.

AP: Me gustaría dar la vuelta a la pregunta. No voy a hacer ningún negocio en Corea del Norte. En China, tampoco parece un buen lugar, pero al menos puedes conseguir algunos pros y contras. Georgia y Malta... también empiezan a educar a la gente. Este es el mayor punto, porque están dando recursos. Hay muchos desarrolladores en Ucrania y Bielorrusia. Hay desarrolladores en San Francisco pero el precio es demasiado alto allí.

PT: Uno de los encuentros de bitcoin más interesantes en los que he estado es el de Nairobi, Kenia. Tenían casos de uso reales para el bitcoin. Dependiendo de tu temperamento y del tipo de negocio que puedas llevar... quizás mudarte a Venezuela e ir a ayudar a la gente a contrabandear dinero podría ser lo mejor que podrías hacer por ti mismo. Puede que no sea lo más seguro. Bitcoin no es un sustituto del dinero fiduciario si el gobierno es digno de confianza. Bitcoin empieza a ser atractivo donde no se puede hacer esa suposición, como en Venezuela.

ES: El 20-30% del mundo es mercado negro. Ve a romper la ley, es un dinero de mercado negro.

AP: Sólo menos del 7% de la población en el mundo tiene acceso al sistema bancario. El ejemplo de África es que ellos fuerzan la caída para impulsar la adopción de bitcoin porque es bastante fácil de usar bitcoin no necesita ningún banco sólo necesita un teléfono móvil y ellos tienen teléfonos móviles. Es casi como el 68% de la población mundial que tiene teléfonos móviles. Necesitas proporcionarles una moneda utilizable. Bitcoin + lightning puede ser exactamente esta.. solución en conjunto. Ellos empujarán estos conjuntos. Será herramienta muy simple realmente les permiten realizar el pago y probablemente decir también de la configuración y el gobierno regulado o gobierno sucio con hjust picar dinero y no hace nada.

RS: Última pregunta porque todo el mundo está cansado. Ustedes van a estar en el registro. Quiero que hagáis una predicción. Cualquier predicción. Volveremos el próximo año y veremos si esto se materializa o no. ¿Qué va a pasar en bitcoin en 1 año? Podría ser cualquier cosa, estúpida o no.

JL: Creo que bitcoin va a seguir siendo uno de los principales competidores. Creo que tenemos suficiente efecto de red, interés, desarrolladores e inversión, que apostaría en contra de cualquier tipo de flippings de cualquier tipo.

RS: ¿Y qué pasa con bcash?

JL: Soy optimista sobre muchas cosas, pero no sobre el bcash.

EV: Predecir es difícil, especialmente sobre el futuro. Predigo que la mitad de las predicciones serán erróneas.

PT: Será mejor que vaya a predecir que voy a lanzar un sistema robusto de copias de seguridad de calendarios para opentimestamps y que voy a hacer público mi sistema a prueba de óxido. Llevo mucho retraso en esto. Puedes burlarte de mí el año que viene.

AP: No quiero predecir el precio o lo que sucederá en la economía global. La economía global se enfrentará a una locura en 5-10 años. Bitcoin puede ser realmente el salvador y puede ayudar a recargar la economía. Pero lo que ocurrirá en años es que muchas altcoins caerán definitivamente porque no tienen economía real. Por definición, la economía real, si usted está proporcionando, entonces usted está utilizando, como la moneda para las ofertas reales para la compra o venta de servicios. La mayoría de altcoins ahora mismo son como el plato, en los intercambios, no tiene el caso de uso real en la vida real. Toda la gente está jugando a través del riego de la cara. Ahora mismo están tratando de entender qué es el blockchain qué es el altcoin qué es bitcoin. Y el sur de Daniel fracasará. Al igual que la ICO. Es una gran herramienta. Pero ahora mismo se acero como utilizarla. Y esto es una cara educativa. En el siguiente nivel, el verdadero estado de valor y el falso valor caerá.

RS: ¿Elizabeth?

ES: Voy a predecir que tendremos una implementación de Schnorr para el próximo año, realmente quiero que eso ocurra. Mucha más gente utilizará Lightning en los teléfonos móviles una vez que tengamos las torres de vigilancia funcionando porque queremos que la gente envíe y reciba. Un montón de forkcoins fueron atacados en un 51% y ataques de minería y ataques de doble gasto. Vamos a ver esos con otras monedas especialmente cuando el coste de atacarlas disminuya. Estas son cosas de las que hemos hablado durante años, creo que veremos más ataques en el próximo año.

RS: Gracias a todos, demos un gran aplauso.


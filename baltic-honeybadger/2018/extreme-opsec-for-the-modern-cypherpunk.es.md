---
title: Opsec extremo para el cypherpunk moderno
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - privacy-enhancements
speakers:
  - Jameson Lopp
---
Opsec extremo para el cypherpunk moderno

Jameson es el ingeniero de infraestructuras de Casa. Demos la bienvenida a Jameson Lopp.

# Introducción

Hola compañeros cypherpunks. Estamos bajo ataque. Las corporaciones y los estados nación en su búsqueda de la omnisciencia han despojado lentamente nuestra privacidad. Somos la rana que está siendo hervida en la olla llamada progreso. No podemos confiar en que las corporaciones nos concedan privacidad por su beneficio. Nuestros fracasos aquí son nuestros. Después de haber sido golpeado hace un año, me propuse reiniciar mi vida con un nuevo enfoque en la privacidad. No hay muchos recursos para conseguir lo que quiero.

Es importante señalar que el objetivo de esta presentación no es cómo desaparecer, aunque es un buen libro que recomiendo leer. Si quisiera una privacidad perfecta, habría cerrado mis cuentas en línea, habría reaparecido con un seudónimo y habría dejado de aparecer en público. Mi objetivo es conseguir la mejor privacidad posible sin dejar de mantener mi reputación y poder participar en este ecosistema como yo mismo.

# Seguridad y privacidad

No tendré tiempo para hablar de los aspectos físicos de la seguridad. Otra cosa que hay que tener en cuenta es que muchos de estos consejos son específicos para las jurisdicciones. Revelaré que vivo en algún lugar de los Estados Unidos de América. En general, al mirar los recursos de privacidad, la mayoría de ellos están escritos para los estadounidenses, y esto se debe a que más de ellos están bajo ataque por demandas frívolas, encarcelados por cargos de seguridad nacional, y vigilados más.

Justine Sacco tuiteó un chiste malo en twitter antes de ir a África. Descubrió que era el tema número 1 de twitter en todo el mundo después de que los famosos la denunciaran. Su empleador, una empresa de Internet de Nueva York, declaró que había perdido su trabajo como directora de comunicaciones. Al menos un usuario la fotografió en el aeropuerto. En la era de la información, no hace falta mucho para atraer la ira de millones de personas.

En bitcoin, tenemos una larga historia de ataques físicos contra los bitcoiners que se remonta al primer contribuyente que trabajó con Satoshi, Hal Finney, que fue acosado durante muchos meses y extorsionado por bastante dinero, culminando con el swatting que le llevó a tener que estar a la intemperie en la fría noche de invierno mientras lidiaba con la esclerosis lateral amiotrófica (ELA) y básicamente parapaléjico o posiblemente cuadrapaléjico.

Hay bastantes otros ataques más recientes a medida que el precio del bitcoin ha aumentado y ha habido una adopción por parte de la corriente principal. Parece que hay una correlación entre los ataques físicos contra los criptopropietarios y los picos de precios del mercado y la conciencia de la industria. Parece de sentido común que a medida que el ecosistema se convierte en una corriente principal, los criminales van a ser conscientes de esto y van a calcular su relación riesgo-recompensa y van a atacar a las personas que hablan públicamente sobre cripto. Este círculo vicioso es en realidad el resultado del hecho de que, una vez que te metes en este espacio, te sientes incentivado a querer hablar de él con otras personas, para entenderlo mejor y construirlo. En cuanto hablas de ello, te conviertes en un objetivo. Después de hacer esto durante un número de años, usted tiene mensajes de 3, 4, 5 años atrás y los criminales están haciendo el cálculo mental sobre oh esta persona entró cuando el precio de mercado de bitcoin era X dólares y ahora vale Y dólares por lo que podría ser un objetivo jugoso.

# Niveles de protección de la privacidad

¿Cuántos recursos va a dedicar su atacante para intentar encontrarle? Y por lo tanto, ¿cuánto esfuerzo quiere poner para exigir que se gaste un determinado nivel de recursos? El colmo es un atacante de un estado nación. Si te escondes contra un atacante de un estado nación, no puedo ayudarte. Pero podemos llegar a un entendimiento de cómo hacer que sea razonablemente difícil para el troll promedio en Internet que sabe cómo entrar en varias bases de datos filtradas para hacer que sea difícil para usted ser encontrado.

Algunos de los recursos que utilicé para ello fueron libros como Cómo desaparecer y Cómo ser invisible. Damos mucha información personal. Cada vez que interactúas con un proveedor de servicios diferente, probablemente estás dando tu nombre y dirección. A lo largo de tu vida, has interactuado con miles de bases de datos. Sólo por la magnitud de las diferentes réplicas de tu información en Internet, algunas de ellas se filtrarán o acabarán en bases de datos que pueden ser utilizadas por búsquedas en la web oscura o por inversores que a veces utilizan servicios para obtener esa información.

# Proteger sus ubicaciones físicas

El objetivo es evitar cualquier dato que conecte su nombre y su dirección residencial física y mantener estas cosas fuera de las bases de datos. La solución es, por lo general, utilizar apoderados de todo tipo, incluyendo apoderados electrónicos, legales y físicos. Usted necesita tener la propiedad de su residencia a nombre de otra persona, o bajo una LLC su propia entidad legal, fideicomisos, algún tipo de entidad legal para blindar su nombre de aparecer en varios documentos públicos de propiedad de estas cosas. Usted realmente encontrará que ... Anoche hablé con un grupo de ponentes europeos; esto es muy específico de cada jurisdicción. Probablemente deberías consultar con un abogado sobre esto. Europa no tiene una buena protección de la privacidad con respecto a la creación de entidades legales. Incluso en Estados Unidos, no es tan bueno. Sólo hay dos estados para esto en los EE.UU. - Wyoming y Nevada. Hay alguien que hace entidades específicas de Wyoming, donde este abogado vende la privacidad como un servicio, y utiliza 3 fideicomisos y una LLC, y hace que sea difícil para la gente a perforar múltiples barreras. He oído que Lichentenshein podría tener algunas buenas opciones de privacidad en Europa.

Además, no puedes retroceder nada de esto. No puedes aplicar esto a tu ubicación actual, que ya está quemada. Una vez que tengas una buena configuración, necesitas no filtrar otros datos. Si estás haciendo un livestreaming, quieres una caja a prueba de audio que impida que los sonidos del exterior filtren tu ubicación. Y en las fotos hay que mirar los datos EXIF, y hay que eliminarlos. Si quieres llegar a un extremo, tendrás que preocuparte por el análisis temporal de cosas como las transacciones de bitcoin o cuándo te conectas o twitteas o algo así y cuánto tardas en llegar a casa. Esto sólo importa si estás en una longitud que no tiene mucha masa de tierra.

Con respecto a vivir en un lugar que es propiedad de otra persona, esto funciona bien para muchas personas que son transitorias o que no tienen atacantes específicos que creen que vienen por ellos, sino que simplemente están tratando de protegerse en general. Pero si estás en mi situación en la que crees que alguien te está haciendo daño, entonces probablemente no quieras poner a tu familiar en peligro. No debería recibir ninguna entrega o servicio a su nombre en esta residencia; lo mismo para los servicios públicos.

También debe preocuparse por los documentos que tenga en su casa, no querrá tirarlos a la basura sin triturarlos o quemarlos. Además, el registro de votantes no es una opción. Si quieres privacidad, tienes que renunciar a votar y a figurar en los registros electorales.

Hace unos años, hubo una instalación artística secreta con una transmisión de vídeo. 4chan fue capaz de rastrear la ubicación mirando los aviones que sobrevolaban la cabeza y lo cotejaron con la información pública de los vuelos. Después, por la noche, miraron la posición de las estrellas y redujeron la búsqueda. El último dato fue el de un conductor aleatorio que conducía por esa zona y tocaba el claxon cada pocos minutos hasta que alguien lo encontró en la transmisión y así fue como dieron con la ubicación. No subestimes el poder de Internet.

# Utilizar apoderados de direcciones de correo

Nunca querrá asociar su nombre real y su residencia. Una vez que la asociación se hace y se pone en cualquier base de datos, entonces usted debe considerar que comprometida. Podrías tener problemas para demostrar que tienes una residencia, por lo que podrías necesitar un lote de RV barato o algo para esos fines. Podrías hablar con un abogado, o buscar direcciones virtuales y servicios de reenvío. El inconveniente de los servicios de reenvío es que están en bases de datos propias; no puedes usar un servicio de reenvío comercial como prueba de residencia y te lo rechazan. Así que tienes que utilizar un apartamento o un terreno para autocaravanas que no esté en una de esas bases de datos.

#Mitigar el seguimiento de la ubicación en tiempo real

Es realmente complicado ir por el mundo real; la proliferación de CCTV es bastante terrible. Vamos por ahí con los teléfonos en el bolsillo. Desactiva al máximo el seguimiento de la ubicación en tu teléfono, lo que puede ocurrir o no aunque le digas que lo apague. Por supuesto, mantén el GPS apagado. Hay un "reflectacap" con infrarrojos que emite infrarrojos a las cámaras. El reflectacap refleja los infrarrojos en las cámaras para provocar el desenfoque. También hay gafas infrarrojas para fastidiar el reconocimiento facial. El problema con todos ellos es que tienden a funcionar sólo en condiciones de poca luz. Si eres un noctámbulo y sólo sales por la noche, entonces esto puede estar bien. Para el día, usa una gorra, gafas de sol y una capucha. No querrás ir por ahí con una máscara, porque eso llama la atención y hace que te miren y, de hecho, es ilegal en algunas jurisdicciones.

# Proteger los bienes inmuebles

Tiene que tener protección para sus lambos. La propiedad registrada públicamente se puede buscar en los sitios web de los municipios locales. Usted quiere que las entidades legales posean estas cosas diferentes, y no quiere que todo sea propiedad de la misma entidad legal. Quieres una entidad legal por pieza de propiedad. Digamos que usted entra en su lambo, obtienen su información de la licencia, y un investigador privado hace la búsqueda para encontrar quién es el dueño de este coche y donde está registrado y que podría encontrar que es propiedad de la LLC z y luego hacer otra búsqueda y tratar de encontrar todo lo que es propiedad de esa LLC y si su casa también es propiedad de esa LLC entonces felicitaciones que acaba de encontrar donde vivía a pesar de tener todas estas entidades legales de configuración.

Los registros de impuestos en Estados Unidos generalmente no son información pública, pero hay 60.000 empleados del IRS que tienen acceso a esa información, así que yo no la llamaría privada. Probablemente no quieras que tu residencia real figure en tus impuestos, y hasta donde yo sé, eso es legal.

Las mascotas también se consideran algo que tiene que ser licenciado y gravado y otra fuente de pistas legales para ir a buscarte. Cuando usted tiene vehículos de propiedad de las empresas, entonces usted necesita para obtener el seguro de la flota comercial que tiende a ser 2 veces más caro.

# Proteja su nombre real

Vivas donde vivas, vas a tener que relacionarte con proveedores de servicios y reparadores. No hay ninguna razón para darles tu nombre real. Mejor inventa un seudónimo. Quieres que el seudónimo sea común a la zona en la que vives, y que no sea memorable. Lo mejor que puedes hacer es mirar los datos del censo y encontrar los nombres comunes y elegir uno y usarlo con todo el mundo, porque si no te vas a confundir sobre qué seudónimo has dado a cada proveedor. Namey utiliza los datos del censo de Estados Unidos. No es que estos proveedores de servicios vayan a pedirte tu identificación gubernamental: nadie me ha cuestionado nunca el seudónimo, a menos que estés comprando un artículo con restricción de edad, no esperes que te saquen tarjeta.

# Mantener un perfil bajo

Escóndete entre la multitud. No destaques. Si tienes una cresta o el pelo azul o una barba de medio metro, probablemente deberías pensar en deshacerte de ella ((risas)). No lleves ropa llamativa, no conduzcas un lambo, no hagas modificaciones estúpidas en tus coches como pegatinas o tapacubos de bitcoin. Quieres un estilo de vida corriente sobre el que cualquiera tenga una segunda mirada.

# Proteger su privacidad en línea

Esta es otra lata de gusanos que podría ser su propia presentación. No uses solo google o yahoo, usa duckduckgo o startpage o varios otros. Obtenga la mayor cantidad de estas extensiones del navegador que protegen la privacidad como privacybadger, https everywhere, ublock origin. Usa protonmail en lugar de gmail. Utiliza una VPN como Private Internet Access. Utilizo una VPN para enmascarar mi ubicación geográfica, no sólo por el cifrado del túnel y para evitar el espionaje. Decidir una VPN es bastante complejo. Para un uso más avanzado, te recomiendo que configures tu VPN en el router de tu casa y esto te ahorra mucho tiempo en lugar de configurarlo en cada dispositivo. Tu servidor VPN va a tener un hipo de vez en cuando y entonces tener que reiniciar tu cliente VPN en cada dispositivo es realmente molesto.

Hay un número de firmware del mercado de accesorios como el firmware asus merlin que hace que sea fácil de configurar múltiples proveedores de VPN. Lo importante es configurar un killswitch donde si la VPN se cae, entonces tu router debe dejar de enrutar, de lo contrario, el valor por defecto es enviarlo a través de clearnet y esto sucederá y no te darás cuenta durante días y semanas hasta que no veas esos captchas de "identifica esta señal de la calle" que a menudo tienes cuando tratas de iniciar sesión y luego se detienen.

Con los routers de consumo de gama alta, tengo este router de doble CPU por aquí, tiene un máximo de 30 megabits/segundo y si quieres más que eso quieres un acelerador de VPN o comprar una caja de linux independiente fornido que se configura para ser un router en sí mismo y puede hacer la compresión y descompresión mucho más rápido que estos costosos routers en casa.

# Protégete de tu teléfono

Los teléfonos son realmente terribles para la privacidad, pero son realmente convenientes. La mejor opción es no llevar un teléfono. Si tienes que tener un teléfono, entonces ve a la ruta de prepago. Utiliza dinero en efectivo o alguna forma anónima de comprar un teléfono de prepago que no sea un plan de suscripción que no tenga tu nombre o dirección conectados a él. Puede ser complicado hacerlo. Soy un gran fan de The Wire, así que me imaginé que podría conseguir un quemador en cualquier gasolinera. En mi zona, ese no era el caso. Pedí planes de prepago y me pidieron una identificación. Al parecer, la seguridad nacional y todas esas cosas. Tuve que conectarme a Internet y conseguir un trackphone sin dar información de identificación.

Si utilizas servicios de telefonía virtual como numberproxy y tossable digits... puedes tener un segundo proxy para tu teléfono. Nunca das tu número de teléfono desechable, pero das números virtuales desechables que se reenvían a tu teléfono desechable. Te proteges aún más haciendo esto, y debería protegerte del intercambio de SIM. Si alguien encuentra un número de teléfono asociado a ti, no sabe a qué servicio acudir para intentar hacer ingeniería social para robar tu número de teléfono.

# Otras protecciones de cuentas en línea

La única contraseña que debes conocer es la que sirve para desbloquear el gestor de contraseñas, que deberías asegurar con la autenticación de dos factores por hardware. Todas tus contraseñas deben ser largas y complejas. Los correos electrónicos son un gran punto de fallo. Deberías utilizar siempre el hardware 2FA. No reutilices las contraseñas. Todo lo que entra en una base de datos en Internet acabará siendo comprometido.

Si no eres un fanático de yubikey, entonces trezor puede ser usado como UAF.

# Proteja sus comunicaciones

Signal y Telegram ofrecen algunas opciones para proteger tus comunicaciones. Cisco tiene un servicio de correo electrónico cifrado registrado. Sendsafely envía archivos encriptados. No tengo PGP en esta diapositiva. Puedo contar con una mano el número de personas con las que puedo contactar con correos electrónicos encriptados con PGP, y es demasiado difícil para el usuario medio y no deberías esperar que la gente sepa cómo usar PGP.

# Proteja sus datos financieros

Hay muchas agencias de informes de crédito. Si las piratean, pueden robarte la identidad. Debes acudir a cada una de ellas y solicitar una congelación de seguridad.

# Proteja sus compras

El efectivo es el rey para comprar cosas. Pero en muchos sitios no hay dinero en efectivo para dar el cambio adecuado. Lo siguiente mejor son las tarjetas de débito de prepago. También se pueden obtener diferentes servicios de tarjetas de débito virtuales de prepago; privacy.com es uno de los más interesantes porque te permite crear un número ilimitado de tarjetas con políticas de gasto y tarjetas de prepago. La desventaja es que esto se conecta a tu cuenta de cheques; pero puedes usar una LLC anónima u otra entidad, configurar una cuenta de cheques con ellos, y luego configurar privacy.com a tu cuenta de cheques anónima. Esto funciona, tardan unos días en aprobarlo, pero no he tenido ningún problema con esto.

Te encontrarás con algunos problemas con estos servicios porque algunos comercios no aceptan tarjetas de débito.

# Proteja su licencia de conducir

Tenemos que proporcionar múltiples pruebas de residencia para obtener una licencia de conducir en los EE.UU.. Si te encuentras en esta situación, entonces no puedes probar tu residencia si has hecho los otros pasos de esta presentación. Es posible que tengas que acudir a un amigo, o encontrar alguna habitación o apartamento barato o un lote de vehículos recreativos, porque tienes que conseguir facturas de servicios públicos y extractos bancarios en esa dirección para demostrar que vives allí.

En términos de prevención de fugas en general, porque hay lugares que le piden su identificación, usted puede obtener una tarjeta de pasaporte hwich no tendrá una dirección en él o un estado que usted vive en.

# Proteja su vehículo

Hay algunos productos que puedes conseguir pero que pueden ser legales o ilegales en algunas jurisdicciones. Si tienes un coche propiedad de una empresa anónima, probablemente sea lo mejor que puedas hacer. Muchos de estos coches más nuevos tienen servicios de rastreo incorporados; es posible que quieras desactivarlos. Es posible que desee obtener un vehículo más antiguo o uno más barato que no tiene eso. He descubierto que he podido utilizar LLCs anónimas para crear cuentas con servicios de transporte compartido p2p. Puedo usar Uber y Lyft sin tener mi identidad asociada a esas cuentas y así no tener mis movimientos rastreados.

# Proteger sus datos en las fronteras nacionales

Hay varias escuelas de pensamiento aquí. Una de ellas es llevar tus datos contigo y encriptarlos, o la otra es no llevar ningún dato. ¿Cómo vas a conseguir realmente los datos en el otro lado? Podrías enviar por correo una unidad encriptada a tu país; podrías tenerla alojada en un servidor seguro que descargues más tarde, pero con la esperanza de que haya suficiente ancho de banda... o utilizar tu cliente como un cliente ligero y conectarte a un servidor remoto.

# Stretch goal: Misdirection

Si quieres una fase de desafío, prueba a despistar. Cuando te estés preparando para mudarte, habla con varias personas y diles que te vas a mudar a un lugar que no es. Incluso puedes hacer un viaje, comprobar un lugar, ver algunos apartamentos, abrir una pequeña cuenta bancaria que no te cueste mucho, conseguir un ping en tu informe de crédito que te estás estableciendo en esa zona antes de bloquear tu crédito. Lo que tratas de hacer es que le cueste más recursos a alguien encontrarte. Enviándolos por el camino equivocado, con suerte se darán cuenta de que los estás jodiendo.

# Pruebas de estrés

La única manera de saber que esto funciona es si alguien puede encontrarlo. Así que he contratado a investigadores privados y a hackers de sombrero blanco para que intenten localizarme. Pensé que mi licencia de conducir no sería un gran problema. La mayoría de los estados en los EE.UU. han estado vendiendo los datos de la licencia de conducir durante décadas en este punto. Además, podrías hacer ingeniería social con tus amigos y familiares. Estos son los puntos débiles. También, la gente con la que trabajas para configurar tu privacidad, como banqueros y abogados. Casi todos no tienen ni idea de cómo hacer estas cosas y van a cometer errores. Puedes pedirles que sólo usen VPNs y canales encriptados y probablemente enviarán cosas sin encriptar, así que tienes que vigilar tu espalda y vigilar a todos los que trabajan contigo.

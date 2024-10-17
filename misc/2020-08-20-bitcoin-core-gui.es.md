---
title: Reunión introductoria de la GUI de Bitcoin Core
transcript_by: Michael Folkson
translation_by: Blue Moon
tags: ['bitcoin-core', 'ux']
date: 2020-08-20
aliases: ['/es/bitcoin-design/2020-08-20-bitcoin-core-gui']
---
Tema: Enlace del orden del día publicado a continuación

Ubicación: Diseño de Bitcoin (en línea)

Vídeo: No se ha publicado ningún vídeo en línea

Agenda: https://github.com/BitcoinDesign/Meta/issues/8

La conversación se ha anonimizado por defecto para proteger la identidad de los participantes. Aquellos que han expresado su preferencia por que se atribuyan sus comentarios son atribuidos. Si usted ha participado y quiere que sus comentarios sean atribuidos, póngase en contacto con nosotros.

## Revisión de Bitcoin Core PR

Parece que hay mucho que aprender sobre los antecedentes de Bitcoin Core, cómo se hace el trabajo, lo que debería ser, lo que es ahora mismo, por qué es como es ahora mismo. Tengo curiosidad por aprender más allí.

Muchos de los enlaces son sobre la revisión, cómo revisar y todas estas cosas. Siento que como diseñador no puedo ayudar con eso tanto como me gustaría. Ni siquiera sé qué podría hacer ahí. Entiendo totalmente la necesidad y que es una prioridad para el desarrollo, pero personalmente no puedo ayudar allí.

Puedo ver por qué piensas eso y para algunos PRs y temas estoy seguro de que es el caso dependiendo de lo técnico que seas. Sin embargo, ha habido discusiones en el pasado en las que un revisor ha dicho "me gusta esto" y el siguiente ha dicho "no me gusta eso, me gusta esto". Creo que es entonces cuando alguien con experiencia en diseño que puede ir a preguntar a la gente y volver con una opinión sobre lo que es mejor para un determinado grupo de usuarios añadiría valor a esa discusión. Incluso si usted no es técnico, no sé lo técnico que eres todavía creo que va a haber ciertas cuestiones y ciertas solicitudes de extracción donde se puede añadir valor a las discusiones y las revisiones.

Para las cosas que están directamente relacionadas con la interfaz de usuario, sin duda. De la lectura de estos documentos se desprende que hay una gran cantidad de trabajo de codificación más pesado donde se necesitan revisiones. Eso debería ser priorizado en términos de trabajo de revisión. El trabajo de la interfaz de usuario es bastante mínimo en comparación.

La revisión es la única manera de que las cosas puedan ser implementadas en el código.

En términos de conocimientos técnicos, no sé cómo construir localmente la cartera y ejecutar una rama en mi ordenador. Revisar para mí es típicamente capturas de pantalla que alguien comparte. Hay una brecha técnica para mí.

Soy razonablemente técnico, quiero jugar con la construcción. No estoy seguro si quiero contribuir de esa manera. Hay muchos temas abiertos en este momento que son fáciles de arrojar nueva luz. Estaba mirando uno que puso fanquake, hacer un icono de Tor para un estado activo y no activo y empujarlo en el repo. Bastante fácil sin tener que compilar completamente el Qt localmente y ejecutarlo.

Lo que me gusta es que en Figma o Sketch, o cualquier otra herramienta de diseño que tengamos, se reproduce uno a uno el software real. Primero se hace un diseño antes del desarrollo y, cuando éste llega, todos los problemas de la interfaz de usuario se han discutido y resuelto. Esto simplifica el desarrollo porque no hay que construir la interfaz de usuario de una manera y luego rehacerla. Ya has resuelto muchas de esas cosas. Cómo deben llamarse, dónde están ubicados y todas estas cosas. Requiere un montón de coordinación porque en la fase inicial de planificación y discusión, es donde se hace el estilo y el diseño inicial. Al principio es más trabajo de planificación y coordinación, pero luego la implementación se hace más fácil. Eso facilita la colaboración de los diseñadores.

## Diseñando para múltiples sistemas operativos

Como codificador, ¿cómo van a soportar los diseñadores múltiples... la misma UI para MacOS, Windows, Linux?

Acabo de empezar a hacer un archivo Figma, que es una manera de mostrar qué elementos encajan donde. Tengo una sesión para Mac, Linux y Windows. He estado importando los diseños de la actual GUI y rehaciéndolos en Figma. Tener esos componentes reutilizables para que cuando la gente empiece a trabajar en los diseños pueda hacerlos utilizando los elementos del sistema operativo actual.

Hay un contexto histórico. Antes de que los diseñadores se involucraran en el desarrollo de la GUI de Bitcoin Core había discusiones en el repo de Bitcoin Core sobre el estilo de la GUI. ¿Debería ser un estilo único para todos los sistemas operativos o debería ser nativo para cada sistema? El consenso es que se prefiere el estilo nativo. Core en MacOS se ve como cualquier otra aplicación de MacOS. Core en Windows se ve como cualquier otra aplicación de Windows. ¿Es la forma correcta? ¿Deberíamos tener un estilo uniforme para cualquier plataforma? ¿Es más fácil para un diseñador? Si es así, los codificadores deberían implementar un estilo personalizado en el código primero.

Hay algunos elementos que son muy fáciles de hacer que se parezcan a su sistema operativo nativo. Un botón, cambiar el tamaño de la letra, cambiar el color de la letra. ¿No hay algunas diferencias fundamentales entre Windows, Linux y Mac que no se pueden localizar tan fácilmente cambiando colores, contornos, fondos o tipos de letra? ¿Se ve y se siente nativo en todas partes o se siente un poco fuera de lugar? No se puede ajustar del todo. ¿Cómo de buena es esta localización? Supongo que esa es la cuestión.

He estado ejecutando la interfaz gráfica de usuario en Mac, Linux y Windows y definitivamente creo que hay algunas inconsistencias en las tres plataformas. Definitivamente son nativas pero hay algunas cosas que son bastante nativas. Para ser honesto, la versión de Linux es probablemente la que mejor se ve, lo cual es sorprendente. Normalmente es Mac o Windows.

¿Sientes que si lo sacas en Windows parece una aplicación de Windows? ¿Tienes esa sensación?

Personalmente, preferiría tener un solo diseño para todas las plataformas. No me gusta la sensación de Mac o de Windows, sólo me importa que se vea bien, que se sienta bien y que haga lo que se supone que tiene que hacer. Se sienten como una aplicación de Windows o una aplicación de Linux o una aplicación de Mac. ¿Es eso lo que la gente quiere? Personalmente, creo que una aplicación sería más fácil desde el punto de vista del diseño.

Incluso el proceso de incorporación para Mac y Windows son diferentes para la GUI de Bitcoin Core.

Es lo mismo. En MacOS, Windows y Linux el proceso de incorporación es el mismo.

Intenté ejecutar una GUI de Bitcoin Core en Windows y el aspecto era diferente al de Linux y Mac. Puede que tenga los mismos pasos, pero visualmente creo que parecía diferente.

La interfaz gráfica de Bitcoin Core utiliza el framework multiplataforma Qt, que fue elegido por su naturaleza multiplataforma. Fue hace mucho tiempo. Si no recuerdo mal fue Wladimir van der Laan quien implementó la GUI en Qt la primera vez. El framework Qt, fue una buena elección para ese momento por el soporte multiplataforma. Tenemos soporte para cualquier plataforma, Windows, MacOS, ARM, Linux cualquiera. El estilo en Qt tiene opciones. La opción por defecto es heredar el estilo nativo del sistema operativo. La mayoría de los widgets de Qt tienen la capacidad de ser personalizados. Esa capacidad no se utiliza ahora.

¿Eso es sólo para el onboarding? Cuando llegas a la GUI real no estás usando las plantillas por defecto, ¿verdad?

## Haciendo cambios en la GUI de Bitcoin Core

Está el desarrollo de características, está la capa de estilo visual y luego está la mejora o el trabajo en la capa de interacción. El flujo de incorporación que no añade ninguna característica, pero hace que la interacción sea más agradable para los nuevos usuarios para configurar las cosas. Entonces, acabamos de hablar del estilo visual. Personalmente, mi impresión es que el estilo visual es mucho menos prioritario que el nivel de características y algunos de los niveles de interacción. El nivel de características es la creación de nuevas cosas y en el nivel de interacción yo incluiría la introducción de algunas funcionalidades que existen en la API o en la línea de comandos y llevarlas a la GUI. Incluiría eso en la mejora del modelo de interacción. ¿Es correcta mi suposición?

Estoy de acuerdo. La interacción del Onboarding fue discutida muchas veces en el repo de Bitcoin Core. ¿Cómo podría ser? ¿Cómo debería ser? ¿Qué pasos deberían incluirse?

Creo que es algo en lo que la comunidad de diseñadores puede ayudar.

El repo de Bitcoin Core funciona en pequeños pasos mucho mejor si se implementa. Puedo sugerir un primer paso de onboarding usando un asistente y eligiendo el idioma. Estos pasos nos permitirán añadir características adicionales a la interacción del onboarding. Las primeras etapas son bastante simples y podrían ser implementadas en el código rápidamente.

Es bastante fácil diseñar esto en Figma. Usted puede planificar para el futuro, los próximos cinco o diez pasos. Entonces eliges uno para la primera implementación y tal vez consigas algo de impulso con la ayuda de otras personas y se añadan más pasos. El diseño es más fácil cuando se sabe a grandes rasgos cómo se quiere que sean las cosas en el futuro.

En el onboarding lo que tenía en mente era centrarse en lo que es rápido de hacer y no implica muchos obstáculos técnicos. Elegir el idioma en la primera pantalla. En la segunda pantalla, una sección sobre el nodo, qué es exactamente eso, qué es un nodo podado y qué es un nodo completo. Creo que tener esos pasos de incorporación supondría una gran diferencia. Luego, en la versión 2 del asistente, para hacerlo más completo, añadir la capacidad de crear una cartera en el asistente de incorporación en lugar de tener que obtener una diferencia en las carteras creadas al azar sin ninguna notificación en la interfaz gráfica de usuario. Esto es bastante confuso en este momento. Obviamente es un obstáculo técnico mayor, mejor dar algunos pasos de bebé. Ese es el enfoque que yo estaba buscando, versiones lentas en lugar de presentar un asistente completo con diferentes Crear Cartera, Cargar Cartera y diferentes flujos. Eso sería más abrumador para los colaboradores del núcleo. Hazlo en pequeños componentes.

Hay limitaciones. No estoy del todo seguro de cuáles son esas limitaciones porque es un proyecto gestionado por consenso. Podemos ir a una persona y preguntarle cuáles son las limitaciones y puede dar una respuesta ligeramente diferente a la que daría si le preguntáramos a otra persona. Me gustaría saber cuáles son las limitaciones para poder trabajar dentro de ellas. Lo único que diría acerca de los pasos de bebé es que incluso en las cosas de fondo han tenido una visión general de dónde están tratando de llegar, es sólo que los RP que introducen en el proyecto son pasos de bebé. No hay nada de malo en decir "Esto es a lo que nos gustaría llegar como destino, pero tenemos que introducirlo en la base de código gradualmente para que la gente se sienta cómoda con ello". Se puede tener lo mejor de ambos mundos.

Creo que las limitaciones son sobre todo técnicas. Por ejemplo, en la implementación de Qt, la interfaz gráfica de usuario interactúa con el núcleo con sistemas de señales y ranuras. Incluso los sistemas mejorados de señales y ranuras de Qt a veces fallan silenciosamente. El usuario no tiene información correcta sobre los datos del núcleo o tiene información errónea de los datos del núcleo. No puede distinguir si los datos son verdaderos o si el sistema de señales y ranuras falla silenciosamente. Esto requiere muchas pruebas reales. Actualmente Core tiene múltiples pruebas unitarias y funcionales. Cada vez que construimos y compilamos ejecutamos pruebas para garantizar que todo funciona bien. La GUI no tiene tales pruebas funcionales automatizadas. Es necesario realizar pruebas manuales. Existen restricciones y estas restricciones son principalmente heredadas del marco Qt y heredadas de la seguridad de Core.

Estaría encantado de ayudar en las pruebas si pudiera poner en marcha el material de desarrollo en mi ordenador.

Creo que es plausible ponerlo en marcha haciendo eso. No creo que sea difícil construir PRs. Volviendo a la discusión de la revisión no tienes que firmar todo. No es como si al hacer una revisión tuvieras que decir "Este código está bien. No hay errores. He mirado todos los aspectos de este RP y todo está bien". Puedes escoger un aspecto y decir "En la cuestión del diseño pienso esto pero no he revisado el código, no he hecho esto". La revisión es realmente importante y todo el valor que podamos obtener de cualquier conjunto de habilidades que alguien tenga, mejor. Ciertamente hay un valor que puedes aportar con tu experiencia.

## Conseguir el consenso para los cambios de la interfaz gráfica de usuario

En el consenso, cuando trabajaba en la GUI de Monero lo que ocurría a menudo es que yo sugería algo a los desarrolladores y ellos decían "No nos lo digas a nosotros, díselo a la comunidad". Así que lo publiqué en Reddit con 150.000 personas. Con las características más grandes, las cosas más nuevas, el primer paso era lanzarlo al público para ver lo que todo el mundo piensa. Luego, sólo después, el equipo trabajaría en las cosas. Podían dar su opinión, pero la idea era ponerlo en el espacio público. Hubo un proceso en el que las ideas se probaron primero en una fase pública y se ajustaron las buenas. En un momento dado, pasaban al desarrollo real. Podía desarrollarse una pequeña cosa o el conjunto, tal vez se tardaba medio año más o menos. Era un proceso bastante lento. Si lo miras en una línea de tiempo más larga, es mucho más fácil para mucha gente pensar en ello y crear un consenso sobre algo. El consenso no se produce a nivel de relaciones públicas y asuntos, pero es un proceso más largo. ¿Está ocurriendo algo así?

No he visto que eso ocurra en Core, aparte de un gran cambio de consenso en la bifurcación suave. En el caso de algo como Taproot, es muy importante que la comunidad se comprometa y la apoye, ya que se trata de un cambio consensuado en el código. En general, para todo lo demás es la comunidad de desarrolladores en torno a GitHub la que discute lo que es mejor. Obviamente, el diseño es un poco diferente en el sentido de que las decisiones de fondo son diferentes a lo que es mejor para este tipo de usuario. No puedo hablar por todo el mundo, sólo puedo hablar por mí mismo, pero supongo que cualquier proceso con el que estés contento en términos de cómo obtienes la retroalimentación de tus futuros usuarios podría ser utilizado dentro de este proceso. Si no quieres ir a Reddit y tener discusiones con cientos de extraños al azar para obtener comentarios sobre los cambios de diseño que quieres hacer, no tienes que hacerlo. Depende de cómo trabajes y de cómo te guste más recibir opiniones sobre las decisiones de diseño que deban tomarse.

Sobre los desarrolladores del núcleo que tienen diferentes ideas sobre las limitaciones y lo que funciona y lo que no funciona, compártelo en el subreddit de Bitcoin y consigue cientos de respuestas y comentarios. Eso puede servir para convencer a los desarrolladores de por qué estás probando un determinado diseño. En lugar de decir "soy un diseñador, esto es bueno" y sentarse a hacer bikeshed, preocupándose por los pequeños detalles. Creo que esto sería una buena idea para trabajar en la GUI.

Creo que cualquier buen diseñador irá a buscar opiniones. No digo que un diseñador tome todas las decisiones en su cabeza. Parte del proceso de diseño consiste en obtener la opinión de los usuarios potenciales. Lo que estoy diciendo es que cualquier cosa que sea preferible para ti en términos de cómo trabajas para obtener esa retroalimentación creo que estaría bien dentro de este marco del proyecto Bitcoin Core. No estoy diciendo que no se obtenga retroalimentación, estoy diciendo que se obtenga retroalimentación de la manera en que te sientas cómodo. La única cosa que me preocupa en el enfoque de Reddit es que a menudo en cosas de back-end en lugar de cosas de diseño alguien abrirá un tema y dirá "Esta encuesta tuvo un 50 por ciento que le gusta esto por lo que debemos implementarlo en el Core". Todo el mundo en el núcleo sería como "No nos importa si es popular, que requeriría mucho trabajo en el núcleo para hacerlo". No es democracia, es gente que tiene un gran conocimiento de cómo funciona el proyecto y que ha luchado con el código durante muchos años, su opinión significa más que la de alguien que ni siquiera ha utilizado nunca la interfaz gráfica de Bitcoin Core. Que ellos digan que me gustaría esta característica en lugar de esta otra no va a convencer a un desarrollador del núcleo para hacer ese cambio si el desarrollador del núcleo piensa que es un mal cambio.

Es un tema delicado. Cuando publicaba cosas en Reddit siempre incluía el diseño y un screencast de un vídeo en el que hablaba de él durante cinco o diez minutos. Puedo narrar claramente cuál es el pensamiento que hay detrás y cómo se relaciona con el actual y qué es diferente. Cuando sólo se publica una imagen, la gente se limita a mirar un botón o algo así, y mira las cosas equivocadas porque no hay una guía sobre lo que significa este cambio y por qué se hizo. Realmente se trata de cómo se escriben esos posts para conseguir un buen feedback. Requiere un esfuerzo y puede salir terriblemente mal.

Si te gusta hacerlo entonces hazlo. Si no crees que sea la mejor manera de obtener feedback entonces haz lo que sea más productivo para obtenerlo antes de ir a GitHub y decir "creo que esto es lo mejor porque obtuve feedback de esta manera específica".

Podría ser que el asistente de diez pasos viva en el espacio público y se discuta mucho mientras se implementa el primer paso. El resto se sigue discutiendo y cuando llega el momento de implementar el paso 2 o 3 ya se ha discutido mucho.

## Interacción de los diseñadores con los desarrolladores de Core

Tengo una pregunta sobre la interacción entre el diseñador y el codificador. He visto bocetos en Figma pero como codificador necesito el tamaño de la ventana y los píxeles. ¿La ventana es fija? Necesito los nombres de las fuentes y el tamaño de las mismas. ¿Cómo funcionan estas interacciones? ¿Debería un diseñador abrir un tema en nuestro repositorio para describir estos elementos que el codificador debería implementar?

Creo que depende. En Figma, en la parte superior derecha hay una pestaña de Código. Si haces clic en ella, todo lo que selecciones en la interfaz de usuario se mostrará... Si haces doble clic en un campo de texto, te dirá qué fuente es, qué tamaño tiene, qué tamaño de fuente tiene.

¿Debo iniciar sesión en Figma?

Puedo compartir mi pantalla aquí, te mostraré. Algunas cosas Figma es bueno que pero nunca hay un reemplazo para hablar con los demás. Aquí en la parte superior derecha se ve esta pestaña Código. Cada vez que hago clic en este campo de texto aquí me mostrará la familia de la fuente, el tamaño. Si paso el ratón por encima de otro elemento, me dice cuál es la distancia a ese otro elemento. Si miras este, a la izquierda verás que es de color púrpura y tiene este icono aquí. Significa que es un componente. Puedo ir al componente principal aquí. Figma también tiene un sistema de componentes donde cualquier cambio que hago a este componente principal se hereda por todas las instancias de ese componente. Creo algunas instancias aquí. Si hago que el componente principal sea amarillo, las instancias también heredarán esto. Cuando miro el código de una instancia me dice cuál es el componente principal. Hay un montón de cosas así en Figma. Si el diseño está configurado de esta manera, como desarrollador siempre puedes mirar el componente principal y ver cómo funciona. Como diseñador no puedes hacer todas estas cosas especiales únicas en cada lugar porque está automatizado. Hay propiedades fijas para todos los elementos que se utilizan. Eso es lo mismo con los colores aquí, estos son todos los colores utilizados en la interfaz. Puedes hacer lo mismo con los estilos de texto. Como diseñador y desarrollador siempre tienes que comunicarte con el otro, pero si tienes una buena configuración como esa, hace que el desarrollo del diseño sea más fácil porque hay un lenguaje compartido de estilos de texto, componentes y su aspecto. Sabes cuáles son las restricciones. No tienes que comprobar con cada botón cuál es el color porque siempre es el color del componente principal. Hay algunas cosas así en Figma que son realmente útiles. Hay un montón de interés en la comunidad de diseño para tener un curso intensivo de Figma. Hicimos uno hace un mes, pero hay más interés. Sólo tenemos que organizar eso y hablar de la colaboración, lo que los diseñadores pueden hacer y lo que no pueden hacer.

Una cosa que estoy notando es que hay una brecha entre los codificadores y los diseñadores. Una cosa que podríamos necesitar para desarrollar más son los codificadores que están interesados en este proyecto. Si todo lo que tenemos son diseñadores y no tenemos a nadie que codifique, no llegaremos a ninguna parte.

¿Tener un sistema de diseño establecido, una documentación que especifique todo esto sería algo que los chicos querrían? En lugar de tener que entrar en Figma y mirar la guía de estilo... En BTCPay no está terminado pero tienen un sistema de diseño que especifica todo este tipo de cosas. Nosotros seguimos esas guías en nuestros diseños de Figma. Cuando compartimos vídeos sabes que estamos siguiendo esas especificaciones. Eso facilita las cosas en lugar de tener que entrar en Figma y mirarlo.

¿Los desarrolladores principales trabajan en todo o hay una o dos personas que sólo trabajan en la interfaz gráfica de usuario, una o dos personas que sólo trabajan en la seguridad o es bastante mixto?

Es personal, depende de la persona. La gente trabaja en lo que es su experiencia. Algunos desarrolladores tienen experiencia en seguridad, en código de consenso, algunos desarrolladores tienen experiencia en el código de la interfaz gráfica de usuario. Podría enumerar a los desarrolladores. Promag, Sjors, Luke Dashjr, fanquake.

Si presentáramos un diseño a la comunidad y luego, en última instancia, a estos desarrolladores, ¿crees que estarían interesados no sólo en dar su opinión, sino también en escribir el código para ello?

Personalmente estoy interesado en escribir el código a partir de las sugerencias de los diseñadores.

Fanquake hace mucho trabajo en el sistema de construcción, Luke hace mucho trabajo fuera de la GUI. Supongo que de esas personas que nombraste probablemente no estarían interesadas en codificar un diseño completamente nuevo. Mirarían los PRs que se abren, pero supongo que la mayoría de esos cuatro, si no todos, no querrían tomar un diseño y codificarlo todo ellos mismos.

Lo que pasó en Monero fue interesante. Yo sólo tenía un diseño por diversión, lo publiqué en Reddit. Un desarrollador que había querido ayudar en la GUI de Monero, lo cogió y dijo "quiero implementar esto". Para él fue una oportunidad de unirse al proyecto porque ese era su interés pero no tenía algo con lo que trabajar. Coincidimos en este diseño. Era su manera de empezar. Tal vez si hubiera cosas interesantes por ahí que estuvieran abiertas y disponibles, entonces tal vez hubiera alguien que estuviera interesado en entrar. Poner las cosas ahí fuera a veces es todo lo que se necesita. No está garantizado. También tengo un diseño en el repositorio de Monero que ha estado allí durante un año y nadie ha hecho nada con él, lo que también está bien. A veces puede funcionar así.

## Usuarios objetivo

En los diseños actuales de Figma ([aquí](https://www.figma.com/file/FJ02rY3m8V9ZCDvoXjW39W/Bitcoin-Core?node-id=281%3A0) y [aquí](https://www.figma.com/file/FJ02rY3m8V9ZCDvoXjW39W/Bitcoin-Core?node-id=462%3A655)) ¿qué tipo de usuario teníais en mente para esto?

En la llamada que tuvimos la otra semana discutimos que la GUI es generalmente usada por usuarios avanzados, gente que sabe una cantidad decente sobre Bitcoin y no generalmente principiantes. El objetivo general que tenemos en mente es que los principiantes se unan a nosotros para que más gente ejecute nodos y cosas así. Mientras diseñaba esto, tenía una visión bastante amplia de la base de usuarios, atendiendo a cualquier persona, desde principiantes hasta usuarios avanzados. Hay elementos técnicos que se dirigen exclusivamente a los usuarios avanzados. Al diseñar las tripas de la interfaz gráfica de usuario me centré más en si es para usuarios avanzados o para principiantes. Creo que tener un proceso de incorporación es adecuado para cualquier persona. Creo que ayuda a explicar las cosas, da algo de contexto y comprensión de lo que están haciendo exactamente.

¿Sería posible introducir versiones opcionales? Una GUI para principiantes, una GUI para usuarios avanzados. ¿Hay alguna forma de separar las GUIs dependiendo de quién sea el usuario?

No estoy seguro en el aspecto técnico. Creo que sería mucho trabajo. Creo que un solo diseño puede atender a todos los públicos. Las características más complejas pueden ser escondidas detrás de las escenas sólo para ser accedidas por aquellos que las necesitan.

En la GUI de Monero, yo estaba en contra, pero decidieron tener un modo simple y un modo avanzado. El modo avanzado tenía la minería, tenía la firma de mensajes, tenía una página de comerciante, un tipo de punto de venta. Había un montón de otros tipos de ajustes. Cuando inicias la aplicación te pregunta algunas cosas. Si quieres arrancar un nodo remoto, el modo simple o el modo avanzado y luego la interfaz se ajustó. Creo que Bitcoin Core tiene menos funcionalidad, no tiene minería por ejemplo o una pantalla de comerciante. Mi corazonada ahora mismo es que no es necesariamente necesario pero quizás más adelante podría ser algo en lo que pensar.

En los monederos se utilizan características más avanzadas como la selección de monedas.

Va a haber mucho trabajo, pero creo que habrá maneras de implementar estas características más avanzadas, como la selección de monedas, de una manera fácil de usar. Creo que sería posible hacerlo. Prefiero ir por ese camino, tener algo fácil con cosas escondidas. La cara de la GUI dirigida a los principiantes.

En cuanto a la localización, ¿hay un esfuerzo de localización?

¿Se refiere a la traducción?

Sí.

Bitcoin Core tiene traducción con Transifex. Se extrae la traducción de Transifex. Los traductores de Bitcoin Core son otra comunidad como la de diseñadores y desarrolladores.

En cualquier idioma que utilices, es posible que la comunidad de traductores tenga ya algunas directrices sobre cómo llamar a ciertas cosas. Puede que merezca la pena comprobarlo cuando escriba el texto.

Cualquier traducción que se añada a la página del proyecto en Transifex se añade automáticamente como una etapa del proceso de liberación.

Sería bueno ver un tema abierto en el repo sobre el onboarding con un enlace a los bocetos de Figma. Traigamos Figma a nuestro repo para empezar a trabajar en la codificación.

Haré un prototipo y un video también para que haya un visual que la gente pueda ver. Pueden usar Figma para ver las tripas. Un video parece comunicar lo que está pasando un poco más fácil.

Para empezar, basta con un enlace al boceto de Figma.

Los archivos de Figma pueden llegar a ser enormes y súper confusos. ¿Qué hay de otras convocatorias? ¿Sesiones de diseño, curso intensivo de Figma, cualquier otra cosa que sea útil o que se pueda hacer? ¿O nos limitamos a GitHub y Slack por ahora?

Probablemente asistiría a un curso intensivo de Figma. Me gustaría entender exactamente los cambios, justo en las tripas de lo que hiciste en la GUI de Monero dado que es Qt al igual que Bitcoin Core. Creo que es un caso de estudio realmente interesante y cómo trabajasteis y qué necesitasteis de otras personas. No sé si eso es una llamada o una presentación o una discusión o algo que podamos poner en YouTube o algo así. Algo para que podamos aprender todo lo posible de ese proyecto. Creo que habrá similitudes.

Bitcoin Core utiliza widgets Qt mientras que Monero utiliza Qt QML que tienen restricciones de diseño muy diferentes. Creo que el QML que utiliza Monero es mucho más flexible y fácil de personalizar, mientras que los widgets son un poco menos personalizables.

Una cosa importante con Monero fue que había un desarrollador muy motivado que realmente quería hacer esto. Realmente lo impulsó. Yo, como diseñador, no sabría por dónde empezar a coordinar a la gente. Se puso en contacto conmigo para tratar diferentes temas y tuvimos un buen intercambio de opiniones. Su comunicación y su energía me ayudaron mucho. También solicitó financiación, Monero es todo financiación comunitaria. "Esto es lo que quiero hacer. Dame esta cantidad de Monero" y la gente dona. Pudo trabajar en esto a tiempo completo. Eso hizo una gran diferencia.

Quizás necesitemos este proyecto global. La preocupación desde la perspectiva del Núcleo es que tenemos este nuevo [repo](https://github.com/bitcoin-core/gui) de Bitcoin Core GUI y todos los contribuyentes existentes se van a olvidar de él y no vamos a conseguir nuevos contribuyentes en el GUI. Simplemente se quedará ahí y no obtendrá el interés o los ojos que habría obtenido si se hubiera quedado en el repo principal de Bitcoin Core. Tal vez un proyecto global para renovar la interfaz gráfica de usuario atraerá a más personas a contribuir y revisar los PRs y llamar la atención sobre ella.

Sólo un puñado de personas motivadas puede marcar una gran diferencia.

¿Crees que hay suficiente para discutir en Monero en términos de lecciones o cambios que podrían ser replicados en Core?

No creo que sea fácil. Monero utiliza Qt QML pero Core utiliza widgets. Son muy diferentes. Bitcoin Core tiene un [pull request](https://github.com/bitcoin/bitcoin/pull/16883) para cambiar a QML. No tiene mucho apoyo. No sé por qué. Se requiere mucha revisión para cambiar de widgets a QML.

No puedo hablar de los desafíos técnicos de lo complejo que era todo. Tal vez podríamos traer al desarrollador de Monero para que hable de ese aspecto. Sólo puedo hablar del lado del diseño. Los desarrolladores de Monero están en el IRC todo el día y no sé cómo lo hacen en cuanto a tiempo y atención. No sé cuáles fueron todos los desafíos y cómo se desarrolló todo eso.

Hay un contexto interesante aquí en este PR. Con esta [separación de procesos](https://bitcoin.stackexchange.com/questions/98398/what-is-the-motivation-behind-russell-yanofskys-work-to-separate-bitcoin-core-i) se van a construir más interfaces gráficas ambiciosas y experimentales que pueden conectarse a Core. La gente puede trabajar en ambos. Pueden trabajar en la sólida interfaz gráfica de usuario estándar de Bitcoin Core y también en interfaces gráficas de usuario más experimentales si no pueden introducirlas en el código base de Core.

¿Hacemos otra convocatoria en un par de semanas?

Intentaré organizar un curso intensivo de Figma, pero no se centrará en la GUI del Core, eso será para cualquier persona de la comunidad de diseño.

En el archivo de Figma quiero tener algunas pautas de contribución para los diseñadores que se incorporen y también dar algo de contexto a los desarrolladores sobre el proceso que siguen los diseñadores para crear diseños. Si más personas se unen al proyecto será importante tener flujos de trabajo para que las cosas no se desordenan.

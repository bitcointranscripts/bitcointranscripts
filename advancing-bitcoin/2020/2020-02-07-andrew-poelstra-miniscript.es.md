---
title: Miniscript Workshop
speakers:
  - Andrew Poelstra
date: 2020-02-07
transcript_by: Michael Folkson
translation_by: Blue Moon
tags:
  - miniscript
---
Página Web: https://bitcoin.sipa.be/miniscript/

Taller de reposición: https://github.com/apoelstra/miniscript-workshop

Transcripción de la presentación de Londres Bitcoin Devs Miniscript: https://btctranscripts.com/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/

# Parte 1

Así que lo que vamos a hacer, es un par de cosas. Vamos a ir a través del sitio web de Miniscript y aprender sobre cómo se construye Miniscript, cómo funciona el sistema de tipos, algunas de las reglas de antimaleabilidad. Luego vamos a ir a un repo que creé anoche, un repo Git con algunos programas de ejemplo. Vamos a tratar de recrearlos y tratar de modificarlos y aprender a usar la biblioteca rust-miniscript y algunas de las capacidades de la biblioteca. Vamos a encontrar algunos errores, vamos a encontrar un montón de limitaciones que podemos discutir y ver si la gente puede pensar en ideas alrededor de estas limitaciones. Algunas de ellas parecen ser intratables desde el punto de vista computacional, otras son dificultades de ingeniería, otras son cuestiones de la API. Con todo esto dicho, sería útil que todos tuvieran una cadena de herramientas de Rust instalada. Es muy rápido si estáis dispuestos a ejecutar este comando curl descargando un script de shell y pipeando eso en sh entonces podéis instalar Rust de esta manera.

P - ¿Hay una versión mínima porque acabo de obtenerla del repo?

R - Sí, la versión mínima es la 1.22 que salió hace como 2 años. 1.37 es suficiente.

Para un poco de antecedentes sobre la configuración de Rust antes de saltar a la cosa real y empezar a hablar de Miniscript. La biblioteca [rust-miniscript](https://github.com/apoelstra/rust-miniscript) es parte de la familia de bibliotecas [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin). Todas ellas tienen versiones mínimas de Rust bastante agresivas. Por agresivo quiero decir agresivo contra la comunidad de Rust, una versión mínima muy conservadora. Requieren la versión 1.22. La razón es que Carl (Dong) tiene una forma de Guix para construir 1.22 a partir de unos mínimos.. Guix. Podemos arrancar Rust 1.22 desde la cadena de herramientas en la que confiamos, mientras que si siempre estás rastreando la más reciente eso sería muy difícil. En general, la única manera de construir Rust 1.x es usar 1.x-1. Si subimos 15 versiones nuestro bootstrap determinista tendría que compilar 15... Esa es parte de la razón. Otra parte es simplemente tratar de ser consistente con lo que está en el repo de Debian y también ser conservador y no cambiar las cosas. Con todo esto dicho, cualquier versión de Rust que puedas obtener hoy funcionará con esto. Rust cambia bastante rápido pero no estamos usando... Hay un par de cosas que necesitamos. Una es que si quieres jugar con las cosas de Rust, aunque lo haré en la pantalla, es bueno agarrar el toolchain de [rustlang.org](https://www.rust-lang.org/learn/get-started). Las instrucciones para Linux son esta cosa de pipe sh. No sé cómo se hace en Mac o Windows, puede ser diferente. La otra cosa que probablemente querrán es este Git [repo](https://github.com/apoelstra/miniscript-workshop). No sé si podéis leer esa URL.

P - ¿Cuándo has hecho este repo? ¿Hace una hora?

R - El último commit fue hace una hora.

P - El commit inicial también fue hace una hora.

A - Lo que sea. Una parte la hice anoche. Sólo lo comprometí, sólo lo publiqué hace una hora, pero fue creado hace mucho tiempo.

Lo bueno de este repo es el README aquí abajo. Un par de enlaces útiles. El primero que quiero es el [sitio web de Miniscript](https://bitcoin.sipa.be/miniscript/). Está enlazado en el repo de Git, pero también es bastante fácil de memorizar. Permítanme dar una rápida visión general de lo que es Miniscript aunque supongo que hice una charla ayer y algunos de ustedes estuvieron en el [meetup](https://btctranscripts.com/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/)  de desarrolladores de Bitcoin el martes donde hice una cosa detallada de 2 horas. Básicamente lo que es Miniscript es un subconjunto de Bitcoin Script que podemos representar en esta bonita forma. Déjenme mostrarles un ejemplo.

`and_v(or_c(pk(B),or_c(pk(C),v:older(1000))),pk(A))`

En lugar de parecerse a Bitcoin Script. Bitcoin Script está basado en la pila, en el opcode y en un nivel muy bajo. Aquí estamos codificando las políticas de gasto en una forma de apariencia oscura. Lo que tenemos son diferentes comprobaciones de claves, comprobaciones de preimágenes de hash, timelocks y podemos combinarlos en varios ANDs y ORs y umbrales y así sucesivamente para componer políticas de gasto más expresivas. Puedes ver lo que está sucediendo. Tienes estos `pk` `pk` con las comprobaciones de firma de la pubkey. Tienes este AND que es un AND booleano y todo el resto del ruido, el `_v` el `v:` cosas así, esas reflejan el Script de Bitcoin subyacente que está siendo codificado aquí. Si hago clic en "Analizar" aquí se puede ver el actual Bitcoin Script que está representado por este Miniscript.

```
<B> OP_CHECKSIG OP_NOTIF
  <C> OP_CHECKSIG OP_NOTIF
    <e803> OP_CHECKSEQUENCEVERIFY OP_VERIFY
  OP_ENDIF
OP_ENDIF
<A> OP_CHECKSIG
```

Los beneficios de Miniscript sobre el uso del Script en bruto es que cuando tienes un programa estructurado de esta manera es muy fácil de analizar de muchas maneras diferentes. Es fácil, dado un Script arbitrario, averiguar cómo construir testigos para él. En general esto es un poco difícil. El Script de Bitcoin tiene un montón de opcodes. Cada opcode tiene requisitos para lo que va en la pila cuando lo ejecutas. Cuando compones un programa entero a partir de estos no puedes simplemente mirar el programa y decir "Para satisfacer este Script necesito proporcionar una firma aquí y una clave pública aquí y una preimagen de hash aquí. Necesito poner el número cero aquí" y así sucesivamente. Con Miniscript es muy fácil responder a este tipo de preguntas. Es muy fácil estimar el tamaño de los testigos si estás haciendo una estimación de tarifas para tu transacción. Es muy fácil hacer un montón de análisis semánticos en los que creo que también entraremos.

P - ¿A ese lo llaman Miniscript y el nivel superior es un lenguaje descriptor de políticas? Al menos para mí tengo cierta confusión sobre la terminología.

R - Esa es una buena pregunta. Esto que llamo Miniscript. Miniscript es básicamente una recodificación de Script. Si tienes esto, puedes llegar a aquello y viceversa. Hay diferentes formas de codificar lo mismo. Son bastante sencillas. Puedes escribir un parser para cualquiera de ellas y un serializador para cualquiera de ellas y se mapearán de un lado a otro. Hay una cosa separada llamada un lenguaje de políticas que vamos a entrar en un poco más tarde. El lenguaje de políticas es algo así.

`and(pk(A),or(pk(B),or(9@pk(C),older(1000))))`

Puedes ver que es muy similar a Miniscript con dos grandes diferencias. Una es que todo el ruido ha desaparecido. Ya no tengo `and_v` y diferentes tipos de ORs y ANDs. Ya no tengo todas estas envolturas y cosas. Sólo tengo ANDs y ORs, llaves pub, hashes y timelocks. La otra gran diferencia es que tengo pesos. Si tengo un OR en cualquier parte de una política tengo diferentes pesos que puedo asignar. Lo que este `9` significa, este OR es una clave pública o un bloqueo de tiempo de 1000 bloques, hay un `1` implícito aquí, el `9` significa que la rama izquierda es 9 veces más probable que la rama derecha. Aquí tenemos 90\% vamos a usar la rama izquierda, 10\% vamos a usar la rama derecha. La razón por la que hacemos esto es porque las políticas no son una cosa de Bitcoin, las políticas no se corresponden con el Script de Bitcoin, las políticas son cosas semánticas abstractas. Si queremos usar algo así en el blockchain tenemos que convertirlo a Miniscript. La forma de hacerlo es ejecutando un compilador al que también llegaremos si tenemos tiempo. Usted puede ver en el sitio web de Pieter aquí hay un compilador WebJS que ha compilado a partir de la C ++. Tomamos esta política aquí, este tipo de cosa abstracta, compilamos a Miniscript y puedes ver que tienes básicamente la misma cosa excepto que todo el ruido ha sido añadido. Hay opciones específicas de qué ruido añadir en qué lugares, lo que corresponde a opciones específicas de qué fragmentos de Script estamos usando. También puedes ver la probabilidad aquí. Bitcoin en sí mismo no tiene noción de probabilidades. Las monedas aparecen en el blockchain, se gastan una vez, ese es el hecho de la vida. Como James (Chiang) estaba diciendo que sólo tienes estas dos transiciones de estado, tal vez tres si se considera ... Una salida se crea, se confirma, se gasta. Eso es todo lo que sucede. No hay noción de probabilidades, ni siquiera hay una noción de ejecución, ni siquiera hay realmente un significado asignado a cualquier rama de Guión que no se tome. Así que todo esto es muy abstracto. Vamos a escribir algo de código y veremos más concretamente lo que significan este tipo de cosas.


P - Hay una [página](https://bitcoin.stackexchange.com/questions/91565/what-does-bitcoin-policy-language-offer-the-developer-that-miniscript-doesnt-w) de Bitcoin StackExchange que responde a esta pregunta. Sipa la responde y James y Sanket.

R - Escriba cualquiera de estas palabras clave en Google y encontrará esto.

Una última cosa que decir sobre las Políticas. Las políticas, en general, se crean cuando se trata de diseñar un guión. Escribes una política que representa las condiciones de gasto que te interesan. La pasas por el compilador, obtienes un Miniscript y luego te olvidas de que la Política ha existido. Al menos esa es la forma en que yo pienso en Miniscript. La Política es una cosa de fondo que se utiliza para que el compilador encuentre un Miniscript óptimo. Pero una vez que he hecho eso me quedo con el Miniscript y me olvido de que alguna vez vino de algo más abstracto. Ya veremos más adelante cuando quiera algo más abstracto es muy fácil de obtener. Puedo dejar de lado muchas de las cosas extra.

P - ¿Se puede verificar que un guión cumple una política?

R - Sí. Pieter no ha implementado esto así que el sitio web no lo tiene. Conceptualmente, lo que puedes hacer es tomar esto y todo lo que está después de un guión bajo o antes de dos puntos son envoltorios o especifican de alguna manera los fragmentos exactos de Script que se van a utilizar. Si los eliminas, lo que te quedará es exactamente lo mismo que esta Política, aunque los pesos no son... Los pesos no importan, por supuesto, por razones semánticas. Por supuesto.

En la biblioteca rust-miniscript, permíteme ir a la documentación de rust-miniscript [aquí](https://docs.rs/miniscript/0.12.0/miniscript/policy/trait.Liftable.html). Esta no es la descripción más legible de lo que sucede aquí. Si tienes un Miniscript de alguna forma puedes usar esta función Lift aquí, lo pasas por Lift y lo que sea que hayas empezado, ya sea un Miniscript o una Política o alguna otra representación de tu Script, lo pasas por aquí y obtienes este [objeto](https://docs.rs/miniscript/0.12.0/miniscript/policy/semantic/enum.Policy.html) llamado una Política Semántica, una Política abstracta que corresponde a un Miniscript. Son sólo los ANDs y ORs y los umbrales. Puedes estos son todos los diferentes componentes. Una Política abstracta, podría ser Insatisfiable, podría ser Trivial, esos corresponden con el Script OP_RETURN cero. Puede ser un hash pubkey, puede ser un timelock, puede ser un hash, un AND, OR o un umbral de cualquiera de esas cosas. No hay más que eso. Si en cambio voy al [tipo de Miniscript](https://docs.rs/miniscript/0.12.0/miniscript/policy/semantic/enum.Policy.html) si puedo encontrarlo. Esto es lo que es un Miniscript. Es una de estas cosas. Puedes ver que tienes `True`, `False`, `Pk`, `PkH`, timelocks y hashes por supuesto pero luego tienes todas estas cosas diferentes, `Alt` `Swap`, `Check`, `DupIf`, `Verify`, `Nonzero`, `ZeroNotEqual`. Todos estos son wrappers. Toman algún otro fragmento de Miniscript y ponen algo a su alrededor. Añaden como un OP_VERIFY al final, añaden un IF, ENDIF para que puedas saltarlo pasando el cero. Pueden poner un OP_SWAP delante para que puedas mover cosas fuera del camino. Puede que mueva algo a la pila altstack, ejecute el programa contenido y luego traiga algo de vuelta a la pila altstack. Cosas como esta que son importantes para la semántica del Bitcoin Script. Entonces tienes tus ANDs, ORs y umbrales. Puedes ver de nuevo que tienes muchos de estos. Tienes tres tipos de ANDs, cuatro tipos de Ors y dos tipos de umbrales.

P - Para que sirva de referencia, ¿cuáles de ellos se solapan directamente con los descriptores existentes?

R - Es una buena pregunta. La respuesta conceptual es que nada de esto se solapa con los descriptores. Tienen nombres similares.

P - ¿Parece que el umbral es exactamente lo que pasarías a `importmulti`? Y `PkH`

A - Un descriptor de tipo `pkh` significa que tiene el DUP HASH estándar sea cual sea el scriptPubKey y la firma estándar scriptSig. Eso es un pkh en los descriptores. Un PkH aquí se corresponde con un fragmento de Script. Es lo mismo que Script pero la cuestión es que en Miniscript el PkH es un Script. En un descriptor el pkh especifica donde va ese Script y donde va el testigo.

P - No. Sigue siendo un guión.

R - No es todavía un Script. Corresponde a la forma de poner el Script y el testigo en la transacción. Eso es todo lo que hace el Script. Vayamos al tipo de descriptor para separar lo que son estas cosas. Descriptor Miniscript, [aquí](https://docs.rs/miniscript/0.12.0/miniscript/descriptor/enum.Descriptor.html) es lo que es un descriptor. Un descriptor de salida, como Andrew (Chow) habló ayer, es un objeto que usarías en un monedero de Bitcoin para especificar cómo se usa realmente un Script en la blockchain. Hay un montón de diferentes tipos de descriptores que nos interesan. Permítanme repasar los más importantes. Hay `Pkh` y `Wpkh`. El `Pkh` es la dirección estándar de 1, donde tienes un hash de la clave pública en tu scriptPubKey y luego para gastar las monedas revelas la clave pública, revelas la firma en tu scriptSig y te vas a las carreras. El `Wpkh` es el equivalente de SegWit donde tienes un programa testigo que es un cero seguido de un hash de 20 bytes de la pubkey y luego el único testigo requerido es la firma. Puedes tener `Sh` aquí es pay-to-script-hash. `Wsh` es pay-to-witness-script-hash. De nuevo P2SH a las 3 direcciones y luego está P2WSH que es el programa estándar de SegWit donde tienes un hash de programa, un cero seguido de tu hash de programa y tu testigo va en tu campo de testigo. Cuando usas Bitcoin hoy en día, los únicos dos descriptores que te importan son WPKH, que se usa para una cartera normal que tiene claves y gastas usando las claves, o puedes usar WSH, que es cuando tienes algún script complicado y quieres usar SegWit. También tenemos P2SH envuelto WSH que podría utilizar por razones de compatibilidad con los servicios más antiguos o P2SH si está ejecutando un servicio antiguo.

P - Se puede hacer WSH - PKH en los descriptores. Eso está permitido y hay una prueba para ello. ¿Bajo esta definición eso no es un Miniscript?

A - Interesante. Según esta definición, el PKH será el Miniscript y el WSH wrapper sería el descriptor.

P - Eso se puede hacer literalmente en los descriptores ahora mismo.

R - Yo diría que, en la medida en que se puede hacer, ya se ha introducido parte de Miniscript en los descriptores.

P - ¿Acaba de afirmar que PKH no es un Miniscript?

R - Estoy diciendo que el `pkh` aquí y el `PkH` en el Miniscript son diferentes aquí. Pero realmente creo que estamos causando una confusión semántica al tener esta discusión ahora mismo. Podemos discutir fuera de línea.

Permítanme decir una última cosa. En uno o dos años, cuando Miniscript esté totalmente implementado en el Core, vamos a pensar que Miniscript es un subconjunto de los descriptores. Los descriptores describen todo lo que necesitas saber para poder gastar una salida de Bitcoin. Te dice si es P2SH, si es un testigo-script-hash, lo que sea. También describirá en el futuro cuál es el Script real y cómo satisfacerlo. ¿Tiene una clave pública, tiene muchas, tiene timelocks, lo que sea? Lo que Miniscript es un subconjunto de estos descriptores que codifican la semántica del Script. Ahora mismo hay una cosa en el Core llamada descriptores que tiene un par de cosas específicas de Miniscript pero no mucho más. En el futuro tendremos todo Miniscript en él.

P - ¿Es esta una forma de pensar en esto? Piense en los descriptores como en un lenguaje de alto nivel, como Java. Tienes tu código de bytes intermedio con Miniscript y luego tu código máquina real, el propio descriptor. ¿Crees que es justo o no?

R - Yo diría que es injusto. Utilizando esta analogía, Miniscript se corresponde con el código de bytes y la parte del descriptor se correspondería con la cabecera de tu programa Java, la versión de tu JVM, algo así, que establece cualquier bandera que necesites para ejecutarlo. Los descriptores incluyen un montón de cosas que no forman parte de Miniscript. Cosas como P2SH. Miniscript no tiene noción de P2SH porque sólo se trata de Scripts de Bitcoin.

P - Creo que una mejor manera de pensar en esto es que los descriptores describen el scriptPubKey y el Miniscript describe su script de redención o script testigo. La separación es que su Miniscript va en la entrada, sus descriptores van en las salidas.

R - Me gusta, es una distinción muy práctica que sirve para cualquier cosa que hagas en la vida real. Pero...

P - Se puede utilizar Miniscript en scriptPubKeys pero, ¿por qué?

P - Los descriptores incorporan más la lógica de validación y el motor de scripts en torno a ella mientras que Miniscript es directamente...

R - Sí. rust-miniscript soporta poner Miniscripts directamente en el scriptPubKey usándolo como un descriptor de tipo desnudo pero realmente nunca deberías hacer eso. Esto existe principalmente para poder escribir pruebas y no tener que envolver con WSH todas mis cosas todo el tiempo. También a veces abuso de Miniscript en otros contextos en Liquid y es útil tener ese tipo desnudo para no tener que llegar a través del Bitcoin...

Espero que esa discusión entre Miniscript y los descriptores haya sido más ilustrativa que no. Me gusta lo que ha dicho Andrew de que tu descriptor describe lo que va en la salida. ¿Cómo señalas al verificador de Bitcoin dónde está tu Miniscript y cómo está codificado? El Miniscript va en su entrada. El Miniscript del programa real. Así que vamos a tratar de hacer esto un poco más práctico. Voy a cambiar a la página de GitHub a menos que ¿hay preguntas?

P - Una cosa que me confundió ayer fue que Andrew Chow dijo que los descriptores describen todo lo necesario para resolverlos. Eso sonaba a analizabilidad, ¿que pertenece más al ámbito de los miniscriptores que al de los descriptores?

R - La razón por la que tenemos una distinción es que los descriptores están implementados en Core, hay un PR para los descriptores. Incluye la mayor parte de Miniscript, no incluye los diferentes ORs y ANDs, no incluye el complicado umbral, no incluye timelocks, no incluye preimágenes de hash. Literalmente sólo incluye pubkeys y pubkey hashes. El punto de los descriptores implementados de esa manera, como Andrew habló en su charla, es limpiar el modelo actual de billetera de Bitcoin, que ahora mismo es incoherente. Tienes las claves de curva elíptica y básicamente cualquier forma plausible de usar esa clave de curva elíptica en Bitcoin Core ahora mismo sólo reconocerá eso como algo que controla. Lo que hace que la interoperabilidad con Core sea muy difícil. Si intentas escribir un monedero que utilice el RPC de Core, o bien tienes que ir a por todas o no puedes. Por ejemplo, si genero una pubkey y te doy una dirección Bitcoin heredada, un 1 cualquiera. Y tomas el hash de la pubkey de esa dirección y luego lo pones en una salida WPKH. Lo cambias de una salida de hash de pubkey a una salida de hash de pubkey de testigo y ahora tienes una dirección bech32. Usted puede enviar dinero a esa dirección y mi cartera Core lo reconocerá a pesar de que la dirección que generé era una dirección de legado. ¿Tiene eso sentido? Lo que significa que si estás escribiendo un software que envuelve el monedero Core y piensas "voy a comprobar las monedas que van a mis direcciones y Core sabrá exactamente el dinero enviado a la dirección que generé" estarás equivocado porque Core reconocerá el dinero enviado a otras direcciones no relacionadas. O bien tienes que implementar este daño cerebral tú mismo en tu propio código o puedes utilizar una versión futura de Core que utilice descriptores en los que realmente lleve la cuenta de qué direcciones se crean y de qué manera.

P: Una cosa es que los descriptores fueron una idea que tuvo Pieter originalmente y de la que surgió Miniscript, así que la distinción entre ellos no es muy fuerte. Están muy relacionados.

R - No hubo mucho tiempo entre estos.

P - Fueron como 20 horas. Un día me habló en su despacho sobre descriptores y al día siguiente... y de ahí surgió Miniscript.

R - Pensé que había al menos una semana. Un poco de historia. Los descriptores de salida son una idea de Pieter Wuille para limpiar el desorden del monedero Core. Se le ocurrió esta idea, escribió un gist, estaba hablando de ello en la lista de correo de Bitcoin dev. Una semana o dos o posiblemente 20 horas más tarde volé a Mountainview para ir a visitarle a la oficina de Blockstream y le dije "estoy intentando hacer algunas cosas generales de descriptores de Bitcoin".

P - Usted estaba tratando de finalizar un PSBT sin implementar...

R - Así es. Carl Dong ha implementado PSBT en rust-bitcoin. Está intentando añadir código de propósito especial para CHECKMULTISIG para poder hacer estos tipos de PSBT de CHECKMULTISIG. Yo tomé esto, dije "No quiero estas plantillas específicas de Script aquí. Esta no es una biblioteca de propósito especial para cada cosa específica que se le ocurra a Carl. Esta es una biblioteca genérica de Bitcoin. Fui a Pieter y le dije "Necesito una manera de modelar generalmente Bitcoin Script". Y él dijo "¿Y si ampliamos los descriptores para añadir MULTISIGs y ANDs y ORs y timelocks y hash preimages?" Así que originalmente Miniscript era sólo una extensión de los descriptores. Pero lo que ocurrió fue que Miniscript se convirtió en un gran proyecto de investigación que sobrevivió por sí mismo. La distinción es una distinción práctica en este momento que refleja que se trata de proyectos diferentes que se desarrollan en momentos diferentes. Pero están diseñados para trabajar juntos y para complementarse mutuamente de manera que no hay una separación clara. De ahí viene realmente toda esta confusión.

P - ¿Entonces todo es culpa de Pieter?

R - Todo es culpa de Pieter, allá vamos. No, la culpa es en gran parte de Satoshi, como siempre.

P - El monedero era simple de Satoshi porque era sólo pubkeys en bruto. Alguien decidió hacer un hash de las pubkeys y añadir SegWit.

P - Ese fue el error.

R - El daño cerebral original y peor es que hace mucho tiempo había lo que se llama una salida de pubkey desnuda donde tu scriptPubKey sólo contenía una clave pública y el operador scriptSig. Tu scriptSig tenía que tener una firma y luego cuando verificabas eso, firma, clave pública, CHECKSIG. Entonces alguien, creo que fue Satoshi, se dio cuenta de que si hacemos un hash de 20 bytes de la clave pública. Ahora tu salida es tomar ese hash de 20 bytes, hacer un hash de lo que sea que esté en la pila, que mejor que sea una clave pública, y comprobar que la clave pública en la pila tiene un hash específico. Entonces haz el CHECKSIG. Ahora cuando creas una salida todo lo que tienes es este hash de la clave pública en lugar de una clave pública completa, así que te ahorras unos 10 bytes y luego cuando gastas las monedas tienes que revelar la clave pública y luego tienes que revelar una firma. Así que el gasto es un poco más caro.

P - Cuando esto se conoció originalmente tenías pubkeys sin comprimir, así que te ahorras unos 40 y pico bytes.

R - Un error aún más antiguo de Satoshi fue permitir que OpenSSL analizara las claves públicas sin restringirlas de ninguna manera. Teníamos estas cosas llamadas pubkeys sin comprimir. Curiosamente, originalmente nadie sabía de las claves públicas comprimidas, alguien las encontró en la documentación de OpenSSL y fueron como ....

P - ¿Nadie en Bitcoin o...?

R - Nadie en Bitcoin. Alguien dijo "Mira esta bandera. ¿Y si usamos esta bandera?"

P - ¿Se puede seguir pagando a una pubkey sin comprimir?

R - Sí y Core lo reconocerá. Aquí es donde las cosas se ponen realmente mal. Si le preguntas a Core qué dirección corresponde a eso te dará una dirección.

P - Ya no.

R - Le dará una dirección de legado que corresponde con esa clave pública, pero luego si intenta compartirla con alguien, hará lo del hash de la pubkey. El núcleo irá de una clave pública a una dirección de vuelta a un scriptPubKey y hace un viaje de ida y vuelta.

P - ¿Qué quiere decir con viaje de ida y vuelta?

R - Me refiero a que si empiezas con una scriptPubKey que es una pubkey desnuda, obtienes una dirección a partir de ella haciendo `listunspent` o lo que sea y luego intentas recuperar una scriptPubKey a partir de esa dirección, obtendrás una scriptPubKey diferente. Literalmente estás produciendo una dirección que todos los demás interpretarán como correspondiente a una scriptPubKey diferente. Esto está accidentalmente bien porque a Core no le importan las scriptPubKeys.

P - ¿El monedero Core probará ambas cosas?

A - El núcleo reúne todas las scriptPubKeys en una nube de nebulosa y vaga Bitcoin en su cabeza. Parecerá que funciona. Si usted está tratando de escribir bibliotecas o software serio que utiliza estas cosas y necesita ser preciso acerca de sus scriptPubKeys, a dónde van las monedas y de dónde vienen las monedas es muy difícil de reproducir.

P - Es muy difícil de razonar. En lugar de limitarse a actualizar la cartera, decidimos meter esa antigua funcionalidad en una caja que Andrew hizo y luego construir una nueva al lado.

P - Es una caja donde el material heredado puede ir a morir.

P - O vivir para siempre.

R - En 2020 tendremos monederos con descriptor que se comportan como esperas que se comporte un monedero de Bitcoin. En 2019 tuve un monedero descriptor. Había mucho papeleo mental manual. No debería decir que tenía software. Usaba descriptores.

P - Yo también usaba descriptores en 2019.

Gran parte de la confusión aquí corresponde a la confusión histórica y a los accidentes que se produjeron en el diseño del monedero de Bitcoin Core que, a su vez, fueron la única fuente de los formatos de dirección y los formatos de intercambio que utilizamos hoy en día. Así que los descriptores limpian esto y hacen una separación mucho más clara. Y luego Miniscript surgió de los descriptores, Pieter y yo estábamos haciendo cosas muy similares que se cruzaron. Puedes pensar en Miniscript como una forma de ampliar los descriptores para no sólo separar claramente los diferentes tipos de direcciones, sino que también podemos utilizarlos para separar políticas completamente diferentes. De repente tenemos esta capacidad de pensar en multisig y timelocks y todas estas cosas. Y los descriptores nos dan un gran marco para ello. Ampliamos el marco de los descriptores, pasando de distinguir entre tipos de direcciones a distinguir entre tipos de programas. Eso es lo que es Miniscript. Pero entonces Miniscript se convirtió en algo mucho más grande porque al implementar esto, como hablé en mi charla de ayer, nos dimos cuenta de que había mucha comprobación de cordura y mucho análisis que queríamos hacer en los Scripts. Una vez que podemos soportar cosas de aspecto arbitrario de Script nos dimos cuenta de que hay un montón de errores que es posible hacer. Vamos a entrar en eso un poco en los próximos diez o quince minutos.

# Taller

Empecemos con algunas cosas del taller. En mi Git repo [aquí](https://github.com/apoelstra/miniscript-workshop) tengo algo de código fuente. Vamos a seguir adelante y abrir algunas fuentes.

`vim src/01-intro.rs`

[Aquí](https://github.com/apoelstra/miniscript-workshop/blob/master/src/01-intro.rs) es un programa simple que escribí para demostrar el uso de la biblioteca rust-miniscript. Estamos usando Rust 2018 aquí, alguien preguntó sobre la versión mínima de Rust. Todos pueden clonar este repo. Pueden ver que tengo un montón de binarios que corresponden a las diferentes cosas que vamos a hacer. Las dependencias de las que dependo son la versión 0.12 de Miniscript crate que es la última versión de Miniscript. Para los que no conocen Rust tengo el descriptor Miniscript. El rasgo Miniscript utiliza un tipo de descriptor. Los descriptores en rust-miniscript están parametrizados por el tipo de clave pública. Voy a demostrar lo que quiero decir con eso en un segundo. Voy a decir que quiero usar la clave pública normal de Bitcoin. Un poco de rareza que es específica de Rust.

`miniscript::bitcoin::PublicKey`

Lo que estoy haciendo aquí es que tengo esta biblioteca Miniscript, se llama un crate en la metodología de Rust. La caja Miniscript depende de la caja rust-bitcoin. El crate de Miniscript en realidad reexporta el crate de Bitcoin del que depende. Si quiero usar el crate de Bitcoin puedo depender de él o puedo usar el reexportado desde Miniscript. La razón por la que hago esto es para que cuando Miniscript cambie su versión de dependencia de Bitcoin y no me apetezca hacerlo, todo mi código que funcionaba con Miniscript simplemente hará lo correcto. Así que puedes imaginar que tengo mis propias cosas específicas de Bitcoin flotando por ahí. Realmente no me importa qué versión de rust-bitcoin estoy usando, hay nuevas versiones que salen cada vez que me apetece y normalmente están actualizando cosas que a otras personas les importan y a mí no. La forma más fácil de asegurarme de que siempre estoy usando la versión compatible con Miniscript es simplemente usar la exportación. Es un truco muy útil. Aquí hay un descriptor. Incluso es un `wshpk` que es lo más confuso que podría haber elegido.

P - Una pubkey sin comprimir, ¿no está permitida en SegWit? No es estándar en SegWit.

P - En realidad no compila, lo que has hecho ahora. Arroja un error de clave pública inválida.

A - Déjame ir a arreglar esto. Estaba tratando de demostrar algo tonto. Aunque si pusiera una pubkey válida sin comprimir, funcionaría aunque eso es ilegal en SegWit. Eso es un error en rust-miniscript. Déjame archivar rápidamente ese bug. Creo que esto es instructivo. Puedo esperar hasta el descanso para archivar los errores, pero creo que vamos a encontrar un montón de pequeñas cosas como esta.

He arreglado mi descriptor aquí. ¿Qué está pasando aquí? Tengo un descriptor. En mi modelo mental la parte `wsh` es el descriptor que dice que este programa lo quiero hacer hash y lanzarlo a una salida SegWit. La parte `pk` es en realidad el programa. Tengo el `pk` y luego tengo el `020202...`, que es la clave más fácil de recordar que es una clave EC válida. Paso esto a un descriptor y luego aquí voy a calcular la `script_pubkey`. Aquellos de ustedes que están familiarizados con Script probablemente pueden leer esto. Estoy empujando un byte cero y luego estoy empujando hex 20 que es 32, ¿por qué estoy empujando 20? WSH, gracias. Estoy empujando 20, 32 bytes y eso es sólo un hash de todas estas cosas.

P - ¿Por qué se hace WSH de una clave pública?

R - Porque esto era lo más sencillo. Quería algo que cupiera en una línea. Vamos a cambiarlo. Primero vamos a ejecutar este programa para que todas mis afirmaciones funcionen. Entonces podemos cambiarlo y veremos qué pasa.

P - WPKH sería más obvio.

R - WPKH no tiene Miniscript.

P - Podrías hacer WSH - PKH.

R - Podría. Deja que lo repase. Luego lo cambiaremos para que sea más sensato.

El scriptPubKey que como puedes ver es solo un programa testigo de SegWit. Usted tiene cero que es una versión SegWit y luego un hash de 32 bytes. También puedo calcular el script testigo aquí. Aquí está el programa testigo real. Esto está empujando 21 que es el hexágono 33 y luego 33 bytes que usted puede ver visualmente es la clave pública. Entonces hay dos maneras diferentes en que podemos imprimir esto. Para aquellos familiarizados con Rust reconocerán estas como el rasgo de visualización y el rasgo de depuración. Si imprimo algo que está usando las llaves rizadas eso dará una representación legible para el usuario. Si lo imprimo usando la llave con el signo de interrogación que imprime la salida de depuración que se supone que tiene toda la información que un programador necesitaría para ver lo que está en el... Déjame correr esto.

`cargo run —bin intro`

cargo: comando no encontrado. ¿Cómo puede ser eso?

`vim ~/ .bashrc`

Comprobemos el PATH.

`echo $PATH\`

Ese es el problema.

`export PATH=“$HOME/ .cargo/bin:$HOME/bin:$PATH”`

Déjame ejecutar el programa.

`cargo run —bin intro`

Esta primera línea está imprimiendo la representación legible para el usuario. Puedes ver que es idéntica a la que hemos analizado inicialmente. En la representación de depuración hay muchas más cosas interesantes. Un par de cosas. La parte de PublicKey, esto es de rust-bitcoin. Sólo dice que es la clave comprimida, la clave real de la CE subyacente es esta cosa gigante, que es una representación sin comprimir, ni siquiera es la estándar. La salida de depuración es lo más fácil de implementar. Lo que es interesante es esta cosa, esta `K/onduesm`. Hay un pequeño problema, déjame arreglar esto. Déjame ilustrar el problema primero. ¿Qué significa esto? Primero la K. La K es lo importante aquí. Esto me dice qué tipo tiene este Miniscript. Hay cuatro clases de tipos en Miniscript. Volvamos al [sitio web](http://bitcoin.sipa.be/miniscript/). B, V, K y W, lo que representan, los llamamos tipos, lo que efectivamente representan es llamar a las convenciones. La más importante es B, la base. Lo que un Miniscript B es un Script donde si lo satisfaces tomará sus entradas, las sacará de la pila y dejará un 1 en la pila si lo satisfaces. Si no lo satisfaces, dejará un 0 en la pila o posiblemente abortará el Script pero no hará nada más. No va a dejar que el Script continúe sin poner nada en la pila. Hay una regla en Miniscript que es que el Script de nivel superior tiene que ser una B. Un Miniscript que se pone en la blockchain tiene que ser una B. Puede contener subexpresiones y cosas y esas no son necesariamente B, esas pueden ser V o K o W. Las K son fragmentos que dejan una clave en la pila. Tenemos este tipo porque hay muchos contextos donde usamos llaves en Miniscript. Las usamos en el contexto CHECKSIG, lo usamos en MULTISIG, CHECKSIGVERIFY y así sucesivamente. Curiosamente también podemos usarlas en ORs. Voy a dar un ejemplo de tal Script. Permítanme describir rápidamente y luego volveremos. Supongamos que tengo dos claves públicas y quiero permitir una firma con una u otra pubkey. Una forma de hacerlo es utilizando el IF opcode. Hago IF PUBKEY CHECKSIG ELSE OTHER_PUBKEY CHECKSIG ENDIF. Esto es un desperdicio, estoy desperdiciando un byte aquí. Lo que puedo hacer en su lugar es IF PUBKEY ELSE OTHER_PUBKEY ENDIF y luego poner el CHECKSIG en el exterior. El uso de este tipo K en Miniscript nos permite hacer eso. Puedo tener una sentencia IF que es como un `or_i` puedes ver que este fragmento es un "IF X ELSE Z" y nuestras reglas dicen que si tenemos una sentencia IF como esta donde tanto X como Z son Ks entonces toda la expresión es en sí misma una K. Si ambas dejan una K en la pila entonces toda la cosa dejará una K en la pila. Ahora puedo tomar `or_i` y envolverlo en un CHECKSIG y ahora he compartido un CHECKSIG entre dos ramas. Este es el tipo de optimizaciones que permite Miniscript. Volviendo al código aquí puedes ver que tenemos un problema porque este Script de nivel superior aquí no es una B es una K. Eso es un error. Este [uno](https://github.com/apoelstra/rust-miniscript/issues/71) lo presenté anoche, hace 17 horas. La comprobación del nivel superior debe ser B ocurre en el Miniscript, no ocurre en el Descriptor. Eso es un error. ¿Qué pasa con este `onduesm`? Estos son objetos interesantes. Son básicamente modificadores de tipo. K es un tipo base, K significa que deja una K en la pila. También tenemos un montón de otras propiedades sobre este pk que son interesantes. Cada una de estas letras es una individual. Voy a destacar un par de ellas y luego volveré. La primera es `o`. Esta expresión siempre consume exactamente 1 elemento de la pila. ¿Por qué es una `o`? Porque consumen una firma. Una clave pública en Miniscript siempre consume una firma que es exactamente un elemento de la pila. En Miniscript realmente represento ese hecho, algunos fragmentos toman un elemento de pila, otros toman cero o dos o más. Hay casos en los que esto es importante. Permítanme bajar a dar un ejemplo donde esto es útil. No hay un ejemplo sencillo. Donde esto es útil es donde uso OP_SWAP aquí. Permítanme ir a un fragmento de tipo diferente que puedo justificar más fácilmente. `n` es distinto de cero, este es uno genial. Siempre consume al menos un elemento de la pila que no sea cero cuando estás satisfaciendo un Script. En Bitcoin puede dar cero en lugar de una firma que es sólo la cadena vacía y esto es siempre una firma inválida. Esto nunca puede ser analizado como una firma. Si quieres no proporcionar una firma por alguna razón, tal vez estás haciendo un 2 de 3 y la tercera comprobación de firma no la necesitas, puedes simplemente proporcionar una cadena vacía. Hay algunos fragmentos en los que puedes satisfacerlos dándoles un cero y otros en los que no. Una comprobación de clave pública es una en la que no puedes, así que tenemos el modificador de tipo `n`. Donde esto es útil, creo que el más genial es esta envoltura `j`. Supongamos que tengo un fragmento `x` aquí que nunca será satisfecho por un cero. Y supongamos que `x` es complicado, podría ser imposible de insatisfacer o podría requerir un montón de PUSHs para insatisfacer. Quiero hacer esto más simple, quiero cambiar esto para que pueda insatisfacerlo pasando un cero. Tengo un fragmento que no puede ser satisfecho por una entrada cero y quiero envolverlo de tal manera que tenga la propiedad adicional de que un cero lo insatisfaga pero no haga nada más. Puedo hacer esto con este fragmento de script. Puedo elegir `SIZE 0NOTEQUAL IF [X] ENDIF`. Lo que esto hace es mirar la entrada, si la entrada es cero comprobará esto, dirá ¿cuál es el tamaño? El tamaño es cero. Se ejecutará `0NOTEQUAL`. ¿Por qué hacemos esto? Aquí hay una pregunta divertida para quien fuera que mi [dos horas de despotricar](https://btctranscripts.com/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/) sobre Script el otro día. ¿Por qué no puedo simplemente usar el opcode IF aquí y decir "Si le das un cero entonces no lo ejecutes. Si le das algo distinto de cero entonces sí lo ejecutas"?

P - Comprobación de maleabilidad, ¿correcto?

R - Sí, en realidad hay dos razones. Una es la comprobación de la maleabilidad. En realidad, hay muchas cosas que se pueden dar al IF que tendrán éxito o no. Esto es ambos lados de la comprobación de maleabilidad. Las reglas de consenso no limitan lo que se pone en un IF. Si se supone que hay que poner un cero, un tercero podría, en principio, reemplazar ese cero con `0000000` o algo así, y eso pasaría. En realidad, hay reglas de normalización contra eso. Hay una regla llamada MINIMALIF que impide que eso ocurra. Supongamos que acabo de hacer IF y tenemos esta regla MINIMALIF que prometemos cumplir. Si pongo algo que es distinto de cero o 1 en un IF... sé que está tratando de propagarse. El punto de esta construcción es que en el caso de que esté dando una salida no nula quiero pasar eso a mi fragmento `X`. Imagina que `X` está comprobando una firma o algo así. Si sólo hiciera IF X ENDIF y tratara de poner una firma allí ¿qué va a pasar? La firma no es 1. 1 tampoco es una firma válida. La regla MINIMALIF va a desencadenar donde usted está tratando de encender una firma, este es un vector de maleabilidad que es hay muchas firmas diferentes, y se niegan a propagar. En su lugar, tenemos que traducir de alguna manera nuestra entrada en algo cero o uno antes de poner este IF. ¿Tiene esto sentido?

P - ¿Para asegurarse de que se puede componer con otro fragmento de Script?

R - Sí. Más sencillo aún que estar compuesto como un fragmento de Script es que pueda utilizarlo cuando le dé una entrada no nula que no sea exactamente uno.

¿Cómo podríamos hacerlo? ¿Cómo convertir algo que podría ser falso o verdadero y conseguir que sea exactamente cero o uno? Hay un par de maneras diferentes y todas se rompen de diferentes maneras. Una forma es ejecutar directamente 0NOTEQUAL. Déjame sacar mi lista de opcode en rust-bitcoin [aquí](https://github.com/rust-bitcoin/rust-bitcoin/blob/master/src/blockdata/opcodes.rs). Desplázate hasta 0NOTEQUAL. Esto parece hacer exactamente lo que quiero. Mapear cero a cero y mapear todo lo demás a uno. Entonces, ¿por qué tengo este SIZE 0NOTEQUAL? ¿Alguna conjetura? 0NOTEQUAL es un opcode numérico. Fallará si le pasas algo más grande que 4 bytes. Por eso no podemos usar 0NOTEQUAL. Así que de alguna manera necesitamos otro mapeo que mapee cero a cero y mapee cualquier otra cosa que sea menor a 4 bytes de tamaño. Resulta que OP_SIZE que le dará el tamaño de un elemento de la pila hará exactamente lo correcto.

P - ¿Entonces OP_SIZE dirá que el tamaño de un cero es cero?

R - Sí, porque el cero en Bitcoin es la cadena vacía.

P - Uno de esos ceros en una cadena vacía. Puede tener otros ceros.

R - Bien, eso nos lleva a la segunda cuestión. Supongamos que estuviera haciendo algo más inteligente e intentara utilizar 0NOTEQUAL. Imagina que no tuviéramos este límite. En realidad hay muchas cosas que no son la cadena vacía y que de hecho son cero. Entonces estaría introduciendo un vector de maleabilidad porque a diferencia de IF que tiene una regla MINIMALIF que me limita todos mis otros opcodes no tienen tal cosa. En cuanto haga esta conversión, estaré introduciendo un vector de maleabilidad. Necesito de alguna manera hacerla cumplir para que sólo haya una cosa que dispare el cero y haga que se salte la sentencia IF. Quiero que esto sea exactamente la cadena vacía. SIZE 0NOTEQUAL realmente hará esto.

P - El cero negativo no es...

A - Correcto. El cero negativo canónico es el hex 80. El tamaño del cero negativo será uno para el cero negativo canónico.

Otra cosa que puedes probar es OP_NOT OP_NOT en una fila. Tienes el mismo problema, hay un vector de maleabilidad ahí. Creo que OP_NOT es un operador booleano no un operador numérico pero tendría que comprobar el código. Creo que hay un par de ideas más pero SIZE 0NOTEQUAL es la que no es un vector de maleabilidad. Esto resalta el beneficio de tener Miniscript. Si estuvieras tratando de hacer cosas geniales con Script este es el tipo de cosa que se te podría ocurrir independientemente. En realidad lo hizo, teníamos esto como parte de un fragmento más grande antes de que nos diéramos cuenta de que podíamos generalizarlo a esta envoltura j.

P - ¿No es tan numérico?

R - Si intentáramos usar NOT también fallaría.

P - ¿Qué significa la j?

R - Probablemente sea uno de los seis idiomas de Pieter. En este punto nos quedamos sin letras.

P - O es una broma o...

A - Pieter podría tener una respuesta para ti pero estábamos empezando a quedarnos sin letras. Puedes ver que la a es ALTSTACK, la s es SWAP, la c es CHECKSIG, la v es VERIFY, la t es TRUE. Todas tienen sentido, ¿es esta la única que no tiene sentido?

P - ¿Joker?

R - Esto es probable e improbable. Ya teníamos n para esta forma de no-cero. La envoltura n cambia la salida de algo que podría ser cero o podría ser un galimatías a algo que es exactamente cero o uno. La envoltura j cambia la entrada de la misma manera. Ambos son distintos de cero, así que creo que tomamos una letra al azar.

P - ¿Sólo cero?

R - Sólo cero, sólo uno.

Este es el tipo de cosas que se te pueden ocurrir de forma natural cuando intentas diseñar Scripts a mano. Tal vez se dé cuenta de los problemas de maleabilidad y de los problemas de límites numéricos que acabo de mencionar una o dos veces. No lo vas a notar cada vez. Hay miles de cosas estúpidas en Script que te encuentras en rincones extraños y oscuros. Lo bueno de Miniscript es que tenemos 38 fragmentos, esta lista baja. Compruebas que 38 cosas son sensatas. La mayoría de ellas son realmente obvias. Puedes ver que si pones un uno ahí, ¿eso va a provocar que haya un uno en la pila? Sí. Sólo unas pocas requieren una reflexión profunda. Podemos pasar todo el tiempo razonando sobre estos fragmentos. Una vez que hayamos confirmado que los 38 fragmentos tienen... entonces somos oro. Lo último que quería decir. Todo esto comenzó con este fragmento de tipo, esta propiedad de tipo aquí, el n no cero. Puedes imaginarte tratando de hacer esta envoltura, pero imagina que X podría realmente tomar una entrada cero y tener éxito. Hay algunos fragmentos en los que esto es cierto. En particular cualquier cosa que utilice un NOTIF pero creo que podríamos haber eliminado esos. Creo que las preimágenes de hash, podría tener un hash de cero. Hay algunos ejemplos de cosas que tomarán cero para ser satisfechas pero creo que son todos un poco complicados. Si pongo esto aquí, de repente estoy en problemas. Tengo esta cosa X que estoy tratando de ejecutar. Le doy cero con la esperanza de satisfacerla pero entonces la comprobación de SIZE 0NOTEQUAL IF la atrapa..... Hay otra cosa extra que hace SIZE que es duplicarlo. Mi cero original en la pila no se consume. Mi cero se copia en otro cero, 0NOTEQUAL realmente lo convierte en un cero. IF lo consume y el cero original sigue adelante. Todo este fragmento si lo insatisfacemos dejará el cero en la pila lo que significa que es una B y también una e y algunas otras cosas. Si yo tratara de satisfacer a X dándole cero no funcionaría. Habría desvirtuado mi Script, ya no sería correcto.

P - Es un comentario realmente interesante en el diseño de Miniscript. ¿Tiene algún principio de diseño acerca de dejar la pila en el mismo estado que la subexpresión original antes de que la subexpresión fuera ejecutada? SIZE aquí está modificando la pila, está empujando dos ceros en la pila. Es de suponer que si se ejecuta todo esto seguirá habiendo un cero en la pila. Eso me parece raro en el sentido de que hay estas operaciones internas en la subexpresión y todavía estás dejando la pila sucia sin dejar a propósito un CHECKSIG o algo así para fallar.

A - Esta intuición es la que recogen las B, V, K y W. Estos cuatro tipos base reflejan de qué manera concreta ensuciamos la pila con estas operaciones. Sólo nos permitimos cuatro formas diferentes que fueron suficientes para nuestros propósitos. Eso es lo que significa el tipo base. Por eso son los tipos base ya que eso es lo más importante, es cómo ensucian la pila porque eso afecta a la forma en que se pueden contabilizar. Todo lo demás son modificadores para que las cosas sigan siendo semánticamente correctas.

Ya está. Para eso es la propiedad de tipo no cero. Indica que esto es algo que puedo envolver en una j. Hay razones de eficiencia por las que querría envolver cosas en j o incluso razones de corrección. Así es como funciona j. Hay un montón de cosas que entraron en el diseño de j, algunos sorprendentes maleabilidad y cosas numéricas. Creo que nos detendremos aquí para el descanso.

DESCANSO

# Parte 2

[Aquí](https://github.com/apoelstra/miniscript-workshop/blob/master/src/01-intro.rs) es el código que hicimos antes de la pausa. Como John señala el scriptPubKey que estoy afirmando aquí le falta un CHECKSIG. ¿Por qué? La razón es que tenemos esta envoltura c aquí. Que toma un fragmento de tipo K y lo convierte en un fragmento de tipo B. Lo hace metiendo un OP_CHECKSIG al final del mismo que toma una clave y una firma y lo convierte en un... Ahora si vuelvo a ejecutar esto.

`cargo run —bin intro`

Vamos a ver que esta aserción aquí va a fallar y vamos a ver la razón por la que falló es que un OP_CHECKSIG aparecerá al final aquí. Ahí está nuestro `ac`. Vamos a arreglar la aserción y luego veremos en la parte inferior, nuestro comprobador de tipos aquí, que K se ha convertido en una B. Puedes ver nuestra cosa original esta `K/onduesm` y luego al poner la envoltura c en ella cambiamos el tipo. Una cosa más que voy a mostrar en esto antes de pasar al siguiente ejemplo. Supongamos que cambio esa c para que sea también una v, v se verifica. Miniscript es lo suficientemente inteligente como para saber si tienes un CHECKSIG seguido de VERIFY para convertirlo en CHECKSIGVERIFY. CHECKSIGVERIFY creo que es una v. Tengo la envoltura v en la envoltura c. Mi cosa original era una K que emite una clave, la envoltura c la convierte en una B y la envoltura v la convierte en una V. OP_VERIFY toma un cero o un uno y lo convierte en un abortar o un continuar.

P - ¿Esto no es un Miniscript válido?

R - Esto no es válido.

P - ¿Debería Miniscript dar un error por hacer eso?

R - Sí y lo hará si intentas pasar el Miniscript a un descriptor...

P - Esta es una diferencia notable con respecto a los descriptores. El descriptor `pk` le dará el CHECKSIG. Eso va a ser un problema de compatibilidad.

R - No lo será porque el nivel superior `pk` es el descriptor `pk`. Desgraciadamente también es un Miniscript desnudo. Pero los Miniscript desnudos no deberían existir.

P - ¿Lo de Pieter es compatible con Miniscript desnudo?

R - No. Tampoco es compatible con el legado. Lo de Pieter es SegWit.

Esta es una ilustración de la envoltura c y v y también de lo que hace el sistema de tipos, cómo funciona. Una ilustración más. Cambiemos la v por una j que creo que realmente comprobará el tipo. Veamos qué sucede. Déjame imprimir el Miniscript.

`println!(“Script: ()”, my_descriptor.witness_script());`

La razón por la que estoy haciendo la impresión aquí para que pueda ver.... Puse la envoltura j en su lugar por lo que ahora tenemos SIZE 0NOTEQUAL OP_IF pasando aquí. Puedes ver mi fragmento original, tengo la clave de 33 bytes seguida por el CHECKSIG y he envuelto eso en un IF y luego la comprobación SIZE. Permítanme desactivar rápidamente esta aserción y veremos lo que ha sucedido con los tipos. Esto sigue funcionando. La j convierte la B en una V. La cosa original era B y todo esto. Una vez que lo envuelves en la envoltura j, la cosa OP_IF OP_ENDIF vemos que nada ha cambiado excepto que el modificador de tipo e ha desaparecido. No tenemos tiempo para hablar demasiado de la maleabilidad pero diré rápidamente lo que significa e, es un modificador de tipo de maleabilidad. e significa que hay una forma canónica de no satisfacer el fragmento. Lo interesante es que esto sigue siendo cierto. Si por alguna razón no satisfaces esto, hay un OR y necesitas ejecutarlo pero no quieres satisfacerlo porque es una rama no tomada entonces e te dice que puedes hacerlo de una manera no maleable. Esto es cierto para un tipo de CHECKSIG. Sólo hay una manera de no satisfacerla asumiendo que estás en las reglas de la Política que es proporcionar una firma vacía. Las firmas inválidas son rechazadas por la Política, he olvidado el nombre de esta regla. Me gustaría que fuera un consenso pero no lo es. Entonces hago la envoltura j y una vez que he hecho la envoltura j he perdido el fragmento e. ¿Por qué será? La razón es que lo que significa e es que existe alguna insatisfacción que es única. La envoltura j añade potencialmente una insatisfacción. Si pasa la cadena cero esto es insatisfecho. La envoltura j no sabe que ya tenemos la insatisfacción cero y que era única. Puedes imaginar que si en lugar de un CHECKSIG tuviera algo más complicado, una insatisfacción única pero que esa insatisfacción no fuera la cadena vacía. Entonces todo el fragmento lo podría insatisfacer o bien pasando un cero, en la envoltura de la j el OP_IF va a dejar un cero en la pila que es insatisfecho, o bien podría pasar la insatisfacción canónica de la cosa interna que sería distinta de cero por suposición. La j pasaría, pasaría aquí y obtendríamos una insatisfacción normal. La envoltura j ha pasado de tener una insatisfacción única a tener potencialmente una insatisfacción no única. En este caso, en realidad estamos bien, pero el sistema de tipos no es lo suficientemente inteligente como para detectar eso, por lo que este fragmento e desaparece cuando envolvemos. ¿Tiene esto sentido? Esta es una cosa sutil sobre la construcción de Scripts donde tomas algo que te convences de que no es maleable en algún sentido y luego haces algo que parece sensato como envolverlo en un IF ENDIF y luego proteger el IF para que siga funcionando. Ese algo podría en realidad romper tu suposición de maleabilidad. No te vas a dar cuenta. Todo lo que haces tiene todas estas interacciones extrañas. Lo bueno es que el sistema de tipos de Miniscript lo detectará por ti. Te dirá "Espera un minuto. Solías tener una única insatisfacción pero cuando añadiste esta envoltura añadiste otra insatisfacción. De repente tu insatisfacción ya no es única". Lo que significa que en la cosa más amplia hay algún contexto en el que podría estar insatisfecho, eso es un vector de maleabilidad. Miniscript detectará eso y rechazará mi Script o al menos lo marcará como maleable.

P - ¿La insatisfacción única para un CHECKSIG es cero?

R - Sí, es cero. En este caso está bien. He añadido un cero de insatisfacción pero que ya era único. Esto refleja una limitación del sistema de tipos de Miniscript. En principio podríamos añadir otro modificador de tipo que dijera "Hay una insatisfacción única y la insatisfacción cero". Entonces la envoltura j sería capaz de detectar eso y decir "Si la insatisfacción única era cero entonces preserva esta propiedad". Me pregunto si vale la pena añadir eso al lenguaje. ¿Ahorraría espacio? Tal vez, probablemente. No lo sé. Eso es algo para lo que Pieter tendría que escribir un fuzzer. Lo importante es que lo que hace Miniscript aquí es lo mismo.

Sigamos con el Script de introducción. Hagamos una ilustración más del sistema de tipos y luego hagamos la satisfacción. Luego haremos la composición.

P - Ese es un cambio que introducirías en el compilador porque todos esos modificadores no están presentes en la Política. ¿Si se añadieran estos modificadores, el compilador los añadiría y crearía scripts más óptimos?

R - Puede que el compilador ya lo intente. La forma en que implementamos el compilador es que hace todo lo que puede hacer y luego esas comprobaciones de tipo. Si se trata de algo que no es sensato, lo rechaza a posteriori. No somos muy conscientes de no probar las cosas porque eso requeriría mucho más código. Sólo nos daría un pequeño aumento de velocidad.

P - ¿Probar todo?

R - No probamos literalmente todo. Fui bastante burdo en las cosas que implementé. Hay una buena posibilidad de que el compilador haga lo correcto. También hay una buena posibilidad de que no lo haga. Ni siquiera lo sé porque mi compilador dejó de funcionar.... Yo sólo ACKed ciegamente y se fusionó. Eso no es cierto, miré para ver que no afectaba a ningún otro código. Coincide con lo que hizo Pieter porque Sanket y Pieter usaron la herramienta de Pieter Branchtopy para producir cien mil millones de Políticas y lo compilaron usando su compilador y el de Sanket.

P - …

R - Eso está en el Miniscript de Pieter.

Lo que mola es que Pieter sabe C++ pero no Rust, Sanket sabe Rust pero no C++, así que en realidad no pueden copiar código el uno del otro. Son dos compiladores completamente independientes que, sin embargo, coinciden en la salida. Sigamos. Un segundo ejemplo es [aquí](https://github.com/apoelstra/miniscript-workshop/blob/master/src/02-types.rs). Esto ilustra algunas cosas más sobre la biblioteca. Voy a apresurarme un poco porque quiero hablar de cómo satisfacer las cosas y quiero hablar de cómo compilar Políticas en la próxima hora. Una cosa aquí, he cambiado el tipo de clave sólo para ilustrar que podría hacer eso. Hay algunos tipos de claves diferentes por ahí que podríamos utilizar. Está la clave pública de Bitcoin, probablemente lo que quieres usar y que representa sólo una clave pública de Bitcoin que es una clave EC, podría ser comprimida. También tenemos este `DummyKey` que se utiliza para las pruebas. Este es un objeto proporcionado por la biblioteca Miniscript. Esto es bueno. Analiza y serializa la cadena vacía y sólo crea un objeto clave ficticia. Voy a ejecutar este código.

`cargo run —bin types`

Imagina que intento poner algo aquí como una llave o lo que sea. Esto va a fallar y dirá "llave ficticia no vacía". La única clave falsa válida es la cadena vacía. Otro tipo de clave que voy a probar es la cadena. Esto es algo genial.

`”wsh(c:or_i(pk(Andrew), pk(Sanket)))”`

Esto sigue funcionando. Ahora tengo una clave pública y estos son sólo cadenas. Ya no puedo traducir esto en un Script de Bitcoin, pierdo mucha funcionalidad pero puedo parsear, serializar y hacer análisis en estos. Esta es una característica realmente útil tanto para probar como para almacenar claves de forma interesante. Hay otra funcionalidad en la que no voy a entrar que permite traducir todas las claves públicas, proporcionamos una función para traducir las claves públicas. En Liquid realmente parseamos Scripts como este donde usamos una cadena que representa a todos los participantes. Después de analizarla y de realizar un par de comprobaciones de seguridad, buscamos en nuestra tabla hash qué pares, qué conexiones y qué claves, y traducimos la cadena de claves a un tipo más rico. Tenemos un montón de errores adicionales que podemos lanzar en ese punto. Convertimos eso en un tipo más rico que indica una clave funcional cruda o una que está ajustada para el hash de pago por contrato o lo que sea. Hay un montón de habilidades bastante avanzadas exploradas por esta biblioteca que te permiten hacer cosas muy ricas con las claves. Vamos a seguir con las claves falsas aquí. Una cosa rápida que quiero ilustrar. Tengo un Script más interesante aquí.

`”wsh(c:or_i(pk(), pk()))”`

Tengo este `or_i` que es la cosa IF ELSE ENDIF. Tengo mi envoltura c en el exterior de mi `or_i`. Déjame imprimir este descriptor.

```
let descriptor = Descriptor:: <miniscript::bitcoin::PublicKey>::from_str(“wsh(c:or_i(pk(020202….), pk(020202…)))”,
)
.unwrap();
println!(“***Witness Script: {}”, descriptor….ss_script());

let ms = Miniscript <DummyKey>::from_str(“c:or_1(pk(),pk())”,
)
.unwrap();
```

Podemos este Script aquí. Tengo esta clave OP_IF, clave ELSE, ENDIF y el CHECKSIG en el exterior.

P - Estás aprovechando la característica de que el compilador de Miniscript no sabe que esas dos teclas son iguales. ¿Piensa que son dos teclas diferentes?

R - Sí, eso es correcto. Ni siquiera es el compilador. Toda la biblioteca asume que estas claves son distintas. No hace ningún intento de detectar claves duplicadas. Es lo suficientemente útil como para no prohibirlo directamente. Pero estás por tu cuenta en cuanto al análisis de maleabilidad. En particular, esto es maleable. ¿Cómo se satisface esto? Usted proporciona un cero indicando que debe usar la rama derecha o un uno indicando que debe usar la rama izquierda, seguido de una firma. Si tratas de usar este Guión la misma firma va a funcionar para ambas ramas. Así que un tercero puede tomar su 0 o 1 y cambiarlo por un 1 o 0 y seguirá siendo válido. Miniscript piensa que esto no es maleable porque tienes un OR de dos cosas que requieren claves. En realidad lo es porque reutilizo claves.

Otra cosa que quiero ilustrar es que puedo tirar de esta c dentro y ahora tengo dos CHECKSIGs

`“wsh(or_i(c:pk(020202….), c:pk(020202…)))”`

Ahora he movido el CHECKSIG en el interior y ahora puedes ver que tengo dos CHECKSIGs. IF KEY CHECKSIG ELSE KEY CHECKSIG. Ambos son Miniscripts válidos, uno de ellos es un byte más corto. Si empezáramos con Políticas y usáramos el compilador, éste siempre notaría la reutilización cada vez. Esta es una de las razones por las que se recomienda utilizar un compilador en lugar de escribir manualmente los miniscripts. Volvamos al principio. Como mencioné, hay un error en la biblioteca ahora mismo que nos permite analizar descriptores que no están válidamente tipados. Voy a ilustrar cómo debería funcionar. Estoy pasando un Miniscript en lugar de un descriptor, voy a poner una v delante de aquí y veremos que va a fallar.

`”vc:or_i(pk(),pk())”`

Ya está. Dice "NonTopLevel", hay esta cosa gigante aquí. Te dice lo que ha analizado en qué modo. Puedo ver que si lo estoy desarrollando no son los mensajes de error más agradables del mundo. "NonTopLevel" significa que el Script de nivel superior no es un B. Entonces realmente escribió en detalle lo que es. Puedo ver en primer lugar que es un V no un B. Incluso puedo ver cómo sucedió esto. Puedo comprobar a través de esto. ¿Las llaves están correctamente formadas? No tengo este `or_i` aquí y ambas ramas son Ks que es correcto. La envoltura c la convierte en una B y luego la v, espera un minuto ahí es donde me equivoqué. Con un poco de pensamiento puedo averiguar lo que salió mal. Es una pregunta abierta de la API. ¿Cómo puedo producir mensajes de error más útiles aquí? Hay muchas maneras de que el nivel superior no sea una B. Prácticamente, si se comete cualquier error en cualquier parte de un Script, esto causará una cascada de errores que se propagarán hasta el nivel superior que es incorrecto. Lo más probable es que en algún punto de la línea haya habido un error real. No sé realmente cómo puedo ser más inteligente para proporcionar orientación al usuario aquí. Puede ser que tengas que hacer la ruta del compilador donde tienes gente que presenta literalmente cientos de errores sobre mensajes de error confusos y tienes cientos de heurísticos.

Si realmente quieres hacer un mal Miniscript no tipado aquí está la manera de hacerlo. Llegas a lo más profundo de la biblioteca, le pasas una expresión genérica, una expresión es sólo un montón de cadenas con paréntesis a su alrededor. Puedes imprimir esa expresión directamente en un Miniscript. Esta conversión de un árbol a un Miniscript, no hace ninguna comprobación de tipo. Esto es útil alguna vez, es muy poco ergonómico, debería serlo porque es algo malo, no deberías hacerlo.

Sigamos adelante. He estado diciendo que Miniscript puede codificar Script pero hasta ahora he estado escribiendo Miniscript en la forma canónica y describiendo lo que es el Script. Si tienes un Script real como esta cosa, esto es un Script crudo codificado en hexadecimal. Voy a parsear eso como un Script de Bitcoin y luego voy a usar la función de parseo de Miniscript aquí para convertir ese Script en un Miniscript. Voy a ejecutar eso.

`cargo run —bin script`

Aquí está mi Script original decodificado de una manera agradable. ¿No te parece que da miedo? Es como un IF anidado. Esto probablemente salió de nuestras pruebas fuzz. Hay una prueba de unidad en la biblioteca Miniscript llamada [all_attribute_tests](https://github.com/apoelstra/rust-miniscript/blob/5ba9bfe01780023062576f6fe4ccd2a9ced9c1db/src/miniscript/mod.rs#L451) que creo que Sanket produjo de alguna manera que hará cosas raras como uuj. Permítanme comprobar rápidamente lo que hace el envoltorio de u. u es improbable, toma un OR entre su cosa y el cero. ¿Por qué lo hace? Es básicamente lo mismo que j. Usted está tomando su insatisfacción potencialmente con algo complicado y está cambiando para proporcionar un cero para la declaración IF. Aquí en lugar de usar SIZE 0NOTEQUAL en realidad requerimos que el usuario ponga un cero o un uno en su lugar. Puede sorprender que sea más eficiente usar SIZE 0NOTEQUAL en lugar de poner un cero o un uno. El cero es un byte y el uno es dos bytes y SIZE 0NOTEQUAL es siempre dos. Pero de hecho lo es. Parte de la razón es que se trata de restricciones diferentes. El hecho de que éstas sean más eficientes es una afirmación sobre el mundo que Pieter y yo comprobamos. Lo que hemos hecho aquí es algo muy poco realista. Hemos tomado la envoltura de la u y luego la aplicamos de nuevo, lo que nunca se haría. No hay ninguna razón para hacer eso a menos que usted está tratando de presentar un error Miniscript. Analizamos el Script y obtenemos nuestro Miniscript. Imaginemos que estropeamos el Script de alguna manera. Cambiemos ese `63` a `61`. Ahora cuando parseamos podemos ver `InvalidOpcode(OP_NOP)`. `61` no es un Miniscript válido por lo que no lo parseará. ¿Qué pasa si en lugar de eso manipulo la clave pública? Voy a cambiar este `d0` por un `d1` que 50/50 hará que falle. Cerca del final tengo estos ceros. Déjame mostrarte rápidamente el Script de nuevo. Tengo este OP_0 y OP_0 aquí que son parte de la envoltura u. Si cambio uno de estos a un 1... `Unexpected("\#104")`. Cambié el cero por un uno pensé, ¿qué podría significar eso? Lo siento, el uno es `0101`.

P - ¿No es uno `51`?

A - Buena decisión. Usemos `51`. Puse `01` que significa empujar un byte y luego `68` que es mi ENDIF. Estaba interpretando eso como datos. Entonces se estaba acabando y no había ENDIF. Pero no tengo ni idea de cómo se convirtió en ese mensaje de error.

P - ¿No es `68` en hexadecimal que `140` lo que sea?

R - Sí, estaba viendo el empuje de uno. Está diciendo el número `101` para indicar que era un número decimal, no un número hexadecimal. Otra cosa que Core hace mal es usar la misma codificación para ambos.

He cambiado el cero por un uno. Tengo OP_PUSHNUM_1. Esto es en realidad un Miniscript válido. Puedes ver mi envoltura de la u aquí es ahora un `or_i` entre esta cosa de la u y el 1 que es un Miniscript válido. En realidad hace lo correcto. Si rompes las cosas, Miniscript te atrapará.

P - Debería cambiar uno de esos `63` por `62`.

R - Mira eso, "InvalidOpcode(OP_VER)". Es curioso.

 Déjame cambiar un `1` por un `2`. "Unexpected("\#2")" porque el número 2, no hay contexto en el que deba aparecer...

P - ¿Es justo decir que si tiene la misma identidad dos veces en el guión es algo que nunca haría?

R - Creo que sí. Si lo usas dos veces puede que haga algo. Si haces `jj` eso cambiará realmente las propiedades del tipo así que no puedo prometerte que eso sea inútil. Estoy 95\% seguro de que en todos los casos es inútil. Hará algo pero ese algo será añadir esto o perder propiedades de tipo. Cuantas más propiedades de tipo tenga, mejor. Esto acaba de salir de la prueba fuzz.

P - ¿Todos los scripts válidos de Bitcoin deberían ser analizables por...?

R - Ese era el sueño. Al final no podemos hacerlo. Hay un par de razones. Una es que conceptualmente hay cosas como las recompensas por colisión de hash de Peter Todd. No hay realmente ninguna manera de representar eso en Miniscript a menos que lo añadamos explícitamente, hash collision bounty. ¿Qué significa eso? No puedes pensar en ello como una combinación de comprobaciones de firmas y hashlocks o lo que sea. Tal vez podrías usar hashlocks si tuviéramos una noción de igualdad y desigualdad. Pero incluso esos no encajan en esta forma de árbol donde sólo tienes una colección de condiciones de gasto en un árbol. El objetivo es que si tienes una función monótona de comprobaciones de firma, hashlocks y timelocks y no tienes claves repetidas o subexpresiones repetidas entonces puedes expresarlo como un Miniscript y no habrá un Script más eficiente que haga lo que quieres. Creo que esto no siempre es cierto, pero está muy cerca de serlo. En la práctica creo que es cierto.

P - ¿Es posible tomar un Script, convertirlo en Miniscript y luego encontrar otro Script que sea más óptimo?

R - Esto ocurrió con Liquid, donde utilizábamos un opcode para contar cuántas firmas teníamos. Si teníamos 11 firmas, formaría parte de nuestra multisig de 11 de 15. Si teníamos 2 sería parte del multisig de emergencia 2-de-3. Con Miniscript originalmente guardábamos un byte. Luego llegó Sanket y añadió estos hashes de clave pública y pudimos ahorrar otro par de docenas de bytes al sustituir nuestras claves de emergencia por hashes de clave pública. Nuestro CHECKMULTISIG que no funciona con hashes, es como una construcción de umbral explícito, resultó que nos ahorró un montón de bytes. La razón por la que es eficiente es porque nunca usamos nuestras claves de emergencia así que no hay razón para jugar con ellas aquí explícitamente. Ese es un ejemplo. Me enteré de Ethan Heilman en Boston que tiene una empresa llamada Arwen que hace algún tipo de comercio altcoin no custodia que el HTLC como objetos que estaban usando, encontraron un par de bytes de ahorro mediante el compilador Miniscript. Con los HTLC de Lightning fuimos capaces de encontrar versiones más eficientes. Eso es un poco académico dado que es un evento para cambiar las cosas que se especifican en BOLTs. Fuimos capaces de encontrar versiones más eficientes de HTLCs. En muchos casos, incluso Scripts rodados a mano por gente realmente inteligente.

P - En nuestro HTLC para Miniscript hizo una cosa interesante donde normalmente tiene 1 o 0, depende de la rama que seleccione. La política de Miniscript genera una que sólo hace la comprobación de la firma en primer lugar y utiliza ese resultado para bifurcar lo que quieres hacer a continuación. Si la firma coincide va a la redención y lo contrario. Si la firma no coincide significa que usted quiere un reembolso probablemente y desencadena el bloqueo de tiempo.

P - ¿Su original era que se ramificaba y luego hacía la comprobación de la firma?

P - Sí. Hay una versión ingenua de la HTLC en la que se deja que el usuario decida lo que quiere hacer. Si intenta interpretar lo que hay como una firma, si funciona probablemente quiera canjearlo, si no lo hace probablemente sea la devolución del dinero.

R - Qué bonito.

Vamos a adelantarnos. Thomas (Eizinger) escribió un compilador para mí que robé descaradamente. Guardé sus notas de copyright aquí. Esto es de la biblioteca rust-miniscript y lo copió rápidamente durante el descanso. Se puede ver que está envolviendo divertido porque tengo un pequeño Terminal aquí. Aquí hay una política de HTLC. En realidad, este es un nuevo uso fresco de la macro de formato que no he visto antes. Puedes ver que la Política aquí es la HTLC. Tienes un OR de dos cosas, tienes una preimagen de hash del `secret_hash` y una firma con el `redeem_identity`. O tienes un timelock para el HTLC `expiry` y esta `refund_identity`. Puedes ver que Thomas ha añadido pesos a estos diciendo que es mucho más probable que se tome la primera rama que la segunda. Eso guía al compilador diciendo que el compilador debería intentar minimizar el tamaño de ese código a costa de producir potencialmente testigos mucho más grandes porque probablemente nunca se tomará. Así que probablemente el tamaño del testigo no importa, pero el código real siempre estará ahí, así que deberíamos minimizarlo. Entonces, ¿qué sucede? Permítanme ilustrar para la gente que quiera hacer esto en casa algunas cosas que sacamos. Traemos este objeto `Concreto`. Hay dos tipos de políticas en rust-miniscript. Hay políticas semánticas que son las que se obtienen cuando se empieza con un Miniscript y se desecha toda la información extra. Estas son las que se usan para hacer análisis y otras cosas. Luego están las políticas concretas, que tienen pesos en las ramas. Siempre se puede llegar a una política semántica desechando información. Tenemos una función llamada `Lift` que creo que usamos más adelante. Hemos importado el rasgo `Liftable`. Creamos esta Política concreta, la parseamos y puedes ver que se parece a Miniscript. La parseamos de la forma habitual usando el trait `from_str`. Luego llamamos a esta función `htlc_policy.compile`. La compilación convierte una Política concreta en un Miniscript. Luego lo envolvemos en un descriptor `Wsh`. El compilador sólo produce un Script óptimo. Por cierto, el compilador asume que se va a incrustar en WSH. Si compilas algo y lo pones en un P2SH puede ser ligeramente subóptimo. La razón es que antes de SegWit era igualmente eficiente codificar un cero o un uno porque el cero es el opcode `00` y el uno es el opcode `51`. En SegWit un uno es ligeramente más caro porque un cero es `00` y un uno es `0101` porque son cadenas de bytes en lugar de opcodes. El compilador toma esto en consideración cuando decide cómo ordenar las ramas IF y otras cosas, si el cero o el uno tendrán más probabilidades de ser tomados. Como resultado, podría tomar decisiones asumiendo el caso SegWit donde el cero es más barato, lo que hará que estas decisiones en cascada sean globalmente subóptimas si no estás usando SegWit. Eso está bien. No usar SegWit es una suboptimidad global por sí misma.

P - Y un problema de maleabilidad.

R - Y puede ser un problema de maleabilidad. En muchos casos lo es pero se me olvida específicamente cuando. Creo que gran parte de la biblioteca se desactiva cuando no se utiliza SegWit, aunque lo he olvidado. Hace tiempo que no pienso en esto.

P - ¿Pensé que querían no usar SegWit a veces?

R - Lo hice pero para cosas muy simples. Como sólo para lo que hace Liquid, que es tan sencillo que podía hacerlo incluso antes de SegWit. No era nada raro. Era como si la envoltura j no hiciera lo correcto. Realmente debería haber documentado eso en algún lugar. Obviamente lo olvidaré así que ¿por qué no lo escribí?

Lo llamamos `htlc_policy.compile`, analizamos la política, la compilamos. La salida del compilador nos va a dar un Miniscript y luego lo envolvemos en el descriptor `Wsh`. Entonces imprimimos lo que es el descriptor resultante y podemos ver que es un Miniscript. Me preguntaba de qué demonios estaba hablando Thomas, sobre tomar la salida de un CHECKSIG y usarla para cambiar. Yo estaba como "Miniscript no puede hacer eso", lo olvidé. Hemos añadido esta cosa `andor` que hace exactamente esto. Déjame mostrarte en el [sitio web](http://bitcoin.sipa.be/miniscript/) cómo se ve `andor`. Aquí está. Hace algún predicado y si nos desplazamos hacia abajo a las comprobaciones de tipo el predicado tiene que tener un par de restricciones. X tiene que ser Bdu. ¿Qué significa esto? La B significa que se mostrará algo distinto de cero en la pila cuando se cumpla. La u significa que ese no-cero va a ser uno y la d significa que es posible insatisfacerlo poniendo así un cero en la pila. Estas tres condiciones Bdu nos dicen que esta X aquí es posible de satisfacer o insatisfacer. Si se puede satisfacer o insatisfacer en esos casos saldrá uno o cero. Eso significa que puedo meter el resultado de eso en el IF o NOTIF según sea el caso. En el caso de que satisfaga X, si no falla será Y, en el caso de que no satisfaga usará Z. ¿Por qué usamos IF en lugar de NOTIF? Es para facilitar el análisis sintáctico. Si no usáramos el NOTIF habría una ambigüedad de análisis entre esto (`or_i`) y esto (`andor`). Cuando vemos el IF no sabemos si X va a aparecer. Hay un hecho claro sobre el análisis sintáctico de Miniscript que es que siempre es posible desambiguar lo siguiente. Hay dos excepciones que son fáciles de tratar. Siempre es posible desambiguar lo que está haciendo haciendo una mirada de un token hacia adelante y literalmente mirando lo que es el token. Mientras que si estuviéramos usando IF aquí tendría que analizar toda la X y mirar lo que era la X para averiguar si era algo sensato. Sería difícil distinguir entre eso (`andor`) y este `and_v`. Si tuviera un IF aquí, entonces si viera esto podría preguntarme ¿es esto realmente el `or_i` y esto es parte de este X Y `and_v` o es esto parte de `andor`? No es necesario seguir. El punto es que es difícil de analizar. Convenientemente Satoshi nos proporcionó dos opcodes IF. En este caso literalmente no importa cual elegimos así que usamos NOTIF en ese caso pero en ningún otro. Puedes ver que está aquí pero esto es en realidad sólo un caso especial. Cuando vemos NOTIF sabemos que estamos en `andor` lo que facilita el análisis.

Volviendo a nuestra compilación HTLC. Puedes ver que estamos usando la construcción `andor`. Hacemos la comprobación de la firma en el `0222......` que es una identidad redimida. Si la comprobación de la firma tiene éxito entonces comprobamos la preimagen del hash aquí. Si falla, significa que la rama izquierda de este IF obviamente no va a tener éxito, así que tenemos que hacer la rama derecha. Si falla hacemos la otra comprobación.

P - ¿Se utiliza `pkh` porque es más pequeño pero cuando se gasta será más grande?

A - Exactamente

Aquí hay un poco de información extra que Thomas añadió a este caso de prueba. Podemos usar esta función `lift()` y lo que hace es desechar la información extra y obtiene esta cosa de aspecto puro. Una cosa interesante es que cuando se levanta a estas Políticas abstractas todas sus claves públicas se convierten en hashes pubkey. ¿Por qué lo hacemos? Porque si empiezas con un Miniscript que tiene un hash de clave pública no es necesariamente cierto que puedas obtener una clave pública de él. Necesitas tener alguna tabla de búsqueda o algo así. No puedes deshacer el hash. En la Política abstracta no quise distinguir entre pubkey y pubkey hash porque son semánticamente el mismo tipo de cosa. Como puedo pasar de una pubkey a un hash de pubkey siempre haciendo un hash y no puedo ir en la otra dirección, simplemente coacciono todo en hash de pubkey en las Políticas abstractas. Esto es desafortunado. Durante mucho tiempo me opuse a incluir el hash de la pubkey en Miniscript debido a esto, pero me alegro de no haberlo hecho porque obviamente ahorramos un montón de bytes al hacer esto. Puedes ver el `script_pubkey`, puedes ver el `witness_script` aquí. Lo que es genial aquí, vamos a imprimir un poco más de datos. Déjame ver lo que tengo para este descriptor. ¿Qué métodos [tengo](https://docs.rs/miniscript/0.12.0/miniscript/descriptor/enum.Descriptor.html)? `max_satisfaction_weight`. Vamos a imprimir eso.

`println!(“Max sat weight: {}”, htlc_descriptor.max_satisfaction_weight());`

P - ¿Qué está pasando aquí? ¿Está descompilando a la política? ¿Vas a ese nivel de abstracción y luego vuelves a bajar?

R - Más o menos. Es muy parecido a descompilar, salvo que no recupero la política original porque pierdo los pesos. Es básicamente descompilar pero es mucho más simple que descompilar. Lo que estoy haciendo aquí es un mapeo directo de cada segmento Miniscript correspondiente a algo. Si veo `pk` o `pkh` eso mapea a un `pkh`. Si veo cualquiera de los tres ANDs diferentes que mapea a un AND. Si veo cualquiera de los cuatro diferentes ORs que mapea a un OR. Si veo un AND OR que mapea a una construcción anidada de AND y OR. Si veo cualquiera de los dos umbrales que se asigna a un "umbral". Es más bien un desmontaje. No estoy seguro de qué otra metáfora. Yo uso la palabra levantar que es un término de categoría. Estoy preservando toda la semántica mientras mapeo en un espacio más simple. Puedes hacerlo a mano, puedes hacerlo visualmente si quieres. El valor de esto es que una vez que tienes una de estas políticas abstractas puedes hacer algunas cosas interesantes. Puedes decir "¿Qué aspecto tiene esta política en el momento cero?" y cualquier cláusula que esté bloqueada en el tiempo la descartarás. Tal vez te diga que es insatisfactible, tal vez te diga que es más simple. Podrías decir "¿Qué aspecto tiene en el tiempo 1000?". Podrías preguntarle el número mínimo de claves con las que podrías firmar. Hay una serie de preguntas que puedes hacer sobre las Políticas abstractas que son más difíciles de hacer sobre el Miniscript porque el Miniscript tiene mucho ruido en ellas.

P - ¿Está haciendo las preguntas a nivel de Política? Creía que las preguntas se hacían a nivel de Miniscript.

R - No. Las preguntas que se hacen a nivel de Miniscript son cosas como qué es el script de los testigos, cuáles son los costes, cómo se hace un testigo. Las cosas que se preguntan en el nivel de la Política son las cosas semánticas. ¿Puedo firmar con estas claves? ¿Necesito estas claves para firmar? ¿Qué aspecto tiene en el momento cero? ¿Qué hace?

Permítanme tomar rápidamente el `max_satisfaction_weight` aquí.

`cargo run —bin compile`

La satisfacción máxima (peso máximo sentado) es de 292.

P - El peso máximo de satisfacción se basa en la Política por lo que tendría que enterrar todos los pesos o toma el peor caso?

R - Se toma el peor caso. Ese caso de satisfacción toma el peor caso. Eso incluye, creo, el peso del guión del testigo y también incluye el peor caso de tamaño del testigo.

P - ¿Es eso lo que utilizamos para la estimación de las tasas?

R - Sí, esto es lo que utilizamos para la estimación de los honorarios. Al igual que en Liquid, lo utilizamos para la estimación de las tarifas. En principio es posible ser más inteligente, pero es difícil.

¿Y si cambio mi política y digo que la primera rama es mucho más probable que la segunda?

`or(1000\@and(sha256({secret_hash}), pk({redeem_identity})), 1\@and(older({expiry}),pk({refund_identity}))’

Ese 292 que ves, es el mismo. ¿Realmente no importa? He cambiado el 10 por el 1000. Lo que quería hacer era cambiar el 1 por el 1000.

`or(10\@and(sha256({secret_hash}), pk({redeem_identity})), 1000\@and(older({expiry}),pk({refund_identity}))’

Veamos por qué fallan las afirmaciones.

`cargo run —bin compile`

Este es el descriptor que obtenemos y este es el descriptor que esperábamos. Aquí está el original y aquí el nuevo. Probablemente puedas ver más fácilmente que yo que las cosas se han reordenado.

P - En el caso del Rayo comprobamos primero la otra firma y el bloqueo de tiempo y sólo después pasamos a la preimagen.

R - Eso es lo que cabría esperar. Lo único que hacemos es comprobar primero la otra firma.

Apuesto a que el peso de satisfacción máxima si lo cambio todo será 1 byte más grande. En realidad no es el peso máximo de satisfacción el que va a cambiar, va a ser el peso medio de satisfacción. Sí sé cómo obtenerlo. Vamos a copiar y pegar la Política en [el sitio web de Pieter](http://bitcoin.sipa.be/miniscript/) porque mi código de bytes no va a ayudar con él. Permítanme primero comentar todas estas afirmaciones para que pueda saltar al peso máximo de satisfacción.

P - ¿Pieter produce la satisfacción media?

R - Sí, cuando está compilando, creo.

Yo corro esto. `Max sat weight 325` 325? ¿Por qué sería mucho más grande?

P - Creo que sigue comprobando primero la primera firma y luego la otra.

Echemos un vistazo a lo que ha cambiado aquí, aunque sólo nos quedan 15 minutos. ¿Qué es lo que realmente ha cambiado para que el peso máximo de satisfacción aumente? Seguimos comprobando primero la primera firma. ¿Se convirtió un hash de pubkey en una pubkey?

P - El hash de la pubkey sigue siendo un hash de la pubkey. Estás añadiendo la pubkey cuando la estás satisfaciendo.

R - Pero en el peor de los casos aún tendría que hacerlo. En un caso medio...

P - Debería preguntar en la página web de Pieter.

R - El sitio web de Pieter no... Al igual que averiguar los errores cuando hay problemas de tipo es muy difícil responder a preguntas como esta de una manera agradable. Si rastreamos este código fuente y vemos lo que está sucediendo mi experiencia es que Miniscript tiene razón y yo estoy equivocado.

P - ¿Se intercambian el segundo y el tercer argumento?

R - Parece que los ANDs están quizás anidados de forma diferente, lo que es sorprendente.

P - La parte confusa es que las cabeceras son las mismas, las claves públicas son las mismas. Si se cambian las claves públicas entonces deberíamos ver que realmente la clave pública cambia y la ramificación cambia con la preimagen.

A - ¿Las claves públicas son las mismas? Ok, este problema. Vamos a probar (cambiando el `refund_identity` a `03333333`). Esto no va a funcionar. ¿Por qué sólo hay una clave pública que aparece aquí?

P - El otro tiene hash. Es el mismo hash.

A - Ok podemos ver que se hace hash de una clave pública diferente a la del caso anterior. Ahí lo tenemos. Miniscript siempre tiene razón. Originalmente el peor caso era que tuvieras que hacer un hash de clave pública que es caro y un timelock que es gratis. Ahora el peor caso es que tienes que revelar el hash y el hash de la clave pública y eso es algo bastante caro.

¿No es genial? Estas cosas son muy difíciles de hacer a mano. Si tienes Miniscript que te dice la respuesta por adelantado al final lo consigues.

P - ¿Con Miniscript no sólo se puede calcular el peor caso sino también la distribución?

R - Sí.

Permítanme copiar rápidamente la Política aquí (en el sitio web de Pieter) y poner el Script de nuevo. El `secret_hash` es H, D es la `redeem_identity`, la `refund_identity` es F. Esperemos no haber dejado demasiados paréntesis aquí.

P - La caducidad también sigue utilizando rizos.

`or(10\@and(sha256(H),pk(D)),1\@and(older(4444), pk(F)))`

Veamos el análisis del coste del gasto. En el peor de los casos, 292. Aquí me da algunos promedios. Puedes ver por las fracciones que esto es un promedio. En promedio, dado lo que proporcionamos, es 212. Es una media ponderada de todas las diferentes vías de gasto. Si hacemos lo mismo, editamos el improbable.

`or(10\@and(sha256(H),pk(D)),1000\@and(older(4444), pk(F)))`

Nuestra compilación debería hacer lo mismo. En lugar de que la F sea hash, veremos que la D es hash. Salida del miniscript del sitio web:

`andor(pk(F), older(4444), and_v(v:pkh(D)),sha256(H)))`

Mi gasto agregado costó (179,673267). ¿Ha bajado? Interesante. Eso te dice algo sobre el HTLC. Si el HTLC funcionara de forma contraria, en realidad sería de media más barato. Desgraciadamente eso es un hecho sobre el HTLC y no una cosa de Miniscript. El hecho es que la preimagen de hash es la más común. ¿Alguna pregunta antes de que yo muy rápidamente correr a través de cómo satisfacer las cosas?

P - ¿Funciona esto ya con Tapscript?

R - No lo hace. Alguien creo que implementó esto y bifurcó tal vez el repo de Pieter y añadió un montón de cosas Tapscript.

P - ¿Con Tapscript cambiarían las optimizaciones?

R - Sí. Al menos en el lado del compilador no sería trivial implementarlo. Por lo demás, creo que hay un par de cuestiones de diseño.

P - ¿El repo de fuzzing está diseñado para colapsar el compilador?

R - Tengo un fuzzer que está diseñado para bloquear el compilador. Permítanme volver a mi Script de compilación aquí.

`vim 06-compile.rs`

Empiezo con la Política concreta y compilo al descriptor y luego lo levanto en esta afirmación. Tengo un comprobador de fallos que compila cosas, levantará la política original y levantará la política compilada y se asegurará de que son iguales, lo que significa que el compilador no ha compilado mal algo. De hecho, tengo un probador fuzz para el compilador que cambia la semántica.

P - ¿Tú y Pieter también probáis ambas implementaciones?

R: Sí. Pieter también generó como 100 mil millones de políticas con las que hizo las pruebas. Eso fue muy cansado. A veces nos desviábamos como en el 15º dígito de nuestros pesos estimados. A veces estábamos de acuerdo pero habíamos reordenado las cosas de una manera que no importaba. Al final pudimos eliminar todas las discrepancias y obtuvimos 100 \% coincidencias.

Tengo fuzz testers para eso. También tengo fuzz testers donde puedes parsear y reserializar Policies y Miniscripts en el formato de cadena. Y puedo ir de Script a Miniscript y viceversa y creo que de Miniscript a Script y viceversa. Siempre es único. En realidad encontramos un montón de cosas geniales, es bastante agresivo, bastante completo. Aunque si miras el repo hay todavía un par de bugs que creo que deberían haber sido capturados pero no lo fueron.

`vim 04-satisfy.rs`

Así que si usted es un desarrollador de la cartera tal vez la cosa más útil sobre Miniscript es la capacidad de satisfacer automáticamente. Voy a ir a través de este ejemplo que también cribado de los ejemplos Miniscript. Este creo que lo escribí yo. Disculpas si alguien en la sala lo escribió y estoy tomando el crédito. Fui yo. Gracias Thomas de nuevo por ese ejemplo de HTLC. Fue muy ilustrativo, realmente genial. Veamos la firma. Firmar es un poco más complicado. Obviamente necesito un montón de datos extra. Aquí hay una transacción de Bitcoin que estoy inventando. Va a gastar esta salida, el punto de salida es el punto cero. Esto obviamente no es real. La salida es un scriptPubKey vacío, que obviamente no es real.

P - ¿Podría ser?

R - Podría ser real, es muy poco probable.

Aquí hay un montón de datos, aquí hay una firma, aquí está el punto DER, las claves públicas. Aquí está realmente el código. Voy a tomar un descriptor. Esto es realmente algo real. Este es un script testigo hash 2-de-3 multisig.

`wsh(thresh_m(2, {}, {}, {}))`

Parseo este descriptor en un descriptor pubkey de Bitcoin. Compruebo que el scriptPubKey y demás son lo que espero que sean. El testigo Script como puedes ver tiene sentido. Hay un OP_2 seguido de 3 pubkey pushes, OP_3 y luego CHECKMULTISIG. Entonces voy a tratar de satisfacer esto. Aquí está la satisfacción real, el 1-de-2. Lo que voy a hacer es llamar a la función `descriptor.satisfy` y lo que le doy es mi `tx.input`. Lo que la función `satisfy` va a hacer es establecer el scriptSig correctamente y va a establecer mi pila de testigos correctamente basándose en si el descriptor es bare o P2SH o lo que sea. La función `satisfy` hará lo correcto. También necesito darle un conjunto de firmas. Esto es una cosa genial de la API en la que no tengo tiempo de entrar. ¿Qué es esta variable `sigs`? La variable `sigs` es en realidad un mapa hash de claves públicas de Bitcoin a firmas de Bitcoin. Lo más sencillo es crear literalmente un mapa hash de claves a firmas. Yo meto las firmas aquí y luego se lo pasas a la función `satisfy`. Pero puedo hacer cosas mucho más interesantes. Esto en realidad tomará cualquier tipo de objeto que implemente este satisfactor. Puedo darle un mapa de claves a firmas, puedo darle un mapa de hashes a preimágenes. No sé cómo codificar timelocks, creo que tengo otro objeto que hace eso. También puedo darle listas de estas cosas. Puedo tomar una firma... un mapa de hash, apuntarlo a esos dentro de una tupla y luego puedo pasar una tupla a esto y usará ambos. También puedo crear algún objeto personalizado e implementar este rasgo diciéndole cómo obtener firmas y cómo obtener preimágenes hash y cosas así. Esta función `satisfy` es extremadamente flexible pero la forma más directa y común de usarla sería hacer un mapa de hash de la biblioteca estándar, claves a firmas. Un `BitcoinSig`, es una firma secp y es un tipo sighash. Como mencioné en un comentario más abajo por defecto si pones una firma en ese mapa hash sólo va a utilizar si eso es eficiente. No verifica las firmas. La razón es que no puede verificar las firmas sin conocer el sighash. Si quieres verificar tus firmas, esto es algo que tenemos que hacer en Liquid, de hecho tengo un objeto personalizado que implementa el rasgo satisfier. Este objeto sabe qué transacciones se están firmando, conoce un montón de cosas que los funcionarios deberían estar haciendo, hace comprobaciones y registrará si algo va mal. Incluí mi propio satisfier que realmente verifica las firmas y que señalará si algo está mal.

P - ¿Podría usar verificar...?

R - Puede utilizar la verificación después. ¿Verificar, como ejecutar un intérprete de Script? ¿Qué quiere decir con eso? Hay dos cosas que podría hacer. Una es que podría verificar las firmas fuera de Miniscript. O podría intentar ejecutar un intérprete de Script y comprobar si el Script tiene éxito.

P - rust-bitcoin no tiene un intérprete de Script.

R - Correcto. O podría utilizar el intérprete de Miniscript de Sanket, con el que si tuviera 3 horas más podríamos jugar. Creo que una cosa sencilla de hacer es sólo verificar las firmas y el tiempo de satisfacción.

Rápidamente le mostraré lo que sucede aquí. Estoy imprimiendo la transacción sin firmar y la transacción firmada.

`cargo run —bin satisfy`

La transacción no firmada que puedes ver está vacía, la firmada tiene ahora un testigo aquí. Un par de cosas a notar. Pone el PUSH vacío que CHECKMULTISIG requiere en el lugar correcto. Pone las firmas en su sitio. Ordena las firmas correctamente, Miniscript lo hace por ti. En algún lugar de esas cosas está el Script testigo. Pido disculpas por la cutre salida sin texto. La razón es que el tipo de testigo es un vector de vectores de bytes. Por defecto, Rust los muestra en forma de array. Hay una discusión en el IRC de rust-bitcoin que probablemente deberíamos hacer nuestra. Otras dos cosas para demostrar si no hay preguntas. Si inserto una tercera firma aquí. Entonces ejecutamos el programa y vamos a ver todas estas afirmaciones todavía tienen éxito. Le di 3 firmas y sólo usó 2. Es incluso un poco más inteligente que esto, le di 3 firmas y si una de ellas era un byte más larga que la otra, lo que ocurre a veces al azar, dejará de lado la más cara. Tomará la firma más corta, que es el tipo de optimización que fue divertido implementar con Miniscipt, pero no sería divertido si lo estuviera haciendo para cada proyecto individual. Si le doy una sola firma va a fallar porque es un umbral de 2 de 3. Se puede ver `assertion failed`. La función satisfy acaba de devolver un error. Déjame ver qué error devuelve. En lugar de afirmar voy a desenvolver.

`cargo run —bin satisfy`

Ok sólo `CouldNotSatisfy`. Al igual que en la comprobación de tipos, y al igual que en la otra cosa que nos encontramos, es difícil en general proporcionar mensajes de error útiles si la satisfacción falla. En este caso teníamos un multisig de 2 de 3 y sólo una firma así que obviamente ese es el culpable. Pero puedes imaginar que tengo algún árbol complicado de diferentes conjunciones y disyunciones. Algo falla en la línea. ¿Se supone que debe fallar? ¿Se supone que debe tener éxito? Es difícil de decir porque tal vez hay alternativas. Tal vez todas las diferentes alternativas tienen algunas cosas que son posibles y otras que no. Tal vez el usuario estaba tratando de satisfacer una rama pero se equivocó y casi satisfizo otra rama. ¿Cómo puede el satisfactor saber cuál era la que se pretendía? De nuevo, no lo sé, son preguntas difíciles sobre la experiencia del usuario.

P - ¿Podría tirar todo?

R: El problema de desechar todo es que se produce una explosión combinatoria de lo que puede significar cada cosa. Una cosa que podría hacer es volcar cada clave y decir que estas claves tienen firmas, estas claves no. Estos hashes tienen preimágenes, estos hashes no. Estas claves de tiempo están satisfechas. Eso sería definitivamente más útil que la salida `CouldNotSatisfy`. En general hay ramas combinatorias diferentes, así que no se puede decir realmente cuál era la elección prevista en cada sentencia IF.

Estamos a las 12:30 y he tocado al menos todo lo que quería tocar. Voy a abrir el turno de preguntas o podemos hacer otras cosas si queréis.

# PREGUNTAS Y RESPUESTAS

P - ¿Esto permite evaluar el impacto de nuevos opcodes? ¿Podría implementarlo en Miniscript y ver cómo...?

R - Sí, absolutamente. Si alguien implementara un nuevo opcode, una nueva construcción AND u OR que se añadiera a Miniscript, Pieter y yo revisaríamos los primeros 100 mil millones de scripts y veríamos cómo compilaron este nuevo opcode y cómo no lo hicieron. Si hubo un cambio, eso es genial, es un opcode valioso por razones de eficiencia incluso sin ninguna otra razón, si no, tal vez eso es revelador. En realidad hicimos eso con muchos de los fragmentos de Miniscript. Los añadimos y luego ejecutamos el compilador 100 mil millones de veces y vimos si realmente afectaba a algo. Descubrimos que en algunos casos teníamos fragmentos que pensábamos que serían más eficientes, pero resultó que nunca lo fueron. Cuando el compilador mostraba que nunca lo era, hacíamos un análisis más duro para convencernos de que no lo era. Así pudimos reducir bastante el lenguaje y llegar al lenguaje actual. Si añadimos un nuevo opcode y nos da algo nuevo que no sea una firma, un hash o un timelock, eso sería obviamente una funcionalidad puramente aditiva. Realmente no hay nada más que podamos decir aparte de eso.

P - ¿Podría romper Miniscript y hacer que sea mucho más difícil de implementar?

R - ¿Podría un nuevo opcode romperlo?

P - Sólo si lo usas.

R - Al ser tan valioso que quisiéramos utilizarlo y luego encontrarnos con que todos los lugares donde lo intentamos tenían algún tipo de problema de maleabilidad o alguna tontería por el estilo.

P - Hay toneladas de opcodes que no utilizamos en Miniscript.

R - Muchos de ellos los queríamos realmente. OP_ROT hasta donde yo sé nadie lo ha utilizado. Sólo gira los tres primeros elementos de la pila. Si rotara en otra dirección que la que hace, podríamos usarla, pero no lo hace. PICK y ROLL, son un par de opcodes que realmente nos esforzamos en usar pero no pudimos encontrar una excusa. En esencia aprendimos que muchos de los opcodes existentes no son valiosos.

P - ¿Hay algún plan para cambiar la máquina virtual de Bitcoin, eliminar los opcodes o hacerlos más seguros?

R - Probablemente no. Si tuviéramos que cambiar Bitcoin Script, definitivamente usaríamos Miniscript para informar sobre la forma en que pensamos en esto, cómo pensamos en la maleabilidad, dónde el sistema Script existente nos causa dolor innecesariamente. El diseño específico de Miniscript tiene un montón de rarezas causadas por el actual Script de Bitcoin. Tratar de hacer que Script se corresponda más directamente con Miniscript no es resolver el problema correcto. Lo que realmente queremos es tener un Script que mapee a una variante de Miniscript que sea básicamente como el lenguaje de Políticas. Todavía hay preguntas como ¿queremos todos los diferentes ORs y ANDs? ¿Queremos un OR en el que tienes que intentar fallar para satisfacer las dos cosas en las que una de ellas tiene éxito, así como un OR en el que te saltas completamente algo? ¿Queremos ambas cosas necesariamente? No lo sé. Pieter y yo siempre nos metemos en esta madriguera y no encontramos ningún final. Mi opinión es que no. Se puede aprender mucho sobre cómo mejorar el Guión, pero no podemos aprender lo suficiente como para llegar a una propuesta que sea completa. En el diseño de Taproot, Tapscript, decidimos no hacer casi ningún cambio en Script. La única cosa grande que hicimos fue deshacernos de CHECKMULTISIG, que hace cosas tontas.

P - ¿No había una lista de opcodes de la que pudieras deshacerte en Tapscript?

R - Sí, pero no lo hicimos. No son útiles para Miniscript, pero quizás sí para otra cosa. Simplemente decidimos no hacerlo.

P - Quizá sean objetivamente malos en algún sentido.

P - ¿Se han eliminado todas las objetivamente malas?

R - Creo que sí. Había un [retraso cuadrático](https://bitslog.com/2017/04/17/new-quadratic-delays-in-bitcoin-scripts/) que Sergio encontró, un OP_IF o algo así. No podemos deshacernos del OP_IF, tenemos que mantenerlo. No creo que haya ninguno objetivamente malo que no utilicemos y que podamos eliminar y que siga existiendo.

P - ¿El lenguaje político sería compatible con algo como Simplicity?

R - Sí, puede escribir una Política en Simplicity.

P - ¿Si se tienen estos lenguajes de políticas existentes se puede volver a cambiar el compilador básicamente y se compila?

R - Sí, e incluso puede levantar del Simplicity a su Política y convencerse de que el Script de Bitcoin y el de Simplicity son el mismo. Se me acaba de ocurrir ahora que definitivamente debería implementar eso.

P - Una cosa interesante de la que Miniscript también se ocupa muy bien es la codificación de los números. Los números están codificados en Little Endian en Bitcoin Script. Puedes tratar de construir tu Script por ti mismo, es como una bonita pistola de pie. Sólo tienes que escribir tu número ahí, los cuatro bytes en Big Endian pero en realidad es Little Endian para el intérprete de Bitcoin y Miniscript se encarga de ello.

R - Sí, me he quemado con esto unas cuantas veces. Aunque se supone que también comprueba el rango... ahora mismo no he implementado eso que es un error bastante grave.

P - ¿Ha implementado ya el finalizador?

R - Todavía no. Tuve un sueño, no un sueño literal. Iba a conseguir todas estas pubkeys y construir una Política gigante con todas nuestras pubkeys en ella de alguna manera. Lo recopilaría y luego todos intercambiaríamos PSBTs y construiríamos toda una transacción en testnet. Me alegro de no haber intentado hacer eso. La razón por la que no lo hice es que tendría que escribir un montón de infraestructura para recoger claves públicas, recoger firmas, recoger PSBTs, analizarlos y validarlos. Rápidamente se convirtió en algo mucho más grande y claramente no habría tenido tiempo, así que me habría sentido tonto. Todavía no tengo un finalizador de PSBT.

P - ¿Puede explicar qué es eso?

R - Así que PSBT es una forma de que las personas que participan en una transacción adjunten datos, básicamente cuelgan datos de la transacción. El finalizador toma todos los datos, todas las firmas, todas las preimágenes de hash cuando las soporta, los datos de bloqueo de tiempo. El finalizador realmente construye un testigo, un testigo óptimo de todos los datos disponibles y crea una transacción válida. La forma en que un finalizador trabajaría es PSBT. Literalmente tomas la transacción sin firma en un PSBT, iteras a través de todas las entradas, sacas todos los datos del PSBT. En realidad, la forma en que lo haría es implementar este rasgo satisfier. Para cada entrada llamaría a `descriptor.satify`. Sería un truco de levantar el descriptor fuera de la transacción, necesitaría un reconocer que era hashes o Script hashes. Saco cada descriptor de la transacción. Llamo a `satisfy` pasándole una entrada de la transacción, el descriptor apropiado y... Entonces parsearía un PSBT.

P - ¿Lleva 18 meses con este proyecto y todavía no ha conseguido su objetivo inicial?

R - Así es. Si estuviste en el [Bitcoin Developer meetup](https://btctranscripts.com/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/) sabes algunas de las razones por las que esto es así. Surgieron muchas cosas geniales y muchas cosas se volvieron difíciles.

Q - You said somewhere maybe on a podcast that Miniscript was a rare example of something that you’d completed.

A - Right so there is a goal that we did complete. We did not complete the original goal of writing a finalizer. We absolutely have a complete language that can parse Scripts. We ripped out half the Liquid code and replaced it with Miniscript and it was all the code that I hated. All the witness building, fee estimates and the unit tests were so bad. We accomplished that. There is a practical sense in which it is finished and I can use it for everything I want to do. I feel like the flag to really say it is finished is we have a finalizer and we have a fee estimator that’s smart. Those two things I’ve been dragging my feet on.

P - ¿Qué estabilidad tiene? ¿Lo va a cambiar?

R - No creo que vayamos a cambiarlo. No ha cambiado en mucho tiempo, desde que añadimos el hash pubkey. Sanket se unió, se dio cuenta de que el hash pubkey era más eficiente y entonces tuvimos una especie de epifanía en la que revisamos todo el sistema de tipos. No recuerdo cómo funcionaba originalmente. Ahora tenemos un mapeo entre cada fragmento de Miniscript y cada fragmento de Script. Antes teníamos a veces ciertos fragmentos de Miniscript que correspondían a diferentes fragmentos de Script dependiendo del contexto. Teníamos esta distinción, y todavía podías analizarlos. Nos dimos cuenta de que de esta manera podías analizar Miniscripts a partir de Scripts sin conocer el sistema de tipos. Esto es algo realmente genial. Antes necesitábamos algunos datos de tipo para poder parsear. Tenemos la B, V, K, W, solíamos tener seis tipos y ahora tenemos cuatro. Se nos ocurrió la distinción entre tipo y modificador de tipo. Separamos los tipos de corrección, los seis, de los tipos de maleabilidad, los tres, lo que simplificó el sitio web un millón de veces. Teníamos dos tablas en lugar de una que era una locura horrorosa. Ahora creo que estamos contentos con ello. No soy consciente de nada que no pueda hacer que no requiera una revisión completa.

P - ¿Esta es la versión 1.0?

R - Creo que esto es 1.0. Creo que estamos en ese punto. Yo sólo terminaría esas dos cosas auxiliares que dije y escribiría el README para rust-miniscript para que esté en la organización de rust-bitcoin. En algún momento deberíamos trasladar las definiciones del sitio web personal de Pieter a algo que nos sobreviva. No creo que vaya a cambiar.

P - ¿Cambios aditivos tal vez?

R - Quizás cambios aditivos. Ciertamente va a cambiar para Tapscript. Probablemente consideraremos Miniscript Tapscript para ser.... tal vez podríamos hacerlo puramente aditivo.

P - ¿Se puede utilizar Simplicity en Elements pero se necesitaría un soft fork en mainchain?

R - Sí. Para Bitcoin Simplicity sería como otra versión de SegWit que reemplaza completamente el intérprete de Script.

P - ¿Alguna idea sobre si eso es viable?

R: Creo que es viable. Creo que tenemos que dedicar al menos varios años, la implementación está prácticamente hecha, escribir herramientas en torno a ella y demostrar el valor añadido, demostrando que podemos hacer este tipo de pruebas y razonamientos y que podemos validar las cosas en un tiempo razonable. Tenemos que hacer muchas pruebas en el mundo real. Para algo tan grande hay que desplegarlo completamente en algún lugar que no sea Bitcoin durante bastante tiempo. No podemos simplemente proponerlo con algunos pull requests y esperar que sea aceptado.

P - La simplicidad es un poco más poderosa, ¿verdad?

R - Simplicity es mucho más potente. Simplicity le permitirá verificar la ejecución de cualquier programa sin importar cuál sea el programa. No es Turing completo pero puede verificar la ejecución de cualquier cosa que sea Turing completo. Mientras que Miniscript sólo se limita a las comprobaciones sig, hash y timelocks. En Simplicity puedes hacer pactos, por ejemplo, puedes hacer bóvedas, que es un tipo de pacto en el que requieres que las monedas sólo vayan a un único destino en el que tienen que permanecer durante unos días o volver. Puedes hacer órdenes limitadas en las que tienes monedas que sólo pueden moverse si un determinado porcentaje de ellas va a algún sitio. Puedes tener entradas de oráculo que especifiquen cuáles son esos porcentajes, cosas locas como esas que Miniscript ni siquiera puede expresar. Incluso si Bitcoin Script fuera más potente no podríamos expresar esas cosas como funciones monótonas de condiciones de gasto. Esas comprobaciones de colisión de hash que Bitcoin Script puede hacer pero Miniscript no. Mi opinión es que si puedes usar Miniscript para lo que estás haciendo quieres usar Miniscript incluso si Simplicity está disponible. Si quieres compilar tu política de Miniscript a Simplicity pero no quieres usar... no tienes que hacerlo. Simplemente puedes hacer un análisis mucho más fuerte y más eficiente porque es muy simple.

P - ¿Se dirigen a otros backends de blockchain con el lenguaje Miniscript o Policy? Supongo que no necesariamente a los derivados de Bitcoin.

R - La respuesta corta es sí. La respuesta larga es que esto podría ser menos eficiente porque Miniscript tiene muchas verrugas extrañas que son específicas de Bitcoin Script.

P: ¿Qué tan fácil sería si se quisiera implementar... en el EVM?

A - Probably not too bad. What you would need to do, all the Script fragments on the website you just replace it with EVM fragments. You’re going to need to rip out all the malleability types and replace it with something different. Maybe you have to replace the other types as well.

P: No es como en un compilador tradicional, que quiere ser componible para poder cambiar la arquitectura de destino. Eso todavía no se ha conseguido con Miniscript, pero es algo en lo que estáis pensando.

R - Sí. Estuve hablando con David Vorick de Siacoin que es un blockchain que hace el almacenamiento de archivos, la verificación de contratos. Comprueba... y algo de codificación de errores pero no tiene un sistema de scripts. Me preguntaba si podía implementar Miniscript directamente, Miniscript crudo de alguna manera. Le dije lo mismo, que podría hacerlo pero que probablemente querría simplificarlo de alguna manera. Lo que es genial es que si tu motor de scripts es como Miniscript es mucho más fácil convencerte de que el código de consenso es sano frente a la pila de Bitcoin que no es sana.

P: Para un usuario final que sólo utilice la descripción de la política, ¿hay alguna advertencia, algún inconveniente al que deba prestar atención?

R - El problema es que el compilador puede cambiar. Miniscript no cambiará nunca. La única garantía de Miniscript es que cualquier Script válido que sea un Miniscript siempre será un Miniscript válido, siempre con la misma semántica. Con el compilador, puede ser que hoy lo compiles y obtengas un determinado Script con una dirección correspondiente. Puede ser que actualices el compilador y obtengas un Miniscript ligeramente diferente, que hayamos encontrado alguna otra optimización. No puedo prometer que eso no ocurra. Sí que es necesario que guardes por ahí la salida del compilador en algún sitio, aunque luego sea difícil de recrear. Esa es la advertencia, las cosas de la Política no llegan a la blockchain y lo que está en la blockchain es realmente lo que importa en última instancia.

P - Esto es en términos de optimizaciones, sería una agradable sorpresa si cayera.

R - Sería una bonita sorpresa.

P - Creo que Miniscript tiene un nivel bastante alto, pero todavía no es muy accesible, así que me pregunto si hay algún trabajo... Creo que podría ser bastante fácil hacer alguna interfaz bonita.

R - Sí. Stepan (Snigirev) lamentablemente tuvo que hacer su propia sesión pero estuvo hablando conmigo ayer. Él estaba planeando decodificar Miniscript de los Scripts en su cartera de hardware y luego levantarlos a la Política. Ahora tiene el árbol de ANDs y ORs y muestra eso en la pantalla. Eso todavía no es súper amigable para el usuario, pero está bastante cerca de explicar directamente lo que está sucediendo en el Script. Tiene una pantalla bastante grande, podría hacer una representación gráfica o algo loco como eso.

P - ¿La diapositiva que presentó ayer estaba delineada desde la Política....?

R - Si se eleva al lenguaje abstracto de las políticas, creo que es bastante bueno. Es algo que probablemente se pueda mostrar a un usuario final en muchos casos. Supongo que todavía hay claves involucradas. Tal vez habría que mostrar las claves de manera diferente y decir que esto pertenece a Alice, esto pertenece a Bob, etc.

P - ¿En una cartera que se pueda abstraer?

R - Sí. En la cartera se abstraería. Pero tienes razón Miniscript en sí mismo no es algo que mostrarías al usuario final.

P - ¿Existe un lugar de recursos para aprender sobre el compilador?

R - Está el [sitio web de Pieter](http://bitcoin.sipa.be/miniscript/), por supuesto, que describe todo el lenguaje. El [repo de rust-miniscript](https://github.com/apoelstra/rust-miniscript), en primer lugar rust-miniscript tiene algo de documentación. No es muy buena pero tampoco es nula. En el código fuente tengo un [directorio de ejemplos](https://github.com/apoelstra/rust-miniscript/tree/master/examples) con un par de ejemplos de cómo usar la biblioteca. Aquí está lo de HTLC. Aquí hay algunos ejemplos de cómo usar la API. Todavía no tenemos un buen comienzo desde cero, aquí está lo que es un Miniscript, aquí está cómo hacemos tareas comunes. Probablemente quieras ir a la biblioteca de ejemplos de rust-miniscript. Eso es probablemente lo más cercano. Probablemente escribiremos una entrada en el blog o simplemente una mejor documentación de introducción.

P - ¿El otro día hablaba de un BIP?

R - Un BIP sería menos útil que la documentación.

P - Un BIP sería simplemente el sitio web de Pieter.

R - Sería literalmente el sitio web de Pieter.

P - No le ayudaría a empezar.

R - Deberíamos y escribiremos una guía de iniciación.

P - ¿El repo de Pieter tiene documentación?

R - No, tiene mucho menos.

Este taller me resultó muy útil para ver cómo explicar desde un punto de partida qué tipo de cosas van mal y qué tipo de preguntas tiene la gente. Esto me ha ayudado mucho a entenderlo.

P - Y encontramos dos bichos.

R - Sí, y hemos encontrado dos errores.


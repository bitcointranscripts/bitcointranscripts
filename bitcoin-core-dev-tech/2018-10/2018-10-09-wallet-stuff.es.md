---
title: Cosas de Wallets
transcript_by: Bryan Bishop
translation_by: Blue Moon
tags:
  - wallet
date: 2018-10-09
---
<https://twitter.com/kanzure/status/1049526667079643136>

Tal vez podamos hacer que los PRs del monedero tengan un proceso de revisión diferente para que pueda haber cierta especialización, incluso si el monedero no está listo para ser separado. En el futuro, si el monedero fuera un proyecto o repositorio separado, entonces sería mejor. Tenemos que ser capaces de subdividir el trabajo mejor de lo que ya lo hacemos, y la cartera es un buen lugar para empezar a hacerlo. Es diferente del código crítico de consenso. Es probable que un cambio en la selección de monedas no afecte en absoluto a la interfaz gráfica de usuario.

P: ¿Cuándo tendremos los descriptores de script?

P: ¿En qué está trabajando la gente y qué les preocupa?

Estoy trabajando en la firma fuera de línea. Básicamente como lo que Armory tiene en términos de flujo de trabajo. Crear una transacción sin firmar, copiar y pegar en formato PSBT, llevarlo a una máquina fuera de línea, llevarlo de vuelta a una máquina en línea, difundirlo. Fusionarla, emitirla, cosas así. Estoy haciendo esto para salir de la armería. Este es también mi trabajo a tiempo completo ahora. Muy a mi pesar, estoy haciendo principalmente el trabajo GUI. Quiero ser capaz de hacerlo en si es 2am y necesito mover algunas monedas y yo tenía algo de beber, no accidentalmente enviarlos a Malí. Armory fue sorprendentemente bueno; es realmente agradable en muchos aspectos y también ha tenido algunos bugs críticos de pérdida de dinero uno de los cuales fue arreglado silenciosamente por lo que me temo. No hay flujo GUI para crear multisig ahora mismo, o para crear watchonly, o para hacer multisig en RPC. El flujo RPC es terrible de todos modos. El flujo RPC tiene como 37 pasos y necesitas preguntarle a alguien como hacerlo; bueno ahora son 32 en vez de 37. Me gustaría que watchonly bip32 funcionara correctamente, y sé que hay contención sobre cómo debería funcionar. Sí, descriptores de script. Creo que una de las razones por las que hay tanta discusión sobre cómo manejar watchonly en Core es que tenemos monedas watchonly y gastables en el mismo monedero, pero si las forzáramos a estar separadas sería más sensato ahora que tenemos multimonedero. En v0.17, hay un modo en el que no tener claves privadas en absoluto ahora. Es -disable-private-keys. Eso sólo separa watchonly y solvable... podrías separarlos completamente. Para cosas fuera de línea, todavía se necesita solvencia. Deberiamos apuntar a cosas solubles en vez de solo mirar; podrias solo mirar, pero realmente eso solo es util para mirar un balance y ver si los pagos fueron recibidos. ¿El modo sin clave privada es solucionable? Es sólo asegurarse de que no hay claves privadas, y no hay otros cambios. Una vez que tenemos descriptores, me parece que tiene sentido decir que un monedero es un descriptor o una familia de descriptores. Si quieres otra familia de descriptores entonces quieres otro monedero, tal vez. Un monedero es la unidad de control de monedas. Nunca me he encontrado con un caso en el que quiera hacer la selección de monedas desde múltiples descriptores separados. Pero imagino que algunas personas probablemente sí. La forma en que funciona la interfaz gráfica de usuario en este momento es que usted tiene un menú desplegable para seleccionar un monedero, y el ndoing un gasto utiliza el monedero seleccionado en ese momento. Si dices que quieres una transacción sin firmar, ¿qué monedas estás intentando gastar? ¿Sólo las monedas watchonly? ¿Las monedas solubles? ¿Intenta firmar utilizando otra cosa?

Watchonly se introdujo para la situación en la que participo en un multisig y quiero ver esas transacciones pero no quiero que se contabilicen en mi saldo. Por eso se introdujo watchonly. Creo que un error fue hacer que watchonly fuera sinónimo de «no tener la clave privada». ¿Ya no es sinónimo? Sigue siéndolo. En el modo de deshabilitar la clave privada, todos son watchonly y no se muestran en el balance. Hay otro pull request que ignora tu balance normal y te muestra otro. ¿Podemos obtener el balance watchonly a través de RPC? Es getbalance, dummy, minimum, y luego includewatching. Usted tiene que hacer los tres parámetros.

... watchonly debe ser disociado de tener las claves privadas o no. Si estoy usando un monedero hardware, entonces no tengo específicamente la clave privada en mi archivo de monedero, pero es mi saldo y quiero que lo incluya en mi saldo. Quiero que todo lo trate como mío. Armory tiene una casilla de verificación por monedero para «tratar como mío». Para Bitcoin Core, la bandera watchonly estaría en el descriptor y será independiente del hecho de si tienes la clave privada allí o no. La bandera watchonly significa que por defecto no se cuenta en tu saldo. Significa que no quieres ver el saldo; aunque quizás quieras darle un significado positivo, como «tratar como mío». Tal vez darle un nombre completamente diferente y eliminar el nombre watchonly.

Si tienes diferentes conjuntos de monedas, ¿la unidad de agregación es un monedero u otra cosa? Si es un monedero, entonces muestra todos tus monederos juntos. Podrías crear una transacción parcialmente firmada y moverla de monedero a monedero en la misma instancia de monedero Bitcoin Core.El dominio de agregación de monedas debería ser el monedero. Watchonly y non-watchonly, ismine y watchonly deberían estar separados en monederos separados como política general.

Si no tienes claves privadas, ¿muestra el saldo watchonly como saldo normal? ¿Que sea el saldo normal? ... En el glorioso futuro, cuando importas un descriptor, eliges si es mío, y si no lo es entonces no contribuye al saldo.

Quieres que importmulti soporte descriptores en la API, pero que lo convierta en wallet-fu en el monedero. Más adelante, puedes hacer que haga cosas mejores. ¿Deberíamos eliminar todos los demás comandos de importación? Primero deberíamos hacer que importmulti no apeste, luego deberíamos eliminar todos los demás. Tal vez desaprobar los otros.

importmulti no debería tomar nada más que combo en este momento. Más tarde, se puede hacer importdescriptor y luego deprecate todo lo demás, incluyendo importmulti.

La dificultad estriba en sustituir el depósito de claves. Es una caché de claves públicas específicas de un descriptor, en lugar de una cosa global de cartera que se alimenta de todo lo demás. La implementación del descriptor necesita tener alguna forma de aquí hay un objeto opaco con cosas en caché, para claves endurecidas necesitas tener las pubkeys pre-expandidas. No puedes derivar direcciones de otra manera. Eso tiene que estar ahí. ¿Cómo lidiamos con la lógica existente que usa un pool de claves y la lógica ismine y la nueva lógica que usa descriptores? Creo que, inevitablemente, estas dos lógicas tendrán que convivir durante un tiempo. ¿Podemos hacer una actualización forzada? Creo que sería bueno con el tiempo tener una manera de hacer una conversión de una sola vez de aquí está todo el goo en mi cartera, por favor convertirlo a un conjunto mínimo de descriptores que hacen lo mismo. Pero esto no sería algo a implementar a corto plazo. Esto está relacionado con el combo.

P: ¿Esto va a estar en un gran PR?

R: Voy a añadir soporte en el módulo descriptor para tener claves pre-expandidas, que es sólo un cambio lógico no expuesto en ninguna parte. Entonces tendremos que eliminar parte de la lógica existente de ismine, que actualmente es global, para ser más encapsulada como un método de cartera. Posiblemente tener una manera de tener múltiples instancias de eso. Y luego se puede añadir un segundo almacén con los descriptores.... y más tarde tener una manera de convertir el material existente en la nueva cosa.

P: ¿Tiene sentido tener un bitflag de cartera para esto?

R: No, no lo creo. Simplemente va a ser una nueva versión del monedero una vez que tengas los nuevos registros. Pasando de que el keypool sea algo global a tenerlo más encapsulado. No tengo muy claro cómo hacer esa implementación.

P: ¿Los descriptores de scripts están sustituyendo a ismine pero también a este repositorio de claves y son dos cosas diferentes?

R: Sí.

P: ¿Cuál es el reto con el pool de claves?

R: Demasiada lógica que no he revisado recientemente. Está integrado en muchos sitios.

Quizá debería haber una segunda reunión quincenal para hablar de la cartera. Tal vez quincenal. Mensual, programada según la zona horaria islandesa. Dos veces por semana es quincenal, no bisemanal. No, eso no es correcto. Quincenal significa dos veces al año, sin ambigüedades. Semestral significa dos veces por semana.

Algunas personas quieren exportar las transacciones de la cartera, como para la presentación de informes fiscales. Quieren exportar el historial de transacciones para poder declarar impuestos, en combinación con intercambios y contabilidad. Una vez que tenga una alternativa dumpwallet que escupe json, que sería útil. dumpwallet no da transacciones, pero una nueva cosa podría. listtransactions también hace que en este momento. Hay una jursidicción fiscal en la que si tienes al menos un millón de dólares, asumen que puedes ganar al menos un 4% sobre eso, y por eso gravan esa ganancia al 30%. Si su patrimonio neto salta significativamente de un año a otro, entonces van a investigar eso.

Otra cosa que se necesita es un reemplazo de berkeleydb.

Aislamiento y separación de procesos... la gente parece pensar que hace cosas complejas que en realidad no hace. Sustituye a los punteros CBlockIndex y llama a través de una interfaz. Es un cambio muy mecánico. No cambia nada en absoluto. Es sólo la interfaz entre la cartera y el nodo. La gente parece estar intimidada por estos pull requests, son 25 commits, pero cada uno es bastante pequeño. El CBlockIndex cosas es el corazón de la PR y luego un montón de commits más pequeños. Tomaré los primeros 5 commits y los pondré en PRs separados.

Wallet PR#s que nos consigue la magia manual de la cartera de hardware PSBT: 14075, 14021, 14019

Tiene que haber un script que muestre la diferencia entre la última vez que se revisó y ahora.

Wallet PR#s que nos consiguen la magia manual del monedero de hardware PSBT: 14075, 14021, 14019

¿Qué pasa con la actualización de carteras? En v0.17, podemos hacer la actualización de no HD a HD. Pero la actualización ocurre al inicio, y si tu monedero está encriptado entonces.... Así que, con el tema del descriptor, puede que también necesitemos descifrar los monederos para poder actualizarlos. No creo que necesariamente debamos actualizar al inicio. Debería ser un RPC y pueden hacer una actualización, «actualiza esto no puedes volver atrás». ¿Qué pasa si arrancas Qt? ¿No se inicia y no carga la cartera? En el futuro propuesto, cargaría la cartera como actualmente y no se actualizaría. Pero tienes que soportar el material antiguo, porque no puedes hacer una actualización única hasta que esté desencriptado. Sin embargo, podrías hacerlo watchonly. Puedes negarte a cargarlo, no tienes que soportarlo. Pero la actualización puede ser, haga clic en el botón en lugar de simplemente hacerlo. Yo personalmente odio eso, pero es una manera de hacer que funcione.

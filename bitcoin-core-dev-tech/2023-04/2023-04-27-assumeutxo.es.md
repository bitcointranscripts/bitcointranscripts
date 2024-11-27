---
title: AssumeUTXO update
translation_by: Blue Moon
tags:
  - bitcoin-core
  - assumeutxo
date: 2023-04-27
speakers:
  - James O'Beirne
---
## Objetivos

- permitir a los nodos obtener un conjunto utxo rápidamente (1h)
- al mismo tiempo, sin grandes concesiones en materia de seguridad

## Enfoque

- Proporcionar instantánea utxo serializada
- obtener primero la cadena de cabeceras, cargar la instantánea y deserializar, sincronizar con la punta a partir de ahí
- a continuación, iniciar la verificación de fondo con una segunda instantánea
- por último, comparar los hashes cuando el IBD en segundo plano llega a la base de la instantánea

## Actualización del progreso

- se ha hecho mucha refactorización; se ha introducido `ChainStateManager`, se han eliminado globals, se ha refactorizado mempool / blockstorage
- cambios en la lógica de init / shutdown se han fusionado
- cambios en la cartera realizados
- cambios p2p aún en revisión (por ejemplo, la elección de la cadena de estado a la que añadir nuevos bloques)

## Cuestiones pendientes 

El orden `nFile` se fragmenta, posibles problemas con la poda y/o reindexación -> Introducir contador nFile de blockfile por tipos de chainstate (cambio simple)

## Poda

- actualmente, objetivo de poda con ventana final
- hacer lo mismo, pero con dos puntas - diferentes posibilidades para conseguirlo

## Indexación

las señales `validationinterface` son recogidas por los índices

- podría construir fuera de orden, pero algunos índices (coinstats) no puede ser construido fuera de orden
- solución sencilla: desactivar todos los índices hasta que se complete la sincronización
- solución sofisticada: desactivar sólo algunos indexadores

- Introducir rpc para cargar chainstate
- Poner hashes assumeutxo reales en chainparams
- En total, sólo ~ 1k loc izquierda, aunque la mayoría en lugares importantes

## Planteamiento de la discusión


- ¿Realmente necesitamos la sincronización en segundo plano?
- No hacer la sincronización en segundo plano es más simple, pero cambia los supuestos de seguridad.
- Además, se eliminaría la necesidad de que cada nodo debe ser capaz de sincronizar la cadena

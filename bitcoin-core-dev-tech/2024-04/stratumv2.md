---
title: Stratum v2
tags:
  - bitcoin-core
  - stratum-v2
date: 2024-04-08
---
I explained the various stratum v2 roles described in the images here:
[https://stratumprotocol.org](https://stratumprotocol.org)

Described the three layers of my main PR:
[https://github.com/bitcoin/bitcoin/pull/29432](https://github.com/bitcoin/bitcoin/pull/29432)

1. Noise protocol
2. Transport based on the TransportV1 / TransportV2 class
3. Application layer (listens on new port, sv2 apps connect to it)

Discussion point: the Job Declarator client role typically runs on the same
machine as the template provider, so technically we don’t need noise encryption.
However, we may in the future want to “take over” some of the Job Declarator
client work, at which point we would need it. Also, currently SRI doesn’t have
any other way to communicate (e.g. unix socket). Also this part of the code is
relatively straight forward (layer 1). We’d still need layer 2 and layer 3 with
or without encryption.

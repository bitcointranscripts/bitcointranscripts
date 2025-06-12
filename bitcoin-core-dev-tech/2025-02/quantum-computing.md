---
title: "Future of Quantum Computing"
tags: ['bitcoin-core', 'quantum']
date: 2025-02-25
additional_resources:
  - title: 'BIP360'
    url: "https://github.com/cryptoquick/bips/blob/p2qrh/bip-0360.mediawiki"
---

BIP360

- segwit 2.0 - new witness field just for QC signature data
- choose 1 (m?) of n schemes
- all the schemes are fixed size to prevent inscriptions ordinals etc
- fixed size for chosen sig type

how do we know that any of these are resistant? once we have QC its too late EC
might even be safe, just because you have QC doesn't mean you can get the actual
information out, it might still be exponential

concern about hash mining, double qubits doesn't double hashrate "progress
freenes" - hit a probablity field instead of just try and fail changes the
incentives at the tip, ie block witholding

OP_NOP upgrade path with some future softfork

the longer you wait the better the algos will be, but the riskier it gets
bitcoin upgrade path is so slow tha tby the time somehting is merged, something
else could be better arms race between bitcoin devs and QC design itself

what if ther is QC design in stealth mode and we can't prepare

watch only / xpub / multisig / HD wallets

expand on matts upgrade idea

- script path commits to hash (hash reveals another hash)
- in the future soft fork in something that requires a proof of the preimage
  - commit to preimage without revealing it, but also commit to outputs
- postpone the choosing of the ZK proof algorithm
- or use open timestamps to prove prior knowledge of a preimage
- prove at some point in pre-quantum time that you can sign an output, and
  reveal that post quantum

have miners aggregate these ZK proofs

Having people move funds is a big social issue, might frustrated users if QC
never comes.

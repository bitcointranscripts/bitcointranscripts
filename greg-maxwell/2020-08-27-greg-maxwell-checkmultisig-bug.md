---
title: Checkmultisig Bug
transcript_by: Michael Folkson
tags: ['hard fork', 'multisig']
speakers: ['Greg Maxwell']
date: 2020-08-27
---

What is stopping the OP_CHECKMULTISIG extra pop bug from being fixed?

Location: Bitcointalk

https://bitcointalk.org/index.php?topic=5271566.msg55079521#msg55079521

# What is stopping the OP_CHECKMULTISIG extra pop bug from being fixed?

I think it is probably wrong to describe it as a bug.  I think it was intended to indicate which signatures were present to fix the otherwise terrible performance of CHECKMULTISIG.

Regardless, there is no real point to fixing it:  Any 'fix' would require that all software using CHECKMULTISIG get an incompatible change (as part of a highly disruptive hard fork).  Because the extra value is now always zero (and was pretty much always, or was actually always zero before)  you can compress it out  completely over the wire or on disk if you really care-- so the only effect it has is its weight in transactions and the one or so extra cpu cycle going into a hash.

Instead a new operation can be introduced that just doesn't have that behavior-- and that would be compatible, software that wants the new behavior would just upgrade when it wants it,  no flag day, no disruption.

BIP342 replaces CHECKMULTISIG entirely with something that is more computationally efficient and more flexible (and more space/weight efficient too, once you count that the signatures are 9 bytes shorter and the pubkeys are 1 bytes shorter).

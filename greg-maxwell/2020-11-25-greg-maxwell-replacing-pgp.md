---
title: Replacing PGP with Bitcoin public key infrastructure
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
date: 2020-11-25
---

Location: Reddit

https://www.reddit.com/r/Bitcoin/comments/k0rnq8/pgp_is_replaceable_with_the_bitcoin_public_key/gdjv1dn?utm_source=share&utm_medium=web2x&context=3

# Is PGP replaceable with Bitcoin public key infrastructure?

This is true in the same sense that PGP can also be replaced with some fancy functions on a school kids graphing calculator.

Yes you can construct some half-assed imitation of pgp using stuff from Bitcoin, but you probably shouldn't.

If all you really want is some file signing thing without any key certification or encryption, I suggest looking into openbsd's signify. Bitcoin is not a buzzword.

PGP does vastly more than just sign a file with a key and verify it. If that is all you need to do then PGP is indeed overkill, but the alternative you should probably consider is a tool made for that purpose, such as "signify".

Using Bitcoin because bitcoin just feels like buzzword following to me.

PGP addresses many things that aren't addressed by narrow tools. For example, PGP does both symmetric and asymmetric encryption. PGP manages key rings (tracking whos keys are who). PGP manages key authentication (how do you know the key you are using is a real one, not an imposter), PGP can encode binary messages to cross non-binary clear channels, and so on.

Bitcoin's message signing was a mostly informal tool created for some narrow purposes where holders of bitcoin needed to sign short messages connected to those Bitcoin. Sure, you can apply it more broadly, but there are tools made for that.

The original message signing is slowly drifting into unmaintained status -- in part because it can't serve its original purpose anymore because just signing with a single key means it can't reflect modern coin ownership. There are [newer proposals](https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki) that import all of Bitcoin script for their signing, restoring the original intent of the signmessage. But those tools will be less well suited for "sign some file" purposes.

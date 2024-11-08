---
title: Smart Signatures
transcript_by: Bryan Bishop
speakers:
  - Christopher Allen
---
Christopher Allen

Smart signatures and smarter signatures

Signatures are a 50+ year old technology. I am talking about the digital signature. It's a hash of an object that has been encrypted by private key and verified by a public key against the hash of the object. All of our systems are using this in a varity of complex ways at high level to either do identity, sign a block, or do a variety of different things. The idea behind smarter signatures is can we allow for more functionality. Multisig, which is what bitcoin and some other tech has allowed us to do, is an exmaple of this. We would like to address much more complex use cases.

We don't want to run into situtaions like TheDAO that break things. We need to do some experimenting. There's AND multifactor (N-of-N multisig), M-of-N multisigs, OR multifactors, for instance for legacy purposes we could have an ECDSA multisignature or we could have an RSA multisignature, or to really future-proof things, a sphinx hash signature which is quantum-resistant. You can choose whatever sig you want, verify the one that works best for you, we will give you all three.

This allows for many types of varied content and things we could do cryptography. We can do time-limited delegation. We could say the signature is only valid during this period, but building it into the signature itself instead of being a policy above the sig. We could do use limitations like, the sig is only good if the transaction does not exceed a certain amount of money value. We could say delegation is only good for signing a subproject but not the prime project, it could be a development release but not a public release.

There's a lot of power when we can do internal depth, there's a variety of uses, but there's a sense of extenral depth that allows us to pass proofs. This is a powerful way of thinking about a lot of the future of blockchain is how does one system or layer pass a proof to another layer that something has been accomplished from a transactional point of view. Sometimes we just need to pass a proof, not actually do computation.

Proofs need to be composable. Those individual elements need to be inspectable. A human needs to be able to understand what's going on. And they need to be provable. There are new comp sci approaches to doing provable components that we can basically go oh we're really certain about the security of the code that's in that. We have some runtime requirements. We want smart signatures to be deterministic, we want them to be bounded and to be efficient.

There are many approaches, like functional languages like Forth, lambda calculus like Lisp, I would love to have a pull request to my paper from ripple about conditions. We will hear about DEX in a quick minute in another lightning talk.

How do you define context? How do you deal with revocation? What hardware devices? How do you deal with oracles?

http://www.weboftrust.info/

September 28, 29, 30 in SF

https://github.com/WebOfTrustInfo/ID2020DesignWorkshop/

---
title: 'Dex: Deterministic Predicate Expressions for Smarter Signatures'
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Peter Todd
---
I have been working on deterministic expressions language called DEX. It looks like lambda calculus. But really we're trying to create a way to specify expressions that would return true if a signature is valid. Something like this, which is really just check a signature against a pubkey for a message, is essentially something that would be baked into your software anyway. We're trying to move into a layer of abstraction where you can specify the conditions you need for your particular use case. This might be a standard public key. But perhaps you want to do a multisig where Alice signs and Bob signs. That's simple. Something like that is opening up a lot of possibilities, like in bitcoin with multisig.

You could also see things like OR conditions where you have a release-pubkey that could sign any release, and maybe a dev-pubkey which is only allowed to sign development builds. You could build this in where you define the defintion of a valid software release, where it's valid if only signed by the dev-pubkey only if the build is marked as a debug build. It's simple, but it's a nice improvement.

Rather than hashing and committing to these kinds of conditions as a hash of your entire script, if you start doing things with trees then you can get more clever. Rather than serializing the whole thing, serialize parts of the tree, you could say the release build is valid by showing the thing that I have revealed as part of the signature process has the same hash. All this stuff about dev-pubkeys you don't need to know, it's just a digest, one branch of the OR checks out and we're all good.

The next use case is something like delegation. I could have a master-pubkey, like if you're in OpenPGP you have a master pubkey associated with your GPP key. What if I have a binding signature (bind-sig) with a hash sub-expression? You could sign your code as needed, and keep expanding the set of capabilities, maybe that's the software release, and the subexpression is when I give the developers the ability to go and sign a debug build.

This is early stuff. Ultimately we're just trying to go and build some basic primitives. The flip side of this is that once you start adding predicates, you might be defining entire protocols in this.

---
title: Signature Aggregation Update
tags:
  - bitcoin-core
  - signature-aggregation
date: 2023-09-21
---
## The status of the Half-Agg BIP?

TODOs but also no use cases upcoming so adding it to the BIP repo doesn't seem useful

BIP Half-agg [TODOs for BIP](https://github.com/BlockstreamResearch/cross-input-aggregation/issues/11)

Consider setting z_0 = 1

Reconsider maximum number of signatures

Add failing verification test vectors that exercise edge cases.

Add signing test vectors (passing and failing, including edge cases)

Test latest version of hacspec (run through checker)

Half-agg BIP has a max number of signatures (2^16), making testing easy

Needs more test vectors

Open it as an informational BIP?

Potentially attract talent/more eyes to the project

## Incremental half aggregation

Kind of new, already included in BIP and PR

Crypto portion straightforward, no secrets involved

Gossip channel announcements use case being discussed (Rusty?), no real momentum currently, not sure if 32bytes bandwidth saving is worth the effort

Half-agg will give a blocksize efficiency improvement, but no computational benefit

How many more tx in a block? Not many more, as witnesses already discounted.

Half agg much easier than full-agg as no interactivity needed

Discussion about whether aggregation could be done in a utreexo style roll-out with a different class of nodes, while not changing the consensus rules

Full aggregation and MuSig are completely different on a conceptual level

Useful to think of sig validation between 3 parties (sender, receiver, and validators)

MuSig example did whoever need to sign sign? (dont care WHO signed)

MuSig, FROST, etc are techniques to have a single key for an input, but going across multiple inputs is fundamentally different

In sigagg, aggregation is done by the verifiers who see everything vs MuSig where only involved parties see the keys

In musig and frost you simply use schnorr verification (verify(sig, message, pubkey) => true/false) while sigagg verification is verify(sig, [(m1, p1), ….])

## Benefits of halfagg

More tx in a block, space savings

But not much computational savings

Coinjoin benefits (halfagg and fullagg)

Concerns about fullagg actually hurting privacy

Having a single signature via full-agg is easier to do on your own txs rather than on multi-party tx where interactivity is needed. This means privacy busting services like chainalysis can use that as a heuristic, assuming aggregated-sigs are a sign that all the inputs belong to the same person.

Batch validation and Half-agg have same computation performance benefits

Approach: Consensus change, v2 witness

Half-agg consensus changes more invasive than taproot

## Security proofs

Under certain assumptions, if you can forge schnorr sig, you break discrete log

Security loss of proof details

When we say we have a security proof, there is nuance; under certain assumptions we prove that if we can forge a schnorr sig, you can also break discrete log. Most traditional Schnorr proof, the statement is of the form, if you have a probability x of forging a sign, that turns into a prob of some function of that (x^2) of breaking the discrete log.

If we assume that the probability for computing the discreet log is not better than 2^128, this only implies that schnorr sig forgery is no more secure than 2^64. Which is not something that we would ordinarily accept. Crypto world has accepted this, theoretical world not so. Can you make your schnoor group big enough this is not a problem?

Can target a certain security level by increasing group size, e.g. 512 bit group bight give 128 bit security.

In practice world accepted that these loss factors are a side-effect of the proof, and not real. And that it actually is hard to break Schnorr signatures.

There is an alt proof with different assumptions re. group size and hash size (the two params). The first one says we have a ^2 one for the group, but this one says use bigger hashes and make the group a bit smaller. Does this point to a lack of a fully-sensible proof? Using random-oracle stuff you might not get a tight proof.

If you don't assume special things about the group, idealised assumptions, you have a loss of that square property. Someone has proved that there is no better proof. This doesn't imply it's insecure, but there is no better proof. In MuSig 1 paper there was a ^4 root loss. Similar here for half agg; there is a fork per signature, so there is a loss factor which is 2^n where n is number of transactions. So with 7 tx it only proves that signature is 1 bit secure.

There is no perfect security proof, but in practice that is often tolerated/acceptable. But for half agg, since it's new, makes sense to be cautious.

If you look at math guarantees, it can be misleading. e.g. if MuSig turns out to be much weaker than schnorr, then we can switch. We are only as secure as the weakest link.

Today we can do broken things in consensus, but it's not whether consensus allows, but whether it's safe. If there are many things encumbered by a scheme that is now insecure, that becomes a problem.

How can MuSig be insecure? Perhaps only from your co-signers. But with half-agg, if this is in consensus and turns out to be broken, then I might be able to spend your coins with a half agg sig, which would be extra bad. Very different level of failure to MuSig turning out insecure.

Half agg needs a much more invasive consensus change than taproot; where instead of True become x, but half agg needs a tx-level something?

Is a stronger proof a requirement to introduce to bitcoin? Some say no. ECDSA was picked before a security proof existed! :P There is a proof but the theoretical-loss is so large that is “appears” broken. There is a “tight” proof (little loss) in a stronger model, but the question is do we accept this. Community must decide…

Is a security proof required for a proposed consensus change?

With full CISA, a problem with a new script version, similar to g'root

separate sigs from scripting - does this also apply to half agg? Yes. Need to be unambiguous about which sigs are aggregated. Imagine a new tapscript, V2 (simplicity?), an old verified will not be able to see those signatures, not recognise them as signatures, need two separate algos; one for pre-fork, and one for the upgraded nodes. Not hard, but must be careful in designing as e.g. OP_CHECKSIG/OP_SUCCESS could break? One thing you could do is say CISA only applies to key-path spend. Downside is that this needs a new witness version. But it is the most impactful as we expect most signatures to be key-path spends. Not aggregating keys in the script side removes many problems.

Tx validation needs to be unambiguous about what the signatures are for

Old verifier cant see those signatures, wont recognized them as sigs even

Covenant cases which could be popular would not be covered by sigagg

Do covenants help this? A vault could hold up? But they don't care about fee savings, less than lightning users perhaps. COuld end with two classes of tx which don't mix well together, which would be unfortunate. We envision more script changes than signature changes.

## Halfagg at the block level

Could run into problems like MW cut-through at relay time (a + b + c works but a+b and b+c don't) but we should just not do something like that

Run into MW problems, talking about block-level half agg now.

During re-orgs we could not separate the signatures again; would need to save them. Notes in the half agg repo describe this interesting Q more.

## Reorg issues

No proposed solution at the moment except keeping the signatures around for a while

Validators at the tip dont get the benefits (at block level)

Block-wide stuff is very future anyway, from one PoV half-agg works, and we can use it now if we wanted. But should we spend time coming up with a full agg proof? Do people want this.

lets say miner does the aggregation, only people who save bandwidth are blocksonly. But for half agg at the tx level, everyone saves. But at the block level, doesn't save any bandwidth. Let's stick to tx-level for now.

What would happen if you didn't commit to the s-values with the tx? No clear answer on this point…

Who is willing to spend time on it? One hand raised.

One Coinjoin implementation is interested, and half agg can make a coinjoined tx cheaper than a non-coinjoined one, and give you more plausible deniability – I coinjoined because it's cheaper! And full agg possible for coinjoins, as it's already interactive.

Full agg is stateful, and has terrible security proof, which is why it's less considered. If you see a fully aggregated tx, you must infer that all inputs belong to the same person. So you make privacy worse.

When more than 1 person in the tx, there's interactivity involved, but pushback on doing full agg as it increased the number of rounds.

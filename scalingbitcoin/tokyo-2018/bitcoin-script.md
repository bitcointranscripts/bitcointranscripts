---
title: The evolution of bitcoin scripting
transcript_by: Bryan Bishop
tags:
  - scripts-addresses
  - op_checksigfromstack
speakers:
  - Olaoluwa Osuntokun
---
## Agenda

* opcodes
* OP\_CHECKSIGFROMSTACK
* sighash flags
* keytree sigs
* MAST
* graftroot, taproot
* covenants, reverse covenants (input restrictions: this input has to be spent with tihs other input, or can only be spent if this other one doesn't exist)
* stack manipulation
* script languages (simplicity)
* tx formats, serialization? what would we change with hard-fork changes to the transaction format? Segwit transaction encoding format sucks; the witnesses are at the end and inline with all the scriptsigs and that should be changed.
* new signatures
* merklebranchverify
* 2019 soft-forks
* restrictive endorsement (jrubin)
* signed sequence numbers, signed sequence commitments

## Restrictive endorsements

OP\_CODESEPERATOR ... you might not need codesep for this. Basically, in the old bitcoin, pre-segwit tx, you could add arbitrary computation into your scriptsig. That will affect the second signature that comes on. This is a thing that used to be possible in bitcoin and has some interesting use cases where you want to say this signature is signed but I'm adding a new hashlock on it, and then you sign a new hashlock and if you don't get that then.... my script is specifying everything in the input? Recursive segwit, kind of. When you add your signature and sign all your signatures you've seen, then you could add one another script to verify against that. It's another condition you want to have checked. You could add in your scriptsig to hash something, then make an invalid signature by signing something that says 1 == 2  or 1 2 OP\_EQUALVERIFY and that would be an invalid signature. This would be useful for signing something and putting a hash preimage in it and the signature is now restricted. It's specifying additional constraints in the scriptsig. Dispatching is similar to graftroot in some situations.

You could encumber it with a special key under certain conditions that wouldn't require someone to create some non-standard pubkey because then if we see that transaction on the network then we know they are trying to take money out of our.... it would be non-standard of course.

OP\_EVAL was an alternative to p2sh. With p2sh, you use canonical pushes.

jl: I'm doing signatures in a semi-honest model and if they are in a semi-honest model, and semi-honest in the sense that if you finish the signature with your other participants then you haven't leaked the data, and if you fail to finish the signature then your keys get leaked. If you're signing a restrictive endorsement then you would put a new hash preimage, add one more round, then reveal that hash and lets you convert something in the semi-honest model into the non-honest model because you have one more thing. I can add an escape clause in multisig that you didn't know about.

## OP\_CHECKSIGFROMSTACK

CHECKSIGFROMSTACK is something where you can check a signature on the stack. This lets you push signatures to the stack, and then check that it verifies. The cool thing is that you can do cool things, like create a new type of lightning channel similar to eltoo but better. You can do oracles, like based on known pubkeys. You could also delegation, like a key in a script and I can sign any of your keys and then you can check the checksig after that.

You could do covenants with this. You could do probabilistic payments. You could have a protocol where there's a random number, you send it to me, I sign it, you reveal it to me, we XOR it, and one of us wins. You want to stop me from double spending a ticket. This is cool because you can do things like a patreon thing, like a mutual assurance contract. You could do a bunch of cool things with that. I think orchid is doing something like that? They use vpn with probabilistic payment to pay for channels.

Schnorr threshold signatures with OP\_CHECKSIGFROMSTACK would allow k-of-n multisig federations.

You could also do blinding with OP\_CHECKSIGFROMSTACK.

You could give a minimal elliptic curve library.... if you could add and multiply keys in script, then you could do some really sick stuff. You could do signature verification input, three or four operations. If you had  addition, scalar, and double scalar mul, and maybe inverse, then you could do some interesting stuff. Then we can make our own parity-terrible multisig contracts.

You could do sigop counting... we have this weighted thing with segwit. Weight is probably not as ideal as cost...  We don't really do hashes in this.

You can't do unconfirmed spends in zcash; you can't specify an intermediate accumulator state. If you did, then you could break the anonymity set. Scripting is inherently limited then. There's no hop-chain nested transactions, and it's only 2-of-2. They didn't think about nested spends.

OP\_CHECKSIGFROMSTACK with OP\_CAT gives you covenants.

## secq

This isn't secp256k1, it's secq256k1. This is related to bulletproofs. The idea of secq is that you have this cycle between secp and secq. The group has a particular order, and on secq it's reversed. You have a private key, multiply it by your generator, you have an element in the group. That element in the same group has the same size as the field in the other group. You could have a STARK or SNARK that can verify another SNARK circuit. We can verify secp and secq in bulletproofs.  You can have a signature over a message for a public key. "Scalable cycles of zero-knowledge" and they found like one curve and it took a lot of computation to find that, and somehow secq popped out and had the proper properties. The equations are the same, too. You could do recursive STARKs.

Imagine you're doing a swap protocol, then as a part of it one party says he is going to prove to you that I have a signature that someone else gave me, I am going to give you a proof that I have this signature, and then they could put that into one of their transactions and say here's the proof that they have the signature. This would enable a lot of weird protocols.

You could also prove that a private key was generated in a certain way, and then you could verify that.

## Signed sequence commitments or signed sequence numbers

It's still replace-by-version, but you do CHECKSIGFROMSTACK to sign the versions.

Now on to a new commitment invalidation method. This is something I call signed sequence commitments. Rather than now us using this revocation model, what we do is every single state has a state number. We then commit to that state number, and then we sign the commitment. That signed commitment goes into the script itself. This is cool because we have this random number R so when you're looking at the script you don't know which state we're on. To do revocation, we could say, if you can open this commitment itself and because it's signed you can't forge it because it's a 2-of-2 multisig, so we can open the commitment and then show me another commitment with an R sequence value that is greater than the one in this commitment and that means that there was some point in history where two of you cooperated but then one of the counterparties went back to this prior state and tried to cheat. So this is a little bit of a simpler construction. We have a signed sequence number, you can prove a new sequence number, and we can prove it because we hide the state of it, because it can be the case that when we go to the chain we don't necessarily want to reveal how many state updates we've actually done.

Signing is pretty simple: you have this number R which we can derive from some deterministic method. We increment the state number. We have c, which is the commitment. The signature is important, it's actually an aggregate signature. It's the signature between both of us. There's a few techniques for this, like two-party ECDSA multiparty computation techniques, there's some signature aggregation stuff you could do, just somehow you collaborate and make a signature and it works.

One cool part of this is that whenever I have state 10, I don't need the prior states anymore. I don't need any of the other extraneous states. 10 is greater than 9 and all the prior states. I now have constant client storage which is really cool. So we can have a million different states but I only need to keep the latest and this tuple thing with the signature, the commitment, opening the new commitment itself. That's pretty cool because now outsourcers have constant-sized state per client. Before, it would grow by some factor the size of the history, but now it's constant in this scheme, which is a pretty big deal. It's also simpler in terms of key derivation, the script, things like that. We're just checking a signature.

There's a state machine in BOLT 2 where you update the channel state, but that doesn't need to be changed to implement signed sequence commitments. We've dramatically simplified the state. The cool thing is that, because the state is symmetric now in mutiparty channels there's no longer this combinatorial blowup of knowing or tracking who has published and what was their state number when I published and who spent from... it's just, it's way simpler to do signed sequence commitments.

You use OP\_CSV to ensure you are always spending with a higher value. But with signed sequence commitments, we have a hash of the state number. SO it's h(state number || P). You create an opening to the commitment itself, you parse out the number, then you could verify the signature of the key itself. You could have a CSV delay.

You could use 2-of-2 ECDSA, CHECKSIGFROMSTACK or Schnorr to produce a signature under that number itself. This is pretty cool. The average transaction in eltoo can't use a locktime. This can use locktime. Once you can sign arbitrary messages, you can have structured constraints or constructions on what the message is itself. In this case, it's a sequence number, it could be a bunch of other things as well.

## Sighash flag stuff

bip118 SIGHASH\_NOINPUT is coming up lately. You can't chain transactions if the original transaction has its txid change; but if you don't have to specify the txid with SIGHASH\_NOINPUT, then your latest transaction can still be valid. You need application-specific key pairs only used for the purpose of SIGHASH\_NOINPUT. The sighash would otherwise include the previous input that you were trying to spend. So SIGHASH\_NOINPUT only signs the script; there's an output out there that satisfies this witness, and that's really powerful.

You can use this for fee bumping.. if you want to add a fee, you can do RBF or CPFP. But with SIGHASH\_NOINPUT, you can add new inputs and outputs and can do anyonecanpay and you can add your own fee input and move it forward once you attach it.

Other sighash flags-- jl2012 had some ideas about choose your own sighash. If it doesn't cover the scripts, then you can spend to a key that doesn't exist. You can pre-sign a transaction and then spend to that transaction, and then get the key using ECDSA pubkey recovery. You don't have the private key, so it's a transaction that can only spend to that. It allows you to do finite covenants. Tadge was talking about this too. It was pre-2015. Should we include the script or not? What happens when we don't? Then this weird things happen. Should you include the value? Arguably no, so that it can be as flexible as possible. Or it should be optional. SIGHASH\_NOINPUT doesn't include the value right now in the proposal.

If you don't sign the value, then it becomes mutable. The value can be changed. This could be useful for like a lottery. Miners can't steal fee here because they are not signing the input value, you're signing the output value.

Blockstream implemented the bitmask sighash flags for Liquid.

For SIGHASH\_NOINPUT, use "application-speicifc keypairs". If you don't know what you're doing, then sorry for your loss.

You can do restrictive endorsements with this too. You can dynamically specify later dynamic set of signers, then later check in the input which of the scripts. Pick whatever inputs you want from my set of these, and then use that to go pick one of them. In the script, you could restrict which inputs you're spending. If you have NOINPUT, then you produce the signature specifying that it is one of these 10 in that slot, then someone else specifies it's one of those 10, then it limits the transaction to only the intersection of those inputs which gives it some interesting new properties for replay protection and lottery protocols. You've signed 100 transactions with just 2 signatures.

Also in sighash flags, being able to fully merkleize a transaction so that you can expose a small part of it. It wouldn't effect the txid, but it would effect the wtxid or whatever you would use to sign. But you could say, merkleize the outputs so that you can show one of the outputs is going to be the one you asked for. This would allow you to do blinding without additional crypto.

Merkleized txid stuff was considered for segwit but there was some patent or something that threw them off? In coinjoin things like 100-of-100, you could do the entire thing, it would be interesting to show this script was included in the chain and that's all you need to know. Maybe we can still do it?

With NOINPUT, you could-- spends from outputs... it only matters when you're spending. What you would do is say this is an address, any time funds get spent to that address, here's a redemption path that goes to some other destination. NOINPUT is not replay safe, they are automatically playable by anyone in the network. It requires a second transaction - wihch a lot of exchanges do anyway. That NOINPUT already exists in the chain because the availability is that as long as you have the blockchain you have that NOINPUT, so it's a forwarding address. Then maybe you can deactivate it through something with time, and maybe only reveal it if you want to keep that one fresh, then you throw them away when you have a new redemption path and that will still be just as good. This lets you emulate some account-like features. It's good for lightning or eltoo because it gets much closer to how lightning is being imploemented for account-based models where you use sequence numbers. You don't sign the output value, it's a complete forward to the new address.

We should have a way of committing fee, and have something where the amount to an output is not signed so that you can say anything that is not in the committed fee goes to the "default" output. Now you have explicit fees. You're signing the fees. An output that is the default; the last output receives anything above that fee amount. This allows you to have a forwarding address based on NOINPUT. Always send any incoming funds to the new address. Would also help with watchtower stuff; if the output value is signed, you could in theory have a single NOINPUT signature that covers all of them, and need a single signature for all the watchtower storage, but they all have different output values, you can't really do that - but if you do that more explicitly then maybe that's explicit.

Explicit fee could be a 2019 soft-fork.

## Stack manipulation

What does everyone think about in a new segwit version doing an append-only stack and then pointer regressive stuff? You could just jump address wise in the stack? No, stacks are harder to analyze. This is the witness, I'm pulling out the 5th thing in the witness data.

You could use the altstack for tree traversal in the tree itself, so you go down, add them, push it on the altstack, push down to the altstack, go to the root of that. I think merklebranchverify is related to this. There's two versions-- one is interpretative, one is more like a type of address. roconnor and maaku are disagreeing about this. We could have made a new merkle tree format, make a new compression function.

You could do interesting things with merklebranchverify and checksigfromstack. Something like that getting in would be useful, and would be helpful for cross-chain stuff as well. You could do OP\_ZCASH.

Should we break up MBV.. or do you just like have a general version of it? Is it specific for each type of merkle branch you want to verify? Do we need two versions of MBV? Are htey behind script versions? That's a big nebulous area. Is it one big sigop? Or is this a DoS vector? Should we have an OP\_DOEVERYTHING and OP\_EVAL, or should we have very specific templates?  Most programming languages are like that meme "why not both?" and they will go and do both. Satoshi disabled so many opcodes, and tried to hide that. He clearly was testing stuff that he didn't understand.

An example where it breaks down in merklebranchverify... should you be able to extract multiple elements from merklebranchverify? If it just does one thing case, it's really hard to amortize that proof. That's where MAST protocol doesn't let you do pulling multiple things out, it's just pull whatever set of keys you want and check at least a few of them. Merklebranchverify is an example where you have to go on the complicated side, not just extracting its own little branch. It's more like a union script, it's 1-of-n. The generalized case is more like "permissionless innovation". Who decides which one of these- which path we should go down?

## DoS vulnerabilities in new opcodes

We need a new fuzzer and randomize the script you're producing, fuzz it, and see what causes a crash and research the memory, sigop count, and so on. Nobody has made one, that would be kind of cool for cross-implementation testing. This would find some random bugs that haven't been found yet.

Bitcoin script is really complicated. It's not strictly interpreted; it's parsed somehow, and then interpreted. Think about OP\_IF then OP\_PUSHDATA and then an ELSE branch... there's weird stuff there. The way branches are handled are weird. The way conditionals are handled is weird. It's written in a way we can reason about, but that's not how they work.

## Merkleized abstract syntax tree (MAST)

Taproot and graftroot gives you MAST. You might still want a MAST construct, because MAST inside taproot is very useful. They compose. Taproot is the probably the thing you do first because it has a bigger impact, but then you still want a MAST mechanism for other reasons. With MAST, you get a merkleized script. MAST seems way more powerful than just 1-of-n scripts. I thought it would be like branches with multiplication and addition or something, and other operations, not just hiding different multisig situations.

BLS signatures would be killers. Non-interactive signature aggregation and cross-transaction and cross-block aggregation. I think someone is working on a BIP with that, for some new curve or something. They released a BLS library. The risk to introduce new signatures is pretty low; you opt-in to it, so you take on that risk of the new signature scheme. If you do a MAST, then you don't even need to reveal what that key is, and if the other keys break then you could go to ECDSA if the other schemes are broken, as long as it's already in your MAST.

## New languages

Simplicity? Ivy?

## RSA

There's something like CL signatures.. it's a proof of a signature on a committed value. They are based on RSA too. At some point Satoshi used RSA-512 and then he realized that's dumb. Unfortunately there's a high computation cost for RSA signature verification. zcash has this thing where they track the worst case block they can produce... they had a fix for quadratic hashing.

## Fun with blinding

Before tumblebit, it was blind signature verification on script itself. Jonas Nick has a few things, like ecash things. Any protocol where you're doing an exchange. Oleg had a thing a while back where he had a protocol with multisig where you have someone sign a transaction on your behalf but they wouldn't know what it was. You could have blinded multisig where you trust them to do a signature but you don't know what you're signing.

## 2019 soft-forks

Schnorr, new segwit version, SIGHASH\_NOINPUT, and OP\_CHECKSIGFROMSTACK. These two are relatively small in line diff. Maybe activate late 2019, early 2020. We haven't tested the waters since the last drama. Schnorr is more straightforward to do than NOINPUT. In terms of the behavior of the system changing, Schnorr changes the behaviorf of the system relatively minimally, and NOINPUT introduces tons of new functionality. In terms of review, it's easier to review NOINPUT. These two opcodes offer a lot of fungibility risk unfortunately. It's not just "don't accept those coins" but think about getting paid or a normal economy or think about where your dollars came from; every dollar is covered with cocaine, and eventually you're mixed with everything. That's the fungibility problem: if you have a weird condition, then your coins are going to be imposed by those conditions whether in a reorg or something. I'm personally okay with that but folks like Greg are vehemently opposed to that. It's like, buy coinbase outputs at that point. It's very old coinbase outputs that are non-fungible because they are worth a lot more than other coins that are spent in any other transaction.  It depends on how binding the covenants are. There would be a market for virgin unencumbered coins at this point.

The low-s soft-fork... that one cannot be done. That's impossible, that's a hard-fork. That could break coins. That's an absolute no. Any transaction ever created that is valid, is still valid, except for the hard-fork to remove OP\_XOR or whatever.

What are the smallest tiniest soft-forks you could do to test the waters?

The only people who have comfort with soft-forks are unlikely to propose a soft-fork and produce software that would be adopted. People are going to fight anything that adds anything, especially considering the recent CVE. People are going to be for the next 6 months significantly more conservative. It's going to be another 6 months before people are even thinking about it. I don't think we're going to get any new soft-forks in the next year.

Fixing timewarp as a soft-fork could get done in 2019. There could be consensus to do that. But should we? Timewarp bug existing might be okay. And maaku has found some interesting things in there to do with that.

Explicit fee could be a 2019 soft-fork.

## Sidechains

I would prefer sidechains with miners instead of federated multisig. Otherwise you're going to have frozen keys or confiscation. Once you have sidechains, then you're done and don't need further upgrades. Anything cool can go into new sidechains. Paul Sztorc has his recent drivechains, there's RSK, then there's Elements and the federated multisig approach.

The custodial agents could be a separate federation from whatever the implementation of the transaction validation federation. There's some flexibility that might be possible here.

With the Sztorc stuff the withdrawals take multiple months, you could rescue coins with UASF in the event of a failure. UASF is the rescue plan, but the bitcoin users have to agree and do it. And they have to understand the nature of the dispute and have to do it timely; is it likely? or will it enforce a trend of miners doing nasty things? The idea of a sidechain was that it was supposed to be isolated.

## OP\_PUSHTXDATA

OP\_PUSHTXDATA was jl2012. You can push transactions into the stack. You can do opcodes to verify that, you can do vaults and pattern match over the structure of the transaction itself, which allows for covenants. You can restrict what the inputs did, and also reverse covenants. Chain.com did the stack-based way which was really sick. They also had pattern matching on the inputs as well, but nobody used that. jl2012 has the stack-based ones specified pretty well and they are pretty ideal. Do you allow the transaction only, the block, multiple transactions, previous transactions, transaction chains, the entire chain?

## Languages

BitML compiles down to a set of transactions. It was a calculus bitcoin script, a functional language. You could specify like a revocation clause and a nested thing, like a second-level HTLC and it would output the entire transaction tree for you to sign. You could make a turing-complete bitcoin by turning bitcoin transactions into turing complete. The next step would be to take BitML and generate the daemon, output some protobufs, compile it into something, then boom you have a full-stack actual execution code of sets of bitcoin transactions.

Zero-knowledge protocols that get compiled to a set of bitcoin transactions based on knowledge exchange.

## Spork

Probabilistic soft-fork where instead of you doing versionbits, you say that if the blockhash has some additional PoW below some threshold, then it activates. Then if the miner doesn't want to activate the fork then they have to abandon their block. The cool thing is that if you set it to 6 months, you'll always have an expectation of 6 months, but it could happen at any time. You could set a minimum like at least 3 months, then you have an expectation of 6 months to get your shit together. Doing it live. You do actually want people to be ready to process those transactions before any known point. This is only for soft-forks, not hard-forks.

## Takeaways

Sigops are dumb. We need to somehow figure out a way to optimize that.

MAST and graftroot is dope. It's generally accepted as dope.

Covenants are also dope and maybe some simple soft-forks might come in 2019 but not holding our breath. Committed fees or maybe timewarp fix. Explicit fee falls under restricted endorsement. Should you commit to an explicit fee rate, or an explicit fee? In the case of watchtowers, if you have 10 possible inputs and any of them could be spent in any combinations, so you have n^n possibilities... so fee rate would be better, but explicit fee would be more difficult. But fee rate would have malleability problems, like if someone adds something to your witnesses which are very big, and witnesses are actually malleable. The revocation case for the HLTC commitment takes any and all data, as proposed by Nicolas Dorier. Someone could put tons of garbage there but it would make their fee per byte really small. This would reuqire them to intercept the transaction broadcast and then do their manipulation. Every input could specify the fee they agree to pay, so it would be fee isolation. If you guess too much fee or something, then you need a default output where all the excess fees must go to that output. If the fee becomes an explicit output, and the inputs and outputs don't add up, then where should the fee go? Should it go to the default output. The output could be implicit, it could be committed to, but not in the transaction-- this would be a hard-fork. It can go in the coinbase transaction, actually. If you make it so that it goes into the coinbase transaction outputs then that would be one way to make it work, and then you could get all the fresh coins you want, you could get fresh coins from the coinbase. 600000 is the blockheight for the activation of the explicit fee soft-fork. Or the next halvening. This could be 666666 and be the evil soft-fork.




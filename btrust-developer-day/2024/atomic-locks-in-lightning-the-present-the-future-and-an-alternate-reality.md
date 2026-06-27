---
title: 'Atomic Locks in Lightning: The Present, the Future, and an Alternate Reality'
speakers:
  - Duncan Dean
date: '2025-04-23'
tags:
  - htlc
  - ptlc
  - adaptor-signatures
  - schnorr-signatures
  - privacy
  - lightning
categories:
  - conference
source_file: https://youtu.be/zYQLrgbOhqU
media: https://youtu.be/zYQLrgbOhqU
summary: Duncan Dean, a South African open-source developer and Btrust grantee working on the Lightning Development Kit (LDK), presents a three-part overview of atomic payment locking in Lightning — the current HTLC model with a detailed walk-through of the offered HTLC witness script and its timeout and preimage spending paths, the upcoming upgrade to Point Time-Locked Contracts (PTLCs) using Schnorr adaptor signatures that replace hash locks with public keys to eliminate payment correlation and the wormhole attack, and an alternative construction using non-interactive zero-knowledge proofs for anonymous multi-hop locks that preserves privacy without Schnorr but generates proofs in roughly 30 seconds per five-hop route and lacks a proof-of-payment mechanism.
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:00

Source lightning developer and a grantee of BritRoss, Mr Duncan Dinh.
Good morning.
Yes.
Good morning everyone.
So yeah, we're going to be talking about atomic locks in lightning.
We're going to see what we presently have, how they work, a brief overview.
We're going to introduce what's coming next, and then something that might be kind of under the radar, but maybe a little bit interesting, so I'll mention it anyway.
So first of all, I'm from South Africa, so second speaker representing the South.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah, I'm a BITRUST grantee, and for the past three years, I've been working on the Lightning Network, the Lightning Development Kit, so in the Lightning Network.
And I'm, so funny story behind my handle, it's at Dungsons on most platforms, so I started with my name and then I just mashed the keys on the keyboard to get the rest of it.
But yeah, so my website is dungson.dev, and you can get my blog there, where The stuff that's public is not the million things in draft kind of thing.
And apparently I like a lot of negative space.
I think I was supposed to put something there, but it's gone now.
So anyway, I already mentioned our goals, so I jumped ahead a bit.
So we're going to see what's presently enlightening, some of the drawbacks around atomic locks and payment routes, discussing PTLCs. So that's going to come up next, and different implementations.
And then, yeah, the last one is a surprise.
Cool.
So now we have hashed time-locked contracts.
You might see it in literature as hashed time lock contracts.
So I'll just call them HTLCs. I don't have any fire backtrack for this talk, so it's just going to be some slides.
So quite intimidating, but I thought we could go through a bit of an exercise.
So this is actually how the witness locking script looks for an offered HTLC output, so on a commitment transaction.
So this is the case of if you have a local node publishing a commitment transaction This is the locking script that you need to satisfy with each of the branches.
That's obviously that for the remote commitment transaction and the local commitment transaction we need to assign blame because of an LN penalty so that the counterparty can claim funds from a revoked commitment transaction.
So yeah, what I've done is a stack machine in a PDF.
So hopefully that goes well.
We almost get a stack overflow at one point.
So as the exercise, we're going to actually go through the timeout path.
So we are the local node, we've published the commitment transaction, and we now need to claim our funds back after timeout.
So how this would work is our witness to actually spend this path is above in the red.
So zero remote HTLC SIG, local HTLC SIG, and then we've got an empty witness element.
So that all gets pushed onto the stack, as you can see.
So zero up until the empty witness element.
So here we come along and we duplicate that empty witness element.
We take the hash 160 of that.
It gets pushed onto the stack.
Then we compare that to the hash 160 of the revocation pub key and they're going to be different when we check it with up equals, so we get false here.
So it looks kind of weird, like how you just start what we've pushed onto the stack before.
But it actually saves some space on chain.
So that equals less fees.
In this case, we're paid to witness script hash, so we don't have funny taproot spending paths and can't save there.
So we have to publish this whole script when spending.
But yeah, so we know that, OK, so when we get to this, we're not in the opf, because we were false.
So we get into op else.
So now that's what's remaining on the stack, is basically what we originally pushed on.
So We push on the remote HTLC pub key.
Then we swap the top two stack elements.
And then we calculate the stack size, the size of the empty witness element, which in this case is zero.
We push 32 onto the stack.
Almost.
OK, we're right at the top of the stack here.
And then up equal checks that 32 isn't equal to 0 the last time I checked.
So that should be false.
Pushed onto the stack.
And then again, it means that we're in the not if branch.
So what we're trying to spend from is this part, the to local node via HTLC timeout transaction.
The reason we have this second stage transaction is so that with ALIN penalty, with the HTLC, we need to time it out.
Within a certain amount of time, it's an absolute time lock.
So we need the local node to actually be able to spend that.
So if it's a revoked state, it's a absolute time lock.
So we need the local node to actually be able to spend that.
But then in the second stage transaction, we need to still have like a delayed output path for the local nodes so that the counterparty, if it is a revoked state, can go and claim those funds as well.
So yeah, carrying on here.
So we'll drop that empty element.
We don't need it anymore.
We'll push two onto the stack.
So this is the...
So here comes the object multisig at the end.
So the two represents the number of pubkeys that are in this multisig.
We're going to swap the top two elements.
We have remote HTLC pub key at the top.
Then we're going to add the local HTLC pub key.
And then This too means how many signatures we need, how many signatures we expect.
And then, yeah, so the order is quite important.
So the pubkey order must match the signature order, so local HTLC SIG and remote HTLC SIG.
Then object multi-SIG actually, it's an original bug that you have to have an extra element on the stack that it consumes.
And then later, that was changed to be more specific that it needs to always be 0.
So that's why we have the 0 at the bottom.
But you'll see after object multiseg consumes all those elements, pops all those elements of the stack.
And if these are valid signatures, then that'll evaluate to true.
Yeah.
And then this part is just related to anchors.
But it's, yeah, so it's Just check sequence verify that it has one confirmation, and then up drop.
Cool.
And then if that all validates, then we can spend to the second stage timeout HTLC transaction, which has an output that looks like this.
It's the same as a claiming transaction as well, if that also had a second stage.
Say the local node had a second stage as well.
So what This basically gives us is that the remote node can actually, if it's a revoked state, they can spend immediately from there.
Otherwise, the local node that's trying to time out the funds has to wait for that to self-delay check sequence verify.
All right, and still with offered HTLC output witness scripts, in this case, the Remote node can actually claim the funds from this branch with a pre-image immediately.
So they don't need to go through a second stage transaction.
They claim it with remote HTLC seg payment pre-image.
And it's just the other branch that we didn't take.
But we won't go through that.
Right, so this is just an example of a received HTLC output witness script.
So if we receive the witness script and we publish, So you can just see that the branches have pretty much changed.
So to remote node after timeout, that doesn't have a second stage transaction.
There's no multi-second there.
So that can be claimed immediately after the timeout.
Yeah, immediately after the timeout.
And we see that the pre-image part is also encumbered with a check multi-sig.
So that needs to go to a HTLC success transaction.
Yeah, so that's what that's pointing out.
And then in this case, you can just claim immediately.
So some of the most well-known drawbacks of HTLCs is since the same hash is used across a payment route, there's this correlation of those payments.
So the classic example is the wormhole attack.
So if you have at least two colluding nodes on a payment route, they can end up stealing the routing fees from hops between them without the knowledge of those hops.
So there's that, the fees they would have made are effectively, it will just time out and it's as if they never forwarded the transaction.
It's practically undetectable, so the sender wouldn't really know.
The recipient wouldn't know.
Stolen wouldn't know either.
So just a basic set up, so A wants to through M1, R, and M2.
So I've named them M1 for malicious one, malicious two, and then routing node in the middle.
So you'll set up your HTLCs. And then when B releases the preimage to claim, malicious node 2 will say, okay, yeah, let's settle that and pay you there.
But instead of rolling it back to the routing node, he says, OK, I take out my UNO skip card, And I'll just pass it to my friend out of band at M1.
So then what we have here is M1 can then unlock that HTLC with the sender.
And then we have these two locks that are still standing that will eventually expire.
Yeah, so it's as if the routing node never routed any payments.
Right, and apart from being malicious just in that way, A similar setup could be for just plain spying on the transactions happening on the network, using maybe some other information as well, but at least along the route, you know more information than you should about what path payment's taking.
So yeah, so a solution to this is anonymous multi-help locks.
So the anonymity here comes from each lock not being correlated.
So there are some solutions here, but we first need to take a bit of a detour to NOR signatures.
I'm going to try to be brief.
It's not completely self-contained, and we do make some assumptions.
But it's also interesting, because this is used in the next talk on silent payments.
So maybe that's helpful, too.
So yeah, Schnorr signatures.
So it's been standardized in BIP 340.
So if you want to get some more information on that, just consult the BIPs. So we still use the same curve, secp256k1, same curve parameters.
Private and public key generation remain the same as for eCDSA, So that's what it effectively means as well.
So it is simpler, and it has some advantages compared to ECDSA.
And the whole reason for ECDSA was to tweak it enough to not violate the patent of Schnorr, which I think expired in 2010 or so and that's why you know and it also wasn't standardized and Yeah, so it took a while to get into Bitcoin, but with the taproot upgrade it did So some of the advantages so it has a nice linearity property, you know adding signatures you can do some fun magic, but you've got to be careful to run into some slight gotchas.
It has a nice provable security with stronger properties than ECDSA under weaker assumptions.
So yeah, that's also nice to have.
And by default, it's non-malleable by a third party.
Yeah, so at least like in Bitcoin today, you know, signature malleability, you know, by adding the after seg words, it's not so much of an issue anymore.
But it's nice just to have it natively in the signature scheme.
Yeah, so brief overview of Schnorr signatures here.
So I've used SK for secret key, that's your private key.
G, that's the generator point for say P256K1.
We use that to then generate public keys.
So you just take your secret key multiplied by the generator point, or well, in this notation, at least, where the group operation is addition.
So yeah, then you'll get your public key out.
And going in the reverse way, there's discrete log problems.
So it's a hard problem that we generally say is not computationally possible.
So that's where the whole security comes from as well.
For signing, there's some cases where, depending on if the points you generate is odd, You have to go and negate the scalar that you use.
I just assumed that everything works out here, but you can see about 344 details.
So K will be like a random nonce for signing.
Capital R is your nonce point, so it's just the same as a public key, you just multiply by G.
And then S is K plus a hash.
You can read up about tagged hashes in BIP 340.
But yeah, tagged hash of RPM, so M will generally be like transaction or whatever, but this is general signing.
And then multiply it by SK, And then the signature is, well, it's actually like you can just take the x value of your r point and then that signature, and then that s value, and then it ends up being like 64 bytes.
So it's always 64 bytes.
And then for verifying, you just check that what you receive there, because you're receiving R and small s, you take small s, multiply it by the generator points, And then you just check that that equality holds to be satisfied.
So that brings us into signature adapters.
One of the magic things you can do with Schnorr.
You can also do it with ECDSA, but It's a little harder.
So for signature adapters, it's an instance of a scriptless script.
So using signatures to avoid doing explicit script stuff on chain.
So we commit to a hidden value.
So it's also like creating a public key.
So you just choose a random small T, multiply it by the generator points.
You get an adapter.
So Your T is called your adapter secret, and then large T is called your adapter.
So you can just think of it like secret key, public key again.
And it's more private than hash locks.
Okay, well, it's a little disclaimer, but we'll get to that.
Because they look like regular signatures on chain.
Right.
So this is a very contrived example of using a signature adapter as a lock.
We'll discuss why it's insecure.
So B is the recipient.
A is the sender again.
So B generates the adapter using a randomly chosen adapter secret and then sends that to A.
So this would be through your invoice, or the normal way in Lightning.
So you'll scan the invoice.
You'll get T.
So A has T.
And then what A does is, so A has a secret key.
So secret is K sub A.
And an ounce, r sub a, and can generate the points corresponding to those.
So public key, capital P, yeah, sub a.
And it can basically generate this thing that almost looks like a signature, but not quite because we're missing that scaler, that adapter secret.
So to add onto the front.
So this won't validate.
You can see why.
A eventually needs to learn small t or whatever as well in order to make this a valid signature.
But then A sends this S prime, which is almost a signature, and the nonce points to B.
So with that knowledge, B has knowledge of the adapter secret, can just add it to S prime and then this actually becomes a valid signature, a valid Schnorr signature.
Right?
You can verify it.
Okay.
It's valid.
So if A created a lock in this way that S could create a signature that can spend correctly, it would be insecure.
Because just by publishing that signature, A can go and compute small t, because if you just look at the top there, if you just put, you know, So A knows S prime, so it would be, yeah, so S prime is equal to S minus T.
And, oh no, yeah, yeah, exactly.
S prime is equal to S minus T.
So from that up there, you could just compute small T.
So that's insecure.
We need some form of multi-party signatures.
We did see it before, kind of with the second stage HTLC transactions.
So for two-party contracts for Lightning, so there are two ways of doing signature adapters.
We have single sign-in adapters, which will be you'll have one signature, which is your local completed signature.
So That first looks like that weird signature we had at the top here.
And then after you add the small t, it becomes that completed signature.
And then we'll have an object sig verify.
And then we'll have a remote SIG that actually makes sure it locks that output to the intended recipient.
And then we'll have an object SIG there.
And then the other way of doing it is using muSIG2, which is also possible now because of Schnorr.
With the 2 of 2 adapter, one of these signatures will be the local completed partial sig, and then the other will just be the remote partial sig.
There are some differences between these two implementations.
So for a single signer, so we'll do it in the context of tap roots.
I'll give a slight aside on that.
The single signer side, So it would need to be in a tap leaf script, because we have this explicit script there.
It's not just a signature.
And on the music 2 implementation, you can use the key path of a tap route output.
And then the on-chain spin, so the single signer is more costly, because it is, you know, you're spinning a tap leaf as well, so you've got the control block and, you know, the rest of that.
MuSig2 on the key path would be less costly.
So the chain fingerprints, single signer, it does reveal the two parties, public keys as well.
And it does reveal, like, you know, the actual construct.
For Music 2, it at least hides that.
It looks like a plain single SIG on chain.
But for interaction, actually, single signer saves about half a round trip time.
And this is because in the Music 2 implementation, you need the remote partial sig before sending your local partial SIG on onwards.
And that's to make sure that you can actually unlock if you're the local side.
So getting into more detail about point time locked contracts.
So if we compare them to HTLCs, which we currently have in the Lightning Network, so HTLCs are locked by your hash digest.
So you need to present a pre-image to basically unlock that.
So that's the commitment there.
PTLCs are just locked as regular public keys, actually.
So yeah, so you're providing a signature in that case.
So route privacy HTLCs, there's that correlation, because it's the same hash digest as you go along.
PTLCs are uncorrelated, as we'll see in a few slides, or the next slide.
Chain fingerprints, HTLCs, I mean, I guess even with taproot, it's kind of obvious how you need to unlock it.
And PTLCs, it's not obvious, but for the music 2 case.
So yeah, a quick aside on taproot spending paths.
So you'll have this output key, which is actually what appears in your taproot output.
Output, but that's the addition of your internal public key and the tap tree spending part.
So you've got the hash tap tweak, which is a tagged hash as well.
P is your internal public key, and then you concat your Merkle root there.
And then that's the tree.
And then the leaves of the tree are your actual scripts that you'll use.
So you'll see in this kind of setup, so it's similar to if you look at a tree of transaction hashes and how that's hashed up to a root.
If you want to prove that it's within a block, you can just provide the intermediate hashes along the way.
So it's similar to that when you're spending.
You can prove that that script was part of that tree.
And you don't need to reveal the rest.
So everything in a separate tap leaf doesn't, you only need to reveal one of them on chain.
Okay, so like if we had to make HTLCs tap rooty, so in this case the offered HTLC compared to what we saw before.
One way of doing it, you'll find these actually in tbest's taproot notes.
Internal pubkey, We could use that for the revocation key.
So you'd have a revocation pub key and then remote pub key.
So we could use that remote pub key, just make sure that it's tied to the remotes as well.
In the tapleaf1, so one of the scripts could be spending to the time locked HTLC timeouts transaction.
Yeah, so it's the same script, just putting it within tapleaf1.
And then tapleaf2 could be your preimage claim, if you actually know the preimage.
So that's only if it goes on chain.
If everything's fine, it's off chain.
And then for PTLCs, something similar, so revocation in the internal pubkey.
It's going to be a they both pay to taproot outputs Tap leaf one would be now this also like a time-locked transaction.
So it looks pretty much exactly the same as for HTLC.
But then we have the difference here for spending to a PTLC success transaction by revealing the local PTLC SIG.
So yeah.
Making payments with PTLCs. So similarly to HTLCs, we're sending some sort of commitment across via an invoice.
It's out of band.
We have D generating.
So this would be like your adapter.
So small z is a random scalar value multiplied by G.
Then we send the points that it generates.
We send it to A, the sender.
And then A will go and randomly select y sub a to y sub c to generate the lock.
So at each hop, they're going to have a left lock.
They're going to know the scalar value, and then they're going to have a right lock.
Except for D.
D will just have the left lock.
Right.
So these are the locks that each node actually ends up knowing about.
So this happens during the setup phase.
So A obviously wants to know the secret to Z.
So it has that as the left block.
And then basically what's happening here is you're consecutively adding those y sub a to y sub b's so that when it gets to d, d can actually, with knowledge of z, has y a plus y b plus y c.
And with knowledge of z, it can start unlocking through to A.
And then all you need to know here is that the locks are uncorrelated as well.
And then in the update phase, so for signature adapters, we need to introduce a PTLC success transaction.
So it doesn't matter if, whether it's local or remote publishing the state, that's because now we require a signature.
So yeah, that's where that signature will be used.
Just going to think we have time for this.
Right.
OK, settlement phase.
Yeah, so it's all these pre-signatures.
The same sort of thing we did with the simple case of just subtracting them.
Don't worry too much about the details.
I think we can carry on here.
So this is one alternative if we didn't have something like signature adapters in Bitcoin.
I guess if we didn't have Schnorr, maybe we'd put in the effort to go forward with the ECDSA signature adapters.
It's a bit more work.
There were also some proposals to do that in a way that, you know, it is possible to mix them as well.
So once you've, you know, before Schnorr was introduced, we could have already had ECDSA signatures and then later made them still compatible, sorry, ECDSA adapters, and later still made them compatible with Schnorr-based adapters.
But there was a lot of work involved there, and it was just probably easier to just wait for Schnorr signatures.
So this is more of an aside, something that could be possible in the future, but it's probably not worth the effort because it has a few drawbacks.
So zero knowledge, anonymous multi-hop locks.
So I think maybe the strongest sort of proposal, concrete proposal of this comes from this paper, so Practical Anonymous Multi-Hot Blocks for Lightning Network Compatible Payment Channel.
Yeah, networks, networks twice, from 2022.
Okay, yeah, so here's a wall of text and not a stack to go through.
But so these actually use like non-interactive zero-knowledge proofs, which we'll discuss the non-interactive part, but zero-knowledge proofs allow a prover to convince a verifier of that proof that some statement is true without revealing any other information.
But it's a bit stronger than that because it's like if I say I want to prove that I know this private key, well I could just create a signature for you.
But then that signature itself is providing a little bit more information because it's saying it's something you can pass around that is kind of, you can convince anybody else that that person also has a private key with that signature.
So zero knowledge proof, the verifier can't actually go and convince a third party of the truth of that actual proof.
But yeah, it's just a side note.
So With the non-interactivity part, you can save on round-trip time, which is good for Lightning because you send that full onion ahead of time for the setup phase.
So that's pretty important for compatibility with Lightning.
The locks are actually hash locks, but they have different pre-images.
So this is where the proof comes in.
So the different pre-images are generated by the payer iteratively for each hop.
So they're also referred to as partial keys, which they're sent to each hop in the routes and only the payee would know the full partial key now This works definitely so it's more like a key send payment so it's not locked by some commitment from the recipient.
So as far as I know, there's no, you know, in the whole paper, I think it's just, it's related to a key send style payment.
Yeah, So the zero knowledge proof is actually required so that you can prove to each hop that if their right lock is unlocked, they'll be able to unlock their left lock without revealing what those pre-images are.
And it's a bit, you know, it's not computationally trivial.
So for a five-hop route, to generate the proofs takes around 30 seconds, so yeah, that's, you know, it's quite long.
But one thing is you can do it ahead of time without knowing who you're paying, or, you know, you can generate a whole bunch of proofs and maybe a different number of hops and that kind of thing.
But it may be not so practical as the paper suggests as well.
But verification is at least fast.
As I said, they're key send style, if I understand correctly.
So there's no out of band commitment from the payee before setting it up, which might be bad, because in PTLC context, that adapter point, that small z, you can actually use as a proof of payments.
So in this case, you don't get that.
And also, because of this as well, a malicious payer can help intermediate hops actually release their left locks before their right locks are released.
Like, the atomicity is still atomic.
It's still preserved, because you'll just have that eventual timeout as well.
But that relationship anonymity is not preserved.
Yeah.
So pretty much, that's the end.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
Yeah.
And then one thing I just wanted to mention is there will be I meant to have the blog post up that was more self-contained because unfortunately I couldn't self-contain everything in here and but it should be more detailed.
I'll let you know when it comes out.
You can follow me on my socials.
Cool, thanks.
You can follow him on his socials.
A round of applause for Danston, ladies and gentlemen.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Awesome, awesome.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you, DJ.
Thank you.
We're going from talking about wormholes to anonymous multi-hops.

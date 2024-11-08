---
title: ANYPREVOUT, MPP, Mitigating LN Attacks
transcript_by: Stephan Livera
speakers:
  - Christian Decker
date: 2020-08-13
media: https://stephanlivera.com/download-episode/2396/200.mp3
---
podcast: https://stephanlivera.com/episode/200/

Stephan Livera:

Christian welcome back to the show.

Christian Decker:

Hey, Stephan, thanks for having me

Stephan Livera:

Wanted to chat with you about a bunch of stuff that you’ve been doing. We’ve got a couple of things that I was really interested to chat with you about ANYPREVOUT, MPP, lightning attacks. What’s the latest with lightning network. But yeah, let’s start with a little bit around ANYPREVOUT. So I see that yourself and AJ towns just recently did an update and I think AJ Towns just did an email to the mailing list saying, okay, here’s the update to ANYPREVOUT, do you want to just give us a little bit of background? What motivated this recent update?

Christian Decker:

Yeah. So when I wrote up the no input BIP it was basically just a bare bones proposal that did not consider or take into consideration Taproot at all simply because we didn’t know as much about taproot as we do now. And so what I did for no input, BIP118 was basically to have a minimal working solution that we could use to then implement eltoo on top and a number of other proposals, but we didn’t integrate it with taproot simply because that wasn’t at a stage where we could use it as a solid foundation yet since then that has changed. And then AJ went ahead and did the dirty work of actually integrating the two proposals with with each other. And so that’s where ANYPREVOUT and ANYPREVOUTANYSCRIPT, the two variants, came out and now it’s very nicely integrated with the Taproot system.

Christian Decker:

And once Taproot goes live, we can, we can deploy ANYPREVOUT directly without without a lot of adaption that that has to happen. So that’s definitely a good, a good change. And so ANYPREVOUT basically supersedes the no input proposal, which sort of was a bit of a misnomer. And so using ANYPREVOUT, we get the effects that we want to have for eltoo and some other protocols and have them nicely integrated with Taproot and can propose them to once Taproot is merged.

Stephan Livera:

Let’s just talk a little bit about the background then what’s for the listeners who aren’t familiar, what is eltoo, why do we want that as opposed to the current model of lightning network?

Christian Decker:

So, eltoo is a proposal that we came up with about two years ago. Now it’s been two years already, and it basically is an alternative update mechanism for lightning. So in lightning, we use what’s called an update mechanism to basically go from one state to the next one and make sure that the old state is not enforceable. So if we take an example and we, you and I, Stephan have a channel open with $10 on your side. The initial state basically reflects this $10 go to Stephan and zero go to Christian. Now if we do any sort of transfer be it a, some payment that we are forwarding over this channel, or a direct payment that we want to have between the two of us, then we need to update this state and let’s say you send me $1.

Christian Decker:

Then the new state becomes $9 to Stephan and $1 to Christian, but we also need to make sure that the old state cannot be enforced anymore. So you couldn’t go back and basically say, Hey, I own 10 out of 10 dollars on this contract, but instead I need to have the option of saying, Oh, wait, that’s outdated. Please use this version instead. And so what eltoo does is it basically does exactly that we create a transaction that reflects our current state. We have a mechanism to activate that state, and we have a mechanism to override that state if if it turns out to be an old one, instead of the latest one. And, for this to be, be efficient, what we basically do is we say, okay, the newest state can be attached to any of the old States.

Christian Decker:

Traditionally this would would would be done by basically taking the signature and creating if there’s N old States n variants with N signatures, one for each of the of the binding to the old state and with the ANYPREVOUT or no input proposal, we basically may give have the possibility of having one transaction that can be bound to any of the previous state without having to resign. And that’s already the entire trick. We make one transaction applicable to multiple old States by leaving out the exact location from where we are spending. We leave out the UTXO reference that that we, that we’re spending when signing. And we can modify that later on without invalidating the signature.

Stephan Livera:

Let me replay my understanding there. So let’s say you and I set up the channel, and this is the current model of lightning. You and I set up a channel together. And what we’re doing is we’re putting a multisignature output onto the blockchain, and that is a 2 of 2. And then what we’re doing is we’re passing back and forward the new tates, the new to reflect the new output. So let’s say $10 to me and zero to you, or $9 to me, and $1 to you. And in the current model, if somebody tries to cheat the other party. So for example, let’s say I’m a scammer and I try to cheat you. And I tried to publish a Bitcoin transaction to the blockchain that I have, my, like the pre-signed commitment transaction that closes channel. Then the idea is your lightning node is going to be watching the chain and seeing, Oh, look, Stephan’s trying to cheat me, let me now do my penalty close transaction. And that would then in the current model, put all the $10 into your side. Right?

Christian Decker:

Exactly. So you basically have for any of my wrong actions, you have a custom tailored reaction to that. That basically punishes me and steals all of the funds or, well, it penalizes me by crediting you with all the funds, right? And that’s already, the exact issue that we’re facing is that these reactions have to be custom tailored to each and every possible misbehavior that I could do. Right. And so your set of retaliatory transactions basically grows with every time that we perform a state change. So we might have had 1 million states since since the beginning and for each of these 1 million, you have to have a tailored reaction that you can replay. If I end up publishing transaction 993, for example and this is, this is one of the core innovations that eltoo brings to the table is that you knew you no longer have this custom tailored transaction to each of the previous states. Instead you can, you can tailor it on the fly to match whatever I just did. And so you you do not have to keep an ever-growing set of retaliation transactions in your in your database or backed up somewhere, or at the ready.

Stephan Livera:

In terms of benefits that I can think of then. So it sort of softens the penalty model. So instead of one party cheating the other and then losing everything now, it’s more like if somebody publishes a wrong transaction or an old state, then the other party just publishes the most up to date one that they have. And as I understand from you, the other benefit here is like a scaling one that, you know, it might be easier for someone to now host watchtowers because it’s less computationally or less, maybe it’s like less hard drive usage. Right?

Christian Decker:

Exactly. So it’s definitely the case that it becomes less data intensive in the sense that the Watchtower, or even you yourself do not have to have to manage an ever-growing set of of transactions. And instead, all you do need to do is to have the latest transaction in your back pocket. And then you can react to whatever happens on chain. And that’s true for you as well as for watchtowers and watchtowers, therefore become really cheap because they basically just have to manage these 200 bytes of information. And when you give them any and you hand them a new transaction and you reaction they basically just throw out the old one and and keep the new one. The other effects

Christian Decker:

That you mentioned is that we basically now override the old state instead instead of using the old state, but then penalizing. And that has an really nice effect that what we basically do in the end is enforcing a state that that we agreed upon instead of enforcing, Oh this just went horribly wrong, and now I have to grab all of the money. So it changes a bit, the semantics of what we do towards we can only update the old state and not force an issue on the remote end then steal money from them. And that’s really important when it comes to, for example, backups with lightning, as it is today, backups are almost impossible to do because the because whenever you restore, you cannot be sure that it’s really the latest state.

Christian Decker:

And therefore if you, when you publish it, that it’s not going to be seen as a cheating attempt. Whereas with eltoo basically you can take any old state publish it. And the worst that can happen is that somebody else comes along and say, Hey, this is not the latest state, theres’s a newer one, here it is. And you might not get your desired state. Let’s say you want to take all 10 out of $10 from the channel, but you will still get the $9 out of 10 that you own in the latest state, because all I can do is override your your 10 go to Stephan with my nine, go to Stephan, and one go to Christian. And so we’ve reduced the the penalty for misbehavior in the network from basically being devastating and losing all of the funds to a more reasonable level where where we can say, okay at least I agreed to the state and it’s going to be a newer state that I agreed upon.

Christian Decker:

Right. And so I often and compare it to the difference between lightning penalty, being the death by beheading, whereas the whereas eltoo is a death by a thousand paper cuts because the the cost of misbehaving is is much reduced allowing us to get, to have working backups and have a lot of of nice properties that that we can probably talk about later, such as true multiparty channels with any number of participants. And that’s all due to the fact that we no longer insist on penalizing the misbehaving party, we now instead correct the effects that the misbehaving party wanted to trigger.

Stephan Livera:

Fantastic. And so from your paper, the eltoo paper it mentions this idea, it says, you know, it introduces the idea of state numbers and on chain enforcible variant of sequence numbers. So can you just talk to us a little bit about why, so, as I understand you, it’s like, there’s a ratchet effect that once you move up to that new state, that’s now the new one. And so it just, it means that at least one of our nodes has the ability to enforce the correct latest state. So could you just explain a little bit around that state numbers idea?

Christian Decker:

Yes. So the state numbers idea is actually connecting back to the very first iteration of Bitcoin. Like we had it with the nSequence proposal that Satoshi himself out it nSequence basically meant that you could have multiple versions of transactions and miners were supposed to info to pick the one with the highest sequence number and, and confirm that basically replacing any previous transaction that had a lower sequence number that had, that had a couple of issues, namely, that there is no way to force miners to actually do this. You can always, you can always bribe a miner to use a version of a transaction that suits you better or they might, be actively trying to defraud you. So there is no really good way of enforcing nSequence numbers. On the other hand, what we do with the with the state numbers is that we do not give the miners the freedom to choose which transaction to, confirm what we do is we basically say, okay we have a transaction 100, and this transaction 100 can be attached to any previous transaction that could be confirmed or it could still be unconfirmed that has a state number lower than 100.

Christian Decker:

And that’s how eltoo, we basically say, okay, this latest state represented by this transaction with a state number of 100 can be attached to any of the previous transactions and override their effect by basically ratcheting forward the state. So let’s say you have a published state 90. That means that anything with state number 91, 92 93, and so on, can be attached to your transaction. Now your transaction might confirm, but the effects that you want are in the settlement part of the transaction. And so if I can come in and attach a newer version of of that state, a new update transaction to your published transaction, then I can basically detach the settlement part of the transaction from this ratcheting forward. And I have just disabled your attempt at settlement by ratcheting forward and initiating the settlement for state 100.

Christian Decker:

And then you could come come along and say, okay, sorry, I forgot about state 100. Here’s state 110. So we can even while closing the channel, we can still continue making updates to the eltoo channel using these these state numbers. And the state numbers are really nothing else than making an explicit way of saying, okay, this number 100 overrides, whatever came before it, whereas with LN penalty, the only association you have between the individual transactions and so on is by following the ‘is spent by’ relationship. Basically you have, you have a set of transactions that can be can be published together. But there is no sense of of transitive overriding of effects.

Stephan Livera:

I see. And I guess maybe just a naive question, that a listener might be thinking, well, Christian, what if I tried to set my state number higher than yours, what’s stopping me from that?

Christian Decker:

You can certainly try. But since these are we are still talking about two of two multisig outputs I would have to counter sign that. And so I might as well sign it, but then I will make sure that if we later on come to a new agreement on what the latest state should be that that state number must be higher than whatever I signed before. So that this later state can then override your spuriously numbered state. And in fact, that’s something that we propose in the paper to hide the number of updates that were performed on a channel, not to go incrementing one by one, but sort of have a have different sized increment steps so that when we settle on chain, we don’t tell the rest of the world, Hey, by the way, we just had 93 updates.

Stephan Livera:

Of course. And also just from watching some of the Bitcoin dev mailing list discussion, I saw some discussion around this idea of whether the lightning node should also be looking into what’s going on in the mempools of Bitcoin versus only looking for the transactions that actually get confirmed into the chain. Can you just comment a little bit on how you’re thinking about the security model, as I understand, you’re thinking of it more like, no, we’re just looking at what’s happening on the chain and the mempool watching is a nice to have.

Christian Decker:

Yes so with, with all of these protocols, we can usually replay them only on chain and we don’t need to look at the mempool. And that’s true for eltoo as it is lightning penalty. But recently we had a lengthy discussion about a an issue that is dubbed RBF pinning attack which sort of makes this a bit harder. And the attack is a bit involved, but it basically boils down to the attacker, placing a placeholder transaction in the mempool of the peers, making sure that that transaction does not confirm, but being in the mempool that transaction can result in rejections for future transactions. And so that comes into play when we are talking about HTLCs, which span multiple channels.

Christian Decker:

And so we can have effects where the downstream channel is still locked because the attacker placed a placeholder transaction in the mempool. And we are frantically trying to react to this channel now being timed out the, this HTLC being timed out, but our transaction not making it into the mempool because it’s been rejected by this poison transaction there. And, if that happens on a single channel that’s okay, because eventually we will be able to resolve that. And an HTLC is not a huge amount usually where this becomes a problem is if we have, if we were forwarding that payment and we have a matching upstream HTLC that now also needs to timeout with, or where, or have a success. And that depends on the downstream, HTLC which we don’t get to see.

Christian Decker:

So it might happen that the upstream time out gets timed out. So basically our upstream node told us here’s $1 I promise to give it to you. If you can show me this payment or the hash preimage in a reasonable amount of time, and you turned around. And for that promise and said, Hey, your attacker, here’s $1. You can have it. If you give me the secret in time now the downstream attacker, doesn’t tell you in time. So you want to, you will be okay with the upstream one timing out but turns out the downstream one can succeed. So you’re out of pocket in the end of the forward amount. And that, that is a really difficult problem to solve without looking at the mempool, because the mempool basically is the only indication that this attack is going on.

Christian Decker:

And therefore that that we should, we should be more aggressive in reacting to the this attack being performed. But most lightning nodes do not actually look at the mempool currently. And so the there’s two proposals that we’re trying to do. One is to make the mempool logic a bit less unpredictable, namely that that we can still make progress without reaction, even though there is this poison transaction, that is something that we’re trying to get the Bitcoin core developers interested in. And on the other side, we are looking into mechanisms to actually look at the mempool, see what is happening then and then start alerting nodes that, Hey, you might be under attack please take precautions and and react accordingly.

Stephan Livera:

Great and also wanted to chat a little bit about the SIGHASH flags because I think obviously ANYPREVOUT and ANYPREVOUT ANYSCRIPT are some new SIGHASH flags. So maybe if you could take us through just some of the basics around what is a SIGHASH flag?

Christian Decker:

Yes. So a SIGHASH flag is sometimes confused with an opcode. It is basically just a modifier of an existing opcode namely objects, seek and object seek, verify, and op check multisig and object multisig verify variants that basically instructs the the check sig operation to which part of the transaction should be signed and which one should not be signed. So in particular what we do with SIGHASH_ANYPREVOUT is we when computing the signature and verifying the signature, we do not include the previous outputs in the signature itself. So these can be modified if desired, without invalidating the signature. Basically it is like a kid having a bad grade at at school coming home and needing a signature from the parents.

Christian Decker:

And what he does is he covers up part of the permission slip, so to speak and the parents still signs it. And and only then uncovers the the covered part, but this changing, what was signed does not invalidate the signature itself. Now that’s sort of a nefarious example, but it can be really useful. So if you’ve ever given out a blank check, for example where you could then fill in the amount at a later point in time, or fill out the recipient at a later point in time, that’s, that’s a very useful tool, for example. And where for eltoo what we use it for is basically we use the reaction transaction to to something that our counterparty has done and adapted in such a way that it can cleanly attach to what your counterparty has done, basically.

Stephan Livera:

I see. Yeah,

Christian Decker:

and there are some already existing SIGHASH flags. So, so for example, they’re the default one is SIGHASH ALL which covers basically the entirety of the transaction without the inputs script. And yeah, there’s SIGHASH_SINGLE, which has been used in a couple of places which basically signs the input and the matching output, but there can be other inputs and outputs as well, that are not covered by the signature. So you can basically amend a transaction and add later on new funds to that transaction and new recipients to that transaction. And we use that for example, to attach fees, to transactions in eltoo. So fees in eltoo are not intrinsic to the update mechanism itself. They’re attached like a sidecar basically which also removes the need for us to negotiate fees. For example, between the end points. Something that has in the beginning of lightning has caused a lot of channels to die, simply disagreement on fees. And there’s also SIGHASH NONE basically signs nothing. It signs the overall structure of the transaction. But it doesn’t restrict which inputs can be used. It doesn’t restrict which outputs can be used. And it basically just if gets one of these transactions, you can basically rewrite it at will basically sending yourself all the money that would have been transferred by.

Stephan Livera:

I see. So yeah, maybe just talking through the SIGHASH pot, I guess, for most users, without knowing when they’re just doing standard single signature spending with you know, on their phone wallet or whatever, they’re probably using SIGHASH all, and that’s what their wallet is using in the background for them. And I suppose if the listener wants to sort of see how this might work, they could obviously pull up a block Explorer and see on a transaction. You can see the different inputs and outputs. And what we’re talking about here is what you are. If I understand you correctly, it’s what we are committing to when we sign. And so could you maybe just spell out a little bit about what it means when you’re committing to a certain, like when that’s, what that signature is committing to?

Christian Decker:

Yes. So what it basically does is it takes the transaction, it passes through a hash function. And then the hash is basically is signed. The effect that we have by it is that if we if anything in the transaction itself is modified, which was also part of the hash itself, then then the signature is no longer valid. So it, it basically means that I both authorize this transaction and I authorize it only in this form that I’m currently signing. There can be no modification afterwards or else the signature or would have to change in order to remain valid. And so if we, SIGHASH flags, we remove something from the from the commitment to the transaction, then we can then we give outsiders or ourselves the ability to modify without having to resign basically.

Stephan Livera:

Right. And so that’s why for the typical user just doing single signature, their wallet is just going to use SIGHASH all, but where they are doing some sort of collaborative transaction, or there’s some kind of special construction with it, that’s where we’re using some of these other SIGHASH flags. And then bringing it back to why, why are we using all this eltoo and ANYPREVOUT the idea is that these ANYPREVOUT SIG hash flags will allow us to rebind to the prior update? Correct.

Christian Decker:

Exactly. Yes.

Stephan Livera:

Alright. And so, could we just talk a little bit about so ANYPREVOUT and then ANYPREVOUT ANYSCRIPT? So what’s the difference there?

Christian Decker:

So what we do with Sig Hash is basically no longer explicitly saying, Hey, by the way, I’m spending that those funds over there, instead, what we say is we have to, the output script and the script have to match. Other than that, we can mix a mix, these transactions, however, however we want. And so instead of having an explicit binding of saying, Hey, my transaction 100 now connects to transaction 99, and then the scripts have to match. And the scripts, I mean basically the output script would would specify the spender has to sign with public key X and the input script would contain a signature by by public key X. So instead of binding by both the explicit reference and the scripts, we now bind solely by the scripts. And so that that means that as long as the output says, I need –

Christian Decker:

I need the spender has to sign with public key X and the input of the of the other transaction that is being bound to it has a valid signature for public key X in it. Then we can attach these two now. What the difference between ANYPREVOUT and ANYPREVOUT ANYSCRIPT is, is basically whether we include the output script in the hash of of the spending transaction or not. And for the, ANYPREVOUT, we still commit to what script we are spending. So we basically take a copy of the scripts saying that this transaction, that the spending transaction needs to be signed by public key X. We move that into the spending transaction and then include it into the into the signature computation so that if the output script is modified, we cannot bind to it.

Christian Decker:

Whereas the, ANYPREVOUT ANYSCRIPT says, okay, we don’t take a copy of the output script into the input of the spending transaction, but we instead we have a blank script. And so we can bind it to any output whose output script matches our input script. So it’s a bit more freedom, but it is also something that we need for eltoo to work because the output script of the of the transaction we’re binding to includes the state number, and that obviously obviously changes from each state to state, but we still want to have the freedom of taking a later state and attaching it to any of the previous states. So for eltoo we to we’d have to use ANYPREVOUT ANYSCRIPT. And there are a couple of use cases where any ANYPREVOUT is suitable on its own. So for example, if we have any sort of transaction malleability and we still want to take a transaction that connects to a potentially malleable transaction, then we can use SIG HASH ANYPREVOUT, such that if the transaction gets validated in the public network, while it is before it is being confirmed, we can still connect to it using the connection between the output script and the input script and the commitment of the output script in the spending transaction.

Stephan Livera:

Yeah. And you just mentioning you were mentioning Malleation there. So could you just outline what is malleation of a transaction there?

Christian Decker:

Ooh, Malleation is the bane of all off chain protocols, basically. Malleation is something that that we’ve known about for, well over seven years now, even longer than that. And if you remember the Mt Gox hack was for some time attributed to malleability, where they basically said our transactions were malleated, we didn’t recognize them anymore. So we paid out multiple times. So what what basically happens is that I create a transaction and this transaction includes some information that is covered by the signature and can therefore not be changed, but it also could include some information that it cannot possibly be covered by the signature, for example, the signature itself because we have in the input script of a transaction, we need to have the signatures. We cannot include the signatures in the signature itself. Otherwise we’d have the circular argument, right?

Christian Decker:

And so while signing the input scripts are set to blank and not committed to. And that means that if we then publish this transaction, there are places in the transaction that can be modified without invalidating the signature anymore. And some parts of this include, for example, push operations for example, normalizations of signatures themselves. So we can add prefixes to stuff we can add. We can add dummy operations to the input script, therefore change how this, how the transaction looks just slightly, but not invalidating the signature itself. So the transaction now it looks different and is getting confirmed in this different form, but we might have a dependent transaction that we’re referring to the old form by its hash by it’s unchanged form. And so now this this followup transaction that was referencing the unmodified transaction can no longer be used to spend those funds because, well, the miner will just see this new transaction, go look for the old output that it is spending.

Christian Decker:

This output doesn’t exist because it looks ever so slightly differently now because the hash change. And so it will just say, okay, I don’t know where you’re getting that money from go away. I’m throwing away that transaction, and it will not get get confirmed, whereas with SIG HASH ANYPREVOUT, we can, we can counter this by basically having the transaction in the wider network, be modified, be confirmed in this modified state. And then the sender of the followup transaction can just say, okay I see that there has been a modification to the transaction that I’m trying to spend from. Let me adjust my existing transaction by changing the reference inside of the input to now this new alias that everybody else knows the old transaction about, and now we can publish this transaction. We did not have to re-sign the the transaction.

Christian Decker:

We did not have to modify the signature. All we had to do was basically take the reference and update it to actually point to the real confirmed transaction. And so that, that makes off chain protocols a lot easier because while having a single signer re-sign a transaction might be easy to do. If we’re talking about multisig transactions, where multiple of us have to sign off on any change, that might not be so easy to implement. And so ANYPREVOUT gives us this freedom of reacting to stuff that is that happens on chain or in the network without having to go around and convince everybody, Hey, please sign this updated version of this transaction because somebody did something in the network.

Stephan Livera:

I see. Yeah. So I guess if I understood you correctly, it’s sort of like the way eltoo has been constructed, it’s that you’re defending against that risk. And then you’re trying to obviously use this new functionality of being able to rebind, you know, dynamically. And I guess I just want to confirm, so for listeners who are concerned about Oh, okay, maybe there’s a risk. I don’t want to it’s, this is all opt in, right? So it’s only if you want to use lightning in the eltoo model that, then let’s say you and I have this special type of seeing hash flag that we are having a special kind of output that we are doing the updates on our channel, but if somebody doesn’t want to, they can just not use lightning. Right. And it doesn’t risk them. Right? Yeah,

Christian Decker:

Absolutely. It’s, it’s fully opt in. It like, like we said before, it, it is a sig hash flag. The, we do have a couple of, of sig hash flags already, but no wallet that I’m aware of implements anything, but the cash all. And so if you don’t want to use lightning or you don’t want to use any of the off chain protocols that are based on SIGHASH_ANYPREVOUT simply don’t use a wallet that can sign with them. These are very specific escape hatches from the from the existing functionality that we, that we need to implement more advanced technologies, on top of the light of the Bitcoin network, but it’s by no means something that suddenly everybody should start using, just because it’s a new, new thing that, that is out there. And with if we’re careful not to even implement SIGHASH_ANYPREVOUT in everyday consumer wallets, and this will have no effect whatsoever on on the users that do not want to use these technologies.

Christian Decker:

So it’s, it’s something that has a very specific use case. It’s very, very useful for those use cases, but by no means everybody needs to use it. And we’re sort of, we’re trying to to add as many security features as possible. So for example, if you sign with a SIGHASH flag that is not SIG HASH ALL you as the signing party basically are the only one that is deciding whether to sign or not whether to use the SIG HASH flag or not. Whereas whereas with the ANYPREVOUT changes that were introduced and AJ has done a lot of work on on this he introduces a new a new public key format that explicitly says, Hey, I’m available for SIGHASH ANYPREVOUT. So even the one that is being spent from now has the ability to opt into ANYPREVOUT being used or not, and both have to match, right. The public key that that is being signed for has to have opted in for ANYPREVOUT. And the signing party has to opt in as well. Otherwise we will fall back to existing semantics.

Stephan Livera:

And also, as I understand this BIP 118, there is a reliance on taproot being activated first before ANYPREVOUT. So can you just talk to us a little bit about that?

Christian Decker:

Yes. So obviously we would have liked to have ANYPREVOUT as soon as possible, but one of the eternal truths of software development is that reviewer time is sort of scarce. And we decided to not push too hard on ANYPREVOUT being included in taproot itself to keep taproot itself very minimal and sort of clean and easy to review. And then do and then try to do ANYPREVOUT soft fork at a future point in time at which we will hopefully have, again, enough confidence in our ability to perform soft forks that we can actually rollout ANYPREVOUT in a reasonable amount of time. But for now it’s more important for us to get taproot through. Taproot is an incredible enabling technology for a number of changes, not just for lightning or eltoo, but for a whole slew of things that are based on taproot. And so any delay in taproot would definitely not be in our interest. And we do see the possibility of rolling out ANYPREVOUT without too many stumbling stones at a second stage. Once we have seen taproot be activated correctly.

Stephan Livera:

Awesome. and also in the BIP118 document by AJ, there’s a discussion here around signature replay, so what’s a signature replay. And how does that’s being stopped?

Christian Decker:

Yes signature replay is one of the big concerns around the activation of ANYPREVOUT. And it basically consists of if I have one transaction that can be rebound to a large number of transactions, this doesn’t force me to use that transaction only in a specific context, but I could use it in a different context itself. So for example, if we were to construct an off chain protocol that was broken and couldn’t work we could end up in a situation where you have two outputs of the same value that opted in for ANYPREVOUT and you have one transaction that spends one of them now, since both opted into ANYPREVOUT and both have the identical script and both have the identical value, I could actually replay that transaction on both outputs at once.

Christian Decker:

So basically instead of the intended effect of me giving you, let’s say $5 in one output, you can claim twice $5 by replaying this multiple times. Now I’m saying that this is true for off chain protocols that are not well developed and are broken because well designed off chain protocols will only ever have one transaction that you can bind to. Or this you cannot have multiple outputs that all can be spent by the same, ANYPREVOUT transaction, but it might still happen that somebody goes onto a blockchain Explorer and looks up the address and then send some money that happens to be the exact same value to that to that output. And so what we’re trying to do is to find good ways to prevent exactly the scenario of somebody accidentally sending money, accidentally sending funds and creating an output that could potentially be claimed by SIGHASH_ANYPREVOUT by, for example, making these scripts unaddressable.

Christian Decker:

So we create a new format for we create a new script format for which there is no bech32 encoding for the script. And suddenly you cannot go on to a blockchain Explorer and sort of manually interfere with an existing off chain protocol. And so there are a number of steps that we are trying to do to reduce this accidental replayability. That being said in eltoo, for example, the ability to rebind a transaction to any of the previous matching ones is exactly what we were trying to achieve. So I would say it’s a very, useful tool, but it, in the wrong hands, it can be dangerous. So don’t go play with, SIGHASH_ANYPREVOUT, if you don’t know what you do.

Stephan Livera:

Fair enough. And so what would be the pathway then to activating ANYPREVOUT or what would, what stage would it be in terms of people being able to say, review it or test it, that kind of thing?

Christian Decker:

I had a branch for no input, which was used by Richard Myers, for example, to implement a prototype of eltoo in Python that is working. I’m not exactly sure if ANYPREVOUT has any code that can be used just yet. I would have to definitely check with AJ or implement it myself. But it shouldn’t be too hard to implement given that it’s very, at least a SIGHASH NOINPUT consisted of two if statements and a total of four lines changed. So I don’t foresee any huge technical challenges. It’s mostly just the discussion around making it safe, making it usable and making it efficient there taking a bit longer. And we have that time as well, because we are waiting for taproot to be activated in the meantime.

Stephan Livera:

Yeah. So that sounds really cool. Is there anything else you wanted to mention about ANYPREVOUT or shall we now start talking about MPP?

Christian Decker:

ANYPREVOUT it’s absolutely cool. And we’re finding so many use cases. It’s really nice. And I would, I would so love to see it.

Stephan Livera:

Excellent. Well, look, I think we’ll see what everyone, what all the Bitcoin people are out there thinking. But I think certainly the benefits of having eltoo in lightning would be a pretty cool. And it enables, yeah, I guess, like you were saying the whole multi-party channels, which for listeners who haven’t listened to our first episode, I think it’s 57 off the top of my head go and have a listen to that. I think there’s a lot of possibilities there in terms of multi-party channels. And I suppose that also helps in terms of being able to get around that idea of there won’t necessarily be enough UTXOs for every person on earth. And that’s why, you know, multi-party channels might actually be a handy thing to have. All right. So let’s have a look into MPP then. So multi-part payments. So listeners also check out my earlier episode with Rusty on this one. But Christian, you had a great blog post talking about MPP and how it’s been implemented in C lightning. So do you want to just tell us a little bit about the latest with that?

Christian Decker:

Yeah, so we implemented multi-part payments as part of our recent 0.9.0 release which which we published just about 10 days ago, I guess. And multi-part payments is one of those features that has been long awaited because it enables us to be much more reliant and be adapt ourselves way better to the network condition that we encounter. And it basically boils down to, instead of me sending a payment and doing it all in one chunk, we split the payment into multiple partial payments and send them on different paths from us to the destination and thus making better use of the of the network liquidity allowing us to create bigger payments since we are no longer constrained by the capacity of individual channels, instead we can bundle multiple channels capacities and use the aggregate of all of these channels together. And it also allows us to make the payments much more reliable in that the we send out parts, get back information and and only retry the parts that failed on our first attempt.

Stephan Livera:

So there’s a lot of benefits.

Christian Decker:

Yeah. There’s also a couple of benefits when it comes to privacy, but we’ll probably talk about those a bit later as well,

Christian Decker:

I guess, what are some of the main constraints then in terms of your node and how it works, if it wants to construct an MPP multi-part payment in a package, is it?

Christian Decker:

Yeah, so, so there’s, there’s two parts of MPP. One is the recipient part which is basically just I know I should receive $10. I received only two. I’ll just keep on waiting until I get the rest holding on to the initial two that I already have for sure. And so the recipient basically just, grabs money and waits for it to be all there before then, then claiming the full amount. And on the sender’s side, what we do is basically we split the payment into multiple parts for each of these partial payments. We compute a route from us to the destination for each of these. We then go ahead and compute the routing onion. So each individual part has its own routing onion has its own path, has its own fate, so to speak.

Christian Decker:

And then we send out the partial payment with its onion on its merry way until we either get to the destination at which point the destination will collect the promise of incoming funds. And if it has all of the funds that were promised available, it will release the payment hash or the payment pre image, thus locking in atomically all of the partial payments, or we get back an error saying, Oh, this channel down the road doesn’t have enough capacity. Please try again. And at which point we then update our view of the network. We compute a new route for this payment, and we try again. And if we cannot find a new route for the amount that we have, we split it in half, and now we have two parts that we try to send independently from each other.

Christian Decker:

And so the sender side is pretty much in control of how big do we make these parts? How do we schedule them? How do we route them? How do we detect whether we have a fatal error that we cannot recover from, or when do we detect that this part is okay, but this part is about to be retried. And so at the sender part is where all of the logic is basically the recipient just waits for incoming pieces. And then at some point decides, okay, I have enough I’ll claim, all of them. And this sendersite required us to reengineer quite a lot of our payment flow. But that also enabled us to build a couple of other improvements, like the keysend support, for example, which we so far only had a Python plugin for, but now have a C plugin for it as well.

Stephan Livera:

Right. And so you were talking through the, essentially the two different processes, you’ve got the pre split, and then you mentioned the adaptive splitting. So I guess that’s the once you’ve tried it one time and it failed. Now you can take that knowledge and try a slightly different split or slightly different route. And then it will then create the new payment and try to send that?

Christian Decker:

Exactly. Right. So the adaptive splitting is exactly the part that we mentioned before is basically we try once and then depending on what comes back, we decide, okay, do we retry? Do we split? Do we what do we do now? What is this something that we can still retry and have a chance of completing? Or do we give up basically?

Stephan Livera:

Yeah.And so does it impact, I guess when you are trying, so let’s say you’re, you have installed C-lightning and you’re trying to do a payment and then does. So I guess in the background really what’s going on is your node has its own little graph of the network, and it’s trying to figure out, okay, here’s where the channels are that I know about. And here’s what I know of the capacity. And does it then have better information and therefore each successive try is a little bit better. How does that work?

Christian Decker:

Exactly. So initially what we have in the network is basically we see channels as total capacities, right? If the two of us opened a $10 channel, then somebody else would see it as $10. And they would potentially try to send $8 through this channel now, depending on how the ownership of those $10 is this might be possible or not. So for example, if we each own five, there’s no way for us to send $8 through this channel, right? So we will report an error back to the sender and the sender will then know aha 8 was more than the capacity. So I will remember that this upper limit on the capacity, it might even be lower, but we know that we cannot, for example, send nine Bitcoins through that channel.

Christian Decker:

And so it will, as we learn and more about the network, our information will be more and more precise, and we will be able to make better predictions as to which channels are usable and which channels are, and for given payment of a given size, basically. And so there is no point in us retrying this $8 payment through our well-balanced channel, again, because that cannot happen. But if we split in two and now have 2 $4 parts, then one of the might actually go through our channels. And we knowing knowing that we have five and five, it will actually go through, and now the sender is left with a much easier task of finding a second for a dollar, a channel $4 dollar path from himself to the destination, rather than having this one big chunk of, of eight all at once.

Stephan Livera:

And also from the blog post, you touch on this idea about, so basically the way the fees work is there’s a base fee. And then there’s typically a sort of like a percentage fee. And so if you split your MPP up into so many, like a hundred different pieces, you’re just going to end up paying massive amount of base fee across all of those a hundred pieces. So there’s kind of like a, your c-lightning node has to make a decision on how many pieces to split.

Christian Decker:

Exactly. So we need basically to have a lower value after which we basically say from now on, it’s unlikely that we’re going to find any path because the payment is so small in size that it will basically be dominated by the base fee itself. And this is something that we’ve encountered quite early on already when when the first games started popping up on the lightning network, for example, Satoshi’s place, if you wanted to draw, to color in one pixel on Satoshi’s place, you’d end up paying one milli satoshi, but the base few would have to get there would already be like one Satoshi. And so you you’d basically be paying a 100,000% fee for your one Millisatoshi transfer, which is absolutely ludicrous. And so we added, we added an exception for really tiny transfers that we call signaling transfers because during their intent is not really to pay somebody it’s more to signal activity.

Christian Decker:

And so in those cases, we allow you to have rather large fee upfront. But that is not applicable to MPP payments because if we were to basically give them a budget of 5 Satoshis each, then these would all accumulate across all of the different parts and we’d end up with a huge fee. And so we decided to basically give up if a payment is below 100 satoshis in size and well, not give up, but not split any further because at that size the base fee would, would dominate the the overall cost of the transfers. And so what we did there was basically to take the network graph and compute all end to end paths that are possible, all pairs, shortest paths, and compute what the base fee for these paths would be. And if I’m not mistaken, we have a single digit percent of payments that may still go through. Even though they they are they are below 100 satoshis in size. And so we felt that that aborting at something that is smaller than 100 Satoshis is safe. We will still retry different routes, but we will not split any further because that would basically double the cost in base fees at each splitting.

Stephan Livera:

Yeah. And I mean, I guess really in practice, most people are opening channels much, much larger than that. So a hundred sats is really like trivial, right? Like that, to be able to move that through. And at current prices, we’re talking like 6 or 7 cents or something.

Christian Decker:

Yes. So the speaking of speaking of channels and the expected size that we have a payment that we can actually send through that brings me back to our other payment modifier, the pre split modifier which basically instead of having this adaptive mechanism where we try and then learn something, and then we retry with this new information incorporated. We decided to do something a bit more clever and say wait, why do we even try these really large payments in the first place when we know perfectly well that most of them will not succeed at first? And so what I did was basically I took my lightning node and tried to send payments of various sizes to different end points by probing them. And unlike my previous probes where I was interested in sort of seeing if I could reach those those nodes I was more interested, okay.

Christian Decker:

If I can reach them, how much capacity could I get on this path? What is the biggest payment that would still succeed getting it to getting it to the destination? And so what we did is we measured the capacity of channels along the shortest path from me to I think 2000 destinations. And then we plotted it and it was pretty clear that that amounts below 10,000 Satoshi. So approximately $1 have a really good chance of of succeeding on the first try. And so we have these we measured the capacities in the network and found that payments with 10,000 Satoshis in size can succeed relatively well. We have an 83% success rate for payments of exactly 10,000 satoshis, smaller amounts will have higher success rates. And so by, instead of trying these large chunks at first, and then slowly moving towards towards the sizes, anyway, we decided to split right at the beginning of the payment into roughly $1 sized chunks, and then send them on their way. And these already have a way better chance of succeeding on the first try, then this one huge chunk would have initially.

Stephan Livera:

Gotcha. And just to clarify that percentage, you were mentioning that is on the first try, correct. So it will then retry multiple times and the actual payment success rate is even higher than that for 10,000 sets, correct?

Christian Decker:

Absolutely. Yeah. Yep.

Stephan Livera:

And I think this is an interesting idea as well, because it means it makes it easier for the retail, you know, HODLer or retail lightning enthusiast, to be able to set up his node and be a meaningful user of the network that they’re not so reliant on routing through the massive, the well known massive nodes, like, you know, the ACINQ node or the bitrefill node or the zap node, or like it’s easier for an individual because now you can split those payments across multiple channels. Right?

Christian Decker:

Absolutely. So, so what we, what we do with with with the pre split and adaptive splitter, we basically make better use of the of the network resources that are available by spreading by spreading a single payment, over a larger number of of routes. We give each of the nodes on those routes, a tiny sliver of fees instead of going through the usual suspects and giving them all of the fees. So we make revenue from from routing payments, more predictable. We learn more about the network topology. So while doing MPP payments, we effectively probe the network and, find places, that are broken and will cause them to close channels that are effectively of no use. Anyway something that we’ve seen with with the probing that we we did for the lightning network conference was that if we end up somewhere where the channel is nonfunctional, we will effectively close that channel and prune the network of these of these relics basically that are of no use.

Christian Decker:

And we also speed up the end to end time basically by by doing all of this in parallel, instead of sequentially where each payment attempt would be would be one attempted one by one. We massively parallelised that and learn about the network and can can make better use of what we learned by speeding up the payment as well.

Stephan Livera:

Yep. And so also wanted to touch on the privacy elements. So you were touching on this a little bit earlier, so I guess there’s probably two different ways you could think of this, right. Or at least there are multiple angles I can think of. So one angle might be, well, if somebody was trying to surveil the network, now they, and they wanted to try to understand what were the channel balances and try to ascertain or infer from the movement in the balances who is paying who, well, I guess now MPP kind of changes that game a little bit. It makes it harder for them, but then maybe on the downside you might say, well, because we’re still in the we haven’t moved to this whole Schnorr payment points PTLC idea, then it’s still the same payment pre image. And so it’s asking the same question to use the phrasing Rusty used? And so in that sense, it might be theoretically easier for a, say a hypothetical surveillance company to set up the spy lightning nodes and sort of see, Oh, they’re asking the same question, right? Yeah. What are your thoughts there?

Christian Decker:

That that’s definitely true. There, there is there is definitely some, some truth in the, in the in the statement that by basically distributing a payment over more routes, and therefore in involving more forwarding nodes, we are basically telling a larger part of the network about a payment that we are performing. And so that’s probably worse than, than our current system where even if we were using a big hub that hub would see, okay, one payment and the rest of the network would be none the wiser on the plus side, however, the one big hub thing would basically give away the exact value direct you’re transferring to the big hub. Whereas if we, if we pre split to $1 amounts and then do adaptive splitting each of these nodes that are each of the additional nodes that isn’t, and now involved in this payment learns a tiny bit about the payment being performed, namely that there is a payment, but since we use this homogeneous, split of everything splits to $1, they know that they don’t really know much more than that.

Christian Decker:

They will learn that somebody is paying someone but they will not learn about the amount, they will not learn about the source and destination. And and we are making traffic analysis a lot harder for ISP level attackers by, by really increasing the chattiness of the network itself. We make it much harder to, for observers to associate or to collate individual observations into one payment. And so it’s definitely not the perfect solution to to tell a wider part of the network about the payment being done, but it is an incremental step towards towards the ultimate goal of making basically every payment indistinguishable from each other which we are getting with with Schnorr and the point time lock contracts. And so once we have the point time lock contracts, we truly have a system where we are sending back and forth payments that are not collatable by payment hash as you correctly pointed out.

Christian Decker:

And not even by amount, because well, all of the payments have roughly the same amounts. It’s the combination of multiple, of these partial payments that gives you the actual transfered amount. And so I think it’s not a clear loss or a clear win for privacy that we’re now telling a larger part of the network. But I do think that the pre splitter and the adaptive splitting is combined with PTLC will be an absolute win no matter where you look at it.

Stephan Livera:

Gotcha. Yeah, I think that’s a very fair way to summarize. So in terms of getting PTLC Point Timelock contracts, the, the requirement for that would be the Schnorr Taproot soft fork, correct? Or is there anything else that’s also required?

Christian Decker:

Only the, yeah. Taproot and Schnorr is the only one that is required for PTLCs. Then we’d be, I’m expecting the lightning network specification to be really quick at adapting it and pushing it out to the network and actually making use of of that of that new found freedom that we have with PTLCs and Schnorr.

Stephan Livera:

That’s great. And I suppose the other component to think about and consider from a privacy perspective is just the on chain footprint aspect of lightning. So this is one thing where maybe some listeners might not be as familiar, but the, obviously when you’re doing lightning, you still have to do the open and close of a channel. And so currently that’s still sort of, well kind of judging by it. You know, you did some recent work at the recent lightning conference as well, showing some sort of chain ability to sort of understand which ones of these were probably lightning channel opens, correct? So I suppose that is another thing where taproot might help also particularly in the case of a collaborative close. Correct. So, as I understand in the, once we have taproot, then let’s say you and I open a channel together, and it’s the happy path. The collaborative, close that channel close is indistinguishable from just a normal taproot key path spend, correct?

Christian Decker:

Exactly.Yeah. So, so basically our opens we’ll always look exactly like somebody’s paying to a single sig. The single sig under the covers happens to be a 2 of 2 multisig disguised as a single sig through the signature aggregation proposals that we have and the close transactions, if they are collaborative closes they will also look like single sig spends to then the amounts to the destinations that are owned by the end points. But it might be worth pointing out that non-collaborative closes will leak some information about the usage of eltoo or lightning penalty simply because we didn’t have to enter this disputed phase where we reveal all of the internals of our agreement, namely, how we intend to overwrite or penalize the the misbehaving party.

Christian Decker:

And then we can, we can still read out some of the information from a channel. And, that’s where where I mentioned before that you might not want to increment state numbers one by one, for example. And this is also the reason why in LN penalty, we hide, for example, the commitment number in the sequence in the lock time field but encrypt it because those informations might still eventually end up on the blockchain where they could be analyzed, but then again, we’d gossip about most of these informations anyway, because we need to have a local view of the network in order to route payments.

Stephan Livera:

I see. So it’s kind of a question of what path do you really need to be private, I guess. And one other part I just wanted to confirm my understanding is obviously not as good as yours, but with the taproot proposal, my understanding is you can either spend, so you’ll have a special kind of taproot output. And the cool thing about the whole Schnorr signatures aspect is that people can do more cryptography and manipulation on that. And that’s this idea of the tweaking. And so my understanding there then is you either have the key path spend, which is the indistinguishable spend, right? And that’s like the collaborative close example, but then in the non-collaborative close, as I understand that would be a script path spend. And then as part of taproot, the idea is that you are showing where like, you have to have so I don’t understand this as well, but there’s a Merkle tree. And then you have to expose which of the scripts that you want to spend. And then you’re showing, okay, here’s the script I want to spend. And here’s the signatures in relation to it, is that right? Or where am I getting it wrong there?

Christian Decker:

No, that’s perfectly right. The whole taproot idea comes out of this, this whole discussion for Merkelised abstract syntax trees for quite awhile. And it’s adds a couple of new features to it as well. So Merkelised abstract syntax tree where it’s basically a mechanism of us having multiple scripts that are then added to a Merkle tree and summed up until we get to the root. And then the root would be, would be what we put into our output script. And then when we spend that output, we would basically say, okay, by the way, that Merkle tree corresponds to this script. And here is the the input that matches this script, proving that I have permission to spend these coins and taproot goes one step further and says, well, that Merkle tree root is sort of not really useful.

Christian Decker:

We could make that a public key and mix in the Merkle root through this, this tweaking mechanism. And so that, that would then allow us to basically say, okay, either we pay spending we sign using the root key into which we tweak the the merkelised abstract syntax tree. And that’s the key path spent, or we can say, okay I don’t, I cannot sign with this with this pub key alone, but I can show the script that corresponds to this commitment. And then for that, I do have all of the information I need to sign off. So in the normal case for a channel close, we basically use the root key to sign off on the close transaction. And in the disputed case, we’d actually go and say, okay, here’s the script that we agreed upon before. And now let’s run through it and, and resolve this dispute that we have by settling on chain and having the blockchain as a mediator for our dispute.

Stephan Livera:

Gotcha. Yeah. Great. That’s a, yeah, there’s a lot there to take in, and also wanted to talk a little bit about some of the lightning attacks that are coming out in some of the articles and from my understanding from chatting with yourself and some of the other lightning protocol developers, it seems to me like, there’s, there’s a bunch of these that have basically they’ve been known for a little while, but some of them are now coming out as papers. So an interesting recent one is called Flood and Loot a system, a systemic attack on the lightning network. So, as I understand this, basically it kind of requires this idea of establishing channels and then trying to send through a lot of HTLC payments, and then maybe you can help me here, but then they kind of go non-responsive and then they force the victim to try to go to chain. But the problem then is because they’ve done it with so many people and so many channels all at once. They wouldn’t be able to get confirmed. And then that’s where the victim would lose some money. Could you help help me there? Did I explain that?

Christian Decker:

It’s absolutely correct. So the the idea is basically to have an attacker send to a second node, he owns a massive amount of HTLC a massive amount of payments going through the victims. And so what what you end up doing there is basically you, you add a lot of HTLCs to the channel of of your victim. And then you hold on to these payments on the on the recipient side of the channel, something that we’ve known for quite some time. And we know that holding onto HTLC’s is kind of dangerous. So this attacker will hold onto HTLCs so long that that the timeout approaches for the HTLC. So HTLC basically has two possible outcomes, either they’re successful and the preimage is shown to the endpoint that added the HTLC, or we have a timeout.

Christian Decker:

And then the the funds revert back to the endpoint that added the HTLC. And this works because we there is no race between the success transaction and the timeout transaction. So if there is no success for let’s say 10 hours, then we will trigger the timeout. And because we can be confident that the success will not come after the timeout came. Now this flood and loot attack actually does exactly that by holding onto the HTLC, it forces us to have a race between the timeout and the success transaction. The problem is that our close transaction, having all of these HTLCs attached is so huge that it will not confirm for quite some time. And so they can force the the close to take so long that the timeout has expired. And we are suddenly in a race between the successful transaction and the timeout transaction. And that’s basically, the attack we have is to bloat somebody else’s channel such that the confirmation of the close transaction that is following is so long that we can actually get into a situation where we are no longer sure with the timeout or the success transaction will succeed in the end.

Stephan Livera:

Yep, and so I guess there’s a lot of moving parts here, because you could say, okay, well, let’s modify the CSV window and let’s make that longer, or let’s change the number of HTLCs and restrict that for each channel. Right. So can you talk to us a little bit about some of those different moving parts here?

Christian Decker:

So it’s really hard to say, okay, one number is better than then the other. But one way of of reducing the impact of this attack for example, is to limit the number of HTLCs that we add to our own transaction. And that will directly impact the the size of our commitment transaction, and therefore our chances of getting confirmed in a reasonable amount of time, and therefore to avoid having this, race condition between success and timeout. The reason why I’m saying that there is no clear solution is that reducing the number of HTLCs that we add to our channels itself reduces the utility of the network as a whole, because once we have 10 HTLCs added and we only allow 10 to be added at once then that means that we can that we cannot forward the 11th payment, for example.

Christian Decker:

And if our attacker knows that that we have this limit, they could effectively run a DOS attack against us by by opening 10 HTLCs. Exhausting our budget for HTLCs and therefore making our channel unusable for, until they released some of the HTLCs. So that’s, that’s an attack that we are aware of. And HTLC that so far hasn’t been caught up by academia, but I’m waiting for it. And and so all of these parameters are a trade off between between various goals that that we want to have. And we don’t currently have a clean solution that has only upsides and the same goals for CSVs for example, if we increase the CSV timeouts, then this attack might be harder to enforce because we we can spread confirmation of transactions out a bit further on the downside, having large CSVs means that if we have a non-collaborative close for a channel, then the funds will return only once the CSV timeout expires. And that then means that the funds are sure to come back to us, but might not be available for a couple of days before we can reuse them.

Stephan Livera:

Yeah. So it’s like an opportunity cost of your time, because you want to be able to use that money now or whatever. Right. So, but again, each of these are kind of, there are trade off and there’s no kind of perfect answer on them. I guess so one other question I had is just around, and this is just a general question is when, so let’s say somebody tried to jam your channels, right? How does, how do HTLCs release? Is that just over time or the function there?

Christian Decker:

So each HTLC has a timeout at which we the end point that has added the HTLC can basically use this timeout to recover funds that that are in this HTLC. After this timeout expires. And so each HTLC that is added starts basically a new clock, that counts down until we can recover our funds. And if the success case happens before this timeout, then we’re happy as well. But if this timeout is about to expire and we need to resolve this HTLC on chain, then we will have to force this channel on chain. Before this timeout expires, a couple of blocks before and and then basically force our counterparty to either reveal this the pre image or for us to grab back our funds through the timeout. So we then end up with a with a channel closing slightly before the time out, and then an on chain settlement of that HTLC.

Stephan Livera:

I see. So we could think of it, like we set up our node, we set up the channels and over time HTLCs will route through. And then as that, I think it’s usually going to be a CSV or maybe a CLTV where over time, just those HTLCs will kind of expire out because the timer has run out on them. And now you’ve got that capacity back again.

Christian Decker:

Yeah. So in these cases they’re CLTV’s because we need absolute times for HTLCs. And that’s simply because we we need to make sure that the downstream the, the HTLC that we forwarded settles before the upstream or the HTLC where we received from settles. So, so we need to have this time to basically extract the information from the downstream HTLC, turn around and then give it to the upstream HTLC, in order to settle the upstream, HTLC correctly. And so that’s where the, the whole notion of CLTV Delta comes in that that is a parameter that each node sets for himself and says, Hey, I am confident that if my downstream nodes settles in 10 blocks I have enough time to turn around and inform my upstream note about this downstream settlement so that my channel can stay active.

Stephan Livera:

Got it. And also wanted to touch on the commitment transaction size. So, as you were saying, part of this attack in the flood and loot example depends on having a very large commitment transaction. So I guess, bringing it back to that model that let’s say you and I set up the channel, and I guess what we’re getting to there is if there’s a lot of pending HTLCs, why does that make the transaction bigger? Is it that there’s a lot more outputs there or what’s going on with that?

Christian Decker:

That’s exactly the case. So the commitment transaction varies in size over time as we change our state. So initially when, when we have a single party funding, the channel, then the entirety of the funds will revert back to that to that party. And so the commitment transaction will have one output that basically just sends all of the funds back to the funding party. As soon as the counterparty has ownership of some funds in the channel, then we will add a second output, basically one going to end point A and one going to end point B. And those reflect the settled capacity that is owned by the respective party. And then we have a third place where we add a new outputs and that’s exactly the HTLC. So each HTLC does not belong.

Christian Decker:

It doesn’t belong to either A or B, but it belongs it’s somewhere in the middle, right? If we succeed, it belongs to B and if it doesn’t succeed, it reverts back to A for example. And so each of these, each of the HTLCs has has their own place in the commitments and a transaction in the form of an output, reflecting the value of the HTLC and having the output script, the resolution script of the HTLCs, which spells out Hey, before block height X, I can be claimed by this and after block height X, I can be reverted back to whoever added me. And so having a lot of HTLCs attached to a channel means that the commitment transactional is really large in size. And that’s also why we have this seemingly random limit on the total number of HTLC in the protocol of 483 maximum HTLCs attached to a single transaction because that at that point, with 483 HTLCs, we’d end up with a commitment transaction that is a hundred kilobytes in size, I think,

Stephan Livera:

Oh, that’s pretty big, we’re normally talking in terms of bytes, right? Like a standard transaction might be, it might be like 300 bytes or something like a standard one, right?

Christian Decker:

Yeah. It’s a massive cost as well to get that confirmed. And it definitely is a really evil attack because not only are you stealing from somebody, but you’re also forcing them to pay considerable amount of money to actually get their channel to settle.

Stephan Livera:

I see. And the other point there is that because we count fees in terms of sats per bytes, and if you’ve done that fee negotiation between the two nodes upfront, let’s say, you and I, we negotiated that early on then. And then one of us goes offline because it’s the flood and loot attack. Then we that’s what you’re getting to there. The point that you’d have this huge, huge transaction, but you wouldn’t have enough fees to actually close it.

Christian Decker:

Exactly. So we would, we would stop adding HTLCs before we no longer have any funds to settle it, but it would still be costly in if we ever end up with a large commitment transaction where something like 50% of our funds go to fees because it’s this huge thing.

Stephan Livera:

Yeah. Right. Yeah. So, I mean, this is, yeah. Quite in depth. I also wanted to just talk a little bit more, maybe if we step back and just talk about lightning generally, right. Like to kind of the growth of lightning network and maybe some of the different models that are out there. So I guess maybe just talking through a couple that exist today in terms of how people use lightning node, and right now today there’s for example, the Phoenix wallet and ACINQ style where, you know, it’s kind of, well, it is non-custodial, but there’s certain trade offs there and it’s all good going through the ACINQ node. Then you’ve got, say Wallet of Satoshi style, which is kind of like, they’re kind of like a Bitcoin lightning bank and the users are just customers of that bank, if you will. And then you’ve got kind of some people who are just going full mobile node you know, neutrino style and then maybe the more self-sovereign style where let’s say people might run, you know, those node packages, like say myNode or nodl, or raspiblitz, and then have a way to remote in with their Blue wallet or with their Zap or Zeus or Spark Wallet.

Stephan Livera:

So I guess, do you have any thoughts on what models do you think will be more popular over time?

Christian Decker:

I definitely can see the first and last model quite nicely, namely the sort of mobile wallet that has somebody on the operational side taking care of operating your node, but you are still in full control of your funds. So that would be sort of the Phoenix ACINQ model where you care for your own node, but sort of the hard parts of maintaining connectivity and maintaining routing tables and, and so on and so forth would be, would be taken care of by a professional operator. And that’s also why together with ACINQ, we came up with the trampoline routing mechanism and then some other facets of this of mechanisms to outsource routing to online nodes because running a full lightning node on a mobile phone while way easier than a Bitcoin full node, it is still going to use quite a considerable amount of resources in terms of battery and data to synchronize the view of the network to find paths from you to your destination.

Christian Decker:

And you would also need to monitor the blockchain in a reliable way so that that if something happens, one of your channels goes down, you are there to react. And so having somebody taking care care of those parts, namely to preprocess the network, the changes in the network view and providing access to the wider network through themself is definitely something that I can see being, being really popular. On the other side, I can definitely see the people that are more into into operating a node themselves going towards a self sovereign node style at home, where they have a home base that that their whole family might share. And or they might administer it for a group of friends and each person would then get a node that they can remote into and operate from there.

Christian Decker:

And there the issue of synchronizing routing notes and so on to your actual devices that you’re running around with like a mobile phone or your desktop, doesn’t really matter because you have this 24 hours snowed online that that will take care of those details. The fully mobile nodes. I think, they’re interesting to see, and they definitely show up a lot of interesting challenges. But it might just be a bit too much for the average user to have to take care of all of the stuff themselves, right. To know, to learn about what a channel is to open a channel, to curate channels to make sure that they are well connected to the network. Those are all details that I would like to hide as much as possible from the end user, because while important for your performance and your ability to pay. They are also hard concepts that I, for example, would not want to try to explain to my parents,

Stephan Livera:

Of course, and obviously your focus is very deep technical protocol level, but do you have any thoughts on what is needed in terms of making lightning more accessible to that end user? Is it better ways to remote into your home node? Or do you have any ideas around that or what you would like to see?

Christian Decker:

I think at least from the protocol side of things we can do, we have still a lot we can do to make all of this more transparent to the user and enable, enable non tech savvy people to take to take care of a node themselves. So I wouldn’t, I don’t know what the big picture is at the end, but I do know that we can certainly abstract away and hide some of the details in the protocol itself to make it more accessible and make it more, more usable to end users as for the nice UI and user experience that we don’t have yet think that will crystallize itself out in, the coming months. And we will see some really good looking things from, from wallet developers. And obviously I’m not, I’m not a very graphical person, so I can’t tell you what that’s going to look like, but I’m confident that that there are people out there that have a really good idea on what this could look like. And I’m looking forward to seeing it myself.

Stephan Livera:

I think there’s a, there’s a whole bunch of different models, right? Because, you know, people who just want an easy something to just get started, something like Phoenix might be a good one for them. And then, you know, if you’re really more technical, then obviously you can go and do the full set up your own c-lightning and spark, or set up LND and Zap or whatever you like. So I guess it’s just kind of building out better options to make it easy for people, even if we know not everyone’s going to be capable to do the full self-sovereign style as we would like.

Christian Decker:

Absolutely. Yeah. It’s one of my pet peeves that I have with the Bitcoin community is that we have a tendency to jump right to the perfect solution and sort of shame people that do not see this perfect solution right away. And so this shaming of newcomers into believing that there is this huge amount of literature they have to go through before even touching Bitcoin the first time. That can be really, that can be a huge barrier to entry. And so I think what we need to have is a wide range of of utilities that, as the user grows in their own understanding of Bitcoin, he can he can upgrade or downgrade accordingly to reflect his own understanding of the system itself. We shouldn’t, we shouldn’t always mandate that only the most secure solution is the only one that is to be used. I think that there are trade offs when it comes to user friendliness and privacy and security, and we have to accept that some people might not care so much about the perfect setup, they might be okay with a decent one.

Stephan Livera:

Yeah. That’s a very good comment there. Also just wanted to talk about trampoline routing. So you mentioned this earlier as well. I know the ACINQ guys are keen on this idea though I know that there have, there has also been some discussion on I think this is on GitHub from some other lightning developers who said, well, I see a potentially an, issue there because maybe there might not be enough people who run trampoline routers, and therefore there’s a privacy concern there that, you know, all those mobile users will be doxing their privacy to these trampoline routers. Do you have any thoughts on that or where are you placed on that idea? Yeah. Do you have any thoughts there?

Christian Decker:

Yeah, so basically just to, just to reiterate trampoline routing is a mechanism for us for a mobile wallet, for example, or a resource constrained wallet to, to contact somebody in the network that offers this trampoline service and and forwarding a payment to that trampoline node. And when the trampoline node unpacks the routing onion, it will see, Oh I’m not, I’m not the destination and I should forward it to somebody, but instead of telling me exactly whom I have to forward it to, it is telling me the final destination of the payment. So let’s say I’m a mobile phone and I know very I have a very limited knowledge of my surroundings in the network, but I know that you, Stephan are a trampoline node that then I can, when I want to try Rusty, for example, I can look in my vicinity to see if I have a trampoline node.

Christian Decker:

I can build a payment to you with instructions to forward it to Rusty whom I don’t know how to reach. And then I send this payment and so when you unpack Iranian, you just receive it like usual, you, you don’t know exactly who I am, because I’m still onion routing to you. You unpack this onion and now see, okay Christian, this, somebody who has sent me this payment has left me 100 satoshis in extra fees. And I’m supposed to send $1 to rusty. And now I have 100 satoshis as a budget to get these get this to Rusty. And so I basically outsourced my route finding to you. Now what have you seen from this payment? You’ve obviously seen that Rusty is the destination and that he should receive $1 worth of Bitcoin.

Christian Decker:

But you still don’t know me. And we could go one step further and say, Hey, instead of having this one trampoline hope we can also chain multiple of them. So instead of telling you to go to Rusty I would tell you to go to somebody else who also happens to be a trampoline, and then he can forward it to Rusty. And so we can expand on this on this concept and make it an onion routed payment inside of individual onion routed hops. And so what does the node learn about the the payment he is forwarding? Well, if we do the, only this one trampoline hop then you might guess that I’m somewhere in your vicinity network wise. And you learned that Rusty is the destination.

Christian Decker:

If we do this multiple trampoline hops, then you will you will learn that well, somebody has sent you a payment, big surprise. That’s what you always knew. You can no longer say that it’s that I’m in your vicinity. I, the original sender because well, you might have gotten it from some other trampoline node, and you can also not know whether you’re the next trampoline you’re supposed to send to is the destination, or whether that’s an intermediate trampoline as well. And so we can claw back some of the privacy primitives that we have in, pure onion routing that is source based routing inside of the trampoline routing. But it does alleviate the issue of the sender, having to know, having a good picture of the network topology in order to send a payment first.

Christian Decker:

And so I think we can, we can make a good case for this not being much worse but much more reliable than what we have before, because we have also a couple of improvements that come alongside with trampoline routing, because for example what trampoline routing allows you is I can, let’s go back to the initial example of me sending to you, you being the trampoline, and then sending to Rusty. It means that once you get the instruction to send to the final destination, you can retry yourself. Instead of having to tell me, Hey, this didn’t work, please try something else you can do in network retries, which is really cool, especially for a mobile phones that might have a flaky connection, or it might be slow. We can outsource retrying multiple attempts to the network itself without having to be in the active path ourselves, .

Stephan Livera:

Fascinating. I think so, I guess if I had to summarize some of your thinking there, it’s kind of like think through a little bit more clearly about exactly what is your who are you doxing and what are you doxing to who rather, and if you haven’t doxed any personal information about yourself to me, well, then really what’s the privacy loss there? I guess that’s kind of the way to think of that. And so it might, maybe it would become the case that you know let’s call them the hardcore Bitcoin lightning people. They might run trampoline routing boxes in a similar way to some hardcore people run Electrum public servers just to benefit you know, people on the network.

Christian Decker:

Absolutely. I mean it’s not just because of the kindness of your heart that you’re running trampoline nodes. One thing that that I mentioned before is basically that you get rather a lot of fees in order for you to be able to find a route. So the sender cannot estimate how much it’s going to cost to reach destination. So they are basically incentivized to overpay the trampoline node to find a route for them. And so this difference then goes to the trampoline running node. And so running a trampoline node, or it can be really, really lucrative as well.

Stephan Livera:

Yeah, that’s fascinating. I didn’t think about that. That’s a good point. And so in some ways it’s actually even more incentive to do it, then say, running an Electrum public server because people don’t pay electric public service right now. So it’s actually even better in that sense.

Christian Decker:

Yeah. And it’s not really hard to implement. We can, implement trampoline routing as a plugin right now, basically.

Stephan Livera:

Yeah. That’s very fascinating. It’s a new way of thinking about it. Great. One other thing I was interested to touch on is people talk about privacy attacks on lightning and so on. And so one of them is talking about channel probing. And so the idea is that maybe you could explain it better than me, but my understanding is people construct almost like a false onion that they know cannot go through and then try to figure out based on that. And they sort of play, you know price is right or whatever, and they might try, okay, try 800 sats, try $8 and then figure it out based on, okay, I know roughly this is how much is available in that channel. But I guess my question is more just like people talk about some of this as like, okay, that’s, you know, that’s violating the privacy principles of lightning, but I wonder how bad is that really? Like what’s the actual severity or is it just losing some small amount of privacy in a small way that doesn’t really stop the network growing? Do you have any reflections on that?

Christian Decker:

Yeah, I do because probing was one of my babies basically. And I really liked probing the network, to be honest, I come from a background that is mostly measurements and probing probing the Bitcoin network. And so I was really happy when I, when I found a way to, probe the lightning network and see how well it works and how if we, if we can detect some some failures inside of the network. And so you’re right, that probing basically boils down to attempting a payment that we know will never succeed because we gave it a payment hash that doesn’t correspond to anything that the recipient knows. So what we can do is basically compute a route to whichever node I’m trying to probe. I will construct an onion and then send out an HTLC that cannot possibly be claimed by the recipient.

Christian Decker:

And depending on the error message that comes back, whether the destination says, Hey I don’t know what you’re talking about, or some intermediate node’s saying, Ooh, insufficient capacity. We can determine where, how far we got with this probe. And and what kind of error happened at the at the point where it failed. And so we can learn something about the network and how it operates in the real world. And that’s invaluable information, for example we we measured, how probable a stuck payment is something that has been, has been dreaded for a long time. And it turns out that that stuck payments are really rare. They happen in 0.18% of cases for payments. It’s also really useful to sort of estimate the capacity that we have available for sending payments to a destination.

Christian Decker:

And that’s something that we’ve done for the pre split analysis, for example, where we said, okay anything below 10,000 satoshis has a reasonable chance of success. Anything above might might be tricky. So we split before even trying anything we split right at the start into smaller chunks. So, those are all upsides for probes, but I definitely do see that there is a downside for probing, and that is that we leaked some privacy. Now, what privacy do we actually leak? It’s basically the channel capacities and why are channel capacities dangerous to be known publicly well that it could enable you to trace a payment through multiple hops? So let’s say for example we have channels A, B and C that are part of a row. And along these three channels, we detect a change in capacity of 13 satoshis.

Christian Decker:

Now 13 Satoshis is quite a specific number. And the probability of that, all belonging to the same payment is quite high. But for us to make this, this collate, this information into reconstructing payments based solely on observing capacity changes, we also need to make sure that that our observations are relatively close together, because if an intermediate payment come through that might obscure our signal, that allows us to collate the payment. And so that’s where where I think that MPP payments can actually hugely increase privacy simply by providing enough noise to make this collating of multiple observations really hard, because channel balances now change all the time. You cannot have a channel that that is, that is constant for hours and hours, and then suddenly payment goes through, and then you can measure it instead you have, you have multiple payments going over a channel in different combinations.

Christian Decker:

And the balances of those of those changes cannot be collated into, into an individual payment anymore. And that then is combined with efforts like Rene Pickhardt’s just in time rebalancing, where you obscure your current balance by rebalancing on the fly while do, while you are holding onto an HTLC. And that can then pretend to be a larger channel than it actually is simply because we rebalance our channel on the fly. And so I think probing can be really useful when it comes to measuring the performance metrics for the lightning network. It could potentially be a privacy issue, but at the time frames that we’re talking today, it’s really improbable to be able to trace a payment through multiple channels.

Stephan Livera:

Yeah. I suppose, especially with MPP, and especially once you add these other, all these different layers and things into it just, yeah, it seems a bit like a very minimal, quite a low risk, I guess. But yeah, look Christian, I’ve really enjoyed chatting with you. We’ve almost gone two hours at this point. So, but I’ve definitely learned a lot and I’m sure SLP listeners will certainly appreciate being able to learn from you today. Christian, just for any listeners who want to find you online, where can they find you?

Christian Decker:

I’m @CDecker on github and @snyke on Twitter.

Stephan Livera:

Fantastic. Well, I’ve really enjoyed chatting with you. Thank you for joining me.

Christian Decker:

Thank you so much. Pleasure as always and keep on doing the good work.

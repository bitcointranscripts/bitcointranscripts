---
title: SLP321 On-chain scaling with Bitcoin Core Developers
transcript_by: Stephan Livera
speakers:
  - Pieter Wuille
  - Andrew Poelstra
  - Andrew Chow
  - Mark Erhardt
date: 2021-11-16
media: https://stephanlivera.com/download-episode/4089/321.mp3
---
podcast: https://stephanlivera.com/episode/321/

Emcee:

All right. I’m really excited for this next panel. I’ve heard some of them speak in different rooms and I can’t wait to hear what they all have to say today. Next up, I’m going to bring up our moderator. He has a podcast. It is a self-titled podcast and he’s also the managing director of Swan Bitcoin International. Please everybody, welcome to the stage Stephan Livera, everyone.

Stephan Livera:

All right, thanks very much for that. I’m excited for this panel. We’re going to be talking about scaling Bitcoin on-chain and we’ve got a really all-star cast to join us. So I’ll just quickly introduce our speakers. We’ve got Pieter Wuille, he’s from Chaincode and he is a very well-known Bitcoin Core contributor. So welcome to Pieter. We’ve also got Andrew Poelstra. He’s the Director of Research from Blockstream, also a Bitcoin Core contributor working on a lot of research. We have Murch joining us from Chaincode. He is the mempool weatherman and he loves talking about UTXOs and coins, and so he’s a great guy to join us for our panel. And finally, we have Andrew Chow from Blockstream as well. Andrew is a Bitcoin Core contributor and he is Mr. PSBT, HWI as well, and works a lot on the Bitcoin Core wallet. All right, guys. So thank you very much for joining us. Certainly this is really—just for people who aren’t aware—this is a very talented panel, so I’m definitely bringing down the average IQ here, but I’m here to ask the questions that you guys might be thinking of. And so we’re talking about scaling Bitcoin on-chain. So maybe let’s just start with each of you: in your own mind, what do you see as the key challenges and constraints around scaling Bitcoin?

Pieter Wuille:

That’s a hard question.

Murch:

Well, first of all, we are looking at a gossip network where every single participant has to know about all that is going on. So this very popular early narrative that we will just put all payments on the Bitcoin blockchain certainly is not going to scale. And so once you’ve gotten this fundamental truth down that block space will be limited in some fashion, you can think about how you want to go from there. And I think that’s maybe a good starting point for on-chain scaling.

Andrew Poelstra:

Yeah. I could maybe try to split things up a little bit. The two big areas of on-chain scalability that I think people care about are, as Murch said, you have this peer-to peer-network, you’re trying to communicate transactions in real-time to everybody across the world. That’s something I don’t know anything about. The peer-to-peer part of Bitcoin really scares me. I’m really glad that other people on this panel are thinking about that. And the other side, which I feel like I understand a little bit better, would be the scalability related to verifying the actual data that’s on the chain. How much space do you need to store the blockchain? How much bandwidth do you need to download it? And then how much computational time do you need to process all of that? Both in real-time—as blocks come in—can you keep up, and also when you’re onboarding, how can you verify that the history from 2008 onward is what you expect it to be?

Andrew Chow:

One thing I would like to mention is that, as Murch said, Bitcoin is a gossip network. So sending one piece of data from one node to another, well that goes to all nodes. So if we send one megabyte that might end up being several gigabytes total in network data just for the same message. So one thing that we really care about is efficiency. We want to have things that are compact and do a lot so that we’re not sending a ton of data everywhere.

Pieter Wuille:

I think what I’m really hearing here is: blockchains, conceptually, don’t scale. It’s all about trade-offs and we’re really talking about a system where fundamentally we want every full participant to hear and see and validate everything. And that is fundamentally a very hard-to-scale problem, and I think that the examples being listed here—we’ve really been talking about ways in which it doesn’t scale. And I think that the challenges to overcome are really restricted to, on one hand, incremental improvements—just improving the constant factors here and there—and in some ways not scaling on-chain.

Stephan Livera:

Yeah. So maybe I can just set a little bit of the context and the gentlemen on the panel can expand a little bit. So as we speak today, the blockchain is roughly 427 or 428 gigabytes. So that means if you want to sync up a full node, that’s how much you’re downloading. And as we know, Bitcoin blocks on average are 10 minutes. And let’s say on average, each block has about 2000 transactions in it. And so that’s like a rough—where we’re at today. So what does it look like then for people who, like you were saying, Andrew, they want to verify the full chain. Could you maybe outline a little bit about what that looks like in the future?

Andrew Poelstra:

Yeah. Well let me outline what it looks like in the present, and then I think I’ll be the representative of moon-math here and try to suggest that we can make everything better so that Pieter doesn’t bum everyone out too much with the truth and engineering constraints. So right now, if you’re joining the Bitcoin network, what you need to do to verify that the current state of the chain—where all the coins are, which coins are assigned to which addresses, and so forth—is you need to download the entire history of the chain. You don’t need to store it necessarily, but you need to download it and you need to verify every single transaction that’s ever happened. Historically, there have been, the last I checked, on the order of half a billion transactions in total on the Bitcoin network. And each of those has a couple ECDSA signatures, those take maybe 50 microseconds to verify. There’s also, when a coin is being spent, you need to keep track of the set of unspent coins, look that up in your database of unspent coins, remove coins that have been spent, add coins that are being created, and you can think of a transaction as kind of a diff on the set of unspent coins. And so you need to go through that for the entire history and check. Not only do you need to play forward, all of those diffs in a row, but every single individual diff—every single individual transaction—you need to verify that the signatures are valid, if the signature is couched in a more complicated script you need to verify a script was executed correctly, and so on. And so that doesn’t work today, right? It’s kind of a slow process. So if you have all the data, even with no bandwidth constraints, if you have a top-of-the-line computer and you try to verify the Bitcoin blockchain from scratch, it’s probably going to take you several hours. And when you do that, actually—this is kind of a dark secret—but you aren’t actually verifying the ECDSA signatures for many of the older transactions, more than a couple of years older, unless you take specific actions in order to do that. And if you did, I would guess that it would probably take you a couple of days, even with a very powerful computer—like a retail computer but still a very powerful one—it would probably take you a couple of solid days of computation to go through all of that.

Andrew Chow:

Actually, not that long I think. So Jameson Lopp every year does a full sync from scratch with all the optimizations turned off. And I think his most recent one was like seven hours and change for a full sync. But his computer is also a little bit more than your average computer, but it’s not like—it’s more like workstation-grade, not your consumer computer—but it does it in about seven hours.

Andrew Poelstra:

Yeah, cool.

Stephan Livera:

If you could maybe explain—I presume you’re talking about Assumevalid?

Andrew Chow:

Yeah so he does it with assumevalid=0.

Stephan Livera:

For people who aren’t familiar, what’s assumevalid?

Andrew Chow:

Assumevalid assumes that signatures and scripts are valid up to a certain block hash. So this saves on all the time verifying those. It can be turned off. If there’s a reorg that reorgs out that block, then it will be off, in which case you are verifying all scripts and signatures.

Murch:

So basically you’re still building the full UTXO set from scratch by looking at the diffs, like what coins are being spent and what new coins are being created. But you assume that it wouldn’t be in the blockchain unless the signature was valid up to a certain point.

Pieter Wuille:

I guess this is the right point to mention work on improving that. So there’s Assume UTXO project—James O’Beirne is over there who’s the main guy driving that today. So let’s take a step back and think about why is it okay that we don’t validate signatures? And the obvious reason is, well, you are already trusting the software you’re running. You’re getting it from somewhere, there’s hopefully review about it—at least in Bitcoin Core we have a whole process where people attest, like you yourself can redo the build that builds Bitcoin Core from source and verify that the binaries being published exactly correspond to that source code—and so you have some necessary trust in how you get that software, and what that software is doing. This is just inherent, right? You will not be doing the validation ECDSA signatures in your head. And so given that we have this process of review, we’re using effectively the same process where every major release—so every half a year—the hard-coded hash of the block up to where we know signatures are valid, is included in the software. It is placed several weeks in the past. Even at the time of release, there are several safeguards—like it only triggers when there’s actually a chain that includes that block. And I think two weeks on top of it and so forth. But what I want to stress is you’re trusting the software and you’re trusting the people writing the software or the process around it and the review. So we can use that same process to verify [that] we know all signatures of this hash are valid. And so going forward, is it really necessary that we process all the historical blocks? Can’t you just get the result of applying all these patches, as Andrew explains it, as a starting point? And so that’s what the Assume UTXO process is about: allowing you to skip that process. It’s unclear where you’d get it, but distributing data is not a hard problem and the Internet does it everyday and you know the hash so it doesn’t really matter that much.

Andrew Poelstra:

So for some historic context, you probably remember on Bitcoin Talk in like 2010 and 2011, there were people hosting torrents of the Bitcoin blockchain that you could download. You could download the blockchain data from BitTorrent and then start your node off of that. At the time, I guess BitTorrent was better than the Bitcoin peer-to-peer network for downloading this data. That’s probably not true anymore, but certainly at the time it was. And so you download this data, you start up your node and you can query your node and say like, What do you think the latest block hash is? What do you think the state of the UTXO set is? And actually, if you know the block hash and you trust that your software is running correctly, that actually implies the exact state of the system. So all you need to do is ask your node, what do you think the latest block hash is? Ask, well, somebody you trust, if you weren’t downloading it from the peer-to-peer network itself, is this the right block hash? Is this the longest block hash? Is this the tip of the longest chain that anyone’s seen? And you can basically download the chain without needing to go through Bitcoin using the peer-to-peer network to sync yourself.

Murch:

I’d actually like to circle back to our previous topic. So Stephan earlier said that we fit about 2000 transactions into a block. And since we’re talking about on-chain scaling, I’d like to sort of push back on the unit of scale transaction, because one of the things that has actually significantly helped in scaling up payments on the Bitcoin network was that a lot of especially enterprise entities have started batching payments into transactions. So the average size of transactions has gone significantly up because—especially enterprises doing withdrawals and batches—have been starting to send transactions with like 200 outputs to pay 200 customers in one transaction. And since the input size is so significantly bigger than the output size, where you would have one input maybe, and two outputs to make a single payment, one output to pay the recipient and one to return change to yourself, when you paid 200 people in a single transaction, you have only one single change output instead of 200, and you might need five inputs to fund a transaction. So by using the block space when it’s cheap to consolidate and then making payments that are very thrifty by batching them, actually has significantly scaled up the payments per block space.

Stephan Livera:

Yeah, that’s a great point. And I think very much worth thinking about is that the number of transactions is not necessarily the number of payments. So in that example, let’s say I’m some big exchange or I’m Cash App. I’m sending out that batched payment as all these customers are withdrawing all in one transaction. So it might be a hundred customers who are receiving some of their coins. So that’s one way to think about the scaling of it.

Pieter Wuille:

Yeah what you’d observe if—I think the point that Murch was trying to make—you would see the number of transactions on-chain going down, but each transaction would be more than proportionately doing more payments. So I think that that’s pretty fundamental that if we’re talking about capacity on-chain, scaling that really corresponds to being able to do more per bytes on-chain and maximizing that, really, rather than the number of transactions.

Andrew Poelstra:

That’s maybe a good segue into talking about Taproot, if you want to talk about maximizing bytes on-chain. I don’t want to steal Peter’s thunder so I’ll let you—cool, then I will. So Taproot is a new proposal for Bitcoin—I guess it’s not a proposal, it’s going to activate in like 10 days. So it’s happening. And the premise of Taproot is that your outputs would be represented rather than by a Bitcoin script or a hash of a script as they are now—they’re represented by a public key. And this reflects the kind of practical reality that most Bitcoin outputs are actually controlled by a single key that represents a single wallet who’s signing. But much cooler than that, it represents two big innovations that have shown up in the space over the last few years. One is that you can actually reuse a public key as a commitment. Rather than having to choose: do we have a hash of a script or do we have a public key—what should be primary? We can actually take a public key and just turn it into a hash of a script while still letting it function as a public key. And this is a cool thing, because it means that if you have a common non-public key case is that you have some happy path where some people own the coin. If they want to move it, even if there’s multiple parties, if they all agree to move it, they can go ahead and sign to move it. And only if there’s disagreement on whether the coin should move or not, then you need to go back to Bitcoin script and actually use a script. The Taproot lets you hide the script commitment inside of the public key and only reveal it in a case that is needed. And that’s kind of the Taproot assumption, is that it usually won’t. Then the second innovation that’s really cool is that it turns out [that] a single public key does not have to represent a single signer. You can have large sets of signers. In fact, you can have different signing policies. You could have a group of like five signers and say if any three of these five signers agreed to move the coins, then the coins should move. Normally you’d express that in Bitcoin script by using the check multisig op code in the scripting system and list out five different keys and say: three of them need to sign. With Taproot in principle, you could have a single public key that represented all five of the signers and you could do an off chain interactive protocol that would allow any three of them to then produce a single signature. So what you have on-chain now is just one key, one signature, basically, when the coins move. And this gives a tremendous scalability improvement because you are now getting more value per byte. One key, one signature, even if that’s like a 3-of-5 policy here. It also gives a privacy boost which is cool, because often there is a trade-off. Historically there’s a trade-off between privacy and scalability, where if you want more privacy, you’ve got to layer on more cool crypto. And cool crypto involves a lot of heavy computational stuff. And there’s a cool feature in Taproot—and in a lot of crypto, but not most of it—which is that: sometimes you can gain privacy by just not revealing information to begin with. Then there’s nothing to validate and there’s nothing to compute with. And so yeah, scalability and privacy kind of go hand in hand in that sense.

Andrew Chow:

One other thing with Taproot is—with the hiding the scripts part—if you have a script that is complicated and has many branches, a lot of those branches might not end up being used. Like you have an if_else statement, you’re either doing one thing or the other. In current Bitcoin script you have to carry both branches, even when one is not being used. Taproot lets you hide one of those behind a hash, and so we get to save a ton of space by just not having things we don’t need.

Pieter Wuille:

I think the slightly less technical analogy to give here is that of the court model. So if you think about the real-world judicial court system, the function of a court is to be present and, when people have disagreements, to have it adjudicate what the correct outcome is. But most things don’t get settled in court or aren’t decided by the court. It gets settled outside the court. And it even works there because the mere presence of the ability to go to a court actually is an incentive for people to behave honestly. And in a way we can think of the blockchain and the network surrounding it as an ultimate court that will always—when presented with the facts—make the exact fair decision that was decided by the contracts upfront. And in a way, Taproot is adding more of an ability to settle out of court because it adds a very cheap way of settling a transaction where everybody just agrees. And with this model of—well, I know if I’m being harmed by the counter-party, I can go to the chain—this is actually incentive for everyone to keep it cheaper and just sign and agree. And it’s more private.

Stephan Livera:

Perhaps an example then, let’s say in the Taproot world, if we had some kind of multisig with the five of us, the idea is using, as you were saying, the key path spend of where we all agreed that would be cheaper in terms of on-chain space. Or maybe Murch, you’re able to comment on this?

Murch:

Yeah, sure. So a key path spend costs about 58 vBytes, and let’s say you have a 2-of-3 multisig: even if it’s in the first level of leaves, it’ll be about 107 [vBytes], so significantly bigger to publish on-chain. So let’s say Andrew, Andy, and me are trying to have this 2-of-3 construction and they know that Andy and I can sign together. So we’ll probably be able to convince Andrew to just go along and do the key paths spend, because he knows already the outcome—the two of us will be able to spend together.

Pieter Wuille:

Also there is another session I think tomorrow with a Q&A about Taproot, specifically.

Andrew Poelstra:

I was then going to go jump onto feature stuff like signature aggregation.

Stephan Livera:

Yeah, let’s go there. Let’s hear that.

Andrew Poelstra:

Cool. Alright. So Taproot is happening—it’s in the future, but like in the actual future that will happen. So I have some thoughts about the other future that might happen. And I guess maybe the most immediate idea that—immediate like the closest to being real—that is past Taproot would be signature aggregation. And this is something that actually we originally were going to bundle into Taproot and we realized that there were a lot of technical questions to answer there that resulted in Taproot without signature aggregation being much simpler than Taproot with signature aggregation. And in the interest of deploying something that we were confident in, we scoped it down to what we were confident in. But the idea behind signature aggregation is this: rather than just using one key that then all these clever multisig constructions have one key represent multiple signers, suppose that across the inputs in a transaction—so now you’ve got all these different inputs in a transaction, each of them have have one key in the ideal case that maybe represents multiple signers—within the transaction, you have one key, one signature, times [multiplied by] every input. Suppose there was a way that we could actually combine the signatures from every input into a single signature? So the technical distinction here to make would be between this concept of key aggregation—where you have a whole bunch of signers and you want to represent them just in the most compact way possible—and if they’re all holding a single coin, well, one coin could have one key on it, so you want to combine all of their identities into this one key. If instead you have multiple parties or the same party multiple times controlling different coins, you can’t really—and when I say coin here, I secretly mean unsigned transaction output or UTXO, which is kind of the primitive object that the Bitcoin network uses to track coins—if there are multiple coins, you can’t really aggregate them in a meaningful way. They’re distinct cryptographic objects. They’re distinct output from distinct transactions.

Pieter Wuille:

Their outputs each have a key, which is already on-chain. Like you can’t get rid of it anymore at that time.

Andrew Poelstra:

So I’m setting the stage here to say: you can’t combine the keys. So Taproot is cool—you can combine all these keys—but you can only combine keys when you’re trying to receive coins all at once to a single address. In a single shot. If you’ve already received multiple coins or you have multiple parties who received different coins—kind of game over as far as compressing that any further—but when you spend them all together in one transaction, you still have room to use kind of the same crypto to combine all of the signatures. And so what you could have is basically one transaction—and then this gets cool, you can imagine an aggregate transaction like Murch is describing where you’ve got this massive transaction representing that spends hundreds of inputs and has hundreds of outputs and so forth—and rather than having a separate signature on every single input, you have a single signature that represents the aggregate of all those other signatures. And then a verifier trying to check this would—

Pieter Wuille:

Would effectively—not necessarily. One way of doing it is that the verifier actually, at verification time, does the key aggregation of all the published fees and then expects a single signature with the aggregate of all of them. That’s one way of doing it. It’s not the only one.

Andrew Poelstra:

That’s a good way to describe it, yeah. So then you get additional [space] savings. It’s cool, right? You can’t compress them when they’re sitting in the UTXO set, but at spend time, there’s still more room to compress there.

Murch:

Don’t get too excited, right? So signature data is already witness data. Witness data is discounted by a factor of 4. The signature is 64 bytes, so you save 8 vBytes, right?

Andrew Chow:

Okay. But if you have a lot of inputs, it does make a difference.

Murch:

Sure, sure. If you have a hundred inputs, you’re going to save 99 x 8 [vBytes].

Andrew Poelstra:

I’m getting more excited. It incentivizes the aggregation of transactions. But an unfortunate fact about Bitcoin today is that privacy would be improved if people would aggregate their transactions together more often in CoinJoin-type constructions, but right now you don’t really save a lot of space by doing this. You do, but you save like 8 vBytes in total or something by combining two transactions, because you don’t have to repeat the version byte, and you don’t have to repeat your transaction lock time. But signature aggregation changes this. And signature aggregation—if you have two transactions—then we would have to have two signatures. And if you combine them then now you have only one signature. And the more transactions that you combine together, for every one of those there’s an additional 32 bytes of data that you’re saving in addition to the 8 that you otherwise would.

Stephan Livera:

One question just on that. So let’s say in the signature aggregation idea, would that require more interactivity at the time of spending?

Pieter Wuille:

Yes. That’s an obvious restriction to this problem that as long as we’re using elliptic curve based cryptography, signature aggregation is inherently only possible when the signers cooperate. There are other cryptographic models that allow doing that non-interactively, so everyone can sign independently, unaware of the others, and then a third party without the keys can aggregate them into one. This is unfortunately not something we can do with elliptic curve cryptography. So signature aggregation is only possible across those signatures that are created with communication between the signers. At the same time, in the more common case, you’d use this when you have multiple UTXOs yourself, and you are the signer for all of them, or the signers for all of them are the same ones. So in that case, the interactivity is already there.

Stephan Livera:

So hypothetically, let’s say someone makes a wallet that can collaborate with other people using that same protocol. And in that way, that’s the interactivity of aggregating across—let’s say the five of us all want to spend at the same time—okay, now let’s aggregate, and let’s kind of put all that into one transaction and get those glorious savings that Murch is talking about,

Murch:

Yeah. Let me correct something. 64 divided by 4 is 16, and not 8. You’d save 16 vBytes per signature. And especially for what you write to the blockchain and what gets stored on every computer, you save 64 bytes. Because the signature is actually not there. So for the bandwidth that you use to transfer the transactions, you get to full savings, not the discounted saving. For the fees, you get the discounted savings of 16 vBytes. So actually every signature saved 64 bytes less data to write to the hard drive.

Stephan Livera:

So if I read you correctly then, it means every person who wants to download the full blockchain—the downloading requirement is less. And also the sats spent, it’s cheaper for all of us to participate in that way. So it’s cheaper in two ways.

Murch:

Right. So on the one hand this is super easy to do when you are spending multiple inputs yourself already and it would be natural to always do so. But the thing where it gets exciting is it encourages multi-user transactions, because now if multiple people collaborate in—let’s say both Andy and I want to send a payment and we know we’re paying the same merchant because we’re both buying a ticket to TAB Con—we would construct our transaction together and save together the additional cost of the other input.

Stephan Livera:

So I’m curious then as well—we’re talking about this idea—but what would be actually required for this kind of thing to become a reality?

Pieter Wuille:

So we’ll need probably something like a successor to Taproot that enables this, and this is really a successor in the sense that it will again be a new witness type people need to use. And this is not something that I expect in the real short-term to happen. So certainly don’t be like, Oh, we’ll adopt this once signature aggregation comes along. We can’t predict the future of when things may make it in, it depends on technical, logistical, political reasons, unfortunately. So what would be needed is—there are a bunch of ideas on how to do this. One is with—

Murch:

I mean, basically you need a new output type that, from the design get-go, allows [you] to construct transactions where you have a single signature for multiple inputs. Because currently that is not part of the Taproot rules, and with soft forks we can only ever tighten rules. We can add restrictions where previously more things were allowed after the soft fork. So doing this thing where there is not a signature on every single input, we would need an inherently new rule set. And one way that we would introduce that with would be to have, say, native SegWit version 2 outputs at some point that have a different output script-type that permits the single signature across all the inputs.

New Speaker:

It would also require changes to data structures to support one signature for many—or at least ACKing something existing data structure.

Pieter Wuille:

Yeah so the easy way of doing it, but unfortunately not the most useful one, is to do this with a new opcode in script. Unfortunately—or fortunately, depending on how you look at it—that approach really aims to not use script at all anymore. Our hope is that in most of the cases, the script part remains hidden and you just sign for the transaction. And that signature, that happy path, because it’s not in the script, it isn’t amenable to be extended with a new opcode, because there are just no opcodes involved. So other ideas that could be combined with this are things like graft roots, which is basically a way of delegating signatures—should we go into graph? Or—

Murch:

I think it’s a little hard to explain without some visualization.

Stephan Livera:

Yeah. So to your point around the not using opcodes, would it be that you could maybe, and tell me if this is wrong, would it be like, you’d say, Okay, yeah, we’re going to use script and opcodes because we’re getting this much of a saving and it makes it worthwhile? Or is it more like you’re just looking for a more technically precise or cleaner way to do that?

Pieter Wuille:

Your goal is minimizing on-chain data. With Taproot, the cheapest way of doing that is a key path spend, because the only thing that ends up on-chain is one signature—period. Our hope is to make something that uses even less.

Stephan Livera:

Yeah. Not something that uses more—

Pieter Wuille:

That first adds a script back and then use—

Stephan Livera:

Kind of un-solving the problem that has been solved.

Andrew Poelstra:

Another reason to not want to do signature aggregation inside of a script is that Taproot has a new kind of soft fork mechanism that we call OP_SUCCESS, or basically any opcode that is currently undefined in Taproot will immediately end processing of the input that’s being spent and say, Yeah, this input’s good. And the idea is that: if we later want to soft fork-in new functionality, we’ll take one of those OP_SUCCESS things and we’ll imbue it with some meaningful semantics. And so old nodes who aren’t updated will see this, they’ll say, I don’t know what this is—I guess it’s good. And future nodes that are updated will be able to actually validate the new rules. And the idea there is that no matter how crazy the new semantic of this opcode is, we can be assured that we haven’t done something that would cause old nodes to reject a transaction that new nodes accept. That’s a hard fork. That’s like, the network splits if people don’t all update it at once. And well, signature aggregation makes this harder, because you can imagine having OP_SUCCESS and then after that you have one of these aggregated signature ops. And now if you’re an old node, you can’t just stop processing there and then say, Well, this transaction is good, because you actually need that extra public key. Whatever extra data is associated with the signature that you need to aggregate, you need to know that. It’s not just changing a Boolean: this might pass or fail; it passes, we’re good. Now it’s: it might fail, or it might contribute a specific mathematical value to this aggregate equation. And that’s something that you can’t shortcut. Now that’s a complicating [factor].

Pieter Wuille:

Yeah. In short, in a signature aggregation world, you want soft forks to not only just restrict the rules within script, but also make sure that old nodes and new nodes keep agreeing about which keys are being aggregated. And script flexibility is just inherently making that harder, using the example that Andrew gave. And so I think the main line of thinking is that cross-input aggregation would mostly be happening on the happy path keys and not the ones inside script where it is fundamentally much harder. It’s also the ones where we care about it much more because that’s the ones we already expect the most.

Stephan Livera:

So then, as an example, if that were to come in, then people who are running Bitcoin Core and they want to be able to collaborate to lower their spend, how would the different clients find each other?

Andrew Chow:

It would probably have to be something user-initiated, like users talk to other people and they work [it] out.

Murch:

Yeah it would probably be out of band in some fashion.

Stephan Livera:

Gotcha. Yeah. So it’d be a separate way. So I mean, in the same way that like CoinJoin coordinates—

Andrew Chow:

Yeah it’s a similar problem to what Wasabi and JoinMarket kind of have to do to find [others].

Murch:

Or maybe a PayJoin or something would perhaps in the future be solved by a PSBT (Partially Signed Bitcoin Transaction), which is another mechanism or protocol with which you can construct multi-user transactions in the first place.

New Speaker:

So basically it would probably be part of a PSBT flow where you already were using PSBTs.

Pieter Wuille:

Also, this isn’t adding anything today. If two parties want to construct a transaction together, they are already collaborating, maybe not with as much interactivity that would be required to do signature aggregation, but they must be in communication already to construct the transaction. So the more interesting question is, Will we have higher layer protocols where, say, people can find each other purely for the reason of making their transaction cheaper and doing a CoinJoin or PayJoin or whatever?

Murch:

Also maybe besides the economic reason for doing this, one of the reasons would be, of course, that it changes how these wallets are perceived in relation to each other. If multiple users get together and build a transaction together, an observer might think that these were all held by the same entity and they clustered together. So in a future where we might be more concerned about privacy of wallets, it might be attractive not only for the economic costs, but the reduced costs always gives us a reason to do it. So it’s quite nice.

Stephan Livera:

Yeah. You wouldn’t necessarily be seen as a malicious person. It’s just: you’re just going for the cost saving as any normal person would if it’s available to them. Maybe that’s one way to think about it. Are there any other big ideas or any other key topics that you think we should touch on in terms of on-chain scaling?

Pieter Wuille:

Yeah. So we’ve been talking about signature aggregation, where we’re getting rid of some of the signatures that go on-chain, but there are multiple aspects to scalability and on-chain space is only one of them. CPU consumption is another, and it turns out you can sort of get something similar to a signature aggregation without actually doing it. That is, you still have multiple keys on-chain and you still have multiple signatures completely created independently on-chain, but you sort of aggregate them at validation time together and then validate them all at once. And it turns out you can do that somewhat more efficiently than validating multiple [ones]. And this is something that isn’t so much being done in this [way]. This is a known technique, like there are papers going back 15 years explaining how batch validation improves things, but in most settings it isn’t all that interesting. In our case, it very much is, because if we have a block with thousands of signatures in it, we really only care if all of them are valid or not. It’s not like we care if one fails, which one it is—the block is invalid, throw it away. So that’s really the use-case for batch validation. And Taproot and the Schnorr signature scheme it introduced have been specifically designed to permit batch validation. It’s not implemented, but it was a design criteria in BIP340, 341, and 342, that nothing in there would interfere with the ability to batch validate, which is the rationale for some of the maybe more unexpected changes. For example, that Taproot script logic doesn’t have a CHECKMULTISIG anymore specifically because the CHECKMULTISIG as it existed before isn’t compatible with batch validation.

Andrew Poelstra:

To add to that, the ECDSA signatures we were using before Schnorr signatures were not compatible with batch validation either. Maybe in retrospect, there were some small tweaks Satoshi could have done that would’ve made it possible, but they weren’t. And we thought about that when defining the Schnorr signatures for Taproot.

Stephan Livera:

And so, as I understand you then, would that be mostly a CPU saving?

Pieter Wuille:

Purely CPU savings.

Murch:

That would decrease the sync time.

Stephan Livera:

So you could spin up your Bitcoin full node faster in a batch validation world, theoretically?

Murch:

Well only for the batch validated signatures.

Stephan Livera:

Yeah not the past stuff, obviously, because that would still be—

Pieter Wuille:

So this is also—we’re not in a rush about that because it only becomes relevant once Taproot signatures are really commonly being used.

Murch:

Right. But then of course, once you implement it, it would still apply to all transactions from that point onwards [in order to be] compatible. So once Taproot rolls out and there are Schnorr signatures in the blocks, if you later then do the batch validation, you get all [of them].

Pieter Wuille:

And it is not restricted to initial synchronization, of course. It also helps with a new block that comes in or a new transaction that comes in—mostly new transactions because we cache the result of signature validation and we don’t do it again.

Murch:

I have another small topic to touch on for on-chain scaling. One of the interesting things we’ve seen this year is that suddenly in the middle of the year, the mempool stopped backlogging as much. And I’m still looking for somebody to change my mind on that, but my hypothesis is that this is simply due to the smaller inputs and that the average input size has decreased so much. So we saw this year a very significant adoption of native SegWit inputs. And the average input size I calculated has roughly decreased from 126 vBytes to 107 or 108 vBytes. So just by having inputs that are 15% less weight, I think that we can fit a bunch more payments and about the same volume of payments can now easily fit into our blocks. And our mempool clears much more often.

Andrew Poelstra:

Yeah, I guess if this were a 2017 panel and we were talking about the interaction between the fee market and the block size, that’s kind of a surprising non-linearity, because 15% sounds like, “15% is cool.” You know, you can put it in your release notes and stuff, but you wouldn’t expect it to result in qualitative changes in the way the network operates. But it does, you get this non-linear benefit to being able to cram more meaning into every byte.

Pieter Wuille:

It really depends on the relation between supply and demand. And if you’re right at that level where you had more before, and after—by removing 17%—you are below, you get the dramatic difference between the mempool clearing and the mempool not clearing, which is the difference between basically no fees and whatever people are willing to pay. So I don’t know if that’s the only reason though. I feel like probably the ecosystem just has matured more and is more using RBF and other—

Murch:

Yeah, RBF transactions are also up to 25% now.

Andrew Chow:

it’s just changes in wallet behavior, and a bunch of other things within wallets can have an outsized impact.

Stephan Livera:

Yeah. So I guess it’s like saying essentially: on the margin, because more people are using native SegWit and batching and maybe some Lightning use, and maybe people are a bit smarter about when they spend, all of these things have driven this outcome.

Murch:

I mean also fee rate-based input selection, right? If you use fewer inputs at high fee rates, the peaks of the mempool will be significantly lower because people add less data when the fees are already high, and then it levels a little more up during the time that the mempool is empty because people use more inputs then. So it shifts transaction data from the high fee rate times to the low fee rate times.

Pieter Wuille:

Also, much more dumb: just better fee estimation.

Andrew Poelstra:

Yeah. And can Andy talk about Bitcoin wallets dropping change outputs more frequently?

Murch:

So when you build your transactions so that you do not have to create change outputs, when you hit exactly the amount of funds that you need to pay to the recipients, your transactions are slightly smaller. You create fewer pieces of Bitcoin in the first place that don’t then later have to get spent again. And some of the players in the space have introduced UTXO selection algorithms that explicitly seek for these sort of input sets when they build transactions. One of them was that Bitcoin Core merged a few pull requests this year that had been open for quite some time, and they introduced this behavior into Bitcoin core. Now, I don’t know exactly how many people are using Bitcoin Core because—

Andrew Chow:

I also don’t think that would really have a significant impact on transaction sizes, because even in simulations I’ve run, it’s not that many that have changeless transactions.

Murch:

Well, 4% more transactions without change is almost—anyway.

Andrew Chow:

4% is 4%.

Stephan Livera:

Yeah. So we’ve only got a couple of minutes left guys. So maybe if each of you could just give a quick summary of where you think things are going? What do you think are the most fruitful pathways for research and development?

Pieter Wuille:

I think that despite all the very interesting technical ideas, the most impactful one is how people use wallets and expectations around capacity of on-chain transactions and alternatives to it.

Andrew Poelstra:

I think in the third kind of future—that probably won’t happen—there’s some new technology involving zero knowledge proof that we could, in principle, use to compact the entire blockchain into a compact proof that people could verify that would let them do initial block verification effectively instantly. This is what people want to hear.

Murch:

He did say he doesn’t think it will happen.

Pieter Wuille:

So the [AssumeUTXO] project is an idea in that direction.

Murch:

I think the biggest saving for blockspace is just not creating transactions.

Stephan Livera:

Yeah, just don’t spend. Just HODL guys, just HODL. Okay guys. So we’ve pretty much got to wrap up. Maybe Andrew, if you just got a last quick comment and then we’ll wrap it up.

Andrew Chow:

My main thing is just that finding smarter ways to use the space that we already have instead of trying to increase sizes, we can think of new ways that use every byte more efficiently.

Stephan Livera:

Right. To be more efficient. All right, guys, this has been an excellent panel. Thank you. Everyone give a round of applause for our panelists. Thank you very much.

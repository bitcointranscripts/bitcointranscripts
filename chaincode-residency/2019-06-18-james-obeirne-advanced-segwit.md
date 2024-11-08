---
title: Advanced Segwit
transcript_by: Caralie Chrisco
tags:
  - segwit
speakers:
  - James O'Beirne
date: 2019-06-18
media: https://youtu.be/JgNgnwF9hfY
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-18-james-obeirne-advanced-segwit/
---
Location: Chaincode Labs 2019 Residency

Slides: <https://residency.chaincode.com/presentations/bitcoin/Advanced_segwit.pdf>

James O'Beirne: To sort of vamp off of Jonas's preamble, I'm not that smart. I'm a decent programmer, but compared to a lot of people who work on Bitcoin, I barely know what I'm doing. I kind of consider myself like a carpenter, a digital carpenter equivalent. I'm a steady hand. I can get things done. I'm fairly patient, which i s key when it comes to Bitcoin Core development because, trust me, you're gonna be doing a lot of waiting around and a lot of rebasing. But fundamentally, I don't think I'm that smart, so that's why this talk is low-budget.

Two things working here. Not only am I not that smart, but SegWit's an incredibly robust topic in Bitcoin. It basically encompasses every component of the system from the peer-to-peer layer, game-theoretical aspects, commitment structures, migration paths, activation, politics. There's a whole lot going on there. So when Jonas asked me to do an advanced SegWit talk, there's a lot of leeway there. With Segwit in particular, I find that when I was in your shoes about a year ago, I had been like in the Bitcoin ecosystem for a few years and you know I had done a few pull requests and stuff and was following SegWit casually, but I found that I really had to review the fundamentals and the basics of Segwit numerous times to really get it through my head. So what I'm hoping to do is go through some of the basics of SegWit and then once we do just a quick review of that, maybe we can move on to a few snippets of code that are kind of relevant that will allow you to dig in a little bit more into the particulars hopefully give you an intuition for how you can go off and study some of this stuff yourself.

We have a few people in the audience who honestly probably have a deeper insight into some of the design choices than I do. Marco and James C, and I'm sure a lot of you at this point are really fluent. I'm hoping to judiciously lean on you with questions.

So let's jump into the basics.

# Malleability

Fundamentally what are some of the features of SegWit? What does it do? Who can tell me about the malleability end of things?

Let's say Fabian.

Fabian: There were several ways to malleate transactions before SegWit came around. Several of those would have been fixable without Segwit, with some standardization. Some of them weren't, and Segwit fixed those by separating them out.

James: Yep, that's all correct. But backing up, I guess what's the problem with malleability? Why is that an issue? Why is it a problem that basically you can take a transaction that's yet to be confirmed with one ID and create sort of an equivalent transaction with an alternate ID?

Felix: If you replicate that, if you store the transaction ID in your database, and then you say you paid out this person already, and then you look at the confirmed transaction, and they never confirmed it. They might say, this transaction was never confirmed, send me my money, then you've hit it twice.

Audience Member: Also, if you're building dependent transactions on that original one, off-chain.

James: Crucially, this is important for Lightning because with lightning and similar schemes, we're kind of setting up these dependent chains where you have to have some reliability in terms of the identifier. Allegedly, back when a lot of the early Lightning discussion was happening, I think there was some kind of way of getting around malleability, so if SegWit hadn't have come around, we can still maybe have Lightning. Does anybody know how that scheme worked?

Elichai: There was BIP62. It fixed everything except the problem in the signature. In the end, someone can regenerate the signature. So long as the signature was part of the transaction itself, we couldn't really do it.

Felix: Nobody else, nobody outside who had a private key to sign for that transaction could maleate it.

James: Antoine, what's BIP 62?

Antoine: BIP 62, it's a try to fix malleability issues, around nine of them. Like he said, the last one, not fixable at all. The main thing that Sipa tried to do with BIP 62 was fixing third-party malleability. There are two different types of malleability. There is malleability by the one who signed the transaction and malleability by people relaying the transaction to the network.

James: You guys are really good. So fundamentally, what SegWit does to prevent this malleability is it segregates the signature data and creates two different identifiers schemes. Its first serialization format here is sort of like the classic TX ID serialization. What's a subtle distinction here to note is that previously the signature data was embedded in this txins data structure here, so you'd have all your signature data as the script sig and then in this WTX ID format here this witness transaction ID format. The witness is actually pulled out of the txins and into this witness structure. The witness structure is like a list of lists where each element in there is a witness stack that corresponds to each txin. And it's important to note that for all the txins here, and witness native transaction, the script sig is empty so that's why it can't be malleated. When we have a native SegWit transaction, we still use both of these ID formats, and this one can't be malleated because there's really no signature data in there. James?

James C: I never understood why the witnesses were aggregated in a vector at this end. Why are they not so part of the txins? We have a marker that tells us this is a different serialization format.

James O'B: I guess what you could do in that case, is assuming you wanted the witness data to actually still live in line with the txin, you could have some procedural parsing routine that would go through and strip out that data if you wanted to compute the TXID. Whereas I guess here...

James C: Got it. It's really to like easier txid...

James: There's just less processing, I guess. Because you can just say, use this offset. Disregard everything after that and then pick up the nLock down at the end.

Marco: Yeah, I don't know the reason. My guess would be it would be easier to create transactions that are both valid to deserialize it. If you're allowed to put in the witness, which is basically random average within txins. The reason for the mark on the flag was to generally make transactions invalid to deserialize it. It doesn't work always, but...

# Quadratic Sighashing

James O'B: The next feature of SegWit is a fix for this quadratics sighash problem. Basically, the idea there at a high level - is anybody familiar with this? Luccianna do you know what's going on with quadratic sighashing? Amiti? No? Alright, good. Finally, something you guys don't know.

So the issue with quadratic sighashing is that you can construct these transactions that take sort of a pathologically long time to validate. The way that you do this I think in practice is creating a really giant multisig transaction and what's happening is when you're trying to validate the spend of this transaction you have, say some subset of keys, and you're trying to figure out if those keys cover the required script pubkey. Does anybody else have any more insight into this?

Audience Member: I thought we talked about that yesterday. I don't know if it was multi-sig though.

Felix: I think it's O(n²). So 1n is like the number of inputs. So if that grows, you have to hash more, but since growing the amount of inputs, you also grow the size of the transaction. You also have to hash more, and then you have to hash it for each input because each input might be different. There's a different transaction hash you can reuse the transaction hash what you signed for that.

Audience Member: Because one signature includes information about the other somehow, is that?

James C: The previous pubkey script, I have to rehash the whole darn thing every input. I can't reuse that hash. So as the transaction grows in size the hash operation for every individual input will also increase, so it becomes quadratic.

James O'B: Yep. That sounds right. To be honest, I don't really know what Segwit does to fix this. There's some kind of caching that happens.

Felix: It's like one hash for that transaction, and that's what you're gonna sign no matter which input I think.

Audience Member: So it's linear, not quadratic.

# Better Hash Security

James O'B: Alright well, I'll gloss over that. There's better pay-to-script-hash security, so does anybody have any idea why this would be? Timo? This is kind of a subtle one. I didn't really realize this is the case until I went back and reviewed in the last few days. The idea here is that with the sort of legacy pay-to-script hash, you're taking some encumbrance script and you're hashing it and saying, "Okay, so when you spend this coin you basically have to present me a script that hashes to the same value that I committed to as well as evaluating it to true." And that hash we actually use HASH160, which targets a range of 20 bytes. In SegWit, that commitment is actually 32 bytes, so you're getting the full security of SHA-256 versus some kind of reduction.

Elichai: Yeah, I just want to say it's more than the amount of bytes. In RIPEMD, you can even lower the security. In SHA-256, right now, no one knows how to lower the security.

James O'B: Why is that?

Elicahi: Because RIPEMD has been with us longer, so there is more research into it, and I think they even came up with a way to make it 80-bit security. 80, like half of the 160, still not breakable yet. SHA-256 right now, there isn't real research that can lower the security. There will be probably. So it's more than the amount of bytes. It's actually a different algorithm that's right weaker.

James O'B: I guess just as a sort of thought experiment assuming that RIPEMD was prone to such an attack...

Audience Member: Isn't HASH-160, SHA and then RIPE?

James O'B: You take some subset, RIPE projects it into a smaller space, so there's a high likelihood of a collision.

Felix: But you still have to find a collision?

James O'B: Yeah, I guess given the certain insecurity here, who can give me a practical example of how you would attack this?

Audience Member: I guess like you were saying, you'd have to find a collision with a script that was different than the one that it was signed. Brute force or otherwise.

James O'B: So at the time of deployment, I think Pieter noted that currently, a sufficiently motivated attacker with a lot of resources could actually find collision because it's like you said, it's like 80 bits of security and at the time at least he said that that was that amounted to a few weeks of the global Bitcoin hashrate. Worth keeping in mind.

Audience Member: Although the Bitcoin network, just assuming somebody wanted to try that, they wouldn't have ASICs for that, right?

James O'B: It was sort of a theoretical point.

Cross talk...

Elichai: Like on the old ones, pay-to-public key for sure. But on the new ones, I don't think there's a billion dollars on any P2SH addresses.

James C: You'd have to find the collision with an "anyone-can-spend script," right?

Audience Member: Or just spend it to yourself. You just make a script and spend it to yourself.

Elichai: That's harder than making them find the collision. You need to find the specific collision.

Audience Member: You could have some random data that you're rotating.

Felix: You would probably say here that, "let's generate a 2-of-2 multi-sig", and then the other person thinks that it's a 2-of-2 multisig, but you have the same P2SH which is a 1-of-1 multi-sig.

John Newbery: Yeah, that's the attack which lowers it from 160 bits to 80 bits where you control the digest and it would lower SHA-256 to 128.

Elichai: But that's where it lowers it by two, but that's for a basic collision, not for a specific hash. From any hash of all of the range one of them to have a collision that would be a birthday attack. And not to take a specific hash rate that it's not a birthday attack as far as I understand.

Felix: It's easier if you try to don't attack a specific…

Cross-talk...

# Script Upgradeability

James O'B: So, the next feature is script upgradeability. This is a pretty simple one, but it's probably profound, especially when you think about Schnoor and Taproot and other upgrades on the horizon. Every witness program basically is namespaced by a version which determines how it will be interpreted. Currently any witness program that has a version that isn't 0 is evaluated as anyone-can-spend.

Antoine: It's not stronger to...

James O'B: There's a weird standardness flag that you can set where it'll basically fail and warn you. It's some constant called to discourage witness upgradability or something like that. The point is that basically, a door has been left open to create subsequent witness versions. This is a vast improvement over the script upgradeability that we had before because basically before, we were limited to redefining some of the unused opcodes, and that's a pretty limited set of things. And I think there were limitations around like the sort of arguments that those could take. Having that window for the upgrade of scripting letters is a big deal.

Audience Member: That's what BIP Taproot is building on?

James O'B: Yeah, SegWit version 1.

James C: I remember I think in our with calls, John proceeding this residency. Newer versions are being made that can pass standard policy. So today, if I have a version that doesn't exist, it's not standard. But I believe the next one's going to become standard before it's actually used. So when it does become activated, they'll propagate at the very end.

Audience Member: Spending to a version one address is standard, but spending _from_ version one is non-standard. It's the difference between saying sending _from_ and sending _to_. Originally both of them were non-standard, and now they make it you can spend to another standard one. Or make it standard.

James C: But then if I want to spend it, it won't propagate. If nodes don't upgrade...

Audience Member: You have to find miners that will accept it, I guess.

# Block Size Increase

James O'B: Finally, one of those notable features is an effective block size increase. In theory, blocks can burst up to four megabytes, but in practice, it's really just 1.6 - 2 megabytes, and that's based on the fact that we're discounting the weight associated with signature data.

Who has an intuition for how block structure differs in SegWit? Of course, like when you ask a vague question like that, nobody's gonna be like, "Oh, I have an intuition!"

Audience Member: I just imagine it as stuck to the end of whatever you consider the block, but I don't know if that's actually how it's done.

Audience Member: The coinbase doesn't have inputs, so they use the input space to fill it with...

James O'B: That's close

Felix: There is an OP_RETURN in the coinbase, which has a certain Merkle root where it's committed to the same structure but instead of using the transaction ID you use the witness transaction ID.

James O'B: Yeah, exactly. In every block -

Audience Member: Can you say that same thing again?

James O'B: We'll go through all of this. I have a nice graph from Jeremy Rubin at some point, but I think it's a little bit out of order.

Antoine: Which was - because at first, SegWit was proposed as a...

James O'B: A hard fork?

Antoine: Was there another Merkle tree or what was the hard fork design?

James O'B: Marco? John? Do you remember if we were just going to add a Merkle root to the block header? For a hard fork SegWit, before we realized we could just stick in the coinbase? Were they going to add it to the block header or…?

Felix: I think that was never formalized. It was just maybe an IRC...

James O'B: Have we talked about hard forks or soft forks yet? No? Okay.

Audience Member: In our prework.

James O'B: Timo, can you tell me how a hard fork differs from a soft fork?

Timo: Hard fork changes the rules; soft fork keeps the rules, but tightens them.

James O'B: So the hard fork, soft fork distinction is a little bit weird because you can have soft forks, so they're sort of like these velvet forks which are ostensibly soft forks, but they so change the way the system works, that it's kind of like a hostile softfork. But in any case, the very course distinction between a hard fork and soft fork is that soft forks constrain the rules the existing system, so everything that was invalid is still invalid, but hard forks basically open up the validity rules, so that's something that was previously invalid can now be valid. So hard Forks are sort of backward-incompatible. The trick with SegWit is that basically we want to add an additional commitment structure, but we don't want to do something like modify the block header because then previous clients are not going to be able to validate these new blocks that come in. So we want to retain backwards-compatibility, so we have to do something kind of clever like add that structure somewhere.

As you guys probably know, in every block, there's a coinbase transaction, which is effectively how the miner pays themselves. So we have this coinbase transaction, and it turns out that we could use one of the txouts to do an OP_RETURN. Is everybody familiar with OP_RETURN or no? Okay so OP_RETURN is just basically how you stick some unspendable data into Bitcoin. Numerous people have used this to embed various things in Bitcoin. Open timestamps. Somebody, I think split up the entire white paper PDF and embedded it using serial OP_RETURNs.

Cross talk...

You can do various things with OP_RETURN. One of the nice things we can do is use these txouts on the coinbase transaction to commit to a Merklel root that corresponds to all the witness transaction IDs. I think I've got some code here. This is a function. In this talk, anything that has like a dark background is the current code. Anything that has a light background is the at deployment time code.

This is a function called generate coinbase commitment in validation.cpp, which is where you'll likely be spending a lot of time if you pick up Bitcoin Core…. Basically, what we have here is we're saying if SegWit has been deployed and if we don't have some pre-existing witness commitment index in the block and we're gonna come up with our witness root, which I'll show in a second, and we're gonna SHA-256 that. And then we're going to stick it in the script pubkey of the first transaction in the block. I think that's gonna be the first txout, but elsewhere on the code we don't assume that it's always the first txout. It's just how we do it here.

So in terms of how we actually compute the witness Merkle root - are you guys all familiar with Merkle roots, or have we not covered that yet? Okay cool. Merkle roots, if I had to pick one piece of magic in Bitcoin that's my favorite by far.

The idea is that we basically take all the transactions in the block in a specific order, we add them as leaves, and then we can compute this Merkle root. So pretty simple stuff. That just goes in again an OP_RETURN and the txout out of the coinbase transaction, which miners have leeway to do whatever they want with.

# Witness Programs

Let's talk about witness programs. There are a few different templates I guess you could say that we have with SegWit. We have a pay to witness public key hash which is kind of like a special case for the common case of spending to a public key and so as you can see here that the witness just consists of the signature and pubkey. The script sig is, of course, empty because this is SegWit now, and so we don't have any in the scriptsig. The script pubkey is just an OP_0 and then the 20-byte hash of the public key. That's pretty straightforward.

For pay-to-witness-script-hash, the witness is the stack that gets evaluated with the script, and the script pubkey is just OP_0 and then the 32 bytes hash of you are evaluating.

Felix: why did we keep the Satoshi original vision for keeping one too many pops on the stack.

James O'B: That’s out of my pay grade.

Cross-talk...

# BIP 9 and activation

James O'B: Let's switch gears a little bit like that activation SegWit, which is some storied history. You guys have not yet covered BIP9, is that right?

Audience Member: I actually did a presentation on it.

James O'B: Oh, you did a presentation on it? Cool, so you guys should have some rough familiarity. The idea is that we've got this state machine that basically defines the way the deployment goes down on the basis of the version string that miner set when they create blocks. In the specific case of SegWit with BIP9 there was a 95% threshold that needed to be met of blocks created that signaled support “yes” for support for SegWit within a given retargeting period. For anybody who's around then and watching Bitcoin, I'm sure you had like your favorite site that you go to I think - mine was fork.lol - and you check desperately to see if that threshold was on track to be met and for a long time it wasn't.

So the idea is that basically there's some timeout period where this deployment would be proposed and if by some median time passed hadn't been signaled for sufficiently, then we go into a failed state. You basically say, well back to the drawing board. The ecosystem isn't supporting this change. But on the other hand, if you hit that threshold before the timeout, you enter this starting phase, and that basically exists so that you can make your way through this locked-in transition, which is as far as I can tell it's basically a buffer of time between, "Okay, we're gonna do this thing" and like" let's give it a few weeks or whatever for everyone to get ready for it." So BIP9 ended up being a little bit controversial. Can anyone speak to why?
Hugo?

Hugo: I think it gave too much power to the miners by setting the threshold too high in 95%. The user had no say in how to activate it. The ball was in the miner's court.

James O'B: So it was kind of agonizing because there had been all this fanfare you know there's this scaling problem and this malleability problem and a lot of the Core devs have gone off and scratched their heads for a while and come back with this proposal. I remember watching Pieter give the SegWit talk to at S.F. Bitcoin devs, and it was really exciting. It was like, "great, let's get this thing rolled out." Previously in Bitcoin's history, every upgrade or fork had been pretty unceremoniously accepted by miners. Partly because there was a small community and nobody really cared that much. So it was frustrating when the code is actually merging into the master, and there was just this euphoric feeling, but then you sit and wait and watch the versions go by, and it was just obvious. The signaling rate was in like 10% or 20% or something for a long time, and nothing happened. Obviously this kind of fomented some fire in the community, and then this personality called Shaolinfry showed up.

Shaolinfry proposed an alternate activation mechanism that it's sort of like BIP9, but instead of having this failure state that you can transition into if you actually time out, what his little patch does here, is it basically says, "Well OK, if we hit Tuesday the 1st August 2017 and SegWit hasn't activated then we're gonna start rejecting any block that isn't signaling for SegWit activation." I can't tell why but it's clamped between that Tuesday and Wednesday of the 15th of November 2017, so actually, that stringency only lasts for a few months. I don't know why that clamp exists because it seems like if you're gonna do that...

Elichai: I think that cause in the future, they would disable it. They would use that BIP for a different proposal. So if anyone still runs this code, it won't be forked off.

James O'B: That's a good point, yep.

Audience Member: November 15th is when BIP141 timeout was. If it's not locked in by then, it's game over.

James O'B: So this got a lot of buzz and riled a lot of people up, but it was not universally appreciated. For example, Suhas said on the milling list: "BIP 148 would introduce a new consensus rule that soft forks out non-SegWit signaling blocks in some time period. I reject this consensus rule as both arbitrary and needlessly disruptive. Bitcoin's primary purpose is to reach consensus on the state of a shared ledger, and even though I think the bitcoin network ought to adopt SegWit, I don't think that concern trumps the goal of not splitting the network."

His point was basically: that's a pretty coercive patch. If we really want Segwit, we can do that, but that's kind of a nuclear option, and it may be unnecessarily causing a consensus split. Why don't we be a little more patient and wait and try to build consensus? Does anybody have any opinions on this?

Elichai: I think the main goal of BIP 148 was to try and balance the situation because the way BIP9 works is all of the powers is by the miners. I'm not a miner. I guess you're not a miner. But we don't have anything saying this. I think this was a way to try and bring some of the power to the users of bitcoin, not just the miners. I agree that it's not the best way because in the end could have caused a fork in the network, but we need some sort of way like BIP 9 but for users to somehow like change what the consensus rules are.

Felix: I think it's worth going back to what BIP 9 actually said. The terminology is signaling, right? Reaching consensus on whether or not something should or should not happen is usually during the PR phase or the mailing list or even earlier, right? Once all the code has been written, I think the whole purpose of BIP 9 was just to like coordinate better the network, so we don't have this like this fork mess we had with. What was the soft fork before?

James O'B: CLTV?

Audience Member: No, there was something like the miners were spy mining, really like checking the validity of the full block rules. So they actually hadn't upgraded, and this was more like to signal, "oh yes, a sufficient part of the network has upgraded." So there won't be any like different header chains.

James O'B: So maybe out of scope of this discussion, I mean this is Bitcoin, so all of this stuff comes into play. It's almost like an anchoring effect in a negotiation where you sort of propose something dramatic that you don't necessarily intend on doing, but you know is a sort of a viable alternative to get the other person to kind of come this way. Maybe this was that. Nobody really knows who Shaolinfry was or whatever. He kind of writes like…. anyway. [Laughter]

Audience: It was kind of like a game of chicken between the miners and UASF (user activated soft fork).

James O'B: So BIP 148 didn't really take hold, so he released a subsequent BIP called BIP 8 debate, which also didn't get much traction. This proposed some alternative state machine, and I can't remember what BIP 8 did. But it didn't get much traction didn't go anywhere. So finally, a guy named James Hilliard, who works on mining equipment, proposed something called BIP 91, and this basically just reduced the activation threshold down from 95% to, I think, 80%.

This was never merged into Bitcoin Core. But I think - Marco, John is it true that there are some miners running this code?

Marco: I don't think any miner ran any copies of fork integration code. They just set the version with some flags or something.

Audience Member: From what I read, there were miners running, 2x, btc1. I think they did merge the equivalent of BIP9, like the signaling of version 4 of the blocks.

James O'B: Was anyone actually ever running SegWit 2X code?

Audience Member: I think they were, but I think this basically was the same thing that signaled the same block version in order to push SegWit through in Core.

James C: James, how do miners even assess what the users want? It would seem like the miner economically wants to provide the confirmation that the user wants. It would seem so, right? It seemed like at first, the user would signal with their preference, then the miners can make their preference, and then it either activates or not or we split.

James O'B: It would seem that way, and this is a great segue into what we're going to talk about next.

...

# ASIC boost

Let's talk a little bit about what ASIC boost is.

A guy named Jeremy Rubin, who you may have seen in the Bitcoin Core project, and more generally around the cryptocurrency ecosystem, put together a really nice write-up on what ASIC boost is and so I highly recommend going through and actually making sure you understand each step.

The short form of that is that miners discovered a kind of clever, sort of undetectable way of getting a slight advantage when trying to compute a nonce that would hash below the target. The way this works is the SHA-256 function happens basically in multiple rounds. You can cache parts of the computation of a SHA-256 function. Basically SHA-256 will split the input into multiple parts, and if you sort of cache the mid-state based on one of the early parts and then just tweak the later parts, you can save yourself some computation.

What it appeared was going on was miners were playing some interesting games in terms of rearranging the Merkle tree, and they could do so in such a way that they could generate collisions that would share parts of the Merkle hash in common with one another so that they could reuse this mid-state and basically get sort of an advantage when they were trying to mine a block. It turns out that obviously, SegWit modifies the commitment structure of the Merkle tree, and it does so in a way by adding this witness commitment to the coinbase output, which is always to the far left of the tree. It does so in such a way that it kind of obviates any way to do its manipulation of the Merkle tree to get an advantage.

That's called covert ASIC boost because you can't necessarily tell a priori that this is what they're doing, but we would see weird blocks that have like low numbers of transactions. I think there were a few invalid blocks that were mined based on ordering that kind of indicated that people were trying to play these games. We had an inclination that it was going on, and I think Greg Maxwell did some research where he actually cracked open a miner and saw that there was an ASIC boost functionality built in some of the ANT miners. So this would certainly give a sort of plausible reason why miners might be hostile to the idea of changing the commitment structure because if it's nullifying some advantage and that's a pretty big deal for them.

It turns out you can do a different version of ASIC boost called overt ASIC boost by playing with some of the data in the version header. But doing this makes it obvious that you're using this over an ASIC boost, and obviously, not all the version field is accessible for playing these kinds of games. That's ASIC boost.

Does anybody have any questions about ASIC boosts or any comments? It's pretty fascinating. When it was happening, it felt like a lot of intrigue, and it had a lot of interesting public relations stuff that came out of it. It was fun to read.

# Peer to Peer Implications

Let's get into some of the peer-to-peer implications of SegWit.

Over the wire, SegWit introduces a new transaction serialization format for communicating with peers, and that kind of mirrors the format that I showed earlier, the wtxid format. It's basically the same thing. Nothing big there. By the way, this is all outlined in BIP144, so the segment suite is BIPs141 through 144, 145. I think 145 might be likely to get blocked template change, which is kind of inconsequential, but the really important ones are 141 through 144. Like I said, you'll probably end up reading these a few times unless you're much smarter than me, which is definitely possible.

In terms of the hashes, like I said before, this is sort of your classic format, and this is the witness ID format that incorporates the witnesses explicitly in their own spot. This is just a quick note alluding to what I said earlier about the fact that I found it confusing because it's not necessarily obvious from these two that legacy transactions include signature data in the inputs. Witness transactions do not, but they still use this same ID because this is a non-malleable ID. This ID, because it contains signature data, is potentially malleable, but I actually don't know if that's even the case given how we restrict the signature data for SegWit. Worth noting.

We introduce a few INV types. You in the back there, do you know what an INV message is? Okay so does anybody else know what an INV message is? Jon?

Audience Member: I'm not a hundred percent sure, but it's in the p2p protocol of communicating where basically I think it's one of the most common message types. It's quite small. I think under 64 bytes. For example, you might send a GETDATA request, and you receive it back in the form possibly of an INV?

Felix: It signals you have a new inventory. And then the person might then respond with a..

James O’B: ...a GETDATA

Audience Member: If it's cool, then they send you INV, right?

Felix: If they don't have that inventory.

Amiti: An INV indicates I have something new, and if you want it, you ask me for it.

James O'B: An INV can contain a list of IDs and block IDs. Super common message.

...

James O'B: Just by way of general advice in your leagues of free time, you should definitely get acquainted with the different message types and how they work in the protocol. I think the [bitcoin.org developer documentation](https://developer.bitcoin.org/devguide/p2p_network.html) has some pretty nice walkthroughs of how these message flows go. But that's really helpful to have a good handle on, and it's a really great entry point into the Core codebase itself because if you understand those message flows, you can then read through net processing and subsequently into validation and then follow where the messages go, and that's a great way of exploring the codebase. Anyway, that's kind of off track.

Basically, we just introduced a few new INV types to use with GETDATA, where you're basically signaling, "Hey, I want a witness transaction. Yeah, I want a witness block in the new SegWit format."

Another thing that happened is we introduced this service bit, which is basically a mechanism for saying to your peers what parts of bitcoin you support. Other examples of service bits are like whether or not you're a pruned node, whether you can offer some blocks. One interesting thing to do is if you want to go through all the peer-to-peer implications of SegWit yourself, you just grab for this NODE_WITNESS, which is the constant associated with the SegWit service bit. We would do various things on the basis of whether our peers signal this the service bit. For example, [in the initial code](https://github.com/bitcoin/bitcoin/pull/8149/commits/b8a97498df1e83f8dcc49bc3fa4344f9e9799242#diff-00021eed586a482abdb09d6cdada1d90115abe988a91421851960e26658bed02R1679-R1682), we would only create outbound connections to nodes that signaled node witness. Unless we tried 40 different connections, failed all of them, and then we fail back to a non-witness node. This is obviously just because you don't want to partition yourself off of the network if you can't find any other witness nodes.

Nowadays, the code is a little bit more nuanced because we introduced this idea of feeler connections, which Ethan Heilman may have talked about when he was discussing the peer-to-peer eclipse attack resistant stuff. The idea of feeler connections is, we have some limited number of connections that we just kind of make free indiscriminately. For any non-feeler connection, we now call this thing called "has all desirable service flags," which is basically just like can they serve me blocks, and are they a witness node? So we actually enforce that for our outbound connections as if they're all witnesses.

You can take a look back at Matt's commit where he actually changed this, and Matt basically says, "it's far enough past deployment time that there are a ton of witness nodes on the network so we can kind of safely transition this over to being more stringent about who we connect with." Funnily enough, it looks like he made that change while he was refactoring, so welcome to classic Bitcoin. [Laughter]

Audience Member: Service bits are not reusable, right? Once you designate a bit as something, you can never reuse again, right?

[TODO]
James O'B: Yep, I think that's right. The node witness is like left shifted 3 and like I think we're on like 4 maybe or something like that. They're pretty low number of these service bits, and I can't remember the size of the field. 64 yeah, so we'll yeah we got a few more. Obviously, that's not a critical consensus piece of data, so that could be a peer-to-peer change if we needed to introduce more. I think this is just basically setting node witness if SegWit has been deployed

Audience Member: That's not validated, right? Can you fake that?

James O'B: You can. You'll probably get banned when your peer asks you for something.

Another interesting detail that was introduced in the validation code is we have this thing called CValidationState, which is basically this object that gets passed in. It's sort of like a piece of data that gets created along with every peer communication that eventually makes its way into the validation part of the system, and it's like how you sort of record what happened or where it went wrong, or like how severely out of alignment the communication is with what you expect.

SegWit introduced this idea of "corruption possible," which is kind of interesting because you might say, receive a block, and now in SegWit if some part of the witness data in that block is garbled, but that's the only problematic part of it, then we say "okay, this data might have just gotten screwed up somewhere along the way, and we shouldn't necessarily consider the block invalid, and we shouldn't necessarily disconnect the peer." When I was reviewing this, it kind of raised a question in my mind because why wouldn't we have always had this? Why is somehow having to witness data cordoned off, why does that introduce the possibility of corruption? I don't know. Maybe we can ask somebody.

This has now actually been removed since in a recent refactor of the DoS handling code. Instead of specifying corruption possible, which I think really just affects whether or not we disconnect or ban a peer, we now have specific reasons, like a constant for each reason, constant for each reason that we set on the state. So it's a bit more specific. But I found this pretty confusing when I encountered it because there's a lot of special-casing going on in the validation code where you're like, "well, this didn't connect properly, but I'm not gonna penalize my peer because corruption might have been possible." It's like well, what does that mean? Where does that come from?

Antoine: In case of corruption, you reject the block, right?

James O'B: Yeah. You reject block, but in the headers tree, you don't necessarily market invalid, I think, which is kind of weird.

James O'B: Yeah, another interesting tidbit during the SegWit deployment was that it didn't support compact blocks. Have you guys gone over compact blocks yet? Okay, cool.

Again, I don't really know what the conclusive answer was here. Shortly after SegWit was merged, I think Suhas merged a follow-up PR that activated compact blocks for SegWit.

James O'B: I think the reason is that it was just more engineering effort.

Antoine: There was not something SegWit native in the compact blocks...

James O'B: Yep. I guess upon deployment, if you were using compact blocks, you'd basically have no hits in your mempool because many nodes weren't producing SegWit formatted transactions, so maybe it's something like that. I'm not really sure.

In any case, this is somewhere in net_processing where we basically track whether a given peer supports our compact block version, which, as you said, is version two for Segwit. So that's an interesting detail of deployment there.

# Extensibility

Let's talk about what SegWit does in terms of extensibility. There are really two main features here that are worth talking about. The first is obviously script versioning.

There's really not much here to say in my mind. Basically, this is a conditional in the script interpreter that says, ok, if our version isn't 0 and the flag called script verify discourage upgradeable witness program isn't set, then basically just say, "yeah we passed, we're good." The idea being here that in order to support a soft fork, you need to have a basically OP_TRUE-esque thing that you can then clampdown in subsequent versions. Is anybody at all confused about that, or should we elaborate more on that?

Audience Member: The flag, when would you want to set that?

James O'B: I think that might be set all by default because we don't have version 1 transactions yet. But I don't know. I tried to grep around a little bit for that flag, but I didn't really dig too deep, but that's a good question. So yeah, when would you actually set this flag? Is this flag set by default now for transactions?

...

James O'B: If you're creating a transaction with the Core wallet, is it going to set this flag? This flag isn't a function of the transaction, it's a function of the script interpreter. Probably by default a flag is on.

James O'B: So it's always on?

Antoine: Yeah.

James O'B: I guess you can't really use higher witness versions so you get degenerate success conditions.

The second thing that's potentially more interesting is we've got this additional commitment that we've kind of hidden in the txins of that same coinbase transaction where we have the OP_RETURN that commits to the Merkle root of the witness transactions. Right now we stick a nonce in there -- that's basically just zeros. In the witness stack of the input to that transaction, it's like we've saved this bit of space, this 32-byte space, where right now we're not doing anything with it other than validating that it's there and it's filled by something. But if we want to say, for example, introduce an assume UTXO or a UTXO hash value, we could stick that in there. Or even more likely, we use a commitment Merkle structure to say that is, “okay by convention, the first upgrade is going to be the left part of this tree and then you know like fill out a whole Merkle tree full of commitments that miners generate and commit to and validators validate.” It gives us a ton of extensibility in terms of what a block actually commits to without having to modify the header and create a hard fork or something. So that's kind of cool, and I don't think anybody's really discussed using it yet, but it's there.

Felix: No discussion at all for what'd it could be for?

James O'B: Beyond some kind of UTXO set hash...oh yeah, BIP 157 filter header hash. Have you guys covered compact block filters yet?

Antoine: Compact blocks? Yes.

James O'B: Oh, sorry. There's a kind of naming collision. The neutrino stuff is called compact block filters even that's different from compact blocks. Anyway, so you guys haven't gone over SPV and bloom filters and all that yet stuff, right? Oh, you have cool. Just real quick, compact block filters are an alternate way of doing SPV where you basically generate a sort of compressed view of the transactions that a block spends or creates. The idea is that in SPV mode, you would just transmit these filters for each block.

Antoine: For BIP 157 you have to build a parallel chain of the headers of the filters to make sure that the headers are true from the beginning. So if we commit the filters in the commitment transactions of the transaction of the coinbase, light clients can rely on it and not on the parallel chain.

James O'B: Yeah, exactly. Instead of having to retrieve the entire headers filter chain for these filters then you just take one block, and you say, "okay there's this commitment here," so I know that the header filter starting with this hash...

Felix: Why not have multiple OP_RETURNS?

James O'B: Because the point is that you can compress basically all of the commitments you could ever want into a single Merkle root that would replace this nonce.

Audience Member: So this couldn't be done pre-SegWit because of the validation rules of the coinbase for legacy nodes, I'm guessing?

James O'B: It would be another soft fork, but you could do it. It would basically be like redoing SegWit. So, in any case, if we were to ever use this thing is still a soft fork. It's a little bit more well defined in terms. This is the place where we can slot in now.

Audience Member: Is it 32 bytes?

James O'B: Yep, 32 bytes so enough for SHA-256.

Alright. There is a worse line inside SegWit, in my opinion, and it's this one. It's like 354 characters. It was awful in GitHub. I was reading through the pull request and had to scroll and scroll. This is basically this is how you search for which txout is in the coinbase transaction has the witness commitment. And so all it's doing is looping through the txouts in the first transaction of a block and what's going on here is, there's basically a preamble to the commitment data, and it's just like byte by byte comparing to see if it's that preamble. I don't know why it was done this way.

James O'B: Or even just like take this block BTX0 vout, O thing and put it in one variable but whatever. Thanks Pieter. Maybe at some point, we will have like some reasonable line length. The important stuff is there.

Maybe some open questions. Do you guys think that SegWit was the right thing to do, or is there some other alternate scheme you could have come up with?

Antoine: Did anyone dig into [flexible transactions](https://bitcoinclassic.com/devel/FlexTrans-vs-SegWit.html), which was another malleability fix?

James O'B: I'm not familiar with that one. I remember what extension blocks were, but I think that was more of a scalability thing. Flexible transactions I don't know anything about. Maybe somebody else…
...
James C: What do you think of Luke Dash-jr's point where with all these soft forks, you know where there is a virtual block size increase, with IBD complexity grows quadratic. If you assume that the block size will continue to grow in that sense. Next time there's something similar, we wanted people to use it. If we give them a weight discount, we're increasing the block size again.

James O'B: The economics are that are not very clear to me. Because I think if you're a miner obviously you're trying to fee maximize. Do larger blocks neccessarily that? Do that they decrease fees, but maybe on net because you're getting more transactions you're getting more in fees. that's not really clear to me

James c: What about IBD complexity?

James O'B: When you say IBD complexity, you just mean the amount of time it takes?

James C: Because if the blocksize increases linearly and the IBD is the integral of it, the integral of it will be quadratic.

Elichai: That's why Luke wants to decrease the block size.

James C: Well, at least not have half step increases like SegWit.

Elichai: He argues he has some calculations as he said that right now, the maximum is like half a MB, and he wants to decrease to that.

James O'B: I haven't thought enough about that stuff. I mean, the proposal I'm working on for assume UTXO is a way of truncating at least you know the initial cost of an IBD. I think long term, it has to be something like that because you just can't have this linear process that's supposed to continue forever. We've got to come up with some way of dealing with that.

Audience Member: Oh, flexible transactions were controversial.

Antoine: Yeah, because it was a hard fork.

Audience Member: Yeah, it looks like Matt was very against it.

James O'B: Oh yeah, maybe we can get him...

Elichai: What about some sort of cut-through? Like we can remove transactions after spend.

Antoin: ...because you can build a chain of transactions...

Elichai: Yeah, I'm saying it won't work with the way it works right now to make some change, but in theory, if I sent you money and you sent it...

Antoine: ...but my question is cut-through is maybe Lightning will change the economics of other things….

James O'B: Okay, very interesting but probably outside the bounds of SegWit. Does anybody think it should have been a hard fork versus a soft fork instead of doing all this like shuffling around?

Audience Member: Some people say it's a lot of hacking. It seems like a lot of hacks. To sort of pigeonhole this in the comes at a cost. I have in mind just maintaining all these hacks and somebody has a knowledge of all how these weird things work together, but it's a tradeoff.

Audience Member: Personally, I think with Bitcoin, it's like for developers are more of you, I don't want to say it, we're like janitors. It's like we're literally like we just got to maintain. I think maintainability is the absolute highest priority. Even if the code was ugly, you gotta live with it. You have to prioritize what's more important.

Felix: Which is unusual if you come from a traditional software background. Most of us have a traditional software background where if the code is ugly, you want to clean it up...

Fabian: You have control over the client. Here people are running clients you don’t have control over. We can't deploy an app for the iPhone.

Audience Member: I think it's interesting too. Since you've got a lot of cases where originally propose a hard fork, and then it simmers for a while, and then you end up with something that's better that's soft forkable. But not only that thing you showed with the Merkle commitment being left open with the nonce. It's not talked about, but it's sort of laying the groundwork. So not only if you get a soft fork, but you laid the groundwork where we do not have as much complexity in the next iteration. I think that makes it where software is like waffles. You always throw the first one out. This is kind of an example of that.

Cross talk...

Audience Member: I think that's a misnomer. It's not really about just a segregated witness. There are about another zillion other things like upgradability and...

Audience Member: I think without your tests and all, we are talking about 600 lines of code or something.

James O'B: In general, I think that's a really good point. Is it preferable to have a very well contained consensus change deployed by itself in isolation, or is it preferable to bundle a bunch of stuff together so you can kind of consolidate testing effort and really make sure that it goes out the right way and all the changes interact in a way that works. How do you make that distinction?

Audience Member: Is there a reason they have to be bundled together. I guess some have to be deployed together but I’m sure they all had to be bundled.

James O'B: One social argument is that it's very expensive for a wide number of people to scrutinize a change like this, and if you were to have to say, seven changes, the aggregate overhead of doing that is big. People may just get fatigued and accustomed to just saying, "Okay, we're gonna take the next change," instead of it being a big, momentous thing.

Jonas: A counterpoint to that is that you're then teaching the users of the software to be more accustomed to smaller changes, and so that's a cultural thing. You know to say that is this something that needs to be scrutinized in such detail or is there an upgrade path where you start getting used to sort of doing these upgrades, and when you run into something that's contentious, it sort of takes the edge off a little bit because you're used to actually change. Then there's the larger conversation about whether isn't the software good enough/ossification and politics. That builds its way in if you create these waterfall releases of these are really big deals, and everybody has to be on edge for a year at a time. As opposed to, we're doing incremental changes, and you know those increments are important, but you know they're not having secret meetings and behind closed doors to decide it anymore.

Amiti: I also think that incremental changes make accessibility or trying to understand them easier. But SegWit it's like they're just so many different things that it's really easy to be like, "oh, it's complicated. There's a lot of politics. I don't get it." If it's an incremental change, it appeals to a wider range of people, who can be like, "oh, I can go understand what's going on there if I want to."

Felix: I don't feel like you could have broken out much out of SegWit. It felt like an MVP.

James O'B: Certainly a script, I guess you didn't have to virtualize the script stuff as much. It was a good opportunity to do so. Like the version like this the segment script version numbers.

Audience Member: It like lays the groundwork for future versions.

...

Audience Member: It just seems like empirically, the more likely scenario is not to do it incrementally. There are some arguments why you would want to do it in one lump sum. One, it does focus attention at distinct times. There's a lot of time between changes, so people have time to review and come up with that next better version, a next better version. You don't really want your users to be used to upgrading like in other communities. That's maybe not such a good thing. Because it doesn't have to be a super complex improvement to introduce a completely failing bug.

James O'B: Yeah, absolutely true.

Audience Member: We can distinguish between the release process and the pull request process.

James O'B: Indeed, there is a big distinction in SegWit, right?

Audience Member: I think that it's suicidal to try to send a Bible into a pull request and it sits there for six months you have to rebase a hundred times, and nobody's still gone through it all. Compared to trying to upgrade the user side.

Audience Member: Yeah, I was thinking more consensus changes type stuff.

Audience Member: I'm looking at your experimental UTXO snapshots. I'm thinking of Jonas Schnelli's work where he has this global proof of concept, but then there's a lot of slices, which makes it easier to review.

James O'B: For your own sanity too.

Jonas: But that depends on the project. Only if there's somewhere you can slice off while delivering incremental value. There are other projects that need to be delivered in a whole chunk. I think looking at SegWit, how do you slice this off?

James O'B: I mean, you see some of these conditionals that are like if SegWit has activated yet, do this. Conceptually maybe you could get those into the code base one by one. I sort of agree. I don't know how much value that would add.

Felix: You have to touch on a peer to peer layer so you can transmit the witness transactions, and you have to have the commitment. I really don't see how you could have sliced it.

Audience Member: You know the peer-to-peer stuff is interesting because, in Suhas's talk, he mentioned that it was accidental that we got it right. This could have accidentally partitioned the network. If you're not sending different stuff to old nodes and new nodes, we just kind of did that by accident. I think that's a reason why it was an accident [we got it right] because it's so complex. It's hard for people to reason about upgrades. Can we foresee everything? We were lucky that we didn't end up partitioning.

James O'B: Next question. Given how this process went, what do you guys think is gonna be involved in Schnorr/taproot? What do you think the code changes are going to look like? What are the entry points that are gonna be in common with SegWit? What will activation look like?

Audience Member: 2023.

James O'B: In terms of the code, how will we have Schnorr signatures?

Audience Member: It's also a bundle of changes.

Cross talk...

Felix: But there's no new commitment, there's no new peer-to-peer stuff. It's pretty much just validation, just a few new lines about validation, no?.

Audience Member: It's pretty small.

Audience Member: Aggregated signatures isn't right away, right?

James O'B: Depends on what kind of aggregation. Cross input, no, but within a single input, yes.

Cross talk...

Felix: How many files does taproot touch?

Elichai: I want to comment on that. Sipa's argument about the number of lines isn't fair. Because it does everything in line. Like he'll do a bunch of math in the middle of validation.cpp. That's now how it will be. That looks even better than if you look at his code to implement Schnorr in Bitcoin. He's saying it's 20 lines. But it's 20 lines if you do the math inline in validation.cpp. The second you start doing it right, it becomes 200 lines of code.

James O'B: It sounds like you showed up to the residency just in time for the next code review. So buckle up buttercup. [Laughter]

Basically, I think for schnorr/taproot we're gonna bump the transaction version, and that'll be that as far as the consensus layer goes. In terms of a deployment mechanism, do you guys think we'll use BIP 9? Do you think we'll do something else? Will Shaolinfrye part 2 will show up?

Felix: More hats!

James O'B: How many hats will we need to get this activated?

Audience Member: It's like BIP 9 with the absolute is happening whether you like it or not. It kind of makes the miners go back to realizing that the signaling is not a vote for whether you want it or not. It's a signal of "are you ready to receive it" and knowing that at some point you got no choice. Because I agree that the vote should have been during development and the BIP process, not during deployment after all the code has been written and reviewed. It doesn't make any sense.

Audience Member: That comes with the risk of a chai split, right?

Audience Member: The miners don't want a chain split either.

Audience Member: You're kind of assuming that the miners are always proactive and pay attention to what we have to do, and I think the case now, but in the future, it could be just like a passive mining farm that you don't really touch. Then you do this BIP8 upgrade, it can cause a fork because nobody is really upgrading their farm, right? You're forcing everybody to upgrade on that day, but that's sort of assumed that people are paying attention.

Audience Member: No. Normally the windows are like a year. I mean if you're running the mining farm and you can't flip a flag?

Audience Member: Right now, that's the case. I'm saying like ten years from now, twenty years from now.

James O'B: Maybe as the system gets bigger.

Audience Member: Right, you might have a solar farm or maybe in the middle of Atlantic.

Audience Member: But the question was like, what's the most likely? I would say that most likely would be BIP 9. Why not? Because that's the only one that's ever been used, that's actually ever been. It may not be the one that is responsible for SegWit, but it was the one that was actually in the codebase.

James O'B: Carla, do you think this change will be more contentious to deploy in SegWit or less?

Carla: I wasn't really around for this, well really around for the SegWit change. If this doesn't affect miners, with the maybe ASIC Boost thing, maybe it'll be a bit less dramatic. And generally, the sentiment seems to be a lot more positive for Schnorr/taproot, but I guess you never know.

Antoine: Yeah, there isn't a big incentive against Schnorr/taproot because it's a big gain of efficiency and privacy.

Elichai: Yeah, that was the same with the incentives in SegWit. It's very premature to say something like that... We didn't know about all that before with SegWit... Maybe there is something else like we didn't think of that before. How can you think of this beforehand?

Audience Member: the problem with BIP9 is that you're not especially with the competing SHA-256 chains, but you can easily get BCH / BSV chained miners that will come into Bitcoin and try to hold it hostage with only 5% of the hashpower.

James O'B: So maybe that 95% activation threshold is pretty high.

Audience Member: It still seems like the conservative approach is generally how things go and then if there's a problem. Because the core thing to prevent is a network split right? It's going to be an overriding reason. You can speculate, but if it goes through with 95% then that's your first choice.

Audience Member: Is it thought that if the SegWit proposal would have been a hard fork proposal, then it would have gone through via BIP 9?

James O'B: Probably. Because the commitment structure would have probably been outside of the Merkle tree.

Audience Member: So the thought is that it would have gone through even though it was a hard fork because the miners would have discounted users who care more about backwards-compatibility.

James O'B: You're saying miners care more about backward compatibility?

Audience Member: No, I'm saying the opposite. Since miners cared less about that backward compatibility, it would have gone through.

James O'B: I think that's plausible. You never know for sure. That is definitely true if you're assuming that ASIC BOOST was one of the primary hold-ups. So it's interesting to think about, but I think it's important to maintain a sort of cultural precedence of not, you know, doing an upgrade hard fork.

Elichai: Is anyone bridging the gap between the developers and the miners? Like we're all here speculating what miners want.

James O'B: You should get Matt to talk. That's a lot about what he tried to do. He's still in close contact with a few miners.

Elichai: I think that's the best way rather than speculate what they want or what they care about, but act[ually sit and talk.

Audience Member: Was that the New York meeting?

Elichai: The New York meeting wasn't between the miners. It was between corporations.

James O'B: One of the first Scaling Bitcoins was held in Hong Kong. The famous Hong Kong roundtable where Matt and a few other people actually went to Hong Kong and talked to the Chinese miners. So I think that kind of thing has been tried. I'm not privy to a lot of it, but you might ask Matt about how that all went down.

So there are some links here. There are two SegWit PR's, which is kind of interesting. One is an [un-rebased version](https://github.com/bitcoin/bitcoin/pull/7910) where Pieter would just kind of append commits to it, so it's got a gazillion commits, and it's kind of hard to follow but a lot of the commentaries there. Then there's a [rebased version](http://github.com/bitcoin/bitcoin/pull/8149), which is where he cleaned up to get history and so I'd highly recommend at least at some point, maybe not now even the next few weeks, but at some point, just read through those commits because it'll give you a really precise idea of what he had to do.

Accompanying that is a write-up that Peter Todd did, which is basically his code review of that pull request, which I think is really well done. He raises some good points.

The BIPs obviously, they're kind of a shorthand for getting exact details on what these changes are. Anecdotally, if you want to not only understand the SegWit message changes, but more generally the Bitcoin protocol message changes, one high-level way to do this is to look in the test framework where we define all of the message structs. That's just kind of a good shorthand for what the serialization formats look like, so those are all worth checking out.

---
title: Bitcoin Transaction Pinning, ANYPREVOUT & eltoo
transcript_by: Stephan Livera
speakers:
  - Greg Sanders
date: 2023-03-06
media: https://stephanlivera.com/download-episode/6040/463.mp3
---
podcast: https://stephanlivera.com/episode/463/

Stephan Livera – 00:02:02:  So on to the discussion with Greg. Greg, also known as instagibbs. Welcome to the show.

Greg Sanders :

Hi, glad to be here.

Stephan Livera :

So, Greg, I know you’re doing a lot of work on some interesting Lightning stuff and transaction fee pinning things. I know you’ve been around for a while in terms of Bitcoin development and Lightning stuff, so yeah, interested to chat and hear a little bit more from your perspective, and want to learn a little bit about what you’re up to. So do you want to just give us a bit of a high level? What are you up to these days? What’s your main focus area?

Greg Sanders :

Yeah. So starting last April 2022, I rejoined Blockstream, this time under Rusty, the core Lightning team leader. And I’ve been working on, specifically was hired to work on Eltoo, the kind of symmetric channel construction using ANYPREVOUT or NOINPUT soft forks. I’m ultimately aimed at getting it deployed on the Liquid network, but as a key part of it, I’m building it for Bitcoin first and then adapting whatever needs to be adapted for it since the systems are so similar. That’s kind of like the high-level direction there.

Stephan Livera :

Awesome. Yeah. And I’m a fan of the ANYPREVOUT idea, and I would personally love to see Eltoo. So listeners, check out my earlier episode with Christian Decker, where we’ve spoken a bit about some of this, and I’m sure, Greg, you’ve probably pushed it forward as well yourself. And I know AJ Towns has also done some work on this stuff as well. And one other thing I was also curious to chat about, I know you have some knowledge or expertise in this area around transaction fee pinning as well because it’s sort of related in a way. So I think it’d be great if maybe you could just give us a bit of an overview of this idea. Transaction fee pinning. Like, what is it?

Greg Sanders :

Right, so this is related to the Eltoo work, actually, because as I started working on it, I wrote the BOLTs, the standards for the Eltoo channels. And as I was writing these, I became more and more convinced that this issue called transaction pinning was going to be a real problem. Transaction pinning is where a kind of a griefer or counterparty that can accidentally do this as well, but they make a transaction that is unlikely to get confirmed anytime soon. And actually, in effect, it’s kind of not paying miners fees. Right. And then you say, okay, well, why don’t we RBF or double spend it with a higher fee? But due to a mixture of kind of design constraints of the current system, it makes it difficult or very expensive to do so. We can dive deeper into details on that, but that’s high-level. Kind of minors aren’t getting paid when they should be.

Stephan Livera :

I think it’d be good to chat a little bit about that. And if we could maybe put that into a context, like, let’s say you and I had a Lightning channel together, and let’s say so I guess for listeners who are more newer to this, the idea is we have pre-signed transactions that are not broadcast yet. And so I guess the idea is if one of us goes offline, if the other has to now force close the channel, we would need to broadcast that transaction, right? But I guess part of it is like we’re getting into this idea of if let’s say I’m malicious and I see you’ve gone offline, I try to broadcast an old state that has less coins for you and more coins for me. And so I guess could you just talk us through what that would look like if, let’s say I’m malicious, I’m trying to stop you from putting in your justice transaction or your penalty transaction.

Greg Sanders :

Yeah. So I think for pinning the specific case that most people talk about are delaying out the HTLC resolution. So a hash time lock contract, which means this contract is supposed to be resolved within N blocks. You could say like a day’s worth of blocks. But what happens is the timer starts. So the commitment transaction, this Lightning transaction hits the chain, this timer starts. And then what the counterparty can do is make a transaction that’s kind of very large and low fee rate. So if there’s a fee rate spike, if there’s a big backlog like we’ve seen recently, and the going rate is high, much higher than one satoshi per virtual byte, maybe the counterparty can get that one satoshi per virtual byte transaction in the mempool, but not actually try to get it confirmed. And then this times out the contract, and then what they can do is they can take the timeout clause of this contract and grab the money back. So, for example, you already forwarded this HTLC to another Lightning peer. They’ve claimed it, but then the person that offered you the contract on the inbound direction, they claw it back. Essentially you’ve been stolen from. And so pinning is one method of kind of stealing from you in smart contracts or at least making your life difficult. There are other considerations. So a less smart-contracty thing is where, let’s say you’re a Bitcoin payment processor or you’re a custodian, right? And you do batched payouts. So you’re paying out to like hundreds of people at a time, let’s say. One issue is that if you make a payout at low fee rate, someone can sweep one of their coins. One of the outputs could get swept by a recipient at a low fee rate. Maybe even they do consolidation, right? So it’s a large transaction, low fee rate. And then suddenly you can’t RBF this transaction, or even child-pays-for-parents, so the tools for being able to increase, to bump your transaction fee, are reduced in these cases.

Stephan Livera :

I see. So let me just walk that through to make sure I’ve understood. So let’s say a big exchange is doing a payout for 50 customers and they’re all getting there, in one transaction they’re all getting say there’s 50 outputs. But one of those customers, if he does a child-pays-for-parent but with a very low fee, you’re saying that depending on the conditions at the time, that exchange is now no longer able to add more people to that unconfirmed transaction. Or can you just walk me through that?

Greg Sanders :

So basically, let’s say they did a very large child-pays-for-parent. Like they’re consolidating for some reason. Don’t ask me why, this has happened in real life. Then what you do is let’s say you have a replace-by-fee scheme for your payouts. Now you have to pay for both your replacement as well as the child replacement. So if the child spent 0.1 bitcoin on a very large low-fee-rate transaction, now you have to pay that extra 0.1 bitcoin to replace that because you’re knocking it out of the mempool. You’re essentially taking money out of miners’ mouths if you don’t replace that fee. Right? In a sense. And also you could say, well, why don’t you just child-pays-for-parent your own transaction? Like, let’s say the payment processor or custodian has a change output. Well, you could spend that output at a higher fee rate to bump it, right? This is called child-pays-for-parent. But there’s also called package limit pinning, which is another flavor of this, which is due to the complexity of the mempool architecture, there’s a limited amount of both number of child transactions in a mempool graph when you’re tracing like parents and children. There’s both count, so how many descendants in the mempool, and also how large they are total. So for example, one large sweep could just lock you out of the size constraints to say you’re not even allowed to spend your own change output in the mempool.

Stephan Livera :

So, as I understand, I mean these are things that just already exist today. So these are already limitations. So exchanges and payment processors and users today are just dealing with this today, right?

Greg Sanders :

Yes. So I previously was the tech lead for the Liquid network a few years ago and this is a major issue because you don’t have a robust interface for doing replacement by fee or fee bumping. And so you’re doing all these heuristics and guessing and saying well, if we get stuck it’s too bad, I guess, and hope it resolves itself by luck, pretty much. I’ve also talked to other people who have worked on custody solutions and this is a pretty common problem.

Stephan Livera :

Right. And so I guess it’s more of a problem if you are a large custodian or payment processor and you’re dealing with these large transactions. It’s not typically just like an individual user who’s falling into these situations, normally, right?

Greg Sanders :

Yeah. Well, it’s more normal where you have a motivated adversary, like in the Lightning channel. So that would be more typical from an end user perspective, is you’re entering to a smart peer to peer smart contract, and you need to resolve a transaction fast. You need to get something confirmed in a jiffy, and there’s people who have financial incentive to stop you from doing it.

Stephan Livera :

I see. Yeah. So then I guess part of this is also coming into that conversation a little bit around mempool full RBF and things like this, because as I read some of the discussion and you clarify for me if I’m getting this wrong, but as I understood at one point, or initially, it was understood that, oh, okay. Having mempool full RBF would help us sort of move into a situation where maybe some of these pinning attacks are less possible, but then later we sort of discovered that maybe it doesn’t help us. Could you help us untangle what’s happening there?

Greg Sanders :

Yeah. So you can think of not having mempool full RBF, if you don’t have that, that opens up a new pinning vector, which is basically in a coinjoin-like situation with a peer, they can double spend their own input during, like, contract creation time and then mark this double spend as not replaceable, so they get it first and then you can’t replace it no matter how much fees you put on there. So that’s kind of the idea, is that even if you put a lot of fee, you won’t be able to replace it efficiently. So, yes, the alternative is, well, even if we have full RBF, a motivated person can make it financially difficult to replace it. Right. And they can kind of do this. So I think in the coinjoin scenario, it’s for every input the attacker controls, they can increase the economic damage, so to speak, by that number of inputs. Right. So it’s multiplicative. So while it doesn’t fix pinning per se, it does remove one pinning vector. So you can’t replace to well, in the worst case, you can replace, but it’ll be very expensive to do so.

Stephan Livera :

I see. So it’s fair to say then that mempool full RBF, or just being in a full RBF world would help against some pinning vectors, but not all of them, is that correct? Fair to say?

Greg Sanders :

Yeah, exactly.

Stephan Livera :

Okay, so it’s possible to have pinning outside of the context of this, even in a full RBF world?

Greg Sanders :

Yes.

Stephan Livera :

Okay.

Greg Sanders :

Yeah. So one mental exercise you can do is you can say, okay, look at the RBF rules. That’s BIP 125. You just read, you read that BIP, look at all the rules that are there and say, how can this pin a transaction? Because pretty much all of these are constraints on when you can replace something, right. It has to be signaling to replace. You have to replace the total fee. One example is you can’t replace it with something that has a new unconfirmed input, which is kind of like esoteric. But there’s always like constraints as a wallet designer, you have to think about and take care not to violate to properly RBF transaction.

Stephan Livera :

Right. And I think there are different arguments back and forth here because as I understand, some of the, let’s say, people who were anti the full RBF, they were trying to say, well, let us manage our risk. And then the people on the other side are saying, no, actually, full RBF is more incentive compatible for the long term. And this idea of first seen should never have been like a promise that should be sustained forever. I’m curious, how are you seeing that debate? Even though maybe it’s a month or two, maybe three or four months old, but I’m curious how you’re seeing that.

Greg Sanders :

Yeah, so my take was I did a lot of discussion with different developers and there’s different opinions, smart opinions on both sides, to be honest. But I do fall on the side of you at least should offer the option of full RBF and pull up full RBF because the economic arguments are pretty solid. And to not have that feature is kind of paternalism, and it just encourages people to run alternative implementations, which maybe it’s what you want, but I don’t think that’s kind of the desire. Right, so there’s prior to the release of, I think, Bitcoin Core 24.0, I think that was when the debate was happening about removing an option or not. I was vehemently against removing an option, even if I don’t think it’s the most burning question at the time.

Stephan Livera :

Right, I see. And as I understand one of the, let’s say, anti full RBF arguments at that point from people, like Sergey over at Bitrefill, would be something like, “But remember, not every user is running a node and there’s lots of users who are just using a wallet and they are not getting a choice per se in the running of a node.” But I guess at some point the answer would just be that, well, ultimately if you want to have a say, you have to run a node. Is that your answer or how would you answer that?

Greg Sanders :

So with this kind of policy, you need something like 10% of the network with the option flipped on to really make a difference. And you need some percent of miners, right. Maybe 1%, maybe higher. So there is this kind of thing where your actions alone aren’t too important, but if there’s a large minority of users that decide it’s important and turn it on, then it may actually be in effect. So I think there’s a bit of irony here in that I think some of the backlash was like, hey, you’re trying to take an option for me? I’m definitely going to run it now. And that’s kind of the Streisand effect. Right. You’re drawing a lot of attention to it and then that causes people to have a backlash. Now, I don’t know what the number is today, I just think the future is going to be something like Lightning payments. I mean, I haven’t done on-chain for a few months now after I set up some channels. So I think that is the future and everyone agrees it’s the future. And that’s partly why I’m working on Lightning, to make sure it is the future.

Stephan Livera :

Yeah. And as I understand, there are different arguments there, I think it seems to me, as I understand it, it seems to me like we’re eventually going to be in a full RBF world, whether it’s by Bitcoin Core or just the network acting that way. It seems to me like that’s the world we’re going into. And so hopefully more and more people are able to use Lightning and ideally in the self-sovereign way, which I think also gets into the ANYPREVOUT conversation as well. But I’m curious, if you see it like that, do you believe that eventually, even if Bitcoin core does not, let’s say, have it on as default, that eventually we would end up in some kind of similar scenario or at least you see that as likely?

Greg Sanders :

Yeah, I think that’s likely, especially when you consider a lot of the popular node software now, it comes prepackaged with its own configuration, right? And you just need one kind of popular, for example like Umbrel or something, those popular distributions where they would flip on that switch themselves. So it’s not even really up to Core per se, it’s up to basically what people are running. The node runners themselves are in charge. So it’s kind of an open question and I think long term, I just think it makes sense.

Stephan Livera :

Yeah. And actually on that point, I think it was interesting seeing some of the arguments there back and forth because some of the arguments were, look, yes, there’s a lot of people who are signaling RBF manually in the current regime, but not a lot of people use the RBF. That was one of the arguments, right? It was saying and I guess the argument could also come back, well, maybe a lot of them don’t know how to, maybe they don’t have a wallet that is enabled for RBF. There’s all kinds of different back and forth there. But it seems to me like the longer term is using Lightning, of course, and of course many of the people on both sides of that debate are pro Lightning. But I just thought it was an interesting one to understand. And so I guess bringing it back to the pinning aspect of it, do you see, as we were saying, even in a full RBF world, that takes away, I guess, some of the pinning vectors or one of the pinning vectors, that’s right. And then what are the other pinning vectors that remain? And should we be worried about those?

Greg Sanders :

Yeah. So I think I briefly mentioned them, but I call them kind of like there’s more than this, but I would call the major two are packet be called rule 3 pinning. This is BIP 125 rule 3, which says you must replace all the total Bitcoin fee, right, the total fee of everything you’re going to knock out of the mempool with your replacement.

Stephan Livera :

I see.

Greg Sanders :

So if the descendant is huge and low fee rate, it doesn’t really matter because you’re paying the total fee. So if your transaction size was going to be 1000 bytes, 1 KB, they could put in a child transaction that’s 100,000. So essentially they’re kind of inflating the size of your transaction by almost 100 times. Right. You can think of it that way. They’re making this whole package 100 times larger and then reducing the fee rate down to something that won’t get confirmed.

Stephan Livera :

I see. So that would allow them to indefinitely pin something to the bottom of the mempool per se, and stop it from getting confirmed through. And in a Lightning context, that means somebody could lose money, right?

Greg Sanders :

Exactly. It’s more interesting in things where there’s timeouts involved. Right. The time value one is if someone pins you and it just inconvenience you. That’s annoying. But no one’s losing their job over it. Like at the custodian level. Right. But at the Lightning level, it’s a money loss situation. So it’s more important then. The second largest kind of pinning vector is package limit pinning, which I mentioned, which is basically in the mempool by default, a transaction can have up to 24 descendants, so 25, including itself. Also, in a mempool package, it can only be up to 101 kilo virtual bytes. So with a SegWit transaction, that’s up to almost 400 KB. Right. As we saw with the ordinal stuff. So a child could just be like too large. So if you’re trying to spend your change output to bump the fee, that stops it from happening. So that’s kind of the other direction there. If you want a child-pays-for-parent, the package limit pinning stops it. If you want to replace by fee, by double spending it, then the BIP 125 rule 3 makes it economically expensive, maybe uneconomical to do it.

Stephan Livera :

I see. And so is any of this impacted then? I know Gloria is working on this idea, and maybe others, maybe yourself, on this idea of mempool package relay. So is there an interaction there? Like, is that stopping any of this stuff?

Greg Sanders :

There’s a light interaction. So today with Lightning contracts, what’s called commitment transaction, which is the thing you’re signing and replacing constantly, this has to have a pre-agreed fee rate, which you expect it to get into the mempool at all. Right. Because let’s say you do one satoshi per virtual byte for this commitment transaction, then the min rate goes to two. Right. We saw this just last month. So in this situation, you would not be able to get the commitment transaction in the mempool at all. Right, that’s a problem. So package really is this notion that, well, if we could tell nodes about the parent and the child, just as a simple example. So the commitment transaction and then a spend of what’s called an anchor output to bump the fee rate, if you could tell a node about both of those at the same time, they could evaluate it together and say, okay, I think this could make it to the mempool, because I think a miner would want this as a package. And so with package, if you just do basic package relay, then what we can do is for the commitment transactions, we can drop those to zero fee. We say, you know what? Ahead of time, we don’t know what the fee rate is going to be for the mempool. So let’s not even try to guess. So what you do is you have the parent transaction be zero fee and then you have the child pay for the entire package out of its own pocket, so to speak. Does that make sense?

Stephan Livera :

Yeah, I think I’m getting you. So it’s kind of like mempool package relay helps miners and the network, see, oh, there’s actually a little bit more fee associated for this, so I’m going to take this one. Whereas previously it might not have had enough fee for me to be interested. Is that kind of how?

Greg Sanders :

Correct. Yes, that’s right. Exactly, because right now you have to individually send transactions and evaluate the fee rate individually. Right. So that’s the problem here. So with package relay, we can simplify these, simplify the Lightning Network a bit, but you still have these pinning scenarios. So I can jump into that now. So you still have the rule 3 pinning, the kind of economic pinning of the total transaction fee issue, and you still have the package limit pinning. But this is where Gloria and others have been working on the version 3 proposal, if you want to jump into that.

Stephan Livera:

Yeah, sure, let’s talk about that.

Greg Sanders :

Okay, so it’s very difficult. I mentioned all these big numbers, 101 kilo virtual bytes. I mentioned 25 descendants. And this descendant graph is, like, hard to reason about because every transaction can have multiple parents, multiple children. And so these algorithms that are there to help the miner get the most fees and the algorithms to make the mempool, like, down to size when it gets too big, these are kind of different algorithms, and they’re hard to reason about. They’re kind of in conflict with each other in some ways and they’re hard to reason about. So the version 3 idea is what if a transaction can opt into a new kind of regime where it’s simple, right, simple to reason about. So the VP proposal is what if you pick transaction version 3 and that means there can only be one parent and one child transaction so a package size or a package count of two transactions, and they have a strict relationship. And from there, it becomes much easier to reason about. For example, package limit pinning and all these other things. In addition, the child is restricted to one kilo virtual byte.

Stephan Livera :

I see. So that would stop the rule 3 pinning.

Greg Sanders :

Yes. So that’s for the rule 3 pinning. And so I call this like an RBF carveout, because in the cases where you want to RBF or can RBF, then it becomes much more doable. So let’s go back to the Lightning case. Let’s say we’ve adapted these commitment transactions to use this. Then the commitment transaction can be any size like it is today. And you’re pre agreeing with your counterparty. You’re saying this is a new channel state. This is a new channel state. But then when it comes time to go on chain, that hits the chain at zero fee. Right? This commitment transaction, zero fee. And then the child, one of the anchors, there’s two anchors, one for each person. One of these anchors will get spent, and it’ll be small. Therefore, you’re basically ensuring that the rule 3 pinning is up to 1 KB. Right.

Stephan Livera :

I see. So we can think of it like it kind of contains the rules or contains it into certain known pathways, and then that makes it easier for us to do Lightning and to do maybe other protocols as well. Maybe not just Lightning, right?

Greg Sanders :

Yeah, exactly. And so, actually, I think the proposal would be that each version of the commitment transaction, since I have a copy, like, let’s say we have a channel, I have a copy, you have a copy. These are separate pre-signed copies. We each have only one anchor on each transaction. We have our own anchor on our own, right. The one we will broadcast. We have an anchor for ourselves. And so then we can package relay RBF each other. So I spend from mine, and I put both of those in the mempool. Then you can respond with a newer version. Right. You can package RBF. And you don’t even have to look at the mempool for this. You’re picking a fee schedule. I think this is a good fee, and I need to go to chain and you can blindly double spend this. And that’s the important part, is that these wallets don’t even have to see the mempool. They’re just submitting packages and outbidding the other person. That’s the important part.

Stephan Livera :

Yeah, interesting. Okay. And this is kind of all leading towards this idea of what are we going to do with Lightning? Because some of this stuff, as you’re saying, it’s already a risk. Like it could already happen. It’s just that some of these ideas are being designed to stop this in the future. So I guess it’s kind of like trying to preemptively stop this stuff happening in the future, where we’re in this scenario where people, not safe in Lightning because they can’t get their penalty transactions or their justice transactions confirmed because of these fee pinning or sorry, transaction pinning vectors.

Greg Sanders :

Yeah. And we’ve also had a long period of fairly empty mempools, and this issue doesn’t show up unless the mempool is consistently backlogged or maybe suddenly gets a big backlog of high fee rates. Right.

Stephan Livera :

Yeah. And so for a lot of people, they’ve just kind of become accustomed to it, or in some cases they’ve shifted to altcoin chains. And maybe we’ve seen this historically with Omni-Tether came off Bitcoin, and then a lot of the stable coins went to shitcoins. Right. They’re on Ethereum Tether and TRON Tether. And so people just, you know, and exchanges did batching, and most people are using SegWit nowadays. So it’s taken a lot of what was previously the fee pressure or the block space pressure, right, off the chain. But it could come back. Like if we saw a big uptick in users, then all of a sudden we’d be back in that same environment. Right.

Greg Sanders :

Yeah. Or lots of people started inscribing ordinals right. You need to be able to react to this because a counterparty could just be sitting there waiting and say, AHA, now the mempool’s backlogged, and then do this attack. So it does actually matter. It’s like a future security argument, even if the mempool is mostly empty in general.

Stephan Livera :

Yeah, right. Because they could be opportunistic about it right now.

Greg Sanders :

Yeah. So let me spin the thread a little bit more. So we have the version 3 proposal, which is being worked on, and package relay, which is being worked on. So V3, I called it kind of an RBF carveout, so it still doesn’t quite solve the situation where you have the package limit pinning, at least in general, the package limit pinning issue is still there. Right. If you want a child-pays-for-parent by spending your own, let’s say, change output, a counterparty that has a spendable output in the same transaction can basically max that out and disallow you from spending doing a child-pays-for-parent. And so this is where I’ve been working on a proposal that kind of extends V3, which is called Ephemeral Anchors, which is this idea that you can attach an output that doesn’t require any signatures or anything. So in this case, it could be an OP_TRUE output. It’s basically a bare OP_TRUE output that is zero value or can be zero value. That is essentially a hook. Like it’s like a lock on the transaction where to get this transaction in the mempool, you have to spend that output. So it’s essentially like you can think of it like a lock on this transaction where yeah, so if it has other outputs, let’s say you have two outputs and this anchor, then a counterparty can only spend the other outputs if they also spend this special output. Does that make sense? Basically, because you have to spend it, it will be spent. And there’s only one child. If you remember this, that in this V3 regime, there’s only one child. So they must be spent together. And so then that makes it kind of like a lock on the parent transaction says, well, you have to spend this, so anyone can double spend these child payments, essentially, these child spends. And so this kind of unlocks the package limit pinning scenario where in the commitment transaction, in the original commitment transaction, it has two anchors, you can’t get pinned because the outputs have to be spent together, essentially, along with this ephemeral anchor.

Stephan Livera :

Interesting.

Greg Sanders :

It’s a little hard to I guess.

Stephan Livera :

It’s hard to conceptualize. I think I’m sort of following you.

Greg Sanders :

I’ll give you a specific example right now. So if we want to do like, splicing, right, or make a channel, all of the smart contract scripts have this thing that is a one-block relative time lock, a one-block Check Sequence Verify. All of these outputs have them except for the anchors. And this is because we’re trying to stop package limit pinning. Ironically, this sometimes can be incompatible with Miniscript, and it also means you can’t do smart things like, oh, I want to splice into a new a new channel funding output, but also not pin the other person, right?

Stephan Livera :

Back to the show in a moment. When it comes to securing your Bitcoin for the long term, you know I’m a big fan of multi-signature, and Unchained Capital can help you out here. They have multi-signature that is secure, transparent, easy to use, and sovereign. With their multi-signature, you generally hold two keys in different locations, of course, and they hold the third key. So they can help you in the case of recovery. They can also help you out in the case of inheritance. So Concierge Onboarding is a program they offer. You can pay upfront, they can ship you some hardware, they’ll do a call with you and teach you how to set this up, even if you’ve never held your own Bitcoin private keys before. They also have some inheritance, step by step checklists, letters for the executor or trustee, and a range of other support and education. You can find all of this over at unchained.com/concierge. Use code LIVERA for a discount. And when it comes to hardware to secure, your bitcoin, Coinkite.com, offers a fantastic range of products here. Most notably, it’s the COLDCARD Mk4, the latest edition. It has two secure elements. It has NFC support, but you can of course disable that and just use microSD or USB if you wish. And it has more RAM and CPU for faster signing of transactions. It’s also a very reliable performer. I found it really reliable and I really like that you could set up this device without even plugging it into a computer. You can just plug it to the wall or you can even battery power it and use it in that way. And then you can set it up easily with wallets such as Specter Desktop, Sparrow, or Electrum. And Coinkite also offers a range of other products, notably the BLOCKCLOCK, SEEDPLATE or the TAPSIGNER, a range of other products you can check out there. Go to coinkite.com, use code LIVERA for a discount on your COLDCARDs. And finally, for those of you looking forward to a Bitcoin event, this is going to be the biggest Bitcoin event in Europe. It’s BTC Prague. It’s happening in Prague, Czech Republic, June 8th to 10th. This is going to be a fantastic event. I’m excited to go. I will be one of the MCs for the event. Michael Saylor will be there. There will be an awesome range of speakers. There’ll be so many Bitcoiners. So if anyone is in Europe or near Europe, definitely check your calendar, check your diary, mark this out, get some flights, look at hotels, do those things now because you want to get in for this one. There are a range of tickets available, whether it’s the standard ticket, the industry ticket, or the whale ticket. And you can get increased access to the whale zones with a stylish environment for networking and meetings. There will also be white glove service and premium food and drinks for those of you who want to get the whale ticket, as well as an exclusive party event. So go to btcprague.com, use code LIVERA for a discount on your tickets. And now back to the show with Greg. Okay. Yeah, so I guess it comes down to protecting against package limit pinning may also stop some of the extensibility of other features, like splicing and so on.

Greg Sanders :

Exactly. So you’re adding on these extra ad hoc measures to stop pinning, but that breaks composability with other smart contracts and whatnot. So you’d love to splice directly to your Coinbase account or whatever, right? But to the counterparty, you might have to prove to your counterparty that, hey, this script has, I can’t pin you in the package sense, right? Package limit sense. Right. But how do you prove that? Right? Maybe it’s Coinbase. It’s not even your address, right? Maybe they have committed to a Taproot script of whatever. We don’t know what that is. So basically it breaks composability when you have to introspect all of the outputs and look at them and say, oh, does it have a time lock on it? That breaks a lot of things, I think. That’s another idea.

Stephan Livera :

I see. So that’s kind of just an open question at this point. And I guess does that conflict then with splicing in general, does that mean we won’t get splicing if we…?

Greg Sanders – :

No, I think splicing is a bit of a red herring. I was just using a motivating example in that as long as the commitment transaction can go to chain, you’re okay. And as long as you aren’t rule 3 pinned, you can package RBF it. So let’s say you do a splice and your counterparty pins it, right. They make a bunch of stuff off it. Well, in the end, you’re supposed to be collaborating with this person and you have a commitment transaction that can go to chain at any time. So you’re okay. You really have to sit there and think about all the situations that can arise based off of the things you have signed. So it complicates things more. But the ephemeral anchors would mean that in a kind of composable way, you can say, I don’t care what the other outputs are saying, I don’t care about the script, like format, of any of these other outputs are. As long as there’s one of these anchors on the transaction, I know I can double spend it, essentially, so I can tie this into kind of I’ve been working on an Eltoo specification for Lightning, and based on this I can remove a lot of things that are complicated, so I don’t have to add any time locks to any of the script outputs. Except for, of course, the contract timeout itself. Like waiting, like the contesting period. Right. So I have to wait a day to claim my funds because I might be lying. Right. They can come back online and put the latest state on the chain. So aside from that, I don’t have to add any time locks. Any of the outputs in any of the transactions can be spent immediately to include fees. Right. So when you’re settling the state, you have your balance output that’s coming out of it, right. You can immediately spend that as a child-pays-for-parent. Today you can’t do that. So when you have a commitment transaction on chain, the only thing you can spend is the anchor, which means you have to bring your own fees always. So it simplifies like the wallet complexity and how much funds you have to have sitting around to settle these smart contracts.

Stephan Livera – 00:37:25:

I see. Yeah. Okay, so could you outline a little bit then? So just for people who aren’t familiar, what is ANYPREVOUT in kind of simple-ish terms? If you could explain that and then just, I guess, summarize the benefit for Eltoo?

Greg Sanders :

Okay. So ANYPREVOUT is an evolution on a proposal that’s been around for a while called NOINPUT. And basically it says normally when we sign a transaction, we’re putting, you know, we’re making a hash like, called a commitment, or like, we’re including all the important transaction pieces that we say the signature attaches to. ANYPREVOUT basically says, well, sign the same stuff, but don’t sign which output specifically this is coming from. So this was any prev out: previous output. So any previous output works for the signature. So what the checks will do is say, is the lock time correct? Are the outputs correct? Some other details, but it won’t look at the previous output identifier. So like the txid and the output number, it won’t look at that. So what you can do is you can sign a series of transactions. Then these can be essentially rebound to any previous output that makes it onto the chain. So for Eltoo, this means there’s a funding output so where you both put funds in at the same time to start your channel. And then once someone goes offline, you can basically put the last version of the signature you’ve had on chain and rebind it to that output. Right. If an attacker, if a counterparty puts an old version of the channel on chain, then you can rebind your latest version to the output they just created. Essentially, you’re building this chain of state outputs, and any of the newer state transitions can attach to older ones, any older one, essentially.

Stephan Livera:

So as I understand, and I believe this is the way Christian Decker explained it to me, is that it’s like a ratcheting effect that let’s say I publish an old state, you’re allowed to publish any newer state, and yours will be regarded as the correct that’s the one that would get confirmed into the chain.

Greg Sanders :

Yeah. So like the 100th channel update can spend the 99th one, the 98th, and so on and so forth, all the way down to the original one. And so that means your overall node state is constant because you have to hold one or two versions of this. In my spec, you have to hold two versions of it. So you’d have to hold the 100th and 99th in memory or on disk or something. And also for watchtowers, it’s the same. A watchtower will only have to hold one version of the transaction.

Stephan Livera :

Yeah. So just to summarize, then, the idea with ANYPREVOUT is there are these SIGHASH flags and they relate to what the signature is committing to. And so in the ANYPREVOUT context, so I guess typically we would just be in a let’s say if you’re just in a normal Bitcoin on-chain wallet, it’s just SIGHASH_ALL, right, that’s like the typical usually.

Greg Sanders :

Yeah.

Stephan Livera :

And then in the ANYPREVOUT context, you’d be having a special SIGHASH flag, which lets you re-, and this is the re-binding concept, right, so it’s saying, let me re-bind this input, right?

Greg Sanders :

Exactly. That’s exactly right. So you might do SIGHASH_ALL ANYPREVOUT, which means I’m committing to all the outputs, but I don’t want to commit to the previous outputs, right, and you can do SIGHASH_SIGNLE, which is, I’m committing to one output but not the input, right? So there’s these combinations that you put together depending what you want. So I use ANYPREVOUT. The version that I use is called ANYPREVOUT ANYSCRIPT, which also means it doesn’t commit to the script that you’re executing, so the tap leaf script, and it also doesn’t commit to the amount.

Stephan Livera :

I see. And so is that going to vary also across script type or are we fully in a Taproot world here?

Greg Sanders :

BIP 118 is only defined under Taproot. So it uses the unknown public key extension hook, which means if there’s a public key, when you do a CHECKSIG operation in Tapscript, if the argument, the public key argument, is not 32 bytes, today it would just say success. Say, okay, that signature passed. BIP 119 redefines two different lengths, the length of one, if it’s one byte long and it’s the number one, then it considers it the internal public key. So the Taproot internal public key, which you can define that, or if it’s 33 bytes and it was a leading 1, then the last 32 bytes are considered a normal public key, normal Taproot, like a public key for CHECKSIG. But it turns on this new SIGHASH mode. So if it has a leading one, that means you’re allowed to do ANYPREVOUT for that key. You don’t have to, but you can.

Stephan Livera :

Right? Yeah. And so I guess that’s the other part where it’s opt-in. Right. People don’t have to use ANYPREVOUT if they don’t want to. Right. I guess that’s an important concept for people to understand.

Greg Sanders :

That’s right. And it won’t be activated for key spend when you’re doing a top-level spend. So 99.9% of the time you wouldn’t be using it. It’s used for these very special smart contract cases that ideally would never make it to chain anyways.

Stephan Livera :

Right. Yeah. And so then summarizing some of the things. As I understand that an Eltoo context or just moving to Eltoo, it would make backups a lot easier. It would make watchtowers a lot easier. And it would also enable this concept of multiparty channels, right, or in future?

Greg Sanders :

Yeah. So the spec I have written now is for two party, but it was written at least the transaction structure is written with an eye for multiparty. So given version 3, ephemeral anchors, and BIP 118 and package relays, these like concepts together, you can fairly trivially expand this to multiparty. There’s tradeoffs, of course, and the peer to peer messages would have to change a fairly significant bit. But I think the parts are there and it can at least be considered. It might be a good intern project or something to work on that. But I’m focused on the two-party case for now. Just seeing implementing a spec and actually implementing it in Core Lightning has been my work for the last almost a year now. And I’m just pushing that ball forward.

Stephan Livera :

Right. And so could you spell out the difference for us in the models of LN-Penalty and the Eltoo way where, as I understand, we might be taking away the penalty and it’s more just updating to the correct state as opposed to having some kind of a penalty.

Greg Sanders :

Right. So Lightning Network today, some of those developers call it LN-Penalty, which means like Lightning Network penalty-based channel. And this is the idea where you have a punishment where if you put the wrong version on chain, intentionally or not, all the balance can be taken by the counterparty. This requires asymmetric state, meaning each of us need a different version of a transaction or at least different witness data, usually different state data, and you have to track this in perpetuity. There’s another version of it called Daric which is an ANYPREVOUT-based penalty channel construction for two parties. So it would get you a lot of the efficiency of improvements that we’ve been talking about, these O(1) state efficiency improvements, but it would retain the 100% penalty. The one I’m working on is dubbed LN Symmetry because it’s symmetric state. So you have this symmetric channel state, symmetric transactions and it has no penalty because since it’s symmetric, there’s no way of ascribing blame, at least mechanically, right? If a transaction shows up on chain, either of the counterparties could have done that. There’s also in-between versions as well. So Anthony Towns has a proposal adding in optional penalties. So optimizing for the two party case and you can add in penalties if you want. And these could be partial penalties. So you could do a percent of the channel balance, a constant size. You could penalize just the HTLCs outstanding, things like that. So it’s like a parameter you could set but it’s a little more difficult to add in watch towers. You can do it, but it re-adds some of the complexity you’re trying to avoid because you don’t want a watchtower to basically play an old state that penalizes you. That’s kind of the key.

Stephan Livera :

I see. Yeah. To me it sounds I mean, I understand there may be some people who want the penalty aspect because they believe that helps stop bad actors, let’s say. But maybe on the other hand, if we have it in a way that’s symmetry, like the LN Symmetry model, it’s arguably more scalable and a little bit easier to transition into, let’s say, the multiparty channel future hypothetically, right?

Greg Sanders :

Yeah. So without penalties, the multiparty scenario is pretty simple to think about. The most naive construction is all the parties have to be online to sign new versions of the transaction which may or may not make sense depending on what your channel partners are like. But it does mean that watchtowers become a lot kind of safer. And I think the incentive here in a penalty-less world would be that you want to be online and your counterparty will want you to be online because it’s the cheapest thing to do. If watch towers are plentiful and it’s easy to get a correct version of the transaction on chain, basically your counterparty will be incentivized to reach out to you and make sure you get back online essentially because it’s the cheapest way you get your money back immediately and it’s cheaper in fees anyways.

Stephan Livera :

Yeah, awesome. And so, as I understand and this kind of gets to that idea of if you really want Bitcoin to scale non-custodially or self-custodially to as many people as possible, then having some way of scaling the number of people who are using one particular UTXO, this would be a big win. Right. Could you outline a little bit how you’re viewing that? Like, let’s say over the longer term, this could really improve self custody?

Greg Sanders :

Yeah, I think so. It improves liquidity. So if you have a channel with two people, right, you have two different channels with two different people, liquidity has to be spread between those two channels. But if you do a three-person channel, a clique between these two people and you, then all the liquidity is deployable to each direction. Right. So it’s a liquidity improvement. So for small numbers, I think a kind of basic multiparty setup makes sense. But if you’re getting to larger numbers, you probably have to think about introducing new complexity to take care of the fact that someone will probably be offline at any given moment. Right. So that’s where things like channel factories comes into play and there’s more complexity and there’s more time locks happening, so things can take longer to settle on chain. So I haven’t really focused on that too much, but they’re definitely possible.

Stephan Livera :

I see. Yeah. So I guess we could think of it like there’s a pathway there, though, whereas if we, let’s say we never get any more soft forks in Bitcoin, that will restrict the number of people who can realistically self custody because you have to be able to at least open a Lightning channel and have a UTXO. And I guess it’s going to be difficult to scale that UTXO set to billions of people. It’s just not at all feasible, right?

Greg Sanders :

Yeah. And I think that will always be the case because you have to have a realistic threat of being able to leave the smart contract. Right. And I think that’s always that’s going to be very difficult, I think, for large numbers of parties. I think it’s a fairly unsolved problem how to make this scale. I think something like the roll-up model, where you have a trusted coordinator, trusted in the sense of they can make channel, like state updates unilaterally, sort of, as long as they’re authorized by the individual participants and that allows them to batch these state updates. Right. But you still need this fallback period, this fallback where you as an individual can go on chain. And so you have to have a realistic threat of going on chain yourself at any given moment. Right. And so I think there is a limiting factor, I think, to all these systems.

Stephan Livera :

Yeah, that’s fair to say. Because I guess, again, some of this is like there’s so many moving parts, we don’t know what happens but it’s quite possible that longer term fees rise a lot. And so perhaps in an ANYPREVOUT world, in an Eltoo world, people can share the cost of some of those on-chain transactions because let’s say we’re in a multiparty channel where let’s say five of us are sharing that fee as opposed to one guy having to pay the full fee himself. Right?

Greg Sanders :

Yeah. And ideally, you wouldn’t have to go on chain as often because your liquidity wouldn’t have to be spread out over so many channels. Right. So if you can set up, I think the most obvious use case today would be these LSP’s Lightning Service Providers would connect with each other, right. So today they are connecting with each other in a two-party manner, but maybe the biggest LSPs come together and they make a huge clique of liquidity. And that way they can reduce their liquidity requirements, which is a business cost. Right. They’re locking up liquidity for you as a customer, so they can reduce their overall costs while not reducing quality of service. Because I’m just assuming these LSPs are staying online, have high uptime, right?

Stephan Livera :

Yeah, of course. I mean, these would be professionally managed services, right?

Greg Sanders :

Yeah, exactly right. And for end users in the far-flung future, maybe do in small amounts as end user, or maybe we do these new constructions that allow subsets of people to be offline but new states to be signed. Just more complexity has to be considered.

Stephan Livera :

Yeah. And so, in fairness, I mean, it’s not a totally free launch, right? There is going to be more interactivity required.

Greg Sanders :

Yeah. There’s always tradeoffs.

Stephan Livera :

So could you outline, I guess, what are some of the downsides of moving to the ANYPREVOUT Eltoo world? Do you see any?

Greg Sanders :

Well, for LN Symmetry specifically, one big downside is that the timeouts for HTLC will be longer. If you care about that a lot, that means it’ll matter to you. There’s a debate about how much this matters because this essentially makes you a less juicy routing node. So if you want to be a routing node and do a lot of routing, maybe people will go around you because you’re locking up liquidity for longer and it takes them a long time to get their HTLCs timed out, essentially. I think that’s one of the biggest downsides. I think otherwise, I think all the constructions of channels that use ANYPREVOUT are almost strictly superior. Like you can pick Daric or pick the Anthony Towns version or LN Symmetry. I think they all offer something unique. And Daric is sort of a drop-in replacement for LN-Penalty today. In a sense, I think it’s just simply better.

Stephan Livera :

Yeah. And so in terms of the increased interactivity, I guess that’s one other aspect, right? So let’s say we wanted to move into a multiparty-channel world. Then you would now need your Lightning node has to talk to, let’s say four other, let’s say in a five-person channel or whatever, right. You’re having to talk to them and there’s now a chance that one of them is offline at the time you’re trying to sign some kind of channel state update, right? That would be the risk, right, or downside?

Greg Sanders :

Exactly. Today you have a channel and the chance of it being down is the chance of you being down… I forget probability. Basically it’s the chance of you being down or the other person being down, right? And so you add a third person in the mix, now it’s three different people that could be down and only one of them has to be down for the channel to be inoperable, at least temporarily, right? And so basically, as you add large and larger numbers, this probability goes up. So it’s a liveliness requirement, but then it lowers your liquidity requirements and I think that’s the key there.

Stephan Livera:

Yeah, interesting. And yeah, it’s just really fascinating to think about. Of course, this is like kind of way off in the future. Of course, the things that are just here now, if you could sort of talk through for us just so we can understand what would be the process of testing some of these things out and proving it out before people could build enough support for the idea of having ANYPREVOUT as a soft fork?

Greg Sanders :

Right. So I think with any soft fork today, we probably should have tooling already going and proving it out because this is when you really run into design constraints of these soft forks. So what I’ve been working on is the spec and implementation of LN Symmetry using ANYPREVOUT. I’ve been using my own private forks of Bitcoin Core with the necessary soft forks and mempool policies. But Anthony Towns is helping administrate the public signet and also doing the Bitcoin inquisition fork, which is essentially an idea that you can have soft forks which are temporary on a signet, and because coins aren’t worth anything, it’s okay if these soft forks go away or time out, essentially, and so on signet he has currently ANYPREVOUT activated, the current version of ANYPREVOUT, and also Check Template Verify, another software idea by Jeremy Rubin. So basically you have these soft forks already activated. So I could basically run what I have for LN Symmetry, except I have a couple of mempool requirements as we’ve been talking about, and so I’m working on getting those kind of a minimal viable version of it in, so I can do kind of signet testing directly of what I have implemented for Core Lightning. And I think that’s kind of the way forward in general is making sure that if we think ANYPREVOUT is good and it’s good for primarily good for like channel updates, state chains, things like that, I think really it should be proven out first because it could be that we go through a whole activation battle and then it ends up not being the thing we actually want. Right. And so that’s like a big danger. And since the cost is so high, I think it should be proven out first.

Stephan Livera :

Yeah. Okay. And so what does proving it out look like in practice? Does that mean a vibrant testnet for this or a vibrant signet for this? What would it take to really show that impact?

Greg Sanders – :

Yeah, I’m not sure what is sufficient, but what is necessary for me would be for ANYPREVOUT, specifically, does it actually allow a new channel construction, which is significantly superior to the current state of the art, right. Needs significant benefits. So what that means, to me it has meaning. But would Lightning developers in the Lightning Network space be excited to implement such a thing? That’s a big question to me. Right. Because you could deploy a soft fork and no one uses it. Well, that’s not good either. Right. And so drumming up kind of end user support or layer 2 support, wallet support, for these ideas is probably step one. Right. Or step two. Step two. Now, whatever step we’re on, because the idea sounds nice, but would people actually end up using it? That’s question number two.

Stephan Livera:

Yeah. And I think that was maybe one criticism that people had or have sometimes of soft fork ideas is they say, well, is there a commercial impact? Right? Are there going to be people who are going to exactly. Are there businesses who want to build this? Right. And I think, for example, with James O’Beirne’s OP_VAULT, it sounds like some of the commercial people focused on building wallets and products are excited about OP_VAULT because it maybe would help with securing our coins. And so I think OP_VAULT makes sense. But I would love to see this idea of ANYPREVOUT and like multiparty channels, because I guess to me, it would be cool to see more people be able to self-custody than what can today. Right. Because it’s kind of like today there are just limits and we can’t go past them without new technology or otherwise people end up custodial. And so shouldn’t we try to stave that off as much as possible?

Greg Sanders :

Yeah. And I think there’s iteration on what’s the best replacement of current channels we could do today, given current knowledge, and then iterating towards that future. So, I mean, that’s what we’ve been doing for the past year or so. A lot has been learned in the past year, and I think we’re going to keep continuing that.

Stephan Livera :

Fantastic. Well, if anyone wants to get involved, they want to help out or they want to learn more, what’s the best place for them to go, or what are you looking for in terms of involvement or help here?

Greg Sanders :

Right, so there’s an IRC channel, a ##Eltoo. That’s one place, if you hang on IRC. Signet involvement, the Bitcoin Inquisition involvement. So from a developer perspective, getting reviews on that. The Eltoo implementation itself isn’t primetime. It’s proving how the protocol works and channels can be made, payments can be made, payments can be routed, but it’s not like it’s not something I would put money in, right? So it’s more at the stage of kind of gathering knowledge about maybe getting these ideas further out there, the benefits of that for node operators and getting feedback from both like the Lightning Network community, DLC community, state chain community, and seeing if the work that has been done already can be directly ported to these other development communities. So I would love to see, for example, I would love to see state chains using ANYPREVOUT on signet, right. The Mercury Wallet, they have a state chains based off of pre-signed transaction like with time locks, things like that. It would be great to see if they could adapt their protocol to using ANYPREVOUT and then deploying it on Bitcoin signet.

Stephan Livera :

And it seems to me from most Lightning people I talk to, they are in favor of ANYPREVOUT. I’m curious, what kind of feedback have you had from the Lightning community? Lightning devs, Lightning users?

Greg Sanders :

I think of a pretty solid excitement. People still have different opinions on penalties and whatnot. But I think that’s kind of now that we know that ANYPREVOUT can construct kind of a fairly wide array of parameters and architectures, I think we’ve crossed that threshold at least. So next would be getting in the LN dev community, getting buy-in on kind of a specific architecture to move towards as maybe a proof of concept of interoperability. Right. So it’d be great if Core Lightning and Eclair or some LDK-based one would be able to do Eltoo payments on signet.

Stephan Livera :

Yeah, okay, so it comes back to again, that proving-it-out aspect. Okay, yeah, I think that’s a fair point. So yeah, I guess outside of the ANYPREVOUT and Eltoo and LN Symmetry stuff, is there anything else that you would like to see in Bitcoin or Lightning development or just in general? I’m curious, are there any other things that you’re interested in?

Greg Sanders :

Yeah, all the tooling is pretty interesting to me. So I’ve been using Miniscript and playing around with it and I’m waiting to see Taproot support for Miniscript. I’m helping get all this Taproot support Tapscript support, Miniscript support, all this stuff just takes time to build. These are basically standards we’re building and we’re building on top of these standards, which makes life easier going forward. I mean, I’m excited about another big project I’m excited about is Fedimint and Fedi. I think that’s a very interesting way forward for pleb use cases and smaller amounts. Right. Privacy. So I’d say that’s kind of the shorter term thing I’m most excited about is tooling and kind of this federated Chaumian mint stuff.

Stephan Livera :

Fantastic. Well, I think that’s probably a good spot to finish up there, Greg. Any closing thoughts for people?

Greg Sanders:

If you’re interested in any of these other topics, just reach out to me. I’m on Twitter sometimes, @theinstagibbs,

or on IRC as instagibbs. So love to talk to anyone about this stuff.

Stephan Livera :

Fantastic. Well, thanks for joining me and definitely a very informative chat for me, so thank you.

Greg Sanders :

Thank you, Stephan.

Stephan Livera :

I hope you found the episode educational. I certainly did. Get the show notes at stephanlivera.com/463. Thanks for listening, and I’ll see you in the citadels.

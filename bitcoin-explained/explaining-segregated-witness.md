---
title: Explaining Segregated Witness
transcript_by: nillawafa via review.btctranscripts.com
media: https://www.youtube.com/watch?v=DsyMUzhfG34
tags:
  - segwit
  - soft-fork-activation
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-03-18
episode: 32
aliases:
  - /bitcoin-magazine/bitcoin-explained/explaining-segregated-witness
---
Aaron: 00:01:46

Live from Utrecht. This is The Van Wirdum Sjorsnado. Hello. Sjors, we're going to talk about a classic today.

Sjors: 00:01:52

Yeah. We're going to party like it's 2015.

Aaron: 00:01:55

SegWit.

## Segregated Witness

Sjors: 00:01:56

That's right.

Aaron: 00:01:57

Segregated Witness, which was the previous soft fork, well, was the last soft fork. We're working towards a Taproot soft fork now.

Sjors: 00:02:06

It's the last soft fork we know of.

Aaron: 00:02:07

Exactly yes I guess so. It activated in 2017. It started being developed in 2015.

Sjors: 00:02:17

I think it was late 2015, yeah, that the final idea came about to turn it into a soft fork.

Aaron: 00:02:24

Yeah, and it's probably, would you say, it's probably the biggest protocol upgrade Bitcoin has seen so far, right?

Sjors: 00:02:31

Well, it's the biggest protocol upgrade we've seen since the days of completely reckless deployments of upgrades, right.

Aaron: 00:02:39

Wouldn't you say it's almost the biggest code change for example?

Sjors: 00:02:43

Yeah, I think so. it's bigger change than P2SH, but I don't know what was done in the very early Satoshi days, you know when hundreds of opcodes were turned off and all that stuff.

Aaron: 00:02:54

So where do we start? Do we start...

Sjors: 00:02:57

We could start with what the problem was.

## Why Do Witnesses Need To Be Segregated?

Aaron: 00:02:59

Okay what was the problem? Why did we need SegWit Sjors?

Sjors: 00:03:02

Yeah why do witnesses need to be segregated? So the problem was transaction malleability, and transaction malleability means that if I'm sending you some coins and you're sending them to Ruben, who's not here, then that transaction that you're sending refers to the transaction that I just sent. And the problem there, and that's fine normally, but the problem is that somebody could take our transaction and manipulate it. It could take my transaction and manipulate it and then your transaction would no longer refer to my transaction but would refer to a void.

Aaron: 00:03:41

Yeah, and to be more specific, I think the part of the transaction that's being manipulated is actually the signature. So every transaction is signed with a cryptographic signature and the signature, I don't understand the details, but I know that the signature can be tweaked somehow in a way that it looks different, but it's still valid.

Sjors: 00:04:00

Yeah, and there were lots of ways to do that. So one of the ways that was fixed without SegWit is that you could, I think, just multiply the signature with minus one or something, just put a minus in front of it, and it would still be valid. And so anybody could just put that minus in front of it so you you would broadcast a transaction and it would go from one node to the other somebody else could see that transaction and they could say well I'm just gonna flip this bit and send it onwards and then we'll see which one wins and and this is just for simple signatures but I think there were other if you have more complicated scripts there are also ways that somebody can mess with that script.

Aaron: 00:04:38

Yes if someone can mess with it in flight, basically you send a transaction to the network and then it's forwarded from peer to peer and till it reaches miner and it's included in a block but every peer on the network but can basically take the transaction, tweak it a little bit, and forward it, or the miner can do that

Sjors: 00:04:55

Yeah, I guess even the person making it can do it, yeah or the miner can do it So you may ask yourself why is this a problem right because I sent you some coins and you sent them to Ruben, okay I ruined your transaction so you just send it again so that's that's not a big deal.

Aaron: 00:05:09

You didn't really ruin the transaction, you just tweaked it a bit but it's still valid.

Sjors: 00:05:13

Well I ruined your transaction, so I send coins to you and you send coins to Ruben, but that last transaction no longer points to an existing transaction because somebody messed with my transaction.

Aaron: 00:05:25

Yeah, it's the second transaction that's getting in trouble.

Sjors: 00:05:27

Yeah, and this is not a problem in the scenario we just described, right? Because you can just make a new one, *except *what about if you're not you but what what if I sent a transaction to a super-secure vault in the Arctic, like thousands of meters underground, and then I went to the Arctic and I created a redeemed transaction back to my hot wallet, but I didn't broadcast it, I just signed it...

Aaron: 00:05:53

Why are you making such a complicated example with vaults and arctics?

Sjors: 00:05:58

Well, this one isn't that complicated. I just, you know, I went to my vault, I created a transaction out of my vault, and then I basically buried the vault in like 100 meters of rock. So it's very difficult for me to go back to the vault and make a new transaction. And then I broadcast my original transaction, it sends the money to the vault and somebody messes with it. Now I have to go back to Antarctica and there's COVID and it's very complicated.

Sjors: 00:06:25

 So that's a terribly difficult example. Another example would be Lightning.

Aaron: 00:06:27

Yeah that's the more obvious one.

Sjors: 00:06:29

Yeah so with Lightning what happens and we've explained Lightning in earlier episodes, but the idea is you send money, two people send money to a shared address, and then the only way to get money out of that address is with transactions that you've both signed before you sent money into that address. So you don't want somebody messing with the transaction that goes into the address, because then you can't spend from it anymore. Or you can, but you'd both have to sign it again. And so one party could kind of cheat the other party out of the coins.

Aaron: 00:06:58

Yeah, the point with Lightning is that you're building unconfirmed transactions on each other. So if one of the underlying transactions is tweaked, then the transactions that follow up on that one aren't valid anymore.

Sjors: 00:07:11

Yeah, and people spent lots of time trying to find ways around that problem, you know, because people were thinking about Lightning-like solutions quite a while and it was just really hard to solve.

Aaron: 00:07:21

Yeah, so to be clear, the concrete attack in this Lightning example is that one of the parties would tweak the transaction they shared between them, send this tweaked transaction to the network, and then I guess the other party probably wouldn't even recognize that transaction, or even if he did, he couldn't use his own transaction to get his funds back. Am I saying that right?

Sjors: 00:07:44

Yeah, all the transactions that get your funds back are no longer valid. So this could be a problem, you know, in all the cheating scenarios.

Aaron: 00:07:50

Yeah, exactly. So, there's also another well-known example, which was the Mt. Gox case. And that was, you know, a mistake on the part of Mt. Gox as well. If we assume that the story we've been told about how the hack happened is really true, but the story was...

Sjors: 00:08:08

The hack or you mean one of the many hacks?

Aaron: 00:08:10

The big one basically. They claimed that the big one was due to transaction malleability. And the story was that they were basically doing their internal accounting based on transaction IDs. So a customer would withdraw funds, use malleability to change the withdrawal transaction a little bit, still get the money because the transaction is still valid, but then claim "guys, I made a withdrawal but I never received the money." Mt. Gox would take the transaction ID, look if it was in the blockchain, saw that there's no transaction ID like that in the blockchain. Our customer must be right and then resend the coins.

Sjors: 00:08:52

Yeah, but there are so many other things you have to do wrong for that particular thing to happen. But anyway, let's blame it on malleability.

Aaron: 00:09:00

I'm just giving an example of something that could go wrong because of malleability if, yeah, in this case you make other mistakes as well. So that was malleability. So that's what we want to solve, right?

Sjors: 00:09:11

Yeah, and there have been partial solutions to this already, because it's a much bigger problem than just the signature I think. But in either way, it turns out that it seems like a whack-a-mole game that's just really hard to solve. And the fundamental problem there seems to be that because you're pointing to something that includes a signature, it just gets too complicated. One thing Segwit does is it no longer refers to the signature because it refers to, well, the signature is put somewhere else in a transaction, in some sort of extra data.


## Explaining SegWit in the Context of Transaction Data


Aaron: 00:09:46

To make this very clear, in case some of our listeners aren't keeping up, the thing is a transaction consists of all of the transaction data plus the signature. Formally, or usually, or still the case in some transactions the transaction data and the signature is hashed together. This gives you a string of numbers and that's the transaction ID. Now, because the signature can be tweaked, that means the hash, meaning the transaction ID, can also be tweaked and you end up with basically the same transaction with a different transaction ID and that causes all the problems we just discussed. So that's the problem we needed to solve. Somehow we need to make sure that a transaction would always result in the same transaction ID.

Sjors: 00:10:33

Yeah, so the solution there is to put the signature in a separate place inside the transaction that, as far as old nodes are concerned, doesn't even exist. And you still refer back to other transactions by the original data. So the original, basically the original part of the transaction, that still creates the hash. And the signature is this new data and you do not use it to create a hash.

Aaron: 00:10:58

Right. So the signature ID can't be tweaked anymore because the signature isn't in there anymore.

Sjors: 00:11:04

Right, so you can still tweak the signature if you wanted to, although there's some limitations on that too, but if you tweak the signature, that's not part of the hash. And this is nice, right? So that's one thing it does, SegWit, and the other thing it does is it just because this data goes into a place that old nodes don't care about, well suddenly you can bypass the one megabyte block size limit without a hard fork. Because old nodes will see a block with exactly one megabyte in it, but new nodes will see more megabytes.

Aaron: 00:11:35

Yeah, blocks have a one megabyte limit, and that used to be transaction data plus all the signatures, plus a little bit of metadata. And now it's basically mostly the signature data and not the signatures and that's where the block size increase comes from. The signatures is sort of the increase.

Sjors: 00:11:55

Yep, exactly. And that's theoretically up to four megabyte but in practice it's more like two and a half I guess the total size that you get for blocks.

Aaron: 00:12:05

Yeah, why is that? There is some new calculation for how data is counted when it comes to the signature?

Sjors: 00:12:15

Well yeah, so I think what happens is you take the old data and you multiply it by three or something, and then you take the new data and you add it up. So the signature is kind of discounted in a way. And that's kind of an arbitrary number, but at least it creates an incentive to use SegWit.

Aaron: 00:12:33

Right. And that's also why it's a bit more flexible now, the block size limit. If there are many transactions with many signatures, for example, multi-sig transactions, then the size of the blocks could be a little bit bigger because of how it's all calculated.

Sjors: 00:12:50

Right, because with the usual old-fashioned transactions, there is not much going on in terms of signatures. There just aren't that many signatures, but you could conceive of much more complicated transactions that have much longer signatures, like in a multi-sig situation, and those are quite nicely discounted in SegWit.


## SegWit as a Soft Fork


Aaron: 00:13:07

Right, so how is it possible that SegWit could be deployed as a soft fork? Which means backwards-compatible upgrades, so old nodes still recognize the SegWit chain as long as it has majority hash power at least.

Sjors: 00:13:25

Yeah and they do this because this new data that we've added is not, like it's not communicated to all nodes. So every transaction has a little piece of witness that's not communicated to all nodes and every block has a part that is the witness that's not communicated to all nodes. So every transaction has a little piece of witness that's not communicated to all nodes

Aaron: 00:13:44

First of all, where is this part?

Sjors: 00:13:46

I think it's at the end of the block.

Aaron: 00:13:49

It's in the Coinbase transaction right?

Sjors: 00:13:52

So I think it's appended at the end of the block but it's also referred to in the Coinbase transaction because what you do want to do is you want to make sure that you know the block hash just refers to the things that are in the block. But it only refers to the things that are in a block as far as legacy nodes are concerned. But you don't want to tell the legacy notes about the SegWit stuff. So what happens is there is a `OP_RETURN` statement in the Coinbase, which refers to a hash of all the witness stuff.

Aaron: 00:14:20

Yeah, the Coinbase, in case listeners don't know this, isn't just a company, it's also the transaction that pays the miner his rewards. So basically the first transaction in any block.

Sjors: 00:14:30

Yeah, and that transaction can just spend the money however it wants but it has to contain at least one output with `OP_RETURN` in it and that `OP_RETURN` must refer to the witness blocks. So all nodes just see an `OP_RETURN` statement and they don't care.

Aaron: 00:14:44

And `OP_RETURN` is a little bit of text.

Sjors: 00:14:47

Yeah, `OP_RETURN` basically means, okay, you're done verifying, ignore this. But it can be followed by text, which is then ignored. Except by new nodes, which will actually check this. So this allows the nodes to communicate blocks and transactions to new nodes and to old nodes and they all agree on what's there. And the other thing, the other reason why this can be a soft fork and that's more important for the new nodes is, well, you're spending, where are you sending the coins to when you're using SegWit? So you're using a special address type now. And this address type, or like on the blockchain, what you have is a script pubkey, that is what an output says. So an output of a transaction tells you how to spend the new transaction. It puts a constraint on it. And so this script pubkey with segwit starts with a zero, or at least does now, but with taproot, it'll start with a 1. And then it's followed by the hash of a public key, or the hash of a script. And new nodes know what to do with this. They see this version 0, they know, okay, this is SegWit the way we know it, and they see a public key hash, and they know, okay, whoever wants to spend this needs to actually provide the public key and a signature. But old nodes, what they see is, okay, there is this condition which is put 0 on the stack and put this random garbage on the stack that I don't know what it is. And the end result is there's something on my stack and it's not 0 and I did not fail. And so, okay, whatever, this is fine, you can spend this. So, old nodes think that anybody can spend that coin, but new nodes know exactly who can spend it and who cannot spend it.

Aaron: 00:16:27

Yeah, it's actually called "anyone can spend". Yes. So, in a hypothetical situation where there would only be all the nodes on the network, then it would also literally mean that the coins in these addresses could be spent by anyone.


## SegWit and Taproot


Sjors: 00:16:40

Yeah, this is why the activation of Taproot was of course, you know, always exciting because yes, the miner signaled, but okay, what happens?

Aaron: 00:16:48

Yeah, we discussed that in the last episode of I think or the one before that

Sjors: 00:16:52

Well, in general we talked about you know what can go wrong with soft fork activation and this this would be one of it and so well it didn't go wrong so that's good

Aaron: 00:17:01

yeah so the reason it didn't go wrong is because if there's a mix of old and new nodes on the network, but most miners enforce the new rules, then most miners will ensure that these coins in the "anyone can spend" outputs from the perspective of old nodes won't actually get spent.

Sjors: 00:17:18

That's right.

Aaron: 00:17:19

They'll consider blocks that spend these coins invalid, and as long as they're in the majority, they'll also create the longest chain. So now new nodes are happy because all the new rules are being followed, and old nodes are happy because no rules are being broken from their perspective, and they just follow the longest chain, so everyone's still in consensus.

Sjors: 00:17:38

Yeah, and this rule I just told you about, this script pubkey that puts things on the stack, and as long as it's not zero, everybody's happy, it's kind of a hack. It's kind of just leveraging some ugly aspect of, you know, ancient ways that Bitcoin scripts work. But with SegWit, the first thing will be the number 0 or the number 1, etc. And this actually introduces a cleaner variant of the same principle, which is that as far as a SegWit node is concerned, if it starts with the number 0, it's going to enforce the rules. If it starts with the number 1 or higher, it'll consider it a, it doesn't matter, anybody can spend this. And if we get taproot, then the new nodes will see version 0 they'll enforce the rules they'll see version 1 they'll enforce the rules but if they see version 2 or higher they'll just consider it valid and that means that moving forward you know it's much easier to introduce softworks like Taproot without having to find another hack in the old scripting system to exploit.

Aaron: 00:18:39

Right, so SegWit was a little bit of a hack, but it was in that sense a one-time hack because now we can use versioning and every time we want to introduce a new rule for spending coins it's gonna be pretty clean and easy moving forward.

Sjors: 00:18:55

Yeah exactly and within Taproot, I guess there's a little out of scope for this one, but within Taproot we have these multiple branches that can have their own condition and those scripts also have a versioning mechanism so there's even more versioning that can be done.


## The Merkle Tree


Aaron: 00:19:08

Right, one more question Sjors, we mentioned that the signatures, they're included in the end of the block you mentioned.

Sjors: 00:19:16

I think they're just dependent.

Aaron: 00:19:18

But there's a reference in the Coinbase. So how are all these transactions included in one little transaction?

Sjors: 00:19:25

Well, it's called a Merkle tree.

Aaron: 00:19:27

A Merkle tree? This sounds exciting.

Sjors: 00:19:29

We talked about Merkle trees in an earlier episode.

Aaron: 00:19:31

I think we did.

Sjors: 00:19:32

Quite at length, we tried to explain him and it was possibly quite terrible, but we've done it and we're not gonna do it again. But basically, it's essentially just taking a hash, but the Merkle tree is a little bit more elegant than a hash because it allows you to like point to specific elements inside the tree. A hash will just say yes or no for everything that's in it, could be a whole megabyte, it's correct or not. But with a Merkle tree, you can say, okay, I can actually prove that this specific transaction exists inside that tree at that position without having to reveal everything else in it. And that's kind of cool.

Aaron: 00:20:05

Yeah, and I think it's essentially sort of a mirror of the actual transactions, right? Which are also included in the Merkle tree in the block. And then there's a...

Sjors: 00:20:14

Yeah, it's the same idea. So it's not rocket science.

Aaron: 00:20:17

So we have one Merkle Tree for transactions, the regular transaction data, and then sort of a mirroring Merkle Tree for all the references to the signatures in the Coinbase block, right?

Sjors: 00:20:27

Yeah, exactly. And I think you could generalize that to something called extension blocks, where you could add something else to transactions in the future and just refer to that in a coinbase output and so you could, you know, increase block size through soft forks to a degree. But you can't really go super far with that, because as far as the *old *old nodes is concerned, there still has to be a valid transaction out there, and a valid transaction probably has to have at least an input, and at least an output, even if the output says do whatever you want with this. Can't make it smaller than that. And there's still the one megabyte limit as far as these old nodes are concerned. You can't use extension blocks just to add data to transactions. You can add it to, you can use it to add data to transactions, but you can't use it to create an infinite number of transactions because those transactions have a minimum size. Probably about 60 bytes.

Aaron: 00:21:25

We're going off the rails.

Sjors: 00:21:26

That's fine. All right, bring us back to the rails. I think there were some other benefits of SegWit that we wanted to mention?

## Benefits of Segwit


Aaron: 00:21:32

Well, so we mentioned transaction malleability is solved, which was necessary for something like the Lightning Network. So that, you know, that's why we have Lightning Network now, because we had SegWit. The other benefit we mentioned is Block size limit increase.

Sjors: 00:21:47

Yeah, and I guess we had four years almost of low fees. Now they're high again.

Aaron: 00:21:53

Yeah, they're stacking up now. Then we had the versioning, so easier to make new upgrades. Were there more benefits than that?

Sjors: 00:22:03

Yeah there is. There is committing to the inputs. So this is fun for hardware wallets. If you're a hardware wallet and you want to sign something, we talked about that in one of the very first episodes where we explained that if you're a hardware wallet and you want to sign a transaction, you want to look at the output amounts, you can do that. But you want to make sure that the input amounts actually sort of add up to the same as the output amounts so that money isn't just disappearing into fees. But the only way to do that is to actually have the input transactions and look at their output amounts. And so that meant that in the old days you would have to send all the input transactions to the hardware wallet as well and it would have to process them and it's kind of a lot of work or it could be a lot of work if they're big transactions.

Aaron: 00:22:48

Yeah, so to be clear, this is always the case for any wallet. You always, you know, you have inputs, that's the coins you own, and then you have the outputs, that's the coins you're sending, including a change output to yourself usually. And then the difference between them, that's the fee, and that's for the miner to keep.

Sjors: 00:23:08

Yeah, the fee is not actually mentioned in the transaction.

Aaron: 00:23:11

Yeah, exactly. There's no fee amount or anything like that in transaction. You just have to calculate it yourself. That's fine for regular wallet because the regular wallet just knows how much all of the inputs are worth and the outputs are obvious there in the transaction. And then the difference, it's easy to calculate but a hardware wallet is basically just signing from private keys and it doesn't necessarily know how much all the inputs are worth. So now it's... Am I saying this right?

Sjors: 00:23:41

Yeah, that's right.

Aaron: 00:23:42

It's sending money away, but it's actually not sure how much money it's sending. And therefore, a hardware wallet has the risk that it's sending 10 million coins as a fee without realizing that.

Sjors: 00:23:55

Right, the main problem there is the fee could be arbitrary and so if somebody colludes with a miner or just wants to take your coins hostage in some weird way, that's not good. So what SegWit does is it commits to those inputs. So normally a transaction, you know, in the old days, the input would just be the ID of the transaction that we just talked about with all the malleability stuff and yeah the the index, basically so a transaction has multiple outputs so you'd say this is spending output zero of this and this transaction and with SegWit what's basically added to that is the amount... actually not just the amount the I think the entire transaction. So take the transaction and hash it, and that's what you're committing to now. And that includes the output amounts of that transaction. So now when you're signing it, you can check it. It could still be entirely fake, by the way. You could craft a fake transaction with fake inputs and any output amount you want, but then if the hardware wallet signs it and you put it on the blockchain well it's not gonna be valid so that's kind of a useless cheat.

Aaron: 00:24:57

Yeah we talked about that in episode 2 maybe?

Sjors: 00:25:00

No I think in the first episode.

Aaron: 00:25:02

Episode one?

Sjors: 00:25:02

Yeah, with the actual tornado.


## Summarizing SegWit Benefits


Aaron: 00:25:04

Right, okay, so now we have four benefits of SegWit. One of them is malleability, which was sort of the main one. I think that was the reason it was included. It was included in the elements sidechain of Blockstream I think before it even made it to Bitcoin and I think that was the reason they had it was solving malleability so

Sjors: 00:25:24

I mean yeah it enables things like lightning so that's a pretty big capacity increase exactly

Aaron: 00:25:29

So that's one and then we have the block size increase, which is two. Then we have the versioning bits, which makes it easier to deploy future upgrades, which is three. And then four, you just mentioned, is the hardware wallet fee issue is solved.

Sjors: 00:25:45

Yeah, or at least we thought it was solved. We explained in the first episode that there's some gotchas. But yeah, those are, I think, the four main benefits, and I think there's some minor tweaks as well in there, but it was a pretty big change compared to that taproot is relatively simple.

Aaron: 00:26:00

Yeah, so I spent a lot of time on reddit.com/r/btc and all I read there is that SegWit is the awfulest thing ever. How comes yours?

Sjors: 00:26:10

The awfulest?

Aaron: 00:26:11

Yes, it's horrible.

Sjors: 00:26:13

Okay, well, sorry to hear that. I don't know. I mean, I've heard more reasonable objections from non-R/BTC places saying, well, it would have been slightly simpler to do it as a hard fork, but the more I look at it, the less I'm convinced of that.

Aaron: 00:26:28

Yeah, I guess the argument there would be that the signature hash reference, the signature hash tree is included in the coinbase and there would have been a cleaner place to put it if...

Sjors: 00:26:40

Well you wouldn't have had to put it anywhere. If you do a hard fork you can just add the witness data to the blocks and in the main Merkle tree, so you don't need to do anything in the `OP_RETURN`.

Aaron: 00:26:50

Right.

Sjors: 00:26:51

But the downside is you need to actually do a hard fork, and just to think through what's involved to do that, that's where all the complexity then goes and all the precedent risk. So I think it's good that this was done as a soft fork.

Aaron: 00:27:04

Yeah, I was saying it in jest, but I think that is probably the only argument that I've heard that even makes slight sense, that That's also being espoused, that English word?

Sjors: 00:27:18

It's been a while since

Aaron: 00:27:20

on r/btc, I meant.

Sjors: 00:27:21

I think that's one of the more serious ones. But other than that, I think the main arguments were, you know, it was a blockstream conspiracy and... Sure, yeah, yeah,

Aaron: 00:27:30

Of course you have all that.

Sjors: 00:27:31

Extra complexity so that Bitcoin Core can get paid more and a whole bunch of other stuff.

Aaron: 00:27:35

Are you a conspiracy denier? Are you asleep still, Sjors?

Sjors: 00:27:41

I'm a conspiracy denier.

Aaron: 00:27:42

Wake up, sheeple.

Sjors: 00:27:43

I'm sorry. I will keep sleeping. I think that's it, right?

Aaron: 00:27:47

I think so, Sjors.

Sjors: 00:27:48

All right then. Thank you for listening to The Van Wirdum Sjorsnado.

Aaron: 00:27:51

There you go.

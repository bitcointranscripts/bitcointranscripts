---
title: Inscriptions
transcript_by: masud-abdulkadir via review.btctranscripts.com
media: https://www.youtube.com/watch?v=Js-5PZi6Uow
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2023-02-08
episode: 72
aliases:
  - /bitcoin-magazine/bitcoin-explained/inscriptions
---
## Introduction

Aaron Van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin Explained. Sjors, we're gonna lean into some Twitter controversy today.

Sjors Provoost: 00:00:27

Exactly, we have to jump on the bandwagon and make sure that we talk about what other people talk about.

Aaron Van Wirdum: 00:00:34

Love it! Yeah, actually I got this request from a colleague of mine, Brandon Green, and since I am his humble servant, I had no other choice but to make an episode about this topic, which is inscriptions, and maybe also ordinals to some extent but yeah as you mentioned everyone's talking about it now which I think for both of us was more of a demotivating factor because everything that's that can be said about it has been said by now maybe. But we're gonna try to at least explain what it is, I guess.

Sjors Provoost: 00:01:08

Yeah, and this may be nice for our listeners who have not caught up on it.

Aaron Van Wirdum: 00:01:12

Okay, but first of all, Sjors , You want to read some boosts.

Sjors Provoost: 00:01:17

Some boostograms. And if you don't know what that is, Google it. First one is nice and short. From @vake. 2500 sats. Second best podcast ever. Behind the Van Wirdum Sjorsnado.

Aaron Van Wirdum: 00:01:30

Love the Van Wirdum Sjorsnado.

Sjors Provoost: 00:01:32

Excellent. And the other one from Mr. Mister 5,674 sats. Excellent topic and explanations. As for topics for the future show, I have some, I need some technical explanation. Perhaps you could be of assistance because I thought I knew how my Lightning channel closed, but my node died and BluWallet seized the on-chain stuff, yay, and I contacted the other node operator and they closed the channel out, yay, but my share of closing Lightning Balance didn't go on-chain. Thanks.

Aaron Van Wirdum: 00:02:07

Is this a question? Did you just...

Sjors Provoost: 00:02:10

Well, I think his question is to please explain how Lightning works to the point that I can fix, I get my money back. But basically this reminds me of something that happened to me a few years ago, which is I had an LND node and a C-Lightning node and I had a channel between them and then I nuked my LND node and I lost the money that was in the channel. But after only two days of puzzling and going to hackathons and talking to Christian Decker and Rosebeef and writing some custom tools, I was able to get my 100 euros back. But the exact way to do that is quite hard and depends on which pieces of software you're using. In this case, I wouldn't know.

Aaron Van Wirdum: 00:02:48

Sorry for your loss, Mr. Mister.

Sjors Provoost: 00:02:51

In general, our lightning expertise is not that. There are some episodes where we struggle to explain certain aspects of lightning. I think we did publish them.

Aaron Van Wirdum: 00:03:00

I mean, we've also had lightning guests on, right? I think that's sort of what we like to do if we do a lightning episode. We'll get someone on board that actually knows more about lightning than we do.

Sjors Provoost: 00:03:11

Yeah, but there's basically, as a general rule, If you have a lightning wallet and your funds are already on chain, those funds should be fine if you have to recover from a backup. But anything that's in a channel requires some sophistication to correctly backup and may be hard or impossible to recover.

Aaron Van Wirdum: 00:03:28

OK, Sjors back to inscriptions, the topic du jour, the new war on Bitcoin.

Sjors Provoost: 00:03:37

Yes.

## Brief Explanation of OP\_RETURN

Aaron Van Wirdum: 00:03:38

The controversy is brewing and we're gonna lean into it with everything we have short inscriptions okay first before we actually get to inscriptions I do want to mention a lot of this ties in with `OP_RETURN` and we made an episode on `OP_RETURN` on the `OP_RETURN` Wars as it was referred to, which was episode 61, 
and we'll recap some of that here, but maybe not all of it. So if you really don't know, and now I'm addressing you, my dear listener, our dear listener, if you don't know what `OP_RETURN` is, then you might wanna go back to episode 61 first to sort of get an idea of what the history there is. That said we will recap it real quick. Yeah sure, so I'll just leave this to you. `OP_RETURN`, What do we need to know before we get to inscriptions?

Sjors Provoost: 00:04:33

Yeah, so `OP_RETURN` was a solution to a problem. And the problem was that, well, the problem wasn't so much that people were putting stuff on the blockchain that wasn't money. They were putting pictures, etc. On the blockchain. That wasn't necessarily the problem, but the problem was in how they were doing it. They were using weird mechanisms. 

Aaron Van Wirdum: 00:04:52

I'll stop you right there. That's debatable, right? Some people will say that's in itself a problem.

Sjors Provoost: 00:04:57

Yeah, some people would, but there was a bigger problem, and that was in the way that we're doing it. And the way that we're doing it was causing the so-called UTXO set to grow a lot. And the UTXO set is basically the set of coins that exist in the world and that could be spent by somebody at any time. You don't know when it's going to be spent. So you tend to keep it in RAM so that whenever a new block comes in, you can very quickly check whether the new block is spending coins that actually exist or not. And the problem with the way they were putting data on the blockchain is they were basically making it look like there were real coins out there that could be spent with public keys and all, but they were really, they could never be spent because there was no private key because of the way the images were encoded. And so `OP_RETURN` was a sort of a mitigation of that by saying, okay, please use this mechanism called `OP_RETURN`, and we'll explain how that works, so that we don't have this problem with RAM. 

Aaron Van Wirdum: 00:05:53

I don't think we will. People will have to go back to episode 61, Sjors.

Sjors Provoost: 00:05:56

All right, fine. We won't explain it. Or we might get back to it. Anyway, so people could use `OP_RETURN`, they could put up to 80 bytes on the blockchain this way, in a way that doesn't waste people's RAM, still takes space in the blockchain, but it doesn't waste people's RAM and RAM is much more precious.

Aaron Van Wirdum: 00:06:13

Yeah, so the even shorter version is people were using Bitcoin for other reasons than transacting money. They were uploading images on the blockchain or whatever. And then developers said, all right, look, if you're going to do that anyways, then please do it in this way because that reduces the cost for everyone else. That's sort of the super short version, right? But then developers also said, please don't do too much data at once. So they set a limit of 80 kilobytes, essentially, right? 

Sjors Provoost: 00:06:48

80 bytes.

Aaron Van Wirdum: 00:06:49

80 bytes.

Sjors Provoost: 00:06:50

Per transaction, which means in practice, in order to do a lot of data, you need not just to have this 80 bytes, but you need to make a whole transaction, which has a bunch of overhead on top of the 80, for every 80 bytes that you're trying to publish.

Aaron Van Wirdum: 00:07:02

Right. So developers said, all right, if you're going to upload data on the blockchain, please use this. But then they did put a limit on the amount of data that you could upload.

Sjors Provoost: 00:07:11

Yeah. And if I remember correctly, that limit was basically such that it was slightly more attractive to use `OP_RETURN` than to use the bad methods that we used before, but not unnecessarily attractive.

Aaron Van Wirdum: 00:07:22

Right. Okay. I think that's sort of the context that you need for the rest of this episode, to get into inscriptions. I think, right?

Sjors Provoost: 00:07:34

Yeah, I think so.

## What Inscriptions are

Aaron Van Wirdum: 00:07:34

Okay, so inscriptions then, I guess my one sentence summary would be, inscriptions are a way to do the same thing, to do what `OP_RETURN` does, but without the limit. Is that a fair one sentence summary?

Sjors Provoost: 00:07:52

Well it has a 400 kilobyte limit.

Aaron Van Wirdum: 00:07:54

Someone found a way around the limit that someone is Casey Rodamore.

Sjors Provoost: 00:07:59

Yeah so instead of an 80 byte limit he found a way to have a 400 kilobyte limit and to get a 4x discount on fees. And in fact, there will be a bigger discount in fees because the overhead of the transaction itself would be lower if you're doing very large pieces of text or image.

Aaron Van Wirdum: 00:08:16

Okay, so then the one sentence summary is, someone found a way to do something very similar to `OP_RETURN`, but with a much bigger limit and with a cheaper, at least cheaper per byte fee wise. Yeah. That's a very ugly sentence, but I still think that counts as one sentence.

Sjors Provoost: 00:08:39

Whatever.

Aaron Van Wirdum: 00:08:40  

Okay, so that's what it does. And then there was this other thing, I forgot what it was called. We're not going to talk about it too much in this episode.

Sjors Provoost: 00:08:51

The Ordinals.

Aaron Van Wirdum: 00:08:52

Yeah, right. Ordinals.

Sjors Provoost: 00:08:53

It's part of the Ordinals system, which is something completely different, a way to do NFTs on the Bitcoin blockchain, I guess. And part of that could be that you want to upload the picture of your NFT right onto the Bitcoin blockchain. That's one use case. But this mechanism...

Aaron Van Wirdum: 00:09:08

Well, that's still inscriptions, right? Like uploading the actual picture, that would be the inscription. And then the ordinal, that would be like a colored coin, essentially, that refers to the inscription. So then you can quote unquote own the inscription in the same way that you can quote unquote own an NFT.

Sjors Provoost: 00:09:31

Yeah pretty much, But it doesn't really matter because the way that you put data on the chain is the same, it could be used for other things.

Aaron Van Wirdum: 00:09:38

Yeah, right. So that's what the inscriptions are. Inscriptions are uploading data into the Bitcoin blockchain. And that's probably, It seems that's sort of what most of the controversy, the Twitter shitstorm, is about. And that's also what we're going to address mostly in this episode. I don't think we're going to get into Ordinals too much, although we've already mentioned it. So, Sjors, how does it work? How did Casey get around this limit, this `OP_RETURN` limit? What's the...

Sjors Provoost: 00:10:10

Yeah, so basically the way `OP_RETURN` works is you're creating an output basically. And when you create an output, you basically have to tell the nodes or the blockchain what way this output can be spent. And that's fine. You basically say `OP_RETURN` and then followed by a bunch of gibberish. Doesn't matter what it is because as soon as the blockchain is reading `OP_RETURN`, it stops, it says, okay, it's valid. And in fact, I'm going to forget it because it is unspendable. That's why it's a nice mechanism. And because it's an output, you're not getting any SegWit discount. You're paying the normal price. If you want to get into weight units - 4 weight units per byte of data - but don't worry about weight units I guess.

Aaron Van Wirdum: 00:10:51

And maybe you're also sort of skipping ahead which makes it more confusing anyways I guess just carry on. So you just explained how `OP_RETURN` works, which is also explained in depth in episode 61.

Sjors Provoost: 00:11:05

Exactly.

Aaron Van Wirdum: 00:11:06

Now my question is about inscriptions.

## How Inscriptions Work

Sjors Provoost: 00:11:08

Exactly. And these are not using outputs, they're using inputs. And an input basically, the goal of an input is to say, okay, here's an output, you just point to a transaction hash and an index in the transaction and here is the piece of script, the witness, that you need to spend that output. Now this witness gets a 4x discount. So what this new scheme does is it basically puts all the `OP_RETURN` like data in the witness instead of in the output. And now we can get into the way it puts it into the witness, doesn't really matter, but the idea is you need to eventually, when you're spending your own coins, you need to provide a signature. But you don't have to do that right away. You can do a bunch of nonsense and then provide a signature. Or you can provide a signature and then continue the script, do a bunch of nonsense and then return. And that's basically what you're doing. So either before or after you provide your signature you write on the blockchain `OP_FALSE` and what that does is it - we talked about bitcoin scripts all the way I think in episode 2 - but it basically puts something on the stack called false. Now stack is like a pile of plates. So you have a pile of plates, which is exactly one high, the word false is on that plate. And then there's the next code is called `OP_IF`. And this `OP_IF` statement looks at what's the top plate, well, false. And then it says, okay, I'm going to skip until either I see an else or I see an end if. And so there is an end if in this particular script and it turns out that between this if statement and the end if statement is where you have all this data that you're trying to upload into the blockchain. And as we just described, the `OP_IF` statement means that we're not executing all that data, we're just skipping past it. So you're able to do whatever you want because it's not evaluated.

Aaron Van Wirdum: 00:13:00

Okay, that was a very technical explanation and I'm gonna try to dumb it down a bit. And then if I dumb it down so much that it becomes inaccurate, you should stop me.


Aaron Van Wirdum: 00:14:09

So I think I would sort of explain it in that, a transaction includes different kinds of data. So most notably, it includes data that says coins are being spent from here, and then other pieces of data says it's being spent to here. But then to prove that the rightful owner is spending it, a signature needs to be added. And the signature is included in yet another part of the transaction, which we call the witness. Yes. And this witness part of the transaction can also include other data. And that's where we're putting this data. So we're putting this data, these images or whatever it is we're uploading, we're putting it in the witness in a way that it's irrelevant for the transaction, but it's still there, right? That's the summary, right?

Sjors Provoost: 00:15:06

Yeah. The witness is providing the signature and it's doing a bunch of blah, blah, blah that is completely ignored.

Aaron Van Wirdum: 00:15:11

Right. So if my Bitcoin node sees one of these transactions, as it has by now, because these transactions now exist, they just see basically a valid transaction, and then they see a bunch, my node sees a bunch of data in the witness, but it just figures that data is completely irrelevant.

Sjors Provoost: 00:15:34

Yeah, because it's between an if and an end if statement.

Aaron Van Wirdum: 00:15:37

I'm not even going to remember it because my node is a prune node, so it forgets blocks older than a couple of days, and it's also not in my UTXO set. So my node after a couple days it doesn't even remember that it was there.

Sjors Provoost: 00:15:50

So if you have a full archival node, so one that keeps all the history, you will remember all this stuff and you have to download it once. But if you have a pruned node, yeah you're gonna toss it as you would with `OP_RETURN` by the way. There's no difference there. And it's not using up any of your RAM, because RAM is only consumed when you create an output. And in this case, you're not creating an output, you're spending an output. So the second the output is spent, you can forget that output ever existed, and the witness never has to be in RAM anyway. Well, except the moment you're checking it.

Aaron Van Wirdum: 00:16:19

Right. So for my node specifically, I think the only cost really was that I had to download it once and then maybe upload it to other...

Sjors Provoost: 00:16:27

Yeah, exactly. 

Aaron Van Wirdum: 00:16:28

That's sort of the cost for me, but That's sort of it, I think. Exactly. Okay. But then if you run a special Bitcoin node, like a inscriptions compatible...

Sjors Provoost: 00:16:39

It's not even a node. You just run a piece of software that talks to your node and that is able to get the inscriptions out of the blockchain.

Aaron Van Wirdum: 00:16:45

Yeah. So that software will see the same data but it will say hey I know what that means. That means... This is whatever and then it is able to subtract an image from the blockchain.

Sjors Provoost: 00:17:01

Yeah so that script will basically ask for every transaction in the blockchain, one by one, and then it will inspect the transaction and look for a certain pattern. And I guess in this case, we'd be looking for an OP CODE called push, followed by the data ORD or something like that. And then it processes whatever comes after that as a file. Which these kinds of tools have existed before for image upload using `OP_RETURN` and using all these other mechanisms. There were also scripts that would basically work in the same way. In fact in my book, now that I'm shilling that, there's an appendix I think it's appendix C which contains the Bitcoin white paper but it also contains instructions of how you can get the Bitcoin white paper PDF out of the Bitcoin blockchain with just one very complicated command.

Aaron Van Wirdum: 00:17:53

Right. Okay, so I think we've now explained... So `OP_RETURN` had this limit of how much data you can upload.

Sjors Provoost: 00:18:03

Mm-hmm.

Aaron Van Wirdum: 00:18:04

So I think we've now explained how Casey essentially got around this limit to otherwise accomplish something very similar.

## What makes Inscriptions possible

Sjors Provoost: 00:18:13

Yeah, though you might wonder why there's no such limit in the witness, right? That could have been.

Aaron Van Wirdum: 00:18:19

Sure, yeah.

Sjors Provoost: 00:18:19

But there isn't. And in fact with SegWit, there were some limits, and with Taproot to the witness size, so it was still much bigger than what you could do with `OP_RETURN`, but with Taproot these limits were lifted even more. And the main reason for that is to make it simpler to interpret a script. Things like miniscript that we've talked about in earlier episodes when you see a script you want to reason about it, what properties does it have? Can I spend it? You might be part of a very complicated multi-sig and you want to make sure that yes I can provide one signature and if somebody else also provides a signature it can be spent and the coins are not lost? And this type of analysis is easier when there are fewer limits in place. So there were good reasons to remove all these limits, but it does mean that you can make a 400 kilobyte image this way.

Aaron Van Wirdum: 00:19:06

So that's the new limit, 400 kilobytes?

Sjors Provoost: 00:19:09

In practice, yes. And this has to do with standardness. So standardness means that this is what nodes will relay by default. But you can take your node and you can edit the software and change that particular limit so that you'll, you'll gossip even transactions with a megabyte or four megabytes actually.

Aaron Van Wirdum: 00:19:25

Four, right? Yeah.

Sjors Provoost: 00:19:26

Yeah. So the real limit is what can be mined. If you contact a miner directly, or you go Peter Todd style, create an alternative client that does not care about this limit and promote this alternative client and then hope that miners will actually just look for it with a big enough bounty, then you can actually produce a full block, 400 megabyte block, with just a giant movie or whatever it is inside of it. And I wonder who will be the first person to do that. I guess Burak.

Aaron Van Wirdum: 00:19:58

Yeah, so you could have a block that consists of one, I guess, almost four megabytes transaction that is actually, like you said...

Sjors Provoost: 00:20:08

Yeah, you have to leave a little bit of space because, the block has to have a header and has to have the Coinbase transaction for the miner and your transaction itself has to have a bunch of overhead, it has to probably send the money somewhere. So don't make it exactly four megabytes, four million bytes, a little bit less, but yeah, you can make it pretty big. And, you can do the same with `OP_RETURN`, but then you can only make it one megabyte. So in that sense, it's four times cheaper. So with `OP_RETURN` if you provided it directly to a miner there's no limit. You can make, as far as I know, a one megabyte or slightly less `OP_RETURN` transaction but for the same cost you can make a four megabyte inscription.

## The SegWit discount that Inscriptions make use of

Aaron Van Wirdum: 00:20:45

Yeah well that was gonna be my next question or the next point I was going to bring up. So we've explained how to get around the `OP_RETURN` limit, so to say. And then the other thing is that inscriptions make use of this SegWit Discount. So we may have explained this in a previous episode, we probably have, or maybe not, I'm not sure, but what does this actually mean? Can you explain what the SegWit Discount is or why people call it that or what is actually what we're talking about.

Sjors Provoost: 00:21:20

So blocks, as far as old nodes are concerned, pre-SegWit nodes are concerned, are one megabyte. And then the question was, how can we... Well, two things were achieved with SegWit. One was to allow all these new features that SegWit allows, and we did an episode about that. But the other was also a block size increase. And the way to increase the block size is to put all this witness data in a special place that old nodes don't see. And so there's three megabytes worth of data in places that old nodes don't see, it's called the witness, or up to three megabytes that old nodes don't see, that's the witness data.

Aaron Van Wirdum: 00:21:55

Well, no, it can be up to four, right?

Sjors Provoost: 00:21:58

The entire block can be up to four. Yeah, so I guess you're right. The witness data can be up to four, but then the main data has to be less, because the total has to be less than four. The witness plus the non-witness data.

Aaron Van Wirdum: 00:22:11

Yeah. Well, I mean, in this case, that's plausible, right? That's what we talked about, the one transaction. 

Sjors Provoost: 00:22:17

So that's where these weight units come in. If you're creating a transaction, a block has to be a maximum of 4 million weight units. And if you're using the non-witness part of a transaction, so the outputs, whatever, each unit counts as, I believe, four weight units. Yeah, so basically if you don't use any witness data, your block size is one million times four. So you're back to one megabyte block for the old nodes. And if you use lots of witness data, then you can have a four megabyte block, which is what you would do here.

Aaron Van Wirdum: 00:22:52

Yeah, so it was basically introduced as a way to get around the block size limit without requiring a hard fork. So to increase blocks without requiring a hard fork.

Sjors Provoost: 00:23:05

Exactly, and also as an incentive to use SegWit, because SegWit is solving some other problems that are very expensive in terms of resources for the computer. So I guess It's a nice way to say, just use SegWit rather than not SegWit.

Aaron Van Wirdum: 00:23:18

Is that also directly UTXO set related? Isn't that the sort of main thing? Because whatever gets into the witness will not end up in the UTXO set. Am I saying that right?

Sjors Provoost: 00:23:29

No, it does. The UTXO set contains... Well, no, the UTXO set doesn't contain any witness data.

Aaron Van Wirdum: 00:23:34

Exactly.

Sjors Provoost: 00:23:34

But I don't think that's the reason. It has to do with if transactions get very large, you have certain things that get quadratically more expensive to evaluate. And I think SegWit removed those limitations Or made it more efficient so that certain transactions when you use SegWit will be less bad on your CPU for example.

Aaron Van Wirdum: 00:23:53

Right. I definitely remember that it was at least one of the arguments or it was claimed that the discount also better aligned incentives. I guess I'm just a bit rusty on why that was exactly. 

Sjors Provoost: 00:24:06

Yeah, I think what you mean there is that it becomes cheaper to spend coins than to create coins. So it used to be, I think it used to be the case that it was cheaper for you to create lots and lots of change and never really spend your original coins unless you were desperate, never combine your coins. And with SegWit, because it's much cheaper now to spend coins, you have some extra incentive to spend your coins. And by spending your coins, you're reducing the UTXO set size, which means you're reducing the amount of RAM used by other people. So in that sense, yes, it creates an incentive to start spending coins.

Aaron Van Wirdum: 00:24:39

Right.

Sjors Provoost: 00:24:40

To start combining coins.

Aaron Van Wirdum: 00:24:42

Okay. Well, in any case, I think the point is that through the witness, blocks can be bigger. So there's a bit more block space. And then if a fee market develops, so if not all transactions fit into blocks, then transactions will have to outbid each other. And if you're using more of the part of the block that's less scarce, then miners are more inclined to include it because they can include more of them. Right? That's how the incentives work. And that's why there's a quote unquote discount on using witness data. So that's why using inscriptions is basically cheaper per byte than using `OP_RETURN`. Yeah. Right? Am I saying it right? I think I'm saying it right. Okay. So then I think we've now explained what inscriptions are and how they work. And maybe we should get a little bit into why it is controversial or why are some people angry about this and or...

## The Controversy around Inscriptions 

Sjors Provoost: 00:25:51

Well I'm not a psychologist but you could you could argue that Bitcoin's primary purpose is to make money basically as a censorship resistant system for money transfer and if you start doing other things with it that other use case might at some point push out the money use case. Now hopefully the fee structure that exists in Bitcoin is enough to make sure that the money use case is always going to be basically able to pay for itself and always outcompete any other system because it is hopefully in the long term insanely expensive to store data on the blockchain and you have to compete if you want to put your JPEG on the blockchain that's fine but you're competing with Michael Saylor that wants to spend a billion dollars and is probably able to pay a much higher fee on that. So that's the hope but because this mechanism gives you a 4x discount compared to using `OP_RETURN`, the dynamics just changed by a factor of four. Essentially, the same dynamics where you have a competing use case is now four times cheaper.

Aaron Van Wirdum: 00:26:49

I think the first thing that may be worth mentioning, and you mentioned it yourself in the `OP_RETURN` episode, is that nodes don't get paid, right? If you're running a note. And so the idea is, or this is one of the arguments, this is why it's controversial, at least in some parts of the Bitcoin world, is that if you're running a note, you're agreeing to process transactions, also the transactions of other people, that's the, the social contract or whatever you want to call it. I think that term is very overused, but that's sort of what you're agreeing to do, But you didn't agree to also process or transmit or store rare peppies. So then if people start doing that, that's abusing the system in a way. That's the argument.

Sjors Provoost: 00:27:48

It's at least abusing the altruism of the nodes in the network that we're not interested in relaying our rare pepes. Now you could say, well, you could just configure your node so it doesn't relay rare pepes. Unfortunately, that gets you into a cat and mouse, well, it's two problems. It gets you into a cat and mouse game of how do you even detect what a rare pepe is. That might be more work than just relaying it, probably.

Aaron Van Wirdum: 00:28:09

Well, you also can't do that. I don't know why you say that. You still have to accept the block, right? 

Sjors Provoost: 00:28:17

The block, yes, but most of the bandwidth is for relaying transactions.

Aaron Van Wirdum: 00:28:21

So okay, that's fair. But in the end, you still have to process it one way or the other.

Sjors Provoost: 00:28:25

Yeah, that's true.

Aaron Van Wirdum: 00:28:26

What was your second point going to be?

Sjors Provoost: 00:28:27

So you end up with this cat and mouse game, you don't know what is what. The second point is and that comes to relaying transactions if you decide to not relay certain transactions your mempool is not going to be accurate which means that when a new block comes in you won't have all the transactions in that block you didn't have to download all these rare pepe's in order to check the block which means you are not propagating blocks very fast, which can create network splits if too many people do that.

Aaron Van Wirdum: 00:28:54

Okay, so that's sort of the main argument against this, but as you mentioned or as you alluded to at least, you can't really do anything about it, right?

Sjors Provoost: 00:29:09

No, from my cursory look at the mailing list, it is replied by Andrew Poelstra, the cryptographer and long-time Bitcoiner.

Aaron Van Wirdum: 00:29:16

I like that you're pronouncing his name in a very Dutch way.

Sjors Provoost: 00:29:18

Yeah, in the correct way. Basically he says, as far as I know, there's no sane way of distinguishing one thing from the other. And if you add any complexity, you end up with a cat and mouse game. And also it makes it more difficult to do complicated transactions that are legitimate because the reason to remove all these limits in Taproot was to make it easier to reason about transactions and then you add a bunch of complicated anti-rare-pepe rules you just throw away all these benefits.

Aaron Van Wirdum: 00:29:46

So the other side of the equation, the argument in favor of stuff like inscriptions is that Bitcoin long-term will need to survive somehow, which means miners need to be mining. They need an incentive to mine and because the subsidy, the block subsidy, is gonna disappear, we need actual fee pressure. So it's good if people want to pay to use Bitcoin, even if it's for other reasons than sending money, just for the viability or the health of the system. That's sort of the other side of the argument, which I personally think I find more compelling. I also want people to use Bitcoin for whatever and let's have the market figure it out. I'm leaning in that direction. I don't know where you are standing on this.

Sjors Provoost: 00:30:44

I mean, On the one hand, I would agree with that argument. On the other hand, whenever you use Bitcoin for things that it's not primarily designed for, the incentives change. And it's hard to reason what the game theory would be under extreme circumstances. Is there a different incentive for a 51% attack now if 99% of the volume is NFTs. But if we go into a low subsidy regime, that's uncharted territory anyway, with or without NFTs. So I don't really know.

Aaron Van Wirdum: 00:31:11

Yeah, I think the important thing to mention maybe as a sort of addendum to my point is that... The way I think about it right now is what's protecting nodes from having to upload and store too much data is the block size limit. That's why the block size limit is there and why it should be there.

Sjors Provoost: 00:31:33

And blocks are already two megabytes right now. And so even if this new thing becomes super popular, blocks might grow to four megabytes. So the problem only gets two times worse. And by only, I mean, it's not exponentially worse. Yeah, two times worse is bad but it's linear. It doesn't get exponentially worse. It's not a million times bad. It's just two times bad. So that's also why I'm not worried about it because any problem that is a problem now, if it gets twice as bad it shouldn't be fatal unless we were already at a very fragile point where a 2x increase of some problem is, which is hopefully not the case. So I'm not super worried about it because it's quite limited in that sense.

Aaron Van Wirdum: 00:32:16

Yeah And then it's sort of an extension of that is if a fee market develops what we want and what we sometimes have it, comes and goes, it seems like, but there is some fee market issue dynamics going on. Anyways, if that continues to develop, I just can't imagine that uploading rare pepes is going to be the most valuable thing. I don't think that's going to win. You can't predict the future. That's right. But I can sort of speculate, right. And I just can't imagine that this is going to be the thing that people will use such a valuable system for.

Sjors Provoost: 00:32:57

It's the most inefficient way possible to upload a file it doesn't give you much more long-term protection than torrents. So there's another downside that I'm a little bit worried about, which is more political than technical, which is that if people start using this to upload bad things, let's just say, Yeah, if bad things have already been uploaded to the blockchain in the past, but it was very incidental so you can very easily argue, well, that's just some weird guy doing something weird and it's not a real problem. But if it starts happening with gigabytes and gigabytes and gigabytes and the FBI gets really annoyed and it starts lobbying Congress, then this could be a stick that's used against having a full node. Yet another argument, you can use Bitcoin, but you have to use an exchange, because if you use a full node, you have all these bad things on your computer and we can't tell if you're just using Bitcoin or you're doing these bad things. And so, it could be another little political push away from self-custody or even a FUD campaign away from self-custody.

Aaron Van Wirdum: 00:33:59

Right. Interesting. Yeah, that's... I haven't thought about this argument, so I'm not going to...

Sjors Provoost: 00:34:05

But that argument is only four times as bad as it was before. Because you can already do these things with `OP_RETURN`, now you can do them four times cheaper. I don't think that's a game-changing fee difference. So it's only about whether this thing even becomes a hype, because it might be that nobody cares about this possibility and nobody uses it.

## Ordinals

Aaron Van Wirdum: 00:34:22

Right. Okay. So we've explained what inscriptions are. I think, I mean, I'm sure there's, more nuance to dive into if you're really interested in that. But I think we've covered the main reason why there's a controversy and the argument for and against. Should we really quickly, before we end this episode, mention the ordinal part of it or how that works or...

Sjors Provoost: 00:34:51

No

Aaron Van Wirdum: 00:34:52

No? Okay yes well I think I'll give you a one sentence explanation right so I think the idea is when you upload an inscription, so when you're uploading the data then I think one of the satoshis in that transaction is the, I mean, it's so dumb. NFTs are so dumb, Sjors. I can't, I have so much trouble. Okay, I should first explain the thing. I just don't understand why people still take this seriously. Let me ask you another question. What's your opinion on NFTs maybe first of all? Because I think it's absurd.

Sjors Provoost: 00:35:37

Yeah, I think NFTs might make sense, but they don't need a blockchain.

Aaron Van Wirdum: 00:35:41

Well, that's why they're absurd. What are people, what are they doing?

Sjors Provoost: 00:35:45

I mean, I could imagine making it, say you are an artist, you can run a little website that, sells tokens representing your art and you can keep track of who owns which token. You don't really need a blockchain for that. 

Aaron Van Wirdum: 00:35:58

But even then you don't own the art, right? You own, what do you own?

Sjors Provoost: 00:36:02

You own- Well, you can do that. If you are the artist, you can make this website and you can put a contract on that website that promises, maybe through some sort of trust construction, that the blockchain really is what legally happens. So you can say that.

Aaron Van Wirdum: 00:36:18

Okay, yeah, fair, you can do that, you don't need a blockchain for that, right.

Sjors Provoost: 00:36:21

You don't need a blockchain for that. So you can say whatever the database said is true. And the nice thing about that is that a judge couldn't reverse transactions, because with the blockchain, you might end up with a situation where... let's say you have a trust that says, okay, whoever has this, this NFT really is the legal owner of this, of the IP of the artwork. And then some guy in North Korea steals the Bitcoin transaction or whatever transaction it is. And then a judge says, this trust may say that, but actually legally speaking, the US government is now the owner of this particular NFT and so that means that now you need to look at the blockchain and all the court records to decide who owns which NFT and you have a mess. Whereas if you have a normal database and the judge says something, then you just change the database. So yeah, I think NFTs are rather pointless with the blockchain.

Aaron Van Wirdum: 00:37:10

Let's take this concrete example before we get into the weeds of all kinds of weird stuff. So now you're uploading a Pepe image into the Bitcoin blockchain. And then by doing that, there's now a satoshi that says you own the Pepe image. And then if I send the Satoshi to you, then you own the Pepe image, but the Pepe image is literally on the blockchain. That's the point. Anyone can download it. So what are we even...

Sjors Provoost: 00:37:38

Well, if you're talking about ownership again...

Aaron Van Wirdum: 00:37:40

Am I taking crazy pills? The rare Pepe is on the blockchain. How do you own it? If you own it, what does it have to do with that?

Sjors Provoost: 00:37:47

Ownership and possession are not the same thing. So I can possess your bicycle and you can go to the police and say, hey, this is my bicycle, I own this bicycle, and then the police will change the possession of the bicycle. Right. So the same goes for NFTs. If somebody draws a rare Pepe, then while they are the artist, they own the copyright. And they can make a contract with you.

Aaron Van Wirdum: 00:38:07

Oh no, I mean I get copyright. But then in that case you would have to actually enforce this stuff with copyright laws?

Sjors Provoost: 00:38:15

Yes.

Aaron Van Wirdum: 00:38:16

Right. But then we're back to why do you need blockchain for that?

Sjors Provoost: 00:38:19

I agree.

Aaron Van Wirdum: 00:38:20

Right, okay. Anyways, I think we're not going to get into ordinals anymore. The idea of ordinals is you have a colored coin that actually refers to the inscription and you can have fun with that if you're into that stuff.

Sjors Provoost: 00:38:33

Exactly. All right, I think we've covered everything. If there's any other thing you may want to Google, Google `MAX_STANDARD_TX_WEIGHT` because that's the real limit that applies here. And I'm looking forward to see the first 4MB Bitcoin transaction with a picture of... I don't care... Somebody. And thank you for listening to Bitcoin

Aaron Van Wirdum: 00:38:45

Explained.

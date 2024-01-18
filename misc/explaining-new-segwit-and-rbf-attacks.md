---
title: "Explaining New Segwit and RBF Attacks"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=B9vazPgqPNs
tags: ['rbf', 'attacks']
speakers: ['Sjors Provoost', 'Aaron Van Wirdum']
categories: ['podcast']
date: 2020-07-08
---
Speaker 0: 00:00:04

Life from Utrecht, this is the Van Wittem Shorsnado.
Hello.

Speaker 1: 00:00:09

Wee, wee, wee, wee, wee.

Speaker 0: 00:00:12

That's my impression of a tornado warning.

Speaker 1: 00:00:14

Oh, Okay.

Speaker 0: 00:00:15

That's probably how they sound, right?

Speaker 1: 00:00:17

I don't know.
I've never heard one.

Speaker 0: 00:00:18

Me neither.
Shors, we're gonna make a podcast.
Yes.
I suggest, since this is our first episode, we first introduce ourselves.

Speaker 1: 00:00:27

Sure.

Speaker 0: 00:00:27

Who are you, Shors?

Speaker 1: 00:00:28

I'm Shors.
I work on Bitcoin Core and other hobbies.
I live in Utrecht, as do you.

Speaker 0: 00:00:37

Yep, I'm Aron van Wittem.
I'm the technical editor at Bitcoin Magazine.
And what we're going to do basically is discuss technical news, technical stuff, Bitcoin-related technical stuff.
Yes.
Correct?

Speaker 1: 00:00:52

Sounds right.

Speaker 0: 00:00:54

I think we can just start then.
Alright.
So we got two topics this episode, see how that goes.
First topic is the, well there wasn't apparently an official name for it or if there was we couldn't find it, but the fee burning bug.

Speaker 1: 00:01:09

Yeah, we call

Speaker 0: 00:01:09

it

Speaker 1: 00:01:09

the fee burning bug.
That's how

Speaker 0: 00:01:10

we're calling it right?
Yeah.
So there was a big issue with hardware wallets in particular.
It is a bit windy here which is fitting for our name.

Speaker 1: 00:01:21

Exactly.
I'm trying to keep the wind from the microphone.

Speaker 0: 00:01:25

So there was a big issue which related to hardware wallets specifically I think.
A new bug or at least sort of new and the problem was that an unknowing victim could pay could overpay in fees and therefore lose money right that's synopsis of it okay so let's start from the beginning what is this bug how does it how does it happen

Speaker 1: 00:01:49

well We can go back a little bit further in history to talk about a similar bug, which people thought was completely fixed, but it wasn't.
So if you have a Bitcoin transaction, it has a bunch of inputs that you're spending from and it has a bunch of outputs that you're spending to.

Speaker 0: 00:02:06

Yeah, so the inputs are basically the addresses, your addresses that you're sending the coins from and the outputs refer to the addresses that they're going to, right?

Speaker 1: 00:02:13

Yeah, assuming Luke Dasher isn't listening to that first part, what you said, but basically.
Right.

Speaker 0: 00:02:20

I'm simplifying a bit.
That's sort of my job, right?

Speaker 1: 00:02:23

But one thing that, you know, if you use a wallet, you'll see in a transaction is a fee but actually if you look at the transaction on the blockchain this there's no such thing as a fee in the transaction.
It's just that it's just a difference between the inputs and the outputs.

Speaker 0: 00:02:36

Yeah, so there's more coins going into the transaction than coming out of the transaction, essentially, and that difference is something the miner can claim as a fee.

Speaker 1: 00:02:44

And The other thing is that a transaction output will say the amount.
So the transaction output might say, here's one BTC, but an input does not.
An input just says, take this previous transaction and spend it.
And it's up to you, again, to figure out how much that was, Because it would be a waste of space to put the amount in the blockchain twice.
So, here's the problem.

Speaker 0: 00:03:06

The amount was already in the blockchain from the previous transaction.
You're just spending the coins from that transaction and the only thing you really need to know is the new amount.
Because then the difference, you can just look at a previous transaction usually at least.

Speaker 1: 00:03:19

Yeah, and so when you make a new transaction, you, when you have a wallet, say the Bitcoin Core wallet, you enter a destination and an amount and then what it's going to do is it's going to look for coins, those are inputs basically, that add up to at least the amount you need to spend.
And then it adds a change to go back to you.
And that's fine because you're doing all the work and your wallet can check it.
But now let's say you want to be safe and you want to put your private keys not on your computer but you want to put them on a hardware wallet.
Now what happens is your computer produces a transaction without a signature, gives it to the hardware wallet and says go and sign this thing please.
Now the hardware wallet will look at it and say okay these are the outputs I can read that but what about those inputs I know nothing about them and then

Speaker 0: 00:04:10

the hardware wallet has no idea about the inputs because the hardware wallet has no idea about the blockchain overall.

Speaker 1: 00:04:15

Exactly unless you tell it about

Speaker 0: 00:04:17

it.
Right.

Speaker 1: 00:04:18

So let's say you just lied to the hardware wallet and say, look, you're spending these two inputs, they're just half a bitcoin, and there's almost no fee on this thing.
Now, the hardware wallet has no way to check that.
It used to have no way to check that.
And so it would just sign the transaction.
And then, oops, turns out you spent one bitcoin in fees.
That's quite annoying.
And maybe some malware on your computer was doing that to you.
So the solution to that is that you give the hardware wallet everything it needs to check.

Speaker 0: 00:04:55

The reason you would overpay in fees in that scenario is because there would actually be more coins in your inputs than you're telling your hardware wallet.

Speaker 1: 00:05:05

Exactly.
So you might think you're spending half a Bitcoin, but actually the coins that you're spending are worth one Bitcoin.
Right.
And the hardware wallet just didn't know that because you lied to the hardware wallet.

Speaker 0: 00:05:14

The hardware wallet can't tell the difference, so it will just sign whatever.
Yes.
So that's a problem.
Yes.
You don't want that.

Speaker 1: 00:05:19

But the signature describes...
So you're signing a message, essentially, and the message is the transaction.
And the transaction, or part of the transaction, and the transaction contains the inputs that you're spending, namely the transaction hash and the position in that previous transaction.
And so now you could give the hardware wallet the actual transaction that you're spending from.

Speaker 0: 00:05:43

The previous transaction.

Speaker 1: 00:05:44

Yes, Exactly.
And that previous transaction, you can look at it and you can check the hash and you can check that the hash matches what's in the input and you can see what the output amounts are.
So now you know that you're probably spending an actual transaction that wasn't mess with and you can check the amount yourself.
So that's basically how it worked.
So you would just give the hardware wallet all the inputs.
And that's fine if it's small, but maybe you're spending from a giant exchange payout, multiple kilobyte transaction, And you maybe don't have a USB connection, but you are sending it through a QR code, so space could be an issue.

Speaker 0: 00:06:23

A hardware wallet is basically a very weak computer,

Speaker 1: 00:06:26

and

Speaker 0: 00:06:26

then you have to load all that information into the very weak computer, and it's a hassle, and it can take a lot of time if it's a big transaction,

Speaker 1: 00:06:33

or

Speaker 0: 00:06:33

a lot of them, so that's not ideal for hardware wallets.

Speaker 1: 00:06:36

Yeah, some of them are really, really slow.
They're using chips that were designed in the Dark Ages,

Speaker 0: 00:06:42

basically.
Yeah, it's not really made for this type of stuff.

Speaker 1: 00:06:45

No, absolutely not.
Anyhow, so in came SegWit and the idea was to say, okay, let's have the signature of the transaction not just cover what coin you're spending, so not just the transaction hash and the input number, but also the amount that you're spending.
And then the idea is that if you sign something, you actually add the amount before you sign it.
And then if somebody lied about the amount, well, then your transaction is just going to be invalid on the blockchain.
So the hardware wallet will just sign it, because it just sees an amount and it says okay whatever, I haven't checked that amount because I haven't looked at the previous transaction, but I'm going to sign it anyway because if the amount is wrong it's going to be invalid, so I don't really care.
Right.
And that's where the attack comes in that was discussed.
And it wasn't unknown, it just was considered a little bit contrived.
But here's what happened.
Let's say you give a wallet, a transaction has two inputs.
And one of them is half a Bitcoin and the other is half a Bitcoin.
But you're actually going to lie, your computer is going to lie to your hardware wallet and say well the first one is half a bitcoin and the second one is just 0.01 bitcoin, don't worry about it.

Speaker 0: 00:08:10

Yes so to be clear the reason your computer would be lying to your hardware wallet is because your computer was compromised.
Yes.
So right the idea behind hardware wallets sort of is that even if your computer is compromised you should be fine, but in this case...

Speaker 1: 00:08:23

Well that's one way to look at hardware wallets, yeah.

Speaker 0: 00:08:26

There's some, there's still some attack factors of which is one and There are others, but...

Speaker 1: 00:08:30

Yeah, if your computer is compromised, you have a very serious problem.
But let's say somehow the problem is limited to just this little thing that's going to happen now.

Speaker 0: 00:08:38

Right, so then your computer is lying to your hardware wallet.
So what's the lie?

Speaker 1: 00:08:42

The lie is, here's a transaction with two inputs, and I'm going to tell you the truth about the first input, and you're going to lie about the second one.
And then you're going to sign it, and you're going to sign both inputs, and you're going to trust the amounts that you get from the computer.
And now, if you were to broadcast that one, that transaction, it would be invalid, because The blockchain would look at the first input and it would say, yeah, that's valid.
And it would look at the second input and say, no, no, no, that's not 0.01 Bitcoin, that's 0.5 Bitcoin.
So I'm not going to do anything with the transaction.
But here's the problem.
What if you send the hardware wallet another transaction, which is the opposite, where the first input is a lie and the second input is actually true and now the hardware wallet will diligently sign that one.
Now you can actually combine the first and the second transaction because you can just combine take the input from one put it on to the other.

Speaker 0: 00:09:33

Yeah so there's two transactions with two inputs, both are really yours.
However, your computer is lying to your hardware wallet twice, telling you only one of them is yours.

Speaker 1: 00:09:46

Exactly.

Speaker 0: 00:09:46

The opposite one in both cases.
Yeah.
So, both times the outcome is an invalid transaction because the input you're being lied about doesn't match what's happening on the blockchain.
However, with the two invalid transactions, you can both times take the valid one, an attacker can both times take the valid half, combine these, and then all of a sudden have a valid transaction.

Speaker 1: 00:10:10

Yes.

Speaker 0: 00:10:10

So that's how you're circumventing the amount restriction.

Speaker 1: 00:10:13

Yeah, and now the question is how would this line take place?
Well, it would just tell you, after you sign the first one, it would say, hey, there's a problem, please try again.
And it would show the other one.
And so that's a very mean trick.
So then the question is, how do you solve that problem?
Well, you go back to basically what we had before.
You just give it the inputs.
Because now the hardware wallet sees the actual input transactions and can calculate the hash and say, hey, the amounts are up.

Speaker 0: 00:10:45

Just to be clear about the problem before we move on to the new solution.
The problem here is that, in theory at least, because we used a very simplified example here with two transactions and half both times, but essentially if you really pull this attack to the limits you can drain someone's hyperwalls completely just with one transaction right?

Speaker 1: 00:11:08

Yeah, I

Speaker 0: 00:11:08

can do it three times.
All inputs just become a huge fee and it's all paid as a huge fee and you know it kind of disappears into the blockchain to the miners somewhere.
Yeah.
So the only way to benefit from this attack is if you are a miner, correct?
Like you need to be a miner because that's the only way you can get the fee.

Speaker 1: 00:11:29

Maybe or maybe you can blackmail somebody and saying like okay now I have this transaction right but I won't send it to the blockchain just yet

Speaker 0: 00:11:37

you better pay me X amount or I'll broadcast this to the network and you'll lose your money.

Speaker 1: 00:11:41

Yeah exactly something like that.
So you never know and in general there's something called defense in depth So just because you cannot think of a way that this could go wrong, you still want to deal with it.

Speaker 0: 00:11:54

Yeah, it's a weakness you want to take care of.
Yeah.
Okay, so the solution.

Speaker 1: 00:11:59

Well, the solution is, we're back to the old story, where you have to give all the inputs, all the input transactions so you can perform

Speaker 0: 00:12:07

the check.
You have to provide the previous transaction, select before.

Speaker 1: 00:12:10

Yeah.
Now there is a difference between this and the past.
In the past, before SegWit, you could fool a wallet with just a single attempt.
There was no need to ask would you like to try again, because you could just lie about the entire transaction.
And right now you have to do this weird trick where you tell the user, oh something went wrong, please sign again.
Right.
And so, you know, things weren't as bad as they were before, but with this, you know, the way Mozart or Wallace have fixed this, or at least some have fixed this, we're kind of back in the old situation where you just need to give it the inputs.

Speaker 0: 00:12:43

Yeah.
So we solved the problem, but then it turned out it wasn't really solved it was just made a little bit harder to abuse and then to solve it again we're sort of back to the original situation

Speaker 1: 00:12:54

yes

Speaker 0: 00:12:55

all right so now there was some I don't know controversy is the right word but there was some

Speaker 1: 00:13:01

but We can first talk about the even better solution.

Speaker 0: 00:13:05

Okay, go on.

Speaker 1: 00:13:07

So there is a new proposal called Taproot, which I'm sure we'll talk about in another episode.
And part of what Taproot will do is for every input you have to sign the amount not just of that input but also all the other inputs and so yeah you can't lie about one input but not lie about the other input.

Speaker 0: 00:13:25

I see.

Speaker 1: 00:13:26

And I think it's not just the amount it's a whole bunch of things you're signing for about that previous transaction so you really don't have to provide it anymore.

Speaker 0: 00:13:32

So with that approach you'd sign way more information about this transaction in general?

Speaker 1: 00:13:37

Yes.
I mean in general with transaction signing it's kind of a weird concept because the signature is in the transaction so how does that work?
You can't sign before you have the signature So what you do before you sign the transaction is where the signature goes you put a dotted line so to speak and you sign everything or you sign some parts of it and you can change that scheme a little bit, add a little bit more to it or remove things from it.
So that's what Taproot plans to do.

Speaker 0: 00:14:03

Yeah, but right now, I guess we're sort of drifting in a different topic now, but that's fine by me.
So right now you indicate which part of the transaction you're going to sign, right?
With the SIGHASH flag?
Yes.
So would Taproot actually make that less flexible then?

Speaker 1: 00:14:21

No, I think it just changes the meaning.
So SIGHASH ALL is what most transactions use, which is pretty much signing everything about the transaction.
And I think, so what Segwit added is you're not just signing the content of your own transaction, you're also signing something about the inputs, namely the amount.
And so what Tapro changes would be to sign not just the amount of the previous transaction, but a bunch of other things.
Probably the script as well, I haven't read it.

Speaker 0: 00:14:48

And was this done to solve this specific problem, or are there other problems it solves?

Speaker 1: 00:14:53

Maybe.
So that comes into why did this thing become an issue again, because this was known since 2017.
And so I'm not sure whether this problem was brought up again on the mailing list.
And this Taproot solution was brought up on the mailing list.
And so my theory is that bringing up the solution for Taproot reminded people of the original problem.
Made other people look at that original problem and not agree that it's innocent.
Like, they would feel more strongly about it.

Speaker 0: 00:15:23

Yeah, because this issue isn't new in itself.
Like, it was, like you said, it was around for years.
So you think it was just rediscovered?

Speaker 1: 00:15:33

Yeah, it was either rediscovered or it was noticed.
Like if somebody proposes this solution, and you think, hey, what are you actually solving?
Oh, I didn't know about that problem.
So something like that might have happened.
But I'm sure you can look it up in the archives.
Now, it should be noted that if you can trick a user to sign twice, you can also just make them send different funds.
So, even with this fix, If I can trick the hardware wallet into signing again, I can just make them sign as many transactions as I want.
But I can't lie about the amounts of each of those transactions.
But you can still drain somebody's wallet.
You say, Try again.
Why don't you try again?
And then you cannot rank up the fees.
You would just have them pay you twice or pay somebody else twice.
So perhaps that's less useful as an attack.

Speaker 0: 00:16:29

If you

Speaker 1: 00:16:29

can't lie about anything, then you're sending money to an exchange and now you're sending it to the exchange twice.
Well, if it's not the exchange that's trying to scam you, but some random malware, the malware doesn't really have any benefit from you sending to the exchange twice.
So it's perhaps a less useful attack.

Speaker 0: 00:16:49

Right, but it would be sending different coins.
Yes,

Speaker 1: 00:16:52

you would just have a brand new transaction, new inputs, different change address maybe even.
But your hardware wallet only says would you like to send this much to this address?
And if it says that twice, you might just click OK twice.
You don't even think about it.

Speaker 0: 00:17:07

Yeah, yeah.
Right, I see.
So there was some incompatibility with some wallets after the upgrade, right?

Speaker 1: 00:17:16

Yes.
Especially BTC Pay Server.
They have a way to receive money on hardware wallets.
That's not affected, but they also have a way to then send money from your hardware wallet using BTC Pay Server.
And the problem is, if you need to provide the actual input transactions, you need to still have those input transactions and BTC based server doesn't have them.
So it would have to basically, those transactions are sitting somewhere in the blockchain and BTC based server at the moment doesn't have a way to just go in and get an arbitrary transaction from the blockchain.

Speaker 0: 00:17:46

Right.

Speaker 1: 00:17:46

But not all wallets have that problem.
For example, the Bitcoin Core wallet, I believe it keeps the transactions that it cares about inside the wallet itself.
Even if it's pruned.
Exactly.
And web-based wallets, they will just ask the server to please give that transaction?
Sure.

Speaker 0: 00:18:04

So it's mainly a problem for prunes types of wallets because they need previous transactions which they don't have in order.

Speaker 1: 00:18:10

Yeah I would say it's a problem for not wallets basically So that aren't used to holding on to information.
They just try to serve the wallet, sign things on the fly.
Like key managers, but they don't hold on to transactions.
Maybe.
It's not fundamentally unsolvable.
But it is, I can imagine it's painful.

Speaker 0: 00:18:30

It's unsolved at least.

Speaker 1: 00:18:31

Yeah, I mean, at least for BTC Pay Server.

Speaker 0: 00:18:33

There's no solution ready yet.

Speaker 1: 00:18:35

At least not for BTC Pay Server.

Speaker 0: 00:18:37

Right.
But in principle

Speaker 1: 00:18:39

it could be fixable because if BTC Pay Server uses Bitcoin Core indirectly and Bitcoin Core has a transaction index turned on, it'll just work.
Or if you store the block height that also helps.

Speaker 0: 00:18:52

So do you think the fix was worth it?

Speaker 1: 00:18:55

I don't know.

Speaker 0: 00:18:57

What's your opinion Sjoerd?

Speaker 1: 00:18:58

The problem is slightly overrated But you know it's other people's money too.
And so you know the problem of course is if you're using a hardware wallet, and you don't like this choice But you've upgraded the hardware wallet.
You're kind of screwed, but not really because at least with Trezor you can downgrade it.

Speaker 0: 00:19:16

Oh, yeah,

Speaker 1: 00:19:16

if you don't like the solution

Speaker 0: 00:19:17

right of course

Speaker 1: 00:19:18

you know you don't get any of the other fixes.
In fact it's open source so you can even just take their latest firmware release and undo that one change.

Speaker 0: 00:19:26

Right.
And

Speaker 1: 00:19:26

maybe they could add a setting where you can turn it off if you want to.

Speaker 0: 00:19:29

Yeah.
Or you can just not upgrade of course.

Speaker 1: 00:19:32

But you know if you were using Trezor with Bitcoin Core and HWI, that's all still experimental, but that would break until the new version of Bitcoin Core, which compensates for this change.
So, It's not the end of the world.

Speaker 0: 00:19:46

The upcoming version for Bitcoin Core will have a fix for this included.

Speaker 1: 00:19:49

Yes, at least if it gets merged, but I think so.
So that's either 0.21, which comes out November-ish, or 0.20.1, which just comes out randomly.

Speaker 0: 00:20:00

Yeah.
Alright, anything else on

Speaker 1: 00:20:03

this topic?
There's one other way that you could deal with this problem as a hardware wallet, which is to remember the inputs you've already signed and warn the user, hey, wait a minute, I've seen this input before, but that requires memory on the device.
But maybe if you only remember the last ten inputs that you signed maybe it's not too bad it depends on how much memory device has some very little

Speaker 0: 00:20:29

yeah you mean a hardware was right yeah so our bubble would have to remember transactions

Speaker 1: 00:20:33

Would have to remember some of the recent inputs they've signed and say, hey, you've signed this before, are you sure you want this?
Right.
And by the way, the amount changed.

Speaker 0: 00:20:43

Yeah, so that would require more memory.

Speaker 1: 00:20:46

Perhaps, or at least it requires another software change.
It might be a way to fool the hardware wallet with that kind of thing, so it's more complexity.
Alright Sjors,

Speaker 0: 00:20:55

you want to move on to the next topic?

Speaker 1: 00:20:57

Yes, let's talk about our favorite topic.

Speaker 0: 00:21:00

Rbf.
Replaced by fee.
Rbf.
There was a news blitz in the crypto media this week about Rbf and how there was a vulnerability, major weakness.
Bitcoin was hacked.
Yes, Bitcoin was hacked.
That's what we all read.

Speaker 1: 00:21:18

Completely destroyed, miners despised, what's to come, end of the world.

Speaker 0: 00:21:23

There were news stories about RBF, so let's get into what was this news story about.
Or maybe we should start with RBF.
Let's start with RBF, what is RBF, what is ReplaceWake?

Speaker 1: 00:21:33

So basically, when you create a transaction, you don't put it in the blockchain.
That's not how that goes.
You actually send it to other Bitcoin nodes, and they send it to other Bitcoin nodes, and everybody sends it to each other in a happy circle and eventually a miner puts your transaction in a

Speaker 0: 00:21:51

block.
Hopefully.

Speaker 1: 00:21:53

Yeah or not and then it's but and then it's confirmed.
Now the reason why they might want to do that it's not just because they're nice it's because they want to make money from the fees.

Speaker 0: 00:22:03

Most of them are nice though, aren't they?

Speaker 1: 00:22:04

Yeah, I would say so, because in the beginning transactions paid very little fees, pretty much not worth the electricity.
True, for the first couple

Speaker 0: 00:22:12

of years, yes.

Speaker 1: 00:22:13

So yes, miners also have some incentive to keep the network useful, but ultimately it's nice if you pay them.
And the other thing is, let's say you have a lot of transactions and they're competing for space and a block is full, or it's not full, but basically the miner has more transactions to choose from than he can fit in the block, what do you do?
Well, if transactions pay fees, you just start with the highest fee and you work your way down.
It's a little bit more complicated than that, because transactions might depend on each other, but basically that's the rational thing to do.
Take the highest paying transactions, put them in the block, and leave the rest out.

Speaker 0: 00:22:51

Yeah, it's a bidding war between transactions in that case.

Speaker 1: 00:22:54

Well, yeah, but the bidding is just one bid.
Right.
So then the question is, can we make that a little bit smarter?
And so you might think, it's a very quiet day, I'm going to pay the absolute minimum fee, one satoshi per byte, and I'm going to send that transaction around.
And then all of a sudden, I don't know, BitMEX pays its daily user base and the mempool is full or it's busy and actually your transaction is not going to confirm for hours and hours and you're like, oh, okay, what am I gonna do?
You increase the fee.
Now, this is always possible.
It's always possible to increase the fee and to send it to other peers and to give it to a miner.
And then they may or may not...

Speaker 0: 00:23:38

Well, to be technically accurate, what you're really doing is creating a new transaction, spending the same coins to the same addresses, but with a higher fee this time.
Exactly.
Basically, right?

Speaker 1: 00:23:47

Yes.
You're creating a new transaction that spends the same points.

Speaker 0: 00:23:51

So it sort of overwrites your previous transaction.

Speaker 1: 00:23:53

Well, it's different than your previous transaction.
And now the question is, why would other nodes in Minus care about that?
Now, other nodes might not care about it at all.
And so initially, I think the default was that they would just ignore it.
Because for them, other nodes, there's nothing in it to relay your transaction.
It's just using their bandwidth.
So they're not gonna do that.
But you could send it directly to a miner, and the miner might look at this and say, well, this new transaction you're sending me pays me more than the other thing I had, so I'll happily replace that and put that in the block.

Speaker 0: 00:24:25

Right.
And

Speaker 1: 00:24:25

so if you can reach the miner in time, it'll get replaced.
And in this case, of course, because the mempool is very busy, you have plenty of time to do this.
But there was no official mechanism for that, and so some people would do that and other people would not, but generally, most of the time, it wouldn't be done, and so people kind of started trusting, okay, if I send a transaction it's probably not going to get replaced by something else so I can just accept it.
Okay, but eventually a mechanism was introduced to formally ask for a fee raise, essentially, to ask nicely, hey, this transaction has a higher fee, please replace it.
And then other nodes, if you use that scheme, would do that for you.
And you would indicate in advance, okay, if this transaction is, If I offer a higher fee, then you should relay the higher one.

Speaker 0: 00:25:17

Right.
So then nodes will accept a new transaction and forward it for miners to ultimately take it and replace the previous one.

Speaker 1: 00:25:25

And there were some rules there, for example, the fee has to be substantially higher than the previous one, and so that way you're kind of disincentivizing, dossing all your peers.
And then all the peers would relay it, even though it's still not there yet.

Speaker 0: 00:25:41

How much higher does it need to go?

Speaker 1: 00:25:43

Just one satoshi per byte.
No, I think the minimum relay fee.
So if the mempool is empty or not busy, then that's just one satoshi per byte.
But if there's a lot of transactions in there, and say the minimum transaction fee is 100 satoshi per byte, if you then want to rip it, If you then want to bump the fee, you'd have to bump it with another 100 Satoshi per byte.
I see.
I think.
Or it's, I don't know.

Speaker 0: 00:26:08

So that's a big difference.

Speaker 1: 00:26:08

At least 100 Satoshi per byte.
I think it depends on how busy the mempool is.
Right.
You have to look it up.
Okay.
Anyway, so it's just a way to coordinate this fee bumping thing, but fundamentally a miner can do whatever they want.
They don't have to care about this RBF flag being present or not.
There's a lot of debate about whether you should make this deliberately unsafe to discourage people to not accept unconfirmed transactions.
It gets a little political or practical.
In practice how high is this risk?
Some businesses are happy to accept unconfirmed transactions for small amounts because they realize that it doesn't happen, it doesn't go wrong that often or they have other fraud detection mechanisms to keep them safe.
So, but anyway.

Speaker 0: 00:26:56

Well, and on the plus side I would say it makes the fee market operate way more smoothly.

Speaker 1: 00:27:02

Yeah, but the concept of raising fees in general is good for the fee market.
Using the specific mechanism of RBF is just one way to do that, that people happen to have agreed upon.
Like this is the way to signal it, and these are the rules.
Rather than just say, everybody for themselves, you decide when you accept a new transaction or not with a higher fee.

Speaker 0: 00:27:23

Yes, but by adding flags like this and tricks like this it you know it allows the fee market to be more efficient or at least you know as a user I can start with a lower bid, and only if I see it's not enough I can start to increase my bid, as opposed to having to go gung-ho on the first bid and lose money unnecessarily to miners.

Speaker 1: 00:27:46

But now the problem is, let's say your wallet is receiving such a transaction.
And now the question is, what do you do?
What do you show the user?
So usually your wallet receives a transaction and says, well this transaction is unconfirmed.
Then when it's replaced with a different transaction, well then you just show the other transaction and say it's unconfirmed.
But maybe you want to have a more consistent, like it might look a little weird for a transaction to disappear and to reappear, or even for two transactions to appear.
So maybe you want to make that UI

Speaker 0: 00:28:20

a little

Speaker 1: 00:28:20

bit nicer, but it gets complicated quickly.
And one of the things that you can change about a transaction is you can bump the fee, but you can also completely change the destination.
As far as I know, there's no rule against that.
So one moment, you think you've received a transaction, and then the fee is bumped, and you're not receiving that transaction anymore it goes to somebody else.
So your wallet needs to be smart enough to realize that, say okay wait a minute this is no longer going to me, it's going somewhere else.
Another complexity is that somebody might send a transaction with a higher fee, but a block is mined and that transaction with a higher fee reached you just in time for your wallet to see it But then it sees the new block and it goes away again So the experience can be quite confusing depending on the timing depending on who relays what fee increase all that sort of stuff And it's possible to make mistakes in that.
And that's what happened.
And that's why the internet is on fire and Bitcoin is, you know, it's all being sold to Peter Schiff for one dollar.

Speaker 0: 00:29:27

So what's the mistake?
It's a wallet problem.
Yes.
Wallets are just not showing unconfirmed transactions as unconfirmed transactions?

Speaker 1: 00:29:36

No, I think one problem that was described as one wallet might have been the Ledger desktop wallet.

Speaker 0: 00:29:42

Yeah, Ledger Live I think.

Speaker 1: 00:29:43

Yeah, that was pretty much doing what I just described.
It would show a transaction, unconfirmed transaction, to you it would increase your balance, saying, okay, you've already got more.
But then if somebody changed the destination, it would not lower the balance again.
So you would see the wrong balance.

Speaker 0: 00:30:02

Right.

Speaker 1: 00:30:02

And I think even if a transaction then confirms,

Speaker 0: 00:30:04

That sounds very sloppy.
People wouldn't

Speaker 1: 00:30:05

forget about it.
So that's a bug.
Yeah.
At least.
Yes.
And, you know, they should fix that because it can, you know, cause problems for their users.
And the other problem sort of related to that is if your wallet can spend from an unconfirmed, if your wallet can spend an unconfirmed transaction, your wallet has to choose a bunch of coins to spend, a bunch of inputs to spend.
And the question is which inputs is it going to pick?
And maybe it does it randomly.
But now let's say it also includes unconfirmed transactions, and it's completely random.
And now for some reason, you have a million unconfirmed transactions because of all these RBF bumps.

Speaker 0: 00:30:44

You

Speaker 1: 00:30:44

keep picking these unconfirmed pieces to compose your transaction.

Speaker 0: 00:30:48

And the reason it could possibly be a million is because once someone has your address, they can just keep sending you transactions which they then replace.
So, you know, it's possible that this could happen to your wallet.

Speaker 1: 00:31:01

Yeah, and one transaction could contain, you know, I don't know, hundreds of outputs that all go to the same address.

Speaker 0: 00:31:07

Right.

Speaker 1: 00:31:07

And then with a slightly different amount and then you keep replacing the transaction with a transaction that has the same outputs but with slightly different amounts.

Speaker 0: 00:31:14

Right.

Speaker 1: 00:31:14

Or different outputs altogether and you could keep doing that and your wallet would just be totally confused.
So that's a way to sort of DOS a wallet.
It seems a bit of a far-fetched attack to do, but it's possible and there might be an economic reason to do it.
So again, defense in depth, you just want to deal with that.
But one way to deal with it is the way VidConCore does it, which is a lazy approach perhaps, but very robust against it.
You cannot spend unconfirmed transactions, period.
You just have to wait for confirmation.
So there might be some noise.
I think VidConCore even shows all the different versions of an RBF transaction in a row like they're separate transactions.
So I'm not saying it's the best UI ever, but you can't spend it until it's confirmed.
So it's not really bothered by this particular attack.
But I'm sure there's other ways to fix it too.
Anyway, this was presented as a complete drama.
And I think it was marketing for a new wallet.

Speaker 0: 00:32:15

It seemed to me like this was an issue between wallet developers, like, hey guys, look, there's something you need to fix, we found a bug in your wallet.
And like that's it, there was no news value to it other than we found a bug in your wallet.
It was presented as if it was a big problem with Bitcoin itself as if someone figured out how to double spin Bitcoin.
But that's not...

Speaker 1: 00:32:35

I think, well, I'm not sure who did that because there's also just the news media, like the CoinDesk, that needs to sell clicks and I think they also just made a bit of a mess of the article.

Speaker 0: 00:32:49

Maybe, maybe, but I'd be curious to see the press release that was sent to them, because I've seen press releases where, you know, they try to make it sound dramatic as well, in order to get a journalist to write about it.

Speaker 1: 00:33:02

The blog post published by this wallet was very sensational and quite ridiculous, but I don't think they were claiming Bitcoin was broken, I think it was just claiming that these other wallets were broken.
Right.
But you know, by the time this reaches CNN, Bitcoin is broken, and That's how that goes.

Speaker 0: 00:33:18

Yes, that's how it works.

Speaker 1: 00:33:19

But the thing is, security vulnerabilities, I'm very happy that more and more companies are taking security work seriously, Google Zero, etc.
They're doing a lot of very important security work.
But they're also using it as a marketing tool.
And at some point when the marketeers start to get a little bit too dominant, they have an incentive to make a problem sound way worse than it is.
Sometimes bounty Systems also make that the case because you get more for severe bounties.
So you just make it sound very severe.

Speaker 0: 00:33:50

Mm-hmm

Speaker 1: 00:33:52

So that incentive sometimes gets out of hand and people just start making a lot of noise about something That's probably not not that bad just to get more clicks.

Speaker 0: 00:34:00

Yeah,

Speaker 1: 00:34:02

I mean it keeps everybody sharp but at the same time if there really is a bug that is really severe, like I don't know an inflation bug, then there has to be some language left to describe something that is actually severe and could actually hurt people very very badly.

Speaker 0: 00:34:19

So was this bug fixed?

Speaker 1: 00:34:21

I don't know I'm guessing that they'll they release a fix I mean the legend was auto updates or at least you can you can click to update it So it's

Speaker 0: 00:34:30

fairly sure that at least for some of the walls it was fixed I don't remember which one fixed it exactly and which one didn't get so some of them fixed

Speaker 1: 00:34:37

it It sounds to me mostly a denial of service attack, which is a problem But it's not it's not necessarily gonna steal your coins.

Speaker 0: 00:34:45

Yeah All right, so Bitcoin is still alive.

Speaker 1: 00:34:50

I don't know.

Speaker 0: 00:34:50

I think so.

Speaker 1: 00:34:51

Yeah.

Speaker 0: 00:34:52

Last I checked it was

Speaker 1: 00:34:53

running.
Alright.

Speaker 0: 00:34:55

Good right?
Yeah.
Anything else?

Speaker 1: 00:34:57

No I think that's it.

Speaker 0: 00:34:59

That was it.
Oh we needed a closing sentence as well.

Speaker 1: 00:35:02

Thank you for listening to the Van Weerdum Shores NATO.

Speaker 0: 00:35:06

There you go.

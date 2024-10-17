---
title: Silent Payments
transcript_by: tijuan1 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=42PMLaz7Avk
tags:
  - silent-payments
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
  - Ruben Somsen
date: 2022-06-09
episode: 58
summary: |-
  In this episode of Bitcoin, Explained, hosts Aaron van Wirdum and Sjors Provoost welcome Ruben Somsen back on the show to talk about a recent proposal of his called “Silent Payments”.

  Silent Payments resemble earlier ideas like Stealth Addresses and Reusable Payment Codes, in that they allow users to publish a static “address”, while this is not the actual Bitcoin address they will be paid on. Instead, senders of a transaction can use this static address to generate new Bitcoin addresses for the recipient, for which the recipient — and only the recipient — can in turn generate the corresponding private keys.

  Like Stealth Addresses and Reusable Payment Codes, the benefit of Silent Payments is that addresses can be posted publicly without harming users’ privacy; snoops cannot link the publicly posted address to the actual Bitcoin addresses that the recipient is paid on. Meanwhile, unlike Stealth Addresses and Reusable Payment Codes, Silent Payments do not require any additional blockchain data— though this does come at a computational cost for the recipient.

  The podcast episode details all this in roughly two parts. In the first half of the episode, Ruben, Aaron and Sjors break down how Silent Payments work, and in the second half of the episode they discuss how Silent Payments compare to Stealth Addresses and Reusable Payment Codes, as well as some potential implementation issues.
---
Aaron: 00:00:20

Live from Utrecht, this is Bitcoin Explained.
Hey, Sjors.

Sjors: 00:00:23

Yo. 

Aaron: 00:00:25

Hey, Ruben.

Ruben: 00:00:26

Hey.

Aaron: 00:00:27

Ruben is back.
I think last time In Prague, we were all in Prague last week and there I introduced you as our resident funky second layer expert.

Ruben: 00:00:38

That is right.

Aaron: 00:00:39

This week we're going to talk about one of your new proposals, which is actually not a second layer proposal.

Ruben: 00:00:45

True.

Aaron: 00:00:46

You've promoted to the base chain.

Ruben: 00:00:49

I guess so.

Aaron: 00:00:46

Congratulations.

Sjors: 00:00:50

Thank you.
Welcome to the base chain.

Ruben: 00:00:53

It's good to be here.
Thank you.

## Introduction to Silent Payments

Aaron: 00:00:55

So, we're going to discuss silent payments.
This is a proposal you made recently, right?

Ruben: 00:01:01

It's a recent proposal.

Aaron: 00:01:04

So you proposed this a couple of months ago, but I think the general idea is also older, right?

Ruben: 00:01:09

Very old.

Aaron: 00:01:10

It's based on an old idea called Stealth Addresses, I think, originally proposed by Peter Todd years ago.

Ruben: 00:01:16

Yeah, 2014.

Aaron: 00:01:16

And this is an improvement on that, an iteration on that?
How would you describe that?

Ruben: 00:01:22

You could say that.
So yeah, the interesting thing is that the original proposal, I think the idea is kind of old, but the downside of this version is that you have to do a lot of work essentially to recognize that you got paid.

Aaron: 00:01:36

Of your version.

Ruben: 00:01:37

Yes.
And I think in the past, it's not like people didn't think of that, but at the time it seemed like that was going to be too much work.
And Bitcoin has improved a lot over the years.
So actually, I think sort of like that, that thinking never got updated.
And now we're at the point where we can do these kind of the verification of the blockchain quite quickly.
And the library that we use, `libsecp256k1`, is very fast now.
So basically, it made it more viable than it was back in 2014.

Sjors: 00:02:15

And for the loyal listeners, we did an episode about `libsecp256k1`.
I think it's episode two.

Aaron: 00:02:24

Really?

Ruben: 00:02:25

Oh, wow.

Aaron: 00:02:26

That's Sjors for you.
You'll remember everything.
You'll remember me.
Okay, So we can maybe get into the comparisons later, but for now, what is the general idea?
What's the general problem that we're solving?

Ruben: 00:02:38

So kind of a good way of putting it is that generally speaking, when you wanna make a payment, you have two options.
Someone can give an address and you can reuse that address and continually pay that person on the same address.
And if you do that, then you lose all privacy because every time you receive a payment, I know it's your address and then maybe, you know, Sjors sent some money to you and I can see how many Bitcoins you have, etcetera, etcetera.
So because that's a problem, generally what we do is let's say, Aaron, if I want to send you a payment, I tell you, I say like, Hey Aaron, I want to send you some Bitcoin.
Could you please give me an address?
And you're sure here's an address and every time I want to pay you, you have to give me that address.

Aaron: 00:03:18

Well, I'll generate a new address every time, right?

Ruben: 00:03:20

Yeah, generate a new one.

Aaron: 00:03:21

Ideally.

Ruben: 00:03:22

Fresh one.
And so this proposal, silent payments, allows you to basically have a single static address and allow me to derive an address from that, that nobody can recognize except for you and me.
And so this makes it basically, it makes it the same process, but now it's non-interactive where I don't have to ask you for an address.
And that is particularly useful when you think of things like donations, where there's a cause.
The cause posts one single address, and everybody goes and donates to that cause, and no interaction is required.
So that is basically the proposal.

Aaron: 00:04:00

So if I want to accept donations, then I'll post this, it's a stealth address, but you're not calling it a stealth address.
You're calling it a silent payment address, right?

Ruben: 00:04:10

Yes, just to differentiate, but it is essentially a form of stealth address.

Aaron: 00:04:14

So I'm posting this quote unquote address on my website.
And then you, Ruben, in this case, can generate new addresses from this and send money there and then somehow I should be able to spend from this address.
That's kind of where the trick comes in.
Like how can I spend money from addresses that you generated?

Ruben: 00:04:33

Yes.

## Technical Deep Dive

Aaron: 00:04:34

Okay.
Ruben, how can I spend money from addresses that you generated?

Ruben: 00:04:40

Sure.
So essentially what we do is we generate a shared secret and generating a shared secret is done by taking two public keys.
You have a public key, I have a public key, and because we both know one private key, you know your private key, I know my private key, we can do this calculation, which is basically a multiplication, that allows us to generate a number that you know and I know, but nobody else knows.
And with this number, we can then generate a key that is sort of shared between us.
So it's a public key.
You could send money to that key, but if I were to send money to that key, both you and I could spend it, so that's not quite good enough.
So we add one more step after we have the shared secret, which we turn into a shared key, we then add your public key to it.
So now it's a combination of the shared key plus your key.
And that combination is something that only you know, because I don't know your public key.
I don't know the private key behind your public key.

Aaron: 00:05:41

Okay, that's a lot of information in one go.
So let's break it down.

Sjors: 00:05:46

So what we did was a Diffie-Hellman exchange plus something else.

Aaron: 00:05:49

Right, exactly.
So, Sjors.

Sjors: 00:05:53

Yes.

Aaron: 00:05:53

What is a Diffie-Hellman exchange?
Maybe we let, that's the first part we can break down here, I think.

Sjors: 00:05:58

So Diffie-Hellman was a famous rapper.
No, basically the idea you're taking, it's being used in browsers too, for example, right?
So when you connect to a website that's secure, they have a public key.
The website essentially has a public key and you on your computer generate another public key and you basically tell the web server hey here's my public key and then the web server can send you information in secret and you can send the the web server information to that secret.
And so this really uses a very nice mathematical property, which is that if you take a private key A and you multiply it by a public key B, that is the same as when you take public key A times private key B.
So that means that, well, with Bitcoin we have addresses which is essentially just a combination of a private key and a public key.
So if I know my private key, obviously, and you know my public key and vice versa, then we can create a shared, essentially a shared address, a shared Bitcoin address where we both would own the shared Bitcoin private key and we both would own the Bitcoin shared public key.
But this would be utterly useless because if either of us sends money to that, then either of us can steal that money.
We don't want that.

Aaron: 00:07:22

Okay.
I'm following you, but that's also because before we started recording, I had an hour to try to understand this.
So to summarize this real briefly, the Diffie-Hellman exchange, two people have a public and a private key and then multiplying one public key with the other private key gets a secret number.
Because both persons know their own private key and the other person's public key, they can both generate this number, but no one else can generate this number because no one has either, no one else has either private key.
Okay.
So from this secret number, you could potentially create a Bitcoin private key.
You could say that's a Bitcoin private key, essentially, and have a public key.
And then basically what you were just saying, Sjors, is you could use that, like if Ruben wants to send me money, he could use that.
Well, he couldn't, but he could send me money to that Bitcoin public key.
And now we both have the private keys.
So the problem is then Ruben can just take the money back.
So yeah, I would have been paid, but I wouldn't because Ruben can claim the money.

Ruben: 00:08:34

It could be a feature.

Aaron: 00:08:36

So we need to add one more level.

Ruben: 00:08:39

It's a reversible payment.
Maybe exchanges would like this, right?
They send money and they can take it back.
Just kidding.

Sjors: 00:08:44

Or you make it a two step process, right?
Where you receive the money on this common address and then the other side sweeps it away and wants to sweep this confirmed, but that would mean two transactions for one, but we really don't need to do that.

Aaron: 00:08:56

So I'm not sure if I just made it more confusing for the listener.
This is the way I understood it.
So maybe that helps.
So like you could now generate a Bitcoin private key and a public key.
However, if you send money to that, that's not secure because you can claim the money back.
So there's one extra step that needs to be taken here.
What's that extra step, Ruben?

Ruben: 00:09:15

So the extra step is that we take that shared secret, that shared key, and we add the public key of the recipients to that shared key.

Aaron: 00:09:25

Right, so this is the same public key that I was sharing publicly, the silent payment thing that I had as a donation address.
And we now add the shared...
No, you finish this sentence for me before I say it wrong.

Ruben: 00:09:41

You add the shared key to it.
Which is a derivative of the shared secret.

Aaron: 00:09:45

And in this case, when you say adding it to it, it's basic, it's kind of like creating a two out of two multi-sig, except we use cryptographic tricks.
It's not actually a two of two, it looks like a wonky out of wonky, but it's sort of, it is kind of like a two of two, right?

Ruben: 00:10:04

You could think of it in that way, but essentially it is, basically we're using the fact that you can use elliptic curve cryptography in a way that is basically like regular math, where you can take someone's key and you can take someone else's key and you add them together.
And if you do this with the public keys, the private key is also the addition of one private key with the other private key.
So we have two private keys essentially.
And by adding those two together, we generate a key that only you know, because I know one of the private keys if I were to send a payment to you, but I don't know the other one because it's your key.

Aaron: 00:10:42

So the two private keys that we're adding together, to be very clear, are the shared secret private key that you were able to generate in combination with my public key, and then my actual private key that corresponds to the public key that I posted.
So that's the two that we're adding together to create a new private key and a new public key.
Well, I'm the only one who can create a new private key because I'm the only one who has the private key that corresponds with my public.

Sjors: 00:11:11

Maybe I can illustrate it from the other side, which is that if you just published your stealth address and we don't use it as a silent payment address, if you just publish an address, then anybody can send to it, right?
It would just be a regular transaction where you only have the private key and I have the public key.
The downside of that is that everybody can see what's going on.
So what if you just add something to this regular address?
So you're adding a shared key to the regular address, essentially.
That might even be an easier way to understand it.
So we just explain how you make the shared key.
And then we say we take a regular address or a regular private key.
We just add a shared key to it so that nobody else in the world can see what's going on.

Aaron: 00:11:50

Okay.
So you, Ruben, you were going to send money to my donation address.
Now we've tried to explain how that works.
We've explained how that works.
I hope people have been able to follow that.
So you're sending money to that address.
Now the question is, how do I know that you did that and how do I actually generate the private key that corresponds to that?
Because I need to know about it, right?

Ruben: 00:12:17

So the first thing you need is you need to know the key that I used in order to generate the share secrets.
Because you know your key, obviously, and I know your key because it was publicly online on your Twitter profile or whatever.
And so the key that I use is one of the keys of the inputs in the transaction that I create.
So if I want to send a payment to you, I create a transaction, the transaction has inputs, the inputs have a public key corresponding to them, and I know the private key of those keys.

Aaron: 00:12:47

This is just a Bitcoin private key, public key, just a public key that you were using anyways, that has your money on it, right?
Yes.

Ruben: 00:12:57

So when I create that transaction, I pick my input.
And that is the key that I use to generate the new address that only you can spend.
And that is where I sent the money.
And so the second step, so this is how I make the payment.
But the second step is for you to recognize that I actually did that.
And that is sort of the tricky part and sort of the downside, I would say, of this proposal, which is that in order for you to recognize that I made a payment, you have to go and check every transaction that appears on the Bitcoin blockchain.
And you have to go and see if it is a payment to you.
And the way you do that is basically the same way we generated this address.
You're also going to generate the address and you're going to see, so you're going to take the inputs, you're going to generate the shared secrets, add it to your own key, see if the result is one of the outputs.
And that is how you recognize whether or not you got paid.
So it's a lot of effort, but the effort is all on the recipient side.
And if you're running a full node already, it's relatively not a lot more effort.

Sjors: 00:13:58

So basically, every input of every transaction on the blockchain could be, as a recipient, could be for you.
So that means you have to inspect every single transaction that's on the blockchain and for every input of every transaction you want to add your shared key to it and then that generates an address and you then see hey is this transaction actually spending to that address?
If so, boom, you just essentially add that address to your own wallet, and then it just functions as any other wallet address would function.

Aaron: 00:14:31

Well, I guess it's already the case that you need to check every transaction to see if there's an output for you, right?

Ruben: 00:14:38

Yes.

Aaron: 00:14:39

So the new part is that you have to do some extra calculations to see if the inputs and then-

Sjors: 00:14:47

But it's definitely a lot of extra work, right?
So normally what you do is when you see a transaction, you only care about the outputs.
I mean, you care whether the transaction is valid at all.
That's why you look at the inputs.
But the outputs, the only thing your wallet needs to do is look at the `scriptPubKey` of this output, so basically the destination of the output, and then compare it to the list of addresses or ``scriptPubKey`` in your own wallet.
So that is just comparing one list to another list.
That's very cheap, but in this new scheme, you need to do basically elliptic curve key multiplication on every input, and then that gives you an address.
So it is significantly more work than just looking at a list.

Ruben: 00:15:28

To give a sort of approximate idea of how much work that is.
It is as if you check every signature twice instead of once.
That is sort of a very rough way of saying it.

Sjors: 00:15:43

So it definitely increases the time you need to verify blocks.
If you look at that from the perspective of your node is running you know, it's already synced and it's just running then one block comes in every 10 minutes your node will verify that block in a few seconds.
So maybe it'll take half a second longer.
That's fine, the bigger barrier is when you first want to sync the whole node.
If you want to restore from a backup, things get a little bit more hairy.
But I think we can get into that later.

Ruben: 00:17:09

That is something actually I would like to get into now perhaps because so there are-

Aaron: 00:17:12

Ruben is taking charge.

Ruben: 00:17:16

Well, I think if we do it later, it's going to be more confusing.

Aaron: 00:17:19

Go for it.

Sjors: 00:17:19

It's called Bitcoin Explained, now!

Ruben: 00:17:21

Exactly.
So there are a couple of things you can do to make this process faster.
And so as Sjors was saying, once you're at the tip and you're validating, a new block comes in, you just have to validate everything.
But one of the things you can do is, there are a couple of things you can do to sort of speed it up when you re-sync a node, and you have an address, and you want to know if there's any outputs that are yours.
So the first thing you can do is simply have a birthday on your key and say, okay, well, I created this key in January 2022.
So from January 2022, I go and I check every block.
And before that, I don't even bother.
So that's one thing you can do.
Another thing is that this protocol in principle is going to only create taproot outputs.
So any transaction that doesn't have any taproot outputs in them can be ignored.
And so you don't have to check those transactions.
That is sort of a thing that saves a lot of effort right now, because we don't have a lot of taproot transactions yet.
But in time, eventually, everything's going to be a taproot transaction.
At least that's the hope.
So it's the kind of, it's an optimization that helps today, but won't help tomorrow, let's say.
And then the biggest one is that instead of validating every transaction from the entire history, what you can actually do is you can take the UTXO sets and only check those outputs and see if any of those outputs correspond to a payment that belongs to you.
And the downside of this is that you will have no history, so you won't be able to see any outputs that were yours and were spent, but you will find all the outputs that were unspent.
And it also requires a bit more of an additional database that ties the inputs that you might require to do this calculation to the UTXO and UTXO sets.
There's a bit more complexity there, but the benefit there is that basically instead of scanning the entire history, you can now just take the UTXO sets, scan that, and find every unspent output that belongs to you.

Aaron: 00:19:36

And then you'd need to somehow get the inputs that refers to the output.

Ruben: 00:18:44

Yes.

Sjors: 00:19:46

So when you look at how a node is actually built, and you know, Bitcoin Core is built in one way, but maybe Libbitcoin is built in a very different way, there are certain pieces of information that are very easy to access and certain pieces of information that are a little bit more work to access, and that can really matter with a proposal like this.
Because if the information, for example, is sitting in your RAM memory, that's very quick to access.
If on the other hand, you need to go on a disk, it's very slow to access.
And you may have a pruned node, where a pruned node throws away all blocks so if you need any information that is in an old block then things get really really really slow because either you just can't get the information or you'd have to download the block again and then get it.
So those details matter and one of the things that I think needs to be done, and you're working on it, or you're having other people work on it, or you're hoping other people work on it, is benchmarking.
And this benchmarking basically could do things like, okay, we could change the proposal and do a little bit more signature verifications, or we could change the proposal in some other way, which means we need to do more disk reading.
And now let's try on the Raspberry Pi with the real blockchain, what performs better, what performs worse, that sort of stuff.

## Comparison with earlier proposals

Aaron: 00:20:59

Is this a good time to get into the comparison with the earlier proposals?
Okay.
So how does this compare to earlier proposals?

### Original stealth address proposal

Ruben: 00:21:11

Sure.
So the original stealth address proposal by Peter Todd, that one basically is quite similar, but the thing that was different is that because the scanning requirement was seen as something that was too much effort.
So instead of taking the key from the input, the idea was that when you generate a payment, you add an `OP_RETURN` to it.
And in the `OP_RETURN`, you add a key.
And then that is the key that is being used.
And the downside of this-

Aaron: 00:21:45

So in that case, the sender's key, in your proposal, the sender's key is actually just the Bitcoin key, the one you're using to send money from.
In this earlier proposal by Peter Todd, there's sort of a special key that's not the same key as the one that you used to spend money from, right?
And that's included in an `OP_RETURN`, a bit of extra data in the transaction.

Ruben: 00:22:10

Yeah, and so when you do that, obviously you add more overhead because now you have an `OP_RETURN`.
And the upside from the recipient side, well, it's sort of a half upside because one of the upsides is you still have to scan every transaction, but now you only have to scan every transaction with an `OP_RETURN` attached to it.

Sjors: 00:22:30

And you only have to look at that `OP_RETURN`.

Ruben: 00:22:31

Yes.

Sjors: 00:22:32

It's a lot less math than you need to do in your proposal.

Ruben: 00:22:36

Yeah, and the database lookups and stuff are easier too, because you don't have to go back and find the inputs.
It's right there in one of the outputs.
So it's sort of an in-between solution that never really got popular.
And I think even the BIP itself was never finished.

Aaron: 00:22:55

I guess one of the downsides is it makes transactions bigger because now you've got to include an `OP_RETURN`.
So, you know, box fill up faster if a lot of people do that and fees go up.

Sjors: 00:23:06

There's also a privacy downside.

Aaron: 00:23:08

It's sort of an indicator that it might be a stealth payment, right?
Even though you're not sure, but if it's an indecipherable `OP_RETURN`, then that seems kind of likely.

Sjors: 00:23:18

Well, it also means that other people looking at the blockchain can see how many "friends" you have.
So because the number of `OP_RETURN`s to your stealth address that's publicly known, people can discount them.
Or is it not?

Aaron: 00:23:32

That's not probably-

Sjors: 00:23:32

That's only a BIP-47 then.

Ruben: 00:23:34

You're confusing it too now.
No, no, so that's not quite true.
It is sort of a general, you see a bunch of transactions with `OP_RETURN`s and those are all stealth payments, but you don't know who those payments are going to.
And the recipients have to check all those specific addresses.
So it's sort of an in-between solution where you could say like, it's sort of like my proposal, but instead there's a tag that says, okay, this is a stealth payment.

Aaron: 00:24:00

And this might be a stealth payment.

Ruben: 00:24:03

Well, I think it's quite obvious, unfortunately.

Sjors: 00:24:06
Ok, so the `OP_RETURN` is only indicating that it's a stealth payment.
And then after the `OP_RETURN` is the shared key.

Ruben: 00:24:12

Yes.

Sjors: 00:24:12

So, in that case, you could probably do that with just combining signatures, and then you're pretty much back to your proposal, right?
Instead of using `OP_RETURN`, you would just basically use some sort of added key or tweak key, and you just have to check every key.

Ruben: 00:24:31

So there's a lot of similarity.
And I think the stealth address proposal also had the suggestion of adding sort of yet another identifier of saying like, okay, well, instead of checking every `OP_RETURN`, we mark it where, let's say, you pick a number between, let's say, zero and 64 or something.
And so my stealth payment is let's say 64 exactly.
So whenever in the `OP_RETURN` it says number 64 and then there's a public key, I only check those.
So it reduces the anonymity set even further, but it also lowers the scanning requirements.

Sjors: 00:25:06

Exactly.
Your proposal is a lot of work, but a stealth transaction will look exactly the same as any other transaction.

### BIP47

Aaron: 00:25:13

Okay.
And then there's,
What is it?
BIP47?

Ruben: 00:25:17

That is correct.

Sjors: 00:25:18

And that uses the concept of a handshake, I would say.
So you publish your stealth address or whatever it is.
I think they use a PayNym as a term for some people.

Ruben: 00:25:27

That is a term that Samurai Wallet uses, and I think Sparrow wallet has it implemented as well, but that's just the implementation.
In principle, it's BIP47.

Sjors: 00:25:36

So you publish this, essentially, public key, and then when you want to send somebody money using that, you do an announcement transaction first.
I think you send a `OP_RETURN` payment to that address or something like that.

Ruben: 00:25:54

That's correct.

Sjors: 00:25:54

And that `OP_RETURN` then includes some sort of key that the recipient now knows, okay, I now have a new friend and I need to start monitoring the following addresses.
So in this case, from one single transaction, you as the recipient can now generate a whole set of addresses that you just monitor as if you got an xPub.
And so that's nice.
The downside is in this case of what I said before, incorrectly for the other one, is now everybody can see how many friends you have.
Because at this handshake address is going to be a bunch of `OP_RETURN` transactions to that address so you can count, you know, a maximum of the number of friends you have.
I guess somebody could pretend that there are like five people.
And it adds a little bit of bloat to the blockchain.

Aaron: 00:26:39

So that seems to be the biggest trade-off.
Is that right?
So your proposal, Ruben, doesn't add any extra data to the blockchain.
And then the trade-off is that the recipient has to do quite a bit of work because it has to check all the transactions.
While the other proposals in their own ways, they add more data to the blockchain, but then it is easier after you've done that.
And then there's more nuances, but is this-

Ruben: 00:27:04

Well, with the stealth addresses, there's still a lot of work to do.
So I think the stealth addresses are sort of just old and outdated, and I think you can just sort of leave those aside.
But for BIP47 specifically, yes, there is not the scanning requirements.
So what you said is correct for BIP47, but to add a little bit to the downsides.
When you create this notification transaction, you're also spending one of your outputs to create that notification.
And then those outputs that you're using can then not be used for regular payments if you want to stay anonymous.
So it's sort of like you have to sort of, the money that you use to create the notifications need to be kept completely separate from the money that you use to pay people.
And that is in general very difficult for wallets to implement.
And a lot of wallets haven't implemented this correctly.
And so there's a lot of potential there for sort of privacy leaking, unfortunately.

Sjors: 00:27:59

So You think you have a stealth address, you think you're sending anonymously, but actually because of that announcement, somebody else can just still see exactly, both from the sender side, they can just see that the sender was doing this, but also it means the recipient loses anonymity because if the sender screw up, you can tell the recipient received this many coins because of this correlation.
So that's a risk.

Ruben: 00:28:21

But one thing that's maybe interesting to note is that in Prague, I had a discussion with a couple of other developers, namely Martin and Alekos.
And we have sort of thought of an idea to sort of make BIP47 better and make it so that the notification transaction can be outsourced to someone else.
So there's maybe a way to sort of mitigate that for BIP47.
And then the only downside that you are left with is the fact that it uses additional on-chain space.
And other than that, it sort of functions.
So that would sort of make the comparison a little bit more favorable in terms of comparing silent payments with BIP-47.
But still there is sort of this, this difference in on-chain space usage, which is particularly problematic for single payments.
When you want to send a one-time donation to someone, then, you know, that overhead of that notification is quite significant.

### Other generic schemes

Sjors: 00:29:20

Might be useful also to compare to some other generic schemes to solve the same problem.
So one is that instead of publishing...
Well, one is that it requires a little bit of interaction.
Somebody has to send you an email anonymously and you reply with an xPub and now they can just send whatever they want to that xPub.
That's one thing you can do.
You can run a little Tor hidden service that will just hand out xPubs to anybody who asks.
That is a problem with, you know, denial of service and of course you have to run server.
Denial of service means basically somebody could ask you for an xPub and then ask you for an xPub and ask you for an xPub.
And then for every time you've given out an xPub, you've got to monitor like a thousand addresses forever.
So that's one thing.
Another obvious thing you can do is use Lightning because with Lightning, you have a public key and something like a Bolt 12 tattoo.
Once that's finalized, we'll make it just very easy to receive money, but it means some...
That puts a bit more burden on the sender, definitely not as much burden on the recipient, because what you're proposing doesn't sound more difficult than running a Lightning Node.
At least not more resource intense than running a Lightning node.
But for the sender, of course, they have to run a Lightning node.

Ruben: 00:30:36

It's interactive, essentially, when you use Lightning.

Aaron: 00:30:40

But Ruben just promoted to the base chain, so.

Ruben: 00:30:43

Now we're moving back to the base..

Aaron: 00:30:47

Don't kick him back to Lightning.
Let him enjoy his stay here.

Sjors: 00:30:51

And on the base chain, you can run a BTCPay Server or something like that that will give out a unique address every time.
That's a little bit less of a DDoS problem than an xPubs.

Ruben: 00:31:03

I mean, you still have to give out a new address, right, for BTCPay Server.
I still think it's a problem.
I wonder how they solved that problem, actually, because you have the same issue where if you continually ask for addresses.

Sjors: 00:31:11

But an xPub represents a thousand addresses, so your problem is a thousand times bigger, but it's the same type of problem.

Ruben: 00:31:18

True.
And so just to sort of generalize, I think the sort of the trade-offs that you're mentioning here is one of interactivity, where with silent payments, the nice thing is it is just entirely non-interactive.
But you are absolutely correct that, you know, given sort of like the complexity of what you said, it is possible to solve this with interaction.
And that is essentially what we started off with, with me saying, okay, well, if Aaron just gives me a new address every time I want to send a payment to him, that works too.

Aaron: 00:31:49

The whole point is to make this non-interactive.

## Using DNS to announce your address

Sjors: 00:31:53

I wanted to mention one cool possibility that I saw somebody bring up on one of the threads that related to this, which is the idea of using DNS or the `/.well-known/` URL to announce your address.
So what you can do is if you run a web server or React, you have a provider that does that for you, is you could say, well, If somebody types in my email address, then the wallet will just basically know where to look, either in the DNS record or at a specific spot on the web server, and it will get the key there.
So then, if you have a very smart wallet, I could imagine that I just type somebody's email address and it'll see, oh, is there a silent payment ID there?
Is there a Bolt 12 invoice there?
Is there an LN URL thing there?
I'll just pick one of those three, and I'm going to send the money to it.
So from a usage point of view, it's very nice to have these static identifiers.

Ruben: 00:32:50

I see what you mean.
That's interesting.

Sjors: 00:32:53

And I also have a downside, but that might be solvable.
And that is what I would call the Hotel California problem.
Because basically once you've given out this thing, people can keep paying to it forever.
And at some point you might realize, ah, this running this extra thing on my node is pretty heavy.
I'd like to downgrade.
I'd like to stop using this.
And I think that can be solved by just putting an expiration date into them.
Like saying like, okay, don't send coins to me after this block height.
That would just be part of the standard.
And then you scan a few hundred thousand or you scan like 10,000 bucks extra, just to be sure.
But you definitely want to make sure that people can opt out of this stuff.
Because with Bolt 12, that's not a problem, right?
With Lightning, you still have to ask an invoice.
And if the server doesn't respond, you don't send money to it.
But with this, if somebody sends you money 50 years from now, like your descendants will have to like scan the whole blockchain.

Ruben: 00:33:46

That is a good point.
And that's something I hadn't really thought about.
But I agree that it would be nice to support maybe a date at which you stop, well, either you stop using the address or you have to refresh the address as to say like, okay, well now I'm going to accept it for longer.

Sjors: 00:34:04

So that's when you combine it with this DNS server system, your wallet would just ask again and you could have very short expiration dates even on them.
That's not necessarily the case, but you could use the same payment code again.
You could just say like, okay, I'm only gonna guarantee this thing for like a week.
And then if you ask again next week, I'll say, okay, no, don't worry.
You can use the same key.
It's gonna be valid for another week.
Something like that.
That's, I mean, I have a whole bunch of like implementation stuff, but I don't think we have to get there.

Ruben: 00:34:34

That's interesting though, but yeah.

Aaron: 00:34:35

How long have we been recording, Sjors?

Sjors: 00:34:37

33 minutes.

Aaron: 00:34:38

How deep are we into this stuff?
Because there's a lot more in the show notes, or at least there's some more in the show notes.

Ruben: 00:34:44

Sure.

Aaron: 00:34:44

Like, do we want to get into that?

Sjors: 00:34:46

I've covered everything I wanted to cover, but...

Ruben: 00:34:48

I guess the one thing...

Aaron: 00:34:50

There's this...
Go on, Ruben.

Ruben: 00:34:52

Just one thing I wanted to mention maybe is that I think what's good to point out here is that the scanning downside really is mainly a downside if you're not running a full node.
If you're running a full node, the way I look at it is that we still have to get these benchmarks.
And so as Sjors already mentioned, there's a pseudonym called W0XLT, who I'm trying to collaborate with a little bit now in order to get these benchmarks.
And he's already created an implementation.
And once we have those, we can get a better idea.
But my feeling is that we can get it down to a level where if you're running a full node and you're doing this additional computation to receive these silent payments, it is not a lot of extra overhead.
So from that perspective, I think you could say that sort of the overhead is practically zero if you're already running a full node.
And then for light clients, the problem is that even though, like many of the light clients, most of the light clients we have today, they share an xPub with whatever server is running the light client for them.
And if you give out your xPub to a server, you lose all your privacy.
So it's actually very difficult to have a ligth client and have privacy at the same time.
It's not impossible.
We have a BIP 157 and 158, that is a compact block filters.
So you could have sort of a light client that preserves your privacy better.
But as far as I know, it's maybe Wasabi wallets.
And I'm not even sure some lightning wallets maybe use it.
But other than that, most wallets don't really do that today.
So my argument there is sort of that if you care about privacy, you already sort of have to run a full node.

## Implementation and Future Directions

Aaron: 00:36:39

And so you mentioned there's a pseudonym working on this.
So how concrete is this?
Are we going to, when am I going to be able to use this?

Sjors: 00:36:47

I did run the demo today on Signet.

Ruben: 00:36:50

Cool, talk about it.

Sjors: 00:36:50

So that was fun.
So the pseudonym you talked about, let's call him Ox.

Ruben: 00:36:56

Ox, yeah, it's easier.

Sjors: 00:36:59

Created a pull request on Bitcoin Core that is like really marked as like this is just a proof of concept.
Don't merge this.
Don't even use this with real coins, right?
And it allows you to create a wallet that can receive silent payments and it allows you to use any wallet really to send silent payments.
And you know, it requires a little bit of manual stuff, but it worked.
I mean, at least it seemed to work.
I haven't checked if the math actually worked.
If somebody steals my Signet coins, I don't care for real coins.
I want to be a little bit more sure that this is right.
I have some remarks in mind that I'll probably post before the show comes out.
But I mean, if you look, I mean, there are different approaches to get a new proposal like this done, right?
And I would congratulate you.
I think this is the first time or the fastest ever that you've gone from like proposing something really complicated to something that actually demos the concept.
And I personally, I like running code to understand something better.
And so, and then when I looked at it, like this approach of changing Bitcoin Core to support it is one approach.
Another approach could be something like what Specter Wallet does is you create a tool that people download or install that is separate from Bitcoin Core, but that uses Bitcoin Core wherever it's useful.
And so I looked at both possibilities and both are not trivial in this case.
For details I don't think we necessarily have to go into, but this proposal, I don't think this pull request will ever, well, will not get merged in the short run, even if he improves everything.

Aaron: 00:38:31

Not in Bitcoin Core.

Sjors: 00:38:32

No, and a couple of reasons for that is because it essentially requires another index, which takes up space and it is, you know, like you said, it's maybe not the worst extra performance downside, but it's still pretty significant.
You know, it still adds.
So I think Bitcoin Core would not very quickly commit to a feature that it has to maintain forever that really eats a lot of resources and may screw with other proposals that might enhance scaling, like how does this combine with assumeUTXO or how does this combine with Utreexo or...
So that's why I think it's better to go for a separate tool.
On the other hand, any demo that works, I'm happy with it.
I don't really care how it's done, whether the demo is a modified version of Bitcoin Core or a little Python script.
I don't think it matters as long as people play with the demo because standards will get much better when people actually try them.
Otherwise you get things like BIP32 and like, oh, gap limits.
I guess we should have thought about that before we defined a standard.
So yeah, I'm happy to see that.
I just would want to caution the listener and this is probably gonna take a while.

Ruben: 00:39:43

I agree with that.

Sjors: 00:39:45

Because I guess I should explain the other side of it.
If you make a separate tool, now you're no longer a first class citizen of Bitcoin Core.
So you have to communicate through Bitcoin Core, through the RPC, and it has very limited features, very limited things you can do.
And one of the things you may want to do is very tightly integrate with block validation.
So when a block comes in, you want to do some processing specifically for the wallet.
You can't do that right now with Bitcoin RPC.
So yeah, it's tricky.

Ruben: 00:40:11

There's some complexity there.
But yeah, at a high level, I agree with you.
And so one of the things that's sort of tricky for me is that actually spacechains is sort of the project that I'm currently focused on.
And now this silent payment thing, it was supposed to be sort of a side project where I thought like, okay, I'm just going to put this out on a gist and then I'm done with it.
And then people start running with it and this Ox guy, he implements it.
And now I'm like, okay, shit, I got to put some effort into this as well now.
So I'm being pulled into multiple directions, but it's a good thing because it's a success story, I guess.

Aaron: 00:40:48

I mean, spacechains is literally a side project, right?

Ruben: 00:40:52

It's a sidechain project, yes.

Sjors: 00:40:54

That's the pun of the week.

Ruben: 00:40:55

Good joke, yes.

Sjors: 00:40:56

All right, it's a good pun.
I have another pun on the GitHub comment, but it's not for here.

Ruben: 00:41:03

All right, well, I'll look forward to hearing that offline.

Aaron: 00:41:06

I cannot wait, Sjors, to read that.

Sjors: 00:41:08

It's gonna be amazing.
Okay, I think that covers everything.

## Coinjoins and Silent Payments

Ruben: 00:41:12

Is there anything, Aaron, I think there's something you wanted to bring up still, or am I mistaken here?

Aaron: 00:41:17

I mean, I was gonna ask about Coinjoin.

Ruben: 00:41:22

Ah, yes, of course.

Aaron: 00:41:23

That seems like opening up another can of worms.
I don't know if we wanna go there.
That is true.
Now that I've brought it up, we can't really ignore it completely.
Do you want to summarize this in like a minute?

Sjors: 00:41:36

I think we should briefly look at the worms.

Ruben: 00:41:38

I agree.
Now that's actually a good one to point out.
So I think this is one of these things that I feel most uncomfortable with in terms of, like, because ideally what you want to do is you want this protocol to not get in the way of how people do transactions.
And so far, the way we've described it, it sort of works really well if there is one sender, if I create the transaction.
But what if we wanted to create a transaction as a Coinjoin where we have multiple people adding their inputs?
And so the first issue is that you sort of have two variants of...

Sjors: 00:42:14

And then one of the recipients is a stealth address.

Ruben: 00:42:17

Exactly.
Yes, yes.
That's good to add.
Thank you.
So the first issue is sort of that you have two variants that you could do for a sign of payments.
Well, there are more variants, but these are the two sort of main ones, which is either you pick one input and you use that to generate the shared secret, or you pick the combination of all the inputs.
And this is particularly relevant with Coinjoins because if you pick just one input, then what that means is that if someone pays you in a CoinJoin, then the recipient normally doesn't know what your input was.
So that's actually very good for privacy.
But if you use the silent payments, now if it's just with a single input, you can see which input was paying you.
And so that leaks some privacy for the sender.

Aaron: 00:43:03

You can see which input pays you because that's the one that adds up to your new address.

Ruben: 00:43:08

Exactly.

Aaron: 00:43:09

There's only one input that matches your new address.

Ruben: 00:43:11

Yes.
And so that's solvable by saying, okay, well, we pick all the inputs instead.
And we add those inputs together and we use that to generate the shared secret.
But once you do that, you need the collaboration of all the Coinjoin participants.
And in fact, you need them to generate a shared secret.
And you also don't want them to know who you are paying.
So you need to get them to give you their shared secret in a way that they don't know what they're giving to you.
And there's a protocol for that too, which is basically a blind way of doing a Diffie-Hellman, which is also used in e-cash.
Long story short, a lot of complexity.

Aaron: 00:43:48

A lot of worms.

Sjors: 00:43:49

And you're actually making the single, the simple case, you're making that more complicated by aggregating the signatures.
Because normally when I use a wallet to make this silent payment, I just need to pick one coin, one input, and then if the wallet needs to, it can just add more inputs to that transaction and it will still work.
But if you want to have all the inputs count towards the shared key, then I need to decide before I have the destination address, I need to decide which coins I'm going to use.
And so then you have the coin selection process separate from the payment process and that at least in Bitcoin Core, that's going to give you another can of worms that I recommend not opening.
There are solutions to it.

Ruben: 00:44:28

Well, the other thing that's sort of nice about adding all the input keys together and why I sort of gravitate towards that is that it essentially cuts down the scanning requirement in half, because now instead of having to scan every individual input, you can scan the aggregation of all the inputs.
And on average, a transaction has two inputs.

Sjors: 00:44:46

That's true, but that's where the benchmarking has to come in, because I would not be surprised at all if the, whether you look at inputs individually or you add them up, most of the work is probably going to be in fetching the original transactions from some disk somewhere.
And then the actual elliptic curve math is gonna be much less than that because in general it takes a long time to read something from a disk it takes a very short time to do a calculation on the CPU but that could be completely wrong that's why you want to benchmark this stuff.

Ruben: 00:45:16

So I am sort of I have the same concern in terms of this needs to be benchmarked and we need to compare it all.
And quite frankly, I even think that maybe the UTXO set scanning is overkill too.
Maybe it's just better to just do the entire scanning when you do IBD and maybe that's sufficient.
So it's sort of, yeah, it all comes down to the benchmarks basically.
I agree with that.

Sjors: 00:45:40

Cool.

Aaron: 00:45:41

Okay.
I think that's our episode.
Sjors, what do you think?

Sjors: 00:45:46

Sounds good.
I'm not going to put this thing as a tattoo on me yet.
But I'm going to keep it in mind.
Yep, I think that's it.
So thank for listening to Bitcoin

Aaron: 00:45:58

Explained.

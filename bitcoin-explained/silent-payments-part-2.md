---
title: "Silent Payments part 2"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-94-silent-payments-part-2
tags: ['silent-payments']
speakers: ["Sjors Provoost", "Aaron van Wirdum", "Ruben Somsen"]
summary: "In this episode of Bitcoin, Explained, Aaron and Sjors welcome Ruben Somsen and Josie to the show to discuss BIP 352, their now-finalized Bitcoin Improvement Proposal for Silent Payments."
episode: 94
date: 2024-07-07
additional_resources:
  - title: https://bitcoinexplainedpodcast.com/
    url: https://bitcoinexplainedpodcast.com/
---
Speaker 0: 00:00:16

Live from Utrecht, this is Bitcoin Explained.
Hey Sjoers.
Hello.
Hey Josie.
Hey.
Hey Ruben.
Hey.
We've got two guests today Sjoers.
Is that the first time we've had two guests?

Speaker 1: 00:00:27

I believe that is a record number.
We have doubled the number of guests.

Speaker 0: 00:00:31

That is amazing.
You know what else is amazing, Sjoerd?
The 9V battery thing that you have in your hands.
You just pushed a...
This is a CoinKite product as well?

Speaker 1: 00:00:41

I don't know if they really sell it, but I think they have it, yeah.

Speaker 0: 00:00:44

Explain what you just gave me.

Speaker 1: 00:00:46

You put it on top of a 9 volt battery and then it has a USB port so you can charge your devices offline in a nuclear shelter etc.
But they also have...

Speaker 0: 00:00:57

Charge what offline?

Speaker 1: 00:00:58

Your devices.
But I guess mostly used to not charge the hardware wallet but just to turn it on and keep it on.

Speaker 0: 00:01:05

Anyways, another amazing CoinKite product.
And here's another one, the Cold Cart Q.
Josh has got many Cold Cart, CoinKite devices.
Buy them all.
Exactly.
Okay, let's get to our episode.
We're going to discuss silent payments.

Speaker 1: 00:01:26

That's right.
And we talked about that in episode number...

Speaker 0: 00:01:31

52 from the top of my head, actually.

Speaker 2: 00:01:33

Somewhere around there.
I don't remember exactly, but it was somewhere 50-something.

Speaker 0: 00:01:36

Yeah, so we did one episode on silent payments right after you, Ruben, proposed it on the Bitcoin Dev mailing list.
Yes.
Now, fast forward two years later.

Speaker 1: 00:01:45

This episode is still up to date and perfectly fine, so you can stop listening.
Almost.

Speaker 2: 00:01:50

There are a few things we could talk about, but it was surprisingly accurate.
So definitely something to go back and listen to.

Speaker 0: 00:01:56

Yeah, we'll give our dear listener, you, our dear listener, a short update.
But first, let's do a short introduction also.
So Ruben, you are our de facto complicated second layer expert who also came up with silent payments, right?

Speaker 2: 00:02:13

Which is not a second layer, so basically breaking the rule there.
But you could kind of see it as a second layer because it's a sort of secondary way of interpreting data on the Bitcoin blockchain.
So sure, let's say.

Speaker 0: 00:02:25

No, no, no.
Now you're stretching the definition.
I'm just giving a picture of who you are usually.
But this is a different proposal for you.
Josie, our listeners don't know you yet.
Where are you?

Speaker 3: 00:02:36

I am a Bitcoin Core developer.
So I started contributing about three or three-ish years ago, I think.
I started off in the wallet mostly out of an interest in privacy stuff, and also just usability, because I used the Bitcoin Core wallet, which was part of what got me so excited about silent payments.
It was kind of the feature that I felt like was missing.
But yeah, I spent a lot of time in the wallet and also a lot of time thinking about privacy improvements without SoftForks.

Speaker 0: 00:03:02

So what happened?
At some point you read Ruben's proposal and you decided to implement it or what?

Speaker 3: 00:03:07

No, I heard him present on it at TabConf in October of 2022, I think.
I think you had just kind of written the gist and had been talking to people maybe following the Prague discussions Yep, so Reuben gave a presentation on it, and I don't think he and I had officially met at that point And I was so excited after the talk was finished I went up to him afterwards and was like, what do we got to do to make this a reality?
This sounds awesome.
And then I think at that point, we decided the next step would be to write the BIP.
And so we decided that's where we would spend the next amount of time just kind of refining the idea.
And then after writing the BIP, I started working on an implementation for Bitcoin Core.

Speaker 0: 00:03:53

And a lot of this work was done in Utrecht, is that right?

Speaker 3: 00:03:56

Yeah, yeah.
Like I said, we hadn't really met each other before.
So at one point Ruben was like, well, it's going to be hard to coordinate.
I'm in Utrecht and I was like, dude, I'm in Amsterdam.
This is perfect.
So then I would catch the train down to Utrecht about once a week and we'd sit in a Starbucks and.

Speaker 2: 00:04:11

Yep.
Talk for hours.
A lot of fun and very useful.
I think, especially, so the funny thing is even though like the, the previous episode, which by the way is episode 58, so just a correction there.
Although it's very accurate, there were still a bunch of details that were very tricky to work out.
We're not really going to go into them, I think, for this discussion, because they're not really relevant for understanding the protocol necessarily.
But there was still a lot of work to be done, and we had a lot of pitfalls, like malleability issues, things like that.
So there was a lot of work left, even though it seemed like it was pretty cut and dry, it certainly wasn't.

Speaker 0: 00:04:56

Yeah, well, I just wanted to point out that it's a second grade Utrecht homegrown project,
which I'm very proud of.
The first one, of course, being Bitcoin Explained.
Needless to say.
So the BIP is BIP352, 352, and this was finalized a couple of weeks ago?

Speaker 3: 00:05:16

Maybe a month at this point.

Speaker 2: 00:05:18

Any longer.
It must have been two months ago now.

Speaker 3: 00:05:21

Maybe it's worth mentioning because I think there's a lot of confusion about this.
We were kind of considering the BIP somewhat final, maybe a few months before that.
Yeah.
Where the protocol was done and we had test vectors, but then it took about another two months for the BIP to actually get merged.
And then all of the changes were just like copy edits.
And we actually had people starting to build implementations before the BIP was finalized, but the BIP actually merged into the repo maybe two months ago.

Speaker 1: 00:05:49

I did a little testing myself because I was maintaining a small indexer pull request on top of your pull request to see if it's compatible and then other people would have other implementations and I would run a little script that would just compare them to make sure that for our mainnet, every silent payment tweak, and I guess we'll get back to what that is, is the same.
And the answer was usually, but there were still a few inconsistencies.
Some bugs on our end and some bugs on other people's end, so it's always useful to compare.
And, you know, so even when the BIP is final, you still want to maybe not tattoo your silent payment address.

Speaker 0: 00:06:22

Yeah.
Well, you were kind of going to do that now, we thought.
Because on the previous episode, you said no time for tattoos yet, but there's still no time for it.
Now you're just copying out.

Speaker 2: 00:06:33

Now the beta is final.

Speaker 1: 00:06:36

I'm starting to talk to my tattoo consultant.

Speaker 3: 00:06:39

Wait for Bolt 12 because then you can get a unified QR code tattoo of Bolt 12 and silent payments.
Unless you want to get two tattoos.

Speaker 0: 00:06:46

Okay, I'm going to give a one-sentence explanation of what this sort of is, and then we'll go to a short recap.
But you can correct me if I'm wrong.
So basically, right now, we use Bitcoin addresses, which are great.
The problem is that you can't, Well, you can reuse them, but it's really bad for privacy.
So if you, for example, want to put up a donation address on your website, then people can donate to you, but then they also see exactly, anyone can see exactly, you know, when you're spending your money, and how much money you received, and all of that.
So, silent payment addresses are also something you can post publicly, but then whoever is paying you basically generates a new address for you every time, with you being the only one to be able to spend from that.
Right?
Well, this was more than one sentence.

Speaker 1: 00:07:31

Yeah, and the cool part there is that you as the sender are generating the address for the recipient in a way, so you don't need to talk to the recipient at that point, because normally the recipient has to do that for you.
So it's not interactive, but the recipient knows what that address is going to be.
So as the sender, you don't have to send an email to the recipient saying, please look here.

Speaker 0: 00:07:50

Yeah, so the challenge of doing something like this is how can the sender generate an address that the recipient can then spend from?
That's basically the challenge that had to be solved.

Speaker 2: 00:08:04

And only the recipient can recognize also, right?
Spend from and recognize.

Speaker 0: 00:08:09

Only the recipient will know that that address is also, well, the sender will know as well, but no one else will know.

Speaker 2: 00:08:14

So In three words, I would say private reusable addresses.

Speaker 1: 00:08:20

Single payment identifier.

Speaker 3: 00:08:23

Static payment codes.

Speaker 2: 00:08:24

All right, everybody has a different.

Speaker 3: 00:08:27

Naming is art guys.

Speaker 2: 00:08:28

As long as people understand it, That's the important part.

Speaker 3: 00:08:30

I think maybe one distinction, the difference here is the sender generates an address that is only spendable or knowable by the recipient, but also in a way that the recipient can find it without requiring extra data on the blockchain or out-of-band communication.

Speaker 0: 00:08:48

Right.

Speaker 3: 00:08:48

So the recipient, and this is a distinction against like XPubs and BIP32 style addresses, the recipient doesn't actually know about the address until the sender creates it and it's confirmed in the blockchain.

Speaker 0: 00:09:01

Okay, so even though we did already discuss this in episode 58, let's do a recap of how this works.
Last time Ruben did it, so maybe Josie, do you want to give this a try?

Speaker 3: 00:09:11

Yeah, yeah.
Let's go.
So in a nutshell, We are reusing information that is already in the transaction to establish a shared secret.
And that shared secret is only valid for that single transaction, and it's a shared secret between the sender and the recipient.
The shared secret is what allows the recipient to find the outputs.
And then the thing that we do to make it only spendable by the recipient is there's of the output that is created, which is a taproot public key.
The output is created by combining the shared secret with the recipient spend public key.
So basically the the transaction itself becomes kind of the notification of a payment and the clip I guess the clever trick is to do a shared secret elliptic curve Diffie-Hellman is kind of the standard for that.
And that involves a private key, public key pair.
And so the sender is just reusing the private keys of the UTXOs that they wanna spend.
And then the recipient is finding that shared secret by looking at the public keys of those UTXOs.

Speaker 0: 00:10:18

Yeah, we're gonna break this down.
So first, to start, what actually is a silent address?
Like, is it basically a regular Bitcoin address?
Could you also just send money to it and then spend from the private key?
No, it's a special type of...
But it is a public key, right?
It's two public keys.
The silent address is two public keys?

Speaker 3: 00:10:38

Yeah, so it's more specifically, it's a batch 32M encoding of two public keys.
So it has an HRP instead of BC, it has SP.

Speaker 0: 00:10:47

I have no idea what any of this means.
Do you, George?

Speaker 1: 00:10:50

It's the HRP.
Human readable part is what HRP means.
So when you look at a Bitcoin address that starts with a BC1P, the BC stands for Bitcoin.
It's like it doesn't have any meaning for the computer other than, well, a little bit, but it's human readable, so you can say, oh, this is a Bitcoin address and not a, say, testnet address.
And a sign-in payment address starts with SP, so you know it's a sign-in payment address.

Speaker 0: 00:11:14

Okay, you are actually literally talking about the address format, how the address starts.

Speaker 1: 00:11:18

But I would say that, yes, there's two public keys, but for the purpose of explaining the shared secret, just assume it's one public key, because you don't need to know about the second one.
Yeah.
Because we were trying to explain how the shared key works, right?

Speaker 0: 00:11:33

Well, I mean, first of all, I guess I'm trying to get to how the shared secret is generated.

Speaker 1: 00:11:37

Yeah, it uses both, I think, but for the sake of simplicity, just assume it's just one.
So you have a public key of somebody else, the person you want to send money to, and they have the private key belonging to that public key, which is an important ingredient for a shared secret.

Speaker 3: 00:11:53

Yeah, I do think it's worth talking about them separately though, because I think separating them was kind of something we took from the Monero community of having the scan key, or the view key and the spend key.

Speaker 2: 00:12:05

It's not from the Monero community.
Before that, it was already a thing.

Speaker 3: 00:12:09

But I think the distinction is good to mention there are two keys because that allows for a separation of responsibility.

Speaker 0: 00:12:15

Okay, so the silent payments address has two public keys and two private keys.

Speaker 3: 00:12:20

Well, two public keys where the recipient owns both of the private keys for the address.

Speaker 0: 00:12:25

Sure, yes, exactly.
Okay, so how is this shared secret now?
So let's say you've posted this somewhere, Josie, and I want to pay you.
So how do I now create a shared secret between us?

Speaker 3: 00:12:38

Yeah, so you would first do your coin selection and figure out which coins you want to spend.
You would take the private keys of all of those coins and you would add them up to get one new private key.

Speaker 0: 00:12:48

Then you multiply- Can we for simplicity just say I'm using one UTXO?

Speaker 3: 00:12:53

Yep, so you take that one UTXO, you take the one private key from that UTXO, you multiply that one private key with the first public key from my address, which is the scan public key.
So you're, you know, your private key times my public key.

Speaker 0: 00:13:09

Yeah.
That's what you're describing right now is the general Diffie-Hellman exchange.
Exactly.

Speaker 1: 00:13:15

Right.
Those, those, you know, you know, Josie's public key because he put it on the internet and Josie will know your public key because that's where the money is coming from.

Speaker 3: 00:13:23

It'll be in the transaction.
So now you've created a shared secret.
You take that shared secret, you do some things to it in the protocol, and then you take that second public key from the address, and you add it to the shared secret.
And then that makes something that is findable by me, but only spendable by me.

Speaker 0: 00:13:41

Right, okay, yeah.
So for those, there might be listeners that don't know this, but the general idea of the Diffie-Hellman exchange is that we both have a public key and we both have a private key by combining or what's a better word, factoring.
Multiplying.
Multiplying one of our private keys.
So I will use my private key in combination with your public key.
And you can do the opposite, your private key with my public key.
Then we create one shared secret that only us will know because you need at least one private key to generate it.

Speaker 1: 00:14:12

Yeah, but of course, because both of you know it, you can't send it to that because then you can just take the money back.

Speaker 0: 00:14:17

Yeah, exactly.
So that's where the second public key in the silent payment address comes in.
And can you repeat that for me?
So what do you do with that?

Speaker 3: 00:14:26

So before we talk about that one, just maybe to make it clear, the public key that I use to find the payment is already existing in the transaction.
And this is kind of the important part of silent payments.
There is nothing extra.
Cause I think in stealth addresses, they had a similar way where you would have this ephemeral secret and then they would encrypt it in an op return.
But then it was kind of obvious and the user had to pay more.
So once I've created that shared secret, as the sender, like Shor's mentioned, if I use just the shared secret, both of us know the shared secret.
So then either one of us could spend it.
When I take the spend public key and I add it to the shared secret, I now have something where both of us can find it with the shared secret, but then only I can spend it because only I know the private key to the spend public key.

Speaker 2: 00:15:15

Okay, so maybe one thing to sort of add here and to clarify is that last time when we talked about this, there was just one key that we basically talked about.
And even back then there was already the separation of there being two keys, but just for simplicity, we didn't really talk about it.
So you have a key with which you generate the shared secrets and then there's a separate key that you add to it.
And the reason we have the separation of two keys is purely to have the functionality of finding out whether or not you get paid, which requires what we call the scan key and actually spending from it, which we call the spend key.
We can separate that out so you can have a device that does all the scanning, that checks, hey, did I get paid or not?
And does the generates the shared secret and then checks, is this actually a payment?
And actually spending it, that key can just be on a hardware wallet that isn't necessarily connected to the internet, cannot really do the scanning in an efficient way.
In theory, probably they could, but in practice, that's difficult.
So that's why we have this separation of having these two keys.
But if you sort of forget about that separation, you could do this whole thing with a single key.
It just means you can't separate out the spending from the scanning.

Speaker 0: 00:16:34

Yeah, as I recall in the earlier podcast, the previous podcast we did on this, you just tweaked the set.
Yeah, you used the same key to tweak it again.
And that was to make sure that only the recipient can spend the money afterwards.
And you're saying that it was implemented differently because this makes it easier to scan to see if you receive the payment.
Am I hearing that right?

Speaker 2: 00:17:00

It means you can have two separate devices that do two separate things.
You can have a device that does the scanning, you can have a device that does the spending, and that would generally be a hardware wallet.
And so the last time we talked about this, basically I tried to keep it simple, So I didn't talk about this distinction.
But since this is the second time, I thought it would be good to sort of bring it up and Josie brought it up.

Speaker 3: 00:17:24

Yeah.
And I think maybe to give a concrete example, when you're the recipient, the way that you scan is by having your scan private key in a hot online device.
And so in the old method where we were reusing the same key, that means in order to scan, the private key that you need to find the payments and also spend the payments is now on an internet connected device.
And that's really not a great idea.
So by having two separate keys and the separation of responsibility, you can hand out that scan key to an online device and that online device will do the scanning for you, which if that device gets hacked or whatever and someone gets that key, it's the same as leaking your XPub.
Someone would be able to see your payments but they wouldn't be able to spend them.
So I think that's really kind of the critical thing why the two keys is so important.

Speaker 0: 00:18:11

I want to pause here for a second on the scanning issue.
So how does the scanning actually, like how do you know you've been paid?
How does this actually work?

Speaker 3: 00:18:21

So you look at a transaction and there's a couple criteria that we can use to see whether or not the transaction is even eligible to be a silent payment transaction.
So the first one is it needs to have at least one taproot output.
You can even go further and say, well, I'm not really interested in other people's silent payments, so I'm only gonna scan transactions that have at least one unspent taproot output.

Speaker 0: 00:18:46

And to be clear, it scans for taproot because it uses the taproot, it uses snore basically, I would say, right?
So if it doesn't have the taproot output, then there's no way it can be a silent payment.

Speaker 3: 00:18:59

Yeah, we specified in the BIP that the sender always generates a taproot output.
So you can skip all transactions that don't have taproot outputs.
You can also skip all transactions where all the taproot outputs are spent.
Then the second thing you look at is what are the inputs of the transaction?
And there needs to be at least one input that is specified in the BIP.
So like a native SegWit input or a wrapped SegWit input or paid a public key and or a legacy.
So pretty much like...

Speaker 0: 00:19:26

Why is that?

Speaker 3: 00:19:28

There's complications with other inputs like the old bare multisig style, where like Ruben had mentioned earlier, one of the things we were working through in the BIP was dealing with these cases of malleability.
And so that's one example of it.

Speaker 0: 00:19:42

Okay.

Speaker 3: 00:19:42

So if you look at the inputs and there's nothing in there that's specified in the BIP, you're like, okay, I'm gonna skip this transaction.
Okay.
Now, when you see a transaction that has an unspent taproot output and at least one eligible input...

Speaker 0: 00:19:53

So, just to stop you for one second, what you've described right now is like, could it technically be a silent payment?
Exactly.

Speaker 3: 00:20:00

That's the first thing.
Okay, now the answer is yes, it could technically be, now what?

Speaker 0: 00:20:04

Now the question is, okay, this could be a silent payment, is it a silent payment to me?
So then you would take the inputs, you get the public keys from the inputs, and each input kind of has its own way of doing that, but you get the public key, If there are multiple inputs, you sum up those to get one single public key.
And then you take that public key, you multiply it by your scan private key, generate the shared secret, and then you add your spend public key to it, which then creates a new public key.
And you see if that public key is present as any of the taproot outputs.
If that public key that you just created matches one of the taproot outputs, then that taproot output is yours and it's only spendable by you and you add it to the wallet and then move on to the next transaction.

Speaker 2: 00:20:47

So any wallet will, you know, look at every transaction in a block to see if the transaction is going to them.
So that's conceptually not new, but what is new is that you need to do a bunch of extra math, multiplying two points or a private key and a public key in order to even see if this is going to you.
So it makes it competitionally a little heavier to scan.

Speaker 0: 00:21:09

And maybe to put some context around how much is that extra computation, when you verify a signature, like so a full node sees a transaction, it verifies all the signatures, you're doing a multiplication to verify the signatures.
So the amount of work that you're doing to check a silent payment is roughly a signature check.
So it is more work, but I think it's good to quantify like how much more work are we talking about.
So it's basically like if a transaction had three inputs, you're verifying a transaction as if it had four inputs.
So not that much more work for a full node.

Speaker 2: 00:21:45

Right.
It's one signature equivalent per transaction, but a transaction can have multiple inputs.
So it doesn't double the time to validate a block, but it adds a bit to it.

Speaker 0: 00:21:55

Yeah, I would say maybe...

Speaker 1: 00:21:59

I think that's the most accurate thing to say, just one additional signature check, which is...

Speaker 2: 00:22:02

Yeah, and so then it depends on what you are.
If you are a full node and you are in the business of doing this once every 10 minutes, as a new block comes in, it'll take you normally, I think, far less than a second to verify a new block when it comes in.
So now it'll take you far less than a second plus a little bit.
Yeah.
So for a full node, this is no extra work.
The more complexity starts when you're dealing with light clients, light wallets, mobile wallets, those kind of things.

Speaker 0: 00:22:28

Yeah.
That's right.

Speaker 3: 00:22:29

Okay, let's get there.
So just to recap, usually any full node always checks any transaction in a block to see if it is being paid, plus checks if the signatures are valid.
Now with this, it would be one extra check to see if you're paid through a silent payment.
Correct.
Okay.
So LiteClient, it's more complicated for LiteClient then, because LiteClient don't usually check every transaction to see if it's, yeah, well they don't check every transaction.

Speaker 2: 00:22:57

Yeah, there's different kinds of light clients, right?
There is the old school Electrum style, well even old school Bloom filters I believe, but let's not even talk about that.
And then you have, well, Electrum style, which basically tells the server somewhere on the internet, hey, here are my addresses, please tell me my balance.
That is not optimal for privacy.
Also wouldn't work directly with silent payments, right?
You would have to give them your scanning key and then they could decide.
But there are better ways and we did an episode about it.
BIP 157 used to be called neutrino filters.
I don't know if anybody still uses that term.

Speaker 1: 00:23:35

Yeah, I mean, I think that was more of a marketing name on the lightning side.

Speaker 0: 00:23:38

But yeah, it's yeah, BIP 157 and BIP 158.

Speaker 2: 00:23:42

Yeah, which are we did an episode about it.
But the bottom line is you instead of telling somebody else what your addresses are, you ask them for sort of a summary of the block, a filter of the block, and you download these summaries, which are much shorter than blocks, And then based on that, you're able to calculate whether or not that block has any transaction that pays you.
Or at least guess.
You might be wrong in the sense that there can be false positives.
So once you think there's a transaction for you, you download the actual block.
And you're going to download slightly too many blocks.
But this is a nice way so that as a light client, you're only going to download a fraction of all the blocks to see if there's an intersection for you.
This can be used with silent payments, but it's just one of the ingredients.
You need to do more because this does not do the multiplication trick.

Speaker 1: 00:24:31

So maybe one thing to sort of start with for this conversation that's important to mention is what is even the definition of a light client?
And I think one useful definition that isn't really used today, but I think is important to highlight is that you somehow figure out whether or not you got paid without a full node doing all the work for you, right?
Because normally like-
Without your full node doing all the work for you.

Speaker 2: 00:24:58

Somebody else's full node will do it.

Speaker 1: 00:24:59

No, but That's what I mean, right?
Like I think connecting to a full node, whether or not that's yours, I think sort of defeats the purpose of a like client.
Obviously, if you connect to your full node, you will know whether or not you got paid.
Is that a like client?
Not really, I would say.

Speaker 2: 00:25:14

No, I would call that more like a remote control.

Speaker 1: 00:25:17

Exactly, but then like if that remote control full node is somebody else's, now suddenly it becomes a like client.
I don't think that makes a lot of sense actually.

Speaker 2: 00:25:24

No, then it becomes a trusted node.

Speaker 1: 00:25:26

Yes, but I think today when we talk about like clients, a lot of people call the connect to somebody else's node model, they call that a like client.
And I think that's a kind of a mistake or at least something which we should differentiate and we should say no if you connect to somebody else's full node and they do all the work as if it was your full node.
I don't think that really is what we want from a like client at least, or what we should call a like client.

Speaker 3: 00:25:52

In either case, in these cases, the silent payments thing is still easy.
The full node just does it and tells you what's going on.

Speaker 1: 00:25:58

Yes and no.

Speaker 2: 00:25:58

So the challenge- Not really, because you have this one extra calculation per block, per transaction that we talked about.
But if you're doing this on behalf of a million people, now for every block, you have 10, 000 transactions in the block, plus a million checks.
So that does not scale very well at all for this way of doing whatever you want to call it.

Speaker 3: 00:26:19

So are we going to try to solve this problem?

Speaker 0: 00:26:23

I would mention it is feasible, but the problem, and this is usually what spooks engineers, is that it scales linearly in the number of users.
So the more users are connecting to your node, the more work you have to do.
Now, because that work is roughly a signature check, if I'm a wallet provider and I'm running like some pretty nice hardware, this is feasible.
And I did some like back of the number math on it at some point.
And, you know, you could scale up to like 10 million users with, you know, Amazon hardware and whatnot.
But the, but the reason I don't think this is super interesting is those users are giving all of their privacy to that server.
It's the same as if you just handed your XPUB to a server and said, hey, just tell me when I get paid.
Now there are some models where I think users might wanna do this.

Speaker 2: 00:27:11

I mean, you're describing the norm, basically.

Speaker 0: 00:27:14

Yeah, I mean, that's basically how- We'd like to avoid that beside- Right, and so, but I wanna mention, I don't think that's really, it's not computationally infeasible.
I just don't think it's an interesting route to pursue or to even advocate for.

Speaker 1: 00:27:27

Yeah, and I think that goes into the second distinction I wanted to make, which is whether or not it's a likeline is one of them.
And the second one is whether or not you figuring out whether or not you got paid, whether you did that in a private way or not, right?
Because the non-private way is sort of simple.
Like you give someone an address and you just ask like, hey, did I get paid?
And they'll say yes or no.
Well, now you lose all your privacy.
And I think especially for a protocol like this, where privacy is sort of like a big point, it makes even less sense to sort of combine this with a wallet that is non-private.

Speaker 0: 00:28:02

Yeah.

Speaker 3: 00:28:02

So what problem are we gonna solve here, both?

Speaker 1: 00:28:04

Yeah, so we want to be able to figure out whether or not we got paid without having a full node do all the work for us and without losing our privacy.
Okay.
That is essentially what we want.
And one of the big components there that Shorst mentioned is BIP 157, BIP 158.
That is one component.
But the first thing we need to answer, the scanning question is how do we get a like client?
How do we get a phone to figure out, to do basically the equivalent of scanning without outsourcing it to somebody else and losing all their privacy?
And the answer to that is essentially that for every transaction in the Bitcoin blockchain, every silent payment eligible transaction, a full node or some kind of server can generate a single 33-byte value and send that to the like client.
And the like client can use that to generate what essentially would be the address if it was a payment for them.

Speaker 2: 00:29:08

So this 32 bytes per transaction is the same for everyone?
Just like the filters in BIP 158 are the same for everyone?

Speaker 0: 00:29:15

Correct.

Speaker 2: 00:29:15

So it's not a privacy sensitive thing.
You just ask it from any node, they'll give it to you.
They don't know anything about you other than that you're interested in silent payments.

Speaker 0: 00:29:23

Not only is it the same for everyone, it's also public information.
It's basically, so like clients don't have access to blocks or transactions.
So this 33 byte value is a summary of the input public keys of the transaction.
So it's the same information anybody would have just by looking at the blockchain.
And so we'll call it an indexing server.
An indexing server just sees transactions coming in.
It says, hey, could this be a silent payment?
If yes, let me sum up the inputs, store that 33 byte key in an index, and then any client that requests it, I'll just send them the 33 bytes that they need to complete that Diffie-Hellman operation.

Speaker 2: 00:29:59

Yeah, because remember, the whole way you figure out whether you get paid was to start with these inputs to look at them.

Speaker 3: 00:30:05

But this sounds to me like Lite clients would still be checking every transaction in a way.

Speaker 2: 00:30:12

Right.
Yes, but they're checking only 32 bytes for every transaction versus the whole transaction.
So a whole transaction might be 150 bytes, but this summary is only 32 bytes and you're only getting the summary for transactions that can be assigned in payment.
So you're getting not all the transactions in a block and you're getting not all of the transactions, not all of the transaction data.

Speaker 1: 00:30:33

And one important point here is that we can save a lot of bandwidth by discarding all the transactions where all the outputs were spent.
So the longer you wait, the more outputs are spent, the less data you have to download to actually check whether or not you got spent.

Speaker 2: 00:30:48

Assuming you keep track of what you've seen before, right?
So you're a light wallet, you have at some point detected a silent payment to you, you remember that for the next time you start the wallet, you say, okay, give me all the blocks, give me these summaries starting from block 100, 000 blocks ago.
And then it's going to say, well, you're not going to be interested, since you asked before, you're not going to be interested in anything that somebody else spent because that couldn't have been your coins.
So assuming you have a single wallet that's keeping track of what it's already asked.
Yeah, it can ask for a summary, this cut-through idea where anything that's already been spent was obviously not spent by you, so it wasn't sent to you.

Speaker 0: 00:31:25

And the cut-through has a really nice property here where the longer, so when you first hear this, the initial thought is the longer the Lite client stays offline, the more data they're going to have to download.
And this has been a problem, I think, in other Lite clients that do this downloading stuff.
If you leave it off for a month, well, now you need to download a month's worth of transactions, which is just not feasible.
With the cut through, the data that the light client needs to download kind of asymptotically approaches this constant value because the longer, and this is kind of an interesting property of Bitcoin, the UTXO set is split into what I would call like hot coins and cold coins.
UTXOs get created and never spent, or UTXOs get created and get spent within three days.
And that's kind of, there's not really much in between there.
So if a Lite client were to scan once every three days, they're skipping a whole lot of transactions that are just not relevant to them.
And this is, I think, the trick that we we realize actually makes light client scanning feasible.

Speaker 2: 00:32:23

The one trick they did not want you to know about.

Speaker 0: 00:32:26

Yeah, it's one trick.

Speaker 2: 00:32:27

And so once you have this list of these tweaks, you can now.
What you do is you use that 32 byte number, you multiply it or whatever it is with your own private key, your own silent payment private key, and then you know what address you should have been paid to.
So basically the result of this calculation is an address, and now you use the traditional PIP 158 filters to say, hey, is there a payment to this address?
And you would ask that for this subset of blocks, right?
So you might get slightly too many blocks.

Speaker 0: 00:33:03

Maybe take one step back.
You create what I would call potential public keys.
So you, you, you do an ECDH with each of these inputs, which means you create all these taproot outputs.
Now you need a way as the light client to know if any of these public keys exist in the UTXO set.
There are many ways you could do this.
One way would be just connect to an Electrum server or an address lookup server and just hammer them with like 2000 addresses and be like, hey, tell me if any of these exist in the UTXO set.
That's not private and it's also kind of a denial of service on the Electrum server.
So the much better way from a performance and privacy standpoint is to get some efficient summary of UTXOs in a block, which I think, you know, BIP-158 is the best example of that.
So you download these filters and you take these public keys and you test to exist whether or not they exist in the filter.
If they exist in the filter, that means that there's a UTXO corresponding to this and you know I'm the only person who would be able to create this UTXO.
So then you download the block and get it.
But I make that distinction there because if we think about, okay, now I have all these public keys and I need to know whether or not they exist, you could use any method for querying a UTXO set, whether that's address lookup, private information retrieval, BIP 158.
And I think BIP 158 is just the best example that we have right now.

Speaker 3: 00:34:23

Right, this sounds clever.
There's one part that's not really clear to me, but I sense that that's maybe more something If people want to know it, they'll have to read the BIP, which is how the calculation is actually done from these 33 bytes, like what is actually calculated there.
Is that something that audio will allow you to explain?
Or should we just refer people to the BIP?

Speaker 0: 00:34:45

No, I think it's really simple.
So a Bitcoin public key is usually serialized in what's called a compressed format.
So that's 33 bytes.
The first byte tells you whether it's an even or an odd point.
And then the next 32 bytes is an encoding of the X coordinate of the point.
So what the client does is it downloads these 33 bytes, which is a serialization of a public key.
It deserializes that public key into an actual point and then does the multiplication.

Speaker 2: 00:35:15

Right, then you're just multiplying your private key with this public key that you just found.
A point is a public key.

Speaker 3: 00:35:22

Okay, somewhat clear enough to me.
Last time, Sjoerds brought up something that he called the Hotel California problem.
Sjoerds, do you want to repeat what this problem is?

Speaker 2: 00:35:34

Yes.
I mean, yeah, so the idea is that because this is a little bit of extra work for every block that you want to scan, if you decide to have a signed-in payment address and you make it known to the world, you now need to do this extra work forever.
And so the question is, should there be a way to expire this thing?
And then, you know, we'll let Josie take over from here.

Speaker 3: 00:35:58

Josie, Ruben, is there a way to expire this thing?

Speaker 1: 00:36:00

Josie is most passionate about this.

Speaker 0: 00:36:02

Yeah, this is what I'm passionate about.
So, first of all, this problem is not unique to silent payments.
If I were to post a regular SegWit address somewhere on the internet, I now have to keep checking that address for eternity to make sure that I actually get payments.

Speaker 2: 00:36:23

But it doesn't need so much CPU power to boil the oceans.

Speaker 0: 00:36:27

I mean, it kind of does in a way, because with assuming that you got that from an XPub, you now have kind of this gap limit thing to worry about.
So I think it's a bit of a misconception that silent payments is like an order of magnitude more work for a full node.
I think any type of address scanning requires some amount of work and some amount of querying the UTXO set, which is an expensive operation.
So really what we have is kind of this like stale data problem, where if I post payment instructions in a public place, I should probably keep checking for them.
It was brought up with silent payments because then people kind of realized, oh, these are designed to be reused.
Because today, if I post an address somewhere, most people aren't going to use it.
Cause they're like, I don't really want to dox my payment to the whole world.
But I would argue that this is a problem that It really shouldn't be solved in the silent payments bit because now we have this scope creep where a silent payments the bit 352 is supposed to be a very you know Concrete proposal for doing this shared secret exchange for address generation and the bit should just be focused on that If we start throwing in like expiry times and other things, it's like, well, it's scope creep.
And then, you know, if we solve it in silent payments, but then the problem still exists for regular addresses and XPubs and all this other stuff, we didn't really fix the problem for Bitcoin.
So I would say, if people believe that expiry is what they want, we should write a new standard, a new BIP that applies to all forms of Bitcoin payment instructions.
You know, Bolt 12 invoices, sign the payment addresses, regular addresses, XPUBs. The second thing I would say, I don't think expiry is actually what you want here.
And I did a write up on the mailing list about this when the expiry time was first proposed and kind of listed my reasons why I think that expiry doesn't really get you what you want, and it's kind of an inferior solution.
What we really want is to be able to revoke something.
I've posted a piece of data that is now stale or bad.
I want to do something else now that communicates to everyone, hey, this data is revoked.
It's no longer good.
The problem is, and I think why people prefer expiry, revocation is really hard.
Like it's just a difficult problem.
But I think our energy would be better spent tackling the hard problem of revocation because that actually gets us what we want.
And I think that would be extremely useful.
If I could post an address and kind of, you know, just using the PGP analogy, because they have this concept of revocation.
I post this key somewhere, I sign it, and now any client that wants to read my silent payment address, they check the signature, and they see everything's good, and they generate the address.
If I lose my wallet, it gets hacked or I just don't wanna use that silent payment address anymore, I issue some sort of like revocation signature.
And then now when the client reads it, they check it, they say, oh, this signature has actually been revoked by this other one, I'm not gonna use it anymore.
And I think that's really the user experience that we're looking for.

Speaker 3: 00:39:19

But this is not implemented in this BIP.

Speaker 0: 00:39:22

It's not.

Speaker 3: 00:39:23

It might, it might be a different BIP at some point.

Speaker 0: 00:39:26

I think it should be its own BIP because then we could use that same method for, you know, everything.
everything.

Speaker 1: 00:39:30

The other thing is when we spoke last time, Ruben, there was some issue with CoinJoin.
Like this silent payment was not compatible with CoinJoin or something along these lines.
Is that...
First of all, can you maybe repeat or summarize the problem and Is that still a problem?

Speaker 2: 00:39:46

Yeah, so,

Speaker 3: 00:39:48

and the problem was more, so there was a solution and it's still the same solution, but essentially the problem is that you, whenever you making a payment with more than one person on the input side, So a coin join is essentially not just your inputs, but somebody else's inputs also go into the transaction.
And the way silent payments work is that you need all the keys from all the inputs.
And so now you have to collaborate with other...

Speaker 1: 00:40:16

You need all the private keys from all the inputs, right?

Speaker 3: 00:40:18

Yeah, you need to do some calculation with those private keys.
You don't necessarily need the private keys themselves.
But now you have other participants that have inputs.
And so you need them to collaborate with you in order to create a coin join to a silent payment output.
And in order to do that, there's a naive way of doing that, which basically means that you're giving up the person that you're paying.
You can say to the other CoinJoin participants, hey, I want to pay this person, please help me out.
But if you do that, then now you're revealing to them who you're paying and you don't want that in a CoinJoin because CoinJoin's primarily-

Speaker 2: 00:40:59

Right, Might be useful here also to distinguish a simple multi, a collaborative transaction with say your friends where you, two of your friends are combining their, well, I guess it's three things.
One, you could have a multi-sig.
With a multi-sig, you are spending one coin, but the key is spread between three people.
So none of these people would have the private key for it.
But I think for a typical multi-sig, you're just adding up all the public keys in the multi-sig.
Right, so that problem is kind of solved.
Like it just says, I'm spending this coin, it's a multi-sig, you have three public keys.
Everyone says their own signature, and then the recipient adds up those individual public keys.
If you do something like Schnorr, where the signature is combined, you don't.
So there you already have a problem, maybe, or not.
So there are a couple of things here.

Speaker 3: 00:41:48

I would say mostly it's about collaborative transactions where there are multiple participants that have some of the keys that are relevant to creating the shared secrets.

Speaker 2: 00:41:59

Yeah, but in one scenario, you're fine with the other participants knowing that you're making a silent payment.
And in Coinjoins, you're not fine with that.

Speaker 3: 00:42:07

But even if you just know, because there's another problem, there is, are you fine or not with them knowing who you're paying?
And the second question is, are you certain that the data that they gave you is correct?
Because the very naive way would be for them to give you your private key, but that sort of defeats the purpose of multisig.
Yeah, so we're not doing that.

Speaker 2: 00:42:28

In a coin join, yeah, you can just rug them.
So yeah, that would be bad.
Yeah, because the problem is, of course, especially in an untrusted situation, but even in a situation where there might be bugs on the other side, you are paying somebody to sign a payment address, but that's not a Bitcoin address.
So whatever Bitcoin address you're seeing on your screen, the wallet's saying, I'm about to send to this Bitcoin address, trust me, it follows from the sign-on payment protocol.
It might not if the other participants do something wrong.
So you want to be able to check.

Speaker 3: 00:42:55

And this is even a problem on the side of hardware wallets, where the hardware wallet might malfunction or there might be some kind of issue, maybe a bit has flipped somewhere and the calculation that your hardware wallet did was actually incorrect.
You would want the software side to be able to verify what the hardware wallet did and make sure that it's done correctly.

Speaker 2: 00:43:15

So there are a bunch of cases.

Speaker 0: 00:43:17

Oh, yeah.

Speaker 2: 00:43:18

I'll just do one summary here.
When you're making a payment using a hardware wallet, you are the only participant.
It's just you, but it's really you and your hardware wallet.
Yes.
And normally, you know, you look at your screen, your wallet says, I'm going to send the money to this and this address, and then the hardware wallet confirms, do you want to send to this in this address and you're good but the problem with sign-on payment is you don't know what the address is going to be because it involves the shared secret and therefore you need your own private key to figure out what the address is.
But that address is, that private key is on the hardware wallet.
So in order to know what address you're going to send to, you need to ask the hardware wallet, hey, this is the sign-on payment address of the person I'm about to send money to, tell me what the address is, and then you just have to kind of trust the hardware wallet.

Speaker 3: 00:44:02

Well, hopefully not.
So this is what you solved.
Yeah, so there is a way to actually basically do an extra calculation when you're generating the silent payment address.
And this is called a discrete log equivalence proof.
And basically it shows that the calculation that you did, the shared secret that you generated was correctly generated.
So despite not having access to the private key, you get the result of the shared secret.
And so basically it's like not knowing any of the private keys, but still being able to validate that the shared secret was generated correctly.
And with this you can actually verify that what you received was correct.

Speaker 2: 00:44:44

And this is five pages of moon math?

Speaker 3: 00:44:46

No, This is relatively simple.
It's basically a Schnorr signature plus some small changes to that kind of algorithm.

Speaker 2: 00:44:56

And this fixes hardware wallets, coin joints, everything.

Speaker 3: 00:45:00

This fixes one aspect.
This fixes the aspect of did the share secret that I receive from the party who has access to the private key, is this the correct share secret, yes or no?
And so the second problem, the one I mentioned before, is the one of privacy.
How can you do this without revealing to the person who generates the share secret, without revealing to them who you are paying?
And that requires what is essentially called a blind Diffie-Hellman.

Speaker 2: 00:45:30

So it reveals that you're about to do a silent payment, but not to which public key, to which silent payment address.

Speaker 3: 00:45:36

And you could even like, if you care about that, you can even go as far as to like pretend that you're making a silent payments as to throw them off whether or not you're making a silent payment.
So even that doesn't have to be revealed.
But yes, essentially, they know you're trying to make a silent payment, but they still don't know who you're paying because you're asking to generate a shared secret on data that's blinded.
And then the person who wanted that shared secret can then unblind that result and use it in the payment.
And so this essentially sort of completes the loop of how can we get to the point where we can do a CoinJoin, know everything went correctly and not leak any additional privacy over a regular coin.

Speaker 2: 00:46:19

Yeah, and I guess, yeah, in the CoinJoin protocol, Hugh, you'd say this is a CoinJoin protocol that is compatible with silent payments, and then just everybody signs this stuff so nobody knows if there's actually a silent payment.
So even if I were to look at, you know, I'm the NSA, I know every silent payment address out there because I watch the internet, I still could not like go back and see if it matches any of them.

Speaker 0: 00:46:40

Correct.
I think that's a really cool part where it's kind of, it feels kind of magical where, So in order to coordinate with these other participants in a coin join, you would need to give them the public key that you want them to do this ECDH with.
And as soon as they have that public key, well, they kind of know who you're trying to pay.
They know what silent payment address it is.
So the fact that you can, one, blind that public key, have them do an ECDH with it where they don't know what they're actually doing ECDH on, and then also have them give you a proof that they did it correctly for the thing that they didn't even know.
It's pretty cool.
And when you look at the math, it's not even really moon math.
It's quite simple.
And, you know, if people are interested in digging into it more, this came up, this idea of formalizing the discrete log equivalency proof came up in the PSBT BIP draft that we're working on.
And then I think now it's gonna be its own BIP where someone suggested, hey, this discrete log equivalency stuff seems generally useful.
We should probably have a separate BIP for it.

Speaker 3: 00:47:38

Yeah.
Makes a lot of sense to me.

Speaker 1: 00:47:41

It's moon math to me, Josie.
I can tell you that much.

Speaker 0: 00:47:44

It's addition and subtraction, maybe.

Speaker 2: 00:47:46

It's yeah, It's just manipulating bits.

Speaker 3: 00:47:49

There are no additional assumptions over what we already have for snore signatures.
So it really is, in that sense, there's nothing like, oh, this is like unproven math or something like that.

Speaker 2: 00:48:01

It's pretty straightforward.
Okay, last topic.

Speaker 1: 00:48:06

This is a new feature since we discussed this last time.
So you added a concept called labels.
You added labels.
What do labels do?

Speaker 3: 00:48:15

Yeah, so that's another interesting one to discuss And one that I didn't think of until after we did the podcast, I think probably pretty brief, pretty shortly after that, but essentially minutes after,
not quite that fast, I think, but, essentially, you know, in the discussions, silent payments are very privacy focused, but there are scenarios where you actually want less privacy.
And so with silent payments, you actually have a case where whenever when somebody sends you money repeatedly, you don't know the same person was sending you money multiple times.
And that is a feature, right?
You as the sender, you might not want the recipient even to know that you're sending repeated payments to them.
And that also helps in the case where the recipients maybe, you know, they go to jail or they have to reveal to the government certain amounts of data.
And now the government knows that you sent them multiple payments or something like that.

Speaker 2: 00:49:16

You have a donation address on your website.
You get random donations all the time.
You have no idea whether that's coming from one person or from 25 people.
Yes.
When you go to jail, you give the private keys to the police because they've been torturing you for seven days of not giving you coffee.
And then I'm sure they'll give you coffee.
But somehow you still surrender your private keys and they still don't know where those donations are coming from.

Speaker 0: 00:49:42

Yeah.
And this is unique to silent payments.
I think this is a really, really cool property where in the world of anonymous donations or like adversarial donations, let's say I want to make a monthly donation to an organization like Wikileaks.
From Wikileaks' perspective, they would just see 12 payments and they would have no idea that those 12 payments came from one person or 12 people or whatever.

Speaker 2: 00:50:01

With the caveat that these payments might, you know, you do some cluster analysis on them.
So there's still some of that, but at least it's not like, I gave this address to this person.

Speaker 0: 00:50:11

Well, let me give a more specific example.
If I had an XPub or something like that, or BIT47, for example, BIT47 establishes this payment channel, And so any payment made through that payment channel is clustered already.
You don't need to do any chain analysis stuff.

Speaker 1: 00:50:29

From the same.

Speaker 0: 00:50:30

Exactly.
Yeah.
And, and like Ruben said, there are use cases where you, you do want that, but I don't think that a protocol like silent payment should have that by default.
So by default, you're starting with the best center privacy possible.
Every transaction is unique and not correlatable to any other transaction.

Speaker 2: 00:50:47

But now let's say I am an exchange and I have, I don't wanna scan a million keys.
I don't wanna scan, I don't wanna have one silent payment address per customer because now I have to, you know, I have millions of customers and we just did the math on how many computer resources you need.
And exchanges, you know, can't afford computers.
Well, they can, they can run Ethereum notes, they can definitely run this.
True.
However...

Speaker 3: 00:51:08

They're outsourced Ethereum notes so who knows but yeah.
Jobs fired.

Speaker 2: 00:51:12

Yeah so it would be nice if they could have one, still one single payment identifier, no just one silent payment address and then they give each customer a variation on it so that they know which deposit is coming from each customer because as an exchange, it's quite useful to know which account you want to credit when that payment comes in, Pretty useful.
And this is what labels do.

Speaker 1: 00:51:32

Okay, so it's still the same silent address.

Speaker 2: 00:51:36

It's not the same silent address.
One of the keys is the same.
The spending key, so the key you need to spend money is the same.

Speaker 0: 00:51:42

The scan key is the same.

Speaker 2: 00:51:44

Oh, You should explain it.

Speaker 3: 00:51:47

I mean, it's not a big mistake.

Speaker 2: 00:51:48

One of the keys is the same, the other one is different for each customer.
That means that in terms of scanning, it's not that much extra work.
It's a little bit of extra work, but it's not like one of those elliptic curve math operations.
It's a cheaper operation.
Like an elliptic curve math is like, you know, you have to write a whole, you have to copy the whole Bible, whereas the, just the simpler operations, like you write one sentence.
And therefore you can tell which customer is making which deposit.
So you give every customer a different silent payment address, they can very obviously see that it's the same entity.

Speaker 0: 00:52:23

Yeah, because they all have the same scan key in common.

Speaker 1: 00:52:25

Hang on, I was promised labels, now I'm just hearing different addresses.
What's a label then?
It's just different address.

Speaker 0: 00:52:34

Yeah, So it's a way of tweaking with elliptic curve math.
It's a way of tweaking one half of the silent payment address such that when you receive a silent payment and you're scanning, you know which address that payment was made to without needing to do an ECDH per address.
So you do one ECDH with the scan key, which is the expensive part, and then you kind of have this database of all the labels you've used and you do a quick lookup.
And then you say, ah, okay, this particular payment was made to this label that I handed to Shores.
So now I know Shores made a payment to me.
And I think the Exchange is the most obvious use case here where, You know, going back to what I said earlier, we don't want the amount of work that the exchange needs to do to scale linearly with the customers.
An exchange has 100 million customers, I don't want to do X work times 100 million.
So, the labels is this really cool way where I still, I do a constant amount of work, no matter how many customers there are, but I do have a way of figuring out, okay, Shor's just made a deposit to his account.
And I think the exchange one is obvious, but also like payments, right?
I want to get paid in Bitcoin.
And so I post my silent payment address on my Twitter for people who want to send donations, but then I also give a labeled version of that same silent payment address to whoever's paying me.
And now I have a way of knowing, ah, this particular payment was actually my paycheck.
And this other one was a donation from my Twitter account.

Speaker 2: 00:54:03

Right.
Be nice if those amounts were the same.
It would be nice.
And just to...

Speaker 1: 00:54:08

So at the start of the episode, we mentioned a silent address basically has two public keys embedded.
Just to be clear, So one of the public keys is just switched for a different public key or not?

Speaker 0: 00:54:19

Yeah, it is.
I mean, it functionally is.

Speaker 1: 00:54:21

One is the same, one is different?

Speaker 0: 00:54:22

One is the same and then one is different.
And the way that it's different is you take that spend key and then you add the label tweak to the spend key.

Speaker 2: 00:54:30

And this brings up an interesting possibility as well for security.
If you are like a famous exchange, key, not the address, because the address is different for every customer, but there's one key that's the same for all customers.
You make that well known to the world, and hopefully some hardware manufacturers or other wallet makers are nice enough to just put that into their software as a sort of an identity key.
So then when you're making a payment, it will literally say, are you sure you want to pay to name of exchange?
Which is kind of cool.

Speaker 0: 00:54:57

It's really cool.
And what's even cooler is because we're dealing with public keys here, the exchange can provide a signature.
And like hardware wallets can trustlessly verify, this is actually the destination that I'm intending to pay.
And so this is where, you know, the silent payment address can kind of be this persistent trustless identity, which plays really nicely into this use case for exchanges, but also BIP, what is it, 353 now, which is like human readable payment instructions where you could have like a username that has an underlying sign up payment address And because we're dealing with public keys here, there's just a lot more trustlessness, but with better UX that we get.

Speaker 1: 00:55:37

Okay, I think it's time to start wrapping up this episode.

Speaker 2: 00:55:40

I think you're right.

Speaker 1: 00:55:40

So about a month ago, the BIP was finalized, roughly.
What does that mean right now?
Are there wallets that have implemented, has BitHook or implemented it yet, Shorz?

Speaker 2: 00:55:52

There are open pull requests in various states of completion that need work.

Speaker 1: 00:55:58

Is it coming?
The answer is no, But it might come.

Speaker 0: 00:56:01

I think there's a lot of conceptual buy-in for it.
That was one of the things that I think we did well in the beginning of silent payments is we talked to a lot of people to be like, are we barking up the right tree?
Is this a good idea?
And so I think so far everyone's been pretty positive about it.
We've got the Bitcoin Core PRs open.
The reason that those aren't making progress right now is they're waiting on an upstream PR to LibSecP, which is the cryptography library that we use in Bitcoin Core.
And so I'm working on a PR right now with another contributor where we're creating a silent payments module in LibSec-P that is super fast, super optimized, super safe.
And so that PR is open right now and waiting for review.
Again, like pretty strong conceptual buy-in.
So I feel confident that it'll get merged eventually.

Speaker 2: 00:56:50

We have an episode about LibSecP.

Speaker 0: 00:56:53

Yeah, it's an amazing project.

Speaker 1: 00:56:55

Episode 2, I think, Josh.

Speaker 2: 00:56:57

It could be, yeah, LibSecP256k1.

Speaker 0: 00:57:01

Yep.
So once that PR merges, now we have all the cryptography for the protocol.
We'll use that in Bitcoin Core and then the Bitcoin Core PRs can make progress.
And also any hardware wallet, mobile wallet, whatever, can also reuse this LibSecP module.
And the nice thing here is we're not making anybody roll their own crypto.
Like, here's a module that does the cryptography part of silent payments.
You don't need to worry about it.
Treat it like a black box.
So that's kind of the state of things right now.
There are wallets who have started implementing it without that.
Cake Wallet, I think, was the first one to have a full-like client.
So they have a fully private-like client that doesn't use Bit.158.
They do a little bit of a different technique.
But they don't have silent payments send and receive.
Last week Blue Wallet merged send support so now in Blue Wallet you can send to a silent payment address.
There's donation wallet which I've been working with a group on which is a BIP 158 style client.
That one is still in testing, like in Cignet.

Speaker 1: 00:58:06

The name of the wallet is donation wallet.

Speaker 2: 00:58:08

Yeah.
Yeah.

Speaker 0: 00:58:09

It was kind of like, it's supposed to be like the flagship use case of silent payments as donations.
And then there's been interest from other wallets as well, but I think people are waiting on the LibSecP module, because once the LibSecP module is there, then it can get into BDK.
Once it's in BDK, it becomes easier for, you know, etc.

Speaker 2: 00:58:26

The BDK is the Bitcoin Development Kit.
It's a Rust library.

Speaker 0: 00:58:29

Yep, it's a Rust library that would then be able to wrap the libsecp.
So there's a lot of discussions happening in these different repos and where people are kind of waiting for the right ordering of things.
Another big one for wallet support, at least on the sending side, is people want to have a PSPT spec.
So we mentioned that earlier, but we've got a post on DelvingBitcoin where we've been talking through a draft proposal for PSPTs. So for me, it's been really exciting to see the enthusiasm where people are just, you know, just excited.
ready to jump in and start building.
But then it's also nice to see the tooling mature as well, because.
For this to be widely adopted.
We want PSBT support.
We want like clear specs of how to do everything safely.

Speaker 1: 00:59:11

Oh yeah.
Two weeks.
How many people are using this?
What, What does the blockchain say?

Speaker 0: 00:59:18

Well, that's the nice part.
We don't know.

Speaker 2: 00:59:22

Maybe it's been in use for years and you just don't know it.

Speaker 0: 00:59:25

Maybe Ruben is just now telling everybody about it, but he's been silent on this for years.

Speaker 2: 00:59:29

Silently getting paid.
But I mean, just one thing to add here, I think, so since the BIP is final, this is really the time for any developers out there to jump in, start working on it.
Yes, we're still sort of like on the, you know, on the side of libraries, There's still a lot of work to be done, but definitely I think this is a time to start implementing it into wallets.
There's the Keystone hardware wallet that's looking into it now as well.
And sending support is the thing we really want all the wallets out there to support because once all the wallets support sending then it's easy for people to start using their silent payment address and know that they can actually get paid and sending support is relatively simple compared to receiving because receiving requires scanning sending does not So that's a little something I wanted to put out there.
Right.

Speaker 1: 01:00:23

Sure, we good?
I think so.
So thanks Ruben and Josie for coming by and explaining all these things.
And dear listeners thank you for listening to Bitcoin Explained.

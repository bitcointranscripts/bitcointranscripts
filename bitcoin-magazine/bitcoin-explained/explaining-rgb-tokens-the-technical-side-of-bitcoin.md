---
title: "Explaining RGB Tokens - The Technical Side of Bitcoin"
transcript_by: AV7OM471K via review.btctranscripts.com
media: https://www.youtube.com/watch?v=JoGYnAS_j0g
tags: ["rgb","layer-2","lightning","sidechains"]
speakers: ["Sjors Provoost","Aaron Van Wirdum","Ruben Somsen"]
categories: ["Developer-Tools"]
date: 2021-03-26
---

# Title: Explaining RGB Tokens - The Van Wirdum Sjorsnado - The Technical Side of Bitcoin
Media: https://www.youtube.com/watch?v=JoGYnAS_j0g





## Sponsor of the Show - Bitcoin 2021 Conference
Aaron Van Wirdum: 00:00:00
Before the show, a quick word from our sponsor.

Sponsor (CK): 00:00:04
What is up Bitcoiners?
It's CK and I'm here to talk to you about the Bitcoin 2021 conference this June in sunny Miami, Florida.
It is going to be June 4th and 5th and we are barreling towards a sold out conference.
Already one third of our available tickets have been sold and way more than half of our whale passes have been sold.
We are almost sold out completely on the whale pass.
We have amazing speakers, Jack Dorsey, Chamath, Nick Szabo, Tony Hawk, Peter Todd, many, many more and many more to be announced.
You can go to the website to check them all out.
Mayor Suarez has welcomed us into the city with open arms and again, tickets are flying off the shelves.
Seriously, I see the feed and like I've done many conferences.
This one really has something going for it.
And honestly, guys, like, after all this, after 2020, Bitcoiners wanna grab a beer, hang out.
We're bringing back Bitcoin 2019 vibes times 10, prices times 10, let's go.
Use promo code SATOSHI, all caps, SATOSHI for 10% off, you can go to the website b.tc/conference.
Again, that is b.tc/conference and get your ticket today.
Today, prices also are going up and hey, we may just sell out.
So we have a hard cap.
Can't really be flexible there.
Don't wait.





## The Van Wirdum Sjorsnado show begins 
Aaron Van Wirdum: 00:01:45
Live, from Utrecht, this is The Van Wirdum Sjorsnado.
Hello.

Ruben Somsen: 00:01:48
Hello.

Sjors Provoost: 00:01:49
Hey, who's there?

Ruben Somsen: 00:01:51
It's another Dutch guy.

Sjors Provoost: 00:01:53
Welcome to the show, Ruben.

Ruben Somsen: 00:01:54
Thank you.

Aaron Van Wirdum: 00:01:56
Welcome back Ruben.
Ruben, did you start selling your tweets yet?

Ruben Somsen: 00:01:59
I tried to sell one of my tweets to my sister but she said, "What the hell are you doing?" and then she just laughed at me, so I failed.

Sjors Provoost: 00:02:06
Yeah, which rule of acquisition is it, exploitation begins at home?

Ruben Somsen: 00:02:10
Yeah exactly I mean families who you gotta exploit first right?

Aaron Van Wirdum: 00:02:15
Sjors, did you make any good deals?

Sjors Provoost: 00:02:17
Uh, no.

Aaron Van Wirdum: 00:02:19
We are actually gonna discuss NFTs today.

Sjors Provoost: 00:02:21
I have been making some really bad price predictions because I hope those tweets will become worth a lot.

Aaron Van Wirdum: 00:02:25
Bad price predictions?

Sjors Provoost: 00:02:26
Yeah, bad takes usually make more money than good takes.

Aaron Van Wirdum: 00:02:29
Ah, I didn't know that.
That's a good tip.
Pro tip.
But anyways, we are kind of discussing NFTs today, aren't we?

Sjors Provoost: 00:02:35
Yes, we are.

Aaron Van Wirdum: 00:02:36
Not exactly, but partly.

Sjors Provoost: 00:02:39
Very exactly, amongst other things.

Aaron Van Wirdum: 00:02:42
Yeah.
RGB, that's what it's called, right?

Sjors Provoost: 00:02:45
That's right.

Aaron Van Wirdum: 00:02:47
Jogged my memory there.
What does it stand for, guys?
RGB?

Sjors Provoost: 00:02:50
Well, I think it's just a reference to the color scheme - Red, Green, Blue.
But it doesn't actually mean anything in the context that we're going to talk about it.
It's just the letters.

Ruben Somsen: 00:02:59
Yeah.
And I think it's because...

Sjors Provoost: 00:03:00
Unless they made it a backronym, I don't know.

Ruben Somsen: 00:03:02
...no, no, I don't think there's an acronym.
It's referring to colored coins, right?
So the colored coin idea of having other coins on the Bitcoin blockchain, the word color, RGB, that's how it's connected.

Aaron Van Wirdum: 00:03:13
Clever.
I didn't know that.
Okay, so we're gonna discuss RGB tokens today.
Wait, is it RGB?

Sjors Provoost: 00:03:21
The RGB System.

Aaron Van Wirdum: 00:03:22
The RGB System.
Yeah.
Okay, where do we start?
Ruben?

Ruben Somsen: 00:03:25
Well, that's a good question.
I think we should start with…
A very, very long time ago in a blockchain far away.
It was really, really, really cheap to make transactions and people thought they could put everything on the blockchain.
For example, the Bitcoin PDF - the Bitcoin Whitepaper, is on the blockchain in its entirety.
And this was done in a very, very, very inefficient way, which is by creating fake transactions.
And in those fake transactions, you're not spending to real other people, to real addresses.
You're creating fake addresses that you can actually interpret and then you can reconstruct a file from it.
So this would be, for example, Multisig addresses.

Aaron Van Wirdum: 00:04:07
Yeah, so the idea is that addresses, as our listeners will probably know, they're just a bunch of numbers and letters.
They're effectively a number in the end.
And you're manipulating these addresses, you're just creating addresses.
Even though you don't have the private key, you're sending some coins to these
And a special software can interpret these numbers and turn them into whatever data you want.

Sjors Provoost: 00:04:33
Pretty much. So we addressed addresses in an earlier episode, but in this case, the thing you're sending to wouldn't even be an address.
It's a script that you put directly in the output of a transaction, and that gives you a lot of space to put stuff in.
The technicalities don't really matter.
But exactly, there is no private key with which to spend these coins.
Because the public key, or even the hash of the public key, was generated as if it wasn't really a public key.
It was just a series of bytes that look like a public key, but actually just contain the contents of a file.
And this means that money is un-spendable, which is very annoying.
And the reason for that is that we have this thing called the UTXO set.
The UTXO set is the set of coins that exist on the blockchain that can be spent by anyone and nodes keep that in RAM.
So when a new block comes in, the node will check whether or not it's spending money that actually exists.
And this check is done using the UTXO set, which generally is kept in RAM, could be 10 gigabytes.
And so it's very annoying when there's something in that blob of memory that everybody needs to keep track of.
Something that has no meaning, that can never be spent because the node doesn't know it can't be spent.
The node just thinks anytime somebody could spend this, even though we know, no, it's the Bitcoin PDF, you can't spend it.

Aaron Van Wirdum: 00:05:54
Yeah, so what you're saying so far is that people were using, basically abusing the Bitcoin system in a way.
They were manipulating addresses and sending coins to these addresses, not a lot, but just some coins to have these addresses on the blockchain.
This translated into data that could be images or the Bitcoin Whitepaper or other pieces of text or memes or whatever people felt like they were uploading.
And because normal Bitcoin software can't really tell the difference, normal Bitcoin software just sees addresses.
So now all these normal Bitcoin nodes like mine and yours and all our listeners' who are running Bitcoin nodes.
All these normal Bitcoin nodes actually have to check if they have to check the coins on these addresses.
Am I saying that right?

Sjors Provoost: 00:06:36
They have to keep those addresses in mind.
So there's two things that happen...

Aaron Van Wirdum: 00:06:39
Right?

Sjors Provoost: 00:06:39
...because these things were put in the blockchain, well, you have to download the blockchain.
So that's just wasted bandwidth for downloading, but that's not too bad.
The problem is that it has to be interpreted as potentially valid coins.
And as an optimization, you want to keep in memory those coins that could potentially be spent and there's no way to drop them from memory.

Ruben Somsen: 00:06:58
Yeah.

Sjors Provoost: 00:06:58
At least there wasn't.

Ruben Somsen: 00:06:59
So the problem is that you think they are spendable as a regular full node, but actually they are not.
But there's no way of knowing, other than kind of externally figuring out, that this is just a Whitepaper.
But, you know-

Sjors Provoost: 00:07:12
Yeah, but you couldn't add that to the node, right?
If, say, we made a change to the Bitcoin Core assets...
You know what? We know that's the Whitepaper. Let's just skip those coins.

Ruben Somsen: 00:07:22
I guess theoretically you could throw it out of UTXO sets if you're certain they're un-spendable.

Sjors Provoost: 00:07:27
That's the problem.
If you're certain, what if some really really smart alien actually made it look like it's just the Whitepaper!
But no no no, it's really there are private keys for it and one day this alien tries to spend the Whitepaper...
...and we accidentally soft fork those coins out of existence and this alien gets really angry because he's like, "Hey, you can't just confiscate my money!"

Ruben Somsen: 00:07:48
That sounds like an ECDSA break, but I'm not sure.
Depends on, I guess, how it's done.

Sjors Provoost: 00:07:53
Maybe the person who created the Whitepaper actually generated lots of public keys from private keys...
...and then reordered them in such a way that it created a readable Whitepaper.

Ruben Somsen: 00:08:05
Oh yeah.

Sjors Provoost: 00:08:06
I don't think that's even practical.

Ruben Somsen: 00:08:07
No, but to your point, maybe there is a way in which it is actually valid and we can't be 100% certain.
But one thing I wanted to add-

Aaron Van Wirdum: 00:08:14
There's also a thing of where do you draw the line because we do have vanity addresses and you can sort of use those as well to create stuff...
...and where, at what point are you sure it's a vanity address and at what point (trails off)

Sjors Provoost: 00:08:26
Well, that would be absolutely unacceptable.
The idea that you can't just decide what is vanity and what should be thrown away.

Aaron Van Wirdum: 00:08:33
That's my point, I agree.

Sjors Provoost: 00:08:35
But if you could mathematically prove that a coin cannot be spent, like theoretically impossible to be spent, then you could have that discussion.
But the problem is we can't really prove that.

Ruben Somsen: 00:08:45
Yeah, but yeah, so one thing that I wanted to add is that it is actually important, that if you want to put data on the Bitcoin blockchain, it needs to be a valid transaction.
So you can't just, that's why we're talking about these addresses, right?
Because you can't just take the Bitcoin Whitepaper, just put it there and just be like, "Hey, please put this in the blockchain!"
No! You need to do it in a format that the blockchain recognizes and that's how you end up with these addresses.

Sjors Provoost: 00:09:09
Yeah okay.

Aaron Van Wirdum: 00:09:11
Yeah okay so that was the original problem - people were just bloating the blockchain with all sorts of nonsense.
Nonsense that most of us don't care about and we still need to all validate it and store it or whatever.
That needs to be solved, Sjors.
How do we solve that?





## What is OP_RETURN?
Sjors Provoost: 00:09:26
Well this was solved many many years ago using something called OP_RETURN.
And the idea of OP_RETURN is that you create a transaction that spends coins.
And then it produces a "coin", which has the instruction OP_RETURN and then it's followed by whatever text you want to put on the blockchain.
And now when a full node sees this it knows, okay, if it starts with OP_RETURN, this coin is not spendable.
Therefore, yeah, this coin is not spendable so I can forget about it.
I do not have to put this in my RAM, I don't have to remember this.
And the idea there was, that it was kind of a compromise.
Well, people are going to put spam on the blockchain, whether we like it or not.
Let's at least reduce the amount of damage they're doing and make sure they pay a reasonable fee for it as well.
So there are some restrictions on the size of OP_RETURN to make sure that it's not too cheap to use it, but it is also cheaper than just spamming a blockchain.

Aaron Van Wirdum: 00:10:21
Right.
So I guess we're still sort of unhappy about it, but if people are going to do it anyways, then this is the least damaging way of doing it.

Sjors Provoost: 00:10:28
Yeah, this at least pays fees when you do this and nodes only have to download it.
But they can throw it away they don't have to remember it so the resource use is, the resource wasting is just a little bit of bandwidth.
And one off CPU but it's not wasting people's RAM and RAM is probably one of the more scarce resources.
So it's fine, it can't be done any better.

Ruben Somsen: 00:10:51
Yeah, so the main thing is it doesn't enter the UTXO sets and therefore it is a lot better than the previous solution.

Aaron Van Wirdum: 00:10:58
So how much data fits into one of these OP_RETURNs?

Sjors Provoost: 00:11:03
80 bytes.

Ruben Somsen: 00:11:04
Yes and no, because I think that's not a consensus rule, that's just a propagation rule.
So I believe it's actually valid to create one with more data, but then it won't be propagated.
So yeah, practically speaking, you're right.

Aaron Van Wirdum: 00:11:20
But....can we do better?
Can we compress it somehow?

Sjors Provoost: 00:11:23
Yeah we could, no well I mean I think I know where you want to go towards the so-called Merkle tree.

Aaron Van Wirdum: 00:11:29
Yes please.

Sjors Provoost: 00:11:30
But I think we want to go somewhere else first, because we can talk about the kind of fun things you can put in OP_RETURN and then have meaning without actually compressing it.
So we'll get to the compression part later.
So let's say you really like Rare Pepe.

Ruben Somsen: 00:11:48
I know I do.

Sjors Provoost: 00:11:49
So Rare Pepe was a trading card system on the blockchain and the way it worked is you could have a card and then you could offer it for sale.
And somebody could buy it and then that other people would have the card and they could sell it, etc.

Aaron Van Wirdum: 00:12:04
Yeah, when you say card you mean image?
It's a digital image?

Sjors Provoost: 00:12:10
Yes, but in this case it's important to note that the image is not on the blockchain.
There's a reference to the image on the blockchain, the hash of the image.
So I wouldn't still not call that compression, but I would say like you're not spamming the blockchain with the entire image.

Aaron Van Wirdum: 00:12:24
Sjors, explain this to someone who's new because it sounds like it makes no sense at all.
You have an image and then you have a hash and they have it on the blockchain.
Why should people care about the hash or the image or any of this?

Sjors Provoost: 00:12:36
Well, this is exactly what's going on with the NFT hype nowadays.

Aaron Van Wirdum: 00:12:39
That's why I'm asking.

Sjors Provoost: 00:12:41
So I would say there's no reason to care about this, but people were doing it.
So we just have to sort of explain at least what they were doing.
And so what you would do is you would have this image somewhere, maybe on a web server, or maybe on your own computer.
And so everybody would have access to this image because it's just data.
But the question is who really owns the image from whatever that means right whatever it means to own the image

Aaron Van Wirdum: 00:13:05
That sounds like an important question though, "What does that mean?", but go on.

Sjors Provoost: 00:13:09
I think it meant absolutely nothing but the way it was done was...
...everybody would have the image and you could take the hash of the image and then the hash of the image would be on the blockchain. And so-

Aaron Van Wirdum: 00:13:21
Let me give you an example where I think it might possibly make sense.
If you're playing something, I've never played this, but you've got something like Magic the Gathering.
If you'd want to make that into a digital version, then you could somehow prove that you own a specific card if you want to play it against another player.
If it's just an image, then everyone would have all the cards all the time. So now if you use-

Sjors Provoost: 00:13:46
Well, that's the idea.
You prove that you have the image of whatever "having" means.

Aaron Van Wirdum: 00:13:50
Right.

Sjors Provoost: 00:13:51
But at least if everybody agrees on the rules, then you can do that.

Aaron Van Wirdum: 00:13:54
Right.
So, yeah.
So within some contexts, it might actually make some sense.

Ruben Somsen: 00:13:58
Yeah.
I mean, I think it does make sense in some limited contexts.
But the main thing is, is there going to be some kind of person who controls the NFT, right?
If somebody issued it or they can issue more of it, then it becomes kind of questionable.
But if it's like a one-time thing, like maybe somebody made a card game and it's just...
...it's kind of like a full node where you download the software's open source and then the software interprets the NFTs.
And as long as everybody kind of agrees on the card game and the NFTs, then you have a card game, like you said, with cards that are actually rare.
But anyone can just take the same game and play it for free, right?
So that's always inevitable.

Sjors Provoost: 00:14:40
Which is pretty much how this counterparty/Rare Pepe system worked, as far as I know.
So basically, you would put on the blockchain, the hash of the image, probably.
And then you would say, well, I'm now transferring this to this other person by just sending them coins essentially.
And then whoever has the private key of where you sent the card is now the new owner.
And so you would have a piece of software that would read the blockchain and would see okay this card is now moved to this other person and it's moved again.

Aaron Van Wirdum: 00:15:07
Yeah I want to take a small step back, and Ruben, this is also something you wanted to discuss.
It is the idea of colored coins, so we already mentioned it in the beginning of the episode.

Ruben Somsen: 00:15:16
Yeah.

Aaron Van Wirdum: 00:15:17
So the idea of, Ruben, colored coins, can you explain what colored coins are and then we'll move on, then we'll move back to NFTs.

Ruben Somsen: 00:15:24
Yeah, so, well, it is very similar because a NFT is a colored coin of one, basically.
So it really is just the issuance of an asset.
The name colored coin has been kind of what's been used I think it's been maybe counterparty was the first or-

Sjors Provoost: 00:15:42
No, counterparty is not a colored coin.

Aaron Van Wirdum: 00:15:43
Colored coins predate counterparty.

Ruben Somsen: 00:15:45
Yeah, there's “Master Coin”, I don't know, but...

Sjors Provoost: 00:15:48
I can give you an example of a colored coin, if you want, but first explain how it works.

Ruben Somsen: 00:15:53
Well, yeah, okay, but I mean, are you saying that counterparty doesn't have colored coins?
Because I think technically they do, you could issue coins.

Sjors Provoost: 00:16:00
Counterparty can do colored coins, among other things, but colored coins was a system on its own.

Ruben Somsen: 00:16:05
I see.
Okay.

Sjors Provoost: 00:16:06
Okay.
So the example I once even used, I think, was called Bits of Bullion.
And what this was, was there was a trust, like a UK or whatever Cayman Islands structure, probably Gibraltar.
And this trust owned gold in the real world and then this trust had basically had its own bylaws and it would define the beneficiaries of the trust.
So the nice thing about a trust is like nobody really owns the trust.
The trust simply exists and you create it and you set it in motion and then it kind of just exists out there.
It's kind of a cool legal structure.
But basically this trust would own gold and then there would be an instruction in the bylaws of the trust that says...
Well, "There's this colored coin out there on the blockchain with this and this block hash or this and this transaction hash..."
"And whoever owns descendants of this original transaction is actually a beneficiary of the trust legally."
"And so he's entitled to that gold, to be able to redeem it.", if they wanted to.

Ruben Somsen: 00:17:07
Right, so what you're saying is basically that there is a UTXO on the Bitcoin blockchain.
And somebody basically said, "Hey, if you own parts of the coins that are in here then you also have ownership over something else".

Sjors Provoost: 00:17:21
Yeah so for example they might start with 10,000 Satoshis and they would say every Satoshi represents one gram of bullion in this specific vault at Brinks.
And then if you were to buy this gold, you could basically go to whatever, an exchange, you would send the right amount of Bitcoin or fiat.
And then they would send you 30 Satoshis, now you'd own 30 grams of gold.
So if you send those exact same 30 Satoshis back, you could redeem it, but you could also send those 30 Satoshis to somebody else.

Ruben Somsen: 00:17:52
Yeah, so the coins, the Satoshis, were colored, basically. So it's where the naming comes from, right?

Sjors Provoost: 00:17:57
Actually. And this is very very brittle because you need to use a special wallet that understands these coins and keeps them separate.
If you put those Satoshis in a regular wallet, it doesn't understand it, it will just spend it.
And your entire scheme, you just destroyed your gold.
But this really exists, so it's kind of cool.
2014 or 2015.

Aaron Van Wirdum: 00:18:16
Yeah, the analogy I used when I tried to explain this to people is...
"Imagine you're organizing like a small festival and you go to the bank and you get a whole bunch of pennies."
"You put special stickers on the pennies and at the festival you can use these pennies with the special stickers and they're worth a beer.", right?
"If you walk out of the festival with the pennies, then there's still worth the penny, but only a penny."

Sjors Provoost: 00:18:41
Yeah.
And if you accidentally try to give a guy a Euro, i.e. a hundred pennies, then you're screwed because you actually just gave him 100 beers.

Aaron Van Wirdum: 00:18:50
Exactly.
Yeah.
If that person knows how to get back to the festival, at least.
So yeah, you're giving a new meaning to the Satoshis on the Bitcoin blockchain.
That's what colored coins are.
And then we just discussed Rare Pepe and Pepe Cash and all that.
And they did something similar, but they used OP_RETURN and it works technically in a bit of a different way, right?

Sjors Provoost: 00:19:12
Yeah, very much differently.
So the colored coins really just use Bitcoin's normal transaction mechanism.
You just combine these Satoshis and move them around.
But the Rare Pepe used a series of instructions.
So that's two things that it used, right?
A series of instructions where you could say, create a new asset and do something with it.
But also if the asset moved on the blockchain, I guess it would also move.
I've never really studied it in enough detail to completely understand.

Ruben Somsen: 00:19:40
Yeah, I'm not entirely certain whether or not Satoshis were moving and they had meaning inside of counterparty.
I thought it did, but I'm not certain.

Aaron Van Wirdum: 00:19:47
I'm pretty sure that's not the case.
I think they just used the data from the OP_RETURNs, and that data just meant something else within the counterparty context.

Sjors Provoost: 00:19:57
Yeah, but at least the new owner was probably done using who got the coins.
Like, which private key received what.
I'm not sure how they would do it.
Maybe the transaction might have two outputs and one output would be OP_RETURN and the other would go to some address.
And then, I don't know, somebody gave me the source code.
It doesn't matter because there's something new and better.

Aaron Van Wirdum: 00:20:18
RGB, that's what the episode is about.

Sjors Provoost: 00:20:20
That's right.

Aaron Van Wirdum: 00:20:20
I think that's where we are now.
We discussed OP_RETURN, colored coins, the other thing, counterparty.
And that was all to get to RGB.

Sjors Provoost: 00:20:31
That's right.





## What Is RGB?
Aaron Van Wirdum: 00:20:32
Sjors, what is RGB?

Sjors Provoost: 00:20:34
Oh, do I have to explain it?
Ruben was gonna explain it.

Ruben Somsen: 00:20:37
Okay, so with RGB, it's a very similar system in the sense that we still have these tokens that are being generated and they're being moved on the Bitcoin blockchain.
But what we're doing here is we're using the existing UTXOs as a kind vessel into which we add and move the coins there.
So let's say I have a UTXO and I have some RGB tokens in there.
Well, first I would have to generate them, but let's skip that for a second.
So there's an output, it's mine.
There are 10 USD Tether RGB tokens in there.

Aaron Van Wirdum: 00:21:14
When you say in there, what do you mean?

Ruben Somsen: 00:21:17
Somehow, and that is of course like, so there needs to be some kind of genesis moment where the tokens were generated.
So the whole point of this system is that it allows you to create tokens and then spend them.
And so first, the USD Tether people would have to issue this token.
And generally, the way that's done in RGB is actually you do use an OP_RETURN.
So first, there's going to be a transaction.
The transaction has an OP_RETURN, so everybody can see it.
And that transaction says, hereby, I declare that now inside of this new UTXO there are just 1 million dollars worth of USD Tether.

Sjors Provoost: 00:21:52
Yeah, and this is actually where your hash at least comes up, because what is in the OP_RETURN as far as I know is a hash of a JSON file.
So anybody who has the JSON file will know that the hash refers to it.
And they can then read the JSON file and see what the supply is and what the rules are for whatever asset has been created.

Aaron Van Wirdum: 00:22:14
A JSON file is just text, right?

Sjors Provoost: 00:22:17
It's just text.
Yeah.
With annoying brackets.

Ruben Somsen: 00:22:20
So, okay, so now we have a UTXO with $1 million in their USD Tether dollars IOUs.
And when they first send them to a buyer, somebody who says, "Okay, I'll give you $1,000, you give me $1,000 worth of these coins."
So the first thing that...





## Client-Side Validation
Ruben Somsen: 00:22:37
...RGB does, is client-side validation, meaning that the JSON file that Sjors just pointed out needs to be transferred during the coin transfer.
So as soon as these coins move from one owner to the next owner, you also have to provide all the data, which refers to the hash that you put in the Bitcoin blockchain.

Aaron Van Wirdum: 00:22:55
Right.

Sjors Provoost: 00:22:56
So the first person who buys the tether, basically, has to receive an email.
And inside that email should be the JSON file, and I guess also a proof that they now own the coins.

Aaron Van Wirdum: 00:23:09
Right. So that's the big difference compared to colored coins, a counterparty, is that now we have a separate layer..
...essentially, of JSON file texts that are also being sent around and they're being linked to in the Bitcoin blockchain.
Is that right?

Sjors Provoost: 00:23:24
Yeah, and this also detaches the amount that's really being moved from the amount of Satoshis that's being moved.
So yes, you're making a transaction.

Aaron Van Wirdum: 00:23:33
But I think that was already the case for counterparty.

Sjors Provoost: 00:23:35
Yeah, for counterparty it is, but for colored coins it wasn't.
For colored coins, the Satoshis really mattered.
But in the case of RGB, you're just sending somebody a transaction and then along with the transaction, an email with what's actually happening.
And that transaction might move one Satoshi or a thousand Satoshis, doesn't really matter.
The instructions are separate, and are not on the chain.
Right.

Ruben Somsen: 00:23:54
So, okay, so we have this one output with $1 million worth of USD Tether, and now they want to send $1,000 to somebody else.
So what they do is they take that output and they spend it and they send it to another output.
And it's still owned by the same USD Tether people who issued the first $1 million.
But inside of that output, there is a public key, that is the person who owns the UTXO and...
...through some cryptographic trickery that's very similar to Taproot, they add another hash inside of this new UTXO.
And inside of this new hash there they point to an output where they want a certain amount of these coins to move.
So they would point to…let's say I was buying $1,000 worth of USD Tether.
I would have to give an output to the USD Tether people, and then when they spend their output, they will point back to me with the committed data.
And they say, "Okay, now $1,000 is inside of Ruben's UTXO."

Aaron Van Wirdum: 00:24:59
Who else can read this?
Can I read this?
How do I know this transfer happens

Ruben Somsen: 00:25:04
So this is a hidden transfer in the sense that it's a commitment that's hidden inside of the public key.
So the USD Tether people need to show the commitment to me so I can open a commitment, they can open a commitment and I can show the commitment to you.
And it can prove that I have 1000 of these USD Tether coins.
And that's what I would have to do if I let's say if I want to then send $100 to you Aaron, then I would have to show that data.
And that is the entire story of the client-side validation.
The entire history of the coin, in this case, the coins were created, then the coins were sent to me.
I would have to show that entire history to you.
And once you see the history, you're satisfied, you see that this is correct.
Ruben DOES have 1000 of these USD Tether coins.
Only then will you accept another 100 from me.

Sjors Provoost: 00:25:54
And this is kind of nice because it creates a really selective privacy thing.
So yeah, Aaron, you can see that you really got the 100 because you get all the history you need to confirm that.
So from the 1 million you see that 1000 was sent to Ruben and from that 1000; 100 was sent to you.
You can see all that.
But what happened to the rest of that 1 million you cannot see.
So I guess the only thing you'll be able to see is that 1 million minus 1,000 was sent somewhere else.
So it didn't increase, but you can't see what happened after that.
So you can imagine history as a giant tree of transactions, but you only get everything that leads to your little branch in the universe.

Aaron Van Wirdum: 00:26:34
Right. So this sounds like the RGB people are making an entirely different cryptocurrency system that's being anchored in the Bitcoin blockchain, right?

Sjors Provoost: 00:26:47
Yeah, I guess.

Ruben Somsen: 00:26:48
Yeah.

Aaron Van Wirdum: 00:26:49
So I think this already came up, but did you mention this off-chain part of it, the JSON files, are these actually sent through email?
Is that actually how it works?
Or what is the-

Sjors Provoost: 00:26:59
You can do whatever you want, but I believe there is a little like do-it-yourself web server that comes with it.
And if you run that do-it-yourself web server, then your special wallet will actually know that it needs to send certain files to that web server.
And it needs to fetch certain files from that web server in order to make sense of just the UTXOs.

Ruben Somsen: 00:27:22
So it can all be automated, right?

Sjors Provoost: 00:27:24
In essence when you're using it, at least if the software is developed all the way to being nice, you would just say...
"I'm going to send a 1000 Tether to you, you have a 100, Aaron, so you're going to send me 10."
I give you an address, you click, copy paste the address, you enter the number 10, you click send and it just works.
On your end, your wallet is uploading certain files to a server that has all the proofs.
And on my end it's actually fetching files from the server to see all those proofs.
And in the case of something like Tether, I guess it would make sense for the Tether Corporation to be hosting that server.
Because in the end, they decide what happens anyway, right?
They're the counterparty.
So you're already trusting them, so it doesn't matter that they also host some data, which as far as I know, they can't really decode.
So it's still kind of nice from a privacy point of view.
Right.

Ruben Somsen: 00:28:17
Yeah, but it is important that you save your own data, right?
Because when I received the $1,000, then maybe Tether has that data as well, and I have the data.
But if the Tether company then stops cooperating, now I can't spend it without the data that they were holding for me.
So I need to hold my own data.
I need to make sure that I have my entire history.
So at the very least, maybe if Tether cooperates, great, you can get the data through them.
But if they don't cooperate, I need to then go and show my data to you.

Sjors Provoost: 00:28:50
Yeah, exactly.
It just means your backup is more than just your 12 words or 24 words.

Ruben Somsen: 00:28:55
Yeah, yeah.

Sjors Provoost: 00:28:55
You need the other data too.

Ruben Somsen: 00:28:57
Right.
The “History” is basically your “Coin”.
If you don't have the history, you don't have your coins.

Aaron Van Wirdum: 00:29:03
Got it.
This does sound like for every Tether transaction, I guess that's the example we decided to run with, for every Tether transaction in this RGB System, we need a Bitcoin transaction.

Sjors Provoost: 00:29:17
Yeah, so the amounts don't have to match and the Bitcoin itself doesn't have to go from person to person, but you do need a unique Bitcoin transaction for every Tether transaction.

Ruben Somsen: 00:29:28
Yes, but it's good to point out that it only has one input and one output.
So you're not, even though there's only 1,000 of the $1 million went to me, on the Bitcoin blockchain, you'll have one input, one output, both owned by USD Tether.
And then another output that was already mine, that was already on the blockchain, that's where the $1,000 went.

Sjors Provoost: 00:29:51
And I guess that means you could piggyback.
So if you have to send money to an exchange anyway, well, I don't think you can tweak that.
Then, well, then at least your input isn't duplicated, but you would have two outputs.
One that goes to the exchange and one that goes back to you which actually has some meaning in the RGB Protocol.
Either way you don't need a lot of data to do this yeah yeah very small transactions and maybe you can piggyback on your normal transactions.

Ruben Somsen: 00:30:16
Yeah, yeah you can combine it with a Bitcoin transaction that you were going to send anyway.
And then also do an RGB transaction at the same time.

Sjors Provoost: 00:30:23
But there's more.

Aaron Van Wirdum: 00:30:25
Can we do better?

Sjors Provoost: 00:30:26
We can do better.

Aaron Van Wirdum: 00:30:27
Sjors, who's gonna explain how to do this better?
Ruben? Sjors?

Ruben Somsen: 00:30:32
I'm confused where we're going.





## Using Lightning channels
Sjors Provoost: 00:30:33
We're going to use a concept from Ruben's little show.
The lightning round.
We're not going to do a lightning round.
But yeah, we can do better with Lightning.
At least in the example that we just talked about.
Because we talked about a fungible asset.
So it doesn't matter which US Tether you have, it's the same.
We previously talked about Rare Pepe, where it does matter what you have.
So what we're going to talk about only works for the fungible stuff.

Aaron Van Wirdum: 00:30:59
Yeah, every USD Tether is interchangeable.
You don't care which one you have.
While when it comes to trading cards, you definitely care which one you have.
So that's the difference.

Sjors Provoost: 00:31:09
And so that means that you can start basically creating Lightning channels where the coins in the channels are these special tokens.
Though I'm a little vague on how exactly that works.

Aaron Van Wirdum: 00:31:19
Well, so to be clear, that only applies to the fungible version - the Tether example we gave or the gold example we gave previously.

Sjors Provoost: 00:31:27
But the awesome thing is, it means that if you somehow get these Lightning channels to work with these colored tokens in it...
...we can start sending very small amounts of dollars back and forth indefinitely.
And only when the channel needs to be closed, we create this Bitcoin transaction and send all the proofs that are needed just for that.
So it means that the metadata you need to keep isn't isn't growing too quickly either.

Aaron Van Wirdum: 00:31:53
Ruben, RGB tokens on Lightning?
Do you see it happening?

Ruben Somsen: 00:31:56
Yeah, so the way I look at Lightning is that it works for every blockchain, at least as long as they have...
...Time Lock and maybe some kind of Hash Lock or Point Locks, whatever they're called...

Aaron Van Wirdum: 00:32:09
Very basic smart contracting tools.

Ruben Somsen: 00:32:11
...So I think it doesn't really matter what kind of blockchain you have.
I think sooner or later, especially when scaling becomes an issue, you have to start using Lightning.
So I would say it works for every chain, it works for every kind of system.
But in this case, RGB is made very specifically to start working with Lightning as soon as possible.
So they're really trying to make it happen right from the get-go.
So specific to NFTs, you can have them in a Lightning channel.
So maybe Sjors and I, we can open a lightning channel, but then we can only send the NFT to each other, basically.

Aaron Van Wirdum: 00:32:51
So, that's more like a regular payment channel than a Lightning channel.

Ruben Somsen: 00:32:53
Exactly.

Sjors Provoost: 00:32:55
So how would you have collateral of the same NFT or you would split it then or?

Ruben Somsen: 00:32:59
So well, there would be one NFT and it would be with me.
And then every time we update the channel, I can then give the NFT to you and then you can give the NFT back to me.
And we can go back and forth, but there will never be, you cannot do the hops, right?
With Lightning, the whole point is that multiple people have channels and they can kind of send from one person's channel to another person's channel.
Alice and Bob have a channel, Bob and Carol have a channel.
So then if Alice sends an NFT to Bob, Bob cannot send the same NFT to Carol because it's a different channel and the NFT doesn't exist in the other channel.

Sjors Provoost: 00:33:33
Of course you could tokenize the NFT, then the NFT itself would be divided into a thousand subunits.
Whoever owns the majority of the subunits is actually in charge of the NFT, but people can trade sub NFTs but let's-

Aaron Van Wirdum: 00:33:47
You're unnecessarily complicating things now.
You're just inventing a new currency based on a single NFT

Ruben Somsen: 00:33:54
A great business proposal.

Aaron Van Wirdum: 00:33:56
Let me ask a concrete question about this, let's keep focused on the fungible RGB tokens, because these can be used in Lightning.
So would that in that case mean that all of the hops need to actually also accept this fungible token as a fee to forward the payment?

Sjors Provoost: 00:34:15
In other words, do you need a Colored Lightning Network, like a completely separate network just for those colored ones?

Aaron Van Wirdum: 00:34:21
Right.

Ruben Somsen: 00:34:21
Yeah. So the answer is yes and no.
At the very least, you need the incoming, like the first hop needs to have the token and the last hop needs to have the token.
But then all the intermediary hops, they don't necessarily, like you can swap while doing, while inside of a Lightning channel.
So you could have a USD Tether to Bitcoin.
And then another hop that remains Bitcoin.
And then the final hop is Bitcoin to USD Tether again.
And in that way, you could kind of lean on top of the existing Lightning network, but you would still need these in points and out points.
And you would still need these swaps to take place.
People that accept the swap.

Sjors Provoost: 00:35:02
Bitcoin Lightning is complicated.
And you think it's like swaps are complicated.
Well, you can do both and have something really complicated, but then you could indeed send US dollar values across the world instantly.
Even if not everybody supports it.

Aaron Van Wirdum: 00:35:16
You say you can, but then there's sort of the other problem where hops on the network can decide not to forward and see what the exchange rate does...

Ruben Somsen: 00:35:25
Yeah, exactly.

Aaron Van Wirdum: 00:35:26
...in the meantime, based on that, then end up forwarding or not.

Ruben Somsen: 00:35:29
Yeah, So specifically there, I think ZMN, SCP, XJ, or something along those lines.

Sjors Provoost: 00:35:35
We call them Zaymom.

Ruben Somsen: 00:35:36
Zaymom, yeah, very Dutch.
Z-man, yeah.
Yeah, he put something on the mailing list saying, you basically have the American call option problem where you can either forward the payment or you can kind of wait and see what happens.
So the final person who is supposed to receive the payment can either accept it or they can wait.
And then they can see if the price goes up or the price goes down and based on that they can decide whether or not they accept the payment.
So because of that it is actually problematic to do these atomic swaps between different currencies on the Lightning Network currently.

Sjors Provoost: 00:36:11
Which is a problem in general, right?
So the idea has been around to have a Lightning Network of Bitcoin that could be connected to a Lightning Network-ish on Ethereum.
And you could just instantly swap between all these currencies.
But there are these kinds of problems there.

Aaron Van Wirdum: 00:36:24
Then one other problem I think is that unless miners are actually gonna accept these fungible tokens in order to settle transactions on the Bitcoin blockchain.
Which sounds like a stretch, they still need to have Bitcoin in the Lightning transactions that are using RGB and you need the fees for that.
It gets very complicated very fast.

Sjors Provoost: 00:36:47
Yeah, and I'm also wondering what the incentive structure is for accepting.
You have these cheap transactions and then you want to punish them.
And if the monetary incentives in Bitcoin are not correct, because most of the value is actually represented by a token, which has its own exchange rate.
I don't know what will happen.
This is where I'm going to make all the details.
Sorry about that.

Ruben Somsen: 00:37:09
Yeah, it's got to be a little difficult.
But, I don't think necessarily, at least the thing that Aaron was saying.
You can actually have a Lightning channel for Bitcoin.
I assume even if you were an RGB user and you wanted to use it on Lightning, you would also want to use Bitcoin on Lightning.
That seems like a safe assumption.
So you could use the same UTXO for that.
So you could have a channel that you're using to send bitcoins back and forth.
And then you can also put RGB tokens inside of it and do the same thing at the same time with a single channel.

Sjors Provoost: 00:37:39
But then it'd be kind of like a collateral.
But then, how do you make sure that I don't end up with just five Satoshis in the channel?
So I have every incentive to cheat, but there's a huge value of colored coins in it.
So somehow you do need to compare the real value that's at stake in Bitcoin versus this tokenized value.
So I think this gets pretty complicated.
I don't know if we wanna.

Ruben Somsen: 00:38:00
Yeah, Yeah, I'm not sure about that.

Aaron Van Wirdum: 00:38:02
Too many worms for now.
Let's move on to more worms.

Sjors Provoost: 00:38:07
Delicious.

Aaron Van Wirdum: 00:38:08
There were more problems, I think, Sjors.

Sjors Provoost: 00:38:09
I think Ruben had one final problem.
That's about it.

Ruben Somsen: 00:38:13
Yeah.
What we were saying earlier about the USD Tether...

Aaron Van Wirdum: 00:38:16
To be clear, we're not talking about Lightning anymore.
We're just talking about RGB.
We're back to basic RGB.

Ruben Somsen: 00:38:21
...we're back to basic RGB.

Aaron Van Wirdum: 00:38:22
And there's a problem with it.

Ruben Somsen: 00:38:24
So even for the Lightning network, right?
Like you still need to use the base layer.
And that's something that people shouldn't forget.
You can't just be saying, "Because we can go on Lightning, it doesn't really matter how expensive the base layer is."
You always need to have these base layer transactions first.
Lots of people need to have USD Tether, then they have to create channels with USD Tether.
And then you can start using the Lightning Network and even then channels have to close and reopen and rebalance, etc., so you're still using the base layer.
Okay so the issue or the first issue would be simply if the token moved many times you have to show the entire history to the person you are sending your coins to.
Maybe at first it's like one megabyte, two megabytes, three megabytes, okay, fine.
But after a while, it becomes hundreds of megabytes or maybe even a gigabyte.
And what's worse is that-

Sjors Provoost: 00:39:14
Right, because we did talk about how you only have to share the relevant part so I only need to see how my money originated from the source.
But I don't have to see the entire tree.
That saves a whole bunch of data.
But even then if the money is passed around a hundred thousand times, I need all those one hundred thousand transactions to see where it's coming from.

Ruben Somsen: 00:39:34
Yeah, the data does keep growing, regardless.
And there is sort of an intermediate solution to that, depending on what kind of token you have.
You could give back the USD Tether to the USD Tether company, and then they could reissue a new token with a history that's completely clean again.
But that works only in the example of USD Tether where there's sort of an IOU system.
If you have some, I'm not sure what kind of token this would be, but if there's some kind of token that is issued once and then never issued again, then you can't do that.
But the problem is that the history of the tokens actually becomes intertwined.
So if I have 1 USDT, and let's say Sjors has 1 USDT, and we both send these to you, Aaron.
Then the history of both these coins becomes connected.
So the proof for your 2 dollars is both our histories.
Now after that, if you want to split them up again, and now you send $1 to one of your friends and $1 to another one of your friends, the history doesn't become unconnected again, the history stays connected.
So each of them has to check the history of both Sjors' coin and my coin.
So, another way of saying this would be, if you have a Bitcoin on the Bitcoin blockchain...
...you can't actually go back and figure out exactly which Bitcoin block that Bitcoin originated in, because the history is connected.
And so because of that, what you end up with is, you might have to download a significant chunk of everybody's history instead of these paths that in the ideal case, short suspension.

Sjors Provoost: 00:41:18
So I guess you're saying that the spaghetti strain gets longer and longer and you get more and more spaghetti strains as money's being combined.

Ruben Somsen: 00:41:25
Yeah.

Sjors Provoost: 00:41:25
So you end up with a ton of spaghetti which is cool for an Italian project.
I think that's all we got right?

Ruben Somsen: 00:41:31
That's right.

Aaron Van Wirdum: 00:41:32
Well I want to ask you guys. Why do we want this on Bitcoin?
Because it sounds like...

Sjors Provoost: 00:41:37
We don't have a choice.

Aaron Van Wirdum: 00:41:38
..it's just a whole bunch of data.

Sjors Provoost: 00:41:40
Well, it's mostly data that exists outside of Bitcoin that we don't care about.

Aaron Van Wirdum: 00:41:44
Yeah, Well, it still requires transactions on the blockchain, at least.

Sjors Provoost: 00:41:47
Yeah, but who can stop that?
Because they look like regular transactions, so it doesn't matter what we want.
We can't stop it.

Ruben Somsen: 00:41:54
Yeah, let's say if you had the option to very easily add native tokens to Bitcoin, where you could issue assets and you could just use them on the Bitcoin blockchain.
If you did something like that, in terms of blockchain usage, it would be very similar, right?
Because with RGB, you have kind of the same thing, where every time you move a token, you do need to create a Bitcoin transaction.
But that Bitcoin transaction doesn't really have anything to do with Bitcoin, other than that it wants to kind of connect to it to to be connected to its proof of work.
So would we want that?
Would we want people to just issue any token they want just natively on Bitcoin?
And then most people would kind of say "No!"
So RGB forces the issue basically and says "You can just do it!", if you do it like this.
So do we want that?
Do we not want that?
I don't think it's going to be terrible.
I think it's going to be okay.
And I don't think there's going to be some kind of token that is so popular that it will pull away most of the proof of work or something along those lines.
That would be kind of the doomsday scenario.

Sjors Provoost: 00:42:55
Yeah, the risk there is, we talked about that in other episodes about Sidechains as well.
If there is, say, the entire world supply of gold expressed as an RGB token, that's a problem.
Because the market cap of gold is 10 times that of Bitcoin at the moment.
Which means that somebody who wants to steal gold through a double-spend attack, might want to do that.
And from a Bitcoin point of view, that attack would look uneconomical, but from a gold point of view, it would look economical.
And therefore, it just messes with the incentive structure that we have.
But we're not there yet.
And I'm not really worried about it.

Ruben Somsen: 00:43:29
Yeah, exactly.
Actually, I think the opposite problem is more likely.
Where the Bitcoin fees are going to go up.
And at that point, you have to, if you want to use USD Tether, you have to pay the Bitcoin fees to use your USD Tether.
And then you have to ask, well, if I can use my use detector on any chain, why would I use it on the expensive Bitcoin blockchain?
So I think that's that kind of becomes the bottleneck for RGB, where any token you want to move on RGB, at least without using Lightning.
And as I pointed out earlier, at least you will have to use the base layer every now and then.
You will have to pay as high of a fee as a Bitcoin transaction and whether or not that's going to be economical, I don't know.

Sjors Provoost: 00:44:10
Yeah, exactly.
And I don't know if you're doing client-side validation anyway, maybe you just want to use a database, but-

Ruben Somsen: 00:44:18
Perhaps, yeah.
And yeah, so the Space Chains, it wasn't called Space Chains back then...
...but the episode we did on the perpetual one-way peg and Blind Merged Mining, it is actually a very similar system, right?
So you could compare the two, but the difference is that you are less connected to the proof of work.
Instead of having one, every RGB transaction you make, you need to make a Bitcoin transaction.
You now have one Bitcoin transaction that represents an entire block of tokens, basically.
So that would at least make it cheaper to do tokens, but at the same time, you're also less secure because you don't have the full proof of work.
It's not directly connected, It's a little bit more indirect.
Okay.

Aaron Van Wirdum: 00:45:04
Okay.
Wait, wait, Sjors.
I have one last question.
Did you want to get into the Proof-Marshall thing or are we going to leave that for a different episode?

Sjors Provoost: 00:45:13
Exactly.
We have another can of worms that's called Proof-Marshalls.
We are not going to open that.

Aaron Van Wirdum: 00:45:17
Okay, do you want to end on a positive note?

Sjors Provoost: 00:45:19
I want to end by saying thank you everybody for listening to The Van Wirdum Sjorsnado.

Aaron Van Wirdum: 00:45:24
There you go.

Ruben Somsen: 00:45:25
There you go.





## End of The Van Wirdum Sjorsnado show

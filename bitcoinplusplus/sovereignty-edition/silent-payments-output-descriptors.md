---
title: 'Silent Payments: Output Descriptors'
speakers:
  - niftynei
date: '2026-01-17'
tags:
  - silent-payments
  - descriptors
  - taproot
  - schnorr-signatures
  - privacy
  - wallet
  - btcplusplus
categories:
  - conference
source_file: https://youtu.be/QQO0pMQB-QU
media: https://youtu.be/QQO0pMQB-QU
summary: niftynei presents a walkthrough of Craig Raw's BIP 2047 proposal at bitcoin++ Sovereignty Edition in Taipei, which adds a new SP top-level output descriptor format to BIP 352 (silent payments), introducing two new key expression types — SP scan (private scan key plus public spend key, for watch-only wallets) and SP spend (both scan and spend private keys, for fully spending wallets) — along with two optional arguments — a birthday block height to limit how far back a wallet must scan the chain, and integer labels that allow a single silent payment key set to differentiate multiple payment sources (e.g., separate Twitter and GitHub addresses) without generating separate key sets; niftynei also explains why silent payments require Schnorr signatures and must therefore be taproot outputs, and notes that the descriptor format enables cross-wallet interoperability by giving implementations like Sparrow, BlueWallet, and Bitcoin Core a common language for importing and exporting silent payment key material.
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:00

Great.
Okay, so silent payments are pretty cool.
We're not going to talk about that.
In fact, there's already a BIP, BIP 352 for silent payments.
What this talk is about is about the app output descriptor format.
Specifically, the BIP proposal for adding an output descriptor format.
Okay, so this is the BIP.
It's called Add SP Output Descriptor Format for BIP 352, which is the BIP number for silent payments.
How many of you have heard about this proposal for output descriptors.
This is new, right?
This is new for most people.
Okay, cool.
Great.
So, okay.
So, the specification is pretty short.
It says we're going to add a new top-level script expression as defined as SP.
And then it also adds two new things called key expressions.
We're going to learn about these in a second.
They're new key expression types.
One is called SP scan and the other is called SP spend.
So we're going to have two new ways of expressing a particular key.
The difference between them is that one has a private key encoded in it and a public key encoded in it.
The other one, SP spend, has two private keys encoded in it.
And I'll show you what this looks like in a second.
So don't worry if this isn't exactly understandable.
Okay, so you're like, okay, what's the difference between SP scan and SP spend?
SP scan is for watch-only wallets, Because it has a public key part of it in it.
And then SP spend as a key encoding is going to have full wallets because it has two private keys.
So basically if someone sends you, so The key idea with a key expression is that it's like, okay, here is key material.
This will either let you identify coins that have been locked up to this particular information, or it will let you both identify them and also spend them.
But I'll get into this a little more explicitly.
Okay, so let's just go back to like, okay, what are we talking about?
We're talking about this SP thing.
So SP is short for silent payments.
So basically when you have a descriptor, what a descriptor, what the whole point of having an output descriptor is that it's like here's a description of what an out point in Bitcoin might look like on chain and it's a way that if you have this description of what an out point or output might look like you're then able to go and find them across all of the out points that exist in Bitcoin currently.
Both past ones that have been spent and ones that are eligible to be spent, to spend.
And the whole goal of this is that your wallet will be able to identify coins that you're able, interested, they're either interested in keeping track of when they're spent versus not, or, and maybe additionally, able to spend those outputs, if that makes sense.
So we basically need a way of writing down, these are outputs that I'm interested in, and here's information that you would need in order to be able to spend them in some cases.
OK, so we're going to write this as kind of like it's very, for whatever reason, all output descriptors look like function definitions.
So this one is SP, so it's like, OK, for a silent payment, here's some information.
So the first thing that we're going to put inside of this kind of set of information about a silent payment output is something called a key expression.
How many of you have seen XPUBs before?
So, XPUB is kind of a traditional or classic key expression.
It gives you information to be able to find not only one output, but a series of outputs that have been spent to that particular output descriptor, to that particular XPUB, right?
XPUBs have this property where you can spend multiple ones of them, and they have a chain code included in it, etc., etc.
XPUBs are not valid key expressions for this SP descriptor.
Instead, Craig invents two new ways of encoding information about keys.
In order to put a key expression inside of this SP thing, and this is part of the spec, which I could pull up to show you, but that's okay.
So it must be a silent payment key expression, which he defines two, which we kind of just looked at.
One is this SP scan, and the other is SP spend.
So these are actually gonna be long series of information, a lot like an XPUB is.
XPUBs can be quite long.
They're encoded in batch 32.
I don't really care about the encoding.
All I care about is what information is inside of them.
So what exactly goes in this dot, dot, dot portion of a key expression for a silent payment?
For, okay, so this is from the BIP proposal that Craig wrote.
He's got SP scan and SP spend.
So actually, he kind of then defines the data part.
It starts with the character Q, because that's V0.
And then there's a payload in each of them.
I'm not going to look at the actual bit, but I'm just going to kind of explain what's in them.
So for SP scan, the first kind of piece of information that you're going to have in this fetch 32 string is a private key.
This is going to be something called the scan key.
For silent payments, there's basically two keys involved in each one.
One is a scan key That's what allows you to go through every single out point and figure out whether or not it belongs to your wallet You actually need two pieces of information though You need the scan key and then you need oh and the scan key since it's a private key all private key material in Bitcoin is 32 bytes of random data, so it's just a number, and this is no different, so you're going to have a 32 byte piece of information, which is a private key, and that's gonna be your scan key, and then there's gonna be a second key inside of this basically key expression, and for the scan type of it, it's actually gonna be a public key.
This is gonna be our spend key.
So spend key basically is whether or not you're able to move the funds that are locked up to that out point.
We just have the public key and the SP scan type of key description.
So this is public key here.
It's gonna be 33 bytes because if you're familiar with how public keys in elliptic curve encryption work, you'll know that they're actually points.
It's x, y, and we put them in the compressed form.
So it's always 33 bytes long.
That's because it's an X coordinate plus a parity description for which Y you pick.
If you're not familiar with private and public keys, there's a great base 58 class all about cryptography up on Udemy.
So I encourage you to go check that out where we explain exactly how private and public keys work for elliptic curves.
But yeah, so for SP scan, you're gonna have, again, two kind of pieces of information encoded into a batch 32 description.
One of them is gonna be a private key, One of them's gonna be a public key.
Again, this first private key lets you scan for information about silent payments.
And the second one is whether or not I, the person who's holding this SP scan thing, can spend it.
Again, So again, if you go back to the BIP that Craig Raw came out with, he had two kinds of key expression types that he defined.
One was scan, which we just walked through.
The second one was the spend, so SP spend.
And instead of having a public key for the second piece of information, it's now actually going to be the private key for the spend key.
So basically if someone sends you an SP spend thing, this has all the information you need to spend any Bitcoin that gets sent to a silent payment that's associated to that public key.
That makes sense?
I'm not gonna get into exactly what the public keys are for this.
That's like kind of inside of the silent payment specification, which this talk is not about.
But again, so that's two private keys.
So if you have an SP spend, you can spend any Bitcoin that anyone has sent to that particular silent payment.
If you have SP scan, okay, so SP spend means I can spend any money that gets sent to this.
SP scan means I can only see any money that gets sent to it.
I can't actually spend it.
Seems pretty simple, right?
Okay, so we have scan, we have spend.
That's the first part.
Okay, so we're kind of defining a silent payment.
The first part is like, here's all the data that you need in order to be identified, these out points on chain, and optionally spend them if I provide the secret key for it.
Craig also defines two additional pieces of information that you can optionally add.
This actually might be like one critique I have, but that's okay.
One is he calls them the birthday, and then he calls them a set of labels.
So let's get into what this says.
Birthday.
So A birthday is a description of when you started sending Bitcoin to the silent payment address, if that makes sense.
This is going to be a block height.
In this case, for example, it would just look like a number, like the block 840, 000.
So basically this is a way, whenever you're making a silent payment address, one of the more complicated and complex pieces of silent payments is that it requires a decent amount of computation using that spend key and that scan key that you identified in the key expression.
There's a lot of computation that goes into scanning every out point and doing ECDSA, like an ECDH, so an elliptic curve Diffie-Hellman calculation for every single out point to check if basically you're able to spend it.
So that's kind of work that's outside of the descriptor and you can use the information in the key expression.
In order to cut down on the amount of work that your wallet has to do to identify silent payment out points that belong to your wallet, Craig is suggesting in the BIP for the descriptor that you can optionally annotate it with a block height from which to begin scanning.
So basically by having a birth, that's why they call it a birth date, you're like, okay, I know that I didn't generate the silent payment key set until block 840, 000.
So whenever my wallet is going to start scanning for any potential out points that match the silent payment descriptor, I will only start at the birth date that's included in the descriptor.
So it's basically a way of cutting down on the amount of work that a wallet might need to do by including a birth date.
I believe it's optional.
You could just include a key expression, and That would be a valid output descriptor.
Or you can add a birth date like that.
So just as an example, this would be a valid output descriptor according to the BIP that Craig is proposing.
So you would have your key material that gives you all the information you need to find it.
And then you would have a birth date.
So it's saying, don't start scanning for these outpoints until this block and after.
So that's birth date.
I have a lot of time.
That's fine.
I'm not going to use it all.
OK.
So then the last piece of this is another optional thing that you can add, and these are called labels.
I didn't know what a label is.
I have to be honest, I had not looked into what silent payments are, really, until I told Craig that I would present his descriptor bit for him.
So I was like, great.
I have to figure out what a label is.
Is there anyone here who knows what a payment, silent payment label is?
Same.
OK.
So in order to figure out what this is, we have to go to the actual BIP that defines silent payments, which is BIP 352.
So I did the find for you by doing control find.
I found this whole section on labels.
Check that out.
They define what a label is.
Okay, let's focus on the important pieces, which is this piece right here.
Bob may wish to differentiate incoming payments.
So the idea with silent payments is that you basically have two kind of private numbers.
You have a scan key, which is private, and you have a spend key, which is another private thing.
If I give you the scan key and the public key version of my spend key, anyone can find it.
If I give you the scan key, which is always private, and the private spend key, then you can spend my money.
But generally, let's say that I want to give one to my friend Janet, and I want to give one to myself, so when I send myself money, and I want to know when Janet is sending me money to my silent payment address versus when me, Nifty, is sending myself money to my private, to my silent payment address, right?
In the spec, they say you might just come up with two different ones, so your wallet might have two different silent payment things, but that becomes computationally intensive, is what they say.
So the way to get around that is this concept of a label.
I'm not gonna go into how the labels work, but basically, again, the idea is you wanna determine the source of an incoming payment.
Because they deal with a silent payment address is that you could post it on your website, but you could have one on your website, maybe one on your GitHub, another one on your Twitter profile, and using the labels you could have give each of them a different label.
So your wallet would be able to pick up all of them, but any time a payment came in, you would know, oh, someone paid me from my Twitter, or oh, someone paid me from my GitHub.
Like, you'd know where they found your silent payment address from because of the label that you gave it when you put it out there.
I don't know how wide wallet's label support is across different silent payment wallets, but this is part of the specification.
So in theory, you can do it, which is why the descriptor needs to be able to talk about what labels you've put out there and for people to see.
So if this was me defining it, a label might look like, okay, I gave this to Janet, so I've labeled this particular SP to Janet, or it would say, okay, this is Nifty, I sent it to Nifty, that's the label.
So there could be multiple versions of the same silent payment information using the same scan key and the same spend key.
But you're able to track who's sending you money.
The thing is that you can't actually put names in it.
Labels as per the silent payment spec is an integer M.
So instead of saying Nifty and Janet, I just can put the numbers 1, 2, 10, 21.
And so then somewhere else, you'll have to map.
Like, OK, label 21 means Nifty.
Label 10 means my friend, Jana.
But that's not part of the specification.
That would be something you'd have to add on top of it, if that makes sense.
So whenever you're describing, okay, silent payments can be made to this key.
Again, a key is a scan key and a spend key.
Starting at this birth date, and then here's all the different labels that I've assigned to this particular set of silent payment addresses.
So for me, it would be 11021.
So altogether, this is what a silent payment descriptor would look like as proposed by Craig.
Again, this is not final.
This is just a proposal.
So this is a full one that has both a key expression, a birth date, and then a series of labels would look like.
I haven't gone and looked at the spec, but one of the questions I have for Craig is whether or not the birth date's optional.
Like, could I leave the birth date out but include...
I don't know if there's a way in his spec that I could leave the birthdate out but also include labels, if that makes sense.
I think if you include labels, you also have to include a birthdate.
So that would be one piece of feedback I would have for Craig about this in particular.
But yeah, that's kind of the descriptor set, or at least that's the definition as Craig has put it out there.
It's kind of fun to walk through.
I feel like I kind of learned a lot about the pieces of what goes into a silent payment just by walking through the descriptor set.
And then this is from Craig's proposal.
So there's three things that you put in the silent description or the silent payment descriptor.
First is the key expression that we talked about.
The second is a birthday or a positive integer representing a block height, which is the second argument.
And then zero or more label integers, which is the main argument, where each label is a positive integer.
Again, it looks like this.
Cool.
Okay.
Great.
Okay, so that's his proposal.
You can find it on the BIPS repo at 2047.
So this is his whole thing.
Again, thanks, Craig, for coming up with this.
This is a, I think it's an important piece of being able to communicate about what silent payments you're expecting between different wallets.
So having an output descriptor that defines a silent payment address or a silent payment type would let you port them between different wallets much more easily so you could import it into BlueWallet or Sparrow or Bitcoin cores, descriptors, et cetera.
So having a common language to talk about this information is really important.
And again, all of this is kind of based on how silent payments work, which we did not go into.
If you're interested in more information about what exactly is in a silent payment and how the ECDH works, how they're actually using the scan key and the spend key to be able to identify outpoints from some data that's on chain.
I suggest you look at BIP 352.
I've got lots of time, but wrapping up.
Just a reminder, I'm Nifty.
I also go by NiftyNai.
You can find me on the internet.
I haven't been posting on socials much, but I'm up there occasionally.
I run Base58, which is a school of engineering based on the Bitcoin standard.
I'm currently reworking a lot of our online curriculum, but our Udemy classes are still up there.
So if you wanna learn more about classic elliptic curves, we've got some pretty good Udemy classes.
We also have a good class on how transactions in Bitcoin work, if you wanna just learn more about the transaction format, et cetera.
But working on trying to relaunch for next year.
Hopefully that happens soon.
Yeah, I also run Bitcoin++.
Thanks for coming to our first ever sovereignty edition in Taipei.
We have about eight more minutes.
If anyone has any questions, happy to hear them.

Speaker 1: 00:18:08

Thanks, Divti.
Might be out of scope, but do you know if there's any plan to be able to derive the scan private key from the spend private key, like deterministically?

Speaker 0: 00:18:19

Yeah, that's a great question.
I think they have to stay separate.
And I can pull up, I mean, if you want to be, let me see if I can find the,

Speaker 2: 00:18:26

I don't have a link to the BIP, do I?
BIP, that would be handy.
BIP 352, there it is, that's this one.

Speaker 0: 00:18:33

Is there a way to full screen this?

Speaker 2: 00:18:35

There's gotta be a way to full screen this.
There we go, does that work?

Speaker 0: 00:18:38

Ta-da, kind of.
Okay, so.
Okay, so this is the silent payments bit, which I have not completely read.
I shouldn't admit that on camera.
It's OK.
So if you dig into the math of how these work, you want them to be separate.
So you could use them.
They could be the same thing.
And in fact, the original proposal, if you look at the simple case, this integer A, I think, discovers, no, that's not it.
Okay, so in the original, kind of the simplest case of private keyments.
There's this public key B.
So this is kind of the piece that belongs to what you're defining in the silent payment descriptor is B.
So here they say public key B.
Public key B would have little case B, which is the private key to the public key.
You could, this is the absolute simplest description of these keys, you could just have a single key that would allow you both to scan, you would use it both for scanning and spending, if that makes sense.
So it's the same.
That is an undesirable property if you want to have a watch-only wallet.
So further down in the specification, they actually define a spend and scan key as separate items.
So they update that original.
So this is like the original extremely simple equation that they use to generate public keys to send Bitcoin to from a silent payment address.
You can make it more complicated in the case that you also want it to, if you want to separate out the key that lets you identify the outpoints from the key that lets you spend the outpoints.
So now you need two keys.
One is the key that lets you identify them and the other is a key that lets you actually spend them.
In this case, it updates basically the kind of compare these sort of hard to do.
So in the original equation, no, that's not.
Hang on.
Sorry.
In the simple case, your spend key basically is here.
So this component of the equation is what lets you spend the Bitcoin.
You make a hash, which this is like, this is basically the Schnorr signing algorithm.
It usually has, I forget what this is called, I think this is called the commitment or the challenge, where you have a hash that you're multiplying times G.
And so it also gets kind of hashed in here.
The biggest difference when you have a spend and a scan key is that now you have your spend key is still what's being added at the front.
So that's what lets you spend it.
Does that make sense?
That's like your secret key that if anyone has a secret to that, they can spend it.
And instead of including your spend key in the hash, you're now including a separate key, which is the scan key, if that makes sense.
So basically you kind of have two different keys.
The scanning key gets added to the hash, but because it's hashed in, it doesn't have any value in terms of unlocking the funds, It just helps you identify them.
And then the piece that actually lets you spend the money is this first component, and so they're separate.
So if you want to look for them, you must know what the input to the hash was.
One of those components now becomes the public side of the scan key.
I don't know why you need to know the private.
I think, yeah, and they kind of have this thing in here where you can detect it by, you need the hash of the, oh, it's a multiplier, that's why.
Basically, you need the private piece of the scan key in order to identify them, though.
So you can send them to, so basically, you can send Bitcoin to this by knowing just the public key of the scan key and the public key of the spend key.
You can identify them by knowing the private side of the scan key is why in the output descriptor definition, We had SP scan and SP spend.
Both of those required the private side of the scan key.
And that's because without that, you can't actually identify them.
And this is why.
This is the math.
Cool.
Sorry, does that answer your question?
That was a longer.

Speaker 3: 00:23:14

Yes.
Do you have a backup PD?
So you can use backup for the scan and PD?

Speaker 0: 00:23:27

Yes.
Ideally, yeah, probably.
But you wouldn't want to, if you have the spine key and you're deriving the scan key, yeah, this is beyond my pay grade at this point.
But yeah, you're right.
If you had a way of deriving the scan key from the spine key, then you wouldn't need to encode both of them in the descriptor, right?
Because there would be, you would need to communicate that, it would be implicit.
So maybe that's something to contribute back to the descriptors back, yeah.

Speaker 3: 00:23:58

Yeah.
So I just have a comment.
You asked a question for Craig about optional birthday.
So since labels are numbers, probably it can't be.
There's no way to distinguish whether it's a label or a birthdate.

Speaker 0: 00:24:15

You're saying with making, so basically my question was like, could we make the birth date optional and also include labels, right?
And I think you're right, because it's all the same type.
I don't know, something to think about.
I don't think leaving birth dates out is necessarily desirable.
But, cool.
Any other questions?
We've got like another minute and a half.
This is the whole specification for silent payments.
Fun fact, silent payments require Schnorr, so they wouldn't be possible without Taproot.
For those of you who know much about the upgrade path on their cryptography stuff, we added Schnorr with Taproot.
I don't think you can't do the math that they're doing to make and have this all work prior to Taproot outputs, so silent payments must be taproot outputs.
It's kind of cool.
Anything else?
Any other questions?
Okay.
I will leave the floor a minute early.
Thank you for coming.
Great.

Speaker 3: 00:25:30

You you you you

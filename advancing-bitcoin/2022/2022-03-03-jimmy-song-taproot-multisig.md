---
title: Taproot multisig
transcript_by: Michael Folkson
tags:
  - taproot
  - tapscript
  - musig
speakers:
  - Jimmy Song
date: 2022-03-03
media: https://www.youtube.com/watch?v=Uo3uzofPlX0
---
Slides: <https://jimmysong.github.io/taproot-multisig>

Pull request adding multisig Taproot support to buidl-python: <https://github.com/buidl-bitcoin/buidl-python/pull/109>

## Intro (Jeff Gallas)

The next speaker is Jimmy Song who doesn’t really need an introduction but in any case, he has been, which is important for this conference, running the Programming Blockchain workshops for 5 years now. Leon is one of his alumni so there is a direct connection to this conference. He has also just released a new book which is a bit more political than technical, it is called “Bitcoin and the American Dream”. This is not what we are going to hear about now, we are going to hear about Taproot multisig now so welcome Jimmy.

## Intro (Jimmy Song)

The slides are at this [URL](https://jimmysong.github.io/taproot-multisig) so if you are curious about what I’m talking about then please go check that out. First of all it is great to see all of you. I know many of you have been locked down for a couple of years. It is hard being alone at home, now you get to meet people in the flesh. I am so happy that Leon put this together. I just want to give him a shoutout. We’ve had that in Austin for over a year now. For many of you in Europe, you just got out of lockdowns, I want to acknowledge your pain.

Let’s talk about Taproot multisig, that’s what we are going to talk about in the next 30 minutes or so. Here is what we are going to cover. We are going to briefly review Taproot, what it does and how it works. We are also going to start with traditional multisig, how does multisig work now? Then we are going to get to different options that you have with Taproot. To be fair I don’t think of any these are implemented anywhere really yet. It is up to all of you to go do that. I am going to give you some options on what you can do to program multisig in a Taproot world. Single leaf k-of-n, multi leaf k-of-k, multi leaf k-of-k MuSig, everything multisig and we’ll talk about degrading multisig. These are all different options that we have. There’s probably more than this, this is stuff I’ve implemented, all of the little gotchas, advantages, disadvantages to each. That’s what we’ll cover during this talk.

## Taproot Overview

Let’s get started with a brief Taproot overview. There are two paths that you can go down, you can do a key path spend, locked to a single key, it requires a Schnorr signature over a point on the elliptic curve. That’s a key path spend. This is what used to be the equivalent of a single pubkey spend. And you have a script path spend that requires satisfying a Tapscript that is embedded in a MAST tree or a Merklized Abstract Syntax Tree. You can have lots of different options there. The way I describe Taproot is right now we have two classes of addresses: single key lock and more flexible with script hash or something like that. Taproot essentially joins them both and puts them under one type of address which is very nice for privacy and so on. A Taproot tree can have up to 2^128 different Tapscripts, virtually infinite for all purposes. The number of different scripts that can be embedded there. Don’t try to make that many because there is no way you are going to be able to roll through a space that big.

## Taproot Structure

This is what a Taproot structure looks like. You have a key path spend with a pubkey, that’s a single pubkey. You have the MAST tree on the right side, this is a script path spend, and you have different Tapscripts that come up to the Merkle root which we call the tweak. The tweaked pubkey is what you publish as part of the scriptPubKey. This is where you spend to, the tweaked pubkey. As long as you know the tweak and you have the private key to the public key then you can do the key path spend. If you can satisfy any of the Tapscripts and you have the pubkey that is enough to do the script path spend. That is basically how it works. This is an example of three different Tapscripts that you can spend out of but this is generally how Taproot works. You have multiple options on how you spend.

## Traditional Multisig Script

<https://bitcoin.stackexchange.com/questions/40669/checkmultisig-a-worked-out-example>

scriptPubKey
```
OP_2
PubKey A
PubKey B
PubKey C
OP_3
OP_CHECKMULTISIG
```

scriptSig
```
OP_0
Signature for A
Signature for B
```

Stack
```
OP_0
Signature for A
Signature for C
OP_2
PubKey A
PubKey B
PubKey C
OP_3
OP_CHECKMULTISIG
```

Let’s talk about traditional multisig script. This is what that looks like. Typically you have some sort of scriptPubKey, usually it is hashed or something like that but you could also do bare multisig I guess. It is something like this. All of the examples on my slides are going to be 2-of-3 multisig. You have 3 pubkeys, you have to have 2 signatures out of them, the scriptSig needs to be OP_0, signature from one of the keys, signature for another of the keys. You have this execution stack that we are going to go through. The execution looks something like this. You have a whole bunch of stuff. All of these things on the left will put stuff on the stack except for the last one which will actually do something to the entire stack. It is a giant opcode OP_CHECKMULTISIG, it consumes one more element than it is supposed to which is why you need that zero at the bottom. The famous off by one bug. If 2 of those signatures are good for 3 of these pubkeys then you are done, it is a valid script and you are good to go.

## Traditional - Advantages/Disadvantages

The traditional multisig has some advantages and disadvantages. The nice advantages are that it is non-interactive. Stepan (Snigirev) just talked about all the problems with interactivity. You don’t have any interactivity here. You just go and collect signatures from different parties and you are good. Also signers can be determined as you go. You have say 3 pubkeys, if A is not available you can just go to B and C and collect their signatures instead and you are good. You don’t have to determine who is going to sign or anything like that. That said all of the unlocking conditions are revealed in traditional multisig. If you have custom multisig like 2-of-3 of these OR 5-of-7 of these, something like that, then all the conditions are revealed. That kinda sucks. Also all of the public keys are identified, that is part of the protocol. Even if B isn’t signing like in the example you reveal B’s pubkey. That way the attacker knows something about you. Finally it is large fees. B didn’t sign but you still have to reveal the public key. That’s additional cost in terms of fees because it makes the transaction bigger. Those are some advantages, disadvantages of the traditional multisig.

## Taproot structure

Let’s start talking about what we can do in Taproot, this is the single leaf multisig Taproot. This is about as close to traditional multisig as you are going to get in Taproot. The idea here is that you have a tweaked public key, usually the key path spend is going to be 3-of-3 MuSig or something like that. You have a single pubkey that you can use. But the Tapscript is going to be something like 2-of-3 Tapscript. I’ll describe that shortly. There is no complicated MAST tree, it is just really one script on the script path side and that’s it.

## k-of-n Tapscript

<https://bitcoin.stackexchange.com/questions/114465/how-does-the-checksigadd-opcode-work-how-does-it-compare-to-its-predecessor-che>

Tapscript
```
PubKey A
OP_CHECKSIG
PubKey B
OP_CHECKSIGADD
PubKey C
OP_CHECKSIGADD
OP_2
OP_NUMEQUAL
```

Witness
```
Signature for C
‘ ‘
Signature for A
```

Execution
```
Signature for C
‘ ‘
Signature for A
PubKey A
OP_CHECKSIG
PubKey B
OP_CHECKSIGADD
PubKey C
OP_CHECKSIGADD
OP_2
OP_NUMEQUAL
```

What does that look like? It is something like a k-of-n Tapscript, that is how I would characterize it. This is 2-of-3. The Tapscript looks something like this. OP_CHECKSIGADD is a new opcode as part of Taproot. This is the recommended way to do k-of-n. The witness is going to have 2 signatures and a blank in the middle. The blank in the middle indicates “I don’t have a signature for this particular one”. The reason for that should be obvious in a second. The set of commands that you need to execute and here is what that looks like. You have a bunch of stuff at the top that is going to go straight to the stack. The first operation that is going to execute is OP_CHECKSIG. Take PubKey A for Signature A, you consume those two elements and if it is a valid one then you put a `1` there, if it is invalid you put a `0` there. We are supposing that it is valid so we put a `1` there. Then PubKey B goes on the stack and we get OP_CHECKSIGADD. OP_CHECKSIGADD is interesting. The way OP_CHECKSIGADD works is it consumes 3 elements, a pubkey, a number and a signature and it only increments the number if the signature is good for that pubkey. In our case right now, if you look at the top 3 elements, the signature is actually blank so it is not a valid signature for that pubkey. It doesn’t increment the number, it will just leave a `1` afterwards like so. You have `1` and Signature for C at this point. Pubkey C goes on top of the stack and we have CHECKSIGADD. At this point it looks at the signature and the public key. It is going to be valid so instead of `1` it is going to increment it to `2` because it is a valid signature. You are incrementing or accumulating signatures. We’ll have a `2` there, OP_2 is going to put `2` on top. And OP_NUMEQUAL will check that the top two are equal, then you have a `1` and you have valid execution. This is how a single leaf k-of-n multisig would look like.

## Single Leaf - Advantages/Disadvantages

There are some advantages, disadvantages to this. First this is still non-interactive and that is a very good thing. You don’t need to go back and forth between different signers. Also the signers can be determined as you go. You don’t have to go “A and C are signing”. If A is not available you go to B instead and still get whatever it is that you need. That said, all unlocking conditions are revealed. Mostly because you have that one single leaf and it is obvious when you see onchain that it is a single leaf. The public keys are still identifiable because you reveal A, B and C as part of revealing it. So if you happen to know who B is then you can go and try to threaten them or something. You don’t want to reveal additional information if you can help it. Also it is larger fees because you have to reveal every public key. If it is a 5-of-9 or something like that you reveal all 9 public keys. The 4 keys that didn’t sign anything you still have to reveal, goes onchain, that’s a lot more bytes, it means larger fees. So you can see that the advantages, disadvantages are very similar to traditional multisig.

## Multi Leaf k-of-k Tapscript

What are our other options? We can do something like multi leaf k-of-k Tapscript. What does that mean? Imagine something like this. This would be the Taproot structure. You have 3-of-3 MuSig which most of the time isn’t going to be used. But on the right side you have 3 Tapscripts that get accumulated to that tweak. It is every combination of 2-of-2 out of the 3 keys. This is A and B, A and C, B and C, and they are all available as Tapscripts.

## k-of-k Tapscript

Tapscript
```
PubKey A
OP_CHECKSIG
PubKey C
OP_CHECKSIGADD
OP_2
OP_NUMEQUAL
```

Witness
```
Signature for C
Signature for A
```

Execution
```
Signature for C
Signature for A
PubKey A
OP_CHECKSIG
PubKey C
OP_CHECKSIGADD
OP_2
OP_NUMEQUAL
```

 Each one will have a Tapscript. This would be for A and C. The witness will require those two particular signatures. The executions are going to be very similar except you need to provide valid signatures for each one. You are not really “wasting” any space because you don’t reveal pubkeys that you don’t have signatures for at all. We can go this. You do OP_CHECKSIG, that will give you a `1` and then the pubkey C, OP_CHECKSIGADD, that will increment the `1` to a `2`. OP_NUMEQUAL, you are good, you have a valid unlocking of that particular Tapscript.

## Multi leaf - Advantages/Disadvantages

Here are some multi leaf advantages and disadvantages. The main advantage is still that it is not non-interactive. You are not forced to go trade nonces or anything like that. But you do have to determine who the signers are beforehand. If A and B are signing then you need to choose that particular Tapscript at the beginning. And then bring that particular transaction over to whoever is signing. If somebody isn’t available, now you have to start over again. You can imagine if it is like 4-of-7 or something like that and you’ve already got 3 signatures and the 4th person isn’t available that sucks. You have to start from the beginning and go through the entire process again. That kind of sucks. That said, only one unlocking condition is revealed. There could be for 3-of-5, 10 different conditions, 5 choose 3 ends up being 10 different combinations. You only reveal that one unlocking condition and it is sort of minimal. You are only revealing the pubkeys that have signatures and not any of the other pubkeys. It is still identifiable, the ones that sign, but it is not quite as bad as before because you are not revealing everybody’s. Smaller fees because you don’t have to reveal all those public keys that you are not signing with. That is kind of nice. Especially for very large multisig setups, you could have lots of different public keys and you don’t have to reveal any of them or put them onchain. Therefore you are going to get generally smaller fees, at least than the other one. That is multi leaf k-of-k multisig.

## Multi Leaf MuSig Tapscript

<https://murchandamus.medium.com/2-of-3-multisig-inputs-using-pay-to-taproot-d5faf2312ba3>

We can also do multi leaf MuSig Tapscript. This looks something like this. It is very similar to the other one except that instead of leaves that use the OP_CHECKSIGADD construction you have MuSig so you have aggregated public keys for each of them. You have 2-of-2 MuSig for each of the combinations of pubkeys. You might have A and B, A and C, B and C as the 3 different MuSig things. Then it becomes trivial for each Tapscript because it is the public key of A and B, OP_CHECKSIG is your Tapscript and the witness is just a single signature which is aggregated. You have to generate it together in an interactive way. The execution looks like that.

Tapscript
```
PubKey A+C
OP_CHECKSIG
```

Witness
```
Sig for A+C
```

Execution
```
Sig for A+C
PubKey A+C
OP_CHECKSIG
```

It is pretty simple. It is checking that one particular signature is valid and you are good.

## Multi Leaf MuSig - Advantages/Disadvantages

The disadvantage of multi leaf MuSig is that it is interactive. This isn’t say a problem if you are doing something like Lightning where you are doing a lot of communication anyway. But for any sort of secure multisig setup, having to go back and forth even in 2 rounds kind of sucks. As Stepan (Snigirev) pointed out there are a lot of different problems that you might encounter, a lot of hardware wallets for example aren’t used to keeping state, things like that. So interactivity is a major drawback. Also the signers have to be determined beforehand. This is an absolutely critical part of MuSig, you need to know who the group is. If one of the parties is unavailable you are kind of screwed. That said there are some advantages. Only one unlocking condition is revealed. And furthermore you are not even revealing your public keys. If you know the pubkeys that are going into it then you can go in that direction and figure out the aggregated pubkey. But if you just know the aggregated pubkey you can’t derive the component pubkeys that went into it. So really you have no idea who signed it or what happened or anything. It gives you a lot more privacy with respect to what you are actually revealing. Of course this has the smallest fees because you are only revealing one pubkey, one signature, no matter what the combination is. Practically speaking this ends up being very nice because you are saving money onchain, you get a lot of privacy. The problem is that interactivity, it costs you more to go and do it, whether or not that is worth the privacy onchain, less fees is up to you.

## Multi Leaf Everything

Those are our three different ways that you can do multisig within Taproot. But there is one other one that I want to point out you can do which is multi leaf everything. The idea here is that with Taproot you can add everything. You can throw them in there because it doesn’t cost you that much other than more levels. Adding a level doubles the number of Tapscripts you can have basically. I didn’t put the key path spend but basically this would be the script path. You can have a 2-of-2, a k-of-k multisig. These would be the Tapscripts that are 2-of-2. You can have 3 of them, you can have 3 MuSig ones and you can have the 2-of-3 k-of-n. You can have all of them thrown in there and you just pick whatever it is that you need as you go.

## Everything - Advantages/Disadvantages

The beautiful thing about this is for all of these you can do one or the other, whatever it is that you want. If you happen to have all of the keys nearby then maybe you optimize for privacy and fees. If you don’t, do I know who is going to sign, who is available? You could figure out what the trade-offs are on your own. But of course I don’t know if you want to be doing that necessarily. It puts a lot of pressure on whoever is coordinating the whole thing. It is kind of nice we have this option as part of Taproot. It is very, very cheap to throw more scripts in there. It is ultimately a Merklized Abstract Syntax Tree.

## Degrading Multisig Tapscript

Finally this one is a little bit more orthogonal to all of the other ones. You can have degrading multisig Tapscript. This is an interesting concept. Without lots of generality this is what I’m going to show you. On the Tapscript spend side you can have something like 2-of-3 and then after some timelock 1-of-3. You can imagine if it is 3-of-5, then after some time 2-of-5, after even more time 1-of-5, something like that. You can have all of those branches. It doesn’t have to be 2-of-3 there. You can have 3 leaves off of there that are 2-of-2 each. It could be MuSig, it could be whatever. Just the idea that you have this option of a timelocked multisig that degrades gracefully.

## Timelocked (k-1)-of-n Tapscript

Tapscript
```
1 year
OP_CSV
OP_DROP
PubKey A
OP_CHECKSIG
PubKey B
OP_CHECKSIGADD
PubKey C
OP_CHECKSIGADD
OP_1
OP_NUMEQUAL
```

Witness
```
‘ ‘
Signature for B
‘ ‘
```

Execution
```
‘ ‘
Signature for B
‘ ‘
1 year
OP_CSV
OP_DROP
PubKey A
OP_CHECKSIG
PubKey B
OP_CHECKSIGADD
PubKey C
OP_CHECKSIGADD
OP_1
OP_NUMEQUAL
```

The actual timelocked (k-1)-of-n Tapscript looks something like this. This is the 1-of-3 case. Essentially you use something like OP_CSV to say “This is only valid after a year of it being onchain”. The rest of it goes through the same way. If you have a valid signature from one of the keys after a year then this would work.

## Degrading Multisig Tapscript - Advantages/Disadvantages

The nice thing about degrading multisig is that you get backup in case of key loss. Somebody loses it or something like that. The other really nice thing about degrading multisig is it is kind of like built in inheritance or estate planning. This is of course for a lot of Bitcoiners not something you think about. What happens if I die? How am I going to make sure that my loved ones get the Bitcoin and it doesn’t get donated to the rest of the Bitcoin community via never being able to spend it again? That is through using something like gracefully degrading multisig or having a backup or something like that. It is kind of nice that we get these advantages. Again because of the way Taproot works you can throw it in there as one of 100 conditions that are similar or like this. The major disadvantage is that the funds have to be moved before the timelock or else they can take it away from you. Of course you might have security by obscurity, they don’t know that they are part of the backup or something like that. In which case maybe you can get away with it. But generally you are going to want to move it on a consistent basis depending on when that is. That kind of sucks because that is going to cost you money.

## Contact details

These are my places that you can contact me: [Twitter](https://twitter.com/jimmysong), [GitHub](https://github.com/jimmysong/), [Medium](https://jimmysong.medium.com/), [Substack](https://jimmysong.substack.com/). The [URL](https://jimmysong.github.io/taproot-multisig) in the upper corner. Thank you.

## Q&A

Q - Size wise, if you go down the Tapscript path you have to reveal the internal key and then the inclusion proofs did you run some numbers on the size of the script where it starts to become beneficial fee wise?

A - It turns out each level of the Tapscript is a 32 byte additional hash. Because of the SegWit discount that’s 8 more vbytes for the purposes of calculation. Each pubkey is also 32 bytes so that ends up being about 8 vbytes. Roughly speaking each level per pubkey, that ends up being the equilibrium there. If you have more than one pubkey and you only go down one level it might make sense. You can run the math on that but depending on how much you want to do and what the probability of using that particular path is you can optimize based on that. That is why I put the 2-of-3 up one level because that’s the most flexible, the most likely to be used and also it is the most costly so you want to reduce the spending on that and balance it out. It depends on your use case obviously.

Q - On MuSig in different branches, does it make sense then to make it 2-of-2 MuSig in the key path spend and then you have a flat 2 other 2-of-2 MuSigs on the script path spend?

A - That’s definitely an option. If you know A and B are going to be more available it is going to be cheaper to do the key path spends. That is definitely another way to do this particular one.

Q - My understanding is that what we got in the Taproot upgrade was one set of things but there are still maybe some other future upgrades. I don’t know if it is MAST or sig agg. What’s the jump from what you just presented to those potential future upgrades? What can and can’t be done? Do we have all this right now or are there some missing pieces?

A - Nobody has actually implemented a lot of this. Especially hardware wallets and stuff like that. We’ve been talking to them about how we are going to do multisig in a Taproot world. They’re like “We want to do the easiest thing” which I think is single leaf multisig because that’s as close to the traditional multisig. They don’t want to think about all the other ones. I think we need to get some of these other things in there and make it a standard. I would love to see an everything multisig be standard and sign the various things as you need. A lot of the capabilities are there to be coded but really it is up to you guys, this is a developer conference, whoever is working on a wallet, go and make this. Selfishly I want to be able to secure things this way. Have all these different options and as a coder implementing this for my library [BUIDL](https://github.com/buidl-bitcoin/buidl-python), it is great. It is very forgiving for developers because you can completely screw up one of the branches of the Tapscript and it doesn’t matter. The other ones are completely independent of it as long as you have the hashes or whatever. You can just reveal and still spend on that particular Tapscript path or the key spend path. I just want more experimentation in this area. I don’t know necessarily what the best UI is or what the best UX is but let’s get some more options out there because we’ve got some really nice capabilities.


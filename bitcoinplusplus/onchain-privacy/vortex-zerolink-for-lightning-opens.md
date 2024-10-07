---
title: 'Vortex: ZeroLink for Lightning Opens'
transcript_by: jasonofbitcoin via review.btctranscripts.com
media: https://www.youtube.com/watch?v=d1HIBE4fCmE
tags:
  - lightning
  - coinjoin
speakers:
  - Ben Carman
date: 2023-12-09
---
(The start of the talk is missing from the source media)

## What is a blind signature

All these people could come, and they all can then present their signatures.
And Bob will know, "okay, all of these signatures are correct, but I don't know who gave me which one.
You'll see how we use this in the protocol to get some privacy.
This is kind of the structure (referring to slide#2).
There's a single coordinator, many clients connected to it.
They can be Core Lightning, they could be LND, they could be bitcoind or anyone who implements the protocol.

## Registering Inputs

So it starts first where you just register inputs.
So you have Alice here, she wants to do a CoinJoin.
So she says, "Here's my inputs. I'm gonna be spending these UTXOs."
And where she wants to send the money is gonna be blinded.
So that'll be that first case here (referring to slide#1) where Bob has already given her the nonce, but Alice will then blind that address as the message, and then she gives the change output for the extra stuff.
And now the coordinator needs to validate a bunch of stuff to make sure that she's not malicious and trying to DDoS attack or steal money.

So the coordinator verifies that these are actually real UTXOs, needs to verify that Alice gave her a valid proof that she does own these, that they aren't already registered, and that they're confirmed, and then that they're of the correct type, because we don't want all the inputs of these transactions to be different types.
If they're all taproot it makes it much cleaner and harder to track who's doing what.
And then we also want the minimal amount of UTXOs selected.
So we don't want her to come in and just give all of her UTXOs and then just get a free consolidation because it's kind of just hurting the overall protocol.

So if they validate all that, Alice is good, an honest party, we'll give them that blinded signature.

## Registering Outputs

And then later, once the round is ready to happen, Alice will then, under a new Tor identity, give that address, the unblinded address, to the coordinator and that unblinded signature.
So this allows the coordinator to verify that this address has been registered by someone, but because they don't know who actually the signature was for, they just know some party is giving me the signature.
So it could have been Alice, it could have been Bob or Carol, whoever registered for the CoinJoin. Just someone gave this address.

So now the coordinator can't link the address to the inputs.
So it gives you a nice you-don't-really-need-to-trust-coordinator-with-your-privacy kind of properties.

### Validation

But they need to do some validation.
Again, Alice could be trying to steal money or do a denial of service.
They just basically verify that, okay, this is a signature that I gave for this round.
And they just verify as well that the address is correct type so they're not screwing with the round.
So, you know, if this is a Taproot round, we're verifying that they gave me a Taproot address.

## Signing Phase

And eventually, once everyone registers their outputs, we need to sign that transaction.
So the coordinator constructs the PSBT, (and) sends it to every person that's registered.

Now, Alice doesn't wanna trust the coordinator, you know, maybe the coordinator's just sending all the money to themselves.
So Alice needs to verify a bunch of stuff, and as well, she wants to protect her privacy.
So she verifies that all these inputs and outputs are the correct type, and that they're not trying to screw her over by putting in random stuff.
Alice verifies that her inputs and her outputs are included.

Something I always think about, I have a comment in my code, is like, should Alice even verify their inputs are included?
I mean, she'll take the free money, but we do, for now, just to make sure there's no bugs.

And as well, she needs to verify that the transaction can actually be broadcast.
You don't want to do this stuff and then the fee rate's like zero so they can't be broadcast and you just wasted your time.
So she verifies that it's a valid lock time.
There's nothing over the dust limit and the fee rate is good.

If all that's good, then Alice -- if she's opening a Lightning channel -- she'll validate it with her channel counterparty, to be like, "I'm gonna open a channel with this transaction. Is that cool?"
If they give her the OK, she'll sign it and then send it back to the coordinator.

## Complete

And then once everyone has signed this transaction, the coordinator can then create the fully signed transaction.
And they'll broadcast it and send it to all the peers.
And they can broadcast it themselves as well, just to get it everywhere.
And that's kind of the completion of the round.

## What does ZeroLink give us?

So what does that give us?
Because of this blind signature stuff we were doing for registration, the coordinator can't link inputs to outputs.
So that lets us really have this nice property.
Where (with) something like a custodial mixer you're really trusting your privacy with that mixer because they know where the money is going to.
But (with) this you never have to trust them with your privacy, because the worst case is, like in this first case, they know which UTXOs you registered together, but that's not the end of the world because normally you lose that with chain analysis anyways.
And they can't link your inputs to outputs, so eventually if you just register one input for a remix, then you should be safe.
And you're never giving up custody of your funds, because it's just a single transaction that you sign and send to whatever address you validate.
You're never giving up money to someone else.
You're always in control of your own keys and never have to trust anyone there.
And the coordinator can protect against denial of service by just banning UTXOs that are bad actors.
So, if Alice comes in and in this phase (registering inputs) and sends me UTXOs that don't exist or a bad address, or in this phase (signing phase) she doesn't sign, then we say, "Okay, your UTXOs are banned, so you can't come back and denial-of-service-attack this thing again."

## Current implementation

"That sounds pretty complicated, like, I don't know how to implement all that."
Well, you don't need to.
We have a nice, hopefully a nice-looking GUI that handles it all for you.
But that's kind of the idea.

Does it work?
So we've done one mainnet one, so it kind of works.
I've done a few on testnet, works on regtest great.

## Challenges

There are some challenges that I want to get into.
Some of them specific to Vortex, some of them, just, I don't know if they are solvable problems.

### Tor

The first is Tor.
Tor sucks.
It's very slow and unreliable.
And the biggest problem is it can cause honest peers to look malicious.
Where, you know, if in this case (signing phase) where Alice needs to sign, and she doesn't sign because her Tor socket got disconnected.
Well now, the coordinator's gonna think she's a bad actor and ban her, but it's like, well, no, sorry, I just have shitty internet.
Or, you know, maybe I have great internet, but Tor just sucks.
So there are some solutions.
I mean, you can use clearnet.
The problem is, with clearnet, you kind of will now have some trust with the coordinator with your privacy where if the same IP address registers this input and this output, now they could correlate it.
So another solution could be I2P.
The thing is though, it's not a total drop-in replacement and has some slightly different properties than Tor, but it could be a solution.
But it is way less used than Tor, so you won't have as great an anonymity set and stuff.

### Max Pending Channels

Another problem is something I realized after doing the mainnet test.
It's something called max pending channels.
So, most lighting nodes only allow, at least by default, one pending channel from another node.
So if I attempt to open a channel to you, I can't attempt to open another channel to you until that whole thing either it's denied and cleaned out or it's confirmed.
So this can cause a problem during blame rounds.
So basically if a peer comes in and acts dishonest, like say they don't sign the PSBT, what we need to do is, basically, we redo the whole round to figure out who was the dishonest peer, and then we just exclude them and do the round correctly.
The problem is, you end up re-initiating that channel with the person you're trying to open a channel to, so you can go over this max pending channel limit.
So it's kind of a hard problem to solve.
I'm not really sure what the correct solution is.
Potentially it could be moving to interactive-tx, like the Lightning dual-funded channel protocol.
I still need to research this, but LND doesn't support it.
So it would greatly reduce the user base and thus anonymity set of the project.
And I'm not sure with interactive-tx you could get that privacy from the coordinator that we do get with ZeroLink.
So it'll be a massive trade off.
I still need to research that.
I mean, maybe we just do some advocacy and get everyone to raise their pending channel limit, but, we'll see.

[Audience]: "Do you know why that's important? Is it like a DDoS protection thing?"

Yeah, it's mostly a DDoS protection thing.
I talked to Lalu about it at TABConf.
He's like, I could just open a thousand channels to you and now you need to watch all these UTXOs and, you could just eat their DB and CPU time.
Thing is though, it doesn't really fix anything because I could just spin up a thousand Lightning nodes and do one channel to you anyways, but it's a little harder.

### Post-mix

Another big problem is the post-mix part of this, where LND and c-lightning really don't have good post-mix tools.
They just kind of have a basic wallet, because they spend all their time on the Lightning stuff.
So something that Samourai does really well is your post-mix UTXOs go to completely separate accounts, so it's very hard to spend them together.
For Vortex to have something like this, it would need to become a full node manager software where it's basically feature equivalent to something like ThunderHub or Ride The Lightning.
But even if we did all that, and it's like, if the user comes in and then uses something like Ride The Lightning instead of Vortex, they could accidentally just ruin their privacy by merging UTXOs they shouldn't.
And even if you're a perfect user, if you use something like anchor channels, which are like default in LND now, you could accidentally ruin your privacy because anchor channels what they do is, if your channel gets force-closed and you need to bump the fee, it just picks a random UTXO and bumps the fee with that, so you accidentally could be associating the wrong UTXO with the channel and then it ruins your privacy further.
So there are some problems there that could be like really big foot guns and you can kind of solve it, but not in the worst case.
So it's another hard problem, but, we can still move forward in that regard.

[Audience]: "Why don't you CoinJoin the change?"

Well, the problem is it's a force-close, so you don't have the keys for it, so you can only, I guess if all of your coins in your wallet were CoinJoins, maybe you're okay because now this random CoinJoin fund is being used to bump it, but if you had non-CoinJoin funds, then, because you don't get to pick which UTXO is used to bump your fee.
LND or c-lightning will do it automatically, so it could just pick the wrong UTXO, maybe it picks your toxic change, now bumps your channel with that, and now you just got rekt.

A solution around here would, if we had these separate accounts, you could say, okay, this is my anchor channel bumping account, and this is all my post-mix UTXOs, then it's maybe safe.
But the problem is LND and c-lightning really don't have support at all for things like that.
So it's a hard problem to solve.

[Audience]: "What do you recommend instead of running RTL (Ride The Lightning)?"

Ride The Lightning and ThunderHub are great. The problem is, if you're CoinJoining these funds, it's not gonna be aware that you CoinJoined previously. So you could do all this perfect CoinJoin stuff and then go into RTL and hit send, and it just sends it without knowing any of that stuff and merged the wrong UTXOs you don't want, or it just opens channels with the wrong UTXOs you don't want
You can't control it.
So it's hard to control things like that.
So, Vortex would need to become this full node manager software to handle everything.
I use RTL and ThunderHub interchangeably.
So, a user might use Vortex and RTL interchangeably and screw themselves.

[Audience]: "So you would need some kind of coin control in RTL or something like that?"

I think RTL does have coin control, but the problem is, it's not gonna be aware of the CoinJoins that you did in Vortex.
It won't know the anonymity set that you have saved in your database and stuff like that, because it's separate, so it still isn't a total solution.

[Audience]:  "RTL could calculate the anon set".

Yeah, I guess you could do that.
You know, then it becomes, you know, now I've got to start contributing to RTL and stuff, and I don't wanna write JavaScript code. [laughs]

## Scala lol

Another problem, though, is I wrote it in Scala, and I love Scala, but also, the main library I built on (Akka), totally rugged everyone, where they're changing their license now to not be open source.

Which is like the main networking library every Scala project uses.
One thing that really pissed me off is, they don't have support for mutual TLS, which is needed for c-lightning's gRPC.
I have a bunch of issues on adding it, and now it's like, even if they add support, I can't upgrade to the latest version because it's no longer open source, or, you know, the license is different.
So that one sucks.
But also, (in) Scala it's hard to make releasable binaries for every application.
So I'd like to rewrite it in Rust, but we'll see.
So that was most of it.
Some of you guys locked in towards the end, but yeah.

## Questions

Any questions?

[Audience]: "Do non-Vortex users join the Vortex CoinJoin?
Can someone not opening a channel with Vortex be in the same CoinJoin transactions as the Vortex users that opened the channel?"

That's something I got in before you walked in.
The dream is, once we have Taproot channels, we can have basically every kind of use case in a single CoinJoin because all the outputs look the same.
So you could have someone opening a channel and it looks exactly the same as someone doing a self-spend, same as someone doing a payment, or, you know, someone could be issuing a Taro asset for all we care. It's all in the same CoinJoin because Taproot lets it look all the same and, you know, the protocol works the same way.

[Audience]:  "How do you handle the amounts on the output side?"

We're just using ZeroLink.
So same way like Wasabi 1.0 or Samourai works, where we have multiple coordinators for different amounts and stuff, but yeah, it's all a unified amount.

[Audience]:  "And one denomination per round?".

Yeah, yeah.
I think right now the mainnet one I have set up is 5 million sats.
It's kind of a hard problem because if we're doing this dream of all these things in the same CoinJoin, it's like okay, a channel open, if I'm doing 5 million sats, it's kind of a small channel on average.
It's not something that a business might use.
At The Bitcoin Company we open huge channels to people.
So like a 5 million sat channel might be useless to us.
But if you're doing a self-spend or trying to get your own privacy, that's probably a good amount because if we had like 1 BTC rounds, now it's like you need to be fairly wealthy to be able to do a CoinJoin.
And something even like a Taro asset issuance, you want those to be pretty small because most of the value is in the Taro asset not the bitcoin.
It's kind of hard to unify all these cases with the amounts.
I picked 5 million sats out of a hat, but hopefully that works.
Anything else?
Well, thanks for coming.

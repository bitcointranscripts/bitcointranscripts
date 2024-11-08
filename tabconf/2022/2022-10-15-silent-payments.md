---
title: Silent Payments and Alternatives
transcript_by: Bryan Bishop
speakers:
  - Ruben Somsen
tags:
  - privacy-enhancements
  - silent-payments
date: 2022-10-15
---
## Introduction

I will talk about silent payments but also in general the design space around what kind of constructs you can have to pay people in a non-interactive way. In the bitcoin world, there are a couple common ways of paying someone. Making a payment is such a basic thing. ... The alternative we have is that you can generate a single address and put it in your twitter profile and everyone can pay you, but that's not private. So either you have this interactivity or some loss of privacy where you continuously reuse the same address.

This talk is going to be about trying to see how we can get both non-interactivity and also privacy in the sense that someone can't just look at all the payments on-chain and see how much money this single address got.

There are some protocols out there for this, but also some newer protocols. I'll show you what the range of these possibilities are.

## Handing out an xpub

There is something that I would call a semi-interactive solution which is not non-interactive but maybe there's a minimum of interaction. One of these methods is very basic where instead of when you interact with a person you want to pay they give you an address, they could instead give you a fresh xpub or a key from which they can generate multiple addresses. Instead of every time you want to make a payment to a person, you can interact with them just once. We don't do this today, but it makes sense to me for situations. It makes it more simple, to me. I've had many situations where a friend of mine we make some payments back-and-forth and it's always a problem to get a new address and maybe they need to go to their hardware wallet to get a new address. But if you only had to do that once, it would seem to be better.

One issue here is a gap limit. You make the gaplimit worse by doing this because you could hand out an xpub with a gap limit. One issue is that if you continuously hand out addresses, the way it works is that you have a single key from which you can derive keys for each person. When you recover from backup, you can generate the keys you might have generated and then go on-chain and find which ones were actually used. If you see a large enough gap of addresses not being used, then you basically assume I am done scanning or checking because the gap is there to protect you from scanning infinitely. But what happens if you hand out a ton of unused addresses? Well, you can bruteforce it to make absolutely sure that you're not missing any money, but this is still ugly.

In this case, because you're handing out an xpub, there could be a gap on the xpubs and also the xpub being used itself can also have gaplimit. If you hand out an xpub to someone, one observation is that you can basically there might be a gap in there too but considering if you can assume that it's the same person continuously paying you, then there won't be a large gap there. There's no reason for them to leave a large gap. That's one assumption that you can make to reduce the gap scanning on those xpubs to make this less worse. There can be a gap between different xpubs, though, based on what you gave out.

This is nice for recurring payments but it's still interactive. You still have this one-time interaction.

## Automated interaction

There's another class of solutions called "automated interaction" where you have a server you run and the server hands out addresses for you. This requires a secure always-online server which in practice is hard for users to do. All the developers in the room are saying sure no problem I'll do that but normies don't find that to be easy.

There is another big problem: it's still hard to deal with gap limits. If you have an automated server, then someone can access your server and keep requesting keys. You have this problem where you can easily hit the gaplimit. So we haven't solved for the gaplimit in this solution.

This exists today like with btcpayserver. I don't know how they handle the gaplimit. I think they wing it and do rescanning. I don't know if they have a good solution. I might be overlooking something there.

In practice, btcpayserver- merchants have used that, but it's not as common as it could have been at least.

## Trustless address server

There's another class of solutions that I haven't come across. I recently made a mailing list post called trustless address server. It's similar to btcpayserver but instead of you running your own server you let someone else run your server. One of the observations I made for why this would be reasonable to do is because we have lots of lite clients on the network that hand out keys sometimes the xpub or sometimes they generate keys and send them to a server. They already lose all of their privacy to a single server that does the blockchain scanning for them.

If we already have a server that we trust with a server that can completely deanonymize us, then why not also rely on that server to hand out addresses on our behalf?

We still haven't solved the gaplimit here. Either you run the server or someone else does, both solutions have a gaplimit problem. I have a solution to that, but I'll get to that in a moment. So now you're not running your own server; someone else is running the server. A new problem that pops up is that if a server hands out a key on your behalf, how does the person who wants to send you money, how do they know that the recipient is you? The server can try to steal money that way and it won't go to the person you intended it to go to.

The answer is that you need a key associated with the person you want to send to, and that key can sign all the addresses in the server. I can use that identity key to sign all the keys or addresses I give to the server. Now when someone gets an address from the server, they also get a signature from the server. This ensures that the server can't cheat and can't give out a wrong address.

This is sort of inbetween solution that we haven't really seen yet. It's only subtly different from btcpayserver. It's an interesting tradeoff. Specifically, this already assumes a non-perfect situation where you have some kind of lite client that you are exposing your privacy to anyway so you might as well use it for this. I think that this is not where we want to be in general in the bitcoin ecosystem with this kind of privacy exposure, but given that it is already happening, when you do it then this seems to be a good tradeoff.

## Dealing with gaplimit abuse

What happens if people just connect and request keys and do nothing with them, and therefore you can't find your funds because the gaplimit was exhausted possibly multiple times in between keys that were actually used for payments?

The first observation is that what you need is that you need there to be a cost to request an address. It's sort of awkward, you could say theoretically well send a lightning payment and get an address. But it's awkward that the person who has to pay you has to first make a payment on another network or something. It's theoretically possible, though.

However, another solution is that, having a UTXO or using a UTXO is a cost in itself. You can't have a UTXO without having some kind of on-chain costly activity. We can utilize the fact that when you make a payment you must have a UTXO and you can prove that you have this UTXO and we can utilize this to add a cost to receiving a fresh address.

After I posted my trustless address server concept on the mailing list with a rough sketch, David Harding replied and fixed some of the rough edges of my idea. He came up with something specific that improves my proposal and makes it quite elegant and seems more practical now. First, you give a non-fresh address. You contact the server, the server gives you a key, which may have been given out to some other user before. It's not a key that will be guaranteed fresh and maybe someone else has seen it before already. The person who wants to pay first creates a transaction that pays to this address which is not ideal, and hten they hand it over to the server. Once the server sees this valid transaction that they could send out to the blockchain, only then do they send out a fresh address to the sender, and now they sign again and broadcast the new transaction with the fresh address. The server, if it wants, can make you eat the cost. And only then do you get a fresh address and it gets broadcasted.

If the sender aborts at any time in between, like not responding after having a fresh address, in this case you just broadcast the previous payment on the non-fresh address. You can argue this is not ideal because now you are leaking, you are sending to an address that someone else has seen before. But if the sender wanted the payment to be less anonymous than ideal, then they could have already paid you to an old address of yours anyway. From the sender side, they already could have done that anyway and now you are just being forced into it by their non-response.

One thing that is interesting here is that it also helps out with the gaplimit. Let's say you are in a scenario where you are broadcasting this transaction on a non-fresh address, well you can make it so that it sits at right at the gap limit. If the gaplimit is 100, then you can have this key be the 100th key, you can hand that out before they are re-signed. If you are forced to put it on the blockchain, you are in a way reducing the gaplimit.

In terms of complexity, it requires on the sender's side to sign a transaction twice. There's some roundtrip communication. And also you have to check a signature on the public key, and the second transaction must spend the same input so that the server can't double spend the sender.

This can also apply to btcpayserver. This is all relatively new so if anyone has any feedback let me know.

## Shared secret using Diffie-Hellman

The non-interactive solutions all rely on a single trick. I want to talk about it first without cryptography and then later with. There's this thing where if the recipient shows their pubkey in public, so everyone knows your pubkey for instance, and then the sender somehow communicates their pubkey to the recipient then with these two keys you can generate a shared secret. The shared secret basically means it's some big number and only the sender and the recipient know it. You can do this trick using Diffie-Hellman with elliptic curve cryptography. Once you have a shared secret, you tweak it so that the address goes only to the recipient. The shared secret is spendable by both parties. You need to tweak it so that only the recipient can actually spend from it.

Big letter is a curve point. Small letter is a scalar. You can turn a small letter into a big letter which is what elliptic curve cryptography does. You can multiply aB and this equals bA. On the public side, on the outside, people only see B or A, and you can't do BA or AB so nobody outside the sender and recipient can calculate the shared secret.

To get a key that the recipient controsl, you do hash(aB)G + A where A is the recipient pubkey. This ensures that the final address is something that only the recipient can spend from.

## bip47: Reusable payment codes

One of the protocols using DH secret sharing is bip47. Another one is paynyms. There's Samurai Wallet. Sparrow Wallet I think implements it. It has seen some use. Compared to the average number of on-chain transactions, there's very minor usage.

The way that bip47 works, first the recipient key is openy published off-chain like on twitter or my homepage. I claim that this is me and ideally you would use some PGP system to make sure. The sender needs to notify me of their key prior to actually paying me. The way this is done is by an on-chain notification. You send a transaction that contains your key, and it's blinded. I guess it depends on the implementation. In this case, you don't want to recognize the relationship- you don't want to see who the sender and recipient are. You ideally want that to be a secret. You don't want to know who is paying whom, even though the actual payment going through later will be uncorrelated. The sender key is blinded. Once you put this notification on-chain, the recipient can see the key and start watching the key that corresponds to the shared secret. Once the shared secret is established, the recipient starts watching the receive address. Here, gaplimit is not a problem because you need an expensive on-chain notification instead of checking a gaplimit. Theoretically you could spam someone but it's not an interesting attack because of its cost and low payoff. This protocol is particularly inefficient for one-time payments. So first you need to notify them, then you need to send the funds. The general downside is the on-chain notification requirement.

In fact, in the current bip47 implementation, there is a problem where when you create the notification you are using some of your inputs to put some notification on-chain and you link some of your inputs to the recipient. There's some information leakage there. Well, you could say, don't use inputs you would otherwise use, and it's a huge mess to deal with privacy pools of your inputs. This is a big problem, I would say, for bip47.

## Why on-chain messages are controversial

There are two big questions that come up often here. Why are these on-chain messages so controversial? There are different opinions. Some people say well if you want to use bitcoin blockchain for on-chain messages then you should be able to, and others call it a waste. Where is this coming from? The initial thing to think about is that the blockchain is global and a notification is meant to be personal and local. It should only be between sender and recipient. Nobody else cares about this message. You're using the blockchain to do something that only concerns two people. In the blockchain, though, we do care about where all the coins are at any given time. We have all agreed to track the UTXO set. But this message is not really part of that. I think that's the fundamental philosophical disagreement there where it is possible to put the message on-chain, but really you'd rather not.

Another perspective and a more appealing argument to some is that as blockspace gets scarce, it should become uneconomical to do this notification activity on-chain. If you want to make a payment, then you have no choice to use bitcoin's blockspace to pay with bitcoin. But aren't there other ways to communicate a message?

More generally, we do have alternatives. This is not the only way to do it. So why use the blockchain for the notification?

This doesn't solve the problem but something to think about is that you don't really need to use the bitcoin blockchain. You just need global state that everyone agrees on. Do we really need to use the bitcoin blockchain? What if we use spacechains, litecoin, or ethereum to put the message somewhere else? I think it separates out the concerns, but doesn't completely solve it because blockspace is theoretically limited everywhere.

## Why the notification can't be sent off-chain

Why does the message have to go on-chain? Why can't we have Alice just send a message to Bob? Just give Bob the key? Isn't that fine? The answer is no but it's not as obvious as you might think. Say Bob gives his key to Alice, sends a message, and Alice never acknowledges that they receive it. If you start sending money before they even acknowledge that they got your key, then that's not ideal. You need someone to respond. But now you're back to interactive, and therefore we don't need a new protocol because you can just ask for a fresh address.

What about trusting a server to relay this message? This adds an element of custody. This key you're giving out is essential for receiving funds. The server can say well if you would like to learn this key maybe you can pay me or something, they can bribe you, there's counterparty risk, you lose control of your funds.

There's also this requirement of backing up data. Even if Bob tells Alice directly, you need to remember the thing you received. Instead of having a single seed you backup once, now you need to do backups every single time someone gives you a key. It's not impossible, but it does add complexity.

An interesting thing that the blockchain does is that it guarantees that a notification will arrive. There is an inherent assumption that therre's a lot of mining, these blocks will be distributed, and if you put it into the bitcoin blockchain then you can basically guarantee that whoever needs to see it will see it eventually. That's what makes the bitcoin blockchain so useful in this case. The blockchain solves the problem and it also prevents spam because putting messages on-chain is expensive.

It's interesting to think about. Alice is sending a message to Bob. She is using a third-party, which is the blockchain, which is a very reliable third-party.

## bip47 variant: Prague protocol

We were discussing if there were any ways we could improve bip47. The idea is to solve the problem before in bip47 where you are using your own inputs to send a message to the recipietn and now you are linking some of your coins to the recipient with an intention to pay. If you could ask someone else to put it on the blockchain on your behalf, then you break the link. You can also batch these notifications. You could have a single person that agrees to do this and they put a single OP\_RETURN or some tricks to put it into witness data into a single message. There are some tricks where you can decrease the size. The key of the sender would have to be put in there, and then the recipient would have to know the message is meant for them. You can get away with saying well I will only use the first 4 bytes of the recipient key, and then there might be a collision but it turns out that the cost is not that high because it turns out that they generate an xpub and start watching is not a high cost so you shouldn't worry about those collisions.

There is a tradeoff where one trick that bip47 does or one design goal was to make it as compatible with existing software as possible. You could say, well, I want to make this as easy as possible for people to adopt this. Or maybe you want to make this more efficient but cause the ecosystem to have to do more work. The choice that bip47 made was, let's make it as compatible as possible. ... yo uwould be notifying your recipient by creating an output that only they can spend or that they can recognize in a way that is currently recognizable and see that they are getting paid in the normal payment flow of how payment workflows today.

One obvious downside of this is that the person who is batching these notifications has to get paid out of band like through lightning network.

## bip47 variant: private payments (bip351)

Here's another variant. This took the Prague protocol and made a few small tweaks, one big change. It replaces the outsourcing to blinding. Instead of having this requirement that someone else needs to put the information into the blockchain, you can take the information and blind it in such a way that nobody can see who the recipient is. While this is a nice thing, it also introduces the other issue where the recipient doesn't know which messages are meant for them. So now they need to download all the notifications, whereas in the prior 2 protocols you only had to look at messages that had your xpub in it. So the recipients have to check all notifications.

On the plus side, there is no out-of-band payment required. It's a bit of a tradeoff. We'll try to speed this up a little bit. This is a tradeoff that I personally don't really know if tihs is an improvement or not. I think people could have different opinions on this. On the one hand you have no OOB payment requirement, but now you make it harder for lite clients to check all these messages. I'm not personally convinced it is an improvement, but it's something. Also it uses OP\_RETURN to put the information there.

The person actually sending the money can put the message on-chain and put it into OP\_RETURN. This would definitely not be compatible with current software and there would need to be some way to relay the OP\_RETURN messages to the clients that want to use the protocol.

## Robin Linus' stealth scheme

Skipping this. I might put a link up. Follow me on twitter and when this video goes out, I'll put a link to this scheme.

## Silent payments

There's a different tradeoff in silent payments. We rely on the data already put on the blockchain to generate the shared secret. Given that you are paying someone, you already have a key that you use to pay someone with. You have the input key. Why not use the input key with the key that the recipient has made public? Why not use that to derive a shared secret? We can do that. It requires no extra on-chain data. The transaction looks like any other transaction. That's nice.

But now there is a scanning requirement: a recipient doesn't know whether or not they are getting paid. The only way to find out is to check every single message and go through it, derive a shared secret and figure out if this is an address that belongs to you. I have some ideas for how this might work for lite clients. It's sort of like if you run a full node already, this extra effort is sort of negligble. You put in effort to validate all the blocks, and now you have to do one more curve operation to check every single one next. As a full node, this would be invisible to you. You would have a single key, everyone can pay to it, and you just notice the payments.

There are some points of complexity. I won't go into it due to time.

## Overview

If you have a situation where you can at least interact once with the recipient, my recommendation would be to just hand out an xpub. Give them an xpub and let them pay you multiple times. If the server knows your keys, and you have a lite client that hands out keys to a server, then use the trustless address server. If you run your own server, you can run btcpayserver or run a trustless address server yourself. If you are okay iwth the concept of on-chain notifications, then you can use bip47 or one of the variants. If you run your own full node, then the silent payments model is the obvious way to go I think.

I also had some slides on coinjoin for this.

Ther is an implementation of silent payments by w0xlt on github. It was a proof-of-concept not intended to be merged into Bitcoin Core at this time. Performance looks good. He made some changes like multiple inputs. Payment purpose tags are a way despite having a single address be able to recognize why someone paid you. Maybe you are accepting donations, but maybe you are accepting donations for two separate reasons and maybe you need to be able to distinguish the reasons. More help is welcome on code, code review, or writing up a BIP for silent payments. I personally have too many projects myself right now but I would be happy to supervise and help out.

<https://tiny.cc/somsen>

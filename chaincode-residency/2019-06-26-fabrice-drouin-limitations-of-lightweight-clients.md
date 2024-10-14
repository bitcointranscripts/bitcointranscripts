---
title: Limitations of Lightweight Clients
transcript_by: Abubakar Nur Khalil
tags:
  - lightning
  - lightweight-client
speakers:
  - Fabrice Drouin
date: 2019-06-26
media: https://youtu.be/ULVItljEiFE
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-26-fabrice-drouin-limitations-of-lightweight-clients/
---
Location: Chaincode Labs Lightning Residency 2019

## Introduction

The limitations it's uh you have to fight when you want to build lightweight clients mobile clients so this again, this is how mobile clients work, you scan payment requests, you have a view of the network that is supposed to be good enough, you compute the routes, you get an HTLC, you get a preimage back you've paid.

So a Lightning node is a Bitcoin node, as in, you have to be able to create, sign, and send Bitcoin transactions on the Bitcoin network. You have to be able to monitor the blockchain to detect when a funding transaction has been spent, but you also need to maintain a routing table that's used to compute payment routes and it has to be good enough, it doesn't have to be perfect, it has to be good enough so that your payments will not fail and on a mobile phone it's a bit of a challenge, so the first part you need to implement is a Bitcoin wallet, so I assume that you can't really have a full node on your phone.

I know that some people are working on it but I am not sure it's realistic right now so you need to choose an option and you don’t have that many options to choose from so you can use bloom filters, do you all know what bloom filters are? BIP 37, okay. Uhm, you can use neutrino, you all know what neutrino is? Very impressive. Wo--a, okay so let's check, why do you call bloom filters uh server-side filtering and why do we call neutrino clients-side filtering?

[audience member gives inaudible answer, and another answers "computations"].

Suppose I am a Bitcoin node and I support BIP 37, and I know there aren’t that many of us left, and you're all "BIP 37 wallets? What exactly, what does it mean?", It's a bit of a mess because if I have two [inaudible] wallets connected to me I have two different filters to juggle and margin and it's a bit of a mess, neutrino is very different, it basically it will give you a very compressed view of blocks but it's a compressed view that you can query for things. So basically we get filters and you will filter for things that you want on the client which is why it's called client-side filtering and which is why it's way better you don't reveal information about what you're interested in. That's the two basic options if you want to implement everything on the clients, you could use an API, a lot of people use APIs I think that's what H-[inaudible] is doing with its wallets, I don't know about trezor, which means you need to roll your own servers and people need to trust you to some extent or you could use electrum servers so who knows a bit about electrum in the protocol and how it works.

I know that electrum is not really popular now because of the phishing attack. They've been fighting for like months. Yeah, but it's Python blah blah blah but it's very very clear, the electrum protocol is very very clever because what is missing in the Bitcoin protocol is indexes.

[audience member interjects]

I would say that if you compare, ok, it's recording

[audience members laugh].

If you compare Bitcoin to Ethereum I think one thing that Ethereum, I wouldn’t say they get it right, but that's why people think,  with Bitcoin a lot of the complexity is pushed toward the clients. If you want to work with Bitcoin, if you want to get information about Bitcoin core nodes you have to do a lot of work yourself, a lot of work. If you want to implement a wallet it’s- building a wallet is much much harder than it looks. I don't know if you think it's easy but it's really hard because you have to do a lot of work on the clients.

Ethereum it’s the opposite. Basically it's very easy to build a wallet because it's a balance-system and not a UTXOs and basically building an Ethereum wallet is very simple and what you need when you're building wallets is basically an index. You need index information: what are my UTXO's, have they been spent, and this is something that is really hard to get, almost impossible to get, with Bitcoin Core as it is today.

I did once - I think it was 2 years ago - ask the core devs to add a spent-by index but that's why we chose electrum because electrum, basically it will give you a lot of indexes, it will index your, the protocol is really clever, it indexes script hashes, as in, hashes of b-[inaudible] scripts. So it doesn't really matter if it's SegWit or not SegWit, you will really really be able to quickly find information about your UTXOs, your transactions, and we started with bloom filters with Bitcoinj and don't work with Bitcoinj.

We gave up after a while and we switch to electrum servers and we were fairly happy with our choice, even though we are looking at neutrino, because neutrino is a really nice model. But we think that it will not be as efficient when it comes to bandwidth. Neutrino would probably get you to download a lot of data, lots of blocks, electrum is extremely efficient in many ways, yes. Because of the phishing attack, I'll talk about the phishing, actually it’s beautiful. I talk about this, it’s really a nice attack [audience member laughs],

[audience member asks inaudible question]

You tell it 'I'm interested in these script hashes' and it will give you history and transactions that are connected to these script hashes, so basically, yes, it knows. That's one of the issues with the API's and electrum, the server's know a lot about your UTXOs and if you use - and that's what we do right now. If you use the same servers to retrieve information about your UTXO's and to publish transactions then they really know what is yours, so yes, it is very likely that's some analytics company are running electrum servers, but you can use electrum over Tor which is like mitigates a bit the issue.

Monitoring the blockchain is difficult on a mobile phone because they will be offline very often. If you are offline and if your peer publishes an old state and if you miss a penalty window, you will lose money. This is why again Eltoo is a much better solution because that problem goes away.

So, you have two options, you can use really long timeouts but when your channel gets closed it means you need to wait a long time, like two weeks, before you get your money back, which is again really hard to explain to newcomers. Or you can delegate blockchain monitoring to a third party that's the watchtowers. Something I should have mentioned, you have today -- you have three types of mobile wallets, like the full nodes that we try to push, you have remote controls, and you have custodial wallets, remote controls. If you can run your own full node and Lightning node and connect to it, then yes. You have less privacy issues. You have a really specific security issue. It means that there is a server somewhere running either in the clouds or in your closet with an API to spend money.

There's something that we used at the beginning. We don't use it now, but I thought it was really nice. There's one case where you don't need watchtowers or to monitor the blockchain at all. It’s when you're only sending money. You know why you don’t need to monitor the blockchain? All you do is -- because all states will be in your favor, so it doesn't really make sense for the other guy to publish an old state. And if they do, why not more money for you?

That’s why for a very long time we didn’t have the option to receive money  -- I mean, you could still make more by punishing them though -- yes, but then not having to monitor the blockchain was a huge goal for us. So when we started, we had a really small channel delay and we could only pay, which was I think really good for UX.

So, watchtowers -- are you gonna have a talk on watchtowers? No? Ok, I will explain. Since we have the original author of watchtowers with us I’ll try to explain the watchtower ID. Basically you delegate monitoring the blockchain to someone else, but you don't want them to learn anything about what you're doing. You don't want them to learn what your channels are, what your payments are, and basically the watchtower is supposed to react when your peers publish an old state and the watchtower will publish the penalty transaction.

One of the first watchtowers designed, which is really nice, is you send a penalty transaction for each commitment transaction that you sign and you encrypt the penalty section with the first, or the last, it doesn't really matter that -- one half of the commitment transaction ID and the watchtower only knows the other half of the commitment transaction ID.

So basically the watchtower is looking at the blockchain and they try to see if there's a transaction that has an ID that matches the 16 bytes you gave it and if it sees one on the blockchain it uses the remaining bytes to decrypt what you gave it that is the penalty transaction -  and it publishes the penalty transaction. So that's really elegant. It's really nice. The watchtowers don't know which channel they're watching and if no one tries to cheat the watchtower learns absolutely nothing. All they have is encrypted data that they can't really do anything with. There's a huge problem with that, it's that you need to store an ever-increasing amount of data. That's a big problem because you will have to pay for that.

For example, what's the difference if you're using cloud providers? What's the difference between buying virtual servers CPU-wise and buying storage? Why is it a bit cheaper to buy -- well, why do you have cheap options to buy CPU but you don't have cheap options to buy storage?

[audience member provides inaudible response]

Exactly. Because cloud providers will overbook basically, they know that you won't be using your CPU one hundred percent all the time so they can overbook CPU allocation.

[audience member chimes in]

Yeah, but if you want to use block storage even if you don't you -- if you want 300 gigabytes and use 10 of them, you're gonna pay for 300 gigabyte. You can't really overbook storage. So it's not cheap to implement watchtowers the way that with this particular design because you need- basically you're giving an interface for people to write on to your disks so that's really hard to incentivize.

[an audience member chips in]

Exactly, Eltoo again, with Eltoo all you -- it's a huge change with Eltoo all you need to remember is the last state that's it. So now I come to the other UX issue we are facing especially on mobile phones. The first one was stack payments. It's the biggest issue for lightning I think right now. The second one is, it's not that much of an issue, except if you want to build like lightweight wallets, is how to get a good view of the network. This is something you already see many times.

Source routing works because you need to have a good view of the network to compute the onion packets. And if your view is not good enough you will get the updates that you're missing because you computed the fees wrong or your CLTV deltas are wrong but your first payments will be slow as you learn your updates when you receive error messages your first payments are so -- it's something you can actually see if you use Eclair and if you haven't used it for a few days you start and you try to pay. You can see that the first payments are slow because we're failing. Actually what's happening behind the scenes is we're failing. We're learning about new updates and we are trying to get the new updates. It's bad UX. What you want is to be able to have a really good view of the network as quickly as possible. So that's what we call the routing table synchronization issue in Lightning. The first version was extremely basic, you download everything every time you start, so it was very efficient for mobile phones. It became very inefficient for everyone so we just -- we're not using that anymore.

The second version was you download all the channel IDs that they have and you compare against the ones you have and you ask what you're missing. But it's -- these too were not too efficient so we've proposed - it's not been merged yet - to add timestamps and checksums to the filter queries to make filtering more efficient. You can avoid downloading channel updates that are older than the one you have and you can avoid downloading channel updates that carry the same routing information as the one you already have. So that's something that we're working on right now. A lot of people think that set-reconciliation techniques like inverting bloom look-up tables or minisketch could be applied to that problem. Basically, there's -- you two nodes with two routing tables either you use set-reconciliation techniques to synchronize uh views of the network. I'm not convinced it works. I know that Matt is absolutely convinced it should work.

So one way we're fixing this is to just not compute routes on your phones and delegate routing to another server. It's implemented by, is it, Lightning simple wallet, Bitcoin lightning wallet, Bitcoin Lightning wallet? It's pretty bad for privacy because basically that node learns who is paying who and that's I think that is pretty bad. It defeats the point of using source routing and the last slide is about implementation issues that are specific to mobile platforms. Basically everyone asks us when we can have a wallet for iOS and it's currently not possible because there are no JVMs for iOS and it's really very hard to have one because for example JVM uses just-in-time compiler. It will generate executable code from byte code and it's something that Apple doesn't want anyone to do. They don’t want people to generate executable code from data, so we're not going to have an iOS wallet for some time, unless there's a breakthrough somewhere. And Android is stuck at Java 1.7 which is obsolete for most cases. So that speaking, it's a bit of a problem now. We think Google will fix it but it's getting a bit difficult.

I think that yes, in the future, we have lots of ideas on how to improve UX. We have, I don't know how many uses, I think is 20,000 for the web, which is not too bad. And more importantly I think if we have to make sure that we can build mobile wallets. If we give up things on the lightning specs so that it becomes impossible, then we would have lost something that is really important. So we still want to push the ability to build mobile wallets even though some people may prefer to use remote controls or custodial services. Obviously onboarding with custodial services is much much better but we need to be able to build mobile wallets

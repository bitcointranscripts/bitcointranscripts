---
title: Current And Future State Of Wallets
transcript_by: Bryan Bishop
tags:
  - lightweight-client
  - psbt
speakers:
  - Jonas Schnelli
date: 2018-07-03
media: https://www.youtube.com/watch?v=CO2NXDWJa08
---
<https://twitter.com/kanzure/status/1014127893495021568>

## Introduction

I started to contribute to Bitcoin Core about 5 years ago. Since then, I have managed to get 450 commits merged. I am also the co-founder of a wallet hardware company based in Switzerland called Shift+ Cryptocurrency.

Wallets is not rocket science. It's mostly about pointing the figure to things that we can do better. I prepared a lot of content.

## Privacy, security and trust

When I look at existing wallets, I see the triangle of privacy, security and trust. Sometimes we forget about this. The triangle is between trust, security and privacy. In privacy, I mean what Adam just talked about- who knows what you are buying or what transactions you are doing, it's about transaction and script privacy. In trust, I mean no-trust required, we want chain validation, we want consensus. If that's not true then we are doing something wrong in my opinion. And the crucial part is security around keystorage and cold-storage. Who has the keys? Who has access to the keys? We are aware of that problem in the community, in general.

Bitcoin Core does okay work on privacy, not at the level that Adam just talked about-- it doesn't use any bloom filters, though. Trust, we agreed, it's a fully-validating node. Security, though- you don't get a hardware wallet. Out of the box, i's not doing well on the security side.

If you look at coinbase, there's a lot of red here-- no privacy, no security, no trust. This is not what bitcoin should be.

Trezor is a well-known hardware wallet. They do okay work on security. But hwo about privacy and trust? When you use the native trezor interface, you have no trust model, it's central validation, and there's no privacy. You send your transactions to their service.

If you look at SPV wallets like Android Wallet or BreadWallet, they do some form of trust using SPV validation which is better than using a centralized server. The privacy isn't really there. Seurity, I would not recommend keeping funds in a SPV wallet, because it's really just controlled by Google or Apple. If they upgrade to something that sends private keys, then that will happen. So there's no guarantee that those funds will stay in your smartphone.

Electrum is another model of how it works. They do SPV validation- not with bloomfilters, it's different. There's basically no privacy here... electrum servers. Security, same problem with Bitcoin Core, there's options, but it doesn't come out of the box. You need to buy a haredware wallet, and then use a native interface.

## Centralized validation

What is centralized validation? Some people think it's great or a good invention. I think it's a root of evil practices we currently do. Centralized validation means that-- let's figure out why people use centralized validation first. New users tend to use centralized services like coinbase or same like trezor or these solutions. They don't want to spend time on the validation lead time, which can take days. They don't want to spend 100 gigabytes on downloading to verify the whole blockchain. And same is true for the CPU requirements.

Solutions in practice-- there's two today. There was another announcement on the mailing list. Another software for centralized validation-- so you index everything and you have access to all addresses, similar to blockchain.info. But in my opinion this is against the philosophy of bitcoin. It's you trusting someone else's validation. You should self-validate what you are going to look at. It's probably the root point of some evil practices.

Centralized validation is handy. There are some benefits. Okay but first the downsides: anyone can inject fake transactions, for an SPV wallet, it's the same problem. If I change a fewl ines in my full node, I can make SPV clients think thay have received 100 BTC. You don't have any control over the consensus layer- if they are going with a fork, then you will be going as well. If you follow the software, then you follow the fork. And privacy is completely abandoned in centralized validation.

Why are people using centralized validation? Well, it's immediately usable. You can't ask users to download 100 GB of data and wait hours or days. It has very low bandwidth costs-- essential for smartphones. And you can serve large amounts of wallets. If you run a company where you need to serve 10,000 wallets then that works. It can make sense in that context.

Another thing is centralized key storage. It's not like validation. It's more like key storage. I think there's no reason to do centralized key storage. You might disagree, but I think there's no reason. You don't need any security setup. On the other hand, what security elements you have to assess that centralized key storage... what algorithms do you use to analyze coinbase? In my opinion, if you use centralized key storage, you don't own bitcoin. The one owning the keys are the owners of bitcoin. You might have a right to receive those bitcoin eventually... it's different. This is why coinbase is an unlicensed futures exchange. Users think they own bitcoin here, but they just have a right to moving the coins or something.

## Simplified payment verification (SPV)

In simplified payment verification, which was described in Satoshi whitepaper section 8... the root idea with a merkle tree, getting leafs, then calculate the hash, or verify hte hash. What's a great thing about SPV? You can verify headers, which can be lightweight, you don't need to get all the ... to do PoW. You can inject consensus rules and download a few blocks and verify size.. There's some weak zeroconf handling. You don't know if funds coming in are really funds coming in. That's a really complex, broken concept. On a SPV level, it's even wors e. Also, you're a network leech, and you don't give anything back- you're just downloading data and not helping network health. And also, you are relying on a free service. If everyone is running SPV and full nodes are hard to run, then there might be a bottleneck there, because you are relying on a free service. And why is someone providing that free service? Maybe they are hard-core bitcoin users, or maybe its' an agency that wants to spy on the network. Free estimation is probably impossible, there's no model for doing that with SPV. Fee estimation means you need a mempool. To have a mempool you need the UTXO set, and to have a UTXO set, you need a full node right now. So fee estimation is another area where you need trust. And also, they tend to rely on DNS.

On the other hand, SPV has acceptable bandwidth consumptions. Mike Hearn was the original driver behind bitcoinj before bluematt. Also, you have an acceptable amount of decentralization around validation.. He thought that using bloom filters was enough for privacy, so you just avoid telling addresses to a node, and set the false positive rate. The set is a bit bigger. But it turned out that the  priacy stuff holds..

## SPV privacy

Bloom filters are used by Android Wallet and Bread Wallet.

Electrum has a bit more centralization, and it has different SPV. You have sort of man-in-the-middle protection by using SSL/TLS, between you and the electrum service there are some privacy guarantees, but on the other hand yo udon't know who is running the electrum server. He might be running a VPS instance which might already be comprmised.

bip158 uses compact block filters. It has the missing concept of zeroconf that people like... people like seeing that Bob sent coins. They want to see that. bip158 has no solution to that problem. There are some solutions, but I think it's really hard to do these things in practice.

Then there's the hybrid SPV way and full block SPV where you downlload all blocks or you start your wallet at a certain part. If I download bitcoin core and create an ew wallet, then Ishould only download new blocks, because I know that my addresses are new.

Bloom filters, shortly... you send your transaction history or your transaction histogram to your peers, they do the filtering for you, it's CPU heavy. They provide this for free. You can send the filter, and they give back transactions, and they know what you need. A man-in-the-middle, the bitcoin p2p protocol is unencrypted. If you do it here at this event and the wifi is uncompromised, I could tell what you have bought and so on, due to the broken privacy.

## bip158 compact block filters

In bip158, it's a new proposal, and is in the process of getting finalized... there's some deployed versions and there's some concerns.. probably soon. The way how it works is you download filters, you don't tell nodes what to filter, and then you download filters and you figure out which blocks are relevant to my usease or wallet. Thisi s way better for privacy, but still, I'm not sure if you have two transactions and you downl oad two lbocks, then maybe someone can figure out which address you were using. Maybe there are some risks with privacy.

If you do client-side filtering like in bip158, there's a lot more bandwidth consumption compared to bloom filters. If you missed a day, you have to download 2.88 MB as an estimate. If you were offline for 30 days, then you dneed to downl oad 86.4 megabytes. It's maybe okay. Mobile users don't always have a lot of bandwidth available.

## Hybrid SPV

Full block or hybrid SPV-- you might need to download a few blocks for security. But if you go offline, and come back in a day, there's 144  megabytes you need. This is probably okay for a desktop, but definitely not a sm artphone.

You can slowly turn it into a full node because you have downloaded the blocks. There might be some missing history blocks but you can slowly turn into a full-block validating node, which is essentially what bitcoin is about.

We have resource costs in one axis, and decentralization in another. SPV is high resource and high dcentralization. Centralized validation solutions are both low resource costs and low decentralization.

## Future of wallets

So what is the future of wallets? I think this is a hard problem to solve. We should try to figure out that triangle of privacy, security and trust. We want something with green checkmarks in each area. You need som ething and it can't be just download something and it works or just buy something and it wroks. You need to confiugre, I think.

If you look at a full node-- and everyone thinks oh I can't run a full node my computer... and yeah maybe during initial sync, sure... this graph is the cpu chart for catching up for a month within 45 minutes. Once the node is in sync, it uses way less resources. So just think about that. It uses less resouces than Slack. So think about that. It's no longer a fan-blowing application.

Hybrid SPV where you slowly turn an SPV node into a full node... you do the header download, you download relevant blocks usign bip158, you can immediately use the wallet, and then you download missing blocks, then you do ful-validation, an then you upgrade transactions once they are fully validated.

You can  turn partial validation into full validation by downloading all the blocks. Bitcoin Core is made to validate as fast as possible to verify all the signatures. This is great for servers, but on your laptop, your laptop is no longer usable during that time, becauseo f the heavy resource utilization of Bitcoin Core. There are some pull requests that throttle the CPU intensity while verify. So then you can become a full node.

This is in my opinion very important. To me, privacy and verification (no trust) is not an opt-in model. This is how it should be. I think this is very important. The whole idea of bitcoin is to keep users away from trusted third-parties.

## UTXO set commitments

UTXO set commitments could be a way to bootstrap a full node. I think it's currently stuck with hashing the UTXO set, maybe rolling sets or somtehing. I think it's stuck there. Stuck doesn't mean no progress, stuff usually takes a lot of tiem if done right.

## Partially signed bitcoin transactions

Another thing that is interesting for wallets is partially signed bitcoin transaction format (PSBT) using bip174. This would allow that you can plug in any hardware wallet with every bitcoin wallet, with multisig and off-line signing. You could use bip32 paths, and raw transactions, redeem scripts, witness scripts, partial signatures. If we could have a good standard for hardware wallets, bip174 would be a good thing to work on. It's easy to understand if you have the time to read through it.

What if you produce a hardware puzzle that you can just plugin and it works? That's my dream. Bitnodes and things like that... people will be willing to spend a couple of bucks to have full validation in a node or wallet. Maybe not in the form of a raspberry pi and a handbook. Maybe you should just buy some hardware.

In Bitcoin Core 0.17, it's useful for a wallet backend. With partial bitcoin transaction signatures, you can use Bitcoin Core and wallet with fundrawtransaction you can do cold storage wallet transaction create. You can enforce watchonly in fundrawtransaction. If there's a proxy breach or a python server, you can create or update your wallet in your smartphone, without having bitcoin core in the background. Also, there's scantxoutset commands now. There's also a pull request for scantxoutset. That's how you can recover a backup. Usually when you use bip39 seeds, you have to recover teh whole chain, and scan back to the genesis block.... or you centralize validation... so the UTXO set would at least have your funds, you can scan the UTXO set in 30 seconds, and you don't have the transaction history, but you would have your funds.

NODE\_NETWORK\_LIMITED has been deployed. It's a standard for how pruned peers can be used for network health or for bootstrapping other peers, or how to bootstrap other peers.

Bitcoin Core is great if you have up to 200 wallets, but then it starts to get to be really not ideal. If you want to serve more than 200 wallets in an an enterprise case, that works. But if you need more, you probably need other infrastructure. This is a diagram where loaded wallets in the blue line versus used RAM in the purple line.

## Personal electrum server

Another thing that might need more attention is the personal electrum server from Chris Belcher. It's a great piece of software. You can use Bitcoin Core. You can index only your wallet. If you are going to startup an eectrumX wallet just for yourself, it's silly, because it processes the whole blockchain history. You could use a personal electrum serer on your own, which woud help. I think in that direction we should do mroe work.

In future wallets, going back to nopara73's talk, there's privacy in terms of coinjoin is important. Joinmarket is just an example.

I think it's impossible to have a great wallet experience without hardware, not only for key security but also validation. Your main computer tends to go offline and online. A mixed hardware solution is something I could see happening.

There could be multi-factor authentication. You could use multisig in a practical way. Multisig still knows that he stransactions hsuffling around it's not really useful... and fee estmations, it's not so rucial righ t now because there are low fees, but if we're going to fight again about block space, then I think fee estimation is important.

Integrate layer 2, like lightning stuff, I think that makes sense. We forget abotu this next one, but it needs to be easy to use. If you want more adoption, then it needs to be way more simpler to use, which means pluggig it in and it works.

## Q&A

Q: Regarding the problem that SPV wallet gets service for free... and it's not scalable because there needs to be full nodes that serve SPV users... could an incentive system be devised with lightning to pay for the service using lightning micropayments?

A: Maybe. Possible. Once we move to bip158, you basically download blocks, and blocks are free, and they are on CDNnetworks. Someone who might pay for blocks-- probably no longer possible, I think payments will force people over to bip158. I don't think payments woul make sense over a longer period of time.

Q: What about bip158? I like this proposal. It's better than bloom filters. Maybe I would have used this in electrum. I think you did not show the full story about bip158. When you show the amount of data used by... so this figure, you should maybe explain, .... false positives, rate of false positives your ability to... full blocks, are nothing... Full blocks you have to download for nothing, will increase iththe number of addresses in your wallet. So maybe you, do you have some figures about that?

A: No, I havent' looked too closely into bip158. I know you can get blocks you don't need, in order to increase your privacy. WIth the consumption model, I took a look at some major stats, and it's roughly 2% the size of a.... so yes, it depends on which privacy model you wanted to use.

Q: So these numbes are not from you?

A: Correct.

Q: For out of the box plug-and-play noe selection, what are the chal lenges of that and how do you keep it up to date without a trusted third party?  And what about people who are not able to do that, or don't understand waht any of this is? How do you maintain the node softwaere? How could users do this without trusting a third-party service provider that operates the block.

A: As soon as you don't want to dig into the details, you need to trust. Maybe you can setup a model where that trust is...  distributed among different vendors. Or you only want to trust a single vendor, and then that then is your trust model. Trust needs to be somewhere, when you run a full node on your r laptop you trust your laptop. When you run a full node on a raspberry pi, you're trusting the chip inside. How can you minimize the trust and make sure it's not spread all over?

Q: What is the biggest challenge in SPV you are facing?

A: The biggest challenge is hardware. You need to produce something and ship something in time. The community has not a great done of this in the past. I think that's the biggest challenge.

Q: I am interested in the lower left side of that triangle, namely security of private keys. What about generation and encryption of private keys? Should that be done, according to you? Should this be done on the protocol itself? When we use devices, phones, tablets, desktops, we run software on them, and by definition, my first primary thought is that the device has been tampered with to start with-- it's the cypehrpunk part. The username and password I'm filling in, is probably getting sent to a server or something, because I didn't create the device.How does one prevent that? What about trusted execution environments, have you used it, do you think it could be trusted? I mean the secure enclave in the device itself.

A: One of the biggest challenge in the bitcoin space is key storage. Where do I store  my keys? There's so little information. It's bytes of information that can hold a coupleof million of dollars. I think it's one of the biggest challenges- how to do key storage right. In hardware wallets, I think we're at a stage where it's acceptable, but it includes specialized hardware. It's just not ideal for grandmothers and these kinds of users. Maybe--- you also asked about software, I think the challenge is over there. Once you use a new device type, key storage is over. You can't do key storage there.

Q: Correct. Thank you.

Q: I don't want to bash bip158... but I'm enough of a geek to want a full node, but I'm enough of a normal guy that I don't want my phone to be cluttered with stuff. At the end of the day, I don't have battery. I think the industry is going to that direction because people are holding email on the cloud, they are putting everything on the cloud. What is your opinion with the current situation that that would be imroved, where for example, in red, you can choose  to-- whatever node is available, or you can manually enter your full node at home. That way, I would go towards a box that you were talking about.

A: Ithink connecting to a known node that you run, I think that makes sense. Most people just use a tcp raw socket. Some people say do a ssh tunnel on iOS, but the problem is that it doesn't work. Is Tor reliable in the long-term? Do we have reliable alternatives to Tor?

Q: You were talking about a hardware device of the future. It has to have enough storage space for a full node... and maybe 5g connection to quickly download the whole blockchain.. and you can trust it. How did you imagine that working? So it connects to a tunnel to your node at home or something? Do you think it's... will it be possible to have a small device with enough connection and space?

A: I'm fairly pragmatic with that project. Iplanned a lot in the past, pointing out, the goal points, and then I, as ... as Adam showed, the lines get squiggly. It's one of the experimetns I want to figure out how to work. But if you have these elements in your back head like a trust thing or a privacy thing, then you will succeed at some point. How it should work, it should have a separate channel from your device. The box should also do hardware key storage, and then you can do coinjoin or lightning transactions that only increase your balance, it's a signing solution only for those types of transactions. You can do multisig between your phone, your devices, and the box, ...

Q: What about security, combining retinal scanner and fingerprinting scanner and multisig and from different devices?

A: I like passphrases more than fingerprint scans and iris scanners. If you combine a full node with a trezor and some elements, it becomes secure and it becomes-- that's the biggest goal again, usability matters.

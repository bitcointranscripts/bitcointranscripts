---
title: Assets on Bitcoin
transcript_by: Bryan Bishop
speakers:
  - Giacomo Zucco
date: 2018-07-04
media: https://www.youtube.com/watch?v=xHWxtmgQP94
---
<https://twitter.com/kanzure/status/1014483345026289664>

Good morning everybody. In the mean time, while my presentation loads, I am Giacomo Zucco. I am the founder of BHB network and a consulting company. We do bitcoin consulting for institutional customers especially in Switzerland. We also like development on top of bitcoin and things like that.

My talk today is about assets on bitcoin. The subtitlte is "Yes, ok, financial sovereignity and cryptoanarchy are cool, but what about those cryptokitties?".

The topic of this presentation is how to issue non-bitcoin assets (assets not like bitcoin) on top of the bitcoin protocol. When I say on-top, I will try to clarify a number of the options. This is a review of past efforts and new proposals.

We're trying to converge on some best practices and standards. We want non-bitcoin bitcoin-based assets.

Your thoughts right now are in these order: if you have a centralized issuer or redeemer anyway, why even bother with deentralization of transfer? We've been hearing about this since 2011. Even if you need some degree of deentralization, why build it on bitcoin and ot something mor specializeed? Wouldn't that mess up with bitcoin's resources? This isn't a new idea at all. Why not just use a database? This might interfere with block space, bandwidth, storage, things that might not be directly related to the bitcoin project. What if you mess up the incentives so that you're promoting a scamcoin which is in competition with the bitcoin asset itself? Assuming your assets are not a competitor to bitcoin, what happens if your token is more valuable than BTC and miners might start doing strange things based on those assets.

There was counterparty, colored coin, mastercoin, omnicoin, and people are now doing cryptokitties on ethereum. So why try something new and discuss it again?

I would like to address some but not all of these objections and concerns. I'd like to convince you it's a good idea to put time, effort, skill and mony into a standard for non-bitcoin assets on top of bitcoin.

# Vape pen argument

Smoking is bad. It's bad for your health. But if you do, then you should probably use the way that is least damaging, so you should smoke in the way that damages your health the least. I happen to smoke cigars so I don't buy this argument.

# Djenga argument

When you build on top, it becomes hard for everyone to emove the pieces on the bottom. As you build on top, the more difficult it is to stop the base layer. It's a blockchain, right? The blocks are somehow reinforcing the stability and immutability of the layer on the base.

I'd like to associate dot com bubbles with... but an interesting thing is that while the internet had its profit wars against competitors and so on, the history was that there was first a protocol war. The internet won, and then we had the dot com bubble on top of the internt.

Do you think the internet itself would be better off if the dot coms bubble was implemented on top of something else instead of TCP/IP? Are you sure it's better for people to scam people on top of ethereum rather than on top of bitcoin? Sure, you are dissociating yourself from scams, but either way, people are building scams on the internet and on ethereum and they aern't building a lot of scams on bitcoin.

You should build stuff on bitcoin even if you're not convinced-- maybe don't help them, but don't necessarily stop them.

# Permissionless stress-test argument

Some of the things you can build on top of bitcoin can reinforce the immutability of the base layer, but they can crash the base layer like they are too heavy, they block the blockchain, reduce anonymity... The interesting thing like assets, and the proposal I'm trying to launch today, are permissionless. Not all of the changes require a change in the consensus layer. If ppeople can leverage bitcoin storage for free riding on top of this to do assets, then people will do that. Yes you can evolve bitcoin to make it difficult, but not forever. There will be a time at which bitcoin will be immutable at the base layer. It'sinteresting to analyze what thngs you can do in this regard.

# Architectural experiment argument

There are some experiments that involve radically different software architectures like proofmarshals from petertodd or mimblewimble. You can't experiment that with bitcoin right now. You need to experiment in real life with economic incentives. Creating an altcoin is a bad thing bcause you're creating a bitcoin competitor. It would be better to use a sidechain. Short of that, instead of experimenting with assets-- you can e xperiment with asets, your own funds, so that you can test this on the strictly not-bitcoin assets.

You can just peg the results. We're going to do exactly like that (spoiler). The proposal that I will be showing you to doay is the client-side validation scheme. We're doing it on top of the issued assets feature.

# Bruce Fenton argument

We all "love" Bruce Fenton. He started tweeting endlessly and he was talking about gun rights, pollution, but then on March 23 he started to talk about tokenized securities, and then again, and then again, and basically every day, and he issued a 100 BTC bounty -- "a database can issue securities digitally"... then he started to publish memes about tokenized securities, then videos, and ravencoin, other videos.... literally every.... our videos, other memes.... they invited him to securitytoken conference.... You cannot talk with Bruce about anything else. We need to help heal him of his obsession. ((applause))

# Idealized use cases

Independent: The asset should try to be independent from the issuer. Everything that happens to the asset after the issuance moment, including the perception of the value by the market, should be independent from the issuer. Asset independence is mostly science fiction. These are difficult to do and not realistic. You can think of something like that. It could make sense. In five years, maybe there will be tech that allows me to make a betting game on top of bitcoin completly decentralized and trustless... and it takes some fee, and then hte creator says, if you pay enough bitcoin, it will use that bitcoin to first to buy his lambo, but then to promote the betting contract.. then he gives back a percentage of the fees to everyone that gave the bitcoin. Some kind of illegal security.... para-legal security, at least. Royalties, equities. So, crypto-equities, grey market stock market. It's not realistic, but I don't think we should rule this out in the long-run. You could have kickstarter all-or-nothing mutual assurance contrats.

Transparency: this is where you still have to trust the issuer or something which is centralized. You could issue regulated stocks on the stock market but maybe you're afraid that we will manipulate the total supply. Or the ownership states will be modified. Or maybe you are committing technology to teh distribution model right now. Transparency can be used in two ways- one way is that bause maybe regulators... if you;re a stock market, why hould you use a blockchain? The main cost is not technical, it's legal. Maybe in 10 years if you prove you cannot inflate the supply, then you will have some kind of regulatory extension of some kind. I don't know.

Blindness:  Assume you are issuing a regulated asset on top of the protocol and your issuing activity follows AML/KYC and SEC guidelines and you're not selling to unqqualified or anonymous people. But because of how the protocol is built, people can, without you knowing it, you can trade on a secondary market which you might not even know about. I am only sering KYC customers, although those KYC customers can sell stuff on a grey market or secondary market. Someone else can go back and register and redeem the dollar.  This provides plausible deniability for the issuer instead of having to admit they are actively enabling a black market.

Standardness: People right now are chatting in this room during this room, and saying this presentation is a scam on telegaram. You're using the wifi of this coference center... it doesn't make sense, technologically, to use telegram. You should just use proximity communication. This network is so open and widespread for communication, that even for closed communication, you share it, because you're externalizing it. You need to build a 1992 closed community porrtal... you don't se TCP/IP for that... you use a mainframe.  There will be reasons to use bitcoin.

Independence:  smart rights or royalties, or digital collectibles. The life of the collectibles should be independent from the lifetime of the issuer. For asset transparency you can do "provably honest rights". For asset standardization-- just whatever. Many of our clients at my consulting company, they ask whether they should use ERC20. I tell them it's a scam and ethereum will crash. They ask what should they use-- I tell them make their own database. So they have to code something.. but why can't they just install an ethereum node. I can't sync it, but I can start it. And then I can leverage other people's stuff. If I am starbucks and I create the starbucks points on my system then I have to make sure that people can use the starbucks app. But if I use ERC20 then every ethereum wallet will be compatible. There's a point for interoperability itself. For asset blindness, you can use an example of "regulated rights". It's a standard-- it's interoperability or a protocol approach. I use the blockchain not for the black market, but because I want to be transprent.

# Review of past attempts

Asset-specific altcoins:for every asset you want to issue, you copy bitcoin, you call it an altcoin, this was a standard in 2011-2012 for scamcoins when people started to issue any kind of asset representing things... there were gold-based altcoins where people would just copy bitcoin. These had some problems. You had to bootstrap everything from scratch for every single asset. To get hashrate and security and review and maintenance by coders, that was basically impossible. There's no current approach. The issuance policy was often incompatible with mining incentives. Say you're Apple and you are going to issue Apple stock... you can't have a fixed supply, you can't really incentivize miners. And then people proposed an asset-enabled sidechain where you make one clone of bitcoin and make it asset-enabled and then you have to bootstrap the hashing power and the coder mindshare just once. This is basically ethereum or the new fixation with Rootstock.... The project will remain centralized around Vitalik Buterin. You have high incentives for scammers. You're trying to bootstrap digital gold, and so many scammers will get involved. You have reduced privacy. In ethereum ERC20, the anonymity set for ethereum users is--- it's account based... ERC20 token users, it's trivial because the anonymity set of people using that specific token.. that's true for colored coins as well. Anonymity on colored coins is really bad, how many people are trading that exact asset? Chain analysis can destroy all the privacy there.

Asset-enabled sidechain: instead of a scamcoin or bitcoin fork, what about a chain that can allow for assets? This is the original sidechain concept where you reuse the bitcoin hashrate with merged-mining and you're reusing the bitcoin asset with SPV two-way pegging. This original approach I'm mentioning BitAsset Drivechain... or confidential assets over the Liquid sidechain. Unfortunately you need to modify bitcoin for some of these sidechain proposals, like a soft-fork deployment. Liquid is a federated model so it doesn't require a bitcoin soft-fork.  Also the privacy is superior because it's using confidential transactions and confidential assets. If everyone can use confidential assets on Liquid, then an on-chain protocol becomes redundant.

Instead of creating another chain, what about using OP\_RETURN metadata? This is omni, counterparty, mastercoin and other strategies. You have low privacy here. You're fighting with bitcoin over scarce resources. You're a counterparty, you want OP\_RETURN to be larger, you want to store stuff in scriptsigs, or whatever. There's no SPV.  You can't do lite nodes with counterparty because the last transaction--  miners are not enforcing the meta-protocol rules. They can put counterparty-invalid transactions into a block. These protocols are using scamcoins like counterparty ICO which was proof-of-burn which was slightly more honest but still you have a scamcoin. The fight over scarce resources also creates a problem for metadata.

Colored coins: .. you can use a pseduo-SPV model. In counterparty or omni, you have to check all the transactions from all the blocks to check for double spends. With colored coins, you only have to check-- other transactions-- like Colu, which was a pseduo-SPV model. There's no scamcoin, which is good, but there's still other problems.

WHat about assets in bitcoin consensus? Well, that's not going to happen.

$ Smart coloring

There was another idea proposed by petertodd when he was working on smart coloring. He proposed client-side validation, applied on issued assets. Basically, you do not use the blockchain to store the meaata and proof of transmission for the assets. You only use the blockchain for an anti-double spending structure. You pass proofs to clients of the existence or validity of the coins. This proof contains all the necessary proofs, which you give to the receiver when you send money.  You have to be a participant in the exchange to be able to trak the original path of the asset from the issuance to itself.

# Why now?

It would be good to do bitcoin-based assets these days. There's client-side validation available.. Also, there is new market pressure. People are using scammy blockchains to issue assets. I personally want to give to my clients a better alternative to do things. And also, segwit makes some new opportunities available, and lightning network was not around when the first colored coins proposals were made.

# The RGB protocol proposal

This is a client-side validation design with possible proofmarshal integration in the future. We use native integration with lightning network.  We use pay-to-contract commitments. This would be compatible wth lightning network.

We are not using OP\_RETURN. We are putting a commitent to a proof by malleating an address. We're using pay-toc-ontract scheme.

<https://github.com/rgb-org/spec>

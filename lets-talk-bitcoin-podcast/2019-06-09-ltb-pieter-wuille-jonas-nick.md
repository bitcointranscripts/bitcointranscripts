---
title: The Tools and The Work
transcript_by: Michael Folkson
tags:
  - taproot
  - schnorr-signatures
speakers:
  - Pieter Wuille
  - Jonas Nick
date: 2019-06-09
---
<https://twitter.com/kanzure/status/1155851797568917504>

Part 1: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-400-the-tools-and-the-work>

Part 2: <https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-401-the-tools-and-the-work-part-2>

Draft of BIP-Schnorr: <https://github.com/sipa/bips/blob/bip-schnorr/bip-schnorr.mediawiki>

Draft of BIP-Taproot: <https://github.com/sipa/bips/blob/bip-schnorr/bip-taproot.mediawiki>

Draft of BIP-Tapscript: <https://github.com/sipa/bips/blob/bip-schnorr/bip-tapscript.mediawiki>

## Part 1

Adam: On this episode we'll be digging deeply into some of the most important changes coming soon to the Bitcoin protocol in the form of BIPs or Bitcoin Improvement Proposals focused on Taproot, Tapscript and Schnorr signatures. If you are a regular listener this won't be the first time you've heard about most of these broad ideas but today we hope to dig deeper. As such we're very pleased to be joined for today's session by Bitcoin developers Pieter, better known as sipa and Jonas Nick. Gentlemen, thank you very much for taking the time and joining us today.

Stephanie: I want to echo that. Thank you so much for being on the show with us. It is really great to talk about these proposed changes to Bitcoin and talk to someone who really knows what they're talking about because they're actually involved with making it happen. We really appreciate your time. I just want to ask you both first, Pieter and Jonas, how did you first hear about Bitcoin and then how did you become a Bitcoin developer and why are you interested in these specific proposals? Pieter why don't you go first?

Pieter: I think I heard about Bitcoin first at the end of 2010 on a IRC channel about the Haskell programming language where people were talking about it and then I started looking into it. I noticed I had a graphics card at the time in my computer that was capable of mining Bitcoins. That was fun, initially I just looked at that. The price was very low at the time, it was like twenty cents or so.

Stephanie: And what was exciting to you about Bitcoin at that time?

Pieter: It was just this idea that you could have a currency defined by the internet, by nothing more than software. It was always a technology that attracted me and had potential for changing how we think about money.

Stephanie: And when did you first start developing for Bitcoin?

Pieter: I think it was early 2011 that I started looking at the code. I think there have been a time when SlushPool was starting too and they were looking for some changes to the code so I thought why don't I have a look? Then a bit later on the bitcointalk forum which at the time was just on bitcoin.org I think, Hal Finney posted a challenge which was “Here is a Bitcoin address, it has 5 Bitcoins on it which was a couple of dollars at the time and a private key. Anyone who can take those coins with that private key can have them.”

Stephanie: Did you win?

Pieter: No I did not. At the time the Bitcoin software that existed didn't have any possibility for importing or exporting private keys so that was a new thing. I started looking how can I hack this into the Bitcoin software? It took me much longer than other people who were trying to do the same thing in Java or Python but in the end I had this patch for importing private keys into Bitcoin. I tried to get that merged because that seemed like interesting functionality. I started talking to Gavin Andresen at the time who had just taken over as maintainer of the project. I think it took half a year or so before that patch was merged but before that was done I had already been asked to contribute and start looking over other peoples' patches.

Stephanie: That's fascinating, I really like that story. Have you been actively developing for this entire time and how did you get interested in Taproot and Tapscript and Schnorr signatures.

Pieter: I have. Initially I was just doing that in my free time and then as soon as I joined Blockstream in 2014 I was able to do it full time. Since that time I've worked on many things. Taproot and the related things are a continuation of the effort around Segregated Witness which started a couple of years ago.

Stephanie: You're interested in scalability and security?

Pieter: Yes of course. The primary advantage here is improving things we started with Segregated Witness. In particular here we improve the potential for fungibility by making all transactions or at least a large subset of transactions look more alike making it less clear to the public what is actually going on. At the same time there are scalability improvements. They are minor for typical transactions, they are most impactful for more complex things like multisig or smart contracts.

Stephanie: We're going to get into the technical details a little later. Thank you so much for that introduction and your background. So Jonas how did you first hear about Bitcoin and what got you interested in becoming a Bitcoin developer?

Jonas: I first heard about Bitcoin in early 2011. There was this bubble I think to 30 USD and I was immediately very interested in this idea of being able to use a money where no one can stop me and also being relatively private while doing that. Actually I listened to your podcast very regularly in 2013 and 2014. It was also the first time I heard about sidechains and Blockstream. I just looked it up, it was [Episode 99](https://letstalkbitcoin.com/e99-sidechain-innovation) with Adam Back and Austin Hill. That was a really good influence at the time.

Stephanie: That's such a cool story.

Adam: I remember that interview. Very interesting ideas in the early days for sure.

Stephanie: So continue Jonas. How did you get started with developing?

Jonas: I started contributing during university. Also in the same year I studied computer science. In 2015 after that I joined Blockstream.

Stephanie: At this point I want to jump into some of the technical details of these topics and we're going to be asking lots of questions here. First I think we should define exactly what we mean when we say Taproot, Tapscript or Schnorr signatures. We've decided we're going to start with Schnorr signatures and we're just going to define what exactly that means. I'd like to ask Pieter, in your words could you describe what is a Schnorr signature and why is it important?

Pieter: Currently Bitcoin uses ECDSA signatures to let keys sign off on transactions. Whenever you have an address, at least when it is a single key one, it is really a hash of a ECDSA public key and when you receive coins to it and want to spend those you need to sign off using the corresponding private ECDSA key. The ECDSA algorithm has an interesting history, it is the DSA signature scheme which is fairly common, ported to the elliptic curve cryptography world. The DSA signature scheme was originally designed pretty much as a way to avoid the patent on Schnorr signatures. Schnorr signatures were invented by Claus-Peter Schnorr I think who came up with this. Over the years people found many interesting properties and things that could be done with these but unfortunately he patented them. As a result the world looked to standardize an alternative that wasn't patented which was DSA. Then ECDSA followed and Bitcoin in its early history apparently picked this up. So on itself the differences between ECDSA and elliptic curve Schnorr aren't that big.

Stephanie: So it is just a different way to sign transactions it sounds like you're saying?

Pieter: Correct. It is even more low level, it is the primitive that you use to produce that signature. However, there are a number of properties that these signature schemes have that we're interested in. One of them in particular is the fact that these signatures are linear. What this means in practice is you can take a group of people, take their public keys, combine those public keys together into a single public key and now those participants whose public keys you have taken to combine can jointly produce a signature for the combined public key. This is really a very compact way of doing what we're calling multisignatures in Bitcoin. In particular n-of-n ones. You have a group of three signers and you want all three of them to sign off on something. Instead of needing to put three public keys on the blockchain you only put one. And instead of having a signature for each you only have one.

Stephanie: It sounds like this is more efficient but also importantly it is more private because you're exposing less information.

Pieter: Exactly. Generally when you're exposing less information you also reveal less. But in particular what is gained here is you leak less about your policy to the world. Imagine a fancy new piece of wallet, hardware wallet software suite comes on the market, a fancy wallet and they're the only ones in the world that use 5-of-7 multisignatures. If you're going to use that software it will be patently obvious to the entire world which transactions are fancy wallet ones. So by reducing that information leak, by turning pretty much everything into a single signature. So far I've only talked about the n-of-n case but there are ways to get similar, not quite as big but similar improvements for k-of-n or different policies as well.

Stephanie: What's k-of-n?

Pieter: k-of-n is say 2 out of 3 where k is different from n.

Andreas: That's what we usually call m-of-n.

Stephanie: So we're just using another letter, that confused me.

Pieter: m and n sound too similar so I started using k and n.

Stephanie: That's clever, thank you. Ok continue.

Pieter: When we talk about k-of-n or thresholds you have a number of participants that you want to sign and you only need a subset to sign off. We talk about multisignature or n-of-n, you have a group of participants and they all need to sign off. Schnorr signatures give a way to make n-of-n very efficient because it just turns into a single key with a single signature. But similar improvements can be made using more advanced techniques for k-of-n as well.

Jonas: It should be noted I think that there are some recent papers that show you can do some of these things with ECDSA as well, in particular n-of-n. In practice they are quite hard to implement and require new assumptions. In particular if you want to have an implementation that is side-channel resistant that's quite hard to do with these ECDSA schemes.

Pieter: You're absolutely right Jonas. These things can be done with ECDSA as well but due to the linearity property of Schnorr signatures it is vastly easier, both more efficient and easier to get right, the protocol overhead is lower.

Andreas: A follow-up question on that. From my reading I understood that there is also a way to produce some formal proof about some of the security properties of Schnorr that is of particular value to a solution like Bitcoin.

Pieter: Yes. Schnorr signatures can be proven secure under the assumption that internally it uses a hash. If we model that hash as a random oracle and assume that the discrete logarithm problem over elliptic curve groups is hard, from that you can prove that Schnorr signatures are secure. The same is not true for ECDSA. People have tried and I don't think there is any reasonable assumption that it will actually be broken but it is nice to have a formal proof for these things.

Stephanie: What happened with the patent that was originally filed on this? You said at the beginning that this was a patented technology that couldn't be incorporated into Bitcoin.

Pieter: Actually it could be, the patent expired in 2008. What the patent accomplished was that people didn't use Schnorr signatures and standardized on other technologies instead. Bitcoin's creator just picked what was available and ECDSA was standardized, fast and small enough so it ticked the boxes and was the obvious choice.

Stephanie: Has Schnorr himself changed his mind about patenting? Has he weighed in on what he thinks about this?

Pieter: As far as I know he always held that DSA actually infringed on his patent.

Jonathan: This has always been a question that I've had. I hear Bitcoin is decentralized and I always try to understand what that means and what that doesn't mean. You hear about who has control over Bitcoin and who is really in charge or responsible for it. We hear of all these protections that Bitcoin Core contributors have under free speech for contributing to the repo but not being the commercial actor engaging in the actual activities which is why there are very strong protections for open source contributions. Why would something like a patent stop a superior technology from being implemented in a repo for a decentralized, open source project? I don't understand where that limiting factor is. Was it just because the libraries weren't standardized like you said?

Pieter: To be clear the reason why Bitcoin didn't pick Schnorr from the start is simply because it wasn't standardized. It wasn't standardized because earlier it was patented. If you're talking about now, would it be possible to incorporate patented technology into Bitcoin or into its implementations? I'm not a lawyer but I think at least a concern would be, even if there is no legal problem with doing so you don't want users to have to worry about can I use this software? The question isn't just is this the right technology, it is also do you expect the ecosystem to adopt it? When there are roadblocks like patents in the way that question becomes a lot harder.

Adam: It becomes more controversial if you were to include something like that because then you would have that as a question whereas the way that the protocol is right now there is really no question about whether it infringes on patents.

Andreas: The standardization question is interesting, I would like to explore that a bit further. From what I understand, the Bitcoin implementation of Schnorr, the proposed implementation of Schnorr is leading the way in standardizing not just how Schnorr signatures are encoded, how they're represented but also there's been a lot of development around multisig with Schnorr in a protocol called Musig that you've also been involved in. Is Bitcoin leading the way in standardization with Schnorr now?

Pieter: There's a number of other signature schemes that are essentially Schnorr based but don't go by that name. One of them is ed25519.

Andreas: Which is the Apple one?

Pieter: I have no idea but that wouldn't surprise me. That is essentially also a specialization of a Schnorr based scheme into a practical standard. We can't use ed25519 for several reasons. One of them is we like to maintain compatibility with the existing public key system we have so that things like BIP32 and everything built on it don't get invalidated. That wouldn't be a terrible thing to do but it is simple enough to maintain compatibility so we define a Schnorr signature over the secp256k1 curve which is the same curve that Bitcoin's ECDSA scheme is currently defined over.

Andreas: So the curve doesn't change which also means the private key space doesn't change, it is the same prime order?

Pieter: Public keys remain the same.

Andreas: Therefore we can reuse all of the existing encodings and in fact derive private, public and signatures from the same set of standard technologies we have. For example, mnemonic seeds based on BIP39 and hierarchical deterministic wallets on BIP32 etc? That's a huge advantage.

Stephanie: And does that also mean it would be a soft fork to incorporate that?

Pieter: Yes it would be.

Andreas: So because of the script versioning introduction in v0 SegWit these proposals are now being… as SegWit v1, the second edition of SegWit essentially.

Pieter: That's right. Due to the script versioning mechanism we can essentially make proposals that completely change the script system or anything within that space and all of these things remain simple soft forks as opposed to trying to hack it into existing OP codes that we had to do before.

Andreas: So two years ago when we started talking about SegWit we predicted that that would be one of the big benefits because it gives enormous flexibility for upgrades through soft forks. The other two proposals that were brought to the table, the Tapscript and Taproot which also incorporates MAST, the Merkelized Abstract Syntax Trees, are also being proposed as a soft fork. One of the things that struck me as very interesting is that they are being proposed as a bundle, meaning altogether. That has a lot to do with the combination of features that bring the best set of privacy features so that it is not obvious that you are using new privacy techniques. Can you talk a bit about what Taproot is and how it relates to Schnorr and MAST and why these are being brought in as a bundle of proposals?

Pieter: Sure. If you start from the perspective of the consensus rules you need to start with Taproot. BIP-Taproot proposes semantics for SegWit v1. The way to look at Taproot is it is a generalization that merges pay-to-publickey or pay-to-publickey single key policies and pay-to-scripthash. In a way every output becomes both of them. Everything becomes a combination of a key or a script. So when you pay someone, when you get an address you won't be able to see anymore is this going to a key or this going to a script. It could be either and the sender doesn't care, the network doesn't care, nobody sees it. When you want to spend such an output you have two options. Either you prove you know the private key to it and then you can just spend it or you prove that it was actually an address that was derived from a script. You give that script, you prove that it is and then set aside the script. The amazing property that is accomplished is that you don't reveal which of these options existed. You can still have outputs that are only to a key or only to a script and you can't distinguish them. When spending you don't reveal whether the other option existed in the first place or if both existed you don't either. The effect of this is if you have an output that is to a key or a complex script but you are now spending it using the key, that looks completely identical to a single key standard payment that was being spent.

Andreas: Let's give a practical example here which springs to my mind. One of the examples where you might be able to use this in the future is have a complex smart contract that involves collaboration between parties such a Lightning channel. Lightning channels are 2-of-2 multisig. When they are closed cooperatively between the two parties which is the vast majority of the time, that's how it should be, instead of revealing to the world this is a channel by dumping a big, fairly verbose script onto the chain when spending it to close the channel, the two parties who are already in communication on the Lightning peer-to-peer network could simply compose a joint signature using Schnorr and spend the public key side of that without revealing that it was a channel at all. It looks like someone just spent a payment, no one even knows that it was a Lightning channel in the first place. That's where the n-of-n type cooperative multisig where all parties sign. Is that correct?

Pieter: That is absolutely right. That is also the reason why Schnorr is integrated into this. We make an assumption here that most contracts can have this cooperative branch that just consists of a number or even all participants in the contract agreeing. Due to the linearity property of Schnorr signatures those things can be turned into a single key. As soon as it is a single key Taproot can make it super efficient by making it just look like a single signature on the chain.

Andreas: And this is both a privacy advantage and a scaling one?

Pieter: It is both a privacy and a scaling advantage. All you see on the chain is a single public key when paying to it and a single signature when spending it, that's all. That goes back to your question about bundling. There are a number of technologies included here. We've already mentioned two, the Taproot construction and Schnorr. Schnorr by itself only gives us a bit better multisignatures and Taproot by itself doesn't do much unless you have this cooperative branch in there that you can assume is going to be used most of the time. But together they are much more powerful. A few other things are added to it. Merkle trees are an obvious win. When we are making these changes already adding the Merkle tree in there is a very simple addition. It means that if you now have multiple, it is not a key or a script, it is a key or one of many scripts. It remains efficient even when you have thousands, maybe millions of possible small scripts. This gives you a similar advantage where you are again revealing less to the world about what you are doing. You are still revealing the actual script you are using but not all the other scripts that were possibly involved in this contract.

Adam: So just to summarize here, in the old way we effectively have specific methods for different types of users and uses. Because of that it is possible or even easy to tell the difference between a normal transaction and something like a multisig or a simple smart contract. In the new way we have a single unified method which because everything looks the same dramatically improves privacy as well as having the other benefits we've been talking about here.

Pieter: That sounds right.

## Part 2

Pieter: There are a few more things that Taproot tries to achieve. One of them is better efficiency for verification because there is another feature of Schnorr signatures which is batch verifiability. Batch verifiability is a way to if you are given a thousand signatures each with their own public key and message you want to verify, you can tell whether all of them are valid faster than testing them all individually. The downside is if batch validation fails you have no idea which of the inputs were invalid. Generally in Bitcoin blocks we don't care about that. We only care about is the whole block valid or not? This property of batch verifiability which is factor 2, 3, 4 sometimes depending on how many things you aggregate together, we wanted to maintain that property even when it was integrated into the script system. In order to do so there are a few OP codes in the scripting language that are incompatible with this. One of them is CHECKMULTISIG. Interestingly we have better ways of doing multisig now but even if those were somehow not available to people the CHECKMULTISIG OP code can't remain in its existing form. You've given a number of public keys and a number of signatures and the verifier has to try to match up which public key corresponds to which signature and this trial operation, we can't batch that. So we were forced to make a few small changes to the scripting language anyway to guarantee compatibility with batch verifiability. That is what became Tapscript. Tapscript is the modifications to the scripting language for scripts under Taproot. Really it is a separate document for two reasons I think. One, BIP-Taproot was getting pretty long already. Also, and that is another feature I think that BIP-Taproot focuses on is flexibility. In the Merkle tree of BIP-Taproot every leaf is a script combined with what we're calling a leaf version. This is again a sort of versioning scheme very similar to SegWit script versioning except these aren't revealed at payment time. They're only revealed at spending time. Even more interestingly different leaves can have different versions and you only reveal the one you're actually using. You get a potential privacy advantage from say a new fancy script improvement gets made but it is only necessary on one branch of your contract. Then you're not even going to reveal this unless you actually use it. Tapscript is the proposed version 0 of the leaf version under Taproot. As there could in the future be different new ones for this it is also a separate document. If it is v0 read BIP-Tapscript, if it is something else for now it is unencumbered but later proposals may redefine this. Does that make sense?

Andreas: Absolutely yes, to me it does. So in terms of batch verifiability Pieter, from what I understand there are three or more different levels of batch verifiability. There is verifying multiple signatures in a single script, there is verifying multiple signatures across inputs of the same single transaction and then there is verifying signatures across multiple inputs across multiple transactions, perhaps even a whole block. Which level of batch verifiability are we talking about?

Pieter: All of them. These increasing levels you are talking about, they are increasingly complicated to integrate in software but there is nothing that prevents batch verifying the entire chain in a single operation.

Adam: Batch verifying the entire chain would have the result of effectively making sure that the entire chain is valid and if there are any transactions or actions within it that are invalid then the entire thing would show up as invalid. So you could do that theoretically and it should still work even at that scale.

Pieter: That's right. It is probably not something you want to do when individual blocks are coming in but for verifying history this may be the case. Andreas, I need to point out we're talking about batch verifiability here. There's another property namely aggregation and there things look very different. When we're talking about batch verifiability all the transactions, all the signatures, all the public keys individually still remain in the chain. It is just a faster way of verifying them all at once.

Andreas: This is basically a CPU and memory optimization in the client that is verifying the chain?

Pieter: Yes, absolutely. It is just that and the reference implementation doesn't even do this at this point. The whole proposal is just designed to make this optimization possible. In contrast to that there is signature aggregation which is technology where you effectively reduce the number of signatures that are in a transaction or in a block even and so on. So far BIP-Taproot and Tapscript as is only support forms of aggregation within a single input, so multiple keys within a single input. One is through Musig, a construction where you get rid of the public keys, you combine them all and now you have a single signature for it. There are more advanced ways of enabling wider aggregation but those are not included.

Andreas: But they are not prevented either so there is a possibility that in the future you could have perhaps a transaction with three or four inputs where we could have aggregation of the signatures so there is one signature for the entire transaction. And then perhaps even later on if all the signatures in a block were like that you could even aggregate a whole block into one signature.

Pieter: Yes, not prevented but it will require a successor to Taproot. The aggregation cross-input would probably not be in BIP-Taproot.

Andreas: In terms of the adoption of this we obviously don't have a timeline for these BIPs to be soft forked into mainnet. But let's assume that they were soft forked at some point in the future. Obviously this would be a hybrid chain where ECDSA, which still exists of course, one of the principles in Bitcoin is that you don't invalidate old outstanding UTXO. Anyone can bring anything back from the very first block and it should still be spendable. At that point you have ECDSA and Schnorr coexisting in blocks perhaps even in single transactions, some inputs could be ECDSA, some could be Schnorr, others could be mixed. How does that affect batch verifiability let's say on a transaction basis? Do you just batch verify whichever Schnorr signatures you have and then separately verify the ECDSA ones?

Pieter: Yes that's exactly it. You get the gains but they only apply to the Schnorr signatures.

Andreas: And so the more adoption you have of Schnorr signatures the more wallets for example migrated and the more new UTXOs that have Schnorr, the more that optimization starts benefitting the network?

Stephanie: Just like SegWit.

Pieter: The difference here of course is that there are no actual user benefit to this batch verifiability so there's no discount for enabling it other than the fact that Schnorr signatures are somewhat smaller. I expect there are sufficient incentives when Schnorr signatures are eventually, this may take a long time of course, widely adopted to give a significant boost.

Jonas: With Schnorr signatures and ECDSA signatures if you don't take batch verification into account they are similarly fast. With batch verification Schnorr signatures become faster. If I look at the numbers here, if you have ten signatures you can validate them 1.5 times as fast for example. Or if you have the number of signatures on the order of a block like let's say a couple of thousand then you get 2.5 times the speedup over validating them all one by one. Doing as the implementation defines, whenever you see a transaction you can try to batch verify it but when you batch verify a transaction or signatures if it doesn't work out you don't know at all which specific signature verification failed. I think this is just an engineering challenge, when to use batch verification and when not to do that.

Andreas: I would assume that one of the big benefits especially over the longer term is in keeping the initial block download time or IBD as it's called which is when you bootstrap a new node and you have to start from the genesis block and verify all the way forward which is obviously very desirable to be able to always do that. The more transactions, the more blocks, the longer it takes. Bitcoin Core has managed over the past couple of years to essentially stop the clock by optimizing about as fast as the block size grows so that is not significantly longer. In some cases even faster than it was in the past. With batch verification of Schnorr when you're verifying blocks that have already been mined where the transactions are presumably already valid unless you are looking at a fraudulent blockchain then this would be a significant boost for long term IBD scalability?

Pieter: It is another factor that gets added to it. To the extent of course that IBD is dominated by signature checks. On most systems I think it is actually dominated by access to the UTXO set.

Adam: IBD? Please define it.

Stephanie: Irritable Bowel Disease.

Andreas: Initial Block Download.

Stephanie: Sorry, medical background.

Andreas: If your node has insufficient RAM they become the same thing.

Adam: So basically what you're saying is that the advantage that we were talking about where you can download the entire blockchain and you'd be able to potentially verify, that only comes into effect when we're talking about Schnorr signatures?

Pieter: Yes

Adam: During that transition period where we've got a lot of Schnorr signatures but we also have a lot of non-Schnorr signatures in the same block can you batch verify that block or would you just be batch verifying all of the Schnorr signature transactions within that block?

Pieter: Yeah exactly. You'd batch verify just the Schnorr signatures.

Andreas: In the past when we've talked about these upcoming BIPs one of the features that has been discussed quite a bit is SIGHASH_NOINPUT as it has been known. It also goes by the name of SIGHASH_ANYPREVOUT. To remind our listeners there are some proposals in the Lightning Network to change the way the protocol works in a formulation called eltoo which greatly simplifies the use of the Lightning channels by making it unnecessary to have penalty closure in the case of trying to cheat by transmitting a prior state that has been invalidated. That requires a change in the Bitcoin script and specifically in the way signatures are applied to transactions which is called the SIGHASH system, in a way that allows you to rebound to a different input. That's been called SIGHASH_NOINPUT, it has some other names because there are various formulations being proposed. That has been included as part of Tapscript?

Pieter: No it hasn't.

Andreas: It was being proposed or discussed for potential inclusion?

Pieter: BIP-Tapscript includes a number of improvements to the sighashing scheme but it does not include SIGHASH_NOINPUT. The reason for that is exactly because there has been a lot of discussion about various ways of doing it, various ways of making it safe. It touches some essential way of how transactions sign previous data, where things are coming from. Breaking this is scary. So instead we realized that instead of including it directly we could include a number of flexibility mechanisms in Taproot and Tapscript that would allow us to do things like this in the future at no loss. In particular, the types of flexibility that exist are I believe versioning as I mentioned before, another one is OP_SUCCESS. Inside Tapscript a large portion of the previously unusable OP codes go from basically being a return false to a return true. Anytime any of these OP codes exist inside your script they would mean that you can spend it unconditionally, just like future SegWit versions or future leaf versions. The practical advantage of this is you can redefine those OP codes to be anything, they don't need to be backward compatible with an OP_NOP which is what we have now. A third mechanism is when you have a public key that starts with a byte you don't know it is also treated as an automatically valid one. This means that we can introduce new types of signature schemes but also new sighash schemes without needing to add new CHECKSIG opcodes for each and every one that gets added. The idea is that things like NOINPUT could then be included at no cost as a new public key version.

Andreas: So these are essentially within Tapscript, mechanisms for future upgradability. There are a whole set of them. There's three different ways that you can do future upgrades to script. Change the version of Tapscript and the leaf, modify the semantics of something that is currently an OP_SUCCESS that old clients that haven't been upgraded will see as a valid script and this public key sighash prefix that could be redefined again that old clients see as a valid script. This means that the things requested by an eltoo implementation in Lightning do not need to be roadblocks in the implementation of these three BIPs: Taproot, Tapscript and Schnorr. The conversation can continue on how exactly to implement those.

Pieter: At some point in the discussion around this we were noticing that the discussion around SIGHASH_NOINPUT was very much slowing down our progress on other things. So we decided to instead have this flexibility and publish the BIPs without but of course this doesn't mean that if one of the proposals for NOINPUT gets enough traction and an implementation, it could even be activated at the same time as the other ones. As you say there are no longer roadblocks in the conversation about Taproot itself.

Andreas: How very Solomonian, that's a great way to resolve a potential deadlock and move forward with features that now at this point have broad traction within the developer community. Having said that, the discussion around SIGHASH_NOINPUT is currently generating about a third of my inbox for today. Today was a particularly lively discussion about that. A lot of different ways of making them safe or whether they need to be made safe in the first place and chaperone signatures and various other mechanisms are being discussed. Assuming that that continues as a lively debate what is your feeling about how these BIPs might progress into implementation, the three BIPs ignoring SIGHASH_NOINPUT and any controversy around that?

Pieter: For now, I hope to get input and review from the developer community, get a feeling for how well received it is. So far it has been very positive but I really can't say much about steps after that. At some point there will be a reference implementation. We'll hope to get a feeling for whether it is acceptable enough to the community to include it in Bitcoin Core and potentially other full node implementations. Then a discussion about how to activate it can start and then we see how to go from there.

Andreas: I think it is very wise not to try to make any predictions about when and how and how it will be activated. One of the most surprising things for many of the developers was how controversy erupted around SegWit when it seemed like everybody was on the same page and it became very, very heavily politicized. That's not really relevant to this discussion. In terms of the reference implementation as a follow up, I thought that you had already published a reference implementation on a fork of Bitcoin Core and it was affecting about 500 lines of consensus code?

Pieter: Yes something like that. I want to point out this is more for demonstration purposes than anything else. I want to show how little is affected here. Before code can be included we'll need a much more reviewed, production ready version with much more tests and so on. Also I expect there will be minor and possibly major changes that we still want to make to the proposal in response to public discussion. Having a production ready version is something that happens after all those discussions.

Andreas: At this stage someone could download the fork, run a regtest blockchain on their own laptop and start playing with all these features today?

Pieter: That is right though I should also add that this reference implementation is purely the consensus rules and nothing else so there's absolutely no integration into the Bitcoin Core wallet for example which has no ability to produce such transactions.

Andreas: And not even in the RPC infrastructure or anything else? You'd basically have to write some code to call the library components?

Pieter: Yes. We're working on a number of other things to make it easier to integrate more complex scripts into Bitcoin Core's wallet and signing logic and possibly other software too called miniscript but how we'll end up integrating those is for later. The point is of course is that for inclusion in the protocol we don't need wallet support. It is a great way to show the advantages if it is there but it is not necessary as a first step. It greatly simplifies the review needed.

Andreas: With proposals and changes to protocol level features like this and consensus layer features like this these don't really become part of the user experience or go into production until wallets implement them. Bitcoin Core of course first but other wallets too. We're now at 18 months from the SegWit soft fork into mainnet and the introduction of bech32 addresses etc and still wallets are lagging. It is very hard as a wallet maintainer to keep up with changes and implement these things at a user interface level of course. How would you characterize the implementation of Taproot, Tapscript, Schnorr signatures and these features in terms of the difficulty for wallet developers to bring these features to users?

Pieter: That's a hard question because it very much depends on what you want to do with it. Given the flexibility and things that Taproot, Tapscript and Schnorr signatures permit it really depends. If all you're doing is changing your P2WPKH receive addresses to something Taproot based it is a fairly trivial change. I expect the signature hashing algorithm change is a bit…. of course you'll need something that can do Schnorr signatures instead of ECDSA signatures but there are several implementations for that already and how you compute your address will change a bit. On the other hand If you're talking about integration of something where you use the Merkle tree with various branches, some using one of the newer features in there, you want to use Musig to combine multiple public keys together, all those things lead to many more options. Of course there is complexity in implementation there but these features aren't necessary for everyone who wants to use it.

Andreas: I'm thinking more of the if I want to hide in the forest I want everybody else to be planting a tree too. It is not so much about the people doing the fancy wallet, it is more the people who are doing the plain P2PKH, P2WPKH, the payment to public key, switching to Schnorr so that that gives the more complex scripts a nice uniform place to hide their privacy enhancing features.

Pieter: Yes I think it is a significantly smaller change than SegWit was because there are no peer-to-peer protocol changes or changes to the structure of transactions or blocks but you do have the Schnorr versus ECDSA thing.

Andreas: As a follow up to that, with SegWit we saw a new address format, bech32, the native SegWit address that starts with bc1. Are we going to see another address format or is this going to be incorporated into bech32 addresses?

Pieter: It already is because BIP173 that defines the bech32 addresses for Bitcoin actually specifies an address format for every SegWit output not just v0 ones. So SegWit v1 outputs can already be encoded using bech32 addresses. There may be some compatibility issues, it is possible that sender software still only allows v0 witness bech32 outputs. Even if that is the case that would be a very simple change to permit v1 as well.

Andreas: So no new address format which I'm sure is a relief for everyone who is trying to learn what all of them are.

Pieter: Yes. In fact the fourth character in a BIP173 address is for v0 always a q, it is bc1q, for v1 it will be bc1p.

Andreas: Very good, I didn't realize that.

Adam: Guys, thank you very much for taking all this time with us. This was a very interesting conversation and I think that I came away with it understanding a lot more about these issues than I did before although I still perhaps have a little bit of a deficient understanding.

Stephanie: Me too Adam. It is going to seep in through us when we listen back to the podcast. All joking aside, I really appreciate it too. I feel I have a better understanding also.

Adam: So we've been talking about stuff that is very real and while it might not have an immediate timeline it seems like it is on the path towards integration and there is broad consensus at least within the developer community on these less controversial parts of it. Stepping back from this now version of the technology what I'd really like to hear from either or both of you is what technologies or even ideas that you're excited about or that you think will be important for the Bitcoin protocol moving forward but which we might not have even heard of yet or which we might not think is important. Are there any technologies out there or ideas that you guys are really excited about in the next couple of years beyond this?

Jonas: This whole Taproot thing is a very new idea so it is really hard to say what will be out there as ideas in the next five years because this seems to change all the time. So now that this BIP is proposed, it is not even formally proposed in the BIP process sense. Right now it is only on the mailing list. The work with that is far from over because this needs to be polished and maybe some improvements need to get in, minor, major ones, Pieter mentioned it. My focus is building some of the libraries that are used in wallet implementations or Bitcoin Core. For example, you need an implementation for Schnorr signatures, we have that right now. It has received quite a bit of review but then we also want an implementation of Musig so we have a PR for that as well but that needs more review. Then we're also going to work on threshold signatures for example. Since these things are relatively new also for Bitcoin developers to work with and they require interactions between multiple participants of the protocol, we really want to make these libraries easy to use and safe first and foremost. I think this will still require a lot of work and this is something that I'm focusing on but I'm also really excited about seeing this in reality hopefully at some point in a couple of years or next year, we'll see.

Pieter: Yeah I think that is a very good point. There are a lot of options that are created by things like Taproot and Schnorr that I think we haven't even considered. Just very recently there was the [CHECKOUTPUTSHASHVERIFY](https://github.com/JeremyRubin/bips/blob/op-checkoutputshashverify/bip-coshv.mediawiki) that Jeremy Rubin proposed for example that is made a lot simpler by Taproot. I expect we will see more ideas of things that people haven't thought about that can be built on top either as minor consensus changes or just purely wallet side payment channel kind of things. Beyond that I'm really excited about cross input aggregation. This means the idea of turning potentially all signatures per transaction into a single one so you would have just only a single signature per transaction, at least when everyone is cooperating even in a large coinjoin or something. This has shown to really interact with many parts of the system so that was something we left out of BIP-Taproot but ironically that feature was what drove us to research Schnorr signatures and all the way it interacts in the first place so I hope we can get back to that in a future step. Also things like Graftroot and G'Root which are improvements over Taproot and generalizations of it. If you are talking about completely unrelated things to Bitcoin scripting, other technologies I'm excited about, for example we've been working for a while on a [better transaction relay protocol](https://arxiv.org/abs/1905.10518), Gleb Naumenko, Greg Maxwell and I. We wrote a minisketch library to do efficient set reconciliation with each other instead of announcing the same transactions over and over again that I'm really excited about.


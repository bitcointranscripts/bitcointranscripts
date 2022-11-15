---
title: Murch and Enterprise Wallets/UTXO Management - Episode 8
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ['Enterprise UTXO management', 'The impact of the 2017 hype cycle', 'The importance of UTXO set minimization', 'The fee market today', 'Batching TransactionsPayment Batching', 'ConsolidationsConsolidation of 4 Million UTXOs at Xapo', 'Change splitting', 'Replace By FeeRBF in the wildFee bumping', 'SegWit', 'How enterprises estimate fees', 'Omnibus wallets', 'Off-chain sending', 'Taproot', 'Bitcoin Optech Field Report: How segwit and batching could have saved half a billion dollars in fees']
---

Chaincode Labs podcast: Murch and Enterprise Wallets/UTXO Management - Episode 8

SPEAKER_02: to throw out a few numbers there, non-segwit inputs cost almost 300 bytes, and native segwit inputs cost slightly more than 100 bytes. There's almost a reduction by two-thirds in fees if you switch from non-segwit to native segwit.

SPEAKER_00: Hi everyone, welcome to the ChainCode podcast. My name is Kara Lee. And it's Jonas. And we're back. We're back. We're not all back. So, while Jonas and I are coming to you very socially distanced from the New York office,

SPEAKER_01: And I'll see you in the next one. We're back. John is the most socially distanced.

SPEAKER_00: So John is now in London.

SPEAKER_01: sunny old London.

SPEAKER_00: So while we are sad to not have him with us, we are very happy to be back in the studio.

SPEAKER_01: We have some new people that work here though, that's exciting.

SPEAKER_00: That is very exciting.

SPEAKER_01: You want to talk to Merch for the first one back?

SPEAKER_00: I think it would be a great idea for you to talk to some column, Mark. Mark. And what do you think you guys are going to talk about?

SPEAKER_01: Mark. He worked at Bicco before he came to ChainCode, so he knows a ton about UTXO management, enterprise wallets, and stuff like that. So let's start there. So welcome to the ChainCode podcast, Merch. Hey, thanks. Welcome to the ChainCode podcast, but also welcome to ChainCode.

SPEAKER_02: Oh yeah, thank you.

SPEAKER_01: Yeah, what do you think about the office and moving to New York and all that?

SPEAKER_02: Uh, well, that sounds like you're fishing for compliments. This is the most beautiful office I've ever worked in.

SPEAKER_01: Obviously. Can you say the same about New York?

SPEAKER_02: I am very happy to be back in a big city. It suits my lifestyle. I'm so glad not to own a car anymore. Yeah. I mean, the pandemic makes it all a little less lively and less social. So I'm looking forward to all of that being behind us eventually.

SPEAKER_01: Yeah. So everybody calls you merch. You prefer to be called merch.

SPEAKER_02: Merch was fun.

SPEAKER_01: Where does merch come from?

SPEAKER_02: I don't know, I needed a nickname for computer games like 20 years ago, and an urchin has spiked hair. I had spiked hair at that time. Some people would call me basically sea urchin in German. So it's sort of like that meeting a character from a book, a fantasy novel that I had read and it stuck.

SPEAKER_01: And you were at Bicco for five years, four years?

SPEAKER_02: No, for-for-

SPEAKER_01: Three and a third. Three and a third. Great. Well, I'm glad you're going to be building and answering questions and reading and writing here at Chincode. Yeah. So welcome. Thank you. Today, we're going to talk a little bit about UTXO management. And it's something that you've been diving into for quite a while. Maybe give us an overview of what you see as UTXO management and sort of the world of enterprise wallets.

SPEAKER_02: Yeah. Yeah, sure. Well, as you already stated in your last episode, or second last episode with the UTXO set, those are the pieces of Bitcoin that float around in the network. They are essentially what the entries of the ledger is, hey, I have money here, this amount, this address it was received to, and this is the locking conditions that I have to fulfill in order to spend it. So it turns out that when you have an enterprise wallet, you have tons of these because you are scaling to make payments all day long with hundreds to thousands or tens of thousands customers that want to trade on your platform. So they deposit into your wallet, they withdraw from your wallet. And it's a little different than having a mobile phone wallet and you make a payment once a month. So there's a huge efficiency of scale to be had there.

SPEAKER_01: Maybe to give us a little bit more context, like in 2017 fees and the UTXO set bloated. So tell us a little bit about that time and then maybe how enterprise wallets have changed since.

SPEAKER_02: Yeah, in 2017 there was a big hype cycle peak for Bitcoin. People got really excited about Bitcoin and traditionally the times when the price is making big swings is also a time when people participate more in trading, which means they move money back to exchanges and from exchanges. So the transaction volume goes up as price volatility goes up. And especially towards the end of the year, there was just an immense amount of speculation in the market. And between October and January, basically the mempool, the queue of transactions to be confirmed in blocks was just out of bounds, completely crazy.

SPEAKER_01: And so tell us again, just for review, why is creating this huge set of UTXOs bad for individuals and sort of the ecosystem as a whole?

SPEAKER_02: Right. So everybody has to keep track of all pieces of Bitcoin that float around. And this main set, this UTXO set is the means of doing so. There's a huge performance gain if you can keep it completely in memory. But if it gets too large, that's not feasible anymore. And then computers that don't have a lot of memory can't efficiently process the blockchain anymore. It makes it more costly to run a full node, especially in data centers where it's easily accessible and you pay for the resources you use. It also increases the time for people to catch up with the network if there's more traffic on the blockchain. So the initial sync takes a longer time if there's more transactions. Generally, you want to keep the UTXO set big enough that everybody can have their balance represented, but small enough that it's not a resource bottleneck for people to do for you.

SPEAKER_01: validation. Right that makes sense. So maybe fast forward a little bit and tell us about the fee market now. Like what's changed in the last four years and where are we today?

SPEAKER_02: So, I think generally there are more tools and a lot of wallets have implemented more tools to respond to rising fees or to backlogs of transactions. Adoption is not quite as high as I would have liked to see. So we had a halving in May and historically there used to be a lot of news is like, oh, Bitcoin is not dead yet and it sort of gets picked up by a lot of people that are aware of it but not following. And then suddenly the price goes through the roof and so does the mempool.

SPEAKER_01: Got it. Given that we haven't explicitly said it, so what's the interaction between the mempool and the fees?

SPEAKER_02: Right. So the block production is somewhat fixed. It's flexible in that when the miners gain more hash rate, it gets a little quicker. Or in the past couple of weeks, there were some rumors that the rain season in China ended and then some miners started moving their hardware to other locations where cheaper electricity was to be had. And the hash rate in the global network went down by a sixth in the past two weeks. So we've just been having sometimes even a third lower block production. And now usually we have 144 targeted blocks per day. Most of the time it's more like 150. And right now we're seeing about 96 to 100 blocks per day. So there's just less traffic or less transaction confirmations available for the whole network to go through. So the network can process about maybe 2,000 to 4,000 transactions per block. And if there's just two thirds in the number of blocks, it'll do that much less per day. And if there's the same demand for getting transactions confirmed, they stack up.

SPEAKER_01: OK, so things are starting to stack up now, and we're starting to see the mempool get a little bit more congested. So what is that, given what we've learned since 2017, what tools are available for wallets and sort of at their disposal to deal with this?

SPEAKER_02: Right. Yeah, I think we haven't said it explicitly. The mempool is the data structure that holds unconfirmed transactions, right? So what tools there are? For one, you can batch transactions together, which means that you make multiple payments in a single transaction. That's more efficient because it shares the inputs. The inputs are the big part of the transaction. The outputs are fairly small. And if you make multiple payments in a single transaction, you can have fewer inputs per payment. So the overall size of the transaction is smaller per payment. And that is the efficiency gain, because the limit of what can be put in the blockchain is the block space. And if you use less space to make the same amount of payments, you can fit more payments.

SPEAKER_01: Maybe as you're sort of describing these different features available, you could tell us a little bit about how common they are, who's using them, who's taking advantage of them, or...

SPEAKER_02: So batching, of course, requires you to make a lot of payments for you to be doable in the first place. If you're making one payment per hour, you'd have to make the first recipient wait for over an hour until the second recipient comes along, so you can make two payments in one transaction. Obviously, that's not going to work, and you're just going to send out the first payment and then the second payment an hour later. Now if you're a big Bitcoin exchange, and have hundreds of thousands of customers, some of them want to always, there's going to be some that want to withdraw, and you can just make one payment per minute and send to 20 people at the same time. So you'll continuously just have this rolling set of payments, you're batching into a transaction, and just on a clock, tick out a transaction once per minute, and you gain maybe a 70% efficiency gain in block space per payment. Wow, that's quite a bit.

SPEAKER_00: you

SPEAKER_01: Wow, that's quite a bit. What about consolidations? What's that?

SPEAKER_02: Again, this is something that affects you if you have a lot of traffic. Every time you receive a payment, you'll have a new due tick zone, and some of them might be fairly small, right? In some countries, say a Bitcoin exchange in South America, the average deposit size will be a lot smaller than the average batch of payments that they're going to make. And let's say people deposit $20 each time, but when you do a withdrawal, altogether you're trying to send out $400 worth of Bitcoin. So you'd have to use 20 pieces of Bitcoin of those $20 pieces to make up those $400. And you'd pay that at a high fee rate because you want to make the withdrawal go through quickly. And you'd have this huge transaction that you pay premium fee rate for to get it through quickly. And what you'd rather do is, well, let's just consolidate all those 20 tiny pieces overnight, and tomorrow I'll have one piece of $400 worth of Bitcoin, and I'll use that to make a payment. But of course, they need the withdrawal now. So you have to be a little foresightful, and you keep continuously consolidating all those tiny pieces when there is little demand for transactions, so overnight, over weekends, when there is a flurry of quick blocks. With the bigger pieces you have in your wallet, you make batch payments with few inputs.

SPEAKER_01: Got it. Is there a footprint on chain when that's happening?

SPEAKER_02: Yeah, you can tell fairly easily on-chain, because you would be looking at transactions that have a lot of inputs, very few outputs, usually only a single one, because it's a wallet sending to itself, so there's no recipient next to itself, and these might set for a while. So, many inputs, few outputs, low fee rate, it's a fingerprint that usually indicates a consolidation transaction.

SPEAKER_01: And this may sort of bleed into some other parts of your expertise in coin selection, but when you're creating these kinds of outputs, do you want a diversity of different kinds of outputs? Like, how do you sort of think about what it's being consolidated into?

SPEAKER_02: Right. Different values do help because you get more options on composing an input set. That can be helpful to avoid creating a change output, which is when the spender sends funds back to themselves because they overshoot on what they wanted to send to the receiver. I don't think that it is necessarily a valid strategy to seed the wallet with specific values. Okay. Either it happens naturally for you or you'll have a better efficiency gain by just consolidating and then using a single input instead of combining any.

SPEAKER_01: Yep. Got it. Okay. Change splitting.

SPEAKER_02: Right. Change splitting, yeah, that ties into a similar problem. You would want to do change splitting if you have a lot of traffic on a wallet, but you have very few pieces of Bitcoin. So let's say you start a new exchange and you've already lined up a bunch of users and they're biting, chomping at the bit to get started. So you know you'll make a lot of transactions right out of the door. If you start your wallet with one piece of 100 Bitcoin, you'll have a bad time because now in your first transaction you use that piece of Bitcoin and then all of your money is in flight. All of it was used in that transaction. Sure, you'll get the remainder back in a change output, but everybody is going to wait until that transaction goes through or you'll build a chain of unconfirmed transactions which can lead to other problems. And so what you do is you split the change. Instead of sending say 0.1 Bitcoin and getting back 99.9 Bitcoin in a single piece, you'd split it into say eight pieces of various values. And now after the first transaction is confirmed, you'll have eight pieces to work with and you can do eight transactions in parallel that are not in the same transaction graph. And you'll only send an eighth of your total balance on flight if you make a transaction. That's the basic idea. You want to fan out your value to a good number of pieces, especially if you have a very high traffic wallet.

SPEAKER_01: Cool. What other things do we have at our disposal to sort of battle this oncoming feast onslaught?

SPEAKER_02: Since 2015 we've had replace by fee. I think it's a little complicated to implement. There's some UX considerations, but it is an extremely powerful tool to save money, especially as an exchange that can use it fairly versatile.

SPEAKER_01: Can you tell me what replaced by fee is?

SPEAKER_02: So BIP 125 is a way of explicitly stating that a transaction will be replaceable. And that's important because there is some interest from people to accept transactions without a confirmation. We call this practice zero conf. They are interested in keeping the traditional behavior of nodes the same, where a node will only accept the first transaction they see that spends specific funds. We call this the first scene safe behavior. So these transactions that mark themselves as replaceable, they explicitly say, please don't trust me. I'm only going to be reliable after I'm included in a block and confirmed. Before that, the spender may replace me at will. So it gives a second way of sending transactions that does not impact the traditional way of sending the first scene safe way of sending. But people that use replace by fee, they can, for example, put a transaction into the mempool with a low fee rate, barely making it into the next block, maybe at the 90th percentile of the block space. And then as more transactions arrive and get queued to be included in the next block, it might get displaced out of the block. And then they update it with replace by fee, send a higher fee, reduce the amount of change they get back, and bump it up again to, say, the 85th percentile of the block. And once it goes below 95, they bump it up again. So they can continuously keep a transaction at the bottom part of the block. And this is completely different than what most other people do when they send their transactions today. They have to look at what was included in the last few blocks and what is currently in the queue. And then they get a single shot where they pick a fee rate and say, like, all right, this might be good to get it into the next block. I want to be in the next block. Or I want to be in the next five blocks. But they have this single shot of guesstimating the right fee rate. And then they just sit there and wait whether it works or not. And sometimes a block takes an hour. And if you wait for an hour and people keep overbidding of what's in the next block, so they put it more on the top of the top 1 megabyte waiting, it'll get displaced. And then maybe if it's the start of a big backlog, transaction might sit for five days or 10 days if you look at the current situation in the mempool. And meanwhile, if you're doing replace by fee, you can aim to be in the last quarter of the block. And every time it falls into the last 10th, you keep bumping it up to the last quarter. And you don't have to participate in this overshooting extremely, which is the primary reason why the top fee rate in the mempool keeps going up and keeps stabilizing itself for days after a fee event. OK.

SPEAKER_01: And so, wouldn't miners actually be opposed to something like RBF? I mean, wouldn't they want this overbidding to occur? Isn't that in their best interest?

SPEAKER_02: That's an interesting question. So I think maybe from a short term perspective, yes, they would definitely be interested in making more fees. But from a long term perspective, the overall wallet value that they gain from Bitcoin, I mean, they're being paid in Bitcoin. So if Bitcoin becomes more useful, more valuable in general, their payments and the stashes that they've built up over the years, get more valuable. So maybe in the short term, they will try to make as much fees as possible. But in the long term, they should be interested in the overall success of the project. And RBF makes it much easier to get the outcome, the transaction confirmation that you want. It also allows people to bid them bid each other up. So I don't know if it overall would lead to lower fees. It would give people more control to to stop bidding at a certain point to be fine with being delayed or to it just would make the whole bidding process more flexible and fluid.

SPEAKER_00: ehh

SPEAKER_01: Got it. So there's a lot of tools, again, that we've discussed. And one we haven't discussed is SegWit. So SegWit should be helping us with fee management. And then you can talk about that. But I would also like to hear about why isn't SegWit more prevalent? Why haven't we seen it more?

SPEAKER_02: Yeah, so the benefit that SegWit offers is that it increases the available block space in the sense that we can make more payments with a block if we use SegWit. SegWit is a new type of output. Well, I shouldn't say new. It's been around for proposed five years ago, active for three years. SegWit outputs are more block space efficient. If you use SegWit outputs, you directly save money because your transactions will cost less fees, but also the whole ecosystem benefits because your transactions take less of the overall resource, so there's more to go around for everyone. So it's a win-win. Everybody should be using SegWit yesterday, and especially a lot of big enterprises use multi-SIG. Just to throw out a few numbers there, non-SegWit inputs cost almost 300 bytes, and native SegWit inputs cost slightly more than 100 bytes. There's almost a reduction by two-thirds in fees if you switch from non-SegWit to native SegWit. Now we already said these people, they run enterprises that send transactions once per minute to 20 people. I've worked with customers that pay on the order of $100,000 per month in transaction fees, and even if all their system was built with non-SegWit transactions in mind and there's a few changes to be made, I think that overall it shouldn't take more than a couple developer months to roll out a feature like that. And then they'd start saving two-thirds of all their fees.

SPEAKER_01: Seems like a good investment.

SPEAKER_02: Yeah, it just blows my mind that it was a big focus of what I was working on was working with customers and telling them about how to, when I was at Bitco, to improve their UTXO management. And that seemed like such a low-hanging fruit for everyone. You invest $2,000 per month, you start saving two-thirds of all of your transaction fees, in the case that I said, like $60,000 a month. I mean, in most places on Earth, you can pay a lot of people from that. But they're already making money, and a lot of them just make the customer pay the fees. So it's sort of a tragedy of the commons. The customer pays for it, and so it's a lower priority item. They might prioritize a different feature that might attract more customers or something like that. I guess in the end, it comes down to users in general demanding from their services. Look, it's not my fault that you're not implementing SegWit. I'm not paying those fees. I'm going to go somewhere else that uses SegWit, where they make me pay less fees. And then eventually it will change.

SPEAKER_01: But so you were talking a little bit earlier about sort of overshooting and certainly there's a there's a aspect of user experience there where people who maybe don't understand an unconfirmed transaction sitting in the mempool for or weeks or whatever the case may be means that they will overpay for piece to get that sort of instantaneous confirmation. Can you tell me a little bit about how enterprises now are estimating their fees? Are they using it? Are they sort of using something like Bitcoin core in terms of looking at their own mempool or like, how do they actually do it?

SPEAKER_02: So, there's a bunch of different services that offer estimates on what fee rate will get you confirmed within whatever your target number of blocks is that you prefer, and some just use these third-party resources to guess. I think that scientifically, research is definitely not done with making better guesses, and some other approaches explicitly look at the mempool, and some even combine the two. That does help. It also is less gameable. For example, a miner could just fill the mempool with a lot of transactions they don't intend to include in blocks. Say you had a cabal of miners that all don't touch these transactions. They could fairly cheaply introduce a fee floor that you need to go above, or it looks like you need to go above in order to get confirmed. But we can also just sidestep this whole one-shot problem by continuously monitoring where our transaction is in the queue, and then putting it at the right point of the queue. So if you would say, for example, hey, I have this payment I have to make. I have 24 hours to get it confirmed. So I'm aiming to be in the next 140 blocks, or let's play it safe, next 120 blocks. And then you can just put it at the bottom of the mempool, and as this block that you're aiming to be included in approaches, you just bump it up so it stays at first the top 120 megabytes, then when it's only 100 blocks away in the top 100. So you bump it up, and eventually maybe bump it to half of what you're aiming at, bump it to the top 50. Now if nobody adds any transactions, you'll be in the next 50 blocks, which is way ahead of what your requirement was, but you probably paid a fraction of the top fees. So if you think more about when does this actually need to be confirmed, and you give yourself that time, you can often, like right now you can save up to 90% or 95% of your fees if you can wait for the next weekend.

SPEAKER_01: Got it. Cool. So we've talked about a few different, maybe better known things. What's an Omnibus wallet?

SPEAKER_02: Oh, this is a concept that comes up in enterprise wallet stuff. So as a solo user, you'll have all your funds, of course, in a separate wallet. And you probably all know your Five View takes those by first name. But in an enterprise wallet where you literally get hundreds of deposits per hour, the first approach many people do when they start building a service like that is, oh, I need to have separate address spaces for each user that I have. And then they basically do their account management on chain. And it is terrible. It does not scale at all. I think one very well-known company here in the US would, when you withdraw money, send it through an address that belonged to that user first so that the return address for the funds would actually tie it to that user. So every time somebody would withdraw, they actually made two payments on chain for every single withdrawal. And that just basically took multiple percent points extra on-chain traffic just to process. Thank you.

SPEAKER_01: It just sounds like a relic of a time when traffic wasn't being considered and fees weren't being considered.

SPEAKER_02: Right. And then of course that time is over and you're with those structures. So as an enterprise though, you're taking custody of the funds in the first place already. So what you really need is you need to know who to credit your IOUs in your database when they deposit. And then when you send out, you send to their address and you don't have to send from specific funds. This is your stash, your custodial bit of Bitcoin that people sent to you. You have custody of the Bitcoin now, you owe some, but why does that have to be on chain, this accounting? So the idea of having an omnibus wallet is you have a single wallet for all of your users and you distinguish user deposits by giving out different invoice addresses. Right. So here's Jonah's address. When somebody sends Bitcoin to this address, we will credit Jonah's user account and we'll offer him a new one every time the address has been used. But also there's a lot of address reuse, unfortunately, there. But it distinguishes who to credit on the deposit and then you have all the funds in one wallet. And now you can do stuff like consolidating, batching, maybe even take 70 or 90 or more percent of your value and put it into a non-hot wallet. You don't want all your funds sitting there on a server in AWS. And if somebody breaks in, they can take all your money. So you just keep an amount that you need to do your business with and the rest of it goes into a stash somewhere else more secure. And all of this is the concept of having an omnibus wallet where everything goes into one part. Got it.

SPEAKER_01: What else? What else did we miss?

SPEAKER_02: Off-chain sending might actually work well with omnibus wallets, because once you have the accounting already in your database, right?

SPEAKER_01: Okay, so tell me about off-chain sending.

SPEAKER_02: Okay, well, you have the omnibus wallet, right? You get the deposits into the wallet and have virtual accounting. Now, you already have all your users basically in your database. And if they're trying to send to each other, why the hell would you put it on the chain? If you know your user Alice is sending to your user Bob, you just update your database. And that's the idea of off-chain sending, right? Why would I put that on the chain if I know it's all in my data anyway?

SPEAKER_01: That doesn't seem, that doesn't sound very Bitcoin-y, updating a database there.

SPEAKER_02: Yeah, so there's actually quite a few critics of custody in Bitcoin altogether, but nothing in Bitcoin precludes people from offering banking services to Bitcoin users. And if they're going to send a ton of money that way and make it a smoother experience, such a payment inside a database is instant, right? No waiting, no fees. Of course, that'll be attractive to some users and make it more efficient. And in my opinion, it is a form of off-chain scaling, which can cause more Bitcoin payments to be made without having a huge footprint on the blockchain. Is it the right solution for everything? No. Should all money be in custody? No. Then a lot of what's important about Bitcoin to me wouldn't work anymore. Is it maybe the right thing for my grandma that wants to have exposure to Bitcoin but doesn't want to have her own treasure next to her knitting set? Yeah, maybe. Maybe I'd be more comfortable with her holding her money in custody and looking at it through the lens of a web interface, yeah.

SPEAKER_01: Cool. Is there anything else that you're excited about in the near future, maybe that's going to help with this, or?

SPEAKER_02: Maybe Taproot, Schnorr, you know, so we talked a little bit about more efficient output formats previously, so SegWit made transactions take less block space. Taproot will do that again to another even, so for a native SegWit 203 multisig, it'll go from 105 bytes to 58. That's a reduction of over 40% again. And additionally, it'll increase privacy because single SIG payments can look the same like multisig payments. So we just got the code merged to Bitcoin Core. People are still debating activation parameters and so forth. I think we might see it mid-next year active on the network if everything goes smoothly. If there's another, it might take longer. And once we get Taproot out, we will see another huge efficiency gain in block space.

SPEAKER_01: yeah something else to look forward to yes cool great and uh maybe we'll do this again soon yeah let's do this again soon cool bye for now

SPEAKER_02: Yeah. Bye. What kind of guy is he?

SPEAKER_01: you

SPEAKER_00: So Jonas, how was it to talk to another human being besides your family?

SPEAKER_01: Pretty good, getting right back in that saddle and, you know, a little rocky. Had a couple moments that, you know, I just remember what it's like to be on a podcast, but. Kind of warm up. Yeah, well, I think we did alright.

SPEAKER_00: Gotta warm up. I think you did great. Well, thank you everyone for listening. We're very happy to be back. You can visit us at www.chaincode.com.

SPEAKER_01: or Chaincode Labs on Twitter. All right, bye everyone. Bye everyone.


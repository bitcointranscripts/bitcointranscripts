---
title: MiniMint, Federated Mints for Bitcoin scaling and privacy
transcript_by: Stephan Livera
speakers:
  - Eric Sirion
date: 2021-12-17
media: https://www.youtube.com/watch?v=5KbY4IX0-NQ
---
podcast: https://stephanlivera.com/episode/331/

Stephan Livera:

Eric, welcome to the show.

Eric Sirion:

Hello. Yeah. Happy to be on. Nice to meet you.

Stephan Livera:

Yeah. So Eric, it was great to read about your proposal and read about what’s going on with MiniMint and all this stuff. And I think it’s definitely a topic that SLP listeners will be interested to hear about, ideas related to this, privacy, scalability, all sorts of things. So do you want to give us a little bit of your background, as much as you’re willing to share without doxing, of course.

Eric Sirion:

Yeah. Sure. My background is in computer science, especially in distributed systems and cryptography. So that naturally led me to explore different systems like Liquid on Bitcoin and federations, Byzantine fault tolerance. And at some point I had this idea for Chaumian E-Cash and building it on Bitcoin. That’s why we’re here today.

Stephan Livera:

Excellent. And so for listeners who are not familiar, what is Chaumian E-Cash?

Eric Sirion:

Yeah. Most simply explained, I think it’s a way to exchange some asset that has value, for example, Bitcoin, for an IOU token. And that IOU token has this nice property that it’s fully anonymous. Like you engage in a protocol with the—let’s call it mint, because we can say it’s like a minting process when this IOU tokens are created, and you send the mint some amount of money and in return you get IOU tokens. And later on, when you want to spend them, the mint can’t recognize during which issuing operation they were actually created. So you’re fully anonymous, which is great.

Stephan Livera:

Right. And so listeners who are maybe new to Bitcoin, you might recognize that Chaumian E-Cash and this whole idea by David Chaum is arguably like a predecessor idea to Bitcoin. It’s been around for a while before Bitcoin. Obviously there’s certain distinctions between this idea of a IOU token, because obviously in Bitcoin, we are also all about this idea of not your keys, not your coins, don’t trust IOUs, et cetera. But why would we even look at these IOUs? What are the benefits of this kind of system and the trade-offs versus literally just HODLing Bitcoin?

Eric Sirion:

Yeah. That’s a really interesting question because Chaumian E-Cash has been around since the early eighties, but it never really caught on. And my theory for why is that you always had the centralized entity, the mint, which controlled all the money and thus could easily either exit scam the users, or could be taken down by a hostile government. And they tend to be hostile against anything that has to do with anonymity and privacy. So it’s no wonder that we don’t see big Chaumian mints today. But what it didn’t have back then was a way to hold an asset in a distributed manner. And we have that today. Like with Bitcoin, you can hold value in a multisig wallet. And that means, for example, if you have a two of three multisig wallet that only if two of three people cooperate, they can actually spend the Bitcoin. And that made it really interesting to revisit the concept of Chaumian E-Cash because now we don’t need to have the centralized entity, but could still get the privacy properties from the Chaumian E-Cash protocol. And the way we do this is the backing funds are now held in a multisig wallet, while also the issuing operation of these tokens can be distributed using fancy cryptography. We probably don’t need to get into this here, but essentially you’re taking the Chaumian mint and you split it up into multiple parts and now a certain amount of these parts can become malicious, actively malicious, without the whole being badly influenced.

Stephan Livera:

Right. And so essentially it offers different characteristics. And now with Bitcoin and multi-signature technology, allowing us to have multiple people who are signing a transaction— we’re taking that idea even further. So it’s like you’ve got Bitcoin where typically people are thinking of like, Oh, I’ve got my coins in my hardware wallet or in my whatever. Then you might have Liquid as an example, which is a Federation and people peg in and peg out. And so it’s a sidechain. And then taking it even further is this idea of the federated mint. And so that’s what you are explaining here. So could you tell us a little bit about this idea of a federated mint? Like how would it work? Who would sign up to be a member? How would you use it?

Eric Sirion:

Yeah, the main benefits as we already touched on, one privacy, that’s what I already mentioned, and also scalability to some degree because mints also allow you to do internal transactions with these E-Cash tokens and that’s the second big reason why we might want them. And so to the question who would potentially be users, I guess like most people actually that want to use Bitcoin in some way. And why? Because like the biggest problem, or one of the biggest problems Bitcoin has today is scalability. And we can solve this to some degree with Lightning, but like Lightning is really cumbersome to run from an end user’s point of view. And so even today we see many people using custodial solutions. And these people that today use custodial solutions, these are my primary target audience. Of course everyone else who wants some privacy can use a federated E-Cash too, but the primary audience uses fully custodial services today because for them, it’s a clear improvement over the state of affairs right now. And who would run these federations? I can only theorize about that. But for example, I can imagine like your local community, if you’re living in a village in El Salvador, probably has some technical people and they can be the Federation members while the others are only users. And we are already seeing this with Galoy and Bitcoin Beach Wallet. They have a very similar approach, a bit more manual and without the privacy properties, but essentially they’re running the same model there and it works. And it’s great. And what I want to see is many of these federations distributed around the world, and you just choose whichever Federation you trust, you want to trust, because you might already have an existing trust relationship, especially in your local community. It’s not a big deal to maybe trust some of your neighbors, like you’re trusting them anyway. And since no single one of them has full control over your coins, there’s also not so much risk that they just run away one day because of some long tail event, like some black swan event, because they would still need to convince others to defect with them.

Stephan Livera:

I see, yeah. And so just for listeners who just so everyone can follow along, you might be interested in the earlier episode I did with the Bitcoin beach guys, but a quick high level is this idea is it is a custodial Lightning wallet, and people can onboard to the Bitcoin beach wallet. It’s a custodial wallet and they can send and receive Lightning. And it’s interoperable with the broader Lightning Network. But in the background, they also have on-chain storage and that is done with a multisignature. So listeners could think of this federated mint or MiniMint idea as like a competitor idea to that, but in a similar way that theoretically there could be lots of these mints around the world. People could be trading in an IOU way, but that could arguably be a little bit better, or maybe a little bit more private, maybe a little bit more scalable. And the idea as I’m understanding from you is that it could still be interoperable with other mints around the world. And you could sort of swap in and out of mints and into on-chain or into Lightning, potentially.

Eric Sirion:

Yeah like that’s a central part of my more recent research into this idea. Like initially I was just thinking about the federated E-Cash part and how to build it on Bitcoin using on-chain primitives. But the more I thought about it, the more it became clear to me that if we have to mint only able to interact with on-chain Bitcoin, then it will be a big centralizing force because people couldn’t easily switch between different mints. And if they would want to, then they’d either have to be some trust relationship, which is not good because that just becomes like this old banking network where banks trust each other and settle their payments at the end of the day. We don’t want this as Bitcoiners. So the biggest improvement after that point was integrating Lightning. And with the help of some people, some other developers, I figured out how to integrate both incoming and outgoing lightning transactions with federated E-Cash. And that essentially makes it into a supercharged Lightning Wallet. Like now you have a fully anonymous Lighting wallet that can interact with any other Lightning node like through invoices. And the other lightning node on the other end might be another mint, might not be another mint. You don’t even have to know. So it forms this network of federations included in the bigger Lighting Network, which I think is quite beautiful.

Stephan Livera:

Right. Yeah. That’s really interesting. So we’ll get into some more around that later. I think it’d be good to just talk through some of the high level ideas, like, so deposit, withdraw, internal transactions. If you could tell us a little bit, what does it look like? As an example, I bring my 10 million sats and I want to deposit them into the mint. What does that look like? What’s going on under the hood when I deposit my 10 million sats?

Eric Sirion:

Right. Let’s assume for a moment that you have on-chain Bitcoin and want to deposit these into the mint, then what you do is much like reflected. People might not be familiar with this. So I will in it for a moment. You generate yourself an address which you know is related to the Federation’s public keys in a certain way. We call the operation done there key tweaking, like you add some secret value to public key, and that gives you new public key. And you can this to all the federations public keys, and then generate the multisig address that way, because you know the public descriptor of the Federation, and then you send your 10 million sats to this generated address. Now the mint can’t yet do anything with these coins because it doesn’t even know it owns them. So in the next step, what you do is you show the mint the secret value used for tweaking and by doing so you also verify yourself that was actually you who sent these funds there, because no one else could have known the tweaking value which led to this address and the secret tweaking values also needed to even spend these coins. So by giving it to the mint, you transfer the ownership in a sense, and in return, the mint will issue you a certain amount of these E-Cash tokens, because one thing that really needs to be mentioned here, to be anonymous, these E-Cash tokens need to have a common denomination. And that might be like 1 satoshi. And like in the really naive model, you would now get 10 million of these E-Cash tokens. But that wouldn’t be very efficient. So in the more like engineered version of this, you would get instead like one E-Cash token that is worth 10 million sats, or like 10 E-Cash tokens that are worth 1 million ssts, depending on how you want to manage your E-Cash tokens, that’s up to the user. And you would engage in this interactive issuing process essentially. And once you have E-Cash tokens, the mint can’t tell anymore in exchange for which Bitcoin transactions, these were initially issued, and you can do whatever you want. Like you can send them to another user, like physically send the data to another user. And then the user can go to the mint and exchange them for new E-Cash tokens. That would be like a transaction, because by giving the E-Cash token back to the mint, you validate if it was already spent, so you really need to do this to avoid double spends. And the user who received your tokens then gets fresh tokens. You don’t know anything about them, the mint doesn’t know anything about them. So it’s fully anonymous again. Or what you could also do is use some of the tokens to generate new on-chain outputs by telling the mint, please give me a 1 million sat on-chain output to this address. And I give you this one 1 million satoshi E-Cash token, or also give the mint some Lightning invoice and tell them, please pay this for me and I will give you the equivalent amount of E-Cash tokens in exchange. So there are a lot of options you have to interact with the mint.

Stephan Livera:

Right. And so we could think of it like, so those listeners who are used to Lightning, they could sort of in a loose sense, think of it like a swap server. Like you can swap in Bitcoin on-chain and swap it out. And so we are essentially getting more privacy for the user who I guess, presumably they might connect over TOR or some kind of anonymization net layer or network. And so then the idea is this federated mint doesn’t know who I am, right? For all intents and purposes I’m just this other person on the other side of the Internet, I didn’t have to do KYC know your customer rules. I didn’t have to provide my ID. And yet I can peg in some Bitcoin into this system and transact around inside that system in the private E-Cash tokens. And then when I need to, pay out to a Lightning invoice or swap it out to a Bitcoin on-chain address, correct?

Eric Sirion:

Exactly. And the beauty of the system is that really there aren’t any accounts, at least in the pure E-Cash version. Like every time you connect to the mint you do it using a different TOR circuit, like at least in the final version it will be the way you do it. Currently in my implementation, it isn’t the way yet, but in the final version, you should use a different TOR circuit every time so you can’t be correlated. Like if you do multiple operations after each other, then the mint won’t be any wiser who did this, because the E-Cash tokens are fully anonymous. You have an anonymity set of every E-Cash token ever issued of the same denomination. If you imagine Alice Bob and Carol are getting one E-Cash token issued, and then someone spends an E-Cash token, then the mint can tell if it’s Alice, Bob, or Carol. It’s just not possible to tell.

Stephan Livera:

I see. Yeah.

Eric Sirion:

So it gives you a very high amount of anonymity, and especially if Lightning, like all the attacks on Lightning privacy, essentially that uses surveiled channels and that you correlate like payments to node IDs. But in this way, like multiple users are using the same Lightning node, so it gives you the entire Federation user base as the anonymity set, which is quite a nice improvement in my opinion, because neither the mint can tell anything. Like they only see someone spending E-Cash tokens to pay a lightning invoice. They can maybe learn something from Lightning invoice, but you can strip it from the description and some of the meter data, you can just take it out of there because it’s not needed. Like the only thing they really learn is to whom you pay. And even that can be solved eventually. Like I remember you had Bastien Teinturier on your podcast and you discussed some ways to do this, like to even hide the recipient of a payment. And once this lands for Lightning, then such a federated E-Cash mint would be the ultimate private lightning wallet.

Stephan Livera:

Yeah. Really fascinating to think about. And so, as an example, let’s say we’ve got this network of, I don’t know how many tens thousands of mints out there. Tell me if this idea makes any sense. Like, let’s say as an example, I put in my 10 million sats, I receive my ten one million sat E-Cash tokens. Would it make sense to ever try to swap across to different federated mints, or is it more just like, I am placing a little bit more trust into this one particular mint who I got those IOU tokens from?

Eric Sirion:

I actually did some research on that, because there was a discussion on Twitter sometime ago, if it’s a better to, let’s say you have have a mint with four participants, a Federation of four participants, and would it be better to evenly split your funds over these four participants individually, or to form a Federation and put all your funds into the Federation? And actually the answer depends on with which probability you assume any single participant to defect, like assuming they’re independent actors and are not correlated in any way. And as long as your expectation is like below 20% defection rate, you should really just leave it in one big Federation. That’s depends a little bit on Federation size and some other factors, but generally the Federation is safer. The main drawback I’d say is that the larger you make the Federation, the slower it becomes. All the BFT consensus algorithms, they scale badly with the size of the Federation. So eventually you want to set a limit to the Federation size. And so maybe for some people, it makes sense to diversify over multiple federations, but then again, it makes payments harder because at least currently I’m planning to implement payments in a way that you can only use funds from one Federation for lighting payments, let’s say. And so you have to switch back to one Federation before making like a big payment of all your funds going somewhere else. So it’s a trade-off, but generally I imagine in the future, when there are multiple of these federations, they all speak an interoperable protocol. So if you have a client that could totally like just support multiple federations and you could have funds in multiple federations, right? Just makes engineering a bit harder and maybe your access a little bit less easy.

Stephan Livera:

Okay. And so, as an example for that user, with presumably they have some kind of wallet that manages their E-Cash tokens, would that wallet now have to manage balances across multiple federated mints as an example? Or is it more like maybe the model might be more like an exchange or let’s say a Bitcoin beach or some other town or some area who wants to set it up. Everyone just has a wallet and that wallet just connects only to that one, federated mint for lightning payments, Bitcoin payments, you name it.

Eric Sirion:

Yeah. I think in practice, it will be like that. That you only have one mint you call your home mint and that’s where you keep all your funds. And like if someone from another mint wants to pay you, then you can just generate the lightning invoice and your local mint generates this lightning invoice and will give you the funds after it’s paid. There are some tricks to do this, and so it doesn’t really make sense for most users, in my opinion, to hold funds on multiple mints. Maybe if they’re in different communities, it might make a little bit of sense because if you’re paying purely internally, you cut out the lightning parts, so it gets a little bit faster. But in the end, I think for most users, it’s easiest also from a mental model perspective, you need to make this understandable to users to have good UX, that in the end, you just choose one mint, one Federation you trust, and then you use them and don’t care about anything else.

Stephan Livera:

And so, yeah, it’s sort of similar to how, if you think how the Bitcoin beach wallet works when they create a lightning invoice, any other lightning wallet can just pay that invoice. And so it’s a similar kind of idea that each of these mints are around there and your wallet would connect to that mint as an example. So we spoke a little bit about deposit. We’ve spoken a little bit about withdrawing, so I guess you are spending out of the mint, you are kind of withdrawing your E-Cash tokens in that sense, or you’re paying out a lightning invoice. And then internal transactions, is there, obviously that would be kind of the easiest of the category because you would just be paying internally to some other person who’s also a part of your mint, right?

Eric Sirion:

Yeah. Like I already explained how you could just give these E-Cash tokens to someone else. That would be the simple internal transaction. And they can go to the mint and request newly issued tokens in exchange for burning the old ones. And that would give them like full access to their newly received coins because now they know they won’t double spend. But in practice, I don’t expect this to happen that much because it’s a UX problem again. So if you now have to decide, do I want to generate like an internal invoice or an external invoice? That doesn’t really work that well, because then people need to know, are we on the same mint?

Stephan Livera:

Right, it’s not very practical to do that.

Eric Sirion:

Exactly. Like, it’s the same problem Chivo has currently in El Salvador. Like you never really know if the one who is generating your invoice, are they generating Chivo invoice or lightning invoice? So it’s a big mess and you really want to avoid this. So instead what I’ve been doing is even if two people are on the same Federation, you can still generate an invoice, but the Federation just recognizes internally, Yeah we don’t really have to pay it over lightning because we own both sides of the equation and we can just settle it internally. So that’s no big deal.

Stephan Livera:

Yeah. I see. I see. And so I guess that’s the other question: as people are using this kind of idea, I mean, there’s different ways it could work, but maybe one way is people might have most of their coin on say their hardware wallet or their multisignature set up. And then maybe the amount that they keep inside the mint is more like the day-to-day spending amount. Is that potentially one way you’re seeing it? So that they wouldn’t be risking all their funds? They’re just risking a small portion? Is that how you’re seeing it or do you see it another way?

Eric Sirion:

Yeah. In the beginning, definitely. I mean there are different use cases for this technology. Like the one you are mentioning is Bitcoin users today that might even be able to run their own lightning node financially and technically, they might want some privacy because lightning isn’t the end-all, be-all for Bitcoin privacy. So that would still be an improvement. And if you only risk some day to day spending funds, that’s definitely okay with Federation. Like it would probably even be okay in like a single mint, like a single-sig mint. But down the road, what I imagine is that people might actually keep their entire network, especially in poor countries where your entire network might be a few hundred dollars, might keep it all in such a Federation. And that’s the market where I think it will have the most positive impact because that’s a market that is traditionally underserved because it doesn’t make sense for banks to be there, like say El Salvador, most people don’t even have a bank account. I think I read somewhere that like more people have Chivo wallet than a bank account, which is amazing, like after a few months. So in these markets, people might not be able to actually have on-chain Bitcoin. And that’s where it actually makes sense to have this Federation, to have all this complication from distributed protocols and all this stuff, because if you have all your life savings in such a protocol then it really needs to be secure and you can only achieve this wide distribution via having multiple parties that run it. And so down the road in these communities, I think there might be people that only rely on such federations to make their payments, to save. And yeah, there’s some interesting ideas about this we can maybe discuss later.

Stephan Livera:

Okay. And so to be clear again, the users of this mint are essentially trusting the operators of that mint to not run away with the money. Like that’s the IOU part. Like they could run away with the actual on-chain funds, the actual Bitcoin. But that’s the trade-off here, is essentially that these are people who might have otherwise been custodial with an exchange or custodial like only having paper Bitcoin in the sense of having let’s say GBTC or one of those paper synthetic exposure to Bitcoin, as opposed to having some way to actually pull it out and claim it on-chain or into a lightning wallet or into something.

Eric Sirion:

Yeah, definitely. Like the people I was talking about that might have all their money in the Federation, they would never really have a chance to go on-chain. Like they would be on a custodial solution either way. And the big benefit of Federation is that even if—like, let’s say we have a four-member Federation, then one may be malicious and it all keeps working. Like you can still make payments, it still works. Like if two are malicious, then it’s not operational anymore. So you can’t make payments anymore. And they might try to extort you, but they still can’t steal funds. That’s the big part. And only if three or four people go malicious, then they could actually take the funds, which in my opinion is a much better chance of keeping your funds than on most exchanges. Especially if these people are someone you cannot know, like they have trust of the community and they would burn a lot of social capital and it might make it not worth it to cooperate and just take all the money. Especially if these mints don’t get too big. Like the idea is having many of these and having them interoperable that none becomes too big to fail. Like they should all stay rather small and like in their community so that we never have systemic risks to Bitcoin.

Stephan Livera:

I see. Yeah. And in fairness, there are a lot of exchange users who just leave it and trust the exchange. And obviously in years gone by there have been exchanges who have been very lax about their security and have been operating with say a single signature setup where maybe the CEO of the company or one person could just steal all the Bitcoin or based. This is obviously quite a strict improvement on that. So that’s an interesting idea. Now we were talking about fee savings and scalability, I guess maybe this is a little bit of a how long is a piece of string question, but could you outline for people how they should think about the fee saving or scalability win here?

Eric Sirion:

Like on a purely technical level, the first saving comes from multiple people sharing one lighting node. And that’s something that could also be achieved using channel factories where multiple people share UTXOS and a shared set of channels. But channel factories are still very theoretical right now and also will require people to be online all the time. And like that’s, in my opinion, not quite suitable for the demographic I’m targeting. And so the big benefit here is that let’s say you have 100 or 1000 people in your local community. And instead of everyone managing their own lighting node, which means at least opening one channel and eventually closing it, now you maybe have one node that has 10 channels, and that reduces the amount of on-chain transactions by 10X to 100X in that scenario. Apart from that, of course, you also hold some on-chain UTXOs as the backing funds of the Federation, but I think their movement will be negligible compared to like rebalancing lighting channels, which would probably be a much more common scenario. And so it’s definitely a big improvement in scalability. And also when you’re not using lightning, especially in the local community context, if everyone is on the same mint, then you can essentially make definitely many transactions, like as many as you want. As long as the computers running the Federation members are fast enough to process all the requests. And that’s the only limiting factor. And that could be hundreds of transactions per second.

Stephan Livera:

I see. And so potentially that could be huge, huge fee savings. Because let’s say hundreds or thousands of users could all be operating off of one mint and all of their payments and receiving information is being essentially bundled into this entity as opposed to each of those people opening their own lightning channels, doing their own everything. Of course there’s certain trade-offs around this, but as we mentioned earlier, these are the people who might have been custodial users anyway. One other thing you mentioned, the idea of channel factories or also known as multi-party channels. And so that would require anyprevout, which is another potential future soft fork upgrade. And so Christian Decker and AJ Towns and people like that are working on that kind of idea or have written about it. Are there any changes to Bitcoin required for this MiniMint idea?

Eric Sirion:

Not really. There never was any necessity, but now with Taproot, we actually have an upgrade path where we can take the federated on-chain wallet and make the transactions much smaller because now instead of needing this, let’s say we have a three out of four Federation, then right now we need to include three signatures and four public keys with each transaction. And instead, what we can do now is bundle them all together into one Schnorr public key, one Schnorr signature, using some special signature protocol like Frost. And now we have much smaller transactions that are also indistinguishable from any other type of transaction, which is great.

Stephan Livera:

I see. Yeah. And so for listeners who are unfamiliar with that one, go and check out the earlier episode, 200 with Christian Decker or perhaps the earlier episode, the panel discussion from Tabcon about Bitcoin on-chain scaling. And so Eric, the other question I’ve got for you is what’s required for the Federation runners, like the uncle Jims of this Federation? What kind of work are they doing in this? Is it essentially they’re helping manage a multisig of the on-chain outputs and then potentially also helping manage the lightning node that’s attached to this MiniMint? Is that the idea?

Eric Sirion:

We haven’t been talking about the actual way to integrate lighting with this all that much yet. So there is a distinction that we made between the Federation proper, which holds all the funds and is secure and n out of n multisig. And there’s also an external entity, which I call the lightning gateway, which actually makes all the lightning transactions. And the Federation merely incentivizes this lightning gateway to do the transactions the user wants. So for the actual federation members, all they have to do is run some software that is configured in a certain way that all the nodes connect to each other, and you run it and forget about it more or less, like that’s at least the idea. Then the lighting gateway, it’s a little bit more complicated. That actually needs active management because it’s lightning out, you need to balance channels and open new ones, close old ones. There, you really need someone technical. For the Federation members, you can actually say like, as long as someone can install a piece of software and keep a computer running consistently and in a secure enough manner, then they can do it. With the lighting node, it’s more complicated, you need an expert.

Stephan Livera:

Right. So essentially they would need a routing note operator to do that role. Of course they can use tooling, the likes of thunderhub and amboss and lightning terminal and RTO and so on. But they would need to know how to operate the nuts and bolts of that. And then from a privacy point of view, let’s explore that a little bit. So currently people who want to be private in Bitcoin today, it generally requires the use of various or multiple privacy techniques. You might be using, say coinjoin to mask your on-chain footprint. You might be using TOR to sort of anonymize or mask your internet, your IP footprint. So with the MiniMint idea, the privacy aspect mostly comes down to the anonymity set of the different amounts. So let’s say you’ve got a 1 million sat IOU token or E-Cash token and a 10 million sat—I mean, I guess that’s similar to how let’s say in some of the coinjoin implementations, they have set fixed amounts, like 1 million stats, 5 million stats, 50 million stats. It’s kind of similar in that sense, because they’re creating an anonymity set that whoever was paying out could have been any one of those people,

Eric Sirion:

Right. Exactly. It’s the same problem they’re trying to solve with this. And I think for MiniMint, it won’t be a big deal because as long as most people are in the same range of network, let’s say, then they should have a similar distribution among their different denomination E-Cash tokens. What could be problematic—if you have one really rich guy in your local community, and everyone knows he’s rich, right? And no one else has nearly as much capital as he has. And then he might be the only one who keeps like 10 million sat E-Cash tokens around, like, he’s the only one who gets issued these. And that would be a problem because you could definitely identify his transactions because only he would spend these high value E-Cash tokens, receive these high value E-Cash tokens. And so if you have a huge disparity in network, then it might make sense for the richer people to keep more of the lower denomination tokens. But in practice, like why would you do this? Like, if you have enough money, then please take some money out of the Federation. Like you can store it at on-chain UTXOs like, especially if you have 10 million or 100 million satoshis, then that will probably be always worth having on-chain UTXO. Like for smaller amounts, maybe not, we don’t know, but for such huge amounts that I think hundred million, should it be like 0.1 Bitcoin? But you’d probably want to have this as a UTXO owned in your hardware wallet, or even your own multisig setup, something like that. I don’t see the big problem

Stephan Livera:

So essentially the idea is there would be a big enough number of people all using the E-Cash tokens and of the similar amounts, right? The 1 million sat or whatever amount. And whenever they are making payments, or swapping out, it’s all mixed around and balanced around because of that. And so then privacy then is helped and protected a little bit because now you’re not trusting one central entity not to dox those individuals. And presumably in this idea, these individuals could have signed up for that mint without KYC. So that’s actually the other interesting part, that they could operate the mint without that. And maybe as another example, let’s imagine some of the Bitcoin exchanges of today, they might be able to provide a privacy benefit to their users because they could have had to maybe KYC that user on the way in, on the website. But actually if they could provide them a minimint way to spend, then they’re kind of spending still in a private way. Although it depends if the regulators would be okay with that or the compliance team would be okay with that, they might not.

Eric Sirion:

I had to talk with some people interested in issuing securities using the same E-Cash technique. And the other idea was you KYC essentially on every like when you enter the system or when you exit the system, but what you do in between, nobody really cares, like that’s one way to look at it.

Stephan Livera:

Yeah. And that kind of reminds me of stablecoins even like Tether today or even like Liquid assets or kind of a similar idea there. Right? Like, is it STOKR?

Eric Sirion:

Yeah. The STO one yeah. The security tokens offering stuff. There you always have a co-signer that knows your identity. So your trading partner doesn’t need to know, but there’s some entity where you have KYC and yeah. Not a big fan of KYC in general. Kinda still hope someone will build a no-KYC STO tool. And then maybe we will actually see some of these federations incorporating as like autonomous organizations, like actual Bitcoin DAOs.

Stephan Livera:

Right. Like a true anarcho-capitalist lightning IOU E-cash bank all merged into one and people can sort of get some more privacy by being a member or a customer of this, that kind of thing. That’s an idea there.

Eric Sirion:

Nobody has to be identified because it’s just software and providing the software. And if some Twitter nyms come together and run such a E cash Federation, who is to stop them? Like run it behind TOR and like, okay, good luck, big brother.

Stephan Livera:

Right. And I think that’s the other aspect as well, because with Bitcoin and privacy, we have to think about it holistically. Because it’s like, how did you acquire those coins? And how did you spend those coins? Because if you had to KYC to get those coins in the first place, well, that’s already a big part of the battle being lost right there on the get go. So I guess the idea potentially, like, let’s say in the future, I mean, this might be years off before this idea even comes to fruition, but it might be that people want to acquire some of their first sats by getting these tokens, like maybe in the future there’s peer-to-peer markets. And as an example, you Eric want to get started with Bitcoin. And I’ve got my, whatever, my a hundred thousand sat E cash token and you pay me whatever the fiat value of that is in cash. And I sell you this token. And that’s your no-KYC onboarding.

Eric Sirion:

Yeah, exactly. And like one interesting fact here—you don’t have the problem of incoming capacity you have with lightning, like with lightning you would need to open a channel first to receive these funds from you, but with federated E cash and lightning integration, you have this one lightning node someone else is running and presumably they will always keep enough incoming capacities so they can actually collect the fees from allowing you to receive and send funds. So you can actually go to someone who sells lighting Bitcoin like for cash or whatever, or gold coins, and then just receive via lightning and get E-Cash tokens in the end. I think that will be a really smooth onboarding experience because it has low fees. Like lightning has super low fees. Like all my lightning transactions are treated 0.1% and 0.2% in fees. And then maybe at open 2% in fees from the Federation or whoever is operating this. But now we can physically buy Bitcoin without any on-chain fees. And I think that will be nice peer-to-peer future.

Stephan Livera:

Yeah. So to be clear though, that would require a network effect to be built up around this, right? So as an example, there’s nothing stopping people doing this, even now with say Liquid BTC, right? They could be trading L BTC for cash, but it’s not like there’s very liquid and big markets for that today. But the hope is that people could use these minimint ideas as a way to potentially onboard into the network in a private way. And then later when they want to, they can withdraw those coins out into their—let’s say they’ve accumulated a large enough balance of E cash tokens. They can now withdraw that out to their hardware wallet, or their multisig on-chain, take it back on-chain and have only the spending amount inside the mint.

Eric Sirion:

And I’d say, there’s not even the big bootstrapping problem that Liquid is facing because if you integrate lightning from the beginning, then everyone who supports lightning supports your solution, in that case federated E cash.

Stephan Livera:

So in that sense you can piggyback the lightning network network effect. Because anyone who can already take a lightning payment can now receive a payment from the mint.

Eric Sirion:

Yeah and everyone who can pay a lightning invoices can sell me Bitcoin, like without opening a channel to me, like that’s the biggest problem today and it’s solved in different ways. Like I had a great conversation with FiatJeff and Anton I think about hosted channels some weeks ago. And that’s another solution, more centralized than federated e-cash, but like, we need to solve the onboarding problem with lightning because currently whenever I want to sell Bitcoin to someone physically, it’s always on-chain because there’s no good way for them, if they have a lighting wallet, to just receive. Like either it’s fully custodial right now, or we need to open the channel first, like that’s the Phoenix solution, which is also expensive. And we are just doing on-chain transactions in the end. So there’s no way around on-chain. But with these federations, you have a new trade-off. Like it’s still custodial in a sense, but trust minimized. And you can receive funds easily.

Stephan Livera:

So one other thing is just thinking through, and maybe this is coming back to the lightning gateway idea, just thinking through the balance. Let’s say you and me and two other people are setting up a minimint and we have to balance the hot wallet versus the cold. So we’ve got our lightning gateway funds and we’ve got our cold storage. How do we manage that balance between them? Because isn’t it all also possible then that if the—maybe there’s some fancy cryptography thing or something here—but how is it that the users know that we aren’t just going fraudulent with the money and like running a lightning node that looks like it makes payments or makes some payments, but actually we’ve taken in some of the Bitcoin for ourselves.

Eric Sirion:

So that’s a really good point. There is a reason that the lightning gateway is an independent operator. Like they have to come up with additional capital. Like whatever’s in the lighting node is not counted towards the backing capital of the Federation. And so they’re an independent economic actor and whenever they receive a payment for a user and then tell the Federation, Oh, we just received some money for the user. Then the lightning gateway actually has to give E cash tokens to the Federation so the Federation can pay the user. And the other way around is if the user wants the lightning gateway to pay some invoice. Then they have to send these E-cash tokens to lightning gateway. And so lightning gateway will have some float of E-cash and can exchange it for on-chain Bitcoin if they need to. Like if all the transactions are outgoing, then eventually they will have a lot of E-cash and no funds in their channels. And so they just withdraws some Bitcoin from the Federation and open new channel. And that’s like their business decision to make, when to do this and how often to do this.

Stephan Livera:

I see. Gotcha. And so their job is essentially to manage the availability, the liquidity of the lightning aspect. And I guess what you’re saying is they would be a different person. So let’s say, it’s you, me and two other people who are running the on-chain aspect of it, the federated mint, and some other fifth person is the one running the lightning gateway. Is that the model?

Eric Sirion:

Yeah. It could be that way. Or it could be one of us because the beauty of the lightning gateway isn’t really trusted except for up-time, like, all they have to guarantee is that there are funds in the channels to go in both directions. And that they’re well connected and always operational. And so they can steal funds.

Stephan Livera:

Right. But that would also be a competitive aspect. Right. Because let’s say, okay, as an example, let’s say there’s some minimint and the guy running the lightning node, there is a doofus, right. He has no idea. And his channels aren’t balanced. He doesn’t have high up time. And then the users are getting a bad experience. So they’re like, well, this mint sucks. I’m going to go over to Eric’s mint because it’s better than Stephan’s mint because Stephan’s mint they can’t manage the lightning node, right?

Eric Sirion:

You actually wouldn’t have to switch them in. Like if I was such a great lightning node operator, which I aimed like it’s fucking hard, but if I was then I could just connect to the same Federation and provide a different lighting gateway. And if people notice that I’m providing much better service, then they can just use me. Like whenever you do lighting payment, what you do internally is you create a smart contract, and the smart contract says if someone can present the Federation with a pre image to a certain hash, then they can take the money out of the contract. And they also require a signature with a public key. And the public key essentially identifies the lighting gateways. So you can’t have two lighting gateways. And then one of them also operates a node in front of the other one. And so sees the pre image to some hash earlier and then can claim some contract. But you also bind it to lighting gateway that you expect to receive the invoice. So you can have multiple of these lighting gateways.

Stephan Livera:

So the short version is each Federation could have multiple lightning gateways.

Eric Sirion:

And it could even be permissionless.

Stephan Livera:

We could maybe think of the lightning gateways similar to how we think of LSPs lightning service providers today.

Eric Sirion:

Exactly. That’s a pretty good point. Like the only limitation is that the lightning gateway has to trust the Federation as well. So as a lightning gateway, you don’t want to connect to all federations that somehow pop up just to provide the services because you have to hold the e-cash tokens and so you have this counterpart risk. But if you know some Federation and trust them enough and think it’s profitable, then you can just connect to them, announce that you provide your services there and people can choose to use you.

Stephan Livera:

So there’s like, in some ways the Federation runners have to trust a little bit the lightning node or lightning gateway guy, and the lightning gateway guy also needs to put a little bit of trust in the Federation guys because each could sort of run off with the other guys’ money. Right?

Eric Sirion:

I wouldn’t say that the Federation has to trust the lightning gateway. The users have to to some degree because they trust them to actually make the payment because otherwise it just times out and the user can take their money back, but they didn’t make the payment. And it’s just annoying. But after your lightning gateway does this to you once, then you probably switch to another one. So that’s not a good business practice because you don’t make any money using these failed payments. So you better be operational. So the only trust relationship is the lighting gateway trusts the Federation because they hold collateral inside the Federation necessarily because they accept e-cash tokens in exchange for lighting payments. So there is some trust in that direction. Users also trust the Federation, but the Federation has to trust no one else.

Stephan Livera:

Yeah. Interesting. That’s a good point. Yeah. And because they’re holding the keys, right. They’re holding the coins. So at the end of the day they’re the ones running the service. Well also the lightning node guy, but yeah. And then, so how does all this stuff—have you thought about things like DoS attacks, like what kind of things are there around that like would a minimint have to deal with that kind of thing? Like could people try to, I don’t know, turn up and just flood the server with requests?

Eric Sirion:

Definitely. Like that’s actually a big problem because the cryptography used to generate these special signed blind e-cash tokens. That’s really slow. Like the verification of one of these tokens takes about four milliseconds and that’s a lot of time in CPU timescales. So with only like a few hundred requests per second, you could totally make the mint inoperable. Totally DoS it. So you need to have some way to limit this. But I haven’t really invested too much energy into fixing this problem because right now I imagine use of such federations to be community internal. And that also means that you can restrict access. Like for example, you have a few people that want to cooperate and use such a federated mint, they all know the same password to it. Like they can all just share the same password, that doesn’t change anything in an anonymity. Like if they’re all using the same, then you can distinguish them, but you still limit the availability to outsiders. So pure griefing attacks are pretty much ruled out that way because like inside your community there might not be an asshole that tries to just take down your Federation because they will throw themselves. And like, it doesn’t make any sense. Later we might want to implement some anti-DoS measures.

Stephan Livera:

And what about on-chain fees? Like who pays them in the model? Like I guess if I’m depositing sats, I guess I’m paying the on-chain fees for that, but then every time there’s a withdrawal, I guess the minimint operators are paying for that, right?

Eric Sirion:

Yeah. Like generally fees inside the federation are up to the Federation itself. Like they can decide to charge whatever fees they want. So for example, when it comes to on-chain transactions, then you could have a policy that the Federation periodically votes on how much withdraw requests costs the user. And they have to manage it in a way that they don’t lose money on the withdraws. They could always set it like 50% over what they’re effectively paying on-chain. So they make a little bit of profit, uh, but still allow people to make rather cheap on-chain withdrawals.

Stephan Livera:

Right. Yeah. And so then the idea could be, I mean, hypothetically people could get together and say, Hey, let’s run a minimint and it’ll be a profitable venture. Let’s run this as like a business to give privacy and scalability for our users.

Eric Sirion:

Yeah. You could probably try to do this. I’m not sure if it will be successful because you’d need a really large user base for this to make sense because users don’t like fees. So if you charge too much, then they will probably leave for someone else. And generally such big federations with a lot of users, like you probably need a few million users to make this profitable, if you have full-time people on staff. That isn’t my ideal future that I want to build. So initially there will not be a support for bigger federations really. its not something I optimized for.

Stephan Livera:

You see this as more like a community hosted node, hosted minimint idea?

Eric Sirion:

Definitely. Initially. Like ideally it will stay that way. But I also know that market forces tend to prefer bigger organizations because they can provide potentially better support or just more development power into user experience and all this stuff. So maybe we will see bigger federations one day. And one thing that was already suggested to me and in a thread about Signal—like Signal and their shitcoin—why not do it with a federated e-cash system? Like that would be pretty cool. And I kind of agree. But then again, like Signal has this philosophy of not allowing different operators. Like you can’t run your own Signal server and still connect to other Signal users. So they probably wouldn’t allow this concept where you connect to whatever Federation you want, but they would want to run their own. So that would make it rather centralized. Maybe it will do this one day, attempt this one day. Maybe not, I don’t know. It might be a net positive for Signal users in the end because then they don’t have to use some shitcoin. But ideally I wouldn’t want to see federations larger than maybe 10,000 users.

Stephan Livera:

And so what we’ve been talking about has been—obviously this is very early stage, right? This is all like a theoretical thing. When do you think this kind of idea would actually start in like a basic way, and what’s needed to get there? Do you need like community support or what are you looking for?

Eric Sirion:

Right now it’s still under heavy development. so generally people who like to develop software and rust and like Bitcoin and lightning, please check out https://github.com/fedimint/minimint. You’ll probably also put it in the show notes, I guess. And currently my plan is to have some sort of closed prototype running end of next year, like hopefully in October. because then there’s the next hackers Congress Paralelní Polis in Prague. And like last year I already bought a coffee with a really hacky setup and fake reg test and the lighting integration where the lighting node was running on main net and the lighting node was paid using reg test tokens and then paying a main net lighting invoice. So super hacky set up, but it worked and it was pretty amazing to see the first transaction go through for a real product. But next time, ideally I want to do it for real and have a running Federation that a few people can connect to. And then maybe in two or three years, we will see the first like mainstream applications of this technology. But till then there, a lot of bugs have to figured out like UX has to be completely reinvented because it’s just such a different approach having these E-cash tokens to other versions of how to interact with Bitcoin. And that needs to be a lot of research.

Stephan Livera:

Yeah. But potentially quite a promising idea in terms of scalability, because long term we know like projecting out who knows 10, 15, 20 years out. We know not every person on earth can have a UTXO, that’s just gonna blow out the UTXO set in Bitcoin. So we need ideas that relate to people being able to share coins and ideally have other trade offs around how they do that. So this is one idea, obviously the multi-party channels is another one and there are a few other ideas out there. But it’s an interesting one from a longer term perspective, at least that’s how I’m seeing it. any final thoughts there for the listeners? Why should they look into this?

Eric Sirion:

It’s a really amazing opportunity here that we have here to both give you the scalability and at the same time, make privacy the most user-friendly option. And that’s, I think what is needed because you will never get people to seek out privacy for privacy sake. But if we build this new scaling technology for Bitcoin, which will be relevant in the next like five to 10 years to include privacy by default, we might win this privacy battle and we might get most people to use private means of transaction instead of banks and KYC and surveillance.

Stephan Livera:

That’s a really good way to put it because what matters is by default. And if people can default use this, it’s easy and it’s more private, then that’s a pretty big win.

Eric Sirion:

Yeah. And it’s cheaper. That’s what will bring users in, in the end. Like it’s easy and it’s cheap and that it’s private. It’s a nice side effect. And that’s how we win.

Stephan Livera:

Fantastic. Yeah. That’s how we win. Thank you. So Eric where can people find you online? Obviously there’s a Github link and anywhere else you’d like people to find you?

Eric Sirion:

Mostly twitter.com/ericsirion. you will probably put a link for that in there too. And also on fedimint.org, I have some more resources about the general concept of federated Chaumian e-cash, and also link to a telegram group. you might link to it too, like I saw you joined yesterday. that is a great place if you’re interested in the concept, but didn’t understand something, just go there, ask about it. And like I’m there. Max Hillebrand is there. He is also quite excited and was one of my earliest supporters and yeah, someone of us will answer your questions.

Stephan Livera:

Well, I’m looking forward to seeing the idea coming to fruition and thanks for joining me, Eric.

Eric Sirion:

Yes. Thank you very much for having me on. It was a blast and see you again, see you in the citadels.

Stephan Livera:

See you in the citadels.

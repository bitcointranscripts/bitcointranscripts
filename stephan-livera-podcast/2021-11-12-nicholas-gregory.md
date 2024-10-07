---
title: Statechains and Mercury Wallet-A New Privacy Technique?
transcript_by: Stephan Livera
speakers:
  - Nicholas Gregory
date: 2021-11-12
media: https://www.youtube.com/watch?v=ZLhCnehAeeQ
---
podcast: https://stephanlivera.com/episode/320/

Stephan Livera:

Nicholas welcome to the show.

Nicholas Gregory:

Hello. Thanks for having me.

Stephan Livera:

So Nicholas, there’s discussion in the community around scaling and how do things scale, and also how do we get more privacy in the Bitcoin ecosystem? I think these are ideas that people are talking about, and I know you’re working on some stuff that’s obviously very relevant for that as well with statechains, Mercury wallet, and stuff like that. So do you want to maybe give us a bit of an overview, how you got into Bitcoin, and what your focus is?

Nicholas Gregory:

Yeah sure. I’m a software engineer by trade. I’m British but I spent some time in the US—worked for Silicon Valley—then moved back to the UK, ended up working for a few of the banks: Merrill Lynch, then JP Morgan. Then I found Bitcoin. I’m not exactly sure when, but it was posted a few times on Slashdot. I think around 2013-14, I started to get into it seriously and started looking—I was working a bit in the OTC markets and then around 2016 founded CommerceBlock. And originally we were building sidechains. So we forked the Elements code base and built our own version of Elements—which is what’s used for Liquid—to do like a more KYC’ed version and put in more requirements for what institutions were looking for. That didn’t take off as sidechains didn’t really blossom the way some people thought, and at the time we were always doing privacy stuff anyway, and it just so happened—at the time we were looking to pivot, we were looking at building maybe a CoinJoin on a sidechain—but it just so happens the way the universe is, at the same time, Ruben Somsen wrote his paper on Statechains. Although, we haven’t followed his paper obviously because his writings required a lot of things like Eltoo which wasn’t available, but we had done some research internally to maybe do something without that. We were also looking at doing a CoinJoin implementation on a sidechain at the time, and it also just happens at that time there had been some talk about CoinSwaps. I think Chris Belcher had discussed it at the Bitcoiner groups. Just merging those two together, we thought, Well, you have this technology that lets you transfer private keys privately off-chain, and CoinSwaps. Obviously we didn’t just want to build like a statechain implementation and have no use case. And clearly privacy is being used a lot in Bitcoin before we merged the two together. That would give something unique and something very different to what’s in the market at the moment. These decisions were made in the bear market. It took a lot longer than expected to go live. We were thinking it was a 6 month project—it probably took 18 months. But yeah, recently we’ve gone live. We’re very much in beta. We officially said we’re in beta about two weeks ago, but it’s getting some usage. Some guys—nothing to do with us—decided to do a Mercury torch. And that’s been interesting! They found a lot of bugs on the way and put us under pressure, but it’s been fun.

Stephan Livera:

Okay, great. So let’s talk a little bit of background then. So as you were saying, the sidechain idea, probably the most popularly known example is Blockstream’s Liquid. Now that has its own trade-offs and its own set of things to wrestle with in terms of what tools were used when we’re interacting with it. And so then this idea of statechains came along. And so just for listeners who are not familiar with the idea of statechains as invented by Ruben Somsen, and you’ve taken it in your own pathway just given the current technology—could you just give us an overview? What is a statechain?

Nicholas Gregory:

So at a very high level, it takes a Bitcoin private key, which has essentially ownership of a UTXO, and it allows me to send that to you. Now of course, the first thing you’re going to say is, Great, send me your private key. Now what about me? What happens if I remember that key? I can steal your money. Well, I can’t remember exactly the way Ruben described it, but I think he used something like adaptor signatures to basically make sure that the previous owner couldn’t keep the key. We went in a different direction. A lot of Ruben’s paper was designed around Eltoo, where[as] we basically used MPC (Multi-Party Computation), where we essentially have a key share. So when someone wants to come to our wallet, the first thing they would do is create what we call a statecoin, which is basically a coin that can be used in a statechain. And using two private keys—the clients’ and the servers’—we generate a statecoin address, and that’s where the money would be deposited to. And then when the user wants to transfer the funds, they have to cooperate with the server to basically create a transaction that would allow the coin at that point to be transferred to the new user. And we as the server, we’d make a promise—and I’ll go into how we do that—to delete the previous key share so that a previous owner could never cooperate. So we say we’re non-custodial, but in a true sense we’re probably not, but we can explain how we describe it in more detail. But for us it’s non-custodial because there isn’t a risk there where the statechain entity could work with a previous owner, but we’ve built like an open source HSM which proves that the previous key has been deleted. So in our sense, it’s not.

Stephan Livera:

I see, yeah. So maybe to put it simply: instead of me sending a Bitcoin transaction to you—and normally I sign the transaction with my private key and really in the background what’s going on is my Bitcoin software wallet is doing all this in the background and submitting that transaction onto the blockchain and therefore all the nodes recognize that—in this case it’s like we’re blinding the private key and sharing it, in a loose sense. Is that sort of what’s going on?

Nicholas Gregory:

This is all happening off-chain. So on the Bitcoin blockchain, you don’t see any transfer. The key is being sent. Now we are not censorship-resistant—clearly if the server was to go down or if we didn’t want to cooperate with your blocks—but every time you do a transfer, you have a backup transaction. So you could basically recede your funds. You could say, If the server’s not cooperating or for whatever reason were not available, you could just issue that backup transaction and your funds come back onto the Bitcoin blockchain.

Stephan Livera:

I see. Yeah. So maybe another model people might be used to thinking of is Lightning. So this idea of, If we open the channel, I at all times have what’s called a force-close transaction or a commitment transaction—a pre-signed one that we already agreed to in advance—to close out that channel and get the funds back on-chain. So I guess in the same way with the statechain idea, let’s say I’m opening a statecoin with you. If you’re now not available later on, I always have that nuclear option of just, Okay, I’m just gonna back out of our transaction, kind of like a force-close channel in Lightning.

Nicholas Gregory:

Yes. And we get compared a lot to Lightning. Obviously Lightning can do any amounts. We’re fixed, obviously, because it’s a UTXO. And we allow anybody to create any size, but we try and force people to go to like a 0.001, 0.01, 0.1, and then 1 Bitcoin. Obviously because you can only swap fixed amounts, and there’s no way to make our UTXOs divisible because they are what they are.

Stephan Livera:

Yeah. So I guess this is just naturally part of the trade-off of it. But at the same time, it also reminds me as well of even with some of the privacy wallets, like say Samourai Wallet and their Whirlpool model, they’ve got the a 100,000 sat pool, 1 million, 5 million, and 50 million sat pools. So in the same idea that you need a liquidity pool of other users who are in that pool—and in that model it’s remixing—but in this case, it’s more just that you need enough of an anonymity set of other statecoin users of that particular denomination, right? So in this example, let’s say you’ve got a 1 million sat statecoin. You need there to be enough other users of 1 million sat statecoins to give you an anonymity set. So on-chain, does it look like you’re just doing a single-signature spend in terms of the Bitcoin blockchain? Or is it just never even touching the block? Like it never even touches the blockchain except for the back-out transaction?

Nicholas Gregory:

It never touches the blockchain. So we do a test to Bitcoin: all our transactions, we use our protocol which we wrote a while ago called Mainstay, which is a bit like Peter Todd’s [single seed set 7:52]. So we do a test once a day of our work just to prove what we’ve done, but in terms of the Bitcoin blockchain, you see nothing. So if you open the wallet, you will see that these coins have a lifetime of three months, and that’s because we use a relative time lock. And this is one of the challenges we had with not having Eltoo. A previous owner, in theory, could broadcast their transaction and take your funds, but they couldn’t do that until this three month window is done. So that’s why a statechain—and with Eltoo coming out, if that ever comes out, we don’t know, that that issue would go away—but at the moment we’re stuck with that. So that’s why a statecoin has a lifecycle which we’ve set to three months. So for example, if I was to give you a statecoin, in that three month period, I couldn’t broadcast a transaction to take your funds. But after that three months, I could. And again, if I did, you still have the concept of Lightning where your wallet could be watching and see me do that. But to be absolutely safe, we say to people, don’t get to that period.

Stephan Livera:

Yeah. I was going to ask a little bit about that. So just for listeners who are unfamiliar, Eltoo is a proposed upgrade by Christian Decker, Rusty and Roasbeef. And they did a paper on this and basically it’s an upgrade to the Lightning Network that relies on what’s called ANYPREVOUT. So anyone interested check out episode 200 of my show. Go back and see that one. But back to the statecoins idea and Mercury wallet: so I installed it and I was playing around, fiddling around with it, and I saw also in the website you had a section showing this concept you were talking about, that you would need to rotate. So could you tell us a little bit what happens with that? What is that?

Nicholas Gregory:

So basically—off the start, at the moment we’ve set this to three months using a CheckSequenceVerify and we do that based on block height. So in that period of three months, if a previous owner was to broadcast a transaction—but that wouldn’t actually, be accepted by the mempool untill that three month period [elasped]. So after that three month period, a previous owner could. We’ve tried to make the wallet as user-friendly as possible, but rather than going through the details, we just say, this is expiring. If people want to go down into details—why? That’s the details. But after three months, really, there is a risk a previous owner could take it, so at that point you can just peg it back to the Bitcoin network and that’s where you pay your Bitcoin transaction fee. And that’s where we take a fee as well.

Stephan Livera:

I see, yeah. So that also gets into the conversation of, How sure are we, the user, that you guys have deleted your side of the coin? And that’s why you’re continually rotating every three months to give the user a bit more of an assurance around that, rather than them being vulnerable to “the back-out transaction” on your side, where you might theoretically claim that coin.

Nicholas Gregory:

There’s only a risk there if you’ve transferred or done a swap, which I presume—we assume people would. And at that point—so the way it works: we do have an HSM on the backend which we built and it’s open source. It’s called Lockbox. And that essentially has a key. That key itself is not a risk, but every time you create a statecoin, it generates a new key share. And one of the hardest things in computing itself is actually to prove you’ve deleted something. I can go on my computer and delete something, but we all know it still could be on a buffer or something. So what we did is we used an HSM to do a provable deletion that we’ve deleted that key. And it runs on Intel SGX. We’re licensed by Intel. We don’t have the remote attestations up yet, but that’s something we would do. But what would happen if we did not delete a previous key? In theory, a previous owner could cooperate with that key—and you know, every key is created per transaction—so it would have to be that key. At that point, there is a risk. But we’re one of the first people to open source an HSM. We are using Intel, and I know there’s risks with Intel SGX, but for us it’s a small risk. We could not use this. We could just say we’re deleting—trust us. But we painfully went through the steps of building an open-source HSM, registering with Intel to prove we’re deleting that key. And it’s not just the case where some law enforcement could, say, open up your HSM. Well at that point, if we did open up, we would have a key that generates other private keys. So they could only ask to request the funds if there were any transactions afterwards. It’s not like we actually have full custody at any point, anyway.

Stephan Livera:

I see, yeah. So just zooming out a little bit, just so people are getting a sense of like, Why are we doing all this stuff? So one, I presume it’s the scalability aspect because you don’t have to touch the chain unless you need to do the back-out transaction. So generally speaking, peopl in the “happy pathway,” you’re just not touching the chain. And so you’re able to transact with these statecoins in fixed denominations, let’s say 1 million sats, 5 million sats, et cetera. And you might get a privacy benefit out of this because of the anonymity set generated by having all these other statechain users out there who have statecoins and they’re transferring them around in fixed denominations. So that’s mostly the benefits side. And then the risks side is more like the availability. Let’s say your server goes down, then they’re going to have to do a back-out transaction and they can no longer do a statecoin transaction. And if they’re not careful and theoretically if the HSM—there’s that risk as well that you put some money into this statechain and the three month expiry happens and you’re malicious and something happens there. That’s a risk people have to think about it as well. But generally speaking, the main benefits, as we’re saying, is scalability and potentially some privacy aspects. Would you agree or disagree?

Nicholas Gregory:

Yeah. It starts to look like one of those Chaumian mint banks. So it’s not censorship-resistant, but unlike the Chaumian banks where you are relying on a multisig for custody, you can take your funds out at any time. You do have control there. Originally when we were looking at this, we were looking at the Chaumian banks, the FediMint stuff, and some of the writings of Hal Finney, and it just seemed statechains with a combination of Lightning could fill a lot of that. And it’s been interesting because recently I think there’s been more talk about Chaumian banks. The FediMint stuff got recently funded. And yeah we’re slightly different—we have the fixed denominations—there are differences, but there are similarities. And Bob McElrath wrote a really good Tweet comparing the differences that was pretty cool.

Stephan Livera:

Yeah, I see. And so then, do you see the users—their motivation—would you see it as like a privacy motivation then? So is the idea that let’s say you want to “get some more privacy on their coins” and they would kind of like run your coins through a CoinJoin? Would it be sort of like that, like they might run it through the statechain and then withdraw outwards and then treat it like that’s the fee they’re going to pay? Is that what you’re thinking? Or what’s the model there?

Nicholas Gregory:

I think the initial users would be to come here and do a kind of quick privacy, because essentially—the swaps are free because we couldn’t take a fee anyway because these are fixed UTXOs, and you can do as many swaps as you want. I mean, obviously you have this decrementing time-lock, but I think someone could go in there, do 20 swaps, and pull out all in a space of a couple of hours, which is a lot faster. It’s a different form of privacy than a CoinJoin. I mean, obviously with a CoinJoin, you take a coin, you mix it with other coins and you’re all grinded together. We’re essentially swapping history. So there’s positive and negatives about both approaches. With a CoinJoin, you’re kind of all tainted. With a CoinSwap you’re not, but someone may end up with the North Korea coins or something, but then because we prove with this attestation we do to Bitcoin, if someone was to end up with the dirty coins, they could say, Well, I participated in the CoinSwap, so I’m not dirty. But you know, we still don’t know how the Chainalysis companies will look at CoinSwaps. That’s where it gets interesting, to be honest.

Stephan Livera:

Yeah. I see. I see. And so the limitation around having set values, let’s say 1 million sats, 5 million sats or so on, how do you see people using that? Because I guess people wouldn’t really use it for commerce, right? Because they’re not necessarily going to be selling something exactly for all [of it], unless they happen to be selling something exactly for 1 million sets, right?

Nicholas Gregory:

So if you compare it to Lightning, obviously Lightning is good at what it does—micropayments—but it does need a lot of liquidity locked up in the net. We don’t need any liquidity, and I think that’s why it complements Lightning very well. We have had conversations with Lightning devs where the statechain could be an implementation of a channel factory-type thing. Where you can imagine there’s a lot of transactions there, a lot of challenges there! But in theory it could take a lot of the unnecessary volume of Lightning to do the the high transactions, the Bolt-based transactions, like in the gold world, how they trade large lots of gold as opposed to micro pieces. That’s the way to think about it. I mean, that starts to become a sidechain in its own right. For now we see people using this as maybe an easier way of doing a CoinJoin, maybe an easier way of doing privacy. And this is really just opening up the first use case for it. Because again, just building a statechain I think people would have said, That’s cool, but what do I use it for? So at least here we can say you can participate in a CoinSwap, you can get some privacy, delete/swap your history, which is what we kind of want to see in Bitcoin anyway at the moment.

Stephan Livera:

Yeah. So I think it’ll be interesting to see if there’s uptake on this idea from a privacy point of view. I could understand maybe the concern might be, Oh, I don’t want to get the “North Korea coin” or whatever in that example. So that might be what stops people from trying, but it might be something that also just kind of grows over time as an alternative. I also wanted to come back to what you were saying around ANYPREVOUT. So let’s say we did get ANYPREVOUT and we did get Eltoo. Would you then look at changing this model? Or how would things change, if at all?

Nicholas Gregory:

So we have this decrementing time-lock so you can’t do unlimited [swaps]—I can’t remember the exact numbers, but every time you do a swap, I think it goes down by 8 hours or something. We’re still tweaking that in the moment to see, but with ANYPREVOUT that would be unlimited and you could swap a million times a day. No one would care. The bottleneck would be the server. So that’s where the big change would be. So yeah, we would definitely implement ANYPREVOUT. I think that means it could be used more. I mean, look, we have very casual conversations with institutions that want to use this for settlement. And I think ANYPREVOUT would solve some of their concerns because they could do unlimited transactions throughout the day, et cetera.

Stephan Livera:

Yeah. And also, I’m curious, I remember some of the discussions—it might’ve been Ruben chatting about this idea back around the time he put that idea out—he was saying though, There might potentially be this idea of opening Lightning channels off of a statecoin. How would that work?

Nicholas Gregory:

Essentially we’re sending private keys around, so why can’t those private keys be Lightning channels? Doing this on a whiteboard, that’s very logical, but then you can imagine most of our work has been dealing with the the attack vectors of previous transactions, et cetera. Now you can imagine when you add Lightning, previous transactions being broadcasted, that makes the problem exponentially [worse], but we are planning to support Lightning hopefully in the next three months, not combining the two, but maybe paying for the statecoin with a Lightning transaction. So at the moment we take a fee when people peg out, so from a privacy point of view, you could say, Well, that coin as it’s being pegged out, as you see the 0.5% fee, [you know] that’s been used in a statecoin, but if we took a Lightning payment upfront to essentially pay for the statecoin, then you would have no taint on-chain at all. And I think Lightning there would be quite interesting. So you would come into the wallet, pay for a statecoin with a Lightning transaction, and then you use it for the three months and then it’s yours. And there’s no fee afterwards. And that would give us an opportunity to play with Lightning as well before trying to merge it in together, and that would make it even more private. So I think there’s benefits there. That’s what we’re thinking about.

Stephan Livera:

Yeah. So it’s almost like this idea of an out-of-band payment.

Nicholas Gregory:

I think someone said it to me better than maybe I describe it. It’s like a virtual Opendime. And that’s probably the best way to think of it. So you would come in with your Lightning wallet, buy the virtual Opendime USB stick, put your Bitcoin on it and that’s it—you swap it, give it to your friends, make it part of a CoinSwap, and then, you know, you snap it and that’s when you get the money.

Stephan Livera:

Then you break it open. Yeah. So I guess that’s the way to think of statecoins. And so this idea of having Lightning payments just helps take away any on-chain fingerprint of it. And it reminds me of even some of the mining pools offer transaction accelerators. So let’s say you put it in at one sat and you’re stuck. You need to put it through, you can go and make a separate out-of-band Lightning payment to them. So in the same way here, the user is just making an out-of-band payment to you to say, Hey, statechain operator, please let me use the statecoin. And the Lightning payment is just how they are getting around any on-chain fingerprint.

Nicholas Gregory:

So you can imagine that if you get five people and they all buy an Opendime, you put it in a jar, you shake it up, you pull a different one out. That’s essentially how we’re doing a CoinSwap. Is it a virtual Opendime? Maybe it’s a virtual Casacius coin, but I think that helps describe it a little bit better.

Stephan Livera:

Yeah. So I guess that’s what a statecoin is when you’re using it. So then the difference is: it’s not really like a CoinJoin round, it’s more just like you’re just joining the anonymity set of all the people who are using that same denomination size of statecoin. And none of this is even touching on-chain. So I guess that’s the other factor. So how does it work then if let’s say I’ve got a bigger than 1 million sat UTXO, but I only want to do a 1 million sat statecoin. How would that work? Like let’s say I come to you with a 10 million sat UTXO coin. Is that just basically when I do the deposit? So in Mercury wallet, as an example, I click deposit. I want to create a 1 million sat statecoin. It’s just: I send 1 million sats to that address and then that’s it, right?

Nicholas Gregory:

Yeah. So if you send the wrong amount—like we had one guy who, before, he sent the right amount but the exchange took a bit of the transaction fee and he didn’t expect it—then you’ve still got a statecoin, but then we flag it and you wouldn’t be able to use it for CoinSwap, but it’s still a valid statecoin. You just have like your own denomination of statecoin.

Stephan Livera:

In a class of his own. Okay, I’m starting to get an idea then of how that works. And so in terms of running the infrastructure around this, is it leveraging the Electrum server infrastructure as well? And what other pieces are involved? Like as an example, when I spin up my Mercury wallet, who else am I calling out to?

Nicholas Gregory:

Yeah. So I mean, since we’ve gone to Beto, people have complained sometimes the server’s slow. We realized that the server wasn’t slow because we’re using TOR under the covers. So we’re going to do a lot more to be explicit about what’s going on with TOR and provide better [service]. But yeah, a lot of what we do is with TOR. We ourselves are a TOR hidden service. So that’s probably the main processes. You connect to an Electrum server, which you can then change into your own. So if you want to run your own node, you can, but we are using Electrum. You don’t connect to our server, which when you create your statecoin, that goes from our server to our HSM, the HSM has the virtual key of the virtual statecoin or the virtual Opendime which we call it, and then you have a separate server for our swaps, which is basically a blinded server which works very much like a CoinJoin where you register, you get a token, you’re blinded, and it orchestrates swaps. At the moment we do swaps every three minutes, but that’s really because we’re in beta. We’re not going to have a lot of liquidity in the early days, but we’ll probably go for one hour slots so that people can congregate on the hour if they want to do a swap. That’d be very similar to what people do with other services—similar.

Stephan Livera:

Yeah. Would you be able to explain for us what the blinding is? Like just for people who aren’t familiar with that?

Nicholas Gregory:

Yeah. So when you’re signing a transaction with the swap server, the swaps are already blinded. It’s multi-step and sometimes it can be unreliable because of TOR. And we’re going to do more to tune that and actually explain when TOR is under attack, et cetera. But essentially you register, you get a token, and then when the members of the swap have all registered, a swap is completed. So everyone signs it blind so the server itself doesn’t know who’s who, and then you get back and you can check your coin to see if the history has changed, et cetera. So it’s very hard to know what a good anonymity set is because ultimately, having more is better, but it’s not as logical as a CoinJoin. So you just want to make sure your history is different. It’ll be interesting to see how exchanges view CoinJoins. They probably won’t know much about it for the first few years—we hope.

Stephan Livera:

Yeah, it’ll be interesting to see if exchanges and the compliance departments and so on, have any—

Nicholas Gregory:

My personal feeling in dealing with them in the past is they won’t know it for a while, but then there are people that may end up with this “North Korea coin,” but that’s why we do these attestations. So you can say, Well, I’ve used Mercury, it’s provable in the blockchain. I’m not a North Korean whatever.

Stephan Livera:

Yeah. Where they could voluntarily disclose the CoinSwap history out of their wallet, as an example. Yeah. That’s interesting stuff. I guess it’s mainly just around the privacy aspect and people who just want to maybe achieve a little bit more privacy. Also, that’s the other question I had: so there’s the concept of statechains. There’s CommerceBlock’s implementation of a statechain, and there’s Mercury wallet, which is one particular way to interact with that. Do you foresee this being something where other people might create a wallet or other people might create some other wallet and software that’s compatible with your implementation of this statechain?

Nicholas Gregory:

I mean, we wouldn’t be opposed to it because obviously everything we do is open source. We haven’t specified a protocol because a lot of this was discovery research work and it’s going to be subject to change with changes to Bitcoin. But at the moment, we could be a federation, for example. A lot of people ask me why we weren’t a federation? We couldn’t originally because of the MPC implementation. However with Schnorr, we could aggregate servers on the backend. But at the moment we’re not really looking at that. But I think there’s been demand by some people to basically have a spec with Lightning. I think that is going to be a challenge. When you start to look at integrating Lightning, there are a lot of attack vectors there and I think Lightning needs to be a bit more stable. And so do we as well, in terms of like, you have to deal with backup transactions and previous owners trying to steal funds. I mean, it’s an interesting concept because the idea of having like this statecoin where you could move from cold storage to some sort of sidechain—MetaLab to Lightning seamlessly off-chain—is great because you could see why a statecoin, you wouldn’t have to do the on-chain transaction. But then is that better than a submarine swap? I don’t know. I think there’s a lot of research that needs to be done there, but it’s great stuff. And I’ve been invited to a few Twitter Spaces to discuss it with some of the Lightning devs and Shinobi—Brian, he’s been quite looking into that stuff as well. So it’s definitely interesting and I hope it progresses. This is one of the many hopefully public and open scaling solutions of Bitcoin, as opposed to it just being all in Coinbase or Revolut or something.

Stephan Livera:

Yeah. I see. And so the idea then would be enough people get into the system of using statecoins that they don’t have to all touch the chain, and the idea is less and less people are touching the chain, so to speak. So in practice, do you think that would be like each individual user or you’re thinking of it more like different communities? Like as an example, the El Zonte Bitcoin Beach wallet: their on-chain usage is obviously reflecting for 10,000-15,000 users. Are you thinking of it kind of like that? Like statecoin users might actually be representing many, many more users?

Nicholas Gregory:

Not at the moment, but we’re open to it. Again, we wanted to get it out there and even the wallet—I mean obviously I know the wallet quite well—but people started using it in ways, which I didn’t think about and obviously there were some bugs there. But it’s opened up. A lot of people now are thinking of different ways of using statechains that I didn’t think of. And that’s probably a good way, because my team was quite involved in privacy—fast CoinSwap was logical—but now people are saying, Could you use this for NFTs or on the Lightning stuff? We don’t have that much experience in Lightning and I think using it as a channel factory for Lightning a certainly interesting.

Stephan Livera:

Yeah. And let’s talk a little bit about the statecoin torch. Was that what it was called? Tell us a little bit about what happened there?

Nicholas Gregory:

Yeah we didn’t really go live mainly because you’re kind of worried about—you know, you probably remember when Lightning went live, the Lightning devs at all times saying don’t trust us, saying don’t put much money in, you never know. And I think that was the right approach. So we didn’t want to have a day where we go live and we suddenly have a few users putting in serious money. So we literally just changed the website from test-mode to beta and then we released a video. And I think a group in Samson Mow’s Telegram community basically came up with the Mercury torch. And it’s been fun. I mean, it has stopped a few times when people have just UI issues. But I think it’s now moving again today. So essentially on Twitter, people are taking the coin and giving it, and I guess that three months is going to go down and it’s going down probably by 8 hours every time there’s a switch. So someone’s going to be in a position where they will get 0.001 Bitcoin for free. It’s fun to watch. It’s built the community a bit, got people playing with the wallet, and it’s been great for us getting real live users as opposed to people who know us or people who use Bitcoin the way we think we use it. And yeah, everyone’s got a different version of their ideal wallet. My team are Electrum users, which is maybe not the best user experience in the world, but we’re very used to that.

Stephan Livera:

Yeah. Definitely Electrum is an OG wallet. So with the privacy aspect of it, you mentioned earlier that TOR is built-in, so is it automatically running over TOR? So when you open the app image file or the Mercury wallet file, it’s already built-in with TOR?

Nicholas Gregory:

Yeah. And we’re a TOR hidden service as well, so we’re not exposed to clearnet.

Stephan Livera:

Gotcha. I see. So that’s how you’re handling the networking aspect of it. And so then it’s just about seeing whether there’s a market demand and whether there’s an anonymity set that grows in use of this over time. And so what would you be hoping to see then over the next 6-12 months?

Nicholas Gregory:

Well I would like this to be one of the privacy wallets of Bitcoin. I mean obviously there’s two. I think if you look, a lot of people still use centralized mixers, which are clearly a challenge—they’re custodial, there are huge risks. I think we probably fit in somewhere there. I think we’re non-custodial, but you can get into quite a long debate of whether we are or not. But I think we’re more non-custodial than say a federation or some of these Layer 2s. So I think we fit a niche there. I think the user experience is very simple: you deposit a coin, you click swap a few times, you pull out. So we would like to see some growth. And I think use cases will come up now that we’re live that we haven’t thought about. I mean obviously a lot of debate has come up about merging Lightning on the statechains. There had been a lot of Twitter threads on that. So maybe with a live implementation of statechains, maybe other people can look at that as opposed to us. People who might like Lightning better, because I think Lightning does have a lot of attack vectors and so does statechains. And I think merging the two would be quite a challenge right now, but I think now with both of them being live, it’s probably worth looking at again.

Stephan Livera:

Yeah, I see. And so currently as I see the statecoin possible values right now, it ranges from a hundred thousand sats to—it looks like 1 Bitcoin is the highest in terms of the current [sizes]—or at least they’re defaults. But I guess theoretically people can set their own size. It’s just that you want there to be an actual anonymity set around that, or liquidity around that.

Nicholas Gregory:

Yeah. I mean if for whatever reason we felt there was a demand we could easily increase the size and that would map out what swap sizes we’d have. So yeah, that’s just suggestions that we thought would work well.

Stephan Livera:

So if there’s all these whales, for example, who want to mix 100 coins or a 1,000 coins amongst each other, then that could be a thing as well, but it just matters on what’s their demand for privacy. And maybe for some of them they’re happy to just keep sitting on their stack and waiting until maybe in the future when they want to actually spend some or whatever.

Nicholas Gregory:

Yeah. Pretty much so.

Stephan Livera:

Okay, cool. So we spoke about the fees as well. So you said it was 0.5%. Is that the only fee involved or are there other fees? Or that’s the main one?

Nicholas Gregory:

That’s the only fee we can take, because it’s a UTXO. It would be impossible. So we potentially would look at that when we go to Lightning and change that. I mean with Lightning there would be things we could do. We could say buy one for X, buy ten for X, divide it by two—I mean that would give us more creative options. And we have to see how people are using this. Arguably people may just come in, swap, swap, swap, pull out. We don’t know if they’re going to stay long in the statechain itself. So we have to see. We are collecting metrics. We are going to have an explorer soon, which all the data we collect is published. We have databases. We’ll publish that and that’ll be viewable from explorer. So that will give us an idea of how people are using this as well.

Stephan Livera:

Yeah, I see. So it’s sort of exploratory, but the hope is that people might be interested in the privacy elements of it. And as you were saying, the idea of it is in the general or the happy path, you’re not touching the chain. And so it’s not necessarily a bad thing if people come in and swap, swap, swap, and then, well, I guess at that point they’re going on-chain when they’re backing out.

Nicholas Gregory:

Yeah. But they can come out whenever they want. I mean, there’s a key there, they can leave it for two months or depending on how they want to play with it. There’s lots of options.

Stephan Livera:

Yeah. And so then that could give them the ability to let’s say get around a timing analysis because normally in the privacy world, timing analysis is one way where people can get doxxed or can be fingerprinted. Let’s say if I’m doing it every Sunday at 10:00 AM or whatever, if I do my statecoin operation at that time, maybe that’s a way that someone could try to fingerprint me or whoever. And so this would be: you could come in, swap around as many times as you can, and then ideally before the three months expire, you would back it out then, or you would then make sure you do a rollover to go to a new CSV, right?

Nicholas Gregory:

Yeah. So the three months is our number. We could change that. I guess at the time we thought, Well if we made it six months and they weren’t to be taken out, asking people to wait 6 months for their Bitcoin is quite a long time. But again, we don’t know how many people are going to use this. Are they just going to come out, swap, swap, swap, and then three months is fine? If they stick around longer, if they start using statecoins in other ways which we hadn’t thought [of], maybe we would extend that to 6 months. I’m hoping that would be logical when you see the behavior patterns of how it’s being used, which would be available on the explorer.

Stephan Livera:

Yeah. And again, just to go a little bit further into the Lightning stuff, what would it actually look like if we were to go further? Because trying to do a channel off of that, I’m just trying to think through how that would work. Do you know? Like what’s been the result of your research into that?

Nicholas Gregory:

Do you mean like taking a Lightning payment or integrating them both?

Stephan Livera:

As in integrating them.

Nicholas Gregory:

I mean, we have had some chats. We have talked to Ruben about it. We’ve spoken to him a few times obviously. Essentially you could come in on a statecoin, but the statechain server would not know if that UTXO is a Bitcoin or a Lightning channel. So the idea would be to make that—as far as the statechain server is [concerned], it’s just a UTXO. It does not care if it’s a Lightning channel or a Bitcoin channel. And in theory they could be swapped. Now you can imagine that you’ve got 1 Bitcoin, I’ve got a 1 Bitcoin Lightning channel—I can swap it. And I think architecturally that sounds pretty cool. But then you think, Well, I’ve got a Lightning channel, I send it to you, and then I broadcast a previous transaction and then there’s a previous statechain transaction. You can see you get into a real—

Stephan Livera:

Getting really complex and messy.

Nicholas Gregory:

Yeah. But you know, I think eventually that would be possible. I think there’s growth in both ecosystems and I think that is going to be solvable. Just not really now. As I said, I spoke casually to some of the Lightning developers on that on a Twitter Space as well and they were like, Whoa—we were both like, Whoa, there’s a lot of attack [vectors]. The more you go down, the more you think about it logically, you think that this is great. You can do insane stuff, because you can essentially move from the cold storage to sidechain-type storage to Lightning seamlessly all off-chain. But then when you think of all the ways that you could be attacked, you go, Oh I don’t want to touch this.

Stephan Livera:

Yeah. Gotcha. And so then going back to just the malicious aspect of like, how would you deal with it if the statechain operator was malicious? That’s coming back to that angle of: you still have the backup transaction. And is there any sense in which you need to watch the chain for anything? Or how would that work?

Nicholas Gregory:

Well, the wallet does act like a Watchtower. So if a previous owner was to broadcast, it would. But so long as you’re in that three-month period, you have no fear, no problems. Now there is an issue: if the server was to be dishonest and switch off the HSMs. But even if a previous owner was to behave [that way] with the server you would know about it, because you have a current backup transaction which is valid, and that’s your proof that the Mercury server has been malicious. And you know, we’re not anonymous—we’re a team. The company knows who we are. People know who we are. So they would know that we’ve behaved in a dishonest way. But again, someone would have to break our remote attestations, which is broadcast to Intel. So there’s a lot of things that would have to go wrong. And people seem to trust a lot of closed source HSMs, and our HSM is public—it’s called Lockbox. It was something that we thought would take a couple of months to build, it ended up taking nine months. Building in the [Intel] SGX environment was a lot more complicated than we thought, but we think it’s worth it because we could obviously operate without an open-source HSM and you’d have to trust us and you’d have to say, Look, we’re nice guys, trust us. Now we don’t have to say that. We say, Well, no, we’ve got a complex piece of software which is public, open source, and anyone could use it. And that proves that we’ve deleted all these key shares and the proof goes to Intel. And yeah we didn’t even seek a license with Intel. They came to us. So I guess being a big company they’ve probably got guys scanning GitHub repos and they saw we were building an open source SGX kind of like HSM implementation, which is interesting because a lot of people said that you couldn’t build MPC in an HSM because of the complexity. But again, it was something that should have taken a few weeks, but it was probably nine months of engineering. Maybe that alone will become a project by itself, because I do think there’s space for more research in HSMs so that people feel more secure with the way servers are behaving.

Stephan Livera:

Cool. Okay, great. I think those are probably the main questions I had in terms of how it works and things. So for people out there who want to play around with it, do you have any tips for them or anything to keep in mind when they are using it?

Nicholas Gregory:

Yeah. Just go to mercurywallet.com. Obviously you’re an old-time Bitcoiner: people always say, Not your keys, not your Bitcoin. We’re now saying, Not your keys, still your Bitcoin. So yeah, the UI is designed for normies, but it is a different concept of using it. I’d say download the wallet, find the Mercury torch on Twitter, get yourself a free coin and have a play. It’s a different way of thinking. But I think that hopefully this will open up some creativity around what you can do with Bitcoin Layer 2s. I mean, outside of sidechains you’ve got Lightning and you’ve got statecoins. So there’s not much options you have outside of the centralized services. I’m hoping this will make people think a bit differently.

Stephan Livera:

Gotcha. Yeah, excellent. All right. Well let’s leave that there. And where can listeners find you online as well if they want to keep up with you?

Nicholas Gregory:

Yeah. I’m on Twitter at @gregory_nico or @mercury_wallet. We’re slowly growing a presence there but we’ve been doing daily releases now. We’re in production. We’re doing weekly releases. Lots of things are going to start happening and hopefully you’ll see the block explorer come out in a few weeks and then hopefully next year you’ll start seeing what we can do in Lightning.

Stephan Livera:

Fantastic. Well, thank you for joining me, Nicholas.

Nicholas Gregory:

Thanks for having me.

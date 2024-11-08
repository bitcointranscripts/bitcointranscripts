---
title: Lightning Network Security Panel
transcript_by: Bryan Bishop
tags:
  - security
  - lightning
speakers:
  - Olaoluwa Osuntokun
  - Justin Camarena
  - Matt Corallo
  - Michael Folkson
media: https://www.youtube.com/watch?v=orWfkdDWQzo
---
<https://twitter.com/kanzure/status/1137758233865703424>

## Introduction

MF: I will start by thanking Kevin and Lea and the organizers. It's been an awesome event. Thanks also to the sponsors. Without their assistance we couldn't have had the event. I'd also like to make some plugs before we start the conversation. One, I run the London Bitcoin developers group. If you're ever in London or interested in speaking, please look up London Bitcoin Devs on Twitter or Meetup. There's a bunch of really good Bitcoin technical meetups being set up. There's one in Boston, there's a bunch all around the world being set up so check those out. Also, if you're interested in setting up a meetup please contact me and I would be happy to help. I'd also like to do a quick plug to  John Newbery who is doing some amazing work in terms of encouraging people to contribute to Bitcoin Core. If you haven't previously contributed to Bitcoin Core and you're interested, there's an IRC group every Wednesday where jnewbery will answer your questions and help onboard you to start making your first contributions to Bitcoin Core. That's a really awesome initiative. So let's start. We'll do introductions. Introduce yourself and the Lightning project that you're working on.

OO: My name is Laolu or roasbeef. I am co-founder and CTO at Lightning Labs. I work on lnd. I’ve worked on Lightning for three or so years on design, protocol, implementation, other high level stuff too.

JC: My name is Justin. I’m a software engineer at Bitrefill. We were the first one to offer Lightning in merchant e-commerce when it launched.

MC: My name is Matt Corallo. I’ve been doing Bitcoin protocol design work since 2012ish. I also have a Lightning library designed to fill the niche of existing wallets who want to integrate Lightning in an easy way. Existing Bitcoin wallets that have all of the onchain state handling already implemented and don’t want to duplicate it. They can take this library that does the Lightning specific work for them but they still get to use the stuff they already have and don’t have to download the chain twice or anything like that.

MF: As we start the discussion it is worth considering that we’re still very early in terms of Lightning development. It is a bit harsh to judge Lightning by the same yardsticks that we would Bitcoin. Lightning is what 3 or 4 years old?

OO: It's like 1 year old on mainnet.

MF: It is very much still training wheels stage but we will explore the security of the Lighting Network as a whole and the individual implementations.

## lnd

MF: Laolu, what’s your view of the security of lnd as a Lightning implementation in its current state today?

OO: It's pretty good, getting better every day. We have a lot of users giving us feedback. Every now and then we discover things even on the protocol level as far as different ways of probing or holes we didn’t know about before. One thing we’ve really been focusing on in the past year or so has been safety measures with lnd. For example the seed backup, this thing called SCP - static channel backups, we have watchtowers now. We're really focusing on making sure things are secure and robust such that people like exchanges and whoever else feel more confident in the software so that they can use it in the future for their needs. It is definitely getting a lot better.

MF: Did you get that Bryan? It's a miracle how he does it. Justin, you've been building on top of lnd. What has been your experience of building on top of lnd? We’ll try to focus on the challenges. Obviously lnd offers so much out of the gate but let’s try to focus on some of the challenges of building on top of lnd?

JC: I've been testing out lnd since before I was hired at Bitrefill. I’ve had experience working with it. I would say we're aware of the risks of using it. One of the challenges was keeping all of our money in hot wallets online. Basically users pay us and we have a channel balance that we cannot get rid of or close. We can close the channels which we’ve done but it has been a growing hot wallet due to the amount of users. API wise, I would say it has been getting better and better. A lot of things that we didn’t know would be a problem we've learned by testing out the software on mainnet with real users.

MC: What problems?

JC: Originally we liked Lightning because we wanted to get away from all of the onchain problems. For example as a merchant if you have incoming payments from users around the world, you have many of them sending partial payments or overpaying or sending you half a Bitcoin by accident, it is really scary. With Lightning, we hoped it would make this experience better so that incoming payments wouldn't be underpaid. I think overpayment is a feature and it doesn't really happen that often except with c-lightning. That’s one reason.

## rust-lightning

MF: Matt, you've taken a very different approach with rust-lightning. It's not trying to do the exact same thing that lnd is doing. Early on you’ve been trying to work out what niche you can operate in. When you observe lnd, being a prolific Bitcoin Core contributor, what are your thoughts on how it has evolved? Would you have done things differently and any lessons in terms of building rust-lightning?

MC: There's two parts to that question. The first just being, obviously I think they have been doing great work, c-lightning has done great work, ACINQ/eclair have done great work among others. There's not really any help in me trying to compete with that, there’s just redundant effort, it is just a waste of everyone’s time. And so as you mentioned, I’m trying to find a niche that is useful for people who want to for example run their entire Lightning wallet on a machine that is only connected to the world over a serial cable. So no internet access required, you could build something reasonably well. Obviously you have to have pseudo-internet access. You have to be able to pass messages to your peers but it doesn’t have to be over an IP stack. You don’t have to expose a full TCP/IP implementation over your critical machine that is holding all your private keys. You can do more flexible things around the ways you do watchtowers. You might send encoded watchtower blobs to multiple watchtowers and get those watchtowers to agree that they have seen this update before you move on, so you can distribute your security model a little bit there but that's obviously a lot more work on the user’s end, that’s a development user not an average user. It is a completely different niche. lnd is not targeting a hardcore developer who wants to integrate it into their app and do a bunch of work themselves and micromanage exactly how data is stored and all those things. It does great in its niche. It is a separate niche to try to say “OK you want to micromanage exactly how this works. You want to have some higher security arguments about what’s going on.” The other angle that rust-lightning is taking is because of that library we've been able to do really cool work with automated fuzzing and trying to analyze the state machines in automated fuzz testing style ways where you throw garbage at the state machine and see if it is able to maintain state with the peer and do all kind of weird things with your messages in ways that is much harder to test for other implementations. That's been fun and interesting. Lightning is still really early. I’m sure everything else will get there eventually. At the same time I don't have to worry about users so I don’t have support tickets, I don’t have a lot of people using it yet which gives me free time to work on other things.

MF: One of the use cases Matt is looking at is existing Bitcoin wallets integrating Lightning into their existing wallets. Is that a possibility with lnd? Do you think rust-lightning is better placed for existing Bitcoin wallets?

OO: With rust-lightning, it's designed from the ground-up for that purpose. It's possible with lnd as well but with lnd there’s a few fundamental abstractions: signing, getting blocks, getting notifications for confirmations, things like that. You can abstract those things out, but maybe it would require you to have them be different processes perhaps. Maybe the signer calls another process that’s not within the lnd process itself. It is still pretty modular but it is not designed really to be integrated into other wallets. You have lnd as the full spec wallet itself. It does a number of things additionally. You can get keys from it, there’s arbitrary signing. It is meant to be more batteries included. Even with that we see people build wallets on top of lnd. There's probably more mobile wallets built on lnd now than other wallets than there were before because it gives you an easy jump start. If you did have a very specific use case for rust-lightning you could more carefully architect what you’re doing with your wallet. With lnd you inherit many of our design decisions whilst outside you can do things specifically for your exact use case. One is completely batteries included, you accept it, here’s the RPC, here’s everything that we have. The other one you can have the particular pieces, maybe reimplement some parts yourself, you can mix and match. A choose your own Lightning node type of thing where you have all these pieces that you plug in together. Different approaches which I think are both valid and it is cool that we’re working on them at the same time.

MF: I feel as if I should always give Bryan at least 3 seconds.

BB: No, we're good.

## Multiple lightning implementations and pace of development

MF: Justin, so building on top of a Lightning implementation. You said something about c-lightning earlier. Are you monitoring the other implementations or are you focused on providing services on top of just one?

JC: Initially when I started implementing it for Bitrefill it was before it went on mainnet, any of the implementations. The one that was ahead at the time was lnd so I went with this first. I didn't bother looking at the other implementations. I took some looks but the APIs weren’t far enough and they weren’t ready for mainnet. So initially we went with lnd. What I learned from running lnd after a few months or maybe even years at this point, was all the bugs that needed to be changed on the API level. It was really useful to have the lnd team on Slack where I could message them and say “Hey this is an issue.” I’d file it and they’d fix it. That’s generally been the style that I have been working with lnd.

MF: Matt, obviously Lightning is a layer 2 system rather than a layer 1. That means there can be a faster pace of development even though you don't necessarily want to go completely crazy and not have sufficient review and make sure users aren’t losing their funds. What insights do you have from a Bitcoin Core perspective? Do you think Lightning is going too fast? Do you think there should be more review? Do you think an implementation like lnd is sufficiently stable?

MC: I don't have as much experience running lnd as Justin does to answer the specific stability question. But obviously, all of the layer 2 systems that we have today and all the proposals we have for reasonably sane layer 2 systems have this property that they have taken the censorship resistance assumption that we have in standard Bitcoin land that is a weak assumption about usability. If you lose censorship resistance temporarily or you lose censorship resistance period, this is a usability issue but you don't necessarily lose funds. All of a sudden this has been hoisted to a fundamental security assumption where if you can't get a transaction onto the chain quickly enough then you lose money. That’s fundamentally the security model of Lightning and really all other layer 2 systems that have been proposed that are at least not super centralized. That’s a different world and is still something… the biggest question about Lightning security is more in that domain. Bitcoin is still an experiment and we don't know how decentralization is going to work out. We don’t know how censorship resistance is going to work out in the long run. So while it's important for scalability that we look at these things and try to utilize them in building these second layer systems, we don't really have any better ideas, it's still kind of a big open question in the long run. In terms of the pace of Lightning development, I think the protocol is actually moving not that quickly. It is moving obviously much quicker than Bitcoin consensus rules moving but it is still moving at a reasonable pace when you compare it to other more flexible protocols, other protocols that have lots of users but also can be changed freely because you have upgradeability on a per connection basis, on a per peer basis. Lightning, I would say is moving at a reasonable pace in that context. It is maybe a comparable pace to the P2P logic in Bitcoin Core where new protocol messages, new optimizations are added. There is a similar pace there as you see in Lightning just as you would expect because they have similar constraints. You just have to negotiate whatever the options are with your peer and you use that with that peer but it doesn't have to be the same with all your peers. Obviously you see fast paced development in the clients themselves just because they are new and users are flooding in, high pace of adoption so you see a lot of bug fixes, a lot of tweaks, a lot of fast development but that is to be expected for relatively new software projects.

OO: Definitely. I feel like Lightning has the possibility to be a little more nimble than Bitcoin development. There's probably three or four classes of different updates. There’s something called  the end-to-end principle in network technologies where you add new features at the endpoints and not really modify the actual core of the network itself. For example people talk about these features like sending a payment to a node without an invoice, I call it key-send now, that can be done on Lightning today without updating any of the other intermediate nodes. If only the sender and the receiver want to do a thing they can do that. I think this is pretty cool because it allows for a lot more flexibility from the developer side of things. The main developers are very excited about that because all of a sudden now they can have an idea and they can implement it as long as they know the client and the receiver have this new feature. The ability to be a little more agile there is exciting because we can take new ideas and implement them really quickly unlike more fundamental things on the network. An example of a more rigorous upgrade to the network is moving to discrete log based HTLCs versus the hash based one. The current hash based one has an issue because it has the same identifier in the entire route, I think maybe this was pointed out in an earlier talk, then you can identify the route if you have two intermediate nodes. The discrete log one would require more of a hard fork of the network in a sense. You would require the network to have that new upgrade. Maybe there would be a period where you have both of them initially in the network and then you switch to the other one. I think it is pretty cool we have a bunch of ways we can upgrade the network in the future. We can do that at a quicker pace but because it is decentralized we can’t flip a button and upgrade everybody. It is still an opt-in thing. If people don’t want an upgrade they can just sit there and don’t accept it. But hopefully the security updates and privacy updates are big improvements with the scalability of the system itself.

MF: Obviously the flip side to that fast paced development is that you can really get new features out the door quickly and see what works and what doesn’t. We’re focusing on security today but there’s obviously that positive flip side to that fast paced development process. Do we want to discuss Rust versus Go as languages? We haven’t had too much controversy this weekend.

MC: I don't know if I'm awake enough for religious debates right now.

OO: I win? Go wins? Ok we’re cool. Let’s move on.

MF: Ok, you heard it here first. Go is the better language for Lightning than Rust.

## Deploying and using experimental features or other upgrades

JC: Back to the previous discussion. I have taken a look at all the other implementations. Not rust-lightning but that’s not really a node together right now. But I have for eclair for example. I’ve been testing and experimenting with new features that lnd does not support. That’s not to criticize lnd, it is more to try both of them and experiment. One of the things we did was with turbo channels. This is a way in a custodial context where we’re able to sell a pre-funded channel to a user and if their wallet supports it they’re able to use Lightning instantly when the transaction is unconfirmed. This doesn’t have to modify the network at all, it just between me and the other node. Another example would be raising the channel size limit. What we did is we removed the limit and any other node that also has these rules where you can fund a bigger channel can also do this with us. ACINQ did this with us. They opened a 1 Bitcoin channel and I think a 2 Bitcoin one.

OO: For those that don’t know the current limit on Lightning today is 0.16 BTC. It is a training wheel type of thing. You can lift it if you want but it is not really rolled out yet.

MF: That's the individual implementations kind of covered. Let’s move onto cross-implementation and looking at it from a network level in terms of multiple implementations. I’m aware Christian Decker has a GitHub repo testing compatibility between implementations. Do any of you have views on the state of the Lightning Network in terms of cross-implementations?

OO: Those tests aren't fully encompassing, it is a very basic thing. That was something we had initially to ensure we can actually send payments over channels with each other. Since then we’ve discovered a number of little quirks. We work pretty closely with developers at c-lightning and eclair. We always have bug reports between us. Many times we’re testing lnd to lnd and if everything works our job is done. But then maybe there is some worry with eclair or c-lightning. That’s something we’re doing a lot more work on. The cool thing about having these sorts of tests is that a new implementation called ptarmigan, based in Japan, they were able to use those tests to at least have some rough certainty that things were partially compatible. We could definitely be doing a lot more in terms of fuzz testing like Matt was saying. It is pretty good to ensure your implementation can do both the happy path and it won’t crash if it gets some random data or something like that. We should invest a little bit more in the future on. It is very important that it is not just lnd to lnd, it is a big network where everyone needs to be able to interoperate properly. Otherwise you have these segments which aren’t connected to anything at all which we don’t really want.

MC: Fuzz testing isn't just for crashing. rust-lightning has been doing protocol level fuzz testing where the input from the fuzzer, you use that as a list of commands to send payments, connect nodes, disconnect nodes, reorder messages, things you would only see if you had very strange internet behavior where you have multipath. This exists, it's not common but it is also entirely possible. To really poke at all of these edge cases so you can really test the state machine and really test the behavior of the nodes. Do you read over a buffer when you’re deserialize something, do you over allocate memory things something simple like that. I'd really like to integrate other nodes into that, but it's really hard to take free standing daemons that aren't libraries. Maybe I’ll spend some more time with eclair trying to do that but I haven’t got round to it yet.

JC: In my experience, testing out the software, running a node on mainnet and having hundreds of channels and some private channels. Initially when all the implementations launched on mainnet they were constantly having issues with each other. They wouldn’t connect, they wouldn’t stay connected, channels would get force closed. It was an endless stream of reporting issues, sharing the bug logs with all of the teams. Lately there still have been issues here and there but it has been getting better.

MF: Obviously we've had the discussion for years on whether multiple implementations are good on Bitcoin. On Lightning it is interesting because there are some parallels but there are some things that are just completely different.

MC: Worst case, you go to chain and no one loses any money. With consensus, the worst case is you fall out of consensus and everyone loses lots of money.

OO: Yeah the risks are pretty different. If things mess up you can just close the channel versus ultimately being on a different chain so we can take a little more risk perhaps knowing we have the base chain to fall back to.

## Watchtowers and static channel backups

MF: Let's move on to end user security. I suppose the big two developments for end user security would be watchtowers and static channel backups. Anybody want to talk about the current state and what the ideal future state would be for watchtowers and static channel backups?

OO: Lightning wallets are a little more difficult than regular wallets because you have additional state. With a regular wallet you just have your seed, you can input that and do a rescan of the UTXOs. Whilst with Lightning wallets you have that particular state of your channel. The difficulty there is that if your state is out of date you can potentially have an accidental breach that can cause a loss of funds. We developed this thing called a SCB, a static channel backup. It is not a snapshot of every single state, it is the initial information necessary to close out your channel in the case that something goes wrong. We try to make it as foolproof as possible. You can try to have an up to date state and hope it is the correct one but that can potentially be risky if you don’t have a strong system on the backend. Instead it is something that allows you to reconstruct the channel and then go to the other party and close it out. Now you have your seed in this special file. Typically the file only gets updated when you open and close a channel. It can be on your iCloud maybe. The other thing is that between users, their channels are pretty stable because they want to keep the channel open for a long time. Closing a channel is a pretty bad thing to do. Anytime a user has an issue, “Do I have to close my channels?”. I’m like “Yeah sorry” and they’re like “Ah man I want to keep it open.” With watchtowers, they were developed a bit of time ago, Tadge had earlier versions back in the day. Conner and I have been working on this new version which will be in lnd 0.7. It is still an early version. Having that out there is pretty good for incentives. It is a deterrent against any funny business. There could be a tower out there, there could be like five of them, you don’t really know what’s out there. It adds an additional level of deterrence. We’ve seen some breaches onchain maybe due to accidents or people testing it out. I haven’t really seen a large scale targeted breach or anything like that yet. Now they have this nuclear weapon sitting on the back maybe it will be less likely to occur in the future.

MC: It is also still relatively small amounts of money in Lightning. It is still much too early to start putting lots and lots of money in it. There are still bugs that people see, nodes that crash not to mention questions about the specs not being quite there in terms of fee estimation looking into the future. If someone actually breaches, it can be hard to punish them in the current design. These are all resolvable issues. It's still early so you wouldn't expect to see large scale exploitation. There’s some money in it but you’re not going to walk away with a million dollars.

OO: We have a lot of code that we have tested and really evaluated but ideally it never executes. It is there as a deterrence. “Hey we have the code don't do anything funny.” It is good to have that code there and I can sleep at night because I know we tested it and it worked in the wild so we can catch breaches and people cheating which is definitely good.

## Payment channel limits

MF: Do you think the talk of increasing those limits on payment channels with wumbology is a little bit premature?

OO: Do I think it's premature? My personal view is that the supply of capital in the network outstrips the demand for it. I think we have a good amount of money on it. I feel like it probably makes sense today for companies that are doing very frequent transactions between each other. They would be better off. The other place that it would make sense in the future would be for exchanges but we’re not quite ready yet. People can do it today because there’s no global consensus. If they open a channel no one can do anything about it.

JC: Right now, it works. Nodes will route through it, legacy clients will route through it, they’ll pay us just fine. It hasn’t been an issue. In the context of B2B it makes sense to raise the limits. It makes no practical difference for us. Eclair has been opening many channels. Instead of having to broadcast five transactions to open a channel with us they can just broadcast one on Bitcoin. There are many nodes on the network that already have 1 Bitcoin worth of channels to us, it could just be one.

MC: Especially when you really know your counterparty, if they really do something and try to steal a bunch of money, you can sue them. There is a fallback.

MF: Have you looked at watchtowers at Bitrefill? Any plans to offer a watchtower?

JC: I don't think any of them are production ready. I think lnd has a pull request. I sleep better at night now that we have static channel backups. Previously it was just a reckless running of a hot wallet. If you have any data corruption and you fall back to an old state I lose all of the money. At this point it is probably not something we want to lose.

## Lightning hardware wallets

MF: Stepan Snigirev talked about hardware wallets on Lightning earlier. It is a difficult problem. I don’t know if you’ve spent much time looking at how hardware wallets would integrate with lnd. Perhaps it is a little early for rust-lightning I don’t know, inform me.

OO: That was a great presentation earlier. I also have many similar ideas. The main difference between a hardware wallet in a Lightning context versus a regular hardware wallet is that there is a lot of opportunity to add more state to the wallet to make it more intelligent. For example you can do something like the wallet only signs when it knows it to be forwards rather than outgoing payments. Maybe it doesn’t sign duplicate payments. If you can add a lot more state into the hardware wallet itself you can add a lot more security. If you’re an exchange you can add security to ensure that any outgoing payment must be a user initiated withdrawal on the exchange, otherwise reject it. There are a number of interesting things as far as topology when you’re running your node. We call it a gateway node structure. You have the main node that’s accessing public channels on the network and you have another node that’s behind it that has maybe more funds. That can allow you to really control what is going on. You can shut that one channel to ensure sure it is blocked off. Hardware wallets are definitely interesting. We don’t really have plans yet explicitly to build them out but it is very cool research. Once you have that there, you have towers, you have backups, you also have hot replication as well. It is a pretty interesting state to be in as far as the security and safety of the system. I think it is inevitable when we have much larger channels than we do right now. Right now maybe we have like a few thousand dollars in a channel but eventually it could be millions of dollars. We definitely want the key security to be in hardware at that point and segregated from the main daemon.

MC: Supporting hardware wallets isn’t an explicit goal of rust-lightning but it is a very different model from the c-lightning hsmd and a lot of the existing research. The model is tricky. There are a lot of issues with just trying to enforce the rules on the hardware wallet end against the Lightning implementation running on the machine. If for example you have two different channels with different dust limits which is completely acceptable, completely realistic if you have different counterparties who have different fee rate estimates. All of a sudden you might receive payments right at the dust limit, forward them and then you can’t enforce these rules anymore. You could get your money drained if you disable these rules on the hardware wallet. Or you have questions about if you broadcast a transaction because you think something is about to timeout but it is just because you haven’t received the latest block. All of a sudden the machine upstream of your hardware wallet that is compromised caused you to lose money. The rust-lightning approach is a little different. Instead, the idea is to move all of the complexity onto the hardware wallet. This is not feasible with today's hardware wallets which run with absolutely tiny CPUs and 128KB of memory or something like that. Instead it says put 5 MB of memory in your hardware wallet, run the full Lightning daemon there and pass the actual messages that you want to send to peers off onto the computer which then sends them upstream. You do routing and other similar things on the actual computer, obviously you don't keep the routing table on the hardware wallet or anything like that. Then for watchtowers, which of course you have to have to have security, you have the hardware wallet have a list of trusted watchtowers which are remote third parties and it sends watchtower updates to them via your potentially compromised machine but it waits for the watchtower to provide a signature saying “Yes I’ve received your update” before it moves forward with the channel. It is a very different model in the sense that you don’t get the benefit that some of the existing designs try to achieve where they have effectively two nodes that have a lot of logic about Lightning enforcing rules against each other but you still get the benefit of today’s hardware wallets which is the keys are on a machine that only connects via a hopefully simpler protocol than a full TCP/IP stack, doesn’t run a web browser, all of the crap that you have today with many Bitcoin wallets. It is a little bit of a different model but I think there is at least some potential there. Of course it doesn’t work with today’s hardware wallets, you’d have to upgrade the CPU on them.

OO: The memory is important too. They’d be a lot beefier than like a Ledger as we have today.

MC: Right. It does still however make sense in a server context where you might say “We’re going to buy a server, we’re going to run a Lightning node on that and we’re only going to connect to the outside world via a serial connection. You can have a lot better assurance of everything that can come in and out of the machine than running a full Linux stack that is exposed to any machine that can connect to it on the internet. You can be a lot more careful about that.

MF: At a high level, the biggest challenge is that if you're using a hardware wallet onchain you just have to monitor the chain when you're submitting a transaction. With Lightning, if you’re a routing node and you’ve got a hardware wallet, you’re having to monitor the chain potentially 24/7.

MC: Not necessarily monitoring the chain but you still have to be online if you want to route. Even if you’re not monitoring the chain you still have to be online to route. It is a very different model.

## Automatic wallets

OO: The biggest difference onchain is that every single transaction you’re going to explicitly approve, you’re going to click OK. With a Lightning wallet it is ideally going to be making automated decisions for you. We had a similar talk on automated wallets. You have to be very careful about that. If it can steal all your money it is not really doing anything, it is security theater. It needs to have verification to ensure that what it’s doing is correct and could be tricky as far as implementation to make sure it is secure.

MF: Any thoughts on hardware wallets at Bitrefill?

JC: I recommend exchanges to do this at some point. In a user context you don’t have to be online all the time. Your node becomes a watchtower when you unplug your device or something. There are different models.

MF: Let's talk about the most controversial topic and then we’ll open up to questions if we’ve got time. Onchain fees.

OO: Yeah.

## Onchain fees

MF: I’ve got a question. I don’t know if he wanted to get credit for the question but I’ll read it as is. As a security guarantee Lightning Network requires that a channel can be closed onchain at any time. So in opening a channel for a payment in which the onchain fee level is significant in relation to the payment, is one not foregoing that guarantee altogether?

OO: That comes up a lot. My response to that is that’s a thing for any output in general. You’re not going to make an output onchain that’s going to be more costly to actually remove it yourself. In Lightning depending on the context there’s different ways you can deal with those fees. For example we were talking about the breach case. In the breach case because you have all the money of the counterparty that is cheating you, you can bleed their funds away into the fee for your justice transaction. As a result you can do a thing where everything he has goes to the miners but I am made whole. But you're right, fees are definitely very important. Right now the current Lightning protocol has a limitation where the fees are pre-committed to for every single commitment transaction which means you’re locked into that 5 satoshis per byte or whatever else. We’re doing something in the future where you can add minimum fees to the closing transaction but then later on update that fee via child-pays-for-payment to ensure that you get into the chain. If you are offline for a long time and you have a very low fee rate you may have difficulty getting in because you can’t update the fee rate in the commitment transaction as of right now. It is something that we’re looking to fix in the future which may require some changes to the way RBF works today in bitcoind and other implementations.

MC: I blame sdaftuar for not finishing package relay yet.

OO: Is he here?

MC: I don't know if he’s here. I blame him either way.

JC: This is also an issue for us. We offer a channel opening service. Since we are the initiator we have to pay the fee. One of the things we have to cost in is the force-close fee. If you sell a channel for two dollars and the closing fee is $5 because the fees are high that day we have to pay that. One of the reasons why our fees for our channel opening service is so high is that the current implementation of channels have a fixed fee. In the new implementation of 1.1 the fee is static but you can bump it.

OO: Fees are definitely important. In lnd you’ll have the ability to anchor down the funding transaction. You could maybe have a very low satoshi per byte fee on your funding transaction but later on increase that slowly up. It is definitely important that all Lightning implementations are very aware of fees. The dumbest thing you can do is use the fee from the estimator and that’s it. The better strategy is to low-ball and use RBF to slowly get in when you need to. You don’t need to pay 100 satoshis per byte, that’s wasteful. That keeps fees up and messes with other fee estimators as well. We’ve been doing a lot of work in lnd to make it more fee aware and give the users control. If you’re closing a channel, it may not need to be immediate. Maybe you can do it in two days with a very low fee. We try to make sure that information is pushed to the end user and the API. We take many requests in that area.

MC: That's another great thing about lightning in general. Because there’s a lot of transactions that you make in Lightning, especially opening channels where you don't really care if it confirms soon. You can actually enforce real security and wait a day or longer for the transaction to confirm. Today taking transactions at 3 confs, 6 confs, 12 confs is really risky. Hash rate is not in any material way secure and taking transactions in a timeframe that is shorter than the amount of time that people can realistically respond to an issue, identify the cause and fix the issue which is definitely not two hours. You’re introducing a lot of risk. The nice thing about Lightning and other layer 2 solutions is you can say “I’m going to wait a day for this”. Then I’m really sure this is not going to be re-orged out or have any problems.

## Future improvements and scalability

MF: There is some really exciting work coming down the pipeline in terms of signature aggregation and potentially opening and closing multiple channels in a single transaction. But I suppose the concern always is if Lightning was an absolute amazing success, is that going to price certain use cases of the Lightning Network or will we need block weight increases? That’s probably a discussion for another day.

MC: We also just don't know. Lightning clearly improves the ability to fit more effective transactions on the chain. It clearly improves the ability to function and send smaller payments given a certain fee rate. How much we don’t know. We don’t know if Lightning results in scaling Bitcoin 10x higher than it was, probably at least. Or 1000x higher. It is probably not 10,000x higher. We don’t really know what the number is. We need to deploy it, we need users, we need to see how things grow. We don’t know how far Bitcoin scales, we don’t know what fee rates will be in five years. These are all huge open questions about the Bitcoin system in general, they’re not necessarily even specific to Lightning.

MF: Finally, Conner from Lightning Labs has a question for you Laolu. Is Raiden more scalable than Lightning?

OO: What? No. They do weird things like store addresses of nodes in the chain and using the P2P network for gossip. So I'd say no.

MF: Hopefully that makes you feel a bit more comfortable Conner about working on Lightning rather than Raiden.

OO: They are also much earlier. They have maybe 40 channels or something like that and we have thousands, very different scale.

MF: Do we have time for questions?

## Q&A

Q - If there’s a breach remedy transaction, I saw a tweet once many months ago where it was a mistake or something. Do we have any statistics on how many channels were closed in that way?

OO: Yeah someone ran a script at the SF Bitcoin Devs Socratic meetup. I can’t remember the exact details but you can easily run a script onchain because the way the script is, you can see when it is a regular settle and when it is a breach and then do analysis on that. Every now and then people try to make sure it works. They breach themselves to get assurance in the software itself but you can run scripts to know. I don’t know any numbers off the top of my head.

JC: In my experience I’ve had like five or six breaches. Probably most of them the users accidentally backing up an older state. I don’t think we’ve had any breaches for months.

OO: Hopefully it is zero.

Q - I would like to have you comment on the autopilot and what is expected to change in that. Going back to the previous presentation as well, is a reputation system necessary to be built for a more accurate and useful autopilot feature?

OO: Are you saying when it is going to be more useful? What is the question?

Q - How much improvement do we expect in the autopilot in the near future?

OO: I would say a lot. There’s a number of things we’re doing The current version is a very basic thing trying to make the network a scale-freeish topology. We’re taking a two pronged approach. Firstly, using graph metrics like liquidity and heuristics on the graph level you can combine those to have catered clusters for different use cases. For example, a client node, a routing node, a merchant server. Another thing we’re doing is active network analysis on the network nodes themselves. A node can look good with lots of channels but it could be managed very poorly. We’re going to combine those two sources of data, the real-time data from all the nodes that are being routed through and the onchain data to have a better picture of what’s going on. Pretty soon we’ll have a mobile app coming out that combines the two of those together. We were testing it, I bought some beers last night. It is definitely a better selection than picking the biggest node on the map which doesn’t really work out. It is definitely a big thing for user onboarding. At the same time you may want to pick your channel yourself, maybe it is your own node or your business or whatever else. We’ll definitely combine those two.

Q - Chris Belcher mentioned in his presentation yesterday about probing. You would connect to one node and you would make fake payments to other nodes. It is kind of a feature if you want to know what the capacity is and how good the routing is. It is also a great way to know in real time what all the balances are. What are your thoughts about that? Should it be impossible to probe? Then you can’t do good routing. Or for now leave the privacy vulnerability in there?

MC: I think we need research. There’s not any real good research. You can’t disable probing globally because probing looks like any other payment. At least whilst you’re receiving it until it’s failed. You could charge a fee for it but at the end of the day we don’t know if probabilistically failing certain payments resolve some of the privacy issues. Can you charge enough of a fee on outbound payments at relay time so it becomes prohibitively expensive to constantly map the network? Research needed. The receiving node is yourself. If you’re probing you might send it back to yourself.

Q - If you’re probing somebody else they could punish you for it but if you’re probing yourself then nobody gets to punish anyone?

MC: If I’m in the middle of a payment and it’s coming down the line and I’m forwarding on to someone else I don’t know where it started or where it went. If it fails I don’t know whether it was a probe attempt or whether the payment just failed because one of the nodes was offline. Even if I did I don’t know who to punish because I don’t know where it came from or where it went.

JC: If you rate limit you’re not sure if you’re rate limiting a real payment. Alex Bosworth has probed our node and he’s been telling me that you have this amount of balance and this amount of capacity. You can tell which is kind of scary. Even the private channels, they’re not necessarily private. They’re unannounced. They’re unadvertised, not really private. People during the Lightning Torch, they were sharing their invoices on Twitter exposing their node and the UTXOs associated with that. It is something that should be improved.

MC: At a high level Lightning privacy is still a big open question.

OO: True, definitely need more research. Probing is a thing where you can go to extreme defenses but the defenses can decrease the quality in terms of the network. If everyone was dropping any random packet all of a sudden your pathfinding is a little bit less reliable. We’ll have to see if it becomes a big issue if there’s anything we can do. Probably the best thing is maybe to charge a fee to even make a HTLC at all and that at least adds a cost to probing. It can also be good with some of the stuff that Joost has been working on to see if a node can route at all effectively. It is still pretty early. We’re definitely watching this stuff and any research paper that comes out in this area I’m usually reading pretty quickly.

JC: It is useful in the context of making payments. I wouldn’t want to take it away. You want to know that the route is online and has capacity before you send the full payment.

MC: c-lightning does a lot of probing, always probing in the background.

JC: So does eclair. It has a configuration where you can probe how many attempts per second I think.

OO: Before it pays?

JC: All the time it is probing the network.

MC: c-lightning does it because they don’t announce the channel down flag, the channel offline flag until they receive a payment. They have to probe otherwise their node will never announce that a channel has gone offline.

MF: I just want to give Matt an opportunity to plug BetterHash because I think it is really important in terms of miners potentially censoring closing of payment channels in the future. I think BetterHash is really important.

MC: Lightning security is fundamentally broken (joke) and a terrible idea until we have better mining protocols so we should probably do that. In all honesty accepting payments right now on Bitcoin is really questionable. We’ve seen BGP hijacks against cryptocurrency companies, against cryptocurrency exchanges. The most recent malicious BGP hijack that I’m aware of globally was against Amazon AWS, the biggest hosting provider in the world in order to steal cryptocurrency by hijacking a cryptocurrency website. The amount of money you could do with a similar attack against Bitcoin miners is potentially much higher than they got against MyEtherWallet. This is not an unrealistic threat model.


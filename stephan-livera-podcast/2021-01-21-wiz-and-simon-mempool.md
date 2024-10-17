---
title: Mempool-space – helping Bitcoin migrate to a multi-layer ecosystem
transcript_by: Stephan Livera
speakers:
  - Wiz
  - Simon
date: 2021-01-21
media: https://www.youtube.com/watch?v=JZE_UlvBBBk
---
podcast: https://stephanlivera.com/episode/245/

Stephan Livera:

Wiz and Simon. Welcome to the show.

Simon:

Thank you.

Wiz:

Yeah, thanks for having us.

Stephan Livera:

So, Wiz I think my listeners are already familiar with you. But let’s hear from you Simon. Tell us about yourself.

 Simon:

I grew up in Sweden. I worked there as a software developer and about four years ago I decided to quit my day job and pursue a more nomadic lifestyle. So for the past four years, I’ve been mostly like traveling and moving in, living in different places around the world. And also got time to really deep dive deep into the Bitcoin space. I realised I wanted to like contribute something to this space. That’s why now being now I’m working on the mempool project.

Stephan Livera:

Yeah, that’s really cool. And I think the whole Bitcoiner nomad idea is something that’s picking up a bit more steam as well that there are more people who are talking about that as an idea, and it’s become, I guess more viable for people as well. So that’s a pretty cool area. And Wiz maybe just give a bit of an overview of yourself just for listeners who might not have heard you before.

Wiz:

Yeah, sure. I’m a full-time Bitcoiner originally from Hawaii. Quit school really young to work at an ISP and stay home and chat with my friends on IRC. And like 20 years later I’m still doing the same thing. Just talk to my friends on the internet and I still run my own ISP. Now with my own server, I run like a bunch of Bitcoin nodes for Bisq and Liquid now, like even one of the Bitcoin DNS seeds. I’m also publishing the Bitcoin Standard’s Japanese edition coming out soon and a few other random Bitcoin projects.

Stephan Livera:

Yeah, that’s awesome, man. So for listeners that’s basically Wiz is running a lot of different operational infrastructure there in relation to different projects. So he’s involved with Bisq, which is a well-known like peer to peer trading platform for people who want to trade Bitcoin. And he’s also becoming a Bitcoin DNS seed. So we might get into that a bit later if we get some time. But for now let’s talk a little bit about the project mempool.space. So just for listeners who aren’t familiar, this is a great website to go and basically visualise the blockchain and see what’s going on with it. So perhaps Simon, do you want to tell us a little bit about how you got started on this?

Simon:

Yeah, I think, I guess you can just start, like from 2017 when, it all became clear that the blockchain and the fees are not going to be for free anymore. And people aren’t really knowledgeable on how it actually works. They make transactions, but they get stuck, but they don’t really understand why. And so that’s why I come up with like this idea of building, like the original idea was like visualising the blockchain, seeing the blocks coming in and seeing how transactions are getting processed by the mempool, by the blockchain basically. So you can actually, for the first time visualise how it actually looks like because yeah, people didn’t have anything to relate to when it comes to that. So I called it the first version of the project in late 2018. And there was like a basic version with just transaction tracking and like this whole basic visualisation of the blockchain. And then like six months later Wiz contacted me, saw the project. He offered me to like host the project and he proceeded me through, you have to open source this man. And I released the code on Github, made it all open source and yeah, we took it from there. And then we just decided to that bit up.

Stephan Livera:

Yeah, Wiz let’s hear from your side, tell us how you found out about this project and how you got started with it, right?

Wiz:

Yeah. Like when Simon said I saw his mempool visualiser website and I thought it was really cool. And since I run a lot of Bitcoin nodes for various projects, I wanted to just monitor my own mempool of my own Bitcoin nodes. And so I basically said, yeah, let’s partner up on this project. Let’s make it into a legit open source project. And he was instantly very positive and totally agreed to do it. So like within a few days of talking, like we made the GitHub project and put together like basic installation instructions and screenshots and documentation. And we launched it. It was mempool v1 that was pretty cool, when we first launched it.

Stephan Livera:

Now, one thing that’s, I think important to point out is up until this point, most block explorers were more about looking at historical transactions and there wasn’t as much of a focus on this idea of thinking about the mempool, right? So that’s probably one important differentiator here, correct?

Wiz:

The mempool was never really relevant before 2017 or 2018. There was that, that so-called block size debate where later we found that it was actually a BitMain doing this covert ASIC boost stuff and spamming the mempool with high fee transactions and all these other scandalous things we heard about. But for whatever reason, the mempool was just not relevant and never got full before that 2017, 2018 bull market run. And Simon’s very innovative idea of visualising the mempool as projected blocks was really cool. That was really unique. And there was nothing like it ever since.

Stephan Livera:

Right. And I think perhaps that’s a really good, you’re probably the right person to ask on this as well. Because you’re a bit more of a Bitcoin OG yourself. But I think for listeners who maybe you’re a little bit newer to the Bitcoin world in the earlier days, because there were so many less people using Bitcoin in those days, it was much faster and easier to just kind of get your transactions through. Whereas in that kind of 2016 and 2017 and era, it started to become more like, Hey, there’s actually congestion here. Now we actually need to start thinking about fees on the blockchain. So perhaps Wiz do you want to maybe give us a bit of context there in terms of what’s happened with fees, transaction fees to use Bitcoin over the years?

Wiz:

I guess if you go back to the early days I remember when I first started in like 2013 or so you could actually do a zero fee transaction. And around that time, that’s when they realised that that was a bad idea for spamming or just denial of service attacks or whatever, and added a minimum fee. And I think it was just hard coded at like 0.001 Bitcoin per transaction regardless of value.

Stephan Livera:

Price was a lot lower than, right?

Wiz:

Yes, it was a lot cheaper and it was a lot it didn’t matter how big the transaction was. And then after that, they changed to this Satoshis per vbyte. And then later I think atoshis per virtual byte when SegWit came along and you have weight units and all these fancy things now, but yeah it’s been an interesting, like almost I guess, eight or nine years now of how the fee markets been slowly developing in the Bitcoin ecosystem. And now we’re kind of transitioning to this period where the mempool is always going to be congested and you always have to bid against other transactions for the getting included into the next block

Stephan Livera:

And Simon, anything to add there just on the fee market or the block space market dynamics over the years?

Simon:

No, I basically joined the Bitcoin space in 2017, so it was already congested and stuff. And I guess I didn’t find any good way of seeing what’s happening in the transaction. And so we are in like in this huge transition right now, we’re going to transition to a multilayer Bitcoin ecosystem. And that’s what the vision of the mempool space project is about now. And then not just supporting the base layer, but we need to support all the other layers and help people in this transition, help people find the right fee help people make an optimised fee, optimised transactions. We focus a lot on that.

Stephan Livera:

Yup. And so I think this is one of those things where in the earlier days, when everything was still viable on chain, people didn’t have to think about these things. So they would do small transactions on chain, but now we actually have to start thinking a little bit more deeply about what Bitcoin is and what it is best suited for. If listeners check out some of the episodes with someone like Vijay Boyapati, he would explain to something like, Hey, it’s actually, we need to think of it more like settlement layer or Bitcoin layer one is more like settlement layer. And so the smaller transactions will happen in other layers. So perhaps you guys want to expand on that kind of idea and tell us a little bit about what do you think that’s gonna look like?

 Simon:

To me now that the block space is extremely scarce and people don’t really realise like for example, if you run a Bitcoin node for yourself, you will start to realise that you need to keep a copy of every transaction that ever occurred like forever and store it on your hard drive right. So that is what you’re paying for when you mentioned your transaction. And if you look at it that way like five bucks. Isn’t that much actually you’re paying to be included and secured and stored in the world’s most distributed and secure ledger. So when people that is going to be a fee market. And I hope that the coffee payments are already priced out or Bitcoin because I don’t see the reason why we should store all the people’s coffee payments, like on all the nodes surrounded while it doesn’t make any sense.

Simon:

Right? So those could be stored in lightning, for example, or be transacted over lightning. And we are just in this huge transition period. When we have a lot of infrastructure, that’s not upgraded. We have a lot of use of non-segwit. We have a lot of transactions that doesn’t support fee bumping and lightning really needs to be activated, implemented on like exchanges and stuff. So it’s going to be a very rough period, like the coming years, I believe that the transaction fees are going to go up and down and be very volatile. So I think that the tool we’re building is like helping people really navigate this transition. And this volatility, that’s happening.

Wiz:

If you look at any project that was developed past five or six years in the Bitcoin ecosystem, a lot of them made this false assumption that Bitcoin transactions would always be cheap, which in hindsight is kind of silly because I think all Bitcoiners now understand why Bitcoin is valuable, right? It’s the first true form of digital scarcity. But if BTC is valuable because there’s only 21 million BTC, well then the space in Bitcoin’s blockchain, which also has a very finite limitation is also going to become very valuable. So one side you have this increasing demand for users who want to create new Bitcoin transactions. But more importantly, if everyone understands that number is going to go up and Bitcoin transaction fees are denominated in Bitcoin, then those two numbers kind of multiply each other. The the price in Satoshis per vbyte of your transactions will go up. And the price of dollars for Bitcoin will go up. So Bitcoin transactions, we’ve already seen it go up like a 100 X since I’ve been around since I mean it was like 5 cents to do a Bitcoin transaction a few years back. And now it’s like $5 to do a Bitcoin transaction, probably in another five, six, seven, eight years. It could be like $500 to do a Bitcoin transaction, depending on how certain apps and use cases get optimised or don’t get optimised take Bisq, for example, they every Bisq trade is like four on chain transactions. And until very recently, it wasn’t even using SegWit it was very unoptimised. And so if you want to buy a hundred dollars of Bitcoin on Bisq you would have had to pay like 10 or $20 just in the mining fees. So it already had priced out those hundred dollar trades. And so a lot of these apps are just going to have to adapt. They’re going to have to change to this transition of where the mempool is just always going to be congested fees, fee market is going to become very expensive. And it’s in everyone’s interest to kind of optimise their transactions, batch all their transactions together so that we’re not all bidding against each other so aggressively and driving the price up for it.

Stephan Livera:

Right. And so it’s a very complicated topic because there’s so many moving pieces or moving parts going on here. So one example is exchanges might start batching all the withdrawals. And so that may help the fee pressure dramatically as opposed to in the past when they were just doing single transactions for each person. And I guess the first level thing that people might be thinking is are, but hang on where’s and Simon, why can’t I just do one sat per vbyte and then wait for it to get confirmed? Why can’t I just do that?

Wiz:

Yeah, that’s a common misconception, right? Is that okay? I have a very low time preference. I don’t care when my transaction gets confirmed. So I’ll just use the absolute minimum fee of one sat per vbyte and just wait. Well, the thing about the mempool is that the mempool has a default size of 300 megabytes in Bitcoin core. And so the lowest fee transactions will actually get kicked out of the mempool once it hits 300 megabytes. And so this is actually one of the newer features we’re going to be adding to the site, but basically the other day, I think it was up to four sats per byte, every anything below that was getting purged. So yeah, I mean, you just can’t this is like a common misconception. I could see how people started using Bitcoin sometime in the past five years and they could always get away with doing this, but that just like zero fee transactions are not a thing anymore. One sat per byte transactions are not really going to be a thing anymore. And we’re going to see the market very volatile.

Stephan Livera:

Poor Ketan, my friend my co-founder of Ministry of Nodes. He is famous for his one sat maximalism. But I guess we’ll see. So there’s a few I guess, pieces to tease apart with this whole one set conversation. So one example would be, Oh help, hold on, Wait, why can’t I just go one sat, but enable this special feature called replace by fee. And so I might lowball at the start and then do an RBF replaced by fee. So long as that feature is enabled and that my wallet supports this feature that I could use, that.

Wiz:

That’s a good point. You can use RBF with a cheap fee and then increase it if necessary. And that’s a pretty good strategy, but not all wallets and use cases support RBF. For example, if you’re sending from one centralized exchange to the other you can’t really RBF it or even a CPFP it, child’s pay for parent. And there’s also this other problem right now, where if you want to bump the fee of a transaction using CPFP child pays for parent, if your original transaction got purged from the mempool, you can’t actually bump the fee for it. I think my friend Gloria right now just got a grant to do this package mempool accept where you’ll be able to submit multiple transactions into the mempool at the same time to address this problem. But my understanding is that once the minimum fee of the mempool has risen to above the fee rate of your now purged transaction, you can’t rebroadcast it, even if you’re bumping it with a seat of another transaction. And so it and that might be a couple of years until that gets fixed. So there’s just a bunch of things that need to get improved all over the infrastructure of the Bitcoin kind of economy here.

Stephan Livera:

Yeah right And I guess one other point as well, where here is that the 300 megabyte default, as you mentioned, it’s possible for some nodes to manually configure that to be bigger, they might say, okay, I’m going to allocate one gigabyte or whatever. And I know as well that there are other, for example, there are mining pools that offer this as a service. So I think pushtx.com is one example where you can go there, tell them this transaction, and then pay them a fee out of band, meaning you might pay them with lightning to accelerate one of your transactions, such that the next time they come across it, they can try to manually bump it in their own and ensure that it goes into a block. And I guess this is just one example of how the ecosystem might evolve over time. What are your thoughts there?

Wiz:

Yeah that’s a really good point. A lot of these mining pools, it’s kind of like a secondary market for space in the Bitcoin blockchain is going to merge. And we’re, we’re probably going to add this feature on the site at some point, but yeah, I mean, there just needs to be a better way out of band. Like you said, for people who want to manually prioritise a transaction and if people make mistakes or they can’t bump the fee for whatever reason and say the market’s moving and the mempool’s congested and they really need this transaction to get confirmed there a market for that. Those people would be willing to pay a fee to have it manually prioritised. And so definitely the future of the Bitcoin mempool space market, blockchain space market will develop as you say,

Stephan Livera:

And while we’re on this topic as well, it’s probably also good to talk about fee estimation. So why is this a hard problem?

Simon:

Well, yeah, the biggest problem is that you don’t know when the blocks are going to arrive. It’s total random, it should be like over time it’s one block every 10 minutes. But if you go to mempool.space and look, when the blocks are arriving, you’re going to get like three blocks in a row within one minute, and then it takes hour for the next block. And during all this time that the mempool is just getting congested. And so you have no clue of knowing, like when, and also not just that, like all the transactions are coming in, new transactions are coming in with different various of fees. So like all of a sudden you have like big players. I know, like BitMEX, for example, like on Mondays, they will, on a specific time, they will dump a huge amount of transactions in the mempool.

Simon:

So it’s impossible to foresee all this stuff. So, and so that’s why it’s also impossible to do fee estimation. And most of the traditional fee estimation tools are using like a statistical approach so that you can get a probability. Like if I use this fee, I will have a probability of 95% of having it confirmed within 30 minutes or something like that. But the mempool website has a more mempool based fee estimation system, which is different. Like some people love it and some other people maybe don’t, but it’s like up to preference, but basically we’re looking at how the mempool looks like and show you, like, what do you need right now to get into the next? And that is reasonably accurate. I mean, I know, and because the mempool is so volatile, you can have one block with a super low fee and then the next block with a higher fee. So we our estimation is more like dynamic fluctuates more than the traditional. And we have received a lot of feedback, of people really liking our approach and have been able to reduce their fees a lot because there are able to see like a snapshot. What does the mempool look right now? Okay. I’ll put this transaction fee if it’s gets into the next block. If I get lucky within 10 minutes. Yeah. I didn’t have to pay that much of a fee.

Wiz:

Yeah, that’s a really good point. When I first started working on the Bisq project all the Bisq nodes were, I think using earn.com fee estimation API. And when it didn’t matter it was okay. But as soon as the mempool started to get congested, like within the past six or eight months users really got upset because they, the API was so like horribly inaccurate and that’s around the time. And it’s also like a centralised point of failure for the Bisq network anyway. So it was a really cool use case of the mempool project to have several fee estimation API backends now running by several different Bisq contributors and using the real time mempool data to very accurately tell you like updated every few seconds, what fee you should use. And that really improved the Bisq networks flow because with Bisq networks, since there’s so many on chain transactions if transaction gets stuck in the mempool, it would really disrupt some trades. And Bisq UX is already kind of clunky because it’s totally decentralised. So you want to improve as many things as you can to make it as smooth as possible for people to stack sats without a centralised party and having a decentralised project like the mempool fee estimation was really important.

Stephan Livera:

Great. And how would the fee estimation using mempool.space differ from say the estimation that might be in my Bitcoin wallet?

 Simon:

Yeah like I said, we’re using the mempool base fee estimation and some tools do that. So just like differ from tool to tool. As I think the majority are using like a more statistical approach and those usually give you a higher fee, but yeah, you have to see which wallets you’re looking at.

Wiz:

It depends on the wallet implementation right? Even core like Bitcoin core’s fee estimation, I found was not nearly as accurate as mempool space, just because of the way it uses the projected blocks. And it takes the medium fee. It’s a pretty simple algorithm we have in there now, and it could still be improved in a lot of ways, but it was surprisingly already the best in my experience.

Stephan Livera:

Great. And so in terms of tools that users are using other than mempool that space, what sort of tools are they using and how would you contrast that with the mempool, that space approach?

Wiz:

I guess when it comes to block explorers most of the block explorers out there, the popular ones are not even open source, right? So if you don’t want to use like a totally closed source. A centralised website, that’s probably logging all of your queries and using all kinds of third-party trackers and analytics. It’s really cool to have an open source tool that you can even just self host locally and not have to trust anybody connect to your own node. If you’re looking for tools, even if it’s not fee estimation or block exploring, just to like be able to know that someone’s not logging your data and connect it to your own full node is really huge. And if you have a tool like that with a really slick UX and design I think you can have the best of both worlds where it’s fast and local and self-sovereign.

Stephan Livera:

Yeah. So a good example, there would be, if let’s say the listener has sent a Bitcoin transaction and they’re waiting for that to actually get confirmed. And now in that time, they might be out there, copy pasting the transaction hash into a block explorer. And if they’re not using some kind of anonymization technique like Tor or VPN, and so on at that point, they may be doxing certain aspects of, Oh, Hey, this IP address is interested in this Bitcoin transaction where if that user is using their own block Explorer then that’s where you’re saying, as you’re saying that user can reduce the amount of leakage of info, because now they’re only looking up on their own computer.

Simon:

We’ve been having this focus since the beginning, actually that you should be able to run this whole mempool explorer locally on your own node. And it’s just this we just recently recently released a latest version. Right. And since it’s a bit different from the original one, it took more some more effort to make it adapted to running on a regular node. But we just finished that work now.

Stephan Livera:

Yeah. So yeah, so I think it’s, the ecosystem is going to have to transition. And so we may see more attention come and that may in some way drive the use of lightning. It may drive, unfortunately we don’t want this, but it may drive more use of custodial services and potentially things like sidechains like Liquid. So perhaps Wiz, do you want to spell out what some of those implications might look like as this ecosystem matures?

Wiz:

Yeah, I guess it’ll be interesting to see how it develops like the most obvious common use cases, something like in USA they have a Venmo or cash app or PayPal where it’s just totally a centralised database. And if you want to send money to your friends, either it’s Viet or SATs it’s just kind of like updating a database entry in essentially what’s a bank fully custodial thing. And up from that a little bit, like you said, you have a side chains like Liquid where you have these kind of IOU tokens that I think it’s pretty cool because on the sidechain, like Liquid, you can verify that not only how much Bitcoin they’re, they’re holding but also the liabilities. So in other words you can verify all the Bitcoin holdings, but also all the the IOU token holdings.

Wiz:

And you can run the numbers and make sure that they match up and you can very easily see that they’re not running like a fractional reserve or anything like this. The sidechains also have cool features like confidential transactions for base layer privacy like one minute block times of course, very low fees. And you can also do like some kind of basic smart contract functionality atomic swaps of other assets, like USD fiat coin assets to sats and things like that. There’s a bunch of really cool stuff on like Liquid that you can’t do on other things. The most extreme, like the most distributed you have lightning, right? Which of course is this layer to payment network is fully distributed. There is no blockchain at all. You’re just kind of settling on chain every once in a while, if you need to. So there’s like a full spectrum sliding scale of centralisation decentralisation to being fully distributed in this layer two ecosystem. They all kind of have their trade-offs in terms of security and privacy and freedom and censorship resistance and verifiability.

Stephan Livera:

Yeah, exactly. I’m, so for listeners interested in a more in-depth around Liquid check out my earlier episode with Allen Piscitello from the Blockstream team and he explains it kind of like a fancy Multisig bank, if you will. But different trade-offs obviously, so have a listen to that as well. But I guess Wiz and Simon, do you have any comments there around how mempool space is going to help enable their user be a functioning member in the same ecosystem across the different layers?

 Simon:

Well, we started with just supporting the Bitcoin blockchain, right? And then we added support for Liquid and I think the next big project for this year, is going to be adding like a lightning explorer and then we can like connect everything together. So we already support this. Like, if you make like a Liquid transaction and you do it, pick out the Bitcoin, then you can just click a link and you get redirected to the Bitcoin transaction where it actually got settled. It’s all very connected in like the same multilayer ecosystem like this.

Stephan Livera:

Very cool. And so maybe Wizz could you tell us a little bit about some of the operations of the website and keeping it running as a, as a community resource?

Wiz:

Yeah. It’s pretty impressive how popular the site has gotten over the past year or so since we started supporting like full block Explorer functionality and especially most recently as the mempool has just been constantly congested over the past month or two. Now, seeing like over 50,000 daily active users and a lot of like wallet apps or exchange networks like Bisq or many others not only are integrating with our APIs or linking to our block Explorer so that users can easily look up their transaction and see where it is in the mempool. But they’re, they’re actually setting us as like the default Block Explorer, which is really humbling. I think Phoenix wallet by ACINQ, which is this really slick lightning wallet. I was very surprised to check out the wallet and click on a transaction and have it open on mempool space.

Wiz:

And it’s just so heartwarming to see the community really embrace the mempool project and integrate with it so much, but operationally like we’ve got a bunch of donations from community sponsors and we use those funds to purchase a bunch more servers. We’re actually in the process of setting up the mempool to be its own ISP. Right now it’s hosted on my ISP. So it’s self hosted by me right now, but we want mempool to be totally self hosted. So once mempool becomes its own ISP, that’ll be really cool and anyone is welcome to set up their own mempool node as well. If you want to take some if you don’t want to route our request to our servers, right? I mean, we of course operate the service, like freely for the community, especially over Tor, but it’s always best to run your own instance, so you don’t need to trust us.

Stephan Livera:

Right. And so for the users who are less technical, or maybe they don’t have as much time to go and manually run it, the other cool part is you guys integrated into some of the well-known Raspberry Pi projects as well. So can you tell us a little bit about that and how users can make use of that feature or make use of that?

Wiz:

Yeah, I guess we just shipped the mempool V2 explorer suite on raspiblitz and that’s the first Raspberry Pi platform we’re supporting, we’re working on the Umbrel app store integration now. And after that probably RoninDojo start nine labs. Maybe even myNode we have see if we can get working with the BTCPay server Docker environment too. But yeah, we hope to be on all of the popular Bitcoin full node distributions for Raspberry Pi soon. So it’ll be as simple as just clicking one button and having that mempool app installed on your Raspberry Pi .

Stephan Livera:

Yeah. And as I recall even I think myNode definitely had a V1 on there. I think it does still have that. And so I guess, was there any question around like the processing and the capability of the Raspberry Pi nodes to be able to run that on top of Bitcoin and lightning and whatever other applications they might be using?

Simon:

Yeah. We have to do a lot of tricks. Like we are using Bitcoin core for a lot of requests, and then we have to use the bundled Electrum server for the address look-ups. So it’s like, we are like missioning and matching to get to almost the same features as on the mempool space website. So you get all, you get all the basic feature, like transaction tracking, you can use scripts, you can do all the most advanced stuff. It’s just some of the high performance stuff that doesn’t really work. Like you can’t open, like an address containing thousands of transactions. Then there’s usually like a limit in the Electrum server and stuff. There is some limitations like that usually related to performance.

Wiz:

Yeah. Unfortunately the trade-off of Raspberry Pi being very inexpensive hardware is that it doesn’t have a lot of horsepower. So like for the mempool space website, we have a cluster of several very powerful servers with very fast non-volatile memory drives and tons and tons of RAM and powerful CPUs to index literally everything and keep it in Ram. So when you use the mempool space website you can view any address, even if it has millions of transactions that it’ll just load instantly. But I think the limitation on the Raspberry Pi is like a hundred or a thousand transactions per address now and give it’s more than that. I think the Raspberry Pi just gives up and says, well, you can look at this on mempool space or another instance, but as a Raspberry Pi that’s all it can really do, right.

Stephan Livera:

Yeah, of course. And I think anyone who’s doing really hardcore level of transactions all off one address and things that those kinds of people can go run like a full instance themselves. So I think for the typical home user retail level, just like a family kind of person or that kind of group of people who are going to just be using a Raspberry Pi , I think that makes a lot of sense as well for the typical kind of customer. Yeah.

Wiz:

Yeah. It’s really perfect for a home user, because most wallet apps these days, they don’t reuse addresses anyway. So on a single Bitcoin address in your wallet, you might only have a few transactions. So ample spaces on a Raspberry Pi is totally sufficient for looking up your own transactions. I mean, there’s no way, the average person is going to have millions of transactions on a single address. Right. That’s the most extreme use case.

Stephan Livera:

Yeah, of course. So how would a mempool.space differ with some of the other kind of older block explorers in the space?

Wiz:

I guess the oldest is probably blockchain.info, right. Which is a fully closed source centralised explorer slash wallet backend, I guess they were like the first like serious ones. So that’s why they have a lot of users still. But I mean, they have a lot of shitcoins. They have a lot of airdrops, they have a lot of like advertisements it’s like they were, they didn’t really add SegWit. They were supporting like BCash and I think even ripple or something, I don’t know, but they’re just not really like the best members of the Bitcoin community. Right? Like you can tell it’s a typical for-profit company they’re trying to increase the value of the shareholders wealth and things like that. Obviously the contrast to that is like mempool being an open source project.

Wiz:

Just give away all the code for free, and there’s no ads, there’s no shitcoins. It’s just pure. It’s like BTCPay in the sense that Phila very famously tweeted at BitPay, I’m going to obsolete you and sure enough. He just hacks a bunch of code together and now BTCPay is like the de facto way to take Bitcoin payments. Like, why would you use BitPay despite them being this big company with millions of dollars of VC, why you use a company like BitPay that has full KYC and all these restrictions, when you can just one click install it on BTCPay on the Raspberry Pi and everything works. And that’s what we’re trying to do with the mempool project, right. Its kind of obsolete these a BitPay style block explorer websites. Block explorer should be an app. It’s not some, it’s not supposed to be like a bank that you have to fully trust with all of your data or all of your self sovereignty, right?

Stephan Livera:

Yeah, for sure. And I think it’s interesting that in the earlier days, a lot of things had to be just done by some more centralised service. And over the years, as things are maturing, it’s becoming easier and easier for the user to become more self-sovereign right. And so I think it’s like there’s a suite of software and projects and hardware as well that are enabling people to become like the early days the saying was Bitcoin, be your own bank. That’s really what it was. How do you see mempool fitting in as part of that call it full stack of apps?

Wiz:

Yeah, that’s a good that’s a good name for it, right? The Bitcoin full stack, where on a Raspberry Pi you have Bitcoin and lightning and Electrum server and BTCPay and maybe Bisq pretty soon and now mempool tool. There’s a bunch of other apps like coin mixing or all of these random applications that are all part of this open source ecosystem. And this full stack allows you to do everything. Like I said, Bitcoin is you can be your own bank. Maybe lightning is your own visa or MasterCard payment network. And BTCPay is like your own payment processor, like square or something like that. And Bisq is to be your own Bitcoin exchange. And mempool you can be your own Explorer and your own fee estimation backend your own everything. Right? So I guess that’s the goal is of a Bitcoin full stack is to kind of eliminate that dependence on companies and just use open source apps that are self hosted on your own hardware with your own keys and no KYC or anything to infringe on your personal rights.

Stephan Livera:

Yeah. Now, one other thing that can be a bit difficult for people in the space now, maybe not so much for the listeners of this show, they tend to be more hardcore, tend to be a little bit more, either technical or motivated to learn, but it is something we have to think about because Bitcoin Twitter and SLP listeners are not representative of Bitcoin holders everywhere. And in many cases the family members are dependent on the technical person in that family running something for them. Just like the technical person in the family might deal with the router for the family and things like that. So I guess maybe the idea then is as long as the tooling can be built out in such a way that at least if the technical person in each family or in that group of friends can be proverbial uncle Jim, as my friend, Matt Odell would say, right?

Wiz:

Yeah. If you’ve got one technical person in your household who you can trust to set up a Raspberry Pi, then all the members of that house can easily point their wallets at it. And maybe you want to share some lightning channel liquidity to save on chain fees and things like this. Maybe you don’t want to use our mempool explorer instance, but your uncle Jim is running one. So you use his because he’s not going to sell your data to blockchain analysis firm, right? So it’s all about being able to choose who you trust, right? If you want to make it, build it yourself and run it yourself and trust yourself, that’s great. But if not, you should still have the option of who to trust. So you don’t have to just trust the government or trust the central bank. You can trust uncle Jim because he’s your family and that’s a really cool capability to have that option.

Stephan Livera:

Cool. And what about, I guess, ongoing, just in terms of keeping the project running there’s obviously got to be some operating costs in terms of servers and I mean, the time for you guys to develop and maintain these things, what do you have any thoughts on how the project will be made sustainable for the longer term?

Wiz:

Right now? I feel we’re finally ready. After working on this project for a couple of years to call it like a real serious open source project and apply for some grants, maybe we’ll set up a mempool foundation or something. I don’t know, it’s community funded, right? So we have a sponsors page including like yourself and a number of other very well-respected Bitcoiners have signed up as sponsors, where if you donate a million sats you get your photo on our page. So we’re totally community funded and developing this project for the community funded by the community, built by the Bitcoiners for Bitcoiners kind of thing. So it feels very wholesome and heartwarming. The love from the community, both in terms of just the number of users and apps integrating with our site. And as well as seeing like how much donations we’re getting too. So hopefully that’ll continue to support us. We’ll be able to not turn into an evil company, but stay as a happy open source project. Right.

Stephan Livera:

Awesome. And in terms of the future of the project, are there any other things you wanted to highlight in terms of features or things that you’re looking to work on? And maybe tell us a little bit about what’s going on just a refresher of what’s happening with the Raspberry Pi support as well.

Simon:

Yeah. We’re continuously expanding our Raspberry Pi support. We’re going to support Umbrel. My node, RoninDojo, there’s one called start9 labs. I think. And I think the biggest thing, the biggest new feature that I hope to start working on this year is like a lightning explorer thing. So, and because that is what most of the Bitcoin ecosystem is moving towards right now. So that feels like the most important next step. And then I don’t know yet if it’s possible, but it would be great if it’s possible to use it on a Raspberry Pi as well. So you can support everything

Stephan Livera:

Actually on that, on the lightning node Explorer, I’m curious how feasible that will be, because I understand right now in the ECDSA kind of world, it’s easier to identify on chain lightning channel opens and closes, but theoretically, if we got Toproot and most people upgrade to that, then it might actually start to become less visible on chain, which one is a channel open and which ones are channel closes and stuff. Right,

Simon:

Exactly. So we have a feature. Now, if you go to a transaction, we flag like this is a two of two multisig transaction. This is a lightning close, for example, stuff like that. But as transactions are moving to taproot, everything like that is going to be invisible so we’re not going to be able to like, do this connection anymore, I think, but it’s going to be a transition. So it’s going to work. I think coming years, most probably, and people are still going to need to use like a lightning explorer to when they’re going to set up the new lightning node. The first question is like, okay, so who to open my channels too. So they need like the tool to provide them, which channels need incoming liquidity, for example, which routing nodes has the best routing in the network. I think that is a big key thing that we need to focus on next up.

Stephan Livera:

Yeah. That’s really interesting. I like that point because I know the Lightning Labs team have this thing called bos scoring. And so then you might want to try to figure out who you need to connect to in terms of, who’s a good note to connect to, and theoretically in the lightning network, if you want to be a good routing node, then you theoretically want to open channels in the direction that people want to pay. Hey, so if there’s some way that the user can have like a dashboard that has that information now, I mean, that could also maybe be done on lightning dashboards, like RTL or thunder hub and LiT but it could potentially also be a part of mempool space as well. Right?

Simon:

I think it makes sense for the mempool, because we are the Explorer, right? You search for transactions block, you also will be able to search for lightning nodes and channels, and the are supporting like all the layer two networks now. So we will just continue to expand and support and see where the emphasis is going forward.

Stephan Livera:

I also like the point that you made earlier, Wiz about, well, it’s a new feature that shows you, which transactions have fallen out of the default mempool, because that will then give the user an indicator that they need to do something about this now. Right. They need to try it if they can to RBF replace by fee or CPFP on the other side to get the recipient, to try to accelerate that transaction or to use some kind of transaction accelerator, right?

Simon:

Yeah. We really want to, I really want to like improve the user experience because I get so many people that they sent me like a link to mempool space and say, Hey, my transaction got stuck. What do I do? So we really need this explanation because people usually don’t get what’s going on. So it needs to like, explain, this is how long until it will get confirmed, you can use this or this method like replaced by fee. And we also flag, like, if you go to a transaction, you see like green or yellow or red flags, like, Oh, this transaction support replaced by fee, or this one has support SegWit and you put a decent fee, but if everything is like blinking red that something is not something that’s not good. You need improvements. Like maybe you need to change to better wallets and stuff like that. So we’re like really trying to help people like, realise what’s going on. What’s why is there a transaction stock? And like, Oh, you can add that as the last option. You’re like, Oh, you can maybe go to this site or do a transaction pay for transaction accelaration.

Wiz:

Yeah. I think it’s the stated goal of our project to basically help the community optimise their on chain usage and essentially migrate to the upper layers of the Bitcoin ecosystem. So it’s really cool to like Simon is saying, be able to paste in a tx ID, analyze your transaction, have the site suggest ways in which you can improve or optimise your on chain usage and save on fees. And for example, if say there’s three ways to improve to bump a fee, you can RBF it. You can CPFP it. Or you can manually accelerate it by paying, bribing one of the mining pools to accelerate it. Then, we could have those three buttons there, but if your transaction does not have the capability for RBF set, then maybe one of those buttons would be greyed out with like a little error message that says all your transaction is not RPF capable.

Wiz:

Maybe you should switch to another wallet. And then we could actually educate the user with a comparison of wallets or explain at least how to do the other options that are available to them. Like CPFP. And just kind of explain that cause we had like a million emails from random users, like, help my transactions not confirming, can you please confirm it? And I always refer them to Simon who’s in charge of confirming a transaction, but I mean, that’s the joke, right? Is that we’re just an Explorer. We don’t control anything of the network. We’re just observing it. But the users really, a lot of these just really think that we’re the mempool. Right. Which of course doesn’t exist.

Stephan Livera:

I mean it’s funny, but also sad. Like it feels like, Oh man, that’s because I can imagine you guys get a ton of emails or people hitting you up saying, Oh, Hey, please confirm this for me. And you’re like, well, I can’t actually help you mate. Well, I can sort of help you, but I can’t really.

Wiz:

Yeah. So that’s what we want to improve. We want to actually be able to help these users maybe we’ll partner with some mining pools and have their acceleration features on the site. Maybe we’ll link to some wallets where they’ll teach the users how to RBF it or CPFP it in the future. So that’ll be like the I guess the next goals of the short-term at the site.

Stephan Livera:

Yeah. And as an ecosystem, I guess it is going to now go towards wallets that have RBF and we might even start defaulting to RBF on where maybe historically that was not always the done thing. Because back in the older days, people could just go one sat per byte and wait, or low-ball it. And wait, where now it’s more like there really is a chance in this next year or two that we hit that level of block space market such that there is a real risk that your transaction falls out of the default mempool does not get relayed, does not get mined, et cetera.

Wiz:

Yeah. I think the mempool is going to become this, a living, breathing beast, right where you have a wallet and currently you pick a fee and you broadcast a transaction and the wallet basically forgets about it at that point. But I feel that you’re not really going to be able to do that anymore. Now wallets are probably going to need to constantly monitor where the transaction is in the mempool. And if it falls behind a certain threshold based on the users priority or time preference, it might want to RBF that up. To avoid getting purged or really buried down deep in the mempool, you might want to stay within the next few projected blocks or something like this. And so in theory, you could start the transaction out with the medium fee and within every few minutes, maybe bump it up a little bit, just waiting and seeing how things go. There’s a lot of things that wallets could do to improve their RBF functionality.

Stephan Livera:

Actually, I’m curious while we ‘re here. Is it, are you only able to RBF it one time?

Simon:

I think you’re able to RBF it unlimited times.

Wiz:

Yeah. The number is very high, right.

Simon:

And also we actually have a unique feature on the mempool space website that actually detects RBF. So you get like a dialogue showing up this transaction has been replaced and you are taken to the new one, but I also like to add to it, like there’s when I watching the mempool all day and stuff, there’s I see so many inefficiencies going on and people are using old wallets and they’re using exchanges that hasn’t like implemented SegWit and they doing a coffee payment on chain and stuff. I mean, there’s so much left optimise. And I guess this is the nature of the voluntary system that Bitcoin is like, nobody can force everyone to just upgrade to the better protocol, better addresses or something. So usually when people complain about fees and stuff, they’re actually running an old wallet just using legacy addresses? Which makes the transaction fee actually twice as much as with a, what it would have been with a SegWit transaction and then they are not able to RBF it and then it gets stuck. So that’s why we really need, that’s why I’m really trying to help people take the decision and leave their wallet changed in other wallet. And there’s a lot of infrastructure out there that hasn’t been upgraded. So it’s a lot of inefficiency.

Wiz:

Yeah, sure. If you’re a business That’s profitable, making regular Bitcoin transactions and you’re probably busy on scaling up that business, whether it be an exchange or anything, and usually passing on the withdrawal fees to the users. Anyway. So as like this decentralised exchange operator, there, isn’t a huge financial interest to implement SegWit or do batching or other optimization until the users are really about the fees. And we saw this with BitMEX. I remember once it costs like 75 or a hundred dollars to do a withdrawal transaction for BitMEX back in like 2018 or something when the mempool was very congested. And now we’re seeing that they’re optimizing things finally and Bisq too. Bisq is a decentralised network. So the interests are more aligned with the community. But it was just a big technical challenge to implement SegWit in the trade protocol itself.

Wiz:

So it’s a huge amount of work for these both centralised and decentralised platforms to optimise their transactions. And it is a risk if they screw something up, they might lose some funds. You really have to work hard on it. It’s a lot easier for them to just say, Oh yeah, we’ll just pass the fees on to the user. Right. So I can see why the community is always slow to kind of adopt the new technologies or optimise things further. But the financial incentives will only get stronger and stronger and stronger to do that. Say it costs Bisq aa $150,000 to pay developers to implement SegWit into the trade protocol. Well, at some point the users will be losing more than $150,000 in additional mining fees. They could have saved. So at some point it makes sense to do it. Right.

Stephan Livera:

Yeah. Really interesting stuff. I’m curious if you guys have any other funny observations in terms of what you see happening on the mempool. Is there any other kind of funny off the wall kind of behaviours?

Simon:

Well, I think it’s very interesting and important to reflect that we see that today, we are like in a new bull market and the fees are like $1 now, or even less to make a transaction. And we’re not congested at all compared to what was it four years ago when like the bull, the end of the bull market 17 when it was crazy and backlog of a hundred thousands of transactions. And so now we’re already back at those levels, but the blockchain isn’t nearly as congested because of all the optimizations that has taken place the past few years. So when people complain that we need to raise the block size or something, that fees are too high. I mean, the only thing that can solve that is economic incentives for people to use the block space more efficiently, do batching do SegWit, and go do stuff on off-chain.

Simon:

I mean, I see a lot of people sending, like, just from exchanges, that’s like a huge part of the mempool people just sending between maybe they buy on Coinbase, then send to Binance. I mean, that transfer could have been occurring off-Chain instead, that like using the Liquid network, which is actually built for inter exchange settlement? I would just remove a huge part of the mempool congestion and the fees will go down again. That’s why I’m a bit optimistic about fees actually going forward. I think we could like 10X the amount of Bitcoin users coming like four years, but still like keep smaller keep not too high fee level because the economic incentives are there to force people to actually optimise. And that’s a good thing when fees go up.

Stephan Livera:

Yeah, that’s a really cool point.

Wiz:

Even if the fee rate in terms of Satoshis per byte, that you’re paying doesn’t go up and it stays the same over the next four years, price a Bitcoin in US dollars is going to go up probably another 10X, right? So in fee it prices, the Bitcoin transaction costs are still going to go way up. And I think that’s even stronger incentive to optimise these transactions. And now I’m on the Liquid board and I hear some interesting stuff. Like there’ll be two large centralised exchanges that send a ton of transactions to each other, and they could put all of these transactions onto a sidechain, like Liquid and there’s even data to show this to the exchange operators, but for whatever reason they’re not very interested to implement it because they don’t pay the fees. And they like the the security of using the Bitcoin blockchain to settle all these things. It’ll be interesting to see who actually takes what actions to optimise what transactions, what gets moved off chain, what stays on chain. The future is bright, right? Like all around. We’re going to have more tools and more infrastructure and more optimisations coming together, along with the number going up, incentivizing all that.

Stephan Livera:

Yeah. That’s a really great point about the fiat value rise. Because as I understand in the earlier days, there were people paying fees, literally multiple Bitcoins in fees. But the fiat value was just so much lower back then. Whereas now the fiat value obviously is much higher as we speak today. What does something like 36,000 USD for one Bitcoin? So the bit in Bitcoin terms fees have come down quite a lot. It’s just that in fiat terms, they’ve gone up a lot. And so that’s an interesting point and we should probably anticipate that to continue. One other point, I think I’d love to get your thoughts on, because you guys are obviously so much more involved with the mempool. I think we potentially, we see this kind of seesaw effect of as the fees rise, then the engineers go to work and the companies get an incentive to start doing batching and SegWit and use lightning and use Liquid.

Stephan Livera:

And then maybe the seesaw kind of tips the other way, because now they’ve made it so efficient. That’s fees become really cheap again. And then and then you have to wait for another big uptake in adoption before you see the congestion rise again. So it’s kind of like this back and forth Seesaw effect. What’s your thoughts? Do you think that’s the likely way this goes or do you see it more just like, no, it’s just going to be continued on chain congestion from now on, and now you just have to use mempool.space and other tools to deal with it.

Wiz:

Yeah. I think you’re right about the Seesaw effect. And more realistically, you’ll probably up until now, we’ve seen where the mempool was just not full all the time and you could always get away with doing the minimum one set per byte, but now I think what we’re going to see, and we’ve already been seeing it like the past month or two, is that even though the going fee rate is only like 10 or 12 sats per byte on the weekends now, there’s still this huge backlog of low fee transactions, like from maybe like three or four sats to eight or 10 sats or something, and just know tens of thousands of transactions that they’re getting churned out on the weekends, but it never really clears out. And so now you’re seeing what, before there was, there was no floor or the floor was 1.0 sats per byte, you buy. Now that floor is variable and it’s probably going to rise up to like four or five sats per Byte. So you will see the seesaw effect, but more importantly and more relevantly to most users. Is that the 1.0 sat days I think are kind of gone, maybe now it’s more like a four or five sat per byte if you don’t want to get purged under the metaphor.

Stephan Livera:

Yeah. Very interesting and insightful comments there. Anything else you guys wanted to mention about the project?

Wiz:

I guess if you want to know what’s going on with your transaction, if it’s stuck in a mempool, check it out at mempool.space, and if you really like the project, you can self host it on a Raspberry Pi there’s even a shop selling Raspberry Pis preloaded with a Raspiblitz on the foremost store where you can buy a mempool Raspberry Pi very low price. If you want to support the project or report some issues to our GitHub or some features you’d like to see you can you can just create an issue on our project page, or if you want to donate some funds you can become a sponsor on the mempool space about page and really just hit us up on Keybase or Twitter whenever you want to to ask us anything at all. We’re very happy to work with the community on anything you want to see added to the site.

Stephan Livera:

Fantastic. I’ll include links in the show nodes and I really liked the project, so I wish you guys well, and thanks for all the great work you’re doing. And thank you for joining me on the show today.

Simon:

Thanks a lot!

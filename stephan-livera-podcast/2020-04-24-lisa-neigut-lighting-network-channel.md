---
title: Lightning Network Channel Accounting and Dual Funded Channels
transcript_by: Stephan Livera
speakers:
  - Lisa Neigut
date: 2020-04-24
media: https://stephanlivera.com/download-episode/1969/168.mp3
---
podcast: https://stephanlivera.com/episode/168/

Lisa Neigut of Blockstream joins me to talk about Lightning Network Channels, c-lightning, and Dual Funded Channels.

Stephan Livera:

Lisa, welcome to the show.

Lisa Neigut:

Hi Stephan. Thanks for having me on.

Stephan Livera:

So Lisa, I saw you tweeted out about wanting to talk about lightning cryptographic primitives and some of the, obviously you’re working on a range of things, at Blockstream on the Elements project working on C-lightning and the lightning spec and stuff. So can you just tell us a little bit about yourself and how you got into being a lightning developer?

Lisa Neigut:

Yeah, sure. So I actually got into Bitcoin, man, I’m going to say like two years ago now. I ended up, well yeah, I guess Bitcoin and in lightning.I got into Bitcoin because I ended up getting a job at Square working on the Cash team on the Bitcoin like backend. I was kind of in this process of transitioning away from being an Android developer. And I knew Java, which is what the Square Cash back end is all written in. And I had some good friends who worked on the Android team there, so I wanted to go work with them. And one of the backend roles that they had available just so happen to be on the team that was supporting the custody wallet that runs behind Square Cash. So yeah, I got on that was like my first ever like Bitcoin job.

Lisa Neigut:

And then while I was there, I like picked up a book on Bitcoin. I think it’s, I always get this wrong. And Andreas Antonopoulos I believe is his name. He has a great book called Mastering Bitcoin that I recommend to like anyone who’s interested in learning about how Bitcoin works, that would be the one. And yeah, so I like, you know, I read that and got like super, I was just got super excited about how cool Bitcoin is, like the engineering, like parts and pieces that go into like making Bitcoin as a system work or just really incredibly beautiful and cool. And I like how Bitcoin is like super, it’s like very multilayered, if that makes sense. Cause there’s a lot of stuff going on at like, so there’s like cryptography and then there’s system engineering. And then there’s like consensus protocols that Bitcoin is really cutting edge, new stuff on.

Lisa Neigut:

And then you can layer on top of that incentive design, which is kind of veers into like the economic and market kinda like, you know, like how there’s like the mining game so to speak. So like incentives for what miners have and then fees games. So there’s just like a lot of stuff going on in Bitcoin. So I like very much like fell in love with how cool and interesting it is. And then the way that I got into lightning stuff is I had this like kind of little project that I wanted to, like I was doing some like light research into. Basically when I was reading Antonopoulos’ book, like the Mastering Bitcoin, I realized it’s not even really a bug. It won’t be a problem until like 2130, which is like over a hundred years from now. But at some point, the header field in the block header, there’s like a timestamp.

Lisa Neigut:

And at some point in the next century that will like no longer be big enough. And so it kind of became this like fun entry point into like figuring out how Bitcoin gets updated. It was like, okay, so like if you wanted to make it such that this like Bitcoin header problem isn’t a problem in 2135 or whatever what would you need to do to change Bitcoin to like make it not a problem? Right. So this was like the research project that I set myself out on. And this was in within like two months of like reading the book and like being like, Oh, Bitcoin’s cool. And I was like, Oh, well what would I do to like change it or like fix this bug, right? And so that kind of led me on like this journey of like, you know, reading the white paper and then reading some of the resources in the white paper.

Lisa Neigut:

Like the footnote stuff. I don’t know exactly what the footnotes are called. References, I don’t know. It was sort of like led this process of reading through BIPs. And then some reason or another happened to cross like inaudible Russell’s email in one of the BIPs. And there’s actually a bit that had three authors. I like Googled each of them and managed to find Rusty’s blog. And so he was the one, I decided I was going to send my questions to about the processes. Like it was basically like, Hey, like I found this like sort of bug in Bitcoin. Like, I know it’s not really a bug, but it’s kind of an interesting thought experiment, whatever. And so I sent him like, all my questions are like, is anyone looking into this? Like, how would you go about like trying to update it or whatever?

Lisa Neigut:

And, you know, send it off into the ether. And this was within me starting like at Square within like a month or two of starting at Square. And then, you know, I got busy doing other things. Then Rusty didn’t write me back. So I like, you know, like got into like, so working on a custody wallet, there’s like the aspect of working on Bitcoin. So it’s good to understand how Bitcoin works because your software interacts with Bitcoin as an entity, but anytime you work on a large software project, there’s also learning how that project works in and of itself. So you know, it was like get on the job, learn how Bitcoin works sort of. Yeah. In like a month know that would took a lot longer than that. But like, okay, like here’s kind of how Bitcoin is. And then rest of the job was like, okay, now here’s how we want to change our system or wallet to do this thing.

Lisa Neigut:

I was working on enabling Bitcoin deposits at square for awhile. That was like my project and so like you have to re pipe a lot of the plumbing in order to make that happen. So then like the rest of my time, basically at Square was like figuring out how to like change the square software and didn’t have a lot to do with like Bitcoin itself. But I sent this email to Rusty and then like three months later out of nowhere like, Oh yeah, great question. Here’s some other stuff you can look at. I don’t know of anyone working on this here. Like you should talk to Pieter Wuille about like this project and like, okay, cool. Like I don’t know who any of these people are. I should put that out there.

Lisa Neigut:

I have no clue what I’ve just done. Like I have sent a single email from like, you know, like, okay, cool. Yeah, so then Peter and I like talk a little bit about like different approaches to how you could prevent it from rolling over. And I think the whole thing ended with like, great, let me like write some tests and I’ll get back to you. Mind you, I’ve never run a C++ project. I don’t really know that much about C++, but I was like, sure, I can like download Bitcoin and like write some tests. How hard could that be? I didn’t end up doing that. I got very distracted, but Rusty was like, Oh, you’re interesting. Like we’re hiring for this lightning developer role, would you like to apply to be a lightning developer? And I was very polite.

Lisa Neigut:

I wrote him back a very long email. That was like, you’re all the reasons I am not a good fit for this role. Also, I just started a new job, like, but you know, as I sent him this like long email, like, Hey, really glad you think I would be an interesting person to have on your team. That’s very flattering. But like I don’t know if that works for either us. But he’s like, okay, well just like interview anyways. And I was like, okay. Like I will let you tell me no, if that’s what you want to do. Like, let’s fine, this sounds like an awesome job. If I get it, great. But you know, like, yeah, sure. But they ended up offering me the job. So that’s how I ended up at Blockstream as a lightning developer fell over backwards into it. Kind of.

Stephan Livera:

Very cool. And do you work remotely as well because obviously rusty is a down in Adelaide, you’re in the U.S. In Texas and Christian’s over in Switzerland. How do you guys make that work with, you know, the time zones and everything?

Lisa Neigut:

You know, I’m gonna be honest, it hasn’t really been a problem. At least not for me. Like I think part of it is that Rusty and Christian are really good about responding to stuff really quickly. I think all of us are, so, you know, it’s if someone needs a review on a thing or wants to like get stuff moved forward, it’s really easy to reach out to one of them. The other thing is like, as you mentioned, we’re really far apart, but that means we also get full round the clock coverage. So there’s always someone else around either Christian or Rusty.

Stephan Livera:

Ah, I see. Yeah. Yeah. I guess cause in your afternoon it would be the morning for Rusty and yeah, yeah,

Lisa Neigut:

Yeah. My morning is Christian’s evening and afternoon, so there’s always someone around to ask stuff too. So it actually like, I think geographically it actually like worked out and I think the fact that we’re all pretty far apart is actually very helpful too because there’s no expectation that everyone will be able to like kind of be all at the same place at the same time. Or like there’s not like half the team is all in Texas and always working on stuff and everyone else is perpetually left out. Like none of that happens because everyone is far away. So I also think it really helps us be a very like like I think C-lightning has a very international contributor, like baseline. Our two like other big contributors. I think one lives somewhere in like the South Pacific and then another is in France. We’ve got a couple of people in Europe who contribute pretty frequently. Yeah, I like to joke. I feel like, I’m like sometimes I feel like I’m like the only North American representative. I don’t think that’s entirely true, but it’s kind of fun.

Stephan Livera:

So look, let’s get into some of the lightning stuff. So you were, I guess when we’re talking about lightning, I think most of the listeners are reasonably familiar with how lightning works. You know, you open up your channels, you become part of this network. But what’s actually underlying some of that? What’s some of the cryptography that’s required to make this all work?

Lisa Neigut:

So it’s like so I think like the angle that I was interested in, I have been thinking about when I tweeted, I wasn’t necessarily the cryptography, which is definitely a part of it, but it’s more the kind of just like the way that the Bitcoin so, well, okay. I’m trying to figure out where I should start with this. So the thing that I think is really interesting about lightning and that I find really cool is the architecture of the contracts that are used to make lightning payments. So for, I’m sure most people are fairly familiar with lightning and how that works, but for those who aren’t when a lightning payment gets made you’re exchanging Bitcoin transactions that both parties have signed, so they’re valid Bitcoin transactions. The only difference between lightning and like a normal Bitcoin payment is that the lightning transactions, Bitcoin transactions, you don’t actually send to the Bitcoin blockchain, you hold onto them and this whole, they just become like a promise though that at any point you could go to the blockchain and publish it and get the money out and that promise or like that guarantee that the transaction you hold is valid at any point you choose to publish it.

Lisa Neigut:

Is what makes like the lightning kind of trust model work because you don’t have to trust that you’ll get paid. You have the ability to get paid on chain at any time. And so like money in lightning channels actually like money in lightning channels, like kind of like the broad way that it works. When you open a channel, you’re creating a pool of money with the other person in the channel. It’s just, you can only have two people in this pool. It’s actually kind of a fun analogy I can make between how lightning works and liquid works cause they’re very similar but have like kind of a different accounting metric and number of participants in the pools. But yeah, so it’s really cool because you get so two people come together and decide to pool their Bitcoin resources.

Lisa Neigut:

And so in Bitcoin, like what does that look like? How do you pool resources and Bitcoin? Right? you do that through contracts. You write a contract, a Bitcoin like contract in the smart contract language, I don’t think it’s, I don’t know how you talk about it, but like smart contract language called Script, which is the Bitcoin’s like contract language that we have currently. And that contract is such that the only way that that money can be spent is if you have a signature from each party to that pool of money. Right. These are called multisig transactions. I’m sure you’ve heard of like multisig transactions, right? Except this is specifically like a two of two multisig transaction, which means that both parties have to agree on how that money is being spent. And the way that you agree is by signing a transaction that has outputs that pays money to you and the other party basically.

Stephan Livera:

And then there’s the fallback condition, right?

Lisa Neigut:

Yes. This is what I got kind of excited about. So the whole backstory to this thing is that I’ve been working on adding I’m gonna call them like accounting primitives to c-lightning. So annotating, c-lightning such that when you run it, you get really fine grained accounting details. I was really hoping my PR would make this last, we’re doing, or at least we just cut the RC, the first release candidate for 0.8.2 today. And I was hoping would make it in, but it didn’t quite, for reasons, but it’ll be there in the next release. But it’s really fun. So like part of having to annotate the C-lightning code base and the cool things that’ll let you do is like, okay, how much did I pay in chain fees for this channel?

Lisa Neigut:

And you’ll be able to answer those kinds of questions. Like what were my routing, how much did I make in routing fees like where’s my capital allocated? Like you could get like a balance sheet basically. So like basically it’s generating the data that you would need so that you could have a like balance sheet of where all your money is currently in your like node basically. Which is cool. So it’s kind of like building this like kind of nice like ledger of movements of money through a C-lightning node. But in order to do that, you have to understand where all the money is and all the places that can end up and all the edge cases in which you end up going to chain and where the transaction fees go and stuff. So one thing that I thought was really interesting is like, so the hard part about the really hard part with accounting and C-lightning payments, and lightning channels just in general is the failure case, right?

Lisa Neigut:

It’s not so much like the failure case, like so there’s like different tiers of how a channel gets closed. So you know, you open a channel with another party, which means that both of you agree to put money into a Bitcoin contract and then that contract goes to chain and is like mined and becomes official like canon, right?

Stephan Livera:

Like the funding transaction.

Lisa Neigut:

Yeah. And that is like public and you tell people where it is, they can look it up and confirm how much money’s in that channel. It doesn’t tell you how much is in each party’s balance, but it tells you the capacity of that channel. Right. And that lets you help. That helps you make routing decisions when you’re looking at all the different routes. You know, what the total capacity is. Anyways, that’s like a whole different conversation. But the like, yeah.

Lisa Neigut:

So you have like this, you have this transaction and then at some point you want to get your money out of it. Right. And so we call that the closing transaction. There’s like there’s three different types of closing transactions that you can have. There’s the happy case, which is like we call it the mutual close and that is where you and your buddy, your channel partner that’s in the shared pool with you are both online and both of you are still talking to each other, like still friends and you both agree about how much money each person gets and you both agree how much fees you’re going to pay for this closing transaction. Right. Cause there’s like a fee rate which changes, you know what a good fee rate is, changes depending on how long you want to wait for it to get confirmed.

Lisa Neigut:

So anyways, you come to an agreement about how the money in this channel is split up and how much you’re paying to get it on chain. That’s called the mutual close, which makes sense. You mutually agree to close it. And those transactions are pretty simple. You, there’s like a back and forth exchange where you figure out what the fee rate is. And then you both exchange signatures. Once you’ve agreed what the fee rate is and what the outputs look like. You exchange signatures and then one or both of you attempt to broadcast it to chain and then then you’re like over, it’s done the money’s back and in your control fully now. Right? Okay. So that’s like pool exit one usually pool exit two is called unilateral and that means that like the other side fell off the edge of the earth and you can’t send money because you need them to be online to sign new transactions, right?

Lisa Neigut:

Like this like relationship that you have requires both of you to be in communication and available to make updates to the balances so that money can move through it. But if for some reason they stopped responding or they fallen offline you don’t, your money is stuck in that pool, right? You need their agreement generally to get your money out. So you part of starting a channel is you always have a valid transaction that spends the funding transaction. And you just publish the one that you have the last version that had like maybe I have like, I don’t know, 50,000 sats in the channel and you have 70,000 sats and that was where we last left it. I have a copy of that transaction that pays out to me 50,000 sats and then there’s another output in that transaction that pays out to you 70,000 sats.

Lisa Neigut:

And then so I just like publish that to chain, right? I didn’t talk to you about it, we didn’t agree on what the fee rate is. Maybe we signed it three months ago cause that was the last time money moves through the channel and the few rates super outdated. So it takes forever to get mined. And there’s like, so there’s a lot of kind of problems around these. These are so this, these transactions so this strategy of closing without talking to you to get like updated one is called the unilateral close. The transaction that I’m publishing is actually something called a commitment transaction. I don’t know if that’s important, but maybe, maybe that’ll ring some bells for some people. So unilateral close is a publishing of a commitment transaction you have. And there’s actually kind of a these are like way more complicated and this is where like the cool and interesting architecting of like Bitcoin scripts comes into play is in how these commitment slash the unilateral close transactions have been architected, so to speak.

Lisa Neigut:

And what’s cool about them is that there’s like the third case, so I said there’s like three cases. The third case is actually the same as a unilateral close transaction and that someone is publishing an old, a commitment transaction that they have. The only difference between a unilateral and like a penalty case is that they’re publishing an old version. It’s like an old commitment transaction. And this has to do with like how lightning, the balance update is that I signed a new transaction and then send you a new transaction. So every time that money moves through the channel, we get a new commitment transaction that records the latest balance information for that channel. If I go back though and I find one where I actually have 100,000 sats and you only have whatever, 30,000 sats, right?

Lisa Neigut:

But it’s like three commitment transactions ago and then I paid you some stuff out. Maybe we went and got lunch or coffee and I owed you some money. And so like current state you have 70K but back in the past I used to have a 100 K so I want to try and get that much. I want to cheat you man. I want, I don’t know, I want the money so I will publish. Maybe it’s an accident to this. We’re trying to make it, you know, sometimes accidents happen, but if I for some reason publish an old commitment transaction and it’s old because there are like new versions have been issued sort of, or we’d like signed new versions. There are special cases built into that transaction that let you, my channel partner come along and take all of the money out of the channel in the pool and pay it out to yourself.

Lisa Neigut:

And there’s, there’s a couple of ways that that happens. Like, so these commitment transactions that you use for the end up being used and unilateral or penalty close cases, they have like time locks, they have like time locks built into them such that, and the reason for the time lock is so that you have time to see what I’ve done publish the transaction and come along. The secret revocation key is we call it and take the money out before I have time to spend it in a second transaction and actually kind of claw it back for myself. So yeah, so they’re like commitment transactions or are they bigger? I guess this, no, they’re not any bigger anyways. It’s like, are they, I don’t think they’re bigger than mutual closes. They’re way more complicated though. So that’s like, right. Okay.

Stephan Livera:

Yeah. So, I guess that’s the let me just kind of summarize that and make sure listeners can follow along and also confirm my understanding is correct. Right. So hypothetically, you and I set up a channel together when we set that up. That was a funding transaction that is a 2 of 2 multisignature, but with this fallback pathway where if one of us goes offline, the other one has a pre-signed commitment transaction, but not yet broadcast that they may broadcast to the chain at any point.

Lisa Neigut:

Exactly.

Stephan Livera:

And then the mutual close scenario is where we agree, we’re both online. We’re saying, yep, this is the correct truth of the world, or this is the correct state of our channel. We’re going to close it this way in the let’s say one of us went offline, then the other one has the pre-signed commitment transaction that they may broadcast to take to claim the money back on chain.

Stephan Livera:

And then the final one is the justice transaction or the breach remedy transaction where one of us has tried to cheat the other, or one of us had a failure in our backups or whatever. And you can, you one of our nodes was watching the chain and saw, Oh, Hey, I’m being cheated, let me broadcast my justice transaction and set the balance correct. Or set the, set the record correctly rather than let they saw the guy’s fake or wrong commitment transaction be the one that gets confirmed into the Bitcoin blockchain. Would you say that’s kind of broadly the right understanding there?

Lisa Neigut:

Yeah, except so when you’re saying so I think the only thing I would like kind of want to maybe clear up a bit is so the cheat penalty thing is still a commitment transaction. It’s just not the most recent one. Right. So it’s kind of a similar thing to the most, if you publish the most recent one that’s called, like that’s the unilateral case. If you publish the not most recent one, you end up in like Badlands where like, yes, then your peer would publish, which you were calling the justice transaction. But then it actually happens after I’ve messed up and sent the.

Stephan Livera:

Right. You tried to send an old commitment.

Lisa Neigut:

Right. I did, I succeeded in sending an old commitment to chain. The thing about the justice transaction though, and so this is actually an interesting difference between the current way that lightning channels work. I believe they’re called inaudible channels is what we just described. There’s a, a new update proposal, that Laolu, Christian and Rusty, I think they’re called, it’s called eltoo channels. And the eltoo channels actually let you publish a new transaction that actually corrects the state on chain. So if I publish my a 100K transaction, you would just have to, you would have to publish a transaction, but the transaction, you’re publishing updates the balance on chain so to speak. So there’s no actual penalty in eltoo channels. It’s just the guarantee that the final state is correct. You’ll always be able to get to the final correct state. And that requires some fancy new script stuff, which we don’t have currently, which we’re kind of, so that like is sort of behind that. The thing about penalty transactions is I actually lose all of my money. So it’s not like justice, restoring justice and making it back to what everyone had agreed on. The current state is right. It’s actually justice. Like, no, we’re penalizing you. You are like losing everything. Like game over like nice try. Yeah. Which is interesting. Anyways.

Stephan Livera:

Yeah. So I guess the next point then, let’s talk a little bit from, you were mentioning around accounting. So I guess from an accounting point of view, we’re thinking, okay, so I’ve got my balance sheet. You might think of it like I’ve got, you know, these are the channels that I’ve got open, but then you might also think more like, okay, what’s my income statement? What is the fee revenue and so on. So maybe let’s just start with the balance sheet or kind of the, what channels do I have open from a C-lightning point of view, what does that look like when you say have 10 channels open and, you know, can you explain a little bit around that part?

Lisa Neigut:

Yeah. yeah, it actually, I think it would also be, I think so is that, I think another interesting thing to talk about with accounting is now that we’ve kind of talked about how penalty transactions work is it’s actually an interesting question of how you treat the accounting around penalties, but we can get there at like a little later. So I haven’t actually, so the work I’ve been doing is actually kind of like, I would almost classify it as like an annotation thing. So it’s basically like when you build, okay, so like in accounting, when you have like your income versus your balance sheet, right? Or cashflow statement those are all like roll-ups of a lot of underlying data, right? So like in general accounting, like you have your journal, like your double entry ledgers and stuff maybe your credits and you have your debits and every single transaction that gets made usually has like you put an entry in two columns so that your whole thing kind of like weirdly balances out.

Lisa Neigut:

So all of that like, so in accounting there’s like all this transaction level data, right? That’s like, Oh, I bought lunch, that’s an expense. Or Oh we invested in some opex or capex by buying this machine. And then we’re gonna like do the depreciation over like five years or 10 years, whatever, depending. Anyways, there’s rules and accounting things. But all of your accounting book data is the line by line transactions of what happened and where you spent your money. So the project I’ve been working on is to create that ledger for a lightning node. I still need to work on to be done project that is like the actual plugin, then that sits on top of that, that that would give you these balance sheet and cash flow statements about your node so that like you need all this like annotation work done for the building block. Exactly. Yeah. But it would be like, I dunno how easy, it should be pretty easy that once you have all that data, which is cool cause then you will be able to see like where all your money and stuff is.

Stephan Livera:

Yeah. I mean as a quick example, I’m just thinking now. So, for example, let’s say I open a channel with you for whatever, 5 million sets, right? And I pay an on chain fee for that, right? And so that would go into the cashflow statement, right? To say Stephan incurred an expense to open this channel with Lisa. And then the, you know, then you would start thinking, okay, this is the channel I have open. And then once payments actually start routing through that channel between you and me, or let’s say someone is multi hop routing through me to you, et cetera, and I’m charging fees and so on or you’re charging me a fee or whatever, then those components also have to get added, counted together and built up so that I can start building my accounting position on what was my income.

Lisa Neigut:

Exactly. And it gives you a good idea of where your deployed capital in your channels is earning your revenues. There’s actually like, so one of the kind of like, difficulties with the ledger data that I’ve built not a difficulty, but something that I think I’m going to have to think about a bit when I’m building like the next layer up, like the view side of it that gives you all this good information is it’s actually like how you account for routing fees is actually really interesting. And the reason that it is like, so the reason that accounting fees are like, or accounting for routing fees are interesting is because they don’t happen in a single channel. The view of how much money you’ve made is actually the difference between two channels. So you make money, which is so like when, so let’s say like, I’m sitting in the middle of a transaction and you’re routing money through me to someone else, like over here you’re gonna pay me and let’s say you’re paying them like, I don’t know, a thousand sets.

Lisa Neigut:

I’m gonna make 10 sats in routing fees. I don’t know what percent. That’s like 1%. Yeah, 1% routing fees. Okay, cool. So you will pay me a 1010 sats, right? And then I will pay your friend a thousand sats. So on a ledger basis, we’re just counting money movements. So in the ledger, all that you will see is 1010 in and a 1000 out. The routing fee information, like the routing gain or like money that I have made, your profit is the difference between those two balances. Right? So that’s not actually, it’s like, at least in the accounting stuff that I’ve like that I wrote in to c-lightning, we’re capturing just the movements because that’s like more, I don’t know that that cause that’s the actual transaction that happened. Right? Like the actual transaction that happened is that you sent me 1,010 and then I sent a thousand here.

Lisa Neigut:

So that’s how like the channel balances then, right? Is it ten thousand moved here and then a thousand went there. But the difference between those two is the routing fee that I’ve gained bitcoin sats. So the like, so this like next layer piece that I’m going to have to write is going to have to take that into account. The cool thing, so like the interesting thing about that then is that routing fees aren’t a, it’s not a single channel that earns you routing fees so much as like channel pairs, which is cool. I haven’t figured out exactly how to represent that. But I think there’s some interesting stuff you’ll be able to do to kind of figure out what are the good like what are which routing peers or which channel is more making you more money than the other rate. So it’s like deploying your capital into channels is more of a network strategy than it is like a single channel though. It might be a single channel that connects to highly connected nodes or something. Right? That yeah.

Stephan Livera:

Right. And I guess if you are in a, I guess the hypothetical node that only has one channel the only, then you’re only, I guess you’re only paying fees or I guess receiving, if somebody’s paying you, right.

Lisa Neigut:

You won’t get routing fees though cause you can’t route if you only have a single thing.

Stephan Livera:

Okay. So hypothetically, let’s say you and I have a channel and I only have one channel with you, but you’ve got other channels elsewhere then it only means I can’t receive, I’m not making any routing fees at all, I’m only ever paying routing fees in that example.

Lisa Neigut:

Exactly right. Yes.

Stephan Livera:

Yep. And so another point I’m curious to ask your thoughts on, I’m sure you’re aware of RTL. Now I did an interview for listeners earlier with the Suheb. RTL is a dashboard that supports both LND and C-lightning. And I noticed they have a routing fee report as well. So you can say, okay, I made 10 sets this day or this. How does what you’re doing compare with what they are doing?

Lisa Neigut:

Yes. So c-lightning already has see lightning accounts for routing fees for you already. And so if you have a C lightning node, I can’t remember exactly which, I think it’s like list forwards is the command. But it’s possible to get a report out of C-lightning that tells you all the rounding money that you’ve made. I think it’s fine grained enough that you could do the channel analysis as you would want. So like I think that that’s like, I’m trying to say like, yeah that’s information that we’re already providing to people and they can already do interesting and cool stuff. Like if all you care about is like, but that’s only if all you care about is routing profits. Right? So the sort of stuff that I’ve been writing, like the ledger stuff is more of like I need to see my books.

Lisa Neigut:

Like I need to see where my money is like on and I need to see where it’s moving. And it’s, it’s more of a it’s more of an audit level information system than, so like when you think about like data and information flows through a system, like C-lightning or like anything there’s two kind of views that you can kind of take on it. There’s like one that’s like present state and kind of keeping, I guess we sort of, well that’s sort of, there’s like present state, right? And so like C-lightning keeps track of the current channel balances. I don’t think we keep like the historical channel balances though, right? Like, so that’s, you lose a lot of data about what the interactions and transactions have been. Any invoices that you have coming in, we saved the for a certain time, but at some point you’re probably going to clear them out. Right. I was like, C-lightning as a system is not meant to be a historical record of where all the money has gone and where it’s moved. So the system that I have built is a way that it’ll export all that data or that you can capture it like a stream of it as it happens and then we can get like the whole picture of what has happened external to the system, so to speak. And routing fees are one thing that you could find from that.

Stephan Livera:

And so I guess you could figure out a historical balance at a certain point in time. Okay. Based on the history record logs, I had a balance of whatever, 500,000 sats and whatever, right.

Lisa Neigut:

Yeah. Yeah. I don’t know. It’s just a different way of looking at similar data and capturing it in like a different way. I don’t know. So the thing I wanted to get back to you though is so there’s this really interesting question in accounting about what happens when a penalty transaction happens. Right? Okay. Why is that interesting? It’s interesting because let’s say that like, so this like ledger that we have, right? We’re writing down every time money moves one direction or the next. And then a penalty transaction is like rolling back to a previous state, right? So like these transactions there still happened, right? So it’s like, okay, so there’s like what did we do in this situation? Technically we’ve either gained money if we’ve, if we’re the sending out that, as you called it, the justice transaction and clawing back all of the money.

Lisa Neigut:

So either we’ve made some money that we didn’t actually earn someone else fucked up or tried to cheat us, but we like, we have like clawed all of that money. So now we, so now magically we have more money than we started with. And that isn’t new balance, right? Like what do we do with that? Well that’s interesting. I dunno. Or we accidentally published an old transaction or maybe we tried to cheat. But now we have, we used to have a balance in this channel and now we don’t, it’s gone. So like the way that I like chose is kind of you kind of, well it’s not anyways, the way that like, C-lightning will handle this is we do something called like a journal entry that’s just like, Hey, you lost money. Or maybe I call it like a penalty of like you tag them.

Lisa Neigut:

But the whole thing is, the whole idea is like all those previous transactions that you had, like let’s say you’re running a business over your lightning node, right. And a lot of the money that’s been flowing through that channel with like payments you’ve received for goods, like you’re selling, I don’t know, hats over lightning. And so you need, you still need all those records of all those hats that you sold, right? You still need you and you’ve sold them. There was like evidence of like the money moving, right? Oops. but like so that all still happened. That doesn’t change because you lost money, you’ve just incurred a loss now it’s like someone stole the piggy bank, right? So all that happens, at least in the journal entry ledger thing is you get a new entry that is like, you lost X amount of money, I’m sorry. Or Hey, you have just gained like 500,000 sats. Congratulations. You know minus whatever chain fees that you end up paying into that. But yeah,

Stephan Livera:

Let’s talk a little bit about the fees that you pay for closing a channel because that’s also another cost that you pay. And that’s also a bit of a negotiation aspect, right? Because we have to like figure out what fee rate you and I want to pay between for this channel that you and I have for example.

Lisa Neigut:

Yeah. This is actually, so this is a really, so this is cool because it’s something we’re currently working on and I believe the lightning labs team has, is it going out in their next release? So there’s, okay, so the fees problem is a real one. The fees problem for like the mutual close that we talked about earlier is not actually that, I don’t know, I’m gonna call it hard of a problem, but and you, it takes some time for you to figure out a mutually agreeable fee rate, but you can do it and it’s fine. The harder thing is like those commitment transactions that you use for like the unilateral or the penalty case. The problem with that is like if we signed a transaction, so like what if the last commitment transaction I have for you is three, a long time ago and the fee rate has like 10Xed since then.

Lisa Neigut:

I’m kind of in like a difficult position because I need that transaction to get, so I believe the way that, so the way that the time to like there’s time locks on my ability to spend the money in that commitment transaction and that timer, my understanding is correct. I believe this is true. My timer doesn’t start until that commitment transaction gets mined. So I can’t actually create a like child. So like the typical way that you pull through transactions. Well there’s two ways you get transactions that have low fee rates mined, right? One is replace by fee which is where, but that requires a recreation of the transaction, which would require your peer to be online. And as we’ve just discussed, they’ve disappeared. That’s not an option. The other option is called child pays for parent, but in order for that to work, it requires an output on the transaction that I can attach a valid secondary Bitcoin transaction on to.

Lisa Neigut:

And both of these can go into the mempool at the same time. The problem with the current commitment transaction is that the one output to me, the one that pays me, my channel balance is time locked, which means that I can’t get a child transaction for that output into the mempool cause it’s invalid until that transaction has been mined for like X number of blocks, however many let’s say like nine blocks. So you kinda just have to like public, you push out your commitment transaction and just hope that it works. Right. just been working mostly fine. But lightning labs team has been working on a proposal called anchor outputs, which will make it a little bit easier to get stuff mined. Because it makes it such that there is always an output that I can spend me as like the person publishing the transaction.

Lisa Neigut:

Yeah. And that’s like, we can talk about that if you want, but yeah, it’s interesting. It actually like, so that actually, and this is like, Oh, actually I went back and forth with lightning labs team a little bit. I promised them I would do some more, sorry I’m like trying to sit down. I promised them I do some more analysis and I have it on my like to do list, I was trying to get like our release out, but they’re actually like considerably more expensive in like a very certain cases. Than anchor outputs are. And part of the reason I think I did like a very naive calculation that they’re like 5X more expensive than like a very cheap which is a lot like if you, depending on how big your channel is, like 5X. So that was like, I don’t know, maybe like a thousand sats.

Lisa Neigut:

Cause like right now it’s like maybe 200 anyways. Like it’s expensive, it’s like a lot more expensive in like certain cases to use the anchor output stuff because it requires more outputs and you have to put sats in the outputs so that that’s more money that you’re paying to get it done. And then child pays for parent actually in the net aggregate increases the number of bytes that you’re trying to get mine. And since you paid by byte-size you pay per byte rate, like that’s what the fee rate is. You are spending more because there’s more bytes to be mined because you need both the original transaction plus the child transactions that are pulling it through. So child pays for parent is more bytes, which means it’s more expensive just by nature of whatever. There’s some cool stuff that they’ve added that we didn’t talk about them at all, but there’s like this really cool sub genre of like topics around commitment transactions called HTLC transactions. Which we probably I don’t think we have time to get into that. But the cool thing about those is, so the cool thing about the anchor outputs is that it actually helps decrease the cost of this like other subsection of transactions you have to pay for in some cases anyways.

Stephan Livera:

I see. Yeah. So you’re talking there about the, the routed parts, the HLTCs as opposed to the like direct payments. Is that what you’re saying?

Lisa Neigut:

Yeah, HTLC’s we didn’t talk about these at all. It feels, these are like how money moves through the system, but it’s, take me awhile to explain it. I think. I don’t know.

Stephan Livera:

Sure, sure. Do you want to talk about Dual Funded channels now?

Lisa Neigut:

Oh, we can definitely talk about that. That’s like a totally different set of stuff for sure. We can definitely talk about it. Oh my God. Yeah. Let’s talk about dual funded channels.

Stephan Livera:

So why would we, why would that be a good thing?

Lisa Neigut:

Okay. Yeah, so I think that cool. So I’m going to start with like current state of lightning is that when you open a channel, there’s two nodes and they’re making a single pool that they put their money into. But only one of those nodes has the opportunity to put money in the pool. So this means that when you open a channel, only one person can send payments through at the start. And in order for it to become like operational for both sides, the person who opened it would have to send payments through it before the other side can send stuff back. Lightning labs got around this restriction by allowing more than one channel between two nodes. So if I have, I can open a channel to you and put money in it and then I can send you money that way and then you could open a second channel to me and send money that way.

Lisa Neigut:

This is kind of inefficient because it takes two transactions. So you’re paying the channel fees, you’re paying chain fees, you know, chain fees to Bitcoin miners. You’re paying fees twice both to open it and then you’re also going to end up paying fees to close it so your fee burden gets bigger. It also increases the amount of gossip in the network because every new channel that’s created creates at least, I want to say five new gossip messages. So it’s inefficient cause there’s just more gossip creates like two X the gossip that you would need. Also, it makes it such that your your bandwidth is like split. So if I wanted to put 100,000, like a million sats into a channel and you wanted to also put a million sats into this channel between us at some point, let’s say someone wanted to send 1.5 million payment through us, and technically we have 2 million worth of capacity, but it’s split between two channels.

Lisa Neigut:

You need a secondary mechanism then in order to send that payment through these split channels, which we’re getting with like multipath payments. But it’s just not as like your stuff’s like a little, I just, I don’t know, I just, I think it’s a little less efficient. So the solution to allowing nodes to create channels that are, one solution is to allow at the opening when you’re creating the funding transaction to allow both parties to that transaction to contribute funds. So that’s the whole, that’s the whole thing that’s like, that’s dual funding. Both people can put inputs into the pool at the start.

Stephan Livera:

Yup. And so what are some of the difficulties around achieving that? Like, what’s the – you know, is that a way for you to try and find out all my UTXO if if you just try and spam it out to everyone and say, Hey, I wanna open a channel with you, show me one of your UTXOs, and then actually you just like run off and say, aha. See, now, I know information about you on chain.

Lisa Neigut:

Yes. That is definitely one of the biggest, I think pieces of pushback or like feedback we’ve gotten from like, you know, just people in lightning about the proposal. There’s some, there’s some stuff we’ve added to the proposal that I think really reduces that a lot. Let me try and like, okay, so the the proposal that we’re kind of like working with now, or like the most recent thing actually comes from JoinMarket, I’m going to get that wrong. The PoDLE of stuff. Yeah. Or poodles or whatever they’re called. I guess I get to decide if, no, I don’t know. I think waxwing gets to decide. But the, so the PoDLE stands for proof of discrete log equivalence. And the basic idea behind it is that it proves to someone to like in an open channel negotiation, there’s always two parties.

Lisa Neigut:

The opening party will approach the other person and be like, Hey, I would like to open a channel with you and the other person, like, great, tell me more about what you would like to do. Like, tell me more about the situation. I’m listening. And then the person who’s opening it at this point would prove to you that they have a UTXO. That they can spend and that only they can spend by giving. They give you like this proof and it’s like, is that a hash? I think it’s a hash. Is it a point? Maybe it’s a point. It’s a hash of a point. It’s a hash of a point. They send you. Like basically they send you like this proof that at some point in the future you will be able to verify that. It means that they have the private key to spend a UTXO.

Lisa Neigut:

You don’t know which UTXO it is. You don’t know what the private key is. All you know is that they can prove to you that they can spend a UTXO so they send that to you as part of the opening negotiation and then you’re like, okay, well you’ve got a proof and cool, okay, yeah, let’s do it. And then so then they send you, so then like you’re OK like, let’s keep going. Great. then they send you the information about that. UTXO so this is the opener, right? This is a person who decided they wanted to open the channel. They send you the information that they have about that UTXO which allows you to go and verify that the proof that they sent you is correct. And the proof is that, that they can spend that UTXO.

Lisa Neigut:

It has to do with the way that the proof of discrete log equivalence works. But basically the only way that you could create the proof was if you had access to the private key that, that, UTXO is also locked to. And you can prove that, you can figure that out and make sure that they have the private key. Cause if they didn’t have the private key, they wouldn’t have been able to produce that proof of discrete log equivalence. So this does two things. This makes it such that the only way that you can create a dual funded channel is if you have a UTXO that you can put into it and you can prove that you have a UTXO. So in order for someone to get my UTXO information out of me, they would have to have at least one UTXO somewhere.

Lisa Neigut:

Right. The other thing is that, well, okay, there’s like a little bit of verification so I can like kind of check that they at least know how to make a PoDLE. The other thing is that those PoDLE then becomes something that you gossip around that you send out to the network and they get gossiped. And so when someone sends you a proof of this gate log equivalents, you can look through the backlog of all the ones that you’ve gotten from every other node and see if they’ve tried to use it on any other node before. So that kind of makes it really hard. So, okay, let’s say that you wanted to get UTXOs out of like a bunch of nodes, right? So you create a single proof of discreet log equivalent and you send it out to everyone. In theory they’re gonna get it, they’re gonna send it out to all it’s everyone else on the, and you’re going to see that it got sent out. And so you’re going to be like, eh, okay. So I see you want to open a channel, that’s great. You can open the channel. I’m just not going to put anything in it. So

Lisa Neigut:

This is the kind of so like the failure case here is that the channel still gets opened. The person who wanted to open the channel can still open it. But basically it gives the other side this like opportunity to opt out of providing any information of their stuff. And that’s the cool thing about like dual funding is that there’s no requirement that both sides put money in. So if something goes horribly wrong and like your PoDLE gets broadcast everywhere, you could still go to another channel or another node and use that UTXO to open a channel, you just wouldn’t be eligible to have the other party put money. The failure case, in this is like status quo.

Stephan Livera:

Yeah, that’s pretty good. And so I guess, what this is achieving is also stopping somebody from spamming it out to everybody because if they’re just trying to spam it out to everyone, the other people will say, hang on, you already used that one before. Either do it, pay the cost to create a new UTXO. And do a new PoDLE. So basically it’s like an asymmetric defense thing. It’s like a, it’s forcing additional cost onto the attacker who wants to try and figure out all what’s everyone’s UTXO. Right.

Lisa Neigut:

Exactly. Yeah. Yeah. It makes it costly. Yeah.

Stephan Livera:

Yeah. That’s pretty cool. And a couple other things here. I think I was reading some Bitcoin Optech on this and there was some discussion around what values for the free parameters in the transaction. So these are like nVersion and nSequence and nLocktime, input and output ordering. Could you discuss a little bit of that around what’s the implication there? Why would we want to try and align that in the way that you know, people are doing these transactions?

Lisa Neigut:

Yeah. So this is like, so what you’re talking about I think is the, so when you create, so the opening transaction is a transaction that two parties are both constructing and they’re both constructing it kind of. So one thing that you do when you create protocol design, as you try and minimize the amount of information that you have to exchange with the other party the reason for that is it’s less stuff you have to send over the wire. If there’s like a bunch of conventions you can agree upon before or like that or just kind of generally known then that’s less things that you have to communicate about. And so it makes it just more efficient. This is also why so one of the ACINQ contributors, their name is escaping me right now. One of his big questions when we started working on the dual funding proposal is why don’t we use partially signed Bitcoin transactions?

Lisa Neigut:

So PSBT’s, totally valid question. The reason that you wouldn’t want to do that though is that as a like, so PSBT’s, are great for I think like, so PSBT is really filled a much needed gap of wallet to wallet interaction. So it became like the, when you have like two Bitcoin wallets, how do those wallets interact with each other? And PSBT became the like universal standard of how wallet to wallet interaction happens. And I think that was like super needed and is great. I’m really excited about getting PSBT into C-lightning. It’s coming I promise. But like the what do you call it? So the, but for over the wire communication in a scenario where the sort of transaction that you’re trying to create is fairly well known as like a user’s like parameters around what you’re trying to create together. Having that much information, having to be sent across the wire. It doesn’t make sense because we were in a situation where we are designing exactly what we can like we can come up with things like, Oh the nSequence inaudible will be exactly like this. I don’t remember what we decided on. I think, I think like we decided like, so lock time anyways, lock time, we’re going to mimic what Bitcoin is doing so that it’s less or Bitcoind is doing anyways.

Stephan Livera:

Right. So it looks more closer to that kind of transaction. And I guess part of the argument there is around yeah, assuming we do get Schnorr Taproot that when you do a mutual close that that would be indistinguishable from a standard Bitcoin transaction. And so the idea is to try and make all of the other bits and pieces about that transaction the same such that it’s not giving off a fingerprint that Oh, Hey, this is actually a lightning close. This is not a standard Bitcoin transaction.

Lisa Neigut:

100%. Yeah. And so we’re trying to apply as much of that as possible to these opening transactions also. Yeah. And then like, so the sequence thing, one of the things we want to do with the new opening transaction, so opening transactions you can actually allow for RBF because assumingly your person you’re talking to is online cause they have to be in order to do the opening thing. So you know, the sequence number would need to be such that RBF is enabled. I think that’s like the limit of that though, I think anyways, but rate, so you write these things out into the protocol and then when you’re creating a transaction, you don’t have to communicate them because you already know exactly what they are.

Stephan Livera:

Yeah. Also curious, I’m not sure if this is anything you’re directly working on, but around hardware wallets opening the lightning channel and then closing it back into your hardware wallet. Did you have any comments to add on that?

Lisa Neigut:

Yeah, so this is stuff that I sort of worked. Yeah, I did. I did all that. Did I do, I think I did all that? Yeah. Sorry. I don’t know. The, right, so this is like, this is definitely a goal of c-lightning.

Lisa Neigut:

Two things I think that we, in order to make this a reality the first thing is, well, do we really need PSBT I want PSBT stuff for hardware wallets. I don’t know when everyone’s like hardware. Well, I don’t, I guess we’re going to get PSBT. It’s gonna be great. The second thing that we want that I think we really need in order to make this like work really well is we need to get script descriptor support into C-lightning. This is like Andy Chow’s project that he’s working on. I believe that Bitcoin, the, I dunno if this stuff has shipped yet, but there’s like this really cool stuff you can do with like script descriptors that allows you to basically like create, it’s basically like, so the problem with payouts to hardware wallets currently is that it’s hard to define like, I mean it’s not that hard but like the way that you at least upwards the, so like, okay, so like the simplest case would be that you provide a single static bitcoin address and every time that any money got paid back to the lightning nodes, c-lightning node, we would actually pay it to that address.

Lisa Neigut:

That would be like the the easy way to do it. The problem with that is then every time that you publish a transaction as the exact same address on that, so that’s like not good. So at some point you want to use like the hierarchical deterministic wallets like HD wallet thing. The nice thing about script descriptors is that allows you to kind of get like this, it allows you to create interesting scripts to send to in your hardware wallet. So maybe you want your hardware wallet to be sort of vault like. So every time money comes out of the C-lightning thing, you want to send it to a script, which is more like, right, for example. Or maybe it’s like your cold storage, whatever script descriptors, let you kind of marry the description of the script that you wanted to get paid to with like the hardware descriptor functionality.

Lisa Neigut:

So you could tell C-lightning, this is like the script descriptor for these kinds of transaction outputs. And then we would be able to slot like the next iteration in that like path plus the script that you wanted as what you pay out to. I see what you think that’s like, I think that’s like the goal. Like, I think that that would be, I think that that’s like the gold standard of what you should want for a C-lightning hardware wallet or external wallet integration is like a script descriptor that you can provide for various like close cases or whatever, maybe every close. Cause that lets you like use cool scripts, cool scripts, like not basic pay to whatever scripts. So it gives you the flexibility you might want and like an off wallet, whatever. Or off chain cold wallet thing as well as like the rotation that you would need. So,

Stephan Livera:

Okay. So let me see if I can summarize that. I’ll hopefully I understood that. So we can think of it like the output descriptive work that Andrew Chow is working on in Bitcoin core. You can, you might have a certain derivation path that you wanted to come into. And you might have a certain script type that you want it to be right, or might not just be a single signature script. It might be a multisignature and you want, you might want it to be because it’s like you’re not necessarily like when you pay into an address, you’re also kind of like paying into a script that may unlock it. And if you had a more complicated cold storage set up, like let’s say this is a business who’s running C-lightning and they have a two of three multisig with a certain derivation path that they want to receive. So whenever they close a lightning channel it would go into the next index number up on the derivation path for that two of three multisig is that if I understood you correctly there?

Lisa Neigut:

So like I might slightly have if I’m 95% sure. That’s how these descriptors work with the path kind of thing. I think. I’m pretty sure. Cause then that’s how like yeah cause I just set one up on like my Bitcoin wallet that lets me, like I said, get me the next wallet thing and it sends me the next one based on the script descriptor that I have. So

Stephan Livera:

Right. It increments it up one further and it takes out, okay, this is the address to spend into. And then C-lightning when it does to channel close, we’ll spend into that address and then boom, off you go. Now it’s in your hardware wallet or whatever your cold storage setup is.

Lisa Neigut:

Yeah, but you need the script descriptors though because it acts like, so I was talking earlier about PSBT acts as like the interface between wallets. Like you need that as the interface between what you’re going to expect to get out on the other wallet side.

Stephan Livera:

All right. Any other cool things you wanted to tell us about? You know, C-lightning or the lightning spec that you’re looking at?

Lisa Neigut:

Yeah. okay, so I guess briefly before we go. And so there’s, so I think like there’s two things I’m really excited about aside from dual funding cause I get excited about that. But there’s two things that, other things that I’m excited about that are going on in lightning right now that I think are worth paying attention to. The kind of category that like one of them is like usability and the other one is privacy. So usability one is I believe so lightning labs just published the spec for something they’re calling LSAT, which is what I think is, I put this in like the usability category at what I think is really cool about it is it marries, HTTP with lightning payments and it does it really elegantly. And so they’ve got a really great like web native, interface or like protocol that they’ve designed that lets, web developers take advantage of lightning payments.

Lisa Neigut:

And I think it’s like the really important path forward for getting making it such that web developers have like this, like common language that they understand that they can like code to for integrating with lightning payments systems. So I think it’s awesome. I’m really excited about it. I don’t know when it’s coming to c-lightning. Hopefully soon, like gotta get some stuff shipped, but hopefully it will get that done. Cause I think it’s just incredibly, I think it’s really great. The other thing that I’m really excited about is that privacy improvement. It’s the blinded path projects that t-bast, bastien teinturier and rusty from C-lightning. So that’s the ACINQ team, C lightning team I’ve been working on. What’s really cool about that is that when, so right now when you share an invoice with someone it exposes who the destination notice.

Lisa Neigut:

So there’s services like I think like Jack Maller’s Strike wallet I believe requires you sharing your invoice with like a central server. And like, so ACINQ is interested in this problem because they tend to do, I think, similar stuff for their Phoenix stuff. I don’t, don’t quote me on that. I’m not hundred percent sure. But what’s cool about blinded paths is it allows you to create invoices where the investigation is blinded. So you can’t tell where that payment is going to. Which allows you to like to, it’s good for two reasons. One, it keeps your information private, so no one knows you’re paying. The other thing that’s good about it is that it it makes it such that these payment services like the strike thing that Mallers has been working on does it have any, so if the government came knocking on their door and said, “Hey, we would like to look at all of your information” they legitimately don’t have any valuable information to give you because you never gave them any valuable information.

Lisa Neigut:

Like they don’t have to worry about like deleting all the invoices they’ve ever gotten on a weekly schedule just so that when someone comes knocking, they don’t have anything. They legitimately like just don’t have any information. Which is similar kind of if, I dunno if you keep up with like Signal the messaging app. I think they have a very similar kind of approach to privacy, which is that like, we just don’t keep any information on our servers that we could, you know, we could hand them everything and it would be like nothing. So anyways, so like, yeah. So those are the two things in lightning that are going on right now that I’m, I’m very excited about. Yeah.

Stephan Livera:

With blinded paths. Is that intended or is it related to an alternative to trampoline routing or is it related?

Lisa Neigut:

No, that’s a good question. I don’t know the answer to that.

Stephan Livera:

No worries. That’s all right. Because I understand as I understand, the ACINQ guys were really interested in trampoline writing because it also helps them from the privacy point of view of like them not knowing who you’re paying.

Lisa Neigut:

Yeah. I think you’ve been putting together, right. So you could have a blinded path to trampoline. It’s like a, so like the trampoline, the whole idea behind trampoline, if I understand correctly, is that the idea is that you specify an end destination. So maybe there is some exposure where you’re trying to get exactly, but you don’t know the exact route to get there. So you would send it to a route, you’d send it to a node that presumably would know how to get there. And then you indicate to them where the next place you want to go is, blinded path. I believe you already have to have the route calculated.

Stephan Livera:

I see. So, okay, I got you. So you would still need to, your node still has to have its own view of the network and you know that might be a bit more difficult for a say a mobile, right?

Lisa Neigut:

Yeah. But don’t, well so the blinded path thing is that instead, so with an invoice right now, the path is calculated by the node that gets the invoice. So they do need to have the route graph, the blinded path. You don’t, the node is calculated by the, don’t quote, I might be wrong about this, but I believe that in the blinded path, the route has already been calculated by the node sending the invoice so that the node that gets, it doesn’t have to calculate the path cause they already, they just know it. It’s already included, I think.

Stephan Livera:

Ah, okay. Okay, cool.

Lisa Neigut:

I don’t know the thing about the blind paths that like now that I’m thinking about, I have a question about, I’m not 100% sure is how do you, well I guess you could sign it as I say, how do you know that the node that send it to you, that’s the correct path. Like what if someone like got in a man in the middle of tact and put a different blinded path in there, right.

Stephan Livera:

Pay this one instead.

Lisa Neigut:

Yeah. But I think that, I think that, I believe that invoices are signed like so, it’s signed so you can verify that the data with the blinded path is what the person who issued the invoice wanted. So I think that’s fine. I think you’re covered. That’s nice. But interesting stuff.

Stephan Livera:

Okay, well look, I think I’ve, I think it’s been a very educational chat for me. I’ve definitely learned a bit more about channel accounting. Lisa, where can people find you online?

Lisa Neigut:

Yeah. Great. I am on Twitter @niftynei. Also, I haven’t been switched streaming very much lately cause I’m very lazy, but sometimes I Twitch stream and my Twitch channel is twitch.tv/niftynei. I also run the also not very well updated C-lightning Twitter account. Its @clightningcomit couldn’t get the second m in there, for reasons.

Stephan Livera:

And actually I think you had a good thread on there a little while ago as well, explaining a bunch of stuff in C-lightning. So I’ll include a link for that in the show notes for listeners who are interested. But yeah, thank you very much for joining me, Lisa.

Lisa Neigut:

Great. Thanks Stephan.

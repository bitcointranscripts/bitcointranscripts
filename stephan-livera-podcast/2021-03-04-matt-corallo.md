---
title: Bitcoin Soft Fork Activation, Taproot, and Playing Chicken
transcript_by: Stephan Livera
speakers:
  - Matt Corallo
date: 2021-03-04
media: https://www.youtube.com/watch?v=SY-v2chnS9s
---
podcast: https://stephanlivera.com/episode/257/

Stephan Livera:

Matt, welcome to the show.

Matt Corallo:

Hey yeah, thanks for having me.

Stephan Livera:

So guys, obviously, listeners, you know, we’re just having to re-record this. We had basically a screw up the first time around, but we wanted to chat about Taproot and soft fork activation. So perhaps Matt, if we could just start from your side, let’s try to keep this accessible for listeners who maybe they are new. They’re trying to learn about Bitcoin. So if you could just give a high level explanation, what is a fork and why are we doing that in Bitcoin?

Matt Corallo:

Yeah, Bitcoin is a consensus system, right? So you have a ton of nodes out there. They’re all checking the rules and making sure that every transaction and block and everything completely is valid and passes all the rules, but what happens when we want to change the rules? Right? So we want to add a new feature in this case. There’s some new cool cryptographic features that we want to add to Bitcoin and so how do we change the rules when there’s, you know, thousands of nodes out there that are all collectively enforcing the rules individually, and we want all of those nodes to change the specific rules that they’re enforcing on every transaction. And so this process generally is called a fork and there’s a few different types of forks and we’ll get into a lot of details on what can go wrong in this process. I’m sure. And yeah, so this just generally we kind of do some weird deployment where we try to get nodes upgraded to enforce new rules on the network.

Stephan Livera:

Excellent. And then when it comes to this specific fork that we’re talking about, so it is colloquially, it is known as the taproot soft fork. So can you tell us a little bit just for, from a newbie perspective, what that is and what are the benefits going to be once we get taproot?

Matt Corallo:

Right. So taproot is a nifty cryptographic trick, and also it also brings Schnorr signatures, which is another cryptographic primitive that’s really useful. It’s not going to materially change the user experience of any Bitcoin soft fork, but it can slightly improve privacy, both on the blockchain by having that, you don’t have to reveal all of the details about, you know, if you’re using some kind of complicated multisig policy or something really fancy, you don’t have to reveal all of those details to the blockchain in every case. So your transactions will look kind of more normal, like everyone else’s transactions. Schnorr signatures can be used to improve privacy on the Lightning network. Make it a little harder for nodes, you know, in a route route to tell what the other nodes in the route and kind of, for like, payments across a route. You can also enable some new features.

Matt Corallo:

So there’s some stuff that people have been working on for years. That’s probably not going to be done in the next year or more, but cool things around that. So there’s a technology called discreet log contracts, which focus on bringing kind of more complicated financial instruments, like contracts for differences to Bitcoin. And they could be run both on chain and on Lightning using Schnorr signatures that are included in this proposed taproot upgrade. But all of that’s a little ways out. And for the most part, you know, there’s not a lot of new features and certainly not anything that your average Bitcoin wallet is going to ever notice aside from, you know, potentially some improved privacy down the line when people are using large multisig contracts.

Stephan Livera:

Yeah. I think that’s all totally. Yeah, those make a lot of sense in terms of benefits that will come to users. And I think too, another point is that if we want to keep advancing Bitcoin, then it’s kind of like we have to first sort out, how are we going to do soft forks so that we can keep doing future ones? And let’s say people want to do other soft forks in the future, whether that is, let’s say any prev out or your great consensus soft fork cleanup that you know, getting soft forks and having that agreed in the community as a way of, you know, when people are willing to change aspects of Bitcoin and how we establish a way for doing that. So perhaps we could talk through a little bit of the Bitcoin history around doing soft forks. Can you tell us a little bit about what that has looked like historically?

Matt Corallo:

Yeah, right. So there’s a long history of forks in Bitcoin, you know, early on in the first year or two of Bitcoin’s existence forks were basically, Satoshi decided there was a new version and Satoshi announced the new version. The new version might basically enforce completely different rules. And everyone was told to upgrade and they did, and it was a small network and there wasn’t really anyone using it seriously or taking it too seriously. And so it didn’t really matter. And that was completely fine way to do upgrades. Over time so, a particularly bad issue at the time where every time there was a new upgrade you could construct a transaction that was invalid on the old chain and valid on the new chain. So invalid in the old chain but valid on the new software. And that could result in users who were on the old software, following one blockchain and users who were on the new software following a completely different blockchain and creating two completely different coins and two Bitcoins. And now we gotta figure out which one’s Bitcoin and they can’t transact with each other. And they’re really just two separate networks. So that’s called a hard fork and that’s bad. We don’t want hard forks. And so the general principles for the way we do it is instead of completely changing what’s valid and what transactions are valid Satoshi at some point, basically the actual code changes seem to imply that we discover this concept that we now call soft forks which is if you take the things that were valid before and you purely constrain them, right? So you do everything that is valid in the new soft fork was also was also valid in the old soft fork.

Matt Corallo:

But some things that were valid in the old software are no longer valid. And we kind of wait a long time to start enforcing those rules and we lean on miners to help enforce these rules. So that transactions, so some transactions that used to be valid, they’re no longer valid, but all the transactions that are valid now remain valid. This keeps the network together, right? So all the old nodes will still validate the new blocks. They’ll see the new blocks, will check them and everything looks great and all the new nodes will hopefully do the same. But you can add new features this way. So you can take you can say, we’re going to add a new signature type. And the new nodes will enforce these rules and hopefully the miners will too. And then you’ll have all the blocks will be valid and you won’t have two different networks.

Matt Corallo:

But, and because all the old nodes will still be able to analyze these blocks and understand that these blocks are valid, you know. And so we use this concept of soft forks, kind of, I think the community has moved towards this being the kind of understood way that we want to do forks, because it keeps the network together. And that’s kind of ultimately going to be the theme of today, I think is that splitting the network is bad. The worst thing you can do is end up with two Bitcoins where people can’t transact with each other, and you’re not really sure which one is which and it’s just bad for confidence. It’s bad for usability. People all of a sudden can’t use Bitcoin. and, you know, if that, if that happened seriously, it lasted a while. Probably we would just all give up and stop using Bitcoin because that would be bad. So instead we all, the community, basically we value Bitcoin because it remains together. And that gives us a really strong incentive to form consensus and all agree on what the rules of the network are, so that we have one network.

Stephan Livera:

Yep. And one interesting dynamic that I’d love for you to touch on a little bit further, or perhaps elaborate is this idea that there might be some user out there with old node software. And it’s important that that user doesn’t get screwed over and lose their connection with the network or get off onto some other network. And it’s like basically that’s the importance of having backwards compatibility or maybe even more precisely, it’s more like old nodes having forwards compatibility. Why is that important?

Matt Corallo:

Right. Yeah. So, you know, we don’t know, people forget to upgrade all the time. You know, like we don’t have a magic wand we can wave and force everyone to upgrade those thousands of nodes on the network. There’s any private nodes that are connectable that we don’t know about. There’s a lot of large businesses that maybe aren’t following the Twitter feeds of various Bitcoin developers. A lot of mining pools, especially run hundreds, if not thousands of nodes, and you don’t want it to be the case that someone just forgot to upgrade one of their nodes. And suddenly they’re on a different network. And someone sent them a payment on this weird fork network that no one’s paying attention to. And they accepted it. And suddenly they realized that it was bogus. It was on this other weird fork and it’s not real Bitcoin. And so now they’re mad. They had a full node, they were doing everything right. They forgot to upgrade, but only maybe one of their many nodes. And suddenly they accepted a payment that was completely bogus. And they gave someone, you know, million dollars and they don’t have any Bitcoin for it. And so we just don’t want that to be the case there’s, there’s even worse scenarios where people have maybe mobile wallets that are connected to servers and they don’t know what version of the node soft fork that server is running. There’s no way to check and who runs that server, you know, maybe they forgot to update. You don’t want to screw over those users. There was just, it’s really a mess if you end up with kind of mini chain splits or mini forks for any user.

Stephan Livera:

Yep. And so perhaps we could just talk through historically the differences in how things have worked. So I guess historically, maybe arguably, we could say that the ecosystem was more centralized in the early days and it has been, I guess, progressively decentralizing. And we’ve been learning a little bit more about how things work, because I guess there are different parties and it’s a decentralized ecosystem. There’s no CEO or top-down dictator here, but there are different actors right there. There’s kind of the technical developer community. There’s the miners. Even then the miners, you know, there’s mining pools and miners, and then there are users and then there are Bitcoin businesses. Could you maybe spell out some of the different roles in the ecosystem and what they can, each do?

Matt Corallo:

Yeah. So, yeah, like you mentioned, and like I said, you know, in the very early days it was completely centralized. Satoshi decided and whatever Satoshi said goes. Over time, you know, kind of this concept of soft forks was discovered and how that’s a much safer way to do consensus changes and kind of keeps the network together a little easier, but even amongst all forks, you could imagine just shipping a new soft fork release and changing the rules tomorrow. And if someone, you know, if some miner has an upgraded and they mined some transaction that’s invalid by the new rules, suddenly that block is invalid, but all the old nodes will follow it. Right? So you could imagine a soft fork design that’s particularly terrible and still splits the network rather trivially. So, you know, over time, various ideas to developed about how to do self forks for a while, basically it was just there’s a new release and this new release says that at some point in the future, maybe six months down the line some new rules will become active.

Matt Corallo:

And hopefully by that point, 6 months down the line, people will have had a chance to upgrade enough nodes and especially enough miners have had a chance to upgrade that it’s unlikely, there will be any of sustained fork maybe there’ll be one block here or one block there, but nothing that’s going to rise to like six confirmations or something like that. I think maybe the best example or the best way to answer your specific question about all players involved in modern soft forks is to just go through the history of SegWit2x. And I guess what’s now referred to as the fork wars. Right. So at some point in the Bitcoin history of a number of years ago, there was a really extended debate over what the block size should be and what the kind of fundamental scalability metric of Bitcoin should be. Should you have these very large block sizes that potentially have no fee pressure and then maybe have trouble paying miners. But every transaction confirms in a few minutes or do you want these, you know, smaller blocks where you ensure that you pay miners and keep the network running. It’s doable for everyone to run a full node and for people to do that if they want to. But on the flip side, of course you don’t need as many transactions. So this debate naturally has debates in decentralized communities, raged for a long period of time. And I think we really kind of figured out exactly how the network works and who all the people involved are and what their role is through the painful process of SegWit. So SegWit was a specific proposal to slightly increase the block size and also fix a number of other technical issues.

Matt Corallo:

It was not a huge block size increase a lot of at the time, a lot of especially businesses in the space where we’re demanding a very large block size increase because their user numbers showed they needed some very large increase. They wanted to fit all their users on the blockchain and that’s the way they were going to continue to grow their business. And so the SegWit thing was proposed one way, that kind of people over developers over time decided it was a good approach for further de-risking the chance of a network split in the case of a soft fork was not just to do this thing where you say, alright, it’s going to activate (inaudible). But to say that we’re going to give it a year. And during this year, what we’re going to say, we’re going to say, we want miners to signal in the blocks.

Matt Corallo:

They’re just going to write a little thing in the block that says, I’m ready, I’ve upgraded to the new software, I’m running it. And I’m ready to enforce the new rules. And when you reach 95% of miners writing in their block that says like, I’m ready to enforce the rules then via just the software on that automatically says, okay, looks 95%. We’re good. Now everyone’s going to enforce the rules. And by relying on hash power, you know, obviously every node in the network is ideally enforcing the rules, but if you just rely on hash power, it leads for a soft fork where you only some transactions that used to be valid and make them invalid, the miners can enforce that by themselves. And specifically can keep the chain together, right? So if one miner mined something that’s invalid by the new rules, then all the other miners will just ignore it.

Matt Corallo:

Like all the new nodes will. And if you have 95% of hash power ignoring it, those new blocks will never kind of form a chain that is longer than one or two. So back to the SegWit discussion, SegWit was released with this design. So it had a one-year timeline. And over the course of one year, if in any two week period, I think it was would have had 95% of blocks in that two week period signaling readiness then SegWit would activate. And if you got to the end of the one year and we hadn’t ever reached that threshold, then SegWit would simply timeout. And we would say, all right, it’s timed out. Maybe we try it again, if there’s a reason to maybe there’s a good reason why SegWit didn’t activate and we don’t try it again.

Matt Corallo:

But we get to the end of a year and attempt again. So, okay. So SegWit’s released it’s this proposal to slightly increase the block size. Some people view it as not enough and argue that significantly more should be done. It’s kind of unclear. There’s also it seems like it might’ve broken some proprietary mining optimizations that some miners were using to get significantly more hash power than their competition that people weren’t aware of at the time, or weren’t aware that it was possible to do this in that way. And so as a result, SegWit never reached the 95% threshold. So for a long time, for months and months, it kind of just sat at, I don’t know, 50%, 40%, whatever, but nowhere near 95 and it just kind of hung out there. And, okay, so we’re a ways into this one-year timeout a one year period at the end of it’s going to time out.

Matt Corallo:

And these businesses who are really hurting right, their users there, they view their business as being killed by this lack of significantly increased block size. So they all kind of get together or a number of these businesses get together in a private meeting and decide unilaterally that Bitcoin is going to change. It’s not just going to be a soft fork and it’s going to be a much more disruptive, hard work. And we’re going to not only do SegWit, but then we’re ultimately double the block size on top of that. So something like 3 or 4x, and they announced this to the world and say like, this is what’s happening with Bitcoin. So Bitcoin is going to change. We’re going to call it SegWit 2X. And on this date, in the future or on the date that we decide in the future Bitcoin is gonna fork and that’s going to be the new Bitcoin.

Matt Corallo:

And we’re all going to follow that. And these kind of Bitcoin businesses we have the most users and the most Bitcoin custodian — custodially stored with us. And so we get to decide what Bitcoin is naturally the kind of bitcoin user base was up in arms over this the concept that a number of, or a small meeting by a number of individuals, but certainly by no means the full set of the Bitcoin community. Shouldn’t get to decide what Bitcoin is for everyone. Because, well, I mean, I think that hopefully kind of stands for itself that it shouldn’t be the case that some small group gets to just fundamentally change some aspect of Bitcoin on their own. Because otherwise, what value would Bitcoin have? We might as well just use PayPal because PayPal is, it works great.

Matt Corallo:

As long as you don’t mind the small group changing who does or doesn’t have access to the system and then what the system is on a regular basis. Yeah, so people were up in arms over this, right? So we have these two opposing camps. Now, it was kind of unclear what was going to happen, right? Here’s these are these businesses saying we get to decide because we have the vast majority of Bitcoin transactions between us. So we just kind of get to decide and all these small, other small fries we just ignore them. Then a futures market was developed, right? So SegWit2X, by nature of it being a hard fork, we’re going to create two coins. It was going to be the coin and SegWit2X coin and there was nothing that can be done about that.

Matt Corallo:

They were just going to be two coins, right? So one particular exchange Bitfinex listed a futures market and said, well, there’s going to be two coins. We just run a futures market and then anyone can trade. And if you want to say one, 2X coins, you can buy those. And if you want Bitcoins, you can buy those. And the market spoke incredibly forcefully. The markets said, well, Bitcoin is worth about 90%. And SegWit 2X coin is worth about 10% of what Bitcoin was at that time. So Bitcoin was worth maybe nine X plus or minus what SegWit 2X was worth. And that basically killed it. Right? So we learned, I think pretty clearly that the market gets to completely overrule whatever some group of transactors, some group of businesses, even potentially a large group of businesses and a large group of transactors and Bitcoin holders say, is that the market gets to just say no.

Stephan Livera:

Yeah. If I could just add a little point in here at this point, I think it’s probably worthwhile talking about how kind of the timeline here, because this is all going down in 2017, right? So this is after years and years of kind of debate and trying to get SegWit activated. And I think towards mid of 2017, so SegWit actually activated, I think it was 1st of August, 2017, if I’ve recalled that correctly. But then there was this whole debate around how basically it was seen as like you know, the SegWit 2X people were thinking of it like, Oh, see, we’re compromising, we want this SegWit thing, but we’re trying to give the other people a little bit of what they want. So we’re going to have SegWit and we’ll have a block size increase. And then as I recall, then it was kind of like later, towards the end of that year, there was a bit of that debate about, Oh, hang on.

Stephan Livera:

Why are you taking SegWit without giving us the 2X part of it also? And you’re kind of welshing on the deal or you’re reneging on the deal kind of thing. Whereas I guess from the small block perspective, it was more like, no, hang on. We never agreed to that. We never agreed to have this 2X component. We just wanted SegWit. And so I guess potentially that was some of the the argument and the debate in that time, in that kind of period after August 2017 kind of leading to around November or December of 2017 where some of the kind of on Bitfinex, for example, there was B1X coin, which was Bitcoin and B2X coin to represent, as you were saying, the 9-1 kind of ratio. Correct?

Matt Corallo:

Right. So the SegWit 2X agreement. So the SegWit 2X story, this private meeting was in May of 2017, right? So there was a ways before SegWit activated, but indeed the kind of resolution of SegWit 2X was not until after SegWit activated. When there, you know, basically the futures market spoke and said no, and the coin had no value and actually their soft fork had a bug. So it didn’t actually create a coin and Bitcoin 2x tokens expire worthless, but presumably if they weren’t going to expire worthless, then, then they would fix that bug in some way.

Stephan Livera:

Yeah. And if I could add one more thing here, I think it’s also probably an important lesson for anyone who’s listening. It’s this idea that I think in 2017, a lot of people realized that ultimately users control Bitcoin. And I think that was also an interesting dynamic there because previously there was some people who thought miners controlled Bitcoin. And I think that was something that was not so clearly understood until that time.

Matt Corallo:

So contemporarily, while this kind of SegWit 2X debate was happening. There was also another debate happening around how to activate SegWit, right? So we had this, there was this agreement, private agreement by a number of companies to say, we’re going to change Bitcoin said that what we’re going to do is we’re going to activate SegWit and then do a hard fork. But their original agreement said, we’re going to activate SegWit in a way that’s different from the rest of the networks. So we’re not going to just activate SegWit in a way that activates it for everyone. We’re just going to do it on our own, on our little fork. This kind of stalling of SegWit by the miners this kind of lack of activation led to what was called the User Activated Soft Fork movement or UASF user activated soft fork and then specifically the BIP 148 was the proposal for it, said that what we’re going to do is we’re going to just say, screw you, this whole concept of soft forks activated by having miners signal was the wrong way to go. It lets miners decide what the rules are, block rule, upgrades, consensus upgrades, and we don’t want that to happen. It seems like they’re doing it on bad faith on this like private proprietary mining optimization stuff. So what we’re going to do is we’re going to go back to the old way and we’re going to just say on this date and they picked a date that was a bit before SegWit was going to timeout we’re going to enforce that every block signals for SegWit. So instead of — so they basically proposed an original style flag based soft fork, where it’s just on a certain date, a new rule kicks in, and that rule was you signal for SegWit or your block is invalid.

Matt Corallo:

And of course then if every block signals for SegWit, you’ll reach the 95% threshold and then SegWit of course, will kick in. So the idea was we force all blocks to signal and by forcing all blocks to signal, not only do we upgrade do we activate SegWit for our nodes. Our nodes being like the kind of BIP 148 UASF nodes, but actually every node in the network, at least that is upgraded in the last number of months will enforce SegWit because every block is signalling and you reach the 95% threshold and that’s every node, or at least the majority of nodes will enforce SegWit, then that’s kind of what makes soft fork ultimately active is that the number of nodes and then certainly economic nodes are forcing SegWit. So you have this, these two things that are kind of coming to a head, right? So you have the SegWit 2X thing. That’s coming to a head and you have this UASF thing that’s coming to a head at the same time. And both sides were obviously very dug in. But both sides were arguing for SegWit activation. It’s just one side was saying, SegWit is a part of a larger package and one side just saying, screw you, activate SegWit now.

Matt Corallo:

What ultimately, what was the resolution to, this was something called BIP 91. So BIP 91 said basically we’re going to signal for SegWit in a way that with the dates picked, we’re going to signal for a segment on a certain date with the dates picked so that it lines up with the BIP 148 and UASF, and it all stays. The whole network stays together and stays one blockchain. And by signaling for SegWit on this date we’re also signaling for SegWit 2X, and we’re also signaling for this hard fork.

Matt Corallo:

And so at the end of the day, kind of miners activated BIP 91, and users are running this BIP 148 client also enforced their rules. And even though you had three different parts or three different sets of nodes on the network that had three different ideas of what the consensus rules were. Ultimately, no block was mined that was invalid according to any of them and Bitcoin stayed one Bitcoin and one blockchain, and there weren’t any kind of large fireworks with forks and then people. So at the end of the day, both sides claimed, they won, you know, the UASF movement, arguably had succeeded, it forced miners to signal. It unlinked the SegWit 2X movement, which failed due to this futures market that showed that there was no demand for their token and for their fork.

Matt Corallo:

There was no futures market for the UASF fork, right? So had miners not signaled for SegWit in time, UASF nodes would have forked off and been a different chain. There was no futures market and there was no kind of way to appropriately value those and to kind of try to figure out what would have actually happened, had miners not signaled. So we don’t really know, but we know at least in this one case this movement led by rando users on Twitter was able to force the hand of miners into signaling with basically playing a game of chicken and saying, we’re going to split the network and we’re going to cause a lot of damage and have two different Bitcoins or you signal for SegWit. And then kind of BIP 91 was a way to save face and say, we’re signaling for SegWit 2X, and we’re going to do the hard fork too and we’ll keeps the network together now, and then we’re going to do the hard fork and then the hard fork kind of fizzled and died because of the futures market.

Stephan Livera:

Yeah. So let me explain some of that as well, just for listeners. So as you were saying, it’s like a game of chicken. And so some users were saying, Hey, we want SegWit. We want some movement on this. We’re willing to play chicken now. And so we are willing to threaten that we will fork off. And the risk on the downside is that if we, if the miners didn’t come along with us on this venture, then we would be stuck on a chain that has very, very bad security because it’s only got, you know, 5% or 10% of the chain security, all of the miners. And then on the other side, it’s kind of like the miners also have a risk on their side because they don’t want to be mining a coin that is very low value because if there is enough of an economic impetus, if there are enough users and businesses and people on that other side of the game of chicken, then they are, you know, very, very maximally invested into these hardware units and the operating costs for being a miner that they would be mining on a valueless chain if you will. So I guess maybe that’s one way to explain the dynamic. Would you agree with that characterization?

Matt Corallo:

Yeah, totally. And we saw also with kind of Bitcoin cash and other forks that the mining power on the two sides of a fork tracks almost exactly the value. Right. And so the futures markets said that you’d have 9x, the amount of hash power on Bitcoin as you would have had on SegWit 2X were the value to remain kind of nine to one. and so we don’t know, you know, it’s possible that the UASF movement had enough money behind it, that it would have actually had material hash power and had blocks on its block chain and had it been able to be used. I think that’s unlikely. But we don’t know there was no futures market. So it’s also entirely possible that you didn’t have enough money and all the money would have been on the Bitcoin side. And you would have had this kind of UASF coin that was just off on its own with no blocks. We just don’t know.

Stephan Livera:

Yeah. And I guess amongst some of the core developers at that time, they were split too, right. Because some of them viewed this as like, no, this is too much risk. We don’t want to do this. And then there were others who were obviously much more pro UASF at that time. Could you maybe outline you know, some of the thoughts of some of the developer technical community at that time?

Matt Corallo:

Yeah. So, I mean, yeah, so it was split I think the kind of Bitcoin core development community, the people who were very active on Bitcoin core ranged from “Uhh, Do you guys have to?” to “Whoa, stop. This is a really bad idea. Don’t play a game of chicken with the network.” Cause if it does split and there is kind of even hashpower on both sides, it’s like really bad and might kind of destroy confidence in the value of this thing. There were obviously other developers kind of from the broader Bitcoin ecosystem that were a little more pro UASF. But it didn’t have the kind of Twitter and Reddit, et cetera, community was significantly more pro UASF than I think the developer community was, well, that’s certainly the Bitcoin core development community. There were some notable exceptions here or there give or take, but I think that’s kind of the high level.

Stephan Livera:

Yeah. Okay, cool. So I think it’s kind of a debatable point, whether, you know, UASF essentially pushed the miners by playing this game of chicken into saying, okay, we’ll just mine the SegWit we’ll signal for SegWit and you can have SegWit or whether it was kind of like you were saying, it’s kind of like if all the sides could just say they were winners out of this. So if we were to sort of fast forward now, we’re in 2021, we’re looking at Taproot and we’re sort of talking about how to activate it. Can you tell us a little bit about your thoughts around some of the main proposals around taproot activation? And obviously it would be a great point here to chat about your proposal of you know, modern soft fork activation.

Matt Corallo:

Yeah. So the last fork we did, so prior to SegWit, you know, had a pretty regular cadence of soft forks. So we were a year or so. We haven’t done one sense. I think a lot of people are burnt out on the whole, the drama and the fighting and the infighting and the cross fighting and whatever. And so there’s kind of not a clear precedent for exactly what should happen next and how we should do future soft forks. Cause I think, especially because what the resolution of SegWit was depends on who you ask, whether you asked someone who thought UASF activated and that’s how SegWit was activated, or whether you thought BIP 91 activated and that’s how SegWit was activated. So there’s different, very valid views. And each of those views is going to take something very different into this conversation about how we should activate things in the future and what their view of kind of how SegWit got activated was.

Matt Corallo:

trying to kind of kick off the discussion of how the activate happened? So taproot has been in the design phase since I think maybe before SegWit was activated, or maybe only a few months thereafter, maybe early 2018 and it was in the design phase. And then it’s very slowly been developed and kind of has reached a point where it’s the code is there and it’s kind of ready to go almost. But certainly there’s no activation method and it’s been there for a little bit. So I tried to kind of kick off the discussion of like, how do we activate Taproot about a year and a month ago or a year and two months ago, maybe with a long email thread called a modern soft fork activation. So if you Google site ” list of Linuxfoundation.org modern soft fork activation,” you should be able to pull it up.

Matt Corallo:

That’s probably a pretty interesting read if also, just because it describes kind of what I thought were the goals for soft fork activation and kind of the goals of keeping the network together and the goals of emphasizing consensus and emphasizing the importance of that and all the kind of goals that I thought we should carry into any soft fork activation design. And then I concluded with a concrete proposal and I said, kind of, you know, we should just go with it the old way, if we can, you know, to do this kind of classic BIP 9 where you just let miners signal. And if it times out it, times out, like we’re not in a huge rush for this taproot, not, you know, being fundamentally changed Bitcoin for users and we don’t need it today has been in progress for years.

Matt Corallo:

And if it doesn’t come for a few more years no one’s too heartbroken. So if it times out, it times out and then we revisit it, and then we take advantage of the fact that we had this whole activation process where hopefully the community was very active and involved as learning and as evidence that the community carefully analyzed Taproot and took a part in that activation process. And that as a result of that learning, then we can say at that point either, yes, this thing has clear community consensus, everyone supports taproot itself. But there were, you know, maybe some miners just didn’t bother upgrading in time, or maybe there’s some other weird stuff going on, like happened in SegWit. And as a result, we should just do a flying day activation and say like two years down the road or three years down the road, Taproot’s going to be active and that’s just what it’s going to be and that multiple years gives us time to make sure that the nodes get upgraded. And that it shouldn’t be a big deal and not a big risk to having kind of a chain split from having the network be half upgraded and half on upgraded nodes. So that was my concrete proposal at the time. I still think it kind of captures the nuance of both having a process for a public clearly visible and clearly understood process through which everyone kind of gets to voice their vote and everyone’s like, there’s this thing that’s going to activate people definitely by that point not only have, will have seen it but we’ll know that everyone else saw it and can make their voice heard. But also it’s just that it’s relatively, I mean, it’s very carefully designed and is super unobjectionable. And so there’s very little like we don’t just see it activate.

Matt Corallo:

So that was my proposal about a year and change ago. It didn’t really go anywhere. I didn’t put enough effort into kind of following up and trying to implement stuff and then getting it going. More recently some efforts gone into going in a completely different way or maybe more recently there’s been a proposal by Luke that is called BIP8 and it’s in fact two proposals. It’s not, it’s not one concrete proposal and it’s more kind of optimized for UASF. So there’s, there’s two halves of it. So there’s BIP8 with a lock-in on timeout set to false, and there’s BIP 8 with locking on timeout. Sorry, set to true. And so with BIP 8 with lock-in on timeout set to false is basically the good old way, the SegWit just signal my new technical changes that are good and, but don’t really impact the way it works ultimately. BIP8 with lockin on timeout set to true on the other hand is several things. So one at the end of that kind of one year period that we had for SegWit or whatever the period is instead of tying out and not activating soft fork, we just activate it, right? So we say oops, it’s been a year. We’re just going to start enforcing these rules. So that’s one part of lock in on time out equals true. The other part is it’s actually two forks, so it’s not just at the end of the year. If it’s timed out, you apply the fork taproot, but first you will play a different fork. And that fork is you force all the blocks to signal. So again, it’s kind of like the UASF BIP 148 design where you say, well, it’s been a year now, every block must signal for taproot or it’s invalid.

Matt Corallo:

And then after two weeks, or when we got, I don’t know the exact timeline, then after a while of doing that, then taproot actually becomes active. The process of this forced signaling really strongly creates this risk that UASF and BIP 148 had of consensus split, right? Because suddenly instead of taking the soft fork like taproot, where in fact, the way modern soft forks are done in taproot SegWit and a few before that is if you were a miner running old software. So not just a user running old, tougher, but a miner running old soft fork will not actually generate an invalid block according to the new rules. So even though the miner soft fork that the miners node that they installed three years ago has no idea what taproot is obviously Taproot’s way newer than that soft fork, that miner will still not include any transactions, which are invalid according to the taproot rules.

Matt Corallo:

So this is actually a really cool property. And it’s done by basically Bitcoin nodes when they’re mining Bitcoin core nodes, when they’re mining, they don’t include any transactions that look weird. So, we define basically is that transaction is like, obviously insecure, no one would want to put that on the blockchain because anyone could just take your money and walk away in less a soft fork is activated and then all the new rules. So taproot, SegWit, and various other things use this fact and say, we’re only going to change the way weird looking transactions work, and we’re going to apply new rules to them and give them a lot of interesting properties. And new nodes will include those transactions, but old nodes will just ignore them. And they won’t mine invalid blocks. This keeps the network together even better. It’s a really great design because both old nodes and new nodes can continue mining.

Matt Corallo:

Both old nodes and new nodes can stay on the network and validate all the blocks. And the only case where the network actually forks is in the case of malicious miners. So someone who spends, you know throws away the value of the block to mine an invalid block and obviously old nodes will look at that and think it’s valid and continue mining on top of that or someone kind of does this accidentally. Either way that you lose the value of that block. So it’s less likely and it could happen today, or it does happen very rarely, but occasionally, but it significantly reduces it. But this design of using weird looking transactions to call them standard transactions, to apply new rules on the network just really reduces the risk of this fork back to debate BIP8 with lockin on timeout equals true, which includes both flagged activation of taproot and a flag day activation of this forced signaling throws that property away, right?

Matt Corallo:

So old nodes will not be signaling for taproot old mining pools that aren’t configured for taproot are going to be signaling for it. And will mine. And in another block, according the rules that say every block must signal that results, of course, in old nodes might follow this chain that has, what’s now invalid. But has these non signaling blocks in it and potentially you run the risk of having two coins, at least for a while, depending on how much hash power you have on each side and having double spends or having people having users be tricked. It’s kind of the big drawback. On the other hand, I think with BIP 8 Luke and other BIP advocates argue that this forced signalling property is nice because it makes it very clear by looking at the blockchain, what is, or hasn’t activated, right?

Matt Corallo:

That you can look at the chain, you can say, Hey, look all these miners are signaling for taproot. And thus it’s going to activate in whatever the time period is. Of course it’s also designed to kind of optimize for UASF BIP 148 or to enable this kind of after the fact forcing of the soft fork to activate, right? So instead of saying, we’re going to do this one year activation window, and it’s going to time out, but we’re not going to care. We’re just going to do it again, but with a longer time horizon and then activate it at that point, but in a more conservative and careful way they say, we’re going to do this one year time horizon, but we really don’t want to wait any longer than a year. And we refuse to wait any longer than a year. And so we’re going to ensure that we have this other alternative, this lockin on timeout equals true. Where we are forced signaling, and we do a BIP 148 UASF again, and enforce that the block signal and thus upgrade the whole network. Not just our little kind of UASF group of nodes and users.

Stephan Livera:

I see. And so perhaps one, as you’re saying, one of the benefits, I guess, of considering the LOT equals true side is that it’s unambiguously been activated and there’s no sort of no two words about it, but I guess the one of the caveats then is seeing how many miners are supporting this thing, because again, it’s a decentralized network and, you know, there are efforts, I don’t know, Alejandro from Poolin has been running a website called taprootactivation.com. And last I checked, I think it’s got something like 88% of of the network counting by hash power is in support of taproot. So I suppose maybe that’s one of the counter-arguments somebody could present in favor of the lot equals true style approach. They could say, well, look so long as we have a very high percentage of miners who are pro this idea, then that theoretically that reduces the risk of one of those old nodes getting, you know, inadvertently pushed onto the wrong chain because, you know, a very high percentage of the miners are in favor of this change.

Matt Corallo:

Right to some extent. So certainly in the case that you have a really high percentage of hash power, taproot will just activate through the course of the normal miner signaling period, right? So it doesn’t actually matter whether you do lockin on timeout equals true or false or you do BIP 9 even if there’s no hash power, they all signal readiness and the fork activates, and that’s the end of the story. There’s no, this not kind of this bad potential end game.

Stephan Livera:

Yeah.

Matt Corallo:

The lock-in on time-out equals true. You know, obviously you only get to that point, if there’s not enough hash power, and if there’s not enough hash power, that’s where you start to see these risks of chain split and potentially double spends and two different tokens and all that kind of stuff.

Matt Corallo:

So it’s, you know, it’s hopefully an unlikely outcome, but it’s a potential one nonetheless. And, you know, originally there was kind of some core people were kind of corralling around, just do lock in on time out, equals false. And, you know, there’s, there’s a lot of disagreement about what should happen if it doesn’t activate over the course of the signaling period. So whether people thought UASF activated it or people thought that BIP 91 activated, or whether people thought UASF was too risky or a great battle for Bitcoin users beating up businesses or whatever your views were, you know, there was there was a lot of debate. Thus thoughts about how taproot should eventually activate the kind of initial signaling window fails. And so for a while there was kind of this consensus building of like, well, let’s just do lock in on timeout equals false. And we’ll kind of figure the rest out later because hopefully we won’t get there because probably we won’t get there because Taproot is pretty unobjectionable. And like you said, the miners are already kind of committing to it at a relatively high threshold. So hopefully we won’t need to worry about it.

Stephan Livera:

Yeah.

Matt Corallo:

I’ll just finish this thought. So that was great until a number of people, you know, obviously the debate rate continued eventually there was a contingent and still is a contingent. That’s now arguing, like, screw it. We’re going to run lockin on time equals true, no matter what other people run, what core does or what a businesses run or what miners run, we’re just gonna run that. We’re gonna, we’re gonna optimize for UASF and that’s just the way we’re going to go.

Matt Corallo:

And all of a sudden, of course, that means we have to debate what the end game is, what should happen if there’s a timeout, because suddenly instead of, you know, we’re just going to try this and if it fails after a year, we’ll revisit it and then we’ll hash this out. Now it’s, well, people are going to run potentially incompatible network consensus rules on the network. They’re going to, you know, basically pull out the gun and start playing the game of chicken before there’s any reason to or before there’s any risk of Taproot not activating. And thus, we kind of need to figure out and make sure that if something does go wrong or this game of chicken, that’s already kind of starting it doesn’t end well. And someone doesn’t blink that the network kind of handles it and that, you know, hopefully things don’t completely fall over and catch fire.

Stephan Livera:

I see. Yeah. And I think one point as well, maybe to spell out potential risks in this scenario, there might be some users out there. So obviously people who are listening to my show or people who are following Bitcoin Twitter, they tend to be more engaged Bitcoin users, but let’s say some user out there who’s on a lightweight client, they have some kind of SPV simplified payment verification they’re using that. Or they have some old node there’s a risk for that user. Let’s say they are just innocently accepting payment in Bitcoin. And there’s a risk then that they get pushed or they are inadvertently acting on the wrong chain, even though they’ve theoretically done, you know, they’ve waited for some confirmations, but the reality is they’re on the minority chain without knowing it. And there’s potentially a risk for them. and I suppose, yeah, we can say, Hey, you should have run your full node, but the reality is not everyone is at that level, right?

Matt Corallo:

Right. Or you’re running a full node. That’sm you know, a few months out of date or what have you know, obviously we see that a lot in folks either because they don’t read Reddit or Twitter because social media tends to be pretty bad for a lot of people or often language barrier is a problem. You know, there’s, there’s not a lot of you don’t get the same information when you’re in a different language speaking, Bitcoin community. And so you might not have upgraded your node or might be running something else. And so it’s not entirely out of the question, you know, certainly the people who are active on Twitter, maybe so not much, but that’s really only a minority of Bitcoin users and even full node users. Yeah.

Stephan Livera:

And the other practical, there’s some other practical components to consider as well because many users might be using, let’s say a package node software, right. They might be on Umbrel or MyNode or Nodl, or RaspiBlitz or one of the, or BTCPay server. And then the question then is how do the package node developers, what are they going to do about it to give their users, you know, if they’re, if it does end up that there’s a choice to be given to the user, or if it’s more like, no, we’re just going to choose what we think the users would want?

Matt Corallo:

Right. I mean, yeah. At the end of the day, you’re just having multiple different consensus rules on the network causes, you know, an inordinate amount of problems.

Stephan Livera:

Yeah. And I suppose there’s also, I think I’ve also heard and I think you probably agree with this as well. This is like like a meta argument that, you know, this argument that you don’t want to centralize too much into making it look like the developers are the ones who are, I guess, putting out the soft fork that activates it with LOT equals true. They want it to be seen like maybe there’s, you shouldn’t have a large business or a government who comes to try to put pressure on developers in the future for some other future soft fork. And potentially that’s an argument why if you had a LOT equals false and you just let the miners signal it and activate it, then it arguably shows that the ecosystem as a whole is more decentralized. So I suppose that’s also another argument that I’ve heard. What’s your thought on that?

Matt Corallo:

Yeah. So I’ve argued something, something similar before for example, in the modern soft fork activation post awhile back. Yeah, it’s very important that I think I phrased it before is like, it should be obvious to a casual observer that this fork that is in — that’s being included in Bitcoin core has a kind of broad consensus among ecosystem. You know, certainly the vast majority of people don’t really care about taproot and it’s not going to impact them. But for those who it does impact, it’s going to be kind of a net positive and a nice little win for them or potentially a large one for them that can come from many different ways. Whether that’s, I think doing it via kind of a LOT equals false activation where you have the miners also signaling, and that also creates a little bit of delaying, and it’s kind of more of a kind of two party you know, if a casual observer might think that it’s kind of a two party activation, even though there’s of course more people involved.

Matt Corallo:

Also it could come from, you know, a kind of dropdown fight in the community over the activation method. And so I think it’s actually kind of in one way, as much as it’s significantly delaying taproot in one way, it’s kind of nice that we’re having this kind of a drop down debate and fight in the Bitcoin community over how to activate taproot, because all of it is almost all of it includes a clear caveat of, well, we all agree on taproot, like almost everything seen written about this or discuss this is like, yes, everyone agrees with taproot. It’s good. And not only, you know, we have this miner website now that that’s indicating large support for taproot from hash rate, there’s the Bitcoin Optech group ran taproot workshops with large businesses. I mean just before COVID so a year and a half ago, maybe two years ago now analyzing a lot of the kind of taproot details and getting into the nitty gritty with Bitcoin at the CTO level. And they didn’t have any material objections and also the development community doesn’t have material objections and now we’re making very clear and then learning that the community doesn’t have any material objections, but this kind of fight has made it pretty clear to a casual observer. And I think that’s a really good outcome and it might give us more latitude to maybe take more aggressive approaches like a flag day activation and not necessarily LOT equals true which is problematic for signaling, but find the activation. That’s kind of without giving off an air of developers deciding because we can point to all of these other things and this broad discussion which make it quite clear what was required to get to this point.

Stephan Livera:

Yeah. Also there is a question around what level of miner signaling we would be looking for. So I think most people, so it seems that 95% seems to be the current threshold. But is it possible then that, you know, let’s say it kind of hangs around at 90% would that be an issue going forward or do you think that just through the normal variation, we might see enough blocks signal to make it happen anyway, even if 90%, only 90% of miners come to the party.

Matt Corallo:

Yeah. So I think there’s already been some discussion and potential to decrease the threshold to 90% instead of 80, instead of 95%. But more broadly you know, plus, or minus a few percent, isn’t going to make a difference to the kind of variation as you mentioned, is going to eventually hit your target if it’s plus or minus a few. But at the same time, we don’t want, you know, recall the reason for this kind of readiness signaling on the part of miners is to indicate, yes, I’m ready to enforce the rules. And thus, because we all miners are ready to enforce the rules or a large portion of miners are ready to enforce the rules. We’re going to keep the network together. And there won’t be kind of the small minority of miners, mining forks, and creating an alternate chain that might lead to these reorg problems and the double spend issues. And so you don’t want to reduce that threshold really very much. It doesn’t take very much to get into problem to get into a state where, you know, three confirmations, you know, all of a sudden you have issues at three confirmations or potential issues at three confirmations or maybe even more. So I don’t think it will be reduced beyond 90%. 90% is already a big reduction, but yeah.

Stephan Livera:

Yeah. I see. And also, could you shed some light for us in terms of Bitcoin core’s code and its ability at least currently to deal with a chain split in this kind of scenario? So if hypothetically, let’s say this happens that people you know, let’s say Bitcoin core puts out the release with LOT equals false by default. And, you know, some people in the community are running an alternate client or creating the UASF version with LOT equals true. What’s the current state of Bitcoin Core’s code to deal with that?

Matt Corallo:

Very little. There was some kind of emergency fixes rushed in immediately prior to the SegWit 2X fork because SegWit 2X was essentially that outcome, right, where you have some set of nodes on the network that are claiming to be Bitcoin nodes saying they’re Bitcoin nodes that suddenly are enforcing completely different consensus rules. And they’re on a different chain in fact. And kind of, you need a way for these nodes to automatically go find other nodes on their chain, or you don’t know kind of what the breakdown is going to be. You don’t know, maybe there’s going to be a lot of UASF nodes or SegWit2X nodes, or maybe there’s not going to be many of them, but either way you need to kind of find your way into kind of evenly splitting the network in an automated fashion in just in the software.

Matt Corallo:

And so Bitcoin core has some stuff to do this. It’s a little slow, you know, there weren’t many SegWit 2X nodes. So it was not as big a concern, but more importantly there, it was just kind of last minute because we had to ship it before the fork happened. So, you know, if we’re going into this with a large portion of the community declaring that they’re going to run, UASF BIP 8 LOT equals true, then, you know, maybe it makes sense to start kind of shoring up that code and kind of dealing with that potential outcome in a better and more automated way so that if there is a chain split and you know, it’s, I think it’s kind of damning if it happens and I think we should do everything we can to avoid it. But if there is that in some way, you need the network to kind of split evenly and have two coins so that the market can figure it out because ultimately that’s the only thing that you can really do at that point. You have two coins. People are just going to have to trade back and forth until we figure out which one has value and which one doesn’t.

Stephan Livera:

And I think you might’ve touched on this before, but I think it might be interesting just to hear your response. I suppose, the Luke Dashjr argument is essentially as I’ve read his email and maybe I’ve misunderstood him, but as I understand, I think his argument is that the overall risk is maximally reduced by LOT equals true being the only deployed parameter. So what’s your view on that idea of just putting LOT equals true as the default, that core that Bitcoin core puts out there and just the network and everyone proceeding on that basis?

Matt Corallo:

Right. I mean, it’s kind of it’s dependent on a false dichotomy, right? Where it’s like the only two possible options for Taproot activation are BIP 8 LOT equals true and BIP 8 LOT equals false, where you have, you know, if those are the two only possible ways we can do it, and it’s obviously not. We can turn off the forced signaling part, et cetera, then you can make that argument. That is a solid argument by saying like, obviously the network is better together. It’s better with only one set of rules on the network. It’s the only way the network stays together and it’s healthy. And if there’s this small minority, who’s screaming about how they’re going to run LOT equals true no matter what then assuming there’s not a similar small minority on the other side, which I don’t know if that’s true, maybe there is, maybe there isn’t then it makes most sense for everyone to just run LOT equals true, but that’s a lot of assumptions that tend to be kind of bogus, right? First of all, it’s not the only two possible ways we could deploy this soft fork. I think not only could we deploy LOT equals false, but also we can deploy a flag day that doesn’t include LOT equals true, or it doesn’t include forced signaling, or in fact doesn’t even include signaling at all, which I’ve argued for more recently was just saying, let’s just do a flag day, get rid of all of these games, all of this UASF debate and people trying to create different clients to force it to activate faster and whatever, and just say, look, we can demonstrate very clearly that there is consensus here. We’re, you know, not just can demonstrate, but do demonstrate and, you know, go through all the details. And thus, we’re just going to activate taproot on, let’s say August of next year and screw it.

Stephan Livera:

Gotcha. So it would be kind of just another way, instead of even having LOT true or false, it’s just literally, we’re just going live with this thing August next year. And that’s that because it seems that there’s enough community support for this thing that it’s just time to get it done.

Matt Corallo:

Yeah. Basically. Yeah. and just, let’s just avoid the drama and avoid this kind of risk and uncertainty and question marks over who’s running what, and people trying to convince other people to run different software and creating two different networks and just, you know, do it and sidestep all the drama basically.

Stephan Livera:

Right. And I think this is another bringing up the idea of practical considerations. Of course, obviously in Bitcoin, we say don’t trust, verify, but of course not everybody is capable of reading Bitcoin core code. And if somebody were to release an alternate client, then how does every user get comfortable about that software and that code that they’re now running and are they running an alternate thing instead of what their default set up was like, there’s all these questions that, you know, very few people are at that level of being able to actually read all the code and decide for themselves properly, Hey, I’m comfortable to run this alternate software.

Matt Corallo:

Yeah it’s, I mean, it’s a mess for a number of reasons, just trying to have multiple different versions on the network, just a mess in every possible way. But yeah, that’s, that’s definitely one reason.

Stephan Livera:

I guess if you had to say what you thought was most likely, what would you say is the most likely pathway forward here?

Matt Corallo:

Yeah, I mean, at this point, I certainly don’t know. Obviously if there’s only one thing I can say for certain, and that’s the all this debate and kind of all of this people digging in on their sides and insisting that theirs is the only true way is delaying, and this is going to result in, you know, potentially months more debate. and that’s just gonna mean longer before, not just before taproot activates, but longer before it’s clear exactly what’s going to activate and longer before that soft fork is deployed in longer before developers start just kind of taking it for granted that it’s going to activate and where they can move on and start working on other stuff. Right. As long as it’s kind of this thing, that’s still, we can’t deploy it yet. And we can’t figure out what the activation parameters are yet and we can’t you know, it just prevents people from moving on. It prevents people from building stuff on top of it, at least to some extent, you know, people aren’t going to quite as aggressively build things, assuming taproot until it’s clearly on the horizon. And so it’s just delaying everything. Basically the only thing we can say for sure. And I think, you know, there will be some people I think, who will try to run, try to get the network to run a different set of consensus rules. And there will be some nodes that do that. Hopefully it’s a very small number and hopefully most people ignore them and hopefully that it’s not people who are kind of transacting with those nodes, which I don’t think it will be. It won’t be kind of the large businesses or people who are doing large volume transactions running kind of alternate consensus rules.

Stephan Livera:

I see. Yeah. I mean, it seems with 90% of is on board, assuming 90% is correct, then it seems like we are very likely to get it. It’s just a question of the timing and maybe that’s really all it is. So I guess, so that’s, I guess in your view then that’s why you’ve been pushing this idea of trying to, I guess, separate the idea of forced signaling from the idea of flag day and just have a flag day activation. And basically given that there has been to your earlier point in the modern soft fork activation that there’s been no sustained objections to taproot, basically nobody is disagreeing with it. It’s just time to have a flag day.

Matt Corallo:

Yeah. I mean, I certainly think that’s one way forward. You know, I threw it out there, I guess just a few days ago. So we’ll see what the response is from kind of, obviously some of the folks who are very strongly in favor of LOT equals true responded very negatively, but I don’t think that’s necessarily indicative of very much. So we’ll see what the response is from the broader community when, if people who aren’t spending all their time on this around to take a look and thinking about it deeply. So that’s one idea, you know? Yeah. I really don’t know where it’s going to go. But you know, we’ll get Taproot eventually. It’s just going to have to, this debate is going to have to hash itself out in one way or another.

Stephan Livera:

Yeah, I see. And in terms of your current focus nowadays can you, do you want to just tell us a little bit about what you’re working on?

Matt Corallo:

Yeah, so actually none of this is my full-time job anymore. I don’t actually work on Bitcoin core full-time anymore. I work for square crypto, so that’s we’re the team at square who works on open-source Bitcoin projects. So we’re not related to the team that works on cash app or any other Bitcoin projects within square. Our job is just to improve Bitcoin and hopefully improve the user experience for everyone using Bitcoin. And so within that, we work on a project called Lightning development kit or the LDK it’s at Lightningdevkit.org, if you want to check it out. But basically our thinking is, you know, Lightning, existing Lightning network and the existing Lightning node implementations are great. They’ve matured a lot over a number of years. And you know, if you want to take Lightning and run it on your Raspberry Pi or on your server and accept payments they’re really great, but they’re not very modular and they’re not even gradable right.

Matt Corallo:

So if you have an existing wallet, you know, if you’re a mobile wallet developer, you know, maybe you’re making a new wallet or you want really tight integration, they’re not really an option for you, or you can’t take LND or c-lightning and run it inside your mobile app. You can kind of with LND, but it’s really slow and pretty janky. And the developers, I think we’ve spoken to a number of developers. Who’ve tried it, and it’s just not a good user experience. You can’t build a great user experience out of it cause it’s just not designed for that. So, you know, we started kind of from the ground up and instead built something that’s this cross-platform library for building a Lightning node, right? So it’s not kind of a Lightning node itself. We have some sample Lightning nodes that you could use, but what it’s really designed to say, you know, I want to integrate Lightning and build kind of Lightning node into my existing application in some way, whether you’re a mobile wallet already downloads the blockchain that already has an on chain wallet, you don’t want to have kind of a second blockchain downloading on chain wallet from your c-Lightning or LND integration.

Matt Corallo:

Or whether, you’re, maybe you’re a corporation who has kind of a lot of back end infrastructure and you want much more tighter integration with your existing infrastructure instead of kind of just running a node and kind of interacting with it over an RPC. You know, maybe you’re a mobile wallet and you want to do live backups of the Lightning state into drive or into the cloud so that you can access it on multiple devices safely and without race conditions. So again, all of these things, it’s a really flexible library to integrate into your application to build Lightning into your application, instead of it kind of being an appendage that you just talk to and you can hopefully lead to a lot, a lot better UX, especially on mobile but across a few different architectures for Lightning.

Stephan Livera:

Yep. And as from my, I recall from my earlier discussion with Steve Lee I think he was mentioning how kind of ironically in one way it would have been a good idea for someone for the team say at Electrum to use this. Obviously they didn’t end up going that direction, but have you got any other, I guess have you had interest from other wallet developers and other, you know, software developers who were interested in looking to use rust and use the LDK?

Matt Corallo:

Yeah. Suddenly Electrum started building their own Lightning implementation before we were kind of available for use, but that is a good example case where it took, you know, multiple years of man hours to build a robust Lightning implementation is really not an easy task. And so we kind of provide that out of the box for people so we’ve spoken to a few wallets getting people from, you know, we’ve had a lot of interest, a lot of verbal interests, but getting people to go from a verbal interest to, yes, I’m going to spend a while kind of redoing our user experience around Lightning and building that in and integrating is a big ask. So we finally have kind of, as of the last few months, have pretty good language binding. So in some different languages where you can, take the Lightning development kit and it happens to be written in rust, but we can compile it for basically any platform and you can use it from C or C++, or Java, or we’re working on some Javascript that you can call it directly from. You can work with it from Swift. So basically whatever language you’re already writing in, you can use the Lightning development kit directly. Some of that’s a little early, but it works and it’s usable. So, you know, folks who were kind of waiting for that, we’re talking to again, and they’re starting to play with it, but certainly, you know, if anyone else who’s listening wants to play with building your own Lightning node into your, in your own custom way, go to Lightningdevkit.org and kind of join our Slack and ask around. And we’re really happy to help people integrate in whatever way it makes sense.

Stephan Livera:

And I guess if I’ve understood you correctly, it might also make sense, even in the case where let’s say, not necessarily somebody who runs a Bitcoin wallet now, but let’s say even, you know, the Zebedee guys they’re doing Lightning gaming, maybe it would make sense for some other game developer to just go straight to using LDK if they wanted to build a Lightning wallet into their game, right?

Matt Corallo:

Yeah. Potentially. Yeah. If you want to have a Lightning, wallet built into your program, this makes a lot of sense. Right. Versus, you know, I think the lightning gaming stuff is focused on that. You know, everyone’s going to have one Lightning node that’s running on their system, that’s LND and then kind of the games will talk to that wallet. And then that might make sense if you have, you know, a lot of games, you don’t want to have a lot of different wallets and that kind of thing. But you know, maybe you have, you want to integrate Lightning into Steam or something where like LDK would make sense for that kind of integration where you can much more tightly control how a Lightning node works. And you have complete flexibility basically in how the lighting node works. And then you can kind of expose that to the individual games, I think a big initial use case is kind of around mobile, where we’re just way lighter weight than the other options, and way more easy to integrate, especially in mobile, you have a lot of weird constraints.

Stephan Livera:

Yeah. Very interested to see where that ends up and hopeful to see more people getting into Lightning as well. So Matt just wanted to say big, thanks for joining me on the show before we let you go. Where can listeners find you?

Matt Corallo:

Yeah, so I’m on Twitter occasionally @thebluematt. But come to the Lightning dev kit Slack and ask me questions there.

Stephan Livera:

Excellent. Thank you, Matt.

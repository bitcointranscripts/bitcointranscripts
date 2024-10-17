---
title: Becoming A Lightning Routing Node Operator
transcript_by: Stephan Livera
speakers:
  - Thomas Jestopher
  - Anthony Potdevin
date: 2021-09-29
media: https://stephanlivera.com/download-episode/3793/307.mp3
---
podcast: https://stephanlivera.com/episode/307/

Stephan Livera:

Jestopher and Tony, welcome to the show.

Tony :

Hey, thank you. Thank you for having us.

Jestopher:

Thanks so much, Stephan.

Stephan Livera:

So I’ve been following what you guys are doing with Amboss and I thought it would be a good time to get you on and chat a little bit about Lightning Network just generally as well as maybe some tips out there for people who want to just get started and start running their own Lightning node and things like that. So let’s hear a little bit from each of you in terms of your background and especially with the Lightning Network and how you got into it. So Tony, let’s start with you.

Tony :

I started working on Lightning—I started off with a ThunderHub. I created ThunderHub like a year and a half ago, and that’s when I really got into the space, really started following a bunch of people on Twitter and just getting more into it. So that progressed into the project that we’re building now.

Stephan Livera:

Fantastic and Jestopher let”s hear from you.

Jestopher:

I just started tinkering with Lightning Network starting with a channel to Pollo Feed and playing with Eclair and then just trying out the different tools. And then I grew into RaspiBlitz and getting into the communities that popped up and I found ThunderHub and that was really a user-friendly platform, so I was sending a whole bunch of feature requests to Tony.

Tony :

And that’s actually how we met. He was sending all the feature requests and and he was in the ThunderHub chat on Telegram asking a bunch of questions and helping people out. And that’s where Amboss then came up and started.

Stephan Livera:

Yeah. And Jestopher, also you have the SatBase project as well. So I guess that was a bit of a precursor for you also.

Jestopher:

Yeah, so it was mostly just because I thought Lightning Network was so cool that I was like, I should write about this. So I created SatBase.org and included a couple of tutorials, which is like what I was doing for Lightning Network at the time. It was just fun to write about Lightning Network and something that I was really interested in. I just wanted to help out the community and pay it forward a little bit.

Stephan Livera:

Awesome. The Lightning Network has grown a lot recently. What do you guys think about that and where are we at right now in terms of Lightning Network as a network?

Jestopher:

So part of it is just, I see Lightning Network as the future of payments. I mean it goes really fast, it costs next to nothing just to make a payment, and it also has all the Bitcoin properties—so borderless, censorship resistant—and then we did have a period of high fees in the mempool and I think right at that same time Umbrel came out and it was like, Oh, okay, here’s a problem, and the obvious solution is to start moving into Lightning and just lock in these low mempool fees and create infrastructure for the future to take advantage of that.

Tony :

Yeah. I think one of the things that’s most attractive for users and why they go into Lightning is because it’s so fun. There’s so many projects that don’t have to specifically be like the huge company or anything. For example, Pollo Feed. Like, I’m sure so many people joined Lightning just because they wanted to feed some chickens with Bitcoin over the internet. So there’s so many little cool projects that people are just like, “I want to test that out. I want to see what it’s about.” And it really grabs their attention.

Stephan Livera:

Yeah. That’s definitely something many of us can relate to. Obviously there’ll be some people who are just more surface-level, they just want to use a Lightning wallet and that’s all they’re ever going to do. They’re just going to pay and receive, and that’s it. And they’re not really going to think too hard about channels and running their own node and software and all these aspects. But then for another category of people—I think these would be your users and many of my listeners are in that category—would be in that category where they start playing with something and now they just want to tinker. They set up an Umbrel or maybe they set up a BTCpay and now they’ve got their Lightning channels to manage and they’re using, RTL, ThunderHub, they’re using different software, they’re talking to friends about how to do these things. So can you tell us a little bit about how people might go on that journey and maybe what was that journey like for you guys when you were going on your pathway of, Oh, okay, the difference between just using Lightning purely as a paying user to pay for things, versus actually taking that next step and thinking, Okay, how do I run my own routing node?

Jestopher:

Right. It starts off just because you’ve heard about this thing called the Lightning Network and it’s really cool. And maybe you’ve heard a couple of people talk about it—on your podcast, for example. And then you find a community because running a routing node or a Lightning node is not something that you can do by yourself. It has to involve other people. There’s a big social network layer attached to it. So the formation of communities is very natural. So just helping each other out and documenting the process has really accelerated this.

Tony :

So as [for] how the process is for a user, I think at the very start, it was much harder to get onto Lightning—you either had to use a custodial wallet on your phone and—actually getting your own server up and running, I remember the first one I got up and running, I tried to go the very simple route—how do I get this running? And at the time it was with the BTCpay server Docker installation. So it was very simple, one-click install and it did everything for you, but I feel like it still wasn’t for everybody. It still had some involvement. You still had to go to the command line and you still had to get everything set up. And then came other projects that were more focused on using small hardware devices, for example, the RaspiBlitz. And it just started iterating a lot into what was easier for users, what was better to drag more users into this space and make it easier for them. And we started getting better user interfaces for people to come. For example, Umbrel I think has brought in so many people into this space just because of its simple install and it’s basically up and running.

Stephan Livera:

Right. And we’ve seen a massive growth in the number of Lightning nodes and channels in recent months as well. So maybe you guys want to comment on that or if you’ve seen the stats recently, if you could comment on where we’ve come from and where we are today, as we speak in September, 2021.

Tony :

Yeah we were just checking some stats this week and we saw that just last year, the size of the Lightning Network has doubled. So the growth that we’ve seen in the Lightning Network this past year has been crazy—and the amount of projects that have been coming out. And I honestly think it’s all community-driven. There’s all of these communities that have come out of just people helping people, like plebs helping plebs. That is the idea of all these communities, and it’s been a huge help because it’s not that easy to find good resources and good documentation on Lightning, but just people sharing their experience in it is growing this huge community knowledge base that has helped so many people.

Jestopher:

Yeah, it was just starting off with openoms for me, and then Alex Bosworth helping me out like as a pretty novice user. I’ve used command line only a few times. But what we see is the growth happening now and the El Salvador news came out and there’s this force that goes like, I know that Bitcoin can’t scale to be a global payment system on the base layer so we need something else. And the Lightning Network seems like the obvious solution because of its inherent properties and you have stable protocol behind it as the base layer. And we’ve seen $11 million worth of Bitcoin added to the Lightning Network just in the last month. We’re just watching this explosive growth. And I think the community really wants the El Salvador payment system to be a success, so there’s like this altruistic force—I want to provide liquidity to the Lightning Network and create some channels that point in the right direction to make the payment system work with Bitcoin as the base layer.

Stephan Livera:

Right. And as you were saying, there’s just been massive growth. I recall at the Lightning conference 2019—so I was an emcee for that conference. And at that time I remember it was maybe 5,000 or 6,000 Lightning nodes on the network. And as we speak today, I’m reading off your website Amboss.space, and you can see 15,753 nodes out there today, 72,000 channels and 2,725 BTC, which is massive when you think about how far it has come. I think also the understanding around how to be a good routing node has also come a long way in that time as well. Maybe you guys could comment a little bit on that. So just for listeners, if they’re learning about the Lightning Network, could you just explain what makes a good routing node?

Jestopher:

Sure. First it starts with node that you’re able to use. I think a lot of people start with Voltage, or Umbrel is very popular, and then Start9 for the privacy focused ones. And then there’s a big question of like, Who do I want to open a channel to? Who is going to be well connected? Who’s going to be reliable? And is this someone that I can reasonably trust? Because the thing that might cost me is if we have a disagreement in the future. So that’s basically like someone for the technical folks that would be broadcasting the old state, or our nodes just disagree. Then we’re also taking advantage of the low mempool fees. So create a channel when it’s cheap to do so, and then in the future, as the mempool grows, you can actually pay for the channel open. So it’s moving the cost of locking in a Bitcoin transaction today and creating a channel, and then you’re able to set fees that would help pay for that channel open and the channel close in the future.

Tony :

In it’s very basic form, a routing node just does two simple things: it’s receiving a payment and sending a payment out through another channel. So I think one of the biggest things that you have to take into account, if you want to have a routing node, is that you have to have a good amount of capital that is incoming towards your node so that you can receive, and hopefully same amount in outgoing capacity that you can send. To me, that’s the ideal situation. If a node can, for example, receive one Bitcoin and send one Bitcoin, that is I would say a very good routing node.

Jestopher:

So that would mean maintaining that inbound liquidity from your best connected peers and then providing that outbound liquidity at popular payment destinations, which could be a retail store or a Mom-and-pop shop or it could be a swap service.

Stephan Livera:

Yeah, very interesting. So let’s explain that just for people who are a little bit new to make sure everyone can follow along. So for listeners: remember, in the Lightning Network, you can think of it like an abacus and you’re moving the beads across from one channel to another. In this case, if all the beads are on your side, you can’t receive. So what Tony and Jestopher were explaining is that when you are trying to be a routing node, you want to make sure that on that abacus you’ve got a reasonable split of beads on both sides. And the important point here is as Jestopher you were just explaining it’s that you’ve got people who have liquidity inbound to you, and then you have channels open in the direction that somebody in the network wants to pay to. A common example there might be a big Lightning exchange or a merchant who accepts Lightning payments, or perhaps you might open your channel in the direction of OpenNode or some of those payment processing [services], because obviously they are going to be receiving a lot of sats. From the listener’s point of view or the user’s point of view, they are thinking, Well, I want to open my channels in a way that they’ll get used a lot, and then I will receive a routing fee for that. That’s the basic idea here, right?

Jestopher:

Right. So with each channel I like to think of it as like you’re adding a direction to your Bitcoin. So I’m going to point my Bitcoin in the direction of either someplace where I want to pay myself, or I can take a guess at where people want to pay in the future. Right now with El Salvador, maybe I want to open the channel to the Chivo Wallet and the node behind that, so that I can help make remittances really, really cheap for the people of El Salvador, because I know that there’s mostly a payment flow. Now, eventually El Salvador will be spending sats and might become consumers—they’ll be paying for goods. As people are just getting started on the Lightning Network, these businesses, hopefully they’ll be running their own node, but when they’re just getting started, they’ll probably use a solution like OpenNode. So you could open a channel to OpenNode and then first there would be remittance flows to El Salvador and then from the Chivo wallet to some of these destinations like OpenNode, that would be maybe a good first step on how I can support routing on the Lightning Network.

Stephan Livera:

And I suppose also important for a good routing node—obviously the channels and the connectivity aspect of it is important—then also, it’s important to have your node be available and reliable. These are obviously very important factors because if your node is offline, you can’t be forwarding payments. And then people who are connected to you might get annoyed, right? Because they’re like, “Hey, I committed capital in your direction and you weren’t available when I wanted to pay you some money as some fees. Come on, what’s going on here?” So that’s also an element of—you’re selecting “Who am I going to be a channel partner with” based on, are they reliable? This is maybe another aspect that might become part of their selection toolset or arguably it already is. Do you have any thoughts on that aspect?

Tony :

Definitely. So I think one of the biggest requirements that came from Lightning is that you have to have a running server and it used to be very easy before because, for example, if you have a Bitcoin wallet, you can have it on your phone. You don’t need to have it like constantly connected to the Internet. It’s just there. And if you connect, in some time you know it’s going to be there. And then came Lightning and it has this requirement that you need to have a running server. So it’s a hard requirement because it’s running infrastructure, it has a cost, it occupies space, it needs maintenance, and it’s not that easy to keep up. So when you’re looking for peers that you want to connect to, reliability is a huge thing that you have to take into account because if they’re not online, they won’t be able to move funds for you, for example. You won’t be able to pay through them. Or maybe if that is the service that you want to pay, you won’t be able to. Or if you’re getting payments from them, then you know that sometimes you might not be receiving payments from them. So of course a reliability or people having constant availability of their nodes is a huge thing to take into account as well.

Stephan Livera:

Yeah. And also I think the aspect around how big the channels are, that’s a factor as well, because if I got here and open the channel to you and—reading off Amboss.space, the smallest channel on the Lightning Network is like 1000 sats—it’s absolutely almost hitting the dust limit at that point, but you have to pick the right size. At the same time, Bitcoin Number Go Up. The price is rising over time, so you might open that channel and then in a year’s time, that channel is actually worth a lot more than it was one year ago.

Jestopher:

It’s true. And when we’re talking about availability and liquidity, we’ve watched some metrics emerge when looking at the market. It’s a big job to evaluate each node on the network because they have their individual characters and they are individuals behind it. So we’ve integrated the balance of satoshis, or the Bos Score—which Alex Bosworth obviously is behind that one—and we’re showing the history of nodes’ Bos Scores. So you can see their performance over time and also be able to use these different metrics that are going to come out to help evaluate these different characters of these nodes.

Stephan Livera:

Thoughts on the Bos Scoring and how it comes up and who assesses it? Because someone who’s new might have these questions. Or is it some social club—if you’re one of the cool ones you get a nice high Bos Score? How should people think about that if they’re new and they’re trying to figure out how to be a good routing node?

Tony :

I think the idea of the scoring mechanisms is very polarizing. Like, you see it on Twitter. People are like, “But what is this score? Where did it come from? Why do people use it?” In my personal opinion, I don’t give too much weight to it. I think it’s an interesting concept. But what you can see is that people like using the Bos Score. Nobody knows what is happening behind. Like, you have some thoughts that they’re probing the network and seeing the state of the channels and everything, but nobody really knows what it’s calculating for it to give you a score. And in my opinion, it doesn’t matter. It’s just a number and people use that number and they’ve seen that it works for them and they keep using it. So, yeah, I feel like people give too much weight to it. I don’t know. I really see it just as one interesting data point.

Stephan Livera:

I see. Longer term, it might be more like there’s competing standards. There might be Bos Scoring and there might be Amboss Scoring or there might be some other way and there’ll be all competing different standards. So if you don’t like this one, you can use some other way. That’s one aspect of it.

Tony :

I’m sure there’s going to be more scorings that pop up. For example, on Amboss we already have it as well. There’s this other tool that’s called LN node insights, and they also do some network analysis and they see like, Okay, what’s the score of your node? If you’re connected to other hubs or big peers, or how many hops can your node take for others to receive a payment? And all of these different metrics. I think they all get aggregated. When you’re looking into who to open a channel to, it’s not that you just check the Bos Score, but you check so many things: you check the Bos Score, you check these other metrics, you check if they’re in your same Telegram group, if you know the person, if he’s in your same city. So there’s so many data points that people take into account to open these channels.

Stephan Livera:

Let’s get into that a little bit. Talk us through the process of how someone uses Amboss.space. Tell us a little bit about that.

Jestopher:

Sure. The first thing that you would see on the homepage is search. So that is a place where you could enter the alias that a node has chosen for their node. So that might be the “Silk Node.” You can also look up the public key for your node, which is an identifier there. And once you go to that node page, you’ll be able to see, Okay, what’s their largest channel, what’s their smallest channel, and what types of fees do they charge? And I think one of the things that we really try to focus on is [to] make this thing user-friendly. And a big part of that is just [to] have that data available on one screen, and you would be able to compare fee rates and decide like, Hey, is this a node that I want to connect to? A big part of that is, One, do they have contact information? Because if their node goes offline, how am I supposed to let them know, like, Hey, maybe you have an error going on. Or like, Are you aware of this problem? Or, I’m having difficulty? How do you troubleshoot? Because at the end of the day, this is a social network and it relies on other people. The other thing that we’ve added are communities to it. So you’d be able to see if this node as a member of different communities on the Lightning Network.

Tony :

Even on the homepage we have a small listing of all the communities that are available and how many people are in them. So just when you get there you already see like, Oh, like there’s all these different communities. And then you can go inside and see all the different nodes that are in them. And as Jestopher said, same on the nodes page. Maybe when you want to connect to some node and you put their pubkey into Amboss and you go and see their information and you see a bunch of little tags under their name that shows which communities they are in, do they have a Twitter account added to their profile, and all of these more social metrics.

Jestopher:

Once you’re actually on the node page, then you can copy their pubkey and their IP address or their onion address, and copy that into your nodes open channel. And then you’ll make a decision on how large the channel you’d like to make.

Stephan Livera:

For these routing node operators, is this a hobby or is it a side hustle—they’re making a little bit of money out of it? Or are they quitting their day jobs? Just give us a context, give us some sense of where it is at just today.

Jestopher:

A really high-performing routing node would make maybe a 1% yield. And this is probably someone that has a good understanding of the Lightning Network already has lots of practice doing it. So it’s generally low yield, but I look at it as a reflection of the stability of this. So we’ve got a strong protocol and relatively low risk. So there’s some hot wallet risk and maybe some risk of a forced closure—so this is where I might disagree with one of my node partners. But for the most part, very low risk and also consequently lower yields. And we’ll see how that changes as the mempool heats up with more transactions competing for a spot in each block.

Tony :

One thing that’s very interesting from Lightning is that it’s a very, very dynamic network. It’s constantly changing and it’s very dependent also on external factors. For example, one very big external factor that I would take into account is mempool fees. Right now, like for the past months, we’ve had very low mempool fees. So on one side, opening channels has been very cheap for you. And I think a lot of people are taking advantage that right now the mempool fees are so low, like to get their node bootstrapped into the network at a very low cost. But then on the other side, if we have very low mempool fees, then people can also transact very easily just on Bitcoin on-chain. So it’s very dynamic and it’s changing so frequently that even these yields that we have today might be completely different tomorrow. And it depends on so many things.

Stephan Livera:

Yeah. That’s a good point about where we are today in terms of mempool fees being very low. Now, there’s different reasons people have speculated for that. I think I saw Murch commenting on this recently and he was saying that it could be mainly just because of SegWit adoption and potentially the adoption of SegWit by blockchain.info or blockchain.com now, where they were previously a massive wallet and sending a lot of on-chain transactions. And now just that marginal improvement by using SegWit and probably the use of batching by a lot of exchanges—of course Lightning is taking some load off the chain as it were—but maybe there’s also less of a culture of on-chain transactions, and maybe over time, it’s going to become more and more of a Lightning thing. And also the other argument I’ve heard is that maybe people are using stablecoins for some things. So I’m curious what you guys think. Do you have any speculation on that, around the fee rates?

Jestopher:

I think looking at the fee rates in the context of what are the alternatives is probably a good way to go about it, because right now, if you’re opening a 1 million satoshi channel, you can pay for both the channel open and the channel close for about 300 satoshis. And this thing can operate for a long period of time. So in order to earn back the cost of those two on-chain transactions, you can charge 300 parts per million. So that’s 0.03% transaction fee. Now you can compare that to what I’ve looked up as a domestic Visa transaction at 1.25%. So that puts us 43 times cheaper than a domestic Visa transaction. We’re watching the cost of commerce just continue to drop. This is a really exciting thing—of course it works for remittances, but it’s also going to start disrupting the typical debit card and credit card payment infrastructure.

Stephan Livera:

I’m just curious on that because here—of course, I’m a Lightning bullet myself—but I could hear the counter-argument. It might be something like, Look, there’s a lot of hobbyists using Lightning today and they are in effect subsidizing everyone’s use of the Lightning Network because they’re not that fee- or price-conscious. They’re just opening channels and making availability. Maybe it would be fair to say that over time, that fee rate might have to rise. But what do you think about that?

Jestopher:

Absolutely. As that fee rate rises that would also mean that the yield, the reward, for being a routing node will increase. So as there’s more commerce that happens, it becomes more and more attractive to join the Lightning Network—as simply someone that’s saving satoshis, and also using their satoshis to provide a meaningful service all over the network.

Tony :

Lightning is at the end of the day a network and it has the same network effects that you would expect from any other network. So why did so many people join Facebook? Because everybody was on Facebook. And it’s the same thing with Lightning. Like people come in and more are rushing in the more they see other services that are being provided over Lightning. For example, a Namechimp, they’ve been receiving on-chain payments for quite a while already, and they had so many requests for them to implement Lightning because when you buy a domain—it’s not a hundred bucks. Buying a domain is like maybe seven bucks now. So it’s a perfect amount that you can easily do over Lightning. And the idea that now Namechimp, you can get a domain over Lightning, and so many other services, is just going to make more people want to join and more people want to see the reach that they can get to with their Bitcoin.

Stephan Livera:

Yeah. And that’s great to see. I’m quite excited to see more and more services now accepting Lightning. And while we’re on this whole topic of fees as well, I’m wondering, do you have any thoughts about how Lightning routing node operators should think about setting their own fee? Because as you might know, there’s the base fee and then there’s the variable fee. What are your thoughts on finding the right fee rates as a routing node operator?

Tony :

I think there’s a lot of [disinformation on] how you’re supposed to price in your fees for channels. I think at the very beginning, everybody joins Lightning and is like, “Oh, I’m just going to set the lowest fee possible so that I helped the network the most,” but it’s actually not that beneficial as they think for the network, because having such low fees is just causing a misallocation of funds. So when things are free, people tend to move them, even if it’s not really useful for them just because it’s very cheap. So normally my suggestion is to have some sort of fee, like try, maybe go up to 100 PPM or go up to 300 PPM and see how it affects your node. And you also get more [of an] idea of how others are valuing your liquidity, how others see your channels and who you’re connected to—how much they value it. It’s very hard to see that when you have like a 1 PPM fee, because you might just be getting funds that are moving just because others want it to move since it has no cost for them—it’s just misallocated.

Jestopher:

The other piece that you might look at is some of these swap services. So a routing node will look at the LOOP node page and that’s like our most frequently visited page on Amboss. People are closely monitoring the fee rates that people are offering to the LOOP node. Now that node is special because it’s reallocating liquidity where it’s needed, where, for example, a mom and pop shop won’t be part of a community necessarily and be able to say to the routing nodes directly like, “Hey, I need some additional liquidity. Can you help me provide this service?” And instead of doing that what they often do is they would use a Loop Out in Ride the Lightning and they would hit that button and it would quickly move liquidity so that they can receive payments and that they can have that reliable payment infrastructure. Now, since they aren’t communicating to the network, we might not be able to allocate channels to them, but instead we can just open channels to the LOOP node and that service will reallocate. But there’s a premium that destinations for payments are willing to pay for that that quick responsive liquidity move. So that’s where most routing nodes are really cashing in because they know this is a popular destination for payments, and they would be able to provide that liquidity when it’s needed.

Tony :

And it’s very interesting to see the activity that is happening, for example, for this LOOP node. You can go in and you see like, Oh, okay, somebody is giving them 1 BTC in liquidity for maybe 5,000 PPM. And then a moment after you go back in and you see somebody else is offering [the] same amount, but for 4,999 PPM. So you see a lot of competition towards who gets to offer this capacity to the LOOP node so that they capture the most value possible. And it’s very interesting to see. It’s a very competitive space trying to get to these swap servers.

Stephan Livera:

Fantastic. I’m curious then in your experience or when you’re talking to Lightning routing node operators, are they individually setting fee rates on channels? So as an example, that routing node operator might be setting 300 PPM on all the other channels, but in the direction for the LOOP node, he’s setting the 5,000 PPM, as an example. Is that a common thing you think?

Tony :

I think every channel is different and the liquidity or the capacity that every channel has and where it can move to is priced completely different. Sometimes you have, for example—one famous node is the Bitrefill node. That node has, in my opinion, so much capacity that is incoming to that node, that it’s hard to price in your channel because you have really set very low fees for a [inaudible 35:39], and then you have other sides of the network that are higher fee channels, for example, LOOP node, or Bolt—that’s another swap provider. So each channel has its own characteristics and you have to play around and see what is the fee that is best for that specific channel.

Jestopher:

One of the other tools that we’ve been watching is Charge-lnd. Maybe more generally, it would be just dynamic routing fees. So as liquidity moves, they’ll start to increase the fee rate that they’ll be charging. And when users turn on this service, what they generally notice is, Oh my gosh, my routing income has increased immensely, but we’ve been noticing that it affects the Lightning Network graph that our node receives. So whenever there’s a fee rate change, it has to communicate that new fee rate to the rest of the network. And that takes time. And now we’re displaying our nodes graph information on Amboss.space, but it can become quickly out of date because just the gossip on the network about this channel fee update is taking a long time to propagate throughout the network. So in the interim, when the fee rate is updated, that channel might not be immediately useful to the people that need that liquidity, because they’re waiting for that channel fee update. So that’s going to be a trade-off that users are going to experience running things like Charge -lnd.

Stephan Livera:

So I presume then that that’s something people might not be aware of in terms of the gossip aspect of that. What happens then, if it hasn’t propagated in time to your node? Does that mean that node might reject your transaction because, Oh, hey, you weren’t paying enough fee, or something like that?

Tony :

It’s all about expectations. So when you are trying to do a payment over Lightning, your node, based on what it sees of the network, it has some expectation of the fees that it might expect from the other nodes for the payments. So for example, if one of the nodes that is in that payment route had some fee and they changed it very frequently and that change is still being gossiped and it still hasn’t reached your node, then when your node goes to do that payment through that route, it’s going to find a fee that wasn’t what it was expecting. So it could be that the fee is higher or the fee is lower, and then your payment could or could not go through. So in general terms, what we’ve seen with Amboss.space is that gossip is slow and the more the network has been growing, and the more nodes that have been coming on, the slower it is, because there’s just so many messages that have to be gossiped to every single node on the network for it to graph the whole state of how it is at that point.

Stephan Livera:

So it’s growing pains.

Jestopher:

It seems that there’s a bit of a trade-off—we’ve made it so that we have lightning-fast payments, however, the landscape [of] the network graph is constantly changing. And as each node is updating its own map of the network, it takes a long time to do.

Stephan Livera:

Yeah. So that could also cause problems in terms of how easy it is to route a payment, right? So it could cause reliability problems just broadly. Who knows, maybe the dynamic fee movement programs have to rate-limit how quickly they change fees, as an example. But again, Bitcoin, it’s permissionless, so you can’t stop someone. So they could just be changing their fee all the time every millisecond and the rest of the network has to now gossip that. So I guess that’s something to consider.

Tony :

Yeah. For example, with this tool that Jestopher mentioned that lets you automatically set fees based on the channel state of your node, it’s like with great power comes great responsibility. So you have to use it in a way that is beneficial for you and for everybody else in the network. But of course there’s people that abuse it too much. So they set certain parameters so that it’s changing your fees very frequently and they might see it as beneficial for them like, Oh, I’m pricing my liquidity up to the last satoshi every minute.

Stephan Livera:

Optimizing it.

Tony :

Exactly. But what they don’t see behind the scenes is that every single one of these changes is a gossip message that has to be sent to all the other nodes on the network, which can take a while. I think there was some studies on it and it’s like an hour for a channel change to be gossiped to the entire network. So that means that for one hour, that channel is basically not used because the other nodes will reach that point and see like, “Oh, something’s different here. I might not use this channel to do the payment.” And it could be up to an hour that it’s disabled.

Stephan Livera:

So that’s interesting. But I guess then at least they do have an incentive to not do it too quickly because they don’t want to take their own stuff offline because that will impact their own availability and reliability as we were saying earlier. So they have an incentive to not be assholes about it, right? So we could say that at least.

Tony :

Yeah, exactly. The problem is that it’s not very known or it’s not common knowledge that this happens, that this gossip has to be sent out and has to be spread through all the nodes. So it’s definitely important for people to realize that this could not be as good as you’re expecting, to have these very constant fee changes.

Stephan Livera:

So keep it to once an hour guys! With rebalancing—bringing it back to doing your channels and managing those channels—generally speaking you don’t want all the beads to be on one side. You want there to be some level of a balance, but maybe trying to go to exactly 50% every time might not be worthwhile as well. So what’s your thinking there around that aspect, like I’ve heard different ideas on this. One idea would be: once your channel starts to get a bit unbalanced, you can try to change the fee to entice people the other way. And then the other way is actually to do say a rebalancing yourself. And then maybe another way would be to use a swap in or swap out service like loop in and loop out Bolt, that kind of thing. Could you just spell out some of your thoughts on that?

Jestopher:

I love the things that you’ve mentioned. And I believe strongly that it’s missing one, which is: either opening or closing a channel. That is one of the tools in your toolbox to say, Hey, there’s a whole bunch of payments going to this destination and I want to continue to provide this service, and [it’s] eventually going to run out of liquidity. So the only way to add that really is to open a new channel. Now, rebalancing is going to move liquidity from your peers that might be underpricing it. So if I’m going to do a rebalance, that means that I have to be able to charge a higher fee than those peers because now I’ve taken their liquidity. So it’s a pretty zero-sum game to do a rebalance, but now looking at the swap services, for example, Bolt, or using loop out, you’re going to pay a premium for that. But what that is doing is actually moving liquidity from one point in the network to a completely different point just through using payments instead of rebalances, which would be a circular payment to yourself.

Stephan Livera:

So that’s a very interesting aspect. Another idea I’m curious to get your thoughts on: the growth of some of the thinking around being a routing node operator. I think more people are starting to be more serious about actually taking into account all of the fees. Because maybe in the early days, people would just [say], Whatever, it’s a small amount of money, just open, close channels, whatever. But now if you’re trying to actually do this either as a semi-pro or trying to eventually someday be a professional, then you have to take into account channel open fees, channel close fees, any rebalancing fees, any loop in or loop out. Is there any thinking or tooling being created around actually calculating that for a routing node operator so they can have a little view of what’s going on?

Tony :

For tools—so there’s a lot of different UI tools that have been popping up that allow users to very easily go in and see what is the status of their node. For example, my favorite—of course, I’m a little bit biased—it’s ThunderHub. It shows a user the information that they have, or it gives them a glance into the status of their node in very easy to read graphs. I’m a very graphical person. I like seeing things in graphs or on tables or presented in a way that gives you an idea of how the status is, very quickly. So all these tools that have been created, of course, they let users not have to use the command line. They let them see how many payments they’ve been forwarding, what is the liquidity on their channels, can they receive more or can they send more, which new channels have been opened—in a very instant, like just open a website and you have everything there.

Stephan Livera:

Excellent. So the tooling is coming up now and people have ways to consider all these elements so that they’re not just naively opening channels without actually accounting for the cost associated with that. And while we’re talking about this also, I’d love to get your thoughts on Lightning in a high fee environment. So maybe earlier this year, the fees were higher and people were like, Oh, is this it like, is the mempool never going to clear again? And of course we know now it did, but I think it does represent some interesting challenges and changes to the way we have to think about how we run a Lightning node in a high fee environment. Do you have any tips or thoughts to share there?

Jestopher:

Yeah. As a routing node operator you’ll be creating infrastructure. And the cheap time to do that is now when the mempool is basically empty. I can pay a Bitcoin transaction today and be able to use that a long time in the future. So I look at this as the great build-out of the Lightning Network, and you’ll be able to price the liquidity based on, one, the mempool today, when you open the channel, and then, two, your expectation of what the fee will be when you close the channel in the future. You will be able to amortize the cost of that channel over the life of the channel. So that is going to be something that involves a little bit of speculation, but it’s also a massive opportunity for people to realize, like, Maybe it is worth it for me to rebalance today to do a circular rebalance, because I know that this liquidity is going to be more valuable in the future as we watch the mempool fees rise.

Stephan Livera:

Yeah. So that’s really interesting to think about, hey. You’re right, you have to think about what the fee will be in the future. And there’s also a chance that your channel gets force-closed. Like, let’s say your channel partner goes down, their node goes down or something happens like that. And maybe as a safety precaution after a little bit of time, either one side or the other just force closes it. Then you’re paying off a channel close at that point. And you don’t know when that could be because they could force-close at a high fee time. And then at that point you’re just getting wrecked because now you’re paying the high fee. But also a countervailing balance is, when we go into a high fee environment, a lot more people will want to pay over the Lightning Network. So you would naturally be getting a lot more routing fees coming through in that aspect also. So it’s an interesting counterbalance there. I recall chatting to a gentleman who was running a relatively large routing node a while ago, and his philosophy was basically to just never bother with rebalancing and just have enough channels in and out that he never really had to when he felt like it. It just managed itself over time. What do you think? Or do you think that approach is insufficiently sophisticated over the long-term?

Tony :

So one strategy that I like to apply that has been really useful for me is directly trying to rebalance the channels, but not by doing these circular payments or looping out and in, but just by setting the fees that you have for that channel. I’ve seen it to be very efficient. If you have all the liquidity on your side and you want it to move to the other side, then just set a very low fee and people will use that channel and it will start moving those sats to the other side. And on the contrary, if you want the sats to move to your side, then just set a higher fee and people will stop using that side of the channel and payments will tend to float to the other side. And I found that to be very useful, at least in my personal experience.

Stephan Livera:

Yeah. So basically setting the fees to help your rebalance go in the direction that you wanted to is the tip there. And also wondering if you’ve got any comments around some of the Lightning communities that are sprouting up now. What’s the deal with these? Why would you want to use those?

Jestopher:

I love the communities. Huge shout-out to Plebnet of course, with their girthy channels and just hilarious references and just a really helpful community. The other ones, the Netherlands—I had no idea there were so many people running nodes and they have a robust community from—a tiny country is apparently just full of Lightning nodes. And we get a significant amount of traffic from the Netherlands. And then the last one that I really want to give a shout-out to is Diamond Hands community run by Koji and that’s out of Japan. They’ve got a very pay-it-forward mentality—get people set-up on the Lightning Network and get running nodes. It’s fantastic to see.

Tony :

One of the very cool things to see is that if you’re just getting into Lightning, if you’re just trying to get set up and trying to learn and trying to see what it’s about, join one of these communities. It’s the best decision you can make. If you, for example, join the Plebnet Telegram chat, ask any question that you want, and there will be like 50 people ready to help you, ready to get you set up, ready to open some channels to you. So it’s a very, very strong community and it’s so helpful for others that are just joining and want to learn about it.

Stephan Livera:

Awesome. So yeah, these communities have really come a long way in a short period of time, because I think if you went back even two years ago to 2019, it was more like people would just hang out in developer chat groups. And it was like, you had to—you basically were a developer. But now it’s like, you don’t necessarily have to be a developer, there’s just Lighting routing node specific Telegram channels and things going. So different ways of people to learn and operate. So I think we’re pretty much coming close to the end of time. So can you guys let everyone know where they can find you online and if they want to find out more about what you guys are doing?

Tony :

On Twitter I would say is the main spot where we are, I’m there as @tonyioi.

Jestopher:

I’m on there as @Jestopher_BTC and our Amboss account is @ambosstech.

Stephan Livera:

Fantastic. So listeners, go and check out Amboss.space and follow the boys. And yeah. Thank you for joining me guys.

Tony :

Thank you so much for having us! Really awesome talk. Thank you.

Jestopher:

Great to speak with you, Stephan.

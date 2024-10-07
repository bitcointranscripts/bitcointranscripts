---
title: Is Consumerism at Odds With Privacy in Bitcoin? JoinMarket, PayJoin, SNICKER
transcript_by: Stephan Livera
speakers:
  - Adam Gibson
date: 2020-02-16
media: https://stephanlivera.com/download-episode/1769/149.mp3
---
podcast: https://stephanlivera.com/episode/149/

Stephan Livera:

Adam, welcome to the show.

Waxwing (Adam Gibson):

Hello, Stephan,

Stephan Livera:

Thank you for joining me. I’ve been very keen to have you on the show. I guess some listeners will know you as Waxwing you’re probably more known as Waxwing than as Adam.

Waxwing (Adam Gibson):

Little bit more. Yeah, yeah.

Stephan Livera:

But yeah, I’m a big fan of your work. I really like what you’ve done in terms of putting a lot of educational stuff like your blog and your work with JoinMarket and obviously you’ve got a, a history within the space and a focus on, I would say, you know, Bitcoin privacy and also around the cryptography and the mathematics behind it. So yeah, I think obviously you’ve done the origin story. I’m sure you’ve done many but if you could just give just a basic background on yourself just for any listeners who don’t already know you.

Waxwing (Adam Gibson):

Sure. my background is sort of a mixture of engineering and teaching. Especially mathematics teaching. I mean, my degree is in mathematics and physics and I’ve done various kinds of I’ve been a nuclear engineer and a software engineer for a big financial corporation, so that background. So, but actually I didn’t really take any interest in cryptography until Bitcoin came along. And I guess I actually took an interest in Bitcoin. Like I said, it was 2012, 2013 because of the kind of political, and especially the financial and economic aspect, you know, the financial crisis stuff. Like most people I struggled a bit to convince myself that Bitcoin actually made any sense. But once I did off the, you know, having an engineering background, even if you don’t have a cryptography background helps you in that you can look at the white paper and kind of make sense of it.

Waxwing (Adam Gibson):

You know, it’s very difficult even if you do have the technical background. But without it, it’s even harder. Right. So because I had that background, I sort of got interested and then that sort of spurred further interest in, well, you know, how does this actually work? At the deepest technical levels, you know, the mathematics behind it, the cryptography behind it. And I really clicked for me after Bitcoin. Why cryptography? And especially public key cryptography is such a huge deal for society. And so I’ve now continued to just take an interest in, in that area, you know, the, the privacy of this digital cash that we’re using and the different techniques we can use and the mathematics behind all that.

Stephan Livera:

Yeah. Fantastic. So look, let’s start with I guess just broad thoughts on privacy right now. So Bitcoin right now it’s one of those things where you get some people who might falsely believe, okay, I just use Bitcoin and I’m private already. And then the other end of the spectrum is, Oh no, the whole thing is transparent and everyone can see everything and, it’s like somewhere in between, depending on how good you are with it. How would you sort of summarize that?

Waxwing (Adam Gibson):

Yeah, I mean that’s, I remember giving that exact kind of summary, excuse me, that exact kind of summary. I don’t know, a few years ago in Milan, there was some presentation. It was just you know, up til some point around 2012, everyone just assumed Bitcoin was anonymous and then something happened. And by, by time we got to like 20, I don’t know, 2016, everyone assumed Bitcoin is perfectly traceable. And if people, I guess it’s just people need shorthands for things in life, things that they can’t study in detail themselves. They want a nice simple summary of something, but unfortunately some things by their nature and not simply summarize bubble. But I think my, sort of broader philosophy on you know, where we are with privacy in Bitcoin and other related technologies that I think, I think we have a kind of, I used to like to express the problem as a, as a category error.

Waxwing (Adam Gibson):

I used to kind of rail about this on Reddit years ago. I used to tell people, stop thinking of Bitcoin. Like, you know, Starbucks points. I used to say it’s more like Swift, not Starbucks points. And by Swift of course, I mean the, the the bank transfer, international bank transfer system. I don’t mean anything to do with Apple code or whatever. So what’s my point is that there’s a tendency, and I think it’s very deeply rooted in us. Maybe it’s exclusive to Westerners, I don’t know. But people who live, in our kinds of societies we have this very consumerist mindset and it’s so deeply embedded that we don’t even aware of it. You know, we tend to think of everything in terms of, you know, how convenient is it? How does it immediately like press my buttons, you know, does it look nice and shiny?

Waxwing (Adam Gibson):

Right. I mean this may seem slightly off topic cause I’m not actually talking about privacy directly, but I think you’re going to see, I’m going to try and convince you that there is actually a pretty close connection because you know, people want a nicely packaged things like, you know, nice UIs. It’s very understandable. They want that. But no matter how nice the UI is, the underlying thing itself is extremely kind of hardcore. You know, it’s a protocol and it’s very much based on a kind of adversarial model of defending against massive attacks. When you’re a user of that protocol, you’re supposed to hold these keys. And that’s just something that people have never really done in the past is taken full responsibility. It’s a bit like, you know, people didn’t store their gold, the gold bars in their homes, you know, they used banks and there were all kinds of problems with that.

Waxwing (Adam Gibson):

But ultimately that’s the kind of trade off people tend to make. And people, you know, they want something comfortable and simple and something that doesn’t force them into very difficult situations all the time. Right? So there’s a tendency to think of how can we make Bitcoin like that? How can we make it a nice shiny app that, you know, make it like FinTech, you know, just I just Stripe or something or whatever the latest app is that people use to pay with Venmo. But you’re trying to fit a square peg into a round hole. I feel when you’re doing that and you should, I think we should think of Bitcoin itself as this very kind of not user friendly, not easy to use protocol, but that doesn’t mean of course that we should give up on allowing people to use it. That of course we should make things as feasible as possible, if that makes any sense.

Waxwing (Adam Gibson):

But we should think about ways of doing that, that are kind of somewhat offset from the protocol directly. You know, raw protocol usage is not an everyday person thing. And I know a lot of people would like it to be and of course huge strides have been made. And just simple things like the fact that you can run a Bitcoin core net node now on your laptop isn’t tremendous engineering achievement, but it still doesn’t mean the average person’s going to do it. And that’s relevant to things like JoinMarket. It’s relevant to things like any kind of coinjoin in my opinion about, you know, best practices and about privacy that it’s fiddly and difficult. It’s, it’s, it’s, it’s a technical question like how can you use Bitcoin in a properly private when, so perhaps in the longer term we’re going to have this kind of stratification so that yes, privacy at the base layer is something we work on.

Waxwing (Adam Gibson):

We’re never going to make it perfect, but we work on it, but it’s more at the kind of higher end, you know, lightning is the obvious example where we’re going to find ways for ordinary people to achieve better privacy.

Stephan Livera:

Right. And I think in your blog you mentioned this idea of lightning privacy bleeding into the base layer, if you will, of Bitcoin.

Waxwing (Adam Gibson):

Yeah. I mean, I really regret not having sort of, I mean, apart from a very trivial proof of concept, a piece of code, I haven’t really attempted to write any, any, any code for that. But I mean, perhaps we’re going to get into the weeds. We can get into some of that later. Yeah. But, that’s certainly an example where we can even that’s an even more sophisticated way of looking at it. Right? Because you’re now saying it’s not just that we have like a base layer and high layers, but also we can interact between them in certain ways.

Waxwing (Adam Gibson):

You know, which is definitely true. Yeah. Good point.

Stephan Livera:

And I think the point you’re also making is that the use of lightning can fundamentally change some of the underlying assumptions about the behaviors on Bitcoins, on chain traffic in, in that sense.

Waxwing (Adam Gibson):

Yeah. I think, but I think that’s, that’s a natural evolution that’s likely to happen, at least in an optimistic scenario that the, the, the character of behavior on chain chain is going to change dramatically. It’s going to be more in the longterm settlement style transactions. I mean, I sort of envisage it like, you know, large corporations or even governments, you know, transacting on chain and, and individuals can, you know, appeal to it as a, as a sort of last resort. But often we’ll, we’ll probably not be doing so directly. I know, I know this is this kind of thing that absolutely, massively triggers a lot of a very large section of our current community and especially people who have left our community. Should we put it like that? Yeah. Bcash and all the similar areas of groups of people. It’s not just them of course, it’s people who went to different altcoins. They get very triggered by this idea that, well I think what people are suspicious of is the idea that always just gonna fall back to what it was before, where you have these centralized parties controlling everything and you know, and the ordinary person can’t use the, the chain or something. But I just don’t think this, I don’t think the successful scenario for Bitcoin could, could realistically be different. Maybe I’m just lacking imagination.

Stephan Livera:

Let’s stay broader for one. I’ve got one other question I was keen to ask you about. We’re living in this world where today essentially many aspects of our privacy have just been pwned, right? Like,

Waxwing (Adam Gibson):

yes,

Stephan Livera:

your IP, like depending on who you’re trying to hide from or whatever, right. The NSA can pretty much get through. Most things like people talk about even using even Tor is not a silver bullet and that’s just that the IP kind of network level then like your data has been basically sold and used by Google and Facebook and Apple and all these people.

Stephan Livera:

Is it, would it be fair to say that in Bitcoin it’s like you’re not necessarily going to be able to get to the level of privacy versus a targeted attacker, but at least if you could get to a level of like some kind of privacy versus the Dragnet surveillance. Do you have any reflections on that idea?

Waxwing (Adam Gibson):

Yeah, yeah, absolutely. I do. I do think like that. And I think it also ties back in again, your comments about Google and Facebook and what have you to this, this thing about the consumerist mindset, which I was maybe, I didn’t really fully explore what I was trying to say there, but I’m trying to get at the idea that if we really, if you want to be part of this sort of new cypherpunk world, so to speak, involving, you know, actually using Bitcoin, not just, you know, going to Coinbase and buying some or whatever, then you’re going to have to kind of toughen up a bit and stop, you know, this, this incredibly soft world we live in where we just, we just give in all the time, just take the easy way out.

Waxwing (Adam Gibson):

I’ll just use Facebook because everyone’s on it, you know, and Oh yeah, I heard that these terrible, terrible privacy violations. But you know, at the end of the day, people just don’t care enough. And I think if you, if you find that you do care enough, then yeah, join us and be part of this, this whole experiment. But you can’t, what I’m trying to say is you can’t have your cake and eat it. You know, you can’t actually be, Oh, I’m just going to go back to the normal consumer mode of doing things. And if I’m going to have a Bitcoin wallet, it’s going to be on my phone and that is just going to be one click and I’m never going to have to do anything. My bank is going to be hooked up to. Well look. I mean, if you’re going to be like that, then you’re just, it’s the same as Facebook and Google on all that stuff. Of course, everything’s going to be tracked, everything’s going to be traced, and it doesn’t matter if you’re using some incredible zero knowledge proof or whatever, because all you’re doing ultimately is hooking your name up to some service provider and having all your data flow through them anyway. So, you know, I’m sort of ranting the same thing over and over again, but you get my general point.

Stephan Livera:

Sure. so look, when we’re trying to be private in Bitcoin, there is a lot of different ideas floating around. Some of them are more, let’s say theoretical and some of them are a little bit more kind of here’s something practical that a person could really use. And like over the years, many people have thrown out a lot of different ideas.

Waxwing (Adam Gibson):

That’s right.

Stephan Livera:

It’s kind of difficult. So, and I guess the other point is that there’s not really like a, I think you were making this point earlier is that it’s not like there’s a prescriptive do X, Y and Z and you’re safe. There’s this kind of, there’s certain tools you can use and they can give you a better chance.

Waxwing (Adam Gibson):

Well I don’t know if this is too nuanced, but you can take a very prescriptive approach. You can decide that there’s this set of steps that one must take.

Waxwing (Adam Gibson):

The question is, of course, how practical that is. You know we look at something like a ZeroLink, the whole kind of project from the Wasabi guys. It’s an attempt to do like, and I don’t really know if it’s fair to say, but I think Samourai in a way, those guys also have their own way of looking at it, which is kind of similar in that there’s, there’s rules you need to follow, right? But ultimately life is messy. You can’t, I mean especially with something like financial transactions, you can’t like control every single aspect of it all the time. So, but perhaps a more important or deeper point is let’s say you did, you were able to follow those kinds of strictures. Like I’m going to control exactly how I spend every UTXO. So on every circumstance, even if you can somehow like arrange for that to be the case, I personally think that that is a, a road which has sort of diminishing returns.

Waxwing (Adam Gibson):

Like it, there is definitely value in it. If you want to be very serious about your privacy, there’s definitely value in, for example, just simply coin control. So instead of just arbitrarily spending actually controlling which groups of coins get spent together. But the problem, when I say diminishing returns, what I mean is that the, it’s the nature of Bitcoin is that it’s a very transparent system. Okay. Especially if we just consider it as it is today. And when you combine that fact, so there is just the fact that there is a transaction graph alone. Even if you had blinded amounts, which we don’t, and you combine that with metadata there are just so many avenues of attack the that’s why I would tend to be on the side of what you were saying earlier, which is that if you’re trying to defend against targeted attacks, you know, something like Bitcoin, good luck.

Waxwing (Adam Gibson):

I mean, it’s almost impossible, right? You’ll have to be very clever, but that doesn’t mean that we just throw the, throw the whole idea of privacy out and we just all forget it. But if we, if we use kind of what I would describe as opportunistic methods well I guess there’s two kinds of methods that I really like. One of them is the more sort of opportunistic and the other one is the kind of steganographic. So the opportunistic method is I’m just going, I just want it to be fairly normal for me to do, let’s say a coinjoin now and again,

Waxwing (Adam Gibson):

And I’m not actually that focused on it having a specific pattern necessarily. I mean it might be nice, for example, it has a larger and anonymity set rather than a smaller one. Yeah. But really I’m over a long period trying to improve the score, so to speak, privacy health of my ecosystem. And that word ecosystem brings up the other point of course, which is that it’s crucial or at least it’s, there’s a huge magnifying effect from the more people you get involved doing it. And the more heterogenous the group is that does it, it’s not just having a large number but having different types of people, you know. So if, if only exchanges do one method, then you oh, those – You want the exchanges and the consumers and the businesses and all the other people just doing, you want it mixing up.

Waxwing (Adam Gibson):

So that’s the opposite opportunistic idea that I’m not actually aiming to say that by March the first I have perfect privacy on all my coins or the 10,000 unlimited, he’s out, whatever. But I’m just trying to incrementally improve the situation over time, which if you’re an ordinary person, I I feel like that’s okay. I mean you’re not on some secret mission. Right. and then the steganographic idea again the key point there is that you’ve kind of blown up this concept of anonymity. So it no longer matters if nobody can distinguish between your type of transaction. And another one, unfortunately, I don’t really think I was thinking of this on the car, on the way here. I don’t actually think any of the ideas of steganographic like privacy or maybe I’ve missed one actually exist yet, which is kind of unfortunate, right?

Stephan Livera:

Just having it like,

Waxwing (Adam Gibson):

Well, PayJoin in JoinMarket technically exists, but it has to be two JoinMarket wallets. So that’s.

Stephan Livera:

right. Yeah. And we’ll get to that part. I think about potentially having more people do that are one point I was going to touch on as well. And I’m not sure if you listened to, I did an episode with ErgoBTC and he’s come,

Waxwing (Adam Gibson):

I listen to some of it, but I’m not sure now.

Stephan Livera:

Yeah. And so in that episode, one point he was trying to make was that actually Bitcoin can be more private. It’s just a, right now the start, we’re giving the enemy in some ways a start point by having this KYC and the data sharing between the exchanges. Right. So imagine if the standard way you came into Bitcoin was like you had a friends and family network. Right. And it’s, and again, I’m not saying, look, KYC exchanges are not going anywhere anytime soon. But imagine if that were the case and then people are using coinjoin and someone, or even if they weren’t, it would be much harder to pierce through that transaction graph veil. Right?

Waxwing (Adam Gibson):

Yeah. I definitely always a huge is a huge issue. And I think it somewhat ties in to my little rant, which I may end up renting again about this. So stop me if I do, about consumerism because people, they just want to click the button on the website that they trust. They don’t want to mess around with some weirdo and go, I mean, people treat even the idea of doing a Bitcoin exchange for cash is, you’re some kind of weirdo. I mean that, no, come on. This is, this is how we have to do it.

Waxwing (Adam Gibson):

We have to have some kind of peer to peer activity so that ultimately there’s some, you know, people talk about closing the economic loop that will be great. I mean, we’re obviously a huge way away from that, but if we just make at least make some moves towards it which is why I get a little bit upset about this whole, you know, which I consider this kind of tribal viewpoint that’s developed of HODL HODL HODL and you know, Oh, you’re an idiot if you spend Bitcoin. I mean, there are several reasons why it’s actually kind of interesting to spend Bitcoin. I understand like if you say you’ve got a job and you, you earn fiat money and you sock some away into Bitcoin every month, it doesn’t really make much sense for that person financially to be spending any of their Bitcoin. But even in those, but those people as an experiment, I think you should try it.

Waxwing (Adam Gibson):

You know, it’s important to actually understand what it is you’re investing in because yes, this is not a consumer payment system. It’s not Visa, it’s not, you know, Venmo, but the other extreme is also a mistake, you can’t say it’s not a payment system. It fundamentally is a payment system. And that’s why it’s, in my opinion, people argue about bootstrapping value. You know, is it just all relative is actually, there’s nothing has absolute value. Okay. Technically, but actually the value here is that there is a payment system and it’s not censorable otherwise. Why are we even bothering, right?

Stephan Livera:

I think of it like for many people it just makes sense to HODL, right? But there will be that phenomenon and you might call it something like a, graduating like people that came to Bitcoin in 2010 and 2011 they’ve graduated and now they actually do want to spend some Bitcoins because they’ve just hit a certain level that okay now it makes sense but someone from the, let’s call it class of 2017 and 2018 they just want to HODL or stack.

Waxwing (Adam Gibson):

But my point, my sort of counterpoint there was that yeah, you might be in a position where financially it doesn’t make sense to spend Bitcoin, but I still think you should try it out as an experiment. Not talking about spending all of your money it and actually using the technology.

Stephan Livera:

Right.

Waxwing (Adam Gibson):

Cause you know, a lot of store people who have stories like, Oh I got into Bitcoin when somebody just like put it on my phone and I just act. The actual act of seeing it being transferred is in itself. Yeah. And I, it kind of upsets me a little bit that there are people nowadays are just like, maybe you set up an account on Coinbase or whatever it is, and they just, they never do anything that just seems wrong to me.

Stephan Livera:

Right? Yeah. No, I absolutely always preach self custody. Right? Yeah. So even for those people buying on an exchange, they should be withdrawing two keys they hold. Obviously there is that debate about, you know, KYC and not KYC. But I think more broadly, let’s go to some of these heuristics, right? So as most of probably my listeners are probably well aware, the common input ownership heuristic is probably the key one to think about. How does it look like in a world where, where, you know, we’re trying to break that. And I think it might be interesting if we were, let’s say, able to have more people using wallets that helped, you know, break that heuristic. Would that heuristic then no longer apply? Is that, is that what you’re kind of thinking?

Waxwing (Adam Gibson):

Yeah kind of, yeah. So I think it’s, it’s like I, I know this is a very pretentious term, but I’ve been taking to using it recently in these discussions is the term shelling point. And just in case anybody’s listening who doesn’t know the term shelling point, it’s the idea that if I tell you, let’s meet in New York and you don’t know the location you’d, you’d pick grand central station. Cause that’s the one that everyone knows. It is a convergence of people in a state of low information, convergence to one most plausible possibility. And what we have today is a perfectly reasonable situation where you know, you look at something like if you look at something that has let’s say one, two or three inputs and two outputs, then the assumption is that it’s a payment from one person to another. Actually you’d have to make this, let’s just keep it simple.

Waxwing (Adam Gibson):

It’s a payment from one person to another with one change output. And that’s why there are two outputs, one’s payment and one’s change. And the other assumption would be that all the three or one or two or three inputs are owned by the same person. And that’s the default assumption because of course that’s the way Bitcoin is most easily like works and the way most people still use it today. So that, part of that assumption as I did, I just mentioned is what you call the common input ownership assumption. A heuristic a, which is just saying that every time that a transaction consumes more than one input, those more than one inputs are owned by one person or one party.

Stephan Livera:

But in the world where that heuristic no longer applies, what does it look like?

Waxwing (Adam Gibson):

Yeah, so what, what that could mean is it could be the case that a coinjoin just be, let’s be crude about it. Let’s say coinjoin was used more than 50% of the time. So somehow that shelling point flips and it’s no longer the natural assumption that all the inputs are owned by one party because in a coinjoin, by definition, that’s the opposite is the case that there is more than one person involved in creating the transaction and contributing inputs. So if that happened it would break the most. I think it’s fair to say that that’s the most central assumption of blockchain analysis. There’s, there’s a lot of other factors to it and I can’t even call myself an expert at it, although I know obviously some parts of it, probably the experts are people sitting, in those companies who really spent a lot of time finding lots of clever heuristics. I don’t know how many they, I mean I think they kind of oversell their skillset actually, but they certainly have done a lot of work in terms of like finding ways to make connections.

Waxwing (Adam Gibson):

But this is the most fundamental one because it allows, it’s like the cornerstone of what’s called wallet clustering at least sometimes it’s called wallet clustering. Sometimes it’s called closures, which is the idea that what you, what you can do by kind of repeatedly applying that heuristic is build up whole sets of UTXOs or I should say TXOs cause first they’re unspent and then they become spent. Right. So building up whole sets of those TXOs and saying oh, all of that set the ones that were spent, you know, two weeks ago and these other ones over here that aren’t spent yet, all of those are owned by the same party. So it would make that, it would make that very difficult or I won’t say impossible, but I’ll make it a lot more difficult to do that.

Stephan Livera:

The thing is that it’s just difficult to get enough people using that. But like you say, the showing point, it’s just kind of, it depends on what wallets people are using if they’re using, you know, so on the coinjoining wallet and today there’s only, well there’s not that many coinjoin wallets. And I guess that is also a heuristic as well. Like if a certain wallet can get,

Waxwing (Adam Gibson):

yeah. I suppose my, my discussion just a moment ago is, is a bit missing the point, isn’t it? Because if we’re talking about current coinjoins and not future plans for like in quotes, steganographic coinjoins, then it’s not really the case as far as I know what’s happening today is that where there are big coinjoins like Wasabi or Samourai or JoinMarket because they are easily identifiable as coinjoins. And I don’t even know if this is completely true cause we hold, have that whole thing about the fixed address, you know, but at least in principle, the blockchain analysis companies could be flagging anything that has the pattern of a multiple equal output coins or, and that’s, that’s the key feature.

Waxwing (Adam Gibson):

There are other features you can look for in these, in these transactions. But the key feature is having multiple outputs at the same amount. That is obviously a massive flag that says this is a coinjoin because there’s, I mean, of course that is not fact because people do make fake coinjoins as well. But, let’s say, so what I think from, I’ve heard second, third hand, you know, what blockchain analysis companies are doing is simply flagging them and saying that is a in quotes mix, but not attempting to trace through it because you fundamentally can’t really, but I think there’s more they could do. For example, they could trace the change and connect the change with inputs. Maybe they are doing that and maybe they’re not, I don’t know. But they, they can’t fundamentally trace through the, the equals sized output. But so, so what’s my point?

Waxwing (Adam Gibson):

My point is that is that doesn’t, that’s not the same thing as if we had coinjoins, which weren’t obviously coinjoins because in that case they might be trying to apply the common input heuristic and being wrong in applying it. And in fact that that’s not even theoretical. That’s a fact because going back even several years, wallet explorer.com which was the first like public blockchain analysis facility that was available to the public. Yeah, I remember explicitly like trying addresses that I had from JoinMarket and plugging it in there. And seeing it connected to Mt. Gox. Right. Cause it was in a cluster. It was this massive cluster, which they’d erroneously assigned me as having the same being the same person as another person I’d coinjoined with, you know, many of them in fact.

Stephan Livera:

And that who knows like those coins might have come a long way before they got to you.

Waxwing (Adam Gibson):

Just a complete mess. You know, it perfectly illustrates the fact that that blockchain analysis is kind of snake oil. I mean, it’s a bit sort of click baity to say that, but there’s an element of truth to that. You know what I mean?

Stephan Livera:

And look with the blockchain analysis companies or whatever, chain spies or whatever you want to call them, they have some blog posts and they talk about, Oh this is how we got the criminals and whatever. And typically when you look at those, oftentimes it’s the, it’s that the criminals weren’t very sophisticated that they were doing address reuse. So in your view, how much of this privacy problem, how much of that is address reuse? Like, not even just like a, you know, they’re just simply not even using HD wallets, the listeners HD hierarchical, deterministic. Well it’s meaning you generate a new address rather than reusing addresses. So Adam did you want to comment just on address reuse?

Waxwing (Adam Gibson):

Yeah, I mean I the, I’m just trying to think of examples where I’ve read in the past, whether it be blockchain and ICO company blogs or similar analyses of criminal cases. And the one that always springs to mind is that guy with incredible name like Carl Mark Force IV or whatever you remember or you don’t read this. I’ll start this crazy story about the silk road case where the, the two of the FBI, I know, I think one of them was FBI agent the other was a secret service agent and they ended, it turned out that, I mean these were the guys that are arranged the fake hit right. But one of them, at least one of them ended up being criminal themselves in that they were they took a whole bunch of money out of the silk road account cause they got admin access, whatever.

Waxwing (Adam Gibson):

And tried to sell it, well not try to, I think he did sell it maybe by BTC E or something. But when the whole case came to light and the guy was put in prison of course, but when the whole case came to light, they showed how they’d in quotes traced it on the blockchain and all he’d done is he’d taken out one exchange, put it into his wallet and put it into another extent. So he had his name on both the exchanges. So what exactly is the blockchain analysis?

Stephan Livera:

And it was fully deterministic spends the whole way.

Waxwing (Adam Gibson):

It’s not like there was, I mean one transparent about like 2013 yeah, 2013 years. Cause when he was actually doing it, I mean even dog, while it didn’t exist then it’s not like he really had such an,

Stephan Livera:

didn’t have the tools,

Waxwing (Adam Gibson):

but he could have at least used a mixer because they had centralized mixes.

Waxwing (Adam Gibson):

They were already a big thing in 2013. But no, he just like took our one exchange, put in his wallet and then sent it to another one. Well, you know, good luck.

Stephan Livera:

Right? Yeah.

Waxwing (Adam Gibson):

Well, even just like one or two hops would’ve at least been something. Right?

Stephan Livera:

Yeah. Like yeah, that would’ve been something, right. I guess. And for most people nowadays, even if they’re not doing any coinjoining, but they’re at least not reusing addresses when they withdraw from an exchange after it’s already gone through a few hops, the trail is going cold there, right? Yeah.

Waxwing (Adam Gibson):

But it brings to mind this case that’s topical isn’t it? That I got quite confused about. And I wonder if you have more information than me, which is this case where now if I get it right, I think it was Binance Singapore, right?

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

And the guy said his funds got frozen after he had sent coins into a Wasabi mix.

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

I might be getting confused with the two cases. I think there was a second case and the second one was the one that confused me because I think he said that he went through one hop and after that he went into coinjoin.

Stephan Livera:

That’s right.

Waxwing (Adam Gibson):

So to Electrum and, or was it Electrum or was it Samourai Wallet?

Stephan Livera:

Let me break that down. So the Binance Singapore, so what we’re thinking of as the first case is actually I think the third case where something like this has happened, but that Binance Singapore case, that individual withdrew from Binance Singapore into Wasabi wallet and then directly, and then they did the coinjoin and because of the fixed fee address, which as I understand Wasabi are changing now as there’s been a big debate about that.

Stephan Livera:

But again, this is that question of proximity versus fingerprinting. And so in this case, that address got flagged because of proximity with the Wasabi mixing and.

Waxwing (Adam Gibson):

Possibly because of the plus token.

Stephan Livera:

Exactly. Right, exactly right. I think it’s mostly because on these blockchain analysis people on their terminals or screens or software, it’s saying, Hey, this is linked with PlusToken.

Waxwing (Adam Gibson):

I think you’re probably right.

Stephan Livera:

And so their analysis tools are probably not yet sophisticated enough to be doing fingerprinting. They are sophisticated enough right now in terms of the proximity. Now, of course, maybe they’ll just code up a new thing and look at these equal outputs, right?

Waxwing (Adam Gibson):

By Proximity, I think you mean like taint analysis, right? Just basically saying there’s a lot of sense, huge percentage relationship between this address and this address.

Stephan Livera:

Closeness to these known bad address right now the second case you’re speaking of I think the individual’s name or the Twitter name was Ronald McHodled. That’s right. Yeah. And so in that example, they withdrew from Paxos as I understand. And then they went via Samourai reason being Paxos does not have bech32 send. So they went via Samourai then into Wasabi and then got done again for the proximity. So that’s what happened.

Waxwing (Adam Gibson):

So your point, your fundamental point, I think I agree with you, is that the reason, even though there’s hops, that that still doesn’t take away, this is what you call proximity, where I’m thinking of it as taint. Yeah.

Stephan Livera:

Taint yeah.

Waxwing (Adam Gibson):

I think that must be the correct answer as to what’s going on. But it’s horrible. We have to kind of guess really, thjey’re black boxes. I mean that’s the thing that just enrages me about this is they’ll go to some law enforcement and they’ve literally, there’s been court cases, I mean, Sjors Provoost the dutch guy, you know, the Bitcoin core dev, he’s really good on this. He’s done some he’s dug up some cases in the Netherlands and he’s shown cases where like the prosecution has said, look, this blockchain analysis company told us that this happened. And the defense say, well, can you show us the reasoning and say, well, no, you’re not allowed to. So how is it allowed? Somehow the judge allows it as evidence even though there’s no actual explanation of what they’ve done. I mean, that’s so dangerous.

Stephan Livera:

Yeah. Yeah. I’ve heard in the U S where there have been literally been cases where people have gotten let off from really horrible crimes because I think it was the FBI, one of the three letter agencies did not want to disclose their exact evidence. And I think in the U S I don’t know the exact law, again, not a lawyer, but there was, there’s some ruling or some law that essentially you’re allowed to see the evidence and because they didn’t want to disclose, they kind of said okay fine, and then because they were a US citizen,

Waxwing (Adam Gibson):

That’s how it should be. Yeah. I mean surely that’s obviously, yeah, it seems obvious to me, right? Yeah. When it comes, but there is a pattern you’ll notice where in when it comes to financial things, you know, they, they use this term money laundering and it basically absolves them of the need to actually prove anything. I mean all this kind of civil forfeiture is another facet of the same thing. They’ll just take money and say, well, yeah, of course prosecute the money. They’ll say somehow that means that they, the police get it and you get, you get nothing. You know,

Stephan Livera:

It would be like if you were, you know, you were making a cash payment to me and I’d have to say no, wait, this cash, this $20 note you gave me, who had it before you and who was the guy two hops before that? And it’s just like stupid, right? But nowadays in this digital world, that’s the reality where we’re moving into and that’s why.

Waxwing (Adam Gibson):

So convenient they make this ethical exception for money, right? Like if a criminal uses a car, the car is not like a know Trey, you’re using the same car. You don’t get put in prison, but somehow with money, it’s conveniently the case that, you’re a criminal by association you know?

Stephan Livera:

I guess, again, I agree with you, but I guess there are some laws about things like knowingly using stolen goods and things and maybe that would be like a parallel there. Anyway, let’s bring it back to the privacy aspect. So I think one fundamental problem right now is even, even if you did kind of the right thing, so to speak, and you used these coinjoin techniques and so on, you could still get done by fingerprinting because there’s other ways of wallet fingerprinting such that they might know, ah, yes, based on the construction of this transaction, I can tell it’s a JoinMarket or I can tell it’s a Samourai wallet. And examples of this might be, I think Chris Belcher has spoken about this, he mentioned nlocktime or potentially nSequence. So could you actually, would you mind just outlining a little bit around how wallets do nlocktime?

Waxwing (Adam Gibson):

Yeah. So and lock time is useful in cases where you well you, it can be used if you want to use the check lock time verify feature. Okay. So you want to actually like control and say this output cannot be spent before a certain block, which is useful in some, you know, contract kind of relationships, protocols. But there’s also.

Stephan Livera:

isn’t there also like an anti fee sniping thing?

Waxwing (Adam Gibson):

anti fee sniping thing. Now you’re testing me here cause I can’t remember, but there’s, there’s a rule where if you want to use RBF you need to.

Stephan Livera:

signal something.

Waxwing (Adam Gibson):

I can’t remember. It’s one of those things I always have to look up, right? But the reason it came up for me personally was because when, this was my perspective on it, when I decided to implement page on, which we might talk about later in, in JoinMarket software, I realized that hang on, this is a bit different from JoinMarket coinjoins, right? What we do, JoinMarket coinjoins, we’ve got a very special structure and it will be absolutely pointless to try and emulate let’s say Bitcoin core or Electrum or anything else in our kind of, as you say, fingerprints nlock time is a fingerprint. The version number is a fingerprint and these little bits of data in a transaction which could make it stand out. And I realized when I was doing PayJoin, oh, this is not the same as like JoinMarket coinjoins.

Waxwing (Adam Gibson):

I should try to make it as much as possible sort of hide in the crowd to make it look similar to let’s say a Bitcoin core transaction or a perhaps an Electrum transaction. I, the reason I keep mentioning Electrum along with core is because I think that they’re both very similar and that the two perhaps of the biggest, probably biggest, yeah. Wallets. So what I had to do then was exactly what you’re mentioning is called anti fee sniping. And I don’t remember the details of the either the, I don’t remember the logic of like the setting of nsequence and nlocktime off the top of my head. And I don’t remember the whole argument behind anti fee sniping, but I do remember that. I just made sure that I did the same. So as far as I remember, it’s something like in Bitcoin core the algorithm is something like a set the nlocktime to the latest block. But with some small probability you set it to some blocks behind or something like that.

Stephan Livera:

Right. And I think the idea is it’s to stop miners doing the fee sniping aspect. So maybe it’s maybe, maybe we’ll just have to let someone correct this, but it might be something like maybe it’s something like a CLTV, but for minors kind of thing, like to stop the miners being able to, having an incentive to maybe fee snipe, something like that.

Waxwing (Adam Gibson):

I can’t remember the argument I’m sure as I recall, it wasn’t too complicated when you’re right, it’s to do with mining and it makes perfect sense. But the reason it’s a bit confusing is because this, the rules for both RBF and CLTV are a bit obscure and it’s, you both have to consider the n sequence value as well as the n lock time value.

Waxwing (Adam Gibson):

And nsequence is the sequence number that’s set on each input. And the n lock time is an overall setting, was just put at the end of the transactions here.

Stephan Livera:

and there’s some other wallet fingerprints as well. So the ordering. So, as most people will know, there’s inputs and outputs in every transaction and then the wallet has to order those. And then the, the zeroth and the first input, you know, the ordering that it puts them, well it might put the change output first and I might put it last.

Waxwing (Adam Gibson):

you might, in theory, but in practice there’s only two options that are ever used, right. One of them is just completely random using a random shuffle from whatever your local software library is telling you is random. It doesn’t have to be cryptographically random. So it’d just be random.random() in Python or whatever. That’s one option. The other option is only subtly different, which is BIP69, which is lexicographical ordering, which is effectively random. But it just, it just chooses to do, make it random in a way that is verifiable to all parties. So, I mean, people have subtle arguments, pros and cons of the two methods, but the difference is fairly minor, to be honest.

Stephan Livera:

So actually on that question, I’ve heard of some browsers trying to do this. I’m not sure if browsers do do this browser fingerprinting.

Waxwing (Adam Gibson):

Yeah.

Stephan Livera:

So yeah, but as an anti fingerprinting tool, I’ve heard of one browser, I won’t name just in case. But the idea is that you would look at what I’m most other people are doing in terms of like what fonts do you have installed, what’s the resolution, what’s your, this, that and the other, and then bluff as that or spoof your values of that. Would it be valuable someone to do that in terms of Bitcoin wallets and say, okay, most people are signaling RBF most people are signaling this [inaudible].

Waxwing (Adam Gibson):

Do you mean dynamically, I guess, as opposed to, because I think that that’s happened currently. Wallet developers sit down and think to themselves, well, which set do I want to be a part of? I want to be a part of the biggest set. But the problem is often the reason somebody sitting down and writing a wallet is because they have some special, unique feature about it. And that means that they can’t know. The obvious example is Blockstream green, right? Which uses a customized.

Stephan Livera:

G pubs in instead of like X pubs. And,

Waxwing (Adam Gibson):

Oh, I didn’t even know about that. But I know that they have the sort of multisig setup and is, it’s their own special thing. So while they can’t realistically hide in the crowd, let’s say Bitcoin core transactions or as far as I understand it, maybe there’s some exception to that rule. But you know, the, my general point is while it developers, as far as I know, we’ll all think about this and try and try to, if they can join, join the party so to speak, but oftentimes quite a lot of limits. Yeah. And I mean, in the case of JoinMarket, and I guess the same is true of Wasabi and Samourai. There’s, there’s this kind of almost flip case where, well, no, it’s the same case where you just have no chance of hiding in the crowd. Your transactions are very obviously flaggable. So there’s pretty much no point, which is of course, why Wasabi originally was saying, well, what’s the point in changing our, our fee address because we are completely transparent anyway. And I don’t want to get into that argument cause people got to be,

Stephan Livera:

Right. Yeah, sure, people are going to come at you for it. But look, I guess the other point, the other way to think of it is maybe you can’t necessarily bluff as you know Bitcoin core, but maybe then the question is building up a big enough user base such that you have enough of an anonymity set. But then the question is how many Samourai wallet users are there, how many Wasabi users, how many JoinMarket users out there. And as you said, we’re living in a very consumerist short time horizon society. So they’re not necessarily going to be thinking about yeah. Using these privacy tools.

Waxwing (Adam Gibson):

Yeah, exactly.

Stephan Livera:

Great. So look what about with let’s say we get Taproot and then that might be another vector for fingerprinting, right? Because at the start not everyone will be using Taproot and then again they will start distinguishing being say, Oh that’s a taproot output. I know that’s a, that’s a segwit.

Waxwing (Adam Gibson):

And we had the review thing. I remember making that comment but I felt guilty making a comment cause it’s not very helpful is it? I mean obviously it’s the case. If you’re trying to create a new thing that’s better than an old thing than initially it’s going to be worse.

Stephan Livera:

But I think, I think with taproot, most people accept it’s a short term pain for long term gain.

Waxwing (Adam Gibson):

And that’s the idea anyway. Yeah. But, but there’s an important point there I think, which is that there needs, well not needs to be, but there ideally should be an economic incentive to switch and not just, this is something we’ve often discussed in the kind of Bitcoin privacy community is, we’re never really gonna get there unless we can find ways to make it not necessarily more convenient but at least cheaper to do like say coinjoin and not the coinjoin.

Waxwing (Adam Gibson):

Maybe that’s just too optimistic, but there are, you know, the obvious one is input aggregation, input aggregation. Signature problem with that is that it, it sounds nice but it really just incentivizes the cocreation of transactions. What it doesn’t incentivize is actual anonymity sets. Because, you know, if I do my payment transaction with you together but that’s all we’re doing. Like I’m making a payment output. And a change out, but you’re making a payment out with a change bowel. But they’re obviously extractable. You can easily see by looking at the values that we see without blinded amounts let’s say, but doesn’t actually incentivize coinjoin in the sense that we mean it incentivizes it in the completely trivial sense of putting inputs and outputs together. It doesn’t actually create privacy.

Stephan Livera:

Right. But it doesn’t, I guess. Okay. So this is, that’s an interesting one as well. So we could talk and we could talk about that idea of multiple interpretations on a transaction. Right, right. And I think we’re kind of here, we’re going into like the Boltzmann and Stonewall conversation as well. And I think you had a great so a couple of years ago, just background for the listeners, there was a get hub, just think of like a little blog page if you’re not familiar. And basically LaurentMT from OXT.me and which was later purchased or merged with Samourai wallet. So part of the Samourai wallet team put out this idea of Boltzmann and essentially as I understand it, it is around trying to assess the amount of entropy in the transaction and the entropy across the blockchain. And the, I guess the argument from Laurent and the Samourai guys would be something like, look, high entropy does not necessarily mean you’re safe. It’s more just like low entropy means bad and it means if your transaction is deterministic i.e. I know exactly my, you know, if I, if I send you all of with one input, all of it, it’s clear that I owned it, right. There’s 100% link, you know. And so I guess the idea that it’s coming from like the Samourai team is something like if you can craft your transactions in a way there are that, there are multiple interpretations of it. It can look like a coinjoin. Now you had an interesting back and forward there maybe you could just offer a kind of a high level comment on it and then whether your view has changed over this time.

Waxwing (Adam Gibson):

Sure. So the, the, it seems like the, how do we explain this? Cause it’s, I personally found it confusing, so I’m not sure when I first read it. So I’m not sure how easily I’m going to explain it to people. But, so first of all, the concept of entropy, it comes from physics and it’s a measure of, it’s literally a measure of the number of ways you can arrange something. So a crude example to, to illustrate entropy is a shuffled pack of cards is in a, is in a high entropy state and a ordered pack of cards where the cards just go one, two, three, four is a low entropy state.

Waxwing (Adam Gibson):

Because think of it as like if the cards were just randomly thrown together, they wouldn’t naturally, the probability of them being thrown together in a way where they’re all in order is extremely low. Right. So that’s considered a low entropy. Okay. So with what as I understood Laurent MT was doing in his analysis there it was, he was coming up with a measure of the number of different interpretations of flows of funds through transactions. But the reason I had a bit of a problem, I mean obviously I can’t give you the full spiel like here’s the formula and here’s a different example. It’s too complicated. But the reason there was a bit of a back and forth between me and him about that was because I had a feeling that it wasn’t more just a feeling. To me it definitely doesn’t give an accurate sense of the, how to say it, the plausible deniability or the different interpretations of a transaction.

Waxwing (Adam Gibson):

There are, so maybe a simple example might be well even, even the very simplest possible Bitcoin transaction is, is illustrates the point I think. Cause if you have one input on one output in that Boltzmann model, that’s what there’s one interpretation cause there’s only one kind of fund flow going on. Yup. But if you think about it there’s at least two, I guess there’s only two interpretations if you’re thinking of it in terms of entities. So it could be me sending to myself. And in fact, if you go on, what does it blockstream.info today, they have the very primitive chain analysis feature where they add some little notes to every transaction, possibly a coinjoin, and you know that you’ll see ‘possibly a coinjoin’ for things which are definitely coins. But you’ll also see probably or possibly a self transfer if you see a one input, one output.

Waxwing (Adam Gibson):

And of course that is not only technically, but actually not a certain deduction is it is clearly the case that you could be sending it to someone else. So in my way of looking at it, I think it’s far more useful to call that a transaction with two interpretations than one and if you go and so when we have the little argument on the, on the gist, I ended up saying, Oh, I see what you mean. You’re distinguishing between link entropy and node entropy. So and I think he uses those signs and I agree with him. So, so node entropy by node I would mean like the individuals or the all the entities like making transfers between each other and the links would be like the flows of funds and in the case of something like a coinjoin. So when you, when Samourai are building coinjoins, it makes perfect sense to look at the link entropy as a measure because it’s saying how many different like ways could the funds flow between these clearly multiple entities.

Waxwing (Adam Gibson):

Right. But I’m more focused on this idea that we want to maximally encourage confusion and uncertainty about the interpretation of transactions in general. Yeah. In general by using opportunistic methods, but especially by using steganographic methods. And that would, in that case, you really want to focus on the other number. So a good example is like , I’ll probably forget the correct number, but if you had a two input to output transaction, you can use what’s called in mathematics, the bell numbers to the formula to calculate the number of different kind of partitions is the technical term for it of that set. And it’s surprising even at a small scale like two and two I think you end up with 15 different interpretations. And at first that sounds too high, right? Because you’re thinking like, or maybe there’s one person paying or maybe it’s a coinjoin with two inputs.

Waxwing (Adam Gibson):

So there’s two people paying. So how is there really going to be 15 but there really are, because think of it that every time you have an extra element, either an input or an output, that could be another person. So the most complicated case could be with two in and two out. It could be Alice and Bob pay, Charlie and David. So you could have, you could have one person which is a completely fake two in two out coinjoin or just just a random pointless to self transfer. You could have two people and there’s multiple ways that could be a range. And then you could have three people. There’s multiple ways that could be arranged, right? For people, there’s a kind of only one really, because you know, there’s no point just switching them around. So anyway, if you do all the counting out you, you come to 15 and then if you go to to like five bits, you know, three in two hour or two in three hours, something the number starts to really blow up.

Waxwing (Adam Gibson):

I think it gets to like 52 or something when you,

Stephan Livera:

when you’re with this kind of different perspective?

Waxwing (Adam Gibson):

from what we were calling in that in that discussion node entropy, which is like which I think is the more important, okay. So upshot is there’s two different ways of looking at it, right? And I think both are valid and I certainly see why he did that the way he did it. But I have a, an sort of allergy to what I think Taleb calls the, the ludic fallacy, which is where you, you tend to like over emphasize things that you can make mathematical formulas for.

Stephan Livera:

Right? This is looking for the keys where the street light is rather than it could be anywhere on the road.

Waxwing (Adam Gibson):

Yeah, it is. It is of that, that general sort of paradigm. It’s specifically the one where you, because you can quantify something you, you place more importance on it than you actually should.

Waxwing (Adam Gibson):

And maybe that’s overstatement, but I think people should at least consider that, you know, there’s a certain a huge amount of uncertainty in, in the nature of Bitcoin transactions, which ultimately comes from one key property, which is the fact that as I said it before, Satoshi’s are not watermarked. This idea that it’s a many input and many output mapping and as long as you actually make use of that, you’ve just intrinsically got ambiguity in where the funds are flowing. So you see even in like the OXT or whatever entropy model is, I think it’s a fair statement that that model assumes no payments. I’ll have to think about that actually. But because the natural way it works is that you’ve got a coinjoin, and there’s, there’s clearly like matches between inputs and change by doing subset sum. Yeah. But then you don’t actually know which output is going to which party. So you sort of have these multiple combinations. But if that was a coinjoin, which one of the parties was paying one of the other ones or something that you didn’t, you know what I mean? I think I could possibly break even, even from its own perspective that, that I could find some weird arrangement where I don’t want to, cause I’ll probably, I might be wrong. So.

Stephan Livera:

Okay. All right. Yeah. So look, let’s see. I think there were a couple of technical terms and things we might just explain for the listeners as well. So we’ve got two things here. So OXT.me, which is like the, like a block Explorer. And then there’s another tool which is also run by the same team. It’s KYCP.org and that one, I think that’s what you were also referring to there Adam, where you might see, okay there’s three inputs and three outputs or two inputs into outputs. And then it’s trying to draw the links there and that’s where, you might’ve seen the green and the red and the yellow and the probabilistic links versus deterministic links. And so what it’s trying to get at there, and that’s coming to what you were saying with like with the two input two output, was it really, where there’s a different perspective that you’re offering here, which is around node entropy as in who’s, which who are the parties behind it.

Stephan Livera:

Whereas the Samourai approach if you will, is more like a transaction entropy, a linkage model. And I guess so I want.

Waxwing (Adam Gibson):

Before I just want to say I don’t want to disrespect any of the work, especially LaurentMT, I think he’s doing incredible work over the years and continues to, and with the KYCP.org I can never remember which, how many letters it is, I’ve only actually looked at it a few times. It’s not like I know in detail how, all the things that they’re doing, but I am, I’m just, I’m expressing, I’m asking people to be a bit more, skeptical of being too concrete in that kind of analysis. I think that’s really all I’m saying. And it’s not that I think that their science is wrong or something. I’d probably, if I did a detailed analysis, I’d probably find things I disagreed with. But and I also think it’s a valuable service to actually give people something to look at. But, I just want people to be a little bit – try to avoid the trap of just falling into, Oh, this is just like a button I have to press.

Stephan Livera:

and now I’m safe.

Waxwing (Adam Gibson):

Now I’m safe. This website tells me I’m safe. That’s what I’m worried about. And vice versa, people thinking that, Oh no, this is clearly this, this, this coin went from here, like traced through 10 different transactions because some website told me. So, whereas I gave the example of Wallet Explorer completely wrongly associated my addresses with Mt. Gox I mean, what if I did ended up in court or something because of that, you know? Did you see what I mean?

Stephan Livera:

Yeah, yeah. I get you to be careful is what I’m saying. Yeah. And in fairness, I think most of the, the times that I’ve seen like the Samourai guys talking about it, I think most of them have kind of railed back against this idea of so-called perfect privacy and that that’s, it doesn’t exist. And really it’s just, you know, you use certain tools and they may improve your odds. I think that’s how I’m, at least that’s how I’m thinking of it. But I think it also comes to how holistically you’re looking at it as well, because here’s an example. You might be not segregating your coins. So, for example, you might have, if you had some coins that you got from a KYC exchange and then some non KYC coins and then if you sort of merge them or spend in such a way that an outside observer is able to cluster that altogether,

Waxwing (Adam Gibson):

Is able to attempt to cluster. They don’t know because, right?

Stephan Livera:

That’s right. That’s right.

Waxwing (Adam Gibson):

They can attempt to cluster, the common input ownership heuristic may be false.

Stephan Livera:

That’s right. That’s right. And so I guess it comes to, yeah, that, that point. And also one other point I think would be good to touch on. You mentioned earlier subset sum analysis. Could you just break that down for the listeners?

Waxwing (Adam Gibson):

Yeah, so that’s just the simple idea really. If you have a bunch of numbers especially if you have two, well, if you have two sets of numbers you know, like, I don’t know, one, two and seven on one side, and then you have three I don’t want to add all this up. Three, four, and eight. I don’t, that doesn’t quite match. What I’m saying is that I could take the one in the two in the first year. That adds up to the three in the second set. Yeah, so I found a subset of the first day one and two which is equal to a subset of the second set. In that case it’s just one number three but it could be multiple numbers.

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

So when you look at a Bitcoin transaction, let’s say a coinjoin transaction, because that’s where it’s most interesting, where you’ve got lots of inputs and you’ve got lots of outputs and what you’re trying to do if you’re trying to disentangle the coinjoin as best you can, is you’re trying to find sets of the inputs which add up together to sets of the outputs. And the assumption is that it’s a coinjoin where each party is, is not paying all the others, but it’s just getting back the same amount they put in. So I put 10 Bitcoin into a coinjoin, let’s say in the form of a one, a three, and a six Bitcoin inputs. I’ve got three Bitcoin inputs, one, three and six total. 10 and my outputs, I’ll have two outputs. One of them is five Bitcoins

Waxwing (Adam Gibson):

And the other one is five Bitcoins. But the first five Bitcoin is, is equal to – That’s a bad example cause that’s two. Yeah. I’ve got one output which is four Bitcoins. And there’s a bunch of other for outputs of equal size four cause that’s the coinjoin effect. The, obfuscation effect and my other outputs six because I need to get my change back. So as each individual in the coinjoin is getting out what they put in although that’s not exactly true in JoinMarket, which we might mention later.

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

And it isn’t exactly true anyway cause of fees, transaction fees. But generally, you know, with a certain tolerance, if you’re a blockchain analyst you can say, well I’ll just give it like a 1% wiggle room. But basically if I can find sets of inputs that add up to sets of outputs, I can assume that they’re correlated.

Waxwing (Adam Gibson):

And of course the fly in the ointment there is that one of the outputs is equal to a bunch of other outputs. So you don’t know which one you should associate to that subset. So subset sum analysis is, is how you, at the very least, you’re going to be able to extract common inputs and change outputs in a standard classical equal output coinjoin. Now we can also have a varied, what’s it called again? Varied size, coinjoins without.

Stephan Livera:

like unequal

Waxwing (Adam Gibson):

unequal mixing, whatever we can, in other words, we can just abandon that whole idea of having equal size outputs to create a specific and obvious obfuscation effect. And then we try and rely on a kind of combinatorial difficulty of the problem of finding subsets. But that’s a highly controversial topic. And I guess it’s a bit technical as well, so.

Stephan Livera:

Right. Yeah. And this is part of the debate around, you know, it zero link and actually having, you know, zero deterministic links. I think one other point that comes to my mind is whether the mixer is trying to deal with these inside the mix or does, does the fees sort of outside the mix.

Waxwing (Adam Gibson):

Oh the fees, you’re talking about fees now.

Stephan Livera:

Okay. Like the, yeah. Or for the, I guess that that’s one part of it. But yeah. Look, also I wanted to just quickly talk about, cause we talked about subset sum analysis and you mentioned coinjoin XT this idea of trying to break that with lightning.

Waxwing (Adam Gibson):

Yeah. This is, an idea that I think I’m forgetting the years now, but I think I presented it in 2017 in Lisbon.

Waxwing (Adam Gibson):

I hope it was 2017 and yeah. Now you mentioned it, I’m trying to think what was the line of like process of thinking that led to this? It was something like that. Was it? Yeah. Because it was shortly after SegWit had activated and obviously SegWit has this really cool property that it allows you to build. And this is actually something that’s written explicitly in the BIP. And I don’t think many people pay any attention to it, but it explicitly says, you know what you can do, you can build sets of transactions in advance and pre-sign them. And of course, that’s what lightning does, right? But that’s just one way of using this feature that SegWit has. You can make transactions in advance, pre-sign them and you can be sure that they’ll be valid if the kind of starting transaction actually gets mined, you know?

Waxwing (Adam Gibson):

And somehow or other I came up with the idea that to improve the, yeah. Okay. So one goal you might have is you look at something like JoinMarket or Wasabi, and you say, well, that’s great and everything, but I would prefer that my transactions aren’t obviously coinjoins and can easily be flagged as coinjoins. Right? And so when we use the word steganographic, we’re referring to the idea that you could make a kind of cryptographic or a hiding effect, but without making it obvious that you’ve done it or an obfuscation effect without making it obvious that you’ve done it. So obviously JoinMarket doesn’t have that property, Wasabi doesn’t have that property. PayJoin does, which we’ll probably talk about in a minute, but this was an idea that I thought might actually be even better than PayJoin in a way, which was to do coinjoins, but to have them kind of spread over multiple transactions.

Waxwing (Adam Gibson):

So the simplest example would be if you Stephan and me, arrange. Now let’s say we both got, I don’t know, five Bitcoins to mix, and instead of just creating two equal size five Bitcoin outputs or whatever size, let’s instead pre-sign two or three transactions. And in one of these transactions I’m going to be paying you four Bitcoins. And in the other transaction you’re going to be paying me four Bitcoin. So the outputs won’t look like equal. Okay. But the trick of it is that we won’t have to trust each other because we use, this is the negative, or at least it was before Taproot. The negative of this is it requires multisig to enforce the contract so that we both know that we, the other guy can’t just cheat us by running away halfway through like say after the first transaction.

Waxwing (Adam Gibson):

You’ve got four from me and then you don’t bother with the second one.

Stephan Livera:

With honoring that initial deal.

Waxwing (Adam Gibson):

Yeah. So, but very much like lightning and these other systems is that you, you can use like a multisig address as a kind of an enforcement mechanism to make sure that that is possible. I’m sort of, umm’ing and ahh’ing cause I’m not sure how much detail to go into.

Stephan Livera:

Yeah, sure, sure. No, that’s fine.

Waxwing (Adam Gibson):

I’m trying to give the listener the, the general concept and the concept is that once we agree between each other, the pattern of transactions we want to make, so it’s not just one transaction. It could be three, four, 10, whatever. Then with a little bit of playing around, we can make sure that with a quick interaction between ourselves, it could be like, it’s sub-second, right, we’re going to set, basically send signatures back and forth in the same way as they do in lightning. On these transactions that we pre-agreed and only when everything looks right at the very end, do we then say, right, everything’s correct. I’m going to sign and actually put money into the funding transaction, the actual start of the process.

Stephan Livera:

Right, yep.

Waxwing (Adam Gibson):

So at that point, that’s where it all gets committed. And then when that funding transaction gets mined, either of us have the option at any time to broadcast the rest of the transactions on the chain. So if one particular transaction in the chain favors me and not you, you don’t have to worry cause you’ve got, you’ve got the ability to broadcast it anyway without my, without my say so. So the extra kind of like, okay, so there’s two extra things that, that’s the basic idea and there’s two extra things that make it more interesting in my view. The first extra thing is that you can, using a backout transaction, so using locktime, again we were discussing earlier, you can like feed in other UTXOs along the chain.

Waxwing (Adam Gibson):

So it doesn’t just have to be a simple like long chain of transaction. It could be like a tree and even better a tree maybe is a bit fancy, but even better is you could, you could add other UTXOs further along in the path. So it’s not cause otherwise from chain analysis point of view is a bit too simplistic. Just having one entry point into such a thing.

Stephan Livera:

Yeah, I see what you’re saying.

Waxwing (Adam Gibson):

Nice to have multiple entry points. So that makes it more confusing. So, but then the final sort of end point of this, so I call it coinjoinXT is a kind of joke, but because this was around the time when you know.

Stephan Livera:

BitcoinXT, yeah.

Waxwing (Adam Gibson):

you know, but the final phase of it was the reason you mentioned subset sum was because no matter how clever that is, and I think it is very clever and I think even on its own is like really good anti blockchain analysis feature.

Waxwing (Adam Gibson):

Cause they won’t know which transact, they don’t know. Like there might be a set of 10 transactions in a relationship and yeah, they’ll all be connected. So there’ll be what we call contiguous technically, you know, they’re all connected together. So it’s not like atomic swaps where the transactions are disconnected. So you might think that’s bad. But the blockchain analysis, doesn’t know where in the whole transaction graph this set of 10 is. So if he’s looking for such a thing, he’s got to find the entry point and do all the analysis and all the transactions. But the small weakness that still remains is subset sum analysis because if we’re not actually paying each other, if we’re actually doing a mixing transaction or multi-stage transaction like this, we’re still in the situation where you’ve got five at the start and you got five at the end and I’ve got five the start, and I got five at the end.

Waxwing (Adam Gibson):

So even though these amounts are like split across multiple transactions, that is still possible statistically to disentangle and say, Oh look, there’s a subset across this multiple transaction, contiguous subset of the graph. I can add them all up and I can see they add up the inputs add up to the outputs across multiple outputs.

Stephan Livera:

But wouldn’t that be kind of assuming we both sent it back to our own cold storage when maybe we would have spent some of that. And now some of that’s off with the merchant off on its own.

Waxwing (Adam Gibson):

Exactly. If you no, hang on, no. If even if you’re doing, let’s say we set up 10 transactions in a big set and like the seventh one you pay a merchant.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

Even if we did that, which isn’t very practical cause you’ve got to wait mess around. It doesn’t break the problem on talking about does it because it doesn’t, you see what I mean?

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

It’s a separate flow. It’s the same with like anyway. Yeah. So that doesn’t break it. But what I spent a long time trying to think of how on earth could we possibly break that and I realized that it doesn’t, it can’t conceivably make any sense to break that subset sum analysis possibility without a cross payment between the participants.

Stephan Livera:

Right.

Waxwing (Adam Gibson):

But then I realized that, I mean, you could argue, this is kind of silly, but I actually, I don’t think it is silly, is if we make the outputs dual funded lightning channels, the advantage of that is the, of course in lightning, you already have this nice property that you’re not exposing on chain who’s paying who.

Waxwing (Adam Gibson):

But by doing that, the final state of the channel when it finally gets closed. However, long that is, the final balances of the two parties are not where they were at the start. And that that’s not because, let’s say I was paying you, but because I was paying Charlie on the other side of the world, right? So that’s really cool. And so I think you already mentioned the phrase I use for that was bleeding the privacy of lightning back onto the main chain because what the beautiful thing about it is, because it breaks that whole subset sum for that whole set of 10 transactions, it, it breaks the ability of the blockchain analyst to even find that set of 10 transactions because they won’t have a subset sum fingerprint.

Stephan Livera:

Right? How much of that is just generally lightning? Like, I mean, even just generally, just say you ran a coinjoin and then, those coinjoined funds are sitting on your LND node or your c-lightning or a eclair node and now you just open channels and you just use it like, I mean, obviously it’s not perfect, but you have some level of privacy there.

Waxwing (Adam Gibson):

So my theory about that was that definitely for sure like 90% of what you’re gaining, or, I wouldn’t say 90%, but a lot of what you’re getting there is coming from just lightning being lightning. So obviously you want to use lightning and dual funded lining, which is a bit of a hot topic on the mailing list at the moment. Yeah. Is a really cool thing for improving privacy. But the difference here is that you could be, and I would estimate maybe a 10 times multiple, you could be mixing much larger funds than you can actually mix on lightning in this mechanism.

Waxwing (Adam Gibson):

And also of course, you can also say technically that it has a nicer property in terms of like, the security properties of on chain payments as opposed to lightning payments. But so it’s not the I would disagree at all that the lightning and especially dual funded lightning, is the most interesting thing there. But I still think it’s very interesting to have it so that I’m able to do sets of transactions on the graph and have this kind of, you think of almost like a, leaky faucet or tap, you know, if there’s this little leak somewhere and it stops the whole thing from actually adding up properly. Yeah, that’s my theory.

Stephan Livera:

Yeah. And I guess it just kind of, it’s sort of really gums up the works there.

Waxwing (Adam Gibson):

Yeah.

Stephan Livera:

So let’s talk about PayJoin now. So pay join, it’s this it’s this way as you mentioned I think listeners would know it as, so there’s two inputs and two outputs and let’s say I’m paying you, you’re the merchant, you’re actually contributing inputs to that transaction. And an outside observer does not know that that is actually a coinjoin. And they also do not know the amount being paid.

Waxwing (Adam Gibson):

Correct? Yeah.

Stephan Livera:

Yeah. And so when it comes to PayJoin, I know it exists right now, but between two JoinMarket wallets and also between, two Samourai wallets.

Waxwing (Adam Gibson):

That’s right. Yeah.

Stephan Livera:

So right now there is that question of, again, how do we get that interactivity across wallets? Do we need a standard? Would it involve, you know, PSBT from our friend Andrew Chow and I know you have a big beef with Andrew Chow. Haha.

Waxwing (Adam Gibson):

(Laughing).

Stephan Livera:

Nah we’re joking about this.

Waxwing (Adam Gibson):

Yeah, Andrew loves me. Really? That’s the truth. Yeah. it’s just, that’s all for show. What was, yeah, no PayJoin yeah.

Stephan Livera:

PayJoin. And how would the wallets, do you think there’s a way that wallets will be able to communicate that cross wallet type?

Waxwing (Adam Gibson):

Yeah. yes. Obviously that’s, that’s, that would be the goal. So I think it’s certainly fair to say in JoinMarket’s case that it was just intended as a proof of concept. It’s functional code. I’ve, tested it with real coins with people and it works. But because JoinMarket, it doesn’t have very many users. It’s, and even if it had let’s say 10 times more users, I still think it’s fair to say that that kind of payment, I’ve always felt it’s not a huge, I mean it comes back to our earlier discussion at the beginning. Like if everyone in the world is like actually using Bitcoin for real as payments, peer to peer payments, not through exchanges, what have you, then of course all these tools become a lot more feasible and important. But obviously it does seem fairly obvious, doesn’t it?

Waxwing (Adam Gibson):

That we should have a standard and not just having individual wallets implement their own version of it, that’s just terrible. But I only did it just cause I wanted to show people that it’s possible that I did it. And I had the same thing with SNICKER, which was like, SNICKER is an interesting idea, but if it doesn’t exist, well, you know, so at least in that case I actually wrote a draft BIP. Whereas with this one we had, I mean there was a Blockstream blog post and there was a couple of other blog posts here and there, including one of mine. But I think partly the reason you don’t see like some draft BIP for PayJoin is, I’m probably gonna say something wrong here cause I’ve probably forgotten things. There’s all kinds of initiatives all over the place, but I don’t think there’s been a settled decision on, Oh, that’s right. I remember now Ryan Havar, that’s his name. Wrote a draft BIP that he called, like Bustapay because his business was Bustabits. And so that’s why he called it Bustapay but I did say to him you know, “You can’t use that name though”.

Stephan Livera:

Right.

Waxwing (Adam Gibson):

That’s just a terrible idea. But he wrote a draft BIP, actually I remember now, and this was probably about a year ago and myself and David Harding I think were perhaps the only two people to really like maybe a couple of other people that were involved in the discussion. But I wrote some detailed notes on it. But for some reason that I didn’t understand, he didn’t want to alter any aspect of the draft and I just felt like, so we’re just kind of stuck. I mean, I could write another one and then that probably go nowhere as well. But I do think it’s a shame because I think that protocol as you quite correctly point out, really needs some kind of standardization, some kind of oomph behind it.

Stephan Livera:

End point as well. Right. It was called endpoint,

Waxwing (Adam Gibson):

which is a fair enough name in a way technically. But I was trying to convince people at the time that, no, just call it PayJoin. But the thing is I think perhaps there’s a reason why it hasn’t kind of really taken off is, is, is when I thought about this idea and I think I was thinking about at the same time as CoinJoinXT because I kept focusing on this subset sum problem. And I realized this general principle that the only way to break subset sum is to actually have payments involved in the process. But I never really took it very seriously because I felt that this is not something. Interactivity from the receiver is just a bit icky. But there is a huge, I’m torn on it because there’s a huge incentive to do it because as you say, it’s this fantastic property that it is both steganographic and it’s even like ambiguous on amount, which is an incredible achievement.

Waxwing (Adam Gibson):

Okay, well incredible, not achievement, but it’s incredibly nice thing to have. To be clear, it’s not like you’ve got no idea the payment amount there. There’s essentially two, if I remember correctly, there’s two possibilities if you know it’s a PayJoin. Yeah. But the other possibilities, if you don’t know it’s a PayJoin there might be four, I’d have to remember, but it’s anyway, it’s not like an infinite number of possibilities is this. There’s an enumerable set of different payment amounts. But I did this little trick. I remember at the time when we were, when I first coded it, I was like, I put it up on Mastodon or whatever, and I said like, Hey, can anyone tell me what the payment amount of this transaction was? It might have been on Twitter in those days. I don’t remember. But anyway, so like one person says, Oh, it’s obviously this and like, Nope, try again.

Waxwing (Adam Gibson):

And there’s other guys, like a really, really smart guys made some really clever statement, but that was wrong as well. And it was just so beautiful to see like in real time that people just don’t know what the payment amount is. And that’s so cool.

Stephan Livera:

Yeah. Well I think one good hope is hopefully with BTC pay server, right? Because it is a persisting, it’s a server, it’s already there. And if you’re a user, you might pull out your phone and you might have to do a couple of rounds back and forward of scanning back and forward. Right now I know if you want to do it with Samourai wallet and you want to do a, in Samourai model in the Samourai Wallet model, it’s called stowaway and it’s a payment between two Samourai wallets and they have to do a little bit of scanning back and forth.

Stephan Livera:

And I think it’s like what two rounds each.

Waxwing (Adam Gibson):

No, it’s like four or five QR codes and I was just like to Laurent, I was like, why is it four? It only needs to be two surely. But there’s some technical reasons why they want to do like four.

Stephan Livera:

I think it’s two each. It’s two each –

Waxwing (Adam Gibson):

so yeah, four and then.

Stephan Livera:

I think it’s four and then the broadcast.

Waxwing (Adam Gibson):

Yeah, it’s a lot of steps. I mean, come on.

Stephan Livera:

And there’ve been times I’ve, sometimes I’ve been able to get it successful and other times I’ve tried it and it failed, so. Yeah.

Waxwing (Adam Gibson):

But yeah, ideally, I mean you’ve, it may have been you, I’m pretty sure it was you and other people have said this to me when I get, when I get pessimistic about it, they say, well don’t forget like BTCPay already does lightning. So it’s not like receiver interactivity is not a thing. It’s already a thing. So maybe you’re right. Maybe we should be optimistic and maybe we will get sort of some kind of PayJoin thing on BTCPay Server, which would be great. Yeah.

Stephan Livera:

Yeah. And especially with so many people using it as well. But yeah, look, let’s talk about JoinMarket. We’ve got a, you know, we’ve got the JoinMarket OG here.

Waxwing (Adam Gibson):

Well not the JoinMarket OG, the second OG after Chris Belcher, who’s the originator of the project, so.

Waxwing (Adam Gibson):

Yup. Yup. So let’s talk about maybe you just give us a high level overview. What is the maker taker model?

Waxwing (Adam Gibson):

Okay. So so Chris Belcher came up with the idea of JoinMarket, I guess. I guess it was like November, December, 2014 and started talking about on IRC and I thought, yeah, that works. And what was his idea, which was simply to do an arbitrary size coinjoin is difficult because you have to get, when I say coinjoin here, I’m specifically not referring to these new ideas of PayJoin or steganographic, but the old idea of lots of equal size outputs. So, and he was saying that it’s difficult to coordinate that because you’ve got to get everyone else to agree on your output size. So obviously one approach to that is to have a centralized party like in case of Wasabi or where you and Samourai actually where they decide the amount is 0.1 or whatever.

Waxwing (Adam Gibson):

And that’s perfectly natural and that’s a model that, you know, it makes a lot of sense. But there is another possibility, which is Chris Belcher’s idea was to have one party be one of the peers in the join to decide the amount, but to have to pay for that privilege. And what they’re essentially paying for is the sort of liquidity to access that join. So they want to do a join, let’s say of 0.2436 Bitcoins or you know, any arbitrary amount. And you know, ordinarily a bunch of other people would maybe be interested in doing that or they might, but it’d be difficult to find them. But if they’re offered a feed to sit around waiting for you to turn up and say, I want that, then they may well be prepared to do it. So that’s like using a market to solve a coordination problem.

Waxwing (Adam Gibson):

And so to be more specific, the advantages of the taker, who is the person who is taking the offer. So let’s say the makers are sitting around and they are making offers and they literally publish a string of text saying I will do a coinjoin between 0.0134 and 2.76 Bitcoins. So there’s many people like that sitting around. I mean currently today there’s like a hundred and something of them sitting around and all different amount ranges and what have you. So the taker comes along and he wants to do a coinjoin of 1.246 Bitcoins right now with let’s say 10 counter parties, that’s a kind of typical situation.

Stephan Livera:

So yeah, going back into it. So, JoinMarket has this a order book and you can go on, what’s the website? JoinMarket.me/ob and you can see all the people who’ve got offers up there. There’s some people that put some pretty big offers up there, but anyway so CoinJoins need a coordinator. So who coordinates in the JoinMarket?

Waxwing (Adam Gibson):

Right? So the, the taker is, this is what’s very unusual about this model is that the taker is the coordinator. And what it means in practice is that the taker actually has the full mapping of inputs to outputs. So the taker is paying, if you think about it for, I think it’s correct to say three things. One of them is, is to not have anyone else know his mapping. That’s the first thing. Assuming that he’s not dealing with all sybil. If everyone else is a sybil, then he’s lost the game no matter what cryptography you use.

Stephan Livera:

Right.

Waxwing (Adam Gibson):

So assuming they’re not all sybils and he actually has some heterogeneous set of people talking to him he pays to actually have his linkages not known by anyone at all. He pays to get the coinjoin done immediately rather than wait around a week. And he just as importantly pays to get the exact amount he wants. He also gets to choose how many counterparties he has as well. So he’s basically in control of everything and he pays a fee for that privilege. Of course that’s inferior like as a privacy model to models where there’s some cryptography used to blind the linkages from anyone, for example, CoinShuffle or the Chaumian server model, which kind of relies on Tor thing or network disconnection anyway. so what’s my –

Stephan Livera:

yeah, yeah, that’s, that’s good. That’s it. And so you mentioned sybils as well. So what is a sybil?

Waxwing (Adam Gibson):

Okay, so the concept of a sybil attack is just, just means the idea that if you develop a protocol where there are multiple participants involved and you have to be a bit more careful to think about, what do you mean by multiple participants, right? Because you know, in the physical world with a bunch of people, you can see individual people, but if you are deciding that, you know, if you see different like network level, people you don’t necessarily know that they’re actually different physical people. They could all be the same person coming over, say multiple IP connections or whatever. So if it turns out to be cheap for one reason or another for a single entity or single person to spin up multiple protocol people so to speak, then we call that a sybil attack. I don’t really know the origin. It’s something obscure, why they call it sybil. But the the idea is in some protocols it could actually be dangerous or have a very bad effect if there are lots of participants, which are actually all controlled by one participant. And obviously coinjoin is one of those protocols where that’s true.

Stephan Livera:

Right? And so comparing some of the different models in the past, they were, I think there were some custodial mixes, right? An example that got shut down was bestmixer.io and so on. But when we’re dealing in the world of non-custodial mixers such as JoinMarkets, Samourai, Wasabi they, that is one of the risks. It’s dealing with sybils. And I said the fundamentally, as I understand you, the problem is that you may be mixing with all that one person and that other person will know the mapping. And then basically doxing.

Waxwing (Adam Gibson):

Maybe am I right to correct you here because it’s kind of weird, but if you think about a centralized mixer in a way it’s the same problem. It’s just kind of offset a little bit because you give your money to the centralized mixer. But the assumption, or maybe maybe I’m not right in saying this, but you’re kind of assuming that lots of people are using that mixer cause if you’re the only one using that mixer.

Stephan Livera:

Oh same problem,

Waxwing (Adam Gibson):

you’re kind of screwed, so, so.

Stephan Livera:

Good point..

Waxwing (Adam Gibson):

Yeah it is more complicated in that case though. But certainly for the noncustodial it’s very clear because we could just random people turn up and they’re almost by almost always going to be turning up in some anonymous way.

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

Because they want to protect their privacy. This, is a very like recurring theme when you get involved in coinjoin and privacy type software is you, it’s just so difficult sometimes. Like I get people coming onto an IRC channel and saying, you know, this coinjoin I tried to do, it didn’t work. Okay. Right. Can you, can you give me any information? No. I’m not gonna tell you the amount. I’m not going to tell you the addresses. I’m not going to tell you the Tx ID, I’m not going to give you the log files. I was like, yeah, we get through it. But, but it’s a curious thing. Problems specific to this kind of software as if you were just working, I don’t know, making graphic software or games or something. People would just give you the logs. Right? They,

Stephan Livera:

so there’s a bit of it. Yeah, it’s a bit harder to do.

Waxwing (Adam Gibson):

And I think one of the reason I, I’ve made it was a silly statement, but the reason I mentioned it, it was because sybil problems are really hard to deal with here, because we because our users are very strongly demanding of privacy every level and they should be. And I, it’s really good. Our connections that the messaging service we use doesn’t hold the information because we end to end encryption between each individual pair of parties. The connections being made are almost exclusively to hidden service. These IRC servers, they’re hidden services. I mean, you can actually connect over clear net. We don’t stop people doing that. Well maybe we should but, I don’t know. But almost everyone uses the hidden service. And so we take all these measures and so how do we deal with sybil attacks in that case is I guess your question, right?

Stephan Livera:

Yeah. And I think Chris has this idea of a fidelity bonds maybe, maybe I’ll try and cover that in another episode with Chris. I guess that’s just kind of the high level.

Waxwing (Adam Gibson):

Maybe, but I would just just perhaps mention one other thing. Cause I think very few people know about it. And it just cropped up recently in the context of the text of dual funding lightning, which is that in the middle of 2016 we had a kind of attack on JoinMarket as a system where what people were doing was acting as takers, not as makers turning up, making requests and then not continuing and completing the protocol. And the sort of the negative effect of that is that as part of the initial setup of, in the first few messages passed back and forth, the makers were handing over UTXO information to the takers. And this is where it crops up in something like dual funded lightning or any really any scenario where people are trying to cooperate to create transactions between anonymous entities.

Waxwing (Adam Gibson):

You’ve got this kind of like who goes first problem?

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

And so what we, what we did, what we did then, which I think is interesting and I’m not claiming it’s some perfect solution, but it was an idea Greg Maxwell suggested to us in the at the time, and he just dropped this idea and said, see if that works.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

So I looked it up and I thought, wow, actually kind of works. The idea is that you make what’s called a discrete log equivalence proof and it’s basically just a cryptographic trick that allows you to sort of say, I’ve got, I’ve got this UTXO, and it’s worth this. It’s worth a certain amount, not up to a certain value and it’s at least a few blocks old. And, I’m going to give you the commitment to it in advance as the taker and you as the maker will be able to tell if that’s been used before without knowing which UTXO it is.

Waxwing (Adam Gibson):

So it’s not like it’s revealing the takers UTXOs, he has to reveal after we’ve actually constructed the you know, but, in the initial phase, it stops them from just like pinging and just get millions and millions of.

Stephan Livera:

right, just like the farming the info from everyone.

Waxwing (Adam Gibson):

And this crops up, like when we talked about PayJoin, it was the same kind of question cropping up. Like, Oh, we’ve got to worry about what if the customers like ping the merchants and just like, let us do a PayJoin –

Stephan Livera:

just learn their UTXO set.

Waxwing (Adam Gibson):

And then you go away and you do that again with someone else or maybe the same guy again. So this, this problem keeps cropping up. Besides, I’ve mentioned that, we called it PoDLE or I wrote a blog post its stupid. I called it poodle in the blog post. But if you look on my blog, you’ll see that that was one of the earliest posts on that.

Stephan Livera:

Oh, great. Yeah, I’ll have to go and check that one out. Okay. So look, I think maybe we can just talk through a little bit of the high level install process just so people are familiar. So also listeners check out my Ministry of Nodes Cofounder Ketan, he’s written up or rather done a video, which is like a walkthrough. Adam, I think you saw that video.

Waxwing (Adam Gibson):

It’s a good video. I like that. Yeah.

Stephan Livera:

Yeah. So let me just talk through some of the steps. Just high level, just so you are familiar with what’s going on here. So you know, you set up the folder, you git clone, you CD, you change into that directory and then you are you, I think you run install.sh and it’s basically running the install script. And then you want to select QT. If you want the GUI environment, a graphical user interface for anyone who doesn’t know, then you run jmvenv like running a environment, then a Python JoinMarket QT.py Right? And that’s it’s like another script, right? And I think in there, you’ve also got to go in and comment. If you want to do tour, as you said, a hidden service. You’ve got to comment out the clean end part.

Waxwing (Adam Gibson):

This, this summary is, I mean it’s not perfect, but you’re getting the right basic steps. But the thing is both the guy you mentioned also myself, if you look on the, read me of when you actually go into JoinMarket-client server the, the main repository which you’ll find if you Google it. Like almost like one of the very first lines, it says there’s a video of me doing this step by step.

Stephan Livera:

Okay. Got it.

Waxwing (Adam Gibson):

Which is also the, what’s this Ketan this guy also did the same thing, but I guess his is a bit more like discursive and he’s like obviously set up. I was talking at a conference so you can see what I’m doing. I hope, I hope the way I did it was clear, but you’ve got like two different video like walkthroughs, so you can I guess one of one or both of those. Plus the instructions in the read me should be enough for most, well, your summary is basically right? Yeah.

Stephan Livera:

Yeah. And so then once you’ve set up your wallet, you can either put the pass phrase on or not, that’s up to you and then you’ll be presented with these mix depths.

Waxwing (Adam Gibson):

Right.

Stephan Livera:

What are these mix depths?

Waxwing (Adam Gibson):

There’s a good, it’s a good question. I think it’s caused a little bit of problems using that term, but it’s kind of stuck, you know? So basically if people know about hierarchical deterministic wallets or BIP32 or HD wallets there’s kind of, what is, I guess there’s more than one aspect to those. Those wallets, is the main point of them of course, is that you can recover just from a seed. So you don’t have to like store lots and lots of separate private keys. You just all one secret key and that regenerates all the addresses. But the other part of it is, the reason it’s called hierarchical is that it has this kind of tree structure and it’s defined even in BIP 32, although it expands it more in BIP44 and stuff. This idea that you can explicitly set up what are called accounts within BIP32. So an account is basically two separate sets of, I’m trying to think of the

Waxwing (Adam Gibson):

Right way to say this that isn’t too technical and confusing to people, but two sets of addresses. One set of addresses are receiving addresses and one set, the other set of kind of change or internal. So sometimes you’ll see it called external and internal addresses and sometimes you’ll see it called like receiving and change or something like that. But the general idea is that one of those sets of addresses is suitable for people making deposits and giving you money. And the other one isn’t. We can go into technically why it’s set up like that, but so that’s called an account, a pair of sets of addresses. And you can have in BIP32, any number of accounts. You know, the tree path involves some, at least according to BIP44 has these settings for, you know, coin type and what have you and testnet and god knows what.

Waxwing (Adam Gibson):

But the fundamental point is these accounts now, most HD wallets tend to just focus on using one account because it’s simpler for the user, right? To just have one account. There’s just less management i,ts less clutter. Electrum for example, used to have the ability to choose to add extra accounts to your wallet, but they actually ditched that. Probably again for a UI reason, they don’t think it’s confusing to a user. So they just tell them if you want another one, just make another wallet.

Stephan Livera:

Yup.

Waxwing (Adam Gibson):

Which is very good practice by the way too. If you’re using Electrum, please do use multiple wallets and try to segregate. And obviously you can’t go to the nth degree, every coin, but you know, you have different wallets for different purposes. All right. So in JoinMarket we do actually use the account feature because why we do that is because a very fundamental aspect, of how JoinMarket is trying to work is it’s not really intended as a single coinjoin function.

Waxwing (Adam Gibson):

It’s intended as a multiple coinjoin function. And the, the idea is that by having multiple separate accounts, we can do coinjoins, which are self transfers. So we send coins from ourselves back to ourselves in a coinjoin. But the trick of it is that the output, the equal size output, or the coinjoin output, the one that has the obfuscation property is sent to a different account.

Stephan Livera:

Right.

Stephan Livera:

So forces that that output does not then get spent with any of the inputs.

Stephan Livera:

Got it. Pre and post mix segregation. That’s what it is.

Waxwing (Adam Gibson):

Well, yeah, I mean we were here before all this, this terminology came up, but yeah. Okay. You can call it that.

Stephan Livera:

I’m just simplifying. I’m just using.

Waxwing (Adam Gibson):

You’re using things that people have heard before. Yeah. So, think of it like that.

Waxwing (Adam Gibson):

And, I wish we could educate people better because often when they start using JoinMarket, if they ever get to the IRC channel, which is where we actually hang out, then we can explain this stuff to them. But there’s some minor explanation in various parts of our docs. But we need better explanation for people so they get this or that. That’s what I want people to remember is the core concept is that, yeah, of course you don’t want to co spend stuff that’s gone through mixing process with the stuff that come that’s from the original place. Right. So you don’t want to go spend the change for example with, you know, so yeah. Cause if you think of it like that, you’ve got a bunch of inputs, you’ve got a bunch of equal size outputs and a bunch of changes and the equal size outputs are, have got some new privacy added to them.

Waxwing (Adam Gibson):

But the change haven’t. The change is still completely connected to what, what went before. So if you don’t want to go spend that change with the equal sized output because then you’ve lost the entire effect.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

So all we do is we enforce it, but every time you do a coinjoin, of course you can do a coinjoin to an external party if you want to send someone money. But if you do a coinjoin back to yourself, it goes into a new account. Now we’re not going to deal with an infinite number of accounts, so we just stick with five. And it means that if you go through five, you’ll, you’ll end up the fifth might go back to zero. But that’s already a huge level of obfuscation anyway. So what we have is something called the tumbler where you actually, we give you a schedule of actual whole sequence of coinjoins.

Waxwing (Adam Gibson):

You can do moving coins from one account to the other and also enabling you to then move funds out to some external place. It could be another wallet or it could be, I don’t know, an exchange or whatever it happens to be. But we try to create both timing and amount, decorrelation, both timing and amount, decorrelation effects by using the schedule of coinjoins instead of just like one or two.

Stephan Livera:

Gotcha. And so you can set up a schedule and it will then run through a number of joins before hitting your destination. So.

Waxwing (Adam Gibson):

In multiple steps crucially. Like don’t want the whole amount to all go out at once because then the input is amount correlated to the output,

Stephan Livera:

Right? It’s tied back. Right. And so you could, so for example, could you say, you know, 0.4 Bitcoin and you want it to spend 0.1 to somebody else and then 0.3 back to yourself.

Waxwing (Adam Gibson):

So what you would do there is you would have, most likely what would happen there is you’d have your target address for the 0.1, and then you would create or not create, but you would find, let’s say you have some other wallet maybe be a cold storage wallet. You would take two or three addresses from that. Not, not just one. Cause we tend to want at least as many destination addresses. If I get this right, about as many destination addresses as we have accounts that we’re tumbling through, it’s getting a bit technical now. But basically, you need multiple addresses. So if you’re just sending it to your cold wallet, let’s say your cold storage just take three or four of them or whatever, and then, you know.

Stephan Livera:

Gotcha. Okay. And now there’s also a yield generator. And this is a probably a good one to talk about. If you are willing to leave a machine on at home, obviously be wary. It’s a hot wallet, but you can generate some yield. Do you wanna just tell us a little bit about that?

Waxwing (Adam Gibson):

Yeah. So the idea is that’s the maker side. So we, our terminology is a bit mixed up sometimes, but the maker side of JoinMarket would involve as you correctly point out, running our hot wallet over some long period. I mean there’s no point running it for 10 minutes. Okay. You’re generally not going to get coinjoins, you know more than once every hour or something even when it’s busy. So usually a couple in a day is normal. So we’re talking about long periods anyway. And yeah, so by doing that you, let’s remember, you don’t get some of the advantages, you don’t get the specific amount advantage, but if you’re running it for a long time that’s probably fine with you.

Waxwing (Adam Gibson):

Okay. You don’t get the perfect privacy advantage in each individual coinjoin where you know that nobody else knows your linkage because actually the taker does know your linkage. But I think in practice this is not very much of a concern. Again, it comes back to that –

Stephan Livera:

Because you continually tumble.

Waxwing (Adam Gibson):

Yeah. Cause because it comes back to that whole thing of like, do you want absolute perfection or are you just, you’re just going to be opportunistic. Like over time your, let’s say you leave it on for a month and let’s say you do a hundred coinjoins or whatever. I mean, are they all the same person? That’s not very likely, right? Yeah.

Stephan Livera:

So it’ll tumble through through and it’ll be different people and, yeah.

Waxwing (Adam Gibson):

yeah, that’s what happens over time in that model is that every time you do such a transaction, you’re going to receive a fee according to a kind of algorithm that you’ve chosen.

Waxwing (Adam Gibson):

We offer basically you can do a relative or an absolute fee. So it can be an absolute number of satoshis or it can be a percentage of the amount of the coinjoin. But generally speaking, what happened over the years that the JoinMarket was running is that it tended to fall to very low levels. So, you know, if you’re looking for like returns, you come to the wrong place. I mean, I know that in lightning the people sometimes get annoyed. I can’t make, you know, I can only make one satoshi but here it’s, yeah, I mean hundreds of thousands of satoshi’s is normal in their coinjoin. But the only sort of caveat I’d say is that it does strongly depend on the amount that you’re willing to offer cause the people willing to offer much larger amounts, are able to let’s say offer a relative fee on that amount.

Waxwing (Adam Gibson):

And so they’re able to get involved in much larger coinjoins and actually make at least it’s still very small percentage wise, but it’s more money. Whereas if you’re just gonna offer like a tiny amount and you’re just going to get a few sats yeah, I mean it’s fine. It’s nothing wrong with it, but I think it’s fun. You know, when you see it and you say, Oh God,

Stephan Livera:

I made 800 sats today or whatever.

Waxwing (Adam Gibson):

But it has, the point I made earlier is worth noting that it has fallen over time. And my suspicion is that the main reason for that is the market kind of figured out that the maker is getting nearly as much out of this as the taker is.

Stephan Livera:

Right. Because you’re getting a free coinjoin out of it.

Waxwing (Adam Gibson):

Exactly yeah, the only disadvantage of being the maker is that the sort of security, well, there’s several, I’ve already listed several this morning, but the main disadvantage is security risk, I don’t want to put like half my stash on, on a hot wallet running all the time isn’t even like a hot wallet that I turn on now and again, but running all time.

Waxwing (Adam Gibson):

And so, obviously there’s been years of work of trying to make this secure and I don’t think we’ve had any meaningful theft. But bear in mind that the nature of such a system is that if there were a software bug, it could result in an actual effect where you’re not even there at the time. You know, that’s, that’s, that’s the danger of it. Yeah. But I don’t think it’s, I think probably the reason that this kind of software is unlikely to result in that kind of outcome is because there’s something intrinsically simple about coinjoins. They’re very, naturally atomic. It’s like there’s only one part of the code where you have to just make sure that you’re receiving what you put in.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

And you don’t sign it otherwise. That’s kind of, it really is whereas something like, I don’t know, lightning is way more complicated, but obviously the people doing that and doing great work. So, yeah.

Stephan Livera:

So look, I guess, look, JoinMarket I mean, it looks like a great tool. The only, I guess the question I would have is, could it ever become mainstream right now it’s very difficult to use. What’s needed, like if you were to try and make it a bit easy for people to use?

Waxwing (Adam Gibson):

Yeah, it’s a good question. People often, that’s usually the main thing people focus on. I don’t know. There’s, I think there’s two I’ve thought for a long while. There’s two fundamental blockages to a broader adoption of this. One of them is the necessity of using Bitcoin core as, as a running node at the moment. And I think that puts a lot of people off even like starting the process cause they think oh god, I’ve got to get a node running, I don’t know right now. We didn’t originally have that requirement, interestingly enough. You know, we started off with a very kind of in a way kind of crappy thing where we’d be using blocker.IO, which doesn’t even exist anymore, which was just like one of these blockchain explorers with an API. We just like, ping’ed it. But that was terrible for privacy.

Stephan Livera:

For a privacy wallet as well, right?

Waxwing (Adam Gibson):

Yeah. I mean it’s like there’s the problem people have with Electrum servers, you know, is it arguably even worse? Maybe not. I don’t know. It’s a similar problem. So we kind of gravitated towards and we did actually have an Electrum server set up as well, but I was kinda, I liked having that for testing, but I had more than one person say to me, you really shouldn’t have that. Because even if like I’m doing all my privacy things right. If all the other people in the join are using, if all the other people in the join are using something like that, it’s kind of screwing everything up. So I hope we will get a kind of BIP 157 you know, client-side filtering kind of thing set up at some point. But yeah, that’s just something we maybe should start looking into now because, I think it would be nice additional feature.

Stephan Livera:

Right, to make it easier. So just for the listeners who are unaware BIP157 it relates to the compact block filters. If you’re familiar with the lightning labs suite of products that’s called neutrino in their model. And basically it’s like, again, there’s been some debate on this, but essentially people use it in lightning to not have a full node and get some additional privacy so to speak. But I’ll just note it’s controversial.

Waxwing (Adam Gibson):

Compared to the old, method which is called bloom filtering, which is not as good in terms of privacy but has the same kind of effect where you don’t necessarily have to have a full node to, well you don’t have to have a full node to use it. So that was, that’s one thing that stops usage a little bit I think. I think that caused some problems. The other one is, Oh I forgot my other one just now. I was thinking that just the fact that cause let’s say the install process is really easy. I’m not claiming it is. I mean let’s say you’re using Linux or Mac because it’s kind of a bit fiddly on windows. Even so when you get into JoinMarket, you’re faced with this kind of slightly confusing to say the least set of stuff and we’ve just gone through a lot of those bits and pieces like the mix depths like what’s the difference between a single coinjoin and a tumble.

Waxwing (Adam Gibson):

Then there’s the confusion about like, it’s not confusion, but, it’s just a bit obscure. Like the fact that you need to fund the wallet and wait multiple blocks and with multiple addresses in order to actually use the taker side because of this anti sybil feature we were discussing earlier, that that’s the kind of thing an ordinary user is not gonna like think of, they’re just going to, “Oh I’m going to fund the wallet.”

Stephan Livera:

You’ve got to be a motivated user.

Waxwing (Adam Gibson):

And then all the decisions you have to think about like what exactly constitutes good. Cause in a way it comes back to the beginning of the conversation about consumerist mindset, what people want is they want some central party to do all the hard graft for them. And I totally get that. What they don’t want to be just left in this sea of like incredibly complicated ideas.

Waxwing (Adam Gibson):

And yeah, I’ve got lots of buttons I can press, but I don’t know which one I should press.

Stephan Livera:

and the order and timing and –

Waxwing (Adam Gibson):

yeah, and they’ve got to think about a lot of things. But if you come at it a little bit more and I totally get that. And it is of course a big of course can be frustrating that sometimes things don’t work because the nature of our system is that we have a bunch of untrusted entities talking to each other. So we do have entities that either because of a software bug or because their networks flaky because they’re all using Tor or because they’re actually malicious, they don’t complete the protocols. So there’s a lot of stuff in the background of JoinMarket software, which is trying to deal with that. It’s like when something goes wrong it makes a tweak, it tweaks several different parameters and it tries again.

Stephan Livera:

Yep.

Waxwing (Adam Gibson):

Also it takes time. It’s not convenient. Like if I, if I just want to do a coinjoin, I have to, I sometimes do this to make like retail payments. I’ll just use JoinMarket because why not? but I have to sit there and wait like 30 seconds to a minute before. Like everyone’s, because you go into this kind of messaging pit on IRC and you just have to ask everyone if they’re available and then you have to wait for them to actually give you a response. And so the whole thing ends up taking like at least a minute. It’s not like an ordinary, just click a button and the payment goes through.

Stephan Livera:

Yeah,

Waxwing (Adam Gibson):

so there’s lots of little, it’s just fiddly. It’s then it just is.

Stephan Livera:

And here’s the rub though. Here’s the thing. Like if you want Bitcoin to have more privacy, you want more people to use coinjoin tools. Now some people might say like, I mean some of the Samourai guys are like, I wish Bitcoin never becomes mainstream. Right. But theoretically if you want people to have some level of privacy, you want a reasonable number of people using coinjoin and PayJoin and so on. But the anonymity set possible, if we stay only with hardcore people, it’s much smaller, wouldn’t you say?

Waxwing (Adam Gibson):

Yeah, I agree. I mean that’s why I think this fits with the more sort of hardcore people. I think that’s what it ends up being is like people may be coinjoining larger amounts and people who’ve like been around in the space a long time and people who know their way around.

Stephan Livera:

Command line.

Waxwing (Adam Gibson):

Linux servers. You know, it just is. Can you make a version of this or like a different version of this that is much more feasible? I’ve never really come to a firm decision about that question. People are always asking about, that’s why like one of the most commonly like discussed points like how can we make the GUI easy to use. And I always feel like you’re aiming at too superficial of a level cause even if you make it really slick like one click, this one click, it’s intrinsically quite a sophisticated tool. Is my opinion. But this is a very difficult question that people are constantly arguing about. But that’s why I spend time talking about stuff like SNICKER and PayJoin and what have you because –

Stephan Livera:

Do you want to talk about SNICKER?

Waxwing (Adam Gibson):

Yeah, because it presents a nice sort of counterpoint to that point of view, doesn’t it? Because that’s almost like the opposite end of the spectrum. Although although I would argue probably Wasabi is more like the opposite end of the spectrum to SNICKER because with Wasabi, you’ve got everything like tightly coupled and coordinated. And that means that the users are. So what am I trying to say? It’s, so with SNICKER it’s a very much opportunistic peer-to-peer. Anytime anything can happen.

Stephan Livera:

Yeah. So would you mind just giving an overview, like just a high level. Just for the listeners, obviously I’ve done some reading, but just for the listeners, can you just give a high level what is SNICKER?

Waxwing (Adam Gibson):

What is SNICKER? Right. So SNICKER is one of those silly acronyms or backronyms that stands for Simple Noninteractive Coinjoin with Keys for Encryption Reuse, which is obviously a mouthful and it is a backronym. But essentially let’s not worry about that. Essentially this is an outcome of trying to find any model at all for coinjoin, which has the property that the sender and the receiver don’t have to interact with each other. That that was the goal. Now superficially it seems very difficult to achieve that. And indeed calling it noninteractive might be a bit misleading.

Waxwing (Adam Gibson):

I think it’s the correct term, but some people tell me it’s not the correct term and they say you should think of it as asynchronous and not non-interactive. Okay, so what that means is that the sender is gonna. The sender is going to do some stuff then post a message that is encrypted somewhere that could be a hidden service for example, and the receiver is not going to ever talk to the sender in any sense, but he’s only ever going to poll or ping that server or multiple such servers to find encrypted messages which he or she can decrypt and by some magic or other, it is the case that the, if the receiver succeeds in decrypting that message from that server that they’ve pinged ,what they find is a transaction. What they find is a transaction that uses one of their coins as input but also uses somebody else’s coins and that other person has already half signed the transaction.

Waxwing (Adam Gibson):

They’ve signed their part and the outputs are agreeable to the receiver. They can see that they get their coins back and maybe they even get a little sweetener, you know, 100 sats, whatever then the receiver may or may not choose to co-sign that transaction and broadcast onto the network. That’s the kind of functional summary of what it is.

Stephan Livera:

Yeah. Gotcha. And so let’s go a little bit deeper into how how it is that you can first of all find this transaction that’s possible. So, and maybe if you could just clarify between the two versions. I think version one you were talking about was like an address reuse case, but I think in practice you were saying version two is actually more appropriate. Could you outline that?

Waxwing (Adam Gibson):

Okay. Yes. So the first iteration of the idea was, was based on the, the problem that we currently have with Bitcoin.

Waxwing (Adam Gibson):

It’s both a problem and a positive which that the outputs in transactions are script pub keys, which are hashes of puppies and not just plain pub keys. So because they’re hashes of pub keys, then if you’ve got, Stephan have got an output somewhere or UTXO that is to say, I can’t see the pub key until you spend it. So if I want to make a transaction which spends your output, I have a serious problem trying to figure out how to do that. Well it’s not that, it’s I have a problem figuring out how to create an output for you. That’s the problem. Cause usually if you think about the normal Bitcoin transaction workflow or spending workflow is that although the receiver doesn’t have to kind of interact with the sender, they have to in advance declare an address to be sent to.

Waxwing (Adam Gibson):

And the problem with SNICKER as an idea is that I am spontaneously trying to create a transaction with you without you having posted an address anywhere. Or maybe you have, but I don’t know you. So I don’t know where that address would be. I don’t know where your website is or where your business card is. Whatever it is. Right. So I don’t know your output address. So the trick SNICKER uses is something called tweaking keys. So you can take a public key and you can add a random number to it effectively. And the magic of that is that even though I have added a random number, which I know to your public key, it’s still the case that only you know the private key. So even though there’s kind of a shared data, you’ve got the secret data that you had to begin with, your private key and you still keep that.

Waxwing (Adam Gibson):

And so when you add your private key to this random data that I created, you create a new private key, which still fundamentally you own because I don’t know your, you get the idea. So that’s the core idea. But in order for that to work with like legacy addresses I need to know the public key before you’ve spent the output, which I don’t. I only know the hash of the public key. And so that’s why the first version of this was, Oh, let’s just use reuse addresses. Cause if you already used that key before,

Stephan Livera:

I’ve now exposed the public key.

Waxwing (Adam Gibson):

you’ve exposed the public key in the spending transaction, the first spending transaction. So I know the public key and therefore I can also, of course it’s nice because one, that’s not thing. So anyway, so that’s the first version and obviously that’s kinda crappy in the sense that it’s.

Stephan Livera:

it’s relying on bad practice.

Waxwing (Adam Gibson):

it’s relying on bad practice but there is a kind of amusing pattern though that it actually also solves a bad practice because it improves the privacy of somebody who’s using a bad privacy technique, which is a pattern that repeats here.

Waxwing (Adam Gibson):

But so in version two, it was just a natural extension, which was like, well, we don’t need to do that. We can just, because this is opportunistic, I’ve used that word before, right? Because this is opportunistic. I don’t have to make sure that every such proposal I make every such like proposed transaction is actually going to happen. I can make tons of them. Right? I can, for example, even if I’m just using your key, I could make 10 different proposals and you could just take up one of them. And after all, you know, Bitcoin’s blockchain solves the problem with double spending, right? So there’s no issue of like having multiple versions. So consequently we could just speculatively try different keys. So what we would do there in the second version is instead of, so the output is let’s say a hashed pub key.

Waxwing (Adam Gibson):

So we don’t have a key there, but we could try and guess what the input corresponding to the output was. Now usually common ownership heuristic type of thing means that you think that all the inputs are from the same party. So the pattern is repeating here. You think all the inputs are from the same party. So as long as you can guess which one is the change output. If you successfully guess which one is the change output, but let’s say there’s two outputs, then you know that the pub keys, the inputs are owned by the same person as that output. So you can use one of the pub keys in the inputs and tweak that to create a new output address instead of tweaking the key in the output. Sorry that the words here are really confusing.

Stephan Livera:

Let me see if I can, it’s a bit tough, but let me see if I can summarize that. So version one, basically it’s relying on identifying an individual who’s doing address reuse and when they spend they’re revealing the public key for that output or any outputs kind of sitting at that address, if you will, even though Bitcoins live in UTXOs. They don’t live in an address kind of. And then version two as you’re saying is, let’s say I did a payment you know, I went to buy from the Blockstream door or whatever and I did a standard two input two output transaction.

Waxwing (Adam Gibson):

Yeah.

Stephan Livera:

And then I, one of those was the payment output and the other one was a change up or coming back to me.

Waxwing (Adam Gibson):

Correct.

Stephan Livera:

And let’s say because you, you’re opportunistically scanning the chain,

Waxwing (Adam Gibson):

Exactly, I’m scanning the chain.

Stephan Livera:

You’re looking for an opportunity and in that change output you’d be like, Oh Hey Stephan, that when you did that change output.

Waxwing (Adam Gibson):

Yeah, though I wouldn’t be calling you Stephan,

Stephan Livera:

We wouldn’t know each other, right? But we’re just making it easy for the listeners. And so let’s say you would, you would be like, Oh Hey, this guy, his change output, I have a key that can like I have an opportunity to put, to create a transaction and send that in some, you know, blind kind of way to a server, an email or, a server, let’s say. And you are able to spend my, what was my change output to your address and you can in return offer one of your UTXOs to me without me knowing kind of and am I getting that right so far?

Waxwing (Adam Gibson):

Just the last couple of sentences, it seems to be getting a bit confused. So you’ve got the change output and I’ve guessed that that’s the change output. Then I look at the, in your case there were two inputs, right?

Stephan Livera:

Yeah,

Waxwing (Adam Gibson):

and I can choose either one of those inputs cause I’m assuming it’s both you or both the same person and I can look at the public key in that spending, in the witness, you know the public key is there so I can take that public key and use that instead of using the pub key in the change output which I can’t see behind the hash.

Stephan Livera:

Yeah, you’re right. You’re right. It’s from my inputs. Yeah. Gotcha.

Waxwing (Adam Gibson):

Once I’ve got that public key, I can do two things with it. The first thing is I can add a random value and tweak it. To create a new output address for you. As I was explaining just a moment ago that will still belong to you even though I’ve added a random value to it so I can construct a transaction that pays you the appropriate amount and uses that change output as an input. Right? That will be one of the inputs. And the other, the proposed transaction I’m creating consists of spending that change output and spending one of my UTXOs and the outputs of that proposed transaction. One of them is the newly tweaked output for you that I’ve created for you. And the second output or there’ll be three actually, but the other outputs will be for me it would be my outputs. And that’ll be it. That’ll be a coinjoin. That’ll be a SNICKER coinjoin. So I wanted to say something, I’ve forgotten what it was. So the inputs, yeah.

Stephan Livera:

And in terms of like, yeah. And then in terms of your wallet quote unquote knowing it can do this, how would it do that and how would it kind of access this info?

Waxwing (Adam Gibson):

Right. So I just remember what I wanted to say also was the same public key that we’ve just like elaborately tried to figure out is the one that I would use to encrypt this transaction proposal and put it on a some, there’s actually some discussion about whether encryption is either necessary or even a good thing here. But it’s certainly possible to do it this way. And that’s how it’s proposed is I take that public key and I do an encryption so that when it gets put on some bulletin board, nobody can read it and figure out who’s proposing what to who in theory.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

Okay. Then you’re gonna try and decrypt various different blobs and you’re gonna find the ones that actually successfully decrypt. And what you’ll see inside there is that proposal and you’ll be able to co-sign. Obviously I’ve included my half signature on the transaction for you.

Stephan Livera:

Right. And so again, so this is a lot of technical details that right, obviously in practice for the user it’s just going to happen in the background, right? Like your wallet will just in the same way, that.

Waxwing (Adam Gibson):

This point, this point is very important. So we are getting lost in the weeds cause is kind of technical, but although, although I have to say all those very technical, the actual like primitive elements of it are really simple compared to a lot of other things. Now the practicality. So when I first wrote the blog post about this back ages and ages ago I decided that it’d be a really good idea to start the first half of it with like a scenario.

Waxwing (Adam Gibson):

And I call it like Alisa in Moscow and Bob in New York. And what the reason I did that is cause I was trying to really hammer home that, the reason I think this is interesting is because if you’re the receiver, you don’t have to be, I don’t personally don’t think you have to be a techie. And I think your wallet developer who made your, let’s say mobile wallet doesn’t have to do that much work, you know, arguably.

Stephan Livera:

To implement?

Waxwing (Adam Gibson):

Yeah. To implement this kind of protocol. And so the, user experience. So in that blog post, it was Bob in Moscow. He’s like, he’s not technical, right. And he’s not even in the same time zone as Alisa and he just switches on his phone. He doesn’t even have his wallet on all the time?

Waxwing (Adam Gibson):

He just has his, maybe, I mean obviously it can be in the background, but let’s say he just switches his wallet on for half an hour every, every day or whatever. And even that’s enough for this kind of thing to work where he could just toggle a switch that says if anyone makes a proposed SNICKER coinjoin to me. As long as it doesn’t like lose any of my money, as long as I have net positive or zero, I’ll accept it cause there’s no risk in that. Right. so in theory it wouldn’t need to involve any user interaction. That’s what I was hoping for. Okay. Now do you see now our way, I was saying earlier, this is kind of like the opposite end of the spectrum to something like JoinMarket or even Wasabi because in both, in the user experience and it’s just very opportunistic and very like, it’s not interactive. It’s not, you don’t have to sit there, turn something on, wait, and what have you?

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

From the receiver side. But from the sender side, I think it could still be quite a technical thing because it depends how it’s set up. But you might have to like scan the blockchain with some sophisticated tools to find, Oh I forgot to mention it in our version two example. The change output, don’t forget, you don’t even have to be smart enough to know which one is the change output. Cause usually, there’s only two. You could just make two proposals, right? Yeah. One is going to be wrong.

Stephan Livera:

Right. And I think there’s one other benefit that’s worth calling out here, which is that it also helps break the common input heuristic because it is specifically like taking what was meant to be only, you know, my inputs and now it’s like your wallet is able to spend that. So kind of to an outside observer does that kind of,

Waxwing (Adam Gibson):

well I’m just going to want to caveat again cause this is one of those non-steganographic things because at least as designed as written down is it’s like a two party equal sized output, coinjoin. So, I mean just the fact of having two equals sized outputs is kind of giving it away as, I mean arguably we can have different designs. There’s various things we could do. But I think that the basic primitive idea is already interesting on its own. It’s just like, okay, it’s just an ordinary two-party coinjoin. It doesn’t give you, it doesn’t have chain efficiency. Like if there were hundreds of thousands of these that would bloat the chain. Right. On the other hand, what I like, the heterogeneity and also in theory you could do payments with it as well. Although this is kind of like pie in the sky really at the moment.

Stephan Livera:

It’s a bit too far out there.

Waxwing (Adam Gibson):

Yeah. But you, because you could make lots of proposals and you, if you sweeten it with enough sats, then there might be lots of people motivated to actually get your, get your payment to go through any actually a reasonably fast time.

Stephan Livera:

Yeah.

Waxwing (Adam Gibson):

So in theory it could be done as a payment, but I mean, yeah, pie in the sky.

Stephan Livera:

Yeah. Well I guess, I mean look lightning, that’s, that’s one aspect. Have you done a lot of thinking about lightning and privacy there? And you know, I mean there’s different, there’s different concepts around the privacy available for that.

Waxwing (Adam Gibson):

I’m certainly not somebody who’s gone into all that. I know there’s been some significant academic research into the whole area of like lightning the network level privacy.

Waxwing (Adam Gibson):

But after I’ve done that a certain amount of study of some of the most important like core elements of lightning, like the, how the HTLCs work and stuff like that. But, so I’ve thought about it, but I, I’m certainly not the expert in like the various weaknesses and how people are plugging them.

Stephan Livera:

Yeah, sure. And look, I guess the thing is, even after a a bunch of these even after, you know, people using coinjoins and so on, there’s still that that factor of fingerprinting, right? So you still have to think about how to avoid that. Like the n lock time and the RBF signaling and so on.

Waxwing (Adam Gibson):

Yeah.

Stephan Livera:

But I guess these are the steps and you sort of have to start.

Waxwing (Adam Gibson):

Somebody was talking about that the other day. I think it was yesterday. I think it’s a really important point as we develop into more sophisticated contract relationships within, especially within taproot, we’ve got to think about how we address this fingerprinting concern. Cause one level is when you have cooperation in contracts, you just have multisig usually two of two or it could be, I guess it could be n of n as well, but in any case, we’ve kind of addressed all that and hopefully we can get everyone. But like we were saying earlier in this discussion like there is going to be really hard to get all the wallets using not fingerprinting themselves because they have special features. And it’s kind of, I mean, I think there is a certain gravitational force that’s pulling people towards using the same values where they can, but there might be cases where they’re not able to.

Waxwing (Adam Gibson):

Yeah.

Stephan Livera:

All right. Well yeah, I guess if you’ve got any other things around where you, where you see, like what are the hopes for bitcoin privacy going forward?

Waxwing (Adam Gibson):

I mean it’s a very big topic. I recommend people to look at Chris Belcher’s privacy page on the Bitcoin Wiki as a good like, cause it can seem overwhelming this topic, but he’s got a long list of all different things that you can think about and try. And if you just want to improve, you know, you just want to be a bit better. That’s a good place to start. And then go from there. The, there’s lots of other areas of this discussion. I don’t think we touched on like the more the newer and more sophisticated technologies that are being used and things like Monero and Zcash, and various less reputable coins, you know, zero knowledge proofs and ring signatures.

Waxwing (Adam Gibson):

But I think especially zero knowledge proofs is something we should look out for. And you know, and of course, just basic things like well not basic, but like confidential transactions. So, there’s lots of like more soup top ways that we could, in theory, we could just like add them just like add an ingredient into the pot, into Bitcoin. Oh, all these problems just disappear. But unfortunately it’s not quite like that. There are some significant trade offs. And the obvious one being to do with like the soundness of the money supply aspect. Which really are kind of a fly in the ointment, but they’re also kind of sometimes other technical trade offs. Things like scalability issues with these things, you know.

Stephan Livera:

Yeah. I guess the most probably the most realistic one I can think of is really the whole cross input signature aggregation one, right? Because at least we can like I mean you were talking, we were talking about it before, but I think maybe that’s the one that looks sort of realistic that we’ll get it, but it will take some time.

Waxwing (Adam Gibson):

Well that and off chain, right. Lightning is already practical. It just, it’s just a bit limited in size and scope, but it’s already practical and, but you’re right that if we are able to move to a better use of the intrinsic linearity of the Schnorr signature, and not just with the signature aggregation, but I think people tend to forget the value of the the scriptless script construct, which means that you can kind of, it kind of means you can embed kind of how to put it. Say you can swap coins for secrets in ways that are completely impossible for, it’s not just that people can’t see that you’re doing it, but it’s got deniability, which literally means that I could tell you that this signature that I made actually was hiding this secret.

Waxwing (Adam Gibson):

And the evidence I could provide for that would be exactly the same as the actual real person who really did use that secret. You know, the real, you see what I mean. So it’s like information theoretically perfect. That you can’t but anyway, my point is that the linearity, of the Schnorr signature, both sort of additive and subtractive means that you can get these very strong effects. And we see the same thing happening in lightning where they have the multi hop lock.

Stephan Livera:

The point time looking idea.

Waxwing (Adam Gibson):

Point time lock contract instead of hash time lock contract. It is very powerful in the same way. It’s the same mathematics if you write it out, that’s why it’s all coming from the same thing, which means that you can kind of, yeah. So the addition of Schnorr, this is why the addition of Schnorr was kind of, there was a lot of enthusiasm for it that and the kind of slightly better security properties. But yeah.

Stephan Livera:

Great. Well look, I think we’ve, we’ve actually gone over two hours now, so yeah. But look, I’m a big fan of your work. Thanks very much for joining me. And obviously Adam, where can the listeners find you and where can they find JoinMarket?

Waxwing (Adam Gibson):

So me, myself I’m on Mastodon Waxwing@x0f.org. That’s Vladimir van der Laan’s server and on github. I’m AdamISZ or ISZ if you’re American. And what’s the third one I’ve forgotten?

Stephan Livera:

Oh just JoinMarket. So there’s JoinMarket.me, is it?

Waxwing (Adam Gibson):

Oh, joinmarket.me/blog is my blog and JoinMarket.me hosts, as you mentioned earlier, a JoinMarket order book like table, but don’t rely on it. It’s not perfectly accurate. So you should set it up yourself. You can do it locally. You can do the same page locally. JoinMarket itself you should go to I mean, https://github.com/JoinMarket-Org/joinmarket-clientserver/. Maybe not the simplest page name.

Stephan Livera:

Yeah, that’ll all be in the show notes. I just think it’s good to just have it called out. Thanks again for joining me.

Waxwing (Adam Gibson):

Not at all. It was great. Thank you.

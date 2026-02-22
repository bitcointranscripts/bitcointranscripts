---
title: 'Scaling Lightning Panel - Lightning++ Berlin 2025'
speakers: null
source_file: https://www.youtube.com/watch?v=oFDaC_2WjP0
media: https://www.youtube.com/watch?v=oFDaC_2WjP0
date: '2026-01-21'
summary: 'Sign up for one of our upcoming dev conf at https://btcpp.dev


    Website: https://btcpp.dev/

    X: https://x.com/btcplusplus

    NOSTR: https://iris.to/npub1dwah6u025f2yy9dgwlsndntlfy85vf0t2eze5rdg2mxg99k4mucqxz7c52


    #btcplusplus #devconf #bitcoineducation #bitcoinconf #bitcoindev #bitcoinconference
    #bitcoin #cypherpunks'
tags:
    - btcplusplus
    - devconf
    - bitcoineducation
    - bitcoinconf
    - bitcoindev
    - bitcoinconference
    - bitcoin
    - cypherpunks
    - niftynei
categories:
    - Entertainment
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:01

But it wouldn't be a lightning panel without a Greek god himself, Evan Kaloudis, welcome back.
So I got told that panels have a fixed size, but my understanding is that lightning panels have a special technology called splicing.
And so we can increase the size of a panel beyond what is already preset.
And so I'm going to splice two panelists into the panel right now.
We have Rita joining us.
And of course, the creator of splicing, Dusty.
Now, actually, Dusty has to go.
And of course, I don't want you guys to feel shortchanged, and so I arranged a special swap.
Of course, that swap is powered by no one else other than Michael from Bolts, so I'm swapping Dusty out, and Michael from Bolts is coming in.
Thank you, Dusty, for your help with the splicing.
Thank you.
My most esteemed panel.
OK, let's construct it.
So the base layer, we have Evan Kaloudis.
Please come take a seat.

Speaker 1: 00:01:18

We have.
No, don't listen to this guy.

Speaker 0: 00:01:22

We have we have Rita.
He's like, see.
And then and then Michael, of course, is going to help me get these.
No, no.
Michael's going to help me get these gentlemen between layers here as he so often helps Bitcoiners move between layers.
So Michael if you can just hold this structure with me and the three gentlemen are going to climb up the back one at a time please gentlemen.

Speaker 2: 00:01:50

There isn't.

Speaker 0: 00:01:51

Shinobi doesn't weigh very much, don't worry.
Bitcoin doesn't care.
Just pay for Bitcoin on top, it's okay.

Speaker 2: 00:01:58

It's the metric system, it doesn't count.

Speaker 3: 00:02:03

We are very serious people.

Speaker 1: 00:02:07

By the way, Shinobi looks like in the memes.
I didn't know.
What's up?
Hi.

Speaker 0: 00:02:17

Michael, you can come take a seat now.
Thank you.

Speaker 1: 00:02:18

Do you have a microphone or are you going to shout?

Speaker 0: 00:02:24

Okay.
So my, my first question, to my, to my esteemed panel is it's never been easier to run a lightning node.
It's essentially plug and play, so why don't more people run their own lightning nodes?

Speaker 3: 00:02:48

Well, it's a huge pain in the butt.
You have to keep it reliably online.
You have to handle all the liquidity management yourself.
So make sure you have enough receiving capacity to receive that your sending capacity is allocated intelligently so that your payments will actually succeed.
And it's also just a lot of other issues that really have nothing to do with Lightning itself.
For instance, my place at home, I have a very unreliable router that loves to just randomly drop devices off the network.
So even though the Lightning side of the infrastructure works perfectly, My node is constantly conveniently offline when I'm traveling around the world and want to make a lightning payment.
It's just a lot of things you've got to get hands on with.

Speaker 0: 00:03:42

That's a skill issue, Shinobi.
Is that right?
Yes.
Is that what you're saying, Kali?

Speaker 3: 00:03:46

That's what I have to say to that one.

Speaker 1: 00:03:48

Oh, Shinobi.
Here we are.

Speaker 0: 00:03:50

Shinobi filtering his words there kindly for you.
Callie, your thoughts?

Speaker 1: 00:03:57

So I think one of the biggest issues is that you can actually lose money.
So lots of people who run Lightning Nodes know that many people who run Lightning Nodes are net negative, basically, with the routing fees that you collect for a year or two, and then you get force closed during a high fee period.
And you can easily lose $50 or $100.
So that's one problem why I know that some people just stop running their own Lightning Node because it's not worth the hassle for them.
But there is the whole you know the centralized way of using Lightning with a centralized LSP maybe, or something like Phoenix, that really works really, really well.
So I have no complaints there.
I've been using Phoenix for many years, and it's been the same lightning node since the beginning and it works just really, really well.
I think it basically depends on how you want to use lightning and if you're going to go the L and D I'm a routing note way and hope that you can make some extra buck, I think that's super challenging to actually pull off.
Other than that, I think just the fact that most people don't want to run a server, we just need to recognize that fact.
It's not going to change very fast and I think home nodes don't really affect that a lot because lightning nodes like to be like well connected and on in the cloud in the best case or on a VPS or something Although home nodes really do work if you have a stable internet connection.
And lastly, I think there is a just, you know, the ugly truth about Bitcoin is that there is around 40, 000 people or so that use Lightning.
That number isn't growing that much so why don't we have like 400, 000 people using Lightning?
Should be, you know, the meta question around it.
The number of Bitcoiners is just growing very slowly.
The number of people who use Bitcoin for payments instead of just, you know, ETFs and stacking and whatever.
So I think that's also, that's probably the strongest factor explaining why not many more people use Lightning.

Speaker 0: 00:06:20

Alex?

Speaker 2: 00:06:21

I mean the question was why don't people want to run Lightning nodes?

Speaker 0: 00:06:25

Yeah, why don't people run their own Lightning nodes if it's never been easier?

Speaker 2: 00:06:29

Well Why would somebody want to run a lightning node first?
Are you talking about as like, why aren't there more hobbyists trying to become routers?
Or why aren't there more people spinning up new lightning nodes just to receive money?

Speaker 0: 00:06:43

Both.

Speaker 2: 00:06:44

So for the why aren't there more hobbyists trying to spin up routing nodes is because, I mean, it's high effort and you're probably going to lose money.
It's still high effort.
It's easy to spin up a new node, but if you're going to run a routing node as a hobbyist, you really have to be checking your channels every day.
It's hard.
And by default, you will lose money because there's people trying to siphon you, siphon your liquidity and you can make money off of people that don't know what they're doing running Lightning nodes.
So that's maybe one reason why you wouldn't want to run one as a hobbyist Lightning router.
For the end user it's really easy to spin up a lightning wallet, but to receive money, the incumbent system that people are used to for receiving money is effortless.
Zero effort.
And in my opinion, in order to really compete for people in swaths that don't care about money that much, we have to compete on that UX.
We have to be effortless.
We can't just be easy.
So.

Speaker 0: 00:07:38

Someone helping with the UX and many more things.
Evan.
These guys sound kind of bearish on lightning, huh?

Speaker 4: 00:07:47

Fucking doomers.

Speaker 1: 00:07:49

Yo. Realists.
The question was negative.

Speaker 4: 00:07:52

Yeah.
Come on.
Is it a better payment experience going to the app store and hitting start wallet or is it a better payment experience going to the bank and bringing all your identification and proving your income or whatever the hell.
I mean, listen, we have a lot of work to do, but there are definitely advantages in our UX that we need to highlight and lean into.
The fact that you can spin up a wallet with a few clicks, put a lightning address in your profile and start receiving funds from people all over the world without KYC, That's amazing.
We've got to lean into that.
The reality though is that our ecosystem is super, super tiny right now.
And the resources that the average person has is obfuscated by all the noise out there.
The advertising from the exchanges, which are really shitcoin casinos, I want to point you towards the latest shitcoin so that they can make fees off the transactions, the trading volume.
The news being inundated with stuff like the ETFs or the latest treasury company.
And lastly, just not enough places to spend it.
Like how many places in Berlin can we find to spend Bitcoin at?
You know, 10, maybe 20 tops.
You know, you probably can't live off it here unless you like going to the same, you know, handful of restaurants every day and we need to make, you know, efforts to improving that.

Speaker 0: 00:09:35

Is the reason why more people aren't running their own node because your company is so good, Michael?
Is it just because I have this recurring theme that every time something's working in Bitcoin and Lightning, you pull off the mask, as in by asking more and more questions, and underneath it's just Michael from Boltz every single time.
Is this why no one's built, no one's actually running their own Lightning Node, because you don't need to anymore, you just use Michael.
Is that it?

Speaker 5: 00:10:01

That's All my database.
That's the answer for it.
No, but seriously, why are you, we're asking that why aren't people running more lighting notes when it has never been easier?
It's because the alternatives that you don't have to run one have never been better with like cash you fed him in liquid swaps, spark arcs.
There are so many more things that connect you to Lightning for which you don't have to run your own node.
And even if you were to run node, like for example with Zeus Embedded, Those don't show up in the public metrics because they are like private and don't announce themselves to everyone And why would you because as everybody is saying running a lot lighting routing node that's publicly announcing itself of hey I'm here just fucking sucks in every single way Like you either lose money if you are forced closers, or until your SSD dies and then all your money is gone.
Unless you pray you have the static channel backup stored somewhere.
And that's just a horrendous experience for everyone.

Speaker 0: 00:10:58

As a user, Rita, Who do you most agree with here and why?

Speaker 6: 00:11:07

Is it working?
Yeah, okay, well, everyone has its fair point.
I agree that the UX part needs to be improved a lot more.
And one of the tools that I actually love using the most was Phoenix, mainly because lightning there is kind of under the hood.
You don't really have to understand what you are doing and what is going on.
It is just there, it's super fast, it's super simple and you don't have to understand like what are the channels, how do you close it in the right way, how do you open it in the right way, what are all of those dozens operations that you need to do.
So like the UX simplicity that it is just working by itself magically under the hood is really the key to people using Lightning more.

Speaker 0: 00:11:54

Phoenix is one of my favorite apps but it has some friction especially when you're teaching new users about lightning.
If you want to tip a waiter or something and you tip them on Phoenix, they're going to take a decent cut of the fees to open a channel, right?
To give you some inbound liquidity.

Speaker 6: 00:12:14

So there should be like UI tips or something like that for people like, Hey, this is this.
If you want fast use this, if you want to on chain, explain in few words, what's that?

Speaker 5: 00:12:23

And we had that exact problem with our local bar, the Bitcoin meetup, where we just had the way to install Phoenix and then Everybody paid their beers with lightning to them and every single one of those payments was an on-chain splice in and those costs do add up.

Speaker 1: 00:12:39

What?
Because the channel wasn't ready yet?

Speaker 5: 00:12:42

I have no idea why, but that was the situation we ended up with.
Is that better than UX?

Speaker 6: 00:12:46

The launching fees were super high at that moment and that's why it was...

Speaker 5: 00:12:49

Not super crazy high but like if you do 10 of those splice-ins over the evening, it adds up.

Speaker 1: 00:12:54

I want to say something controversial.
Sure.
I think it's a really bad idea to onboard someone onto Bitcoin with a non-custodial Lightning wallet.
Yes.
Like, I'm a, you know, I've been using these tools myself for a very long time, don't get me wrong, but just this, you're going to lose money with your first transaction, it's going to be super fast in the second transaction, but the first one really takes like an hour or so and this whole you know if you lose it then everything is gone and you know where do I export it how do I restore it all this is so much information for someone who just wants like five dollars worth of Bitcoin for example so this is why well it was a Toshi became so popular for so long because it didn't have that the fee for you tipping your waiter or they weren't there wasn't a cup being taken seemingly.

Speaker 0: 00:13:43

Yeah, that's not proper lining.

Speaker 1: 00:13:45

It's username and password which is also something you know it I'm the first guy who criticizes these login methods all day long, but this is something that you don't need to explain to anyone.
Everyone knows how username and password works or email and password.
And People don't even care about their password, because they know that they're going to be able to restore it when they lose it.
So it's like they put in a random password, not even saving it somewhere, because they know that there is this emergency button.
And with all these options that we've talked about, you don't have that.
You need to be like super sharp from the first second on and not make any mistakes basically and then you're good.
But for onboarding I think this is just, you want to receive money, that's all you want to know, all you want to do.
You don't want to learn anything, you don't want to get a PhD in fucking Bitcoin to receive your first payment.

Speaker 0: 00:14:36

But if you do want to get a PhD in Bitcoin, please keep coming to Bitcoin++ events.
It's the best way to further your Bitcoin technical education.
Thank you.

Speaker 6: 00:14:43

Yeah, removing the fear factor really matters because a lot of people are really scared to lose their funds if they do something wrong.

Speaker 5: 00:14:50

Rightfully so.

Speaker 3: 00:14:51

I think it just comes back to like what Alex said, like people just expect like I received the money, that's it.
Like somebody who's confronted with what is receiving liquidity, what do you mean on chain versus off chain, like This channel has to be set up first.
It's just so departed from their expected experience.
That is the worst way to try and onboard somebody.
Kale is entirely right.
That is the fastest way in the universe to create an impression in someone's mind that Bitcoin is a convoluted, overly complex thing that is completely counterintuitive to all their expectations.
And you are going to make it harder to get that person to adopt Bitcoin in any way in the future or anybody that they talk to and share that experience with.
It's just the absolute wrong way to start somebody off.

Speaker 5: 00:15:43

What's the right way then?
What's the right way?

Speaker 3: 00:15:46

I want to answer...
You graduated wallets like Evan is building.

Speaker 1: 00:15:49

I want to answer that question by a question to Evan actually, something that I didn't ask after your talk, if you'll allow me.
Sure.
Which is, do you think...
You know this concept of annealing or annealing, which is like cooling a magnet down slowly, and if you do it slowly, it gets like, it's more stable, versus if you do it fast, then it's unstable.
So I wonder if you think that you onboarding someone through a graduated experience, basically with zero information first, you receive money and you're done, and then slowly you increase the pressure Basically saying like now you have 15 20 30.
You should now learn about this like click this button.
Did you read this?
Yes Okay, then you can receive more So going step by step by forcing the user to not understand anything in the beginning and then forcing them to understand slowly more and more, do you think that creates like a more stable Bitcoiner?

Speaker 4: 00:16:43

God, you're a nerd.
100% and listen, you know, on the other side of the spectrum, the financial elites that are trying to take all the rights away and enrich themselves as much as possible use that very tactic.
Gradualism, right?
Like the analogy everyone brings up is boiling frogs in a pot.
If you turn up the temperature very slowly, eventually it's just going to get to a point where they just stay in there and they get cooked.
But if you turn up the temperature right away, it gets really hot, Suddenly they get the fuck out of that pot.
So in the same regard, we need to think of how we turn on the pressure, the heat, very, very gradually as to not have our frogs jump out of the pot.

Speaker 3: 00:17:29

Yeah, I kind of want to come out of here left field and go back to something, like an offhand remark you made a minute ago, Walton, that's not using Lightning properly.
I want to ask the question, what the hell do you mean Lightning in the first place?
If you really look at what it is as a protocol, like the way a channel is structured and the pre-signed transactions that make it up, or the gossip protocol that's used to inform everybody the channels available on the network they can route through, or a million other individual components like HTLCs being used to route payments across multiple channels.
All of these are things that can be individually like taken and replaced and done differently.
So like if you slowly piecemeal change these individual things until everything is different, it's the ship of Theseus.
Is that still lightning?
And I think this fixation on, like, the shape of lightning and how it works now and how it's implemented now or how you should use it now is a complete red herring question because at the end of the day every single component of the protocol can be replaced piecemeal and done in a different way and we should we should appreciate that and actually be doing that in a way that learns from the friction points users encounter that deal with the the problems that actually discourage users from using it.

Speaker 0: 00:18:57

When I use that when I said not real use of lightning I mean the I think it's a common misconception amongst a lot of Bitcoin is probably not those in this room but the you know the lightning network growth is driven by by people zapping each other on NOS when actually those payments are often between the same custodian That's what I mean by not real Lightning payments.
Ones that aren't actually on the Lightning network, right?
They're on a layer above, if you will.

Speaker 3: 00:19:26

I would beg the question, would that also apply to your mind to users of Spark or an ARC implementation?
Those things are trivial to make compatible and interoperable with Lightning, but are those now a part of Lightning or are they their own independent thing?

Speaker 0: 00:19:43

Is ARC custodial or is it self-custodial?

Speaker 3: 00:19:47

ARC is a clear no to that, but Spark, that's an ambiguous grey area.

Speaker 0: 00:19:53

State chains have trade-offs?

Speaker 3: 00:19:56

So like, I think we should stop fixating.

Speaker 0: 00:20:00

on these purity tests and whether something is or is not lightning.
Does it work for a user?
Does it provide value and utility to a user that they were missing in their life otherwise?
And does it compose with all the other aspects of this?

Speaker 2: 00:20:15

Maybe another way of saying this is like, why are we, or is lightning the end?
Like what are we trying to do here?
Lightning is a tool, just like Bitcoin is a tool.
But like what is the end that we're going for?
Like I'd say it's something that approximates like saving people from weak money.
So how can we get people to use strong money faster and not get hurt?
And lightning is a phenomenal tool in that direction.
But yeah, the lightning itself, it's not the end.
It's just a means to get to something more impactful.

Speaker 3: 00:20:47

Completely agree that lightning is not the end goal here.
It's the means to an end and it's the best tool we have at our disposal right now.
But if in 10 years time we have something nicer or replace all of the parts with the next generation, that'd be fine too.

Speaker 4: 00:21:02

Every tool exists of many components and if you upgrade each one of those components it doesn't mean that it's a different tool.
Like, if HTLCs are going to be upgraded to PTLCs, like, it's not going to be not Lightning anymore.
It's just going to be like points instead of hash time-log.

Speaker 1: 00:21:22

Mm-hmm.
To me, one of the reasons I love Lightning is because unlike on chain, if you run a Lightning node, you get paid for spam, right?
You know, I get the people send me those one sat messages and I'm like, oh, thanks for that, thanks for that.
It's not dust because, you know, sats don't really exist.

Speaker 2: 00:21:43

Channel jamming is a problem, Let's be real.

Speaker 1: 00:21:47

You just don't see it.
But jokes aside, routing nodes are able to earn real yield in Bitcoin terms, in self-custodied Bitcoin, and yet this yield increasingly comes from institutions deploying their capital with lightning custodians.

Speaker 0: 00:22:07

I'm actually very skeptical in the long term that that can be a material source of income.
I think like you see a very, very fat-tailed curve where the largest nodes with the best connection in the network and a lot of capital deployed can actually see a decent return on things, but that drops off very rapidly the minute you start going out into more sparse, disconnected parts of the network.
And that is just going to be a hyper-competitive thing.
Those yields, I think in the long term, will be driven down to absolutely nothing.
Because these large players will look at this as, oh, I can just park my money here.
Some specialist like LightSpark who knows what they're doing, can deploy it on the network and earn some income, and it's going to be a race to the bottom very quickly.
And ultimately I think just become kind of the lowest risk benchmark yield.
Like that will be what people will settle for if they are very risk intolerant.
Like they do not want to take any risk with their money to earn a return on it.
This will be the place they can park it and know that that risk is very minimal, but that yield will also be very low.
So I think that's not a viable revenue strategy in the long term, trying to earn money off of Lightning.
I think services like what Michael does with bolts and more direct monetized tooling like that, that is going to be where any substantial yield comes from in the network in the long term, I think.

Speaker 3: 00:23:48

Yeah, and like also Lightning is not risk-free to run a routing node especially.
It might be considered low risk compared to like custodial lending platforms and yield things, but there's still quite a bit of risk to it because it's a goddamn hot wallet in the cloud somewhere and there's also implementation risk of like your lighting, not implementation, just having a bug.
And there is responsible disclosures of grave bugs all the time.
Like there is actual risk there to have all your stash in a hot wallet, in a cloud, in a hugely complex application with bunch of state with a database you can't properly back up beforehand and not really live.
There is risk there.
Bunch of risk.
So it's not risk-free at all.

Speaker 2: 00:24:34

Shout out Lightning Fuzz.

Speaker 3: 00:24:35

Risk-free.
Compared to BlockFi maybe, but not in general.

Speaker 4: 00:24:39

Nothing is risk-free.

Speaker 3: 00:24:41

Yeah, there is no such thing as risk-free interest in Bitcoin.
There's always risk.
Lightning routing might be on the lower end, but there is still like non-substantial, but like not negligible risk.
I wouldn't put my whole cold stack into a Lightning routing node.

Speaker 5: 00:24:54

100% agree.
I don't think that running a Lightning node is risk-free at all.
It's just the fact that you can lose your database and you're wrecked is basically just, it's a no-go.
You can't just back up a seed phrase and be okay.

Speaker 0: 00:25:05

We added scare quotes.
All right, the scare quotes have been appended.

Speaker 2: 00:25:11

Yeah.
Also, there's no money in routing, no offense.
Like, if you're gonna run a routing node, like, It's already virtually free to route payments on Lightning, which is phenomenal for users.
We can send payments anywhere in the world for free, basically.
The only way to make money in routing is if your inbound's free.

Speaker 3: 00:25:27

Yeah, which is the case for the crazy yield numbers that have been circling around.
They make those numbers because their inbound is free.
And there might be a couple players out there generating decent yield, but it's like they have a very special positioning and it's a not fiercely competitive market right now.
There are only a few people know where exactly to put themselves in that work to make it work.
But once those spots are known, it's like a fierce competition and driven to zero.

Speaker 1: 00:25:55

So do these inbound, outbound liquidity requirements naturally drive centralization of the Lightning network over time?
And will this institutional deployment of capital like hyper-catalyze that process?

Speaker 0: 00:26:14

I think There's just always going to be a natural drive towards centralization with something like Lightning.
I mean, it really, from a topological point of view, mirrors the internet in a lot of ways.
And I don't think that means it's just going to forever get more and more centralized until there's one big super node.
But there will always be those players who are a lot more central in the network topology than others, just like the internet.
There might be thousands of different ASNs across the world, but you still have very dominant systems like Amazon, like Comcast, like other higher tiered networks that are like the bulk of the connectivity and where things route through.
But the internet is still not a place, despite that, where you can just flip it off right away.
Or one of those players can prevent other pathways or channels of communication through it.
It's just efficiency.
And looking at the internet as an example, we've kind of settled in a place where we've leaned into that centralization a good degree to get the benefits of that efficiency, but not so much that the robustness and the redundancy that keeps the internet a free and open place have disappeared.
So it's that balancing act.

Speaker 2: 00:27:38

Even email?

Speaker 0: 00:27:40

Yeah.
Email might be an example.
We just lost that one.

Speaker 5: 00:27:43

My bad.
I actually think Lightning is almost a bit better than the Internet.
I would agree that there are centralization forces going on because just of the efficiency gains of having a well-capitalized node, you know, it's economics driving centralization, and I think that was expected.
However, the fact that anyone can join the Lightning Network as on the same playing field as all the other nodes is something special.
That is not the case on the Internet at all.
You cannot just be your own AS or start, you know, propagating DNS or whatever.
All these special roles that the internet has developed over the decades that are not accessible for any one person.
Also, you cannot just, I mean, you can always host your own server, but first of all, you need an IP address that someone gives you.
And you also need an ISP to even talk to the internet, right?
So the internet seems like much more, like there are many more, gates to become an internet player.
Whereas in Lightning, I think even if we have centralization forces, the fact that you can just spin up a node and you don't need to register with anyone, that you don't need to talk to anyone, you don't need to call anyone.
You are a node and you connect to someone and they typically accept your channel, which is something that we should be aware of how much that is actually worth.
Even if it makes a routing bit more inefficient and we've seen in, in René's talk previously, you know, the edge nodes have a harder time in being good payment routers.
But the fact that we still allow that, and we should keep allowing that as long as we go, and we should work on more privacy features so that the difference between a big node with a well capitalized company behind and a pleb node which is an individual's person node at home maybe so that the differences between those two on a privacy level get smaller and smaller so that there is less opportunity for discrimination on the network basically.
So as long as we keep on pushing that ethos, that's a kind of a social thing as well, Because lightning could have been like a club of the rich nodes like Bitfinex and Phoenix and whatever and you know you can lose use lightning but only hop one you know then you need to connect to one of the big ones or for example the fact that we have onion routing makes it very hard for them to close off the system, right?
So if we keep pushing the privacy features, then that also means that we can make sure that Lightning can exist into the future as a equal system where everyone can participate.

Speaker 6: 00:30:33

But I think the important thing is that the privacy features, they got to come first.
You can't expect to bolt them on later.
A hundred percent agree.

Speaker 3: 00:30:40

You're kind of doing that now though with planet paths.
They are being bolted on as we speak.

Speaker 0: 00:30:45

Well, I mean, let's, let's poke a little fun at Tade here and I'll say I'm very very happy that his proposal to not do onion routing at first and try to add it later is not what we did because given the current state of players in the network like LightSpark, all these big businesses getting on board, I don't think we would have been able to add that afterwards.

Speaker 6: 00:31:10

Right.

Speaker 1: 00:31:11

Is the lighting network over reliant on Tor for privacy?

Speaker 0: 00:31:18

From a theoretical point of view yes but you know it's it's really hard to run a reliable node over Tor.
Like the payment reliability goes way down, the latency for payments goes way up.
I know a lot of very privacy focused people that don't run their node over Tor.
Like mine is just through a conventional proxy over ClearNet.
It's just really, really hard to get the reliability you need for, you know, high success payments or high payment success rate over Tor.
It's just too unstable of a system.

Speaker 3: 00:31:54

Yeah, Tor is fun and games for loading websites.
A little bit of HTML and CSS that's fun and games, but long-lived, high, like, interactivity TCP connections for lighting peer-to-peer gossip and sending onions around, like, just speaking from experience, it just doesn't work out well in the long run.
They're going to run into flakiness eventually and then you'll sit there rebooting everything and praying your next circuit is going to be better.

Speaker 1: 00:32:18

My favorite line.
No, doesn't like tour, right?
Evan, your favorite lightning wallet.
What did I say?
Sorry.
Node.
No, my favorite lightning wallet.
Walton node management tool.

Speaker 6: 00:32:31

Yeah.
Walton's had a lot of issues connecting to his note remotely using Tor.
Oh boy.
Thank God we got a lot of alternatives.
We got to talk about a couple of them.
Talescope.

Speaker 2: 00:32:41

Yeah, I mean, I think a more interesting or probably like important question is just, is the world relying too much on Tor for privacy at the network level?
And it's like, absolutely.
Like, Tor is the only thing we got as a, like, even remotely an antidote at this point that's being used widely in production.
Like, you know, we should have better mix nets and improve on Tor.
But yeah, you're going to challenge that.

Speaker 0: 00:33:03

Nim is a promising looking direction for something to really compete with Tor and bring a degree of robustness that's been hard for that.
Yes, it is.
And I have made many, many criticisms over that decision to the team over the years, but it has been a stereotype, you know, promoting these things.

Speaker 1: 00:33:26

Kat, Callie you seem to be disagreeing with Alex that the tour is a we've got.

Speaker 5: 00:33:31

I, I Don't know why everyone is so bearish on Tor.
Tor is I think pretty cool I mean I have other critic about Tor not the reliability the fact that it has centralized Registry basically and You know that's a problem and then there is something like Nim that tries to solve that with a shitcoin instead of a centralized registry Which is also not a ideal solution obviously there's I to P which is also getting more and more popular also supported by Bitcoin D and generally the interest for mixed net seems to be growing and I mean we shouldn't forget that Tor it was basically invented by the US secret military three-letter agencies and we're just their cover traffic at this point so they can hide in our masses.
But you know the fact that this network supports almost all of Bitcoin plus almost all of dissidents in the world and many more people that try to escape the Chinese firewalls, the Russian intranets, is simply amazing to me.
That this thing works is amazing, but I would agree that it hasn't much improved in the last decade or so.
So I don't think that we're over-reliant on Tor at all.
It feels like we should use it more and try to improve it more.
And if it's not Tor, then it should be one of these alternative systems.
But the idea that we can build a second layer on top of the internet that can hide our traffic, I think, is extremely valuable and will be something in the future that we will keep using that for a long time.

Speaker 6: 00:35:11

Can we help improve Tor by fixing some of the incentives with Lightning and Cache?

Speaker 1: 00:35:16

Right.
So one of the things I think many of us appreciate is how network topologies change based on their incentives.
I don't know how many of you are familiar with LTOR, a relatively new project, a guy out of Texas, trying to incentivize people to run Tor nodes, right?
And get paid.

Speaker 2: 00:35:39

Yeah, it started as a Bigwin++ hackathon project, actually.

Speaker 1: 00:35:42

It did indeed, so.

Speaker 2: 00:35:43

Really?
Wow.

Speaker 5: 00:35:44

Well, the tor network is every now and then is the tor networks under attack everyone probably knows that somehow Felt that with the lightning note for example and tor actually has implemented proof of work a couple versions ago to mitigate the issue I recently was told the story by one of the contributors there that this whole war Started with darknet markets to darknet markets waging war Towards each other on the Tor network trying to take out the other darknet market to gain like dominance there So it wasn't probably like a state sponsored attack, it's just literally drug dealers doing their thing.

Speaker 2: 00:36:23

Just fighting on the internet.

Speaker 0: 00:36:25

Be a normal person and go buy drugs from someone on the street.
Buying it on the internet is retarded.

Speaker 5: 00:36:32

Not recommended.
But so what Tor then did is they took a look at Bitcoin and implemented proof of work in their protocol.
So the rationality here is when they wage war on the Tor network, everything stops working.
So it's strictly better to exclude a bunch of phones and JavaScript Tor clients that cannot compete with servers by imposing proof of work.
So you as a Tor service, you can just say, now this is getting a bit too crazy.
I need proof of work for my packages now.
And then you kind of exclude 50% of the users, maybe, just making up that number.
But at least the other 50% gets to enjoy your service.
So all of this is for, we know, like, if you close the hash cache loop again, it started with Adam Beck email spam Satoshi looks at it puts it into a Satoshi like into a set Using proof-of-work, and then we start using Satoshi's again to mitigate spam.
I think this is a beautiful circle.
So I think it's a great idea to use Bitcoin to help out these anonymous systems that clearly need some rate limiting.
But I think that lightning is not the best way to do it.
And the reason for that is that lightning is great when it works, but it's really bad if it doesn't work.
And for these systems you need something that just always works.
You can send like, you're downloading a video and it works like for 10 minutes and then an HTLC gets stuck and now you have to like wait for two weeks until it settles.

Speaker 1: 00:38:10

So what you're saying is you need offline payments and that maybe there's something in this ecosystem that provides that, is that right Kalle?

Speaker 5: 00:38:17

Yeah I can think of a few things.
I mean, obviously an e-cash payment will always work, but there are also other, you know, layered systems on top of Bitcoin that don't have this issue where you have timeouts, basically, like HTLCs that need to timeout somehow in order to resolve a conflict.

Speaker 0: 00:38:32

ARC could be an answer.

Speaker 2: 00:38:33

Like ARC

Speaker 5: 00:38:34

or Fedinance, yeah.
Yes.
So, but with, you know, I have issues.
ARC is going to be very centralized service.
You know, we should not build the Tor network using ARC, I think.

Speaker 0: 00:38:46

Well, I think there's a deeper problem to confront here and I think just ideologically like most of the people who contribute to Tor are not fans of capitalism, they're not fans of interjecting monetary aspects and incentives into systems like this.
So even if we can technologically figure out a way to deal with this problem, will the team be motivated to actually implement or integrate anything?
Or will they fight or resist that on ideological grounds?

Speaker 5: 00:39:19

I wouldn't make like a bad faith argument about that.
I think it's fairly reasonable to assume that, you know, you have a system that is supposed to serve everyone and then now you want to make it...

Speaker 1: 00:39:29

want to limit it to 40, 000 people.
You know, that's the number of Bitcoiners in the world.
So,

Speaker 2: 00:39:35

exact number.

Speaker 1: 00:39:37

Yeah, exactly.
So, I'm not sure, you know, you can put a price tag on everything, but there is, First of all, there's differences in the world.
You know, a US-American person and, I don't know, whatever, somewhere else, and they are supposed to pay the same price for the service, one problem.
The other problem is not everyone has Bitcoin.
That's actually the biggest problem.
We could solve spam issues for so many systems out there using Bitcoin, but there are not enough Bitcoiners to make it worthwhile.

Speaker 3: 00:40:08

Philosophically, it's also just a growing worry is that you have this paradox where the price has to be high enough to discourage spam traffic but it also has to be low enough that it really doesn't affect the user and I'm terrified that those numbers are actually like inverted where the price that's too high for spammers to overcome is actually higher than the amount that is gonna not affect the user experience.
So I'm not so sure we really have a solution that will work at this scale.

Speaker 4: 00:40:39

You're looking on the base there?

Speaker 3: 00:40:42

No, I mean anything.
Just anything that's like just paying to reduce spam.

Speaker 1: 00:40:47

You want to send a message and how much is that going to cost you?
Like let's say it's one cent, you know, is it worth one cent for a message?
Maybe yes.
But is it worth like $1 for 100 spam messages for a spammer?
Probably yes too.
So that's a good price.

Speaker 3: 00:41:01

I can take you down.

Speaker 1: 00:41:02

So yeah.

Speaker 4: 00:41:06

Is the current low fee environment evidence of little demand for Bitcoin transactions Or is it evidence that lightning is already scaling to meet the needs of its users?

Speaker 0: 00:41:15

I?
I think it's it's the latter.
I think clearly a large amount of transactional use has slowly shifted over the last few years onto the Lightning Network and that's just looking at the payment data from a number of companies who've integrated Lightning, just my anecdotal experience.
I almost never make an on-chain transaction for something these days anymore.
And it's just, it's like this is what we were hoping for.
You know, it's just kind of the question of how long is it going to take for Javon's paradox to play out in terms of using the resource that is block space more efficiently, driving that huge jump in demand for it.
And a couple of us have said this up here, it's just not enough people own Bitcoin.
And that is the core of almost every problem as far as the lack of transactional use.
Like somebody needs to be able or wants to receive it.
Like the person paying them needs to have it to give it to them.
And I think that just boils down to like we are not very densely packed together geographically, but everyone keeps fixating on like these, you know, narratives or attempts to push people to use Bitcoin in meat space.
Like go buy your coffee or eat out at a restaurant or things like that with it, as opposed to trying to create digital economies, where that geographic density isn't a problem.
Like you're on the internet, you can pay or receive any digital good or service from anyone on the internet.
It doesn't matter where you are in the world.
And I really think if we want to kind of see that manifestation of Bitcoin as a means of exchange actually happen, we need to focus on where it's logical, which is the internet, not in person.
Like it's just there's not enough of us in the same place to actually bootstrap that means of exchanges.

Speaker 4: 00:43:23

Do you want to repeat the question because I do think you answered it but you also were a little bit off there.
So is it the low, is it, is it the low fee, is it the, Is the current low fee environment evidence of little demand for Bitcoin transactions or evidence that Lightning is already scaling to meet the needs of its users?

Speaker 1: 00:43:40

Both.
Can it be both?

Speaker 4: 00:43:42

Sure.

Speaker 3: 00:43:43

Yeah, I mean, I think everybody not paying for their coffee on-chain is probably contributing to some degree.
Yeah, so...

Speaker 2: 00:43:51

But did it happen to you that the Lightning transaction was costing a lot more than on-chain one?
Because it did happen to me several times.

Speaker 5: 00:43:58

It happens all the time.
If the amount is high enough and you pay a percentage instead of a flat 30 cents, easy.

Speaker 2: 00:44:05

Yeah, so then why would people prefer Lightning when it's more expensive than on-chain?

Speaker 4: 00:44:12

The immediate finality is important UX in a payment.

Speaker 2: 00:44:16

Well, sometimes it's like double, triple, quadruple more expensive.

Speaker 3: 00:44:20

Are you talking about like when you hit like a channel open or just like a normal payment?

Speaker 2: 00:44:24

Sometimes like a normal payment.
With a channel it's even more.

Speaker 0: 00:44:27

When you have like a really bad liquidity situation like some notes.

Speaker 5: 00:44:32

Come on,

Speaker 4: 00:44:32

you're sending like a few million sacks you mean like on lightning rather than on chain.

Speaker 3: 00:44:36

You're getting abused if you're paying more for a lightning payment that's not opening a channel.

Speaker 0: 00:44:42

The this this is it's the strategy incentive of a routing node operator to maximize their revenue.
So they are going to play games where they try to tactically arrange their channels or push fee rates in one direction or another to their benefit.
I mean,

Speaker 3: 00:44:56

then you should use a different wallet.

Speaker 5: 00:44:58

That's not a good thing.
Guys, guys, seriously, like an on-chain payment right now at .1 sat per VBAT is like how much?
50 sats or something?
Like you easily pay tens of thousands of sats for huge lightning payments.
Easily.
Yep.
Like this happens all the time.

Speaker 0: 00:45:14

This is not some outrageous node, like basically robbing you at the day that robbing you with crazy outrageous fees that's just the way it is right now big lightning payments you pay good money for them I mean I think like this narrative of like lightning being super cheap to use is just a huge mistake as a narrative in the exact same way that that narrative was crafted about on-chain transactions 10 years ago.
Like we can't make that promise.
And like this example of like fluky things like this even when on-chain fee rates are non-existent, it's just an inherent consequence of the liquidity dynamics of how the network functions.
But project forward another 10 years, think of higher fee rates, a more mature fee market, like at the end of the day, the fees that you pay on Lightning are going to have to recoup the on-chain costs that Lightning node operators experience, or the entire thing is economically unsustainable.
So just making this promise that lightning will always be cheap payments, it's just not reality.
And we're doing the exact same thing we did 10 years ago when everybody just assumed we would increase the block size when fees, like when we hit that limit and fees went up, we're creating the exact same problem of laying these false expectations down and then when reality goes no, like you're wrong, you're going to have a bunch of people like who've plugged into this system, gotten used to using it, assuming it's gonna work like this forever, and then reality kicks in.

Speaker 3: 00:47:01

The whole point of lightning is that you have fixed upfront capital costs for an indefinite number of payments through that capital.
You deploy once and then you get to reuse it over and over again.
I think the mature version of lightning will adhere to that strength.
If we're having to cover on-chain costs all the time and we're moving liquidity around, then that doesn't seem like a sustainable future state.

Speaker 0: 00:47:26

Well, so are we talking about the magical economy in the future where everybody receives exactly as much money as they pay constantly, it's always going to have a directional push in one direction that has to be rebalanced.
And ultimately, you can delay it, you can play balancing games, but at the end of the day, like when you've exhausted all of those options, you are going to have to interact with the base layer on chain to deal with the consequences of that directional push.

Speaker 1: 00:47:57

And pay your 30 cents.
For now.

Speaker 4: 00:48:03

These seemingly competing Ideas are even published in Fidelity's report on the lightning network Well two key takeaways one of the key takeaways they said a well-optimized participant in the Lightning Network can see transaction fees as low as 0% and payment completion times of less than half a second, but they also make one of the key takeaways that Lightning can be viewed as a yield-bearing network that does not require users to give up the control of their Bitcoin.
How can you have 0% fees and yield?
You can't have both, right?
It's obviously, these are extremely...

Speaker 0: 00:48:39

You have to look at that from two directions.
Like, the fee the user is paying, and from that perspective.
But then also, like, what is a node operator actually receiving in terms of profit?
The fees can be very high from the user's perspective.
But if most of that is the node operator just recouping their cost of interacting on chain, they're not actually making that much yield and profit.

Speaker 3: 00:49:04

Yeah, I don't think it's a fair characterization.
I think the majority of the time that users are paying a lot is because they are using a wallet that has one, that has a lightning node with one channel, to somebody that's overcharging them because they can.

Speaker 0: 00:49:16

Well, I'm talking like projecting out and like higher people.

Speaker 1: 00:49:19

All right,

Speaker 4: 00:49:19

guys, well, enough on fees for a minute.
I have one further question, and then we have a couple more minutes for questions from the audience.
The growth of the Lightning Network, and this is something that is difficult to measure, you don't know what the total transaction volume is, is gonna be driven by a number of different factors as we move forward.
How much of it is gonna be driven by things like e-cash and ARK and other tools that are actually about Bitcoin versus how much of it is going to be driven by assets on Lightning and is this a real problem when we look at the Lightning network moving forward?
Does the growth come from a base that is increasingly prone to regulatory attack?

Speaker 0: 00:50:25

I mean, the speculation, like either way, But I think looking at the reality on the ground, that the transactional use of things like stable coins far exceeds people transacting natively with an asset like Bitcoin.
That if we actually do see deployment and issuance of stable coins on Bitcoin and see that link into the Lightning network as a settlement mechanism, that probably will be the primary driver of any growth or revenue increases for node operators on Lightning.

Speaker 2: 00:51:01

It's just-
Like stable channels?

Speaker 0: 00:51:02

I don't know.

Speaker 4: 00:51:03

Shout out Tony, let's go.

Speaker 0: 00:51:05

Yes, I would prefer if it was stable channels, but I think the reality is it's going to be things like tether tokens issued and then just having the channel do the atomic swap between some service provider to forward the payment in Bitcoin.

Speaker 3: 00:51:22

Everybody and their mother is starting a new stablecoin protocol for the record.

Speaker 6: 00:51:26

Yeah,

Speaker 3: 00:51:26

seems like every week there's a new one.

Speaker 4: 00:51:27

If you would like to start your own stablecoin thing, I think you should go to Tether for funding, right?

Speaker 3: 00:51:33

I'm curious to hear from Callie.

Speaker 5: 00:51:35

How much do you think about the regulatory burden that mint operators in the future will have to bear no comment The one thing I'm not exactly sold on yet is when you have these stable coins on Bitcoin, why would you want to have them and use them on Bitcoin in the first place?

Speaker 2: 00:51:56

Tether is going to do an RGB.

Speaker 5: 00:51:57

Yeah but like why wouldn't you use the tether chain, the plasma thing?
What's the advantage of using it over Lightning with all its intrinsic downsides?

Speaker 4: 00:52:05

My skin's cream right now, I have no idea.
I'm not the person to answer that.

Speaker 2: 00:52:09

You're asking the wrong person.

Speaker 0: 00:52:12

I think this is very much an example of a solution looking for a problem.
Like a stablecoin is centralized at the end of the day, it's worthless the instant the issuer won't redeem your coins or starts playing funny games.
Like whether it's on an SQL database like something like Solana or the Bitcoin blockchain it's utterly completely irrelevant.
Exactly, like why do we need a permissionless network to transfer around IOU tokens of someone's bank account?
Mm-hmm, I mean like charitably I think the only straw man you could make is if you look at things like RGB or taproot assets, you can make the argument that how those protocols are structured technologically, it would make it a lot more difficult to do things like have the selective ability to like freeze or seize a specific users coins, because this is all client side data, like none of it's explicitly recorded on chain.
But you know, again, like, there's no reason you can't architect systems like that that provide privacy in a similar way that don't connect to Bitcoin at all.

Speaker 5: 00:53:26

Yeah, I'd love to be proven wrong.
I'm just entirely sold on the concept of stablecoins driving lightning that McGrowe fiat.

Speaker 3: 00:53:33

I mean, there's huge demand for dollars around the world.
I mean places that don't have access to dollars want dollars.

Speaker 1: 00:53:39

Yeah but why lightning?
Sounds retarded.
Yeah, fair enough.

Speaker 2: 00:53:43

And a huge amount of people who don't want volatility.

Speaker 3: 00:53:47

Yeah but it's not the dollars.

Speaker 1: 00:53:48

I think generally like the stable coins I mean I see two reasons.
First shit coining that's one thing that drives it printing money is fun for some people.
Secondly is people don't like to control their infrastructure So it gives them like a better time in front of court when you can say like, oh I don't control Tron.
I can't like you know I can't control whether this person sends my assets to that person because it's all on this public infrastructure.
So there is also, that's also one reason why people want to build on something like Bitcoin, but they could also just take one of the other kind of a phantom, decentralized systems where you can just throw your hands up and say like, oh, I didn't know about this eventually.
But I agree that it's a huge larp because as long as you can freeze these assets with a click of a button, then it becomes a kind of a clown show.

Speaker 3: 00:54:43

So that big dollars are cooler because you don't freeze them, you just get exposure to them.

Speaker 4: 00:54:52

Let's hear some questions from the audience.
Before we wrap up this panel.

Speaker 1: 00:55:02

People are speechless.

Speaker 4: 00:55:05

They should have enough of Shinobi talking, maybe.

Speaker 6: 00:55:07

So, comment and a question.
First off, I'll say that report was not the Fidelity report.

Speaker 4: 00:55:11

It was in partnership with Voltage, my bad.

Speaker 6: 00:55:14

Fidelity Digital Assets in partnership with Voltage.
I had a question.
So I was at a Presidio Bitcoin for Bitcoin Design Week last week, and Christoph Ono from the design community had an interesting idea.
He's been really drilling into the fees problem lately and just kind of exactly what you all have been talking about, about kind of unexpected fees that pop up whether it's on-chain or larger than normal lightning payments and he kind of did this analysis of like you know remittance companies not Bitcoin like remittance companies and just found that their advertising just goes hard on fees like gigantic letters saying like we are the lowest we save you so much on fees we're like 0.1% fees they just like that's all they do is just go hard on their their low fees and then you look at all the Bitcoin products and they're always like yeah we're a simple wallet with low fees.
And it's just really kind of passive and weak.
And so he was trying to think, could there be a company that you prepay for some kind of plan and your fees are kind of kept under control with your Lightning service provider.
Not sure how it would work on a technical level, but I'd just be curious, any thoughts, is that the sort of thing an LSP could implement?

Speaker 0: 00:56:24

I mean, I don't see any way you could do that without hedging and creating some kind of derivative product where you could actually find a counterparty willing to like trade against what your fee expectation.

Speaker 3: 00:56:37

Can we hear from the guy that runs an LSP?

Speaker 4: 00:56:39

Yeah that's about literally my thought.
The universe sent it like Evan come on.
The guy that actually runs an LSP runs.

Speaker 7: 00:56:47

There's some ways but I'm not sure people would want to accept all the trade-offs.
I mean, either you're shifting risk around, you don't necessarily have to turn into a derivative, even though that'd be the sexy way to do it.
Or you introduce more components of trust to help the cost down.
I mean, there's countless ways to do it.
And yeah, I mean, we already have a subscription service, UsePay Plus, that gives you a discount on LSP services.
You could definitely fix costs in various ways.
I think the whole space in terms of these service providers is just getting started and is gonna mature by leaps and bounds in the coming years.

Speaker 1: 00:57:28

I think fees aren't a problem, Unpopular opinion, but who cares about 100 SATs fees or 200 SATs fees or 0.2% fees or 0.5% fees.
I mean our competition is literally trash.
So I don't think that anyone said like, oh I won't use Bitcoin because the fees are too high.
This is like an intermediate episodes where four megas hit the chain every ten minutes or something, then we get into those problems.
But I to me, this feels like incredible technology.
And I'm happy to pay fees for using Bitcoin.
I kind of assume that it's the same for everyone here.
So maybe this is just Like a non argument.

Speaker 7: 00:58:11

Maybe this is something that that really doesn't affect too many people Yeah, I mean, I mean honestly like the bar is so low like we don't have to be perfect.
We don't have to have zero fees.
We just have to be better than the incumbents.
And then you have people like the steak and shake COO going out and saying, Hey guys, we implemented Bitcoin.
It cut our processing costs in half.
That's huge.
That's all we need.
We just need to be twice as good as what exists now.

Speaker 5: 00:58:37

In all fairness though, Stake and Shake was a receiver of Lightning payments and the sender pays the fees.
So, er.

Speaker 2: 00:58:45

In a wallet UI, in cases if lightning fees are too high, it would be great if the UI can kind of detect it and maybe give you alternate ways how to send Bitcoin at this exact moment.
Maybe use some other tool.

Speaker 1: 00:58:59

Maybe you could use...

Speaker 0: 00:58:59

could use Cashew.

Speaker 2: 00:59:01

Or Cashew or some RGB coin conversion or like whatever the hell else because like this would help users to see that like this is unreasonably high amount right now to send and if they don't want to send on chain and wait 10 minutes they would have this this and that alternative.

Speaker 0: 00:59:18

Right, right.
Have a price breakdown across the different layers.

Speaker 2: 00:59:21

Maybe.

Speaker 3: 00:59:22

Unified QR codes help.

Speaker 0: 00:59:26

Definitely.

Speaker 3: 00:59:26

Unchain and Bolt 12.

Speaker 4: 00:59:31

QR code.
Well,

Speaker 3: 00:59:34

you need to be able to decide which payment rail you're going to use.
Like you want to scan once and then have like the best option to be chosen for you in the best case without having to have a PhD in fucking Bitcoin.

Speaker 2: 00:59:47

Yeah, or simplify it like to bare minimum.

Speaker 5: 00:59:54

I have a question.
So there's a really cool Zeus hackathon prize, which the goal is to HacktonPrice,
which the goal is to enable discovering of trusted mints in SUSE.
And Evan knows about cachemints.space, but in cache.me, Kali, there's a very cool feature called Discover Mint.
And I've been told that there's something called KYM, Know Your Mint.
And So my question is, can you explain Know Your Mint to Evan?
And how it searches Noster for recommendations for cache mints?

Speaker 3: 01:00:48

Well, I would run into the risk of repeating, not myself, but someone has actually done that after his talk.
So, thank you for your question, but you should have watched his talk.

Speaker 4: 01:01:00

Education happens incredibly fast here at Bitcoin++ and this was the scaling lightning panel.
I think the way we scale lightning is by having more and more Bitcoin++'s.
So I'd like to firstly thank all of you audience that came to this panel.
Bitcoin++ and panel discussions wouldn't be the same without all of you, but also please give a round of applause for my panel Alex Lewin, Callie, Shinobi, Evan, Michael from Bolts and Rita.
I'm Walton.

Speaker 3: 01:01:30

Thank you very much.

Speaker 6: 01:01:45

Alive, unstoppable, through rain and shadows we run.
Forged by fire, forged by freedom.
Because now, the current is ours.
Bitcoin, plus, plus Berlin.

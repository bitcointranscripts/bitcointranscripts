---
title: 'Scaling Lightning Panel - Lightning++ Berlin 2025'
transcript_by: 'dillamondgoat via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=oFDaC_2WjP0'
date: '2025-10-02'
tags:
  - 'btcplusplus'
  - 'bitcoinconference'
  - 'lightning'
  - 'scalability'
speakers:
  - 'Evan Kaloudis'
  - 'Shinobi'
  - 'Calle'
  - 'Michael Boltz'
  - 'Alex Lewin'
  - 'Walton'
  - 'Rita'
  - 'Dusty'
categories:
  - 'education'
source_file: 'https://www.youtube.com/watch?v=oFDaC_2WjP0'
summary: "Sign up for one of our upcoming dev conf at https://btcpp.dev\n\nWebsite: https://btcpp.dev/\nX: https://x.com/btcplusplus\nNOSTR: https://iris.to/npub1dwah6u025f2yy9dgwlsndntlfy85vf0t2eze5rdg2mxg99k4mucqxz7c52\n\n#btcplusplus #devconf #bitcoineducation #bitcoinconf #bitcoindev #bitcoinconference #bitcoin #cypherpunks"
---
## Panel Introductions

Walton: 00:00:01

But it wouldn't be a `Lightning` panel without a Greek god himself, Evan Kaloudis, welcome back.

I got told that panels have a fixed size, but my understanding is that `Lightning` panels have a special technology called `splicing`.

We can increase the size of a panel beyond what is already preset.

I'm going to splice two panelists into the panel right now.

We have Rita joining us.

And of course, the creator of `splicing`, Dusty.

Actually, Dusty has to go.

I don't want you guys to feel shortchanged, so I arranged a special swap.

That swap is powered by no one else other than Michael from `Boltz`, so I'm swapping Dusty out, and Michael from `Boltz` is coming in.

Thank you, Dusty, for your help with the `splicing`.

Thank you.

My most esteemed panel.

Let's construct it.

The base layer, we have Evan Kaloudis.

Please come take a seat.

Calle: 00:01:18

No, don't listen to this guy.

Walton: 00:01:22

We have Rita.

He's like, see.

And then Michael, of course, is going to help me get these gentlemen between layers here as he so often helps Bitcoiners move between layers.

Michael if you can just hold this structure with me and the three gentlemen are going to climb up the back one at a time please gentlemen.

Alex: 00:01:50

There isn't.

Walton: 00:01:51

Shinobi doesn't weigh very much, don't worry.

Bitcoin doesn't care.

Just pay for Bitcoin on top, it's okay.

Alex: 00:01:58

It's the metric system, it doesn't count.

Shinobi: 00:02:03

We are very serious people.

Calle: 00:02:07

By the way, Shinobi looks like in the memes.

I didn't know.

What's up?

Hi.

Walton: 00:02:17

Michael, you can come take a seat now.

Thank you.

Calle: 00:02:18

Do you have a microphone or are you going to shout?

Walton: 00:02:24

Okay.

## Why Don't More People Run Nodes?

Walton: 00:02:24

My first question to my esteemed panel is it's never been easier to run a `Lightning` node.

It's essentially plug and play, so why don't more people run their own `Lightning` nodes?

Shinobi: 00:02:48

It's a huge pain in the butt.

You have to keep it reliably online.

You have to handle all the liquidity management yourself.

Make sure you have enough receiving capacity to receive, that your sending capacity is allocated intelligently so that your payments will actually succeed.

It's also just a lot of other issues that really have nothing to do with `Lightning` itself.

For instance, my place at home, I have a very unreliable router that loves to just randomly drop devices off the network.

Even though the `Lightning` side of the infrastructure works perfectly, my node is constantly conveniently offline when I'm traveling around the world and want to make a `Lightning` payment.

It's just a lot of things you've got to get hands on with.

Walton: 00:03:42

That's a skill issue, Shinobi.

Is that right?

Is that what you're saying, Calle?

Shinobi: 00:03:46

That's what I have to say to that one.

Calle: 00:03:48

Oh, Shinobi.

Here we are.

Walton: 00:03:50

Shinobi filtering his words there kindly for you.

Calle, your thoughts?

Calle: 00:03:57

I think one of the biggest issues is that you can actually lose money.

Lots of people who run `Lightning` nodes know that many people who run `Lightning` nodes are net negative, basically, with the routing fees that you collect for a year or two, and then you get force closed during a high fee period.

You can easily lose $50 or $100.

That's one problem why I know that some people just stop running their own `Lightning` node because it's not worth the hassle for them.

There is the centralized way of using `Lightning` with a centralized `LSP`(Lightning Service Provider) maybe, or something like `Phoenix`, that really works really, really well.

I have no complaints there.

I've been using `Phoenix` for many years, and it's been the same `Lightning` node since the beginning and it works just really, really well.

It basically depends on how you want to use `Lightning` and if you're going to go the `LND` routing node way and hope that you can make some extra buck, I think that's super challenging to actually pull off.

Other than that, I think just the fact that most people don't want to run a server, we just need to recognize that fact.

It's not going to change very fast and I think home nodes don't really affect that a lot because `Lightning` nodes like to be well connected and on in the cloud in the best case or on a `VPS` or something.

Although home nodes really do work if you have a stable internet connection.

Lastly, I think there is the ugly truth about Bitcoin is that there is around 40,000 people or so that use `Lightning`.

That number isn't growing that much so why don't we have 400,000 people using `Lightning`?

Should be the meta question around it.

The number of Bitcoiners is just growing very slowly.

The number of people who use Bitcoin for payments instead of just ETFs and stacking.

That's probably the strongest factor explaining why not many more people use `Lightning`.

Walton: 00:06:20

Alex?

Alex: 00:06:21

The question was why don't people want to run `Lightning` nodes?

Walton: 00:06:25

Yeah, why don't people run their own `Lightning` nodes if it's never been easier?

Alex: 00:06:29

Why would somebody want to run a `Lightning` node first?

Are you talking about why aren't there more hobbyists trying to become routers?

Or why aren't there more people spinning up new `Lightning` nodes just to receive money?

Walton: 00:06:43

Both.

Alex: 00:06:44

For why aren't there more hobbyists trying to spin up routing nodes is because it's high effort and you're probably going to lose money.

It's still high effort.

It's easy to spin up a new node, but if you're going to run a routing node as a hobbyist, you really have to be checking your channels every day.

It's hard.

By default, you will lose money because there's people trying to siphon your liquidity.

You can make money off of people that don't know what they're doing running `Lightning` nodes.

That's maybe one reason why you wouldn't want to run one as a hobbyist `Lightning` router.

For the end user it's really easy to spin up a `Lightning` wallet, but to receive money, the incumbent system that people are used to for receiving money is effortless.

Zero effort.

In my opinion, in order to really compete for people in swaths that don't care about money that much, we have to compete on that UX.

We have to be effortless.

We can't just be easy.

Walton: 00:07:38

Someone helping with the UX and many more things.

Evan.

These guys sound kind of bearish on `Lightning`, huh?

Evan: 00:07:47

Fucking doomers.

Calle: 00:07:49

Realists.

The question was negative.

Evan: 00:07:52

Come on.

Is it a better payment experience going to the app store and hitting start wallet or is it a better payment experience going to the bank and bringing all your identification and proving your income?

Listen, we have a lot of work to do, but there are definitely advantages in our UX that we need to highlight and lean into.

The fact that you can spin up a wallet with a few clicks, put a `Lightning` address in your profile and start receiving funds from people all over the world without `KYC`, that's amazing.

We've got to lean into that.

The reality though is that our ecosystem is super tiny right now.

The resources that the average person has is obfuscated by all the noise out there.

The advertising from the exchanges, which are really shitcoin casinos, want to point you towards the latest shitcoin so that they can make fees off the transactions, the trading volume.

The news being inundated with stuff like the ETFs or the latest treasury company.

Lastly, just not enough places to spend it.

How many places in Berlin can we find to spend Bitcoin at?

Ten, maybe twenty tops.

You probably can't live off it here unless you like going to the same handful of restaurants every day and we need to make efforts to improving that.

Walton: 00:09:35

Is the reason why more people aren't running their own node because your company is so good, Michael?

Is it just because I have this recurring theme that every time something's working in Bitcoin and `Lightning`, you pull off the mask, as in by asking more and more questions, and underneath it's just Michael from `Boltz` every single time.

Is this why no one's actually running their own `Lightning` node, because you don't need to anymore, you just use Michael.

Is that it?

Michael: 00:10:01

That's all my database.

That's the answer for it.

Seriously, why aren't people running more lighting nodes when it has never been easier?

It's because the alternatives that you don't have to run one have never been better with `Cashu`, `Fedi`, `Liquid Swaps`, `Spark`, `Ark`.

There are so many more things that connect you to `Lightning` for which you don't have to run your own node.

Even if you were to run a node, for example with `Zeus` embedded, those don't show up in the public metrics because they are private and don't announce themselves to everyone.

Why would you?

Because as everybody is saying running a `Lightning` routing node that's publicly announcing itself just sucks in every single way.

You either lose money if you are force closed, or until your SSD dies and then all your money is gone.

Unless you pray you have the static channel backup stored somewhere.

That's just a horrendous experience for everyone.

## Improving the Lightning UX

Walton: 00:10:58

As a user, Rita, who do you most agree with here and why?

Rita: 00:11:07

Is it working?

Everyone has a fair point.

I agree that the UX part needs to be improved a lot more.

One of the tools that I actually love using the most was `Phoenix`, mainly because `Lightning` there is under the hood.

You don't really have to understand what you are doing and what is going on.

It is just there, it's super fast, it's super simple.

You don't have to understand what are the channels, how do you close it in the right way, how do you open it in the right way, what are all of those dozens operations that you need to do.

The UX simplicity that it is just working by itself magically under the hood is really the key to people using `Lightning` more.

Walton: 00:11:54

`Phoenix` is one of my favorite apps but it has some friction especially when you're teaching new users about `Lightning`.

If you want to tip a waiter or something and you tip them on `Phoenix`, they're going to take a decent cut of the fees to open a channel.

To give you some inbound liquidity.

Rita: 00:12:14

There should be UI tips or something like that for people like, hey, if you want fast use this, if you want `on-chain`, explain in a few words what's that.

Michael: 00:12:23

We had that exact problem with our local bar, the Bitcoin meetup, where we just had the waiter install `Phoenix` and then everybody paid their beers with `Lightning` to them.

Every single one of those payments was an `on-chain` splice in and those costs do add up.

Calle: 00:12:39

What?

Because the channel wasn't ready yet?

Michael: 00:12:42

I have no idea why, but that was the situation we ended up with.

Is that better UX?

Rita: 00:12:46

The `on-chain` fees were super high at that moment and that's why it was.

Michael: 00:12:49

Not super crazy high but if you do ten of those splice-ins over the evening, it adds up.

Calle: 00:12:54

I want to say something controversial.

I think it's a really bad idea to onboard someone onto Bitcoin with a non-custodial `Lightning` wallet.

Yes.

I've been using these tools myself for a very long time, don't get me wrong.

But this you're going to lose money with your first transaction, it's going to be super fast in the second transaction, but the first one really takes an hour or so.

And this whole if you lose it then everything is gone and where do I export it, how do I restore it.

All this is so much information for someone who just wants five dollars worth of Bitcoin.

This is why `Wallet of Satoshi` became so popular for so long because it didn't have that fee for you tipping your waiter or there wasn't a cut being taken seemingly.

Walton: 00:13:43

That's not proper `Lightning`.

Calle: 00:13:45

It's username and password which is also something I'm the first guy who criticizes these login methods all day long, but this is something that you don't need to explain to anyone.

Everyone knows how username and password works or email and password.

People don't even care about their password, because they know that they're going to be able to restore it when they lose it.

They put in a random password, not even saving it somewhere, because they know that there is this emergency button.

With all these options that we've talked about, you don't have that.

You need to be super sharp from the first second on and not make any mistakes basically and then you're good.

But for onboarding I think you want to receive money, that's all you want to do.

You don't want to learn anything, you don't want to get a PhD in Bitcoin to receive your first payment.

Walton: 00:14:36

But if you do want to get a PhD in Bitcoin, please keep coming to Bitcoin++ events.

It's the best way to further your Bitcoin technical education.

Thank you.

Rita: 00:14:43

Removing the fear factor really matters because a lot of people are really scared to lose their funds if they do something wrong.

Michael: 00:14:50

Rightfully so.

Shinobi: 00:14:51

I think it just comes back to what Alex said, people just expect I received the money, that's it.

Somebody who's confronted with what is receiving liquidity, what do you mean `on-chain` versus `off-chain`, this channel has to be set up first.

It's just so departed from their expected experience.

That is the worst way to try and onboard somebody.

Calle is entirely right.

That is the fastest way in the universe to create an impression in someone's mind that Bitcoin is a convoluted, overly complex thing that is completely counterintuitive to all their expectations.

You are going to make it harder to get that person to adopt Bitcoin in any way in the future or anybody that they talk to and share that experience with.

It's just the absolute wrong way to start somebody off.

Michael: 00:15:43

What's the right way then?

Shinobi: 00:15:46

Graduated wallets like Evan is building.

Calle: 00:15:49

I want to answer that question by a question to Evan actually, something that I didn't ask after your talk, if you'll allow me.

You know this concept of annealing, which is cooling a magnet down slowly, and if you do it slowly, it gets more stable, versus if you do it fast, then it's unstable.

I wonder if you think that you onboarding someone through a graduated experience, basically with zero information first, you receive money and you're done, and then slowly you increase the pressure.

Basically saying now you have 15, 20, 30.

You should now learn about this, click this button.

Did you read this?

Yes.

Okay, then you can receive more.

Going step by step by forcing the user to not understand anything in the beginning and then forcing them to understand slowly more and more, do you think that creates a more stable Bitcoiner?

Evan: 00:16:43

God, you're a nerd.

100% and listen, on the other side of the spectrum, the financial elites that are trying to take all the rights away and enrich themselves as much as possible use that very tactic.

Gradualism, right?

The analogy everyone brings up is boiling frogs in a pot.

If you turn up the temperature very slowly, eventually it's just going to get to a point where they just stay in there and they get cooked.

If you turn up the temperature right away, it gets really hot, suddenly they get out of that pot.

In the same regard, we need to think of how we turn on the pressure, the heat, very, very gradually as to not have our frogs jump out of the pot.

## Is It Still Lightning?

Shinobi: 00:17:29

I kind of want to come out of here left field and go back to an offhand remark you made a minute ago, Walton, that's not using `Lightning` properly.

I want to ask the question, what the hell do you mean `Lightning` in the first place?

If you really look at what it is as a protocol, the way a channel is structured and the pre-signed transactions that make it up, or the gossip protocol that's used to inform everybody the channels available on the network they can route through, or a million other individual components like `HTLCs` being used to route payments across multiple channels.

All of these are things that can be individually taken and replaced and done differently.

If you slowly piecemeal change these individual things until everything is different, it's the ship of Theseus.

Is that still `Lightning`?

I think this fixation on the shape of `Lightning` and how it works now and how it's implemented now or how you should use it now is a complete red herring question because at the end of the day every single component of the protocol can be replaced piecemeal and done in a different way.

We should appreciate that and actually be doing that in a way that learns from the friction points users encounter that deal with the problems that actually discourage users from using it.

Walton: 00:18:57

When I said not real use of `Lightning` I mean I think it's a common misconception amongst a lot of Bitcoiners, probably not those in this room, but the `Lightning` network growth is driven by people zapping each other on `Nostr` when actually those payments are often between the same custodian.

That's what I mean by not real `Lightning` payments.

Ones that aren't actually on the `Lightning` network, they're on a layer above, if you will.

Shinobi: 00:19:26

I would beg the question, would that also apply to your mind to users of `Spark` or an `Ark` implementation?

Those things are trivial to make compatible and interoperable with `Lightning`, but are those now a part of `Lightning` or are they their own independent thing?

Walton: 00:19:43

Is `Ark` custodial or is it self-custodial?

Shinobi: 00:19:47

`Ark` is a clear no to that, but `Spark`, that's an ambiguous grey area.

Walton: 00:19:53

State chains have trade-offs.

Shinobi: 00:19:56

I think we should stop fixating on these purity tests and whether something is or is not `Lightning`.

Does it work for a user?

Does it provide value and utility to a user that they were missing in their life otherwise?

And does it compose with all the other aspects of this?

Alex: 00:20:15

Maybe another way of saying this is why are we, or is `Lightning` the end?

What are we trying to do here?

`Lightning` is a tool, just like Bitcoin is a tool.

What is the end that we're going for?

I'd say it's something that approximates saving people from weak money.

How can we get people to use strong money faster and not get hurt?

`Lightning` is a phenomenal tool in that direction.

But the `Lightning` itself, it's not the end.

It's just a means to get to something more impactful.

Shinobi: 00:20:47

Completely agree that `Lightning` is not the end goal here.

It's the means to an end and it's the best tool we have at our disposal right now.

But if in ten years time we have something nicer or replace all of the parts with the next generation, that'd be fine too.

Evan: 00:21:02

Every tool exists of many components and if you upgrade each one of those components it doesn't mean that it's a different tool.

If `HTLCs` are going to be upgraded to `PTLCs`, it's not going to be not `Lightning` anymore.

It's just going to be points instead of hash time-locks.

## Routing Nodes and Centralization

Calle: 00:21:22

To me, one of the reasons I love `Lightning` is because unlike `on-chain`, if you run a `Lightning` node, you get paid for spam.

I get the people send me those one `sat` messages and I'm like, oh, thanks for that, thanks for that.

It's not dust because `sats` don't really exist.

Alex: 00:21:43

Channel jamming is a problem, let's be real.

Calle: 00:21:47

You just don't see it.

But jokes aside, routing nodes are able to earn real yield in Bitcoin terms, in self-custodied Bitcoin, and yet this yield increasingly comes from institutions deploying their capital with `Lightning` custodians.

Walton: 00:22:07

I'm actually very skeptical in the long term that that can be a material source of income.

I think you see a very, very fat-tailed curve where the largest nodes with the best connection in the network and a lot of capital deployed can actually see a decent return on things, but that drops off very rapidly the minute you start going out into more sparse, disconnected parts of the network.

That is just going to be a hyper-competitive thing.

Those yields, I think in the long term, will be driven down to absolutely nothing.

Because these large players will look at this as I can just park my money here.

Some specialist like Lightspark who knows what they're doing, can deploy it on the network and earn some income, and it's going to be a race to the bottom very quickly.

Ultimately I think just become kind of the lowest risk benchmark yield.

That will be what people will settle for if they are very risk intolerant.

They do not want to take any risk with their money to earn a return on it.

This will be the place they can park it and know that that risk is very minimal, but that yield will also be very low.

I think that's not a viable revenue strategy in the long term, trying to earn money off of `Lightning`.

I think services like what Michael does with `Boltz` and more direct monetized tooling like that, that is going to be where any substantial yield comes from in the network in the long term, I think.

Shinobi: 00:23:48

`Lightning` is not risk-free to run a routing node especially.

It might be considered low risk compared to custodial lending platforms and yield things, but there's still quite a bit of risk to it because it's a hot wallet in the cloud somewhere and there's also implementation risk of your lighting node having a bug.

There is responsible disclosures of grave bugs all the time.

There is actual risk there to have all your stash in a hot wallet, in a cloud, in a hugely complex application with a bunch of state with a database you can't properly back up beforehand and not really live.

There is risk there.

Bunch of risk.

It's not risk-free at all.

Alex: 00:24:34

Shout out Lightning Fuzz.

Shinobi: 00:24:35

Compared to BlockFi maybe, but not in general.

Evan: 00:24:39

Nothing is risk-free.

Shinobi: 00:24:41

There is no such thing as risk-free interest in Bitcoin.

There's always risk.

`Lightning` routing might be on the lower end, but there is still non-substantial, but not negligible risk.

I wouldn't put my whole cold stack into a `Lightning` routing node.

Michael: 00:24:54

100% agree.

I don't think that running a `Lightning` node is risk-free at all.

Just the fact that you can lose your database and you're wrecked is basically a no-go.

You can't just back up a seed phrase and be okay.

Walton: 00:25:05

We added scare quotes.

All right, the scare quotes have been appended.

Alex: 00:25:11

Also, there's no money in routing, no offense.

If you're gonna run a routing node, it's already virtually free to route payments on `Lightning`, which is phenomenal for users.

We can send payments anywhere in the world for free, basically.

The only way to make money in routing is if your inbound's free.

Shinobi: 00:25:27

Which is the case for the crazy yield numbers that have been circling around.

They make those numbers because their inbound is free.

There might be a couple players out there generating decent yield, but they have a very special positioning and it's a not fiercely competitive market right now.

Only a few people know where exactly to put themselves in that network to make it work.

But once those spots are known, it's a fierce competition and driven to zero.

Calle: 00:25:55

So do these inbound, outbound liquidity requirements naturally drive centralization of the `Lightning` network over time?

And will this institutional deployment of capital hyper-catalyze that process?

Walton: 00:26:14

I think there's just always going to be a natural drive towards centralization with something like `Lightning`.

It really, from a topological point of view, mirrors the internet in a lot of ways.

I don't think that means it's just going to forever get more and more centralized until there's one big super node.

There will always be those players who are a lot more central in the network topology than others, just like the internet.

There might be thousands of different `ASNs` across the world, but you still have very dominant systems like Amazon, Comcast, other higher tiered networks that are the bulk of the connectivity and where things route through.

But the internet is still not a place, despite that, where you can just flip it off right away.

Or one of those players can prevent other pathways or channels of communication through it.

It's just efficiency.

Looking at the internet as an example, we've settled in a place where we've leaned into that centralization a good degree to get the benefits of that efficiency, but not so much that the robustness and the redundancy that keeps the internet a free and open place have disappeared.

It's that balancing act.

Alex: 00:27:38

Even email?

Walton: 00:27:40

Email might be an example we just lost that one.

Michael: 00:27:43

My bad.

I actually think `Lightning` is almost a bit better than the Internet.

I would agree that there are centralization forces going on because just of the efficiency gains of having a well-capitalized node, it's economics driving centralization, and I think that was expected.

However, the fact that anyone can join the `Lightning` network as on the same playing field as all the other nodes is something special.

That is not the case on the Internet at all.

You cannot just be your own `AS` or start propagating `DNS` or whatever.

All these special roles that the internet has developed over the decades that are not accessible for any one person.

You can always host your own server, but first of all, you need an IP address that someone gives you.

You also need an ISP to even talk to the internet.

The internet seems like there are many more gates to become an internet player.

Whereas in `Lightning`, I think even if we have centralization forces, the fact that you can just spin up a node and you don't need to register with anyone, that you don't need to talk to anyone, you don't need to call anyone.

You are a node and you connect to someone and they typically accept your channel, which is something that we should be aware of how much that is actually worth.

Even if it makes a routing bit more inefficient and we've seen in René's talk previously, the edge nodes have a harder time in being good payment routers.

But the fact that we still allow that, and we should keep allowing that as long as we go, and we should work on more privacy features so that the difference between a big node with a well capitalized company behind and a pleb node which is an individual person's node at home, so that the differences between those two on a privacy level get smaller and smaller so that there is less opportunity for discrimination on the network.

As long as we keep on pushing that ethos, that's a social thing as well.

Because `Lightning` could have been a club of the rich nodes like Bitfinex and `Phoenix` and whatever and you can use `Lightning` but only hop one, then you need to connect to one of the big ones.

The fact that we have onion routing makes it very hard for them to close off the system.

If we keep pushing the privacy features, then that also means that we can make sure that `Lightning` can exist into the future as an equal system where everyone can participate.

Rita: 00:30:33

But I think the important thing is that the privacy features, they got to come first.

You can't expect to bolt them on later.

A hundred percent agree.

Shinobi: 00:30:40

You're kind of doing that now though with `blinded paths`.

They are being bolted on as we speak.

Walton: 00:30:45

Let's poke a little fun at `t-bast`(Bastien Teinturier) here and I'll say I'm very happy that his proposal to not do onion routing at first and try to add it later is not what we did.

Because given the current state of players in the network like Lightspark, all these big businesses getting on board, I don't think we would have been able to add that afterwards.

## Privacy and Tor

Calle: 00:31:11

Is the `Lightning` network over reliant on `Tor` for privacy?

Walton: 00:31:18

From a theoretical point of view yes but it's really hard to run a reliable node over `Tor`.

The payment reliability goes way down, the latency for payments goes way up.

I know a lot of very privacy focused people that don't run their node over `Tor`.

Mine is just through a conventional proxy over clearnet.

It's just really, really hard to get the reliability you need for high success payments or high payment success rate over `Tor`.

It's just too unstable of a system.

Shinobi: 00:31:54

`Tor` is fun and games for loading websites.

A little bit of HTML and CSS that's fun and games, but long-lived, high interactivity `TCP` connections for lighting peer-to-peer gossip and sending onions around, just speaking from experience, it just doesn't work out well in the long run.

They're going to run into flakiness eventually and then you'll sit there rebooting everything and praying your next circuit is going to be better.

Calle: 00:32:18

My favorite line.

No, doesn't like `Tor`, right?

Evan, your favorite `Lightning` wallet.

What did I say?

Sorry.

Node.

No, my favorite `Lightning` wallet.

Walton node management tool.

Rita: 00:32:31

Walton's had a lot of issues connecting to his node remotely using `Tor`.

Oh boy.

Thank God we got a lot of alternatives.

We got to talk about a couple of them.

`Tailscale`.

Alex: 00:32:41

I think a more interesting or probably important question is just, is the world relying too much on `Tor` for privacy at the network level?

And it's absolutely.

`Tor` is the only thing we got as even remotely an antidote at this point that's being used widely in production.

We should have better mix nets and improve on `Tor`.

But yeah, you're going to challenge that.

Walton: 00:33:03

`Nym` is a promising looking direction for something to really compete with `Tor` and bring a degree of robustness that's been hard.

Yes, it is.

I have made many, many criticisms over that decision to the team over the years, but it has been a stereotype promoting these things.

Calle: 00:33:26

Calle, you seem to be disagreeing with Alex that `Tor` is all we've got.

Michael: 00:33:31

I don't know why everyone is so bearish on `Tor`.

`Tor` is I think pretty cool.

I have other critic about `Tor` not the reliability the fact that it has centralized registry basically and that's a problem.

Then there is something like `Nym` that tries to solve that with a shitcoin instead of a centralized registry.

Which is also not an ideal solution obviously.

There's `I2P` which is also getting more and more popular also supported by `bitcoind` and generally the interest for mixnets seems to be growing.

We shouldn't forget that `Tor` was basically invented by the US secret military three-letter agencies and we're just their cover traffic at this point so they can hide in our masses.

But the fact that this network supports almost all of Bitcoin plus almost all of dissidents in the world and many more people that try to escape the Chinese firewalls, the Russian intranets, is simply amazing to me.

That this thing works is amazing, but I would agree that it hasn't much improved in the last decade or so.

I don't think that we're over-reliant on `Tor` at all.

It feels like we should use it more and try to improve it more.

If it's not `Tor`, then it should be one of these alternative systems.

But the idea that we can build a second layer on top of the internet that can hide our traffic, I think, is extremely valuable and will be something in the future that we will keep using for a long time.

Rita: 00:35:11

Can we help improve `Tor` by fixing some of the incentives with `Lightning` and `Cashu`?

Calle: 00:35:16

Right.

One of the things I think many of us appreciate is how network topologies change based on their incentives.

I don't know how many of you are familiar with `L-Tor`, a relatively new project, a guy out of Texas, trying to incentivize people to run `Tor` nodes and get paid.

Alex: 00:35:39

Yeah, it started as a Bitcoin++ hackathon project, actually.

Calle: 00:35:42

It did indeed, so.

Alex: 00:35:43

Really?

Wow.

Michael: 00:35:44

The `Tor` network is every now and then under attack, everyone probably knows that somehow.

Felt that with the `Lightning` node for example and `Tor` actually has implemented proof of work a couple versions ago to mitigate the issue.

I recently was told the story by one of the contributors there that this whole war started with darknet markets.

Two darknet markets waging war towards each other on the `Tor` network trying to take out the other darknet market to gain dominance there.

It wasn't probably a state sponsored attack, it's just literally drug dealers doing their thing.

Alex: 00:36:23

Just fighting on the internet.

Walton: 00:36:25

Be a normal person and go buy drugs from someone on the street.

Buying it on the internet is retarded.

Michael: 00:36:32

Not recommended.

What `Tor` then did is they took a look at Bitcoin and implemented proof of work in their protocol.

The rationality here is when they wage war on the `Tor` network, everything stops working.

It's strictly better to exclude a bunch of phones and JavaScript `Tor` clients that cannot compete with servers by imposing proof of work.

You as a `Tor` service, you can just say, now this is getting a bit too crazy.

I need proof of work for my packages now.

Then you kind of exclude 50% of the users, maybe, just making up that number.

But at least the other 50% gets to enjoy your service.

If you close the `Hashcash` loop again, it started with Adam Beck email spam, Satoshi looks at it puts it into a `sat` using proof-of-work, and then we start using `sats` again to mitigate spam.

I think this is a beautiful circle.

I think it's a great idea to use Bitcoin to help out these anonymous systems that clearly need some rate limiting.

But I think that `Lightning` is not the best way to do it.

The reason for that is that `Lightning` is great when it works, but it's really bad if it doesn't work.

For these systems you need something that just always works.

You're downloading a video and it works for 10 minutes and then an `HTLC` gets stuck and now you have to wait for two weeks until it settles.

Calle: 00:38:10

So what you're saying is you need offline payments and that maybe there's something in this ecosystem that provides that, is that right Calle?

Michael: 00:38:17

Yeah I can think of a few things.

Obviously an `ecash` payment will always work, but there are also other layered systems on top of Bitcoin that don't have this issue where you have timeouts basically, like `HTLCs` that need to timeout somehow in order to resolve a conflict.

Walton: 00:38:32

`Ark` could be an answer.

Alex: 00:38:33

Like `Ark`.

Michael: 00:38:34

Or `Fedi`, yeah.

Yes.

But with `Ark` is going to be a very centralized service.

We should not build the `Tor` network using `Ark`, I think.

Walton: 00:38:46

I think there's a deeper problem to confront here and I think just ideologically most of the people who contribute to `Tor` are not fans of capitalism, they're not fans of interjecting monetary aspects and incentives into systems like this.

Even if we can technologically figure out a way to deal with this problem, will the team be motivated to actually implement or integrate anything?

Or will they fight or resist that on ideological grounds?

Michael: 00:39:19

I wouldn't make a bad faith argument about that.

I think it's fairly reasonable to assume that you have a system that is supposed to serve everyone and then now you want to make it...

Calle: 00:39:29

Want to limit it to 40,000 people.

That's the number of Bitcoiners in the world.

Alex: 00:39:35

Exact number.

Calle: 00:39:37

Yeah, exactly.

I'm not sure you can put a price tag on everything.

First of all, there's differences in the world.

A US-American person and someone somewhere else are supposed to pay the same price for the service, one problem.

The other problem is not everyone has Bitcoin.

That's actually the biggest problem.

We could solve spam issues for so many systems out there using Bitcoin, but there are not enough Bitcoiners to make it worthwhile.

Shinobi: 00:40:08

Philosophically, it's also just a growing worry is that you have this paradox where the price has to be high enough to discourage spam traffic but it also has to be low enough that it really doesn't affect the user.

I'm terrified that those numbers are actually inverted where the price that's too high for spammers to overcome is actually higher than the amount that is gonna not affect the user experience.

I'm not so sure we really have a solution that will work at this scale.

Evan: 00:40:39

You're looking on the base layer?

Shinobi: 00:40:42

No, I mean anything.

Just anything that's paying to reduce spam.

Calle: 00:40:47

You want to send a message and how much is that going to cost you?

Let's say it's one cent, is it worth one cent for a message?

Maybe yes.

But is it worth $1 for 100 spam messages for a spammer?

Probably yes too.

So that's a good price.

Shinobi: 00:41:01

I can take you down.

Calle: 00:41:02

So yeah.

## Lightning Transaction Fees

Evan: 00:41:06

Is the current low fee environment evidence of little demand for Bitcoin transactions or is it evidence that `Lightning` is already scaling to meet the needs of its users?

Walton: 00:41:15

I think it's the latter.

I think clearly a large amount of transactional use has slowly shifted over the last few years onto the `Lightning` network.

That's just looking at the payment data from a number of companies who've integrated `Lightning`, just my anecdotal experience.

I almost never make an `on-chain` transaction for something these days anymore.

It's like this is what we were hoping for.

It's just kind of the question of how long is it going to take for Jevons paradox to play out in terms of using the resource that is block space more efficiently, driving that huge jump in demand for it.

A couple of us have said this up here, it's just not enough people own Bitcoin.

That is the core of almost every problem as far as the lack of transactional use.

Somebody needs to be able or wants to receive it.

The person paying them needs to have it to give it to them.

I think that just boils down to we are not very densely packed together geographically.

Everyone keeps fixating on these narratives or attempts to push people to use Bitcoin in meat space.

Like go buy your coffee or eat out at a restaurant or things like that with it, as opposed to trying to create digital economies, where that geographic density isn't a problem.

You're on the internet, you can pay or receive any digital good or service from anyone on the internet.

It doesn't matter where you are in the world.

I really think if we want to see that manifestation of Bitcoin as a means of exchange actually happen, we need to focus on where it's logical, which is the internet, not in person.

There's not enough of us in the same place to actually bootstrap that means of exchange.

Evan: 00:43:23

Do you want to repeat the question because I do think you answered it but you also were a little bit off there.

Is the current low fee environment evidence of little demand for Bitcoin transactions or evidence that `Lightning` is already scaling to meet the needs of its users?

Calle: 00:43:40

Both.

Can it be both?

Evan: 00:43:42

Sure.

Shinobi: 00:43:43

I think everybody not paying for their coffee `on-chain` is probably contributing to some degree.

Alex: 00:43:51

But did it happen to you that the `Lightning` transaction was costing a lot more than `on-chain` one?

Because it did happen to me several times.

Michael: 00:43:58

It happens all the time.

If the amount is high enough and you pay a percentage instead of a flat 30 cents, easy.

Alex: 00:44:05

So then why would people prefer `Lightning` when it's more expensive than `on-chain`?

Evan: 00:44:12

The immediate finality is important UX in a payment.

Alex: 00:44:16

Well, sometimes it's double, triple, quadruple more expensive.

Shinobi: 00:44:20

Are you talking about when you hit a channel open or just a normal payment?

Alex: 00:44:24

Sometimes a normal payment.

With a channel it's even more.

Walton: 00:44:27

When you have a really bad liquidity situation like some nodes.

Michael: 00:44:32

Come on.

Evan: 00:44:32

You're sending a few million `sats` you mean on `Lightning` rather than `on-chain`.

Shinobi: 00:44:36

You're getting abused if you're paying more for a `Lightning` payment that's not opening a channel.

Walton: 00:44:42

It's the strategy incentive of a routing node operator to maximize their revenue.

They are going to play games where they try to tactically arrange their channels or push fee rates in one direction or another to their benefit.

Shinobi: 00:44:56

Then you should use a different wallet.

Michael: 00:44:58

That's not a good thing.

Guys, seriously, an `on-chain` payment right now at 1 `sat` per `vB`(virtual byte) is how much?

50 `sats` or something?

You easily pay tens of thousands of `sats` for huge `Lightning` payments.

Easily.

Like this happens all the time.

Walton: 00:45:14

This is not some outrageous node basically robbing you with crazy outrageous fees, that's just the way it is right now.

Big `Lightning` payments you pay good money for them.

I think this narrative of `Lightning` being super cheap to use is just a huge mistake as a narrative in the exact same way that that narrative was crafted about `on-chain` transactions 10 years ago.

We can't make that promise.

This example of fluky things like this even when `on-chain` fee rates are non-existent, it's just an inherent consequence of the liquidity dynamics of how the network functions.

Project forward another 10 years, think of higher fee rates, a more mature fee market, at the end of the day, the fees that you pay on `Lightning` are going to have to recoup the `on-chain` costs that `Lightning` node operators experience, or the entire thing is economically unsustainable.

Making this promise that `Lightning` will always be cheap payments, it's just not reality.

We're doing the exact same thing we did 10 years ago when everybody just assumed we would increase the block size when we hit that limit and fees went up.

We're creating the exact same problem of laying these false expectations down and then when reality goes no, you're wrong, you're going to have a bunch of people who've plugged into this system, gotten used to using it, assuming it's gonna work like this forever, and then reality kicks in.

Shinobi: 00:47:01

The whole point of `Lightning` is that you have fixed upfront capital costs for an indefinite number of payments through that capital.

You deploy once and then you get to reuse it over and over again.

I think the mature version of `Lightning` will adhere to that strength.

If we're having to cover `on-chain` costs all the time and we're moving liquidity around, then that doesn't seem like a sustainable future state.

Walton: 00:47:26

Are we talking about the magical economy in the future where everybody receives exactly as much money as they pay constantly?

It's always going to have a directional push in one direction that has to be rebalanced.

Ultimately, you can delay it, you can play balancing games, but at the end of the day, when you've exhausted all of those options, you are going to have to interact with the base layer `on-chain` to deal with the consequences of that directional push.

Calle: 00:47:57

And pay your 30 cents.

For now.

Evan: 00:48:03

These seemingly competing ideas are even published in the Fidelity report on the `Lightning` network in partnership with Voltage.

Two key takeaways.

One of the key takeaways they said a well-optimized participant in the `Lightning` network can see transaction fees as low as 0% and payment completion times of less than half a second, but they also make one of the key takeaways that `Lightning` can be viewed as a yield-bearing network that does not require users to give up the control of their Bitcoin.

How can you have 0% fees and yield?

You can't have both, right?

Walton: 00:48:39

You have to look at that from two directions.

The fee the user is paying, and from that perspective.

But then also, what is a node operator actually receiving in terms of profit?

The fees can be very high from the user's perspective.

But if most of that is the node operator just recouping their cost of interacting `on-chain`, they're not actually making that much yield and profit.

Shinobi: 00:49:04

Yeah, I don't think it's a fair characterization.

I think the majority of the time that users are paying a lot is because they are using a wallet that has a `Lightning` node with one channel to somebody that's overcharging them because they can.

Walton: 00:49:16

I'm talking projecting out and higher people.

## Stablecoins and Lightning Network Growth

Evan: 00:49:19

All right, guys, well, enough on fees for a minute.

I have one further question, and then we have a couple more minutes for questions from the audience.

The growth of the `Lightning` network, and this is something that is difficult to measure, you don't know what the total transaction volume is, is gonna be driven by a number of different factors as we move forward.

How much of it is gonna be driven by things like `ecash` and `Ark` and other tools that are actually about Bitcoin versus how much of it is going to be driven by assets on `Lightning` and is this a real problem when we look at the `Lightning` network moving forward?

Does the growth come from a base that is increasingly prone to regulatory attack?

Walton: 00:50:25

Either way.

But I think looking at the reality on the ground, that the transactional use of things like stablecoins far exceeds people transacting natively with an asset like Bitcoin.

If we actually do see deployment and issuance of stablecoins on Bitcoin and see that link into the `Lightning` network as a settlement mechanism, that probably will be the primary driver of any growth or revenue increases for node operators on `Lightning`.

Alex: 00:51:01

Like stable channels?

Walton: 00:51:02

I don't know.

Evan: 00:51:03

Shout out Tony, let's go.

Walton: 00:51:05

Yes, I would prefer if it was stable channels, but I think the reality is it's going to be things like tether tokens issued and then just having the channel do the atomic swap between some service provider to forward the payment in Bitcoin.

Shinobi: 00:51:22

Everybody and their mother is starting a new stablecoin protocol for the record.

Rita: 00:51:26

Yeah.

Shinobi: 00:51:26

Seems like every week there's a new one.

Evan: 00:51:27

If you would like to start your own stablecoin thing, I think you should go to Tether for funding, right?

Shinobi: 00:51:33

I'm curious to hear from Calle.

Michael: 00:51:35

How much do you think about the regulatory burden that mint operators in the future will have to bear?

No comment.

The one thing I'm not exactly sold on yet is when you have these stable coins on Bitcoin, why would you want to have them and use them on Bitcoin in the first place?

Alex: 00:51:56

Tether is going to do an `RGB`.

Michael: 00:51:57

Yeah but why wouldn't you use the tether chain, the plasma thing?

What's the advantage of using it over `Lightning` with all its intrinsic downsides?

Evan: 00:52:05

My skin's crawling right now, I have no idea.

I'm not the person to answer that.

Alex: 00:52:09

You're asking the wrong person.

Walton: 00:52:12

I think this is very much an example of a solution looking for a problem.

A stablecoin is centralized at the end of the day, it's worthless the instant the issuer won't redeem your coins or starts playing funny games.

Whether it's on an SQL database like something like Solana or the Bitcoin blockchain it's utterly completely irrelevant.

Exactly, why do we need a permissionless network to transfer around IOU tokens of someone's bank account?

Charitably I think the only straw man you could make is if you look at things like `RGB` or taproot assets, you can make the argument that how those protocols are structured technologically, it would make it a lot more difficult to do things like have the selective ability to freeze or seize a specific users coins, because this is all client side data, none of it's explicitly recorded `on-chain`.

But again, there's no reason you can't architect systems like that that provide privacy in a similar way that don't connect to Bitcoin at all.

Michael: 00:53:26

Yeah, I'd love to be proven wrong.

I'm just entirely sold on the concept of stablecoins driving `Lightning` that macro fiat.

Shinobi: 00:53:33

I mean, there's huge demand for dollars around the world.

Places that don't have access to dollars want dollars.

Calle: 00:53:39

Yeah but why `Lightning`?

Sounds retarded.

Alex: 00:53:43

And a huge amount of people who don't want volatility.

Shinobi: 00:53:47

Yeah but it's not the dollars.

Calle: 00:53:48

I think generally the stable coins, I see two reasons.

First shit coining, that's one thing that drives it, printing money is fun for some people.

Secondly is people don't like to control their infrastructure so it gives them a better time in front of court when you can say I don't control Tron.

I can't control whether this person sends my assets to that person because it's all on this public infrastructure.

That's also one reason why people want to build on something like Bitcoin, but they could also just take one of the other kind of a phantom, decentralized systems where you can just throw your hands up and say I didn't know about this eventually.

But I agree that it's a huge larp because as long as you can freeze these assets with a click of a button, then it becomes a clown show.

Shinobi: 00:54:43

So that big dollars are cooler because you don't freeze them, you just get exposure to them.

## Audience Q&A

Evan: 00:54:52

Let's hear some questions from the audience.

Before we wrap up this panel.

Calle: 00:55:02

People are speechless.

Evan: 00:55:05

They should have enough of Shinobi talking, maybe.

[Audience]: 00:55:07

So, comment and a question.

First off, I'll say that report was not the Fidelity report.

Evan: 00:55:11

It was in partnership with Voltage, my bad.

[Audience]: 00:55:14

Fidelity Digital Assets in partnership with Voltage.

I had a question.

I was at a Presidio Bitcoin for Bitcoin Design Week last week, and Christoph Ono from the design community had an interesting idea.

He's been really drilling into the fees problem lately and exactly what you all have been talking about, about unexpected fees that pop up whether it's `on-chain` or larger than normal `Lightning` payments.

He kind of did this analysis of remittance companies, not Bitcoin, like remittance companies, and just found that their advertising just goes hard on fees.

Gigantic letters saying we are the lowest, we save you so much on fees, we're 0.1% fees.

That's all they do is just go hard on their low fees and then you look at all the Bitcoin products and they're always like we're a simple wallet with low fees.

It's just really kind of passive and weak.

He was trying to think, could there be a company that you prepay for some kind of plan and your fees are kind of kept under control with your `Lightning` service provider.

Not sure how it would work on a technical level, but I'd just be curious, any thoughts, is that the sort of thing an `LSP` could implement?

Walton: 00:56:24

I don't see any way you could do that without hedging and creating some kind of derivative product where you could actually find a counterparty willing to trade against your fee expectation.

Shinobi: 00:56:37

Can we hear from the guy that runs an `LSP`?

Evan: 00:56:39

Yeah that's literally my thought.

The universe sent it like Evan come on.

There's some ways but I'm not sure people would want to accept all the trade-offs.

Either you're shifting risk around, you don't necessarily have to turn into a derivative, even though that'd be the sexy way to do it.

Or you introduce more components of trust to help the cost down.

There's countless ways to do it.

We already have a subscription service, `Zeus` Pay Plus, that gives you a discount on `LSP` services.

You could definitely fix costs in various ways.

I think the whole space in terms of these service providers is just getting started and is gonna mature by leaps and bounds in the coming years.

Calle: 00:57:28

I think fees aren't a problem.

Unpopular opinion, but who cares about 100 `sats` fees or 200 `sats` fees or 0.2% fees or 0.5% fees.

Our competition is literally trash.

I don't think that anyone said I won't use Bitcoin because the fees are too high.

This is an intermediate episodes where four megas hit the chain every ten minutes or something, then we get into those problems.

But to me, this feels like incredible technology.

I'm happy to pay fees for using Bitcoin.

I kind of assume that it's the same for everyone here.

So maybe this is just a non-argument.

Evan: 00:58:11

Maybe this is something that really doesn't affect too many people.

Honestly the bar is so low we don't have to be perfect.

We don't have to have zero fees.

We just have to be better than the incumbents.

Then you have people like the Steak 'n Shake COO going out and saying, hey guys, we implemented Bitcoin, it cut our processing costs in half.

That's huge.

That's all we need.

We just need to be twice as good as what exists now.

Michael: 00:58:37

In all fairness though, Steak 'n Shake was a receiver of `Lightning` payments and the sender pays the fees.

So, er.

Alex: 00:58:45

In a wallet UI, in cases if `Lightning` fees are too high, it would be great if the UI can kind of detect it and maybe give you alternate ways how to send Bitcoin at this exact moment.

Maybe use some other tool.

Calle: 00:58:59

Maybe you could use...

Walton: 00:58:59

You could use `Cashu`.

Alex: 00:59:01

Or `Cashu` or some `RGB` coin conversion or whatever the hell else.

Because this would help users to see that this is an unreasonably high amount right now to send, and if they don't want to send `on-chain` and wait 10 minutes they would have this this and that alternative.

Walton: 00:59:18

Right.

Have a price breakdown across the different layers.

Alex: 00:59:21

Maybe.

Shinobi: 00:59:22

Unified QR codes help.

Walton: 00:59:26

Definitely.

Shinobi: 00:59:26

`On-chain` and `BOLT 12`.

Evan: 00:59:31

QR code.

Shinobi: 00:59:34

You need to be able to decide which payment rail you're going to use.

You want to scan once and then have the best option to be chosen for you in the best case without having to have a PhD in Bitcoin.

Alex: 00:59:47

Yeah, or simplify it to bare minimum.

Michael: 00:59:54

I have a question.

There's a really cool `Zeus` hackathon prize, which the goal is to enable discovering of trusted mints in `Zeus`.

Evan knows about [cashumints.space](https://cashumints.space), but in [cashu.me](https://cashu.me), Calle, there's a very cool feature called Discover Mint.

I've been told that there's something called Know Your Mint.

My question is, can you explain Know Your Mint to Evan?

And how it searches `Nostr` for recommendations for `Cashu` mints?

Shinobi: 01:00:48

Well, I would run into the risk of repeating, not myself, but someone has actually done that after his talk.

So, thank you for your question, but you should have watched his talk.

Evan: 01:01:00

Education happens incredibly fast here at Bitcoin++ and this was the scaling `Lightning` panel.

I think the way we scale `Lightning` is by having more and more Bitcoin++'s.

So I'd like to firstly thank all of you audience that came to this panel.

Bitcoin++ and panel discussions wouldn't be the same without all of you, but also please give a round of applause for my panel Alex, Calle, Shinobi, Evan, Michael from `Boltz` and Rita.

Walton: 01:01:30

I'm Walton.

Shinobi: 01:01:30

Thank you very much.

[Outro Video]: 01:01:45

Alive, unstoppable, through rain and shadows we run.

Forged by fire, forged by freedom.

Because now, the current is ours.

Bitcoin++ Berlin.
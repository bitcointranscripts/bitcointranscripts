---
title: Lightning Privacy & Splice Panel
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=SjLPbjs9LkI
tags:
  - splicing
  - rv-routing
  - offers
  - privacy-enhancements
speakers:
  - NVK
  - Bastien Teinturier
  - Jeff Czyz
  - Dusty Dettmer
  - Tony Giorgio
  - Vivek
date: 2023-05-12
---
## Housekeeping

Speaker 0: 00:01:17

Today we're going to be talking about Lightning privacy, splicing and other very cool things with an absolute amazing panel here.
Just before that, I have a couple of things that I want to set out some updates.
So OpenSats is now taking grants for a Bitcoin application, sorry, taking grant applications for Bitcoin projects and Nostra projects and Lightning projects.
And there is about five mil for an OSTER, five mil for Bitcoin.
So do apply.
I joined as a board member and Gigi joined as the Ops person and we're gonna get those SATs flying.
So let's get that funding going.
The other thing is for cold card users, we have merged Taproot and BSMS with that.
So expect a separate edge release.

## Guest introductions

Speaker 0: 00:02:14

And we'll go with that.
So without further ado, guys, I have some awesome guests here.
Let's start with some intros.
Jeff, welcome back.

Speaker 1: 00:02:25

Hey, how's it going?
So yeah, my name is Jeff.
I am a developer at Spiral.
I've been working in the Bitcoin space for about four years now.
And my current project is the Lightning Development Kit implementation of Lightning.
It's more like a SDK.

Speaker 0: 00:02:41

Awesome.
Tony, pickle Tony.
Hey guys, this

Speaker 5: 00:02:45

is Tony.
Lightning dev, one of the co-founders of Mutiny with Ben and Paul Miller.
Yeah, I've been talking about lighting privacy for a while, so looking forward to this.

Speaker 0: 00:02:55

Very cool.
T-Bast.

Speaker 6: 00:02:58

Hey, I'm T-Bast.
I've been working at Async on the lighting specification and our implementation Eclair and also our Phoenix wallet.
And I've done a lot of things around lighting privacy as well, like blinded paths.
So excited to be talking about that here.

Speaker 0: 00:03:14

Yeah, we did an episode, the lightning panel, episode 15.
So for people interested on this, they should definitely go check out that episode.
Dusty Damon.

Speaker 4: 00:03:24

Hey, what's up?
Dusty Damon.
Not that it matters.

Speaker 0: 00:03:30

I know.
I, you know, it's people haven't settled if it's like demon or Damon for, for the demons.

Speaker 4: 00:03:37

It's like proven work.
If you can like, you know, pronounce Damon, then you can find me on Twitter and also spell it.
So good luck with that.

Speaker 0: 00:03:47

And so Dusty, what do you do?

Speaker 4: 00:03:49

I'm an independent Lightning Protocol Engineer.
I've been working on splicing for the last, God, like two years now.

Speaker 0: 00:03:55

So does that mean we ship?

Speaker 4: 00:03:57

Shipping, like right now.
Me and Team Best, we got to get Interop going soon.
Soon.

Speaker 0: 00:04:04

Two weeks?

Speaker 4: 00:04:05

Two weeks.

Speaker 0: 00:04:06

OK.
And Vivek, Seared Salmon, welcome back.

Speaker 3: 00:04:12

Thank you.
Just, you know, VP of BD at CoinKite and recovering Greenlight and CLN shoe.

Speaker 0: 00:04:22

Nice to have you, sir.
So props to Vivek for putting this panel episode together.

## Current state of LN privacy

Speaker 0: 00:04:29

It's kind of cool.
So guys, where do we start here?
This is a hairy long, big topic.
So, so, so how about, why don't we sort of like maybe cover a bit of a primer on, on the state of things, right?
Like Where are we in Lightning in terms of like things that are privacy related that are either just shipped or about to ship?
Let's not talk about things that are going to come in sort of like, you know, months from now still.
Like just right now, what's going on?
Who wants to take that?
Go ahead, T-Best.

Speaker 6: 00:05:05

So basically I'd say that why once you are inside Lightning, sender privacy is good, receiver privacy is not.
When you are interacting with the chain, like opening channels or everything you do on chain, privacy is not great.
So that's an easy way of summarizing all the things where you have or don't have privacy.
And for all of those, we have things in the works.
Some of them are coming sooner than others, but there's still a lot to do if we want privacy to be better on across the whole board.

## Receiver privacy

Speaker 0: 00:05:41

Okay.
So, so like if you want to get a little bit more like, like detailed on this, like, you know, why is it that receiver privacy is bad right now?

Speaker 6: 00:05:51

Receiver privacy is bad for many reasons.
First of all, if you when you receive a payment at the cryptographic level, because of onion rounding, the guy just before you shouldn't be able to infer that you are the final recipient.
But if you're not careful about adding CLTV expiry deltas on top of the current block height, it's actually very easy to infer that the next guy is actually the recipient.
Also when you are using unannounced channels, oh actually this has become better.
A few months before when you are using unannounced channels, oh, actually this has become better.
A few months before when you were using unannounced channels, your invoices were leaking your unannounced channels all across everywhere because people just pasted invoices directly on Twitter.
And once you've doxed your channel, you've doxed it forever, or you have to pay on-chain fees to open a new one.
And this has become better since we introduced a CID aliases, which as you give an alias to a channel, which is much better, but it doesn't hide the public key of a recipient.
And this is getting much better with Blended Path.
With Blended Path, you're finally getting good privacy with some trade-offs on potential usability.

## Blinded paths

Speaker 0: 00:06:59

How do Blended Paths work?

Speaker 6: 00:07:01

Okay, so Blended Paths are if you, I guess everyone has a vague idea of how rendezvous routing works in Onion, in Onion networks, where the receiver, when you want to receive a message, instead of directly giving your address or your Node ID, you find paths to yourself that take a few hops to reach you.
You encrypt those and you just tell people get to that introduction point and they will know how to reach me with this encrypted blob that I'm giving you.
So people who are sending payments to you only learn the identity of a few introduction points that you chose on the network so you can choose them however you want to make sure that people cannot infer that then you are the recipient.
So algorithmically speaking and in order to be able to receive, to make the most of your incoming liquidity.
This isn't trivial to correctly choose your blinded paths.
And that's something that we are experimenting with a lot.
And there's a lot of cool stuff to do to make sure that this doesn't impact usability too much.
But in theory, once you're able to choose routes that still allow you to have enough income and liquidity, you're able to make people enter a route towards you far away from you or at least in different places in the network so that they just have no way of figuring out what node ID you are.
And it's even better if you are a wallet user that doesn't have any public announced channel because then no one should see your node ID anywhere.
You have no reason to advertise anything.

Speaker 5: 00:08:32

Yeah, there's almost like a little bit of a...
With raw network routing, you hinted at it, but who you select as your introductory nodes is important too.
Like, if you're the only person that keeps selecting the same introductory nodes, you can kind of do some analysis there and kind of guess that, okay, that's the same person.
So yeah, are you guys, you know, I'm not, I'm just like a lightning protocol LARP.
Like I never touch protocol code.
I'm just like right above it, like you know, fine grain analyzing it.
But are you guys like taking into consideration like how you actually select which introductory node for the users to maintain their privacy?

Speaker 6: 00:09:18

Yeah, sure.
That's something we are working on.
At first, I thought that the hard part was coming out with a cryptography to protect that, but then it's only just the first step, actually.
Just like doing onion routing and saying, oh, Intel, we are using onion routing, so everything is private, was only the first step and it's just not enough.
It's the same here.
Doing the cryptography at the cryptographic level, everything works, but you need to make sure that some other metadata doesn't leak your identity and choosing your routes correctly, changing your routes, but not too often.
There are a lot of ways the way you choose your blinded paths can expose who your node is.
So this is really far from easy.
It really needs a lot more research and a lot more experimentation because we can say we have a good algorithm, this works correctly.
But there are cases where it's much easier.
For example, if you are a mobile wallet using a few LSPs, it's much easier to choose your introduction point.
You could just use one of your LSP as the introduction point, another LSP that you are not connected to, but you know that LSPs are correctly, have good connectivity between themselves as another introduction point.
And since your node ID is completely private, there's a, this is a good way of getting good privacy without sacrificing incoming liquidity that much.
But in the general case for normal public nodes that have a lot of channels on the network, this is much harder.
And this is this is where we have a lot of fun things to do algorithmically speaking in graph analysis to make sure we are able to score the privacy of a blinded path and it's really non-trivial but it's going to be a lot of fun to explore.

Speaker 5: 00:10:58

One of the things there though is at least the blinded paths are supposed to go over the Onion messaging protocol, right?
The Bolt 12 Onion spec.
So at least it's only being leaked to the sender and not the whole world.
I believe, I could be wrong, even if you post a Bolt 12 invoice on the internet, sure, other people can try to query it at least, but once that invoice is expired, some may not expire, but once the invoice is expired, no one will see your routes again, right?

Speaker 6: 00:11:31

Yeah, but there are potentially issues as well, because someone's sending you an invoice request of an unknown message to get an invoice with blinded paths.
If you refresh and change your blinded paths too often to change the introduction points you select, that guy can just make it look like they just failed to use the previous blinded path because of a liquidity issue somewhere in the network.
So you're giving them new blinded paths.
But every time you give them a new blinded path with a new introduction point, potentially that helps them triangulate in some way what your node ID is.
So you need to protect from that and make sure you don't give out too many different blinded paths to users but you don't really have a very easy way to throttle those.
So those are open questions which honestly we haven't had time to completely thoroughly look at, but we know there are potentially a lot of issues there and we need to spend a lot of time researching them and figuring out how to best protect against that.

Speaker 0: 00:12:29

Dusty, Do you want to jump in?

## Obscurity of lightning

Speaker 4: 00:12:31

Yeah, I mean, like the privacy on Lightning is a big, complex subject.
I think like there's a lot of details you can get into talking about, but at a high level like today, I think maybe a part of this is just the obscurity of Lightning.
I think that Lightning is quite private.
It looks like probably about a year and change ago, year to year, two years ago, there was a guy who was just using Lightning as a coin join service to clean stuff.
There was this activity where people were opening channels to big nodes, moving all liquidity into the Lightning Network and then just not even closing the channels, just abandoning them.
And it looked like people were just using it to wash Bitcoin, right?
So I think that we have evidence in the wild that people have been using Lightning to do very private stuff.
But obviously, there's more we can do.
I think like blinded paths, PTLCs, stuff on the horizon.
I'm not trying to talk about horizon stuff, but there is stuff on the horizon to make things a lot better.
I just think it's, I just like to say, like, there's hope.
I think Lightning's already in a pretty good privacy spot.
And I think that it can be a little, when people hear the complex, like, discussion, more private, what we're really doing is like, in my mind, I'm like, we got like 90%, we're going to last 10%.
Like, don't be scared.

## Onchain privacy compared to lightning privacy

Speaker 0: 00:13:47

So if you had to sort of like do a comparison, right, between like base layer transactions that we have right now, you know, to Lightning, I mean, it's, you know, especially if you're running on Lightning Node, I mean, you know, you can't, it's incomparable the kind of privacy you'll get for free just by using Lightning.
Like, as is, in the worst possible sort of like solution out there.
Unless you're using like a custodial sort of like KYC Lightning solution, right?
But you still get more privacy.
It's just that they know your stuff, but the other side doesn't know your

Speaker 6: 00:14:21

stuff.
100%.

Speaker 3: 00:14:21

It's information asymmetry, exactly.
It's not on-chain forever, but now specifically your wallet of Satoshi knows exactly those details.

Speaker 0: 00:14:31

That's right.

Speaker 4: 00:14:32

It's like a fundamentally different privacy question, right?
Like on chain, it's like, everyone can see the ledger.
How do you hide yourself in plain sight?
Lightning is like only your peers that you touch along the channel have any access at all to your transaction, right?
So like if those peers are the government, okay, yeah, they're gonna be able to track you.
But at its current state, knock on wood, the government's not running a lot of lightning nodes, right?

Speaker 5: 00:14:56

Well, so I think the concern, I mean, I agree with all that, the history and everything, but if there are big aggregators on the network already collecting this information forever and then selling it to third parties, then like that, You could say that doesn't last forever, but I mean it lasts as long as that company is, you know, lasts or that organization lasts.
So, you know, I wouldn't say like, you know, we're safe yet.
I mean, there are chain analysis companies looking at Lightning.

Speaker 0: 00:15:29

But personally, just I'll say just assume it's being captured.
I mean, like that's the best way of looking at this.
But even then, I mean, like the privacy leaking graph is still pretty shallow, right?
It's not like on chain stuff.
Like you still have like a much better privacy set.
Let's put it this way on Lightning, right?
I mean, if I am using my, you know, my Breeze or my Phoenix wallets, which is like, you know, just kind of like not fully custodial, but also not like your own node, It's kind of like in the middle there.
And I'm paying for a beer at the Bitcoin park.
Right.
And they're using their whatever, like BTC pay server there.
You know, unless somebody is really, really trying to get me, the chances of anybody seeing that that's what happened are pretty much lower than if I was using on-chain transactions, right?

Speaker 3: 00:16:21

I don't know if it's much lower, but I'd say it's lower.
And there's definitely aggregators like Tony was saying, and that's always been the concern.
I remember when Ellen Big showed up, everyone was like, oh, these guys are the feds or there's some other agency.
But you know, you just kinda, you're happy to get that inbound liquidity at the end of the day.
I actually want to go higher level and just get our principles first, fundamentals established for the Lightning Network, the challenges for the privacy.
I think I've heard T-Best and Tony explain it for those who haven't checked out their contributions, You should definitely check it out.
T-Best has an amazing chapter in the Mastering Lightning book, which I recommend nonstop.
And then Tony just sprung onto the scene, I think in 2021 with a massive privacy article describing issues with payment hashes, hash correlation, long paths.
So from a high level approach, T-Bass, can you explain how, I guess, is it Bolt1 or something, the init messages with noisexk, basically how the sender is always unknown and the receiver used to be known and the challenges with that in regards to unannounced channels which were mistakenly called private channels back in the day.

Speaker 6: 00:17:51

Okay, so I'm not sure I'm going to be exactly answering your question, but I think it will encompass what you'd like.
Our goal with Lightning, once you are inside Lightning and sending Lightning payments, our goal is that any node that is in the route can only infer who a previous node was and who the next node was, and nothing more than that.
Because that's something we cannot avoid.
That's how they receive a message from someone so they know that it came from that direction and they're sending a message to someone so they know it's going that other direction.
But we want to remove anything else they could use to track you.
So right now, we're using the same payment hash across the whole route, which is an issue.
PTLCs will fix that.
That also means that the sender, for example, should not be able to infer who the recipient is based on only potentially an invoice.
The issue right now is that in the Bolt11 invoice, that when it doesn't yet support SCID aliases, is that you are leaking both your node ID, which you don't actually really have to, but it's a bit inconvenient to hide it with Bolt11 currently, and exactly the channels that tell people how to reach you and who you are connected to.
So this part is more about the intersection between Lightning and Unchain.
And that's where we really need to distinguish the privacy challenges once you are purely off-chain and the privacy challenges when intersecting between on-chain and off-chain.
Because the way we fix each of those are really different.
They are completely orthogonal and operating at different layers of the stack and require very different solutions.
And to be honest, I think that we have good ideas on how to somewhat easily fix at the protocol level.
Almost everything that happens once you are in Lightning and sending payments, it's much harder to find changes that are only at the protocol level and that will fix the potential privacy leaks when you are doing on-chain to off-chain stuff.
Does that answer what you wanted or is there still something that I missed?

## Lightning privacy challenges

Speaker 3: 00:19:57

No, that's pretty good.
I just mainly wanted to touch on exactly what you said, how we're kind of piggybacking off of all the on-chain activity, with the SCIDs. And maybe I can ask Tony about, you know, the alias change that happened for XerioConf and Maybe some goodness there.

Speaker 5: 00:20:16

Yeah, I mean, that was huge.
I know my article, abytesjourney.com slash lightning privacy, I can put it in the show notes.
I wrote that in like 2011, and I get asked every now and

Speaker 3: 00:20:29

then.
2021.

Speaker 5: 00:20:30

Or sorry, 2021.
Yeah.

Speaker 4: 00:20:33

Read lightning security papers in 2011.
Yeah.

Speaker 5: 00:20:38

I wrote that and people sometimes ask me, okay, well, it's 2023 now.
Can we get an update?
I'm like, yeah, nothing changed, Except for SCID aliases.
So the aspect of trying to de-link the on-chain UTXO that was used in the invoice, you know, and T-BAS described that earlier, like that's huge.
Other than that, yes, we will get route blinding soon, like really soon, I'm super pumped for that.
Yeah, there's still challenges to be made.
But besides that, nothing's really changed in the last few years.
I will say, though, on the sender privacy side, It's not always going to be as easy as senders have good privacy all the time.
There's edge cases where that breaks down, and I think it's important to express when it breaks down.
It really breaks down when two users are sharing the same LSP.
The two mobile users sharing the same LSP.
If they both have unannounced channels with the LSP, there's no multiple hops that it's going through.
It's basically sender, LSP, receiver, and no one could have made that, no one could have gone through those hops besides the sender to the receiver.
So the LSP does see that.

## PTLCs

Speaker 6: 00:21:57

With PTLC that changes though, because with PTLC the sender can force the payment to go outside before coming back to the LSP and getting to the final destination.
And that's something that the recipient can do.
When they're using a blinded path, they can force the blinded path to start at another point than their LSP to make sure that even if someone is using the same LSP, they're first kind of going out of that whole garden and then coming back in, which when you are using the same payment hash doesn't do anything.
But when you are using PTLCs, could be useful, Even though you could still correlate with timing, amounts, CLTVs, when you have enough volume, when you start fuzzing those amounts, which is hard to evaluate how much it does work.
But I think there are ways to make it better, to at least make it not completely terrible.

## Routing and LSPs

Speaker 1: 00:22:49

Tibias, would you say then that like for that scenario, the LSP wouldn't be the introduction point on the blinded route?
And if so, how would a mobile user choose a different introductory point?

Speaker 6: 00:23:02

Either the mobile user just syncs a local neighborhood, for example, every node that is two hubs away from them, if they're only connected to one LSP, they cannot just sync it from that LSP if they don't trust that LSP because the LSP will just filter out everything else.
But if they are connecting to a few LSPs, they could just sync their local neighborhood and make sure that they make payment bounce between LSPs because in your blinded path, you can force the payment to bounce from one LSP to the other if you're using PTLCs from a list of LSPs. Or you can just even assume that without even knowledge of a graph, you can assume that some big nodes have good connectivity and benefit from their user base.
If I'm a Phoenix user, but I make all my payments go through the Breeze node, people will potentially assume that I'm a Breeze user, while I'm not.
Maybe they will assume I'm a Phoenix user that is doing that trick, but maybe Breeze is doing the same thing with other nodes.
This is where privacy is just evaluated in terms of how big is the crowd you're hiding in and other things that could leak some of your privacy.
But I think there are things that we can explore here that can make it potentially good enough once we have enough volume and a large enough number of different LSPs that offer that kind of services.

## Gossip filters

Speaker 1: 00:24:20

Would that mobile client then, in order to do this sort of local sync of the gossip, which is maybe, I guess, it's preferable for a mobile user, Gossip is pretty expensive as far as network bandwidth and downloading it all.
Does that require then like a sort of custom implementation for the mobile wall to do that sort of local sync?
Now in the LDK side we have like this rapid gossip sync which makes it pretty quick.

Speaker 6: 00:24:46

And the other idea is in the very old trampoline PRs I had like three years ago, there was a proposal to do gossip filters that would be applied that you ask your peers to apply some gossip filters so that they forward to you only a subset of the gossip that interests you, so that mobile wallets can get a fraction of the gossip that they're interested in without wasting too much bandwidth.
But this is still waiting for people to play with Trampoline before we do something like that.
And this will have to be reevaluated to see if it really makes sense compared to something like rapid gossip syncs or other ways of syncing subparts of the graph.
But I think that there's a large design space here to do it in a lot of different ways that could help

Speaker 4: 00:25:30

your practice.
Oh man, it sounds like you're bringing Bloom filters back.
I love it.

## Gossip and BOLT7 summary

Speaker 3: 00:25:36

Jeff, can you summarize what is Bolt 7 and Gossip and this graph that we always talk about?

Speaker 1: 00:25:43

Yeah, so this kind of actually touches on privacy a bit too.
So, and others here probably could do a better explanation, but I'll try my best here.
So, when you are constructing a path to make a payment, you need to know, I guess, the state of the network to route that payment from the center of the recipient.
And the Lightning Network protocol specifies a way to gossip basically node announcements and channel announcements.
And that allows you to kind of like the node announcements being sort of the, I guess, the nodes of the network and the channel announcements being the edges.
And that's a, I guess, something that you're essentially doxing your UTXOs that way because that's how the channels are identified.
And anyone that has access to the blockchain could see what your balance is.
So the act of gossiping currently in Bolt7 is not very privacy preserving.
Now I think there are some proposals out there, one for zero knowledge proofs to be used for this.
So you kind of say, I have some on-chain balance.
I'm not going to say how much exactly it is, but I can at least prove to you that I do.

Speaker 0: 00:26:51

It's like a range proof kind of thing?

Speaker 1: 00:26:53

I believe so.
I don't know the exact details honestly, but that's essentially the idea.

Speaker 3: 00:26:59

This is a Rusty's idea for the ownership proof or something like that?

Speaker 1: 00:27:04

I'm not sure if it's the same, but there are a few proposals out there.
There's like Gossip 1.5, which I believe that might be you're referring to.
But I could be mistaken there.
Someone else could correct me.
And then there's more of a long-term gossip B2 where we want to maybe be a little more privacy preserving than that proposal would allow.
I don't know if anyone else wants to jump in on that, probably a little more details.

## Speed of development

Speaker 0: 00:27:27

T-Best, you wanted to bring up something about the features that are sort of slow to?

Speaker 6: 00:27:33

Yeah, just quickly and I think it's a general comment about how things are added to Lightning nowadays.
A lot of the features that we are finally shipping now have been discussed for years.
A lot of them and a lot of things we are discussing, people get excited about it, but they're not gonna be really shipped before years.
And it looks like some of the things are very slow to arrive on Lightning, but That's really because we've already done all the easy stuff.
It was much easier to ship things faster before because they were the MVP, they were the easy things to ship.
The things we are doing now are really much more complex than what we did before.
We also have the whole ecosystem that we need to move whenever we do something, a whole ecosystem that has to follow and actually use those features.
So our goal, there are a lot of things that really need to be done at the protocol level and will take a long time to ship.
For example, blended paths, placing and the interactive transaction protocol that's underneath it, liquidity ads, that kind of stuff.
But the goal is that what we are trying to add right now are big building blocks that can then let people build new stuff, build cool stuff without too many protocol changes.
This really lets other people build on top things that are still quite low level.
Things like, for example, maybe we'll tell you, we're going to eat afterwards, things like LN Vortex, that kind of stuff, are much easier to build with the protocol changes that we are creating now.
We're creating more flexibility, growing the design space for people who are building on top of a lighting implementation to actually be able to do something about privacy, for example, to do something about a lot of low level aspects of Lightning.

## Lightning implementations and compatability

Speaker 0: 00:29:22

Yeah, so like, but what's like the dynamic on Bitcoin base layer, it's always been, you know, the issue is we always need backwards compatibility but you know, realistically speaking, we have one client, right?
Like for Bitcoin, there's reference client.
It has 999% of market share.
And it kind of needs to be that way, you know, especially on how Satoshi wrote it.
You know, there is no spec for the protocol.
The spec is the client and things are like, they get complex and they break very easy if you start messing around.
So essentially when you wanna make a big change on Bitcoin, right?
Like the main thing is like, okay, great.
Is it backwards compatible is the first thing, right?
And how can we sort of like, you know, shove it into something like adapter signatures or like you always have to shove into something else, right?
Because you can't change most of the things to keep backwards compatible.
Now, on Lightning is different, right?
You guys have the privilege of being able to break things.
Now, how do you find a dynamic between the major node implementations, right?
And sort of like this idea of like, okay, we are ready to push this because we coded this faster, right?
Like whatever is the feature.
And, you know, maybe the other two implementations are busy on something else because they have different priorities.
And like, how do you guys manage all this dynamic?
And like, at what point do you say like, fuck it, I'm just gonna ship it.
And if they wanna have it, great.
If they don't, then they don't get to use this feature.
Like, how does this play out?
Because, you know, I have Jeff here who does LDK, which is a growing, very like fastly growing implementation and is going to have a node soon.
And then we have Async, right, which is a clear, I always get confused with like all the names.
And then we have, unfortunately, LND is not represented here.

Speaker 3: 00:31:18

So Tony's a fair representation of LND and LDK because of his experience as an app dev.
And Dusty is like a stand in CLN contributor.
So there

Speaker 0: 00:31:26

you go.

Speaker 3: 00:31:27

It's a fair, fair representation.

Speaker 2: 00:31:30

So

Speaker 0: 00:31:30

should I just give a knife to everyone and see whoever comes

Speaker 2: 00:31:33

out of

Speaker 0: 00:31:33

the room gets to pick the next feature?

Speaker 3: 00:31:35

No, no knives, Moonrakers.

## BOLT12

Speaker 1: 00:31:38

There's definitely a temptation to sort of move fast like that.
And it's, you know, You have to resist in some respects.
So like for Bolt 12, for instance, people have wanted Bolt 12 for a long time.

Speaker 0: 00:31:50

Oh, I've been hearing as a unicorn feature that one day is going to happen.

Speaker 1: 00:31:54

One day, one day.
So we are really close actually now.
But the point I wanted to make...
Two weeks?
Two weeks, Two months maybe.
The point I wanted to make around that is that, C lightning or core lightning, I guess, had an implementation of Bolt 12 pretty early since Rusty was the proposer of Bolt 12, But the spec changed quite a bit over the year plus it was when he first offered the proposal.
And now where it's like pretty much ready to very close to being merged.
And without feedback from other implementations, you're going to get a lot of churn later on if you really try to like, you know, push maybe an operability between two implementations early, get it out.
So for instance, in Bull 12, there was a few changes that were made.
Like, so one, there's a certain sequence of offer, invoice request, invoice in Bolt 12.
And the information from those, that chain of messages is sort of important if you want to do stateless verification of invoices and invoice requests.
So having that data inside of like, so say having the offer fields inside invoice requests and those fields as well inside the invoice was a change that was made that made this very easy for us to do.
And it allowed for scaling a node that uses Bolt 12.
That's just one example.

Speaker 4: 00:33:16

So basically I think what you're saying, I agree with, is that you almost want to interact with the other implementators early.
Right.
Like last year, I was working on splicing kind of all alone and I was like, hey, guys, I

Speaker 0: 00:33:28

have these ideas for the spec.
Any thoughts?
And there was a whole

Speaker 4: 00:33:31

lot of crickets, right?
And now everybody's doing splicing and they have opinions on how to change the spec, right?
So I'm literally in the process of rewriting things for those new changes, just like Jim was talking about.
So I don't think it's...

Speaker 0: 00:33:43

That's when the bike shedding begins.

Speaker 4: 00:33:45

Yes, exactly.

Speaker 1: 00:33:48

I remember listening to your talk at Bitcoin++ last year on splicing and now a year later, it's getting a lot of traction now, but there's a lot of movement too.
And what is the final specification?

## Why an additional node implementation? (LDK)

Speaker 0: 00:34:00

So Jeff, here's a related question, a bit, I would say a bit tangent, but so if we already had say three node implementations, right, why create a fourth and add one more to the sort of like the dynamic of getting features out.
Right, because you know, every time you add one more player that has enough market share, it adds more complication.
I mean, I love LDK.
I'm not like, that's not a criticism of LDK.
I'm just curious, what was the rationale for that?
Aside from just like, we wanna do things in a certain different way.
So it's worth adding one more implementation to the

Speaker 1: 00:34:39

market.
Well, the more the

Speaker 2: 00:34:41

merrier, right?

Speaker 3: 00:34:42

Jeff, don't let the C programmer bully

Speaker 0: 00:34:44

the Rust community like

Speaker 1: 00:34:45

that.
Yeah.

Speaker 0: 00:34:47

No, it's crust now because rust is a trademark.
So I'm calling it crust.

Speaker 1: 00:34:53

I think that's been resolved, but yeah.
So, you know, we had a different approach, right?
So we saw a sort of gap in mobile wallet usages of Lightning.
Or like there were many usages that were very custodial, you know, they might be relying on servers and not having an easy path for Bitcoin wallets to add Lightning was something we saw as a gap in the ecosystem.
So that was the primary reason I believe that LDK was sort of pitched in that direction, I suppose.
We do use Rust compared to other implementations like C and Go, and I guess Eclare is Scott's style, is it?
Might be off on that.
Yeah, so Rust is a very secure language too.
So having that aspect and allowing for language of app findings on top of that.
So developers that are, I think, sort of mobile first and can work in their language of preference was another draw for L2K.

Speaker 0: 00:35:48

Okay.

Speaker 4: 00:35:48

I just want to say it, all the patients that I'm not working on are stupid.
Just kidding.
I think in reality, like the implementations, they're finding their own niches of like things they're better at.
And I think that's one of the advantages of multiple implementations.
And that's just kind of, it's kind of good.
I think everyone's sort of like, as the years go by, getting more and more into their own specific niches.

Speaker 0: 00:36:10

That's fantastic because, you know, it's an honest question, right?
Like it's like more things, more complexity, right?
Is it, is it the right way?
Is it the wrong way?
It's a big market and people are going to want different things.
So it's kind of cool to see that like the implementations are getting less fighty and more sort of like finding their own niche.
So they're not sort of like so much on top of each other because there's only so many customers too for now.
Sorry, Tibas.

Speaker 6: 00:36:38

From the spec point of view, I'm really happy that there's a fourth implementation because the way, the best, the ideal thing when you start working on a new big spec feature is to have another implementation, start working on it almost at the same time as you, because doing it on your own means that whenever someone will come one year later, they will want to change everything potentially for good reason, but you're wasting a bit of time.
But when we only had three implementations and since people have different short term focus and everything we're doing takes a lot of time, so people cannot be working on all the things at the same time, we have a better chance at finding two implementations that work on the same stuff for almost each big feature that we are working on.
And I really think this helps, for example, a very simple example is Taproot, because right now Taproot is not a priority for Eclair and Core Lightning.
It is a huge priority for LND.
So I think they're very thankful that LDK has found time to actually really work on it, give them feedback and make sure that they have two implementations working together on that specification because otherwise L&D would have been blocked because they were the only one working on that and it's a big chunk of work and Core Lightning and Eclair thought it was more important to start with things like splicing and dual funding before moving on to Taproot.
So I think four implementations that are really committed to working on Lightning and collaborating at the spec level is much better than three.
Maybe five would be okay, but maybe it would be too much.
I don't know.

Speaker 1: 00:38:09

I don't want to speak for L&D necessarily, but having Arak and Wilmer from LDK kind of pushing forward on the Taproot classification, I think it's been a boom for that work, I guess.

Speaker 0: 00:38:20

I mean, adding a new crypto primitive is a ginormous amount of work.
I mean, it seems simple, but it's not.
There's all the bindings, there's everything else.
And it is all money handling code now, right?
This is not just business logic.
I mean, I can speak from our hardware wallet perspective.
I mean, we just merged Taproot and we don't trust implementation yet for money handling.
So it's gonna go on a second release, as a separate release.
It's ginormous, but it does allow for a bunch of new cool shit that it can do.
Now, the question always is, like, is the new cool shit actually useful to the users, like, soon?
Or is it just like catnip, you know, developer make work because, you know, every developer wants to work on the new cruise ship.

Speaker 6: 00:39:06

Depends on what you mean by soon.
Is soon 5 years?

Speaker 3: 00:39:12

I'd want to say that it's good that we have four implementations now.
I think there was more of a stagnation or stalemate when it was three.
I don't agree necessarily that there were blockers because I've seen implementations release their own features as experimental and gain adoption for whatever nodes that actually do run it.
But you're right, the interrupt missing is detrimental for the network.
It almost causes an externality if they're not doing something, for example, like forwarding onion messages or things like that.
And I think because there were three before, the app developers also grew frustrated.
And then there's been things that bloomed out of that, such as LNURL.

Speaker 0: 00:39:56

You know,

Speaker 3: 00:39:57

they were very frustrated with the, the stagnation or the disagreeability.

## Feature experimentation and market validation

Speaker 3: 00:40:03

So they kind of took things into their

Speaker 0: 00:40:04

own hands.
In a good way, it's sort of like when the practical people that may not have the best sort of technical solution put it out, the market starts to take, often puts a fire in the ass of the people who can ship the better sort of implementation of something.
Right.
So, so like that was one of the things that I liked the most about LNERL.
Like it fucking works.
You know, does it leak privacy?
Does it have major issues?
Absolutely.
Right.
But it fucking works.
So, and now we have LN proxy for example, too.
Right.
And these things are going to keep on happening, you know, and pushing the other people to sort of get going.
And it also like, in a way it helps people who are going to put the hard time, like, like a lot of time on hard code, like it validates to them that the market wants the feature as well.
Because like, you know, yeah, everybody wants both 12.
Yeah, yeah, yeah.
Right.
Yeah.
Okay, great.
When you ask something like, of course, we're going to say yes, But do you know if the market actually wants that feature?
Right?
Like the LNURL to me just proved that there is like this massive market demand for something like that.
I think it's sort of like a nice indicator there.

Speaker 5: 00:41:13

Yeah, I think the skill too is being able to be, and I say this from the application to oversight because this is where I really shine.
But knowing when you can do things at the application level and when you shouldn't, and them doing LNURL doesn't break interoperability with Lightning.
This is a scenario where, I'm not going to use the word allowable, but it's incentivized to them to be able to do it and it doesn't break anything.
I think another interesting example, TBAS, you guys I believe had Trampoline and Phoenix since day one.
This is another scenario where yes, Phoenix and Eclair, another implementation of, Eclair is another implementation of Lightning Node, but them adding Trampoline to their node and then to their end-users wallet, that doesn't break interoperability anywhere on the Lightning Network.
That's a place where you can add application-specific logic.
And then, NVK, you brought up LNProxy.
This is another application where it's like, okay, let's add some privacy to the Lightning Network.
And this is kind of how we do it in MuniWallet 2 with we use the voltage LSP to hide the receiver's pubkey.
It just looks like it's voltages pubkey on one of their nodes.
This is another case where we can add some application logic until we get the protocol features that we need to get, but it doesn't break anything else.
So it's like a way to add and innovate on top

Speaker 0: 00:42:41

of it.
So like one super important thing that like, you know, you get from Bitcoin is this like extreme backwards compatibility.
Like the I guess like the slightly like variation for that on Lightning is like graceful degradation.
Right.
And I think like that's like so far it's been good that way.
It seems to me that like every time I try to pay something, if that receiver or sender do not support part of the feature, somehow the wallets find a way to gracefully degradate to some other solution to resolve that payment.
I think that's going to be super important as you have all these different implementations going forward.
Right, it's like, how do you still resolve the payment so the customer doesn't suffer?
He may lose some privacy, maybe something happens, but at least like when you scan the QR, right?
Like the payment still gets made.

## Communicating feature sets

Speaker 3: 00:43:29

I think this is a great chance for Jeff or Dusty to touch on the, I think it's Bolt 9, the OK to be odd, like the feature bit stuff.

Speaker 4: 00:43:37

Right, like every feature gets like a, you get to register your numbers.
Like your feature needs to have a feature number.
So like splicing has its own one, and there's evens and odds.
And one of them means like it's optional, and like experimental, and the other one means it's required.
But with the feature bits, when the two lightning nodes connect to each other, they exchange a bunch of feature bits to each other, and then things that are compatible, they then activate those features.
That's the technique that allows the reverse compatibility to happen.
I don't know.
You want to

Speaker 1: 00:44:05

talk about more, Jeff?
Yeah, the feature bits, just to clarify, come in pairs too.
So typically a feature will have both an even and odd bit and such that if you are odd, it's okay to be odd as this expression goes, then it's sort of an optional feature for you where if it's even it's required and you could, I guess, because required, that means you probably disconnect from your peer if they don't support it.

Speaker 0: 00:44:26

That's pretty cool.

Speaker 1: 00:44:27

Yeah.
And I think kind of going back to the conversation too, about like application layer versus protocol layer.
It's great that we have people experimenting on top of Lightning and that allows for that.
I guess what it does also is it puts a spotlight on some of the shortcomings of Lightning.
Seeing, like you said, people building fast because they can't do something on Lightning now, but they want to do it.
So while there are privacy shortcomings of LNURL, it's a spotlight on what we need to do to help fix the protocol level with, for instance, both 12 point paths.

## Payment descriptions

Speaker 3: 00:45:05

Tony, you also fixed something, I think, for one of your applications that you were hacking on last year regarding I think the payment descriptions, right?
Because those are also shared.
I think you started encouraging the practice of hashing it, something like that?

Speaker 5: 00:45:22

Yeah.
Putting descriptions in memos, I think, was a bad decision for Lightning.
And not just putting it there, requiring it.
Requiring that field or a description hash is required and the reason that you know And at the time it was a good idea, right?
Because you want to know that when you pay an invoice That it's gonna be for a specific order like you could have an order number It could have a list of the items in the description.
It's practical for it to be there, but what is ending up happening, especially when we have large custodians on the Lightning Network as more chain analysis starts aggregating more data, but the invoice is being collected, you start to now see you start to attach the receivers pub key to the reason for payment.
And that gets if that's getting shared and aggregated around, you can now start correlating people with the reasons that they were paid.
And that's not good.
In my opinion.
And there's been a...

Speaker 0: 00:46:21

Also, it's pretty annoying, to be honest, as a user, like, stop asking me, forcing me to put a goddamn fucking note.
Like, I don't want to put a note.
Like, You know, it's the same with wallets that require an amount.
Like, I don't want to, like, just leave me alone.
You know, it's weird.
Cause like, you know, I'm a, I'm a base layer boomer.
You know, I kind of feel that way.
You know, when I come sometimes to Lightning, It's like, there's all this weird, different dynamics that like annoy me.
I get that there's limitations and stuff, but it's nice to see that like people starting to see that way too.

Speaker 5: 00:46:54

Yeah.
And so when an invoice is created for Mutiny, like we, there, there is a optional tag field you can put in there, but that's only saved internally.
We are specifically never going to create an invoice with a description and we kind of refuse to because I think it's a privacy leak that, you know, I'm trying to be out here like expressing, hey, don't put descriptions in your invoices, like this leaks metadata and everyone does it anyway.
So I'm just going to build a wallet that doesn't do that.

Speaker 1: 00:47:22

And.
How does Build12 fix this?

Speaker 5: 00:47:24

Does it not require descriptions?

Speaker 1: 00:47:27

It doesn't require.
They're in the offer, but not in the invoices.

Speaker 4: 00:47:30

Oh,

Speaker 5: 00:47:31

cool.
Good.

## Nostr and zaps

Speaker 5: 00:47:31

Nice.

Speaker 0: 00:47:32

Are you guys following all the zapping on Nostr?
Because there's a lot of very interesting things that are coming up on like, for example, like private zaps where like I think you are essentially putting the Nostr node inside of the Lightning comms network and it's encrypted with the Lightning transaction itself if I remember right.
I haven't followed that NIP too much but so There is the NIP 57 for the zapping and sort of like being extended for more things.
And now there is also the Lightning like wallet connect thing.

Speaker 1: 00:48:14

Oh yeah.

Speaker 0: 00:48:15

Yeah, that's like super cool.
I mean like you're not going to need to have a lightning wallet inside an app.
You can just connect to a wallet, but he feels to the user as if you have an integrated wallet.
So your app doesn't open a fucking wallet every time you want to pay something.
So like, are you guys like, as people who work on the protocol and on nodes a lot, like, are you guys following this stuff?
Is this on your radars?
How are you guys like sort of going about it?

Speaker 3: 00:48:43

That's probably a question for T-Bass, Tony, and maybe Jeff.
I'd say T-Bass is also extremely well-rounded because Eclair ships Phoenix as well as their implementation and everything.
So it's like one comprehensive thing.
So he probably has great insight.
Yeah, to be honest, I haven't had time to follow everything that's happening around Nuster.
So yeah, I don't know,

Speaker 6: 00:49:07

to be honest.

Speaker 5: 00:49:08

Yeah, I'm very concerned about Lightning usage on Nuster for both the Zaps aspect and also the custodial integrations like Wallet Connect.
You know, there's a side of it where it's like, we can be up here preaching about lighting privacy all day long and then someone connects their node up with AMBOSS and shares the balance.
Like, we can't stop that on a protocol level.
And all we can do is educate and tell people why it's dumb, why you why you shouldn't do that, why you shouldn't use custodians.
We can preach this all day long, but then someone goes and

Speaker 0: 00:49:44

do it.
I mean, we can't say anything like saying won't change behavior, offering tools that fix the behavior that are easier to use will fix the problem.
Right.
Like and this is why I'm bringing this up because you know like when you actually look at like the transaction graph I mean like it looks like Nostr's like what like 70% of all the Lightning transactions at least was the peak.

Speaker 3: 00:50:08

Yeah, I think Ben Carman did some research.
Yeah, it's 70% of all Nostr's apps were Wallet of Satoshi or something like that, right, Tony?

Speaker 5: 00:50:17

No, it was around 40 or 50 percent, but in total, 92 percent were custodians.

## Custodial lightning and censorship resistance

Speaker 1: 00:50:25

Yeah, I think you have to be also very careful about custodians with this because there's a censorship resistant aspect, not just the privacy aspect.
So if you have someone who wants to receive Zaps and there are dissidents in the country, say like in Iran, there could be a problem with censorship from, I guess, different regulators.
And so you have to be very careful about the services you use.

Speaker 0: 00:50:49

Or I mean, you could be you could be going to jail because you're sending money to a country.
You're not allowed to send money from your country.
Right.
Like they literally have laws that do that, you know, because it's all small amounts.
Like nobody really cares.
But, you know, technically you're breaking some serious fucking laws.
And, you know, if there was interest taking on this, it would be a big deal.

Speaker 5: 00:51:09

Well, but then the aggregation amount, too, right?
Like, yeah, everyone everyone says, oh, I just put, you know, five five dollars worth of Bitcoin on wall of satoshi.
But if that, you know, five dollars adds up, you know, hundreds of thousands of users, then, you know, you start to you start to get a lot of money that could be rug pulled all at once or or seized, to be fair.
Like that's probably more what's going to happen than anything else.

Speaker 3: 00:51:34

Or price appreciation, right?
In 2031, you get a knock on the door, why'd you give this Iranian $20,000?

Speaker 5: 00:51:43

Right, like wasn't it a lot of the Silk Road data was collected and used for chain analysis data too.
So it's like, yeah, this is a custodian, you know, that data wasn't on chain, you know, not all of it, but you know, you have a seizure observers.
And then now that data is basically set in stone because it was collected and is going to be and has been used to prosecute people.

Speaker 0: 00:52:06

Okay.
So, so, okay.
So, so like, is that, does he also like the Nostra stuff is not something you're paying attention right now?

Speaker 4: 00:52:13

I think, Bitcoin has reached this point where there are so many things happening that no one person can cope with all of it, right?
Like, I feel like just keeping up with all of everything happening in lightning is like a full-time, you know, job on the side of my existing job, right?
So the Nostr stuff, like, I find it very exciting that, like, you know, PGP never took off.
Nostr feels to me like a PGP replacer that is taking off.
I'm excited that's happening.
I have one.
Oh my God, I'm guilty of this.
My Nostr account is a custodial connected app.
But like, really, I'm just looking at it.
I just want to see it.
You know, I'm not putting any real money on there.
I'm just sort of like checking it out.
But I think Tony is absolutely right.
The way we solve this problem, or whatever it is that we can't set it, the way we solve this problem is we need to make the self custody solutions as close to as easy as custodial ones as possible, right?
We gotta remove the barriers, make it easy to do it correctly.
And then we can evangelize doing it correctly to people and like actually have that movement get some team.

Speaker 1: 00:53:13

Yes, it's important just to provide that option.
People will use custodial services, but they need to have the opportunity to self-custody.

Speaker 0: 00:53:20

Well, I mean, being very realistic, I mean, like lightning doesn't scale past a certain amount too, right?
So base layer takes us from like, you know, having cuck money, right?
Having a central bank to not having a central bank, right?
Like, and, and, you know, like it's more akin to Fedwire.
Hey, great.
We can now send each other a million dollars for like reasonable fees and nobody can stop us.
Right Now we can't buy coffee on Bayes layer as people are, I don't know, somehow people are surprised that the fees are going to be high, you know, like sure it's the DGN right now who are clogging up the pipes, but like soon is going to be just the population of the world.
Right.
And Lightning is like fully dependent on base layer, right?
So there is also a scaling limit to Lightning as is.
I mean, you know, maybe you guys can educate me on like very cool things on how we can do things better and more scalable, but Lightning, Yeah, we're going to get there.
So, so like, but you know, like lightning as is right.
Like, you know, it doesn't scale to a billion people.
Like you cannot do, you know, like a billion payment channels.
Like right now you just can't.
So, and the world has 8 billion people.
So like, you know, there is a scale here that, that we're going to slowly get into.

## Splicing

Speaker 0: 00:54:39

So it sounds like, splicing has both like this amazing privacy aspects to it.
And then he has very cool scaling things too.
And also incredible like economic advances too.
So who wants to explain Spicey?

Speaker 4: 00:54:57

I could try.
I think like, it's, It's just like you said, there's like three different things there.
It's a whole complex rabbit hole.
But simply put, it's the ability to resize lightning channels without closing them.
But what's become apparent over time is that unlocks a whole lot of things.
What you're doing is you're essentially creating fungibility from on-chain Bitcoin to lightning, which changes the entire game.
At first, it's like, ah, just resizing channels, whatever.
But then literally everything changes about it, including there are some theoretical concepts now about changing how coin joins work to integrate splicing and perhaps make those better, get some like stenographic techniques going.
So like literally everything's changing.
There's sort of like a laundry list and depending on like which part you wanna talk about first we can go into the individual one.

Speaker 0: 00:55:43

So first question is how long do he ships?

Speaker 4: 00:55:48

Two weeks.

Speaker 0: 00:55:50

Before we get into this, two weeks.

Speaker 3: 00:55:54

Dusty shipped it for himself, right?
I don't know if he's revealed like any of the script, but he did point to a mainnet transaction.
And I believe T-Best also has done that.

Speaker 6: 00:56:04

And we are we are actually going to ship it in at least not the final spec version.
And it's a simplified one because in Phoenix, since we don't have public channels, It's it makes it seem like it removes the aspect of the gossip part.
But we are going to ship a prototype version of Splicing in Phoenix on mainnet real soon in the next few months so that we can get real world data about the issues with that, feed that back into the spec and put the finalizing touch on the token.

Speaker 0: 00:56:33

You heard here first one hour into the show that we're going to get splicing this year.

Speaker 4: 00:56:38

If I could just add.

Speaker 0: 00:56:39

Go ahead, Dasi.
Let's explore the three major aspects

Speaker 2: 00:56:42

of this.

Speaker 4: 00:56:42

Yes, let's plant my flag.
I did the first splice on Chain last year in May and I finished my Splicing Limitation around October.
But like things in Lightning aren't normally considered done until two Limitations do it, sort of like the way that things do it, call it interop.
And so I'm working on interop with T-Dash and once we get two Limitations that have it done, then it's officially like, you know, considered launched or whatever.

Speaker 3: 00:57:04

I want to, I want to take a quick tangent about like how proud I am to NerdSnipeDusty via Nifty who like onboarded him to CLN to do this specific thing.
Poor guy has been banging his head for splicing since CLN had only one channel per peer.
So he's adjusted it multiple times.
And then now his work on Interop.
Kudos, man.
You've really like you've stuck to it.

Speaker 0: 00:57:29

Well, I mean, you know, like subtle masochism is known also as core developers of Bitcoin or Lightning.
Anybody who's a protocol developer really likes pain and rebasing.
It's a It's a thing.
I mean, like some people like pain, you know, like, you know, I'm not judging here.

## Scaling

Speaker 0: 00:57:50

So anyways, so let's explore scalability first, because, you know, without that, like privacy and everything else, kind of like who cares, right?
I mean, Are we scaling here?
Are we reaching capacity to really on board our next billion people?

Speaker 4: 00:58:05

I think spicing gets us closer, but it's not the slam dunk that's gonna be like, yay, now we get all the billion.
But maybe today we get a billion, so we only need to 8X, right?
Just pull one trick out of our hat to get 8x that and we're good forever, right?
Population will never grow.
So. So. So.

Speaker 6: 00:58:23

So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So. So.

Speaker 2: 00:58:41

So. So. And you just update that UTXO, but right now we need multiple UTXOs per users.
With splicing, you only need one, but it's still one UTXO per user.
So it's not going to scale to 8

Speaker 6: 00:58:41

billion users.
We still need to add sharing that UTXO between users on top of that.
And that's something we don't know how to do yet.

Speaker 0: 00:58:47

So tell me what we know now.
Like what can we do now and how does splicing works with a single UTXO?

Speaker 6: 00:58:54

Yeah, this part is really simple.
Right now, that means you have a lot of channels.
Whenever you have one channel in your mobile wallet, whenever you want to, whenever you would have wanted to open a new channel, you just instead update your existing channel.
So you're basically spending that UTXO, creating another UTXO for that channel.
So you're still sticking to one UTXO per user.
You have to make on-chain transactions, But at least you only use one UTXO per user.
And for pairs of nodes, for routing nodes, you basically need only one or a few UTXOs per pair of nodes.
Because you may still want to have multiple channels with peers you are relaying a lot of payments to because channels are still limited in the number of payments that can be pending.
You may want to have one public channel and unannounced channels on top of that to hide some of your balance.
There are reasons to keep multiple channels between pairs of users, pairs of nodes, but you're going to need fewer of them than today.
Today you end up having too many channels with those peers because you don't want to close them and then make another transaction to open a new one because it costs you two transactions whereas with pricing, updating a channel costs only one transaction and you can also batch it with other things that you want it to do to make it more efficient.

Speaker 1: 01:00:06

Yeah, I think the blocks-based argument there is what you guys are getting at too.
What we see today with high fees, if you have to close a channel then reopen it, you know, that's gonna cost basically twice as much.
So splicing is going to help with that.

Speaker 3: 01:00:20

And the beauty of all of this is the Lightning node itself experiences no downtime, right?
You can still be paying each other.
For all the nodes that understand the new form of gossip, but even like the old form of gossip, I guess, like they'll see it as like that SEID, the original one closed and there's a new one, right?

Speaker 4: 01:00:41

Yeah, I think the way to think of it is like when you want to use lightning, you have to basically plant your stake or your flag on the blockchain.
And there's only so much space in the blockchain.
And splicing like legitimately, like can double or triple our capacity by reducing the blockchain usage by that much or potentially even more, right?
It's kind of hard to know exactly the number.
So we've like, we just like tripled the capacity of Lightning, right?
All we need is like a couple more triplings.
We can get to a million people, right?
Obviously, I think the next, as we go down, we're getting to harder and harder things.
How do we actually triple it again is gonna be a lot harder than splicing was.
And then the next thing we try to chip away, it's going to be impossibly difficult.
But I think like if we can get some, if some changes do come through on the core layer, there are some really interesting stuff that can be done.
And we're kind of inching closer to maybe the world scalable, but I don't know what the future is going to hold.

## Bitcoin core changes that would advance lightning

Speaker 4: 01:01:32

We'll see.

Speaker 0: 01:01:32

So what changes to Bitcoin Core do you need?

Speaker 3: 01:01:34

APOs.

Speaker 0: 01:01:35

Let's just put them all out here because then people will definitely make the changes.

Speaker 4: 01:01:39

APOs is a big one.
Signature input aggregation would be another big one.
I'm trying to think.
The mempool stuff would be awesome to see fixed.
We're wasting a lot of block space, package relay.
If you're wasting

Speaker 2: 01:01:50

a lot

Speaker 4: 01:01:50

of space with these anchors, that could all go away with those.
Those are the three that come to mind.
You guys got any other core projects you guys are favoring?

Speaker 5: 01:01:57

Some of the transaction v3 stuff to kind of help against paying tax on Lightning.

Speaker 6: 01:02:03

In the short term, I would really like to see package relay and ephemeral anchors, because that's something that's only a policy change.
So in theory-

Speaker 0: 01:02:11

Package relay shouldn't be hard to change.
It's not consensus.

Speaker 6: 01:02:15

Yeah, so it should be easier to train.
It's actually, people are working on that.
It's making progress, but like everything, it takes time because you want to make sure you don't create new DOS issues and you really fix the problems you are trying to fix.
But this would have had a huge impact on Lightning, especially nowadays with the high fee situation, because once we have that, we can actually make the commitment transactions pay zero fees and only pay fees by doing CPFP, which means that when you are touching the chain, you see exactly why you have to pay fees and you can choose that fee rate.
But then once you're in Lightning, you are completely decorrelated from unchanged fees.
Whereas nowadays, this is not the case because since the commitment transaction needs to pay a fee that has to be able to at least enter the mempool, whenever you add HCLCs to a channel, you have to take into account the fact that you are the commitment transaction is getting bigger.
So it has to pay more fees.
So potentially you're restricting how much the user can use from its channel balance, which is really annoying and impossible to understand for users and impossible to explain to normal users.
So that's something we've always wanted to get rid of.
We know the fix.
It's easy.
We just make the commit transaction, pay zero fees.
But it needs that package relay and ephemeral and cost change in the Bitcoin policy logic.

Speaker 0: 01:03:32

I mean, technically, you could just fork and start doing that.
I mean, like, you know, it's just a policy.
Like it's not really that big of a deal.
I think we're going to actually start seeing a lot more of standardness and other things starting to change.
I think we're going now towards a direction where we're going to see more balkanization on core non-consensus rules.
Fortunately, people like the non-FooRBF people probably just learned now that why you need FooRBF because the fees are high.
But, you know, it goes both ways.
You're going to find also reasons why like, you know, core wanting to sort of keep something tidy in a certain way.
Like it's not accepted by the rest of the network.
Again, if it's not consensus, you can do whatever the fuck you want with your node.
So here's a question.
How does it leverage APO?
Like the change you were mentioning?

Speaker 4: 01:04:17

Oh, APO is so exciting.
Well, I mean, the big thing about APO is that the Lightning database is going to go a smaller, which isn't necessarily an on-chain thing, but like currently, whenever you do a Lightning transaction, What we're really doing behind the scenes is we're making a whole bunch of Bitcoin transactions that we sign and just never actually publish.
We end up with this, if you do thousands of payments, each one of those payments is a whole collection of transactions we made to go along with that.
You end up with tens of thousands, hundreds of thousands of Bitcoin, unpublished Bitcoin transactions.
With APO, all of that goes away.
The big thing is because when you chain multiple transactions together, like I published this transaction with spends into this transaction to that one, ABC, all child of each other, they have to be signed referencing who their parent is, right?
And APL allows us to separate that bond, be like this child transaction, we can sign it for any parent at all.
And that just makes, it makes lightning just so much better in general, but it also makes things like wash showers a lot better.
It just it just fixes the entire like everything basically.
And to me, I don't think it's I think it's not a controversial change, which is maybe why it's not getting a lot of attention.
It's just there's nothing wrong with it.
It's sort of an obvious like next of improvement for Bitcoin in my eyes, I haven't seen a good critique of it.

Speaker 0: 01:05:34

Famous last words.

Speaker 3: 01:05:36

Yeah, I was just about to say like what Dusty is referring to is, is LN symmetry, previously known as L2, and it has a channel factory benefits and things of that nature.
I do disagree that APO soft fork is not controversial.
I think it's actually any soft fork by definition is extremely controversial.
But Nevertheless, it is very exciting to see if it does come to fruition because it's been in the works for a very long time as in other names as SIGHASH, NOINPUT, many other things like that.
So I don't know.
We'll see where that ends up, perhaps.

Speaker 0: 01:06:16

I don't know.
Like I'm partial to CTV and OpVault sort of path there because I really want to see that stuff happen.
I think you can do some of that stuff with CTV instead of APO.

Speaker 3: 01:06:27

You cannot, you need another soft fork for a check

Speaker 2: 01:06:30

to

Speaker 3: 01:06:30

sig from stack.

Speaker 0: 01:06:31

That's right.

Speaker 3: 01:06:32

So it gets very hairy about like, who wants which soft fork for which purpose?
Cause the covenants, yeah.

Speaker 0: 01:06:37

Oh, it's going to be like, first it's going to be very hard to get any soft fork done in the next few years.
Like realistically speaking, we can't even agree on how to activate it, which is even more contentious than the actual content.

Speaker 1: 01:06:49

Yeah.
And when we build on those, L2 is the name I was familiar with.
Is there a new name for L2 right now?

Speaker 3: 01:06:56

Yeah, I believe InstaGibs has taken the mantle and He's calling it LN Symmetry now.

Speaker 1: 01:07:02

OK.
Are there changes to the original L2 because of that or is it just a rebranding?

Speaker 3: 01:07:07

I think there are some changes.
He's just kind of putting it all together with the new package relay stuff and ephemeral Anchors, all the new innovations recent to Bitcoin.
I think he's taken a lot of Anthony Townes' feedbacks and previous like Christian Decker's work and he's like put it all together in one comprehensive thing.
There's a Chaincode Labs podcast episode where he discusses it in deeper detail.

Speaker 1: 01:07:33

Yeah, I'll take a look at that.
As we add new support at the base layer for these enhancements to Lightning, new challenges are going to arise, of course, with L2.

Speaker 2: 01:07:46

Symmetry.

Speaker 1: 01:07:46

From what I remember, there was, you know, it's a different punishing...
Yeah, symmetry, right?
There is a...

Speaker 3: 01:07:51

There'd be

Speaker 1: 01:07:51

a different punishment mechanism.
Exactly.
And so there's, you know, issues around that.
And then I think channel factories were mentioned at one point and how that is practically managed, I think is probably a...

## Testing, breaking and adversarial actions

Speaker 0: 01:08:06

And I'm pretty sure Burak is going to be

Speaker 4: 01:08:08

the only person who tested.

Speaker 0: 01:08:12

What an amazing event that was.
The fact that nobody had tested.
Classic.
But it also shows how many, like not a lot of adversarial work being done.
Right.
Like, I mean, practical for real, like there is no real adversaries right now trying to break it and trying to steal that money.

Speaker 3: 01:08:30

That's why we have people like Gleb, Antoine, Tony, Paul, and Ben, Clara.

Speaker 5: 01:08:39

I wouldn't say that there's nobody testing.
I think that's very unfair.
I think the protocol process of like two implementations, I think that weeds out a lot of issues from a bug standpoint to multiple brains looking at it standpoint in depth.
But also, I mean there are people trying to break things actively all the time.
They don't catch anything or they don't catch everything all the time.
In fact, you could say like, I mean, there's what, like over $100 million worth of Bitcoin on Lightning currently.
I mean, that's a big bounty.
Like I know there are people attacking Lightning.
I've done my fair share.
I think.

Speaker 2: 01:09:16

We got

Speaker 3: 01:09:16

to talk about that for sure, how you probed all of T-Bass' private channels

Speaker 2: 01:09:24

because he

Speaker 4: 01:09:24

was the biggest node.

Speaker 5: 01:09:25

Yeah, well yeah, and there are attacks, but there's a lot of attacks that are just privacy level because security level is pretty good and has been tested and is being tested.
But yeah, going back to that, if you go to hiddenlighteningnetwork.com, there's a list of I think almost 10,000 different private channels that I probed out and found the original UTXO for it and which node it is that opened that private channel.
And most of those 10,000 are from the Eclair node, specifically.
So I was just trying to guess, like, OK, Let's see how many private channels there are.
This probably correlates to how many users of Phoenix there might be, and so I went out and did some probing and found that out.
But that's being fixed.
You know, store channel ID alias.
I'm not going to say that I pushed for more SCID alias adoption by attacking it, but it was already being worked on.
It just sort of finally happened and now I can't do that anymore and I stopped probing.
That's just one scenario where I like attacking, I like looking in depth on things.
I think channel jamming is the one.
There's a lot of really intelligent people working on channel jamming solutions right now and they're all kind of at the point where if we want to rush this, and if we want to rush adoption and get some more eyes on this and stress the priority of this, we can channel jam the network if we wanted to.
We know how, but we're not going to.
It's like the ethical, It's an ethical way to go about it.
They're very well capable of doing it.
You know, the Claire and Antoine, especially on the channel jamming research, but you know, it's one of those cases where like-

Speaker 0: 01:11:09

Just do it guys.
Just do it.
It's the only way to get the devs to move their ass on it.

Speaker 3: 01:11:15

Yeah.
Barack, if you're listening, don't listen to him.

Speaker 0: 01:11:20

Hey, Barack, I'll buy you a beer if you jam the entire Lightning Network.

Speaker 5: 01:11:25

See, like probing is one thing, but like jamming, like there's actual damages that come across from that.
So that's, I think, the ethical dilemma there.

Speaker 1: 01:11:33

Yeah.
And Tony, just to plug it, I think you had used LDK to implement your probing tool.

Speaker 5: 01:11:41

Yeah, that was my first LDK project.
I did the proof of concept in L&D in one hour and then it took many months to do my first LDK project and do that jamming.
And then from there I built Lnsploit, which is based on LDK and it's the whole concept of attacking the Lightning Network.
That was right after Brock released that vulnerability that broke all LND nodes, I reproduced it inside Lnsploit.
Me and Ben Carman hacked on that a little bit and then we demonstrated it at TabConf on RegTest where we actually went through, used LNSploit to broadcast the bad transactions, break an LND node, and to do a force closure on a previous state.
We did that all with LDK.
That's something that would have been very hard or almost impossible for me to have figured out how to do with L&D or other implementations.
And that's just like a kudos to LDK and the customized ability you can do with that.
But yeah, that's that's I'm on my like fourth or fifth LDK project now.
It's a lot easier.
So I appreciate all the efforts there.

## Shadow channels

Speaker 3: 01:12:48

So that was another fascinating thing to me.
You know, just naturally being at Blockstream previously, I approached things more from the spec angle.
So I had a great time always chatting with Tony because he's approaching things from the app dev angle, more from a routing node operator.
So Tony, can you touch on some of those shadow channel theses you had, basically how people had their private channel and their public channel, and the public channel shows a certain amount, but the private channel is the one with the actual depth.
And then when you try to probe, it automatically leeches onto like the public one.
Like you knew all the works.

Speaker 5: 01:13:27

Yeah, I don't know if there's there is an actual term for I've just been calling them shadow channels, the idea of having one smaller public channel and that's what people see on the graph and then you have bigger channels behind that and those are all private channels.
And one of the things that would have helped is some of the SCID alias stuff, which has been fixed anyway, so that doesn't help that one as much anymore.
But from a balance probing angle, it makes it a lot more difficult to do accurate balance probing if you have – if your actual depth of how much you could route is not only hidden behind that public channel, but also you can't hit the limits.
You can't go above the limits of the channel itself in a single payment.
So you may have just like a one million sat channel that's public and you have like a ten million sat channel underneath it.
No one can actually balance probe that whole ten million.
They can only really guess what side one million of that channel is on either side.
So I think, you know, it's been a long time since I've even thought about that concept.
So you guys correct me if I'm wrong there, but the whole idea is about obfuscating how much funds you actually have on your Lightning Node, but then also going further and obfuscating how much funds you actually have on a particular channel too.

Speaker 1: 01:14:51

Yeah, I guess there's probably publications for probing then.
So if a node is relying on any sort of probing to determine if their payment could be made through that channel, if they're probing through, I guess the public channel that's smaller, they might have like a incorrect sort of assumption of what your balance may be, and thus may avoid your channel entirely, if you're a routing device.
But If you're a recipient, then you would definitely need to at least, like I said, if you're a recipient, you might just use a routing hint for that.

Speaker 5: 01:15:24

Yeah, you're exactly right.
You just prove that you could route a payment, which before that would imply, okay, there's this much balance at least on this side.
And that's still the case here, but by reason of subtraction, you can't do that anymore now, if you have shadow channels, you know, multiple private channels underneath the public channel.
So that kind of, you can't do the same subtraction method you could before.

Speaker 1: 01:15:48

Yeah, there's like this give and take between reliability and privacy.

## Splicing (cont.)

Speaker 0: 01:15:52

Going back to splicing, we kind of only started exploring it.
So we get the benefits of scalability, right?
Because we're making the transaction small.
What are the benefits and how do the privacy benefits work of splicing?

Speaker 4: 01:16:06

So like the privacy benefits mostly all just go on chain, right?
I think like when a couple other lightning features come together, you're going to get this crazy level of privacy.
And you have like a private channel, not unannounced channel, whatever it's called.
We're not calling it private anymore.
You combine that with Taproot outputs, you get to some crazy stuff where, with Taproot, the Lightning channels look on chain like any other payment.
And once you get to the place where lightning channels look like getting the payment, you can start doing things where, Adam Gibson has this awesome video that he recorded talking to down in BTC plus plus Mexico, talking about how you can use splicing to deal with toxic change.
And you can eliminate like all of the change problems with coin joins.
So essentially, because you can just dump your change into a channel, it enables this crazy stuff.
And it's all theoretical.
But if anybody's got to work on it, it's Adam Gibson, right?
I think he's trying to encourage others to sort of like take the take the baton with that.
But I think the core thing to think about with privacy is is is coin joins changing one to not need change but then two one thing that happens with coin joins is you have to have a coordinator.
So this is somebody like a usually like a company that you go register with them say hey I want to go coin join and that's that's like a tiny pot right there's a company that's controlling it.
It's kind of a problem and one of the things we're getting with splicing is using Lightning nodes themselves as the coordinator of these coin join like things.
So you can do a combined multi-person transaction with you and your peer, but your peer can also do with their peer and their peer can do with their peer.
And you only, just like lightning, you only know about the two peers next to you.
It could be any number of peers down the road and all of their splicing activity plus any on-chain activity they wanna bundle in can be put into one single transaction.
And this is all being done without a central coordinator, which I think is quite a big deal for the privacy on-chain.
Anyone else want to add anything to that?

Speaker 0: 01:18:07

Tony, is this part of the Mutiny's solution?

Speaker 5: 01:18:12

Well, not immediately, but it is something that we even written about.
Lightningprivacy.com, me, Ben Carman, Paul Miller, a few other people, Evan Kludis, we worked on this.
We actually, both T-Bass and Dusty came and presented some of their concepts to our research group while we were going through it.
And this is one of the biggest things that we're interested in the most when we actually get splicing and we can use it, is the concept of being able to do coin joins from splicing rounds.
I mean, not just for privacy standpoint, but also a scalability standpoint, too.
I mean, I think some of the free rate stuff kind of shows that, you know, we sort of need collaborative transactions to be able to help scale Bitcoin on chain usage even more.
And part of that is even channel open, channel opens.
So being able to do coin join in channel opens, dealing with, you know, the toxic change, not having that privacy leak, that's some of the things that we're kind of wanting to build into LN4TX, which is something Ben Carman started on specifically to do CoinJoins on Lightning.
I think splicing really changes the game from what we can do, because also it's like zero downtime, too.
So you can say if you can add CoinJoin liquidity onto the Lightning network, you're still able to route and collect yield off of your routing fees.
You now just basically created a way to coin join and make fees at the same time.
That's huge.
Let's go.

Speaker 0: 01:19:38

So like here's the thing, right.
So, for example, joint market, unfortunately, like kind of like it has volume that kind of comes and goes.
But it's not dissimilar to what you're describing.
Right.
I mean, you have a market maker in your case will be the liquidity provider probably.
And, and then you have people who are just the takers there.
And for some weird reason, I mean, it might, it could be the UI problem, right?
That JioMarkets doesn't have like a very dumbed down UI.
And then there is also, of course, the privacy, Bitcoin drama and all the stuff around it that makes it trickier.
But In my view, having essentially like a mixing markets, right?
It's a much more elegant and much better privacy solution, right?
Because you don't have a central coordinator who may or may not have extra visibility and also has the wrong incentives really, because their incentive is to collect fees, right?
So anyways, like this to me seems to be going in the right direction.
And it feels like you'll be kind of like just integrated into things because why wouldn't it?

Speaker 5: 01:20:43

And also like the last point on that, like the fees collected, they're not even necessarily the fees from the coin joiner and the quitting service itself, because you're just being a routing node collecting fees.
You're just participating in zero downtime splices collaboratively with other people as well.
So it's like both a privacy enhancer, it's almost like you're doing, you have two different business models almost, but you're still routing off of fees, so it doesn't provide perverse incentives like you kind of described with being the coordinator and collecting fees and controlling all of that.
You're just doing one thing over here, collecting fees from it, but you're able to participate in another system as well.

Speaker 4: 01:21:25

I think one of the big things that separates splicing from some existing coinjoin stuff is you have to pay money to do coinjoins.
If you're doing splicing, you're literally saving money.
It's cheaper to join the splice to your own transaction.
And I think what that means is it's going to encourage a lot of people that wanna do something on chain to be like, you know what, I don't need this today.
I could wait a week, put it in a queue, wait for someone else to start a splice, someone to make that market, and then just automatically join it.
And I think if you look in the long run, this should create a lot more sustainable activity in the splice network compared to something like, I don't know, join market, you know?

Speaker 0: 01:22:02

Yeah.

## Payjoins and keysend

Speaker 0: 01:22:02

Could you, like expanding on this, like, could we do a pay join, for example, also with something like this?
Because I don't know, like, I can't see why you wouldn't be able to just like do the pay join and get even one more privacy set.

Speaker 4: 01:22:18

100%, yeah.
You can put whatever you want in these things and pay joins are a great idea that I think it'd be.
I think like I've been I've been toying around with some proposals of like how we can get wallets to integrate with pay join splicing compatible protocols, right?
So the challenge, like it's totally doable.
There's nothing stopping it from happening other than just basically evangelizing to wallets to do it.
And I probably give them on like a specs, they're all doing it the same way kind of thing.
But that's probably the future.

Speaker 0: 01:22:45

Yeah, cause like the problem with pay join is that like it requires like coordination and and Bitcoin one of the most beautiful things about like base layer Bitcoin is that it doesn't have to be interactive, right?
Somebody posts a Bitcoin address an invoice, right?
You pay that You don't need to be online at the same time.
You don't need to talk.
You don't need anything like you're essentially completely like can leave, go your own separate ways.
But because Lightning is interactive, you're already having that like trade off, right.
Of having to be online and talking to each other.
Well, then might as well talk about a few other things, right?
Like, hey, is this your happy conversation?
You know, do you also want to exchange some UTXOs?
I got a whole one here for you.
You know, like, And you can add like quite a few more things there.
It's like, why not?
So like.

Speaker 3: 01:23:35

Yeah, you're not crying about the interactivity about three rounds of going to two rounds when you're having like 20 hops.

Speaker 0: 01:23:42

That's right.
Right.
So I don't know, like it really feels natural, right?
Like to do these things with Lightning and payments are like one of the most privacy needed parts of the whole money experience, right?
Like, you know, maybe you find some privacy in your savings, right.
Where you're stocking your Bitcoin, we can argue about how that could be done and you know, how much privacy you need on that and all that stuff.
But, but then like at the payment side, when you're spending it, right.
Like really is the part where most people get doxxed.
And because you're now having to interact with a secondary party, right?
A third party there.
And I don't know, like this, this feels perfect.
I mean, I could finally buy a latte and nobody's going to know about it.

Speaker 3: 01:24:30

I guess like the hacky way people are doing that today would probably be with like Key sends and amp right Tony.
That's probably the closest tool that people are using

Speaker 5: 01:24:43

For what specifically

Speaker 3: 01:24:44

buying coffees on lightning like with privacy or whatever

Speaker 5: 01:24:49

Yeah, I mean, I mean just a normal so normal invoice would would work there.
I mean,

Speaker 4: 01:24:54

yes

Speaker 5: 01:24:55

Yeah, I don't think people key send for actual payments.
I think that's mostly for donations as the selling point.
Like, you know, value for value stuff.
Yeah.
Not even Nostra uses a key send based approach.
Yeah.
I haven't thought I haven't thought about key send in a while, to be honest.

Speaker 4: 01:25:12

Whenever I buy a coffee, I always pay ten dollars in on chain fees alongside

Speaker 0: 01:25:15

of it.
That's right.

Speaker 5: 01:25:17

I just use cash.

Speaker 0: 01:25:18

I don't know.

Speaker 3: 01:25:20

Dusty, I need to give you some of our Sats cards.
You know, they're perfect for this use case.
You put $10 on here.
It's also off chain scalings.
We're doing our best.

Speaker 0: 01:25:33

You know, we do it mountain man style, right?
Like here's private key, take private key.
You know, like you guys are doing all this complicated shit, You know, like some crazy interactive cryptography.
Like here's the private key.
Just fucking take it.

## Blockspace concerns

Speaker 3: 01:25:52

So for like all of this privacy benefits, it sounds fantastic to me.
How is the transition to it on a heuristic change approach?
You know, we're switching into Taproot outputs on-chain.
The non-sets are slightly shifting because of the UTXO set.
I guess Taproot is in more usage because of the BRC20 Dgens too.
Like we're in an odd place now.
How do you guys feel about it?
What's going on with the heuristics?

Speaker 4: 01:26:20

Oh man, splicing is more important than ever with all the spam going on.
Right.
Like I think I think

Speaker 0: 01:26:25

they're valid.
Shitcoin transactions.
There is no such thing as spam in Bitcoin.
I will repeat this 50 times.
If it's a valid transaction is a valid transaction.

Speaker 4: 01:26:38

I think it's a weird it's a weird match for for Spicing where it's like I think people are paying more attention to Spicing now because of all the legitimate on-chain activity.

Speaker 0: 01:26:49

DGN complete retard activity.
Sure.

Speaker 2: 01:26:53

But

Speaker 0: 01:26:53

it's still valid transactions.

Speaker 4: 01:26:57

Oh man.
But it's kind of funny that the bedfellow of getting Spice and getting more attention is these DGNs. Doing whatever they're doing on-chain, which the more I look into it, the more I'm like, what am I looking at?
I'm wasting my time trying to understand this at all.
But, splicing like really does increase the on-chain efficiency.
And I think you just go back like six months ago, that was like, oh, theoretically that matters.
Now it's like, oh shit, I should have been thinking about this a long time ago.
And hopefully that kind of like wakes people up a little bit and gets them gets them geared towards the future.

Speaker 0: 01:27:25

Yeah.
I mean, like, you know, it's kind of weird that like people are.
I mean, I get why people are triggered by all this shit because it's all shit.
But at the same time, it's like, what do people expect when like Bitcoin has a real amount of users coming in?
Like, you know, you think the fees are going to be like, you know, I mean, I'm one set V-byte maximalist.
I might not even rebroadcast them when they drop.
But like, you know, the expectation is that like we're going to be like 10x this in cost, like when there is a few hundred million people.
I mean, if there is 5 million Bitcoiners right now, it's like, we're probably exaggerating.
I love like, you know, sure the VCs and all the startups claimed, you know, Bitcoin has a hundred million users, 200 million users, 500 million.
It's all bullshit.
I mean, if there is 5 million people right now on Bitcoin, it's like, you know, pushing it.
So can you just imagine like, it's a great dry run in my opinion, for us to sort of like get a little taste of what it's like when there is not just price, Because when the price goes up, you know, all the retail comes in, they all want to buy their, you know, their 615 Bitcoin.
But like now we have other people coming in with all these other users that, you know, are completely yotic.
But they do set a floor, right, for transactions.
And, you know, Lightning has to get its shit together.
Right.
Because Lightning was never in scale around a high fee market.

Speaker 4: 01:28:54

I think this brings up a great point of if you look at there's some apps like the Moon Wallet, maybe people will try it.
M U U and Moon Wallet, where they're they're trying to be this wallet where you can pay to an on-chain destination and also to a Lightning destination, right?
But their concept is storing all the Bitcoin on-chain and moving it to Lightning on demand.
That works fine when on-chain fees are like 10 cents, but now that they're like $10, suddenly every Lightning payment, which should be basically free, costs $10 on Moon.
So that kind of app isn't sustainable, but splicing enables you to make a moon wallet in the reverse.
So this means you can store your funds on the lightning side and then make on-chain payments as needed, but get those cheap views on lightning when you need it.
I think this is gonna be a big deal.
Like, if you look at a lot of the apps that are out there, they tend to have separate balances.
They have a Bitcoin on-chain balance and a Bitcoin lightning balance, right?
And they don't really merge them together.
When they are merged together, the app developers doing all this crazy compromises, either making them charging the users a ton of money or making it slow or both.
Right.
And I think Spice is going to just change that game.
And Eclair, obviously, with the Phoenix wall is the first one that's going to be doing this.
But eventually, I think all of them are gonna have to switch over to it.
And this is gonna be a big UX improvement for new users.

Speaker 0: 01:30:10

I still remember on Breeze where I didn't read the fine print, I never read the fine print.
I always just pressed the button.
As people would know, I deleted my account on Nostr by pressing the button.
So like I receive more than my wallet could receive on chain.
So they had to do this whole like, you know, first, second, whatever transaction.
And you know, I didn't really bother reading to understand what the fuck was going on, but like essentially took like two days or three days for me to get my money in and also pay fees.
And this is was in the low fee environment.

Speaker 3: 01:30:44

Really?
Yeah.

Speaker 0: 01:30:46

So Roy explained to me on a DM, I kind of forgot.
It's been like, what, a year now since that happened.
But it's just, you know, users are going to be users and they're going to do stupid shit.
And they're not going to read the fine print.
So with custodial solutions, like all these things are resolved because you got mulligans, right?
Like the user's activity can always be resolved because the user doesn't have Bitcoin, has IOUs or some form of that.
And so the custodian can sort of like fix the mistake.
You know, with all the self-custody solutions or semi-self-custody solutions, you don't get backseas, right?
Like you're kind of having to handle all the scenarios.
Like I can see like splicing should probably help if you receive too much coin in your, because you can now break them apart, right?

Speaker 6: 01:31:33

Yeah, it's just that whenever you were using splicing and you're going to receive too much, we're going to splice those in.
And we can do that zero-conf because we know we're not going to double spend ourselves.
And the user, If they want to send those funds out, why did Zeroconf are trusting us?
But they can just wait and they can just wait for a transaction to confirm.
Or if they want to do to you to be completely self-custodial, they just have to turn off Zeroconf in the wallet.
And then the wallet is completely non-custodial.

Speaker 2: 01:32:05

They

Speaker 6: 01:32:05

have to wait a bit when things are confirming but with splicing it makes it much easier to tell users how much fees they need to pay on chain for things to be confirmed soon.
They will have better control on the on-chain fees of all their swaps, all their splice basically.
And yeah, it's gonna give more control to the users while making it simpler for them and making usability better.
So I'm really excited about this.
This is gonna be a very big upgrade for usability for mobile wallets and I think for notes as well.
So I hope everyone will follow in and also implement splicing and start leveraging it.

Speaker 0: 01:32:41

So when do I get my update?
Like two weeks for splicing on my Phoenix wallet?

Speaker 6: 01:32:47

If you want it on the testnet, I can give that to you in two weeks.
If you want it on the fenix net, it's going to be definitely this year, hopefully before the end of the summer.

Speaker 0: 01:32:55

Because my Fenix right now has a Bitcoin mempool is full and fees are high.
See how Fenix is affected.

Speaker 6: 01:33:02

You're going to pay a lot.

Speaker 3: 01:33:04

It's still operational, though.
Some other wallets had to completely shut off because, you know, they weren't so keen on full RBF and the DeGens definitely solved that debate.

Speaker 0: 01:33:19

Yeah, I know.
I don't know why we still have in this debate comes back.
It's like, it only comes back when the fees are low.
I mean, it's obvious, like it's, you know, like I always say that zero conf Bitcoin is not your Bitcoin.
Like it really is that simple.
So, you know, if you want to do that in your own sort of mixing of UTXOs within your own control, I mean, by all means, like that's great.
But once you send a third party, that's a different story.
So, so anyways, so, so that's really cool.
I mean, so splicing seems to like fix everything.
What other aspects of splicing we have not?
We have about, I'd say, like another like we can still explore a little bit and then we start like closing up.
So like what else should we should we bring up?

## Taproot channels and gossip

Speaker 3: 01:34:04

I wanted you guys to finish up the heuristics because we are switching to taproot channels, right?
I know LND and LDK have championed that.
How does that change with like P2WSH on-chain for unilateral versus P2TR or whatever on-chain.
And then, you know, because Lightning implementations are first other than the DGENs, are the DGENs actually giving more cover to Lightning users now?
Like How did the heuristics adapt and change?

Speaker 5: 01:34:35

I can chime in a little bit on some of that.
And Jeff, you were talking about gossip earlier.
You may be a good one to talk about a little bit further.
But the concept of Tapper channels, I'm excited from them.
I mean, we get PTLCs, it's one step closer to PTLCs, which I'm really excited about.
It's probably still years away, but it's one step closer.
We need Tapper channels for that.
But there's a really cool concept where part of the reason I was able to do my hidden lightning network probing to try to find UTXOs that were part of a lightning channel was because I was using the UTXO set and specifically looking for basically what looked like a multi-sig transaction.
UTXO with a multi-sig output.
Taproot channels, if we start moving towards those and every spend, if we start getting to the point where like every spend is a taproot transaction, then it starts to get harder to distinguish what could possibly be a multi-sig transaction, what could be a lightning channel, and things like that.
The missing piece, I think, is the gossip itself.
If you're opening unannounced channels, that's one thing.
You can make it look like it's just a normal Taproot transaction.
But when you get into Gossip and you publish your transaction, you publish your channel, you're automatically contributing, I am one of the owners of this multi-sig Taproot lightning channel And you just broadcasted everyone that can listen to lightning gossip, which you should assume is you know viewable by the whole world I'm really curious of like some of the Concepts there Jeff you if you know more on some of the gossip V2 stuff in regards to like Tapper channels, you'd be better to be able to explain it.

Speaker 1: 01:36:24

Yeah, I don't know a ton, but yeah, you're correct in that you're essentially doxing yourself by saying, you know, this is my UTXO in the Gossip process.
With the VT, which again is a long way off, and it might be a step between the 1.5. Instead, you're sort of saying, I have at least this much, or I think there's a range of sort of value you have tied into UTXO.
And I guess we didn't really touch on this too much earlier, but the point of actually using a UTXO in Gossip is So it's a denial of service vector, I guess, if you didn't have that.
So if you're freely able to gossip without having to actually lock Bitcoin into a channel, then the gossip network is basically unusable.
So we still want that property.
And so with Gossipy 2, there needs to be a way, it looks like zero knowledge proofs would be the idea to still say that you have Bitcoin locked up, but not saying exactly where it is and how much.

Speaker 6: 01:37:30

Yeah.
I'd say that the state of that proposal is basically zero knowledge proofs, magic maths, details left as an exercise to the reader, but we'll see.

Speaker 3: 01:37:40

So I've kind of declined in my LN whatever, keeping up with it.
Gossip V2, correct me if I'm wrong, is Alex Meyer's proposal that has incorporated mini-sketch or is that 1.5? Okay.

Speaker 6: 01:37:56

Yeah, there are a lot of things about gossip that we need to fix because gossip is Basically the simplest form of gossip we could get away with that was easy to implement.
Nobody is ever satisfied with it, but it's really hard to make it good, to do something that's really good.
So there are a lot of things we'd like to change, but some of these things conflict.
Some of these things don't have a really nice solution for, for example, the ZKP stuff would really need a production grade ZKP library that would be available for everyone.

Speaker 0: 01:38:25

And

Speaker 6: 01:38:26

people still don't know what the system is gonna be the one that people will still care about in two years.
So it's really-

Speaker 1: 01:38:33

Yeah, we did an exploration a while back about that.
And we just, you know, like you said, there just wasn't anything that was, I guess, thoroughly sort of gone through the wringer and tested enough that you'll be, I guess, happy with choosing.
So still a lot of work.

Speaker 0: 01:38:51

Well, I mean, anytime you hear anything that requires a new implementation of a novel cryptographic primitive that is production grade, you add five years.

Speaker 4: 01:39:07

It's a good rule.

Speaker 5: 01:39:08

Yeah.
Even Tapper channels themselves, they in order to broadcast them, you need a gossip chain.
So like we could get There's been some, I think, testing, interrupt testing between it right now.
You can have private, unannounced Tapper channels.
You can't have public Tapper channels yet without a gossip chain.
So that in and of itself, I don't know, could take five years.
Who knows?

Speaker 6: 01:39:31

Yeah, but one of the interesting things with Gossip is that it's not a critical system of lighting, it's something that we can evolve.
If there's a flow in the cryptography here, it's not the end of the world.
It's probably not gonna break horribly, it's not gonna, People cannot lose money because of that.
So there are a lot of ways we can still experiment with things, even though they are not, they wouldn't be ready to put in the signature logic for Bitcoin, for example.
But we can take more dangerous approaches to play with cryptography for the gossip part.
And it's okay if we have to change it entirely afterwards because it's broken.
So it's a good ground for experimentation, but we don't want to waste too much time either on experimenting with too many things that we know won't work in the long run.

Speaker 0: 01:40:16

There you go.
So see if you are a researcher who can make a production grade cryptographic library apply for a grant, you know, that's what OpenSats is for.

Speaker 3: 01:40:27

Just please focus on MuSig too.
Forget about all this ZKP stuff.

Speaker 0: 01:40:31

I am done in MuSig too.
I am a Frost evangelist now.
A fully Frost sold Frost maximalist.

Speaker 4: 01:40:38

Are you Roast sold though?

Speaker 0: 01:40:39

I mean, the Roast can get interested.
Yeah.
No, but the Frost stuff is just amazing.
We won't get into this on this episode, but.

Speaker 3: 01:40:47

We'll have to call Jesse on, I guess.
Jesse Posner.

Speaker 0: 01:40:50

That's right.
I have a strong feeling now that the Frost Fix is everything.
So, so guys, let's start wrapping up then.
So is there, Is there anything that part of this conversation, like you really think that you wish it was like sort of mentioned or discussed?

## Splicing (cont.)

Speaker 4: 01:41:09

Yeah.
The one thing I might just add is that I know that I think one thing about splicing is it has so many benefits.
You could probably talk for many, many hours about it.
So I was gonna touch on that.
Like one of the things I wanted to get to just briefly is-

Speaker 0: 01:41:21

Please do.

Speaker 4: 01:41:22

The big Lightning routing nodes, I think they're actually most excited about splicing.
And a couple of reasons, like we were talking about how, if you as a consumer have an app that wants to pay for lightning and on-chain, currently they store the funds on-chain, move it to lightning on-demand, that's gonna reverse, you can start on lightning.
Routing notes have the same problem.
They need to be ready to open a channel at any moment if an opportunity arises.
So they end up with this whole pile of just for them dead capital Bitcoin sitting on chain waiting to deploy into and at risk waiting to deploy into a new channel.
It was splicing.
You can store that dead capital in a chain of channel And you can instantly move it out of your lowest quality channel into the new opportunity at any moment.
So like there's this dead capital problem that is just eliminated by splicing, which I think is a pretty big deal.

## Signing, UTXOs and pre-signed splices

Speaker 0: 01:42:13

So like Could I keep some pre-made UTXOs code for this somehow?

Speaker 4: 01:42:24

Oh, that's an interesting question.
You would need your peer to be on it too, right?

Speaker 1: 01:42:28

But-

Speaker 0: 01:42:29

It's like, Let's say we're both like big liquidity providers, right.
Or whatever.
Or you're a big wallet and I'm a big liquidity provider.
So, you know, we have some, and we have some off like a side channel sort of like coordination as well.
Right.
And you know, I want to use some proper HSMs on my end.
So do you, cause you know, say we have like, you know a hundred thousand coins to make liquidity for Bitcoin lightning, you know we definitely don't want all that money to be hot.
So we, but we want to also like pre prepare things.
So they're kind of like ready to go to leave the HSM and go somewhere else.
Is there anything interesting that can be done here?
Yeah, there's a couple of

Speaker 4: 01:43:08

things like you could pre-sign, people talk about pre-signing splices, which is a little wild.
And in theory, you can pre-sign a splice to close when that spec exists.
But the other direction you can go is with the VLS remote signer stuff.
So this is be like a the equivalent of a cold card, but plugged into the internet that like has its own signing rules.
And it's like a remote key for the for the server.
Personally, if I had a lot of money in there, I would want multiple of those in a multi-sig.
I want like five, it's a lot of money, 10 of those in very different locations.
And they would auto sign for certain things that I pre-approve and then not for other things in a multi-sig quorum.
But you can, you can kind of do both.

Speaker 0: 01:43:45

I mean, technically you could do that with CK bunker right now.

Speaker 4: 01:43:49

I'm pre signing stuff out of a channel.
So that T Bass was talking about, God, I think like two years ago.
And the idea being that like if I could just correct me to best, but the idea being, they had a lot of people that would open the app, get a channel from them and then never come back.
And then they had to force close those channels, which was expensive.
And if they had a had done a pre-signed splice that they just held on to at a lower fee, that would allow them to get, like, you know, the bulk of the money back at a lower fee.
And maybe that could solve the use case you're talking about, NBK.

Speaker 0: 01:44:21

Oh, that's cool.
Because it is a challenge, right?
Right now I was talking to a player who might be a very big liquidity provider in this space.
And, you know, like due to how, not regulation, but just like how you have to, the stuff for enterprise, you know, they're going to end up using Amazon HSMs and sort of like get stuck in that world, which is a world of pain and sorrow and is not secure and it has no privacy.
So like, I don't know, like I still, like I haven't moved into this space because I still don't see a technical solution on the hardware side, aside from the current cold card HSMs, The CK bunker, right?
Aside from like, it's not quite there.
Like what we can do to provide a meaningful improvement.
Because we can keep stuff cold or even USB connected via Tor, right?
Like safe enough.
But the Lightning solutions don't take advantage of that in any sort of sane way.
So I don't see any point.

Speaker 4: 01:45:22

I think that the big challenge is the transaction you publish might end up being justice.
If it's stale, you're going to get screwed, lose all your money.
So like the, you end up needing to have an awareness of the whole blockchain and network to use a transaction safely Which you can do too, right?
It's just it gets it gets complicated.

Speaker 3: 01:45:38

Well, yeah, exactly I was just about to touch on like the VLS project and this is like the ambitions that they have essentially right But when you are adding all this complexity to that external remote signer, it has like all these other checks about like velocity, whitelisting, blacklisting, other specific peer instances, maybe like time, maybe thresholds.
So it does quickly become, at what point are you just running another like light client or full node?

Speaker 0: 01:46:11

Exactly.
It's just like, I'm still failing to see a sweet spot for the, let's call it like the, the warm, cold available liquidity, right.
That is not necessarily at like full risk.
It's not full risk yet.
Right.
It's not like actually hot, hot, But it's like kind of like ready to go in a slightly different solution that like could put it at, it could move to this other facility that like that would be probably the wallet.
But anyways, that's a part that I'm curious.
I just don't don't know yet where to go.

Speaker 3: 01:46:46

It'd be cool to see CK bunker added to maybe even one of the six base points or if you guys were to hack it together.
I've been trying to nerd snipe some people for

Speaker 5: 01:46:56

a while.
Yeah, I think it just goes back to just like if you're blind signing anyways, then you're at almost the same trust model.

Speaker 0: 01:47:03

That's right.

Speaker 2: 01:47:03

So

Speaker 5: 01:47:04

it's like you have to do all the policy stuff.
And maybe you can still do that.
You know, you can have, I don't know, some secure channel that that it talks to with with your actual running node.

## FROST

Speaker 0: 01:47:15

I mean,

Speaker 5: 01:47:15

it's hard

Speaker 0: 01:47:16

once we have frost that it changes a bit.
Right.
Because now you can have some better thresholds distribution, right?
Of how you move funds, the authorization of the funds.
And those signatures can actually move probably through the Lightning Message Network as well.
I don't know.
It's like this is all like sort of like moon brain for later.

Speaker 1: 01:47:38

Yes.
Let's

Speaker 0: 01:47:41

add Frost to splicing.
Let's go.
That's right.

Speaker 5: 01:47:45

Let's go.
Let's do lightning communication.
Let's do it on Nostr.

Speaker 2: 01:47:48

Let's switch.

Speaker 3: 01:47:48

Frost splices on Nostr in two weeks.
You heard it here first.
That's right.

Speaker 0: 01:47:52

That's right.
Okay, guys, any other things that should be part of this conversation that we missed?

Speaker 1: 01:47:59

Well, I don't know if we touched on this, but there is that swap in potentium proposal.
Oh, yeah.
That Zman, which I believe is splicing.
I'm only vaguely familiar with it.
I read it a little while back.
But I think it's a way to essentially go from on-chain to off-chain and serve that, I guess, like not quite hot manner, if you will.
Is anyone else here familiar with that proposal?

Speaker 3: 01:48:26

I've talked to Jesse Posner, I think Nadav Cohen, and maybe Matt and Steve about it.
That's about it.
Oh, Rindell too.
Rindell explains everything so well to me.

## ecash

Speaker 0: 01:48:41

You know, like when the Galaxy brain gets a little too far, I go, I go, I slide into Rindell's DMs. So, okay, so I think there's one more topic that I'd love to address is the e-cash stuff on top of Lightning that like, to me, it fixes pretty much most of the scalability problems and it makes the custodials to be 10 times better, even though there's two custodials.
You know, how is this affecting like your thoughts around like Lightning, if it is at all?

Speaker 5: 01:49:12

It's a really interesting thing because as someone that's been trying to push as much education and application side Lightning privacy for a long time, Fetiments just kind of come in and almost solve Lightning privacy from a lot of aspects of like, the custodian doesn't know anything about the user or where they're spending or the original source of funds in any way.
So you give up the custodial aspects of it, at least temporarily.
You don't have to leave your coins on there for very long.
You can't do it instantly.
There's still timing analysis and amount analysis to be aware of.
There's IP address leakage, so you've got to make sure you go through Tor, or maybe even something like Nostr as a way to obfuscate the source of network.
So there's still a lot of other concerns.
But if you do it correctly, and you're willing to give up some risk, lots of funds, it's a huge improvement from a privacy perspective.
Now being able to receive into a mint, now you've just effectively got receiver privacy.
And then being able to send that out at any time, at least waiting like a day or so, you send that out and the custodian doesn't know who the original person was.
They don't even know where the source of funds came from, first of all, but then they can't correlate this incoming payment is now correlated to this outgoing payments on Lightning.
It's just a huge step up in privacy.

Speaker 0: 01:50:41

You know, one of the reasons why I bring this up is not because it's just the next new shiny thing.
It's, It's because like, at least to me, like, I really believe that between Nostra and eCash is like where most of the lightning demand is going to come in the next couple of years.
I don't think it's going to be from people, normies trying to buy coffee.
I think it's going to be from this sort of like side technologists trying to address some problems with like very specific solutions.
So like, it's going to be like, you know, people trying to do mining Fetty pools, right?
So like they're Fetty Mint pools for mining.
It's going to be, you know, this kind of like very specific thing that requires the e-cash solution in a way that they're developing.
And it's gonna bring like huge demand for Lightning.

Speaker 1: 01:51:31

It also really touches on the scalability aspect of Bitcoin.
And like you mentioned earlier, not everyone will have a UTXO.
And the Feddy Mintz model where there's sort of these community banks, if you will, and interoperability through Lightning helps solve that.
And like, you know, and this sort of community aspect is also about, you know, how would you onboard people?
Like if everyone's not going to have a UTXO, well, they're going to have to earn Bitcoin, right?
And I really think that's a pretty elegant solution.
Hopefully you see this.

Speaker 0: 01:52:04

I mean, like I was, you know, I always found eCash to be sort of like, kind of like idiotic at like how it was sort of like, like presented and available back in the day, because you never had like an anchor of truth in it.
So, you know, it was kind of like, you know, might as well just use like Fiat.
You know, now that we have like Lightning sort of being the IO for eCash and that be the source of truth for that sort of mint, like it changes everything, right?
Like it makes the thing like fully usable.
And it does, again, it breaks down those ETXOs into smaller units and do not have a footprint on chain until you try to get out of that mint.
So anyways, like I feel like, you know, this is a lot more interesting and a lot more shippable than all that Taro stuff and all the other things that people were trying to do, like kind of like shit coins on Bitcoin.
I don't know.
Like it's a, it caught me by surprise at how fast, especially because of Cashew, the public development of Cashew happened, like how sort of like ahead this is and how usable it already is.
All right, guys, you know, after my e-cash rant there, I think we've reached a good point here.

## Final thoughts

Speaker 0: 01:53:18

So any final thoughts, Jeff?

Speaker 1: 01:53:21

Yeah.
So I think this, a common theme I guess has been on-chain versus off-chain.
And we talked a bit about that quite a bit, and especially as fees are rising and just be able to design protocols with that in mind.
Yeah, I think it's a very important thing.
And there's things we need to do in Lightning to improve that, but we're working towards it.
I think We didn't really touch on much, but like, oh yes, we did talk about like building on Lightning and there's a talk about like coin joining of Lightning, but we didn't talk about onion messages and how that may be sort of a building block in some of these protocols in the future.
So it'd be pretty interesting to see where that goes.

Speaker 0: 01:54:02

Tony.

Speaker 5: 01:54:02

Yeah, yeah, thanks for the conversation guys.
Yeah, I feel like everything has been said already.
So I don't know if I have final thoughts, but I do think, you know, privacy on Lightning is improving, it's getting better.
And I'm really excited about some of the scalable solutions that could very well end up being a very privacy enhancing feature as well.

Speaker 0: 01:54:22

T-Best.

Speaker 6: 01:54:23

Yeah, thanks everyone.
That was fun.
And as Tony said, my conclusion would be privacy on Lightning can already be quite good depending on how you use it.
It's getting better and better.
Splicing is really happening.
A lot of progress has been made the past year.
We've discovered a lot of things, improved a lot of things, and truly there's no open issues anymore.
Basically, we know how to do everything and do everything correctly.
So it's coming and it's gonna be very useful and it's gonna be a very nice building block for everyone.

Speaker 0: 01:54:54

Thanks man.
Dusty.

Speaker 4: 01:54:55

Yeah, I'm just excited for the future.
I think that splicing is here, lightning is getting better and better And there's endless challenges, but we're tackling them all.
I put together a little site if you were looking for more information on splicing.
I got lightningsplice.com and the goal is to put all the resources that help try to explain things to people there in one spot.
So check that out lightningsplice.com.

Speaker 0: 01:55:17

Very cool.
By the way, guys, if anybody has any resources, links or whatever, feel free to just put on the on the chat and we're going to add to the show notes.
Vivek, any final thoughts?

Speaker 3: 01:55:29

Yeah, I just want to say thank you to all of our guests and everyone that's implementing splices.
I think full credit to Dusty on the CLN side.
I think Lisa as well on the LDK side, I believe that's Jeff and maybe someone else.
Jeff, you can chime in on who.

Speaker 1: 01:55:46

Yeah.
So Dodkin's doing some of the permitting work, also fuel funding.
And then Jervis and myself will be our sort of working on splicing, but early stages.

Speaker 3: 01:55:56

Awesome.

Speaker 4: 01:55:56

So you're the splicing guy over there.
Awesome.
Yeah.

Speaker 1: 01:55:59

Yeah.
So next next quarter, Q3 is the goal for sometime Q3 to have it done.
Let's go.

Speaker 0: 01:56:04

Look at that.

Speaker 3: 01:56:05

And then thank you to T-Best as well, who's tested the early interop for these sort of things with like V2 opens and whatnot.
Really grateful for that.
And I believe on the L&D side that someone named Eugene correct me if I'm mistaken but yeah I want to say thank you because there's just too much crap now like we talked about APO, LN symmetry with splices and with music too and then incorporating that into payjoins and then how does that tie in with like other routing pathfinding stuff for mobile with async payments and trampoline, you know?
So there's just-

Speaker 0: 01:56:45

There's a lot of words there, man.

Speaker 3: 01:56:47

Yeah, exactly.
Buzzwords, buzzwords on buzzwords in an ever changing landscape.
So I don't know how you guys do it, but really appreciate your efforts, whether on the app dev side or protocol side.

Speaker 0: 01:57:00

Listen, guys, thank you so much for coming and giving two hours of your time.
I find that these conversations are super important and we need to get the information from the people who actually write the code out to the world.
So it's not just the LARPers sort of like talking about the things and like seared salmon.
Thank you.
No, seriously, guys.
Thank you.
Thank you so much for coming on and talking about all this.
It's always an education for me.
I am not as versed on the lightning things.
So, thank you.

Speaker 3: 01:57:37

Hey, when lightning at a coin kite store?

Speaker 0: 01:57:41

So in a good fashion, like a good enterprise, we are seeking a fully managed solution because there is real customers trying to give us real money and I do not wanna deal with that.
So we, and it's only inbound liquidity which is a nightmare to manage too.
And the invoices are not small.
So, you know, if people are trying to give you a grand like all the time, it's a problem.
So we're, you know, we're working on it.
We're talking to a bunch of different providers and hopefully people take off their, for our hands.
And as we get more versed into non-boomer chain, bunker coin, then we can, we'll do it ourselves.
We have, listen, we have a sea lightning node now running for, I don't know how long, a year or two, still running.
It doesn't connect to anyone, but still running.
So yeah, I do deserve to be called out.
I mean, our store still uses legacy addresses.
But anyway.

Speaker 3: 01:58:39

That's more of like a pitch for people to win our business.
So you can reach out to me or NVK to convince us to use Lightning.

Speaker 4: 01:58:47

You should just get the SegWit address and just go straight to Taproot addresses.

Speaker 0: 01:58:50

Yeah, I mean, we do legacy addresses.
We have never changed the store.
It's just running.
The code is running.
I mean, I think the server has like five or seven year uptime, so I'm not messing with it.
All right, guys.
Thank you so much.
You guys have a great day.
So let us know about your project.
Visit bitcoin.review to find out how to get in touch.

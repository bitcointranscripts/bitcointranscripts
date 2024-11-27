---
title: How Bitcoin UASF Went Down, Taproot LOT=True, Speedy Trial, Small Blocks
transcript_by: Stephan Livera
speakers:
  - Luke Dashjr
date: 2021-03-17
media: https://www.youtube.com/watch?v=rspXF6Gp3-g
---
podcast: https://stephanlivera.com/episode/260/

Stephan Livera:

Luke welcome to the show.

Luke Dashjr:

Thanks.

Stephan Livera:

So, Luke for listeners who are unfamiliar, maybe you could just take a minute and just tell us a little bit about your background and how long you’ve been developing and contributing with Bitcoin core.

Luke Dashjr:

I first learned about Bitcoin back at the end of 2010, it was a new year’s party and I’ve been contributing since about a week later. So I recently got past the decade mark.

Stephan Livera:

So I know you have done a lot of different things in the Bitcoin world, and I know you have different projects running. So one of them is Knots as well. So can you tell us a little bit about that?

Luke Dashjr:

Bitcoin Knots is pretty much a product of the same development process that creates Bitcoin core, but it doesn’t have as onerous the review requirements for things to be merged. And it also preserves some features that have been removed from the mainline core, such as the transaction priority, coin age and all that.

Stephan Livera:

Okay, great. And I know you have been developing in Bitcoin Core for a while, and there are certain things that have you’ve helped progress some of those forward. And I believe it was your suggestion that enabled SegWit to be done as a soft fork as well. So maybe it’d be good now to also just dive into some of the different views on how SegWit got activated, because I think looking back now, there are different visions of how exactly SegWit was activated in the Bitcoin network looking back to 2017. So perhaps if you want to maybe set the scene in terms of how you viewed the lead up to 2017, as I understand there were multiple attempts to raise the block size at that time it was XT and unlimited and a few others. Can you maybe spell out for us your view on what that looks like leading up to 2017?

Luke Dashjr:

I mean, there were a lot of people who wanted to increase the block size mainly as a PR stunt to say, Bitcoin can handle so many more transactions. There was a lot of reason not to do that. And at the end of the day, when we got SegWit made up as a soft fork, a block size increase was included in that sort of a compromise with the big block faction. So to speak pretty much doubling the effective block size that Bitcoin blocks can be. For whatever reason, they didn’t like that. They wanted to have more, I guess they wanted to take control over the protocol rules away from the community. And so they pushed forward with trying to do a hard fork despite that.

Stephan Livera:

And so the view at that time is those people who are more in the let’s call it small block camp, or even in the let’s just keep things the way they are and not change it too much. They, some of them viewed that as an attack, correct?

Luke Dashjr:

Yeah. But SegWit was pretty widely accepted as a compromise between the big blockers and the small blockers because SegWit not only increased the block size, it also enabled lightning to be a lot more effective and secure and that hopefully will eventually help reduce the block sizes significantly.

Stephan Livera:

Yeah, I see. And so by fixing some of the different bugs and for example, transaction malleability and setting up the possibility for lightning and so on, it was viewed like that would be the way forward, but obviously in the community there are now it seems that there somewhat different views on how exactly SegWit was activated. So could you perhaps tell us the story from your perspective, how do you believe SegWit was activated in that time in 2017? I know there were various attempts and different BIPs and proposals made.

Luke Dashjr:

Initially we had configured SegWit activation to be done with the BIP9 version bits, which was an upgrade over the previous model had simply used the version number as an integer for each new feature we’d increment it. And then all the, eventually the old version number would become invalid and all the blocks had to be upgraded. So version bits, the idea was we can just temporarily assign each of the bits for the activation. And then once activation is over, we stop using it. And that way we can have up to 20, some soft forks activating in parallel, which at this point seems like, why would we ever have more than one? But at the time things were speeding up and it looked like that was going to become a possible issue that we want to have multiple in progress at the time.

Luke Dashjr:

So SegWit used this and because of the whole big block controversy, it turned out and there may have been other motives in the middle there, but it turns out the miners decided they were going to, instead of coordinating that upgrade, actually just refuse to coordinate it and effectively stop the upgrade in its tracks. It was never intended to be a way for miners to make decisions about the protocol. The community had already decided SegWit was going to happen. Otherwise you don’t deploy an activation at all, but in any case, the fact that it was relying on the miners to coordinate it meant the miners were able to effectively prevent it. And so BIP9 at that point, pretty much failed. So an anonymous developer named Shaolin Fry proposed that we’ll just fix this by making the signal, it’s no longer optional.

Luke Dashjr:

The miners have to at least no later than a certain date set in the signal or their blocks wouldn’t be valid. And this meant basically close the loophole that miners could refuse to coordinate instead of, they still had the coordination involved, but if they didn’t coordinate then it would still activate anyway. Yeah. And so that was BIP148. At one point it was found that due to some due to a bug in BIP9, it would have to be moved forward and ended up being moved to August 1st. It was very rushed and somewhat risky because of the timeframe was only three to five months, depending on when you first heard about it and very controversial obviously, but pulled it off in the end of the day without any issues at all. Despite everything it had going against it, it still was a complete success.

Stephan Livera:

Yeah. And could you also outline what BIP 91 is? And are there any impact that had there?

Luke Dashjr:

BIP 91, put frank was essentially a 51% attack. The miners collaborated on against the network. The only reason it was acceptable at all was because it was in effect the miners complying with BIP 148. BIP 91 was effectively a way that the miners could say. “Yeah we activated SegWit,” even though they didn’t really have a choice at that point, you know, BIP 148 was just a day or two later.

Stephan Livera:

I see. Yeah. And so this also, I guess, calling back to my recent episode with Matt Corallo, we were talking about this idea of so-called playing chicken with the network. And so I guess that’s one of the concerns that people had, that there could potentially be a split caused in the network. And this is why the idea is you want the miners to come along to help enforce that rule. And so I guess this comes into the topic of what we call forced signaling. And I think that’s essentially what BIP148 was helping achieve because it was basically saying all of the nodes who are running this version are essentially saying, if you do not signal for SegWit, we will not recognize your blocks as valid, right?

Luke Dashjr:

Yeah. I mean, that’s a framing that revolves around BIP 148 and the events of that time, it doesn’t really apply to the current situation where all the miners are friendly and hopefully going to just activate it anyway.

Stephan Livera:

Ofcourse. Right. Yeah. So we’ll get to the Taproot stuff, but I just wanted to sort of get your view on the SegWit stuff in the sense that, you know, for us to,

Luke Dashjr:

I don’t know that I would portray it as a game of chicken though. The users pretty much said SegWit is going to be activated. That’s how it is. That’s not going to necessarily causing networks split the network only splits if miners violate these new rules that the users have decided to enforce.

Stephan Livera:

I see. Yeah. So I guess, and I personally, I’m kind of more in the camp of UASF myself, but I guess the counter-argument would be something like, see, even if all you UASF nodes go off and create your own Bitcoin network, you might not have the same level of hash power and therefore not the same level of security, or maybe even at the start, you might not get that many blocks coming through because you’re just not getting because the difficulty would not have adjusted back down. Right. Well, or how would you think about that? Or would you disagree with that?

Luke Dashjr:

Well, that’s implying, I completely disagree with the premise that UASF splits off at all. I mean, it’s just one more rule that the blocks have to follow to be enforced. Miners can violate that rule, but they could violate that rule tomorrow. If they wanted to, they can violate another rule. If the miners decide to violate rules, that’s just the miners splitting the network that has nothing to do with the actual UASF.

Stephan Livera:

I see. Yeah. Okay. And then moving on in, the event in 2017, could you spell out your thoughts on how you viewed the SegWit 2X aspects? So that was later in the year post SegWit being activated, I guess for listeners who are unfamiliar, it was seen, okay so –

Luke Dashjr:

That was right before BIP 91, which was a few days before BIP 148 activated, they saw that essentially SegWit was going to happen. The UASF was going to work. So they decided they were going to tack on their hard fork as an after effect, or try to anyway, obviously Bitcoin doesn’t work like that. You can’t just force users to do something. So it was a complete failure.

Stephan Livera:

Yeah, of course. And so in your view, was it important that as, as for example, Bitfinex had a B1X token and there was a, B2X token to represent in some sense, a futures market of what people viewed the value of Bitcoin versus the SegWit 2X coin, which never actually eventuated. But the fact that at that time it was something like nine to one in favor of Bitcoin over the SegWit 2X coin of which one was the true Bitcoin. So in your view, was that significant, did that matter at all? Or did that just not really matter?

Luke Dashjr:

I mean, at the end of the day, it would have had the same outcome. I’m not going to say it didn’t matter at all. Obviously it helped get us there quicker. It made it clear before the fact that it wasn’t going anywhere, which I guess that caused them to give up early. But at the end of the day, the users are the final rule on what the protocol is. So it’s not like it would have succeeded without a futures market involved.

Stephan Livera:

Of course. I think another important topic to bring up here at this point is the concept of economic majority. So it’s one thing for people to let’s say, spin up a node, and if they are not actually transacting, if they are not receiving Bitcoin. And then in that act of receiving Bitcoin and saying, yes, I recognize this as valid Bitcoins or no, these are not valid Bitcoins, in that act they are helping in some sense influence the rules of the network. And so I guess the argument from the people who believe that it was not UASF that did it might say, well, okay, that might’ve been a few people on Twitter and therefore they were not actually the economic majority, the economic majority would have been actors like Coinbase and other big exchanges. What would you say to that sort of line of thinking?

Luke Dashjr:

I mean it’s kind of history revisionism. Although we, though everyone implies that the exchanges really, they have to do what their customers want. They’re not really the economic actors, the economic actors are the people who are offering services or products for the Bitcoins. You have to be able to, when you receive the alleged Bitcoins, if they’re not valid, you have to be able to say, no, I’m not going to give you a product or not. I’m not going to give you a service otherwise, you know, you’re not really enforcing anything. Right.

Stephan Livera:

I see. Yeah. And so perhaps the counter argument, and again, I’m more on your side, right. But just for the sake of kind of talking it out and thinking about it, what would it look like? If a lot of users are, let’s say they are naive or they do not understand this aspect of it, and maybe they’re not as engaged in the conversation around what Bitcoin is and thinking about the technical ramifications of what’s going on, they are just an everyday user and they just see on their wallets or on their front end, whether that’s Coinbase or some other front end that they see, Oh, I’ve received SegWit 2X coin. And I think that that’s Bitcoin. What about that?

Luke Dashjr:

That’s a scenario where Bitcoin has failed.

Stephan Livera:

Okay. Fair enough. So then but nevertheless, go on.

Luke Dashjr:

Bitcoin only works because of decentralized enforcement. If it’s centralized enforcement, you may as well go back to PayPal because that’s all you have, except it’s more expensive than PayPal because it’s inefficient, it’s trying to simulate decentralization without actually having decentralization at that point.

Stephan Livera:

I see. Yeah. And I absolutely, it’s important that people take that on and actually treat Bitcoin seriously and try to learn about it and be more actively engaged in how they use Bitcoin. But I guess it’s also, there are a lot of people out there who maybe they are only on a mobile phone or maybe they are not very technically savvy. What’s to be said for those users or potentially, and I know you might not agree with this, but for the people who are lightweight client users?

Luke Dashjr:

Well, hopefully they’re an economic minority at all times. Bitcoin just doesn’t work if the majority isn’t enforcing the rules, there’s nobody else that’s going to do it for them.

Stephan Livera:

I see. Yeah. And in your view then, is it not feasible? Let’s say that there would be enough users who might say, call out a service and say, Hey, they’re not actually valid. They’re not properly, they’re not giving me real Bitcoins. And then maybe everyone stops using that service. And then people go to some other service that is using, you know, true Bitcoin quote unquote.

Luke Dashjr:

I would hope that would occur.

Stephan Livera:

Okay. Gotcha.

Luke Dashjr:

I would imagine if any exchange tried to pass off fake Bitcoins, then they would probably get a class action lawsuit.

Stephan Livera:

Of course. Yeah. That’s what we would hope to see. Right. And I guess the worst case would be like, nobody can natively interact with Bitcoin or very few can natively interact with Bitcoin. And then we end up in this scenario where people are essentially all having to trust somebody else. And obviously that’s a very antithetical to the idea and the very notion of Bitcoin. I also wonder as well, is there a question there around some nodes being more important than others? In some sense, because some actors might let’s say hold more coins. They might be more interested in it. And they might be the ones in some sense, defending the ruleset of the network in a loose sense. Do you understand, do you get what I’m saying there?

Luke Dashjr:

Right. Yeah. That’s back to the economic majority, that economic activity being used, using your node to validate is eventually the weight of your note on the network enforcement. If your node doesn’t validate any transactions that people are using in real economic activity, then to be frank, then node is not doing any enforcement at all. If you notice verifying, you know, if you’re selling products every day for Bitcoins, then you’ve got a lot of push compared to someone who’s only selling something maybe once in a while.

Stephan Livera:

Yeah. Yeah. So more active users and ideally people who are using it to receive Bitcoins, they’re the ones who are in some sense, enforcing the rules, as you’re saying.

Luke Dashjr:

And of course, people who have the Bitcoins and there’s willing to spend it also get to choose who is receiving the most.

Stephan Livera:

Yeah. Yeah. You’re right there. Okay. So are there any other points around SegWit and 2017 that you wanted to touch on? It’s okay. If you don’t, if not, I just wanted to kind of make sure you had your chance to, I guess say your view.

Luke Dashjr:

Yeah, I’m just trying to think. I’m not sure that there was too much else.

Stephan Livera:

All right. So let’s move on then to Taproot now. And so we’ve got this new soft fork that most people want. It’s, there’s been no serious sustained objections to it. Can you spell out your thoughts on the discussion on how Taproot activation has gone so far?

Luke Dashjr:

We had, I guess it was three, maybe four meetings a month or two ago. Turnout wasn’t that great only maybe a hundred people or so showed up for them. But at the end of the day, we came to consensus on pretty much everything except for the one lock-in on time-out parameter, since then a bunch of people have started throwing out completely new ideas, which, you know, it’s great to discuss them, but I think they should be saved for the next soft fork. We’ve already got near consensus on taproot activation might as well just go forward with that. There’s not consensus on the lock-in on time-out, but there’s enough community support to enforce it. I think we should just move forward with that, how it is and just, we can do something different next time. Maybe if there’s a better idea that comes around, but right now that is the least risky option on the table.

Stephan Livera:

And so with the lock-in on time-out discussion, there’s been a lot of discussion back and forth about true or false or other ideas proposed such as, you know, just straight flag day activation or this other idea of speedy trial. Could you just outline some of the differences there between those different approaches?

Luke Dashjr:

The lock-in time-out true is essentially what we ended up having to do with SegWit. It gives a full year that the miners can collaborate to cooperatively, protect the network while it’s being activated early. And if the miners don’t do that for whatever reason at the end, it activates. if we were to set lock-in on timeout to false, and we essentially undo that bug fix and give miners control again. And I mean, it’d be like reintroducing the inflation bug that was fixed not so long ago. It doesn’t really make sense to do that. At the end of the day, it is a lot less secure. You don’t really want to be running as an economic actor, so you would logically want to run lockin on timeout true. And therefore a lot of economic actors are likely to run it true.

Luke Dashjr:

In most of the polls I’ve seen most of the community seems to want true. As far as a flag day, that’s essentially the same thing as lockin on timeout true, except that it doesn’t have the ability for miners to activate it early. So we’d have to wait the whole 18 months for it to activate and it doesn’t have any signaling. So at the end of the day, we don’t really know if it activated or if the miners are just not mining stuff that violates taproot which the difference is whether it’s centralized or decentralized verification at the end of the day, it’s economic majority still, that will matter for the enforcement, but you want to be able to say, this chain has taproot activated. You don’t want it to be questioning an opinion. Yeah. I say, taproots activated you say it. Who’s to say which one of us is right. Without a signal on the chain. We’re both in a limbo where we’re both saying the same thing about the same chain and there’s no clear objective, answer to that question.

Stephan Livera:

I see. And now I know this may be a bit more contentious, but I think there are other developers and other people out there who have made an argument that they think setting lock-in on time-out equals true is quote, unquote, putting a gun to the head of the miners and forcing them to signal in a certain way. What would you say in response to that?

Luke Dashjr:

I mean, are we putting a gun to the miners and forcing them to not mine transactions stealing satoshis coins or whatever? I mean, there’s rules and the miners have to follow the rules. They’ve got a whole year to figure out whatever they need to do to enforce the rules themselves. It’s not any different than any other rule.

Stephan Livera:

Gotcha. And what would you say… Sorry, go on.

Luke Dashjr:

Would you add the inflation bug back? Because we don’t want to force the miners not to inflate.

Stephan Livera:

Of course not.

Luke Dashjr:

Kind of nonsensical argument.

Stephan Livera:

Of course. Sure. And now what about the arguments that, so some people make this argument as well that each party in the system, if you will, I guess if we loosely thought of it, like, okay, you’ve got developers and you’ve got miners and you’ve got users. And if you wanted to sort of think of it, like, okay, each of them can propose things like in some sense, developers can propose and write code and put it up there. And ultimately it’s up to people to run that code. And then I guess there’s an argument that I’ve heard as well. What if you let miners signal it on their own and activated on their own, I guess perhaps that is one of the arguments around LOT equals false. So what are your thoughts on that kind of idea of letting them signal it on their own and then changing? If they do not signal then changing at that point?

Luke Dashjr:

There’s no point to it though. LOT true gives them the whole year to signal on their own. And if they do, then there’s no difference whatsoever between the two. The only question is do they have the ability to refuse to collaborate? And if they refuse to collaborate, does that essentially cancel the soft fork? There’s no reason to ever do false. If they collaborate great, then it works. If they don’t collaborate then it works as well.

Stephan Livera:

Another argument I’ve heard is, Oh, well, another reason to have LOT equals false is if let’s say in this activation period, there is a bug to be found and coordinating the stoppage of the soft fork is easier in a LOT equals false scenario than if we were to go with lot equals true as default. What’s your thought on that?

Luke Dashjr:

First of all, the possibility of finding a bug at this stage is very unlikely. There’s been years of review on this, or at least during development there’s been review. And then even after it was merged, there has been more review. But at this point it’s just sitting there waiting to be activated. It’s not, there’s not really much more review to be done with it. And the next time we’re going to see any possible bugs would be after it’s activated. And then at that point, you know, it’s, after all this is relevant, it’s activated at that point. And the second point thing LOT is that it doesn’t actually make it any easier to cancel it. Sure. You could just not activate it. But if the miners have the trigger, only the miners can not activate it. So you, as someone, an economic user running a full node, then to the day you want to change to different software, you don’t want to allow the miners to activate it. And finally, even in the best case scenario there, you would still have to update again, because you’re going to want to activate taproot at the end of the day, what with that bug fix? It really doesn’t, there’s nothing to gain in that regard.

Stephan Livera:

Yup. Now there is a bit more of, let’s say this is more like a meta or a long-term argument, but this argument that if it is seen, like the developers are unilaterally able to put out this code and everyone just adopts it, is there potentially an argument that in the future, let’s say maybe a large government or a large business could try to bring pressure to bear onto developers in the future to try and co-opt or change the protocol, or somehow sabotage the protocol. Do you see a potential risk in that angle or on that side?

Luke Dashjr:

No. No, not really. The developers, no matter what we release at the end of the day, if the users won’t run it, then it doesn’t have any effect.

Stephan Livera:

I see. Yeah. So I guess the argument then would be maybe something like if there were something

Luke Dashjr:

And again, if users just, if the users just blindly run, whatever developers release, that is another failure scenario for Bitcoin, that’s something that’s a problem no matter what we do with the legitimate soft forks.

Stephan Livera:

Of course. Yeah. And I guess in practice though, not everybody is a software developer, right. And not everyone is. And even for the people who are software developers, they may not be familiar with the Bitcoin core code base. And I guess, it’s a sliding scale, right? There’ll be some who are loosely familiar. And then others like yourself who are much more closely familiar with the code base. And I guess to some extent, people are there’s some level of trust paced placed into people who are maybe a little bit closer to the detail. And so I guess the argument then is something like, well, the reality is not everybody, basically not everybody can review the code, right?

Luke Dashjr:

Right. But we can we can provide honest explanations in the release notes of what this code does. And at the end of the day, no matter what we do with the legitimate soft forks, it does not change what a malicious soft fork or 51% attack rather can attempt to do. Developers are going to put out malicious code. It doesn’t matter. What we do with Taproot with the malicious code is going to be malicious no matter what.

Stephan Livera:

Right. Yeah. And so nevertheless, either way we are reliant on basically somebody and because there’s enough, you know, there’s enough eyes on the code so to speak, there’s enough people reviewing it that if there were, hopefully if there were some malicious code to be inserted that somebody could raise a flag and let everybody know, and then there’d be a warning about it and people would like kick up a stink about it basically.

Luke Dashjr:

You would hope so. But regardless what we do with legitimate soft forks has no influence on that scenario.

Stephan Livera:

I see. Yeah. So I guess the other argument I have heard now is like, so this discussion about if Bitcoin core were to release, let’s say a client with LOT equals false. And then the argument that, you know, another contingent of developers and users who want to go out and do similar to the UASF and release an alternate client with LOT equals true. And so one argument I’ve heard and seen is this argument that look, the average user can’t review all the Bitcoin code, and they would now have to decide whether they want to run this alternate client that does include LOT equals true. So what’s your thought on that aspect?

Luke Dashjr:

I mean, that’s no riskier than running the one with LOT equals false. LOT equals false actually, for other reasons, it doesn’t come too achy hair, coherent view of consensus. It will not, it will not be very useful to people who are on the false client. So for that reason, I think core releasing LOT equals false would actually be abdication of the duties toward the users. Obviously Bitcoin core is provided, you know, as is any way, but there’s this expectation that it’s going to follow what the users want and be, you know, safe use and LOT equals false simply is not safe to use.

Stephan Livera:

Gotcha. And also there’s also the discussion around Bitcoin core and the code in Bitcoin core on dealing with chain splits because as I’ve seen some of the discussion, people go into points like saying, okay, how would you, if there were to be a chain split at that time, a Bitcoin call would have to deal with having like the peer to peer ramifications of finding other peers who are on the same chain you are on and stuff like that. Could you outline any thoughts on that aspect of it, or I guess that’s also why in your view, LOT equals True is the way to proceed with this.

Luke Dashjr:

Oh yeah. I mean, there’s a, that LOT equals true or minimizes any risk of chain splits that only happens if the miners are malicious at that point. But if they are, which they could be again, they could be malicious tomorrow and cause problems. But in any case, Bitcoin core can definitely improve on its handling of such miner attacks, but it’s not really related to taproot or locking on time or any of that. It’s a general issue that could be improved, but it doesn’t really have to be, there’s no reason to link it to lockin on timeout or any of this.

Stephan Livera:

Gotcha. and in terms of the minor signaling ratio or percentage, right. So the current percentage or threshold, rather, probably threshold is the correct term. 95% is the current threshold that I understand. What’s your thought on that level and what sort of scenarios could happen if the hash power were to be more, I guess, evenly split. And it wasn’t just like a one or two blocks kind of thing before everyone figures out, okay, this is the correct chain, and this is what we’re going with.

Luke Dashjr:

Well, I mean, SegWit had 95%, but that was also, you know, that one failed. The current consensus for taproot seems to be around 90%. As long as you’re relying on miners to protect the nodes that haven’t upgraded yet, probably don’t want it to be much lower. You know, I would say 85% at least, but once you get to the after the year’s over and we’re activating, regardless of the miners at that point, hopefully the whole economy has upgraded and we aren’t relying on the miners anymore because that could be kind of messy. So at that point, the hash rate doesn’t matter quite so much.

Stephan Livera:

I see.

Luke Dashjr:

as long as it’s, you know, as long as there’s enough blocks to use it.

Stephan Livera:

Yeah. Maybe let me just take a step here just to summarize that for listeners who are maybe you’re a little bit newer, and you’re trying to follow the discussion. So the point I think you’re making there is that miners are in some sense, helping enforce the rules for the older nodes. So basically because the older nodes aren’t validating the full set of rules because of the way Bitcoin works, the idea is it’s like old nodes still have forward compatibility. And so the old nodes could theoretically be put onto the wrong chain, but the idea is,

Luke Dashjr:

Old nodes essentially become light wallets at that point and sort of get a better view of the timeline overall before any signaling before the miners even have the opportunity to activate you really want the majority of the economy, the economic majority to have upgraded by that point, so that when the miners activate the enforcement of the rules also agrees and is, so you have the majority of the economy enforcing the rules that no matter what the miners activate at that point. For the next year, the miners are, they’re enforcing the rules on the mining side. So if someone were to make an invalid block, the longest chain would still enforce the taproot rules and that by doing that, they protect the the nodes that have not upgraded yet, the light wallets and such after that year is over. That’s why you would hope at that point that the entire economy, you know, maybe plus minus one or two small actors has upgraded and is enforcing the rules. So regardless of what the miners do at that point, the rules are still being enforced and nobody is, you know, at that point, if you lose money because you haven’t updated your full node, though, that’s kind of on you at that point. You’ve had your time, a whole year, to get ready.

Stephan Livera:

Yeah. And so the idea then is, let’s say if somebody had not upgraded at that point, there basically wouldn’t be enough hash power actually pointed at that incorrect chain such that people would be kept to the correct chain, even if there are, even if they are on an old node because of the rule about the most work,

Luke Dashjr:

Well, after the full year, then you’re no longer relying on that assumption.

Stephan Livera:

Yes.

Luke Dashjr:

The miners, if they were to produce an invalid block, then everyone’s expected to use their own full node to reject that block no matter how much work that chain has.

Stephan Livera:

Gotcha. Yep. And so now probably a good point to bring up the Speedy Trial idea. So just for anyone who’s not familiar with that, could you just outline what that is and also what your views are on that?

Luke Dashjr:

Speedy Trial is essentially a new idea where signaling starts basically immediately and pretty quickly three months away from when it starts. But if at any point during that three months, the miners signal 90% or whatever the thresholds end up being then three months after that. So it’s a total of six months into the future. At that point, taproot is considered active. And so this gives us the six months window where, the economic majority has an opportunity to upgrade. And because of the short window, it doesn’t conflict with the sort of, so to speak real plan, the hopefully LOT equals true. They don’t overlap with signaling and if speedy trial activates sooner, great, we don’t even have to go with the regular one. It’s just active in six months. If it doesn’t work that’s okay. We just go forward as if it had never been tried.

Stephan Livera:

So I presume then you’re also in favor of speedy trial then in that case and you’re encouraging other people to go with that approach?

Luke Dashjr:

I think it’s still important that we move forward with the lock-in on timeout true. Just because speedy trial manages to preempt it. That’s okay too. It’s not really an alternative as much as of a cooperative, you know, another way that the miners could activate before the deadline

Stephan Livera:

And while we’re here as well, it might be a good point to talk about BIP8. And as I understand, I think there are some parts about it that you would prefer to change if you were to be writing it today, could you outline that?

Luke Dashjr:

Well, in light of lock-in on timeout false being unsafe, and it really doesn’t have a purpose. If it were solely up to me, I would just remove the parameter and just make it always true effectively. I don’t think it would be right for me to just make that change, unilaterally when there’s still disagreement about that. But if it were up to me, I don’t think that there’s any purpose in having a parameter in there, it should just always be true at this point. There’s no point.

Stephan Livera:

I say. Yeah, just because of the way it’s evolved by now.

Luke Dashjr:

Yeah. And there’s no point adding a bug back in once we fixed it.

Stephan Livera:

I see. Yeah. So I guess if you had, in your view, if you had to think about what is the most likely outcome at this point, what do you, what do you think that would be?

Luke Dashjr:

Considering all the minor support for Taproot I’m guessing that speedy trial might succeed. But like I said, if it doesn’t, that’s fine. If people have to switch to a so-called Bitcoin core with taproot added that’s okay. It might actually be better than if Bitcoin core were to release in the main line release. Cause then it’s the users even more explicitly acting. I think it really should have been released by now with the timeline that had been proposed by the meetings a month ago, but I’m not about to go, do it myself. If there isn’t enough community support to actually get it done, then you know, just one developer isn’t, it’s flawed if it’s not going to succeed in the first place. So I do think, I mean, I’m happy to help the community. Of course, if they want to move forward with this, but I do think it should happen sooner rather than later, we don’t want to wait until after speedy trial and then realize, Oh, we should have done this three months ago or yeah.

Stephan Livera:

You might’ve seen I believe it was Suhas who wrote a blog first. I think his focus — Suhas from Chaincode labs for people who are not familiar. And I believe his overall guiding thrust was he was saying, look, the important thing is to keep the network consensus. I’m not sure if you have any views on that or if you’ve had a chance to read that blog post?

Luke Dashjr:

Didn’t read the whole thing, I did skim through it. I agree that keeping the network consensus is probably very high priority, if not the highest I think LOT true does that.

Stephan Livera:

Okay. Yep. Okay. So I guess those are probably the key points, I think like, at least from my reading of the community discussion, I’m sure people out there, if I missed any few key points, any questions, let me know. Luke, did you have any other points around the taproot activation conversation that you wanted to make?

Luke Dashjr:

Yeah, I did think it was important to point out that the miners aren’t going to be caught by surprise with the requirement for signalling, if they haven’t signaled for a whole year, they’ve had that whole year also to prepare for the inevitable need to signal for, to make valid blocks. So if they have no outlier node somewhere, not even a node because they changed the signal on their own, but if they have an outlier server somewhere that they’re setting the wrong version, and they’ve had a whole year to work out that problem, there’s no risk that there’s going to be an accidental chain split with LOT True. I noticed there’s been a lot of fear being spread about accidental chain splits and all that, but the only way that LOT true would have a chain split, which isn’t really lot true, but the only way chain split would occur at that time is if miners are maliciously, intentionally creating invalid blocks, there’s no risk of an accidental.

Stephan Livera:

Yeah. And so I guess in your view, so I guess if I had to summarize your view, then it’s essentially we should be pursuing the LOT equals true approach. Because that, as you’ve said, maximally reduces the risk of these splits and given that basically there’s been no serious sustained objections to taproot, that’s just the way to proceed.

Luke Dashjr:

Yeah. I mean, we can go ahead with speedy trial too, that doesn’t hurt. But I do think we should be doing both in parallel in case that doesn’t succeed.

Stephan Livera:

Gotcha. Okay. Also while we’ve got you here, Luke, I thought it would be interesting as well, just to hear more about your views around the whole small block approach. And I know this is one of those things where you have been I guess, campaigning for this and agitating for this idea of smaller blocks in Bitcoin. Can you outline some of your thoughts on this and why is that an important thing to pursue?

Luke Dashjr:

Earlier you mentioned users who just want to use a smartphone that that’s pretty much impractical these days because the full node, you have to download and process 350 gigabytes of blockchain size and that’s just way too much for a smartphone. So that ship has pretty much sailed. What would reducing block size now get us? It would hopefully accelerate the return to the blockchain, being manageable as smartphones get better. Right now, the blockchain is still growing faster than the smartphone or any technology improves. So it’s actually getting harder and harder for phones or computers to keep up with it. So reducing the block size would get us to the point where the technology improvements, hopefully if they keep pace will finally catch up to, and maybe someday smartphones will again be usable for a full node. The best we can hope for in the meantime is, you know, people run a full node at home and they remotely access it from their phone.

Stephan Livera:

So in that case what about the idea of using pruned nodes on the smartphone and things like that? Is that a possibility in your mind? Or do you think that even that ship has already sailed?

Luke Dashjr:

That ship’s already sailed. That’s, I was kind of assuming that in the first place cause even with the prune node, you still have to download and process all 350 gigabytes of data. It’s just what it requires to be a full node, even if you prune it.

Stephan Livera:

Yeah, and there are also the battery and internet considerations as well because people are walking around with a smartphone. They might not want to take that kind of battery loss.

Luke Dashjr:

Yeah. And when the CPU is pegged, it’s going to get hot. And that also destroys the phone. Usually if it’s running too hot for too long.

Stephan Livera:

So I wonder then whether smartphone use might not have been feasible, even if, you know, even if it had stayed at 350 gigabytes, just because of the battery and the CPU aspects.

Luke Dashjr:

No, no, because the technology would continue to improve. While, the blockchain grows slower than the improvement. So you would have, it would remain viable if it had written reduced in a reasonably timely manner. It may have actually needed to have been before SegWit, but there was a point in time where the reduction would have preserved that use. I see. I remember back in and I don’t know if it was 2013, 2012, I was actually running a full node on my phone with no problem at all.

Stephan Livera:

And what about your thoughts on, okay, maybe another developer or someone else could come back to you and say, well, maybe we can just make it easier to remote into your home node. Right. So right now a lot of people can do the whole raspberry pi thing with one of the different package nodes.

Luke Dashjr:

That’s pretty much the approach I’ve been looking at lately and working toward I’ve got a, you know, got the whole pairing thing that I have in knots. So there’s a QR code where you can point your phone’s wallet to the QR code and scan it, and then it will automatically connect to your node on the computer that you’re showing the QR code on. But kind of part of the area I’ve been trying to focus more on lately is trying to get it so that people can use Bitcoin as easily as they want to, but still have a full node of their own for security.

Stephan Livera:

I see. And your thoughts on the compact block filter approach?

Luke Dashjr:

That’s just another light wallet. It’s no more secure than the bloom filters. In fact, the existence of that feature it’s harmful because there’s no longer a privacy incentive to run your own full node.

Stephan Livera:

I see. So in your view, you would rather that not exist and you would rather basically people would just all be on their full node at home kind of thing.

Luke Dashjr:

Yeah. And it’s actually less efficient than the bloom filter protocol.

Stephan Livera:

That’s interesting. So why is it less efficient?

Luke Dashjr:

Because now your light wallet has to download the block filters for every block. Whereas with the bloom filters, you just tell your full note at home, you know, essentially this is what my wallet, what addresses my wallet has and your full note at home just tells you, okay, these are the blocks you need to worry about and nothing else.

Stephan Livera:

I see. Yeah. So it’s just, I guess it’s, there’s a privacy trade-off there, but it is less computationally demanding, I guess.

Luke Dashjr:

There is a privacy trade-off if you’re using somebody else’s full node, if you’re using your own full node, then it doesn’t matter.

Stephan Livera:

I see. Yeah. That makes sense to me. I guess longer term as Bitcoin grows, it eventually will hit a point where not every user will be able to hold their own UTXO right. So I guess putting context and some numbers on this, right. So, you know, we’re speaking in March 2021, the the population of the world is about 7.8 billion. And the current estimates of Bitcoin users around the world, it might be something like a 100 to 200 million people, but obviously even then not all those people are using it directly on the chain. Some of those, are just, custodial users, they’ve just got their Bitcoin on some exchange somewhere. So let’s say, you know, over the next call it five to 10 years, we get a big increase in the number of people using Bitcoin. What happens when they can’t all fit it, you know, on the chain?

Luke Dashjr:

I’m not sure, hopefully we’ll have a comparable increase of developers actually working on solving that.

Stephan Livera:

Yeah. Yeah. And because I think, as I understand, even if you were to go with lightning and obviously I’m a fan of lightning, I’m a supporter of lightning it’s even then it might be difficult because by the time you get each person opening or closing channels, then it just, it would just completely blow out the capacity in terms of block space.

Luke Dashjr:

Yeah, I mean, it can do what it can do and then what it can’t do, we can try to solve, but maybe we will, maybe we won’t come up with the solution. It’s hard to tell at this point.

Stephan Livera:

Yeah. So I guess the optimistic view, you know, go on.

Luke Dashjr:

There’s already plenty of work for developers without having to try to look at things like that.

Stephan Livera:

Of course. And so I guess the optimistic view would be something like we have some kind of multi-party channel thing going where multiple people can share one UTXO and then people sort of splice in and out of a channel factory or something like that. And then that allows people to preserve some more sovereignty in their use of Bitcoin, rather than a lot of people having to be custodial users of Bitcoin.

Luke Dashjr:

I haven’t given it much thought, but it’s possible that taproot might actually enable that since it has the, the multi-party Schnorr signatures.

Stephan Livera:

Yeah. And I think another approach I’ve heard of is using like covenants and things, which is, I guess, kind of related with what Jeremy Rubin is doing with CTV. Do you have any thoughts around that kind of approach or using covenants?

Luke Dashjr:

I haven’t given it much thought, like I said, you know, there’s just so many things going on here now that I haven’t really,

Stephan Livera:

Of course. Yeah. I mean, it’s a big world out there and there’s so many different ideas going around. It’s obviously very difficult to kind of maintain with all of that, but I guess maybe that would be another, you know, for some people who maybe they don’t want small blocks in their minds, they might be thinking, well, let’s say we did lower the block size, then it might make it even harder right now for people who want to open and close their lightning channels. And it might not be enough in terms of block space. Because like we also have to remember that lightning does rely on us being able to react accordingly. If somebody tries to cheat us or something goes wrong, we still have to be able to get our transaction, our penalty close transaction or justice transaction in the lightning labs parlance that we still have to get that back into the chain in time. And if the block size was lower at that point, then maybe that’s also another consideration there.

Luke Dashjr:

I haven’t looked at the specs, but my understanding is that lightning does not count the time as long as the blocks are being mined.

Stephan Livera:

Right. Yeah. Cause I think it’s mostly around like relative time time-locking is that what you’re getting at? Yeah. Right.

Luke Dashjr:

Well, not so much the relative time-locking, but just that if, while the blocks are full, that it’s not counting towards your time limit on the penalty. So you have more time if the blocks are full.

Stephan Livera:

I wasn’t familiar with, I’m not familiar on this part of how lightning interacts with Bitcoin. So I probably can’t comment any further there.

Luke Dashjr:

I could be wrong. My understanding lightning is still mostly based on the theory rather than what has been implemented.

Stephan Livera:

Cool. have you, have you messed around, have you used any lightning stuff yourself or you’ve mostly just been focused at the Bitcoin core level?

Luke Dashjr:

Mostly at the Bitcoin core level. I’m not going to say I haven’t used it, but pretty much just to the extent of losing a bunch of testnet coins.

Stephan Livera:

Have you tried that with any phone wallets on lightning or?

Luke Dashjr:

No, I like to understand what is actually happening with my Bitcoin.

Stephan Livera:

Okay. Of course. Yeah. I guess, yeah, it’s good to get a sense of…

Luke Dashjr:

I have a really high bar, I will not even let it touch my Bitcoins if I haven’t looked at the code and compiled it myself.

Stephan Livera:

Right. Yeah. But what if, what if someone just sent you, you know, like 10 bucks on a small lightning wallet or something like that?

Luke Dashjr:

Yeah. I’ve had some people offer to do that. I have should probably figure out something for that. At some point I haven’t taken the time to, I also don’t want to use a custodial lighting wallet. Cause that’s just, in my position I don’t want to set a bad example.

Stephan Livera:

Of course, of course. I mean, you could, you could do…

Luke Dashjr:

If I’m going to do it, I’m going to do it right.

Stephan Livera:

Right, right. Yeah. But I mean, you could use one of the non-custodial ones. There are some out there depending on kind of how much trust or how much self sovereignty you want. There are different choices out there. I mean, things like Phoenix or Breez or, you know.

Luke Dashjr:

Yeah. I’m sure there are, I just haven’t seen much yet.

Stephan Livera:

So I guess with the whole small blocks thing is your hope there that you know, there might be other people out there in the community who agree and help agitate for that idea or are you sort of kind of resigned to like the block size as it is now and the block weight limit as it is now.

Luke Dashjr:

I mean, there’s only so much I can do if the community tomorrow decides that yeah, we’re ready to reduce the block size and sure we can do it. But until that happens, it’s just a matter of, yeah. I think the block size should be lower and right now there’s not enough support. So there’s really nothing more to do.

Stephan Livera:

I see.

Luke Dashjr:

Until other people agree with me.

Stephan Livera:

Yeah. And I guess it, it may be that, you know, large holders of Bitcoin are the ones who are much more able to fully be self-sovereign with their own full node, holding their own keys and things. And maybe to some extent, the people with a smaller stack of Bitcoins are to some extent using more custodial services and things. And to some extent they are more reliant on the protection, if you will, the rewards of the of the wholecoiners or the large coiners.

Luke Dashjr:

Well also you have to consider that even if you have a lot of Bitcoins, if you’re not very economically active with those Bitcoins, you may find yourself at a loss if you’re running a full node. And nobody else is if you’re cut out of the economy because other people have accepted an invalid chain, your Bitcoins, aren’t going to be worth quite as much anymore.

Stephan Livera:

Yeah. I see what you’re saying. So essentially you could be some, even if you’re a whale sitting on, you know, over a thousand coins or whatever, right. And the scenario would be that if a lot of other people out there get tricked into some, you know yeah.

Luke Dashjr:

And then the economy moves on to another chain that doesn’t necessarily recognize your rules. No matter how many Bitcoins you have, you’re still at the mercy of the economic majority. And that is essentially putting what puts the price on the Bitcoin and the value. Even if you’re not valuing it in dollars, it’s still, the value all comes from the economy.

Stephan Livera:

Right? So your purchasing power could be impacted, but I guess it also is about if you are running a business, then you’re regularly doing transactions. And in that sense, you are helping enforce your vision of what the rules of Bitcoin should be out there into the network. And you’re helping influence that in some ways you’re running it as long as you’re running a business or you’re regularly, even if you are regularly accumulating and you’re regularly receiving, well then you are helping enforce in that sense.

Luke Dashjr:

Yes. To a limited extent, obviously it would be very bad if there was a handful of people that made up the whole economic majority.

Stephan Livera:

Yeah, I see. Okay. Yeah. Well it’s very been a very interesting discussion, Luke. I wonder if you’ve got any kind of closing thoughts that you want to leave for the listeners?

Luke Dashjr:

I guess if you are interested in working on Bitcoin core with taproot or getting Taproot activated, join the IRC channels. If you are not necessarily, if you’re not comfortable with your skill in doing it, I can help teach.

Stephan Livera:

Great. Luke, for any listeners who want to find you online, or they’d like to get in contact with you, or maybe they want to follow your work, where’s the best place for them to find you?

Luke Dashjr:

If they just want to follow my work or ask me questions in general, probably best way these days is probably Mastodon or Twitter. My handle is @LukeDashjr, and then on Mastodon that’s @bitcoinhackers.org. If you have, if you have a reason to reach out privately, like there’s some privacy sensitive information, you can always email me directly. It’s just luke@dashjr.org for my email.

Stephan Livera:

Excellent. Well, Luke, I enjoyed chatting with you and thank you for joining me.

Luke Dashjr:

Thank you for inviting me.

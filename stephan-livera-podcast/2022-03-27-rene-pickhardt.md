---
title: Pickhardt Payments & Zero Base Fee for Lightning Network
transcript_by: Stephan Livera
speakers:
  - Rene Pickhardt
date: 2022-03-27
media: https://www.youtube.com/watch?v=WoVPkmT3gjY
---
podcast: https://stephanlivera.com/episode/361/

Stephan Livera:

René, welcome back to the show.

René Pickhardt:

Hey thanks, Stephan. I really practiced pronouncing your name.

Stephan Livera:

Ah yeah, it’s all good. There’s lots going on in the Lightning Network. The network is growing and it’s maturing. And a lot of the work you’re doing is around research and looking at ways to improve that and improve the way we route our payments and getting more reliable payments as well, as I understand you. So do you want to just start off today and give us an overview? Where are we today and how did we get here in terms of the current situation with routing of payments? And then we’ll obviously go into your research.

René Pickhardt:

Yeah. So right now, if you want to make a payment on the Lightning Network, there are basically two situations. Either you have a direct payment channel with the person you want to pay, and then of course you just update the balance in this payment channel, but since it’s already called a network most the time, you don’t have a direct payment channel. So you have to find some way of channels or some amount of channels where you want to forward your payment through or route your payment through the network to the other person. And obviously there’s this question of, Which channels do you choose? And historically speaking, people have mainly looked at what is the cheapest way of delivering this payment, right? Because nodes usually charge a fee to forward a payment. So you can look in the computer science literature and find some algorithms on how to solve this, and people have done this. And I think one issue that many people are discovering and experiencing is that the Lightning Network doesn’t work particularly well for large payments. And even for small payments, you have a certain amount of payments that just fail. And my main argument is that this is related to the fact that we are optimizing for cheap fees and we should maybe look to optimize for other things.

Stephan Livera:

I see. And so there’s this impact then because of the way routing works. And I think it’s also important to distinguish the different ideas. So people who are listening, you might have seen some of the discussion—whether that’s on Twitter or the mailing list or GitHub comments—let’s distinguish between your different focus areas or parts of research, right? Because you’ve got the probabilistic payments and the exact name of your paper versus this zero base fee part. And they’re related, but they’re not exactly the same. Could you just explain that for people?

René Pickhardt:

Sure. So the first observation that we made basically one and a half years ago is something that a lot of people actually observed before us that, as I just said, payments have not a good success rate. And what we did differently is we basically turned this around: instead of making payments and measuring the success rate, we asked the question of, If I make this particular payment, how likely is it that this payment will actually be successful? So we basically center everything around the uncertainty of the liquidity in payment channels, and once we are able to estimate the likelihood, we can actually find a candidate set of channels so that we can route the payment that maximizes our success probability. And this is the entire field of this probabilistic payment delivery that you were mentioning. And then there’s the other question: what people have been doing in the past is they said, Well, if large payments don’t work on the Lightning Network, let’s do some obvious trick. Let’s just split the payment into smaller ones and try to deliver the smaller payments. And I mean, this sounds extremely reasonable and very obvious to some degree, but the question that emerges is, How do you actually split this payment? And then for the sub-payments, which paths do you actually choose? And what we observed is that this is also an optimization problem, the question of, How do you split properly? And this is the second paper where you were looking the title, which is the optimally reliable payment flows. So the title is actually “Optimally Reliable & Cheap Payment Flows”, because I still argue we should not only focus on the reliability that comes from optimizing the success profitability and the uncertainty, but we should also focus on optimizing the fees, of course. But you can answer the question of how do you split the payment properly and which ways through the network to choose for each of these partial payments. And what I was able to demonstrate is that I can basically send pretty large amounts of Bitcoin through the Lightning Network in a very short time. And that’s obviously a big game-changer.

Stephan Livera:

Fantastic, yeah. And so with this whole idea—this alternative approach to routing—and I think you make an interesting point in the Mastering Lightning book where you talk about the difference between path finding and routing. And so that’s also an interesting distinction, but then in this case here we’re talking about the way in which you do path finding. So can you talk to us a little bit about—at a high level—what were some of the differences? Maybe it’s a bit of a How long is a piece of string question, but how much more reliable were the payments using this let’s call it Pickhardt payments?

René Pickhardt:

So it’s actually, as you said, a very diffuse question to answer, because it obviously depends on the exact amount and the exact setting. But what I can say is we did, for example, one test where we set up an LND node. And the new LND node, we put half a Bitcoin on it, opened some channels to random peers using their autopilot, and we tried to deliver this payment to my Lightning node, which certainly had enough inbound capacity. And what LND did is they used their splitting heuristics, sent the first partial payment, found a good path, delivered it, but the remainder of the amount that we wanted to send of a large amount didn’t go through. After a minute LND timed out, so we said, Well, you know what? Let’s give LND a little bit of more time. So we recompiled LND, set the time-out to 10 minutes, which is block time, right? Lightning should be at least as good as on-chain transactions, but even in 10 minutes, LND wasn’t able to find a path through the network to deliver the payment. So what we then did is we used our software on top of LND to compute these candidate paths, and we have been able to deliver this payment. It still took, at that time, two minutes for us to do so, but the reason was that, until two weeks ago, we didn’t know how to do the computation quickly. So out of these two minutes, we basically spend 115 seconds on computing stuff, and now we can boil down this computation to a much faster runtime—basically less than a second. So yeah, this is where our results actually also become very practical, because before we actually only knew how to do it properly, but it still took us quite some time. But now finally I found the way to also speed up the computation and that’s very exciting, obviously.

Stephan Livera:

Right. And so you believe that result would be replicable to the rest of the network, right? Like, if other people running LND or other people running C-lightning were to use this method of route-finding they would also see the same kind of benefits?

René Pickhardt:

Yeah. As we just discussed, there’s basically two results here. One result is that we do this probabilistic approach to path finding, or to optimizing the probability. And then the other question is: once we do this, how do we split accordingly to our optimization goal? And C-lightning, for example, has integrated just the probabilistic part of our results. So it’s basically a one-line code change in their code base that they did by just changing how they compute the cost of a route. And once they did this—they did some experiments—basically, the time for payments to complete was cut in half, the failure rate was cut in half. So the speed obviously doubled, because if you have less attempts on average, you’re faster to deliver the payment. So this one observation to focus on reliability and not only on cheap fees was already a huge improvement. And my claim is, if you now apply this to the question of how do you split a multi-part payment, you actually can deliver really substantial and large amounts. And this is great.

Stephan Livera:

Great. And so, summarizing at a high level, the idea then is you can dramatically improve the probability of that payment being successful. And secondarily, you can compute it faster because you’re having to try less times, because for people who aren’t familiar, and you can tell me if I’m getting this wrong, but the idea is that when you paste that Lightning invoice or you scan it and you pay it, really what’s happening in the background is your client is trying to successfully route that payment through. And it might be literally 15 or 20 attempts or 30 attempts. I think there’s a max of something in that range. And that’s what’s happening in the background when you’re waiting for it to go green and tick and say, Yes, payment made. And so what you’re saying is: that process could even be sped up because you could have chosen it along a better pathway. And I think part of the insight is that you’re looking at where is the liquidity more available? Is that essentially it?

René Pickhardt:

Oh I think you described it better than I could have. No, honestly. So what is happening is that making payments on the Lightning Network is a trial and error process. Maybe I should have said this in the very beginning, right? So we select a candidate way of routing this payment, of delivering this payment, we try it and maybe it fails. And then we have to try another one. We have to basically discard those channels and then say, Hey, let’s find some others and try again. And this obviously also puts a lot of load on the network. So initially, when we presented our results and said, Look, we delivered this substantial amount of Bitcoin over the network and we used the split into some 150 onions, people were like, Yeah, you’re spending the network. You’re just making small payments and going through all different loads. Everybody is complaining. And I’m like, No, no, no, no, no—we are optimizing the probability. What this means is, statistically, we’re using a much lower load of channels on the network overall, because if we didn’t optimize for this, we would fail more frequently until we finally delivered the payment. So there is this sweet spot. Like, you don’t want to split too small, you don’t want to split too large, but if you find the exact split, then this actually puts the least load to the network. Which is also great because, as of now, a lot of nodes are complaining about their channel databases growing because of either spam or just regular fake payments. I mean, what Lightning Service Providers currently are doing, as far as I know, is they’re probing the network very heavily. So they’re just making fake payments all the time to know where the liquidity is, so then if a customer later wants to make a payment, they can actually already select the correct route through the network because they don’t have this uncertainty. And I’m basically making the claim of saying, Hey look, you don’t need to do this aggressive probing—just try to optimize for this uncertainty of the liquidity, and then everything works out of the box just fine enough.

Stephan Livera:

Ah, very interesting. Right. And so there’s a few ideas coming to my mind here. But one example is this idea that, Well, there’s a max number of HTLCs. And so in the case where people are doing a lot of probing, effectively what they’re doing is they’re constructing a fake onion path or they’re constructing an onion that won’t actually resolve, but they’re trying to probe and it’s playing that guessing higher or lower game and figuring out, What is the capacity across these channels? And so in practice, what it might mean is there’s a lot of these inflight HTLCs that are not settled yet, and it takes time for them to settle out. And so what you are saying is: if LSPs and other Lightning routing node participants in the network were to adopt this method—this probabilistic payment method and the optimal, reliable part—they could dramatically improve their success probability without having to do so much probing. That’s the basic idea, right?

René Pickhardt:

That’s the basic idea. What comes additionally is, obviously, every time you make a payment, you learn something about the network, right? This is the entire idea of probing. So even with regular payments, you learn something. And if you look in the implementations, LND has this software part called Mission Control. So they at least save basically every payment attempt that they made on remote channels and store the information. I would argue that currently Mission Control doesn’t use this information in the best way for future payments, but at least they’re trying to utilize this information. My claim is that, using the probabilistic model, you can actually use this information to your best goal. Carsten Otto, for example, he already has implemented a dialect of Pickhardt payments on top of LND where he uses the data from Mission Control. And he produced a flow from his node to my node that had a ridiculously high probability, and this was obviously only possible because he is a routing node and he already has some information about the network and he used it properly in the probabilistic model. And I was very surprised to see his results. So what I’m saying is not only can we use this result for a node that knows nothing to start making a payment, but even for highly active nodes, they can actually utilize the information they observe on the network by just operation to also improve their reliability.

Stephan Livera:

And probably the other big question people are going to be thinking is: what’s the impact of fees? Am I going to be paying so much more in fees if I adopt the Pickhardt payments or routing model?

René Pickhardt:

Yeah. So the thing with the fees here is interesting. I will certainly release a little bit more of code—I’m currently working on a simulation framework that people can actually see this, and the simulation framework is very easy to adapt to actual code on top of an implementation. But I shared a picture on Twitter recently where I said, Look, now where I have this fast solver for these problems, I optimized for fees and I paid something like 0.25% of the amount that I wanted to send in fees—and then I had so many attempts, so many onions, so many failures, I [spent] so much time to deliver this payment to find this really, really cheap route through the network. On the other side, when I optimized for reliability mainly, then I paid 0.4% of the amount in fees—so not even the double amount. But basically I was able to deliver the payment with a very, very high probability, which was in that particular case a thousand times more likely to deliver the payment, which is ridiculous. So you get like a factor of 1000 in reliability asset. You have to take this with a little bit of caution: it depends specifically on the nodes and the amounts that you’re choosing here. And you paid not even twice the fees, right? I personally would always choose the reliability part here. Of course, by the end of the day, you want to find something in between where you optimize for fees and reliability. So you also want to find the sweet spot here.

Stephan Livera:

So just to be clear: as you said, you gave us the 0.25% number and the 0.4% number. That 0.25% number, is that just not using your method? Or are you saying that’s 0.25% actually using that first paper approach?

René Pickhardt:

So the question is: what does my method mean? As I said, my method consists of two things. One thing is of saying, Also optimize for reliability, and the other one is just computing the best split. And when I optimized for fees, I was still optimizing for computing the best split that would optimize the fees. Of course, I had to ignore the base fees in the computation for technical reasons, but I paid them later anyway. So I might have been able to maybe save one or two more satoshis on it because of the base fee, but currently the base fee is very low anyways, so I just neglected it in the computation.

Stephan Livera:

Yeah. And so those numbers—the 0.25% and the 0.4%—how would they compare to just an average everyday user today using LND or C-lightning or ACINQ, Eclair?

René Pickhardt:

That I’m not sure. I would assume that those nodes are probably closer to the 0.25%

Stephan Livera:

In that range, right.

René Pickhardt:

Maybe C-lightning not anymore, because C-lightning already implements the probabilistic approach for path selection. So maybe in C-lightning it’s already a little bit more expensive, but therefore faster.

Stephan Livera:

Right. But, there’s more reliability, so that’s the trade-off there. And as you were saying, it’s like that difference of going from 0.25% to 0.4%, and now you’re getting so much more reliability. And maybe that is actually what enables other businesses to build their business model on this idea of, Hey, now the payments are more reliable, so that’s why we should do it this way or that way.

René Pickhardt:

Yeah. That is exactly the situation.

Stephan Livera:

Oh I’m just actually curious as well: so then this would be a decision mostly to be made by, let’s say, the different implementations, but I guess any user and any business deciding what do I build on—obviously that will then impact their decision too. So let’s say as an example, if you are an entrepreneur building some kind of product and you’re thinking, Okay, am I gonna do it on top of C-lightning? Or am I gonna use LDK? Or am I gonna use LND? There’s a competition there in that aspect, right?

René Pickhardt:

Yes and no. Our entire method is kind of independent of the implementation. I mean, you can compute the optimal solution to this payment delivery problem, and then you can take the result and use the API of any of these implementations to actually deliver the onions. So if you have an implementation of our algorithm, you just need one API code that is Send onion, and then you need to be able to pass the result. And then you can basically use that tool and software to deliver the payment. So you can basically stick with your own implementation. And I think implementations are already signaling interest to implement the stuff that we were doing. The other question, of course, is: who is deciding what to optimize for? I’m proposing [that] there are two very obvious optimization goals. One is the reduction in uncertainty, which increases the reliability. The other one is the fees. And the question is of how do you combine these two? Do you want to put more emphasis on the reliability, or do you want to put more emphasis on the fees? For example, I mentioned Carsten Otto before—the reason why he is mainly interested in our results is he’s running a node where he’s doing a lot of rebalancing. He doesn’t need reliable payments. He just needs to shift liquidity from one channel to another channel, so he will most likely very much focus on fees, putting a lot of pressure to the network, but yeah there’s that, right? So you could shift this to userland where you basically give the user a slider and say—look, I mean, some wallets in Bitcoin do this currently—how much fees do you want to pay? And do you want to be in the next block or do you want to be in the next 50 blocks? I mean, they cannot guarantee you that it’s actually really the next block or the next 50 blocks, but there’s a high likelihood that this will happen. And I think a similar thing can happen on the Lightning Network. That being said, I think there’s other things we can optimize for. So for example, the latency of channels is currently something that at least in the open source version of implementations, nobody is optimizing for. So if you use, so-called, my method of probabilistic payment delivery, I might give you five channels to deliver a payment that go from Norway to Australia to Paris to San Francisco to Frankfurt to actually deliver a payment from Norway to Frankfurt. And it’s very clear that just the Internet traffic of this onion takes a lot of time. Maybe we should optimize for a payment that doesn’t have such a high success probability, maybe just like 1%-2% less, but it goes from Norway to Denmark to Berlin to Frankfurt, because even if you fail, at least you fail quickly. So there’s obviously a lot of other features that we can look at and study to improve the reliability and the user experience of making payments. This is certainly stuff that I’m working on, because my mission in this space is to just improve the payment speed on the Lightning Network in general.

Stephan Livera:

Right. Yeah, it’s an interesting angle. So it’s like that three-way trade-off thing—it’s fees, reliability, and speed, and you’re looking at ways to improve all of those. Now I’m also curious as well: are we calling this Pickhardt payments or probabilistic payments—whatever we’re calling this—if somebody is just using the defaults today, just LND or C-lightning or LDK or ACINQ, Eclair, are there cases where it’s just a strict improvement on that three-way trade-off—you’re either the same or better off. Is that the case?

René Pickhardt:

So I would argue what the current implementations do best is deliver a very small payment, very cheaply. That is basically what the current implementations do. I mean, everybody does it a little bit differently so it’s also very hard to say this in a precise way. As I said, C-lightning already has probabilistic path finding. LDK has implemented it, but I think they don’t focus on that feature too heavily. But I would argue that the probabilistic model and the optimal splitting is in general a vast improvement. That’s what we see in the lab, and that’s also what we saw in the limited mainnet experiments that we have been doing.

Stephan Livera:

Yeah. And I’m not 100% sure, as I’ve read a lot of the different documents and things—if you could clarify this for me? The idea is basically that you can route much larger payments using this method, correct? And so what kind of numbers are we talking about here? So again, I know it’s a bit of a diffuse question just like before, but how much of a size question or difference are we seeing using this method?

René Pickhardt:

That’s the obvious important question here, and I have to dig a little bit deeper into this in order to answer this. And I can actually answer this quite precisely and not diffuse, even though the question seems diffuse. So let us assume for a moment, we would know how much liquidity is in every channel on every side. We know the total capacity, but that’s obviously split in two parts where some liquidity is on one side and some is in the other side, and maybe some is stuck in HTLCs because it’s being used for routing. But let’s assume we would know this with full certainty. Then the question, What amount I can pay to you?, is answered by a computer science problem that is the so-called mincut problem. I can just compute the mincut of this network, and I know that this is the absolute maximum number of satoshis that I can pay to you. So in our studies, it turns out that the mincut is actually defined—in 95% of all cases—by the number of satoshis that you have inbound on your node and the number of satoshis that I have outbound on my node. So let’s say I’m owning two Bitcoin in my payment channels, and you can receive on your channels two Bitcoins. In 95% of all cases, I will be able to deliver my money to you. Assuming I know everything, right? And now the question of course comes is: I’m not knowing everything—how quickly do I find this mincut? How quickly am I able to deliver this two Bitcoins? And what I’m saying is, with our method, we are very quickly able to either deliver it or decide that it’s worth giving up. Because right now what nodes do is they try to split and they give up after a minute pretty arbitrarily. Like, why do you give up after a minute? Of course from a user experience, maybe a minute is like really something that you don’t want to stand at a cashier, but maybe a minute and one second would’ve been the right time. But what we can say is: we try to make the payment, some onions might fail, we update our probabilities, we try another round, and at some point in time, we can say, Well, we can try, but the probability becomes so low that it doesn’t even make sense to try anymore, and then we can stop. And what I’m claiming is that we figure this out pretty quickly.

Stephan Livera:

Yeah. That’s a fascinating result. And so, as you said, that relies on having perfect knowledge of the Lightning Network. And I guess today, that’s not likely. But there is an interesting part—actually I was reading in your paper—it said, This 95% of payment pairs are limited by the local outbound capacity of the sender and the local inbound capacity of the receiving node. And then you also mentioned there’s a motivation for this information to be shared. And so is that sort of similar to this idea of like a route hint?

René Pickhardt:

Yes, exactly. Totally. So there’s two things. So first of all, this 95% measure, that’s the truth, right? Even if we don’t know this, we know in reality it’s still limited by this. So it’s still possible. The question is: do we find it? And my claim is we do find it when we do the computation properly. But the other thing is, of course, we can very quickly or much better improve the chances of finding the answer if we share a little bit of information. So of course I will use the local information of my channels. I mean, if I want to pay you two Bitcoin, it might make sense that you already say, Hey look, I can receive half a Bitcoin on this channel, one Bitcoin on that channel, 0.3 Bitcoin on that channel, and 0.2 Bitcoin on the other channel, and the other ones you don’t even have to try. Like, why would you make me try to figure this out? And by the end of the day, I know, Okay, now on these channels you have this money. Because by the end of the day, I’m gonna figure this out anyway. So it makes sense from a reliability perspective to share a little bit of information. I opened a PR about two years ago based on earlier research results and some intuition that it might make sense to not only share information between my channels and your channels, but also ask our neighbors if they would be willing to share some information—basically proactively. Obviously this has huge privacy implications, and one has to be very careful if you want to do this. That being said, on the other hand, while delivering a payment, I’m learning some information all the time anyway, and I’m probing the network. And people are complaining about spam. So what I have been doing actually in the last week—and it’s funny that you asked about this—is that I have been actually studying how our method improves if we do this sharing of information, and to what degree do we actually have to share information. And what I saw is I had one case where I was able to deliver 0.5 Bitcoin to a node that is kind of far away in the network—I think something like three or four hops—where we just shared the information of our channels and our neighbors, which was I think 0.5% of all channels that we knew the exact balance information, and we were able to deliver the Bitcoin on the first attempt. And this is just crazy.

Stephan Livera:

This is not a small payment.

René Pickhardt:

I mean, right now, if you want to send like a millibitcoin, you try like two or three times. That’s substantially—

Stephan Livera:

And 0.5 Bitcoin is like $20k. It’s like more than $20k that you could send.

René Pickhardt:

Yeah. So yeah, there’s certainly also the need to do more research in this direction. And so far this proposal to the boards of creating a protocol where nodes can share information voluntarily was not picked up very heavily. And I think it makes sense, because at that time it was a suggestion that was more based on an intuition. But I think now we have the tools that we can actually study this.

Stephan Livera:

Now there would be a privacy impact, obviously, if you’re telling people, Hey, this is my channel—I have this channel. I could imagine, let’s say, some chain surveillance firm is running around and just collecting invoices and routing hints off people and then figuring out, Ah, see, I know René’s capacity is this much, and this is his channel output, and this is his—et. cetera. But it is that trade-off of the privacy versus the reliability part of it, isn’t it?

René Pickhardt:

That’s the trade-off. And what I’m currently working on is asking the question of: how much information do I have to share? So being very technical here, the information that is in a payment channel is the logarithm of the capacity. So just to give—in bits—measured entropy, so to give some concrete numbers: what this means is if you have a payment channel of, let’s say, a million satoshis, the uncertainty or the entropy that you have is 20 bits. And I was doing an experiment where I was just sharing 2 bits of information on those channels, and this already improved reliability like crazy. I mean, 2 bits of information is what you would learn by two routing attempts on a remote channel. So what I’m saying is: that’s not a lot of information I’m voluntarily sharing. I’m not giving exact balances out here. So there are these trade-offs that can be made that might be reasonable. What I can certainly say—also from our experiments—is if you optimize for reliability, you learn the least about the network, and you still deliver quickly. Whereas if you optimize for fees, you actually learn much more information about remote channels because you have so many failed attempts, and from all of those, you learn something.

Stephan Livera:

Frivolous attempts, yeah.

René Pickhardt:

Yes. And I can quantify this again in bits of information: I think you’ll learn about twice the information if you optimize for fees instead of reliability, at least on the experiments that I did. That’s quite surprising.

Stephan Livera:

And so there is also an argument here—as you were saying earlier, and we were talking a little bit about this—that you might be improving, it’s like a positive externality of everyone else maintaining smaller channel DBs because of the less spam and the less HTLCs sitting and waiting to be expired out, right?

René Pickhardt:

Yeah. So as of now, I think if you want to be a Lightning Service Provider and you want to basically ensure a high service level agreement—with ignoring our results, you basically have to crawl the network all the time, probe the network and just get this information in order to deliver a high service level agreement. But my case is that if you use our methods, you don’t have to do this as aggressively anymore. You might still do it a little bit, but yeah, that reduces load on the network and your service level agreement might even be better. And you save costs because also this probing costs you quite some money. With our results, you can actually do something like find the optimal way of probing the network. It’s also an optimization problem to be solved. It’s much harder, but I have looked into this a little bit.

Stephan Livera:

Yeah. Okay. One other question: does this impact any other future ideas that might come to the Lightning Network? So as an example, listeners who are interested in, say, privacy on the Lightning Network, they might be interested in ideas like route blinding or trampoline nodes and these concepts. Does using probabilistic payments conflict with any of those ideas? Or is there not really any conflict in your view?

René Pickhardt:

One thing that I found interesting is I was talking to Rusty when he was working on the Offers pull request, and I said, Look, you can use the route blinding to actually give those routing hints. So let’s say I want to pay you, Stephan. When you give me the hints of where you can receive—well, you can give me blinded onions. So I don’t even know on which of these remote channels liquidity really exists because it’s blinded. So of course this interacts with some stuff. And you as the recipient didn’t know which channels I used. So in this way, we reduced the amount of information that is actually being actively shared while still using this information. So this is crazy and mind-blowing that stuff like this is actually possible. If you really think hard about this, it’s like, Wait a second, we kind of utilize this information without actively sharing it, but we still are somehow blindly sharing this? I mean, this is crazy. So yeah, there’s a lot of implications. I think another big one is the problem of stuck payments. Right now, when you send out an onion, the problem with the onion is you only know that it arrived at the recipient if the recipient releases the preimage. But if you do a multi-part payment, the recipient won’t release the preimage, if not all onions or the full amount with various onions have arrived. So if only one node on the network decides not to forward an onion, this entire method breaks. But this is not a me problem, right? This is not a problem of my method. This is a general problem of multi-path payment (MPP).

Stephan Livera:

This is just a general Lightning Network thing today, right?

René Pickhardt:

It’s a general MPP Lightning network problem. So there are proposals to make cancelable payments. Onion messages would be required to acknowledge payments. So what you would do is you would basically send out an onion and the recipient would basically send you a message back saying, Look, I have received this onion. You can cancel another one because that is not coming. So you certainly need protocol updates and improvements, but as I said, this is not a me problem. This is not a problem of our method. It’s just becoming much more visible with our method because now that we do substantial amounts, the chance for somebody not routing onion routes also increases, obviously. So yeah, a lot of these problems are connected in a very surprising and weird way sometimes.

Stephan Livera:

Yeah. I wasn’t expecting that. That’s pretty cool. And so just around one other idea—so we need to talk about this as well—is zero base fee. Now this is another idea. So I think the discussion online can get confused and because it’s the same person talking about these different ideas, they just think, Oh, it’s all the same thing. So can you explain firstly, what’s the normal Lightning—like you’ve got that base fee plus a variable fee. What’s this idea of a zero base fee?

René Pickhardt:

The idea of a zero base fee is that in order for nodes to optimize for fees, especially when they want to split payments—which they want to do at some point in time—it’s very hard for algorithms to compute this if there is a base fee on the channel. There’s some weird mathematical reasons for this, and this is a provable fact. This is not my claim. I mean, I’m saying this so in that sense it’s my claim, but I’m pointing to research of people who basically prove these things like 30 years ago or so. So historically what happened is I was working on this question of how do I make payments more reliable. That’s why I came up with this probabilistic framework and model. And then I was saying, Well, we want to use this to its best, so let’s look at how to split optimally. So I found this min cost flow service that is being used to compute the optimal split with respect to the reliability question. So what was very obvious is to say, Well, can we do the same thing to optimize for fees? Can we just use the same software? Just change the cost function—this one line of code change that C-lighting did—and go back to fees. It turns out—no, we can’t, because there is a base fee. It’s really stupid. So it’s kind of strange because everybody so far was trying to optimize for fees, but then when the payment got too large, they were just arbitrarily cutting the payment into chunks and then saying, Yeah, but each of these chunks, we gotta optimize for fees again. Like, Yeah, but if you select the chunks wrongly, you don’t globally optimize for your fees and the base fee is destroying [the ability] for you to solve this problem. So out of our research, basically a very tiny corollary was to say, Look, it would be better for the Lighting Network if we just set the base fee to zero for everybody, because then we can actually also optimize for fees, which is something that for the last four years everybody always wanted. And we have been very careful. We actually asked on Stack Exchange before we published the paper, why was there ever a base fee in the protocol? Is there a good reason? And Rusty Russell, he answered. He was like, No, we were sitting in the spec meeting and we decided we need something for fees and it seemed reasonable. It’s like arbitrary choice. And if you look in all those PlebNet communities and all those people who run routing nodes, the only thing they talk about all the time is PPM. They’re trying to optimize their PPM all the time.

Stephan Livera:

Which is the variable fee.

René Pickhardt:

And if you look at gossip, 90% of all nodes had a base fee of one satoshi, which was just the default of LND, so nobody ever cared about the base fee until we said, Hey, by the way, the base fee makes optimal routing a really hard mathematical problem—and then it exploded. And they’re like, Yeah, but maybe your algorithm is not good. And I’m like, This is not a problem of my algorithm. I was working on reliability. I was working on optimizing the payment delivery. I didn’t even care about the fees. I was just saying, Hey, the fees was a you problem all the time, and if you want to solve this, then it’s fundamentally difficult independent of what algorithm you choose. But apparently it became highly polarizing. But I think more and more people are understanding this. If you look nowadays about—and the numbers are changing—but I would say a little bit more than a third of all nodes actively set their base fee to zero. You can look this up on lnrouter.app on gossip. So yeah, I assume this will just change over time.

Stephan Livera:

Right. And yeah, it’s interesting. Yeah so I saw that statistic on LN Router, I think off the top of my head it was around 38% of the channels of the Lightning Network. Yeah. And I think something around 35% of the nodes of the Lightning Network.

René Pickhardt:

The capacity, I think.

Stephan Livera:

Sorry, by capacity. One was by capacity, one was by channels. And we’re basically talking about 35% or 38% of the network is already saying, Yeah, let’s just do zero base fee.

René Pickhardt:

Yeah. Of course, if you start a discussion like this, people try to find arguments, especially if they were already convinced. And there might be some arguments that people find, for example, that HTLCs produce a cost if you do a force close on the channel. But honestly, if you start to figure in these costs properly, you’re gonna set base fees much differently than one satoshi.

Stephan Livera:

Right. And actually just to explain that HTLC thing. So I believe this is a concern, I think was it Matt Corallo? And maybe Zman on the mailing list also voiced this kind of concern. And let me explain how I understand it—you tell me if I’ve got this right or wrong. So the idea is these HTLCs, hashtime log contracts, these relate to an in-flight HTLC, and so the idea is that if you are creating a lot of HTLCs, for that to close down on-chain, well it’s gonna be another output. But when you make a Bitcoin transaction, the size of that transaction is very much driven by how many outputs are in that transaction. And so this could lead to the Lightning node operator having to pay a very high fee to actually go to chain—in the case where there is a lot of inflight HTLCs. And so this is part of the theoretical argument of why you should try to charge for that. So, and as I understand, part of your response here is: look at the actual base fee—it’s nowhere near the level required to account for that. Is that part of your argument?

René Pickhardt:

That’s part of my argument. So first of all, you stated the problem absolutely correctly. But I would say my argument goes a little bit further. I would say: when you operate a business, you have some things that cost you money and some things that bring you money, and you don’t necessarily have to charge for everything that costs you money. You can do this on average. You can do this statistically. So what you can do is you can look at the lifetime of a channel, how likely is it for a force close to emerge, and how much traffic would you expect to route in this time? And as soon as the number of revenue that you expect to happen is higher than the number of costs that you expect to happen—like how likely is the force close and how expensive is the force close?—is larger, well then you operate on a profitable business if your estimations work correctly. So what I’m saying is, Yeah, you can include this into the PPM. You just set your PPM accordingly to figure out that maybe once in a month you have force close off your channel and that force close is going to be expensive, because that’s just part of the nature of Lightning. And of course the force close is more expensive if you have more HTLCs, that’s also true. There’s that. The other thing that I think makes our results extremely interesting to node operators in general—what we do is we put actually a cost to the uncertainty of a payment to be forwarded. And what we haven’t talked about in our conversation right now is that the likelihood for a channel to successfully route a payment increases substantially if the channel is larger. So the more capacity or the more liquidity you bring to the network, the better you are from a reliability perspective, because the chance is just higher that you can actually forward the payment. So what this means is you can actually start to charge a higher fee. Right now in the Lightning Network, the fee market is actually really, really weird because everybody can basically dump everybody else. The Lightning nodes try to find the cheapest thing, so you just dump the other person, and then everybody is like—at some point in time—Yeah, but if we do a force close then it’s going expensive, and since we dumped ourselves all the time, we’re actually not running a profitable routing node. On-chain fees are more expensive than what we have. Whereas when you put a cost on the uncertainty, then you actually have a hard limit of how to set the lower bound of your fees depending on how big your channel is. So I would argue—with our results being utilized properly—people can actually charge for reliability, and this creates a healthy fee market. So I would argue: using our results widely on the Lightning Network is actually—it’s hard to say—a win-win situation. It’s a win for the operators because they make more profit, but it’s also a win for the users because they can actually send large amounts still for a comparatively cheap price.

Stephan Livera:

Fascinating. And so basically the point then is: instead of this crazy race to the bottom with unreliable payment amounts and small payment amounts only going through, we could have a Lightning Network where payments are more reliable, can be larger and yeah you might be paying a little bit more for them, but that’s the cost of doing business. That’s the cost of using the Lightning Network. You are transacting with Bitcoin after all—this is better than using fiat money.

René Pickhardt:

By the end of the day, we are having a very technical discussion here right now. But if we go one step back, it’s just really, really crazy to see that we have a decentralized peer-to-peer network where—well, obviously routing nodes are intermediaries—but without the necessity to trust intermediaries, to send amounts of money from A to B—like real money. It’s unbelievable. If you had told me this 20 years ago that I would experience this, this is insanity that we can actually do this. It’s mind-blowing.

Stephan Livera:

Yeah, absolutely. Because the thing is, people compare, say, Lightning Network with credit card payments. So as an example, in the fiat world, let’s say you you’re paying 2, 3, 4, 5% transaction fees, but the trick is the consumer is not the one who’s paying. It’s often the merchant and it’s actually kind of worked into the cost of that coffee or whatever you’re buying. But in the Lightning Network, as you were saying, we’re looking at something in that range of 0.25 to 0.4%.

René Pickhardt:

Well we don’t know how fees will change. When people start to pay for reliability, maybe—there’s still a competition, right? We don’t know where this will end up, but it’s interesting. So for example, I don’t know if you have observed this one routing node right now which is called Zero Fee Routing, this crazy person who basically says I’m routing for free. And this person claims that the operation is profitable. And I had a really, really interesting conversation with that person. The main claim is—and I find this argument extremely intriguing, to be frank—the main claim is the person says, Look, if somebody needs inbound liquidity, they’re gonna pay for it—I open a channel to somebody. I have so much inbound liquidity because everybody is opening channels with me because I’m routing for free. And if somebody needs inbound liquidity, they can request a channel from me and they’re gonna pay. And they pay 2,000 PPM. He announces that on dual funded channels with liquidity that’s currently already on the Lightning Network, but he also does a lot of this actually by hand. Like, people can literally send him a Twitter message and say, Hey, I want to open a channel. And they pay an invoice and he opens a channel—it’s funny. But the thing is, he charges 2,000 PPM. That’s really expensive in comparison to other fees on the Lightning Network. But then the channel is open and their money flows in all directions all the time. But he got paid. The funny thing is—and why I find his argument compelling—is he got actually paid without the uncertainty if this channel is ever being used. If you open currently a channel with somebody and you set it to 2,000 PPM, maybe nobody’s going to use that channel—you never get paid. You open the channel with the sheer hope that somebody might drop there. He doesn’t care anymore. The channel is—

Stephan Livera:

Sorry—I’m a little confused though, René, because how is it that it’s zero fee routing, but then it’s also 2,000 PPM? Could you just explain that difference?

René Pickhardt:

Yeah. So the 2,000 PPM is what he charges for the opening of the channel. So he basically says, I assume you route the entire liquidity that I open to you. And he basically charges 2,000 PPM on the capacity of the channel.

Stephan Livera:

Oh, it’s like an upfront model.

René Pickhardt:

Yeah. It’s an upfront model. He charges for the capacity that he provides, but then keeps his fees at zero. So he certainly got paid—independently whether he routes or not—for the use it’s getting free because it’s free routing, like a lot of people use this node. But the reason why I mention this right now is because what happens is it actually goes a little bit back to the credit card model, because somebody has to pay these 2,000 PPM, and who pays them are the merchants who request the inbound liquidity. So the merchant is just later on putting this back to the customer who doesn’t pay routing fees on the Lightning Network. So it’s kind of funny to observe this, and I’m not sure if his case actually plays out. I mean, it’s kind of refreshing to see what he’s doing.

Stephan Livera:

Yeah. Interesting. I wonder whether that’s replicable and is that something that would work for him, because maybe he can then become very central in the Lightning Network. Because obviously the more central you are the better at routing and so on, but yeah.

René Pickhardt:

Well the question is: how do you define centrality? And centrality, as of right now, was often measured by the fees. But what I’m also claiming is you can also measure centrality by the capacity of your channels, which relates to reliability. So if somebody offers zero fee routing, but just only brings like 10 millibitcoins to the Lightning Network, this node will never be central on the reliability part of the network. This channel will basically be ignored and not be used heavily, because no sane routing node will ever try to send, let’s say, 5 millibitcoins through a 10 millibitcoin channel. The likelihood for this to be successful is just way too low, independent of those fees. So it’s not clear if that person actually becomes central because liquidity actually has to be there. But again, that’s a market at some point in time.

Stephan Livera:

Yeah. Right. Okay, so just turning to some other questions just around the Lightning Network just generally—and maybe this is also related to what we’ve been talking about—is we’ve seen this big growth in the number of Bitcoin on the Lightning Network. Do you believe some of that could be an attempt to overcome poor routing algorithms by just throwing liquidity at the problem?

René Pickhardt:

Well, I’m a researcher and I’m a little bit more skeptical on a lot of things. So first of all, I would doubt this notion that we have seen a lot of liquidity being put on the Lightning Network. If we’re being honest, I think as of right now, that’s not even 4,000 Bitcoins. I mean, that’s the number of Bitcoins that’s being mined in like what, five days? That’s like literally nothing. So there’s way more liquidity that can be put on the Lightning Network. Another thing that I did is—and I should publish these results, I actually even announced in November last year that I would publish these results—I looked at what I called the routability of the network, and this is basically the expected number of satoshis that two nodes can send to each other using the probabilistic model. So you can compute an expectation value by just looking at the amount that you want to send and looking at the probability if this is being delivered. And the thing is, I did this for several snapshots of the Lightning Network over time. And the funny thing is, while liquidity is growing on the network, the number of satoshis that I can expect between two peers to peer route was actually decreasing. So I would say this indicates a little bit that maybe liquidity is allocated wrongly on the network, or that the liquidity doesn’t grow as much as the number of nodes. I think if I remember correctly and maybe I’m saying something wrong here so please be very careful, but I think I tried to correlate this routability measure with the average liquidity per node, so looking at how much liquidity does every node bring. And what just basically happened is—also over time—this number dropped a little bit. So yeah, it’s a preliminary result, but I’m just saying I’m a little bit skeptical of how the growth is really going here and how things play out. I mean, maybe Lightning Network doesn’t have to be that much. Maybe a lot of money is just for savings and only a small amount of the money in the world is being used for actual trade and commerce and payments—I don’t know.

Stephan Livera:

Yeah. That’s a fascinating idea. And I mean, part of it is also just there’s so many different variables. Like how big are the payments that go through on the Lightning Network? And what about all those people who earn on the Lightning Network? But at a high level, yeah, you could argue that, actually, if the world’s commerce is running on Lightning Network someday—hypothetically—all other things equal, you might say less coin on the Lightning Network is a measure of how efficient it is. Like, you’re doing more with less.

René Pickhardt:

Yes. So there’s two thoughts that I have to mention here, and I hope we do have the time for this. So first there is this phenomenon called Braess’s paradox, which is related to the price of anarchy and selfish routing. And the observation here is: if you have a traffic network—and basically making payments on Lightning is the same as a traffic network with cars and streets—if you have a traffic network, people will selfishly try to find the cheapest route. And the cheapest usually is the one that has the shortest time to travel. So people will do this, and this might emerge into a traffic jam, which overall produces the situation that the network is being congested. So what actually helps to fight this—and this is kind of paradoxical—is sometimes closing a road. You would expect if there’s a lot of traffic, you would build a new road. But in real life settings, we have seen that sometimes closing roads or limiting the amount of traffic that can go through a road actually increases the overall throughput through the network. So this relates a little bit to your conjecture of how things can get more efficient. The other thing is a lot of the behavior of people on the Lightning Network I would say currently comes from the fact that Lightning works best for small payments. When I first had the result of, Hey look, I can send a large amount of Bitcoin, I contacted one of the developers and the developer literally said, Yeah, but we don’t really see payments larger than a millibitcoin on the Lightning Networks. Nobody does this. Nobody uses is Lightning for that, so why do we need this? I’m like, Yeah but I think we got a chicken and egg problem here. I think the reason why you don’t see this is because it’s not working, and I’m pretty sure if it is working, we will see it. So now comes the thing: if we will see people doing substantial amounts of payments and you get paid a nice 2,000 PPM, for example, certainly some people who already have a lot of Bitcoin think they want more of those juicy satoshis and they will put this liquidity on the network. So I expect with better reliability, there’s more incentives to put more liquidity on the network, which in turn produces even better reliability. So networks grow in a weird way and have these effects of—a network is more useful if more participants are there. So this self-enforcement—

Stephan Livera:

You’re saying there could be this virtuous upward cycle, yeah.

René Pickhardt:

I think with Lightning—take my Lightning node: I never tried to be a routing node, but I paid so much in electricity and hosting in comparison to what’s happening with the routing. It’s not working—you have to be crazy initially to do this. But I think nowadays there’s more and more the case coming where we solve these problems, where we’re getting better, where the incentives are just better aligned. And yeah, I think we’re getting there. It takes time. I mean, I was on your podcast like three years ago and I said, Yeah it’s gotta take a lot of time.

Stephan Livera:

Well, here we are. Yeah, we’re still going. But look, I’m excited to see what happens. Of course, it’s probably time to wrap this one up. I’ve got some other ideas, but let’s save those for a future podcast. But I think it would be good—because we’ve spoken about a lot of things—let’s just do a bit of a summary just so people are kind of, Okay, what did I learn from this episode? So let me try and just summarize off the top of my head a few of the key ideas. So one is: a lot of the routing on the Lightning Network today was done in a way to solve for the minimum cost. Min the fee—minimize the fee. But actually, if we’ve done it with this method—this probabilistic payments or Pickardt payments, whatever you wanna call it—this idea is that we may be able to make the payments much more reliable to do bigger payments with only a very small rise in the amount of fee paid, is kind of broad strokes.

René Pickhardt:

At least for now, yes. Fees obviously can change in the future. But as for now, given the current shape of the network that’s what’s happening, yes.

Stephan Livera:

Yeah. And also I guess the other big idea is that this is independent of which implementation you’re using. Like you could theoretically have a plug-in, let’s say, or do it independently of just running the defaults of the major Lightning implementations of today. That’s probably another key point. And then probably the other key point is the zero base fee part. So it’s this idea that, Well, should we question the base fee and actually make that zero to help the efforts around payment reliability and these broader questions we were talking about?

René Pickhardt:

Yeah, though I would still add that zero base fee has no relation directly to reliable payments, because the reliability comes from the uncertainty and the probability. The zero base fee is making it also more easy for people to also optimize for cheap payments.

Stephan Livera:

Right. Yeah. So you’re saying they actually work in independent ways. They are independently valuable.

René Pickhardt:

Yes. I mean, later we want to combine these two. If you look at the actual code that we are producing, we’re actually saying, Look, here’s the reliability part, here’s the fee minimizing part, and we just like combine these two. So in that sense, of course it’s related, but the fee thing has nothing to do with the question of reliability to first approximation. I can find the most reliable payment if I just don’t care for fees at all—I can do that. The question is: is this reasonable to do? Somebody is going be like, Hey, I’m so reliable I’m gonna charge you everything. It’s only one satoshi—the rest is my routing fee. But it’s very reliable!

Stephan Livera:

Right. It’s the most reliable. So you’ve gotta find that sweet spot—that’s really what we’re trying to talk about here.

René Pickhardt:

Yeah. And finding that sweet spot obviously is just computationally much, much, much more easily [done] if everybody drops the base fee. Since most people don’t seem to care about the base fee anyway—if you look at my code, what I wrote, most of the experiments I just compute this on the zero base fee graph of the network. I just ignore the other channels. I mean, if they don’t want to route my payments—sure.

Stephan Livera:

Hey, no one’s stopping you.

René Pickhardt:

Yeah, exactly. That’s my freedom.

Stephan Livera:

It’s a distributed network. It’s an open project.

René Pickhardt:

You’re just never gonna see a payment from me.

Stephan Livera:

All right. Well look, I think that’s probably a good spot to wrap up here. So René, any closing thoughts? Anything you think we didn’t touch on for the listeners?

René Pickhardt:

On the technical side, no, but on the other side, as some of you know for the last three and a half years, I’ve been basically independently trying to work on research questions and trying to get funding from the community. So if you want to support my work, go either to my website, that’s donate.ln.rene-pickhardt.de where you can throw me some sats—over the Lightning Network, obviously. But if you want to do it with large payments and you don’t have an implementation of our algorithm yet, you could still do on-chain. Or if you want to support me more regularly, of course you can also become a patron of mine. And yeah, I’m always searching for opportunities to fund my research.

Stephan Livera:

Of course. Yeah. And I appreciate the work you’re doing, René. I think it’s really cool. Listeners, make sure you check in the show notes. I’ll put the links for René there, so you can go and support him there. And finally René, actually just on Twitter as well. Where can people find you there? What’s your Twitter?

René Pickhardt:

Yeah, just @renepickhardt. And I hope you put the link too, because as I said, last time on the show, it’s really the spelling of the name that’s tricky. Especially now with all the clones going around, and Twitter is really having a hard time fighting those.

Stephan Livera:

Of course, yeah. All right. Well look, thanks very much, René, I really enjoyed it.

René Pickhardt:

Thank you too, Stephan.

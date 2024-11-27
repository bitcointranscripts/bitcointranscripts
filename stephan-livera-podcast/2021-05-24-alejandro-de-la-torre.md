---
title: Coordinating Bitcoin Upgrades With Mining Pools
transcript_by: Stephan Livera
speakers:
  - Alejandro De La Torre
date: 2021-05-24
media: https://www.youtube.com/watch?v=u-W1wz6UNms
---
podcast: https://stephanlivera.com/episode/277/

Stephan Livera:

Alejandro welcome to the show.

Alejandro De La Torre:

Thank you, Stephan. Thanks. Thanks for having me.

Stephan Livera:

So Alejandro, I’ve been trying to get you on for a little while, but it just kind of hasn’t happened, but I also want to, I really wanted to chat with you about some of your work you’ve been doing around taproot activation. And obviously this has come quite some way and hopefully it’s looking like it’s pretty close to being signalled, but I’d like to chat a little bit about your process and what it was like for you. But first of course, let’s start with a little bit about yourself. Can you tell us a bit about your history in Bitcoin land?

Alejandro De La Torre:

Sure. I’ve been in Bitcoin for a while now. One of my startups I was working for an Amsterdam was acquired by BitMain. It was called blocktrail. we rebranded to btc.com. So I’m co-founder of btc.com. I built that out for three years, we became the largest Bitcoin mining pool for two years in a row. We also had a pretty successful wallet and that I left that a couple of years ago to join the same team that co-founded btc.com. now part of the — it’s called Poolin. Now that’s what the new company is called. I joined them — Poolin, we’re the second largest mining pool in the world, we provide also a bunch of nice synthetics and whatnot. So I’ve been in total about five years in the mining space.

Stephan Livera:

So five years in the mining space is a long time, especially because one year in Bitcoin land is multiple years in normal land. And so I know you were helping to coordinate some of the taproot activation, at least amongst miners. So can you tell us how that came about from your perspective?

Alejandro De La Torre:

Yes. Well the whole idea was to, I mean, I was around when SegWit — the whole SegWit, debacle, civil war. It was I was working at BitMain. Well, I mean, btc.com. I was working at BTC.com, Which was owned by BitMain. So, you know, I was, I had a front row seat at of all the debates and all the betrayal and all the very upset feelings a lot of people have with each other. And what I remember what I’ve pinpointed in those days was that there was a very, very clear lack of communication between all parties and especially from the miners to the rest of the world. The reason being that most miners are based in, well, in those days, it was even more now it’s less, but still a very substantial amount of miners are based in mining farms.

Alejandro De La Torre:

Mining pools are based in China or from China. And the rest of the — a lot of the other ecosystem is not in China. So there’s like aside from that issue or that situation of, you know, cultural differences and language barriers, location barriers, right? Location differences, there was also the added thing of the miners also being very — you know, the miners in those days would never, they were just mining this coin that, that was called Bitcoin. They never thought they would have to do something in terms of upgrading anything — mining pool operators. So it was a new thing. So I saw how the communication caused a lot of issues. So I thought, let me just go ahead and jump the gun here before, before any issues started arising, I wanted to quickly find out what the mining pool operators felt about taproot.

Alejandro De La Torre:

I felt I was in a good position because I’ve been working in industry for many years and most of the time has been with Chinese mining pools. Oh, all the time it’s been with Chinese mining pools. So I know all the operators in China of all these mining pools. So I felt like I was in the right position to do this. And so I jumped the gun and created taprootactivation.com. I asked them all, and I was highly, not surprised, but I was very happy to find out that more than 90% of all the mining pools were willing and down to upgrade to taproot. And that’s, that took me actually went quite quickly, which was also quite surprising. Most mining pools you know, all the large mining pools were aware of taproot. They know what it was at least like the main operators of these pools. So it was not too difficult to explain. You know, I just had to basically ask them and yeah, it was a very happy experience.

Stephan Livera:

So let me replay some of that and just add a little bit of a historical context for the newer listeners. So in 2017, we had the culmination of a multi-year civil war, so to speak, or a little internal debate within the Bitcoin world. And as you were saying, there were different tensions that led to that right, as you were saying, some of it was language difficulty. Some of it was, you know, not really having a clear way, you know, because again, Bitcoin has no king or CEO. It’s all about people voluntarily agreeing things or doing things on the network. And that’s basically how things are done in the Bitcoin network. And so then what happened is now with this next soft fork — the taproot soft fork, I think some of the developers were maybe they felt like they were in a position where they had done what they could, but now they didn’t want to be unilaterally deciding on behalf of all the users, all the miners and everyone in the network. And so it had reached that point, and I think it was actually quite a useful thing that you did there to go around and actually start communicating with the miners and actually pull that together. So can you tell us a little bit around the timeline at the time you setup the taprootactivation.com website? Like, what time was that?

Alejandro De La Torre:

Right. So I started the website in November of last year, it took me about a month of work together, all the mining pools. I mean, — at least all the major mining pools and mid-sized mining pools to answer not only was it the Chinese mining pools, but also Western European American pools also answered Russian pools. It took about a month. It was like I said, quite quick that actually, I hope — that brought a lot of attention towards taproot. And I think that then led that to, you know, discussions on how to actually activate.

Stephan Livera:

Yeah. And so I recall, in that prior 2015, 16, 17, there was some debate and discussion around things that were unknown to the rest of the world. So these were some of the things that were happening in the mining world, the whole ASIC boost thing, or some of the discussion about, oh, would it be against the miner’s incentive to support SegWit because that might’ve helped enable lightning. And would that take away mining fee revenue or would that just be seen like a short-term pain for long-term gain aspects? Were there any concerns similar to that this time around with taproot, or was that mostly seen as like a, this is an upgrade for the network nobody’s really losing, it’s a, win-win all round. We’re just going to support it. What was the view?

Alejandro De La Torre:

That was exactly, yeah. That’s exactly the view. Everyone seemed to be down with taproot. It’s a privacy enhancement, upgrade in privacy essentially. It’s a non-contentious software from what I got from what I got it from the mining pool operators at the very least I’m speaking about the mining pool operators of course. No one seems to have an issue with it. So that’s a good thing.

Stephan Livera:

Sure. Yeah. And now I think there was also some discussion around in, and this was perhaps more in the Bitcoin developer community, which, you know, you can see on the mailing list or on IRC discussions where essentially there were debates had about what is the correct way to activate this thing? Because there were some debates and some arguments being presented that, doing this in a forceful way, if you will, or in a way where the users are just unilaterally deciding and not having the miner signaling approach that you know, that this was being coercing against the miners or not in your view, I guess, in your view, professionally, and also in your interactions with other mining pool operators and other miners, what was the view there? Was that seen as being like a coercive thing? Or was it just seeing more like you know, was there a different view there?

Alejandro De La Torre:

That’s a good question. I think the SegWit debate had a very traumatic experience for everyone that was involved in that situation, in that upgrade. A lot of people still have, you know, kind of remember, some bad memories of what happened in those days and in SegWit days some miners, perhaps not, and not in the best way, some of these same initiatives and or miners in those days have different interests. So that was the whole reason why user activated soft forks or UASF was a very good way to upgrade on that day. So those feelings were still around, but the whole idea was to actually kind of heal those wounds. So to speak, I think going through a miner activated soft fork, is a good way, especially for non-contentious soft fork.

Alejandro De La Torre:

So I did not even — for me, that’s why I really pushed forward for taproot for the answers very, very early on before any of the real discussion started brewing, because I wanted to avoid any of this political stuff to start seeping in, into the conversation. I just wanted to quickly ask them — this is called Taproot. Miners knew about it. And look, do you guys want to upgrade? Yes or no? Yes. Cool. That’s it, that was kind of the whole entire idea. I wanted to quickly move forward before any of this political situations started seeping in. So I did not even mention anything about user activated soft forks or anything like that. I still think it’s a very elegant way to move forward with miner activated soft forks. So, yes.

Stephan Livera:

Yeah. Okay. So moving on then. So there was some discussion then around which method would be used also. So there was a discussion around median time passed and also block height. Did you have any thoughts on that particular approach or that didn’t really matter to you from your perspective?

Alejandro De La Torre:

From my perspective, it didn’t really matter for me. The more important thing was these were just kind of like some snippets of the end of the conversation. It was not very interesting for me. For me, it was, you know, all about getting the miners to signal. So we can just activate it through the miners, a miner activated software. I don’t really care if it’s, you know, MTP or block height. It’s fine either way.

Stephan Livera:

Gotcha. Yeah. And also the discussion around alternate clients as there was an alternate client released called Bitcoin with taproot. Now, I guess maybe I’m phrasing that or framing that in an unfair way, because maybe there is no official Bitcoin software. It’s always, you know, “don’t trust, verify”. So to be clear, there’s the Bitcoin core supported release. And then there was another release called Bitcoin taproot. I think that was the name they were giving it. Did you have any perspectives around that or is it a similar theme from your point of view? It’s just, you know, whatever way we need to get this thing activated using speedy trial is good enough.

Alejandro De La Torre:

Well, yeah, I mean, that’s my general point of view, but I still think it’s — there’s nothing wrong with other clients coming into play. I don’t see it as being wrong or bad at all. I think it’s good that other players in the ecosystem want to go ahead and provide an alternative client for anything it’s the whole beauty of this whole system, right. This, you know, there’s always a possibility of a different client. If something doesn’t work, this, we can try this something else. Of course, if we reached consensus to do that. Of course. So, no, again, I was pretty confident after doing the taprootactivation.com survey or consensus effort survey. So I was not very focused on none of these other things, but nonetheless, I don’t think there’s nothing wrong with that. I think it’s great. And the goal of these other guys, or all other alternative clients was to upgrade taproot. So their goal was the same as mine. So how can I be upset with that?

Stephan Livera:

Gotcha. Yeah. And I guess another interesting question might be because — I guess the group who have created the Bitcoin taproot client, I think it could arguably be said they wanted something closer to the BIP8 LOT equals true approach. And so for listeners, you can check out my earlier episode with Luke Dashjr. I think he represents that view. I wonder, is it — well, I don’t know if you know this or not but would, you know, if the existence of this kind of LOT equals true client out there applies some pressure to mining pools to say, Hey, if you don’t support this, well it’s coming anyway?

Alejandro De La Torre:

That’s the kind of viewpoint of of Luke I believe and I guess, I can see his point of view. I can understand what he means there. But I don’t know if I can give you a good answer, because I don’t know if mining pools like saw this alternative client and thought, “oh, we need to do it fast because there’s this…” I don’t think we ever got to that point where that was ever. I don’t think we got to that point. So perhaps if we — in the future if there was another scenario and we get to a point perhaps that would cause them, or lead miners to push the upgrade quicker or whatever, but in this particular situation, I don’t think many pool operators even knew about it, but again, it’s still okay for them to do for Luke do or any of the listeners can do anything they want with bitcoin and that’s the beauty of it.

Stephan Livera:

Right. Yeah, of course. And I guess maybe an alternate view might be more like AJ Town’s view. Now AJ is a Bitcoin developer, also a past guest on the show. And I think he did a blog post recently talking about his views on summarizing some of this conversation around how to activate, how to move forward in Bitcoin and perhaps the way he framed it was more like, look just because a calvalry charge is worked last time, that’s not necessarily what has to happen this time. Right? Hence it seems that this time we’ve got the miners onboard here, so it’s not really as much of — Maybe that’s just not the right approach or the right way to frame it. And people are thinking of it, like that kind of hero’s journey, this small band of people and you get what I’m saying, right. Maybe that’s just not the right way to think about it at this time.

Alejandro De La Torre:

Yeah, exactly. Again, that’s why I — after the taproot activation effort, I knew that the miners were on board from what they told me in private conversations. So I knew that that approach, the other approach that worked in the last upgrade was not necessary anymore. So right now, already more than 90% of all the largest mining pools have signalled for taproot. Most of them are fully signaling some still having some issues, but that approach was not necessary this time around, but this time around the approach that I guess I took was more adequate, just finding out quickly what they wanted and then coming out quick. Bitcoin core really, really was I think, phenomenal coming out with speedy trial as soon as possible. That was the way to go quick [and] efficient. Yeah. So I think that for this particular situation, we didn’t need that strategy. That strategy worked last time. It doesn’t need to work every single time. It might work next time, it might not. But nonetheless it’s still a legitimate strategy last time around, but, sometimes just you know, working together, is also fine, you know? Yeah.

Stephan Livera:

Right. And so with the speedy trial approach, the idea is to have this quick three-month signaling period and have basically two weeks signalling periods. And we are, I think just closing up the second one where we’re not going to get it this time, but potentially if all the pools, if we get enough of the pools signaling in the next period, then we are going to have decided that. And I guess from your perspective, does speedy trial make sense, this idea of having a short three-month period, or did you find, that mining pools had issues getting their software and their nodes working correctly to signal in that version bit? Was there an issue around that or is that you think this is a reasonable way to get it done and would it be useful in future?

Alejandro De La Torre:

I think, well, actually Poolin, the pool that I work for. We did face some issues with the firmware, there was this one particular firmware that was being used by some particular machines. I can’t speak too much about it because it’s just one firmware that we saw this issue in, and I don’t want to call them out, but basically they would be knocked off our pool, which would be a pretty significant amount of hash rate. So we worked, we worked around the clock, the Poolin team actually helped the firmware team to fix that. And now we’re fully signaling, I assume some other pools probably faced something similar. Of course we’re all — the mining pool business is extremely competitive. So, we don’t really share a lot of what’s going on internally with each others backends or whatnot.

Alejandro De La Torre:

So, so, but I assume that’s what happened with some of the pools. I do know that that node softwares people have like custom nodes, mining pools, or mining operators, mining farms have custom node software that perhaps did not have, the ability to signal, which would then knock them off as well, or would knock the block — would knock the signalling ability off the block header. So, yeah. There was some issues with this type of signaling, I guess there could be another way to do it, but you know, the one thing I want to add is that, you know, soft fork upgrades don’t occur very often. Right. You know, the last time, it was four years ago [which was] SegWit, so, you know, you can’t really blame these firmware teams about forgetting about this particular small, you know, subset. This is something that doesn’t happen often.

Alejandro De La Torre:

So, you know, it’s just some normal bumps along the way to get towards the upgrade. Another added thing I want to always say is that the signaling started exactly the same exact day as like a national holiday started in China, you know, in China, this is like the second most important holiday in China after the new year’s. So it was very interesting that the signaling started exactly the same day. All the teams, the firmware team was in vacation, all of the mining pool operators were on vacation, mining farm operators were on vacation. You know, everyone that was in big, everyone was down they were off on holiday. So it was kind of a little bit of a slow start in the very beginning. But yeah, I think all pools — all major pools except BTC.com, Which is kind of ironic because I’m the co-founder of that mining pool, which is very ironic, personally, but nonetheless all the other pools are signaling fully. So I do really think that the next difficulty adjustment epoch will lock in for activation in November, which turns out to be the same time that Bitcoin conference in Miami between 2021 is going on, which will be great because everyone’s going to be in a very happy mood.

Stephan Livera:

Yeah, exactly. So it doesn’t matter what the price is doing. If we’re getting taproot lucked in, well, that’s going to be bullish long-term for Bitcoin with all the new technology and a potential future soft forks that we can get out of that. I also had a quick question around the mining firmware question as well. So again, not singling out that particular manufacturer, but was there a difficulty there in terms of, now, even if that firmware gets updated, then does that mean we’re reliant on all of those individual mining pools or sorry, oh, those individual miners, rather not the pools — going and updating their own machines in that case to then support the ability to signal, or is that something that was fixed at a pool side, like on the pool end, you know, creating the block template and so on.

Alejandro De La Torre:

No. That was relying on the mining farms themselves, which was kind of the reason why it took some, some days for everything to go through, because we had to update the firmware aside that everyone was on holiday. We had to then upgrade the firmware, send it out, get everyone to upgrade. Of course you need to keep in mind that the mining farm operators have firmware programs that update all their machines in one go. Right? So they’re not sitting there and going to every single, you know, 10,000 machine and clicking. So it’s not that difficult once they get the firmware. It’s just a quick update, but still, yes, we were reliant on mining farm operators to update, however mining farm operators, you know, we told them, look, you need to upgrade the firmware. Otherwise you’re going to get knocked off the pool. So the mining farm operator understands that, he doesn’t want to get knocked off. They don’t want to get knocked off the pool. So it’s kind of — that’s the last thing they want. So they upgraded, you know, quickly enough.

Stephan Livera:

Yeah. Got it. And so just in terms of contacting them as well, because I know in the mining world, maybe for people who are not closely into it, not all the players in the mining world are identifiable. Right. Because, because they could just be pointing their hash at your pool. Right? I mean, you might not necessarily have an easy way to contact them.

Alejandro De La Torre:

Yeah. Sometimes we for example, we have anonymous miners and many pools have that feature. So that’s another added issue. Another added challenge that happened to us. Actually, we did, we did have some miners that were, we were not unable. We were unable to contact because we had no contact information for them — that were knocked off, but you know, these anonymous miners, once they find out that they’ve been knocked off, they’re going to find out what happened and they’ll upgrade. So even though we, but we weren’t able to contact all of them, we did contact the main ones. Usually, how it goes is that large mining, farm operators do contact mining pool mining pool, the mining company, like Poolin. They do contact us because they want, you know, special. They’re big farms so they want special deals, like lower fees. They wants, custom support. They want you know, private nodes or whatever. There’s a whole — they would even want us to send them a shirt, whatever it is, they could, you know, it could be anything. So they have a relationship with us, but the smaller anonymous guy, sometimes they’re bigger guys, but sometimes they’re big — the anonymous miners, but usually it’s not very large, but as soon as they get knocked off again, they’re going to find out what’s up.

Stephan Livera:

Yep. And so I think the other interesting aspect here is the competitive part, right? So in some ways, as you were saying before, you are trying to coordinate this upgrade to the network in a voluntary way, but at the same time, you’re interfacing with competitors. And there’s some competitive pressure here too, because let’s say you are trying to, let’s say you want to do the upgrade and you end up having to knock some of your customers off then were you worried that those customers might just say, “Oh, f*ck taproot. I’m just going to go to some other pool that doesn’t want to signal taproot!” Were you worried about that kind of thing. And would that have a competitive impact to the bottom line of Poolin?

Alejandro De La Torre:

That’s a good question. I think that it actually goes down towards another point, which is miners do have ultimately the choice to point their hash rate to this pool or that pool. It’s kind of, I call it a UASF inside the MASF. And that’s also kind of boils down to like, some people claiming that some pools lost some hash rate because they weren’t signaling nonetheless. It is like the overwhelming majority of people felt that taproot is a good upgrade. There’s good feelings. Everyone understands that if we, you know, upgrade Bitcoin with taproot long-term, it’s a good thing for Bitcoin. So all competitors, when — you and listeners need to keep in mind that Bitcoin feeds us, right?

Alejandro De La Torre:

It gives us our business. It is what we do. It is everything, you know, most of us like myself are hardcore Bitcoiners. And then we love this, but it pays the bills. So we understand that if we upgrade and are always looking towards bringing the best towards Bitcoin, because it’s going to ultimately help us and help our business. So with that in mind, I approached all the mining pools and you know, even though we’re competitors, the overarching upgrade to what powers our businesses is stronger than our competitive nature. So we work together in this particular situation. And that’s a beautiful thing. It’s a beautiful thing.

Stephan Livera:

Yeah. That’s cool. It’s good that everyone has some skin in this game and that we all want Bitcoin to be more valuable because that’s going to pump all of our bags. Right? So that’s a cool thing. So in terms of then getting this over the line, so as we speak today, I’m looking at taproot.watch, which is a website that shows the recent blocks, whether they are signaling for taproot or not, and the percentage hashrate. So as we speak today, it says the current total is about 86, just under 86%. But the potential is 95.6%. And I think the only reason that’s falling down, as you mentioned earlier, is the inconsistent signaling. So that’s actually might be down to btc.com as you mentioned, because they are the pool who’s not consistently signaling, but presuming they are able to sort that part out. Then if they are able to solve this out in the next period, then basically we’re very, very high likelihood of getting this locked in. Right?

Alejandro De La Torre:

Yeah. And I really suggest if there’s anyone from BTC.com listening to me and I will tell them this, myself and I have told them this myself, but I will remind them that if they’re in the next difficulty epoch, that everyone is fully signaling and they’re the only ones not signaling, which, if that is the reason why the upgrade fails for the next difficulty adjustment epoch, then that’s going to look very bad for them because it’s a very bad PR, very bad marketing, you know, that’s not going to cause them any favors with the miners that are currently using BTC.com mining pool. For sure. So it really is in their interest to just fix that as soon as possible. So we can get this things locked in and move on to the next step.

Stephan Livera:

Excellent. Well, yeah, hopefully we’ll see what happens there and I presume then let’s say it doesn’t happen for the next signalling period. Well then maybe miners will start pointing their hash power elsewhere to one of the other pools. And so that could also be a competitive impact there on them also.

Alejandro De La Torre:

Exactly. And that’s what I was saying about this mini UASF inside the MASF, you know, the miners do have a choice to switch around pools that are signaling in this case for taproot. The choice is theirs too. So, you know, it’s kind of a UASF, but inside the mining pools nowadays, it’s pretty interesting.

Stephan Livera:

Yeah. So we’ll see I think that’s one of those things where again, when people are new, they don’t understand there’s a difference between a miner and a pool and they’re not necessarily the same thing. Right. So that’s something to understand there. And so thoughts on how future soft forks could go down. Do you think this is a sustainable kind of approach that could be used for future soft forks? The examples could be anyprevout by Christian Decker and AJ Towns has contributed to that too, or potentially the great consensus soft fork cleanup, or there are other ideas out there. Do you believe this is the way that future soft forks could be coordinated?

Alejandro De La Torre:

Yes. I do think this is definitely a good strategy for future soft forks. Yes, I do. Of course, I think this strategy in itself, or this way that we’ve done it with speedy trial, asking the miners, the mining pools and whatnot, I’m pretty confident it’s going to work and I hope it will, but I think this particular way of upgrading Bitcoin through soft fork perhaps only works for a non-consentious upgrade, you know, like Taproot is. So I don’t, I can’t give you an answer for something that might be contentius, but if it’s a non-contentious upgrade, I don’t see why not try the same exact thing we’ve done this time around.

Stephan Livera:

Yeah. That’ll be interesting to see and hopefully, well, I’m personally, I’m hoping we get anyprevout because that will then enable eltoo, which is a more advanced form of the lightning network. But I guess I wonder because taproot has been spoken about for years and years and years, and by now basically there’s been no serious objection to it. Everyone agrees with it. Yeah I wonder what would happen if it were a soft fork that may be, you know, even if it was, let’s say not a contentious upgrade, but just not that many people were going to shout and scream and try and get it happening. What would happen in that case?

Alejandro De La Torre:

Yeah. I wonder — there’s so many. It’s a very difficult task to upgrade a decentralized financial tool — freedom tool, in my opinion, that is Bitcoin. It’s not an easy task. There’s so many different players, so many different interests, so many different points of views, cultures, whatnot. It’s no easy task and, you know, we’re figuring it out as we go along. There’s very smart people working on this right now. And anyone can actually participate in this discussion and this debate. That’s another beauty of this system. You can do it yourself. You can do things yourself. You don’t need to ask for permission from anyone. That’s the beauty of Bitcoin, and you know, I am confident that Bitcoin I’m optimist and I think Bitcoin will — I already think it is successful, but I think it will continue to be successful into the future. And my part with taproot, whatever small it may be, you know, it’s an honor for me to be able to help in this particular situation with what little I can to impulse this project forward into the future.

Stephan Livera:

Yeah. Well, I certainly think it’s a great thing you did with the taprootactivation.com website. And I think from what I can see that was used in discussions to try to say “Hey, look, it looks like we’ve got 90% of the miners on board here. We can try this approach.” So I think it certainly helped. I’m also curious your thoughts on this idea that maybe — we don’t know what the future holds, but could it be that in the future, not all the pools are easily identifiable or easy to communicate with, or do you actually think no, there is an incentive for every large pool to have, let’s say, let’s call it a front desk or someone to talk to, or pick up the phone because they want to be able to do sales and they want to get miners to point their hash rate to them. What’s your view there? Do you think pools will still be easily identifiable into the future five or 10 years from now?

Alejandro De La Torre:

That’s a very good question. I don’t know what the future holds, but there’s a lot of bumpy road ahead that we have. We have pools now, like doing censorship of transactions, you know, not including non OFAC blocks or non-compliant transactions. There’s a whole bunch of new stuff that’s being tried. There’s also the trend of hash rate leaving China. I think 30% of the hash rate will leave China on by end of this year or beginning of next year. So that can also change the whole game because if a lot of the hash rate is let’s say in north America, and then it’s going to be much larger pools in North America, which will then have their own set of rules and whatnot. So I don’t think it’s — the next time we touch upon a soft fork upgrade or trying to do a miner activated soft fork again, if we do get to that point.

Alejandro De La Torre:

I don’t think that the space would be the same at all. I think the hash rate will be more, I guess, decentralized…

Stephan Livera:

Distributed.

Alejandro De La Torre:

Yeah. It’s distributed across the world, so that’s good. That’s a very good thing, in my opinion. And I don’t know, because some pools might not want to play the game, play by the rules. There’s also national mining pools coming into play. I think Iran is trying to do that. I’ve heard of Kazakhstan trying to do that as well. I dunno. There’s also Uzbekistan. I was trying to do that. Pakistan is also trying to do national mining pool or I’m not too sure about that, but, so there’s going to be also national mining pools. So it’s definitely not going to be the same.

Alejandro De La Torre:

And if there is — let’s just focus on the national mining pools, if there are national mining pools and there’s a soft fork coming into play I’m sure the national mining pools will have geopolitical intentions far, far above than upgrading Bitcoin. You know, like I think they will want to coordinate with, I guess, enemy of their country or whatever. So who knows what the future holds. Bitcoin is here to stay. It’s the real deal. Today, the whole entire FUD that was going on. Even the Pope, was talking about Bitcoin mining. Can you believe that? I mean, when I started in 2013, I never thought I would hear the Pope discuss or mention something about Bitcoin. In my opinion, it’s very bullish. I think Bitcoin is the real deal. Otherwise all these large nations religious leaders will not be talking about it. So it’s definitely going to heat up a little bit.

Stephan Livera:

Yeah. That’s an interesting way to put it because yeah if large countries start their own mining pools and, you know, there’s a USA pool and Kazakhstan pool and then Pakistan pool, then yeah. Coordinating upgrades at that point might not really be feasible as in with, you know, via the mining pools. And then maybe it actually does go back to a UASF approach in the future. Who knows. Right? And I guess another idea would be that if there’s a lot more people who are solo mining or unidentifiable hash rate growing over time, do you have any thoughts on that idea? Because right now the pools put it in that block and say, yeah, this was my block. But let’s say there was a growth in the unidentified hash rate. What happens in that scenario? Or do you just think it’s unlikely?

Alejandro De La Torre:

Well, I mean, there is already about 2.5% of the Bitcoin network that is around unidentified hash rate. They don’t, they, they could, there could be private pools from big players. It could be actually solo miners. Huge. There must be. I know a handful over the years of solo — to solo mine in this ecosystem requires a very, very large mining farm, like something out of this world mining farm. But they exist. So yeah, I guess that’s actually quite interesting because perhaps if some, you know, some miners do not want to, you know, mine on this particular nations national mining pool, because it’s required for them to do so. And they might not want to, so they might, you know, just band together and create their own little mining pool or smaller mining pool to mine, and forego any national mining pool requirements. That’s something that can be done for sure. Yeah. That’s really interesting. I’m sure that’s going to happen in the future.

Stephan Livera:

Yeah. And also another idea there is just going back to the national pools idea, depending on the way the political conversations are going, that might also impact which upgrades can be brought into Bitcoin. Right. So it might be, I mean, who knows but if there was some upgrade that was going to bring a lot more privacy to Bitcoin, and let’s say some governments don’t like that, or, you know, that might also become harder to coordinate through the mining side. But again, we don’t know exactly what will happen with that. But I also wanted to ask your thoughts on this whole China bans Bitcoin mining. I mean, obviously this is anyone who’s been around Bitcoin for any serious amount of time. We’ve seen this movie before,

Alejandro De La Torre:

Many times!

Stephan Livera:

At least this current round of it. Can you tell us tell us what happens next in the movie?

Alejandro De La Torre:

Nothing happens. I don’t know how many times I’ve seen China ban Bitcoin throughout my time in Bitcoin. It’s unbelievable. It’s every single year. It’s insane. And yet we have 60% of all the mining going on in China and in China, the only real difference this time, I guess, and this is me you know, this news came out this morning. So you know, there might be clarification some data down the week or throughout the time in the future. But, you know, the only real difference is that it’s a higher up in the Chinese government that spoke about it, but the document that came out was only a summary was not even written by him. It’s not a formal document by anyone. So it’s very early to say. For me, it already looks to me very suspicious that it’s not a formal document.

Alejandro De La Torre:

That was just a summary of the talks. Yes, it was higher up, but, you know, that document doesn’t mean literally it doesn’t mean anything. They just had a conversation about it. In essence, the only real news is that it was that this time around it was a higher up in the government. That’s the real news here. What is going to happen, it’s unfair. I can speak about it from Poolin side, we’re unclear what’s going to happen, but in my opinion, I think it’s already very suspicious that it’s not a formal document. However, I do think the trend of hash rate moving outside of China will continue. I think it might actually boil down to be is China wants to lower the amount of fossil fuel usage in their country, because it makes sense. It does not only make sense for the country of China and the Chinese people but it [does] make sense for the rest of the globe.

Alejandro De La Torre:

So that’s good in my opinion, and this is pure speculation from my end. Right. But I think they might clamp down on mining using, heavy fossil fuels, which already is not too much. In China, most of it, or I think more than half of it is already using hydroelectric power plants or other green sources. So those miners that will have to move, I don’t think there’s enough space for them in China, or I think they will move out of China. And I think that trend is already starting. There’s already — you’re going to see a lot of news coming up about Chinese mining farms, buying land, or doing joint ventures with American mining farms and American mining power producers, whatever.

Stephan Livera:

Yeah. Interesting. So this has been a common criticism that “Oh, see there’s so much hash rate in China. “And there was that natural experiment recently where a lot of the hash rate went offline and some people were trying to infer that actually based on the amount of hash rate that went down, that I think they were estimating that the amount of hash of Bitcoin’s total hash power, it was something like 40% or so in the China region. What’s your view on that? Do you agree or disagree? Do you think it’s higher than that number? You said about 60% in your view?

Alejandro De La Torre:

I think it’s around 60%. Well, it was less, [but] yeah, I think it’s around 60, 65% of the entire hash rate is still coming from China that blackout that happened or that something blew up, some transformer blew up. I’m not too sure what happened. Some power plant blew up and then the Chinese government decided to do a sort of or the local government there decided to check all the other mining farms for fire safety. So there was like a 20%, I think it was around actually the real number was 17% of the total hash rate coming from China was turned off because of this incident. But yeah, I think around 30% of this 65% total will leave China in the next upcoming year.

Stephan Livera:

Interesting. Hey, because that’s been a common criticism and it seems that now is the time that it might actually be distributing further out to the rest of the world. So as you said more into perhaps North America is a likely situation there also wondering what are your thoughts around the whole, because people are becoming more conscious about things like buying carbon offsets and things like that. Do you think that is going to be a common thing for miners?

Alejandro De La Torre:

Yeah. I think it’s going to be a common thing. Yeah. I do think it’s going to be common. The reality is that some of the mining that occurs still in fossil fuel — using fossil fuels, although it’s less and less, but if there is that, then the carbon offsets could be a good option. I think mining pools will start offering that for sure. Yeah.

Stephan Livera:

Yeah. That’s an interesting one as well, because even recently with Elon Musk and all his Tesla, et cetera, talking about the impact of Bitcoin mining, I wonder whether that’s going to become a new angle where Tesla is itself running on, you know, basically receiving a lot of either subsidies or receiving the credits on the basis of the favorable regulation around that. And I wonder whether that’s going to become new grift in the Bitcoin world of basically people who are trying to get those credits, something equivalent to that, but in the Bitcoin world, do you see a scenario like that coming up?

Alejandro De La Torre:

Do you mean like government subsidies for, for miners that are offsetting their carbon?

Stephan Livera:

Yeah. It could be that, or maybe it could be like a regulatory requirement that they do that, or it could be. And then who knows if, maybe in the future that they, if someone tries to come out with a “Oh, see, this is like the green mining things. So therefore I should be receiving credits for this.” Whereas you quote unquote dirty fossil fuel miner, you have to pay me kind of thing, or it ends up acting like a cross subsidy, right?

Alejandro De La Torre:

I think I think that’s sort of strategic — those are all strategies that are going to be played out by business, by mining pool operators and mining farm operators. It’s a very, it’s highly competitive market. Again, I think it’s the most like legitimate or capitalistic industry out there. It’s pure capitalism. And that’s a very good strategy to say that your green farm and get some subsidies in order to beat your competitor, even though you might be just offsetting it or whatnot. Yeah. I think these types of scenarios are coming already are sort of already happening. They’re just building up right now.

Stephan Livera:

Yeah, just anything going on with Poolin and what’s the latest with Poolin?

Alejandro De La Torre:

We have very low fees for miners. We have nodes across the globe. We have many years of experience with large mining farm operators. So if you’re listening in and you’re a farmer, we can take care of you. And we have synthetic mining called Mars project, which is synthetic Bitcoin hashing, synthetic Bitcoin mining, and synthetic Ethereum mining, very easy to jump into. We were the first ones to come out with this sort of tokenized hash rate protocol. And it’s doing very well. So if you’re interested in that piece, go to poolin.com or reach out to me.

Stephan Livera:

Excellent! Well yeah, Alejandro any final thoughts for the listeners there just around upgrading on Bitcoin?

Alejandro De La Torre:

I think… If any of you, if any of the listeners are just normal operators or normal users, I’ve gotten this question many times, you don’t have to worry about upgrading your wallet or anything going wrong with your Bitcoin. You can still send and receive Bitcoin. You’re not affected by the, by the upgraded. The only thing, the only way you’re affected is that it’s just going to become more private and it’s going to become a better Bitcoin. So don’t worry about that. And and I hope everyone listening here gets so some sort of inspiration to not only just buy the coin. And hope that it goes up, but also, you know, build and this is a great industry to participate in. And I think there’s a lot of opportunities here. So, you know, building is also a very good way to move forward.

Stephan Livera:

Excellent. Well, thanks very much for joining me, Alejandro.

Alejandro De La Torre:

Thank you, Stephan.

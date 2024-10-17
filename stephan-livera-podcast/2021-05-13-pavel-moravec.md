---
title: SlushPool Signalling For Taproot
transcript_by: Stephan Livera
speakers:
  - Pavel Moravec
date: 2021-05-13
media: https://www.youtube.com/watch?v=fxRKMUXoCeE
---
podcast: https://stephanlivera.com/episode/275/

Stephan Livera:

Pavel welcome to the show.

Pavel Moravec:

Hello. Great to be here again.

Stephan Livera:

Yes, So, Pavel, I see you guys have been keeping busy over at Braiins and SlushPool. So you were one of the first pools or I think you were the first pool to signal for taproot, which is very cool. And we’re definitely going to get into some of that for listeners who don’t know much about you, can you just give us a little bit of a background on yourself?=. You’ve obviously been around the space for awhile. But can you just tell us a little bit about some of the things you’ve been doing.

Pavel Moravec:

Yeah, of course. The Bitcoin history of mine started in 2013 when me and Jan, my partner in Braiins, we jumped in Bitcoin projects, which started — it was started by Marek Palatinus, just SlushPool. So we basically taken over SlushPool development and everything and this year. Yeah and from that point in time, we spent all our time in Bitcoin space. We got back to our — like historical focus towards firmware development and, embedded development, which we did before in the company Braiins. But from 2013, it was all about Bitcoin going even in this embedded system space. Obviously a lot of time we spent with SlushPool and the server side of mining, but yeah, I’ll a lot of very interesting stuff happened during the years.

Stephan Livera:

So I guess just to summarize some of that for listeners who are maybe not familiar, so Braiins is essentially a Bitcoin mining company and they really focus on basically a full stack. They provide a full software stack and also have SlushPool, which was the first Bitcoin mining pool. So just for listeners, make sure you understand if you’re new, there’s a difference between a miner and a pool, right? They’re actually different entities. But we’ll get into some of that as well, but I’d love to also chat about taproot, what it is and why signaling for it and all of that. So Pavel from your perspective.

Pavel Moravec:

Thanks for correcting me or fulfilling the empty space. It’s you know, you’re living in this environment for so long and you’re having the discussions with so many people that it’s super easy to just forget about the details or…

Stephan Livera:

Yeah, of course.

Pavel Moravec:

You kind of expect that everybody understands how Bitcoin mining works. So sorry for that. But yeah, there is a very huge difference between being a physical miner, somebody who has the machines who needs to think about electricity and all this stuff, this is super tough business. And there is a second part of inside of the same coin being a pool or any kind of service provider for the physical miners. And we as a company, focus more on building tools and services for the physical miners or operators, or there is a lot of names how we can call them. But yeah, it’s a different business. We don’t have any large mining operations ourselves, besides some developments, a mining farm for testing our firmware and stuff like that. Because we, in the middle of Europe don’t have probably the best like electricity prices for running the operations ourselves. But yeah, there is a huge space in this industry to specialize on different aspects of mining. And we are doing the software side and server side more.

Stephan Livera:

Excellent. And so if you’re new and you’re thinking about Bitcoin mining and getting involved well SlushPool is one of the pools that you might consider when you want to, if you’re setting up a miner, you have to think about, well, what’s my electricity costs going to be, what’s my CapEx, what’s my OPEX. And then you have to think which pool am I going to point my SHA256 hashing power at and SlushPool, you know, run by Pavel and Jan and the team are one of the pools that you could point them to. So yeah, I wanted to talk a little bit about taproot and signaling for it and what does all this mean? Right. So just keeping in mind that we’ve got a lot of new people coming into the space. So Pavel, can you just give maybe just an overview from your perspective, what is a taproot and what sort of benefits do you see from this soft fork upgrade to Bitcoin?

Pavel Moravec:

Yeah. Taproot is a super exciting thing. But to keep it easy, Bitcoin has potential for smart contracts, not a lot of people, think about smart contracts in context of Bitcoin very much because there are other chains more known for it — that’s got that feature, but Bitcoin has scripting. And yet Bitcoin is more capable in this area than people understand and taproot is very clever extension of what Bitcoin currently allows to do with, in terms of scripting or building smart contracts right. And it is very nice take how to get some data reduction and huge privacy gains from clever trick made by some cryptographic primitives used by Bitcoin. So essentially, it’s just an algorithm, but it has a huge consequences for privacy on-chain especially in context of smart contracts, where you, as a user of Bitcoin, you can you can arrange credit, complex business or other like contracts and not allow other people to look into the stuff. Even though the chain can double-check that your contract is fulfilled. So it’s maybe, too difficult, even in this…

Stephan Livera:

Yeah. Let me, let me take a crack at that. So, absolutely. That’s the main one. So maybe for listeners, just to give them a simple example, let’s say, if you’ve heard of this idea of multisignature, and as an example, you might have some kind of three or five multisignature set up and meaning you need three keys out of the five to sign to spend. But within the taproot world, people can create a special kinds of contracts where maybe over time, it could back off or back down to say two signatures required. If, you know, let’s say after five years or something, and they can do all sorts of more advanced kind of contracting and it, taproot can also give some additional privacy in that as well, because you might be able to use it in a way where you’re not disclosing the conditions of how you’re spending, but I guess that’s kind of getting into the taproot weeds itself. But I guess…

Pavel Moravec:

It would be for an hour of talking…

Stephan Livera:

Yeah. Exactly, exactly.

Pavel Moravec:

All the details and what the consequences could be but yeah.

Stephan Livera:

Yeah. I guess, let me put it this way. I would say it makes some uses of multisignature more private. It can improve Lightning’s privacy and I guess getting this soft fork done then enables other things to come in the future. So I guess kind of high level, that’s probably the way to think about it. And then for you guys over at Slush Pool why did you want to signal for taproot?

Pavel Moravec:

It was a no brainer, no pun intended. It’s just cool — a cool feature. There’s virtually no downside of having this property of Bitcoin. It’s just, simply better Bitcoin for everybody. You don’t have to use it. But, still there is no reason why to prevent anybody else to use it. From software perspective, it’s just a new, better version of Bitcoin, which is not harming anybody basically. So we even didn’t think about it basically at all, because it’s super cool. Part of the great thing being part of a Bitcoin industry or this environment was always this great technological stuff we are in heart nerds. Yeah. Just start to read about taproot more. It’s fascinating. Sorry. Like on the technical level and for users, obviously there’s so many, many benefits, so yeah, it was super easy and we wanted to support the signaling as soon as possible.

Pavel Moravec:

Yeah. It was fun because we were able to manage to signal for taproot. The very first block we found after the signaling started, which from external perspective looks cool, but it’s kind of messy, but anyway, it happened. Yeah. And we were the first pool signaling and it had quite nice PR spin so that it forced other pools to probably signal a little bit starker than strictly yes. Yeah. The first signaling period. Yeah. It was obvious that it’s not going to be the signaling period, which would force Taproot to be accepted or activated, but yeah. Started starting our land forcing other other pools to signal was kind of fine.

Stephan Livera:

Great. So let’s just back up a little bit just to explain, okay, what is all this signaling stuff? So if the listener has established, yes. This Taproot is a soft fork that we are bringing into Bitcoin, what’s all this miner signaling business, like is the network voting or is it really more like signaling readiness? Can you outline a little bit about that upgrade process for the Bitcoin network?

Pavel Moravec:

Yeah we mentioned that taproot is an extension or newer version of Bitcoin, and because there is no central point of cooperation or how do you say it there needs to be some process how to get the new features into the network in some way. And what Bitcoin uses even for this upgrade, it’s based on miners putting in information about their willingness or readiness to support this new version of Bitcoin. And it is quite necessary for miners to do it because to keep the network secure you want miners to double check these rules and enforce these rules when taproot is activated. So the mechanism is at the beginning when the software is ready, miners put an information — set one particular bit in the header of Bitcoin blocks created by the miners saying, Hey, I’m ready and willing to run taproot in the production.

Stephan Livera:

So to clarify, then it’s like the users can all run the latest version of Bitcoin core, which supports taproot. But what we’re talking about here is actually having the miners signal their readiness. And as you mentioned, this happens inside a version bit. And so, why do we care about all this? Right, for the listener who’s new, part of the reason why goes to this idea that we want. We’re trying to see first, if the miners will support us in enforcing this new taproot rule set, and if they do, then it helps protect some of those users who are on older node software and maybe they have not upgraded, but as you rightly said, we want to keep the network together, but there is no top down king or CEO of Bitcoin. So it’s really just a voluntary process of people trying to encourage each other. Okay. “Hey, can you signal this thing?” And also there’s a period of signaling. Can you tell us a little bit about that?

Pavel Moravec:

Yeah everybody knows that Bitcoin difficulty is changing regularly. It’s roughly every two weeks. This period is often used as great for signaling so that you can measure how many blocks has this bit set during this one period. And then you can start over in the next retarget period and the next, and it is very easy for everybody to look at the number of blocks in this period and make a judgment about it. And right now taproot is — like signaling of taproot is based on this retarget period measurement as well. So whenever there will be 90% of blocks with this bit set in one retarget period in one difficulty change period then taproot would be considered activated all miners from some point in time. And all users of the rules start to enforce this rules. There is very nice like battle of ideas or two parties or kind of parties, miners and users — there’s a lot of talks about this in history. And yeah, you can enforce the rules from both sides basically, but it’s always best when miners and users cooperate in this particular case. We don’t think it is any whole controversial or not controversial so much that it could cause any troubles. So I hope all the signaling goes well. Right now we are on 40, maybe 50% of blocks already contain the bit. And yeah.

Stephan Livera:

So listeners you can see on the website, it’s a really good website. It’s taproot.watch, and that’s got actually I can’t recall the name of the individual — oh it’s @hampus_s has created this website and he’s basically just giving you a breakdown how many pools are supporting. But the other important thing to remember is what we were saying before is that miners and pools are not necessarily the same. Now it may actually be the case that given taproot is a widely supported upgrade across the network. That basically there’s been no serious objections to it that maybe we’ll see some jockeying around in terms of miners. Because as an example, if I, as a miner am pointing my pool — my hash rate, or my hash power somewhere else to some pool, that’s not signaling for taproot, I might then re-point that. I might change that and say, “Hey, I want to point it to SlushPool because SlushPool guys are signaling for taproot.” Right?

Pavel Moravec:

It will be awesome. Obviously it’s nice that you’re doing sales pitch instead of me, I should visit more podcasts like this.

Stephan Livera:

That’s right. Well, I think this is one of those things where it’s a community thing as well, because to some extent, people have to share the message out and if they really want this upgrade, well, then they’ve got to try and convince, cajole, try and get everyone else on board with this idea. And just to sort of see if well, if taproot is something we want, well, then that’s something that people have to try to encourage. So I guess that’s one way that people can try to push things. And I guess, there is a competitive pressure here because maybe there will be some other pools or maybe they’re a bit slower, or maybe they’re dragging their feet a little bit on actually supporting taproot. So maybe it would be good to talk a little bit.

Pavel Moravec:

Be very interesting if there is maybe one, two pools at the end when everybody else is already signaling, what’s going to happen then because like, technically I think it is net positive for almost everybody. I don’t know about any particularly user group or anybody basically, who would benefit from taproot not being activated. I don’t know about any such group, but yeah, there can be some politics. I don’t know. it can be interesting if there is, maybe one large pool, not signaling, not communicating. Yeah, we will see. I hope it’s not going to happen, but if it happens, it will be fun to watch what the events will be if the hashrate would start moving between the pools. Cause it’s not so easy, it’s technically very easy to switch pool, but business-wise, it’s not always super easy to switch pools because there are typically some agreements in place, especially for bigger players. So yeah, there can be some political games as we already saw in the history of Bitcoin.

Stephan Livera:

Yeah, of course. So I think given that we have this 90% threshold, so, you know, maybe it’s possible even if we’re a little bit under 90%, but just with a bit of luckiness in terms of the variability of when the blocks come in, that we end up over 90% and it’s considered activated, but we have to wait for that to happen. And I think it’s also probably fair to point out that there are — so I guess dropping back a little bit as well around Speedy Trial. So there are multiple periods, right? It’s not that this has to be happening all in the first period and perhaps it might’ve been an unfair or maybe unreasonable expectation that all the pools would have all their stuff set up in the first signaling period, what are some of the difficulties around that or in your, or do you disagree? You actually think it’s not that difficult for the pools to signal for Taproot.

Pavel Moravec:

Yeah, it has a lot of aspects in it. Obviously you mentioned Speedy Trial — we have basically three months. So the earlier we start to signal the better that’s basically the stance of us. So we wanted to signal as soon as possible to just get the ball rolling. Technically it is very easy in principal because it is only about creating blocks with one particular bit such to one instead of zero. Infrastructure wise, If you’re running a pool, it can be easy or difficult, but it is basically only a software change. And what we did — we even didn’t deploy bitcoin core the newest version of Bitcoin core for signaling. We just changed our mining software on the pool side, which organizes the work, which sends the work to to the miners and enforce this bit, it was literally two lines of code which we changed for that.

Pavel Moravec:

And there is a second part of the whole deployment and it is being ready for enforcing the rules when Taproot is activated, and then obviously you would want to run the newest version of Bitcoin core: Bitcoin network software. And it is slightly more complicated procedure. The reason is bitcoin mining pool is a very distributed system. You have to run your software on a lot of different servers in different geographic locations basically being as close as possible to your customers. So it is not in one data center. It has to be very widely spread, and you have to run even Bitcoin core nodes in these locations as well. So we are running tons of Bitcoin networks in production all over the world. And you have to update all this software during the normal operations there.

Pavel Moravec:

So there is some procedure needed for switching the backends when you are doing the upgrade and stuff like that, but all the pools with significant hashrate that everybody has to be ready for rolling out new features, not necessarily only on the Bitcoin side, Bitcoin network side, but even for internal software as well. So it’s not a rocket science, it can be done as a normal like deployment process. So yeah, I don’t think it’s a problem I think at all, it’s more willingness to do it than complexity of doing so.

Stephan Livera:

I see. Yep. And perhaps in the case of different pools, because I guess there are different size pools. And I guess for context, Slush Pool, as I see on the side has roughly 3% of the network’s hash rate, and maybe some of the largest pools might be around 14%, but that’s like really the biggest ones.

Pavel Moravec:

It is completely the same for everybody. I think we are not significantly smaller infrastructure wise than the largest pools because the hash rate is not the best number for estimating how large the infrastructure needs to be. If your hashrate is very concentrated in small number of data centers with a lot of hashrate, your business or work is much easier. In our case, we do have more spread hashrate all over the place. I can imagine we would have to run more servers than much larger pools. If you look only on the percentage the network, it’s not giving the best information about which I’m completely not complaining. It’s very scalable thing. Adding more servers, if your infrastructure is well done. It’s easy. So I think it’s the same for everybody basically.

Stephan Livera:

Yeah. And then perhaps it’s also a question of having the right technically skilled staff, and maybe they’re not away on holiday or away on leave at the time that you’re trying to do this upgrade and things like that.

Pavel Moravec:

Yeah. But you don’t want to mine on a pool without skilled people to change one bit in the Bitcoin header, you know?

Stephan Livera:

Correct. Yeah, for sure. So while we’re here as well, just for listeners to get some context, what are some of the ways that the pools will differentiate themselves from each other? Like how do they compete? Like if you’re a miner and they’re listening right now and thinking which pool that they would like to point their hash rate towards, what do they choose that based on?

Pavel Moravec:

It is very value-based, you can choose your pool based on who you trust. You can obviously choose pool based on fees. You can think about what kind of blocks would this pool create. There are some pools who will definitely censor transactions or are doing it already, and you can be okay with it or not. It’s one of the big goals or no goals for some people. There is this transparency thing, some companies are mining, for example, with us because we can give them a very good support in their auditing process and so on. So their even reasons for like running firmware or even the pool with a known entity from Western world. So that internal processes, audits, or getting insurance and stuff like that can be reasons for having a decent partner who you can have legal agreements with, can be difficult with some pools and so on.

Pavel Moravec:

And so it’s really differs based on who you are as a miner. If you are a publicly traded company, for example, your preference would be slightly different and it would point more in direction of not screwing your shareholders basically, and ensuring that nothing can go sideways. If you are a small miner, you can be more you can look more about on the censoring thing or trust. It really depends obviously economical things like fees or one of the cool or critical features of pool is being 100% time available and working. So you can measure how your latencies are, how the pool really behaves from this perspective, because if you are, for example, half percent of time down, or the servers are not responding properly and so on, it cuts to your earned Bitcoins profits and so on. So yeah. A lot of stuff you should consider it as a miner, especially if you are running a larger operation.

Stephan Livera:

So, yeah, so there’s a range of thing. So I guess it’s fees, it’s uptime, it’s latency to your nodes. It is structure around whether they are planning to censor, of auditability through the stack. So I suppose let’s go a little bit further into the auditability aspect. I think that’s something I know you at, you know, you and the team at Braiins are big on this idea of trying to own, or self-sovereign through the whole stack. And I see, you’ve got firmware for the actual it’s going down to firmware for the hardware to having pool for mining farm management. Can you tell us a little bit about the offerings there from Braiins?

Pavel Moravec:

Yes. As I mentioned, we are focusing more on the software stack and services around the mining. So our software from — let’s take it from the hardware physical side of things. We do provide firmware for the miners or the physical machines doing the dirty work of hashing blocks.

Stephan Livera:

Boiling the oceans?

Pavel Moravec:

Yeah. The bad boys. So we do provide a firmware for these machines, but invention to give people software, taking the, all the power the missions can provide. You can do pretty complex optimization tricks on the level of hardware, like extract all the power you can. So it’s this thing. Then we historically have a pool so that the machines are connecting to a pool, which organize the whole mining. And you’re being paid for delivering the hashrate. There is a in-between software as a local proxy or some management proxy in the farm. We are not currently publicly offering this yet, but we are getting into space as well. And it is related to a local farm management so that there is this area we do work on the poolside that the offerings are basically very similar to what’s other pools are doing we are working on a solution, which would allow you to sell your hash rate for you freely. So extending this stake even further towards trading of the power. There is a whole aspect of managing the farm from external point of view. So you can go and manage your machines through internet which is what you mentioned Braiin’s OS manager. There is a lot of pieces. It’s quite difficult to wrap your head around if you’re not familiar with the physical spec, if you are not a miner, there is a lot of moving parts that the software stack it takes like four different layers. So it’s so fascinating.

Stephan Livera:

Right. And so speaking of firmware then in terms of running Braiins as the firmware, does it matter which miner which manufacturer brands that you’re using or is it only for specific unit?

Pavel Moravec:

It would be awesome if we support all the machines or kinds of machines which are running right now in the world. It’s unfortunately not the case. We are pushing as hard as we can to support various types of miners. Currently we do support Bitmain machines subset of bitmain machines, mostly S17s, S9s historically — all different versions of this kind of hardware. These machines are much easier to switch firmware on them. It’s they are trading at times where manufacturers are not so protective. The newer machines are more complicated to get on with a firmware, or we do have a wolf miner firmware running in our internal lab. It’s not publicly released yet, but as I said, we are trying to push it as hard and as soon as possible, it is very promising on the wolf miner side. The newest versions of Bitmain hardware will follow pretty soon as well. Yeah. it would be great if we have support for everything and it’s definitely the intention but it takes some time is not always very straight forward to support more hardware, but it’s…

Stephan Livera:

And I think the other thing to point out is just the aspect of having open source firmware. And I know that’s also a big, that’s something you and the team are quite big on that aspect of it. Why is that important? Why should people care about having open source firmware and other aspects of their mining stack?

Pavel Moravec:

Yeah. You, if you buy a machine, you don’t want to be a slave]. it’s super easy. Look at wifi routers. There is a huge problem with firmware in wifi routers. For example, from our perspective, whenever we buy such a machine, we flash our firmware there, which is much more secure than the typical offering, because we care about the machine and security of the machine. And with firmware and the miners, it is a similar thing. You’re buying a machine for doing some work, but at the same time, you want to have a full control of what the machine does or not. And there are historically some not very nice examples of the firmware doing stuff you didn’t know what it is. Not always good for you as a user, like controlling from external APIs or not using all the power the machine can deliver to you because reasons and so on and so on.

Pavel Moravec:

So we deeply think that you should have full control over the hardware you’re purchasing. It’s similar to, you should have a control over your keys as a Bitcoiner. You can opt in to some — let’s say wallet provider offerings, if you decide. So yeah, the whole thing that you will have the control and you can decide what to do is normal, and it’s the same with firmware as well. And there’s a second layer to it. You mentioned, and it is open source. It’s an extension of the right to do whatever you want with the hardware — flashing, anything, what you would like to run on the machine. For example, auditability for a large companies is I think like having completely unknown firmware running in your data center, connected to the internet and the network site, without possibility to look into source code or talking with whether what’s this thing, is doing, yeah, it’s a big topic, but the open source is even an extension of it, where whenever it is possible to open source the code so that the user can tweak stuff, audit stuff by themselves, or do changes and run their own version of the firmware. It’s a great thing. In general, obviously there is a tension between having all the codes open and having some proprietary algorithms, which you would like to make some money on. we kind of struggle with this two things internally as well, because there needs to be some line, but yeah, in general, being capable of doing with your machine, whatever you’re pleased, it’s like no brainer for us. As far as we can go with providing the basic versions as open source. Yeah. It’s again something.

Stephan Livera:

And to the aspect of having control over your own device, it’s probably useful for listeners to understand that it’s not, this is not just a totally theoretical thing. There have been historically examples where people bought mining equipment and unbeknownst to them, there were say, remote kill switches or remote abilities to change things in that device. And essentially if you know the ecosystem with pushing and driving towards the idea of having an open source ecosystem, then those kinds of things are much harder to get away with. Right?

Pavel Moravec:

Look, let’s look at the Braiin’s OS manager. It is kind of external management tool. So we have the capability of changing the stuff on the machines remotely. It is part of the whole solution that you can from your browser manage the whole farm changed such things, do crazy stuff with the hardware remotely, but there’s very big difference between doing it in a way that user opts into this feature set or doing it covertly. And if the user has to ability to say, no, I don’t want this. I want to switch this off or switch to a different firmware or whatever. That’s perfectly fine because then we can talk. It’s an open offering. And the user is still the one with the control of what’s going to happen or not. Obviously there is a trust to the vendor. if you’re running somebody else software, you’ll always expecting them to not behave badly, but the whole thing that you can choose is the critical piece of this this equation.

Stephan Livera:

Yeah. And I think there’s another benefit I’ve seen on your website. You mentioned dynamic power scaling. Now this is something that you would do on certain types of machines, right? So, so what is dynamic power scaling?

Pavel Moravec:

Yes. It’s a very cool name for quite simple principle. It’s a feature allowing the firmware to lower its power draw when the external conditions are changing. So one particular example is if the machine is overheating and the machine is unable to cool itself down by running the fans faster, or some external temperature changes outside of a normal range the machine downscales or lowers it’s power draw so that it can maintain safe temperatures, you can do it in the other direction as well. We are still improving this feature because the holy grail would be being able to change these properties based on, for example, different electricity price. When in environments where the price is different in different parts of the day and stuff like that, because then you can run for example, in economy modes in one part of the day and give me everything what you can in different parts of the day. And it has different power draws and you have to manage it properly during this time. So this cool sounding feature is basically tweaking with power draw of the machine automatically.

Stephan Livera:

Awesome. So that is but as I understand, that’s only available on certain machines as well. Right? So which machines is that available for when you’re using Braiin’s firmware?

Pavel Moravec:

It is a good question. And I don’t have answer for that at the moment. I’m not doing this thing myself spending more development or management time with the pool side of the things.

Stephan Livera:

I see. Yeah. so turning back to this whole idea of doing soft forks and upgrades in Bitcoin, I think it’s interesting because right now there’s a few different things here. So one is — it might not be clear that all the pools in the future will actually be identifiable, right. That there’s a person you can pick up the phone and call or email them. I mean, in the future, it might not actually be that case, or maybe they might be distributed down a little bit more. So then I wonder.

Pavel Moravec:

Yeah, but do you think it is a good thing, right? Or are you suggesting that not knowing the person running the pool is worse than knowing it? I’m not completely completely sure that knowing everybody as a pool operator or owner of the hashrate is a good thing in principle. It’s obviously good. If you want to tweet that, “Hey, start to signal taproot” and you have some handle to tweet too. But from the other perspective, I dunno, I think some kind of privacy can be good thing even in this space.

Stephan Livera:

Yeah, of course. And I think it’s just an interesting thing.

Pavel Moravec:

Imagine you have a very big farm and you’re running your own operation, you’re running — you’re a solo mining, and there is two, 2% of hashrate who, which is unidentifiable for external world. It’s your hash rate. You have the same power over the blocks related to your hashing power obviously as everybody else, but you don’t have to say to everybody, “Hey, I have this farm.” That’s perfectly fine. So yeah, the premise that we should know who runs the pool, maybe — maybe not.

Stephan Livera:

Yeah. So and I’m not saying that it has to be that way. I’m just saying from purely from the perspective of trying to coordinate an upgrade in the future, that may not be possible. Right. And so that’s just something we have to think about and accept, that may be the reality going forward. We don’t know that for now, for sure. But it could — maybe the other argument would be something like maybe there is a tendency towards using big pools because you, otherwise, or just using a pool rather than solo mine. So I guess just for listeners who are unfamiliar, if you are solo mining, it means you’ve generally got a small percentage of the overall network’s, hash power, obviously. And you might experience some variability in your income that you’re getting from Bitcoin money, because how often are you going to find a block when you are some tiny fraction? So you kind of have to use pools unless you’ve got enough hash power. Right?

Pavel Moravec:

Yeah, it’s perfectly correct. But we can see tendencies as you mentioned pools are getting bigger. This somewhat stopped in the last years, but we can point to few, very large pools. And it is in most cases, beneficial for users to join pool, especially if you’re not investing hundreds of millions of dollars to your own hardware and data center and all this stuff. And then you can probably mine yourself as a solo miner, but it’s not the typical use case. Let’s face it. So for normal users its very beneficial to join some pool. And from — for example, the taproot perspective, fortunate we do know who the operators of these pools are, or most of the pools, so we can push them on Twitter. But yeah it is not necessarily the case, but unfortunately I think it’s going to go into this direction of pools being more like an exchanges in the Bitcoin space where they started as garage projects. But as time progresses, there are more KYC, full off lawyers companies, let’s say, and unfortunately pools are going into this direction as well, which has obvious some good properties being a proper partner to these publicly traded miner companies. It has its value, but at the same time, you know, running a pool as a garage project is fun as well. And there is some history — some spirit in it.

Stephan Livera:

Yeah. That’s an interesting way to put it. And I think, yeah, I agree with you that there’s benefits and costs there, right? On one side, it’s easier to coordinate an upgrade, but on the other hand, having identifiable pool, you know, people who are running the pool, you know, maybe that makes it a little bit less able for people to, who want to be, who want to have like a private or kind of more sovereign if you will. So I guess, that’s something to think about there.

Pavel Moravec:

Yeah. You can force — If you know, who runs the pool, you can do a lot of stuff to influence their decision.

Stephan Livera:

Exactly.

Pavel Moravec:

So not knowing it can be beneficial because the person can decide more on a clear, economical incentive level, what is right. And it would typically be aligned with Bitcoin in general, more than if you open this influence from external world, because if the person is anonymous, and makes Bitcoins, assumption would be, Hey, whatever is good for Bitcoin, this person will probably wants to go in this direction, but once it’s a publicly known person, you know, there can be reasons or some just this aspect is interesting as well.

Stephan Livera:

Yeah. And the other point as well is — okay, so right now we’re looking at blocks and saying, Oh, see, this is as an example, SlushPool. And some other block is some other pool, but that part is not actually verifiable. Right? Like, it’s just, they are all — like all the pools, are just stamping it with their name, but you know, what, if someone stamps it with somebody else’s name or just doesn’t stamp it at all, like that’s also another thing, right?

Pavel Moravec:

Yeah. It’s interesting thing because as you mentioned it’s just few bytes in the block and the software detecting or showing which pool has which percentage of network just looks into the blocks and tries to pattern, match some bytes or string by doing it, this thing which is which pool created this block, but you can do better analysis than this. You can obviously look at the stuff just from this perspective, but it’s not, you know, you can go and see transactions. You can double check hashrates against the produce blocks once you look at the whole block content, you can draw better conclusions. Once you started [doing] blockchain analysis on payouts, you can link the addresses towards which the block is mined, and you can link it from there as well, and so on and so on. So there is a way how to distinguish pools if you spent enough time with the problem. But the typical markers are working just fine.

Stephan Livera:

And I think the other point, as you said that over time, as some of the pools have gotten larger, they have a presence, right. They might have a social media profile or a website because they want to do marketing because they want to get new miners pointing some hash power there. So I guess that’s…

Pavel Moravec:

The business.

Stephan Livera:

Yeah. I mean, you’ve got to run a business. And so as these businesses get larger, well, then they might start having more of an online or a fingerprint or a way of trying to draw people in. Because as a customer, let’s say, if you’re a miner out there, thinking which pool do you choose? Well, you might want to choose one that has, you know, a big enough hash power or whatever features it’s offering. So I guess that is also kind of a tendency pushing the other way. So maybe it will still be identifiable pools going into the future.

Pavel Moravec:

I think it’s going to be exactly, as you’re saying, it takes only one mistake when you try to be anonymous on the network and you make one mistake of leaking the information publicly through some transaction being made, for example, from your coins then you can go back and look at the history on the blockchain and probably Identify a lot of stuff exposed. So it, I think it’s very difficult to be completely anonymous as a bigger player in the mining space, but the principle is still quite nice.

Stephan Livera:

Yeah. I see.

Pavel Moravec:

Not everybody is doing blockchain analysis over the weekends. So…

Stephan Livera:

Yeah. So just for listeners who are unfamiliar there, what that is, it’s referring to how, when you let’s say the way the Bitcoins are paid out from the pool to the miner if somebody is able to look at essentially like chain surveillance and use, either of those tools are open-source tools like OXT.me or so on where they can try to trace it back and say, Oh, it came from this wallet, or I guess in the other case also even just clues from the block itself that give off which pool it came from. Right. Which pool created that template, right?

Pavel Moravec:

Yeah we started the discussion with the taproot. Taproot is — there is an analogy with taproot as well. Taproot basically masks differences between different kinds of transactions. So everything looks the same. So from chainalysis perspective, it is great for the users because there is less meat to look at if you’re trying to infer some information from the transactions, because everything looks the same, it’s much more complicated and similar thing is for blocks as well. You can see slight differences in the blocks produced by different pools because not all the pools are or not all pool software works exactly the same. So you can see patterns in the data so you can distinguish different source of Bitcoin blocks. Obviously you could try to hide it as a pool, but if you don’t do it intentionally, you can see, and the data are pretty clear. It’s a nice exercise for a data analyst.

Stephan Livera:

Cool. And so I guess just broadly in the ecosystem around supporting upgrades to the ecosystem. Now, if we look back at 2017 and all the drama around activating SegWit, which was seen as a very much an enabling technology that would then allow, I mean, there’s a range of things, but it was seen to be enabling Lightning network. And so there was a bit of a debate back then about, “Oh, would miners support this?” Because maybe if everything’s happening on Lightning, well then is that going to take away on-chain demand in terms of the transactions? And so are miners is going to miss out on the transaction fee revenue from that. But I think the counter argument would be something like, “no, but it’s bullish overall because it’s making the overall ecosystem more valuable.” And therefore, even if there’s less at the start, it’s kind of like a short-term pain for long-term gain situation where even all the channel opens and closes and all of that stuff is contributing to the overall ecosystem. So I’m just wondering if you have any insights to share there, I guess, from your side as well. And from when you talk to miners whether that is playing on their mind at all about any potential future upgrades or it’s sort of saying like if it’s building the overall ecosystem, then it’s a good thing and we want it.

Pavel Moravec:

I think most of the non-crazy miners, there can be some crazy ones — understand it the same way, and it is anything what can push Bitcoin further as a good thing, all the small gains, you can probably gain if for example, Taproot is not activated than transactions can be slightly larger so that you can try to think okay, it’s going to cost more on fees. It is childish game. the big thing is understood by miners. If the Bitcoin, as a whole thing is stronger and better, it has much bigger influence on them as well. Most of the miners I know are bullish in Bitcoin in general, they have to be, and they’re HODLing. So whatever helps the ecosystem in terms of price or stability or whatever it is good for them as well in general. So yeah, besides some political games, as we saw it a few years ago, and I’m not downplaying that there were some serious discussions in that time, I’m not saying it was silly in any way, but in general, I think miners are for stronger and better Bitcoin because it will give them like a future.

Pavel Moravec:

Even from the economical perspective, it’s good, for any HODLer to have strong Bitcoin with as much features as possible in a secure way. I think the alignment is quite nice on taproot especially.

Stephan Livera:

Yeah. And so for any, I guess, listeners out there who want to encourage taproot adoption or signaling, and then later adoption, do you have any messages for them or what can they be doing if they want to try and get this over the line?

Pavel Moravec:

Right now it’s just about signaling. So if anybody can, has any influence over directly miners or pools, if you have a friend in China running a pool, give him a call. It’s not necessarily the thing everybody would do, but if, yeah, if you know any miner — the signal, I think it is very easy to switch pool. If you can choose. There is a lot of signaling pools already out there and any influence even in social media that the public understanding or public mood, can make a difference as well. The whole gain with the first signal blog was just this, it has not direct influence on anybody, but if the discussion is present then maybe the miners or pools will be a bit faster and we will make it into activating taproot in time.

Stephan Livera:

Excellent.

New Speaker:

It will be awesome. If it’s in one month done and there’s no drama, I would be super happy. It’s easier to move to some other improvements or getting the space better than trying to play with bits.

Stephan Livera:

Yeah, of course! Pavel, thank you for joining me today for listeners who want to find you and find Braiins or Slush Pool online, where can they find you?

Pavel Moravec:

No, I’m a very public person you just type SlushPool or Braiins into Google, and it’s going to be a lot of links there. Braiins.com as a good starting point to eyes and you can get everything what can be interesting from our offerings or information available from there so…

Stephan Livera:

Excellent. Thanks for joining me.

Pavel Moravec:

Thanks for invitation. It was a pleasure.

---
title: Bitcoin Mining Firmware and Stratum v2
transcript_by: aphilg via review.btctranscripts.com
media: https://www.youtube.com/watch?v=xrdhtQPHg2o
tags:
  - mining
speakers:
  - Rachel Rybarczyk
date: 2021-11-04
---
## Introduction

Coming to the stage next, she is the VP of Mining at Galaxy Digital.  Everybody please welcome to the stage Rachel Rybarczyk, everyone.  My name is Rachel, I'm VP of Mining at Galaxy Digital.  I've been in the space for a few years now and I recently started developing on Stratum V2, which is a new mining protocol.  So I want to talk today about Stratum V2, how it compares to Stratum V1, the adoption efforts, some adoption hurdles, and how it all fits in together.  But first, let's take a look at some history.

## Mining History

### Network Hash Rate

So I know that Bitcoin mining firmware might be new to some people, and I just want to level set with some terminology we're all familiar with, and that's network hash rate.  So here we see the network hash rate of all time.  Network hash rate is the measure of computing power on the network, and computing power is contributed by ASIC machines.  Generally, the hash rate has gone up and to the right with more adoption and more efficient machines.  So regardless of the machine, whether that's CPU, GPU, or ASIC, how the machines are capable of connecting to the network is done by the mining protocol.  Most commonly, this protocol is implemented in the firmware.  There have been three main protocols so far, and right now, Stratum V1 is the most widely used today.

### Stratum V1 History

So how did Stratum V1 come about?  Its predecessors, which is get work and get block template, were fine for pre-ASIC era, but by late 2012, it was apparent that ASICs were going to be released,  and they were going to lay the foundation for a new network hash rate that was going to be higher than ever before.  So on this chart, we see the hash rate spike when ASICs came online in early 2013, and then right at that time, the community switched to Stratum V1.  And then before that, we had a hash rate spike when we switched from CPU to GPU mining, and we also got a new mining protocol, which was the getwork.  So Stratum V1 was created by a Bitcoin talk user named Slush.  He explained his reasoning for creating the protocol as follows.  He says, "The reason why I designed this protocol and implemented an opensource pool server is that the current getwork&lp mining protocols have many flaws and can hardly be used in any large-scale setup.  Asic miners are probably coming at the end of the year 2012, so bitcoin community definitely needs some solution which will easily scale to tera-hashes per second per pool user..."  So timing was really important here.  We see that the conditions that called for a new mining protocol was when the network hash rate was making a major and permanent jump.  So let's look and see how hash rate has scaled since then.  It's only continued to grow.  Today, we're roughly at 150 million tera-hashes per second, but we're still using the same mining protocol developed in 2012 when the hash rate was roughly 12 tera-hash per second.  There have been no changes to the protocol despite the steep hash rate increase.  In fact, I would like to argue that based on the network hash rate alone, a new mining protocol is several years past due.  I think we should have gotten one around 2017 when the hash rate started to really spike.  And this is actually when Matt Carollo released his BetterHashBip draft, which was a new mining protocol that was later absorbed into Stratum V2.

### Stratum V1 Basics

So now to understand why we need a new update to the protocol, let's take a step back and understand what Stratum V1 does offer us.  In mining, we've got ASIC machines that perform the hashing and the pool server that sends out the jobs to the machines.  They communicate by sending messages back and forth.  And the four main messages of the Stratum protocol are subscribe, authorize, notify, and submit.  So you plug in a miner, it turns on, and the first thing it does is it sends the pool a subscribe message indicating that it wants to authorize itself as a worker and commence working.  If the request was successful, the pool responds with a notify message back.  The miner then sends an authorize message containing the pool username and password credentials.  You can see them here in plain text.  And then the pool responds with another ACK, followed by a notify message that contains all the information required for a miner to commence work.  Once the miner has found a valid job, it sends the information to the pool via submit message, and the pool responds with an ACK and another notify message continuing the cycle.  So all the messages you see here are real example of like real Stratum messages.  So you can plainly read what's being passed back and forth.  And then with this diagram, I just want to demonstrate that the current Stratum V1 firmware used today, each miner has a direct connection with the pool service.  So this is not ideal for large scale mining because it eats up a lot of bandwidth.  And so a lot of large scale miners will use proxy servers to help improve their efficiency of their operation.  But the proxy server is actually not part of the Stratum V1 protocol.  So right now you have to go to GitHub to find a proxy and a lot of them aren't really robust, or a lot of these mines will just make custom in-house solutions.  Now that we have a decent understanding of the Stratum V1 protocol, I want to look at what are some of the characteristics for mining protocol we would like.

## Successful Mining Protocol Characteristics

So I think there's like four key features that we want to consider.  And that's usability, maximizing miner revenue, keeping that revenue safe, and minimizing the potential security threats to the overall Bitcoin network.

### Usability

So first, a miner needs to be able to use the protocol.  It needs to be a very low barrier to entry to get a miner up and running, especially when considering getting the protocol adopted in a timely manner. It needs to be simple to operate after it's installed.  And it needs to be well-defined and well-documented so we can all conform to the same standard.  It also needs to be flexible.  We need a mining protocol that's going to work for someone who's got a couple ASICs or someone who has thousands of machines in an industrial mine.

### Maximizing Miner Revenue

So after getting up and running, we want to make sure that we're maximizing the miner's revenue.  Maximizing revenue is all about minimizing the computational power and time it takes for a miner to receive the job, commence mining, and send it back to the pool.  So we just want to make every single watt count here.  We do this by having very lean messages and minimizing the number of packets that are being passed in between the pool and the farm.  All of these things save on computational power, bandwidth, and time.  And they all reduce a miner's stale job ratio.

### Keeping Miner's Revenue Safe

So after maximizing a miner's revenue, again, we want to keep that revenue safe.  A mining protocol should have the proper encryption and authentication in place so the reward is protected against man-in-the-middle attacks.  And there's a specific tag called hash rate hijacking, which an attacker will sit on the wire in between the miner and the pool.  And it will read those messages that we saw in a previous slide.  And it will replace the honest miner's pool username and password with the attacker's username and password.  And so it effectively reroutes the honest miner's hash rate to the attacker.  And these attacks can and do happen.  I actually have no proof, but I think that they're a lot more common than we think because they're really hard to detect.  Like, if you have a huge mine with thousands of miners, and if you're not monitoring every single miner for possible attacks, you really have no idea if it's happening.  And another reason why I think we don't hear about it very often is because, like, if I was a pool operator and I got hash rate hijacked, I wouldn't tell anybody about that.  Like, it's just not a good look, and I wouldn't want to publicize that.  But it's still really important that we understand that this is a real threat to miners.  We also want to have some sort of, like, mechanism in place to prevent against pool operators from skimming off of the top of the honest miner's reward.

### Bitcoin Network Security

Finally is network security.  We need a protocol that aligns miner incentivization with the censorship resistance and decentralization guarantees we all expect from the Bitcoin network.

## Stratum V1 and V2 Comparison

Okay, so what is Stratum v1 lacking and how does Stratum v2 compare?  Let's use our metrics to assess.

### Usability

#### Low barrier to entry

So Stratum v1, despite its limitations, or really kind of because of its limitations and how the industry has grown around it, it's really easy for a miner to get up and running.  They get the miner in the mail, they plug it in, put their credentials in, and they walk away.  In my opinion, this low barrier to entry metric is the most important thing to get a new protocol adopted in a timely manner.  And this is because, like, mining is complicated.  There's a lot of moving parts that go into creating a mine, and we just need to make it as easy on the miners as possible.  Unfortunately, neither of the adoption efforts of Stratum v2 fulfill this criteria.  So we're not really off to the best start, but it will get more compelling.

#### Easy to use

So Stratum v1, it's really not that easy to use because there's a lot of weird edge cases.

#### Well defined and Well Documented

Stratum v2 is very easy to use, and this is because it's well documented and well defined.  Stratum v1 was never standardized, and there's a lot of inconsistent implementations made, which really harms the community and harms miner products.  But Stratum v2 aims to be fully and precisely defined.

#### Flexible

So Stratum v1 is also very inflexible.  We saw in the previous slide that each miner has its own connection with the pool, and that's not good in terms of flexibility.  And there's no configuration settings to aggregate these connections so we can share data where appropriate.  And also with Stratum v1, a miner has very limited control over their search base.  So Stratum v2 fixes this.  It's very flexible in its search base and configuration, and it does require some extra server infrastructure to take advantage of the full feature set.  But this proxy is part of the Stratum v2 spec where it's not in Stratum v1.

### Miner Revenue

Okay, so let's talk about maximizing miner revenue.  Stratum v1 fails on this account.

#### Lean Messages
They use those plain verbose JSON RPC messages we saw in the previous slide.  And that was really great for initial adoption because people could read the messages and they could understand the protocol.  But mining has gotten much too competitive to continue to be using human-readable messages.  That's because ASIC miners, they don't understand JSON.  They only read bytecode.  So we're wasting a lot of time serializing and deserializing these JSON messages to binary.

#### Fewest Packets
Additionally, Stratum v1 has a lot of legacy messages left over from other protocols that aren't doing anything.  So Stratum v2 fixes these problems by removing those unnecessary messages and by using a  binary protocol.

### Miner Security

Okay, so now comes keeping that reward safe.  And shockingly, no pre-Stratum v2 protocol has really addressed miner security.

#### Authentication

Stratum v1, it fails here because it's got an unauthenticated connection between the  pool and the miner, leaving it susceptible to hash rate hijacking attacks.

#### Encrypted Connection

And Stratum v2 fixes this simply by just using AEAD encryption over an authenticated communication  channel between the miner and the pool.

#### Verifiable Payouts

Another aspect of miner security is verifiable payouts because we want to make sure the miners  are being fully compensated for their work and the pools are not stealing any of their  rewards.  Unfortunately, no protocol fixes this, including Stratum v2, but I do just want to start talking  about it in case the next time the hash rate makes a major and permanent jump and we upgrade  protocols, maybe someone can solve for this.  So for now, let's just get rid of it.

### Network Security

Finally is network security.  There's a major network security vulnerability baked into all pre-Stratum v2 mining protocols,  and that's the very real threat of transaction censorship by the pool operators.  So right now, the handful of pool operators, they decide all of the transactions that are  confirmed on the Bitcoin network, and that is way too much power to have in the hands of one group.  If the pool operators began colluding to censor specific transactions, right now with a protocol  in place, the community would have no recourse.  So Stratum v2 is not good for network security because it is decentralized by design.  The full feature set of Stratum v2 offers a miner the choice to select their own transactions  and build their own block template, so it effectively democratizes the block template.  So overall, while Stratum v2, we don't have that low barrier to entry metric, it is much  better in every other way.  And now I want to talk a little bit about the two adoption efforts.

## Adoption Paths

### BRAIINS OS

So first is a third-party firmware called Braiins OS, and this is developed by the people at Slushpool.  And the second is an open-source Stratum proxy server.  So starting with Braiins, they are doing an astounding job developing this firmware.  It's already in production.  This is the only production-ready Stratum v2 implementation today.  There's two parts of this project.  There's Braiins OS, which is the open-source project, and it runs on a few S9s.  And then there's Braiins OS+, which is a closed-source fork of Braiins OS, and it has some closed-source  auto-tuning in there.  And it has several more machines available.  So yeah, it's running on 100,000-plus machines right now, which is an incredible feat that  I think we should be celebrating as a community.

#### 3rd Party Firmware: Hurdles

So looking at the high-level architecture of how the Stratum v2 firmware would connect  to the pool, we see that just like with Stratum v1, each ASIC has an independent connection to the pool.  And perhaps you're wondering, okay, like if this is exactly the same as Stratum v1, then  what's the holdup with adoption?  And that's because of a few things.

##### Slow Firmware Development

One, firmware development is slow.  You have to have a new piece of firmware for every single chip architecture, so that can  slow things down.

##### Closed Source

But the bigger problem is that ASIC manufacturers want to keep their firmware closed-source.  They make it very hard for people to install third-party firmware on the machines.  This is not unique to Braiins.  This is any firmware, Stratum v1, Stratum v2, whatever.  It's very hard to put that on a lot of new machines.  This is very anti-the ethos of Bitcoin, right?  Like if we buy our machines, we want to be able to put whatever software we want on there.  But unfortunately, that's not the case.

### Stratum Proxy

So let's switch to the other adoption effort real quick.  It is the Stratum proxy, which is open-source on GitHub.  And Square Crypto, BitMEX, Galaxy, they're all funding developers to work on this project.  But it is not production-ready.  It is still very much in the development phase.  All right.

#### Stratum V2 Proxy Connection

So let's look at some configurations of the Stratum v2 proxy.  Here we've added the proxy on the farm side, and the proxy does all of the heavy lifting.  We see there's a couple different channel types.  We have a standard channel between the miners and the proxy, and then we have a group channel,  which is a group of the standard channels between the proxy and the pool.  And channel is just kind of like a fancy way of saying this type of connection can only  pass these types of messages.  So this ability to group the channel lets us pass data a lot more efficiently, and these channels are really what gives Stratum v2 its flexibility.  And then what about transaction set selection? All we need to do from a miner's perspective is add in a Bitcoind node and just flip some  configuration settings.  Underneath the hood, transaction selection is much more complicated, but we're just looking  from a miner's perspective here.  So what's cool about the Stratum proxy is that you can still be running Stratum v1 firmware  and use a Stratum v2 proxy server.  And so that'll give you the authenticated encryption, and it'll give you a little efficiency  boost in comparison to Stratum v1.  And then you can also still select your own transactions here.  So even if a miner has Stratum v1 firmware on their machines, they're still able to build  their own block templates, which is great for flexibility.

#### Stratum Proxy: Hurdles

All right, so a couple hurdles here.

##### Additional Server

By design, the proxy requires operation of additional server, and then if you want to  build your own transaction set, you have to operate your own Bitcoin node.  And that could be a burden to entry for an average miner.

## Adoption Paths Comparison

So right now we've got two adoption paths in the works, and let's use our metrics to  see how they measure up to Stratum v1.  All right, so immediately we see that both adoption efforts give us a lot more than Stratum  v1 does.  I'm just going to focus in on some of the negatives though.

### Braiins OS Negatives

So for the third-party firmware, it's difficult to install because of how the manufacturers  operate, so we lose that low barrier to entry. It doesn't include the logic to do your own transaction set selection, so you still suffer  from transaction censorship.  And then you don't get as few of packets as you would if you were using a proxy, but you  still get a much more efficient protocol than if you were using the Stratum v1 firmware.

### Stratum V2 Proxy Negatives

So moving on to the proxy, we get everything we wanted except for that low barrier to entry  metric.  So overall, both of these things are great, but we still need something to sort of get  us started.

### 3rd option? Stratum V2 OEM Firmware

And I started thinking, is there another option, maybe one that wouldn't give us everything  we wanted but would just be super good for adoption?  And I really didn't like what I came up with, but I think in terms of just getting everybody  bootstrapped with Stratum v2, it will be the fastest thing.  And that's to get the ASIC manufacturers to implement Stratum v2 in their closed source OEM firmware.  I think if we can get Stratum v2 functionally identical to Stratum v1, that Stratum v2 would  unquestionably be adopted essentially overnight.  So getting back to our metrics, if we are just looking at firmware now, we see that  if we have Stratum v2 OEM firmware, we lose out on the same things as a third-party firmware,  but we gain that low barrier to entry because the machines are already coming with Stratum  v2 pre-installed.  And you might be thinking, well, if we do it this way, we're never going to get transaction  censorship resistance.  And to be honest, you're right.  But I'm actually going to make the argument that that's OK for now because, again, the  first step in gaining transaction censorship is to just get miners onboarded with Stratum  v2 in its most basic form.  As much as we wish every single miner wants to select their own transaction set, and maybe  they do, but I still think that this Stratum v2 feature actually needs to be looked at  not as the number one benefit of Stratum v2, but as a safety mechanism where if pools really  are skimming off of the top, and if pools really are censoring transactions, and it's  becoming a really big problem that Bitcoin network, like Bitcoin tank is pricing a miner's  bottom line, is getting impacted, they will switch over to start selecting their own transaction  sets. But it's much better to have that infrastructure already in place than continue on with Stratum  v1. And if that does occur, have absolutely no recourse.

## Social Dynamics

So I actually think that getting the manufacturer to get Stratum v2 in their firmware might  be the hardest path.  And that is just because of how the industry has developed, like just the social dynamics  between manufacturers and the rest of the industry.  Because manufacturers keep their closed source, keep their firmware like extremely closed  source. There's a there's a rumor that all the manufacturer's firmware are a fork of  CG miner, which is an open source miner that's under the GPL 3.0 license.  And so these manufacturers allegedly have illegally closed source this firmware and  have been selling it.  So I was thinking since CG miner is already open source as a community, we could like fork CG miner, put the Stratum v2 logic in there, keep it all open source and then let  the pools basically just like merge that back into their firmware and closed source it,  which, you know, isn't ideal, but it's better than nothing.  This also really highlights how the space is divided between what the manufacturers want and what the devs want.  And there's actually another elephant in the room here.  And that is there is a disconnect between the developers and the miners as well.  And that's especially when it comes to what we prioritize in a mining protocol.  And that leads me to my next and final point.  So this fundamental disconnect between developers and miners, I'm definitely generalizing  here, but developers tend to be very altruistic. They dedicate their work to ensuring Bitcoin remains decentralized and censorship  resistant. But miners, on the other hand, they're very profit driven.  And there's really nothing wrong with either side.  In fact, Bitcoin is designed to have both.

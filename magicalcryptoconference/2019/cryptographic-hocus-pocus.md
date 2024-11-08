---
title: 'Cryptographic Hocus-Pocus Meaning Nothing: The Zcash Trusted Setup MPC'
transcript_by: Bryan Bishop
tags:
  - privacy-enhancements
  - cryptography
  - altcoins
speakers:
  - Peter Todd
media: https://youtu.be/YHieWJWwVbE
---
or: "Peter Todd's secret love letter to Zooko"

## Background

See <http://web.archive.org/web/20170717025249/https://petertodd.org/2016/cypherpunk-desert-bus-zcash-trusted-setup-ceremony>

and later it was then redacted: <https://petertodd.org/2016/cypherpunk-desert-bus-zcash-trusted-setup-ceremony>

## Introduction

Alright. Hopefully you guys are all awake ish or something. I am going to give a talk about the zcash trusted setup. As many of you know, I was involved in it. The way to start is to answer, what is it?

## What is the zcash trusted setup?

It's a bunch of toxic waste, basically. Zcash has some advanced privacy technology called zkSNARKs. It means that if I have a zcash coin and send it to you, where that coin comes from is essentially completely secret. It could have been any other zcash coin in existence.

To make this math work, you essentially create toxic waste. In cryptography terms, it's kind of like the private key to the public key that proves these proofs. If you have access to this, then you can create zcash out of thin air. So needless to say, you want to dispose of the toxic waste.

## What is the zcash trusted setup MPC?

This is a multi-party computation process for zcash's trusted setup. The idea is that multiple people come together to collaboratively create this toxic waste in such a way that at least in theory, you need all of the in our case 6 people to collude to actually generate that waste for real in one place. You could imagine a nuclear reactor where the waste is dematerialized into six other dimensions.

This sounds good in theory. There's some ec2 machines on AWS forwarding some data, some network machines, and then some airgap. The airgap lets you pass some information, and you hopefully isolate your nodes from the internet, communicate with each other through this airgap, and then do the computation to make it all happen. Sounds simple enough.

## How I became involved in zerocoin and zcash

My involvement in zerocoin goes wnay, way back. This is an email from 2014. Someone was working on zerocoin, which is a similar concept to zcash, but using different cryptography. Long-story short, he wanted to make this happen. Back in 2014, cheap scientist with their stuff. I had been working in crypto for only a few months at this point.

Zooko got involved, and we had a few discussions. He got to the point where he wanted to hire me, but there were some conflicting issues. I sent an email to him saying, if you don't want to work with me that's all good, but what exactly how exactly do you want to make this valuation. He wanted to hire gavinandresen and as we all know he supported Craig Wright.

Still, we kept chatting. When they did finally get private funding and got ready to launch, they asked me again about what I thought about zcash. It seemed reasonable enough to me. I said I had to commend zcash for having the courage to deploy zkSNARKs, and that the whole system could be taken down by an unfortunate bug-- it was an inflation bug and they were lucky enough to find it a month prior.

## Ceremony invitation

When they wanted to do the ceremony, they again contacted me. I thought this was interesting because zooko asked me this through twitter DM. I said, doing this is kind of dangerous because you're going to be potentially compromised when you go do this. This is a lot of money at stake. Currently the zcash market cap is like $500 million USD. The peak was $2-3 billion USD. With this amount of money at stake, what risks are you exposing to others?

I had concerns but I eventually said yes. We got all setup and decided to come up with a plan about what I would actually do to help with the trusted setup. Part of the security of this is that you don't want an adversary to know about this. If you're going to use an airgapped machine, you don't want the adversary to know what the machine is or to even be able to guess it. Zooko and I talked about this. I decided to not tell him what I was doing for the trusted setup. I just asked him for his budget and then did this. Of the six people participating in this, nobody but zooko knew that I was involved. I think there was one other person who to this day hasn't been revealed, and then zooko himself of course.

## The ceremony: compute node

So I rented a car, got some laptops, and traveled a big chunk of British Columbia. If you have a compute node and you're worried about bad guys getting access to it, if you're hurtling down a highway then all the threats have to come from you or the things in your car like cellphones and things like that. I did a pretty good job with this setup, long-story short. The one on my left is the first laptop which I was using to connect to a cell phone, the other one is a network node,. and the one in a tinfoil box is the --- so you could burn CDs and move them back and forth, and ulitmately, get this to-- which, obviously, this is really cool and sexy stuff in Canada, hurtling down to the Rockies and beautiful mountains on either side and wonderful rocks... But that wasn't really true.

## Cypherpunk desert bus

What actually happened was the cypherpunk desert bus. The Canadian rockies gets good cell phone service. So I actually went somewhere else where there's forestry, mining, industry, a lot of trucks, and poor cell service. It's flat and boring. Hundreds and hundreds of kilometers and trees and that's about it, really.

## Cypherpunk desert bus writeup

I wrapped this up and made a 28 page blog post. As you can see, not everyone really liked it, including Emin Gun Sirer... but some people said some reasonable things about this. In my writeup, section 1.1 is about trust and section 1.2 is about a single point of failure. Nothing changes that as much as I can write a story, you're still trusting me and a few other guys. Even if we say all this great stuff, ultimately nothing could have stopped zooko and so on from compromising a setup. And secondly, it was a single point of failure. How did I actually generate the key. Unless the software gets audited, how does anyone know what you did?

## My apology

I should have brought that right up. I found a serious issue. I had a great story about what I did, but it was all based on some artifacts. Like I say in my title, this is hocus pocus meaning nothing. Until we do the foundational part, how do we know what happened?

If we look at the single point of failure diagram, note that these are not independent systems. These are essentially one party, one piece of software that we all ran. So what did that software look like? What's behind that?

We all had a DVD with a full linux distribution. We all booted off of that. We kept copies of that. But how about we go audit what's on that DVD? Here's the first line of the build script that builds that DVD. This is an alpine linux distribution sha256 02ebc5cfe4b721495135728ab4aea87 .... we made this the base distro. All that software, again, that's 100's of megabytes of binaries and nobody can reasonably disassemble that and reverse engineer what it did. This is one of your roots of trust. Anyone with access to that distro on that day, had full access to the entire distro, and anything we ran on the trusted setup ceremony was on top of that. That's your fundamental base.

It gets worse, too. There was also a rust compiler that we used, but how was it compiled? Some guy ran it on some server somewhere and compliced rustc? How did you know what happened? You kind of don't. You have dozens of megabytes of instructions and nobody can go reverse engineer that really. Also, the compiler was released the day prior. The rationale was that somebody found a bug in rust and maybe that compromises the security. But if that kind of thing can compromise the ceremony then how exactly-- these computers are supposed to be in tinfoil lined boxes with no communication with the outside world. ... This was actually a failure.

There is a lot of unfinished hard work. Some people were trying to replicate the deterministic build. There was a url broken in the build system. I don't think this is indicative of a team that wants to put in an effort for people who want to go check whether this is actually true or really working. The other issue I had was the version of rust they used. In the build script, they specified it as stable, rather than a specific version. So I wonder, did the first team even notice this? If the latest version is updated, and stable is updated, then it's a different version and this breaks the deterministic build. So we're not even fixing really basic build versions? All they had to do was fix this one simple line, and they didn't? This worries me.

## Morgan Peck's phone

Morgan Peck is a journalist who covered zcash. During the ceremony, her phone started acting up. This is from her article. She made a big deal about forensic validation and so on and so forth... but her phone was there. You've got a bunch of hardware, and you have to verify these systems. It's just not happening. You can go on twitter and you can find me prying the zcash team. I was waiting for them to answer and see what they would do, and they just kind of said nothing.

## Risk denial

There's some risk denial going on here. It's not about six independent sources of randomness. Those sources were not random. I didn't know what my compute node actually did. I don't think anyone does. Sorry, this just isn't independent. For us to be promoting this myth in public, isn't really correct.

<https://twitter.com/peterktodd/status/977958044138070017>

## Security theater

We can't hide these risks, we have to be honest about this stuff. What kind of impression are we giving to people when we practice security theater? The crypto was relatively slow. It's considered infeasible to make all of the zcash payments private, unlike monero. It's really slow. A future version should fix this. Part of that process is that we need to run another trusted setup to get that. But this time around, more people can participate in this, which I think is a great thing. This time I think it's 60 people participated rather than just six people. The way the math worked, people could come and go and it just worked.

But there's still this issue about toxic waste from chernobyl, doing setup, and when really you have to look at what you have actually done. Yeah we took a random number generator that gives off of a lot of values, and it's easy to go and tap... Once people see this, they think well what kind of security is this? It's more like mashing keys on a keyboard, which is how I generated the parts of my part of the trusted setup ceremony. I felt pretty comfortable with this.

But this is security theater. Like the drone communication bugs. Look at Andrew Miller's "powers of tau" email to zapps-wg. They needed to prove about when they went and did stuff. I told them to use opentimestamps. On opentimestamps twitter, I keep reminding people that this proves something existed at a certain point in time. When you're saying you have this ceremony to the public, what are you actually telling them? This worries me. In crypto, we need to communicate to the public what the risks are. We can't hype this stuff up. We must explain what can fail, and we need to explain it in terminology that people understand.

These days, I might go choose to do a single party trusted setup and say look it's trusted end of story. Sorry but we don't have the technology right now to do these things well. Yes we have this MPC math, but what we don't have is the more fundamentals like what computers you run on, what do the OSes do, are the OSes deterministic? Until we do, I'm not sure we should be talking about this MPC kind of stuff. We don't have good answers yet. There's a chance that you are going to lose your money.



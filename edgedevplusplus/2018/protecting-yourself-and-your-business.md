---
title: Protecting Yourself And Your Business
transcript_by: Bryan Bishop
tags:
  - security
speakers:
  - Warren Togami
media: https://www.youtube.com/watch?v=ZrZlCpmcvBU
date: 2018-10-05
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/protecting-yourself-and-your-business
---
<https://twitter.com/kanzure/status/1048087226742071296>

## Introduction

Hello. My name is Warren Togami and I will be talking about exchange security. Not only protecting the people but also the business. This has been a topic of interest recently.

## Warren's security background

I have some credibility when it comes to security due to my previous career in open-source software. I have been working on the Linux operating system first with Fedora then with Red Hat for many years. Related to security is the problem of open-source spam filtering (Spamassassin). After that, I did an MBA, and did various security consulting. Later I became a bitcoin developer. A few years ago I was one of the three co-creators of the scalingbitcoin.org conference to bring academic rigor to the bitcoin industry. I hope all of you are attending that conference tomorrow. In 2015, I joined Blockstream. I happen to work at that company, we do things relevant to the crypto-exchange industry but this talk has nothing to do with Blockstream.

## Security is a process, not a product

A general problem especially wiht business-type people is that they see all the marketing for security products and security brands and they do not understand that security is a process, not a product. It's not something you can buy. It's a philosophy, a culture practiced by your people. It's far more than the technology in a company. Ordinary business, like security is often not taken seriously because you can often recover from mistakes or errors in your business. But when it comes to cryptocurrency, errors are not reversible and the consequences are far more dire.

Security can slow down feature development. If you are lacking security, then your years of hard work can be instantly destroyed anyway.

## Some recent hacks

I'll talk about a few recent hacks of bitcoin exchanges from this industry.

* 2012 Bitcoinica hack
* 2014 Bitpay hack
* 2014 Mtgox, Poloniex
* 2015 Cryptsy hack
* 2016 Bitfinex
* Detected attacks: mobile number porting theft, emailed trojan compromising an engineer's laptop

Apparently at Bitcoinica a virtual machine provider called linode.. their customer service infrastructure was hacked and an attacker searched for any reference to bitcoin among their customers, and targeted the virtual machines of 8 customers and stole all of the BTC they could find in there, the largest of which was an exchange and they were robbed of 43,000 BTC which is now a lot of money.

I'll talk a lot more about cloud security a bit later.

In 2014, there was an incident where spearfishing (a targeted email attack) was used to compromise the email of an executive at Bitpay and then the attacker was able to see that the way bitcoin transactions were manually authorized was with email. Using that, they sent fake email and tricked the executive into sending 5,000 BTC to the attacker. The details of this hack were later released due to a lawsuit between Bitpay and their insurance company. That's a combination of social engineering and targeted attacks at someone's browser or email client to compromise their system or their email account.

In 2015, there used to be a prominent cryptocurrency altcoin-only exchange called Cryptsy. Exchanges like this would add every altcoin they could find in existence, with no quality standards. Unfortunately, one of these altcoins had a backdoor. They had a lack of isolation in their server infrastructure and this led to a total compromise and theft of all other assets.

These other examples were known in public. I happen to know other examples of attacks that were detected and thwarted before damage happened.

An entire datacenter was targeted to go after one customer. Luckily, this was detected quickly and no losses occurred. Or, a very common attack in this industry is mobile number porting theft. I know several people in this room have been targeted by this attack. It's not just people at an exchange or people who work on cryptocurrency software but even non-obvious targets like their spouses. They are trying to get information so that they can use social engineering attacks against the people involved. Or, I heard of an incident where an emailed trojan was sent to an engineer and it managed to compromise a laptop. Thankfully, due to precautions inside their company, this was caught very quickly.

This is a survey of hacks that I'm aware of, although there are many examples. I'll go over risk mitigation measures.

## Risk mitigation

There are many considerations when it comes to security. I am going to skip over the obvious ones like physical security. In those examples before, I talked about detection as an important technique. For those who have done system administration, a thing that I often see is that they will only setup a server and the application such that it works but that's where they stop. Or maybe they will lock things down to be a little more paranoid about what the application is allowed to do. One of the names of this is called "the least-privilege principle". The example of this is the firewall where you close all ports and then you only open up the ports that you expect the application to use. For incoming connections, that's where most sysadmins stop. If you're aiming to protect your infrastructure, you want to go even further than that and also block all outbound connections other than the specific resources the operating system and application actually require.

Similar to network-level firewall lockdown with least-privilege, there are even more fine-grained means of locking down resources with mandatory access controls like the-- a very good mechanism in the linux operating system is selinux or security-enhanced linux. It's also known as "that thing where people who installed redhat or fedora and immediately turn it off because it's a pain". It doesn't take that much to learn how to customize these roles. In the documentation, it even shows how to set the selinux to permissive mode, where it will only record what the system is actually doing, and keep a log of all the resources that the application uses and then you could run that log through a tool that would spit out roles for you and then you could apply those roles and change to enforce mode. I would say that's a 99% improvement because if your production system are running in a way where applications are locked down to only what they are supposed to be doing then you could be monitoring the logs and anything that deviates from that behavior will look suspicious.

## Safety-critical engineering process

This is just general security for any company. There are some things that are very specific to our industry because errors are not reversible. There are some types of issues where exchanges can become insolvent even without a hack of the exchange, because we are all so blindly reliant upon software made by other people. The quality of that software differs substantially. One example out of many, from last year, the Ethereum parity wallet... multisignatures are supposed to be more secure than a mono-signature wallet. But if you were using the Parity multisig contract last year, twice all of your money was stolen or destroyed. I haven't heard of exchanges losing money this way, but a lot of ICOs lost a huge amount of money. This kind of thing can easily happen again due to errors. There needs to be a safety culture around how these systems are engineered.

## Write software quickly, patch later

For most software companies, write software quickly patch later makes sense. You can recover from problems. But for cryptocurrency, this is an unacceptable attitude. There are other kinds of engineering where this has been understood for a long time, such as aerospace. Look at the history of rocket boosters and how many of them explode at launch. The 1986 Challenger space shuttle explosion was later found to be... well, I like the way Nick Szabo put it in this tweet. In this tweet from 2015, he's talking about bitcoin but using Challenger as a metaphor.

Blockchain transactions are not reversible. The purpose of a business is business, and the payment tech must be boring. Safety critical engineering process will minimize that business risk.

## Don't trust, verify.

The bitcoin philosophy is don't trust, verify. A goal here is to minimize the need for trust. For years I have been visiting exchanges and talking with people at exchanges. A very common problem of how people have implemented exchanges, especially years ago, is to query their deposit addresses against third-party block explorers to look for deposits. There are problems with this. You are trusting someone else's system while only you are responsible for losses. If you run your own full node, then the cost of automated verification is super low, so why trust a third-party at all?

There are other elements to what I believe is the true meaning of "don't trust, verify". I think that this as a philosophy highlights the bitcoin engineering approach. It's not well understood outside where bitcoin is criticized for moving slowly. Well, there are reasons for moving slowly, that have to do with the peer review process.

## Bitcoin's safety-critical engineering process

If you look at pull requests on github, which is how code changes happen in bitcoin, you'll find examples-- people in this room have a pull request like 9622 which took 7 months and has 120 comments. 10195 took 2 months and has 245 comments. It turned out to be very important for security reasons later. This is 245 comments. This is just examples of the extreme level of care used in bitcoin engineering. Segwit is another example; that took 14 months between design, implementation, review and deployment in a version of Bitcoin Core. Even outside of the bitcoin industry, people are aware of the security disaster that openssl has had called heartbleed, which was the beginning of using brand names for security vulnerabilities. OpenSSL has many other security issues that needed a lot more attention. Bitcoin developers knew this years before heartbleed and had begun on a very narrow replacement for openssl called libsecp256k1. It took years of review and even some formal verification for them to be confident that they had a high level of assurance that libsecp256k1 would work correctly and be secure. In general, the rule in software development is to not roll your own crypto. By eliminating openssl, the attack surface has been reduced.

## Defending people

The first step of defending a company is defending the people. I gave examples of exchanges hacked by tricking people into opening emails that they shouldn't. Social engineering attacks are typically used against a phone company in the U.S., to steal someone's phone number. It's very hard to defend against that. If you're using a mobile number as a second factor authentication for logging into services, I know people who have a second unlisted phone number under someone else's name that they use for that because you can't be too careful especially when you're in this industry.

Copy-paste of cryptocurrency addresses can be very dangerous as well.

## End-user hardware security

One of the defense for end users, not only for wallets like Trezor and Ledger, but also for two-factor authentication and logins used by wallets like GreenAddress green bits, or there are hardware two-factor solutions like yubikey. There's a standard called FIDO which is implemented by-- this is Google's titan key and another popular brand is yubikey. You probably want to lock down your gmail account by this kind of second-factor security if you are in this industry.

## Hardware security

I don't have a good photograph for server-side hardware security, but here's a fun example from a tweet. Earlier today, Tadge was talking about lightning. A drawback of lightning is that the user needs to be online with the private keys, and this can be bad because computers can be hacked especially if they are online. So in this picture, that's the lightning network from earlier this year. In March 2018, someone took a system on a chip and made this into a lightning node that isolates from the main system that is on the network, the private keys, and you can program a thing like this... I personally worked on hardware like this in order to separate like a private key signing from a server for different use cases. You could program rules into this. For example, only sign if the lightning balance goes up. There are some exceptions to that when it comes to balancing, which makes it more complicated.

## Isolation: Do not trust third-party softwre

Isolation of different hardware or software is very important. The biggest example or the easiest example to use is the Cryptsy hack from a few years ago. You really have to be careful about the software you download from other people. In the case of this altcoin, even the backdoor was visible in the source code on github. I'm not sure about this. But it's easy enough to hide backdoors in only the binary so that it's not visible in the source code. The information that the experts at the time heard is that the security practices at Cryptsy were very bad where they were running all of the altcoins daemons on the same machine or maybe even the same non-root account. Just very basic and obvious security isolation measures were completely ignored. I would design things such that you not only don't trust third-party software, but you shouldn't even trust your own software. This is why I recommend the least-privilege principle. You need to create security zones in your system, and you should use one-way logging where you have a notification system. The examples from earlier about hacks that were detected were because of audit logs and notifications and one-way logging which were detecting unusual behavior. You want these systems to be as separated as possible.

## Extreme risk: the cloud is total isolation failure

I'm astounded as to how people don't talk about the extreme risk that "the cloud" has. I've been working on operating systems for now two decades. While working at that company, I witnessed over and over again exploits, local exploits, exploits of hypervisors, container breaks, and this happens over and over again. Recently, there was meltdown and spectre which were also complete breaks for virtualization. The idea of "the cloud" is that you are sharing virtual machine resources on physical servers possibly with other customers. Any of those other companies of your hosting provider could break the physical security and get into the other customer's data, in other words your data. This is even worse for containers; virtual machines have never been secure all these years either. The reason that companies use "the cloud" is because actually it's very convenient and it's great for rapid development. I entirely encourage developers using "the cloud" for prototyping and testing and not production instances of their systems. It's great for on-demand capacity. It's great for cost control. But keep in mind that the bitcoin industry differs from most normal software. We cannot recover from errors. In general, you need to be aware and to appropriately design isolation between systems keeping in mind that virtualization is never secure.

## Spectrum of safety

The cloud industry is sort of aware of those problems. I would stay away from the public clouds like ordinary Amazon AWS. In the case of the 2012 Bitcoinica hack, that was a hack of the Linnode service providers. They were one of the earlier very convenient virtual machine providers. Knowing full well how dangerous these things are, some countries demand that the cloud infrastructure be hosted in their country or their company. The people who sells those to governments have security clearances, and you have to trust that the provider doesn't mess up.

It creates a large attack surface for a bunch of people who work inside those providers and companies. These things are "secure" until they're not.

I have friends who work at "traditional" payment companies in the United States. The consequence of a hack there is significantly smaller and the situation is recoverable in many cases. They don't host their infrastructure in public clouds at all, it's only in-house servers. There are some platforms that give all the convenience of the cloud but on your own hardware in your own company, so then you only need to trust insiders of your own company and hopefully that's safe enough. Keep in mind, it's secure until it's not.

## Server application security

Other popular things for developers include nodejs, npm, golang... These are convenient libraries, you add them as dependencies to your project, and the latest version is downloaded. The problem is that you have no idea what you are downloading. You did not audit this code. The download infrastructure itself may not be safe. There are very paranoid ways of using this. In nodejs, you can lock down your package.json to particular hashes and particular versions--- but nobody does that.

A related issue, this was last year, for a while there were trojans thing in the npm library. I think there was even one case of mainstream modules being compromised. I'm not sure about the details on that.

## Reproducible builds

Another attack that has always been an issue is being able to hide backdoors in compiled binaries. You should first verify if the source code is compromised or broken; nobody checks the source code they use, but maybe with careful peer review of the software you use, and signed commits, and knowing the people involved-- it's kind of like social proof that the source code is maybe safe... But it's possible for entire operating systems and compilers to be compromised in a way that is not visible in the source code. One of the famous papers on this was a 2009 dissertation by Wheeler. Bitcoin developers were among the first to take this as a serious problem and pioneered a tool called gitian. The goal is to make binaries bit-for-bit reproducible no matter who builds it. Gitian is pretty good, but still not safe. It blindly downloads the latest version of Ubuntu and uses that to build and you have no idea what's in there. Due to this, the bitcoin developers have been aware of that risk for years and have been working on a next-generation deterministic build toolchain. There are people in this room working on this, and other people attending Scaling Bitcoin in the next two days are not ready to announce it yet. As our industry deals with larger and larger amounts of money where things are secure until they are not, we need to be especially careful about like the chance of this kind of compromise is very low but it only has to happen once.

Not in my presentation is the risk of hardware attacks. There was something in the news yesterday. There was a Bloomberg article about state-level attacks where a chip was inserted into motherboards. It takes a lot of time, effort and money to do that. To be able to trust the supply chain of hardware, that's a problem described in that article. I'm talking about the supply chain of software here, and we need to be able to fix all of these problems as we deal with larger and larger amounts of value where the stakes are not recoverable.

## Trustless exchange

You also heard earlier today about trustless exchange and atomic swaps, so I don't have to talk too much about this. This is the future, especially when you see time and again exchanges in the past custodial model who are responsible for customer funds getting hacked and losing it over and over again... this runs the risk of regulators panicing and creating rules that are increasingly draconian. That makes me wonder whether the industry will be able to move more towards a trustless model that shifts the liability to personal responsibility of the coin owners.

## Redundant consensus safety

Here's another crypto-industry specific problem... so, when we talk about full nodes and "don't trust, verify", we want everyone to verify for themselves. That's great if it works. The risk of consensus is if your view of the truth differs from other nodes. This can happen due to consensus bugs, sybil attacks, and other problems. No time to explain sybil attacks, just look it up. So one idea is to run multiple alternative implementations and then stop if they get out of sync and get a human operator to investigate. The problem with alternative implementations is that they need to be bug-for-bug compatible and the problem is that bugs are not completely discovered yet (otherwise we would have picked them). The bip66 DER bug due to unexpected behavior in OpenSSL is one example from bitcoin history.

## CJK education project

What I've done in my career for like 20 years in open-source is not only the development of the software, but also like-- organizations and projects to help the industry and the community to do a better job at this work. A few years ago, I was a co-creator of the Scaling Bitcoin conference series. A more recent project with a few people in this room and other people in the community and industry is that we're launching an education project. It's very simple. The bitcoin developers choose or write articles that explain something that is misunderstood, and then through this project it gets translated very carefully into the major languages of the world, especially languages where English is not very strong in their community. In some of these countries, there's not a lot of experts or there might be experts but they don't have time to explain things. So this is translating source material from the experts very carefully, and this sort of material can be more readily quoted and used as source material in media and all sorts of thing in those countries. This is useful for developers in those countries to better understand, learn and get involved. It's also useful for non-developers to learn and get more involved in the industry.

In this room, I would like to introduce Ruben Somsen. We're creating a non-profit organization for Reading Bitcoin. We intend to be working with the Linux Foundation, which has 160 other sub-foundations for various open-source projects. There's a prototype website at readingbitcoin.org, and you can click on the language selector and it shows what this site could be. It's Chinese, Japanese and Korean. We need sponsors in order to do a good job of this. We tried to do this only with volunteers over the past years, and to maintain the quality of translations from volunteers is too difficult. I would encourage you to follow these accounts on twitter and you will see more news as we are bringing these online. We need your help.


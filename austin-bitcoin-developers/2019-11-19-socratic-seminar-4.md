---
title: Socratic Seminar 4
date: 2019-11-19
transcript_by: Bryan Bishop
---
<https://twitter.com/kanzure/status/1196947713658626048>

# Wallet standards organization (WSO)

Make an economic argument for vendors to join an organization and put in some money or effort to build the organization. The economic argument is that the committed members have some level of funds committed, representing some X number of users, and X billion dollars of custodied funds. This can then be used as a compelling argument to get each organization to join and bootstrap the standards body.

The economic argument hasn't worked in entrepreneurial situations. FOMO is an important part of the standards process, and people feel like they have to jump in and play with it. There's definitely a strategy around the technologists making decisions in this area, like with SLIP39, where sometimes you have to threaten to fork someone or go with another approach- but the reality is that it's better to embrace and extend them rather than Microsoft embracing and extending you.

What about companies that believe their wallets are super proprietary, and there are security issues of describing those details in public. So they would only participate by contributing a new development or system. It's unclear how to incentivize companies to join such a standards organization.

A standards organization like IEEE or W3C needs a little bit more of a proof-of-concept in our hands, before going to pitch them. Having more proofs-of-concepts would show we have something solid, and a number of companies that are otherwise competitors working on this together. This is a great place to go back to those companies like Fidelity, Bakkt and ICE and say hey take it to the next level. We never write a standard, we write a spec. We deliver a v0.1 or v0.99 or whatever you want to call it. Once we have something there, we say this spec could become a standard with your involvement and your support and don't you want to be a part of that? And if you're not part of that, then IBM will, or Bakkt will. That's a full time jobs, of someone going around saying that in their ear.

BIPs have become a dumping ground for ideas, some of which get used and some don't. There needs to be standards somewhere. When talking to some people, "standard" has a particular legal definition. A standard is an organization that has applied for something with the United Nations and they have an assembly that says this can be a standard. This is a legal status. These are self-regulatory organizations like FINRA, which regulates banks. They started out as a cooperative organization among banks. What happened with FINRA is they said we need standards, we need to be able to do wire transfers or whatever, and over time the SEC blessed FINRA to be a standards organization. Now instead of being a voluntary organization among banks, they are now regulated and a self-regulatory organization. The same thing might happen in this industry, where the group that writes these standards ends up being blessed by some government or body. SROs are its own little half of this. I don't know what the future is for this space. Right now the blessing is really just getting implemented in Bitcoin Core or something.

You could have a custodial operator, and hand Trezors to each customer. There could be a signature from the customer, before the hardware is sent to them. You don't want one multisig per employee in the operations department because some of them are going to quit, and you can't afford to do constant key rotation.

The motivation to join a standards organization is either to (1) be compliant with an important standard that will bolster your reputation (either for security or otherwise), or (2) benefit from leading the community which can help with hiring, getting bleeding-edge features earlier, or influencing standards directions to benefit certain types of products.

Identifying multisig devices that need to be used needs a standard as well. How do you identify who the other co-signers are, or who they are, or how to contact them? Or what other keys will be required? Another one is a health check-- how do I know the whole setup works? How do I know what the next step in the process is? It's not just testing, but also observation and watchtowers. Part of the problem with orchestration is that your devices are going to be offline. When you need to rotate your identity key, you need some other key, which is committed to by the first key, to say this is rotated. But that information is super secret, and you can't lose your rotation keys. So we used a variant of Shamir secret sharing that is redistributable so that you can change the set of participants. What you need is all the devices online. So I want you to conform some computations to prove you still have the keys. You can also use verifiable secret sharing or linear secret sharing which is compatible with partial signatures, which looks kind of like multisig but it's still Shamir secret sharing at the same time.

If you have a bunch of devices, you might want a healthcheck. You have a device that knows the public keys of all the others. So it could send a message, a heartbeat, it could be encrypted or half diffie-hellman like snicker protocol, and it can include time-based data, like the current bitcoin block header or something. A nonce or something. An orchestration device, can collect all this information, not read any of it because it doesn't have the private keys, and the other devices can say yeah I see the signatures from the other ones and everything is cool. You can have an aggregator for availability.

In a vault construction, some of the devices are supposed to be more accessible than others. Bringing all the devices into the same room short-circuits the purpose of having a vault in the first place or using multisig or something.

There's real value in outlining what a crypto custody audit really looks like. What should customers be looking for? Is there an organization that just attests that a company is doing the right thing? Or could users verify it in some way-- but what if the company is just fooling the users that they are using some standard proposal?

A sophisticated wallet should ask the user to delete the wallet and restore immediately. But companies aren't going to do that, because they just spent all the money getting a user to download the app in the first place. So deleting the app would send retention to zero.

You could use multisig to protect against bitrot, but then you would need a regular healthcheck to make sure the multisig devices aren't experiencing bitrot. You should never store keys off of devices.

Justin has been working on a software implementation of the Glacier protocol. Tails is nice because it wipes everything on shutdown. So you go into the vault and you the tails equipment has no data afterwards. One of the neat implementations is seedpicker.net, where you pick your 23 of your 24 words out of a hat, and the 24th one is a checksum. It prints out 2048 words on paper and then you be your own monkey and draw them out of the hat. And you should put them back each time. The problem is the need for the 24th word... and that's what seedpicker is, but you should run it on tails because you don't want the user to save it on their file. This is somewhat better than putting in dice rolls into a hardware wallet, because you could end up using your attacker's entropy.

Blockchain Commons has been commissioned to write something about the intersection of digital wallets and the identity-key problem space. We came up with some new language for some of that. It would be nice to have some review of this.

Multisig wallets reveal some of the complexity of wallets, which is usually hidden for users that are using single key wallets. But the complexity was really all there; you really should be doing heartbeats, check-ins, tamper-evident checks, etc.

Casa calls it sovereign recovery and they send you your xpubs and bip32 paths by email. It's a product for normies, so yeah. You can setup an airgapped eternally quarantined electrum client, you can put in those xpubs, and generate every receiving address on this. One of the xpubs is held by Casa, and you can't derive your xpubs unless they give it to you. We were trying to pull it out. We were grilling them on this, and Casa was ((REDACTED)). They said we provide it to the users when they request it.... In theory, they do this.

There should be a "bill of rights" for custodial customers, like fiduciary standards that a custodian can not only testify to but prove to you that they are engaged in. Those are the kinds of things that someone who maybe can't do a technical spec or something could help work on, like what are those expectations and what are those questions.

There aren't many strong incentives or pressures. Proof-of-keys Jan3 is kind of interesting and applies some pressures to custodians, but it's not a consistent pressure. A lot of users don't have the expertise to ask for technical excellence, or they wouldn't know how to recognize it or its absence anyway. So there's very little pressure on companies to behave. Perhaps something about engineers and ethics and saying, we won't work somewhere that isn't doing something standardized and reviewed, and this ethical approach could be worn as a badge of honor. Ethical custody is possibly a marketing term that could apply pressure. So it's a marketing effort, and you can enforce trademarks. So this is a certification process, kind of. It's also cheap user education, where the marketing effort basically is paying to convince users to prefer products that are part of this consortium. The member companies fund the marketing effort, and they all benefit from collaborating and being part of the consortium since the products cross-recommend each other or something.

Caravan or something like it is going to get popular, and it will work with the absolute minimum number of signers. Something like, it will push every other manufacturer, because oh it's not compatible with the tool that everyone uses. That's not a subjective thing; it either does owrk or it doesn't. If you want to do multi-hardware multisig, then you can't use that device-- period.

It would be nice to finish the Shamir secret sharing BIP. Get the randomness right. The mnemonics side of slip39 is useful, great for trezor, but not sure how many other people are going to be using that. The underlying Shamir construction is almost 30 years old. The fact that we have no reference implementation for Shamir, is really weird. We're the first community to use Shamir for anything real, and we need to make sure we get it right the first time. With slip39 or not, we have a subset where we need to do a Shamir properly, safe reliable code no dependencies. This is a project that Blockchain Commons is also working on.

Above a commitment to open-source, what is this open collaboration? Being able to fund developers, for example, or other people that could get some of this work done and do it right and architect it well and pay for a design shop. I've been circulating an open development blog post or proposal. The other thing we've been doing is Bitcoin Standup and is a protocol between the network nodes and the.... consensus side.. I'm trying to do that with, to be able to easily setup a consensus on a laptop, VPS or whatever, and ideally at somepoint a wallet-less implementation. Then have a tor connection, v3 authenticated, to a remote that can ask that to do different services on its behalf. We have this up and running on Mac OSX. You don't need to understand xcode to be able to run the app, so I'm looking for some more beta testers. We're also looking for people who aren't xcode people... what are the best practices for setting up a personal node? I have my own opinionated defaults as to all the things in bitcoin.conf, but there's no standard as to a lot of the values in what you should be doing for those settings in a node.

We have had about two hours of intense extremely abstract discussion... How about we take a break for a little bit, and get started in 15 minutes?

# Socratic seminar #4

<https://www.meetup.com/Austin-Bitcoin-Developers/events/266418133/>

<https://bitdevs.org/2019-11-13-socratic-seminar-98>

We just read through bitcoin news. It's been a month or two since our last one. We'll lead some discussions. Some of it is really technical, and some of it is less technical. The idea is to bring some of the knowledge out of the audience and there's some real experts in the audience and hopefully they can educate everyone else. Before that, we're going to have Christopher Allen who is visiting from San Francisco and he's going to talk about Blockchain Commons.

But first we'll start with introductions. When we do the Q&A portion of the socratic seminar in San Francisco, please don't quote someone directly. It's fine to quote things, but don't say specific names. Don't give attributions. This is called Chatham House. If you want to quote something and give proper attribution, then ask them. Don't arbitrarily put it on twitter. This way, your words won't be taken out of context against you.

This is a "socratic" format. There's a number of these groups now in various cities.

<a name="blockchain-commons" />
## Blockchain Commons

This is my 30th year as a digital currency engineer. I started working in 1990 with Xanadu and Digicash on very early digital currencies. I am a coauthor of the TLS/SSL standard, it's the "S" in HTTPS. In more recent years, I've been educating people on blockchain and bitcoin at Blockchain Commons. I have a very popular bitcoin command line course which is a step above most of the intro bitcoin courses, but it's a step different or parallel from what some of the other bitcoin technical courses do. I worked at Blockstream for almost 3 years, doing work on Liquid and sidechains and all that type of stuff. I left them about a year and a half ago for a new organization called Blockchain Commons, which was founded out of my frustration as a 30 year veteran of this field that some of the more fundamental security premises and approaches are failing. How many of you know what Heartbleed is? The world's number one used security software was called OpenSSL and it was developed in 1999 and being used by 60% of the internet... Probably 70-80% of commerce sites. It ended up having a one person supporting it for security updates. A serious bug got into the source code. A year and a half later, they discovered a fairly major attack that had likely been used by the Russian mafia and a few other people before it became publicly disclosed-- maybe it was used by others to basically remotely read private information off of servers. So 60% of the world was using it, but only one person was working on it. It's sort of a tragedy of the commons.

We support blockchain infrastructure. We try to look at the basics and the foundational things that people are forgetting about, or maybe there isn't venture capital money for. We want to fix those or do them in a principled, systemic fashion and try to find a way to support these aspects for long-term. Today, we have great engineers working on bitcoin. In 20 years, this might become boring and they might be off working on something else. We might get into a situation where there's only a few engineers working on bitcoin and maybe it's 50-90% of world's commerce... that could happen, if we're not careful. I'm trying to help prevent that.

We have a number of projects. Our first major one was about smart custody. Smart custody is how do you manage the custody of your own digital assets. A lot of it came out of my interviewing of a variety of hodlers, bitcoin core developers, etc., as to what their practices are for storing digital currency and basically discovering that they were crap. The number of bitcoin core developers or oldtimers that had only one copy of their key and it was on paper, was about 50%. That's totally unacceptable, especially if you have your retirement savings on that piece of paper. I am in California, and they are threatening to cut off my power for the third time this year in order to avoid forest fires. A friend of mine has been in those fires and saw his safes melted to the ground from the fire.

I wrote a book called Smart Custody with a long-time co-author, Shannon Appelcline. It has been supported by many including Unchained and Adamant and others. You can go to the url and download it. You can also go to lulu and get the physical book at cost, which at cost is $13. I am not making any money off of that. I would say it's, not an engineering level. It's supposed to be an approachable document. The idea is that there are some procedures in the middle of the book that tell you what are the best practices today for how to store your digital assets, if you have more than 5% of your net worth in digital assets. At the end of your journey, which will take about 2 hours and $200 of supplies, you will have one of these titanium key storage items-- this is a 24 word key recovery- and you'll systematically test it, erase the devices, restore them, and do test transactions. Does anyone here know what the Glacier protocol is? How many people have implemented it? I haven't found anyone that has actually implemented it, including several of the Glacier protocol reviewers. Perfection is the enemy of the good. This time next year, we might not want to be doing it this way. There might be better best practices or whatever, so this has to evolve.

One of the emerging things that we're working on is basically instead of having it on a recovery key that basically if someone steals that one key, they basically have your assets. But having ways to split it up either with multisig or Shamir secret sharing would be good. You might give one of the partial keys to your mom, your best friend, one might be in a bank vault in Canada or something. There's a lot of strategies for how to split these up.

All of our projects are up on github. The smart custody book is up on github, and you can contribute with git. You can open issues, or fix problems yourself. If you are an engineer or coder, and you have this wonderful new wallet and you want to use it instead of Ledger, then you can fork our document and create your own procedures for your particular hardware. Or you can submit a contribution and we'll have people like Bryan Bishop review it and maybe it will be in the next edition.

We have some iOS reference apps and code. We have something called Bitcoin-Standup. How many people have their own full node? A higher percentage than normal, which should be expected from this community. How many people didn't, because it was too hard? I was someone who did it, but it was also too hard. We're trying to make it a lot easier. Right now it is for Macintosh but we're going to be doing it in a variety of ways. It's a Mac OSX app that will install bitcoin and tor, it will turn on some simple hardening things on your Macintosh to allow you to setup bitcoind, and then you can optionally add things like lightning or btcpay or any number of different things that sit on top of bitcoin, and doing it in a "best practices" way like setting up settings for a home server and we're going to be doing this on Windows too. Maybe there are scenarios where you want to put it on a VPS or in the cloud-- don't put your keys up there, but having a full node in the cloud can also be very useful. At the end of this process, you can run an app called Fully Noded. It's an iOS app that I can basically point to a QR code on my Mac and it will allow my iOS app to securely control over tor, which allows for a lot of secrecy and privacy, to control my app from my iPhone no matter where I am in the world. So I can talk to my full node from my phone, and do multisig transactions or do other things there. It allows you to be self-sovereign, basically.

I like using the term self-sovereign. I coined the term "self-sovereign identity", this is another project of Blockchain Commons called Rebooting Web of Trust. How many people have used PGP? How many of you like using PGP? Okay, well that's another one. PGP is on its 27th or 28th year. Architecture is fundamentally a hack from 1992. It's time for it to go. We have much more modern cryptography and methods and we could make this better. That's another project of Blockchain Commons.

How could you support Blockchain Commons? There's a QR code on all of the pieces of paper here. You can contribute a hundredth of a bitcoin; or you can hit "sponsor" on github and contribute some money each month- or whatever you think is appropriate for what we're doing for the community. A number of people have contributed x days/year of engineering time or documentation time. Mark Friedenbach, a Bitcoin Core engineer, has basically said you have 50 days/year of my time, spend it as you want. Not more than 50. I could give you two weekends a year to do testing, or security review or something. I will give you a week of evenings a year to maybe do some UX work; that's another way you can contribute to the commons through these efforts. I am ChristopherA on twitter, and on gmail, and all the major things. In particular, christophera@blockchaincommons.com ... So that's my intro.

Q: What other things have you learned, observations- interviewing people about their strategies? What were some of the other things?

A: How many people use the extra word that you can add to bip39? That seems to be one of the largest losses in the bitcoin community. It's not well documented. Making mistakes with that, confusing it with another password, there is no error checking. If you mistyped it, it will not tell you that you mistyped it, and then you might move funds into a place that you can never get back to. It's a thing where people think they are protecting themselves, but they end up not protecting themselves. If you're in a place where kidnapping is common, there's use for a 25th word for deniability purposes. But every time you do it, you're moving the problem of secrecy to another place where now you need another procedure and backups of your secret, in order to have another secret that you will need to restore, and you don't want that.

Q: One of the anecdotes from the bitcoin space, I think Stepan Thomas now at Ripple, he stored 7k BTC that was donated to him back in 2012 and he triple-encrypted it and forgot one of the passphrases and now it's lost.

A: The middle of the book is all about adversaries-- it's the 27 digital asset adversaries. This is a personalized way of thinking about the different kinds of things you have to overcome. This could be intimidating. So part of our job is to say, some of these adversaries you shouldn't care about. If you're in the first world, then maybe you don't need to defend against the NSA when the bottom line is that rubberhose is cheap and they might take away your house or home-- so maybe don't focus on things that add extra process fatigue for unnecessary precautions or protections. We hope to teach you how to decide what you need to focus on. This is how we got it into a nice package that you can do in 2 hours, as opposed to 3 days for Glacier which nobody does in practice.

Q: How much time does the prep work take for sitting down and doing the 2 hours?

A: I think you can start straight up. There's a list of purchases and optional purchases at the beginning of it. So I recommend two Ledgers for a variety of reasons.. you want to get the titanium thing.. Amazon has a nice titanium thing for $20 called Coldkey. There's a couple different brands.. Then there's the high-end brand, -- actually, do you have your box? .. Show and tell. The one with the hammer.

For my social key recovery, I want to use 3-of-5, so I might need a few of the titaniums. It might take me more than an hour to hit the hammer on each of the things. And then I can distribute copies to a few different places.

Q: Is anyone working on bridging the gap between ...

A: Under fiduciary law, if you hold keys or funds for anyone else, then you are responsible to them and you cannot basically say oh the contract that you and I have says that I have no warranty. Fiduciary law trumps contract law. One of those particular areas is that if you're going to have someone else's money or digital assets, then you need to have separation of duties. What that means is that you can't have one person do all. So single-key strategies will not work and are not legal if you're holding other people's money. There are some grey areas, like maybe you're holding capital or ICO money that you've received, that may or may not be fiduciary money. Some people say it is, some say it isn't. But the best practices are to use at least two people. But the reality is that, in our world today, a 2-of-3 multisig is a good minimum baseline for anything where there's any question about fiduciary responsibility. It also makes it more secure, and it allows for some more resilience if you do it right. There's a few strategies for doing that; we met for 3 hours before this event, to talk about how to do multisig on multiple wallets. You can do multisig on a single class of wallets, like multisig on 3 coldcards and you can do multisig by exchanging tiny sdcards and it's hard to tell who owns each sdcard. It's emerging, though. What can we do to make it easier or better? Unchained Capital has proposed a "transaction planner" that sits above and helps you manage the fact that you have a Trezor for one of the keys, a Ledger for one of them, or some other device, how can we make that work and make it as easy as possible? Caravan was announced recently. Blockchain Commons has been involved in the discussions a little bit. Take a look at the video, I think that's going to be an important future. I think everyone in the Bitcoin Core community think it is the future of these kind of wallets.

Q: We're also trying to do a smart custody bridge... how and where should you hold the other keys? How do you think about it? There are some twisty things like, there's the-- the harder you-- the more you increase the security of it against certain kinds of adversaries, you're also raising the risk that something will go wrong or something in the processes will cause you to fail and then you will lose your access to funds. So this is the fatigue that you have because of elaborate processes, versus the risk of having somebody attack you or use your elaborat processes against you. There's a balancing act there, and it comes down to preferences and your particular needs. So how do you think about it? We have some good stock answers in the Smart Custody document.. and then from there you can say, oh I'm a little different because I travel to somewhere that has a kidnapping issue so maybe I should do something with anti-coercion rubberhose type of thing- which we don't usually recommend for US citizens or most of Europe.

Q: How many people here know what taproot and schnorr is? Led by Pieter Wuille, Andrew Poelstra and others, they have been working on a soft-fork. I'd say it's definitely bigger than the bech32 change. A variety of PRs and proposals have been laid out for how to do it, such as in BIPs and now some PRs. There was a call by Bitcoin Optech...  are running the reviews I think? Xapo maybe? They are putting together IRC meetings where they are focusing on different parts of taproot/schnorr, and the groups would work through problems and questions. They expected a few dozen, but it turned out to be like 150 people that show up to these meetings. They are finding really interesting things. If you're familiar with bech32, one of the cool things about it is that it has some more error correction support in it. Someone discovered something obscure, which is you can put a p or q in there and turn a 24-byte key into a 32-byte key, as a particular flaw in there. I have no idea how they figured out this flaw, it's something that has been in Bitcoin Core for a few years, so this review process is really good. I've also heard from a few people that they have done a good job of finding places for people who aren't at the same level of coding and finding useful things for them to do in this review. If you feel like, I've only compiled bitcoin once and I have no idea how I did it, or whatever, then there might still be a place for you to help out with these types of things. If you have customized your own bitcoind and added in some hacks from some other places, then you should be at a lot of these IRC meetings.

Optech did these full-day workshops in New York and Bryan Bishop was there as well... They setup some basic code to play with taproot.  We were thinking about running one of those workshops here in Austin for like a day, to go through all the materials that Optech put together. Who here would be interested in this? They have videos, Jupyter notebooks and transcripts. Who here would be willing to show up to one of those? Oh, fantastic. Okay, so we'll probably do that then. The one in New York was really good. With that number of people, they might send someone, or Mike Schmidt, or Poelstra... we can drag him across the river.

# Socratic seminar

<https://bitdevs.org/2019-10-24-socratic-seminar-97>

<https://bitdevs.org/2019-11-13-socratic-seminar-98>

## Taproot and address formats

Taproot is going to use this new bech32 address format. There's some discussion about whether we want to include the legacy address format in this upcoming proposal, like this pay-to-scripthash support. It looks like they are trying to drop it completely. Are there any opinions or comments about this?

Q: How would it change?

A: It's going to be the new bech32 address format, like bc2, the second segwit version. That's what the addresses will be. They are putting the call out there to say, is there any reason to support p2sh with this? So far it doesn't seem like anyone is demanding it. This would be version 2. If you still don't support segwit and bech32, then something else is going on and you're not going to be supporting taproot anyway. So it forces people to upgrade to keep up.. Having the wrap support just adds complexity to the implementation of the new address format, if you've looked at any implementations that do the p2sh wrap, it's just extra recursively going through the address.

Q: So if you want to support taproot, then you have to use bech32 addresses?

A: Yes, there's only one address format. It's interesting that Bitcoin doesn't drop these old formats. That was one of the arguments for the segwit upgrade in the first place; a more streamlined approach to doing version upgrades. Now you can see the witness version; so it's more clearcut. Moving funds from the old format, is what the wrapped version is for.

## Erlay

There's a new transaction relay system called Erlay. Right now, every pair in the graph of the p2p graph is going to send transactions back and forth but Erlay is a new technology to only figure out who needs to know it, and only send in that situation. This is especially interesting for the network aspects. This will reduce bandwidth used by bitcoin nodes by almost an order of magnitude. It's not a consensus change, so it's pretty impressive.

Q: If you look at the time it takes to validate a block, that's partially driven by the delta of transactions that I don't have versus the ones that I had previously validated. If you add additional delay to the transactions going across the network in a situation where you're not pulling a majority of the transactions from the mempool, adding that delay means validating... ...

A: Well, erlay reduces the delay.

## Lightning bug

There was a big lightning bug in all lightning clients a few months ago.

## Exchange operation at BTSE

There was a cool chat with one of the exchange engineers. One of the interesting points was the difference between, basically, using segwit in a 2-of-3 transaction will save fees by 44% which is a pretty interesting anecdote from this interview. Segwit really helped with multisig in terms of fees. You can see this pretty easily if you look at blockstream.info which tells you hey look idiot you could have saved xyz in fees if you would have used segwit. So that's pretty nice.

## Bitcoin Core release candidate

There's a new release candidate for Bitcoin Core. It's 0.19rc1. There's a new one out for testing. If you're somewhat technical, download it and use it in your everyday usage and this will help iron out bugs. This is completely volunteer driven, so this helps.

## Default address

There were some recent changes in Bitcoin Core, this one changes the default address for RPC users. This is for users who are sending messages to bitcoind from somewhere other than GUIs like Fully Noded app or Caravan might use RPC interfaces. It switches the address to the new bech32 address format, as a default.

There was another similar change for GUI users. That required two different changes, I found that interesting.

## pyln

This is a partial python implementation of lightning network. I think this is the one that Rusty was using to find the bug. He was trying to test multiple lightning clients at the same time.

## The lightning bug

When you open up a lightning channel, there's a-- okay, so here we go. There are two parties to a lightning channel. This guy opens the channel, and this one goes along with the channel opening procedure. Basically, you can fool the other party and say yes the channel has been opened. It did not require the receiver to actually check that the transaction is the one promised by the funder: both the amount and the actual scriptpubkey. They check everything abou what happens when the channel is stopped, but they won't actually check that the money locked up in the channel was really locked up in the first place. This bug was least bad in eclair, but it was pretty bad in c-lightning. The root cause was that there was a spec for lightning, multiple implementations were encouraged, and they forgot to include this in the spec so all the coders wrote code that was clearly wrong.. which is horrifying.

Another really interesting thing here was the timeline of the discovery. It was discovered on June 27th and it wasn't disclosed until 3 months later because they were trying to make sure that everyone upgraded their software. They released a fix within a few days. But they wanted people to slowly upgrade. The disclosure is, it's like a multisig.... When you're dealing with a disclosure of vulnerabilities in open source projects, where people are voluntarily and running-- if you disclose before enough people have upgraded, then you're giving attackers the tools to attack a bunch of people that haven't upgraded yet. Disclosure is hard, especially for altcoins that copy Bitcoin Core....

Some tried to exploit the c-lightning bug. It was discussed on twitter. This was at bitdevs 97. Rusty gave a great explanation of this. Someone figured it out, but they didn't steal much. We think it was probably some engineer just trying to see if they could do it, not an actual attack of any large magnitude.

## Cryptoeconomics summit

There were some really good talks here at the MIT conference. There were a few good talks in particular... one was from Cory Fields, about problems in Bitcoin Core and things like that. One was about critical CVEs in Bitcoin... These were really interesting. If you want to learn about bitcoin security, then give this a look. There was also a great section about what the worst case malware would be for bitcoin. That was really interesting.

## Output descriptors

Output descriptors are another interesting thing being developed. They have been implemented in Bitcoin Core.

## Taproot review

All the best engineers are in the taproot review IRC channel and it's really high quality discussions.

## Electrum-lightning support

Someone was talking about the different responsibilities of a wallet... the thing that watches the blockchain, the thing that manages keys, and the thing that plans out transactions. Those should all be separate. Electrum is the opposite approach, it's a monolithic implementation and now it does lightning. If it works, then it would be amazing. If it would work on tails, then that would be great. Why wouldn't it? Nothing works on tails. Tails went for like almost a year with no working bitcoin support because the electrum/lightning people do their debian version last or something, it's low priority for them. You're using tials with electrum? There are use cases for it. Using tails with electrum is worthless, .... well, you can use Electrum Personal Server, which you can use on tails.

## 600,000 blocks

We hit 600,000 blocks on the blockchain recently. So that's fun.

## Simplicity

Do you want to give a brief overview of Simplicity? There was a first transaction on a test environment for Simplicity.

There's a general problem of how do you formally prove any code. We can obviously have code where you have different extremes and limits that can cause code to do things you don't expect them to do. You need a formal description of what you want the code to do, and then formally prove that your code does that thing without errors. This is a big challenge. There are various small domains where people have been able to do this, like in flight controllers in aircraft. The reason why it's only these constrained problem domains is because that's simpler, and doing formal verification of anything biger is an enormous undertaking.

Russell said, well, we have tools like coq for doing proofs-- but could we create a language that from the beginning it's designed to use these tools to prove these statements? Instead of taking a computer language and trying to prove it, he's trying to take proving tools and trying to create a language that would be easy to prove.

He calls it Simplicity, but it's not simple. It's simple from the perspective of a prover; a prover can test this code and make sure it ensures its guarantees. This is in some ways at that level, the ideal thing to write cryptocurrency code with. If it's specified correctly, then the code can be proven that it will not do something stupid. Russell has been working on this for a couple of years, it's pretty abstract.

They were able to create a branch on the elements sidechain to do Simplicity transactions. It's the first step- I kind of compare it to, how along did Elements do Schnorr? Uh, 2015? Yeah, a few years ago. To get this into bitcoin, this would be a new scripting version.

It's not actually a langugae. It's more of a computational model.. it's more like a Turing computer or a lambda calculus. It's a method of computation. Compilers of simpler languages like python will target it as the output. It can also be mapped directly onto a rank-one constraint circuit, which can be turned into a zero-knowledge proof. In the future, you could provide a zero-knowledge proof without telling someone what your script is.

## Miniscript

Miniscript is half-way between.... Would miniscript and simplicity work together? They are completely unrelated. Miniscript is a simplification of bitcoin script for the most common use cases. Simplicity is more about starting from scratch. Last time, we had Andrew here and he gave us a nice little discussion on miniscript.

## bip70 and the travel rule

There was a demo wallet made by Singapore and some accounting firm... it's a wallet that can only send to wallets that understand its protocol, and it includes travel rule info. There's many bad ways of doing this. If we're not careful, then one of the bad ways will get broad support from industry. So ideally we can focus on privacy and keeping as much as possible while also being compliant.

## Don't query all DNS seeds at once

This is PR 15558. There's like a few bitcoin developers that run seed nodes. It used to be, when you started your node, it would query all the nodes at the same time. So these DNS seeds would have a relatively complete view of the whole network. So now it only asks 3 of the nodes. If you only query one, there's an eclipse vulnerability and if that node lies to you you're in big trouble. But you don't want to query them all, so you reduce the visibility these things have into the state of the network. There's some interesting questions here.

Another issue is that everyone runs the same DNS seed. Pieter Wuille wrote it, and everyone else uses it. It's an interesting things. In my class, I have people write a DNS seed and bootstrap Bitcoin Core on their own. If there's a bug in the DNS seed implementation, then all the nodes could be brought down by that bug potentially. It hasn't failed for five years, so it's probably okay, but it could be significant.

## Kyrgyzstan

Kyrgyzstan shut off some miners because they were using too much power. In Monglolia, some regulators or Chinese regulators were complaining about Chinese mining. Mongolia... only 23.16% renewable, sothey are pretty dirty energy. It's kind of interesting. One of the other things going on is that a lot of the US coal is now uneconomical in the US, but it's economical to ship it to China and for China to burn it. Chinese don't like paying Americans for anything, so they want to have less purchase of coal from the United States.

## DIY bitcoin hardware

Stepan Snigirev was here a few months ago, and going through all the DIY hardware wallet projects that we know of. Like build your own trezors or all kinds of stuff. If you like to tinker, check out this project of ours.

## Quantum resistance

Andrew Chow had a great question on Stack Overflow where it's asking-- does hashing public keys provide quantum resistance? I am looking at Bob because he's one of three people that understands this in bitcoin. He made a good argument that, p2pkh does not provide quantum resistance. He gave a number of things I'll run through. When you spend a p2pkh transaction, you reveal the pubkey when you spend it. If someone has a super powerful quantum computer, they can use your public key to presumably-- break your key hash-- if you reuse addresses.

Q: Will there be a point where somebody uses a very early quantum computational device to start going after early bitcoin with public keys exposed, things like keys that were exposed on altcoins but not exposed on bitcoin etc? In an attempt, so one question is, will that be an early warning system for bitcoin that something weird is happening, or will the price immediately collapse because the process has begun of destroying bitcoin? I think Pieter Wuille has been arguing that, no, once this starts happening then it puts all of bitcoin immediately at risk and we can't wait for a warning sign of early quantum supremacy.

According to Pieter Wuille's analysis, about 30% of the existing UTXOs out there are exposed and already have a public key on the blockchain that has been revealed. So 30% is already vulnerable to such a quantum computer. If you have a quantum computer, then what do you do with it? The number of quantum gates you need to compute a sha256 hash is approximately the same as the ones required to break an EC circuit. sha256 is millions of qubits. Right now, we're at 50 physical qubits which is less than 1 logical qubit. So we can't compute anything right now. My background is in theoretical physics. On physics grounds, I don't think we're ever going to see a quantum computer.

The reason why a lot of people are doing quantum cryptography is because that's where grant money is and how you can get stuff published. My informal survey of most of these, of at least a decent percentage of them, of even the people doing this work, they are saying 2050-2060 maybe 50% chance that quantum computing will be there at that point. So there's people building their careers on this and they still believe this is a longshot. That's just the computation side. On the physics side, they say we're scaling up qubits from virtual to logical or whatever, that classic computational constraints will creep in with error correction and so on.

You have to describe a wave function with the accuracy of 256 bits.. It's just physically impossible, so if that statement is true, then a physical quantum computer is impossible. We don't know how to build a big quantum computer yet, which is the fact of the matter. It's a great way to make money in academia right now, think about it as another altcoin scam or something. There are hundreds if not billions of dollars of money getting put into research quantum computers. Google saying "we have quantum supremacy".... There were literally ICOs around this, and this is how Ethereum was started with Vitalik right?

We should put a nail in this coffin though. If we're going to deploy taproot, and quantum computing people are going to scream.. we're going to have to definitively say this is an issue or it's not, end of discussion. Stepan is also a quantum physicist. So to say this can't happen, is going against quite a large group in academia. To say that it is going to happen, means that we should do something about it. I think this is hard. It's got to be one of these two options: it either happens, or it doesn't happen. If it is really happening, then on some time scale we need to know when should we do something.

It's sort of like fusion. They have been saying fusion is 5-10 years away, for as long as I can remember. It's still 5-10 years away. But you can't steal a bunch of bitcoin with fusion other than mining or something. It's possible to definitively prove that quantum computing is impossible. If someone would like to fund me to do that, I would be happy to do that.

## How does the bech32 length-extension mutation weakness work?

I read this on stackoverflow but I don't really understand it. Pieter Wuille wrote in... it has something to do with bech32 addresses mapping to a polynomial with 32 terms, and the p or the q is like the 1, and you can add a bunch of 1's, and something happens. It's a weakness in bech32. I don't really understand it any more than that. The short-term answer is that we only accept 24 or 32. The long-term answer, is that at some point we will need a new-- a bech64 or a bech48 or whatever, and we'll fix it then. But there is a short-term non-consensus fix, right there.

## CVE-2017-18350

Given how Bitcoin Core... a tor proxy called SOCKS, which is how you use tor, could completely rewrite memory, basically. This is something from like 2012. The fix went in during 2017 and now the disclosure has been released. It was two years after the fact that the disclosure was released. The timeline is interesting. Vulnerability introduced in 2012. Disclosed to security team, two years later. It makes you wonder what kinds of problems are hiding in things at the moment.

## Jameson Lopp testing on different nodes

Jameson did great tests on different nodes and downloading things. Bitcoin Core took the number one slot. bcoin was number two. btcd struggled. libbitcoin also performed as number four. Libbitcoin indexes all the UTXOs so it actually indexes more than just the txindex. It's hard to do a one-to-one comparison. I have heard that libbitcoin makes some extraordinary claims about how fast their initial block download is. They might be developing libbitcoin on highly multicore systems so there's probably a lot of threading that they are relying on. Note that initial block download time is faster with a year's more of blocks with a year more of improvement. Initial block download is really important, and we want that time to continue to go down, because otherwise you can't sync. Someone was trying to sync with Ethereum and it was failing over and over again, but he finally got it to work after two months. It was an interesting blog post.

# Bitcoin public keys and x-coordinate removal

In bitcoin, public keys are ... the problem is that it's a little larger than 32 bytes. There's a trick that allows it to always be 32 bytes. The problem is that you can say that  removing the y-coordinate might make it less secure. This explains in a really nice way, for someone who doesn't understand how cryptographic proofs are made, why it doesn't reduce security. It's really an elegant explanation for why removing the x coordinate doesn't reduce security. This is for bip-schnorr, which decided to do this a while ago. But the rational wasn't explained at the time.

These public keys are points on a curve that looks like this. You don't really know whether it's on the top half or the bottom half. So there's this byte in front that tells you which one it is. This removes that byte... No, it's a single bit, not a byte. Given the x-coordinate you can calculate the y-coordinate up to the mirror symmetry whether it's top and bottom. And the blog post argues for how you can get away with not having that bit.

Also significant is that they have finally published in the secp256k1 library, a PR for this x-only schnorr. It doesn't look like they will merge it before the taproot proposal gets merged or something. We're still a year or two away from the next step. Blockchain Commons has a fork of that secp256k1-schnorr implementation in the Blockchain Commons github repositories. If you're interested in playing around with Schnorr, it's a really simple and interesting digital signature algorithm. We're overdue to switch form ECDSA to Schnorr signatures.

## Coinbase blog post

<https://blog.coinbase.com/how-coinbase-views-proof-of-work-security-f4ba1a139da0>

This was a great blog post from Coinbase. You don't want to monopolize the hash rate of the algorithm being used; if there's a lot of general purpose hardware that can jump in... So he goes into a lot of reason for why they believe this, and they have some interesting examples from Monero and... to prevent ASICs from coming in, specific computers that go in and do hashing. This is the opposite; people believe that you want specialized hardware which is what bitcoin embraces.

The argument against ASICs is that there's no tradeoff in security but it democratizes it, and anyone can mine it on their computer which is better for the community. But the reverse argument is that it reduces security so much... Anyway, it's impossible to get full ASIC resistance. It raises the entry requirements to make an ASIC ,for an "ASIC resistant" algorithm. It's a walled garden or competitive advantage. This is what you see every time Monero hard-forks their network. I think for the last 3 hard-forks, someone figured out an ASIC each time. Another problem is that the devs know what the next algorithm is going to be, and they could sell this information to a miner, which is an incredible advantage.

## Optical proof of work

No, it's not a real thing yet. It's more hypothetical. We can talk later about this.

## Android NDK build of Bitcoin Core

This can compile Bitcoin Core for android so that's cool.

## UTXO snapshot creation (16899)

jamesob is working on this. This is for dumputxooutset. This defines a way to create UTXO snapshots with an RPC command.

## The node operator's guide to the lightning galaxy

This is a blog post series. It goes over how to run a good routing node. So all the things you'll need to do to setup and kind of the way the ecosystem is developing and how to measure these things. There's a few things in this that I thought were interesting. In this blog post, he talks about how-- one of the problems of the UX issues of lightning that they have to figure out, you can't just submit a transaction to the network and it gets mined. But you have to be connected to some good peers. If you want to send money to a merchant, you have to rely on the peers you are connected to in order to route the payment. So there's a lot of work around how to make sure you're connected to good peers. When you connect to a peer and open a channel, the funds you're committed in that channel are locked up and if it's a bad channel or bad peer then you're out of luck until the expirations.

## Whatsat

<https://github.com/joostjager/whatsat>

This is end-to-end messaging using your lightning node. This is a proof-of-concept for now. There's an update to one of the BOLTs that allowed for arbitrary data to be included in the packet that is being routed around, so this juice-- Joost.... I think he had been pushing for this to happen, and one of the things I... it's arbitrary data that is passed around in onion packets. You can send an arbitrary message to the final destination, but it can also be passed around to individual hops. I don't know if it does that right now. It might only be able to be addressed to the specific destination. For now. There's a whole bunch of things though. This is a cool thing, but at the same time it's kind of an attack since you're not paying the network for this. Basically the way it currently works is that you're sending a payment that you intend to fail, and that's bad because you're adding a burden to everyone on the network. That's also something they have been talking about and most likely it will not be possible in the future.

In the last socratic in San Francisco recently, we had roasbeef and andytoshi and some others. One of my big arguments was that this continues to demonstrate that Lightning in particular has a concept of identity which we are very much in denial of that identity exists. Identity is any time you have a long-term correlation or a public key, then you have an identity. Even more so with lightning, because you have all these funds staked. So you can't just discard a key, because you have to close all those channels or sacrifice the money.

We might be able to charge satoshis to move messages along, and now we have an incentive for replacing asynchronous social network features. But on the other hand, we're also relying on long-term persistent identity stuff which can be used against vendors or free speech. There was a lot of back and forth. Laolu was saying this is a cool thing but maybe it shouldn't be done at this layer, maybe offer it in a safer non-correlatable form at a layer above the payment layer. Whatsat is there whether we like it or not, though.

In finance, the idea of identity is required: you must know who you are paying. So the idea that bitcoin or lightning has no identity, is stupid. At the very least it's TOFU (trust on first use). By being in denial about identity, identity can be pushed to another layer where bad things can happen where we find we more and more can't use bitcoin in the ways that we would like to and the on/off ramps get closed down and make bitcoin less valuable because we're in denial that there are identities here.

There are pragmatic things that we could do, which allow for voluntary disclosure. Every time you send a payment, you're making a voluntary disclosure of your identity that I'm the person sending you money. Your question should be, did someone change the address before you got it? This applies to every payments use case. If you fulfill a lightning invoice and i'ts a multi-hop payment right now, the node that receives the payment has no idea what--- no, that's a donation. If you do not receive a good or service, then it's a donation.

There are situations where the payer's identity are not known, especially if you move to some form of adaptor signatures or something where the payer for these can not be correlated from these one-use keys or something. Hide the payer, good. Even sometimes the payer needs to share information like a refund address or a physical shipping address.

FinCEN guidance a few months ago made it sound like if you're non-custodial and not offering other services, then you would not be considered a money transmitter. There's a little bit of wiggle room. But it's not clear that even a half cent of profit, that might still be caught under those regulations. Wyoming has been looking at this and their money transmitter laws do not consider those kinds of things to be subject to money transmitter laws. They have not yet done an exemption for de minis small payments. There was a proposal in congress I think for de minimis that would be the same as the de minimis is for W2's.

## polar

<https://github.com/jamaljsr/polar>

Testing in bitcoin is easy- just spin up a regtest node. But for lightning, you need a regtest node, two lightning nodes, then you need to fund them, then open the channels, mine more blocks, and then you can start transacting. It's just a huge pain in the ass to set that up. As a result of that, there's been some efforts to help improve that. Hopefully polar will make it easier to play around with lightning. I think UX around a lot of these things is pretty good, but what people mean is user expectations and people aren't used to interacting with money in this way.

I think this one is using lnd over bitcoind. c-lightning and eclair are coming soon. cdecker has a version called lnet.

## lsat

There's been a lot of talk about.... when you can do micropayments online, it opens up this idea of being able to use payments as a form of authentication going back to the identity topic. But you kind of need standardization around that to make it practical. You have servers, clients, browsers and apps and all these different things that aren't aware of each other. This is what the HTTP protocol was all built around, creating standardization. So that servers and clients would know what to expect from each other.

lsat was something htat roasbeef presented at lnconf about using the-- there are two things that are ready to exist in our current internet infrastructure... One of them is the 402 payment required HTTP status code, which was something that was proposed decades ago and we never had a thing for it. Now we have a way to use it. The other bit is the... in the HTTP header field for authorization, there are certain standards around things like-- like if anyone has used oauth where you use a social media login to sign into something else, the basic authorization in the header would be user-password. This would be a new type of authorization format called lsat. Is it authorization or authentication? It's authentication, sorry.

They use macaroons in the HTTP headers, which can also be used for authorizations based on what you put into the macaroon. So you hit a paywall, which you see in the beginning of this terribly compressed twitter video... and it says, you need to pay this invoice before you can make any more requests. This is an LSAT demo with Joule. This is a proof-of-payment essentially, and the browser in the background or the website will pull that secret out, like if you're using lightning-joule, and add that into the authorization header, and along with a macaroon that came back with the 402. So the macaroon is saying here are the caveats you need to satisfy in order for us to let you access this endpoint, and pair that with a proof-of-payment in the form of a secret. So this is an alternative to a username-password combination.

Macaroons are really cool; you can do timelocks that timebox something to be valid for only the next few minutes or whatever. With passwords, even if you're using secure methods to connect to a website, you don't really know how that website is storing your password on their server. But what this does is that it means you're in control of the strength of your own security; you're sending them a secret they already knew. You don't have to trust them to store your authorization credentials at all. If they do a bad job at it, you just get free access to the API or whatever. This is not possible with the current way that people interact with the email. There's a pseudoidentity made possible with cryptocurrency payments.

OCAPs and authorizations and... macaroons. User group access control list method of doing security was started in the 1970s. It was easy and straightforward. Unix started using. Then there was Linux. Now the whole internet is built on Unix and Linux so we have had these authentication-authorization model and it has some fairly interesting security problems. The most well known in that category is the "confused deputy problem". It's basically where you end up accidentally giving more authority to someone. There was an alternative architecture in the 1980s called OCAPs which was more about capabilities and for whatever reason didn't win the hearts and minds of the early internet developers that addressed these problems. It solved some of these things. Because it didn't win, it gave in to the---- one of the reasons it didn't win was because people weren't really doing multiparty computation on multiple machines. One of the first broad internet uses of OCAP was macaroons. If you're really interested in the issues of authorization and least authority and better security, then I encourage you to look at the macaroon stuff.

This is just a demo and it has some pieces to iron out. I built a paywall middleware called boltwall that uses macaroons separate from the lnd stuff. I want to collaborate with them to standardize it a little bit more. It's cool because macaroons let you delegate authorizations, so you can have a third-party that can give you a "discharge macaroon" where we say this third-party needs to authorize and if they don't then I won't give you access. There's some more security and flexibility here than what we currently have with oauth, and combining it with lightning is pretty cool.

## Lightning rod

This is kind of complex, but it's about hodl invoices. You can do some layer 2 smart contracts with hodl invoices.

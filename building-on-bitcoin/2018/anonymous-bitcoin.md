---
title: Anonymous Bitcoin
transcript_by: Bryan Bishop
speakers:
  - Adam Ficsor
date: 2018-07-03
media: https://www.youtube.com/watch?v=QiySI4-MWww
---
<https://twitter.com/kanzure/status/1014128850765303808>

<https://github.com/zkSNACKs/WalletWasabi>

One year ago I was standing here at this conference and Igave a talk. Today I am standing here and I titled my talk "Anonymous bitcoin". One year ago at this conference, the conference was named "breaking bitcoin". I did not break bitcoin. Someone else did, you might remember.

Today I want to present how I build on bitcoin. I have two goals with this presentation. I want to provide a case study of the bitcoin developer and his mistakes and successes. That bitcoin developer is me. The second goal is secret. I will only tell you the goal at the end of the talk.

I organized this talk into thre sections: joinmarket, tumblebit and zerolink. I just want to tell you the differences. These were the things that I pursued. This is something I wanted to achieve in different phases in my bticoin developer career. I will also speak some of the speakers. And hopefully you will want to-- you will wait for their presentation just as much I will be waiting in anticipation.

So first slide. respect my authority. I worked on a few projects. I wanted to talk about zerolink and dotnettor. What I am most proud of is that I became one of the 100 most active contributors on github. Github only countsp eople with 1000 followers. So anyway, this is something that I am proud of, as a ersult of this project.

I am going to talk about what success looks like versus what people think it looks like. People think success is a straight line. But then you start looking into what you contribute to bitcoin. But very often, your goal changes. Success doesn't look like a straight line. It looks like a complex line. In every part of my presentation, my goal changed.

I first looked into bitcoin but I didn't see much for me to do. I was coding in python. There were no tools that I could have used. There were so many things to build. That made me-- just hanging around in social media, or gambling on altcoins and things like that.

And then I was in Taiwan, it was 10pm at night, and I was out of money and I had this job interview as a blockchain developer. I was excited about it. This guy said to me, "hey, f you come tonight, I will buy you a ticket to Thailand". I was excited. I went to Thailand. The guy took me to The Vroots. There were some other developers and they were trying to come up with a blockchain product. The criteria was to come up with anything that was blockchain related. It did not succeed.

That's when I realized that I have to stick to bitcoin. This thing came out called joinmarket  and everyone was excited about it. I built a user interface. I wanted to call their python code from my C# code. It seemed like an easy thing to tackle. I was spending months on this. I was trying to solve this problem. But then I told myself that I was going to rewrite joinmarket in C#.

One of the developers and creator of joinmarket, Adam Gibson (waxwing), is also going to speak at this conference. That's his face in the picture.

I said to myself that I was going to rewrite some parts of joinmarket in C#. For that, I had to learn how to develop in bitcoin and C#. I found that someone built a C# bitcoin library who is also here, NicolasDorier, working on Nbitcoin. I sent an email-- how many messages did you send to Mark Zuckerberg? I sent a lot. I sent a message to this guy too. And he said come to Japan and let's do something. So I found myself a few days later on a plane to Japan. The guy who wrote the dotnet bitcoin library, Nbitcoin, is NocolasDorier, who is also a speaker at this conference.

I went to Japan. He had already written a book called programming the blockchain in C#. At this time, blockchain was not a curse word. So I call it the C# bitcoin book now. I rewrote the book to my level. I wextended the concepts and ut it on github. That's how I learned bitcoin programming.

I wanted Nicolas to come and do joinmarket with me. But he wasn't interested in privacy. By the time that I-- there was so much more going on in bitcoin, and a rewrite would not happen in a few months. And then I realized that I should just learn python.

I wanted to write an http communication system or daemon for joinmarket so that I can finally connect my code with it. But then NicolasDorier sent me a message that hey did you hear about this thing called joinmarket-- no, called tumblebit. I told him yes, I've heard of it, it's very complex. Why don't you do joinmarket with me? And then he said no  I'm going to code tumblebit. It's much easier than joinmarket.

"I was wrong" - NicolasDorier (a comment from the audience)

Tumblebit is a uni-directional payment hub like the lightning network but without the network part. It's anonymous. There's two modes to tumblebit. One is the payment hub mode and the other is the other mode.

Joinmarket-- the difference between joinmarket and tumblebit is the size of the anonymity set. Joinmarket is instant, though. I started to work on tumblebit but first I had to understand what tumblebit is. It's not an easy job. There's only the whitepaper.

I started writing a bog post called "understanding tumblebit" and it was a series. With these blog posts, I was starting to understand tumblebit. One of the things is that it needs tor.

Microsoft was already open-sourcing a cross-platform dot net at the time. The cross-platform for dot net is dot net Core. We decided to go with that, but ther ewas no Tor library for that. Tor is an anonymity network for those who don't know. There was no tor library for dot net. So I wrote a tor library. It's called dotNetTor and I am still maintaining that on github.

<https://github.com/nopara73/DotNetTor>

Now we have tor in dot net. We have tumblebit. I realized something else too. There is no litewallet that would not fail on the privacy level on the network at this level. Every lite wallet is vulnerable to network analysis. With most lite wallets, it's easy to see because it's querying a bitcoin API. It's just conneted togethe. With SPV wallets, i'ts a little more subtle. Jonas Nick is also a speaker at this conference and he has de-anonymized a lot of SPV wallets. He said, give me one of your bitcoin addresses, and 70% of your wallet addresses. That's pretty scary.

I was looking into, what can you do? Building tumblebit on Bitcoin Core would mean that you have no users, no anonymity set, it's just not going to work like that.

I was looking at-- a place to do it-- and Jonas Schnelli had a pull request into Bitcoin Core, he is also a speaker at this conference- and he built a full block downloading SPV wallet which is kind of like a full node but it does SPV verification and it only downloads the blocks from the creation of the wallet. That pull request to Bitcoin Core is still there. I'd like to see some progress on that, you guys.

I built my own full block SPV downloading wallet in dot net. I called it... something wallet.. By the way, the idea of it, goes back to the joinmarket phase. I built that wallet, which was lite-ish. That was good enough.

One of the interesting things I realized while I was building the wallet was that fee estimation is non-deterministic. You don't know the fee before you know the transaction size. You don't know the transaction size until you calculate the fee. Think about that.

The lite wallet is ready. It does not expose your links between your addresses on the network. The tor library is ready. Tumblebit is ready. I was integrating tumblebit into the wallet. And then Itook a step back and I wrote a blog post.

<https://medium.com/@nopara73/tumblebit-vs-coinjoin-15e5a7d58e3>

I compared tumblebit and coinjoin. Joinmarket is coinjoin. Tumblebit's classic tumble mode and joinmarket.... there was something that I didn't know existed, called coinshuffle, which existed at the time. It didn't click for me. I realized that ... the classic tumbler mode.. the network fees were at the time were going up, like crazy, and tumblebit wruns were taking two hours, today it takes 6 hours, so it's not getting better. The fees get higher and there's this coinjoin ... that... that might, that might perform much better in almost every way. So I was looking to see if this thing existed. I found coinshuffle, but it was so complex, that, I think it would take a lot of time for developers to get a good handle on it. So I was looking into something else.

Does anyone know who is gmaxwell? The other one is David Chaum, in the picture.

gmaxwell made a 2013 bitcointalk post where he wrote an idea about how can we do coinjoin as envisioned, with David Chaum's blind signatures. It was just two lines of writing and he then inside a fragmented question section-- nobody seemed to notice this-- Iasked Ethan Heilman, one of the creators of tumblebit, look at this, you wrote something in the tumblebit whitepaper about coinjoin, but it seems to work properly this way. And he goes, "oh really? I read that blog post a thousand times and I never seemed to notice this". So it seemed to be pretty hidden. Nobody was doing chaumian coinjoin. Yeah...

So I got into that. It was a pretty hard realization. When you spend... probably a year to work on tumblebit an then you find something that works probably better in every way, so... so for example, tumblebit rounds take hour, and chaumian coinjoin rounds take seconds at most minutes. Tumblebit rounds are 4x more expensive than the coinjoin rounds. So this kind of differences there are. It was really hard to realize that. There was this quote that-- from Eugene T. Gendlin- what's true is already so, owning up to it doesn't make it worse.

If you think about this quote, in terms of the scaling debate, it works pretty well. People didn't own up to the truth of the lack of scalability of the blockchain. So I owned up to the truth that chaumian coinjoin was better.

Zerolink

<https://www.youtube.com/watch?v=RY-QQOjycgI>

Zerolink is-- even if you have a privacy technique on the blockchain- you have to look at what happens before and after the mix. Zerolink puts them together and says you have to look at how you broadcast your transactions, how do you set your fees, just all this linking metadata on the blockchain. I presented zerolink one year ago at Breaking Bitcoin 2017.

With the help of Matthew, we implemented zerolink into the wallet.  And finally we were doing public testing in December.

It didn't go that well.

We wanted 100 people to join the mix. We wanted an anonymity set of size 100. That's something that even an altcoin would be doing. Maybe zcash but they don't because nobody is actually using it. I like the privacy altcoins. I would prefer to not say bad things about people working on privacy. I like privacy. The biggest mix that we were able to achieve was 26 people.

I went to scalingbitcoin 2017 in the US.  At the border, they asked me, why did I come to the US. I told them I came for a bitcoin conference. And they said, okay, come with me. Okay, why. They said just come with me. But why? Just come with me. They took me to a room. There were a couple of people in the room. I tweeted that they were taking me somewhere. They started shouting at me. Put down your phone, don't get it out again. I was terrified. I couldn't use technology. I had to stay down. I was asking why I was there. I had to sit there not doing anything just thinking for 12+ hours. I was terrified.  Maybe they knew I was working on privacy in bitcoin? This resonated in me, that working on privacy in bitcoin, I don't think I can go to the US anymore. I think I should not. Should I even release this software? Is it even a good idea?  Anyway long story short, they had a shift change and they had no idea why I was there.

So then I figured I should delay the release a bit. WIth the help of Lucas Ontivero, we did as much as we could. We did regression tests, continuous integration cross platform, added 10x more unit tests, rewrote the tor library. It's fun to rewrite an http protocol from scratch. You write something that is specified. It's very rare that this is how you write software- already having the spec. It's nice. Anyway.

And then we came to the idea that I should find some lawyers and team up with them. So Gergley Hajdu, Balint Harmat. They are here in this room. We work on zkSNACKs - unfairly private.  This was after blockdigest series named after a blockdigest series. Thanks for that digest.

When I first went to Gergely- who was my university law teacher- they said, this is a crazy idea, this is-- you can't do this. You cannot build privacy on bitcoin. Something like that. But later they came back to me and said this could work. There are some very strong privacy laws in a lot of countries. We could make this work I think. So we founded a company.

We renamed HiddenWallet to Wasabi Wallet.  Full block SPV became bip157-158. Wasabi is a snack food or something like that. Electron became Avalonia.

The lightning devs introduced bip157 and bip158, which is the replacement of bloom filters in SPV wallets. The original bloom stuff was terrible. You setup some filters and then from those filters you can figure out which blocks you are interested in. You can get those blocks from random nodes, and then nobody can figure out which blocks you're interested in, and if you change tor circuits, it's hard for anyone to know what you're looking for. So this doesn't harm your privacy. We implemented it. We are probably the first one to release it on the testnet. Bitcoin Core nodes don't support it yet. We have our own backend that sends it... to the clients.. and that's how it works.

And finally, we replaced electron with avalonia, with the help of Dan Walmsley. Avalonia is a native.. dot net.. user graphical interface framework and I succeeded to get one of the maintainers of Avalonia here to work with us. That's an interesting story too.

He said that he doesn't have time, but he's going to ... to this one, and come to this one and that's what we did, and then they asked me about a conference to speak, and I said I don't have time, I'm going to be in Lisbon, and then they said well the conference is in Lisbon too... and I said alright tht's just great.

Wasabi Wallet is almost finished.

<https://github.comzkSNACKs/WalletWasabi>

The 10 year anniversary of the Satoshi whitepaper is coming up. It would be great to be able to use bitcoin in a fully anonymous way with wasabi wallet on that date. I want you to join your coin with mine. Thank you.

# Q&A

Q: What is wasabi based on?

A: Coinjoin. Zerolink is a framework. Coinjoin is a mixing technique.

Q: Tumblebit, compared to coinjoin, you cannot link one input to one output. That's one big difference. The other big difference is that there's a server that allows different people to come togheter but doesn't know where the coins go. It has a different security assumption. That said, I'm excited about it. The server doesn't know where the coin comes from and where it goes.

A: That's the same with chaumian coinjoin. Tumblebit transactions are recognizable on the blockchain, unfortunately.

Q: If we had good anonymity set, then it would be better Also, we should taproot and graftroot to hide the contracts, and that would make them indistinguishable. But yeah, right now, coinjoin seems like the way to go.

A: Are scriptless scripts going to enable that?

Q: I am not sure. We can hide the contracts. That would make me able to--  people wont be able to identify these transactions. It would remove some of the stuff that deanonymizes me and links it to me and stuff like that.

Q: How does your work relate to confidential transactions and bulletproofs?

A: In every mixing technique except joinmarket, you have to do rounds. The amount has to match everyone else, otherwise you could deanonymize it quite easily. Confidential transactions would fix this. I hope we're going to see confidential transactions in bitcoin when it gets secure enough.

Q: And then you can combine it with your framework for even more privacy

A: Yes. There's time to figure out how to combine it.

Q: In joinmarket, ther's an incentive structure to motivate people to provide their coins for the market. To provide more anonymity. Is there anything like that in wasabi wallet?

A: There is nothing like that in wasabi wallet. The only incentive is anonymity.  Joinmarket has market makers and market takers. You guys are market makers waiting for someone like me to come and want to join your coins, and join my coins together with you, you and you. That's what joinmarket does. Some people are waiting, they join coins together, and I pay some fee for you guys to join your coins with mine. This is the thing about coinjoin.. you're not going to pay 100 people to have an anonymity set of 100.  And you're not going to wait for other people to make a large coinjoin and schedule it.

Q: What about lightning?

A: Lightning and coinjoin is an interesting idea. This is pretty good. You don't need a -- you are okay with.. to open the channel.. that would be a good use case. There are a lot of things to fix about privacy and that's what's prioritized.

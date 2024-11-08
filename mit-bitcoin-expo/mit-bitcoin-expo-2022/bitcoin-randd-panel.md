---
title: Bitcoin R&D Panel
transcript_by: WeAreAllHodlonaut via review.btctranscripts.com
media: https://www.youtube.com/watch?v=UIkvHzPIgRM
tags:
  - research
  - covenants
  - scripts-addresses
speakers:
  - Jeremy Rubin
  - Gloria Zhao
  - Andrew Poelstra
date: 2022-05-07
---
Ayush: 00:00:07

My name is Ayush Khandelwal.
I am a software engineer at Google.
I run a tech crypto-focused podcast on the side.
And I have some amazing guests with me.
So if you want to introduce yourself, what do you work on?
And yeah, just get us started.

Jeremy: 00:00:31

I am Jeremy Rubin.
I am a class of 2016 MIT alumni, so it's good to be back on campus.
And currently I work on trying to make Bitcoin the best possible platform for capitalism, sort of my North Star.

Ayush: 00:00:51

Noble mission.

Gloria: 00:00:55

I'm Gloria Zhao.
I did not go to MIT and I don't work at Google.
I went to Berkeley, go Bears.
So I work on Bitcoin Core, mostly transaction relay and mempool.
I work on package relay, if anyone's heard of that.
And I'm sponsored by Brink.

Andrew: 00:01:22

Hi, I'm Andrew Polstra.
I went to the University of Texas at Austin since we're doing this.
I'm the Director of Research at Blockstream and I've been involved in a number of different privacy and scalability technologies over the last few years.
But lately, I'm working on more boring kind of wallet stuff, interoperability, key storage, key management protocols.

Ayush: 00:01:49

Useful things.
All right, so the goal of this panel is to focus on Bitcoin research and development.
We hope to leave you slightly excited about the future of Bitcoin and all the exciting work that's actually taking place right now.
So Jeremy, this is a question for you to start us off.
Paint me a picture, if you will.
The year is 2040.
Do you think people are still using Bitcoin?
And if so, what is the day-to-day transaction, what does it look like, what is the user experience like in the year 2040?

Jeremy: 00:02:24

Yeah, so let's see, that's about 18 years away, so a little bit of time.
I think the things that I would really like to see happen by then would be a lot more scalability with the combination of self-sovereignty.
What that would mean to me is that everybody would be able to, and when I say everybody, I mean everyone in the world would be able to have Bitcoin that they can say this is mine and nobody can take it away from me under a reasonable security model is what I would really like to see.
I'm a little bit more skeptical that we're gonna be able to achieve results around privacy, for example.
I think the self-sovereignty and scalability will be able to do probably on that sort of timeline.

Ayush: 00:03:10

Do you have anything to add to this, Gloria?

Gloria: 00:03:14

Well, I would hope in 2040 anyone in the world can pay anyone, regardless of where they're living, what their political views are, and what they work in.

Ayush: 00:03:28

So what do you think are some of the key problems we need to solve to reach that stage?

Andrew: 00:03:35

So, there are two ways that we can answer that.
Probably for this panel, I should say, the two key problems are scalability and privacy, or self-sovereignty.
I guess that's three things.
The other answer I could give is more user-focused, and say, well, the two big things that we need to solve are the user experience, like how can Bitcoin be understandable, how can you use it, and the way that you use other payment rails, that kind of thing.
And then also key management, it was a related but distinct thing.
How can you store your keys in a way that they're not going to get leaked, they're not going to get destroyed, they'll work with whatever wallet you might have even as years and decades go by?
And how can you be comfortable with that, right?
Like who is in charge of custodying your coins and what technologies are they using and how do you split that up?
And there's a lot of questions there.

Ayush: 00:04:25

Yeah, so focusing on security and privacy, a lot of people store Bitcoin in custodial wallets currently.
Do you think there's something wrong with storing your crypto in a custodial wallet?
Do you think it's inherently insecure?
And do you think there are better ways to store crypto?

Andrew: 00:04:44

I think it's probably a bad trade-off.
It's a complicated thing, right?
So if you have your coins on like Coinbase or something like that, on the one hand, you're trusting Coinbase to not lose them, to not get hacked, to not have a database failure that all their backups fail or something catastrophic like that.
You're implicitly trusting their software developers and their security team and stuff like that to make sure that your keys are being managed securely.
And if you're reasonably technical and kind of know what you're doing, probably you could do a better job.
Especially if you're not moving your coins very frequently, if you had them stored on a crypto steel that was on ice somewhere, or in a volcano, or something like that.
But because of the usability story around key management is so bad right now.
It's hard for me to say that unilaterally.
Like I wish we were in a world where I could say like, yeah, Coinbase is horrible, don't ever store your coins there.
But now I have to say that in a more qualified way.
Because self-custody is also difficult.

Jeremy: 00:05:48

Oh, yeah, I was just gonna say, I think that a lot of people are looking for the soylent of custody solutions, where they're like, if I could just have this one thing, then I wouldn't have to eat any other foods.
And I think ultimately we'll probably be in a world where people have a couple different things that provide different sets of properties, and maybe you split up your coins as like, 30, 30, 30 among different types of things, and then 10% for just random petty cash accounts might be a little bit more of how people move, rather than having one universal solution that they're applying.
And I think exchanges do play a reasonable role, but maybe that's your 10% of petty cash is there where you're comfortable losing it in an adverse event.

Ayush: 00:06:32

Andrew, you're also working on some really interesting analog computing method, some way to store secrets.
Do you want to tell us a bit about this?

Andrew: 00:06:43

Yeah, sure.
So I'm going to give a longer talk about this later on, so I'm going to try not to monopolize this panel.
But Jeremy, if you could pass me the blue notebook behind you.
So I've been working on a project to do Shamir secret sharing and checksum verification of BIP-32 master seeds entirely using these hand paper computers.
You can just print these off, you cut them out, you use an X-Acto knife and assemble them.
And so you use these things, I've got a couple of them that all work together.
And also some worksheets.
This is what they look like when you print them out, by the way, so you just cut out things like this and then cut them.
And it's all open source, it's handwritten PostScript that you could verify if you're willing to read PostScript.
But the premise here is that you can do a lot of your key management, including stuff like Shamir's secret sharing, where you have a threshold number of (keys). you split your key into multiple shares and some threshold number of them are sufficient to reconstruct.
The idea is you don't have any electronic computers.
So there's, I'll say more in my talk, but there's a number of reasons to just be suspicious of electronics, period.
Which is essentially, I mean, they're too small to see what's going on, and they do a lot of weird, surprising things at basically every level of abstraction.
So if you can avoid that and just use human-scale, comprehensible things to manage your keys over time.
That for a lot of people I think would make them more comfortable.

Ayush: 00:08:09

And we're also seeing this.
I actually read an article yesterday.
Facebook, Apple, Microsoft, and Google are working together with the Fido Association to have these passwordless login mechanisms.
So let's say if I just open my iPhone with Face ID, everything else should also open because I use biometrics to get in.
Do you think there's ever going to be a situation where the seed phrase is not what we use to log into our wallets?
Because we're human beings, we tend to forget things.
Do you think there's a better way for us to store, to get access to wallets?

Andrew: 00:08:46

So I don't like biometrics, because they have bad incentive structures.
Or if somebody wants to steal them, they're physically attached to your body and maybe they'll try to detach them or something.
And they're also difficult to replace and all that good stuff.
But Fido too is not only like biometrics and stuff, there's also like Yubikeys and stuff.
I've got one in my pocket, probably a lot of us have something like that.
The issue with those is that they're, by design they're impossible to clone, right?
So there's a risk that you physically use them.
So with seed phrases, they have this nice benefit in that you can store them in a variety of ways and you can make copies of them.
I do think that people will continue to move to more of the model where they have a hardware token or something that has their seed phrase in it, but their master backup will continue to be on a crypto steel or a piece of paper or in their brain.
Hopefully not for long, but if you're crossing dangerous borders or something, sometimes that's the best place to keep it.

Jeremy: 00:09:44

One thing that I think is maybe one of these 20-40 things is I wouldn't be surprised if at some point in the future, a lot of people have just laser cutters in their homes.
And if you're a friend of somebody, you give them access to print out a encrypted seed share on their laser cutter.
And so you get a durable storage that somebody else has.
And then the main thing would be the social recovery aspect of like, hey, can you please give me the thing that I printed out because my personal access got destroyed.
And that might be a direction where things go, where it's a little bit more about the who you know side of people who you might trust to help you recover, rather than your own individual thing where you can get compromised on.

Ayush: 00:10:28

So one of the biggest things is people want to develop for Bitcoin, and Bitcoin has seen like massive upgrades over the last 10 years or so.
What is the process like, and Gloria, this is for you, what is the process like to start contributing to Bitcoin?
How does someone's code request or a feature get launched, what does it look like?

Gloria: 00:10:49

So my experience is all on Bitcoin Core, which I would like to distinguish from Bitcoin in general.
It's one possible node implementation to join the network.
And as far as I know, there's also a Rust Bitcoin which you maintain, which is another implementation of Bitcoin nodes.
But, I mean, Bitcoin Core operates pretty similarly to any other software project.
There's a GitHub repo and you open a pull request when you want to make a change and then people review it and it gets merged if it is reviewed thoroughly.
Although there are a few notable differences, I guess.
Human-wise, I'd say we're a lot more decentralized than say, open source project maintained by Google.
So actually a lot of people don't know this, but I think more than 50% of what Google works on in terms of code is actually open source.
But it's like, oh, we're in this open source alliance, and technically it's under this open source license, but 99.999% of the commits are written by Google and some other big software companies.
It's just when something breaks upstream that they get a PR from someone else.
Whereas Bitcoin is, like actually I think all of the maintainers except for two of them are like funded by a different company and those are all through donations, which is a very different model from, salaried employees at Google who are responsible for reviewing each other's PRs. So there is, I think, decision making-wise, it's a bit more decentralized.
But other than that, it's literally the same thing.
You open a PR, it gets reviewed, it gets merged.

Ayush: 00:12:46

So what does deployment look like?
Let's say it gets merged and how do you get consensus for everyone to move towards that side?

Gloria: 00:12:54

That's a good question that I think a lot of people are asking right now.
So Bitcoin Core, like any other open source project, has a release every six to 12 months.
Sorry, so your question was like, what does consensus look like?

Ayush: 00:13:14

What does consensus look like when you have to, let's say a change has been merged and we want people to start using that version of Bitcoin.
How do you get people to transition to the latest version?
How do you get consensus amongst the miners and everyone running Bitcoin Core?

Gloria: 00:13:32

I don't think we make much of an effort to do that.
We just release the software and then maybe people will run it.
We don't force upgrades.

Andrew: 00:13:41

Right, so most changes to Bitcoin Core don't affect the consensus layer on the network.
Typically they would affect the way that the node operates, like network efficiency, peer-to-peer things, or the wallet, or the GUI, which are kind of separate components that are increasingly being pulled apart.
And the wallet, of course, only affects people using the wallet.
And the GUI, of course, only affects people using the GUI.
I think there are users, I hope.
That's the one perennial problem in Bitcoin Core is that most of the core developers never open the GUI, and there's been, historically, there have been bugs that lasted for a while.
I think the situation's better now.

Jeremy: 00:14:18

So I think one example that I would give, pulling from your work, Gloria, is Gloria works on package relay.
And I think the argument is that that makes a miner who's using that software make more money.
And so it would just be within their self-interest to run it.
And if they don't want to run it, then it's only to their own detriment.
But that's not a consensus change.
It's just like, if you accept this patch, you'll make more money.
If you don't want to make more money, you're free not to.

Gloria: 00:14:47

I think one thing that Andrew touched on that I kind of want to throw out there is I think consent, there's like an overly over-represented attention to consensus changes when like that's maybe historically has been major upgrades to Bitcoin, but there's so many ways to make Bitcoin better without requiring a consensus change.
Like Pieter Wuille is famous for authoring many of the past soft forks, or most recent ones at least, but I often throw out the example that I would say one of the biggest scalability things that he did for Bitcoin was Ultra Prune, which is instead of looking at history using the blocks and looking at those transactions, just keep a UTXO set and that can represent your chain state in just a few gigabytes.
And that allows you to prune blocks and whatnot.
And I would say that that is one of the biggest improvements but that didn't require a soft fork.
That's in fact, I think most nodes would not, I wasn't there when it was deployed, but there would be no noticeable difference in terms of node-to-node interactions.
Consensus changes obviously require community consensus.
P2P protocol changes, you probably want a BIP so that people can implement that as well.
But above, that's just the tip of the iceberg of like all of the things that you could do to make Bitcoin better without involving everyone and the miners and the users to like, come together, because that's very costly.

Ayush: 00:16:29

Yeah, and speaking of BIPs, we have, Jeremy, you put out Bitcoin Improvement Proposal 119.
Yeah, do you want to speak a bit about what that's about?
What is Covenants?
And what that enables us to do?

Jeremy: 00:16:45

Yeah, so BIP 119.
I originally released something like it in 2019.
And the idea was to bring a little bit more powerful smart contracting capabilities to Bitcoin.
Not quite reaching into the depths of what you might be able to do in Ethereum, but covering a couple basic use cases that would have, I perceived, a lot of value for your everyday Bitcoin user.
One of the ones that I like to talk about is wallet vaults.
So adding a little bit more in the name of protection when you go to pull your funds out of cold storage so that you're sure that they're ending up in the right space and have more ability to prevent theft or hackers or whatever.
So, couple basic things.
It's not like Ethereum and you're gonna see AMMs and Uniswap and stuff if you want that, it's in the other conference hall.
But sort of as a part of that, because that is a consensus upgrade, there's been quite a process of trying to educate and inform and get the word out and also seek a little bit more detailed review of the impact that this might have on how Bitcoin operates and I think Gloria is absolutely correct that when it comes to consensus upgrades they actually because they're a little bit more dangerous, they end up being significantly safer because they get so much attention compared to your average change to Bitcoin, which kind of gets review but sails through with a couple of the experts who understand that area, doing it, and it goes out and releases and people don't make a big global fuss of something like ultra prune but there are impacts of like if all the nodes on the network are running pruned like how long could we do a rework in Bitcoin does that have an impact on that it's worth kind of analyzing some of those things and we take care and consideration and not doing something obviously wrong.
But in any part of the code that changes Bitcoin, the entire behavior of the network can change pretty radically.
For the specific process that I've been in, in BIP-119, recently there's been a little bit of controversy because I put out a blog post which said, if the network wanted to adopt this, here is a potential release schedule upon which it would be possible to get consensus and activate if it were desirable to the community.
Here's how if users didn't want that, they could resist that change.
And also that if the community didn't want that, it's like fine, it just means that it wouldn't be, it wouldn't happen this year.
It would maybe happen next year or in years future.
Maybe there would be a bigger research program, but if people want it this year, then this is sort of the only way that it could happen.
And in response to that, that was a little bit interpreted as like, Jeremy believes he's the dictator of what happens in Bitcoin, which was not really related to anything I actually put out into the universe.
But it's kind of like a game of telephone to get consensus with people, and people interpret things and pass it along and pass it along, and the message gets sort of distorted.

Ayush: 00:19:48

Yeah, so does this fit in with like, I know you've worked on Sapio, which is a smart contract programming language for Bitcoin.
Is this something which will fit in with Sapio, which you've developed?

Jeremy: 00:20:00

Yeah, so one of the things that anybody who's looked at in other ecosystems is usually these ecosystems have a programming language for developing a smart contract in, and then they have a base layer that's actually executing that.
And Bitcoin is maybe a little bit unique because while there's Bitcoin script, and there's now miniscript and policy, which are a little bit higher level, there's not really a general language for, let's say, like implementing something like the Lightning Network, or implementing something like a wallet vault until Sapio.
And Sapio is kind of trying to be a general purpose tooling for developing any Bitcoin smart contract and having automatic interfaces and integrations into other services.
And so check template verify is something that you could use within that for writing smart contracts, but it would be optional or it could integrate with other smart contracting primitives as well.
So that's a little bit of what that is.
And it works with the stuff that Andrew works on in terms of miniscript and policy too.

Andrew: 00:21:05

Yeah, I can say a couple words about miniscript.
So as Jeremy's hinting, Bitcoin's script is very difficult to write code in directly for a couple of reasons.
One reason is that all these different opcodes are designed and they're kind of, well, not designed, they were implemented in C++ by Satoshi so many years ago and there are a lot of weird edge cases and surprising properties and some decisions related to the way that arithmetic works and the way that numbers are encoded and stuff that maybe were not super wise or well thought out.
But the other reason is that the Bitcoin script model is very different from the way that people think about contracts or the way that people think about scripts on the blockchain.
The model that Script uses is it just uses a bunch of binary blobs of data.
And you're allowed to rearrange those.
You're allowed to duplicate them and move them around.
And you're allowed to interpret them as keys and signatures, but you don't have to.
You should at some point, I guess, do a signature check.
But you basically have these blobs that are floating around, and at different times you can think of them as keys or signatures, or you could think of them as numbers, or you could think of them as numbers, or you could think of them as Booleans, and there are different rules for when you can do what, and like what counts as true and what counts as false.
I could probably spend the whole panel just describing the rules for truthiness or falseness.
So it's not the way that people think about things, or the way that people think about scripts on the blockchain.
Usually when you're writing something in Bitcoin, you think, well, I want the coins to be spent if this set of keys signs off on it, or if a hash pre-image is revealed, or if it's an HTLC or something, or after a certain amount of time, then maybe the conditions change, or whatever.
But Script doesn't have a notion of times, or signatures, or queues, except in the context of specific opcodes.
So what Miniscript does is it kind of prunes the set of opcodes that are available.
And with the remaining opcodes, which are sufficient to express signature checks and hash checks and time locks and all that good stuff, the remaining opcodes are put together in a structured enough way that you can encode your programs as kind of lists of spending conditions, rather than as a bunch of instructions for moving blobs of data around.
So when you're writing code in Miniscript, it's really just a re-encoding of scripts.
It's got the same low levelness, but the model is much closer to the human model.
And it's also a model that's much easier to reason about mechanically and say things about under what conditions can the coin move, stuff like that.
So I guess Sapio is built on top of Miniscript exactly because Miniscript has a sane model that you can reason about, and building directly on top of Bitcoin script would put a lot more work on Jeremy to make sure that the code Sapio was producing was correct.

Gloria: 00:24:03

Can I add something?
I have a pet peeve about how people refer to smart contracts because often, as Andrew kind of hinted at, the difference is what the dev experiences.
So for example, Ishaana Misra wrote a really good article, I think, titled Bitcoin has always had smart contracts, and then a bit about scripts.
And literally it is like, you can express a lot of the things that other blockchains might call smart contracts, it's just that people find opcodes of script hard to deal with.
And it's just a matter of how many layers of abstraction can you build on top so that you end up with the exact same result.
Even if it's like, oh, an oracle needs to attest to this and then provide the hash pre-image, like a lot of people would consider that smart contracting because now you have a lot more expressiveness with like what you can bake into spending conditions.
So that's just my two cents on like, think about how arbitrary your definition of smart contract is.

Ayush: 00:25:23

Do you think this deviates from the original idea of Bitcoin, which was to send money on the internet, whereas Ethereum is meant to be a distributed computing platform.
So do you think this merges the line between Bitcoin and Ethereum and doesn't keep Bitcoin the way it's meant to be, or do you think it's a positive change?

Gloria: 00:25:46

Okay, there's a lot to unpack there.
So there's the assertion that the point of Bitcoin is only to send payments and then Ethereum is meant to be a more distributed computation platform, which I kind of agree with, but not quite.
So I would agree that Bitcoin is not trying to be a generic distributed computing platform.
Obviously, we, or I, would like there to be more mature conditions that you could bake into spending.
And I see all of this, layers of abstraction, as being, you get the expressiveness, but also the scalability.
So if we're gonna talk about scalability right I think there's two things you can do.
One is don't put everything on the blockchain, which I think is a very good scaling mechanism.
And the other is fit more into the data that you use on the blockchain.
I think that's my scaling philosophy for Bitcoin.
And this is not all encompassing, I'm sure there's other stuff.
But I think when you want arbitrary computation and you're like, okay, here's what we're gonna do.
Everyone's gonna put all the code into the blockchain and everyone's gonna run it.
That to me is, you're getting the expressiveness without the scalability.
Actually, I would be interested in hearing you speak about simplicity as well, which is kind of, sorry if I'm speaking on your half, but kind of a similar idea where it's like we're gonna fit more logic and expressiveness, but it's gonna be very small in terms of what you require all of the nodes to compute and what you require all the nodes to store in the blockchain.

Jeremy: 00:27:46

If I can just hop in with one thing before we go there.
What I would add just sort of as a historical context is, I think that there's a decent amount of evidence that Satoshi really wanted to build this decentralized world computer thing, and then hit a bunch of dead ends and said, well, it still seems to be good enough for a money system.
Because there are a lot of sort of stubs in the Bitcoin early code base and comments around, oh, we're gonna have decentralized poker, and we're gonna have decentralized marketplaces running on chain, and then all of those things sort of had massive problems in actually getting them to work and then the thing that remained workable, and I think that this is why Bitcoin script even exists, because it's kind of a surprising engineering decision, given it's sort of, I would describe it as Satoshi's kind of like main miss, is it's cleared the script system is sort of like a legacy artifact that was not really end-to-end tested of like, does this thing actually meet the need?
But I think Satoshi got to a point where he said, well, the cash part of this is working really well and we can launch with that.
And then we've not really seen the evolution of decentralized poker on Bitcoin.

Gloria: 00:29:05

I just wanted to attach, I think this is one of the main things that I love about Bitcoin as opposed to all other software engineering, where it's like, okay, here's what we want our security model to be, and we're not gonna budge on any of these security assumptions, and we'll build bottom up, and over time, we'll build whatever the features are.
Because you're not gonna go, and I like that, whereas other places, it's like you're not gonna go to a VC pitch meeting and be like, we need five years to strengthen our security model, and then we can start building features.
Like that's just not how the world works, right?
But that is how Bitcoin works, which I really appreciate.
Sorry for interrupting what you were saying.

Andrew: 00:29:50

No, I appreciate that.
That's a very optimistic way to describe Bitcoin's history and how Bitcoin thinks of security modeling.

Jeremy: 00:29:58

It's only gonna take five years.

Andrew: 00:30:02

Like in some ways, it's almost in contradiction with Jeremy's historical comments, which are true by the way.
You can find a copy of Bitcoin 0.1 floating around.
It's got a lot of commented out code and weird stuff about like, there's like an eBay like thing, and like auctions and poker, and all sorts of weird stuff that never made it into the actual software.
But what did make it in were a whole ton of general computing kind of opcodes, and it turned out that a number of those were busted in various ways, so a ton of them were removed in 2010, but we still retain a large number of them, right?
You can still add and subtract numbers.
For example, you still have control flow and if statements and Boolean logic and all of this good stuff.
Now, even though historically it does seem like Satoshi was trying for something really general and maybe couldn't make it work and that's an interesting interpretation that he just sort of said well I guess transfer is work, so we'll just ship it as is because at least you can transfer things I think the notion that you that the I Think there's value in expressivity even if you're just trying to do transactions even if you're just trying to do transactions.
Even if you're just trying to do Bitcoin-denominated economic transactions.
You want expressivity, it turns out, for things like controlling spending conditions, having multiple signatures and thresholds and fallbacks and logic like this.
It turns out that you can use this expressivity to hook layer two things into Bitcoin, like lightning HTLCs or PTLCs or whatever have you.
Then going forward, the one big category of things you can't do in Bitcoin's script is control where the coins are going.
You can define whatever conditions you want for the coins to move at all, but once those are satisfied, once you have enough signatures, they just go wherever the signers want them to go.
Whereas covenants is kind of a future thing in Bitcoin maybe, where you can restrict where the coins go a little bit more.
And this leads to all sorts of fears, rational or not.
But it also leads to the ability to do things like vault.
I think a really important feature where you have the ability to rate limit how quickly you can move your coins.
So even if your keys are stolen, then you have this vault mechanism that will slow down how quickly the coins move, and you can maybe intercept them before they get stolen or something like that.
So I would continue to describe Bitcoin as being in this model where it's trying to be a transaction system, right?
It's not trying to be a world computer.
It's not trying to be a multi-asset platform.
It's not trying to do general computation and stuff.
And despite that, you still want more computational expressivity, and you still want more of the ability to control where coins are going.
And I think probably in 2009, Satoshi probably didn't recognize the value in having these general computations just for the purpose of doing transactions.

Jeremy: 00:32:52

Yeah, I think one way of restating that is even if you just want Bitcoin to be the best possible cash, you don't care about the other stuff, it's pretty difficult to carve out the smart contracting primitives you would want to just be the best possible cash and prevent people from doing all these other things.
It's kind of you can't prevent people, it would just sort of if you had the right primitives to do it, it would be general purpose enough to do whatever.

Andrew: 00:33:15

And I would build on something Gloria was hinting at earlier about simplicity or taproot, which is a simpler model of simplicity in some sense, which is if you want Bitcoin to just do transactions and stuff, one way to try to achieve that is by just not having functionality that would otherwise be usable.
And that's sort of historically what happened.
I don't think on purpose, really.
Again, in the very early days, I think Satoshi tried to do a bunch of things.
A bunch of ideas just didn't work out of the gate.
A bunch of them didn't work later on, and there are a number of crazy historical bugs in 2009 and 2010 that would have let people steal all the coins in the system and stuff like that, that have long since been patched over by basically just like erasing, like deleting functionality.
But there's a better way to, sorry, what Gloria was saying is that we do want to move away from the Ethereum kind of model where you're putting code onto the blockchain to do these general computations.
So the fear that motivates kind of not having functionality is that people are gonna throw a whole ton of code into the blockchain, it's all going to be explicitly executed by all the validators and so on.
But there are better ways to add functionality, or there are ways to add functionality such that you don't necessarily have to publish a whole ton of stuff on the blockchain, and one simple example of that, there are complex examples that have all sorts of crypto and stuff, but a good start, or a simple example of that, is in Taproot, we have what's called the MAST, Merkleized Abstract Syntax Tree.
What I mean by that is that if you have all these spending conditions that are encoded in Bitcoin script, rather than having to write this big script saying the coins can move if this key signs or if time goes by and this key signs or if a hash pre-image is revealed and this key signs or whatever or whatever or whatever, the way you do now.
In Taproot, you produce what's called a Merkle tree, which is just a single 32-byte hash, and we actually can fold that into the public key itself.
A single 32-byte hash that commits to all of these different things in a way that you can efficiently reveal one of them without revealing the others.
And there's a privacy benefit there, but there's also a big scalability benefit, because it means that you could, in principle, have a coin that could be spent by one of a million different spending conditions.
And there are real cases where you'd actually get to a million by just mixing and matching different keys.
Actually about 10 years ago, I remember, there was a Burger King commercial where they were advertising you could have your burger over a thousand different ways because they had 10 binary options, I guess, which, I wish they had just said a thousand and 24 different ways.
I think that would have been a better commercial.
But over a thousand, I don't know, I'm not a marketer.

Jeremy: 00:36:15

Actually, if you order one of the 24, they tell you they can't do it.

Andrew: 00:36:19

That's right, that's the one, the 23.
Yeah, so there we go.
That's why I'm not in marketing.
I do these off-by-one errors.
Similarly, with Bitcoin scripts, you can easily have this large explosion of what look like astronomically large numbers, but actually it's just a bunch of combinations of stuff.
With Taproot, you can have a million different conditions, and you only reveal one when you're actually spending it.
And that means that even though you get more expressivity by being able to do that, by being able to encode numbers of conditions that you literally can't encode right now in Bitcoin because you would have to fit them all into a single transaction.
You get this extra expressivity, but you don't take the efficiency hit.
You don't force all these validators to be looking at all of your crazy harebrained logic and stuff.
And kind of for free, you get this extra privacy benefit, right, because the less data you publish, the less data people can see.

Ayush: 00:37:13

Yeah, so Jeremy, one thing I'm wondering is what Gloria said.
Optimizing the mempool is a big part of the scalability problem, so when, if and when this change gets into effect, would it have any impact on the transaction size and how the mempool operates, and would transaction fees go up?

Jeremy: 00:37:34

So I guess as a first sort of like recap, like the mempool is, in my view, like the most important and impressive data structure in Bitcoin.
It's kind of like this central brain of everything that goes on, and people are like, oh, isn't it like the blockchain?
It's like, well, how do you figure what should go into the blockchain?
It's like the mempool figures it out, how do you validate the transactions?
Aren't those, well, actually the mempool's kind of involved there.
How do you decide when to do a transaction?
Well, you gotta look at the mempool.
If Bitcoin, how is it gonna pay for blocks in the future when subsidy goes away?
Well, the mempool, everything always points back to Bitcoin is an agent-driven process where the mempool is our brain for that thing and so the mempools main objective is sort of twofold right now and the first is to be able to tell miners what to mine in a way that maximizes profit.
And the other function is to make relaying transactions sort of efficient, which is also kind of helping miners who want to put blocks out into the world.
Part of what we're seeing a larger evolution towards as people are doing more and more smart contracts is the mempool as an API to program against for people making things that they wanna be able to guarantee happen on some timeline.
So an example, if you have a lightning channel that's open and your counterparty goes away, you might need to close it within an amount of time.
And what you have to do is make a rational argument to the mempool that says, hey, you'll maximize your revenue by closing my lightning channel appropriately.
Now, it turns out that a general reasoning introducing intelligence is a complicated program to write, especially one that we're trying to have be largely rational.
And so what you end up getting is circumstances where the mempool can be committed to a belief, let's say, and that belief would be that this transaction looks like we're gonna get a lot of money for it, so we're not gonna consider anything else that might challenge that transaction or replace it or conflict with it.
And so that can get you into situations where if you're, let's say, doing a lightning transaction, your transaction might end up being stuck because somebody else has frozen it and you're not able to make an argument that the mempool's willing to listen to.
And that can get you into a lot of trouble as you're depending on it.
And so for the stuff that I work on, which I think is where your question was centered, what the impact on the mempool might be, I think that there's a couple of different ways.
One of the things that I like to talk about is congestion.
What that means is when the mempool has a lot of entries, Bitcoin can only consume one megabyte of them at a time, but the mempool could have, let's say, a hundred megabytes of stuff in it at any given time.
So a hundred blocks worth, how's it going to pick?
And if you want to get into that top megabyte of space that might be sort of next in line, what amount of fees are you gonna have to pay to convince it to take your thing next?
And what this can lead to in a lot of circumstances is positive feedback loops.
And so a positive feedback loop is where, let's say you really wanna be next, and so you say, okay, I'm gonna pay a little bit more than the last person in line, but the last person in line also really wanted to be next, so then they're gonna pay more, and what you can get is situations where things run a little bit out of control, and so a lot of the work that I focus on is sort of trying to think about those in the long run and provide features for coordinating to defer usage now to avoid some of these sort of runaway positive feedback loop scenarios and let people be a little bit more incentive aligned to be lazy is sort of some of the stuff that I work on.

Ayush: 00:41:34

Yeah, so do you think we can, when NFTs became a big thing, we saw gas fees absolutely shoot up.
Gloria, what changes do you think are required on a protocol level for the mempool to account for something like BIP 119?

Gloria: 00:41:50

Oh. I don't think we do we need to change mempool for 119?
I don't think we do.

Jeremy: 00:42:01

There are some changes that would be nice that you are also working on.

Gloria: 00:42:07

Okay, okay.
So I think, okay, how do we frame this?
So Jeremy started talking about congestion, which is currently, before package relay, very dangerous for especially contracting protocols, or L2s, where essentially, if you think about Lightning as you're creating transactions, Bitcoin transactions, with your counterparty that hopefully you don't need to broadcast unless something goes wrong.
And since it's a contracting protocol where hopefully you have the same security assumptions where you can't just be like "hey I know you're trying to cheat me but like can we re-sign this transaction that we agreed on like a month ago?"
You don't have that option, right?
So you're locking yourself into whatever fees you put on that transaction when you created it with your counterparty.
And because you have locked yourself into fees beforehand, when you go to broadcast your transaction, not only do you need to do it within, I don't know, five days or like one day or whatever, but also if there's congestion, you can't really adjust your fees.
There are some options, but right now it's limited without package relay, coming soon, TM.
And I think that's where CTV helps in that, okay, let me know if I'm not doing this right.
But CTV essentially allows you to commit to a transaction that might be a few hundred V-bytes or a few thousand V-bytes that you might want to send in the future that you can't right now because the mempool's congested.
You can commit to that transaction now and get like 100 Vbytes into the mempool right now, thereby resolving you of the time lock situation where you need to get this in ASAP, but you don't have the same problem where you're screwed because you're fighting for block space that's not available.

Jeremy: 00:44:20

So it's a little bit synergistic because also in order to use these things you also need package relay.
So it's one of these things where it's a little chicken egg, like this helps with the decongestion, but also to use the decongestion technology, you need package relay to be able to actually fully withdraw some of these things.
So it's a nice little synergistic bundle.

Gloria: 00:44:43

Yeah, I'm really glad I picked a project that doesn't conflict with anyone's.

Ayush: 00:44:49

So we are coming up on time, but it's been an absolute honor having you guys here.
I think we're all leaving this room smarter than we came in.
So that's been awesome.
Yeah, thank you so much.



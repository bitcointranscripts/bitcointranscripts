---
title: "B-money and RPOW"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
source_file: https://bitcoinexplainedpodcast.com/audio/@nado/episode-89-b-money-and-rpow-rm5k2.mp3
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-89-b-money-and-rpow-rm5k2
tags: []
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: []
summary: "In this episode of Bitcoin, Explained, Aaron and Sjors discuss two more electronic cash projects that predate Bitcoin: Wei Dai's b-money and Hal Finney's RPOW. As detailed in Aaron's new book, The Genesis Book, these systems introduced design elements that were later utilized by Satoshi Nakamoto. Aaron and Sjors explain what these elements are, and how the inspired Bitcoin's design."
episode: 89
date: 2024-01-22
additional_resources:
-   title: https://web.archive.org/web/20050211031649/http://www.eskimo.com/~weidai/bmoney.txt
    url: https://web.archive.org/web/20050211031649/http://www.eskimo.com/~weidai/bmoney.txt
-   title: https://nakamotoinstitute.org/finney/rpow/index.html
    url: https://nakamotoinstitute.org/finney/rpow/index.html
---
Speaker 0: 00:00:18

Live from Utrecht, this is Bitcoin Explained.
Jors, are you ready for Bookshell episode 2 out of 2?

Speaker 1: 00:00:26

Absolutely.

Speaker 0: 00:00:27

So today we're going to discuss two more electronic cash proposals that predated Bitcoin that I've also written about in my brilliant …
No, I'm not.

Speaker 1: 00:00:37

So, should we call these things shitcoins or is that not fair because they are pre-Bitcoin?

Speaker 0: 00:00:43

Well, no, they're definitely not shitcoins then, right?

Speaker 1: 00:00:46

Right.

Speaker 0: 00:00:47

I don't think that wouldn't qualify as shitcoin.

Speaker 1: 00:00:50

We'll have to ask Giacomo.

Speaker 0: 00:00:52

Yes, good idea.
So we're going to discuss B-money and ARPAO, but first, dear listener, Do you always lose your coins?
Have you tried everything?
Have you tried passwords, firewalls, – have you tried wallets?
– Brain.
Have you tried hiding your computer under your mattress?
Nothing works?
Well, there's a solution for you.
It's called the cold card produced by coin kite, which happens to be our sponsor, a hardware wallet, completely offline, where you can store your Bitcoin.
Shors, what's great about the cold card?

Speaker 1: 00:01:29

PSBT.

Speaker 0: 00:01:30

There you go.

Speaker 1: 00:01:31

All righty.
Thank you, Goldcard, for sponsoring the show.

Speaker 0: 00:01:35

Indeed.
So…
B-money.
B-money, yes.
So, a little bit of…
I'll start with a little bit of context, right?
So, in the previous episode, we discussed…
What was it?
HashCash and Bitgold, right?
And then in another episode, I don't remember the episode number, we did e-cash as well, because these are sort of the five main digital cash projects that I detail in my book.
There's a couple more that are sort of mentioned in passing, but the main sort of ones that are highlighted are e-cash, hash cash, Bitgold and B-money and ARPAO.
So today we're going to discuss, we're going to do sort of a deep dive deep dive into B-money and ARPAO.
Sounds good.
What's the name of the book?
It's called the Genesis book, the story of the people and projects that inspired Bitcoin by Aaron Van Weerdum.
He just bought it.
It's right here on the, on his table.

Speaker 1: 00:02:31

Exactly.
You still need to sign it.

Speaker 0: 00:02:33

So one more sale for this guy.
Yes, I'm going to give you some little bit of context on B-Money.
If you want to know more context on B-Money.

Speaker 1: 00:02:45

Yeah, tell me about B-Money.

Speaker 0: 00:02:46

You can't read it.

Speaker 1: 00:02:47

Was it code?

Speaker 0: 00:02:48

Okay, let's start here.
So B-Money was a proposal.
It was proposed by Wideye shortly after Bitgold.
So Bitgold, we discussed in the previous episode, proposal by Nick Szabo.
If you haven't listened to that episode, this would be a good time to maybe pause this episode and go back one episode, listen to how BitGold works.
B-Money was…
It was sort of…
So Nick Szabo and Y-Dai and a couple of other people, they had this separate mailing list where they were discussing digital cash ideas as well.
So there was the Cypherpunks mailing list, and then there was also the Libtech mailing list.
And So it's pretty safe.
Basically they were discussing these ideas with each other.
So Bitgold and B-Money are fairly similar because of that.
They were sort of just discussing how to realize this, or they were coming up with similar designs, essentially.
Now we're not going to repeat how Bitgold worked, but B-money…
Okay, so here we reach that point again.
Who's going to take the lead on…

Speaker 1: 00:03:58

You're going to explain this one.
I'm going to take the lead on this one.

Speaker 0: 00:04:02

Well what I will say, one thing about B-money, yeah, you just asked, was there code, I think?
Yes.
So the answer is no.
So B-money was actually never implemented.
It is mentioned in the Bitcoin white paper,
by the way, but it was never actually implemented like Bitgold, which was also never actually implemented.
Yeah.
And I would say B-money even more than Bitgold, there's definitely some, there's significantly a significant hand-waving going on with several parts of the design.

Speaker 1: 00:04:33

Right, so we don't exactly know how it works because it wasn't described in a lot of detail and there were a lot of unsolved problems.

Speaker 0: 00:04:39

Yeah, it was more, it was a rough sketch of a digital cash system.
It was an idea, it was almost sort of brainstormy, but it was getting there, but a lot of problems sort of unsolved.
So To sort of get to the essence of how it works, it is good to have listened to the BitGold episode because it's similar in several ways, as I mentioned.
But the way it works essentially is the coin creation would probably have been similar.
That's a safe assumption, even though that's not really fleshed out in the proposal either.
But that seems sort of…

Speaker 1: 00:05:25

I thought you mentioned there were two kinds of coin creation mechanisms.

Speaker 0: 00:05:30

Well, what I'm referring to is mostly the actual proof of work.
Like the proof of work system would have probably been similar.

Speaker 1: 00:05:40

They were just hashing something.

Speaker 0: 00:05:42

Yeah.
Yeah.
And it would have probably started with a candidate string in the same way that Bitgold did and then you hash on that candidate string.
Okay.
So, B-Money, it's not even really one proposal.
It's sort of several proposals wrapped into one.
It's like an idea and there's several ways to do it.
Now, what I think was the most interesting thing about B-money is how double spending is prevented,
or at least one of the ways.
Yeah.
This is getting tricky to explain this because of all the possibilities, if you fork the different design options.
So if you want to send coins from one public key to another, similar like Bitgold or Bitcoin, I guess,
if you want to send coins.
Now the problem of course is how do you prevent double spending?
How do you prevent that one coin is sent to multiple people at once and there's a discrepancy there?
Wideye's proposal essentially was everyone's going to keep track of the state of the ledger.
So again, you know, everyone who's been listening to Bitcoin Explained for a while knows that this is essentially how Bitcoin works.

Speaker 1: 00:06:56

Exactly.

Speaker 0: 00:06:57

Everyone's keeping track of who owns what.
So this was an idea that B-Money introduced, that YDAI introduced, which is very relevant to Bitcoin.
Now, unfortunately, YDAI also concluded pretty quickly that this doesn't actually prevent double spending, of course, because you can still do the double spend and then people will just have different…

Speaker 1: 00:07:21

Yeah, they'll have different versions of history.
…ledgers.
Yeah, so…
They don't know which is the real one.
Right.
Especially if they got it after the fact, I guess.
Because if you're following it live, you can at least say, well, you know, whichever comes first, but even that can split it up if it happens at the same time, but at least if it was like two weeks between it, you could say, well, clearly this one was first and this one was second.
But if you're coming online a year later, you have no idea, right?

Speaker 0: 00:07:45

Yeah, pretty much.
So the only way it could work, why did I mention that in this proposal, if you have an unjammable, you know, instant communication network or something like that, which is magic,
yeah, Essentially.
So that is not what I guess.

Speaker 1: 00:08:04

Yeah.
If everybody knows about it at the exact same time and with no delay, then you can, everybody can see who's first, but it does require everybody to not just to store all the transactions, but to be online all the time.

Speaker 0: 00:08:16

Right.
So I would qualify this.
And the way I sort of described this in my book is I think it was, you can sort of see it as a breakthrough in thinking, like it was a novel approach to do it this way.
However, it wasn't actually possible.
So, but then why I had a second idea and this actually very much resembles what Nick Szabo proposed for Bitgold, which is to have some sort of, you know, server, a group of servers that maintain this registry.
So there's sort of two types of participants in the network, one type of participant that's just a user, and one type of participant that's keeping track of the state of the ledger.
And the regular users would have to inquire by these special servers.
And what Wideye specifically proposed is you inquire by a number of these servers.
And if a great enough number of them all say, yep, this transaction is valid, then you accept the transaction.
So say there are 20 of these servers, then YDI may have said, I don't think he mentioned, I'm sure actually he didn't mention specific numbers, but he may have said, check with two thirds.
And then if two third of them say yes, then it's good.
So in that case, it would have been 14, I guess, my example.
Now, again, this sort of reintroduces the problem that Nick Zabo had, which is who gets to be one of these servers?
How do you prevent Zipple attacks?
And then Ydai again came up with sort of his own solution here, which is these servers would have to deposit like stake.
So they would have to have a certain amount of B-money tokens.
And then if they would try to cheat, then these tokens could be taken from them.
By whom?
Exactly.
So again, it's sort of this hand-wavy thing where it's sort of an interesting idea, but who's going to decide that you've been cheating if it's not these servers themselves?
How can you...
I don't think, or it's not clear to me if he had an answer for it that he just didn't spell out, or…

Speaker 1: 00:10:36

Or maybe he didn't have an answer for it.

Speaker 0: 00:10:38

Yeah, that sort of seems to be the case, as I mentioned in the beginning.
The way I'm reading it, it's sort of, here's this idea, here's what I come up with, do with it what you want.
And it kind of makes sense in a way as well.
This is also something I describe in my book, is that Wideye had sort of, actually by the time he published B-Money, he'd sort of already given up on the idea of digital cash.
He'd become disillusioned with the whole concept in particular because he thought people don't actually care.
So there was this Cypherpunk group, I'm not going to get into all of that, but they were building all these privacy technologies.
But then when people start to go online in greater numbers, they were just using centralized non-anonymous services and credit cards online to make payments.
So this sort of vision of the cypherpunks that they were building privacy tools for the people wasn't really coming true because no one seemed to care.
And for that reason, YDai also, he became kind of disillusioned.
So from that perspective, it might make sense that he sort of reached this point of, all right, this is what I came up with.
I'll just post it in case someone wants to build on this, but I haven't got all the solutions.
Even the way he posted the proposal, like on the Cyberpunk mailing list anyways, like it's not even an email about the money, the digital cash system itself.
It's like an email about an upgrade to PipeNet he was building, which is some other anonymity tool.
And then there was like this, by the way, I also came up with this B-Money thing, if you will.

Speaker 1: 00:12:22

But wait, there's more.
Yeah.

Speaker 0: 00:12:27

Was this a reference, were you referring to me telling more about B-money?
No, I was referring to Steve Jobs here.
Yeah, okay.
There is something else that's interesting to say about B-money, which is that Wideye had this idea of, he wanted to build or introduce a monetary policy in B money.
So we discussed with Bitgold or with Hashcash before that, that the problem is inflation essentially.
It becomes easier and easier to produce valid hashes.
So there's more and more coins, if we want to call them coins, in circulation.
And so there's this sort of inflation because of that and the money is not very desirable.
So BitGold solved this as we discussed, I think we discussed this, right?
With a second layer, with banks and these buckets and that whole thing.
By the wide eye instead, he proposed that he wanted the monetary purchasing power to be stable, like in a CPI type of way, although he doesn't define this as either, he doesn't define what is stable actually specifically, or importantly, who's going to decide it.

Speaker 1: 00:13:45

But the idea was then that the amount of proof of work needed depends on the supply that's out there and then the desire for keeping the price at a certain level.

Speaker 0: 00:13:54

So there's two proposals.
So the first idea was, again, let's for Simplicity just take this, it doesn't really matter, but let's take this registry, like the version of B-Money where there's this group of servers that sort of decides, you know, prevents double spending.
Now then this group of servers would have to kind of come to some kind of consensus of how hard or expensive it is to produce a valid hash of a certain value.
And then they would sort of take this basket of goods and then they would match like, okay, so this is now how expensive a hash is to produce to match this basket.
And they would, so in a way they would sort of set the difficulty of B money.
So there would be sort of a committee, if you will, setting the difficulty.
So there's not a difficulty algorithm.

Speaker 1: 00:14:48

It's not even an oracle.
It's really a committee that has to look at how difficult it should be.

Speaker 0: 00:14:54

Yeah, pretty much.
So that's how they keep, What's the best way to put it?
I think I've made it pretty clear, right?
But yeah, producing a difficulty should be as expensive over time compared to this basket.

Speaker 1: 00:15:12

I mean, the eventual breakthrough was to realize that if you want to have a constant amount of new supply every so much time, then you just use time as a way to decide how high the difficulty should be.
That was the insight by Satoshi.
So you don't need a committee, but you can actually just use a clock.
Yes, however- He was getting there, but he didn't make it all the way.

Speaker 0: 00:15:36

Well, but it is very different, because Bitcoin does not have this goal of a stable, you know, stable in quote marks, I guess, because who defines stable, but stable purchasing power, at least not in a CPI type of way.

Speaker 1: 00:15:50

COREY HENDRYS That's a separate thing, right?
So there's two things you want to do is you want the supply itself to be at least predictable, and that's I think what they both have in common.
And Satoshi figured out how to make the supply predictable.
But then the secondary goal is how to make the purchasing power stable, and that is something that Bitcoin simply has not solved.
Some people see that as a feature, other people see it as a bug.
Stablecoin solved that problem, but then they have all the other problems.

Speaker 0: 00:16:17

I mean, this to an extent comes down to the definition of stable, right?
Which is actually…

Speaker 1: 00:16:22

Stable purchasing power, basically.
I think you can objectively see that the purchasing power of Bitcoin is less stable than that of the euro, at least so far.
Maybe in the long run it becomes more stable.

Speaker 0: 00:16:35

That I would probably agree with.
However, you're always stuck with defining stable, which is never...

Speaker 1: 00:16:47

No, that's what I'm saying.
Stable compared to purchasing power.
You have to pick something.

Speaker 0: 00:16:52

No, no, no, sure.

Speaker 1: 00:16:54

It doesn't have to be CPI.

Speaker 0: 00:16:55

Purchasing power of what?
What are you purchasing?

Speaker 1: 00:17:00

Yeah, of whatever lifestyle you're having.
But I agree, there's also the factors that decide that, right?
So that's a whole economics discussion.

Speaker 0: 00:17:08

Yeah, so let's sidestep that.
But I do get into that aspect in my book as well, at least for a part, especially Hayek's ideas about that, this sort of what I highlight.
Anyway, sidestepping that, YDI had this idea of stability in this kind of a CPI type of sense, basket of goods type of sense.
And so, yeah, there's this committee that says, okay, That means that right now the difficulty should be X.
Alternatively, B-Money had this other idea or YDAI had this other idea, which was, okay, to keep the value stable, we now need X amount of new coins to come into circulation today or tomorrow, per day, so to say.
And we're going to auction this off to the highest amount of proof of work.
So whoever is willing to produce the highest, you know, most difficult to string, highest proof of work, they'll get the new coins.
That's sort of an auction system.

Speaker 1: 00:18:05

And interestingly that is also very close to what Bitcoin is doing.
It lets the market figure out how much hash power there is and who is willing to mine and who is not.
But it's not a winner takes all system, right?
This proposal would have been a winner-takes-all system.
You win the auction, you get to make the coins.

Speaker 0: 00:18:23

Well, Bitcoin is that as well, right?
There's only one winner of a block, essentially.

Speaker 1: 00:18:27

Per block, yeah.
But on average, everybody can contribute hash power.
And it's not the case that like any given hash is predetermined to go to you, right?
With this proposal, I think if you win the auction, then you are doing the mining for a certain period of time.

Speaker 0: 00:18:45

I mean, I think the way B-Money, I think this proposal would have been, okay, we're going to bring 100 coins into circulation today.
How much hash do you want to show for it?
And then people would produce different hashes and there would be only one winner.
The highest one.

Speaker 1: 00:19:00

Oh, okay, but that's more of a race then, where everybody has to put in effort.
Because an auction is something where only the winner pays or has to do something.

Speaker 0: 00:19:08

Yeah, but how do you know?

Speaker 1: 00:19:11

So what I thought he was doing, but I haven't read it, so maybe That's why I'm wrong.

Speaker 0: 00:19:15

Well, it's not detailed, but it's hand-wavy, so that's why I can't…

Speaker 1: 00:19:18

It's like a tenure, right?
Where you say, okay, who wants to, for the next week, produce hash power?
And then somebody says, okay, I have a 10-terahash machine, I'll turn it on for a week.
And then it's okay, you get this job for the next week, and then next week, somebody else gets a job.
Because otherwise, a lot of people are basically doing a lot of effort, but they're not winning at all because they are not the very best.
They are the second best.

Speaker 0: 00:19:41

Yeah, but I do suspect that that is how it would have worked in White Ice mines.
I don't know.
That was my assumption.
So, yeah, you have to sort of factor in the probability that you'll be the highest one.
I don't know, it introduces an interesting dynamic to an auction.
Like, it could work, right?
There's no technical reason it can't work.
And it's sort of simpler to implement it that way.

Speaker 1: 00:20:04

I don't think it's an auction because in an auction you only pay if you win.
Whereas here you always have cost as a miner, you're always spending energy, but you may or may not get the reward based on whether you're the highest bidder.
So it's not proportional.

Speaker 0: 00:20:17

Yes, yes, it is a bit different in that sense.
Anyway, so this stuff is kind of hand-waved.
Like these data are not fleshed out in the B-money proposal.
Again, to clarify this, the B-money proposal is not like a white paper like Bitcoin was, it's more like a post of one or two pages sort of on a web form, so to say.
So yeah.

Speaker 1: 00:20:41

Which brings my question is why, given that it was just a side note, Why is it then still remembered?

Speaker 0: 00:20:50

Well, for one, it's of course in the Bitcoin white paper referenced.
I think what I emphasize in my book as sort of the breakthrough step that B-Money in a way introduced is this idea that everyone's going to keep track of balances, even though he didn't actually propose a way to do it.
That's consensus robust.
It was still the first time that this was proposed in a digital currency context and is used in Bitcoin today.
So I see a relevant step there, although it's a smaller part of my book than, for example, something like BitGold.
I do see that sort of this intermediate thing a little bit, but it's still interesting.
It's still a thing that people were thinking about.
It was one of the notable digital cash proposals before Bitcoin.
The last thing I can mention about B-money, which I'm not going to get into detail on, is that it was very heavily focused on smart contracts as well.
Bitgold was kind of as well, but bmoney as well.
There was this idea with like an arbitration system and there was a bigger idea than just cash.
It really was sort of meant to be a platform for smart contract.
So it's kind of, it's also, you could argue sort of a pre-echo for Ethereum, because you've got both sort of a pre-proof of stake kind of thingy going on, even though it's not fleshed out And then there's sort of heavy emphasis on smart contracts, even though it's not actually purely smart contract because there's still a lot of arbitration going on.
But anyways, it's interesting to see that these ideas kind of preexisted as well, maybe.

Speaker 1: 00:22:46

Yeah.
All right.
Sounds like there was another proposal.

Speaker 0: 00:22:50

Yes.
So now we're going to take kind of a jump in time actually, because so Bitgold and Bmoney were both proposed in 1998.
Of course, both not implemented.
And then for a couple of years, actually, interest in this whole domain sort of died down a little bit.
The Cypherpunk mailing list itself sort of went defunct.
But then in 2004, Helvhiny pops up and he...
Actually, I believe he explicitly says that he wants to implement something like Bitgold's MB Money, but he's going to use a simplified version of it.
I would say that's even kind of a misnomer.
He just sort of comes up with his own thing, but there's some similarities, sure.

Speaker 1: 00:23:37

But it was inspired by these ideas.
But what was very unique about this proposal is that it had code.

Speaker 0: 00:23:44

Yes, yeah, That's right.
RPOW was actually implemented by Helvini and run by Helvini.
So, shall I take the lead on this one again?

Speaker 1: 00:23:54

Yes, please.

Speaker 0: 00:23:55

Okay.
So RPOW, it's sort of interesting.
It started with E-cash, which was centralized, and then that failed.
And that sort of made Cypherpunks move to a more decentralized direction of thinking.
So both Bitgold and, well, Hashcash before that, even Bitgold, B-money, they all have this idea of how can we centralize the protocol.

Speaker 1: 00:24:22

Decentralize.

Speaker 0: 00:24:23

Oh, sorry.
Yeah, decentralized.
And then RPAO actually sort of goes back to just doing it centralized.
Now, there were some ideas or Halvany had some ideas where it could be also kind of decentralized or multiple servers.
But the system he implemented was essentially centralized.

Speaker 1: 00:24:42

But it was transparent, right?
That was…

Speaker 0: 00:24:44

Yeah, yeah.
So I'm getting there.
So let me first just mention real quick how it works, essentially.
It's also worth mentioning at this point, for example, Tor has been invented, the onion router.
So now it's possible to use, you know, to connect to the server anonymously, which sort of did away with some other anonymity technologies, that's for example, eCash used.
So actually what you did with RPOW is you connect with the server, the server then gives you a proof of work assignment.
And if you perform this proof of work, you get coins.
So the server issues coins to you.
Now these coins are just numbers essentially.
And then if you want to pay someone, you just send that person these numbers, and that person sends these numbers to the server.
And then the server says, yep, these are indeed numbers that I generated.
Like the server keeps track of what numbers it issued essentially.
And at that time, it also makes these numbers invalid and gives new numbers in return.
Yeah.
Does it make sense so far?

Speaker 1: 00:25:56

Well, yeah, the making things invalid and giving new ones in return is something you see with the e-cash as well.

Speaker 0: 00:26:01

Yes, indeed.

Speaker 1: 00:26:03

Except that these are not blinded at all.

Speaker 0: 00:26:05

Right, so the privacy in this case, as I mentioned, is you can just connect with the server through something like Tor and then the server doesn't know who you are anyways.
Yeah.
So instead of like this, you know, blind signature technology that E-cash uses, RPL kind of takes a simpler approach and just, the server just doesn't know who you are anyways.

Speaker 1: 00:26:25

Yeah, which has, I believe, one of the benefits is that it's easier to check the supply.

Speaker 0: 00:26:34

Yeah, I guess that's a good point.
Well…

Speaker 1: 00:26:37

How was the supply created?

Speaker 0: 00:26:39

Well, hang on.
So the server, there's two ways that the server essentially issues coins, right?
So one way is in return for proof of work, and another way is in return for other valid coins.
Now, there's no actual limit on the supply, or at least the way Helvini implemented it, there's no limited supply, if That's your question.

Speaker 1: 00:27:01

Yeah, it was completely inflationary, but you can at least check the amount of proofer work that goes in.
I don't know if you can check it actually, because you'd have to ask for the whole transaction log and I don't know if the server will give you the entire transaction log.

Speaker 0: 00:27:16

I don't think it would.
No, I don't think so.
Not that I know of.
I haven't looked at the code itself, but I've not read that it would have been the case.

Speaker 1: 00:27:25

No, I think then the model was different, right?
There is…
but we'll get to the transparency side of it later.
But I think you rely on understanding what code is running and you can see that that code is not creating inflation, therefore you're trusting extra inflation I mean.
It's not like printing money for the owner, but only because you know that that code should do what it says it does.

Speaker 0: 00:27:48

Yes.
Well, that's the next point where we're getting at.
So the part of creating coins makes sense, right?
It's just proof of work.
So it's called RPOW, which stands for reusable proof of work.
And really, if you read Helvini's comments on it, it was more supposed to be kind of like Hashcash, kind of like postage, just reusable postage.
So there wasn't, again, there wasn't like this big idea of monetary reform or scarcity, or it was really just, let's make proof of work reusable, you know, sort of hash cast what you use.

Speaker 1: 00:28:24

Yeah, because the idea of being able to get change for the work, that's new here, I think.
Change?
Well, so what we talked about last week, or last time, which of the systems was it again?
BitGold?
That one, you didn't have change, so you would send a piece of proof of work and you could not get change back.
You'd have to go to this bank and work with these buckets and all that stuff.
Whereas now, with ARPAO, you do have change.
The server can give you change.

Speaker 0: 00:28:57

Yeah, with ARPAO you don't own the hashes themselves.
The hashes are just a way to earn coins.
Yeah.
So the server will just issue you coins if you perform proof of work, or if you give coins to the server.
Like if you receive a coin, then you get new coins.
Okay.
Okay.
So that's pretty simple so far.
Now what was important for Helvini though, was that he did want RPOW to be trustless.
So it was centralized, but he still wanted it to be trustless.
So the trick he used for that is that remote attestation.
So essentially the code he was running on this server was free and open source software, and this was just published online.
So anyone could read the code, could read how this product worked, could read that the only way new coins would be brought into circulation is either for proof of work or in return for other coins.
So even the owner of the server, Halvini in this case, couldn't just issue himself free coins, right?
Because it's free and open source software.
Now, how do you know that the server is actually running this software?
So this is the remote attestation trick.

Speaker 1: 00:30:09

Yeah, because of course, in open source, the big problem is you have no idea what code is actually running.

Speaker 0: 00:30:17

On someone else's server,

Speaker 1: 00:30:18

yeah.
Or even on your own computer, that's what we talked about in an earlier episode about geeks and deterministic builds.
But ignoring the problem of build systems, which he ignored, I believe.
The binary that's running on that machine, how do you know that that's actually running on the machine?
And that's where indeed remote attestation comes in.
Yes.
Which is a pretty cool concept.
I can try and explain it.

Speaker 0: 00:30:42

Yes, that's, we're getting close to your wheelhouse now.
Like I know the concept, but yeah, let's go for...
Let's give you the short special on this one.

Speaker 1: 00:30:50

So I believe this was the first or one of the first computers created by IBM that did this feature.
So he was excited about that, presumably, and probably that's why he used it in the proposal.
So you can basically connect to this machine and say, please tell me what code you're running.
And it will tell you, okay, here's a hash of the code I'm running, not the actual code, but it will give you a hash and it will sign it with a signature.
And then, and this is where the mercury starts coming in, you trust a signature because IBM signed something that says this person, this computer can sign on my behalf.
So there's a private key on the computer, Not a Bitcoin private key in the sense that you can spend with it, but a private key that can sign a secret.
So IBM has said, okay, this key on this computer, you can trust it.
It's a computer that we sold.
And then if this key signs anything, then you believe what it says.
And then the question is, what does it sign?
It basically makes a hash of whatever program is running right then, and that's what it signs for.
There's a lot of caveats here.

Speaker 0: 00:31:58

Yeah, well, the private key is really embedded in the chip itself.

Speaker 1: 00:32:03

Yeah, in a secure enclave basically.
So very much like a hardware wallet in the sense that the assumption there is that nobody, the owner cannot get that private key out, so the owner cannot sign another message pretending that there's a different program running on the computer.
However, of course, we know from hardware wallets that sometimes they are compromised.
And this is 20 years ago, so they were probably less secure.
But I don't know if that ever happened to this particular computer.
But the assumption is that the owner cannot get the key out, therefore you can trust that the computer is talking to you.
That's the public key cryptography at work.
And that the computer is maybe not lying because IBM says that their computers don't lie.

Speaker 0: 00:32:49

Yeah, you're trusting IBM essentially.
Now you could make the argument that you're kind of trusting IBM anyways if you're running their hardware?
Yeah.
Like whatever you're doing?

Speaker 1: 00:33:02

The owner is, but you as the person using the money system have to trust IBM.
And not just trust them for not being malicious, but also trust them for not having a vulnerability in there and not disclosing it or something like that.

Speaker 0: 00:33:17

Right.
So yeah, that's the essence of RPOW.
There's free and open source software running on the server, and you as a user can verify with some caveats that this is actually the free and open source software running on that server, and therefore you're not being cheated on, double-spent on, Helvini is antiquarily making himself a millionaire for RPOW.

Speaker 1: 00:33:43

And so the funny thing about Bitcoin then is that saying, okay, well, we'd rather not trust this one computer running all the things, so we're going to run the same program.
Everyone is going to run the exact same software, and it should produce the same result giving the same data.
So that's kind of a fun way back.

Speaker 0: 00:34:01

Right.
What else can I say about RPOW?
Because that covers most of the technical part of it.
Fun fact is maybe that Greg Maxwell worked on it for a bit.
You know, the Bitcoin Core developer, the Bitcoin Core wizard.

Speaker 1: 00:34:18

One of the funny things is I briefly looked at the source code of like several months ago, but it has a something like a difficulty adjustment algorithm in there.
Because when you are selling work to the main house, so anybody can sell work essentially to the server to get the RPOW tokens.
And the code is there that produces the work that you can then sell.
And that code actually makes sure that it's producing roughly the same number of coins every 10 minutes.
So that is, it's not like, it's not a requirement in consensus, but it's just some, for some reason, there's already difficulty adjustment in there.

Speaker 0: 00:34:53

Right, right, right.
What else?
Yeah, so it never really took off.
It always remained sort of this very small niche play thing that almost no one cared about, probably in large part because it had this inflationary effect to it.

Speaker 1: 00:35:10

And it was also quite risky from a centralized point of view, right?
If the government says, hey, Mr. Affini, what are you doing here with all this money?
Please turn it off.
Because yes, it's transparent, but if he turns it off, it's off.

Speaker 0: 00:35:23

Yeah, that's very true.
Of course, he couldn't cheat, but the server could still be shut down.
Yes.
Yeah.

Speaker 1: 00:35:29

And the government can, of course, also force IBM to produce fake signatures and all that stuff.

Speaker 0: 00:35:34

Right.

Speaker 1: 00:35:35

But I don't know if that's the reason why people didn't use it.

Speaker 0: 00:35:38

Well Greg Maxwell and I think it's just there was no economic incentive for anyone to use it.
Like why would you use something if you know for sure that next year it's going to be worth less?

Speaker 1: 00:35:49

So purely the inflation was holding people back.

Speaker 0: 00:35:52

I mean, it could still be useful in a hash cash type of way, like to use it as postage.
But even then you're dealing with this chicken and egg problem, right?
Like in the case of an email, why would you require people to produce proof of work?
If no one does it, that means you're never getting any emails.

Speaker 1: 00:36:09

No, but you could even imagine using it as money, but only for very short term transactions where the volatility is acceptable.
But yeah, so maybe it was the inflation, but also maybe it was just ahead of its time, or there was something about Bitcoin that made it take off.
Sometimes it's the market's system.

Speaker 0: 00:36:28

I mean, I think it's the economic incentives.
I think it's a limited supply of bitcoins.

Speaker 1: 00:36:32

I'm just thinking the QWERTY keyboard classic story, right?
It wasn't necessarily the best keyboard out there purely from an economics point of view, but it's just the thing that took off.
Sometimes in technology something takes off because it takes off, but it could also be for the reasons that you mentioned.

Speaker 0: 00:36:51

True.
Okay.
Is there anything else you want to mention about RPOW?

Speaker 1: 00:36:57

No, I would just say that it's very cool that the Nakamoto Institute has published the source code for RPOW, including the older versions of it.
You might, I don't know if you can still compile it, but maybe with some effort.
Could be fun to play with it and see if you can run it and, you know, see what it actually does in a modern world.
And it also has quite an elaborate FAQ and descriptions of how, have any thought the privacy would work.
So, that's all I have on it, but very cool.
Okay.
In that case, thank you for listening to Bitcoin Explained.

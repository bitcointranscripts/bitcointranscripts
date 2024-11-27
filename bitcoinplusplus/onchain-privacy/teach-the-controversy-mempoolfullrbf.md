---
title: 'Teach the Controversy: mempoolfullrbf'
transcript_by: nillawafa via review.btctranscripts.com
media: https://www.youtube.com/watch?v=F6qPuhsM5Ng
tags:
  - rbf
  - transaction-pinning
speakers:
  - Peter Todd
date: 2023-12-09
---
## What is transaction replacement?
(00:00)

So, let's go start off.
What is transaction replacement?
And maybe not the best screen, but this is a screenshot of the Bitcoin wallet, Blue Wallet, and it shows off transaction replacement very nicely.
I have a transaction, I got rid of $25 worth of Bitcoin, and I can do two things, I can go bump the fee or cancel the transaction, and if any of you guys played around with it, it does what it expects, it increases the fee or it cancels it.
From a technical point of view this is pretty simple.
If you have a transaction, it's unconfirmed, you make another transaction spending at least one of the same inputs.
That means that transaction could also be mined and thus if that other transaction does things like say, increases the fee or makes all of the inputs now go back to you, you've achieved the goal of bumping the fee or canceling the transaction.
Pretty simple.
Other things people like to do with replacement is being all fancy and taking multiple outputs as they come in on an exchange and adding them together to optimize the fees etc etc.

## History of transaction replacement
(01:16)

The history of this I think is actually kind of interesting, which is well, Bitcoin 0.1.0 actually did ship with transaction replacement.
This is not a new thing.
And that's the code (referring to slide).
I didn't bother looking up 0.1.0. That's code from 0.1.5 for how it actually checks for a conflict in the mempool acceptance and it does all its thing, looks at the outputs, etc, etc.
But the key thing is, my next slide, when did it decide to replace one transaction with another?
Well, it used something called the `nSequence` field, which, we don't really understand quite why it was introduced.
It's just a 32-bit number.
And it said, well, if the number is bigger, go replace.
Now, it's a 32-bit number, which means you could replace 4 billion times, and this was a really bad idea.
You could go sit there starting at zero and then just spam the mempool of all nodes 4 billion times using up bandwidth for no particular reason.
It was a dumb idea, but apparently, and this is my current making claims, and we don't really know if this is totally true, but supposedly Satoshi way back in the day thought you'd implement payment channels with this by having transactions hanging around in the mempool that could get mined, but aren't yet, and then someone would eventually go and make them mined.
But there's a lot of problems with this, and I'll let you go think of some of them, but needless to say, this got yanked and we came up with a much better idea, which is called replace-by-fee.
And the way it does it is very simple, more money is better than less money.
Now, there's a couple more rules which I'll also mention later, but that's really is all there is to it.
It's if the transaction has a higher fee, you know, put the one in with a higher fee in.
Seems really, really simple, right?
I'm not exactly sure whose idea it was, it might have been mine, it might have been someone else's, but this dates back to, like, 2013 or so.
And at the time, mempools weren't congested and all, but people could go and foresee, like obviously this could be an issue and this seems like a good thing to have.

## First Seen Rule
(03:29)

Well, there's a catch, which is people don't like transaction replacement, because part of Satoshi's original implementation as a byproduct ended up having something called the First Seen Rule which is as it suggests: the first transaction you go see it's the one you go mine.
Simple as that.
Why is this useful?
Well, if you want to go and pay for coffee with Bitcoin to an extremely unimpressed looking barista, who's probably annoyed at all these stupid Bitcoiners, you can do that.
Now, this gets back to the block size debate and as we all know, paying for coffee with Bitcoin doesn't really work that well.
There's not that much block space out there and so on, but that's the politics around this.
Even up until now, there's still some people trying to accept unconfirmed transactions with the First Seen Rule.
I keep on trying to find examples of this and having a very hard time to actually get good examples.
ATMs are something people often bring up.
But you know, I was in El Salvador recently and supposedly the ATMs there would accept unconfirmed transactions and just spit out money.
Well, half the time they would, half the time they wouldn't.
And whether or not I'd set this BIP-125 thing didn't seem to matter.

## Opt-In-RBF - The Political Compromise
(04:47)

Speaking of, So what was the political compromise?
How did we get transaction replacement in?
It's this thing, which I'm co-author of.
It's BIP-125, and there's more to this BIP than this, but the key thing that allowed transaction replacement to get in was this part: explicit signaling.
Transactions are considered to be opted-in to allow replacement, etc, etc, if the `nSequence` number is less than some value.
So this is kind of in the spirit of Satoshi's harebrained idea.
We're still using `nSequence`, but now we're letting people opt into this.
Of course, it's not that hard to replace transaction whether or not it's being opted in, but you know that was a political compromise.
In this other rule here, inherited signaling, that basically means if you have a transaction in the mempool, then you spend it again, so you have two unconfirmed transactions, it's supposed to be that the second one can be directly replaced, and long story short, it's not actually implemented.
So if you ever read the BIP, that part isn't true.
But the moral of the story is we got transaction replacement in.

It is actually used, you know, with this opt-in thing, and that's all well and good.
My own OpenTimestamps calendars use it to go get optimal fees and as a byproduct to update the Merkle tree of transactions of timestamping.
So they start off at the minimum possible fee, and every time a new block comes in, which is indication the fee was too low, they double spend it with a higher fee and a higher fee, and a higher fee, and eventually gets mined.
It's a pretty good technique if you want to pay the minimum possible price and are willing to wait.
So this got in in like 2016 if I remember correctly, and nothing much happened for years, until... multiparty transactions.

## Multiparty Transactions
(06:33)

So what's the issue here?
Well, you know, as the years pass by, people started having the clever idea of, well, let's do protocols where multiple people offer transactions.
And the issue there is, and I'll give a coinjoin as an example.
If you and I create a coinjoin, both our inputs are in that transaction, but if you go and accidentally or intentionally double-spend that input, if you broadcast that transaction first, it could get to majority or even essentially all miners.
And then it's just gonna sit there if it's a low fee.
And now on my end, I have my coinjoin, but nothing really happens, and I'm kinda stuck.
I mean, I don't really know how do I make the coinjoin progress forward?
Do I spend a higher fee?
Well, it won't work because if you don't set this BIP-125 opt-in, I still can't replace your transaction.
I'm just waiting for you to finally time out or something happens.
And there is no set time limit for how long a transaction can sit around in mempools.
I mean, in theory, it could sit around for months.
There's a thing called transaction expiry, but transaction expiry, because mempools are, of course, a per node thing, if a transaction expires from your mempool, some asshole can just go and rebroadcast it again and get it back into your mempool, and then the two weeks goes on again.
There's no clear solution to this.

So finally, after all these years people said well why don't we just go and add full replace-by-fee?
Why don't we just say screw this opt-in thing?
Why don't we just do the transaction replacement rules for any transaction?
Seems simple enough.
As you can see here, Marco (Falke) here thought, looks good to me, shouldn't be controversial given that the default is unchanged, remains false.
Right?
Simple enough.
So this was back in June 13th of this year.
And I think this got merged, what, two or three months later?
And on top of this, people also had other versions of these proposals, but that was the basic idea.
Seemed simple enough.
Well...

## The Panic: Pinning Attacks
(08:47)

Now, we get a bit of a panic.
Suhas (Daftuar) goes and realizes, hang on a second, there's this transaction pinning thing, like it won't really work properly, we should go remove it.
And frankly, I and a few other people said, well, screw this.
You know, we've been trying to get full replace-by-fee in for ten fucking years.
I think it's time to get this in, and long story short, this is one of the most NACKed pull requests in Bitcoin core history, and it eventually did get closed.
So what on earth was Suhas talking about?
Well, there's this thing called pinning attacks.
Now again, if you and I have a protocol where I might want to replace an unconfirmed transaction, and you might not want that to happen because you're just being mean, there are things you can go do by exploiting the BIP-125 rules.
And this is the full set, at least in the BIP, of what the rules really are, for when one transaction should be replaced by another.
Rule number one, it's a bit about the `nSequence` opt-in.
Rule number two is something we kind of added to make it easier to reason about to miners.
If I replace a transaction that depends on a transaction that's really big, it's arguably not as good for miners and that might make things be slower and it's not in sense compatible.
Rule number three, it's a similar kind of deal where, well, if the replacement doesn't pay at least all the fees of the other transaction, I mean maybe you can go spam the mempool with this.
And frankly when this was introduced, like a lot of these rules were just things I kind of came up with, well, you know, why don't we go and make sure this is conservative and won't be problems.
Similarly (rule number four) the replacement must pay for its own bandwidth.
That's just saying, well, you can't replace for like, one extra Satoshi.
You got to replace for at least, you know, the minimum relay fee times the size.
And then (rule) number five, well, you're not allowed to replace more than a hundred transactions at once.
And between these like three and five are the main ones that allow pinning to work.

Again, let's suppose we're in this coinjoin.
You want to go and make my coinjoin sit around forever.
If you just take your input and broadcast a chain of 100 transactions, Bitcoin Core instances running these defaults, we'll say, hang on a second, we're not gonna replace one with the other because that's 100 and that's just too much.
Now, is this 100 limits...Like, is there a reason for it?
Well not really, I mean it's a number we kind of pulled out of thin air.
Like obviously if it was a million, there may be issues, but this really gets down to implementation, like how exactly does all this work?
But that was Suhas' idea, since transaction pinning is a problem, well, obviously we should just go yank full RBF and come up with something better.
Now, I would argue this is not really true.
And it really gets back to cost.
If we're doing a coinjoin and someone accidentally does a double-spend, like maybe they've imported the same seed into two different wallets at once.
Well, full RBF helps a lot.
And let's go through why.
So, there's a couple scenarios.
First of all, you might have double-spent with a transaction that is more desirable to miners.
So the coinjoin transaction can't replace that first one.
You know, it doesn't pay as much as fees.
Well, yes, the coinjoin gets canceled, but we still make forward progress because the double spend eventually gets mined, potentially quite quickly.
And that's good, right?
The reality is, coinjoin protocols, like Wasabi, JoinMarket, and so on, those protocols fail all the time because they tend to be two-phase protocols.
A bunch of people, they propose inputs to the coinjoin, then they propose outputs.
If they don't propose output for the input, the coinjoin just fails and you try again.
And apparently Wasabi, they've achieved the amazing success of having 25% of coinjoin attempts succeed.
You know, it doesn't sound like much, but be honest, when I was told this I was assuming it was like 1 or 2 percent.
So, you know, that's better.
But, now let's go and look at the case where the double-spend isn't as attractive.
It's a lower fee.
Well, if it's a lower fee, the coinjoin's just gonna replace it, and the vast majority of miners are gonna have this transaction and we make forward progress by getting the coinjoin mined, nice and simple.

Now, let's go look at the scenario where someone's trying to maliciously stop the coinjoin.
Well, how do they do this?
Well, if they don't want to spend money, they have to broadcast a pinning transaction that pays low fees.
Now without full RBF they can just broadcast any transaction at the minimum possible fee to send the mempool, and it's not clear when that will get mined.
Maybe never, maybe the mempool minimum fee goes up and the transaction gets kicked out and now they can use those coins in some other way.
There's a lot of ways that could go work.
With full RBF, provided they paid less in fees, it will get replaced with the exception of pinning attacks.
That sounds bad, but let's just go look at this rule.
Rule number five, it's the only rule that's really relevant in this type of pinning attack.
The total of 100 transactions: well, if I'm forcing the attacker to create 100 transactions in a row, they're tying up more money, and also if it's a fee that's high enough to get mined in a reasonable amount of time, which is what it would take to not get replaced, now they're paying a hundred times more money when it does get mined.
So frankly, long story short, I think Suhas is wrong on this.
I think he just hasn't considered through how the attacks really work.
Because, again, in the case of coinjoins or, lightning opens, all these attacks are things where I can also attack by just not fully participating in the protocol.
Again, coinjoins are particularly vulnerable to this because they're two-phase protocols, but if all I do is create a bunch of outputs, and DOS attack people by advertising those outputs, and refusing to go along with protocol, I've also wasted time.
So we just have to do better than this, and full RBF does.

## Why Full-RBF is a Political Tradeoff
(15:29)

I know a lot of people on the Bitcoin dev discussion so on around full RBF been trying to frame this as a technical discussion.
They say this is something that should be held to technical debate and so on.
And I mean, they're not entirely wrong.
Like, obviously, if full RBF was something insane, well, maybe you would have a technical debate about this.
But the technical debate is done.
You know, we know it's a rule that works.
We know there's no technical issues with this.
What's really happening now is this is political debate.
This is about trade-offs between different users of Bitcoin.
And one of these trade-offs is privacy, for instance.
You know, this opt-in flag is a privacy problem for everyone because you had one more bit of information to de-anonymize wallets.
You have another trade-off where wallet authors now have to go deal with people sending money without the opt-in flag and getting their coins stuck because the mempool's full.
And again, that's a trade-off.
Like, there's no clear technical consensus on what's better or not.
What do you value more?
You also get really nutty stuff, like Craig Wright saying if a node allows double-spend and mines it, we should go sue them.
And this nonsense, well, I hate to say it, but I'm personally being sued by Craig Wright.
And I would rather, this first scene rule not be yet another thing people can go start suing people over.
It sounds silly, but, back in like 2015, 2016 or so, I remember talking to people, trying to get the First Seen Rule to go work reliably, who were proposing things like colluding with miners to, for instance make sure that blocks that did do double-spends got re-org'd out.
Which is insane, like, the Bitcoin protocol can't be decentralized yet also have a list of what is or isn't the valid transaction seen in mempools.
You know, there just isn't consensus over gossip networks.
We just have to accept that.

But one of the political trade-offs is people will try to go do these things if they build businesses on it.
And this is the kind of outcome that can happen.
And other people in Bitcoin can say, well, screw this.
We're just going to sabotage your business from the get-go, so it doesn't get big enough that it matters.
It's kind of ugly there, but like that's one of the political trade-offs involved there.
Another example of political trade-offs is on the other side.
Some people do try to build businesses around this.
There's also people who try to build business around lightning.
Can you really, from a technical point, say that one is much more valid than the other?
You kinda can, but that's not really how this plays out.
I'd argue it's much like the block size debate, where it's not like one or the other is clearly better, but there are trade-offs between them and we chose to use second layer protocols rather than make things better for on-chain protocols.
That is what it is, so if you agree with me, how do you actually make it go happen?

## How We Can Make Full-RBF Happen
(18:56)

I mean, that's a that's pretty obvious thing to do.
In Bitcoin Version 0.24.0 you add that to `bitcoin.conf` and you'll start applying full RBF, simple as that.
If you use Bitcoin Knots, Bitcoin Knots has had full RBF enabled for a couple years now by default.
Also you could go patch it yourself if you really wanted to, although I don't really see why.
But that's the basics of it.
Now, there's been a nuance here though, which is you enabling that flag doesn't mean you necessarily have peers who also do this.
And there's two sides to this.
First of all, if you're running a listening node that is reachable from the rest of the internet, and you run full RBF, people can go and make sure full RBF transactions propagate to you by just connecting to every node.
And IPv4 nodes as an example, there's only about 5,000 or so listening nodes.
Running a beefy server that literally just connects to every single node at once is completely feasible.
That side of the propagation issue is easy to solve.

I think the more interesting thing is what happens when someone turns on a node that isn't accepting incoming connections?
What is the chance that they wind up connecting to one of these full RBF nodes?
Well, that's your math for it (Peter refers to figure on slide).
Your probability is basically the probability of, let's say you have m full RBF nodes out of n total nodes in that category.
What is the probability of all eight not being full RBF?
And of course, inverted there.
Well, that's your graph.
On x-axis, percentage of full RBF nodes, y-axis, probability of having at least one.
And as you can see, it gets to like 50-50 pretty quickly.
It takes like eight percent of nodes running full RBF for there be 50-50 chance of at least one, and for you know out of like 5,000 IPV4 nodes that's like 400 nodes.
As far as I can tell, Bitcoin knots, because it's by default is actually already gotten us something like halfway there, maybe more.
So it won't take that many more people turning it on to make propagation happen fairly reliably.
Another example of this is Blockstream.info recently turned on mempool full RBF on the backend nodes for their website.
It doesn't always work, but a lot of the times it does, and if you hit Ctrl-R, because the web interface actually connects something like 10 different ones, you'll see what percentage are actually connected at one time.
And I'm talking to them to go fix up the propagation issues.

## Preferential Peering
(22:01)

There's also an easy way to guarantee this, which is preferential peering.
If you're familiar with how services are advertised on the bitcoin peer-to-peer network, there's something called the `nLocalServices` field, and that's a bit mask of all the services you offer.
Well, I have [a longstanding patch](https://github.com/petertodd/bitcoin/tree/full-rbf-v24.0), the code in this particular case was written by someone else, but I've adopted for version 24.
And basically, this code advertises a full RBF bit and ensures that at least four of your peers are full RBF peers.
Long story short is if you run this you'll reliably get full RBF propagation.
It's quite helpful if people do this, because it means that you, don't have to go brute force it as much.
It's a very elegant thing.
And interestingly Bitcoin Knots, when it does run full RBF, it advertises this bit too.
It doesn't do the preferential peering part, but it does advertise it.
So again, this is another way where you can ensure that all these different nodes are interconnected.
And finally, of course, obviously, miners need to actually go run this, although not as much as you think.
So if you get situations where say the mempool is full, as you may know, when the mempool's full, we sort all the transactions by fee paid, and we drop the lower ones.
And that's how you keep it in check.
Well, one of the side effects of this is it means that doing double spends is easy, and having more full RBF nodes makes it more likely to get to miners who've happened to have dropped it.
But obviously if miners just go run this, full RBF replacements can get mined.
And with that, I hope you're doing your part too.
Thank you.
[*Applause*]

## Q&A
(24:09)

I assume we have time for questions.

Q: Do you know any miners currently that are saying that they have full-rbf turned on?

A: I do actually.
I'm not going to say who until I see them have evidence of it actually happening.
But I've been talking to them on and off for the past couple of weeks, and it was literally like an hour ago that they told me they'd forgotten to go restart their nodes when they turned the switch on.
Well, you know, it happens.
So, we might see a replacement pretty quick.
Earlier I said how the OpenTimestamps calendars do opt-in replacements.
Well, there are four of these calendars in total, all doing timestamp transactions independently, and I run two of them.
And on the two I'm running, I've changed it so that it does full RBF replacements.
So if you go to alice.btc.calendar.opentimestamps.org or bob.btc.calendar.opentimestamps.org, you can go see this first hand.
And any of the transactions that it does in the chain, they are full RBF replacements.
And eventually, at some point, one of them will get mined.
It's just a matter of time.
Also on the Alice one, I've upped the fees to basically perform a bounty, so anyone running full RBF or potentially screwing with mempool in other ways can get particularly high fees right now.
I think it's probably about a hundred bucks right now per transaction mined and I've had donations from people to go and fund this.
There's a lot of people who really want full RBF to happen because it simplifies a lot of stuff.
So, this is how it is.
Any more?

Q: Is there a patch for running on RaspiBlitz?
[*inaudible*]

A: Well, so, you want to check GitHub.
I'm pretty sure I remember there being a config option that just got merged for Raspberry Pi Blitz to make it easy to do.
I know for sure on Start9 that recently got added so it will be just a checkbox in their configuration UI somewhere.
Now, like I say, if you do this, there's not a guarantee you'll be connected to another full RBF node, but once we get past that threshold, it just becomes more and more likely, so certainly enabling it on your Raspberry Pi will help things.
And in particular, for things like RaspBlitz, Start9, I think Umbrel as well, a lot of these things do Tor by default.
So all the connections, or at least incoming ones if not all the connections, are over Tor, and doing the trick of just connecting to all the nodes is harder on Tor because Tor is kind of screwy and slow.
So especially people running full RBF nodes on Tor makes a difference for that subset of the network.
It's easy to go and get propagation work on IPv4 because IPv4 is reliable.
But Tor, it's trickier.
And same would apply to I2P, although I don't think very many people run I2P nodes.

Q: Is the configuration public knowledge? Can I find out if other nodes [*inaudible*]

A: On Bitcoin Core, it's not easy to figure this out.
You would have to do something active where you would send the node replacement transaction, see if they get rejected, but on the preferential peering patch it explicitly advertises it.
And also Bitcoin Knots.
So the preferential peering thing ensures you're connected to other nodes and then the service bit just advertises it.
So Bitcoin Knots will advertise the fact that it's full RBF, but (on) Bitcoin Core, it's not trivial to figure out.
On the other hand, I mean, if you're connected to a node, obviously you can just go wait for full RBF replacements to happen, just see if they came to you.
Frankly, there's no way to avoid this if you're thinking about attacks.
Certainly if someone really wants to go screw with full RBF nodes, they could start doing stuff like this.
When that starts to happen, it really tells miners, hey, could you please go mine full RBF so we just get rid of this nonsense immediately?

Q: Is your branch, is that just Antoine's PR?

A: Exactly.
Yeah, yeah, yeah.
Plus a few more fixes by, I wish I remember the guy's name, sorry.
There's like two or three more fixes by someone else plus and I fixed, some minor details.
But yeah, Antoine did the main work on that.
And I have earlier branches where I did something similar, but he rewrote it from scratch, because since 2016, when I last made one of those branches, all the net handling code has changed.

Q: How many miners actually mine your drives?

A: Well, funny enough, I mentioned earlier how it looks like one miner will be turning this on very shortly, supposedly they have it on right now, so the next block they find we'll find that out.
But prior to that when the mempool was full, curiously, I noticed F2Pool seemed to be the ones most likely to go and mine full RBF, because you know obviously as the mempool gets full, transactions get dropped, but F2Pool seemed to be doing that when the mempool wasn't at the 300 megs limit, and I'm not really sure what was happening there.
They might have been experimenting with full RBF, it's possible they had a different mempool size limit than other nodes, which would mean they would do this earlier.
In one case, I believe they probably just restarted a node or installed a new one and thus didn't have a full mempool.
And it just happened to be, when they did that, one of the full RBF nodes did broadcast a transaction to them.
But it's hard to know, because after all, the mempool isn't consensus.
So, you can't really assume too much based on what miners actually mine.
And along those lines, I don't think I pointed it out yet, but remember you can always go do double spends by just broadcasting multiple simultaneous versions of transaction with the same size and fee, because there is no reasonable way to go pick between one and the other, and currently Bitcoin just doesn't even try.
If it receives a transaction that's the same size and fee as the one it's evaluating, it'll do nothing, because replacing it would just mean you could go and use up bandwidth on the network without cost.

[*inaudible follow-up Q*]

A: I mean with current Bitcoin Core yeah, it would just delete it.
It doesn't even add it to mempool, literally that piece of data just gets deleted and it accepts it again.
In the future, there are potential, like, possibilities to add this to package relay.
If you've heard the term package relay, it basically says, rather than look at transactions one at a time, we look at transactions as a package.
Classic example why this is useful is in Lightning--the commitment transaction that you need to get mined if your peer disappears, well, the fee might be too low to get into the mempool.
And currently, this is a real problem because even though you can use child-pays-for-parent to make it worthwhile to mine, if you can't broadcast the first transaction, you can't tell miners it's worth mining.
So the package relay proposal that Gloria (Zhao) is working on is to, at the tech level, to take the orphan pool, which is transactions you receive but can't connect, like you don't have the inputs, and reuse that for package relay so you would add it to a per-peer orphan pool, and then when the second transaction comes in you say, oh hang on, now it was worth mining, alright now I'll tell my peers about this.
So something similar could be done in this case of like divergent transactions too.
Well, thank you.
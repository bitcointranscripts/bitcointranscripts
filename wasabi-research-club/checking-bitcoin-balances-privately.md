---
title: Checking Bitcoin balances privately
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=8L725ufc-58
tags:
  - research
  - privacy-enhancements
  - cryptography
speakers:
  - Samir Menon
date: 2022-09-27
summary: In this video, the Wasabi Research Club delves into the topic of checking Bitcoin balances privately. They discuss the use of homomorphic encryption and private information retrieval to protect users' privacy when querying data from a server. They explore different solutions and strategies to address challenges such as address linkability, block retrieval, and the scalability and cost of checking balances. The team also emphasizes the need for an open standard for private information retrieval to ensure decentralization. They discuss the use of Tor and homomorphic encryption together, as well as the possibility of batching requests to improve efficiency. The video concludes by highlighting the ongoing research and exploration of potential solutions to ensure private querying of Bitcoin balances and more...
aliases:
  - /wasabi/research-club/checking-bitcoin-balances-privately/
---
Speaker 0: 00:00:00

So hello and welcome to the Wasabi Wallet Research Club.
Today we are speaking from with Samir from Spiral, which is the title of a fancy cryptography paper of homomorphic value encryption or homomorphic encryption and private information retrieval.
The gist of this cryptomagic is that a client can request data from a server, but the server does not know which data was requested.
And there are different variants of the CryptoMagick for different use cases.
And there are currently two proof of concept apps.
One is a Wikipedia, so where I think six gigabytes of text entries, no pictures, can be queried so that the server doesn't know which article you're interested in.
And the second, more pressing and important for us, is an anonymous block explorer so that you can query the UTXO set and request an address and the server will give you the balance of that address.
And well, the server doesn't know which address you're actually requesting.
So that sounds like impossible magic.
And Samir, please tell us how all the magic works.

Speaker 1: 00:01:26

Yeah, that was a great introduction.
Honestly, a little better than the one I had.
Thank you.
Yeah, that's exactly what it is.
That's kind of what got me into this field is that it does sound like magic and it does sound like you probably shouldn't be able to do something like that, but you can.
So yeah.
I'm actually going to just mostly, I'll talk a little bit about the internals of how Spiral works at the end, but I'll kind of first just like, let's just try to situate, you know, the security model of a server that doesn't learn what you query is kind of complicated.
And so let's just first try to compare it to all the other ways you can check a Bitcoin balance.
And let's just like situate it amongst the many, many alternative ways, you know, one could look up the balance of a Bitcoin address.
A little background on me, I was a graduate student at Stanford and this PAR project was kind of my senior project for my master's and it was advised by Dan Bonet but it kind of I went and got a real job, and so I stopped working on it for a little bit.
Then the itch came back and I worked on this again and published this paper, I believe, I guess I presented it in May of this year.
So we're starting a company, I'm quitting my job soon.
So yeah, yeah.
And we're trying to start a company around this technology.
All right, so today, I think you guys and me probably have a very similar goal, which is what we want our private-like clients.
We want clients that don't have to run a full node, but also do not leak information to third parties or as little information as possible.
Today, third parties learn a lot of information when you use them directly.
So if you're a like client and you just over the regular internet connect to a full node, you are going to tell them a lot of information.
In particular, they're going to get both your IP address and your actual Bitcoin wallet addresses as you query them.
So that's pretty bad.
You're kind of linking this very identity correlated feature, an IP address with your money.
You can use a public block explorer to do this instead of connecting to a full node directly, but it's kind of the same picture.
You're still sending your IP address and your wallet address to a third party who can link them.
A really good frontline solution is to use Tor.
So a very simple thing to do is to remove this network level identifier, the IP address, from the information that the public block explorer gets.
There is still some leakage.
And in particular, the leakage is gonna come from the fact that you typically query many more than one address.
And even using something like Tor, even if you actually build a new circuit every time, even if you appear to the public block explorer, like someone coming from many different clients, you're going to still leak actually the metadata, if you will, that you're querying all these addresses at the same time and over Tor.
It depends on the actual practical circumstances, but there's still even just timing will lead actually that these addresses are related.
And of course, like figuring out that addresses are related is actually a pretty big deal because some of the point of like things like CoinJoin is to actually hide that exact information that two addresses are controlled by the same person.
So this linkability problem is important, we think.
There's another solution in BIP 157 and 158.
I think it was implemented by the Neutrino wallet also, which is this block filter solution.

## Block Filter Solution

Speaker 1: 00:05:42

So basically what happens here, I'm sure you guys know, but it's basically compact data about the transactions in each block is kind of streamed to the client continuously.
And then when the client sees that a block contains a relevant transaction, it just fetches the full block.
So there's like a couple complications with this way of doing things.
One, I guess, practical thing is that the blocks are kind of big.
The blocks are one megabyte up to one megabyte each.
And for kind of privacy reasons, you can't just get a subset of the block.
If you have a wallet that's kind of busy, like if you use your wallet, say, every hour, you have to download a megabyte an hour.
So as frequently as your addresses are making transactions, that's how much data you need to kind of stream.
The filters themselves are also, you know, a kind of continuous ongoing cost, because you've got to monitor.
So if you're offline for some time, you need to kind of scan through all the filters and see if you're offline.
And maybe in a different way, there's kind of this leakage problem.
So one problem is the act of fetching the block is not protected.
I mean, we announce which block we're trying to fetch.
But what we do is, I mean, as a mitigation, you know, if we did this all with the same node, that would be bad because the node could kind of pretty easily tell from the blocks that you fetch which address you're interested in.
You could just kind of do an intersection attack, can work quite well.
The mitigation is generally that you connect to different peers for each block.
So you connect to a different peer to download each block.
But you know again here the timing really trips us up right again just knowing that just watching it even if I'm not like even if I'm not a Tor adversary, I'm not able to like, you know, de-anonymize you on Tor.
If I'm just like your university network administrator, and I just watch your bandwidth consumption, I will just notice a one megabyte download on some cadence, right?
And if I just like kind of correlate that with blocks on the chain, then I just kind of see, it seems like you might have downloaded block 379 and 24.
It doesn't become terribly difficult to figure out an address.
So there's some leakage.
I think in all of these examples, the attack I outlined is kind of theoretical, but it's mostly just to illustrate that there is leakage that's still kind of there.
There are some other options which people kind of suggest.
I don't know if you guys are the audience who would exactly suggest this.
I guess industry kind of more, I don't know, the A16Z folks or whatever would say, oh, why don't you just run it on AWS?
But of course, kind of just replacing a box with a different box, right?
Here, now you're just trusting the cloud provider kind of to do everything.
And I guess another suggestion folks have is running a full node.
And I think that, you know, to be honest, that is a great suggestion.
If you want really sovereign kind of control over the data, I think running a full node yourself is a good idea.
It is just kind of hard.
I mean, you have to make it remotely accessible.
It's kind of annoying to set up and maintain.
If we could find a way without having to run a full node, allow clients to kind of privately query the blockchain, that would still be a good thing because we want to reduce the barrier to entry, we want more people to use this.
Yeah, I mean, there aren't that many full nodes, so not that many people do something like this.
So the way Spiral works is it uses homomorphic encryption to remove the wallet addresses piece of the query.
So the server is still learning your IP address, but now there's no useful data to correlate with that IP address.
The basic idea is a spiral uses homomorphic encryption to encrypt your query when it leaves your device, and then it's able to process your query and return an encrypted answer without learning anything about your query.
The guarantee is it's not statistical, this is not like a mixing or any kind of thing like that.
This is, it's not like hashing, it's not buckets, it's a full cryptographic guarantee that the server cannot learn anything about the query, even if they're actively malicious.
It does incur higher computational costs for the server.
In particular, the server has to do work that's linear in the size of the database.
So if the database gets bigger, so today the database is a bunch of Bitcoin balances, if we wanted to include, you know, when we added transaction data or if we want to include more data say about individual transactions, that will make the server's runtime longer.
But On the other hand, the communication is better, and there's kind of no ongoing syncing really needed.
The server can kind of keep its database up to date, and whenever the client wants to get the most up-to-date information, they can make another query.
Today, we only support balances and the five most recent UTXOs. That's because of this thing I talked about earlier where the computational cost for the server is linear in the size of the database.
So if we wanted to make it 10 most recent, it would cost more.
So we need to think carefully about how we can make that kind of scale to at least a use case that's useful.
And yeah, of course, the code is open source, and there's a paper and everything.
And I'm happy to answer any questions about how it works.
I have a slide that kind of explains more of the technical underpinnings of Spiral.
So if you want, I can just go through that slide if you want to hear more about homomorphic encryption stuff.

## Open Questions

Speaker 1: 00:12:00

But before I do that, I'll just kind of say, yeah, I think the open questions for us are, you know, what minimum set of data is enough?
I think balance is on its own, it's not quite enough.
I think if I was, When I run a wallet software, I kind of expect more than just the balance in all my addresses.
We obviously need to think about fetching more than one address.
Because today there's like a website and you can fetch one address, but you know, wallets have more than one address.
And yeah, I think there's a couple options on how we do that.
We need to think a little bit about the pay or incentivization structure for servers.
This is a kind of class in computation.
So how can we make it feasible or practical for them?
And long term, I think I would like to see an open standard for PIR for this data.
So what we want is something that's not tied to a company or a person or an organization, but just kind of ideally, like maybe a BIP or something that allows us to not tie ourselves to any particular scheme and do this PAR thing as an extension of our current way of, you know, say doing a get block RPC or whatever.
So yeah.
Would you like me to just go through the homomorphic encryption step?
Because I got the idea.
Would that be interesting?
Yeah.

Speaker 2: 00:13:32

Go. Max, actually, maybe we can take an intermission just to ask a few questions and then we'll continue with

Speaker 1: 00:13:39

the- That sounds great.
Yeah.

Speaker 2: 00:13:42

Sure.
Because I think a lot of people are going to have questions here and I'll just start myself.
Can you kind of give us a ballpark of the cost of the server per UTXO?

Speaker 1: 00:13:57

Sure.
So I guess today what we do is we take the UTXO set and we kind of summarize it.
So today we take the UTXO set and for every address we take the top five UTXOs if there are up to five.
And we also compute its balance.
And that's the data we do today.
If you wanted to, say, query the entire UTXO set, that would be slightly bigger than what I outlined, but not that much bigger.
If you want a sense of the size of the computational cost, maybe the simplest summary would be, you know, for every, yeah, I guess, if you think of the database size, the computational cost is about 300 megabytes per second.
So what that means is like, if the database is one gig, it takes three CPUs to do this task.
So the task is fully parallelizable.
So you can think of computation as just a cost.
You know, like if you did it with three cores, you know, you would take one second.
But yeah, it's around 300 megabytes per second.

Speaker 2: 00:15:15

I see.
So the big situation here is that for WasabiWallet, we would want, as like an MVP for us to work, the amounts simply wouldn't be enough.
Our users, they want proof.
They want to know that it's connected to block headers that are in the chain with the most proof of work.
But on top of that, we also need to know that the server isn't in some ways deceiving us.
For example, just lowering the balances of all the users or just omitting certain UTXOs. Block filters do a nice job of this because you're, you know, you're just hoping the server does an accurate job of creating the filters and you're clearing the blocks and you get these entire blocks.
So the only way that you're going to have an incorrect balance is if the server somehow malleates a filter but there's not really a good, you know, it's kind of a weird, unclear attack vector.
So how practical would it be to actually get some kind of proofs on top of the balance that you're already producing?

Speaker 1: 00:16:35

Yeah, yeah, that's a great question.
So, so, so, I'm sure the exact name of this is so, so what we want is a Merkle inclusion proof, right?

## Miracle Inclusion Proof

Speaker 1: 00:16:45

We, we, We just want to say that this transaction is part of this block and to do that we need the log, if n is the number of transactions, we need log n kind of hashes to show inclusion.
I think we use this kind of vertical proof of inclusion somewhere else, but I'm forgetting.
I think there's a wallet that that uses these.
But yeah, so to include those that would be more costly.
And yeah, to be clear, today we definitely do not have any kind of, you know, there's no proof that the server is really serving you the right data.
So that is a big problem.
Obviously, we need to kind of have some proof.
The good news is, yeah, we could always add Merkle proofs of inclusion.
If you do the math on the size of those, it's like roughly, I think I looked at this before, it was something like on the order of hundreds of bytes, maybe 200 bytes or something.
So, it would be a significant increase, but possible.
I'll highlight one alternative way of doing this, which is actually suggested in the bit, in bit 157.
There, what we could instead do is actually continue to use block filters, but use PIR for the block retrieval part.
So you would retrieve blocks using PIR, but you would use client block filters as normal.
I think the problem there is it doesn't save on your bandwidth.
I could be wrong, but I think most of the bandwidth is coming from the filters and coming from the streaming to the client of the filter data.
So you wouldn't say that.

Speaker 0: 00:18:28

Just as a heads up for you, we're downloading the filters from our server, like the Wasabi backend server, but then the blocks are downloaded from the Bitcoin peer-to-peer network.
So the server doesn't incur the block download cost.

Speaker 1: 00:18:41

Oh, okay.
So is the main cost for you guys right now actually the filters because you incur that cost as I see.
Yeah, it's a large outgoing cost.
I'm sure your hosting provider is charging you.
Yeah, okay.
Yeah, So, yeah, actually doing proofs of inclusion is possible, but yeah, it's good to know, yeah, you need that kind of to deploy this for real.
If I can ask a follow-up question, do you guys, do you guys, to do this, do you, Are you mostly querying the UTXO set, the full set of transactions, just balances?
Like what kind of data is crucial?

Speaker 0: 00:19:30

We do want the full transaction history list.
Yeah.
And so that's what we get in the filters right now.
Wasabi is SecWit only, so we don't have to create filters pre-SecWit, August 2018 or something, or 17.
Okay.
Yeah.

Speaker 2: 00:19:48

And the filters are as large as the number of BEC 32 addresses in the blocks?

Speaker 1: 00:19:55

Sorry, say that one more time.

Speaker 2: 00:19:57

The filters are all essentially a compact representation of all BEC 32 addresses in a block.
Single public key.
Okay, yeah.
Single public key BEC 32 addresses.
So they're very compact, you know, three years ago, because it was a minority of people use those addresses more and more they become larger and larger but they're they're they're very space efficient I would I don't know the exact details maybe Max can answer but the exact

Speaker 0: 00:20:31

number of megabytes or something I think it's below a gigabyte I might be off here but it's not that much.

Speaker 2: 00:20:39

Oh below a gigabyte for the entire four years.

Speaker 0: 00:20:43

That might be complete bullshit But I think yes.

Speaker 1: 00:20:47

That sounds right.
I mean, it's not that much data, right?
Because it's also statistical, right?
It's a Bloom filter-esque thing, right?

Speaker 2: 00:20:56

That's right.
When it's not exact, then there are some false positives, but there are no false negatives.
That's the goal.
You'll never miss.

Speaker 0: 00:21:08

But you will get more.
Yeah, that false negative, that false positive rate can be configured.
And the lower you want that first positive rate, the larger the filter size is.
I'm not exactly sure where we fall in the line of tradeoff here.
Yeah, I don't know details like that.
Lucas is in the call, so maybe he knows.

Speaker 1: 00:21:34

Happy to take any other questions, Elsa.

Speaker 3: 00:21:38

Hello, guys.
It's quite nice to be here.
I don't have any strong background in crypto and higher order math, but as a layman, you know, is there a way to simplify the explanation of how homomorphic encryption works?
I have tried to see the, you know, the information on the internet, but it's just not possible for a basic layman like me.
Would that be possible on this call, or is it not?

Speaker 1: 00:22:17

Yeah, I have a slide.
Let's talk a little bit more about Wasabi Wallet and privacy, but then I can give that explanation.
Does that sound good?

Speaker 3: 00:22:28

Yes, thank you very much.
Thank you.

Speaker 0: 00:22:34

What I do wonder is, you do need to know the input, like the value of the UTXO that you're trying to spend.
Does your database include amounts?

Speaker 1: 00:22:49

Yes.
Yeah.
Yes.
So the total size of our database is roughly one gig right now.
We translate every, all UTXOs kind of reduced down to about a gig of data.
If we instead made the set all UTXOs and we didn't just take the five most recent ones for every address, the database would not be much larger.
It would be like a small multiple, like maybe three or four times larger, that would be kind of feasible.
I guess when I'm thinking about it, I suppose it helps that you guys only support the BEC 32 addresses, because That means there's kind of a limited set of addresses that are on chain that have transactions for that.
But yeah, we need to think about how big would it be to include all transaction history?
Because UTXOs are very different than every transaction.
So, yeah.
OK, It's good to know what the...
Yeah.
And just to ask one more time.
So, the problem that you guys face with block filters is Mostly that you have to download this gigabyte of things to get started.
Is that the issue?
Mostly?

Speaker 0: 00:24:08

So you have to download, first of all, the server has to generate filters, which can take weeks.
Then the clients have to download all the filters, which we do over Tor, which also can take an hour maybe.
I see, right.
I forgot it's all over Tor.

Speaker 1: 00:24:23

So that also… Exactly.
Yes.

Speaker 0: 00:24:29

And Then for block downloads, we spin up a new Tor identity for every Bitcoin peer that we download a block from.
So all of this together is, if you have a really big wallet and you're making a full rescan, I mean, it can take a couple of weeks, if not a month.

Speaker 1: 00:24:47

I see the issue.
Yeah, so there, yeah, weeks if not a month.
Yeah, okay.
So,

Speaker 2: 00:24:57

Let me just add one more thing.
So when you use Wasabi Wallet, you're making many addresses because you're you're quenching so you have to make a new address every time and if you use the wallet regularly you might go through something like 300 addresses or 400 or thousand over time that means that what you're looking for in the filters is actually quite broad.
And so you get more and more false positives.
And so if you just think it through, you're going to have a thousand blocks or more.
And each block is actually more than a megabyte typically.
And so you might end up with a gigabyte of blocks that you have to query, and each one is queried from a different node over a different Tor circuit.
Not necessarily a different node, just a different Tor circuit.

Speaker 1: 00:26:00

So I guess there are two things to ask here.
One is, so one thing to notice, it's perfectly fine to use this homomorphic stuff with Tor.
They're orthogonal.
One hides your IP and one hides the content of your queries.
Doing both is probably a good thing.
But I wonder if what homomorphic encryption could allow you to do is not construct a new circuit like every time.
So if the query is encrypted, in some sense you don't need to use Tor, but if you'd like to also kind of hide your network level identifier, you could do both and use Tor, but not build a new circuit every time and instead just make many private queries to the same node.
This would be presumably faster because Tor circuits can reach decent bandwidth, right, but not if they're, I think, freshly constructed every time, right?
Then you're going to pay the latency.

Speaker 0: 00:27:02

Can we actually make batch requests with Spiral, like requesting multiple addresses simultaneously?

Speaker 1: 00:27:10

Yeah, yeah.
So if you notice today, no, right?
I mean, we just have like a text field with an address.
We want to support that.
There's actually a lot of theory and research about doing batch requests kind of more efficiently.
So Yeah, I think it's really useful to hear that a very typical use case is like hundreds of addresses, because that says a lot about how we need to build this to make it usable.
So yeah, OK.
Yes, so batching is possible, but it's in the works.

Speaker 0: 00:27:56

Yeah, by the way, it's way more than just a thousand.
I'm checking a not even that old wallet and it has well 8,000 addresses here 13,000 addresses so since we do you know we do we attempt many coin joins and a lot of them fail and we generate new addresses for each attempted coin join and you can register up to 8 outputs in a round so let's say a round fails, I don't know, 5 times before it succeeds so that's 5 times 8 addresses that we have to add to your gap limit.

Speaker 1: 00:28:35

I see.
So are the addresses that you create there, are they unspent?
Do they contain any...
I mean, If you create an address and no one hears about it, did it really get created?

Speaker 0: 00:28:50

Well, in this case, yes, because the CoinJoin coordinator hears about it.
And probably also the other CoinJoin signers.
So it's semi-public.

Speaker 1: 00:29:00

Yes, but it never...
Will it store value?
It will, right?
I guess to start the Coinjoin it has some value in it.

Speaker 0: 00:29:09

No, sorry.
So we spend inputs that are addresses with money on them, but then on the output side we create new addresses that are not yet used without money on it.

Speaker 1: 00:29:18

Oh, I see.
So they can be empty output addresses.

Speaker 0: 00:29:22

Exactly.
Those are addresses that never were on the blockchain in an output with any amount of stats.
It's just unused addresses, so to speak.

Speaker 1: 00:29:32

So then those would not need to actually hit any kind of...
We don't need to query the blockchain for them at all, right?

Speaker 0: 00:29:41

Well, but the client doesn't know if an address is empty or not.
So we need to query all of them.
Just a lot of them, the server will say there's nothing on here.

Speaker 1: 00:29:50

I see.
I see.
Yeah.
So an easy way to actually resolve that will be to actually just make a set of addresses that have any money.
So this is a technique we actually use for the current service.
What you can do is instead create another database that just says, like, does this address have any money at all?
And that database can be very small, right?
Because again, we can use like the classic Bloom filter thing where we, it's not quite a Bloom filter because the addresses are already random.
So just take the X top X bits of every address that has money in it and send these to the client or allow them to fetch them using PIR, right?
So, yeah.
And WasabiWallet already handles the mempool, right?
You guys already kind of privately listen to everything on a mempool and then cross-reference it with the addresses you have and all that.

Speaker 0: 00:30:52

Yeah, we build a local mempool.
The issue is when we're offline, we of course don't know it.
So maybe actually some private information retrieval over someone else's mempool might be another interesting use case.

Speaker 1: 00:31:07

Yeah, so.

Speaker 0: 00:31:12

So, sorry, a bit more about the batch requests.
So, like, would it be possible to just send 10,000 addresses to the server and he responds in a single package?

Speaker 1: 00:31:26

So it's definitely possible.
I mean, the simple way is, yeah, You can send 10,000 queries, you can upload them all, and then just kind of the server can just do all the computation and send you all the responses.
The problem is going to be, well, the problem is going to be twofold.
One, there's a significant cost to running a query.
So a query costs today like six CPU seconds, right?
So six CPU seconds is not nothing, but it's also, it's something, you know?
Like It's a significant cost.
So 10,000 addresses times six CPU seconds is 60,000, it's a thousand hours of computation.
So it'll be tough.
So in order to make that work, to make 10,000 addresses work, What we need is to do batching or reduce the number of addresses that we're effectively querying by, like I said, figuring out whether the addresses are empty or kind of reducing the set that way.
But yeah, 10,000 is hard.
The other thing is, the other problem is going to be communication.
So like every query is 14 kilobytes.
So 10,000 times 14 kilobytes is, you know, a lot.
And then that's a lot of 140 megabytes to upload.
So it's not going to be that feasible.

Speaker 0: 00:33:00

Actually, to this I have a question, because I saw on the website that the first request, the client needs to send more data, and for every following it's less.

Speaker 1: 00:33:09

Yes, yeah.
Why is that?
Yeah, it's because the first request contains what's called the setup data or the public parameters.
Basically, the server sends essentially like an extended, like a large public key to the server.
So the server uses this public key to kind of let it do the query processing.
So it's state that the server needs to store on a per client basis, but it has no privacy implication.
It's just used for the homomorphic processing.
So that's why it's big.
And you might have noticed it's pretty big.
It's like eight megabytes or something.

Speaker 0: 00:33:59

And Does that size depend on the database size?

Speaker 1: 00:34:02

It does not.
Or it only logarithmically does.
So it's like very, I mean, like if the database was 100 times bigger, it would be like 12 megabytes or something.

Speaker 0: 00:34:17

Yeah, like, I mean, just general, like, it's a very broad question, but is it, so if we want to have the full TX outset of all, like, of, but actually, we probably also want transaction IDs and stuff like this so basically we want the full transaction metadata blockchain thing for all sacred and taproot outputs yep and let's say we have I don't know 10,000 users or so and each of them has let's say, a thousand addresses or so.
And this is still rather small scale, but is this completely crazy?

Speaker 1: 00:35:03

Yeah, no, no, no, you're asking a very, very good question.
So, so I think that the way that it's not so so that's, that's very true.
So, so I think like, It is difficult, especially from a cost perspective, I think, for the server.
It's difficult to see this scaling to, I check 10,000 addresses kind of regularly.
Like Every day I check 10,000 addresses and there's like 10,000 users.
That will quickly become difficult for the server.
But I think there's two things.
One is the set of active addresses is not 10,000.
So what can we do to kind of like reduce the number?
Two, it is just a cost for the server.
You know, computation is just money, as we know from proof of work, right?
So A question is, you know, if clients were willing to pay for it, if I was willing to pay for six CPU seconds for my query, maybe that would be okay.
I might not be willing to pay 10,000 times six CPU seconds.
So we'd have to see what clients are kind of, you know, quote unquote willing to pay.
And then also, I guess the last thing I would say is it would be very feasible to use PAR just for blocks.
So if you think that the privacy leakage is an issue or you're interested in that kind of angle on it, I think just doing PIR, just in that block retrieval phase of the standard client block header thing, if you want to do PIR, I think that is very feasible.
Is very, very feasible.
One other thing, I think that there's kind of like a, there's also like a kind of narrow use case for just like onboarding or just like set up.
I think if you're like a client is setting up and it's taking weeks to sink your wallet, I think it's really powerful that in the meantime you can, you can make queries, for, for addresses.
You can see if you've been paid

Speaker 0: 00:37:21

privately.
Yeah, exactly.
Right, to just get the active wallet balance really quickly.

Speaker 1: 00:37:26

And yeah, so no syncing, no.
Right.
So actually it might even make sense just as a kind of, yeah, as a fallback or even kind of as a like setup thing.
I mean, the fact that you don't incrementally have to do anything, like each query costs the same and, or I guess the first one costs a little more, but basically there's no sinking, right?
There's no like client state that I'm trying to get into sync with the chain.
I'm just kind of, I can make a query kind of one-off.
Something I noticed is, can you query the balance of an address that's not in your wallet today?
I think you can add a public watch address but you can't you can't actually use it like a block explorer, right?

Speaker 0: 00:38:08

Yeah, you cannot and the problem is you would have to run this address through all the filters, download all the past false positive blocks And so it would take a

Speaker 1: 00:38:18

long time.
I don't know if that's a feature.
Yeah, I don't know if it's a feature you guys are interested in, but I think it would be useful to be able to just say, hey, what, you know, like, yeah, how much is at this address?
Because today, you know, the option is to go to a Chrome tab and type it in and send it to, you know, who knows, send it to blockchain.com or whoever.

Speaker 0: 00:38:40

Yeah, and by the way, if you receive a transaction and you want to, Then you don't know the inputs of that transaction.
So you, sorry, the input amount of that transaction, because that's on the blockchain, not in the transaction itself, right?
It's on the previous transaction output.
And then you cannot do effective fee bumping in a child pays for parent transaction.
Because you'd...
So this is an issue that we have of kind of quote-unquote stuck payments that you received.
And maybe something like that might be helpful.
And so you can query the amount of that input and then do better fee bumping.

Speaker 1: 00:39:24

I see.
I see.
So to summarize, You know you received a payment, but you just don't know how much it is, essentially, because that information is just kind of not local.

Speaker 0: 00:39:38

No, so you receive a transaction where on the output side your address is.
That's why the transaction was hit in the filter.
But you don't know the value of the inputs exactly, because that's in the previous transaction output.
So you don't know the fee rate that this current transaction has.

Speaker 1: 00:40:00

You know that it's less than or equal to, but you don't know what gap was left for the minor in the form of the fee.
I see.

Speaker 0: 00:40:08

Exactly.
And then you can't do child pays for parent fee calculations.

Speaker 1: 00:40:14

So that is a, yeah, that is...

Speaker 0: 00:40:17

It's just one of those edge cases where we thought it would be nice to be able to just well search for an address.
Yeah.
But then we realized, yeah, it'll take minutes, you know, hours.

Speaker 1: 00:40:30

Right.
I think, yeah, so long term, I guess I have a slide on this, but, oh, no.
I think long term, we would like to build a, like an SDK, so that we're not kind of like individually hand engineering the homomorphic encryption, but so that it's kind of a totally generic thing.
So the dream is that there's like a piece of code that you point a bunch of, like basically an array app, and then there's an endpoint that you can privately query that data using.
So certainly for all these kinds of smaller things that you want to do, that really kind of makes sense.

Speaker 0: 00:41:12

Definitely.
Oh yeah, by the way, to jump back.
So you say the client needs to upload his Quantico public key to the server.
So then all the queries are connected to the same public key?

Speaker 1: 00:41:26

So all of the queries are made using the same, yes, each query is connected to the same, let's say, key pair.
The crucial part is that every query is encrypted.
So it's encrypted under this key.
So it's not, the queries, I guess, are identifiably from the same party.
But what the queries are for is not.
So I guess there's some there, you're right, there's some meta metadata almost that's that's still visible, right?
Because you can see, I guess, the main leakage is timing.
So you can see that some party made five queries over this period of time.

Speaker 0: 00:42:12

I see.
So you want to go extreme and even hide this type of metadata, then we'll use a different public key or key pair each time.
So then that means upload more data for every query.
And then do some randomization of the timing as well, plus new for circuits.
And then it gets a lot more inefficient as well.

Speaker 1: 00:42:32

Yeah, some mitigations for timing are just pacing.
So a simple thing you can do is just kind of like just paste requests and send dummy requests.
But yes, obviously these incur costs.
So yeah.
Yeah, I mean, today, if you want to do the same thing for block filters, you are kind of stuck in that.
I mean, the timing alone of your request is going to kind of correlate them.
So yeah, it is kind of a tough problem.

Speaker 0: 00:43:08

That's why batch requests are also very important, I would say.

Speaker 1: 00:43:13

Yeah, yeah, certainly a batch request where we round up the size.
So like, it would be important to kind of like, not reveal the exact number of addresses you have in your wallet, just because that is probably kind of identifiable.
So yeah, if we just round up the number of addresses and let you query, you know, up to X thousand addresses at a time.
I will do some more research and thinking on batching.
It's very useful.
Thank you so much for like talking to us and letting us hear your problems and stuff.
I think it would be useful to go back and look at batching and see if it can be practical.

Speaker 0: 00:43:57

Super cool.
So then, how long does the request take?
So let's say we want to look up a thousand addresses or so, how long does the client have to wait?

Speaker 1: 00:44:12

The client has to wait for as long as it wants to, almost directly in proportion to how much it's willing to pay.
So I mean, if you want to make a thousand queries, right, let's say it's, you know, 5000 seconds of computation, right?
If you pay the server, as you know, computation is like, kind of cheap and parallelizable.
So you can imagine a server, especially like in a search look, basically like a cloud provider or something that just goes, okay, if you pay me 5000 times one cent, or, you know, point one cents or whatever.
I'll, I'll process your query in one second, cause I'll just throw 5,000 cores at it.
So, so it is kind of, it is infinitely divisible.
It's, it's naively parallel as an algorithm.
So.

Speaker 0: 00:45:01

That's really interesting to hear.

Speaker 1: 00:45:06

So yeah, there's a nice, Yeah.
There's an interesting intersection with the fact that this is all for a payment system, right?
So It would be interesting to think about.
Yeah.

Speaker 0: 00:45:19

Okay, I think I'm pretty much out of questions for now.
Does anyone else have any?
No, then would be nice to get a bit more into the crypto magic.
If you could.
Sure.
Sure.

Speaker 1: 00:45:30

I I'm If this altitude is kind of too much or too little, let me know.
The slide is kind of gross looking.
But I'll just walk through the basics of how this works.
So, here's how this kind of works on the inside.
So, basically, remember we have a client and a server.
And we'd like the client would like to retrieve an item from this database of items without letting the server learn which one in queries.
So basically, if we imagine our index is three, like we want the third item of the database, what we're going to do is we're going to have the client create a kind of bit vector.
So a vector of bits.
If you remember linear algebra, I'm using the word vector kind of on purpose.
So it's a column vector of bits where it's a one-hot encoding.
If you've been around machine learning, you might have heard the term one-hot before.
But basically that means there's a one in the location that I want to retrieve and zeros everywhere else.
So there's a zero in these entries and there's a one at the desired index.
So I'm going to form this vector.
It's just a plain text bits on my client.
And then I'm going to encrypt each of them.
So I'll explain, you know, the encryption we use has a special property, which we'll get to, but basically it is also, it behaves mostly like a normal encryption scheme.
So you encrypt each bit, and now these, you know, these encrypted bits get sent to the server.
And just like if you AES encrypted them, the server can't tell what any of these bits encrypt.
It's kind of crucial to remember that the encryption of zero and the encryption of zero, they don't look the same.
Every time you encrypt zero, you get a different looking random thing.
And the server cannot distinguish whether you encrypted the same thing or a different thing.
So that property applies.
It's called chosen plaintext security or semantic security.
But basically, yeah, this vector of encrypted bits, it's not visible to the server which ones are 0 or which ones are 1.
So that gets sent to the server.
And then how does the server actually figure out the answer to your query?
Well, if you look at the plaintext database elements in green, it does this kind of special.
This is the special property of the encryption.
The encrypted zero gets multiplied by the plain text eight here.
And what we get is the encrypted product of them.
So if we multiply encrypted zero by six, we'll get zero.
If we multiply encrypted one by seven, we'll get encrypted seven.
So the point is this ability to do this multiplication, that's not normal.
Normal encryption doesn't let you do that.
So if you AES encrypt zero and then like multiply by eight, you will just get garbage.
There's no, it does not become like encrypted zero.
This is...

Speaker 0: 00:48:38

Sorry, on the left and right hand side, the number four, E zero times eight equals E zero.
Is the two times E zero, is that this exact same thing or just a different encrypted blob with the same zeros clean text?

Speaker 1: 00:48:55

It is not the exact same thing.
So do you mean on the left and right, like this encrypted zero and this encrypted zero?

Speaker 0: 00:49:02

Yes.

Speaker 1: 00:49:04

Yeah, so they are not the same thing.
They actually, again, to the attacker, look completely indistinguishable and random.
So they both look, what they encrypt looks completely hidden to the server.

Speaker 0: 00:49:27

Nice.
Thanks.
Continue,

Speaker 1: 00:49:29

please.
So then you can do the same thing just like we multiplied, you can also, you're allowed to add.
So if you add encrypted zero and encrypted seven, you get encrypted seven and so on.
So you kind of add all of the results and now you have a single encrypted result that you can send back to the client.
The client can decrypt and get the item that it wanted.
So this is how it's kind of, let's say, possible to do this.
You should, there's probably one glaring problem with this toy example, which is that we uploaded in our query the same number of elements as are in the database.
So, our query is very, very big.
You know?
So, that's a problem.
So, in the real scheme, there's kind of a whole bunch of complicated stuff you can do to mitigate that.
Basically, you can kind of structure the database as a cube and kind of send bits that correlate to each kind of dimension or axis on the cube, and then you can multiply and reduce that way.
And that makes the query smaller, you know.
So, but this is the gist of it.
This is how it works.
So, the point is, now you can maybe conceptualize how if there was an encryption scheme that did these things, then you could do PIR.
You know, If there was an encryption scheme that had this multiplication and this addition operation, then it would all work.
So then the question becomes, okay, well, how do you get an encryption scheme like that?
It's not something that AES does.
It's not something that even ECC really does.
So, yeah.
The process of getting that is more involved.
But that's the gist of this is the gist of how this scheme works.
Any questions?
I know it's like a super, it's complicated, so I'm happy to answer anything.
I haven't given this talk that many times, so it's a little, I'm happy to answer anything.

Speaker 0: 00:51:31

Yeah, that's, it's pretty nice.
The data size in number 4 for the orange boxes on the right, so E0, E0, E7, E0, and then underneath the sum of E7 again, So is the data size of these orange blobs different, especially the sum?

Speaker 1: 00:51:52

Yeah, it's a great question.
So no.
So all the orange blocks have the exact same size.
So that's a very good point.
Like this vector of encrypted 0's and 1's, it's not small, Because every one of them is big enough to hold a plain text element, so it's pretty big.
There are a bunch of things you can do to kind of not actually send encrypted zeros and encrypted...
So I guess I can just explain it this way.
So the operations we have are homomorphic multiplication by a plaintext item.
And like here, and addition.
I don't know your familiarity with linear algebra or something, but that's a not quite complete set.
If you were also able to multiply two encrypted numbers, you can kind of do the...
You can think about it and see that actually you can compute any function on encrypted data if you have addition and multiplication.
You know, addition and multiplication kind of...
Every computation is like a composition of adding and multiplying.
All our computers do are add and multiply.
So there are ways to compute an arbitrary function on encrypted data.
So what that means is the query is now much smaller and you perform this arbitrary computation to make all of these encrypted zeros and ones in a big way while keeping the query small.
So yeah.

Speaker 0: 00:53:39

Let's go to more.

Speaker 3: 00:53:42

OK, this is where I saw this illustration, because I sent maybe the link to it before.
My question is what is the mathematical principle that enables this?
I'm a bit familiar with linear algebra.
So that's, yeah.
Yeah.
So, yeah.
Yeah.

Speaker 1: 00:54:09

So the main principle is that it's difficult to kind of invert matrices when they have noise.
So I can say more about that, but basically what that means is like if you have a matrix, a large random matrix, and you multiply it by a vector, The outputs are easy to determine.
The output and the input vector are kind of correlated.
It's easy to invert the matrix and figure out what the input was from the output.
So if you have A, S, you know, if I give you A, S and I give you A, it's easy to find S, because finding the inverse of a matrix is not hard.
But the key insight, the algebraic insight that enables this is that, Well, if I give you AS plus E, where E is just some very small noise, suddenly the problem is very hard.
It's very hard to figure out S from AS plus E.
The post has, I think, like further down kind of a discussion of like learning with errors and stuff.

Speaker 3: 00:55:23

In programming we have this concept of you know in IEEE floating numbers there's epsilon.
Was that related to that E?

Speaker 1: 00:55:34

No, no.
So it's not like super small.
I mean, when I say small, I don't mean like infinitesimally small like epsilon.
I just mean that it's small relative to the size of the of the of the data.
Yeah, so it's small enough that when the client decrypts, it can kind of round away the error.
So you can think of it, it's less like epsilon, more like error.
Like that floating point error where you add 1.00001 and 1.00001 and you get 2, because of that floating pointer, it's analogous to that.
It's more like there's the small error that you can ignore at the end.
Also to Max's point, I remember I forgot to mention something which is interesting, which is you asked whether this left and right thing are different.
And they are, to the attacker, they're indistinguishable.
But something that is happening that is kind of interesting is that each ciphertext contains noise.
So what's happening every time we do one of these operations is the noise inside the ciphertext is growing.
And when I say noise, it's kind of sounds fuzzy, but basically there's noise inside every ciphertext.
And as you do operations to it, noise grows.
And when the noise is too big, when you decrypt, you'll get the wrong answer.
You'll get an incorrect decryption and you won't know it.
So part of it is that there is something happening when you do these multiplications and these additions.
The noise is growing.
You can't do it an unlimited number of times.
Otherwise, the ciphertext will kind of become garbage.

Speaker 3: 00:57:19

Okay, that's the way you explained it in the terms of matrices.
Yeah, I think it clicks something on me.
You know?

Speaker 1: 00:57:28

Yeah, sure.
Yeah, feel free to reach out if you have other questions.

Speaker 3: 00:57:33

Yeah, sure.
Another thing is that how do you get this kind of noise?
Does it, when you deal with the floating numbers, just a little bit of noise can throw off calculations like in physics and stuff.
How is that dealt with this encryption scheme?

Speaker 1: 00:57:55

Yeah, it's a good question.
So we, yeah, I mean, for the noise we use is sampled from the Gaussian distribution, so like a normal distribution.
And what we do is like we kind of, before we run a computation, we kind of almost like predict or check ourselves.
We check, okay, if we do this computation, what's going to happen to the noise distribution?
And we kind of calculate like a bound.
We calculate the standard deviation of the noise distribution at the end, in advance.
And we make sure that the noise distribution is not so wide as to make the ciphertext unreadable, as to cause an error in the decryption.
So basically what we do is we bound the standard deviation of the output noise.
And by doing that, we can say the noise will always be within six standard deviations of the mean and we know the standard deviation is going to be x and so we know that we will decrypt correctly.

Speaker 3: 00:59:11

Yeah.
Okay, cool.
That's all for me.
Thank you so much.
Yeah.

Speaker 4: 00:59:19

Hello, guys.

Speaker 0: 00:59:23

Hello.
Hey, Adam.
Glad that you're here.
Catch the recording.
It was very good.
I do have another question, and that is about the...
So I saw the client on GitHub and mentioned that this is free open source.
What about the server?

Speaker 1: 00:59:42

So the server does not need to be open source because of homomorphic encryption guarantees.
But I think we still are open sourcing it.
So the server is at my GitHub.
It's at this one.
I think this is our old repo.
So I can message it in the chat.
So there is a server here.
So we also have the server open source in public.
I do think that the really crucial part is to get kind of reproducible builds and stuff on the client.
Because the client, as long as you trust the client, everything else is fine.
So yeah.
But obviously for an open standard, we're going to need open source clients and servers.

Speaker 0: 01:00:35

Cool, thank you.

Speaker 4: 01:00:36

So I just arrived.
Is there a way to summarize whole Spiral work in a, like, like on five?

Speaker 1: 01:00:54

That's magic.
Sure, sure, sure.
Yeah, I think the summary, the best summary is honestly Max's at the beginning, which was just like, basically Spiral is a way to retrieve an item from a database without letting it ever learn what item you retrieved.
And the way it works is kind of complicated but

Speaker 4: 01:01:14

yeah.
What does that mean?

Speaker 1: 01:01:18

Okay, okay, I can do a little, I can explain a little more.
So, so yeah, the way it works intuitively is basically the client sends this kind of encrypted vector of bits.
Encrypted vector of bits and the server does like an encrypted dot product between the bits that the client sends and the items in the database.
And the point is, you know, The one bit will kind of be the item that we want, and the zero bits will kind of cancel out all the items we don't want.
And the server will add these all up and send it back to the client.
And the point is the server never learned, you know, what the encrypted bits were.
It never learns what the sum of everything was.
It just kind of does the computation and sends the encrypted result back to the client.

Speaker 4: 01:02:12

Oh, okay.
Okay, it's like a cryptographic challenge

Speaker 0: 01:02:16

protocol

Speaker 4: 01:02:20

that's like the server is sending bytes, but those bytes are not the address, but somehow be the client server challenge, you can establish the address or the information that the

Speaker 1: 01:02:40

server is sending

Speaker 4: 01:02:41

on the client.
Holy shit,

Speaker 1: 01:02:44

that's something.
Yeah, so the client is sending an encrypted version of its query and it gets an encrypted response.
And the point is the server never decrypts anything.
Yeah, that's the point.
Everything stays encrypted.
So it's kind of like, it's almost like end to end encryption.
Like, like end-to-end encryption.
The catch is that it's expensive for the server to do the computation.
So you know the server has to invest a lot of effort to kind of answer your query.
So you might need to eventually pay them or like in some way incentivize their their behavior

Speaker 4: 01:03:23

How expensive is it so expensive as?
For the entire Bitcoin transaction history Blockchain wouldn't be able to run on a single server no matter how big you are trying to buy?

Speaker 1: 01:03:40

That's a good question.
I mean, it used to be impossibly big.
It used to be like, you know, I would say years, you know, to do a single Bitcoin address lookup.
But today it's not so bad.
So today there's been a lot of innovation.
Today you can look up a balance of an address today at our site, like, very easily, and our server costs, I think, like, 50 bucks a month to run or something.
It's not an expensive server that we run.
So, today, it's not too bad.
I think doing all of the transaction history is definitely more costly, but it's not infeasibly costly.
I think it gets maybe really bad if you are trying to query tens of thousands of addresses.
Then we'll have to think of a better way to kind of batch your queries.

Speaker 0: 01:04:38

Yeah, so Adam, there's multiple layers of why this might be very difficult for us to use.
One is we might want the transaction history, so this is the whole TX outset instead of the

Speaker 4: 01:04:49

UTXO set.
We definitely want that, so we cannot get that?

Speaker 0: 01:04:55

We could, but then the size of the database gets larger because you need to store all outputs, not just the unspent ones.
And so that's the first issue.
The second

Speaker 4: 01:05:05

issue is because- But how large?
Like so large that we cannot run on a server or we can buy that big server for it?
I mean, come on, like seriously, if this is the issue and we could buy a server for it, like I think it would be worth it because, you know, this is the single most problematic thing that we have performance-wise in Wasabi Wallet.
But this is why we are not like Blue Wallet.
This is the reason and if it would be feasible, then I think it would be worth it.

Speaker 0: 01:05:53

But let me try to summarize the complexity of why it might still not be feasible.
Yeah, there are other...
Exactly, there are others.
So one is the size of the database.
The other is the number of addresses that a single client is looking for.
And my client often has over 10,000 used addresses.
And so we would need to query all of them.
And not just once, but every time you load the wallet.
And so we have I don't know 10 000 users with each 10 000 addresses making queries over the entire blockchain database so to say that's that turns very expensive very quick And however a solution around this is...
You would have to only do it once.
Well, next time you open the wallet, you might have received a coin to one of those many addresses.

Speaker 4: 01:06:49

Oh, yeah, you're right.
Yes.

Speaker 1: 01:06:53

So I think there's a couple of layers.
So yeah, Max and I went through this.
There's a couple of layers of mitigation you can do.
So one layer is you can also just look at which addresses were because of kind of this homomorphic encryption thing, because you can query kind of arbitrary data as long as the server kind of forms it for you.
You could have a database that says, when were these wallets last interacted with?
You could just query that database and you could find out, okay, 9,000 of these addresses, nothing happened on them since I last opened this app.
Right.
And then for the thousand that are remaining, you could look and see, you know, which, which ones of them have a balance still or are still active.
And then you could retrieve each of their transaction histories kind of individually.
It's not perfect, but something I'll do is I think I will, I will try to build up a number of addresses in my wallet that's large enough to kind of test with.
And I would love to play around and see how this could work or at least, yeah.
Yeah, I think it's a kind of urgent challenge.
So, yeah, and it's cool tech.

## Private Information Retrieval from a Database

Speaker 0: 01:08:20

Another interesting, like, the cool thing is like private information retrieval from a database.
It seems massively big as a concept.
And we can use it in many different areas.
One, for example, might be to query the mempool of someone else, which you boot up your client and you have unconfirmed transactions and this way you could be able to get them.

Speaker 4: 01:08:45

So I did that in hidden wallet.
I was querying the entire mempool of all the nodes I'm connected to, but it got expensive pretty fast.

Speaker 1: 01:09:02

If you're interested in the checking addresses you don't own, I think that's also very feasible.
I don't know if that's interesting.
But I think that today your options are pretty bad.
So I think at least on that front, yeah, we're kind of clearly better than the best way you have today to kind of look up the address of a balance that you don't already have in your wallet, of an address.

Speaker 4: 01:09:35

So that is a super important point and that might...
So what are people looking in block explorers?
They are looking at quite a few things there.
But building a private block explorer based on this protocol might actually be possible.
Yes, that's a huge thing, really huge.
Right now, people are putting in, and people, I mean, I do that as well.
We are putting in our addresses in block exporters to check if everything is going well or how well was constructing wasabi this transaction, stuff like that.
And well, that's a huge database that block explorers have.
So that's pretty problematic, I hope.
It's not gonna be like that well-known fact that they are going for block explorers to disclose data.
You know?

Speaker 1: 01:11:00

Yeah, I mean, if I was, I would definitely subpoena Block Explorer.
I think Ledger keeps their logs on Ledger Live for like five years or something.
So yeah, I think, I think, Yeah, I don't know if you guys are interested.
I think that's another angle we're interested in is this hardware wallet kind of integration.
I think it's kind of funny how you go to kind of you're currently able to go to Greatlands and kind of keep all your private keys on hardware.
But then when you want to just like know how much money you have, you kind of have to, you have to just, you end up kind of just going to a block explorer or ledger or whoever, and kind of just telling them your address and your IP address and stuff.
So yeah.

Speaker 5: 01:11:46

You could connect it to your own node, right?
Yes, yes.
I guess, to it and stuff, so yeah.

Speaker 1: 01:11:53

Yeah, yeah.
Especially from mobile clients and stuff.
Yeah, no, go ahead.

Speaker 0: 01:11:58

You know, even when you connect to your own node, which is the scenario you brought up earlier.
But the problem with this is you still put your sensitive information on another computer.
And sure, you're the one mainly in control of that computer, but maybe you get hacked, or maybe you are already hacked.
And So the less information you store on someone or on another computer, the better.
Like an existing example is ElectrumX versus ElectrumPersonalServer.
ElectrumPersonalServer stores your extended public key on the server versus ElectrumX only receives an address and then forgets it later.
Right, so if someone walks into your house and takes your Electrum personal server, he knows your XPAL, versus if he takes your ElectrumX, he knows nothing.
So this is better in the sense like I would want to run a Spiral block explorer on top of my own node, just so that if someone gets hold of my computer, he still doesn't know anything.

Speaker 1: 01:13:00

Yeah, I think another way to think about it would be, you know, if you want to just kind of like not do the management, but get all the privacy, I think this is the way to do it.
If you run Spiral in AWS, you know, like you can be very confident that they don't learn anything about what you query.
But you also don't have to take it with you when you move and figure out your ISPs, like static IP situations so you can use it on your phone when you're going somewhere or something like that.

Speaker 4: 01:13:35

So if I understand it correctly, the reason why we cannot use it is because There are two problems here.
First, if we want to have the entire transaction history of an address, then we would have to run a server that might be too big for us.
There is no such a server existing in this world to run that.
And this question could be investigated, right?
And the other issue is that when you have tens of thousands of addresses, like it is taking long to make those tens of thousands of cryptography key challenge exchanges to figure out the entire transaction history.
So this might be taking like half an hour or how long?

Speaker 5: 01:14:43

If I may add something, you can have multiple servers, let's say in Amazon, and running them in parallel with Spiral on.
So it should be costly, but still more fast.

Speaker 0: 01:15:01

Yeah, for your info, this is a CPU heavier, but it's parallelizable.
So if we get a server with 50,000 CPU cores, then it would be super quick.

Speaker 5: 01:15:12

And you can have multiple of them.

Speaker 0: 01:15:15

But I don't think that's needed, right?
If you can just multiply CPU cores?
Is there a speed difference between having two servers with each five CPU cores versus one server with ten CPU cores?

Speaker 1: 01:15:30

No, not really.
I think you'll run into memory at some point.
I mean, you'll want to, you know, you'll start thinking, okay, well, if you put 5000 cores on a system with 8 gigs, you might get bottlenecked by other things.
So there is kind of a thing.
I will say, I don't think it's super feasible.
CPUs are cheap, but they're not that cheap.
So I don't want to...
I think I agree with Max's assessment that for this to be feasible, we need to find a way to do this for large numbers of addresses and not have it be like, you know, dollars per lookup, you know, like significant amount of money per lookup, because I think that's, that's if the goal is to lower the barrier to entry and to like, make it better, right, that's, that's going to be a roadblock.
It's going to be tough to, to want to pay a dollar every time you want to know how much money you have, you know.
So, I believe we can work on this.
I'm not, I haven't lost all hope.
I think it's really useful to hear that people have so many addresses and I want to know more about like what those addresses look like.
You kind of explained that they're kind of the outputs of a, of a, their output addresses as a result of a coin join, sometimes a failed coin join.
But yeah, the more I can kind of understand that, the more I think it could be feasible kind of to make progress.

Speaker 0: 01:17:12

Yeah, but I would guess the vast majority of these addresses are unused.
So they never made it on the blockchain.
And then only a rather smaller number made it on the blockchain and is already spent.
And so not in the UTXO set anymore.
And then the smallest percentage is going to be the unspent UTXO addresses.

Speaker 1: 01:17:38

Okay.
Certainly, I mean, spent.
So something cool about spent coins is that like, you know, once they're spent, they can't come back.
So yeah, we can exploit that.

Speaker 4: 01:17:56

Lucas, what's your take about all this?
Can we use Spiral somehow, if not even if it's a, can we use it to make Wasabi like really light?
Or even should we, even if we could work it out?
Mike, you are the one who wrote the Columbus Rites Theater stuff, so you put a lot of thoughts into around here.

Speaker 6: 01:18:37

Honestly, I don't know.
I would like to know more about the technology, but when I entered into the meeting, they were already discussing things that I mean, how to use the technology, but know what the technology really is.
So, I tried to do my best to understand.
Basically, what I think is the technology is clearly good.
Right?
So, I'm sure there are many scenarios that we can, many problems that we used to have can be solved by this.
But I don't know exactly how can we use it for our, let's say, for reconstructing our local UTXO set.
I mean, the UTXO set that is relevant for the wallet, right?
And all the transactions and all the information.
I cannot see it.
Basically because the problem that we have is mainly for new users, right?
Or users that have to, for some reason, to resynchronize the wallet.
But I use the wallet more or less frequently, right?
And it takes nothing for me to open, to synchronize.
It's just, to me, it's exactly the same as blue wallet, right?
It's very good.
So I think it, no, I think it doesn't worth the effort to even if the technology, no, no, the technology, even if the requirement of the technology in terms of bandwidth, storage, CPU, even if we can afford that, I don't know if we can afford to change the architecture of the wallet to use this technology, right?
And even if we can afford all of that, I don't know if the result will be so good because we have to do a lot of requests, lots.
And the process of discovering the wallet is the same, right?
I don't know what's the keys.
So I have to query one key, one key, one key, one key, one key, and we will discover that, oh, well, now I have to try with the next 21 keys or the next, I don't know, some of our users have minimum gap limits of, I don't know, 600.
I don't know.
So I have to query the next 600 keys.
No, I don't think it is possible.
However, I'm sure this is something, because the PIR technologies have been improving a lot and now it seems this is like something great, a great achievement, right?
Before, first time I read something about this, three servers were required for this because one server keep one table, the other server keep a different kind of information.
It was a feeling mess, but now it's getting, it seems it's getting better and better.
And so we have to have an eye on this technology, but no for synchronizing the wallet.
I'm pretty sure about it.

Speaker 1: 01:22:36

I think that

Speaker 2: 01:22:37

makes a

Speaker 0: 01:22:37

lot of sense.
Yeah, absolutely.

Speaker 1: 01:22:38

Yeah, yeah, yeah.
I, I, I, that your, your point about the multiple servers is, is funny.
Yeah.
I mean, it used to be that you had to trust that the servers don't collude, which is kind of a silly assumption.
Yeah, we've come a long way.
Yeah, yeah.
I think I'm really interested in this in this private block explorer thing.
And I think it might not be part of Wasabi wallet, but I think it's obviously part of like an ecosystem of private Bitcoin.
I mean, if you use Wasabi wallet, but then use a public block explorer, you're kind of fucking it up, you know, you're kind of not, you're kind of defeating some of the purpose of the wallet.
So I hope at least those two things sound kind of complimentary.

Speaker 6: 01:23:28

Sorry, yes, I completely agree.
In fact, many times we say, okay, how can we, for example, provide more information to the users, right?
Because basically a server has a global view of the blockchain while a client has only a local view of the blockchain, right?
So basically, the client many times can take advantage of information that only the server knows, but you cannot ask the server, hey, can you, could you please tell me this?
Because, well, in that case, you are revealing information to the server.
So, sometimes you want to say, okay, how can I ask for this to a central server without revealing my identity or my intentions, right?
So that kind of things is something that, that's why I say that we have to keep an eye on this technology.

Speaker 1: 01:24:33

Yeah, so that's a great point.
So I know I'm kind of more familiar, I have been in cryptography, but not crypto.
So I'm kind of like, I was really into Bitcoin in like 2015, I TA'd our class and then I like totally checked out.
Yeah, so I'm a little unfamiliar, but what kind of metadata, what kind of like data do block explorers provide about an address that is kind of that global state.
So I can think of like in the kind of Ethereum version, I can think of like, you know, I don't know, they like, I don't know, some NFT thing, they like, pull up some image or, you know, there's like that kind of data.
But what are you thinking of that is global that these explorers would show?
Well,

Speaker 6: 01:25:28

of course we don't know, right?

Speaker 4: 01:25:31

It's- IP address, Bitcoin address.

Speaker 1: 01:25:35

Ah, I see.
So what IP submitted this address?
Yep.
Are there, there's also, is there like a kind of naming, is there like a DNS equivalent, like people who use like op return to kind of store data in some kind of structured way to register a name or whatever.
That kind of data is also, while it's in the transaction, the metadata about it is not, right?

Speaker 0: 01:26:12

Maybe to combine the block explorer with a lightning explorer, so you would for example see which on-chain transactions are associated to a certain Lightning node publicly.

Speaker 1: 01:26:24

I see.
Yes, so that's information that's not local normally.
So today, I guess there's almost no private way to look that up.
I guess you just, your best bet is to use Tor and to use a public block explorer and be careful.

Speaker 0: 01:26:45

Different question, but since Lukas brought up that private information retrieval isn't a new thing, like why is Spiral new or how does it improve upon what came before?

Speaker 1: 01:26:56

Sure, that's a great question.
So yeah, I mean, there's so private information retrieval as a problem was posed.
Yeah, like in the 80s.
And there's been like a bunch of kind of talk about it.
But it never was practical.
My best my my biggest thing I always make fun of is like, I think IBM had like a big demo where you could look up like the 50 US states privately.
And it was like a big demo in 20, you know, I think 2019 or something, that you could look up 50 states.
It wasn't like a very large database.
It was like the capitals of the 50 US states.
The reason we've come a long way and what Spiral does, what advancement kind of Spiral made was basically just, it wasn't something super special.
It was a lot of, it was the accumulation of a lot of research tricks that like we kind of knew about but hadn't implemented or just hadn't tried in the particular way that we did.
I think we are definitely like the accumulation of years of research rather than like some kind of fundamental like we noticed something that no one else did.
We just brought to bear like a lot of techniques all at once, kind of very analogously to how ZK stuff has grown in cryptography.
Like years of research from smart people eventually makes some problems feasible.
So yeah, in particular, what we really did, what we really focused on was making queries smaller.
So a big problem with most previous schemes that were efficient on the server side was that then the queries were like hundreds of megabytes.
So we found ways to exploit the fact that, you know, with fully homomorphic encryption, you can compute any function on encrypted data.
So we kind of, we encrypt a function that expands the query.
So we can send a very small query and then the server can do work to expand it into a vector.

Speaker 4: 01:29:00

That's pretty cool.
Yeah, okay,

Speaker 0: 01:29:03

And then somewhat related, but like, how does peer review work for such a paper?
Because it seems to me it's not a new cryptography, just as you say, applying old concepts, but how was the peer review

Speaker 1: 01:29:14

process?
So it's a good question.
I remember my advisor was like, yeah, are we are we is this going to be kind of like publishable?
And we we actually after we had that conversation, we did come up with some new cryptography.
So we did end up kind of creating some some new techniques, kind of constructing a kind of variation or change to old schemes.
So we did end up publishing it and I presented it at Oakland, which is like the kind of top security conference for academics.
So I think we were in less of a, we were not in like a theoretical cryptography venue.
We were in like a privacy enhancing technologies kind of venue, but it was still, yeah.
I mean, it was a big deal for the reason you pointed out, which is it hasn't been practical.
And I think our work was kind of one of several works that took it from being impractical to practical.
There are now a couple, but at the time we were kind of one of the early ones that, yeah, I mean, when we told people, you know, you go to this site, and we could read Wikipedia, that was like a big deal, because I think everything else had been kind of speculative.
It was like, if you were looking up a sensitive medical condition in theory and if you wanted to you know there's a lot of like hypotheticals so yeah

Speaker 0: 01:30:39

yeah the MVP demos are pretty great

Speaker 1: 01:30:44

yeah if you have ideas for other ones let me know I I want to do Ethereum and I want to do, sorry, a password checker.

## Password Checker

Speaker 1: 01:30:54

So I know, I don't know if you guys have seen, have I been pwned, but they have like a site where you put in a password to see if it's been leaked but you know of course you're just giving them your password.
They do some hashing and stuff they say it's okay but you know you could do much better with PAR.
So I think DNS is also something we're interested in, although there are complications there, but yeah, DNS is also exciting.

Speaker 6: 01:31:24

Sorry, this is not about this topic, right?
But just curiosity, how do you see the, how, I don't know how to ask, homomorphic encryption?
How far do you think we are from fully, I mean, something that I, for example, can operate in a remote on data, on encrypted data in a remote, I don't know, for example, I save something in Google, in Google Drive,

Speaker 1: 01:32:06

for

Speaker 6: 01:32:06

example, right?
And I can, for example, I don't know, add information to that file, to that encrypted file.
Do you think we will see something like that?

Speaker 1: 01:32:21

It's a great question, honestly.
Yeah, it's a great question.
I think there's a lot of companies, there's a surprising number of companies trying to do this who will tell you like, yes.
I take a fairly pessimistic stance on this.
I think something companies are really excited about is encrypted machine learning.
What they really want to do is do machine learning on encrypted data, Which of course is kind of just like a way of using cryptography to violate your privacy instead of using it to, what they want to do is do like machine learning on your encrypted, on your end to end encrypted photos or your end to end encrypted, you know, messages.
So it's kind of like, almost like the evil version.
I think the good news is those are really impractical.
I think it's just like, people in the field know this, but encrypted machine learning is just like, you could do it if you want, but it's really expensive.
And it'll never be, it'll always be like 100 times more expensive than doing it the regular way.
So as the regular way gets more expensive, and people now want to do like DALI, and they want to do GPT-3, now paying a hundred times that cost is too hard.
We're just barely able to do private machine learning from like 2010.
So I'm not super optimistic on that front.
I think something that is really quite realistic that I'm really personally excited about, part of why I'm founding this company, is I would like to find a way to kind of raise money and fund the building of metadata private messaging services.
So, the thing I want to build is basically like WhatsApp or Signal, but they don't learn who you talk to.
So, that is something you can use homomorphic encryption for.
And then that is amazing, because obviously, who you talk to is really sensitive.
And if we could hide that data, even more than what you say, but also who you who you talk to, that would be really cool.
So so that's, that's, that's something I see as as really realistic.
And we have to do this foundational work of making PIR practical first.
But once we do that, I think building a messenger, I hope I can in five years tell you, yeah, you can go and message people and the service will never learn who you talk to.

Speaker 0: 01:34:52

It's pretty sweet.
Just a fun fact.
But the Signal groups use the key to verified anonymous credential cryptography scheme that we use for our Wabi Sabi coin joins.
So it would be nice if we throw your homomorphic encryption on top and...

Speaker 1: 01:35:10

So what is that called?
It's a key, what is key?

Speaker 0: 01:35:14

Key verified anonymous credentials.

Speaker 1: 01:35:19

Okay.

Speaker 0: 01:35:20

This is for

Speaker 1: 01:35:21

context or for a setup

Speaker 0: 01:35:23

of the conversation?
We use it as basically eCash token for access rights.

Speaker 1: 01:35:29

Okay.

Speaker 0: 01:35:30

The token gets created during input registration and you can only register an output if you present such a token and it's anonymous e-cash so to say.
Very rough explanation.

Speaker 4: 01:35:43

Cool.
Are you familiar with the Chowmian blind signatures?

Speaker 1: 01:35:49

Chowmian blind signatures?
Yes.
I'm familiar with the name Chowmian, but no, I haven't heard of Chowmian blind signatures.
Blind signatures probably did a piece set about that, but I could not off the top of my head say what exactly it is.
It's for voting, right?
I think.

Speaker 4: 01:36:09

Yeah.
So key verified anonymous credentials are a generalization of the blind signatures.
In Wasabi, at 1.0, we used blind signatures.
In 2.0, we used key verified anonymous credentials.

Speaker 1: 01:36:27

Oh, so this is actually a homomorphism too.
It's actually, yeah, so if you want to think of it, if you want to think of it this way, I mean, you're exploiting, these signatures also exploit a homomorphism in RSA.
They're just, it's just a different homomorphism.
Yeah, so homomorphic encryption is a little bit of, if you want to think of it this way, you could think of it as a generalization of, it's also a generalization of pairings-based cryptography, if you've seen that before.
There's kind of like, that's a very specific homomorphism for ECC, but yeah.
Yeah, they're connected.

Speaker 0: 01:37:06

As far as I remember we do use peterson commitments or generally speaking homomorphic encryption for the amount of the value of these credentials.

Speaker 1: 01:37:15

Ah okay

Speaker 5: 01:37:17

yes

Speaker 1: 01:37:18

yeah so those are again yeah homomorphic right sorry go ahead.

Speaker 6: 01:37:22

Yes because we have to the server needs to verify that the operation that we realized with the amount are correct without knowing the amount itself.
So, yes.
But it's something I mean, I don't know what I don't know exactly how to define homomorphic encryption, right?

## Homomorphic Encryption

Speaker 6: 01:37:51

Because homomorphic encryption, like, in the concept, It's okay, but it sounds like something that is not still possible, right?
So homomorphic encryption, and the scope is this for most of the time.
It's something like what we do is basically we operate in a committed value and that value is basically a point in an elliptic curve and that's it.

Speaker 1: 01:38:36

It's funny, I think elliptic curves are way more complicated.
I'm always like, I think lattice-based cryptography and homomorphic stuff, which is lattice-based and, you know, was initially pioneered for post-quantum resistance and stuff.
I think it's way easier to understand than elliptic curves.
Because what is an elliptic curve, really?
I'm always very confused.
Not confused, but it's always very abstract for me.
Whereas lattices are just, you know, it's matrices and it's noise.
And I understand that a lot better.
It's like a lot easier for me.
So it's funny, you should you guys are, guys are real crypto people.
If you guys are just sitting around thinking about Henderson commitments and

Speaker 0: 01:39:21

homo.

Speaker 1: 01:39:24

I promise homomorphic encryption is is it's also is in some ways much easier to understand.
So yeah.

Speaker 6: 01:39:32

We are not cryptographers here.
I mean, we are.

Speaker 1: 01:39:36

We are.
Yes.
It looks like a duck and talks like a duck.
I don't know.
You guys are as much cryptographers as anyone, I think.

Speaker 0: 01:39:48

Self-taught cryptographers.
The most dangerous kind.

Speaker 6: 01:39:55

Oh, yes, yes.

Speaker 1: 01:39:56

It's true.
I suppose academic cryptographers are less dangerous.
You know, I think we mostly write papers and that's it.

Speaker 4: 01:40:05

So to be fair, we hired a cryptographer for this, so that's okay.
But he's not here.

Speaker 0: 01:40:18

Plus, we didn't roll over on crypto, but we're script kiddies and just copied it from an existing paper.
So should be

Speaker 1: 01:40:25

all right.
That's what a cryptographer would do, right?
That's that's exactly they would say, we're not going to roll around, we're going to get a library, right?
So you did the right thing.

Speaker 4: 01:40:34

We kind of did it all, right?
Like we wrote a lot of cryptography code.
Yep, did not use a library.
But Lucas, we didn't roll.
Lucas, would you say we rolled our own crypto or not?
Good question.

Speaker 6: 01:40:58

No, I mean, the crypto that we are using is just a very specific case of one more general case that is the one that describes the signal white paper for anonymous groups.
So they have a general case and we use only one specific case of that.
So we are not doing that.
Now the problem is in the implementation.
I mean, the code, someone has to write the code, right?
And that is where developers always make mistakes, huge mistakes.
But so, yes, we implemented that because there are no libraries for that.
There is no, it's not, I mean, it's so basically, let's say we implemented our own crypto library, right?
However, the good part is that in my case at least I made so many mistakes before that I think I learned by doing and by making mistakes and and also the code is extremely reviewed.
So I think we did it really, really well this time.

Speaker 0: 01:42:30

Samir, do you still have time?
Are we just boring you

Speaker 3: 01:42:33

at this

Speaker 1: 01:42:33

point?
I have about 10 or 15 more minutes if you guys want to keep chatting.

Speaker 0: 01:42:39

Cool.
Well, most important questions first.
Guys, what do you have for Samir for the next 15?

Speaker 4: 01:42:46

How about a big one?
All right, go ahead, Jumar.

Speaker 0: 01:42:55

You have to bring a big not now.

Speaker 3: 01:42:59

Sorry about that.
This is one question that I've been meaning to ask, is that given that the homomorphic encryption has addition and multiplication, as far as I know about abstract algebra, does that enable Turing-complete machines or computations?

Speaker 1: 01:43:22

Yep, yep, yeah.
That's what the, sometimes you see this abbreviated as fully homomorphic encryption, that's what the fully means.
So yeah, you can do arbitrary computation, encrypted.
Anything you can compute on regular data, it's possible to compute on encrypted data,

Speaker 3: 01:43:39

yeah.
I see.
So you can, In a hypothetical scenario, how does one implement, for example, say, in Boolean logic, they say the NAND gate is...
Yeah, yeah, absolutely.
How does that translate into homomorphic operations?

Speaker 1: 01:44:03

Yeah, so there are some homomorphic schemes that actually operate directly on the bit level.
So they actually implement a NAND gate in the scheme, basically.
In fact, the scheme basically just is a way to compute a homomorphic NAND gate and then everything else just goes from there.
Something to note, I guess, about the fully part of fully homomorphic encryption, something we kind of mentioned, but the homomorphic encryption that Spiral uses is bounded depth.
What that means is there's a certain depth of the computation of the circuit that you can compute, and then after that it doesn't work.
So that kind of bounded depth-ness is not fully homomorphic, right?
You can't do anything Turing complete in bounded depth.
So there is a kind of encryption, a homomorphic encryption that can do arbitrarily large and arbitrary computation.
So that is fully homomorphic.
And it exists.
We don't use that part of it because it's quite slow.
But it does exist.
It is possible.

Speaker 3: 01:45:15

I don't suppose you can make a mini computer out of a fully homomorphic interface.

Speaker 1: 01:45:22

No, you absolutely can.
In fact, people are working on it for roll-ups and stuff.
Yeah, it's possible.

Speaker 3: 01:45:30

If I may ask Fabricio, is that implementable in lookup tables and FPGAs and stuff?
Yeah, it's

Speaker 1: 01:45:40

not that amenable to hardware acceleration.

Speaker 7: 01:45:44

You preceded me with the question I was going to ask.
If the implementation on FBAs or ASICs could constitute a significant improvement.

Speaker 0: 01:45:58

It's a

Speaker 1: 01:45:58

great question.
So we've actually tried GPUs and GPUs are really well suited for this.
NVIDIA actually has like an instruction set extension and a library that they put out that helps you do this.
So It's not, I think they might have, yeah, I don't know what the status of it is, but they are thinking about this.
ASICs and FPGAs are kind of not very useful because you need, what you need is, you need a fairly significant amount of memory because the database needs to fit in memory.
And GPUs have a lot of effort invested in really, really good memory access, right?
So, actually, GPUs are kind of optimal.
We tried it.
At the time, GPUs were really expensive.
So, we actually, it didn't become cost effective.
It was it was cool.
And it was it was fast, but it wasn't very cost effective.
Now, now that GPUs are way cheaper, it might be.
I have to have to like revisit it.
But yeah.
Yeah.

Speaker 0: 01:47:05

I show you a question because you just said the database has to be kept in memory.
Like, is that the case in Spiral?

Speaker 1: 01:47:11

Yes.

Speaker 0: 01:47:12

Oh, okay.
But then, I mean, if we have a large data data set, for example, the full blockchain, you know, many hundreds of gigabytes.
Right.
All of that needs to be in memory?

Speaker 1: 01:47:23

Yeah, yeah, it does.
I will say the memory cost usually kind of pales in terms of in comparison to the compute cost.
So I mean, making everything fit in memory is, I mean, hundreds of gigs of memory is, like, on a cloud provider, not that expensive, actually.
And once you have everything fitting in memory, you can throw as many compute cores as you want at it.
So it's a limit, but it's not crazy.

Speaker 3: 01:47:55

Out of topic question for Fabricio.
I've been quite interested in FPGA development.
What's this?
Have you looked into the open source hardware's beta log synthesis stuff like Ice Storm or something?
Ah, sorry, project starts with that.
I forgot.

Speaker 7: 01:48:23

But actually, these are crypto project guarding FPGA, because actually I'm dealing with FPGA for actually for genomic recognition.
But actually regarding crypto, I actually I didn't look yet, let's say.
But actually if you, let's say regarding, for example, the primitive function

Speaker 3: 01:48:58

to, for example,

Speaker 7: 01:49:01

do hashing stuff or cryptographic primitives, I think you can improve probably one order of magnitude if you implement some cryptographic computation and hashing on FPGAs. This is something that I think is worth looking at, definitely.

Speaker 3: 01:49:28

Cool.
Last question for you.
Has it been feasible, given that is it been in FPGAs, you are bound with a manufacturer's tooling?
And lately, there has been some developments regarding open source tooling for like uses and stuff.
Have you used those tools before or is it still vendor locked?

Speaker 7: 01:50:03

Well at the moment we we are using proper proprietary tools, for example Vivado, which is very famous, but actually, no, actually didn't yet look at the say open source opportune source development regarding that I will have a look

Speaker 3: 01:50:33

so much thank you so much

Speaker 0: 01:50:37

well Samir, thank you very much for coming here.
That was really kind of you.

Speaker 1: 01:50:43

Yeah, thanks so much for...
I learned so much.
I'm learning so much about what Bitcoin people want, the need and stuff.
You guys are super helpful.
So thank you so much.
I want to, the only thing I want to say is, you know, let's keep in touch, especially as we get closer to building something that looks less like just a balance checker and more like a private block explorer, I would love to see if there's kind of a synergy between what we offer.
I would love to see if people who use Wasabi Wallet also wanna use a private block Explorer.
So yeah, if that sounds good, I would love to keep in touch.

Speaker 0: 01:51:21

Yeah, definitely.
I mean, especially if you run the server and we don't have to, and we can use it for small niche things, like finding out the amount of the input of a payment transaction so that we can pre-bump it.
These types of small things where it doesn't really make sense for us to make huge infrastructure changes for those very, very niche case things.

Speaker 1: 01:51:46

No, we'd love to.
We'd love to mostly, we'd love to see people use the server.
We'd love to see like what your pain points are.
We're absolutely happy to host and run those kinds of things.
So yeah, absolutely.

Speaker 0: 01:51:59

Pretty sweet.
And I'm really curious what we can come up with to use this other than just blockchain sync and wallet balance sync.

Speaker 1: 01:52:08

Yeah.

Speaker 0: 01:52:10

Pretty cool.

Speaker 6: 01:52:12

Yeah, sorry, just one comment.
You know, it's not obvious what we can do with this technology.
I don't know if everybody understands.
In fact, I think the white paper is not a good starting point for, in fact, it is the, you know, So, sometimes you need to know the tools that you have available.
So, when you say, okay, we can fix the, oh, there is this technology that we can use, and this is exactly for this.
So if you have documentation or presentations or examples or snippets or whatever or use cases, right?
That's also cool.
I'm pretty interested in this stuff.

Speaker 1: 01:53:05

I will definitely send you guys that stuff.
You're totally right.
You have to kind of know what the tool is before you can really see where it makes sense to use.
Absolutely.

Speaker 6: 01:53:17

Okay.
Thank you guys.

Speaker 0: 01:53:20

Yeah, then I guess that's it for the recorded part of this week's Wasabi Research Club.
Thanks for all the guests joining us here and all the viewers online.
Hopefully this was as exciting and useful for you guys as it was for me.
Again, thanks Samir for coming here.
Real pleasure, real honor.
Let's stay in touch.

Speaker 1: 01:53:40

Yeah, absolutely.
Thank you so much.

Speaker 0: 01:53:43

See you on the next show.
Bye-bye.

Speaker 1: 01:53:44

Yeah, See you.
Bye.

---
title: "Exploring P2P Hashrate Markets V2"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=IvfmfcAX9wU
tags: ['mining']
speakers: ['Nico Preti']
categories: ['conference']
date: 2023-07-25
---
Hi everybody, I'm Nico.
I work, I'm one of the co-founders at Wrigley, and we are a peer-to-peer hashrate market.
The way this talk is kind of broken up is the first part we're going to go through a little bit how hash rate, what is hash rate, how the protocol for mining works across the network, and then a little bit on how hash rate markets have come around, and then finally how we can potentially do hash rate with root layer two, which is obviously given the kind of subject matter of the conference, apropos.
Okay, so hash rate.
What is hash rate?
Well, it's the output of a hash function, right?
A hash function you have a pre-image that gets passed into through a function that outputs an image, right?
So, if you've ever looked at a Bitcoin block explorer, you'll see at the bottom that you'll have these blocks that the hash here in hex has a bunch of zeros in front of it.
So that is a result of what Adam Mac did with HashCash.
So we base Bitcoin's hash rate is all based on the hash-cache algorithm.
And kind of a quick math here on how this works is that, see over here, we have zero to the power of K.
The output or the image here on the right, it's supposed to start with a certain amount of zeros, right?
And that zero to the power of K is basically the difficulty of how many zeros this hash will start with.
So if we do this algebraically, you have the function which is the hash of X, takes the input X, and is supposed to output a zero or a string of zeros.
The kind of proper expression for this function would be that you have a hash with a service string and a counter.
The counter gets incremented.
And the service string is what gives the hash actual purpose, right?
Because otherwise you're just hashing through a bunch of things, you can prove that, okay, this was the number that went into giving this hash, but it doesn't have any actual utility.
So the service string is the utility in the case of Bitcoin blocks.
That service string is going to be all the transactions that we're actually trying to put into the network, which is consolidated into the block header.
So hash pass was SHA-1, which I think was 160 bits.
Usually the standard for that was, I think K was 20.
That gave you about a million tries to be able to find a correct pre-image.
Bitcoin uses 256 bits, So it's much larger, a lot more tries.
And yeah, we have a, one of the main differences between HashCash and Bitcoin is that you can only, HashCash is 2 to the power of K.
For that difficulty, which means you can either only double or half the difficulty in any one period.
Whereas with Bitcoin we need to be much more granular with how we adjust difficulty every 2016 blocks.
So instead of that, We turn the integer K into a floating point, so we can be a lot more precise with how we change difficulty.
So yeah, every 2016 blocks, we have this difficulty adjustment that comes in, and what ends up getting changed there is that floating point, right?
It's like, what are we trying to do?
And the kind of full expression there of what the map looks like is you have S as your service string, X is your random starting point, which for most miners ends up actually being the coinbase transaction that then you compute into the Merkle root.
We'll go into that in a second.
But that's kind of your random starting point because every miner is changing the coinbase transaction, right?
And then you have, instead of it equaling zero, we're going for less than a certain difficulty target.
Target equals to the power of MIT, and That gets all put over one usually.
But yeah, so this is a little bit of a kind of math behind how this works.
Cool, so in Bitcoin, we take block headers and that is what we're hashing, right?
As a miner, You just give me the block header and I'm going to start hashing on it.
What goes into the block header?
This is actually pretty important.
Usually people look into this when you first read about Bitcoin, but then they kind of forget about it.
It goes to the back of your mind and you don't really ever remember what's actually going into these blocks.
And it's kind of important, right?
So we have like the version, what's the version of the software that you're running, the hash of the previous block, right?
That's what actually creates the blockchain, right?
We're chaining the blocks together, so we need the previous block hash.
You have the Merkle root, which is what I was just describing, all the transactions that get hashed together in the form of a tree.
The current block, like timestamp, right, that gets updated every few seconds, So that actually is another bit of entropy that gets added into the equation there.
You have bits, which is just the target that's in hex usually.
And finally the knots, that's the counter.
The knots field is actually really, really small.
So there's 32 bits, you run through them with miners nowadays really quickly, right?
So that's where you have to go to what we call the extranauts field, which sits in the Coinbase.
And that gets calculated as part of the Merkle group.
Okay, so what actually ends up changing there in the block header is the Merkle group.
Cool, so if you guys didn't know, we usually measure any one miner today, you measure in tera hashes, right?
So we're talking about a trillion there.
Then if we're talking about a group of miners usually, so a mining farm, you measure in peta hashes.
And then finally, when we're talking about network hash rate, we're talking about Exa hashes.
So right now I think we're around 350 Exa hashes on the network.
Your standard miner today runs about 100 Tera hashes per second, and your average mining farm will be something like 10 Peta hashes.
Cool.
So the mining protocol.
So this was kind of how actual hash rate or hashing works, but then how do we organize that over the network?
It's a little bit more involved.
So right now we use Stratum V1.
You guys I'm sure have heard about Stratum V2, which is a very hot topic at the moment.
It's a little bit beyond the scope of this talk.
I'll go and I'll kind of add a few bits here and there that'll tell you what the main difference is in a couple slides, but just know that right now we're talking about strategy one.
And mining and mining pools really are just TCP connections, right?
So we open a TCP port with a pool that a miner communicates with, and that communication is JSON RPC, right?
So it's really straightforward.
The messages are literally these that we see here.
So mining.subscribe, authorize, set target, notify, and submit.
That's pretty much everything that there is to the Stratum protocol.
It's really simple.
Here you see a little bit I gave some background of what's happening.
So subscribe is the first thing that happens.
It's like the miner says, hey, I'm here, I'm ready to start mining, please register me with your pool and give me a job ID.
And it also starts to send over the extranauts info.
So this is the really important part of Strato, That was actually an innovation back when they first started Stravins here in 2013, 2014.
One of the guys who wrote Stravins here.
But in any case, the extranauts information, that's where we're able to localize most of the work that a miner needs to do with the actual miner rather than having to go back and forth with the pool.
That would have a lot more overhead if every time you need to iterate through proof of work, you had to be talking, you had to be getting that information from the pool.
So the pool sends over some extra non-sync that says, hey, start with this and then iterate on it.
And that basically is what you're sending over right at the beginning with subscribe.
The other thing that happens is with authorization, you're basically getting your worker.
So you can have an individual pool account, but you can have many workers, which usually corresponds to multiple different machines.
And when you're authorizing a given worker, you're basically saying, hey, I have this worker who's ready to receive jobs.
So that's happening from the client to the server, so here if we're thinking client, we're thinking the actual mining machine, to the pool, and then the pool is going to send back the shared difficulty target.
So we have, In mining pools, we organize work according to shares, which sits below the difficulty of what the network requires for a new block to be found.
That difficulty is basically adjusted per machine such that the pool gets a share every two to five seconds.
So the pool is basically telling the miner, hey, how much hash rate do you have?
Okay, you have about this much, so give me, I'm going to make the difficulty, you know, whatever, one or two, such that I can get information from you between two and five seconds.
So it adjusts, right?
Does that make sense?
Yeah, okay.
So that's what's happening here.
Once the miner knows what difficulty it needs to be mining at, it then needs to get the information to actually produce hashes, right?
And that information is what we just went over before.
Which is basically this information.
What's in the block header that I need to put together.
And the main thing that the miner is going to individually be working on is this extra knots field.
So the main bits that it gets, like I said in the subscription, is you get extra knots one and two.
One is kind of a fixed variable, but then what needs to get iterated on by that specific miner is the length of that extra dots field.
And then it has basically the beginning of the coinbase, which is just the address for where the mining pool payout needs to go, and the end of the point base, which is basically just extra information I've added.
Meijer will iterate through this extra-nonce-2 field until it finds a target hash, or an output hash just below the target difficulty for that share.
It does that by concatenating basically all these fields, hashing it together, and then we go and we create the Merkle root.
So if In every block, the Coinbase transaction is always the leftmost leaf over here.
So in order to calculate the Merkle root, this is the difference between strategy one and strategy two basically.
In v1, you're not getting the full tree.
You're only getting the branch, the branches that you need to get this root.
So if this is the coinbase and what you're iterating on is only this transaction that you get, they give you this transaction, they give you this transaction to get here, and then They give you this transaction to get here, and then they give you this transaction to get here, this hash, not transactions, to get over here, and then this one to create the root.
So you can go all the way up and create the Merkle root that is obviously the most important problem component of your service string.
Cool.
So, once you have a Merkle root, you're basically iterating through time.
You can add the rest of the components together.
You hash that all together, and that's what goes to your mining software to get pushed out to the pool, right?
And try and get paid for these shares, or try and submit shares that are under the target.
Cool, so mining pools.
I'm not gonna go through this entire graph, But this is in essence how a mining pool is put together, and this will be on Revlit, so if you guys do want to refer to it, you can.
Did you name that Kafka, or is that actually the name of some protocol?
Oh, that's the name of, yeah, it's like a piece of software.
No, I didn't name it.
Some mining pools use Kafka, some others, it's arbitrary.
But the essence of a mining pool is that you have a node that's connected to the network, it's scraping for those transactions, those transactions get put together then into a block, and that, well, It gets put together into the branches of the Merkle tree that we just described that then gets fed into a job Through the stratum server to the miners, right?
And then the miners work on that until they have they find a valid share And then hopefully one of those shares will be below, or one of those hashes will be below the network's difficulty, right?
And then that's what gets pushed back to the nodes and gossip throughout the network.
Payouts.
So we have, there's a lot of different payout mechanisms for pools.
The two main ones that are used are PPL and S, which is pay per last number of shares, and FPBS, which is full pay per share.
The basic difference is that in PPL&S, which for example is what Brains uses, or formerly the Slush Pool, You're paid when the pool finds a block.
So whenever the pool finds a block, there is a last number of shares that were issued prior to finding that block that then goes to the miners based on the work that they contributed for finding that specific block.
Part of the reason for how they do the last number of shares is to avoid switching between different pools, so that you only are rewarded if you are mining on the block within that time period when the block was found.
At PPS, you're guaranteed, basically, if the mining pool doesn't run out of money, to get paid per share.
So for whatever amount of shares you produce in that day, you will be paid out of their liquidity pool for the shares that you produce or you contribute to the pool that day.
So it's independently of whether that pool finds blocks or not.
So that obviously begs the question, well, what happens if the mining pool doesn't find any blocks in the day, or over two days, or three days, or what have you, then how do you pay out of the FPPS pool?
Well, that is basically the risk of running an FPPS pool, is that you could potentially be having to pay out your miners, but not be bringing in enough Bitcoin to issue those payments.
Whereas in PPL&S, you basically push that risk onto the miner.
So you could be going days where the pool doesn't find any blocks, but the pool is only paying when they find blocks.
So the pool itself doesn't actually take on that risk.
Instead, the miners have to take on the risk of potentially not getting paid for multiple days.
Has there been any cases of a mining pool running out?
Oh yeah.
That's what happens in that case.
They get bought out by a bigger mining pool.
Or a financier comes in and basically takes over to pay the IOUs. So at Poolin, for example, They were commingling some of their mining pool funds with some of some DeFi investments they had made.
So when 3Eros Capital went down, a lot of their funds for the pool were actually tied with that with that with those DeFi protocols.
And all of a sudden, everybody, all the miners around Poland got Bitcoin IOUs, is what it said on the mining pool site.
So instead of you saying, oh, let me get my Bitcoin out, It's like, no, no, you have a Bitcoin, I have you.
Right, so that's a typical example.
I used to work at pool, so no hate there.
Cool.
So kind of the meat of the talk now, what are these mining markets?
Because if we have pools, and pools are in essence a kind of marketplace because you have hash rate that's considered being sold to the pool because the pool is then turning around and mining big one with it and getting percentage off that and then distributing those funds to all these miners, and in essence that acts like a form of market, but what if we could try and take it one step further?
So, the idea was originally, this is from the white paper, that proof of work is essentially one CPU, one vote.
Satoshi had originally had that idea.
Well, long gone are the days where you can mine with a CPU.
We went from CPUs to GPUs very quickly, then to FPGAs pretty much at the exact same time.
And finally, for ASICs, I think started rolling around, coming out 12, 13, around there.
And from then on, you really need to buy pretty sophisticated hardware that was not inexpensive, right?
You couldn't just be running this with like your hardware at home.
After a few years, even if you did buy that hardware, You needed to find really cheap electricity to run that hardware on.
So even if you had that ASIC sitting at home, you weren't going to be making much money on your Bitcoin.
And it wasn't really feasible to do it or sustainable to do it in the long run.
And nowadays we're at the point where even If you have really cheap electricity, you really need to have scale and a lot of infrastructure to drive down your operating costs.
So it's really tough to mine nowadays.
And even for these big miners, it's really hard.
Obviously, this has a pretty strong tendency towards centralization for mining, which we've seen on Twitter and I guess on Bitcoin social layer a lot of pushback right because you have no mining pools like Foundry and between Bitmain and Foundry you have easily 70-80% of the network.
Those are two actors, right?
And sure, you can switch out of pools and it's like not necessarily, it doesn't necessarily have to be an existential threat to Bitcoin, but it would be nice if we can try and distribute that risk somehow, right?
And my risk here, a lot of it is really the capital risk.
So in order to run mining operations nowadays and to have this scale, you really need to tap some serious amounts of cash.
If you look at the balance sheets of any of these large public miners, they're huge, just really big purchases for machines and investments that are involved in these kinds of projects.
It inevitably leads to a lot of lending, which is in this kind of market very predatory because nobody wants to lend to Bitcoin, as it's so risky.
So you end up having very high interest rates.
Or you have kind of new loan kind of scenarios using something like ASIC-backed loans where people like Knighted, for example, that after the company goes bankrupt, they end up having all these ASICs that they don't have anywhere to put because the company went bankrupt.
This happened last year a lot.
I'm sure you guys heard the news.
And basically there's no good way for miners to hedge on any of this risk.
So there's no real like liquid markets where a miner can try and lock in their revenue, which they shouldn't be making over the course of whatever, six months, a year, two, three years, given whatever miner they're running, and their logistic price, and say, hey, I know Bitcoin's price is going to do something, and I know that difficulty will probably go up and hash price will go down.
So let me just like lock in a price on a depreciating curve, let's say two, 3% per month or 1% difficulty adjustment, whatever you wanna call it.
And I'll just like lock that in, right?
That doesn't really exist for every other major commodity in the world that exists.
So we can't do that with Bitcoin, right?
And as a miner, it's, especially when we're dealing with this kind of capital structure, it's very heavy capital structure we have to manage, it's really debilitating, and it makes it a very difficult business to actually be successful.
So, part of the way we've been thinking about this is, well, I think we're actually just looking for liquidity in the wrong place, but we're looking for to diversify that risk in the wrong place.
Why are we going to all these traditional financial institutions that are really just trying to get as much as they can to get these loans, and why don't we just actually go to the people that have capital sitting around, by capital I mean Bitcoin, that sits there, and they're very interested in obviously the security of the network, and they're interested in distribution of that security of the network.
So why don't we leverage all that latent capital for distributing this kind of security risk, right, or the security of the structure.
So you can kind of think of hosting and cloud mining as maybe an attempt at doing that, not really, but we can like try and say that that was maybe, you know, in the most charitable sense what they're doing.
For those that don't know, hosting is when you buy a rig and somebody basically has it at their facility for you and they run it, they give you the payouts for it or they point that hash rate to your mining pool.
Cloud mining is basically where you can buy a hash rate contract for a given amount of time.
Usually it's not with actual delivery of the hash rate as far as I know.
I have heard that there are some instances where that happens.
But basically the difference is just that with cloud mining you don't buy the actual machine, you just buy some supposed contract to mine.
But often it's very abstracted away from you.
So, the main problem with this is that it's really not, like, it doesn't adopt any of the principles that we use in Bitcoin, right?
So you have a totally asymmetric trust model.
You have to trust that the person is, you have to fork up a bunch of cash first to buy this, to buy this miner to whatever service provider that may be.
You have to trust that that person isn't going to be price gouging on the price of the miner because they take care of that.
You have to trust that the facility operator is going to stay up and you have to trust that ultimately when the price rips or something's happening that you're still going to be receiving your hash back.
You have no recourse, right?
This could be in some random other country that like God knows where your mining is.
So oftentimes, this leads to ruckus.
It's just either scams or straight rug pulls.
And cloud mining, you're getting price gouged almost always.
I've never seen a cloud mining contract where you make any money.
On the contrary, you're usually losing quite a bit.
And hosting is really, like I'm saying, not only do you have this asymmetric trust where each person here can rug you, but you also just have premiums, right, that get put in at every level there.
So a good way we can try and avoid this is just go straight between the miner and the buyer, right?
Just kind of try and create a market where you have the two that are talking to each other directly.
Before getting there.
So we've had some hash rate futures markets.
FTX had launched one last year.
Luxor has something which is a little bit more legit, which is a non-deliverable future.
So it's a swap, basically.
It's a lot more traditional.
The problem with these is that we haven't seen much liquidity, right?
And again, this kind of goes back to, I think, what I had mentioned before, is that why are we going to these traditional financial institutions looking for money when they're the ones that like, usually, one, they don't understand Bitcoin, they have no real incentive to understand or try and take that risk on Bitcoin outside of the fact that they're gonna try and be relatively predatory on the fact that, oh, you need the money and no one else is gonna give you the money, so I'm gonna give it to you for like really expensively.
And yeah, it creates this situation, right, where nobody's really out trying to buy these future hash rate contracts in the traditional financial markets.
Other considerations are, well, what if you want to actually take delivery?
There's nothing really like that.
What about the duration of this contract?
So for the most part, if you look at marketplaces like NiceHash and Mining Regret tools, you have pretty short contract durations there, which makes it okay if you're kind of trying to do the betting in one direction or another, but it's fairly short, right?
So you're not really buying something and then just kind of letting it sit there and do its thing.
And then in terms of the actual non-deliverables or like the swaps, like contracts, well, it's, you know, you're buying kind of like a traditional financial instrument and it's not code.
Oh, wow, okay.
That was fast.
Well, I'm gonna run through this really quick.
Thank you.
So our model is where you go, we have auctions set up in order to have price discovery.
We have multi-sig where the payment to the seller of the hash rate, or the miner, only occurs after the hash rate's been delivered, and we deliver the hash rate through a proxy.
So we're able to see exactly how much hash rate ends up getting delivered.
So Here we have a little model of how this works.
So we create this little agreement here in the middle.
The agreement, the purchase part here in orange at the bottom is held on chain in multisig.
The delivery for The terms of delivery are held through the pool account.
So the hash rate gets pointed here from the miner to a pool where eventually a coinbase hits the pool and the payout goes to a mining pool account, right?
And that's where this part of the agreement comes into play.
And finally, you can actually obviously remove your funds from your account model to the next model, right?
So you have your hot dog shape.
And the way in which we actually are able to ensure that that delivery is happening is that we have a proxy that we can read that the hash rate is getting delivered to that pool account.
So we have a demo running right now, which you can sign up using this QR code, which I'll give another link to in a second.
This is the basic flow of what's happening with our model, but basically we have an event-driven system where as soon as you make a payment to us, we'll switch a hash rate that is currently pointed elsewhere on our proxy straight to your guys' pool account, the pool account that you have registered with us and our database.
Last notes on lightning, we want to be able to bring mining pool payouts over lightning.
The issue with that is that, I mean this is, I don't know if you guys saw the Jade, basically it produces hashes.
And the idea here is like, okay, well, we have 10 sats per terahash per second per hour.
How would you be able to stream that over lightning?
Would that be possible?
Could we use every spare or wasted jewel and convert that into hashes or gigahashes or whatever it may be?
Well, as things stand right now, no, you definitely couldn't.
Over lightning, well, maybe.
Lightning allows us to do that.
The problem is, as Lisa calls it, we have terabat liquidity issues with mining pool payouts to miners over lightning, Because we're only pushing liquidity in one direction.
You're going to exhaust those channel capacities immediately.
And that just isn't how lightning works.
We need to have payment flows in two directions.
Now with our model, We do have liquidity that's going in both directions, right?
We have the payment for the hash rate that gets basically pushed all at once in one direction, and then you have per day hash rate delivery that's occurring in the other direction.
So we can try and balance those channels out.
The question here becomes where does the pool sit and how do you actually include new Coinbase transactions?
So this could be a situation where hopefully maybe splicing could come into play and you could actually splice in new UTXOs into existing channel balances.
And then what actually ends up getting closed at the end is that marginal difference on what the contract, like the terms were, right?
So if you, let's say as the buyer, wanted to make X percent of margin on that bet that you took, will that channel close and end up reflecting basically whether you were on the right side of the bet or the miner was on the right side of the bet on that futures curve, right?
Finally another potentially easier way of doing this rather than going straight over Lightning, is to use a pedicool.
So, I'll leave it there.
Yeah, we'd love to include, basically, the hash rate marking over Nostr.
We think that'd be, it's really fertile ground to try and use static IDs to issue payouts.
So, yeah.
You guys wanna try out the demo, that's QR code.
And we'll see you all there.
Woo!

---
title: R&D Goals & Challenges
transcript_by: Bryan Bishop
tags:
  - research
  - bitcoin-core
speakers:
  - Patrick Murck
  - Gavin Andresen
  - Cory Fields
aliases:
  - /bitcoin-core-dev-tech/bitcoin-devcore-2015/research-and-development-goals/
---
We often see people saying they are testing the waters, they fixed a typo, they made a tiny little fix that doesn't impact much, they are getting used to the process. They are finding that it's really easy to contribut to Bitcoin Core. You code your changes, you submit your changes, there's not much to it.

There's a difference, and the lines are fuzzy and undefined, and you can make a change to Core that changes a spelling error or a change to policy or consensus rules, for those high-level things, for ecosystem-level things, there's several mailing lists, the dev list gets the most traffic. Things get debated there, they get debated on the social media. So it boils down to what changes you are after, so whether you're adding functionality to the program itself it's easy to do that as long as it's not controversial.

Touching on what Gavin said, we are working on making things much more modular. We have confusion about the fact that we have pull requests for the pipeline as well as policy changes all in the same pipeline, as things like the wallet or things like the miner start to become broken out, we don't have to worry about thos ethings, we have just the more core central big fun changes. It's a way to weed out some of the noise. That's one of the things I'm currently working towards. As far as contributing, I would say it's actually we have a very low barrier for entry for anyone who actually has some functional changes that they want to make.

That's great. So again we want to make this more of an open conservation so that I don't have to monopolize Cory and Gavin's time. More importantly, let's open the floor up for questions.

Q: Gavin I think you said that the wallet could be greatly improved or broken out as a requirement before version 1.0, and it would be the community's call or something. Do you consider it that the wallet has to go into a separate repository before a Bitcoin Core could get to a 1.0 stamp of approval? Could it be improved in a way, plausible to release the whole thing as a 1.0?

A: I call Bitcoin Core a reference implementation. A good way to do a wallet to do it is nice. Right now the wallet is not a good reference implementation. It doesn't use HD keys, and it ought to. To make it do that is basically a rewrite. It still uses BerkeleyDB, which we don't like for lots of reasons. We would prefer a different way to store keys in the wallet. It should interact with hardware key storage in some way. It doesn't at all right now. If I was thinking about what wallet would be a good reference implementation wallet, if we had that I think it would be fine if it was part of Bitcoin Core, and we don't have that right now.

Q: But you want to modularize it?

A: You can compile Bitcoin Core without the wallet at all. I don't care whehter it's a separate repository or not. If we ship a Bitcoin Core 1.0 with wallet code, it should be something we could point at and say it's best practice.

I saw another hand, who's the next victim?

Q: Who would you expect to run a full validating node? Your average consumer, businesses, who would you expect to do that?

A: Um. Satoshi actually wrote about this. There's another part of the quote where he imagines that only people with machines in datacenters would be running nodes in the future, and everyone would be simplified payment verification nodes. I think many people don't like the idea of you having to rent a server in a data center to handle Bitcoin transaction volume. While I personally would be okay with that, expecting someone to pay $100 or $200 a year, I think I am in the minority here. I think people find it important to run full nodes on their home computers. We have fast network connections today typically, and we have fast computers at home is okay. I think that going forward we can scale up with you know the transaction volume that we're going to get running my phrase is kind of the the the the geeky hobbiest, so somebody with a pretty fast computer and a pretty good internet connection should continue to be able to run a full node at home. Geeks like us who do have pretty darn good personal computers and pretty good internet connections can continue to participate as a full node. I don't know. If there was a ground swell "no, we need to scale it way faster than that", well fine I would actually prefer that. I don't see being able to get consensus that you have to rent a server to participate as a full node.

Cory: I would agree for the most part with that. I think for the forseeable future I think that any powerful user should be able to run a full node. It may not do the network any good.

Gavin: We do get people that complain about not being able to run a full node on their raspberry pi. Well, okay. Why would you want to? And what good would it do for anyone?

Cory: If it gets to the point where a person with reasonable bandwidth and horsepower can no longer run a full node, I think that's something that should be looked into. I think that will happen organically, and I don't see much need to worry about the requirements as they grow.

Q: Do you have any thoughts on the mining centralization? Possible ways, is there a future where the average Joe Schmoe can spin up a miner? I know you mentioned proof of stake in your other presentation that it wasn't a good way to secure the blockchain. Is there a hybrid version that could be feasible?

Gavin: Um. Um. That's a whole different talk. How to arrange my thoughts.. I'll first start by saying something that I've said for a long time that nobody believes. I think that mining centralization will ebb and flow. Like we just saw. Huge concentration of mining power in the hands of a small number of people. I think I read on reddit that there's some group working on high temperature computing where you cna run your chips at 250 degrees Celsius which is enough to boil water. If you can boil water and create Bitcoin at the same times, that becomes really interesting and driving turbines and steam heat and so on. That could be a huge decentralizing force because you don't want all that heat in a factory in China. So you can imagine a future where apartment buildings all over the world are Bitcoin mining and heating themselves basically for free. I tweeted that I want a Bitcoin mining electric blanket to keep me warm at night. producing heat, why not produce some Bitcoin at the same time. I think it is hard for people to think about this, when they see 40% of mining power owned by GHash.io or whatever. I think those decentralization forces will eventually take hold. I think there are other forces that will decentralize mining. The fact that transactions are created all over the world, it's a global phenomena, just that, early access to transactions into blocks could be a decentralizing factor so that we don't have one country or one hemisphere that monopolizes mining.

Gavin: Another thing that I have been thinking about recently is that we are over secure with mining. I think there is a possible future. Mining has two reasons. One is the initial introduction of coins, it's a fair way of distributing Bitcoin. Do some work in the form of mining, get coins. My fundamental problem with proof of stake is that they don't have a solution for introducing coins fairly. They premine and then sell them, then they handwave the SEC issues. Why do you get to decide who gets your coins? There's all sorts of legal reasons too. So the initial distribution of coins is important. Can you do proof of work to distribute, and then use proof of stake? You probably could. You could use something else to secure. Maybe proof of stake would make sense because then you have that proof of work anchor. Although.. there's all sorts of theoretical issues with you know, if it becomes costless to rewrite the blockchain, or very low cost then you run into problems. But if you are trying to secure against double spending, there are probably ways to secure against double spending without decentralization. Perhaps we will have no mining, but we will have a secure blockchain to secure against double spending. I think I may be writing a blog post soon about 51% attacks and ohw we should be more specific when we talk about 51% attacs. There's security against double spending, and then security against block censorship. That's sort of what you can do in a 51% attack... you can double spend or you can prevent certain transactions from appearing. Securing against double spending, we don't need a whole lot of mining for that, securing against censorship you probably do need a fairly large amount of potential mining on the sidelines ready to go if someone is trying to censor blocks. I hope this wasn't too long winded.

Q: So there's... there's a battle of sorts between how coins are distributed. You have some die-hards who say cold storage all the way, my key nobody should ever touch it, and then you have services holding private keys, and then you have multisig which is sort of a hybrid inbetween. Do you think that all three of these models have their place? Is one a really bad direction?

A: It's all a security convenience trade-off. I think that some company is going to figure out where the sweet spot is. I think corporations will have a very different model for how they secure their coins than how individuals do. I don't think it will be either or. I think it will be all of the above.

Cory: I think practices will evolve and models will evolve. Different companies and different use-cases will use the safest with real-world usability. It doesn't really matter from a technical perspective, the most perfect will be usable.

Gavin: I think we will get to the point where we have a multisig hot wallet with millions of dollars and it will be someone in the cloud signing off on transactions. Maybe if you have a billion dollars of BTC then you should use cold storage vaults in Switzerland or somewhere else where you're worried about nuclear war wiping out your BTC, I think the trend will be increased security and the amount of money you store in a hot wallet... I used to tell people don't store more than you would store in your back wallet in your hot wallet. I think this will scale up as we get better at security.

I think you are seeing the democritization of bank-grade treasury control, whether you are a co-op running on $100/mo or you are a bank holding a trillion dollars. That's kind of cool. It's the same cost, or it will be down the road. I think that's part of it, democritization of treasury management which is cool.

Andy (Armory): I have question about inevitability of a hard fork, or what are the benefits and risks of that?

Gavin: I think we do need a hard fork to increase the block size. We have a one megabyte block size today. If you take the size of an average BTC transaction, it works out to under 3 transactions per second which is pathetic for a payment network. People have all sorts of ideas regarding not increasing the block size, and doing ome other complex thing to increase transactions. The engineer in me says do the simplest thing that can possibly work unless there's a compelling reason not to. Increasing the blocksize is really simple conceptually. I did some work testing much bigger blocks with our current code, our current code can handle bigger blocks with no problems. I have been thinking about 1 gigabyte blocks, could we theoretically handle that in the future, I think we can. I think there's a clear path from getting from here to there. There are some economic arguments over, I think most of the arguments, mos tof the problems that people have with economics of increasing the block size. They are looking at an infinite block size, with no limit. I think everything would be okay, but I am not going to propose that. I think that there are good reasons to not propose infinite block sizes. The blocks should be small enough so that people with reasonably fast connections and reasonable machines at home could participate at full nodes and then growing over time as technology scales. I think the one rational argument that makes some sense is the worry that it would increase mining centralization. Bigger blocks may cause miners to increase the costs and maybe that means that fewer miners are involved. I wish somebody would articulate that better so that I would understand it better. We have already experienced mining centralization, and I don't undestand how bigger blocks would facilitate that even more. So you need to find someone who argues the opposite. So whether I can get enough consensus to get a hard fork to happen, we'll see. I am going to be asking people to help. So if you have a business that you think needs more than 3 transactions per second on the blockchain, speak up, start lobbying, tell us that we need to scale. I think we would make a huge mistake at this point if we didn't do everything possible to smooth the path towards widespread adoption. I think there's a risk that otherwise Bitcoin will be overtaen or it will be squashed by governments that don't like it. There's only a million people in the US that like it, we will try to squash it because it's okay to make a million people unhappy. We have a much better position if 100 million people have used Bitcoin in the United States and liked it. It's hard for a government to squash something that is widely used and popular. I think we should do anything to get as many people as possible to use it. We need to make transactions as inexpensive as possible. We should do anything we can so that companies are successful for those who are trying to use the blockchain for interesting things.

Q: You used to be able to mine off your own CPU. So now you can't mine with anything except an ASIC. Part of the whole blockchain is that people are running nodes, and the reward is less and less, but you're spending more computing power to maintain the blockchain, and you're talking about bigger blocks, and it will take more processing speed? Or not? One more, and we keep talking about as Bitcoin as the currency... if we start building these other businesses on the protocol, like proof of contracts, identity, real estate, incredible infrastructure over all built on this blockchain, is that, is there parallel to people maintaining the node, solving these blocks if they are building structures on top of it? Wont you have CEX or one or two maintaining the blockchain because nobody will want to fry their computer with it?

Gavin: So the actual proof of work is actually independent of the number of transactions in the block. So miners try to find a hash of an 80 byte block header. So it doesn't matter how many transactions are there, they all get combined by the merkle root which is in the block header. Block size is independent of the ASIC/GPU migration. It's really irrelevant. Putting a block together, watching the netwokr for transactions and deciding which transactions to put in your block, that can be done on the raspberry pi right now, that's the level of CPU power you need to do that. I am proposing that we scale that up so that you would need a reasonable home computer to be able to do that. I don't think that's an unreasonable requirement for miners. I think that miners should buy a new Dell computer every year or two to attach to their network to process blocks. I think that's a perfectly reasonable expense. I think that scaling up to Visa's transaction volume would require a transaction volume, but if we scale to that in 10 or 15 years when our personal computers will be little data centers that can handle that transaction volume, sure. Does that make sense?

Q: At some point, most people are going to drop out of mining... in 6 or 7 years...

Gavin: I think some people will say that has already happened. I think we will see small people come back. I may be wrong. I can't predict the future. I do have a problem with people tying the block size issue with mining because I don't see the connection between blocks and mining.

Q: I was talking with a large miner this weekend. The miners are being hit hard right now because of the price. They are over-invested in equipment and all that stuff. He was thinking about a mining coalition to enforce transaction fees. Most of their income has been coinbase rewards. Do you think a 1% fee could have a serious impact on adoption or success of the network if miners start demanding transaction fees?

Gavin: I haven't heard of miners doing that.

Murck: I think that a coalition is usually not a good thing. The idea of decentralization is that you shouldn't have that.

Cory: Those things will come and go. It's a logical progression. What if you end up with two competing coalitions that vie for their rates?

Gavin: Small block low fee, large block high fee? I think competition will make transaction fees end up wherever they end up. I think that it will be interesting to see if they can form a coalition to produce small blocks with high fee transactions. Thta will be okay with me. Bitcoin is an experiment. This is a free market in fees. Last year I worked on floating transaction fees so that we don't have hardcoded fees, this will be in 0.10 so it will be interesting to see what happens with average transaction fees. If there is a coalition of miners that decide to only accept high fee transactions, we should see transaction fees go up on average. I don't know what will happen.

Murck: There would be a strong incentive to drop out and go to 0.99% and take up all the juicy transactions that are just under. It would be very tempting as the economics shift to see how that coalition would actually hang together. Yeah, for sure.

Q: Once all the coins are mined, will there be fees?

Gavin: No. Nothing. One possible future is that all transactions are free and mining is paid for through some other way... like BitPay and Circle want to run mining farms so that their transactions go through, they might not put fees on their transactions, there's nothing in the protocol that forces a particular transaction fee at any time.

Murck: There is sort of an assumption. If the transactions are not subsidized by the block reward, if there's no externality like you described then the other logical thing would be to charge fees for the processing power. I think that's what people predict. As the block reward gets lower, something has to take that up whether it's hidden fees which is what Gavin mentioned, if people decide to do it for some other reason, or it's visible fees, or it's charging for transactions to go through the network.

Q: I have a simple question. How would you describe the Bitcoin system to a five year old?

Gavin: That is not a simple question.

Q: You know Bitcoin deeply. Peopletry to explain Bitcoin using different stories. What's the best story to explain?

Gavin: Asking geeks to explain things clearly, that's probably wrong. Ask a marketing person.

Murck: That would be a good contest with a bounty. Find a five year old, and once he understands it, pay the bounty.

Gavin: I think five year olds don't even understand money yet.

Q: Okay, 10 year old.

Gavin: Maybe. Uh.

Cory: Not understanding money almost helps in a way. People always get caught up with the things they do know. People have some very hazy concept of mining. So when you try to explain Bitcoin, you get kind of half-way through a speech that you think is a good explanation, and then they jump in with "What aobut the miners? What do they do?" And that's important, but mining is almost a different subject on its own. It's almost a distraction from an explanation of what the thing is at a basic level. I've found it hard to explain to some who have some basic knowledge, because the preconceived knowledge tends to be kind of close to how one part of it works, but not the whole explanation.

Murck: So for a while there, I was explaining Bitcoin to regulators and policymakers which is sort of like explaining it to a 10 year old. Instead of trying to convince people about Merkle roots, nobody understands that. Gavin might, I don't. I also don't really fundamentally understand how SWIFT transactions work, or how the ACH network works or the SEPA network or whatever. Any time you start talking about how money moves around the world. I don't know if anyone has written that book yet. Try to meet people with that. If you talk with a 10 year old, try talking to them about buying a toy around the world. Or a grandmother about passing a deed to their grandchildren, here's a cool way to do it on the computer now. Describe something useful to them. The other best resource out there, honestly, and this isn't to just because Andreas is here, the first two chapters are excellent descriptions that are accessible.

One last one? One or two very quick.

Q: Two part question. With the hard forks, do you feel any, ...

Gavin: The reason why I am pushing the hard fork now is that it has to be scheduled. In six months to a year, we might run up into the 1 megabyte block limit if we have another run-up bubble. I am not worried about it being harder in the future. I think it may be easier in the future if we have a good standards process. Run a hard fork through some standard sprocess. It would be easier than arguing on bitcoin-dev endlessly. I think it may be easier to do in the future. I want to do it now just because I'm worried about another bubble and a transaction volume hard limit.

Q: We were talking about the fee structure a few minutes ago. I think that obviously the fee and prioritizing of transactions is necessary to prevent penny flooding, in terms of making this a friendly technology for users, it's confusing to them that they have to pay a fee at all. I was wondering if there's going to be anything in bitcoin 0.10 to address that, or any protocols. Or maybe BIP 70?

Gavin: I think merchants want that. I think it would be a trivial extension to the payment protocol. Maybe in 0.11.

Q: A payment protocol around that?

Gavin: The problem with child pay for parent is that you need both transactions to be sent at the same time. If you send a free transaction that doesn't relay across the network, you need both to be bundled up at the same time, and you might as well just use the payment protocol in the first place.

Q: And coinjoin for privacy?

Gavin: Exactly there are all sorts of reasons.

Thank you for participating.

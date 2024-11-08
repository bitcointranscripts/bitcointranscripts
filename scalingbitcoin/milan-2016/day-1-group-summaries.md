---
title: Day 1 Group Summaries
transcript_by: Bryan Bishop
tags:
  - lightning
  - privacy-enhancements
  - mining
---
We need two to three minute report backs from each session. Also, note takers. Please email your notes to contact@scalingbitcoin.org so that we can add notes to the wiki. Come join us. Okay, so.

## Lightning

We discussed routing and several aspects of routing algorithms in the lightning network. We talked about the tradeoff between privacy aspects and reliability in routing. We quickly discovered that after some of the things were already resolved by the papers-- the way how we deal with a general separation and channel transaction fees, is actually quite an interesting discussion topic. We looked at how do you want to communicate, how many times, and how do you prevent attacks. That covered much of the time of the discussion. You can read the details in the discussion notes.

## Fungibility

Who wants to talk about fungibility? Who is going to speak? We are just getting the notes.

## Non-financial applications

Okay while we're waiting on them, we'll do non-financial applications. Okay, so for the workshop about non-financial applications we talked about non-financial applicatios in this space, existing in such a way that they would benefit from a blockchain system in some way. After we talked about categories, we talked about scaling. The consensus was what that we had timestamping applications, proof-publication applications, and state transition applications. To help them scale, timestamping solution was pretty straightforward. You just have a service aggregate the various pieces of data into a merkle root and you write the root of the merkle tree into the blockchain.

As far as publication, there's not really a trustworthy way to do this in a coordinated fashion. I have to trust someone to cooordinate publication for me. Using multiple operations on the blockchain, you can get a weaker form of consistency if you write operations to the blockchain and then interpret thisme in a database log, as ong as you are okay with nodes diverging and following different rules. Other than that, we think it's not really feasible to put a whole cluster of operations off-chain and try to get all the nodes in a rigorous application to play them because that will open up to data availability attacks.

DHTs and IPFS might be one solution to data storage. DHTs are not good reliable stores of data because even if you have a whitelist and blacklist of keys that to be stored, you might be target of DHT routing attacks. A big component of non-financial applications is that you ensure you have a copy of that data and you should replicate that far and wide however you can and have a way to reconstruct it if at all possible.

## Fungibility

We discussed several topics in the fungibility workshop. One question which came up was could we tell the price of privacy. What are people willing to pay for getting better privacy for bitcoin? You can't extract a single value for everyone because the people who want better privacy are willing to pay more. They go to greater lengths and they use multiple tools. A single price for privacy is not something that exists; it's worth more to different people. Another concept is this-- money soiling as a side-effect of using tools for unlinking where you get deniability in your transactions it gets more difficult to extract what you're doing, but the coins you end up with are now essentially dirty, they have been marked as coins that people have taken an effort to make more fungible. If everyone was using fungibility tools, and joinmarket was merged into Bitcoin Core wallets, then that would be much better for everyone.

AML and KYC regulations-- often the businesses that require compliance with these-- they don't care about the cryptograhpic proof of where your coins come from and where they went. They only care about whta kind of business you do, what you claim to be doing, etc. So the fungibility tools are better for giving you a sense of privacy but the businesses still simply be interested in your answer when they ask you where is this money from and where is it going.

Another issue that we brought up is essentially a low-hanging fruit that individual wallet developers and application developers can each take steps to improve this successively, which is coin selection algorithms and the way that their wallets cluster coins. Output ordering, bip69 I think.

Thank you. Awesome. Thanks.

## Community

We started out by talking about the general perceived problems. Everyone said a word about what they thought the bitcoin community was with a descriptive adjective. We got open, we got closed, that was interesting. We also came up with three broad categories of issues and we tried to identify solutions. One category was tools and techniques like censorship and moderation, echo chambers, negative perceptions of bitcoin, continual reinvention, and on the solution side we talked about a matching tool for communication types where technical conversations happen in specific forums and we can have them specifically threaded and followed. A library of great debates of bitcoin and revisit them, and maybe if there were ideological debates then key take aways there. We have issues about conversations on reddit, where it focuses on recency and archival efforts are important. On expertise and knowldge, there was issues on estimating what knowledge we have or don't have, and on the solution side we talked about the role of research and more fact checking and more empirical ways to engage in debate and backing up things with facts. We are disproportionately intelligent so we should have lots of resources on that. And not one person can do everything... maybe be more open about it being an open and creative process to develop expertise and get more adversarial thinking to stimulate that creativity. And lastly we talked about behavior, which was discussed a lot at prior Scaling Bitcoin conferences. Respect for different opinions, lack of inclusion, lack of decency, people using inappropriate appeals to authority, character assinsations-- less concrete, but perhaps someone can help implement them - how do we develop empathy, how do we freeze out disruptors, how do we cultivate patience because this is going to take a lot of time. Our resilience is a positive trait. We need everyone to have more humility and broach discussion with perhaps more humility.

## Hashrate decentralization

Mining centralization is a bad thing. The incentives are unfortunately aligned in that direction. From our discussion, some interesting points emerged. We can push more hashrate to the edges. We could have an open-source ASIC design. The actual hardware design, the actual VHDL is the easy part. The fabrication is difficult. The specification is different, there is no standard. That would be a great higher cost in keeping that synchronized.

Second point, beside the high cost of entry into mining... there's also the mining equipment.. it's not through market. Another point we discussed is why mining centralized in China? Currently it should be about 70% of the hashrate is located in China. The reason why is that, China is quite friendly towards Bitcoin. Low cost of energy. Around 3-4% per kilowatt. Also logistics for mining operations, for buying and building farms. And low beaucracy. It's much better than Iceland in this regard.

We talked about moving to different proof-of-work algorithm. Obviously the dust is not settled on this one. We were talking about new attack vectors on the network. That hardware could be used for something else, if it was memory-hard hardware. The optimal behavior for a single honest miner with internal blockchain incentives is to .. less than 50% of the hashrate, because anytime more than that would actually be a race against yourself. External economic incentives.

The decision of .. keeping at the center.. only the ledger cost, but also consideratio as... and the production of the country because the lifetime of mining at the center is around 2 years. So you don't want your data center to get shutdown before the cost.



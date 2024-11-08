---
title: Google Tech Talk (2016)
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Jihan Wu
---
Bitcoin

Google Tech Talk

Okay so maybe we will start. Thank you for coming. We have about 25 folks here from the Bitcoin community, both miners and Core developers. Don't know exactly what the definition of a Core developer is, but I guess I know one when I see one. So anyway, we're lucky here to have Jihan Wu. He's the co-founder of Bitmain, a leading Chinese bitcoin technology company and mining pool. He runs Antpool which has 270 petahash which I think represents about 20% of the hashrate currently. Mr. Wu will be telling us about bitcoin mining, understanding the technology and the economics.

Hi everyone. Thank you very much for asking me to give a speech here.

Bitcoin mining is about doing PoW, proof-of-work. It's difficult to compute, but it's easy to verify. Bitcoin is using hashcash proof-of-work system which was invented by Adam Back in 2002. Bitcoin's proof-of-work is like building a timestamp server. The hash, it's hard to find a good nonce. If you find a good nonce, it means that you have spent some amount of work on it.

If we adjust the difficulty of this job, it means that you have spent some work on this block. So it becomes a timestamp server where it's difficult to forge.

Bitcoin is using sha256 as a proof-of-work hash function. In the beginning, people were using CPU to mine. Someone was able to develop a GPU algorithm so that many GPU cores could do sha256 hash simultaneously. Later, someone developed an FPGA. It had some tradeoffs. The GPU was cheaper to buy but it's more power consumption. FPGA was expensive to build, but the power consumption was much smaller than GPU.

Eventually we had ASICs, around the beginning of 2013, which was cheaper than FPGA and used less power than FPGA and GPU. When the ASIC showed up on the market, the majority of the hashrate has come from professional mining data center. In this picture, this is an example of a hashrate mining farm. The miners in China, there are about 100s of these mining farms. In the Western world there is less, but there are still tens of them.

We can see that the technology improvement of Bitcoin mining technology was driven by and highly related to the price. It is driven by the bitcoin market price increase. At the beginning when the price was low, everyone was using CPU mining, the community was small and perhaps nobody knew about GPU and FGPA. Later, someone joined the community and had the capability to do this, and then the ASIC method was invented for hashing.

ASICs have also experienced a very fast improvement in the technology from 55nm to 28nm to 16nm in BM1387. During each process node, we can see that the time is only about 6 to 9 months until the new product. All of this improvement was driven by the bitcoin market price.

We can see that in 2015, Bitmain's customers were distributed. If we count by the number of customers, 76% of the customers came from China. .... According to the number of sales, if we count the units of machine, ... 75% of the mining machines were bought by Chinese people, and only 25% were bought by Western individuals. Basically the Chinese people are more likely to buy large chunks of miners, and in the U.S. they seem to be more likely to buy a single miner per person. ((Note: some of these numbers may have been written down incorrectly during transcription.))

I think this trend is driven by the cost structure of mining farms in the U.S. and China. In China, to build a mining farm is much cheaper than building one in the United States. The time to build a farm in China is much shorter than the time to build a farm in the U.S.. When you are doing a mining investment decision, in China you can do it faster you can use less money and you can get a much sooner cash flow positive status. The capital expenditure in China is much smaller. Even if the America's power cost is much lower than in China, there's mining risk in the investment in America. So you have to reduce the payback period to reduce the risk.

The bitcoin mining difficulty rises very fast. The more risky it is the more quickly the difficulty is rising because you underestimate or over-estimate the amount of mining you need to buy and operate. In the past 3 years, a bitcoin has had a volatile price. Especially from the end of 2013, until the end of 2015, all the price was in a deep bear trend. This kind of bear trend also makes mining risky. With bitcoin mining, you are trying to have a short payback period so any long-term planning in bitcoin mining is unacceptable because you cannot expect that you can do a bitcoin mining investment based on 3 year assumptions about difficulty growth. So everyone is trying to capture their initial investment as quickly as possible.

We are saying that the situation is going to change because the mining, first of all the risk for the first of the parties about bitcoin exchange rate. We have a kind of trend, a volatility trend, the volatility in bitcoin price is declining and I see that in the future bitcoin might become a stable currency like the U.S. dollar against the euro. It has some volatility, but it will be acceptable as a store of value and as a saving currency.

We are also seeing that the technology improvement will be ... because we have a thing where Moore's law improved from 16nm, compared to 28nm, the power consumption dropped, and the cost to build a transistor decreased. After 16nm, we are looking at 10, 7 and 5 nm, at TMSC. The cost per investor is not going to drop very significantly, perhaps it will even rise. We can definitely see that ... before 2015, the mining experienced improvement in process node and design method. The process node has seen some fast improvement in 3 years time. The semiconductor industry went through that much development but it took them 30 years. Going from standard node to full custom design flow. Standard design flow means that we design the chip, and then the computer will compile the chip automatically. Full custom design flow is where a human manually place transistors on the chip to achieve the most effective circuits and the design methods are already best possible optimization. So the mining technology is going to stop improvement for a long time, and we might have to wait for semiconductor technology to improve, or perhaps we will have to wait for new technologies (such as quantum mining ASICs).

Every generation with a mining rig in the near future might have a 4-5 year lifetime use. They need to find a cheaper long-term operational cost, without reducing the issue of capital expenditure.

That's my presentation. Thank you. Next, I think we should go to Q&A. We are also lucky to have many important Core developers in this room. They have a rigorous understanding of the Bitcoin protocol. Anything about mining, protocol, Core, we can share lots of information to any questions.

Q: I am one of the Googlers. I can be considered a newbie in comparison to the others in this room. What's happening with the other second hand miners? Do people have free energy where they just buy up second-hand equipment, or does it go into the trash heap?

A: There is a liquid market for second-hand miners. Some people will buy new miners, decide to sell their old miners on the second hand market. It's very liquid. Eventually those miners will end up in some... zero cost electricity. There are some hydro power stations. Some of the hydro power stations in the summer. Lots of wind, and they can't sell the electricity to the grid company, so they will use low-cost mining rigs to generate the revenue.

Because difficulty is growing quite fast, old hardware represents a small amount of capability. Right now, about 80% of the hardware is 28nm and 16nm. The old hardware is representing a small amount of hashrate capacity.

Q: I am also with Google. I am sort of fascinated by the concept of free energy. Is there any notion within hydro power where you have these hydro power plants need to get rid of energy, and in that point in time, bitcoin gives them an opportunity to monetize that energy in a way that they would not be able to?

A: Yes. Grid company in China is a monopoly business. Where the power is generated is very far away from where the power is used. In the summer, lots of rain. In the summer, lots of energy that cannot be sold.

Q: Isn't that to some extent, say that, in those cases at least, bitcoin is not burning up any energy at all. This is excess energy that would otherwise be burnt anyway. And now bitcoin can put the energy to good use.

A: Yes.

Q: Also a Googler. How does AsicBoost paper effect this? How does it effect hashing?

A: AsicBoost... there are two ... compress, another part is we call it labrio. Using AsicBoost technology, one patent, maybe the other patent could be shared.

Q: How much power per chip?

A: One part can be turned off, and the power can be reduced. Our chip already has this function.

It was independently invented by 4 different parties. So is it .... it was independently invented by several different parties. Legal questions probably the wrong context for those.

Q: As a mining company, do you think about hedging against currency itself? Some other coin plus bitcoin, how do you hedge against actual currency you are mining for?

A: We have a litecoin (LTC) mining chip. We also do other mining algorithms, like ETC if they change their mining algorithm.

Q: What percentage of your mining power is devoted to BTC versus LTC or other algorithms?

A: LTC chip has not arrived yet. So 100% of our business is related to bitcoin at the moment.

Q: Thanks for coming to give the talk. Very interesting. I have another question about hedging. Is there a sort of well-developed and liquid futures market where you could forward-sell bitcoin that you estimate you will produce in the future?

A: We are aggressive about bitcoin price. So we only sell to cover the cost of the company. The rest of our revenue and profit is saved in bitcoin.

Samson from BTCC. There is a futures market. Also, CFDs that you can buy and sell in advance. You can hedge what you're earning.

Q: Is that used by lots of miners?

A: Used more by traders. Miners could do it, but I don't think that many miners did that. It would be good if they did.

Alex Petrov from Bitfury. If you have a big data center, you can keep a couple of bitcoin for the future. But for smaller miners, they should sell them almost immediately with some delay to cover energy cost, data center cost, or employees who were working for data center support. They have bigger risk. Because they have bigger risk, they have lower margin for what they can keep for future. Bigger miners keep bitcoin, they believe in bitcoin's future market price, and they are trying to save bitcoin for the future.

My name is Jack. Sometime it's in fiat, sometimes in bitcoin. But the difficulty of hashrate rise, you don't know. So mining company tell you how many miner produce, and the price faulty too, so there can be bubble, you can tell, sometime miners lose money. In my opinion, small miners are... very very quickly, and hashrate is centralized, especially in Western area there is lower cheaper electricity and in some places in America, like Washington State, and Iceland, because they are using water to produce their electricity.

Q: I have a question. It is my understanding that a core part of the Bitcoin transaction thing is the verification of transactions which has a relatively high average completion time. I was wondering is that something that limits the potential of bitcoin's growth into less of a niche market, or is that latency unrelated to the potential throughput of the currency?

A: Gregory would you please take this one?

A: Hi this is Greg Maxwell. You can look at the 10 minute average expected time between blocks is more of a settlement time of transactions. So in comparison, a credit card takes months before you know the transaction is irreversible. We don't view the transaction rate as gated by the confirmation time. There are other technologies in the Bitcoin ecosystem that people have been building and deploying that also get weak confirmations of transactions much faster than the 10 minute average expected time.

A: Hi this is Pieter Wuille. So there is the time to validate transactions, is important for the time that blocks take to propagate across the network. We don't require every payment, every economic activity in the bitcoin ecosystem to go on the blockchain. There are many technologies being developed, and there are some people here from Lightning Network here, who are working on second layer systems for technology here. You can have a large amount of transactions that happen between two parties individually and only when a party doesn't follow the protocol, they then go to the blockchain to settle that dispute and get your money back based on the agreed rules. Not everything as a payment needs to be a transaction that the whole world needs to see.

Q: My question is, ideologically speaking, where do you see bitcoin going in the future? What sort of fork do you support? Do you choose for yourself what you're going to support? How much of that did you catch?

A: I see the future of bitcoin as a payment network and store of value. These will be self-reinforcing and it will power the growth of bitcoin. The payment people will use bitcoin as a store of value and as a payment as a way to accept value from other people. And as a store of value, which is to say investment and long-term savings in the bitcoin network, just in the same as lots of payments are occurring, so it can be safe to store value in this. I think that bitcoin will have to support very high frequent payments, a combination of the main chain transactions and also several other layers of tech like sidechains and lightning network. Different use cases and different use scenarios will use different technologies. You also asked the question about a hard-fork. The hard-fork right now becomes a really risky situation that lots of stories very well known right now. I can summarize it in a few words. I want to say that if we want to define what is bitcoin, there's the github repo and most of the proof-of-work by sha256 hash function. These things together will define what bitcoin is. However, if there are two things following apart, there's a risky situation for Bitcoin, and splitting it into two things is a huge risk. The value has a strong network effect. It would be very risky for bitcoin. We need to work together and try to find the widest consensus possible.

Q: What point in time do you see transaction fees as becoming more valuable to you than the value of the coin itself? Do you see this in the future?

A: Bitcoin was constructed initially to provide interest for the miner to provide the work. The miner not performing the work, just to rework, performing critical point for bitcoin network functioning. They are signing the blocks. To support integration for the future, rework during the time decreasing, and at the same time, they should just be crossed and the fee should cover the expenses. Right now, we are trying to calculate the fee, using a linearly assign the price in fiat and use euro, during time that the bitcoin price should be higher, and the bitcoin should be fully balanced to cover expenses in dollars for what the miners are spending. Or it could be modified, if we are getting resource of electricity so it will be supported mostly by small donations to just support the bitcoin network functionality, or it could be business interest to support the network function. Answering the previous question, the bitcoin blockchain is very interesting and multi-layer and multi-dimensional tech. We haven't studied it sufficiently yet. You can build timestamping services. You can store a lot of information. Blockchain is storing information forever. It is hard to store all data forever. Bitcoin became a big network, perhaps it's not the perfect solution, but it was able to collect the biggest hashing power to protect the asset in the bitcoin blockchain network. As a result, there can be many different solutions and locking itself on the central blockchain of bitcoin.

Q: To what extent does ASIC manufacturing still consolidating to just a few manufacturers? KNC is out of the picture, I think. Are we going to end up with just Intel and AMD where there are only two companies able to produce the chips?

A: It's very messy situation that we will have to get into. From the beginning, in the middle year of 2012, I was an investor in ASICMINER, they were one of the first ASIC companies. Mining manufacturing could be consolidated. Any semiconductor industry can be used. Whether we have to use a semiconductor produced by Intel, AMD or Nvidia, we specified same type of algorithm and we can end up in that scenario inevitably. If we have to end up in the kind of consolidated state of mining equipment, I think that's something special that is independent. [.....]

Q: A question from the online dory. What challenges is the bitcoin community facing at the moment? What would it take for mass adoption of bitcoin?

Gregory would you like to answer that?

A: I have this interesting thought about the growth of bitcoin. If you, and maybe others don't share this, but I like this one. If you imagine that everyone in the world would wake up tomorrow and know in their heart of hearts that bitcoin would be the true reserve currency of the world, then this would not be good news. The result would be war. People would fight over the supply of bitcoin. The adoption of bitcoin into society, for it to not be a huge wealth transfer from everyone to me, requires time. There must be time and for actions to flow throughout. From the perspective of a developer and industry member, this is good because we need time to mature our protocol and our industry to handle the greater adoption. I think the greatest challenge for us is primarily time. Inside the bitcoin industry, the participants are all new. We are all young companies. We are still feeling out how we interact with each other and how this future looks like. When you build a currency that is intrinsically decentralized, some of the traditional models of building industries don't map as well. We are still stumbling in the dark on some of this. We have a lot of shared interest in cooperating on this, and many people around the world are excited about the potential that bitcoin brings.

Thank you.

Q: One of the ways I think about me being able to contribute to the bitcoin company, apart from buying bitcoin off an exchange, is to participate in mining using a small miner. Is that a possibility today with your company? Can I get stock in Bitmain?

A: Work for Bitmain to get stock from us?

Q: Are you a public company?

A: No, we are a private company and we offer options.

Q: What do you think is the biggest threat to bitcoin right now? Government? Opposing coins?

A: Governments are not a threat to bitcoin right now. It's too small for the government to touch. It's a new thing. Different governments in different parts of the world will not want to lose the opportunity that bitcoin brings them. I don't think government will be threatening to bitcoin. The largest threat to bitcoin is that bitcoin has a network effect. It is not a physical effect. It's more about consensus reached by its users widely distributed over many different backgrounds. If a substantial part of this network decided to act seriously against the other group, then the network might fall apart. That's kind of the risk that bitcoin needs to solve in the near future. If we somehow have a solution or found some way to make sure that this kind of consensus will always be united in technological and political goals and better governance models or better communication models, there are many things we need to check into. But it will be up to the community and the different parts of this economy to work together and stay united that bitcoin will have 100x growth.

Q: Can I ask a follow-up question, if you do not see government as a threat, do you think governments will have a hand on monetary policy going into bitcoin? Do you think they will decide what code will allowed to be written?

A: Bitcoin will be a worldwide distributed system. No single government will be able to decide anything about bitcoin. U.S. dollar is controlled by the Fed, every other currency seems to be controlled by a central authority. Bitcoin will be a world-wide protocol like the Internet protocol where no governments would be able to control the monetary supply. Yes maybe if there are 200 governments that decide to unite together and try to control Bitcoin that yes maybe that's doable. Technically, however, I think they cannot do that according to the current international relationships.

Q: What is coming in the next year?

Gregory?

A: Hi, I am Pieter. I work for Bitcoin Core. I can say a few things about what are being worked on. This is about full nodes, validation rules and the consensus system. I will say a few things about what's in the upcoming release, 0.13, which is about to be released in weeks from now and a bit after. Things we have are for example, a recent change that has been merged is child-pays-for-parent which is the idea that an unconfirmed transaction you could spend one of its outputs with a higher fee, and both of them will be considered by miners to be included in a block. Miners get better fees from this. Wallets get an additional opportunity to re-decide that their previous fee was not good, and perhaps reprioritize their transaction. There are alternatives like replace-by-fee. There is also segregated witness, which is what I have been mostly working on. This is the idea of moving the signature data out of transactions and thereby giving moderate capacity increase to the network in a backwards-compatible manner. It has been tied with some other improvements that are probably more interesting, one is that it fixes the idea of malleability in bitcoin transactions, at least adversarial malleability where third parties on the network can modify the transaction in flight. More complex protocols in bitcoin depend on transactions being immutable, so this solution has been in demand for a long time. Another thing it will solve is script versioning. Before, script versions did not have a version number itself, which limited us greatly in which changes could be made in the scripting language which define what bitcoin contracts can do, to a very limited subset and often needed hacky solutions. Due to script versioning, we can pretty much make anything we can come up with as a scripting improvement to be upgraded in a backwards-compatible way. Things that I hope we can propose in the near future are things like better tech for multi-signature and complex transactions where not the entire script needs to be revealed to the entire world, thus saving space in the blockchain. Compact blocks are coming, so this is something that has been merged for v0.13. Before, we had to transfer every block as a whole once found by a miner, to everyone. This caused delays and bandwidth spikes and various problems related to it, the most important issue was the delay it takes for a block to reach the entire world. And compact blocks improves on this by using short hashes to refer to the transactions that most nodes on the network already know and have already validated. So this is a big step.

Among other things we are working on, particularly falling from seeing the mess in ethereum right now, is tech to make any kind of future like a hard-fork to be safer when deployed on the network. There has been work that has been going on in that for a few years. We have been reminded that having things ready is a lot of sense, especially for network emergencies and other demands in the future to make sure the solutions are well-engineered.

Something I think worth mentioning is that, we were just talking about changes made to Bitcoin Core, some of those changes are not consensus changes, like compact blocks. If we both runs Bitcoin Core nodes, regardless of whatever other people do in the world, this is not a change to the protocol, it's about getting data to other nodes faster. If someone doesn't use compact blocks, they don't have to adopt it. In a protocol change like segwit, it's often that we're guilty of saying this is coming, but ultimately it has to be adopted by the rest of the community. They might choose to adopt something different. There's not just Bitcoin Core, there's btcd and other implementations. They are much smaller and sometimes they have no team; you should not assume that their proposals wont happen. Our changes usually get adopted because we have better proposals, but if they disagree then the community might go in a different direction and that's fine.

Q: To what extent are Core developers learning from Ethereum's hard-fork event? Are the teams communicating often?

A: We don't generally communicate well. We sent warnings privately to Ethereum developers in the past. We expected most of the things here. When you're cynical, it's easy to be right about things going wrong. We're definitely cynical, so expect us to be right when things go wrong. We absolutely look to see what we can learn from other systems. It's difficult. Many altcoin systems are small compared to bitcoin. Their failure modes are often complex and involve economic situations which are unique to them. It's sometimes difficult to extract useful lessons, but we still try to. The things we are dealing with have very high stakes. Mistakes are difficult to fix. There are not many precedents for the things we work on.

Something to point out too is that because this is a social system, mistakes made in other communities can have an impact on bitcoin because they change the perception of what is right or wrong to do. The ethereum split is an interesting example in bitcoin. We have seen this split, people have seen it, some people have incentives to make it happen (or not), and this makes the situation more complex. It's also not just learning but also reacting to the changes they make.

Q: How do you expect lightning network and sidechains to effect the mining ecosystem?

A: Alright, I can give some comments. I was trying to get Joseph... oh there he is. There is this baseline you have on what transactions go into the chain. There is going to be a line, no matter what. The alternative is not you know removing transactions off-chain. That's going to happen, no matter what. It's not feasible, no matter the block size, to allow a transaction worth 1/1000th of a penny, to get on the chain. There are some alternatives. Either don't have those transactions at all, do them in a centralized system like Coinbase or some other exchange transacting completely off-chain, or you do payment channel systems like lightning network. The nice thing about lightning network is that you are still having transactions on the blockchain, when you establish a channel and when you exit the channel. For miner incentives, you are still participating in the network, and your coins are still enforced by the network in the sense that you do have a UTXO output. It's possible that lower-value transactions move off-chain, and I believe that is something that we should welcome.

Q: To follow-up, do you think you require some mining on sidechains and on lightning network?

A: It does not remove the need for mining.

Q: Will it be the same ecosystem of miners, mining on other chains? Will it change, will it allow smaller miners?

A: I believe there is a misunderstanding here. Lightning Network itself is not a separate blockchain. It's a network in terms of channels among Bitcoin nodes on the network. They send money to each other. There is still a single blockchain only. It is secured by the same mining.

A: Yes, the most concise explanation is that it's a multi-sig output using smart contracts and coding behind it, with bitcoin transactions. Not concise?

Could we explain lambda calculus? Well if we're not going to start there, the lightning network transactions are bitcoin transactions. It's a caching layer. You've got multiple transactions. What ends up on chain is one transaction, even though you may have passed 30 or 40 transactions back and forth. Everything on lightning network are real bitcoin transactions, they are just elected to be broadcast at a later time in the event of non-compliance of one of the parties. You are committing to the summary of those transaction on the blockchain. You don't need to have all the different transactions on the blockchain. You can look at the blockchain as a dispute-resolution mechanism. If two people disagree, then you can go to the blockchain and resolve the dispute. But you don't want to do that unless you have to, because it's cheaper to avoid doing that.

Q: What makes bitcoin unique compared to ethereum? Do you see ethereum as a challenge?

A: Money-like goods gain their value from their network effect. Bitcoin has a tremendous network effect. We have a very strong focus on the properties of sound money. This has been in the system from the start. We have an extremely conservative approach to money. We expect bitcoin to be a better money-like good than ethereum. Most of the people associated with Ethereum Foundation position their system as a smart contract system and the ether asset is to fuel the smart contracts. There's a different focus there. I think it gives bitcoin a strong position. Ethereum has talked about some future experimental changes which are interesting intellectually, but may not be good long-term security, such as the elimination of Proof-of-Work and so far the research on that front does not look like that system would have particularly strong immutability.

Q: One last question for the Bitcoin Core folks. The closest example is ... security contingency plans?

A: When in danger or in doubt, run in terror, scream and shout. It's very difficult to deal with security issues. The answer is unfortunately that we have to make sure there aren't any. We have to work on provable validation of software. We found several bugs in OpenSSL. Our research efforts turn out CVE in many underlying packages that we use. It's a lot of work. This is one of the reasons why it's going to take time for the bitcoin technical infrastructure to mature. We need to drive forward the state of the art in software validation. There is a lot of diversity in bitcoin wallet software. That's interesting for mitigating and finding bugs. There's also multi-sig in bitcoin, and with heterogeneous multi-sig signing software, which makes it more difficult for a bug to cause a problem in multi-sig and bitcoin in particular.

Ethereum has been putting the complexity of the entire ecosystem into one place, in smart contracts. All subject to the same bugs at the same time. In bitcoin, the underlying layer is a lot simpler. The complexity of smart contracts is more... client side in bitcoin, unlike ethereum. Because the complexity is between the two of us, when we screw up and we have a security failure, the underlying layer is going to be unchanged and the fixes will be at the layer above rather than manipulating the layer below which Ethereum Foundation did when they bailed out TheDAO.

Thank you very much Jihan.

---
title: Trust And Blockchain Marketplaces
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - David Vorick
---
# Introduction

I founded Sia, a decentralized storage platform started in 2014. Today, Sia is the only decentralized storage platform out there. I also founded Obelisk which is a mining equipment manufacturing company.

# Mining supply chains are centralized

Basically all the mining chips are coming out of TSMC or Samsung. For the longest time it was TSMC but for some reason Samsung is at the forefront for this cycle but I would expect them to fade out in the next cycle. There's just two, and there's nobody else.

# Mining rig manufacturing is also centralized

At the next level down, TMSC and Samsung make the chips but you have to make the boards and rigs and stuff. There's really only five major companies that manufacture these-- Bitmain, Whatsminer, Innosilicon, Canaan, and Bitfury. Mining rigs don't have multiple features to compete across; either it does a ton of hashrate at not much electricity consumption or it's a worse product. So each cycle you end up with one miner that is pretty dominant. Bitfury is usually that one. Bitfury's development team left and started Whatsminer.

# Mining pools

Mining pools are also centralized. As we go down the stack, things get better. There's 8 mining pools that have 80% of the hashrate. Current mining protocols allow the mining pools to decide what gets mined. Mining pools are also more flexible, it's difficult-- if you don't like Bitmain, it's difficult to push them out, but mining pools on the other hand, there's a lot of software and it's not that difficult to write some of it is but you can switch mining pools a lot more easily than switching manufacturers.

# Mining farms

Mining farms are definitely the most decentralized. Mining farms don't publish clean data, so it's hard to figure out how many there are and where they are located. We know that roughly 60% of the hashrate is in China. It's probably a few low dozens of mining farms to get 50-60% of the hashrate. It turns out that cheap electricity is not that scalable. It's still not 1 CPU 1 vote vision that was originally presented.

# Progress in decentralized mining is slow

If you look at decentralizing TMSC, that just seems like an insurmountable task. Decentralizing Bitmain has been tried a few times, but it has failed at great cost to the people that tried. And mining pool situation doesn't look too bad, things are moving slowly but we might be able to get to the point where mining pools are actually decentralized.

# Mining is inherently centralized

This is inherent to how mining economics are setup. Bitcoin mining is zero sum, and this kills everything. If Bitmain comes out with a better rig that is faster and more energy efficient, then this hurts all the other manufacturers. So your revenue drops and your profitability drops if you don't keep up and buy the Bitmain rigs. So mining is ongoing and incredibly expensive. So if you're not running competitive hardware or in a competitive data center, then you get pushed out of bitcoin.

One thing that we saw on, when we were manufacturing, is that if your competitors are raising money by using dubious means like lies or if there's legal stuff happening that doesn't make sense... that's profit margin for them, that you don't have. If you refuse to compete using dirty tactics, you just won't be able to survive, at least in our experience. Basically, every dollar that your competitor can get that you're exlcuding from yourself by ethical means, is you getting put out of business. Every dollar you place into true decentralization-- to open-source stuff, for our engineers we needed to focus them on building and optimizing. We couldn't take someone aside for 3 weeks to present something to the public. It was a lot more challenging, the survival grind was very strong.

This indicates to me that mining is inherently centralizing. The economies of scale cut a lot deeper than normal economies of scale. It's a zero sum survival grind that binds you against doing anything else.

# Challenge: Assume a monopoly miner

So maybe as protocol designers, we should get rid of the assumption that you have 51% of the hashrate not colluding. Maybe it doesn't make sense to assume 50% honest hashrate. I think it would be interesting to open the doors to this new assumption where we assume that each blockchain ends up with a single monopoly miner on top of it, and we just see what happens to the ecosystem if you have to live under that assumption. Having been on the ground, assuming that 50% of the hashrate is not colluding is always going to be risky and tenuous. So maybe we should just accept that we're going to end up with monopoly miners, and then design around that.

If we have a monopoly miner, then we want to eliminate what powers they have. Depending on how you design the protocol, blockchain miners can be malicious in different ways. We want to minimize the window of opportunity for a monopoly miner to be malicious. Also, we want a penalty where if we catch them being malicious then we should have some way to cause damage or disincentivize them from acting maliciously.

Two fnudamental miner problems that I don't think you can get around... the first one is that miners choose transaction ordering and how blocks are formed. So your monopoly miner is able to censor transactions from being able to make it into consensus. Since they build chains, they can reorganize the chains and reorder history at a cost. They have to redo work. There is some price that miners can pay to organize history, but I don't think in a standard blockchain you have a good way to stop reorgs.

A lot of protocols, we get these bonus powers. SPV nodes assume that miners are mining valid blocks. If you have a monopoly miner, this assumption maybe becomes a lot more questionable. In some protocols, miners can set the block fees, set the block size, etc. If you have a monopoly miner, they might play with these parameters. Some other protocols go a step further and give miners a unilateral power to change consensus rules, which if you have a monopoly miner is not something you should do.

If you assume a monopoly miner, then you want to cut out as much of this as possible. So don't give miners bonus powers, don't endorse SPV, and don't let miners signal the activation of soft-forks. You don't want miners to have power; they have a job to build blocks. If you let them choose about soft-forks, that gives powers to miners and maybe if we have monopoly miners that might not be what we want to do.

# Limiting censorship potential

Miners can't censor transactions if they can't distinguish transactions from different actors. Either they choose to block everything which kills the chain, or they have to choose to accept almost everything. A miner can choose to censor, but if we can hide from them which transaction is which, this power won't do a malicious miner any good. This would protect us against a monopoly miner.

# Limiting double spend potential

The other thing we can do is limit double spending potential or history reorg potential by asking for more confirmations. So if it's a valuable transaction, ask for a lot more confirmations. You should depend on layer 2 channels that are super burried, this might be too optimistic and maybe we should think about that more. For future research, what are design principles we can use or techniques we can use to limit the malice a miner can do if we assume a monopoly miner mining our chain?

# Attacks are detectable

We should also penalize rogue miners. Censorship is detectable when a transaction with an appropriate fee is not being mined. You can determine censorship is happening there, it requires you to be watching in real time, so you can't prove to an offline friend that the malice was happening. But in real time, we can see censorship. If the protocol is running honestly, there's a probability of a reorg of a certain depth, and if we see a reorg on chain beyond the probable depth, we can assume an attack because it's just probabilistically unlikely otherwise.

# Out-of-band penalties

If we detect an attack, we need some means of penalizing miners. These penalties must be off-chain. The miners control what transactions get on the blockchain, therefore the miner can make sure that anything that penalizes the miners doesn't make it on-chain. So fraud proofs on-chain doesn't work, and the miner can deny access and never be penalized. We need an out-of-band way of penalizing miners.

Mining is expensive. It requires expensive hardware. It's intentional. The out-of-band techniques we can use, we want to threaten that revenue by off-chain behaviors that we can have. One example of a really heavy handed thing is that if the miner attacks the chain, then you could just quit altogether and walk away. If there's a lot of money at stake for the miner, then this is an effective deterrent. So it's a big bet to pursue this strategy because we're essentially putting the entire industry on the line. If we can't find a way to get consensus stable in a reliable way, then it's worth walkin gaway all together. This is not an empty threat, and we should take this seriously but it's also not our only option.

Something less severe would be a PoW fork to switch from sha256 to sha512 or something. You can break the bad actor or you can just switch away to a new algorithm. You can also change the supply chain. This really damages the miners. Normally this is ASIC resistance coins breaking other coins. Sia did something about this a year ago now. From our perspective, it was super effective. Miners were really respectful after they lost like close to $100 million dollars. I do feel that on the ground floor, since the hard-fork miners have been more respectful of developers and altcoin developers which is really the point. You want miners to pay attention to you and take care of you. At the bitcoin level, this would require a ton of coordination and split the chain because it's so heavy-handed.

There's a third one, I'll skip it.

Strategy four is to do a counter-attack. If you have more general purpose hardware, a chain gets attacked, then you can rent a ton of hashrate off of nicehash and counter-attack and the attacker will lose money making blocks. You're going to lose money, or long range attacks get more complex. I owuld conjecture that there are counterattack games which are interesting and not as expensive as the defender as they are to the attacker, in the event the attacker wins and if the defender wins then it's asymmetric in the other way. This amy or may not be useful.

You can also combine strategies: so if we ever see a successful attack, we leave altogether and the ecosystem collapses. You want everyone to participate in a counterattack; the person who is a victim of a censorship or double spend might not be the only one fighting to have the counterattack succeed. You get into more involved games beyond the scope of this attack.

# Concluding remarks

I have more ideas, but they didn't fit easily into this presentation. I think this is an underconsidered area and it merits more attention. I'm not saying we should just drop the assumption and change everything we do in bitcoin starting tomorrow, but I do think that we're getting to the point where we should take this assumption more seriously and look at things we should be doing to protect ourselves if it turns out that monopoly miners are the steady state.



---
title: Bitcoin Without Internet
transcript_by: Bryan Bishop
speakers:
  - Adam Back
  - Rodolfo Novak
  - Elaine Ou
  - Adam Back
  - Richard Myers
media: https://youtu.be/5Fim6g2BMZI
---
SM: We have a special announcement to make. Let me kick it over to Richard right now.

RM: We completed a project that will integrate the GoTenna mesh radio system with Blockstream's blocksat satellite system. It's pretty exciting. It's called txtenna. It will allow anybody to send a signed bitcoin transaction from an off-grid full node that is receiving blockchain data from the blocksat network, and then relay it over the GoTenna mesh network. It's not just signed transactions but also API data. I want to thank everyone at Blockstream who has made this possible. Check it out at <http://txtenna.com/>.

AB: I really like how they have integrated the blocksat API. This could be useful for relaying news in an emerging market scenario with a small amount of infrastructure built around a full node to use the satellite and the mesh network to submit information. So that's pretty cool.

EO: Okay, let's get started on the panel. Show of hands from the audience, who here has a Gotenna? Who here has successfully connected to the blocksat satellite? Oh. Anyone here have HAM radio devices? Okay just Johnathan Corgan. I guess we have some work to do. Richard, could you describe, who was this built for? You're building txtenna, but who needs it?

RM: There's a few people where this would be used. If you tihnk about being in an off-grid scenario like in your cabin in the woods, you don't have an internet connection but you still want to do some commerce. This would allow you to do ecommerce transactions over the mesh network and get it relayed to the internet. Another example is if you live in an area with censorship. This allows you to privately route information through a mesh network, which can help anonymize this because of the mesh relays. There's privacy and resiliency as motivation.

RN: We do a few different things related to both privacy and bitcoin. One of them is opendime. It's a sneakernet-style bitcoin. You can load it up, and then physically move it around. It's quite fascinating. You can use blocksat fee to check the device is actually available, right? And the other thing is PSBT the new standard for partially-signed bitcoin transactions. It really facilitates doing this sort of decentralized coordination of wallets and signing. One interesting thing about PSBT is that the bitcoin wallet doesn't have to know which hardware wallet it's using anymore, so you don't have to have a plugin in your hardware wallet into your computer. You can use an airgap. What's nice is that if you're using multisig, one person can sign offline in the hardware wallet, they can load the transaction into a micro SD card, and then send it over, he can sign a transaction and then send it through the third person who signed the transaction and then somebody will broadcast it. At no point do you need internet or a computer to do this. It's kind of remarkable.

AB: I think there's a lot of things that we have aspirations for the blocksat satellite network. One is general resilience and robustness. I mentioned, we have a situation where you can have network splits. You can be disconnected from the internet for political or even infrastructure reasons. It's important for bitcoin security that there's global visibility of a single network, particularly if a country with a lot of mining gets temporarily separated from the rest of the internet. So this is what independent connectivity is useful for, it's useful for bitcoin businesses to have multiple internet connections particularly if you're mining because if you're mining and lose connectivity then you're losing a lot of money very quickly. There are some countries that have one full bitcoin node for the whole country... part of that is because internet is expensive in real terms, it's more expensive than here in New York or in other developed countries. Also, the average salary is low, and in real terms bitcoin is very expensive. Typically these users will have smartphones just less bandwidth than we would expect. Radio technologies can help bridge this gap. Radio and mesh networks can fill in infrastructure gaps around those users.

EO: Could a user conceivably hobble together a bitcoin independent technology to actively participate in bitcoin?

RN: I think we have achieved that already. I think the last barrier has been getting off the internet. It doesn't mean we're not going to leave the internet, just like a bitcoin user might still use a debit card at Starbucks. But it's important that we know that we are able to do this, and expand on this capability. There are real locations that seriously benefit from these technologies. We can bring bitcoin to places where people are less fortunate or have extreme needs and would benefit from the censorship resistance model.

EO: How easy is it to cutoff someone who is depending on satellite? What about interference?

RM: What do you mean cut them off? With the mesh network itself, you would have to jam the mesh network somehow if you wanted to prevent people communicating that way.

RN: With lower frequencies, it's extremely hard to pinpoint someone. The same mechanism that helps you talk to somebody on the other side of the planet, you're bouncing radio signals off the sky and back down, so good luck trying to find where that person was. The other thing with meshnets like Gotenna is that they are like half a watt. Very modern countries have ways for pinpointing radio signals and their transmission, but when you have low power and it's a moving target, it becomes very hard. Soldiers use low-power radio because they don't want to be seen from satellites.

AB: For portable device, .... it could be infrequent, just sending transactions. For satellite, there's a different characteristic. There should be no radio signature for a user receiving block data from the blocksat satellite network.

EO: Ultimately any of these technologies will need a relay point to transmit information to the actual internet. How does this change bitcoin's trust model? If we're using a meshnet or the satellite network, are we trusting Blockstream?

AB: For satellite, surprisingly the answer is no. The bitcoin blockchain is all authenticated data. Transactions can be verified independently by anyone. Also, when you connect to a bitcoin peer-to-peer node, how do you trust that peer? It's the same reason- you are able to verify it. One thing you can do to help yourself is try to spot check some of it with other information sources, which you can do with extremely low bandwidth methods like checking a block explorer once in a while. This is a cross-check.

RN: You can double check Blockstream's satellite feed. You can check the blockheaders against the Blockstream fee... you can also check the fecundity of the blocks to make sure the difficulty is high, if something drops then something funny is going on. There's also 200 countries in the world, it's unlikely there will be a coordination of all 230 nations in the world to block the internet everywhere when we can't even solve world hunger.

RM: There's also an aspect to it, it's an alternative last mile connection. Just knowing that it exists, makes it less likely that a government or large company might try to create this sort of attack because they know they can't fcompletely control the ISPs in the country or a satellite company. People can get information from multiple sources, so hopefully you can avoid that attack.

RN: If you look at the Turkish internet shutoff and the protests there... people were re-broadcasting tweets over SMS, and then they started having call-in services where you could dictate a message for someone else to tweet for you. There's also the balloons going into North Korea with South Korea soap operas. Information wants to be free, and it's becoming substnatially cheaper to make sure that you're not blocked.

EO: It sounds like people with different streams of information access can use this redundancy to cross-check and route around censorship resistance. One thing with bitcoin is that there's some security assumptions like the assumption that all nodes are receiving information pretty quickly. The synchronization has to be faster than the proof-of-work solve rate. If people are using different forms of sources to get this information, could this open up the network to a reorg attack or partition attack?

AB: Because the satellites are in geostationary orbit, there's a few seconds roundtrip just to get to the satellite due to the speed of light, but it's not much worse than going around the world with the regular internet. It's not that much worse. I think the best defense against a network partition is having multiple connectivity. You can connect to the satellite network, and you can tether a smartphone as well. In order to save data, we could also get bi-directional internet service. There's some battery powered box that provides you with internet service, 2400 baud, and anywhere... satphone would work. There's another type of ... laptop-sized thing, you point it to the satellite and then you get some wifi and it has bi-directional internet. Someone running a mining node in a remote location could continue to mine even if there's an internet connectivity outtage. This is useful if you have geopolitical uncertainty.

EO: Richard, what about with remote mesh networks? How do they ensure that it is receiving information from the actual blockchain?

RM: We haven't implemented a receiver, it's a good match for the blocksat satellite network. The place I could see that playing well, and this is just a hypothetical, but say you had a miner and maybe they had ... and they found a block and they want to get it out as quick as possible. I could see something like a mesh network because it's such a small amount of information to send out, it's very easy to send out on the mesh network. If timing is an issue, then you probably don't want to rely on a mesh network anyway. But if it is the only connection you have, well, it's better to have something rather than nothing. I don't think we imagine a full node running on one mesh technology, it's probably a hybrid of multiple solutions, or high-speed fiber too. I think it's really more of a last mile technology.

RN: I think it's important to remember that most people don't need fast bitcoin. Miners have a speed problem because it's a race to show your new block. But as a receiver, your coins have been validated multiple times already. You are spending a coin that has already been validated. There's no speed problem there. You can take your time to send it out, the receiver can go through multiple hops and do multiple checks on validity. It's not like a line during the morning rush at Starbucks.

EO: In the event of a reorg attack by an exchange that was attacked, could Blockstream blocksat protect against this?

AB: One issue that has been along is with bfgminer and luke-jr.... you don't want your miner to not be mining, he had a feature in there which looks at the first one and if it's starts to mine something at a lower height than it previously mined, it takes that as a sign that something was wrong and switches to the pool. This kind of autoswitching could be interesting. It's one of those things where if you want to a participant in the network, you should make an economic decision that you're aware of the factors and if you're operating a miner then you're an economic actor. If the second one fails then you can rely on the first, and so on. Mining equipment should alert its owners when something strange is happening.

EO: The network technologies you guys decide are ad hoc networks where the only limit to join is that people need to run the network. How do you incentivize or envision incentivizing participants to run these networks even when they are not actively transacting?

RM: One thing that our co-founder said is that you can get some inspiration from bitcoin because it's a protocol that incentivizes its own use. Mesh networks have been around for a long time, why haven't they predominantly spreaded? With bitcoin we can get some inspiration for how protocols can inspire its own use, and get some incentives for running mesh nodes, even if it's not a lot of money, just like the lightning network sure you can make some money but just having that incentive of some trickle value will inspire people to go to a lot of trouble to run a node and there might be some approach like that for a mesh network.

RN: I described in my talk, there's an easy way to pay someone to do something for you in the bitcoin realm. You can just add an extra output to your transaction and if they broadcast that transaction they literally get paid, because their payment is embedded in the transaction and they cannot split it. If there's value or demand there, then people will do it, in the same way that wifi hotspots get paid for using the hotspot. It's fairly simple to incentivize users.

EO: Earlier today we heard a lot from people working on lightning network. Would these ntework technologies be applicable to lightning?

AB: It's something we have thought about because of the availability of bi-directional satellites. You're really in a quite extreme high latency low bandwidth situation with these satellites. Lightning is designed to be bandwidth efficient, but there might be specific things that could be optimized for network behavior characteristics.  I think some of these use cases might benefit from the ability to receive offline. If you require continuous connectivity to receive.... but with lightning, it's source-routed. When you connect to a lightning node, it tries to download a full map of the lightning network for routing purposes. It periodically updates.

EO: ... we did, and we cheated by ...

RN: So you can send any data if you have a, despite those.. It takes just a little longer, but it's totally doable. You can have a Liquid-based bank in a small village and say this small village is in the mountains and has bad weather and it's just a disaster to get data out of that. Maybe there's some accounting and when the sky opens up, you get some fee and you can do some consolidation of those transactions. You could literally have a federated bitcoin pseudo-bitcoin village running that.

AB: With high-frequency radio, one of the characteristics of lightning is that you need to maintain some TCP connection for the duration of the channel.

RN: You always have to pick, like low bandwidth or high bandwidth and the constraints.

RM: Lightning network is really about exchanging signatures. At the end of the day, it's mostly signatures being transmitted. There's down the road things like Schnorr signature aggregation. There are some opportunities to make lower bandwidth versions. It might not be the exact current protocol but it could be some low bandwidth versions of these protocols which would work over a mesh network or something. With mesh networks, mesh lightning is a mesh, it's a flat network, but it's an overlay network on a more-or-less centralized internet. The payment network and the communication network could be running on the same layer or same mesh network one in the same. There's advantages to that. Now your nodes aren't just for sending payments, but they also pay for the communication part of that.

RN: That's the cool thing about radio. It's all light speed. The speed is the same. But the bandwidth for lightning is not that much for a single transaction. We were using a, it wasn't the greatest bandwidth protocol for that... if you're using....

EO: When it comes to radio or satellite, what's the biggest hurdle in getting more people to actively participate in non-internet bitcoin?

AB: It's probably ease-of-use in the sense that at Blockstream we have received many requests about this. It's kind of complicated. Someone has to find a lnd with these characteristics or something. They just want to pay money and get going, they don't want to hunt for parts or hardware. Pointing a satellite dish is also kind of difficult and there's some tools required to do that. It's a bit of a learning experience.

RM: Gotenna shows that ... I think that's one important lesson to learn. There might be places that have problems with connectivity or expensive internet data rates. I think you will see adoption in those places before you see adoption in more developed areas.

RN: I see disaster relief as a particular use case. It just helps out, right? The learning curve is a little bit high, and it's complicated stuff. It has as many buttons as possible. These things could be packaged by programmers who want to turn this into here's a parts list, just buy this stuff, you just load this software and boom. You are now in the relay system. I think because we don't see a lot of need there for these solutions, like people reaching out saying I really need this yesterday, therefore we haven't seen a lot of solutions being made easy.

AB: ... and now, .. smartphone and.. and the other one is, hardware cost factors. Devices sometimes start out as like in the James Bond scenario where the satphone is extremely expensive. But maybe some devices like that do interesting survivability things for bitcoin but cost $500 or $1k will sell surprisingly well in this market, and this would provide funding to reduce the cost and iterate on this technology for other places in the world that really need it.

RN: There's a very selfish motive for any bitcoiner to do something like this. It's like running a full node. Do you really need to run a full node? No, but you do it anyway. If you want to be a first class citizen, you run your own node. But if you're invested in bitcoin, then it is in your interest in helping to make the bitcoin network decentralized. Maybe this means also adding a satellite dish on your house, or doing other things. If you have a voluntary system, all the solutions are kind of going to be voluntary too. There is no government money going out to do this. There's no list of things you must do to interact with bitcoin.

RM: Merchants are obviously enthusiasts, but once you see the bitcoin economy develop, you will see merchants that want to plugin just as a resiliency method. I think that is how things like that will get bootstrapped.

AB: The internal bitcoin economy is not that big yet. It has potential to grow, though. The cost is one factor. Things we would take for granted in other markets we take for granted, like equipment versus internet equipment which is heavily subsidized. People in emerging markets sometimes skip entire generations of communication technologies. Most major currencies have lost 99% of their value over 100 years or less. The pain point that bitcoin solves is not the main problem that most people in developed markets are actively experiencing pain from. But in emerging markets, they are excellent use cases for bitcoin. So make things cheaper and easier to use. Make more resilient infrastructure.




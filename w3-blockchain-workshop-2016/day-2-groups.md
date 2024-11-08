---
title: Day 2 Groups
transcript_by: Bryan Bishop
---
# Browsers

One was creating a new API or updating an existing API for Web Auth or an expansion to the web auth spec, where the browser would understand blockchain-based identity. We want to resolve and display blockchain identity in the browser, anything identified as an identity in a blockchain in a browser. Request payload signature. Apps receiving payloads could check from the user. Those are the four areas we are interested in pursuing for standards.

# Blockchain standardization proposals

These are actual proposals to start work at W3C or IETF perhaps. I am going to kind of list the proposals. We are going to write each one of these proposals up here for the dot voting segment. These are in priority order. These are in priority order where things people were most interested in. Blockchain receipts was up there at the time. IPLD. Semantic vocabularies and ontologies for blockchain. Folks felt like we need a blockchain interest group at W3C to steer this work. There was a discussion around smarter signatures that Christopher and Peter are going to take that stuff up. Expressing digital assets in decentralized systems. Libp2p which is interfaces for p2p protocols, peer discovery, peer transports, a URI format for blockchain networks, key management in the browser, cryptographic key management in the browser, proof-of-existence, generalized lite client header proofs, ways of expressing and using deterministic keys, the multiformat from IPFS like multihash multicodec multiaddr etc. There was discussion around exposing core network primitives like udp and bluetooth or NFC. There was a proposal for a blockchain gateway interface. The next steps are to put these proposals up here, and then based on the dot voting there would be some indication of the priority that folks would like to assign to them.

Q: Key management in the browser? This would be the 4th attempt for W3C. What are we going to do different this time?

A: I don't know. There seems to be more pressure for this. I don't think there was a concrete proposal about what that would be. The field has changed. We would like to have that discussion again.

# Legal implications

The proposition we considered was that legal docs, consider them as we do open-source software or documents. Systematic doc at a time. Specifically we discussed challenges around blockchain as a communication channel. How do you legally secure that? There has been no legal framework established as of yet. Our friend working with the Chinese bank mentions that they are extremely conservative and want it to be governed appropriately. Myself, working at a nuiversity, our office of general counsel is swamped using old syschronatic methods. We were looking at some next steps, we were looking at Common Accord as a core for a solution or a beginnings of a solution, coming up with a common record format. We talked aobut pagerank for transactions. If you are dealing with audits, it would be nice to have a weighted average like the amount, neutrality, identity, and the amount. We also talked about standards that don't exist but ought to, our friend Eric brought up that ISO has been recently looking at ISO TSP 2508 which has been looking at whether they need to get involved in blockchain. They are looking at a 50% vote to go ahead with a few countries. Looks like July 14th end date for responses.

Q: Is any of that up on the board?

A: Shortly.

Q: Pagerank for transactions?

A: It's a notion of centrality of the transaction. In blockchain, a transaction has a connection, we can calculate centralities up to the second depth, connected to the weighted address, we can add more weight that can be part of the address, and we can calculate the size and amount and distance from the genesis block. Ratio of changes of amounts. This can be a calculated effect. We don't know who own the addresses, and the auditor or regulator are able to screen which address has importancy and we are- that is my thinking.

# Smart signatures

Our table brought together Interledger's Crypto Conditions and petertodd's and mine's DEX for deterministic expressions. At the end of the discussion, we settled that they are compatible and we ought to make them work together. We got some additional requirements from crypto conditions that we will try to resolve with DEX. There is some discussion about bringing it to IETF in July in Berlin so maybe I will be going to Berlin after all to see whether there is any interest there. If not, then we might bring it to W3C.

Q: What was the discussio nabout?

A: Crypto conditions is a structure. DEX is a simple language. So the discussion was can we get their bitmask in the beginning to let you know that something has an RSA operation in the expression, or there is an ECDSA operation in there, do you support the bitcoin curve or whatever? Those things can be prepended to the structure that allows an evaluator to know that it doesn't even want to attempt to evaluate the expression, whereas in DEX you have to evaluate it to determine if there were things in it you might not understand.

DEX thing commits to the operations. Instead of pre-caching the parsing. But long expressions wont be too long.

# Security

..... We talked about TheDAO and governance and the implementation. Separation of hash and execution so splitting the different parts to make them hardened and secure.  Understanding the risk when you execute something, to have some sort of measure. We went back to Matsuo's slide which had different levels of the stack and it had the standards that you should apply to that layer in the stack. It was a great slide so we had a discussion about that. The stack had implementation and application and cryptography layers. So the outcome of this discussion was that we need to be able to have some implementation layer that can be tested, and cryptography can be evaluated and analyzed so that we have an assurance that the code is secure. We need more research to do a fine-grained analysis. Some parts of the stack are too compact and there's no way to evaluate it clearly. Fine-grained layering of the security stack would be useful. Finally, looking at, coming from the cloud world, we have organization like cloud security alliance which gives us a best practice in terms of security and we couldn't find an equivalent in blockchain. We thought it would be good if there were some initiative like that which would allow us to understand the way to implement security from day 1.

# IoT

The next steps could be, one is pretty clear that there isn't a good categorization of devices. There needs to be work to categorize those devices. There are probably many dimensions on how to do it. One could be by footprint and size, other could be by mobile versus fixed, third could be by longevity which is what I talked about in my slides, another could be spatial or temporal dimensions. This is an important body of work that ought to be done. The second is that, broadly phrased, the integrity of devices and transactions from a user interface perspective. The vision is that transactions would be happening rapidly, and how does a user keep control for stuff that should be reconfigured? And the third thing is, some of the key words that came up in the discussion was, and not all exhaustive, indexing, declaring, making data available in a standardized manner. I think that's another important body of work that is just missing. And a little bit related, is the whole area of discovery of a device, addressing a device, directory services, what's the equivalent of DNS for the IoT world. The registration of a device, provisioning, and a lifecycle standpoint should also be considered to organize all of these events and states.

There were some other sentiments expressed. What's unnecessary centralization? What's the right amount of centralizaiton when it comes to devices? Identity is separate from reputation or trust. Again different categories of devices. Different categories of devices would change that. Another one was delegation, the concept that for in order for things to scale, you have to deal with lot more devices than we might want to deal with on a one-by-one basis. Avoiding surveillance and considerations regarding surveillance. Pretty much I think that, that was kind of the overview of sentiments that were expressed.

# Lightning network

We were initially the table with crypto conditions but then we split up. We talked about interoperability like interledger and lightning network and how these networks on top of blockchains would look. There were some very differnet perspectives. Some people were from the crypto bitcoin blockchain side, and some others had more experience with traditional finance. There were some similarities with problems and how we deal with it.

What does the topology of these networks look like? Will they look like a star topology, or a well distributed graph? Do you want it to be a well-distributed graph? In the web case, it started off with everyone running their own servers, and now you have a very long tail and it's definitely a power law distribution where the top 10 sites get 90% of the total visits. There are reasons to look at this either way. We also talked about not necessarily how to make standards, a lot of these projects are not standards ready and they are not operational yet, still in development, but standards between ledgers, currencies and blockchains, and how to get existing financial institutions to say, we don't have a blockchain but we will accept some of the same crytpo conditions that a blockchain has maybe. Like saying yes we will move money if you give us a digital signature, getting a bank to say that now even ahead of blockchain integration would be really helpful for the upcoming massive migrations required by upgrades to these new technologies.

How can companies do risk management and how can the legal aspects work too? It's good conversation. A lot of the conversation was about how this could potentially work. A lot of this is still early.

Q: You say it's not ready for standardization. Would incubation help? Is it still in a phase where you are working on projects, or is it at the point where starting a conversation might lead down to 2 years down the road? We can prioritize things based on their urgency and readiness. We can also be thinking longer-term about how does this fit into the larger thing.

A: Standardization is important. Right now we're still trying to figure out what works. A lot of this is education.

As an admin note, if you have pages of notes or something, we will record those either by photograph or typing.

Q: You said, I thought it was important, you said you don't think some of this is ready. What would be ready? I would be interested to hear your sense. What are the aspects that you think seems not ready. It's easy to get caught up and moving forward with momentum. What are the signs that make you think it's not ready?

A: I think it was sort of the idea that you want things that are operational. You want a descriptive standard rather than a prescriptive standard. I am not experienced with W3C. It seems like that's the idea. A lot of these technologies are not being used widely. People are talking with companies, we are building things, but we have no idea what the network is going to look like. Let's see how it works in real life first.

We do have a W3C group focused on interledger. We are talking aobut a lot of these things on there. If oyu guys are interested in these types of protocols, then I suggest you use that group because we are interested in using the W3C structure for interledger's purposes.

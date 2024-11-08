---
title: Roundgroup Roundup 2
transcript_by: Bryan Bishop
---
# Communicating without official structures

Roundgroup roundup day 2

Hi guys, okay I am going to try to find my voice here. I am losing it. I ran the session on communication without official structures. We went through the various channels through which people are communicating in this community like forums, blogs, irc, reddit, twitter, email, and we talked a little about them each. There's also the conferences and meetings. There are different forms of communication in text than in person. It's a lot easier to read into things negatively when it's just via text. It way may not be intended, but people may assume negativity. One of our goals was, are there ways to encourage people to assume good faith?

We also discussed trolling. We noted that certain communities can establish a baseline whereby the general respect is such that you don't have a lot of trolling, and why we want to encourage that in this community. We discussed getting new entrants into this space, and we'd like to have core devs explain everything to everyone new in the community. We need better resources for new entrants to the community so that when they have a new idea when they join mailing lists they aren't shutdown, but onboarded into the community in a way where they don't need to be shutdown.

There can be mentorship, ambassadors that are not involved in core development but could explain to people just getting involved certain resources or certain forums to get up to speed. This depends on getting the right resources. Lastly we discussed a concept of not a code of conduct, but maybe a general rallying cry for a code of ethics or a statement that the community can collaborate on, for collaboration and treating each other with respect, we point to Wikipedia that has a community with that. It of course would be opt-in and look good when you sign it.

We should remind people about the human nature of the people they are communicating with. Their online interactions should include remembering that these are real people. We should get folks in the community to assume good faith and assume that people are well-intended, while not being less scrutinous. Several of us decided that we would write this rallying cry or statement and the point is to make it positive and encourage people to collaborate and be respectful.

# Payment channels

We were talking about payment channels. The initial topics were the soft-forks required for lightning network. Some of the changes that need to be made before this is usable, like checklocktimeverify (CLTV), a relativechecklocktimeverify (RCLTV). And the malleability fix is the trickiest, it's not that anyone disagrees- except that they do, ... it can get fairly big pretty quick. SIGHASH\_NORMALIZED might be nice. You might as well make a new signature type when you have a new sighash type. There's a lot of rider bills that want to go on. Normalized txid, no txid, don't sign your input at all which allows for some really fun stuff, so that's sort of the worry.

We also talked about usability of payment channels, not just be about layer-2, but what does the presentation look like to the user? We need to focus on the UX aspect. Once you hit a button on the phone, are the users even aware that they are using payment channels? Routing payments need to be solved too. Outsourcing- we can't expect users to always have a computer online at all the time. It has to be compatible. We can incentivize people to ... to stay online for them, delegates, maybe your friend broadcasts transactions for you, maybe you can broadcast old payment transactions to educate users about the security parameters.

Are we still going to use bitcoin addresses? Maybe another encoding. Maybe a wallet-to-wallet communication channel and a payment protocol like bip70 but not bip70. We want a well-connected graph for payment routing. You don't want a situation where there's a bottleneck in the graph. There should not be a small number of large nodes at the center of the network. You should optimistically connect to a lot of people and route things that way. What do you use for initial discovery? Probably an IRC channel, use some kind of DHT, maybe something from bittorrent will be applicable to this. How do you present this to some user? Some identifier at host?

Tor should be considered as the de facto transport. We can have locks around it because tor as a high-latency network would still be compatible with the timelocks. We didn't discuss timestop too much, there are sort of systemic problems that anyone channel is not such a big channel, but what happens if you have lots of channels going down at once? So having a timestop where you have a blockheight a real blockheight and then an adjusted blockheight that transactions could reference would be something that could prevent that. We discussed crazy edge cases that will almost never be a problem, but you still have to have a solution for them, because if you have a solution then it would definitely never be a problem so that nobody will ever try that attack.

A bunch of people are implementing these things and they should all bug Rusty Russell to prevent him from continuing. It's sort of annoying that there are incompatible clients. It's nice to have consensus here. We need to take the time and design these systems correctly. We need to make sure we don't take shortcuts or undesirable properties.

Lightning payments on average should be sub-satoshi because hot wallets are required and are extremely low security.

# Interfacing with W3C, IETF, etc.

What are some of the other organizations out there that we might want to be interacting with? Well we decided to hell with them. We decided there is value in talking with other groups out there. One of the first things that came up when we were talking about it was that we saw organizations with similar characteristics but they tend to self-organize around issues in the same way that we did at the roundtables to allow some more focused discussions happen and allow people to work in their areas of expertise. We should try to define the problems we have, like some of the networking issues and being able to more quickly blocks distributed across the entire network, these are the things that people have already worked through the problems on. The challenge that we have of trying to make sure the block gets everywhere very quickly is something that CDNs have worked with. We can learn from their experiences, this gives us a really good way to go into other ecosystems and do some spearphishing for some really good developers. If we go into a group of networking people and not mention bitcoin, then you can get them hooked on their own technology love rather than convincing them that bitcoin is awesome as a first step. This could be a really valuable way to do it. I think we have pulled some developers from linux and other places by doing exactly that.

The web consortium is going out and working on web payment standards, ensuring that we have representation at those meetings would be nice. We want them to build a bitcoin-positive way, and we should make sure the standards bodies understand our needs and what we can do.

Those were some of the big takeaway points. We should organize around problem topics, leverage that to work with other organizations without framing the problem as bitcoin.

# Perspectives and challenges on interfacing with China

We didn't have that many questions in the roundtalbe. If you want to do business in China, everyone in China uses weechat. You can use it to pay each other, use it to chat, it's like facebook, snapchat and uber all combined into one package.

What does the Chinese government feel about people mining bitcoin in China? As long as it gives the government some benefit to have bitcoin, they'll do it. They have a panel of advisors from research institutions advising them on what they should do with bitcoin and cryptocurrencies in general.

What about the block size issue? They don't really understand technical aspects of bitcoin, they just want you guys to make a decision. Chinese miners just want to go with the flow. Tell us what your decision is. So at the end of the conference they were asking us what the decision was, have they decided?

Latency is an important parameter for Chinese miners with regards to the miners.

# Systematizing knowledge

Hopefully we have been making a lot of knowledge here today, perhaps it's Zero Knowledge but it still counts.

The problem over the past few years was that we have an enormous amount of ideas and original research and this isn't very organized. We have bitcointalk, reddit, IRC, various development mailing lists, a new mailing lists on linuxfoundation.org, and it's difficult to index all of this. It's also difficult to bring new people into the bitcoin community because it's difficult to point them to anything to navigate themselves to figure out how to get up to speed. There's a few different targets for outreach and documentation.

We have several groups that have different requirements: developers, miners, users, professionals from other industries, policymakers and regulators, academics in university and researchers, and we need to take a different approach in providing all of these people.

There are problems with organizing information on IRC. There are big bottlenecks in producing content, especially around Bitcoin Core development. Often there's only one person that knows what's going on, and often it's the same person. Often the answer is "go answer person X" and person X is then completely swamped. This is a bottleneck that needs to be improved.

The organization is also important. Things are very spread out. Looking towards solutions, we talked a lot about hiring technical writers. How do we get more developers? Let's try to hire technical writers. There's more writers out there than there are more developers out there. They are probably a bit cheaper too.

What ideas can we copy from academia? Academics hate the way that peer review works. It's very slow. It's very formal and hard to work with. There's some good consequences of the academic peer review process. One of these is that if you want to find a new idea, there's only one place. You can do a journal search and you'll find it, plus any responses or any refutations if anything was wrong. There's also a culture in academia of formatting your proposals in a certain way, including how your proposal is new and how it is different and what the related work is, and what the idea is that you are contributing. It's taboo to fail to cite or taking credit for something you didn't do. This is sort of missing in bitcoin to a large extent; just random posts to reddit and blogs. This contributes to the difficulty in organizing information. We would like a way to encourage a culture of producing new ideas and describing new ideas in a way that is amenable to finding them and finding related work and finding how they fit into everything that is going on.

# Non-currency applications

There were a lot of contentious areas where people don't exactly agree or have a shared view on what's going on now or what the future will be. We tried to pin/pen a few things down, we tried to figure out what about bitcoin applies well to non-currency applications. There are information technology properties, like availability and integrity. We talked about general areas in applications today like notaries, timestamping, copyright, arbitration, identity management, loyalty points, asset management systems.

We're thinking about applications with trustless timestamping, stake consensus, we weren't able to agree on any core categories. We talked about a number of different methods. We also talked about possibilities of various different applications with different levels of security required and various options to poo all over the blockchain versus higher security and more expensive for others. That about covers it.

# Network events and planned responses

Network partitions, the block size halving coming up, and failures of centralizing such as what if Coinbase collapses or there's a major hack or something. Disaster notification kind of like when the hard-fork happened in March 2013. How do we get people notified and get them on it as fast as possible?

When the network partitions happened, we were really talking about what happens if China shuts off all bitcoin communication? There's going to be the China side of the network, or maybe the hashpower will be even and there's going to be a reveal where one side is 16 blocks ahead and one side is 18 blocks ahead. And maybe the 16 blocks will still keep mining on the chance that they might get ahead in the future. They aren't going to give up 16 blocks of rewards just because the other side is 2 blocks ahead.

If one side has much more hashrate than the other side, then the side without hashpower, they are just going to freeze. Confirmations are going to be meaningless, and you have to get the transactions across the network. You can setup multiple jumps and jump a network partition or use SMS or some form of steganography to get over the firewall.

For the block size halving, there's a lesser problem which is that the final 25 bitcoin reward block is going to be more attractive to mine than the first 12.5 coin block, so miners will never forward and they will keep mining and keep trying to steal that 25 coin block. If this gets really bad, we can have someone just make timelock transactions that are a few blocks in the future and incentivize miners to move past that one block reward. I think that would resolve quickly and require specialized software and I don't think most miners are going to implement that.

The more interesting problem is that the reward halves and the difficulty does not. Where the electricity is the most important expensive cost in mining, then suddenly it wont be profitable. So all the miners shut down at the same time, which would be a disaster because the chain grinds to a halt, so how do you get around that? Hoping that miners stay on, beg them to take a loss for 2 weeks until the difficulty adjusts? Or do a kickstarter with transactions with high fees? But then we realized that miners have fixed electricity costs or are even fined if they don't use the full $20k/mo megawatt. They pay a penalty for not consuming their electricity. Some of these costs are fixed or something. Miners might eat it for two weeks because their costs are already fixed, so large farms do not benefit from shutting down their miners for such a short period. So this probably wont be a huge issue.

Decentralization failures- there sohuld be some sort of process for responding to these and be prepared for some service to bring a bad name to bitcoin. And there is talk about exchange failure and preventative modes, like proof-of-reserves, which isn't that valuable because I can just buy a signature from soneone and give them $100 and then they give me a signature that says I own $1k bitcoin. Proof-of-reserve can be faked using collaboration. I think the best alternative is to combine cryptography and government regulations to protect from centralized service failure.

The notification system, what happens if something out of the blue goes really wrong, how do we get ... there's no phone number tree for contacting everyone. I think that from a federal perspective, regulators would like to know that the ... we need to get everybody on board in a few hours. We need an emergency mailing list.

There's a good track record on previous disasters. On the recent fork we had everyone online and talking within a few hours. I think that we just need to formalize this to make other people feel better. I think the system we have in place does a good job informally.

# Challenges for major protocol changes and their benefits

We started talking about hard-forks versus soft-forks, then we saw that major changes that can be soft-forks and minor changes that can be hard-forks. A hard-fork makes a change more major because it requires far more coordination. And then we talked a lot about different proposals and mostly we spent a lot of time about the challenges of getting proposals through, and then we started listing changes, and then particularly what would be blocking them and what would the rewards be. It's on the whiteboard paper in the back after this you can go take a look. I'll cover some of the common themes.

The benefits are usually either that they make some feature set work like sidechains, SPV stuff, blockchain pruning, or they increase performance of bitcoin, like make more transactions per second, faster signature verification, and then kind of pretty uniformly the challenges had to do with the fact that there isn't consensus in the community and everyone involved as to whether the change to go through. Sometimes the incentives are not clear because what are the results of changes?

So it makes it hard for the community to agree for whether a change should be proposed or even agreed about.

# How can we get 10x the number of "core" contributors?

crescendo

This is not a linear scaling problem. We actually drew a lot of parallels between the early time in Linux and what has happened in the bitcoin community. You have large entrenched powers that are responsible in Linux but they were originally UNIX companies really. The big banks are sort of the parallel. We talked about problems like the industry, the parties interested in bitcoin and blockchain. They are not prioritizing contributions back to the core software. There are only two companies that are responsible for hiring, with the other notable addition of MIT DCI and previously what the Bitcoin Foundation did.

We were thinking of asking newcoming professionals to hire dedicated developers that is responsible for contributing back to the Bitcoin Core developers. Hire technical writers to encapsulate these ideas and get them into simple clean formats that are more easily understood by developers and others alike with a wider range of skill sets.

We talked about this other problem where there isn't enough talent out there, developers are already in extremely high demand. With bitcoin it's doubly high demand, it's proficient developers plus cryptography knowledge, that's doubly more difficult. We suggested industry companies investing in the community by sponsoring mentorship, hiring interns and providing internship, take someone under your wing and provide mentorship and guide new people. This is a start but doesn't get us to 10x.

There's also a lack of modularization in the Bitcoin Core codebase. It manifests in a number of different ways. There are existing efforts. When you have such a small coupled system, it's hard for one change to not impact other parts of the system in unexpected way, there's also libconsensus but more effort needs to be put into breaking this system out. Other developers can then contribute and provide contributions without breaking other parts of the system.

We obviously talked about communication problems and this has some ways of manifesting which is that the information out there and available is duplicated, incorrect, and we need to make an effort to consolidate a lot of this information, and one of the best ways we found of doing this is the bitcoin wiki. This has largely fallen into decay. It would be beneficial to increase community effort to document conversations in bitcoin-dev, bitcoin-wizards and stackoverflow and getting the useful chunks of information to go read it without wasting someone's time for the 100th time or something with the same old questions.

There's also the importance of reducing the information down to something consumable. It has to be simpler. Developers that don't have deep expertise should at least be able to see the nuances and complexities so they can have perceptual understanding or insight.

There's also something to be said for face-to-face meetings, including smaller events. We need to see the SF Bitcoin Devs meetup in other locations. These are important conversations to be had. Looking someone in the face changes the nature of the communication.

We need more mentorship, and we want to make a call to industry players to actually make a commitment to invest in the future of bitcoin. This is not just one year returns of profit. This is massively important. If you invest in the bitcoin community, the bitcoin community will become stronger as a whole which is absolutely necessary for the long-term success of the projects.

There are also parallel communities like altcoins such as litecoin, ethereum and dogecoin, these provide low-risk ways for new developers to get involved. Also these are probably false flags to recruit new developers. We shouldn't poach developers from each other. And we should poach more Linux kernel developers. We need to reach out to parallel communities and get them more involved.

Also, we talked about how to encourage developers to participate. We need more people to offer jobs to developers that want to work on bitcoin stuff, but also this unified vision that we're all building a better vision and that we are all working on this. We should show people that the vision is without centralized systems and without censorship, the value loss that is taking place, the middlemanship then even more developers will get involved and most people aren't aware of that.

I want to highlight MIT's program, if you are interested in offering mentorship to students or other individuals, please email bitcoin@mit.edu because they are actively looking for people to provide mentorship.

# Sustainable financing

Patrick Murck

Thanks for organizing this. This conference reminds me a lot of San Jose in 2013. The first big Bitcoin conference which set the stage for a tremendous series of events afterwards that really grew bitcoin in general. So this is a great show.

So how do we fund bitcoin in a sustainable way? Bitcoin development and infrastructure. We want to put some parameters around that. You can easily find yourself in a space where you are trying to boil the issue. Let's cut out marketing and policy and so on, because those aren't essential to operating and running bitcoin. What are the absolutely critical aspects? Well, full-nodes to propagate transactions. Miners, protocol maintenance making sure the uptime of the network is there. Core developers who work on maintaining the protocol and the software and network, and also improvement as needed to keep things moving forward.

How do we measure this? What are the true costs of operating these full-nodes? What about the costs of developers? Once we have figured out the costs of maintaining what exists today, then what is the cost of improving it even in marginal ways? If we can measure what the true costs are, even the costs of making improvements, how are resources being currently allocated, and how are we resourcing the resources anyway? The mining ecosystem had the incentives built-in. But other infrastructure is not incentivized, like full-nodes. We had a great presentation about incentivizing full-nodes. We kind of left that up in the air for whether it should be a financial incentive.

Is money the right way to fill that gap? Technical writers we have heard that two times early, but those are hugely important. We can fill that gap. Technical writing isn't very sexy, but that can be funded. We talked about filling in that gap by creating a culture of giving back. We've talked about this before, but the companies that are funded that have got VC funding or miner revneue or whatever, developing a culture of giving back, whether running full nodes or incentivizing full nodes, or lending out your developer resources, those are some of the ways that the companies can give back.

MIT is a good example of this, but we should leverage academic institutions because they have different resources that are generally available and we have wondered around why every academic institution isn't yet running a full node. There are over 50,000 institutions out there. The NSF is giving out grants, perhaps they could get grants for running full nodes. When companies are raising money, what is giving back going to look like?

# Scalability of wallet technology

One of the first things we talked about was separation of wallet from Bitcoin Core node activities. The idea of reusing the Core software within other wallets, the ability to embed the core ode in other wallets, the idea of having standard interfaces and the importance of running a full node. Everyone should be running a full node. Perhaps there should be a storageless full node on your router device. We also discussed whether SPV is going to stay. How can we incentivize the use and development of SPV? The issue of SPV with privacy, security and the fact that you're not really part of the network, you're a leaf and not participating. We discussed the issue of the number of nodes.

We also discussed what happens if we have 50,000 new nodes. Can the network handle that? Are those nodes going to start sinking and take the network down?

We discussed the idea of oracle services having standard interfaces for multisig, the idea of blockchain API companies having standardized APIs between each other. It's hard to have customer service with open-source software, so are we going to have some Red Hat model, how is it going to work for software? Today most of the companies that offer wallets go beyond their applications in order to support the customers. Is that how it's going to work in the future?

---
title: Zerolink Sudoku - real vs perceived anonymity
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Yuval Kogman
---
<https://twitter.com/kanzure/status/1171788514326908928>

# Introduction

I used to work in software. I transitioned to something else, but bitcoin changed my mind. This talk is a little bit of a work in progress. This was started by a guy named Aviv Milner who is involved with Wasabi. He roped me into this and then subsequently became unavailable. So this is basically me presenting his work. It's been severely ....... as I said, Aviv started this project, he defined the research questions and then became unavailable so I'm here presenting in his stead. He also arranged for funding to be provided for me by zksnacks, the company behind wasabi. I have no formal qualifications, I am just a confused code monkey.

The title is a misnomer. The sudoku bit is still a work in progress, the idea of solving associated inputs and outputs. I am apprehensive about saying anything about real world anonymity.

# Agenda

With that aside, the outline of the talk is going to be a few minutes to introduce Wasabi and what it is and what it's for and how it works, then we're going to look at some transactions made on the blockchain and then if time permits then we have some thoughts about future directions.

<https://github.com/nothingmuch/zerolink-sudoku>

# What is wasabi wallet

Wasabi is an open-source desktop wallet that has a key feature called Chaumian coinjoin which is a specific type of non-custodial mixing strategy for bitcoin. It was first released last year. The beta release was August last year, the final release 3 months later.

# Privacy

When I talk about privacy, I am referring to on-chain leaks of activity and net worth. This is a multi-faceted subject and I'm deliberately using a very narrow definition of privacy. It's narrow even in the context of bitcoin. I'd like to refer you to the fantastic writeup on privacy on the bitcoin wiki for something comprehensive and well-rounded.

# Bitcoin whitepaper on privacy

The bitcoin whitepaper just for historical interest had a statement on privacy. I think this is a naive take on what it means to be private.

# Fungibility

The second term I'll be using a lot is fungibility. By this, I mean the units of some currency are interchangeable with one another due to their indistinguishability. This is a very important property of money that Wasabi tries to promote. We're going to explore how it does that.

# Censorship resistance

It's important to distinguish between censorship resistance as part of the network and resistance in terms of unaccepted by the recipient in terms of fungibility. There was another joinmarket post on <https://joinmarket.me/blog/blog/the-steganographic-principle/> which talks about the potential of bitcoin to talk about hiding data and also it gives a fantastic overview of just the various tradeoffs betwee nscalability, privacy and security.

# Bitcoin transactions

We can think of bitcoin transactions as creating outputs, where outputs are just an amount and some opaque condition for how you spend it (the output script). In particular, this is going to be, we can think of it as a sort of bipartite graph between transactions and outputs that is directed forward in time even if this isn't how it works under the hood.

# Privacy and fungibility challenges

The typical bitcoin transaction is quite problematic for both privacy and fungibility because an adversary can make easy inferences about which output belongs to whom. The properties of what it takes for a transactio nto be valid; there's a lot of public information. All the amounts are completely open, the relatedness of all transactions is completely transparent to anyone who wishes to validate the data, and the cryptographic identifiers associated with all this activity are again.... and you can see the public keys and signatures. So in a sense, bitcoin is trivially non-fungible because literally every coin is uniquely identifiable on this graph. It also means transactions leak a fair amount of confidential information, especially to counterparties who can make inferences about which outputs are yours and what your prior or subsequent activity after you transact with them.

# Early research

These problems were fairly obvious early on. There was a lot of early research on this all the way back to 2011. There were a few papers that I first found:

* An analysis of anon....

... these heuristics trace back to the whitepaper.

# Common ownership heuristic

The common ownership heuristic is that when you see a transaction, all inputs are assumed to be owned by a single entity that produces the transaction unilaterally. This is not technically true, but it's a common assumption to make when analyzing activity.

# Change identification heuristic

The change identification heuristic can identify which outputs are payments and which outputs are the change output sending back to the payer.

# Coinjoin

This motivates what coinjoin is for. A coinjoin is a technique for creating bitcoin transactions that is based on the idea that inputs are signed independently but the transaction is only valid if all inputs are signed. Transactions are atomic, but they don't have to be the product of a single user. They can have multiple participants constructing them collaboratively. The second observation is that within the scope of a single transaction, if there are outputs with identical amounts then those are in some sense fungible within that very narrow scope of that transaction. So there's some caveats to that, but the goal is to kind of utilize these two properties to create privacy.

This is gmaxwell's post on bitcointalk.org is where I took this image from. This is an example of a coinjoin transaction. The idea is that you cannot attribute the inputs to the outputs at least not unambiguously.

For historical interest, this idea dates back earlier in various forms. The author of Wasabi-- zksnacks-- has a nice little overview of the history of this.

# Some coinjoin implementations

There's some coinjoin implementations. The dominant one is joinmarket, which is a p2p market. Takers create coinjoin transactions by buying offers from makers. So makers put up coins, and then takers use those coins to create transactions that obscure the traceability of the taker's data. The makers are not fully anonymous in this model since they do publish offers. In practice, they do gain privacy as well.

The two other coinjoin dominant implementations are Wasabi and Samurai both of which use a Chaumian coinjoin protocol.

# Coinjoin and privacy

Are coinjoins actually private? I would say yes, but with serious caveats. The problem inherently lies in the connectedness of the graph and the transparency of the amounts. You have to be very careful about how you're going to go and consume the outputs of coinjoin transactions, whether or not you're linking them together in a subsequent transaction reveals information.

You also have to make an assumption that you're not mixing only with malicious entity, or in particular one malicious entity who is pretending to be multiple entities, thereby being able to recover all of your activity.

# Coinjoin and fungible

It remains to be seen if coinjoin promotes fungibility. We could argue that all privacy tech could help fungibility in principle, in that it obscures information on the blockchain. But in practice, it often ends up identifying the subgraph of a transactions that actually utilize privacy tech, necessarily restricts the total population of users and therefore the anonymity set. So in effect, you often have a smaller anonymity set in some circumstances. For fungibility, those transactions are clearly identifiable by the patterns they leave.

# Coinjoin research

* Coinjoin sudoku, Atlas K 2014
* Anonymous alone? Measuring bitcoin's second generation anonymization techniques (2017)
* Anonymous coinjoin transactions with arbitrary values (2017)

Moser has publsihed a number of papers about bitcoin anonymization. There's also a bit of research into how to do better coinjoins I guess for lack of a better term. As it stands right now, you should know that only coinjoin transactions with identical outputs are actually deployed and used effectively although in theory the property that the amounts are identical is not strictly necessary.

# Chaumian coinjoin

Chaumian coinjoin-- zerolink is the name of the protocol that Wasabi wallet uses. The idea here is that a server helps a number of users to collaboratively build a coinjoin transaction without the server being able to identify which output is associated with which user, or which input. Both Samurai and Wasabi give heritage here. If I'm not mistaken, the authors collaborated on the original spec.

This utilizes blind signatures, which are normal digital signatures with an additional property that they contain a blinding factor that allows a signer to create a transaction without seeing what they're signing and then later it is possible to verify those signatures with respect to the unblinded message.

Here's the verification equation in case anyone is curious.

# Simplified protocol

Wasabi uses Schnorr protocols on bitcoin's secp256k1 curve. The actual protocol as implemented is an HTTP-based API. The roles here are Alice and Bob which are both the same user and there's many such users. Here in this interaction diagram, we can see the protocol going as follows. Alice connects to the server. Alice checks whether coinjoins are being built right now and if so what amounts are necessary. She then submits her inputs and blinded outputs. The server verifies that the inputs are valid, and can use ... in such a transaction, and returns a blind signature on that output. After all participants have signed up and the round moves to the after registration phase, Alice reconnects under a new tor identity Bob, and submits her unblinded signature provided by the server. This allows the server to validate that Bob did indeed participate as Alice without knowing specifically who Bob is. After all users have submitted their outputs, the server creates a signed transaction, and finally if they see all their outputs are represented faithfully, they then sign the transaction and it's broadcasted.

Any questions so far now that we have this out of the way?

# Obtaining wasabi subgraph

We were going to use blocksci but we ran into some issues, so we have a homegrown solution using electrum. The data is a subgraph of the entire blockchain. We first downloaded all transactions that look like coinjoins and spend to the wasabi fee earning address. We downloaded all transactions associated with any scripts specified in those transactions, in order to look into address reuse.

There's just over 5,000 transactions with an average about 100 outputs per transaction. A total of about 46,290 BTC ... 117,000 BTC. Now I will go to some graphs.

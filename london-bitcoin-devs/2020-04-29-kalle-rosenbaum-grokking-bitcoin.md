---
title: Grokking Bitcoin
transcript_by: Michael Folkson
date: 2020-04-29
speakers:
  - Kalle Rosenbaum
media: https://www.youtube.com/watch?v=6tHnYyaw0qw
---
Slides: http://rosenbaum.se/ldnbitcoindev/drawing.sozi.html

Book: http://rosenbaum.se/book/

# Intro (Michael Folkson)

Welcome to this London Bitcoin Devs online. We will be joined by Kalle Rosenbaum, the author of Grokking Bitcoin. In terms of London Bitcoin Devs you can follow us on Twitter at ldnbitcoindevs. We have a YouTube channel where we have a bunch of presentations from the last two years from people like John Newbery, Matt Corallo and Andrew Poelstra. Check those videos out. We are also looking for future speakers. If you are Bitcoin developer or a Lightning developer get in touch and we will see what we can do in terms of either doing a Socratic Seminar or a presentation or maybe both. We did have a Socratic Seminar last week. The transcript is [here](https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-04-22-socratic-seminar/). That was a really interesting discussion. Maybe during the Q&A we can continue some of those discussion threads. In terms of Kalle’s presentation you will be able to ask questions during pauses in the presentation. Apart from the pauses everyone will be muted. There will be a Q&A afterwards. Kalle will be focusing on Chapter 10 which is SegWit. But in the Q&A feel free to ask about any of the content in Grokking Bitcoin. If you are not on the live call you can ask questions on Twitter, comments in the YouTube video or on IRC. We have a channel \#\#ldnbitcoindevs. Let’s get going. We are live-streaming on YouTube so anybody on the call please behave yourself.

# Grokking Bitcoin (Kalle Rosenbaum)

I am going to talk about my book Grokking Bitcoin. I will do that in two parts. The first part will be a meta part where I talk about myself and also about the book and what you can expect from it. The other part will be a deep dive into one of the chapters which is Chapter 10 on Segregated Witness or SegWit.

# About

First I will talk about myself. I am Kalle Rosenbaum. I like to lay on a bed of Easter Lillies reading a good book. If you want to reach out to me you can do on that Twitter kallerosenbaum. You have my PGP fingerprint there as well.

# Grokking Bitcoin

Let’s talk about the book. Grokking Bitcoin is a look under the hood of Bitcoin. It explains how Bitcoin works technically and how it achieves censorship resistance which is a very important property of Bitcoin. Who is this book for? It is for technical people. Technically interested people, people that need to understand Bitcoin at a deeper level because they need it for their business needs or they need to gain better trust in the system because they want to maybe invest in Bitcoin. To do that they need to gain more trust in the system. This is one way of gaining that trust. Or maybe you are just curious. These tech people, they don’t need to be developers. There is no code in this book at all. But it is also great for devs because I teach Bitcoin with very few analogies. It is plain Bitcoin. I describe the data structures as they are. I describe the algorithms as they are. I just don’t do it with code. I do it with concrete examples and lots of illustrations. This is a book that I would have loved to read when I started out. I am a long time developer so I would have loved to have started with this to get a very good understanding of the concept of Bitcoin before digging deeper into code. This book started out in 2016 when the publisher Manning contacted me and asked me if I wanted to write a book about blockchain. It was peak blockchain back then. I answered back and said “No but I would like to write a book about Bitcoin.” We started negotiating terms then. One of the requirements that I had for this book was that it should be open source. They agreed to that. It is now open source on GitHub under Creative Commons license. You can’t read the book on GitHub because you won’t see the images. You need to build the book before reading it. To make it easier I have made a build myself that I put up on my [website](http://rosenbaum.se/book/). Please head over there and have a look if you want. It is a great way to try before buy. If you want to buy the book it is available on Amazon or any other major book store. As well as Manning’s [web page](https://www.manning.com/books/grokking-bitcoin).

# Foreword

I also want to brag about the foreword that is written by the excellent David Harding. David Harding is a technical writer. He writes about documentation for Bitcoin and also contributes to bitcoincore.org. He is also a major contributor to the Bitcoin Optech newsletter that is sent out every week. I recommend that everyone reads that newsletter. It is great from a technical perspective.

# Translations

The book is also translated into a few languages. The translations for German and Japanese are finished. The German translation is done by the great Volker Herminghaus who did this in a very short time and he did it open source. This translation is part of the source tree on GitHub. There is also a commercial Japanese version now which came out in March. There are several other languages in the making, still trying to finish Finnish, Spanish, Portuguese, Russian, Polish.

# Structure of the book

Let’s talk about the structure of the book. The book contains eleven chapters and a few appendices. The first chapter Chapter 1 is your typical overview of Bitcoin. It describes why Bitcoin matters, why censorship resistance matters and how Bitcoin operates on a very high level. Chapter 2 introduces two very important concepts in Bitcoin. That is cryptographic hash functions and digital signatures. It also sets the stage for the rest of this book by creating a very simple payment system or money system that we call cookie tokens. You can use these cookie tokens to buy cookies for example at the cafe. The cookie tokens are being tracked in a spreadsheet that only one person has write access to. Everybody can read this spreadsheet but only one person, Lisa has write access to this spreadsheet. When John wants to buy a cookie from the cafe he asks Lisa to move ten cookie tokens from him to the cafe. Lisa does that by adding a row to this spreadsheet. Of course this spreadsheet has a lot of problems. You can’t use this as global censorship resistant money. We will chapter by chapter add Bitcoin tech to this spreadsheet. In Chapter 8 we will end up with Bitcoin. Chapter 3 changes the names that you saw in the spreadsheet with public key hashes to make this spreadsheet more private. Chapter 4 adds the concept of a wallet that manages the keys for you and also standardizes a message that you send to Lisa. But Lisa still updates the spreadsheets just as she did before. One problem here is that Lisa can easily steal money. She can just change anything in this spreadsheet to increase the amounts for her for example. That is not very good. In Chapter 5 we introduce the concept of a transaction. We change the spreadsheet into a list of transactions and introduce the concept of a transaction. Now everybody read this list of transactions and the transactions as we know contains the signatures. Lisa can no longer steal money by changing data in the transactions. But she can delete transactions from this list without anyone being able to prove that she did. In Chapter 6 we introduce the blockchain or rather a blockchain. This is not “the blockchain”. In order to stop Lisa from deleting transactions Lisa now has to collect transactions into blocks that she signs with her private key. And publish those blocks to a shared folder. I will go back to this shared folder in a moment. But this way since the blocks are signed by Lisa’s private key she can no longer remove transactions from blocks without being proven a fraud. This still has problems because Lisa can still prevent transactions from entering the blockchain in the first place. She can still select which transactions to add to the blocks. She is still a central point of censorship here. In Chapter 7 we fix that by introducing proof of work. With proof of work anyone can become a Lisa. Anyone can become a miner and create blocks and put them in the shared folder. This means that if Lisa won’t process my transaction I am sure somebody else will. We are heading closer to a censorship resistant system here. But there is still a problem. You remember the shared folder. It is time to get rid of this shared folder. There is a shared folder administrator that has ultimate access and power on what can enter the shared folder. The shared folder administrator can censor blocks. To stop that from happening we create this peer-to-peer network where block producers now publish their blocks. A block producer will probably publish it to multiple peers who will then verify them and relay them to their peers until everybody has the blocks. This is pretty much Bitcoin we have created here. From this point forward we discuss only Bitcoin. We leave the cookie token system from now on. This is Chapter 8. The last part of Chapter 8 discusses how you install or start your own full node. It also includes a tutorial on how to do that on the Linux command line. That is as close to source code we get in this book. There are three more chapters. Chapter 9 is more about transactions. We pick up where Chapter 5 left off. We talk about replace-by-fee, sequence numbers, CheckLockTimeVerify and stuff like that. Chapter 10 is about SegWit that we will dig deeper into in the other part of this talk. Chapter 11 is about Bitcoin upgrades. It talks about soft forks, hard forks, deployment mechanisms and how certain features were deployed in Bitcoin.

Q - How much did you dog food this book? I think most of the people on this call have probably been into Bitcoin for a while. But especially with the intro stuff how many people did you get to go through the basics of Bitcoin and what was their feedback? Did it require any iteration?

A - Manning was very valuable there. They provided me with a lot of reviewers. I wanted reviewers that had little to no experience in Bitcoin before. I wanted technical people but preferably not Bitcoiners. They provided extremely valuable information back to me. We did quite a bit of revision there. I also had certain chapters out to different experts. I had a cryptographer looking at my cryptography explanations and people looking at Chapter 1 to make it accurate enough. Quite a bit of revision there.

Q - It sounds like you did a lot of work to ensure the accuracy but did you get some beginners to go through the content and see how useful and accessible it was for new people?

A - We had thirteen reviewers from Manning.

Q - I haven’t got through the whole book yet but it is brilliant. How long was the process from start to finish to pull this together?

A - It took ages. Two and a half years probably. Manning contacted me in autumn of 2016 and it was published about a year ago now. It was a pretty tough process. The writing phase was like one and a half years. The production phase was pretty extensive with reviews and with type setting and copy editing. That process was a nightmare actually. But the end result was great. I am actually quite glad it took that long because it wouldn’t be this good otherwise. We also had problems with the first illustrator. I did the drafts for the illustrations. Then a professional illustrator redid them for me. The first illustrator wasn’t great so we lost several months there trying to get him onboard. But eventually we changed to another illustrator. We lost a few months there. That was sad but the end result is great so I am happy we did that.

Q - Do you intend to see this as a work in progress? As Bitcoin evolves do you intend to add to it?

A - Not really. Maybe I will do a second edition of this book. It is not in the making right now. We will see what happens. Right now I am pretty pleased with not writing. We will see what happens in the near future. I can’t say anything about that now.

Q - At what point did you get into Bitcoin Kalle? I saw your name was referred to in a Scaling Bitcoin presentation back in 2015. You were into Bitcoin pretty early?

A - I talked about something called IBLT, Invertable Bloom Lookup Tables. I presented some work I did together with Rusty Russell. We presented together there at Scaling Bitcoin. That was very fun and very interesting. It had to do with improving the efficiency of block propagation with a certain data structure that we call IBLT.

# Grokking SegWit

The second part of this talk is about SegWit or segregated witness. That is covered in Chapter 10 of the book. I will do that by presenting a problems and the solution to that problem. There are several problems that SegWit solves. I will focus on just one of those problems. Please refer to the book for the rest of the problems. The problem I want to talk about in legacy Bitcoin is transaction malleability. You probably heard the term several times. To malleate something means to deform. You can mallet a sheet of metal for example with a hammer. That is the same as what happens in Bitcoin with transaction malleability. Suppose you have a wallet and you send out a transaction Tx2 in this example. You send it to Tom’s node and Tom verifies it and sends it to his peers. But there is a problem here. Qi’s node is a malicious node. Qi does everything she can to make your life miserable. What Qi does is take this transaction Tx2 and makes some subtle changes to this transaction without invalidating the transaction. She can make some small changes to the transaction and then she publishes or forwards the malleated transaction, the changed transaction, to her peers. Now we have two transactions floating around the network. We have Tx2 and Tx2M which is the malleated version. These two transactions are extremely similar. They spend the exact same coins and they send the coins to the exact same addresses with the exact same amounts. That might not seem like a problem you might think. But there are problems with this. I will come back to why this is a problem soon. Right now I will focus on what Qi has done to this transaction or what she could do with this transaction. To do that we will closer at Tx2. In this example where the transaction looks like this. I usually draw transactions like a rectangle with a vertical bar in it. To the left of the vertical bar are the inputs and to the right of the vertical bar are the outputs. This particular transaction has only one input and one output. So what can Qi do now to malleate this transaction without invalidating it? The only known way to do that is to modify stuff that is in the signature script. The signature script is the stuff here which you see within the bracket. In this example the signature script consists of a signature and a public key. If we look closer we see that the signature is in a way encoded by let’s call it the signature container. It is encoded in a certain way. You have the signature container containing a signature and you have a public key. I am going to present three different ways to malleate this transaction. There are others but I will show you these three clauses. The first thing Qi can do is alternate the encoding the signature or the container format. There are a few different ways you can encode the signature that are all valid. You don’t change the signature itself, just the encoding of the signature in the signature script. Another way to malleate the transaction is to apply some cryptographic tricks to the signature itself. There is at least one such known way to do that which you can apply to the signature itself without invalidating the signature. The third thing I want to mention is that you can add operations to the signature script that together does nothing. In this example we add OP_DUP followed by OP_DROP which means duplicate the top item on the stack and then drop it again. This is together a NO_OP so it doesn’t change anything in the script but it changes the transaction. Now we have the possibility to malleate the transaction. Why is that a problem? The transaction still does the same thing. It spends the same coins and it sends the coins to the same outputs. So why is it a problem? To understand that we need to understand the concept of transaction IDs. This is from Chapter 5 but I reiterate it here. A transaction ID is calculated from the whole transaction including the signature script. If you malleate anything, if you change anything here in this signature script you will also change the transaction ID because the transaction ID is calculated by hashing the whole transaction including the signature script. Changing the transaction will cause a change in the transaction ID. Why is that a problem? That might oftentimes not be a problem. For simple payments if another transaction than an the intended one gets confirmed it is not usually a problem. It might cause a little confusion for the wallet but you still have your money safe. But payments aren’t always simple. Oftentimes you need to create chains of transactions before publishing any of the transactions. For example, when you set up a Lightning network channel for example you need to first create the funding transaction. Let’s call this Tx2. You create that transaction but you don’t publish it yet. Then you create Tx3 here which spends the funding transaction and sends the money back to you somehow in case of a dispute. When you have created Tx3 safely then you dare to publish Tx2. As you see here I draw hashes like this, a pile of paper. This transaction uses the transaction ID of Tx2 to refer to Tx2. Tx3 references Tx2 via its transaction ID. Suppose now you have created those two transactions and you then decide to publish Tx2. You publish Tx2 and this happens. Qi malleates your transaction. There are two transactions floating around the network and you end up with this unfortunate situation. The malleated version of the transaction is the one that gets confirmed in the blockchain. As we know the malleated transaction spends the exact same coins as the original transaction which means that Tx2 now is forever invalid because it spends coins that are already spent by another transaction in the blockchain. That means Tx3 is also invalid forever which means that this whole contract is totally broken because of transaction malleability. Let’s recall why this is a problem or why this occurs. This occurs because changes in the signature script causes the transaction ID to change. This is the problem part.

Q - I remember first hearing about transaction malleability back in 2014 when there were quite a few funds missing on MtGox. Mark Karpeles at that time claimed that transaction malleability was to be blamed for the loss of funds. Do you have any comment on that? Is that a plausible explanation?

A - I would rather not. Maybe it is plausible. I don’t know. I’m sorry, I can’t comment on it. I remember the discussion but I don’t remember any details at all.

Q - In this example we now have two invalid transactions. Does that mean the funds are now locked?

A - Yeah they are. Tx2M now contains the funding output but if me and my partner cooperate on reclaiming those funds we are good. But if my counterparty won’t cooperate with me the funds will be lost. It is very important that the events happen correctly.

Q - This has occurred a lot in the past?

A - Transaction malleability has occurred a lot in the past because it was very easy and cheap to set up a rogue node that just malleates for the lulz. I don’t think it caused much economic damage but it caused confusion of course. It caused a vivid discussion on transaction malleability and various ways to prevent it.

Q - It was just malicious attacks. There was no benefit other than damaging Bitcoin. Is that right?

A - I can’t speak whether there was economic damage. Maybe there was I don’t know. One little detail. These are the three ways to malleate the transaction but I forgot to say that this first way to do it is fixed by now. It is fixed in BIP66. There is a new consensus rule that prohibits this. The other two are still possible to do but they are limited somewhat by policy rules in the nodes. A node won’t relay a transaction that does this. But a miner can still do this. Back in the day you had no policy rules against this.

Q - Lightning is one thing that really needed a solution to this transaction malleability. Any other constructions or any other projects that needed this problem to be solved?

A - I think most complex constructs will be easier to perform without transaction malleability. Most contracts will actually gain from it either because they suddenly because they become possible or they become more easy to do. Less convoluted. Examples, I don’t know actually. Let me pass on that right now.

Q - If Tx2M was included in a block and was confirmed Tx3 referencing Tx2 will not be confirmed in a block right? On the blockchain level it is not a problem. If someone puts Tx3 in a block the other nodes will check the block and will find that Tx3 doesn’t fit in. Do you know if the miners check it after it is in the mempool? They have Tx3 and Tx2.

A - I’m not sure what you are asking. If someone tries to create a block with Tx3 in it that block will be rejected by other nodes because Tx3 spends coins that don’t exist in the blockchain.

Q - It is not possible that my funds got locked on the blockchain?

A - In this case where Tx2M is the one that gets confirmed, if we talk about Lightning. This could be any type of contract. When we created Tx2 and Tx3, Tx3 is like dispute resolution transaction. In case you don’t cooperate on how to spend Tx2 you can always publish your dispute resolution. But this dispute resolution transaction depends on Tx2 being confirmed in the first place.

Q - It is mainly an offchain problem?

A - Yes it is only a problem for this particular instance of the contract. The blockchain is fine and everybody else’s contracts are fine but this particular contract is broken because of transaction malleability.

Q - Tx3 will get relayed but if it is in the same mempool as the miner and the miner doesn’t have Tx2 and has Tx2M it will be rejected?

A - Yes but I think it will be rejected even earlier. It will be rejected by each node when you try to propagate this transaction through the network the first node it encounters will see that Tx3 spends coins from an invalid transaction. Or it doesn’t even have this transaction because it is invalid. The node has already received this block. If it had this transaction in its mempool it will drop this transaction because it is now invalid.

Q - I thought Tx2 and Tx2M were simultaneously relayed through the node network?

A - They are simultaneously. For a while they are both in the mempool but once transaction Tx2M gets confirmed in a block then every node will drop Tx2 because it is invalid.

Q - As a summary there is no problem if you just have the transaction go onchain and you don’t need any transactions linking to that transaction. Future transactions to link to that transaction. But if you do and you are building constructions and projects that rely on referring to that transaction ID then transaction malleability is a real problem.

We said that transaction malleability was a problem because of what Michael just said. That’s because the transaction ID is calculated from the whole transaction including the data in the signature scripts. If the data in the signature script changes the transaction ID will also change.

# Solutions

Let’s move over to the solution to this. What SegWit does is move the data out of the signature script and into a separate data structure that we call the witness. This witness or more or less attached to the base transaction. We call the transaction without the witness the base transaction. When we rip out the data from the signature script and put it in the witness the signature script becomes empty. Now if you hash this base transaction you will get a transaction ID. If you change anything in the witness, the witness data, the signatures for the pubkeys or add or change any data in the witness it doesn’t affect the transaction ID. The witness is not included when you hash the base transaction. You can change the witness all you want but that won’t change the transaction ID. That eliminates all known problems with transaction malleability. Suppose that you have a SegWit wallet that knows everything about SegWit. You want to sell your laptop to Amy. The first thing you need to do is get a Bitcoin address from your wallet so you can give your address to Amy. Your wallet will create this address for you. This is the new address format that came with Segregated Witness. It starts with bc1 and is followed by a q. You have a lot of lower case letters and numbers. You give this address to Amy so that she has an address to pay to when she wants to pay for your laptop. Amy inputs this address into her wallet. The wallet will then construct a transaction with the help of this address. She wants to construct a transaction output with this address. I won’t go through all the details of this diagram. I just want to show it because I think it is cool. I want to highlight a few things here. This address that you see at the top there, the SegWit address, it encodes two pieces of information. First of all it encodes the witness version. In this case this version is 0. This version is for future upgrades of SegWit. The address also encodes what is called a witness program. In this example the witness program is a 20 byte array. This array happens to be a public key hash. It is the same kind of public key hash you are used to from legacy transactions, pay-to-pub-key-hash payments. Nothing new there. Amy takes these two pieces of information, the witness version and the witness program and she puts it in the scriptPubKey of her output. I usually say pubkey script. She puts the version byte and the witness program into the pubkey script in her output. She is paying 0.1 Bitcoin to you for the laptop and the scriptSig is a version byte and the witness program. As you might recall from legacy transactions, a legacy output would look like something like this. It is a small script here with a pubkey hash in it.

`OP_DUP OP_HASH160 <PKH> OP_EQUALVERIFY OP_CHECKSIG`

In our example here we don’t have a script of the same kind. We just have a few data pushes.

`version_byte, witness program`

Let’s say that Amy does this and she publishes this transaction and eventually it will get confirmed in a block. Now you can give your laptop to Amy. That deal is done. Amy has the laptop, you have the 0.1 Bitcoin. Now you want to spend this coin. You want to buy a popcorn machine using this money. How would you do that? How would you spend this output to buy a popcorn machine? You create a new transaction that you see over here. You create a transaction that references Amy’s transaction and the output that Amy created for you but you don’t add anything in the signature script. You instead add a signature and a public key to the witness instead. The signature script is empty and the signature and public key is entered into the witness. This is the feature that we saw earlier where you rip out the data from the signature script and put it in the witness to avoid transaction malleability. You create this transaction and you add an output to the popcorn guy here of 0.09 Bitcoin. Then you send the transaction out to the Bitcoin network. Then it will reach a node and a node will probably want to verify this transaction. Let’s see how this transaction is verified. The node will look at the output of Amy’s transaction. The node is a SegWit enabled node. This node knows everything about SegWit. It notices that the output consists of a zero byte followed by a 20 byte array. This is a specific pattern that it looks for. It finds this pattern and from this pattern it can conclude that this is a pay-to-witness-public-key-hash. If it encounters pattern it will trigger certain verification functionality. It will take the pay-to-witness-public-key-hash template that it has and replace the placeholders with data from the transactions. This public key hash placeholder will be replaced by the witness program which is the public key hash. The signature placeholder and the key placeholder will be replaced by the signature and the public key from the witness. Then as you can see here we have a complete program that resembles very much the program that is run for legacy transactions. In fact it is the same program apart from one tiny detail in the OP_CHECKSIG. I will not talk about that. This program is then run and evaluated. If it evaluates to TRUE the transaction is valid. In this case it is TRUE so this transaction is valid and the node will gladly forward it to its peers. A node has now verified a transaction and relayed it to its peers. But eventually this transaction wants to end up in a block. Some miner wants to include this transaction in a block. We will look at how that is included in a block.

Our transaction in this example is Tx2. A miner that wants to include Tx2 in a block or wants to create a block at all, creates a block just as it did before. It creates a Merkle tree of all the base transactions and calculates the Merkle root that it puts into the block header. It creates a Merkle root of all the base transactions. As you recall the base transaction is the transaction without the witness data. This is exactly how it was done before SegWit too apart from one little detail. That is this Tx1. This is the so called witness commitment. It is a hash that has been put into the coinbase transaction of this block. It is a OP_RETURN output of the coinbase transaction that contains this witness commitment. This is a commitment to all the witnesses of the transactions in this block. This is the new thing in the block construction. Let’s see how this witness commitment is done. This witness commitment is created in pretty much the same way as how the Merkle root is created from the base transactions. It is a Merkle tree made from the witness transactions, the witness transactions including the witnesses. In this way we get to commit to the witnesses in the Merkle root in the block header. It is a nested Merkle tree in a way. This is how the transaction is included in the block. Any node that receives this block will be able to verify it in the same way as it was created by calculating this witness commitment and the Merkle root. Eventually this block will reach a node that is not aware of SegWit. An old node that is not upgraded should be able to verify this block successfully. Otherwise we would have a blockchain split which is unfortunate. Old nodes need to understand this block and need to successfully verify it. Let’s see how an old node would verify this block. Old nodes don’t download witnesses because they don’t know what a witness is so they can’t download it from their peers. They only see this data, this is all they see. They see base transactions. There is a hash in an output of the coinbase transaction but that is perfectly legal according to old rules. Nothing new here, nothing illegal. Everything is nice and dandy. This Merkle root will match the Merkle tree of the block header. There are no problems with verifying this. It just doesn’t verify every aspect of this block. It just verifies the aspects that it used to verify. But it also apart from this, needs to verify that Tx2 is ok and valid. It also needs to do that with Tx3 but let’s focus on Tx2 because that is our transaction.

This old node needs to verify that this SegWit transaction is valid. Of course it doesn’t know it is a SegWit transaction. It just sees a transaction. What the node sees is a transaction with an empty signature script. It doesn’t see any witness because it hasn’t downloaded the witness. And it sees an output with two data items in it, to them meaningless data. This node will do what it always does. It will run the program starting with the signature script and then run the pubkey script after that. Starting with the signature script, it takes nothing from the signature script and puts it on the stack. Nothing is put on the stack. Then it will run the stuff in the pubkey script. First it encounters a push of zero bytes to the stack. Then it will push this 20 byte array that it doesn’t know anything about. It just pushes that data because it is told to do it. This 20 byte array is put on top of the stack. Then the program is finished. There is nothing more to do in this program. What is left to do is to find out whether the program evaluated to TRUE or not. Or if it evaluates successfully. If the top item of the stack is nonzero Bitcoin will regard the script as successful. In this case we have a program stack that has zero on the bottom and the 20 byte array on the top. The 20 bytes on the top is nonzero so this script has evaluated to TRUE. That means that the transaction is valid. This is how an old node would verify this transaction.

Q - How is the witness in a block connected to the transaction? Is the Merkle tree of the witnesses exactly the same as the transaction Merkle tree? The bottom right transaction and the bottom right witness is exactly the same? If a block will be relayed the node will check if Tx3 on the upper right is valid. So they have to check the witness too? The witness is in the Merkle tree on Tx1 in your diagram. How do they combine these?

A - When you send a block to a SegWit node you will send a block header and a list of all transactions and all witnesses. The block will receive all transactions and all witnesses so that it can create this Merkle tree.

Q - How does Tx3 compare to the witness Tx3? It is only the witness or is there a transaction ID additionally on the witness? I want to check if the witness fits to Tx3 but it is in a different place.

A - You want to verify this witness belongs to this transaction. You can take the witness and attach it to this one and verify that transaction as if it was a SegWit transaction. That is not a problem.

Q - There is a data field that refers to Tx3 in a witness?

A - When I draw the transaction like this and it is attached to Tx3 it is not completely true because in a witness transaction the witness is actually an integral part of a transaction. It might be a bit misleading to draw it like this. There are two versions of the transaction. One version is the base transaction and another version is the witness transaction. The base transaction is one data structure and the witness transaction is another data structure. Depending on which node you are sending transactions to you are sending either a witness transaction or a base transaction. You send base transactions to old nodes and you send witness transactions to witness capable nodes. They are actually two different data structures but they are very similar. The difference is that witness transaction contains a marker flag at the beginning of the transaction and it also contains the witness.

Q - I think the question was that if you are trying to verify a transaction how do you know where the witness of that transaction is on the other Merkle tree, the other data structure? You want to verify the witness for that transaction but is in a different data structure so where is it on the other Merkle tree? There’s a Merkle tree for transactions and there is a Merkle tree for witnesses and my understanding was that they were totally separate.

A - These are the witness transactions that you hash into witness transaction IDs. Witness transactions are not only the witnesses. It is the transactions including the witnesses. It is the transactions including the witnesses down here. These hashes here are the hashes of the total witness transaction.

Q - Two transactions will be stored efficiently?

A - A witness node will only store this witness transaction but an old node will only store the base transaction. You don’t store two versions of it. A SegWit node will store this witness transaction here and if it wants to send this transaction to a non-SegWIt node it takes out the witness part and just sends it.

Q - This is where I think there has been a massive hole in my knowledge this whole time because I thought there was a completely separate Merkle tree. But this is one Merkle tree that has pre-SegWit transactions and then SegWit transactions at the bottom of the same tree and the witnesses are with those transactions at the bottom of the tree. That’s a hole in my knowledge for all this time.

(This discussion was continued on [Twitter](https://twitter.com/michaelfolkson/status/1256272461722681344?s=20) afterwards.)

Q - Just on how we are defining witness. Are witness and signature interchangeable here? How are we defining witness?

A - The witness is just a data structure that is part of the witness transaction. On a conceptual level what is a witness? Anything that attests to the validity of the transaction. It could be a signature, it could be a hash and several signatures.

Q - And a preimage to a hash could also be a witness?

A - It could. Let me be clear here. This whole data structure is called a witness. There is one witness field for each input of the transaction. This transaction Tx3 has two inputs. Each row in this witness is called a witness field. The witness field is associated with a corresponding input of the transaction. What is called a witness of this transaction is this whole square here.

Q - Are there any actual legacy only nodes left? Everything now is SegWit, all the nodes?

A - I saw some statistics the other day, I can’t really remember. There are probably a few but they are pretty rare these days. There are definitely old unupgraded nodes still. Maybe they are not that economical those nodes because if they were economical the users of those nodes would probably have upgraded by now. I think SegWit was introduced in 0.16.

Q - They don’t really play a role?

A - Not really because they don’t verify all aspects of the block. Of course if the users only use legacy transactions the node will work perfectly for them to verify the legacy part of the transactions.

Q - All the SegWit transactions they see as anyone-can-spend. Any user that runs a non-SegWit node would be able to spend them inside this small community of nodes that still run pre-SegWit?

A - Yes. It will probably get propagated among those nodes but you need to have the transaction confirmed. If a miner tries to create a block with this transaction in it, an anyone-can-spend transaction if you spend it as anyone-can-spend and if a miner includes that in a block that block will be invalid according to an overwhelming majority of the nodes on the network.

Q - Also it won’t be propagated because you are usually not connected to all legacy nodes.

A - It is going to be hard for it to be propagated.

# Quadratic hashing

I can talk about another problem that SegWit solves. I haven’t prepared it much. That basically means that the bigger the transaction gets, the more inputs the transaction has the harder it is to verify this transaction. Or the longer it will take. Just not linearly but quadratically. The problem with quadratic hashing. Let’s say a transaction with two inputs takes one millisecond to verify. Then a transaction with four inputs would take four milliseconds. You double the amount of inputs but the time to verify the transaction will quadruple. If you double again from 4 to 8 inputs the time to verify this transaction will quadruple again to 16 milliseconds. If you scale this up to 1024 inputs it would take about four minutes to verify this big transaction. This is called quadratic scaling. When you double the size of the transaction you will quadruple the time to verify it. This is a major problem that is being solved by SegWit. I will show you how this happens, why we have this quadratic hashing problem. Let’s see how a typical transaction verified. You want to verify the right transaction here. Step 1 is that you remove everything from the signature scripts and you then want to verify the signature for this input here, the first input. You do that by taking the scriptPubKey and putting the scriptPubKey in the place for the signature scripts. That is how it works. Then you sign this transaction with a signature that you later put in this signature script. Now you have created a signature for the first input. Now you need to do the same, you need to create a signature for the second input. You do the same dance again. You clear out all the signature data from this transaction and you take the scriptPubKey and put it in the signature script place here. Then you sign this transaction. Signing a transaction means first hash it and then sign it with a private key. You sign the hash of the transaction. First you need to do this and sign that. Then you need to do this and sign that. This means that if you double the number of inputs you also double its size more or less. If you double the number of inputs you also need to double the number of signatures you need to create. If you double the size of the transaction the time to create each signature will double. When you double the time to create the signature and you double the number of signatures you need to make then the time to create the signatures is quadratic. That also goes for when you later verify this transaction. When you want to verify the transaction it is the same thing. You need to verify in the same way as when you create the signatures. To verify the transaction you need to perform the same dance. Replace the signature script with the pubkey script and do that for each input. That is the cause for this quadratic hashing. When you double the number of inputs you double its size and you double the number of operations you need to do. Each of these operations will take double the time.

# The SegWit solution to quadratic hashing

SegWit solves this in a neat way. Instead the dance we talked about earlier you will create an intermediate hash once and for all. No matter how big or how many inputs you have, you create one intermediate hash that you will reuse for each input. You create this intermediate hash here and then for each input you add just the data that is unique for this particular input. The first signature you make here takes data from the first input. Then you sign it and put it into the witness. In this way if the transaction size doubles you only need to hash the whole transaction once and then you have to make one constant size signature for each input. This causes the time to verify such a transaction to drop to 0.5 seconds instead of 4 minutes. That is quite a bit of a difference. That is what I had to say about that. That was highly unrehearsed.

Q - How is the timing behavior of hashing relative to signing? Which one tends to be slower? Is signing a very slow process?

A - In this case here if you have a very big transaction in the legacy system the hashing would take most of the time because the transaction is so big. You need to create the hash of a very big value. You need to hash a lot of data. In this case the overwhelming time is hashing. Then the actual signing, when you sign the hash with the private key that is only 32 bytes.

Q - I was wondering when I got to this part of the book about the quadratic timing. If hashing takes so much time it appears illogical to me that in the Bitcoin system everything is always being hashed all the time. Sometimes double hashed, sometimes 1024 hashes. As if it didn’t take any time. That’s why I was interested in learning whether it is a very fast thing to do. I don’t think it is.

A - When you talk about a big transaction like this that is really a problem. Most of the time in Bitcoin the pieces of data that you hash are pretty small and you don’t do it in stupid ways like this most of the time.

Q - It is highly dependent on the size of the data block?

A - Absolutely.

Q - I thought it was another set up to be done. The initial pattern that you XOR all this stuff with has to be set up and memory allocation. You have to do that for every hashing?

A - You do need that but that is usually very quick for small pieces of data. I am not an expert in this field so don’t make my word for it.

# Q&A

Q - How did you come up with a structure for the book? It is very easy to get lost because is so mingled.

A - That was a major handle in the beginning. I had early drafts of outlines that I never got pleased with. I had a conversation with my wife and we came up with this way to teach Bitcoin together. I have seen similar approaches previously as well. That just seemed natural. It came to me there sitting at the kitchen table discussing it with my wife. I think it was her suggesting it. That was a great idea. It fits this book perfectly I think.

Q - I am interested to hear about forks. The changes introduced and in particular why so far they have not done very well e.g. BCH which increased the block size.

A - Because they provide nothing new. I think they provide nothing interesting and less security than Bitcoin provides. For average users why use a less secure asset when there is Bitcoin that is very secure comparatively? Bitcoin Cash has one percent of the hashpower of Bitcoin which is tiny. Any miner can cause problems in Bitcoin Cash today. I am just surprised that double spend attacks haven’t happened to Bitcoin Cash yet but it will. It has happened to other coins but not Bitcoin Cash. It is just a matter of time I think. I think they don’t work out as well because they are not as good as Bitcoin. Not as secure and not as widely used. So why use it?

Q - It feeds into the discussion at the Socratic last week around what the actual history was. The initial fork of BCH and then SegWit2x and all this kind of stuff. I thought at the time, I still think now, SegWit was a very good change and the Bitcoin Cash guys didn’t implement SegWit. I think this was a mistake. I suppose the majority of the developer community stayed on Bitcoin rather than moving to Bitcoin Cash. I think that is a big factor as well. All the innovation we have been seeing since the formation of Bitcoin Cash, the vast majority of it has been on Bitcoin. You are seeing Lightning being built on top of Bitcoin. You are not saying a Lightning Network being built on top of Bitcoin Cash. Not much happened with Bitcoin Cash apart from the block size increase.

A - They are falling hopelessly behind especially when Taproot probably gets deployed on Bitcoin. We are so far ahead of what Bitcoin Cash has achieved. I think it is weird that it exists still.

Q - I suppose it is very hard to kill. They have a very slow death. It will probably be around for many years more but I don’t have too many hopes for it. What are you most excited for the future of Bitcoin? Wallets, BIPs, hardware wallets etc

A - I am excited about Taproot. I think it will bring huge benefits to privacy and blockchain space. With blockchain space I mean blockchain real estate. It will save a lot of space in the blockchain and provide enormous privacy improvements. I think that is just amazing work from the guys behind those BIPs. That’s the part I am most excited about I think. I am also excited about descriptor wallets in Bitcoin which is coming. Me and my wife are working on a project that utilizes descriptors in Bitcoin Core to create a wallet on top of Bitcoin Core that uses 2-of-3 multisig. We are both pretty excited about that. It is hard to keep your eyes off the Bitcoin charts right now.

Q - Maybe just explain what Taproot is.

A - So Taproot is SegWit version 1. I showed you SegWit version 0 in my talk. Taproot is a major improvement. I did a couple of diagrams on it with illustrations. I put up those on [Twitter](https://twitter.com/kallerosenbaum/status/1197652948484083714?s=20) a couple of months ago where I described it with diagrams which I am pretty pleased with. Basically every transaction that you do, as long as your counterparty cooperates with you which is 99 percent of the cases each transaction will look like a single signature spend. Everything will look the same on the blockchain no matter how complex your scripts are. You can have a lot of different options to spend a coin but it doesn’t show. If you don’t agree and you need to use one of the exit strategies for this contract, there might be multiple exit strategies for the contract, you only have to reveal the one exit strategy that you use. The others are still hidden from the blockchain. That’s the major part of it.

Q - What would be the impact of Taproot on chain analysis?

A - I think it is pretty much the same there. Chain analysis, if you look at companies like Chainalysis, they get data from exchanges on which addresses belong to which users. In those cases it doesn’t really help that much. But if you use very exotic scripts today those scripts will be easily identifiable on the blockchain because it is only you using it. With Taproot that is no longer the case. Even if you use exotic scripts no one will see that. Your anonymity set will grow enormously.

Q - The privacy benefits as Kalle says are in really in those complex scripts. Lightning, funding channels, complex multisigs with hashlocks and timelocks and all this kind of stuff. That’s where the privacy benefits come in. If you are just sending to single public keys or single addresses there is no privacy benefit really. It is the privacy of the complex contract around that spend.

A - Even for single sig ordinary payments you will also gain because all the complex stuff now looks like the same kind that you use. Your anonymity set grows too but not as much as for the complex guys.

Q - How private is Lightning now?

A - More private than onchain transactions. A Lightning transaction is very private but the channels are not much more private than ordinary Bitcoin transactions. I guess you could still identify what channel belongs to what person. In the same way you can do with ordinary transactions. But the Lightning transactions themselves are extremely private. How private? I don’t know, how long is a string?

Q - You can be on Tor as well can’t you with private channels?

A - Yes. I’m not a Lightning expert so I can’t talk about it that much.

Q - It is very different set up. There are certain privacy attacks like probing where you can try to find the balances of Lightning nodes but the core privacy benefit is that there are a lot of transactions that don’t make it onchain. Normally if you make a transaction onchain that is there for everybody to see. If you are making a transaction on Lightning unless you are actually closing the channel out all those transactions aren’t going to the chain. At least on the face of it the privacy benefits are very promising. There are always other attacks that people like Chainalysis will be orchestrating.

Q - I think the problem is that all your funds are on the same node. With Bitcoin transactions your addresses are mostly separated from each other. But in Lightning you have everything on your node with one IP. If you don’t use Tor it is very easy to see how much funds you have in total. Or to at least assume how much funds you have. With Bitcoin this is more difficult onchain.

A - I think you have a good point there.

Q - We are kind of repeating history. Bitcoin initially had to pay to IP address I was hearing the other day. With Lightning if you are not using Tor we are still in the world where your node is connected to your IP address unfortunately.

Q - I don’t think you can see the amount of funds even if you watch the traffic, even if it is not on Tor. You see a lot of transactions coming out and coming in but you can’t see the amounts as far as I know.

Q - You can’t on the face of it. There are certain attacks. You can probe to see if there is enough capacity to go in a certain route and therefore work out that way whether a node has a certain balance. Or you can set up lots of Lightning nodes and people route through your Lightning nodes and then you are seeing the whole route. If someone like LNBIG controls literally every node on the network they will therefore see all the traffic.

Q - You can attacks like you can analyze the graph. Because it is Tor routed you shouldn’t be able to know at what point you are in the route. Whether you are close to the endpoint that is sending it or receiving it. But by analyzing the graph you could find out if the node that I am getting the transaction from is a certain position in the topology then he must be an endpoint because only if he is an endpoint would it make any sense for them to send the transaction via my node. You can detect certain things from the topology which is an attack vector. Personally I would take Lightning over onchain any day.

A - I haven’t heard about that kind of attack, interesting.

Q - Lets say as a Lightning node you have the full connectivity graph in memory. Now if a peer sends a transaction via your node and you see where it is going then you can deduct that your node is only on the ideal path if the node you received it from is the sending node.

Q - On Lightning and Taproot which project fills you with more excitement. Doing a second edition of Grokking Bitcoin including Taproot or Grokking Lightning?

A - Probably Taproot. I like both projects but some thing draws me to Layer 1. I like Layer 1 very much. It is a very special set of problems there that you don’t have on Layer 2 networks. The scarcity of block space, the challenges there are unique compared to other systems. It is very interesting.

Q - It would be interesting to see how Andreas’ book on Mastering Lightning with Laolu and Rene works out because things do move so much faster on Lightning.

A - Absolutely. I look forward to reading that book. I only have an abstract understanding on Lightning Network unfortunately.

Q - After the second edition including Taproot, Grokking Lightning after that.

Q - Taproot and Schnorr, these are separate things?

A - Schnorr is a new signature scheme, it is not new, it is old that has been around for ages but it has been encumbered by patents. In recent years you have been able to use it freely. It is a signature scheme that is more appropriate for Bitcoin because it is a linear system.

Q - You need Schnorr for Taproot. Schnorr allows for key aggregation. Taproot is combining all of that complex smart contract stuff in a Merkle tree and hiding it within your taproot or address. You need the properties of Schnorr to be able to build pay-to-taproot addresses. It is a signature scheme that is no longer patented to replace ECDSA which was the signature scheme Bitcoin was previously using.

Q - No other benefits other than it is needed for Taproot. That would be the benefit. Taproot is the benefit?

A - And efficiency.

Q - It is a little smaller and it allows for key aggregation so if you have a 2-of-2 multisig you only have to put one key and one signature onchain. Before if you had a 2-of-2 you would have 2 keys and 2 signatures go onchain which would be much larger.

Q - Good for scarce block space then?

Q - Absolutely. It seems at least from my high level perspective to be a really designed proposal, very similar to SegWit but perhaps less dangerous than SegWit.

Q - Where we can buy those Grokking Bitcoin T-shirts?

A - This is a super scarce T-shirt. I have a few left here.

Q - Regarding Taproot I was wondering why we use public keys again and not hashes of public keys or addresses. Does anyone know why this is used?

A - We use public key hashes in legacy and SegWit version 0 transactions. But that is a waste of block space. First you need the public key hash in the output of a transaction and then you need to add the public key in the scriptSig of the spending transaction. You need to add a lot of data just to be able to verify the transaction. If we move away from public key hashes and just use plain public keys in the output instead we save a lot of block space. We make it more straightforward that way. That is one of the reasons. I think other reasons might have to do with Schnorr and Taproot technicalities. One of the major advantages is that we save block space.

Q - Why was it added in the first place then? We went from pay to IP addresses. Then we went to pay-to-pubkey and pay-to-pubkey-hash. A pubkey hash smaller than a pubkey so that is saving some space. Then you had pay-to-script-hash, you are hashing the script until you spend it. Then we had pay-to-witness-script-hash. To get the benefits of the key aggregation you can’t hash those public keys. To be able to do that key aggregation they need to plain public keys. If they are hashed you can’t add two hashes together and get the same properties you can with plain Schnorr public keys.

A - I have one comment there on the first steps. When we went from pay-to-pubkey to pay-to-pubkey-hash the pay-to-pubkey was huge. It was 64 bytes because we had uncompressed public keys back then. We went from 64 bytes down to 20 bytes which was a very valid trade-off back then. Now we have compressed public keys it is not that much gain anymore to go from 33 bytes to 20 bytes. That gain is not worth it anymore. It was worth it back then when we went from 64 bytes to 20 bytes. I think it was more obvious back then but it is not anymore.

Q - I heard that the quantum thing is not the right answer. This is in reference to people thinking that hashing the public key provides some protection against quantum computing. I think this has been one of the major discussion points on Schnorr and Taproot. Pieter Wuille and some of the other Taproot authors have gone over this over and over again with people asking about this. One of the arguments is that if we have a quantum computer that comes out of nowhere it is going to threaten the Bitcoin network anyway. And also there were questions on how much protection hashing provides in that world where a quantum computer comes out of nowhere.

Q - In today’s Bitcoin Optech newsletter there is a link to that. Pieter Wuille explains it again.

Q - I thought it was the reason that if ECDSA cracks or gets broken you only need to crack ECDSA to get to the private key. If you hash it you have to do two cracks initially. The hash algorithm and the ECDSA.

A - That’s right. That’s the classical argument. But as Pieter Wuille says a lot of coins on the blockchain today, I think it is like 5 million coins are not protected by a hash, just by the discrete logarithm. It is protected by signatures and not by hashes. 5 million coins are already vulnerable which means that if a quantum computer would suddenly appear then Bitcoin would be pretty much dead because 5 million coins lost would probably crush the system.

Q - Your point Kalle that Pieter has also said is that there are a lot of funds on the network that have exposed the public key. They are not protected by a hash anyway. Then there are various arguments on if the quantum computer can break elliptic curve cryptography then perhaps it can also break the hashing algorithm.

A - Also there is a slight window between when you publish the transaction until the transaction gets confirmed. If you have a quantum computer… When you publish the transaction you reveal the public key so during the time from when you publish the transaction until the time it gets confirmed you are still vulnerable to this quantum attack because then you have already revealed the public key. You have up to an hour to crack that.

Q - And if you reuse addresses you have the public key in the blockchain and you can take a lot of time to quantum compute the key.

Q - Can you please elaborate why the public key is seen between confirmation and sending.

A - Let’s take this transaction for example. If you create this transaction you include the public key in the scriptSig here, the signature script. If you publish this transaction you would reveal this public key that corresponds to the public key hash. The only thing that an attacker would need to do from the time of publication is actually find the private key that corresponds to this public key. Here you have already revealed what is behind the public key hash, what the public key actually is. If you have a quantum computer you can just crack this and find the private key.

Q - Even if you use addresses you put the public key in there? You don’t put the addresses in there?

Q - Only if you spend from that address. You can have an address on the chain and funds are sent to that address. If funds are sent to the address but you aren’t spending from that address you aren’t revealing the public key. As soon as spend funds from that address you are revealing the public key.

A - I only reveal the public key of the address that I am spending from.

Q - In terms of IRC, I’m not on it. What do you recommend for an IRC client?

Q - I’m in the process of transitioning. I am using Textual at the moment because it was easy to set up. But I need to set up a bouncer personally. When you close the computer or go offline you can’t get messages and you don’t get the history of the chat. You need to set up a bouncer so when you go offline and then come back you can still see messages people have sent you or the conversation that has happened while you’ve been away. It is a little fiddly to get set up. Textual is a good start if you are not worried about not receiving messages when you’re offline. Textual on Mac OS. I’m sure there are better set ups.

A - I am also struggling to find a good client. I am using Hex Chat and I am not very pleased with it but it works.

Q - I think we need to all compare notes and make sure that we have got the best set up. There were some tweets in the past on this topic. Core developers saying what set ups they were using to connect to IRC.


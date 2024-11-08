---
title: Covenants - Structuring Multi Transaction Contracts in Bitcoin
transcript_by: Michael Folkson
tags:
  - covenants
speakers:
  - Jeremy Rubin
date: 2017-01-26
media: https://www.youtube.com/watch?v=r7xN7K0OqaA
---
Slides: https://rubin.io/public/pdfs/multi-txn-contracts.pdf

## Intro

Hey everyone. How is it going? Happy to be going last right now given that I had all these wonderful speakers before me to explain so much of what I am about to tell you. I’m going to talk to you today about structuring multi-transaction contracts in Bitcoin. I think there is a lot of great work that happens in Bitcoin at the script level, at the individual input and output. I really think the magic happens when you have a concert of contracts working together and you see the interactions between them.

## Is Cash Bitcoin’s Killer App?

One of these fundamental questions is is cash the killer app for Bitcoin? Is it the last word? I would say no it is not. Ethereum does quite a lot of interesting things with smart contracts. You have bad things 	that happen like the DAO but it certainly shows that there is more that can happen in this space.

## Safe Contract Extensions for Bitcoin Contracts

In Bitcoin we try to figure out ways we can do this that are safe. I think that it is our jobs as developers and engineers in this space to find tools for complex contracts that avoid internal complexity inside the system and allow us to express that complexity at a layer above. A lot of people are skeptical that this is really possible. You might have to push down and keep the application simpler.

## We Can Have It All

I think we can have it all. We can express these as transaction level invariants rather than at the script level and we can use covenants to help us get there. I am glad you have already heard about what covenants actually are. I think of it as any invariant on what the output of a transaction will be. I’ll go over that a little bit more.

## Contributions

The main contributions of this talk today, I’m going to talk about some extensions to covenants. Some types that I think are novel that I haven’t really seen discussed before. I am cognizant of the fact that everything has been developed in \#bitcoinwizards on IRC before. If you have some prior literature I would love to hear it. I’m going to talk to you about how you can use covenants to Merkle compress a script. To do the same thing as what a MAST would do which you might have heard about earlier. Similar to how Ivy hopes to have a language for compiling to Script I have a diagram language that I have been using to describe contracts and the interaction between them that I think will be useful. I will go over the primitives there. Also I am going to talk about multi-phase execution techniques. Once you have this interplay of contracts you have all sorts of fun types of race conditions and there are ways you can structure your contracts and your programs to be resilient or tolerant of these types of failures.

## Covenant Contracts - Background Knowledge

To start off with some background knowledge on what covenants are.

## The Naughty Banker

You might imagine that you have a naughty banker who you give 100 dollars and then he buys himself a banging pair of new kicks. You are a little bit angry because you gave him the money to store and give it back to you.

## Covenant Contracts

You may want to rather express that “Hey. When I give you this money it is for you to give it back to me later. I am the only one who can withdraw.” That is an example of a covenant. You’ve given control of something to some other structure but you’ve specified what exactly can happen after that point.

## Placeholder Notation

There is a general placeholder notation for this. I’m just going to say you have a standard function COV with some plain English statement or if we are in a Bitcoin Script thing an arbitrary block of data and then OP_COV. That will be verified in the script and guaranteed. For example you could have a covenant that Bob’s bank only lets me withdraw. The reason for that is there are multiple ways of implementing covenants. We haven’t had the final word on what that way is. We’ll see where that goes.

## Making Covenants

As far as implementing them there are a couple different ways that are interesting. I think they fall into two major camps. You have invariant by execution and invariant by construction. I think you will find people on either side who prefer one or the other. I would say that an invariant by construction is slightly preferable. When you are invariant by construction it means simply by having an element of that set of things you know that it is correct and the covenant’s property has been fulfilled. Whereas a covenant that is invariant by execution you have to run some program using that to verify. That relates back to Russell’s (O’Connor) [talk](https://www.youtube.com/watch?v=TGE6jrVmt_I) as well.

## Grave Concerns

It is not all flowers and sunshine. There are some pretty serious problems with covenants that are things to be worried about. Fungibility and privacy could be all but eliminated if you require the propagation of metadata and compliance. You could have computational explosion where you require some massive computation to happen in order for your transaction to be spendable. In general we have seen with some of the earlier talks there is an open topic to see if we can build expressive and safe contracts in Bitcoin without covenants. It is a little bit like preventing Turing completeness, these things pop up in ways that you wouldn’t expect them to happen. CSS is Turing complete, so is MOV and so are C++ Templates. All of these things tend to coalesce on providing certain ways of expressing very powerful computations as well as expressing powerful covenants. In Bitcoin they already do exist. There is a covenant in every Bitcoin transaction that says the sum of the outputs’ value does not exceed the sum of the inputs. You can’t create new money. That might seem like a very trivial thing that is very obvious to us but it is a restriction on the way that a transaction is able to create outputs from inputs. It does exist but it is a question of are there more powerful constraints that we can levy on our transactions without making unsafe or dangerous conditions.

## Extensions to Covenants

Now that we understand what a covenant is and what it could allow us to do I am going to talk about some minor extensions to covenants that I think are interesting to consider.

## Tale of Expired Accounts

I am going to start off with an anecdote about some expired accounts. Let’s say you have a phone number and you have some two factor authentication enabled with your bank account that sends you a text message anytime you try to deposit. When you change your phone number you would want the two factor authentication number to change as well because somebody might come in and take your old phone number and then be able to authenticate your bank right away. It is something you have to be careful about. We’ve seen recently some problems with AT&T and various companies allowing phone numbers to be changed to different SIM cards causing the two factor authentication to fail. What you kind of want is not be able to change your phone number before your two factor authentication for every service you are using changes to point to the new account. Maybe there is some kind of notion of you want two things to happen at the same time that are unrelated.

## Input-Join Covenant

 In Bitcoin this translates to a notion of an input-join covenant. What this is an expression of is that you have one input that must be spent in the same transaction as another input. If you specify that for both transactions then you are saying these two outputs must be spent within the same transaction. That gives you a property that things execute at the same time and that one doesn’t get left off and replaced with something else. Having to execute by its lonesome that it might not be able to do. The funds might be provisioned elsewhere. An input-join covenant is a pretty important property that gives you this both or nothing semantics. In order to implement this in Bitcoin there are a couple of ways that you can do it. It is somewhat minimal extensions but it does require rethinking how we specify transactions.

## Two Cars Problem

The next problem I want to tell you about is the two cars problem. Let’s say you are doing fairly well and you have a Porsche and a Ferrari. You tell your really good friend “Hey why don’t you take one of my cars for the day? I am going to decide which one I want later. Don’t take it until I have decided.” You give them the keys and you give them the option but you want to express “Don’t take a key until I have chosen the key that I would like to use.” That is a little bit tough to do in Bitcoin if you want to say this happens before something else happens. You want to be well on your journey before they are able to take the other key and take the car that you might have wanted.

## Impossible Input Covenant

The way that I term this is an impossible input covenant. In Bitcoin what would you say is you provide a proof that an input could not be constructed. In the key metaphor I’d be saying “I am providing a proof that I would not want that key.” In Bitcoin I am providing a proof that says “This input that I’m talking about has been consumed or has otherwise been made impossible to construct.” There are a couple of ways of doing this. Both on the correct by construction side and on the correct by execution side. You could either just audit a property on the chain or you could try to consume an input that is only made available when the branch has gone in the other direction. You would know that you have some mutual exclusion between the two things executing. This ends up being implementable as a normal input script but it is a covenant of how things are able to be used. There are some interesting things you can do with this.

## Bad Airlines

The next example I want to give you is what happens when you fly on a bad airline and you are going from JFK to SFO and you have a layover in ORD. You go from JFK to ORD and then you get snowed in and you are stuck in the snow. That is awful, I hate the snow. What you want to ensure is that you go directly from JFK to SFO. You want to know this when you get on the plane. If you have two contracts that have some relationship between them you might want to specify that these things happen either both together or neither.

## Intermediate Output Covenant

This is what I call an intermediate output covenant. What you want to say is “I am going to make an output in this transaction but if it isn’t consumed within the same block in a long chain as they’re called in Bitcoin, then this block is invalid.” The onus is on the miner to ensure that there is some transaction which does end up spending this. It is a little bit similar to the Child-Pays-For-Parent code which allows you to pay the fee for an ancestor transaction in order to do a fee bump. It is also bad for a two phase protocol. If you want to say that one thing happens, we’ll wait a little bit for it to confirm and then the next thing happens. It could happen in between phases. In general it is good for allowing you to not worry that two things might get broken up and one half might execute and the other half won’t.

## Bad Airlines (Part 2)

Your trouble with the airline doesn’t stop there. Now let’s say you decide “Screw booking a ticket which goes directly through one airline. I am going to book my own transfers and make sure I only go through places without snow.” You get to the airport and then you realize they are not going to give you all the tickets at the first place you check in. You have to go back through security again. That is a bit like having two separate transactions you have to do. You have to go back through the security process and it is completely separate. Maybe you are going to be late for your flight as a result of this.

## Virtual Output Covenant

The solution here is a virtual output covenant. Now a virtual output covenant says that you have an output that gets created with maybe zero satoshis. It is not something that is going to give you any value. You are also going to provide a script that would redeem that within the same transaction. What that gives you is a proof that if you could have spent that you did. And it is not spendable by anyone else. Everything executes all at once. This is a little bit like a delta zero script because you are able to then have any property that you have go recursively if you have a covenant combined with a virtual UTXO. You don’t have a safety risk of this leaking outside of a single transaction so all the execution happens on your end because you have to construct the transaction to have spent all these UTXOs.

## Application - Merkle Covenants

Now we have constructed a couple of primitives in this space to play with I am going to give you the core of this talk which is what a Merkle covenant is.

## Compressed Contracts

Let’s start off with a compressed contract. What does it mean for a contract to be smaller than necessary? You have some useless clause. Let’s say you are filling out a tax form. It says “If you have a taxpayer identification number” which probably 90 percent of you do you just fill it in. It is very simple. If you don’t they tell you to read Appendix A and that will tell you what number to put in. Then you fill it in. Most of us can throw away Appendix A, we don’t actually need it. In Bitcoin we can kind of do the same trick.

## MAST: Merklized Abstract Syntax Tree

The way that we do this is what is called a Merklized Abstract Syntax Tree. This gives us a O(log(n)) branch compression. It is Huffman codable so we can	make the most probable things the shortest to express. A simple example of this is we take a program, a very simple IF ELSE branch and we turn it into an assertion that if the condition was true we provide the proper code for that branch and then we execute that code. That is a very simple high level description of it.

## Bitcoin Implementation (Proposal)

There is a current implementation proposal for this in Bitcoin. The way that this one works is you put all of the branches, all their final execution states into a big set. You make a Merkle tree out of them and then you prove one branch and you execute the end of that branch.

## Properties

I actually take a little bit of an issue with this. I don’t think this is quite the right semantics that you would want out of a Merklized Abstract Syntax Tree representation because this is completely atomic execution. You can only execute the entire program at once or not at once. There is no possibility for intermediate state. In terms of implementation it is good. There is no hash overhead but it doesn’t quite get the whole picture of things that are possible to compress.

## Conditional Covenant

The way that you can do it in the way that I would envision is you can do a conditional covenant. What happens when you have two covenants and you are able to choose which one you enforce. You say “I either want to output A or I want to output B”.

## Either Red Tx or Blue Tx

When you spend something like that it looks like this. You have two possibilities of transactions that you could construct. One spends to the A, the other spends to B. Only one can go on the chain, the other one will preclude the other one from being spent. Once you have spent that you can expand out A and you can see that this one is also another level of a conditional covenant. It breaks out giving you a Merklized Abstract Syntax Tree representation at the covenant level.

## Properties

This is pretty interesting because this gives us a lot of possibilities of doing not only the atomic side that goes across blocks, executing in multiple phases but we can also guarantee using virtual UTXOs that this happens all at once as well. We can use this primitive either way. When we are using it in the virtual way there is no extra hash overhead. When we are using in the non-atomic way where it happens across multiple you do need a hash commitment for the new txid that you create. There is a bit of overhead to do it in this new way but it might be worth it for the various types of contract you could be composing. There are also some benefits if you want to have larger scripts or if you want to parallelize your signatures. This makes it slightly easier to do them all at once.

## Transaction Diagrams

Now I have introduced the core idea of this talk, the core principles, the covenants and the Merklization primitives I think it is a little bit abstract and a little bit difficult to see. Generally with Bitcoin things you are looking at a lot of text on the relationships between them. I think having better diagrams would help.

## Primitives: Transaction

To start off I am going to show a very primitive transaction. A is an input and A is spent in a transaction which creates B. Very simple. A could spent to anything else but A just creates B here. Now we are going to get a little bit more complicated. We are going to have an output covenant and so we are going to specify that A now must create B. Borrowing from symbolic electronics we are showing that A is bound to create B. One of its options is to do this.

## Primitives: Conditional Covenant

What if it is conditional? What if we have multiple things? We are going to borrow a multiplexer. We are going to say that you can either construct B or C. You can see in the transaction trace that only one of them could be constructed at a time. You could not construct both B and C from this diagram.

## Primitives: AND Covenants

You could have the opposite. You could have an AND. You could say we want to construct multiple things at once. So the way that we do that is similar. We use a demultiplexer to be a metaphor for this. We would just have two covenants, both get enforced and both outputs get made.

## Primitives: Input Join Covenant

The other type of thing I introduced in this talk was an input join covenant. These are a little bit harder to express. We have an arrow pointing backwards to show you that there is this constraint. Sometimes you have a lot of inputs or you have got a big diagram. Those can get laborious. Anywhere you would see one of these arrows pointing upwards coming out of an output being created that would imply that all of those inputs are bound together. They have to be spent that way.

## Primitives: Impossible Input Covenant (Constructive)

Similarly we can also pretty easily express an impossible input covenant by just explicitly making a marker output that gets consumed by one of the scripts. If NOT B (~B) gets created then this output C can be spent in a transaction to D. If B does get created then C is permanently unspendable.

## Primitives: Impossible Input Covenant

You can see here the beginning of the execution of this impossible input covenant. We spend to the ~B and A branch and we create two outputs. Then we are able to finish the construction and spend C.

## Primitives: Virtual Output

Lastly a virtual output looks something like this. In reality the output is not really creating any coins but sometimes it is useful to think of it in logical order of what it does end up creating. We will kind of lie and give it a dotted outline just to show that it is not permanently there. It is something that has to happen with its parent.

## MAST

Now to show you what a MAST looks like in this diagram notation. You can layer some of these multiplexers together and now there are four possible outputs from the original one. We can show the execution going through there. We can expand out one of these child transactions D to show that D must create some transaction G and H at the same time.

## Shorthand

All of this gets a little bit large and so in general we can compress this notation down very easily and just expand out the size of the bus, shrink everything together and then add an annotation for the depth and how far each of these things goes in a tree. So you do understand that there is some transaction level structure here but it is easier for you to build something that says “These are the possible things but in a compressed manner” so that this thing ends up only taking up log(n) size compared to the number of outputs.

## Techniques for Multi-Phase Execution

So with this in mind, these diagrams that let us show how pieces of the transaction all come together and make inputs and outputs, giving us an idea of the higher order logic flow between transactions. We can talk about multi-phase execution. What happens when you have these multiple components that can execute either together or at different times. You have some problems.

## Stuck State

You can hit stuck states. You can reach nodes that are impossible to have further progress from. The problem is that transactions in a Bitcoin sense can’t be rolled back. Once it is on the chain it is done. You would have to maybe re-org the chain and have a hard fork in order to go back and change what had happened. An example of a trivial stuck state is just this. This is a booby trapped code. There are multiple opportunities for you to fall off a cliff and not be able to reach the promised land of C. You have to be very careful when making a script like this that you don’t have these possibilities to get stuck.

## Simply Non-Stuck

The easiest way to avoid this is just don’t get stuck. Don’t write a program that could ever get stuck. You can do this if you are only using virtual or intermediate outputs. It is pretty easy to do that because you know the entire thing executes all at once or never. But if you want to do a two phase commit protocol, you want to maybe have some secret nonce that gets revealed at a certain point this isn’t really an option and you are going to need to try something else. I am going to give a couple of suggestions. There is a pretty large space of them, ways of thinking about how these transactions should compose.

## Taken-Branch-Elimination Rollback

A pretty simple one is taken branch elimination rollback. What happens is if you go down a branch and then you get stuck you have some timeout period. Then you rollback to the earlier input except you remove the possibility of spending it in the same way to have gone down the same branch. You maybe add another condition saying “Don’t take Branch 1.” The way that this looks in the diagram format would be as follows. You start out being able to go directly to A or being able to go to some covenant to select C. If you timeout at C you have to roll backwards up to the higher version and you are no longer able to roll back to the C branch. You eliminate it if you timeout. That is one option. It is not great because we all know that sometimes our internet connection is down and maybe you are offline for a week and you end up rolling back on some contract. It is not necessarily the best but it is an option.

## Safe High Voltage Switching

To go back to another metaphor. When an electrician is building a safe high voltage system, something that deals with a lot of voltage, they actually have two separate circuits usually. They’ll have one low voltage that deals with the signal for control and they’ll have one high voltage one for delivering the power. I kind of like to think of Bitcoin as being a little bit like that. You’ve got your actual Bitcoin which is worth a lot of money. Then you have your control flow logic which is maybe not worth as much. It would be really nice if we could separate those.

## Optical Isolated Contract

This is what I am calling an optical isolated contract. That is what you use as an electrical engineer. We can kind of use this in Bitcoin too. We separate control flow and access control. These are now two separate things. Impossible input covenants ensure that funds get used properly within in the protocol. This is a pretty complicated topic but I am going to give you a quick diagram which shows you how one of these might work.

Imagine you have some protocol that you are starting. You have two sources of funding M0 which is just providing some source of fees like Ethereum sends fuel for the transaction to run through the network. Then you have M1 which is actually providing quite a lot of Bitcoin, 100 Bitcoin let’s say. As you roll through you would want to say that if it is impossible for me to go to the F program then I would like to be able to recover my coins out of this input. Otherwise they have to be spent to F. If we start rolling forward this way and we execute and we take Covenant A. If Covenant A creates F our funds have to be used with F. But if we roll the other way and we start going here we create NOT F. NOT F serves us the impossible input covenant to show that we are not safe to move into G. What this lets us do is move the actual value of our transaction to the very end phase of a protocol. We can separate out the propagation of value with the control aspect which is a pretty powerful property.

## The Deli Problem

Another social problem you might be familiar with is when you go to a deli and there is no number system. You just get mobbed at the counter. You can’t even see what is going on. In Bitcoin there is a block size problem, there is limited space, a finite resource that everyone is trying to share. When you do go to the deli often times they do have a number and then they orderly call out the numbers. The number allows you to go somewhere else in the store and come back later to fulfill your order.

## Congestion Control

In the same way I think that this technology can be used for congestion control in Bitcoin. If you have some time sensitive operation that you just want to ensure forward progress on but you don’t care for the entire operation to succeed. You just want to commit to what it will be you can use a congestion control protocol using covenants. This works when the size to commit is less than the thing that you’re trying to actually do.

An example I would give for the Lightning Network would be you have some Lightning transaction that is sitting there. You have two options for closing. One that creates some RSMC and some payment out to Alice. The other that creates the same for Bob. You can go through either one but these transactions might be somewhat large. You might not be able to do them all at the same time. If you’ve got a million people trying to close and finite block bandwidth. Instead you can add a congestion control layer. You can say there is a covenant to create this. This should be cheaper because it is just a commitment to a hash. Then you can roll forward one part at a time. You can get the commit which tells you “You can go offline and you will be able to resolve this. You know what state it goes into resolution with.” You don’t need to worry about whether or not your transaction will go through because you are able to share the resource more efficiently across all network participants. This is the kind of thing when you’re building one of these multi-phased protocols you can bake in these congestion control points throughout the entire code. If you do run into a resource constraint situation you are always able to make some amount of forward progress.

## Etc

There are a number of other potential execution techniques that are useful when you’re dealing with these multi-phased protocols. I am not going to go too heavily into them just for the sake of time. I am happy to talk more afterwards about them.

## Quality of Service Matters

In general I would summarize the point of my talk, there are a couple of things. Quality of service matters. If you are building a protocol you can’t just say we are going to make it more resource efficient and more resource efficient. That is a diminishing return. At some point you have some amount of variance and there will be a point where there is limited resource available for everyone on the network for some reason or another. Maybe the internet is just down. I think the key is making these protocols work well when bandwidth is constrained exogenously to your system. Compression techniques can help with that.

## “Secure Contracts Isolate Value”

Another thing is that secure contracts should isolate value. I think it is a bad design when you see a contract that has all the value coming in at the top. That introduces an incentive to try to break that contract at every phase, to be able to extract the money from it. You can always have lower down some kind of timeout but this allows you to make something where there is less incentive to break because they might not even know there is a lot of money attached to it as you are executing your contract.

## Covenants Are Not Evil

Covenants aren’t evil. There are a lot of people in Bitcoin who are very afraid of what covenants could bring. I think there are some pretty low risk ways to introduce them. VUTXOs, virtual UTXOs are one way that I can think if they are only allowed for covenants you get this nice ability to recurse and have your Turing complete computation. That provides a delta zero so it actually doesn’t run with unconstrained resources across the entire network.

## Bitcoin Must Pick Battles

Lastly, Bitcoin has to build its battles. There is a lot of tension between security and complexity in a lot of these things. I think a solution like OP_MAST might introduce more complexity because now you have a big binary blob that is being parsed within a transaction script. That is not necessarily great either. It is maybe better to have higher order primitives that let you program at other levels that keep the base level as simple as possible. That’s my talk. I’m happy to take any questions. Thanks to Neha for helping me prepare this talk.

## Q&A

Q - Do you have a higher level language for writing these?

A - I am happy to help you with that.

Q - I think this is fabulous. I love this diagram notation which could contain pages and pages of Bitcoin Script. I wonder if the next step is to state your security properties that you’re going for and state the goal of the congestion… You might be able to prove that you are reaching that by doing analysis on the diagram.

A - That would be fantastic. This is obviously work in progress so I would be happy to figure out more of how I can express this in a formal context, the benefits of working in this model.


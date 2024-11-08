---
title: 'Simplicity: A New Language for Blockchains'
transcript_by: Michael Folkson
tags:
  - simplicity
date: 2018-01-25
speakers:
  - Russell O’Connor
media: https://www.youtube.com/watch?v=VOeUq3oR2fk
---
Slides: https://cyber.stanford.edu/sites/g/files/sbiybj9936/f/slides-bpase-2018.pdf

Simplicity white paper: https://blockstream.com/simplicity.pdf

## Intro

Good morning everyone. I have been working on a new language for the consensus layer of blockchains and I am here to present that to you today.

## Blockchains and Smart Contracts

I know everyone is familiar with this in the audience but I want to make sure that I’m on the same page with you guys. How do blockchains and smart contracts and programming languages work together? Very briefly a blockchain is a distributed ledger where all the participants share that ledger through a network. Then we append transactions to this ledger to transfer funds between participants. But rather than just sending funds to public keys which are controlled by users Satoshi Nakamoto had this brilliant idea of sending them to little programs and because we have a little programming language, the simplest of which is a program that says “Here is a public key, To authorize transfers out of this thing requires a signature that corresponds to this public key.” We can have little programs and then we can do more sophisticated things where we can have 2-of-2 or 2-of-3 signatures. Then with even more complicated programs we can get escrow and covenants and digital swaps that are atomic etc. Adding a little programming language to your blockchain has vast consequences on the types of things and the usefulness of your blockchain.

## Language Design for Blockchains

So we need to design a language for designing different authorization schemes for these transactions. We have a lot of programming languages out there already in the world so we could just use Javascript maybe. Ethereum’s primary smart contract language is Solidity which is syntactically similar to Javascript. Solidity compiles to machine code for an abstract machine called the EVM. What could go wrong? I don’t want to belabor the point of what could go wrong but lots of things can go wrong.

## Problems with EVM

I think that the problems we’ve seen in Ethereum can be attributed to the design of the EVM. It is difficult to assign costs to the various primitives that are used in the EVM. This has caused denial of service attacks against Ethereum where you can create transactions that consume too many resources whether it is CPU or I/O and grind the network to a halt that way. It is difficult to bound the costs of programs. You’ve created this smart contract but any smart contracting language used on a blockchain has to limit the amount of resources because you are not going to allow unbounded computation to occur in the network. That would be a denial of service attack in itself. There have to be some limits imposed on these transactions. But when you have a Turing complete language or any sophisticated language, by Rice’s theorem it is impossible to come up with upper bounds on the cost of executing the program in all possible inputs. That is not to say you can’t reason about it but there is no universal algorithm to reason about these cost bounds. You have something like gas which prevents programs running forever. But then you enter these contracts where it turns out you don’t actually have sufficient gas to complete them. There are a lot of transactions that get stuck in Ethereum just because it is impossible to provide them with enough gas to achieve their computation. Then related to that is that the complex and informal language semantics makes reasoning about the EVM programs very difficult.

## What about Bitcoin?

So there is an argument to be made that it is really the participants’ responsibility to make sure that their programs are correct. There is a certain truth to that. I think that a lot of the problems can be avoided by taking a look at the language design. What about Bitcoin? This was the first programmable blockchain in addition to being the first blockchain. The problem is that Bitcoin’s programming language is inexpressive. There was a big purge done by Satoshi in 2010. We speculate it was because there were some denial of service attacks in some of the operations in early Bitcoin. There was just a vast purging of operations to ensure that there wouldn’t be a problem going forward. Even poor multiplication got axed. You can add numbers but you can’t multiply them in Bitcoin.

## A language design problem

We have a language design problem here. I like this quote attributed to Tony Hoare. “There are two methods to software design. One is to make the program so simple, there are obviously no errors. The other is to make it so complicated, there are no obvious errors.” We want to aim for the former rather than the latter here.

## What we need is Simplicity

What we need is Simplicity. We need to create a solid foundation for building smart contracts that are simple.

## What is Simplicity?

So what is Simplicity. Simplicity is a low level language that I’ve designed for specifying user defined programs to be evaluated within an adversarial environment. Most of the time when you are writing languages and doing programming you are not in an adversarial situation. You are cooperating with the computer in order to build a program to accomplish some task. Our public blockchains are a different scenario. You are receiving programs from other people and you are executing them. Those people might be trying to create malicious programs to do denial of service attacks and other things.

## Simplicity’s Features

Some of the features in Simplicity’s design. We’ll take a look at the language in a minute. It is a typed combinator language. It is designed to be finitarily-complete instead of Turing complete. That means that for any particular program there are only a finite number of possible inputs that the program will accept. And a finite number of possible outputs. This makes it Turing incomplete. Simplicity comes with simple formal denotational semantics that we specify in the Coq theorem prover. It has formal operational semantics so we can talk about how much time and space Simplicity programs take. And then one of the key advantages is easy static analysis of the computational costs that’s implied by these operational semantics. We will look at these features.

## Type System

The type system for Simplicity is very simple. We only have three basic forms of types. Anyone familiar with functional programming will find these very natural. If you are not familiar with functional programming you might be a little confused. The first basic type is the Unit type. This is the Type with exactly one value in it. In C it is analogous to void. It is not a perfect analogy. Other languages have a Unit type. It just has a single value of that type, call it whatever you want. Then the second is the type former for disjoint union types or Sum types. Here we have a tagged union between types A and types B. It is important that it is a tag here. You can do A + A and you know you have different values for the types of A from the left hand side that are distinct from the values of type A from the right hand side. Then we have Product types which are basically a record type where you have a first component and a second component from types A and types B.

## Expression

Then the Simplicity expressions themselves, they are always functions. An expression t is a function from some sort of input type to some output type. We denote it this way with this notation here. To denote that some Simplicity expression t has input type A and produces output type B.

## Simplicity Language

The core of Simplicity has only these nine combinators. Here are the typing rules that you have for it. Very roughly speaking we have in the top an identity function and a functional composition operator for composing Simplicity programs. Then we have a unit primitive which is a constant function that returns that unit value. Then we have a bunch of operations associated with the disjoint union type to add the tags and do case analysis on the tags. At the bottom we have the operation related to the product types where we can pair up values and we can access the first and second components of inputs that we have over here.

## Denotational Semantics

Then we can write out the denotational semantics for it. It looks like this. The larger point here is that it fits onto a T shirt. We are not at a programming language conference so we don’t have to go into the details of the semantics but it is very simple. It is based on some sequent calculus instead of the lambda calculus. The sequent calculus is well understood.

## Example Expressions

## Bits

With only nine combinators you might be wondering how we might possibly write programs in such a paltry language. We start at the bottom or maybe even below the bottom. We can start defining bits using our type system. A bit is just the disjoint union of the unit type with itself. Remember we have a tag union. We have a tag distinguishing the left unit value from the right unit value. There are two values of this disjoint union 1+1. I like that equation 2 = 1+1. 2 is the notation for a bit. Once we have a bit we can start building machine words. We can take the product of two bits and we can have a bit string of 2 bits which we write 2^2. Once we have bit strings of length 2 we can build bit strings of length 4 by pairing those up and getting 2^4. Then we’ll get 2^8 which is a 8 bit word which is starting to sound a little computery. Then we get 16 bit words, 32 bit words, 64 bit words, 128 bit words and 256 bit words. Now out of 256 bit words we can start doing real cryptography. That’s nice.

## Half-Adder

So what we do is we build a half-adder. Go back to your digital logic course from your undergraduate computer science. We can build a little function that takes 2 input bits and produces the sum. You need two bits in the output type to hold the value of that sum in the worst case. Then you just write this program like that. Once you have your half-adder you can compose those together to get a full adder to add 3 bits together. Once you have your full adder you can build a ripple carry adder to build up your adders for 32 bit words and 256 bit words. You can build multipliers and stuff like that. You just go through your digital logic course and programming course and pretty soon you’ve built the SHA 256 block compression function.

## SHA256 Block Compression

It takes an initial vector of 256 bits and it has a block size of 512 bits and compresses that down to a 256 bit word. I have written this in Simplicity. But because we have formal semantics in Simplicity we can reason about this code and then we have a proof in the Coq proof assistant that this compression function is correct. What does it mean by correct? I’ve taken a specification from the verified software toolchain folks where they verified an implementation of OpenSSL’s SHA256 implementation. They have an implementation that is proven correct in Coq that it meets their specification. I take their exact specification using the formal semantics of Simplicity to prove that my implementation in Simplicity meets that same specification. Now if you put the two formal proofs together we have a proof that the implementation in Simplicity matches the OpenSSL implementation in C. That will be important in a moment.

## Expression DAGs

When you actually represent in memory Simplicity programs it is important to take advantage of sharing of subexpressions. This is what the half-adder looks like inside memory. Diagrammatically we have a bit of sharing going on in the leaves. As you build up full adders and so forth you get more and more sharing of subexpressions. You get a direct acyclic graph, a DAG that represents your expression and when you have lots of sharing you get this exponential decrease in the size of the DAG compared to the size of the abstract syntax tree. That keeps things manageable. This is SHA256, it looks like that. The big blob in the middle is the giant lookup table that they have for all their constants and all the logic is in the bottom corner and there is some composition on top.

## Commitment

How do we use Simplicity inside of a blockchain? We are going to follow this similar to the pay-to-script-hash in Bitcoin. Basically we are going to take our DAG of our Simplicity program and we are going to recursively hash the values of the program following the Merkle tree that follows the abstract syntax tree until we get a hash of the root of your Simplicity program. That becomes a commitment to your program. When you make your output and you want to lock your program you make a commitment to the Merkle root of the DAG of your Simplicity program. That means when you receive coins you don’t have to provide your Simplicity program at that point in time. You can make a commitment by spending to the hash of the Simplicity program. Only when you redeem the coins, only then do you need to show what the actual program is. Then you will check that that Merkle root matches. This is basically the same way that pay-to-script-hash works in Bitcoin.

## Merkle Roots

Here is the simple recursive definition of how to compute a Merkle root. It is very straightforward.

## Witness Values

Another feature of Simplicity is that we have this special witness combinator that makes a constant function for some sort of output value B. For any value B we can create this witness node, this witness expression which is a constant function that ignores its argument and just outputs the constant B. The purpose of the witness point here is that the witness value b itself is not committed as part of the Merkle root. When we compute the definition of the commitment Merkle root for a witness value we can see that its definition does not include the value b. When you have these witness leaves in your Simplicity expression and you compute the Merkle root you get a commitment to everything except for those witness values b.

## Redemption

Then when it comes to redemption time you provide your Simplicity program and you provide the witness values. Then the system will recursively check that the Merkle root matches the commitment. But at that point in time you are free to set those witness values to whatever value you want. At that point in time you will be providing your digital signatures, you’ll be making choices about which branch that you want to redeem with. If you have a multisig, which public keys you are going to be using for your redemption? The system checks that the Merkle root matches and then it evaluates the Simplicity program including these witness values over here to make sure the program returns success. The important point here is that you would think that the Simplicity function which is a function from an input to an output type, that the input type would represent the input to your Simplicity program and the output would represent the output of the Simplicity program. But that is not true. The inputs to your Simplicity program are really provided by these witness values over here which are malleable and that input, output definition for Simplicity is really used for internal composition of Simplicity programs not for top level inputs to your programs.

Another thing is that during redemption if you have unused branches because you made choices where you are not going to utilize part of your code those unused branches can be pruned at redemption time. You just have to provide the Merkle root for those pruned branches and you can still verify that the commitment matches. As long as the execution doesn’t encounter any of those branches that you pruned away it can still determine that you’ve returned success over here. This is great. It decreases the size of your program because you don’t have to reveal all those branches that you are not actually using. It enhances privacy because you don’t have to reveal those branches that you’ve committed to but not used. In this way Simplicity is basically a native MAST programming language.

## More Features

There are other features that are part of the design of Simplicity. We are going to have signature aggregation once that is decided upon. We’ll learn more about that after the break. Covenants and delegation are also on the roadmap for support in Simplicity.

## Operational Semantics

## Bit Machine

I want to talk a little bit about the operational semantics because that is a very important part of the design of Simplicity. The denotational semantics are great about reasoning about programs. We can talk about the correctness of the SHA256 implementation and so forth. But denotational semantics basically says nothing about the operational costs of executing Simplicity. We need to make sure that our Simplicity programs aren’t going to themselves cause denial of service attacks against the network. We need a way of modeling the time and space costs of executing Simplicity programs. In order to model that I have defined this abstract machine called the Bit Machine. It is designed to evaluate Simplicity expressions. It is a state machine that has two stacks, a read frame stack and a write frame stack. There are about ten instructions for the Bit Machine that manipulate the values on these two stacks. It is not like a stack machine that you would see in typical cryptocurrencies just because I have two stacks. Its operation is quite a bit different. But these ten operations, they can push frames onto the write frame stack and copy data from the read frame stack to the write frame stack and manipulate the stack elements.

## Simplicity Costs

You can find more details in the [paper](https://blockstream.com/simplicity.pdf) that is linked in the program. Once we have this abstract machine… The way the evaluation works is the machine traverses the DAG that represents the Simplicity program and it executes these instructions and manipulates the Bit Machine. Once we have the Bit Machine defined we can start asking questions to determine the cost or the weight of Simplicity programs. We can look at the size of the program DAG. We can ask how many steps does the Bit Machine take to execute this program? And what is the maximum amount of memory is allocated by the Bit Machine in any point in time during evaluation. Now we can specify what it means to take a certain amount of time or use a certain amount of memory we can program a static analysis of Simplicity programs to quickly compute upper bounds on the amount of time or space needed to execute Simplicity programs. This is great. The static analysis runs in time linear with the size of the DAG so it is very quick. It gives you upper bounds on the cost or weight of your Simplicity program. Those upper bounds hold for all possible inputs. When you and I are entering into a smart contract we can do this universal static analysis of the Simplicity program. We all know the worst case costs for execution of that smart contract in any context.

## Jets

The astute observer may have noticed that this language is entirely impractical to use for anything. That’s the price of simplicity I guess. We have to address that problem. When you analyze how the Bit Machine operates, it is doing this tree traversal of the DAG, of your Simplicity expression. When it encounters an internal node it processes the subexpression at that point in time. It turns out that all that subexpression can do is read data from a segment in the middle of the top read frame stack and write some output to the middle of the write frame stack. You know exactly what portion of the read frame stack that could possibly be read from. And you know exactly the portion of the write frame stack that will be written to. What you can do is because we have this Merkle root, every subexpression has some sort of name which is basically the hash. It is a Merkle root. We can recognize a commonly used subexpression that appears in lots of programs. We can recognize that and instead of running the Simplicity interpreter to do the computation we can run some sort of C code that does the computation instead. So now looking back to the SHA256 implementation of the compression function for SHA256 we can compute its Merkle root, we can recognize when running the validator “I’ve encountered this node. The subexpression’s Merkle root matches the Merkle root of the SHA256 compression function that I know about.” We have a proof in Coq essentially that proves that the implementation of Simplicity matches the OpenSSL C implementation of the SHA256 compression function. We can go ahead and run the C version and just write the output to the write frame stack of the output of the compression function. This is basically an optimization that the interpreter can do. Then what we can do is create a list of these discounted jets and provide discounts so that you don’t pay the full costs associated with those jets. That incentivizes people to use the jets and makes the costs not entirely prohibitive for running it. In this way by having a rich set of jets we can make the Simplicity language practical. You might be thinking to yourself “Ok you’ve just ruined Simplicity because we now have a whole bunch of jets that are implementing a bunch of behavior and your language is not really just those nine combinators that we set out to start with.” That is true but I think we’ve still gained something by going through this process over here because by using this jet mechanism the jets named themselves by its Merkle root provide a formal specification of the behavior. The C code has to implement exactly the same behavior that the Simplicity program would’ve run if you had run the interpreter itself. By using the Coq proof assistant we can guarantee that sort of behavior. Jets provide formal specification of their behavior inherently. Jets themselves can’t introduce new effects or new behaviors into the language because they can only perform what Simplicity code could have done anyway. Another important point is that jets are transparent when reasoning about their behavior. When it comes to some code that uses a bunch of jets and you are trying to reason about what is going on. You are using the Coq proof assistant to prove some security property or something like that. The jets are transparent. When you are doing the reasoning you can replace the jet with the Simplicity code that specifies the jet’s behavior and you can continue reasoning. Basically you have a single unified language for both specifying the behavior of jets and for composing jets together. I think that is a big advantage.

## Formal Verification

I wanted to talk a bit about formal verification because I think the ultimate vision here is that we want to have a smart contract language that supports the ability to manage hundreds of millions of dollars worth of funds that is possibly custom tailored for whatever purpose the participants in the smart contract want and it might be single purpose in the sense that this smart contract will only ever execute once and then it will be done. And we want to run it in a public blockchain which is probably the most adversarial environment to run these programs in. In my opinion formal verification is the only conceivable way of actually achieving the safety that we need in order to manage millions of dollars on a one-off piece of code that will only be run once and has to execute in the adversarial environment of a public blockchain. Honestly I am not certain formal verification is going to be enough but I believe it is literally the best we can do. I think it is the only game in town.

So to aid formal verification the plan going forward is we have this Simplicity language specification given in Coq. We are going to come up with a C implementation that gives an interpreter for evaluating that and then we are going to use the verified software toolchain to formally verify that the C implementation of the interpreter matches the language semantics on the T shirt or in the Coq proof assistant. This is important because if your implementation doesn’t match the specification of the language, guess what your blockchain’s real language is the thing that you’ve implemented in C not whatever you’ve put on your T shirt. That’s going to be an important step to get a formal link between that. Then we are using C because the CompCert project more or less modulus some hand waviness has a specification of the C programming language. That makes it possible to say the C implementation meets the language semantics of Simplicity. Moreover they have a certified compiler for that C specification that they’ve given and then you can produce x86 Assembly. By combining those proofs together you’ll know that the actual machine code you’ve compiled out is in fact going to give you an interpreter for the Simplicity language itself. There are some projects that take that a little bit further to specify the hardware and get some guarantees about the hardware executing the Assembly correctly and so forth.

Going the other way this is the tail end of a larger formalization effort that is necessary. There is probably going to be some sort of front end language because Simplicity is not designed to be written by hand. It is going to be the target of some compiler. Maybe Ivy or Sigma state language or some of the other ones that we’ve seen yesterday. Or multiple front end languages. If those languages have formal specifications then we can create a formal verified compiler to Simplicity to show that transformation is semantics preserving. We have to go further because smart contracts are composed of lots of little scripting language. We can take the Lightning Network as an example. You have your breach contracts, your payment channels and stuff like that. A smart contract protocol is composed of multiple little bits of these programs that are operating in concert together. We’ll need a specification at the protocol level of what is going on which will produce these front end languages which get compiled to Simplicity and so forth. That is just a protocol specification. Our ultimate goal is to guarantee that some properties of this protocol are achieved. Really we need to formally specify the security properties that we are trying to achieve from our smart contracting language. Then we’ll have to prove that the protocol achieves those security properties. Here you’d use something like the foundational cryptography framework or other similar projects that are ongoing in Coq. That’ll connect to your protocol. The nice thing is that we have all these various projects, Simplicity is just one node in this graph. They are all using the same proof assistant which is the Coq proof assistant. I’m a big fan of the Coq proof assistant. For the argument here the important thing is that they are all in the same system. When you combine all these components that various people are working on, they are all formally connected together and we get to the point where we know that the actual Assembly code that is running the nodes on our blockchain are working in concert to achieve the formal security properties of your smart contract protocol. This is the ultimate goal. We are not going to get there this year or anytime soon. The point is to have a design that supports the ability to achieve this end verification effort. I think that is an important way to design things.

## Solutions provided by Simplicity

To quickly review. What are the solutions provided by Simplicity? We avoid denial of service attacks because we have a simple model for computing resource costs. There are only nine core combinators. It is not hard to analyze the space and time usage of those little bits over there. There is a little bit of an issue with jets but even then the jets are so constrained because they have to only implement what Simplicity can do. I think it will be much more feasible to analyze the computational costs of the individual jets. We can avoid running out of gas because we have a very simple static analysis that bounds the resource costs for arbitrary programs. We have a universal algorithm to determine resource costs. We can try to avoid hacks. I can’t make people produce bug free code but I can provide them with tools that will enable them to formally reason about their smart contracts and have a hope of doing verification. Whether people will or not I don’t know but at least we can provide them the tools. Those people who are willing to provide the expense… If you are going to have a hundred million dollars in a contract maybe it is worth spending 100 thousand dollars or half a million dollars to do the verification effort. If you are running a 100 dollar contract maybe you are just going to wing it. We want to enable that 100 million dollar case. Then we get some privacy benefits and reduce costs because we have this native MAST language. You can read more about Simplicity. The [paper](https://arxiv.org/abs/1711.03028) is on the archive, it is also linked from the program. I guess I have some time for questions.

## Q&A

Q - I like Simplicity. In your program is a conditional statement possible? Also loop? Another question. It looks like you based it on DAG, the data structure. Did you introduce it as a data structure?

A - The DAG is not a data structure, it is the format for holding Simplicity programs. It is not something that the program manipulates itself, it is just the internal representation of the program.

Q - The DAG is a type?

A - The program itself is in expression form. For the branching operator, this case operator that does case analysis on the tag of a disjoint union type. In the case of a bit the contents of the left and right branches of a bit are just the unit types so they contain no information. All the values are contained in the tag. The case analysis for the bit type is an if statement. For loops, there are no loops in Simplicity. There are 64 rounds inside SHA256 and the reason that this program is so compact, you can’t really see it over here, is that those 64 rounds are unfolded. There are no loops so we have to unfold it. Then because we have sharing in the DAG all the body of the loops end up being combined together. If you were to analyze this graph you would see a fan in of 64 arrows. I found it at one point in time pointing over here. We have no loops but we have this replacement for loops that is very effective.

Q - Any conditional statement?

A - Yes the case expression is the conditional statement.

Q - Each cell, in this DAG what kind of type of data in each cell?

A - It is the program. Each one and its descendants represents a subexpression of a program.

Q - Can you talk about the reason why you’ve gone with sequent calculus rather than lambda calculus?

A - Lambda calculus is the natural thing to reach for when aiming for a simple programming language. The problem I have is with function types. In principle you could still do this static analysis with function types, my conjecture, if I’m wrong I’d like to be proven wrong, is that when you do static analysis in the presence of function types you’ll end up with upper bounds that so far exceed the actual bounds of exceeding the program that they will just be impractical values. It is no good if your upper bound that is computed is 2^60 steps for execution or 2^60 cells of memory when you only use a tiny amount in practice. The purpose of the sequent calculus is to avoid function types and I’m expecting that you can still have function types in your front end language. The aim here would be to use defunctionalization to turn a higher order language into a first order language. The people I’ve spoken to about defunctionalization tell me it works very well. I am pinning my hopes on that. For the toy programs I have used so far I have not missed the function types. Keeping in everything in first order seems to be working ok.

Q - For the estimations are there any bounded estimations for the language that you are using?

A - For any Simplicity program there is a universal algorithm that will give you an upper bound on the time and space usage when executed by the abstract Bit Machine.

Q - How close is it to the optimal solution?

A - For the SHA256 expression I have run it on several inputs. All the inputs take the same amount of memory and that memory is within 1 bit of the bound or equal to the bound with a variant that I have.

Q - …

A - The static analysis produces an upper bound but I have no doubt that you can construct programs that force that upper bound to be arbitrarily far away from it. I think those programs aren’t going to be practical. That again is part of the unknowns of this project.

Q - How are you assigning costs to operations? How do you decide the discounts for jets?

A - I haven’t done that part yet. The idea will be to do something very simple like counting the number of nodes. When you have the C implementation, this type for loop that is running through the expression and doing the updates to the Bit Machine. You can count the number of iterations you are going to have through that loop. Some iterations will be faster than other iterations depending on the interpreter they are running I think they are all pretty similar. Regarding discounts for jets that is probably the weakest aspect of this design that we’ll have to do some analysis and come up with arbitrary discounts. I think it will be ok because we have this space of programs that you can write in Simplicity which is fairly large. We have the space of programs that people want to write for smart contracts. And the set of programs that are just infeasible to run on a blockchain. My hope is there is a large gap between those two sets and we can draw a bound roughly in between. We don’t have to be exactly precise about our estimates of computational costs as long as we encompass everything you could reasonably want to run on a blockchain and exclude everything that will be a denial of service attack.

Q - How do the constraints expressible in timelocks fit in to all this?

A - I didn’t discuss this. There are some extra primitives beyond what I stated before. You are going to have some sort of sighash function in Simplicity that produces a digest and provides access to the environment that the program is running in. For covenants we are going to give you fine-grained axis to the components of the transaction data so you can pull out the nLockTime and so forth.

Q - Is there going to be a jet for clients?

A - I am willing to jet anything that I can find a use case for. I plan to very generous with jets. The plan for jets is to look at the type of programs you want to run, look at the subexpressions that make up that program. Even looking at SHA256 we see we want XOR, we want a majority function and stuff like that. We want to go through and find all the various components and provide jets for all of them so people have the flexibility to build what they want.

Q - …

A - It is a bit tricky but I think we can design it so we can soft fork in new jets as we proceed. When we get our post quantum crypto we will be able to add jets that are suitable for that.

Q - I have two questions. You talk about a space that people want to write these types of contract. What do you enable with Simplicity? Today you talk about all these nice properties. What you can prove, what you can formally verify, the notational semantics that’s great. To be able to have all these nice features we simplify hence the name Simplicity. Is there anything that people will want to use and need to use that we will have to exclude in this language design because of the nice properties we want to achieve? The second question is when can we use it?

A - To address your first question. The language design is trying to not make any statements about what people want to do with it or what not to do with it. My hope is that everything that people want to express can be expressed with Simplicity. There are some other features like delegation that enhance the power of Simplicity that go beyond what I have talked about over here. I don’t want to exclude anything reasonable. The only thing I want to exclude are things people might want to do which are prohibitively expensive to run on a blockchain. There are a lot of things that people talk about with smart contracts that I think are entirely infeasible to run on a public blockchain. Unfortunately they will be excluded but they are going to be infeasible to run anyway. Regarding when we can use it, I’m doing that actual thing where people say that they are going to throw away their first implementation and redo it. I am actually doing that. When I made this paper this was basically based on a research prototype, code that you would be embarrassed to share with other people. I am working on redoing that. I can’t provide any particular timeline. I wouldn’t expect any earlier than the second quarter of this year. It will be ready when I think it is presentable.

Q - It is hopeless to compile Solidity contracts to Simplicity?

A - It is necessarily going to be incomplete because there are no infinite loops in Simplicity. The semantics of Simplicity are too narrow.

Q - You could define a subset of Solidity that you could compile to?

A - In principle especially with the delegation feature that I didn’t talk about at all you could take a Solidity program and produce a trace of its output. You could write a Simplicity program that is able to verify the trace of Solidity programs that do something like that. I think it would be totally unreasonable to take this approach but theoretically possible.


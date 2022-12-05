---
title: Stratum v2 
transcript_by: Michael Folkson
tags: ['mining']
speakers: ['Daniela Brozzoni']
date: 2021-02-21
---

Topic: Mining Basics and Stratum v2

Location: Bitcoin Munich

Video: https://www.youtube.com/watch?v=58LrQ0Q89x0

Matt Corallo presentation on BetterHash: https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2019-02-05-matt-corallo-betterhash/

Stratum v1 (BIP 310): https://github.com/bitcoin/bips/blob/master/bip-0310.mediawiki

Stratum v2: https://braiins.com/stratum-v2

Transcript by: Michael Folkson

# Intro (Michael Ep)

Hello and welcome to tonight’s Satoshi’s 21 seminar session hosted by the Bitcoin Munich meetup. We are always looking for good presenters or other contributors for this format by the way. So don’t hesitate to approach us. Our audience is usually a good mix of experienced Bitcoiners as well as more general audience with a good background in tech, finance and other fields as well as newcomers. If you are new today, welcome, price is rising of course. That draws a lot of new interest. Tonight will be a bit technical but feel free to ask any questions you might have. There are no stupid questions. We have also connected a VR room to make this event a little bit more real life like. We already tried this out. If you are in VR we can hear you and we can communicate and you can contribute to the discussion later. Today we will cover some basics on the technical side of Bitcoin mining and then go into some specific details of the new Stratum version 2 protocol. Daniela Brozzoni, from Braiins, will do a presentation. We can also take a lot of time for Q&A and discussions. Another thing, we are here on the Jitsi conference server of the non-profit Freifunk Munich who put up this great infrastructure that can be used by everyone. As you can see it is easy to use and it is free as in beer and free as in speech for non-commercial use. Consider using it yourself, they are happy when people use it, use their bandwidth. Also consider donating to them or even join the non-profit and help build great open infrastructure. As I said, tonight our guest is Daniela Brozzoni. Feel free to introduce yourself and let’s start

# Intro (Daniela Brozzoni)

Hi everyone, thanks for having me. I am Daniela, I at working at Braiins as you said. Not much to say about me, I’m a programmer. I have been working on Bitcoin related companies for 1 year and a half now. That’s pretty much it. Let’s get started. Tonight will be all about mining so we will look into the basics and then we will look into the v2 protocol. Let’s start with the basics and the easiest and most common questions of all.

# Mining basics

What even is a blockchain? The answer won’t surprise you, a blockchain is just a chain of blocks. Each one of those blocks contains some Bitcoin transactions. As you may already know a new block is added every 10 minutes on average. What happens when you send a transaction to the network?

# Sending a transaction to the network

This is you, you are trying to send a transaction from your giant iPhone. What happens is your transactions get sent to the mempool which is this space where all the transactions which haven’t been confirmed yet are. Then someone picks them from the mempool and puts them in blocks. So now you may ask who is the one who is creating blocks? Well miners are creating blocks. Mining is the process of creating new blocks on the blockchain and the miner that finds the new block gets paid. In fact the first transaction in the block is called the coinbase transaction and it sends some money to the miner. It sends the block reward which at the moment is 6.25 Bitcoins and then it sends the sum of the transaction fees. They depend a lot on the state of the mempool. At the moment it is about 1 Bitcoin.

# Who creates blocks?

To find a new blocks the miners have to solve a mathematical puzzle. Every 10 minutes this puzzle is solved by someone and thus a new block is created. When a new block is found all the miners have to start working immediately on the next puzzle. Let’s look into a mining device. It is just a computer that is good at math. It spends all day trying to solve this puzzle, it never gets bored. If you have a lot of those devices you have a mining farm. This is just a lot of mining devices working together usually in the same building owned by the same person. Let’s look a little bit more into this mining puzzle. The only way of solving this puzzle is doing a lot of calculations and then you will find one calculation that solves it. Miners have to be efficient doing so. They can’t waste time not calculating. We have this term which is hash rate. The hash rate is a measure of how many calculations a second a miner does. The higher the hash rate, the higher the chance of finding a solution of the puzzle. Let’s look at this mining puzzle with an example. 

# Mining puzzle: an example

Let’s say the game is rolling dice. The winner is the first who scores less than the target. In this case the target is 3. When you roll the dice it is 4. You are like “Ok I didn’t win.” You try again and it is 6. You still didn’t win. You try again and it is 2 and you won. You found the new block. This is an example to show this mining puzzle works. Only the first one who solves the puzzle wins. If you want a higher chance of winning you have to roll the dice as quickly as possible and you have to not waste any time between rolls. You just want to keep rolling until you find the solution. The same applies for miners even though their mining puzzle is not rolling dices. If they want a higher chance of winning they have to maximize their hash rate aka doing as many calculations as possible per second. They have to avoid wasting time. There are some places where they might be wasting time. They might be a bit slow constructing a new block but they have to do it as quickly as possible. Then they might be a bit slow in switching to the new puzzle. When a new block is found they have to work immediately on the new puzzle without losing any time. Otherwise they are working on an older puzzle and that probably won’t get paid. 

# Mining process

Let’s look at the mining process. What happens when a lot of devices join the network. We have more devices so the overall hash rate of the network increases. A lot more calculations are done every second and so blocks are found more quickly. But we don’t want that, we don’t want blocks created too quickly. We want a block created every 10 minutes. The solution to this is adjusting the game difficulty. By difficulty we mean how many calculations it takes on average to find a solution. Every 2016 blocks the difficulty of the game is adjusted. If the last blocks were created too quickly the games become more difficult. We need more calculations to find the new block. On the other side, if the last blocks were too slow then the game becomes easier. 

# Mining pools

In 2010 the hash rate kept increasing and and it increased very rapidly. The difficulty increased too. For solo miners mining was not profitable anymore. By solo miners we mean those miners with just one farm mining by themselves. The farms with the lower hash rate had a lot of problems finding blocks. Maybe they would find a block once every month and that was not good. The solution for this is using mining pools. Mining pools are a bunch of miners who probably don’t even know each other working together to solve the puzzle. When the puzzle is solved they share the payout. The coinbase transaction pays to the pool address and then the pool shares the rewards with the miners. The miners are paid proportionately to how much hash rate they have. The bigger miners still earn more than the smaller ones. The difference is that the smaller ones get more than one payout a day instead of one payout each month or something like that. This decreases the payout variance. Let’s look at that with an example. Let’s say a certain miner could find on average one block after working for one whole year. One year of all the machines using energy and paying rent and paying the machines and then you find a block. This is a problem obviously. So instead of working alone the miner joins a mining pool. Now the miner gets paid a little bit less because the pool has some fees but still the miner doesn’t have to wait a whole year to get paid. It will get paid a couple of times a day which is way better. The first mining pool was invented in 2010, it is Slush Pool, which is now operated by Braiins. 

How can a mining pool calculate a miner’s hash rate? The pool asks the miners to solve the puzzle with a lower difficulty. This means that the pool is sending you a job which is just a block template. Some data which has to be filled with a solution. When you find a solution you send the solution back to the pool. This is called a “share”. The puzzles which are valid for the pool’s difficulty are used just for calculating your hash rate. For example, you submit 15 shares in 1 minute and the pool knowing that will be able to calculate your hash rate. The puzzles which are valid for the network’s difficulty are broadcasted and those are the new blocks. Note that if a puzzle is valid for the network’s difficulty it is valid for the pool’s difficulty too. We will see why in a moment with an example.

# Mining pools: an example

This time we have two different targets. The first one is the Bitcoin network target which is 3 and the second one is the pool target which is 5. It is easier to find the solution for the pool’s puzzle. You roll the dice and you get a 6. That is not enough either for the Bitcoin network or for the pool. You roll again and you get a 4. That’s not enough for the network but it is enough for the pool. So you just send the solution to the pool. You tell the pool “Hey I solved your game, look at that.” Then if you roll again and you get a 2, you send the solution to the pool and the pool will notice that it is valid for the Bitcoin network so it will broadcast the block and it will get paid.

# Mining basics (but a bit more technical)

Still on the mining basics but a little bit more technical.

# The real mining puzzle

So let’s see what this puzzle really is. The puzzle is “Please find a block whose header hash (we’ll see later what the header of the block is) is lower than the current network target.” The network target is just a number and it depends on the current difficulty. The miners construct the block and manipulate various fields of it to change the header hash. 

# Block structure

Let’s look at how this block is constructed. The block has a header. The header contains the previous block hash which obviously is going to point to the previous block. You can’t change it trying to find a valid hash. You are just going to put the previous block hash and then you don’t touch it. Then the Merkle root, you can think of the Merkle root as a summary of all the transactions in the block including the coinbase. It needs to be recalculated each time the transactions are modified. If you add a transaction, if you remove it, if you shuffle the transaction list, if you modify something, you have to recalculate the Merkle root. Then you can change some bits in the version (see BIP 320). You can use the bits in the nonce field. Nonce just means number used once. It is used only for solving the puzzle. If you see a certain value in the nonce it doesn’t have any real meaning, it is just the miner used the nonce for trying to solve the puzzle. Then you can change a little bit the timestamp. Also you can change the coinbase transaction, that is outside the block header, because it has some bits that aren’t used for anything. You can just change those if you need to look more for the solution. Then you can change the transaction set. You can for example shuffle the transaction list. But you shouldn’t really do it because it may happen that you end up with an invalid block. This is something you don’t want because you won’t get paid. The network will reject it. For example Stratum v2 denies transaction shuffling.

# The real mining puzzle: an example

Let’s look at this real mining puzzle as an example. The device just constructed the block and now has to find the right nonce. The target is `0010` so it tries some different nonces such as 1 and it doesn’t work, 2 and it doesn’t work. After a lot of tries it finally finds the nonce which works. Please notice that it happens a lot of times that you finish searching the nonce, you try all the numbers possible and you still can’t find the solution. You have to change the coinbase data or change the version or the timestamp. That’s it for the basics of mining. Any questions?

# Stratum v2

The first question we may ask is why v2? The fact is that it exists as Stratum v1.

# Stratum v1

This is v1. It was developed in 2012 by the creator SlushPool. It is used by pools and miners to speak with each other but it had some technical flaws such as the messages are not encrypted and the miners didn’t get to construct their own blocks. The pool just gave the block already filled to the miners and they just work on it. But they couldn’t decide the transactions to be included in the block. 

# Mining proxy

One thing you may notice is that there are a lot of open connections from the device to the pool. To reduce the connections on the server side you can use the mining proxies. Those just aggregate hash rate. They look like one single device from the pool side.

# V1 can be improved

As I said v1 had some technical flaws. There were some tries to improve it. The first one was BetterHash which was presented by Matt Corallo in 2018. It allowed miners to construct their own blocks but it was difficult to implement from the pool side so it was never really implemented. Instead in 2019 Corallo joined forces with Pavel Moravec and Jan Capek and they created Stratum v2. 

# Stratum v2 design

Let’s look at the design of v2. It is composed of four different subprotocols. The mining protocol which is the mandatory one and all the other ones it is not mandatory to implement them. Those are the template distribution protocol, the job negotiation protocol and the job distribution protocol. 

# Mining protocol

As I said the mining protocol is the important one. It is the main protocol, it is a direct successor of Stratum v1 and it is used for communication between the devices, the proxies and pools. It addresses some v1 flaws like it prevents man in the middle attacks, it reduces bandwidth consumption and it introduces the concept of mining channels. 

# Prevents man in the middle attacks

Let’s look at what a man in the middle attack is. We have the pool which is sending jobs to the device and the device is sending back shares. In v1 those messages are all exchanged in plaintext. What could happen is you could have a malicious third party which sits in between the pool and the device. First of all this party could read everything and this is an obvious privacy leak because the third party will know everything about your miners. But another attack that this third party could do is it could steal a little bit of your shares and submit them to the pool as if they were their own. In this case you wouldn’t even notice that this happened because if the third party just steals 1 percent of your shares you look at your payouts and you are going to be like “Ok it is a little bit less than usual but maybe I’m unlucky today or something like that.” The bad thing about these attacks is you won’t even notice that you are being attacked. What v2 does is it uses an (AEAD) encryption scheme for all the messages which provides confidentiality and integrity for the messages. No one will be able to read the messages you send to the pool or modify them. 

# Reduces bandwidth consumption

V2 reduces the bandwidth consumption. The protocols goes completely binary instead of JSON based. JSON creates big messages. If you look at the size of a share submission message, in v1 it is about 100 bytes while in v2 it is just 32 bytes without encryption and 48 bytes with encryption so it is a lot better. Then v2 eliminates some redundant messages that weren’t used or not important.

# Supports mining channels

V2 supports mining channels. The downstream devices should open channels with the upstream devices. A channel is not a TCP connection, in fact one TCP connection supports more than one channel. You can just open one connection for all your farm and that will do it. Stratum v2 defines three different mining channels. The standard channels are used for header only mining which is mining without touching the coinbase. If you don’t touch the coinbase it means that you don’t have to recalculate all the Merkle root which is cool. The end mining devices use these standard channels and they are given jobs where they don’t have to touch the Merkle root. There are extended channels which are intended to be used by proxies and they can in fact manipulate the coinbase. What happens is that proxies are sent by the pool in extended channels the jobs. They can touch the coinbase and then they will send to the end devices in standard channels the standard jobs. Then we have group channels which are just some standard channels grouped together. 

# Template distribution protocol

Let’s look at another protocol which is the template distribution protocol. It is used for getting information out of Bitcoin Core. It replaces `getblocktemplate` the RPC call which is in Core. As this protocol is more efficient and more easy to implement as we said before it is super important for miners to be efficient. To not waste time when asking for the new block from Bitcoin Core. It is also used for broadcasting blocks when they are found. In this case when a miner finds a new block it broadcasts it instead of sending it to the pool. This way the pool can censor valid blocks. 

# Job negotiation protocol

Another protocol is the job negotiation protocol and it is used by miners to negotiate a block template with a pool. We have this guy, the negotiator which is another part, it negotiates with the pool for a new template. The result of this negotiation can be reused for all the mining connections to the pool which means you negotiate once for all the mining farm and then all your devices can use that block template. This improves decentralization as the miners can choose their own signaling bits and their own transaction set. But we have to remember that it is still a negotiation.

As a negotiation it might succeed but another case is that it fails. It might happen that the pool tells you that your block template is not right. But it is not the end of the world.

You just ask again to the pool and this negotiation phase goes on until a block template is found. You can just start mining before negotiating it but you can’t start mining if the pool refused your block template because otherwise you won’t get paid by the pool.

There are different reasons for the negotiation to fail. It might be your fault, you included invalid transactions in the block or you put the wrong payout address. But it might also happen that the pool wants to censor certain transactions. It asks you to remove them from the block template. In fact the pool can still do some censorship. It can still avoid mining some transactions but the fact is the miner knows why a certain block template was refused. In this scenario you can go to Twitter and write an angry thread because your mining pool tried to censor some transactions. The censorship is more transparent. For example in v1 you wouldn’t even know if some transactions were being censored because you would just be an end terminal that does calculations but doesn’t even know about the mempool. The point is you can still be censored but at least it will be more transparent. 

# Job distribution protocol

The last protocol is the job distribution protocol. It is used to pass newly negotiated work to the interested nodes, to the proxies who deal with the end devices. Usually proxies are the ones distributing them. 

# Stratum V2 scenario

My last slide is a Stratum v2 scenario with all the protocols being used. The first thing is the template distribution. The negotiator asks Core for the block template and Core answers. Then there is the negotiation phase where the negotiator and the pool negotiate the block template. As I was saying before the negotiator asks “Is my template ok?” and the pool goes “Yes” or “No I don’t like it.” That goes on for a while. Then there is the job distribution. Once you have the job to work on you have to distribute them to all the devices. Then there is the mining protocol which is the devices working and sending the jobs to the proxy and the proxy to the pool etc.

# Questions

If you have any questions feel free to reach out or if you are super shy you can also reach out on Twitter \@danielabrozzoni.

Q - Thank you, great presentation. My question would be in my mind it should be enough if every pool, at least one of the miners is trying to use their own templates to figure out that the pool is denying certain transactions. At least one would be needed and the others can just play along using the templates from the pool?

A - Yes but do you trust that miner to be a good player? Maybe that miner is also trying to censor some transactions. I think the right thing to do would be everyone using that block template. It is like saying “We don’t need to run our own nodes because someone else will do that for us.” Bitcoin works even if you don’t run your own node but you should really do so. Yes it is true, 1 or 10 people running the job negotiation protocol are enough for discovering if a pool is censoring some transactions. But I don’t think you should trust them and avoid negotiating the blocks. Also you have to consider that the block has some bits for signaling. For example in this period we are speaking a lot about Taproot and there are some bits to signal if you are ready for Taproot. You want to run your own negotiator so you can put your own signaling bits in the block you mine. You are voting what you want and not what the pool wants. 

Q - Yeah it makes sense that you do it yourself and not move to the problem to someone else. I want to add that I am against saying that that is voting from the miners because they are only signaling readiness for upgrades. I am against the view that it is voting for the version bits.

A - Ok yeah. I see your point. 

Q - Could you go into the game theory? Why should pools adopt it if they are giving away their power to the individual hashers? Of course there is competition between pools. Are there some considerations there?

A - If you just look at the mining protocol it doesn’t make sense not to upgrade because it is more efficient. But speaking of the other protocols, a bad pool might want to avoid the negotiation to still go on censoring transactions. At least this could reveal bad actors. I see your point. If you are a bad pool I don’t think it makes sense to let the nodes make their own blocks because they will at some point discover that you are not acting fairly. 

Q - Great presentation Daniela. You said the template distribution is going to replace the `getblocktemplate` RPC in Bitcoin Core. Is there potentially going to be a new RPC in Core that does what Stratum v2 does in addition to the `getblocktemplate` RPC that is already there. Are there going to be two RPCs?

A - I don’t think so. Some parts are still not very specified so I’m not sure. I think `getblocktemplate` will be replaced. You don’t need any templates in Core because you just use the node for having all the transactions to put in a block. Everything else you just use your own software. I would say just one RPC to replace `getblocktemplate` and then you don’t need anything else. I think so.

Q - Do you know if people are using the `getblocktemplate` RPC? I have never used it for anything but obviously I haven’t done mining pool type stuff.

A - I’m not sure. I don’t know because I think it is quite slow. Solo miners don’t exist anymore so probably pools have implemented something like `getblocktemplate` for getting out transactions or maybe not, I don’t know. I know for sure there aren’t solo miners using `getblocktemplate` because they don’t exist basically. Not sure about what pools do at the moment.

Q - When you said mining channels is that communication between mining devices?

A - Exactly. The line you draw from a device to a proxy. That is the channel. The point is that it is a subdivision of a TCP connection. You have this physical connection to the pool but in that connection you have 100 channels because you have 100 devices. In the end it all boils down to every time I send a message I just write on the message the channel number. The point is I don’t need 100 TCP connections to speak with the pool. I just need one and on each message I just write the channel number which is basically my device number. It is used for not opening too many connections.

Q - What is the current state of deployment in the wild? Did you have any feedback from miners regarding the migration? Are some of them being apathetic?

A - I don’t know of any feedback at the moment. I do know that the mining protocol, at least some parts of it are in production. If you use SlushPool and Braiins firmware you can use the mining protocol to communicate. Otherwise if you don’t use the mining firmware you can still use a proxy which translates from v2 to v1. Or if you don’t want to use SlushPool and your pool just speaks v1 you can still use a proxy. I don’t know if you saw but Square Crypto is giving some grants for the Stratum v2 development. There is still a bit of code that needs to be written and some things that need to be documented better or specified. That’s pretty much it. It is not very used at the moment I guess but probably will be in the future. I don’t know of any feedback sadly.

Q - Do you know if any other mining pools are interested in offering this?

A - SlushPool, I don’t know of other pools, sorry.

Q - The pool operators, they check the validity of the new block templates asynchronously? 

A - The question was is it asynchronous? I’m not sure. The negotiator sends the template and then the pool replies back. I don’t really know much of the detail of how it is implemented. 

Q - On a lighter note what are your favorite arguments for the common criticisms or misconceptions of the general public about Bitcoin mining? You are working in this field, what is it that you usually explain to your friends and family when you are contributing to boil the oceans (Joke)? What do you say to these kinds of arguments?

A - I think that the main argument is that Bitcoin is polluting too much because it is “wasting” energy. But Bitcoin is not in fact “wasting” energy, it is using energy for doing something cool. If you follow the same argument you could say that Google is wasting energy just by running Google. That’s not true. It is just using energy. Bitcoin is a new cool form of money. I don’t see anything wrong in using some energy to make Bitcoin run. Maybe in the future we will have all the mining farms using green sources of energy. They are even cheaper I guess so it is totally possible. But I don’t really like that argument I usually hear from Bitcoin haters because I don’t think it makes much sense. There are some arguments on Bitcoin itself not being something real, being a bubble. I don’t spend much time discussing against that kind of argument. I don’t spend much time discussing it at all. I don’t usually start angry discussions on Twitter or with family on such arguments.


---
title: Drivechain
speakers:
  - Paul Sztorc
date: 2019-05-27
transcript_by: Bryan Bishop
tags:
  - sidechains
media: https://www.youtube.com/watch?v=BH-qZhEZSrg
---
Drivechain: An interoperability layer-2, Described in terms of the lightning network- something you already understand

<https://twitter.com/kanzure/status/1133202672570519552>

## About me

Okay. So here's some things about myself. I've been a bitcoiner since 2012. I've published bitcoin research on truthcoin.info blog. I've presented at Scaling Bitcoin 1, 2, 3, 4, tabconf, and Building on Bitcoin. My background is in economics and statistics. I worked at Yale Econ Department as a statistician for 2.5 years. My boss from back then won a Nobel prize earlier this year.

## Topic: Drivechain

I try to call this layer 1.5 instead of layer 2. It sneaks between the lightning network and layer 1. You can have lightning network on top of this. Because each piece of software that is a sidechain is going to be the layer 1 of its own blockchain. So this fits in between.

Drivechain aims to provide interoperability, primarily. It can be deployed by soft-fork. It's very slowly being assigned a bip number-- BIP300 and BIP301. The project website is drivechain.info. If you're technical, the BIPs are really good now. They are nice, short and clear. You have to find them by their pull request because only 301 has been assigned a number and luke-jr said he would get around to assigning 300 at some point whenever he gets around to it. I have links on drivechain.info to find the pull requests.

## In one slide

Here's the idea in one slide. The problem is meta-consensus. Consensus would be getting all the nodes to look the same way. We already know how to do that, Satoshi figured it out. Meta-consensus is about humans agreeing what those nodes should be agreeing about. It's consensus about consensus. A good example is the block size debate. Whatever we set the block size to, at least in theory you can get all nodes to agree on a block history given those parameters. But we're not sure what to do about the fact that different people have different ideas about what the nodes could do. Every hypothetical change to bitcoin too, including turing-complete scripts or mimblewimble, these are all things that we could have bitcoin do but we're not sure if we should. We know how to get nodes to agree, but we're not sure how to get humans to agree.

The solution is to have one token that travels between many blockchains. There's 21 million BTC. But there's lots of software that the coins could be using. This idea used to be called sidechains, but unfortunately that word doesn't have as much meaning because the word is used to describe things that aren't even blockchain. Originally it was used for blockchain specific things. But I'm worried that at this point it will cause confusion.

The reason why this is important is because-- why compete to win? When you can simply play all the hands. You can do everything at once. Then you definitely can't lose. Then you can't lose even if someone has some dumb idea; it doesn't matter, you're doing all the things.

## Interoperability

Interoperability is an easy thing to understand but here's some slides about it. It's teamwork plus differences. The team is going to agree on the bare minimum number of things they have to agree on, but then they will disagree about other things. In drivechain, everyone will agree about 21 million coin limit and everyone is going to agree on which piece of software those coins are on.

I had this idea here, this is a representation of that. This is a 21 million coin limit here, and some that are unmined so that's 16 million floating around. In a world with drivechain, probably most of them would be on Bitcoin. But some of them will probably be on some other funny systems like mimblewimble or ring signatures or systems using other things. It could be some really dumb ideas too, and maybe someone puts 50 BTC on it. It's just the interoperability idea.

## How drivechain works

I am going to get to how drivechain works. This soft-fork allows for a new type of output, which I call a "hashrate escrow". Anyone can put bitcoin into it, but money can only be taken out of it in a deliberately slow process gated by the miners. This is more of a curse than a blessing for the miners. They can only extract money slowly and transparently. So instead of sending money to a person, you send it through this process. Escrows are a prison where miners are rewarded; you can choose to go in at any time but it's hard to get out. It's a prison metaphor.

This is hard to explain. After months of trying, I just go straight to an example.

## Example: A payments sidechain similar to lightning

Say you start with bitcoin. This is what the software looks like. Then you add, this is with bip300 and bip301. Then you adds it-- the guy working on this the most is ... he really likes Qt. So he made all of these themes, he has this dark Qt theme. It adds a tab at the top of the Bitcoin Core GUI.

Then you have the meta-consensus problem... where Roger Ver is complaining about transaction fees, and suppose he wants things to work differently than how things work. If Roger runs Bitcoin Core then it has to agree with the other Bitcoin Core nodes. If he doesn't like Bitcoin then he has to use some other thing which is the problem.

So Roger is going to hunt for likeminded community members, create a new blockchain using a drivechain template. This is Bitcoin Core with bip300 and bip301. Then there's a sidechain template fork of Bitcoin Core too. So every sidechain has a new piece of software and in that software you can do anything you like. There's two pieces of software you have to think about-- Bitcoin Core and bitcoin after this soft-fork, and number two what's happening on the sidechain software which you can make it do whatever you like which is the whole point.

Roger and friends are going to fork this, and rename it. It was called "testchain" before, but they are going to call it "Bitcoin Payments". So they can change sigop limits, block size, whatever. This software is like layer 2, or other things, where in order for this software to work it actually needs a Bitcoin Core node. All the sidechains need all the nodes beneath them, so to speak. This is like layer 1.5. This software is going to need to have Bitcoin Core running in the background in the same way that a lightning network node does.

Roger and friends then are going to need to add a new hashrate escrow, a new prison, on Bitcoin. Then they need to tie the payments into their sidechain. This is what happens if you open up that tab in the GUI. One of the things in that tab is a little menu for adding new escrows or new prisons so to speak. So you can see there's some fields here. There's no way to know if the person is doing this intelligently or correctly, but nevertheless they are recommended. This is your opportunity to tie the prison to a piece of software, so we added those fields.

So anyway, just brushing over the details, and assuming that he clicks this button and he does all this stuff correctly. You have this new escrow open. Roger will deposit some huge amount of BTC inside. On layer 1, it shows up here. You can see what's happening on layer 1 and what's only happening on layer 1.5. But anyway, the first thing to happen is Roger puts a lot of money in there. For fun, I decided to have Brian Armstrong put in some money into the escrow too. On layer 1, it looks like 1 UTXO is accumulating a lot of BTC. If you want the number to go down, you trigger a whole different branch of code.

Q: What's special about the escrow output?

A: It's identified when you create this sidechain. It's explicitly brought into existence.

Q: What's different about it from-- someone just looking at the blockchain? How could you tell?

A: The goal is to be able to tell. So if you run the software, then it will list them for you. There's a different kind of script. I'm not exactly sure, since we have changed it a few times. I'm not sure that's relevant though. It would be interesting if I could open up--- the output itself is changing all the time, but we keep track of the most recent one. It becomes something else when someone deposits coins into the escrow again. The software is keeping track of which "thread" is the current latest escrow. I'm not sure if that answers your question or not. It's explicitly identified at first.

Q: What does the script look like? If I am in the code and want to compose a script that updates the balance of the sidechain.

A: Ah, this is a difference between how this works and how every previous soft-fork in bitcoin works. Mostly, transactions go into the script interpreter and then it's either true or false and then a transaction or block is valid or invalid. But in drivechain, transactions have to stick around. The withdrawals have to stick around. They are in an ambiguous state of being valid for a while, and then they default to invalid, but they could become valid over a long time which I am going to explain. I'm not sure if I understand the question. The way this works, there's not just some kind of opcode. That owuldn't work, because ultimately it needs to keep track of the output over time as you will see. I haven't explained that part yet. This isn't like OP\_NOP2 being redefined as CHECKLOCKTIMEVERIFY or whatever. Anyway, they are readily identified. The first output is explicitly created. You mnust do this threading, or it's invalid. This is just a ton of block validity rules. There's not so many transaction rules, as there are block validity rules. Does that make sense? They are not so much about individual transactions as much as this process that is going across different blockchains and between pieces of software. You're trying to keep them in sync. I don't know, does that help at all? I don't know if that helps.

Q: You're accumulating value in an output, and tracking that output.

A: Yes, so far this is like a roach hotel: only one way in. If you don't do that, the transaction is invalid.

Q: How do you identify that output?

A: It's identified by the first output, it's explicitly given to all users.

Q: If I'm scanning the blockchain and I wanted to identify all escrow UTXOs and all sidechains, how would I do this?

A: We have tables in the thing. The GUI will populate it, and track how many escrows there are and what the output is. It's always displaying that for you. There's an RPC command for that, like listsidechainunspentoutputs or something. I don't think it's that important. It's of critical importance I guess. It's something so important that it is already in the GUI table.

Q: What if I wanted to make my own GUI?

A: You would just look at the code for ours and rip out what you like. I don't know the exact line of code off the top of my head.

Q: If I didn't know about your GUI and was looking at the blockchain, how could I pull how many of these exist?

A: You'd look at-- there's a different message. There's a blockchain message for creating one. Then there's block validity rules for whether they are successfully created or not. It's much more clear in the BIP. The BIPs are very short now. I would definitely recommend opening them.

There's like 256 slots. Then people complained, what if we want more than 256 sidechains, which I don't think will ever happen. But you can have a sidechain on a sidechain. You can soft-fork a drivechain and have another 256 byte header and then have more.... I refuse to put in bip301 first because luke-jr really needs to merge bip300 first.

<https://github.com/bitcoin/bips/pulls/642>

I broke it down into these messages: propose new escrow, ACK escrow proposal, propose withdrawal, ACK withdrawal (implied), execute deposit, and execute withdrawal. Here are all the fields you use in a message. Here's exactly what they are and how the messages are constructed. There's a little header here. There's also a commitment header and a commitment hash. If the miners don't care, then the proposal expires. By default, it's thumbs down. This part is not automatic, it's defaulting to not approved. Everyone else has to ACK it, like bip9 version bits. If it gets the 95% thumbs up threshold over some number of blocks, then it turns on.

The one thing to keep track of this is critical output. We call it CTIP though, it's the tip of its own transaction chain. It keeps track of exactly what the-- where this money is. So when you deposit into the hashrate escrow, this could be recomputed by honest nodes and if they don't have something that matches it then they..... there's a table tracking this very specifically. It's probably, I don't know if this is helpful or not, but I hope that it is. Probably it might be better to-- I don't remember, where possible, we added links to code. I don't know where the nearest one is around here. I can instead go back up.

Q: Basically, any nodes that care about what's going on in sidechains, you're just keeping track of OP\_RETURNs that have this format and then you update them as they change?

A: Yes. This stuff is either new in the coinbase transaction, or new stuff in the blockchain. So all of this stuff starts on layer 1, of course.

The third and fourth message proposing a withdrawal, but then the fifth and sixth are about executing a deposit and executing a withdrawal. So all of these messages are defined in the BIP at a byte level. But this answers the question, about how to find if sidechains have been created or not. Then you will know from these messages whether the sidechains were added or not. We added the table to the GUI because people were curious.

Roger puts his money in, and so does Brian. There's only one output. It's 32 bytes. It's not 32 bytes, it's 36 of course. Because it's a txid plus the 4 byte counter thing. So it's 36 bytes. But the point is that, it's being tracked by all the nodes and they know this is a special thread that they can let anyone spend money into it. The amount of money going into the thread is going up then it's always valid. But if it's going down, then that's a withdrawal and they have to check some things.

Now Roger is going all around the world and he's giving away free bitcoin, doing the things that he does, he's running down his wallet and giving away $5 of BTC to everyone in the crowd. He's doing his shtick or something. But different from lightning, none of this would show up in layer 1. There's a lot happneing in the escrow, but it doesn't show up in layer 1. This is like a super aggressive channel factory, where people are onboarding people into layer 1.5 without anything happening on layer 1. They can get onboarded, and then make payments back and forth to each other.

There's something interesting here where I will explain a second thing, which is the blind merged mining. There's a lot to explain here before I go back to explaining drivechain.

## Blind merged mining

There's transactions within the escrow, and they generate transaction fee revenue for miners on layer 1 even if they don't see them. So they are going to try to get 100% of the transaction fees generated on other pieces of software, even if they won't see the transactions. How is that even possible?

The trick is that I assume that among all the people using the sidechain, which hopefully will be a good number of people, everyone using the sidechain also has to use the mainchain because this layer 2 requirement. It's like lightning, where you can't use lightning without using bitcoin. All the people using the sidechain will be using the mainchain as well as the sidechain. I assume that the sidechain blocks, their transaction fees--- but there's someone who happens to own a good amount of mainchain coins, and it's the same person. So they trust themselves completely. That's the trick. They are going to pay themselves the sidechain transaction fees to themselves. They are going to assemble blocks-- the sidechain nodes- they are already running a sidechain node because they are a sidechain user. They have to check a button to do this. They are already running a sidechain node, and they will act like they are miners where they assemble blocks and pay themselves transaction fees, even though they have no hashrate. What they're going to do is, they are going to bribe the mainchain layer 1 miner. They are going to pay those mainchain miners funds to set the coinbase to a certain little thing that will mine the sidechain block. They are going to be earning BTC on the sidechain because they will be mining sidechain blocks. As they collect money on the sidechain, money goes to them. Outside the prison, they will be paying funds out to Jihan Wu or whoever mines the bitcoin blockchain these days.

The summary is that the act of finding a block that is found with blind merge mining, the act of finding a blind merged mined block is completely reduced and transformed-- just by including one new layer 1 transaction. So a bunch of stuff is happening on the sidechain, and users are just bidding. There's some important bytes in here, in the coinbase, and everyone wants their agreed block to be the one that is found. They are paying themselves transaction fees, so they want their block to be found because the sidechain has some amount of BTC in transaction fees and everyone wants it for themselves. If the mainchain coinbase includes a certain set of bytes, then they will win the BTC they mined. So the same person is going to say look to the miners, I'll pay you some amount of BTC if you just set these bytes to a certain field. People can be bidding this up too. It's a contest. Instead of the mining doing all the work, they just do nothing and then they just see whatever is the best offer they get.

Q: Going back to the prison analogy, you have bitcoin being generated by miners on the mainchain, and you also have this escrow here. You have all these people on this sidechain-thing which are trading on top of that escrow and creating blocks.

A: Yes. This is not necessarily the case, but I just assume the stuff in the escrow be its own blockchain. But it could be something really strange, like an exchange but they shouldn't want to do that because it's pointless. It could be something weird. It could be something like Liquid with a paxos-signature thing. Or it could be an R3 Corda-esque thing. It could be anything, people just want to put in money into this process because they think miners will gate it the right way.

Q: Keeping it simple though, assuming there are blocks, they then at some point say they have to get this included on the main chain and they try to bribe miners to do that?

A: These are two separate things. Drivechain and blind merged mining are two separate things which is why I broke it up into two BIPs. Blind merged mining was something that was written to make it very easy for miners to mine sidechains because they don't need to run a sidechain full node anymore. In practice, I imagine they will run a sidechain node. It's just how mining has evolved. You have all these hashers, and they have their ASIC chips, and then they just dial out to some pool operator and the pool operator calls the shots. This is what people seem to prefer, because it's more specialization. The mining pool operator, just running some additional software is a small amount of overhead. It's hard for me to imagine a sidechain or any piece of software that is so burdensome that a bitcoin miner isn't going to want to run it, or the pool operator wouldn't be interested for that matter.

Q: Are they trying to get something from inside the escrow, onto mainnet?

A: Yes. They will calculate what they think the next sidechain block should be, and what the sidechain header should be. People can write sidechains that are horribly designed and don't have headers or blocks, but you shouldn't do that. Fork the template, which is a fork of Bitcoin Core. So then you calculate the header, the hash of the header, and that's what they need-- plus sidechain number and others.

Q: So it's just checkpointing?

A: Yeah, I think so. It's a lot like Counterparty. Instead of including all the Counterparty messages, you're just including one per block that blasts them all together.

Q: I'm curious as to how it is that you could have the next sidechain block decided and then included on mainnet. Miners are making money from both the funds in escrow as well as from mining the next block. What's to prevent two opposing factions within that sidechain or escrow contract from saying this is the next block and both of them to be accepted?

A: That's a good question. There's rules. Both bip301 and bip300 are different soft-forks. bip301 enforces coinbase transaction message format, and mainchain miners are only allowed to blind merged mined... it's a certain part of real estate in the block that is defined, and it's magical real estate. It is defined in a certain way. These next few bytes are magic bytes and the first 37 would be for the sidechain 1, next 37 bytes for sidechain 2, and so on. Those bytes are something. Then the other piece of the puzzle is, to make it trustless, is that this person will broadcast a message into the blockchain and say look if you make those bytes exactly what I say they should be then I'll pay you some amount of BTC. So according to the miners, if nobody has submitted a message like this, this is one transaction that is paying a high bitcoin transaction fee so they will definitely include that one and set the bytes in the header to that value. There's some other rules-- like, they can only include one of those such messages, otherwise they can collect bids from everyone. There's extra rules but thankfully they are quite simple. If you do it more than once, the block is invalid.

Q: So if someone finds a bonus block, then..

A: That's probably a better word for it. The onous is on the sidechain user, this guy, when he assembles the sidechain block, he wants it to be a valid sidechain block and he also doesn't want it to be reorged. He's worried. The mainchain guy just gets paid no matter what, as long as he sets the bytes right. The bytes can be set to invalid blocks on the sidechain. People who run the sidechain nodes will see this. The act of this special real estate being set, is the equivalent of the difficulty requirement being met- it doesn't mean the sidechain block was valid, only that it was broadcast. People might say this is what the next sidechain block is, but they still need to validate that sidechain block.

Q: Who signs off on saying--- what if the pool mines a block where they receive some additional reward? Who is the authority there? How is it decided? There are a lot of people using this sidechain. Who's the one who is proposing this block and who's the one offering this reward to the miners?

A: It's just broadcast all across the network like any other transaction. It's a pretty different concept. We incremented the transaction version number in fact. It's all layer 1 funds, yes.

Q: Again, these miners are getting their normal block reward plus some extra which will eventually get withdrawn?

A: No. That's the distinction, as I was trying to say in bip300 (drivechain), that's going back and forth in the escrow. This is not the same. There should be an image with one arrow like this, actually I did that and I wondered why did I need that. You would have one red hook inside an escrow, and then another one outside where it's two things outside and they are linked because they are controlled by the same person (infinite trust). They are broadcasting messages, and each one is paying a transaction fee.

Q: The miners on mainnet are the ones assembling blocks on the sidechain. So they are routing the coinbase message to themselves. So they are making money on both sides. It was confusing when you said there's bidding.

A: This is the person doing the bid. The miner can be a yet another person. This is the person who is bidding. You need there to be at least two.

Q: So if the miner was a participant in the sidechain, then there would be no bidding.

A: Right. This is supposed to be like, regular merge mining which is already something that probably only 40 people on the whole planet understands, plus some tweaks. With regular merge mining, the miners need to run a node and they get paid in namecoin. There were concerns about, what if someone makes a bizarre sidechain that is also really popular, and you can't easily run the sidechain? This argument is actually invalid, but nonetheless I helped designed this to address this argument even if it doesn't make sense. It goes something like this. You have this giant super popular blockchain and it became de facto mandatory because it was so much money and the only way you could mine was by having a big server farm and that was only 3 miners. So now we shutdown bitcoin. The argument doesn't really make sense, because of the fact that people could-- what it implies is that you can just shutdown bitcoin by paying whatever the sidechain value was, through some other way like having US government cut miners a cheque to... at that point the adversary would be a miner. There were other things that didn't make sense; if you shutdown the server farm, then you could keep mining bitcoin before without the sidechain. So the worst case scenario would be that it had no effect. The only reason I'm bringing up this confusing word salad paragraph is that because this person has settled on conveniences, which is they don't need to run the sidechain if they don't want to, and they can be paid in mainchain BTC immediately.

I think the modern mining landscape is one where a couple people are running pools, and a lot of people have professional power and specialization. I'm not sure, I relaly thin kthe pool operators will run sidechain nodes for the foreseeable future. It's difficult for me to imagine a disaster case where running the hardware is so profitable that they feel must do it, and yet it's so harmful that they feel it would harm the network. The main reason I find this impossible to believe is because regular users have to run the full node for free, and they aren't compensated at all. This is a node you need to use in a data center, but you have a whole network of users using this in concert to pay transaction fees. I don't know if I believe nay of that. Users don't get anything, miners at least get some transaction fees to offset the cost. The true problem is that the users aren't getting compensated at all. If the node is so difficult to run, then I would imagine the network would collapse because people aren't using it.

If you don't run a node, then it will be impossible for you to figure out whether or not miners are stealing when they withdraw money. It's going to be impossible to figure out what's going on when money is being withdrawn.

Q: What's the main advantage of this over lightning?

A: I'm going to get to that.

Q: Let's wait. Please proceed.

A: Okay, that's one vote for proceeding.

I was taking a small detour in our story to talk about blind merged mining. I tried to get it through quickly. Anyway, it generates value for the miners. It's both direct and indirect.

## Sideshift, shapeshift, atomic swaps, etc.

When lay people want to settle their coins back to layer 1, leaving the escrow contract, they are going to be using Shapeshift or Sideshift which charges 1% but you get out of the escrow immediately. It's sort of like prisoner exchange. Inside the escrow, there will be a transaction where Andreas owns some coins in the escrow but in exchange on layer 1 he is going to pay out some guy Jeff. Andreas is going to pay out the customer on layer 1. So we have a new layer 1 transaction. There could have been 10 trillion transactions on the sidechain but so far the layer 1 has only seen the deposits and this different one which is an atomic swap type transaction. This isn't even a drivechain transaction, it's just a "hey if the hash is revealed" type deal. But in practice, since people don't seem to care about that, in the real world what woul dhappen is that Andreas would have a -- people would send him money in the escrow, and it will jus tlook like normal transactions. Most lay people just don't care, so there will be this fluid trust, it's much better than exchange for example. So this begs the question, how does Andreas get his money out? Even though there's specialization and one guy will be paying people out in exchange for 1%. How does Andreas get his money out? He will broadcast a message inside the sidechain software saying I want these coins out. This is the withdrawal transaction. The software aggregates all of these messages. This is what the sidechain template Bitcoin Core fork we wrote does. You're free to do whatever crazy things you want, but I think this is optimal. The software is going to look at these withdrawal requests and say, what transaction do we need to make that happen? Then let's make that happen. What do we need, and the transaction will be defined by a 32 byte txid and these 32 bytes are going to be very important. There's a step-- meanwhile there can be new deposits into the escrow, which can be changing htis. It's done cleverly, so that certain bytes are zeroed out and you can still make deposits to this.

This is a view of the sidechain template inside of the Bitcoin Payments hypothetical sidechain. This is a getblockheader command. The 32 bytes are going to be in here, right now it was 0s because this is just an example and there's nothing. The point of this slide is that the sidechain full nodes are going to know what the 32 bytes are, and then they will be shouting those bytes out in the headers for every block. We are going to promote these 32 bytes to tremendous salience. They are going to be in the header for as long as it takes, either the withdrawal will fail or it will succeed.

On layer 1, someone will put this 32 byte message, they will propose a withdrawal in a layer 1 coinbase message. It starts here. Once per block, it can either go forward, stay where it is, or goes back. It has 6 months to make it out, or it expires. This is already a weird metaphor at this point. If it makes it all the way out, then the transaction that matches this ID can be included in layer 1. Otherwise, it can't. So the 32 bytes make it out, they are out. That means you can include this on layer 1. You still have one that has all the remaining money in the hashrate escrow. But the others got paid out.

Q: The mechanism that layer 1 is seeing to know it's 3 months is because they are all timelocked?

A: Timelock implies that.... it may not imply it, but I think the locktime field is in the transaction. But in this model, this is different from--- usually, a transaction goes into a script interpreter and then it will either be thumbs up or down. It's assembly line and it just goes through. If all the transactions make it through the assembly line then they are and the block is valid. But in drivechain, we loop back through it every time and it has some score. It will accumulate a score. The score can-- the block validity rules allow the score to move up, down or stay where it is. There's a little bit more to say about that, but there's only so much time. I don't know what would happen if I tried to do a presentation about all the things. The rules just say, there's kind of a new database that says, what value is this database allowed to take? This thing is getting a score, and it's going up or down or staying the same. If it get shigh enough, then the transaction that matches it can be included in layer 1. They are not timelocked. This is not a transaction at all, this is just 32 bytes. It's part of a special message in a coinbase transaction. It has nothing to do with the blind merged mining message, which is a different thing. This is just 32 bytes and it's not a transaction at all. There's no timelock, there's no anything, it's just random-looking 32 bytes.

Q: But the miner including it, they...

A: They include it once.

Q: But the miner when it solves the block when it comes up, like it's 3 months later, and it's approved, how do you know it's not the same miner solving that block?

A: It doesn't need to be. The first guy is going to include a message. Later, there's a much smaller message as it moves back and forth, and once it's out, you can include this big transaction on layer 1 here. The way I setup this on the sidechain template is you pay two transaction fees- you pay one transaction fee to the people to include these messages, but then they have a transaction fee waiting over here on layer 1. When the transaction finally gets through, it's just a normal bitcoin transaction like any other. The only message that can take money out of here are the...

Q: These withdrawal transactions are not signed, right?

A: Oh, that's a good point. I think they are signed, but that's only because we were using it to track-- they were watchonly and that wgas the most convenient way to get the nodes to track them. But the private key signing it is publicly known to everyone. So it signs as a ceremony but it doesn't mean anything. There's nothing else gating this money, the money is open for everyone to take it. Anyone can try to take money out, but if it makes the number go down, then the txid has to match this 32 byte value. But they are not signed in any real sense.

Q: So someone still has to publish a transaction once that time finishes. So you could do it after the 3 months.

A: Yes. It will eventually expire in 6 months. If you are very slow, or it's like whatever and you don't get around to it. You only have 1 or 2 blocks to get in, before this thing goes away. It's really only going to pay attention to the frontrunner in any sidechain. If you have a bunch of people trying to do this all at once or after one after each other. Per escrow. Inside of them, you can move any of the 32 bytes, if you move one forward then the others all automaticlaly move back. You can do whatever you want, but you can only have one champion moving forward at the end. The goal of this project is to minimize the auditing. It's no good to hard-fork and have people audit Bitcoin Cash because that defeats the whole point. But you also want to do the opposite-- what you want to, it's hard to explain..... when that transaction is assembled, it should overpay the layer 1 transaction fees because it's like lightning where you don't know what the fees are going to be in the future.

Q: Does the withdrawal transaction have any variability, or masking, or is it just an absolute transaction?

A: Well the escrow output changes so there's some bytes that are zeroed out. It's difficult to do the transaction fee, because the sum is also changing. The transaction fee is just an anyonecanspend output that the miners can spend. There is structure, excellent question. There is structure imposed on the withdrawal transaction. A lot of things can go wrong, money is thrown up into the air, and the software has to be able to send it anywhere. Virtually every part of this is controlled by weird things.

Q: What if there is a reorg?

A: Excellent question. Reorgs-- it depends on .... with reorgs you go back in time. The people who did the reorg could advance it back out in those reorg blocks, or they could do something else. Separately, what do they do to the merged mined sidechain blocks? They could keep them the same, in which case the sidechain history is the same. Or they could make them different in which case they would reorg. But this is much safer from reorgs than a typical transaction. It advances in like 2-3 months. It makes it seem that a representative pool of hashrate really does want to get this transaction in and collect its fees. It depends on what the reorg designer does. The reorgers could decide to move it along, or not. Maybe the transaction makes it out, but then you reorg somewhere in the past. All the sidechains on layer 2, when the mainchain reorgs it back, the sidechain will say this money-- because when the withdrawal is through, the sidechain deletes the money because the sidechain says you withdrew it on layer 1 so now it's deleted. Andreas and Erik say they want to take this money out, and when they finally do the sidechain says oh good you did that and the ndeletes the money and it's gone. If you reorg, it undeletes it.

Q: What about the escrow UTXOs? Won't they be out of sync?

A: If people are depositing to this, it's changing and it will go back to the state at which the reorg branched off. This is changing a lot. That part is zeroed out in the 32 byte txid transaction. It's not a txid exactly, it's clever, it does not look at the bytes for this one escrow output. Those can be anything, it overrides those with zeroes. But this can change as a result of a reorg or any random guy depositing into it. Whatever happens, it's nothing that couldn't have happened originally. A regular payment in a 20 block reorg, you don't know if your payment will be included again. But if your thing already made 2 of the 3 months, then probably it will occur. It is less risk than a regular payment really. The cases where the withdrawal did go through, but the reorg clipped us into a world where it didn't go through, but this probably won't happen because in all the worlds where it went through there was tremendous effort to make it go through.

Q: Is this really merged mining?

A: Not really. Did the terminology of merged mining ever really make sense?

Q: No.

A: I pick terrible names for things and people constantly make fun of the names. I thought escrow was a big improvement over sidechain. But, it's hard to say because-- do you, what do you consider Counterparty to be? Is it merged mining? It kind of is. Every message is a new block. Counterparty had lots of blocks that each had one transaction.

Q: Counterparty had special bitcoin messages.

A: So does this.

Q: But Counterparty didn't require bitcoin miners or pool operators to run other software.

A: Is it really merged mining? Another difference is that with merged mining, you could mine the block without messing with bitcoin at all. In namecoin, you could hash in a separate world. So I see you're one of those 40 people. But here, I decided you can't, it's linked directly and make it much more like lightning network where it's absolutely required that you run and monitor layer 1. This helps with reorgs, otherwise it would be pretty weird. So with this, I just say if you unwind this then you're unwinding all sidechain activity also. Yes. They are slightly different. I think the terminology might be confusing but I don't know what to do about it. The funny thing is, in general terminology in bitcoin is terrible. All the stuff is crazy.

Q: How the withdrawals signed?

Q: There is a signature, it's from the last 5,000 blocks and mining.

A: I agree, that's how I think about it. The people constructing the ledger are in a dynamic membership. It's the same as the DMMS structure from the Blockstream whitepaper. They are slowly building a signature over 13,000 blocks. It's like chizzeling something into a statue or slab of marble. Other than this gate, there's no other requirement on these withdrawal transactions. There's no transaction that just shows up to the script interpreter and then the scrpit interpreter gives it a thumbs up. No. It goes through this gating process and then at the end you get your coins.

## Costs and risks

This is where I start to compare it to the lightning network. With lightning, you don't necessarily need to use lightning.

Q: What makes this layer 1.5 and lightning is layer 2?

A: You can have a sidechain that has its own lightning network nad it could be interoperable.

Q: But you can have a sidechain on lightning itself?

A: I don't think you really can. Lightning is all the things that could be dragged down to the lower layer at any point.

Q: It's the same thing with a drivechain, it's a bunch of things that could be drawn down to layer 1 at any moment.

A: Only through Shapeshift or Sideshift. So I think no. What I'm imagining is that you have layer 1, you have lightning across, and any of those can be dragged down to their blockchain. I feel like it sneaks in. Lightning already took layer 2, they were impolite about the existence of layers between them and layer 1, and there was no more space, so that's how I colonized layer 1.5.

There's a new security consideration. This is a slide I used at Consensus. It was for much dumber people. For lightning network, you need to be able to notice fraud in time, you need to do an emergency broadcast to layer 1 if someone is defrauding you, and you also need to not be too much of a burden if you go AWOL due to the custodial period. You need to be online. That's different. It depends on the use case. For many use cases, that won't matter, but for others, these issues will matter.

For hashrate escrow contracts, what you really want to know is, how much money is-- how invested are the miners in this whole scheme? You want the escrows to be really popular. That's really what you want. It's not that different philosophically from when you use any other piece of secure software, you want a lot of eyes on it and things like that.

In lightning and sideshift, the fees are percent based. And you also have at least 3 layer 1 fees. In lightning, you can't onboard users without layer 1. In lightning, you have to be online and you have to have your private key around, so it's like a hot wallet and that's pretty annoying. In the future I'm sure it will be better but for now that's not great. Lightning is better because it does settle immediately, especially if the buyer and seller are online, like if you want to walk into a store and buy something. Lightning is not immune to griefing or routing attacks. This isn't the free option problem in atomic swaps?

Tadge Dryja became twitter famous temporarily recently because he said lightning isn't useful for micropayments because when you route through hashlock contracts, it expands the transaction by 40 bytes and the fee would have to expand by much more than that and it won't work for super super tiny micropayments. It would still work in channels, is my understanding, I don't see why it wouldn't. So that's slightly different.

## Miner theft

I've already explained what happens when everything goes wrong: say Jihan Wu is going to steal all of Roger's money. He imagines, what transaction do I need to steal the money? He calculates the "evil 32 bytes", and he walks it through the gates, and for 3 months the sidechain nodes are going to freak out and say this doesn't match. Because of the existence of twitter, everyone else will also know. Everyone using the sidechain will know immediately. Other people using a different sidechain will take an interest in this because thye will think "oh maybe I iwll be next" or maybe they will be people pointing and laughing at the situation. Word will get out quickly. If he walks it through, he can put that transaction through and then steal all the money.

The big gun is the UASF (user activated soft-fork). But I don't want to rely on this because you could use a UASF to ensure that the fraud does go through. UASF goes outside of code and just asserts a consensus. It's circular reasoning. It's not a complete infinite regress. The point of talking about the 3 awkward months is that it should be obvious, something dishonest is happening. You have a long time, anyone running the main chain. Anyone running the mainchain will see this proposal in there, and I hate to use this terminology, but you can right-click and you won't let that transaction into the main-chain block ever. There's no coordination problem here. This is strictly superior to several previous incidents, like situations where there has been emergency coordination. Like the overflowing incident in 2011, the March 2013 chain split, and then there was- I would argue the segwit UASF was an example of this but much slower. It's probably a nbetter example because it took multiple months. In the first incident, 140 billion bitcoin was created out of thin air. What you had to do was you had smart people that had to figure out what to do, then have everyone upgrade to fix it. That happened within a few hours. Similarly in March 2013, you had no warning in advance at all, and it was fixed with a lot of creative specialist labor that did this complex thing to fix it and then everyone went on with the plan to fix this thing. All these previous examples, all the rules of the code were being followed to the letter- which was the problem because the code was wrong- and the only thing getting people to switch was their desire to have a more useful protocol. For the UASF that was also the case. There was nothing wrong with the previous rules in any technical sense, but people wanted them to be different, so they coordinated over a timeframe of months to get what they wanted.

If this becomes a popular scheme, then what the miners are going to do when they steal is they are going to destroy their transaction fee revenue from that escrow because nothing will be happening on there anymore and people will give up on it. They will probably not be able to collect any transaction fee revenue, and this will be the end of the sidechains' experiment. The way interoperability must work I think is that there's only three possibilities: you either have altcoins, which nobody really wants, but some people think it's tolerable... but you could make the whole thing mandatory in bitcoin and you could say bitcoin will do everything, and then this is the light touch so to speak, but it's SPV proof. You check the work but not everything else. There's probably some other options in between. But ultimately, it depends on whether or not people come up with cool new software that does something useful. If every altcoin that exists today and will exist in the future is useless, then this project is also worthless and useless and it's probably insecure too.

The other thing to say is that it's only 3 months if there's 100% hashrate. If it's 51% then it will take the full 6 months nad it will take even longer. The other thing you can do is, different miners can move it back and they can move them all back. They could say something fishy is going on, and they can click an alarm. If you have 25% of miners saying look I don't know what's going on, but something crazy is going on..... Also we already have this assumption that there isn't a dishonest evil 51% in bitcoin anyway.

Blocking the UASF costs almost nothing. There's no need for this process to-- in those three previous examples, you needed a lot of specialist creative labor to bring up those fixes. You needed something complicated to be done. But with this, you don't need anything complicated to be done. And the other big difference is that the first two happened without warning, but this thing will be announced at least 2 months in advance for people to figure out what they want to do about it. The big deal is that it can't be accidental, and the miner can't say "oh I had something configured". It's a very slow thing. It's like the UASF. It's a slow read on what miners want. If they want to kill the goose that lays the golden egg, then it means it would be the end of this experiment and the token will only ever be able to do what layer 1 bitcoin can do. Yeah you can UASF and hard-fork maybe change the proof-of-work and attempt to continue. But it's desirable that it be possible and easy to steal money from this thing, because that's what makes it optional. Otherwise it would not be as useful. You want everyone on layer 1 to be able to ignore all of this. If someone makes some weird sidechain, you want everyone else to be able to say look, .... I think I have something like this in the appendix. This is something I tried to explain in Lisbon when I gave a talk. It's basically this, which is that.... with other protocol changes, like, when we added CLTV or CSV, the NOPs changed to real things, this is another way to do interoperability because they are soft-forks. Soft-forks ensure interoperability- which isn't the case if a node rejects the block, but if a node acepts the block then all the other nodes should in theory accept. It's still leaving you in a confused state because over time maybe you haven't upgraded to the latest protocol but other people have, and maybe someone has paid you money and it ewnt through a transaction type that you don't understand... now you're not sure if you really received money. It looks like you got paid, but you don't really know. So you're in a state of permanent confusion until you upgrade. But with drivechain it's slightly better, because there's still a concept of settlement finality which is independent of whether it's the good or evil 32 bytes. The rules are the rules, basically. Once you introduce the UASF for all the weird maneuvers, then that pendulum swings back to the other side.

Q: Wouldn't you need just one person to ... you're counting on everyone to ban that transaction?

A: Yeah.

Q: Do you think this will work repeatedly? Can this technique be counted on 10 times?

A: I don't want to count on it at all. UASF is like weird circular reasoning. It's not a complete infinite ingress. It's like going to court, where you assemble all your documents in advance, then you bring them to court organized and if you don't then Judge Judy will yell at you to get lost or something. So you have to do all this work to prepare this attack in advance. People can just shoot it down 2 weeks before, they might have been on vacation and the nthey just UASF 10 days before. At the last day, the miner has to decide do they want to include this or not. The users of the mainchain don't have to-- they have a long time to decide whether they want to do anything. They could say, I don't want to run any sidechains because they are stupid. But say someone tries to do a theft, maybe a user would suddenly get interested because they want to use a sidechain in the future so they want to protect this and join the UASF and provide political pressure. You have to do all this work upfront in order to do the attack, and it's trivial to right-click and UASF it out. I have a different talk about prediction markets and organizing votes and using lazyness to fix everything. That's my favorite talk to give. The sidechain node is going to be sharding in SPV mode with all the headers. But one thing you could do, a malicious person can fake headers or they could-- they really can't because.... there's no knowing if the headers are actually a valid sidechain, so they could have an invalid sidechain block that correctly pays them all the funds. What you could do is if that there's a real dispute, you have 3 months to figure this out, so let me run the sidechain software and get it. You only need 6 months of history, say, you don't need th ewhole sidechain history because you can take it for granted that the last withdrawals that went through were correct because there were no disputes about those, so you just have to validate the blocks that happened on the sidechain since then.

Q: It sounds like in the worst case, everyone on layer 1 has to do all this watching and download software.

A: Yes, that's the paradox. But people don't have to do it. It's actually good that it's possible for funds to be stolen. That one detail is what makes it all ultimately ignorable.

Q: That's the only way to do scaling, to offload verification to users. In payment channels, users escrowing funds have to verify everything between each other. They are almost creating their own blocks. This is the only way to scale.

Q: At least that's something they are directly using. But the users on layer 1 are not necessarily participating in the sidechains.

A: It does not require its own hashrate, because of the blind merged mining idea. These are kind of like-- plugins, or bonus blocks. It's borrowing... for some reason people are determined to say, oh the sidechain can have proof-of-stake... people ask questions, and a lot of them are possible, but I don't see why anyone would not just use the blind merged mining template the way it is? There are a lot of weird possibilities like maybe you have a second proof-of-work and maybe it alternates or something. But ultimately you don't want the sidechain to have its own hashrate because the sidechain isn't minting its own coins. The sidechain is getting the fees, so yes it could be a fee market. But you could have a nasty correlation where maybe it's 4am EST or something and the transaction fees fall to zero temporarily. Now, there's no incentive to mine the block at all. So if you had your own hashrate, then this would be awkward because you would have to wait or something and it would be strange and it might lead to panic where people say I don't want to use the sidechain because what if tomorrow at 4am this happens again and then everyon ewill abandon the sidechain and there will be no users, no transaction fees and no hashrate. Whereas instead, you could get 100% of bitcoin's hashrate with merged mining for free, and you don't lose any security assumptions. The way this works, if 51% of the miners are against you, they already have so many ways of blocking transactions or messing with withdrawals. There's no loss of security at all, really. Miners are just stopping themselves from earning more money. It's this thing that is just for free, 100% of bitcoin's hashrate really for free, and I don't see why people would do anything else. I keep getting weird emails from people that want things like even and odd blocks and other crazy things.

## Summary

This provides a new source of miner profits and revenue. Miners choice is that it can either claim the revenue or destroy it. There's also high-auditability- you can reduce all transactions down to "net transfers". You can crunching all transfers down to 32 bytes. One transfer at a time, and transfers take 3 months to settle.

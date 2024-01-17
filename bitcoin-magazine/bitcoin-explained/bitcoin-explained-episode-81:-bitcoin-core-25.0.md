---
title: " Bitcoin Explained - Episode 81: Bitcoin Core 25.0 "
transcript_by: edilmedeiros via review.btctranscripts.com
media: https://www.youtube.com/watch?v=TN2P9xwd6ZU
tags: ["bitcoin-core","miniscript","merkle trees","spv","wallet"]
speakers: ["Sjors Provoost","Aaron Van Wirdum"]
categories: ["Podcast"]
date: 2023-06-26
---

# Bitcoin Core 25

Transcript By: Edil Medeiros

Media: https://youtu.be/TN2P9xwd6ZU?si=EhqI7E4Hvqgq3RJW

Sergio Demian Lerner post: https://bitslog.com/2018/06/09/leaf-node-weakness-in-bitcoin-merkle-tree-design/

Aaron van Wirdum (AvW): Live from Utrecht, this is Bitcoin...

Sjors Provoost (SP): Explained.

## Introduction

AvW: Hey, Sjors, we're back.
We're back in beautiful, sunny Utrecht after I spent some time in Miami and Prague.
You spent some time in Prague, and more Prague, is that right?

SP: Mostly Prague.

AvW: You were in Prague for a while. That's where we recorded the previous episode about Stratum V2. 
Now we're back in Utrecht, and we're gonna talk about Bitcoin Core 25, the latest Bitcoin Core release, but it came out a couple of weeks ago.
Because we were traveling, we didn't have time to record this episode, but dear listener, we won't disappoint you.
Here we are with our episode on Bitcoin Core 25.
Before we get there.

SP: It's time for the critical part of the show.

AvW: I will be honest with you, Sjors, I am starting to regret doing the jingle myself.
I do feel like I painted myself in the corner with this one.
But here we go! 

AvW (singing): Sjors stacks sats, Sjors stacks sats, Sjors stacks sats! Y

SP: Yay!
Okay, I guess I'll read one.
We have 250 sats from Unit of Ag, which I would probably read as Prost, as in Cheers, because it's two beer glasses.
And then there's another one from Michael Matulev, Sjor stack sats without a music jingle, and MRMR 1750 sats.

AvW: How do you know that was without the music jingle, Sjors?

SP: Because it doesn't have the music emoji; the last one did.

AvW: Oh, it actually did, and you still didn't sing it?

SP: Yeah, this one doesn't.

AvW: Okay, well, what was the third one?

SP: Whatever, let's move on.

AvW: Sjors, do you still like this part of the episode?
Because I don't think I've heard a single interesting message so far.

SP: Well, we could make the criteria a bit stricter so that the message should actually be interesting before we do the segment.

## Bitcoin Core 25.0 release

AvW: All right, Sjors, stacked, sats.
Sjors, BitcoinCore 25, or 25.0.

SP: Speaking of not very interesting.

AvW: Right, I was gonna say this doesn't strike me as a particularly spectacular release.
I guess at this point, most listeners will know, but just for context: what does it mean that there is a new Bitcoin Core release?

SP: It means that about six months went by since the last Bitcoin Core release.
So whatever makes it in by some date is what goes in.
And then there's some time, maybe a month or two, spent on fixing bugs, not changing anything, just fixing bugs.
And then it's released.

AvW: Right.
That's in contrast with some other types of software that will release a new version once they've included some important new upgrades.
Instead of that, Bitcoin Core releases a new version every six months.
Sometimes it's very interesting and sometimes not much happens in six months.
That's really worth talking about, but we'll still talk about it.
Is that right?

SP: It also depends on your interest.
Because if you look at the actual list of all the little commits that go in there, there's a lot of stuff that's under the hood.
If you find that stuff interesting, then there might actually be much more for you there.

AvW: Sure.
I'm just approaching it from a podcast host perspective and what an average listener might find interesting.
I think this will not be the most spectacular episode, but we're still going to do it short.

SP: That's right.

AvW: Okay, so we highlighted a couple of upgrades that are at least kind of worth talking about.
And we're just going to do them in order of us having written them down in our own show notes.
They're not in order of importance or in order of anything else, right?

SP: That's right.

## Performance improvements related to BRC20

AvW: Okay. So, number one.
There are some performance improvements when it comes to huge transaction loads, and they have something to do with BRC20.
Is that right?

SP: Yeah, that's right.
More in general, what we've seen in the last few months is the inscriptions, the ordinals, and then the BRC20 hypes; and also the stamps hype that we talked about in an earlier episode.
It just causes...

AvW: Hang on.
We spoke about inscriptions and ordinals in a previous episode, as well as stamps.
We have not spoken about BRC20.

SP: No, BRC20 is based on inscriptions, they are inscriptions.
They're inscriptions with a piece of JSON in it, and they are supposed to be smart contracts.
And I'm saying that with a very cynical face and scare quotes because they are not smart, and they're also not contracts.

AvW: So this is also what I thought.
But you're sure about it, they are just using inscriptions, right?
It's kind of counterparty reinvented?

SP: Yes.

AvW: Because that's how it sounds.
It's just the counterparty reinvented, more or less.

SP: Yes.

AvW: Okay.
And there's some kind of performance improvement in Bitcoin Core that has something to do with this.

SP: Generally speaking, what you see is people start using Bitcoin in very different ways.
So the transactions look a little bit different than what you're used to.
For example, you know, in the last episode or a few episodes ago, we talked about how invalid blocks were produced because people were putting multiple signatures in.
That wasn't a problem with Bitcoin Core, that was a problem with the miner software.
But the software just gets stressed out and starts hitting weird corners.
Similarly, these BRC20 transactions are atypically small.
That's sort of one thing you would see about them.
They're not the typical two-input, two-output transactions that you see normally.
They're smaller.

AvW: Why?
What do they look like?
Or what's the deal?

SP: I haven't looked at them in detail, but I think a lot of them are just one-input one-output (transactions).
Because a lot of time, what you do is to update the state of your smart contract.
You're saying: "Okay, my little fluffy image of a dolphin is now for sale."
And that is just one JSON picture or one piece of JSON that you're uploading to the blockchain.
But you're not sending your coins anywhere, so you probably just sent the same coin to yourself with this extra node.

AvW: Right.
We don't have to re-explain how inscriptions work: you just put this data in the witness, and most nodes wouldn't even look at it.
They're very small, like you said because not much else is happening with the transaction.

SP: Right.

AvW: This is the idea. Okay, go on.

SP: It does mean they're a little smaller than expected.
Then, if you really look at how Bitcoin Core deals with things like the mempool and how transactions are relayed to other nodes before they go in a block: they were assuming that was happening at about seven transactions per second. 
With SegWit, that increased a bit.
For this type of usage, it should be slightly higher, too.
The new release contains some improvements to handle these higher numbers.
But I'm being very vague here.
So we should do another episode where we try to explain that in more detail.
I mean, probably when I understand it.

AvW: Or not, because it doesn't sound super interesting.
If I understand you correctly, the Bitcoin Core software is calibrated with certain assumptions about how Bitcoin would usually be used, the software is optimized for that situation.
Now, that situation changed because of BRC20 and inscriptions and all of that.
This new Bitcoin Core release takes this new way of using Bitcoin into account with its assumptions in its code.

SP: Yeah.
The bigger picture here is that in blocks, we have a very hard limit.
There are only so many megabytes that go into a block, so it's much easier to reason about the worst case.
But for the mempool, there are not really any rules because it's not consensus.
So it's a little bit more complicated to make code that handles all mempool scenarios ideally.

AvW: Right, okay.
Now, let's make this as practical as we can.
I'm a casual Bitcoin Core user; what's the benefit for me when I download Bitcoin Core 25?
How does it help me?

SP: Probably when there's another storm of these super small BSC20 transactions, your node will be happier.
And by happier, I mean it's probably gonna make your computer less hot and use less memory...

AvW: ...require less resources.
Okay, I like my computer cooler, so that's good.

## Updates related to miniscripts

AvW: Next point: there are some updates with Miniscripts.
We've done a whole episode on Miniscripts.
Do you remember what episode that was?

SP: I do not.

AvW: Look it up.
In a previous Bitcoin Core Core release episode, we mentioned that something related to Miniscript was implemented, but it wasn't quite there.
It sounds like a new step has been made, right?

SP: Yeah. We described Miniscript several years ago, I think it was one of the first episodes.
It's not a consensus change, it's not a soft fork.
A miniscript is a way to write scripts in a sane manner, because writing Bitcoin scripts by hand is the best way to lose your money.
Using miniscript allows you to write scripts in a safe way.
Bitcoin Core added support for making a watch-only wallet.
That's a wallet that you can see your balance, you can create addresses, you can use Miniscript, and you can receive coins, but you couldn't spend it.
That's not ideal for most people.
This new release does let you spend it.
I'd still say it's pretty experimental.
And there are some edge cases where you can actually not spend it.

AvW: Okay, as a brief recap of Miniscript.
The thing here is that the Bitcoin protocol allows certain kinds of basic smart contract functionalities: it allows multisig, time locks, hash pre-images; it allows a bunch of things.
With Miniscript, it's very easy to implement these things in the smart contract QA, so you can receive coins in a certain way.
So, for example, you can have a board of directors in a company, and they can say, three out of five have to agree or two out of five after a year, whatever.
You can do that kind of stuff.
With Miniscript, you can implement that easily.
Now with Bitcoin Core is where I'm getting lost.
Because this is what the Bitcoin protocol allows.

SP: Yeah, nothing changed in the Bitcoin protocol for Miniscript.

AvW: Right, so what is Bitcoin Core, actually?

SP: Bitcoin Core is really multiple things.
Bitcoin Core is the node, the thing that checks the blocks for validity.
Nothing changed there.
But Bitcoin Core is also a software package that has a wallet built into it.
Anybody's free to build a wallet, there's nothing special about the Bitcoin Core wallet.
In fact, it's probably not one of the most user-friendly wallets, but it is quite powerful.
At least, it's becoming quite powerful.
I think that's a better way to say it, thanks to Miniscript.
This wallet is able to use Miniscript...

AvW: When you say use Miniscript...

SP: It means you can give it a piece of Miniscript and it understands how to create addresses, how to sign transactions using it, etc.

AvW: But you still, MiniScript is literally script.
It's still something you code as a programmer, right?

SP: Yeah.

AvW: So you give that code to the Bitcoin Core wallet.

SP: Yeah.

AvW: We're not talking about the GUI, then.
You have to go into the command line, you paste a piece of code there and this is what Bitcoin Core will understand.

SP: I mean, some people may have been used to pasting xpubs around. 
The way miniscript works in practice is just an xpub with a bunch of extra script around it saying what to do with the xpub.

AvW: Okay this is what you paste in the command line.

SP: Yeah. You paste it in the command line, but there's no reason this could not be added to the user interface too.
It's just that you'll have to paste something magical that you probably don't understand so that's a bit dangerous.

AVW: Okay. So far, Bitcoin Core could understand it, and you could receive the coins.
But they were sitting there in your wallet, and you couldn't actually spend them.

SP: Yeah.

AvW: Sounds like being able to spend them is a pretty good upgrade.

SP: It's one of the nicer features of Bitcoin, although it's good for inflation if people don't, you know...

AvW: Okay, so I guess. Wait, but this is still sort of limited.
It doesn't...

SP: Yeah, I think for most cases that you've described, it'll work.
You can create a PSBT because there are now, I believe, two hardware wallets or maybe three.
The Ledger was first. 
Then I believe it was Coldcard or Bitbox, one of those two, that added support for Miniscript, which means you can make like a multisig wallet with three physically different devices with each of having their own trade-offs.
In order to do that you need PSBTs to move between these devices.
But there are some limits to what you can do.
So there may be some obscure scripts that you can write, you can receive coins on it, but you will not be able to send them to the hardware wallets using a PSBT.
Some edge cases that, if you know Miniscript, you'll probably understand them.
I don't.

AvW: Also, it doesn't work with Taproot yet.

SP: Yeah, that's a bigger drawback, I would say.
MiniScript was designed quite a while ago before Taproot.
It was initially designed for use with SegWit, basically SegWit script.
There's also a Miniscript standard for pre-SegWit script, I think.
But, at least, it was designed for SegWit scripts.
And so there has now been a recent modification to that proposal that makes it work for the Taproot script.
Most of the script is the same between SegWit and Taproot, most of the same opcodes so that you can make signatures, etc.
But there are a few subtle changes in Taproot.
That changes a few things about Miniscript.

AvW: That would be an upgrade in the future, I would assume.

SP: Yeah.
And again, that's one step at a time.
The first step would be that you can write miniscripts, and then it'll generate a script leaf in Taproot because you can put your individual scripts in individual leaves in the tree.
But there's no way yet to decide how to distribute your scripts between all the leaves most efficiently.
If you have five different conditions, do you want to make five leaves in taproot, or do you want to make one leaf that does two of them?
That sort of stuff, there's no tooling for that yet.

AvW: Right.

SP: Soon, TM.

## Fast wallet rescan

AvW: Two weeks.
We've mentioned two improvements so far. 
One of which was the transaction loads, BRC20.
And then we now mentioned Miniscript.
Now we're getting to the third one.
And that's actually the last one already.

SP: Fast wallet rescan.

AvW: Fast wallet rescan.
Sjors, explain.

SP: So, Bitcoin Core has a wallet built into it.
Let's say you first used that in 2012 and you received some Bitcoin. 
Then you were like: "okay, let me put this wallet on a USB stick, put it in a vault somewhere physically, so the whole wallet, not just the backup codes, the actual file and remove it from my computer because I'm traveling around with it".
Your node just keeps updating, keeps syncing, keeps syncing, keeps syncing.
Now you come back and you put the USB stick back into your computer. 
Maybe that's a bad idea if there's a lot of money on it, but let's say you do.
Then, your wallet is behind, in a sense, because the new transactions that happened since 2012 would not be in that wallet file, because it was in your vault.
And your node doesn't really track them either, not specifically, it just has all the blocks.
So, there's something called a rescan, in which the wallet file...

AvW: Wait, wait, wait, wait.
Because it is confusing.
I think what you mean to say is you received coins in one wallet, and now, after that, you started using a new wallet, right?
When you say "syncing, syncing, syncing", your node is not syncing based on that wallet anymore.

SP: Yeah, your node is still syncing.
It just stores all the blocks and checks their validity.
But it's not keeping track of how that matters for your wallet.

AvW: Right.
So you basically reinstalled Bitcoin Core or something like that.
You got a new computer, something like that?

SP: No, you can basically unload a wallet and then load it again.
But I guess another scenario would be, yes.
So you are restoring, you're reinstalling Bitcoin Core, and you're recovering your wallet.
You're trying to see if there are any coins in that wallet and find the transactions.
The only way to do that is to go through all the blocks and check if there's something useful in that block.
This takes a long time, it could be several hours.

### Advertisement 

We are prond to have Voltage as a sponsor of this episode. 
How many of you developers out there have wanted a streamlined infrastructure provider for your particular project.
Well, I'll tell you what: Voltage is the Bitcoin infrastructure provider you have been looking for that makes building on Bitcoin quick and easy, whether it's Bitcoin nodes, Lightning nodes, BTCPay, and so much more.
But don't take it from me.
Just ask the guys over at Amboss, Sphinx, Podcast Index, Thunder Games, and so many others that you guys already know and love.
Their enterprise-grade products make it fast and easy to build, deploy, and scale your next project.
So make it easy on yourself.
Even normie plebs can use the dashboard or API.
Don't wait before the next block confirmation.
Let your team focus on building great products, and let Voltage handle all the rest.
Voltage is your go-to zero management Bitcoin infrastructure solution.

### Back to fast wallet rescan

AvW: That's not so bad.

SP: It depends on your patience.

AvW: I guess we can do better than that.

SP: Yes, we can.

AvW: So how do we do better?

SP: This is using the neutrino filters that we did in earlier episode about the compact block filters.
I forgot the episode. Look for "Bitcoin Explained Neutrino", and you'll find it.
The idea there is that light wallets can use these filters to figure out which blocks they need to download.
Instead of downloading all the blocks, a mobile wallet can figure out by itself, without revealing any private information to the outside world, which blocks it should download.
In order to do that, it needs to download something called these filters.
These filters are much smaller than normal blocks.
Bitcoin Core can create these filters and now the wallet will take advantage of that because rather than scanning every block from the history from the last time you checked your wallet, it now knows which blocks it needs to scan.
And so it'll scan fewer blocks, which is faster.

AvW: Wait.
So if I have a wallet.dat file on a USB stick, as we discussed, that's the example we're using.
I buy a new computer tomorrow and I sync Bitcoin Core.
Now I get the wallet.dat file.
Somehow Bitcoin Core would know which blocks to download based on the wallet.dat?

SP: The wallet.dat file contains the addresses that belong to your wallet.
Depending on how old it is, that's gonna be somewhere between 2000 and 8000, because it basically creates a cache of addresses.
It knows these addresses, and yet, using these filters which Bitcoin Core will also have created, it's able to know which blocks are relevant and which blocks are not, because these filters are like a compressed summary of the blocks.
It looks at the filters and it says: "Okay, if I run my addresses through this filter, does it say yes or no?"
If it says yes, I'm gonna download the block and check everything.
The filters are not accurate, so it's possible that you might download ten times more blocks than you really need, but you're not downloading them all.
In the case of Bitcoin Core it's not even about downloading them, it's just about checking them.

AvW: So it doesn't work with a pruned node, right?
You do need to have all the blocks available.

SP: Correct. At the moment, it does not work with a pruned node.
If you have these filters on your computer, but have pruned blocks, you would be able to know which blocks to download again which currently you can only do with some manual magic.
It is possible with the pruned node, but then you need a script.
I've tried this myself, like experimenting with it.
You can... Yeah, you can scan...
I don't know if I tried this myself, I may not.
No, I think I'm lying here.
In theory, it's possible to download all the blocks that you're missing and then scan them, but the wallet will be very confused.

AvW: Okay. I don't understand how this works, but that's probably because I forgot how Neutrino works.
So, if I want to understand that, I would have to go back to our own episode and listen to that.

SP: Sounds good.

AvW: Unless, Sjors, you want to try explaining this right now?

SP: Did you forget how Neutrino works?

AvW: I mean, I don't remember.

SP: I just told you.
So the idea is if you're...

AvW: I mean, I understand the idea. I just don't understand why that...

SP: Why it works?

AvW: I don't understand.

SP: It's magical math.

AvW: Yes, exactly.
I feel that at some point I understood it more than just magical math, but not right now.

SP: The magical math basically says that you've done some calculations before to make a filter from a block and then you can check against the filter. 
You say "do these addresses belong to this block or not?"
That is it.

AvW: Okay, do you want just to leave it there?

SP: Yeah, because that's about as well as I can explain it.

AvW: Okay, we'll leave it there.
If you want to know more, I think we go a little bit more in-depth in our actual Neutrino episode.

## 65 byte transactions

SP: We missed a topic.

AvW: I wasn't done, Sjors.
I think you will bring up the RBF, the full RBF.

SP: No, no, no, no.

SP: The 65 byte transactions.

AvW: Oh, you're right, we missed a topic.
Sjors, you're so sharp today.
Luckily, because I'm apparently not.
So yes, there's something going on with the minimum size of transactions.

SP: Yeah, we added more freedom to the mempool.

AvW: Is that so?

SP: Yes.

AvW: Okay, explain.

SP: Remember there is consensus, which are the rules for the blocks, and there's standardness, which are rules for the mempool.
Generally, the standardness rules are stricter than the consensus rules.
In fact, that's always the case.
In other words, There are some transactions that are perfectly fine in a block, but they are not fine in the mempool.
This has to do with preventing denial of service attacks on your node.
In this case, though, it's not really that.
There is a minimum size.
I believe it was 84 bytes, so, any transaction that's less than 84 bytes would not be relayed by nodes.
If it's in a block, it's fine.

AvW: Is there a minimum size (for transactions) to be in blocks at all?

SP: I don't think so.
There's probably a minimum practical size because you must point to a previous transaction, etc.

AvW: There's an actual minimum size that a transaction can be, but there's no consensus rule for it.

SP: I guess you'd say there's an inherent minimum size.
It follows from what has to be in a transaction.
But other than that, I don't think there's a number.

AvW: Okay, but there is a minimum size for the mempool policy.

SP: I think it was something like 82 or 84, some number.
And this number has decreased.
Now it's 65.

AvW: Why?

SP: There's some use for it. 
I think the idea is that it makes it a little bit easier to burn coins if you need to.

AvW: To burn coins?

SP: Yeah, if you have some dust that you want to get rid of.
You want to remove it from the UTXO set.

AvW: Okay.

SP: I think it's easier to do that with smaller transactions.
But the...

AvW: Wait, what?
Why would you want to do that?

SP: Because you want to clean up the UTXO set.

AvW: But you literally want to throw away coins?

SP: You'd throw away coins that are not economical.

AvW: Why not just leave it alone?

SP: Because it's sitting in people's memory and using up resources.
Be a good citizen and clean up your UTXOs.

AvW: I guess, okay, yeah, go on.

SP: I think this was proposed by Greg Sanders ([instagibbs](https://github.com/instagibbs)).
He's working on ephemeral anchors, which are ways to combine two transactions that are paying a zero fee and then one is bumping the other.
Maybe those transactions are actually smaller, and maybe that's why he needs it.
I haven't looked at the reasoning.
In any case, it's possible, so it's done.
The original reason is kind of funny.
The original limit was made this weird number like 82 or 84 because if they had made it 65, then the bad people would have understood why it was done, and they might have been able to exploit something before the fix was released.
So this is a case of you have a vulnerability, you know that if people make 64 byte transactions, they can cause problems.
You don't want to give that away too obviously.
So you say, yeah, we won't make the limit 65.
We will make it like 84 and then make up some excuse for why 84 is a good number.
Because nobody needed it.

AvW: This is super confusing.
Luckily, I know what you're talking about.

SP: All right. Well, maybe you can explain it.

AvW: Yes. So you mentioned the original number, and you said that it was 82.
So that's the confusing part.
No. The original number was 64.
That was a minimum of 64.
And then it was increased?

SP: No, no, there was no minimum.
But it had to be increased above 64.

AvW: Oh, so it was not 64?

SP: No, I think it was just...

AvW: So there was no minimum?
Yeah, okay, okay.
So there was no minimum.
And then a minimum was imposed.
When was this?

SP: I think it was 2017, maybe earlier.

AvW: Oh, a while ago.

SP: It might have been done even earlier.

AvW: Then a minimum was imposed, and that minimum was 84.

SP: Something like that.

AvW: And now that has been decreased to 65.

SP: Exactly.

AvW: What you're saying is the reason that 84 was picked originally is because 65 would have been ideal, but they didn't want to do that because it would reveal something.
So they picked 84, which was a little bit more off to the side, and then attackers wouldn't notice it, hopefully.

SP: That's right.

AvW: What was wrong with? Why is 64 a magical number?

SP: In fact, the strict rule that you really need is not 64.
It can be smaller than 64, it can be bigger than 64, but you don't want 64.
The reason has to do with Merkle trees.
We've talked about Merkle trees in earlier episodes.
We even tried to explain Merkle trees in earlier episodes, I think we should not try that again.

AvW: Probably multiple times.

SP: What it looks like is you take two transactions side by side, and then you hash.
No, you take two transactions, you hash each of them, and you put the hash of the first transaction on the left, the hash of the second transaction on the right.
And the hash of a transaction is how many bytes?

AvW: 64!

SP: No. 

AvW: Oh.

SP: The hash of a transaction is...

AvW: I don't know. Should I know?

SP: It's called SHA256.
The 256 stands for the number of bits.
256 divided by 8 is 32.

AvW: Okay.

SP: So, the hash is 32 bytes.
You put two of them next to each other.
That is 64.

AvW: Right.

SP: Then, you know, this tree goes up and up and up, you keep combining two.
So every...

AvW: What? This is not how a Merkle tree works.

SP: That's exactly how a Merkle tree works, at least how it works in Bitcoin.
You start with transactions at the bottom, you pair them, and then you hash each of them.
You put the hashes next to each other, so 32 bytes next to 32 bytes, that's 64 bytes in total.

AvW: Right, yeah, hash these together, right?

SP: Yeah, exactly.

SP: The problem is that if you implemented the Merkle tree well it would be clear how many leaves there would be.
You would basically say this is a Merkle tree and has so many leaves.
Somebody who looks at the Merkle tree can extract it and see these are all transaction hashes.
The problem is, in Bitcoin, it's done unsafely and this has caused problems in the past.
Anything that's 64 bytes can be either a transaction of 64 bytes or it can be one of these points inside the Merkle tree.

AvW: Okay, they look the same.
I just want to clarify...

SP: They look the same.
That is where multiple attacks have come from, including much older ones where you could create a block, then you would pretend that the block is invalid and send the same thing again. 
All sorts of nasty things.

AvW: I want to clarify: we're getting really into the weeds with weird niche, but interesting attacks, here.
So, yeah, okay.
The transaction hash is 32 bytes...
I'm not going to try to re-explain this one even, but I was kind of following you. 

SP: Transaction height is 32 bytes.
You put two of them next to each other, and now you have 64 bytes.

AvW: Yes.

SP: So, what does that mean?
Well, I think it was Sergio who...

AvW: Sergio Demian Lerner.

SP: ... who wrote a blog post in 2017 explaining exactly what you can do to attack the user of an SPV wallet.

AvW: I'll add the link to the article in the show notes.

SP: You definitely want to read it.
I'll try to explain it at some high level, but I find it confusing.

AvW: Go for it.

SP: What is important to know is that it's an attack on SPV wallets, these are wallets that do not download full blocks but only get a summary.
They get something called an SPV proof, which is saying "hey, this transaction exists, it's inside this block", and then you give it all the block headers so the SPV wallet knows there's some proof of work on top of this transaction.
It can't check all the consensus rules, but at least it knows some miner paid a lot of money to make this thing.
That's a kind of wallet use that's not very common anymore because there are all sorts of problems with it, including the one we're about to describe.
If you have a few million dollars in budget, you can perform this attack and this was in 2017.
I think you also need to have a pretty substantial amount of Bitcoin to do that which was cheaper back then.
You create a 64-byte transaction and you pretend that it is part of this Merkle tree or the other way around.
This is where I get confused.
The idea here is, because a transaction is hashed into 32 bytes, and there are two of them next to each other, that means that you can basically start making a...
How do you say this?
There are certain parts of the transactions that can be whatever you want.
So you don't have actually to find a SHA256 preimage. 
You have to try far fewer random transactions to be able to craft a transaction that looks like this.
One of the tricks he does is he doesn't care about the amount in advance, so how many amounts can there be?
There are just several bytes worth of what the amounts can be.
So you basically keep looking for transactions with random different amounts.
Once you find the right hash, you use it and you send money to yourself.
Anyway, you should read the blog post, but the attack is quite expensive.

AvW: Can I summarize this?
Here's the summary: SPV wallets are not secure if you want to accept millions of dollars worth of Bitcoin.

SP: Assuming his calculation is correct, it would cost several million to do this attack at the time.
If you are receiving more than a few million, you should absolutely run a full node.

AvW: There are some weird quirks in the Bitcoin protocol and miner incentives. 
SPV is not secure for that.

SP: No, and this attack also requires collaboration from a miner.
If you have collaboration from the miner anyway, you might as well do a noble double spend.

AvW: Right.

SP: I think the target audience for this attack was automated systems that use SPV proofs. 
I think, at the time, Liquid and RSK had some components that were fully automated and would use these SPV proofs. 
They would have lots of money in them.

AvW: Okay. Now I want to ask you, Bitcoin Core made this change?
Apparently they made the change a couple of years ago, actually.
It's only now, I guess the developer figured most people have now upgraded, so now we can stop pretending that 84 was...

SP: No, the pretending stopped earlier.
I think it was changed in 2017 without any explanation, although his blog post was around the same time.
Then in 2019 there were comments added to the source code saying actually this is nonsense but this is the reason.
Only now somebody bothered to actually change the limit, which is because nobody needed it.
And the other irony is...

AvW: So why is it needed now?

SP: I don't know.
I mean, that's what we speculated on earlier.
Maybe it's easier to burn money, or it has something to do with these ephemeral anchors.
I didn't study it in enough detail.

AvW: Okay. Anyway, so now the limit is 65.
However, even now, that's only a policy change.

SP: Yeah. The irony is this never prevented the attack because the attack as described actually requires being a miner or at least working with a miner.
It's ironic because a miner doesn't care about standards and rules.
It was a step, like, okay.
But there's something called defense in depth where you say, "okay, we think only a miner can do this, but maybe somebody else figures out a way to do it without the help of a miner".
It still helps to make it more difficult to relay these things.
And there is a software proposal called the Great Consensus Cleanup, which Matt Carollo proposed in 2017.

AvW: We may done an episode on that or no.

SP: Yep, and one of the parts of that proposal was to make the minimum transaction size 65 bytes.
That would be consensus change.

AvW: Right.

SP: Which is precisely for this reason.

## Replace-by-fee implementation release

AvW: Right, but that's not what this is.
I feel we're getting really into the weeds with this Bitcoin Core 25 episode, Sjors.
I think this is a very niche upgrade, but it's an upgrade.
We've now covered four topics.
We're done with this one, right?

SP: I think we've covered four of them.

AvW: Good. Are we done with the episode?

SP: I think so.

AvW: I mean that was this other thing you wanted to mention maybe something about the full RBF (replace-by-fee) release.

SP: Yeah, there's an alternative implementation which you can download at your own risk.
Make sure to check all the signatures.

AvW: Is this is Peter Todd's implementation?

SP: Yes, Peter Todd, I think, together with Antoine Riard.
They're lobbying the full RBF thing, which we've done plenty of episodes about.
It's essentially Bitcoin Core 25 plus the full RBF stuff.
The one thing that's interesting about it is that when you turn on full RBF, you're able to replace transactions without setting the RBF signal.
But if you're sending it to your peers, none of those peers might relay it.
So, you want to find other nodes out there in the network that also support this feature.
There's something called service flags in which nodes can communicate that they have this feature and deliberately connect to him.
This patch does that.
But I should warn you that changing peer-to-peer code is always very scary.
If just one or two people are doing that, I don't know, it's up to you.

## Farewell message

AvW: Anyways, this is not Bitcoin Core really, and we were talking about Bitcoin Core.
So that's the episode then, Sjors.

SP: That's right.

AvW: Bitcoin Core 25 is released.
Where can people find it?

SP: BitcoinCore.org.

AvW: There you go.

SP: Thank you for listening to Bitcoin...

AvW: Explained.

## Bitcoin 2024 Conference Advertisement

Thank you Miami, for the last three years in this amazing city.
The whole world shut down, but Miami welcomed us with open arms.
We want to show Bitcoin to the whole world.
We are taking the conference on the road to set the stage for Bitcoin in a new city: Nashville.
Bitcoin 2024 is coming to Nashville,Tennessee.
A city that is known as a music and freedom city.
Bitcoin 2024 in Nashville from July 25th to 27th.


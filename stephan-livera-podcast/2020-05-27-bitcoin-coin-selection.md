---
title: Bitcoin Coin Selection - Managing Large Wallets
transcript_by: Stephan Livera
speakers:
  - Mark Erhardt
date: 2020-05-27
media: https://www.youtube.com/watch?v=B3wn6JC0aWc
---
podcast: https://stephanlivera.com/episode/177/

Stephan Livera:

Welcome, Murch.

Murch:

Hey, Stephan, thanks for having me.

Stephan Livera:

Well, yeah, thanks for joining me, man. I am a fan. I’ve read some of your work on coin selection. And I know you’ve, you’re you’re the man to talk to about this topic. So look, let’s start with how you got into Bitcoin and Bitcoin contribution and also just some of your work at BitGo.

Murch:

Yeah, sure. I started following Bitcoin about 2011, 2012. I don’t remember exactly. I just like the third time it swept through my media stream, I realized, Hey, this is coming up again. And I actually read the white paper and then I was like, wait, that might actually work. And so pretty early on I found Bitcoin Stack Exchange, while like a Bitcointalk was already fairly noisy and Reddit was a mixed bag because stack exchange just answered all my questions with usually pretty high quality posts. And I tried writing a few answers myself at first, but they got heavily corrected or I even deleted them because they were crap. But after awhile I got better at it. Now I’ve been doing that for almost seven years. Six years as a moderator. And about three years ago when I finished my thesis, I wrote a thesis on coin selection was studying computer science and for my master’s degree I was looking for a topic and I found out that there was a lab at my university that was looking into blockchain stuff. So after a few weeks of waiting, because my prospective advisor was on vacation, I rolled up in his office and was like, Hey, I want to write about coin selection. And I prepared a bit of an idea here. Here’s like a page. And he’s like, okay, turns around a stack of paper. I had a few ideas, but let’s do that.

Stephan Livera:

That’s awesome man. And I think it’s really interesting because in terms of online Bitcoin discussion, you see, well you’ve got like the old school stuff. So Bitcointalk was the forum. That was the main thing then and then there was the Bitcoin subreddit. But in terms of technical forums for discussion, you pretty much have, okay, so there’s the IRC channels, you’ve got the mailing list for discussion and you’ve pretty much got Stack Exchange, right? Because that’s where the more technical discussion actually occurs. And so for listeners who are unfamiliar, tell us a little bit about the sort of questions and some of the things they might see on Bitcoin stack exchange?

Murch:

I mean, the nice thing is just when you have a single question, you can usually either find it there or just ask a single question and you’ll get all the best answers for it. And other people will look over those answers and correct them or provide their own to supersede a not so optimal answer. And you end up getting this big set of questions and answers that are well, not authoritative, but pretty decent. And since they stayed present and when people vote on them, the authors get notified again, people are inherently look at them again later. I mean, frequently I just looked back at a question or answer I wrote five years ago and then are like, I think I can inaudible this a little better now and improve it. So we have this living body of just questions and answers for the ages that probably at this point answer most of your technical questions around Bitcoin and compared to reddit, it’s just Bitcoin talk would be so noisy that you would be on page five and then actual question had been answered three times already on page two, three and four.

Stephan Livera:

And they start over on page five. And on Reddit it’s just there’s a lot of good content on Reddit, but there’s also just a lot of noise and price posts and memes. So right.

Stephan Livera:

It can be the blind leading the blind on Reddit sometimes.

Murch:

Yeah. But although I don’t want to say that, for a very long time, that was a very good place to learn about what was going on in the community. And there’s definitely a bunch of people that really know their stuff. But a lot of that has since moved to Twitter, which just wasn’t the case, I don’t know 5 years ago, 6 years ago. Yeah.

Stephan Livera:

Let’s talk a bit about your work coin selection. And you know, how you got interested in all of this stuff because you’re seen as one of the experts in this area now what was your, why did you get interested in coin selection of all things?

Murch:

I think I read in a, probably in a Bitcoin stock exchange question that somebody was asking why is my input set built like this? And, and why is it spending an input that is actually not paying for itself in this transaction? And then I looked into what exactly Bitcoin what does and found that it was fairly consolidatory, wrote up the coin selection algorithm of Bitcoin well probably then Bitcoin core and just sussed out a little bit what was happening there. And then I thought, well, surely an input set should never include inputs that can’t even pay for themselves. That is just detrimental for the sender. So I created a patch, I think that was 2014 and that would just prune such inputs from the input set when a transaction got built. And so I believe that Wladimir merged it with can make it worse. And about three months later it got rolled back when some other developers pointed out that the UTXO set was growing. So that was my first patch to Bitcoin core and I wanted to do better and that’s how I came up with my master thesis. Okay. This is obviously more complicated and this solution just doesn’t seem satisfying. Let’s see if we can do something better.

Stephan Livera:

That’s awesome. So can we just contrast some of the different potential approaches then? So I’ve heard of let’s say the knapsack approach or the random approach or the branch and bound approach or let’s say Electrum I think in those days had a slightly more private mode. Could you just spell out for us what are some of the different high level approaches that we can take with coin selection?

Murch:

Okay. That’s a really broad question. But generally the problem is that coin selection is a multidimensional issue, right? You when you’re sending a transaction, what you actually want to do is you want to create a transaction output. That’s the payload, right? That’s also the only part of the transaction that you actually want to create. And if I’m sending money to you that is the payload of the transaction, my one output to Stephan to pay him. All the rest is just overhead. Right? So you want to think about, okay, what fees am I paying to pay Stephan? What does that do to the liquidity in my wallet? How does that impact the privacy of my wallet? How does that, yeah, that’s mostly the ones that I would go with at that point. But, so the, you can do something that works fairly simply by just taking the oldest unspents or taking the largest cent spend or just randomly selecting from them. And you will find solution and it’ll work, but it turns out if you think a little more about it, you can do better.

Stephan Livera:

Right. and so could you just outline what was the knapsack Approach?

Murch:

I think so. This is a little funny because a knapsack problem means that you can only approach it from one side, run. How many boxes can I fit into a larger square or something? Right? But in Bitcoin you can overshoot, right? You can just pick an input that is way larger and then just pay with that and create a change output to send the rest back to yourself. Right? So a knapsack has related, but it’s sort of a little bit of a different problem. You really have to find an input set that pays enough so it can pay for the output, can pay for the transaction input and transaction overhead altogether. And then you probably want to minimize either fees or set up, or manage your UTXO or yeah. Or to stay private right?

Stephan Livera:

Yeah. And so I suppose there can be different things that you might be trying to optimize for, right? So one example might be how do I do it to just literally just minimize the fee. I don’t care about anything else. I just want to minimize my fee. And then another one might be what are some of the different conflicting goals that might be there?

Murch:

Right? So there’s this, the funny thing is minimize the global fees over the whole course of your wallet or for this single transaction is even already two different approaches, right? So one method that was really popular back when I wrote my thesis was to do just highest priority first or largest first. And that would always have a very small input set because you would literally take the least number of inputs that you needed to fund the transaction, right? Because you’re stacking the biggest ones, however that ground the funds into dust because you would take the biggest as long as it was the biggest ever and ever again until it was so small that another unspent would be ground down. And then basically you would reduce the size of all your unspents over time until they were all tiny and you had this huge backlog of tiny unspents which you then later had to spend in the future for one input per piece right.

Murch:

So that was actually fairly popular back then. And when fees exploded, people that had been using that suddenly sat on a huge amount of dust and were not well set up or a huge congestion. So a better approach was to spend these tiny pieces over time, right? So maybe you go with oldest first, right? So you pick the oldest unspent and then each next oldest unspent until you have enough money. And that definitely makes sure that you cycle all the funds, but it reveals how all the, all those funds in your wallet are. It’s might not always have the smallest input set. Yeah. So each of these comes like with its own privacy implications and its own long term and short term fee implications. And the thing that I realized at some point actually after the presenting my preliminary results at scaling Bitcoin in Milan was that if you just avoid a change output, that actually helps most of these dimensions.

Murch:

It makes it more private because there’s nothing going back to your own wallet. It makes the transaction smaller because you don’t need to change output. It makes the liquidity in your wallet better because you’re not sending a huge amount of change back to your wallet, which is not available for immediate transactions. And it also reduces the number of future unspents that you have to take care of because an unspent not created is an unspent, you don’t have to spend later. So you save the output now and you save the input later as well. So while the output is only 34 bytes for regular pay to public key hash, you also save the 148 of spending it later.

Stephan Livera:

Right. And so yeah. So I guess backing up, it’s like your wallet has to pick which pieces of Bitcoin it wants to send. Right. And one of the, you know, so each transaction has inputs and outputs. And as you’re saying there, one of the interesting ideas is to avoid the creation of a change output altogether because of the overall saving to both yourself. And potentially you could even argue that’s better for the ecosystem as well. Because it means less space is being used on Bitcoin’s blockchain in each block.

Murch:

Yeah. And the UTXO set doesn’t grow from your transaction, it’s a net minus one on your input to output quota. Right. under the output side. So yeah, I, once I realized that that avoiding a change output all together was beneficial for all fees, liquidity, privacy, and your own, you take some management that sort of became the silver bullet to a degree and branch and bound is essentially just a way to systematically efficiently search the UTXO pools, combination set as in like UTXO pool being the UTXO wallet and now basically it just goes like combined one with two combined, one with three combined, one before. Oh, this is a perfect match. Let’s send a transaction where I don’t need to create a change up.

Stephan Livera:

Gotcha. And so this branch and bound what was something from reading a paper? I think it was initially proposed by Greg Maxwell, like many other ideas in this space.

Murch:

Yeah. Yeah. He described something that I I don’t remember exactly when I found it, but probably around the time of going to Milan or I think I might have described it before even, but I hadn’t really implemented it first time was actually going with other suggestions such as trying to match the output amount to the recipient amount as in create a change output that was the same size as the recipient amount because that’s obviously a sort of amount that I would be sending. So maybe it’ll be useful to have inputs in the future that are the same size as something that I’m often sending. But that turned out to not be very efficient at all. Turns out that the frequent price changes, the fee rate changes and also just the differences in amounts sent didn’t really make that as effective as I thought. So, yeah. I don’t know exactly how that came together anymore. It’s been almost four years at this point.

Stephan Livera:

Yeah, sure. So I think it’s also interesting just to talk about the different dynamic. So there’s a few things here. So you are, we’re considering not just, you know, the here and now, but what will happen when fees rise. And that’s an important thing if you’re managing a large wallet, particularly because, and what means not just large in the sense of, Oh, I’ve got, you know, 2000 Bitcoins in this wallet, but more like lots of pieces of Bitcoin in this wallet. So why is it important to consider the longer term implications when you’ve got lots of little pieces in your wallet?

Murch:

Yeah. Okay. So short history lesson in 2017, we had a huge price run up from I believe, somewhere around $2,000 in January to $20K by December. And the price rise increased the speculation and a lot of people were sending money to exchanges or withdrawing and it just overall increased demand for transactions blockspace. And we in, I think it was around Christmas and new years that the fees spiked and we saw fee rates of over 1,200 Satoshis per vbyte. So if look back into past few weeks, we saw about 200. So it was six fold that even. And for a lot of people that meant that their smallest pieces of Bitcoin were completely unspendable, economically unspendable the input cost was higher than the value of the unspents. In particular, there was one wallet that I was looking into a little bit that had over 500,000 unspent of exactly 10,000 Satoshis and they became unspendable at I think 30 Satoshi per byte if I remember because 2 of 3 multisig with non SegWit there’s 297 bytes.

Murch:

So I think 30 works out about, so from 30 Satoshis per byte provided up to 1,200. They literally just could not access any of those funds and they were operating on a few hundred unspents for almost a month even though they had over half a million unspents in their wallet. And doesn’t an extreme example of course, but a lot of larger enterprises get more deposits than they do withdrawals. And they I’ve seen ratios of like 20 to 1 or so. They really have to consider how they will ever combine all those tiny pieces of Bitcoin into larger chunks. Because when the fees go to 200, you don’t want to send a transaction with over a hundred inputs in order to pay us and go withdraw, right? You’re be paying under hundreds of dollars for a withdrawal. Right? So you need to have enough, UTXOs that you can process a lot of transactions even if there’s maybe not a block for a whole hour, but you don’t want to have so many that you are forced to make huge transactions and to yeah spend a bunch of dust in one go.

Stephan Livera:

Great. And let’s also consider the dynamic as well. So obviously in December, 2017, it was crazy FOMO. It was, you know, and who knows, we may well see that come again in another, in a year or whatever. Right? But it’s also an interesting dynamic right now, and you have been commenting on this right now because we just went through the halving and we haven’t fully, I mean it takes a couple of difficulty adjustments for the block. So the on average yes, it’s every 10 minutes, but in practice it’s been a bit longer because we’re still waiting for the difficulty adjustment now that has caused let me summarize this. So basically that has caused, because we’re seeing slower blocks, we’re trying to see more transactions trying to get stuffed into each one, which is also in turn pushing up the cost right now temporarily. But it’s kind of giving us a glimpse of what’s to come if we’re not efficient in our wallet management in the space. Right,

Murch:

Right, right. Exactly. Yeah. The having was now two weeks ago I think right? 16 days and the, well the reward dropped by almost half and the block subsidy half, but just a inaudible roughly assuming the same throughput. But the hash rate then dropped by somewhere between 20 and 30% or so? And in the first difficulty adjustment, we only saw a reduction of 6%, I think. So we’re still down by about 20% compared to our expected 10 minute block. It means one block every 12 and a half minutes. So even if you consider that the transaction demand was the same and we had about whatever, 90% full blocks for the past few months, which tends to be just fine because it clears every night or if it doesn’t clear over night, it definitely clears on the weekend.

Murch:

But suddenly, if there is a reduction of 20% of the block space, you have 90% of full blocks for 80% of the block space. And now there’s this excess just keeps stacking up. And we saw the mempool rise to a point where the default mine pool size, our nodes would cause the lowest free transactions to get dropped by the nodes. We exceeded the default mempool size. And so yeah, I’ve been looking at this a lot lately. Posting some Twitter updates commenting a little bit on it. It’s just fascinating because every time a block is found, you don’t know how long it’ll take for the next block to come around. It might take an hour, it might take 10 seconds and sure there’s probability. But as long as no block has found the expected time for the next block is always 10 minutes. So there’s a little boggling. But Peter has a great thread on for the explaining. Sorry I’m getting sidetracked here.

Stephan Livera:

No, that’s totally cool. That’s totally cool. So look I think I actually, we’ve got a question here from Vake, so let me just pop that up on screen. So the question from Vake is how do we balance privacy versus reducing transaction fees when choosing whether or not to consolidate UTXsO? Now I guess probably the answer there is more just like, what’s your priority? Are you, are you trying to optimize the privacy or are you trying to optimize for fees? How would you answer that question?

Murch:

It totally depends on your trade offs and that’s also why there’s not one size fits all coin selection for everyone and not one size fits all UTXO management for everyone because unfortunately if we’re honest, a lot of the bigger businesses, their KYC’ed already they talk to governments because when they get funds that are from certain sources they might need to reveal information about them and so forth. So they don’t care that much. If somebody can track whether they have, withdrawal is highly likely to be from exchange A. So for a business that does thousands of payments per day, it just is a little bit of a different question for you. For a retail user that just has a tiny amount of transactions, maybe a few per month or a few per week, they can probably afford to look at their UTXO set and are like, okay, this piece I got from that transaction disputes I got from that transaction, I’ll use exactly these inputs to keep funds separate or something like use coin control or for some, I mean it just totally depends on what’s important to you and whether you’re talking about saving $10,000 per day by doing consolidations or just, yeah,

Stephan Livera:

Yep. Yeah I think that’s a fair way to answer it. And I think if you are an individual, a retail HODLer kind of guy, and you’re more concerned about privacy, you might be using, for example, the Samourai wallet Stonewall. And what that does is it includes additional inputs into the transaction, which as I’m sure you know, Murch but just for listeners, the typical, the size of the transaction is very much based on how many inputs you are including into that transaction. And as you, as you scale that up, that massively increases your cost. But for some people that’s worthwhile because we want the privacy. But for other cases, let’s say you know, your BitGo managing a large wallet then if that’s not really cost effective or may not even be practical, might not even be possible based on the size of those wallets. It might be actually interesting. You know what, we might as well pull it up on screen. Just cause I’ve got it here anyway. So here, so we can see here, Murch, you recently put out this table. Do you want to just tell us a little bit about some of these input and output sizes?

Murch:

Yeah, so I frequently get into discussions about transactions and transaction sizes and, or what people should do and whether they should batch or not. And I kept needing to look up just how big exactly transaction inputs and outputs were. And I finally just made this table to have it handy for myself. So it has been pointed out to me by now that I should have just put the exact values instead of rounding up to make it virtual sizes. So it’s slightly inaccurate overestimating costs. But the main point that you can see here is at BitGo we use two of three multisig, right? The benefits of multisig are clearly a there. And being able to have a second check on whether something should go through or not and putting in other mechanisms to control your funds is just super helpful.

Murch:

When you get attacked or something. And that comes at a cost though, right? Putting a multisig input for a non SegWit is literally twice as big, right? 296 would be exactly the double of 148. And by putting that into a wrapped SegWit input instead people were able to save over 50% of the input cost on every single input, right? So we rolled out wrapped SegWit, I think it was October or November, 2017 just before the biggest congestion. And we urged people to just start giving out these wrapped SegWit addresses because they were perfectly forward compatible and they could, people could just send to them. Anybody that could send to Petro script hash could send to rep SegWit addresses, but the, our user could then spend 140 virtual bytes instead of 297 bytes. Right? And that got even better with native SegWit, but native SegWit is not forward compatible.

Murch:

While it’s neat to support-32 address format in order to be able to send to them. So that has been slowing in the adoption. I like recommending it for change addresses immediately because that’s when users send to themselves. So what you can see in this table anyway is that using a more efficient address format can have very significant cost savings for you. Switching from non SegWit to SegWit either for singlesig or multisig is a reduction of, well in multi-sig, 50% in single state guy. I could guess 40% roughly. And native SegWit is even cheaper. And the thing that people were a little excited to hear about was that taproot is on this table too, which of course has been talked about for, what is it now, two years or so. But it’s still a little undetermined when we will actually be able to use it.

Murch:

But the trade offs get even more exciting for taproot right here, if you think about it the cost of the user is when they create the input, right? So they paid the input costs the 58 vbytes for taproot put here versus 68 for a native segregate singlesig or 105 for two of three multisig. So very clearly lots of savings. But the cost increase is on the side of the sender. So if I’m the recipient and I hand you a taproot address, I’m actually distributing some of the costs that the total transactional flow will have to the sender. And it makes incentives more compatible. What you want is that inputs, Sorry. Creating outputs should be more expensive because that’s something that increases the global cost of nodes to run. Right. And spending inputs should be cheaper because it makes it easier to reduce the UTXO set. This is globally great does this generally the only case here that is cheaper as native SegWit singlesig has 99 bytes versus taproot having 101 vbytes. So very insignificant, total size increase. But in all other cases, taproot will be the cheapest way of sending Bitcoin and even for the single sig case since some of the inaudible to descender and it is very much, great for the recipient to give out taproot addresses.

Stephan Livera:

Awesome. So can you just outline a little bit why it matters the size of it, of the overall UTXO set? Why is that important? Why do we care about that?

Murch:

Oh yeah, good point. So every single full node keeps track of all pieces of Bitcoin that float about these are called the unspent transaction output or UTXO which we’ve mentioned frequently in this podcast so far and this is the only way to know whether you actually got paid. You have to know every single piece of Bitcoin and have to be sure that it has not been spent before and is available for spending and has been signed properly when somebody sends you funds. So if every full node has to keep track of every single piece of Bitcoin, you kinda don’t want this to balloon and it’s been growing pretty rapidly. We are at about 64 million I believe. And that is we had a recent new all time high. The previous all time high was I believe in January 2018, just after the biggest congestion. And now we’ve grown again to the same size. So it’s just a cost of operating a node and if it goes to a very large size, it’ll make it prohibitive for people to run their own nodes at home. Yup.

Stephan Livera:

And so I guess what you are also getting that there is also around what is the incentive for people whether they are sending or receiving Bitcoins. What’s their incentive, whether they will be on net creating new inputs or creating new outputs or will they be destroying those pieces, thus reducing the cost to the overall ecosystem right?

Murch:

I mean, if you think about it, the number of inputs and outputs will eventually match because over the life cycle of Bitcoin, every output will have to be spent as an input eventually. You can argue of course. Well actually no, that’s even true for a coinbase output. So in the end if you want to take your funds out, everybody is a net zero, right? But you might want to have more outputs to increase you privacy because having all of your funds in a single output is just terrible because when you pay somebody, they know exactly how much money you had in total. And you might not want to have too many though because as we discussed earlier already, it’ll increase your cost of operating your transaction creation. So as more users stream into Bitcoin in general, I think it’s natural that the set will grow and our computational resources do too. And certainly there is also some unspent for which the private keys were lost at are unspendable. Now that’ll stick around forever. But we just want to design the incentives in a way that people don’t arbitrarily balloon the set and make it more expensive and prohibitive for the general user.

Stephan Livera:

And in terms of so this one here, we’ve got a question here, I might put that one up. So what is the most compatible address format for the future of BTC?

Murch:

I guess we first have to talk about what compatible means. So the BIP for taproot actually specifies that or I guess I think that must have been in the BIP for bech32, it specified that you should not prevent sending to higher versions of SegWit. You might remember that the SegWit script came out with version zero when SegWit was introduced and taproot now introduced this version one of script. And so hopefully a lot of wallets that can now send to native SegWit addresses will just be able to send to pay to taproot outputs or say create pay to taproot outputs by sending to bech32 addresses there as well. But back when, when it was introduced first but Bitcoin core actually wouldn’t allow transactions to be broadcast if the version of the witness script was unknown.

Murch:

So I think a lot of one of my friends advised me that probably the, a lot of wallets would, would have the version check. So we might be in a similar situation as before native SegWit rolled out where old wallets would just not be able to send to new addresses. So that’s what’s been delaying the rollout of native SegWit addresses, because not every wallet consented. So if you just without context put a native SegWit address in front of your end user, they might be running on an ancient android wallet on their phone and or whatever. And it, it just can’t send to that at all. So you need to have a backup, a fall back where they can get a pay to script hash address or wrapped SegWit address and so forth. And I think we might see something similar with native segments.

Murch:

So while I would love for everybody to start using taproot addresses, the moment that it comes out, it’ll just take a while until people consented. And well, you might be familiar with whensegwit.com or yeah, that site is what, one and a half, two years old now. And we still have a very small number of native SegWit use both. So the most future proof at this point probably is still wrapped SegWit but you should, you should move to showing people native SegWit addresses with a fallback that gives them a wrapped SegWit.

Stephan Livera:

Yeah. So here’s the one SegWit website. But so I think it’s also, so let’s say we get taproot like optimistically speaking maybe early or mid next year in 2021 I guess. It will still take time for wallets to implement it and it will take time for people to, you know, get comfortable with using it as well because it might be a little bit of work for that. Right.

Murch:

I think actually for any wallets that already send to native SegWit will be fairly easy. They just have to allow sending to version one witness scripts. That’s it. Native SegWit addresses are the same. They are also formatted in bech32 just standard covers everything including taproot. So as long as they just want to centered, they literally just have to get rid of the version check for a while. It’s at, can’t send to native SegWit yet. Well maybe it’s time right?

Stephan Livera:

Yep, and so I guess it bringing you back to, what were you talking about that block space market dynamics. Right? So I think in, in, in years gone by, people referred to it as a fee market, but perhaps it’s more precise to call it a block space market, right? Because that’s really what you’re bidding on space within, inside that block. And so maybe it’d be good to just talk about the dynamic there around, we believe eventually as more and more people come into Bitcoin, eventually all the blocks would just fill up and that then people will sort of have this dynamic of they might continually put in low priority transactions, which might be their consolidations. Just put them through at, you know, one Satoshi per bite and then just kind of wait until they eventually clear through. People might be concerned that, Oh, it could it get lost, right? Like, and then they would now need to go and have some kind of rebroadcast mechanism,

Murch:

Right? So transaction cannot really get lost. They can. So maybe one step back. Each full node maintains its own mempool. The mempool being just the current queue for getting included in a block. And the body of unconfirmed transactions, payment payments that have not been executed yet. And while some users or most users probably use the default value of 300 megabyte and Bitcoin core. You can just set it to five gigabytes if you want and keep it, everything that ever floated about the mempool. And once the mempool dips enough, you just resubmit the stuff back to the other network participants. So the other thing is the transaction will never get invalid, right? It’s just literally I spent these pieces of Bitcoin here is a signature. This is my payment instruction to the network and it stays valid indefinitely until one of those inputs gets consumed otherwise.

Murch:

So yes, no, it’s well dropped by default. A transaction that has been in the mempool for 14 days and then probably won’t reaccelerate it for a while. But other than that, the sender himself, they can keep it forever and it’ll stay valid forever, but they might actually want to forget it on purpose in order to send a new version of it. Or my big hope is that in the long run, people actually roll out, replace by fee more broadly because it would just solve a lot of other problems around fee estimation that make it really difficult because it’s a, it’s a one shot, will this be enough and here’s my submission. And then you wait. Whereas with RBF you, can make a decent guess and then just up it a little bit if it sticks around too long without getting confirmed.

Stephan Livera:

Right. And it may also be this dynamic where currently the fee estimation across the different, across the ecosystem, right? Whether you are an exchange or an individual with a wallet or whatever, and depending on your time preference for that transaction, right? So if you’re like, I must get into the next block, well then obviously you can pay a very high fee. If you’re willing to wait, say six hours or one day, then obviously you’ll set a lower fee. And so the point I guess you’re getting out there is that if more people are capable of using RBF replace by fee, they would then start with the sort of lowball, the fee or mid range, the fee, and then if you still don’t get through, then bump the fee higher.

Murch:

Yeah. I think that a lot of people that don’t necessarily, to be honest, I, I think that most people that try to be in the next or segment next block completely overestimate their time preference. But for most people they can probably save 80 to 90% by being a little more patient. For many users, like whatever if I withdraw from an exchange, I want to see that they sent the money to me, but I don’t urgently need it. If I get it sometime this week, I’m fine with that. Right. So I’m happy if they send it at a lower fee rate, but given that they’re probably batching, they’ll all send all of their outputs at a single transaction in a single transaction with the same fee red. So I don’t really have a say in how high the priority is and that’s fine. Batching is as efficient in itself, but for everybody else, yeah, just just pay a 300 block target fee you and then just come back in three days and see if it’s still floating around and then bump it a little bit.

Stephan Livera:

Yeah. I think the other dynamic is also in 2017 towards the end of 2017 there were a lot of newcomers and they weren’t necessarily familiar with this idea of the block space and the dynamic of the fees and so you could argue that the exchanges and some of these service providers know that their users are not comfortable with that and so that’s why they were just trying to pay to get into the next block because I don’t have time to educate my customer, I just want to get into the next block.

Murch:

Sure, definitely. Yeah, and so there will be a multi-tiered market there. There will be the froth on top that needs to be in the next block or next two blocks and they’ll be fine if it takes three to five blocks occasionally if there’s a lot. But they, and then there’ll be other people that might go, I dunno, five Satoshis per byte that just don’t want to get mixed into consolidations.

Murch:

But otherwise they’re happy to wait a bit for the confirmation. And then the min relay transaction fee, you’ll, you’ll get the very low time preference, Hey, just take those 200 inputs and give me a single piece back consolidation transactions that don’t have an external recipient. So it’s just somebody is sending to themselves and it’s just between them and themselves to how long they’re happy to wait. And usually that means more or less indefinitely. But you bringing up a point that I honestly don’t have a good answer for, which has the block space supply is inelastic and when there’s more transactions being created, then I can get confirmed. Eventually it’ll overflow. And sure at first that that’ll drive adoption of more efficient formats and second layer protocols. Maybe, maybe sidechains and things like that. But eventually either those second layer markets and the main chain get into an equilibrium when the main chain costs are too high transaction volume flows off to the second layer or vice versa.

Murch:

If it’s super cheap to transact on the main chain the overhead of creating lightning channels or locking up funds in a side chain or something like that will be enough friction to move stuff back to the main chain, right? So either there’s going to be an equilibrium there or at some point we actually just exceed the capacity of the main chain. And then I think real have to have a better discussion in the network, what exactly we want to achieve. And it’s, it’s difficult to argue about complex systems and all that. But yeah, I mean, I just don’t know how in the long run this whole thing will evolve. And I’d completely blind to, well, the inelastic block supply.

Stephan Livera:

Right. And let me just throw a few points here as well. So for some people, let’s say you are a trader and you’re moving money across exchanges and obviously liquid makes a lot of sense in that scenario, but some of these people justifiably have a high time preference because for them they would otherwise be paying like $70 or $80 for to wire some money around and waiting days of time anyway. And so for them they might well be happy to pay $30, $40 as a Bitcoin transaction fee. And in this case, if they are on an exchange, then the exchange is kind of paying that fee on their behalf because the exchange, wants you know their volume that the exchange makes a lot of money out of. Right. So that’s one point. Another point is also, again, this is kind of zooming out more economic, but if you look at someone like say Nick Szabo, right? So he speaks about this idea of, you know, medium of wealth transfer. And so those people might well be comfortable paying $40 $50 fee because their alternative is to get gold and spend millions of dollars moving gold around the world. And so in that sense, maybe it really does make sense to them to pay that high a fee because it’s still cheaper for them broadly considered to pay that $40 or $50 Bitcoin fee in the, in the extreme example right?

Murch:

Right. I mean there’s, there’s other things to consider there. So for example, for traders that want to make use arbitrage opportunities and make money for them, it really has to be fast. Of course they want it to be in the next block, but for them, liquid and lightning are both much faster as well. Right? So once there is sufficiently large lightning channels and the good infrastructure between enterprises, they should use lightning because then they have the funds instantly on the other exchange. In fact, I think a lot of OTC and large exchanges have agreements with their largest traders to accept their transactions unconfirmed because they’ve had a long relationship and just solve the problem that way. But it is very specific between a service provider and a specific individual that they trust each other to a level or might even have a deposit collateral or something.

Murch:

Right? So even for these people it might make sense to move to a second layer because the trade offs benefit them. But inherently the trade off is different here right? On lightning, you pay for amount sent because you’re using the liquidity of other participants lightning’s letting them channels to forward funds. So you’re paying for the amount transferred. Whereas on chain, inherently a large payment will be capable of paying more because you’re paying per data and not relative to the amount. So if you’re sending a million dollars in a single Bitcoin input, a single input transaction you don’t mind if it’s 40 bucks, but if you’re sending 40 bucks, you do. Yep.

Stephan Livera:

Yeah. And so I think it just comes down to selecting the right tool for the job. Right? So I think that some of the discussions around using lightning for large amounts, it might be difficult because you then, it’s a question of having the liquidity in the right, you know, who’s got the balance on the right side and, and then as soon as you start routing multi hop in that scenario, then maybe liquid just makes a lot more sense. And so I think for these kinds of high value between quasi semi trusted parties, if you’re large exchanges or OTC, I think liquid probably makes the most sense in that scenario and that will kind of take a lot of those transactions off Bitcoin’s blockchain and put them into liquid. Whereas say the small and maybe some medium transfer stuff, maybe that makes sense on lightning. If you’re doing just, you just want to be able to quickly transact.

Murch:

I mean multipath will help a little bit with bigger transfers as well. But to be honest, it’s taking a little longer than I expected. We had our own project on at BitGo to work on lightning and it’s gotten delayed. And I think it is, I loved that it was working out of the box. It’s a simple idea growing to be a more complex ecosystem, which in my opinion is the only way how you can build a complex system is by starting with a kernel that is really simple. And but yeah, lightning, well it will take a little more time and then it might even have a little bit of a chicken-egg problem. You need some big players that provide a lot of liquidity in the network or a sufficient number of participants before it’ll become attractive for payment providers or merchants to implement receiving lightning.

Murch:

And on the other hand, while there is no merchants there, it’s not that attractive for a user to maintain a lightning channel and so forth. So you get a little bit of a catch 22, but I do see it coming eventually. It’ll just take a little longer than I thought. And to be honest, liquid is a little more difficult to not as transparent. So I think you can see how much money in general is in, sorry, how much Bitcoin is in liquid in general because you can, I think they use what, 12 of 15 multisig or something fairly recognizable.

Stephan Livera:

Yes, there is a way to see how many Bitcoins. There are. I think even on Clark Moody’s dashboard, it’s here as well. So you can see here liquid inaudible capacity and in value. You can see that, but yeah, go on.

Murch:

Yeah. So but other than that, once the money, once the Bitcoin isn’t there, it is just a lot more private. And especially for really, really large payments that again, might become more interesting. The anonymity set for midsize payments on chain is fairly decent right now. But for, I mean, just look at that one spend of block 3600 and something, and everybody is talking for two days about it. Right?

Stephan Livera:

Right. So the anonymity costs, if you will. But you know, maybe for those people that don’t care, like it’s not that important for them. Yeah. The other question I think is also really interesting is around the incentive, right? So some, depending on who you are you may not care about, like, I mean, if you’re an exchange, you’re making all this money. Like if you think back to 2017 days BitPay and whoever else, like you might, it might not matter that much to you that you’re not being chain efficient because you’re just, you just want to make money out of your customers so you can just push the cost on to them. And there’s an interesting dynamic there around if you’ve got like a commons right? Is it a tragedy of the commons? Because those people who put in the engineering effort and the time, obviously people like you care about it.

Stephan Livera:

Obviously I’m interested in that because, you know, I’m just interested in it. But there are many people who use Bitcoin who for want of, they just don’t care. Right. It doesn’t matter to them. They just want to use it. So do you think that represents any kind of issue for Bitcoin or is it more just like, look, over time people will just naturally get driven towards using the more efficient ways they will get driven towards using taproot? They’ll get driven towards using liquid and lightning and batching and all these techniques.

Murch:

Yeah, I mean that’s sort of touches an interesting subject. We’re happy because Bitcoin is a censorship resistant money that inherently means that we have no say in the transactions other people create. So for me, it’s good to create a smaller transaction because I saved money for myself, but it also benefits everybody else because it reduces my block space footprint and makes room for other people’s transactions. Right. So in the end, the customers of those services pay for those transactions and when the fees are high enough, the exchange that implements the more efficient transactions will have a lower cost and will be able to offer their service cheaper. So in the end, bad behavior gets driven out. But until then, I’m afraid they can spend as much as they want. And if they still don’t see why they should have SegWit in 2020 then that’s, I mean we were looking at, so the men that stare at the mine pool or people that stare at the have pool.

Murch:

We’re discussing two of these cases in the past weeks. One is the Laurent I think called it crazy one Oh one. I just thought that today actually. So I was looking into whether that was the same entity that I had looked into two weeks ago and that was a wallet that was consolidating inputs at the same cost as they were sending. They had hard-coded a single fee rate at like 72 satoshi’s per byte. A high fee rate and they were consolidating at that same fee rate as well. So it’s just hard to watch. And this crazy 1 o 1, they were consolidating at over a hundred Satoshis per byte. And I think Laurent or so wrote that 720,000 UTXO in this period where we had congestion already. They added another 104 Bitcoin worth of fees.

Murch:

By consolidating at highest fee rates.

Stephan Livera:

I guess the miners are happy,

Murch:

Yes the miners are happy. And to be honest, probably somebody is going to spin a conspiracy theory around that, that somebody just had money to burn in order to make Bitcoin look bad. But in the end, we don’t have a say. Everybody can create their own transactions if they want to pay too much. Well, we as a, as if Hydra can outspend them. Everybody has to spend a little more and they’ll get in and whoever is flooding the network with consolidations at 100 Satoshis per byte while they’re paying a lot because they’re a single entity that is paying for all of these transactions.

Stephan Livera:

Viewed in one way it could be seen like they’re helping pay for the security of the network, right? Because they’re paying the miners basically, and the miners are who secure Bitcoin. So I mean, it’s, you know, I think, I guess the con the converse, right? So let’s imagine they’d just put it all through at one set per by it. Then we would have had this huge now I guess the impact to the users who are transacting, they could have put through at lower fees. Right. So that’s probably one of the impacts there.

Murch:

Just if you’ve been watching the mempoll in the past weeks, you have seen there was a 40, 50 megabyte one to two satoshi band that’s been growing. Somebody is adding like a big, like about a megabyte or so at a certain hour every day you see just a little tick where, where another bunch of transactions get added and that’s just somebody that has a regular consolidation job.I think that is adding to the backlog and they’re just saying, well this will eventually be a single piece of bitcoin and it’ll be great for my wallet, but I don’t need it now. And yeah, so I guess it’s not super efficient for the bandwidth stuff. All the nodes, if you keep adding transactions, that won’t confirm anytime soon. But then on the other hand, it doesn’t matter either. If you don’t need the funds soon, you can add, you might as well add them to the backlog of the network and eventually get them confirmed. I think optimally you have a limit on how much you have in the backlog. And you don’t throw in say more than one megabyte of your own consolidations at one time, but it really doesn’t matter if the mempool overflows for a note. It’ll just kick out the lowest and then eventually they will come back when they’re getting close to getting confirmed. Yup.

Stephan Livera:

So in that case where, let’s say there’s a lot of low fee transactions such that they go above the default Bitcoin full nodes, mempool size of, I think you mentioned it was 300 megabytes. Are those users who their transaction got kicked out into the bottom end of that? Are they now reliant on people who have manually set their node to take more than 300 megabytes? I guess it’s that, or they have to find a way to rebroadcast.

Murch:

I mean, eventually once the mempool drops lower a while it will just rebroadcast its transaction. If the wallet is offline and it doesn’t itself broadcast transaction, again, yes they would be reliant on some other node operator that has the larger mempool set in their node. But at that point when you have over a hundred megabytes worth of transactions ahead of you, you might want to just resend or send later again it actually adds options to you because most nodes still operate on a first seen principle. They will not accept a double spend. So if you have a transaction that’s stuck at 1 Satoshi per byte you might actually be happy if it gets strapped from the network. So you can send a different one. And just why I said a hundred megabyte of transactions ahead of you, the 300 megabyte is actually the memory use of the full node. And that’s platform dependent and it’s for the deserialized transaction. So to unpacked transaction with all the information about the input transactions and so forth. And it’s not the serialized transaction volume. So while we saw about 110 or so mega virtual bytes of transactions waiting, that exceeded the 300 megabyte mempool default limit.

Stephan Livera:

Yup. Also just around RBF and RBF signaling. So that’s one of those things where, it’s probably growing a bit over time. Right. So as I look now on Clark Moody’s dashboard, I think it’s saying about 18% of transactions are signalling RBF. What’s your view? You’re essentially saying you want to see more people signaling that and that would essentially help the ecosystem sort of plan its transactions a little better.

Murch:

So the problem is with currently mostly deployed fee estimation mentioned that you have this single shot and then you don’t know if there’s actually going to be a block in the next 10 minutes or if it’s going to be 30 minutes and there’s going to be 30 minutes worth of transactions added with which you’ll be competing with or, or whatever. Right. So RBF makes this from a single shot to something that you can readjust later. So it’s pointed out of course that that is a bit of a privacy detriment because you reveal that which of those outputs probably was the change output because the recipient outputs you will recreate in another transaction that you replace your original transaction with. But then okay, sure. So people have lots of ways how to tell what the change output is already, if you use inaudible the change I put as the one that you use to bump the transaction unless a recipient bumped it. But most wallets will not spend foreign outputs if they are unconfirmed. So if you’re spending an unconfirmed output, there is a strong indicator that you send it to yourself. She risks sticks are pretty there. There’s a bunch of heuristics that make it fairly obvious what the change output is, like unnecessary input heuristic. If inputs were not needed, if the I think it’s usually the smaller output, then the smaller, output is the change output

Murch:

Okay.If you’re sending to singlesig addresses and there’s a single multisig output, but your, your inputs are multisite. Well, it’s fairly obvious multisig output is the change output so especially for larger services there often already is information on what to change. Output is, so especially for them RBF makes a lot of sense. And RBF has actually has a smaller on chain footprint. With CPFP you have to add a second transaction in order to bump the first. Sure you can add additional recipient outputs in the second transaction, but now you have these new recipients dependent on your earlier transaction and if both these transactions are delayed you’ll start creating a chain and once you get 25 of those or more than 101 kilo virtual byte of transaction data, you’re just not going to be able to submit another transaction and then you’re really stuck. So RBF makes that easier because you’re not chaining stuff together. You’re actually replacing it with a better transaction for roughly the same block space. The big advantage of CPFP of course, is that the recipient can also use it.

Stephan Livera:

YeahtThat’s really fascinating stuff. And I think the other part to that is just around the heuristics and so on that people apply to try and understand who’s doing what on the chain. And so on. Using multi sig is quite distinguishable and you can sort of say, Oh, this is, this is a spend of a two of three. Or you can, I guess you can infer based on the transaction what kind of spend it was. And if there’s, you know, two keys signatures, then that just is another heuristic. And so depending on who you are and what your use case is, that will change how you’re thinking about, okay, well if I want it to be private, then I would have to not use multisig and just do everything on single sig to not give off that fingerprint. Right?

Murch:

Yeah. Or, well, once we get taproot the big hope for taproot is that a lot of people will be making use of the default spending path right the okay. So taproot has two ways of spending. One is by revealing the tree and paying the script or satisfying the script in one of the leaves. That’s the script path. And the keypath is just having all of the participants in some way create a single public key and spend it just like that as a pay to pub key with Schnorr and pay to pub key. Sorry. Yeah. Pay to pub key is done the same for everyone. Whether it’s multisig, whether it’s a lightning channel, it all looks like a single sig pay to taproot input and it’ll actually make the anonymity set a lot bigger. It’ll make the block space a lot smaller. So at that point I think some of those dynamics might change a little bit, but first we have to get it right.

Stephan Livera:

Yeah. Right. Yeah. And I think that’s really interesting stuff. And listeners so if you’re unfamiliar with that, go and check out my earlier episode with AJ Towns, we spoke about that. And we talk a little bit about the key base key based the key pathway and then the script pathway. And so as you’re saying, the key pathway there is the one that would be more indistinguishable. And that’s what I think Pieter Wuille terms that as a policy privacy. So it’s that idea that you don’t necessarily know

Stephan Livera:

What was the underlying policy or kind of restriction or encumbrance that was kind of placed on that UTXO that piece of Bitcoin. Right?

Stephan Livera:

It’s basically a similar to the idea behind lightning. As long as we all agree, we continue to use the most efficient medium, which in lightning’s case is on channel a payment channel. And in pay to taproot is the key path. So we craft a single signature that spends the funds as one of the people could have enforced in the first place.

Murch:

Yeah. But if it falls apart or people disagree or don’t want to help out each other or are offline, they can fall back. And force what they are allowed to do by revealing all the options they have in the script, in the script path in the tree and revealing that, spending more input size but enforcing inaudible and in lightning the equivalent would be to take the HTLC to the blockchain to enforce the channel contract.

Stephan Livera:

Fantastic. so look, let’s just see if there are any other questions from the chat. So guys in the chat, just put your questions if you’ve got any for Murch. And just while we’re waiting, do you have any thoughts around the people are getting onto Liquid, let’s say do you see that happening over the next year or two and potentially that helps alleviate some of the pressure in terms of this? Well, if we’re speculating that there’s a coming bull run and there’ll be a lot of people do you see that dynamic happening?

Murch:

I dunno. I think I don’t have a very well informed opinion on Liquid. I roughly know how it works, but I’ve not been keeping track of it too much. So I don’t think I can comment on that. But yeah, what I think definitely will happen is if fees generally go up and it just incentivizes people to be more cost efficient and that’ll drive adoption of native SegWit, perhaps taproot when it’s there it’ll make lightning network more attractive. It’ll also make liquid more attractive. And I think as we already have discussed, liquid and lightning and main chain they all have different trade offs cost-wise, privacy wise, functionality wise, and people will use whatever works for them and has the right trade offs for their use case. So if costs on chain go up, that’ll drive use. Yeah.

Stephan Livera:

Yeah. I think that’s a great way to summarize it. So a merge. Have you got any closing thoughts for us? Otherwise, make sure you let the listeners know where they can find you online.

Murch:

Oh well be sure that you consolidate your stuff before the next bull run because especially if you’re running an enterprise wallet, you’ll save a lot of money if you do. And a lot of heartache, use batching. Batching will save you a lot of money. And you can find me on Twitter @murchandamus and yeah, if you ask us a question on stack exchange, I’ll probably edit or answer it.

Stephan Livera:

Awesome, man. Well, thank you very much for joining. I found it very educational and I’m sure my listeners found it very educational also. So thank you for joining me.

Murch:

Thanks for the opportunity.

Stephan Livera:

Awesome. All right, listeners, so make sure you find my show at stephanlivera.com and press like and subscribe if you enjoyed it. That’s it from us. See you guys in the citadels.

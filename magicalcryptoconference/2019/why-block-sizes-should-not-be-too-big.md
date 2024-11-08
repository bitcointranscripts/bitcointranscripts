---
title: Briefly, Why Blocksizes Shouldn't Be Too Big
transcript_by: Bryan Bishop
speakers:
  - Luke Dashjr
media: https://youtu.be/JJF5Gnro1GU
---
slides: <https://luke.dashjr.org/tmp/code/block-sizes-mcc.pdf>

I am luke-jr. I am going to go over why block size shouldn't be too big.

## How does bitcoin work?

Miners put transactrions into blocks. Users verify that the blocks are valid. If the users don't verify this, then miners can do basically anything. Because the users do this, 51% attacks are limited to reorgs which is undoing transactions. If there's no users verifying this, then miners have no incentive to do this. If we wanted to trust someone with a centralized issuer, we could just use that, and we wouldn't need proof-of-work or any of this.

## How many full nodes are needed?

How many full nodes are actually needed? Obviously, miners could run full nodes but that doesn't protect you because the miner could modify the source code. If you alone don't run a full node, that puts you at risk because the miners could do something and you might receive an invalid block and accept it even if it includes inflation and it wouldn't really hurt anyone but yourself. Suddenly you would see currency that only you would accept and not everyone else would accept.

What if most people don't run a full node? Then there's economic pressure. Everyone is buying and selling in the miner-issued currency? Then miners don't necessarily care about the minority, they are essentially replacing bitcoin.

We need at least a majority that are using a full node to ensure that miners cannot create inflation or break any of the rules that we assume are bitcoin rules.

What happens if the majority of the full nodes are all in the US, and they go to sleep during the night? This gives time for miners to potentially cause inflation over night. So you need not just a majority, and not a simple supermajority, you need to have a sufficient majority such that the whole world is covered and there's a majority running full nodes all the time, not just running at one part of the day. I usually estimate this as 85% of the people using bitcoin- not necessarily people but the economic activity.

## How difficult is it to run a full node?

Another question is how difficult is it to run a full node? A strawmen argument is "everyone can download 2 megabytes in 10 minutes". Sure, but that's not an issue. Another argument is that "we have multi-terabyte sd cards now!" and these aren't a problem either. The problem is bandwidth.

The real problem is initial block download. When you first install a new node, it takes time to catch up from the past to the present. The block size is the rate of change of all that data that needs to be processed initially. Right now it's manageable, and most people can handle it. It takes a few weeks. The question is, can people do this? But how long does it take? Some people might give up because it takes too long. Just being able to do it isn't really enough, people need to actually be able to run the full node, and if it's too hard, then people will just choose not to do it.

For the last decade or two, technology has improved about 18% per year. The current 2 megabyte blocks are about 52 gigabytes/year, I think that might actually be 1 MB blocks. It's much higher than 18%/year. The rate that technology is improving is slower than the rate the blockchain is growing because of the block size. Even though technology continues to improve, and hardware gets faster and software gets faster, it's still growing slower than the blockchain is growing, and syncing is going to get harder and harder.

A few years ago I was able to run a full node at home. It didn't use too much data. But now it's borderline. People are still doing it, but not many people. It's getting harder. At the same time, society is moving such that people don't buy computers any more, they just have phones. That's something that bitcoin may have to adapt to if we want people to adopt bitcoin.

On top of all of this, that 18% per year is the last few decades of improvements. It's possible that in the future we might not be able to continue that 18%/year. If it gets harder, then it gets a lot worse at that point.

Running simulations over block size possibilities, we see that technology eventually catches up. I ran a simulation for block size at 300 kilobytes, 1 MB, 2 MB and 8 MB. For the current 2 MB blocks, the worst case scenario if things continue to improve, it's about 1.65x the peak sync time. That's a little scary. It's 9x over the sync time from 2013. The peak will probably be in 2024 for sync time. Returning to the 2019 sync time won't occur until 2033. And returning to 2013 sync time with new technology will take until 2048. If we had kept the 1 MB block size, then the peak would be about 11% higher than we are now, and technology would catch up faster. It's a little better, but not great still. If we had 300 kilobyte blocks starting today, it's 1x the peak sync time in 2019, and we get back to the 2013 sync time in 2035. It's a long time, but it's a lot more manageable than what we have today.

## Other problems with large blocks

There are other issues with block size and large blocks. One issue is that some people want to run the blockchain over the satellite networks, which is possible today but it would be impossible as data size increases. Right now miners would need centralized peering, and some people want to shutdown bitcoin by confiscating miners and that's hard. In theory, anyone can mine and nobody can stop bitcoin mining around the world, but that's no longer the case because if someone knows who the miners are then they can be shutdown. Another problem is that many people have bandwidth quotas. Right now in the US the highest level is 50 GB/month and many people are limited to 5 GB/month. If people are sharing traffic, it's not the same thing as people constantly maxxing out all the time. A lot of people want to watch movies in real-time. If bitcoin is taking all the bandwidth, then they won't want to do that. This is another case where they could run a full node, but they probably won't.

There are other issues but I'm going to skip them. The main issue is the initial sync time.

## Answering objections

Some people are concerned that smaller blocks will cause higher fees than bigger blocks. So a lot of people say increase the block size to reduce the fees. It's not necessarily true that the fees will be higher for small blocks, no matter what the block size is, people are going to want to store random garbage on the blockchain just because they can no matter the block size.

Another objection is that if the fees rise, then "unimportant" transactions will stop rather than bid up fees higher. But important transactions will just optimize, or use layer 2 or something. Not all transactions need on-chain security.

We don't really know what the actual cost of bitcoin really is. Maybe the cost of securing the network is $50/transaction then that's the number.

Another concern is that the fees should probably be higher than node costs anymore, because they will be creating transactions without running a full node-- but when the node is cheaper to run the transaction fee, then it should be less likely that.....

Another objection is that eventually we will need a block size increase. It's not necessarily true. We don't know what will happen in the future and what sort of proposals we will see. It's more important that the network remains secure and decentralized and that we have the features where we get to the point where people actually want to use it. Otherwise we're just another paypal or something. We should focus on the promises of today rather than promising future problems down the road.

Eventually the technology will catch up, if we can delay larger block sizes until that point, then we can be in a better place for an increase than otherwise. We'll be in a better place sooner, if we keep the block size smaller for a longer period.

Sometimes people will suggest that pre-synced nodes or sync snapshots should make the initial block download problem go away. But this changes the security model of bitcoin because now you end up trusting the snapshot-issuer. Verification of snapshots can be done only with initial block download anyway.


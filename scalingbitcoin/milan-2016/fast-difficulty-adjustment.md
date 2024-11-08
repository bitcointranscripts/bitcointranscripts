---
title: Fast Difficulty Adjustment
transcript_by: Bryan Bishop
speakers:
  - Mark Friedenbach
---
Fast difficulty adjustment using a low-pass finite impulse response filter

<https://twitter.com/kanzure/status/785107422323085312>

slides <https://scalingbitcoin.org/milan2016/presentations/Scaling%20Bitcoin%203%20-%20Mark%20Friedenbach.pdf>

# Introductions

I work at Blockstream Labs. This work is based on work I did in 2013 which is now only being presented. If there are any control engineers, I would encourage you. I am going to cover some mistakes that have been covered in the industry on alternative networks and proposals.

# Difficulty adjustment

Difficulty adjustment happens every 2016 blocks in bitcoin. It takes the average of block time and adjusts to the same observed hashrate in the future. On average it's aiming for 10 minute block time. It's not responsive to sudden differences in hashrate or any catastrophic event that might happen in bitcoin. Historically it has worked very well, because we can limit it to historic cases that we have already seen. However we should be thinking about low-probability high-damage events and what we can do to prevent those problems.

# Problems

Looking at where there has been some more experimentation in altcoins, we see very fast hashrate fluctations sometimes decreasing or increasing by 10x, even within minutes or typically in a day. These are because there are multi-chain pools that will retarget based on profitability to whatever coin will give them the most money for mining. So these chains see that they end up in vicious cycles where the hashrate is reduced and not only does the opportunistic miners who disappear go away, but also the people who are mining and go away and their confidence is lost and so on and so forth. Merge-mined sidechains are still hypothecated but there aren't any exmaples yet; still one of the expectations is that with the current mining ecosystem  there might be some difficulty in getting htem secure and defended against these attacks. If merge-mining is being done at the pool level with 25% of the hashrate, that might turn into more merge mining hashrate. Dropping that pool could drop by half the hashrate of the merge-mined sidechain, and this could happen because of technical issues or it could happen because of for example an attack or something, or the attacker has to stop mining the valid chain and start mining an invalid chain. This would be observed by the sidechain hashrate suddenly dropping. We also worry about the success of that sort of attack. If that attack happened, the throughput of the sidechain seems to be effected. And finally, a low probability event as a low point-- if we have mining centralization but let's say 60-80% in China what happens if there was major civil unrest and the country shuts down access to the internet such as in the Arab spring incident. We could adopt an adjustment algorithm that is more responsive to these sorts of changes.

The problem is that we would have 1/10th the transaction throughput if we had that sort of adjustment. If this happened just after a difficulty adjustment in the worse case, we would have 4 months before difficulty adjustment. This has happened in altcoins as a result of a "hash crash". So these coins often end up hard-forking to another difficulty adjustment algorithm but often these have problems. The solutions available is to adjust more frequently. The reason for 2016 blocks in bitcoin is extremely conservative choice in fact it might be suboptimal choice. There's no reason why the blocks have to be associated with the adjustment window; they are almost the same in bitcoin, there's a bug because of this. But there's no reason for this to be exactly. Finally there are some altcoins that change the control algorithm.

# Simulation

I'll spend some time talking about this slide. Unfortunately none of you will be able to read the axis. What you're looking at is the effectiveness of a difficulty adjustment algorithm run in simulation for various sizes of adjustment for both the sliding window and interval of adjustment using the standard bitcoin adjustment algorithm. When you're adjusting every 2016 blocks with 2016 blocks of data--- and then the y-axis is an error metric. So we run the simulation for 20 simulated years and then we build a histogram for the actual observed interblock times and compare to the expected histogram given by the problem. The first thing we will draw attention to is the sawtooth pattern. What's simulated here is a square wave moving from 10x back up to 10x, the sawtooth pattern is lining up with that with the difficulty adjutsment algoirthm. So I ignored that-- what about the area without that sawtooth part? You see here on the right-hand side first, you have the linear relationship where as you increase the difficulty adjutsment interval you get more error because you're not reacting to sudden shifts in hashrate. On the left-hand side oyu see confounding from two separate sources of error. The sliding window size in this simulation was linked to adjustment interval; so as you go shorter and shorter you are reacting to sample sizes that are not statistically significant, but even if you subtract that out there's still underlying error. You're responding quickly and you overshoot or undershooting by quite a bit if you happen to have a couple of lucky blocks in a row. The number of coins that are considered to have "better" difficulty adjustment algorithms are adjusting per block... it would be something through the ceiling on the left-hand side of this graph; it has a tremendous amount of error just from that variance. If you are using the bitcoin adjustment algorithm, you get minimal error, if you're measuring somewhere in the range of 30 to 50 blocks.

# Adversarial side

Perhaps bitcoin difficulty should be adjusted more quickly. The time traveler attack and others become more easy with a smaller window, because effectiveness is larger, because timestamps are very loosely constrained to be related to the actual wall clock time. Miners are allowed to move by 2 hours on block time. So if you had to give a function for calculating a hashrate, miners would be able to choose blocks that create lower difficulty periods. As long as the window you look at is at least as big as the adjustment interval, then they are unable to lower the difficulty on average. You can lie and lower it for one period, but you have raised the period after that same amount anyway after that. If you consider systems quite different from bitcoin, you could run into this problem so you have to keep it in mind. If we were to choose in this example a window size of 36 blocks, so about 6 hours, if we're looking back 36 blocks then how frequently do we want to adjust? We could still adjust every block, but looking back 36 at a time. The right side is 36 because any larger we have the time traveler attack again. It turns out that you get a rapid exponential increase if you adjust every block. With a bitcoin-like adjustment algorithm, if you're adjusting anywhere less frequently than half the size of the window then you're okay. So if you are looking at a 36 sliding window then you can adjust every 18 blocks for example. If you choose a longer adjustment window like 100 or 1000 blocks, you can get a lot closer. So this rule of thumb I just gave you is trying to minimize the sliding window and having the fastest reaction time.

# The problem revisited

It turns out that the bitcoin adjustment algorithm is sub-optimal. You can look into the literature for control theory where you have some variable, in this case hashrate which we're sampling; but we have lots of random noise added to our samples. So we want to figure out the general trend and respond to the larger trend ignoring the noise. Well, this is called a low-pass filter. You can find the optimal filter. You can generate an optimal first-order filter using the following filter design argument.

# Low pass filter design

It's a linear weight that you apply to interblock time that results in the average which you can then use that as more likely to be more accurate of the interblock time than the straightforward naieve average as used by bitcoin. At the top here, it's plotting the ... themselves. There are periods on the side that are having negative weight which means longer block time would be adjusting in the opposite direction. This is an interesting characteristic of how these filters work. The bottom graph is a log-log graph showing the frequency response for that filter. The low frequencies representing long-term averages are passed through unchanged, and high-frequency where that rippling are changing, remember this is a log-log plot, so that variation is just canceled out by this filter and you can see the long-term average as a result.

This adds in two more parameters which are tweakable. There's a gain and limiter. If anyone is doing this kind of analysis for your own network, this adds so that you have a total of 4 to 6 variables to minimize.

# Applications

As I said at the beginning, it would be very interesting to apply this technology to a sidechain in the merge-mined case or alternative networks that are doing mined currency schemes. In these cases you have to be very sensitive to-- there's not really a one-size fits all solution. You have to be sensitive to the goals of the system. A shorter block window might have more variance. Sometimes you might overshoot and undershoot. You are responding to large hashrate changes, if that's in your threat model, and you need to respond quickly, then you'll want that-- versus a longer window that will allow more oscillation but be more accurate as well.

# Q&A

Q: Where is this used?

A: Freicoin. Other systems like zcash and ethereum both do immediate response to last block, so based on time between the last block and next block, they do a non-linear adjustment which is a weak approximation of this, it's a bit more noisy. They fall in the left hand side of the curve from my slides.

Q: ... selfish mining ...

A: Because you are capturing more subsidy in that case?

Q: You increase your relative hashrate relative oto ther miners, if the difficulty was constant then relative hashrate doesn't matter... if you adjust it immediately, then this is all you care about. You probably care about something in between.

A: That's partially true. The largest aspect of that is simply the, it's not the time traveler attack, the fact that the bitcoin adjustment is longer, considering you're shorter than the length of the adjustment cycle.

Q: You have to think about the ...

A: One of the issues is that if you allow large variation in your difficulty then you can temporarily allow a much shorter interblock time by unfairly adjusting downward. This will be compensated for later with another adjustment. During that time period you can use selfish mining properties and use that advantage at the time. I believe the effect is quite small though.

Q: In your plots you have a minimum of around 30 or 50. What is that parameter causing that?

A: Not sure. This is an experimental design. I could explain why you have noise to the left and noise to the right. I think this is just when two noises are a minimum. On the right-hand side is when you're adjusting too infrequently. So therefore you have a large error rate because of a long period of time before your adjustment. On the left hand side you have a lot of variance due to high frequency adjustments. So your expectation is that you settle around the right hashrate, but you oscillate so much that you don't have consistent difficulty.

Q: Critical oscillators... shock absorbers... if you know the oscillation or in this case if you have the sliding window or block time, you could set the maximum rate that someone can adjust the hashrate. So this could be a critically dampened oscillate. A low-pass filter has an additional parameter.

A: Yes, thank you. I skipped over that. The linear filter is a first-order correction. In the literature, the optimal one is a second-order critically dampened oscillator.

Q: If some of the miners go down, then the other miners can adjust the frequency to generate more highpower and provide a lot of compensation. For some miners they can double or triple the hashrate so it will be bigger power consumption but just believe us. If one part or fifty percent of miners go down, the others can economically push up to generate more profit, it's in their interest. There's a lot of hashrate located in China. So, no, this is not for sure. There are a lot of pools but there are a lot of customers overseas. Jihan from Bitmain can confirm they have a center in US and they can adjust location. If something happens, users can switch hashrate for another pool. So it's more flexible. But still this is great adjustments so any improvements can be great, but no promise.

A: Thank you for the corrections.

Q: One of the other oscillations is halvenings and different altcoins have approaches to that as well. What about the intersection of this oscillation and block rewards changing as well?

A: Unfortunately in both halvenings, they have been preceded in a ramp up in price. Some people think it's casually related, but I think it's coincidence. We don't have good historical data because the market price went up and hashrate then increased as well. If it halved and it became unprofitable, the others would be able to make up the difference, and it would only go on for a bit. It's only the catastrophic scenarios that I am concerned about, like on the range of 5x to 10x or more.

Q: What about sidechains?

A: Similar story but more exaggerated. Bitcoin is the gold standard in terms of decentralization-- with a merge-mined sidechain, it is likely to be less decentralized than bitcoin itself.

Q: Correction from Jihan... they have 42% from onsight in China.

A: This is Bitmain specifically?

Q: Yeah.

A: I did not mean anyone in particular, by the way. Substitute any other country. There's a possibility that if the electricity prices in the Pacific Northwest... in which case we would have the same problem in the US if the US had internet connection issues.

Thank you very much.



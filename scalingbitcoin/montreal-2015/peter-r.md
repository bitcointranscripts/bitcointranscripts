---
title: Fee markets
transcript_by: Bryan Bishop
tags:
  - fee-management
speakers:
  - Peter Rizun
---
((Note that there is a more accurate transcript from Peter-R himself below.))

Miners have another job as well. Miners are commodity producers, they produce something that the world has never seen. They produce block space, which is room for transactional debt. Let's explore what the field of economics tells us. We'll plot the total number of bytes per block. On the vertical we will plot the unit cost of the commodity, or the price of 1 transaction worth of blockspace. The coordinates of the point represents the price and quantity of that commodity. The law of demand states that as the unit price increases, the total quantity demanded by the market tends to decrease. As the price falls, the total commodity decreases. These points form a demand curve. If the price per unit is low enough, the quantity demanded can be arbitrarily high. Demand can be considered infinite. This is something that I hear regarding the block size debate, and people say we need a limit because the demand for block inclusion is infinite. Economists have been thinking about this for 100s of years; they have the law of supply. The law of supply is the opposite to the law of demand. It says that producers will only produce more if they are paid more to do so. Apple farmers will only plant more trees if they get more money by doing so. The law of supply has a positive slope. The demand curve has a negative slope. The intersection of these two curves is the free-market equilibrium. Even if the demand is considered infinite, we still get a finite quantity produced.

Is blockspace a normal economic commodity? Does it satisfy the laws of demand? It makes sense that as the unit price for block space decreases, more data will be written to the blocks. But does it also satisfy the law of supply? It might seem that if miners can add as many transactions as they want for free to a block, then the supply period would flatline like this, and supply-andd-emand would never meet, and we would have a tregedy of the commons. It's not really a problem as you will see later. There's a flexcap proposal. It's artifically simulated the supply curve of a normal commodity. There would be a forced equilibrium instead of a free market equilibrium. With a finite quantity of block space.

flexcap requires a centralized group of people to decide what the right price is for block space. That group would be able to decide winners and losers by deciding that price.

What is orphaning? Normally when a miner finds a block, he broadcasts it to the other miners, they all start running away, and if that guy finds a block later, everyone is happy. Let's imagine that this time that miner mines a really big block. It propagates more slowly. Now when our miner mines a small block, his spreads much faster. Everyone think the small block came first even though it didn't. The miner at the top.. the miner at the bottom is happy. Orphaning is not a hypothetical theoretical construct. There were 155 orphans in the first quarter, and 97 in the second quarter, about a 1% orphan rate.

How does orphaning effect the miner's cost for the production of block space? If the miner finds a block, he gets the fees from any transaction plus the reward. Reward + fees times the ratio of miner's hashrate to network hashrate. We need one more term to account for the bigger the block the more likely it is to be orphaned; it is a decaying exponential in propagation time according to my paper. The miner can control the fees and can control the propagation time. He can get more fees by making his block bigger, he can get lower orphan rate by making his block smaller. He must choose between fees and size to maximize profit.

The cost per byte is proportional to bitcoin inflate times a term that grows exponentially with propagation time. There's a real cost for block space. If the inflation rate is zero when the block reward runs out, it's not clear what happens to the production cost, we want to find the total quantity of the commodity produced. There's a Shannon-Hartley theorem that says that the amount of time to communicate information is proportional to the amount of information to communicate.

Propagation impedance (how long it takes to propagate a megabyte of block information) times the block size... The cost grows exponentially with the size of the block. flexcap wanted to make the block size increases; bitcoin already has that property, but instead of a forced market equilibrium, we would have a free market equilibrium.

In other words, a free market exists without a block size limit.

What happens if a mining cartel decides the block content beforehand? They all decide what they are working on. They never orphan each other's blocks. Sure, that's called a mining pool. But tha tdoesn't effect the fee market because the miners still need to transmit the block solutions to each other.

For the inflation to be non-zero, we need more than one miner per pool. If everyone joins the same pool, then the market no longer holds. There's nobody to lose orphan races to.

We don't need a block size limit. Do we want one? Economics helps us answer that question too. When Satoshi Nakamoto put the block size limit in place, it served as an anti-spam measure, it was above the free market equilibrium point, it was 800x greater than queued star.

Bitcoin has been growing over the years. The block size limit is on this side of Q starred. This is causing "deadwight loss", the loss of economic activity as a result of this production quota. Some people think that production quotas can be positive if they serve to eliminate some negative externality. I am not going to weigh in on whether I think a negative externality exists. How can a group force a production quota against a market? How will a group fight this invisible hand of the market?

I think they would follow the playbook of command and control. They would probably censor people who speak out against the quota. This is not a hypothetical example, theymos already censored everything about BitcoinXT.

The production quota will fail because you can only enforce rules that people agree with. Bitcoin wil break down dams erected by special interest groups attempting to implement quotas. various conspiracy theories here.

* Sirini Devadas
* Campbell Harvey
* Christopher Douglas
* Elaine Shi
* Vijay Pande
* Jerry Brito
* gmaxwell
* Houman B. Shadab
* vitalik buterin

Good afternoon.  Today I’m going to speak to you about my recent paper that shows how “a transaction fee market exists without a block size limit.”

There are a few provisos to this claim:

(1) Firstly, we need for Bitcoin’s inflation rate to be nonzero

(2) Secondly, we need for more than one miner or mining pool to exist

Under my sports jacket, I’m wearing my Bitcoin miner’s T-shirt.  This helps me to think like a miner.  Now, many people think that the job of a miner is to find the magic nonce value that allows a new block to be appended to the Blockchain.  While this is true, miners have another job too.

Miners are also commodity producers.  What they produce is a brand new digital commodity unlike anything the world has ever seen before.  This new commodity is block space or room in a block for transactional data.  Before I explain why block space is a normal economic commodity, let’s first review what the field of Economics tells us about the production of such commodities.

We are going to be looking at several charts in this talk, and most will have the same set of axes.

We will plot the quantity of the commodity produced on the horizontal axis.  For example, the total amount of apples per year or the total amount of kilobytes per block.

We will plot the unit price of the commodity on the vertical axis.  For example, the price of one apple or the price of one transaction’s worth of block space.

The Law of Demand states that, all else being equal, as the price of the commodity increases (↑), the quantity demanded falls (↓); likewise, as the price of the commodity decreases (↓), the total quantity demanded increases. The resulting curve is known as the “demand curve.”

An interesting thing about the demand curve is that if the price gets low enough, the total quantity demanded can become arbitrarily high.  In other words, we can consider the demand for a commodity to be infinite.

Now this is something I hear thrown around regarding the block size limit debate: people say that we need a hard limit because we can consider the demand for block space to be infinite.

Well the economists struggled with this conundrum too: but they solved it over one hundred years ago now.  The way they wrapped their head around it was to work out another law.  As you may have guessed, it’s called the Law of Supply.

The Law of Supply is sort of the opposite of the Law of Demand.  It says that producers will only produce more if they get paid more per unit!  Apple farmers will only plant new trees if they can earn even more profit, miners will only include more transactions in a block if they can earn more by doing so.

The supply curve has a positive slope and the demand curve has a negative slope; when we put the two curves together, they meet at the free market equilibrium point.  P* is the equilibrium price and Q* is the equilibrium quantity.  In other words, even if demand can be considered infinite, the amount produced will actually be finite.

So, is block space really a normal economic commodity?  Well, does it satisfy the Laws of Supply and Demand?  I think everyone agrees that it satisfies the Law of Demand.  It just makes sense that if it becomes cheaper to write data to the Blockchain that more data will get written.

What isn’t obvious is that block space also satisfies the Law of Supply. At first glance, one might imagine instead that transactions could be added to a block for zero cost by a miner.  The supply curve would flat line at zero like this.  Supply and demand would never intersect and we would have a “tragedy of the commons” where the Blockchain fills with spam.

There was a recent proposal called Flexcap to "fix" this problem.  I use the scare quotes because it's not actually a real problem as we'll soon see.  Anyways, the idea was that Flexcap would charge miners more and more per kilobyte the bigger the block became.  It would artificially makes block space behave like a normal economic commodity.  It results in a *forced* equilibrium rather than a free-market equilibrium.

There is a problem with Flexcap. It requires a centralized group of people, rather than the free market, to decide what the right price for block space is.  And if a group or people get to decide, then those same people will also be able to decide winners and losers by adjusting that price.

Fortunately, we don’t need Flexcap. The supply curve for block space already looks exactly like this do to a phenomenon called orphaning that I'll explain next...

So what exactly is orphaning?  Well normally, when a miner finds a block solution, he just broadcasts it to the network and most the other miners accept it and start mining on top of it.  If another miner finds a block solution a bit later, the other miners ignore it.

However, let’s imagine our miner mines a really **BIG** block.  Big blocks propagate more slowly than small blocks because they contain more bits of information.  Let’s imagine our miner again finds his block solution first, but this time it’s so big that it propagates very slowly.  Now, when the other miner publishes his small block, it spreads through the network much quicker. Most the network thinks that the small block was first and so they ignore the BIG block that lost the race.  As a result, our miner loses his 25-bitcoin reward!

Orphaning isn’t some theoretical idea.  We can actually measure it happening.  In the first quarter of this year, there were 155 blocks orphaned, in the second quarter, there were 97.  Typically, about 1% of blocks gets orphaned.

OK, now let’s try to model how orphaning affects the miner’s cost of production.  If a miner solves a block, he earns revenue equal to the block reward plus any fees from transactions he includes.

      (Reward + Fees)

The miner's expected revenue per block attempted is equal to this multiplied by his chance of winning (the ratio of his hash power to the total network hash power).  So the miner’s “expected” revenue per block is:

      Revenue = (Reward + Fees) (hash rate) / (Network hash rate)

But, remember, if the miner’s block takes a long time to propagate, then it’s more likely to be orphaned.  My paper explains that we can model this as a decaying exponential:

      Revenue = (Reward + Fees) (hash rate) / (Network hash rate) exp(-propagation time)

The miner can control two variables in this equation: fees and propagation time.  He can collect more fees by making his block BIG but he can minimize his block's propagation time by making his block small.  A miner thus must choose a balance between lots of fees and fast propagation to maximize his profit.

With a bit of algebra and a bit of calculus, it follows from this equation that the cost for a miner to produce block space is proportional to Bitcoin's inflation rate and a term that grows exponentially in block propagation time.

This is cool because we've shown that there's a *real* cost for a miner to produce block space.  But this also brings up proviso #1: it's not clear what happens to the miner's cost of production when the block reward goes away.

      (price per byte) = (inflation rate) x exp(propagation time)

It gets a bit complicated now—and you’ll need to refer to my paper for the details—but with a bit of algebra and a bit of calculus, it logically follows from this equation that the price to produce a kilobyte of block space is proportional to bitcoin’s inflation rate and to a factor that grows EXPONENTIALLY with how long it takes to propagate a block.

OK we want to get an equation for the unit cost in terms of the total quantity of the commodity (the block size).  There's a theorem from physics called the Shannon-Hartley theorem that basically says that the amount of time it take to communicate some block of information is proportional to the amount of information contained within that block.  This let's us re-write this equation as

 (price per byte)   =   (inflation rate) x exp[propagation impedance x size of block]

The really cool thing is that the production cost to produce block space is exponential in the size of the block!

So what does this mean?  Let’s go back to our supply and demand curves.  Remember, the idea of the flex cap…to make the price per byte increase with block size?  Well, we just showed that this is exactly what happens with no cap at all!  In other words, block space already obeys the law of supply.  We already get an efficient block size without intervention.  If we experience another growth spurt, then the demand curve will shift up like this and the price per byte will rise.  If miners get better at propagating blocks, then the price will fall.  The point is that a balance will always be achieved.  In other words, a transaction fee market exists without a block size limit.

Objections.  What is a group of miners decide everyone's block contents beforehand?  Then group members are at no risk of orphaning blocks of other group members.

Yes, but this already exists.  It's called a mining pool.  It doesn't affect the existence of the fee market between pools still need to communicate block solutions to other pools and miners.

Now onto the last proviso: what if **all** the network hash power joins one big super pool?  Well in this case the fee market no longer exists.  There is no no one to lose an block race too; no orphans are generated.

OK, so we don’t strictly NEED a limit.  But maybe we want a limit anyways?  The field of Economics says something about this question too.  From the perspective of the economist, the block size limit serves as a production quota.

When Satoshi put the production quota in place 5 years ago, it served as an anti-spam measure.  Since it was to the left of Q* it didn’t affect the free-market dynamics.  It was actually 800 times greater than Q* so this line indicating the limit would be a block down the street.

Over the last 5 years, Bitcoin has grown tremendously, and I believe this limit is now on the left side of Q*.  This results in what economists would call a "deadweight loss."  This is the economic activity lost as a direct result of the production quota.  Some argue that production quotas can be good if they serve to reduce or eliminate some negative externality.  I won't weigh in on whether or not a negative externality exists.

Instead I'm going to ask how a group could enforce a quota agains the will of the market.  The market wants to be here (at Q*), the quota forces it to be here (at Q\_max).  How can the invisible hand of the market be restrained?

I’d imagine they’d follow the playbook of other command-and-control economies in the past.  First they would begin to censor those who spoke out against the quota to make it seem like everyone thinks the quota is a good idea.

[Shows slides with evidence of censorship]

Haha this may not be a completely hypothetical example!

The tighter they squeezed the more nodes would slip through their fingers to clients that support removal of the quota.

And then the attacks would begin..

[Shows slides with evidence of attacks against Bitcoin XT and Slush Pool]

In the end, I believe the production quota would fail.  The thing is that we can only really enforce rules that most of us agree with anyways.  Bitcoin will break down dams erected by special interest groups attempting to block the stream of transactions.  That's all I have to say about the transaction fee market.

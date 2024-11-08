---
title: 'Multi Party Channels In The UTXO Model: Challenges And Opportunities'
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Olaoluwa Osuntokun
---
<https://twitter.com/kanzure/status/1048468663089618944>

# Introductions

Hi. So my name is Laolu. I am also known as roasbeef and I am co-founder of Lightning Labs. I am going to go over some cool research and science fiction. In the actual implementation for these things and cool to discuss and get some discussions around this. first I am going to talk about single-party channels and multi-party channels.

# Agenda

So we have single-partyt channels and the promise of multi-party channels, the nthhe utox model and the account model for multi-paryty channels. We're going to talk about existing constructions for xutox-based multi-party channels. I'm not presenting a new construction, just building off of older stuff. I am going to talk about some new things that could be call and some problems with it.

# Single-party channels

So for starting we have a single party channel. We are going to emulate a shared account i using a 2-of-2 multisig channel, and on-chain control transactions for moving in and out funds from the channel using splice in splic eout transactions. This is rapid off-chain balance updates, and we can do cool things with HTLCs and we have hash-time locked contracts and bridging channels with HTLCs over the network and this lets us get more networky.

We also have limitations in single-party channels. The flow of funds are constrained by topology of the channels and this restriction requires you to do the upfront work about the otpology. You have to do something with lnd and you can use tets applications like that and you can dynamically create new channels. Each new channe lyou create requires an on-chain transaction and one chain per user would take a while, and each channel requires a single UTxo and one person can't have a UTXO for every person in the world and that causes scalability problems. We also have accumulator things and problems.

# Multi-party channels

In multi-party channels, we are a generalization of two-party contracts to multi-party contracts and have interactions. We no longe rneed a new UTX ofor each channel which wis good for scalability. Each channel can use a UTXO from other channels and maybe collapse them together. The cool thing aqbout multi-party channels is that it looks like a sweep, and you can use signatur eaggregation and use a single signature and it looks like a single output with a pubkeyhash and really maybe it's 100 people in a multiparty channel. Ypou can also have oc-located economiec zones ande they can interact with each other in multi-party channels, communicate amongs thtemselves, save on transaction fees, have low latency, and have certain guarantees. You can also do off-chain channel creation and destruction using dynamic route creation in the lightning network. This is really cool because now we can dynamically create routes between participants on the lightning network. Another cool thing is that you can have "tunneling" because you can now create routes between individuals and not have them on the blockchain and these can be ephemeral. I think one of the applications is like MMO gaming servers, and all the economy in the game is on a single multiparty channel not on a big public channel, the channel is super fast and they can all audit it. We can also have p2p payment focused applications like Square cash and everyone can be in the same channel. We can also do bill splitting and other venmo stuff.

# Multi-party channels iun the UTXo model and account model

In the account model you have a single account, a single contract, a nbunch of virtual accounts- we have seen this in plasma for example where you use hierarchical sidechains with exit clauses, root chain stamped in the main cheain. We also have osmething called NOCUST which is newer, whic hcreates a bi-modal accounts and ledger and periodically you sync these every few blocks. Before the epoch which isn't final yet, you need to wait until it's actually final. These typically require an operator and maybe the operator sees all the transactions and things like that and every single transaction goes through the operator.

In the UTXO model, ytou have some obstacles, like a lack of state in contracts tseems to force hierarchical constructions. You might have ten or five transactions and this might cause mass exits and will yo uget your money out in time is a good question. We typically have limited scripting in the UTXO model, so it makes scripting a little bit more difficult. But UTXos have a number of advantages like creating vcontracts off-chain; the account models have like factories and counterfactual instantation and you don't know the address going on-chain so you can create new contracts off-chain but in UTXOs I can just nest that transaction and get that guarantee. Creating a new contract off-chain would require something like SIGHASH\_NOINPUT and we proposed that a number of years ago, and maybe it's coming for eltoo or something. And finally, because of hierarchical states allow flexibility and decoupled updates, I can do updates in a subtree and maybe if you're in another subtree you don't know about that.

# UTXO based multi-party channels using lineage

Originally there was "duplex channels" which required a nested commitment replacement by relative locktime and nested timelock evaluation. Invalidation tree recursively applies relative-lock time to achieve longer channel lifetime. Addition of kickoff transactions later allowed for indefinite channel lifetime. These channels could then last a little bit longer. These had a finite lifetime and then CSV allowed for other constructions. Before, you had like 10 days and then extend it.

Something else recently is called eltoo where typically for lightning you have to use replace by revocking the old state. BUt in eltoo, you replace yb version and the best version is the latest version. For eltoo, you can say you can always publish a private state but there's never a punishment. Addresses on-chain blowup issue due to usage of invalidation trees. It can also use channel factories which is a framework for hierarchical multi-partry channels. You also need to have an invalidation tree and eltoo helps us get rid of that.

There's something claled channel factories which was a way of doing hierarchical channels in the UTXO model and you used validation trees for commitments but now with eltoo we can simplify this a lot and limit on-chain state blow-up.

Something interesting is lightning factories- it tries to do a channel factory construction in the revocation model. It applies replacement-by-revocation to a channel factory-like framework. This was recently published; like earlier this week. It uses BLS signatures to actually solve some of the interaction issues and you have n^2 communication.

# Channel factories for UTXO model

These are basically multi-party channels. They are a layered set of transactions of intermediate transactions. Typically you have one layer below that that you use that and then the penalty and you broadcast that and it would be final. The first thing is called a hook. The hook is the n-of-n multisig, so the thing is that evrey time we want to modify something for the hook in the channel factory we require all parties to sign-off ofr the updates. We also have the allocation which spends the hook itself and goes through smaller commitments. Imagine a few parties in the channel. So you could use this in mix and match to create a construction for what works for you. And finally we have a commitment which is a leaf nodes of 2-party channels, and it uses eltoo at leaves allowing for n+ leaf chains. I could do an HTLC myself here.

# New directions - new user off-chain channel creation

We could be able to join new channels without on-chain transactions, we could do this by partially addresing the on-boaridng poroblem of new usres to lightning network. Simply modify mexisting allocation to add key of the new user. We basically make a new key, and put it in a subtree, But the downside is that because we can't modify the hook, there's a bit of a trust model where it's bettween a custodian model and a trustless model. The ofcol thing about this is that once the user is in the channel then they are able to update the channel in place, without touching the blockchain. This allows for dynaimc growth of the number of users in channels, and the UTXO growth problem is contained. Unfortunately this requires new trust assumptions; how does the new participant know what the most recent state of the channel is? Need to ensure being "teleported" into the latest valid state within the channel, so this requires a channel auto-proof-- I can get this proof from the leaf all the way up to the root; but there's a threshold question here, how many parties am I going to get to attach to the state? Maybe all the parties lie to me, but maybe 2/3rds of them or something and then I can trust the maybe. It's kind of like a research question about "weak subjectivity" in PoS- who am I trusting about the latest state in this model? We can also splice in/out new funds participants via SIGHASH\_NOINPUT. The cool thing htat we can do with channel creation is we can splice in the participants from the hook transaction itself. If we modify the root allocation, without, that would be without the root txid and now all transactions in that tree are now invalidated.

# Threshold channel audit proofs

You need to fully prove every single channel in the tree from the leaf to the root; if they can give that to me, then I can bypass that- we use single SHA because now I can know with some degree of trust sassumptions this is the latest step. If I want to create a new channel, I can drop in and use these proofs and decide it's legitimate and go for it.

# Route tunneling

Right now in lightning there's a graph that is relatively static because opening and closing a channel is an on-chain state operation. Also we have a 10-minute block time. So updating the lightning network grpah is time consuming. But we can do route creation per the techniques described earlier in my talk. What if the channel participants are in the same multi-party channel ,and I can tunnel between them- it's sort of like a new dimension or a new underworld and you can tunnel them into the third dimension which I think is pretty cool. I can directly create channels based on the direction of the channel itself. Maybe hte liquidity wasn't sufficient for selling stickers or whatever is cool these days, I can advertise short cuts routes that tunen lthrough channel formation. We are able to create new channels in seconds to satisfy directional flow above above ground. This requires distance-vector like announcements, in contrast to circuit-switching widely utilized today. You can show that you have a path to the destination, maybe try with a small amount to test the route. Some ideas have been suggested for balanced congestion aware packet switching in the network, causing packets to go through the paths of least congestion. People talk about rebalancing but this would be automatic, which would be pretty cool. You could also use these in a bridge to multiple multi-party channels. These bridges can be reallocated. In your imaginoation because maybe you create a new one at any given time, at an upper layer and validate it and go from there.

# multi-party nodes

You can actually have multiple people in a single LN channel. Many nodes are under one pubkey in the network, it looks like a single regular channel. You can do aggregate channels and combine liquidity. This shrinks the size of the public graph, 100s of channels seen as a sngle channel. So maybe if you don't have enough money to go on-chain then maybe get together and you have enough money to pay the fees to get on-chain. So this one mega-node would then be something you could use.

The current protocol implements a limit on the number of outstanding HTLCs per channel. But with atomic multi-path payments we can combine these with a max HTLC size (essentially an MUT)( resulting in a constrained commitment space network wide. This allows you to split payments over multiple paths through the network. What you can do is use these channels to conditionally add newer twitch which-- the larger channel; the inode has like a direct block, then you have an indirect block pointing to more blocks and fan this out and have more space there.

# Hierarchical prefix addressing for lightning cross over

How to handle receives over multi-node network aggregate of multi-party channels/ Today HTLCs targeted at a single desitnation public key. Right now we have onion blobs but we can add extra data, another address in there. So based on the structure of the tree, I can have an address in there that would say left-right left-right and I can use that to route a payment among htese participants.

# Cross channel swaps using swaptions

Possible to exhcange positions within a particular channel, or even trade positions within distinct channels. So typically there are some issues with atomic swaps, but once we do this we all the transactions are laid out, we can defer execution. We don't want this to happen because we want everything to be timely, and we don't want the atomic swaps to stop the liquidity. So a swaption is an option to perform an atomic swap. Alice sells Bob the option to do the swap himself. So the difference is now there's two secrets- the acceptance layer, once Bob buys the swap, Bob is now going to wait since Alice has been compesnated. Bob has paid a premium to get he swap. And then there's an exercise layer to go ahead wit hthe swap. You can do swaps for cryptocurrencies, channel accpetance, and other things like that. Bob can exercise the option til expiration by revealing his secret. This allows for people to sell their channels within other channels. You can use a swaption to sell channels within channels.

# Channel orchestration servers

Distributed version requires quadratic communication for re-allocations scaling with the number of participantsi n internal nodes. This shifts to single key n-of-n Schnorr requiring additional round trips for each signature. We can use a message passing server to reduce to linear communication cost. We might be able to use this for offline payment receipts; why not also use orchestration servers for offline mailbox? We can pay orchestrators to deliver messages with set deadlines. This allows for quasi-offline payment sending/receipt, and during clearing phase the HTLC add, if participants not offline within threshold, cancel back. During settle phase, fully async as receiver is to pull things forward.

# Open problems

One problem is how do we cut-through to reduce the on-chain footprint in mass exit cases?

How do we use covenants to allow hook transaction modifications wihtout all the parties involved? Maybe something with taproot or something magic like htat.

Other question is how to do health check protocols to splice out inactive parties within allocations. We need to have a way to efficiently figure out if someone is inactive and get them out of the channel.

How can we have the language express swaptions and swaps and things like that? We need a high level language to do this, maybe something like BitML? It's from some academics in Italy, it's a high-level language that compiles down to transactions and scripts. This give syou a full transaction execution tree.

The other thing is, how do you do the efficient execution of fees + timelocks in the packet-switched model? You might end up paying the max fee every single time, which is not ideal.

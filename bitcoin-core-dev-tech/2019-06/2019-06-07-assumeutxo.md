---
title: AssumeUTXO
transcript_by: Bryan Bishop
tags:
  - assumeUTXO
  - bitcoin-core
date: 2019-06-07
aliases:
  - /bitcoin-core-dev-tech/2019-06-07-assumeutxo/
speakers:
  - James O'Beirne
---
<https://twitter.com/kanzure/status/1137008648620838912>

## Why assumeutxo

assumeutxo is a spiritual continuation of assumevalid. Why do we want to do this in the first place? At the moment, it takes hours and days to do initial block download. Various projects in the community have been implementing meassures to speed this up. Casa I think bundles datadir with their nodes. Other projects like btcpay have various ways of bundling this up and signing things with gpg keys and these solutions are not quite half-baked but they are probably not desirable either. The thinking here is that we want to do something analogous and do it right and make it relatively safe. There's technically a slight change in the security module.

## What is assumeutxo

You get a serialized UTXO set snapshot obtained by a peer. This all hinges on a content-based hash of the UTXO set. The peer gets headers chain, ensures base of snapshot in chain, load snapshot. They want to verify the base of the snapshot or the blockhash is in the header chain. We load the snapshot which deserializes a bunch of coins and loads it into memory. Then we fake a blockchain; we have a chainstate but no blocks on disk, so it's almost like a big pruned chain. We then validate that the hash of the UTXO set matches what we expected through some hardcoded assumeutxo. This is a compiled parameter value, it can't be specified at runtime by the user which is very important. At that point, we sync the tip and that will be a similar delta to what assumevalid would be now, maybe more frequent because that would be nice. Crucially, we start background verification using a separate chainstate where we do regular initial block download, bnackfill that up to the base of the snapshot, and we compare that to the hash of the start of the snapshot and we verify that.

The fakechain is a CChainState object without any blockdata. It's an ordered headers chain. It's kind of like a pruned chain. We load in the snapshot, we deserialize everything into a CCoinsView and then we have to construct a chain object to go with that even though we don't have any block data. We're fast forwarding a header chain up to the base of the chain. We have to think about a few things like ntx and chaintx to get accurate estimation of the remaining verification time to tip. There's a few things we have to hack in there.

Q: What about reorgs?

A: We don't account than reorgs that go into the snapshot. The idea is that the snapshot is at least a week old or something. You won't get a reorg that does that, and if we do then we have bigger problems.

## demo

There's some assumeutxo demo. Here's a demo. This demo is a server node that I have pre-populated up to a height of like 30,000. Basically you're going to see this sync to tip. This thing is only 4000 blocks ahead of the snapshot. Then it will switch to background validation, and then you see the background validation chain disappear. This is all thorugh some hacky RPC call that I created.

## Wallet usage during initial block download

Once the user gets the network tip they can start using the wallet. One caveat is that if the wallet has a last updated height below the base of the snapshot, well we can't do that until we can rescan so we just disallow that.

## Objections

This is easier to attack than assumevalid. With assumeutxo, all you have to do is serialize out a bad UTXO set, give someone a bad hash and get someone to accept that bad hash and then you convince them maybe their coins don't exist or hwatever. The security here hinges on using the right binary. The argument is that if you're using the wrong binary, there's a million different ways to screw you really easily anyway.

Someone raised the point that if we're okay with accepting this snapshot security model while we're backvalidating, then maybe background initial block download is pointless. What happens in this implementation if background IBD result doesn't match up with this? We freakout and shutdown. So you're getting close to the tip anyway, so you could just overwrite... we could reorg. You could invalidate the block of the assumeinvalid and then you move on. Screaming and shutting down seems like the right thing to do. They need to know their binary is broken. So we shutdown. Or the developers are corrupt. Or there's a bug. What it should really do is delete the Bitcoin Core binary when that happens ((laughter)).

In the best case, it means you need to catch-up a half-year of blocks because we do releases every 6 months. So there's a maximum speedup that this can do. When I looked at options for casa hodl alternatives, either it's immediately ready which is what a user wants, or they wait. Whether they wait 6 hours or 2 days is a different, but it's way different from waiting half a minute versus an hour. There's a user experience preference basically. I think it's great but I don't think it solves the problem where a user wants this immediately.

Q: How is the hash of the UTXO set constructed? I've been working on that for like a year.

A: Great question. For now, it's a naieve hash of the UTXO set contents. That's contingent on how we want to transmit it, what are the contents, one option is for it to be a merkle root. I think we're going to want to do some scheme where we bech-encode this thing and split it up into a bunch of different chunks. The commitment structure, I'm not really sure yet.

It would be useful if sipa's rolling hash, and we can eventually make a commitment. We can do assumeutxo first, and then later on, we could do.... It's like chicken-egg problem. There's a lot of low-hanging fruit that can be fixed with utreexo. You can already incrementally verify; you can ask for UTXOs in the set; you don't have to download 4 GB at once to see. You could say, resource usage from duplicate chainstate is significant but in utreexo you could say I'm going to hardcode a hundred different UTXO roots and you can parallel validate it, like imagine 80 cores not just 4 cores or something. They are suggested UTXO sets, and you can validate all of them and see if they link up.

In assumeutxo, if you get a false set then there might be some coins that don't exist. But if your utreexo is false, then you will detect within some blocks that it is false. Another thing you could do is encode separate checkpoints and then dependening on when the wallet was created, you can take the one that was previous to when the wallet was created and go from there. You do the validation later.

## How assumeutxo

I have divided this up into phases. The first phase is allow snapshot use via RPC, and no distribution mechanism. Only sophisticated users will do this. It doesn't matter where they get this from. Maybe put the hash on a CDN but we don't want to do this long-term. We could use bittorrent, IPFS, whatever. The second phase is more speculative but it's build distribution layer into the p2p network, with like FEC-encoded chunks. We could split up the snapshots into Reed-Solomon codes and fountain codes so that it's not just a naieve striping of data which would be vulnerable to DoS. But with Reed-Solomon you have to talk with n unique peers and then piece it together from that.

For phase one, we have to do a bunch of refactoring because in the code we assume there's only a single chainstate. Some pull requests have been merged related ot this. There's some snapshot creation/activation logic. There's some minor `net_processing` changes. We have to think about how this effects pruning and cache management, and introduce some new RPCs.

We should assume there isn't going to be a soft-fork for assumeutxo. We should try to make it work without one. If we get a soft-fork for it, then great. If we do assumeutxo then we will have an intuition for what the commitment structure should be in the soft-fork. The reason we don't have UTXO set commitments is that it has been argued what it should look like every time it has come up. So a working assumeutxo might give us some evidence or experience with this and be able to better make a decision about a soft-fork for UTXO set commitments.

## Refactoring details

Right now, the M.O. is to deal with the interface that validation.h gives you, and this operates on one global chainstate. Instead, the CChainState interface has been made public- this is already merged. We put all the global functionality into the CChainState methods and you can pass around these objects. We break out shared block data into a new class, BlockManager. All CCoins views are owned by a given CChainState instance. All the validation interface callbacks now need to know which chainstate they are dealing with.

`g_chainmain` is the chainstate manager and it abstracts dealing with multiple chainstates, it acts as a factories for creating chainstates. It does a bunch of things.

## Wallet details

We're not going to rescan if the wallet was updated previous to the snapshot base. The solution to this might be the block filters, we could use them also here. Yep, definitely.

## Cache details

The advantage of having a big cache only comes in play when you're doing a lot of validation. I allocate most of the cache to the background validation of chainstate, and then afterwards allocate it back to the other one. Once you hit the tip, then the background validation starts.

## Pruning details

Pruning can happen aggressively for background validation chainstate since we don't expect reorgs (within 1 block of tip). Kinda marginal because of extra 3 GB chainstate.

## utreexo stuff

If you want assumeutxo that is the same structure as utreexo, you can do that without worrying about any caching because the point isn't having a tiny little node the point is so that I can incrementally download the entire UTXO set and then go from there as a normal node. So that's like using a smallish part of utreexo, it's basically some merkle trees at some point. You don't care about transitions in the accumulator state, you just have a single accumulator state and you want to verify UTXOs in there. You don't want to miss any UTXOs, either, but that's straightforward.

Is there benefits from validating backwards? If a coin ends up in an OP\_RETURN then you don't have to verify the signatures in the past? Well, you still want to be in tune with everyone else. I don't know if the 10 different parallel validation things is useful, it seems like it's not useful but maybe. You can just set them to the number of cores you have. Well, you hardcode like 100 of them, and then you use as many up to the number of cores your CPU has.

## Other changes

There's a few places where instead of acting on a single chainstate, we just get all the relevant chainstates from the ChainManager. The actual diff in net\_processing is pretty minimal. Then there's some init/shutdown stuff, some metadata serialization about whether we have a or not... there's really not that much to it.

The format of the RPC calls, it just writes out serialized bytes. It's reusing the same thing we use for getutxosetstats. We just go in order, for each in the leveldb. I think this works.

## About phase 2

Nodes would store some number of FEC-encoded chunks across n historical snapshots. In this version, assumeutxo isn't a scalar, but a list of height-hash pairs. How do we generate snapshots before assumeutxo updates? How many snapshots do we keep around anyway? Maybe we say every 40,000 blocks we generate a snapshot or something. I haven't really thought about it.

The FEC-encoding solves the problem that-- for each node, we want each node to store a few versions of the snapshot, but the storage burden might be high. You don't want to retrieve your snapshot from a single peer. It's that you don't want to retrieve it from a single peer, not that you don't want to store it. If you didn't use erasure coding, someone could DoS the network and take out all the nodes that offer a specific snapshot of data. But in my mind, why wouldn't every node all have this data anyway?

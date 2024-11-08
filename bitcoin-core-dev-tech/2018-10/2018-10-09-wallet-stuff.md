---
title: Wallet Stuff
transcript_by: Bryan Bishop
tags:
  - wallet
date: 2018-10-09
aliases:
  - /bitcoin-core-dev-tech/2018-10-09-wallet-stuff/
---
<https://twitter.com/kanzure/status/1049526667079643136>

Maybe we can have the wallet PRs have a different review process so that there can be some specialization, even if the wallet is not ready to be split out. In the future, if the wallet was a separate project or repository, then that would be better. We need to be able to subdivide the work better than we already do, and the wallet is a good place to start doing it. It's different from the consensus critical code. A change to coin selection will likely not effect the GUI at all.

Q: When do we get script descriptors stuff?

Q: What are people working on and what do they care about?

I'm working on offline signing. Basically like what Armory has in terms of workflow. Create an unsigned transaction, copy-paste it in PSBT format, take it to an offline machine, take it back to an online machine, broadcast it. Merge it, broadcast it, stuff like that. I'm doing this to get myself off of armory. This is also my full-time job now. Much to my deep regret, I'm primarily doing GUI work. I want to be able to do it in if it's 2am and I need to move some coins and I had something to drink, I don't accidentally send them to Mali. Armory was surprisingly good; it's really nice in many ways and also it's had a few critical money-losing bugs one of which was quietly fixed so I'm afraid. There's no GUI flow for creating multisig right now, or for creating watchonly, or for doing multisig on RPC. The RPC flow is terrible anyway. The RPC flow has like 37 steps and you need to ask someone how to do it; well now it's 32 instead of 37. I would like to have watchonly bip32 working properly, and I know there's contention about how that should work. Yeah, script descriptors. I feel like one of the reasons why there's so much argument about how to handle watchonly in Core is that we have watchonly and spendable coins in the same wallet, but if we forced them to be separate then it would be more sane now that we have multiwallet. In v0.17, there's a mode where not having private keys at all now. It's --disable-private-keys. That only separates watchonly and solvable... you might to split those apart entirely. For offline stuff, you still need solvability. We should aim for solvable things rather than just watching; you could just watch, but really that's just useful for looking at a balance and seeing if payments were received. The no private key mode is all solvable? It's just making sure there's no private keys, and no other changes. Once we have descriptors, it feels to me like it makes sense to say that a wallet is a descriptor or a descriptor family. If you want another descriptor family then you want another wallet, maybe. A wallet is the unit of coin control. I've never run into a case where I want to do coin selection from multiple separate descriptors. But I imagine some people probably do. The way that the GUI works right now is that you have a drop-down to select a wallet, and the ndoing a spend uses the currently selected wallet. If you say you want an unsigned transaction, which coins are you trying to spend? Just the watchonly coins? The solvable coins? Are you trying to sign using something else?

watchonly was introduced for the situation where I am a participant in a multisig and I want to see those transactions but I don't want them to be counted towards my balance. That's why watchonly was introduced. I think something that was a mistake was making watchonly be a synonym for "not having the private key". Is it no longer a synonym? It still is. In the disable private key mode, they are all watchonly and don't show in the balance.  There's another pull request that ignores your normal balance and shows you another one. Can we get the watchonly balance over RPC? It's getbalance, dummy, minimum, and then includewatching. You have to do all three parameters.

... watchonly should be disentangled from having the private keys or not. If I am using a hardware wallet, then I don't specifically have the private key in my wallet file, but it is my balance and I want it to include it in my balance. I want everything to treat it as mine. Armory has a checkbox per wallet for "treat as mine". For Bitcoin Core, the watchonly flag would be on the descriptor and it will be independent from the fact of whether you have the private key there or not. The watchonly flag means it is not by default counted in your balance. It means you don't want to see the balance; you might want to give it a positive meaning though, like "treat as mine". Maybe give it a completely different name and drop the name watchonly.

If you have different sets of coins, is the aggregation unit there a wallet or something else? If it's wallets, then maybe show all your wallets together. You could create a partially-signed transaction and move it from wallet to wallet on the same Bitcoin Core wallet instance.The coin aggregation domain should be the wallet. Watchonly and non-watchonly, ismine and watchonly should be separated into separate wallets as a general policy.

If you don't have any private keys, then show the watchonly balance as the normal balance? Make it the normal balance? ... In the glorious future, when you import a descriptor, you choose whether ismine, and if it's not then it doesn't contribute to the balance.

You want importmulti to support descriptors in the API, but convert it into wallet-fu in the wallet. Later on, you can make it do better things. Should we just remove all the other import commands? First we should make importmulti not suck, then we should remove all the others. Maybe deprecate the others.

importmulti shouldn't take anything other than combo right now. Later, you can make importdescriptor and then deprecate everything else including importmulti.

The difficulty is replacing the key pool. It's a cache of public keys specific to a descriptor, rather than a global wallet thing that feeds into everything else. Descriptor implementation needs to have some form of here's an opaque object with cached things, for hardened keys you need to have the pubkeys pre-expanded. You can't derive addresses otherwise. That needs to be there. How do we deal with existing logic that uses a key pool and ismine logic and the new logic that uses descriptors? I think inevitably these two for at least a while need to live side-by-side. Can we do forced upgrade? I think it would be nice over time to have a way of doing a one-time conversion of here's all the goo in my wallet, please convert it to a minimal set of descriptors that do the same thing. But this would not be something to implement in the short-term. This is related to combo.

Q: Is this going to be in one huge PR?

A: I am going to add support in the descriptor module for having pre-expanded keys, which is just a logic change not exposed anywhere. Then we'll need to remove some of the existing ismine logic, which is currently global, to become more encapsulated as a wallet method. Possibly have a way to have multiple instances of that. And then you can add a second store with the descriptors.... and then later have a way to convert the existing stuff into the new thing.

Q: Does it make sense to have a wallet bitflag for this?

A: No, I don't think so. It's just going to be a new version of the wallet once you have the new records. Moving from the keypool being a global thing into having it more encapsulated. I'm not quite clear on how to do that implementation.

Q: script descriptors are replacing ismine but also this keypool and these are two different things?

A: Yes.

Q: What's the challenge with the key pool?

A: Too much logic that I haven't reviewed recently. It's integrated in many places.

Maybe there should be a separate or second bi-weekly meeting to talk about wallet. Maybe bi-weekly. Monthly, scheduled by Icelandic time zone. Twice weekly is semi-weekly, not bi-weekly. No that's not right. Bi-annual means twice a year, unambiguously. Semi-weekly means twice a week.

Some people want to export transactions from the wallet, like for tax reporting. They want to export transaction history so that they can file taxes, in combination with exchanges and accounting. Once you have a dumpwallet alternative that spits out json, that would be helpful. dumpwallet doesn't give transactions, but a new thing could. listtransactions also does that right now. There's a tax jursidiction where if you have at least a million dollars, they assume you can make at least 4% on that, and so they tax that gain at 30%. If your net worth jumps significantly from one year to another, then they are going to investigate that.

Another thing that is needed is a berkeleydb replacement.

Process isolation and separation... people seem to think it does complex stuff it doesn't actually do. It replaces CBlockIndex pointers and it calls through an interface. It's a very mechanical change. It changes nothing at all. It's just the interface between the wallet and node. People seem to be intimidated by these pull requests, it's 25 commits, but each one is pretty small. The CBlockIndex stuff is the heart of the PR and then a bunch of smaller commits. I'll take the first 5 commits and put them into separate PRs.

Wallet PR#s that gets us manual PSBT hardware wallet magic:  14075, 14021, 14019

There needs to be a script to show the difference between the last time you reviewed and now.

wallet PR#s that gets us manual PSBT hardware wallet magic:  14075, 14021, 14019

What about upgrading wallets? In v0.17, we can do upgrading non-HD to HD. But the upgrade happens at startup, and if your wallet is encrypted then....  So, with the descriptor stuff, we might also need to have the wallets decrypted in order to upgrade. I don't think necessarily we should be upgrading at startup. It should be an RPC and they can do an upgrade, "upgrade this you can't go back". What happens if you start Qt? Does it just not start and not load the wallet? In the proposed future, it would load the wallet as currently and not upgrade. But you have to support the old stuff, because you can't do a one-time upgrade until it's decrypted. You could make it watchonly though. You can refuse loading it, you don't have to support it. But the upgrading can be, click the button instead of just doing it. I personally hate that, but it's a way to make it work.


---
title: Electrum
transcript_by: Michael Folkson
date: 2020-08-09
speakers:
  - Thomas Voegtlin
  - Ghost43
media: https://stephanlivera.com/episode/199/
---
Topic: Electrum Wallet 4

Location: Stephan Livera Podcast

Electrum GitHub: https://github.com/spesmilo/electrum

Transcript completed by: Stephan Livera Edited by: Michael Folkson

# Intro

Stephan Livera (SL): Thomas and Ghost43. Welcome back to the show.

Thomas Voegtlin (TV): Hi, thank you.

Ghost43 (G43): Hey Stephan, Thanks for having me.

SL: Thomas, my listeners have already heard you on a [prior episode](https://stephanlivera.com/episode/125/). Ghost, did you want to tell us about yourself, how you got into Bitcoin and how you got into developing with Electrum Wallet?

G43:  I got into Bitcoin a few years ago because I had some personal bad experiences with the traditional financial system. I only started using Bitcoin for doing a couple of donations but then I set up cold storage and I’m full on using Bitcoin since then. I started contributing to Electrum almost three years ago now. At that point I had been using Electrum for a year or so already but near the end of the summer of 2017 I had a lot of free time and I decided I would fix a few bugs that had been nagging me that I experienced as a user. First I was only fixing a few things in my free time but then I spent more and more time on it. It became a full time job basically. Thomas offered me a job back then so since then I’ve been working for Electrum Technologies and I get paid to work on stuff that I love and would use anyway.

# Electrum v3.38 and v4

SL: That’s great. Today we’re going to chat more in detail about Electrum Wallet 4 which is the new release. Thomas, our last interview was towards the end of last year. There was a gap between versions 3.38 and version 4. Can you tell us about that?

TV: Just to bounce back on what Ghost said, if you want to work for Electrum, if you want to have a job it is a very good idea to start by submitting pull requests. From there on you might actually end up being a full time developer. That’s my two cents. So why was there such a big gap? Last time we talked on your podcast I mentioned that we had just merged the Lightning branch into master. We had code that was already fairly stable but merging it into master triggered a lot of code reorganization. There are things that you cannot do when you work on two branches. You can only start doing them once you have the thing on the same branch. Since it is a big change we did a lot of things that have to do with the code architecture and how things interact that couldn’t be done before we were working on a separate branch. We had to test a lot of edge cases people will know with Lightning. The difficulty is not the happy execution path, it is when things go wrong. This involves a lot of testing. Along the way we added more features that we were not planning in the first place. This is also one of the reasons why it took so much time.

SL: Let’s talk about some of the new features that came in. Obviously Lightning is probably the big thing. Can you tell us how that came into Electrum and what your experiences were there? What were some of the hurdles or what were some of the things that were difficult getting Lightning into Electrum?

TV: When I say new features, along with Lightning we added things such as watchtowers and submarine swaps that were not planned initially but that are nice to have too.

G43: Lightning is a meta feature. There’s a reason we’ve been working on it for like two years.

TV: It has been a long process.

SL: Let’s talk about the process of setting it up. I had a play around with Lightning on Electrum to test it out. I spun up a test wallet, put a small amount of sats in there. I noticed you’ve got that additional tab with the channels. You go into Wallet Information, enable Lightning on that wallet and then you can start the Lightning part of it. I noticed when you go to open a channel there’s also a suggest box where it suggests a node to open the channel with. Can you tell us about that feature and how that suggestion works?

TV: In terms of GUI things are not really finished or set in stone. The feedback we have received from users suggests that it might be a bit confusing because users do not expect to have to visit that dialog in order to enable Lightning. I’m thinking we might actually move that button into the Channels tab. The user interface is really our first iteration. We are going to change a few things there.

G43: Specifically on the wallet information dialog thing to enable Lightning, we made that decision as a temporary thing as far as I recall. We wanted to make it a bit more hidden. We didn’t want too many users to enable Lightning at the same time as soon as we release and have more bug reports than we can handle.

TV: That’s also the reason why we have not yet enabled the notification that there is a new version available. I’m planning to do it in the coming days. That’s because I was away from from my computer. At the moment we want to slow things down so we don’t receive more bug reports than we can handle.

SL: What was some of the early feedback on the new version of Electrum?

TV: Some users were confused and are still confused. I’m not talking about Lightning here. I’m talking about the way you do coin selection. It is related to Lighting because we wanted coin selection to be more generic, to be usable with not just onchain transactions but also when you open a channel or when you do a submarine swap. You want to be able to to select the coins in any context. So Ghost43 had this idea to have this coin selection visible from all the tabs. That means you have to do it in two steps but it is much more powerful. Another thing is in the Send and Receive tabs now we handle both onchain and Lightning transactions. That means requests are abstracted away from whether they are oncchain or Lightning. The onchain fee is decided after. These are the new things that have confused some users.

# Submarine Swaps

SL: Essentially when switching between doing a Bitcoin onchain transaction and thinking in terms of sats per byte to doing a Lightning transaction it is different how it operates there. I also noticed that there’s a few different dialogs. You’ve got watchtowers and swaps. I had a look in the dialog and it looks like that’s going through Boltz exchange. So can you tell us how the submarine swaps feature works?

TV: It is not going through Boltz exchange. It is a node we are operating using the Boltz software. That’s not exactly the same. It is also a new business model for us because we are collecting the fees. We hope that is going in the future to develop as a new source of income. If you are familiar with the Boltz exchange the UI is very close. What we have done is give a bit more freedom to the user in terms of selecting the fee. You cannot do that on the website of Boltz. It is a double edged sword because we give more power to the user but it also implies that they can shoot themselves in the foot more easily. In the end it is not so dangerous because if the transaction never gets mined you can cancel the whole thing.

SL: In terms of the submarine swap could you tell us what direction and what context it would work in? Let’s say I’ve just funded my wallet. Is the idea that I can create a channel and push some of that balance out of the Lightning channel and receive it back onchain. Now I’ve got more incoming capacity. Is that the idea?

TV: That is the main use case. We have this issue that if you’re a merchant and you want to receive Lightning funds you do not necessarily have a channel with incoming capacity. Initially we thought about creating a server like Bitrefill, they open a channel to you for you and that’s a service they charge for. We thought about that. Then I found about this Boltz exchange software that is nice and easy to use. It allows us to do more things than just a service that opens a channel. For the user it is better to have swaps. This submarine swap is also known as Loop In, Loop Out if you use the terminology of Lightning Labs. They also have the same service with a different name.

SL: Which direction is it in?

TV: You can go both ways. If you open the Swap dialog you can click on the Lightning icon and it will swap the Lightning and Bitcoin icons. You can either send onchain or you can send Lightning. You can also switch in the same way on the Boltz website.

SL: Let’s say you are a merchant, you’re taking a lot of payments. Over time all the balance is sitting on your local side and you need to push it back out. That’s where you might use that swap.

TV: That allows you to keep receiving on the same channel. That’s good because the customers that have found the path to you are likely to find the same path again in the future. So if that channel gets exhausted you probably want to rebalance it.

SL: In terms of opening channels, let’s say I open up my Electrum. I fund it with some Bitcoin. I try to open a channel. I was having some issues trying to manually open channels to some of my own Bitcoin nodes. I was able to do it through a suggested one. Is there any difference there in terms of using the URI to pick which node? I think the box currently says Alias. Can you outline a little bit around that?

TV: Which box says Alias?

SL: When you open a channel you have to paste in the pubkey of the other person you want to open the channel with.

TV: You can paste a remote node ID or a connection string. It is the node ID plus the IP address and the port. If the node is already in your database then you don’t need the full connection string but sometimes it is not going to be the case. That’s why there are connection strings. The Suggest button will give you a node that you are already connected with so we know that this node is online.

G43: The Suggest button is very naive at the moment. We are going to change it probably in the future. At the moment it just gives you one of the nodes you already have a transport connection established with.

# Watchtowers

SL: Let’s talk about watchtowers. For people who might’ve used another Lightning wallet or Lightning daemon they’re used to that daemon monitoring the chain to check for if somebody is trying to cheat you etc. Can you outline how the Electrum watchtowers work? I see you’ve got two different models there.

TV: We developed this because I was thinking about watchtowers as a business model for us. The idea was that we were going to have a watchtower as a service for our users. I backed up because the requirements in the current model are too large. So currently the Watchtower implementation that we have is ok for your own personal use but we did not implement a user authentication system that would allow you to have a watchtower with many users. You are asking about the different models. There is this idea that you could incentivize the watchtower by giving them a share of the justice transaction and you would not need to pay them. I don’t know if anyone has ever actually implemented that kind of watchtower because you don’t have good guarantees if you use this type of watchtower because you have strong anonymity. The watchtower doesn’t need to know anything about you. But you don’t have the guarantee that they will keep watching your channel forever or for the life cycle of your channel. My suggestion was to have a watchtower that knows a few things about your identity so it knows about your channels and so that you can at least trash the data when the channel is closed. Then you can save some disk space. The idea was to have a watchtower that would not charge you for the justice transaction but it would charge you for the action of watching. You would need to have a subscription for that kind of service. We did not develop this fully into a commercial service. The code is open source. Someone else can use it to do that if they want. At the moment we decided that we are not going to offer this as a service. The watchtower code is useful if you run your own private watchtower and you can do this. For example if you have a machine that is always online but you don’t want to have private keys on that machine. If you have your own private Electrum server it makes sense to also have a watchtower on that machine.

G43: On the question of there being two different watchtower models in the current code, there’s the local and the remote watchtower options. The remote watchtower is what a power user might think about watchtowers without compensation. If you have multiple computers, let’s say you have a server or an always online desktop machine back at home then you could use the remote watchtower. You run Electrum with the watchtower options configured always online or almost always online on that machine. Then your other client sets a remote watchtower to connect to your home machine. The other option, the local watchtower is specific to Electrum. In Electrum you can have multiple wallets. I’m not sure whether this is true about any of the other current Lightning wallets. If you create multiple wallets in Electrum you can even open them at the same time simultaneously. Enabling or disabling Lightning is independent among the wallets. You can enable Lightning for two out of five of your wallets or whatever. You can even open them at the same time. Then they will spin up independent Lightning nodes with separate IDs and their own channels. This introduces complications. Without a watchtower if you have Lightning enabled in one of your Electrum wallets but you don’t have that Electrum wallet open because you’ve created another one for your work funds or whatever. You only have that one open and you’re using that one to do a few transactions. If your counterparty cheated and breached one of your channels for your other Electrum wallets then you wouldn’t notice because that’s a completely independent wallet. It’s a separate Lightning node. To check for that, naively you might think that you might want private keys but in any case you have to have some kind of information and you have to have this wallet decrypted. If you enable a local watchtower with Electrum then we will save some information that doesn’t include private keys on your local disk such that if any wallet file is open with Electrum, if Electrum itself is running independent of what you are doing, then it will watch all of your wallets at the same time.

TV: I just wanted to make one thing clear. It might be obvious but if you run a watchtower you don’t need to run a Lightning node. A watchtower is simply a daemon that watches the blockchain. If a UTXO is spent then it broadcasts a transaction. When you run a watchtower it is completely independent from running a Lightning node.

SL: Let’s say the user is running Electrum Wallet on their laptop and they open up some channels. Later they close their laptop for the day and they’ve gone to sleep. They only open their laptop again when they wake up in the morning. At that point the local watchtower on the laptop running on that Electrum Wallet would then pick up “There’s been a transaction onchain. I need to broadcast the justice transaction.” Is that how it would work there?

G43: The point of running a local watchtower is that you don’t need to have the wallet file decrypted. That’s the most simplistic use case. You might have everything encrypted, the whole file and you need to enter your password to open it. You might have multiple wallets and without some kind of architecture such as this local watchtower you would need to decrypt all of your wallets and have all of those checked for breaches. But with the local watchtower it’s enough to just start the application and don’t care about that. You don’t need to open all of your wallets.

SL: Because otherwise you might have to sit there doing the five different passwords for your five different wallets.

TV: You can even have the application run in the background without any wallet open, there is a GUI preference for that. So in that case the watchtower will be active.

SL: For users who are running an always on node, the package node in a box, things like myNode, Nodl and RaspiBlitz. If they package in an Electrum server it might make sense for them to also package in the external watchtower. That way it is always running there.

TV: Yeah absolutely.

# Static channel backups

SL: Can you talk to us about the use of static channel backups for Electrum Lightning?

TV: The backups that we have do not allow you to restore the channel. That’s also the same with lnd. The only thing you can do with this kind of backup is have the channel closed. It should not be confused. There should be a different word than backup but I don’t have one. The main point here is that if you have a Lightning channel the funds in your Lightning channel cannot be recovered from your seed words. So in case you lose your device or you have an accident you probably want to have a backup of your channels. Currently we use a static remote key and that static remote key is one of the public keys of your wallet. That’s a feature that might not stay in future because it won’t be possible anymore soon because of some changes in the Lightning protocol. Currently you have this extra comfort that if the remote party force closes the channel your funds will land on your wallet whether you have made a backup or not. You could argue that the backup currently is not very useful but it will probably be more important in the future if this feature is removed.

# Electrum Lightning Implementation

SL: Can you tell us about your efforts doing your own Lightning implementation? Has that been difficult for you?

G43: Originally we didn’t want to do our own implementation. We had another developer who experimented with another model. We researched other existing implementations to see whether we could somehow package them up and write some API to use those. But in the end as amusing as it might sound it turned out to be easier to write our own. Maybe it wouldn’t be the case today with rust-lightning which was written with this use case in mind of packaging it into an existing wallet. Back then rust-lightning didn’t exist so we decided to write our own implementation. The main advantage for us is that because it is written in Python and because we are the ones maintaining it, although that entails burdens, we can experiment freely with it and implement stuff that is not part of the protocol yet. Experimental features, it allows us more freedom. For example, we could come up with features such as what ACINQ is doing with Phoenix with the experimental TLV type length value extensions.

TV: Also trampoline routing. We have more freedom to experiment and to implement our own features. It is a lot more motivating than having to adapt to a moving target, another implementation that changes its API every time.

G43: Originally when we started with this approach, maybe in April 2018, we didn’t think it would take this much time. We thought that we might have a prototype that works for the happy path in like two weeks but that was overly optimistic. Even for something that worked somewhat reliably for the happy path it took like two or three months. After maybe a year we had something that worked okay but it was almost trivial to trigger bugs that resulted in critical issues. That’s why it took more than two years in the end. It’s a lot of work to implement Lightning from scratch. You don’t want to do it unless you really have the resources and you can commit to it.

SL: With rust-lightning I presume you’re referring there to LDK by the Square Crypto team.

G43: I guess that is the new name for it. Originally when Matt (Matt Corallo) started rust-lightning, at the very beginning he said that he wanted to just experiment with Lightning. But after a few months he said that he wanted to write something that could be integrated into existing wallets. That’s been the narrative ever since as far as I’m up to date with it. That’s exactly the use case we would have needed except it didn’t exist at the time.

SL: It would too difficult now to change back?

G43: It would be a lot of work I think. We are more comfortable with Python code and we can freely change anything and are deeply intimate with how the code works that we wrote now. At this point it’s not worth even trying to change it.

TV: I think Lightning is so important that at some point someone would have started to write a Python implementation of Lightning if we didn’t. It is also about the language, people are familiar with the programming language.

# Electrum User Experience

SL: I wanted to chat about user experience. When the user is starting up Electrum for the first time, there’s been some discussion that people who are more privacy conscious might want to get prompted when connecting to their own server or to a public server. Do you have any thoughts on that and whether anything could be done there around the user experience for the more privacy conscious?

TV: There is a difference between the Android app and the desktop. The desktop app allows you to do what you just said. We have had the request to have the same option on the application which doesn’t have it at the moment.

G43: You can already do this on QT, on desktop, but not on Android yet.

SL: You open it up and then in the bottom right you click the connection, red light or green light. We’re referring here to the first time set up of Electrum Wallet?

G43: It is a special case in what we call the install wizard. If you start Electrum and you don’t have a wallet, or even if you do have a wallet but it’s encrypted, the wizard will open to allow creating new wallets or entering your password for your existing encrypted wallet. We have logic to detect that it is the first time you start the wizard. That means it’s the first time you started the application itself. If so there’s an extra dialog at the beginning which is the same as the network dialog users might be familiar with as part of the main application, when you already have a wallet open and you can configure to only connect to one server or connect to your own server or any combination of these.

SL: Any thoughts on whether that could be made easier for some users who aren’t as comfortable with command line or doing manual configuration? Is there anything that you might be able to add to the user interface so the GUI only user can achieve a similar level of privacy, like a one server option?

G43: We have plans to make the Android application up to par, to implement the same with Android. On desktop I think even in the GUI, this is already possible. I guess it’s not that well known. There’s a prompt when you open Electrum for the first time and you can set up this one server mode. Maybe not one server mode but definitely connecting to your own server.

SL: I think you can select your own server but there’s that thing where it shows you how many other nodes or how many other servers you could connect to. If you’re more paranoid and you only want to connect to your own one.

TV: I don’t want to promote too much the one server option because it’s actually a deep reduction of security. If you don’t use it with your own node and you use it with an external server that is not yours the one server option makes SPV ineffective.

G43: You’re talking about the scenario where that single server operator is also a miner?

TV: For SPV to work you need to connect to multiple nodes not just a single one.

G43: I think SPV works even if you only connect to a single node except you have to be more careful which only a power user would know to do. You would have to check whether you have the expected number of blocks and stuff like that. One possible attack vector is that you connect to a single server with one server mode which is not yours. This would be easy to do if everything was exposed in the GUI. Then let’s say the operator of the server is either a miner themselves or collaborates with a miner and they have 10 percent of the hash rate. They could trick you with a transaction that has one or two confirmations and mine actual blocks for that transaction. All the SPV checks would pass and even full node checks might pass. This branch of the chain would be shorter than the best chain but you wouldn’t know about the best chain because you’re only connected to one node.

# Electrum and hardware wallets

SL: Let’s chat about hardware wallet support. That recent [thing](https://blog.trezor.io/details-of-firmware-updates-for-trezor-one-version-1-9-1-and-trezor-model-t-version-2-3-1-1eba8f60f2dd) with the Trezor, I think they locked it down to certain derivation paths. Did that impact you guys?

G43: Do you mean the BIP143, the SegWit signing?

SL: Yes.

G43: It impacted us in the sense that it was another factor to speed up releasing 4.0 to fix that vulnerability. They had to do a breaking change in their internal protocol such that the existing latest version of Electrum back then wouldn’t be able to sign transactions with the Trezor.

SL: In terms of maintaining support with other hardware wallets has that been a challenge for you?

G43: Our current model for hardware support doesn’t really scale I would have to say. In practice hardware wallet manufacturers send a pull request. They write the initial code and we ask to have actual devices sent to us so that we can test it. But it’s only some of the larger manufacturers who help us maintain that code. The smaller ones, after the initial pull request, don’t do anything. That means every time we change something in the code, even a minor refactor, we have to obviously change their plugin as well which is fine. To properly do that we have to test with the actual device because it would be extremely difficult to set up automated tests that would catch everything. We have to test with the actual device. We have to test with 10 devices at this point. We keep getting requests to have more hardware wallets added. We will have to figure something out. I have to say that at least Trezor and BitBox02 they keep sending pull requests to significantly lesser the burden of maintenance for us. They maintain their own plugins. So that’s very nice but not everyone does it.

SL: So other hardware manufacturers pick up your game?

TV: I’m very much looking forward to a unified hardware wallet interface. I think that will be progress but it might not align with the interests of private companies because they want their product to have more features than the competition. So I don’t know if that will ever be a reality.

G43: The Bitcoin Core project, the HWI at this point is kind of similar. I don’t think any further unification would happen because that took away all the incentives. One question is whether we could use HWI for Electrum.

TV: My point is whether hardware wallet manufacturers are going to fully embrace this and comply with this.

G43: I think the whole point of HWI is embracing the reality that that won’t happen. Andrew Chow decided to write an abstraction layer himself. I think realistically the question for us is whether we could use HWI. Last time I looked at it I’m not sure that it would be good for us mainly because first and foremost this is written with the CLI use case in mind.

SL: Does that mean you might have to eventually start rationalizing the supported hardware wallets down to just the big ones that you want to maintain support?

G43: I don’t know.

TV: We might have to do that at some point It depends on the burden that we have maintaining the plugin.

SL: Electrum is well known as one of the ways if an individual wants to set up their own multisignature. It’s got the wizard there. Users can pull together different hardware wallets and put them together. I think previously there were some difficulties doing different hardware wallets together but I think this new version does allow it. If you want to do a Coldcard and a Ledger and a Trezor in a 2-of-3 I think this new version allows for that. What are some of the things users need to think about in terms of backups? What should they be keeping if they want to do that kind of setup?

G43: Even since Electrum 2.8 or something I think multisig with multiple hardware signers was possible already.

TV: But not with Coldcard.

G43: The change in version 4 is that Coldcard because of the intricacies of PSBT it didn’t work well. There was a very involved workaround but Coldcard didn’t work as part of a multisig before. Now it works but even right now it’s not really ideal. I’m not sure a complete newbie could set it up. It works easily if you’re willing to connect the Coldcard via USB to the computer. But if you want to use it cold then it’s still a bit involved because the issue is that xpubs are no longer sufficient to set up a signer. You also need a derivation prefix, the beginning part of the derivation path and also a root fingerprint. The issue is that an xpub is no longer enough to describe fully a co-signer as part of a multisig. This used to be the case in the past. We would need to come up with a new format which could hopefully become standardized to contain this extra information in addition to the xpub. Then it would once again become easy to do all kinds of multisig and in the future maybe even more complex wallets.

TV: There is already the issue of what we’re going to do in the future with script descriptors or Miniscript. It overlaps with the question that Ghost just raised.

# Script descriptors

SL: That’s what I was going to ask whether you were interested to use that script descriptors approach and whether that would save you time or whether that wouldn’t really save you much work there.

G43: We are definitely interested in using output script descriptors not just for this reason. I’m not sure when we will have the time to get to that. Obviously if anyone is interested in working on that then contributions are welcome and we would help in any way we can. Otherwise it might need a year or whatever. Specifically for this issue output script descriptors themselves would still not be enough because they are not high level enough. The most simplistic example is that in almost all HD wallets nowadays maybe apart from Bitcoin Core is you have a simple depth, two or three, where one branch is used for receiving addresses or external addresses. Another branch is used for change addresses or internal addresses. This would not be hardened, it would be public derivation. So like m/0/i is your receiving addresses and m/1/j are your change addresses. To describe your receiving addresses you would need one output script descriptor with a star at the end. To describe your change addresses you would need another. You would need two output script descriptors, not just one, and you would need some kind of additional metadata to signal that you want to use one descriptor for your receiving addresses and the other one for your change addresses. You would need to put all this information into a string or some kind of blob that you can copy paste instead of what we are currently doing with xpub.

SL: There’s a bit more complexity there. Maybe the user has to save some kind of JSON file with all that information in it?

G43: Yeah, exactly. At that point it becomes really hard to back up. I’m even not that comfortable to even copy paste. In terms of backups if you have a multisig wallet ideally you would need multiple backup locations. I’m talking about the scenario where a single user to reduce risk and attack surface sets up a multisig wallet. Contrast that with multiple signers sharing a multisig wallet. A single user could create multiple seeds and distribute the backup locations physically or maybe store one seed online and another offline and another at a friend or whatever. Then require 2 out of those 3. They would need to store all the xpubs potentially at all the locations or at least that’s the easiest way to do it. In the end when you restore if you have to use your backups you will need all your master public keys involved. The corresponding public keys can be derived from the seeds but probably you will have only one or two seeds and you will need the master public keys for the missing seeds as well. With multiple script descriptors tagged whether they are change or not, you would need to store those instead of the xpubs, which becomes more difficult. That’s not something you can print onto paper because you cannot really expect users to be able to tie back some JSON string from paper.

SL: So you might be doing a 2-of-3 multisignature. You might want to keep them in 3 different locations. If you lost one of the keys and the wallet file now you will no longer be able to spend unless you also kept the backup of the xpubs for all 3?

G43: That’s how it always works. That’s how it must work because to be able to reconstruct the onchain Bitcoin script you need all the public keys involved and the different public keys are derived from different master public keys.

SL: It could be done with 2 separate output descriptors, one for your main receiving addresses and another for all your change addresses. So would that mean then you’re keeping two script descriptors?

G43: Yeah. That’s one possible thing we could do.

SL: What you do today is you have to keep the xpub for each key. I guess it also helps if you keep the derivation path for each one.

G43: It depends on what kind of key stores, what kind of individual signers the multisig is comprised of. If you’re using Electrum seeds, the kind of seeds that Electrum the application would generate and give you then all the derivation path and script type logic is abstracted away from the user. It’s encoded into the seed itself. The user doesn’t have to know about it.

SL: So it’s more if they’re using the traditional BIP39 or a hardware wallet then they need to just be mindful of that.

TV: Maybe we will come up with a very simple mapping between Miniscript or script descriptors and integers. If we can do that then we could have a seed type that includes the script descriptor in the seed.

SL: Are there any other things that could be done to make multisignature standardized across different hardware wallets or different wallets?

G43: I think there are two large points here. One is how you would back up and restore from the backup for your wallet. The other is how you would sign transactions and transfer unsigned and partial transactions between your different locations. I think the second point has been by now almost completely solved by the PSBT approach BIP174.

# BIP 39 seeds vs Electrum seeds

SL: The PSBT approach seems to be supported by many different wallet software and hardware. That’s the spending part. I guess it’s just the backups part where there needs to be some sort of standard that people kind of form up on. Thomas, I know we spoke about this on the earlier episode, currently many hardware wallets are using BIP39 style mnemonic seeds and Electrum has its own seed style. For some users that could be confusing. They are often taught they only need the first four letters of each word to be able to recover that wallet. It can be confusing if there’s multiple word sets. I’m wondering whether your thoughts have changed on that, the comparison of the different seed types and whether you would go to a BIP39 style seed.

TV: We would need to get rid of our old word list if we wanted to have this four letters disambiguation. I don’t know if we can do that yet. Maybe we could disable it by default but some users would be confused. The big problem we have is that when BIP39 was published it was a standard that collided with existing Electrum seeds. Because both use English words they have words in common. The old Electrum seeds could be in some cases valid BIP39 seeds.

G43: You’re talking about word lists but the word list is just one small part of a seed scheme. Regarding the word list there are currently two English Electrum word lists. The one we used at the very beginning which is used by so called old type seeds for Electrum. Since version 2 when the current seed scheme was introduced for Electrum, these modern seeds have been using the same word list as the BIP39 English word list. The current scheme is independent completely of the word list. Technically to decode a seed you don’t even need the word list. The word list is simply used to generate seeds that contain English words but the current Electrum scheme for the seeds is completely independent of any language or words, it just uses Unicode characters.

SL: The word list is distinct from the actual way by which you turn…

TV: The idea was to not include the word list in the standard and to be able to change it freely later or to localize. That was my initial ambition. The big problem we have now is that on Android and also on desktop users want to have completion. It is much easier if the word list is fixed because you can have a smart keyboard that detects the beginning of the word.

G43: This is in contrast to what BIP39 has with several word lists. If you only consider the English word list it is part of the BIP39 standard. You couldn’t just change the word list because then the checksums would not work out. The word list for BIP39 is set in stone. You cannot change it. In the case of ours if we wanted to we could change it at any moment.

SL: If enough new people are coming in and they’ve already got a BIP39 seed then they’re getting confused about trying to recover that into Electrum.

G43: I think that’s a separate question but we can talk about that too.

TV: I think BIP39 is dangerous because non-technical users will only write down their seed words and nothing else. Or they might even give this information to someone else who does not know which client they were using. The problem is that since there is no version number in BIP39 the software is supposed to be smart and know about the derivation for your private keys. Of course it cannot work that way because new derivations are added over the years all the time. You cannot expect software to work like that unless you are willing to accept losing users’ Bitcoin. The whole point of this English word presentation is to make it simple for users who do not want a technical description. If users are willing to have a technical description then why would they use these seed words? You could just write a string of hexadecimal and that would work just as well. The whole point of those words is to have something simple, something you can write down without a computer, just with pen and paper, and you can restore later. The restoration process should be unambiguous. It should not require more technical information such as the deviation path or the type of software that you were using and how many derivation chains you are using in your wallet. It is ridiculous to expect users to know that.

SL: There’s definitely some valid concerns there on both sides. On the question of re-scanning I saw Luke Childs made a contribution around rescanning all the common, well known derivation paths. Could you tell us a little bit about that?

TV: This is something we are going to merge. We haven’t had time yet because we’ve been really focused on the release. I didn’t want to touch BIP39 myself because I think it’s a neverending thing for the very reason that BIP39 works with BIP43 and BIP43 is really the issue. It says that the number of potential derivations is unbounded. It can go indefinitely in the future. So you need to perpetually maintain code that will explore the different derivations that have been used by different software wallets or hardware wallets. So with these pull requests the goal is to precisely do that. To have a comprehensive exploration of the derivation path. I don’t know how it’s going to be maintained in the future but I’m open to merging it because it will make life easier for some users.

G43: This is only needed because of how BIP39 is constructed because the user might not have their derivation paths written down. It is not even the derivation path anymore, it is also the script type. In the future it might be other things. Nowadays most wallets use this very simple two depth structure of one HD branch for receiving addresses and another for change. This is also implicit. So with BIP39 everything is implicit and the user would write all this down as part of their backup. In the future you could conceive that not only do you need to brute force the derivation path and script types but also different branches of wallets.

TV: Gap limit.

G43: Gap limit too.

SL: A user might be in a situation where they’ve got their 12 words or 24 words but they still don’t know exactly how to access their coins. It is like searching for a needle in a haystack because there’s all these different possible combinations of what that wallet might’ve been set up to use. That makes it very difficult trying to recover into Electrum wallet for example.

# ElectrumX

SL: We should chat about Electrum servers. So as I understand the ElectrumX guy went all BSV. Now the Electrum team is maintaining ElectrumX?

TV: This developer kyuupichan was maintaining [ElectrumX](https://github.com/kyuupichan/electrumx) for a bunch of different coins actually. But he’s a Bitcoin Cash and then Bitcoin SV guy. Now for some reason he has decided to drop support for anything else but Bitcoin SV which he calls the real Bitcoin. So we had to take over and of course we are familiar with the code because we’ve been co-developing this. Every time we had to do a change in the protocol we had to add it to ElectrumX. It’s not a problem for us to maintain this code but it was convenient to have him maintain it because he’s the author of that code. I am not the author of ElectrumX. I designed the initial Electrum server which is a different codebase and which was slower. Now we are going to maintain the server code for that reason. In the future we might also add new things to the protocol. I’m very excited about [utreexo](https://dci.mit.edu/utreexo) I don’t know if you have heard about that. This is something I have a branch on that repo that that is a preliminary implementation of utreexo. If we want to do these kind of things, of course we need to change the protocol all the time.

G43: It was great to have kyuupichan maintain and even write ElectrumX in the first place because hats off to him he did write really good code and it’s really maintainable. There are small bugs here or there but that’s true for any codebase, nothing can last forever. Now kyuupichan decided that he wants to support Satoshi’s vision so we will have to maintain our own [fork](https://github.com/spesmilo/electrumx).

SL: As I understand a lot of the packaged nodes, they typically run with the [Electrum Rust server](https://github.com/romanz/electrs). Whereas I think the people who want to be more efficient across lots of wallets, they tend to use ElectrumX. There was a recent [post](https://blog.keys.casa/electrum-server-performance-report/) by Jameson (Lopp) and the Casa team talking about benchmarking and the different Electrum servers. They found ElectrumX worked best for them.

G43: Yeah I saw that blog post too. It was nice. If you want to run a public facing Electrum server serving the public, serving many wallets, then I still recommend you should run ElectrumX, you should run our own fork now. If you just want to set up an Electrum server for yourself and you don’t want to expose it publicly then you have a whole bunch of options. It works for that too but you can also run the Electrum Rust implementation or [Electrum Personal Server](https://github.com/chris-belcher/electrum-personal-server) by Chris Belcher or there’s another implementation now that’s very lightweight similar to EPS by Nadav Ivgi (shesek).

SL: [BWT](https://github.com/shesek/bwt). Bitcoin Wallet Tracker.

TV: One thing about Electrum Personal Server, last time I checked, you cannot use it with Lightning because Lightning requires your Electrum server to be able to watch arbitrary addresses.

G43: There’s that complication. If you run Electrum Rust server or ElectrumX then you should be perfectly fine.

SL: You mentioned utreexo by Tadge Dryja. That might be an interesting idea for people to be able to more easily run something in between. As I understand the idea is that you could have people running a full node on a mobile phone because it would compress the blockchain.

G43: I think he called it a compact node.

TV: It has what is called a compact node. I would not call it a full node but there are different reasons why I’ve been looking at utreexo. We are experimenting so it’s not clear yet whether we will make it part of the Electrum protocol or not. That’s really an ongoing experiment.

SL: So is there anything else that you guys wanted to touch on in terms of things you’ve got coming up with Electrum that should users be looking out for?

G43: I think at the moment we are focused on bug fixes.

TV: We’ve been adding a lot of new features and now is the time for fixing bugs, consolidating code and also improving the GUI because we get feedback on the user experience. When you add a new feature the first iteration of the GUI that you make for that feature is obviously not the best. You learn also from the user feedback.

G43: For example I’ve seen on the subreddit for Electrum that it’s been a recurring question since version 4 that the Receive tab changed and users can’t find their receiving address. Previously you were given a Bitcoin address right away, it was shown by default and now you actually have to press a button to generate a new one. It was an attempt to unify the onchain and the Lightning experience but also to reduce address reuse such that you would have to manually create an invoice and be given an address to use for a new payment. These kinds of things will have to be made easier to use but there’s a lot of things to be done. For example I think we need more tests, unit tests and functional tests for the Lightning parts. We already have quite a few but we would still need more to sleep better at night. There are new features to implement in the medium term too. For example I would like to look into Payjoin but I’m not sure when I will get to that.

TV: There will also be a changes to the Lightning protocol itself.

G43: Of course we have to keep up with them.

TV: Maybe at some point we will also want to have Taproot.

SL: If any listener is interested to contribute where would contributions be most needed?

G43: First of all if you want to contribute you should come to the IRC channel on Freenode \#Electrum. The [repository](https://github.com/spesmilo/electrum) on GitHub is a good place to start. Look at some open issues and pull requests and maybe also look at recent commits to see what we are working on. First of all I think you should ask on IRC, you should say if you have some time and what you might be interested to work on and we would probably be able to help you or to give you ideas.

TV: I’m very happy with the approach where people propose a pull request for an issue that has been annoying them. That’s the best capital allocation in terms of programming time. People usually start contributing because they see an issue that we do not see. That’s very important. I think that’s also how you started to work on Electrum. Ghost, you were fixing an issue that was annoying you. Most of the time we receive a pull request, it is something that is not so important for us but it is important for someone so they propose to fix it. That’s very good because it increases the number of viewpoints on the software.

G43: Even if someone wanted to implement a completely new feature they can go for it. I just mentioned Payjoin, if someone said that they were interested in implementing Payjoin for Electrum then great. We would give all the help and could discuss the possible approaches and what modifications would be needed for the code. They would maybe not do the whole thing but some prototype that sort of works.

TV: We talked about Payjoin earlier because it seems kind of easy to do now.

SL: Thinking about Bitcoin more broadly, do you have any thoughts on what’s going to happen over the next year or two? Are there any things that you’re really interested to see in the protocol and any other developments in and around Bitcoin and Lightning?

G43: I hope the Taproot soft fork happens. I don’t know, realistically like a year or two. I hope that the Lightning Network with the BOLTs can start using Schnorr signatures and Tapscripts for some of the onchain scripts. Replacing the hash preimages with point multiplication and stuff like that. That’s very exciting and I think it could realistically happen but the prerequisite is having Taproot.

TV: I would really like to have a much better way to find a path in the Lightning Network. Currently we need to have the whole database locally. There is this [Trampoline routing](https://diyhpl.us/wiki/transcripts/lightning-conference/2019/2019-10-20-bastien-teinturier-trampoline-routing/) proposal. I don’t know if someone will come up with an even better solution. It seems to be the best solution that has been proposed. I hope that something will emerge or the Trampoline routing solution will be adopted because if you don’t have to run the Lightning database locally with the gossiping it makes your client much lighter.

G43: In terms of user experience after we fix some GUI issues when you use Electrum with Lightning, I think the main issue would be all this path finding and gossip stuff. If you use Electrum it’s intended to be used as a light client that you just fire up when you need it for a few minutes or whatever. It is really problematic to sync up all the Lightning gossip. Without that path finding doesn’t really work that well and you have a lot of failed payment attempts. The whole thing cascades because this is one of the main reasons watchtowers don’t really scale at the moment. You have to make like 20 payment attempts to have a somewhat larger payment succeed or maybe even more. That needs 20 times the storage so everything is related.

SL: I know some of the discussion there was quite heated amongst some of the Lightning developers. I think the concern for some of them was that it would be a privacy concern because not enough people would run the Trampoline node and too many people trying to be use the Trampoline routing. That’s more of a technical debate that we don’t need to wade into.

G43: The main point is not that we want to use Trampoline. It’s just the most mature solution which doesn’t completely give up your privacy in terms of better path finding and routing. We would be content with any other competing solution if there was one.

TV: Maybe there will be one we don’t know yet. At the moment Trampoline is the most reasonable solution in town but maybe someone will find something even better.

SL: Do you have any closing thoughts for the listeners?

TV: Thank you for giving us this opportunity to talk about Electrum. We really want to make Bitcoin easy. That’s always been the motivation behind Electrum to increase both security, privacy and ease of use. So use Electrum and do share feedback with us. That’s the best thing you can do to help. If you’re a programmer please do help us fix bugs, propose pull requests.

G43: If you’re already a user of Electrum or if you are a programmer then please report bugs and have a look at existing bugs, look at the code. If you have a bit of free time, maybe submit a pull requests, that’s how open source works. That would be nice.

SL: Listeners go and find electrum.org. Follow them \@ElectrumWallet on Twitter. Obviously it is \#Electrum on Freenode. Thank you guys for joining me on the show today.

TV: Thank you.

G43: Thanks for having us Stephan.


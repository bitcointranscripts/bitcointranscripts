---
title: What Am I Working On 
transcript_by: Michael Folkson
speakers: ['Andrew Chow']
tags: ['wallet']
date: 2020-07-10
---

Topic: What am I working on?

Location: Reddit (r/bitcoin)

Reddit link: https://www.reddit.com/r/Bitcoin/comments/ho0t1a/what_are_bitcoin_developers_currently_working_on/fxhwqli/?context=3

# What am I working on?

I've been working on essentially rewriting the Bitcoin Core wallet, one piece at a time. Now when I say "the wallet", a lot of people think of the GUI. That's not what I've been working on. Rather I've been changing the internals; how keys are managed, how transactions are tracked, how inputs are selected for spending. All of those under the hood things. At some point, I will get around to changing the GUI. And in general, my focus has been on improving the user experience. Cross wallet compatibility is also something I've been working on.

One of the big things I've been working on recently is descriptor wallets. What Core does right now is treat the wallet as a bag of keys. It turns these keys into scripts and addresses. But fundamentally, everything is centered around "do we have the keys to spend this script". Descriptor wallets change this. Instead, everything is centered around the script, which a descriptor describes. This makes more sense than keys as Bitcoin transactions are really script based, not key based. The keys are still there, they are just attached to a specific script as auxiliary data. By using descriptors (which map one-to-one to a script), we have an engineer readable way to write a script so they will be easier to import to other wallets. And descriptors leads us into Miniscript which will give us the ability to have and reason about complex contracts.

Descriptor wallets also greatly simplifies a lot of internal logic, so there will be far fewer corner cases and bugs. Notably, because they are script based, we no longer determine whether a transaction belongs to a wallet by checking whether we have any key that can spend the output. Instead we just check whether the scriptPubKey matches any of the scriptPubKeys we are watching for. This also makes watchonly behavior much simpler and actually sane.

Descriptor wallets have since been merged into Bitcoin Core as an experimental feature for 0.21. Hopefully it will become the default wallet type soon and we'll have a way to migrate legacy wallets to descriptor wallets. I'm actually going to be streaming the entire process of writing the migration code on my [twitch channel](https://www.twitch.tv/achow101/).

My current big project is changing how the wallet is stored. Namely, instead of using a super old version of Berkeley DB, I'm migrating us to using SQLite. We consistently, though not frequently nor regularly, get reports of wallet corruption. This usually means data loss and the loss of private keys. And that is not good. I attribute a lot of the issues we have with our unusual use of BDB; we're essentially using the database in a way that it really wasn't designed for. The gist of it is that we want all the wallet data to end up in the wallet.dat file, and consistently. But BDB wasn't designed to always have everything in a single file, and for everything to end up in that file when it considers the data to be written to disk. So we have a bunch of hacks to force it to do that.

So BDB isn't really good for our use case. It just so happens that SQLite is. It actually is designed for use as an application file format and can be configured to ensure that the data is written to the database file. So I've been refactoring the database handling code to let us integrate SQLite and use that for wallet storage. There are several PRs still open and in review to do all of this. The goal is to have this for 0.21 as the default type for descriptor wallets. Then I'll see about adding the migration of legacy wallets to use SQLite as well.

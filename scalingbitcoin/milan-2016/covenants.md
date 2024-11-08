---
title: 'Bitcoin Covenants: Opportunities and Challenges'
transcript_by: Bryan Bishop
tags:
  - vaults
  - covenants
speakers:
  - Emin Gun Sirer
date: 2016-10-09
media: https://www.youtube.com/watch?v=_Z0ID-0DOnc&t=10241s
---
<https://twitter.com/kanzure/status/785071789705728000>

We published this last February at an academic workshop. The work itself has interesting ramifications. My real goal here is to start a conversation and then do a follow-up blog post where we collate feedback from the community. We would like to add this to Bitcoin Core. Covenants.

This all started from a very basic and simple observation about the current status of our computing infrastructure. The observation is that the state of our computing infrastructure is no where near safe enough to store assets like bitcoin. The default low energy state of an exchange is that it's empty. We have seen this with MtGox, we've seen it with Bitfinex, etc. Some of them are insider attacks, sure. Insiders are able to get away with it because their attacks are indistinguishable from other attacks. Teamspeak users get hacked since forever.

"Sorry for your loss" has become an acronym on bitcoin forums. Bitcoin has become a universal bug bounty. It used to be that vendors would fight with you and eventually htey would cave in. You don't have to do that. In the first bitcoin workshop, there was a fantastic paper from two people and they did this incredibly cool study where they looked at the reuse of Q values in signatures. The private keys were immediately exposed. The person giving the talk said they found 318 cases where they could immediately recover the private key. He got all the money from those accounts--- but he recovered $0 because someone else had done their own work and were sweeping the blockchain on their own.

So what's our response to this? Well we all work on bitcoin, we care, but it's someone else's business to secure this? Mobile OSes are not updated frequently enough. If you are using django or ruby-on-rails, the infrastructure you trust is just huge. We're not going to be able to fi all of this. We need to provide in-protocol mechanisms to secure our coins.

We started to think about a vault abstraction. What's a vault? It's a secure place to hold your coins that you are not using immediately. A vault enables you to recover your bitcoin if they are hacked. You can revert a transaction that a hacker makes to steal your coins. It's structured in such a way that you can't take back a legitimate transaction you make to a merchant. I want to describe why this is not contradictory and why the solution is elegant and why it almost eliminates incentives attacks against coin holders.

A vault has two keys. An unvaulting key and a recovery key. You place coins into the vault. At that time, you specify the unvaulting interval. Someone like me would say 24 hours. If you were a daytrader you would say 8 hours while you sleep or whatever it is you do. This is the downtime, the time during which you don't want your coins to move. If you want to move htem, you use your unvaulting key and move them from your address. You can't pay directly from a vault. A vault is only for your personal use only. You can't pay a merchant with a vault payment. If osmeone hacks your key and steals your keys, then you use your recovery key to take your coins back. This is an incredibly useful feature.

Given this audience, they are thinking about the security problems. What happens if you lose both keys? Suppose you didn't bury the second key deep enough. If the hacker gets both keys, then you burn the coins. If the hacker hacks the vault, then the expected gain should be zero coins. This is a powerful primitive. There is absolutely no incentive to go after vaults.

# Vault implementation

We could have a new address, a special prefix, a special casing, a whole lot of complexities could be added to Bitcoin Core to support this. I would like to present a new abstraction to allow this and also allow a few other use cases. I am here to tell you about this new abstraction so that you can think about other applications. Please let us know if you do use this.

You guys are familiar with traditional payments where Alice pays Bob and that transaction is of course a script. In covenants, there is additional code that restricts the next spend transaction. This covenant is a restriction on the transaction that follows. The way this is implemented is a single opcode, using OP\_CHECKSEQUENCEVERIFY. A cline is a self-generating program. You have seen this in obfuscated C contests perhaps. You can build them with a simple opcode. Covenants can be recursively enforced down the chain for as long as you need to reinforce them. OP\_CHECKOUTPUTVERIFY adds a limited form of reflection. Bitcoin script used to be limited in the data to the ouput and input scripts. We want to add OP\_CHECKOUTPUTVERIFY and check the abstract syntax tree. It's incredibly limited in scope, simple to implement, and it's an actual opcode that the ethereum folks don't have, it would give us a lot of flexibility in how to use it.

# Covenants for vaults

If you use the unvaulting key, then you use a checksequenceverify to check if the transaction with a relative locktime of 100 blocks during that time someone can revert it, or during that time there's a recovery key to tak that back with a new covenant on that.

Covenants are not just useful for vaults. There are some bonuses. There are some other use cases. An incredibly popular use case for covenants, on many people's mind, is colored coins. There was a period of time where about 2 years ago I was getting multiple calls per week where someone would ask me to sign an NDA and then they would tell me an idea about colored coins. They wanted to put gold on the blockchain. "How did you know?" It's just what people want to do. If you have some asset kept in a vault or an actual vault somewhere, where you want to collate and combine those items that can combine. If you have a sliver of gold and you have another sliver of gold, then you should be able to combine them, but you don't want to pay for coffee with that.... I feel like lord of the flies up here.

You can use this in satoshis, there's no gaurantee that the satoshi being used to represent your halves will fall below the dust limit, and that would be bad. We need to distinguish coins from actual coins. We can do that with covenants. The covenant can make sure these assets do not mix with others.

Another feature is fraud proofs. You have seen sidechains. But I have never seen a trustless reverse peg in operation. The big limitation of trustless reverse peg is that you need some way of proving a fraudulent sidechain transaction. This is trivial to implement with covenants. People who have tried to implement sidechain pegs know the difficulty of getting this to work on bitcoin without this.

# Covenants concerns

There are a number of concerns people have here. People were trying to fight about block size reparameterization, and this other stuff fell off the map. This is a lot of work to bring bitcoin to the next level. I have heard some concerns.

The actual complexity of covenants is only 200 lines of code, so adding a new opcode is therefore not complex.

Covenants can be used to break fungibility. But so can many other things in bitcoin, so it doesn't matter. Wallets could limit covenants. At the end of the day, fungibility today is already not protected by protocol mechanisms. It's protected by social consensus that we must have fungibility. For covenants to break that contract, they would need to be adopted by people using covenants. I am very secure in the knowledge that this community will not adopt coins that restrict fungibility. So I remain steadfast in covenants having no effect on fungibility.

Overhead is an issue. The execution time of this overhead is proportional of the size of the pattern to check. This is reflected in the transaction itslef. The number of bytes is proportional to complexity.

I am sure there are other concerns. I'd love to hear about them.

# Early deployment

Elements Alpha implemented covenants and deployed it just two days ago. At least this is operational on a sidechain. Russel O'Connor is going to be releasing some blog posts. I think this is a good time to be thinking about this.

# Summary

OP\_CHECKOUTPUTVERIFY will make thefts a thing of the past. It will take away the incentive to think that you can get away with a big heist. Your daily hot wallets might be at risk, but the actual stuff that we keep in cold storage in all sorts of protocols-- that would remain revertible back to us and that's a good feature. It also opens up new use cases. I would love to hear from the community about their concerns and feedback.

# Q&A

Q: Your description of color coins is wrong. You don't allocate satoshis to assets. You have your transaction commit to a distribution layer above it.

A: Didn't realize that.

Q: Right, just obsolete. So I don't think you need covenants for the first application. You could use nlocktime.

A: There are multiple ways of implementing vaults?

Q: Transactions work fine until the covenant period is over. So you might as well sign the nlocktime and show the transaction goes forward.

A: I would like to see an example of your counterexample.

Q: Sure.

A: I would appreciate that.

Q: Hacker... two keys here. Can your hacker show your coins...?

A: Always a problem. This is not a universal solution for all ills. It just makes it a little better.

Q: What is the period to destroy the coins?

A: You set that. You can set that to be multiple months or as short as you want. It's entirely up to you.

Q: In the case of destroying coins, is it also possible to make it so that it's spending to fee, so that the hacker can collude with a miner to mine that?

A: The way we have it right now... and there are other ways to implement this, we are simply keeping the miner from spending it. We keep the hacker from spending it. You could imagine it doing it the way you mention. The hacker would have to join forces with miners; I think the miners wouldn't go with that.

Q: My concern about covenants on fungibility is that it gets in the way of future improvements like one-way aggregate signatures or mimblewimble where you do non-interactive coinjoin. But if you have covenants you can tell the inputs and outputs are linked because the person who authored it cared about the content.

A: True, but you need ... covenants attached for coinjoin.

Q: Right, but you wouldn't be gaining from non-interactive coinjoin. So would you be able to mask which outputs are being linked?

A: In the case of coinjoin with covenants, I just imagine it's, the two things don't mix. They are at odds with each other. One is trying to hide the origin of coins and the other is tracking. So unless all of the coins into the coinjoin have the same covenant, then the outputs shouldn't have any covenants as well; that's a way to make sure everything is uniform you're not adding or subtracting.

Q: Can you compare this to multisig security? If the hacker gets both keys, they can steal this.

A: You burn the coins if they get both keys.

Q: What happens if someone spends a coin before you can revoke or destroy them?

A: They cannot spend during the duration of the unvaulting period. You specify this period.

Q: Related to the coinjoin topic, would merklized abstract syntax trees... help with that if you reveal the path with the covenant? The script would actually be... and you reveal the path you spend. So maybe it's fine to do coinjoins if you don't get the money stolen?

A: I didn't understand the question.

Q: Are you familiar with merklized abstract syntax trees? MAST.

A: No.

Q: Okay well we can discuss later.

A: Okay thank you.

Q: Can you use the opcode to make script payments?

A: What?

Q: like 50% from one to another?

A: I don't follow the use case. It's programmatic restriction on what payments can go to which outputs. That's the use case.

Q: Do miners introduce denial of service blow-up?

A: It's a concern. Your wallet will always know the covenant. If you don't understand it or agree with it, you don't accept those coins.

paper <http://fc16.ifca.ai/bitcoin/papers/MES16.pdf>

coin covenants <https://bitcointalk.org/index.php?topic=278122.0>

<https://en.bitcoin.it/wiki/User:Gmaxwell/covenant_busting>

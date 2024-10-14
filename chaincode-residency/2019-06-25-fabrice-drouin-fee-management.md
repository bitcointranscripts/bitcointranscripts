---
title: Fee Management (Lightning Network)
transcript_by: Keyan Kousha, Shiv Patel, Nelson Galdeman
tags:
  - lightning
  - fee-management
speakers:
  - Fabrice Drouin
media: https://youtu.be/r8S3iELg9_U
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-fabrice-drouin-fee-management/
---
Location: Chaincode Labs Lightning Residency 2019

Fabrice: So I'm going to talk about fee management in Lightning which has been surprisingly one of the biggest operational issues we had when we launched the Lightning Network. So again the idea of Lightning is you have transactions that are not published but publishable, and in our case the problem is what does exactly publishable mean. So it means the UTXO that you’re spending is still spendable. It means that the transaction is fully signed but it also means that the fees that you attach to the transactions are realistic - you're not overpaying fees but you're not underpaying fees otherwise it could take a long time to confirm it. This has been a source of issues on lightning almost from the beginning. Okay so you can say this on fee management in lightning: is that funder, the one who opens a channel, pays on chain fees and to adjust the fee rates because obviously if you leave your channel open for a long time the on chain fee rate will change. So what you're supposed to do is you're supposed to monitor the on chain fees and adjust what you want to apply by sending to your peer and update fee message which says ok this is what I would want to apply for on chain fees for the commitment transaction and the fundee can refuse an update fee message and close the channel. So do you know why the fundee would care about onchain fees? Do you have any idea why it would matter also on the fundee’s side to avoid having fees that are not realistic?

Audience: [inaudible]

Fabrice: Again the funder pays on chain fees so why does it matter for the fundee to have fees realistic. Look at, look again at this, this is what a commitment transaction in lightning looks like. You have typically one output for this, this is Alice's payment transaction, so there's one output for her that sends her money after a delay and that is spendable by Bob if you know its revocation key. Its remote output just sends money to Bob and you have one output for each incoming or outgoing HTLC, okay? And for each of these pending payments you have a second stage transaction, timeout transaction for offered HTLCs, and successful transaction for received HTLCs and these transactions they must pay fees too, okay? And the funder pays fees but if I'm Bob and if I have an HTLC that is offered by Alice I like to make sure that funding, that commitment transaction can be published quickly enough. I don't want to wait to have money locked up on chain for too long.

I don't want to have fees so high that my HTLC is not spendable so a fundee even though it's not as important for the fundee as for the fundee is also concerned about onchain fees. This is why the fundee can refuse a fee that they think is not realistic. This has been the most common source of channels getting closed on lightning for a long time. Like, during the first month, basically I would say half of the channels getting closed, problems we saw, were caused by fee mismatch. All implementations have a different name for the error you see but basically you would see a huge spike in fees, or you would see a huge change in fees, you would send an update fee message and your channel will get closed because on the other side the fee estimators are not seeing a spike yet.

Audience: why would they close the channel instead of renegotiating the fee?

Fabrice: how are you going to renegotiate the fee?

Audience: [inaudible]

Fabrice: It's really harsh but basically if you don't like the update fee you see you close the channel and it's been a source of huge problems at the beginning and what happened is implementations all became very lax. So basically now all implementations will accept almost any fee change which is not too good because I think fees that are too high or too low will have an impact on the UX of lightning. If your, if your closing transaction takes days to be confirmed it's a problem. If you're overpaying fees a lot it's also a problem so it's not too nice, and it's not a problem that can be solved because predicting a good fee rate is strictly impossible. It's like predicting the future. So you can look at the mempool, you can look at whatever you want. I think a good fee prediction algorithm doesn't make sense and some people say okay but maybe by looking at the mempool I could figure out something really clever and it won't work. And do you know why it wouldn't work?

It's a common problem when you have trading algorithms. I don't know if you've seen research papers on “smart trading algorithms” but people always look at historical data and say okay if I were to apply a really smart strategy look at what I could have won using historical data but this is really flawed. Do you know why it's flawed? Yes it works very well when you look at historical data and say ok I'm the only one that knows, that implements these specific algorithms so if I apply this to data, the past data, I'm gonna win. But if everybody is using the same algorithm then gains are canceled out and when you see, its something I learned by talking to someone who did research on algorithmic trading, most research papers will never do that thing, will never say ok what happens if everyone is using my robots. Nobody does that because then nobody wins anything and it's the same with fee estimators. If everyone has a really really smart fee estimator it's not gonna work. For it to work it means you're the only one that can actually use your fee estimator and this just doesn't happen.
Fabrice: So predicting the good fee rate is a red herring, It's not gonna work, so we need something else. So now we have a problem and since you all become experts by now, you should be able to figure out the solution. Yeah this sign commitments transactions, you have signed commitment transactions. You like the fees, the fees are too low but how do you increase fees without getting the other party to sign that transaction again ok that's one one one answer is Child Pays For Parent (CPFP). Do you all know what CPFP means ok? CPFP doesn't work, why doesn’t it

Audience: [inaudible]

Fabrice: yes, who said it's locked? Okay that's because it's locked so it's the first thing that comes to mind and I've made the same mistake. I don't know how many times Christian always told me oh you can't use CPFP I guess you told me maybe 20 times because of the lock time. So CPFP doesn't work, because you have a locktime so you can't spend that transaction until it's been... and it doesn't work so what are the other options, CPFP is out what's left?

Audience: [inaudible]

Fabrice: Yeah okay okay but… [big pause] I want to [missing word] this but I can't spend this before a delay, the delay starts when the transaction is actually confirmed. Okay, so how do you... I... I don't have enough fees to get my transaction to confirm

Audience: [inaudible]

Fabrice: Yeah... there...

Audience: [inaudible]

Fabrice: That's something we consider for yes, yeah so yes one of the proposals was to add an opt-to outputs say okay we're going to burn fees in this.

Audience: Can you use eltoo?

Fabrice: yes, eltoo is actually the best solution for this because the fee management is removed from lightning with eltoo. It's not a silver bullet because... well it's the wallets that will have to handle fee management so the complexity of on lightning goes away but complexity on the wallet side becomes a bit worse. But, basically one of the things you can do is have it for some other transactions use a different sighash flag, so you all know the sighash flags sighash_all sighash_anyonecanpay sighash_single.

Audience: [inaudible]

Fabrice: Soon, very soon sighash [inaudible]. Sighash_all is actually a bit of a problem but, is there something else you can do? Especially for all these transactions have one input and one output

Audience: [inaudible]

Fabrice: yes, do you all know what sighash_anyonecanpay is? Who doesn't know? Okay, so sighash_anyonecanpay means you're signing, you’re only signing your inputs and you're not signing... you can add inputs to your signed commitment transaction and you don't invalidate selectors you have.

Audience: But you sign the outputs, so it’s a fixed amount of …

Fabrice: So what can you use in combination with sighash_anyonecanpay? You use sighash_single, so if you use a single to sign your HTLC timeout and success transaction you can add inputs and outputs and the signatures you got from your peer are still valid. So, in that case you can bring your own fees to the second stage commitment transaction and the fundee cares about the fee rates problem goes away. So that's something that has been proposed, the first proposal was... new commitments structure or something I don't remember the full name but … commitment v2 maybe. So it was it was a bit complex because it changed a lot of things and it was not accepted but changing the sighash flag on the second stage transaction is very easy to do it is something that we will probably add in lighting very soon

Audience: [inaudible]

Fabrice: no but it does solve the fact that the funder, that the fundee sorry will close the channel because he's not happy with the fees. The big problem we have is that if there's a fee mismatch today on lightning channels get closed so it's something you see very often on Github or Reddit like block X closed 200 channels because the fees that were used in the new incoming block were much higher than the ones you estimate it and so it changes your estimation a lot and it gets you to a few standard dates or it gets you to create a new channel bit and send it and your and the other guys hasn't seen that block yet and will refuse your a bit or is using a different fee estimation strategy that is just too far off. This is the problem that will be solved because it still happens. I think everyone except c-lightning now will accept almost anything, c-lightning still does refuse either are very different from what they have I think

Audience: [inaudible]

Fabrice: it's much much less common. It is not a huge operational issue now but it is sometimes. This is what will fix it.

Audience: [inaudible]

Fabrice: no, basically what it means is you don't have to worry about fees for the second stage transaction you can just bring your own fees you can just add inputs and outputs. This is something that will be used everywhere with eltoo, in eltoo basically there are no fees in in like instructions, you have to supply own inputs and outputs

Audience: [inaudible]

Fabrice: no you still have you still need a fee high enough to at least have a chance of getting your commitment transactions to confirm, this doesn't go away without eltoo. Unless we add that opt-to output or something.

Audience: [inaudible]

Fabrice: This is another problem with fees in lightening its how do you manage on-chain funds. So basically lightning what it is, is a non-chain wallet and an on-chain wallet and there are many options you can choose from to implement the on-chain wallet paths and all implementations have made different choices. You can call in two standalone separate wallets or you can implement your own wallets.

And if you do choose to implement your own wallets there are things that are very specific to lightning UTXOs. You may choose to deal with them within the channels or in your on-chain wallet. So if you decide to use an external wallet, that's what we do on the server version of Eclair, we use your Bitcoin node as a wallet and we use RPC calls into your Bitcoin node wallet. This is the laziest and easiest solution. You really don't have anything to do. It's up to you to backup your own lightning wallets. Backup and restore is like standard but you get to use more on chain transactions. So when a channel gets closed, what we do on Eclair is we will just wait until this is spendable, spend it, and return it to your wallet. So you have one closing transaction and one transaction that returns funds to your wallet. So it's an extra transaction which means when fees are really really high you pay extra fees.

If you choose to implement dealing with lightning UTXOs at the wallet level you have other problems. So when I say that things that are specific about lightning UTXOs - those specific things are typically the key derivation that is not BIP 32 or something, it's something that is really specific to lightning and the timeouts. So basically this: I'm Alice, this is mine, this is not something that you can easily guess or that you can derive using BIP 32. This is a key that uses key derivation scheme that is specific to lightning and it has a delay so it can't be used straight away so either I wait until it is spendable and return it to my wallet or I need to add rules in my own chain wallet and say okay this you UTXO has a time lock and I think LND calls it a nursery so you have baby UTXOs that are too young to be spent and when they grow up they become spendable but you need to keep track of this and it's actually more difficult so it's more efficient when it comes to fees but it it makes it harder to use and harder to backup and restore because you can't have static backups of your on-chain wallet. You need to add your UTXOs dynamically otherwise you may not recover all your funds. So it's much better from a fee point of view but it's something we decided not to implement for now because it makes backup and restoring, the on-chain parts of your wallet a bit more difficult.

Audience: [inaudible]

So honestly I was not aware of that. That’s something I will look into. I don't see how it works but okay so maybe bitcoin core will be able to understand some of these lightning specific rules but basically you have two options you return money to your wallet as soon as you can but you pay fees and when fees are really really high and we've seen two hundred sats per byte few months ago then it's really a problem or you keep your lightning UTXOs in your wallet but then you have to remember how old they are you have to add them to your backups and it's a bit more complex so there is no perfect solution yet. This part is not gonna get better with eltoo because the wallet will have to manage the extra inputs and outputs you want to add or fees so if you don't have UTXOs then you have a problem and on chain management is not going to get much much simpler but lightning will be much simpler. So eltoo is really something I look forward to.

Audience: [inaudible]

Okay if I'm fundee and if I have first of all I may want a commitment transaction to be confirmed quickly because I don't want to have to wait days or weeks before it's suspended as well for me. Also ... I think that's the only reason actually. I can't see why you would need to care about the HTLC second stage (?) transactions now so I think the only problem is you want to be able to have the output that is for you usable as soon as you can and there is no way for you to bump its fees. So unless we add these opt to (?) outputs, that is a bit hacky, there is no way to bump the fees on the commitment transactions. if we had the opt to (?_ outputs then anyone could spend it could be even miners could spend it that was the original idea the miners would probably want you to clean this up or just anyone now there is there is no simple way of being the fees of a commitment transaction is being either are too low and you can’t use RBF you can’t use CPFP and basically you’re stuck.

Fabrice: If the fees are too high it's not much better anyway

Audience: [inaudible]

Fabrice: If if with sighhash_anyonecanpay a sighash_single then you don't need these you don't need to worry about fees for these transactions. You could have the zero fees on these transactions and when you want to spend them you can add any input and output you want

Audience: [inaudible]

Fabrice: Yes, because it's one input one output so sighash_single combined with sighash_anyonecanpay is a nice fits but it doesn't work for the commitment transaction

Audience: [inaudible]

Fabrice: No because this has to be confirmed first

Audience: [inaudible]

Fabrice: Yes, that's the same delay, I basically it's the delay that Bob needs to punish Alice if she tries to cheat so this is the same delay

Audience: [inaudible]

Fabrice: Something that is these are outputs and there's one input in the commitment transaction, these are all outputs I mean it's not it's a bit confusing on the diagram but…

Audience: [inaudible]

Fabrice: That's one of the reasons why we don't have dual funded channels in lightning because it makes a lot of things much more complex. So now it's really easy for the fundee transaction pays for everything and pays the fees. If you have dual funding channels how do you split the fees between funder and fundee as I think we said yesterday that it's easy to game and if all the money is moved to the other side does it still make sense - I mean splitting the fees is very difficult and there are also problems on you need to an interactive way of building the funding transaction between Alice and Bob, each canal includes an output in its design and agree you leak inputs it's really messy so it was too complex to get right for the first version of lighting, there's a proposal that is open today but it's really hard to get.

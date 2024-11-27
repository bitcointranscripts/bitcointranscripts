---
title: OP_VAULT for Bitcoin Covenants Panel
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=LC3lZ9dMRoA
tags:
  - covenants
  - vaults
  - fee-management
speakers:
  - NVK
  - Rijndael
  - Antoine Poinsot
  - James O'Beirne
  - Ben Carman
date: 2023-02-11
---
Speaker 0: 00:00:45

Today we have an absolute all-star panel here.
We're going to be talking about the Bitcoin Op Vault.
It's a new proposal by James.
And you know, like any new proposals to Bitcoin, there is a lot to go over.
And It's a very big, interesting topic.
So today we have Rindell.

Speaker 2: 00:01:05

Hey, good morning.
Yeah, I'm here talking about vaults, Bitcoin developer, and I work a lot on multi-sig and vaults that don't use covenants.
So really interested to talk about this proposal.

Speaker 0: 00:01:19

Very cool.
We have Ben de Carmen, ReturnGast.

Speaker 1: 00:01:26

Hey, thanks for having me on again.
I'm guessing I'm here because I posted to the mail as well how you could do like the CTV optimization with, for DLCs, you can optimize them with Covenants and I showed how you could do it with OpVaults as well.

Speaker 0: 00:01:42

Great.
Antoine?

Speaker 3: 00:01:44

Hey everyone, I'm Antoine Ponceux.
I've been working on building an actual vault architecture, which does not use Covenant for the past two years and a half.
Lately I've been working on other projects, but I guess that's why I'm here.

Speaker 0: 00:02:00

And the man of the hour, James O'Byrne.

Speaker 4: 00:02:03

Hey guys.
Yeah, I'm a Bitcoin developer.
I spend a lot of my days working on core, but for the last few years, I've been really interested in custody systems and the promise of vaults.
And last year, I actually implemented a similar vault design on top of OpsyTV, which I'm sure we've covered at some point on the show, maybe.
But I was kind of dissatisfied with those implementations for various reasons, and so decided to come up with this proposal.
So just want to say that, you know, I mean to make this a lively discussion, you should do your best to rip into this and you won't offend me, you know, kind of regardless of whatever you say, you know, like NVK said, any new proposal for Bitcoin has to be kind of shredded apart and scrutinized.
So totally ready and welcoming of that.

Speaker 0: 00:02:57

Now, this is going to be great.
So guys, there is a lot of confusion because there's a lot of stuff going on in terms of the Bitcoin Twitter drama and Bitcoin list.
I think a lot of people like me had the list muted for a few months due to, you know, tail emissions, RBF, Like, you know, there's been a lot of stuff that happened in the last few months.
So I kind of got the vibe that a lot of people like kind of missed UpVault, some of the discussions that happened because it was kind of like lost in the noise.
And also sort of like confuses it with like, you know, the ordinals and all this other stuff.
Like we just posted some questions this morning on Twitter.
And we were sort of like talking about ordinals.

## Overview of OP_VAULT

Speaker 0: 00:03:39

So let's just sort of like box in.
Like, so what is OpVault?
Like the elevator pitch first, just so we can get people to just sort of get it.

Speaker 4: 00:03:49

Yeah, so I guess I can field this one.
To be really brief, op-fault's basically just a really practical, low overhead way of introducing this way that you can lock up your coins in such a way that if you wanna spend those coins, you have to navigate through this delay period.
You have to wait for the coins to kind of settle, aside from the fact that you can sweep it at any time before that final withdrawal to a pre-specified, what I call, recovery path.
So the idea is, you can set up your coins to have some ultra secure, totally impractical, completely offline recovery wallet, or you could even do something kind of interesting like have a social recovery type thing where your friends hold keys and maybe you need three out of five friend signatures to actually recover the coins or something.
So basically it just gives you a way of introducing, you know, key storage or a fallback mechanism that like isn't really practical for day to day use.
But in the worst case, if your coins are gonna be stolen, you can kind of invoke.

Speaker 0: 00:05:00

Would you say like very simplistically, that's kind of like having a wallet in the blockchain, you know, like people, you know, deposit funds to this wallet in the actual chain.
And then there is this sort of, you know, they gave a bad name to it, but a smart contract that has some conditions.
And then if these conditions are met or change, like something else happens.
Right.
So like you kind of have like an if and else sort of like if this, then that kind of thing on the chain on your wallet.
Right.
So I'll give a very brief example.
Say, for example, I put the coins in this script, right?
This op vault that uses op vault that says, you know, you can only spend one BTC per block.
And if you try to do more, I'm going to send the coins to this other address, right?
That is like a recovery.
So for example, if somebody tries to send more, the coins are going to simply go somewhere else, right?
That's kind of like how you take your money back in case it gets stolen.
Would you say that that's correct?
Or that's sort of like pushing a little too far on what's possible?

Speaker 4: 00:06:07

It looks like Rheindel wants to talk.

Speaker 2: 00:06:09

I was going to say like, or the other motivating example that I use a lot is, you know, I think a lot of people will have some really, what they hope is secure, long-term storage for their Bitcoin.
So they've got maybe a multi-sig setup or they've got some hardware wallet that's buried under the well and they want to be able to periodically take coins out of it and move it either to a hot wallet for spending or maybe they have to send it to an exchange to sell or whatever.
And for a lot of people, I think the nightmare scenario is, oh God, what if my house gets burglarized and somebody takes my wallet?
Can they now just steal all of my money?
So a really great capability to have would be to say, you know, I've got a white listed set of places that I expect to be sending my coins.
You know, I might send it to my phone wallet, I might send it to an exchange.
If it goes to any of those, it's okay, I'm going to let it happen.
But if somebody breaks into my house, steals my hardware wallet and tries to sweep my funds, then I have some big red button that I can push and sweep it somewhere else.
And maybe that somewhere else is like a crazy five of nine multi-sig, maybe I'm going to sweep it to my Aunt Betsy's wallet.
Whatever makes sense to me, it's a way to have a holding period on the withdrawal of my coins.
And during that holding period, I can revoke that action.
I think that's generally what vaults give you and I'm sure we're going to talk about how you can scale that up to more sophisticated institutional setups like what folks at Revault are doing.
Or you can scale that down to just I'm a, you know, single hodler.
I've got my stash in cold storage and I just want to have really good security for when I take my money out.

Speaker 0: 00:07:56

So how does the blockchain know what's going on?
How does, you know, because, you know, this is not like we have a Turing complete between quotes blockchain contract system here, right?
So, so how does it know, like, how does your script know that somebody tried to do something?
And what, how does it know what to do next?
And how does that get triggered?

Speaker 4: 00:08:17

Yeah, so NVK, to get back to the example you brought up earlier, which is this idea of kind of like thresholding some kind of transfer rate, I just want to be clear that OpVault doesn't actually get into specifying things like thresholds because that gets really, really complicated.
And Antoine can probably talk about that because Revault is a way of basically enabling very fine grained thresholding and spending conditions kind of at a higher layer with multi-sig.
Now, Re-Vault could probably make use of Op-Vault almost certainly.
And actually, if you wanted to do the scheme that you were talking about where you're thresholding some transfer amount sort of per block, It's possible you could like tranche up your coins into different OpVault invocations, but I'm not as sure about that.
But OpVault is a much more kind of simple mechanism than Specimen Exertion.

Speaker 2: 00:09:15

Yeah, Maybe something that might help explain OpVault is maybe we can spend a few minutes talking about how you would do a system like this today with just multi-sig and ephemeral keys and pre-signed transactions.
Because all of these use cases that we're talking about, you could actually do today, but there's some real trade-offs in terms of liveliness, availability, and security of funds.
And I think what James' OpVault proposal does, or NVK, if I can say the C word on your show, what other Covenant proposals enable, is letting you get rid of some of those trade-offs by having consensus rules encoded.

Speaker 0: 00:09:52

The problem with the whole ephemeral key thing and the whole like Brian Bishop's vaults and things that he was creating, I forgot the name of that proposal.
It was just sort of like a theoretical idea, right?
Nobody is going to do that realistically because, you know, you can't prove that the keys were deleted even for yourself.
You can't.
That was what I think I talked to him about that in, what was it?
In a Miami meetup during the conference last time.
And I don't think most people even know about that, aside from people who are very close to core work.
So maybe we can touch up on it, but I'm not sure if there is much value in sort of like expanding too much on that.

## Practical examples of OP_VAULT

Speaker 0: 00:10:34

Why don't you give us like some some examples of of what you could do right now?
Like give us some practical stuff.

Speaker 4: 00:10:41

Like as a 30 second kind of overview of how you could do vaults today.
There are really like two techniques.
Number one is to generate these temporary keys and basically use those keys to sign, you know, a number of transactions that spend coins in certain ways.
And then you delete those keys.
And so after you've sent the coins into those transactions that are controlled by the keys that you just deleted, they're basically locked into a covenant structure.
The other thing that you can do is kind of like the way that Revolt works, where you have sort of a big array, like a big multi-sig setup.
And some of those keys are controlled by computers that will just kind of auto sign on the basis of certain conditions.
And you know so I think in the in the pre-signed transaction ephemeral key thing it's tricky because like you say key deletion is really tough and you have to kind of like, you're locked into all the parameters that you choose when you're creating the vault, like what key it's going to get transferred to, you know, what amount, who's managing the fees, and you have to keep track of all that transaction information.
And then if you're going to go with the more like sort of flexible revault implementation, you know, there's a big infrastructure burden, or I mean, bigger infrastructure burden in terms of like running all those auto signers and making sure everything's online and available and all that.

Speaker 3: 00:11:59

And also the introduction of new assumptions with regards to having pre-signed transactions because if you're running let's say a network monitor, watchtower as it's called in lightning world, that would enforce your spending policies.
Let's say with Reibolt basically you have a large multisig and you're delegating funds to a lower multisig.
So the covenant let's say is enforced by the fact that the lower threshold multisig does not have access to the keys of the N of N that is at the root.
So they are stuck with using an N-Vault transaction that is basically what's enforced on-chain with an open vault in more complex ways because then you have multiple keys and to this N-Vault is presigned to cancel transactions and so the N-Vault basically sends the coins either immediately to a transaction set is clawed back to the initial line of N or after a delay to some funds managers that can then use them.
In the meantime, a spending policy can be enforced by just broadcasting the canceled transaction.
And it comes back to your initial question about how these spending policies can be enforced under Blackchain.
The answer is that we don't.
We just let it delay with the pre-signed transaction or a covenant where we can enforce basically any spending policy whether it is a 2FA, whether it is a limited amount that can be spent per day, a whitelist, anything.
And what's very limiting with using pre-signed transactions here is that you need to know that all your watchtowers that are enforcing your policies get your pre-signed transactions before you actually sign the unvault transaction, before you actually commit to being able to get the funds out of the vault, you need to know that you are going to have a way to get them back with the cash transactions.
And usually in Bitcoin we assume, and especially with the SAMs, we assume that the laptop is compromised.
But basically with pre-signed transactions, you would store them on computers and had servers and you would not be able to, it's stateful.
So you would not be able to check on your signing device and only have the signing device as a rate of trust that you can always get back your funds.
Whereas if it's encoded in a covenant, you can check it on your signing device.

Speaker 0: 00:14:29

I mean, all computers are compromised.
Like, I mean, we're past that point now and the incentives are to become further compromised by even more actors compromising them, right?
Because now the money is in the computer and more people have the money in their computers.

## Anchors and fee management mechanisms

Speaker 0: 00:14:44

So let's say that we have op vault gets in, right?
And also anchors so that we can change fees.
Because you can't realistically have op vaults without having a way to changing fees or adding

Speaker 4: 00:14:57

more fees.
So what's cool now, I have yet to announce this on the mailing list, but I've actually figured out a way to avoid the reliance on v3 and anchors and all that stuff.
So like,

Speaker 0: 00:15:08

Well, that's amazing.
Wow.

Speaker 1: 00:15:11

Yeah, yeah,

Speaker 4: 00:15:11

yeah, yeah.

Speaker 0: 00:15:11

That is really cool.
Do you want to give us like a quick Brief on that?

Speaker 4: 00:15:15

Yeah, yeah, yeah, sure.
So basically in OpVault, you have to make a decision about whether your recovery path is authenticated or not.
And what I mean by that is so when you create the vault, you have to declare like where the funds can be recovered to.
In OpVault, you can optionally specify an additional script that has to be satisfied to even trigger that recovery.
And so the reason originally that we needed anchors for fee management in OpVault was if you're doing what I call an unauthenticated recovery, which is basically just like, if someone knows your recovery path, the way that OutVault works is when you create the vault, you hash the recovery path, and then you add that as a parameter.
So basically like the ability to recover is correlated with the ability to reveal that pre-image.
So if you do that you can sweep.
So it's sort of like you're not to get really technical you're not signing it with Sighash all and so there's some like pinning problems that can happen.
But what I found was that if you actually require you know an authorization for the recovery if you choose you know some key It could be based on like sort of a, you know, passphrase you memorize or a, you know, a wallet that sits in your closet.
It's okay if it gets lost actually.
But if you use that key, then you can basically roll in unrelated inputs and outputs to both the recovery and to the unvault transaction.
And so you can use that as your fee management mechanism when you're actually doing the recovery or the unvaulting, you can roll in unrelated coins, or you can rely on the ephemeral anchor approach.
So you have a lot of, you have even more flexibility about how fee management works.

## Fee management

Speaker 2: 00:17:05

So with like a, I'm not saying there's a good idea or a bad idea, right?
I just like as an illustrative example.

Speaker 0: 00:17:10

It's a safe space.
This is a safe space.

Speaker 2: 00:17:12

Right, yeah, yeah, for sure.
Safe space for bad Key management.
So if I wanted to have like a hot wallet on my phone that held the keys to authorize the recovery path, it sounds like a thing that I could do is keep a couple bucks in that wallet.
And then if I ever have to hit the big red button on my phone, I can use those little bit of funds to pay the fee for my recovery sweep.
Is that kind of the idea for whatever your choice of thing on your phone is?

Speaker 4: 00:17:40

Yeah, yeah, exactly.
That's right.
And, you know, like, oh, go ahead and end the case.

Speaker 0: 00:17:45

So, so like how, how would you practically do that?
Say like, you know, because the vault might be 10 year sort of plan here, right?
Like if people are doing this, they're thinking like, you know, they're kids, right?
Like, so, so like, I guess like, you know, you leave your key, like a key to a safe deposit box that has like, you know, say, you know, 1%, 5% of your stash in it, that is just sort of like the backup plan to handle things, because You don't know relative to your transaction how much that may cost in 20, 50 years from now, right?
It could actually

Speaker 4: 00:18:22

be a

Speaker 0: 00:18:22

lot more than 5, 10% of the actual stash itself, depending on how the UTXO set is, right?
So just curious, like how do you sort of like see that?

Speaker 4: 00:18:33

Yeah, so it's tricky to think about, right?
Because, you know, I think people rightfully raise the point that if in your fee management strategy you need to rely on actually having other coins available that aren't that aren't vaulted.
That's a reasonable objection to me, but at the same time, I think there are definitely plausible schemes where you've still got value locked up in that vault.
And so it's very easy to do this kind of atomic swap type thing where someone offers to fund your unvault on the basis of you presenting them with an unvault that pays them out some amount.

Speaker 0: 00:19:09

I can see that as a service.
And I think that's not an objection, per se.
I think this is more just trying to work out the kinks through, right?
Because it's sort of like a, we're going to have to rethink, right?
Like, and I'm speaking as somebody who does the harder wallets, right?
Like I'm going to have to rethink of like, how do I advise the users on how they do their setups and how do they use the, how do they, how do they do key management?
Right.
Because that's all going to change.
And this is actually fantastic.
Right.
Because multi-sig is a shit coin.
Yeah.
So, okay.
So, you know, like we have a way now to, to handle the fees.
Maybe it's, there is an op vault for the op vault.
Like maybe there's a simpler op vault that you built that just handles fees in case you need more fees.
Right.
That's like your fee wallet.
And the other

Speaker 2: 00:19:58

thing that's really nice about op vault as opposed to other vaulting schemes that rely on pre-signed transactions is that you don't have to pre-bake them.
If you're DCAing into your savings every month or something, you can then have one unvault or a few and then a series of recovery transactions.
That makes the fee management in the future more flexible than if every time you deposit into your savings, you have to pre-bake a transaction.
And now you have hundreds of these things and you have to worry about, how do I do fee bumping across this set of hundreds of pre-signed transactions from the 20 years that I was DCAing or something.

## Generating addresses

Speaker 0: 00:20:37

How practically speaking would a user get a list of addresses or generate new addresses to deposit on a vault?

Speaker 4: 00:20:44

Yeah, so you have a lot of choices there.
And this is kind of where I need to spend a lot, I mean, we need to spend a lot of time thinking about like what kind of the recommended usage patterns are because let me describe to you like all the variability that you have in terms of what goes into an op vault address, right?
So in simple terms, when you lock up coins in a vault, you're creating a pay-to-taproot transaction to a taproot script that looks like op-vault, and then the first parameter is the hash of your recovery path with that optional authorization key.
Second parameter is the spend delay.
And the third parameter is the hash of the key that you use to actually trigger the unvault process.
So that's what goes into the script.
But because this is tap root, right, we can choose an internal key to use.
So you can either choose a nums point so that the vault is the only spendable way.
What I prefer to do is actually use an XPUB that's associated with your super, super cold path, your recovery path.
And obviously there, you can either vary the XPUB along that descriptor.
You can keep the XPUB, you can keep the internal key static.
You can vary the recovery path along a descriptor.
So like really you can mask the fact that you're using, that you have like a number of different coins and addresses that are all actually controlled by the same key material, or you can just reuse an address.
And this is good.

Speaker 0: 00:22:20

So so like let's say we're doing this deterministically, right?
Because that's the best way to generate addresses like, you know, and you don't want to dox the pile, right?
So, you know, I'm I'm generating addresses there, right?
And I'm depositing to new ones because I have this XPUB somewhere.
So if I understand correctly, when I'm generating a transaction to unvault some of those UTXOs, it would look very similar to a standard wallet, right?
I mean, I pick those UTXOs, and this wallet understands the parent script there and sort of like say, hey, I want to spend this.
And if the key matches, then you start the process.
Right?
Would that be correct?

Speaker 4: 00:23:00

Yeah, that's right.
The only thing that gives you away in terms of that you're using a vault or doing an unvault is that you have to present certain data on the witness stack when you're actually spending the vault.
Because like with any kind of taproot script spend, you've got to present essentially the path, you know, and there are certain, like, I think the shape of the data that you're putting into the witness is going to be pretty readily identifiable as being a vault thing.
But to me, I don't know.
That's

Speaker 0: 00:23:33

not such...
I don't see that as an issue.
It's more a concern about, you know, people being able to link the UTXOs to the vault.

Speaker 4: 00:23:40

Oh, yeah.
Yeah.
No. So they can't.
They can't.

Speaker 0: 00:23:42

Exactly.
This is beautiful that way.

## Use cases for OP_VAULT

Speaker 0: 00:23:44

Yeah.
So let's say we get it in, right?
Like somehow we get it into Bitcoin, right?

Speaker 3: 00:23:50

Somehow.

Speaker 0: 00:23:51

Somehow.
Which we should get into a little bit too, because I think it's important.
You know, we get it in.
What do you think would be sort of like the first low hanging fruit sort of like scenarios that people are going to start building that are sort of like less complicated and sort of like more accessible to wallet developers, right?
They may not fully comprehend it, like how far this thing can go.
So like, What are the first few case scenarios you see that the people could sort of like start using very fast?

Speaker 4: 00:24:19

Yeah.

Speaker 0: 00:24:20

That would be also safe.

Speaker 4: 00:24:21

And I know I'll have to hand it off to Reyndall to cover because I know he's got some, but I do have a few.
Number one is like the brain dead improvement security that everybody could make at pretty much minimal effort, which is basically just introduce, like use OpVault and have your recovery path be a sort of separate hardware manufacturer kind of wallet technique than you have right now, even if it's as stupid as like some software wallet that you spun up on a computer one time, as long as it's not correlated with the way that you store your coins right now, there's essentially no cost.
I mean, the cost that you pay is like a slight delay to spend your coins, but there's no cost to introducing kind of an uncorrelated path to do recovery.
So really anybody could do that.
The second pretty easy scenario to set up, which I think is pretty cool, is if you're worried about like a hostage situation, you can actually, and really, I mean, OpVault is kind of uniquely allows you to do this.
You can set up a configuration where let's say that your spend delay is a week.
And let's say that your recovery path points to a taproot script, which is only spendable after a month.
You can have a situation where you can prove to your attacker, hey, look, I can't touch these coins, even if you start the process moving.
We can't touch this for at least another week.

Speaker 0: 00:25:48

So that secondary receiving script, would that be based on where is the private key for that?

Speaker 4: 00:25:56

You're talking about the recovery path?

Speaker 0: 00:25:57

That's right.

Speaker 4: 00:25:58

Yeah, so that's up to you.
However you want to store that, whether it's in your backyard, safety deposit box.
You want to store it in such a way that it's not readily accessible, you know, I think, online.
It's because if somebody gets your recovery key and they figure out your recovery key, where your vaults are, and the sort of recovery parameters that you used, they can trigger a sweep to your recovery wallet.

Speaker 0: 00:26:24

Yeah, I mean they have access to the nuclear code.

Speaker 4: 00:26:27

Yeah.

Speaker 0: 00:26:27

Let's put it this way, right?

Speaker 1: 00:26:28

Yeah.

## Key management

Speaker 0: 00:26:29

So would you say that, you know, with a few years of this in the market and people really making this safe, let's put it this way, would you say that maybe you don't have a nuclear code anymore?
You go the path of the ephemeral keys to generate all these paths.
And then they just sort of like keep on rolling, right?
And your family has been the owners of this vault for the last 100 years.
And things just keep on rolling and moving and rolling and moving.
And maybe you have a key ceremony every 20 years where you give the, you do a key shuffle, for example, a provable key shuffle, where nobody essentially knows what the keys really are, and it's provable, and you do it on camera or whatever.
And then the family sort of wealth continues into this sort of rolling vault.
Is this something that you sort of like imagine or you're thinking more sort of like today, nuclear cold kind of thing?
Or it's maybe unsafe to do that, I don't know.

Speaker 4: 00:27:29

I can imagine that.
I mean, you can certainly facilitate the transfer of a vault pretty securely based on the spend delay.
So if you and your family decide you want to set up different security parameters, different key configuration, obviously, like Taproot gives you a lot of flexibility in that recovery path.
So you can set up all kinds of spending conditions there.
In terms of like doing key delegation and renegotiating, you know, which keys can sign, that's, are you, Rheindell, are you unmuting this?

Speaker 0: 00:27:56

Yeah, I

Speaker 2: 00:27:56

was gonna say, like, the other cool thing about this being TAPRUD is since we have Schnorr signatures, we can do things like proactive secret sharing.
With Frost, which is a threshold signing scheme for Schnorr signatures, you can do things like you can change the quorum size of the signing set or you can change the composition of the signing set without actually doing an on-chain transaction.
So if over time you wanted to change your primary vault key from being a three of five to a 10 of 15 or whatever, because you've amassed generational wealth in your vault, you could do that without actually needing to reconfigure your vault.
There's a lot of moving pieces there, but because this is built on Tapper, there's these orthogonal key management gains that we're going to have that I think are additive for vaults.

Speaker 0: 00:28:48

If we just use the imagination, the idea is I no longer need to make hardware wallets, right?
Like, no, seriously, it's like, you know, I make a device that is a safe device for you to construct the transactions outside of computers, right?
Or construct the scripts outside of computers.
And you're in your starship going somewhere else, and the vault just exists in chain.
And you just continue rolling, and nobody needs to touch it.
And it doles out funds based on your trust's actual trust rules.
And you have trustee keys.
And you can really represent the trust rules, for example, on a script.
It really is not that hard so that you're complying with the law.
And like, it's quite amazing when you sort of really extend this out.
I know it's like, there's a lot of moving parts and things, but I get excited about that because seeing users have single SIG plus passphrase being way more sane than cool multi-stick stuff that you can do, and people lose money with that.
I think that what we have is amazing.
It's an incredible upgrade from fiat and from gold vaults and things like that, but it's completely unsustainable.
Like I cannot see, you know, like a billion, two billion people, you know, with like harder wallets that look like the ones we make, you know, maybe the cards, but like, even then it's like, there is a limit to this, right?
And most people also won't have enough money or wealth that will be worth the device.
And we can make sort of like poor people's vaults.
Right?
Like, you know, like, and like a person doesn't have to have a lot of money to be able to have a solution that's like, here, you spend this script and the little savings you have go into this.
And these things are all done for you.
They're all very safe and simplified.
At least this is how I see the stuff playing out.

Speaker 2: 00:30:50

It also expands the design space of where you can have trust-minimized third parties that can help you with management without actually delegating spend authority to them.
So James was talking about this hostage situation a minute ago.
Imagine a scenario where you're like a high net worth person or you've amassed your giant stack of Bitcoin.
And so you have some company that you say like, hey, look, If you see movement out of my vault and I'm not present in your office with all of my family, then push this button and it'll trigger my emergency spend path.
And boom, that's how you deal with somebody kidnapping your kids and using it to extort your money out of you.
That's a way that you can delegate some very, very, very specific

Speaker 0: 00:31:38

spend path execution

Speaker 2: 00:31:38

to a third party without them actually being able to spend all of your money.
There's lots of really interesting use cases in that direction.

Speaker 0: 00:31:44

Right now, there are people out there that have an envelope sealed in their lawyer's hand with their private keys.

Speaker 4: 00:31:50

100%.

Speaker 0: 00:31:52

And it's not a non-trivial number.
Well,

## Inheritance planning

Speaker 2: 00:31:56

the reason why I started talking to James about this is I think that a really underappreciated use case of vaults is for inheritance planning.
Right?
Like everybody has this problem of I want to make sure that either my kids or my wife or whomever can get to my Bitcoin if I get hit by a bus.
But I also don't want to have like a spat with my wife and then she runs away with all my Bitcoin.
Or I don't want my kids to decide that they want a new car and they like go upstairs into the family firebox and like steal all the Bitcoin.
So it'd be really great if I could give my kids or my heirs or whomever some easy way to get to my Bitcoin, but there's time as an additional sort of authentication factor.
And if I look at my phone and it says that my inheritance path has been activated and I'm still alive, then I can push a button and sweep those funds back.
I think that kind of thing is maybe a really killer app for Bitcoin self-custody because you can't do that with other bearer assets.
And being able to do that at an individual level without a bunch of extra infrastructure is really appealing.

Speaker 3: 00:32:57

You can do that on Bitcoin today.

Speaker 2: 00:33:00

How would that work?

Speaker 3: 00:33:01

You just receive two scripts with the CSV, maybe of one year.
So of course, with Covenants, it would make that easier because then you can have a trigger transaction and so you don't have to rotate your coins.
This inheritance thing, you can already do something.

Speaker 2: 00:33:20

Yeah, so you can do that with CSV today, but then you end up with the problem of, you know, I set a two year, you know, relative time lock on my coins, and now every year and 11 months, I have to like go and rotate my UTXOs in order to reset the timer.

## Simplicity vs complexity

Speaker 0: 00:33:35

You know, it feels unsafe.
It feels that everything that we have for this purpose without something like proper covenants on chain is not possible for most people.
Right?
You're definitely going to have something like Revolt, you know, where, you know, institutions are gonna go and they're gonna have people audit the script and audit the paths and sort of like, you know, like go through the, but it's gonna be very hard and it feels unsafe.
I mean, like when people are talking about their money, it cannot, if it feels unsafe, right, like multi-sig feels unsafe, right?
Like people won't use it, right?
This is the beauty of passphrase with single SIG, right?
Like it feels safe.
Yeah.
And then

Speaker 2: 00:34:19

it's so simple, right?
Like there's not many moving parts.

Speaker 0: 00:34:22

I mean like the amount of people who lost money on the most secure system that there was at the time, which was Armory.
Remember Armory wallet?
Yeah.
I know so many people whose coins got locked and that's it.
You know, this is the issue with all this complex, amazing setups is that like you end up screwing yourself out of your coins, which is the majority of the people.

Speaker 2: 00:34:45

Well, and I think we're seeing market demand for that, right?
Because like when the multisig descriptor was added for Taproot in Bitcoin Core, like the first thing that everybody did with it was time decaying multisig.
Because people want the security of multisig, But they also really want to make sure that they can get to their money.
So they say, OK, cool.
In two years, it's going to decay from a three of five to a one of two or something.
But then you have this problem of like, OK, I've got a ticking clock until my coins become less secure.
So now I have to have a reminder on my phone every two years.

Speaker 0: 00:35:19

Yeah, but then you get hit by a bus and your wife didn't know.
And now you went to another wallet that they had no idea.
We see this all the time.
The clever programmer husband goes and creates a shadowy super code, or amazing script and amazing set up on their, you know, like vintage, you know, 93 IBM laptop, right?
And we feel like cubes OS and you know, and then like, great, So cool.
Well, one, he probably gets pissed off one day and accidentally like attaches a USB stick and boom, money gone.
Right.
Because he was just not thinking that day.
And then the other one is, you know, again, guy passes, right.
Or get gets like, you know, brain doesn't work anymore.
And that's it.
Like family can't recover.
Like it just happens a lot.

Speaker 2: 00:36:11

I don't see how

Speaker 3: 00:36:12

it relates to having a time-locked recovery key.
I mean, it's just a straight improvement to the situation that you described with the envelope having to share your public key for inheritance.
You just have a secant public key that is tamelocked and you just share this one.
So at worst case, you don't rotate your coins within years and well, you're probably dead.
But if you're on that and just you forget for years to not rotate your coins, then the lawyer can access your coins and it's the same situation as today.
So.

Speaker 2: 00:36:42

Well, I think the challenge is sort of this thing of I think there's been enough education in the Bitcoin ecosystem about, hey, you really need to have your seed backed up.
But I think when you start getting into more interesting scripts and more interesting spend paths, people are less sure about How do I back up my descriptors or whatever other metadata I need to actually spend those coins?
And so, you know, there's a lot of just, you know, people are figuring out new places to hide a piece of metal with seed words stamped on them.
We haven't really gotten to that level of creativity for what do I do with my descriptor?
Like I haven't seen somebody, you know, tattoo their blood type and their descriptor on their butt cheek yet.
But I'm sure it's coming.
And I think that how we back up that metadata is a super important question.

Speaker 0: 00:37:31

One of the things I absolutely hate is Shamir's secret sharing for key backup.
Because it's like reinventing multi-sig with a complex script that's completely custom.
And it's like vendor specific and it's not Bitcoin related.
So I'm like, okay, if you're going to do this, then use multi-sig.
At least it's Bitcoin.
Right.
And there is more sort of like, you know, greater sort of education and adoption.
So that was the motivation to create CDXR.
Right.
Like We still needed a way for people to split their main root keys, right?
But we wanted a way that a donkey could recover with pen and paper.
And just sort of like every time we start thinking about practical security, we try to go back to World War II, right?
Seriously, this is how we think about this stuff.
And it's like, OK, I am a guy trying to flee some country that's in war, and computers are not available or compromised.
I need to take my money with me, right, like and I have to go naked, right, like how do you actually like go through that process, right, like based on this complex stuff and sort of like that kind of leads me to Like, you know, the further picking and risks that I'm trying to sort of like think through on OpVault are the practical ones.

## OP_VAULT practical applications

Speaker 0: 00:38:52

I think we can still like sort of go through a little bit more of the technical stuff in terms of like the actual, like interesting parts of how this works, but the practical stuff, you know, needs a lot of thoughts still, right?
Like how do you manage this keys?
How do you manage the nuclear codes?
Do you do an op-vault, an op-vault, an op-vault?
So like you have some recursive way of like moving stuff around.
How would wallet UXs address the vaults and create all the stuff?
And you know, what kinds of like things you guys have like sort of fought through in this sort of practical space?

Speaker 4: 00:39:30

I think that's a lot of the work that remains to be done.
I mean, I think the framework right now gives the end user a lot of configurability.
And in designing it, I'm trying to avoid any particular configuration that would be like just blatantly unsafe and, you know, like any use that just wouldn't make any sense.
But at the same time, you know, I mean, things like for your recovery path, are you using a static address there or are you varying it over a descriptor?
You know, like that does have implications.
Is your optional recovery off parameter, is that derived from maybe the descriptor of your cold wallet?
Or is that a separate key that has its own life cycle and is independent?
All these choices do have implications.
And I think we're really going to have to spend the next year, a few years, like kind of figuring out what the right usages are and like really nailing those.
But my concern, you have to balance kind of like getting the usages exactly right with like the fact that right now custody for everybody is nerve-wracking.
It's totally nerve-wracking.
Like Jameson Lapp has this great article where he talks about vaults, a little bit about the history, a little bit about OpVault.
And he introduced this framework for thinking about things, which is like right now we have proactive security, which is like you do your best to build your fortress, like set up your keys in the right way.
But, you know, like, I mean, notable developers, right, have been compromised and it's probably likely that they went to great lengths to do this proactive security and build this wonderful fortress that like fell down.
Something like OpVault gives you like reactive security where you can see, okay, like I've been compromised, an attack is happening, what can I do about it?
How am I going to respond?
And so OpFault's really the first on-chain mechanism for doing something like that.
And I think we have an acute need for it, especially at the corporate level.
Like, look, I mean, individuals holding Bitcoin is my favorite and most important use case, but like, we all like that micro strategy holds a lot of Bitcoin.
You know, one plausible argument for like a better future is for someone like America, you know, to hold Bitcoin as a reserve in their central bank.
To do things like that, you need an ironclad nuclear level strategy.

Speaker 0: 00:41:57

It lowers insurance.
See, this is the thing.
Yeah, by a lot.
When you're talking about institutions, institutions don't have the luxury of like choices, like of many choices or like, you know, how they feel about stuff.
You know, like you have like legal frameworks, right?
For custody of things as a public trader company or whatever, right?
And then you have your charter, and then you have all your fiduciary nuances of things.
And you're going to have to follow these very traditional ways on how things are custodied.
And then they might de-risk it by using different vendors as well, so splitting the pile.
And then everything needs to be insured.
And often you have insurance of the insurance as well, especially because if you're trying to, and it's in dollars for the next foreseeable near future here at least, you know, this is denominated in dollars, so you have to get reinsured as the price of Bitcoin goes up and down.
And, you know, they're gonna try to understand your vault, your security, you know, like that's why you use custodians that already have like a lot of like, you know, provable experience on what they've done, like Fidelity or Coinbase or whatever.
And you know, it costs a lot.
The insurance on this stuff is obnoxious, right?
Because this is a very easy to steal asset, right?
Like its best feature is its solubility and you know, fungibility and transportability, right?
So how do you do that cheaper, which everybody cares about, and safer, right?
And I think this is great for enterprise that has to deal with insurance.
And soon enough, we're going to see even individuals seeking insurance, right?
That's what the guys from like Anchor Watch and things like that are trying to do.
But it's hard, because you can't prove that you lost a key.
You can't prove that it was not a boat accident.
It's very tricky.
You know, like say the cops break into your house because somebody did a swatting on you, and they opened your safe, and they took a look at the keys.
Now the money disappears a month later.
How do you prove that the law did it, right?
I mean, look at the Silk Road problem, right?
I mean, all the cops involved in taking down the Silk Road magically became millionaires, right?
So anyways, like this stuff really sort of facilitates this next stage of the Bitcoin future, at least in my view.
That's why I'm so excited about this.
Now, I think we can do like a lot more complex stuff.
And, you know, that's why I brought Ben here.
Ben is interested in the shit coining layer of Bitcoin.
I'm just kidding.
He's going to talk a little bit about DLCs and like lightning stuff and all the things that we could maybe do with OpVault as another primitive in Bitcoin?

## Covenants and discreet log contracts

Speaker 1: 00:44:34

Yeah, I mean, to preface it, like, if we want to do all this stuff, we probably don't want to use OpVault for it.
We should use like CTV or APO or like, I mean, things that are like more custom tailored for it.
Like the way you do it with OpVault is kind of a hack.
But basically like, you know, we want these primitives where, like today with like Bitcoin script, you can't really say it has to be spent.
It's only locking it under these conditions.
You're not saying it must be spent with this amount or to this address and anything like that.
So you can't have any guarantees in your address that it's gonna be spent to the right person, just by the right person.
And because of that, say you have an address with one Bitcoin in it and you say, I want it to be split 75% to me, 25% to James.
The only way to do that is just like me and James have a multi-signature agreement to sign that correctly.
Versus like with not vault we can have that or like CTV or any of those, we can have it like enforced in the script that 75% will go to me and 25% to James.
So with that kind of primitive you can build a lot of like really cool stuff where I mean, the one I pointed out was DLCs where I mean, Lloyd funny point out originally, and I showed you could do it vaults where you could, instead of like having a DLC with like a 10,000 pre signed transactions, you just have a single address that's encoded inside the address as your entire DLC contract.
So you can create these really fancy stuff all inside of a single address.
And the cool thing is too, you can make these extremely composable, where your DLC payout address is just another DLC, or maybe instead of being an individual in a DLC, you have it as a company.
So then say I win the DLC, then the payout goes 9% to me, and then 10% to my investors or something.
So you can kind of like build these structures really easily where like all these fancy things are happening all in force in Bitcoin script instead of like hoping your multi-sig game theory works out.

Speaker 2: 00:46:29

Yeah, like The way that I've been trying to generalize this is a lot of times if you want to do interesting smart contracting with Bitcoin, what that usually ends up looking like is trading around a lot of transactions for people to sign and then trade back.
And what's really cool about Covenants, and you know, I think like a really simple generalization of Covenants is that Bitcoin script right now lets you put conditions on the inputs of a transaction.
Covenants let you put conditions on the outputs of a transaction.
And so if you have some Covenant system, then you can take all of the network IO and the coordination of signing in contracting protocols and you can reduce it down to signature generation.
So locally, I generate a giant Merkle tree of all the possible conditions and I sign it and we just have to trade around Merkle commitments.
And that's a lot cheaper from a coordination perspective than we have to actually pass all of these things around.
And that's really important for DLCs. I think it's also important for things like coin pools or channel factories or other multi-party constructions.

Speaker 0: 00:47:33

Let's talk about some examples that a person who does not understand this technically sort of like would get like, what things could we see here?
Because now that you have the DOCs, you know, with proper chain control, right?
You can do a lot, right?
I mean, you can create financialization things, products, you can do like batting things, you can do, there's really like a very big sort of like new space of things you can do.

Speaker 4: 00:48:05

So maybe, Ben, you know, could you talk about, I know this is kind of controversial, but for me, this is one of the most exciting things is this idea of doing endogenous USD stable coins with DLCs, where you don't have to have some entity that's like holding dollars in a bank account.
You can synthesize USD exposure with Bitcoin.

Speaker 1: 00:48:24

Yeah, that's exactly what I was going to bring up.
Like I think the biggest use case most likely for DLCs is either degenerate gambling of like sports betting or, you know, 100% or other likely is, you know, creating stable coins without like having like, you know, Tether, which just has a bank account somewhere and you hope it's there.

Speaker 2: 00:48:42

And a stable coin, a synthetic stable coin is degenerate gambling on the price of Bitcoin.
So it's all the

Speaker 3: 00:48:48

generic answer.

Speaker 0: 00:48:48

It's a directional trade.
This is the problem.
Yeah, for sure.
Both legs of the asset and the collateral are of the same market to market.
Like, you know, this is essentially what we saw in this last Bitcoin pump and break, right?
Like, it was the fact that everybody was using the same asset as the collateral, you know, betting on that asset.
But like reality is like especially people who don't have money, what they want is USD.
Like I mean, they need stable stuff, right?
They can't, they don't have enough float to survive Bitcoin's volatility.
Right.
I mean, that's that's a wealthier people problem.
So, you know, I'm a huge fan of stable coins.
I think like until we're hyper-bucanized world, like we're going to need them.
And I don't want them to be controlled by the state actors that provide the armies.
So Ben, how would you build the most simple, stable coin on this setup?

Speaker 1: 00:49:39

Yeah, I mean, with DLCs, you just create a contract where you say like, you know, I'm going 1X short and your counterparty is going 1x long.
So then the person holding 1x short, you know, they're holding Bitcoin, but they're short.
So it's not even.
And they're like essentially holding dollars on Bitcoin.
And like to do that today without like any covenants, it's a little impractical, like, you know, because you're doing a bet based off the Bitcoin price and the Bitcoin price is just a number.
So you're going from zero to like, say like 100,000 or like a million, you have a lot of different outcomes there.
And especially like in a DLC, you're trusting an Oracle.
So maybe instead of trusting one Oracle, you wanna trust like a three or five set up and like, you kind of get an explosion of possible outcomes there for all the different Oracle outcomes, or which Oracles are signing exactly like what price they're signing.
And like we were doing tests when I was a shared bids of this and like, we did like a bet on the Bitcoin price with two or three Oracle set up and it was something like 80,000 possible outcomes with all the optimizations we did.
So we sent around 10 megabytes of signatures.
It took a couple minutes to sign and it was ridiculous.
It works on our laptop, it's eight cores and all this stuff, but, you know, making an actual user-friendly thing on an app is like not really going to happen with that.
At least, you know, not anytime soon, but with the Covenant's route, it would make it a lot more simpler where we're not doing all this huge bandwidth of signatures and stuff like that.
We're just gonna calculate the Merkle tree, which would still be a little complicationally expensive, but not nearly as enough.
And it makes it so much simpler in the protocol as well, where we need all these round trips back and forth and all this P2P stuff is basically generating address, verify the other card and probably do the same thing and sign a transaction.

Speaker 0: 00:51:24

A critic would say like, you know, but why, why, why not do this on AWS?
Right.
And like, just, you know, do the payouts in Bitcoin.
Like, why do we need to do this on Bitcoin?
Why do we need this extra stuff?

Speaker 4: 00:51:39

Trusted third parties or security holes, right?

Speaker 1: 00:51:41

Yeah, exactly.
Like, you could, yeah, like deposit in the Coinbase and do the bet and then, you know, withdraw, but you know, we saw FTX worked out.
We saw, you know, the other thousand before them worked out as well.
Like we need to kind of wait to do this natively.
And like, I think there is demand like and the shit coin space, like a lot of people are using like, you know, all their trading stuff on there That's like a uni swap and blah blah blah just to like trade stuff quote-unquote trustlessly So there actually is demand for this and it seems like you know I'd rather people use Bitcoin than shit coins to do it So I hope it's

Speaker 4: 00:52:15

been as I understand it the big problem with doing stable coins on DLC is, I guess the technical term is novation.
So it's like, if you want to treat this thing as a coin and trade it around, you're essentially trading like a futures position around.
And that's like, I've thought only briefly about it, but I couldn't figure out kind of how to do it right away.
Do you have any thoughts on how that might work out?
Like, is there some key delegation thing you could do?

Speaker 1: 00:52:42

There's a way to do it.
On SharedBits, there's a few blogs on how to do it for all the different setups.
But I mean, essentially, the worst case is if your counterparty disappears, you just open up another trade with someone and you're double collateralized, which kind of sucks.
But otherwise, you kind of start closing it with your counterparty while also opening it with the new counterparty and you're able to kind of sell it in that way.
But yeah, it kind of takes like.

Speaker 2: 00:53:10

So it's like an atomic thing of like, I sell one position and open another position at the same time.
And so my net exposure stays the same, but I've actually closed and opened two contracts.

Speaker 1: 00:53:24

So you'd have to say Alice, Bob, and Carol.
Alice and Bob already have the position open and Carol wants to buy Bob's position.
Basically, you'd have like one transaction that's opening Alison Carol's new contract while closing Bob and Alice's contract.
So Bob gets the exit to set up, while like, you know, leaving his position while Alice and Carol kind of start the new thing.
And you know, you could update the contract in there, you could pay out anyone in that transaction of someone's paying for a premium or something like that.
So it should all technically be doable.
I mean, the covenant model gets a little easier because, you know, now there's less activity or interactivity and stuff like that.
So, you know, if you had to do these 80,000 signatures, you have to do, you know, 160,000 for the two parties.
So this makes it like a little easier.

Speaker 2: 00:54:15

Yeah, I was gonna say like with the Covenant case, if I've got a mobile app, and on my mobile app, I say like, because I think the best lightning app that we could ever build is kind of what Bitcoin Beach is trying to do.
But theirs has a custodial backend, where you have a lightning wallet.
And then in your lightning wallet, you can say, all right, I've got 50 bucks.
I want 30 of that to be pegged to the dollar because I can't stomach short-term volatility.
And then the other $20 I want to keep in Bitcoin.
And like you just kind of drag the slider.
But if every time you do that, if I'm opening a new position and we use DLCs as they exist today and me and my counterparty have to trade and sign 80,000 CETs, like contract execution transactions, that's insane from a mobile phone.
And then I have to do that like every time I drag the slider versus if every time I drag the slider, you know, yeah, I'm hashing a bunch of, you know, CETs locally into a Merkle tree and then we trade one commitment, both sign a transaction, we're done.
Like that's something that I could actually imagine happening.

Speaker 4: 00:55:20

So are either you guys going to, you know, like advocate for either CTV or kind of whatever your preferred mechanism is?
Because I know there's talk about like simplicity, there's talk about these more general, fancy Covenant structures, but I think there's just, in my view, a ton of time difference between Now and when these things are deployable and proven safe.
So I mean what what's your guys's plan?
I

Speaker 1: 00:55:51

Mean simplicity would be the best thing but like that is so far away Like I don't think it's reasonable to talk about

Speaker 4: 00:55:57

I looked at the patch set on elements.
That's up right now.
It's 77,000 lines plus

Speaker 2: 00:56:05

It's a year Linux desktop it's

Speaker 4: 00:56:08

And spoiler alert like the code is not breezy.
It's not like a nice Python.
You know, it's like hard to read.
So

Speaker 3: 00:56:17

Yeah, well, I mean like one

Speaker 2: 00:56:18

of the things I like about the op vault proposal is that I think it is more specific, and I think it's easier for people to see a straight line from that proposal to actually use cases that gain market traction and actually add value for Bitcoin users.
I think you can have a really, really good debate about, do we want to have a really general purpose covenant structure that takes a long time to figure out if it's safe, or do we want to just hold tight for simplicity?
If the goal is that eventually we're going to have either super general covenants or simplicity but that's in the future, I think there's a reasonable case to be made that okay, in the near term, let's do something sooner that adds value now but doesn't try to go 90% of the way to a super general purpose covenant scheme.
Like, I think I'd be less inclined to say, let's do really super generic covenants and then also try to do simplicity, because there's a little bit too much overlap there, whereas something like OpVault, I think, is much more targeted and kind of adds value

Speaker 1: 00:57:23

to that.

Speaker 4: 00:57:24

I'm definitely gonna shill OpVault in the short term, but I do think, I mean, if you look at the patch set for CTV, like, it's a very well-scoped, limited change.
A lot of people have spent a lot of time, you know, trying to pick it apart.
God knows everybody wants to dunk on Jeremy.
And so.

Speaker 2: 00:57:41

And there's money there to be made if you bring

## OP_VAULT benefits

Speaker 4: 00:57:44

the problem.

Speaker 0: 00:57:44

So, so like just before we go into activation and a path to sale, it's a sales job, one more thing I wanted to just address in terms of features and benefits of this is in terms of Lightning, what benefits do some of the Lightning setups right now would have like sort of like immediate improvement?
Because right now Lightning doesn't scale, right?
I mean like, you know, it's cute and all we can have say a hundred to like 50 million people using it, but we cannot have say like half a billion people using Lightning.
It's like actually impossible.
So do we get some extra sort of like braving room on Lightning with OpVault?

Speaker 4: 00:58:24

I think it's plausible that OpVault might help to compress the witness sizes for Lightning transactions a little bit.
But to be honest, I think that that might be marginal.
I mean, you'd need someone who's really, really in the weeds on Lightning to sit here and tell you whether or not there is some kind of significant kind of game changing improvement there.
But from my impression, I think it's it'd be a nice little marginal compression maybe, but it wouldn't be like a game changer.

Speaker 0: 00:58:53

Okay.

Speaker 3: 00:58:54

Yeah, maybe there is some benefits to coins pools as well as well as scaling solutions that are possible with constructions that are close to upvotes, but a bit more generalistic, such as tapleaf, update, verify.
I think there is definitely value with that.
If there is a spectrum between just doing CTV and doing simple CD, maybe in the middle, doing something like tapleaf, update, verify, maybe with some kind of checker, it puts verify.
I think it would complete what you need to do vaults.

Speaker 4: 00:59:25

So the trade off there, if you do sort of more low level granular opcodes, like TLOV or check outputs, then everybody comes up with this standardized vault construction that you have to encode in script.
And everybody's basically doing the same thing, but the script sizes are huge.
And so these transactions end up being very costly.
And I'm not even sure, to be honest, if you can get the same behavior from OpVault that you can, like, just with those two opcodes, because there is some special logic around supporting immediate re-vaults during un-vaults and things like that.
So it's, you know, I think like something like vaults is a really good example of even if you had the super futuristic flying car covenants, it's like, well, maybe you still want to vault because it's a very common usage that you want to compress.

Speaker 3: 01:00:19

Well, we don't know if it's yet a very useful, very used, well, very common use case.
We don't know yet.
And I don't think, well, I'm not buying that it would be so much more expensive to do with WP-5D to verify what you're doing with UpVault.

Speaker 4: 01:00:34

It could be, but you know, nobody's shown me the scripts, like nobody's written me the scripts, like Show me the code.
People come up with these highfalutin proposals and it's like, okay, maybe that sounds good and if I squint at it, I can interpret it in such a way, but like, where are the patches, you know?

Speaker 2: 01:00:51

Yeah.
Show up with patches.

Speaker 3: 01:00:52

Yeah.
I agree.
I agree with regard to the implementation and that's something that I was, I was wanting to, to look into, I wanted to implement a Taply Third Date Verify on ReVault, like just implementing ReVault with Taply Third Date Verify, which would basically give upvault in a bit more generic way, but I never came to do it.
But AJ in this original Taply Third Date Verify post as a vault construction that is close.
Well, it's not really a freeze all my funds recovery path like you have on upvaults, but it's a revolt path that keeps revolting.
It's a decent vault construction with the detail of the scripts that seems to work.

Speaker 4: 01:01:34

I haven't seen an implementation.
I read all those posts.
They seem to be very vague.
And I've been working closely with AJ on his proposal, actually.
He gives me feedback on a semi-daily basis in terms of how to guide the proposal.
But I'm not buying the T-Love stuff until I see the code.

Speaker 3: 01:01:52

Yeah, sure.
That's fair enough.

Speaker 0: 01:01:54

So like if we had to just like sort of like wrap up the benefits, right, like of this for like your average user, right, like out there who is going to be engaging in hats and other means of getting things into Bitcoin dramatically or undramatically.
Like what would you say are like the 10 main sort of like one liners that like, okay, like we activate this today, like you gain this set of lists, like nearly immediately, right?
Like assuming of course there's a UI to use it and stuff, but like, you know, it's like very achievable, very simple, very safe.
Like, you know, you get this.

Speaker 4: 01:02:34

Yeah, so my tagline has kind of been, you get the operational complexity of single SIG with multi-SIG security, multi-SIG safety.
And, you know, Personally, if I could do this for my own funds, I would sleep a lot better at night because I could have coins in cold storage and I could be alerted if somehow in any number of a million different ways, my infrastructure got compromised, my Rodolfo backdoored my cold card.
There's just a million different ways you can get popped.
And I don't want to rely on having built the perfect fortress and pre-anticipated everything.
And so I want to be able to have reactive security.
And I think OpVault is today like kind of the most straightforward, easiest to use way to do that.

Speaker 0: 01:03:24

So like, you know, essentially you get like, you know, like end user, sort of like amazing security with like, you know, you can build some fairly safe, straightforward scripts that handle normal people's money problems.
You can have institutional problems resolved.
You can create.

Speaker 2: 01:03:43

There's probably also a middle thing in there too.
There's been a lot of discussion about things like e-cashments, like Cashew or Fetimint.
And this would also be an upgrade for their setup.
Because what those systems are is they're basically just smaller custodians.
And so if you want to uncle Jim funds for your family, your friends, your community, your school, whatever, and give them a very private lightning wallet via Chami and eCash, it would be great if you could upgrade your security setup without dramatically increasing operational complexity.

Speaker 0: 01:04:20

Yeah.
So, you know, you get the DLCs, right?
So we can finally have some interesting dynamic stable coins or any other kinds of dynamic contracts really being represented in the actual chain, right?
Or protected by the chain.
And we get some simplicity.
I mean, like, you know, UpVault is a very, it's like, it's a small patch.
It's a small, I mean, compared to other things that do covenants, this is my new school.
Totally.
Right?
Like, yeah.
I think, at least I have not bumped into very reasonable, very strong opposition from anybody who understands this stuff.
So I don't know.
It feels like a very sane next feature for when everybody is in the mood of getting next feature.
And you resolve the fee problem, which is kind of a huge deal.
I think that the rest of the unresolved things are more practical, like how to handle the keys and how to sort of do things in the UI, sort of like the implementation real sort of like issues.
But those things are true for everything that you build new.

## Criticisms and risks

Speaker 0: 01:05:31

So now like we sort of like we should start addressing like the hard part, right?
Can we go through some of like let's try to steel man some of the some of the realistic sort of criticism and risks and also maybe some of the most absurd ones.
Especially I think like addressing absurd things is very important because, you know, this stuff is not simple, right?
So like people don't get it.

Speaker 3: 01:05:56

Yeah, maybe if I can add something, maybe some nuances to the use case of Vaults because obviously I'm a big fan of Vult.
And I've been, or maybe the more nuanced that I was in the beginning after trying to solve all the issues, especially with the actual implementation and deployment of these solutions, because it's not all in the scripts and having an MVP, but trying to figure out what theories of that you're going to use and how you're going to manage this theories of and how you're going to use them is a huge problem.
And that has huge consequences on the security of your setup as well.
So yeah, just to give more answers, is that basically Vaults give you spending policies.
It's give you spending policies and you can have spending policies today with a cosigner.
So you could always have an HSM that enforces co-signing policies and that is going to, well, you can always trust that this policy is going to be enforced as long as you trust the HSM.
So it's a single point of view.
And vaults give you the possibility to have decentralized enforcement of these policies, but hopefully the transaction confirms.
So it's a trade-off.
And it's

Speaker 0: 01:07:11

always hot.
So this is the part that people don't get about like HSMs, generally speaking, is that, you know, banks have been doing this forever.
They have essentially spent policy.
HSM is a hardware security module.
It's essentially a server that's made secure.
It costs a lot of money and a manager needs to go and tap on it or multiple managers go to tap on it and the thing turns on, turns off and you can add more spending policies that have been audited.
Let's put it this way.
And you know, that's completely unrealistic for Bitcoin, right?
Because banks have, they can do backseas.
They can roll back.
They get hacked all the time, but they get to roll back because it's just fiat, it's just IOUs, right?
They call the bank, the receiver bank and say, hey, you know that money, yeah, that was hacked, send it back, right?
And they just change their ledgers and it's great.
With Bitcoin, the money's gone.
So, you know, We don't have a way of doing that in a secure way.
Any server that is hot on Bitcoin is a matter of time before it gets hacked.
And also, maybe the controlling keys that may not be able to, maybe they can't hack the server itself, but they can maybe change the policies with some other key.
So go ahead Antoine.
Antoine

Speaker 3: 01:08:19

Chouchard-Lambert But yeah, I know exactly what you say.
It's just that it's trade-off and you need to be willing to get into the assumption that the transaction is actually going to get confirmed before the end of the delay.
Because with an HSM, the policy is actually enforced every time, as long as you trust it.
But with pre-signed transactions, the policy, there is no single point of failure, but it might not be enforced if people are trying to fuck with you by filling all the blocks, for instance.
It's the outpriced you out of the block space.
And so you might want to consider having high fear reserves.
And if you have high fear reserves, it means that it's only for very high value vaults.
And well, no, I mean, you might consider having large delays, but then you want only to have large delay for large value spendings.
So you might only use vaults for very large value, But then it's going to be a huge incentive to price you out because it's one transaction.
If you get to send so, you can steal, essentially.
So, yeah, it's a tradeoff.

## Watchtowers and handling blockchain information

Speaker 0: 01:09:27

How would you handle sort of like, you know, some Watchtowers or something, right?
Like you need something watching the stuff and let you know what's going on, right?
It's not like the blocking is gonna call you.
So How would you how would you do this?
Because you know again, you need to know that something happened to the coins

Speaker 4: 01:09:43

Yeah, so Like many things with this proposal, there's a lot of optionality on the part of the end user here.
And it kind of depends on how much you want to actually trust the watchtower, right?
Like if you have full trust in the watchtower, you can basically just hand it the location of the vault or some descriptor that tells you where all the vaults are, and then the information necessary to actually do a recovery transaction.
And the risk there is that if the watchtower turns on you, they can just sweep all of your coins into the recovery path, which might be annoying.
I mean, you're not gonna lose the coins, but it just might be annoying because your recovery path is presumably difficult to recover because it's difficult to access.
If you, on the other end of the spectrum, if you don't trust anything at all about the vault, I mean, about the watchtower, You could give it some compact block filter-like object or a bloom filter-like object, and it would basically alert you every time it saw something move on chain that might be one of your vaults.
So there would be a lot of false positives and you would have to have software kind of running on your end that's like getting notified and then checking, okay, well, you know, is this actually an out point that I care about or not?
And then there's like a whole range of stuff in between there.
Like one thing you might do is you could give the watchtower some information that's encrypted with other information that's only revealed when a vault is being unvaulted and then it could, you know, kind of intervene and broadcast.

Speaker 0: 01:11:16

That's more like a flag, right?
Like if this flag is raised, you know, I see the flag.
And what's cool about this is that it does not review amounts.
It does not dox UTXOs, none of this stuff really, right?
It could be easily done in that way because you don't want the server knowing how much coins you have, what the UTXOs are, because all those things, it's like when bad, if bad guys don't know how much money there is, they're less likely to do something.

Speaker 3: 01:11:41

Yeah.
And also James mentioned with trusting one watchtower on it, but you probably want to have several of them as well because and then it gets into issues with the few reserves as well because You might not trust only one watchtowers and not trusting it is not only that there might be many issues but it might just get compromised and compromising for watchtowers is not actually getting control of the servers, just cutting internet access and it just can't enforce the policy anymore.
So you might want to have plenty of watchtowers but for each of them you want to have different fear reserves because if there were two shares of fear reserves then one of the main issues watchtowers could actually steal the funds from under the other watchtowers.
So you need to duplicate all the fiat reserves for the actual enforcement on all the watchtowers.
So it really needs to be high value vaults again.

## Fungability concerns

Speaker 0: 01:12:35

So like another sort of like thing that came up during CTV was like, you know, is there a concern for Bitcoin's fungibility, actual fungibility, not sellability, right?
So like, you know, now you have this coins, they're kind of trapped in this things.
And, you know, are we creating some new sort of incentive structure that we maybe don't understand, right?
I mean, like, you know, Taproot gave us dick butts, right?
On the blockchain.
So like with every new feature, right?
I mean, like you could get dickbutts.

Speaker 4: 01:13:06

So I hope that becomes a term of art.
I hope you know.

Speaker 0: 01:13:09

Yeah, I mean a hundred percent I want dickbutts to be the representation of possible Bitcoin surface attack.

Speaker 2: 01:13:17

So It really sums the whole thing up.
It does, right?

Speaker 0: 01:13:20

Dickbutts and the blockchain.
So that's what Forex block size increase, which is the original SIN in my view, gave us in conjunction with this other amazing thing, which was Taproot that removed the script limit on The Witness.
And it's also discounted, right?
So you have discounted big blocks with dickbutts.

Speaker 4: 01:13:41

Sounds like a porn.

Speaker 0: 01:13:43

It does, right?
You know, like, have you guys thought about like some of this dis-fungibility more sort of like economical concerns around this?

Speaker 4: 01:13:52

I think with vaults it's pretty minimal.
I mean the classic concern that everybody has with recursive covenants or in other words covenants that can continue indefinitely is like, oh well, you know, if we have that, then you know, they're going to roll out GovCoin tomorrow and you know, all the, I'm going to have to get a signature from the Treasury Department to spend my coins, and oh, God, it's gonna be horrible.
The reality is that that's already possible today in a way that's much more convenient than covenants would be.
You know, we have multisig.
So if tomorrow the government orders Coinbase, you know, to have all their withdrawals encumbered in a two of two, then we're already toast anyway.
So I think covenants don't really add any risk in that sense.

Speaker 3: 01:14:36

I talked to that.
So I agree with you, James, but I talked to people that actually don't buy these arguments, saying that actually reversing the policy is would be a hard fork with Covenant but would not be with MaltSig.
I think that's a criticism that the issue is even beforehand.
If you're opting in, like with a Covenant, you need to opt in, you need to send your coins into it.
So if you are opting in into a covenant, you might even opt in to the government altcoin in the first place.
And you might opt in to not using Bitcoin.
If they can force you to use the government covenant, they can force you to use their own currency.
So I don't think it's a concern in the first place.

Speaker 0: 01:15:19

You know, I always like to say that the state actors like to do the low friction approach, which is just knock on your door, you know, drag you to some very uncomfortable place and just say, hey, listen, give me the keys or you can't leave.
Right.
And most people try to stay there for a little bit of time and maybe you're just very, very good at staying there a little longer.
But eventually, you know, people will sing.
Right.

Speaker 4: 01:15:45

Yeah.
They're much better at doing that than writing Bitcoin script.

Speaker 2: 01:15:49

Exactly.
Well, and especially like two things that I think a lot of people miss when they're worried about the GovCoin covenant encumbrance.
One of them is exactly what was just said, which is, you know, when you generate a receive address, your receive address has to commit to the covenant in order for your coins to now be encumbered by the covenant.
So if I just generate a plain old, you know, pay to taproot single sig address, then you, like, you can't send me coins that I now can't spend because I didn't commit to the covenant.
That's one thing that's important to understand.
The other thing that's really important to understand is that if you use covenants to enforce some kind of whitelisting mechanism where coins can only be sent to people on the list and if you eat too much beef this month then you can't spend your money.
Like whatever the doomsday scenario is.
Anytime you want to change the contents of that list or the semantics of that list, you have to regenerate the covenants.
And so from an operational perspective, it's a very not scalable solution.
Something like having a co-signing server and having all your coins encumbered with a two of two multi-sig is way more scalable because some bureaucrat can just push a button and add or remove entries from the list and then that list goes into a policy enforcement engine that decides whether or not to co-sign a spend.
That's actually how people would build things.
There's actually a product from Blockstream called AMP that does exactly this thing for registered assets.
So if you want to go and play with it, they have a demo site and you can issue yourself a restricted asset.
But yeah, and then to NVK's point, all of this stuff is moot if they just drag you out of your house and put you in a box and say you're using, you know, GovCoin now, right?
Like, so the Covenant thing, I think, is a little bit of a red herring.
And it's, it's not a good argument.

Speaker 0: 01:17:40

I think, you know, once you sort of like get into a little bit more practical flag theory as well, you know, you start having the recovery, for example, nuclear keys and XORed in two separate different countries.
And listen, if you have enough money that you are a person of concern, a prescribed person or whatever, however your state actor like to call these people, you know, you probably have a little bit more means and you're going to probably start sort of like distributing yourself outside of single jurisdiction and provably too, right?
So maybe, you know, if they point the gun at you, you know, that vault that was not touched just disperses to your Monaco PO box, right?
And there's nothing they can do, really.
These things get a little sort of like, they get weird very fast.
I'm not very concerned about state actors.
I guess my concern is more like, do we have some blind side on some economic nuance that gets missed?

## Drivechains & CTV

Speaker 3: 01:18:46

Maybe drive chains.
I don't know much about drive chains, but it's something that has been...

Speaker 0: 01:18:52

Not going

Speaker 4: 01:18:52

to happen.

Speaker 3: 01:18:52

...Asked people.

Speaker 0: 01:18:55

You know, like, and maybe I should just bring it up, like the CTV.
I absolutely love the work that was put into BIP119 and like, and Ruben, absolute brilliant kid.
But I think, you know, a lot of people don't like this, but you know, Bitcoin is still people.
People change software.
And 100 years from now, it's going to be different people.
So they may change the software very differently than we do now.
But you know, once you burn yourself sort of like politically to the economic nodes, which are people, I find it extremely unlikely that you can do things, especially if they're very complex and they sound like some crazy shit that people can't understand, like CTV.
So you know, drive chains changes a lot of incentives, a lot of complication on Bitcoin.
I like to call it soft fork hell.
Because essentially that's what it is.
It's just going to soft fork Bitcoin for infinitum, right?
And then CTV is like absolutely amazing, right?
But God knows, man.
I mean, like it's just like, I don't think my brain can comprehend what can be done with that thing to be able to say like with some, at least feeling confident, like it's not more than just dick butts.

Speaker 4: 01:20:03

I think that's the thing, you know, with, with, I mean, so CTV, like you said, it's a very small patch set, but to your point, evaluating something like CTV, evaluating like Opcat, like these are very, they're simple mechanisms that can build a lot of different stuff.
And the conceptual surface area of what can be built is a lot higher than a proposal like check, lock, time, verify, or op vault, where You can fuzz test the shit out of the interface and be reasonably certain that you've like kind of exercised the full span of the space that it enables.
Whereas like with these more open ended things, it's harder to get an intuition for what's actually possible.

Speaker 0: 01:20:49

Sorry, somebody dropped some bait here on the chat.
I am not gonna open any link that has drive chain on the URL.
There's just a

Speaker 1: 01:20:57

blog post from Jeremy Rubin where he showed like you could kind of recreate drive chains with any preval.
So like, I mean, I'm a big fan of any preval.
I think there's a lot of cool things, but I am not a fan of drive chains.
So it's, you know, there's a lot of weird things like this.

Speaker 3: 01:21:11

Yeah, exactly.
And we see it here as well.

Speaker 0: 01:21:14

Yeah.
It's Funny, the people who have a more sort of like flexible, big composition space mindset really gets drawn to this.
Like you see this with like Fiat Jaff as well, big supporter of that, creator of Nostr, right?
And Nostr is like the complete opposite of Bitcoin.

## Unforseen consequences (ordinals)

Speaker 0: 01:21:32

It's like rough consensus, but it's simple, very flexible.
That's not added a lot of rules.
Because also it's trying to do something completely different.
And I think Galaxy Brain sort of starts to get a little lost in what's acceptable to a certain purpose versus another.
And a lot of the pushback into new features and things on Bitcoin comes from this sort of like, hey, can we not break this incredible amazing thing by just adding this one more thing that we really want.
Maybe this is a good segue to sort of start thinking like, OK, great.
Let's say upvault, like extreme low risk, at least it is in my view, adds an incredible amount of security that Bitcoiners are going to need.
You know, if we don't want to go to jail or get killed for our coins.
And I think that on itself is the sale pitch.
It's like, listen, you don't want to get killed, kidnapped or like arrested, right?
For your coins.
Like you want to have a peaceful sleep at night technology.

Speaker 2: 01:22:31

Without enabling DickButts.

Speaker 0: 01:22:33

Exactly.
Without DickButts.
Well, we don't know yet.
Maybe.
I don't know, man.
Casey, brilliant guy.

Speaker 2: 01:22:38

Super creative.

Speaker 0: 01:22:39

You know, he's he's going to find a way of like DickButting, you know, internal contract.

Speaker 2: 01:22:45

James mentioned this earlier.
Ordinals are compatible with vaults.
So you could vault your dick butt.
Yes.
Like it doesn't create new dick butts, but it does create new ways of securing your dick butt.

Speaker 0: 01:22:55

By the way, we're doing an episode on ordinals.
Rindell is joining me.

Speaker 4: 01:22:59

Are you going to have Casey on?
Yes.
Oh, that'll be fun.

## Activating OP_VAULT

Speaker 0: 01:23:02

Probably next week.
So anyways, how do we activate this?
How do we convince people?
How do we?
Because we can't even agree on how to activate shit.
And as I like to say, it should be excruciatingly horrible experience to try to activate anything, to discourage even the most hopeful people to not do it.
Because, you know, activation is the ultimate bad attack surface of Bitcoin, right?
Like it's adding shit to it.
So like, how do we go about maybe activating this thing?

Speaker 4: 01:23:30

Just a few thoughts.
I mean, I don't want to play a massive role I mean, I don't want to unilaterally push this thing obviously because that just doesn't doesn't work But you know My hope is that the value will be so obvious and and that there will be people who take time to evaluate the proposal like you, like Alex Leishman did a lot of tweeting a few days ago, the CEO of River, about how valuable this would be.
I think the people at NYDIG are pretty positive on it.
And so I just hope there's kind of like this overwhelming sense of like, wow, this is pretty low risk and pretty high value.
And, you know, it's something that we want.
And the other note that I'd like to make is like there was a time where for things like check clock time verify, check sequence verify, like these were like purpose specific tools and their activation wasn't full of drama, wasn't this huge massive thing that people freaked out about.
And we actually did those like, you know, in rapid succession kind of around SegWit.
So I kind of hope, you know, I mean, Segwit and Tapper have been very profound, complicated changes that have been, you know, I think generally positive massively, but...

Speaker 0: 01:24:39

It's a full change to Bitcoin.
We added a new crypto piece.

Speaker 4: 01:24:42

It's like a platform change.

Speaker 0: 01:24:44

It's a

Speaker 2: 01:24:44

whole new thing.

Speaker 1: 01:24:45

By the

Speaker 0: 01:24:45

way, I want to do an episode on just explaining people what SegWit actually is.
I don't think people understand.

Speaker 2: 01:24:50

It's so crazy.

Speaker 0: 01:24:52

And VBytes and all the stuff we did that nobody understood.

Speaker 4: 01:24:57

Completely.
Look, like I work on core as my full time job and I have to routinely reread, you know, the BIPS for SegWit and Taproot because I forget all the details, and I forget all the nuance.
And when the ordinals and the inscriptions came out, I forgot that Taproot had removed the 10,000 byte limit on witness scripts.
So these changes are massive.
Abvol, not massive.
And I hope activation can be,

Speaker 0: 01:25:23

you know.
So maybe the way we start addressing this is to explain that this is a gardening job.
This is not a construction job, right?
I mean, like, we're adding a small primitive, right?
It's just like, you know, all the little things that we do.
Because again, people don't understand the difference between the little things and the big things, right?
Maybe drawing sort of like analogies to like, you know, like for example, lock time verify.
You know, like, okay, so this one did this, you know, up.
Vault is going to do this, right?
And not sort of blow this thing up out of proportion, not try to say this is a massive feature, even though it does enable a lot of things.
I think how we frame this and how we sort of like start addressing the people that don't want changes, because, you know, they're kind of right.
I mean, we don't want changes to Bitcoin.
We want just at least in my view, gardening.

Speaker 2: 01:26:10

Well, and like something that I'm cautiously optimistic about here is I think a lot of times when people have software proposals, they end up in a chicken and egg situation of trying to prove demand, where it's like, somebody's like, oh, I want to build this new opcode that'll let us do coin pools.
And I think a reasonable pushback is like, well, no, like demonstrate in the market that people want that.
Show that there's enough demand that it's worth the dick-butt risk to go and build coin pools.
I think what's cool is that because you can build vault-like setups that have a bunch of trade-offs out of things like pre-signed transactions, ephemeral keys, and relative lock times, like people like Re-Vault and other groups can go and build products in the market, have customers, and then say, hey look, even with these trade-offs, people want solutions that are shaped like this.
Wouldn't it be great to be able to just eliminate a whole class of these trade-offs and have it be enforced by consensus rules instead?
And that might be a more compelling argument to the economic majority than just saying like here's a really great idea that I have.

Speaker 3: 01:27:14

Yeah I agree with that it would be useful for arrivals, but two things, first, I really don't want to be into pushing for consensus changes for my company.
And two, I actually don't think we should, well, not rush, but I don't think we should go with activating anything, well, not too soon.
So there's been a lot of covenant proposals floating around.
People are still working on covenant proposals that are not announced yet.
There is a lot of research going into it.
So I think it would be premature to activate anything.

Speaker 0: 01:27:48

What would be the least disruptive way of getting this in?
Even if it was like maybe like not fully featured?

Speaker 1: 01:27:56

I think something to keep in mind as well is like we don't have to do OpVault and that's it for Covenants.
Like we could do OpVault and TTV and APO.

Speaker 0: 01:28:03

No, I know.
I know.
I know.
But like...

Speaker 1: 01:28:04

It's not going to be all at once.
Yeah.

Speaker 0: 01:28:06

The way that the people like if you use some EQ here, right, the way that...
A lot's true.
Yes.
Listen, like Bitcoin is politics.
It's people and you have to convince people.
So this is why I'm asking.
It's like, what is the best way we can sort of like dip our toes into this?
Or like, how can we propose like a way of activating this that is like not a big deal?
Because it's not a big deal.

Speaker 4: 01:28:28

Yeah, so I mean, I was writing the bit before I got on this call.
I want to put that out there.
The implementation, frankly, is mostly complete.
There's a rich suite of functional tests that I've got to add some stuff to, but largely I've written a wallet, basically, to functional test this thing.
So the implementation's all there.
You can see exactly how it works.
So my hope is that I can put it out there and people can spend time getting familiar with it, maybe sketch out some, really do some in-depth thinking on what the use cases actually look like for end users.
And then hopefully it just becomes obvious that it's something we want and we activate it with a speedy trial or something like that.
But I think Antoine makes a good point about not activating too quickly, but I do wanna push back a little bit and say, look, I'm not wedded to OpVault.
I came up with it, like it originated as a thought experiment.
I just wanted a benchmark against like, what would the perfect vault construction be?
I wasn't even thinking about implementing it.
And then I was like, oh, you know, I should give it a shot.
And so I tried to implement it And it worked.
But if something comes around that's categorically better, I mean, I'm happy for that.

Speaker 0: 01:29:35

That's often how it works.
I mean, Toproot had like 50 different sort of ways that sort of went here and there.
Segwit was the same thing.
These things are never like the original proposal who really makes it.
Yeah, right.
And that's why I sort of like, I guess I brought it up.
You know, maybe there is like a version that's like feels like more like a compromise.
It sort of like feels like a little bit more restrained.
And that's how you kind of start to get it in.
And then maybe it gets more featured as it comes closer to activation?

Speaker 4: 01:30:03

The point that I wanted to make, though, is that custody is a real problem right now.
I mean, people are losing coins.
Insurance is basically not doable.
The situation right now is pretty bad, and we're all used to it, and so maybe we don't realize how bad it is, but it could be a lot better.
So I'm not really wild about the prospect of waiting three years for some ultra-perfect covenant proposal to come along that like maybe kind of emulates OpVault.
You know, I think I'd like to put the proposal out there, see what the objections are.
And if someone is like, hey, I really don't like that we can, you know, do this DLC thing with

Speaker 0: 01:30:46

the pack.
You know, if I have to like, sort of like really address what I think it's gonna happen, is that it's not gonna necessarily, I don't think the criticism is gonna come regarding the actual nuances of OpVault or OpVault.
It's gonna be activation.
Is the idea is like, the problem is, I think Speedy Trial like pissed off enough people.
Yep.
And it was kind of like felt rammed through by the cabal of core developers.
So there is that bad taste in the mouth of a lot of economic nodes out there.
The dick butts certainly did not help.
And I still think we don't have a good way of activating stuff.
And we sort of like, we're a little PTSD from things.
So it's not going to be upvote.
It's going to be like, I don't want to change Bitcoin.
Right.
So and I think a lot of the people who criticize changing Bitcoin, they are correcting the sentiment of not wanting to change Bitcoin.
But they don't also don't understand that like software doesn't live forever without gardening.
Like, you know, the stuff that's running on your computer today doesn't run tomorrow.
And you need the people who understand the code base to sort of upgrade it for new hardware, for new concerns, for, you know, Unix time problems.
And there's all these things that need to change.
And you know, when my good friend Steve says, fire the devs, I understand why it feels that way.
And I kind of agree in a way because, you know, like core, I addressed this in the last episode.
It kind of feels like this, it's like Internet Explorer has 99% of the market.
It doesn't rule the internet, but kind of rules the internet.
And, you know, it has this sort of like bad taste by the CTV people as well, where, hey, if you don't get the right people on court to like your idea, It doesn't get activated to you.
So these are the gatekeepers.
But you know, like realistically speaking in software, like there's always just like a literal handful of people who understand the whole banana and are the people who are qualified to truly have an opinion.
You know, like Facebook used to have five guys merging the code of 5,000 people.
You know, in our shop, like we have, you know, Doc Hex.
And if he doesn't get through his shit, like it's not going to get through.
And very few people have the full picture of that cold base.
And those people are often not the best people who are selling themselves or selling the cold.
So I think like Bitcoin is sort of like suffering at this right now.
Like that's the current sort of like cold and sneeze that Bitcoin has.
And, you know, maybe OpVault is the simple thing that helps us find a better way of activating things and sort of talking about these things.
So maybe James, like, you know, you're very good at sort of like tech and also dealing with people.
Maybe you should champion this.

Speaker 4: 01:33:36

Well, I appreciate you saying that.
And I'll champion it to the degree that I don't feel like it's actually impairing the proposal.
Again, I don't want to Feel like I'm pushing this really hard and and I want to be clear I'm totally agnostic about our activation parameters to be to be frank.
That's not something I've thought a lot about so I Don't really care exactly how the activation works there are probably other you know galaxy brains who can weigh in on that and suggest some stuff.
And maybe this process will motivate me to kind of play a bigger role in that and try and understand some of the different approaches a little bit better and the objections that people have.
But I think you're totally right there right now.
Bitcoin is a little bit wandering in the desert.
And, you know, the last two massive changes have been led by a real small group of people.
And I think we all have this muscle memory of kind of relying on them to sort of say, okay, This is the blessed next step for Bitcoin.
And I think they very rightfully realize that that's not healthy.

Speaker 2: 01:34:36

They earned that.

Speaker 4: 01:34:37

They earned it for sure.

Speaker 0: 01:34:38

I mean, listen, how many people in the planet can actually review LibSec?
Like, seriously, like two?

Speaker 4: 01:34:47

Yeah, yeah.

Speaker 0: 01:34:48

I mean, like fully, fully, fully, fully understand what truly is going on in there.
Like, I don't think there's more than two people.

Speaker 4: 01:34:55

It's not a lot.
It's not a lot.

Speaker 2: 01:34:59

You can definitely count it on one hand.
Like, you could argue if it's two or four, but it's definitely on

Speaker 0: 01:35:03

one hand.
But this is like, I think we do a very poor job at representing the technical problems to people who are not technical.
Like just conveying these realities, right?
Like, you know, people in this space, you know, like my NCAP comrades, sort of like love to talk about meritocracy and things like that.
But, you know, part of the meritocracy understanding that you have absolutely no fucking idea how Bitcoin works.
And you have absolutely no qualification to also understand what they're trying to change.
And there is always going to be a little bit of this sort of like bad taste of a technocracy, Right?
And it feels weird in Bitcoin, right?
Because it's your money, it's your node.
But you're trusting somebody else's code, especially if you can't read the code.

Speaker 4: 01:35:53

Totally.
And it's like the, oh, I'm sorry.
Did you?

Speaker 0: 01:35:57

No, no, no.
Go ahead.
I was like, how do we improve this?

Speaker 4: 01:36:00

Well, I was going to say, the situation that it's very much like is taking your car to the mechanic, right?
Like you take your car to the mechanic, this guy knows what he's doing, but there's also a good chance he's trying to screw you.
Like there's also a good chance he's trying to charge you, you know, 20 to a hundred percent more than you actually pay, maybe do some unnecessary work.
And so you're in this awkward position where you can't do this work yourself.
You can't even evaluate the proposed fix.
But you also don't want to get screwed.
And as we see in medicine, there can be situations where the group of experts is dead wrong.

Speaker 0: 01:36:34

Or they're sold out.
I mean, there's a lot of different interests in Bitcoin.
We don't know people's motivations.
It is realistically impossible to know them.

Speaker 4: 01:36:43

Right.
So it's important to retain your bullshit detector.
It's important to retain the culture that makes sure that no change in Bitcoin violates the property rights of the system.
But at the same time, I think the best you can do if you're not a technical person yourself is like you go out and you consult a lot of car mechanics, right?
You get a lot of prices.
And I mean, that's kind of the best that we can do.
But I don't know if you guys have other thoughts.

Speaker 2: 01:37:06

Well, I mean, so another thing that is a relatively recent development is I think AJ set up Bitcoin Inquisition, which is, you know, like let's proactively merge different software proposals into a SIGNET so that people can play with them on a shared network.
And so unlike some of the more ambiguous, ambitious big change proposals, Because OpVault is really targeted at a very specific shape of use cases, maybe there's an easier path here of it ends up on something like Bitcoin Acquisition, people can build little dummy wallets, and normal users can get a little bit of stick time playing with what would custody in a post-op vault world look like and demonstrate that this is better.
Even if you don't know whether or not the mechanic is trying to screw you, you can at least take it for a test drive first.
There might be some stuff like that where it's less about how do we go and win the rhetorical fight on Reddit, and it's more about what can we do to incrementally de-risk their proposal so that the community understands what they're signing up for.

Speaker 0: 01:38:16

I mean, there was a lot of that at Taproot, right?
There was a lot of sort of working groups and things like that.
But Taproot still felt pretty like rammed through.
I mean, I went

Speaker 2: 01:38:24

and found like Optech did a workshop on Taproot, I think two years before activation.
So like, you know, You could write code and watch videos about Taproot, but people still felt like it was sprung on them.

Speaker 4: 01:38:36

Taproot is just so hard.
It's so hard.
It's so hard to get your, I mean, I had to really, the only, I until very recently didn't, I feel like, fully understand Taproot.
For this proposal, I had to write a bunch of tests that's all on taproot and there were things that I just kind of didn't understand.
I found it pretty difficult to get sort of valid taproot constructions and I basically relied on sort of the example code that other people had written.
So it was, you know, it's a very, again, I'm massively positive on Taproot.
I think it's awesome, but it was like so difficult to get your arms around, even as a deeply technical person.

Speaker 3: 01:39:13

I wanted to address as well, you said that it was a small group of people, but while

Speaker 0: 01:39:16

it's true that it was

Speaker 1: 01:39:17

a small group of people

Speaker 3: 01:39:17

but why it's true that it was a small group of people that coded for Tapwritz, I found that it was there was a lot of demands and they definitely set a high bar.
Well there was a lot of demands, a decade of research.
When did we start discussing Merkle scripts?
2012 or something?

Speaker 2: 01:39:38

Years ago.
Yeah, a decade of research,

Speaker 3: 01:39:40

a lot of involvement of a lot of people in the community with the workshops, a lot of involvement with the activation, and maybe that's why as well people are happy with it because they were actually involved.
And so, yeah, I think that did put a very high, not high bar, but reasonable bar for community involvement and normal user involvement.

Speaker 2: 01:40:03

Well, like Shnor is injured for a similar thing.
Like people have been wanting Shnor in Bitcoin for years.

Speaker 0: 01:40:08

See, like, you know, the Shnor is funny that you brought that up.
Like, you know, it's always been a concern of mine that like, what if ECDSA is backdoor?
Right.
And it's not revealed for a long time and there is no proof for for ACDSA.
So, you know, the idea of like, and again, this is a fundamental change to Bitcoin, right.
Adding another crypto primitive, it's like crazy different.
So, You know, but just having a secondary fallback crypto primitive in Bitcoin before we're big enough to state actors are going to that extent.
Right.
It's pretty cool.
Thanks Antoine.
Antoine is stepping out.
Appreciate it.
But now, like, you know, we have this sort of like the fights have always been hard, you know, up return limit back in 2009, 2010, because people were concerned about the worst part of dick butts.
And then you had, say, P2SH was also a huge fight.
The original block size changed from 32 megabytes to one megabyte.
You know, SegWit was a bamboozle of most people.
People did not understand that the block size increased.
I don't know, I just hope that this one is not part of the contention.
We can find a path where this is the gardening sale, not the construction sale.

Speaker 4: 01:41:22

I think the point Ryan Dell made is so good.
And what I love about the idea of people taking this for a test drive en masse with Inquisition is like, that gives technical people who maybe don't want to work on core or don't have time to work on core, can't, like they can write tooling to kind of make this an easier process to be able to experiment with this stuff more easily.
So I just love that idea.

Speaker 1: 01:41:48

I think something to keep in mind too, like MVK, you just went through all those different soft forks, like from like the original block size decrease to like stuff like segment tab rates.
Like You didn't mention like CLTV or CSV or like BIP66 I think or 68.
Like there's tons of BIPs that are like worse off works that are just like are just normal things that happened and no one cares because they're like simple small upgrades that are super effective.

## Chain ossification

Speaker 0: 01:42:15

Let's see, here's the thing.
As Bitcoin grows, right, and we have more people with their bags depending on it, the more you're going to have screech.
And that's a feature, right?
Like, you want this to progressively become more immutable, even as a feature set.
So like, you know, I think we're still in a place where like a few things could get in, but I don't think we're far from like, you know, like a true ossification of new features.
Unless, you know, like people come up with some more clever way of testing them out on main chain.
I don't I don't see how how this gets much easier.

Speaker 4: 01:42:51

I just think it's just to spice up the conversation and throw in some opposition.
I think the counterpoint to that is that I'm really worried about some future where Bitcoin, the scale of Bitcoin is limited to what we have today.
And it becomes this gold like asset where you as a regular person, as a non-institution, you can't actually take custody of your Bitcoin.
I just think that's a failure mode Because at that point, it's just like maybe a slightly better gold that develops a paper market, gets captured by governments to some extent, re-hypothecated, all that stuff.

## Bitcoin vs gold - attack vectors

Speaker 0: 01:43:23

Yeah, I mean, can we just recognize that gold lost?
You know, it had a 5,000 year run, right?
And it's like, it is an element.
It is a fucking like, you know, universe element.

Speaker 2: 01:43:38

It conducts electricity really well.

Speaker 0: 01:43:41

I mean, just like this thing lost, an element lost, right?
To human ingenuity, right?
The MMT guys are smart as fuck.
And they will find a way to try to gain Bitcoin.
I mean, FTX was a fiat maxi attack on Bitcoin.
They inflated the Bitcoin supply by, what, 20% for the epoch.
It's crazy.
It's absolutely crazy.
And Bitcoin not inflating is the whole fucking point.
So like, you know, we're going to have to create defenses against fiat attacks.
It's not going to be the guy using the backdoor on ECDSA, extremely unlikely.
Right.
Like it's going to be like how they they capture, you know, 60% of the Bitcoin custody in Coinbase.
And then they start inflating that.

Speaker 4: 01:44:30

Exactly.
You know, because like, look, changes that happen to Bitcoin consensus are in the open there that you can you can look at the Code you can judge it for yourself So if someone comes along and tries to change the supply schedule or the inflation rate like that's obvious And that's not gonna be a very effective attack on Bitcoin for that reason.
It's going to be exactly what you're describing.
It's going to be on these higher layers on the Fiat on and off ramps.
Like if they want to antagonize Bitcoin, like hiring an open source developer to go and try and sneak some change in is going to be totally ineffective.

Speaker 0: 01:45:00

I mean, you know, Operation Orchestra is in full effect, right?
Like, let's waste everybody's time with stupid shit.
But think about the whole game that just happened against Bitcoin, right?
Total price suppression, coordinated or uncoordinated.
So you have the Fiat Max is doing and come on state backed like FTX, right?
Like inflating the supply.
And then you have CME adding all the possible ways for you to short Bitcoin.
And then they don't give us a spot ETF to call these motherfuckers up.
Right.
So, so like, you know, and Bitcoin is extremely illiquid.
Right.
Like, I mean, you have like it on spot.
Right.
Like you have like 10% of all Bitcoin supply available on spot.
So like you can't call their bullshit.
And like, you know, if you just think about that for a second, it's like, holy shit.
And this is not even like how far these guys can go.
I mean, this is like this is a Sunday play for them.
Right.

Speaker 4: 01:45:58

Absolutely.

Speaker 1: 01:46:00

That's also today, like it's something like only like 10 percent of all Bitcoin is custodied on these institutions.
It gets worse without Bell, so you can't reasonably custody lots of Bitcoin safely.
It's going to move more and more and more on the coin base, and it becomes an even easier attack.

Speaker 2: 01:46:16

And what's the natural market response?
Oh, well, I can't actually move my Bitcoin because it's too expensive because it's like locked up with 50 HSMs. So instead what I'm gonna do is I'm gonna transfer a paper claim on my Bitcoin, which is custody at this institutional custody solution.
And then you just start rehypothecating Bitcoin.

Speaker 0: 01:46:33

Well, that's exactly what happened to gold.

Speaker 4: 01:46:35

Bingo.
But NVK, you know, to go back to like your point, I mean, it is vitally important that we maintain this culture of not changing the premises of Bitcoin, not changing the property rights.
And so people have to develop the ability to distinguish changes that are even remotely close to challenging that versus these gardening changes where it's like, yeah, you can completely understand this feature.
It's not going anywhere near the viability of the system or the premises.
And, you know, it's really I mean, Bitcoin is like America and America relies on the founding documents, the frameworks that are tangible, but it also relies on the cultural ethos of like pushing back on ambiguous situations that challenge the premises of the system.
So I totally believe like, you know, we need people out there who are skeptical, but you need to have the wisdom to be able to differentiate between things that are gonna help the system versus things that challenge its premises.

Speaker 2: 01:47:27

Yeah, I mean, like one of the longest running debates in Bitcoin, which is like, I think one of the juicier debates is should Bitcoin be money or should it be smart contract fuel?
I think that anytime somebody tries to introduce a change that allows for more expressibility of script or allows for more novel peg-in mechanisms or whatever, one of the pushbacks is, okay, well, Bitcoin isn't for arbitrary program execution, it's for money.
What's, you know, hopefully the thing that people can distinguish is that OpVault or something like it is doubling down on custody.
Right.
It's making the money part better.
Right.

Speaker 0: 01:48:03

Yeah.
You know, like my rule of thumb for Bitcoin, sort of like very, very grub brain, like sort of framework is, you know, every single Bitcoin feature serves at the store of value pleasure, right?
Like that's the king, right?
Anything else you add in Bitcoin is for that.
Bitcoin having uncensorable transactions, it's because without that, you don't have a store of value, right?
Because somebody can just make you not spend or take it from you or block you.
So some privacy is for that, so that you have the privacy to transact your store of value.
So you protect the store of value, right?
So Every single change and every single thing that I see people trying to add to it, does it like really fit that box and it's a small box.
I think that was one of the original sins of the CTV sort of like frame narrative.
It was like sort of unleashing this galaxy brain into sort of like, look at all the cool shit they can do.
Oh my God, this is amazing.
Right.
Like it's like, that doesn't really help with store of value.
So like go fuck yourself kind of thing.
Right.
Like, and I think they're like, if we can just like help people who are like, who may be on the fence or who may be against this proposal, for example, just understand that like this does fit that small box.
Like this is like it's in the name and like this thing is to help you hold your coins and have property over your coins and not be capturable, I think this would move sort of like fairly fast and fairly straightforward.
And if we have more criticism that is like completely stupid and retarded, at rest is even better too, right?
We need to get things that are completely absurd at rest and raised even by us.
It's like, oh, what if SHA-256 is broken?
Well, I mean, airplanes fall from the sky, Right.
Everybody can understand that.
So like, you know, 51% attack every all time high.
It comes back to Bitcoin.
Right.
You know, oh, you know, it's not like that.
Right.
So like you have to have this sort of like very attainable China.
You have to have this very attainable, very like drug brain explanations of things because my pocket doesn't care about how complex and cool Bitcoin is.
You know, I don't want to have to think too deeply about these concerns with my money.
And I don't know, I feel like you've been doing a very good job from the things I've read and sort of seen about OpVault.
And I just, yeah.
I guess that's where I wanted to do with this episode, is sort of like address it, see if we can pursue some paths here, reflect a little bit on it.
Is there like anything else you guys feel like we should address it or that we missed?

Speaker 4: 01:50:50

I think we kind of hit on most things that I can think of.
But yeah, I'm just really thankful, you know, for the opportunity.
Like it was a great group of people.
And You know, your analysis is really important to me because I think you're one of the best people that's set up to kind of evaluate something like this.
And so all I want is just kind of a continuing exchange of, you know, Does this work?
Is this right?
And so I can't thank you enough for all that.

Speaker 0: 01:51:20

No, I mean, listen, man, like I absolutely love the work.
I think you're approaching this with like a good cool head and like the correct humbleness because Bitcoin tend to humble us all in some way or another.

## Further reading

Speaker 0: 01:51:35

It's essentially a kick in the nuts every day.
So like, you know, thanks Rindel and thanks Ben.
You know, your contribution here was like super, super amazing.
Thanks Antoine, who had to leave a little early.
So guys, I guess like any final thoughts and maybe like further material for people to read, that would be great.
So Rindell.

Speaker 2: 01:52:00

Yeah, I think Antoine already left, but for me, I think one of the first times that the notion of Vault really clicked was I was actually reading the docs for ReVault.
So if you go to ReVault's page, they have a link about how it works.
And ReVault is really aimed at institutions, so you have to kind of squint at it and imagine how it would scale down.
But I think between that and the paper that James wrote about OpVault, if you read those, I think it kind of plants a good seed in the back of your head to start thinking about what vaults are, how they're useful, and how that could go forward.
So if you're interested in that, I would definitely look at those two things.

Speaker 0: 01:52:40

Thank you.
Ben?

Speaker 1: 01:52:42

Yeah, I just want to say, like, I think off vaults or any sort of a covenant proposal, like should we need this eventually in Bitcoin?
And we have some really good proposals on it right now and we should probably decide on one in the next few years and try to activate it.
This isn't going to be a whole re-architecture like we did with Taproot or Segwit having to like, as Coinbase said, support the setting to this.
This is gonna be super minimal and like a much smaller change set.
So it's not as risky or anything like that.
So I hope people can understand that and hopefully work on activating it.
Great, James?

Speaker 4: 01:53:18

I can say it better than those two guys just did.
So thanks for bringing us on, man.
If anybody wants to find the Vault paper, you can just go to my Twitter at JamesOB.
It's linked right there.

Speaker 0: 01:53:28

Chill it.
Seriously, tell people exactly where to find the stuff and where to read and what they should look into it.
People don't know.
And what should we add to the show notes?

Speaker 4: 01:53:38

Sure, yeah.
So you can access the paper just by going to jameso.be slash vaults dot pdf.
So that's the paper I wrote.
I think it gives a pretty good summary of prior work, kind of a setup for the problem, and then the actual design itself with some nice diagrams in there that kind of make some of the benefits clear.
Then if you want to dive even deeper, There is a full implementation of it.
There's a pull request open in the Bitcoin core repository.
Embarrassingly, I don't know the number because I never remember those things, but it's there.
It's got a lot of functional tests, so you can kind of get a really good sense of what it looks like, how it works, what the transaction structure looks like.
Like I said earlier, I'm working on a BIP.
I'm really hoping to have kind of a final draft that I can circulate within the next week or so after I get a little bit of feedback from people.
And then, yeah, beyond that, I think just, you know, if you have any questions, hit me up on Twitter at James OB and we can talk about it.

Speaker 0: 01:54:36

Just for the record, I mean, James is one of the friendliest people around with one of the biggest galaxy brains that's completely hidden in that pretty face.
So do reach out to him.
And like, I'm certain that he will politely explain things and and try to convey to you without pushing.
And like, you know, really, like if you can't understand this stuff, because really nobody can, You know, reach out to people and try because it is worth it.
We want a Bitcoin future where people don't get robbed or lose their coins.

Speaker 4: 01:55:10

You're too kind, man.
Yeah, absolutely.
Thanks for having us on.
And it was a really Great discussion.

Speaker 0: 01:55:16

Awesome, guys.
Thank you so much.
Ben, I'll see you in the kitchen in like five minutes.

Speaker 1: 01:55:20

Yeah, I'll see you.
Thanks.
See you guys.

Speaker 0: 01:55:24

Take care.

Speaker 2: 01:55:25

See you guys.

Speaker 0: 01:55:30

If you're new to the pod, make sure to listen to some very cool other episodes.
Episode 15 about Lightning, episode 11 about podcasting 2.0 and Value for Value.
And we also had a hardware wallet security panel on episode 5.
Don't forget to follow at Bitcoin Review HQ or get in touch on Telegram, Bitcoin Review Pod or BitcoinReview at CoinKite.com.
We don't have a crystal ball, so let us know about your projects.
Leave your Boostagram on this episode and we'll try to read it on the next episode.
We've added more people to the splits.
Now if you send us streaming sets, some of that go to opensets.org And also to Citadel Dispatch with my guest Odell.
If

Speaker 1: 01:56:30

you

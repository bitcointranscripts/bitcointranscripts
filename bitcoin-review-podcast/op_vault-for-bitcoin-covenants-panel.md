---
title: "OP_VAULT for Bitcoin Covenants Panel"
transcript_by: satstacker21 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=LC3lZ9dMRoA
tags: ["covenants","vaults","fee-management"]
speakers: ["NVK","Rijndael","Antoine Poinsot","James O'Beirne","Ben Carman"]
categories: ["podcast"]
date: 2023-02-11
---
Introduction

NVK: 00:00:40

Today we have an absolute all-star panel here.
We're going to be talking about the Bitcoin OP_Vault.
It's a new proposal by James.
 any new proposals to Bitcoin, there is a lot to go over.
And It's a very big, interesting topic.
So today we have Rijndael.

Rijndael: 00:01:05

Hey, good morning.
Yeah, I'm here talking about vaults, Bitcoin developer, and I work a lot on multi-sig and vaults that don't use covenants.
So really interested to talk about this proposal.

NVK: 00:01:19

Very cool.
We have Ben de Carman, a return guest.

Ben: 00:01:26

Hey, thanks for having me on again.
I'm guessing I'm here because I posted to the mail as well how you could do  the CTV optimization with, for DLCs, you can optimize them with Covenants and I showed how you could do it with OpVaults as well.

NVK: 00:01:42

Great.
Antoine?

Antoine: 00:01:44

Hey everyone, I'm Antoine Poinsot.
I've been working on building an actual vault architecture, which does not use Covenant for the past two years and a half.
Lately I've been working on other projects, but I guess that's why I'm here.

NVK: 00:02:00

And the man of the hour, James O'Beirne.

James: 00:02:03

Hey guys.
I'm a Bitcoin developer.
I spend a lot of my days working on core, but for the last few years, I've been really interested in custody systems and the promise of vaults.
And last year, I actually implemented a similar vault design on top of OP_CTV, which I'm sure we've covered at some point on the show.
But I was kind of dissatisfied with those implementations for various reasons, and so decided to come up with this proposal.
So just want to say that to make this a lively discussion, you should do your best to rip into this and you won't offend me, kind of regardless of whatever you say,  NVK said, any new proposal for Bitcoin has to be kind of shredded apart and scrutinized.
So totally ready and welcoming of that.

NVK: 00:02:57

So guys, there is a lot of confusion because there's a lot of stuff going on in terms of the Bitcoin Twitter drama and Bitcoin list.
I think a lot of people  me had the list muted for a few months due to tail emissions, RBF, there's been a lot of stuff that happened in the last few months.
So I kind of got the vibe that a lot of people  kind of missed OP_Vault, some of the discussions that happened because it was kind of  lost in the noise.
And also sort of  confuses it with  the ordinals and all this other stuff.
 we just posted some questions this morning on Twitter.
And we were sort of  talking about ordinals.

## Overview of OP_VAULT

NVK: 00:03:40

So let's just sort of  box in.
What is OP_Vault?
The elevator pitch first, just so we can get people to just sort of get it.

James: 00:03:49

Yeah, so I guess I can field this one.
To be really brief, op_Vault is basically just a really practical, low overhead way of introducing this way that you can lock up your coins in such a way that if you wanna spend those coins, you have to navigate through this delay period.
You have to wait for the coins to kind of settle, aside from the fact that you can sweep it at any time before that final withdrawal to a pre-specified, what I call, recovery path.
So the idea is, you can set up your coins to have some ultra secure, totally impractical, completely offline recovery wallet, or you could even do something kind of interesting  have a social recovery type thing where your friends hold keys and maybe you need three out of five friend signatures to actually recover the coins or something.
So basically it just gives you a way of introducing, key storage or a fallback mechanism that  isn't really practical for day to day use.
But in the worst case, if your coins are gonna be stolen, you can kind of invoke.

NVK: 00:05:00

Would you say  very simplistically, that's kind of  having a wallet in the blockchain,  people deposit funds to this wallet in the actual chain.
And then there is this sort of, they gave a bad name to it, but a smart contract that has some conditions.
And then if these conditions are met or change,  something else happens.
Right.
So  you kind of have  an if and else sort of  if this, then that kind of thing on the chain on your wallet.
Right.
So I'll give a very brief example.
Say, for example, I put the coins in this script, right?
This oP_vault that uses oP_vault that says, you can only spend one BTC per block.
And if you try to do more, I'm going to send the coins to this other address.
That is  a recovery.
So for example, if somebody tries to send more, the coins are going to simply go somewhere else.
That's kind of  how you take your money back in case it gets stolen.
Would you say that that's correct?
Or that's sort of  pushing a little too far on what's possible?

James: 00:06:07

It looks  Rijndael wants to talk.

Rijndael: 00:06:09

I was going to say the other motivating example that I use a lot is, I think a lot of people will have some really, what they hope is secure, long-term storage for their Bitcoin.
So they've got maybe a multi-sig setup or they've got some hardware wallet that's buried under the well and they want to be able to periodically take coins out of it and move it either to a hot wallet for spending or maybe they have to send it to an exchange to sell or whatever.
And for a lot of people, I think the nightmare scenario is, oh God, what if my house gets burglarized and somebody takes my wallet?
Can they now just steal all of my money?
So a really great capability to have would be to say.
I've got a white listed set of places that I expect to be sending my coins, I might send it to my phone wallet, I might send it to an exchange.
If it goes to any of those, it's okay, I'm going to let it happen.
But if somebody breaks into my house, steals my hardware wallet and tries to sweep my funds, then I have some big red button that I can push and sweep it somewhere else.
And maybe that somewhere else is  a crazy five of nine multi-sig, maybe I'm going to sweep it to my Aunt Betsy's wallet.
Whatever makes sense to me, it's a way to have a holding period on the withdrawal of my coins.
And during that holding period, I can revoke that action.
I think that's generally what vaults give you and I'm sure we're going to talk about how you can scale that up to more sophisticated institutional setups  what folks at Revault are doing.
Or you can scale that down to just I'm a single hodler.
I've got my stash in cold storage and I just want to have really good security for when I take my money out.

NVK: 00:07:56

So how does the blockchain know what's going on?
How does, because this is not  we have a Turing complete between quotes blockchain contract system here.
So how does your script know that somebody tried to do something?
And what, how does it know what to do next?
And how does that get triggered?

James: 00:08:17

Yeah, so NVK, to get back to the example you brought up earlier, which is this idea of kind of  thresholding some kind of transfer rate, I just want to be clear that OpVault doesn't actually get into specifying things  thresholds because that gets really, really complicated.
And Antoine can probably talk about that because Revault is a way of basically enabling very fine grained thresholding and spending conditions kind of at a higher layer with multi-sig.
Now, Re-Vault could probably make use of Op-Vault almost certainly.
And actually, if you wanted to do the scheme that you were talking about where you're thresholding some transfer amount sort of per block, It's possible you could  tranche up your coins into different OpVault invocations, but I'm not as sure about that.
But OpVault is a much more kind of simple mechanism than Specimen Exertion.

Rijndael: 00:09:15

Yeah, Maybe something that might help explain OpVault is maybe we can spend a few minutes talking about how you would do a system  this today with just multi-sig and ephemeral keys and pre-signed transactions.
Because all of these use cases that we're talking about, you could actually do today, but there's some real trade-offs in terms of liveliness, availability, and security of funds.
And I think what James' OpVault proposal does, or NVK, if I can say the C word on your show, what other Covenant proposals enable, is letting you get rid of some of those trade-offs by having consensus rules encoded.

NVK: 00:09:52

The problem with the whole ephemeral key thing and the whole  Brian Bishop's vaults and things that he was creating, I forgot the name of that proposal.
It was just sort of  a theoretical idea.
Nobody is going to do that realistically because, you can't prove that the keys were deleted even for yourself.
You can't.
That was what I think I talked to him about that in, what was it?
In a Miami meetup during the conference last time.
And I don't think most people even know about that, aside from people who are very close to core work.
So maybe we can touch up on it, but I'm not sure if there is much value in sort of  expanding too much on that.

## Practical examples of OP_VAULT

NVK: 00:10:34

Why don't you give us  some some examples of what you could do right now?
 give us some practical stuff.

James: 00:10:41

 as a 30 second kind of overview of how you could do vaults today.
There are really  two techniques.
Number one is to generate these temporary keys and basically use those keys to sign, a number of transactions that spend coins in certain ways.
And then you delete those keys.
And so after you've sent the coins into those transactions that are controlled by the keys that you just deleted, they're basically locked into a covenant structure.
The other thing that you can do is kind of  the way that Revault works, where you have sort of a big array,  a big multi-sig setup.
And some of those keys are controlled by computers that will just kind of auto sign on the basis of certain conditions.
An so I think in the in the pre-signed transaction ephemeral key thing it's tricky because  you say key deletion is really tough and you have to kind of , you're locked into all the parameters that you choose when you're creating the vault,  what key it's going to get transferred to, what amount, who's managing the fees, and you have to keep track of all that transaction information.
And then if you're going to go with the more  sort of flexible revault implementation, there's a big infrastructure burden, or I mean, bigger infrastructure burden in terms of  running all those auto signers and making sure everything's online and available and all that.

Antoine: 00:11:59

And also the introduction of new assumptions with regards to having pre-signed transactions because if you're running let's say a network monitor, watchtower as it's called in lightning world, that would enforce your spending policies.
Let's say with Revault basically you have a large multisig and you're delegating funds to a lower multisig.
So the covenant let's say is enforced by the fact that the lower threshold multisig does not have access to the keys of the N of N that is at the root.
So they are stuck with using an N-Vault transaction that is basically what's enforced on-chain with an open vault in more complex ways because then you have multiple keys and to this N-Vault is presigned to cancel transactions and so the N-Vault basically sends the coins either immediately to a transaction set is clawed back to the initial line of N or after a delay to some funds managers that can then use them.
In the meantime, a spending policy can be enforced by just broadcasting the canceled transaction.
And it comes back to your initial question about how these spending policies can be enforced under Blockchain.
The answer is that we don't.
We just let it delay with the pre-signed transaction or a covenant where we can enforce basically any spending policy whether it is a 2FA, whether it is a limited amount that can be spent per day, a whitelist, anything.
And what's very limiting with using pre-signed transactions here is that you need to know that all your watchtowers that are enforcing your policies get your pre-signed transactions before you actually sign the n vault transaction, before you actually commit to being able to get the funds out of the vault, you need to know that you are going to have a way to get them back with the cash transactions.
And usually in Bitcoin we assume, and especially with the SAMs, we assume that the laptop is compromised.
But basically with pre-signed transactions, you would store them on computers and had servers and you would not be able to, it's stateful.
So you would not be able to check on your signing device and only have the signing device as a rate of trust that you can always get back your funds.
Whereas if it's encoded in a covenant, you can check it on your signing device.

NVK: 00:14:29

I mean, all computers are compromised.
, I mean, we're past that point now and the incentives are to become further compromised by even more actors compromising them, right?
Because now the money is in the computer and more people have the money in their computers.

## Anchors and fee management mechanisms

NVK: 00:14:44

So let's say that we have oP_vault gets in, right?
And also anchors so that we can change fees.
Because you can't realistically have oP_vaults without having a way to changing fees or adding more fees.

James: 00:14:57

So what's cool now, I have yet to announce this on the mailing list, but I've actually figured out a way to avoid the reliance on v3 and anchors and all that stuff.
So ,

NVK: 00:15:08

Well, that's amazing.
Wow.

NVK: 00:15:11

That is really cool.
Do you want to give us  a quick Brief on that?

James: 00:15:15

Yeah, sure.
So basically in OpVault, you have to make a decision about whether your recovery path is authenticated or not.
And what I mean by that is so when you create the vault, you have to declare  where the funds can be recovered to.
In OpVault, you can optionally specify an additional script that has to be satisfied to even trigger that recovery.
And so the reason originally that we needed anchors for fee management in OpVault was if you're doing what I call an unauthenticated recovery, which is basically just , if someone knows your recovery path, the way that OP_Vault works is when you create the vault, you hash the recovery path, and then you add that as a parameter.
So basically  the ability to recover is correlated with the ability to reveal that pre-image.
So if you do that you can sweep.
So it's sort of  you're not to get really technical you're not signing it with Sighash all and so there's some  pinning problems that can happen.
But what I found was that if you actually requir an authorization for the recovery if you choos some key It could be based on  sort of a passphrase you memorize or a wallet that sits in your closet.
It's okay if it gets lost actually.
But if you use that key, then you can basically roll in unrelated inputs and outputs to both the recovery and to the unvault transaction.
And so you can use that as your fee management mechanism when you're actually doing the recovery or the unvaulting, you can roll in unrelated coins, or you can rely on the ephemeral anchor approach.
So you have a lot of, you have even more flexibility about how fee management works.

## Fee management

Rijndael: 00:17:05

So with  a, I'm not saying there's a good idea or a bad idea, right?
I just  as an illustrative example.

NVK: 00:17:10

It's a safe space.
This is a safe space.

Rijndael: 00:17:12

Right, yeah, for sure.
Safe space for bad Key management.
So if I wanted to have  a hot wallet on my phone that held the keys to authorize the recovery path, it sounds  a thing that I could do is keep a couple bucks in that wallet.
And then if I ever have to hit the big red button on my phone, I can use those little bit of funds to pay the fee for my recovery sweep.
Is that kind of the idea for whatever your choice of thing on your phone is?

James: 00:17:40

Exactly.
That's right.
And , oh, go ahead and end the case.

NVK: 00:17:45

So  how would you practically do that?
Because the vault might be 10 year sort of plan here?
 if people are doing this, they're thinking  they're kids, right?
I guess you leave your key,  a key to a safe deposit box that has say, 1%, 5% of your stash in it, that is just sort of  the backup plan to handle things, because You don't know relative to your transaction how much that may cost in 20, 50 years from now, right?
It could actually be a lot more than 5, 10% of the actual stash itself, depending on how the UTXO set is, right?
So just curious,  how do you sort of  see that?


James: 00:18:33

So it's tricky to think about
Because, I think people rightfully raise the point that if in your fee management strategy you need to rely on actually having other coins available that aren't vaulted.
That's a reasonable objection to me, but at the same time, I think there are definitely plausible schemes where you've still got value locked up in that vault.
And so it's very easy to do this kind of atomic swap type thing where someone offers to fund your unvault on the basis of you presenting them with an unvault that pays them out some amount.

NVK: 00:19:09

I can see that as a service.
And I think that's not an objection, per se.
I think this is more just trying to work out the kinks through.
Because it's sort of  a, we're going to have to rethink.
And I'm speaking as somebody who does the harder wallets.
I'm going to have to rethink of , how do I advise the users on how they do their setups and how do they do key management?
Because that's all going to change.
And this is actually fantastic.
Because multi-sig is a shit coin.
okay.
we have a way now to handle the fees.
Maybe it's, there is an oP_vault for the oP_vault.
 maybe there's a simpler oP_vault that you built that just handles fees in case you need more fees.
That's  your fee wallet.

Rijndael: 00:19:58

And the other thing that's really nice about oP_vault as opposed to other vaulting schemes that rely on pre-signed transactions is that you don't have to pre-bake them.
If you're DCAing into your savings every month or something, you can then have one unvault or a few and then a series of recovery transactions.
That makes the fee management in the future more flexible than if every time you deposit into your savings, you have to pre-bake a transaction.
And now you have hundreds of these things and you have to worry about, how do I do fee bumping across this set of hundreds of pre-signed transactions from the 20 years that I was DCAing or something.

## Generating addresses

NVK: 00:20:37

How practically speaking would a user get a list of addresses or generate new addresses to deposit on a vault?

James: 00:20:44

Yeah, so you have a lot of choices there.
And this is kind of where I need to spend a lot, I mean, we need to spend a lot of time thinking about  what kind of the recommended usage patterns are because let me describe to you  all the variability that you have in terms of what goes into an oP_vault address, right?
So in simple terms, when you lock up coins in a vault, you're creating a pay-to-taproot transaction to a taproot script that looks  op-vault, and then the first parameter is the hash of your recovery path with that optional authorization key.
Second parameter is the spend delay.
And the third parameter is the hash of the key that you use to actually trigger the unvault process.
So that's what goes into the script.
But because this is tap root, right, we can choose an internal key to use.
So you can either choose a nums point so that the vault is the only spendable way.
What I prefer to do is actually use an XPUB that's associated with your super, super cold path, your recovery path.
And obviously there, you can either vary the XPUB along that descriptor.
You can keep the XPUB, you can keep the internal key static.
You can vary the recovery path along a descriptor.
So  really you can mask the fact that you're using, that you have  a number of different coins and addresses that are all actually controlled by the same key material, or you can just reuse an address.
And this is good.

NVK: 00:22:20

 let's say we're doing this deterministically, right?
Because that's the best way to generate addresses , and you don't want to dox the pile.
So, I'm generating addresses there.
And I'm depositing to new ones because I have this XPUB somewhere.
So if I understand correctly, when I'm generating a transaction to unvault some of those UTXOs, it would look very similar to a standard wallet, right?
I mean, I pick those UTXOs, and this wallet understands the parent script there and sort of  say, hey, I want to spend this.
And if the key matches, then you start the process.
Would that be correct?

James: 00:23:00

Yeah, that's right.
The only thing that gives you away in terms of that you're using a vault or doing an unvault is that you have to present certain data on the witness stack when you're actually spending the vault.
Because  with any kind of taproot script spend, you've got to present essentially the path, and there are certain, , I think the shape of the data that you're putting into the witness is going to be pretty readily identifiable as being a vault thing.
But to me, I don't know.
That's not such...

NVK: 00:23:33

I don't see that as an issue.
It's more a concern about, people being able to link the UTXOs to the vault.

James: 00:23:40

Oh, yeah.
Yeah.
They can't.

NVK: 00:23:42

Exactly.
This is beautiful that way.

## Use cases for OP_VAULT

NVK: 00:23:44

Yeah.
So let's say we get it in.
 somehow we get it into Bitcoin.

Antoine: 00:23:50

Somehow.

NVK: 00:23:51

Somehow.
Which we should get into a little bit too, because I think it's important, we get it in.
What do you think would be sort of the first low hanging fruit scenarios that people are going to start building less complicated and more accessible to wallet developers.
They may not fully comprehend it how far this thing can go.
What are the first few case scenarios you see that the people could start using very fast?

James: 00:24:19

Yeah.

NVK: 00:24:20

That would be also safe.

James: 00:24:21

And I know I'll have to hand it off to Rijndael to cover because I know he's got some, but I do have a few.
Number one is  the brain dead improvement security that everybody could make at pretty much minimal effort, which is basically just introduce,  use OpVault and have your recovery path be a sort of separate hardware manufacturer kind of wallet technique than you have right now, even if it's as stupid as  some software wallet that you spun up on a computer one time, as long as it's not correlated with the way that you store your coins right now, there's essentially no cost.
I mean, the cost that you pay is  a slight delay to spend your coins, but there's no cost to introducing kind of an uncorrelated path to do recovery.
So really anybody could do that.
The second pretty easy scenario to set up, which I think is pretty cool, is if you're worried about  a hostage situation, you can actually, and really, I mean, OpVault is kind of uniquely allows you to do this.
You can set up a configuration where let's say that your spend delay is a week.
And let's say that your recovery path points to a taproot script, which is only spendable after a month.
You can have a situation where you can prove to your attacker, hey, look, I can't touch these coins, even if you start the process moving.
We can't touch this for at least another week.

NVK: 00:25:48

So that secondary receiving script, would that be based on where is the private key for that?

James: 00:25:56

You're talking about the recovery path?

NVK: 00:25:57

That's right.

James: 00:25:58

Yeah, so that's up to you.
However you want to store that, whether it's in your backyard, safety deposit box.
You want to store it in such a way that it's not readily accessible, I think, online.
It's because if somebody gets your recovery key and they figure out your recovery key, where your vaults are, and the sort of recovery parameters that you used, they can trigger a sweep to your recovery wallet.

NVK: 00:26:24

Yeah, I mean they have access to the nuclear code.

James: 00:26:27

Yeah.

NVK: 00:26:27

Let's put it this way, right?

Ben: 00:26:28

Yeah.

## Key management

NVK: 00:26:29

So would you say that, with a few years of this in the market and people really making this safe, let's put it this way.
would you say that maybe you don't have a nuclear code anymore?
You go the path of the ephemeral keys to generate all these paths.
then they just sort of keep on rolling.
your family has been the owners of this vault for the last 100 years.
things just keep on rolling and moving and rolling.
maybe you have a key ceremony every 20 years where you give the, you do a key shuffle, for example, a provable key shuffle, where nobody essentially knows what the keys really are, and it's provable, and you do it on camera or whatever.
And then the family sort of wealth continues into this sort of rolling vault.
Is this something that you sort of  imagine or you're thinking more sort of  today, nuclear cold kind of thing?
Or it's maybe unsafe to do that, I don't know.

James: 00:27:29

I can imagine that.
I mean, you can certainly facilitate the transfer of a vault pretty securely based on the spend delay.
So if you and your family decide you want to set up different security parameters, different key configuration, obviously,  Taproot gives you a lot of flexibility in that recovery path.
So you can set up all kinds of spending conditions there.
In terms of  doing key delegation and renegotiating, which keys can sign, that's...
Rjindael, are you unmuting this?

Rijndael: 00:27:56

Yeah, I was gonna say the other cool thing about this being taproot since we have Schnorr signatures is we can do things  proactive secret sharing.
With Frost, which is a threshold signing scheme for Schnorr signatures, you can do things  you can change the quorum size of the signing set or you can change the composition of the signing set without actually doing an on-chain transaction.
So if over time you wanted to change your primary vault key from being a three of five to a 10 of 15 or whatever, because you've amassed generational wealth in your vault, you could do that without actually needing to reconfigure your vault.
There's a lot of moving pieces there, but because this is built on taproot, there's these orthogonal key management gains that we're going to have that I think are additive for vaults.

NVK: 00:28:48

If we just use the imagination, the idea is I no longer need to make hardware wallets, right?
, no, seriously, it's , I make a device that is a safe device for you to construct the transactions outside of computers, right?
Or construct the scripts outside of computers.
And you're in your starship going somewhere else, and the vault just exists in chain.
And you just continue rolling, and nobody needs to touch it.
And it doles out funds based on your trust's actual trust rules.
And you have trustee keys.
And you can really represent the trust rules, for example, on a script.
It really is not that hard so that you're complying with the law.
And , it's quite amazing when you sort of really extend this out.
I know it's , there's a lot of moving parts and things, but I get excited about that because seeing users have single SIG plus passphrase being way more sane than cool multi-sig stuff that you can do, and people lose money with that.
I think that what we have is amazing.
It's an incredible upgrade from fiat and from gold vaults and things  that, but it's completely unsustainable.
 I cannot see,  a billion, two billion people, with  hardware wallets that look  the ones we make, maybe the cards, but , even then it's , there is a limit to this, right?
And most people also won't have enough money or wealth that will be worth the device.
And we can make sort of  poor people's vaults.
Right?
and a person doesn't have to have a lot of money to be able to have a solution that's , here, you spend this script and the little savings you have go into this.
And these things are all done for you.
They're all very safe and simplified.
At least this is how I see the stuff playing out.

Rijndael: 00:30:50

It also expands the design space of where you can have trust-minimized third parties that can help you with management without actually delegating spend authority to them.
So James was talking about this hostage situation a minute ago.
Imagine a scenario where you're  a high net worth person or you've amassed your giant stack of Bitcoin.
And so you have some company that you say , hey, look, If you see movement out of my vault and I'm not present in your office with all of my family, then push this button and it'll trigger my emergency spend path.
And boom, that's how you deal with somebody kidnapping your kids and using it to extort your money out of you.
That's a way that you can delegate some very specific spend path execution to a third party without them actually being able to spend all of your money.
There's lots of really interesting use cases in that direction.

NVK: 00:31:44

Right now, there are people out there that have an envelope sealed in their lawyer's hand with their private keys.

James: 00:31:50

100%.

NVK: 00:31:52

And it's not a non-trivial number.

## Inheritance planning

Rijndael: 00:31:56

Well, the reason why I started talking to James about this is I think that a really underappreciated use case of vaults is for inheritance planning.
 everybody has this problem of I want to make sure that either my kids or my wife or whomever can get to my Bitcoin if I get hit by a bus.
But I also don't want to have  a spat with my wife and then she runs away with all my Bitcoin.
Or I don't want my kids to decide that they want a new car and they  go upstairs into the family firebox and  steal all the Bitcoin.
So it'd be really great if I could give my kids or my heirs or whomever some easy way to get to my Bitcoin, but there's time as an additional sort of authentication factor.
And if I look at my phone and it says that my inheritance path has been activated and I'm still alive, then I can push a button and sweep those funds back.
I think that kind of thing is maybe a really killer app for Bitcoin self-custody because you can't do that with other bearer assets.
And being able to do that at an individual level without a bunch of extra infrastructure is really appealing.

Antoine: 00:32:57

You can do that on Bitcoin today.

Rijndael: 00:33:00

How would that work?

Antoine: 00:33:01

You just receive two scripts with the CSV, maybe of one year.
So of course, with Covenants, it would make that easier because then you can have a trigger transaction and so you don't have to rotate your coins.
This inheritance thing, you can already do something.

Rijndael: 00:33:20

Yeah, so you can do that with CSV today, but then you end up with the problem of, I set a two year, relative time lock on my coins, and now every year and 11 months, I have to  go and rotate my UTXOs in order to reset the timer.

## Simplicity vs complexity

NVK: 00:33:35 

It feels unsafe.
It feels that everything that we have for this purpose without something  proper covenants on chain is not possible for most people.
You're definitely going to have something  Revault, where, institutions are gonna go and they're gonna have people audit the script and audit the paths and sort of go through the, but it's gonna be very hard and it feels unsafe.
I mean when people are talking about their money, it cannot, if it feels unsafe  multi-sig feels unsafe.
people won't use it.
This is the beauty of passphrase with single SIG.
It feels safe.
And then

Rijndael: 00:34:19

it's so simple.
 there's not many moving parts.

NVK: 00:34:22

I mean  the amount of people who lost money on the most secure system that there was at the time, which was Armory.
Remember Armory wallet?
Yeah.
I know so many people whose coins got locked and that's it, this is the issue with all this complex, amazing setups is that  you end up screwing yourself out of your coins, which is the majority of the people.

Rijndael: 00:34:45

Well, and I think we're seeing market demand for that.
Because  when the multisig descriptor was added for Taproot in Bitcoin Core,  the first thing that everybody did with it was time decaying multisig.
Because people want the security of multisig, But they also really want to make sure that they can get to their money.
So they say, OK, cool.
In two years, it's going to decay from a three of five to a one of two or something.
But then you have this problem of , OK, I've got a ticking clock until my coins become less secure.
So now I have to have a reminder on my phone every two years.

NVK: 00:35:19

Yeah, but then you get hit by a bus and your wife didn't know.
And now you went to another wallet that they had no idea.
We see this all the time.
The clever programmer husband goes and creates a shadowy super code, or amazing script and amazing set up on their,  vintage, 93 IBM laptop.
And we feel  cubes OS an, and then great, So cool.
Well, one, he probably gets pissed off one day and accidentally  attaches a USB stick and boom, money gone.
Because he was just not thinking that day.
And then the other one is, again, guy passes, right.
Or get gets , brain doesn't work anymore.
And that's it.
family can't recover.
it just happens a lot.

Antoine: 00:36:12

I don't see how it relates to having a time-locked recovery key.
I mean, it's just a straight improvement to the situation that you described with the envelope having to share your public key for inheritance.
You just have a second public key that is timelocked and you just share this one.
So at worst case, you don't rotate your coins within years and well, you're probably dead.
But if you're on earth and just you forget for years to not rotate your coins, then the lawyer can access your coins and it's the same situation as today.
So.

Rijndael: 00:36:42

Well, I think the challenge is sort of this thing of I think there's been enough education in the Bitcoin ecosystem about, hey, you really need to have your seed backed up.
But I think when you start getting into more interesting scripts and more interesting spend paths, people are less sure about How do I back up my descriptors or whatever other metadata I need to actually spend those coins?
And so, there's a lot of just, people are figuring out new places to hide a piece of metal with seed words stamped on them.
We haven't really gotten to that level of creativity for what do I do with my descriptor?
 I haven't seen somebody, tattoo their blood type and their descriptor on their butt cheek yet.
But I'm sure it's coming.
And I think that how we back up that metadata is a super important question.

NVK: 00:37:31

One of the things I absolutely hate is Shamir's secret sharing for key backup.
Because it's  reinventing multi-sig with a complex script that's completely custom.
And it's  vendor specific and it's not Bitcoin related.
So I'm , okay, if you're going to do this, then use multi-sig.
At least it's Bitcoin.
And there is more sort of , greater sort of education and adoption.
So that was the motivation to create CDXR.
We still needed a way for people to split their main root keys.
But we wanted a way that a donkey could recover with pen and paper.
And just every time we start thinking about practical security, we try to go back to World War II.
Seriously, this is how we think about this stuff.
And it's OK, I am a guy trying to flee some country that's in war, and computers are not available or compromised.
I need to take my money with me and I have to go naked.
How do you actually go through that process, based on this complex stuff and that kind of leads me to the further picking and risks that I'm trying to sort of think through on OpVault are the practical ones.

## OP_VAULT practical applications

NVK: 00:38:42

I think we can still go through a little bit more of the technical stuff in terms the actual, interesting parts of how this works, but the practical stuff, needs a lot of thoughts still.
 how do you manage these keys?
How do you manage the nuclear codes?
Do you do an op-vault, on op-vault, on op-vault?
So  you have some recursive way of  moving stuff around.
How would wallet UXs address the vaults and create all the stuff?
And, what kinds of things you guys have sort of thought through in this sort of practical space?

James: 00:39:30

I think that's a lot of the work that remains to be done.
I mean, I think the framework right now gives the end user a lot of configurability.
And in designing it, I'm trying to avoid any particular configuration that would be just blatantly unsafe and any use that just wouldn't make any sense.
But at the same time, I mean, things for your recovery path, are you using a static address there or are you varying it over a descriptor, that does have implications.
Is your optional recovery off parameter, is that derived from maybe the descriptor of your cold wallet?
Or is that a separate key that has its own life cycle and is independent?
All these choices do have implications.
And I think we're really going to have to spend the next year, a few years, kind of figuring out what the right usages are and  really nailing those.
But my concern, you have to balance kind of getting the usages exactly right with the fact that right now custody for everybody is nerve-wracking.
It's totally nerve-wracking.
Jameson Lopp has this great article where he talks about vaults, a little bit about the history, a little bit about OpVault.
And he introduced this framework for thinking about things, which is right now we have proactive security, which is you do your best to build your fortress, set up your keys in the right way.
But I mean notable developers have been compromised and it's probably that they went to great lengths to do this proactive security and build this wonderful fortress that fell down.
Something OpVault gives you reactive security where you can see, okay,  I've been compromised, an attack is happening, what can I do about it?
How am I going to respond?
And so OpVault's really the first on-chain mechanism for doing something like that.
And I think we have an acute need for it, especially at the corporate level.
look, I mean, individuals holding Bitcoin is my favorite and most important use case, but , we all know that micro strategy holds a lot of Bitcoin, one plausible argument for a better future is for someone  like America, to hold Bitcoin as a reserve in their central bank.
To do things that, you need an ironclad nuclear level strategy.

NVK: 00:41:57

It lowers insurance.
See, this is the thing.
When you're talking about institutions, institutions don't have the luxury of choices, of many choices or, how they feel about stuff, you have  legal frameworks.
For custody of things as a public trader company or whatever.
And then you have your charter, and then you have all your fiduciary nuances of things.
And you're going to have to follow these very traditional ways on how things are custodied.
And then they might de-risk it by using different vendors as well, so splitting the pile.
And then everything needs to be insured.
And often you have insurance of the insurance as well, especially because if you're trying to, and it's in dollars for the next foreseeable near future here at least, this is denominated in dollars, so you have to get reinsured as the price of Bitcoin goes up and down.
And, they're gonna try to understand your vault, your security,  that's why you use custodians that already have a lot of , provable experience on what they've done, Fidelity or Coinbase or whatever.
And it costs a lot.
The insurance on this stuff is obnoxious.
Because this is a very easy to steal asset.
its best feature is its solubility and, fungibility and transportability.
So how do you do that cheaper, which everybody cares about, and safer
And I think this is great for enterprise that has to deal with insurance.
And soon enough, we're going to see even individuals seeking insurance
That's what the guys from  Anchor Watch and things  that are trying to do.
But it's hard, because you can't prove that you lost a key.
You can't prove that it was not a boat accident.
It's very tricky, say the cops break into your house because somebody did a swatting on you, and they opened your safe, and they took a look at the keys.
Now the money disappears a month later.
How do you prove that the law did it.
I mean, look at the Silk Road problem.
All the cops involved in taking down the Silk Road magically became millionaires.
So anyways, this stuff really sort of facilitates this next stage of the Bitcoin future, at least in my view.
That's why I'm so excited about this.
Now, I think we can do a lot more complex stuff.
And, that's why I brought Ben here.
Ben is interested in the shitcoining layer of Bitcoin.
I'm just kidding.
He's going to talk a little bit about DLCs and lightning stuff and all the things that we could maybe do with OpVault as another primitive in Bitcoin.

## Covenants and discreet log contracts

Ben: 00:44:34

Yeah, I mean, to preface it if we want to do all this stuff, we probably don't want to use OpVault for it.
We should use  CTV or APO or I mean, things that are  more custom tailored for it.
The way you do it with OpVault is kind of a hack.
But basically , we want these primitives where, today with  Bitcoin script, you can't really say it has to be spent.
It's only locking it under these conditions.
You're not saying it must be spent with this amount or to this address and anything  that.
So you can't have any guarantees in your address that it's gonna be spent to the right person, just by the right person.
And because of that, say you have an address with one Bitcoin in it and you say, I want it to be split 75% to me, 25% to James.
The only way to do that is just  me and James have a multi-signature agreement to sign that correctly.
Versus  with not vault we can have that or  CTV or any of those, we can have it  enforced in the script that 75% will go to me and 25% to James.
So with that kind of primitive you can build a lot of  really cool stuff where I mean, the one I pointed out was DLCs where I mean, Lloyd funny point out originally, and I showed you could do it vaults where you could, instead of  having a DLC with  a 10,000 pre signed transactions, you just have a single address that's encoded inside the address as your entire DLC contract.
So you can create these really fancy stuff all inside of a single address.
And the cool thing is too, you can make these extremely composable, where your DLC payout address is just another DLC, or maybe instead of being an individual in a DLC, you have it as a company.
So then say I win the DLC, then the payout goes 9% to me, and then 10% to my investors or something.
So you can kind of  build these structures really easily where  all these fancy things are happening all in force in Bitcoin script instead of  hoping your multi-sig game theory works out.

Rijndael: 00:46:29

Yeah,  The way that I've been trying to generalize this is a lot of times if you want to do interesting smart contracting with Bitcoin, what that usually ends up looking  is trading around a lot of transactions for people to sign and then trade back.
And what's really cool about Covenants, anD, I think  a really simple generalization of Covenants is that Bitcoin script right now lets you put conditions on the inputs of a transaction.
Covenants let you put conditions on the outputs of a transaction.
And so if you have some Covenant system, then you can take all of the network IO and the coordination of signing in contracting protocols and you can reduce it down to signature generation.
So locally, I generate a giant Merkle tree of all the possible conditions and I sign it and we just have to trade around Merkle commitments.
And that's a lot cheaper from a coordination perspective than we have to actually pass all of these things around.
And that's really important for DLCs. I think it's also important for things  coin pools or channel factories or other multi-party constructions.

NVK: 00:47:33

Let's talk about some examples that a person who does not understand this technically sort of  would get , what things could we see here?
Because now that you have the DLCs, with proper chain control
You can do a lot.
I mean, you can create financialization things, products, you can do  betting things, you can do, there's really  a very big sort of  new space of things you can do.

James: 00:48:05

So maybe, Ben, could you talk about, I know this is kind of controversial, but for me, this is one of the most exciting things is this idea of doing endogenous USD stable coins with DLCs, where you don't have to have some entity that's  holding dollars in a bank account.
You can synthesize USD exposure with Bitcoin.

Ben: 00:48:24

Yeah, that's exactly what I was going to bring up.
I think the biggest use case likey for DLCs is either degenerate gambling of  sports betting or other likely is creating stable coins without having Tether, which just has a bank account somewhere and you hope it's there.

Rijndael: 00:48:42

And a stable coin, a synthetic stable coin is degenerate gambling on the price of Bitcoin.
So it's all the generic answer.

NVK: 00:48:48

It's a directional trade.
This is the problem.
Yeah, for sure.
Both legs of the asset and the collateral are of the same market to market.
This is essentially what we saw in this last Bitcoin pump and break.
It was the fact that everybody was using the same asset as the collateral, betting on that asset.
But  reality is  especially people who don't have money, what they want is USD.
I mean, they need stable stuff, right?
They can't, they don't have enough float to survive Bitcoin's volatility.
I mean, that's that's a wealthier people problem.
So, I'm a huge fan of stable coins.
I think  until we're hyper-bitcoinized world,  we're going to need them.
And I don't want them to be controlled by the state actors that provide the armies.
So Ben, how would you build the most simple, stable coin on this setup?

Ben: 00:49:39

Yeah, I mean, with DLCs, you just create a contract where you say , I'm going 1X short and your counterparty is going 1x long.
So then the person holding 1x short, they're holding Bitcoin, but they're short.
So it's not even.
And they're  essentially holding dollars on Bitcoin.
And  to do that today without  any covenants, it's a little impractical, , because you're doing a bet based off the Bitcoin price and the Bitcoin price is just a number.
So you're going from zero to , say  100,000 or  a million, you have a lot of different outcomes there.
And especially  in a DLC, you're trusting an Oracle.
So maybe instead of trusting one Oracle, you wanna trust  a three or five set up and , you kind of get an explosion of possible outcomes there for all the different Oracle outcomes, or which Oracles are signing exactly  what price they're signing.
And  we were doing tests when I was a shared bids of this and , we did  a bet on the Bitcoin price with two or three Oracle set up and it was something  80,000 possible outcomes with all the optimizations we did.
So we sent around 10 megabytes of signatures.
It took a couple minutes to sign and it was ridiculous.
It works on our laptop, it's eight cores and all this stuff, but, making an actual user-friendly thing on an app is  not really going to happen with that.
At least, not anytime soon, but with the Covenant's route, it would make it a lot more simpler where we're not doing all this huge bandwidth of signatures and stuff that.
We're just gonna calculate the Merkle tree, which would still be a little complicationally expensive, but not nearly as enough.
And it makes it so much simpler in the protocol as well, where we need all these round trips back and forth and all this P2P stuff is basically generating address, verify the other card and probably do the same thing and sign a transaction.

NVK: 00:51:24

A critic would say, but why not do this on AWS?
And, just,do the payouts in Bitcoin.
why do we need to do this on Bitcoin?
Why do we need this extra stuff?

James: 00:51:39

Trusted third parties or security holes.

Ben: 00:51:41

Yeah, exactly.
you could deposit in the Coinbase and do the bet and then, withdraw, but we saw FTX worked out.
We saw, the other thousand before them worked out as well.
we need to kind of wait to do this natively.
And I think there is demand  and the shitcoin space,  a lot of people are using , all their trading stuff on there That's  a uni swap and blah blah blah just to  trade stuff quote-unquote trustlessly 
So there actually is demand for this and it seems I'd rather people use Bitcoin than shitcoins to do it So I hope...

James: 00:52:15

As I understand it the big problem with doing stable coins on DLC is, I guess the technical term is novation.
So it's , if you want to treat this thing as a coin and trade it around, you're essentially trading  a futures position around.
And that's , I've thought only briefly about it, but I couldn't figure out kind of how to do it right away.
Do you have any thoughts on how that might work out?
is there some key delegation thing you could do?

Ben: 00:52:42

There's a way to do it.
On SharedBits, there's a few blogs on how to do it for all the different setups.
But I mean, essentially, the worst case is if your counterparty disappears, you just open up another trade with someone and you're double collateralized, which kind of sucks.
But otherwise, you kind of start closing it with your counterparty while also opening it with the new counterparty and you're able to kind of sell it in that way.
But yeah, it kind of takes .

Rijndael: 00:53:10

So it's  an atomic thing of , I sell one position and open another position at the same time.
And so my net exposure stays the same, but I've actually closed and opened two contracts.

Ben: 00:53:24

So you'd have to say Alice, Bob, and Carol.
Alice and Bob already have the position open and Carol wants to buy Bob's position.
Basically, you'd have  one transaction that's opening Alice and Carol's new contract while closing Bob and Alice's contract.
So Bob gets the exit to set up, while , leaving his position while Alice and Carol kind of start the new thing.
And, you could update the contract in there, you could pay out anyone in that transaction of someone's paying for a premium or something  that.
So it should all technically be doable.
I mean, the covenant model gets a little easier because, now there's less activity or interactivity and stuff  that.
So, if you had to do these 80,000 signatures, you have to do, 160,000 for the two parties.
So this makes it  a little easier.

Rijndael: 00:54:15

Yeah, I was gonna say  with the Covenant case, if I've got a mobile app, and on my mobile app, I say , because I think the best lightning app that we could ever build is kind of what Bitcoin Beach is trying to do.
But theirs has a custodial backend, where you have a lightning wallet.
And then in your lightning wallet, you can say, all right, I've got 50 bucks.
I want 30 of that to be pegged to the dollar because I can't stomach short-term volatility.
And then the other $20 I want to keep in Bitcoin.
And  you just kind of drag the slider.
But if every time you do that, if I'm opening a new position and we use DLCs as they exist today and me and my counterparty have to trade and sign 80,000 CETs,  contract execution transactions, that's insane from a mobile phone.
And then I have to do that  every time I drag the slider versus if every time I drag the slider, yeah, I'm hashing a bunch of, CETs locally into a Merkle tree and then we trade one commitment, both sign a transaction, we're done.
that's something that I could actually imagine happening.

James: 00:55:20

So are either you guys going to,  advocate for either CTV or kind of whatever your preferred mechanism is?
Because I know there's talk about  simplicity, there's talk about these more general, fancy Covenant structures, but I think there's just, in my view, a ton of time difference between Now and when these things are deployable and proven safe.
So I mean what what's your guys's plan?

Ben: 00:55:51

I mean simplicity would be the best thing but  that is so far away  I don't think it's reasonable to talk about

James: 00:55:57

I looked at the patch set on elements.
That's up right now.
It's 77,000 lines plus

Rijndael: 00:56:05

It's the year of the Linux desktop

James: 00:56:08

And spoiler alert  the code is not breezy.
It's not  a nice Python, it's  hard to read.
So

Rijndael: 00:56:18

I mean  one of the things I like about the oP_vault proposal is that I think it is more specific, and I think it's easier for people to see a straight line from that proposal to actually use cases that gain market traction and actually add value for Bitcoin users.
I think you can have a really good debate about, do we want to have a really general purpose covenant structure that takes a long time to figure out if it's safe, or do we want to just hold tight for simplicity?
If the goal is that eventually we're going to have either super general covenants or simplicity but that's in the future, I think there's a reasonable case to be made that okay, in the near term, let's do something sooner that adds value now but doesn't try to go 90% of the way to a super general purpose covenant scheme.
I think I'd be less inclined to say, let's do really super generic covenants and then also try to do simplicity, because there's a little bit too much overlap there, whereas something  like OpVault, I think, is much more targeted and kind of adds value to that.

James: 00:57:24

I'm definitely gonna shill OpVault in the short term, but I do think, I mean, if you look at the patch set for CTV. 
it's a very well-scoped, limited change.
A lot of people have spent a lot of time, trying to pick it apart.
God knows everybody wants to dunk on Jeremy.
And so.

Rijndael: 00:57:41

And there's money there to be made if you bring the problem.

## OP_VAULT benefits

NVK: 00:57:44

So just before we go into activation and a path to sale, it's a sales job, one more thing I wanted to just address in terms of features and benefits of this is in terms of Lightning, what benefits do some of the Lightning setups right now would have  sort of  immediate improvement?
Because right now Lightning doesn't scale, right?
I mean , it's cute and all we can have say a hundred to  50 million people using it, but we cannot have say  half a billion people using Lightning.
It's  actually impossible.
So do we get some extra sort of  breathing room on Lightning with OpVault?

James: 00:58:24

I think it's plausible that OpVault might help to compress the witness sizes for Lightning transactions a little bit.
But to be honest, I think that might be marginal.
I mean, you'd need someone who's really in the weeds on Lightning to sit here and tell you whether or not there is some kind of significant kind of game changing improvement there.
But from my impression, I think it's it'd be a nice little marginal compression maybe, but it wouldn't be  a game changer.

NVK: 00:58:53

Okay.

Antoine: 00:58:54

Yeah, maybe there is some benefits to coins pools as well as well as scaling solutions that are possible with constructions that are close to upvotes, but a bit more generalistic, such as tapleaf, update, verify.
I think there is definitely value with that.
If there is a spectrum between just doing CTV and doing simple CD, maybe in the middle, doing something  tapleaf, update, verify, maybe with some kind of checker, it puts verify.
I think it would complete what you need to do vaults.

James: 00:59:25

So the trade off there, if you do sort of more low level granular opcodes,  TLOV or check outputs, then everybody comes up with this standardized vault construction that you have to encode in script.
And everybody's basically doing the same thing, but the script sizes are huge.
And so these transactions end up being very costly.
And I'm not even sure, to be honest, if you can get the same behavior from OpVault that you can just with those two opcodes, because there is some special logic around supporting immediate re-vaults during un-vaults and things like  that.
So it's, I think  something  vaults is a really good example of even if you had the super futuristic flying car covenants, it's , well, maybe you still want to op_vault because it's a very common usage that you want to compress.

Antoine: 01:00:19

Well, we don't know if it's yet a very useful, very used, well, very common use case.
We don't know yet.
And I don't think, well, I'm not buying that it would be so much more expensive to do with WP-5D to verify what you're doing with OpVault.

James: 01:00:34

It could be, buT, nobody's shown me the scripts,  nobody's written me the scripts,  Show me the code.
People come up with these highfalutin proposals and it's , okay, maybe that sounds good and if I squint at it, I can interpret it in such a way, but , where are the patches?

Rijndael: 01:00:51

Yeah.
Show up with patches.

Antoine: 01:00:52

Yeah.
I agree.
I agree with regard to the implementation and that's something that I was, I was wanting to, to look into, I wanted to implement a Taply Third Date Verify on ReVault,  just implementing ReVault with Taply Third Date Verify, which would basically give upvault in a bit more generic way, but I never came to do it.
But AJ in this original Taply Third Date Verify post as a vault construction that is close.
Well, it's not really a freeze all my funds recovery path  you have on Opvaults, but it's a revault path that keeps revolting.
It's a decent vault construction with the detail of the scripts that seems to work.

James: 01:01:34

I haven't seen an implementation.
I read all those posts.
They seem to be very vague.
And I've been working closely with AJ on his proposal, actually.
He gives me feedback on a semi-daily basis in terms of how to guide the proposal.
But I'm not buying the T-Love stuff until I see the code.

Antoine: 01:01:52

Yeah, sure.
That's fair enough.

NVK: 01:01:54

So  if we had to just  sort of  wrap up the benefits, right,  of this for  your average user out there who is going to be engaging in hats and other means of getting things into Bitcoin dramatically or undramatically.
what would you say are  the 10 main sort of  one liners that , okay,  we activate this today,  you gain this set of lists,  nearly immediately
assuming of course there's a UI to use it and stuff, but , it's  very achievable, very simple, very safe.
you get this.

James: 01:02:34

Yeah, so my tagline has kind of been, you get the operational complexity of single SIG with multi-SIG security, multi-SIG safety.
And, Personally, if I could do this for my own funds, I would sleep a lot better at night because I could have coins in cold storage and I could be alerted if somehow in any number of a million different ways, my infrastructure got compromised, my Rodolfo backdoored my cold card.
There's just a million different ways you can get popped.
And I don't want to rely on having built the perfect fortress and pre-anticipated everything.
And so I want to be able to have reactive security.
And I think OpVault is today  kind of the most straightforward, easiest to use way to do that.

NVK: 01:03:24

So , essentially you get end user, sort of  amazing security with like you can build some fairly safe, straightforward scripts that handle normal people's money problems.
You can have institutional problems resolved.
You can create.

Rijndael: 01:03:43

There's probably also a middle thing in there too.
There's been a lot of discussion about things  e-cash mints,  Cashew or Fetimint.
And this would also be an upgrade for their setup.
Because what those systems are is they're basically just smaller custodians.
And so if you want to uncle Jim funds for your family, your friends, your community, your school, whatever, and give them a very private lightning wallet via Chaumian eCash, it would be great if you could upgrade your security setup without dramatically increasing operational complexity.

NVK: 01:04:20

Yeah.
So, you get the DLCs
we can finally have some interesting dynamic stable coins or any other kinds of dynamic contracts really being represented in the actual chain, right?
Or protected by the chain.
And we get some simplicity.
I mean opVault it's a small patch.
It's a small, I mean, compared to other things that do covenants, this is my new school.
I think, at least I have not bumped into very reasonable, very strong opposition from anybody who understands this stuff.
So I don't know.
It feels  a very sane next feature for when everybody is in the mood of getting next feature.
And you resolve the fee problem, which is kind of a huge deal.
I think that the rest of the unresolved things are more practical, like how to handle the keys and how to sort of do things in the UI, sort of  the implementation real sort of  issues.
But those things are true for everything that you build new.

## Criticisms and risks

NVK: 01:05:31

So now  we sort of  we should start addressing  the hard part.
Can we go through some of  let's try to steel man some of the some of the realistic sort of criticism and risks and also maybe some of the most absurd ones.
Especially I think  addressing absurd things is very important because, this stuff is not simple
So people don't get it.

Antoine: 01:05:56

Yeah, maybe if I can add something, maybe some nuances to the use case of Vaults because obviously I'm a big fan of Vaults.
And I've been, or maybe the more nuanced that I was in the beginning after trying to solve all the issues, especially with the actual implementation and deployment of these solutions, because it's not all in the scripts and having an MVP, but trying to figure out what theories of that you're going to use and how you're going to manage this theories of and how you're going to use them is a huge problem.
And that has huge consequences on the security of your setup as well.
So yeah, just to give more answers, is that basically Vaults give you spending policies.
It's give you spending policies and you can have spending policies today with a cosigner.
So you could always have an HSM that enforces co-signing policies and that is going to, well, you can always trust that this policy is going to be enforced as long as you trust the HSM.
So it's a single point of view.
And vaults give you the possibility to have decentralized enforcement of these policies, but hopefully the transaction confirms.
So it's a trade-off.

NVK: 01:07:11

And it's always hot.
So this is the part that people don't get about  HSMs, generally speaking, is that, banks have been doing this forever.
They have essentially spend policy.
HSM is a hardware security module.
It's essentially a server that's made secure.
It costs a lot of money and a manager needs to go and tap on it or multiple managers go to tap on it and the thing turns on, turns off and you can add more spending policies that have been audited.
Let's put it this way.
that's completely unrealistic for Bitcoin
Because banks have, they can do backseas.
They can roll back.
They get hacked all the time, but they get to roll back because it's just fiat, it's just IOUs, right?
They call the bank, the receiver bank and say, hey that money, yeah, that was hacked, send it back, right?
And they just change their ledgers and it's great.
With Bitcoin, the money's gone.
So, We don't have a way of doing that in a secure way.
Any server that is hot on Bitcoin is a matter of time before it gets hacked.
And also, maybe the controlling keys that may not be able to, maybe they can't hack the server itself, but they can maybe change the policies with some other key.
So go ahead Antoine.

Antoine: 01:08:19

yeah, I know exactly what you say.
It's just that it's trade-off and you need to be willing to get into the assumption that the transaction is actually going to get confirmed before the end of the delay.
Because with an HSM, the policy is actually enforced every time, as long as you trust it.
But with pre-signed transactions, the policy, there is no single point of failure, but it might not be enforced if people are trying to fuck with you by filling all the blocks, for instance.
If they outprice you out of the block space.
And so you might want to consider having high fiat reserves.
And if you have high fiat reserves, it means that it's only for very high value vaults.
And well, no, I mean, you might consider having large delays, but then you want only to have large delay for large value spendings.
So you might only use vaults for very large value, But then it's going to be a huge incentive to price you out because it's one transaction.
If you get to send so, you can steal, essentially.
So, yeah, it's a tradeoff.

## Watchtowers and handling blockchain information

NVK: 01:09:27

How would you handle sort of some Watchtowers or something
you need something watching the stuff and let you know what's going on.
It's not like the blockchain is gonna call you.
So How would you how would you do this?
Because again, you need to know that something happened to the coins

James: 01:09:43

Yeah, so  many things with this proposal, there's a lot of optionality on the part of the end user here.
And it kind of depends on how much you want to actually trust the watchtower, right?
if you have full trust in the watchtower, you can basically just hand it the location of the vault or some descriptor that tells you where all the vaults are, and then the information necessary to actually do a recovery transaction.
And the risk there is that if the watchtower turns on you, they can just sweep all of your coins into the recovery path, which might be annoying.
I mean, you're not gonna lose the coins, but it just might be annoying because your recovery path is presumably difficult to recover because it's difficult to access.
If you, on the other end of the spectrum, if you don't trust anything at all about the vault, I mean, about the watchtower, You could give it some compact block filter-like object or a bloom filter-like object, and it would basically alert you every time it saw something move on chain that might be one of your vaults.
So there would be a lot of false positives and you would have to have software kind of running on your end that's  getting notified and then checking, okay, well, is this actually an out point that I care about or not?
And then there's  a whole range of stuff in between there.
one thing you might do is you could give the watchtower some information that's encrypted with other information that's only revealed when a vault is being unvaulted and then it could, kind of intervene and broadcast.

NVK: 01:11:16

That's more like a flag
if this flag is raised, I see the flag.
And what's cool about this is that it does not review amounts.
It does not dox UTXOs, none of this stuff really, right?
It could be easily done in that way because you don't want the server knowing how much coins you have, what the UTXOs are, because all those things, it's  when bad, if bad guys don't know how much money there is, they're less likely to do something.

Antoine: 01:11:41

And also James mentioned with trusting one watchtower on it, but you probably want to have several of them as well because and then it gets into issues with the few reserves as well because You might not trust only one watchtowers and not trusting it is not only that there might be many issues but it might just get compromised and compromising for watchtowers is not actually getting control of the servers, just cutting internet access and it just can't enforce the policy anymore.
So you might want to have plenty of watchtowers but for each of them you want to have different fiat reserves because if there were two shares of fiat reserves then one of the main issues watchtowers could actually steal the funds from under the other watchtowers.
So you need to duplicate all the fiat reserves for the actual enforcement on all the watchtowers.
So it really needs to be high value vaults again.

## Fungibility concerns

NVK: 01:12:35

So  another sort of  thing that came up during CTV was is there a concern for Bitcoin's fungibility, actual fungibility, not sellability, right?
now you have this coins, they're kind of trapped in this things.
And, are we creating some new sort of incentive structure that we maybe don't understand.
I mean Taproot gave us dick butts.
On the blockchain.
So with every new feature
you could get dickbutts. So

James: 01:13:06

I hope that becomes a term of art.

NVK: 01:13:09

Yeah, I mean a hundred percent I want dickbutts to be the representation of possible Bitcoin surface attacks.

Rijndael: 01:13:17

So It really sums the whole thing up.


NVK: 01:13:20

It does.
Dickbutts and the blockchain.
So that's what Forex block size increase, which is the original SIN in my view, gave us in conjunction with this other amazing thing, which was Taproot that removed the script limit on The Witness.
And it's also discounted
So you have discounted big blocks with dickbutts.

James: 01:13:41

Sounds like a porn.

NVK: 01:13:43

It does
have you guys thought about  some of this dis-fungibility more sort of  economical concerns around this?

James: 01:13:52

I think with vaults it's pretty minimal.
I mean the classic concern that everybody has with recursive covenants or in other words covenants that can continue indefinitely is , oh well, if we have that, then, they're going to roll out GovCoin tomorrow an, all the, I'm going to have to get a signature from the Treasury Department to spend my coins, and oh, God, it's gonna be horrible.
The reality is that that's already possible today in a way that's much more convenient than covenants would be, we have multisig.
So if tomorrow the government orders Coinbase, to have all their withdrawals encumbered in a two of two, then we're already toast anyway.
So I think covenants don't really add any risk in that sense.

Antoine: 01:14:36

I talked to that.
So I agree with you, James, but I talked to people that actually don't buy these arguments, saying that actually reversing the policy is would be a hard fork with Covenant but would not be with MultiSig.
I think that's a criticism that the issue is even beforehand.
If you're opting in,  with a Covenant, you need to opt in, you need to send your coins into it.
So if you are opting in into a covenant, you might even opt in to the government altcoin in the first place.
And you might opt in to not using Bitcoin.
If they can force you to use the government covenant, they can force you to use their own currency.
So I don't think it's a concern in the first place.

NVK: 01:15:19, I always  to say that the state actors  to do the low friction approach, which is just knock on your door, drag you to some very uncomfortable place and just say, hey, listen, give me the keys or you can't leave.
And most people try to stay there for a little bit of time and maybe you're just very good at staying there a little longer.
But eventually, people will sing.

James: 01:15:45

Yeah.
They're much better at doing that than writing Bitcoin script.

Rijndael: 01:15:49

Well, and especially  two things that I think a lot of people miss when they're worried about the GovCoin covenant encumbrance.
One of them is exactly what was just said, which is, when you generate a receive address, your receive address has to commit to the covenant in order for your coins to now be encumbered by the covenant.
So if I just generate a plain old, pay to taproot single sig address, then you can't send me coins that I now can't spend because I didn't commit to the covenant.
That's one thing that's important to understand.
The other thing that's really important to understand is that if you use covenants to enforce some kind of whitelisting mechanism where coins can only be sent to people on the list and if you eat too much beef this month then you can't spend your money.
whatever the doomsday scenario is.
Anytime you want to change the contents of that list or the semantics of that list, you have to regenerate the covenants.
And so from an operational perspective, it's a very not scalable solution.
Something  like having a co-signing server and having all your coins encumbered with a two of two multi-sig is way more scalable because some bureaucrat can just push a button and add or remove entries from the list and then that list goes into a policy enforcement engine that decides whether or not to co-sign a spend.
That's actually how people would build things.
There's actually a product from Blockstream called AMP that does exactly this thing for registered assets.
So if you want to go and play with it, they have a demo site and you can issue yourself a restricted asset.
But yeah, and then to NVK's point, all of this stuff is moot if they just drag you out of your house and put you in a box and say you're using, GovCoin now,.
so the Covenant thing, I think, is a little bit of a red herring.
And it's, it's not a good argument.

NVK: 01:17:40

I think, once you sort of  get into a little bit more practical flag theory as well, you start having the recovery, for example, nuclear keys and XORed in two separate different countries.
And listen, if you have enough money that you are a person of concern, a prescribed person or whatever, however your state actor  to call these people, you probably have a little bit more means and you're going to probably start sort of  distributing yourself outside of single jurisdiction and provably too
So maybe, if they point the gun at you, that vault that was not touched just disperses to your Monaco PO box
And there's nothing they can do, really.
These things get a little sort of , they get weird very fast.
I'm not very concerned about state actors.
I guess my concern is more , do we have some blind side on some economic nuance that gets missed?

## Drivechains & CTV

Antoine: 01:18:46

Maybe drive chains.
I don't know much about drive chains, but it's something that has been asked by people.

NVK: 01:18:52

Not going to happen.

NVK: 01:18:55

Maybe I should just bring it up,  the CTV.
I absolutely love the work that was put into BIP119 and , and Ruben, absolute brilliant kid.
But I think, a lot of people don't like this, but Bitcoin is still people.
People change software.
And 100 years from now, it's going to be different people.
So they may change the software very differently than we do now.
But once you burn yourself sort of  politically to the economic nodes, which are people, I find it extremely unlikey that you can do things, especially if they're very complex and they sound  some crazy shit that people can't understand like CTV.
So drive chains changes a lot of incentives, a lot of complication on Bitcoin.
I like to call it soft fork hell.
Because essentially that's what it is.
It's just going to soft fork Bitcoin for infinitum.
And then CTV is  absolutely amazing.
But God knows, man.
I mean,  it's just , I don't think my brain can comprehend what can be done with that thing to be able to say  with some, at least feeling confident,  it's not more than just dick butts.

James: 01:20:03

I think that's the thing, with I mean, so CTV,  you said, it's a very small patch set, but to your point, evaluating something  CTV, evaluating  Opcat,  these are very, they're simple mechanisms that can build a lot of different stuff.
And the conceptual surface area of what can be built is a lot higher than a proposal  check, lock, time, verify, or oP_vault, where You can fuzz test the shit out of the interface and be reasonably certain that you've  kind of exercised the full span of the space that it enables.
Whereas  with these more open ended things, it's harder to get an intuition for what's actually possible.

NVK: 01:20:49

Sorry, somebody dropped some bait here on the chat.
I am not gonna open any link that has drive chain on the URL.
to happen.

Ben: 01:20:57

There is blog post from Jeremy Rubin where he showed you could kind of recreate drive chains with any preval.
So , I mean, I'm a big fan of any preval.
I think there's a lot of cool things, but I am not a fan of drive chains.
So it's, there's a lot of weird things like this.

Antoine: 01:21:11

Yeah, exactly.
And we see it here as well.

NVK: 01:21:14

Yeah.
It's Funny, the people who have a more sort of  flexible, big composition space mindset really gets drawn to this.
you see this with  Fiat Jaff as well, big supporter of that, creator of Nostr, right?
And Nostr is  the complete opposite of Bitcoin.

## Unforseen consequences (ordinals)

NVK: 01:21:34

It's  rough consensus, but it's simple, very flexible.
That's not added a lot of rules.
Because also it's trying to do something completely different.
And I think Galaxy Brain sort of starts to get a little lost in what's acceptable to a certain purpose versus another.
And a lot of the pushback into new features and things on Bitcoin comes from this sort of , hey, can we not break this incredible amazing thing by just adding this one more thing that we really want.
Maybe this is a good segue to sort of start thinking , OK, great.
Let's say Opvault,  extreme low risk, at least it is in my view, adds an incredible amount of security that Bitcoiners are going to need, if we don't want to go to jail or get killed for our coins.
And I think that on itself is the sale pitch.
It's , listen, you don't want to get killed, kidnapped or  arrested
For your coins.
you want to have a peaceful sleep at night technology.

Rijndael: 01:22:31

Without enabling DickButts.

NVK: 01:22:33

Exactly.
Without DickButts.
Well, we don't know yet.
Maybe.
I don't know, man.
Casey, brilliant guy.

Rijndael: 01:22:38

Super creative.

NVK: 01:22:39 

he's he's going to find a way of  DickButting, internal contract.

Rijndael: 01:22:45

James mentioned this earlier.
Ordinals are compatible with vaults.
So you could vault your dick butt.
Yes.
it doesn't create new dick butts, but it does create new ways of securing your dick butt.

NVK: 01:22:55

By the way, we're doing an episode on ordinals.
Rijndael is joining me.

James: 01:22:59

Are you going to have Casey on?
Yes.
Oh, that'll be fun.

## Activating OP_VAULT

NVK: 01:23:03

Probably next week.
So anyways, how do we activate this?
How do we convince people?
How do we?
Because we can't even agree on how to activate shit.
And as I like to say, it should be excruciatingly horrible experience to try to activate anything, to discourage even the most hopeful people to not do it.
Because, activation is the ultimate bad attack surface of Bitcoin
it's adding shit to it.
So how do we go about maybe activating this thing?

James: 01:23:30

Just a few thoughts.
I mean, I don't want to play a massive role I mean, I don't want to unilaterally push this thing obviously because that just doesn't doesn't work But My hope is that the value will be so obvious and and that there will be people who take time to evaluate the proposal  you,  Alex Leishman did a lot of tweeting a few days ago, the CEO of River, about how valuable this would be.
I think the people at NYDIG are pretty positive on it.
And so I just hope there's kind of  this overwhelming sense of , wow, this is pretty low risk and pretty high value.
And, it's something that we want.
And the other note that I'd  to make is  there was a time where for things  check clock time verify, check sequence verify,  these were  purpose specific tools and their activation wasn't full of drama, wasn't this huge massive thing that people freaked out about.
And we actually did those , in rapid succession kind of around SegWit.
So I kind of hope, I mean, Segwit and Taproot have been very profound, complicated changes that have been, I think generally positive massively, but...

NVK: 01:24:39

It's a full change to Bitcoin.
We added a new crypto piece.

James: 01:24:42

It's  a platform change.

Rijndael: 01:24:44

It's a whole new thing.

NVK: 01:24:45

By the way, I want to do an episode on just explaining people what SegWit actually is.
I don't think people understand.

Rijndael: 01:24:50

It's so crazy.

NVK: 01:24:52

And VBytes and all the stuff we did that nobody understood.

James: 01:24:57

Completely.
Look,  I work on core as my full time job and I have to routinely reread, the BIPS for SegWit and Taproot because I forget all the details, and I forget all the nuance.
And when the ordinals and the inscriptions came out, I forgot that Taproot had removed the 10,000 byte limit on witness scripts.
So these changes are massive.
OP_vault, not massive.
And I hope activation can be,

NVK: 01:25:23.

So maybe the way we start addressing this is to explain that this is a gardening job.
This is not a construction job
I mean we're adding a small primitive
It's just , all the little things that we do.
Because again, people don't understand the difference between the little things and the big things
Maybe drawing sort of  analogies to ,  for example, lock time verify, , okay, so this one did this, up.
Vault is going to do this
And not sort of blow this thing up out of proportion, not try to say this is a massive feature, even though it does enable a lot of things.
I think how we frame this and how we sort of  start addressing the people that don't want changes, because, they're kind of right.
I mean, we don't want changes to Bitcoin.
We want just at least in my view, gardening.

Rijndael: 01:26:10

Well, and  something that I'm cautiously optimistic about here is I think a lot of times when people have software proposals, they end up in a chicken and egg situation of trying to prove demand, where it's , somebody's , oh, I want to build this new opcode that'll let us do coin pools.
And I think a reasonable pushback is , well, no,  demonstrate in the market that people want that.
Show that there's enough demand that it's worth the dick-butt risk to go and build coin pools.
I think what's cool is that because you can build vault-like setups that have a bunch of trade-offs out of things  pre-signed transactions, ephemeral keys, and relative lock times,  people  Re-Vault and other groups can go and build products in the market, have customers, and then say, hey look, even with these trade-offs, people want solutions that are shaped  like this.
Wouldn't it be great to be able to just eliminate a whole class of these trade-offs and have it be enforced by consensus rules instead?
And that might be a more compelling argument to the economic majority than just saying  here's a really great idea that I have.

Antoine: 01:27:14

Yeah I agree with that it would be useful for arrivals, but two things, first, I really don't want to be into pushing for consensus changes for my company.
And two, I actually don't think we should, well, not rush, but I don't think we should go with activating anything, well, not too soon.
So there's been a lot of covenant proposals floating around.
People are still working on covenant proposals that are not announced yet.
There is a lot of research going into it.
So I think it would be premature to activate anything.

NVK: 01:27:48

What would be the least disruptive way of getting this in?
Even if it was  maybe  not fully featured?

Ben: 01:27:56

I think something to keep in mind as well is  we don't have to do OpVault and that's it for Covenants.
we could do OpVault and TTV and APO.

Ben: 01:28:04

It's not going to be all at once.
Yeah.

NVK: 01:28:06

But the way that the people  if you use some EQ here, right, the way that...
A lot's true.
Yes.
Listen,  Bitcoin is politics.
It's people and you have to convince people.
So this is why I'm asking.
It's , what is the best way we can sort of  dip our toes into this?
Or , how can we propose  a way of activating this that is  not a big deal?
Because it's not a big deal.

James: 01:28:28

Yeah, so I mean, I was writing the bip before I got on this call.
I want to put that out there.
The implementation, frankly, is mostly complete.
There's a rich suite of functional tests that I've got to add some stuff to, but largely I've written a wallet, basically, to functional test this thing.
So the implementation's all there.
You can see exactly how it works.
So my hope is that I can put it out there and people can spend time getting familiar with it, maybe sketch out some, really do some in-depth thinking on what the use cases actually look  for end users.
And then hopefully it just becomes obvious that it's something we want and we activate it with a speedy trial or something like  that.
But I think Antoine makes a good point about not activating too quickly, but I do wanna push back a little bit and say, look, I'm not wedded to OpVault.
I came up with it,  it originated as a thought experiment.
I just wanted a benchmark against , what would the perfect vault construction be?
I wasn't even thinking about implementing it.
And then I was , oh, I should give it a shot.
And so I tried to implement it And it worked.
But if something comes around that's categorically better, I mean, I'm happy for that.

NVK: 01:29:35

That's often how it works.
I mean, Taproot had  50 different sort of ways that sort of went here and there.
Segwit was the same thing.
These things are never  the original proposal who really makes it.
Yeah, right.
And that's why I sort of , I guess I brought it up, maybe there is  a version that's  feels  more  a compromise.
It sort of  feels  a little bit more restrained.
And that's how you kind of start to get it in.
And then maybe it gets more featured as it comes closer to activation?

James: 01:30:03

The point that I wanted to make, though, is that custody is a real problem right now.
I mean, people are losing coins.
Insurance is basically not doable.
The situation right now is pretty bad, and we're all used to it, and so maybe we don't realize how bad it is, but it could be a lot better.
So I'm not really wild about the prospect of waiting three years for some ultra-perfect covenant proposal to come along that  maybe kind of emulates OpVault, I think I'd  to put the proposal out there, see what the objections are.
And if someone is , hey, I really don't  that we can, do this DLC thing with the pack

NVK: 01:30:46

if I have to , sort of  really address what I think it's gonna happen, is that it's not gonna necessarily, I don't think the criticism is gonna come regarding the actual nuances of OpVault
It's gonna be activation.
Is the idea is , the problem is, I think Speedy Trial  pissed off enough people.
Yep.
And it was kind of  felt rammed through by the cabal of core developers.
So there is that bad taste in the mouth of a lot of economic nodes out there.
The dick butts certainly did not help.
And I still think we don't have a good way of activating stuff.
And we sort of , we're a little PTSD from things.
So it's not going to be upvote.
It's going to be , I don't want to change Bitcoin.
Right.
So and I think a lot of the people who criticize changing Bitcoin, they are correcting the sentiment of not wanting to change Bitcoin.
But they don't also don't understand that  software doesn't live forever without gardening.
the stuff that's running on your computer today doesn't run tomorrow.
And you need the people who understand the code base to sort of upgrade it for new hardware, for new concerns, for, Unix time problems.
And there's all these things that need to change.
when my good friend Steve says, fire the devs, I understand why it feels that way.
And I kind of agree in a way because,  core, I addressed this in the last episode.
It kind of feels  this, it's  Internet Explorer has 99% of the market.
It doesn't rule the internet, but kind of rules the internet.
And, it has this sort of  bad taste by the CTV people as well, where, hey, if you don't get the right people on court to like your idea, It doesn't get activated to you.
So these are the gatekeepers.
But  realistically speaking in software,  there's always just  a literal handful of people who understand the whole banana and are the people who are qualified to truly have an opinion,  Facebook used to have five guys merging the code of 5,000 people, in our shop,  we have, Doc Hex.
And if he doesn't get through his shit,  it's not going to get through.
And very few people have the full picture of that code base.
And those people are often not the best people who are selling themselves or selling the code
So I think  Bitcoin is sort of  suffering at this right now.
that's the current sort of  cold and sneeze that Bitcoin has.
And, maybe OpVault is the simple thing that helps us find a better way of activating things and sort of talking about these things.
So maybe James, you're very good at sort of  tech and also dealing with people.
Maybe you should champion this.

James: 01:33:36

Well, I appreciate you saying that.
And I'll champion it to the degree that I don't feel  it's actually impairing the proposal.
Again, I don't want to Feel like I'm pushing this really hard and and I want to be clear I'm totally agnostic about our activation parameters to be to be frank.
That's not something I've thought a lot about so I Don't really care exactly how the activation works there are probably othe galaxy brains who can weigh in on that and suggest some stuff.
And maybe this process will motivate me to kind of play a bigger role in that and try and understand some of the different approaches a little bit better and the objections that people have.
But I think you're totally right there right now.
Bitcoin is a little bit wandering in the desert.
And, the last two massive changes have been led by a real small group of people.
And I think we all have this muscle memory of kind of relying on them to sort of say, okay, This is the blessed next step for Bitcoin.
And I think they very rightfully realize that that's not healthy.

Rijndael: 01:34:36

They earned that.

James: 01:34:37

They earned it for sure.

NVK: 01:34:38

I mean, listen, how many people in the planet can actually review LibSec?
seriously, like two?

NVK: 01:34:48

I mean fully understand what truly is going on in there.
I don't think there's more than two people.

James: 01:34:55

It's not a lot.

Rijndael: 01:34:59

You can definitely count it on one hand.
you could argue if it's two or four, but it's definitely on one hand.

NVK: 01:35:03

But this is  I think we do a very poor job at representing the technical problems to people who are not technical.
just conveying these realities, right?
people in this space,  my NCAP comrades, sort of  love to talk about meritocracy and things  that.
But, part of the meritocracy understanding that you have absolutely no fucking idea how Bitcoin works.
And you have absolutely no qualification to also understand what they're trying to change.
And there is always going to be a little bit of this sort of  bad taste of a technocracy, Right?
And it feels weird in Bitcoin, right?
Because it's your money, it's your node.
But you're trusting somebody else's code, especially if you can't read the code.

James: 01:35:53

And it's  the, oh, I'm sorry.
Did you?

NVK: 01:35:57

No, no, no.
Go ahead.
I was like how do we improve this?

James: 01:36:00

Well, I was going to say, the situation that it's very much  is taking your car to the mechanic, right?
you take your car to the mechanic, this guy knows what he's doing, but there's also a good chance he's trying to screw you.
there's also a good chance he's trying to charge you, 20 to a hundred percent more than you actually pay, maybe do some unnecessary work.
And so you're in this awkward position where you can't do this work yourself.
You can't even evaluate the proposed fix.
But you also don't want to get screwed.
And as we see in medicine, there can be situations where the group of experts is dead wrong.

NVK: 01:36:34

Or they're sold out.
I mean, there's a lot of different interests in Bitcoin.
We don't know people's motivations.
It is realistically impossible to know them.

James: 01:36:43

So it's important to retain your bullshit detector.
It's important to retain the culture that makes sure that no change in Bitcoin violates the property rights of the system.
But at the same time, I think the best you can do if you're not a technical person yourself is  you go out and you consult a lot of car mechanics, right?
You get a lot of prices.
And I mean, that's kind of the best that we can do.
But I don't know if you guys have other thoughts.

Rijndael: 01:37:06

Well, I mean, so another thing that is a relatively recent development is I think AJ set up Bitcoin Inquisition, which is,  let's proactively merge different software proposals into a SIGNET so that people can play with them on a shared network.
And so unlike some of the more ambiguous, ambitious big change proposals, Because OpVault is really targeted at a very specific shape of use cases, maybe there's an easier path here of it ends up on something  Bitcoin Acquisition, people can build little dummy wallets, and normal users can get a little bit of stick time playing with what would custody in a post-oP_vault world look like and demonstrate that this is better.
Even if you don't know whether or not the mechanic is trying to screw you, you can at least take it for a test drive first.
There might be some stuff  that where it's less about how do we go and win the rhetorical fight on Reddit, and it's more about what can we do to incrementally de-risk their proposal so that the community understands what they're signing up for.

NVK: 01:38:16

I mean, there was a lot of that at Taproot, right?
There was a lot of sort of working groups and things  that.
But Taproot still felt pretty like rammed through.

Rijndael: 01:38:24

I mean, I went and found  Optech did a workshop on Taproot, I think two years before activation.
So , You could write code and watch videos about Taproot, but people still felt  it was sprung on them.

James: 01:38:36

Taproot is just so hard.
It's so hard.
It's so hard to get your, I mean, I had to really, the only, I until very recently didn't, I feel , fully understand Taproot.
For this proposal, I had to write a bunch of tests that's all on taproot and there were things that I just kind of didn't understand.
I found it pretty difficult to get sort of valid taproot constructions and I basically relied on sort of the example code that other people had written.
So it was, it's a very, again, I'm massively positive on Taproot.
I think it's awesome, but it was  so difficult to get your arms around, even as a deeply technical person.

Antoine: 01:39:13

I wanted to address as well, you said that it was a small group of people, but while it's true that it was a small group of people that coded for Taproot, I found that it was there was a lot of demands and they definitely set a high bar.
Well there was a lot of demands, a decade of research.
When did we start discussing Merkle scripts?
2012 or something?

Rijndael: 01:39:38

Years ago.
Yeah, a decade of research,

Antoine: 01:39:40

a lot of involvement of a lot of people in the community with the workshops, a lot of involvement with the activation, and maybe that's why as well people are happy with it because they were actually involved.
And so, yeah, I think that did put a very high, not high bar, but reasonable bar for community involvement and normal user involvement.

Rijndael: 01:40:03

Well,  Shnorr is for a similar thing people have been wanting Shnorr in Bitcoin for years.

NVK: 01:40:08

See, the Shnorr is funny that you brought that up.
it's always been a concern of mine that , what if ECDSA is backdoor?
Right.
And it's not revealed for a long time and there is no proof for for ACDSA.
So, the idea of , and again, this is a fundamental change to Bitcoin, right.
Adding another crypto primitive, it's  crazy different.
So, but just having a secondary fallback crypto primitive in Bitcoin before we're big enough to state actors are going to that extent.
It's pretty cool.
Thanks Antoine.
Antoine is stepping out.
Appreciate it.
But now, , we have this sort of  the fights have always been hard, up return limit back in 2009, 2010, because people were concerned about the worst part of dick butts.
And then you had, say, P2SH was also a huge fight.
The original block size changed from 32 megabytes to one megabyte, SegWit was a bamboozle of most people.
People did not understand that the block size increased.
I don't know, I just hope that this one is not part of the contention.
We can find a path where this is the gardening sale, not the construction sale.

James: 01:41:22

I think the point Rijndael made is so good.
And what I love about the idea of people taking this for a test drive en masse with Inquisition is , that gives technical people who maybe don't want to work on core or don't have time to work on core, can't,  they can write tooling to kind of make this an easier process to be able to experiment with this stuff more easily.
So I just love that idea.

Ben: 01:41:48

I think something to keep in mind too,  NVK, you just went through all those different soft forks,  from  the original block size decrease to  stuff like segwit and taproot.
You didn't mention  CLTV or CSV or  BIP66 I think or 68.
there's tons of BIPs that are  worse off works that are just  are just normal things that happened and no one cares because they're  simple small upgrades that are super effective.

## Chain ossification

NVK: 01:42:15

Let's see, here's the thing.
As Bitcoin grows, right, and we have more people with their bags depending on it, the more you're going to have screech.
And that's a feature
you want this to progressively become more immutable, even as a feature set.
So , I think we're still in a place where  a few things could get in, but I don't think we're far from ,  a true ossification of new features.
Unless,  people come up with some more clever way of testing them out on main chain.
I don't I don't see how how this gets much easier.

James: 01:42:51

I just think it's just to spice up the conversation and throw in some opposition.
I think the counterpoint to that is that I'm really worried about some future where Bitcoin, the scale of Bitcoin is limited to what we have today.
And it becomes this gold asset where you as a regular person, as a non-institution, you can't actually take custody of your Bitcoin.
I just think that's a failure mode Because at that point, it's just  maybe a slightly better gold that develops a paper market, gets captured by governments to some extent, re-hypothecated, all that stuff.

## Bitcoin vs gold - attack vectors

NVK: 01:43:23

Yeah, I mean, can we just recognize that gold lost, it had a 5,000 year run
And it's an element.
It is a fucking , universe element.

Rijndael: 01:43:38

It conducts electricity really well.

NVK: 01:43:41

I mean, just  this thing lost, an element lost.
To human ingenuity.
The MMT guys are smart as fuck.
And they will find a way to try to gain Bitcoin.
I mean, FTX was a fiat maxi attack on Bitcoin.
They inflated the Bitcoin supply by, what, 20% for the epoch.
It's crazy.
It's absolutely crazy.
And Bitcoin not inflating is the whole fucking point.
So we're going to have to create defenses against fiat attacks.
It's not going to be the guy using the backdoor on ECDSA, extremely unlikely.
it's going to be  how they they capture, 60% of the Bitcoin custody in Coinbase.
And then they start inflating that.

James: 01:44:30

Exactly, because , look, changes that happen to Bitcoin consensus are in the open there that you can you can look at the Code you can judge it for yourself So if someone comes along and tries to change the supply schedule or the inflation rate  that's obvious And that's not gonna be a very effective attack on Bitcoin for that reason.
It's going to be exactly what you're describing.
It's going to be on these higher layers on the Fiat on and off ramps.
if they want to antagonize Bitcoin,  hiring an open source developer to go and try and sneak some change in is going to be totally ineffective.

NVK: 01:45:00

I mean, Operation Orchestra is in full effect
let's waste everybody's time with stupid shit.
But think about the whole game that just happened against Bitcoin
Total price suppression, coordinated or uncoordinated.
So you have the Fiat Max is doing and come on state backed  FTX
inflating the supply.
And then you have CME adding all the possible ways for you to short Bitcoin.
And then they don't give us a spot ETF to call these motherfuckers up.
So, and Bitcoin is extremely illiquid.
I mean, you have  it on spot.
you have  10% of all Bitcoin supply available on spot.
So  you can't call their bullshit.
And , if you just think about that for a second, it's , holy shit.
And this is not even  how far these guys can go.
I mean, this is  this is a Sunday play for them.
Right.

James: 01:45:58

Absolutely.

Ben: 01:46:00

That's also today,  it's something  only  10 percent of all Bitcoin is custodied on these institutions.
It gets worse without vaults, so you can't reasonably custody lots of Bitcoin safely.
It's going to move more and more and more on the coin base, and it becomes an even easier attack.

Rijndael: 01:46:16

And what's the natural market response?
Oh, well, I can't actually move my Bitcoin because it's too expensive because it's  locked up with 50 HSMs. So instead what I'm gonna do is I'm gonna transfer a paper claim on my Bitcoin, which is custody at this institutional custody solution.
And then you just start rehypothecating Bitcoin.

NVK: 01:46:33

Well, that's exactly what happened to gold.

James: 01:46:35

But NVK, to go back to  your point, I mean, it is vitally important that we maintain this culture of not changing the premises of Bitcoin, not changing the property rights.
And so people have to develop the ability to distinguish changes that are even remotely close to challenging that versus these gardening changes where it's , yeah, you can completely understand this feature.
It's not going anywhere near the viability of the system or the premises.
And, it's really I mean, Bitcoin is  America and America relies on the founding documents, the frameworks that are tangible, but it also relies on the cultural ethos of  pushing back on ambiguous situations that challenge the premises of the system.
So I totally believe , we need people out there who are skeptical, but you need to have the wisdom to be able to differentiate between things that are gonna help the system versus things that challenge its premises.

Rijndael: 01:47:27

Yeah, I mean,  one of the longest running debates in Bitcoin, which is , I think one of the juicier debates is should Bitcoin be money or should it be smart contract fuel?
I think that anytime somebody tries to introduce a change that allows for more expressibility of script or allows for more novel peg-in mechanisms or whatever, one of the pushbacks is, okay, well, Bitcoin isn't for arbitrary program execution, it's for money.
What's, hopefully the thing that people can distinguish is that OpVault or something like it is doubling down on custody.
It's making the money part better.


NVK: 01:48:03

Yeah,  my rule of thumb for Bitcoin, sort of  very, very rug brain,  sort of framework is, every single Bitcoin feature serves at the store of value pleasure
that's the king
Anything else you add in Bitcoin is for that.
Bitcoin having uncensorable transactions, it's because without that, you don't have a store of value, right?
Because somebody can just make you not spend or take it from you or block you.
So some privacy is for that, so that you have the privacy to transact your store of value.
So you protect the store of value, right?
So Every single change and every single thing that I see people trying to add to it, does it really fit that box and it's a small box.
I think that was one of the original sins of the CTV sort of  frame narrative.
It was  sort of unleashing this galaxy brain into sort of , look at all the cool shit they can do.
Oh my God, this is amazing.
it's , that doesn't really help with store of value.
So  go fuck yourself kind of thing.
And I think they're , if we can just  help people who are , who may be on the fence or who may be against this proposal, for example, just understand that  this does fit that small box.
This is  it's in the name and  this thing is to help you hold your coins and have property over your coins and not be capturable, I think this would move sort of  fairly fast and fairly straightforward.
And if we have more criticism that is  completely stupid and retarded, at rest is even better too, right?
We need to get things that are completely absurd at rest and raised even by us.
It's , oh, what if SHA-256 is broken?
Well, I mean, airplanes fall from the sky
Everybody can understand that.
So , 51% attack every all time high.
It comes back to Bitcoin.
Right, oh, it's not  that.
So  you have to have this sort of  very attainable China.
You have to have this very attainable, very  rug brain explanations of things because my pocket doesn't care about how complex and cool Bitcoin is, I don't want to have to think too deeply about these concerns with my money.
And I don't know, I feel  you've been doing a very good job from the things I've read and sort of seen about OpVault.
I guess that's where I wanted to do with this episode, is sort of  address it, see if we can pursue some paths here, reflect a little bit on it.
Is there  anything else you guys feel  we should address it or that we missed?

James: 01:50:50

I think we kind of hit on most things that I can think of.
But yeah, I'm just really thankful, for the opportunity.
it was a great group of people.
your analysis is really important to me because I think you're one of the best people that's set up to kind of evaluate something like this.
And so all I want is just kind of a continuing exchange of, Does this work?
Is this right?
And so I can't thank you enough for all that.

NVK: 01:51:20

No, I mean, listen, man,  I absolutely love the work.
I think you're approaching this with  a good cool head and  the correct humbleness because Bitcoin tend to humble us all in some way or another.

## Further reading

NVK: 01:51:37

It's essentially a kick in the nuts every day.
So , thanks Rijndael and thanks Ben, your contribution here was  super, super amazing.
Thanks Antoine, who had to leave a little early.
So guys, I guess  any final thoughts and maybe  further material for people to read, that would be great.
So Rijndael.

Rijndael: 01:52:00

Yeah, I think Antoine already left, but for me, I think one of the first times that the notion of Vault really clicked was I was actually reading the docs for ReVault.
So if you go to ReVault's page, they have a link about how it works.
And ReVault is really aimed at institutions, so you have to kind of squint at it and imagine how it would scale down.
But I think between that and the paper that James wrote about OpVault, if you read those, I think it kind of plants a good seed in the back of your head to start thinking about what vaults are, how they're useful, and how that could go forward.
So if you're interested in that, I would definitely look at those two things.

NVK: 01:52:40

Thank you.
Ben?

Ben: 01:52:42

Yeah, I just want to say, I think opvaults or any sort of a covenant proposal,  should we need this eventually in Bitcoin?
And we have some really good proposals on it right now and we should probably decide on one in the next few years and try to activate it.
This isn't going to be a whole re-architecture  we did with Taproot or Segwit having to as Coinbase said, support the setting to this.
This is gonna be super minimal and  a much smaller change set.
So it's not as risky or anything  that.
So I hope people can understand that and hopefully work on activating it.
Great, James?

James: 01:53:18

I can say it better than those two guys just did.
So thanks for bringing us on, man.
If anybody wants to find the opVault paper, you can just go to my Twitter at JamesOB.
It's linked right there.

NVK: 01:53:28

Shill it.
Seriously, tell people exactly where to find the stuff and where to read and what they should look into it.
People don't know.
And what should we add to the show notes?

James: 01:53:38

Sure, yeah.
So you can access the paper just by going to jameso.be/vaults.pdf.
So that's the paper I wrote.
I think it gives a pretty good summary of prior work, kind of a setup for the problem, and then the actual design itself with some nice diagrams in there that kind of make some of the benefits clear.
Then if you want to dive even deeper, There is a full implementation of it.
There's a pull request open in the Bitcoin core repository.
Embarrassingly, I don't know the number because I never remember those things, but it's there.
It's got a lot of functional tests, so you can kind of get a really good sense of what it looks , how it works, what the transaction structure looks .
I said earlier, I'm working on a BIP.
I'm really hoping to have kind of a final draft that I can circulate within the next week or so after I get a little bit of feedback from people.
And then, yeah, beyond that, I think just, if you have any questions, hit me up on Twitter at James OB and we can talk about it.

NVK: 01:54:36

Just for the record, I mean, James is one of the friendliest people around with one of the biggest galaxy brains that's completely hidden in that pretty face.
So do reach out to him.
And , I'm certain that he will politely explain things and and try to convey to you without pushing.
really,  if you can't understand this stuff, because really nobody can, reach out to people and try because it is worth it.
We want a Bitcoin future where people don't get robbed or lose their coins.

James: 01:55:10

You're too kind, man.
Yeah, absolutely.
Thanks for having us on.
And it was a really Great discussion.

NVK: 01:55:16

Awesome, guys.
Thank you so much.
Ben, I'll see you in the kitchen in  five minutes.

Ben: 01:55:20

Yeah, I'll see you.
Thanks.
See you guys.

NVK: 01:55:24

Take care.

Rijndael: 01:55:25

See you guys.
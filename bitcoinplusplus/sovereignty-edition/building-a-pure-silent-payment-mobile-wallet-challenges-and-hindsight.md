---
title: 'Building a Sovereign Silent Payments Mobile Wallet: Making Silent Payments Practical'
transcript_by: 'muchai254 via review.btctranscripts.com'
media: 'https://youtu.be/MgoPkXHUH0E'
date: '2025-12-15'
tags:
  - 'silent-payments'
  - 'wallet'
  - 'privacy'
  - 'cryptography'
  - 'compact-block-filters'
  - 'btcplusplus'
speakers:
  - 'Cygnet'
categories:
  - 'conference'
source_file: 'https://youtu.be/MgoPkXHUH0E'
summary: 'Cygnet presents Dana Wallet, a pure silent payment mobile wallet built with co-developer Sofstein, covering BIP-352 fundamentals (ECDH-derived unique addresses via input-hash-summed-private-keys times recipient scan key), the two core receiver-side challenges for light clients (needing per-transaction tweak data and scanning every taproot output in every block), and two implementation iterations — an initial Electrum-Rust plus Nakamoto BIP-158 approach and a more mobile-friendly Blindbit Oracle over HTTP. Benchmark results show a budget Motorola phone scanning 16 months of chain history in 6 minutes, made feasible by the finding that 95% of UTXOs are spent within two months so old fully-spent transactions can be skipped, with the talk closing on BIP-353 human-readable addresses as a near-term UX improvement that could eliminate displaying raw Bitcoin addresses entirely.'
---
## Introduction: Why We Built a Sovereign Silent Payments Wallet

Cygnet: 00:00:16

All right, yes, so hello everyone.
My name is Cygnet and for the last two years or so I've been interested in silent payments.
I think it's going to sort of nerd snipe me for like two years now.
More specifically, me together with Sosthene, we have been working on a specific type of silent payments wallet, which we call, I guess, a sovereign silent payments wallet.
So yeah, I'm going to talk about that, but before I'm talking about my wallet and to give you a good idea of why it's sovereign, I think it's first important to give a quick overview of what silent payments itself actually is.

## The Privacy Problem: Address Reuse

Cygnet: 00:00:57

To understand silent payments, we first need to talk about the problem that silent payments is trying to solve, which is address reuse.
So I'm sure I don't really need to tell the people in this audience that address reuse is something that you generally should be trying to avoid.
This was known basically from day one, I think, technically even before day one, because it was in the white paper that you should not reuse keys.
You know, for privacy concerns.
But despite that, address reuse is actually super prevalent.
So here are just two examples that I screenshotted.
So the one on the left here is the donations page for GrapheneOS.
Now GrapheneOS is obviously a very privacy-conscious project, so you would imagine that they care a lot about privacy, yet they even on their donation page, they use this single, you know, like just normal hard-coded Bitcoin address, 
And of course, if you can essentially everyone can just look this up and they can kind of see what, you know, how many people have sent funds to them.
So that's one example of, you know, like people using or people often like still doing address reuse.
Another example is Bitcoin exchanges.
So to the right is a screen shot of a Bitcoin exchange.
For exchanges, it's generally just more user convenience.
So if you want to withdraw, especially in Europe, it's sort of starting to become customary that you have to verify the addresses that you own, and that is because impartially it's for compliance reasons but it's also just more convenient.
Like if I'm a user, I want to be like sort of good, have good privacy, you kind of just need to, like, verify an address like every time you want to withdraw, but nobody does this, so it's much more convenient to just use the same address.
So, yeah, this is just a big problem, and this is something that silent payments is trying to tackle, basically.

## How Silent Payments Use ECDH

Cygnet: 00:03:04

So the way that if I wanted to describe silent payments in a single sentence, I would say that silent payments is trying to counter address reuse with the use of ECDH.
So ECDH, elliptic curve Diffie-Hellman, it is a cryptographic scheme that is pretty popular, and it is like a scheme that's two parties that have a public-private key, can sort of without really even interacting with each other, they can form a shared secret together.
And this requires private and public key pairs, and as it happens, most Bitcoin transactions tend to use public-private keys.
So if you think of a normal Bitcoin, a common Bitcoin script is like sending to Taproot or sending to like a Witness Public Key Hash (P2WPKH), you're basically sending to a public key, and when you spend it, you are actually using the private key to spend it.
So there's private-public keys here.
And so the idea of silent payments is that we can exploit this fact, the fact that a lot of transactions on chain are using private-public keys to create a new address.
So this function you can see here, that is kind of in a nutshell what silent payments is doing.
So normally you would kind of send to a public key, which is I call P_recipient, but now instead of sending it to that directly, what I'm going to do is I'm going to use Diffie-Hellman to calculate the shared secret, and I'm not going to send to the address directly, but I'm going to tweak the address with the shared secret, and I'm then going to send it to that address.
And you know, so this is sort of unique per sender-recipient pair, so that is what avoids address reuse.
Before I continue on, I think I first want to quickly mention that in a silent payment address, we have two different keys, a scan key and a spend key, and these are separated out because we will get into this, but, you know, for a silent payment, you need to do a lot of scanning, and it's useful to have a separate key for this, because maybe you don't want to always have the spend key in memory when you do this.
There's a bunch of other reasons for it, too.
But that's short of it.

## Sending and Receiving Silent Payments

Cygnet: 00:05:21

So yeah, that was silent payments in a nutshell.
I'll just quickly go over how you can actually do a silent payment.
So first of all, if you're a sender, you need to do use or spend from an output that is using public keys, or using public-private key pairs, so these are some script types which, again, this is not a very high requirement because these are very popular script types.
So you need to have at least one of these in your spending transaction.
Then using the private keys from the inputs that you're trying to spend, you sum up the private keys.
The reason you sum them up and not just take one at random is because this is slightly more convenient or this is more convenient to do, like, collaborative transactions.
So you sum up, you create this a, which is the sum of the private keys.
Next you also need an input hash.
So the reason here that we take an input hash is because just using the sum of the private keys, it's possible to create transactions reusing the same keys.
So like you can imagine if you have if you already have like an address and you spend from that address twice, you can you're kind of reusing the keys, so just taking the creating a secret just from the private keys itself doesn't guarantee uniqueness, but we guarantee this by taking this input hash which is essentially just the outpoints and then hash, and because outpoints are related to UTXOs, and UTXOs can, of course, only be spent once.
If UTXOs could be spent multiple times, then that would be like a double spending problem.
So that is essentially that kind of guarantees that this address that we create is unique.
So next we create a shared secret.
This is the input hash times the A sum times the B_scan, which is the scan key for the recipient that you're trying to send to.
And then finally, we calculate what the resulting on chain output looks like with this formula.
So P is you have the shared secret, so you send to the B_spend, which in the previous slides would be what you would normally send to, but now we don't just send to the B_spend, we also send to a B_spend summed up with the hash of the shared secret multiplied by the generator points and make it a public key.
So that is what makes it unique.
Then on the receiving side, this is this looks actually very similar to the sending side, that is because, you know, it is actually following the same steps, but now instead of taking you're sort of doing it from the perspective of the receiver, so on the input side you're actually looking at the public keys which is shown with a capital A, so capital A is the sum of the input public keys, and now we have this b_scan which is like a small b, so that's the private key for the scan key.
So however, the A is the same, the input hash is the same because it follows the same principle, and the shared secret is also essentially the same because this is the Diffie-Hellman scheme.
That also means that in step five, the resulting on chain is calculated, you basically arrive at the same result as the sender would.
So that's how a receiver can derive the same address.
However, only the receiver is able to spend this address, so you can see this function at the bottom.
Of course, the right side, the two parties know the shared secret, but only the receiver knows the private key, knows the spending key, so only the receiver is actually able to spend this output.
So this is basically how you can do both sending and receiving.

## The Main Challenge: Efficient Wallet Scanning

Cygnet: 00:09:23

In a nutshell, or the way I've just described, it might sound to you like, okay, this seems pretty straightforward, so what is the catch here?
Because if it was that easy to solve address reuse, then why haven't we done this like 10 years ago?
So the catch here is that this process, especially for the receiver side, is very incompatible, or it looks like it's very incompatible with light clients.
So on the sending side, it is relatively straightforward.
All of the extra data that you need is, it's already part of the transaction.
You need to do this extra, like, calculate the shared secret, but other than that, it's basically not that much extra unique stuff.
However, on the receiving side, there are two problems that you need to solve before you can, you know, find these addresses.
So one of them is that you need extra on chain data.
So we have both this input hash, and we have the sum of public keys.
This is part of a transaction.
Normally, light clients, they basically just have a list of addresses that they're interested in, and they have their own ways of finding, like, if there are any funds on those addresses.
So maybe they query an Electrum server, or maybe they use a compact block filter or something.
But the point is they kind of know what scripts they're looking for.
However, in our case, we don't know what those scripts look like.
We have to calculate them.
And we need on chain data for this, or we need this extra piece of data.
So we need to be able to provide this to the light clients.
And also, another very big problem with silent payments is that, and this is kind of a good thing but also a bad thing, is that silent payments outputs, they look like just any other Taproot output.
They are just sort of indistinguishable from normal Taproot payments, which is great for privacy, but it also means if I'm a receiver, I don't actually know if a certain transaction, if I look at it, I don't immediately know if it's a payment that is coming for me.
The only way for me to figure that out is by assuming, OK, imagine if this was a payment that comes to me.
What would the output script, what would the address look like?
So I would have to do this, I have to go through this receiving step, I have to take the input hash, I have to take the sum of the public keys, I have to calculate the shared secret, then I have to calculate the resulting address, and then I finally I check if the address are in the outputs of the transaction.
Now, 99.9% of the time, that is not going to be the case, because most payments are not for you.
But that is the only way that a silent payment wallet is able to determine if you receive any payments.
You just have to brute force basically every single transaction there is.
So this creates a huge extra what we call a scanning step.
And we need to, like, you know, you can kind of imagine when silent payments was first proposed, that this was considered a death sentence, that this seems like it's way too much.

## Making Silent Payments Work for Light Clients

Cygnet: 00:12:40

However, I think for both of these problems, there are some mitigations.
So the first one is actually not that big of a deal.
We need some extra bit of on chain data.
We need two things.
We need the input hash, and we need the public key, or the sum of the public keys.
So this is something that is essentially all public information, which means that if you want, you can have like some sort of a server that can, for a given block or whatever, can create like an end point that gives this data to you.
So this is called a tweak data, or a tweak.
This is something that is unique for every transaction, and using this tweak, a recipient is able to calculate the shared secret, because, you know, the shared secret was the tweak and the public key sum and the input hash.
So this is just enough for any silent payment receiver to create or calculate the actual resulting on chain address.
So that's great.
That solves the first problem.
Next is the second problem, which is the huge amount of data you have to process, so this is by itself seems insurmountable, but one important aspect that is of relevance here is that, you know, if you're a light client, A lot of UTXOs in Bitcoin, they tend to get spent pretty quickly.
So you can kind of imagine if a UTXO has already been spent, or if a transaction has outputs that are all spent, then at that point, none of those outputs are going to have any financial value.
So if you just want to check if you have funds on your wallet, then you don't really even need to scan these types of transactions.
So just to give kind of an idea of how much data this can, like, basically save, I did some pretty, you know, I wrote like a script that just kind of looks at the UTXOs from like a range.
I think I took like the last 20,000 blocks.
I just look at all of the UTXOs, and I looked at how long it takes for these UTXOs to get spent.
As it turns out, from my measurements at least, 50% of UTXOs that get created tend to get spent within two days, And, after two months, 95% of UTXOs that get created get spent again.
That means that if we're a silent payments wallet, and we want to find out if we have funds, if the data that we're scanning is more than two months old, then we can already basically drop 95% of the data.
So that is a pretty huge performance saving.
And it can basically be considered that silent payments would have been completely infeasible without this, but with this, it seems like it might be possible, and, of course, seems like it's kind of the second part of this talk, the point of the second part, which is what we have been working on.

## Building Dana Wallet

Cygnet: 00:15:47

So all of up until what I've mentioned just now was sort of theorized in the silent payments BIP.
But it wasn't really like it was sort of theorized that light clients were possible, but it wasn't really like tested out.
So this was kind of the reason that we started to work on our project, which we call Dana Wallet.
So, yeah, we just initially started it just to see how difficult, how expensive is it actually to create a silent payment light client.
And eventually we realized pretty early on or pretty quickly, like, OK, this to us seems to be pretty acceptable.
So now we kind of want to show it to other people, like, OK, this might actually be possible.
And so we kind of came to the realization, like, let's turn it into a proper wallet.
Because that's basically the best way to convince people, is to actually show an example of it.
And so, yeah, that's how Dana or Donna kind of got formed.
Our target use case that we imagined our users to be is to use it for is donations.
So donations is a very typical example of every now and then you may receive payments to your address, you know, It's not a lot of data, so you don't want to be sophisticated and run a full node.
You just want to check maybe every couple of weeks, maybe every month or two.
So not very often.
But you also want to make use of this reusability concept that silent payments bring.
So we thought that was a good target use case.

## Version 1: Electrs + Nakamoto

Cygnet: 00:17:22

So we did basically two iterations of Dana Wallet.
In the first one, we kind of built out 
Our first iteration was based on two software projects, one of them is electrs, which is an Electrum implementation in Rust, and we just slightly modified electrs to have like this tweaks endpoints
So this tweaks is what I talked about, this minimal amount of data that you need to find outputs.
And the other software thing that we use is Nakamoto, which is a BIP158 client
So the process for us in this first version was we first get the tweaks from electrs for a particular block, then we calculate the resulting addresses that may possibly have payments, may possibly have, like, funds on them.
Then using at that point we kind of have, like, a list of output scripts.
And at that point, it's very similar to a normal wallet would be, which is you have a list of addresses that you're interested in, and you just, in this case, we requested this, we requested like a compact block filter, a BIP158 client filter, and we just checked, okay, is this block interesting to us?
If not, we skip it.
If it is, we download the block and scan all the transactions.
So this was, this approach seemed to work, it seems like technically to work, however, we had a lot of issues like which are kind of just like probably a consequence of the fact that we were not that experienced with building for mobile clients, so we had to run a BIP158 client which is a continuous process and we had to run this in your mobile app.
So yeah, this caused a bunch of overheads or a bunch of, yeah, this was just a lot more complicated than we probably needed it to be.

## Version 2: Blindbit Oracle

Cygnet: 00:19:32

So the next thing we did was we switched over to another back end, which is called Blindbit Oracle.
So Blindbit Oracle is a project by another person in the silent payment space which is sort of like a minimalist server that you can use to basically, like as a light client, can use to receive and send.
So this is actually very similar to the previous approach, except this time.
So a Blindbit Oracle is kind of like a tweak server plus a BIP158 client, but over HTTP.
And because HTTP, this is a lot more much more common procedure in the mobile space to have just to make HTTP requests and responses and process these sorts of responses.
This was actually a lot more manageable for us.
So this was really nice.
The other workflow is essentially it looks very similar to the previous one, so you first get the tweaks.
You also query the filter.
In this case, the filter, it's not quite a BIP158 filter, it's a slightly modified filter that only looks at Taproot outputs, but it works more or less the same.
We calculate the output addresses using the tweaks, then we check this filter if there's a match, if there's not a match, okay, this block isn't interesting to us.
If there is a match, we then use this other query endpoint that Blindbit has, which is like the UTXOs. 
So you can basically request the UTXOs that are in a specific block from Blindbit.
Again, it's slightly modified to make it more compatible or make it easier for silent payment wallets to use, but it's functionally it's very it looks very similar to like a BIP158 client.
So, yeah, we loop over these simplified UTXOs and we just add the outputs that are interesting to us if we find them.
So one important thing to note here is that the first two steps here, getting the tweaks and getting the filter, those you kind of have to do for every single block, and the third step, which is calculating the output vector, this is the part that is really computationally expensive.
So one thing we can do is we can kind of, if we scan block N, we can, while we are processing the tweaks for block N, we can already do web requests for all the blocks that come after it.
So that means that basically, you know, networking and computation are sort of done concurrently.
So one of these is going to be the bottleneck, and the other one we can kind of do for free if it's on.
So yeah, that was basically the iteration that we use right now.

## Performance Benchmarks

Cygnet: 00:22:28

Now I want to talk a bit about what are the actual results of what we have.
So here I have some measurements that I made.
So these are benchmarks for how long it takes to scan a certain amount of blocks, a certain block range.
So I kind of just used phones that were lying around, so these may not be the most representative of what people use, but this was sort of a nice range for me.
On the left side is a Motorola phone, which is a more cheaper phone.
It was like a slightly older phone.
And on the right is a more high-end phone, a Pixel 9.
And what this shows here is basically the amount of time it took to scan this amount of data.
So I think especially the lowest row is probably the most interesting one.
So just looking at the Motorola, for 16 months, which is like one and a quarter year, it took the Motorola, the cheap phone, it took it six minutes to scan 16 months' worth of data.
I think personally that this is totally acceptable.
This is kind of the point where the technical element sort of drops away, now it's more user opinion, like, what do people think?
Do people think that waiting for six minutes is acceptable?
Now I will say, like, six minutes or this 16 months is kind of like the most extreme case.
This only happens when you do a full wallet recovery probably.
Most of the time you don't even need to scan 16 months' worth of data.
So I think for a worst case, six minutes is pretty good, but of course, that's kind of not really up to me.
It's everyone that uses a wallet, they sort of have to decide if this is worth it for them.
But, yeah, I think these results are pretty nice.
I will say one caveat is that this was all using a blindbit that was running on my same network, so basically this is more of a benchmark that shows the computational side, because we assume that if a blindbit is running on your local network, all of the network stuff is kind of instant.
So this is just to show how long the processing of data looks.
So maybe your results may vary, but they always vary, of course, because you can have different hardware, you can have different network connection speeds.
So it does give a pretty decent picture, at least, I think, of the processing time.

## Future Improvements with Silent Payments

Cygnet: 00:25:10

So yeah, I think, oh, yeah, finally, I just wanted to say, okay, now we have kind of a working light client silent payments wallet.
Because we now have sort of access to this reusable address, we can finally start to think about other things that we can do with, like, a reusable payment code.
So yeah, one of the pretty obvious ones is BIP353.
So BIP353 is like this email address-looking format.
This is already in use, I think, for example, by Phoenix Wallet, this is pretty popular, but it's also possible, especially with something like silent payment, it's possible now to also do this on chain.
So if you use this BIP353 approach, we can kind of basically create a wallet that just can completely drop showing Bitcoin addresses at all.
We can basically create a user experience that is only built around this sort of email address like user experience.
So I think that is pretty cool, and there's a bunch of other improvements that you can think of, but obviously that is for another time.

## Closing

Cygnet: 00:26:25

I think for now that was basically all we wanted to show, so if any of this sounded interesting to you, We really would like to get feedback on our app.
We have only been testing it out mostly between ourselves and some people that we talk to.
But if any of this sounded interesting to you, please check it out.
We have a website here that you can see for more information.
We have an Android repository to download the app.
Right now, it's still only on Android, or you have to download the APK.
But we kind of want to release it on the Google Play Store and the Apple App Store.
So hopefully, we can get to that early next year, but that was it.
Thank you very much
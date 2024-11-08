---
title: Lightning - The Transfer Layer
transcript_by: Will Clark
tags:
  - lightning
speakers:
  - Fabrice Drouin
media: https://www.youtube.com/watch?v=CGE8I8L7BAc
---
Location: Chaincode Labs Lightning Residency 2019

## Context

Fabrice: Alright so, I'm going to talk about the payments model we use in lightning, which is mainly the HTLC, and how it works. So what we've explained so far is that a channel is basically a funding transaction that's been published. And a commitment transaction that spends from the funding transaction but is not published. So the funding transaction is confirmed and it's on-chain and it sends money to A and B. The commitment transaction is not published, but it's publishable which means it's signed properly and other things, and it spends the funding transaction.

Basically lightning, when it's being used, it looks like this. You have a funding transaction and Alice and Bob at all times each have a valid commitment transaction that they could publish, they won't, but they could publish it. And lightning is basically about how to update these commit transactions so that you shift some of the money from Alice to Bob and back. For example in this case, the first commitment transaction gives everything to Alice, 10 bitcoin to Alice and nothing to Bob. The second one gives 3 bitcoins to Alice and 7 bitcoins to Bob. So some funds have moved, 7 bitcoins have moved to Bob's side. And the last one is 4 bitcoin to Alice and 6 bitcoins to Bob, so Bob has given back 1 bitcoin to Alice. This happens off-chain and when happy, Alice and Bob can decide to close the channel and publish a closing transaction that goes on-chain. So the trick is, how do you actually update your commitment transaction, how do you actually procure the model for payments?

And this is what HTLCs are about. So basically you have this, a funding transaction and a commitment transaction, and you want this. So, how do you get there in a trustless way?

And the payment model used in lightning is HTLC, which means Hash TimeLocked Contract. "I will give you some money for the preimage of a hash, and if you don't give me anything, after a while i'll get my money back." So I guess that everyone knows what preimage means? There is a [BIP](https://github.com/bitcoin/bips/blob/master/bip-0199.mediawiki) which tries to formalize what HTLC means, so that's not the script that we use in lightning, this is the script that's described in the BIP. The actual scripts in lightning are a bit more complex because we have to mix payments and revocation. But basically that's the idea. On the first branch of the, if you have, you check that you do have a valid preimage and if you do, you use the seller’s public key, and, I think that's reversed... On the second branch of the IF, there's a timeout and after the timeout you give money, no no that’s right. First branch, if you have the preimage you give money to the vendor, the one who wants to be paid and after a timeout on the second branch you get your money back.

This has also been described a bit earlier by Rene and Christian, but we have a two-stage structure for transactions in lightning. So you have the commit transaction, it has several outputs: one for you, one for the remote party and one output for each pending payment. These pending payments are spent by a second-stage transaction, so offered payments are spent by the timeout transaction and received payments are spent by a success transaction. And each of these outputs has a, some kind of circuit-breaker, that gives money without any other conditions to Bob if he has the revocation key. So that’s the trick that was described earlier; that's how you revoke an old state. If you know the revocation key you can just spend all the outputs.

A payment we request in lightning is, looks like what you need for an HTLC, what you need is an amount, a delay and a payment hash. That's basically what you have in a lightning payment request. Amount, hash and delay. You can also have optional fees, a description, routing hints, but basically when you scan a lightning payment request you'll get, amount, hash, delay and of course the ID of the destination node that you actually want to pay.

What also is very important in lightning is that the merchant creates the preimage. So it will be a random value, random preimage, the preimage will be sent to the buyer using QR codes or whatever, it could be an SMS it could be anything, and then the rest happens off-chain. So for example if Alice wants to buy a pic of a cat from Bob, Bob will display a QR code which says "send me an HTLC for 2 bitcoin redeemable with the preimage of that payment hash".

Alice will create a new transaction for Bob, so that's very important in lightning, when you send signatures, you send signatures for the other party's transaction. Alice when she sends a signature to Bob, she signs Bob's commitment transaction, not her transaction. So what Alice will do is she's going to take 2 bitcoins out of her own balance and move them to an HTLC output of 2 bitcoins to Bob, redeemable against the preimage of the hash she received in the QR code. And she's going to sign that new commitment transaction, and send the signature to Bob. Bob is going to send back the revocation secret for his previous commitment transaction and a new commitment point that will be used to compute the new commitment transaction. Alice will then check, so basically Bob has this: he has a pending payment of 2 bitcoins and he's going to sign the revocation secret for the previous transaction, that looks like this.

Alice will check that the revocation secret is valid, so the secret matches the revocation point she was using in the previous commitment transaction. And now that Alice knows that secret Bob cannot use these old transactions any more. Bob will sign Alice's view of the network, Alice's commitment transaction, with the same structure: Bob will move 2 bitcoins from Alice's balance to a new output with the same payment hash and amount. Alice will send her revocation secret to Bob and now Alice and Bob both have a commitment transaction with an HTLC output of 2 bitcoins redeemable by the preimage of the hash exchanged in the payment request.

What this means is that, now, if Alice learns the preimage of 'H' then she has the money. Sorry, she's paid. The bitcoins are moved from Alice to Bob. So Bob will send the preimage to Alice, Alice will check that the hash of that preimage matches the payment hash. And she will remove the pending HTLC and add it to Bob's balance. She will sign again that transaction and send it to Bob. Bob will again send the revocation secret, a new commitment point. He will sign Alice's view of the commitment transaction, he will remove the pending payments and move the money to his own balance, and Alive will send a revocation secret and new commitment point.

You see now, 2 bitcoins have been moved by Alice, from Alice's balance to Bob's balance. Alice has sent 2 bitcoins to Bob. This is what happens in a local channel between Alice and Bob. And now they both have fully-signed commitment transactions with updated balances.

If you have questions, don't hesitate to ask. Don't wait until the end of the presentation, just ask.

This can be extended to multi-hop payments if you re-use the same payment hash along all hops. So basically suppose that Alice wants to pay Carol, but she doesn't have a direct channel to Carol, she has to go through Bob, it would be exactly the same thing. Carol will display a QR code that says "send me an HTLC for 2 bitcoins". Alice will use that QR code to create a payment of 2 bitcoins to Bob for the same preimage, and Bob will create a payment of 2 bitcoins to Carol for the same preimage. Something that is really important to notice is that Bob will only create a pending payment on this side of his node, when both commitment transactions, Bob's and Alice's, have been signed. So before you forward a payment you need to wait until both your transactions are signed. So once Alice and Bob have signed their commitment transactions, Bob will forward the HTLC to Carol and Carol will send the preimage back. Bob will send the preimage back to Alice and he will do this right away; he doesn't need to wait until it's been signed by him and Carol. As soon as you have a preimage you use it on the upstream channel. You don't need to wait. As soon as Carol has a pending HTLC in her commitment transaction, she's been paid. Basically there, Carol has a commitment transaction with an HTLC output that says "OK you get the money if you know the preimage". Obviously Carol knows the preimage, so she's been paid. She doesn't need to wait until the transaction has been fully updated and the payment is gone.

So the preimage goes back to Bob and then back to Alice. Alice has paid, and Carol has been paid.

From Bob's point of view, his overall balance has not changed, he's just moved money from one channel to the other. Basically that's why lightning is really special when it comes to payment networks because it's a payment network that is not custodial. Typical payment processors, when you use a payment processor for Visa or whatever, your customers will pay your payment processor and your payment processor will pay you after a while. This is really different. Bob is not really holding funds that belong to Carol and Alice. So from a payment point of view, even though it's not clear-cut yet, from a regulation point of view, Bob is not a custodian as in traditional payment gateways.

There are limitations to this, for example what happens if you reuse a payment hash? Suppose Carol's program for creating payment requests is really bad because it's Javascript and when you reload the page you start with the same values, and I'm not making this up, do you know what happens when you reuse R values in ECDSA signatures? Is it something you've seen?

Audience <Inaudible>

Fabrice: Yes, so basically signatures in ECDSA are a couple of numbers, usually you call them R and S. R is a random value and S is the result of a computation that includes your private key and the message you want to sign. If you reuse R values, basically you have two equations, two unknowns and it’s game over, you know the private key. All it takes is two signatures with the same R value and a different message obviously, it was a hack for the Playstation and for many many printed bitcoin wallets using Javascript because it's really hard to generate good random values. Very very hard. A lot of attacks actually target bad random generators and the stupidest generators you can use are the ones that start from the same value when you just reboot your application, which is something that can happen to you very easily if you're doing Javascript in web pages and you're not really careful about what happens when you reload the webpage.

So in the case of Carol, if she reuses payment hashes, basically Bob, when he sees the payment with the same payment hash he says "OK, I'm not going to forward the payment, I'm going to send the preimage back to Alice, I'm gonna get paid and Alice will get a preimage." This is extremely bad because Alice has a valid proof of payment. Carol never saw the money the second time but Carol, if there's a conflict between Alice and Carol, Alice will say “I have a payment request that you've signed, signed by Carol's node, and I have a preimage that matches the payment request.” It's really bad. If she was buying something then Carol has to send the product to Alice.

Reusing preimages is really bad and it's really bad to get yourself into a situation when you actually, unknowingly reuse random values.

It's also bad for privacy because, it's, the same payment hash and R values are used along all the hops. So if you find yourself in two different places along the route and you see the same payment hash and same preimage, you know it's the same payment. They’re not randomised at every hop. There's a proposal for switching from payment hashes and preimages to private keys and public keys, where you could rotate the public keys at every hop, but it's not ready yet. So right now it's also a privacy issue. The fact that the hash is the same along the route is not too good for privacy.

Question:
Audience: If I just basically lied about <fee drop-off?> method, that's also provable right?

Fabrice: What is provable?

Audience: Er, that I just routed through the destination back to me and <drop off?> without a payment hash? Does that have the same provable...? That doesn't sound right?

No, the proof of payment is a payment request, that is signed by whoever is selling things. And the preimage matches the payment request. And it's a trick that's been used a few weeks ago to demonstrate how you can implement lightning payments in offline vending machines. If you find the trick, I think, perhaps this is something we'll be talking about in the next few days?

Decker: I may have a part on spontaneous payments but...

Fabrice: OK but if you reuse ECDH to create payment hashes that someone along the route knows how to find the preimage for, then you can create payment requests that can be paid even though you don't have an internet connection. So a lot of people are looking at this for vending machines and basically if you do that, all you need to do to prove that you've paid is show the vending machine a payment request and a payment hash. Then, since the payment request has been signed by the vending machine, it knows it's been paid and it can deliver the goods. There are lots of projects working on how to implement offline payment reception, and that's a cool trick that can be really useful for these types of applications.

Audience: So if the vending machine is completely offline...

Fabrice: That's your vending machine, I'm your vending machine, I'm offline, I don't have an internet connection. I will create a random preimage, turn it into a lightning payment request and show you a QR code like this. It includes the node ID, my node ID, well, not the vending machine's node ID, but the vending machine basically is owned by a company who has a node somewhere on the lightning network. So the vending machine has been set up and I know the node ID I'm supposed to use, so I will generate the payment request and I will use a trick with EDCH so that when Christian [the vending machine] sees that payment hash, he knows how to compute the matching preimage. So you want to pay, you scan this, you will send the payment and you will receive the preimage since Christian, since even though he has no internet connection to the vending machine he knows how to compute the preimage for these payment hashes, so you will receive the preimage back and you will have paid. And all you need to do to get the soda or whatever you’re trying to buy is to show me, with a QR code for example, there's a camera on the vending machine, the payment request and the preimage you got from Christian.

Audience: So the offline machine doesn't even have to implement lightning at all, just preimage and hash stuff?

Fabrice: Yes, and it needs to store preimages that it's used before. It’s very simple to implement.

Audience: It has to assume that your own node is still active?

Fabrice: Yes.

Decker: It doesn't really change much if i'm offline, you simply won't get the preimage and you won't release whatever you were buying.

Audience: I don't quite understand the ECDH part of it, but for instance if you were just generating a random number, the seed, that you (Christian) also had, that would accomplish this thing?

Decker: It would, so the trick he's actually using is basically, he's not giving an invoice that pays to me, but he's giving you an invoice that pays through me to some virtual node that sits behind me, so when I get this incoming payment, I am being told where to forward it, but of course this node does not exist really. So I have some data that he can transfer through the invoice to me and I can then use that information to mix in into my preimage generation. And that allows me to then recover the preimage from whatever he decided.

Audience: So if you look in the onion, there's this ephemeral key that you forward right? And this ephemeral key is partly used for the ECDH exchange to create this secret right?

Decker: Well the ephemeral key is generated by the sender who does not support this protocol. What you have control over is the short channel ID that I am supposed to forward over.

Fabrice: So basically this channel doesn't exist, and actually the idea of that channel is a secret that the vending machines used to generate a secret that Christian can find because he knows his private key.

Audience: You need a connection between the lightning node and the vending machine at some point?

Decker: No, only at setup, only at setup when we share parameters.

Audience: If it’s run out of hashes you need to get new access to the machine?

Decker: Oh yeah.

Decker: So that happens after 2^64 payment attempts

Audience: If it's limited on the destination then you have to store that many hashes?

Decker: So all he actually has to do is to remember the last index he used, and so we have constant memory for the machine itself. And we both have a primage generation mechanism that uses that index and some pre-shared index to start generating preimage and he will then go on to generate hashes from those primages, and my job is just to stop and create requests.

Fabrice: ...so what happens when your vending machine <inaudible> offline <inaudible>?

I know that for example we were contacted by a company in South Africa that is very interested in offline payments because they want, for them it's too complex to have the machines setup connected to the internet and they want to use the customers' internet connections, basically that's what it's doing.

Audience: Key … <inaudible> ... they have small devices for offline payments?

Fabrice: Yes.

Audience: <inaudible>

Fabrice: Do you remember, have you heard of them? I don't remember the name but, basically there's some kind of secure element in a tiny device you can put in vending machines and basically it can sign things but it's impossible to steal it. I don't remember the name of the company.

There's something that is very important to notice, when you forward payments the delay you have to <?> payments, has to be a bit smaller on this side than on this side. Can you see why? Suppose Bob forwards a payment to Carol and the payment times out, if the timeout on the left side is shorter than the timeout on the right side, Bob has a problem.

Audience: Because the hash will be cancelled and when Bob gets the preimage he has no-one to ask.

Fabrice: Yes, this is why the longer the route, the longer the CLTV delay you include in your HTLCs. Which means that for very long routes, you may need to wait a long time before your payment is actually timed out. Also something else to understand, suppose Carol never sends the preimage back to Bob, what happens on this channel? What do you think happens?

Audience: The money gets stuck?

Fabrice: Yes and what then? When it times out? Alice has sent a payment to Bob, Bob forwarded the payment to Carol and Carol never sends back anything. What is supposed to happen, the good case?

Audience: The first one times out and then the second one times out.

Fabrice: No, that's bad. That means that the channel is going to get closed between Alice and Bob because of a problem that happened between Bob and Carol.

Audience: Oh, right yeah. They should timeout at the same time.

Fabrice: No, what is supposed to happen is, OK this side is nothing to do with Bob, after a while he has to go to the chain and claim his outputs with, after a timeout. But on this side, Bob is supposed to fail the payment off-chain.

Decker: Once he gets back his funds, he has secured his funds back, he can then turn around and say "sorry, it didn't work".

Fabrice: So it's going to take a long time, but the channel is not supposed to get closed between Alice and Bob.

Audience: So long as Bob is also still co-operative.

Fabrice: Yes.

Audience: But this is when Carol stops being co-operative, Bob can't close with Alice until it's an on-chain close?

Audience: On-chain has a timeout expiry.

Decker: So Bob can only fail gracefully if the HTLC between Bob and Carol has been resolved by sweeping the timeout. So it's quite a common misunderstanding that people think that if an HTLC gets stuck, the entire path gets closed. But it's only until that point where you can be sure that this timeout has been swept in time for, basically, then gracefully failing backwards.

Audience: But how do they gracefully fail if no-one has the preimage right?

Decker: But I can always say "hey, I have no chance of ever getting this preimage, I'm OK with you retracting your promise to give me money." Because there's no point in holding on to a promise if I can't fulfil my...

Audience: But the promise is on that channel, like if somehow Bob then does get the preimage, he can take that transaction.

Decker: But it's Bob that basically says "hey I see that I have no chance of getting that preimage, I prefer having our channel active and please, you take the money back, I surrender, I can't get the preimage".

Fabrice: Bob will go on-chain with that transaction that includes an HTLC output, he'll wait until it times out, and then we fail the payment. So there's no way that the preimage can be used to get money from Bob at that point.

Audience: And Bob's timeout with Carol is shorter? Because how does Bob know that Carol has timed out, because he doesn't really know, I guess if it's not immediate, then it's...

Decker: The way Bob decides whether to fail or not is when he gets his money back, or once he gets his money back you can basically clean up..

Audience: I’m just thinking that Bob doesn't know if Carol hasn't responded because Carol's waiting for somebody.

Decker: The way that Carol would respond on-chain would be to create an HTLC success transaction that contains the preimage. That has not happened because I was able to claim using a timeout transaction.

Audience: So quicker than timing out, Carol would say it's failed or succeeded. And if there's no quick fail or succeed message, then you know that it's gotta be closed.

Decker: Then the channel will drop onto the blockchain because at some point this HTLC timeout will be getting closed, and I need time to actually react on it.

Fabrice: That's also a valid point because what makes lightning hard to implement if you want to implement absolutely everything is that, when you're monitoring the blockchain, you need to implement the case you described where the channel is closed between Bob and Carol because Carol is not sending back the preimage, but she publishes an HTLC success transaction on-chain, so you need to be able to understand what's going on, Bob needs to be able to understand what's going on and extract the preimage from the on-chain transaction and send it back to Alice, otherwise it's lost money.

Audience: And worse than that, you may have <?> and Carol may publish it's commitment transaction with an HTLC success transaction, or preimage transaction, and so Bob must be sure, or must wait, <be sure that Bob’s going to open before the timeout?>

Fabrice: No, suppose that Bob sees the preimage on-chain...

Audience: But in a failure Case, if Bob...

Fabrice: Yes, he must be sure he got his money back

Decker: Oh you mean the re-org case, in combination with the channel... that's nasty.

Fabrice: If you want to implement your own lightning node, all these corner cases are really hard to get right. It takes a lot of time...

Decker: Wait, this is not a problem with eltoo!

<laughter>

Decker: You will get so sick of me saying that the entire week.

Audience: So during this time when the channel between Bob and Carol is gone on-chain, while you're waiting for that, between Alice and Bob they're unable to close that channel.

Decker: They could close the channel unilaterally at any point in time, but they have chosen their timeouts high-enough so that, hopefully the Bob and Carol part will be settled and give them the necessary information to basically settle that HTLC gracefully.

Audience: So how does Bob feel confident of rewinding the HTLC back to Alice if he hasn't gotten the money yet from Carol?

Fabrice: He can't, he has to wait.

Decker: You hold on to it, so that's why we need to have a timeout difference that's large enough for you to settle here then turn around and actually act here.

Fabrice: The CLTV delay is shorter on this side than it is on this side.

Decker: So the left side settles after a day and the right side settles after two days, right. So once the first day gets to a close, we now start settling and timing out or having a success. And we still have the extra day to turn around and say "hey, we don't have to close, here's the information that you need.” I'm either happy to fail this HTLC and keep this channel open and running. Or I actually got the preimage from the off-chain transaction and turnaround and say "hey this was successful".

Audience: Ah Ok, so you can close it, but there's still going to be a delay?

Decker: Oh yes

Audience: You're still going to have to wait for that to complete, so that you can't cooperatively close it immediately?

Fabrice: If, suppose Bob closes the left hand side channel with Alice before this one has been closed, then you have the same problem of monitoring what's happening to the HTLC output. Can you get the preimage?

Audience:- So you have to wait

Audience: So the thing is, if Bob closes the channel with Carol on-chain, Bob probably does this because Carol is not responding or anything right, so in this way Bob has to timeout because Carol could still show up and on-chain enforce the preimage. So Bob has to wait for the timeout and then can turn to Alice and "let's cancel our HTLC because there's no preimage coming". Because you have already seen on-chain that it's not coming. He already claimed his funds back. On the other side, if Carol is quick and provides a preimage quickly, Bob can turn around and claim the funds from Alice off-chain, because he now knows the preimage.

Fabrice: So when it works well, lightning is almost instant <laughter>, but when it fails it's a bit ugly because you need to wait and basically a stuck payment in lightning is not something you can cancel and say "OK i'll try again". If you're trying to buy something on the internet with lightning, and if it doesn't work, you can't try to buy again because it's not safe; you may end up paying twice. Unless the shop is really… A lot of early lightning merchants were happy to settle any HTLC even if the same item had been sold before and the checks they made on links between their inventory and payment requests were very very limited, it's probably better now but...

- <inaudible>

Fabrice: If you do that, you may end up paying twice.

- If you requested the invoice...

Decker: The issue is that if you initiate a payment and then at some point this gets stuck, you aren't sure whether the payment went over that gap or whether it stopped before, and so you don't know whether the recipient actually received the money in the end, or whether it actually failed. So this uncertainty makes it really really hard to actually do anything with this, because it means that yeah, re-trial isn't safe because you might end up paying twice. And just hoping and praying that it eventually arrives will also not work because well, it might never. So stuck payments are a pain.

Audience: So before Bob and Carol timeout, basically the entire route, you can't do anything <with?> So the money gets stuck for the entire chain and also any path on that chain cannot be used for routing at all, right? You’re stuck in the state?

Fabrice: It depends how many pending HTLCs you have...

Decker: No you can add additional HTLCs and still use those channels. So for the HTLC you've just set aside a small portion of your channel and that will not get resolved until you resolve the HTLC, but with the remainder you can still perform updates.

Fabrice: OK so the money is stuck, but you can still use the route. Yes?

Audience: The channel is still operational. You can have about 480 HTLCs concurrently.

Audience: You can also pass the preimage out-of-band, you could create the preimage yourself, and accept the payment hash and then ask for the primage when you want it. So you create the preimage, as a sender, then you tell the receiver the payment hash, you send out the payment, they get it, they attach the HTLC, they get it.

Audience: You need to add an extra onion blob in the packet right?

Audience: No, the preimage isn't like

Audience: Yeah but you need to add it at some point in the packet.

Decker: You mean having a refund path?

Audience: No, just have the receiver, they don't know the preimage right, so they get an incoming HTLC and they're like OK, I have this payment hash, and they need that preimage now. Then they go and ask the sender, what's that preimage. The sender says OK, here's the preimage.

Audience: But you may also have the preimage in the onion package.

Decker: That's spontaneous payments. That's not a solution for stuck HTLCs.

Audience: Well, it's not a problem if... Stuck HTLCs are mainly a problem in terms of the danger of paying twice right. I don't know what the resolution of this payment is, but if you made the preimage, and you haven't released the preimage to anybody yet, then there's no way that it can complete.

Decker: What you can obviously do is just have a refund half, going back to the sender, but using the same payment hash. And then if the shop basically gets his money and then I can get this preimage and I can use this on the refund path. So we can atomically link the forward and the backward path. That's less of a problem but we suddenly are consuming twice as many funds on the lighting network. Which is awkward.

Audience: But your method of the sender generating the preimage and waiting for the onions to setup the route and then the receiver asking from the preimage, I mean this can also be gamed right?

Audience: If the receiver is not a good guy, then you have to go back to this normal case where it's like, OK, what's happening?

Audience: What it does is give opportunity to the sender, that the sender knows that he/she can abort the payment process, right, so the...

Audience: Well they can't abort it...

Audience: They initiate the payment process, and if there's never a request coming from the recipient for the preimage, they say well something is going wrong, I'll just try a different route, Fabrice: I'll just try something else. I can abort it. Because now if someone asks for it they say "I won't give it to you", but now all the HTLCs are stuck.

Audience: It's similar to a probe

Decker: We have ways...

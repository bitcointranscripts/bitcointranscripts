---
title: 'Receiving BOLT12 Payments in LND'
speakers:
  - Maurice
tags:
  - offers
  - lnd
  - onion-messages
  - blinded-paths
source_file: https://youtu.be/GMrpXKyfsWY?si=F8sUoT-HAEXUYB3N
media: https://youtu.be/GMrpXKyfsWY?si=F8sUoT-HAEXUYB3N
categories:
  - Lightning Network
  - Privacy Enhancements
date: '2026-01-21'
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
summary: >
  Maurice, an LNDK maintainer and Spiral grantee, makes the case for running
  LNDK alongside an LND node to unlock full BOLT 12 offer support. The talk
  opens with the motivation: BOLT 12 improves Lightning privacy and censorship
  resistance through onion messages and blinded paths, eliminating dependence
  on HTTP-based LNURL servers and hiding receiver identity. Because LND holds
  roughly 80% of the network's node share yet does not natively forward onion
  messages, the broader network's BOLT 12 adoption (measured at ~5.6% onion
  message support) is severely limited — LNDK bridges that gap. LNDK is a thin
  sidecar that intercepts LND's custom message API and delegates cryptographic
  heavy lifting to LDK's onion messenger. Key design decisions explained
  include: stateless offer management via HMAC-authenticated TLV fields
  embedded in blinded path hops (no persistent database), deterministic key
  derivation from LND's signing API so LNDK survives restarts without stored
  state, and a 100 ms queue-based relay with per-peer rate limiting for DoS
  protection. Maurice walks through both the pay-offer flow (decode offer →
  build invoice request → send via onion message → receive invoice → pay via
  LND SendPayment) and the receive-offer flow (create blinded path with HMAC
  authentication → handle incoming invoice request → translate BOLT 11 invoice
  to BOLT 12 → send back via onion message). A live demo shows LNDK paying an
  Eclair BOLT 12 offer and receiving a CLN-originated payment. The v0.3
  release delivers complete BOLT 12 payment flows; upcoming work includes
  async payments and BIP 353 DNS-based payment address support.
---

Speaker 0: 00:00:02

So, hi, I'm Maurice, I'm an LNDK maintainer.
I'm going to explain what it is now soon.
I'm a Spyro grantee and also part of the V4S team.
You can find me there on Twitter.
So today my talk is mostly trying to convince you if you run an LND node to try to run LNDK too.
So, it has like a workshop inside the presentation.
But if not, I'm going to explain how we do it.
It is not magical.
It is just doing the right stuff on the right time.
So a little agenda.
So why Bolt 12?
So what is going on in LLDK?
What's new on v0.3 that launched last month?
And a little demo.
So If you want to do some coding or if you want to give someone a good way to start trying it out before running it in production, you can go to that URL and just do it hands down if you want.
So why Bolt 12?
First I think it has a better UX for payments.
You could use reusable QRs, auto-withdrawals.
We can have a contact scenario, like any PayPal or Venmo app should do it, using Vault 12.
It also has protocol accessibility.
We could use recurring payments in the future, or we can add other stuff on the spec so it can be done using those, this.
And actually as Elias talked before, actually fixes the privacy and censorship problem that current has because of Onion messages, does not rely on HTTP servers like LNURL, that they can be censored, and also root blinding, let the receiver do not show herself when in a payment or when they are receiving Onion messages.
So the big thing here are blinded paths, what we're introducing in Bolt 12.
It looks mostly like this.
We have an introduction node that is in the beginning of the path.
We have blinded hubs for each node.
This is completely the blinded path.
And the receiving node is in the end and it could be like this be like the same node itself repeating itself and not being any forwards on that or this can be like different nodes that they are forwarding like only messages between them.
So this is the offer flow in general.
Bob does create this structure that is called offer that has one to end blinded path on it.
This will use a QR code to scan it.
It will regride to create this invoice request TLV with its own blinded path.
Send it through the on your message blinded path of Bob.
Then Bob will need to create this invoice message with his own set of blinded path, and that's for until the payment is made done through this blinded path.
So, Bolt12 kind of fixes the privacy censorship problem on this stage, because if we see like right this way, we need to build a different part of the system and everyone needs to support it so we could start using.
So first we need everyone to start building this kind of structures and they can be shared between each other.
We have to have messages forward to be supported broadly so we can hide between this node and network.
And also we have to have the forwards of HTLCs using BindedPath that is kind of the same but they are built different in each implementation.
So just paraphrasing what Matt said a few years ago, they were saying like privacy isn't that bad, just use Vault 12 and not LND.
I want to try to explain why he was saying about that.
If we see all these instructors that I was mentioning, All the three implementations kind of already implemented, except for these two, like LND also implemented, like forwards of HTLC, you can do it with Bolt 11 and LND.
And invoices in Bolt 12, they are kind of the same in Bolt 11?
Okay.
So LND already implements that.
So you can actually translate the Vault 11 invoice to the Vault 12, it's quite easy and straightforward.
So this one we already implemented for LND, so everyone in the network can use it, but this one you cannot do it, and only these implementations are doing it.
So that's what I say.
If we need to fix the privacy problem, we need to do the network fix.
And if we go to the ILEA's presentation, it's 5.6% of node supports on your messaging.
And mostly because LND market share is quite like over 80% or something.
I don't know the number, but it's kind of my suggestion about it.
So we need to do something about it.
So here comes LNDK.
What is this?
It is a little thin server that is like a side card that runs next to your LND server and mostly use LDK for every functionality of like heavy work.
So it's a shim because it intercept calls from the LND side, translate it, do something about it and then it's going to be used in the LLDK back and forth.
So LND is mostly like a messenger in this case.
LLDK does the heavy part of signatures and everything related.
I think it's like a little Frankenstein, but I think also it's quite clever how it's done.
Today, you can, if you run LND gain next to your LND node, that I will show how quick it is, you can have on your messages routing, like forwarding, you can pay both of payments, and now you can generate offers and receive payments through it.
What's next?
We already built the VIP353 payments and Merck can pay user flows that are coming in the next version.
Afterwards, we don't know yet what's going on about the project.
So with that, currently with the latest version, we can have all the instructors, all the TLVs, and we can do all the payment flows of Vault 12.
So that's a great win for the network itself.
So instead of just saying that words of math, maybe it's like use LNDK with your LND node and you can use Vault 12.
It's not like that hard of a statement.
So I'm going to explain now how it is done inside of LNDK, what are the things that we're doing, so we can maintain LNDK as stateless as possible and as simple as possible to be running next to your LND node.
First, We need to, on the spec of Vault 12, you have to do some signatures, not the offers, but all the invoice requests and the invoice needs to be like signed.
For that, one option was to have a set of key instructions inside of the LND gate, but we wanted to do it as stateless as possible and just run it.
So we did, we stole the idea from the BLEEPS, BLEEP50 actually, that they use this kind of message that is going to be signed in LND with a specific seed key found in a specific key index.
With that, we just hash it, the answer, and then we can have like this stateless state that is of a seed, so we don't have to store it.
We only ask for the node to sign something, and then use that as a seed to do all the signatures that is required on the offer flow.
So that I think is quite clever.
Now, before we were doing that, every time you restart an NDK, what is going ‑‑ that's what is happening currently in the strike, every time you restart, they generate new keys, those data cannot stay, they cannot know if the invoice request that they're coming is from an offer from their self.
But with this, we could actually restart the server with not state.
Then, I'm going to try to explain how we do the onion handling, onion messages.
We only use this Lightning RPC from LND.
We subscribe to peer events.
We subscribe to custom events type.
That's why we, on the LND side, they can handling handlers as the message the onion messages and we use the same custom message to send the onion message actually there are just sending operations whenever we see a subscription a peer event we were in queue the peer connect and the peer disconnect events into a general queue of events and we are going to feed the Onion Messenger in the LDK site that is going to view what is in our neighbor on the network.
And whenever we see a message from the LND, like it's a coming message, we're going to feed it also to the Onion Messenger, and it will handle the Onion message itself.
It's going to decrypt it, see what we need to do next, that it could be like either it's a message for us or we need to actually forward it.
So if we need to forward a message, the handle on a message, we're going to enqueue the new message to be sent.
And every 100 milliseconds, we are going to enqueue a send-up going for each peer.
So we're going to just process each message differently for each peer.
And we're going to use the same custom message in the LNC.
So it's mostly just LND trigger our queue, our queue triggers on your message, and then on your message trigger another queue, and we are just sending it back.
So it's pretty straightforward.
And hope it, yes.
So this is how we get invoice internals.
So we can say what we are doing on the LNDK site.
Whenever we receive a pay offer or get invoice in your PC request.
We just decode it, try to understand what is going on.
We're going to try to blind the path, blind the path.
For the invoice we just list the peers and we randomly select three of them.
When we have the peers we build the blinded path and then we build an invoice request that is mostly like the TLV that we're going to send.
We build the invoice request, LDK what this does, it takes our key that we already have it, like the seed, is going to sign it, build the Onion message, we are going to queue the Onion message and just send it through the network.
Then after 100 milliseconds or so, we are going to receive a message, like an Onion message to the LND, we are queuing it on the onion processing queue, LDK just process it, and we are done.
We will have the invoice to be paid.
Finally, when we have the invoice, we can pay it through using the ERPC, or we can pay the offer, it's going to be automatically.
We're going to decode the invoice, we're going to request the query routes in the LND side using the path that is provided in the invoice.
And we just do the sequence of paying both level invoice.
We're going to send the payment, we're going to extract payment v2 or something, and we wait for the result and the payment should be done using like the common way of doing it on LND.
So this is the same exact flow on the strike site.
I didn't like that much, but it actually shows the full paying offer.
We're going to, from pay offer, decoding, creating the request, sending the message, waiting for the invoice to come.
We have a timeout for that.
We subscribe, we track the invoice, and we just return when it's paid.
So I'm just going to do the same demo for you guys for now.
This is like the first thing that I just showed.
You can then ask me if you wanted to do it.
We're going to set up a ‑‑ This is what it's doing, it's building a network without using polar.
I'm spinning up LND, Eclair 1, Eclair 2, and CLN network.
It's going to create the channels automatically.
It's going to wait for the...
Also the peers are peers in the graph network.
Actually, there is, but it ended in a graph.
So we are waiting for that.
It shouldn't take that much.
So, afterwards I'm going to use this handy script.
Hopefully it doesn't take that much.
So we want all the nodes to have where are actually in the network, so it sometimes takes to just make the network sync.
So live demo.
Okay, well, okay.
So we have all the node info.
And already copied the secrets wherever I needed to.
I don't know if, yeah, I think it.
So if we run lncli list, oh.
List peers, LND should have like three peers, there's one, there's two, and there's three.
So we have three peers, if we list payments, We should have no payments on LND.
We just set up.
So I'm going to just run the LNDK server.
What we're doing, we start in the Rectus network for node that we fetch.
And we are just connecting to the subscriptions that I already told.
So we're waiting for that.
We're going to fetch an Eclair offer from the network.
And then we're going to get invoice so we are running the LNDK CLI command and it shows like the encrypted invoice.
We are not using the invoices in Vault 12 doesn't have a standard way of showing off.
We are just using the hex string.
And if we want to just pay the offer that is going to fetch the invoice and then we just pay it It's going to do exactly the same.
It's going to fetch, and then we're going to and successfully paid the offer.
And I can show you that I'm not lying.
We list the payments again, that is the latest one, it succeeded, and we actually paid an offer using all the schemes that I already showed.
So that's one thing.
You can try it out afterwards if you want it.
So then how can I receive payments using the same?
So how does it work?
First we need to solve the statelessness because LND does not store both 12 and LNDK doesn't have state.
So we need to store somehow and know when the offer is from us.
So one way of doing it, this is stolen from LDK side.
They were first doing, adding on the TLV metadata, where We were adding an ounce and we could calculate using the TLV records and HMAC also added an encrypted payment ID so we can query faster.
And using this, we could actually maintain the statelessness and not store in a database which one were our offers.
But this has some issues, because if we don't authenticate actually the blinded path, we could de‑anonymize the offer, like correlating two offers from one specific person or node forging like custom invoice requests.
So in order to solve that, what we started doing is actually doing kind of the same, storing unknowns and also an HMAC, calculating an HMAC and put it inside the blinded path hub receive and the blinded on the blinded hub that is receiving that is actually us, we are adding a new TLV that we can recalculate it.
So we kind of for each blinded path that we created, we have a way of authenticating that the user used that blinded path specifically that we built, and we only know that we built.
So in that way, we maintain the statelessness, and we don't have to store anything in other database.
So, knowing that, what we do for create an offer is quite straightforward.
We receive a URPC, we start building our blinded path, for that we list our channels, because we want to have like ‑‑ well, channels are the most conservative way of connecting to peers, so we use that because offers can be like long, they can last longer.
So we use that, we build the blinded path, then we build the offer itself, we don't need even to sign it, we build the offer and we return the offer.
And whenever we receive an invoice request through the Onion message, what we do is when queue the Onion processing, the onion processor will know that we are receiving this, they are asking for an invoice, we should authenticate the invoice request with the trick that I already told you, we then create an invoice for the invoice request, we use, actually we create a vault 12, vault 11 invoice using a blinded path options in LND, then using that we parse the Vault 11 and just transform it in what is a Vault 12.
Then we enqueue the invoice to the onion processing handler, and we then send the outgoing message.
And finally, the payment arrives like any other payment like Vault 11 payment that LND was waiting for.
So just to show off that I'm not lying I'm going to just run the script, create an offer.
And what it did was ask for the channels, then create, and it's quite big compared to the Eclair because the Eclair one wasn't adding that many binded paths, we tried to build like three unique binded paths for this route.
So then we can use the CLN for example.
And...
For a CLM they are doing it differently, you have to request the invoice and then pay it, So I'm going to do that.
And there you go.
Payment is complete, destination, the payment hash and how many parts.
So we can just do list invoice.
And we could see the same invoices as the Vault 11.
We have one settled here.
So we are receiving, actually, the Vault 12 payment through that.
So cool.
And you can see that down there.
And wrapping up, so Vault 12 is important for Lightning Privacy, Sensory Street Precision and also better UX.
And NDK is important in the ecosystem so we can accomplish that.
You can run it now.
You can start receiving payments now.
Even if you are not using wall2f payments now, you can help the network just running it.
And Actually you have my local development, because I just pin up networks like this and you can hack around LNDK stressless without using money.
So thanks, you can ping me on Twitter.
Questions?

Speaker 1: 00:20:59

Any questions?

Speaker 2: 00:21:05

Thank you for explaining how LNDK works.
I have two questions.
One is, will you keep maintaining LNDK after Bolt 12 is merged in LND?
What does the future look like?

Speaker 0: 00:21:18

Yeah, it's actually we don't know yet.
For the first part we will keep maintaining but we are thinking to add also other features that are not in L&D for example async payments is a thing that we are currently looking at and we probably continue on that path for the next year or so.

Speaker 2: 00:21:40

Okay, so my second question is do you in any way mitigate the DOS vector of like if somebody's doing a lot of on-emessaging, do you have some way to protect your node against too much traffic?
Yes.

Speaker 0: 00:21:54

Yes, so, that one was one of the main issues in the beginning for strike, the strike is running this, so we added a rate limit, rate limiter inside the LNDK, so we are trying to, if we have so many message from one, from one, from one peer, or two one peer, we're actually rate limiting inside of the queue, and the queue also has a specific fixed size of it, so we haven't had that many issues related to the OS attacks.
Cool.
Here was one question.

Speaker 1: 00:22:43

Yeah, thanks for the presentation.
Is there a reason why LND is not interested in this?
Is my first question, the second one, are you considering doing splicing or anything like that, that L&D doesn't have as well?
No, that's a big one.

Speaker 0: 00:22:56

Yeah, I think I cannot talk from L&D, but they are working on it.
I saw some PRs of Onion Messages.
I thought they were going to be launched on 0.20, like this is the current version.
I think it didn't land.
Hopefully it's in the next three months.
I would like to see this implemented natively in LND.
This is our hack around or my hack around to just make it happen.
And in the splicing side, I think it's harder to implement it like this kind of outside because you have to do like, I don't know the specifics of splicing, but you probably need to do something related to the scripts and all that is pretty embedded in LND.
It's not that practical to have it outside.
Cool.
Some questions No?
Okay, thank you you you you you

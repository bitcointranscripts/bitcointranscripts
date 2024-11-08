---
title: Rendezvous Routing
transcript_by: Caralie Chrisco and Darius Parvin
tags:
  - lightning
  - routing
date: 2019-06-28
speakers:
  - Christian Decker
media: https://youtu.be/Ms2WwRzBdkM
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-28-christian-decker-rendezvous-routing/
---
Rendezvous Routing (Lightning Network)

Location: Chaincode Residency 2019

Slides: <https://residency.chaincode.com/presentations/lightning/Rendezvous_Routing.pdf>

Transcript by: Caralie Chrisco and Davius Parvin

## Introduction

Okay, the second part is rendezvous routing. I basically already gave away the trick but I hope you all forgot. So what is rendezvous routing? Anybody have a good explanation of what we are trying to do here? So we have someplace where we meet in the middle, and I don't have to know where you live, you don't have to know where I live, we're all really private. It also has another feature; what happens if I want to buy from this guy and I don't know how to get there because this guy is basically in a hidden part of the network that is all private, and I don't know how to access that part of the network? What we can do is, basically this guy selects some meeting point that is somewhere between the two of us and he then generates an onion that would lead from the meeting point back to himself. So he is basically creating an onion on behalf of the meeting point; this is the sender, and this is how you get to me. He sends this onion back to the original sender. The original sender then creates his own onion (in this case I made it blue). The blue onion basically goes from this guy to the meeting point, and we then take these two onions and combine them into one single onion such that we can then send through the meeting point over to the recipient. So we have two features that we're trying to do; basically one is we want to hide the identity of the recipient, and the other one is we want to give the sender, he's not that good at finding paths, we want to give him a hint on how he could reach us.

## How do we combine two onions?

We already talked about this, but how do we actually combine onions, right? This is how we serialize the onions; the important part is the payloads here that are a one thousand three hundred bytes, and we want to combine that with something else that is also one thousand three hundred bytes, and as we saw on Wednesday this is all HMAC’d. How can we put something that is this big (1300 bytes), in here, plus some signaling bytes? Clearly, putting the onion inside of the onion in this case doesn't really work, right? So, what should we do then? So basically taking this (onion) and then prepending stuff and rewrapping doesn't really work because of the way we modify the ephemeral key along the path. In this case (rendezvous routing), for this part of the journey the recipient generates an ephemeral key as if he were sitting here (at the meeting point), and then starts tweaking that on every hop to generate secret secrets right? Then this guy (sender) needs to generate an ephemeral  key and tweak it along the way such that the ephemeral keys meet up in the middle, so that the terminal keys are identical. So, that's not really possible; that would be a scalar point division. It's kind of hard, that's sort of the whole point of ECDSA and Schorr, that that operation is hard.

So, can anybody see the trick here? Less hops, that might be possible, but then you're giving away that you just used a rendezvous route, and the other guys in the network would actually have to understand the protocol for shorter paths. This (rendezvous routing) is actually possible without people along the way having to do anything at all. Anybody? Alright, Rene - give it away.

Rene: So one thing that I would do, I think he was proposing, is when the recipient creates the route, there’s a lot of filler at the end, and this junk can now be the first part of the second onion. So you put this entire onion together.

Christian: So you would put the second part of the journey onion inside of the first one?

Rene: No, just the hops payload; that stuff I need there.

Christain: So what you're proposing is basically wrapping the onion some more?

Rene: Well I need some more stuff, but there is something that we should do, because you give me an onion for the rendezvous point; it might have five hops, it might have ten hops, I don't know; but I definitely know I need three hops to come to the rendezvous point. So I take the seventeen hops that are there, and I put the first seventeen hops of your onion in there, that is one thing I need to do. But, there is the problem with the ephemeral keys, so I need to do an ephemeral key switch. So I somehow need to put this into the data.

## Solution to Ephemeral Key problem

Christian: So, that's exactly the trick; this is the [write-up](https://github.com/lightningnetwork/lightning-rfc/wiki/Rendez-vous-mechanism-on-top-of-Sphinx).

So the idea is basically that, if you remember the construction of the onion, we were basically taking an onion and wrapping it going backwards from the recipient to the sender. This looks very similar, but instead of going from the recipient to the sender, we are being given an intermediate set and we just continue wrapping our part of the journey backwards. The only issue that we really have is that the ephemeral keys don't line up.

Rene: So you use a different realm in the payload, to transport the ephemeral key?

Christian: So we do it a bit differently now that we have TLVs; we basically just have that. So the actual solution is, in the payload for the rendezvous point, the point where these two onions meet up, we just say, “Hey, instead of generating the ephemeral keys like we used to, just use this.” The ephemeral key that we switch is basically just the ephemeral key that we got from the recipient. So we have this this 33 byte ephemeral key that is hidden inside of the payload for the rendezvous point, and the rendezvous point is basically just being told, “Hey I know you just generated an ephemeral key for the next one; don't use that, use this.” That way we can actually solve this quite nicely, and have basically all of the same mechanics that we use so far, but we have this really simple if statement that basically says, “Okay, if there is an ephemeral key switch in there, just switch out the ephemeral key and everything lines up again.” That's basically the whole solution; easy isn't it? So, very last time for me. Thank you so much for having me, it's been a real blast. [Applause]


---
title: Onion Routing Deep Dive
transcript_by: Arik Sosman
tags:
  - lightning
  - routing
speakers:
  - Christian Decker
date: 2019-06-25
media: https://youtu.be/D4kX0gR-H0Y
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-christian-decker-onion-routing-deep-dive/
---
Location: Chaincode Residency – Summer 2019

## Intro

We've not seen exactly why we are using an onion, or why we chose this construction of an onion and how this
construction of an onion actually looks like. So my goal right now is to basically walk you through the iterations that
onion routing packets have done so far, and why we chose this construction we have here.

So, just to be funny, I have once again the difference between distance vector routing, which is IP-based routing,
basically, where we just have the recipient’s address, and source-based routing, where we have a list of intermediates, in
which we can then finally reach our destination. And we've been talking about this before during the trampoline talk,
about why we chose source-based routing in the first place, and what the disadvantages and advantages of each other are.

Obviously, here we have this list of hops that we'd like to go through. And for a remainder of the talk I will basically
represent this as a list of individual hops that will be attached to our HTLCs and will be forwarded. So this is
basically the onion as it looks for user A, and user A receives this list of addresses, or list of hops, and A sees
that, "okay the next hop is B." So B comes along and sees, “oh, the next hop is C.” C comes along sees, “okay, D is the next
one,” and once E gets it, this is a terminal node, no need to forward it anymore.

This is all cleartext currently, and I guess everybody sees the downsides of this, namely that we know almost the sender
(we know the first peer of the sender) and any node in the list definitely sees who the recipient is. So we can do one
better: basically, instead of having this fixed list of addresses, we now go and just chop off the beginning every time
we process it, and that turns out to be: A sees this thing, “okay, I am supposed to send to B,” and we chop off B, now
send it to B, B sees, “oh, the next one is C, I'll chop off C and send it forward to C,” C sees D, and so on and so
forth.

So the point here is basically that we now have, while we are routing, each node sort of elaborates or processes this
addressing packet, and the packet that is going to be forwarded to the next hop doesn't look like, or has less information,
than the one we had before. And of course then E gets it and E sees “oh, I'm the intended recipient, and I shouldn't
forward it anymore.” Now this still has this downside of well, B still sees the exact route and the amounts and who the
destination is but at least he doesn't see who the sender is anymore, or any hop doesn't see who the later one is, but I
will get to that later. So, of course, this all being cleartext is kind of dumb, so let's maybe start encrypting stuff?

## Encryption Scheme

So I have chosen this wonderful black color to represent encryption, and so what we have again is that I, as A, receive
this blob of information, and I will process it somehow, and from processing this I will receive the blob that I should
forward to the next node. So that stays the same, but now, processing actually involves me having to decrypt this blob.
So I get this encrypted blob of information, I do some magic ECDH, basically we'll see how that is
transferred actually later, and I generate a secret, and I peel one layer off of this onion; basically I decrypt the
entirety of this thing.

And now I see that I'm supposed to forward it to B. Notice that the color got a bit lighter because I peeled one layer
off the entire thing. Anybody want to guess why I'm not just decrypting this part, but I'm decrypting the entirety of
this? Right, but I could also, if all I care about is my part and want to send it forward, I could just have encrypted
this part and have left the remainder singly encrypted.

[Audience member]: _“Then if C, for example, which we don't see yet, intercepts it before you could decrypt it before B,
like everything should be encrypted with B's key and then B should decrypt all of it, and only then should C be able to
decrypt, otherwise the last person can know from the start where it got from. If he can decrypt the package of the
original hop…”_

C can only decrypt its own hop, that's not the real reason. The reason is…

[Audience member]: _&lt;inaudible&gt;_

I mean, I could decrypt the first two bytes and that tells me how many bytes you decrypt, that’s also not the
exact reason.

[Audience member]: _“To keep the size of the final image?”_

We'll get to that later but the real reason–

[Audience member]: _“Hampering?”_

“Hampering?” Sort of; the real reason is that if I were just to decrypt this part and keep the tail constant,
a passive observer could associate the previous onion with a follow-up onion. So by actually decrypting the entirety of
this thing, this part looks also completely different from what I got on the inside, so I can't really associate the
two. There's other tricks we can associate them a bit, but the idea is basically to have the incoming onion and the
processed onion as detached and looking as different as possible on every single hop.

So, the process is again the same: A gets this packet, has just decrypted it, can now read B (or it can read the
information it's supposed to read and supposed to act on; basically: forward to B). Now it chops off its part and it
forwards to B. B again decrypts the entirety of the packet, chops off, forwards, and we basically have the same thing
again. And E and T and notice that at no point the color of the onion was the same as it was incoming, right? So at any
hop in this process we change the entire look of the packet; you can't really associate them anymore.

So somebody mentioned it already: we still have a pretty good idea on how many hops there are here, right? It's three,
because every time we chop off the the initial part, we know the we are probably getting close, and, in particular, D
knows that E is the final destination because there's just one more hop, which is basically there to signal, “hey, you
are the destination,” so we are still leaking information. And of course the solution to that is to make a constant
onion. Any ideas on how we want to create a constant onion?

[Audience member]: _“Add random data in the end?”_

Is random really good?

[Audience member]: _"It’s padded with zeros after the termination. So E gets its information and then everything else you
can throw away."_

When do you add it, before or after decrypting? Okay, so then, by decrypting it, by using the decryption
stream, you encrypt the zero pad at the end, right? And indeed what we do is, we get this fully encrypted blob of
information; A gets this and we now start processing, and we do that by appending a zero pad at the end, which is
equivalent or bigger than the part that we are going to process on our side, right?

And we then decrypt it and the way we decrypt it is basically an XOR between a pseudo-random stream of data that is
starting here and goes beyond the end of the original package, which was here; and by decrypting it at this packet, the
head of the packet we also encrypt the trailer that we just added, the pad.

No, it's actually this black that we stripped, and so we add that black here.

[Audience member]: _&lt;inaudible&gt;_

Sort off yes, yeah no. I thought about it, and I wanted to make it clear that the decryption and encryption
is basically the same operation, that's why I chose the same color. And once we have that, we can actually chop off the
head, and this is the new packet that we can forward to the next hop in our route. And if you were to shift this to the
left we would actually have the same identical size again of the initial packet. And this way we can ensure that at
least from simply by looking at the packet, you cannot infer what position in the route you are, and how close you are
to the destination.

That also means that we have to have a global parameter that tells us how many hops to pad to. In this case we have four
hops and we're limited to four hops because we could distinguish five-hop-onions from a four-hop-onion, and simply
having this information about how far apart the source and the destination are would give away quite a lot of
information. What we do in Lightning is, we have twenty hops in total. Each hop has 65 bytes, and so, when we create an
onion, we may fill the first three, four, up to eight (currently) hops, and then we just pad with all zeros, and
whenever we decrypt, we actually generate a stream that is 1365 bytes, basically because we append one additional hop at
the end, which is going to be shifted in with the rest of the pattern.

## HMACs

[Audience member]: _“What happens if one of the hops &lt;inaudible&gt; rigged? Does it &lt;inaudible&gt;”_

That's an excellent question. It also ties in perfectly with the next question I had. So what happens if A,
basically, goes here and fiddles a few bits here? So we need some mechanism of detecting tampering, right, and how do we
usually protect against tampering? HMACs, exactly!

So what we need to do here is introduce a MAC that ensures integrity of the onion packet itself before decrypting the
onion packet, right? So which range of this packet—let's see let's go here—which range of this package should we HMAC?
Should we just MAC this part that we are about to decrypt, or should we HMAC the entirety of the packet? The whole
thing, exactly. Because if A was to tamper with something back here, A could basically probe for who is the final
destination. Because remember, we have trailing padding in here that is basically just zeros that we only have there
because we want to have this constant size, and so if we tamper with something beyond the last hop and we were only to
MAC the individual packets, then this would still work, and we could basically probe out which of these sets we need to
tamper, and then figure out which node is the final node in the graph.

Our HMACs always cover the entirety of the packet. And we'll see this later, when I talk about how we serialize the
onion, but what we do is, basically, when A decrypts this, this does not only contain the address of B, but also the
HMAC, and some additional information that we should give to B—in cleartext, by the way. So when B then gets the HMAC
and this onion, it knows it can verify the integrity of the package it just received before decrypting it. And if the
HMAC does not verify, then we will just say, “hey, away, it just failed. Tear it down, the entire route, we can't go
on.”

[Audience member]: _“I'm sorry I keep asking the same thing, but what exactly do you do? What do you mean, ‘go away?’ What
happens, what does the product exactly do when it fails to decrypt?”_

So what we do then is, we don't fail decrypting, but we fail verifying integrity. It's the same. So the
protocol is, we send an Update HTLC, the Update HTLC contains both the HTLC information, as well as the onion. This
onion gets stashed away. The HTLC gets added to our commitment transaction, and once we have exchanged the commitment
signatures, only then we go back and look at the onion, right? We have now committed to an HTLC that is incoming for
which we have an onion. We go look at the onion, try to decrypt it, maybe fail; if we fail, we say “A, Update Fail HTLC”
and we give it an error code that indicates that the onion failed.

[Audience member]: _“We don’t say what exactly failed, right?”_

We don't say what failed, because all we can say is just that it doesn't match the HMAC I was expecting.

[Audience member]: _“It’s best not even to say that, that’s what I’m trying to understand. Should even say if it was just
HMAC or failed decryption.”_

Well, there isn’t a difference between the two.

[Audience member]: _“The HMAC can succeed and you can fail to decrypt it?”_

So what can happen is that we failed to parse the payload, that's true. We currently distinguish those
because we find it easier to debug with more information, but you are right, we should eventually just say, “go away”
without further details.

[Audience member]: _“Cause then you can use a timing attack to try and time the HMAC.”_

Yes, well, timing in this kind of network is kind of hard because we need to be committed first, so we have a
whole prep it's not just “I receive an onion and I decrypt it,” but it's “I receive an onion, stash it away, and then
look at it later, once we have exchange commitment signatures.” So we add a lot of noise, but I do agree, there is some
signal left.

And this brings us to Sphinx, the construction we actually use, and what we have here is the filler construction, which
is really the only hard part in all of this, because it's weird how we use sub-parts of the stream to encrypt parts of
the onion that are trailers. And I'm not sure you can see that, but I have, sort of, a shadowed out version of the clear
text payloads here, and what we do is, basically, the sender, initially, when he wants to create this structure here, it
will basically take this onion prefix here, it will have the filler or trailer or whatever you want to call it, and it
will then go and generate the shared secret that will be used to decrypt it, and it will encrypt this whole thing, throw
away that part, and only keep this, okay? So it will encrypt this part.

Now for the next hop, what we need to do is basically, we need to take this part, shift it here, and add the filler that
the second node would add, and now we again generate the entire encryption stream, and encrypt this part here, and throw
away the beginning. So we have one more layer of encryption.

[Audience member]: _“Why exactly do we need to cover the filler with the HMAC? I don’t see why it would matter if someone
is tampering with the filler.”_

If you were not to cover the filler with the HMAC, then you would have to communicate to your peer, which
parts are covered by the HMACs. If you only were to cover this part by the HMAC, then you would need to tell A, who is
going to receive this packet, “hey, you are supposed to only check the first four of these,” right? It's not actually
only easier, but you're actually telling A that this route is only four hops long. And here you say, “B, hey, this route
is only three hops longer;” this guy, “hey, it's only two hops long;” and this guy—well, this guy knows he's the final.

[Audience member]: _“The general advice is to never encrypt anything without MACing, it’s always a bad idea. Cause then you
can manipulate tons of different stuff.”_

And the reason why we HMAC not only the payload destined for the processing node is exactly that: because
then, if A receives this packet here, and only checks the HMAC here, then somebody before him could basically tamper
with the C, and if then that HMAC fails, we know, okay, it's at least going to be B and C. So by tampering with
individual parts of this onion, you could basically start probing, “hey, how long is this onion?” And you'd lose all of
the security gain that you just bought really expensively.

So this whole filler construction is really the only hard part in this whole process, and it took me forever, with paper
and stuff, to actually draw this out. So now, we go ahead, shift that again; this is how the packet would be looking at
the node C. We add the final filler, encrypt again the entirety, and then finally we get this last step, and we encrypt,
and then we can start computing HMACs for all of these.

And we compute them in reverse order, because this HMAC is going to be in the payload for E. This HMAC is going to be in
a payload for D, and this HMAC is going to be in the payload for A. And there's one more D. It gets really confusing
because you have to reverse order a bunch of times.

## Ephemeral Keys

Okay, so the actual packet serialization we use in the Update HLC format is, we have a single version byte (which we
recently found out we can never change… sort of dumb); we have an ephemeral key.

[Audience member]: _&lt;inaudible&gt;_

Because if we change that, basically the entirety of the entire network needs to switch that. It’s not about
the anonymity set, but if I give you a version 1 onion, you decrypt it, and you process it, we have not built a
mechanism that we can tell you, “hey, by the way, forward this as a version 2 to the next hop.” We can downgrade from
version 2 to 1 by saying, “by the way, in the payload, the next hop doesn't understand version 2, please downgrade,” but
we cannot upgrade, which is kind of the whole point of this.

I mentioned before that we are performing ECDH to actually get a shared secret, and the ephemeral key here is the one
that we are actually using to perform ECDH with the node’s private key. And this ephemeral key is, basically,
public-key-matching some private key that we randomly generated as senders.

Ephemeral key for shared secret generation of payloads, that's basically the 1300 byte blob that we were just
constructing, and the HMAC that is needed to verify before decrypting the whole payload. All good so far? Cool.

And now for the piece de resistance. This is the actual process of unwrapping and wrapping the onion. I'll start with
the unwrapping because that's easier. So upon receiving a packet, we will use the ephemeral key and our own private key
matching our node ID to generate a shared secret. Using that shared secret we can compute an HMAC on the encrypted blob,
and compare it with the HMAC that we were given in cleartext by the previous hop.

Then we can append the filler, that is, basically, the zero padding at the end, we decrypt using the shared secret, and
we use a Chacha20 stream for that. We extract the hop payload. The hop payload is basically just, once we have
decrypted, the first 65 bytes contain the HMAC for the next hop, contain who is actually going to be the next hop, the
CLTV delta, and the amount that we'd like to have the processing node forward.

Remember, this is the sender talking to one of the intermediate hops, right? So the sender tells the intermediate hop,
“ey, you should forward to this hop with the CLTV delta, and that amount should then get transferred to you,” and then
we just take all of this information and serialize it again. So we take the version byte, we take the ephemeral key—the
ephemeral key which, by now, has been tweaked using the shared secret (I'm actually missing that part in the slide).

The ephemeral key gets modified by multiplying with the shared secret. This makes sure that also the ephemeral key
changes from hop to hop. So you can't look at two onions and say, “okay, this is a precursor to this one” or “this has
anything to do with the other one” because the entire packet basically changes.

You serialize that and basically propose an Update Add HTLC to the next hop or we have some error because, well, we
don't have a channel, [the one] we were supposed to use wasn't active, or something like that. So that's the unwrapping
of the onion. This is pretty straightforward because it just goes one direction. Wrapping the onion is a bit more
involved because it goes backwards, and then forwards again.

So we generate random ephemeral key and using that, we compute the shared secret in forwards order, so that way, we
basically compute the first shared secret with the first node ID, and then use that shared secret to then tweak the
ephemeral key for the next hop, and using that we then generate with a node ID, and the ephemeral key we generate the
shared secret, and then tweak it again—basically, this is a full work process.

Then we serialize the last hop payload, and since we don't have a next hop, the HMAC is going to be all zeros. And then
in reverse order of the onion, because we are wrapping the onion, we right-pad to 1365 zero bytes (this is to get the
constant size). We derive the Chacha20 stream from the shared secret (this is what we are going to use to encrypt). By
the way, this encryption scheme and decryption scheme is XOR, so they are symmetric, which makes this whole thing a lot
easier. We encrypt the onion, we compute the HMAC, put the HMAC inside of the payload, and serialize the payload inside,
and we right-shift this whole thing once, making room for the previous payload (which is the one we are currently
processing), we serialize the payload inside of this 65 bytes of thing, and then we rinse and repeat. Well right-padding
is not really needed, we basically chop off the end to make it to the size that we expect it to be. Derive Chacha, and
decrypt, and compute HMAC, add HMAC to the prior hopm and so on and so forth. And we do that 20 times, or however many
hops we have in here, and finally, we then serialize the onion and can use it when using Update HTLC.

The whole complexity here is that we generate shared secrets forwards and wrap the onion backwards. That's basically it.
This is all done by the center, yes. This is also why I'm saying that actually computing a route and d creating an onion
packet is quite expensive. Also, implementing this is hell. It's funny as actually that’s the first code that I touched
on CLightning, and I was learning C and this stuff at the same time. I think I still haven't recovered.

Anyway, so all that's left is basically, add a few more details about what encryption we use, and what HMAC, and what
shared secret. So we use ChaCha 20 for the encryption stream, the stream is initialized using a shared secret that we
derived from ECDH, and from that ECDH process we derived three keys: the rho key is the encryption key, the mu key is
the HMAC key, and the um key is what we use for the error on the backwards route, which is a joke I came up with because
it's backwards mu. You've got to have fun sometimes.

HMAC is sha256 because that's all bitcoin knows. All bitcoiners know. Okay, two more slides and we're done.

## Returning an error

So this whole process is going forwards, right? This is a one-shot routing packet that we can only
ever go forward and the question is, if something goes wrong, how do we return an error, how do we tell the sender,
“hey, something is wrong here?” And we don't have a good construction of how to create a backwards onion of using just
Sphinx, because we heavily modified Sphinx to not include a payload anymore for the final hop. So what we ended up doing
is, we rely on pre-existing information, right? This onion does not exist in a vacuum. This onion is associated with an
HTLC, we can store the shared secret with an HTLC and so whenever we fail an HTLC, the previous hop can actually look at
the shared secret, look at the um key, and use that to encrypt whatever error we had. So that way, we can rewrap an
onion that contains an error.

Now this onion is a bit simpler, it's a lot simpler, actually, because there is no HMAC; we don't have a good way for
any intermediate node that doesn't have any information about the path to create HMACs that could be verified by
individual hops, it's also not constant size, because hopefully this happens not that often, but it will not change
during the during the forwarding of the error. So if I have a 60-byte error message that I'm trying to get back to the
sender, it will be 60 bytes all along. It will it will just be encrypted using the um key at every hop, and when
receiving the error packet, the sender can actually regenerate all of the shared secret, or it has stored them
somewhere, and can then decrypt until it finds a valid error message, at which point it knows, okay, which node failed
that is returning this error.

So yeah, this return onion is really simplistic on purpose, because we hope to eventually find something that is more
stable, but still breaking.

## Recent developments

So far I've told you about how this is actually implemented right now. I have, like, three pending
PsS on the specification that all try to get us away from this fixed 65-byte-frame. 65 bytes, by the way, was chosen
because it's 64, which is a nice number every every CS guy likes, plus 1 byte, which is sort of that payload type (
realm, as we call it). So totally arbitrary. It was just the smallest power of two that would fit our payload.

And the initial proposal was basically to allow having multiple hops be one payload, so basically, say, okay we can
decrypt the first byte or 2 bytes would tell us how many frames to use, and that would be our payload. And then we would
also shift accordingly. So if we were to use two frames, each 65 bytes, then our filler at the end would need to be 130
bytes, and we would also need to encrypt that many more bytes. That worked, but it was still not flexible enough, so we
came up with a different scheme where we basically, instead of having these fixed size frames, which we were using to
enforce the 20-hop-limit, are now completely gone, and the first 2 bytes basically tell us how many bytes our payload
is, and that gives us the the opportunity to actually pack our our payloads much closer, and to basically aggregate what
we were using as padding inside of the payload, and add additional hops at the end. Or basically add an arbitrary
payload for any of the intermediate hops inside there, and if you were wondering, that's also how we could fit an onion
inside of an onion, by basically having a 19-hop-onion inside of a 20-hop-onion. There's enough room for us to basically
have this large piece of data inside of a slightly larger piece of data.

And once we have that, we can do a lot of fun stuff. So one of the proposals that we were talking about before is having
the AMP proposal, which requires us to put a bit more information there, basically, “hey, you are about to receive sixty
satoshis. I know this is short ten satoshis, please just wait.” By adding that information in there, we can tell the
recipient, “hey, you should be waiting for more.”

We can have stuff like spontaneous payments, which we just figured out lately, that we don't actually need to put in the
onion, so yay!

And we can have stuff like rendezvous routing. So rendezvous routing, basically, is that the recipient tells us a part
of the onion, and the sender basically prepends its own path to whoever the rendezvous or the meeting point in the
middle was. I can say, “I'm the recipient, I want you to communicate through Richard,” and “James, I will give you an
onion that relieves from Richard to me.” And you will not be able to see that I am the final destination; all you will
see that you’re supposed to communicate through Richard, and so you will take that second half of the onion and prepend
your path to Richard, and then we can communicate in this way without either of us knowing who the endpoints are. Well,
we need out-of-band communication for that.

And the reason why we need that, why we need bigger hop payloads for that, is because of the ephemeral key. We have no
way of generating an ephemeral key such that they meet up perfectly at Richard, so what we need to do is have an
ephemeral key inside of the onion and then basically, when Richard gets your onion, he will be instructed to switch out
the ephemeral key with the one that was transported in the onion itself, and then this all works. But otherwise it's
kind of hard. I mean, it's actually cryptographically proven that you can't really meet up in the middle, otherwise
you'd have broken some cryptographic assumption.

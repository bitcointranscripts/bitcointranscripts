---
title: "Lightning on Taproot"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=E_z4hjvVzoQ
tags: ['lightning', 'taproot']
speakers: []
categories: ['conference']
date: 2023-07-18
---
My name is Arik.
I work at Spiral.
And most recently I've been working on adding support for taproot channels.
At least I try to work on that, but I'm getting pulled back into Swift bindings.
And this presentation is supposed to be about why the taproot spec is laid out the way it is.
What are some of the motivations, the constraints, limitations that are driving the design.
And I wanna really dig deep into the math that some of the vulnerabilities that we're trying to avoid as well as how we're solving those issues.
So first of all, obviously we know that Haproot has not been active for a while, but why are we actually bothering with modifying the way that lightning channels are opened such that we can have lightning channels operate on half-route.
I guess I should have asked this question before showing this slide, but let me just go back and see if the audience has any suggestions they want to know here.
Is there privacy?
Great.
Yeah, so the biggest reason, of course, is that we have privacy improvements.
At least, you know, assuming that eventually everybody is going to be using hatred haproot addresses.
As you know, haproot is segwit v1.
Segwit was segwit v0, that was our new software mechanism.
If at some point we decide that we need segwit v2, then all of the old lightening haproot channels that aren't human support yet, that are going to be using SegWit v1, are going to lose their privacy status and they're going to once again start sticking out like a sore thumb.
So that is one of the benefits.
We are also able to improve privacy by decorrelating payments.
That is PTLCs. And that is a privacy benefit that is actually going to persist even if we have a SegWit V2 or V3, because there the primary issue that we have with HDLCs right now is that if we were to have multiple channels that have the same inflight HDLC go on-chain, then that hash would be correlatable and we would be able to link the payment chain, you know, link one channel to the other.
There are hopefully also some security improvements such as directional signatures, but it's still very much a research phase.
So you know, mostly I think the greatest benefit really is privacy.
There is also something to be said about the fact that with the way that Taproot works and the way that Lightning requires a bunch of different spend paths, with Taproot Taptrees we are able to make a bunch of those pen paths much cheaper, and we are also able to not reveal the ones that are being unused.
So it's also a bit of a cost reduction there, which will save us some fees.
But first of all, why do we have better privacy?
The primary reason that we have better privacy is because right now, Lightning channels on chain have a signature of a 2 of 2 multisig.
The big improvement, or one of the two big improvements that Taproot brings is Schnorr signatures.
And the cool thing about Schnorr signatures is that they allow us to have quite trivial n of n signatures that still look like they're single SIG.
So nobody monitoring the chain would know that channel open is actually a channel open because it would be theoretically indistinguishable from just regular transaction to a single key.
And I hope that you all remember how Schnorr signatures look.
You know, we see we have this big entity called S, and we have a public key point called R.
We commit to our pub key, so here in this slide the example is Alice, So her public key is uppercase A, her private key is lowercase a.
And Alice's signature is a commitment to the nonce that she used, her public key, and the message.
In order to make sure that the signature doesn't tweak her private key, we tweak the hash of her commitment with the message multiplied with her private key by a little random value called r.
And we tweak that because if we weren't to tweak that, then somebody would trivially be able to apply the modular multiplicative inverse to lowercase s here and extract Alice's private key, which, of course, we see to avoid.
But even doing everything correctly here, there are some risks with opening, with creating two of two signatures, for example.
One of those risks is naive key aggregation.
The other one that I'm gonna talk about later is not so used, but what do I mean by naive key aggregation?
So let's say that we have Alice and Bob, who are trying to open a channel between the two of them.
And specifically, they're trying to figure out what their shared public key is gonna be.
Obviously, somebody has gotta start in that protocol.
So let's say that Alice initiates the conversation and she sends her public key to Bob, and then Bob is supposed to send his public key to Alice, and the sum of those two pubkeys is going to be the pubkey that's going to be the shared public key for the store signature.
Well, Bob can quite trivially do an attack where having received Alice's public key first, he first generates his own pubkey, but then instead of sending his random pubkey back to Alice, he subtracts Alice's pubkey.
And then as a result, we have that the sum of the two pubkeys that they calculate is one that completely eliminates Alice's.
So It ends up that Bob has the capability to unilaterally create a signature.
And of course, you do not want lightning channels where one of the parties is able to just unilaterally close it and unilaterally update the state without the other parties buying.
So that is one of the issues that require some solution.
Another issue, of course, is nonce reuse.
So here I have a quite simple equation where we have two separate signatures for different messages, m' and m'', but we're using the same nonce.
As you can tell, lowercase r, which is a random number, and uppercase R, which is the same random number multiplied by the generator point, are equivalent.
So what does the attack look like?
Well first of all, we can subtract one signature from the other, and then we see that we simply — so the r's cancel one — they cancel each other out, and we end up with an equation that is just the private key multiplied with this expression that we can actually quite trivially calculate ourselves because we know the public key, we know the public nonce point, and we also know both messages.
So knowing those, we apply the modular multiplicative inverse, and we have just solved for x, which is the private key.
So not great, and really highlights how trivial it is to attack and to extract a private key if you have two signatures that have reused the same nonce.
It's really, like I wish this equation were written out more frequently because I think people understate quite how trivial of an attack this is.
I mean you can write Python code in like two minutes.
Yes Cody?
So Sony got pwned, they were reusing nonces on all of their ECBSA signatures.
It was the same nonce for all the signatures for all the Playstations.
Yeah, that is true.
I believe that was the PlayStation 3, right?
Although for ECBSA signatures, so the thing about Schnorr is the math is so simple, it's just additional application.
You don't have any of the ECSA complications, so here you don't even have to think that long about why this attack is trivial.
However, obviously we need to mitigate these attacks, so MuSIC2 comes to the rescue.
I'm sure all of you have heard about MuSIC2 many times.
And essentially, the main thing that MuSIC2 does, it's like the same approach that eliminates the attack vector for both the naive key aggregation and the non-tree views, is it introduces coefficients.
And those coefficients are deterministic.
They are based on just hashing some of the data, and each participant hashes slightly different data.
And that results in not being able to execute such targeted hacks, because if you were to try to execute a hack where you feed Alice an adversarial pub key, that would actually completely modify all the coefficients, and then you would be back to square one.
So that's what music does.
And specifically, you know, let's dig into the math because it's actually not too complicated, at least with the key side here.
The way music works is we have these coefficients that are applied to each public key.
So maybe if we start, if we work our way from the bottom up, all right.
So if you see at the end, the resulting public key that we end up with is ultimately just the first public key multiplied with a coefficient, and the second public key multiplied with a different coefficient, the coefficient being C1 and C2.
So really the interesting aspect here is how are these coefficients calculated?
So one of the things that is important is that the coefficients are calculated by hashing something, and one component of the hash is all the public keys that all the participants are using, which means that in order for the hashes to work out, we need to know a priori what order those public keys are gonna be used in.
So In Lightning, what we do is we simply sort the pubkeys lexicographically, or based on their bytes.
But if you have some other sorting algorithm, or you just know the order and it's not sorted, but it's just ordered beforehand, that also works.
The important thing is just that you know which public key corresponds to which coefficient.
And then, say if you're Alice and your pub key also comes first, so your index is 1, because in math, indices don't start at 0.
If Alice's index is 1, then she simply takes her own pubkey, concatenates it with a hash of the sequence of all the pubkeys, which in this case would be first hers, then Bob's.
That thing is hashed, and that hash is concatenated with her own pubkey, then we hash that again, and so, you know, because of elliptic curve photography, we can simply interpret hashes as big integers, you know, we take that hash, we take that hash and simply use that as a big integer that is a coefficient for her public key.
Now, if you have been reading the Music 2 protocol, then you will know that this is not actually true, because we have an exception for the second index.
But in the grand scheme of things, it doesn't really matter.
So I think for understanding what problem music solves and how it does that, this is kind of deep enough.
So I hope I haven't confused anybody yet.
All right, because next is non-segregation.
And with nonces, we really do the same thing.
And one might actually wonder, why, if we're already doing this stuff with p's, Do we even have to bother with non-segregation and adding coefficients to our nonces?
And actually, this is probably a good point where I should poll the audience.
Any guesses as to why we care about nonce coefficients also?
Yeah?
You could fool people into nonce-reuse, right?
You could fool people into non-serious, yeah.
That is one thing.
And you could also construct a nonce adversarily in such a way that you would then be able to unilaterally create a signature with Music 2.
So it's really pretty much the same thing.
And with Nonsense, the protocol is a little more complicated.
But I really still want to go through it, because one of the innovations with Music2 is how this protocol can work with just one round trip as opposed to multiple round trips that we had with regular music.
So the way this works is as follows.
Each participant generates not one lowercase r that we had here Yeah, but they generate two So a music two knots is actually not one knots, but it is two knots.
Let me get back here so then both of these knots are then sent to the other participants, and what then happens is that we calculate a hash that we then use as a coefficient, and that coefficient is applied only to the second nonce.
So what happens is that we have one of the nonces being used at least once, and the other one being used some deterministic number of times.
But we have this linear combination which guarantees that we cannot really adversarially target either one of those nonces.
Specifically, how the coefficient is calculated is not super complicated.
Because what we do is we add all the nonces with index 1 across all the participants, that is going to be our aggregate first nonce, and we add all the nonces with index 2, also from all the participants, And then we apply the coefficients just to the second one of the two.
So we have these aggregate partial balances.
And we add them up.
We have a linear combination that is the same as doing the same linear combination individually.
But it just makes our mathematics a little simpler, because we don't have to repeat addition.
We have that automatically from the addition that happened beforehand.
And The coefficient we're using is actually the sum of the nonces with index 1, the sum of the nonces with index 2, the aggregate public key that we have already determined in the prior step, which we only need to do once, and the message that we want to assign.
So then, really, it's just a matter of aggregating all of those partial signatures with those nonces.
But yeah, really the interesting trick, the cool innovation with Music2 is the fact that each participant sends two nonces at once, and that we then aggregate the nonces by their index across all the participants.
However, even in Music 2, you would think, all right, now we have this thing where we are calculating coefficient, so really, music 2 is guaranteeing that there should be no nonce reuse.
Well, what happens if one of the participants were to reuse their original nonce, or their original nonce pair, across multiple partial signatures?
So here I have simplified the equation a little bit, because really what we would get is, you know, this expression at first, the hash multiplied with a private key, plus, in principle, it ought to be C prime, which times rA, and then plus rB, because we have those two.
But really, for the purposes of mathematical simplification, we're going to ignore the one that doesn't have a coefficient, because I think the coefficient one is more interesting.
And this, I'm pretty sure everybody can tell, is a very simple linear equation system.
So what we do is we simply multiply each one of these equations with the coefficient from the other one.
And then we can simplify the equation, and we can extract x.
We can extract the private key.
You know, if I hadn't simplified this, if I had also included the other partial nons, then we simply would have done this elimination step twice because, you know, we're trying to eliminate multiple variables, but we have sufficient equations to do so.
So why do we care about this?
That is because we don't really trust our counterparty.
Because in a multi-state setup, we don't really worry about the rest of the world attacking us and knowing what our private key is.
We also really want to make sure that each one of the participants in a multi-signature cannot know what the other participant's private key is either.
Because as soon as they do, we have lost the whole benefit of having a multi-sig setup.
So now that we know that these are the steps that we need to do in order to avoid the pitfalls with Schnorr.
We need to use music too.
How then do we transcript to actually creating and signing Lightning commitments?
And before we'll dig into that, we need to first consider what the properties of Lightning commitments are.
First of all, without SIGHASH, any Provout, or Covenants, or anything of the sort, we are going to have to rely on asymmetrical commitment transactions, which means that when Alice and Bob open a channel with one another, their commitment transactions are not going to look identical because we have the read-sharmony branch and the to-self delay is going to apply to different outputs depending on whether you're looking at the commitment transaction from Alice's or from Bob's perspective.
So right out of the gate, we already have two different messages that we need to sign.
Second, we have the same aggregate key.
Because our aggregate key is our funding key and it doesn't change across each new commitment, it means that we have to be extremely careful not to reuse nonces.
And because we have to sign multiple commitments, it really means that we have to have two non-spares as opposed to one non-spare that we send out with each exchange.
So let's look at how it would work in practice with, say, a channel opening.
So what you want to get to is you want Alice to have a signed commitment transaction with Bob's private key, such that she can later append her own partial signature where she is in a need to broadcast unilaterally.
We need the same for Bob, too.
If Alice opens a channel to Bob, then of course what she needs is eventually for Bob to provide her with a partial signature.
In order for Bob to be able to do that, Alice, right out of the gate, needs to send Bob her local nonce.
And That local nonce, which is the public nonce there, is the one that Bob is going to need in his partial signature, because the commitment incorporates an aggregation of those nonces.
So Bob, in order to be able to calculate the music two-step, needs to know what Alice's local nonce later down the line is going to be.
So, you know, if we just follow the flow, Alice sends Bob her local nonce, as well as the remote nonce such that Bob can create a partial signature for himself.
We then have Bob respond with the same step where Bob generates the nonce pairs and sends those in the accept channel message.
And then in Funding Creative, Alice can now provide a partial signature to Bob because what Bob needs is a partial signature that uses Alice's remote nonce, because the conventional transaction that Bob has, from his perspective it is his local, and from Alice's perspective it's Alice's remote.
So we have on Bob's side, Alice's remote nonce and Bob's local nonce, and on Alice's side, we have Alice's local and Bob's remote.
It is impossible to keep track of, and as a matter of fact, reading the spec and trying to implement it, it's really messing with my mind.
So that is why we have been proposing a little simplification of the protocol, where we don't send the nonces until they're actually strictly necessary.
And the way it works is when Alice opens a channel, she doesn't even bother in theory sending any nonsense whatsoever because she doesn't even know whether Bob's going to accept the channel yet.
So why generate any sort of cryptographic material if you're never going to end up using it.
So if Bob Huber does opt to open a channel with Alice and accept it, then he can generate a local nonce pair for himself.
And he then sends his own local nonce, which is still a pair, we have to remember that now even though it's called a nonce, it's still a nonce pair because of the whole music 2 thing.
So he generates this local nonce pair and sends it to Alice.
Now Alice knows what nonce of Bob she needs to combine her remote one with.
And she can just trivially create a partial signature.
And the nice thing is that now, because she has pre-committed her remote nonce, she can generate that partial signature and the nonce all in one step.
So she needn't ever store her own remote nonce.
In fact, you can just toss it out.
She'll send it with Funding Creative and never, ever worry about it again.
The other thing that she's gonna send with a Funding Creative message is also her own local nonce, such that Bob can later create a partial signature and then it's gonna be signed with Bob's own remote nonce and Alice's local one.
And this scenario, once again, because Bob has not pre-committed to his own remote nonce, he can very trivially generate it randomly as he's doing the signature and then as soon as he has a signature he can toss it out because he will never ever need it again.
With the channel operation we have pretty much the same thing.
You know we have the commitment sign and remote and act messages where we do pretty much the same nonce exchanges.
And we really...
When we send a commitment sign, we just need to send the remote nonce, such that Bob can then use a partial signature and revoke an act, as well as any revoke an act, he will send one for the next step.
He'll send the local nonce for the following iteration of the channel exchange.
But really, there isn't much of a difference between channel opening and channel operation.
Really the most important thing is that you have to have separate non-fairs for your own local commitment transaction and for the remote commitment transaction and it's something that can be a bit of a pain to keep track of.
One thing I will note is if you think that your node setup is such that you will never ever possibly have to sign a local commitment transaction with your own private key multiple times, then in principle, you don't even need to update your own local nonce, because there would never be a nonce freeze.
However, it is something that is very hard to guarantee, so for the purpose of safety, please ignore I said that.
Well, we have pretty much covered the thing that Hackroot enables with the nonce communication.
Even though on-chain the footprint is smaller, with the nonces we do have this additional headache that all of you who are implementing Lightning protocols are going to have to be cognizant of.
But that is not the only thing that Haproot does.
Haproot also, as I have alluded to earlier, allows us to have HAPtrees, where instead of having just one massive, dare I say, inscrutable script, especially with all this up-if, up-else nesting, we can very cleanly divide the spend paths into their separate tab branches.
And one of them just happens to be so trivial that we don't even need a script spend for it.
We can just use the keyspend path.
So with our vacation pubkey, or with our vacation key, we can sign and spend a transaction lightning immediately.
Because it's unencumbered by any sort of check sequence, verify, delays, whatever, that is the obvious candidate that is going to end up as the key spend path.
So In Taproot, the cheapest way to spend a commitment transaction is going to be using their vacation fee.
With the ScriptSend path, for the regular local output, it just has a self-delay.
We don't really need any other scripts that has other than the one that has this to self delay.
There is some discussion, there's some discussion as to whether we want to prepend one or something to object sequence verify, but you know, this is, I don't think the discussion is quite done yet.
The idea is that we're gonna beat the scripts into a manuscript parsers and generators and then see what the optimal script output is.
But just reading this, people might be confused because they'll say, oh, if check safe passed, but say 2-sulfulate is 0, will it go through?
To solve the layout, this should never be 0.
But there's going to be a follow-up case where there's going to be a bigger question.
So for HDLC offers, and I don't really want to go into accepted HDLCs because they're so similar to offered HDLCs. We still have the same situation that the revocation key is the unencumbered spend path.
And for that reason, it becomes the key spend.
For script spend paths, We now have two situations.
So one of them is if we are able to provide the hash preimage, which is marked in green here, And the script looks a little complicated, but the point is, once OPTCHECKSIG verifies here, then it should be 1, and then we have OPTCHECKSQUENCEVERIFY.
But if OPTCHECKSIG does not verify, then we have a 0, and then we have 0 OPTCHECKSQUENCEVERIFY.
And The question is, would it then mean that without a valid signature, we would be able to spend it without delay?
Well, it doesn't, because Ops CSV has some weird consideration where a transaction can never actually be spent with a zero sequence because it's doing greater than and not greater equals.
But just reading the script, nobody would know.
So this is something where we are still figuring out what the stack ought to look like and whether we want to optimize for minimal cost or whether we want to optimize for legibility.
I guess that is kind of the perennial debate within Bitcoin's script.
Maybe simplicity will make things simpler.
One would hope.
But, no idea.
It's, it's still kind of up in the air.
And I do hope that maybe some of you will also add your input to it on the spec discussion.
So this, of course, is a situation where we weren't able to provide the pre-imagined time, and so the original person that offered the HTLC wants to spend it again because it never went through and there we have quite trivial one-to-one matching of what the script looked like before taproot and what it's going to look like after taproot.
So nothing really all that complicated to get big into there.
And yeah, I really think that the script path spence are not the difficult part of taproot.
It's really going to be understanding and making sure that the cryptography is sound and safe.
Now if you have a Taproot channel open and there are some other nodes in the network, then in principle What do you think?
Are those other nodes able to send a payment if they don't support Haproot through a channel somewhere in the middle of the route that is a Haproot channel, or should they not be?
Should be able to.
Should be able to.
In fact, cryptographically speaking, there isn't really anything preventing them from being able to do so, right?
Well, here's the thing about Haproot, though.
The way that gossip works today, you have signatures that match on-chain outputs, and those on-chain outputs are signed using ECDSA, with taproot channels that wouldn't work because we now have Schnorr signatures, which means that even nodes that don't support taproot, in order to so much as be aware of the fact that there are taproot channels out there available for routing, they will need to understand taproot gossip before they even support actual taproot channels themselves.
So this is one of the issues that has to be discussed.
Now, El has a proposal up which says that for captured gossip, you have the possibility of combining and aggregating a signature across both the on-chain Bitcoin keys and the off-chain node public keys into one.
So you reduce the footprint of the gossip signature by a considerable amount.
It's just, you have to actually do that aggregation, so it will add a little extra communication that is going to be necessary between nodes just as they are opening the channel.
And you also need to make sure that nodes understand what this gossip is supposed to look like even before they necessarily support taproot.
So that is unfortunately one of the drawbacks of taproot, that by using a different signature algorithm and different on-chain footprint, unless you have support for gossip from the very beginning, you're going to have part of the network otherwise unable and even unaware of the fact that there is a part of the network that is now based on taproot.
So just going back to the beginning, so far we have talked about how in order to leverage the benefits of Schnorr for improved privacy, to mitigate the risks of Schnorr, we have to use Music2 for key aggregation and non-key aggregation, as well as Now, because we're using Taproot and therefore we need to use Tapscripts, we have to modify where those individual spent paths are located, as well as how the gossip looks like.
So it's quite a dependency tree, and I hope it gave you a little bit of an overview of what the constraints and design decisions and the vulnerabilities are that are driving the spec and why it is the way it is.
However, there is some really cool stuff that Caput enables that I also want to dig into, and that is BTLCs. BTLCs are also going to be driven by a bunch of very similar considerations.
But before I move on to PLCs, I was wondering if anybody had any questions so far.
Yes?
Does the fact that you have to explicitly announce the fact that you're on the gossip, does that get rid of any of the privacy issues, or any of the privacy methods that you get on-chain?
Yeah, yeah.
So if you're monitoring the Gaussian from lightning, then you would know the particular output on chain of course corresponds to the Lightning channel.
And that is a privacy consideration that you're facing right now already.
That is why there's talk about Gossipy 2, which would essentially be only committing to a fraction of the money that you have put up.
But that is its own can of worms.
So honestly, I can certainly recommend watching Matt Corralo's talk from CapConf last year, where he...
Well, it was titled, Lightning Has Broken the Stock.
And One of the major breakages is privacy.
Lightning has atrocious privacy today.
Even though with Tampered we improve on-chain privacy, if, say, Chainalysis and therefore the IRS—not, of course, that they're bad guys, but you know what I mean.
If they were to monitor the Lightning Network, then they would also know what the outputs are, tampered outputs on-chain.
So, Yeah, it's actually a big subject of research.
I don't think there is consensus quite yet, but I guess that v2 is the way to move forward, although I think it's slowly building.
We'll see.
I'm extremely curious to see how it's going to go, because it's definitely cause for concern.
Because as long as you have these privacy considerations, if you want to extend—as long as you have privacy considerations, you also have censorship considerations.
Because as long as anybody knows who payment initiators or secants are, they can be censored.
So I think it's a major issue for the full kind of research and investigation on Lightning.
But That being said, another aspect where we can somewhat impropriate the STTLCs, because of the issue that I mentioned earlier, where payments in hops could not be correlated.
Even though, to be quite frank, today already the odds of multiple hop All right.
Even today, the odds of multiple hops being correlated on chain are fairly low because you have to have multiple channels go on chain with HDLCs in flight, which, let's be honest, is not a big risk.
What this does help though with is wormhole attacks, for example, where somebody can see, if somebody has multiple nodes that they're controlling and those nodes are talking to one another and it just so happens that multiple of those nodes are involved in the same route of payment, then they would know that they are involved in the same payment and they would be able to steal some money.
With BTLCs, they wouldn't know because there is no correlation whatsoever.
So how do BTLCs work precisely?
Actually who here already knows how BTLCs work?
All right, cool.
I'm really glad that I'm finally able to actually bring up something that people here are not as familiar with.
Let's say that Alice is trying to pay Emily, or more precisely, Emily is trying to get paid by Alice.
I'm using this particular phrasing because Emily is the one that has to initiate the whole flow by creating an invoice.
Her invoice is no longer going to be a hatch.
What Emily does is she generates some random number z, some number of which is within the finite field we're using for our elliptic curve, and she multiplies it with a generator point, as we always do, so essentially the public point corresponding to that private integer, and she sends uppercase Z to Alice.
So that uppercase Z is now the invoice.
So the invoice, instead of being a hash, is and will be curve point.
What Alice does is the following.
So Alice sees that there are a bunch of intermediate moms, namely Bob, Carol, and Faith.
And Alice generates four random numbers, one for herself and one for each of the intermediate moms.
Those random numbers are A, B, C, and D, quite easy to keep track of.
And she sends her first PTLC message to Bob.
What does it contain?
It contains Bob's own secret number, B, as well as a PTLC that is locked to Alice's public point corresponding to her secret number, so uppercase A, and the addition of that, and uppercase Z, which Alice originally received from Emily.
Then Bob, having received this PTLC, he sends a PTLC to Carol, because he knows who the next hop is.
And that PTLC to Carol is locked to the thing, the value that it was locked to from Alice, A plus B, plus uppercase B, which Bob is trivially able to calculate by simply taking his own secret number that he received and multiplying it to the generated point.
However, how then is Bob able to send a PTLC to Carol or how is Carol able to send a BTLC today?
The interesting thing is that the BTLC that Bob sends to Carol in the Onion message also contains the secret number that Alice generated for Carol.
Bob doesn't know it because it's in the onion, but Carol does.
And that is where I really struggled with the visualization.
So the PTLCs are truly peer-to-peer, but this thing that is originating from the very beginning, you know, those lowercase b, c, d, and the sum here, those are meant to be in the onion packet that Alice sends.
And so those are only ever unwrapped at that corresponding point.
So then Carol sends a PTLC to Dave where she takes her incoming PTLC and tweaks it by the elliptic curve point corresponding to the secret that she extracted from, from the onion.
And Dave does the same.
And then ultimately, Emily receives one.
But the secret that Emily receives is not some random number that Alice generated for her, but it is the sum of all the random numbers that Alice generated.
And why does it work?
Well, let's work our way backwards.
So Emily has received a PTLC that is locked to the sum of all of these points, uppercase A plus B plus C plus D, as well as her own invoice.
She is able to unlock it because she obviously knows her own secret, her own lowercase z, and she knows the sum of the other points, albeit not any one of them individually.
The reason she knows that sum is because Alice sent it to her in the onion packet.
So then when she unlocks it, This is where the PTLC magic is coming in.
So the way that the unlocking is supposed to work is It's supposed to reveal to the preceding hop What the secret is going to be so the preceding hop sees this unlock using A plus B plus C plus D plus Z.
And then by subtracting their own secret, which Dave still has because it is lowercase D that Dave originally received in the onion packet from Alice, Dave is then able to subtract lowercase D and using that, unlock the PLC from Carol.
And that propagates all the way to the bottom.
Smooth sliding animation.
Where the last step has Alice subtracting her own secret from the thing that was unlocked by Bob, and then she gets lowercase z, which is now our proof of payment, which is really elegant.
You can see that each hop has a completely random PTLC value.
Now the magic is, how do we design a system where we are able to extract the secret?
Where the proceeding hop, just based on the signature, is able to know, okay, this is how they are able to create a valid signature for the other op that came before that.
This is where adapter signatures come in.
There's always a lot of talk about adapter signatures, but I think I'll leave it.
I think it's helpful to just talk a little bit about how precisely they work.
An adapter signature looks almost exactly...
No, drop that.
It looks exactly like a Schnorr signature, except it is invalid.
It is tweaked.
As you can see here, we have, you know, if we ignore the T here, we have exactly the thing that we would expect from a Schnorr signature, but our commitment in the hash is not to all random nods, but our random nods plus some tweaked T.
So what happens is, in order to be able to spend it, we need to find out what the tweak is, and then we can fix our little signature.
The tweak, when we learn what it is, the tweak can actually be used to embed a little secret in there.
So if the tweak is exactly the secret value that you're looking for, then once there is a valid signature, you can use that to, you know, calculate the difference between those two signatures and extract the tweak and use the tweak to create a valid signature for your preceding hop.
So let's think about it a little bit more thoroughly.
So let's say Carol wants to send a PTLC to Dave, right?
And she wants to make sure that they come up with an adapter signature that is initially invalid.
Because initially, if we look at this slide, this PTLC, We need an adapter signature for it, which means we need some sort of signature that is not correct, but that is gonna be correct once the right value comes in.
So how precisely, how do we do it, and what is that adapter signature gonna look like?
So we then decide that Carol and Dave do a music two with one another, which is completely unrelated to their channel opening.
It's a music two just for this particular PTLC.
So Carol generates some random key and some random nonce pair, Dave generates some random key and some random nonce pair.
Dave generates some random key and some random nonce pair, and they use that pair solely for this particular PTLC.
They then, instead of signing it regularly, they commit to a partial signature that is broken and that is tweaked by whatever the PTLC has to be.
Here the PTLC has to be a plus b plus c plus z.
So therefore, a plus b plus c plus z is our tweak, which means that then, once we find out the valid signature later on, that that tweak is going to be lowercase a plus b plus c plus z.
And guess what Carol needs to know in order to be able to spend Bob's PPLC?
She needs to learn what a plus b plus c plus z.
And guess what?
Carol needs to know in order to be able to spend Bob's PTLC.
She needs to learn what a plus b plus c plus z is, because then she can subtract her own secret that she received in the onion, and that way she can spend Bob's PTLC.
So now the question of course is, I think you guys can figure it out, especially with this slide, why are we bothering with this music complication here?
Why do we have to have music just to create an adapter signature that is tweaked damaged broken Whatever terminology when I use No, come on The same reasons you don't want the nodes private key leads, you don't want the payment point linked as well, if you're not doing the same knots, you know, computations or anything.
Not quite.
Just depending on that payment not to be there in general.
Not quite.
I mean, I guess, you know, what would happen if it were to be...
What scenario are we trying to avoid?
A payment being redeemed without it.
Having gone through, yes.
All right, you know what?
I'll just tell you.
So...
So one of the important things about this tweak thing is we want to guarantee that if there is a valid signature, it can only be the untweaked signature.
We must not have any valid signature for this message that is not exactly using this tweak from this nonce.
Which means Because, why is it so important for us?
Because if, say, it were to be spent on chain, because, I don't know, the channel had to close and it had to have a unilateral withdrawal, then we need to be able to extract the signature from on-chain and still be able to claim the PTLC that is incoming to us from our preceding hop.
In order to guarantee that the only way a valid signature is using this particular commitment and this particular tweak, rather not using this particular tweak or not using any tweak at all, is by making sure that neither party can unilaterally create a valid signature.
Let's say if instead of using music2, our PTLC basis for the adapter signature were offered by Carol.
So Carol just uses her own random public key when she sends a PTLC to Dave.
Well, guess what?
She doesn't have to wait for any sort of payment to go through.
She can just create a different signature because she has the private key already and go on chain with that stuff.
Then Dave is off in the cold.
Similarly, if Dave were to be able to unilaterally dictate which key were to be used for the PTLC, then Dave would be able to, when claiming his own incoming PTLC, do so on chain using a different key in such a way that Carol wouldn't be able to extract the tweak because, you know, Dave would be using a different nonce, and then Carol is left out in the cold.
So that is why we need to make sure that They both pre-agree on what the nonces are a priori, such that the only way there can ever be a valid adapter signature, or a valid de-adapted adapter signature, untweaked signature, is using the nonce and the public key that the decree agreed upon, such that the arithmetic always holds.
But once you do that, well, you already know what happens once you do that, but what is the complication?
What is the issue with that thing?
The hint is right here.
What is the issue with requiring that you have a music 2 exchange for the whole PTLC stuff?
It's an extra round trip.
It's an extra round trip.
So now an HTLC round trip is 1.5 round trips.
Here, that will become 2.5. So it's because you also have to have the commitment sign and then rebook an act, and you can also combine multiple messages in one TCP message.
But it's an initial complication.
We're going to have to see whether it significantly delays, slows down multi-hop payments.
We are going to have to see whether it adversely affects scalability, but we'll find out.
Yes, Dr. Do the non-sys need as an input the ptlc point transfer?
Can you sort of pre-share, like here's the next 10 non-sys and you can do pre-sharing.
Well, you can always do pre-sharing, but then with pre-sharing, you have to figure out, okay, how many do you have to share, how frequently do you have to share?
You're still moving the round trips.
I guess you can do it slightly less frequently.
It also depends on how frequent your payments are.
If you have like a million payments per hour, that pre-sharing isn't going to be much good.
But that is exactly the sort of thing that I think warrants research.
The only issue is right now we can't do the research because I keep getting pulled back into Swift stuff, so I don't need to come here.
Simple, backward channels.
It's just not ready.
I sincerely apologize for being here talking about this stuff instead of actually implementing it.
Here we are.
Are there any questions?
I'm sorry it took so long, because it's been 51 minutes.
But I hope it was actually elucidating to some degree.
So just in terms of, you're working on it in LDK.
I know that Rose Creek's doing it on the site.
Is every implementation sort of on board and getting all these things, or is it sort of one set of people's going?
No, I think the spec hasn't been merged yet and there are still new comments popping up.
And initially we had agreement to...
So one of the things that I was really excited about initially, still am to be quite honest, with the channel opening, if you read the spec, you have all of those different, you know, the remote, local non-spare, remote non-spare, partial signature for this, partial signature for that.
I was hoping to simplify the messaging a little bit to say, you know, if we have this partial signature, the partial signature only ever contains the remote nonce because that is the only situation where it's relevant.
So create a new message type that is partial signature with nonce such that the other party would immediately know what it is they're dealing with.
And as they are processing and verifying the signature, the same blob would already contain the partial nonce that they need to verify the mustic2 aggregation against.
And delay it to the point where it's needed, such that you do everything just in time and you do semantic aggregation so people understand the meaning and have an easier time following the protocol.
But there has been some back and forth on that, and moving when messages are supposed to be back to the original and then splitting the partial signature nonce back into a partial signature and the nonce, where now you have to understand what the hell a remote nonce even means.
Is it remote for the person sending it or is it remote for the recipient?
It's a pain to read and understand this protocol because music 2 is kind of annoying.
If we could make the stipulation that a local nonce is ever going to be used for a signature once, then of course the local nonce would only ever need to be exchanged once because we wouldn't have to worry about signature use, but that is not a stipulation that you can safely make.
There's a ton of back and forth on the spec, and I just hope that one day soon, hopefully Q2, We will have an interrupt for the simple half of channels Honestly, I don't even know whether it makes sense to work on that first and not on the gossip because as I was just saying earlier Gossip is actually more important But with the gossip you have this nested stuff and you have to do the aggregation where you are going to have extra round trips.
It's a lot of work and maybe honestly I should be asking you to not contribute to the spec because the fewer people are applying changes to it, the sooner we are able to get it merged.
Yeah, just like, you know, just hack it.
Send it in.
Yeah, that's good.
The references.
Anything else?
Thanks for everything.

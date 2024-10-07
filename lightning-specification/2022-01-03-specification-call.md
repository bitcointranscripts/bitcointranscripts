---
title: Lightning Specification Meeting - Agenda 0949
transcript_by: Michael Folkson
tags:
  - lightning
date: 2022-01-03
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/949>

# Introduction

When people put comments and they are fixed they should mark them as resolved so that we don’t waste time thinking there are lots of outstanding comments and we have to read them again. I think that helps a lot.

I can spend some time doing that.

There are a lot of comments, I’m starting at the bottom to see the things that have maybe not been addressed yet. There are things like “disallow non-SegWit outputs because we have an opportunity to disallow them and not have the issues with closing and dust amounts”. You did update that.

That should be in there. SegWit is not allowed.

I need to do a full review.

It is exciting to hear, this is great.

Once I am finally done with the first version of anchor outputs with fee bumping next on the list is dual funding and splicing. Hopefully we will get some traction here.

That’s great to hear.

# Warning messages

<https://github.com/lightning/bolts/pull/834>

I think this is good to go. We said we would re-add all-zero errors. It is not explicitly said that we can do all-zero errors and close all channels so Matt said that we should really re-add it before he ACKs. Apart from that everything looked good.

You changed the “must fail the channel” to “must fail the channel as referred to by the error message” but there is no mention that all-zeros mean all channels anymore. Maybe we should fix that. Did the bot get an upgrade somehow?

I fixed that warning message. I have added a few explicit lines. I should have done fixups, sorry. I didn’t push to the right branch, let me fix that. I will push the fixup commit, just need to clean my Git tree.

I think this one deserves to be the first PR to be merged in 2022. It has been too long, it has already shipped and already helped us. Do you realize it was opened year ago almost? We must have a limit of less than a year to merge PRs. We are barely in time.

# Clarify commit broadcast and clarify channel_reestablish requirements

<https://github.com/lightning/bolts/pull/942>

<https://github.com/lightning/bolts/pull/932>

I think both of these work well together, two clarifications. We’ve seen an occurrence of this thing on testnet where someone reestablished a channel with our node, was late, we did not close the channel and we saw that later they reestablished a channel with the right numbers and we did not have to fail the channel. Probably someone was testing that and verifying that we did just wait for them to send an error before closing the channel.

The weird thing about 932 is it says “should send an error to request that the peer fails the channel” but last I checked the definition for error still suggests that the peer force close.

No it means we send an error instead of failing the channel ourselves and broadcasting a commitment because we must not broadcast. 932’s must not broadcast the commitment and should fail the channel did not make sense because failing the channel would mean broadcasting our commitment.

That doesn’t solve the issue that you bring up.

The issue I’m bringing up is implementation. When you see the other guy is late the spec says you should already wait for an error before you force close.

Is your proposal then that the node that decides it is late should not send an error and give the administrator time to figure out what to do?

No if you realize that you are late you should send an error to the other guy to close but an implementation can choose to halt the protocol to give the node operator time to fix something. But if they cannot fix then yes you have to send an error.

I guess it is confusing that it just says you should send an error.

In practice I can see how this could be useful. Two things, one is that it is unclear what the expectation is. This will modify that to have them send it first. You need to be ready for either scenario. It is not a breaking change but it is modifying the expected behavior. It seems like y’all run into this pretty frequently but I have never had an instance where we were trying to manually stop a force close from happening. lnd’s behavior is bound by prior versions of lnd’s force closes. This is an interesting change in that it is not changing things fundamental, it is changing an expectation but you need to be ready for the prior versions still. It seems difficult to handle rollout.

What do you mean by prior version? It should be compatible as is.

If for example we ship in eclair something that lets you halt before sending the error when you see that you are late maybe that doesn’t work because the other guy has already force closed. In which case it doesn’t matter, it doesn’t harm either. But if the other guy has not closed and you have the DB issue our issue is mostly that if someone has a big node with thousands of channels and they just misconfigure the DB they would lose all of their channels as once. It would be a very costly mistake. They can easily avoid it if we just prompt when they restart and say “It looks like something is really bad. Are you sure that this is right? Do you want to continue?” We give them a chance to fix it and avoid a very horrible mistake that costs a lot of onchain fees.

It seems more of an advisory rather than a spec requirement. You can wait or you can just do it.

We are not putting any changes in the spec for that. We are just asking implementations to do what the spec says and only force close when they receive the error and not when they see the other guy is late.

I feel like what I’m getting at is a little bit more meta as far as changes of this nature to the spec itself. It should be pretty straightforward. I will double check that lnd can do it. Whenever we get a bad reestablish we will write it on disk don’t use this channel. When we close a channel we can still send that if they do SCB properly. I need to check that path, it probably works. We also have this old PR for a safe mode that would come up and would never force close until you manually said “Ok”. I think that is something you are moving towards.

Exactly. That requires the other peer to not anticipate your errors and not force close on you. We are trying to clarify the spec because the spec says you should not anticipate an error and you should not force close just because the other guy seems to be late. You should wait for him to send an error. There is nowhere where it says you should force close before that. But since implementations have started doing that we are just trying to clarify the spec to make it more obvious that you should wait for the error before you broadcast your commitment.

Is this related to the warnings I see when I force close?

No.

Did warnings die in the background?

No warnings are going to be merged soon.

I do not know what happened there. I pushed to the branch and GitHub closed it and I don’t know why.

In order to reopen I believe that you need to force push back to the last commit that was on the PR and then you can reopen it and then you can force push to something different.

I don’t know how I got no commits on the branch but I will figure it out.

I am going to make an issue to give this a shot. I think one of you already has an issue on our tracker. I need to double check that it doesn’t mess up our SCB assumptions. We always store the reestablish to make sure we can send it but it should just be a small thing.

There is one gotcha, it is going to be on our side when we implement the halting thing. If you halt and tell the node operator to check the DB but they don’t have anything better you need to store the commitment point that the other guy sent you. You will need that to get your funds back.

To my knowledge you all have implemented static remote key? The one thing I see with this is what if the error is never sent or it just gets lost. At this point the channel is just there and if your node doesn’t have a SCB, I guess they need something like that anyway. There is an intermediate step here between it ultimately closing, this error being sent. Maybe it is not an issue in practice. Before it was like get a bad reestablish, force close and now it is like get a bad reestablish and get the error, force close. Maybe it doesn’t matter, I guess we’ll see in the implementation. Is it true that eclair still doesn’t do static key? Or Phoenix, I know it is one of them.

Static remote key? No we’ve done that for almost as long as static remote key was available. It is only eclair-mobile that never implemented it.

I pushed an empty branch, that is why it closed. I am not quite sure how to reopen it. I have re-pushed and it is not giving me a reopen button. I may have to open a new PR which is the same PR with one more change.

I believe if you force push back to the last state, the last commit that was in the PR at the time the PR was opened then it will let you reopen it. I may be wrong though. That is how it used to work, you have to have the exact same commit in the PR.

You should remove your fixup, reopen the PR and then push your fixup? Is that right?

I think so. GitHub is stupid. To close the loop on 942 and 932, personally I am fine with this. I think it should send an error, that was my only trip up. It feels like the point of 942 is that you should maybe not send an error and wait and then send an error later. The text saying “should send an error” seems confusing to me. Maybe it should just be mentioned in the rationale, I am fine with the thing in principle.

Maybe we can add it in the rationale that “should send an error” does not mean send it immediately. You can halt and let the node operator do something before you send it.

Sure, that would suffice. It would be useful why this is the way it is.

That makes sense.

That was a comment for 942. I guess it also applies to 932.

Are they different?

They are touching the same thing and basically doing the same thing but from two different places. I don’t really care, someone else figure out how to merge those.

The spec advises people to breach in a certain case or something like that? I think this also gets at the whole “fail channel” wording which I think they made another PR for as well.

Yeah they did make a PR for that. This person, lightning-developer, is very helpful.

It is like Spartacus, I’m Lightning Developer. I would have to check this one. They are saying it can create a deadlock but I think it is just their interpretation.

I assume by deadlock they just mean the channel is there and it is not closing anytime soon. It could just be if the node hasn’t been online for a year or two. I’m not sure how it is different.

I think I should check this one out. It could be a typo fix or something greater, it depends on how much you squint at the shoulds and musts.

Do you think we should merge these two PRs? Ask lightning-developer to cherry pick pm47’s commit and add a section to the rationale to clarify what we said. Just have it in one PR so it makes more sense?

Aren’t they in different BOLTs? Yours is 2 and theirs is 5.

They are different BOLTs but they are touching the same thing. The lightning-developer one imports some kind of clarification about not broadcasting your commitment…

“Should send an error”, I see what you are saying.

It makes sense to have it because it is the general place where we explain what you should do with your commitments.

Isn’t this a layer violation? Here we are talking about onchain but then it is saying “Send a message”.

I just mean cherry picking the commit, having both of these changes in just one PR.

If you look at their diff, it adds “Don’t broadcast and you shouldn’t send an error”. Should sending an error, a P2P thing, be in 5 when we usually have thing in 2. 5 has just been this is how you do things onchain. Isn’t that what we intend the structure to be? If you remove that then this diff doesn’t do anything.

What you mean is that the change to BOLT 2 would be to completely remove the “should fail the channel” and not replace it with anything else? Just have 942 go in which says that you must not broadcast your commitment transaction.

I think Laolu is saying that the change in 942 that adds a “should send an error message” is in a weird place because BOLT 5 is all about things onchain. Mentioning that you should send a P2P message is very out of place there.

We should go with 932 assuming lightning-developer agrees that they are interchangeable. That is the only thing that the diff adds. Or we could just leave the “must not broadcast” to make that explicit. I think that is what they were getting at if it is outdated. I think they can be merged, just that one line can be moved. I’ll comment on that.

I opened [950](https://github.com/lightning/bolts/pull/950) which is the same as 834 but with a final fixup that makes it really clear that you are allowed to send all zeros and what it means.

Do you want to go ahead and squash the fixup?

It made more sense when we had the running commentary so yeah. I will now squash.

I posted that comment on 942 that we want to merge it, remove that line, cherry pick the other thing from 932 and try to move forward from that.

And then 932 should probably have a rationale update. Or 942 if they both go together.

I think that’s important because otherwise you have to read between the lines, why should I do this? That makes sense.

We’ll add rationale and squash it in 932 and ask lightning-developer to cherry pick that and make the small change in his PR.

Cool.

# Anchor outputs cleanup

<https://github.com/lightning/bolts/pull/903>

903, there’s just one small change for you Laolu. Just one typo, apart from that it looks good.

Sorry I am confused about 942, I thought we had this language in here already. I will go find it.

We very well might. 942 is just adding it in another spot. It is a trivial diff, merge it or not it doesn’t really matter.

Reestablish where you detect this talks explicitly about “must not broadcast”. “If it is wrong must not broadcast this commitment transaction” and that is where you’d implement it. Where have they put it?

They are putting it in the onchain BOLT.

Adding it in the onchain BOLT seems like the wrong place. I think it should be in 2 because that is where we define the channel reestablish stuff and that is where 932 added it.

Yeah onchain is usually where it is already done. It does talk about broadcasting. It talks about failing a channel here. I’ll comment on the PR.

# Add payment metadata to payment request

<https://github.com/lightning/bolts/pull/912>

I think this has interop. I think there are questions around actual deployment.

Regarding payment metadata, it looks all good to me. I have a PR on eclair that is ready to be merged. If you have the same on lnd and it hasn’t changed we know that it interops. We can deploy it. I did metrics on the eclair side so we will always put the payment metadata in all invoices that we generate once we activate the feature on the node. Then we register in the metric whether the sender actually sent us the payment metadata or not.

The receiving side, we only have one implementation right? So we test with eclair sending and lnd receiving?

I thought we tested in both directions?

You support both directions now? You said to me that eclair doesn’t support receiving so I could only test in one direction.

We support receiving, we just don’t support making it mandatory and rejecting the payment if the payment metadata is not there. But we do support receiving it and we will log that the sender actually sent the metadata.

I could also run that test? I think I did comment that I only tested one way in the PR. Everything is very straightforward so I don’t expect any problems there.

That’s great, thanks.

I added the extra line that Matt requested to include the metadata at the HTLC. If you include it with every HTLC you have the opportunity to fail early. If you include it with every HTLC you have the opportunity to fail early. If the metadata is not what you expect you can already fail with the first shard. You don’t need to wait for the shard to arrive that contains the payment metadata.

Sounds good to me.

For the lnd implementation on the receiving side what we do is just store the metadata that we receive. But actually that alone doesn’t make much sense because we generated the metadata ourselves so we are just storing the same thing that we generated. This thing only becomes valuable once you’ve got a different way of handling those invoices. That is a much larger project to take on. I guess we stick with storing it in the database and leaving it as a next step to do something smart with it. I think LDK is implementing code now based on this feature?

We need to ship reading it and sending it as fast as possible because we cannot do any of the other things until everyone sends it. That is the first step. It is useless but it at least lets us test whether senders do support that.

I just ACKed it. Unless there are surprises in interop I think we just merge it. Hopefully I will get the warnings one in first.

Sounds good.

One other question. Joost do you plan making a bLIP or something like that for the stateless invoice thing. Have something to accompany an actual structured use case of this? Then people can have something to implement off of if they choose.

There are multiple ways to do it.

Maybe you describe one way of doing it? On this one you say this is cool but what can you do with that, we know but for posterity.

We are a little bit locked on missing API hooks on lnd, we would experiment with this but not all the API hooks are there to do it. Just the HTLC intercept part, it doesn’t have an onchain path. You also announce this centralized database to run a cluster of nodes. More details about it would be nice, what to expect from it, we don’t want to implement things that are a copy of what you might already have. We are dealing with some uncertainty there whether to dive into this and create PRs for stateless invoices or to wait a bit to see what you’ve got with a centralized database.

Maybe we can make an issue on the lnd tracker to see what we are missing and what you have in mind there.

# Long term - Taproot

Next step do you want to look at something more long term? Is there a topic you’d like to touch on? Taproot or dual funding or splicing?

Taproot myself but happy to do other stuff first. I started [implementing it](https://github.com/btcsuite/btcd/pull/1787) over the break, I got super far. I just need to do all the OP_SUCCESS and some of the new policy things. Pretty happy with where lnd is right now. The one thing that came up with my implementation that will need to be in the spec or maybe another BIP, a deterministic algorithm for including the leaves in the actual tree itself. There are a bunch of ways you can do it. You need to make a binary tree but that is not canonical. It needs something similar to BIP 69 even though we don’t really use it for creating the tree itself. The BIP does have this recursive algorithm in there as well so we could try to further specify that. That is one thing that came up. How far are people in wallet level, node stuff? I have done the node stuff in btcd, I haven’t done the wallet stuff fully but I have things planned out for the wallet. You need an index of every leaf to the inclusion proof which is data that we don’t really store. We just store the script, there is other stuff to store. Are people starting to implement Schnorr stuff? I guess people use libsecp, are people starting to do wallet level or library stuff?

For which scripts are you concerned about? For the HTLCs we would just copy them and have only one leaf basically. For PTLCs it is not obvious that we would need multiple leaves. That depends on how much the leaf inclusion proof costs instead of just the branching. AJ said that we need to verify but it may be less costly to put everything in just one leaf for the PTLC case because it is quite simple. The version that I have is quite simple.

It has two leaves right now. That is something that didn’t occur to me until I got into the code. Another thing I was thinking about as well, this was a surprise to me, there are two sighashes, the external one and the internal one. But the internal one doesn’t actually commit to the path of the script itself. You commit to a leaf but not the entire path. I remember in the past we had an issue with duplicate scripts for HTLCs. The BIP recommends never having a duplicate script, maybe there is some weird thing where because you can take a signature for both of those two and they will be valid for a given input. Maybe there is some weird thing we need to account for. You can re-bind a signature for duplicate leaves and that is something that I didn’t know was possible. I thought maybe you committed the index but as far as I can tell that is not there. That’s another thing to be cognizant of when we are doing the design. I don’t think it affects anything but it was something surprising once I got into the code level. Something we should consider for future stuff.

That’s interesting.

A question on sequencing before we get too far down planning. The actual design here, we do need to redo gossip, at least for public channels right? That is something that hopefully we do it right and if we do it right it is a huge amount of work.

There are two paths naively. One is just say “We had four sigs, now we have one sig. Combine all the pubkeys.” The other path is what you were talking about on Twitter, redesigning the entire thing. Not having it be as tightly coupled to the graph and the outputs. Just doing some cooler ring sig type of thing. Maybe there is a Merkle proof in there as well, we have some code lying around. Which path makes more sense? Obviously the initial stopgap one, things get a bit smaller and then people get familiar with the MuSig type stuff at least. There is a [BIP draft](https://github.com/ElementsProject/secp256k1-zkp/blob/master/src/modules/musig/musig-spec.mediawiki) now for the key aggregation. It seems to me like the MuSig thing is pretty contained but the other vectors we have had some threads which are horrible to follow the discussion. We probably need to get something more concrete brainstorming wise. There are definitely some cool things we can do on that front.

I wanted to gage where people are at. The Chainalysis people are annoying me so I’m tempted to [redo the whole thing](https://btctranscripts.com/c-lightning/2021-11-15-developer-call/#upgrading-c-lightning-for-taproot). Though I think roasbeef has got a good point, a minimal step. But if people are interested, if people think we should do this then I can get a solid proposal together to do the next step which is basically divorce the gossip, figure out what the constants are so you don’t have to reveal all your channels.

I would hope we all want all of the above. So it is a question of what people want to work on and where they want to spend their time. But to some extent MuSig channels, awesome we want those. PTLCs is a whole other amount of work on top of just doing a Taproot switch. So to some extent I feel like redoing gossip to make it private is a substantially bigger win than the Taproot switch without PTLCs. Adding PTLCs is also a big win, I don’t have time to work either. At least if I can give feedback to the people who do have time, I am more excited about the gossip write up. I think I have already made that clear.

I’ll throw something together. I have got to figure out how does it interoperate with the existing one, you are going to have to do both for a while.

Exactly, the bridging. In either case if we make a new one we have that issue. You can’t validate the new channels anyway. It is a thing where there is some sort of hard split. Does that mean we should go for a bigger thing or do the minimal thing? Let’s say we had pointing to [t-bast’s docs](https://github.com/t-bast/lightning-docs/blob/master/taproot-updates.md), the initial first section done, people wouldn’t be able to validate those public channels. Unless you had like a bridge message, you send both. If you understand it, cool, if not you ignore it. This maybe means a new gossip message, node announcement 2 or whatever we want to call it.

We have to hard fork the gossip. Let’s do it once and do it with privacy instead of doing it twice.

That means we should all dedicate some time to it because we need to get it right then. We need to be sure that we all agree that this is the right way to do it.

Conceptually it is simpler. You go “I am a node and here’s my UTXO to justify my existence” and then you just add channels. We figure out what is the ratio. How much do you need to prove you own and how long does that proof last? What happens when it gets spent? Is it a UTXO or can it be any txo? All those details.

Number one, do we want to retain the trait that you are strongly bound to that UTXO? Right now at least it is a multisig and there is someone else. It seems like what you are saying is “I’ve committed 5 BTC. Therefore I can route 5 BTC.” How do you prevent that from being reused elsewhere?

My thought is if you have 5 BTC you can route 50 BTC, you can claim 50 BTC in channels, some factor probably. A naive implementation could use the first channel that it opens, attach that to its node “Here you go. I exist.” It doesn’t have to actually advertise, can just make up stuff for the other channels. If you have some magnification factor then you don’t have to add to your node announcements every time you open a channel “I’ve got this other UTXO”. Of course it could be cold storage, it could even be someone else’s UTXO and you have done some weird thing.

You can rent a UTXO.

Which is kind of cool.

Is it? If you have a magnification factor doesn’t that mean we introduce credit as well? You are saying I am adding leverage to my funds committed.

No. It means you don’t care what other people are doing. You never have any credit issues.

Let’s say we have 1000 BTC in the network right now. We could have 10,000 BTC overnight if everyone does 10x leverage with this right? Number go up.

Anything that detaches us from real UTXOs on channels is going to lose our ability to tell the size of the network as a whole. That is fundamental. If you are not revealing UTXOs you can no longer measure. We have to have some limit on how much they can claim. Prove a UTXO for 1 BTC, you can have 4 BTC or 8 BTC worth of advertisements for channels or something. If you make it one-to-one it doesn’t actually let you obscure that much because you end up having to advertise all your UTXOs so you can advertise your channels. Of course if the magnification factor is too big you can spam. For 1 BTC I can advertise a thousand channels.

You don’t necessarily have to point to a specific UTXO though right? I think you are assuming that you are pointing to a specific UTXO and you keep the same mental model. You could in theory have some kind of Merklized ZK proof and then you don’t point to a specific UTXO, you could remove the factor if you wanted to or you could keep it. You still gain the privacy.

How do you know which routes to try if you don’t know at least a ceiling of volume of BTC available?

To me it is not clear how I would route in this network.

You still have your max UTXO size, you just believe them.

Do I not have edges? You’re saying “I am creating a series of unconnected graphs and this vertex has capacity”. If there isn’t an explicit edge how am I routing?

You also then announce edges. First you announce “I am a node and here is a proof that I have some balance and I have some Bitcoin. This allows me to announce things.” From that you can announce edges. You announce some value and this is my node, my node has a value of 1 BTC. Now I am allowed to announce edges up to a total of 5 BTC.

Who is the edge attached to? You are announcing edges somewhere but who is on the other side of them?

Imagine the channel updates remained the same. Channel announcements just lose the UTXO pointer.

If we don’t have the countersigning of both edges can’t I say I have an edge to Matt and it doesn’t exist?

You can but that is cool because you ignore it unless you’ve got announcements from both sides.

Gotcha. It seems like this could be pretty big. I don’t know if conceptually it makes sense to me yet. Maybe it does to y’all.

There is a whole heap of unanswered questions. Can I take 1 BTC and advertise 10,000 tiny channels or is there some limit on how many channels as well as capacity?

If there is no leverage it is one-to-one. You need to map out the UTXO set in order to get something in the public graph. With this you have some multiplier, maybe it is good, maybe it is bad.

Why do you assume that we can’t do a ZK UTXO proof?

Size.

Where is it anchored in? Bitcoin doesn’t have any ZK friendly…

Bitcoin doesn’t have any friendly APIs for asking for a UTXO that was output at block x at index y. That’s not a thing either.

It has getblock txn which gives you the index. I have always wanted to make that get Merkle block check, I could give you the index, that’s the short channel ID and I get the Merkle proof. That would be cool.

We got rid of query utxos for a reason.

That is different. That is you give me a Merkle proof of a transaction, not just a UTXO. I want the output but I’m getting the whole transaction which we need anyway.

If you have UTXO snapshots you can do it. If you just use TXOs rather than UTXOs you can do it but I’m not sure what it does to the anti-spam properties if you just let anyone use any TXO even if it is spent. It is nice though because pruned nodes still validate it.

What about something like a TXO that was unspent for a month allows you to claim? That way you rate limit.

It feels like it could all probably work and it is going to need to be a parallel network anyway. T-bast is right, it is going to take a lot of people to examine stuff. To me it seems like a great background goal. I am just interested in near term Taproot stuff which is step one. This does necessitate something on the gossip layer but it can be smaller potentially.

That’s the point though right. If we do a naive Taproot public channel, we can do private channels all day long, then we “hard fork” the gossip layer twice.

You need something new, yeah.

We do it twice. When do you stop the backward compatibility stuff?

It sounds like Matt and I need to go offline and figure out what we can make. If we can make something that is convincing and simple enough then we go “That’s our hard fork.” If we can’t then we need to do something in the meantime. We will hard fork a second time and it will get pushed back.

At least if we do the super simple version everything else stays the same. Validation stays the same, for the most part the signature is slightly abstracted now. We are looking in the output etc. The routing table is exactly the same.

We don’t want to do it the same. The current one is horrendously broken and has a massive privacy issue.

It is not perfect but it is there. It is also not clear what properties we can achieve. All this stuff is early. I know Chainalysis [announced](https://blog.chainalysis.com/reports/lightning-network-support/) but it is kind of a good thing that they did.

Taproot is still early too.

It is more concrete at least in my mind than this gossip thing.

As far as Chainalysis, people just want a checkbox and they have that checkbox. It is actually good for Lightning.

Half of the reason that they launched it is that it is a data collection thing.

People asked them to launch it also. “We need something to tell the boys in blue that we are doing the checkbox”. They have the checkbox now.

They launched it, it probably doesn’t do much yet, it is probably just a huge data grab.

It is not even clear that they are running a node yet. We know they are looking at onchain stuff.

And Lightning payment data via all the new clients that they have signed up to check boxes. What kind of data are they collecting and using? They have all these invoices now. What data are we leaking in invoices? Maybe that is something we should be considering.

I think we need to find out more about the implementation. Some people I may or may not know have sat on some of these sessions to ignorantly ask questions and gather information. We definitely need to learn more.

Redoing the gossip this way does simplify one thing. That is that you announce your node then you announce your channels. At the moment we have this thing, you have to announce your channel and then you can do a node. You can’t really reverse the order and stuff like that. In some ways conceptually gossip becomes similar.

Right now at least on lnd if a node sends an announcement we don’t write to disk unless they have channels. Now you are saying you need to write to disk first to process their future proofs. Why can’t I just spam you with nodes and say I’m sending the proofs later?

The proofs go in the node announcement now. Node announcement 2 has some UTXO proofs or TXO proofs or something. You check those, you go “Cool you are now a node. Now you can announce channels.” At the moment you have to have at least one channel before you can send a node announcement. Otherwise you go “I don’t know who you are”. All your channels are now in the future, we have to reorder things and that sucks. Now your node announcement would lead in gossip order. You’ve got to bump that to the tail and that’s nasty.

If we are not giving information about the output itself then how can we verify the capability of the output?

We can do that by the set. In a ZK proof gossip model you would do the proof against a Merkle root of the set of Taproot outputs. Not all outputs. You could still enforce that.

I don’t know how long it would take to create something like that. We could do something super quickly and MuSig it. We’d need to learn a lot more on ZKPs, I read papers every now and then but in order to write this I’d need to dig deeper.

That is why I want to get together with Matt and see if we can sketch out something and see what the size of this is. I am on the fence here. This is nice in the end but do we hack something together now? We have got all the other stuff to do. A long term goal of having this better thing.

Zoom it out, probably this month lnd will be ready to start to do some basic experimental stuff with how it looks code wise. Keeping in mind the two things I pointed out, the duplicate leaf thing and some other stuff. But at least we are heading in that direction now. That doesn’t tie us to any designs, just a matter of making sure we know how to get the proofs on disk and the wallet stuff etc.

You are talking specifically about Taproot channels? Using Taproot for funding?

Yeah. Only Taproot for funding, step one of Taproot verification basically. Taproot Lightning transactions in the document that t-bast wrote. Mechnically porting things over, MuSig top level and then basic leaves, nothing super crazy yet, nothing super optimized. Just to get us that output to start with. From there assuming we have cool dynamic commitment stuff whatever else, we can bridge that theoretically to anything else as long as we get the output initially. On top of that there is what Z-man posted on the dev mailing list, hording the Taproot spend offchain. Now you don’t incur that upfront transaction, you defer it. You can hold it offchain and theoretically upgrade everyone on the fly offchain. At that point we need to worry about gossip stuff if people are doing a bigger flip like that.

I think the fix for a splice with gossip was you have something where you ignore the close, you give them a grace period if something new shows up and you just continue through. In theory you can go “It looks like you spent it but I am going to give you like 6 blocks.”

I am referring to the path where you never broadcast it. I keep the Taproot spend offchain. When I close I incur the two transaction penalty which I would have anyway if I didn’t open and close. This avoids all the channels closing when everyone upgrades. This needs to be fleshed out more but at least I’m happy we can make some basic progress on the onchain side. Also super looking forward to doing the MuSig within the MuSig. Letting people have multisig multisig channels, that is going to be nice.

I am assuming the gossip in the naive one will just turn out to be a basic proof that I own a UTXO. You can’t really prove it is 2-of-2 anymore. “I have a UTXO, it is a new style Taproot one”.

Why can’t you prove it is a 2-of-2? I can show you what the internal key is comprised of and you redo the MuSig key aggregation?

Are we planning on doing that?

It is possible.

But it is more work than just “Here’s a key, here’s a sig. Done.” It does mean that it doesn’t have to be a 2-of-2 anymore.

If someone wanted to generate a fake 2-of-2 they can always generate a fake 2-of-2. It doesn’t cost them anything.

They can do that today with multisig. I can just put my 2 keys in there.

Right, so I’m confused why we would bother proving it.

I am just saying if we wanted to retain the same level of “verification”.

But it is still a different level of verification. At least with current multisig it costs you more money.

To put two keys in there, yeah.

Why? We don’t care.

I think if you want the same level of binding and the binding being on the output.

I don’t think that is true though. Now you can make a 2-of-2 that costs the same as a 1-of-1. You don’t even have that cost anymore. I could split my private key into two parts and go “It is really 2-of-2”. I can still spam with any Taproot UTXO that I control and make it look like a 2-of-2 even though it is not.

Perhaps. It is cheaper. I feel like we’d want to at least retain the current properties we have but that is something that will come out in design.

I don’t understand why we’d want to retain the current properties. I think 90 percent of the current properties we have are entirely useless.

At least with the current version we ensure that we minimize reuse of the output. We at least say it is a multisig. That restricts the uses. If we say this is an output I can use anything. As long as I know an internal key I can use anything.

This is what led me to the gossip 2 stuff when I realized this. If we are going to go any UTXO anyway. I think you can turn any Taproot output into a fake 2-of-2 anyway.

Not if we require a particular MuSig derivation. That is going to hash all the keys into one. You can’t retroactively say “This random key is actually MuSig derived.” You can’t go backwards. You have to start with the 2 keys and then MuSig it up aggregation wise and that’s only valid. We do make it more structured.

Can you even prove a key is MuSig without revealing the secret key?

You just need to reveal the constituent keys basically. I have key A and key B, if I know what the hashing digest is and how to combine them.

It hashes the public key.

Exactly and the public keys are hashed in the main thing as well. It is all committed.

I am still very unclear as to why we need this property that it needs to be a multisig at all.

It does mean you have to share two keys in the gossip rather than just the one combo key. “Here’s a key, here’s a signature. You’re good.”

I think we’d definitely prefer to avoid 32 bytes over having that property.

“Here’s the UTXO and here’s the signature.”

We get one sig but we need to leave the keys. That is still a pretty big saving. The sigs are double the size of the keys.

But we can get more savings, why don’t we want more savings?

We could say no keys, just have UTXO. Can’t you just do “Here’s the UTXO and here’s a signature proving I own it” because of the Taproot output itself?

You can but the proof is less binding to the context, that is all I am trying to say. It would let you take any UTXO, maybe that is good, maybe that is bad. Maybe that is good because you lose the link on the graph level. Maybe it is bad because now you can take any UTXO and say it is a channel.

We are taking over the world so all UTXOs are going to be Lightning channels right?

I guess that’s the Taproot idea, you don’t really know.

That’s the whole point of Taproot, let’s not break Taproot.

It is not about breaking Taproot, it is about giving you a binding proof. I can write up why I think that matters in the non-spoofyness of the current graph. That’s a longer form thing.

Who cares about the non-spoofyness? It is useful for statistics but we could just not have this statistic.

It is the sanctity of the channel graph as a data structure in the chain.

Why do we care about that? The channel graph is about ability to route. I do not see why it matters at all if some other nodes in the channel graph even use credit. It is not sanctity in terms of connecting to onchain. I don’t see why it needs to connect to onchain except for statistic gathering purposes. Sure 1ML may break.

The original justification was anti-spam.

Anti-spam and that I know it is legit. Don’t trust, verify. I want to verify as much as possible.

The anti-spam part, I want to know that you have Bitcoin, I want to know that there’s some reasonable chance that you are just not sending me garbage and denial of service me when I try to route through you. Why do I care about anything more than that?

Because I want to verify as much as possible. Why do we refer the input amount of the channel? So I know that I can route 1 BTC over it. I could not verify, I could just try. That sucks for UX.

The node is often online, there’s some balance of payments in both directions and if a node says “I will route up to a Bitcoin”…

We disagree on this. I want to verify as much as possible. You want to verify as little as possible and you just want people to commit funds. I don’t think that is the proper route. I think we want to maintain the current structure we have right now. By verifying as much as possible you increase the cost of a false signal. “You went through MuSig derivation for this output and you need the two keys to spend. If you lose one of them you can’t spend it.” That increases the cost of a faulty signal.

Isn’t it the case especially with Taproot there is no difference in cost to faulty signal. Anything we can come up with, the cost of a faulty signal is the same as the cost of just having a wallet that is deliberately doing this.

That’s additional cost in the complexity of the wallet. If you want every single wallet to make a fake multisig output onchain you can do that but you increase the cost of the false signal.

If you want every single wallet to try to spam the Lightning node graph that wallet still has to implement taking that private key, signing the various Lightning messages etc. It is purely a question of how much additional software you have to write into that wallet in order to spoof the graph. The difference in the amount of software and the amount of effort required between doing a MuSig derivation and having some additional code to send Lightning messages and whatever is basically nothing.

I think I disagree. If you implemented MuSig you’d see the cost isn’t nothing.

In practice you are using libsecp so MuSig is just there for you.

I think a faulty signal should be expensive and you do that by requiring more structure on the input. If you want to fake graphs and whatever else you need to go through the MuSig steps. Before you didn’t need to.

But you are adding a lot of additional cost in the gossip layer, a lot of additional signatures, a lot of different validation complexity in order to make people do an additional 10 minutes of work in the software development stage.

We need MuSig anyway, we need MuSig to do the signing.

Let’s say we want to aggregate the signatures, me as a verifier I need to do the MuSig aggregation myself as well too. I am pretty sure the aux nonce actually commits to the MuSig challenge hash. The aux nonce is something they added to let you inject randomness for hardware wallets. Assuming MuSig is final requires you to have that value there then you bind it there.

It is a good point. It gives us the ability to obfuscate the onchain footprint. If that’s a priority we are going to lose this tighter binding anyway. But if we are not going to do that then I see the point. You are making it a little bit harder for people to lie and make up random channels. In practice for significant amounts of funds that you’d need to spam the network anyway and make fake channels, you’d probably want to be in a hardware wallet and it is a little bit harder to get your hardware wallet to do this crazy 2-of-2 thing than it is just to do it in software. I buy that there is a practical reason why it is hard for somebody to just make fake 2-of-2s that cost them the same from a practical point of view but I also agree that it is not that big a hurdle. It might be worth giving up that surety if we gain something significant. With the naive one I am happy to do the minimum thing, prove the structure and everything else. And in our more ambitious gossip 2 protocol if we decide to do that, then we go “We’re going to lose that ability anyway” so we figure out what we’re happy with. How much do you need to prove if we are detaching them anyway? If you don’t have to prove a specific UTXO, at that point then we are going to lose that anyway but we gain something.

Even the value of saving 32 bytes and a little bit of additional code on the validation side is worth it. Maybe others disagree on that.

I also think it is going to depend on what the MuSig we do even looks like. People are looking at the key aggregation, the signing could add other stuff that maybe adds to the requirements. We’ll figure it out. That’s why I’m trying to make sure we can start to dive in at the code level even if it is non-committal just to see if there is anything weird stuff. Implementing Taproot, I was surprised a few times already.

The thing I like about it is that it is simpler in some ways. Prove your node, claim your channels and it is done. If both sides claim a channel you just assume it is right.

It feels a lot simpler as long as you can work out exactly the kind of denial of service concerns and make the proof small enough. It is just a proof size question to me.

I have got to go implement it to figure out what I don’t know. Come up with a sketch, come up with some hacky implementation and convince myself it works.

To a large extent I want to know what the concrete proof size is which may require an implementation, I’m not sure. That is not a question for me, that is a question for like the Blockstream Research Crypto people.

They can’t be busy doing anything important (Joke).

I’m sure they have a hour to spare.

Last thing, I updated the test vectors in route blinding. If you have time to validate them then I think we should be good to go to get route blinding and onion messages in. No hurry, whenever you have some time.

That means I’lll check them in 13 days time.


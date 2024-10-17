---
title: "Lightning Specification Meeting - Agenda 1185"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-07-29
---
Agenda: <https://github.com/lightning/bolts/issues/1185>


Speaker 0: Are we on the pathfinding one or did we pass that?

Speaker 1: I think [redacted] should be attending because they added their new gossip status thing to the agenda. I think they should join soon, but we can start with the verification, where I think it just needs more review to clarify some needs. But apart from that, it looks good to me. 1182. That's the kind of thing we want to get in quickly because otherwise, it's just a mess to rebase everything on top.

Speaker 0: 1182 is on my list for this week basically. As far as getting through it.

Speaker 1: There's one thing that I commented in there. The way [redacted] put it, whenever you use blinded paths for payments, you usually do not use blinded paths before the introduction point, but you could in theory. They phrase it like it's something that we may want to do in the future, but do you think we ever want to do that? Because if we do that and use blinded path before the introduction point, that means that the sender needs to create dummy encrypted reception data and dummy values for the fees and CLTV, and I think it's really a mess. But I can't think of a scenario where we would want to use blinded path before the introduction point for payments. But if someone…

Speaker 0: Do you mean the sender just like making their own blinded path and using that independent of the receiver's blinded path in the invoice or…?

Speaker 1: Yeah, but what would that gain for payment?

Speaker 0: So that's a scenario, right? Basically, I have my own line of path and I use that in addition to yours. That's just to clarify that. Is that the scenario we're talking about or something else?

Speaker 1: It's just that in order to get to the introduction point, once you have found the route to the introduction point, do you make it look like it is a blinded path and tell each node inside that route that they are inside the blinded path and should relay as such?

Speaker 0: Oh, up until the introduction point. So you're saying a fully blinded route. Half from me, half from you.

Speaker 1: Yeah, what I mean is that I don't see what we gain by adding a blinded path from the sender. Oh. Hi, [redacted]. We were discussing 1182 and my comment about — let me post.

Speaker 0: I guess it's like uniformly where everyone does the same processing and it looks like one big tunnel. I guess you would lose the explicit errors outside of the tunnel, which is nice assuming that the part outside would be larger than the part inside.

Speaker 1: It seems to me that it's useful to not use blinded path before the introduction point because as you mentioned, you get nice errors and you can more easily retry. It's a bit annoying to actually use. Make it look like it's a blinded path before the introduction point because you have to construct the encrypted recipient data correctly. And it's a bit annoying, and there doesn't seem to be any benefit to that. But maybe it’s a use case I'm not seeing.

Speaker 2: Yeah, I thought about doing that too, but then I decided we've got code that works. We'd have to add a whole heap more code, and you'd lose the errors.

Speaker 0: Yeah. I don't think we do this right now. I guess one question I have while reviewing some of the blind paths code for dummy hops. So, for example, whenever y'all add dummy hops, are you adding dummy hops just to pad out the size of the blinded path or are you actually adding real fake policies or CLTV and fees? If you're adding real fake policies, what do you do for the fees, right? Because I guess you would want to add additional fees, but not too much that you're making them pay too much or something like that. I'm just curious about it because I was just thinking: ‘What should we actually do here?’ We could just do nothing. Does that make it look worse than if we did something? Because at least for the old shadow route, it was basically just CLTV. But now, you can add other stuff potentially. So I was curious: How dummy do you make the dummy hops look basically? Or how real do you make them look?

Speaker 2: We don't. It's like this big ‘fix me’ game. We should put dummy hops in here, right? You could argue that you should do what we used to do. We used to flip a coin and pick a random channel and go: ‘Let's pretend we were going down that one.’ Then, we'd add fees — it used to be that we would add fees and CLTV for that. But with MPP, we dropped the fee thing. It wasn't as obvious anyway. In theory, yeah, you should do both, but I think I decided that three dummy — like, making it always three hops long. So, ‘cause we only introduced single — it's a single if you've got a private, like an unannounced channel. That's when we automatically put one in. I'm like: ‘Really, we should just always make it three hops rather than a single hop.’ If we're gonna use it at all, we should make — three is a good number. It covers most of the network. It's believable. Then you've got the question of if you're just going to take some extra fees. I'm doing it for your own good, man.

Speaker 0: Yeah, I think it's really interesting because you can say: ‘Well, take some extra fees, but my node gets the fees that happens to be around.’ 

Speaker 2: Exactly. Yes.

Speaker 3: So actually, regarding the fees, the recipient could just eat these fees. Like, you could always use…

Speaker 0: Yeah, the recipient can get more. 

Speaker 3: You can always use your blinded routes with zero fees, and you eat these fees.

Speaker 0: Mm-hmm. It's a little tax. 

Speaker 3: That way, you hide the fees completely, and there is no way to guess the channels that are used using these fees.

Speaker 0: Yeah, I guess given we already allow overpayment in that regard as well. As far as the blinded hops, what we do now is basically, rather than targeting a fixed value at the moment, we take all the blinded paths that we have and make sure they're all the same length. Maybe one of them was five, one of them was three, and one of them was one. We'll make sure they're all five. That's what we do at least right now. Obviously, we can add that constant in the future, but there's just some code I was reviewing for MPP stuff in particular. I realized that we do a similar thing to what [redacted] mentioned last week as far as making it look like they all go to the same destination when you have multiple blinded paths for a particular hop. You can read the algorithm. So we have that now, and we're trying to get this into the next minor release, so we can get some more testing and stuff like that in it.

Speaker 2: There's a problem with eating the fees, and that is that if they've got a base fee and they use MPP, you have different amounts. So I wonder if you're actually creating a vector where they can potentially probe. I mean, because if you say: ‘Well, okay. We'll just pretend it's zero fee, right? And we'll just end up with slightly less than we expected.’ If they MPP across it, you'll end up with a different number if they have a different — if they ever said base fee involved or rounding in fact. So it's not entirely clear to me how that would work cleanly. But when the fees are so small at the moment that it's de minimis. You probably could do it and say: ‘Well, you'll allow some smaller payment than you expect because it's eaten by fees.’ Maybe.

Speaker 0: Yeah, it could just be like below one sat even, just top up 100% of each of them or something like that. Yeah. Depending on the amount. It's interesting. Gotcha. Okay, but I guess going back to the top thing, I guess we're saying: Is it actually useful to add binary passes yourself as a sender before the introduction point? Probably not, seemingly. You could do Trampoline, of course. That actually gives you some stuff. But maybe in this case, you basically just lose information. I guess the only argument would be uniformity of processing for all the nodes, but I don't know if that's a big deal either.

Speaker 1: Yeah, it's just that I found the paragraph on the spec a bit confusing because it makes it look like you should do that by default unless the previous nodes do not support route blinding. So I think it should be clear that whenever you do payment, the thing you do by default is not used to find the path before the introduction point. So, just a small clarification.

Speaker 0: Okay, I see the comment for that now.

Speaker 2: Yeah.

Speaker 0: So, 1182 is on my list. I'll promise to check it out before the next thing I have on my high-priority spec list. Should we talk about gossip status? Something new? I haven't read it yet.

Speaker 2: Yeah, I added it. So, one of my nodes had fallen behind. I misconfigured it and it didn't allow incoming connections for a while. The gossip was like: ‘Hold on. Why have you lost half the channel updates?’ I was like: ‘Okay, I could sync it manually and stuff.’ But then I'm like: ‘Really?’ Or I could play with the heuristics and try to get them to try harder, and then I'm like: ‘Ugh.’ But what I really want is to be able to send a message out to peers to go: ‘Here's how much gossip I have’ and have them go: ‘Nope. You need all of it’ and just flood me with gossip, right? So basically, it's the simplest message you can imagine. It says: ‘I know about this many channels. I've got this many channel updates. I've got this many node announcements.’ The idea is your peer goes: ‘Wow, you're way behind’ and just sends you all the gossip. So, I've got a scratch implementation of this. Of course, using the feature bit plus 100 and message plus 30,000. When you connect to a peer, we just send this message, and if it supports the feature, it should look at it. Basically, I picked a random number of 100. I looked through what's the — because you could be one block behind. Like, you could be a little out, right? There was one block where we had like 96 channels open. So I went: Okay, 100 is a good number. So basically, the recommendation is that if you've got 100 more of something than they have, just send them the gossip. Just send them everything. It was the dumbest thing I could think of. It will work, I think, and not give too many false positives. Because I mean, I know that LDK for a while were every so often just asking for all the gossip, and that's a bit antisocial. This is designed to be a little bit nicer. So you can at least tell that the peer is way off. 

Speaker 4: We still do that when we connect because there's no other reliable way to make sure you have all the gossip.

Speaker 2: Yeah. So I sympathize, but I'm like: ‘Well, this is slightly less antisocial, right?’ At least the other person opts in to sending you all the gossip. Sure for V2, I want fast, intelligent minisketch, blah, blah, blah, but this is basically a bandaid until then.

Speaker 0: So, isn't this basically introducing the old initial gossip dump that we took out, but this is like doing it with more context, I guess?

Speaker 2: Yeah, basically. The nice thing is that for bootstrapper, obviously, it just works really well. If you end up somehow missing a whole heap of data — particularly, I'm always nervous about node announcements getting lost because they're not kind of essential. So you can function reasonably well and without any node announcements at all. Because there's no really great way of syncing those up. So if you lose them somehow or whatever. So yeah. This is kind of about as trivial as you can get, and I'm hoping it won't have too many false positives. I don't want to — because my worry was you get into a loop where you start sending this and everyone starts going: ‘Oh, wow, you're way behind,’ and for whatever reason, you reject enough that you're asked to stay out of sync.

Speaker 1: Should we then also have requirements about gossip timestamp filters that say that you have to do a graph dump if you receive a gossip timestamp filter that covers basically everything? Should we entirely remove that in that case and rely only on gossip status to decide whether to do a graph dump on the other peer?

Speaker 2: That would be possible. I mean, at the moment we treat it as a trinary, right? I think that it is maybe still useful to have the whole ‘I want everything' message. But yeah, this could supersede that if we're on support it.

Speaker 0: One question for you, [redacted]. So, I guess you have this old node. Did you find that for some reason it didn't catch up? Or was it that it was super slow? Or you were looking for a faster way? Or was it in some weird…?

Speaker 2: It was in a weird state. It wasn't sinking half the — like, it seemed to have all the channels. It just didn't have half the channel updates, and I'm like: ‘What the hell?’ I don't know. I'm guessing that — so we pick a random peer and we query it. Then, if we don't get a response, we go: ‘Okay, I think we're caught up.’ I tried not to put any heuristics, like we should have this many channels or something like that. But it seems to be missing a whole pile of channel updates, which is really weird. So yeah, I should debug that on the side as well. But I was like: ‘We keep hitting these kinds of problems where people end up with partial gossip.’ I was tempted to go the map route for a while, where every minute, we ask someone: ‘Hey, give me everything.’ Or randomly pick a peer when they connect or something.

Speaker 0: But don't we kind of have that? As you're saying, for a while, we didn't implement the time test. Now, we have timestamps. Timestamps are great because nowadays, we ask for the heights, intersect that, and then also the time the timestamps, which is a way that you can spot check. So, I should say that I think we already do have the ability. It is more round trips because now, we have a lot of channels.

Speaker 2: Yeah, we spot check every so often, and then, we kind of double the number that we asked for. I'll have to check my heuristics again. But we basically go: ‘Huh? What have you got in this range?’ If you give us stuff we don't know about, we start doubling the range till we cover the entire possible lifetime. I'm not quite sure why that heuristic is not working. So, I'm gonna look through my debug logs. But yeah, I decided to try to fix it properly. [redacted], you were gonna say.

Speaker 4: I really feel like it does seem increasingly like we've all found weird issues with gossip, either on our nodes or someone else's nodes. We've never really managed to track down a cohesive set of issues here, and it seems like we haven't in fact tracked down any issues lately for the gossip problem. I'm a little hesitant about adding more band-aids. Like, band-aids are fine, but it seems like we should have more than a band-aid here, and we might maybe prioritize doing something minisketch-y.

Speaker 2: Yeah, Gossip v2 makes this much, much easier, which is kind of…

Speaker 4: To be clear, I'm not raising my hand to actually do the work.

Speaker 0: We're working on the implementation. We got to revise some draft PRs, but it’s moving along. 

Speaker 2: Well, this implementation was easy. I modified the spec. So originally, I was like: ‘Oh, if they were behind on node announcements, you should just send the node announcements.’ But then I added that ‘may send everything.’ So we basically go: ‘Huh, you're more than 100 behind on something.’ We just flood you with everything we've got, which is nice and dumb. We keep our flags, we'll only do it to each peer once. It's no worse than them just asking for all the gossip currently anyway. But yes, [redacted], I agree with you. But I definitely don't want to — I mean, we looked at some designs to do minisketch with Gossip v1, and they're all ugly. It's much nicer with v2.

Speaker 0: We're gonna be working on referring up some of the blind paths I just mentioned, and then, we'll basically be back fully on finishing up the concept of v2 stuff. Or at least what we have of that so far.

Speaker 2: We've got our release coming up within a month. So this will probably ship out in that, but with dummy numbers. So at least we can test and drop and stuff, and see if that helps my node.

Speaker 0: Cool.

Speaker 1: Alright. Next up is offers. Where are we on that? Now a few comments directly on the PR that potentially need to be addressed, and I'm not sure if everyone is caught up on the implementation.

Speaker 2: Okay. I need to do another pass, but our implementation is finally caught up. So, our master branch should be interoperable with everyone.

Speaker 5: We have to do the experimental ranges still and add new test vectors. I noticed also that the invoice error section is kind of empty, and there's a fix me, I think, in there. One question I had was whether invoice errors are expected only in response to invoice requests or either invoice requests or invoices.

Speaker 2: That's a good question. You can definitely send an error in response to an invoice. So, I think it's either. It's basically an error field.

Speaker 3: I think usually you don't set a reply path when you send an invoice.

Speaker 5: We did not until — I think we're going to add it soon. But it helps us in the sense that if we get an invoice error back for outbound payment, we could abandon the payment. We, of course, authenticate that.

Speaker 2: Yeah, it does give you an ability to — actually, I have to check our implementation. We may not set a reply path there either, in which case you just discard whatever error we have, but you certainly could.

Speaker 1: You just could reuse the blinded path you used to send the invoice request. You send the invoice request through a blinded path, you receive the invoice, and you can send the invoice through the same blinded path as the invoice request, right?

Speaker 2: You can, but we would ignore it because we never allow you to use — we strictly match that you're using it for the intended purpose. In theory, yeah, you could. The same way you could push an unsolicited refund a similar way, right?

Speaker 5: Yeah, we don't have state for invoice requests. If we get one, we're not going to hold on to it to the blind path. Oh, and we also authenticate request inside. Or at least we're adding that code now. 

Speaker 2: The experimental ranges, I managed to get it wrong. I've moved the recurrent stuff, so we still support the old recurrent stuff in a, I think, still works kind of way. We moved that into the experimental ranges to actually test that that works. Also, ‘cause it's cleaner. So that seemed to work pretty well. It was kind of painful because we used to have some really — it was really neat to cut a single range out of the invoice to cut two ranges out. It was just a bit fiddly, but we've got that now too.

Speaker 1: I'm curious: In which case would you want to send an error when receiving an invoice? What kind of errors did you encounter in your implementation?

Speaker 5: One if you receive an invoice where you don't understand the features, you'd send back an invoice error. That would be one.

Speaker 1: But that should never happen because there's a features field in invoice request. So the invoice should never set a feature that was not set in the invoice request, right?

Speaker 5: I think they were independent fields, right? Or independent features? There's nothing in them at this point. Actually, no, invoice has features, but invoice request does not.

Speaker 0: Either like it's missing fields that are required or something like that. Or say it gets bad or something. I don't know.

Speaker 2: Expired.

Speaker 1: Yeah. Or expired. 

Speaker 2: Wrong amount. 

Speaker 5: Yeah, expired, so they're on. 

Speaker 0: Yeah, it's like a sanity check, I would think.

Speaker 1: It would basically just be a way to get debug logs on the invoice generator to see that they have a bug that they need to fix, right? Because this is not really actionable in an automated way. You would just redo a request.

Speaker 5: I mean, you could see that when you have currencies, if the conversion is not to their liking, they might send back an invoice error.

Speaker 0: Yeah. Or the receiver just knows that the sender can't pay versus expiring. I guess it's one of those two. Either you get the fast error or they don't pay. Then, you just mark it as a dollar something.

Speaker 1: Interesting.

Speaker 2: I mean, if it's already paid once, for example, you'd be like: ‘No, I'm not giving you more money.’

Speaker 5: I think for that case, we do not send back anything because we actually send multiple invoice requests. So if we get multiple invoices, we'll just only pay the first one and ignore the rest. It's very normal for us, I suppose.

Speaker 2: Yup.

Speaker 0: Cool. Should we go to the BOLT 12? Mutual auth and contacts?

Speaker 1: Yeah. This is just picking your brain on this. We wanted to have a feature where you're able to have something that really looks like a payment app. When you pay your friends, they see that it's coming from you. So when you have trusted contacts and you send a payment to one of your trusted contacts and you are also in their trusted contacts list, we can automatically display: ‘Oh, this is coming from Bastien. This is coming from someone else.’ The way we initially did that was by reusing the payer key that was in our offer. So the payer key I use in my offer is actually the public key that identifies me as a contact. But [redacted] pointed out that we should probably decouple those because then, this is really tied to either a single offer or I have to reuse the same payer key in my other offers, which can be an issue for wallets that want to handle multiple offers and segregate them for privacy reasons. So, do you agree that we should do something completely different and find a completely different way to exchange those public keys and handle a public key that identifies you as a contact? Or should we reuse something that is inside the offer somehow?

Speaker 0: So you're saying add like another key? I guess like an opt-in?

Speaker 1: Yeah. You derive from your seed a specific key that is your contact key, and this one is never going to change. When you see one of your friends, you can send them a QR code with some specific encoding that says: ‘This is my contact key.’ You can store that and you can put this — when I use that as a payer key when you receive a payment, that means I'm the one paying you.

Speaker 0: Yeah, that can make sense. I guess either way it'd be like opt-in, right? That you would check, like use my contact key or something like that?

Speaker 1: Yeah. The thing is, then we need a way to distribute those keys and I'm wondering whether we could include them in BIP 21 URIs so that you can put them in your BIP 353 address directly. This way we'll have ways to pay you and ways to know that you are paying them. I don't know.

Speaker 4: You don't strictly have to — I mean, yeah, there was a bunch of conversation back and forth on the bLIP. You could imagine a key exchange protocol when you first pay. So you don't have to — I mean, there's a bunch of different property questions around what exact properties you want. It was my opinion that the ideal outcome is that a recipient can only see that someone paid them if you're mutually in the contacts, in the lists of each other. So, if I pay Bastien regularly, Bastien won't learn that I'm the one paying Bastien unless Bastien also has me in his contact list, which makes it a little easier. It makes it so that we can do things like exchange keys that are derived from the name or something. Versus if you want it so that you reveal that you're paying twice if they're in the — Bastien’s in my contact list, but not the other way around. I think there's a lot of different questions that we need to answer on what exact properties do we want before we start to commit to a specific key exchange. Is it okay if it only gets shown after the first payment, or does it have to work just in the contact list? Can we assume that a user knows they're BIP 353, and that you only want it to work if the contact list was derived from BIP 353? Or do you want it to work more generally, like someone scans an offer and then stores the offer in the contact list? Do you want that to work without BIP 353?

Speaker 2: I was sort of assuming — I think this is documented on the BOLT — that the issuer field — if the first part looks like a URL, like everything up to the first whitespace, then that is a handwave, something important, right? Whether it's BIP 353 or whatever else, right? Which is kind of a hacky way of ad hoc dividing the issuer field. But that was my assumption that the issuer field would literally be something and then perhaps, some comment. So, the obvious thought was originally it would be blockstream.com space. Blockstream incorporated or whatever. Obviously, blockstream.com is the URL or even HTTPS. Whatever. I think that scheme is reasonably robust and fairly simple rather than splitting into two fields. Do we want to extend that to BIP 353? Do we need — I don't know. I agree with [redacted] that I don't quite know what exactly this UX is going to look like. So, it's hard to come up with a protocol that works. But I mean, this is what the issuer field was kind of for originally. To basically say who's doing that.

Speaker 4: I think [redacted] wants it the other way around though, right? [redacted] wants the sender to tell the recipient who they are. Is there an issuer field on the invoice request?

Speaker 2: No. There isn't, but there is a payer note.

Speaker 4: Right. 

Speaker 2: And there's the payer ID, which is nominally a transient key, but doesn't have to be, right?

Speaker 4: Yeah. [redacted]’s kind of proposing we're using the payer note or payer ID, but only if you are paying someone who's in your contact list. Then, it is an open question to me whether that's exactly the thing we want when — do users expect privacy there or are they okay with it? Like, are users going to be suddenly surprised that their wallet is docile? The fact that they're the same guy who bought this thing once a week. Just because it was in their contact list.

Speaker 1: Yeah, I think we want, at least, the option for someone else to make this private, because maybe I only really want to give this key to my friends, whom I see in real life, and whenever I hand out an offer for people to pay me. I don't want them to know my contact key. 

Speaker 2: But you've got that UX problem on both sides, right? When you're paying someone, you're like: ‘Do I want to reveal who I am to this person?’ You're suggesting you do that through your friends' contact list. If you're paying someone in that contact list, you automatically reveal by default.

Speaker 1: Yeah. Or you make it a choice. You could, on every payment, let the user tick a box or make it tick by default if it's in your contact list and they can untick it. There are a few exceptions here. I think we can easily allow all of them, but it's rather where we want to put that contact key in the first place to be able to share it with others where I'm not sure yet what we want to do.

Speaker 2: I mean, so payer note is unstructured by definition, but I wonder if we want to, at least — so I don't know. It depends. Is 353 going to take over the world? In which case, it's easy. We end up going: ‘Well, if your payer note is structured the same way.’ Basically something that looks like a 353. Something that looks like a URL, or an app, or something followed by space and some junk. Then, that first thing is basically saying who you are.

Speaker 1: But why wouldn't you use the payer ID instead? Because it's just a public key, so that's exactly what the payer ID is for.

Speaker 2: Because it doesn't give you the information that you want as to who they're claiming to be, right? So, it gives you the actual key to pay them, but it doesn't give you anything to display to say: ‘This is Bob at whatever,’ right?

Speaker 0: Also, the payer ID is only in the invoice request, right? Not in the onion you send. So, you're basically tracking that the same person fetched the invoice, but not necessarily that paid it. I guess we're saying the same thing.

Speaker 1: What you include you as the creator of the invoice, you can include that in the encrypted recipient data for yourself in the invoice that you are going to receive it again.

Speaker 0: Ah, I see. 

Speaker 1: You were able to identify that this was linked to the payer ID, but the sender doesn't have to do anything specific here.

Speaker 2: Yeah. I mean, you can always delegate who actually pays it, but in theory, you have authorized it, right? Sorry. I honestly saw these briefly last night when I was looking through to edit the thing and was like: ‘Okay, I'm gonna have to read up on those and figure out what I think.’ We use transient pair IDs at the moment, so I haven't really thought really hard about what this would look like.

Speaker 4: We currently let the user pick whether they want a transient pair key or not. I think we were actually about to remove that option and force the user to use transient pair keys.

Speaker 1: Yeah. What we're currently doing is transient pair keys by default, unless you're paying someone in your trusted contact list. But we're still evaluating that as well. I think we want to make sure that wallets are able to choose for themselves what they do and that all options are on the table.

Speaker 2: So, there's definitely an intersection here with Nostr and stuff like that, where people are starting to use pub keys and actually build out a web of trust or a key distribution mechanism, which I definitely don't wanna get in the way of. Like, it would be nice if someone were to merge those really nicely, in which case, yeah, this would fit pretty well. As long as we don't have to go through a PGP signing party, I'm good.

Speaker 1: Alright. Let's keep thinking about it and discuss it directly on the PR and move on to something else.

Speaker 0: Cool. Okay. We’re gonna do some other stuff. No updates on Taproot stuff on our side. We fixed that bug I mentioned a bit back. I think last, Eclair's working on some interop. They're figuring out the splicing component of it. Any updates related to that?

Speaker 1: [redacted] is on vacation right now. They have been making some progress there, but they have quite a bit to do before they’re ready to share something. So, they have some work that needs to be done on that side. That's what we're working on. Cool.

Speaker 0: Cool. As mentioned in Taproot Gossip, we're looking to get back to that pretty soon. We want to get these by blinded path finding receiving stuff in first, and then we'll revive these PRs. Feed them our draft PRs. I think last, we got some diffs from people, and then people said they'd take another look at it as well. Okay. Liquidity ads.

Speaker 1: For channel jamming, there has been some discussion on channel jamming. I think [redacted] and [redacted] will need to discuss something.

Speaker 6: Yeah, I think we're kind of just down to bikeshedding on values for the bLIP. Like, [redacted] and I only need to use a binary value, and I think [redacted] wants to use a value between zero and seven. So, just the mapping of those two things between them is difficult. This is an experiment, so we do want to be flexible. But I think for the purposes of the bLIP, if we just say: ‘Zero is unendorsed, seven is endorsed, and it's up to your interpretation what the things in between are,’ we can move forward.

Speaker 4: I mean, is there a way we can use this test and do 0 to 7, but then also gain information for whether 0 to 1 will work? Because in an ideal case, we run the test, we learn what the right number is. Hopefully, that number is just 0 or 1 because that's much better for privacy. But if it's not, maybe we will discuss that. Is there a way we can use this to learn that?

Speaker 6: I don't think we can learn about both things at the same time. Because right now, what it would look like is whoever runs what [redacted] and I are working on interpreting 0, 1 and then the async node uses 0 to 7. My concern…

Speaker 4: Right. So maybe we do one, then the other?

Speaker 0: But isn't the question like what does 7 mean? And 0, 1 is like a clear cut...

Speaker 4: Exactly. That's kind of where we are. A system that uses zero to seven is never really going to set a seven. So then, where do we interpret that threshold meaning 1? That's really difficult. This is why I kind of think a 0 or 1 is preferable because you don't run into these interpretation issues.

Speaker 0: Yeah, I guess the question is like if you get a 4 what do you do with that? Does that change it for you? I would think for the initial computation probably not, right? Like, a 4 is a 1.

Speaker 6: Yeah.

Speaker 2: I think that [redacted], if you want to take that one, but I think the algorithm they were working on was basically using a certain state probability of success and mapping that to this value 0 and 7?

Speaker 3: Yes, exactly. So actually, I could work with any number between 0 and 1. I treat it as a float, basically, and 0 and 7 is just like, I discretize it. But I treat it as a continuous value.

Speaker 7: So I think for us to understand what comes from you, it will help us if you'll give us a cutoff. ‘Cause 50% doesn't seem —  I don't know. Something like 80 or 90 or something like that. What should we round to zero and what should we round to one? I think it will also inform you — maybe some logarithmic scale or something like a softmax kind of thing, but where should we cut off?

Speaker 3: So currently, the score we output is an estimation of the priority that the HTLC will succeed. 

Speaker 7: I understand.

Speaker 3: Then you can — I don't know what should be a good threshold. I guess that depends on you. 

Speaker 7: Did you run some simulations? What kind of numbers do you see? 

Speaker 3: No, we didn't.

Speaker 2: How do you estimate the probability of success? I'm interested in that.

Speaker 4: Basically, for each source, we just look in the past how much fees they paid divided by how much fees they should have paid if all of the HTLCs had succeeded.

Speaker 2: Right.

Speaker 7: So, is 75 a number that you'll feel okay with for the experiment?

Speaker 3: Yeah, I guess. Okay.

Speaker 6: I mean, you have historical records with your peers, wouldn't you be able to just run this at one point in time for us and get probabilities for everyone? Then, we could get an idea of where that threshold sits. It's not perfect, but this doesn't need to be perfect because it is an experiment.

Speaker 3: We could also measure what's the range of priorities that we get and instead readjust it so that like half means not a priority of half of this succeeding, but that it's exactly in the median of what we've seen so far?

Speaker 7: Maybe, but I think like if you run the Times of Peace version, there will be some kind of threshold that most of the time it's above.

Speaker 3: Yeah. Once we deploy the version, we can measure it and we'll tell you what's the number.

Speaker 6: Yeah. I mean, that would be perfect. As long as we know where to split that range reasonably. I don't think 50-50 is a great split point for us. But if that's anything greater than 6, and you can just tell us based on your history, I think that that gives us a good shot of supporting both things.

Speaker 3: I was thinking 50-50 because that's the bucket that we then use. I mean, do you assign 50-50 buckets to the unendorsed and endorsed?

Speaker 6: Yeah, but that's unrelated to what good reputation means.

Speaker 7: It's a very, very different meaning. So just for us to be able to move forward, when do you think you'll be able to have numbers?

Speaker 3: Well, the code is almost ready. We just need to fix a few things. And then, I don't know, [redacted], what do you think?

Speaker 1: I think it's mostly blocked right now on the question of what to do when we are not running a reputation algorithm and whether we should forward the endorsement value we receive or not. Because that's one of the outstanding questions on the bLIP.

Speaker 3: Yes. So, the answer was that it shouldn't be used for decisions. Like, it's just an experimental field.

Speaker 6: So this is a read-only thing. I don't expect anyone to be actually bucketing things on this yet. It's just to figure out whether these reputation algorithms actually work. So, the idea was that you just forward it on with the signal that you would have set, but you don't make any forwarding decisions, right? Because we don't know how these things operate in mainnet. But I do think one question that also comes up with the multi value range is we would only want to have a default where you forward on as endorsed if it's above that threshold and otherwise, set to 0. Because I'm a bit worried about getting the step-down effect if we just copy the incoming value. So I do think a default behavior needs to be that we shut that down to 0 very quickly if it doesn't have a value above this threshold. 

Speaker 3: Why? 

Speaker 6: Because I think that if you're running a 0 or 1, you're really not leaking any information about your location in the path. But if you are running a range of values, you risk getting something like 7, 6, 5, 4. And I think that that's fine if you're the one running that code, that's like your choice to do that. But if you're a random node in the network and someone forwards you a 4, you don't want to forward on a 4 because you're revealing more information about where you are in that path than you would like, so if you get a 4, you just round it down to 0 by default. 

Speaker 3: Okay. 

Speaker 6: That make sense?

Speaker 3: Yes.

Speaker 6: Okay. So we'll wait on you to get numbers for — we also need to brush up our implementation. But just to sort of summarize that: It's only forward on as endorsed if it's fully endorsed; otherwise, drop it to 0. I think in the bLIP, what we have now is just leaving it up to interpretation is fine. So, 7 is endorsed, 0 is unendorsed, and your algorithm can choose the interpretation in the middle. Is that fine?

Speaker 3: Yes.

Speaker 6: Okay, cool. Then, we'll grab that number from you, and that's what we'll actually choose as our threshold to relay so that we can get some meaningful numbers. 

Speaker 3: Okay. 

Speaker 6: Cool. Thanks for taking a look at it. I appreciate it.

Speaker 0: Okay. Ten minutes left. Anything popped on the agenda or people have burning questions of?

Speaker 1: Yeah, there are two things I wanted to mention. First, [redacted], I pinged you on a PR, where I used the official spec version for splicing so that you can start doing cross-compat tests with CLN, and we got... 

Speaker 8: Awesome. Perfect. 

Speaker 1: Regarding async payments and Trampoline, I've also created a commit that details — we had some discussions with [redacted], [redacted], and [redacted] about how to combine the Trampoline and blinded path. I have a data commit that does a rough spec of that. [redacted] and [redacted], you probably want to take a look at it for the ECDH thing I've been doing to include the payer ID and to be able to make sure that the payment really comes from the node that received the invoice and generated the invoice request basically.

Speaker 9: I think it looks good to me. [redacted], did you have a chance to look at it yet?

Speaker 4: No, I haven't looked at it yet.

Speaker 1: Okay. So basically, I'm just using the almost the normal Sphinx, but when we derive the row and mu key to encrypt and do the MAC — instead of deriving this key based only on the shared secret that is using the normal Sphinx ephemeral pubkey that comes from the header — we also add another shared secret which is ECDH between the invoke request player key and the node.

Speaker 4: Yeah, I think that makes sense. I think I was happy with that, and I think that's basically what I was thinking.

Speaker 1: Okay. It's just a bit annoying to write in the spec because I realize now that [redacted] has started reworking the BOLT 4 spec to make it much better and much more readable in terms of what we actually do in terms of cryptographic operation, I re-read the Trampoline spec, and it's really not explicit enough. So, I want to rewrite it to be clearer, like what has been done in BOLT 4. I'll do it at some point, but I just wanted to get a rough consensus that this was an okay way to do it before.

Speaker 2: Are we okay to merge the BOLT 4 rewrite in that case once we've had a bit more time? We don't need another meeting. We'll just make sure we've got it. I think we're pretty close.

Speaker 0: Yeah, I have it marked as high priority. I should be able to get a pass through today, if not tomorrow. Basically, just to avoid rebasing because it's going to touch a lot of stuff.

Speaker 2: Yeah. It's a world of pain for everyone. So yeah, [redacted] has a comment about it being a little bit unclear at one point. so I will try to…

Speaker 1: Also, one about updating the route-blinding test JSON file that doesn't refer to the right name, but apart from that, it's fine to me. Once that is fixed, it's an ACK from me.

Speaker 2: Yeah, cool. Okay. I'll get on that today.

Speaker 5: [redacted] sent me a note earlier saying they were updating the Trampoline stuff according to the [redacted]’s changes from earlier today. So, I just want to pass that on.

Speaker 1: Okay, cool. Perfect. Then we can continue discussing it directly on GitHub and offline. Liquidity ads. I updated the spec based on the feedback we had from the last meeting. I quite like it. It's ready to review whenever people have time.

Speaker 10: Hey, everyone. If no one else has something to say, I would like to introduce myself. I just got a grant from OpenSats. I'm implementing the Lightning specification in .NET C#. It's called N’Lightning. I'm pretty advanced on this. I'm doing BOLT 2 and 3, but I stopped it to do BOLT 11, so people can already use it. Like, everybody uses C# in their back-end, they will be using the library. It should be a library and a full implementation. So I expect to have a node by the end of this. I already have BOLT 1, 8, 10, 9, and 7 implemented, and I can connect to other nodes and start doing the feature bits and other things, starting the communication. Now, I'm doing the transactions and just relaying the HTLCs. 

Speaker 0: Cool.

Speaker 2: Nice. 

Speaker 0: Definitely open issues if you find that stuff sucks. I think we know some stuff does. We're trying to fix it.

Speaker 2: If it's not clear, then yeah.

Speaker 10: I'm having some issues. It's not clear in some places. Then it's just a matter of — I was trying to follow from 1 to 11, and it doesn't work that way. Because for 1 to work, you need to go to 8, and then you implement 8, and then you go back to 1, and you can send messages. Then, I would like to implement 2, but then I need feature bits, so I went to 9. Then I went to 10, and so on. So it's not straightforward to implement, but I've been working in the field for five years, so I got a feel of how to do this. But other than that, everything is very clear what's happening. I guess when I got to implementing not only the library but communicating to other nodes, I might have some issues.

Speaker 0: Have you done BOLT 4 or the state machine? I'm assuming no.

Speaker 10: No. BOLT 4 not yet.

Speaker 0: Okay. Yeah because we're working on BOLT 4. I think BOLT 2 could definitely have a revamp, particularly [redacted]’s state machine stuff too. But you always get to have some new eyes looking at stuff because we have code at this point.

Speaker 10: Yeah. It's been some years since someone got from the ground up running this. It's been fun.

Speaker 2: Yeah, welcome.


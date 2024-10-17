---
title: "Lightning Specification Meeting - Agenda 1183"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-07-15
---
Agenda: <https://github.com/lightning/bolts/issues/1183>


Speaker 0: How do you do MPP by the way? For example, you have two blinded paths. You don't even split inside the path.

Speaker 1: We won't MPP. Our new routing rewrite — which is on the back burner while I sort all this out — should be able to MPP across because they give you the capacity. In theory, we could do that. In practice, if you need MPP, we're out. While I was rewriting this, I was thinking maybe we should have just fixed the onion more seriously and said: ‘You will put exactly this many sats through this route.’ It would have been simpler in some way, but that would have forced MPP to be on the receiver side and re-drive.

Speaker 0: Yeah, it would expire so quickly, and you don't even know if you're using a real kind of a real blinded path where the introduction node is not a direct peer of yours. You don't have a balance. You don't know what to put in there.

Speaker 1: Yeah. Exactly. You would have to throw a lot more trial things at it. But I don't know because the errors you're going to get are going to be terrible anyway, right? It's just going to be: It failed. So, I guess you hope that it's a capacity problem and you try again, in theory, but there's going to be a whole…

Speaker 2: As far as us, we have a PR — that I haven't reviewed yet — that claims it does MPP. Do I know how it works yet? Not necessarily. So, I'm not established like someone with the edge case you're talking about as far as which path you select and things like that. I think now we'll generate multiple blinded paths and we'll also incorporate those multiple blinded paths into payments. I think we just sort of treat the blinded paths as the way we treat hop hints as far as extending to the graph and then, wrap from that and use that. But this is on my list to catch up on. We merged something yesterday. doing some refactoring to get ready for receive. I don't think [redacted] is here, but they’d be able to explain it better. But I think we have it.

Speaker 1: We do something even dumber. We basically take the first blinded path for payments, we route to that, and we just slap the onion on the end. We don't MPP. We don't do anything. It's like the minimum viable solution. So if you give us 20 blinded paths, we will use one. That's the actual payment.

Speaker 3: I think we do the same thing as LND. I think we just treat each blinded path as if it were a very weird one-hop route hint with a given fee and a given…

Speaker 1:  You also have to isolate the node in case it's public because you can't not use them. That's the issue, right? You can't not use the blinded path if they're provided. 

Speaker 3: Yeah. 

Speaker 1: If it's a public node, you've got to cut off all the existing channels first and then add in that. So, it's a little bit nasty.

Speaker 3: We don't actually handle it as if it were a BOLT 11. We don't munch it. We just have code in our router to say: ‘Oh, these are some blinded paths.’ Okay. These are all hops that get to the destination, and we don't care what they do. We invent a fake pubkey for the destination.

Speaker 2: [redacted], I guess I missed the beginning of it, but are there any edge cases or concerns in your mind as far as MPP bypass, or are you just wondering what the current level of implementation is?

Speaker 0: I'm wondering about how you handle it because when you get an error from inside the path, you're just going to get a garbage error. Do you assume that you may try to split and see how that works? There could be multiple channels actually in that blinded path, so maybe splitting inside the same blinded path would work. That's something we do right now because initially, we didn't, and now we do it. Basically, we have kind of the same thing that you do in LND, where when we have a blinded path, we add that to our graph as a virtual hop, but we add it a few times. We duplicate it and add it a few times so that you can automatically use it for MPP in pathfinding and actually split by using the same blinded path multiple times, but taking the total capacity into account, but potentially splitting into it because maybe inside that blinded path, the first part is actually a node that has two channels. Each channel has half of the capacity that you think you may be able to route. We had issues where we wouldn't be able to route through that. So, we are just spraying those blinded paths multiple times into our graph. It works okayish, but it feels really hacky.

Speaker 1: Yeah. But if somebody is relying on that for their blinded path, they're in deep trouble. Your blinded path really has to have capacity because of the lack of feedback to the user. If it doesn't work, you're really in a small percentage, you would hope. If you're worried about that, you should be providing multiple blinded paths.

Speaker 2: Yeah. In theory, since the receiver is selecting them, they can do more stuff to make sure they're better paths. That's like a research thingy. The receiver could be doing probes to themselves or something like that, right?

Speaker 1: Well, [redacted] pointed out that most failures happen on the first or last hop. So now, you've got last hop information. So it may not be as much of a problem as we think. But yeah, if you're doing elaborate blinded paths — so we were talking about fronting, like picking a node and saying: ‘You're going to front for all my payments and routing through that.’ In that case, you may have multiple hops and it gets dicier, right?

Speaker 0: We're on the edge of discovering all that as users actually really using blinded paths and really starting to use multiple payments. So it's going to be a lot of fun. Yeah.

Speaker 1: I wonder if I should add a dev mode where in dev mode, we actually return some meaningful errors rather than just blinded path errors.

Speaker 2: Yeah. That's one thing I need to look at error-wise because our pathfinding is very much based on trying to interpret the error in a way to reduce the search space or increase our confidence interval in one of the paths. Obviously, if we get a vanilla, very large error,  like a coarse-grained error, I'm not sure what we do there. But yeah, that's a good question. I need to review this PR, obviously.

Speaker 3: I think, [redacted], it's not filter introduction points as non-Tor nodes. So it is entirely possible you failed to send to me because the introduction I picked was a Tor-only node. Even according to my node, we don't filter on that.

Speaker 2: You're saying that y'all filter out Tor nodes for introduction points.

Speaker 3: No, we do not. I believe [redacted] failed to pay me because of this. 

Speaker 2: It looks like the connection was down or something between them.

Speaker 3: Or they just didn't know how to connect to the Tor node.

Speaker 0: No. Actually, it was an issue with node announcement propagation because we found that specific node that you use as your introduction node. The only node announcement that we had in our DB was one from 2022, where they only had a Tor address and we never got the node announcement with a more recent version of their IPv4 address. I tried to troubleshoot that and I didn't see anywhere in the logs where we received a new node announcement from them. So, I think there are overall issues with node announcement propagation in the network, and that's an issue for the environment.

Speaker 1: Yeah, because there's no good debugging for node announcement propagation. If you get a failure, most of the time you don't even notice.

Speaker 2: Yeah. For example, we had that issue where we weren't yet assuming TLV onion and we didn't have a node C-lightning. So, we tried to do the legacy and they're like: ‘We don't like legacy.’ But so we do have the thing that — I think it's in 18 too — we will just assume TLV onion now. So now, we can actually start to break that up. That was one thing where it's like: ‘Oh, we didn't have the announcement,’  so we fall back. We don't need to fall back anymore. 

Speaker 1: Yeah. So, one good thing about gossip v 1.5, for gossip stuff, is that it does get a lot easier for us to use like minisketch to do set reconciliation and that will hopefully lead to better propagation of down the road to node announcements. 

Speaker 0: By the way, I don't know if this is an expected issue, but we've noticed that WOS seems to be running an updated version of LND, they kept forwarding us channel updates that didn't set the HTLC maximum MSAT optional field. First set the channel flag — the one that we renamed to must be one — zero. I thought that nobody was forwarding those channel updates anymore. But it's like they are. I don't know if LND still by default does not check it and still relates those absolute channel updates.

Speaker 2: LND should always set it. We should always set the max, but I don't think we'll reject something if it's using the older format, if that's what you're saying. Because remember we added it, then we made it a TLV, if I recall correctly, right? Or we found a way to munge it into a TLV?

Speaker 3: Yes. 

Speaker 0: Yeah. It was, of course, compatible in a way. I don't remember. There was a trick. But actually, we actually checked that almost all of the nodes did set this, but there were only a few channel updates that did not set it. We modified the spec to say: ‘If that is not set, you should just drop the channel update.’ We're still seeing some getting relayed — at least from a Wallet of Satoshi's node. So, I don't know if they modified anything or if it's LND’s default behavior that they rebroadcast stuff that is actually obsolete.

Speaker 2: Okay. I can look into that. I know we always said it, but maybe we're not rejecting the ones that don't have it set properly. Okay. I can write that down.

Speaker 1: Yeah. We ignore new ones and because we will prune them after a certain period of time, you shouldn't even have any old ones in the gossip store.

Speaker 2: I mean, I guess [redacted], that would indicate that there's some node in the network that I guess is ‘important’ that's not setting it, basically, which is the…

Speaker 0: Yeah, exactly. I think there are still a few nodes that are still sending channel updates that do not set this to one and do not set the HTLC maximum on the same side. And this is exacerbated by the fact that I think LND nodes would still relay the channel updates instead of just dropping it.

Speaker 2: No. Yeah. I think you're right. I think we don't drop it, but we do set it. I can double check that, too. That should be an easy thing to just drop. Okay, cool. I wrote that down on the side.

Speaker 0: Right. Should we start with the agenda and start looking down the PR list? There's a first one that I think should actually be a prerequisite to the ones [redacted] opened because there's probably going to be a small rebase conflict in it that is clarifying the CLTV expiry for blinding path. I think we're on the same page between LND and there. I think we're on the same page with LDK because you just take a huge security margin, so you don't really care. But I'm not entirely sure if you are not, and I don't know if CLN, you're on the same page of that. It's 1176.

Speaker 4: Yeah. What you said is right on our end.

Speaker 1: I'm just checking the commits. It looks correct. Yep. For the path expiry, for example, we go 600 seconds plus 10 minutes times by the CLTV delta, which seems like a reasonable value. Like, an extra hour on top of like the estimated 10 minute blocks. Because you have the problem of when you expire, and that was our rough formula. I think that's fair.

Speaker 0: But that means if you only it depends on whether you include the mean final expiry delta in your own max CLTV expiry or not. Because otherwise, just one hour is really six blocks. I think most people use 12 blocks at least, or 18, for the mean final expiry delta.

Speaker 1: You have to include that, yes. Otherwise, you won't even make the payment. If you take the worst case and we multiply it out — I'll have to check the code, but I was looking at it recently. We basically went: ‘600 seconds plus an average of 10-minute blocks will probably work.’

Speaker 0: Yeah, but do you, in your own, even in the payment free on the site itself, you add the expiry delta? The mean time? 

Speaker 1: Yes. 

Speaker 0: Okay. So I think we should be good. If everyone ACKs it, we can just merge that one, and you can then rebase.

Speaker 1: I'll rebase yours because I like your fixes over my fixes better. So we'll rebase that.

Speaker 2: Cool. Going back on the thing we just mentioned, so I looked at our code and we do reject it, and we've been rejecting. This is basically if you have a zero max HTLC which is not set, we'll reject it. We started to do that one year ago. So, maybe they're running some custom thing. We can reach out to them about that because I mean, obviously, the newest version is the best, right? Like, that's just how we work. So, but yeah, I'll ask them about that.

Speaker 0: Yeah. I’d be interested because it looks like they're at least running 0.18 based on the feature bits that they set, but maybe it's a fork and maybe the fork code does additional things.

Speaker 2: Or they had a merge issue when they were doing it. Because we have a PR from a year ago — this one here — that started to add it basically. I think that was in response to something like this that came up. For example, one of the Breeze people made this issue ‘cause they probably ran into the same thing where it's not optional anymore. We said: ‘Oh yeah. We should make that required.’ But we can reach out to them and see what's going on there.

Speaker 0: Alright. So should we just merge 1176?

Speaker 1: Yep.

Speaker 0: Good. Next up is [redacted] rewriting BOLT 4 to actually be useful when you implement Sphinx, so that we don't all have to re-understand everything, and I think it's a really good thing.

Speaker 1: The main thing was renaming the blinding to something else because it's also other things, but spelling out the requirements. [redacted], so you pointed out in your comment that: ‘Yeah, we should re-hoist that into a requirement.’ It is in there now. As literally, the new style, when you must do this as this and it says you should record. I think we suggested — can’t remember which field we suggested —  it might've been the HMAC field.

Speaker 2: Yeah, it can be something. You can hash out like a small value as well. ‘Cause I think something came up maybe a year and a half ago where there were some divergence about that, and that's because I think we had like a sentence in this spec. 

Speaker 1: Yes.

Speaker 2: It was just sort of qualitative. You should do this versus exactly why.

Speaker 1: Well, when I went to add the blinding stuff in, I went, there's no good place to put it, and so I went: ‘Fuck this. I don't know what I'm doing today.’ Now, I haven't written up the ‘encoding the onion’ in the same style, but at least I've done the decode, which is now in the modern the step-by-step recipe.I seriously had to read our code to figure out some of the bits too because it was described all the things, but we never actually laid it out. I think it is a win. The new language.

Speaker 2: As far as that, [redacted] has this recent blog post just going through the Sphinx stuff in more detail. So this could be useful as well, because I definitely would have to look at our code to verify and stuff like that. Maybe we can use this to help and potentially, even some of the diagrams here as well if you scroll down in it. 

Speaker 5: I've had to read the entire Sphinx paper really, to more or less, make sense of some of the references in BOLT 4. So plus one for that.

Speaker 0: Yeah. I also had to create diagrams and write these documentation to understand Sphinx.

Speaker 1: Yeah. So I think we've all done it at some point. The intersection of that and the onion because the onion messages have the double encryption because there's three parties involved. It gets particularly hairy. It kind of assumes you understand all the Sphinx wrapping and then, you've got this other layer. I got myself very confused while I was trying to fix up our implementation because we had all these pieces implemented separately, and we're gonna have one place that implements all of the onion stuff. It was quite a task. So, there's some minor comments. I've got to rebase now, and [redacted] has some fixes and things. But I think generally, people like the idea that we should rework it. So, if you're thinking of the second one — if you try to read the whole thing, you'll tangle yourself. Because there's textual moves and then there's changes and stuff. If you actually read each commit, it's much clearer. So if you want to look through, you should read the whole commit. Or fuck it — sit down with a nice glass of wine and actually just read the whole BOLT afterwards and see if it makes sense. Because I'm sure there are other things we can clean up there too if we wanted to.

Speaker 0: Yeah, I agree. That's the point of PR. I think we should review quickly because I think that's the kind of thing you don't want to review, have to go back at it again and re-review everything. So please, if you can all find some time to review it so that we can just merge it quickly and get done with it, it would be great.

Speaker 1: Yeah. It doesn't actually change anything. It just finally spells it out.

Speaker 0: Alright. So I guess it's just a matter of reviewing those two. Then on the other side, we've been doing some mainnet tests where [redacted] has been very generous with their sats, and I can't send them back because of bugs in Phoenix. I'm sorry. I really want to, but I can't send them back. There's a bug.

Speaker 3: I want my 42 sats back, or 21, or whatever it was.

Speaker 0: It's really great because we've been able to find some issues related to those node announcements. Making sure that the onion would correctly fit. I'm also writing the update to the Trampoline spec to the Trampoline to blinded path version, so that we can then build on top of the async payments and all the other things that the LDK team wanted to do. So, I hope I'll be able to have a spec PR up soon for that. On the other side, I think we're just back to just finishing our code and testing that everything works. I would really like to see some tests about the failure cases and verifying that everyone handles failures the same way correctly. That's a bit harder to test because everyone needs to just modify their code to introduce fake failures, but I think it's useful. So, I hope we can get that done in the coming weeks.

Speaker 1: I have some test vector updates for new test vectors and just some minor tweaks that are still in my queue because I haven't completely finished my rewrite. I've still got a pile just of silly little changes. We talked before about zero-length blind hops being a trap that you shouldn't allow them and stuff like that. So, I have a few more changes to push, but they're incremental, and none of them actually change semantics. They're just cleanups.

Speaker 3: Speaking of testing the offers stuff with Phoenix, I also found some fun weirdness in [redacted]’s selected DNS provider. But the code to do DNSSEC verification stuff seems to be quite robust now for those who want to get around to 353 or whatever it is. The DNS pull stuff seems to work pretty well now. I did get [redacted] to look at all of my crazy crypto shit and they said it was ‘not bad.’

Speaker 5: That's about as good as you can ask for, right?

Speaker 3: Yeah, I figured that's probably sufficient.

Speaker 2: What signature scheme does DNSSEC use? Just curious.

Speaker 3: SECP256R1.

Speaker 2: Oh, the R1. Okay. Gotcha.

Speaker 3: Which I implemented from scratch. Nothing. For a reason. 

Speaker 1: You just added another thing to my to-do list. Yeah, we should do 353. I also want to see people implement your bLIP, which allows you to resolve through onion messages.

Speaker 2: Our question for you, [redacted] — I think it's probably come up on Twitter or something like that a few times to follow some threads — but what's the preferred way to handle 353 if you have like a ton of users, basically? Is it that you put one wildcard thing and then you do the demultiplexing when you're sending the offer? Or are you just putting a bunch of records or…?

Speaker 3: Yeah, kind of up to you. Kind of up to people how they want to handle it. If you can do the DNS thing, that's obviously — if you're custodial, it's obviously not a problem. You just do the wildcard thing and then the who they're paying gets shoved into the invoice request. So you just have it when you skip the invoice request. It's not a problem. If you are small scales, obviously also not a problem. It's only if you are a large operator who wants to offer addresses for people non-custodially on your domain, that's a question, and there, yeah, you can do either one. So, I think Phoenix is just going the whole just added to DNS because whatever. A million DNS records is super easy. But you can also do the wildcard thing. You just have to create a whole — I'm not going to bother specifying the protocol, but you can absolutely do a thing where the user gives the LSP, or whoever it is, some set of payment hashes. They generate invoice requests. They can do that. I'm just not going to bother writing a spec because I don't know. DNS is easy, man.

Speaker 2: I guess one of the operational questions, like [redacted], are y'all like using roughly three API? Are you running like your own custom thing or…?

Speaker 0: No. We're just using the SDK provided by AWS for Route 53 to be able to create records on demand.

Speaker 2: Gotcha. I guess that seems like the simplest way. At least if you're using that infrastructure.

Speaker 3: Yeah. I think most stuff is pretty cheap, but also running a DNS server is pretty easy. The bitcoinheaders.net thing, which shows the entire Bitcoin header tree in DNSSEC-signed IPv6 addresses — so it's whatever,  a million times five or eight or something entries plus all the DNS-like signatures — fits on like an R-PI running bind. It's really no big deal, which weirdly enough, Cloudflare mentioned in a blog post, it's like I have more records on my R-PI than Cloudflare has on their big accounts. So many of them just aren't set up for this. So sometimes, it's annoying to deal with them, but it is also really very trivial to just do it.

Speaker 2: Oh yeah. I run our DNS on the $5 Digital Ocean box I've had since my sophomore year of college

Speaker 0: I think we may look into that then because AWS doesn't charge you until you reach 10k DNS records, but then they charge you a bit more. It's not crazy expensive, but it's still, I think, too expensive for what it is. So, I think we'll look into it as well. 

Speaker 3: Yeah. Just run a copy of Bind. It does transparent DNSSEC signing. It's all super seamless. And then just run, if you don't want to host all of it yourself, just find a secondary DNS. There's a bunch of people who offer secondary DNS services who might be willing to run with a bigger zone for some moderate amount of money. Or just run 10 copies and all of the DNS stuff set up. Mirror itself very well. The mirroring protocol is standard across all of the DNS implementations. You can run four different DNS implementations and the mirroring stuff all works super seamless. It's actually a very well operational modern protocol stack.

Speaker 1: The $5 a month Digital Ocean box as a DNS backup is pretty cheap.

Speaker 2: Yeah. That's what I'm writing too.

Speaker 1: And trivial. Like, just set it up to mirror.

Speaker 2: Cool. Okay. I guess we kind of covered 1180 just now. You hear anything you want to add on that? This is the invoice request.

Speaker 3: No. We covered it. I mean, it's just the one commit. It's just put the data in the thing, and that's it.

Speaker 2: Yeah. This just so the host provider can know who they're paying to basically.

Speaker 3: Yeah. This is really for the custodial.

Speaker 2: Maybe they should credit.

Speaker 3: This is really for the custodial folks with the one wildcard DNS entry. You just know who to give the money to.

Speaker 2: One question. I saw some stuff around the B-thingy. So, is that a softer requirement now? Is that a harder requirement? Because I think people are talking about distinguishing versus not. I don't know how to type that on my keyboard. I guess I would copy paste.

Speaker 3: There was a lot, a lot, a lot of discussion about this. There was like: ‘Well, we wanted to be backwards compatible with LNURL, so people can do the like seamless upgrade downgrade thing.’ But also, there were a lot of issues with the LNURL email thing. I think Alby uses their Alby domain for both their corporate email and anyone can register an LNURL. There are name collisions. So, somebody who works at Alby, somebody else has their LNURL. So, the Bs are trying to find some kind of middle ground there. The spec tries to say you have to have it there in your UI. You should expect users to not type it by having it fixed next to your text box. If you have a little copy button for your users, it should include the B. If a user types in a double B, you should ignore it. So it's trying to walk a little bit of a middle line. I mean, the intention is that people will have a fixed B next to the text box that you won't necessarily have to type.

Speaker 1: I mean, the eventual endgame of this is that Gmail provides you — you've been emailing someone and you want to send them some sats and it just works right. The overlap with email addresses is not an accident. It is a feature, right? That is also the reason why you shouldn't do the LNURL scheme. Because the idea that you would be telling — Google would love to know every fucking payment you make and know. I do think that we want — it is a feature that overlaps, right? 

Speaker 3: Yeah. There's a lot of debate there. I don't have strong opinions.

Speaker 2: I think the combo of this and the silent address thing is kind of cool. I'm not going to lie. You just have this thing, and it's all reusable, basically.

Speaker 3: This is what made me go from a silent address bear because I was like: ‘Ah, new address format. No one's ever going to adopt this.’

Speaker 2: Yeah, the scanning and everything.

Speaker 3: To like: ‘Oh wait. We can do this. We can make it backwards compatible. You can have a regular on-chain address too, and it'll fall back to it. But if people speak silent addresses, you'll seamlessly get no address for use.’ So yeah, this is what took me from a silent address bear to like: ‘Oh, actually though’.

Speaker 1: Oh, yeah. We should totally be pushing silent addresses.

Speaker 2: In 353, could you have — well, I guess just like a generic address thing. It doesn't say this is a silent address. You say this is the on-chain fallback basically, right? Then, it's up to you to know…

Speaker 3: So there is also a lot of debate around this between [redacted] and the folks. They wanted no fallback. So they want people to put the silent address in like a Bitcoin colon silent address with no fallback, and if you don't speak non-silent addresses you won't be able to donate. I was of the opinion that people probably actually want fallbacks, but you know whatever. So then, it would be Bitcoin colon existing address question mark SP equals silent payment thing. I am also pushing if you don't want to fall back, that's okay, but it will be Bitcoin colon question mark SP equals. So, just nothing in the body. And also pushing that as a general ‘this is how we should do new address formats’ period because when you think about Taproot rollout and stuff, it's kind of annoying that I actually can't specify Taproot with this SegWit fallback. Like, I shouldn't be able to specify that. So, there's a whole new BIP to replace BIP 21 that basically is just BIP 21 copied and pasted that says if you add a new address format, put it in the query parameters, and by the way, if there's nobody, you should be willing to accept that.

Speaker 2: Gotcha. Okay. Cool. Thanks for answering those questions. We're trying to catch up between the world and our stuff. 

Speaker 1: Yeah. We've been looking at trying to implement at least paying to silent addresses. It's kind of a pain because we're all PSPT-based, and that's still a little bit hand wavy. So, I didn't really want to roll our own thing and then go: ‘Oh, but we differentiated from where the spec works.’

Speaker 2: Yeah, I think we had a Delving post. They're trying to hash out whatever that would look like.

Speaker 3: Yeah, I think that BDK is kind of blocked on that too.

Speaker 1: Yeah, I pointed to [redacted]: ‘Can you review this so that they're going the right direction?’ They said: ‘Yeah. Well, okay. We actually disagree with some of that.’ So, there's a whole debate going on over there, and I'm just sitting on the sidelines. But I think it was the Stephen LeVere podcast, they went on — [redacted] and whoever else went on — and basically, they were saying the most important thing is to be able to pay to those addresses. I kind of agree because if everyone can pay to them, then it certainly speeds it all out. So, that'd be kind of cool.

Speaker 2: Taproot stuff. Same, same. Cool. Moving on. I think we have the PR for that bug fix thing I mentioned. I don't remember the last — [redacted] talked about Eclair got pretty close. I don't know if there are any updates there. 

Speaker 0: [redacted] has put up some PRs that are in draft. I think they have something that...

Speaker 2: Oh. Y'all were doing the splicing thing, right? To add the splicing.

Speaker 0: Yeah, exactly. That's one of the potential issues. They are trying to write the addition to your BOLT PR that adds the splicing stuff. I think everything is going okay. Just needs a bit more time.

Speaker 2: Okay. Cool. Gossip stuff. I think we're starting to gear up in review mode on this end. Given again to the last major release, that's where generally —  I think [redacted] went through a lot of the comments. Like, [redacted] had a whole diff they put there. I think that's incorporated now. I need to reload this context into myself.

Speaker 1: Yeah. Me too.

Speaker 3: Yeah, I should probably take a look at it. Somebody from our team can take a look at it. We've been getting more and more cases of things that look like gossip problems. It seems like over the last six months or so, the frequency of things that look like gossip just didn't propagate has gone up substantially. So, this plus minisketch, got to make progress there.

Speaker 1: That'll give us something to discuss in September as well. In case you get bored.

Speaker 2: Channel jamming stuff. I'm not sure.

Speaker 6: Not much there. I've been out for a bit, and catching up since. I am just waiting to hear from [redacted] on the bLIP. But other than that, nothing blocking.

Speaker 0: On our side, [redacted] has been working on that a lot recently, so I think we should be able to make progress by just discussing directly on the bLIP and getting things deployed.

Speaker 6: Okay, great. Sounds good.

Speaker 2: Cool. Async payment stuff?

Speaker 7: No updates. Still landing PRs in LDK, although kind of slowed down by the release right now. 

Speaker 0: I am actually working on the Trampoline part to make sure that we have a fully specified version of Trampoline to blinded paths and Trampoline to blinded paths with a Trampoline onion for the recipient where you can put keys and TLVs. I should have that by the end of this week or next week so that you are unblocked on that one.

Speaker 7: Okay, awesome. I'm looking forward to taking a look at that.

Speaker 0: Cool.

Speaker 2: There's the new splicing PR, 1160. Relatively new.

Speaker 0: Last time, I promised [redacted] that they would have a PR of using the official values, but Trampoline got in the way. So, this is going to be for the next time. After I get done with Trampoline and the final things for BOLT 12.

Speaker 8: Okay. Yes, I was going to ask about it. When you make it, can you just tag my GitHub on there so I see it? 

Speaker 0: Yeah.

Speaker 8: Sweet. Thanks. 

Speaker 2: By official values, you mean like the official TLV values basically, right? Like, you're using some other numbers, not using the ones in the spec?

Speaker 0: Yeah, exactly. The ones we're using are not exactly the ones from the spec, so I need to make some updates.

Speaker 2: Okay. Cool. Dynamic commitment. I remember last time, we started moving forward as far as separating the kickoff on the fly thing versus the base version, and moving forward with the base version. I think there are questions around: ‘Should it be a different PR? Should it be a different document or commit?’ I'm not sure if there's anything to add there, [redacted].

Speaker 5: From what I remember, it seems like the consensus opinion is that it should be separate documents so that they can be implemented independently, and we can get interop independently. Whether or not they use the same negotiation mechanism, I don't remember people planning too much on. I think our plan right now is to use the same negotiation mechanism as we implemented in LND. But if people get around to it and actually decide that they want to do the virtual outpoints and they want a different negotiation mechanism, we can always decide to do it. We can update that spec as people find interop, and we kind of butt heads over how that should be done. But in the meantime...

Speaker 2: What do you mean by virtual outpoint?

Speaker 5: I just mean like the kickoff stuff.

Speaker 2: Ah, okay.

Speaker 5: I guess what it is, right? It's like you have a virtual...

Speaker 2: Sure. Yeah Cool. Okay. I definitely have some PRs to catch up with you guys there.

Speaker 5: It's almost like — I don't know. I'm trying to come up with names that actually provide some sort of intuition. I think the closest thing I can think of is that it's a dynamically linked out point. Same way that we have like DLL, like dynamically linked libraries. 

Speaker 1: And they never caused any problems at all. 

Speaker 5: Never. No security problem has ever been caused by this. I think good things can happen, guys. I assure you.

Speaker 3: Cool, okay. Thanks for the update. Liquidity ad stuff. So, I started to catch up a little bit, at least just with [redacted]’s' bLIP spree, as far as how they all combine together. I think I see the grand vision now, which is cool. I haven't gotten into all the details, but I think it's cool just to have all this stuff laid out in a way that people can implement themselves as well.

Speaker 0: I have a few questions where I need feedback on the liquidity ads part. So, there are a few dimensions that need extension. The one I think that is really useful is how you pay the fee. That's why I introduced a payment type that can be specified and extended, where you either directly pay during the interactive TX session or you can introduce other ways of paying by deducting the fees from future HTLCs. Another thing that we discussed recently with [redacted] is what is the fee? Right now, the only fee I’ll owe is something that is computed based on the funding weight that you refund. A fee base and a fee proportional on the amount. But do we also want to have a fee that would be — a subscription fee, for example — where you say you would pay some amount regularly? Is this something we want to invest into right now in the base version or do we want to just leave it open to be able to extend it? Because it's quite hard to reconcile with this flat fee that you pay only once. It's really a different format of data, basically, of negotiation. So I think it should really just be maybe in the same field, but that is abstract and could be either this flat fee or a regular fee, but I don't see how I can make both of those fit in the same data structure. The last thing is whether we want to change these parameters. For example, right now, there's no duration. Nothing. It's the simplest you could imagine. So it's different from the original one that these are put up where there's a list duration and there's a commitment also on the routing fees. So I left that you can potentially extend this and change that. Do we want to have that opportunity to potentially change that? Or do we not care for now and use, in the future, completely different TLVs if we want to introduce duration-based liquidity ads? I'm not sure.

Speaker 2: But by change, do you mean it's not specified at all right now and you assume some hard-coded value?

Speaker 0: For which one?

Speaker 2: For the least duration thing.

Speaker 0: Yeah. Right now, you buy that amount; there's no duration attached.

Speaker 2: Ah, I see.

Speaker 1: Yeah. There's a whole heap of things here. One is like in practice, you want to guarantee some minimum. But beyond that, it's like: ‘Well, if I'm making money off you, I'm obviously going to keep it open.’ So, there's sort of an implied momentum there. But there should be some minimum commitment, at least nominal. But the marketplace is more efficient if that is a fixed value, to be honest. Otherwise, it gets really hard to compare. Liquidity is everything, right? You want to have a lot of different things that you can just look at and simply compare and go: ‘That's the best.’ I mean, you still have to tweak the fact that: “Oh. Well, this provider is better than that provider.’ But at least you can compare the prices. Whereas the more variables you introduce, they're like: ‘Oh, but they're offering me a one-month lease, and they're offering me a one-week lease.’ I think, pick a number.

Speaker 0: Yeah, but we said that we cannot really enforce it.

Speaker 1: No, you can't enforce it. But it kind of sets an expectation, right? You would have more insight into it than me of what's a good number. But I think from a user point of view, a week is probably not enough and a month is probably about right. I mean, if you say: ‘Look, we will hold this channel open for a month for you and then, we'll figure out what's going on.’ That sounds fair. Like, that's something worth paying for. Whereas if you did it for a week, I'm like: ‘Really? That's not very long.’ And longer than that is too far in the future.

Speaker 0: Should we have a mechanism to enforce that or should it just be a recommendation in spec saying: ‘If someone buys that amount from you, you should keep that channel open for a month at least.’ What should we do? 

Speaker 1: I think so.

Speaker 0: Yeah? Just a recommendation in spec and saying that this is what people expect and that people would just flag you as a bad liquidity provider if you don't do that. I would love that because I think it's enough.

Speaker 2: Yeah. I think [redacted] and I are on different sides of this. To me, I like the ‘let's enforce as much as possible,’ but they bring up the whole issue around having heterogeneous leases and splicing with that as well. It definitely does complicate that, and that's as far as doing more on the script level. If it's a service level thing, then, you just have that agreement and then you don't really need to modify that stuff. But if you do want a script level one — for example, you had one for six months and then you add one, now that one's five months — are you partitioning the output balances there? Definitely gets a little more hairy, but I'm into the output.

Speaker 0: Yeah, it's a nightmare to implement, so. Have fun implementing that and come back when you've implemented it. Then, we’ll discuss it again.

Speaker 1: Yeah, we hacked the CSV delay in the original one so that you had to keep updating it because your CSV delay is relative, right? And so, you had to reconnect. You had to kind of agree to shorten it as blocks went up. But that way, instead of the CSV one, you had to see CSV N, and that was simple. But it did mean that if I haven't spoken to you for two weeks, now you're a month from now and not a month from when you started. At what point do I just give up? Like, if I wait for the full month, then I've got to wait another month because you've never spoken to me, and we've never agreed on an update. So, it's kind of mechanically messy that way. By not guaranteeing, you kind of sidestep that whole problem. But I just do think from a market point of view, just say one month. At least,it's for a month. Beyond that is implementation defined. If later on we want to add a monthly lease rate or something — but there's a lot of design space there too. Like, do you go: ‘Well, we've gained this much in fees from you, so we're gonna discount what — you have to pay the Delta.’ How does that work? Or do you just go — I mean, is it even worth it at that point, right? Do you just go: ‘No, if you're not worth it. We're just going to close the channel with you. Goodbye.’

Speaker 2: Yeah. For example, we did a CLTV thing, but then, [redacted] analyzed that. That works if you're mostly a net receiver. Once you start to do rebalancing or forwarding, it gets kind of weird because funds that you got elsewhere are now in the lease that you wanted towards them. So, if you have  sort of a directed graph model, that makes more sense. But if things are going in both ways, the bookkeeping is difficult basically. Which is like: What's the best argument then?

Speaker 0: But regarding what you mentioned [redacted], I think it's really easy with what is currently spec because you also send your rates in init. You can customize them to each peer. If you see that the peer is a good peer, you're gonna send them smaller rates in init than what you advertise in your online announcement, which implicitly tells them that they are a good peer and you're ready to sell them liquidity for a cheaper price.

Speaker 1: No, you're not because they won't find you. I mean, if they connect to you and ask, that's because they're prepared to pay the amount you advertise. Why would you give them a discount at that point?

Speaker 0: No. I mean, someone that already bought the channel from you and you are telling them your lease for splices for additional liquidity that they would rebuy, but they also already have a channel with you.

Speaker 1: That is true. You could basically use that as a ‘here's your rate.’ That's possible.

Speaker 3: I didn't want to interrupt this conversation too much, but to go back to your earlier point, [redacted], you were like: ‘We shouldn't have more parameters because it makes the market less efficient.’ I agree with you, but at the same time, the ability to say: ‘I'm going to rent liquidity to you at an amount per time’ rather than — I think there's some flexibility that needs to exist, not just for the market — like, I'm a routing node. I want to buy some liquidity or whatever — but also for end consumers because that difference in user experience between upfront fee and fee over the course of the next n payments is pretty huge. I think that's going to make a big difference in the UX people ultimately receive, and those people are really going to want to play with that number. In fact, we've already seen LSPs want to play with that number.

Speaker 1: Yeah, but I was more talking about the duration. If we can have a fixed duration that everyone agrees a month is a reasonable unit of time, that's simplified. It avoids a whole other axis of complexity.

Speaker 3: Yeah, the duration is fine. I don't have an opinion on it.

Speaker 5: This is why in derivatives markets, they fix the strikes at a certain interval because otherwise, you can't even have an order book with comparable products.

Speaker 2: The other argument there is also concentrating on liquidity, for example. Because we added other markets. We have the two-week, the three-month, the six-month, and the year. No one used anything, but the two weeks basically. And then, you're fragmenting it across all those other buckets as well. You could combine them and blah-blah-blah, but it definitely just makes that problem easier as far as satisfying that.

Speaker 1: I mean, I think that the eventual future of this is basically it's all automated, and your node just picks something based on heuristics. That just gets a lot easier if you've got fewer variables, right? I mean, it still has to judge: ‘Oh, you're a more reliable node. You're bigger, whatever.’ But the fewer variables we can introduce there, it's just better all across the board. So, I would rather pick some things and extend it later if we need to subdivide markets. But the other thing is that people adapt, right? So, if you just give fixed parameters, they work around it pretty well. Because we're guessing at the moment, so, but that's OK.

Speaker 4: But I think per your point, [redacted], if liquidity is everything, once the liquidity gets to a certain threshold and beyond, then you can subdivide the market. The drop in efficiency is not because the reason we care about efficiency is because of the liquidity of the market. So once the liquidity expands to that point, it's like we can afford the loss of efficiency because the liquidity at each market interval is going to be good enough. So I think…

Speaker 1: Also, there's usually demand at that point.  People like ‘No, I really need two weeks’ or ‘I really need a year’ — whatever it is. There's some reason that people are screaming for it. Then, go for it.

Speaker 0: Okay. So based on that feedback, I think that I will remove the potential extension on the lease type and keep it fixed to a month with that recommendation. The things that you can change...

Speaker 2: Do you have a handy link to where that is right now, [redacted]?

Speaker 0: Yeah, it's in the latest liquidity ads PR, 1153. So the two parts that will be open for extensions are the payment types — how you pay that fee? —  and the fee amount — what is that fee right now? So, I will add the possibility to add that fee is a monthly subscription. Something like that.

Speaker 2: What's the name of the field that talks about duration? If I can CTRL+F for that.

Speaker 0: There's none right now. I wanted to, but right now, I left it open so that there's this abstract thing that is called the lease type. The only lease type that exists is one that doesn't have a duration, but you could add a new lease type that has a duration.

Speaker 2: Ah, I see. Basic funding lease.

Speaker 0: Potential opportunity to extend this at all. The only lease time you will have, it will be this one with no duration that you could set and the spec tells you that you should own all this for a month, and then you'll see.

Speaker 2: I guess either way it's a TLV somewhere in it, right?

Speaker 0: Yeah, so we could always introduce more in the future by using a different TLV. If we think that was a bad idea. We'll see. So, I will slightly rework the data structures used by liquidity ads to take that into account. Also, one of the things I want to remove is right now, there's this lease witness thing. This kind of a witness that the seller gives the buyer just to have some proof that they bought liquidity, but it's kind of weird here because there's no fixed duration in the script. I'm not sure what to do with that one. I think that since you have a signed channel that is enough already. I don't think there's a need for a dedicated field for that. So, I'm inclined to just remove this lease witness thing.

Speaker 2: Oh. This is the signed lease version. Is this what you're talking about? Where you basically commit to what the lease is? The problem is there's no way of tying that to your channel. So someone can say: ‘Hey, they sent me this,’ but there's no way to prove that it was the channel that you actually had.

Speaker 0: But I think it does because you could just store the open channel and accept channel messages. That contains the TLVs for the lease details, and that contains the final ID and the pubkey. So that directly maps to the funding script. I think if you just saw open channel and accept channel, you have enough proof that the seller agreed to sell you this amount of liquidity. So, I don't think we need to add anything more.

Speaker 1: Okay. As long as the commitment chain is intact, that's good.

Speaker 0: Yeah. Okay. I'll spell that out in more detail in the PR.

Speaker 5: Is there sensitive information in the open and accept channel? Like, MuSIG stuff for Taproot? I can't remember.

Speaker 0: There should be nonces, I think, for Taproot. But public nonces. Individual nonces.

Speaker 5: Yeah, so that gets tricky, right?

Speaker 0: Yeah, But then in that proof, that's just — okay. I'll think about it. I'll think about it more.

Speaker 5: Because I haven't totally tracked 100% of this, but I think the goal of this is that once you have that signed commitment to the lease duration, then that paired with an actual mined transaction that may close the channel can be used to be gossiped around to be like:  ‘These people are frauds’ — right?  And we don't want people to be leaking sensitive information in that process. Now, granted, if the channel's already closed, then maybe the MuSIG descriptors that are in the open and accept messages are no longer relevant, because I don't think they're sensitive. I think their sensitivity is ephemeral.


[Error in video. Transcript cut off.]

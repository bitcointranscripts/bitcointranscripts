---
title: Lightning Specification Meeting - Agenda 1118
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-11-20
---

Agenda: <https://github.com/lightning/bolts/issues/1118>

Speaker 0: We won't have posting for the mailing list anymore in one month and a half, so we should probably do something. My plan was to just wait to see what bitcoin-dev would do and do the same thing. Does someone have opinions on that or an idea on what we should do?

Speaker 1: Who's managing the email account for the lightning-dev mailing list? You, [Redacted]?

Speaker 0:I think it's mostly [Redacted] that has the main admin rights or is it someone else? [Redacted], do you know?

Speaker 2: Yeah, there is no such thing as main admin rights. There is one username and password, and like five people have it. The admin panel is kind of sketchy. I think either [Redacted] or [Redacted] were the point of contact with the Linux Foundation.

Speaker 0: Yeah, so I guess we should mostly do exactly what bitcoin-dev does and just follow what they do. Let's just wait for that one.

Speaker 3: It doesn't really seem like a decision is forthcoming. I haven't totally kept up, but I'm not sure we're going to have a decision by the 1st of January from the Bitcoin mailing list  folks. 

Speaker 2: Yeah, I think part of the problem is there's no good option. There's no real option at all, I think, so they haven't been quick to do anything. Like [Redacted] noted, bitcoin-dev might just do nothing and leave it for people to do whatever. Like, there's this forum thing that [Redacted] is running called Delving Bitcoin. So maybe they'll just not have a mailing list. I mean, part of the question is: Do we even want a mailing list? Can we survive with GitHub?

Speaker 4: I actually do wonder if GitHub is sufficient. Like, we already do all the bolt stuff in there with the discussions feature. Like, I actually do wonder if we could do it. I mean, obviously, there's the centralization issue, but I don't know if that ends up being material for the time being.

Speaker 2: Yeah, we just use GitHub discussions for anything that someone would post on a mailing list. I don't think you can reply to GitHub things via email anymore. You used to be able to, but I think they disabled it.

Speaker 5: Well, we use Google groups for some stuff. I know some people don’t like Google, but it works. It's worked for a long time, and Google uses it internally. Maybe that means that they won't turn it off.

Speaker 2: Yeah, I think that's the only other option really.

Speaker 5: But so what's the current state of things?  ‘Cause I feel like the mailing list seemed like it was imminent, but there's not really a clear timeline. How much time do we actually have to figure out a new solution?

Speaker 0: By the end of year.

Speaker 5: End of year, okay. Well, there’s more time, but yeah. Still coming up.

Speaker 6: So if someone could run a forum, why can't they run a mailing list?

Speaker 5: Supposedly, the software is hard to run, and I think [Redacted]’s the only person here that actually knows how email works.

Speaker 2: I don't think it would be that hard. Anything with email, you're constantly fighting a battle with spam classifiers and whether your email gets marked as spam. If we're a small group and we just say: If it's going to spam, it's your fault, not the mailing list's fault — it wouldn't be hard to run. But that tends to be the issue with it.

Speaker 1: I would definitely prefer the mailing list because I have a lot of folks who are still reading this stuff. So, it looks like they're more Bitcoin-like. I think I would miss something if we would get rid of the mailing list.

Speaker 5: Yeah. I think the latest email flurry showed that a lot of people lurk and read the mailing list, right? These random people who plus one. So there is that aspect. But if it is Google Groups, it's not super hard to set up. The main thing is just giving whoever admin permissions. For example, the LND mailing list, our mailing list, is run with that. It's like: Yeah, right here. Some people have probably seen it. Not too much activity, but it works and importantly, you can keep using an email. You'll also have the UI, which is probably a little bit easier to use than the Linux Foundation UI thingy as well.

Speaker 2: The only issue I've had with Google Groups in the past is it has issues letting you subscribe without a Google account, or at least it did many years ago. I don't know if that's still the case. Can you just go on there and say: My email is x; please subscribe me and let me post without having a Google account tied to it?

Speaker 5: That's a good question. I remember some people asked that for us when we started making the mailing list or are they only mailing us on groups? That is a really good question. ‘Cause I just went in incognito and there's a sign in button, but that obviously just goes to sign in with Google. That is a good question.

Speaker 2: That would be pretty frustrating.

Speaker 5: Yeah.

Speaker 2: Even just for me, I use a different email account than is on my Google account. So that would be pretty frustrating.

Speaker 5: Yeah, I know there's a lot of part-time mailers on the mailing list, too.

Speaker 6: I think you need an account, but it doesn't have to be a Gmail account. You just sign up with whatever email.

Speaker 2: Right. You have to create a Google account with your given email. Google will fraud mark your account and disable your account too though if you don't. I don't know if they would do it for this kind of user, but they have aggressive stuff on that too.

Speaker 5: Okay. Well, I can note down to look into that. At least, in terms of options that we have.

Speaker 2: Yeah, if you could look into that. I think, basically, that leaves three options: get up discussions Google groups; host a forum, like what [Redacted] does the Delving Bitcoin thing — we could use Delving Bitcoin, host our own forum; or I could set something up, but that would take some amount of effort. So, I think at some point, we vote. Maybe next week, we vote or something. Or maybe we create a GitHub issue and/or send an email on the existing list: list those options and then vote.

Speaker 0: Sounds good.

Speaker 5: Okay, alright. We're done with the options. Do people know what bitcoin-dev is going to do? There's a lot of spam on the email list, but there's a clear direction from that. 

Speaker 2: Unclear. It seems like maybe they'll do nothing and use Delving Bitcoin.

Speaker 5: Interesting. Okay. I mean, this course isn't bad. You have markdown and other stuff available, so there's that. I'm not sure how backups work or anything like that though. Nor if you need to have a paid account. I'm pretty sure it's all open source. Okay, alright. Should we go from the top?

Speaker 0: Yeah, so dual funding. There's been only a few minor comments since the last meeting. I think [Redacted] pushed changes to address those, so I guess it just needs the last round of review and should be okay. [Redacted], is there anything you want to add about that or specific things you want feedback on?

Speaker 7: No, I think we're pretty good to go. I pushed the last round of white space changes this morning. There's been some great feedback, so thanks to everyone who's already taken the time to leave comments, et cetera. Yeah, I don't have anything else. I don't know.

Speaker 0: This is just happening. 

Speaker 7: Yay! Yeah. What are the next steps for getting it acked, [Redacted]?

Speaker 0: Yeah, I think I'll review it to see the last commits you added and see if I can suggest some things for the outstanding issues. I think [Redacted] had a few issues you said, so let's see if we can rewrite some things to make them happy. Then, once we are okay with that, we have cross-compat test that work across everything. So, I guess we should merge.

Speaker 5: By the way, do you know if [Redacted] can join this meeting schedule wise? I think they know about it vaguely or secondhand, they see the issues right? Maybe they’re not available? I guess we can try to reach out to them on that.

Speaker 0: Yeah, it's a good point. We should tell them to join since they’ve been reviewing a lot of spec stuff.

Speaker 5: Yeah, I would imagine.

Speaker 0: Right, So I guess that's it on dual funding, and I put up liquidity ads because [Redacted] made a lot of changes and improvements to it. So [Redacted], if you want to describe what's happening and what changed?

Speaker 7: Yeah, definitely. So, I just sent out a mailing list post to lightning-dev. It probably hasn't worked its way to the moderator stuff, but it'll probably come out in a day or two, which also will contain all this stuff, but in written format, if that makes sense. But just verbally — it's in draft; I haven't implemented it yet. Some of the biggest changes that we're moving from: originally, we were using CSV locks, now we're proposing using CLTVs. We're also moving to the previous version of it — proposed having a fixed size of leases. They weren't negotiable; it was always gonna be about 4,000 blocks, which is a month. The new proposal lets you kind of propose into what block you would want your lease to end. What's cool then is we can use that and we put it as the CLTV and all of the outputs for the person that's basically lending the money. We call them the leaser. So, one of the things about moving to a CLTV lock, they're kind of — one of the things you're basically trying to do, like in the protocol spec for a lease, is make it such that the person leasing the money can't close the channel to chain and get their funds back and release it out to someone else because that would not be very useful for you as someone who paid for that service of having that liquidity available. So, the way that we kind of incentivize the lease, or to keep the channel open and keep their funds available for routing, is to add that time lock onto their funds in the commitment outputs, such that they're not able to get them out on chain until the lease would have ended anyways. One of the tricks with the CLTV, it's easy — straightforward — to add a CLTV lock clause to most of the outputs where the leaser gets their money back, except in one case, which is where it's on the lease ease commitment transaction for HTLCs that would go back to the leaser. So, if they're able to induce the person that leased the channel to close it, and they have money in an HTLC, those HTLCs will be available to them whenever that HTLC's fund condition is met, either timeout or in success. So I'm able to prevent them from being able to basically send HTLCs to the other side, lock them up, get the peer to force close the channel and then have them claim them back after that time lock. There's really two options. One, you could extend those time locks to be at least the minimum of the CLTV lock. This is kind of problematic because it adds a bunch of time to any routed payments, which I think is pretty undesirable, especially if someone for some reason — you can pick how long your lease is. You could do a five year, a 30 year lease. I don't know. Like a UST treasury bond. I don't think you'd want to. I don't recommend that. But then, having a payment that won't get resolved for 30 years seems very problematic. The solution that we came up with, and I think actually [Redacted] made this recommendation in the original draft, is that we add the equivalent of an HTLC timeout transaction with the — basically, that's just like a second stage lock that has the final CLTV on it. This lets you have two CLTVs on it. One for the HTLC timeout, so that can be independent of what the lease is, and then, that final lease lock on the second stage transaction. It's considerably more complicated, but we kind of already have all the transaction on chain handling stuff. This would just be another case of looking for a different type of transaction, so I included it. I think it's the right thing to do in terms of walking down every avenue of getting your funds out in terms of griefing on the side of the leaser. But that's probably the biggest change.

Speaker 0: How would you exchange the signatures for that? Because this kind of breaks the usual symmetry between a local and remote commitment.

Speaker 7:  It does. Yes. Okay. This is a good point. I hadn't figured that out. It's a draft proposal. I hadn't implemented it, which I assume would bring these things up. You would have to send it with your commitment SIGs, right? So, let's just naively say a TLV and commit SIGs, where you now include any additional signatures for that second stage transaction.

Speaker 0: So this would create an issue with #483 current limit because then you could not reach that anymore. So you need to make sure that you adapt your limit. You lower them to take that into account.

Speaker 5: Good point. [Redacted], one question — I guess I don't understand the HTLC thing, and I think this is what we do — can't you just put a CLTV at the output of the second level HTLC? Or are you talking about the other party force closing?

Speaker 7: I'm talking about the other party force closing. So yes, on your commitment transaction, it's quite simple to add the additional clause, and that's in the proposal. So we do that. Every output of how the leasee can get their funds back is encumbered with the CLTV. The only exception is in the case where the peer force closes and their HTLC is there. Whatever the HTLC resolution clause on the other side of the channels, saying they could get them out. Problem is, like I said, naively, you’re just like: Okay, we'll just add the CLTV to that branch in the output. But again, maybe I'm wrong about this, but my understanding was that it would start having an impact on the timeout of any transactions sent to that channel, which seemed highly undesirable. Just on a whole.

Speaker 5: Yeah. Kind of going back to the other thing — I'm trying to remember what we do. I'd have to have to go look at the actual scripts.

Speaker 7: Yeah, that would be great. We'd love to get that out. Again, it's a draft. I haven't started implementing it. Part of it is because I wanted to have this conversation and get people to start thinking. Because if there's other ways to do it, it'd be great to get that out and figure it out. We were talking about this at the Core Lightning Hack Week two weeks ago. We spent a lot of time talking about liquidity ad stuff. Maybe we already talked about this in the last spec meeting. I apologize if we did. But one of the things that's interesting, and I think kind of a new and interesting research problem for liquidity ads, is that the signed commitment that you get for the cap on the channel fees that the leaser is going to commit to for the length of the lease basically creates the conditions — you have good conditions for like a fraud proof basically. So, you get a signed commitment from them for a set of blocks that they have a cap on what their channel fees will be for that liquidity. Then, if you get a signed channel update for them, which has a timestamp within that block thing — handwave about how we would exactly make sure that the timestamps within the block range. But ideally, you then have to sign messages that in theory, handwave using magic crypto, you could have some sort of fraud proof that you would be able to do some magic using script magic, which is beyond my understanding. I've talked to a few cryptographers about this problem, and they all agree that doing integer ranges in cryptographic-like proofs is quite difficult. So no one has a quick and easy solution. But I think there's a broad possibility that we would be able to do some sort of in channel commitment bond output for if your channel peer breaks their promise about channel fees, which is kind of interesting and definitely a new thing. I think I included it in my email as a kind of a passing comment. I might try and write up the problem a little more specifically and put it out on the general mailing list just as like a general thing that might be cool and interesting to solve if we get handwave covenants, et cetera. The cool thing is the protocol already, — well, it might need some tweaks depending on how you do the fraud proofs — in theory, includes a proof that you've broken your commitment, which is kind of cool. So we have two parts. It's just like: What do we do with them once you have the proof?

Speaker 5: So, are you saying something like a single show signature? Kind of like something where if they sign another version of it, you restrict the nonce? That kind of thing or something else?

Speaker 7: The problem is it's not like they're signing another version of a message. It's that they're signing a message whose contents have values greater than another message, right?

Speaker 5: Yeah, the restrictions on the attribute.

Speaker 7: Yeah, exactly. So they're well-structured messages. They're values, but it's values within a range and also like there's a couple ranges you need to check. It's like these values must be beneath this other rate, this committed range. Then, you also need the timestamp when it — I don't know. 

Speaker 5: Okay, that makes sense. One thing that occurred to me about the other thing — around kind of you getting the party to force close to get your money back sooner because maybe the CLTV is shorter than the release duration. I guess the one thing you can do there is at least modify the max in flight value so that controls the max that can be leaked via that vector. It's not perfect, but it mitigates. So if you have a few btc in the channel, maybe that means you can only get 100k out at once. But obviously, that has some trade-offs.

Speaker 7: Yep. Yeah. So, for the current proposal, I wrote it the strongest. I was like: This is probably the most ambitious in terms of protocol change. It's like: Okay, the current proposal is the strongest thing that we could get in the protocol in terms of keeping that lease. Whatever. If we think that that's too much work to add in that other layer of transactions, which is totally fine. That's kind of why I wanted to put it in the draft, so we could talk about it. I think you're exactly right, [Redacted]. Just having a recommendation to minimize the amount of HTLC in flight is basically the best you can do without that.

Speaker 5: Yeah. For people who are doing another layer of transactions, like the whole replacement thingy basically — if you want to go back to restricting that — that's a path to doing that as well. But like you're saying, that's more changes, but it's directionally similar.

Speaker 7: Wait, what's the replacement thing?

Speaker 5: Basically, the whole thing of if you're just saying that no party should be able to unilaterally spend an HTLC without going to the second level — which sounds like what you're saying somewhat — that would also because then, at that point, you would go backwards to that. But yeah, not that everything needs to be done at once, but just that it's in the same direction.

Speaker 7: Yeah, I think that's right. Maybe L2 fixes this. I don't know. Handwave. But yeah. Cool. Okay. I think that's everything I had about liquidity ads stuff. It's pretty cool. I'm excited about it.

Speaker 0: Yeah, there was one interesting thing to note. At some point, early on, when we started discussing liquidity ads, we thought we would need a lease renewal mechanism. Like, when you get close to the end of a lease, you say: Oh, please renew this liquidity ad. But we actually don't need that because it would just be a splice. It would just be exactly a splice with existing liquidity ad, so there's nothing to add and we already have that lease renewal mechanism built in.

Speaker 7: Yeah, that's a great point. I've already been talking to [Redacted] about how we can add it to splicing. I think the messages are basically the same. You don't have to do anything. That's pretty nice. Cool stuff. Alright. Yeah, that's everything I had right now.

Speaker 0: Perfect. So then, simplified middle-close — if someone worked on that since the last meeting. There are no changes on my side. It is just still implemented and waiting for compact tests.

Speaker 5: Cool. This is on my radar like I have a staging branch I'm working on this stuff in, and I think by the next meeting, I should have something that you should just interop basically.

Speaker 0: Cool. Perfect then. Ship it in two weeks.

Speaker 5: It sounds good to me. Like you were saying, the plan there is still just to have the official protocol taproot feature bit — some type of feature bit; just assume this — and then, I would update that. I guess we do a dependent, or make the bits dependent on each other, like what we do sometimes.

Speaker 0: Yeah, sounds good. Alright. Anything new in the spec clean-up path? I think there's nothing new in that one.

Speaker 5: Nothing new, but I think our plan still for 0.18, the next release, to basically have that, at least the required feature bit thing.  I think some people already have that master as well, so if some people deploy our master, I feel like it's not just breaking anything, essentially.

Speaker 0: Perfect. We haven't seen any issues on our side, so I think everything should just go smoothly. Alright. Anything new on the offers side? Bolt 12?

Speaker 6: Nothing new on the spec side. I think there's some conversation though on the Discord about a use case that's not covered there. It's point of sale and Twitter donations. I'm not sure if there's any thoughts around that. 

Speaker 5: There's something unique about that case. I thought donations were sort of the forefront.

Speaker 6: So I think, at least the point of sale part, was that you would have a — so you think of Square, right? They would have a terminal, which is not the wallet of the merchant, but needs to know about the sales and how essentially that is done in a sort of non-custodial sort of way. I don't know. You could review. I'm not sure if you're on the discord for the Bolt 12, but there's some discussions there about using onion messages. I think [Redacted]’s got some ideas that were promising.

Speaker 5: Ah, so it's basically about delegation. I mean, you need to delegate some privileges to the register or whatever.

Speaker 6: Kinda. I mean, basically, the terminal needs to know that the payment was made, but they're not being paid. 

Speaker 5: I see what you are saying. 

Speaker 6. So yeah. They could just put a nice green checkmark and the customer could get their item. They're not running out of the store saying they paid, but they're not sure; you know they really did, et cetera.

Speaker 5: So, it's like a general backend thing, but there's a protocol side. 

Speaker 6: Yeah.

Speaker 7: Do you guys have an issue or something you're tracking for that, [Redacted]?

Speaker 6: No, [Redacted] has brought it up on Discord, I think, on Thursday or Friday. So, there's nothing that we have open on it yet.

Speaker 7: Cool. Okay.

Speaker 6: Maybe we should make something though.

Speaker 0: Alright. Do you want to talk about the Bolt 12 lightning address post that I made or…? I don’t know if anyone has feedback on that. 

Speaker 5: Sure. 

Speaker 0. Basically, the idea was to remove the IP leaks that we make with the current lightning address protocol and see how we could use Bolt 12, especially the fact that we both know that you have this long lived offer and you just need a way to fetch that offer once. Then, you can keep it and only have to refresh it once in a while when it's close to expiry. Or sometimes, it won't expire, so it's even easier. Then, the invoices themselves will always be short-lived, so it changes a lot of things. You can actually use DNS quite heavily to be able to make that better. So, there are two ways you can use DNS. Either you have one DNS entry per user where you directly put the author, but it requires creating a lot of DNS records and maybe from an ops point of view it could be an issue, but that option is to directly map from DNS to an end user. What you can also do is, what I called option one in my gist, is that you just use DNS to map a domain to a node ID, and basically, you don't just put the node ID, but you put a blinded path to the LSP or domain owner node that is responsible for the users under this address domain. This lets the payer contact that node to then redirect to the final user and get a Bolt 12 offer from that user. So it's quite easy because on the provider side, it's really simple. You just have to create one DNS record with a blinded path to yourself, and in most cases, you won't even need to actually blind it. You don't care about hiding your node ID if you are a big provider like Breeze or someone else. You can also use it as a small community and hide your node ID, which is interesting as well, and then we use onion messages to be able to fetch the offer. It's like a pre-step, the way we do invoice requests. Here, this would be an offer request made to LSP that handles that end user.

Speaker 2: It's worth pointing out that one further feature is, even if you're using a custodial or non-custodial service, if you can get them to give you an offer, you can always put that in your own domain. So, even if you're using a different service, you can choose not to trust them and put it in your own domain with just adding one record, which is kind of cool too.

Speaker 0: Yeah, exactly.

Speaker 5: Can you talk about — I think it was in there — but how do you verify that the invoice is actually from the person you requested it from. Because I think that's an issue with the existing ones where people try to do the delegation, but the operator of the DNS servers can just swap out their own invoice. But I guess I missed something in that — like, there's like a layer of indirection, right? And the second option, the record has a blinded path to this node,  guess that's always online. Then, you can fetch it from them and they'll forward to the actual party, basically.

Speaker 0: Yeah, exactly. So, this is going to be trust on first use because if the only thing you have about the recipient is that address, then you have no way of verifying anything. But you can always get a signature from the LSP that they attest that the offer — they contacted that user and got the offer from that user — so that if they cheat, you have something that you can show the world. Or you need more than just the address. So, you'd need the recipient to display something else that would let you validate the node ID of the offer, for example, or something like that. But otherwise, it has to be trust on first use. Then, you can keep it and reuse it and you have no trust issues. Does that make sense? Does that answer your question?

Speaker 5: Yes, I think so.

Speaker 0: Yeah. If you're only starting with Bob at phoenix.co and nothing else, and you get an offer and you have no way of validating that this really matches Bob at phoenix.co unless you either add something else or get a proof from RNode — a signature from RNode attesting that we say that this does belong to Bob or to Bob at phoenix.co. If we lied, then you can show it to the world.

Speaker 5: Yeah because I guess the sender can't verify that Bob is actually in the blind of paths by construction, right? Because obviously, if that's not the case.

Speaker 0: Yeah because if the only thing you have is Bob at phoenix.com, you don't even have a node ID. You have nothing cryptographic that you can use to verify to do anything. So if you have only that, then there's not much you can do. But if you also display, for example, a verification code based on the node ID of the offer that the user can optionally verify after importing the contact, then you may have a way of verifying it before paying, which would be useful.

Speaker 5: Yeah. I guess you could use onion messages to sort of ping that, right? Once you have that information, you use the blinded paths to ping, and if they can sign with the pubkey, then that's good enough, right?

Speaker 2: That's also why I mentioned the cell phone domain thing. That lets you kind of sidestep this problem a little bit. At least for marginally advanced users who have their own domain.

Speaker 5: And that's because like you would get the provider to put a C name to your domain?

Speaker 2: No, you don't need anything. You just need to go in your UI in your wallet. Click: Give me an offer. Maybe you need a button that says: Give me an offer that doesn't expire. Then. you take that offer and you paste it into wherever your DNS is.

Speaker 5: I see what you're saying. That's just the short circuit. Okay, that makes sense too. Interesting.

Speaker 0: So, the goal is mostly to move away from the HTTP stack because the issue with an address is that the domain owner hosts just a file for each user, which means that the domain owner sees whenever who is paying who basically — the IP address of the sender and the recipient — which is an issue. This is something we can get rid of with that scheme because in the scheme I propose, the sender makes a DNS request to get the node ID associated with the domain, but the domain doesn't see the IP address of a sender anytime. They only see an onion message coming from them. So, they don't learn anything about the sender, which is what we want to preserve.

Speaker 1: But when they do the DNS request also over HTTP, they can't track the IP though or…?

Speaker 0: Yeah, but it's not made to the domain owner. That goes to DNS. Someone else manages those DNS servers, so they cannot mitigate it. 

Speaker 2: In the long term, we might even be able to get rid of the DNS request as well. As long as we require, which the current spec says you should, DNSSEC signing on the domain, you can actually serialize the full DNSSEC proof and put that in the node announcement. There's an RFC for this that describes how to do it. It's actually to put it in the TLS key. But as far as I'm aware, there's no open source software that actually implements this. So, once some software exists that implements this validation, we could just take those serialized proofs and put them in the node announcement and call it a day. Then, we're bootstrapping off DNS, but we never actually touch DNS during the normal flows.

Speaker 6: Would that be — that wouldn't work with unannounced nodes though, right?

Speaker 2: That would not work with unannounced nodes. That's correct, yeah. You might still have a fallback to do the thing where if a user adds it to their own domain with an offer. Yeah. there are issues there, but in the common case of an announced node, it's nice and easy.

Speaker 6: Gotcha.

Speaker 1: And I wonder currently: When I host this kind of domain or put this blinded path in the domain, how can I easily say: I don't use this anymore? And: How could I propagate this to all the other people who already fetched this thing prior to my change?

Speaker 0: You mean the offer. The thing you get is a Bolt 12 offer. So, at some point, it expires. Even if it doesn't expire at some point — if you make an invoice request to try to get an invoice for that offer and you get an error, or you cannot reach that node, then you're going to try to refresh by re-going through the steps of doing the DNS thing, and maybe you'll get a new offer or an error code saying that this user just doesn't exist anymore. Then, you'd have to contact the guy because if, for example, you move entirely and stop using that lighting address at all because you move to a different domain, then you're not going to be able to get anything. So, you're going to get an error and won't be able to fetch invoices and offers for that user. Alright. Let's move on to channel jamming. I know that [Redacted] wanted to talk about it again. I had been discussing it recently with [Redacted] as well because we have a PR that is waiting on the Eclair side, and we were wondering what the status of that was, and if it was worth moving ahead with it and deploying it on our node.

Speaker 3: Yeah. In New York, we spoke about how to move forward on reputation stuff. My takeaway was: On one hand, looking at mainnet data collection, and on the other hand, working on some simulations, which I'm busy doing. I just wanted to check in on the feasibility of deploying an experimental feature bit to mainnet because I've written some data collection stuff for LND, but without that endorsement signal, we're kind of missing a key piece of the puzzle, so the data gathering isn't really that useful. So, I guess the question is: Would we be happy to, number one, relay this value in the network even though we know it's experimental, so just copy it — like, if you receive it, you copy it even if you're not implementing any of this jamming experimental stuff. And number two, to actually start setting it with some very low probability to begin with, but for 10% of payments, start setting this value. Because that would get this value moving through the network and make any experimental thing we do more representative. Because if we don't do that, then a few people setting this bit, it's just going to immediately be dropped afterwards.

Speaker 0: I think I don't have anything against it. I think I would definitely follow all those things and make that by default in Eclair.

Speaker 5: Yeah, I guess the only thing is just you can just say: Feature bits already give away who's running the latest stuff; and this would give you something like that. But it's not really giving you critical information to say: Come attack me or something. So, I'm just doing this.

Speaker 0: We already did that. The activity is already a good fingerprint.

Speaker 2: Yeah. We can also consider flagging this because it would also indicate whether this payment was routed through someone who supports this. So, we might also consider shipping software, and then having code that just says: On this date, at this time, turn it on. Or maybe if you restart after this date, at this time, turn it on or something?

Speaker 5: Yeah, I think that would make sense. I don't have any major qualms against this. I think [Redacted] already implemented it, at least for LND. I guess it's just a matter of whatever this flag day is. Our next major release is February maybe or something like that. That's when we would, at least, be able to hard code the flag date into the release or whatever.

Speaker 3: Okay, That's great to hear, and then on the sender side, just do a flag day for both. On this magical day, we will both start setting this — sometimes as a sender, obviously not all the time  — and if we're relaying, we'll start to copy whatever value it receives.

Speaker 1: Yep.

Speaker 0: Sounds good.

Speaker 3: Cool. Great. I'll write that down somewhere. Think of it and just write up short instructions for that intermediate step of copying the values you get and setting it: not always. So you don't leak the good standard. But yeah, that sounds good.

Speaker 5: I have one question, I guess, as far as the balance of the experiment. So, let's say we're doing this and people are saying it: Is there something we're looking for? Is it just testing the code path all the way through? Or is there some other information that we can obtain from the experiment that is useful for future development or research?

Speaker 3: Yeah. The idea of having everyone relay it is then individual nodes can run a more complete experiment and really gain much more information than we have right now. So once everyone's relaying — like I actually sent on the LND mailing list today: a data collection thing using [Redacted]’s tool, Circuit Breaker — the idea is once we have this field, we can actually run the entire reputation algorithm, completely dry run, so that we can really understand how it would behave because it's very difficult to get a real sense of how this thing would happen in the real world network, right? So you run this thing; it just logs exactly what it's going to do; and then, we can take a look and kind of inform the specification from what we see there.

Speaker 5:That makes a lot of sense.

Speaker 0: Alright.

Speaker 3: Yeah, thanks. That's all I had.

Speaker 0: Let's do that. I don't think there's anything new on the quiescence unless someone did anything since the last meeting. But I see that there was an update on the dynamic commitment proposal by [Redacted], so maybe that's something we'd want to cover.

Speaker 5: Yeah. So we started to implement at least the mechanics for questions, so not the message yet, but just figuring out how to stop it reading racially and restarting and stuff like that. I don't know if you have more direct stuff on that, [Redacted].

Speaker 4: Yeah. With respect to quiescence, actually it's interesting that you say this because the reason that I did push up commits to the dynamic commitments proposal this time was per a suggestion of what to look into, [Redacted], you made last time. You basically said it'd be really nice to build dynamic commitments on top of quiescence rather than having a different flushing mechanic. Can we do this with live HTLCs? So I did go and look, and it turns out that we can by using [Redacted]’s suggestion, where we don't make it such that the new channel parameter is really — they're not about constraining the state of the commitment transaction, but they constrain the target state of any update ads. So, if we lower the max value in-flight HTLC number or lower the max accepted HTLCs number, then if those new lowered thresholds would cause an invalid state, that's fine. But then new ads will not succeed until the fulfills or fails have freed up the room for it. So I went in there and put an appendix in, basically about dropping this flushing requirement where we flush HTLC states similar to the way that we do shutdown, and I believe that we can do it. So really, the original idea for not doing it that way was going to be that it would be easier. But from the discussion that we had last time, it sounds like from your perspective and from [Redacted]’s perspective, it sounded more attractive to try to do this without actually flushing HTLC state, even just from an implementation perspective. So far, looking into the actual spec side of that, I don't think that we're going to have any issues. The one thing that we might have issues with is: I don't think it would be possible to convert to a as-of-yet designed PTLC style channel type while there were HTLCs on the link. I don't think that we have to think about that really? I think that that's a bridge that we can cross when we get there because…

Speaker 2: Why would that be impossible?

Speaker 4: Well maybe this reveals my lack of understanding of PTLCs, but how would you convert the HTLCs? Would PTLCs be like also on the same link as HTLCs or would you convert the HTLCs?

Speaker 2: Yeah, I can't imagine we'd play a PTLC supporting channel that didn't also support HTLCs. Otherwise, we'd fork the network, right?

Speaker 5: Yeah, it'd be combined. So I think you're right, [Redacted], in that you can't translate it. You can't take HTLC and make it a PTLC. You would just leave that as an HTLC. 

Speaker 4: Got it. Yeah, so my imagination is that it would be PTLCs only. So if that was never in the cards, then yeah, this won't be a problem.

Speaker 5: Okay, cool. Yeah, I'm envisioning that we'll have the feature a bit and for a while, we do both. Then, similar to when we made the legacy onion deprecated, we'll do that and switch over. But once we know senders are updated, how will we figure that out?

Speaker 0: So, it’s basically the sender's decision. The sender decides whether they use PTLCs or not depending on whether the full path supports it. So in your commitment, you're going to have a mix of HTLCs and PTLCs depending on who's the sender — which kind of reveals some stuff, but you can enforce senders to update to PTLCs and you can enforce all the nodes in the network to be at once. So, it will be a slow rollover where the portion of PTLCs will eventually win against the portion of HTLCs. Then at that point, we can maybe disable HTLCs.

Speaker 2: That may be another thing that we might consider flagging.

Speaker 0: Yeah.

Speaker 4: So, given all of that, from my perspective, it turns out we can build dynamic commitments on top of STFU, and we don't actually have to flush HTLC state. 

Speaker 0: Perfect.

Speaker 4: Yeah, as long as the only requirement really is that we are okay with the fact that the parameters don't necessarily apply as a constraint on the state as much as a gateway on the ad.

Speaker 5: Ah. So basically you mean like the next signature.

Speaker 0: It's already the case for the channel reserve, for example, where you start with the reserve. So, we already have that in our checks — that everything happens at HTLC time. So I think it will just work out okay in practice. So, I don't think it needs any complex change to make it work. 

Speaker 4: Cool. I'm gonna then rework the proposal to design around that. Maybe I should email [Redacted] or something and get an agreement there. But if you have that... 

Speaker 5: For the change to STFU?

Speaker 4: Well, and removing the requirement to flush from the dynamic commitments.

Speaker 5: Gotcha. The first one, I think the PR was pretty light. We seem to have on board with it at a high level. What's the PR number? I tried to search STFU and nothing came up.

Speaker 0: For quiescence or dynamic commitments?

Speaker 5: I think the issue is I can't spell quiescence. Oh, I did it right in the first try, actually. Okay, sorry.

Speaker 0: It takes nine. It should be over.

Speaker 5: Yeah, I got it. Okay, cool. Yeah because the actual diff right now is a new section. So, it's not super tangled up, at least. But I guess you could stage the changes against that, [Redacted], and either try to PR to [Redacted]’s thing or make a new one. I'm not sure.

Speaker 4: I think I would stage it against it. I wouldn't want to make dynamic commitments part of the STFU.

Speaker 5: Oh, yeah. I mean just the STFU changes or the qualification.

Speaker 4: Got it.

Speaker 0: Next up is taproot. I don't know if there's anything new on the taproot side.

Speaker 5: I have the script changes locally, but I sort of switched off to do the co-op close thing, just to kind of get that stable. Other than that, I mentioned last time we fixed a bug related to nonce exchange after channel reestablish, and I think I'll try to make sure that's clearer on the spec side as well. Just that in a certain state when you need to send both funding lock and channel re-establish, you need to, basically, handle that and ensure the nonces are the same. That's a minor thing. But so far, haven't had any other big stuff with that. I guess if we're on taproot stuff, we made some more progress on the gossip side of stuff. Just as far as getting the sort of changes through the code base. I think [Redacted] was close to having just the new channel only working, and I think the thing we took a back on is to what degree we want to support reannouncing old channels, nothing with timestamp versus blocks, and things like that. But at least, we'll work on the new pipeline and then we'll see what people really want out of supporting old channels and time channel blocks; things like that. 

Speaker 0: Okay, cool.

Speaker 8: Yeah, I think on my side, just some fresh rebase issues that I think I just solved, but we should be getting a bunch of taproot stuff in for 1.19.

Speaker 0: [Redacted], are you also using an implementation of MuSig2 that you made in Rust or are you depending on libsecp-zkp?

Speaker 8: For the time being, using the one that actually [Redacted] and I wrote in rust. But I don't think that zkp has rust bindings yet, do they? Because I haven't seen those.

Speaker 2: They are. You’re gonna have to check in a couple of weeks. 

Speaker 5: I think [Redacted] has some maybe?

Speaker 2: No, they exist. They're just in a different package.

Speaker 8: Okay, I thought [Redacted] was still working on them. Alright. Well then, I'll take a look and refactor to use those instead of our MuSig2 library. That's gonna be much better.

Speaker 2: They may not have taproot support yet though, I'm not sure. But they do exist.

Speaker 8: Do people know what the latest is on the upgrade from zkp to secp proper? Is that just waiting? Does that need more fault testing or something like that? Or is the idea just to use zkp for those that need the library?

Speaker 0: Yeah, I think there was a comment about those silent payments or — there was something on the because I thought they didn't want to move it to libsecp normal because it was not required for Bitcoin Core. I don't remember which feature, but there was one feature that would potentially have to be supported in Bitcoin Core that may need MuSig2 support. So they were thinking, again, about including it, but I can't remember which feature it was. I don't think it's the same.

Speaker 5: Well because one thing that happened really is that [Redacted] made some PSBT extensions, like a bip, to basically support the MuSig2 stuff. So, if they're saying that we have complete PSBT flows, then maybe that is what brings it in, perhaps.

Speaker 0: Yeah, that was the reason. Good point.

Speaker 5: Okay. When I have a chance, I could have bindings in the meantime.

Speaker 0: Yeah, but apart from that, I haven't seen any work on that. So, my conclusion was that they would do it because it was required for those descriptors, but I haven't seen anyone work on it. So…

Speaker 5: Yeah, it feels like it would be weird to put silent payments in libsecp proper, but not MuSig2, right? Because everyone's using MuSig2 already. Silent payments still seem like a work in progress. I don't know. Cool. What else?

Speaker 0: Yeah, I don't know if there has been any sales on the attributable error’s PR.

Speaker 5: [Redacted] left a comment. I tagged them at the last spec meeting, and they left a comment there. I think [Redacted]’s back to refreshing the PR basically.

Speaker 0: Okay. Yeah because we said that we might want to move the flag outside of the onion and inside the updated addition message. I don't know if [Redacted] was okay with that. I don't think they really answered that part. Yeah, they did answer, but it's unclear whether they liked it or not. So, I guess we'll have to just touch base with [Redacted] on the PR.

Speaker 5: Sounds good. Okay.

Speaker 2: Okay.

Speaker 5: Check. I made an issue for the peer storage backup thing on the LND side just tracking that. That seems pretty straightforward. Just implementation-wise. But not sure exactly when that will make its way to release. Cool.

Speaker 0: Interesting. I didn't think you would work on that in the short-term.

Speaker 5: Yeah, I made an issue. No commitments. I just, at least defined, the scope of the work. So, it's all good. Just thinking about if we can do something to help people get their funds out. That's always nice.

Speaker 0: This is something that has been working nicely for us, for Phoenix. It really made support much easier because in most cases, people are just able to get their state back automatically, which is really nice. Alright. I guess we're done with all the topics. Is there anything someone wants to mention or anything someone wants to discuss before we wrap up?

Speaker 5: How do people feel during the high fees? Like, we had two or three undecided buy blocks last week or so. Any like stuff that broke? I think we were looking into some fee estimation stuff. We had something — we started to modify the way we sweep anchors in 17, but I don't know if people fully adhered to that. Other than that, nothing was too bad. But I think maybe we'll examine some of the changes that I think people talk about when you decide to force close and in that light of the dust and shills and things like that. Or can we do something in the near term. But this happens every time we have high fees. People freak out. We make everything get better. We repeat in a few months, right?

Speaker 2: Yeah. I screwed up some code on my own personal node that was a patch, so that was fun. But I have seen a number of channels that are anchor channels, but are still stuck in the mempool because they just don't have enough fee on the commitment transactions itself. Note that they often confirm. If you just run a node that has an infinite mempool and accept connections from peers, there's this weird effect on the peer to peer network that even though the mempool is 300 megs, most nodes don't hit 300 megs because other peers will do the limiting for them and then, not forward transactions. As a result, most nodes don't actually have a minimum fee. So, things well below the minimum fee actually propagate kind of okay, not well, but kind of okay. And so, if you have enough peers and you get those transactions into your mempool, they will often confirm. Just a useful hack for those.

Speaker 5: But how would they really, if other peers are setting the fee filter? Wouldn't that mean that even if...

Speaker 2: My point is many peers do not set the fee filter because they never actually hit the mempool limit because their peers hit the mempool limit first. Thus, most peers,or many nodes, don't hit the mempool limit. Or if they do, they hit it fairly irregularly and will not have a high fee filter. 

Speaker 5: Interesting. So you're saying that if you increase your max mempool, connect a bunch of peers, you can relay stuff below 10 sata byte or whatever is getting purged right now?

Speaker 2: And it will get included, yes.

Speaker 5: Oh, okay. Interesting.

Speaker 0: Not sure we can rely on that to be... 

Speaker 2: No, it is not reliable, and it will often take many, many blocks before it does get mined, but I have seen a number of transactions like that get mined.

Speaker 5: Interesting. 

Speaker 1: [Redacted] had a nice thought where they said maybe we should not focus on making the force closes cheap, but maybe make sure that we address all the reasons why we force close. Like, maybe working on the reasons, not the consequences. I think if we do like the sweeping so cheap, everybody would say: Yeah, it's so cheap to force close. Let's do it like this.

Speaker 0: Yeah, we should definitely fix every force close. I think that every month I comb through our logs and all the force closes that we have to see if there's something that seems to be a new bug and seems to be something that we can fix. Yeah, it's a constant fight, but I think we should all spend some time, all the time, trying to figure out how to fix all the potential force closes that we have.

Speaker 5: Totally. One thing LND is doing, I think in 18, is that before, the reason for the force close was in the logs and that would get lost. Now, we're actually trying to keep records basically so you don't necessarily have to look at the logs. Maybe you can just see exactly why it force closed and the conditions around it. Maybe that can help us find some odd cases or something like that. But I think that would be — that's not master yet. I think it's PR. Cool, okay. If that's it, Happy Holidays and Thanksgiving and stuff to the Americans. For the rest, you guys can eat a big dinner or two. Cool. Okay. Thanks y'all. See everyone on time. 

Speaker 0: Bye.

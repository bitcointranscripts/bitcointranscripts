---
title: 'Newsletter #292 Recap'
transcript_by: 'markon1-a via review.btctranscripts.com'
media: 'https://twitter.com/i/spaces/1mnxepjZboAJX'
date: '2024-03-07'
tags:
  - 'developer-tools'
  - 'psbt'
  - 'musig'
speakers:
  - 'Mark Erhardt'
  - 'Dave Harding'
  - 'Josibake'
  - 'Salvatore Ingala'
  - 'Fabian Jahr'
categories:
  - 'podcast'
---
Mark Erhardt: 00:03:57

Good morning.
This is Optech Newsletter #292 Recap.
And as you can hear, Mike is not here today and I'm filling in as the main host.
Today we have four news items, two releases and release candidates, and four PRs to talk about in our notable code and documentation changes.
I'm Merch and I work at Chaincode Labs and bring you weekly this OpTech newsletter recap.
Today I'm joined by Dave.

Dave Harding: 00:04:41

Hi, I'm Dave Harding.
I'm co-author of the OpTech newsletter and co-author of the third edition of Mastering Bitcoin.

Mark Erhardt: 00:04:48

Josie.

Josie Baker: 00:04:51

Hi, I'm Josie.
I work on Bitcoin stuff.

Mark Erhardt: 00:04:57

Salvatore.

Salvatore Ingala: 00:05:00

Hi, I'm Salvatore and I work on the Ledger Bitcoin app and right now I'm working on `MuSig`.

Mark Erhardt: 00:05:06

Fabian?

Fabian Jahr: 00:05:09

Hi, I'm Fabian.
I work on Bitcoin Core and some related projects and I'm supported by Brink.

## GitLab backup for Bitcoin Core GitHub project

Mark Erhardt: 00:05:16

Super.
So Fabian asked that we could move forward the GitLab backup topic because he has a limited time window.
So I propose that for the people that are following along with the newsletter, we actually start with the fourth newsletter item.
Let me try to put it together in one sentence and then Fabian can maybe give a bigger, better overview.
So for a very long time, we have been thinking about that we do not like very much how we're tied to GitHub.
And since occasionally stuff just disappears on the Internet, we would be in a lot of trouble if our 30,000 or so issues and pull requests and all the comments written there were not available anymore.
So for a long time, we've already been doing backups.
We have just mirrors where people write out all the comments and issues and pull requests that are created.
Obviously the code itself is backed up to all the contributors that have copies of the repositories and their own local branches.
But it looks like Fabian has spent quite some time to investigate on how syncing with GitLab would work for the Bitcoin GitHub account.
Understanding is that you figured out how to make this work for good, but not live, just you can get everything synced over.

Fabian Jahr: 00:06:56

Yeah, exactly.
So I mean, to just give a little additional recap from my side.
So 18 months ago, many people probably remember this, we had the Tornado Cash incident where, aside from the other legal action that happened, the repository just disappeared from GitHub completely.
And that kind of triggered me to look into this topic again more deeply and basically put it as one of my high priority projects in the last year.
And so the idea is clear, like as you said, we have a lot of mechanisms to back up the code.
We have a lot of mechanisms to back up like the comments and reviews.
For these there's a lot of scripts that people can run and just like save the raw data as JSON locally.
Then a developer B1OX, has something that also displays the data then again, nicely and kind of like a similar format to GitHub so you can then read the backup again in kind of the fashion that you're used to.
But what we're really missing so far is kind of something where we can have the data transferred and then continue working on it in a similar workflow that we are used to with GitHub in case the GitHub repository goes away.
And then it's a related question if we were to do this only and keep this kind of only for the worst case scenario, or if we want to do the switch at some point soon in the future.
What I did is I basically, yeah, set up a self-hosted GitLab.
So this is not about GitLab.com, the kind of the comparable to GitHub.com, but you can self-host GitLab.
The nice thing is the code is almost all open source.
So they say the core code is open source.
There's some modules that you can pay for then that you get in addition.
But all that I'm using is open source.
And so you can host that.
And if you know GitLab, it looks very similar to GitHub.
And then you have syncing mechanisms and they also have some additional tools that you can use.
And so they have one functionality that they call mirroring, which is kind of allowing you to do this like live following of another repository.
That was originally my goal to use this, which is what was called being like a live feature.
Unfortunately, that doesn't work for our use case right now.
I made a writer where I described a bit more, but they simply haven't built it out for this direction from Github.com to a self-hosted GitLab.
So that means we would need to build this all ourself and run it.
So what I've done now is you can basically run a one-time syncing process continuously with a script.
And so that means you have an up-to-date backup that is on average maybe like a day old or so, because the, the sync takes over a day to run completely.
But then you have all the data there and you could continue the work on the self-hosted GitLab instance.
Then there's quite a lot of configuration that was the reason why it took so much time for me to figure this actually out and to actually make the sync be successful for the first time.
But yeah, that is all documented now what you have to configure.
There's some things that you have to turn off, some things that you have to switch on, so that the syncing process just doesn't fail at some point after 28 hours or something like that.
With that in theory, at least it's possible for us to run this practice is possible for us to run this.
And then, if GitHub.com repository would go away, we could continue working on a self-hosted GitLab instance.

Mark Erhardt: 00:11:14

Right.
So previously we only had archives and we would be able to search for previous conversations and ideas being exchanged, but there wasn't a way to go directly to a workable copy of the repository where we could jump in and continue our conversations immediately.
And that's what you've been working on.
My understanding is that it takes 36 hours to sync the whole repository.
So for all the active conversations, you might actually, if they're earlier in the process, already be a day late, but that's definitely a lot better than nothing.
Is there any way to sort of just get the diff and add to things you've synced before?

Fabian Jahr: 00:11:59

Unfortunately that's not possible.
I mean, with all of this, GitLab is open source.
And of course, we could all build out of this, but also GitLab is very complicated.
And so I really try to use it kind of as a user and see if it has features for us that we can use, configurations that we can set as a user, and then it's going to do the job for us because engineering resources are very scarce for Bitcoin Core.
And so I was really trying to get something that is maintained by somebody else.
But still, like, I mean, of course, worst case, we can look inside because it's open source.
But yeah, that is kind of the idea.
So with all of that, all the limitations that I'm giving, they're not, like, you can do this if you want to build it.
It's possible to still do this, but then you will also have to maintain it yourself.
And that of course takes a lot of time.
For what we have from GitLab as a user, that is a limitation.

Mark Erhardt: 00:13:04

Right, but that's of course a huge improvement already over the previous situation.
Dave, Josie, Salvatore, does one of you have comments or questions?

Dave Harding: 00:13:15

First of all, thank you very much, Fabian, for working on this.
This is obviously very important that we have a backup that we're able to move quickly to an alternative if we have to.
And I tried out your preview site and I thought it looked really good.
It was really nice.
I was impressed that It attributed everything to everybody.
It just felt like a slightly different GitHub look.
You just go there and it looks slightly different than what you're used to, but otherwise it's the same.
If we actually moved to that site, I noticed all the issues and PRs were correctly attributed to an account with the same name as the GitHub account.
So fanquake stuff was attributed to fanquake and so on.
How much work would it be for people to claim those accounts?
Because I mean, obviously, you didn't copy over their GitHub credentials, would you have to be sitting there and, emailing everybody and saying, here, here's your one time password, log in and change it and all that kind of stuff?

Fabian Jahr: 00:14:17

Yeah, so that's something where this actually is kind of cool from GitLab, but also we're running into limitations and this is really like part of why it was hard for me to figure this out.
And so you see some comments and PRs and issues or so being attributed like to an actual account.
And then you see others that are actually attributed to the root administrator.
And then you will see like a comment inside of the text of the comment, yeah?
And that in the top says, for example, user fjahr.
So, and the distinction between the two is because some people have their email as public set on their GitHub account.
And then a lot of other people have it set as private.
And so what GitLab does for the people that have set it as public is it creates an account on the instance and then attributes all of the comments and PRs and issues to that account.
And then if somebody like, for example, if Fanquake has their email public, then you can go in and you basically log in, you basically do a password reset and then you have the account and you have everything basically just like it was on GitHub.
But most people, myself included, have the email private.
It's for the people that contribute actively, it's in the commits anyway, then you can probably think about setting it just public in your GitHub profile as well.
But then this feature goes away and then you have this like inline comment in there that where it's still clear historically that you made that comment, but for example, you will not be able to go back and just edit that comment later on.
It's not a huge deal, but yeah, for maximum convenience, if you care about this, set your email to public and then you will be able to just switch over and it's really going to feel not much different to before.

Mark Erhardt: 00:16:32

Super.
So I think we've covered mostly this news item.
If anyone else has a comment, now would be a good time.
Fabian, do you have any calls for action or where are you going from here with this?

Fabian Jahr: 00:16:50

So I mean, I made a Delving Bitcoin post that you're probably going to link to.
And from there, I'm also linking to just that and it's also on GitHub, ironically, but I can also send it to you if it goes away.
So there you can read the instructions basically to set it up.
If somebody wants to set it up and you get stuck anywhere, of course, contact me.
I'm very happy to help you explore this.
I'm also very happy to get feedback from somebody who looks in this hosted repository, in this example repository, the instance that I have set up.
And if you see anything in there in the data that looks weird to you, that is different than you would expect it, then also of course notify me so that I can track down any bugs or so that are potentially in the syncing mechanism.
So these are really things that I'm suggesting if you're interested in this.

Mark Erhardt: 00:18:00

Super, so play around and let Fabian know if you find anything curious.
We got a question from the audience.
Mike, go ahead.

Mike: 00:18:08

Hey, apologies my voice is messed up right now, but Fabian, are there any concerns with hosting upgrade security of GitLab and then the second one is, are there, I mean the plain Jane, free GitLab version is pretty feature incomplete with roles and different RBAC controls and stuff.
Is any of that concern?
Because I feel like you're going to end up losing a lot of functionality that GitHub gives you potentially.
I would be curious to hear your thoughts on that.

Fabian Jahr: 00:18:52

So, for the second question, we currently from Brink have an enterprise, testing, license basically that I'm currently using.
The idea there was, so we asked GitLab to give us that and they give it out for free in some cases to open source projects.
So that's probably why I'm not really running into these limitations if they are relevant to us.
But of course, it's not for everyone.
Not everyone can get this license.
So, but maybe I'm not seeing these limitations, but from what I was seeing in the documentation in terms of the syncing features, like what I'm actually doing now, because the mirroring is not possible as I said that was originally the idea but it wasn't possible after all.
But the syncing should be possible with the community edition as well, same way that I'm doing.
But with actually running it as administrators like the maintainers do on GitHub right now, I haven't played around that much with it.
And I'm also not a maintainer myself, so I don't have full overview of all the tools that they are using on GitHub.
So that would be probably also a good step to put on to-do list to explore this a bit more with one of the maintainers who can give feedback, like if they were going to switch over and they wanted to fulfill the role the same as before, if that would require additional, adjustments to, to their workflow, yeah.
Sorry, the first one I didn't fully understand.

Mike: 00:20:44

The first one.
So running a GitLab server.
So first off, just to follow up, having the enterprise license is a big deal for free, because GitLab can get quite expensive.
We're talking $100 per developer using the server.
If you get all that for free, that's pretty powerful.
The first question was, and again, sorry for my voice.
The first question was, is there any, GitLab is a constant battle in my opinion of like making sure it's secured and upgraded, it's, especially when you have a lot of users using it, is there any concern with who's going to actually maintain that GitLab server if and when it would be used as like a source of truth for the think of GitHub's, or sorry, Bitcoin's source code?

Fabian Jahr: 00:21:35

Unfortunately, I haven't put that much thought into this as well.
For now developed as like the worst case scenario backup, right?
Like if GitHub just goes away, this is better than what we had before.
And yeah, this would still need to be figured out.
Like right now, there's two people that have access to the server.
Both are working at Brink or supported by Brink.
So, yeah, that would be a conversation to be had.
That just hasn't been a big concern for me.
But definitely something also to put on to do list.

## Updating BIP21 `bitcoin:` URIs

Mark Erhardt: 00:22:18

Awesome.
Thank you for your questions.
And I think we're going to wrap up this topic then.
Fabian, thank you for joining us.
If you need to drop, we understand if you want to hang out a little more, please stick around.
We're moving on to the next topic and the next news item is Josie Baker suggested on Delving Bitcoin a revamp of the BIP21 URIs, what is it?
Universal Resource Identifiers.
So you've probably already seen at some point Bitcoin colon and then Bitcoin address.
It's used for example in QR codes.
And as I understand it, the original BIP21 suggests that the first item after Bitcoin colon always has to be a pay to public key hash address.
Now, especially I have been vocal on this topic, but pay to public key hash is not the most block space efficient method of receiving funds anymore.
And a lot of people have been using the scheme basically non-spec compliant and have been putting other Bitcoin addresses there or have been labeling the addresses that they give with various schemes.
So my understanding is that Josie has taken some time to investigate how the spec is specified versus how it's actually used in the wild and is suggesting how we could improve it to cater to what we're seeing the actual use to be like and how that would be future-proof and compatible with going forward.
Josie, do you want to take it from here?

Josie Baker: 00:24:06

Yeah, sure.
Thanks for having me on to discuss it.
I think I'll give a little bit of background as kind of how I got interested in this topic.
And then I want to mention briefly something about like why I think it's important when we talk about spec compliant versus non-spec compliant.
And then kind of maybe talk through the meat of the proposal.
But this came up for Ruben Thompson and, because as we've been writing the silent payments, but we thought a lot about how do we not contribute to new address format fatigue, which is in Bitcoin, I'm a wallet developer, I build a wallet, and then next week somebody comes out with a new thing, a new address, a new protocol, and then I got to go and I got to update that.
But then it's not really going work until other wallets understand it.
So we kind of have this problem where as we innovate and come up with cool new stuff, there's then this rollout and adoption phase, which is very frustrating.
I think Taproot is probably the best example of this.
There are people who really want to use Taproot and there are wallets that want to support Taproot, but it's hard from a developer's standpoint to do the work of supporting something like Taproot if you know that every single user of Gemini, Coinbase, Binance is not going to be able to withdraw from those exchanges to their wallet because those exchanges don't recognize the address format.
So this is this like, I think, known pain point that people feel a lot.
So I think naturally when you see someone coming along being like, hey, I've got a new address format, there's like people kind of grit their teeth, like,
 no, not again.
So Ruben and I had been thinking about that.
And when we were designing silent payments, we were like, cool, let's just try to make this as close to a silent, I'm sorry, a Taproot address as we can.
So we reuse the Bech32M encoding.
You know, came up with a HRP and identifier.
And then it was kind of brought up like, well, if you want to use this in BIP21, you got to define a key for it.
And that seemed kind of weird to me that like every bit that wants to be compatible with BIP21 has to define a key in their own bit.
So I started to kind of look into it a little bit.
And that led me to actually read the text of BIP21.
And I see there's a hand up there.
I can pause if you have a question.

Mark Erhardt: 00:26:34

It's kind of funny because the human readable parts, the HRPs on all of the addresses actually tell you what it is already.
So needing to have that parameter label that tells you what the following data part is, is kind of funny because that's already done by the HRP itself.
Sorry.

Josie Baker: 00:26:57

No, yeah, I think that's a great point.
And I think this is where like context is helpful.
So I went back and I reread BIP21.
And kind of the first thing that jumped out to me is the spec says, the the root there needs to be a pay to pubkey hash a legacy address.
And it says, you know, Bitcoin address is base 58 encoded.
And you read that and you're like, nah, that's kind of weird.
Like nobody does that.
And I've seen, you know, BIP21 URIs and QR codes that, even like Bitcoin Core does like Bitcoin: the address.
So that was already kind of like, okay, well that's kind of annoying.
And then reading through, I think the original intent of BIP21 is any new address format that we came up with was going to get its own extension key using the language of BIP21.
So you'd have your legacy addresses, which was the only thing at the time.
Then we came out with pay to script hash.
And I think if everyone had been following the BIP21 philosophy, they would have defined a key, you know, pay to script hash equals blah.
And then that way it's usable in BIP21.
Same with Segwit, we would have defined a new key and so on and so forth.
What that would give us in theory is a fully backwards compatible URI, meaning I as a receiver can post this URI in a QR code.
One QR code, someone can scan it and their wallet will pick the key that it understands.
And there's no failure on either side.
I always get paid.
The person sending always gets to pay, which is great in theory, right?
It's an amazing user experience.
And then it avoids this problem of like sometimes you go to someone's page where they're posting Bitcoin stuff and there's like six different ways you can pay them.
And for us that are in the ecosystem, we're like, okay, that's fine.
But for newcomers or people who just kind of want like a payment experience, this is a really bad experience.
So I think the philosophy of BIP21 was really good.
But that didn't happen in practice, right?
People just kind of started defining new address types and they didn't define extension keys in BIP21.
And that, you know, we have, we don't have an extension key for PID script hash.
We don't have an extension key for batch32 or batch 32m.
And instead people just started using the addresses directly.
And this is where maybe I want to comment on like what I mean by, not spec compliant.
People used it in kind of how they took the spirit of it to be, which is totally fine.
We look at something else written and we're like, okay, yeah, that was written in I think 2012 or 2011 when legacy was the only address.
So it's reasonable that the spec says that it needs to be Base58 encoded, whatever.
We all can kind of figure out what the intent was.
The problem is the more time goes on and the more new people come into the space, we can't really rely on this tribal knowledge, right?
Like if I were a developer that didn't really know anything about Bitcoin and I got hired by a company to build a Bitcoin wallet, and then they said, hey, go like implement BIP21.
I would go read that and I'd be like, okay, every BIP-21 URI needs to have a Base58 legacy encoded address.
I would code it up that way.
And then it just wouldn't work with how 90% of people are using it.
And that's a problem the more Bitcoin grows and the space becomes broader, which is kind of what initially got me thinking, I think we just need to go back to BIP21 and rethink this a little BIP because there's a lot of what I'll call non-spec compliant or tribal usage of BIP21.
And if you're not really in the club, you might not know about that.
And so then it really doesn't function as a standard anymore.
People just kind of do it however they feel like it should be done, which has worked, I think, relatively well up to this point.

Mark Erhardt: 00:30:34

All right.
So you've established well how the actual use and the original writing have diverged and you say that actually The intent was good, but what should we do?
We should?

Josibake: 00:30:50

Yeah.
You already kind of hinted at it.
Since BIP 21, we've learned a lot, I think, and we've come up with a lot of really good solutions to problems that existed back then.
One of them being batch 32 encodings, which as you mentioned, the batch 32 encoding includes an HRP, which is a human readable key that allows the encoded data to self-identify itself.
The HRP says I am blah.
In the case of SegWit, it's the BC is the HRP, and then we also have HRPs defined for test networks, etc.
And then batch 32 encoding has the separator, which is the one character.
And the one character says, okay, everything after this is the data.
And then in the case of segwit addresses or batch 32, you have a version which indicates the segwit version, so on and so forth.
So you have this really clean way of encoding a piece of data and the data immediately tells whoever's using it, hey, I'm this, and here's how you should interpret the data part based on what the HRP is.
So it's functionally the same as a key value pair.
So looking at how BIP-21 is used and how we might further extend it, it just seemed natural to me.
It's like, well, if something already is using this self-identifying scheme of having the HRP, why don't we just allow people to include those directly in the URI, which is what I proposed in the delving posts or what I kind of arrived at through some conversation.
And this is just one idea of how to do it, but this is the one that feels the most natural to me.
So then you don't really have this key, you don't really have a root and then key value pairs.
You just kind of have self-describing things with, with a separator.
The nice thing about this is, and this is, I guess, the thing that's most attractive to me about this as a solution is, now anybody who uses the batch 32, batch 32M encoding scheme, which really, when I say batch 32, I really just mean batch 32 M since that's like the latest and greatest.
So batch 32 M, let's say one of these new proposals like Arc was like, oh, okay, we need a new address type to signify like, if you pay to this, you're gonna join the arc network or whatever.
If they encode it as batch 32 M and they choose an HRP and encode their data, they are automatically able to be included in BIP 21 URIs without developers needing to change anything, Right?
No, well, more specifically, not needing to change anything about their BIP 21 parsing.
If they can parse an arc address, it just works.
So we get this future extensibility that's really nice.
Same with silent payments, right?
We're encoding silent payments as a batch 32M with the SP HRP.
So if developers were to update their BIP 21 implementations to just look for HRP encoded thing, batch 32 encoded things with HRPs, then silent payments just works for free with a BIP 21 URI.
So this future extensibility thing is a thing that really clicked for me of like, okay, stuff encoded with an HRP fits really nicely with this.
And then we don't run into this problem of every new address format or every new payment protocol that comes out then needs to also go and define a BIP 21 key or else it's not going to work.
And looking at history, this is kind of how we got into the problem in the first place.
SegWit addresses came out and they did not define a BIP21 key, pay to script hash addresses, and so on and so forth.
And I think that that just kind of indicates that process doesn't scale really well.
That like every new BIP needs to be aware of BIP21 and define something for it in order for it to work in this future extensible way.
So yeah, that's kind of the crux of the proposal.
That learn from how we're using things to kind of update the spec for BIP-21 so that the spec actually is a little bit more reflective of how it's being used, and then also allow for this more future extensible method of using BIP-21 that doesn't require all these BIPs out there, both existing and new, to kind of go back and retroactively define key value pairs.
And in the case of batch 32, M encoded stuff or batch 32, defining a key value for a batch 32 address kind of seems silly because the, like you mentioned earlier, Merge, the, the HRP is already functioning as a key.
So I'll stop there.
Questions or.

Mark Erhardt: 00:35:12

So basically, bring it forward a decade, touch it up to, match the current reality.
Allow for any addresses to be put there instead of tying it to a specific type, like the legacy address.
Maybe while we're at it, we could also say, if there's multiple things, the order in which they appear is the order in which we prefer to be paid, for example.
And finally, I think there's also an issue around whether Bitcoin has to be lowercase or uppercase, Because in the QR codes, we can encode stuff more efficiently if it's all uppercase, but the spec, for example, demands that it's all lowercase, I believe.
So sort of just a chance to update everything.
So what do you think?
Are you going to try to update BIP 21?
Are you writing a new BIP that supersedes BIP 21?
Does anyone else have questions or comments on this one?

Josibake: 00:36:14

Yeah, regarding the updating or superseding, I think it's like the big question, right?
Like what makes the most sense?
I think that the, the idea of following like a strict reading of the bit processes, we should write a new bit that supersedes it.
I would kind of, you know, whatever makes the most sense, right?
If it makes sense to just write a new BIP, I think that makes sense.
I think Matt actually, so there was some discussion on the Delving post, mostly just between Matt and myself.
Reuben Thompson chimed in as well.
I think Matt, the blue Matt, went ahead and opened a PR to update BIP 21, kind of with his version of how he thinks it should be updated.
So just to, I think, summarize his version, he says we instead say anything that falls into this whitelisted set of addresses, which is taproot, segwit, pagescript, hash, and legacy, those can go in the root.
And then everything else has to go in key value parameters.
And then once the things in key value parameters have received, like once we're sure that they're near universally supported, then you can omit the root entirely.
So you'd have Bitcoin colon key value pair, key value pair.
So he proposed that as a PR to update the BIP.
I disagree with that approach.
I don't think it solves the future extensibility problem.
I still think it creates some ambiguity of what goes in the route and whatnot.
So I responded on that PR with the things that I'm proposing.
I don't know, just kind of like see where it goes.
At some point, you know, if it kind of just deadlocks on no agreement on how to update BIP 21, I might just open a new BIP just to see, you know, like, hey, here's a new BIP that's kind of superseding BIP 21, learning from the past.
And then it's kind of up to people, you know, you can keep implementing that 21, you can go with a new BIP.
But I think just having more clarity for wallets would help a lot.
Especially with interoperability and everything.

Mark Erhardt: 00:38:19

Yeah.
Thinking about how I would like to use BIP 21 in a future where we have silent payments would be, I would probably not even want to have a potential address reuse permanent address there.
I would just want to post a silent payments address.
And if I'm not allowed to do that by the new BIP, I guess, yeah, I would suggest that we should allow any subset of the addresses.
And if they read it and they can't use it, well, maybe I don't want to receive a payment that doesn't follow the payment instructions.
Dave.

Josibake: 00:38:54

Yeah.
I want to comment on that really quickly because I think that's super important.
That's actually where some of my initial, why I didn't initially want to specify anything in BIP352 about BIP21 is because if you're using silent payments, it indicates to me you're a privacy conscious user, right?
And if you were to add a silent payments address in a URI with a static, you know, reused address, there are real privacy implications, right?
Like if someone pays your reused address and then someone else makes a silent payment, and then you spend those coins together, you're effectively linking an address that was intended to be silent to this reused address.
So I was like, I don't really want to put this in bit three 52, because then I'm going to have to write this massive explainer about why you really shouldn't do this.
On the other hand, I think Matt has a good point that some people might not care and they might just want the UX benefits of silent payments.
And in that sense, they should be able to use it in BIP 21.
And so that kind of got me thinking of like, all right, well, I don't want to define it in this, but because I think there's privacy problems, but I also don't want to stonewall anyone from using it.
So why don't we just update BIP 21 in a way where, you know, things can just kind of automatically be included without us requiring to go and have every single BIP, you know, promote something about it.
So I agree with your sentiment and, you know, I think that's going to be the better middle ground.
Like let the users of BIP 21 use what they want to use and let the other BIPs kind of stay focused on the thing that they're supposed to be focused on, which in the case of silent payments, I think is a much stronger focus on privacy.
Go ahead, Dave, you had a question?

Dave Harding: 00:40:32

Yeah, I had a few comments.
First of all, thank you for working on this.
And also, I find it very interesting how your silent payments work has basically brought you to every level of the protocol stack.
Like you're just basically you know rewriting all of Bitcoin in little pieces everywhere just to you know make sure everything just works really well with this silent payments.
It's just very interesting to me how what's basically a very simple idea, it's just got you going everywhere.
So a couple comments there is, first of all, I didn't actually realize that BIP 21 was only PDBKH addresses.
I had not even thought of that.
So you're right, we need to document that, as you call it, the tribal knowledge.
My suggestions for what to do with regard to updating the BIPs is, I think the BIP 21, and this is not what the BIP process says you should do.
It says you should write a new BIP.
But I think BIP 21 should probably be updated to document what everybody is doing right now.
And then maybe a new BIP should come and document how we want to go forward.
That's how I would kind of divide that work.
I wouldn't think about forward compatibility in updates to a BIP 21 now, but we should definitely document how people are using it now.
So we get that, as you said, that knowledge out of tribal knowledge and into an actual specification that people will read.
And then we can have a separate BIP that describes how we wanna go and use this in the future for silent payments, for lightning, for whatever.
And The other thing I had there was one concern I might have about you know throwing new keys or whatever you want to call it, address formats into a Bitcoin URI is what's an optional key there and what's a required key.
If you just throw, say, a base 32 arc address into there, how does the software parsing that know whether or not that's important and it should drop the payment request if it doesn't understand it or that it's optional and maybe there's also a fallback address, a silent payments address, an on-chain address in there and they should just ignore that.
For example, in the Lightning protocol, they have type numbers that they assign to all their protocol messages.
And they have this idea that even messages, if you receive an even message and you don't understand it, you have to drop that request.
You have to say I don't understand what you're talking about, I'm just going to...
Actually I think they closed the channel for some of the stuff because it's clearly they're incompatible and they don't want to get into a case where they're losing money.
And with Bitcoin URIs, again, we're talking about changing money and software that parses them needs to know what's optional and what's required.
So I just wanted to know if you had any thoughts on that, is that something you considered?

Josibake: 00:44:02

Yeah, yeah, Great questions.
To your first comment about silent payments kind of touching everything, that was certainly not my intent.
You started with this like really small idea and you're like, oh, this would be a pretty simple project.
Next thing you know, it's like, it's everywhere.
But it is a lot of fun.
And it's been a good learning experience.
I think the reason for that is, sign-on payments and just this whole idea, it's kind of core to how Bitcoin works, right?
Like, we have to, You and I have to agree on how to communicate how I want to receive money and how you're able to send money.
And this is kind of like the core idea of Bitcoin, which is why I think when you get into something like silent payments, it does start to touch a lot of different stuff.
To your second question, I want to say let's talk about a simplified world where everything is batch 32m encoded, meaning it has an HRP and a data part, and the HRP is kind of what describes what it is.
And we're kind of, we're allowed to redesign BIP 21 however we want.
So BIP 21 had this notion already of like optional versus required parameters and optional parameters are just what's in there by default, right?
You throw some stuff in there And then whoever's parsing it, the sender actually decides what's important to them.
So Merch earlier had mentioned, you know, kind of like some order dependence.
BIP21 says no, there's a root address, which is a legacy address, which everyone can pay.
And then there's these optional key value parameters that come after it.
And the sender actually gets to decide which one they want to use, not the receiver.
So in the case of like unified QR codes and BIP21, there's a lightning key that you attach on.
And the sender says, ah, if I understand lightning, I'm going to use lightning.
And then everyone was like, oh, shouldn't they always use lightning?
I was like, well, no, like what if the lightning payment is so large that the on-chain would actually be cheaper for the sender.
So then the sender might prefer to use the on-chain one.
So the idea of BIP21 and kind of what I'm proposing too as well is the sender is actually the one that decides what's important.
So like in that sense everything is optional.
Now the receiver also has some ability to communicate how they want to be paid and more specifically how they don't want to be paid.
And that if the receiver doesn't post a URI with lots of options for you, so let's use sign of payments as an example.
I'm a very privacy conscious sign of payments user.
I want to post a URI that just has a sign of payments address in it.
And I don't, if you can't understand silent payments, then I don't want an on-chain fallback because that would lead to address reuse for you and me or loss of privacy.
So in that sense, I'm gonna post a URI and I accept that whoever tries to pay this, if they can't pay silent payments, it's gonna fail.
And the reason it would fail for the user, the sender is they would try to parse that URI and they wouldn't see anything that they recognize just by looking at the HRPs. Another example would be I post a silent payment address and I also include a tap root address because I'm like, all right, maybe they don't understand some of the payments and I'd rather get paid even if it's in a non-private way.
So then I include a taproot address.
Then the receiver, I'm sorry, the sender would parse that URI and they would look for an HRP that they recognize.
They don't recognize the SP HRP.
They do recognize the BC HRP.
They split that BC1P.
They know how to pay a taproot address.
They're good to go.
This is, I think, functionally equivalent to how it works today in BIP21, where instead of looking for an HRP, people just look for a key.
And as soon as they find a key that they're interested in and aware of, they just ignore everything else and they try to pay that key.
So I think that's kind of how they solve the ambiguity problem.
I guess the biggest difference between kind of where I'm leaning and the existing BIP-21 is BIP-21 is pretty opinionated.
There should always be something there that they can pay, which is the legacy address.

Dave Harding: 00:48:04

I guess, I don't wanna go into too much detail here.
I can always post on the thread, but I guess I'm just thinking about the other query parameters that it passed.
For example, if you pass an amount parameter, might there be a case where that amount parameter would apply to legacy addresses and base 32 addresses and silent payments, but it might not apply to Lightning.
You might be passing a bulk 12 URL where you want the person to get the amount from the offer rather than the amount parameter, but you want to include the amount parameter in the thing.
That's not a great example because presumably anybody with- I think it's a perfect example.

Josibake: 00:48:57

I had the same question reading BIP21 as written where we do have these optional parameters like amount, message, etc.
And then I think the most common pattern that you see people using Bit21 today is called the unified QR code, where you have Bitcoin address, then you have a lightning equals parameter, and that lightning equals then specifies a Bolt11 invoice.
But the Bolt11 invoice, if I understand correctly, also encodes an amount into the bolt 11 invoice.
So then it's like, well, do I prefer the bolt 11 invoice?
Do I prefer the amount?
And that's currently not specified.
I think, you know, you could work around this where bit 21 specifies two separators, the question mark separator and the ampersand separator.
And I think that the intent there is like the question mark separator is kind of like the big one.
And so I can have A question mark, B question mark, C.
And then if I want to attach additional optional parameters to C, it would be question mark, C, ampersand amount, ampersand message.
And then the parser kind of knows that.
OK, these ones belong to this one, but I don't know if that's true, because that's just it.
I feel like it's a little under specified currently.

Dave Harding: 00:50:12

I think that's actually an RFC something that's required that the first parameter be with a question mark and all remaining parameters be ampersand.
So it doesn't have any semantics in a URI.
I think it's RFC 3986.
But yeah, so I don't think we can do it that way.
I think we'd have to use uppercase, or I don't know if that's the right thing, but an underscore character or something.

Mark Erhardt: 00:50:46

All right, I feel like we're getting a little too much into the detail of the proposal.
Let's try to wrap it up.
Josi, do you want to make a call of action or a summary, like a sentence or two, And then we'll move on to the next topic.

Josibake: 00:51:03

Yeah, I mean, the biggest one would be like, if this is something you're interested in, please chime in on the WBitcoin post, there's stuff, you know, I'm coming at this from the thing that interested me, but I'm sure there are other people who have also, you know, feel like there's unaddressed points that could be addressed.
So if we're going to do this, I'd rather get a lot more input.
And I would say that that's the thing that would motivate me to actually keep working on this and maybe even write a new BIP is if there's a lot of feedback from people to be like, hey, by the way, we have a chance to fix a bunch of other stuff.
So if you're interested, feel free to comment.

Mark Erhardt: 00:51:37

All right.

Josibake: 00:51:37

Thanks, everybody, for the great questions.

## PSBTs for multiple concurrent MuSig2 signing sessions

Mark Erhardt: 00:51:40

Yeah.
Thanks for coming on again.
If you have time, please stick around.
If you have to drop off to do something else, we understand.
We're moving on to the next topic.
The next topic is PSBT for multiple concurrent Music 2 signing sessions.
So Salvatore is working with hardware wallets and looking to make PSBT and especially in the context of music to work well.
And from what I understand, one of the issues he has been bumping into is that the state of the music to signing session scales with the number of inputs on transactions.
And of course, when you're working with a hardware device that has a very limited amount of memory, that can become a blocker or a problem.
So Salvatore is suggesting that we could instead of having the amount of data that you have to keep track of in the session scale with the inputs, have some sort of unified session data that you can derive the input related data deterministically but pseudo randomly from.
Did I roughly understand that right?
And do you want to take it from here?

Salvatore Ingala: 00:52:58

Yeah, that was a great explanation.
And yeah, as you said, I'm thinking about and I started prototyping how to implement music to support in the in the ledger Bitcoin app and meanwhile there is also independent work that HR is doing for standardizing descriptors and everything else it is needed to make all these things work together.
So it's looking great for Music 2 to actually start being used more widely in practice, hopefully, this year.
And yeah, One of the issues that I discovered when I was thinking about how to implement it on a hardware device is that, well, when you're implementing a protocol in Music 2, because it's a two rounds protocol, it's not like simple signatures like we do today, whether Schnorr or STSA, if you do one signature, you just ask the device to produce a signature, the device responds, that's it.
While in Music 2, you have a two-round protocol.
All the cosigners first are invoked the first time to produce what is called a nonce, which is a short for a number that should be used only once.
And after everybody produced this number, the nonce, all these nonces are aggregated.
And then you call the signer the second time with all the nonces and now the protocol does its magic and can continue and produce the final signature.
And bit 327 is the specs of the of music too for Bitcoin and it goes in great length into explaining what are the pitfalls, what can go wrong, like all the ways that this can cause security issues because since you have two rounds it means you have to keep some state between the first round and the second round and this state is a small number it just like could be just 32 bytes let's say but when you sign a Bitcoin transaction you could have an unbounded number of inputs you could have 200 inputs and And so while in BIP-327 a sign-in session is defined in the sense of a single message, in the context of sign-in devices normally you're signing a transaction So your session intuitively is more on the level of the PSBT of the transaction.
And on embedded devices, having all this, if you read the letter, BIP-327, and you implement it without any change whatsoever, the natural way of doing it would be to actually have all these sessions in parallel and for each of these sessions, for each of these inputs basically, have to store some stuff on the device.
And so the idea that I was describing, which is pretty straightforward, since the state that you need for each of these inputs is basically derived from a random number.
A standard idea in this case is to just use one random number and then derive all the other numbers in the same session, pseudo-randomly, using a cryptographically secure pseudo-random number generator.
And the reason I thought it was good to have this audited properly is that, well, when you're implementing cryptographic protocols, there are many ways that things can go wrong.
And so I thought it's very useful to have this first audited and judged by other people who are more experts.
I already had this discussed with Janik Surin who's one of the authors of the Music 2 paper but it was on previous drafts that were not written in the same level of detail and I thought anyway if it took me some time to figure out it could be helpful also for other people to express, like to write down what I thought it could be a good solution.
And yeah, the solution is exactly as you said, that you basically use one random number for the PSBT level session.
And then for each of the individual music to sign-in sessions, you can derive the initial randomness in a pseudo-random way so that you can continue the protocol by keeping only a small amount of state which is just potentially 32 bytes for the whole transaction rather than for each input.
And yeah, the protocol received some comments also from...
I mean the approach received some comments also from Jonas, Nick and Tim Rufing, the other authors of the Music2 Paper.
So I'm happy that I didn't break music.
And So I look forward to try to implement it.

Mark Erhardt: 00:57:49

Yeah.
Thank you for going down that rabbit hole and seeking the, well, feedback of all this community already in advance.
So this seems to be very specifically to hardware wallets.
Would that mean that anyone else has to change how they use music too?
Or is this just at the hardware wallet level, you act differently than other people in how you contribute your announcements?

Salvatore Ingala: 00:58:22

No, this is just at the level of a single signer.
Even non-hardware wallets could do it, but for them maybe it's less relevant because If you have a transaction with 100 inputs and you want to store some 32 bytes for each 100 inputs, it's like 3 kilobytes of data.
So outside of embedded devices, maybe it's much less pressing.
It could still be useful outside because maybe you want to be able to sign 100 transactions in parallel and each of them has 100 inputs, you know.
And so not having to think in advance about hard limits could help, but it's definitely more relevant in the context of harder wallets because state, like having to persist state in memory, it's a much bigger limitation because even if the secure element has some small amount of persistent memory, it's not a lot.
So reducing the amount of state to a small amount per transaction, it's definitely going to make implementations in practice a lot easier.

Mark Erhardt: 00:59:25

Yeah, that sounds right.
Dave, do you have other comments or questions on this one?

Dave Harding: 00:59:31

I guess my only question is, again, thank you for working on this.
It's not something I had thought of, but you're right, it's really important.
And I do like hardware well hearts.
Is there any risk that this data would be easier to leak if someone gained physical access to a hardware wildcard.
It sounds like you may be able to store this data on the secure element, But it also sounds like you're moving it into, from the post, you are moving it into the volatile memory during actual signing operations.
So if I start a session, and let's say I need to keep my hardware wallet in a safe deposit box and some bank employee, while I'm in the middle of a session, you know, but not actually physically with the device, obviously, they grab my device.
Does this increase the risk that somebody could extract compromising information from my hardware wallet if they had physical access to it even though the device had a secure enclave on it?

Salvatore Ingala: 01:00:48

No, I would say it doesn't change anything in that sense.
So the level of security of this memory is the same as any other memory which is in the secure element.
So extracting anything from there, unless there are bugs in the code that allow you to extract this information programmatically, let's say, is as hard as extracting any other secret from the secure element.
But the distinction that I made between the volatile memory and the persistent memory, that was more as a matter of guaranteeing that you are never reusing unknowns.
Because one of the pitfalls you can have when you implement these things is that because you're storing something at the end of the first round, if you can be tricked into running the algorithm twice without repeating the first round.
So you complete the second round with two different transactions, for example, two different executions, but with the same nonce that can lead to nonce reuse, which basically can leak the private key.
And so that was just a way of making auditability as easy as possible, because I am only storing permanently this session in the persistent memory at the end of round one.
And the first thing that I'm doing, so the end of the first round, and the first thing that I do when I begin the second round is I delete it from the memory.
So this makes it a lot easier to make sure that, well, it can never happen that you are able to run the second round twice without generating your randomness.

Mark Erhardt: 01:02:31

Oh, yeah, that's a really important idea.
If your session randomness is tied to the PSPT and isn't specific to an output, you can of course track on the PSPT level whether the session has ended or has to be restarted.
So that sounds cleaner, actually, at the implementation level.

Salvatore Ingala: 01:02:55

Yeah, it's something that, I mean, it's not really a change to BIP-327, because this is something that I do on top to make the implementation mostly more auditable.
But I thought it was a good thing to write down because I think it's a useful detail in implementations.

Mark Erhardt: 01:03:15

Great.
Thank you for coming on and talking to us about your work.
Do you have a call to action or a summary, something that you want to add, still?

Salvatore Ingala: 01:03:26

No, I think we covered it.
I mean, I'm still probably a few months away from having this in the wild, at least on testnet.
But yeah, it looks like progress is happening also outside.

## Discussion about adding more BIP editors

Mark Erhardt: 01:03:40

Okay, super.
Well, thank you for joining us.
If you have time and want to stick around, please feel free.
Otherwise, if you have other things to get to, we understand.
We'll move on to the next news item.
So there's the fourth and final news item because we pulled forward the GitLab backup issue with Fabian.
We're now talking about the discussion to add more BIP editors.
So we have a repository in the Bitcoin organization, which is there for historical reasons.
It's not really related to Bitcoin Core.
And in that, we track proposals to the Bitcoin protocol or just public write-ups on methods and ideas that are useful to many different implementers or groups in the Bitcoin ecosystem.
And we call those the Bitcoin improvement proposals.
Currently we have 135 open pull requests in this repository.
And the process has been frustrating for a few developers to the end that recently we had AJ Towns start the Banana repository as a parallel mechanism where you can post an idea publicly so that a distributed discussion of an idea can reference a single document and everybody knows exactly what we're talking about.
So another approach here is now, Eva Chow posted to the Bitcoin developer mailing list the suggestion that we add more editors because the main editor that is currently shepherding the repository has stated that he's not getting around to doing all the work that is necessary and is to time constraints.
So we're at a point where there's a few people proposed and the discussion hasn't really progressed much since then.
So yeah, if you are interested in that topic, you can find it on the mailing list.
Dave, do you have more information or ideas on where this is going?

Dave Harding: 01:05:57

No, but it would be nice if we could make more progress on BIPs or people can just switch to bananas or however you like to host your documentation.

Mark Erhardt: 01:06:09

Yeah.
Maybe to jump in a little more.
One of the points of frustration is the Understanding is that a BIP is owned by the authors of the BIP because they're proposing their idea and it becomes a public document for everyone to talk about, but it's still sort of their writeup.
So one thing that is supposed to be allowed is that the authors, as they develop their idea, especially while it's still in draft status, but potentially even after it has been published, can add to the BIP or make minor changes like typo corrections.
Or if an example was not 100% clear, like add a clarifying sentence, things like that should always be possible for the BIP owners.
And the other thing that has been holding up processes, the BIP process states that not only should BIPs be obviously from the sphere of Bitcoin interesting topics, but they have to be technically sound.
And so it takes a lot of work for the technical editors of the BIP repository to assess, well, is this actually technically sound?
Is this a well-enough described idea that it can be implemented or not?
And one of the participants in the discussion has proposed, really the documents should have some formal requirements like is it complete, does it not have any references to outside things, is it well written, Does it specify an idea that is about Bitcoin?
And then whether or not it is technically sound should perhaps be more the job of the readers of the BIPs rather than the BIP editor.
So yeah, the discussion seems to be a little bit in the air right now.
The two proposed participants are Ruben Sommersen and Kanzer that have both been around for a long time and would probably be well capable of assessing at least whether the documents are fully fleshed out and whether they're about Bitcoin.
There's been also a couple of self-nominations.
So anyway, That's where I understand the discussion to be.

## Eclair v0.10.0

Mark Erhardt: 01:08:35

All right, we're moving on to the releases and release candidates section.
The first release that we have is Eclair version 10, sorry, version 0.10.0, which is a new major release for the Lightning Node implementation, the Eclair Lightning Node implementation.
So Eclair Version 0.10.0 adds a dual funding feature.
It adds Bolt 12 offers and it has a fully working splicing prototype.
So This sounds like a pretty cool big new release.
We've seen a bunch of these topics out in the wild lately.
We've had T-Best on to talk about dual funding before and about splicing.
Yeah, I don't know if there's many other people that also use the Eclair node besides Sank, but yeah, sounds like a bunch of cool new features, especially if you're using Phoenix Wallet, you'll see what comes down the pipeline there.
Dave, do you have something here?

Dave Harding: 01:09:51

Not really.
I just want to just echo that these are really cool features and I think it's just it's great that Eclair and their team there, they've been really active in working on not just adding these features to their software, but the specifications.
They've been working on, as they implement it, going back and taking their discoveries and talking it over and tweaking the specifications on those things.
So this is the dual funding and the offers and displacing are all compatible with the Boltz protocols for those.
So I think it's just really great seeing a team not just using open source work and releasing open source software, but contributing to the specifications for those.

Mark Erhardt: 01:10:43

Yeah, especially if you look at how small the Assign team is, it's really impressive how on top of the spec work they are.

## Bitcoin Core 26.1rc1

Mark Erhardt: 01:10:53

All right, we have one more release candidate in the section.
We have seen the release candidate one for the Bitcoin Core version 26.1. So this is the maintenance release in the 26 branch.
So if you're currently running Bitcoin Core version 26 and you want to not directly upgrade to the upcoming 27 version, but want to maybe wait a little for the new version to, to settle in and just want to be up to date with the latest bug fixes.
26.1 looks to come out in the next few weeks once the release candidate process is over.
If you're, depending on that, maybe try running it in your testnet setup and give feedback if, for example, you've encountered some of the bugs that are being fixed, whether it works for you.
I've looked over the release notes, and to me it looks like there's only a bunch of small issues and bug fixes that are in there.
Nothing really big that we've talked much about.

## Bitcoin Core #29412

Mark Erhardt: 01:12:06

All right, we get to our notable code and documentation changes section.
We have four different pull requests that we're going to discuss this time.
If you have any questions or comments, please, now is a good time to search for the speaker request button and let us know that you want to contribute to this recap.
So the first one that we'll get into is Bitcoin Core 29,412.
And this one fixes an interesting problem, which is dealing with mutated blocks.
So one of the problems that we've encountered in the past is when a node just gives you bad data, but it is bad in specific ways that the peers that receive it think, oh, generally anything announced to me with this identifier, I do not have to look at again, because it can cause the peers to, for example, not follow the best chain anymore or not to accept a transaction that is valid on the network because they first saw a garbled version of it.
In the context of blocks, for example, someone could temper witness data or change the witness commitment such that it actually no longer matches the block header, but indicates, of course, that the block is invalid.
And I think there was a bug, from what I understand, where the node would actually process such an invalid block and then store partial information and therefore poison itself against the real block.
So what this pull request does is it really gets into all the ways that you can mutate a block and change like little pieces of it to turn them invalid, but make them still propagate and test that Bitcoin Core behaves correctly in that it does not process this mutated block but discards it and stays open to receive an alternative correct version of it.
Dave, I might not have looked as much at this as you have.
Do you want to take it from here?

Dave Harding: 01:14:34

I think you did a great job.
Yeah, this is a really interesting class of problems that we've hit a couple times in Bitcoin Core in the past.
Anybody really interested in this should click on the link in the newsletter to newsletter number 37 which goes into a lot more detail about two of these cases and also we do cover briefly in MASH from Bitcoin the 2012 bug CVE 2012 2459 and It's just you know It's interesting.
It's it's basically the way the attack works is or the the problem It's not necessarily an attack, But the problem works is because Bitcoin uses a Merkle tree and there's some problems in its Merkle tree designs, it's possible to construct multiple different Merkle trees that hash to the same Merkle root, which is in the block header, and the hash to the block header is how we identify blocks in Bitcoin.
So it's possible to create what look like two different blocks, that look like they have the same ID.
So we just end up looking at one of them and saying that's invalid.
And now we don't want to download that same block from our other potentially 124 peers.
So we say if that peer announces a block with the same ID, we're just going to assume it's invalid.
And so we reject it.
And if that happens, it's kind of like an eclipse attack on your node.
And an attacker can exploit that to prevent you from learning about valid blocks.
Now we only reject blocks while the node is still running.
So if you restart your node, they go back and double check and maybe download those valid blocks again.
But it's a potential attack.
It could potentially be used to steal money, especially if you're using something like Lightning where you need to be getting the most recent blocks.
And so This PR just very early in the process, we look at a block and we see if it has one of these things that would make the block invalid but also could later cause us to cache the header and we just stop processes in that block at that point.
We don't catch anything, cache anything.
We just throw away that block and move on.
And I just think that's a really good solution to this problem that we've hit twice.
Like we've hit this problem twice.
It was when you hit it once you fix that immediate bug.
When you hit it twice you got to try to figure out the root cause and stop it.
So I'm really thankful for this PR coming in and just making us safer.
It doesn't, as far as I know, it doesn't fix any active vulnerability in Bitcoin Core right now.
But it just means we're less likely to have vulnerabilities in the future.

Mark Erhardt: 01:17:43

Yeah, that's my understanding too.
So, also maybe this question just popped up for me.
Why doesn't that open us up to abuse from peers or anything like that?
Well, if someone sends us an invalid block, and we then throw it away, we would accept that same invalid block again from another peer.
But the original peer that sent us invalid data, we would disconnect already because they're misbehaving, right?
Sending us invalid blocks is just a no-no, and we don't want to talk to them anymore.
We drop them on the street.
And therefore, even if we get an invalid block and we waste that bandwidth to download the block header and the transaction ID list, maybe if it's a compact block relay.
We only do that once per peer.
So this is naturally already limited in the amount of DOS or abuse that it can lever on us.
And then you also have to remember, A block always has to have proof of work because that's the first thing we check.
We look at the header and if the header doesn't pass the proof of work requirement, we'll never request the rest of the body of the block.
So actually this mutated block thing cannot really be used for dosing much, only for, well, for example, making you drop something or stop following the best chain.
I see that there's a question from the audience.
Dave, did you want to say something?

Dave Harding: 01:19:20

Oh, just really quickly.
All the peer can do is waste your bandwidth.
When you process a block for this code, which runs really early on, like you said, the proof of work happens, So it has to be a mutated valid block.
So that peer can get you to download a whole block and run some hashes.
Hashes are really quick computationally.
A block is something we already have the memory to process.
So the peer is just basically wasting bandwidth and a few computations.
So dropping them, I don't think there's a deal aspect to there if you end up reprocessing that block again.
So it's just a very quick and easy mitigation.
Sorry.

Mark Erhardt: 01:19:58

No, thanks for clarifying.
So, Mike, you have a question here?

Speaker 5: 01:20:03

Yeah, I think he was actually clarifying as I came up on stage, but I might have missed it What was the idea with two Merkle roots with different trees with the same hash, or did I misunderstand that?

Dave Harding: 01:20:23

Yeah, so Bitcoin's Merkle tree design, When you have an odd number of nodes in a Merkle tree, you have to do something.
And in any Merkle tree design, what Bitcoin does is it hashes the node with a copy of itself.
And what this allows an attacker to do is to create a block that looks like it has two copies of the same transaction.
Now ever since VIP30 and VIP34, we really haven't had duplicate transactions in Bitcoin.
And the idea was we'd never had them in the first place.
But you can make a block that looks like it has a duplicate transaction that has the same TXID.
And so you can create a version of the block that has only one transaction with a particular ID and a version of the block that has two transactions with the same TXID.
The second block is invalid, But it hashes to the same Merkle root as the first block There's other ways to cause problems particularly with 64 byte transactions a Merkle Node is the result of two 32 byte hashes And so you can do weird things with 64 byte transactions.
That's also considered in this pull request.
But basically you can create different block contents that hash to the same Merkle root.
Again, the Merkle root is included in the block header.
The block header, and the hash of the block header is how we identify blocks on the network.
Does that answer your question?

Speaker 5: 01:22:07

Well, okay, so I'm still a little bit confused because I'm like thinking, well, if anything in the tree changes, the Merkle root should be different.
So if I wanted to do some homework and look this up, what phrasing would I type in to like look up what this is, like what is this called?

Dave Harding: 01:22:27

What I would suggest you do is go to the newsletter on this news item, the BitcoinCore29412, in the notable code and documentation changes, we have a link to newsletter number 37.
And in newsletter number 37, we have a link to CVE 2012-2459.
It's a write-up on Bitcoin talk by the guy who invented P2P pool.
He discovered the vulnerability.
Also that newsletter number 37 includes a very informative PDF written by Suhas Daktwar who fixed one of these bugs, actually introduced one of these bugs and also fixed one of these bugs.
That PDF goes into a lot of detail about this.
There's an illustration in newsletter number 37.
So I would basically just go to news number 37 and you'll get all the information about this that I think you could possibly ever need.

Speaker 5: 01:23:20

Hey, thank you so much.

## Eclair #2829

Mark Erhardt: 01:23:22

All right, we're moving on to the next PR.
Eclair 2829 allows plugins to change the default behavior when encountering a request to dual fund a channel.
So by default, Eclair will not put any of its funds into a channel opening.
But With a plugin, for example, you could change that behavior and then, for example, try to match the opener's amount or, I guess, talking to T-Bus about being over leveraged by the other party, them putting way more funds in than you wanted and therefore being able to tie up funds on your side.
Maybe there's some interesting things that you want to do on your side for the amount.
So anyway, with this new PR, you can override the default policy and change how much by default your node will contribute to dual funded channels.

Dave Harding: 01:24:32

Yeah, so by default, Eclair just doesn't know what you want to do with your money and it won't tie up your money without asking your permission and basically you can give your permission now by creating a plugin.
So that's all this is.
But it's good for people who want to experiment with dual funding opens and who also want to start experimenting with things like liquidity advertisements.
The core doesn't support liquidity advertisements natively yet, but if you want to experiment with that, now you have the opportunity to.

## LND #8378

Mark Erhardt: 01:25:02

Super, thank you for the color here.
We move on to LND 8378.
LND has made some improvements to its coin selection implementation.
Most specifically, it allows you now to preset some inputs and then allows you to use coin selection to fund the rest of the transaction.
And it also changes that coin selection can now be set as a parameter.
So you can choose what selection strategy your node uses.
I think from cursory look at the pull request, The two choices right now are random selection and largest first selection.
But now when you make the call to build a transaction specifically for funding a channel, then you can A, decide some of the UTXOs manually and B, decide which strategy is used to pick the rest.
Cool.
I take it that Dave signals me to move on.
So we're getting to the final poll request and topic.
If you have any more questions or comments for us, please, you can raise your hand now or ask for speaker access.

## BIPs #1421

Mark Erhardt: 01:26:26

So finally, we're talking about a pull request to the BIPS repository.
We already touched on the BIPS repository earlier, of course.
BIP 345 op-vault, the pull requests got merged now.
And so obviously there is no activation parameters in the description of OpVault or anything like that, but the specification of what James O'Byrne proposes to do with the OpVault opcode is now part of the merged code in the BIP or documentation in the BIPs repository.
Dave, do you have more on that?

Dave Harding: 01:27:14

Nope.
Apparently at least one BIP got merged this week.
We have not had a lot of bits merged.
So go back to our previous news item about needing more editors, but I'm happy to see this merge.
I think James worked on it really hard, and it is a very novel and interesting proposal.
So if you were waiting to read it, now is your chance.

Mark Erhardt: 01:27:39

All right, so we're through our newsletter this week.
Thank you for joining us for the OpTec recap.
Thank you to our guests Salvatore, Fabian and Josy and also for Mike to jump in and ask us some additional questions.
And a lot of thanks to Dave, who's writing most of these newsletters all the time and has lots of things to add here in our recap.
Thank you and hear you

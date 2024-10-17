---
title: Bitcoin Miniscript and what it enables
transcript_by: Stephan Livera
speakers:
  - Antoine Poinsot
  - Salvatore Ingala
date: 2023-01-23
media: https://www.youtube.com/watch?v=D5Q7yB_txkU
---
podcast: https://stephanlivera.com/episode/452/

Antoine and Salvatori, welcome to the show.

Antoine :

Thanks for having us.

Salvatore :

Thank you, Stephan.

Stephan :

So I know you guys are both building out some stuff in Miniscript. Obviously, software and hardware. And I know this is an interesting area, there’s been a bit of discussion about it, but there’s also been some critique about it as well. So I’d be interested to get into this with you guys, but maybe first if we could start. What was your interest like, why did you get interested in this idea of Miniscript?

Antoine

For me, it was starting working in revolts and actually having the responsibility of developing the projects and tinkering with bitcoin scripts and thinking, well, I’m not going to take the responsibility of writing bitcoin scripts by hand. So I needed framework to do that safely.

Stephan :

Yeah. And for you, Salvatore?

Salvatore :

And for me as well, it was kind of a natural extension of the work I was already doing to support multisignetor. Like when I was figuring out what is the best way of doing multisignetor, I figured it out. I figured out that a lot of the things that I was doing would actually generalize to more complex scripts. And because the possibilities of using more complex scripts have a lot of potential applications, as we probably discuss, I thought that I should plan that from the beginning, from the get go. And so that has been on the roadmap since we already probably mentioned something like that on the episode last year. But now it’s ready.

Stephan:

Yeah. Fantastic. And so let’s try to make sure we keep it accessible for people as well as we go. So let’s just start with a very basic what is Miniscript?

Antoine :

Okay. Miniscript is a framework for writing bitcoin scripts safely. So it was created by Peter Villa and Andrew Polestra, later joined by Sanket Kanjalkar. And essentially it bridges the gap between what spinning policy you want for your coins and what actually ends up being implemented in the bitcoin script. So value transfers in bitcoin works with these coins that are out there in the open and each of this coin has a value and a small program that is attached to it. And the network is enforcing that. Anyone can spend these coins provided that provides the data, such as the program linked to the coin executes correctly and Miniscripts is going to provide you the tools in order to analyze this program. So it’s going to analyze the spending conditions of the program and also it’s going to give you more information about it, such as suggesting resources. For instance, it’s very important for present transaction protocols to know what’s going to be the size of the spending transaction that you are presigning, because if someone can somehow inflate the size of the spending transaction, it could be a security issue because it could hinder the confirmation of such transaction. Also, it’s going to allow you to analyze well whether this program will be spendable without third party malleability, which is a good thing as well, more for the networks and for itself. But it’s interesting. And so what’s really nice about manuscript is that it’s going to give you your guarantees about this analysis and granting traces these two main concepts that may be a bit complicated but really done it. It’s about consensus, soundness and thunderness completeness. In Bitcoin you have these rules, this consensus from the other network rules and you have also some policy rules or standardness rules. These standardness rules are stricter than the consensus rules. And when we say that the spending conditions that analyze by Miniscript it guarantees that it’s consensus sounds, it means that there is no other way of spending this program, there is no other way of spending this coin of satisfying this program than the one that Miniscript gives you. And standardness Completeness tells you that all these spending paths given by miniscripts are going to be spendable by standardness. Essentially, if you create a coin with this program, you’re not going to get stuck and not be able to spend it. There is no way around spending it otherwise from someone with bad intentions, for instance, and you’re not going to get stuck.

Stephan :

Okay, so let me try to summarize and you tell me where I’m getting it wrong. So just for people who are totally new or relatively new to Bitcoin, you might be used to sending a Bitcoin transaction and we might think, oh, I’m just paying to an address. But really you’re paying into like a script. And in order to spend out of that, you need to satisfy certain conditions. And in Bitcoin that can be things like a time lock, that could be things like multi signature, like multiple people need to sign and it could be like who needs to sign? And so then what we’re doing here with Miniscript, and this is again coming back to what was created by Peter Waller andropolstra and Sankit, is this idea that we can more easily use complex scripting that already exists in Bitcoin today. But this is kind of like a layer that helps us analyze and communicate it to each other, even if we’re using different wallets. Like if I’m using a ledger device and some other software wallets, or if I’m using a spectre DIY or maybe in the future a cold card and that we can sort of speak the same language and more easily analyze the conditions. And so you were mentioning here the consensus Soundness and standardness Completeness. So you were saying with Consensus Soundness you’re saying that there’s no other way to spend those coins than what you’ve spelled out in those policies. And in standardness Completeness, I think you’re saying that basically we’re checking that you can spend out of it, that we’re not kind of burning our coins, right, that we’re putting them into some address that nobody can spend out of. No, actually, let’s say we did a miniscript today and that it needs two out of the three of us, that those are valid and we can’t spend those coins so long as we meet the conditions. Right.

Antoine :

And every branch, every spending condition encouraged by the scripts is spendable and is vetted based on this. So all persons taking part into the scripts can spend as well. So I can try to make a script with both of you guys and then you just get stuck and I can blackmail you if you analyze the scripts with miniscript, miniscript is going to tell you, yeah, it’s safe for all three of you to get into the script.

Stephan :

Salvatore, anything to add here?

Salvatore :

Yeah, maybe the only thing I love to that is that Miniscript is not so much a feature for users directly, but it’s more a feature for developers because it enables so bitcoin already is programmable because you can already program the way you want your money, your coins to be spendable. But bitcoin makes that actually work in practice, so it will be possible to decide the spending conditions in practice, which is something that so far was always hypothesized, but never really done at a large scale and never was easy to do.

Stephan :

I see. And so probably that comes into one of the criticisms. I guess you’re touching on that as well, because some of the criticism I’ve seen online as well, my friend NVK has mentioned, he’s saying he’s kind of said, “all right, we’re going to bring in Miniscript support into Cold Card, but it’s probably going to be something that two users use. And what’s the point of this anyway? Couldn’t I spend that time doing more other things that are practical?” So I’m curious if you have any views on that kind of criticism.

Salvatore:

Yeah, sure. So the way I see Miniscript is that it enables a whole landscape of different things that can now be built on top. Right. So while this can sound very complicated because there are so many possibilities, some of these will be advanced use cases, but some might be even very easy use cases. So miniscript is not something that users will have to handle directly. And while we initially, of course, the first deployments will be on advanced tools for people who are a bit more keen to experiment with new toys and new tools. But there are many use cases where you could actually make self capacity a lot easier than it is today. So the programmability becoming easier will enable both advanced use cases, but also very easy use case where you can help users to do things more easily than before. And we can cover this a little bit more later with some examples.

Stephan :

Yeah, sure. And one other area I’m sure people might be thinking, or they might be concerned. Well, hang on. If I’m going to do all this Miniscript stuff, how do I verify that as a user? That okay? My screen is telling me that it’s a two of three. But how do I know for sure that maybe there’s not some, let’s say, the malicious attacker or the company is building in some unknown pathway that I don’t know about? Like let’s say I think it’s a two of three multisig with the three of us here but actually this malicious company also has their own spend condition that they can just spend on their own. How do I as a user protect myself against that?

Salvatore :

That’s why the possibility to verify what you’re signing and what you’re doing with miniscript on the screen of the device is crucial. So in fact, when you are going to try to use miniscript wallets on a ledger device, the way it’s designed is that before you start using this new wallet that uses Miniscript policies you will have to inspect the policy itself, like the spending conditions. And so this could definitely be a point of friction for the user experience of the user. But this is something that you do only once when the wallet is created while in all the future use cases you’ll be able to use the fact that you reinspected that policy, that maybe you give a name to that policy and you call it cold storage. And so the next time you use the policy the device will just tell you you’re spending from cold storage or you’re receiving in cold storage. So definitely there are possibilities for friction there because these things are not necessarily easy to inspect for the user but we are just starting. So of course there are ways of making these things easier for the user and in the future, for example, we might figure out what spending policies are commonly used by people and so have additional support in terms of UX for those specific policies where instead of showing the miniscript which is a difficult thing to understand, you could name these policies in a more easy to understand language. For example. Definitely there will be a lot of iterations on getting the best possible UX but the only way we can get started is by deploying these tools in a way that’s safe and we start with advanced users.

Stephan :

Sure and so maybe we can summarize that answer as there might be some well known policies or well known ways of executing this and people just kind of stay into those well known pathways. I mean just like today when people sort of they’re operating in certain contexts where maybe they are using a specific kind of wallet, like maybe it’s just a basic wallet, this kind of keep it simple, stupid. So on that topic then, could you explain for us what are some of the use cases that you could see people using Miniscript enabled tooling for like is it inheritance, is it decaying multisig or degrading multisig? What are the main use cases do you guys see?

Antoine :

Yeah, maybe just to get like an antipraised question. People nowadays don’t check to script themselves on their signing devices. So if you use Digbot, you trade a new address, you don’t check the scripts. If you take part into a multisig, you are not going to check the row bitcoin scripts and the check multisigs that is happening on your device. You’re trusting the film of your device to have implemented these templates and Miniscript allows you to do that. But it also allows well it allows developers to use these templates and much more and also it allows you for instance to analyze some bitcoin script on your device and infer the semantic policy out of the row bitcoin script that would be analyzable for a regular user to get back to you the use cases. Obviously I’m biased on the inheritance here. Maybe something else is that we’ve been rebuilt with miniscripts so it was with Multisig as well. It allows having time-locked recovery paths. It follows…sorry something just tolling and some noise. Sorry. Well also maybe what’s very interesting about miniscripts is that it’s composable. So let’s say that the three of us want to get into some script of some sort and that we say two out of us must agree to spending this coin. From there we only think about it with one key per person but it could be one policy per person. For instance, Stephan, you might want your personal policy to be a two out of three between three different type of wallets. Might say if I might want to have some sort of cosigning with the company that I trust and Salvatore might want to just have his own key on the ledger and we can come together and compose these policies. And when we want to agree to spend this coin we do our little things on all sites. Well essentially it makes everything more powerful and composite.

Stephan :

Yeah, that’s an interesting point. So we could also point out that it’s like an interoperability thing. So as an example, if it’s in a company context you might have an individual or let’s say it’s a senior person in the company who maybe has a personal wallet but that wallet can play multiple roles, right? It might be used in a personal context but then it could also be that could also be part of a multisig for something related to the company as well. So I guess there’s like an interoperability benefit that’s basically one idea you’re getting at there, right?

Antoine :

Well what you mentioned is using the same device in different setups and what I was mentioning is more that let’s say that you have a two out of three multisigs and what I was saying is each of the key is actually not a key but a miniscript itself. It’s a script itself and multisig inside a multisig it could be a timelapse recovery multisig inside.

Stephan :

Sorry, you’re right, I think I explained that poorly. But I mean is like you could have your own personal set up and in a way the Miniscript is indifferent to whether I just had one single device or whether I’m having a two of three actually in the background. It doesn’t really matter. As long as I satisfy the condition, the script doesn’t care.

Antoine

Yeah, exactly.

Stephan :

Yeah.

Salvatore :

Okay.

Stephan :

And so let’s talk through some of those uses as well, because I think it’s in I think it would be valuable for people listening just to understand, like, can you just talk through the inheritance idea? So let’s say, as an example, you want to leave some coins to your son, but today you’re still using those coins now. So could you just walk us through what does that look like from a policy point of view?

Salvatore :

Maybe I’ll mention a piece of this one. And then perhaps if Antoine wants to speak more about how what they’re building at Liana, because that’s different. Could be overlapping use case, I guess. So one example that has been done many times for me is, in fact, inheritance. And the reason is that you could have a wallet that you’re using on a day to day basis. But what happened, for example, if you are not able to spend your coins anymore? So that could be because you lost your key, or it could be because, unfortunately, people died. There was a recent talk in the conference in Prague about that from Daniela Bruceoni, and it was exactly about what things you can do to prevent your coins from being lost in case you die. Right. And one thing you could do is that, for example, if you have three children, you could attach to your normal spending policy, which is just your hardware wallet, your key. You could say that after one year, two out of three of your children are able to spend their funds. So in this way, they could automatically inherit the funds without having to go through any different kind of setup. Like past ways of handling that would be that you give them the instruction somewhere. But of course, there are a lot more footguns there because someone might find out the instructions, access to your seed, or that becomes a very difficult problem on how to protect the seed. And you can even go further. Like, what happens if two out of three of your children don’t agree on how to split the funds? Well, then you can add another key, which is with the notary, and it’s only active after two years. And so all these things become possible with Miniscript, and they become possible almost at no cost.

Stephan :

One question just on that. Could you just explain, is that done in a relative time lock way or with an absolute time lock? So in this example, let’s say you’ve got three children. Does that mean from the last time you spend it’s one year from then, or it’s an absolute time lock from the time you started the wallet?

Salvatore:

Exactly. So Miniscript supports both kind of time locks. So you could say that some conditions become active at a specific time in the future, which is the block number, typically. Or you could say that if the coins don’t move for a specific amount of time then some condition becomes active. So in a case like this one that we just mentioned, if you want the condition to be active after one year, then you have to remember every once in a while to spend the coins by sending them to yourself so that you refresh the timer, which is of course, it’s a possible source of friction. But this is also something that can be handled on the UX side from the wallet to remind you to do that or that’s something definitely we can work in the future.

Stephan:

One other question there, would that also blow up the transaction size? Right? Because now we’re dealing with a more complicated script. Does that mean you’re paying more for every transaction to have that?

Antoine:

Not if you use taproot well, much less if you use taproot but yeah, it’s going to increase the transaction size but it’s less going to increase the cost of using it because most of the data is going to be part of the witness data that is currently discounted. So it’s going to increase the absolute transaction size, but the virtual size of the transaction is going to increase, but much less so. And with taproot even much less so, because you only have to reveal part of the script when you’re spending maybe well, this discussion between relative and absolute is something that has come up for Leanna. And it’s very interesting because also one drawback of using relative time locks is that they’re limited to one year and a half, roughly. So the value of the time lock in blocks is only encoded in 16 bits by consensus and so there’s roughly 65,000 blocks. So the maximum time locks that you can use in relative is one year and a half. So that’s not that’s large, but not so large if you want something very, very cold. And you can use absolute ten locks there. Let’s say if you want all five years, like can use an absolute time lock. But then you have to redo your setup every time. Every time you have to recreate a new descriptor to register it on your same device. But hey, if it’s only every five years and also when you want to recover with relative time locks, since you don’t receive your coins on your wallet all at the same time, they are not going to get to be available at the same time by the time you want to recover. So if your heirs are not technical and want to recover or maybe only part of the coins are going to be available at certain height and for the rest of the coins they would have to wait even more blocks. So that can be confusing and it’s something that we are thinking about fully in and also for the use cases the use inheritance is I get one key and I give one key to my heir and it’s time locked. Then there is the multisig that Salvatore mentions that you have, let’s say four out of five. That degrades into three out of five. That degrades in two out of five, let’s say. And then maybe you introduce many more keys at the end, like after one year and a half. And you decide that after one year and a half is 15 at normal, if you didn’t spend the coins, you can say it becomes one out of ten with ten keys that you would have given to many different people to do some kind of social recovery. Maybe because you just decide, by this time, if I didn’t spend it after one year and a half, it means that I basically lost it. So I better be trusting my friends or relatives than losing it completely. And that’s also something that we are thinking about with Liana. Many people don’t want to move from custodial services because of this very low probability that they have from losing their coins. So maybe something that we could do is that okay? Well, the interim is specific for you from losing your coins by having this recovery time locked key to us. That is. In any event, you trust us after one year and a half if you fuck up completely. But if you don’t, you’re always in total control. So you get from something that is fully custodial to something that is 99% non custodial. But in the event of total fuck up, you can still choose to trust the company. And I find this particularly interesting to bring more people to self custody.

Stephan:

Back to the show in a moment. When it comes to securing our Bitcoin, removing single points of failure is important. And Unchained Capital can help you do this by upgrading to multi signature, meaning you have a total of three keys where you hold two and unchanged holds the third key. Now you keep those keys distributed and this can give you that additional peace of mind. So that way, even if your house were to be robbed at night or things like this, you wouldn’t lose your coins because you have used multi signatures to remove single points of failure. And multi signature can protect against a range of attacks. Now, Unchained can help you with this. They have a concierge onboarding program where you can pay upfront, they will teach you, they’ll do a call with you, they’ll send you the hardware if you need it and you can create a vault using multi signature and Unchained can guide you through that process. So if you’re interested in this program, go to unchained.com/concierge. And lastly, Mempool.space is the leading bitcoin blockchain, visualizer and explorer. So bitcoin is a multilayer ecosystem now, so you can see a range of things on mempool.space, whether that is the Mempool, it’s the blockchain or second layer networks such as the Lightning Network. And with mempool.space it is fully open source, you can host this yourself. So if you are with an enterprise, mempool.space offers customized Mempool instances so you can have your company branding your own style with increased API limits, and you can be more closely in touch with the developers and the team for your feature requests. So if you’re interested in that, go to mempool.space/enterprise. And now back to the show. Yeah, so let me summarize that, and I think this is something that it may be controversial for some people, but it might also help more people self custody. So it might be a debate point, but I think there will be some people out there who would otherwise want a custodian. And so this person, this company, let’s say it’s a bitcoin company, and they may want to have this kind of deep recovery key. And maybe, like you said, it’s one and a half years out, or maybe it’s five years out. And so this, let’s say the new or less kind of confident bitcoiner or new bitcoiner who’s maybe not totally comfortable to be fully self sovereign. They may like that comfort factor because they may say, oh, okay, I’m controlling. The coins. But if I don’t spend within, say, one and a half years or five years, then this company has a deep recovery key so I don’t lose the coins. I might just have to wait if I totally lost my keys. Now, that may be controversial, but we’ll see. Salvatore, just nothing to add there.

Salvatore:

Yeah, another exciting use case is that because with multi signature and with miniscript, you can create policies where there are many keys that are participating in this policy. Right. And so why that’s interesting, because different keys can have different properties, for example, in how they are sort of how they are managed. And so, for example, one use case that I’m particularly interested about, it’s imagine you’re a company that actually uses already moved to the bitcoin standard or uses bitcoin on a day to day basis and so it has a spending wallet that they bring with them, right? So they would probably bring with them a hardware wallet, so they can spend from this wallet. And then in that case, because they use that in the field, they still have to be a little bit concerned about this hardware wallet being not hacked. But maybe someone gets to their pin or they observe them while they put in their pin. And so then later, they steal the wallet, and so they manage to access their funds. Right? And so one thing that you can do is that instead of using this as a single signature the wallet, you could combine this with a second factor key that could be hosted on a different machine, either self hosted or even by a service. And this key can be programmed, can be instructed to only sign according to the predetermined policies. For example, you could. Say to this service will only sign at most 0.1 bitcoins per day. Right. So even if your primary key is stolen, then you can put some limits on how much the hackers will be able to steal. And then this you can again combine with additional recovery keys that are in deep cold storage, so that this can be done in a fully trustless way compared to the service, because the service is not able to spend these coins without your help.

Stephan – 00:28:49:

Got you. Yeah. So it could be kind of like a corporate policy thing that limits… it’s like a rate limiter. So it’s like rate limited on this way. But with the deep recovery keys, you can sweep the whole amount out into a safe set up something like this.

Salvatore:

And you could have different people in the companies that have different policies or different and you can do this with different keys and different spending paths that you can all combine with Miniscript.

Stephan:

One other question I have is there may be some privacy ramifications here if somebody wants to operate fully in this kind of mini script inheritance paradigm. Like as an example, you may be a hodler who has got coins from ten years ago and you may not want to spend or move those coins around. So are these Miniscript policies, are they going to apply at a UTXO level? And then so that means if you want to keep those policies active, you’re now going to have to spend all of your coins and common input ownership heuristic right, because you’re going to spend all of your UTXOs together. Does that mean you’re kind of doxing a bit of your privacy to use this kind of thing?

Antoine:

Yes, simple answer. Yes. But it depends. If you are going to use legacy segwid, let’s say P2WSH, then you’re going to reveal scripts. And if you are using a time lock in your script, let’s say, or if you’re using a miniscript at all, because most people don’t, you are going to have a very small anonymity set and even more so that you are choosing your time lock yourself. So even the verity of the time lock, you can actually stick out if you’re using taproot, you’re not going to show on chain that you have this hidden recovery path until you actually need to use it. So most of the time it’s not going to be shown on chain. And I think the question was about the patterns of cycling the coins in order to recycle the relative time looks to restart the clock. Essentially, yes, you could see some patterns that someone that is recycling the coins, but they don’t have to merge all the coins themselves. So it’s a trade off between paying more transaction fees and using one or two coins per transaction. But yeah, definitely you could simply put a button in the future if people are recycling coins. But also what’s very interesting is it opens up a lot of questions about a lot of areas of bitcoin developments using all these new scripts. For instance, with coin selection we don’t have coins for now in Vienna we don’t have automatic coin selection but we’re thinking that during the coin selection process we’re going to have a bias towards older coins so that you don’t have to actually do recycling transactions. Deals off. But when you’re spending, you’re just spending the older coins. So it’s recycled themselves and you break these patterns that could be identified in you.

Stephan:

Yeah. So this almost brings in a new paradigm, right? Because I think historically, at least in the coin control and coin selection world, it was sort of like there were, as an example, people like Merch, right, who will talk about optimizing fees and he has this branch and bound algorithm and it’s kind of like you’re either optimizing fees or some in the privacy world are saying no. Like, do, it all about privacy and you should be very careful which coins you spend and which ones you merge and all of that. So it’s almost like now we’ve got a third paradigm now we’ve got this third paradigm that you may be optimizing for functionality because your tap script or your miniscript is now dictating which coins you will actually choose to spend. Because I might have this old coin that’s about to hit a degrade, a degradation and I need to spend that now because I want to keep it in my control, as an example.

Antoine:

But you could see this functionality as just being future fees. You know that you are going to have to recycle this coin anyhow in the next six months. So you might as well spend it now that you need to make an actual payment, than pay the fees of an entire transaction, an additional transaction in the future.

Stephan:

I see. So there may be some ways you could be opportunistic about it and be like, oh, I was going to spend anyway, I might as well just build in my recycling transaction to the same spend. Therefore my wallet is kind of keeping me in compliance over time or keeping me in the state that I wanted to be in. And now that’s probably also going to be an interesting challenge from both a software and a hardware perspective because then it kind of it’s like how do you remind that user, like, does the wallet tell you, oh, Stephan, your coin is going to come up, you need to recycle it now hit this to reset. How does it work?

Antoine:

Well, we have the UX bugs, I want to know how to call it, but we have analytics on the end and the UI telling, yeah, well, there is only 10% of your timelock duration that is left. You might want to spend this coin to restart the time lock, or the record path is going to be available, but surely there is a huge space for UX and UI optimization from Bitcoin designers. I’m far from being manageable that we could use help on this side. Definitely.

Stephan:

Yeah, Salvatore, anything?

Salvatore:

Yeah, but specifically, I do think that because the design space is so big, the biggest challenges are actually on the software wallet side. There are some specific challenges for hardware wallet that you can touch base later if you want. But yeah, really the UX issue around these things and also, especially when they combine with things like optimizing privacy, I think that will fall mostly on the software wallet user. And that’s why actually hardware wallet support is so important because it removes the bottleneck that has been so far in trying out these things in the wild.

Stephan:

And I think another area that might be interesting is of course there’s going to be commercial services around this. And of course in Bitcoin there’s a strong open source ethos. Is there going to be a possibility for people to self manage? Right, like to not have to use a provider and be able to obviously today we have various node in a package, right? Umbrell, and RaspiBlitz and all of those. Maybe this could be like a module that is like your little self hosting module that if you wanted to run it for yourself and not have to because here’s an example. Like what if there’s like some decaying multisig and a company goes bust or the company that you were relying on as a service provider? They’re not there anymore. Now what?

Salvatore:

Yeah, that’s why this property of Miniscript that you can compose or add additional spending policies is so important. And especially on Taproot, adding an additional spending policy for emergencies comes almost at zero cost. Meaning unless you use it, you don’t pay for it. And so, in this way, you could always add additional keys that you only use for recovery if the main keys that you expect to use in most cases are not available and related to something that we touched before for privacy. Actually, there is one nice property of Taproot that without getting too technically into how Taproot works, but the way Taproot transactions work is that you combine one spending policy, which is just one key together with an arbitrary number of policies that are scripts. And so scripts could be miniscript, for example. And the nice thing is that actually because of the properties of Schnor’s signature argument, you can replace any key with some complicated protocols that do basically multi signature, but only using one key on chain. Right? And so this is nice because in many of these multiparty signing protocols, if all the parties that are participating, they know if you are able to use one of the spending conditions. Right? And so in that case, if you intend to use one of these spending conditions, as long as the participants are available and are online, they can just cooperate with you to use the main spending condition which is the key path and so these scripts will never be rebuilt on chain. So this has huge implications for privacy. And while it will take a long time to develop like that’s, the end goal of where all this is going, in my opinion, to have these spending conditions that they are able to condition how the coins can and will be spent, but in most cases they will not have to be rebuilt on chain.

Stephan:

One other concept that would be interesting just from what I was reading there’s this term Descriptor templates. So can you tell us what is that and why is that useful here?

Salvatore :

Yeah, the idea of using Descriptor templates or something like that has been kind of rediscovered over and over in many different settings. And for me in this idea that I’m developing of what I call wallet policies. The idea came out while I was trying to support multi signature in the best possible way for ledger hardware wallets. But then while realizing that the same problems would apply more general to miniscript, then I tried to make it completely independent from the specific application and make it fully general. So that will work for an arbitrary policy. Right, and so the problem that it tries to solve is the following: there is this language called output descriptors that is basically able to describe all these spending policies that you can use and you can combine that with minuscript that basically extends output descriptors. And so this allows interoperability, because any software that understands Descriptors will now be able to understand how these spending policies work, how to understand how these things should be signed and how these things will work on chain and so on, how to estimate the fees for this transaction and all the necessary things that wallets need to do. But the problem is that there are a few problems though output descriptors are a very general language and so they are a bit too general, meaning they can describe sets of scripts that are not how typical software wallets actually manage the wallet accounts. For example, if you take the typical wallet, let it be single signature or multi signature. The way they handle these scripts is that they generate basically two sequences of possible scripts that correspond to their addresses and those are the receiving addresses and the change addresses. The receiving addresses are the addresses that you will give to someone who wants to send you money. And you try always to give a new address because otherwise people can basically about how you use money. People will able to link payments, right? While the change addresses are basically addresses where you send money back to yourself. Because without getting into how exactly the UTXO model works. But when you spend some coins, you always have to spend them in full. And so if you don’t have a set of coins that matches exactly what you want to spend, what you do is that you send whatever is the amount you want to send to your receiver, and then you send some money back to yourself. And those go into this change addresses, right? And so what a software wallet considers an account is basically a chain of these two chains of addresses, basically. And so wallet policies kind of built on top of descriptors and miniscript by creating a standard language that software wallets can use. And it’s very close to descriptors. So it’s very easy to convert from wallet policies to descriptors or from descriptors to wallet policies that are supported and by kind of forcing the pattern that any way wallets are using nowadays, you avoid using scripts that are not following these patterns unless you have specific reasons to do it. And another reason that wallet policies, another thing that wallet policies tries to address is that more specific to the usage of these things in harder wallets. And so, as we mentioned before, when you use wallet policies, and this is already true for multi signature, when you start using these policies, you need to be able to verify on the hardware wallet exactly how the policy looks like and so that you know exactly what you’re doing. And the reason that’s important is that your computer might have some malware, and if the computer has malware, they could change the policy. And so for the hardware wallet is not enough to verify that your key is in this policy, because if the malware changed the policy, they could control more keys than you, for example, or even in mulit-signature, or they could control enough keys so that you are unable to spend your funds. And so in this way they could ransom you to say, hey, if you want to see your bitcoin again, you give half to me, right? And so to prevent these kind of attacks, you need to be able to inspect policies exactly on the screen of the hardware wallet. So one of the things that wallet policies try, this standard that I’m trying to propose of wallet policies tries to do is to make these descriptor templates as short as possible and also to separate the descriptor templates that kind of specifies the structure of the policy from the public keys, which is another thing that is also part of the wallet policy. But it’s easier to inspect these two things separately. So when you register a wallet policies on a ledger hardware wallet, you will first inspect the descriptor template, which is the policy, which is the structure of the policy, which is like a multi signautre, two out of three or a second factor between my key and some other key. And then on a separate step, you will inspect exactly what are the public keys. So one or more of these public keys will be your own public keys, while some other keys will be from other parties or from some service or something. I’m proposing that as a standard because I believe it solves problems that any hardware wallet implementing these things will have. And plus it makes it a natural language to agree on a common ground for all the software wallets.

Stephan:

I see. Yeah. Because as I understand some of the critiques and maybe going back to what NVK from Coincard was saying is he was saying there’s all this complexity here and so they want to build something safe. They don’t want to put their customers into, as I’m sure you don’t either. Nobody wants to put their customers into like a dangerous position. But then that means there’s a lot of work on the manufacturer, the software engineer to make sure it’s safe and if there’s all this complexity in there. But I can understand from your perspective, you’re saying this is actually something that maybe it helps ease some of that or at least make it easier to assess what is…If I’m the user, “what am I signing on, what am I saying yes to?” And hopefully not being susceptible to a ransom or some other kind of malicious signer attack there. So could we talk a little bit about what it looks like from the software side as well? So, Antoine, could you just walk us through what does it look like, let’s say today on liana. What does it look like today when you want to set up Miniscript?

Antoine:

Yeah, maybe just again to get back and what you just mentioned about the complexity, it’s important to remember that it’s bitcoin that is complex and minuscript that makes it safer to use it’s, not the other way around. We’re not making things more complex than try using minuscript. We make them valuable. Yeah, for two it’s in two parts. Mainly you have to first create your output descriptor, which supports many scripts, and then you can use your wallet. So typically you would run Vienna. It would perpet what we call an installer, where you have to choose the spending policy that you want for your wallets. For now, we only support one primary key and one timelock key. So the installer is very simple. You just plug, let’s say your first tiny device gets the expert from the tailing device, and the installer for the primary key gets the expert for the secondary keys, the time lock key, the recovery key, and you choose the number of the locks before the recovery key becomes available. And then you just go through the steps. It checks your connection to your Bitcoin D and everything that is a regular wallet would do. And then you get to the installer and you can also, from the installer, import a descriptor that you would have created on another wallet and recover from a descriptor. And let’s say if you are recovering from your backup, you input the descriptor, you take your recovery key, and you can sign a recovery transaction. In the future, and sats one of the big UX strategies that we are going to face the installer is going to get much more complex because even at the end of the month we’re going to have the release of multisig. So you will be able to use multiple keys in each of these two passes. So multiple keys as primary keys and multiple recovery keys. And then in the future we’re going to have multiple passes so you can have multiple keys and more than two passes, timelock passes, for instance, filing key and offset. And it becomes quite a mess on the installer. You just put everything on it and not very understandable for the user.

Stephan:

Yeah. And so just on liana then is the idea that you can like, the main wallet is like a hot wallet and then the recovery key is like a hardware signing device or can you just walk us through what you’re currently able to do and what you’re planning to do?

Antoine:

Currently we only support signing devices in Liana. We don’t have any hot keys support. We are going to edit for the next release that is coming up for the end of the month. So the next release is going to have multisig plus hot keys. Yeah, I see it mainly as just make it easier to test it, but you probably don’t want to use hot keys for any substantial amounts anyways.

Stephan:

Yeah, fair enough. And Salvatore, can you tell us a little bit? I’m not sure if this is built into Ledger Live yet or is that coming? Could you tell us what it looks like in Ledger Live?

Salvatore:

No, at this time it’s not a plan to integrate this feature in Ledger Live. It’s more like supporting something for the ecosystem and then people build new things. And one of the exciting things is that because the design space is so big, we already mentioned a bunch of applications, we could mention more and I’m sure one year from now we can look back and people have implemented maybe 10, 20 different use cases that we didn’t think about. Like one example is like a few months ago I learned that this company.

Stephan:

Rob Hamilton’s one, Rob One Ham, and.

Salvatore:

So they were building something to do insurance on Bitcoin, right? And they learned about Miniscript and they just figured out themselves that with Miniscript they can do stuff that is useful for the use case because since they are doing insurance, they can tell the users that they will do insurance on their assets, but they want them to custody their assets with specific ways, with specific policies. Right. So this is not something that I will ever think about, but people will find use cases for these things and people will build useful things that’s my…

Stephan:

Yeah, so I could see, as you mentioned, insurance. Obviously they might want to use that to help derisk the way coins are stored. It could be applied in a corporate context. Right, as we’ve mentioned, the corporate or business context where multiple people need to have access to coins. Like you mentioned, inheritance, maybe even a family, maybe a family might want maybe not today, but let’s say after this has been built out, a family may want to do some kind of mini script policy together and then that way jointly manage their coins.

Salvatore:

Or the simplest thing, how do you defend yourself from a $5 range attack? You can send coins to a wallet that you control but you cannot spend for a year. That’s very simple, right?

Stephan:

So you can have like a panic button, right? You can sort of have an “I’m under attack”.

Salvatore :

If you really don’t plan to spend most of your assets, you could leave 10% out and send 90% to a wallet that you yourself cannot spend for a year.

Stephan :

That’s an interesting idea. And then, I don’t know, maybe you would have some kind of emergency unlock with multisig and things like this.

Salvatore:

Exactly.

Antoine :

What if I come with a branch and I make you precise the transaction that is going to be valid in six months and then it’s basically a race between me in six months and you.

Salvatore:

Well, that’s because since you do taproot, you can hide another spending condition on the script with a different key.

Stephan :

Actually on that, let’s talk a little bit about the Taproot applet aspects because as I understand, miniscript was pre-taproot, right? Like it was created pre Taproot. So what’s going to change in a Taproot context? I know we’ve mentioned it across our conversation, but if you could just summarize for people, what are the Taproot implications of having Miniscript?

Antoine:

You are going to afford using much bigger scripts. You are going to afford from the privacy, but yet let’s say using actual complex scripts because you’re not going to reveal them. And I think it’s the main point of using separate for a regular user is that you can have all these hidden passes, spending passes that you would only use in case of emergency. But also technically it removes a lot of the bounds that represent on the legacy scripts, such as the maximum numbers of operations that can happen in a script. So you can afford having larger scripts and it also removes some malleable vectors in the script by making some rules that were only standardness rules that were enforced by must nodes and the networks, but that were not part of bitcoin by actually enforcing them by consensus. So we can rely on them within the script.

Stephan:

Interesting, because I saw some of the haters were saying Taproot was not really doing much or adding much to the network. But I mean, this is an obvious case where maybe there’s actually new functionality being brought by Taproot. So the Lightning guys are using they’re looking to use Taproot and I know La Lu and the Lightning Labs team are looking to have Taproot channels and they’re working towards that. And this is another example where Taproot is actually bringing a new functionality that could bring all these new features or make it more feasible for people to do. But I mean, the jury is still out. Like we still need to see companies actually building out and making these things. But I think it’s an interesting example of actually here is an actual Taproot benefit.

Salvatore:

Yeah, I have no doubt that use cases on tablet will flock soon, as soon as the tooling is built and people expecting Taproot usage to grow before the tools are built. Well, there is no reason to switch the taproot before the tools are built. You can do the same things on segwid.

Stephan:

Okay, so looking forward, do you have any other ideas on where you would like this to go? Is there any other directions that we haven’t mentioned so far that you think or any other important points that you think about this that we haven’t covered?

Antoine:

It’s a slippery slope because I don’t know much about it, but I guess I’m interested in that. That’s something that we were discussing that before to share with Sarvatore. I’m interested in how covenant would be integrated into miniscripts. So on this side, if some FC more technical listeners want to have a look, andrew and Senkat it have an extension of minus scripts for liquids, for elements and that takes into miniscript some of the introspection primitives that are made possible by the elements scripting system that yeah, that’s interesting. Basically you could say your minuscript you can only spend immediately, but as long as the output at the sequence index in the spending transaction at this value or that, you can only spend after six months if you spend with the transactions that I don’t know as a single input. So you can introspect in the spending transactions. That’s interesting, but that relates also to the governance proposals. What are the limits? What can really be encoded into a Descriptor for governance? For instance, I’m not sure if all the information formats for the proposal could be encouraged in a single Descriptor. If we need more powerful language for this.

Salvatore:

That’s definitely an interesting thing with Descriptors that we are implementing Descriptors today. But it’s not something that is set in stone. Meaning we can always add new features. We can always like if a future soft fork adds new features to bitcoin, then you could expand the future language to implement these new features. And so having this language already available will make it a lot easier to extend the language and roll out new features because there’s always been a pain point like from the Legacy to Segwid, from the switch to Segwid to Taport and so on. Every one of this upgrade has always been very slow in adoption because it was very long and time consuming to build the tooling. While I think now we are getting to some solid foundations that are much more easy to extend and much easier to adopt.

Stephan:

Okay, great. So, yeah, let’s just summarize. We’ve gone through a lot of stuff and I know this is probably a bit more of a technical episode, so hopefully people might have to kind of go back over. But let’s just kind of quickly give a high level summary here. Right? Miniscript is this way of making it easier to assess and interoperate between wallets in terms of Bitcoin scripting and make it so that maybe you’re less likely to have like, a vendor lock in, right? Because you can have Miniscript and it’s like cross compatible in a way so that’s useful, that’s handy and it makes it easier for engineers and entrepreneurs to build something out in a that would have previously been too complicated or maybe that was in the too hard basket before. Whereas now, with minuscript, some of these ideas become feasible. And maybe it makes it easier to do this inheritance planning, time locking business context. So I guess that’s kind of how I would summarize it. Do you guys have any other closing thoughts? Why should listeners care?

Antoine:

Closing thoughts? Maybe something that we didn’t touch on that’s important output descriptors. Even less and especially less technical listeners should look into output descriptors. It’s a way of making your backend explicit, because the recovery process in Bitcoin is not only about being able to sign for a coin, it’s about being able to locate the coin in the first place. In the UTXO set, when I took this analogy, the value transfers in Bitcoin being just coins in the open with value and a program attached, there is about 80 million of these coins. Roughly. If you do not know in what scripts your key was used, your key backup is useless. And frankly, we rely on implicit information. It’s good enough in most situations that when we’re talking about people’s money, most is not enough. It’s output descriptors way of making these backups explicit so that you know where your key was used and you have your private key to sign for the coins that you located with the backup. So, yeah, closing starts looking to backup output descriptors and try out Liana. And we need designers for Liana. It’s going to be an S for the installler.

Stephan:

Salvatore?

Salvatore:

Yeah. My closing thoughts. So we all got excited listening to Andreas Antonopoulos and mentioning how Bitcoin is programmable money. And I think Miniscript changes that from programmable in theory to programmable in practice. So Bitcoin companies, I think everybody should look at Miniscript and what Miniscript can do for them.

Stephan:

Fantastic. Well, thank you guys for joining me. I’ll put all the links in the show notes, so thanks, Antoine and Salvatore.

Antoine:

Thanks for having us.

Salvatore:

Thank you.

Stephan:

So what do you think about Bitcoin mini script? Is it too early? Is it too complex? Or will it actually help things and make it better for us in Bitcoin? Get the show notes at stephanlivevera.com/452. Thanks for listening and. I’ll see you in the Citadels.

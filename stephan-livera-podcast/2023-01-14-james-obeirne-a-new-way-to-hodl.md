---
title: A New Way to HODL?
transcript_by: Stephan Livera
speakers:
  - James O'Beirne
date: 2023-01-14
media: https://www.youtube.com/watch?v=Nq6WxJ0PgJ4
---
podcast: https://stephanlivera.com/episode/449/

James, welcome back to the show.

James – 00:02:46:

Hey, Stephan, it’s great to be back. I think it’s been almost four years.

Stephan – 00:02:50:

Damn. Yeah, well, in terms of on the show, yeah, actually in person, you know, a couple of times, some of the conferences and things. But I know you’ve got this awesome proposal out, and it looks pretty interesting to me, and I’m sure SLP listeners will be very interested to hear more about it. So do you want to just set the background for us? Where did this whole idea come from?

James  – 00:03:12:

Yeah, sure. So I think everybody knows that custody in bitcoin is really hard, and pretty much everybody’s major fear on bitcoin is waking up one day and checking your wallet and seeing that somebody’s gotten away with your coins. And so a lot of thought has been put into things that can mitigate the risk of losing your coins and especially kind of having experienced an industrial custody context at a few different places. There’s been an idea circulating for a while of this notion of a vault. And the idea of a vault is basically that you can lock up the coins in such a way that if you want to move them in general, you have to wait for this delay period. And during the delay period, you can kind of contest the spend, aside from spending the coins into a prespecified recovery path. And so I think the first time that vaults were really discussed was in a paper, I want to say in 2014 or 2015. It’s a paper called Bitcoin Covenants, written by Malte Moser and Emin Gun Sirer. And it’s kind of an interesting paper because they formalized sort of the notion of bitcoin covenants, which had been kind of mentioned by Greg Maxwell in a bitcoin talk post back in 2013 in actually a very derogatory context. But these guys formalize it into a paper, sort of, and it’s a weird paper because they spend the first half talking about vaults and then, like, the second half talking about how they can repurpose this covenant stuff to make bitcoin and g. But it’s worth the read if you’re interested in vault. So anyway, they sort of discussed in the abstract this idea of how you could put a constraint on not only just unlocking a coin and spending it to some arbitrary destination, but you could put constraints on how the coin is actually spent, and then you could use that to reify this idea of a vault.

Stephan – 00:05:19:

Got you. So let’s just take one step just to make sure everyone’s following along, right? Because I think I’m following you, and I think obviously you understand this. But just to make sure listeners are following along let me put it this way, or you correct me if I’m getting this wrong. But the basic idea is when you have probably people are used to this idea of sending bitcoin from one address to another, but really what’s going on kind of under the hood is that address it can contain a script. And you can think of it like we’re locking coins into a certain script and we need certain conditions to unlock that coin and spend it somewhere else. And so what we’re talking about here is like using script in a special way to create this special vault construction that gives us maybe a little bit more confidence about if something were to happen that I could then stop the theft of my coins, let’s say, by pulling them into a different recovery address, let’s say. Is that high level, what we’re talking about?

James – 00:06:14:

Yeah, that’s exactly right. Just to restate, when you’re sending your coins somewhere, quote, unquote, what you’re really doing is you’re spending a coin, which involves presenting a proof or an input to basically a little computer program that had locked the coins. And that input gets fed into that computer program. The bitcoin script engine executes that program with the inputs. The inputs are now called witnesses. And then if that execution succeeds, then you can basically lock the value up with another computer program. And in bitcoin today, right now, if you successfully unlock that first computer program, you can pretty much spend the coins in whatever way that you want. But this idea of covenants is that, okay, maybe you’re presenting a proof. Well, you’re definitely presenting a proof to unlock the coins in the first place, but you might then put them under a certain kind of computer program, a certain kind of locking script that looks at something beyond just a signature to unlock. Maybe it looks at the structure of the transaction that you’re spending it into. And so this is a very general and very powerful idea, and for a long time maybe we can talk about this later. A long time, people were very worried about that idea enabling something like government, you know, control of of coins, but that actually turns out not to be any kind of a concern, really. But basically you can use this really powerful new ability to do something like vault, which just exactly what you said is this idea. Let’s say someone gets a hold of the key that you use to do this unvaulting process, right? They start to try to move the coins, but because you’ve locked the coins into a vault with a delay period, they have to wait, say a day or week or maybe even a month to move the coins. And then in the meantime, you have some very trivial system or program that’s monitoring the chain and sees, oh wow, I just saw an attempted spend on your vault. Did you expect that? And if you didn’t expect that, you can jump in and immediately sweep those funds into a recovery path. And so the idea is that if you get the tooling right, this makes bitcoin theft exceptionally difficult. Because what it allows you to do and let me know if I’m jumping the gun here, but it allows you to generate the keys to this recovery path in a completely different way and perhaps a very sort of impractical or operationally difficult way than your sort of everyday keys. Right? So you could do a completely offline key generation. You could generate the keys in such a way that they would be almost like useless for use in a multisig quorum, which is what people do now to secure their coins. They have maybe a multisig quorum with a few different kinds of keys or devices and that’s great. But if you’re talking about super, super cold storage, you just kind of can’t use that every day in a multisig quorum to spend coin. But with vault, your recovery path could be that like ultra cold path. And so I think between that and sort of the ability to intervene if someone does capture your unvault keys, which definitely could be multisig or could be really any kind of bitcoin key arrangement, it’s a very powerful combination.

Stephan – 00:09:54:

Got you. Yeah. And so can you just explain for listeners who are the typical users here, are we thinking of like, big institutions? Are we thinking of, let’s say, a family office with a lot of coins? Or are we talking even like DIY hodler, average stacker guy is going to use this kind of set up? Or is it even like to the level that you might have like a mobile phone, bitcoin wallet with a vault kind of set up? Could you just explain who do you see as the primary users here?

James – 00:10:23:

Sure, yeah. So when I started thinking about this stuff, I was really kind of a moron personally with my own coins. I had a single SIG with a passphrase, basically.

Stephan – 00:10:33:

That’s a reasonable set up to dox myself.

James – 00:10:35:

I mean, yeah, it’s pretty low tech, right? But like I said, I was sort of in an industrial custody context, or at least was exposed to one. And I was really, really trying to think about how to de risk those operations and vaults were known at the time, but the problem was with the existing vaulting strategies were that, like, they’re just operationally extremely difficult and we can talk about that in a little bit. But what I really love about this proposal is that it kind of hits the full spectrum. I think everybody from kind of the biggest custody operations to individual hodlers. It’s very easy to use this new construct of a vault. Like the user interface, if you will, is like very, very simple, but flexible enough to sort of accommodate any use case. And that’s in large part due to the power of covenants.

Stephan – 00:11:35:

I see. Yeah. Okay, so your paper also mentioned so talking about covenants as well, your paper mentions two kinds, so it’d be cool if you could explain that. So we have the precomputed and general so could you just explain what are those?

James – 00:11:47:

Yeah, sure. So again, the idea of a covenant is that you are encumbering coins not just on the initial unlocking script, but you’re actually encumbering them on the basis of the transaction that the coins are going into. And so what that means is you have two options here. You could either do something where you basically pre compute like a tree, all possible paths of how these coins can flow through this vault thing over the lifetime of some number of transactions, or you could encode a more general program almost in the script that is not bounded to a particular number of transactions. And the second is significantly more powerful, obviously, because you could, for example, have a vault where you can partially unvault as many times as you want, revolt and so forth. But the difficulty there is that up until now, all of the techniques for doing this general covenant thing were sort of complicated and scary and well, maybe the techniques themselves were not complicated, but they resulted in these scripts that were really complicated. So an end user, to use one of these general covenant techniques, would have to write a very long or relatively long and complicated bitcoin script. I mean, it’s like if people out there are familiar with the difference between assembly language and, say, Python, if you’re writing bitcoin script to do something like what Op fault does, you’re essentially writing like assembly language versus calling some Python function. But these precomputed faults are still very useful, and I think specifically in the case of a proposal called Check Template Verify that Jeremy Rubin and others have worked on that’s still a very useful construct for a variety of things. And the idea there, again is you’re sort of saying, okay, I’m going to lock up these coins into a predetermined flow of transactions, but I know that at some point that flow of transactions will terminate and I’ll just kind of get regular coins out. But the problem with that is that you’ve got to pre anticipate all the different ways that you want to spend. And so if you’re talking about vaults, that introduces certain limitations.

Stephan – 00:14:29:

Yeah, got you. And your paper also calls out this idea that as an example, there’s this issue, similarly with Lightning, of understanding what’s the fee rate now when we start the vault, and then let’s say in five years time when we unvault, the fee rates could be totally different. And I understand in Lightning they have this concept of an anchor output. And I know from the paper you also mentioned a similar kind of idea of anchor ephemeral anchors. Yes, ephemeral anchors. So could you tell us a little bit about the goals, I guess, like, what is a good vault proposal going to look like?

James – 00:15:01:

Yeah, so I think there are certain features that a vault should have. So I guess maybe by way of comparison, do you think it’s worth talking through how sort of the most basic vault implementation with pre signed transactions work?

Stephan – 00:15:17:

Yeah, sure, let’s talk about that and then kind of look at what’s the difference with up vault.

James – 00:15:22:

Yeah, because I think it’s hard in the abstract if I start describing features of vaults, they’re kind of like abstract. And so I don’t think they make sense until you kind of see the alternative. But right now, if you want to do one of these vaults with Bitcoin, what you would do is you would generate this one time key that you intend on throwing away and you would send your coins into some transactions that are controlled by this one time key. And then you would use that key to sign a few sort of pre-formulated transactions that essentially lock the spend paths into these transactions that you’ve generated. Does that make sense?

Stephan – 00:16:05:

Yes. Got you. So it’s a very critical set up step. And then you also want to make sure that key never gets compromised because you’re done if that key gets compromised.

James – 00:16:15:

Yeah. As a user, if you do this set up ceremony, you better hope that the key was actually deleted because then someone has the ability to spend these funds that you think you vaulted but you actually didn’t. And in fact, key deletion is notoriously sort of impossible to prove. And this is especially a concern in an industrial context where you might have to prove to auditors that you’re doing everything right. So for both individuals and companies, it’s pretty tough. So the setup ceremony can be fairly onerous for something like this. And then along the lines of what you were mentioning a few minutes ago about fees, because you’re pre generating these transactions, you’re locking yourself into some set of fee rates, you’re locking yourself into the set of destinations that the funds can be unvaulted to. And that might mean that you have to use some kind of intermediate hot-ish wallet to actually route the funds after you’ve unvaulted them. And so there’s still value, perhaps, in doing this kind of a set up, because, again, it gives you that delay period where you can contest a hacker trying to spend your coins. But there are all these operational considerations. And you have to think about a whole lot upfront, do everything right operationally, and then kind of hope that you’ve chosen the right, say, fee rates to pre generate. And this is really how the development of this started out for me, was sitting down. I didn’t intend on writing a software proposal, to be honest with you. I almost wanted to come up with a thought experiment about what the perfect vault would be. And so for one, I think for the perfect vault, you can have multiple deposits to the same vault. With this pre signed approach, you basically create the vault that you’re going to create and then that amount is sort of fixed until you withdraw it’s like.

Stephan – 00:18:16:

A one time deposit rather than multiple deposits, let’s say.

James – 00:18:20:

Yeah, exactly. Whereas I thought you should be able to choose these vault parameters and then just kind of deposit so that, for example, if you want a DCA on an exchange, say every day, and you want to have that withdrawal go immediately into your vault, you should be able to do that without any kind of operational headache. So that’s one another is this idea of having a dynamic vault target. I’m sorry, a dynamic unvault target. And what that means is when you want to go to withdraw from your vault, instead of having to lock in some fixed intermediate wallet that you’re withdrawing to and hoping that that doesn’t get compromised. Because if that does, then you’ve got to sweep to your recovery path, which is probably a big pain to actually go and access, if you could actually just pick where you wanted to withdraw to and then start the unvault process with those parameters. So this dynamic unvault target allows you to do that, then the other thing that you want, that’s probably just nice to have. But this idea of doing partial unvaults where you’re not moving the entire balance of everything that’s vaulted at once, you’re just kind of peeling off some amount to unvault at a time.

Stephan – 00:19:42:

Got you. Right. So you could have like a big saving amount and okay, that bitcoin has gone up so much, I want to peel a small amount off and buy a house for the family, but keep the rest in the vault that kind of set up or that kind of use case, let’s say.

James – 00:19:54:

Yeah, exactly. And then the final thing that you want, which is kind of an implication of the dynamic targets, is this idea of batching. Batching is really, really important because if you’re generating all these vault outputs, then you don’t want to have to generate unvalued outputs for every single vault that you create because otherwise, let’s say that an attacker gets hold of your hot wallet keys or your unvault keys, then they might start to withdraw. Could be thousands and thousands of vaults depending on your scale of custody. And so in a case like that, you want to be able to sweep to the recovery path as efficiently as you possibly can in batch. And so that’s one of the big innovations of a vault, is that it’s the only proposal to date that actually enables this.

Stephan – 00:20:45:

Got you. So to be clear, in this case, this is more useful for, let’s say, a professional large scale custodian who is perhaps managing thousands of vaults and maybe not as useful for, let’s say, the individual hodler just doing one vault for himself, right? Am I understanding you right there?

James – 00:21:01:

That’s an interesting question because if you want to allow people to, let’s say, deposit to these vaults on a daily basis. The only way that you can actually have multiple deposits like that work is with separate UTXOs. And so at the end of the day, you’ve got to spend those UTXOs. And if you don’t have Batching, then that becomes a very inefficient process with a Vault. So naively, yeah, it does look like this is only a big deal for big custodians, but it’s really not. It’s a big deal for any user of Vault, I think. And so this idea of Batching, I think without it, it’s very hard to make vaults a practical thing.

Stephan – 00:21:43:

Got you. And just out of curiosity, even today there are limits on how many UTXOs you can have in one transaction. Right? I don’t know the exact number, someone correct me, but it might be like 100 or maybe more, maybe a little bit more. So let’s say this Stacker has been stacking, you know, once a day for years. He might have like 800 outputs or something, right? And so even that would have to be, let’s say, broken down into chunks that are actually doable.

James – 00:22:08:

Absolutely, yeah, absolutely. I mean, you’re still sort of hitting the same problem if you’ve got, let’s say you’re doing your daily DCA and you’re creating…

Stephan – 00:22:17:

yes, to be fair to you, that’s a problem already today. So you could be really screwing yourself over if you’re not careful about how you manage your coins today. So we’re not going to ding you for that or anything, but yeah, that makes sense. So let’s talk a little bit about the relation of this with some of the other ideas that people have been talking about. So, as you mentioned, and I’ve got an episode with Jeremy Rubin talking about CTV probably a year or two ago now. And at the same time that the CTV drama happened, I think there was also there were other proposals. Right. I think Rusty from Blockstream had another idea. I think it was Op TX hash. And then some other people were talking about a combination of I think it was checksig from Stack and Cat, which could do something as well. So could you just talk a little bit about the relation with Vault up Vault as opposed to some of the other ideas?

James – 00:23:07:

Sure, yeah. So I think a lot of people have realized that bringing covenants into Bitcoin somehow is a really, really good idea, perhaps even essential, if you think about the need for things like coin pools to actually scale at UTX ownership. Certainly vaults, I think, is increasingly seemed to me to be an essential thing for custody. But, yeah, this problem of how to actually bring covenants into bitcoin in the right way is very, very thorny. Because not only do you have the option of doing, say, precomputed covenants, which are sort of simpler versus these general covenants, but then even within those two categories, you’ve got a whole number of different options for actually implementing this stuff. And so the design space there is wide open and there are a lot of different proposals, each of which has certain limitations and certain advantages. Check template verify, for example, is very, very simple and I’ve reviewed it in depth and I think it’s a safe change for bitcoin. But it does have certain limitations, mostly in that you have to actually pre compute this graph of transactions. So anyway, to step back, solving the general covenants problem is kind of like a holy grail at this point and it’s really, really difficult. Vaults in particular are just a use case of covenants. They’re kind of like a subset of the covenant functionality. And so one of my ideas here was instead of trying to solve the general covenants problem, which a bunch of people have done, and it’s kind of a quagmire at this point, I figured I just want to do as good a job as I can on Vaults, and maybe that requires some covenant like behavior, which it turns out it does.

Stephan – 00:24:53:

Back to the show in a moment. Blockstream are creating a community for bitcoin builders. It’s called build on LTwo. So the Build on L Two initiative, it’s a community led effort where contributors and companies building on core Lightning and the Liquid network can come together. It’s an interactive community platform and this could be useful for you whether you are a builder, a product manager, a designer or an engineer. There’ll be events, there’ll be mentorship programs to fast track your success and you will have a community space to learn something new alongside other bitcoin is building on the future of bitcoin layer too. So go and sign up. It’s over at Build on L two.com. When it comes to securing our bitcoin for the long haul, Unchained Capital can help with multisignature. Multisignature means you are putting your coins into a place where it requires multiple keys signing to move those bitcoin. And so this can give you massive improvements in security compared to single signature setups. Now, Unchained can help you with this process. They can make it easy for you, they have a concierge onboarding and you can have the hardware shipped out to you. You can have a call to set you up and to withdraw the coins out of your single signature wallet or out of an exchange or a custodian into keys that you control. And Unchained can’t stop you from controlling your bitcoin. So that’s a really cool feature. If you’re interested in that, go to Unchained.com/concierge and use code Livera for a discount there. And now back to the show. I see, so maybe it can be interpreted as you’re trying to thread the needle here in terms of trying to solve this grand, grand problem of trying to do the whole covenant shebang, but trying to give people the specific thing that’s needed for people to be able to vault and unvault their coins. Is that a fair summary?

James – 00:26:32:

Yeah, absolutely, exactly. I was excited when I finally understood check template Verify and worked with Jeremy a bit and actually developed a prototype of implementing vaults within CTV. And the advantage that you get there is that you don’t have to do this really precarious ephemeral key thing where you generate the one time key and then throw it away. CTV just kind of enforces the covenant on chain, which is great, but you still have the problem of dealing with fees because with CTV, because you’re pre computing the exact flow of transactions and then committing to it in a hash, kind of like merkel trees, if people are familiar with that, you have to pre specify the withdrawal paths. The recovery paths. Well, I guess you have to specify the recovery paths in any case, but the fee rates. And so it’s an improvement for sure over the pre signed transaction implementation of vaults, but it still left me kind of wanting in terms of functionality.

Stephan – 00:27:42:

I see. Yeah. So basically you see it like Vault offers a different functionality to what CTV was, but it’s not the full covenant thing.

James – 00:27:50:

Exactly. CTV is much more general than Op Vault, but Op Vault has some behavior in there that CTV can’t do. So it’s not like one is a subset of the other, if that makes sense.

Stephan – 00:28:01:

Got you. Yeah, that’s totally fair. And so could you tell us a little bit about just the life cycle of this process then? Let’s say we had a vault. What does it look like to start a vault transact or even do, let’s say, a partial unvaulting, and then at the end you’re closing down the vault because you’re passing it on inheritance scenario or something like that. If you could just talk through a lifecycle there.

James – 00:28:24:

Sure. Yeah. So when you’re creating a vault, all that means is that you’re unlocking some coins that you have control of, or getting someone to send you some coins to what’s called a script pub key. The script pub key is basically the name for that puzzle that you have to solve whenever you spend a coin. And the contents of that script pub key contain an opcode op Vault, say, that has three parameters. The first parameter locks you into a certain recovery path, so that determines what your super cold key is going to be. The second parameter is the spend delay, which is just a number. It works exactly in the way that check block time verifying check, I’m sorry, check sequence verify works in that you can specify a relative delay in terms of either time or blocks. And then the third parameter that you give it is the unvault key. And so that’s basically like what’s the mechanism that I’m going to use to authorize the start of the unvault process? So once you have that script, you can just send UTXOs to be encumbered by that script kind of as much as you want. And at. Any time, you can sweep those vaults into the recovery path with no delay whatsoever.

Stephan – 00:29:51:

Got you. Yeah. So it’s sort of like a watchtower. You sort of need some kind of watchtower, like feature, kind of like Lightning, this idea of a watchtower that you’re watching to see, oh, somebody spending my coin. Oh, quick, I need to use my recovery key to kind of but I know I’m safe as long as I have the watchtower that detects it within a certain time period, right. Depending on how many blocks we set that time lock. Right. And so then, as I understand, then the idea is, let’s say I put some coins into my vault. I see, oh, look, someone’s stealing from me. Okay, let me recover those coins into my recovery pathway, because the hacker guy is he’s encumbered by the time lock, but I am not. I can just pull it straight out to my recovery key. Is that the scenario that’s the set up?

James – 00:30:35:

Yeah, that’s exactly right. If you want to start the unvault process, then you send some amount of the vault into the script that’s op unvault with the exact same parameters, except instead of specifying the unvault key, you’re specifying the target hash, which basically locks you into, where is this withdrawal proposing to go? And just as you said, what you want when you’re using Vault is some kind of a watchtower. And what’s nice about the watchtower for vault is that it’s exceptionally simple and you can do it in a variety of ways under a variety of trust models. So, for example, let’s say that I don’t want to run this watchtower myself, but maybe I’m comfortable with the watchtower company knowing which outputs I have. You can tell them what the outputs are to watch, and then they can alert you if those start to move. And then you can make the judgment call whether to intervene or not. Or maybe I want to give them my recovery pathway, and then they can just scan for any movements associated with that recovery pathway, and then I can give them the recovery transactions, and then they can broadcast that’s, putting a bit more trust in the watchtower. Or maybe I don’t trust the watchtower at all. I can give them some kind of probabilistic data structure that might tell me if my coins are moved or kind of like a bloom filter. They might give me some false positives for whether the coins are moving, but the watchtower can sit there, and then I can get an alert from them about maybe your coins are moving, and then jump in and check myself. So the point being that there are a variety of ways to run these watch towers, and they’re very, very simple things.

Stephan – 00:32:19:

And so one other question with the recovery pathway. So is it the case that, let’s say you are a big custodian and you are managing thousands of vaults for thousands of customers? When you have to do the recovery or to kind of you see that there’s a hack? Does that mean you would need to now pull all of them at once or can you? Individually? You get what I’m asking.

James – 00:32:39:

Yeah, absolutely. So it depends on whether the vaults share a recovery path. And in practice I think what you would do typically is you would say, okay, I have my ultra cold key, I’m going to take the xPub of that key and then just generate different recovery paths as needed so that they’re all locked by the same super cold key. But you’re getting different recovery paths because exactly as you’re saying, what happens is when you sweep one vault with a given recovery key because there’s no additional authentication or authorization required to actually do that sweep, anybody might be able to come along and just kind of replay that sweep against vaults that share that recovery path. Now one proposed change that I’m kind of noodling on after putting the initial release of this out there, getting some feedback from the other devs is one option is, you could actually give some flexibility around how the recovery path works. So right now I just say, okay, if the coins are headed into the recovery path, it’s valid, let’s do it. Another option would be you could do that or you could decide to say, you know what, actually this recovery path is protected by another key that I have to sign with and so you don’t have that replayability problem. So that option would introduce a little bit of flexibility but then it makes it a little bit more complicated to decide for vault user what they should do.

Stephan – 00:34:10:

I see. Yeah. Okay. So with the unvault process, like the normal unvault process that still allows you to specify a different address, let’s say like a new address it received the vaulted coins out into, but it’s just the recovery path has like specified pathways. Does it?

James – 00:34:30:

Yeah, exactly. And the idea there is that when you set up the vault you want to say this is the only way to recover these coins because that’s a special ability to be able to sweep all of the value into one path. So, yeah, the recovery path is prespecified and completely static. But the recovery path could be like, say, a Taproot script where you could do something where you say, okay, my recovery path is that within six months I can spend it or I can spend it immediately with my super, super cold keys, or after six months, I can spend it with this backup set of keys. So you can do anything that Taproot allows you to do with the recovery path, which is a huge range of flexibility.

Stephan – 00:35:17:

I see. Yeah. Right. So because of that Taproot idea with the public keyspend or the script path spend, you can set up different scenarios and people are talking about this idea of having, let’s say like a degrading set up, right like that after a certain amount of time that only two out of whatever five keys or whatever keys could spend. One other question I had as well, is there’s this idea in your paper, it’s saying being able to sweep to the recovery key at any point with no witness data. Does this just push the problem back one step? Like could the criminal or the hacker just try to find out the recovery key or hack that part? Is that just pushing the problem back one step?

James – 00:35:59:

I would push back a little bit because they have to figure out two things. Well I mean if they compromise your sort of backup recovery key then yeah, totally. They can generate the data necessary to sweep all the vaults and everything. I think the idea here is that we all know, at least in theory how to generate a really cold key. It’s just that oftentimes we don’t do that because it’s very inconvenient and basically inaccessible. But yeah, if someone finds your just in the same way that if someone right now kind of discovers your keys, your host the idea here is that this just allows you to kind of like segment that process from sort of the everyday operation of spending coins and it gives you some granularity in security, if that makes sense. But please push me on that if it doesn’t make sense.

Stephan – 00:36:54:

Yeah, no, I think I’m getting you there. So I think the way I’m seeing it then is it’s sort of like you could have this separate set up with much harder to access keys than what you are normally using. But I guess today, nowadays, let’s say if you’re like a serious hodler with lots of coins or maybe you’re a company, you might have today a hot wallet with a small portion of your coins and a cold wallet with some big, big multi SIG or just keys distributed and all this kind of complicated stuff. So I guess that’s kind of what people are doing today. But in fairness, not everybody can use multi SIG today. Now of course there’s my sponsor on Unchained capital and there’s specter and sparrow and all this stuff out there. But I think in practice and I think that’s where your proposal is getting at is like this idea that it could give the benefits of multisig for people who currently do not have the either technical means or the comfort to use multisig today. And that’s where I’m seeing it at least.

James – 00:37:52:

And then, I mean in an industrial context, multisig can be very troublesome. Getting together enough of a signing quorum, that means managing a diversity of teams and devices and it’s really a lot of kind of amortized overhead for the operation of coins. Whereas with this you can have sort of a streamlined setup for spending and then if something goes wrong with that setup you can just fall back to a really secure system. But kind of on a day to day basis you can have something that’s really secure whether that’s kind of a lighter multisig or some kind of shame of secret sharing or MPC thing. But it’s just easier to use than having a single multisig configuration that’s both extremely robust but also kind of permits spending. So it makes sense to me that you want to segment kind of the security model a little bit for those two.

Stephan – 00:38:53:

Okay, yeah. Can you also explain the reliance on package relay? Because that’s something also mentioned in your paper. So if you could just give like the super high level of what package relay is and then explain the reliance there.

James – 00:39:05:

Yeah, sure. So package relay is the pretty simple idea that if you have a number of unconfirmed transactions that depend on one another, you should be able to relay those to the peer to peer network and they should be able to travel together and have a kind of aggregate fee rate that allows nodes to say, okay, well, this parent transaction has a really crappy fee rate, but the child transaction pays a ton. So if I mine them together, I actually get a very attractive fee rate. And this is important because pretty much any second layer contract application for bitcoin involves sort of pre specifying a fee rate at least. So in Lightning, for example, what they do is the commitment transaction has some fee rate itself, but then to support dynamic fee adjustment during settlement time, there’s an output that anybody can spend that they call the anchor output. And this allows you to do child pays for parent. But things kind of get into trouble if you don’t have package relay because maybe the parent is so low fee that it can’t even broadcast to land in the mempool to get bumped by the child. So anyway, package relay is very important and pretty much everybody wants it. Gloria and others are working on a proposal there and it’s looking like it’s going to come along pretty shortly. But the long and the short of it is that package relay just allows us to do dynamic fee adjustment in a way that lets us kind of not worry about potentially getting typhooned by the Mempool fees.

Stephan – 00:40:46:

Yeah. And for anyone who’s interested, I have an episode with Gloria talking about package relay, of course. And one other question I’ve got, is there’s a bit more chatter about Miniscript right now? So I’m curious, does Miniscript play into this at all? Does it help? Does it not help?

James – 00:41:00:

I’d say it’s sort of unrelated. Like if a vault wound up making it in, there would be a Miniscript, I don’t know what they call them, function for a vault, not unvalt. But what’s nice about op vault is that the opcodes are very, very simple and the resulting scripts are very, very simple. So typically Miniscript is a big benefit if you’ve got some kind of relatively complicated I mean, using multisig and bitcoin script is cumbersome to say the least. And so something like Miniscript there, if you’re composing things with time locks and multisigs and making very complicated scripts, Miniscript is a huge win. I think it’d still be great for out fault, but the Miniscript and the bitcoin script for outfall look very similar.

Stephan – 00:41:46:

Got you. Yeah, I’m with you. So it helps, but it’s not a huge win. Okay. And then actually one other question I had was around one of the, I guess critiques, let’s say, of the general Covenant schemes, because I think in your paper you also mentioned that it wouldn’t be suitable because it would result in very bloated script pub keys. So could you just explain that a bit?

James – 00:42:07:

Yeah. So again, general Covenants give you this very low level machinery to essentially write computer programs in script that determine the spend path of the coins. And because you’re articulating something like a vault in bitcoin script, to get the equivalent functionality of what something like vault provides you, you have to write like really long, really complicated script. And a lot of people have proposed these general Covenant mechanisms, but I haven’t seen a lot of actual end uses of them because I think the resulting scripts are just so gnarly that they make the proposals kind of unattractive, at least for me personally. And then the other problem is, let’s say that you have one of these general Covenant mechanisms and someone devises, they go to the time and write this giant script that does everything that you want and everybody wants to use it. Well, now you’ve got everybody kind of doing the same thing, but they’re bloating the chain space with the same exact script. That’s really big. So I think kind of the bull case for General Covenant stuff is that it allows end user experimentation and you don’t have to get a soft fork done if you want some new big piece of script functionality. But I think in actuality, if you had something like that and some exciting use comes along that’s relatively complicated, you’d really have to soft fork it in at some point because the waste would just be so much in terms of the witness sizes.

Stephan – 00:43:49:

Got you. Okay. And so one other question. Is there anything specifically enabled by Taproot here or not?

James – 00:43:56:

Not really. This could have as easily been done with bearscript or paid a witness script hash. And indeed, the way that it’s written right now is it’s kind of compatible with anything. It’s not Taproot only. So I mean, Taproot certainly helps, but I wouldn’t say the two are directly related.

Stephan – 00:44:18:

Yeah, sure. I saw from the mailing list, there was some interesting discussion. I think Greg Sanders had this suggestion and you were commenting that this could allow all the outputs to be paid to Taproot. So that could be maybe some small privacy benefit there.

James – 00:44:34:

Yeah, I think so. I’m trying to think through that one because originally when I wrote this, you could do the vault output any way you wanted, so Taproot or Segwit version zero. But then when you went to spend it into the Op unvault output to sort of trigger the start of the withdrawal process, that had to be a bear script, because when the script interpreter is looking at that Op unvault output, it’s saying, okay, is this compatible with the Opvault it’s spending? And mostly due to my own inexperience, I was just like, okay, well, it needs to be bare so that we can read it directly. But when I put the design out there in the code, Greg Sanders came back and said, hey, if you just stick this extra little bit of information in the witness, when you’re spending the out vault, you can actually support doing the op unvault in any kind of address type or any kind of script hashed address type. So that was a big improvement. I actually implemented that and pushed the code last night, and I think that’s a big upgrade.

Stephan – 00:45:34:

Okay, fantastic. And any other feedback you’ve received on the proposal so far?

James – 00:45:40:

No, it’s all been pretty positive. I think people were just kind of hungry to see a more narrow proposal, a more specific application of some of this covenant stuff. I’m happy that I released the paper and an implementation at the same time, because I think a lot of people have been proposing ideas on the mailing list. And it’s one thing to write an email, but it’s another thing to actually code it up with some tests and see it working. So feedback has been good. I mean, I think the next step is probably to write a BIP, and I’m pretty mellow in terms of activation. I mean, look, I think it’d be a huge benefit to have this in bitcoin. I would use it personally. I know a lot of industrial users would use it personally. I think it makes custody a lot safer for anybody. But I’m not really, my expectations about where it’s going are very tempered because you just can’t have expectations about that kind of thing, especially after watching what happened with Jeremy and OP CTV.

Stephan – 00:46:39:

Right. I think it was probably a case where maybe the community hadn’t been, let’s say, brought on board with it, and maybe that was I’m speculating. Right. That’s what it seems like to me. But that said, I mean, if it helps hodlers hodl, in this case, I think that there could be a case there people could see, you know what, this actually could be useful. This could be handy for people. So let’s see what happens there. Hey.

James- 00:47:06:

Yeah, right. I know. Yeah. With Jeremy and CTV, it took me a long time to actually appreciate what CTV does, because when you first see it, I just think Jeremy’s clock speed is like 3x of what everybody else’s is. We all have our strengths and weaknesses. I think Jeremy is brilliant, but when I first came across CTV, I was like, what the hell? What do I want this for? And it took me a while to actually internalize what some of the uses there are. I think opvault is a little bit easier to approach because, again, the use case is just so clear cut, and keeping coin safe is kind of everybody’s concern in bitcoin. And so it makes it a little bit easier to evaluate kind of whether or not opvaults the right thing, ultimately.

Stephan – 00:47:52:

Yeah, I think it certainly seems more crafted with this particular use case in mind. Whereas I think if a proposal comes and it’s like extremely general and very conceptual, you kind of have to be really deep into the technicals or really, really into it to go spend the time learning about it and then pushing for it. Because yeah, for this kind of thing, I think it just seems like the bar has risen a lot for what it would require. Whereas if you went back years and years ago, they used to do so forth pretty regularly.

James – 00:48:28:

Actually, on that note, I just like to comment a little bit. You said something interesting just now, which is we used to do soft forks more regularly, and obviously bitcoin was more nascent and smaller back in the day, but people forget we activated check sequence verify, check lock time verify BIP 68 all within the same year, and that was pretty close to segwit. And so I think you know more than anybody, trust me, I i get that there are certain things about bitcoin that we don’t want to change. I get that, like, this is the base layer, and you want to be very risk averse, but bitcoin definitely isn’t finished, and that’s an easy kind of tagline to use on Twitter. But there are certain aspects of bitcoin that I think really do need to change to facilitate the use that they’re all kind of hoping for. And so I hope we can be less skittish about evaluating proposals, kind of from first principles, determining whether they’re safe, and then looking at proceeding. Because as things stand, I do worry about bitcoin stagnating a little bit,

Stephan – 00:49:46:

And I think it’s fair to point out as well that you have to also consider, what’s the harm? Right. Let’s say we do obvault. The only people being harmed potentially are the people who choose to use opvault, correct? Right. It’s not that op vault has some kind of massive negative externality on all the other hodlers and users of bitcoin. Right?

James – 00:50:05:

That’s right. I mean, you have to be diligent about. So the one exception to that would be if you could construct a pathological use of opvault that, say, makes validation very difficult. And so you have to have a period for a few months where people are just sitting there trying to construct these pathological uses that can break. I sat there doing that with CTV for a while, and I was like, well, I can’t figure out how to break it. And it’s been months, and a lot of people who aren’t favorable to it can’t figure out how to break it. So it looks safe to me, and everything needs to go through that process, because conceptually, you’re exactly right. If you introduce a feature, maybe only the people using that feature are harmed. But from an implementation standpoint, it could be that there’s sort of contagion in terms of validation.

Stephan – 00:50:53:

I see. Yeah. So, yeah, at the end of the day, I think that was probably one other critique that people were I mean, just rewinding back to what happened with CTV. I think people were complaining that there was not any, let’s say, commercial use cases of CTV, or at least that was one of the critical lines. I’m not sure if that maybe you disagree with that. Maybe they were. But it seems with the idea of the vault, it seems a bit more very clear and very obvious. There are companies built around this whole idea of securing people’s coins or helping them secure their coins. It seems like there is a bit more of a commercial use here, and so therefore, we might see more interest in this idea. At least that’s my speculation.

James – 00:51:31:

Yeah, I think it’s a more tangible thing that more people can immediately go, oh, yeah, I might have a use for that or that’ll benefit me somehow. I think with CTV, the irony is, I think there are a ton of use cases that might be really valuable, like the DLC efficiency improvements, this idea of being able to initiate and receive Lightning while you’re completely offline or while your signing keys are offline, and then, to an extent, the vaults there could be helpful. But I think it was just tough when you think about trying to understand and appreciate CTV because you were kind of blasted with all these possible use cases. But I think nobody, a given use case wasn’t maybe fleshed out or championed enough for it to kind of go through. So it’s all understandable, I think kind of from everybody’s perspective in the CTV case, it’s understandable. I have all kinds of concerns about the bitcoin development process. In no case is it like, oh, somebody’s doing a bad job here. It’s just kind of the nature of trying to do something as decentralized and as kind of structural as this whole process is.

Stephan- 00:52:52:

Right. And I think that was perhaps hard for me to, I’m not trying to put words in Jeremy’s mouth, but it seemed that he was perhaps unclear about what bar he had to meet to sort of get this over the line, maybe in his mind. And other people were saying, no, we just don’t want to change it, don’t change anything. Like just leave it as it is. And so maybe that’s always going to be a debate and an argument going when anyone wants to do literally anything with Bitcoin. But perhaps it’s about if you get enough people on your side in terms of, let’s say, if the Bitcoin community, whatever you want to call it, is this anarchic mob of users, developers, miners and companies. And you sort of have to win enough of them over with this idea and say, look, there’s so much value here. We’re going to make Vault easier, and that’s going to make custody easier, and that may make people more comfortable to use Bitcoin, which obviously is going to grow our network and grow the users and bring more people in. Maybe that’s the argument. Maybe that’s the case you’ve got to make.

James – 00:53:47:

Yeah, that could be. And I think we’re in a little bit of a tough spot because for the last major softwares, there have been really a small set of people, extremely capable people, who have proposed them and have written the code. And now some of those people have kind of stepped back a little bit because they realize, I’m speculating, that maybe they realize that kind of having a dependence on the same group of people making changes is not a healthy state for Bitcoin to be in. And so as a result, this process of making consensus changes is in a little bit of a no man’s land where there’s kind of a vacuum in terms of like, okay, well, who’s kind of the authoritative voice here? And of course, there shouldn’t be an authoritative voice like you’re saying you do have to go out and get kind of this critical mass of community support. And that’s a tough game because where do you cut the line on that? It’s fascinating and very difficult.

Stephan – 00:54:49:

Yeah, well, I guess that’s the question. The final closing thought, where to from here with Op Vault?

James – 00:54:57:

For me, I think I’ve got a lot of irons in the fire with different projects I’m working on, and so I’m going to probably write up a BIP and then propose that, and then I think I’ll get the implementation to a point where I feel pretty comfortable with it. I’m sure I’ll need a lot of help from some of the gray beards in terms of making sure the script interpreter changes are really kind of ironclad. But once I get the code into a shape I’m happy with and I get a Bit written, I’ll just let it sit there, I guess. And if people like it, we can move forward, whatever that means. But otherwise I’m just going to go back to my other projects and let it hang out as an idea.

Stephan  – 00:55:42:

Fantastic. Well, listeners, I’ll put the links in the show nodes. James’s website is jameso.be/vaults.pdf is where you can go to read it and there’s a mailing list post and a Twitter thread. I’ll put all the links in the show notes. James, thank you for joining me today.

James – 00:55:57:

Hey, man, it’s always a pleasure.

Speaker A – 00:55:59:

So if you found that discussion useful, make sure you share it with anyone who is interested in bitcoin security and custody. That episode is Stephanlivera.com/449. You can get the show notes and a transcript will be put up there later on. Thanks for listening and I’ll see you in the citadels.

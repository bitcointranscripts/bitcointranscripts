---
title: Bitcoin Multi Sig With Sparrow Wallet
transcript_by: Stephan Livera
speakers:
  - Craig Raw
date: 2021-03-24
media: https://www.youtube.com/watch?v=xxxEST18_p0
---
podcast: https://stephanlivera.com/episode/262/

Stephan Livera:

Craig welcome to the show.

Craig Raw:

Hi there, Stephan! It’s great to be here.

Stephan Livera:

So Craig I’ve been seeing what you’re doing with Sparrow wallet and I thought it’s time to get this guy on the show. So can you, I mean, obviously I know you’re under a pseudonym, right? So don’t dox anything about yourself that you don’t want that you’re not comfortable to, but can you tell us a little bit about how you got into Bitcoin and why you’re interested in Bitcoin?

Craig Raw:

Sure. So I’ve really been in it for quite a long, long time, but largely just watching from the sidelines sitting every day on our Bitcoin back in the day. And ever since then, just really wanting to be part of things in a more kind of day-to-day manner. And that really just became possible for me personally towards the beginning of last year. So that was the time when I was able to put aside some time and really get into things. And that’s the outcome of the Sparrow Bitcoin wallet that you see today.

Stephan Livera:

Fantastic. So can you tell us a little bit about how the idea for Sparrow came about?

Craig Raw:

Sure. So the key idea that I wanted to work on was how to become self-sovereign over your own finances and what does that really mean? For me, and I think this is an idea you see over and over in the Bitcoin space was really about trust minimization. So at the time I had recently listened to your first interview with Michael Flaxman, which is, I think SLP97 which is really great. And he goes into some detail about the chosen nonce attack, which is where a hardware wallet manufacturer can effectively have the sort of sunset attack quite late in the day by just effectively having a certain chosen nonce, then they can you know, steal your funds. And that was I think just a really scary idea. And the interesting part about that was that you could eliminate virtually this class of attack by just getting hardware, wallets from different vendors and creating a multisig set up with those because it just became so difficult to action that kind of attack with that sort of setup.

Craig Raw:

So it was this multi-vendor, multisig idea that I was trying to work on myself and I was doing it with the Electrum client at that stage. And it was just really difficult to do. So that was one of the key ideas that I was working on at the start. Now it’s true to say that the ecosystem has greatly improved since that point, but I think that that was one of the sort of key ideas. It was just getting the sort of multi-vendor multisig set up done in this trustless way, as I could. The second idea that I wanted to kind of work on around this theme was that there needs to be a degree within every wallet software that you use, that you need to trust the wallet to some extent, but the idea of how we can minimize this degree of trust was one that was really trying to, was an idea that I was working on. And ultimately I believe that the more confident you are on what you’re doing, the fewer mistakes you make, and that idea of allowing the user to see as much detail as can be shown, really builds that degree of confidence in what you’re doing and allows you to ultimately dig into the details if you really want to and see that the wallet is in fact doing what it says it’s doing.

Stephan Livera:

And so, in relation to Electrum, what was the main thing that you saw that you wanted to change about the way Electrum operates in terms of Electrum multisignature?

Craig Raw:

Sure. So, I mean, at the time it was really difficult to set up an air gapped multi-vendor multisig. You know, I was trying to do it with a number of different hardware wallets, and it just really wasn’t easy at all. I had to write my own scripts to get certain information out of certain hardware wallets, and it was a difficult thing to do. But then I also was looking at the transaction screen on the Electrum wallet client. And there was a lot of information being shown there perhaps, but you really had to trust that that dialog was showing you what was actually going on. And ultimately when you’re working with a cold storage wallet you get what I think are called the cold storage sweats, where it all comes down perhaps one or two transactions at the end of the day that you need to send, maybe you are transferring from one cold storage set up to another, or whatever it is. And that’s a really scary thing to do. And you want just as much confidence as you can have before you press that broadcast button.

Stephan Livera:

Yeah. That’s a great point around giving yourself that confidence in the setup that you are actually sending where you want to send it to, and just seeing all the right details in terms of are you receiving into the right address and all of that sort of stuff. So moving to the server model and what is actually, what is the wallet or the client calling out to? So another wallet, obviously, as you know, I’m a big fan of Specter Wallet, but I think it’s great to see other great options like Sparrow. I know that Specter, if you will try to popularize the idea of just directly calling out to Bitcoin core, where I know with Sparrow, I think you started with the Electrum server approach, and now you’re also supporting this idea of directly calling to Bitcoin core. So can you just elaborate some of your thoughts there on the different approaches there?

Craig Raw:

So I think it’s important to say at the start that privacy is a journey and what we’re really talking about here is how to keep your coins private rather than losing the funds. I think those are two different things. And it’s important to go and create a whole lot of FUD in the space about saying, well, you can’t do it that way because it’s just doesn’t work. You know, but I think that what I’m really interested is in is trying to eliminate a certain class of attack versus various mitigation strategies that will work, but you have to kind of follow and do everything quite carefully along a certain line of thinking. So one of the ideas that I had at the very start was I just wanted to use an Electrum server versus using the core wallet in the background.

Craig Raw:

Now it’s obviously simpler to just set up a Bitcoin core node and to call directly into that. You’ve only got one piece of software to install apart from your wallet software itself. But there’s one really big downside to that in that you are now using the core wallet and the core wallet is stored on your hard drive in an unencrypted format. So your funds are not necessarily at risk from direct theft, because it should only be the public keys if you’re using something like Specter. But one thing that is certainly at risk is if anyone was to get access to that computer, whether it’s physical access or remote access, cause remember it is a node and it is presumably connected to the internet. Then they have access to the public keys and the addresses of your wallet.

Craig Raw:

Now that’s not a great thing because now obviously they know how much you have and they can go in there and potentially target you. So, one way to just eliminate this is to run an Electrum server, which effectively, rather than Bitcoin core, which just indexes the transactions of that wallet, Electrum server indexes all of the transactions in the Bitcoin blockchain. And whenever you ask it for the history of a particular address, it just goes and looks that up out of its really big index and says, here it is. And then forgets that you have asked so effectively, you’ve now taken what was a storage on sort of media on your hard drive and replaced that with just a very ephemeral kind of RAM access lookup, which is then forgotten. And that kind of idea just eliminates that whole class of attack, which I think is a very powerful idea.

Stephan Livera:

Interesting. So just to replay that for listeners then I guess, and maybe paraphrasing it a little bit, is one of the ways in the let’s call it the Specter model of calling out to Bitcoin Core. You are, I guess, giving the public key from your Sparrow wallet or your Specter wallet out to the Bitcoin core node. And it has to then keep that public key there. So it knows to watch for what transactions. And then what you’re saying is because the Electrum server model uses like the fully indexing model or an address index, it can then look up against that specific address that it’s calling for and asking, Oh, Hey, show me the balances on these 20 addresses, let’s say, and it will feed you back the balance and the transactions of that only. And potentially if you are now layering on the fact that this user may be connecting via Tor, then you’re getting an additional level of, you don’t necessarily know where this user was at the time they were interested in these addresses, correct?

Craig Raw:

That’s right. Yes. And I think the Tor thing is actually a really interesting addendum to it. So many people expose their Bitcoin core node over toward, because it allows them to then go and call into that node wherever they are in the sort of world. So you can have your node instead of set up and that sits at home perhaps, and then wherever you are, you can just call into it. But I think the danger there is that most software stores it’s server configuration details in plain text, or at least there’s no simple way apart from entering a password, every time you open your wallet client, as opposed to actual words itself you can’t really encrypt those details easily. And having a Tor dot onion address accessible over the internet to a Bitcoin core node, which holds your wallet just means anybody can go and fetch the details of that wallet as a remote attack. And I think that that’s quite a worrying thing that’s certainly just a class of attack I don’t want to have to worry about, especially if I’m using my wallet software on a daily use computer, and we all know that one shouldn’t expect that computer to be virus free.

Stephan Livera:

Yeah. And it might also make it easy for startup processes in some way, as in to get a new user to use this kind of thing, because there are sometimes some difficulties and maybe some teething issues getting a new user to use their own. Let’s say — using a Coldcard because you either have to get them to. Now, in most cases, they might have to buy, say a one terabyte hard drive or an SSD, and plug that to, their computer to have a full archival node. Ie. Full blockchain history, which as we speak is maybe 370 or 380 gigabytes, or they’re going for the pruned node approach. In which case sometimes you can have issues there around keeping that up to date, or it might be if the public key hasn’t been ingested correctly, then sometimes you get these weird issues where they can’t see the balance there correctly. And so sometimes it’s just these little teething issues that are a little bit difficult, but if you’ve got the Electrum server model, and maybe you can tell that newcoiner, Hey, just paste in this Tor address into your Sparrow wallet and then type in the port 50001 or whatever. And then from their point of view, yes, it’ll take a little bit longer to connect to Tor, but once it’s done, it just works. Right?

Craig Raw:

Yeah. That’s it. And I think there’s, as I say, it’s really about a journey. You know, you don’t have to start off with the most secure setup from the start and you shouldn’t let that put you off. You shouldn’t be thinking well, unless I go for the sort of, what I would call the expert level I just shouldn’t even begin. I think that you should absolutely begin and you should start off with what is the sort of easiest way of doing it if that’s the right place for you to begin, which is in Sparrow’s case, connecting to a public Electrum server. Now with that, you’re obviously giving your public keys, not your private keys, which are the sort of amount that you own over to these servers. I think it’s a pretty low risk thing to do.

Craig Raw:

So as long as you’re not connecting to a random server, which is something that the Electrum client does Sparrow uses a curated list of servers. That’s not to say that those servers are guaranteed to be good, but it’s just, there’s a high chance of it. And then you can move on from there perhaps then you move on to a Bitcoin core node and you have the issue that I talked about, but at least then you’re validating all of the transactions yourself and that’s an important step forward. And then beyond that, getting to an Electrum server is what I would call really just taking away that risk of somebody coming across your node and finding out what’s in your wallet. And that’s another great step forward.

Stephan Livera:

Yeah. And so you mentioned there what you would call an expert level. So could you just walk through in your view, someone’s listening out there and there’s probably a range of listeners. Some are beginner level, some are intermediate, some are advanced. How would you spell that out for them in terms of the high level progression that they should go through from beginner through to advanced level?

Craig Raw:

Sure. So as I said at the beginner level, I think you’re really just looking to get your funds often exchange and that’s super important, not your keys, not your coins. So you want to, at that stage, just be getting some kind of what it’s software, let’s say you’ve chosen Sparrow and you don’t really have an ability or the time to set up your own node at this stage. So you choose the first option, which is really just connecting to a public Electrum server. Now this is a model which is used by many wallets, Bluewallet, use it as well. They have their own set of Electrum servers, which they connect back to. And it’s a decent model, but you should be aware that the amount of your funds is being shared. Beyond that point you really want to start thinking about how can I become more self-sovereign over my funds? How can I avoid sending my balance out? And that’s about trying to get your own node up and going that’s about either a downloading Bitcoin core validating that you’ve got a correct and verified download, getting that installed, syncing the blockchain, all of that is quite a big step up. So it’s not something that, which most users will find easy, but there are a number of different node packages out there, which allow people to do it in a much easier way these days. So I think that that part of the ecosystem is getting a lot better. And then once you’ve got that node set up, you can connect your wallet to it, and you can then be sure that all of your transactions are not going beyond that node.

Craig Raw:

And then that is what I would call the intermediate level. And then beyond that you have the expert level, which is really about, I think, trying to minimize the amount of time that your cold storage wallet in particular is exposed to anyone, right? So you want to only have that wallet open for the minimum amount of time that you need it to be open for. And you want those public keys to be exposed to as limited a number of servers and as, for as limited amount of time, as you can be. So that’s about running an Electrum server, your own one, which connects to your own node and getting the information about your wallet, the most recent information, and then disconnecting the wallet and all information about those keys as they’re not stored anywhere except for your encrypted wallet file.

Stephan Livera:

Then in terms of the progression, I think for typical newcoiners, it might be starting on say a phone wallet, right? Just a small amount on a phone, just learning about it, then maybe a hardware wallet, and then potentially that’s where the conversation around maybe start maybe considering a hardware wallet with a passphrase or looking for the multisig approach. So how do you think about that and guiding how should a person who’s new think about that progression step there?

Craig Raw:

Yeah. So I think you should do the things that you are comfortable with. I think that’s the first principle don’t feel that you need to go, as I was saying earlier to the most secure setup from day one, I think that’s going to put a lot of people off and maybe actually make them less secure at the end of the day. Another concept, which I think is very important is don’t think there are any shortcuts in this you’re not going to get away if you are truly being self-sovereign over your funds from learning and understanding what you’re doing. So I think that that’s just a very important point is that you’re operating in a different model. We are so used to trusting banks and other people to look after our funds. And as we know that hasn’t in the, in the end, worked out all that well for us.

Craig Raw:

So this is a different model and people often talk about how the user experience is not there yet, and people are not going to do this thing because it’s too hard to do. I actually have a different view on that. I think when it comes to your wealth and your money and the other side of the coin, if you will, of not looking after these things and not taking responsibility for them yourself, then I think you will find the time to learn. So I think I just wanted to say that upfront as a different perspective on how to think about wallets, but I think ultimately trying to start off with a phone wallet is a great place to begin should you should absolutely get your coins off the exchange.

Craig Raw:

That is job number one. And when you do it, you should make the necessary backups. You should write down your seed words. And then from there one thing that I suggest to people who ask me, I just say, buy a hardware wallet right off the bat just go ahead, order one, because it’s a great place to, it’s not too hard for a beginner to use. Once you’re used to it, you’ve used it for a while, then I think it’s appropriate to start thinking about a multisig system sort of set up. That doesn’t mean that you, you have the level of funds that might require it, but if you lying awake at night, wondering whether you’ve done things right. Whether you’re actually secure, then maybe multisig is right for you. Yeah.

Stephan Livera:

And so part of the, I guess, difficulty with multisig is that there are all these other little nooks and crannies and things to think about. So for example, how do you do backups and recovery with that? And how do you make sure that you really get comfortable with using it as well. And then there are also issues around things like, okay, maybe the QR codes, won’t all be compatible across the different wallets or different applications. And sometimes there are little difficulties with that. So I guess you have to get comfortable with a certain setup and a certain wallet and then sort of progress up the stack or progress up the levels in that way. So can you tell us a little bit about the different hardware wallets that are supported by Sparrow?

Craig Raw:

Sure. So Sparrow supports pretty much all of the popular hardware wallets, whether it’s a Coldcard, Trezor, Cobo Vault, Bitbox, all of those whether you’re connecting them over USB, whether you’re connecting them via an SD card or via the QR codes. I think the USB sort of access is the traditional way of doing it. And certainly we’re very lucky to have now the HWI project by Andrew Chow, which I think has all of the hardware wallet manufacturers make sure that their hardware wallets can talk through that. So that’s really great and has largely taken away, I think a lot of the risk around USB access you have a standardized library that most wallet software uses to access them so long as they can talk to that, which is, it’s very much in their interest to do.

Craig Raw:

Then I think you’re safe on that front. From an SD card point of view, it’s really just around file format and those file formats don’t really change all that often. So again, once you have a setup you’re comfortable with, it’s unlikely that that’s going to break. And then finally on the QR front, we are still, in some degree of flux, we have a standard which is called uniform resource, or UR, there’s two versions of it out there in the world. And there’s a legacy version which Cobo currently uses. And then there is the more standards-based what is called UR2, which both of which Sparrow supports. And I think this sort of industry is going to settle quite soon on the UR2 format. So I’m hopeful that this year we will see a lot more in terms of the QR space and that being used because it really is such a great user experience.

Stephan Livera:

I see. And in terms of being able to do like an import from another wallet. So as an example, let’s say somebody had set up a Specter multisig, and then they try to import that into Sparrow and then still being able to do the transactions and do QR codes and so on. That’s still a possibility?

Craig Raw:

Yeah. So that’s been certainly one of my key goals within Sparrow. I’ve been sort of guided by the idea of just having this wallet software that can work with as many other different you know, hardware wallets, software wallets as I could. And you know, it’s really it’s often portrayed as multisig is bad because multisig is hard and you’re going to lose your funds. But I think the reality is that it’s not that bad and most people, most users that talk, talk to me often report how they created a wallet and Specter and import it into the Sparrow. The arrival of output descriptors on the scene has really made things much more easy. and I think we’re going to see a lot of wallets just use those.

Craig Raw:

Certainly in spite of Sparrow, that remains one of the easiest ways to get to set up with your wallet or to transfer your wallet is just to cut and paste what looks like a sort of a three or four line string of numbers and digits across, and then put that in and your entire wallet is then set up and ready to go just off of that. So that’s a very standard spaced approach to sort of doing things. I think the fear around multisig is no doubt coming from a good place, but I don’t think we should be too eager to dismiss it as being too hard. I think it’s absolutely achievable for many users. You just have to put a bit of time in to trying to understand what are the different concepts involved.

Stephan Livera:

I see. And so considering then as part of making sure we don’t screw this up, what about backups and recovery? What is your thought there? And what’s the approach that Sparrow Bitcoin wallet is using?

Craig Raw:

So I think first of all, the most important thing that everyone really knows about is backing up your seed words. so long as you know the threshold and the words, the number of co-signers that you need to sign, and you have all the seed words for all of the different key stores that you have. So if you have those pieces of information, you can pretty much be confident. You can restore your wallet. Now that’s because we have more or less standardized derivation paths for multisig wallets these days. It wasn’t so back in the day, but I think largely all of the modern, software wallets use the same standard derivation paths. So you can go ahead and simply back up your seed words and your threshold and ideally your script type as well.

Craig Raw:

But with just the first two of two of those, there is a very high chance. You’ll always be able to restore and multisig wallet. I think in terms of the future, we’re going to see advocation of backing up the output descriptor for your wallet. Now that’s something which is a bit more difficult to do, because as I said, it was sort of a three or four line long set of numbers and digits were so it’s a bit harder than a set of seed words. So we’re going to have to see what kind of technologies come to market that make that kind of thing easier. But of course, once you have that, then you really have a very precise and clean way of saying, this is exactly what my multisig wallet is. And that can’t be you know, sort of underestimated. I think that that’s a really nice way to feel confident that you’ve got your backup, right. So that’s right there on the set of settings page in the Sparrow, you just click the edit button next to the output descriptor, and it’s all there. You can write that down and then you will know that you’ll always be able to recreate that wallet in just about any wallet, software.

Stephan Livera:

I see. And so, as I understand the Specter approach on that question is that they have like a PDF output that basically you can print this PDF out and it’s got a QR code, which has that, that you can ingest using a QR, and it’s also written out. And then I guess the other prudent way to go about this is also to have, let’s say USB backup of that. Let’s say the JSON JavaScript Object Notation file. And so maybe as an, as an example, let’s say you’re doing two of three multisig. And in each of those three hardware wallet locations, you keep that paper and perhaps a USB holding the JSON backup file for the full wallet in each of those locations. And maybe that’s something to make sure that even if you were to lose one of the seeds, as long as you still have the quorum, i.e. The two or three or the three or five, you can still, as long as you’ve got two of three, plus that USB key, then you can still spend, right?

Craig Raw:

That’s right. I think the you know for me on a personal level, I wouldn’t like to send my multisig wallet details to a printer. Certainly if I had a USB backup, I would like to be encrypted backup with a really good password on it. So that’s some things I would think about from my point of view. I think one of the areas where software wallets traditionally, haven’t been that great is in this sort of encryption of the wallet files themselves. That’s not to say that they all are, but for example, the Electrum client uses a key derivation function called PBKDF 2, which is really quite old school. It’s sort of several decades old and it’s relatively easy to attack. So your encrypted Electrum wallet is not necessarily as safe as you might think. And that’s something that I really worked quite hard on when I was building that area of the Sparrow wallet was just trying to use the best tech in that area to make sure that your wallet file itself keeps all of those details as safe as they can be.

Stephan Livera:

And I think the other thing to think about is inheritance, right? So this comes up often in these kinds of discussions. It’s about when let’s say something happens to us, how do we make sure our heirs can still access the coins? And I think that is part of the challenge. And it’s just, it’s kind of just an unsolved problem. And if you will, I mean, I’m sure of course there are companies and people out there working on this. I know Casa have their own kind of inheritance planning and Unchained Capital — my sponsor have various approaches and thinking on this and then people who are doing it in the more let’s call it sovereign or DIY multisig approach, they have to think about how would their heirs recover this. And the difficulty with that is it might be, if we’re talking about somebody who’s cold storage, they might literally not be accessing that for a long time. And that they might, I mean, just as a quick example, if you look at laptops today, some of them don’t even support USB. They might only support USB-C. And so that’s like another example where over time, if you’re not careful, and you’re not regularly maintaining these things, then you can run into trouble down the line because now your heirs might have trouble actually recovering them.

Craig Raw:

Yeah. You’re quite right. It is relatively unsolved. I do hope that when we get Taproot, we will be able to create scripts that have, or more easily, I should say, create scripts that have a certain time delay on them. Cause I think that that is one of the approaches that has a good set of trade offs that you can effectively put your funds in a wallet, which protects them from anyone, but you for a certain period of time. And then that kind of gives you the certainty of knowing that your funds are self sovereignty, you for that period of time. But after that point, they can be accessed by a trusted set of others who you can assign keys, keys to, for me, that’s one of the most you know, interesting ways that we can go go forward. And I think that the kind of scripts that we will be able to write in future in terms of privacy level, make that much easier. so that’s, I think the way that I hope that gets solved at this time that’s what I have the most hopeful. I see.

Stephan Livera:

Yeah. And I think it also, just to me, it spells out the importance of maintenance and thinking about this, not just as like a set it up one time and you’re done, it’s not that. You have to think of it more like a maintenance thing where you regularly go around, you check your keys and you check that everything still works. And it’s still relatively functioning smoothly because you might find, let’s say six months down the line that your laptop doesn’t support this kind of thing anymore. Or like you get a new laptop and you didn’t think about it. And now your old hardware wallet that only has USB doesn’t work with this anymore or whatever. And then now you’ve got to start thinking about, okay I need to get like an air gapped one or whatever, or even another example might be micro SD cards. Right. Maybe the support for that fades over time, or I don’t know, there’s, there’s all these things that we can’t know, and we can’t predict. So you just have to be regularly out there checking it and maintaining it. And I think it’s just early days, high risk, high reward.

Craig Raw:

Yeah. Look, I think that that traditionally has been where it’s been been at. I do believe that industries do mature over time. I think we’re in that phase phase now in terms of the sort of wallet era, I think back in the day, that was certainly the case. But you know, ultimately so long as you have those seed words, it’s very unlikely. We’re going to get to a stage where the set of BIP39 seed words, you just can’t use them anymore. I think that you can pretty much rule that out. So yes, the hardware wallet that you have may not function in sort of 10 years time, but it’s unlikely that you won’t be able to restore a set of seed words. And I think that the risk is coming down all the time.

Craig Raw:

You know, we are getting better at these things. So the caution in the past and the idea of going back and making sure your set up sort of works is an excellent idea, and everyone should do it, but I don’t think you should be too afraid that somehow your setup is just going to suddenly fail. So as long as you are using the modern technology, that’s on the market today, because standards were few and far between even as little as two or three years back, and these days we have output descriptors, we’ve got PSBTs, we’ve got a lot of different technology, which is unlikely to suddenly fade. It’s not proprietary. It’s based on BIPs, which have been generally, and widely adopted. So things are not as bad they were. And that’s certainly been my kind of experience. I wouldn’t be able to write as many wallet, import and output formats, if the underlying data itself, hadn’t reached a point where generally speaking, you can import and output things from a variety of different wallets.

Stephan Livera:

Yeah, sure. And so I suppose that also goes very counter to let’s say, in the example of some companies and people in the space doing, let’s say the seedless approach where they try to just use, have additional devices where maybe that approach that you’ve outlined is more in line with the, let’s say the typical 24 words back them up on a metal seed. And you might have multiple sets of that because you might, you might be doing two or three or three or five or something like that. And I guess the other one is there are some wallets going down, a more approach where they’re not doing the typical backups for so one example I did an episode recently with Dario from Muun wallet where they literally, it’s not the typical 12 or 24 word backup.

Stephan Livera:

They are actually doing the whole output descriptors two of two multisig, Lightning and all this sort of fancy stuff where they are emailing you a back up. And now you’ve actually got to write down the password to decrypt that backup. So I wonder if there were to be a hardware wallet coming out, trying that sort of approach, or maybe if hardware wallets come out and say, we don’t want you to have to write down the seed words, you just put it on a micro SD card and then it kind of we’re back again to that same problem, aren’t we?

Craig Raw:

Yeah. I mean, there’s many different ways to do it, and it’s hard to kind of say this way is right and this way is wrong. I think that all approaches kind of have different trade-offs. I think what you’re trying to do is to have an approach, which as widely supported as you can, because going forward, it’s more likely that you will be able to do something with that. If you have dependence on a single vendor or a single kind of proprietary approach, then I think you’re at more risks. So I think it’s really just around trying to use as many standards as you can and seed words. Certainly that’s a very big standard format, derivation paths and script types are on multisig, which I think have largely really just coalesced now into sort of a few very set ways of doing things. That’s that’s good. Output descriptors are great. You know, they’re just a really great way to know exactly how your multisig set up was defined. So I think we’re in a much better place than we were.

Stephan Livera:

And in terms of taproot, as you mentioned, that opens up a whole new world in terms of scripts and potential script path spends that user could use. And I suppose in the future, that might be something like, okay, so assuming we get Taproot maybe we get some kind of Musig2 approach. Is that something you’re thinking about? You’re looking at that?

Craig Raw:

So look, I mean, I kind of need to focus you know, to larger extent, like most wallet devs are on the sort of needs of the users today. Taproot, I would guess is probably about a year off at least. So I’m certainly keen to get more into it, but, you know it’s going to be awhile before we can actually practically use that. And it’s also worth saying that the sort of privacy set is going to be quite small at first. So it’s unlikely you’re going to want to become certainly from a cold storage point of view early on to that. So I think we have a little time to try and figure out the best ways to do it. And that’s great because it allows us to kind of come up with ways which are hopefully better than what we have had in the past.

Stephan Livera:

Great. And you mentioned earlier around showing a lot of detail and exposing those details to the user. So let’s go into that a little bit. What are some of the details that the user will see when they are using Sparrow wallet and why is that helping them?

Craig Raw:

It kind of goes back to what I was saying. You know one of the sort of key ideas that I had was trying to create in a Bitcoin wallet, the experience that a programmer has when using a modern, integrated development environment, or IDE now whether using whatever it is, visual you know, the sort of Microsoft one or Vim, or you have a really you know, comprehensive environment environment that gives you confidence in terms of whatever it is that you’re doing. And it does so because it gives you the detail behind it. Now that detail has to be accessed in a way in the UI that doesn’t overwhelm, that doesn’t kind of throw so much at you, if you don’t know what you’re doing, but it also kind of allows you to really dig in if you have something that you want to go and check.

Craig Raw:

And that, that kind of idea is one that I wanted to bring across. So what Sparrow does is it really allows you in a sort of a gradually explorable way to dig into the details around what’s going on in your wallet. So you can obviously see like any wallet, you can see the transactions that have happened, but if you want to then go and dig in and then see, well, where did this particular amount arrive from? When did it arrive from? What was the UTXO connected to it? And what is the UTXO connected to that, then you can go in and dig in and do all of those things. When you are constructing a transaction, what are the UTXOs going into it, what’s the how does that whole thing look presenting that in a way, which is visually easy to understand.

Craig Raw:

And that’s really the sort of little graph that Sparrow shows whenever you create a transaction, it gives you an idea of what are the inputs, what are the outputs? Many Bitcoin wallets kind of try to go back to the idea that we’ve always had around an account, which is sort of a balance and then minuses and pluses to that balance. But Bitcoin under the hood doesn’t work that way. It works with a set of UTXOs. And as you know, when you spend a UTXO, you spend the entire type thing and you create a new set of them. And if you don’t think about Bitcoin in that way, you really are. I think, further down the line, exposing yourself to privacy risks. Because if you consume that entire Bitcoin, people can see well it came from that source and that’s how much change there was.

Craig Raw:

So therefore you must have at least that much, right? Those kinds of ideas I think are very important. And Sparrow is really around just trying to show as much detail as you can. There’s also the idea that when you are constructing a transaction and let’s say you’re doing that transaction, we were talking about earlier that sort of cold storage sweat one where you have to transfer the majority of your cold storage funds from maybe one multisig wallet to a single sig wallet, to a multisig wallet. You know, that particular transaction you want as much certainty as you can have before you click the broadcast button. And that’s really what Sparrow allows you to do. You can kind of dig into really all the way down to the bike level what is going on there, what UTXOs are being spent, where are they being spent to. And that gives you the confidence that can reduce that fear that can take away that sense of worry, because you can see what’s going on and you can trust yourself. And ultimately it comes back to the original idea that I spoke about is being self-sovereign over your funds. In other words, only needing to trust yourself, not needing to trust the wallet or the hardware wallet, because you can go in and just check everything if you really want to.

Stephan Livera:

Right. And I see that that can be very handy when you are teaching people as well. So if you are teaching a new person and you’re showing them one example, there is you can show them, Oh, Hey, look, this transaction, it’s going to create a change output. And that’s going to come back to you and you can sort of show them Oh see this amount is the fee. This amount is going to the other person. And this one is the change coming back to you. Another example is you can actually see the specific derivation path and you can see that, okay, this is M slash 84 slash zero slash zero, blah, blah, blah. And then you can actually talk about address checking, verifying a receive address, for example, and you can go into, as an example, you can open up the Coldcard, you can go the address Explorer, and then you can show that person, Oh, Hey, go into the BC one addresses, and you can see the zeroth address, right? Like in programming, sometimes they start from zero and then you can check that on your Sparrow wallet and you can see Oh, see, it’s got this specific, it’s got that same pathway.

Craig Raw:

Yes, that’s right. And you know, that’s really what I think it’s about the other feature that I’d like to mention, there is one that came out recently, which is using the replaced by fee or RBF feature, which is built into Bitcoin and it is really an amazing and underused kind of aspect to how Bitcoin works. So with that, you can send a transaction at a really low fee. And that goes into the mempool, and it just sits there, but it doesn’t get mined because the fee is too low. And then what you can do is then come along later and you can actually replace that entire transaction simply by spending the same outputs at a higher fee. And that feature built into Bitcoin is just a way to be able to make sure that your transaction is going to the right address before you actually have it confirmed.

Craig Raw:

in its first block. So what you can do is use what Sparrow calls try-then-replace, which allows you to send a transaction at a low fee one, which is unlikely to be confirmed any time soon, go and check in the destination wallet. Let’s say, you’re sending it to yourself. Or maybe you sending it to somebody and you ask them to go and check. And they say, yes, I can see it. It’s popped up in the mempool. It’s not confirmed yet. And then at that stage, you can then go and increase the fee on that. And then it will be confirmed and go into its first block. So if that doesn’t work, if it doesn’t appear in the destination wallet, what you can actually do is replace the transaction completely.

Craig Raw:

So you can send it to a different address you know, perhaps you just replace it and send it back to your own wallet. That really reduces the amount of worry. You know, if you think about that cold sweat transaction that you’re wanting to send, you can now know before even if you really don’t check it at all, you can, you can just do the very simple check of going to the destination wallet its going to and saying, has it popped up there and if it has, then you can be pretty sure that you’ve done everything right.

Stephan Livera:

You’ve also got PayJoin support. So can you tell us how that works and you know, what the story is with that?

Craig Raw:

Yeah. So what we have have have there is the sort of PayJoin in the format of the pay to end point as it’s called. So this works with a merchant, like somebody running BTCPay server, where if you go into the sort of invoice, and I think it’s actually on the sort of second tab. If you click across, there’s a link there at the bottom for those merchants that have turned it on. And that what that effectively does is puts a URL into your invoice, which Sparrow then uses to then say to the merchant say, Hey, can you provide me with an additional UTXO to make up this transaction that I’m going to send to you. Now, why do we do that? We do it to break what is called the common input heuristic, which is where basically, if you’re trying to analyze the chain, you can say, well, all of the inputs to a transaction are coming from the same owner, but in this case, we have the merchant providing one of the UTXOs.

Craig Raw:

And that allows you to effectively break that because now you really don’t know what’s going on now. You can’t say that individual X, Y, Z has this much Bitcoin because part of that amount is the merchants. So that’s the format that Sparrow has built in, right now. Now the downside to that is the need for this HTTP address, right. That we need to go and talk to the merchant and say, Hey, where’s the additional UTXO that you want to add what I would really like to do and what the Samourai wallet has really built in. So you can do this from one Samourai wallet to another, is the ability for any wallet to go and fetch UTXO effectively in a collaborative way, construct a transaction where the inputs are coming from both wallets. And that’s really, I think the part of that, that I really liked as it helps the privacy for everyone.

Craig Raw:

So for example, coinjoin is a great tool, but it helps fewer people, particularly the sort of equal output coinjoin because it doesn’t necessarily break the privacy guarantees for everyone on the chain, but PayJoin is really great because it effectively creates doubt for everyone. Right now, you’re looking at a transaction and you’re looking at the inputs and you’re saying to yourself, well, I don’t actually know that there’s a common owner to these inputs. So for me, increased adoption of PayJoin is a big goal. And I would really like to find out and develop better ways that we can allow just different wallets to be able to create those.

Stephan Livera:

And you also have Tor built-in. So we mentioned this a little bit earlier, but can you chat a little bit about the uses of having Tor built in?

Craig Raw:

Yeah, so I mean, Tor is a great tool. It obviously allows you to basically not divulge the IP address that you’re using. That’s the sort of key goal there. And it’s both great and it’s not so great. So plenty of people have issues with Tor. You know, if you go on any wallet, user support group, you will see people complaining about how Tor is not working on that day, or all sorts of things. So I think it’s an important tool in the Bitcoin’s toolbox. I think it’s important not to rely on it 100% unless you are prepared to deal with Tor downtime, and that does happen. But you know, it’s certainly there in terms of being able to connect to your Electrum server over Tor which is a common way. Many people will do it that will allow you to run an Electrum server, let’s say, at home connected to your own node, and then talk to it in a very private way from anywhere in the world. So that’s, I think a very good use case for Tor, but as I say, Tor does come with some down sides, which are worth thinking about.

Stephan Livera:

Of course, and I think it’s probably worth highlighting just for listeners here that if you are the kind of person who is being Uncle Jim for your newcoiner friends, this is probably a really easy way to do that because I’ve been fooling around with it, obviously, just to try around in preparation for this discussion. And I’ve noticed that it was quite easy to just use Sparrow and connect that through Tor to my umbrel node. So, as an example, if I want to help a newcoiner friend, I can just tell them. And if you are out there and you’re thinking, you’re trying to help your friends. If you are running, let’s say an umbrel or one of the other package nodes, you can just get that Tor address. And then the port, and then all your friend has to do is paste that in. And then boom, now they are connecting their Sparrow to your Electrum server, as opposed to a public one. And obviously the aim is ideally they can grow up and become an adult Bitcoiner run their own Bitcoin node. But while they’re still your niece or your nephew, you can help them out.

Craig Raw:

Yeah. And I think that the great thing about that is that you not putting yourself at risk in any way there, as I was saying, when using the Specter server, you are basically you know, that server has indexed all of the transactions on the blockchain. So that request comes in, the server looks it up and then sends that information back. So there’s no risk to your own funds. Your own funds are not stored, or there’s no reference to the keys that you particularly hold on that sort server. So that’s a really nice way to help people out without putting yourself at any risk at all.

Stephan Livera:

Now, in terms of the I guess the funding and sustainability of this approach, what’s your thought there? Because I guess the other thing in the Bitcoin world is people don’t want to use something if it’s, they don’t want to basically trust it too much, if it’s really new. And so what happens is things need to have time to have been built up trust in it and for there to have been other people contributing and eyes on the code and those kinds of questions. So how are you thinking about that aspect of sustainability? Because people ultimately feel like they want to use something that has been around for a while and it’s going to continue to be around for a while. And I think that’s why things like Electrum have been so long standing also.

Craig Raw:

Yeah. And I think, I think that that’s an excellent you know, sort of point of view to have. So I think that there is no really replacement for just the period of time and people should certainly be cautious when it comes to new pieces of software as indeed they are. You know, one of the things that we can do is ask for people to take a sort of look. We can ask for instance, Bitcoin.org has a review process, which they go through before they add any wallet to that site. And that’s a process that Sparrow is in now. There is just no easy way to solve that particular issue. You know the best way forward, as I was saying is to really try and take that as much as you can onto yourself and to check and to learn as much as you can so that you can make yourself as secure as you can be. You can obviously delegate that trust to others, and you can say, well, XYZ, there’s check the code, or this many thousands of users have used the word too. It’s been around for this many years, and those are great signals, but ultimately there’s no replacement for the sort of self-sovereign trust that you can have by understanding how Bitcoin works and doing your own checks.

Stephan Livera:

I see. And just from a Sparrow perspective, then how is the wallet going to be funded going forward? Is it going to be monetized or is it going to be treated more like, it’s just a free open source project out there and it’s just reliant on contributors?

Craig Raw:

Yeah. So, I mean it’s an interesting question. I’ve had plenty of times in my life where I’ve begun building something and it’s sort of turned into something which was a successful sort of endeavor further down the sort of road. So I’m relatively comfortable with working on something where the sort of end path is not really known. What I can say is that Sparrow is going to remain open source and free. It’s not going to change from those goals. I can say that it sort of gets me up every day and I’m enthusiastic and keen to work on it. And I really just believe that there is so much human good to be done in terms of providing people with platforms that allow them to be self-sovereign over their own funds.

Craig Raw:

That for me, that’s reason enough. I don’t need to have additional sources of income to make this worthwhile to me. Now, I think everyone’s different and that’s fine. But I’m really keen to keep building on this to keep making it as good as it can be because ultimately I serve myself by doing so, and the sort of feedback. And if you will, the sort of social credit that you get in terms of being able to build a thing which is useful to many is enough. So yeah, that’s the best answer that I can give. I’m not looking to make this into a business but who knows what the future holds? It’s just for now enough that it is useful and usable by others.

Stephan Livera:

Gotcha. Yeah. And I can understand that. I mean, obviously there are a lot of things in this space that aren’t necessarily done for money, but I think perhaps that helps in a sustainability point of view because then the user looking at that product or that project might think, Oh, okay. It looks like that thing is going to be maintained and going forward, because they might feel a little sense of hesitation about jumping over to something where it’s not clear that it’s going to be around. Oh, I don’t know. Maybe it’s yeah, it’s just less clear in their mind, but hopefully over time, if people like it, there’s more contributors and it builds up a community around it, then that’s a good sign, I would say.

Craig Raw:

Yeah. I think that you just have to see something that’s stood the test of time, like the Electrum client wallet. I mean it’s been around for a very long, long time as far as I’m aware, there isn’t a business behind that, but it’s clearly a model that can work. So I look to that as an example of there’s something which kind of indicates that the model I’ve chosen for Sparrow can be one that lasts for a long time.

Stephan Livera:

I see. Yeah. And of course there is number go up. So of course for many of us that kinda does help obviously for people who can maybe as number goes up, there might be more people who are, let’s say passionate about something, and now they can afford to work on it in either in their spare time or even as a full-time thing. So we’ll see what the future holds there. So look, I think it’s probably a good spot to finish up here. Was there anything else you wanted to mention about the wallet?

Craig Raw:

No. I think the last kind of feature that I wanted to touch on which is, I think just interesting for people to think about is really to try and minimize the trust that you have to have in the environment in which the software runs. So I’ve mentioned this before, and I think it’s a discussion which needs to be had more is the idea of running a wallets in a browser. I do think that they are risks there. I think that the risks can be reduced by using certain kinds of browsers, but it is something which I certainly think about a lot for example, if one was to fire up Chrome, which as we know is one of the most, one of the least privacy conscious browsers that there are out there where you can have all kinds of plugins.

Craig Raw:

You know, you have to think about whether that is the best environment to run your, for example, your cold storage wallet in. And that’s really one of the key goals that I had building Sparrow was just to get away from the sort of browser world, which has been so much a part of the way everything was built for a long period of time, because we wanted to have things as sort of easy to build as cross-platform and as sort of connectable as we could, but it’s, it kind of runs a lot of those ideas run pretty contrary to the idea of a cold storage wallets. So it was really getting away from that and getting back to the idea of a traditional desktop app, which was a key goal for me in this. And it’s just something which I think needs to be talked about more and thought about, particularly as I say, when it comes to securing the sort of the sort of cold storage funds that you might have.

Stephan Livera:

Right. And I think probably the other implication as well, of what you’re saying and potentially that’s the security risk for the person is if they are known to be holding a lot of coin, well, then that itself becomes a security risk. So people sometimes when they’re new, they confuse privacy and security, but this is potentially one example where there is some blurred line there that if you are known to be you know, a big, HODLer, then that might essentially paint a target on your back.

Craig Raw:

Yeah. From a sort of a risk point of view, I think the Bitcoin community has been focused. And I think rightly for a long time on the sort of nation state attack the sort of they’re going to ban Bitcoin, it’s going to become a black market. Good. and what can we do about that? And that’s a, that’s a great point of focus to have. But I think if we look at the sort of momentum right now in places like the US it seems very unlikely that we’re going to have a ban. It’s just to me, anyway, it seems a very unlikely case that that sort of momentum is going to shift back. Now they could ban self custody and do all kinds of things.

Craig Raw:

I think those debates are very much still to be had, but it seems to me that one risk, which is sort of being a little bit more sort of overlooked is the idea of a sophisticated criminal attack. Based on the fact, somebody finds out how many coins you have and then targets you as a result of that. And that, to me seems like a more real risk that we should perhaps start thinking more about. So that means first of all, around securing the public keys that you have and making sure in the different ways that we’ve talked about making sure that those never get leaked. So just making sure that your cold storage wallet is used as little as it can, making sure you’re not using it in a browser still stands, making sure using you’re not storing those keys, unencrypted on a drive.

Craig Raw:

So those are kind of the ways of which I would try and reduce that sort of sort of threat. And beyond that. Making sure that you have geographically distributed keys. So making sure that any kind of attacker would be forced to go to multiple locations, ideally with different kinds of security attached to them, so that it becomes just really hard for somebody to rock up at your door, put a gun to your head and say, give me all your funds. Those are the kinds of discussions that I think we should be having more, because if you think about what Bitcoin is, it represents one of the easiest or one of the most attractive forms of wealth that we’ve ever had in order to sort of steal. It’s very hard to steal a house or to steal somebody’s gold bars sitting in a vault. You know, that’s not an easy thing, but if we’re looking at advising people to store their Bitcoin funds at home, and then we’re not providing them with the right tools and thinking to be able to really protect themselves against a criminal threat when doing so then I think we’re kind of overlooking one of the big risk aspects here. So that’s really what I’ve focused on quite a lot. And what’s quite sort of close to my idea of how to be really secure.

Stephan Livera:

Of course. And I think that can be a bit confronting maybe for some listeners they’re thinking, Woah, like maybe in a few years time, if number goes up and now I’m at massive risk, but at the same time, we have to remember, I think as my friend, Michael Flaxman says, if we can successfully popularize the use of multisignature, it means there’ll be a lot less people who even try this kind of attack. So I think that’s also really the opportunity here that if speaking broadly, we, as an ecosystem, the Bitcoin ecosystem can successfully navigate this kind of transition where it’s kind of a default thing that a lot of people are just using single signature and get them into a multisignature world. Then it may just make it that much more asymmetrically. It just makes it that much more stronger from an asymmetric defense point of view, right?

Craig Raw:

That’s right. Yeah. So I think if we can much in the same way that if we can just make it so that the chosen nonce attack that Michael mentioned becomes so unlikely that people that it just no longer becomes something we really need to worry about. This is very much the same, right? It’s just about trying to have thinking that makes it so that a criminal just thinks; that’s going to be way too hard because that person is almost certainly with that level of funds going to have multisig, it’s going to be sitting in different locations. It’s going to require me to not just enter one place, but to enter several, perhaps some of those are sort of bank vaults or so forth it just starts to become so hard to think about that it really reduces the risk for everyone because now even if you are sitting with all of your funds on your Coldcard at home, you are classed in that same kind of bucket of all of the multisig users. So yeah, I think that that’s a great idea. And one of the kind of reasons why we really need to make multisig a good option and in fact, a default option at some point in the future.

Stephan Livera:

Excellent. So, Craig I think that’s a good place to finish up here. So before we let you go, Craig, where can listeners find you online and where can they find Sparrow wallet obviously?

Craig Raw:

So I’m on Twitter @craigraw, one word and Sparrow can be found sparrowwallet.com Sparrow wallet, all one word.

Stephan Livera:

Fantastic. Thank you very much for joining me, Craig.

Craig Raw:

Thank you!

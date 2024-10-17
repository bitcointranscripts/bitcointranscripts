---
title: Specter Desktop Bitcoin Multi Sig
transcript_by: Stephan Livera
speakers:
  - Stepan Snigirev
  - Ben Kaufman
date: 2020-08-28
media: https://stephanlivera.com/download-episode/2433/205.mp3
---
podcast: https://stephanlivera.com/episode/205/

Stephan Livera:

Stepan and Ben, welcome to the show.

Stepan:

Thank you. Thank you, Stephan. It’s very nice to be here again.

Ben:

Thank you for inviting me.

Stephan Livera:

Stepan I know you’ve been on the show twice before, but perhaps just for any listeners who are a little bit newer, can you tell us a little bit about yourself?

Stepan:

We are doing well originally I came from quantum physics into Bitcoin and started working on hardware stuff mostly. And now it’s also like we have both the desktop app and the hardware wallet that we are working on. And currently me and Moritz are running a small company, a startup that is working on this product and also the enterprise solution.

Stephan Livera:

And Ben, let’s hear a little bit from you. Tell us a little bit about yourself and how you got involved with the Specter project.

Ben:

Yeah, so I’m just, yeah, I’m software developer patiently contributing to some open source projects for like the past year or so I think. And I just stumbled upon a video of Stepan setting up a multisig on Twitter with Specter. I I’ve been looking for something like that like connecting a big full node with multisig for quite some time. And we’ve hardened wallets in general, but I couldn’t really find anything that worked very well. That was convenient. But for the first time this was like something that just worked for me real easy. So I kind of just started using it. Then whenever I wanted a new feature, I just started writing it myself. And I did that. And from like small contributions, like avoiding address reuse, for example, or labeling UTXOs just stuff that I needed. I just continued contributing more and more often.

Stephan Livera:

Excellent. And so we’re going to talk about Specter desktop today. So maybe Stepan can you just tell us a little bit about why did you start this project? Why are you making it?

Stepan:

Yeah, sure. So we started it a year ago, I think roughly and the main reason was that first I actually needed a wallet that would work with our hardware. And I was thinking that, okay, it’s nice to use Bitcoin core for that. And as we were from the very start working on the multisignature supports, we also wanted other signers. So the very first version of Specter Desktop was the GUI that was only working with Specter DIY and Coldcards. So only airgapped hardware wallets and then people actually started contributing and we got an integration with HWI the hardware interface by, Andrew Chow. And we instantly got a support for all hardware wallets that are out there. So the main idea is that okay, I want to run my own full node.

Stepan:

And Bitcoin core is very powerful in that sense but it is not very convenient to work with it, especially with hardware wallets. So the goal of Specter desktop is to kind of close this gap and actually provide a convenience or user interface for hardware wallets to Bitcoin core. And the main focus is on the multisignature and then the Multisignature with hardware wallets we have problems with the security, because we are only like a small coordinator app that is in between these kind a very well tested powerful tools.

Stephan Livera:

I see. Yeah. So I guess just for listeners too.If you’re not as clear what’s going on here, so some of the discussion is around how can we leverage Bitcoin core as much as possible, because let’s say that code base has been well reviewed and get a multisignature setup going in a way that’s easy for the user, but is minimal in the sense that it’s mostly pushing most of the, kind of the heavy lifting over to Bitcoin core, but then how do you do it with your own Bitcoin node for if you want to have your own privacy, or if you want to be doing your own verification? So I suppose that’s kind of the focus. So Ben, did you want to just tell us a little bit, what does it look like if I try to set it up and use it?

Ben:

Yeah, sure. So first of all, you just set up a Bitcoin core full node. It can be on the laptop, it can be on a Raspiblitz or myNode or whatever. But just setting that up after that you can, right now we’re working on very simple like desktop apps, which you can just install normally. We’re very close to finishing that. But for now you just you have like executables which you can run on your computer and it will just run Specter, desktop as the server on your machine. Yeah. And then you can start using it like by adding your devices, your hardware wallets, so you can connect to your computer your Trezor or your ledger use your Coldcard in air gapped, or directly with your computer. Basically we support all major hardware wallets.

Ben:

We support airgapped devices like Electrum on your mobile phone, on your computer. So basically you just need to extract it, the pub keys, the public keys of your device and input them into Specter. So we can do that automatically for non airgapped devices or for airgapped devices. You can just either scan a QR code if the device supports it or whatever. Like it depends on the device you use. But then after, setting up your devices on Specter, you can start just playing with them, creating multisigs with them, whatever setups you want, two of three of five you can do like just single wallets you can do basically whatever you want. I it’s quite flexible, I think. Yeah. And just once you have wallets set up, you can start receiving funds. You can start sending funds. All signing is taking place on the devices in which you’re using. So if you’re using a hardware wallet, you just connect it to your computer and Specter communicates with it, or if you’re using an airgapped device, you can for example, Specter do it yourself. You can just scan the transaction with QR scanner and then scan it back on your computer to sign it. Yeah. And that’s it basically.

Stepan:

Yeah, maybe I can add a few things. So currently we support different setups, so you can run Bitcoin core on the remote machine. You can connect your, Specter desktop that is on local machine to the remote machine or you can run both of them on the remote machine, and then you run another instance of Specter desktop, but in this HWI bridge on your computer.

Stepan:

So, and also Bitcoin core itself can be either a full node or a pruned node. So for example, what I do, I run Specter on the cheap together, with Bitcoin core on a cheap VPS server that is five bucks per month, and it is extremely approved. So it just takes 10 gigabytes of space. And I’m using it to watch my funds prepare the transactions. And then whenever I need to do the transaction, I can, either use air gapped hardware wallets to sign it, or I can use this HWI Bridge mode to communicate with my hardware that they’re connected to or to my laptop. So it’s pretty convenient. I would say currently we have support also of Raspiblitz and myNode. So the guys commenting in this project actually integrated it. So I think that’s RaspiBlitz it’s just single click installation and implemented that. And myNode I think it is on premium package, whatever it means. And it also can be installed pretty easily.

Stephan Livera:

Yep. And so I guess, just to put it into context for listeners who might not be familiar in this space, people who want to do multisignature and if they’re not really at an advanced level, then usually it’s, you know, the usual choice for people is to use a guided provider. So such as my sponsor Unchained Capital or Casa, and then now in terms of non, you know, if you want to do it yourself, probably up until now, the main option that people have done is Electrum. But now we’re starting to see some of these other options that come up. So obviously Specter desktop is one of the ones that looks promising. Also there is unchained capital’s caravan, which is also again Unchained Capital are my sponsor, but they offer caravan, which is like a way to also do it yourself. And also there’s Lily wallet by Kevin Mulcrone as well, which is also another promising project as well. So I guess, could you guys just tell us a little bit about how you see Specter Desktop as compared to some of the other options out there, let’s say versus say Electrum or any of the others?

Stepan:

Yeah. So Electrum for example, it’s either connect to remote servers and then you don’t have your own phone out and you give up the privacy, or you need to run an Electrum personal server or electrs. So for example, electrs takes like 20% more space comparing to a normal Bitcoin core. Basically none of these options sexually rewire on the wallet, functionality of Bitcoin core but Electrum works fine. I tried it with hardware wallets and they also support very many hardware wallets. The only problem is that I cannot just run simple Bitcoin core without any like extra on top of that, comparing to caravan supports only the Trezor and ledger and I think that every time when you sign a transaction with Trezor, you actually need to go to their website to confirm that or something. I’m not quite sure. But basically Caravan is a very interesting tool, too bad there are not very many hardware wallets supported. Lily wallet I can’t really say anything. I didn’t try it.

Stephan Livera:

Sure and I suppose part of this also, it comes to how do you make it easy for the user who is not so technical because obviously the number of technical users, it’s probably less than 5% of the overall population, if you will. And so one of the barriers for many people is that they have to install different libraries. For example, with Electrum, if they want to use Linux, they’ve got to make sure that they go and install these different, like the udev rules and so on. There’s, there’s kind of a bit of configuration involved. So can you just tell us a little bit about when you’re setting up with Specter Desktop, how does that compare from a setup perspective and how technical is it? And I can also understand it, it might be kind of more technical now, but you’re planning to make it easier for people as well. So it’s more like a GUI and a double click and install sort of thing.

Ben:

Yes. So right now we’re just finalizing the proper desktop app, which can be installed normally like any other one. So we already have it for MacOS and almost ready for Linux and like pretty much halfway for Windows. So I hope this will be like, at least that the Mac and the Linux will be out until this episode airs. But currently what we already have ready for all platforms is an executable, which you can just download on your computer and just double click and it will run everything.

Ben:

But it’s like in the past you had to install it through Python through pip if you know about that. So it was a bit more complicated but like right now it’s quite simple already and going to be like any other normal desktop app very soon.

Stepan:

At the moment it’s actually determined or are you always this terminal window popping up and printing stuff. And windows, is always causing problems. So we actually started packaging it mostly because of the windows setup, because installing Python is a nightmare there.

Stephan Livera:

And so one of the big features that you guys are building with Specter desktop is that you have more of a focus around using unsigned PSBT partially signed Bitcoin transactions and also the use of QR codes as well. So listeners, if you haven’t already make sure you listen to episode 97 with my friend Michael Flaxman, who spells out some of the reasons why we care about some of these aspects. But can you tell us a little bit about the HWI aspect also, and also which devices are supported inside Specter desktop?

Ben:

So right now we’re supporting pretty much all major devices, so Trezor or Trezor One and T ColdCard, KeepKey Ledger Electrum as airgapped mode. We even support Bitcoin core as a hot wallet, but we don’t really recommend using the hot wallet. But we also support that. We also support Specter do it yourself, of course, and Cobo Vault, which is another air gapped device using QR codes which is fairly new. But yeah, so that’s pretty much the devices we’re supporting. Soon, also BitBox02 will be added to hardware wallet integration. There is an open PR for that there, and once it’s edited, it’s just like a few minutes of work for us to add it also to Specter. So it can easily support that as well very soon. So yeah just hardware wallet integration handles most of the heavy lifting with communicating with the hardware wallets for us and working and airgapped devices they’re all supporting PSBT which if anybody doesn’t know is just partially signed Bitcoin transactions.

Ben:

It is a standard way to use an interact and pass around a Bitcoin transaction for signing between devices. So yeah, all Specter use that for everything. Hardware wallet integration uses that, Bitcoin core uses that. All the airgapped devices are using it that Trezor and Ledger and other devices, which are connected directly to your laptop doesn’t really use that exactly. Like not natively, but hardware wallet interface interface by Andrew Chow parses that. So we don’t really need to worry about that as well. So everything just uses PSBT.

Stephan Livera:

Yeah, I think that’s definitely the way it looks like everything is going towards a PSBT future, which is a hopefully making it a little bit easier for well, for software developers and for hardware creators as well to make wallets that can pass around the information to each other in a way that’s easy for them to understand what they’re sort of saying, I guess, and for the listener who is, you know, using your hardware wallet to keep your private key secure will then the PSBT is how you can pass that information from say your Specter desktop, to your Coldcard or to your Cobo Vault or et cetera to sign. And also it’s interesting, you mentioned around cross compatibility. So you mentioned there that you might even have Electrum can actually be part of your quorum of keys for Specter desktop. Is there any other aspects around cross compatibility there you wanted to touch on?

Ben:

Yeah. Sure. So what we currently have, for example, we can we have also been working with fully noded, which is an iOS app for interacting with your full node. We have been working with them on compatibility. So you can both use that as a signing device if I remember correctly, and you can import and export wallets from Specter over there to watch them over there as well. And vice versa. We also are planning to add support to import and export to Electrum. So you don’t just use it as a signing device. You can also, if you, for some reason, want to use that as your wallet software, you can migrate easily or migrate from there to Specter and the same, hopefully for (?) as well. We just need to, we still need to check we’re planning too.

Stepan:

So the important thing here is that it would be very nice to have cross compatibility with different software so that if something breaks in Specter desktop, you know, you’re in the development sometimes introduce bugs or whatever happens during the update, you shouldn’t be locked out of your funds, right?

Stepan:

So you should still have access to your finances. Ideally you could just install Electrum and import the wallet and use it there, or just to keep it just in case, or I normally use Specter desktop.

Stepan:

For example, but, you know, if something from something breaks, then you can always fire up Electrum and use that to sign the transaction, to send the files, and also other way around, so if people decide to migrate from Electrum to Specter Desktop it should be as easy as importing a wallet file

Stephan Livera:

Just on the idea of working without having an Electrum server as well. So we were touching on there. So I guess typically people who want to do this, they might have to, it takes additional computing, power, hard drive space, and so on. How it working here where you’re basically doing the same, you’re doing a similar function, but without having an Electrum server, how’s that working?

Stepan:

Yeah. So Electrum server, what it normally does, it creates so first it requires Bitcoin core to run the txindex such that you can actually look up all the transactions and also electricity, for example creates an address index. So you can look up transactions and balances for any address and in principle, well, you don’t care about all other addresses out there. You only care about your own addresses and Bitcoin core, wallet functionality already provides all these features. So the only drawback here is that if you’re importing a very old wallet, where you have plenty of transactions, then you need to rescan. So you still can use just a bare Bitcoin core without any extra flags like txindex or additional indexing. But if you’re importing old wallet, then you need to wait for , I don’t know dependent on your computer, but it can be even hours to rescan full blockchain to actually see your balance. So this is the problem, but you don’t import wallets very often. So once you actually set everything up then you just use a wallet functionality available in Bitcoin core.

Stephan Livera:

Great and also wondering whether you would look at, or consider light clients using, say like compact block filters, BIP157, 158 style, or any other style of light client?

Ben:

Yeah, we were open to that. I mean, we will look into that, but I think like more in the future like it’s definitely not going to be available short term. And anyway, I personally would not really recommend light clients I think full nodes are more secure and generally better, but we will be open to look about something like neutrino, as you said. I think it can make sense in some scenarios. And I think it’s a good compromise. If you can’t have a bit full node but right now we already support just pronounced Fully Noded Bitcoin as well. So you can, it takes like what 10 gigabytes maybe, which is definitely not terrible for like any desktop I think or at least most desktop. So I think I think for now this is not something very important but we are open to that. I mean, we will check that once we have we have the time

Stephan Livera:

Also just on the topic of building your own hardware wallet. So Stepan, you mentioned a little bit earlier around the Specter DIY, which was the one of the projects that you’re doing at Crypto Advance. Can you tell us a little bit about that and how that interrelates in with Specter desktop?

Stepan:

Yeah, so I already mentioned that we started all that just to get integration for Specter DIY. So the idea there is that we want to have a hardware wallet that has a completely different security model compared to normal hardware wallets. And one of them is that you want to avoid supply chain attack. So we actually design it to be able to build it from off the shelf components, or you just go to your local electronics store or you shop online or like a general purpose microcontroller boards and the QR scanner, and then you just put it all together. Put the firmware there and it just works. And yeah, it does air gaps. It does work with PSBT natively. It works with wallet descriptors natively so not, or not full support of wallet descriptors, but the most common ones. And in principle, I think that it can will evolve into something nice in the future. But at the moment I think it’s really like a project for tinkerers and maybe for developers that want to try out a new interest in things, because we are not (inaudible). So like an experimental platform, let’s say.

Stephan Livera:

All right. Yeah. So, and also I wanted to just dig a little bit deeper into the Specter desktop app as well. So wanted to talk through a little bit, some of the features that are there. So I’ve seen just from reading some of the documentation, I’ve seen you have a coin selection there and you’ve got labeling as well. So can you tell us a little bit around how those are done and what’s happening with those?

Ben:

Yeah, so we’re just basically taking advantage of existing features in Bitcoin core And making them easily usable. So Bitcoin core, all of that is like allows you to do coin selection, allows you to manage labels. Everything can do through the RPC, which this is how we interact with the bitcoin core. So yeah, we’re just trying to take advantage of all the important features. First of all, Bitcoin core and the hardware wallet, so coin selection, I think it’s quite important. I just means that you can choose which UTXOs you want to spend in a certain transaction. Labeling allows you to manage better manage that the UTXOs and understand like what address you’re sending to, or what address you’re receiving to like the description where it came from. So you can better manage your privacy first as well and just your, your funds as well.

Ben:

Besides that we also support like dynamic or manual like fee settings. So if you want to adjust for better confirmation times, or you just want to do it like manually whatever you choose. We recently added, for example, so on sending transactions, you can send out batch transactions to save gas. So basically just instead of sending if you want to send like five transactions to five different people like to an exchange to cut like service provider, et cetera, you can just do it on one transaction. You just input the amount you want to send to each of the addresses you want to send to, and everything is going for in one transaction which is usually better for fees and for privacy. Besides that. Yeah. Yeah,

Stephan Livera:

That’s an interesting one. I think as an example, you might be, let’s say you’re running a Bitcoin business and you need to do payroll and pay out the employees and you could batch that transaction, let’s say to to the different people. And then it’s all in one transaction. So there’s a fee saving there, although obviously they would then have to think about privacy and so on, but that’s a potential saving there. But yeah, tell us as well about address verification. So I understand that’s something you’re looking at. And I understand that’s also quite difficult depending on which hardware device we are talking about.

Ben:

Yes. So for example, Ledger is probably the worst in that. So it doesn’t allow for verification of multisig addresses at all which we can’t really solve, cause this is something in the Ledger framework itself. But for all other wallets, we just very recently finished allowing full like verification on the device. So we added that to hardware wallet integration as well. So currently where we allow verifying on Trezor on keepkey Specter do it yourself, obviously on Coldcard. We allow we support change verification. So when you’re sending and transmit a multisig transaction you also want to make sure that the change address that you’re using is generated from the same xPubs that your wallet is using, that your multisig is composed of. So you’re not sending to a malicious address to a malicious like multisig if, for example, someone switched the public keys so we want to make sure that the address you’re sending to the change is correct.

Ben:

So we just added a verification of that on Trezor and Keepkey and it’s already available on on coldcard. So yeah, I think the address verification is quite important as you, of course, that the entire purpose of using hardware wallets is not to trust the computer you’re using it form, that you assume it is compromised. So we finished basically adding all verification for all the major wallets basically all of the wallets that we support except ledger, which doesn’t allow that. But for all the others, we are already supporting hardware certification, so we can verify everything on the device itself. So even if your computer is compromised, you can make sure you you’re using it trustlessly basically.

Stephan Livera:

Yep. All right. So just to replay that, because that was probably a bit much for people to follow, they’re a bit newer. So what’s going on is if you’re doing a Bitcoin transaction, generally speaking, you want to look at your hardware device to check the address that you are either spending too, or, you know, or that you’re checking like for a receive address. And so this is a feature where you would before you spend to a particular address or you’re receiving it, it shows you on the device. And so you’re checking that address on the device to make sure just in case something, so there’s some malware or there’s some, you know, hack or attacker on in terms of your desktop or your laptop computer, the hardware wallet should be able to pick it out. And then that other point point was around, there are some attacks that basically try to trick you and basically have the change go to an address that you don’t necessarily control. And so this is a feature where you can try to figure out, I guess, your hardware wallet is trying to figure out yes, I own, or I have the private key that allows me to spend from this change address. Would you say that’s a fair summary?

Ben:

Also, like for the latter part about the change I think what’s also important is not just that you have the private key on the hardware wallet, but also that the co-signers didn’t change. So the other public keys didn’t change by an attacker.

Stephan Livera:

Yep. So in that example, it would be something like, you know, let’s say, I don’t know, maybe if I had set up like a quorum but then the attacker has changed it to say, actually now you’ve, it’s now I have that other key instead of who you thought it had it, and therefore they’re gonna, now there’s like a blackmailing possibility, that kind of thing. And then the other one was around collaborative multisig. So it’s this idea of multi-user support because I guess in practice, let’s say, you know, between the three of us, we set up a two of three multisignature and we are storing a lot of Bitcoins on that. And we want to be careful to never have all three or at least two of us in that same with the hardware wallet in the same room, let’s say. So we want to be able to collaboratively, let’s say I can sign it just the first signature, and then I could pass it to one of you to do the second signature. Can you tell us a little bit about that flow? What does it look like and how does it work in Specter desktop?

Ben:

Yes. So this is basically two features, which kind of compliment each other, but are essentially different. So first of all, collaborative multisig, you can basically import and export the PSBT Bitcoin transactions. You are doing, you can import wallets from others. So for example, you send someone your xPub and they’re creating the multisig wallet and you can import it into your Specter. Then you can just start creating a PSBT and then sign it on your side, send it to the other project to sign. Yeah and collaboratively managed funds. And with multisig support, you can do this on the same Specter instance.

Stepan:

Multi user support.

Ben:

So yeah, multi user, so the multi user support. What it is allowing you is just to have multiple users on the same Specter server. So if you want to share it in like a family office, a small company, or just with friends and family who don’t know how to set up a bitcoin full node or something so you can just do this for them and share the instance with them or in a small company, you can manage funds together on the same instance.

Stephan Livera:

Also wanted to chat about multisignature standards, because up until now, it doesn’t seem like there’s any one unifying or well adopted standard, if you will. I think there’s, you know, Electrum is a well known one and some of the other providers are sort of using something similar to that, but it’s not quite do you want to just comment a little bit on the current state of play there? What does it look like in terms of multisignature standards and what’s needed?

Stepan:

Yeah. So what is really surprising that there is not so many software that supports multisignature so like all normal software wallets that just assume that you use one key and that’s it. Yeah, so that is pretty unfortunate, but good to see that there are now projects that multisig. So on the standard side there are standards for quite a while already how to create multisig addresses. So how to sorts the public keys there and how to how to manage all that and also what the derivation path is to use. And in that sense on the base layer for developers, everything is already out there. Everything is standardized. So what is what was missing is just the support from the software. And multisig itself is pretty tricky, especially on the hardware wallet side.

Stepan:

So as Ben mentioned hardware wallets need to verify the change address and it depends on the wallet, how exactly they they do it because basically you have a situation where you have multisignature addresses where you have only one of multiple keys and there are different ways to handle it. Some wallets are stateless like Trezor and Ledger, for example they don’t save anything in there, on the recovery phrase or like the master key and nothing else. So they don’t save any information about the multisignature addresses. So in this situation, in order to verify that you are your transaction has change, and this change is indeed going back to the same setup you need additional information about your cosigners. So in particular, you need xPubs of your cosigners, and then the wallet can verify that, okay.

Stepan:

Yeah, this is basically the change address. Other wallets, like Coldcard, Specter, Cobo, and Electrum they actually save the wallet. So first, before you start doing the transaction, you actually need to kind of import the wallet into the device, and then the device can verify that. Okay. Yeah, I know this this setup already. I know the co signers and so on. And yeah, this all this information in principle, doesn’t matter if you are stateful or stateless hardware world it is all included in the PSBT already. It can be included in the PSBT so in Specter desktop. We just make sure that all the hardware, wallets receive all the information that is necessary. Yeah. One note regarding the hardware wallet Ledger is probably the only one that is decreasing the security of the multisignature set up if you’re using it there. So I would say that ledger is better to use in the, you know, set up just because they don’t do any verification for change addresses if it is multi sig.

Stephan Livera:

In terms of backing up and so on, let’s talk a little bit about what you need to backup for a multisignature setup. So how does it work right now with Specter desktop for a backup?

Stepan:

So we are using descriptors from Bitcoin core and Bitcoin core descriptors actually contain all necessary information about the multisignature set up. So it includes the xPubs of cosigners, the derivation path, and also the script type either you use a native SegWit or nested SegWit. So in principle, just one simple string is enough to recover through generate addresses center, to recover your wallet. And yeah, that’s basically nothing else. So just a descriptor.

Stephan Livera:

One other point that just came to me from as well from my earlier chat with some of the Electrum guys ghost43 was also pointing out how many Bitcoin wallets today, other than I believe Bitcoin core do this thing where they’ve got a receive address chain and then a change chain, and then they respectively have different output descriptors. So what’s it look like? In Specter desktop on that.

Stepan:

Well basically the same. So the idea is that you have this xPubs of cosigners, and then you derive it with a zero index and then the kind of index for receiving addresses and one index for the change addresses. Bitcoin core, doesn’t use it for the default wallet, but it can use it for a wallets that you import when you provide a corresponding descriptor. And well, they don’t use it for the default wallet because they always use a hardened derivation there. So if you are using this standards default wallet that is created when you launch the Bitcoin core, then you cannot have another software that is watching this address because in order to generate new addresses, you actually need private key. So this is the only problem, but it also is a little bit, well, more secure, I suppose on that side, like hardened and not hardened derivation has certain tradeoffs in sense of, but yeah, you don’t have to use the default wallet that is created in Bitcoin core. You can also just import the private key and specify that you want to use this standard way with receiving and change indexes.

Stephan Livera:

And just on the hardened derivation versus non-hardened derivation. At least my understanding there is Bitcoin core’s developers have, I guess, gone for the slightly more secure option of having hardened as the default. Whereas I believe most other Bitcoin wallets are using unhardened derivation and that’s like a usability trade off. Would you say that’s a fair summary there? Or how would you modify that?

Stepan:

Yeah, yeah, it is very, very precise description of what’s going on there. And I would personally also do the trade off to the side of a non-hardened derivation here, just because I personally wants to have a watch only wallet as well. So I don’t want to touch my private keys very often.

Stephan Livera:

I see. And I guess in practice, somebody might use that if they want to regularly accumulating Bitcoins and they want to be able to, you know monitor that and generate new addresses, that’s where say the watch only function is a bit easier with a non hardened derivation, right. Or non hardened pathway. Right?

Stepan:

Yeah.

Stephan Livera:

And one other point around this whole, like around multisignature and standards, I know with Electrum, there was some discussion that made it a little bit difficult historically to get Coldcard to work as part of a multisignature with other hardware wallets. And as I understand that was to do with knowing what the root fingerprint was. Can you elaborate on that idea and whether that applies within Specter desktop as well, or how are you dealing with that?

Stepan:

So I think the problem there was that Electrum doesn’t store fingerprints, root fingerprints, or doesn’t provide root fingerprints by default because you don’t really need it. So it was and it is in the PSBT standard. So when you’re providing the derivation path for your cosigners you actually or for the device, you actually encode it as a fingerprint and then the derivation path and it is used to detect which of this derivation paths to use. So it is more like a cross compatibility issue between Electrum transaction parsing and PSBT transactions. So I don’t think that it is related to like actually verification and security issues. It’s more like compatibility issues between standards.

Stephan Livera:

Yup. And also you were touching on output descriptors earlier, so that’s like a one way of describing the wallets type. And you’ve mentioned, you know, you’re, you’re looking to use that natively. So what sort of features and things are possible with output descriptors? Why is that a good idea to use?

Stepan:

So output descriptors basically this is another standard that is adopted by Bitcoin core and hopefully will be adopted by the rest of the industry that allows you to just having this output descriptor to derive addresses or however many addresses you want. So yeah, it simplifies the backup mechanism and recovery mechanism for complicated scripts. And the most important ones are actually the multisig addresses, multisignature descriptors sorted multi that is more standard. But also in principle, you can include their custom script and what would be really, really awesome if we get a miniscript support there. So I think there are plans to include a manuscript to kind of combine miniscript and output descriptors. And then with the same language, you can actually specify not just Single sig or Multi signature, but you can also have a pretty complicated policies, for example that includes timelocks or some additional backups keys or policies like either two of three or a four of five that are different key. So basically it’s something more involved and more complicated, and that would be nice to have. And I think that’s, we are getting there. So I already saw the pull requests that include miniscript into Bitcoin core or, but, you know, Bitcoin core and big changes, take time.

Stephan Livera:

Back to the question of in practice then, what does it look like for a backup? So other, I know, for example, with caravan, if you want to do a backup, they have, I think it’s like an export of a JSON file and that JSON file .JSON JSON I think it stands for Java Script object notation, but anyway, that JSON file contains the xPubs. So what does, so I guess then the user who has created the multisignature, they have to basically just make sure they keep the back up with that on a USB stick somewhere and so on. What does it look like for Specter desktop?

Ben:

Yes. So we have like the minimal backup is basically what’s a term we have borrowed from a fully noded and blockchain commons and account map, which is basically like their own format, which they use. And we integrated it into perspective as well. So it just stores like a title, the descriptor of the wallet and like a block of the birth of the wallet. So when you created the wallet or when the first transaction is made in the wallet, you also add that. So this is just for to make rescan faster, so you don’t need to rescan the entire blockchain, when you want to import it again, some wallet you can just rescan from the first transaction. So yeah, we support this format, like the minimal exporting method. But also we can, you can like Specter itself is using some more information just which is not necessary. I mean, you can import just from account map, but you can also do this from the more rich format, which is also JSON of Specter which you can just download again from the UI, from the settings like a full backup of all your devices and wallets. But yeah, when we also of course, want to make it interoperable with more like with Caravan and others so that you can back it up in other softwares and not just as a file yeah, and fully noded, for example, you can just scan a QR code. You don’t have to download the JSON, you can, but you don’t have to. Yup.

Stepan:

But the QR code actually contains the JSON file inside?

Ben:

Yeah, exactly, exactly.

Stepan:

The minimal amount of information that you need is xPubs, number of signatures required and type of Multisignature. So Caravan is providing, there’s very minimal information. You can include more if you want but it is optional.

Stephan Livera:

More of a broader comment. So in the industry over the years, I guess most people have been operating on single signature because maybe they’ve been, for whatever reason it’s been technical or they’ve been scared about, you know, moving their set up and stuff. And so they would have been coming from this mindset of, Oh, if I’ve just recorded my 12 words and the passphrase, or my 24 words and the passphrase, that’s it. And I can understand perhaps the concern of someone like Thomas Voegtlin from Electrum, he’s concerned with something like, Oh, you know, we want to have the backup be easy for people so that they only write down these words and that’s it, they don’t need to have like the words and the derivation path and the, you know, and then all of a sudden, now we’re coming back into now only technical users know what to do. So I’m just wondering what your thoughts are on that idea. And you know, is it basically in your view then, is the practice going to be going forward that let’s say multisignature becomes really popular? Everyone does it, does everyone just get into the habit of saving the JSON file? Is that basically what we have to teach people as well?

Stepan:

Not necessarily there are standards for a derivation process for multisig. So if you’re not a techie user, you’re probably using defaults. And then you can just have this if you have sheets of paper with their recovery phases with the 12 or 24 words and then if you want to recover, you just need to remember was it two or three or one of three or something like that. So already order is not important, so it’s not important if it is one to three or one, three two and so on. The if you’re using defaults will be directed to magically. So in principle yet just having three sheets of paper with your recovery phrase is enough. And if you are more technical, then you can go further and use the additional accounts and calculate derivation paths. And then you need to recover using a more complicated procedure and say some files probably, but then you’re already (inaudible). So I would say that at the moment, if I remember that these three recovery phrases were used in my two or three Multisig, then I can recover it.

Stephan Livera:

I see. Yep. And so then really the main concern then is just if a, let’s say a non technical user, and this is not really relating to making it easy. I guess it’s more just, if a non technical user has done say a two of three setup, they’ve lost one of those three hardware devices and they didn’t have the seed back up for that device. Then if they didn’t have the JSON file back up, they would not be able to recreate and spend with only two of the three keys, which they might naively think, Oh, I only need two keys. Right?

Stepan:

Yeah, that’s true. So that is actually a good point. I didn’t think about that. So if you lost, if you lost one of these seeds and you don’t have in your software already set up, or if you’re completely wiped everything and the last one of the seeds then you have a problem. So then probably it is better if you have some kind of a PDF that prints out information of public keys as well. But maybe for the backups, as people tend to put it on paper or something it would be easier to have something like a, not a JSON file, but maybe a PDF or some human readable.

Stephan Livera:

Yeah. I guess that’s one other point as well, because if people are coming from single signature world, they’re just thinking, Oh, I’ll just write down the 12 words or write down the 24 words. But if it comes to the point where someone has to manually write out an output descriptor, that’s probably getting a bit much. Right. So I guess these are just things that people have to think about when they’re doing backups, right?

Stepan:

Yeah. Yeah. Multisignature in that sense is a little bit more complicated. It also improves the security, right? Sure. Incur increasing security and linear increase in complexity over backup.

Stephan Livera:

Yeah. Yeah. So I guess it just means as an industry and a, you know, for, for listeners who are out there trying to teach their friends how to use Bitcoin, well, they’ve got to make sure they save that backup file and so on. So that, that way the, you know, their friends are protected. And so I think the other interesting part about Specter Desktop is that it seems to me, the focus is really, is just multisignature right. Whereas if I compare with something like Electrum, it’s got, you know, they’ve got lightning, they’re doing like, they’re doing a bunch of other things along with it. Whereas I see it like Specter, desktop is focused a bit more on to multisignature only. So I guess, arguably that means we are reducing the attack surface and trying to only do one thing. Well, would you say?

Ben:

So yeah, I think first of all we’re of course we’re also supporting like Single sigs for hardware wallets. So if we want to use it with your prospects, so just as a Single sig, you can do this too. But yeah, we try to like first of all, we try to minimize like everything that is going on on our side. So we don’t even like have a crypto library, which we’re using, we’re using Bitcoin core currently for basically doing all the heavy lifting. So we don’t have like a very critical code, which needs like very thorough testing because we just offload whatever we can to the battle tested Bitcoin core. And yeah, we just focus on making it easier to use. Basically we were trying to minimize that attack surface, which Specter adds on top of using just Bitcoin core.

Stephan Livera:

Cool. And in terms of user experience and user interface, what’s the feedback been so far on Specter?

Ben:

I think like, at least first of all like considering the fact that both me and Stepan aren’t like designers or UX experts at all, I think this, we did like a fairly good job. I think, like the UI is pretty convenient, like personally when I just onboarded myself. And when I like checked with other users, like we’ve got very good feedbacks, there always something to improve. And I think, especially what is confusing is importing xPubs. So when you need to import the public keys especially from airgapped devices in order to create wallets. So this concept is quite confusing especially to a new users who are not so familiar with that. And we are still thinking on how to simplify it. But compared to like command line and even Bitcoin core UI, I think we are already like very convenient and got very positive, like feedback from users who onboarded like themselves and also just their less technical family even. So I think we’re doing pretty good on that. And if anyone who listens to that happens to be like an open source designer we’re really, really happy to like, to get help on that.

Stepan:

Yeah. I would say that at the moment, the interface is becoming a little bit too busy, so we are adding new features, new options, more things. So we already have plenty of buttons, several words, some weird tables and so on. So at some point we need to take a step back and rethink the the UI. But there are also always other things to do, like bug fixing and making sure that it is reliable and fast and so on. But I’m personally pretty happy with the interface. Yeah, it could be better but works.

Stephan Livera:

For sure, so where would you say, where to next for the project?

Stepan:

One important thing that I’m really missing is replaced by fee. So at the moment when the fees on the Bitcoin blockchain are going crazy up and down or orders of magnitude, you know, sometimes I see the transaction and I need to wait for a day. But I was just trying to refill my phone for example, or something. And I would like to be able to pump the fee and Bitcoin core supports this, but there are certain problems with implementing that in Specter at the moment. So that feature would be really nice. Another one that is really, really awesome. And also I personally wanted desperately is a proper support of the pruned nodes because yeah, I personally run it, as I said on the very cheap VPS server that only has like 25 gigabytes of storage. And at the moment, if I’m importing an old wallet I can’t really do it. So I need to redownload the full blockchain for that. So supporting the pruned nodes is already another very nice thing and bug fixes because you have more people have started using it and we have a wide variety of platforms that we need to support and test. So like Windows Mac and also ARM Linux. So all this stuff is pretty complicated, but so sometimes we find some bugs and we’re fixing that. And yeah in the future, Ben maybe you can also continue.

Ben:

Yeah. So we’re now working on finalizing the desktop app which should make it much easier to set up, like as easy as any other desktop, I believe. I think like generally we have like probably the most like versatile hardware wallet support? But I think like as more companies create more hardware wallets more options are available. We will want to add as many as possible. Another thing that I think would be really cool is mobile support. So right now you can use, you can like set up Specter as a server on like on your machine or your laptop or anything, and access it from mobile. But we have very bad UI for small screens currently. So maybe in horizontal mode, you could use that, but it’s not really proper support.

Ben:

So I really hope we will have some better mobile support in the future. And besides that, we just, yeah, I hope it will be much more stable. We’re currently like, as well as more users are being onboarded I guess new bugs are kind of arising and we need to take care of that every time. And they become like stranger and stranger. So like something which happens on a very specific type of machine, which we didn’t like check ourselves, which we don’t have for example, or something. But I think we’re handling that pretty, pretty well. And I hope that it will be a much more stable in the future. Yeah, besides that, I just hope to onboard more users whereas just grow up the community of the project.

Stepan:

It would be nice also to have a few more contributors.

Stephan Livera:

Yeah, yeah. Sure. Of course. One other thing that just came to my mind now as well. So some of the, so I guess just thinking about when you’re maintaining your setup some of the guided multisignature platforms such as, you know, Casa or Unchained capital, they have a concept of like a key check or a health check where you might periodically go and check that the key still works. That there has been no bit rot. Or things like that. Is that something you would look at a building into expected desktop.

Stepan:

How exactly does it work?

Stephan Livera:

I think, I think it essentially signs a message to check that the key is still intact.

Ben:

Yeah. You can always like create a test PSBT for example, without actually sending it you can always like verify addresses on your, like on your device to check that the private key is matching. You can verify also that like all the addresses, the new addresses, you can obviously see them on the device to check that the device, a private key is matching basically. And you can always like do a test transaction. You can always like sign transaction without actually propagating it. So just save it or delete it, whatever you want, you can manage like pending transactions. Well, pending might be confusing. So just transactions, which you created in the past, you can save them for later. Or if it’s test, you can just delete it after you finish signing with everything. So we could maybe add some like more easy, easily, like a health check, but I think you could just use the, do like a very tiny PSBT and then delete that after you’re done.

Stepan:

Or spend the transaction to yourself.

Stephan Livera:

Yeah, exactly. Yeah. So that’s another idea. All right. Well, I think those are the key points I wanted to touch on. If listeners would like to find you online, they would like to contribute. Where’s the best place for them to find you guys?

Stepan:

Telegram group.

Ben:

We have the telegram as support channel for the community. We have the github page, which I use to just open issues if they want but I think we are mostly available on telegram. Like we respond there the fastest. And I guess like, if anybody prefers like privately, like my DM on Twitter open, but yeah, I think the Telegram is probably the best.

Stephan Livera:

Excellent. All right. Well, I’ll include those in the show notes for listeners. So Stepan and Ben, thank you for joining me today.

Ben:

Thanks for having us here.

Stepan:

Yeah. Thank you.

Stephan Livera:

Get the show notes at stephanlivera.com/205 and I’ll see you in the citadels.

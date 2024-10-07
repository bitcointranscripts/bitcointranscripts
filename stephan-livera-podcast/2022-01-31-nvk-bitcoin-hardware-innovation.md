---
title: Coldcard Mk4, Tapsigner, Satscard – Bitcoin Hardware Innovation
transcript_by: Stephan Livera
speakers:
  - NVK
date: 2022-01-31
media: https://www.youtube.com/watch?v=2cp2FoUgAYM
---
podcast: https://stephanlivera.com/episode/344/

Stephan Livera:

NVK, welcome back.

NVK:

Hey man. Thanks for having me, dude. It’s been a while.

Stephan Livera:

Yeah, it has.

NVK:

I’m still winning on the amount of appearances consecutively.

Stephan Livera:

Yeah—actually I don’t know. I haven’t run that count actually. It’s been a while. But yeah, there’s so much going on with the world of Bitcoin, and obviously there’s always improvements going on in terms of hardware security, new technology coming, and how are we dealing and adapting with that, and how’s the software going to work with that hardware, and all of this. Maybe you want to just open up and tell us a little bit about what you’ve been working on lately? What’s been on your mind, and what have you been working on? What are the key things from a Coinkite point of view?

NVK:

We’re trying to explore two things in parallel because we think they’re important and they’re under-addressed in the market. So, as usual, we have (1) the ColdCard track, which is like, How do we make it arguably the best, most secure hardware wallet in the market that is fully open for you to verify and all that good stuff. And we are exploring further security on that, and some interesting UX aspects. We’ll get into it. And then (2) on the other track, we have this idea that started with the Opendime, which is the ultra, true, minimum common denominator of like, How do you make it really easy, as like giving somebody a bank note, for Bitcoin transactions and gifting and all that stuff. And we’ve been exploring technologies and stuff, but we couldn’t get it to a price, into a shipping format that would truly, truly be cheap even for the developing world. So we started exploring that direction as well with Satcard and Tapsigner, which we’ll get into. So that’s where we’re at now, aside from another pile of things.

Stephan Livera:

Yeah, of course. These are the key things, and I’m sure we’ll get into some of the techniques and standards involved as well. Maybe we should start with the ColdCard, the new ColdCard Mk4, what you’re willing to share so far with it. Could you give us an overview—what’s new here? What’s going to be the improvement with the Mk4?

NVK:

Yeah. ColdCard is already what people like to use for security, especially us. So we didn’t want to just simply change everything and go, Oh, let’s put a camera, let’s put a big screen, do this, do that. No, it’s a product that a lot of people trust with a lot of money. It sort of became the standard, but we had a few things that were really bothering us that we wanted to really improve. So even though it looks just like an incremental update, it’s actually quite a lot. And we fought tooth and nail with suppliers with some clever supply chain acquisition strategies as well to maintain the price nearly the same, giving you a shit-ton more. So what we did is—the first thing was the connector. So Mk4 is going to have USBC. I think we’re ready for that, everybody wanted that, we could find the economics to make that happen. The other thing was memory. Mk3 was designed a while back, the economies of scale worked that way. But it became clear to us that a quarter of our user base really wants to do multisig, and wants to do multisig with setups that are a little bit more complex. So they need a lot more memory in order to make those transactions and get them signed with all the UTXOs that they want. So what we did is we jumped a family up on the microprocessor that we use. It’s substantially—it’s probably a 100X everything. So it’s more than double the speed. It’s what we call now, infinite memory. I’d say a hundred times more memory, probably. Essentially now, we have enough memory on the device to make a Bitcoin transaction that will be as big as the Bitcoin network could accept. So ColdCard is no longer the bottleneck for Bitcoin transactions when they are very complex. And this doesn’t really affect most people. This is really related for multisig and complex multisig transactions with too many inputs. So if you’re using CASA on-chain and you’re doing a lot of big things moving UTXOs around—that resolves that. We also wanted more memory to do a lot of other more interesting features that we’re still working out. And we’ll talk about it a little bit later. That’s the trend here with this device. The flash memory is much bigger, so we can process the firmware upgrades much faster. Settings memory is a huge deal. It used to be just 4K. Now it’s 512K. That’s a lot. And we can put a lot of things that we had to keep encrypted in a very complex way in the MCU or in the IPRAM memory—we can move those into secure elements as well. We can do a lot more clever things.

Stephan Livera:

Yeah. Let’s talk a little bit about some of those aspects. So you mentioned around the unlimited memory, or just dramatically improved memory. And so this might be important then as we’re moving into the new world with a lot more people using multisignature, because those transactions are a lot bigger. And especially if somebody’s got a lot of UTXOs—a lot of coins—and all those UTXOs need to be individually signed. And historically, depending on what hardware wallet you were using, if you were doing a lot of UTXOs, it would take ages to sign. Or sometimes it would just cark itself—it would not make it.

NVK:

None of them can make a full 2 MB multisig transaction with all the stuff in it, like multi-UTXO—they just can’t. Every single one will fail, because it just wasn’t a requirement when a lot of this architecture was designed. And there’s also a cost. I can make you a computer-level hardware wallet, it’s just you’re not going to want to pay that much. So we’re still working with the economies of scale here in the economics of the product. Right. So we’ve achieved that. I think this is a huge thing. And because—when you jump up an MCU family, you get a bunch of other stuff too, extra. So you get more speed—it’s double the speed, you get more features. We have more hardware acceleration for SHA256. Yes, we don’t use those for actual Bitcoin things because we don’t trust those, but we can use those for decrypting, for example, encrypted data inside the device. So it makes the whole experience a lot faster. Things that felt like you were waiting for just happen, which is really cool.

Stephan Livera:

And that may also have an impact in a Taproot, Tapscript world. We’re moving into a world where people are doing more advanced things where they have advanced spending conditions and things like that. I wonder, is there any factor—

NVK:

It’s funny because Taproot, like Schorr, really, is a lot kinder on the hardware. We actually don’t even need all this memory for Taproot, unless you’re trying to make a big transaction—that’s still a bottleneck. But for normal multisig transactions, they’re going to be a lot smaller because Taproot is linear, while RSA is exponential, on how the signatures are aggregated together for each UTXO. So it’s just kind of interesting how this stuff really compounds. But yes, ideally we can even fit more of the policy logic and all the complex stuff that we yet don’t know that you could do with Taproot. So we’re hoping to get the market to inform us which direction we should go with that stuff.

Stephan Livera:

Yeah. And so the big shift as well is the USB-C connector. A lot of people are used to doing the Micro USB, but of course times changed and now it’s 2022 and I’m sure a lot of people are having to charge different connectors—their mouse, their phone, or whatever—with USB-C. And so now they want to be able to use that same connector plug to plug to their laptop or for power purposes.

NVK:

The next thing that’s really cool about Mk4 is that we are upgrading the security substantially. We’re adding another secure element, so it’s going to be dual secure element. And what’s fun is that we already had that architecture where we don’t trust the secure element, so the secure element and the MCU play against each other. Now we’re adding yet one more from a different vendor. So essentially you have two secure elements plus the MCU, and they’re all playing against each other, and they’re from different vendors. There’s an exponential increase in security here, because even if you do know a back door in each of them, the way we design it, the back door is still useless because you still need to know the encryption keys and blah, blah, blah. But let’s say, all things being considered, Dr. Evil is sitting on your billion dollars inside your ColdCard. You know what I mean? Now he needs to break three separate things and they all have to work perfectly—it’s exponential. It really is cool. And this new secure element that we’re adding has a lot more memory and features, so we can add even more features to the ColdCard like trick pins that are dynamic so you can choose the order in which your security labyrinth works in the rest. You’re going to be able to say, If I type this pin, I want this to happen, and then that to happen. So, maybe don’t brick yet, maybe just show the duressed wallet and then brick kind of thing. There is a lot of cool stuff you’re going to be able to use, and design your own duress path security that is really fitting to your life.

Stephan Livera:

Yeah. And in terms of the users who want to do air-gapping, they can still use Micro SD as they already can with the preexisting [method]?

NVK:

It’s exactly as people love. People have their ColdCard hidden under whatever, and then they still can load the transaction to a Micro SD, travel to their place, do the signing, travel out, and never touch computers—all that stuff remains the same. It’s actually improved a lot speedwise, too. There’s a lot of nice little improvements on that. And we’re working on a few other multisig features that are going to take advantage of the Micro SD card. So you’re going to be able to do some multisig—clever things. We’re just not putting it out there yet because it’s still in the works.

Stephan Livera:

Yeah. And then NFC—I noticed you put out an NFC standard, and you’re looking at NFC for the ColdCard Mk4. So do you want to talk a little bit about that? And I guess some people might be thinking, Whoa, hang on, is that a security concern? Because now I’m opened up to NFC?

NVK:

Yeah. So we started exploring ideas and what other connectivity we can do that is safe enough for your device, but that does make it easier. And we have essentially the user base split in two: half of the user base, it’s like real money HODLing on a computer, using a computer to sign—they’ll never use a phone-related device for that. And then we have the other track of people who—like your average pleb with a bit less money, trying to sign it with their phone wallet and keeping it that way. Phone wallets with ColdCard are a bit harder to use—it’s possible, but a little trickier. So we started exploring NFC a while back, and we fell in love with the technology. It’s quite amazing really, especially if you do it in the way we’re doing it, where we are essentially not respecting the NFC body and going around them. We’re essentially leveraging everything in NFC without bending the knee. We figured out how to do that, and it’s really cool. So we call it NFC-compatible. And we published the spec so that other wallets can do the same—everybody should be doing this. So with NFC, you’re going to be able to just tap. You tap to sign, you tap to share an address. You just tap—it’s super easy. It’s a lot cheaper. The module for NFC is very economically relevant. We have our own antenna network that we designed. And unlike a camera where it costs a lot more, it makes the device more complex so there’s security concerns around that. Anyway, the cool thing though is like—for example: for my HODL, I don’t trust. Even though NFC comes disabled by software by default, I don’t want to have to trust the software. It’s trust no one, right? So we’re adding the means for you to physically, permanently disable the NFC as well. So you can literally kill it—it doesn’t work, it’s both software disabled and then you go and scratch this thing that’s irreversible. And maybe you have two ColdCards. That’s my plan. You have one for your HODL and you have one for your operational that you tap with phones. We think it’s super powerful that way. And we do have one more way of you doing PSBTs now, but we haven’t talked about it publicly yet. We’ve built a virtual disk on USB mode. So essentially, if you’re in a pinch, or this is not your HODL device that you connect to the USB, you can just plug the ColdCard, and it will display for you a virtual disk on the computer that you can just dump the PSBT in, it signs, it puts [it] back there, you publish transaction—done. It is so easy to use for that stuff, it’s ridiculous. So we’re pretty excited about that. And of course, the way that this virtual disk works is properly secured. It’s not like a normal USB drive and all that stuff.

Stephan Livera:

So let’s walk that through. So as an example, you’re using Electrum or Specter or Sparrow, or one of these, and we are directly plugging in the ColdCard and we’re dragging a PSBT file over into that hard drive. And then on the ColdCard, we’re looking and saying, Do you want to spend 0.01 Bitcoin to XYZ address? Yes or no—you hit Yes. And then you have to move that PSBT back into the wallet and then broadcast it? Or how does that look?

NVK:

Actually the file shows up there and just broadcasts it. You don’t have to broadcast with the wallet. So, why did we do this? A few things: one is you can use it with Linux CDs. So Tails or whatever, without having any ColdCard drivers or anything like that. You can use it with Android phones, because disk mode exists for USB. So you can just save two ColdCards on an Android phone. So even if you have NFC disabled, then you want to do that—it’s fantastic. The way we’re looking at this is optionality. All these features come turned off, disabled by default. USB’s going to come, I believe, disabled by default as well—even normal USB. So if you want to activate some of this stuff because it fits your lifestyle, your needs—you activate them. If you want to permanently disable them, you can do that too. We just want to create ways for people to figure out what works for them. And that will inform us which direction to go next.

Stephan Livera:

Yeah. One tip I’ve been using when I coach someone who’s new is I might say, Okay, if you’re a beginner, just directly plug the ColdCard. But let’s say you’re intermediate, you’re advanced—you use the Micro SD. So in this same kind of scenario, you might coach that beginner, Okay hey, go and enable NFC, because you need the easy way to do it. And then for the advanced person they already know—they do their own thing with the Micro SD or whatever.

NVK:

The goal is: it would be really cool for you to be able to just tap to sign on, say, BlueWallet. Or even better, you can tap to co-sign. The possibilities for multisig with this stuff are absolutely huge. Huge. Because it’s an open standard like PSBT. Technically the phone doesn’t even know what’s going on because we are using a Plaintext protocol. So it’s secure. The transfer is very good. So we think that people are going to end up using hardware wallets more with phone wallets, as opposed to just trusting phone wallets because it is more convenient. That’s the idea. And right now with this version of Mk4, the NFC is passive-only. So this is not a master NFC—it’s only a client NFC. We hope that maybe in the future, if this plays out, we make ColdCard be a master NFC as well. And then we could actually have other things tap a ColdCard—not there yet. We’re still exploring it to see where the market goes.

Stephan Livera:

While we’re on that point as well just around NFC and support: so presumably then you want to have support with say BlueWallet or dongles or plug-in connectors that you could connect to your laptop or your desktop, if you want to use it with the likes of Electrum, Specter, Sparrow, and other multisig coordinators. So what’s the software support looking like—if we survey the Bitcoin wallet world—what’s the software support looking like for NFC?

NVK:

It’s early days, but BlueWallet already has NFC or a beta version of it—I can’t remember now. They’re just waiting for devices from us to start fully testing. Zeus just announced NFC. They showed the demo on Twitter. I think there are a few big players. I’m not sure if it’s public yet, so I’ll just keep it at that—a few extremely big players in the Bitcoin app space. I think it’s probably one of the biggest ones, is exploring NFC as well. There is a lot of uptake on this, because I think that everybody who understands economies of scale around hardware wallets, signing devices, and phones, pretty much understand that the only path that’s economical is to do NFC, Micro SD, or something else. The camera really is not an economical path. So that’s the direction that a lot of players are going into—that haven’t hit the market yet—but things are coming.

Stephan Livera:

Yeah. That’s interesting to see. So we’ve got all sorts of different levels and uses here. As you were saying, some users might just be like, Look, this is just—I’m HODLing. This is day-to-day spending and receiving money, and I’m okay with NFC, and that’s fine. Just single signature, just to keep it simple and easy. And other users might say, No, I want a passphrase as well, or, No, I want multisignature and I want to have my coordinating app. And who knows, maybe in the future, you could have BlueWallet as your coordinating app and go around to your three different devices in three different locations to sign and tap to sign. And then you’re saying, Okay, I’m using NFC, but I’m multisig with 3-of-5 or 2-of-3, or maybe in the future some of the devices are using a QR code and others are doing NFC. So I guess that’s like a high-level way it could look.

NVK:

All that stuff that we invented with ColdCard, like for example, exporting the skeleton file to Electrum or to Sparrow, or exporting the wallet descriptors for Core—all that stuff that was invented for ColdCard Mk3 essentially now just goes through NFC, if you want. So the way we’re playing this is: whenever you are on a screen that is a data exporting screen, you have options. You can show a QR for that data on the screen, you can NFC it out, or you can Micro SD it out. So we’re just like, Here’s all your options. It’s as disabled—or not—as you prefer. It’s the freedom way of handling things. And what’s nice is they’re truly securely-disabled, too. I’m the biggest paranoid person here. So I don’t want any of that crap on that ColdCard that’s for real money. And I’m going to literally go through and make sure everything is off. So we are just using this approach now for everything. The more time we’ve have this product to market, the more we have learned on how real people want to use it, not the people asking for features, but the people actually using the devices. We have these open conversations with people offline, and it’s very informative. Because we learn about it through actual pain on those things. Talking about pain, the key pad on Mk4, the presses are going to be a little lighter, and we’ve expanded the hole a tiny bit so it’s a little bit better to press. Some people may have lighter hands.

Stephan Livera:

So soft hands have got to be strong hands, as Bitcoiners. Yeah, I was just saying, to your point earlier around the ease of NFC, I think that might be an interesting one then from a wallet designer point of view. So let’s say Electrum, Specter, Sparrow, BlueWallet—they might now coach the user through the setup a little bit more easily, because instead of telling that user, Oh hey, now get a Micro SD card, connect that to this, connect that to—now it can be more like, Hey, just tap your ColdCard to this and then done. Right. And it can go both ways. Because it can extract data from the ColdCard, let’s say the XPUB and that data, or it can send data to the ColdCard—the transaction data, the multisig coordination file aspect.

NVK:

People really have this romantic idea with QRs and cameras. They haven’t really actually tried to do a transaction with QRs. It’s too much data. It takes too many QRs. And the cameras are shit, and the displays are shit. QRs on phones are fantastic, because the phone is like a super computer and it has these beautiful screens. But when you do that on a cheap, small secure device, the experience is shit. It’s cute and all when you’re doing a singlesig transaction for a tiny little amount of money, or just a single UTXO—whatever. But when you’re actually trying to give, say, an Electrum file to a wallet, or a descriptor, or bringing back a full PSBT that’s larger—we couldn’t make it happen in a way that was acceptable. We have a lot of different technologies that we have experimented with internally. And this was the best experience we could come up with that was economical.

Stephan Livera:

I might just add some experience to there as well, because obviously I’ve played around with a lot of these wallets. I’ve used a lot of them, and I’ve spoken to people, and I’ve heard different experiences from people. Because some people will say, Oh, look how great it is. But there is also the difficulty around sometimes the lighting in the room isn’t right, if the angle isn’t correct. If the camera is some old laptop that you’re using and it’s got a really bad webcam, then it won’t be able to read it back in. And there has been some work on that. I know there were efforts to try to standardize some of these things. I know some of the Blockchain Commons guys are trying this, and I know obviously the Specters and Sparrows of the world are big into this. But I’m actually curious to see where this goes with NFC, because it might actually make it accessible—if a lot of smartphones just have it by default, then maybe that is a practical point.

NVK:

I think it’s a leap [frog] technology. It’s just so much better, and it was literally designed for this. While the QR stuff is trying to solve a problem in a way that it’s just not designed for. Because again, the hardware wallets, the cameras that they use are really crappy, because they have to be cheap. It’s understandable. And the screen for you to try to figure out what’s going on is also not great, because it’s not a beautiful phone screen. So the point is, I think we’re just trying to—not trying to fit our preferences into the tech—it’s trying to get the tech to inform us what’s the best way of doing this. And I think NFC is very interesting for all this stuff. What else did we do? Oh, there’s going to be a very cool slide cover. Check it out: a calculator.

Stephan Livera:

Just like a calculator, yeah.

NVK:

So this is really cool because people are going to be able to customize it. It’s nice, it protects the screen for shipping, and we are using super, super premium polycarbonate as the material for the device. This is not cheap plastic, like other things. The device was super solid because we have a super solid new industrial designer. So we definitely upgraded the finish of the plastic too. It’s more clear, so you can see a little bit more inside. We still want it to be fuzzy, but it’s just a different design. We added an LED for the USB now. So if any data goes through the USB, the device knows and shows it to you.

Stephan Livera:

Interesting. So what’s it showing? Basically, if you just plug it in and it’s power-only, it doesn’t come on. But you’re saying, if there’s data transfer, then it shows?

NVK:

Exactly. It’s very nice. It’s just a peace of mind, just in case you had the USB connection [enabled] and you forgot to disable again, because you were just trying to do something somewhere. Now at least you have something telling you, Hey, I’m sending data, I’m receiving data. So it’s just nice little improvement touches that we feel like people need it and want it. We have a better supplier of the same display as well, and the display now has a connector instead of being soldered on. So, it’s substantially more pro, let’s put it this way. I think people are really going to like it. It feels a lot nicer on the hand, too. I don’t know why. It’s not a huge difference in terms of plastic design, but it does have that super-tough vibe to it.

Stephan Livera:

Yeah. It’s interesting as well that it’s at the same price point, then. Essentially a similar price of the Mk3.

NVK:

But inflation–adjusted it’s the same. Like, all of our suppliers increased the price. And what we did is we essentially bought pretty much a year’s supply of parts last year to build this. We took some risks and stuff, but we’re good at supply chain, so we know how also to resell parts we change our minds on. We actually made a buck on that. But it’s an interesting challenge. It makes making hardware—physical things in this time and place, in civilization—definitely not your usual just send stuff and get it back.

Stephan Livera:

Yeah. And I’m sure the microprocessor shortage—or at least it happened with Raspberry Pis. So that is a real risk.

NVK:

Yeah. So we essentially de-risked everything by just [being] like, We’re going to just own inventory. A lot of it. And we’re just going to trade inventory if we need to. We’re going to become—fuck it, we’re going to become a parts bank. You know what I mean? And it’s great because they do hold their price very well. So it’ll be hard for others to compete on that, which is fun as well.

Stephan Livera:

Yeah. That’s an interesting angle to see where it goes with that as well. So I think those are probably the key questions that people are thinking in terms of the new ColdCard. And I guess probably the other one is people are thinking, When? What’s the shipping time? Or when are people going to be getting the Mk4?

NVK:

So we started production of the first batch. But because there’s a lot of changes to the firmware because there’s a new secure element so the boot ROM has a lot of stuff we want to do with it, it’s still going to take a little longer. But the bottleneck is going to be software, not hardware, which is a good place to be in, because we can start making inventory. People know we ship. So it’s a different—it makes me happy that we have a good relationship with our customers. So people understand. They’re not even rushing us. It’s like, Hey, we’re building the inventory, we’re building the devices. They’re going to be all ready, and then once we are ready—to start programming them all and start shipping them out. We are never going to rush things, because if the firmware is not ready, it’s not ready. But I hope to have a better timeline in a few weeks. Like in a few weeks, I should be able to say, Hey, we’re thinking about this month, that month kind of thing. But everything is slower now with all this bullshit going on.

Stephan Livera:

Okay. So let’s talk a little bit about some of the other products. So you’ve got this Satscard and Tapsigner. So do you want to just talk us through, What was the high-level insight? Is it basically—as what you were saying earlier—the economics of it around having NFC devices that are cheaper? Is that the main finding and logic there?

NVK:

Yeah. So here’s the problem: everybody wants to use Opendimes to gift Bitcoin. And this Christmas was an absolute rektage of our inventory. They took it all for Christmas, which was a lot of fun. And Opendime is absolute shit margins. We make it because we love it. It’s not exactly the kind of product that we’re like, Hey, this is going to make this company become a Fortune 500 company—no. So it’s not going anywhere, either. It’s a product of fashion. We love it. It’s our little cypherpunk stick. However, we want to make something that scales, that is marketable, and that works outside of North America. So that developing—I wouldn’t say the poor, sorry, I don’t have something for you yet—but this is something the developing world can handle, price-wise. We’re still finalizing the price, but we’re getting very close to it. We took years, really, for us to find the right smart card chip. And we have found the one we like, the one that works for us, the one that’s economical, which is the most important part. And it’s EAL6 certified, so it’s super secure. It’s the same certification the Ledger has. What we’re trying to do is—it’s two products, really. There’s a small variation on some stuff. So one product is the Opendime replacement. So essentially this card is going to be cheaper. It has 10 slots, so you can reuse it 10 times. You don’t have to trust it because you give entropy as well for the nine slots—the first slot is created by the factory, but we do use chain code. Which is kind of cool: there’s a level of trust minimization. But still, it was picked by us—the key. But it’s the only way we can put a QR on the back. Because if you pick the key, we don’t know the address, so we can’t put a QR on the back. And we wanted to make a thing that is derisked, because people are going to use it for small amounts of money, especially on that first key. But it’s super easy because you receive a card, you take a picture of it—boom—money deposited. And then when you want to unseal it, you put the PIN and you take the money out. So for gifting people Bitcoin, it really is next-level easy. And then, if you want to use it a little bit more interestingly and without trusting so much, then you use the other nine slots on the secure element where you can put new keys that you provide the entropy, and you can unseal those and do other crazy stuff. You can put Rare Pepes on them, for all I care.

Stephan Livera:

So just one question on that. How does the user actually interact with the Satscard? Are they presumably using something like BlueWallet to tap it and interact with the card in that way? Because obviously it’s just a card—it doesn’t have buttons or anything. So how do you use it?

NVK:

It’s two things. One is: you would use an app wallet to use NFC with it. But there is also the QR code that you can just take a picture of. So it has a quick way of interacting with it, and then there is the better, more secure way which double checks everything—which is the NFC. And for this product, we are actually releasing a new NFC spec as well, very soon. It’s a specific NFC spec that we’re going to need app wallets to integrate, and I’m pretty certain they probably will, because it makes sense. And it’s going to make more sense to you when we start talking about the next product.

Stephan Livera:

Yeah, for sure. And that’s been historically one of the things—I know this has been a Coinkite position in your thinking on it, is that you don’t want to go and make the proprietary software. You would rather just make the hardware and let other people make the software. And so I guess now you’re in this position where you’re making a product and hopefully you want software wallets out there to take this standard and to use it, because you don’t want to have to go and make your own wallet. You would rather some other already existing wallets integrate.

NVK:

This brings us to another very exciting thing: we want to find new business models that are more Bitcoin-specific, works with Bitcoin economics, and help the space flourish. So we’re exploring rev-share based on hardware activation. It’s still early. We’re still not sure exactly the numbers or the economy, like how it’s going work, but we want to find a way, because one of the biggest problems in this space is that software wallets have no revenue path. So aside from mixing, there really is nothing else for them to make money on. Maybe selling shitcoins inside the wallet, but that’s not the best way to go about it. So we want to find a way to share some of the revenue of these cheaper cards that have better margin with some of the app developers. It’s unclear to me yet how we’re going to do that, but the first stage is testing out with artists. So we’re working out a model in which you go buy limited versions of Satcard on our website. The first one’s going to be @cryptograffiti—there is a sample of his art there—where you’re going to pay for a premium rate because it’s going to be smaller quantity run so it costs more to make. And a specific amount goes directly to them. So we’re trying to figure out how we’re going to make the store work for that and all that stuff. If it’s going to be straight to his wallet with a double output transaction—whatever. We want to make it easy for people to support artists. And if the model works for artists, we can make it work for wallet devs as well. So we really want to figure out a way of making this space be self-maintaining with revenue, so it’s not just donationware for a lot of these projects. So that’s stuff that we are exploring.

Stephan Livera:

Gotcha. And so the other question people might be thinking is: let’s say they’re using an Opendime—again, sometimes it’s different markets, right? So the Opendime user might not necessarily be the same as the Satscard user, but the Opendime user right now is used to that example where they press a pin through and they break it and they can see, Oh, it’s been broken and opened, so now I know not to trust. That was the Opendime thinking. With the Satscard, how does that work? Is it just an NFC tap and then you see, Okay, this has been spent? Or what’s that looking like?

NVK:

So the fascinating thing is Opendime doesn’t need the physical break. We could have made it software-defined, which it is, because when you break that pin is not really doing anything, it’s just essentially like a button just letting the software know to enable the sharing of the seed. And Satcard operates in the nine-tenths of the law is possession mentality. So if you have the device physically, it’s yours. It doesn’t matter. So it’s just software-defined. So once you give the PIN that’s on the back to the device, the device unseals itself and shows the private key. It’s a WIF format, as it was before. So yeah, it’s very similar to that sort of mode. We figured, like, What’s the point of making some theater thing happen when whoever has it, has it, anyways?

Stephan Livera:

Right. So just thinking out what a typical use might be. So in a similar way to the Opendime, the idea is it might be a round number of coins, let’s say 10 million sats, 1 million sats, or 100,000 satss. And the idea is it may pass through multiple owners. That’s the idea in that mind, that you might not necessarily do an on-chain transaction for every transfer of ownership of the Satscard. That’s the idea with the Satscard, which is contrasted with the Tapsigner. So maybe if you could talk a little bit about the differences there between the cards, and let’s talk a little bit about the Tapsigner.

NVK:

Sure. So this was informed to us by the market with Opendime. A lot of people were trying to use Opendime as one of the co-signers in a multisig, but it doesn’t have the brains to do any of that stuff. So they just reverse-engineered to get the public key out to use that for Rare Pepe, for multisig, for all kinds of stuff. We wanted to make that actually possible. So on the Satscard, the model is as explained: you give it physically, people take it and it’s like, Is it to buy a car? Is it to pass along digital money but physically? Exactly like Opendime was, just more slots. Now, we were like, Why don’t we develop a blind signer? Why don’t we develop something that people can use for co-signing multisig, for experimenting with lower amounts of money, for co-signing, with things like Muun wallet because that’s a 2-of-2, or for opening and closing Lightning channels that are smaller amounts on phones—that kind of stuff. Your threshold of security is not ColdCard-level, but you still don’t want the keys hot. Or maybe you just want an easy, quick, co-signing device in your mix of devices. So we’ve leveraged what we learned with NFC development and the stuff for Satscard to create Tapsigner, and Tapsigner is exactly what that is. It’s a tap-signer. You tap—it signs. It doesn’t know it’s signing, it knows it’s Bitcoin, it uses method digest so it’s not PSBT, although you could use PSBT via HWI as well, which is really cool. And so essentially it’s extremely dumb, extremely secure, and you also provide your own entropy—the security of it is quite good. And the trust-minimization is actually quite nice, too. So we see this being used for, say, Unchained or Casa. They hit us up, we make one branded with that brand, and they have it as their package of multisig now because it’s a lot cheaper as well. It’s not going to be as cheap as Satscard, but it’s a lot cheaper. So you now have an extra device that is extremely secure, like physically speaking. It’s an EAL6 chip. So you can now co-sign with your app, or have that as a backup sitting somewhere like a safe deposit box or something. It’s a very good addition to that bundle. Or for example, you keep it in your wallet, so if somebody steals your phone and you don’t have your PIN or whatever is happening, or you don’t want to trust the phone wallet, you can have a quick tapping to either sign or co-sign transactions on your phone—super useful. And then there’s key shuffles. There’s all kinds of cool stuff you can do with this thing. Because again, as a blind signer, you can use it for messaging. So if the PGP messaging is based on Bitcoin cryptography, you can just sign messages. You can use it to open your gun safe if it uses NFC and you can do this crypto. By crypto I mean cryptography, the real—

Stephan Livera:

Crypto.

NVK:

Yeah. So it’s a lot of new sort of uses, which is awesome.

Stephan Livera:

Right. And so as you said, it’s a lower price point. And so there is more trust being placed into the software wallet, because in the traditional model, the idea is you don’t trust the software wallet. You look at the hardware wallet to show you on the screen what is the hardware wallet saying, spend X, Y, Z, this number of sats to this address. So it is like a lesser security model, but I guess the idea is just saying, it might be part of your overall setup. But same kind of idea. Like we were saying, you’re still relying then on support being built out for this into the software wallets and services so that they can use it alongside the other things.

NVK:

In good Coinkite tradition, this is not a centralized service or product. You don’t need us to exist to get your money out. So there is a companion like open source code that can help you take the money out in case our quick, easy website is not available, or the app wallets don’t wanna support it anymore. Whatever happens, people’s monies are safe and recoverable without the vendor. That this is an integral part of that design. I wouldn’t want to make a product otherwise. If we have to close shop because whatever reason. People are fine—we don’t have to exist for people to redeem their money.

Stephan Livera:

The other question people might be thinking is: how do they know the private key isn’t leaving the card when it taps?

NVK:

Yeah. So the protocol is very obvious. The device is just signing. It’s never showing the private key. With Tapsigner, the cool thing is you can actually back up the private key, but it only leaves the card encrypted. So it’s encrypted with a specific key that’s on the back of the card if you want to make a backup and because it’s low amounts, maybe you save it in your iCloud, or whatever. It’s not ideal. Ideally you save it in a safer place, but being realistic, with a cheap signing device, the customer base will be the more noob base—they’ll probably save it in their iCloud or something. But what’s nice is that that’s really encrypted. It’s a proper level of encryption. And the keys, the passport for the encryption is on the card itself physically, so you’re not exposing yourself to that.

Stephan Livera:

Yeah. So just walking that through then the backup is essentially: you need the data from the card, which is encrypted, and then you also need the decryption key, which is on the card itself. You need those two pieces together to actually take that back up and use it in something else and recover it if, say, the card’s broken or whatever.

NVK:

That right. And this is BIP32-based, so not BIP39. There is no seed word—it’s too complex for this kind of chip. So it’s just BIP32, which would work even on the original Satoshi client. So it’s fully recoverable, backwards compatible. It really is that kind of mindset. We don’t want to leave people stuck with things. As you know, walletrecovery.org, will show you where bad designs will take you. So we really wanted to make sure this stuff is recoverable with very simple software.

Stephan Livera:

Yeah. And so presumably, like before we were saying, your aim is that mobile wallets and maybe some of the desktop wallets would support NFC, and maybe the NFC would have to happen if—I don’t know, do laptops normally have NFC? Or do you need to buy a dongle to do that? Or to use it with a computer?

NVK:

A lot of the touch laptops I think do have NFC. So like the Surfaces—some of those do. But realistically speaking, this is for a phone experience. That’s the goal of it. We’ll indicate to people some card readers to buy for the desktop, if they want to mess around with that, or for a ColdCard as well. But realistically speaking, NFC is for the phone or a tablet. And when you’re going to do stuff on the computer, it’s probably for more money, and you would be using a different mix of solutions. Because some of the collaborative multisig companies do have apps—there is more of them coming. There are more of these solutions for multisig coming out, and a lot of them are going to have an app component. We think that this is a very good fit for that. And then eventually, we’re going to end up probably seeing nice co-sign solutions for developing country people. You’re going to be able to afford this card to have your co-signing with your BlueWallet if you are in El Salvador where buying a ColdCard may be a little bit too expensive. And when you look at the two, it makes sense. The amount of money you’re defending should be relative to your security solution too. Like, why are you going to buy a ColdCard if you’re holding just two, three times that amount of money?

Stephan Livera:

Yeah. And I think it’s an interesting point as well, because for some people—and we’re starting to see this now—where some people literally don’t have a laptop or a desktop PC, they just do everything off their phone. And so for some people—or maybe they have a laptop but it’s only a work one, or it’s a really old one. And they can’t be asked or figure it out trying to get Electrum, or Specter, or Sparrow, et. cetera, working on that. And so for those people who still want to have some coin, even if it’s a smaller amount, then maybe that’s where having a phone—pretty much everyone has a phone nowadays. That is an interesting point.

NVK:

Right, because the people who want the best UX are the people with the least amount of money. It’s a very funny correlation there. Snd we know this. We have enough customer base, enough support. We know this is a fact, as opposed to what the people on Twitter want to believe. So the people that want the best UX have the least amount of money, so they’ve been best served by phone wallets. So we want to improve that with a cheap hardware solution. And then the people who have the most amount of money, they don’t want the phone experience. They don’t want QR—they don’t want any of this stuff. What they want is a Micro SD cold storage, bunker-level stuff. So these are the two tracks. They’re not going to risk real money with, like, pictures. And it’s a terrible idea. And the same way with the other side is like, they’re not going to buy a pretty hard wallet that can take pictures for a lot of money. They’re just defending a little money with their easy UX. So again, it’s just getting informed by how people are actually using the product. This really reminds me of the beginning of the Internet where you had companies trying to make devices that people are not going to use. A solution trying to find a problem.

Stephan Livera:

Yeah. That’s a really good and counterintuitive insight. And now that you mentioned it, it actually makes so much sense to me. The people who want the best UX may have the least money to secure. So when it comes to the prices then, are you able to give us a rough idea just for listeners? We’re recording this January, 2022. Can you give us a rough idea? What’s the price points for Satscard, Tapsigner, Mk4, just so people have a rough idea?

NVK:

So Mk4 the price has already been released. It’s $149. We’re taking reservations on early-bird pricing for $109. We try to make it as cheap as possible for customers because realistically speaking, I’d say probably half the sales are going to be for people who already own our devices anyways. And we want the early people who are going to buy the device anyways, who already have our devices, to get a deal. It’s like every 2 years we have new hardware. So we take it as cheap as we can sell it to you. And then we’re going to go back to normal pricing, which is $149, or around that. For Satscard, it’s going to be cheaper than an Opendime right now. A single unit is probably around $12, $14 kind of thing. So it’s going to definitely be cheaper than that. We’re working tirelessly to try to lower that. There is a lot of R&D involved on this product, so we have to make that back. And then Tapsigner will probably be around double or triple what Satscard is going to cost. It’s just more maintainability, more stuff going on. We hope to have some very good volume discounts on this stuff. And we hope to have a lot of custom art on it. We want artists to monetize hardware instead of monetizing JPEGs. No really, it’s like, Did you just buy a picture of a rock for $3 million? No, you bought a piece of art that’s in your hand and you can frame it, and the artists that we have talked to, they’re pretty excited about being able to do that. So yeah, I’m sorry I didn’t give you specific pricing.

Stephan Livera:

No, that’s fine. It’s just to give people a rough idea, and then that might inform their decisions as well when they’re out there thinking about who to advise on what they’re getting, because a lot of the listeners of this show tend to be the ones who are out there teaching other people. So I think that’s a useful thing for them to just have a rough idea there. A good point to wrap up with is, I think it’s interesting the direction things are going with ColdCard, and it’s almost like you and the company are almost zigging when a lot of other people are zagging, but in a way that actually makes a lot of sense now when you think about it, when it’s actually explained, and as you’ve been explaining. So I think that’s a really interesting direction. And I think it makes a lot of sense, as we were saying, that there are a lot of users who don’t have a laptop or a PC that they can use. And so for those people, they need to use it with a phone. And then what’s the device that works with a phone, but is also cost effective? And so I think this NFC direction is actually a really interesting one. So yeah, I’m curious to see where this goes, and I’m obviously excited. I’m definitely going to order my own Satscards and Tapsigner and Mk4s myself to play around with. But any final comments for the listeners?

NVK:

Yeah. So I think on the Tapsigner side, we hope that that’s probably the first hardware wallet people end up having—for Bitcoin only. It is Bitcoin-only, like everything we do. I think that’s part of why we are zigging instead of zagging, is that Bitcoin-only use 10 years from now is how we define the products internally. We’re also doing a lot of stuff right now with I call it defensive domain buying that I just wanted to mention, because we are looking for writers, we’re looking for people to contribute good Bitcoin information. And there are some interesting domain projects coming soon. And those are like semi non-profit kind of thing. The way we do it is we’re going to put some links to our store and things, but that’s it. And we want to produce extremely high-signal content that maybe gets resyndicated—or not, I don’t know. But we really want to have a holistic approach to Bitcoin bag security, that is through content that tells the right story about Bitcoin, that teaches people Bitcoin. It’s not just, Oh, Bitcoin is easy. No, it’s: this is what this BIP does, but in a way people understand, or is showing the Bitcoin holidays where it explains what happened that day with the true story of it, or is through security where we have a place for you to really hold your money without getting robbed, or is it for you to gift Bitcoin, or what else can we do to have Bitcoiners succeed? That’s our goal, and I think that’s the direction the company’s been going in, and it’s been a lot of fun.

Stephan Livera:

Fantastic, NVK. Well, it’s been a pleasure, and I’m really excited to see where it all goes. So thank you again for joining me.

NVK:

Hey man, thanks for having me. It’s nice seeing you.

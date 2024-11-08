---
title: Bitcoin multi sig security under $50
transcript_by: Stephan Livera
date: 2021-08-24
media: https://www.youtube.com/watch?v=TAEQ2D3Npjc
---
podcast: https://stephanlivera.com/episode/302/

Stephan Livera:

Seedsigner welcome to the show.

Seedsigner:

So glad to be here. Thank you for having me.

Stephan Livera:

So just for listeners, Seedsigner is operating under a pseudonym, so I’m just going to be calling him seed or SeedSigner. So seed, can you tell me a little bit about yourself and how this project came about? What was the inspiration?

Seedsigner:

So it’s actually a full circle kind of journey to be talking with you today because my journey with SeedSigner started probably mid to late last year with an episode that you did with Michael Flaxman on his 10x, Bitcoin security guide. And that kind of launched my journey down the rabbit hole.

Stephan Livera:

Fantastic. So were you coming from a developer background or like more like a hardware guy or what was the like what were the main skills required in this project?

Seedsigner:

So I have a unique background that I’ve talked a little bit about before. Not sure if you’re familiar with it, but I’m actually a retired police officer. And I spent the majority of my career in law enforcement working as a digital forensics examiner. I was you know, to give you a little bit of my backstory, I was a local cop the kind of guy who wears a uniform, drives a police car answers calls for a fight in progress, that kind of thing. And the chief of the police agency I was working for knew I had a background in computers. I had studied computers a little bit in college, and I’ve always kind of been leaning kind of in direction of being involved in computers. And there was a newer digital forensic working group that was starting up in our area.

Seedsigner:

And he asked me if I had any interest in joining that and I of course jumped at it. So I drank from the fire hose the forensic firehose for the first few years, just attending training and getting caught up with my everyday work for 12 plus years of my career was in a digital forensic lab taking apart phones and computers and hard drives and attempting to attempting to get data off of devices to see if the data would support prosecutions. And so that gives me kind of a unique technical background from a hardware perspective, but as a digital forensic practitioner, you kind of have to be a generalist in that a little bit about everything. You know, we know a little bit about how data is stored in binary fashion, a little bit about operating systems, user artifacts, how data’s stored in the cloud, how different hardware devices work and what kind of vulnerabilities they have.

Seedsigner:

But more specifically with my forensic background, one of the things that informed some of my journey with SeedSigner was this concept of air gapping. And a lot of people may not be familiar with mobile phone forensics, but best practice in mobile phone forensics is that you’re isolating a phone that you’re doing an analysis on from the internet in any kind of way. So that’s the parent kind of cellular network, but that’s also wifi and Bluetooth. And a lot of digital forensic practitioners have these large boxes like glove boxes, or even like entire rooms that are what they call Faraday shielded. And all that means is that there’s special shielding and the door and the walls that block radio signals. So once you go into that room, you close the door. If you have say your personal phone up in there, you’re going to notice the bars very rapidly, go to zero. Your wifi is going to go away. So this concept of air gapping devices and being able to isolate channels of communication that devices usually use was something that was in my background. And that also kind of applies to examining hard drives and stuff using write blockers. I don’t want to get too, too deep into that, but you asked kind of my background. So I, I’m kind of a little bit of a Jack of all trades with a bunch of different kinds of hardware and software kind of skills.

Stephan Livera:

Yeah. Well, it’s great to hear that my show was in some way able to help influence the creation of other projects that are pushing it forward. And I’m sure Michael Flaxman well, I think he’s actually, he’s been commenting a little bit on the project himself as well. And so essentially just for listeners who aren’t familiar, it’s essentially a new type of DIY hardware wallet device. Right. So can you tell us a little bit about that and what are the key features at a headline level for people?

Seedsigner:

Sure. And if it would be okay if I can continue the backstory just a little bit with the podcast, so people get a sense of how that ties in. So I’m listening to your podcast with Michael Flaxman. I’d never heard of specter, specter desktop, specter wallet, and was really intrigued by some of the security concepts that he brought up in his paper and in his conversation with you. So I am looking to transition at that point to a new Bitcoin security model I’ve been wanting to get to multisig, but it didn’t feel at least with my knowledge at the time on what was out there that multisig had kind of gotten to that point where it was more user-friendly and easier to interact with. But after I heard about Specter, I was eager, eager to give it a try. So I download Specter and I start looking at the options within the software, and I’m looking in their GitHub repo.

Seedsigner:

And I noticed that they have this additional kind of side project called a specter DIY or a do it yourself signing device, which is kind of akin to a hardware wallet. And I’ve like I referenced a little bit of a background in hardware, so it didn’t seem like a huge lift. So I ordered the components and assembled the DIY hardware signer that they have in a separate repo. And what I tell people is, so I set up a multisig wallet and I use kind of the signing mechanism where you use animated QR codes, are how you move the partially signed Bitcoin transaction, the multisig coordinator in this case, specter into the signed device and you review, the transaction details, the signed device is an isolated offline device where your private keys stored. And if you approve the transaction, you can communicate that partially signed transaction back to the multisig coordinator again, via QR codes.

Seedsigner:

The first time I did that with a specter DIY, it was like a magical light bulb moment. It was like the first time I sent a Bitcoin transaction. The first time I used lightning, it was just holding the QR codes up to my web cameras my web cam and seeing once it had ingested the partially or the, now it was a fully signed transaction and it pops up on the screen that one of your co-signers has approved it and it’s ready to send, like, that was magical for me. And so I started thinking around with Specter DIY a little bit more, and Michael Flaxman had made a tweet that he really loved the DIY, but he was hoping that someone would make an enclosure for it, a case. I have a little bit of a background in like a three-dimensional design and 3D printing.

Seedsigner:

So I made a case for it and I DMed him and we started interacting a little bit. I also started interacting with Stepan and Moritz from Specter, about the case design and stuff. And Michael communicated to me that he had this idea for using a very specific version of the raspberry PI. It’s called a raspberry PI zero. And there’s an even more specific version of the zero called a version 1.3. And the secret sauce in that specific version of the pie is that it’s a smaller form factor than what a lot of people use in nodes. And it does not have wifi or Bluetooth built into it. So it doesn’t have that hardware functionality. So it’s a naturally kind of isolated air gapped kind of device. And Michael had talked about using that particular device to calculate the final checksum word for seed phrase.

Seedsigner:

If a lot of your listeners are aware, you can generate a Bitcoin seed by just pulling 11 or 23 seed words out of a hat basically. But that last word operates as kind of a checksum against the first 11 or the first 23 words to verify that everything comes together. So his idea was to use this very specific version of a raspberry PI zero that was isolated from the internet to be able to securely calculate that checksum word. So you’d be able to generate a Bitcoin private key in a pretty secure way without having worried about it, having come into contact with the internet. He also pointed me towards like a little display and control module that looks really kind of like a very small video game that has a joystick, a tiny screen that’s 240 by 240 pixels and a few buttons.

Seedsigner:

And he said, what if we could combine these and you’d kind of independently be able to set this up under the words, and it would calculate the final checksum word. That seemed kind of like an interesting project and with Python being kind of native to the raspberry PI operating system. I started brushing up on my programming. I’d taken a little bit of java in the past, but I spent a lot of time on udemy learning the basics of Python and a lot of time on Google and stack overflow, kind of bang my head against the wall with different errors, but I’m kind of in my living room, just iterating step-by-step with these components. Can I run the manufacturers test code? Can I make my own image appear on the screen? Can I make letters appear on the screen?

Seedsigner:

Can I use the letters to collect words? And finally, I got to the point where I’d achieved the function of inputting, say 23 words, and then outputting that 24th word. And I, threw the proof of concept out on Twitter and people seem to react favorably to it. And I still kept thinking about my experience with specter DIY. And I started wondering if I added an inexpensive camera to the raspberry Pi zero with the camera and the screen and the controls could I possibly replicate replicate that basic air gapped, QR exchange signing capability that had been so magical to me with the Specter DIY? And in the process, like I kind of joked that my main contribution to SeedSigner has been being a cheapskate, but I wanted to see how far I could drive down the price for that like basic air gapped, QR exchange, signing experience.

Seedsigner:

So I started iterating with the code some more and kind of updating people on Twitter and started to get more and more interest. And eventually it got to the point where I released like a very basic clumsy proof of concept, but it worked like you could fire up specter desktop. You could use SeedSigner to set up a very simple, like one of two or two of three multisig wallet where it was all of the signers. And then you could ingest, using the camera in just a partially signed transaction, approve it on the device, and then communicate it back to specter to where the transaction was ready to broadcast. So that was, that’s really kind of the journey from you talking to Michael Flaxman to me, kind of just banging my head against the wall with this hardware, trying to get the basic functionality there.

Stephan Livera:

Yeah. That’s really a cool story to hear. And so it’s funny because in some ways this whole idea of low-cost hardware wallets, even though they may not have the secure element that some of the more premium hybrid worlds will have as an example, right? Like the ledgers of the world or the cold cards of the world. But despite as Michael Flaxman explained, you could theoretically make an argument as to how having multisignature, even with cheaper devices distributed into different locations, you might actually be more secure than using a single signature premium hardware wallet device.

Seedsigner:

Right. I think there are trade offs as with any kind of security decisions you make when you’re deciding how to, how to store your Bitcoin. But one of the things I like about multisig is that it’s a little bit more forgiving in that with a single hardware wallet. Like if something happens with the wallet and for some reason you don’t have your seed or it wasn’t backed up properly. it’s hard to come back from that, but with multisig you know, the larger, the number of signers you have typically the more, a little bit more room for error you have, if you should happen to have a signer compromised, or if for whatever reason you lose access to the private key. So think there are some advantages to that even though I have to acknowledge belt and suspenders multisig is a mix of different code bases and hardware manufacturers, and maybe even signing protocols to kind of have that resilience so that if one particular platform fails because of a vulnerability, the rest of your co-signers are unaffected.

Stephan Livera:

So speaking of the costs, then can you give us an overview? What is the rough cost in US Dollars in terms of parts to create a SeedSigner?

Seedsigner:

Sure. it’s probably at this point, just makes sense to quickly step through the different parts. So we have the raspberry PI zero, I mentioned before, specifically the version 1.3 prices on that’ll vary if you’re an American and you happen to live next to a micro center, which is a large kind of like electronic box store. You can actually walk in with cash and walk out with one of those for five bucks in also in America through the adafruit website, you can order if you’re willing to pay with a credit card and give up an address, I should say, you can find one for $10 with shipping included, if you’re okay with it going through just the regular post and not any sort of accelerated shipment, if you go on Amazon, you’re probably going to pay a bit more of the prices on Amazon are more, so let’s say roughly $10 for a Pi zero, maybe 15.

Seedsigner:

In addition to the pie zero, we have the display and controls that I mentioned, which is a very specific version of a wave share. They call it a display hat and that I would price between $13. If you buy it directly from waveshare up to $17 or $18, if you buy it on Amazon on Amazon, it is prime eligible. So that 17 or $18 is like a real price shipped to you. And then third main component you have is like a very basic raspberry PI camera module. And those are kind of commodity hardware because there’s a bunch of them out there with different brand names that are all kind of the same basic hardware profile that are kind of rebranded that camera. You also need to make sure you get a cable with it. That’s compatible with the zero. There’s two types of Raspberry PI camera cables.

Seedsigner:

One of which is compatible with like the raspberry PI 2, 3, 4, the larger ones that people use in their nodes. But the zero is a different camera cable. That just one of the ends is a little bit smaller to be compatible with a smaller form factor of the zero. So the camera, I can get them for as little as $4 on Amazon here. That may not be the case, obviously for people anywhere in the world. So let’s say 10 bucks for the camera. So we’ve got, say $15 for the PI $15 for the wave share, display and controls, and then maybe $10 for the camera that gets us to $45. You’ve got some shipping in there, maybe. Yes, maybe no, but I like to say about 50 bucks or less than 50 bucks, that’s not going to be true for everywhere in the world. Some people will pay a little less, some people pay a little bit more, but that’s kind of the general consensus amount that we’re on right now.

Stephan Livera:

Yeah, very impressive in terms of the low cost and the ability to have a QR air gapped wallet. And so this might also have applications for people out there who want to just get started with Bitcoin, and maybe they can’t justify paying the higher prices for the more premium hardware wallets. And this is just a way for them to get started. And they could even start with, with this as a single signature set up couldn’t they, and then later graduate up into a multisignature set up.

Seedsigner:

Right. And that’s actually how one of our lead developers, Nick found the project. I think he was just looking on GitHub at Bitcoin wallet related projects. And he had been at a point where he was curious to start just playing around with multisig more and setting up kind of a test wallet and was a little bit put off that even to just get a simple two of three multisig, like you have to either have them where you need to say purchase like either a mixture of hardware devices, like a Trezor and a Coldcard or a ledger or something like that. But you can spend easily two or $300 just kind of getting the basic three wallets. You need to set up a multisig, but if you if you just want to get started playing with it, and especially I encourage people we’re fully compatible with Testnet.

Seedsigner:

So jump on Testnet. But yeah, with that one device, it can act as as many signers and a multisig quorum as you’d like it to. So you can hit the ground running with multisig and start setting up different wallets and getting more familiar with the signing process. And also, like you said, we’re single-sig compatible. So this air gap QR exchange is also a model that a lot of people are less familiar with because it’s a newer kind of way of moving the partially signed transaction back and forth. And our device is also a way for people just to get some exposure to that model. And I think it’s really kind of intuitive to a lot of people that once they have built it or they get their hands on one and they kind of experience it for the first time, I really think it’s intuitive.

Seedsigner:

And it gives you that kind of like little bit of magic feeling that was talking about earlier. And it also allays some of the hardware wallet profile sorry, the hardware wallet devices that have a secure element and where you plug it into your computer via USB. I, my background in digital forensics was such that whenever say I had a piece of evidence that was plugged into a machine that I was working on, say I was doing, an evidence acquisition. We would always use this thing called a write blocker. And a write blocker is really just kind of like a one-way valve for data. So if I take a thumb drive and I plug it into a write blocker, that ensures that I can only read from that device. And then I can’t modify that piece of evidence by inadvertently or even intentionally pushing any sort of data to it.

Seedsigner:

So from my experience in the forensic world, when I see like a hardware wallet plugged into my laptop, just plugged straight in, it just makes me a little uncomfortable because I know that there’s a lot of possibilities with that protocol. If I was updating the firmware or as it’s moving signatures back and forth you just don’t know what’s going on with that hardware connection. Whereas this QR exchange, it’s a very sort of constrained protocol that your laptop and the signing device use to communicate. And I just get a better feeling because the only way that seedsigner can ingest data is with that camera that is incorporated in the device via QR codes. And the only way it can talk to your laptop is through QR codes. Now, human beings, aren’t fluid and QR codes. We can’t decode that just by looking at them. But it just, it’s a much more constrained communication protocol if that makes sense. Yeah.

Stephan Livera:

And I think this is what, something, when I’m often talking to a newcoiner maybe someone who’s never used a hardware wallet, that’s often a way I’ll explain it is they’ll say, imagine you had a house with $10 and 20 windows, and then you had a house with only one door in and one door out. Well, which one’s easier to protect. Right. So it’s kind of like that similar kind of idea. and so speaking a little bit about the way, so just for listeners who might never have used a QR wallets before, so listeners, you might’ve been using a phone wallet before, or maybe you’ve used to say a Trezor or a Ledger, or those kinds of devices where you plug them in. Well, in this case, the computer will show you a QR code and you scan that with this hardware wallet, and then it will show you the details saying, oh, Hey, do you want to send 0.1 Bitcoin to this address?

Stephan Livera:

Yes or no. And then you hit yes. And then it approves, and then it will show you the QR code. And that QR code is now the the signed version of that transaction. And now it may have, it may only be one of three or two or three or however many signatures. And then you would then have to show that back to your computer and basically show your computer, this QR code. And that computer will then ingest that using its webcam. And then that’s where specter desktop or Sparrow can help you coordinate that across multiple devices. And so…

Seedsigner:

And if I could kind of jump in and point out, it takes what people know is the traditional hardware model and kind of breaks it into different components. Cause if you I’ll just use ledger in as an example. So if you use ledger to set up a Bitcoin wallet, you are of course generating the private key on ledger, and then you connect ledger to your computer and you interact with their software interface where you’re using kind of their portal to the blockchain and they help you assemble the transaction and help you broadcast it and such, and this kind of different model with the air gap signers breaks it into what I’d call like three different components. There’s first the wallet coordinator, which is your specter or Sparrow or even blue wallet can function in that way.

Seedsigner:

So you have your wallet coordinator, or I’ll also sometimes refer to it as a multisig coordinator, because that is what basically puts together the multisig components and helps them make sense to the protocol. So you have your coordinator and then you have a signing device, which is like a specter DIY, or a SeedSigner. And then you have your private key storage. And with the signing device, what happens with it is our particular signing devices stateless. And what that means is that when you power it on, you have to enter your seed phrase into it, which represents your private key. So now your private key is live on that device, but with our platform, it’s not written to the memory card. It just exists as a variable in memory in the Python code, such that when you remove power from the device, like I said, it’s not saved to the memory card.

Seedsigner:

So it just goes away with memory. But at any rate with the signing device, after you’ve entered your seed, which represents your private key, and then you ingest, like you referenced that partially signed transaction, I think it’s important to emphasize to people that your private key never leaves that device. It’s not communicated within the QR code somehow back to the multisig coordinator using cryptographic signatures, the signing device just proves that it has knowledge of the key through those signatures. And those are what it communicates back to the multisig coordinator. It’s a little bit of a nuance, but it’s critical to the security model. So again, you have multisig coordinator, you have that signing device, and then you have your seed storage or your private key storage, which a lot of people use in addition to just writing their seed on a piece of paper. They’ll also etch it in a metal or use washers to kind of stamp the letters enter kind of one of those similar, different mechanisms.

Stephan Livera:

Gotcha. Yeah. So then putting that into an example, as an example, we might have a two of three multisignature set up, they could be using, say a cold card is one of the keys. They could be using a SeedSigner as another key and maybe specter DIY as another key. And so you might have three different locations. And with each location, you might have say the metal seed backup for that location, even. I mean, obviously there are different ways to go about this. You could even have six locations and have the seed backups in different locations, but I guess, but actually, sorry, in the seed signer case you would want to have the metal backup with the SeedSigner itself, because you would need to re type in the seed words when you do the signatures. Right. But that’s not a huge deal if we’re talking about long-term cold storage, that you very, very rarely access.

Stephan Livera:

And so you might have I mean, just to keep the example simple, it might be three locations. So three hardware, wallet devices, and three metal seed backups, right. You might have the Cyphergrid from my sponsor, Cyphersafe.io or one of the other metal products. And then you might need to bring some power with you when you go out to the location, because you need say a mobile phone, power bank, and then you can plug that into your seed signer to then give it enough juice to do the operation. And you might have say a laptop with Specter desktop on it. And that’s where you’re kind of going back and forward. So you bring that laptop around to do the multisig transaction in the different locations. So I guess that’s an example of it.

Seedsigner:

Yeah. That’s a great example. And I’d also point out that first off you mentioned that for holders it’s less cumbersome and I definitely want to reinforce that the impetus for the device SeedSigner is to reduce the cost and complication of multisig. And we’re really kind of zoned in on areas where people don’t have two or $300 laying around to buy various hardware wallets. So our device, as it currently exists is optimized for savings. So it’s a little cumbersome in that you have to enter your seed details every time you power it on, but for somebody who’s using Bitcoin, primarily as a savings mechanism and making more deposits and relatively few spends over time, it’s really not a huge encumbrance for the use of it, but I’d also point out this is a recent feature that’s been added by.

Seedsigner:

I want to give a shout out to Keith Mukai who kind of pioneered this to reduce the friction and being able to ingest your seed back in the SeedSigner. He came up with this very clever interface within SeedSigner to where the first time you have your 24 words or your 12 words, and you input them in a SeedSigner, it validates that the checksum words, correct. And that’s a valid seed and it gives you the opportunity to using a template using basically a piece of paper and a sharpie. You can print out a QR code template and use a Sharpie, and it will display a grid view of a zoomed in QR code on the screen. And you can grid square by grid square transcribe the QR code onto a sheet of paper that represents your seeds, such that any time in the future, when you want to power on your SeedSigner and ingest your seed, instead of typing in those seed words, you can just actually scan this QR code and instantaneously your seed is ingested in the SeedSigner and validate that it’s a good seed and you can move right onto signing.

Seedsigner:

There’s still a little bit of friction that it’s going to take you maybe five or 10 minutes with a marker to sketch out this QR code, but QR codes are super forgiving and I’ve done it. And then for the convenience of being able to instantaneously import your seed like five or 10 minutes to color in some squares is a pretty good trade off. But I’ll also point out that if people are worried about that seed QR we also implemented BIP 39 passphrases, such that in addition to your 24 word seed or your 12 word seed, you can also do the, what they sometimes refer to as word 25 or just a passphrase. That’s an additional layer of security for your seed. So when you’re in an example where I’m traveling to a location, maybe where my seed is stored one possible workflow is I have my SeedSigner with a little power bank.

Seedsigner:

So that’s powered. I go to the trusted friends house or the safe deposit box I get there. I either manually input my 12 or 24 words, or maybe I just scan in the QR code that I’ve manually transcribed there. And then maybe I go to multiple other locations and I can input seeds in the seedsigner as well, knowing that the seeds are protected by word 25. And it’s not until I get back to my home where I have specter set up and I have the wallet set up. Those seeds are basically useless until the word 25 passwords are entered into the device as well.

Stephan Livera:

Yeah. So each device can have its own little layer of additional protection. As an example, you might have a passphrase on each of the different devices. It could be the same passphrase, or it could be a different one for each device. Again, depends how complex you want to make it and how secure you want to make it. And so I guess also just thinking out loud another examples set up, you could do, let’s say you wanted to do a two or three multisignature, but also here, we’re going to exploit this idea that seed signer is a stateless device. So we’re going to do a two or three with one device. And so you might, as an example, have three different locations and have the metal seed backup for each of those in the three different locations. And you just have in your backpack, you’ve got your laptop with specter desktop on it. And you walk around with one seed signer device and to each location, you go around ingest the 12 or 24 words, sign that part of the transaction and then move on to the second location and do the same with that. And so that way you’ve actually got like a two of three multisig, but using only one device, but obviously you would still have three seeds backed up across three locations. Right.

Seedsigner:

Right. And I can take it a step further and say like, let’s throw out El Salvador’s, as an example, as a stateless device, even a few households could share this device. And if they want an additional layer of protection, maybe they each just have their own micro SD card that contains, that contains a firmware that they’ve loaded themselves, that they feel like they can trust without worrying about some kind of they call it the housekeeper attack or the evil maid attack. Right. And so it’s something that is a stateless device that can actually be shared by multiple different parties to use their multisig. That’s kind of an additional feature. And we’re also working on some additional improvements such that users can feel like they have an additional layer of security where they can power on the seed signer, this isn’t a live feature yet, but it’s well into development, you’ll be able to power on seed signer.

Seedsigner:

Once the device is fully up and running, you can actually remove the micro SD card and it still functions. Normally this for one advantage of that is that it gives users kind of an additional layer of reassurance that their seed is not somehow being leaked onto the micro SD card inadvertently. And we’ve taken several steps to ensure that doesn’t happen. But if you’re physically removing the seed before you put your your words in like you, that’s an additional layer of assurance, the other thing it opens up for us is the ability for people who prefer to move partially signed transactions with a memory card, we should be able to implement a system where with a different micro SD card, you can pop it in. And maybe it has a partially signed transaction in it, seed signer, will recognize and ingest that, display the details and then add the necessary signatures. So you can eject it, pull it out and put it into your laptop. So we’ve got kind of some interesting improvements, but to get back to the original idea, like we’re really trying to optimize for places where people are saving in Bitcoin and they may not have the resources for much of hardware wallets, so they can even share this between households.

Stephan Livera:

Okay. So yeah, there’s this idea that it can be used in low cost scenarios, and that can help in different jurisdictions where obviously the wealth levels are different to the wealth levels that you and I enjoy in the Western world. Now that is an example where it can be dramatically made more accessible, right? If it’s only $50 for a hardware wallet device, and that device can now be shared across multiple people well then dramatically. Now there’s a lot more possibility there. I know, even in the example of Bitcoin beach with in El Zonte in El Salvador, as part of that wallet, they have a multisignature set up using Specter desktop. I think if I recall correctly and so different places around the world could incorporate Seedsigner as part of that, multisignature set up or as part of the way they implement that. So I guess the next question, I’m curious what kind of technical skill is required to create this thing, or could there be maybe a market for people who just want to buy it outright? Can you tell us a little bit about that?

Seedsigner:

And if I could also kind of touch back on what you were saying about helping out in El Salvador another kind of advantage of our model, and it’s just trade-offs in terms of our signed device versus hardware, wallets another kind of advantage is that for people who are very privacy focused, say I had contact with people living in the middle east, and they don’t feel like they want to signal that they’re saving in Bitcoin, or they don’t feel like they can trust the hardware, wallet, resellers, where they are like the hardware may have been tampered with, or maybe they just don’t want anybody to know that they’re using Bitcoin, or maybe they don’t want to provide their information to a Bitcoin company because they see that as potentially like a violation of their operational security. The nice thing about seed signer is you can buy the parts online and none of the parts are explicitly Bitcoin related.

Seedsigner:

So you can get all the components, put it together, and you haven’t necessarily signaled to any sort of wallet company or any sort of Bitcoin focus company that you’re intending to buy or build a wallet and store Bitcoin and interact with the Bitcoin network. So I just wanted to point that out while we were talking about kind of the hardware side of it, but to get back to your question about the technical skill that’s required the biggest hurdle with, if you’re going to build it from just bare components, is that it is hard to find that specific version of the raspberry PI zero the 1.3, it is hard to find it with GPIO Pins installed. And if people aren’t familiar with the GPI opens, those are that’s the set of 40 pins that you see that do come pre-installed on the larger versions of the raspberry PI.

Seedsigner:

So you’re going to have to go through like one of two directions to get the GPIO pins on a raspberry PI zero. The first of which is if you’re comfortable trying it, or somebody who can solder, you can buy the pins and attach them yourself that way with a soldering iron, but understandably that’s a little more advanced or there’s also this device called a GPIO hammer. And listeners can just do an internet search for that. And it’s on Amazon, it’s on a lot of the other kind of like hardware tinkering websites. And that includes like a jig, it gets a little more expensive option. I think it’s maybe 15 bucks, but it lets you with a jig and a hammer just kind of tap the pins into place. So that, like I said, that’s the biggest hurdle is getting those GPIO pins onto the pi zero beyond that it is just attaching a ribbon cable to the camera module and the pi zero. And then it’s pushing the wave, share LCD hat just onto the GPIO pin. So pins are the kind of major friction point, but beyond that, it’s really just kind of a snap together project.

Stephan Livera:

Excellent. And so that’s a possibility for people. And then there may also be, I mean, this could even be a business idea for people out there. If you’re in a country where maybe you want to help improve the access to Bitcoin, you could basically manufacture this and sell it to people who maybe they’re at one step lower in terms of the commitment or time commitment they’re willing to put in to figuring it out. You might be able to make money just by selling this as a product to people, right?

Seedsigner:

Yeah. And I I’d point out we have a couple of different versions of a 3D printed enclosure houses, all the components and those along with all the software, the 3D models are fully open source. The whole project project is under an MIT license. So if somebody in Guatemala or El Salvador wanted to spin up kind of like a cottage manufacturing operation and source the components yeah, that’s absolutely something that I would love to see.

Stephan Livera:

And that’s really interesting as well, because it brings up the difference between being a project versus being a product. Right. Because I guess you see yourself as starting a project here. And the idea is that you would like to, we would like to see more and more people. I mean, along with the broader Bitcoin project, we want to see the proliferation of this broader idea. And part of that means some of it, some of it has to be commercialized. And so that means other people can take the project and commercialize it and in doing so helps spread the word and it, it brings back benefits for everyone.

Seedsigner:

Right. And SeedSigner is, has been, I can’t emphasize enough how much of a collaborative project it’s been, even from the very beginning when I was just tinkering around with hardware, Stepan from…

Stephan Livera:

Stepan Snigirev?

Seedsigner:

Yeah. He was enormously helpful. So in and I should also mention, we use a library called [inaudible] that he wrote himself and that he maintains, and to my knowledge, they use that in Specter DIY as well, but it’s like a lower level Python library that handles a lot of the heavy lifting between the Bitcoin protocol and kind of higher level Python functions. And he was immensely helpful in terms of me being a novice coder, asking him all sorts of boneheaded questions about how to implement his library into what I was trying to do. Can’t emphasize how supportive he was as well as Moritz with specter.

Seedsigner:

He’s been an enormous friend of the project and kind of helping even get the word out about it on Twitter and kind of giving me advice on how to make strategic decisions with the project. I mentioned Nick and Keith before who were kind of the two primary developers that jumped in especially Nick very early when with my super basic coding skills the code was not optimized. It wasn’t, conventionalized in a way that Python coders would recognize I didn’t have a lot of knowledge of structure. And Nick is a coder by trade that’s his day job. And he came in pretty early on. This is a few months ago and rewrote the whole code base so that it conformed to Python structure. And it was in syntax that other Python developers would recognize and be able to work more easily with Keith has jumped in with a lot of creative, super creative UI improvements, like with an improved keyboard to make that process of entering the seed words a lot easier and less painful.

Seedsigner:

He also came up with the seed QR feature that I was talking about, but beyond those guys, there’s another guy named Richard who is in Europe, who has been a huge help with the 3D printing aspect of this and getting the cases out to people in Europe so that we can avoid so much VAT and avoid shipping costs and everything else like that. The website, we have SeedSigner.com that somebody reached out to me, a developer, whose name is Jay in the Philippines. And he has taken the lead with a website. He has another, a guy named Jonathan working with him that they have, they really built the website from scratch. I provided the content some of the direction, but they have been a huge help. Jan R who’s a European guy who’s leading the charge are what I was talking about before with a custom operating system image that kind of gets out all of the raspberry PI OS stuff.

Seedsigner:

It’s a custom Linux build that will allow us to streamline the boot process. Well, to remove the memory card after boot and do some of the things I was talking about, a guy named easy, who his day job is in he’s a user interface designer and he’s helping us in a future version. We’re going to overhaul the UI. Cause right now it’s a very basic, almost DOS like UI, where you just use the arrows to select things and he’s going to make it much more approachable, much more intuitive. And even like a guy in south America who his Twitter handle, I think of shadows Lewis does graphic design and he came up with our logo. So I wanna like commend all those people for jumping in, especially early in the project, when it wasn’t clear whether or not this thing was going to go anywhere and offering their assistance with so many different aspects of the project.

Seedsigner:

So that’s like with what you talked about, about being a project versus a product, I think there’s kind of elements of both kind of ideas and what we’re doing. I kind of take a lead since Nick and Keith has stepped in with the coding. I’ve taken a step back from the technical stuff. And I’m more in a position where I’m being the GitHub repo maintainer, and I manage our Twitter presence and I coordinated the website and that kind of stuff. And with a product it’s kind of interesting versus a project like we do sell components to help support some of the costs associated with the project itself, but we’re really not trying to sell anyone anything. If you wanna, if you want to buy the parts and build this thing, like you don’t need anything from us, you can just download the software, order the components and build it yourself.

Seedsigner:

But at the same time, there is kind of like a marketing aspect to it. And you have to convey the device and the project in such a way that it gets people excited. Like people see the functionality and they see the device. Maybe they I think Bitcoiners kind of have a little bit of an attachment to physical devices that are associated with Bitcoin because Bitcoin is of course a virtual good. So hardware, wallets, swag, t-shirts I think Bitcoiners into all that kind of stuff. Cause they’re physical representations of this thing they’re so passionate about, but with the project, it really it takes time and engagement with people to communicate the value proposition that I think we’re offering and to get them excited about having that same like little magical experience the first time that they scan a QR code in and then approve a transaction and scan it back into their laptop, you have to get people excited to at least just build it. And even beyond that, like want to help contribute to it, cause it’s a collaborative effort for sure.

Stephan Livera:

Yeah. That’s great to see. And to hear that there are people all over the world contributing to the project and then yeah, as you mentioned, speaking from a product perspective, there’s marketing and there’s all sorts of other aspects to involve because look, the general person out on the street who is just trying to start learning about Bitcoin and holding Bitcoin. It might be quite difficult to get them over the line on, Hey, use this project to store your Bitcoin. But if somebody were out there as a company selling it as a product, well then maybe that’s a bit easier for them to jive with. And you know, of course we can sit here saying no, everyone should just be being able to fully DIY I think the reality is a lot different, right? Because if you think what percentage of the population would use a project versus what percentage of the population would use a commercialized product that there’s a company there to you know, to yell at, if something goes wrong or to give them customer support and things like that.

Seedsigner:

Right. And it’s getting to the point where you can purchase a SeedSigner assembled, like you’ve alluded to it. It dramatically expands our audience in terms of right now, if somebody maybe sees me on Twitter, sees the device demo of the seed signer being used and thinks like, wow, that’s really something cool that I’d like to try, but maybe they don’t have the time or the interest in building it themselves when we get to the point that they can go from, Hey, that looks really cool, to, I can purchase one and get it several days later in the mail, that’s really going to dramatically expand our potential audience. And I’d also note I’ve kind of been moving in that direction over the last, even just the last several days, probably within the next, we’ll say two to four weeks, I’m gonna have the kind of component quantities on hand, I think to start offering it for sale probably worldwide.

Seedsigner:

There are also some people in Europe that are in touch with me about spinning operations up there because you know, it’s a lot of people, the VAT in Europe is kind of a pain for people to have to deal with. And then there’s the shipping times and the COVID world are a little bit longer than I think they have historically been. So I have a square store currently where we sell the enclosures and I also sell pre soldered raspberry PI zeros. That was kind of a way of removing some of the friction for people wanting build it. The cases are also available for sale on crypto cloaks. There’s a version of the case called an orange pill that they sell, which was the earlier version of the enclosure. And I’ve moved to a simple, more streamlined version of a 3D printed enclosure.

Seedsigner:

That’s more optimized for fast, cheap and easy deployment in places like El Salvador. And that’s what I’ll be using to offer the assembled devices for sale such that the one thing they won’t include is a memory card because I really want to encourage people to write their own firmware image. I think that’s important. And it also encourages them to be able to be familiar with how to update the device because we’re, we still are at a place where we have some really great features in the pipe. And I want people to be comfortable writing the software and updating the software so they can get access to the latest features. But beyond connecting a micro USB cable and popping a memory card in, it will be an assembled device. So people can kind of just hit the ground running and start playing around with multisig.

Stephan Livera:

Yeah, that’s great to see. And I’m also curious what your experience has been like with the QR codes, because in my experience playing around with various setups and QR code wallets, in some cases I’ve had issues getting the QR code to scan. And so from my understanding, this can be if, say the screen is not a high res one, or if the webcam is not good enough on a low quality laptop or device, sometimes there can be issues around scanning the QR, or sometimes it can be a lighting thing as well. So you need to make sure you’re in good lighting. And so that the QR code reads easily, what’s your experience been with QR codes?

Seedsigner:

There, there is a bit of nuance and I’d call it skill development with the QR exchange process. We are forever working with the different multisig coordinators in any way we can to kind of optimize that process because there are a lot of variables that go into it in terms of the QR density that’s displayed on your laptop and the density that’s displayed on seed signer, because the more dense that the QR is, the more information it can contain and the fewer frames. So you have to scan back and forth, but if it gets too dense, that can get a little more difficult to scan it back in so we’re forever, kind of trying to find the optimized default settings for people. And then also giving people the option to tweak the settings in terms of beyond frame rates and QR density with our screen.

Seedsigner:

It’s not something that a lot of people think to do, but it makes a dramatic difference in terms of ambient light. If you’re holding the seed signer screen up to your webcam, and for some reason it’s, there’s a glare, or it seems like it’s too dark. If you slightly clockwise or counter-clockwise rotate the screen. And I’ve had lots of other people like kind of rave that this solved a problem that they have been wrestling with somehow with the pixels lineup or whatever, how they’re exiting, maybe it has to do with how the light is exiting the screen. But if you just rotate it slightly, it resolves a lot of those glare and light issues. I’m not sure if that’s the case with some of the other air gap, QR devices out there, but that’s a big kind of, that’s a great technique to improve the process with ours.

Seedsigner:

So like with anything though it’s practicing, so get on Testnet set up a wallet and just start making transactions that’s well within the reach of a lot of people just to start getting more comfortable with it. I always encourage people to, before you start putting live funds on main net or, or if you do start on main net, start with small amounts and get comfortable with that QR exchange process, whether it’s using a SeedSigner or a DIY or Cobo vault or passport, or whatever people are working with always get comfortable and practice with your your hardware.

Stephan Livera:

Interesting tip there around rotating the device that maybe that there’ll be the new Bitcoin QR dance move inspired by the QR dance. But I’m also curious, as you mentioned, it is a stateless device. What about the concept of registering your multisig quorum? So I guess maybe just backing up just for listeners who aren’t familiar when you create a multisig, if you haven’t done it before, typically you might, if you’re using Specter or Sparrow, you might ingest in the public keys of each of the three wallets, and then it will then spit out back a multisig quorum, a QR or SD card thing to basically send it back into the wallet. So it knows who the other signers are and basically gives it some info on how to sign the transaction correctly. How does that work with SeedSigner?

Seedsigner:

So with seed signer or the necessary information to sign, the transaction has to be communicated because it’s a stainless device. It has to be included in the PSBT every time that’s communicated from the coordinator to seed signer. So there is a little bit of extra information that has to come through that provides the necessary descriptors for seed signer to be able to properly add the signatures. That’s something that, again, Stepan from specter was super helpful working with us when we — they were the first platform that we had, like a dedicated hardware profile on, so that when you fire up a specter and you want to create a multisig seed, signer actually appears as one of the options in there. But also Craig from Sparrow has been great to work with as well.

Seedsigner:

He let us ship him a test device because he didn’t have access to the components where he is. And we shipped him kind of a pre-built SeedSigner that he was able to kind of play around with and optimize the hardware profile that is on their platform for seed signer as well. So it’s like I said, the coordinator developers have been really great to work with because on both of our ends, we want users to have the best experience possible, and we want to encourage a diverse ecosystem assigning devices so that nobody is locked into one particular project or one particular manufacturer. I think that’s in everybody’s best interests.

Stephan Livera:

Yeah. That’s great to hear. And so it’s like this open ecosystem with lots and lots of choice and lots of, lots of different possibilities, and people can mix and match the different components, whether they’re using specter, desktop as their coordinator wallet, or as Sparrow as their coordinating software wallet. And so yeah, it’s interesting. You mentioned that as well around the stateless aspect, because that’s one area where different wallets will have different ways of doing it. So if you’re registering a multisig quorum into the coldcard you, yeah, it’s got that little special, special ingest backend, right? Because it can maintain a state or the Cobo which is now the Keystone, or rather the creator created the Keystone similar kind of thing where you would then ingest back in the registered multisig quorum. And I guess this is where you know, having a relationship and working with the coordinator software people like stepan and Ben Kaufman of specter and working with you know, Craig of Sparrow that the wallet knows, oh, I need to actually, if you’re, if I’m dealing with a Seed Signer, I actually need to feed it the multisig quorum in the inside the QR that has the PSBT in it, as opposed to, for the other devices where it might not do that. Right. I guess it feeds it a different thing based on what hardware wallet it is coordinating with.

Seedsigner:

Right. And there are, I can also point out there there are standards that are kind of converging within the whole air gap, QR kind of space. There’s a standard called a UR2 standard that’s been developed that allows for some fault tolerance in terms of missing QR frames and tries to smooth that process out. So it’s not it’s not a process where you feel like you have to capture every single frame. There’s some tolerance built into it. Such that the data spread out in the different QR code, so that if you miss a frame here and there, you can still gather all the necessary information. And I think there are going to be more multisig coordinators that support air gap QRs coming online, like over the next year which I think is, I think that’s that would be a very welcome development, especially in the mobile realm, because that’s really the kind of platform that the people in El Salvador can use because it’s probably no surprise to you or anybody listening that in El Salvador, they don’t have as many nodes.

Seedsigner:

Like it’s not a super common thing, unless you’re a hardcore Bitcoiner there to have your own nodes. So they’re going to be relying on a lot more of these kind of like uncle Jim setups, where you have kind of a trusted blockchain information provider. And right now, the only mobile based coordinator that I’m aware of is Blue Wallet. And they have blue wallet vaults that are very similar to what specter and Sparrow do. And that’s a great tool with kind of a semi trusted setup, but considering that even laptops, we take it for granted having access to a laptop, but most people in those kind of areas are interacting with the Bitcoin protocol through a mobile phone, and likely they’re going to start with a custodial Lightning wallet, and hopefully over time as they transact more in Bitcoin and they see the price appreciation, they’re going to want to start to use Bitcoin as a savings mechanism.

Seedsigner:

And when they accumulate a certain amount of Bitcoin, they’re going to become like we all do less and less comfortable with that Bitcoin staying with a third party provider. And they’re likely going to want to settle back to the main chain in a more independent sovereign way, and, or at least in a sovereign way to where it’s not a third party custodial kind of entity that that can access your funds. So blue wallet is a great example of something that is, it’s still kind of an uncle Jim set up where you’re using their interface to access blockchain data, but it’s not a custodial sort of set up to where you are truly custodying your own Bitcoin, that way in a multisig being able to use our gifts. You are. So I that’s a long roundabout way, but I really, there are developers out there who are mobile developers and are looking for a project. We really need more multisig coordinators that are primarily mobile based and that are fully featured and that have access to features like test net, multisig, airgap QR, all that kind of stuff. So just kind of a shout out.

Stephan Livera:

That’s a really good call out. I think because essentially what we need is like a mobile version of specter, desktop, or a mobile version of Sparrow basically. And obviously blue wallet is playing a little bit of that role for now, but it would be good to have more and more choice there. And I could imagine as this thing grows and builds out, like as an example, taking the El Salvador example, as you mentioned earlier, a lot of Salvadorians will probably start with Chivo, right? Which is the government planning wallet. There’s a custodial wallet, it’s KYC, it’s all of that. And so they’ll probably start with that. Or there might be using sort of like a Bitcoin beach style wallet. And so it’ll start in a more custodial Lightning way. And then maybe as number goes up and as the number of sats HODLed rises, then they would rather start thinking, well, if somebody get a noncustodial wallet and that might be like a phone wallet but even then they might be thinking, well, once it rises enough, you might be thinking, I don’t want to keep too much on my phone.

Stephan Livera:

I want to keep it on a hardware wallet. And then that is where the SeedSigner can come in and either be part of their single signature set up or part of a multisignature set up. But in order to facilitate that what’s needed is ideally mobile phone wallets that can do multisig. So right now it’s blue wallet, but hopefully in the future, if we mobile equivalents of specter and Sparrow, maybe that’s the direction the industry can sort of go in to make it accessible in the lower income countries. But also, I mean, and not just in the El Salvador’s of the world, but just elsewhere around the world, just to have more choice and more possibility for how people secure their coins.,

Seedsigner:

Yeah. I think we keep talking about El Salvador, I think Bitcoiners, like I’ve been I first heard about Bitcoin in 2013 when I was actually working in the forensic lab. And there’s been this narrative for so many years that we’ve all been following Bitcoin that Bitcoin can help people in third world countries and places where their currency is being debased and their purchasing power’s being diminished. And they can save on their own without having to set up an account or ask anyone for permission. And we’ve been kind of banging this drum for years and years. And so to finally have a country where it seems like if it’s going to work, this is the place where it’s going to be able to work. I think we all kind of get excited and keep referencing back to that. But like you said, like Bitcoin is for everybody everywhere in the world. And so like…

Stephan Livera:

Yeah, Exactly. And so one thing to be frank as well is that when you’re in a low income or low wealth situation, you might not have as much savings. And because you’re living more hand to mouth, but over time, hopefully you know, you can sort of come up out of that. But in the meantime, there’s millions of millions of people around the world who do have savings and they want ways to easily and safely store that. And so obviously hardware, wallets, and having more choice around how we do hardware, wallets and multisig is all part of that story. And as more and more people learn how to do these things, the more we popularize multisignature for large amounts of coin storage, then it just also as Michael Flaxman says, it might actually reduce the amount of overall attacks because if more and more people are using multisig criminals might be less likely to even try it.

Seedsigner:

Right. If multisig becomes the standard, then you know, that significantly diminishes, what do they call it? The $5 wrench attack where somebody can try to coerce you into turning over your Bitcoin. If you’re not able to do that, there’s less of an incentive for them to even try to coerce people from you know, giving up their Bitcoin in a theft situation.

Stephan Livera:

For sure. Yeah. I guess one other question I’ve got just around SeedSigner and the project in terms of people who might be thinking, oh, look, I’d like to use it, but what do I do if something goes wrong? Like, is there a technical support community? Is there like a telegram chat or is there some way that I can get support or if some upgrade or some firmware update goes wrong? What do I do?

Seedsigner:

Yeah, we absolutely have a telegram group. I think it’s coming up on 350 members strong. There’s a link in our GitHub repo. I think for whatever reason, there’s not a link on the website yet that that’s an oversight. But in terms of resources, we have of course, SeedSigner.com. We have the GitHub repo. So if you duct echo or Google seed signer or GitHub, it’ll take you there for more resources. And we have a telegram group of lots of people who are enthusiastic, and who’ve already been through the process of building one. And they’re super willing to be helpful with questions that other people may have about building one or for some reason I’ve encountered this bug or for some reason, like I can’t figure out how to set up X. It’s a great place to bounce your questions off of others and get some get some feedback.

Stephan Livera:

Yeah. Well, look, I think that’s probably a good spot to finish it up here. So thanks very much for joining me seed and listen to this, make sure you go and check out all the resources and they will also be in the show notes. Of course, the seedsigner.com and all the other resources like to GitHub and the telegram go and have a look. And yeah, any final comments there from you?

Seedsigner:

This has been amazing. You get the opportunity to talk to you and to kind of come full circle from what we discussed before, about how your podcast being kind of the origin point for this. And then coming back to get to talk to you about it has been a real thrill.

Stephan Livera:

Fantastic. Well, thank you!

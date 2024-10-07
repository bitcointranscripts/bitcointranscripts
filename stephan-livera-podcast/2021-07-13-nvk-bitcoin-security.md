---
title: Bitcoin Security & Backups Primer
transcript_by: Stephan Livera
speakers:
  - NVK
date: 2021-07-13
media: https://www.youtube.com/watch?v=K03UDeE1PeE
---
podcast: https://stephanlivera.com/episode/290/

Stephan Livera:

Mr. NVK. Welcome back to the show.

NVK:

Hey man. Thanks for having me.

Stephan Livera:

Yeah, dude, it’s been a while since we spoke about backups. So listeners, you might know we did an episode a little while back, but things change over time and we’ve got new listeners and new people coming in. So it was a good time. And I think there was a lot of support on Twitter for this idea of doing an episode specifically talking about how to do your backups. So maybe you want to just start with a little bit of a basic why do we need to do all this? Why is it important?

NVK:

Well, I mean if you go from the not your keys, not your coins principle well, if you don’t have your keys anymore, then you don’t have the coins anymore, right? It’s kinda like self-evident that it’s kind of important.

Stephan Livera:

Yeah, of course. And so maybe just to keep this friendly for the newcoiners or the new bitcoiners out there, let’s talk a little bit about a standard hardware wallet setup process, and then we’ll sort of talk about integrating that with how we think about our backups, right? So I guess you might buy a hardware wallet, you might do a firmware update and you might want to learn how to do GPG verify, right? Which is a command that you use to basically check that the firmware update that you’re installing onto that piece of hardware is legitimate. It’s correct as was signed by the creator. And then maybe you just want to tell us a little bit about that initial setup process for a hardware wallet.

NVK:

So first of all, always make sure you buy hardware wallets direct, right? Unless you have a local reseller, which like you have some level of trust, right? Always buy directly from the actual manufacturer of hardware wallets, right? So a Coldcard, like we don’t even have resellers at least not official ones because for us to vouch for a reseller, there’s definitely honest ones out there, but for us to vouch just opens people up to more attacks, right? So it’s better that way. So don’t buy it, like buy directly from us or from the other ones. And once you get a hardware wallet, right? Inspect it, right? Make sure that things look kosher that unfortunately like some are just like the little shiny sticker. That’s kind of useless. Don’t trust that that shiny seal, right.

NVK:

Those things are very easily reproducible. So that’s one of the reasons why it’s best to get directly, right? Because in order for somebody to attack to the supplier check a supply chain attack on you with directly from the manufacturer, you have to be a very targeted person, right? It’s going to be much harder for somebody to go through that trouble. So anyway, so don’t trust the little seal, buy directly from the manufacturer, make sure things look right. And then when you get it they don’t use it right away with coins, right? Always flash the firmware. That means you’re gonna download the firmware from the manufacturer. Ideally you build it from source code, but if you’re new, you’re just gonna download it, right? And then you’re going to do the GPG or PGP verify command. Unfortunately, there is no GUI for this. Not that I know of. You have to do it on the terminal. It’s very simple. Right? Like, I mean, you just type it in, there’s a million different tutorials out there. It doesn’t have to be Bitcoin specific. It’s just showing you how to do a PGP key verification, right?

Stephan Livera:

Right. And I guess while we’re here, we might just mention, there is the guides. I think Matt Odell has his one. If you go to mattodell.com, I think there’s a Coldcard guide there. Keep it Simple Bitcoin has his guide and even on Ministry of Nodes, which is my venture with Ketan. We’ve got guides as well. So just to listeners out there, there are guides out there on how to do GPG verify if you’re not sure.

NVK:

That’s a very good point. KISB made a video with us called from zero to hero. Okay. it’s more newb- focused and it does walk you through in video how to do PGP verification. It’s very simple. It just looks complicated, but it’s simple anyways. So you verify the firmware, you make sure you install the firmware right. In the correct way. You don’t have coins in the device. So there’s a lot less fear of losing funds in case there’s an issue. So now at least you have like a clean device, right? And now you’re going to go through the part that really matters, which is dealing with seeds.

Stephan Livera:

Yeah. So now we’re going to initialize that wallet. And so it would be good if you could tell us a little bit about the differences between, because people might get confused that they might’ve heard the 12 or 24 words, but then there’s also a pin and then there’s this other thing called a passphrase. So NVK, can you spell out the difference for people? What’s the difference between those 24 words, the pin and the passphrase?

NVK:

So the words they’re essentially the secret in which we calculate keys from to sign Bitcoin transactions, right? They’re kind of like how to explain this, they’re not really a password, right? They are the actual entropy, right? The actual secret sauce that protects your Bitcoins or signs or Bitcoins, right? So they’re unrelated really to the hardware that you’re using most hardware wallets will support BIP 39, which is what the seeds are based on, right? So it’s between 12 and 24 words. It should never be less than 12. And the pin, the pin is very, very specific to the hardware wallet that you’re using, right? So in Coldcard, we support, I think two sets of eight digits. If I remember, right? Most hardware wallets will support at least six and this pin is just to unlock your little device, right.

NVK:

It has nothing to do with Bitcoin itself. And now passphrase is interesting because it’s essentially just making your seed longer, right? Maybe it’s a misnomer, it’s not a great name for it. You could almost call it like a seed word extension. So say you have 24 words, right? 24 words, if you multiply that by like say if you’re doing this in math, right? And then the words were numbers, if you multiply those 24 words by a certain like random number or something, right? You’re going to get a result, right? And that result is going to be your private key. Now, if you add a few more words to that, you’re going to get a different result. So that’s a different private key. So the passphrases themselves are just an extension of that. So that you can have more secrets, like you can have an extra layer of security by just giving it — by calculating, altogether into a new secret. Does that make any sense?

Stephan Livera:

Yup. Okay. So let me just summarize that for listeners. So just for listeners, if you’re totally new and you’re like, whoa, I’m a bit lost here. Just think of it like this, your hardware wallet, will give you 24 words, right? So just to keep it simple, that 24 words is the backup for every transaction you will ever do on that device, essentially. But there’s other complicating factors, right? So you could take those same 24 words and put them into another device and it will then recreate all the same transactions. This is assuming no passphrase. Then there’s a pin which think of that, like a control that’s specific to that device. So this is just like to let you into that device. But if somebody gets the 24 words, they don’t need your pin. Now, the other complicating factor as NVK was explaining it’s the passphrase, or perhaps a better term is seed extension.

Stephan Livera:

So instead think of it like instead of a 24 word phrase, you might have a 30 word phrase with six words in your passphrase. And this passphrase is like changing the actual entropy of your Bitcoin. And so remember in Bitcoin, think of it like everybody who runs a Bitcoin node is holding a ledger with all of the Bitcoin transactions that have occurred. And so really what this is you are kind of storing your key, which allows you to unlock the coins you have and send them to another place on the ledger. That’s kind of like one way to think about it. And so really what we’re doing with these hardware wallets is we’re storing our private key. And then the hardware wallet can also do, what’s called signing a message to say, yes, I am the legitimate owner of these Bitcoins. And I am sending them to address bc1, blah, blah, some other address. So that’s a little bit of an explanation around seed words, pin and passphrase. And so then we are initializing the wallet, right? So this is creating that initial wallet. So in the case of Coldcard, there will be a couple of additional steps. You’ve got those anti-phishing code words that, which we’ll write those down. And what else is involved with the initialization step?

NVK:

Okay. So on Coldcard, what we do is we have an anti-phishing feature. So you have two sets of pins, right? One pin. And then you’re given two unique words that only you and the device know. And then you have a secondary pin. What that means is that if somebody ever swaps your device for a malicious device that could record your pin, especially remotely, if you put in half of the pin, because they don’t know the secret words, right? It would show you something else. And if it shows you something else, stop typing. Because they won’t have the second part of your pin and you’re protected. Now don’t freak out. If you put the wrong pin, initially, you’re going to get different words. So just a caveat there because the pin — the words are based on how the pin is entered. But anyways, so yeah. So what’s the next step you want to check?

Stephan Livera:

Yeah. So the next step now we would think about, well, if we want to use it with a wallet now with the Coldcard as I often mentioned, you can use it in an air gapped way, so you can actually use an SD card and export that wallet. So there’ll be a function to basically export the generic xPub. And you would then take that out and put that into your computer and use that with a wallet like Specter Desktop, or Sparrow or Electrum or Blue wallet, right? so that’s a more advanced way to use your Coldcard, but you can also use it in a direct plug way. And other hardware wallets are like that too. And NVK any tips around desktop wallets to use with our hardware wallet?

NVK:

Yeah. So I highly highly recommend using it air gapped. Yeah. So air gapping is important just because nothing is bug free. Right? So if the hardware wallet does have a bug or some backdoor that’s discovered or something, right? The fact that a hardware wallet is not connected to a computer, it’s not going to make that bug exploitable, right? So you add a layer of security. That is like huge just because you cannot remotely attack that wallet because it’s not connected to it. So that’s one comment on there. Now, I am a big fan of Specter desktop, Sparrow. Sparrow is very used to use and I like Electrum aside from privacy considerations and you can do core, but core is too tricky for most people. Now, one thing that’s really nice to do is to have maybe a spare laptop that is like, sort of clean.

NVK:

You don’t really install anything in it. And that’s sort of like your Bitcoin laptop, right? The laptop, you can run a core on it. You can sync it every time you’re going to use. It doesn’t have all your crapware you don’t surf porn on it. There is nothing that could expose you to more to more attacks, right? it’s a nice little clean machine just for you to do money things. Because remember right, if bad guys don’t know how much money you have, they may not be interested in going after you, just because they’re assuming that you don’t have a lot of money, right? So just not exposing your HODL, even if the keys are not, on the computer or a big deal. So I highly highly recommend using like, sort of like not using your main machine for it, but at the same time, listen, you’re starting out, don’t freak out. You can start from the beginning, you can use your main machine. It’s just try to improve your setup and make it sort of more sanitized as you put more time in it, as you acquire more Bitcoin.

Stephan Livera:

Yup. And so for are listeners who are new, if you are like, whoa, it’s a little bit much, what I would say is there’s probably two main choices for you. One is Sparrow wallet, which has like a default setup where it goes to that default set up will call out to somebody else’s server. But it’s been defined to certain more well-known community members who are running an Electrum server. That’s one option, but obviously it’s not as private if you’re running your own Bitcoin node, but it’s like an easy way for you to get started. Or the other way is Specter desktop. Specter desktop has this thing called quick sync, where basically they will in the background, it will run Bitcoin core and prune it, and just kind of get you to a basic level set up after something like a couple of gigs of download.

Stephan Livera:

So you can get set up relatively quickly and you don’t need a lot of technical knowledge. So that’s just a tip for new listeners and newcoiners. If you are for the first time learning about how to use a Coldcard, that’s a tip I would give for you guys. And then those of you who want to get more advanced, you want to learn to run your own Electrum private server or Electrum personal server, or Electrs which is like Electrum rust server. There are, ways to run that easily with some of the package node devices, things like myNode and Umbrel and Ronin Dojo and RaspiBlitz and so on. So then at that point — here’s one important step that I like to tell people who want to properly feel comfortable is you might start by sending a small amount of Bitcoin into that wallet and then testing actually destroying it and recovering it.

NVK:

Yeah. So we’re going to get into backups, I guess. Right?

Stephan Livera:

So as an example, you might send in a hundred bucks.

NVK:

Yeah. So first, like if you’re new, please like download the phone wallet, write down those seeds, like learn how to send Bitcoin back and forth. You know what I mean? Try it. You don’t even need the hardware wallet to start, right? Like just do with like a phone app is fine. Just to play around. So you get an understanding of like seed writing and all. Now you have your hardware wallet, right? You’re sitting there with your Coldcard, you have the little paper card, right? Let’s say that the paper card is not like the best backup, but is your working sheet right. Of backup. So you write down your pin, you write down your anti-phishing words and then you write down your 24 words. Right? So the first stop is, you know first make sure you’re not in a room that has a camera pointed at that piece of paper, especially your computer, your laptop camera is pointed at that piece of paper.

NVK:

Somebody could be watching try to like sanitize your environment, right? Like, it’s like, this is serious. This is like your money. So you’re going to have a clean desk. You’re going to have a little sticky on the laptop camera and get all set up. So you write down your 24 words I would recommend then you send a few bucks worth of Bitcoin to the hardware wallet. You then do a test transaction, right? You try to send it, you can send it to itself, back to an address you control in the same wallet. So you test that. You can sign it that that’s like the first step. So yes, I can sign it. Fantastic, right? So then you go into the hardware wallet and you actually delete your seed.

NVK:

So you go into Coldcard, into the danger zone, destroy seed, right? So that means that seed is gone from Coldcard. Now you go in and you go into import and you write down the seed again. And the wallet is going to be initialized again. And you can just check that the funds essentially show up, right? Because you’re going to be able to sign it again. So if you have those two sets of initial signing transactions, you know that the device one worked. So you don’t have to do the whole thing again. And two, you know now that your backup works is recoverable backup. So you’re in a good spot, right? So if you’re very newb, this is your first thing. You could almost stop there with this whole thing right now, you could just sort of have your normal life.

NVK:

You just have to start up a piece of paper somewhere safe. Now let’s say that you have a bit more money. And now it’s when it gets interesting with backups, right? So paper burns. So I highly recommend you get like a seed plate, right? You get like a metal backup solution. You punch in your words in there most of the metal backup solutions are only going to need the first four letters of each word. I know it’s a little confusing. However, the word list for this system of seeds has the first four letters unique of all words. So you don’t need more than four letters if it’s BIP 39. So that’s the first step with like, improving your backup to the next level right now you’re protected against fire. So you’re in a much better place because most people will not get robbed. Most people probably will have a house fire or a flood or something that destroys paper, right? So rock paper, scissors, paper’s not great. And then like, we can sort of start increasing here as like, you’re going to have many different options right. On, on how to do things and how they have different sort of gain scenarios.

Stephan Livera:

Yeah, that’s right. So that’s the, I guess the standard backup scenario. And so we would say for people, maybe when you’re starting, if you’re unsure about all this stuff, and it’s a bit too much, you can go with no passphrase. And so basically just have the 24 words and your pin and the that’s it. And then as you want to start increasing things and change and making the setup a little bit more complex, then you might start adding in the pathways, as we said. So this, depending on how secure you want to be, it might be another 5 or 6 words on top — extended to your seed, if you will. And so there’s like a little option in your Coldcard. You can go in there and basically enable or disable your passphrase. And it’s like entering a whole new wallet, basically. So do you want to tell us a little bit about what that passphrase backup looks like?

NVK:

So I think it’s very important that people don’t get confused about like, you must have a minimum of a metal backup for your normal seed phrase, right? At a minimum, you have a metal backup, and then for your passphrase, you also need a backup, right? Ideally, they’re not together. So you’re going to have one metal plate for your seed, and then you get a second metal plate. And instead of just using random, I highly discourage people to use a random passphrase just because you don’t write it down correctly or it’s hard to read. And then you have like a widow that cannot recover from, from, from that, right? So I highly, highly recommend people picking words from the same word list, right? The BIP 39 word list. We can add it to the show notes, some links to it.

NVK:

And then you put those word lists, which are compatible with most metal backup solutions, right? And you have a nice little backup of that as well. And ideally those two pieces are kept separately because if somebody gets hold of both parts, they could spend your coins, right? So that’s sort of like the first way of doing this another way of doing this is for example if you don’t want to have a passphrase, right? You could, for example, split your main seed, right? You can’t just cut it in half. That’s not a good idea. So we created this little thing called SeedXOR. It’s very easy to use. It’s compatible with any other wallet. What essentially it does is it lets you create a seed from two seeds, right? It cannot be done in reverse.

NVK:

You cannot split the seed. You can only combine the two to create a new one. What’s nice about that is that you can have a secret in two separate places to make the original, big secret, right? If you want to add a passphrase on top of that, you can as well. So you can sort of further decentralize your seed solutions. Now caveat, you always have to be careful because again, chances of you getting robbed are much smaller than you screwing yourself out of your coins. So don’t complicate things too much to a degree that you are not comfortable, or if you’re dead, the people who you’re leaving things to are uncomfortable about. What I like to say is like don’t create treasure hunts to your grieving family.

Stephan Livera:

Yeah. So we can think of it, like there’s different ways to go about this. So you might just have when you’re starting no passphrase and just 24 words and then you might say next level is to have a passphrase and in that passphrase context, you might have the Coldcard in one location. And the passphrase backed up in another. And so there’s different scenarios. And then, so then the next level is we’re talking about is SeedXOR. So this is a new feature relatively, where you can actually sort of split up your key a little bit in a way that requires all of the pieces, right? So you might set it up into three pieces where you need all three to reconstitute the overall thing, right?

NVK:

That’s right. What’s really nice about that is that it’s plausibly deniable. So we built this really because we found that people couldn’t find a spot to keep their seeds, right? That was not possibly very exposed. So people were putting seeds in safe deposit boxes, right? That’s how a lot of people do it. And the problem is if the puzzle box is that they’re capturable right. They’re capturable, by the state, they might be capturable by somebody with a very good fake ID and the right story. It’s essentially your seed is sitting on somebody else’s house. Right? Like it just happens to be a very safe house, but still it’s somebody else’s place like you don’t control the bank vault, right? So what do we want it to do is give people a chance to maybe get two separate, safe deposit boxes in two separate banks.

NVK:

Right now it’s much harder to attack that. Maybe they’re in different countries, maybe they’re in different states, right? Maybe they’re in different names. So now you can put a seed there. And what’s cool about the SeedXOR is that seed looks like a normal 24 word seed with checksum. So you could even put a little bit of fake money, or like just decoy money on that seed. So if somebody gets hold of that, they think they got what you had, right? and plausible deniability around most attack scenarios in like in private key defense, right? It’s like one of the best things you can do because you are not — like infallible. You’re not bulletproof. Family members could be used as leverage. Other things could be used as leverage.

NVK:

So if you have a good story, a very believable story, right? To deal with things you are much ahead, right? Because most of the low level, mid level, even some of the high level attackers, won’t be able to get past that story, right? Because it checks up, right? So building those layers is very helpful. So that you have — say, you have like a decoy hardware wallet in your house, right? Then you can give to the bad guy, that one, he can even take it, and then you have a next one. And then the next one has maybe a passphrase as well, right? So you can keep on building these layers, both on your personal vicinity and also where you store your backups. It will buy you time and that we’ll give you a lot more security, right? Because you have time to move funds to remove yourself from the situation. Because remember bad guys are always on a timer, right? They don’t have all the time in the world, they have to move on. So you’re really adding a lot of defense to your system that way.

Stephan Livera:

Yeah. Then I guess you just have to think about your redundancy also, right? Because as an example, if you are creating it into two of two SeedXOR set up, or now you’ve got to make sure you can access both, because if you lose one of them, now you’re in trouble. So it’s just about making sure you are covered from that point of view.

NVK:

Yes. So one thing I love to suggest to people to do, if they are going to go the SeedXOR route is to, they could have two copies of each part and just distribute them further, right? So if they lose one, they’re not out of luck. They could also have a passphrase on top of that, so that they have say a full seed backed up somewhere, very deep in the sea kind of thing, right? And then they have the two parts in places where a little bit more accessible in case you need to recover and you have a passphrase on top of that. So if somebody finds the one under the sea, they can’t get it, right? so like, you’re much more ahead. And I think I should add that, like you never want to be in a position where you could sign your wealth out, right? You want to be able to to like truthfully right under duress say like, I don’t have access to my BTC to sign it all out. So you have to sort of like put that in into your scenario. You don’t have your hardware wallet with all your Bitcoin, like in your house, because you could do that. And somebody like uses the type of attacks that works against you. They will make you sign.

Stephan Livera:

Right. Yeah. Now, I’m just imagining some new listeners might be thinking, whoa, this is a lot! So I would say, look, just start basic and slowly work your way up. So you could start with just single hardware wallet, no passphrase just start basic. And then maybe the next level is, okay, now I’m going to have a passphrase. I’m going to think about, okay, I’m going to have my Coldcard and the steel backup at home for it, but I’ve got a passphrase and that passphrase is backed up into another location. So that way the attacker has to take me to this other location.

NVK:

Yeah, that’s right. So I think, I think what we maybe should split this in two, right? Because we got a lot of feedback on Twitter about this pod. So maybe it’s like, if you are a newb stop a few minutes ago, right? Like don’t over complicate the rest. Maybe the rest of this conversation is more sort of like it’s more for your curiosity, but you don’t have to do a lot of this stuff. There is people who hold hundreds of millions of dollars, right? Like who need to keep things. And there’s people who live in countries that have security considerations, there’s people who live in safe places. So find what is comfortable to you at this point in your life, with the amount of money that you have at this point in your life, right? You don’t have to go too far. So you’re okay. Have your — just your seed. It’s fine. You’re okay. Hold, hold your initial sort of Bitcoin HODL, right? And then as the price increases, as you acquire more, then you inquire further into how to make more complex systems, because this thing is also going to make sense to you as you use Bitcoin more often.

Stephan Livera:

Yep. Correct. Okay. And so now we’ve spoken about SeedXOR, but what about the encrypted SD card backup? Because I know that’s another prominent feature in the Coldcard, and even Matt Odell’s infamous Tales from the Crypt guide, the one where everyone was talking about his hands has an encrypted, a SD card back off say, can you tell us a little bit about that and how that might fit into this whole scenario?

NVK:

So it’s very nice and convenient to have an encrypted backup of your seed in digital form, right? Say you accidentally run over your hardware wallet and it breaks, right? Like now you’re going to have to go under the sea or to a different country or whatever, to pick up your backups right now, if you have an encrypted backup somewhere that is not easy accessible, but it’s easier accessible, right? So you just have to travel to another state and then go into a safe deposit box and find that backup, right? So that it can recover your hardware wallet. What’s nice about that is that that micro SD card has all the settings of the Coldcard. It has everything you need. And because maybe you use the passphrase right that, micro SD card, even if you you’re compelled to give the encryption keys to the micro SD card, you’re still in a good place because you have a passphrase on top of that, it’s important to not have a single point of failure that is either via duress or because of accident.

NVK:

So having enough backups out there in different forms, will help you recover in case you need or help family members recovery in case you need, right? Maybe you don’t use the micro SD card with yourself. Maybe it’s a very remote place, but you can leave the instructions to a family member on how to get that card, right? And maybe it’s easier for them to deal with that card and the password because the password has no Bitcoin consequence, right? You can give them the password. They just need possession of that card.

Stephan Livera:

So as an example, they could have a location where they go to pick up the encrypted SD backup, and then you tell them also, that’s not all, you need to actually get the passphrase, which is in this other location. So then if an attacker comes to your house, gun to the head, you can literally be like, look, I can’t access the coins right now. It’s in different location. You’re gonna have to take me to this other location. And this other location might be in a vault. It might be in a security location. It might be overseas. It might be in international. So there’s also different ways of approaching that. Now let’s bring up what a lot of people are thinking about, which is also multisignature right now. There’s different ways to go about multisignature you can use the let’s call it guided multisig with say my sponsor, Unchained Capital or Casa. They’re probably the two well-known providers there. Or you can go DIY, right? So Specter Desktop, Sparrow, Electrum others. They support this function where you can create your own. What’s your thought there on using a Coldcard as part of a multisignature set up in contrast to doing something like SeedXOR?

NVK:

I think if you’re a newb seeking multisig, you pretty much have to go with like a paid solution like Casa or Unchained. Unfortunately, there are privacy consequences of doing that. They will know how much Bitcoin you have, right? There is no way around that. But multisig is amazing. Let’s start from that premise. Right? It’s a really cool thing, right? Because you need multiple keys to be able to sign it. However, it’s very complicated. Especially if you’re gonna do a DIY, if you’re a seasoned Bitcoiner, you can totally do it right. But like for a newb, I really discouraged doing it because I’ve seen people lose money because they can’t recover their setup. Now, with Unchained and Casa, what they’re going to do is they both have two separate types of preferences on how they do this stuff, but they will help you make sure you don’t screw yourself.

NVK:

Right. So they will sort of like help you set up the wallets, help you set up the backups, give you a lot of education and they will hand hold you when problems happen as well. And they will explain to you the things that you have to keep so that they can help you recover in case you do screw yourself. So you’re more safe that way, but again, you’re exposing yourself to American companies, right? Like with very private information, I’m sure they have some ways of doing this anon as well. I haven’t explored like how, good those anon options are. But it’s totally worth it. If you already have KYCed coins, for example, right? If you are say a company or a family trust or something where it’s already very like your Coinbase kind of trading a desk for your family office or whatever in all this, Casa, and Unchained are great services because it’s already sort of pwned anyways.

NVK:

Right. now there’s very good solutions now that made multisig much easier, right? So Sparrow, Specter Blue wallet to a certain extent, they do make enrolling and creating the multisig much easier. Coldcard, it can also do this very easy if you use Coldcard only so multiple Coldcards, because we can create for you the quorum. However, again make sure that like, you know what you’re doing, you’re not just complicating your life with multisig because you heard that multisig is good. Don’t do anything because you heard. Go explore yourself and feel that you’re very competent and confident with the solution you’re gonna use. So yeah, so like I do recommend it. I do. I am not a fan of multi-vendor multisig at this point, unless you’re a very advanced user, because none of the vendors, including us is capable of supporting the giving full support to the multi-vendor multisig, right?

NVK:

Because each hardware wallet, each vendor has their way of doing things, different preferences, different ways on how they prefer to set up all the complications around like each of the signers. Right? So if you’re a very advanced user, by all means Michael Flaxman has a great guide. Bitcoin QnA has great guys Openoms, have great guys you guys at Ministry of Nodes, good guys on this. Matt Odell has some. There’s a plethora of guides out there. But again you could be out of luck. If the vendors changed their firmware. For example, this happened to another vendor where they changed their firmware and all of a sudden they broke everybody’s multisig. It’s tricky.

Stephan Livera:

Yeah. And what I could suggest is get comfortable with one main setup, and then you could have multiple other setups that you’re testing, and you’re trying to learn and have a small amount of coin on setups while you’re learning on those. And then you can sort of try practicing around with those, but yeah, you’re right. It is difficult if you are DIY and trying to do the multi-vendor approach, but I’m confident, I’m hopeful that with things like Specter and Sparrow improving over time, and hopefully we sort of get to a point where that’s possible. But otherwise for listeners out there who are like, well, I really want the security of multisig. And I’m okay with the privacy trade-off then Unchained or Casa certainly are options there. So I guess, do you have any thoughts in terms of backups in a multisignature context, just as we’re talking about backups?

NVK:

Yeah. It’s very similar right. to the SeedXOR backup considerations, right? You now have multiple parts, you should have every part in metal personally, that’s what I think people should do. And I, think when you can debate a Bitcoiner on that, you’re probably ready to have your own solution. So if you’re starting out and you’re just listening to us and taking our advice then go with metal for all the options there, make sure they are not combinable in where they are. So they are different locations. Each part is in a different location, remember paper burns and electronics die, right? So you can’t just put a hardware wallet in a safe and expect that to be like, good forever there. Maybe you forget how you did the backup and then you die.

NVK:

And then years later your family finds out that you had Bitcoin and they go recover and the device is dead, right? It could happen. So make sure that when you think about the physical storage of those backups, you’re thinking about two sort of rule of thumbs, right? One is if Bitcoin was 10 or a 100 times more per Dollar today, is my backup good enough? Right? Two is, if I die, can they recover? Three is if I die and they don’t know about it because whatever reasons you did a poor way of leaving the instructions behind or something and years pass, is it still there? It’ll did you prepay that safe deposit box for enough time? Right. Imagine if a trustee like a bank trustee or something like takes hold of that. And it takes a picture of that seed and then sort of spends it, right? So that’s why it’s so important that there’s so many, you essentially want to prevent all these things from happening. And it’s very easy to prevent them from happening. If you just sort of like follow a little bit of this advice.

Stephan Livera:

So it’s basically planning it out. And right now it is early in inheritance planning days as my recent episode with Hector Rosekrans, from Casa, we spoke about that and he was saying, he gave an example where there are literally, some lawyers who are emailing around seed words, right? Like that’s the level we’re at these days. So be careful out there and think about carefully about how you’re doing your backups. And generally that means have metal seeds. And so that means get a metal product. And so in the case of Coldcard, you’ve got the seedplate, or, I mean, you can use the seed plate with any hardware wallet it really, and basically you buy that metal stamper thing, it’s called an automatic center punch. And then basically you go and stamp out those words. So four letters per word, as we said, and then you have multiple locations.

Stephan Livera:

So now let’s talk a little bit about locations of our backups, right? So I guess high level, there’s a few ways to think about it, right? So in your home, you might have a home safe, or you might get one installed that’s one location. And you might have, let’s say a safe deposit box. You might have one in a bank, or you might have one in say like a self storage kind of place. And then there’s, I guess the idea of also with geographic distribution. So you might have say someplace in another state or in another country. So could you just give some tips for listeners out there on locations for their backups and for the hardware wallet itself?

NVK:

Right. So don’t leave your hardware wallet on your desk or leave one in your desk. That’s a decoy one. Because I make hardware wallets, I probably have 200 in my house. So like good luck with that. So I think it’s important that people realize that safes are not infallible. Right? So metal safes, they have ratings, right? So 15 minutes, 30 minutes, that kind of stuff, right? And even a pricier safe, say like you spend like three, five, $10,000 on a safe for your house, right? So like you get like a TL 30, right? So it’s supposed to survive 30 minutes with like full on, right? Reality is it’s a lot quicker. So you can ask any safe manufacturer. They know exactly where to cut and how to open, like it opens like butter, right.

NVK:

And I’m talking about like a safe here, the door is almost a foot deep. Okay. This guys can just like done. So safes are great to prevent, say, meth heads from taking it from your house, or like your more average home burglar, right? Some safes will also have like a more reasonable fire rating as well, which is kinda nice. So and also, your documents don’t burn as well, right? At least if they’re in the correct installation location. So just assume, right? That that safe in your house when it could be compelled to open and to, it could be opened in enough time. So you’re just trying to prevent the low to mid-level guys from getting it right. Which is a huge improvement. Now that’s safe shouldn’t be visible? It should be like probably hidden somewhere.

NVK:

And then safe deposit boxes are great, different countries have different laws around that, right? So you have to be careful. You have to do some research on where you live. What are the requirements for somebody to get in? what happens if you die and don’t pay the bill? Or if you just fail to pay the bill because you forgot, right? Like what happens to the safe deposit box? Another cool thing about doing physical backup solutions is that humanity has thousands of years of like improved custody — chain of custody for physical things, right? So lawyers don’t know how to deal with digital seeds. They’ll send it on an email, right? But if you tell them that this is a secret in metal, they’ll put it in an envelope, right? And they will deliver it to the family or whatever, physically with chain of custody. Same for police matters, right? they know how to handle this stuff to a certain extent. Of course. So yeah, so safe deposit boxes are great. Geographically distributed, safe deposit boxes are fantastic too, right? So you can go to another state or another city or another country, right? Where if a bad guy wants to take it from you, it’s like, you’re going to do, like, do you want to go for a two week trip with me? Right. Like, have you to another country,

Stephan Livera:

And sit through quarantine as well?

NVK:

Exactly, right? And the different country will also have different laws and regulations around releasing that safe deposit box. So you might have some protection against whatever government you have, right? They might not be able to compel the other country to release that safe deposit box, or it could be some countries are specialized in this stuff, right? So like Monaco or Switzerland, they will have very, very interesting solutions around this stuff. You can also leave it to your family members. If you did your SeedXOR or your multisig where that one seed is not a concern, right? You can put inside the little envelope or something else. And give it to a family member to hold it for you in a different location, right? you can do the encrypted backup. You can leave it with a family member because they can’t really use it.

NVK:

They cannot be compelled to use it, right? You have to think about them being malicious and also them being compelled. And if you have like maybe some some property somewhere that has a bit more space, you can bury it, right? There is many ways of hiding secrets around. It just makes sure that like they’re recoverable, family members know where they are. And then if you die in sometime and that somebody does find it and spend it before your family does, right? again, no treasure hunts for grieving family. It’s not a good idea.

Stephan Livera:

Yeah. And another tip I know of is to make sure your family have a contact person who they can trust on Bitcoin. Right? So like it, at that time, they’re going to be under stress. They’re going to be feeling it, and they need to go to somebody who knows what they’re talking about and can help them recover. And so it would be good if you tell them in advance, Hey, if something happens to me, this guy can help you Bitcoin wise, right? With recovery and doing these things.

NVK:

And add a note there. Never show that person the seed words, unless you really, really need to, because their relationship may have changed and you don’t know that it changed. So say, for example, you you’ll find out that your partner left you a seed and a passphrase, right? Maybe this person is helping you set up the wallet again, you don’t have to show them the passphrase, or even the seed. An honest helper in IT will turn the laptop around, let you type in the password or seed, right? And then turn it back for them to help you do that stuff. They don’t need to see the secrets, right? That’s like a good sort of way of going about, because if something did happen, it could get awkward, right? Say for example, somebody else found out that seed and that those funds were spent and this guy helping you and he sees the seed, and now you don’t know if he stole it from you or if it was pre stolen, right? So don’t put yourself in that situation.

Stephan Livera:

Yeah. Okay. also there’s this question of whether people should have all of, or let’s say most their HODL stack all in one big, super secure setup, or should they be splitting it across multiple set ups? Do you have any thoughts on that?

NVK:

I do. I think if you’re somebody who’s new, right? And you’re just sort of –so you’re just buying some Bitcoin to accumulate, right? You just started, right? Having a simple set up as a single one. You start to understand it fully and go from there. As you increase your Bitcoin HODL, it is nice to decentralize it a bit, right? You might want to have, say, a warm setup, right? Where it’s like, you have a hardware wallet. That’s your operational one where when you go buy Bitcoin or you go trade Bitcoin, you use that one. And then you have a threshold in which if it crosses a certain amount, you transfer parts of it to your deep, deep storage, right? And because remember your deep, deep storage is inaccessible to you without some serious amount of work.

NVK:

Right? So what’s cool about that is you always have some in case you’re trying to trade you’re trying to leverage whatever you’re trying to do, right? I think it’s nice to have that, or you’re trying to experiment with different backup systems. It’s nice to explore. So do have an intermediary, a system at a minimum. I think. And then as you HODL the increase even further, or maybe you have I dunno, multiple families, right? Like your divorce and like you have a previous wife and like, you have different families, you have more complications in your life, or maybe you manage funds for your family office or whatever, right? You’ll start having more setups because remember if you’re made to compel and they know you have a hardware wallet or something, you have something that is believable or it’s actually like what you have, right? Like honestly have and you’re not completely lost, right? So it is nice to have more options there too. Kind of like how you have checking and savings in your bank account, right? it’s nice to have that sort of separation because you’re treated differently too. And it helps the taxes as well. If this is a consideration for you.

Stephan Livera:

Yeah. And so listeners might want to think of segregating their coins, and this might also be useful in a KYC coins and non KYC coins context. You might want to segregate from that point of view as well. So you might let’s say have a non KYC, little portion of coins that you keep on, say a coin join wallet, like say a Samourai wallet or JoinMarket, let’s say and then your kind of other stuff is on the Coldcard and or multisig or SeedXOR or those kinds of setups. And so I guess going back to that checking account and savings account analogy. So let’s say you have a checking account and a savings account. What about the idea of having multiple savings accounts? Should you have multiple, let’s say multisig setups, or say two savings accounts. One of them is a multisig and then another account that’s like a SeedXOR with like another say 40% of your stack is there. And 50% of the stack is there and 10% is in your intermediate wallet. Do you have any thoughts on that or…

NVK:

Yeah. I mean, if that makes sense to you, you should absolutely do it, but like learn to crawl before walk, right? So just increase things progressively so that you don’t get overwhelmed and you get stuck with like, oh my God, I have like five wallets now. And they’re all different than I don’t know what’s going on, right? Cause remember, you’re still going to have to find secure ways of documenting all this stuff to family if you die, right? So it’s important to not overcomplicate, but complicated enough so that you’re like secure and functional, right? So find a balance, create a little decision three, right? So get a piece of paper and throw out, right? Like your plan, right? In a very high level first and then sort of like go in there and sort of like add in, like, how do you intend of backing up each of these parts, right.

NVK:

How are you gonna like split things? How do you leave each part for the person that’s going to receive it, if you die, right? Maybe it’s like both you and your partner dies and your kids are too young to recover it, right? So like, how is the people who are going to recover it, gonna deal with it? It can get very tricky. So having a map is really nice and then we burn the map of course, right? Make sure you don’t leave you formation. That’s going to give bad guys your full map, right? Your full idea of how you do things because obscurity really helps.

Stephan Livera:

Right. Obscurity, shouldn’t be the only thing, but it can be part of your overall context, right? There’s no need to go out broadcasting to the world, “This is exactly how I store all my coins”. So yeah. A couple of other questions that came up just from the Twitter discussion as well. Do you have any thoughts on crossing country borders with a large stash of coins? Should we be using multisignature to mail hardware to the country and go from A, to B set up the hardware wallets the other side, then come back to A and send your coins into B from A, or should you be going overseas with a passphrase in your head or… Do you have any thoughts on that?

NVK:

Well, let me premise this first to say that most countries have capital controls on property as well. Right? So transporting large amounts of money between borders can get dicey and tricky, depending on which country you live in, where you’re going the amount exact and so like doing your research, right? But at a minimum, I’d say, don’t take your hardware wallet through customs, right? Because you don’t know, like, even if your country allows you to take however much you want out of the country, you don’t know the border agents, either the country you’re leaving or the country you are arriving, right? These guys could get confused. It could be malicious. It could be non-malicious. I mean, you look at the silk road guys, you can all like all the law enforcement made money illegaly.

NVK:

on that operation, right? so watch out for that. if you’re leaving some country that you’re trying to exfiltrate like Bitcoin, because like they’re trying to kill you or come after you or whatever, right? You also don’t want to take the hardware wallet with you through the airport, but you can, you can maybe write those seed words in a book, right? You can take an encrypted micro SD inside a camera with pictures on it. You could mail yourself to the new address, right? The encrypted micro SD you can try to remember part of the seed, right? Say you’re doing this, like you find out that whatever legislation in country you’re in requires you to go set up something in the other country and whatever, right?

NVK:

So for even your own security, you don’t want to have signing capabilities for everything on you anyways, so you might want to travel there to set up a hardware wallet there. Have everything you need there, test the transaction there, and then bring an address back with you, right? And then send the money out and then travel, right? maybe it is a multisig solution. Maybe you even just send everything to an exchange and then we draw there, right? I think it’s important that you put some thought into the key scenarios, right? Of one, your legal framework. Two, you’re not overexposing yourself during that trip, right? With everything. And three, your new location is properly backed up too. Right? So like, you had to do this amazing setup. You have your safety for all this stuff is awesome.

NVK:

Right. And then like you take your hardware wallet with you like with full signing capabilities, through an airport, into a new country, right? Like, it’s not a good idea. So really put some thought into it. And if you are fleeing in a hurry from like some insanity going on in your country, right? I mean, I don’t know, like some dictator says everybody’s Bitcoins mine now, right? Maybe you just take your seed and paper in your head and you travel, destroy the backups eventually, or just make sure they’re inaccessible right. And move on with your life, right? The beauty of Bitcoin is it gives you the capability of escaping tyranny with all your money. Yeah. So there’s many ways for you to accomplish that.

Stephan Livera:

And so perhaps an idea then is to have some spare hardware, wallets, and metal backups at your house that you have uninitialized and unused. So you’ve got them ready to go. If you need to change something or spin something up or some say, you go and check one of your keys and you find, oh, the key is broken. I need to replace it. Well, I’ve got some spare Coldcards at home, new ones that I can open the bag and put that into the setup.

NVK:

Highly recommend having spares because things break, right? I mean, let’s say you’re doing a real estate transaction, right? You decided to either borrow against BTC or sell some or whatever, right? And it’s a timely transaction in your life, right? You have to spend it at a certain date, you have to be done. What if the hardware wallet breaks, right? You drop it on the floor, breaks the screen, right? you want to be able to quickly recover into something else and having spare hardware around is going to help you make sure that you can accomplish that. without stress theoretically, you could load that seed into another wallet or whatever, but you don’t want to expose yourself to other attack factors because you don’t have a way of recovering in the same way that it did before. So having spares is very useful.

Stephan Livera:

Yep. So that’s another thing that might ease the mind of listeners out there to have some spares of whatever hardware wallets you’re using, right? If it’s Coldcard plus something else, whatever other hardware wallets you’re using. So maybe just to summarize then, so I guess a typical flow or way that a newcoiner might come in today, they might start with a phone wallet. Right? So as an example, something like Muun wallet is probably a good example to start on just as a phone wallet, just to get started, start out with a couple of hundred bucks on there just to learn. And then the next step is hardware wallet. And then maybe next step is passphrase. And then maybe next step is SeedXOR. And then maybe beyond that, you’re thinking, okay, now I really want to go hardcore.

Stephan Livera:

I want to go multisig and I’m ready. I’ve learned I’ve done my time. I’ve done my learning. I’m comfortable with how to use multiple types of hardware wallets. I know how to use Specter and Sparrow. I know how to run my own Bitcoin node. I know how to recover. I’ve tested recovering I’m sort of familiar with these different products now I’m ready for the maximum or at least a high level of security. Do you have any tips to add there in terms of progression steps for people like, let’s say someone’s coming in?

NVK:

I think you nailed it. I think the phone wallet with seed is a very good learning experience. Right? Learn how to recover, learn how to transfer that seed to something else you can play around. It’s play money, right? For you to learn and understand how all this seed thing works, right? Because it sounds complicated. But once you put a little bit of time into it becomes like second nature, right? It’s very simple. It’s kind of like, I don’t have to explain to you how a car key works. You understand that the car key is a secret that if you stick it in there and you use it in the right way, he turns on the car, right? I bet when those things came about, everybody was confused about car keys and trying to understand how they work, right? So it’s just like it’s familiarity.

NVK:

Right? So get familiar with handling seeds securely, making sure you don’t have a camera behind you accidentally, right? Like all those things and then do progress into the hardware wallet. One thing you should never do, absolutely never do is have seeds or private keys on computers. Computers are fully pwnable. They’re not devices designed to holds secrets. Right? So they have viruses. There’s all kinds of considerations, right? So unless you’re an absolute expert, which then we can debate all day. But like, if you’re listening to this for advice, you probably not somebody who can set up a secure freeBSD box, right? So don’t put seeds and private keys on computers, including multisig and don’t make paper wallets because paper wallets, you’re also exposing yourself to the computer that generated that paper wallet if you’re doing the paper wallet inside Coldcard is a different story, but it’s a whole different rabbit hole.

NVK:

So I highly discourage that. It’s a nice little rule of thumb is to keep you safe. People stop losing money when they stop using computers for private keys. So yeah, so you go into the hardware wallet thing, that’s the next step. And then you can try the passphrase thing. With the SeedXOR, you could actually reuse maybe those seeds, if you want to, as your — because they’re already distributed, you already have this awesome set up. You can maybe use them as your multisig keys because they are valid seeds. There is a lot of, sort of like mix and match that you can do as you have a better understanding of how the stuff works.

Stephan Livera:

Okay. So let’s just refresh some of those key points for people. I think it would be good to talk about what are the common pitfalls, right? So common pitfalls. Number one. Don’t, over-complicate your setup, right? Keep it simple. Don’t forget to have your backups, right? Because people can screw that up. Don’t forget to test your backups because backups might not be correct. You might’ve written it down wrong. So actually, do you have any tips there for testing backups on say, Coldcard?

NVK:

Yeah. So the best way to test the backup is destroy the seed before you have too much money in it just a little bit, right? So remove the seed from the device and recover from backup. So if you have SeedXOR, Coldcard is going to walk you through how to recover from that. If you’re using Shamir, you do that in the devices that support that whatever set up you have, pretend it’s broken, right? That’s the idea of recovery backups pretend you’ll actually broke it. So make it lose the secret and then try to recover from the exact backups set up that you have for your real thing. And if it all shows up there and everything works great, you know, like that doesn’t matter what happened. You can actually recover from that backup because you tested it.

Stephan Livera:

So one tip there for listeners as well. Cause I’m sure there might be some listeners out there saying, oh, hang on. But guys, I’ve already put my coins on my hardware wallet. How do I test that now? Well, remember there are other ways to test. So another example could be, let’s say you get your metal seed back up. And you’re just comparing that. And you go into Coldcard and there’s a thing called view seed words. And you just compare that this is what you’ve written down on your metal seed and see, is that the same. Other things you can check, you can check is the fingerprint the same, right? So with Coldcard, when you set up a wallet, it’s got that little fingerprint thing saying, oh, I can’t remember. It’s like, I dunno, maybe 10 characters or something like that. And you can check that when you recover it recovers to the same fingerprint. So that’s another tip there for listeners who want to test their backup.

NVK:

Yeah. So another very easy way to do it. Say you’re don’t want to mangle with you’re the one that’s working, right? Just buy a second one and then recover into the secondary device and maybe keep that secondary device with the backup. So you have a ready to go backup device for that part of the secret. Very useful especially for multisig, you could keep each of the signers stored with each of the metal backups. So that you have them all ready to go in case you need to go recover. That’s super useful.

Stephan Livera:

Yeah. So going back to the pitfalls, I would say another one I’ve seen is don’t do things you’re not comfortable with. Right? So, I mean, obviously when you’re learning, you might be a little bit uncomfortable, but don’t do things that are way outside your comfort zone. Because if you’re doing something way outside your comfort zone, there’s a good chance you’re gonna mess something up because you don’t understand something you’re doing. So try to get comfortable, get familiar with it. And then you’ll be more sure about what you’re doing because you’ve recovered it before you’ve done. You’ve been here. You’ve done that.

NVK:

It’s kind of interesting because a lot of the complication comes because people shouldn’t do what the experts do. People should do, what the experts suggest. It’s very different, right? When people go on Bitcoin Twitter, for example, and they see all the expert arguing about like the best secure element super complicated, like multisig set up. So whatever, it’s like we’re all talking and trying to find the best solutions for people, right? But you shouldn’t go and just do it because that expert does it, right? Because he knows how to recover in case he screws up. So you should do what you are very comfortable in terms of complication. So yeah, so don’t do experts do, just listen to the advice that they give in terms of like the more simple stuff to begin.

Stephan Livera:

Yep. Okay. Well, I think that those are the key ones. Oh, one other one, actually. So there’s discussion now about this idea of output script descriptors. And so this is maybe a different context and maybe this is a little bit more of an advanced conversation, maybe not for the beginners, but for years and years in Bitcoin, a lot of people have been using the BIP 39 style set up and potentially with a passphrase, or they’ve been using multisig on certain kind of well-known well-trodden pathways. What happens if, and when we move into this output script, descriptor context, like as an example, I know Muun wallet, their backup is already doing output script descriptors, but most of the wallets are not at that level yet. Do you have any thoughts on,

NVK:

Yeah, it’s the same Coldcard. We absolutely love output descriptors. Remember I created a website, walletsrecovery.org, because, so in Bitcoin you essentially have two things that you need to know in order to spend, right? You need to know the secret, but you also need to know where the coins are in order to spend them and in multisig that’s a script. So it gets complicated, right? So BIP 39, the seeds don’t have versions. They don’t have location of the coins. None of that stuff. They’re just the secrets. So what else could the desscripters do is describe, right? A way of you to find the coins programmatically. So it’s just it’s just a very good way for us to find the coins, to construct the transaction that then you need the secret to sign, right? So it is definitely better than like anything else that we had.

NVK:

Now we do have it, more wallets are supporting it. And as I like to say, when you are creating backups for your whole setup, create a backup of the wallet that you use. So if that’s Electrum, Specter or whatever, make a backup of that, and specifically the version that you were using in case things change in the future, and you have a gap right. Between when you had things set up and when your family is recovering or whatever they can go use the old software and get the money out much easier and make sure you back up your derivation path if you’re not using descriptors because what the descriptors do is they will describe the derivation path in a way the wallets can just import right. Don’t mingle and do custom derivation paths. It’s another good issue to always remember a lot of said stories of people that simply can’t find their coins because they created some custom thing or used some wallet at the time that was not standard. This space is infinite near infinite of where the coins could be. So it gets very tricky. So yeah, so output discriptors are great. I created a little website. I think it’s outputdescriptors.org or something. The lists of wallets, the support output descriptors. I might have even linked from walletsrecovery.org.

Stephan Livera:

Got it. Okay. Yeah. I can put that in the show notes for listeners and yeah. And in terms of the backups as well. So as an example, you might want to have that, as you said, the backup of the wallet, the version used to create that set up on, say a USB and you keep that in the different locations. Right? So as an example, you might have multisig and you might have three of five or two of three, and each of those locations, you’ve got a USB key with the backup saying, okay, this was like the output descriptor. This was the specter desktop version with each backups. So that way you’re making sure.

NVK:

So you gotta be careful, right? Because if you’re including your public key, right? There’s a privacy concern, right? So maybe you don’t have it in all the boxes, or maybe you have in the boxes that you have more control, or maybe you bury it or whatever, just be mindful that there is a privacy consideration with those with the backup. So the attacker could now know how much coin there is.

Stephan Livera:

Yes. So this is like a trade off between having redundancy versus privacy, right? So I guess if you want to try to cut it in the middle of what you could do is say, okay, family members in the locations that you guys have access to, I’ll put the privacy concern back up in there, the USB key with that stuff. And then for the other locations, I won’t have it there. Right? Maybe that’s one way to try to cut it in the middle a little bit, but you have to — listeners, you have to make your own decision, what’s more important to you, redundancy being able to recover under any circumstance? Or privacy of your coins and anybody, or let’s say the state or some big company, or an attacker, knowing how many coins you have and the locations of those coins, if you will.

NVK:

Yeah. It’s all a balance really is, right? And different people have different preferences. They will live in different countries that have different security concerns, right? So you really have to study and sort of think about your life, right? And sort of like where I live, like, is it a consideration or not? Right. Where do I put backups? How many backups? And put some thought into it. Don’t just like take advice from people because their life circumstances might be different than yours, right? Maybe you don’t even have like anybody to inherit your coins if you die, right? So like how do you leave that to somebody, right? Like, what’s your plan? Are you going to do a proof of burn and then make everybody else richer? Or like, what are you going to do?

NVK:

Right. I think it’s important for you to think, just take time to think there’s no hurry, right? Just get off zero, right? So have BTC. And the other part is take your time to build your security set up and you can always change it. you’re not stuck with that. It’s not like a bank account that like it’s a pain in the ass to create a new one. No, you just, you can always just create a new, no finger or try different stuff, right? It’s actually a lot of fun once you get into it.

Stephan Livera:

Excellent. All right. Well, I think those are a lot of good tips for listeners out there. Hopefully they have benefited from this, and this is probably one of those ones where things change. So it’s kind of good to do an update episode every now and again, to kind of refresh that for listeners out there. And especially if there’s a lot of new people. So let’s just, I guess, leave people with tips on where to find you online. So Twitter @NVK, and you can go to coinkite.com and get your Coldcards there and get your other material there. Of course, use code LIVERA. NVK anywhere else. So you’ve got walletsrecovery.org any other sites, anything else you want people to find?

NVK:

There’s wallets recovery, like related to the topic. Oh there is the Bitcoinsecurity.guide. That’s a good one. Just because it’s like, I don’t get into details there, but I give you just like, sort of like a run through of a basic set up that’s through and thrive for most people, for most sort of average HODLers right. And like with links to, and how to complicate it further. I think that set up is like, truly is like a good, solid way of doing the basics. You’d have to be like seriously attacked to have a problem with that one. Yeah. What else? Yeah, I mean check out all the guides that we have on the docs page of Coldcard, because we link to other things we, including linked to multi-vendor multisig setups as well. And don’t be shy. There’s no stupid questions. Go ask questions. Don’t give your personal information to people or your coin information to people, but do ask, and especially on Twitter, like people will help, like people will point to good guides to go read and learn.

Stephan Livera:

Excellent. Well, thanks very much for joining me.

NVK:

Thanks for having me. It was fun to come again.

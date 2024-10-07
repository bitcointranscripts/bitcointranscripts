---
title: Bitcoin Grants, Design & Crypto Patents (COPA)
transcript_by: Stephan Livera
speakers:
  - Steve Lee
date: 2020-09-15
media: https://stephanlivera.com/download-episode/2480/211.mp3
---
podcast: https://stephanlivera.com/episode/211/

Stephan Livera:

Steve. Welcome back to the show.

Steve Lee:

Thank you so much. Glad the glad to be here,

Stephan Livera:

Steve. I see you guys have been very busy over at Cquare Crypto. Since we last spoke, you’ve been doing a lot of work in different, in different arenas as well. You’ve got the grants going, design and this crypto patent stuff. So tell us a little bit about you know, what you’ve been doing over the last few months.

Steve Lee:

Yeah, I think it’s been about a little less than eight months since we last chatted. And it’s been a bit busy, 2020 for us. We’d love to go over many of the grants we’ve given out and any questions you might have about that you think our audience might be interested in. And yeah, happy to cover the design community and the open patent Alliance as well. And we can, if there’s time at the end, we’d love to give a update on where we’re at with the lightning development kit progress too. The core team has been hard at work with on that. And I think we’ll soon, soon have some good stuff there too.

Stephan Livera:

Excellent. Well, look, let’s start with some of the grants you had. I’ve lost count of how many you’ve got a lightning signer project you’ve got. Yeah, well, let’s start with that. So what is the lightning signer project?

Steve Lee:

Yeah, I think with last time we spoke, we had two grants that we’d given out to BTCPay server and to zmnSCPxj, and I think we’re up to 15 now. It’s even hard for me to keep track. But let’s see. So yeah, we’ll start with lightning signer project. So that’s a project that a developer named dev random and Segwick (?) are working on it’s a lightning infrastructure project, which enables signing lightning transactions in lightning state updates in hardware security modules. So be that on like an iPhone or Android phone or enterprise systems, either way. What that does is it improves security for Bitcoin and for lightning by imposing policies on what are valid transactions that can be signed. And if they don’t fit sort of the organization’s policies or the wallet’s policies and also fit sort of standard lightning transactions, then they would be rejected. It’s just a way to reduce the attack surface of lightning.

Stephan Livera:

Right, so as an example, lightning, the keys have to be hot. And so what this could be kind of like a warm wallet or something like that. And the idea is that you could set up rules such that it will only sign the channel state update if it meets certain rules. And that is like a, we could think of that, like an infrastructure to help the space in terms of building and using lightning in a way that’s managing the safety and security, but also having convenience, like, managing that trade off a little bit better. Would you say?

Steve Lee:

Absolutely. That’s correct. So you can imagine a future where you’re an exchange or a merchant and you’re handling a significant amount of Bitcoin. That needs to be in a hot wallet for lightning, as you point out this sort of makes it a warm wallet. It’s still, it’s still connected, but you can significantly reduce the number of ways that a hacker or attacker could access the Bitcoin. And then on an individual level on a mobile phone, you can imagine a future in maybe perhaps three, orfour years where your iPhone or your HTC or Samsung Android phone actually has this built in to their their security mechanism and their secure enclave on the phone.

Stephan Livera:

Like the Titan chip and things.

Steve Lee:

Yep. Cause like today if you run a Bitcoin wallet on your iPhone, probably that wallet stores the private key in the secure enclave, which is step number one.

Steve Lee:

That’s great if it does that, but if your wallet actually signs a transaction, it has to read that private key into main memory. And all of a sudden the benefits, the security benefits you had of storing it in the secure enclave go away. Because if there happened to be malware zero day attack, that could access main memory, but not the secure enclave, it could then access that private key. So step two for securing on a mobile phone is being able to not only store the private key in the secure enclave, but signing Bitcoin transactions. And then the third step would be to sign lightning transactions. And it’s a very complex project. It’s you have to put a non trivial amount of the lightning network, state machine in firmware in these secure enclaves. And that’s what this project is about.

Stephan Livera:

I see. Yeah. And so as part of that, it might involve putting certain rules into the firmware so it’ll say, for example, only sign the update if you know, the money is coming in this way, or it meets certain policy rules. And that kind of is part of the lightning channel, state update aspects.

Steve Lee:

That’s right. I think their website lists like 20 examples of policies that you could implement and there’s probably even more but the way, but how you described it as exactly. Right. so this, this project it’s just, it’s obviously all these projects are free, open source software. This project is not tied to any particular lightning implementation. This, this should benefit the overall ecosystem, whether someone’s running lnd or C lightning or LDK. So we’re excited about this infrastructure project.

Stephan Livera:

Yeah. And with these grants, are they generally done on like a time basis or are they done on sort of like a we’re paying you for this result? What of what’s the way that most of the grants being done?

Steve Lee:

The way we structure the grants are time-based so many or 12 months the ones we will talk a little in a little bit about some designer grants. We’ve typically done six months for those. But there’s no particular, duration that it has to be, but they’re, time-based, there’s a lot of vetting upfront to make sure that make sure it’s sort of obvious that, you know, we believe that this is a valuable project for Bitcoin. Typically a criteria for us is that it doesn’t have an obvious business model. Cause if it has an obvious business model, then my recommendation to the applicant is to go start your own business. We want to fund high-impact valuable projects that don’t necessarily have a business model and are often under invested because of that. We look at, of course, you know, do we think that the person or team can execute on it and make it happen?

Steve Lee:

And the last criteria, which is the least obvious is that we want to make sure that they can sort of be their own boss because we, you know, I don’t manage any of the grantees, no one at square does or square crypto. So we’re going to make sure that like each morning they wake up and they’re excited about their project. Know what the next step is to make progress on it. And I’m really happy to say that, you know, putting that time and effort upfront while we evaluate grants has paid off. And I’m really happy with all of our grantees.

Stephan Livera:

While we’re on this topic of just kind of the meta or the broader aspect of grants in Bitcoin, I think, yeah, you make a great point around how we want people who can make a business out of it to do that. And I think it just tends to be that some of the more protocol level work is not so easily monetizeable and perhaps those are the things that are more suitable for a grant, but I think I’ve also, you know, reflecting some of the Bitcoin community, obviously coming from a more capitalist perspective. And some of them have expressed a bit of a concern that, Oh, is that really a sustainable way? If things are done through donations you know, everything needs to be done as a business, that kind of thing. That’s like a concern that I’ve seen as well

Steve Lee:

Yeah. I mean, I think it’s a fair concern and I mean it does merits discussion. I feel fortunate to be at square and the Square you know, gave Square Crypto a budget to do this type of investment over the last indefinitely. I mean, I’m really encouraged this year at the number of other organizations and companies that are, are now doing the same, very similar types of funding, like OKCoin and BitMex and Kraken, BTSE, just many organizations are doing the same thing. So I think the trend is positive. But yeah, having said that anytime there’s an opportunity where there is a natural business model that allows for that organization to be consistent in terms of Bitcoin principles and keeping, just staying true to Bitcoin. I think you know, following a business model makes sense, which is why. Yeah. I mean, I’m definitely a free market capitalist person, so that’s why I do encourage people to follow that route. If it makes sense. I also think there’s a chance that with some of our grants that over time after the infrastructure and the free open source software gets developed that those developers or designers could go on to build a business around it as well. And we’re perfectly comfortable with that as well.

Stephan Livera:

I see. Yeah. And I guess then it reminds me very much of something like say the red hat model. So some of these grant grantees might develop some of this technology and then be the one to go and consult out to an exchange and say, Hey, I’ll consult with you to help you set up your lightning signing module to help your security. And that could be a consulting revenue for them also.

Steve Lee:

Yeah, that’s definitely one path there’s certainly there’s potential in wallets to have like a freemium model where certain services users pay for you know, Wasabi and Samourai I think are doing that. And Electrum, I think has some kind of a paid option with a two factor. So those are just examples of what could potentially be done there. I could imagine a future with multisig custody kind of a Casa model where it’s more do it yourself than Casa, but like the fifth key or the, you know, one of your n keys could be with a third party provider in which you you’d pay for that service.

Stephan Livera:

So that’s a, those are some ideas that for people to think about as well, the whole freemium idea, it’s tricky though, in this space, because I think people have, you might think, okay, well let’s have advertising, but then does that advertising also mean some kind of tracking and is that like a concern from like a, you know, surveillance and privacy aspect, I can genuinely appreciate, it’s difficult for people to make a profitable Bitcoin business. So yeah, but let’s go back to some of the other grants that you guys have. So I see you’ve got Tankred Hase.

Stephan Livera:

Is that how you pronounce it? Hase Tankred?

Steve Lee:

Yeah, I think so. Actually don’t make me pronounce everyone’s name because I actually have, but yeah, Tankred. He’s great. He started maybe six months or so ago on his grant and what he wanted to work on really, really resonated with us in that he’s very focused on improving the user experience for mobile wallets and especially for new users, like he would love to just increase the conversion rate of people who do a first time buy on like Coinbase or CashApp or, you know name, your favorite exchange and getting them to move into a self custodial model. And certainly a big barrier today with most wallets is that the first step you have to do when you install a wallet is write down 24 words and then type them back in.

Steve Lee:

And a lot of users at that point have no idea what this is. Don’t really appreciate the importance and definitely find it to be a hassle. And I have no idea what the metrics are, but I suspect there’s a lot of people who drop off at that point and, don’t even do it. So he started a project called photon which will store the private key that’s on the phone in the cloud as a backup. So the recovery option is in the cloud and not stored you know in real life, like in a piece of paper or otherwise. And, you know your initial reaction to that might be, but security you don’t want to throw your private key in the cloud. And while that’s certainly, I think the right frame of mind, if you’re storing a substantial amount of Bitcoin, if you are a brand new user and bought like $50 or a hundred dollars of Bitcoin or if it’s your spending wallet and you have something like the amount of money you’d have in your billfold or your purse, then I think the UX security trade off of this project makes tremendous sense because there actually are a number of security measures he’s taken in the project.

Steve Lee:

The approach is to store an encrypted version of the private key in either iCloud or Google drive. So if you have, depending on if you have an iPhone or an Android phone, and then the decryption key for that is stored in a separate server, and that’s the photon server that is the software he built out, and that could be run by anyone. I think a common model would be that server would be run by whoever is the wallet provider. And what protects the photon library has a number of ways to authenticate to access your decryption key. But sort of the default is a pin code. So the User Experience is if you just use your mobile, like normal, the private keys in the phone, but let’s say you lose your phone or uninstalled the wallet, or you somehow lose access to that.

Steve Lee:

And you need to recover, you install a new version of your wallet. It asks for a pin code, you type in the pin code, which then fetches the decryption key from that server. And then that decryption key is then used to decrypt the encrypted version of the private key stored in iCloud or Google. So as a user, you’re protected by your authentication to Apple or Google, and you’re protected by that pin code. And the pin code in the server that serves up the decryption key also is rate limited so that you can only request, you know so many pin code tries per I forget if it’s per hour or per week until it throttles that.

Stephan Livera:

That reminds me a little bit of the Casa wallet model and also a little bit of Umbrel are using a similar kind of thing in terms of like having like a deterministic backup go to their central server kind of thing. But I guess this is the idea that other wallets could use that kind of approach. And the idea would be this is for a new Bitcoiner, and this is meant to be for smaller amounts of Bitcoin, obviously not for your main HODLing stash, but if you just getting started, this is kind of a way to ease you in such that you don’t have to write down the, do the dreaded 12 or 24 word, write it down and then get quizzed and tested on it when you set up your Bitcoin wallet.

Steve Lee:

That’s right. And it is very similar to Casa’s. And technically there’s a slight difference. I think Casa takes a 24 word seed, splits it into two to sets of 12 words. One set is one of the set of the 12 words is stored on Casa server. And the other 12 is in Apple or Google. I often, I don’t even know, you know, which is, which is more secure or less, but I mean, I think they’re, they’re roughly equivalent. But the big difference is that photon is structured as a library, like part of a software development kit that would allow any, any wallet to integrate it. So, you know, the future I’m looking forward to is in a few years, it would be odd to not have a wallet that’s intended for new users or spending wallet that doesn’t have this type of functionality. And actually just a few days ago, blockchain.com announced cloud backups with their wallet which is an interesting direction. I looked through, glanced at their, their UX, for them. I don’t know if they have the same, if they get really the same user experience when, because they still required to do a 12 word backup. But it is interesting to see more movement in this direction.

Stephan Livera:

Yeah. And I guess for all the flak people throw out blockchain for, you know, being late laggards in terms of things like SegWit and so on, they do still have a very high SEO and a place where let’s think of it from a Bitcoin newcomer’s perspective. If you don’t have an experienced person guiding you, you’re just going to search Bitcoin online or in the app store. And so typically some of those companies will come up first. So any movement forward from those companies should be, you know, at least that’s a good, it’s a step in the right direction.

Steve Lee:

Yeah. The last thing I’d say on the photon project is it, you know, it’s not only a library that wallets can choose to integrate, but it’s, parametized in the sense it’s as a wallet developer, you can choose different UX security options. So for example, the wallet might monitor what the balances in the wallet, and if it exceeds a certain threshold, the wallet can then warn the user, Hey, you’ve exceeded this threshold. You might want to take more security precautions and either no longer store the key in the cloud and perhaps even sweep the wallet or some other measure. And also things like the pin code, it’s a variable number of digits, so the wallet can choose, or the user could choose. And there’s other two factor options. Photon library has built in including email and phone number. In case you forget your pin or the wallet could even choose to require both a pin and an email authentication. So there’s a lot of different options that the different wallets will choose.

Stephan Livera:

Yes, We see that kind of model in terms of Bitcoin wallets. Maybe they can integrate that as a future feature or future possibility or new wallets coming down the pike in a couple of years, maybe they will start with that kind of approach as a way to ease the newcoiner in. So let’s chat a little bit about the next one. We’ve got Jon Atack. He’s doing a lot of Bitcoin core review and contribution work. Can you tell us a little bit about the process with Jon?

Steve Lee:

Absolutely. And I believe he was on your show last fall, too.

Stephan Livera:

Yes, he was.

New Speaker:

talking about what it’s like to try to get funded. And at the time you know, I think he’d been contributing to Bitcoin core for maybe six to eight months at that point and had yet to secure funding. So I’m very proud to support Jon and his work on core get a proven track record from last year. And he also has the right, just a great attitude, I think for a Bitcoin core, he spends a substantial portion of the time doing reviews because he rightly has observed just like most core contributors that reviewing PRs is the primary bottleneck on the project. And for a lot of developers, it’s not the most fun task to do, you know, I’m not sure if Jon loves doing it or doesn’t but the bottom line is he does it, you know, he sees it’s important and he does that. So he’s yeah, he’s done a great job in core and continues to do so.

Stephan Livera:

Yeah. It’s interesting that because I think there’s different culture or different motivations around why people develop and contribute. And in some cases it’s more fun to write new code than it is to actually review other people’s code and contribute in that broader sense. And I think maybe that’s part of the reason why sometimes there’s a bit of a bottleneck there in terms of getting review work done, which is actually what helps move things forward in terms of Bitcoin Core’s process.

Steve Lee:

Absolutely. And actually I’m there maybe a month or two ago, there was some discussion on Twitter about I think it was Bitcoin magazine or BTC media created was it carrot.earn or something like that? And, you know, they had a good intentions to try to incentivize developers to new developers to contribute to the core and had an incentive mechanism. But the discussion around that was something that can seem good, but actually be a burden on that project is a new contributor coming to the project, adding, creating a new PR which if you’re brand new to the project, a new PR is probably going to be relatively light weight and not, not really super substantial and it just increases the review burden. So the discussion that ensued was really healthy, I think, and a lot of people pointed out that what a new contributor to the core project could do that would be really valuable, would be reviewing PRs, adding test cases and adding documentation, things like that can be very valuable contributions. You don’t have to come up with the next wiz-bang crypto change or add a new feature. The real win and the real help to that project would be code reviews.

Stephan Livera:

Yeah. And I think that’s also a point Jon has been making himself, even on the episode he did with me, he was making that point also. So I think that’s something that for people who aren’t as familiar with open source and development that’s maybe not so well understood point, but hopefully that’s kind of, the message is coming out with that. And more people are coming around to that idea. So you’ve also got a Vasil Dimov of, I know a Vasil has been doing some Bitcoin core contributions. Can you tell us a little bit about?

Steve Lee:

Yeah, he he has a really extensive career and resume in open source development in general. And the past, I don’t know, six or 12 months he’s been contributing to Bitcoin core. He’s really focused on the peer to peer part and adding and privacy. And specifically he wants to add support for Tor v3 to Bitcoin core, and he’s been making great, great progress you know, as you know, and probably a lot of your audience knows contributing to Bitcoin core can be a lengthy exercise, especially if you’re changing consensus code or peer to peer code. So it’s really nice to see him make progress in the period of the peer to peer part. I think I saw Jon Atack tweet today that he’s running a branch of Vasil’s on with core that is running on Tor v3 now. So it’s not yet merged, it’s not yet in a release version of core, but it’s starting, you know, it’s getting closer and closer to that. And my understanding is the Tor v2 support is being deprecated as of next summer. And there actually is some some urgency to getting this change into Bitcoin core.

Stephan Livera:

Right. So the implication would be, so I think it’s like July 2021 from what I’ve heard. And so the implication might be that if we, if Tor v2 is deprecated and we don’t have Tor v3 support in Bitcoin core, then that may be more doxing in terms of the privacy for a user who wants to be able to interact with Bitcoin through Tor only they might now have to actually, I mean, there’s probably other little workarounds they could do, but it’s not going to be very practical for most people. And it would be just far simpler if they could just use Tor v3 with Bitcoin core. That’s my understanding of it. But is that in line with what your understanding is?

Steve Lee:

It is, I’m not super expert on this, but that, that is consistent with my understanding. And so we’ll see, hopefully, hopefully this work can get into the next core release. But times ticking on that, so I’m not sure it will make that release, but, but in the next either the next release or the one after that, it seems realistic that it can get in, and that’ll be a big win for core users.

Stephan Livera:

And I suppose that’s part of the difficulty with, you know, working with Bitcoin core and making, putting things in. And I mean, partly for good reason, there’s a lot of concern around security and things might have to get rebased if there’s other changes going on at the same time. And so that can be, and then getting the review done as well as we were talking about, I guess these are some of the hurdles that a core contributor might face in terms of getting a change through.

Steve Lee:

That’s right. So, yeah, so we’re the last two people we mentioned, you know, they’re both Bitcoin core contributors and we’re at Square Crypto super happy to support the Bitcoin core development. And I think what your audience will see in our grant program is that while our core team is focused on the lightning development kit, one specific project that’s focused on lightning network, our grant program is broader and it’s broader in the sense that anything that’s going to help Bitcoin, whether it be privacy, security, scaling, user experience, we’re happy to fund grants in all those different areas.

Stephan Livera:

Next one is a guy he’s actually from the Bitcoin Sydney scene. So Lloyd Fournier. So he’s doing some really cool work. Can you tell us a little bit about why square crypto supported Lloyd?

Steve Lee:

Yeah, Lloyd’s great. We’re happy to support Lloyd for many reasons. I mean, one is that I think Bitcoin really needs more applied cryptographers. And I think Lloyd would not describe himself as a cryptographer, but, he certainly, he’s certainly applying cryptography to Bitcoin. And historically most of the people doing that have been at Blockstream and Blockstream has a number of very talented people working on this and the one observation, and I’ve talked to the folks at Blockstream and Peter, for example about this, I think, well, everyone they’re working on opensource Bitcoin is very well intentioned, very talented, and I’ve seen no integrity issues. It’s still unhealthy for Bitcoin. If only one organization has everyone working on applied cryptography. So it’s really great to support Lloyd and in the case of Pieter he just left for Chaincode as well.

Steve Lee:

So it’s good for Bitcoin to see other organizations other than Blockstream supporting this type of work. I first came across Lloyd last fall when he was doing review work on Taproot. We started a taproot review that had over a hundred developers around the world who volunteered to spend seven weeks of their time reviewing taproot. And he was one of them and he really showed that he understood Taproot and cryptography at a deep level. And I think you know, gained a lot of credibility with other Bitcoiners then. Yeah. And he has a number of projects that he’s working on now that we’re happy to support.

Stephan Livera:

Yep. So as I understand, he’s working on some ideas around DLC based Oracles, so that’s Discrete logarithm contracts, and also looking at some things like alternative payment channel constructs, kind of like all possible alternatives to the lightning network.

Steve Lee:

And there, yeah. And a third,Well, so the, and there was a third project too. He has a version of libsec256k1 written in rust that, it’s not intended for production, but it’s great for experimentation. So anyone wanting to experiment with different cryptography, if you try to use the C based production version, it can be difficult to program this Rust based version of he has that I think he forked from the existing Rust one he’s just, he’s just trying to optimize for how do I make this easier for other experimenters and researchers to do quick work? And so that’s one project he’s working on. A second project, you just mentioned the discrete log contract based Oracles ultimately he’d love to be able to, support lots of different types of you know betting and different smart contracts using DLCs. So he’s doing some infrastructure work there.

Steve Lee:

I believe he helped out with a 2020 presidential election that, between Nicholas Dorier. And I think Chris Stewarts on the other side of that, but a bunch of folks are working on that. I think it’s on chain now. And I think inaudible helped with that too. The third project is, as you mentioned that a new payment general construct, some other folks wrote a paper and published it recently. It doesn’t, it’s not, it’s not really an alternative to lightning network. It’s an alternative to the update mechanism within lightning network.

Stephan Livera:

I see.

New Speaker:

And so, and it’s still early enough that Lloyd is just sort of teasing out. Does this even make sense? Is there reasonable trade offs with this approach? It’s actually an improvement over what is currently used and yeah, he’s gone to the developer email lists and gone back and forth with several developers on that. I think it’s not concluded yet. But it could actually turn out to be a clear, win and improvement over the current mechanism, even a pre eltoo. I don’t know if people have talked about eltoo before on, on your program eltoo. That’s another, you know, that’s another improvement of the update mechanism, but one that requires a Bitcoin consensus change, what Lloyd’s working on doesn’t require consensus change. So it might be a, like an intermediate term win.

Stephan Livera:

I see. Yeah. Yeah. So for listeners interested check out episode 200 with Christian Decker , we spoke a little bit more in detail about ANYPREVOUT and eltoo but as you’re saying, Steve, sometimes we have to consider the possibility that even if we didn’t get those, or if we want these as an intermediate step, well then having some of these alternative methods of achieving something similar arre worthwhile looking at.

Steve Lee:

Just to add a little bit to that. In that square crypto is clearly believers and investing in the lightning network, you know, that’s our core project. So we’re, we’re definitely believers in that. But it’s certainly not without risks number one lightning network, the tech can improve. So any kind of alternative to a portion of the lightning network infrastructure is interesting to us. And we’re also interested in completely different layer two approaches and scaling approaches as well. That are, you know, can deliver on being decentralized, good user experience, et cetera. So our grant program could go towards that as well, but so far lighting network is where we think the majority of the investment should be for layer two and scaling.

Stephan Livera:

You got Steve Myers here as well related to Richard Myers working on you know, GoTenna and lot 49 as well. So tell us a little bit about what Steve’s doing?

Steve Lee:

Yeah, right. So I actually, they’re brothers and, Richard actually introduced me to Steve and I’m really happy he did because Steve had at Disney for a long time. And I think he is, but he’s also been a long time Bitcoin or sort of as a hobbyist and on the side. And he’s really, really itching to be able to focus fully on Bitcoin. So this grant enabled him to quit his job and focus on Bitcoin. He’s working on the Bitcoin development kit, which is, it’s a project that was another leading candidate for square crypto to focus on. But we, you know, we decided to focus on lightning development kit. The Bitcoin development kit is very complimentary to that and that it is a software development kit intended to make it 10 times easier to build a Bitcoin wallet is just focused on an on chain wallet as opposed to layer two.

Steve Lee:

So it’s dealing with, how do I get block data? You know, am I getting full blocks from the peer to peer network? Am I getting compact block filters through like BIP157? Am I getting it from Electrum, there’s all these different ways you can get block data. Each has tradeoffs. And as a wallet developer, there’s really no great open source library or development kit. You can use to do that as well as do things like coin selection and key store and all the different things that a wallet has to do. So the goal with the BDK is to build out a library again, very much like LDK. But for both of those projects, the hope is that it’s free open source not tied to any company or entity highly regarded as like the Bitcoin core project and libsecp256k1 which are very trusted projects. And people generally know that they have a lot of eyeballs, a lot of people reviewing and auditing them both the LDK and BDK project, aspire to that as well. And hopefully in two or three years, if for anyone creating a new wallet, it just becomes like a no brainer decision to start with the BDK and the LDK and then customize it from there based on what your goals are with your wallet and who your users are.

Stephan Livera:

I guess one other comment that, one observation I see as well, is that there’s been more of a focus recently, at least in recent years around a move towards rust. And so I think there’s probably a theme there as well, right? Like LDK is using Rust and BDK is building on Rust Bitcoin as well. And I know there are some kind of longer term ideas around what could be done in terms of Bitcoin core with Rust as well. So do you see that as a bit of a thematic aspect there?

Steve Lee:

I do, and I happen to be of the opinion too that it’s the right decision for these libraries to build them in rust. And the, the goal with BDK is, is similar to LDK in that even though it’s being written in rust, the, the intention is to have APIs in a variety of popular languages that people are building applications and wallets in. So if you’re building an iOS or iPhone wallet and you want to use Swift, or you want to use JavaScript and like react native different technologies, you should be able to access the functionality in the BDK and in the LDK and do it through a Swift or a JavaScript API. And similar with Android, you should be able to access it through a Java or Kotlin API. And as an application developer, you shouldn’t need to know anything about Rust or touch any Rust code.

Steve Lee:

So that’s a goal that both of these projects share. It’s a lot of work and it’s not a whole lot of fun either. It’s a big part of the work that’s being done this year for the LDK. But I think it’s very crucial for adoption by developers because speaking with different wallet developers and projects, a big barrier for them to adopt another another third party open source library is that if it’s written in a language they don’t know or that they would struggle to modify and update, then that would be a concern. So I think delivering these native API is very important.

Stephan Livera:

Let’s move on. So we’ve got Chris Belcher, another well known well, he’s a well known privacy advocate and developer in the space and he’s working on CoinSwap. Can you tell us a little bit about your decision to fund Chris there?

Steve Lee:

Sure. one last quick thing about BDK that’s important to say it’s actually it’s an announcement that the, I don’t know if you you’ve covered the magical wallet before on your, on your show?

Stephan Livera:

I haven’t no.

New Speaker:

It’s another open source library. That’s been developed this past year by a developer Italian developer named Alekos. And he came from, he was at Blockstream last year, and he’s been focused on what he calls magic magical library. It also is a Bitcoin development kit library, and I’m really excited to see in the past week, Steve Myers and Alekos have been meeting up multiple times and they decided to merge their projects. They’re going to merge their efforts. And by all accounts Alkeos has done amazing work with the magical wallet library it’s already being developed on by other projects.

Steve Lee:

And they really have shared goals for their projects. And so it just, it’s wonderful to see two developers be able to come to that decision to merge projects, because to your point earlier in the show, you mentioned that oftentimes developers, want to like code up a new feature or do their own thing versus review code another dynamic, that’s very common is a developer wants to just create a new project from scratch. Cause it seems sexier or easier than to start contributing to an existing project. So I really admire Alekos and Steve to join forces and merge their projects. And I think the end result will be much stronger because of that.

Stephan Livera:

Yeah. Actually just on this while we’re on this topic. My understanding is I haven’t looked into it in a lot of detail, but as I understand the magical Bitcoin wallet, one of the ideas is it’s very like supportive of miniscript and that might have some important implications in terms of people being able to have better policy in terms of like the Bitcoin scripting. It requires them to be less advanced in terms of that, because as I understand, it helps them try to write the code in a way that’s a bit easier for them to kind of, and this is like a thing within Bitcoin core. And I know Andrew Poelstra’s big on this as well. So I suppose this would hopefully with all of that working together, then it makes it a bit easier for people who want to do some of those more advanced spending conditions, as opposed to just the typical single signature spend stuff. Right.

Steve Lee:

That’s absolutely right. Yeah. So it and I think Alekos has already made great progress on that there. And if, if any listener wants to go to Bitcoindevkit.org that’ll be the website for this project. And it’s a bit under construction right now because they’re merging the two projects, but you’ll be able to get a sense for their vision for where this has had a fantastic, yeah. So we get, we can talk about Chris Belcher now.

Stephan Livera:

Yeah, let’s do it. Let’s talk about coinswap.

New Speaker:

Well, that’s you know, Chris Belcher contributed to Bitcoin for many years and has done a lot of great work for privacy. We’re thrilled to be able to support him and human rights foundation also supports him with the grant as well and the project.

Steve Lee:

And just like, I think he’s done with, you know, on Joinmarket. He is excited about growing active contributor base for Coinswap. So it’s just more than himself. But I’m excited about the Coinswap project, because I think it’s one of, it’s an ambitious project. But it’s one that you know, so far from certain that it’s gonna work out and work, but if it does work, it could really move the needle on privacy because of the way that it works in terms of sybil resistance. I think it’s novel in its approach and just the kind of footprint it leaves on chain is distinct and different than other approaches to mixing coins and doing Coinswaps.

Stephan Livera:

Yes.So that’ll be really exciting to see obviously it’s still early days with Coinswap, but with some more work, maybe we’ll see that come to fruition and then maybe we’ll see it used more in a day to day spend case. And maybe it becomes a little bit more like a PayJoin sort of thing, where it’s more of a common thing that people will use Coinswaps to pay for things.

Steve Lee:

Exactly. And you just said it, but it is early days. You know, there’s still back and forth on the developer list about analyzing different attacks on this. And you know, I’m optimistic, but we’ll see. We have to sort of nail the design then of course implement it and in terms to implement it and then launch it. And there needs to be a good user experience around it. And maybe, maybe it is kind of like a PayJoin or just naturally works into the wallet. So it’s really easy for users to use, which would be great. Another thing that is needed for it to succeed is that there needs to be liquidity for this and this actually, if successful, it could be really amazing. One aspect of Bitcoin holders that provide liquidity is that there would be a way to earn interest on your Bitcoin while you retain your private keys.

Steve Lee:

So your Bitcoin can be in, your self custody in your hardware wallet or what have you and your earning interest on that Bitcoin, which is a really amazing aspect. I think the sacrifice of the cost you’re making to do that is that you time lock your Bitcoin for a period of time, such as say, six months. So that’s the reason you’re getting paid interest on it. So you do bear a cost, but if you’re a HODler, you don’t really care, you likely don’t care about having to lock your Bitcoin up for, or at least some portion of your Bitcoin for six months. And so huge security win and in counterparty risk, when by being able to retain your, your private keys.

Stephan Livera:

I see. Yeah. So it kind of, it’s reminiscent also of Chris Belches JoinMarket, which is where using the maker taker model. Now this is slightly different because the keys are hot but that is another potential way for people to earn a small amount of Sats by contributing their Bitcoins as CoinJoin liquidity for other people who want to be takers in that model who want to use that to get some privacy. So that’s probably a little bit of a interesting parallel there with CoinSwap.

Steve Lee:

Yeah. And I think the main difference is just, yeah, being able to keep it in cold storage and still earn interest is pretty cool if that all works out. You know, even if you make like 50 basis points or something, if it is relatively good user experience and easy to use, and you truly, if truly the only risk or cost you’re taking is that you lock up your Bitcoin for a period of time, like six months then that’s a pretty attractive deal.

Stephan Livera:

The big win really will also be around breaking some of those privacy heuristics, right? The obvious one is to comment, input and ownership, heuristic, and so on. So if these heuristics can be broken with sufficient use of these privacy techniques, things like PayJoin and things like potentially CoinSwap then maybe that will improve the overall story around Bitcoin’s privacy and kind of make it a bit more of a more, more like that fungible money that that we would like to see it become.

New Speaker:

Yep.

Stephan Livera:

Okay. So let’s move on. So I know square crypto has the focus on lightning, Sergi Delgado is working on eye of Satoshi. So how did the support for this project come up?

Steve Lee:

Yeah, it’s similar to the lightning signer project and Eye of Satoshi is a, it’s a lightning infrastructure project that you know, isn’t tied to any particular lightning implementation, so it can work with in fact, I think it does work with like C-lightning and can work with any of the lightning implementations. And it’s an important part of lightning becoming successful. I think for lightning to be used by mobile phones it currently looks like what third-party watchtowers are going to be, or I shouldn’t say third party, but really a Watchtower, whether you’re running it from your, like your home server or it’s a third party, but watchtowers are an important part of the security model. And if you dive into watchtowers, there’s some pretty, you know, pretty significant trade offs you can make between privacy and security and how much it might cost in a bunch of other parameters. So I think it’s important to have number one, a free open source version that anyone can use. And number two, to have a healthy market of different watchtowers that are running that make those different trade offs, so that users have good choices.

Stephan Livera:

Sergi’s done some interesting work around comparing the different Watchtower types as well. So I think he was comparing, say like the lnd lightning labs version of watchtowers versus you know, the other ones that are out there and he’s trying to move the ball forward in terms of making watchtowers more feasible and put them into practice. I think.

Steve Lee:

That’s right. He gave a really good presentation at Advancing Bitcoin in London last, I think it was February that reviewed that. Yeah. So we’re really happy to support that, that project too. And his work on Eye of Satoshi.

Stephan Livera:

Fantastic.So let’s talk a little bit about designs. This also been a focus of square crypto. So can you tell us a little bit about why you’re focusing on this and what are some of the projects that you are advancing in this area?

Steve Lee:

Yeah. From the beginning of Square Crypto, we felt that design is, is very important and that it’s also very underfunded and, and mostly nonexistent in open source. A lot of the design that we do see in Bitcoin comes from companies, but very little in open source. And so a year ago, we announced that we were seeking a full time designer to join the square crypto team to sort of lead the charge on this and over the ensuing nine months or so, we talked to around 70 different designers from around the world. None of them we hired for that job. And it wasn’t because we didn’t meet amazing people. We met many, many amazing people, very talented, just none of them checked all the boxes we were looking for. So we took a step back last April or May, and asked ourselves, is there another way to approach this?

Steve Lee:

And what we realized is that we’ve met dozens of talented people who are principled Bitcoiners, who want to contribute to open source Bitcoin. Each has their own set of talents. And the combination of those folks can lead to a very powerful design community and powerful way to improve Bitcoin design. So we went ahead and just announced, announced a Bitcoin design community and brought these folks together. And we spoke individually with 20 or so people that we had previously met, they all loved the idea. And once we announced it that community grew very quickly. It’s 600 people now that are part of the Bitcoin design Slack, and the vast majority of which are creatives. You know, whether they be user experience researchers or designers, or artists or copywriters just creative people, you know, different type of person than the developers that are so prominent in Bitcoin.

Steve Lee:

So it’s really great to see that another observation is that I think the reason why we had 600 people join so quickly is that we just identified there’s pent up demand to create a community for many, many, many years, the designers that had an interest in Bitcoin, but they feel like they’re off in their own little Island. They had no place to go. And now, now they have a community that they can, that they can go to. And you know, it’s not just the Slack, but the designers on there are creating, you know, they’re doing whiteboard session, remote whiteboard sessions and video calls to do design reviews. Every few weeks, we do a community call and have 30, 35 people show up to talk about the design community. And it’s just a really healthy, active community that I’m excited about.

Stephan Livera:

What are the ways in which that design community might influence Bitcoin development or Bitcoin application. Maybe it’s more like application development.?

Steve Lee:

Yep. I think A couple, couple of different ways. One is that the main work product that we want to create as a community, as a Bitcoin design guide, which will have many different aspects to it. Three obvious sections of this design guide would be onboarding private key management and payments. And, but, you know, we have an outline for what this could, could look like. And we’re envisioning those are three examples sections. And we have, Square Crypto has given out grants to designers to focus on those sections. Not that they’re going to be the only person contributing to it, but just to get it going right now, we’re at a point with this design community where we just need to start producing some content to get it out there and then iterate on it. So that’s the current state of things. So the Bitcoin design guide is one, one piece of this.

Steve Lee:

Another way that we’re already seeing designers contribute is actually go contribute to existing projects. So there’s some energy around helping the Bitcoin core project with the GUI wallet. And so there’s a few designers who are working on that. They’re collaborating with some of the developers on Bitcoin core to make those improvements. That’s nice to see. There’s one of the designers is working with a multisig open source project to improve its user experience. So I think there can be a lot of just by we can help each other guide and provide sort of yeah, just provide a guide to designers about here’s how you can contribute to an open source project, because it’s not very common to do that. And if we can create those bridges and get designers, helping different open source projects, it’ll not only improve those individual projects, but the learnings from that can be fed back into the Bitcoin design Guide.

Stephan Livera:

Excellent. I liked the idea about focusing on existing well-known wallets, whether they are, you know, Bitcoin core, or maybe like Electrum, or some of these other projects that are already out there and existing, they could do with some design expertise. And so you’ve got a few people who you’ve given some grants to go, Jamal, is it Jamaal Montasser and a Project Horizon? So what’s Project Horizon?

Steve Lee:

Yeah. So I’m really excited about Jamal’s project because it’s the first user experience, a research grant that we’ve given out. So we’re sort of green at this. We’re going to learn but we do value user experience research, and he’s going to take look at Bitcoin core and full node users, as well as people who don’t use it and to understand why they don’t use it. And just to explore a bunch of questions that we have around a full node and Bitcoin core usage. And we’ve reached out and spoken to several, several long time Bitcoin core developers to get their input into this process. And the hope with the final result of this is to gain some insights that can just provide some direction and guidance for future development on the existing Bitcoin core wallet. As well as any, any future wallets that might want to have a full node aspect of their wallet should be able to derive insights from this research project.

Stephan Livera:

Yeah, that’s a tough one because it’s like people get turned off by having to let’s say still, or was it 320 gig gigs or what, roughly that amount that the Bitcoin blockchain is now, and there might be people who, you know they don’t necessarily have an always on computer. So I guess these are some of the difficulties that people have to try and design for.

Steve Lee:

Yeah. I just like to get some data and better understand what’s people’s awareness, even of Bitcoin core and a full node. Like, you know, how many people, it can be easy to get caught up into Bitcoin Twitter, and think that everyone knows about this stuff, but it’s quite reasonable that a large percentage of people buying on CashApp and going based have never even heard of Bitcoin Gore, and don’t even know about it, don’t even know about the benefits of running your own full node. And, you know, so if we have some data that suggests that that would be good to know, because it can suggest where we can spend more time on whether it’s coding or design or marketing or awareness, et cetera. For those that are aware of Bitcoin core yeah. Understanding the pain points, like did they give up because of the long initial sync or the resource requirements. Or did they give up because it sounds intimidating? I actually think there might be a large population of people that have heard of it Bitcoin core, and they don’t even try to use it because they’re intimidated and they might, you know, if they actually tried to download it and run it, they might find that it’s not, not as hard as they might’ve thought. So there’s all these open questions and hopefully this project can provide some data as well as a qualitative you know, research to just getting, understanding, you know, getting quotes from users and sort of understand the emotional aspect of using it too.

Stephan Livera:

Excellent. I think that makes a lot of sense and I think you’d make a really good point around the intimidation point. And yeah, I guess it kind of comes to if someone’s a casual Bitcoiner versus the hardcore Bitcoiner, but let’s talk a little bit about some of your other design grant recipients. So you’ve got Christoph Ono.

Steve Lee:

Yeah. So Christoph Ono, great. He’s doing a number of things first and foremost, he is doing a really great job at helping the design community get organized. And as you can imagine, a newly announced community that has 600 people sign up right away and start enjoying Slack. It was pretty chaotic at the start. And, and now a lot of that initial chaos has died down, but you still have, you know, dozens of active people that are contributing and hundreds who are interested in staying, staying on top of things and knowing what’s going on, and it needs some organization need some leadership, but this is a decentralized community. And we, I really try to emphasize that. And I’ve been really happy so far with the rest of the community, recognizing that this is Bitcoin design and it’s decentralized, you know, I’m not, even though I kickstarted this and Square Crypto kickstarted, it w you know, this is not a Square Crypto or Steve thing.

Steve Lee:

So Christoph has really helped shoulder, a lot of the load of organizing and what I call decentralized leadership in the community. He’s also contributing to one section of the Bitcoin design guide, which is the getting started section. And that’s getting started for designers because there’s a lot of designers that are going to be new to Bitcoin and new to open source. And so that part of the guide is just to help them bring them up to speed so that they can utilize their talents on open source between design and the third area that Christoph contributing is he wants to contribute to it directly to an open source product. And he’s interested in multisig. So he’s looking at that.

Stephan Livera:

Yeah, There’s a lot of contributions and a lot of people you’ve been supporting as well. And it sounds really interesting to see the different directions and ways that you contribute in this kind of crazy open source, decentralized way, with no top down leader, it’s just kind of people form a project and then see whoever else wants to join. And then but I guess the downside could also be, there might be a lot of duplicated or quote unquote wasted effort. And it’s about how do you efficiently leverage things that are already out there as opposed to creating the wheel over and over.

Steve Lee:

Yeah. Although I think that can be addressed fairly easily, in a decentralized way. I mean, certainly from like Square Crypto investments, like where we place our funding, we’re, you know, we wouldn’t want to create a duplicate projects.

Stephan Livera:

And of course.

New Speaker:

I mean, that’s sort of obvious, but even if it’s, you know, anytime I see a duplicate effort in the space, I’ll reach out and just chat with folks and just mentioning it, you know, just you know, presenting the option to them that, Hey, maybe you can join forces, or maybe you should chat with so, and so they’re working on something similar. And what I’ve seen is just like super everyone’s, like positive and welcoming around that. And yeah, people chat with each other. So I think, I think generally people have the right intentions. It’s typically just the lack of awareness of what other folks are working on. So you know, that’s why I sort of that’s a role I like to play and I’d love, you know, I’d love to see other people, and there are several other people in Bitcoin who play a similar role, which is really just sort of like decentralized coordinator almost for different different efforts.

Stephan Livera:

Yeah. That’s a cool idea.Yes. And you’ve got a few other people with design grant as well. We should chat about some of them. So I’ve seen an interesting one Thor Bjorn Konig working on like visual, verbal and musical ways to memorize seats. That’s certainly very different.

Steve Lee:

Yeah. This is this project is definitely a bit out there and risky, but I think it’s super interesting. I mean, I think we can all agree that private key management is both super critical to Bitcoin’s success and really hard to do in a secure way where you don’t have your keys stolen or lost. And I think most of the investments so far improving that has been from a cryptographer perspective, which has obviously a very important perspective to improve things, but there’s been much less innovation and research around things like Thor is focusing on which is, are, are there other means to memorize a portion or all of your private key? And so he’s exploring like music in three D shapes and all kinds of different things, which sound a bit crazy and certainly some people’s initial instincts and concerns which, I’d like to address.

Steve Lee:

Number one, I don’t think Thor or myself would be an advocate for a Brain wallet only approach to your private keys. If you only start, you’re breaking your head, you are at risk of forgetting it or having or permanently forgetting your private key and then you’d lose your Bitcoin. So that’s not the intention here, and I’ve heard other, other comments on this. Like, you might sing your private key in your sleep or something, which is pretty funny. And, but I mean, funny, but also, you know, like that would not be a great way to lose your Bitcoin, right? So there are ways to use what comes from his project, not for your full private key, but maybe just a portion of your private key. Maybe you’re using BIP 39 plus a passphrase.

Steve Lee:

So maybe this helps you remember your passphrase or maybe you’re using 24 words, and this helps you memorize half of that. And it could be just used in conjunction with your overall self custody strategy. And I think could be interesting. Another idea I’ve heard is that in a multisig or Shamir secret sharing setting where multiple people or multiple keys are involved, you know, this, especially in the case of like a Shamir secret sharing where you might have family members participating, you might have some family members that are stronger, you know, their brain is just wired to be stronger visual or tonal and maybe that’s how they memorized their portion of the secret.

Stephan Livera:

Suddenly early days for that kind of thing as well. Because it’s kind of like, there’s a lot of different yeah. Like the standards around how it would work with that. I guess aren’t as clear or set out, but I mean, that could certainly evolve over time. Are there any other design grantees you wanted to highlight?

Steve Lee:

Yeah, that’s really cool. So Daniel Nordh he used to be a design manager, Coinbase and left last fall. He was instrumental in helping us get the design community off the ground, so they hats off to him. And he’s a grantee as well. And he, where he’s focuses the time now for the design community is around the private key management section for the design guide, which is arguably the most important section. So he focused on that. And then the last grant that we’ve given out for designers is for Johns Beharry and he is focused on the payment section of the design guide. And there’s already several different payments protocol into coin for, you know, layer two and on chain. And you throw in coin joining the PayJoin. And it’s a bit, you know, it’s both been designed by developers and independently designed by different groups. So he’s going to try to bring, you know, be able to summarize where we’re at and deliver best practices for what we have, and then also focus on what are future potential protocols or merging of some of these protocols for best practices for developers and designers?

Stephan Livera:

Yeah, that’s an interesting one as well, because it could be confusing to someone who’s not deeply into this space about, Oh, is that a Bitcoin address or is this a lightning invoice? And is there a PayJoin inside the QR? And does that, you know, can my wallet read that correctly? And, you know, even, even today with BTC Pay server sometimes some newer users get a little confused because they don’t know that you can flip between Bitcoin or lightning at the top. And so that can also be a bit confusing for them also. So I guess some of these are efforts around how to streamline these as well. Right.

Steve Lee:

That’s exactly right. Yeah, so we’ve given out five designer grants. They’ll probably be a few more this fall and we welcome other companies to see the value in supporting open source design and to do funding as well. So it’s not just from Square Crypto. I think it will become more and more evident once we have a design guide for people to see. And then ultimately, again, what I’m imagining in a couple of years is that there’s going to be the LDK the BDK and this design guide. And those three will probably be merged into one package. And if you are wanting to create a new wallet or application, you just download this package and it helps your whole team, both the design team and the developer team to build a new Bitcoin application much more rapidly. Instead of doing everything from scratch, you’re just focused on what you want to optimize for. And it goes from like a year long project to get a v1 out to being like in a weekend, you could have something, you know, out there ready for feedback and testing from users.

Stephan Livera:

A cool vision to be building towards. Also while we’ve got you here, Steve, we’ve got a chat about the new Square Crypto Patents or COPA. So can you just give us an overview? What is COPA?

Steve Lee:

Yeah, so really excited to see this introduced it’s an open patent Alliance and the intention is to create a defensive patent shield for developers open source projects or companies in the space to help protect them and protect the foundational cryptocurrency technologies that everyone’s building upon. There’s what the situation we want to avoid is where technology goes into open source software. Let’s say like the Bitcoin core or the sorry, the Bitcoin consensus protocol or lightning protocol. And then in the future have a patent troll or patent aggressor assert their patents against that. And I think it’s one reaction from Bitcoiners is like, well, too bad. Bitcoin’s decentralized. Who are you going to sue? However, you know, companies can be sued and while Bitcoin will survive without this company or that company, or even all companies, it certainly would decelerate the adoption of Bitcoin. I mean I’m certainly believer that, that healthy, productive companies in the space of have improved the user experience and have accelerated the adoption of Bitcoin. So it would be bad for Bitcoin to have that disrupted and to whatever extent there’s risk in even individual developers being sued which would be highly unfortunate. This could provide protection for those developers as well.

Stephan Livera:

And some of the feedback I saw why Crypto and not Bitcoin?

Steve Lee:

Yeah. Which we, you know, I love that feedback because one thing I love about the Bitcoin community is, is keeping you on your toes. I think that’s an important attribute of the Bitcoin community and what helps strengthen Bitcoin. So I welcome that feedback. Rest assured myself and square crypto, we are still very focused on, on Bitcoin. So the answer to why crypto and, you know, why is it COPA and not BOBA or, you know, Bitcoin Open Baton Alliance? Well, it’s because even if you’re only interested in Bitcoin that still doesn’t mean that a, another, another project, or like, or like a patent aggressor who has patents that are outside Bitcoin, can’t sue you, or can’t sue, you know, a company that’s doing Bitcoin. So COPA would absolutely welcome any member including you know, non Bitcoin cryptocurrency projects or companies that support different coins or multiple coins.COPA even welcomed bad actors. Like if you, even if you’ve been a patent aggressor in the past, you’re welcome to join Copa because guess what, then you can’t be a patent aggressor. So COPA is very open, open and welcoming to to anyone that’s, you know, within the scope of the foundational cryptocurrency technologies. And yeah, that’s why it’s scoped at crypto and in cryptocurrencies and not, not just Bitcoin.

Stephan Livera:

I see. And what are the requirements to join?

Steve Lee:

There really are none like in the sense, like I said, you know, it’s, you don’t have to be a corporation. You don’t have to have a certain amount of employees, or revenue. It, you can be a small company, you can be a startup, you can be an open source project. You can be an individua it’s open to anyone. And the two main aspects of COPA number one is a patent pledge. So if you join any patents that you have that fall within the scope of COPA, which are foundational cryptocurrency patents, you pledge that you will not use them and sort of in an offensive way, you know, you would not assert those against anyone else unless it’s for defensive reasons. And another feedback I’ve heard is it, Oh we don’t have any patents, so we’re probably not welcome.

Steve Lee:

That’s actually not, not the case at all. You can have no patents and you can still join. You can have an internal organizational philosophy of, we’ll never have a patent. You’re still welcome to join and reap the benefits of this, of the organization and that you can use the patent shield, which has everyone’s patents that joins is collectively used. You get that benefit. So you don’t need any patents. You can hate patents, you can hate the patent system which a lot of people do including myself. And COPA can make a lot of sense because we, even, if you hate the patent system, you still have to deal with reality. And, and I think COPA is the next best thing to having no patent system at all.

Stephan Livera:

Yeah. I mean, I’m certainly in a similar camp, I come from the Stephan Kinsella point of view of being anti intellectual property, but I can still see some value in COPA for that reason. As you said, defensive reasons, maybe we should talk about defensive reasons. What is classified as a defensive reason?

Steve Lee:

The most obvious is that you’re sued. You know you’re sued and the claim is that you’re using certain IP that another, another entity owns. And then you can use your, your own patents that you’ve pledged to COPA, as well as all other patents that have been pledged to COPA all of those, you know, I refer to it as a defensive patent shield. All of those can be used in defense of being sued. There’s so I think that one’s fairly straightforward and obvious. There’s also a carve out for copy cat usage and that would be like, if someone wholesale copies like your UI of your product then you could use it to defend against that. So there’s a couple of inaudible-outs like that.

Steve Lee:

I would recommend anyone interested in COPA definitely read the membership agreement, which is on the website, open-patent.org. Read through that, to understand the agreement. It is fairly complicated because it’s, a challenge. And the lawyers and the team at square that put this together had a huge challenge. And I think they’ve struck the right balance because you need to make it attractive enough that entities with patents will join. But also it needs to be it needs to uphold the whole intention and purpose of COPA, which is this patent pledge and created creating a defensive patent shield. So I think the right balance has been struck. Having said that, you know, we’re very welcomed to, to feedback this, this is just to emphasize, this is not like a, it’s not a square centric initiative, COPA is a separate entity, the nonprofit entity it’s intended to be, you know, independent and fair for all the Bitcoin and cryptocurrency companies and projects.

Steve Lee:

So we want to get this right. So if people see ways to improve the membership agreement, we’re happy to, you know, we’re listening and we’re happy to modify that if it makes sense.

Stephan Livera:

And have you had any companies and members join? I think I saw some chatter about Blockstream potentially joining.

Steve Lee:

Yeah. So Blockstream publicly said that they’re going to join which is fantastic. And it’s it’s also not surprising. I mean, Blockstream has a long history in doing similar things. In fact, I think four years ago, they, they had announced their own patent pool and defense defensive patent pool, which like EFF wrote about. And so this is very aligned, I think, with their philosophy and vision. So we’re very happy to have Blockstream planning to join COPA. I’m also really happy several not so many major companies in cryptocurrency have already responded and reached out expressing interest.

Steve Lee:

They haven’t committed yet, so I don’t want to share their names, but it’s very encouraging. So I think, I think there’s, there’s a good chance that we will see a lot of you know, major cryptocurrency companies join and for startups to, you know, every company, every organization will need to evaluate this on their, you know for them different makes sense for them. But I think at a startup, it really can be beneficial because you are kind of a sitting duck as a small startup that does not have a of resources because a patent troll one strategy for a patent roles is you don’t start with the five or the 800 pound gorilla. You start with small, the smaller folks who can’t defend themselves and you rack up legal win after legal win, and it helps build your case so that then you can go after the larger organizations with more money. And so I just, I sort of fear for startups that they’re sitting duck. So I think COPA can make a lot of sense for a startup as well. And then I’ll be interested to see reaction from open source projects and developers as well whether they find this compelling and compelling enough to join.

Stephan Livera:

And also it’s an interesting world with all the patents, and it’s almost like you need a war chest and so some of the big companies like Apple and Google and Samsung obviously are big enough, they’ve got their own war chest. And so anyone who wants to go to war, they kind of have the funding and their own patients to kind of use in defense, where I think to the point you were making it’s that it can make it difficult for an upstart or a small competitor to try and compete in that world, because well arguably, there’s been kind of a centralization that has been driven by intellectual property laws. And so this is potentially one way that the industry can allow for the creation of newer projects and actually permit more innovation.

Steve Lee:

Yeah. And that’s actually a big, that’s a big reason. I’m not a fan of the patent system. I saw firsthand up close at Google, how this works. So Google of course, once was a startup and Google had a philosophy of, you know, of not being a patent aggressor and not even really caring about filing patents like let’s just build great products and great software and deliver that to users and build a business. And that was Google’s focus, which is great. And I feel like that mindset, is, you know, the mindset of many people in crypto companies and working on open source software as well. But then comes a day when your company is making enough money, that it becomes a target for patent aggressors and patent roles and, or, or other just aggressive companies. And then all of a sudden you realize, Oh, I need this war chest.

Steve Lee:

And so you start doing things like buying Motorola for billions of dollars and creating an internal machine to create patents. And you know, I was part of that machine at Google. I think I had something like 25 or 30 patents in my name at Google. And it’s just, it was all part of this machine. They create a very efficient machine driven by lawyers that makes it very, not requiring much time by engineers and product managers to create patents that are organization. And it allows a large organization to create hundreds and thousands of patents in their war chest. Even if that corporation didn’t even want to do that, they’re sort of just the way the dynamics work out. They’re forced to do that. Yeah. Then they have this war chest, and all of a sudden the patent system is no longer really protecting the little guy or, you know the lone inventor who doesn’t want to be squashed by big companies. The patent system is really not helping that person.

Stephan Livera:

Just to make it real for listeners. Do you know of any example patents or technology that would go inside COPA?

Steve Lee:

Yeah. So Square has already committed to transferring and pledging all of its crypto patents to COPA. There’s seven to 10 or so that have been identified just, just to give a feel for how many and one that your listeners might be aware of, just because it made the news back in January of this year CoinDesk, and a lot of other organizations talked about this patent, but, you know the CoinDesk headline is Jack Dorsey’s Square Crpto Patent for Fiat to crypto payments network. And that made that made a big splash. And even at that time, some people were fans of that square one that and other people in Bitcoin community were concerned because here’s a, you know, large company that has potentially a very crucial patent. And what kind of nefarious things cause square do with that? Well, I’m happy to say that Square’s going to transfer that Patent to COPA so that anyone that joins COPA has access to that patent for defensive purposes and by square transferring it to COPA, it means that square will never assert that patent against any, anyone, even, even nonmembers of COPA.

Stephan Livera:

Yeah. That’s great to see. And I think that’s probably a really great example for the listeners who might’ve had a concern when they saw that news earlier in the year, just with COPA in terms of sustainability, how does COPA sustain itself into that future?

Steve Lee:

Yeah, so it, it will, the first year, I think square is planning to, like fund any kind of operational costs. After that it would be membership fees. And I think what square said publicly right now is just TBD, but I think there’s a desire at square to state those fees sooner, sooner than later. I can certainly say that the goal here is not to, to rent, seek on COPA. Like square and COPA do not want to maximize revenue from membership fees. The desire is to keep it as lean and mean as, as possible. And you know it is classified as a nonprofit organization. The governance of it will be a board of directors of nine people and a mix of independent board directors and people from member companies. Yeah, so that as far I don’t expect operational costs to be that much maybe like one full time person on an ongoing basis who would be probably an IP attorney, but also someone who’s just helps with all the operational aspects of COPA.

Stephan Livera:

Excellent and let’s also chat a little bit about what the team is doing on LDK. Do you have any updates for us?

New Speaker:

Yeah, I can give a quick update. So yeah, in January we announced that the core team at square crypto would focus on lightning development kit. The progress to date I mentioned earlier in the program, the creating API’s and different programming languages to make it to lower the barriers for developers to use LDK. That has been a major thrust this year. Inaudible and Matt in particular have done a lot of work to make it so that Swift and JavaScript and Java can be used with LDK that’s one aspect. Another is just a lot of what developers call re-factors. It really just taking the LDK is the engine. The LDK is the Rust lightning project that Matt Corallo started a couple of years ago.

Steve Lee:

But, you know, I think he started that project as sort of a hobby project that where he wanted to learn lightning and he wanted to learn rust and his original intention with that project was not to turn it into this production, quality, robust piece of software. And so another major thrust this year from the team is turning into that. And that includes redoing a lot of the code internally, as well as redoing some of the API is, and the touch points where other developers who are the users of LDK would use use LDK. And we’ve received a lot of feedback too, from prospective LDK users that have helped guide us into what the API should look like. So that’s, that’s the two primary areas that we’ve done development. There’s also been a little bit of feature catch up.

Steve Lee:

So LDK now is pretty much fully compliant with the lightning specification, just like the other lightning implementations. Our goal is by this fall. So in a few months to have an LDK website where a developer can just download the LDK and there’s example application that you can build and run, and you have a lightning node up and running with LDK and you don’t have to write a line of code. And then from there is where a developer could start customizing. For example, you might want to integrate LDK into your existing Bitcoin wallet to add lightning functionality. Like the Electrum project would be an example. They ended up having to write their own lightning implementation, but if somehow magically the LDK existed two years ago, when they made that decision, they could have just downloaded the LDK, plugged it into Electrum and use that to add lightning capabilities. So hopefully starting this fall, we’ll start to see more projects begin to experiment and tinker with LDK.

Stephan Livera:

Yeah. It’s an interesting one there with Electrum and from my episode chatting with, I actually brought that up with the Electrum guys and I think in their minds, they were more interested in the idea of having their own partly because they wanted to have it all in Python and perhaps they wanted a little bit more control over it for themselves, but potentially maybe, you know, it kind of missed the boat with Electrum, but perhaps in other wallet cases, they may be interested to try using LDK and maybe there’s some other wallets out there that are currently only Bitcoin on chain, and they would like to have a lightning component as well. So maybe those are potential candidates for further use.

Steve Lee:

Absolutely. I mean we have a list of over 30 wallets that are interested in using LDK. So I think that there’s ample evidence that there is demand. LDK just needs to mature to a point where it’s realistic for those projects to integrate it. But we’re very optimistic that the software will get used and also ultimately just, you know, make it way easier to build a wallet and build a great, great user experience.

Stephan Livera:

I guess just turning more broadly with Bitcoin lightning. What are you excited about for Steve?

Steve Lee:

I mean, at the highest level adoption, you know, just more, more adoption of Bitcoin and that comes in, that comes in stages. Obviously a predominant use case today is just HODLing and the speculative investment. But you know, we’re already, I think we’re already seeing it mature to being a little less speculative and a little bit more confidence that this is gonna be a very sound investment. But as you can see from where square crypto is investing, we’re trying to make Bitcoin more than just an investment. So we’re, we really look forward to seeing Bitcoin be used as money and that’s maybe a 10 year long marathon roadmap, but yeah we’re just excited to see each year of progress and improvement towards that 10 year vision.

Stephan Livera:

Excellent. Steve, for any listeners who would like to follow you online or find out more, where can they find you?

Steve Lee:

Twitter is probably the best place I’m my handle there is @moneyball. And my DMS are open. So feel free to reach out and say hi.

Stephan Livera:

Well, really enjoy chatting. Thank you for joining me.

Steve Lee:

Awesome. Thanks for having me. It’s been great.

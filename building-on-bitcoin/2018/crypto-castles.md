---
title: Building your own bank or... Constructing Crypto Castles
transcript_by: Bryan Bishop
tags:
  - security
speakers:
  - Jameson Lopp
date: 2018-07-04
media: https://www.youtube.com/watch?v=gXDR4tjaGQc
---
<https://twitter.com/kanzure/status/1014483571946508288>

I am going to do a brain dump of basically anything that people who are building systems protecting private keys are thinking about. Hopefully you can ingest this for when you decide to build one of these systems.

If you have been in this space for long at all, you should be well aware that there are risks for trusting third-parties. Various entities are trying to centralize aspects of this system. The next problem once we have successfully pushed back against trusted third-parties is that we should recognize users securing their own keys costs time and money and users are not security experts.

As a result, we have many types of losses. Chainalysis is estimating around 4 million BTC has been lost and at least 2 million BTC has been stolen. That's looking at well-known  publicized hacks. There's no way to keep track of all the individuals that have lost money.

For much of human history, we have seen this structure of our society evolve in a way where we're using specialists. We're outsourcing a lot of pieces of our lives to specialists because it allows us to be more efficient. The problem here is that we're generally coming to trust these third-parties. A lot of users are not so keen on their digital and physical security, and as a consequence, they are trusting their bitcoin to third parties.

I think people are not keeping self-defense on top of mind because they think they are not a target.. and they might be correct, but you can be not a target for all your life and then unexpectedly very quickly become a target. We see from having these systems like creating liquid bearer assets, the attackers tend to have different profiles than we have seen in previous real-world situations. Attackers are seeing this as a juicy situation because they can get away with it and it's less likely for them to be caught. If many people are failing to secure their assets, then in a herd immunity sense, I think that there will be more attackers. I am looking at the physical evolution of physical attacks and it seems to be accelerating. We need to dis-incentive these types of attacks.

If you are building these systems, then you need to worry about physical theft, digital theft, physical disaster, social engineering, collusion. Most users are going to put minimal effort into securing their own assets .We need to be proactive about helping users. Physical theft is a pretty well known problem that hmans have been dealing with. Digital theft is pretty easy to fix-- take it off the internet. We have hardware devices that help that. Physical disaster is an IT problem, but most people are terrible at doing good IT, so we need to help people do redundant storage. The bigger problem long-term is going to be social engineering and that's where education is going to have to come in. Users are going to have to understand they are constantly under threat of being hacked not just on their computers but their brains. Collusion is also vulnerable to trusted third-parties.

When we talk about keys and holding them, there's a lot of ways to do this. If the user has the key, there might be malware, weak passwords, coercion-- we heard about the $5 wrench attacks... Death of owner and end-of-life is something that people don't think about. There was a book recently out about this. There's also data loss, like due to bad IT practices. Forgotten passwords is another kind of data loss. Phishing and brain hacking is always going to be a problem.

Even at custodial services, they can be vulnerable to malware, and they are a honeypots where hackers can focus on one door to get a lot of money. Insider threat-- a trust issue again. They might be fractional reserves, you just don't know what's going on if you can't audit it.... government seizure is a possibility, confisication by the service is pretty big and it happens at a lot of AML/KYC places where accounts get seized. Phishing can also happen on the enterprise service-side. At Bitgo, we saw some of the most sophisticated spearphishing attacks against our own employees-- it's mainly because you have created such a juicy honeypot.

If you use a 2-of-2 multisig situation, you can get rid of some of the weaknesses. However, there are still things we haven't fixed, mostly around data loss. That's because of a lack of redundancy. If either one of these parties screws up, then you could lose access to the assets. I think the next logical step is that you can get the user the keys-- they just use the third-party as a service provider or facilitator, like in a 2-of-3 or 3-of-5 situation... and the facilitators can help with recovery and fractinoal reserve scenarios. The user can audit what's going on, because the wallets are segregated. Fundamentally, while we can't solve all the problems, we bring down the risk quite a bit. The main remaining risk is phishing, on all the sides.

We want to get rid of third parties, and attackers. I want to push for users being their own worst enemy in these systems. A principle we had at Bitgo is that it's preferable for the user to get temporarily locked out rather than for an attacker to get in even momentarily. I think we shoud flip it-- I have seen far more users lose access due to negliglence then I have seen them lose access due to an attacker stealing money from them. Protect users from themselves, protect users from attackers, protect users from trusted third parties. We're getting to the point where we have a number of options where we have pushed security out to the edges and users have sovereignity and they might experience loss due to negligence.

How would you build a bitcoin bank? All you have to do is write down that 24 word seed phrase and keep it safe. This probably seems normal to most of us.... but to an outsider, this is kind of insane. It's like saying hey, here, have some radioactive material, and keep it safe. What person even really knows how to store and keep secret a small amount of digital data? OUtside of this room, there are very few security experts that know how to manage these kinds of systems. This might be controversial, but I believe we wont be able to get to mainstream adoption if we're requiring people to keep small amounts of data safe where they have no recourse if they don't have great IT practices.

I am not trying to rag on trezor or anything but part of the thesis at Casa is that a user should not be trusted to manipulate and handle private keys by hands... then logically it should make sense we shouldn't require them to hold on to the seeds. Just a few days ago, we saw a phishing attack against trezor users that was trying to exploit this vulnerability. Was this DNS poisoning or BGP attack? It doesn't really matter-- we're in a phase now where we have fairly secure hardware, and this proliferation of secure hardware has made it obvious that the weakest point is in fact the user. It's really difficult to get rid of the user from these systems. But they keep coming back and finding new vulnerabilities to create.

There's probably an infinite ways to store and recover data. At Casa, we have created an easy-to-use wizard where the user can rotate the keys in their wallets, and this works well due to the multisig multi-location vault product. There's also a seedless account recovery that the Edge wallet has as a setup where it's a 2-of-2 scheme where you have a key sent to your email and then an encrypted key is sent to the Edge server and you decrypt it through account recovery questions you have to answer. I would like to see more work happening in this space.

You should be able to recover your private keys without touching that data physically. Don't let the users touch the private keys.

Some people say well just create a paper wallet and send money to it... but we have seen a lot of money loss there. If it's an unencrypted paper wallet, then physical attackers can sweep your wallet. And paper wallets are not robust against environmental disaster. If it's a paper wallet with a single private key, then someone will sometimes load that into their wallet, and then send part of the value to some destination, and the rest goes to a change address and a user doesn't understand what's going on and they have accidentally lost the vast majority of their money.

Metal wallets are prone to failure, they are more robust to environmental factors. I'll be publishing in-depth stress tests of the popular metal wallets. I managed to get access to a 20 ton hydraulic press so I really mean stress tests. Improper transaction construction is not a problem if you use a whole seed phrase, but it can be a problem if you use only a single private key.

We need more redundancy: multi-sig, multi-device, mutli-location. Users should not be relied on to do the most basic IT practices. We should help them do that. We can all agree that five Ricks are better than one.

I used to use an airgapped computer, and I had an insanely long generated passphrase... I put in all my recovery data.. then I did Shamir secret sharing scheme to take the insanely decryption passphrase into an m-of-n setup.. and copy this encrypted file into n different USB drives and put text files into that one shard for that person along with a text do cument with instructions... hand out USB drives in faraday bags to my executors of my will, and update annual to protect against bitrot. Writing this down and testing it took up even more of my time. If you don't test, you are guaranteed to have a failure. At end-of-life, it's not just creating them for people in this room, people who are enthusiastic and nerdy and willing to put effort into making this work. But we need to make sure our heirs can navigate these systems. They are going to be really upset if you get hit by a truck and can't access anything.

Crypto-castle is this concept I came up with after I submitted this talk proposal.  Air gaps are the moat. Strong crypto and multisig are the stone walls. Hardware key managers are the portcullis. Wallet software is the gatehouse. Automated alerts are the watchtowers. A simple duress kill switch is the drawbridge.

Facial recognition for wallets might be interesting for being able to blink an SOS or stick outt your tongue or falre your nostrils or something so that you can signal to your wallet that things should be locked down. That's more of a long-term thing.

Trust minimization is a big deal if we're trying to build systems where we're using third-parties but we don't want them to be trusted. Us building a team allows us to come together and build software... but the problem is that you can easily centralize it in a way that makes failure scenarios much more likely. So we're trying to make a balance between low trust and high convenience and high trust... and pushing security out to the edges can allow for untrusted third-parties to facilitate bank-like relationships where we can provide financial services without actually being custodians. You can have a key on a device that you are cryptographically signing data with, that gets stored on a server, so that you can be protected against third-party attacks where an attacker gets into that server. You can throw alarms on the device and shutdown operations before you get received by whatever data is on that third-party service.

As several people noted yesterday, I think a full-stack integration where you cna have a node running at home in your own trusted environment is something we're going to see long-term and hopefully get plug-and-pay going.

Bitcoin is a new paradigm because users have been trained to trust third-parties. If the average user is not going to read the manual or make any sufficient effort to try to secure their own data, then we need to do what we can to build guiderails to force users to go through educational processes. At Casa, we're trying to do that in a user-friendly visual format where we're trying to visualize the security in real-time or at least as well as we can to let people have a better understanding of what's going on with their wallet.

With phishing-- people are going to get tricked. If you are sending a large amount of money, it should say, "hey this is a lot", and tell the user to not copy-paste, and tell the user to all someone and verify all the data. I'm also interested in CHECKLOCKTIMEVERIFY being used more which can stop some social engineering attacks. It becomes an issue with multisig if your funds are locked up, you lost your keys and you need to do recovery. I want to do a graceful degradation of multisig where we lock it up for the next year but we can degrade from 3-of-5 to 2-of-5 after a year if nobody is touching this money. This gets more complex on a technical side... I hope MAST can make this more possible.

At Bitgo, we had malware blacklists where we found malware bitcoin addresses and just blacklisted those addresses. It was surprisingly effective.

I am hoping to see more KYC-- know your counterparty. We need web-of-trust and reputation systems. Some people are working on that.

Bitcoin covenants have been implemented in the Elements sidechain. Hopefully we will someday see those on mainnet as well.

# Q&A

Q: Where did you get those blacklists from?

A: They were publicly posted by Kaspersky on their blog.

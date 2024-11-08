---
title: 'BIP151: Peer-to-Peer Encryption and Authentication from the Perspective of End-User'
speakers:
  - Jonas Schnelli
date: 2016-10-09
transcript_by: Bryan Bishop
tags:
  - v2-p2p-transport
---
<https://twitter.com/kanzure/status/785046960705339392>

Good morning. Thanks for having me here. I would like to talk about the end-user perspective of p2p authentication. I would like to start with a little example of how difficult it is to be aware of end-user issues that they are facing at the front. Who is using a thin client? An "SPV" wallet on your smartphone? Yeah. Who of you are on iOS? Yeah iOS has a pretty large market share, maybe not in this room. But in general, yes. And who of you are self-compiled and self-installed on iOS? Oh, two guys. Alright. Well, you can self-compile on iOS but you can't self-install unless you're participating in the expensive developer program. There is no proof that you are installing iOS app that reflects a certain git state. There is no link between the binary you download and the source code on github, unless you jailbreak your phone to hash your binaries. You can't hash an iOS application. Private key storage with iphone apps has a questionable trust and security model.

Assume you have a large vaults at home, storing some gold bars. Would you allow unlimited access from the wallet manufacturer at all times? No, of course not. This is what you're doing when you're running an "SPV wallet" on your smartphone. Let's assume breadwallet as an example; assume there are 10,000 breadwallet users. Each of them stores maybe $1,000. This is a $10 million bounty protected only by a single icloud login; we have seen icloud logins attacked for much less value. Yes, apple has code signing. But what's the purpose? You have to be participating in the app developer program. The end users can't verify the signatures. You can always revoke the signature anyway, and upload a updated new-- revoke the key and upload a new application.

Bitcoin scaling like bip151 is about core infrastructure. A $10 million bounty? People have been kidnapped and murdered for much less than $10 million. Breadwallet can be forced to upload malicious binaries. I love the talks we had yesterday and today. I think it's important for scaling and throughput. But we can't forget about end user problems. They are pretty important. People losing their private keys and running into stupid issues-- all the scaling is kind of useless at the end. So I think we need to have some group of people focusing on end user problems and looking at it from a different perspective.

This brings me to the point that running a full node... "extremely difficult" for novice users. I hate Bitcoin Core. I have worked for 3 years on Bitcoin Core. Starting on Bitcoin Core really sucks. It's not fun. I would not recommend novice users to download Bitcoin Core. People are downloading Bitcoin Core. Nice. They get some addresses. They receive some coins. And then they're stuck because they need to do all of their validation before they can send out coins. So I'm wondering out why there's no thread on r/btc that Bitcoin Core is stealing funds because of this. You block coins for several days before you have done initial block downloading (IBD).

Thin clients and "SPV" wallets are only working because there are enough full nodes that provide a free-of-charge service with bloom filtering. It's pretty CPU heavy. There's no incentive to run it. People are slowly disabling the feature. We have a declining number of full nodes. This could be a problem because there's a lot of people using "SPV" wallets.

Also, almost all light clients are leaking private data. There's a lot of privacy information leaking through the "SPV" wallets. Taking the SMTP analogy, most people today no longer speak SMTP when they send email. I sure some of you in the audience do. Most people use gmail or yahoo or hotmail or some sort of hosted solution. SMTP has been extended to death with all sort of additional features. You can no longer run your own SMTP server. Users were dragged out of the protocol. You need hashcash to get rid of spam. Encryption has never been made a standard on that protocol.

Let's make bitcoin great again. What's missing? I think we see declining amount of full nodes. It's hard to run a full node. I think we should do something to kind of make it more attractive to run full nodes. I also heard people said you know well when there's not enough full nodes on the "SPV" front we just bootstrap hundreds of full nodes. It's nice, but it doesn't help decentralization. People have perhaps started most of them now using centralized solutions like blockchain.info and all these solutions where you are no longer on a p2p network. It's also the problem that multisig, one of the nicest features we have in bitcoin, we cannot bring that to the end users right now, it's extremely complex to setup multisig solutions. There's CoPay, but do you really want one company responsible for bringing multisig to end users? We should have p2p based infrastructure, decentralized infrastructure to create shared wallets, to cosign transactions.

And also, as I have made the example at the beginning, end users are not aware of the security model they should be aware of. Perhaps they have learned that private keys should be kept private, but what means private? Perhaps that's the problem right now. Also, there are no standards for hardware wallets. It's hard to protect your private keys. There's no compatible hardware wallet for iOS. Also, there are missing option to securely connect to a full node. I am pretty sure some of you run a full node, and at the same time you might have an "SPV" client on your smartphone, but you have no way to connect them. I don't know of any wallet that has a trusted connection to your smartphone. This means you have validated the blockchain, but you can't use it from your smartphone.

This is what bip151 addresses. I would like to see the end users closer to the p2p network. This should be based on the p2p network. I think this would help decentralize and maybe bring those users back. It's already in a late stage. Your swiss bank account in your pocket, is that still true? Yes you can run a full node on your Android device. If you could run a full node somewhere in your server, and maybe have your swiss bank account in your pocket and maybe connecting to your server, yeah we could do that with bip151. There are two bips. As Gregory said, I have too many bips. Sorry about that. But they are distinctive.

So today we have in bitcoin, the nature of bitcoin does not really require encryption---- unless you have bloom filtering. But it would be good to encrypt this. We don't quite know how the protocol is going to be extendd. SMTP was made in the 80s to send information about shutting down servers. We should think a little bit ahead about the protool might be in 5 to 10 years. Encryption in my opinion is essential to have in such a protocol. Today, "SPV" wallets they connect if you pay for a coffee, you kind of connect to the internet over wifi provided in the coffee shop, and you leave a lot of traces about what addresses you're using. Your ISP could censor those transactions or link those transactions to you as a form of surveillance and privacy violation. They could look at your transaction graph, hold back transactions, things like that. So it would be a good option to connect "SPV" wallets to trusted full nodes running at home or at your server rack or whatever. Also in more poor countries, they might want to share a full node with an entire village, that would be possible. They would trust the village full node, as the bank in the village, and they would connect to it in a secure way. Also maybe multiple trusted nodes because of the nature of the p2p network. This leads to a swiss bank account in your pocket.

People tell me they can't run a full node anymore. It's pretty easy. A $29 computer that I bought a few months ago and it's running a full node. I have a trusted node for $29. It has no case, I guess. But I still have the black box next to my router at home having a yellow light when my blockchain is not in sync, and a green light when it's in sync. When it's not in sync, well I sacrifice some privacy and connect to random peers. If you own maybe more than 0.001 BTC, you should consider running a full node and being part of the p2p network. It's possible with $50. We should make people aware of this. You don't need a huge server at home to run a full node. You need to have some bandwidth and things like that.

bip151 is the encryption bip. It eliminates passive surveillance. Right now, anyone can listen to the stream between nodes and they can learn everything and even tamper with the stream. bip151 does diffie-hellman key exchange with all peers. There is a session-based key. Then the channel is encrypted, without any authentication of the remote peer. You would have to do active surveillance to listen to the stream. It's easy to do that, to put the man in the middle and substitute keys in both directions and you could listen to the stream. But you risk being detected, because you don't know if the peers are going to authenticate with each other-- it's increasing the chances that the surveillance enemy will be detected if they are monitoring the entire network or something, because someone will probably do authentication.

ChaCha20-Poly1305 is used in openssh. Also used by Google. People have told me eh come on, why not use openssl? Well we're using well-known proven crypto. Well, look at the long list of vulnerabilities in openssl. The scrollbar there-- it's pretty tiny. I'm not happy with openssl. So what about related solutions? Most stuff is already possible. Is it accessible for end users? Even for us, it's hard to setup an stunnel between your full node and your client. i2p, tor, openvpn... it's always about the accessibility from the end user perspective. If you can't use it, then it's worthless. It should be made into Bitcoin Core. Simple. Nothing on top of it. No other layers. It should be possible in the standard protocol.

The implementation is quite simple. It's roughly 300 lines of code. It's fairly auditable. We could farm this out to some academia people who want to audit this. It's very fast. It's faster than AES256. There's no known security weakness by today.

Here's a performance graph of ChaCha20.

We have a chance to slightly update the message structure of how bitcoin p2p messages are working. First, we could get rid of the 4 bytes of magic, which is no longer required. We are seeing leaked information in another space in the past. It's pretty inefficient because every message has a double sha hash digest. Each message gets double sha256 to get the 4 byte checksum. When we have the AED poly1305, it's no longer required. It's also possible that we can aggregate or combine into one message that contains bitcoin messages, one encrypted message could contain several, for example. This leads to a thing where with encryption for an nth message, we are only slightly higher in bytes. Pieter Wuille came up with a thing where it might be faster over the network than the current protocol because double sha256 is pretty extensive, and the AED construction that we want to use is in theory faster. So encryption in this case is not a performance penalty.

In bip150 (not bip151), is fingerprinting-free peer authentication. Greg Maxwell came up with a fingerprinting-free authentication. I think this is amazing. It allows you to authenticate a peer without revealing any information about your identity. A hacker cannot be pretending to be the trusted peer and then see who wants to connect. Authchallenge, authreply, authpropose, authchallenge, authreply. I think this protocol is pretty amazing.

Thank you.

# Q&A

Q: AB Core on Android?

A: Yes.

Q: Anti-fingerprinting?

A: The authentication scheme in bip151 assumes we have pre-shared keys. If you have a full node at home, you could scan the QR code with your smartphone and then the two devices are paired. Or maybe you need to put the identity key on your node first. You have to pre-share the keys in advance. And then you can authenticate without revealing your identit key, using a hash, and then the other party tries to use the pre-shared key to see if there is a match. And then producing a signature to prove that they know you, and then the same thing on the opposite side. It's impossible for a man-in-the-middle to steal identity or get information about who wants to connect.

Q: Would you be open to running a contest for developing crypto protocols to get a larger field and get some adversarial engagement towards this?

A: Totally. I think the only thing that drives me is having something that works. I think the standard we're using seems to be okay. But I agree we need more studies on the stuff we're using. But we're not inventing a new crypto system for this.

Q: You mentioned some issues on iOS for hardware wallet. Given that most wallets work for Android, isn't the problem that iOS forces you to whitelist devices in order to connect them? As opposed to specific problems with standards.

A: Yeah I mean the exact problem is that no hardware wallet for iOS, in many directions. We need a standard to decouple keys from the application that wants to sign something, in order to have secure key storage. Otherwise it's going to be a mix. It's going to lead to people not able to use solutions like hardware wallets that sign digital information.

# References

<a href="https://github.com/bitcoin/bips/blob/master/bip-0151.mediawiki">bip151 peer encryption</a>

<a href="https://github.com/openssh/openssh-portable/blob/05855bf2ce7d5cd0a6db18bc0b4214ed5ef7516d/PROTOCOL.chacha20poly1305">openssh PROTOCOL.chacha20poly1305</a>


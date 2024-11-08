---
title: BIP324 - Version 2 of p2p encrypted transport protocol
transcript_by: Bryan Bishop
tags:
  - v2-p2p-transport
  - bitcoin-core
date: 2022-10-10
aliases:
  - /bitcoin-core-dev-tech/2022-10-10-p2p-encryption/
---
# Previous talks

<https://btctranscripts.com/scalingbitcoin/milan-2016/bip151-peer-encryption/>

<https://btctranscripts.com/sf-bitcoin-meetup/2017-09-04-jonas-schnelli-bip150-bip151/>

<https://btctranscripts.com/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/>

<https://btctranscripts.com/breaking-bitcoin/2019/p2p-encryption/>

# Introduction and motivation

Can we turn down the lights? "Going dark" is a nice theme for the talk. I also have dark coffee. Okay.

We're going to talk a little bit about [bip324](https://bip324.com/). This is a BIP that has had a long history. We even have a page about the history. It all started more than 6 years ago... Bitcoin p2p traffic is unencrypted. It always has been. We'd like to change that. The argument for why we want that is more subtle than in many other settings. In Bitcoin, by nature, all data being exchanged between nodes is public data. Or at least at some point will be public data. Every transaction you relay hopefully ends up in the blockchain, and so forth. So the question for why we would want encryption or privacy on the p2p network in general is more a question of metadata in the sense that for example a global observer who can see lots of connections may infer the origin of the transaction by seeing bandwidth spikes in one place propagating further. Now they can just look at the data and see the transaction going everywhere; they might be able to identify where miners are in the network topology by seeing where a block originated at first. This leads to more second-order effects, and if you're willing to pull off an eclipse attack on the network then you can extract more information, or privacy about who is running which version or who is transacting with whom.

This, of course, ties into the question of authentication where bitcoin nodes don't have an identity today and we don't want to change that. But by its very nature, nodes don't really have a reputation system. Every node is equal and we can't really talk about as long as they speak the protocol and do things we can't talk about an attacker or not. But at the same time, it is true that many people do use deliberate connections where I run two nodes and connect them or I run a wallet on my phone and I want to connect to my own node because obviously I trust my own node more than I trust other nodes. Today, the identity system used for that is IP addresses. Sure, you can setup a VPN, but this is annoying.

Most of the time, we don't care about authentication, which is why it's not part of bip324. But now the question is, does it make sense to encrypt if you don't have authentication? As most people would know, if you don't have authentication then you can't really do secure channels because you could always have a man-in-the-middle attacker. More importantly, the fact that an attacker can just spin up nodes makes the whole question of, well, an attacker is hard to define even without a notion of identity.

Our answer is yes, that it's worthy to encrypt even if we don't have authentication. It raises the cost of an attack. Doing global surveillance style attacks on the network, even just for metadata analysis, is significantly more complex if you need encryption state and you either need to spin up millions of nodes yourself or get others to connect to your nodes or actually man-in-the-middle existing connections, which is significantly more expensive than just looking at traffic. If you have to MiTM all existing connections in the world, then that's not really feasible; if you MiTM some of the connections in the world, then hopefully some people somewhere in the world would notice it.

So this is all about raising the costs of such an attacker, and it's cheap to raise these costs. We also want to build a system on which optional authentication mechanisms can be included. They are not included in the bip324 proposal. We have a cool cryptographic scheme that we're working on too, but that's for later.

We don't want global identities on the network. Most of the connections won't be authenticated. At that point, it's not even clear if people would want some form of authentication. Say you have two nodes and you want to directly connect them. In that case, you might want authentication. But even then, it's not clear what information you would want to reveal there and what information you wouldn't want to reveal.

We make a distinction between the network consisting of a bunch of random automatic connections where peers truly don't care about whom they are connecting to, and manual deliberate connections where you connect to a specific node where you have some notion of an identity. What this encryption proposal does is that, even if only the deliberate ones start using at some point an authentication mechanism then they should be indistinguishable because every connection we want is encrypted. Some of them will be authenticated, but an attacker wouldn't be able to tell.

Does it make sense to encrypt without authentication? Yes, because it raises the cost of an attack for the attacker, and it will hide metadata information on the network. Our vision is that all connections will be encrypted, and then if people want to use authentication then they can additional use that too, which is not included in this proposal, although there is an interface for later authentication proposals to use this platform.

There is one authentication included in bip324 which is that node operators can out-of-band compare the session ID... it's sort of like... it may be sufficient to detect a MiTM attack. For running your own node with authenticated connections between two of your nodes, this would probably be feasible. It's a defense against MiTM attacks. If you know that some nerdy people are doing this comparison, then the attacker can't just MiTM all the connections.

Q: jonaschnelli was saying this shouldn't be referred to as encryption but rather a v2 p2p message format because of all the other updates, which could also include an encryption session id.

A: Yes. The messages are 3 bytes shorter now in this proposal. Messages will be shorter in the end. I'm not concerned about this argument, because we had this in the TLS debates 20 years ago where something was a half percentage more of CPU utilization and others argued that was too expensive.

The rationale is more like, we're proposing an upgrade to the p2p network and its primary feature is that it does opportunistic encryption. At the same time, it does not worsen bandwidth or CPU time. Or at least not measurably. It really comes at no cost compared to what exists because the existing network is really inefficient.

Q: ...

A: There are two distinct pieces of information that we're aiming to hide. One is, is there a bitcoin node running here? We make some steps there. The other one is hiding the data that is being transferred. Neither of these we succeed at hiding perfectly, the only thing that we do is raise the costs. An attacker can just run a node themselves or MiTM the connection or whatever and still see what's going through there. They can still do traffic analysis, even if not reading the encrypted bytes they can see spikes. We provide mechanisms for hiding that information but how to use them is not actually part of bip324.

Q: How do you quantify this... and because of this traffic analysis... What is the global passive attacker if...

A: Look at all the connections and look at where a bitcoin transaction first appeared and then you would know which node created it. This is specifically about hiding transaction flows.  It's still possible with traffic analysis, but traffic analysis becomes harder than just seeing the transaction on the wire. Once transaction relay is encrypted, you can pad transactions so that they are the same size with some extra bytes, which is useless right now because transactions are not encrypted at all.

Traffic analysis becomes less easy or less possible. Some kinds of transactions are easily mapped, like based on UTXO set size. It fundamentally makes it harder to understand what it is because the properties are different and there's more possible sources. That's true if you're just a passive observer that only gets traffic data, versus getting the data by tapping the wire. The attacker can also MiTM the connection but that is much more costly. It's not the same class of attack. With this type of thing, you will find that global active attackers have a much harder time to go and do their attacks, especially if there is more than one of them.

Q: But I can still look at encryption size?

A: Yes, but small transactions have roughly the same size. ....

Q: With other methods getting more costly, ... what about connecting to each nodes and try that way to do that?

A: They are already doing that.

Q: But wouldn't this encourage more people to do that?

A: That's a good question. It's along the lines of what we just described. I think we say this literally somewhere. We want to force attackers to become active if they actually want to attack. It's a good question if this would be bad for the network. The counterargument would be that we should just dump all the data to them so that they don't attack the network. I'm not sure if that's better. We get requests from people doing research into p2p analysis; "why don't you provide a p2p message to ask nodes who they are connected to, this would be very valuable information" yes, it would also be very valuable to attackers. It's mutual escalation....

Any more questions about motivation or setting? We could go into history.  One piece of information that we want to hide is if we're running the bitcoin protocol. One way to see is to just try to make a connection. The v1 protocol literally starts with sending the network magic followed by version. It's 12 very recognizable bytes that probably nothing else in the world sends. So we make an attempt to have a little bit of censorship resistance; at the moment, it's really easy for firewalls to look at the first 12 bytes and see that it's a bitcoin connection. They can also look at more simple information like port numbers, of course. But we want to provide a basic protocol that you could do in the future to do more advanced work.

This is, again, about raising the costs. An obvious response to a would-be bitcoin p2p censor is, well, now they need to block everything except a whitelist of permitted protocols which probably has a lot more collateral damage rather than just blocking bitcoin p2p. This is always the game for censorship resistance. When you define it, it's not the ability to connect, because your ISP can always pull the plug. It's really about the collateral damage they would do by pulling the plug entirely.

Q: If I want to design my own p2p protocol, and I follow this, would it be indistinguishable from bitcoin?

A: Yes. To a passive attacker, the bytestream from a bip324 connection is uniformly random. Every byte going through it, there is no statistical pattern whatsoever. This is a very nice common denominator that anything like, you don't even need to use the same kind of cryptography... there are other kinds of protocols like tor, or others. You can also stick it into other protocols, you could write an HTTP wrapper. That would be a much more ambitious goal of trying to disguise bitcoin p2p traffic as HTTPS or ssh traffic, which is difficult because we're not running on a standard HTTPS port which already gives it away. HTTPS has another problem. But at least it becomes easier to build on top of a uniform construction like bip324.

Tampering also becomes more complex. Right now, an attacker can just flip bytes in a message and notice immediately and terminate the connection. Even for an active attacker right now, say changing a surface bit in the version message is super cheap, you just pattern match and flip it out. Once you have an authenticated encrypted connection, and at this point I should say authentication in the context of encrypted connections has two completely different meanings. One is am I talking to who I am intending to talk to with respect to some identity, which we don't do in bip324. But we do have an authenticated encryption scheme, which means we do know that every message after it decrypts correctly comes from the other side. We don't know who they are, but we know no MiTM attacker came in and changed it. We get an ephemeral identity at the beginning of the protocol and if later the attacker wants to change something, then we notice that. Either you do a full MiTM attack, or you can't change things.

If we were to use unauthenticated encryption, which we don't do, then an attacker might be able to guess; "oh this is probably the version message and this is the service bit" even without knowing what the bit is, they can flip that bit. This is prevented in authenticated encryption.

Why have pseudorandom bytestream? Traffic analysis... yeah, we went into that. You can look at timing, sizes, and a clever interceptor can look at larger messages and if you get a block every 10 minutes then maybe it's the bitcoin protocol. But it's much harder than just doing pattern matching on exact bytes.

Why not use a secure tunnel protocol? Why not use tor for everything? Or VPN? Really the answer is that we want something that works for every connection. We want it ubiquitous and we also want to later be able to define extensions like for authentication. We don't want the authenticated and unauthenticated ones to be distinguishable. This has to work everywhere. Doing it over tor would work, but would come at a great cost.

Tor is a centralized network. It has a set of 16 nodes that control the entire thing. Many people forget this. So just right out of the gate, we can't just say use tor. Also latency is much higher, and bandwidth costs are much higher. Controlling a lot of IP addresses is harder than getting thousands of new tor identities because they are just public keys. Eclipse attacks on tor only are way way cheaper than on the real internet.

VPNs or wireguard or whatever, yeah you could do this but it's built for manual config. VPNs require configuration. We want something that works for automatic connections that is enabled by default.

Another thing you could do is there are general-purpose secure channel protocols like TLS and Noise, Noise is actually a framework for defining your own protocol. You could do this, but it doesn't really fit our use case because that focuses on authentication. Often you want encryption with authentication. All these protocols focus on it... their properties break down or introduce a huge amount of complexity just for having authentication. Instead, we want something very simple that just does encryption but is modular enough that you can build something with authenticaiton on top. The downside is that this will probably result in a protocol with more roundtrips, but we don't care about roundtrips because bitcoin p2p connections live minutes, days, hours, weeks, sometimes more.

Q: So you are using authenticated encryption but you are not authenticating the other endpoint?

A: Correct.

Q: Can we use a word other than authentication?

A: I proposed "integrity" but it's bad because the cryptographic community has already settled on these terms so it would create more confusion.

There is a public key, though. It's just unidentified. There's authentication and then there's authenticated encryption. Hard disk encryption is generally unauthenticated encryption. The definition is in the BIP already. We have a footnote. So just read the BIP.

If you want to run TLS without authentication, you can do things like self-signed certificates, but introducing that into Bitcoin Core doesn't really make sense. No one wants that. We have a few other reasons, like we want a message-based protocol not a stream-based protocol. This on itself introduces privacy properties that we want to introduce. TLS and Noise are string-based and have no notion of hiding packet information. We would still need to build something for that and undo that damage if we were doing that.

Another reason is that we want to use the secp256k1 curve, but the reason for using off-the-shelf protocols would be gone because they don't do that. So in the end, using something that already exists doesn't make sense. Also, we have long-lived connections. We don't care too much about latency of connections. This means that roundtrips are okay. Say we start with encrypting and then if you want to do authentication you can do that later, inside the encrypted connection. In other protocols, they try to do this at the beginning of their protocols to save on roundtrips. Modern TLS engineering goes into making it work with half roundtrips or in some cases no roundtrips at all. But we don't really have those requirements.

The nice thing about a pseudorandom bytestream is that no matter what cryptography you use, it's all indistinguishable from each other, modulo timing and all the cryptography being itself broken.

# Goals

We want confidentiality against passive attacks. As a passive attacker, you shouldn't be able to read the data that is sent.

Observability of active attacks: now that passive attacks don't work, you have to become active. So the least that could be done is session ID comparison.

You want a pseudorandom bytestream because every single byte needs to look like a random byte. No version identifiers and no prefixes or public keys, nothing.

We want to have a shapable bytestream. That is the padding we refer to. The protocol has the ability to pad messages arbitrarily, so you can do something like define an extension or have an implementation that says every second I send 10 kilobytes like clockwork. If I have more to send, it goes into a buffer and I only send out 10 kilobytes every second. If my buffer is empty, I pad it with garbage to still send 10 kilobytes. Now your timing fragmentation information reveals nothing. Our BIP does not specify how to do that, it only provides the mechanism for doing it.

We want forward secrecy. There are different notions of forward secrecy. In our case it means that if an eavesdropper attacks the encrypted bytestream and later you compromise a node with the session secrets, then you shouldn't be able to decrypt past session traffic. Maybe the last few bytes, but not all the previous traffic. There is a limited time window of what you can see.

We have a symmetric encryption key, and every few packets we hash the key into... if you steal the new key, you can't go back, the hash function protects against that. This hasn't been used in practice, interestingly, but it's cheap and simple and it works.

There is a notion of a double ratchet construction in Noise and other message protocols. There are even ones where every message you send requires new key negotiation. Forward secrecy can mean different things. Often it means, like in TLS, it means you have a TLs connection and it gets terminated but now you steal the server secret key and I shouldn't be able to decrypt past traffic. That's related to long-term secrets; but here we don't have long-term secrets because every secret is only session based. So here we have forward secrecy inside the session.

If someone then adds identity authentication on top of this, it doesn't compromise forward secrecy because the forward secrecy started with a key and only.... this property on the encryption side remains. Obviously they might be able to forge identities when they get the identity secret keys.

Upgradeability: we have a version mechanism in this. This is important. It's important to have this. We think the step of going to a uniformly random protocol is that, there's no identifiable feature to a passive observer which means we have removed the ability of the future in.... we can't do a v3 or... we could, but you would need out-of-band signaling to determine which of the two versions to use. So we feel it's important that the protocol itself has a means of saying once the encrypted session is negotiated, we can negotiate further and now switch to v3 and now switch to v4. So, to an observer that cannot break v2 encryption or cryptography, they can't tell which version you're using. You could upgrade to optional authentication or to post-quantum crypto handshake, and this is more complex in this setting you would have something like... let's say Diffie-Hellman is broken and you want to do post-quantum crypto then you would do the normal handshake as now and maybe an attacker can read this, and that's okay, but then we would upgrade with a post-quantum handshake inside of it. It would probably be a long time for which secp is not actually broken, and as long as that's the case, an attacker can't see anything. Also, if it does get broken, the p2p network is not the biggest problem.

Compatibility: v2 clients will allow inbound v1 connections because we don't want to partition the network. This will be very opportunistic if either side does not support v2 it will just be a v1 connection. What about having different port numbers and advertising them separately? No. First of all, using fixed port numbers is kind of impossible, having pre-defined port numbers is a contradiction with hiding your running of a bitcoin node. Since the previous bitcoin main release, it doesn't have a strong preference for port 8333 any more. ... You could advertise two separate identities and two separate ports. We started treating different ports on the same IP as a separate.... hmm. We started treating different ports on the same IP as different addrman entries; we totally could do that.

How would that work with DNS seeding? That's a good question. It really doesn't. I think the longer-term future for DNS seeds is that they become p2p nodes that you connect to with a one-shot connection. But now this means the DNS seeds would have visibility into who is asking them for peers. But the upside is that your DNS seed wouldn't; only PDNS servers in the middle know now. We could imagine something like, having DNS seeds that use a different name for the ones that are v2-enabled but still you need a means of communicating the port number. I think that for the time being those will need to remain on a standard port.

Q: Why don't we use SRV records?

Historically the reason was that we looked into that I think, 10 years ago I don't know, and the difficulty was basically that we needed to implement our own DNS resolver because you can't use the operating system name resolver because its interface just gives you an IP address back. But yes that is a solution.

Some ISPs their DNS resolvers are broken and won't return SRV records properly.

Another downside of using different ports is that at some point the argument becomes fuzzy but it's even easier to block. At some point a firewall can just allow or disallow ports, so then it would be really easy to block v2 connections and allow v1 connections.

You could make the argument that for this upgrade you could have separate ports. But in the future, all protocols should just use the same port. Long-term, we hope everything uses bip324. This is long-term future. It should become ubiquitous.

Will v2 ban v1 for sending garbage? We solve this by adding one sentence in bip324. If you are met with an immediate disconnect, you are encouraged to immediately reconnect as v1. I don't think you get banned immediately for this at this stage because it's just a mismatch of the network magic and it will disconnect.

If it was that easy to go and get banned, then you could go partition the network. We would have a big problem if your node could get banned just for that.

The last goal here is low overhead. We talked about this already. It should not substantially increase computational cost or bandwidth for nodes. It's slightly lower bandwidth than v1 p2p, and it's a bit lower CPU if you have a pure CPU implementation of sha256. If you're using hardware accelerated sha256, it's really hard to beat that.

Q: Does the new checksum have error correction?

No. Something to do at a different layer.

# History

This proposal has had a long history. It started in 2016 by Jonas Schnelli. The initial idea was two bips: bip151 and bip150 which would do encryption and authentication. They had a very different approach than what we now have which is why it's a different bip bumber. Bip151 started as a v1 connection and would send an application level message and say I would like to upgrade to v2 and the other side would reply yes we're v2 now. This has some obvious downside: among others, you have sent a version message in the clear before any encryption negotiation took place. This doesn't hide the connection going on. It might even be worse for authentication because you might want to only talk to a certain node, and after sending a few cleartext messages you would figure that out, .. there were attempts at privacy there but they were weaker. At some point we thought, no if we want encrypted connections then the whole connection should be encrypted which is when the bip324 effort started without authentication. We thought this was more modular and could be done later or separately. This went through a number of iterations. Until 2019, Jonas was mostly working on this but only on-and-off.  Dhruv got interested, and he kept us busy. He kept sending us messages about the progress. Big kudos to Dhruv.

Q: Do you remember [countersign][countersign-section-on-another-transcript]?

That's the private authentication protocol we're thinking about. That's a novel cryptographic scheme that we want academic or more formal writeup and review on before we even consider proposing it. It's not clear what kind of authentication people would even want in the future. It's not necessarily the only authentication scheme; there could be multiple schemes. It's modular. Everything has baseline encryption, so it doesn't really matter what people do on top of it in terms of authentication.

Any questions on motivation, goals, history, or design at this point? I think we can go into some of the more technical aspects about how we achieve these goals.

Q: Why is the service bit necessarily? We try v2 first and then try v1?

A: The idea is that our proposal has a surface bit that tells the initiator of a connection whether they should try v2 or not. The reason we want that is the alternative is that a v2 node basically tries to always connect to v2 and tries to downgrade. We feel that the latency cost during deployment, like when this proposal is new, almost all responders will not support v2 and the cost of needing two connections is just too great for early on deployment. Maybe we can think about it later on where v2 just becomes a default.

Q: Is this much more costly than another roundtrip?

A: ... additionally you have concerns like nodes having a limited number of inbound connection slots. You're at a disadvantage as a v2 node trying to make a connection because if at the same time someone else can.. get it on the first try, then you on the second.. but.. of course, an attacker on the network which ORs the v2 service bit into every other message can probably trigger this on the network at a fairly low cost anyway. But maybe not.

Q: Is it possible or practical to support other protocols on the same port? Like if you only had port 443 with a secure webserver there as well.

A: I think yes that is possible. SSL is actually fairly identifiable. You could have some protocol multiplexer that input side says oh it looks like SSL so I will forward that to my webserver and if it doesn't look like SSL then forward it to bitcoin. Since it's uniform, you need something where everything else matches to some fallback.

That's interesting, you could run another protocol in parallel. Especially if they are both uniformly random.

Q: I notice a lot of VPNs allow for a single digit number of ports on which you can listen on.

To be clear, this is designed like an encrypted packet level scheme. You're not, this isn't an encrypted stream. It's not a stream-based interface. The application interface is packets. But you're only thinking about running this on TCP so far. We do have this shapeability, so you have an ability as an implementation to fragment up your packets arbitrarily or stuff them with garbage. So you can defeat the fact that TCP at the wire level has observable lengths.

Q: Have you thought about what form of comparison the secure session ID would use? Does it need a secure side channel to avoid tampering?

You do it out-of-band. I have two nodes. I run getpeerinfo on both and then compare the session ID. There is no protocol. If we want a protocol, then that is an authentication protocol. But this is a mechanism that any authentication protocol would use, at the end of it they would compare session IDs in a cryptographically secure way.

# Specification: transport layer

As it says, when a v2 connection is established, and there is nothing else sent. There are no packets, there's no v1 messages exchanged or anything. The first thing that goes over the wire is .... the specification has a transport layer, which is the bulk of the BIP is how do we establish encryption keys? How do we create encrypted messages? How do you verify them? Almost everything is there. Then the application layer is for how do we now route bitcoin message commands over that transport layer? The signaling is then just using the service bit. Almost everything we will talk about is in the transport layer. That's where the cryptography is.

There are two parties. We call them initiator and responder. We start with a key exchange. The first thing that goes over the wire is not exactly a public key; it's not a public key with a normal encoding. If you send a public key, you would be able to recognize it. Even if you just send the x-coordinate of an elliptic curve point, you could check if it's on the curve or not. Even the fact that, an attacker can observe; "well I've seen 30 connections come out of this node and the first 32 bytes of them are always valid x-coordinates on the secp curve, which only has a 1 in a billion chance". We defeat that using a scheme called [Elligator Swift][Elligator-swift-paper] which is a recent paper that came out but it is a way of encoding public keys in 64 uniformly random bytes. There is an overcomplete representation. Every 64 sequence of bytes encodes a secp public key. As long as you can decode them, it's fine. This is fairly new and was not in the original BIP. bip324 originally used x-only public keys. We switched to ElligatorSwift to make it harder to identify.

In addition, we want to avoid the pattern of 64 bytes and then you wait. So we wanted a mechanism for stuff-padding the public keys too. For the encryption scheme later, once you setup a channel that will become easier. But during the hanshake you need something special.

Q: At a high level, what's the benefit of ElligatorSwift over the previous one?

A: It's faster to encode and faster to decode. He implemented the first one, and then ElligatorSwift came out. I found some optimizations and informed the authors. They used some of it in ElligatorSwift. It's significantly simpler, and it's faster.

In order to defeat this pattern of 64 bytes and 64 bytes and then it starts; both parties are allowed to append to their public key up to 4 kilobytes of garbage data. After that garbage, they send what we call a "garbage terminator". The garbage terminator is derived from the shared key. The idea is now I can send my public key and my garbage, and I haven't received the other side's public key yet so I can't send my terminator yet. In fact, I don't know what the terminator will be yet. The terminator will have to be a shared secret because otherwise the attacker can compute it and see it. So the garbage terminator is a fixed 16 bytes and you scan the bytestream until you find it. But it's derived from the shared secret. We're looking for a fixed computed string in the garbage. I can send my garbage, and I don't even know what the terminator will be. I get the public key from the other side, and now I can send a terminator. Both parties can do this and you break the property that no party... so without this, we would have the property that no party can send more than 64 bytes before having seen 64 bytes. But with this, every party can send up to 4 kilobytes without having seen 64 bytes.

Q: Do you recommend sending more garbage before sending the terminator?

A: You could, but you don't actually need to. As soon as you have established the keys, you can use our other shaping mechanism which is much more flexible. But you could, yes. In fact, an earlier writeup used this before we recognized this was unnecessary.

Q: So the responder has the freedom to send more garbage? Only the initator... the responder already has both keys?

A: Good observation. As is, as the bip is written, there is actually no reason for the responder to use the garbage mechanism. As soon as the responder replies, they have a shared key. Initially we had this only for the inititaor, however we considered the possibility of having later relaxing some of the byte flow and allowing the inititaor to send less than 64 bytes initially and actively introduce more rounds into the negotiation. In order for that to be possible, we need the ability for now the responder to respond before having seen the initiator's full public key and that's why also for symmetry reasons it's a bit easier to do it on both sides. It would allow us to upgrade this protocol or have an extension that is backwards-compatible where we send 20 bytes as my public key or something. We thought the additional complexity is kind of okay because we have it on the initiator side anyway, and now it is on the responder side.

The 4095 byte number is basically set for DoS reasons. It can hide the 64 number. It's a square, too. In the future, maybe the large packets could be a default. But surely this is much bigger than the average packet can be on the average link.

So both of the parties send a public key. Both parties wait for the public key. As responder, if you see the v1 magic, .. you see the v1 protocol starts with the 12 bytes and it's sufficient. It's 4 byte network magic, followed by version and a 0 byte, ... isn't that observable? That the responder is acting that way, only responds if there is a byte that does not match the...? In theory, yes, but it is 2^(-96) that it matches which is so low that it's not worth consideration. The question though is you could look at a few actions of the responder and see by looking at the first bytes he received and when he responds. Yes, but usually, the initiator sends 64 bytes of public key plus garbage, all at the same time. An eavesdropper can't tell oh you started sending as soon as you saw this byte because the receiver just receives the whole packet at once and reacts or doesn't react. An active attacker can also go byte-by-byte.

So they both receive the full 64 byte public key... they use X-only ECDH because it's faster, but there has been lots of discussion about x-only keys when it comes to Schnorr signatures but for ECDSA it's another story. It doesn't add more security to do more than x-only. So we derive a whole bunch of encryption keys, two in each direction, the garbage terminators.... This is what the garbage terminator would look like in the wild, thanks to Greg and his stable diffusion setup for making this. I think it took 15 minutes. It's an illustration of a cryptographic garbage terminator. Maybe he changed the prompt to include bitcoin but I don't think so. Trending on Art Station.

We use HKDF-SHA256. This is a very standard mechanism of turning a bunch of entropy into private keys. Not the fastest in the world, but it's robust.

Next they send their garbage terminator, and then the other party waits for that. We wanted a property that any byte that an active attacker changes on the wire causes disconnection or can be detected. The garbage is sent before there is a shared secret. Our solution is that after the garbage has been sent, both parties commit to the garbage they have sent just to make sure everyone agrees. So even if the attacker flips a bit in the garbage, the connection will terminate. For similar reasons, the ElligatorSwift encoding of the public keys goes into the shared key derivation so that even if an attacker goes huh I wonder if this is ElligatorSwift and decode it into a public key and encode it into another ElligatorSwift for the same public key that will still cause disconnection for the same reason.

At this point, both parties have the same keys, and all further communication takes the form of encrypted packets.

Q: Could you remove the authentication packet by using the garbage as part of the derivation? I know which garbage I sent you, so I would be expecting something.... Both sides know which garbage was sent and which ones they received, and if they use that in derivation for their keys, you could use that for an authenticator. The problem is this needs two steps: in order to send the garbage terminator, you need both public keys. I mean, the derivation of the encryption keys after, though. The derivation of the garbage terminator, that would be less efficient because for every byte you would need to ..... But if you use it for the encryption keys you derive, I think this is what you're asking, this works. I argued that what we do is a little bit cleaner from a crypto structure point of view but I think that would work yes.

A slightly earlier design was that we didn't have the garbage packet, but we would update the encryption keys after hashing both identities.

An advantage of that is that if there's a bug in the code that actually verifies this, I think you would notice if it's an update or a step that someone has to implement to get it right. A subtle difference. From a crypto engineering point, I think this is more clear because you already have shared keys and have an authentication mechanism so why not use this authentication mechanism.

Does the immediate disconnection upon a violation reveal anything? Possibly. There is a signal in disconnecting and when to do it. But it's the best we can do; we want the property that as soon as an attacker messes with the connection we want to drop it. We could keep sending garbage data. This is how we expect authentication to work: if I want to make a deliberate connection to a certain node and it fails authentication then we should probably treat it as a random node, or not offer them extra services, or give the user a warning. We can keep the connection, because it's no worse, so maybe. It's natural, though, to terminate connections and not send data. An active attacker can always learn something though. If you modify one bit in the garbage, the connection will only terminate after the garbage terminators have been sent. You might be able to learn the length of the last message that gets sent.

Q: Does the garbage authentication packet have all the garbage in it?

A: It commits to it. We use the ADA and it's associated data. It's an empty packet with the additional data being authenticated.

# Version negotiation phase

The specification is that both parties send an empty message. They receive a package from the other side, and then ignore it. This is surprising to me that it is sufficient. But really the notion is that we think of this packet as encoding a version number. The version that gets used is the lowest version sent by both. We encode zero as empty, and since I only support zero then whatever the other side sends is also going to be zero. So the specification is that you send an empty packet, and you receive a packet and you ignore it. The semantics for future versions may change if the other side sends something that is not empty.

What this is implying is that you really expect version upgrades to be a linear thing? Not necessarily. By not specifying what the encoding of that version number would be, then it is equally possible to interpret this message as a fac.... we defer how that works to the future where it may or may not be needed.

Also, here you can optimize by combining one of these with the garbage authentication packet. In practice, the whole setup of key negotiation, garbage, and garbage authentication and version negotiation is 1.5 roundtrips if you combine as much as you can.

# Application phase

In the application phase, any future messages sent after decryption is handed to an application and interpreted as bitcoin p2p messages. We skipped over decoy packets though.... as soon as the encryption keys are established, everything sent takes the form of an encrypted packet. We will talk about what is next. An encrypted packet is an encryption of a variable length byte string, with a boolean flag for ignore. If it has the ignore flag, then the receiver just throws it away. We call those packets "decoy packets". Interestingly, this happens before the version negotiation phase. Even during the version negotiation, people can already send decoy packets to pad their data. We do not specify how and when to send decoy packets, but we do specify that a receiver has to ignore them. The minimum size of a decoy packet is 20 bytes.

Q: Can you jam another protocol into decoy packets?

A: Possibly.

Q: Max size of a packet?

The maximum size of the packet is 16 megabytes (60 megabytes?). In an earlier version, this ignore bit and length were sent simultaneously in a single 24-bit field so there was only 23 bits for the length. The ignore bit is not part of the length, for reasons of security. Really only the length should be there. We can go up to 16 megabytes, but really you shouldn't do that.

Q: In version negotiation, does that apply to the application layer as well?

A: Purely the transportation layer.

Q: So another application layer version negotiation can happen?

A: The notion of version or verACK none of that changes. The only thing we have is that the command message to the 12 bytes gets abbreviated to 1 byte by having a table that specifies a mapping for common ones.

Q: So the distribution of the packet length is controlled by the application by the garbage?

A: The garbage is just for the public keys. It's a one-time setup thing. After the first 64 bytes, there's up to 4 kilobytes. After that, there's decoy messages you can use instead of varying the length.

Q: Is there a reason you use decoy packets instead of having extra bytes to ignore after each packet?

A: It's similar.

Q: Could the decoy be used to leave a signal like if you want to poison these channels?

A: You can in fact.. the encryption mechanism we use does permit choosing the ciphertext if you don't care about what the corresponding plaintext is. This can be a benefit, or a curse. So someone could use it to make the protocol look like something else. The benefit is that someone could use this to make the protocol look like something. We believe it may be possible to create a valid but somewhat weird TLS v1.3 stream that is actually bip324. It would be cryptographically indistinguishable from TLS v1.3. It would look like a potentially valid TLS v1.3 connection. To emulate TLS, one thing that you could do is just run with TLS, but that comes with all the downsides of all the certificates and such.

# Packet encryption overview

One special feature of our protocol compared to other secure channel protocols is that we want this entirely pseudorandom bytestream. In other protocols, they usually have the packet length on the wire. When you start to send the package, the receiver doesn't know when to stop reading and decrypt. You need a means to communicate to the other side where does my packet end. If you look at TLS, they send a length prefix and then the plaintext. An alternative is to send the length encrypted and authenticate the length. I believe that this is what the lightning protocol uses. This is pretty expensive because now you are sending a couple bytes to encode a length, and then a 16 byte authentication tag on it. We argue that because of the nature of the bitcoin p2p protocol which is largely query-response based, a lot of messages in the p2p protocol will trigger an instant response from the other side, and so we try to argue that authenticating the length doesn't help.... Well, first, authenticating the length is not necessary as done by lightning because anyway the length is authenticated visibly. If you send a length packet that says the following encrypted and authenticated package is 16 bytes; if you modify this to 15 bytes they would read that, try to decrypt, and fail, so it's implicitly authenticated so you don't need to add authentication to the length.

What do we hope to achieve by encrypting the length anyway? From the perspective of a passive attacker, it's simple. We want something that is uniformly random. It doesn't need any authentication at all because a passive attacker can't modify that. But what are we trying to hide from an active attacker? We can hide lengths from an active attacker. An active attacker even one that doesn't change any of the bytes could trickle them like receive a packet from one side and then every second release one byte of it and wait until a respone comes, and a response will come as soon as the packet is done. This is how an active attacker can figure out the length. Our stance is that it is impossible to prevent an active attacker from learning packet lengths.

Q: In something based on UDP, when you say trickle out the packet byte by byte what you're saying is take TCP packets and re-shuffle them around. This discussion might be different on UDP.

A: That's true.

Q: What if instead of the decoy packets, we have the extra length and we wait until that extra length is received in order to defeat that.

A: I think what you're suggesting is that every packet would have two length fields. One legitimate length and the other would be padding length. Then you would only respond after having received both and authenticated both. The downside of that is that for someone who does not want to use decoys, this is extra data. For someone who wants to use decoys, it's less because now you can have decoys as little as 3 bytes or maybe even 1 byte rather than 20 bytes. And potentially at the start you can negotiate whether you want to use the decoys. There are many other possibilities like for example I could imagine an extension where you have a request-decoy feature where I send the packets that ask the other side to send the decoy in return. Exactly because the protocol is query-response based, this has huge red flags for- you really want strong protections against hey send me a megabyte of decoy data constantly hitting your node.

Q: Is there ever a situation where the attacker is looking for a repsonse to a packet, you can always send a decoy first, and once it trickles through you then go and act upon it. Sometimes you might want to send a decoy without a packet. I might want to go and send a decoy, and then pretend to reply.

A: Yes, that's a good argument for why you wouldn't want decoys just associated with legitimate packets. Because sometimes you just want to send a decoy. But what you could do is send a packet with outter length 20 and inner length and say... 0 is ignored. Yes, that's fair. It's just a generalization of the ignore mechanism. But it has two byte extra cost. It's an interesting idea.

Our design is largely based on the OpenSSH ChaCha20Poly1305 cipher. You take ChaCha20Poly1305 from the RFC. A lot of protocols use it. You use this to ... there is one header byte that includes the ignore byte and some reserved bits, and then the payload. Then we take this thing, and prefix it with a length, with an encrypted length independently. And also an independently derived key just to make sure that if you are creating a decryption oracle from this, because it's not perfectly..... The highest priority is confidentiality for all the data sent on the wire. Noise uses it. WireGuard uses it exclusively. TLS uses it. SSH uses the two different keys trick, but not TLS. You can use a separate key for the length encryption, we took that idea from SSH but modified it a little. What they do is take two encryption keys  .... but then their authentication tag is computed using the contents key but it covers the other one so they don't have this perfect separation and for our design we can argue you can think of this as two separate layers. The first layer is to encrypt the content with a completely standard authenticated encryption content, and then prefix the encrypted lengths to it. That's why we generate the two keys at the beginning. Another thing is that their protocol is smaller because for the length encryption they use an entire ChaCha call. So they generate 64 bytes of random bytestream and take 4 bytes of it, which in our case would be 3 bytes and throw away the other bytes, which is not a very efficient use of random bytes.

Q: So compared to original BIP, the crypto merged about 2 years ago is unchanged. So there's no new crypto?

A: Well, we do specify what has changed... the length encryption has changed. But we already merged ChaCha20Poly1305. I'm not sure what's in the Bitcoin Core codebase. AEAD was merged. We still have those. Were layers on top of those that used to be there and those additional layers are changed.

# More

There is a nice diagram for the entire handshake protocol. We have the XElligatorSwift algorithm here. This is how we derive secrets. We also have a naive python implementation. The specification goes into the design decisions without specifying everything to the byte level, but the pseudocode handles all the details.

# Application layer message encoding

Instead of sending ASCII strings like "version" or other things, we have this table for message type IDs. We send one byte and if that byte has value 1 through 12 then... if the value of the first byte is between 1 and 12 inclusive, then we treat that many bytes that follow still as an ASCII string because someone might need to send something not in our table. Another BIP might introduce a new message. This could add another byte in the table. So why ASCII? We could get rid of it entirely... but this is for compatibility with.... There is a question of coordination. Will we be able for every future BIP that introduces new messages to uniquely assign a single byte ID without coordination problems? I think that's likely we can do that, I'm not convinced though. The fallback mechanism exists that if someone has a private extension which hasn't been allocated a number or whatever, you can still use that. I feel like you could just define one byte as meaning that, so that you can save 11 bytes. You could do that. If you see this 1 byte, then read the length and then read the ASCII message. Another approach is to send your table. For service bits, you could define a range of service bits for experiments and if you pick something hope it works. We left the message table in for bikeshedding. You might notice that the message table is mostly ordered alphabetically except the bips which were added later if you notice.. Maybe the message type should depend on what the message length is. We could do that, that's the PHP trick, right? The lookup table based on the byte and the last byte based on the length of the command which is why early PHP commands are weird. It's true that it works, and we could make the lookup table be based off of the encoding byte and the length.

Q: Establishing a channel that is encrypted and authenticated sounds like a simple idea, but historically this often goes wrong. These other protocols often have real authentication that is only ephemeral, but you also have this additional requirement that you want the bytestream to be indistinguishable from random. Why do you think that whole thing works? Does the BIP make clear which parts are standards stuff and perhaps even have a security proof and stuff, and which parts are custom?

A: It might be easier to answer the second question first. I think the standard stuff, all the symmetric stuff is very standard. The core encryption things. The key derivation is standard. Except for the length encryption. Here we argue that if this fails, we still have the inner part, and it's pretty easy to argue about that we haven't written out a proof but other people have looked into hiding length. There is literature about this called "bondable hiding" about hiding the number of packages in a stream. This openssh thing has been proven secure, and we deviate from it, and we argue the deviation is tiny. We would like to see more research into that, but I'm confident enough that our modifications are fine there. It's good to know that the openssh stuff is known to be secure.

The other part where we have new stuff is like Elligator stuff. The only real security property is the pseudorandom bytes.. if this really fails then we fail at establishing pseudorandom bytes, which is bad but not the end of the world. The other property from ElligatorSwift is that it's a correct encoding. You don't need a security proof for this, you can just write tests. Take the equations for encoding and substitute them in for decoding and you will see if it works.

About the uniformity part... ElligatorSwift paper has a proof that sets a bound on how uniform it is. I did exhaustive testing for small curves to verify their bound. It works. It is way better than their bound says it should be. It is also better than ElligatorSquare. This is hard to make formal but it is a function of 64 bytes mapping to a single x-coordinate. So it's mapping 64 bytes to 32 bytes in a non-trivial polynomial rational functional way. It would be like extremely hard for it to be non-uniform. Even if it was maybe not quite as uniform as the paper proves it, even if their proof is ... I would have a hard time being convinced that it is not uniformly because mapping something real bigger to something smaller....

Are you picking 64 random bytes and getting a key, or are you picking a key and then deriving 64 bytes? No, you pick the first 32 bytes and you figure out the second 32 bytes should be such that it encodes your target key. Because you're starting with less than 64 bytes, I assume there is some computational attack where you can do a lookup attack of every single key. It's 2^512 table... but from a theoretical crypto point of view, this is a vulnerability. No. You're mapping 32 bytes to 64. There's additional randomness going into it, though. Given a uniformly random public key as input, the output of the algorithm is actually a uniformly random 64 bytes. Because you are adding more randomness? So it's not a deterministic protocol. Okay, that's fine. But it could be. You could use the private key as your randomness for the encoder, and interestingly there are only 2^32 encodings but it's still computationally indistinguishable from uniform.

There are secure channel protocols that have historically failed. There are a lot of places, like maybe in authenticated encryption. I hope literature community has understood that we know how to do authenticated encryption now. Another place where those fails is a lot of state complexity and a lot of state machines like the wrong state of the connection or something. Here, look at the protocol and convince yourself that it's simple. We tried to avoid having high complexity from TLS like where it can do session resumption and different forms of authentication. We don't have a notion of cipher suites because that's a huge source of boundary attacks. No sense of cryptographic agility here. Some of these questions become more relevant once extensions are added; say you have post-quantum key negotiation added and now you maybe have to wonder about an attacker that can trigger a downgrade into not doing that. Right now there's no room for negotiation of connection parameters.

# Adding authentication

Q: Could you briefly outline how you would add authentication?

A: Maybe we should do that later, after the session. This has been a long session.

Q: Is it defined how clients and peers treat undefined message types?

A: It's the same as... it's disputed right now how it is handled. The libbitcoin people terminate the connection. Our BIP does not address this. You treat it as a message that you don't know. Maybe you should throw in a message saying unknown message types should be ignored. Bitcoin Core ignores them. libbitcoin does not. There is some dispute about it. btcd since recently I think... they changed it to at least before the verACK they ignore unknown messages now. Someone just wrote up a BIP to ignore everything before verACK. btcd will ignore it because it's a message unknown. Compact blocks are not implemented in btcd.

I don't think we should go into that, really. The question of how to handle them seems to depend on whether you're before or after the verACK. I think that our transport encryption BIP shouldn't have a notion of once we hand it off to the application layer.... but before you can hand it off, if you get an undefined message type number, how would you even translate that to the application layer? Ah, that is fair. We should probably specify how at least with respect to, the possibility would be treated as an unknown message, or disconnect, or ignore. That is indeed a separate question from how do you handle unknown messages in general.

I think this question should really not be a concern of this BIP. The changes we do here in the message type table... if you change the entire underlying thing, it makes sense to put the change on top of it because you need another negotiation mechanism to switch to something like this.

Q: It might help if this BIP could be split into a generic packet relay scheme, and then the bitcoin parts. Someone should write up a rust library that just exposes this interface and absolutely nothing else.

A: The only reason not to do that is because the application side of it is so little that it would be a very thin BIP. I'm not opposed to splitting it up though.

Q: Can it carry messages for different applications?

A: So lloyd, who was involved in the design process earlier on, wanted that property... we don't have that, but it would be easy to add because we have this header byte now where you could define a bit in the header byte and say this is.... The property he wanted was that you could have one connection and then multiplex messages from multiple applications through that. That is relatively easy to do with this header byte mechanism where you can define a bit.

Q: If you have a fully authenticated connection, you might want to do JSON-RPC over the same connection.

A: I think there are reasons why you might not want to do that because JSON-RPC you never want to do unauthenticated. If it's persistently authenticated, okay, that's fair.

[countersign-section-on-another-transcript]: https://btctranscripts.com/bitcoin-core-dev-tech/2019-06-07-p2p-encryption/#countersign-a-secret-authentication-protocol
[Elligator-swift-paper]: https://eprint.iacr.org/2022/759.pdf

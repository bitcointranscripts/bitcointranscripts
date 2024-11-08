---
title: P2P Encryption
date: 2019-06-07
aliases:
  - /bitcoin-core-dev-tech/2019-06-07-p2p-encryption/
transcript_by: Bryan Bishop
tags:
  - v2-p2p-transport
  - bitcoin-core
---
<https://twitter.com/kanzure/status/1136939003666685952>

<https://github.com/bitcoin-core/bitcoin-devwiki/wiki/P2P-Design-Philosophy>

"Elligator Squared: Uniform Points on Elliptic Curves of Prime Order as Uniform Random Strings" <https://eprint.iacr.org/2014/043>

# Previous talks

<https://btctranscripts.com/scalingbitcoin/milan-2016/bip151-peer-encryption/>

<https://btctranscripts.com/sf-bitcoin-meetup/2017-09-04-jonas-schnelli-bip150-bip151/>

# Introduction

This proposal has been in progress for years. Many ideas from sipa and gmaxwell went into bip151. Years ago I decided to try to move this forward. There is bip151 that again most of the ideas are not from myself but come from sipa and gmaxwell. The original proposal was withdrawn because we figured out ways to do it better. Since people have started to implement bip151, I decided to not alter that proposal because it would end up with confusion.

So I have proposed v2 message transport protocol for the p2p network. This is a one-time chance to do things better, I think. I don't want to call it "p2p encryption" again because it has opportunity to do much more than just adding encryption.

# Goals

The goals are again to add opportunistic encryption; sometimes I regret not adding an authentication scheme into that proposal because people are still not super happy with the possibility of man-in-the-middle attacks. But it's a building block, and including everything into a proposal makes it too complex and there could be multiple authentication schemes and maybe picking one is not the best idea.

It's also an opportunity to optimize the protocol. The goal isn't like censorship resistance.  It's just opportunistic encryption, not for censorship resistance. It has some nice properties of solving passive observers, but other than that it's more of a building block. Also, eliminate non-detectable message manipulation.

# Handshake

Let's go over how it works. Here's the simple overview. The current proposal is that an initiator sends a 32 byte pubkey without any message header or anything else, it's just pure 32 bytes to the responder. The responder reads the 32 bytes and then detects whether it's a version 1 message magic, and does it start with the version of the magic. If yes, then it's a v1 protocol handshake then it continues with v1 because we still want to use v1. If it's not containing the magic in the version, then it treats the 32 bytes as a handshake. Then it does an ECDH, then he sends back his public key, and then on the other side we do ECDH and have a shared secret.

Q: Aren't public keys 33 bytes?

A: Yes they are 33 bytes in general. We use only odd pubkeys, though. Why? Good question. Censorship resistance is not a property. I think gmaxwell came up with the idea to say okay, if we use a 32-byte only on pubkeys then it looks random, it's not random but it looks random. It's not as easy to identify. You can't do naieve traffic analysis anymore. You could do more advanced traffic analysis, but it's not just "match these bytes, oh it's probably bitcoin". The handshake otherwise would always be obvious to observers.

Q: What's the more advanced traffic analysis?

A: You would be able to see if there's many connections from a single IP, and maybe all of the 32 bytes are good ECDSA curve x-coords, and if they are all valid coordinates then it's more likely that it's using this protocol.

Also, pubkeys are not allowed to start with magic, otherwise we would break backward compatibility. We do the handshake, and then it uses symmetric encryption. ECDH is also something that is already available in libsecp256k1. We do ECDH with our current secp256k1 curve. It's not new crypto in that sense.

Q: Instead of sending an x-coordinate, just send randomness and hash it up?

A: You can encode a public key in 64 bytes and then it really looks like random. I'm not sure it's worth it to do that, but it could be done. Allocators, right? Yes. Let's talk about that later. It's probably not worth it because there's so many other traffic analysis things you can do that are trivial to identify bitcoin traffic, like all the messages being roughly the same size or predictable sizes. You would have to send a constant stream of data or something. The biggest traffic analysis is looking at the size of packets and the timing and correlation of packets between nodes. Unless we're going to add in garbage packets to make the bandwidth look constant, then there's not much you can do there. This is not something that would be in Bitcoin Core but maybe something else on top of Bitcoin Core. Well then we would be the only application with constant bandwidth...

# Custom AEAD construct

Once you have a shared secret after the handshake, the proposal is to use ChaCha20Poly1305 for symmetric encryption, a custom AEAD construct. ChaCha20 is the stream cipher, and Poly1305 is the MAC. Also, some devices have hardware elements that do these instructions. ChaCha20 is merged in Bitcoin Core and Poly1305 is merged.

# Message size

Q: What about the performance between that and hashing the full message?

A: That's a good question, let's skip forward to that. I gathered some traffic over a 24 hour period on a standard node, that means serving blocks. No changes to configuration parameters. There, we can see that almost more than 1/3rd of messages sent are below 64 bytes. So what I want to say with that is that most of the messages are very small, and more than one third is below 64 bytes. So it's worth optimizing for small messages. Prune peers it's a bit less. Is this because pruned nodes don't serve merkle proofs? INV just shoots out... for now. That's just btcflood.

Why is blocktxn so much for Bitcoin Core send message bytes with prune during a random 9 hours? This was a long-running Bitcoin Core node. This is sent bytes. So you could be talking to a peer that doesn't have a good mempool. Block reconstruction fails all the time, and if it fails then it's going to be a lot of bytes more than compact blocks, so that ratio could make sense.

Do we have these numbers in getnetworkinfo? If you disconnect from a peer, they are just gone. This is from debug log.

So, it's clear that we have a lot of small messages.

# AEAD performance

There's an IETF proposal of ChaCha20Poly1305 which is good, but then OpenSSH took that proposal and improved it by encrypting the length field. The IETF proposal has the length unencrypted and it's very easy to identify packets. You can't pad with random data, it's a bit more straightforward. So OpenSSH changed it a bit and made encrypting the length be a part of the AD field. We took that and optimized it further for small messages, which is only a slight change. The change is visible here....  This is the openssh version, there's a handshake, there's two keys from the handshake, there's one ChaCha20 round, and then we derive the Poly1305 key, and then we do n ChaCha20 rounds for encrypting the payload. A ChaCha20 round is always 64 bytes so you need to do it anyway. So you would throw away 32 bytes of the Poly1305 key... but for each message, we do a ChaCha20 round for just encrypting 4 bytes length. So we don't use 60 bytes of a computational part, it's 4 bytes AD. In Bitcoin Core, we reuse that stream, so we can reduce one ChaCha20 round for a 64-byte message, or we only have to do it once every 21 times. The weird thing in ChaCha20 output is that it has a variable number of variable length blobs that come out. There's an IV that counts which message you want, and then there's a counter for the bytes within that. It seems that in ChaCha20Poly1305 OpenSSH one, they basically don't use the fact that all of these messages are variable length, they just generate the new message and use the first bytes. That seems simpler to treat ChaCha20 as a stream cipher and use the bytes that come out. The strema cipher is nice, it just stores the plaintext actual string position and you could calculate it upfront when you're not using the CPU and then store when you want to encrypt. You can use unused CPU time. This is the optimized version.

So what are the numbers? Again, I haven't done thousands of queries. It's just one. I used an x86 i7-8700, and another on AARCH64. I compared hash (the existing double hash), bitcoin, and OpenSSH. The current version is 4 bytes checksum in every message, and the checksum is calculated by double hashing over the whole message and then truncate the whole thing to 4 bytes which is not super fast. That's why we can make the protocol faster by adding encryption, which is hard to understand. But it's not always faster.

Hashing a one megabyte message takes more than double the time. So it's 3.8 milliseconds. What is bench reporting, seconds? Hashing a megabyte should be in a millisecond range yeah. Focus on the relative difference instead of the actual numbers. Encrypting a one megabyte message takes less time than using the hash method. On a large message, we don't benefit against OpenSSH. But on a 256 byte message there's a difference, and a 64 byte message has an even larger difference with OpenSSH and both are faster than the double hash method.

The alternative proposal would be, not encrypting and dropping sha256. I don't think that's a good idea. It has been floating around on the mailing list though.

For the performance, you can cache 2 MB of stream, for block propagation. I think in general using ChaCha20 has a lot of potential for optimizing in the future.

# v1 vs v2 message structure

v1 message: 4 bytes net magic, 12 bytes message command, 4 bytes length, 4 bytes double-sha256 checksum, variable bytes payload, and it's at least 24 bytes total.

v2 message: 3 bytes encrypted length, 1-13 bytes message command, variable length bytes payload, 16 bytes MAC (message authentication code), and it's at least 20 bytes total.

If you want to send with v2 something that is larger than 8 MB, then you need to split it up into packets, which would be a good idea anyway. You have to do it anyway. So gigameg blocks, we chunk those out. We also move away from the 12 bytes message command and use a single byte zero-12 identifying the length, so if the first byte is between 0 and 12 then it means a length then the rest is a standard-variable length encoded value. If it's above 12, then we identify it as a short id, so 13 could be INV etc but that table still needs to be made. We can use a single byte for sending a command rather than a string. This is a general optimization that has nothing to do with encryption.

It's either 1 byte or 12 bytes. We don't want to eliminate string-based commands. If you're already going to have the optimization for most messages are going to be one byte, why not have a byte that says the next 12 bytes are command.  It's a bit different. That would mean you always have to send 12 bytes... No, you wouldn't ever actually do that unless you're sending a custom message. Can we not add more variable length stuff? What's wrong with variable length? This reserves 212 short IDs. Adding variable length stuff sucks, in general, in any protocol. This is an optimization you're not ever going to use, thus adding complexity to the protocol. So you could say 255 means the next 12 bytes are message command... This is not worth discussing. I don't want a parser that includes variable length command strings. I don't want to implement that. I really don't. I see the point, it's reasonable. We can discuss that further.

Using the v2 message protocol, it means messages are not larger, they could even be larger due to the short command ID.

Q: Do we really need a 16 byte MAC? Can we reduce that?

A: We shouldn't. I would prefer 32 byte MAC. Poly1305 is a well-studied MAC and it has 16 byte outputs.

Q: Well, I don't know anything about cryptography.

A: Me either. Let's send it twice! ((laughter))

We could say version 2 only supports INVs or something. But this brings special planning into this. The great thing with strings is that collisions are less likely to happen. Someone has to maintain the table of all the p2p messages. We already have a handshake and version negotiation. It doesn't matter if someone else is doing other p2p messages. We're not going to connect to those weird nodes anyway, right? If we use bytes only, then everyone has to update the BIP.

Does the length include the checksum and the type and all of that? Or just the name of the command? The length is only containing the payload, just the payload. So you will have to understand how to parse the type because I can't just skip it. Right? You need to read the first byte, and then you can skip the rest. I also need to support the variable length type. You need to read the first 4 bytes so that you know how many bytes to skip. The encrypted length may need to be the size of the entire packet, but there's concerns about having a padding oracle..... That's the reason why the length is encrypted by a different cipher, to avoid people being able to infer information from it by observing how you respond to invalid messages. We need to think about that. In the openssh version, the MAC is not included in the length-- sure, that's easy, but for the variable things... That's a good question. It should include the size of the message command as well. The MAC doesn't matter, it's constant-sized. But I think the length needs to include everything of variable size. So you can packetize your stream by decrypting your length fields and not looking at anything else. It must cover the variable length. You could encrypt the first four bytes with a special cipher but this is not ideal.

In v1, INV is a 61 byte message, and in v2 INV is 57 bytes.

3 bytes for the length, giving 24 bits. The most significant bit is used for triggering a rekey. So we can only use 23 bits. The one bit reserved triggers a rekey which means we need to use the next key for the symmetric cipher.

Longer messages could use multi-part messages, like gigablocks or whatever.

Q: Have you done any benchmarking on constructing the MAC?

A: It's in the code, if you run bench, it gives you Poly1305 benchmarks.

Q: So those graphs you showed included Poly1305?

A: They included two rounds of ChaCha20. It's not only ChaCha20, it's the whole thing, the whole stream cipher. It compares double sha against the AEAD construction.

Q: The MAC covers the rest of the packet?

A: The AD is just the encrypted length, and the MAC goes over everything including the id. It's the payload and the command, but yeah.

# Open questions

This is an opportunity to change the protocol. If there's other ideas then we should eventually work them into that proposal. I think we should call this "v2 transport protocol" rather than calling it encrypting. The question Tim raised yesterday is, what do we need to consider now so that we don't break future improvements in terms of when cryptography gets broken? Or downgrade attacks? Here, we start with sending a public key, but if it's a symmetric string then we fallback to v1, but now the first thing we send is basically random, so what if at some point in the future we want v3. How do we do that upgrade? At the moment it's not possible; send even keys? If we want to add another handshake, we could do that handshake first and then do a second handshake. We also have the service flag. We could add another port. We already support binding multiple listening sockets. The way to do it as an upgrade is if you want to do this v3 thing, then you first do the v2 handshake, then you negotiate using v2 messages to handshake v3.

At the moment, the proposal seems like a between wanting encryption and it should look like random data but not too much because we don't want to invest too much bandwidth. Usually protocols start with what we have at the moment, like a magic string, some version number, and now we have optimized that away to look like random, and we encrypt the length to make it look like random. IETF doesn't encrypt the length because they assume message length should be visible or doesn't need to be confidential. At the beginning we send an x coordinate, which could still be distinguished. I think we should either go for 64 byte public keys to make them really-- then the entire protocol looks like random data, except you can do traffic analysis like timing and length. Or we pad stuff. Or we say this is not a goal, and we can have another magic string, and we don't have to encrypt length, and have a version number. We should pick what the goals are.

There's definitely something in between-- there's a difference between being able to do trivial traffic analysis where you match on the first five bytes and knowing what it is, versus having to put in some quantity of CPU to figure out whether this is bitcoin traffic. This is a massive difference for many practical applications.

There's a few choices. Maybe we don't care about traffic analysis, maybe it's all random, and maybe it looks random to a CPU-constrained observer. I think the CPU-constrained observer is the most important threat model. As soon as the key exchange is done, everything really looks random, so why not take this low-hanging fruit of adding more bytes in the handshake? Well, they could just see your traffic spiked after receiving a bitcoin block and therefore you're running bitcoin.

In terms of upgrade, don't underestimate making a new port and having that be the new protocol. Otherwise you're doing TLS and start TLS. In bitcoin, there's no reason to not keep binding new ports for every single protocol we want. We could say 8336 we assume that's v2... What if people want to use a different port? There's no reason to not use a different port. If you can't bind 8336, you can't bind something else. If a country blocks 8333, you cannot start a new node. You do a DNS seed, everything is 833x, you can't connect.

You can do a DDoS by advertising a bunch of services, then all the nodes try to connect and make random connections to that service. I run a bitcoin node that uses a non-standard port, and it has literally never received a legitimate connection from a Bitcoin Core node. If you use the same port, then all this anti traffic analysis stuff is sort of worthless. You need to allow unique port numbers.

Would it be useful to reuse the upper 32 bytes of that Poly1305 round? For encrypting the payload? Only for creating the poly1305 key. We always throw away that 32 bytes. As long as you don't mix it with the other key; you need to keep the two things separate. ChaCha20 just gives you as many random numbers as you want. The openssh proposal is stupid throwing away those things... I think it was an implementation choice that reduced a couple bytes of state they would have had to keep track of, it's a counter for a message and that's all you need. It made it a little faster, but not substantially. I might try to implement something there.

# Next steps

ChaCha20 has been merged. Poly1305 has been merged. The AEAD construct has been pull requested. It has test vectors, it has bench, it is stable. It needs total review by cryptography people. It's not new crypto but it is a new construct. It's not like walking on a frozen lake, but it's still similar to walking on ice. Needs more review and to build up momentum. It has a full implementation. It works, although it's not good.

After the version handshake, you send the version message. After the crypto message, yes.

As an alternative to using the elegator square 64 byte construction, you could be permitted to send a number of non-valid x-coordinates before the actual x-coordinate and then you use a poisson distribution for this. You read 32 bytes, is it a valid x-coordinate, yay go, and if not skip it and continue. I think this actually looks random. The sad point of this is that you end up with things on 32 byte boundaries that are also identifiable. Why not elegator squared?

One of the properties should be that we have a dependency in terms of having external libraries or something..... I don't think that's necessary, and it also complicates.. not every project that wants to implement p2p protocols has the same resources to develop. We'd add it to libsecp256k1 if we do that.. Yeah, that's true. There's more concerns than just "can we implement it".

Making it look random is not that much of a goal, especially if we go to this effort and leave the port the same. It seems clearly a boneheaded move. This is what gets detected now. If you run on that port, you get emails. This is what gets detected for "I want to identify people running Bitcoin but I'm not trying to block people running Bitcoin". This is just a really easy step, you just block port 8333 incoming. If someone is trying to mess with bitcoin, that's what you do on day one, not on day five. Well, we need to have something else, then blocking it just works. If we care about traffic analysis at all, then the first thing to do is randomize the ports.

Well, then let's talk about randomizing the ports.

Tor is a good example. It solves censorship resistance for a bunch of applications. I don't think we want to include censorship resistance techniques. It's a layering violation. But we are, to some extent. If there's low hanging fruit, then we can do it. But changing the port is low hanging fruit. Well, then we should have a real version field or magic byte string, this makes it much easier to upgrade to future versions. I see, that's a good point. This was the entire story of TLS upgrade sadness and you have to convince the person that you are talking in the new protocol and go to enormous lengths to make messages look compatible or incompatible to certain versions. Having a version field can result in a downgrade attack if you don't do it in the right way.

Someone asked, if we do see an attack, would we randomize the port? Well, maybe you don't take the last step, but make it easily available, like making it an option. If I am internet gateway and I want to block internet traffic. I just block all the ipv4 listening ports. Port randmization doesn't help you when you have a small network. You need to name the attacker. What are you trying to mitigate? Comcast sending people emails because hey you have port 8333 open.. I've gotten emails from MIT about me running something on port 8333.

We don't want to have a new port number for this specific thing because people have to update their router to allow port forwarding. We should keep the port they are currently using, because it's hard to get people to open it. But we should have a feature for randomization to be used in the future.

How many nodes are behind NAT? What percentage of nodes are behind NAT? Most people when they run Bitcoin Core they don't open up the port and we turned off UPNP a long time ago. Luke-jr has some analysis of listening and non-listening nodes. Can't you use ipv6 for this? Europol said they would really like to use ipv6 so they can attribute copyright infringement to specific devices instead of just "somewhere in this home". Yeah it was my refrigerator.

When do you do the rekeying bit step? The AEAD with ChaCha20 in general you're never supposed to reuse the same key with the same nonce. You need to rekey when the nonce hits the limit and starts to overflow. That's the max. To be safe and to follow other protocol practices, you usually rekey after 1 gigabyte of data. It's also up to the client in our case. The client can trigger or initiate a rekey by sending that bit. That means both sides re-hash or just hash the current symmetric key so it's perfect forward secrecy. When an attacker attempst to grab the key for various reasons, then....

If the client doesn't do rekeying, what does the receiver do? If you flip the bit, then it means it must rekey. So if they don't do it, then you need to disconnect immediately. If the rekey comes on every message because of a CPU attack then you also need to disconnect.

Q: Why strip authentication out of this?

A: There is a form of authentication in the proposal. The proposal states that the clients or the implementations following the proposal must show the session id. The session id is currently an ECDH secret hashed into a specialized form into a string. That's after the handshake has been done. Each side can compare the session id. This is authentication although it's not practical, and you need to do that after every handshake with every peer is not practical.

Q: Would it be practical to HD-derive these pubkeys you present, like given this pubkey you know you're talking to this guy?

A: That's authentication. There's still bip150, which is an authentication scheme which is still valid with this proposal. The problem is, you need to understand how the current authentication happens. One way we do authentication on the internet is certificate authorities like TLS stuff. This doesn't work for bitcoin. The second one is the SSH form which is pinning down on first-use. I think it's also not something we should do. In ethereum, nodes have a public identifier. SSH does the trust on first use model. You connect, you get the fingerprint, you pin the fingerprint. If you have an attacker during that first connection then you're fucked I guess. Lightning publishes its own public key. In lightning, nodes have an identity, but in bitcoin they don't. You have to prove ownership of a travel. Electrum is trust on first use, too.

We could have multiple uathentication schemes. One is comparing session ids which is sort of stupid. Another is bip150 where you do out-of-band share of the keys. Then there's the scheme that Pieter came up with once that I sadly can't find the link for anymore. It's awesome. Anyway, there are many potential authentication schemes.

It would be interesting to use the lightning gossip system to connect bitcoin nodes. It's mixing abstraction. You can supply your own authoritative like, -- it could be external.

People complain that it's not man-in-the-middle safe, which is true. But we can't build everything at once. But this is more complicated than that; in bitcoin, we're generally talking about not just authenticated connections but also an identityless system. If you assume your attacker can spin up their own nodes that have as much identity as the thing you are trying to connect to, then they can spy on you. There's a weak argument for encryption: it rules out certain kinds of attacks, but we should be careful about stating what its advantages are on its own. I like how you talk about how it is a building block, not something that immediately solves the other problems. I also like that it's a performance improvement, although that's a low bar.

The blockchain data is public, but traffic is not meant to be public. This proposal doesn't make it private, but it's on the way. One simple attack is your ISP listening to your transactions. The ISP can do man-in-the-middle but that's extra work and maybe detectable or something.

The opportunistic encryption, if you're an ISP doing man-in-the-middle listening to a connection, I can listen without the user having a chance to detect it. But after that, there are session identifiers. The ISP must take the risk that its tampering could be identified. Just the risk on identifyability will convince them not to do that. But to make that argument, you must talk about authentication. If you only do encryption and nothing else, then the argument doesn't hold. You need to bring authentication or at least the option of authentication into scope as "why encryption itself is useful". The absolute minimum for that is a session id, and that's enough for a security researcher to catch a big ISP doing it. Also, ISPs must calculate that there might be a covert authentication form not published because we obviously want to detect ISPs doing the wrong things.

The biggest threat on the internet today is pervasive monitoring, and encryption makes it reasonably difficult for CPU-bound attackers. If you're running a service that is using an encrypted socket, I can just connect to you and now I'm your peer anyway.... This makes traffic analysis take actual effort.

For encryption, you have to be in the middle. Perasive monitoring generally means you're not man-in-the-middle you're just monitoring packets. You can only decrypt if you're the peer or in the middle. If you're an ISP, you can install something on the router to listen to the traffic, manipulate packets, observe packets, no cost, no handshake nothing. But if you want to man-in-the-middle this protocol, you need to actively intercept the handshake and fix up the keys, track each peer, it's way more complex to do. Imagine you're a surveillance entity where what you get is a live dump of packets across the internet.

# Countersign: a secret authentication protocol

<https://gist.github.com/sipa/d7dcaae0419f10e5be0270fada84c20b>

The bitcoin network is mostly consisting of identityless peers. But there is identity in the form of "I have a trusted peer with this IP address". That is a form of identity. It's a horrible easily fakeable one but it is used. Like I have a VPS on my phone and I'm going to configure it to connect to that IP address because it's a node that I trust. The nice thing you could do if you had an authentication mechanism that is where you could query someone hey are you identity x without telling them what x is, and so, they don't know what they are being queried for and they don't know whether they are successful at authenticating. It is possible. It sounds impossible, but it is in fact possible. What you do is you always run this authentication protocol over every connection. If you don't care who the other peer is, then in 99% of the cases, you say you run the protocol with a random key and he won't know what is being asked for and he responds in a way and you learn that of course he is not because you did a random public key and you ignore it. But when you do want authentication, you query for the right key, they still don't know whether they are, but you learn yep I'm connected to the node I want. A nice thing is that a man-in-the-middle cannot distinguish between these two scenarios. They can't tell if the other party is--- well, they can tell after disconnect because they had the wrong key. Maybe you shouldn't disconnect. It depends. Generally you want to keep a connection open and treat it as a random connection. The man-in-the-middle always has the ability to see well, if authentication is optional at all, we're only going to run the authentication protocol some of the time, the MITM can just say I'm going to intercept every connection and hwen I see an authentication attempt I am going to disconnect and blacklist these two IP addresses and not interfere anymore and this probably won't be detected. But if you always run the protocol, they only have either the option of dropping every connection or being detected. You know the identity key of your server, so you can configure it on your phone to connect to that one. But there is no observable identity for that server. You're just not publishing the public key. The other peer knows it. It's unobservable. It's not possible to leak it unless you give the key to someone. Also, you should not reuse identity keys-- well, it shouldn't matter because you are only using this protocol for yourself not to connect to peers. It's a zero-knowledge protocol, an observer learns nothing. This is not bip150. In bip150, if you have a failed connection and later learn the public key that you could have connected to, you can correlate those failed connections with that public key. But here in this proposal you learn nothing. It's a query, are you key x but it's a randomized-- it's two points that go over the wire and they look random, and there's a response which is you take those two points and your private key and you get two points back which look random to everyone except someone who has the corresponding public key.

# Post-quantum

I think PQ is too much for this proposal. I think adding post-quantum makes no sense. It makes sense for tor because if I communicate something today it might still be secret in 20 years. There's probably people collecting lots of tor data now in the hopes of decrypting it in 20 years. If there's an easy and obvious way of adding post-quantum then you should do it. If you're CPU bound you do timing and bandwidth analysis anyway, so you don't gain much from adding post-quantum.

One thing that would be useful is a version field or some way to upgrade for post-quantum in the future even if a solution is not included in the proposal. If we add post-quantum now, there is no way we can make that look totally random as far as I know. There might be a way you can. Maybe you can, I don't know.

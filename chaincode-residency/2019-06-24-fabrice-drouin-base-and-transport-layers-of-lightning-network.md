---
title: Base and Transport Layers of the Lightning Network
transcript_by: Duncan Dean
tags:
  - lightning
date: 2019-06-24
speakers:
  - Fabrice Drouin
media: https://www.youtube.com/watch?v=wyri7cc83kQ
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-24-fabrice-drouin-base-and-transport-layers-of-lightning-network/
---
Location: Chaincode Labs Lightning Residency 2019

Slides: <https://residency.chaincode.com/presentations/lightning/Base_Transport.pdf>

## Introduction

Fabrice: The base and transport layer, almost everything was already introduced this morning so it's going to be very quick. So have you visited the [lightning repo on GitHub](https://github.com/lightningnetwork/lightning-rfc)? Who hasn't?

Okay, good. So you've seen all this? That was a test.

We've covered almost everything this morning. I'm just gonna get back to the base protocol, BOLT 8 and maybe BOLT 9 because I don't think it's been mentioned a lot.

Basically this is the kind of communication we have in lightning. You have a transport layer that encrypts and authenticates messages and then you have a base layer that describes what kind of messages you actually use and the two can be cleanly separated.

The base protocol has been shown this morning so I'm gonna be very quick. It's a custom binary format. The max size of a message is 65 kilobytes and basically you have a type, 2 bytes that tells you what kind of message you're dealing with and a payload and a payload depends on the type. The old messages and the one we use today uses custom encoding, which is a bit hard to extend and the new messages that are going to be introduced hopefully within the next few weeks use TLV encoding which is much nicer to play with and extend. I'll explain what TLV means now.

## TLV encoding

TLV encoding, it's a generic type-length-value encoding that you find in a lot of protocols. It's something that you find in ASN.1 for example. Who knows what ASN.1 means? Okay you're very lucky. ASN.1, it's something that is used in - yes. It's ugly as hell but it's an example of TLV.

TLV record means you have a type in our case it's going to be a Bitcoin VarInt, a length, again a Bitcoin VarInt, and a value, it could be anything and it depends on the type. And you have TLV streams -- that are just a bunch of TLV records all put together. In lightning, we added additional rules like records are sorted by type and you can use a specific type only once in a TLV stream. The good thing about TLV encoding is even if you don't understand a specific field you can skip it - you can just read its length and skip over the field. It's not possible with the messages we have currently in lightning so if you don't know how to decode them you're stuck.

Audience member: [Inaudible]

Fabrice: Probably, yes.

## Transport Layer

The transport layer, it's been described this morning. It's based on Noise. Each node has a unique private/public key pair. The node ID is your public key. There's a handshake phase in Noise, so you authenticate that the node you're trying to talk to is actually - I don't know - that node has the private key of the public key it's using as an ID. And once you've performed the handshake - once you've checked that you're talking to who you really want to talk to - then you do have encryption keys, one for inbound traffic, the other one for outbound traffic. And then everything is encrypted using these encryption keys, which will be rotated every five hundred messages.

Transport layer is in charge of handshake - you really check that you're talking to the node you're supposed to talk to - and then you decrypt packets that you pass to the application layer. So that's it for the transport layer.

Do you have any questions?

Audience Member: Why 500? I mean, how was this number chosen?

Fabrice: Oh, because we want to rotate keys every five hundred messages and keys are used twice for every message so that the keys are rotated every 500 messages. You use the keys to decrypt the length and then to decrypt...

Audience Member: But why 500? Why not 200? Why not 5,000?

Fabrice: I don't think there's a specific reason for that. You want to change the keys too often and I guess 1000 is...

Audience Member: I don't there's any reason for a specific amount. There's the birthday attack, so the amount of nonces is divided by two, and then just every couple...
something that sounds reasonable for the protocol. If your protocol sends thousands of messages every second you won't want every 500. If your protocol sends one message per second you'll want every this...

Fabrice: One cool thing you can do with lightning is you could basically isolate this and have your implementation work with any text messages and build like a front that is in charge of encrypting and authenticating messages that is separate from the rest of the application. It's something we're thinking about.

Audience Member: I would actually really like that because I'm running the integration tests and they're hell to debug with the encryption layer intact.

Audience Member: So is the key exchange here, is that also Diffie-Hellman?

Audience Member: We use Diffie-Hellman here and for the HTLCs.

Fabrice: Yes, for completely different reasons, but the handshake phase in Noise uses Diffie-Hellman.

Audience Member: Then every 500 messages you go through the same process?

Fabrice: Basically, you increment an index and you have new keys.

Audience Member: Is that like HD?

Fabrice: No no, it's not. It doesn't look like a BIP 32 derivation; it's something else.

Audience Member: It's the ChaChaPoly that Christian mentioned, so it's basically this random generator that is XORed with your messages and the random generator has a certain seed value and this is just increased basically. And this creates a new pseudo-random stream. That's why it's also important to know that it's every 500 messages because both parties have to exchange keys at the same time.

Fabrice: If you have an off-by-one error in your application, you won't be able to understand the traffic after the first key rotation.

Audience Member: Would that happen - off-by-one?

Fabrice: It did happen I think, the first few weeks but not anymore.

Audience Member: So there's no handshake to say “Hey!” we change key now, we just change it?

Fabrice: Yeah.

Fabrice: Something that was mentioned this morning also, is a payment request we use in lightning. So, basically it's a way of encoding payment details like hash, amount and expiry. You can add metadata like description of what you are actually buying, and you can add routing hints. That is, suppose your channels are all private. It's impossible to reach you because nobody will see your channels in the public routing table. So you can add hints - I'd say okay use a channel I have to a node that is in the public routing table to get to you.

This is what we use on Eclair. I don't know if some of you use the Eclair wallet, but all the channels it creates are private so you won't see them on explorers. So if you want to receive money there is no way to find you, so we use routing hints in a payment request you generate when you want to receive money to make sure that you can be reached.

This is also very useful if you're a merchant and you don't want for some reason to publicly announce your node because you're a terminal node - you will not be routing payments, you're like the end of the way. All you get is incoming payments, not outgoing ones. It doesn't make sense to make your node public; it's useless from a routing point of view. So you will also use routing hints to receive payments.

And there's something that was mentioned really, really quickly this morning a lot. It's how we assign and use features in lightning. So this is about to change, but right now we have what we call them local features - features that are local to the channel you have with your direct peers, and global features - features that are global to the network, and for example that you would need to know about if you wanted to use nodes that have certain properties. Suppose we change the onion formats and not all nodes support the new onion format, then you will need to select nodes that you know will understand the new onion packet. There are no global features assigned yet.

The local features that are defined today in lightning are data loss protect. So when you reconnect to a peer when you've been disconnected, you exchange what we call channel re-established messages and they say, “okay the last point I have is this one the last secret you send me is this one.” If you've fallen behind, for example, if you have lost data or your disk crashed and you're using an old backup, it's very risky to keep on going because you will probably publish an old set and lose your money. So if the node you are connected to is nice and supports a loss protect option, they will give you the points that you need to dispense your outputs from the detection that they will publish. So it is something that is called I think by LND “static channel backups,” but it's not really backups because you still need the other guy to do something for you. The data you have locally is not enough, you need the peer you're connected to publish their current commitment transaction and then with the information they gave you you have enough to spend your remote outputs. You have enough to recompute the key the remote outputs sends money to.

Audience member: What if they lie? If they don't send you the current state but an older state?

Fabrice: Basically, it's something that is supposed to be a last resort. If you know data you have no money, so it's an extra change to get it back. Suppose you lie and you say ok that the last point I remember is an old one and you basically haven't lost data. It's very risky for the peer you are connected to try to cheat because maybe you have not lost your data. And if they do that they will lose everything. So it's a way of making sure that you can get your money back if you've lost everything. Basically, to get this to work you need a very limited amount of data that you can know once you've created the channel.

The second option is initial routing sync, it's what Christian said this morning. Basically, it says send me everything, all the routing information you have. It's not used anymore because it's that the routing information is just too big.

Audience member: [inaudible]

Fabrice: No, it's because you need to generate blocks. Then it would be notified that new blocks have been known. I think everyone is using the zmq classifications. What are you using?

Christian: We poll for blocks.

Fabrice: Okay, but whether it's polling or using zmq notifications it's not really instant. It takes a few seconds before you get the notifications.

Christian: So even in that case, since there are denial of service concerns, we implement what's called a staggered broadcast. We queue up changes in our local buffer, deduplicating them, and only after a minute or so do we flush them to our peers. So that means that I can bombard you with channel updates because, well, you can actually do that. But since I buffer them locally and deduplicate, only the last one will actually reach beyond me, to the rest of the network. So that’s how we throttle your broadcasts in the network. So that's how we throttle your broadcasts in the network, but that also means that your update will actually be delayed by the diameter time one minute. So that may be the case there. So what we have is in the Deaf mode for c-lightning, for example. We simply set this staggering mode to a second or so, and then it probably takes like a diameter number of seconds...

If you compile it with `developer=1` you can do.

Fabrice: So the next option is `option_upfront_shutdown_script`. Basically, what it says is as soon as you open the channel, you're gonna tell it to use your what's public key script for the final closing transaction. It's an option that's useful because suppose your node gets compromised and someone takes control of it to get you to steal your money. It's very easy. You close the channel and send everything to the hijackers address. If you use this option, what it means is, even if somebody takes control of your node and makes it initiate a closing transaction. That closing transaction will send money using the public key script that was defined when you see that control of your node and that it's supposed to be much harder for the attackers to steal funds from.

And the last option is `gossip_queries`. It's more sophisticated gossip control. It is still pretty basic, but basically it's a few queries. (I think it's gonna be explained in detail some more.) You can use them to synchronize your routing table much more efficiently than just, “send me everything.” This is something for which there's an open pull request to extend it further with timestamps and checksums. Basically it's a way to very quickly get the information that you're missing so that you can start finding paths for payments very quickly when you start.

That's the last item today.

[applause]

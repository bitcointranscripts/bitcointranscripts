---
title: Ipfs
transcript_by: Bryan Bishop
---
I will not have time to describe IPFS. We have multiformats that allow protocol agility, interop and avoid lock-in. Multihash, multiaddr, multibase, multicodec, multistream, multikey. What do you do with cryptographic hashes? When you have four different hashes all the same length that happen to be coming from different functions, what are those functions? sha256? sha512? sha3? blake2b? How do you know which hash type it is?

The problem is that the values aren't self-describing. There's usually no way to pack the values out of band when they were not designed for that. Think about what git is going to have to do to switch from sha1 to sha2. So you need some encoding to prove something about the hash itself.

Multihash makes sure that the value is part of the digest. It should be encoded in the same way as the value. The self-describing thing should be part of this. It's a simple format. You have a notion of a length, because as I showed before, these are all 256 bit hashes which means some are truncated and you want to take that into account. The codes are in the value itself for multihash. No assumptions about what the hash function you are using now or using tomorrow will be.

There are a bunch of implementations in many languages. People are already adopting it. Like multihash there are other protocols, like multiformats used by a whole bunch of different systems, coming out of the IPFS project but yused by a bunch of other things.

multiaddr shows a number of different ways to express addresses like /ip6/::1/tcp/80/http. It improves human readability, but also has a binary-packed version which is very efficient. The goal is to create very small formats that is uable across a number of systems iwthout having to lock yourself in.

IPLD, libp2p, etc.

plan9, torrents, git, bitcoin, they are all distributed authenticated data structures. IPFS is a forest of hashed data structures with merkle trees. The goal is to move around these different kinds of data structures without worrying about the specific use case. The file system part is just one application of the whole thing, right? IPLD is a format for creating, think of it as an intermediary thing waste for all these different hash-chain based distributed systems. You can think of addressing different kinds of data structures across hash links, like merkle links, merkle paths, canonical, universal, serialization, linked data. Serialization - CBOR, JSON, YML, XML, PB. JSON-LD, RDF compatible.

There are ways to put integers into json.

We should pack this into a nice binary format, and then serialize it for users with YAML or something. We use CBOR as one of the representations. But we want one-to-one mappings between these so that it's extremely clear how to move from one to another. IPLD is used by a bunch of different systems. It's ready for standardization. There are some extensions that will be added over time. IPLD would be a good candidate for a standard. IPFS is producing this for blockchain projects.

The format looks like this: ... I will go through this with other people in time. ob2hash. You have these hash links that you are resolving through. You have a path across hash links, so you can refer to a parent block and then walk back the history, you say slash parent and then you move down and say slash transactions and you can address everything with random access. This format is probably one of the more interesting things we could contribute to W3C on blockchain. I will do a longer tutorial and send it out as a beta. Okay, thanks.

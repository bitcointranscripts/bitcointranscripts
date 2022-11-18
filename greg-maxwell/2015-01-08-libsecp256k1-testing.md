---
title: libsecp256k1 testing
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
tags: ['bitcoin core', 'testing']
date: 2015-01-08
---

Topic: libsecp256k1 testing

Location: Reddit

<https://www.reddit.com/r/Bitcoin/comments/2rrxq7/on_why_010s_release_notes_say_we_have_reason_to/>

# libsecp256k1 testing

Today OpenSSL [de-embargoed CVE-2014-3570](https://www.openssl.org/news/secadv/20150108.txt) "Bignum squaring may produce incorrect results". That particular security advisory is not a concern for Bitcoin users, but it allows me to explain some of the context behind a slightly cryptic statement I made in the [release notes](https://github.com/bitcoin/bitcoin/blob/master/doc/release-notes/release-notes-0.10.0.md) for the upcoming Bitcoin Core 0.10: “we have reason to believe that libsecp256k1 is better tested and more thoroughly reviewed than the implementation in OpenSSL”. Part of that “reason to believe” was our discovery of this OpenSSL flaw. 

In Bitcoin Core 0.10 we are migrating transaction signing, and only signing for now, to a cryptographic library we're currently developing-- [libsecp256k1](https://github.com/bitcoin-core/secp256k1) -- which is intended to provide a high-speed, sidechannel avoiding, and high-assurance implementation of the underlying public-key cryptography used in Bitcoin. Doing this allows us to deliver safer and more reliable software that better fits Bitcoin's specific needs. The library is mostly the work of Bitcoin Core super-contributor Pieter Wuille (sipa), though many other people are working on it too-- software created alone tends to be inherently unreviewed. This library is part of what Pieter and I are working on at Blockstream.

During the development of libsecp256k1 we've been building a rather extensive test suite and employing a number of strategies to increase the assurance level of the software. Part of our testing verified the agreement of our internal functions with other implementations such as the ones in OpenSSL on random and specially-constructed random inputs. While doing this our tests turned up a case where OpenSSL's implementation of number squaring gave a wrong result. I've written a bit more about the technical details in a [post](https://np.reddit.com/r/programming/comments/2rrc64/openssl_security_advisory_new_openssl_releases/cnilq2w/?context=3) in /r/ programming. This error in OpenSSL could result in a number of cryptographic operations (for many different kinds of cryptosystems) yielding wrong results but due to good fortune the issue is not a concern for Bitcoin implementations.

The incorrectly squared numbers would be expected to be found randomly with probability around one in 2128, and so when one of the reference implementations of ed25519 had a very similar mistake [some described it](https://gist.github.com/CodesInChaos/8374632) as "a bug that can only be found by auditing, not by randomized tests". But when we found this weren't auditing OpenSSL (the issue was burred deep in optimized code). Our tests used specially formed random numbers that were intended to explore a class of rare corner cases, a technique I'd previously used in the development of the Opus audio codec. Since our 'random' testing in libsecp256k1 was good enough to find one-in-a-{number too big to name} chance bugs which could "only be found by auditing" I'm a least a little bit proud of the work we've been doing there. (Obviously, we also use many other approaches than random testing on our own code.).

I generally don't consider my own software adequately enough tested until its tests have turned up a bug in a compiler/toolchain. So far I've not encountered a compiler bug for libsecp256k1-- GCC and clang have been getting much better the last few years-- beyond some cases where the compiler produced brain-dead slow but correct output, so I may have to settle for discovering that a ubiquitous system library couldn't square correctly.

I consider this a fun example of how the Bitcoin ecosystem can contribute to driving forward the state of the art in the security of cryptographic tools, and how our needs justify higher level of assurance than has been found in common software in the past. This example isn't the only reason I have to believe that this new code is better tested and reviewed, but it's a very concrete example.


---
title: OpenSSL bug discovery
transcript_by: Michael Folkson
tags: ['cves', 'libsecp256k1']
speakers: ['Greg Maxwell']
date: 2015-01-08
media: https://np.reddit.com/r/programming/comments/2rrc64/openssl_security_advisory_new_openssl_releases/cnilq2w/?context=3
---
I contributed to the discovery and analysis of CVE-2014-3570 "Bignum squaring may produce incorrect results". In this case, the issue was that one of the carry propagation conditions was missed. The bug was discovered as part of the development of libsecp256k1, a high performance (and hopefully high quality: correct, complete, side-channel resistant) implementation of the cryptographic operators used by Bitcoin, developed primarily by Bitcoin Core developer Pieter Wuille along with a number of other people.

Part of our testing involves an automatic test harness that verifies agreement of our code with other implementations with random test data, including OpenSSL; though to reduce the chance of an uncontrolled disclosure we backed out some of the low level testing after discovering this bug. This randomized testing revealed the flaw in OpenSSL. I suppose it's also a nice example of statistical reasoning (p=2-128 that a uniform input triggers the misbehaviour) doesn't itself express risk, since while we've put enormous amounts of CPU cycles into tests we've certainly not done 2128 work. In this case the reason our testing revealed the issue was because we used non-uniform numbers specifically constructed with low transition probability to better trigger improbable branches like carry bugs (<https://github.com/bitcoin/secp256k1/blob/master/src/testrand_impl.h#L45>). I used the same technique in the development of the Opus audio codec to good effect. (Whitebox fuzzing tools like Klee or AFL, or branch coverage analysis, while good tools, seem to not be as effective for errors where the code completely omits a condition rather than having a wrong condition which was not exercised by tests.)

In libsecp256k1 the field operations (nearest parallel, we don't use generic bignums) are augmented with proofs of correctness (e.g. <https://github.com/bitcoin/secp256k1/blob/master/src/field_10x26_impl.h#L810>) though only a small part of our provable correctness can be machine checked currently. Of course, correctness proofs are only one part of our strategy. Fortunately, because of the much smaller scope of libsecp256k1 we likely have an easier time hitting a higher level of assurance than OpenSSL does.

We were initially unsure how serious the bug was and came up with several sophisticated attacks that were fortunately prevented by OpenSSL not using its optimized squaring operation in all the places it could have used it. Perhaps most interesting is that one of the reference implementations of curve25519 had almost exactly the same bug as OpenSSL: <https://gist.github.com/CodesInChaos/8374632> but it seems to have gone largely without notice.

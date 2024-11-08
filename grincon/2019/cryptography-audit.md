---
title: Cryptography Audit
transcript_by: Bryan Bishop
tags:
  - research
  - libsecp256k1
speakers:
  - John Woeltz
---
libsecp256k1-zkp audit

It's a real treat to be able to be a part of this.

## Why bother?

Just a high-level, why are we taking community resources to spend time on audits? There are some perspectives-- it's good for the community and it's what you do.

Bitcoin had on professional security audits and did just fine. But it launched in a very different environment, and it did get audits eventually.

Beyond just covering your ass, it's good to have these audits because if there's a vulnerability then you can have someone with liability. For projects like grin, it's more than just people covering their asses and taking losses for the community. This is a privacy-oriented project that I think is intended to use in real life.

## Reduce scope for pre-launch audit to secp256k1-zkp

libsecp256k1-zkp is an extension of libsecp256k1 to add bulletproof rangeproofs and an aggsig module. This library supports critical cryptographic operations that grin relies on. The audit was paid by an anonymous donor, and the community security fund was not deducted from. The primary auditor was JP Aumasson. He's a cryptographer who created the BLAKE hash function, SipHash pseudorandom function and Gravity-SPHINCS signature scheme.

So we did a reduced-scope audit for the library. We looked for the following things, which are all pretty standard things to check for. We looked for sidechannel leaks (like timing leaks), software safety such as memory leaks or API abuse, usage of underlying cryptographic primitives, RNG/PRNG problems, cryptographic security level (e.g. key lengths and parameters and magic numbers), decoding serialized/DER data which is notoriously buggy. For PRNG it's important to not pull entropy from system time or somtehing like that.

I'm just going to step through some of the things we found. None of them are groundbreaking or earthshattering. It's good to look at these things though and see what has been thought about.

## Some bugs we found

The compiler could potentially optimizee out a dead assignment that might leak sensitive data. This was in /src/ecmulti\_gen\_impl.h at line 153, bits = 0 which is used to overwrite the value of private bits may be removed by compiler since "bits" is no longer used. After compilation, you have to check if the compiler has optimized that out.

There was also missing null pointer checks. There were missing null pointer checks in secp256k1\_aggsig\_sign\_single, secp256k1\_aggsig\_verify\_single, secp256k1\_aggsig\_add\_signatures\_single. This was fixed by yeastplume.

There was unfreed heap allocations found. There was also unchecked heap allocation, which could get you a null return, which isn't that good if you're relying on that library and you're not prepared to handle that null value. As a library that other things are relying on, these things are important to clean up.

There was also an unnecessary operation in secp256k1\_aggsig\_content\_something. It just increases attack surface. So you should remove anything you don't actually use.

There was an opportunity for faster rejection of invalid parameters in secp256k1\_bulletproof\_rangeproof\_prove. This has been implemented now.

There is a pull request with fixes submitted by yeastplume: <https://github.com/mimblewimble/secp256k1-zkp/pull/37>

## Next steps for grin audits

Mainnet is already launched. We want to add more features and grow. But it's still important to take security seriously and to, again like I was saying before, you need a good perspective on it. It's not a magic bullet. But you also have to do what you can to beresponsible to your community.

The next thing for the audit are some rust, and hopefully that will have less memory errors. We'll look at grin core crate, grin keychain create, grin chain crate. We're waiting on some bids to review, and we want to compare a few different firms to see which timelines and what the community is going to get. We're still trying to reach a decision on that.

## Audit completed

<https://grin-tech.org/audits/jpa-audit-report>

<https://github.com/mimblewimble/grin/issues/1609>

<https://grin-tech.org/funding>

<https://grin-tech.org/yeastplume>


---
title: Yubikey Security
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
tags: ['security', 'hardware wallet', 'wallet']
date: 2020-11-05
---

Location: Reddit

https://www.reddit.com/r/Bitcoin/comments/jp2fp3/opinion_regarding_security/gbhojor?utm_source=share&utm_medium=web2x&context=3

# Yubikey Security

> By this logic, a yubikey would also be a great targeting vector.

They would be, and if US intelligence services have not compromised yubis or at least have a perfect targeted substitution solutions for them then they should all be fired for gross incompetence and mismanagement of their funding.

Likewise, if parties which things of significant value to secure who might be targeted by state level attackers are securing those things with just yubs instead of using yubis as a second factor in an otherwise secure setup then those parties ought to be fired too.

There are places where yubis are used as single-factor security but thats rare, compared to bitcoin hardware wallets where single factor use is essentially universal.

> You can't possibly claim an operating system with a monolithic kernel and thousands of packages is more auditable compared to

I can and I do. You have to also factor in the number of reviewers, ease of review, and targetedness of the attack.

So for example: Standard hardware wallets leak secret material via timing sidechannels pretty much universally (there are a couple that probably don't, but most do), even though it is not hard to avoid this. Why? Because there is essentially no effective review. The software running on these devices ends up being created by one or two person teams, and copy and pasted all over the place.

> A device with a secure chip and which runs nothing else but an open source firmware that I can actually handle at auditing myself, in addition to confirming what it runs exactly via a reproducible build.

"Secure chip" also means you cannot confirm what the device is actually running. You can build all you want, and compare that this matches the firmware signed by the maker but you have no idea if that is what is actually running on the device, only that the device claims that its running that.

Moreover, under your theory that all linux kernels are vunlerable to network attacks even on locked down machines, the HW wallets still end up compromised: because the vulnerable hosts can be used to compromise the HW firmware, or cause the user to purchase a compromised/backdoored device.

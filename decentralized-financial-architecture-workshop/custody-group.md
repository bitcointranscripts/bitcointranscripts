---
title: Custody Working Group
transcript_by: Bryan Bishop
tags:
  - regulation
date: 2019-09-08
---
One of the problems in the ecosystem was nomenclature. We started working on a report about what features a nomenclature would have. Airgaps, constant-time software, sidechannel resistance, Faraday cage, deterministic software, entropy, blind signatures, proof-of-reserve, multi-vendor hardware to minimize compromise. Multi-location and multi-sig. Insurance guarantee scheme. Canaries, dead man switches, tripwires, heartbeat mechanisms. Shamir's secret sharing vs multisig. The second part of this report was going to be market analysis. Most companies don't advertise what their custodial process really is. Coinbase had a lot of marketing. Xapo had videos of their vault. There's the Glacier protocol and Square's subzero now which is open-source. Bryan Bishop's proposals for vaults and restricted signing devices. What is a hot wallet?

We could make a BIP about terminology and actually proposing a real standard. An actual standard should rely on proper terminology.

It's difficult for regulators to define wallet and custody and key management and other terms. It's hard to get those terms down. I think we have to coordinate that. We hhave criteria for key management, within the frameworks of wallets.

An audit might be more effective in practical terms, but it might be hard to legislate because it's kind of subjective. Regulations can be a list of rules describing what a custodian has to follow. Whereas an audit is probably more helpful to be audited, but it's harder to pick that. You can't just say, we were audited.

Some regulators are still forming teams. Legislating about multisig thresholds is bad. It can't be prescriptive. It must be a step-by-step process, and it must be best practices in the market. Nobody wants to be left behind, of course.

What about the extent to which custody has to rely on functionality not in the blockchain itself? We're interested in things like covenants or these Bishop re-vaulting transactions. There are clever ways to use current functionality with presigned transactions and the 1% chunks idea. But without doing an actual upgrade to the protocol, it's actually quite a challenge to develop a safe custody solution.

There needs to be best practices around custody and they should be published. Basic information about companies is not even available, like what does Coinbase or Xapo really do? Is Square using subzero exactly, or are they doing anything differently internally? What is Fidelity doing internally?

Even a checklist-based standard would be something useful.

Custody is not a great business model. For a proper solution, the margins won't shrink to zero if it's a really secure product. Institutional investors can't really invest, due to the lack of custodians. 25 basis points for storage, in addition to their management fees, is not out of the question.

Some companies are doing bitcoin lending, like Unchained and Blockfi. If you do custody, you can blend the cost from kicking back the lending rates. There's a lot of services now where you lend your bitcoin to a service, and you get 6%, 12%, 15% depending on the service. If there's a minimal custody solution, then you can get 25 basis points on it and get income. You can also bundle it with a lending service. Instead of paying 25 basis points, you will actually get 6% minus 20 basis points. Nobody has really done it yet because lending services come up and custody solutions come up separately. I generally think people-- if you look at the hardware wallets, Casa nodes, a lot of people are buying these services.

We should ask custodians, what do they do? What should regulators be asking? What should their users be asking?

Shamir secret sharing, Hermit, Unchained Capital. Shamir for recovering one single key-- I don't see a problem for that. This is orthogonal to multisig. Multisig is superior to Shamir secret sharing. Verifiable secret sharing recovers some of the benefits of multisig. Social key recovery.

<http://diyhpl.us/wiki/transcripts/rebooting-web-of-trust/2019-prague/shamir-secret-sharing/>

<http://diyhpl.us/~bryan/upcoming-slides/dfa-workshop-bishop-best-practices-exchange-custodians.pdf>



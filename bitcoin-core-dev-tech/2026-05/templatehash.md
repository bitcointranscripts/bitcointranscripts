---
title: TemplateHash
tags:
  - bitcoin-core
  - covenants
  - script
date: 2026-05-08
---

CTV - CheckTemplateVerify

The CTV idea is to commit to information about the child of the transaction
within the transaction itself, e.g., the output, locktime, etc.

When it was introduced, it had weaker use cases.

Anyprevout also motivates the idea behind TemplateHash, as does
CheckSigFromStack.

TemplateHash was introduced, published, and merged into the repository.

The next step is to deploy it in Bitcoin Inquisition and then build a
demonstrated use case for the newly proposed opcode.

Channel Factory and MultiParty Factory are some of the use cases; a demonstrated
use case also exists in ARK.

PTLCs also become easier using these constructions. With every update, a
significant amount of interactivity and signing is required, but with these
constructions, the round-trip is reduced and initial signatures can be reused.

Multiple teams are building ARK now, and these constructions will significantly
simplify and improve it.

BIPs have been published, comments have been addressed, and demos are planned to
be built.

However, one of the authors is driving consensus cleanup softforks, so resources
are constrained.

Progress depends on whether ARK takes off, and the use case needs to extend
beyond ARK. This softfork is an optimisation for existing use cases: Lightning
PTLCs and ARK. It has been argued that this proposal is also a security upgrade,
and that it would be unwise not to deploy it. It is agreed that it is currently
being tested.

The motivation is stronger than the previously suggested congestion control.

TemplateHash and CSFS are not obsolete compared to other similar proposals,
which offer only vague motivations.

The previous covenant proposal is insufficient.

What is the stopping point for all these proposed opcodes?

CCV and TemplateHash overlap nicely; both constructions allow you to specify how
much money goes to a specific address, enabling vault-like constructions. The
full value of an output must go to a specified address — this is an opinionated
way of doing things. If any manipulation of the output amount is required, large
number arithmetic is needed.

Use of CheckSig in scripts is undesirable.

Interested parties should review the BIP, the motivations, and the use cases.

A PR has been added to Inquisition and tooling, e.g., Miniscript. A Bitcoin Core
PR signs the template hash with reblindable signatures.

Calls to Action: PSBT experts and Miniscript developers are encouraged to review
it, including the tooling and motivations.

What are the potential stopping points? Just template hash, arbitrary introspection, and native
ZK proofs?

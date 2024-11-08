---
title: Abstract Groups
transcript_by: Bryan Bishop
---
# Blockcert

As the standards around verifiable credentials are starting to take form, different flavours of ‘verifiable credentials’ like data structures need to make necessary changes in order to leverage on the rulesets outlined and constantly reviewed by a knowledgeable community like RWOT and W3C. The purpose of this paper is to identify all of the changes needed to comply with the Verifiable Credentials & Decentralized Identifiers standards.

# Cooperation beats aggregation

One important economic implication of a new network scaling law for meta-platforms is that the network effect benefits of cooperation may be advantageous to centralized aggregation (non-cooperation). An open interoperable portable decentralized identity framework is a prime candidate for a meta-platform. Significant momentum has been developing behind a universal decentralized identity system based on open standards. A proto-meta-platform as it were. The standards include the W3C supported DID (decentralized identifier) and verifiable credential standards. Associated industry groups include the Decentralized Identity Foundation (DIF) and HyperLedger-Indy/Aries/Ursa. A meta-platform is a platform that enables and fosters participant controlled value transfer across and among other platforms. Because platforms are a type of network, a meta-platform enables network of network effects. Network-of-network effects may be the most valuable kind of network effects especially for participants on the associated platforms.

The purpose of this paper is to foster awareness of the economic benefits of cooperation and the crucial role decentralized identity may play in unleashing historic new sources of value creation and transfer.

# Reputation interpretation

There are many different ways that people are collecting data and different parameters about people. We need a reputation table of some metrics. The question is what do you once you have it? We want to divide the different categories of reputation that people might have, like knowledge or skills in a particular domain, emotional intelligence, and generalized skills. What kind of outputs would you have? This is actionable output like a yes/no output or it might be something a little more like a recommendation or a report about something. It might also be an interpretation of that person's reputation in your new system or new community. How do we take a reputation that this matrix that comes from many different sources, and what does the actionable output look like?

# Issuer independent verification

Independent and, ideally, also universal verification of credentials is a key requirement for trust in Verifiable Credentials and will lead to broader adoption by vendors, issuers, and end-users in different ways. The challenge is that each vendor is creating their own credential schemas and there are no common methods for cross-vendor/ecosystem verification. In this paper, we will propose a set of methods by which a vendor can assure issuers that the credentials using the vendor’s chosen schema can be independently verified.

Ultimately we envision a "universal verifier" which is interoperable with a broad set of credential formats, parallel to (and of course reliant on) the "universal resolver" for DIDs. The schemas of these different credential formats can be seen as a subset (or implementation of) the Verifiable Credentials data specification. It should be possible to identify the schema type (sometimes called a "meta-schema") early in a verification process: for instance, knowing whether a credential is academic, medical or financial might be a useful scale at which to specify this, or perhaps more or less granular scales. With this foundation, vendors will naturally converge on a quick implementation of methods that make their credentials broadly useful.

The system of verification cannot be wholly dependent on end-user critical thinking and analysis, particularly in cases where both credential bearer and credential issuer are unknown or at low trust at time of verification. Nudging and signaling will be an integral part of the credential-passing UX and adoption roadmaps, but for quality checks such as these to eventually develop to support end-user adoption, future reputation and trust systems need to be anchored to “audit trails” of trust. One way to quickly build these up is by bootstrapping pre-SSI issuer verification systems (such as government-administered identity provider systems and education credentialing), focusing on interoperability and redundancy with more focused systems. Importantly, implementers with hands-on experience of the OpenCerts schema and BlockCerts standards are represented here in the writing of this document to provide a test-case for interoperability on existing systems.

There are some people here with opencerts and blockcerts. The point of this group was to describe and think about and put up some preliminary thoughts about a standardized way for the verification of credentials from unknown issuers, and thinking about the interoperability of issuer credentials. This was sort of like a backlog item in some ways. It's sort of getting more urgent now. It might soon be an interoperability issue if people can say they can accept and pass along credentials from different networks with different issuers.

# Alice abuses verifiable credentials

Alice has a valuable credential, and she wants to somehow cheat the system. What are the ways that Alice might try to abuse the system, and how can systems mitigate the threat? This paper will model threats surrounding a malicious holder of a verifiable credential, referring back to existing threat models and attack definitions.

# BTCR continued

<https://github.com/WebOfTrustInfo/rwot9-prague/blob/master/draft-documents/btcr_contd.md>

# Decentralized DID rubric

<https://github.com/WebOfTrustInfo/rwot9-prague/blob/master/draft-documents/decentralized-did-rubric.md>

The communities behind Decentralized Identifiers (DIDs) bring together a diverse group of contributors, who have decidedly different notions of exactly what “decentralization” means. For some, the notion of a DID anchored to DNS is anathema, for others, DIDs that cannot be publicly verified are problematic. This debate about decentralization is a continuation of a similar, ongoing argument in cryptocurrency circles: the question of whether or not bitcoin or ethereum is more decentralized is a nearly endless source of argument. Rather than attempting to resolve this potentially unresolvable question, we propose a rubric — which is a scoring guide used to evaluate performance, a product, or a project — that teaches how to evaluate a given DID method according to one’s own requirements. Our goal is to develop a guide that minimizes judgment and bias. Rather than advocating particular solutions, the rubric presents a series of criteria which an evaluator can apply to any DID method based on their particular use cases. We also avoid reducing the evaluation to a single number because the criteria tend to be multidimensional and many of the options are not necessarily good or bad: it is the obligation of the evaluator to understand how each response in each criteria might illuminate favorable or unfavorable consequences for their needs. Finally, this rubric allows evaluating aspects of decentralization of a DID method, but it is not exhaustive, and does not cover other issues that may affect selection or adoption of a particular method, such as privacy or efficiency.

# DID resolution v2

We will work on the next version of the DID Resolution spec (v0.2) and add/improve various issues that have been discussed recently and that are critical for ongoing implementation efforts.

This includes: DID Resolver architectures, trustable DID Resolver software, versioning matrix parameters, immutable DID URLs for keys, the DID URL dereferencing algorithm, and resolution metadata.

# Holochain

<https://github.com/WebOfTrustInfo/rwot9-prague/blob/master/draft-documents/did:hc-method.md>

# How to design good reputation

<https://github.com/WebOfTrustInfo/rwot9-prague/blob/master/draft-documents/how-to-design-good-reputation.md>

Common mistakes built into reputation systems create mixed signals, confuse users, and alienate or exclude certain populations. Many recognize the need for trust-enhancing reputation, but carry in unconscious assumptions which undermine the effectiveness of their design. This document is a “how to” guide intended to help you challenge your hidden assumptions, walk you through critical decisions, and design an effective reputation framework.

# Minimum viable protocol for decentralization

Alice wants to become self sovereign. Alice’s needs vary, but to get into decentralization she needs an agent. This agent has to be represented as some kind of physical option that she can prove the control over her self sovereignty. This agent can be mobile, biometric or other existing communication protocols. It might be a trusted execution environment online.

Alice’s agent then controls access to one or more persistent resources that are typically separate from her agent.

We want to define a couple of simple agents and needed components to make Alice self sovereign, creating a minimum viable protocol for decentralization. Making it clear to the community how one can enable self-sovereignty where there is a differentiation of agent capabilities.

# Proof of person: Not a sybil

<https://github.com/WebOfTrustInfo/rwot9-prague/blob/master/draft-documents/proof_of_personhood.md>

This paper discusses the need for, design of, and use of digital information that suggests that an entity is a unique individual human without necessarily identifying the individual. It is important not to rely on politically centralized entities for the creation of such information, in order to safeguard certain universal human rights; thus we consider only approaches that ensure a governance structure that is robust to abuse of power and preserves system integrity. This could be information that provides either a 100% guarantee, or one that provides less certainty; it could also be anonymous or pseudonymous. For example, such information could enable a decentralized voting system, distribution of a universal basic income, or ticket scalping reduction. Organizing Sybil-proof identity information in this way is associated with various risks; thus we warn against some possible paths of abuse.

# p2p lending reputation system

Reputation System Spec for a specific use case: P2P Lending. A reputation system designed to support lenders (including groups of individuals) in making good decisions about issuing loans on a P2P lending framework such as Kiva. The reputation system should avoid the pitfalls of a single, legible credit score. Designed for one-to-one, one-to-many, and many-to-many connections.

# Secure data storage

We store a significant amount of sensitive data online such as personally identifying information, trade secrets, family pictures, and customer information. The data that we store should be encrypted in transit and at rest but is often not protected in an appropriate manner.

This paper describes current approaches and architectures, derived requirements, and dangers that implementers should be aware of when implementing data storage.

This paper also explores the base assumptions of these sorts of systems such as providing privacy-respecting mechanisms for storing, indexing, and retrieving encrypted data, as well as data portability.

# Shamir secret sharing

At last rebooting, we had a group working on SSS. Some code was implemented for SLIP 39 but we never really shipped the final paper. A lot of this is a response to the SLIP 39 code.

Social key recovery allows users to collaborate with each other to securely recover their secrets instead of using centralized account reset procedures. Shamir secret sharing is an increasingly popular implementation for social key recovery, where a secret can be split into a number of shares with various threshold requirements or in the future any arbitrary monotone boolean function.

SatoshiLabs' SLIP 39 is one proposed implementation of Shamir secret sharing with mnemonics. SLIP 39 is Simple Shamir Secret Sharing plus a two-level fixed threshold group, and a mnemonic text encoding scheme, and an encryption scheme as well.

We are uncomfortable with some of the decisions in SLIP 39 and uncomfortable with the fact that they are all bound together tightly. In light of this, we are writing a Bitcoin Improvement Proposal that is loosely inspired by SLIP 39. In this BIP, the proposal includes a binary format, additional metadata (such as birthdate), allows for the greater flexibility of thresholds, optional pre-defined pre-parameterized threshold requirement templates, and one of the goals is to make the design so that it is possible to independently audit the independent parts of the proposal, making the proposal more modular. It will also be compatible with future upgrades like verifiable secret sharing and MuSig.

We are looking forward to championing this proposal in the community, collecting feedback, and driving the improvement proposal process. We also propose to make an implementation as required by the BIP process.

# The real problem with centralization

So often when discussions arise about centralization and specifically about decentralized networks, the issue is framed through the lens of corruption or concentration of power. While these are significant problems, there is a separate issue that may ultimately be of greater importance: centralized systems have significant limitations in their capacity to adapt and respond. At present, humans are facing a world with increasingly complex challenges that our centralized systems (institutions, but also our existing digital communication systems) are not proving capable of responding to. In this paper, we will articulate the difference between a centralized network, a decentralized network, a distributed network and an ecosystem, and articulate the ways in which an ecosystem, in which agents are able to bridge between multiple networks has significant advantages in terms of innovation and adaptation. This is a result of an asymmetry between the propagation of learnings (experiments that prove contextually useful to those that try them are able to spread rapidly via those who also find them useful) and the propagation of failures (experiments that prove costly or useless tend not to propagate much further than those who find them to be problematic). Contexts vary, and so there is no one-size-fits-all set of information that will be appropriate. However, in an agent-centric ecosystem which would include distributed identity processes, participants are able to iteratively improve their sensing and coordination capacities over time, resulting in increasingly capable coordination of efforts and high responsiveness to shifts in the environment.














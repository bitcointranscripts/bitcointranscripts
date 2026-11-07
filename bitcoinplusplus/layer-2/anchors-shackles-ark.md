---
title: 'Anchors & Shackles (Ark)'
transcript_by: 'mazubukuntalo8-collab via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=OBt1nS14Ac4'
date: '2023-06-24'
tags:
  - 'ark'
  - 'c-lightning'
  - 'acc'
speakers:
  - 'Burak Keceli'
categories:
  - 'security-problems'
---

# Proposed Bitcoin Layer 2 Protocol: Full Edited Transcript

## Part 1: Presentation

### 1. Introduction and background

So, hey everyone. My name is Borat.

Today, I’ll be talking about something I’ve been working on for approximately six months.

To give you some background, I initially came from the big-block camp. Later, I was introduced to Liquid, where I spent about two years doing covenant research and development. More recently, I’ve been exploring the Lightning Network space for approximately a year.

Coming from a big-block background, I’ve always had objections to Lightning, particularly around the user experience. These concerns include backup mechanisms, interactivity requirements, and liquidity problems. I’ve had some pretty serious objections in these areas.

A few months ago, I started working on a new Lightning-related idea to address these problems. Over time, I came to realize that most of my earlier objections are potentially solvable in the long run.

For example, point time-locked contracts, or PTLCs, can address some of the limitations associated with HTLCs. Asynchronous receiving initiatives and proof-of-payment mechanisms can also help address existing shortcomings.

However, one major problem remains: inbound liquidity.

For me, this is a fundamental obstacle.

Imagine orange-pilling someone for the first time. They download a wallet, but they cannot receive a payment because they have no inbound liquidity. They may need a swap-in service or some other mechanism to receive funds. That introduces friction and does not scale well.

My view is that if a payment system works 90% of the time but fails 10% of the time, it is not good enough for a truly seamless user experience. The goal should be zero friction.

I therefore started exploring solutions to these problems. Today, I’ll present an alternative Layer 2 protocol designed to address them.

### 2. From a wallet concept to a new Layer 2 protocol

The project originally began as a wallet idea based on Lightning and channel factories.

As the design evolved, I realized that what I was building was no longer simply a Lightning wallet. At its core, it had become a new Layer 2 protocol with its own off-chain transaction model.

The protocol requires a new covenant primitive, such as `APO` or `CTV`, to function as intended. These capabilities are not currently available on Bitcoin mainnet in the form required by this design.

However, we can experiment with them on Bitcoin Inquisition's Signet. I believe that is where development and testing would begin.

We have not settled on a name for the protocol yet.

At a high level, the protocol has several important properties:

- No inbound-liquidity constraints: Users do not need to acquire inbound liquidity before receiving payments.
- A familiar wallet experience: Users can receive, send, and hold Bitcoin in a way that resembles using an on-chain wallet.
- Minimal interactivity requirements: Users do not need to remain continuously connected to a server. The goal is to support ordinary smartphone wallets.
- Non-custodial exit: Users can unilaterally recover their funds on-chain without requiring a cooperative organization to authorize the withdrawal.
- Privacy through transaction mixing: Payments are designed to pass through a CoinJoin-like off-chain mixing process.

The protocol is not intended to be a state-channel construction or a conventional rollup. It is intended to represent a distinct category of Bitcoin Layer 2 architecture.

### 3. Privacy and the motivation for CoinJoin

Every payment in the proposed protocol takes place through a CoinJoin-like process. The goal is to avoid unnecessarily revealing payment relationships, particularly the identity of the receiver.

Consider Lightning. If routing hubs collaborate or comply with a surveillance request, they may be able to correlate payment information.

For example, suppose I use one Lightning service provider and a receiver uses another. If both providers have a direct channel with the same intermediary, they may be able to correlate information about the payment route.

Depending on the implementation, they might use information associated with the same HTLC, including its BOLT 11 payment-hash identifier, to help establish a relationship between the sender and receiver.

The proposed protocol attempts to reduce this kind of correlation by placing payments inside an off-chain CoinJoin-like mixing process.

The objective is to make the payment participants part of a shared anonymity set rather than expose a clearly traceable payment route.

This privacy component is not strictly necessary for the protocol to function. The underlying construction could work without CoinJoin. However, I consider privacy a valuable addition.

### 4. Comparing the protocol with existing Bitcoin systems

I want to compare the proposed protocol with several existing systems:

- On-chain Bitcoin.
- The Lightning Network.
- Ecash systems, including Cashu and related approaches.
- Fedimint and other federation-based systems.

There is some controversy over what qualifies as a Layer 2, so the comparison depends partly on the definition being used.

My definition is that a Layer 2 is a separate software system that allows users to transact in Bitcoin without placing every transaction on the Bitcoin blockchain, while still permitting users to recover their Bitcoin on-chain without requiring a corporation to authorize the recovery.

Under this definition, the proposed protocol qualifies as a Layer 2 because transactions occur off-chain while users retain a unilateral recovery path.

Ecash is useful to include in the comparison, even though I would not classify it as a Layer 2 under this particular definition.

#### Interactivity and receiving payments

Lightning's HTLC and PTLC designs have different properties, but they still involve operational requirements associated with channel management and monitoring.

Asynchronous receiving mechanisms can improve the receiving experience. However, users may still need to monitor the network for channel breaches unless they rely on a watchtower or another monitoring service.

The proposed protocol is intended to reduce these requirements and provide an experience closer to that of an on-chain wallet.

#### Scalability

I believe scalability is one of the protocol's most important potential advantages.

I do not believe the current Lightning architecture can onboard the entire planet without encountering significant constraints. Channel openings, on-chain swaps, liquidity acquisition, and other operations can become bottlenecks.

The problem is not limited to the on-chain footprint. Liquidity itself is a constraint.

I have an ambitious goal: to give as many people as possible the option to use Bitcoin in a non-custodial way.

I realize that onboarding the entire planet may never be practical, but it is a goal I care deeply about.

In theory, the proposed covenant primitive could enable a very large number of users to participate without requiring a separate on-chain transaction for every payment. There would still be other engineering, economic, and operational challenges, but the intention is to minimize the on-chain footprint.

Most activity would occur off-chain. On-chain transactions would primarily support the underlying factory construction and recovery mechanisms.

#### Privacy

Privacy comparisons between Lightning and on-chain Bitcoin are controversial.

Some people argue that Lightning provides better privacy than on-chain transactions. Others argue the opposite.

The proposed protocol introduces an additional privacy mechanism: payments are processed through a CoinJoin-like mixing round.

In conventional CoinJoin implementations, a mixing session may take considerable time to coordinate. In this protocol, factory sessions would occur regularly, potentially every five seconds.

The intended anonymity set would consist of the participants whose payments are included in the relevant mixing process. The actual privacy guarantees would depend on the implementation, participation levels, timing information, and the ability of observers to correlate activity.

#### Onboarding

The intended onboarding experience is simple.

If I want to orange-pill someone, I should be able to send them Bitcoin without requiring them to obtain inbound liquidity first. They should be able to download a compatible wallet and receive a payment.

The aim is to make receiving Bitcoin as straightforward as receiving it with an on-chain address, while keeping most activity off-chain.

### 5. The participants: users and factory operators

Conceptually, the protocol has two main participants:

1. Users.
2. Factory operators.

Factory operators are similar to Lightning service providers, or LSPs. In fact, a factory operator could also operate Lightning infrastructure.

The protocol is intended to interoperate with Lightning rather than compete with it.

For example, users should be able to pay Lightning invoices from the protocol. A factory operator could route Lightning payments and provide liquidity for the protocol at the same time.

The two systems would serve somewhat different purposes.

Lightning is well suited to use cases where immediate payment settlement is important and liquidity can be managed efficiently.

The proposed protocol is intended to offer a simpler user experience for receiving and holding Bitcoin without first acquiring inbound liquidity.

There is, however, a liquidity trade-off. Lightning channels are bidirectional, allowing liquidity to be used in both directions. The proposed protocol uses a more one-directional design, which means factory operators may need to provide liquidity continuously.

### 6. The covenant primitive

The protocol requires a covenant-like primitive that can constrain the outputs of a spending transaction.

`CTV` is one possible approach, although its use is controversial. `APO` may provide another route, potentially emulating the required behavior through a combination of signature and script mechanisms.

The original discussion also mentions alternatives involving `OP_CAT`, synthetic constructions, and other covenant proposals. The exact feasibility of each approach depends on the precise script construction and the Bitcoin consensus rules available in the target environment.

The essential requirement is to commit to the relevant transaction structure in advance, so that outputs can be constrained when a Bitcoin output is created or spent.

The rest of the design builds on that capability.

### 7. Coins and factories: the basic architecture

The protocol uses a concept called a factory.

A factory resembles a channel factory, which is why the speaker uses that name, although the design has evolved beyond a conventional channel-factory model.

A factory is a Bitcoin transaction output that acts as a shared UTXO. Nested within that output are commitments representing multiple off-chain coins.

These coins are not ordinary independent Bitcoin UTXOs. They are off-chain objects whose ownership and spending conditions are represented through the factory's transaction structure and associated scripts.

You can think of the design as a UTXO set that exists almost entirely off-chain.

A wallet might contain anywhere from one coin to a million coins, ignoring dust limits for the purposes of the conceptual explanation.

Each coin is designed as a one-time-use spending object. Instead of repeatedly updating the state of a persistent Lightning channel, a user spends an existing coin and creates new coins representing the resulting balances.

#### The factory transaction

The factory operator periodically creates a factory. For simplicity, imagine that a new factory is created every five seconds.

Unlike a conventional CoinJoin, which may take hours or days to coordinate, this design aims to establish mixing rounds on a regular schedule.

A factory transaction contains several outputs:

- Coins output: Contains commitments to the coins participating in the factory.
- Connectors output: Contains commitments to connector outputs used by the spending protocol.
- Factory change: Returns any remaining value to the factory operator or the relevant change destination.

The factory operator funds the factory transaction and coordinates the creation of the new factory.

The coins output contains a collection of coin commitments. Each coin is associated with a two-of-two arrangement between the coin owner and the factory operator, similar in concept to a Lightning channel.

However, rather than maintaining a persistent channel state, each coin is intended to be spent once before being replaced by new coins.

The initial concept involved placing Lightning channels inside a shared UTXO, as in channel factories or coin-pool designs. The current design instead uses individual coin objects.

The factory's coin commitments can be revealed through a suitable script path by someone who knows the relevant template information. In the proposed construction, the commitments are intended to make it possible to recover the coin contents when necessary.

#### Connector outputs

The connectors output contains commitments to a set of connector outputs.

Connectors are also Bitcoin transaction outputs. They serve as commitments linking the spending of coins from a previous factory to the existence of a new factory.

They differ from the coin commitments in an important way:

- The coin commitments are intended to be revealed as a group in the current construction.
- Connectors are intended to be revealed individually.

The connector structure resembles a withdrawal tree, with update-and-verify behavior. The speaker suggests that a more efficient tree-based construction could improve the design in the future.

Connectors also carry a small amount of Bitcoin value, described in the presentation as dust. The factory operator can spend them through a single-signature path.

Their purpose is to help establish an atomic relationship between the old coins being spent and the new factory being created.

### 8. ATLCs: the protocol's core spending primitive

The speaker introduces a new term: ATLC, described as an alternative to the HTLC and PTLC constructions used in Lightning.

The proposed primitive is intended to support the same broad goals as Lightning's conditional payment mechanisms while addressing the liquidity limitations of receiving payments.

The speaker argues that conventional HTLCs have significant limitations for asynchronous receiving, particularly when the receiver cannot provide the required preimage while offline.

PTLCs and asynchronous receiving initiatives may address some of these shortcomings, but the proposed ATLC construction aims to remove the inbound-liquidity requirement.

In the speaker's description, receiving should work almost like pressing a button: a user can receive the funds they are owed without first arranging incoming liquidity.

The protocol is designed around one-time-use coins, each associated with a two-of-two relationship between the coin owner and a factory operator.

When a user wants to spend a coin, they participate in a new factory session. The old coin is consumed in the off-chain state transition, and new coins are created to represent the payout and any remaining change.

The ATLC construction connects the coin being spent to a connector associated with the new factory.

This relationship is intended to make the transfer atomic: the factory operator should not be able to claim the old coin unless the relevant new factory exists in the required form.

### 9. How a factory session works

The protocol's factory session resembles a CoinJoin round, with additional commitments and spending conditions.

Suppose a user has several coins from previous factories and wants to spend them.

The user joins a new factory session and registers the coins they intend to spend. These coins were created in earlier factories and are now being consumed.

The user also registers for the new payout coins and any change coins they want to receive.

The factory operator acts as a blinded coordinator.

#### Phase 1: Coin registration

The user registers the existing coins they want to spend.

The factory operator provides blinded credentials that allow the user to register for new coins without directly linking the old coins to the new payout coins.

In a conventional CoinJoin, inputs and outputs are generally registered within the same coordination process. Here, the protocol aims to use blinded credentials to separate those registrations and improve privacy.

A session could contain many participants. The speaker describes a design that could accommodate thousands of coins and potentially millions if a more efficient update-and-verify construction becomes available.

#### Phase 2: Payout registration

After registering the coins being spent, the user registers for new payout coins and any change.

The factory operator combines these commitments with those of other participants when constructing the new factory.

The new factory contains the relevant payout coins and a corresponding set of ATLC connectors.

If \\(N\\) coins are being spent, the operator adds \\(N\\) ATLC connectors. The session can create \\(M\\) new coins, where \\(M\\) depends on the number of payouts and change outputs required.

#### Phase 3: Signing

Once the registrations are complete, participants sign the relevant off-chain transactions.

The user attaches an ATLC to each coin being spent. That ATLC is connected to a connector associated with the new factory.

The user and the factory operator exchange the necessary signatures for the ATLC spending construction.

The ATLC is intended to represent a single state transition: the old coin is spent and the new payout is created.

The user signs the ATLC using the two-of-two arrangement associated with the old coin. The connector from the new factory supplies the commitment needed to link the spending transaction to the new factory.

All participating users perform the corresponding operation.

If a participant refuses to complete the required signing steps, the factory operator can exclude that participant from the session, according to the proposed coordination rules.

#### Phase 4: Factory creation

After the signing process, the factory operator broadcasts the factory transaction.

The new factory contains the new coin commitments and connectors. The operator has funded the transaction and provided the liquidity required to create the coins.

The ATLC construction is intended to ensure that the operator cannot simply claim the old coins while failing to establish the corresponding new factory.

The speaker describes this as an atomic construction.

### 10. The on-chain ATLC transaction

The speaker describes an ATLC transaction as having two inputs.

The first input is the coin being spent from a previous factory. It is controlled by a two-of-two arrangement involving the user and the factory operator.

The second input is an ATLC connector associated with the new factory.

The first input commits to the relevant spending transaction, while the second input references the connector from the new factory.

The proposed construction uses `SIGHASH_ALL` so that the signature commits to the transaction's inputs and outputs, including the relevant outpoint associated with the new factory.

The intent is to create a relationship between the old coin and the new factory.

If the factory operator double-spends or otherwise invalidates the factory transaction, the connector commitment no longer satisfies the intended spending construction. Consequently, the operator should not be able to claim the old coin through the normal path.

The user can then use the appropriate script path to recover the funds.

The operator's ability to claim the old coin is therefore conditional on the new factory existing as required.

This is central to the proposed atomic transfer mechanism.

The transaction also includes an output that allows the factory operator to reclaim the relevant funds under the appropriate conditions.

### 11. Factory expiry and recovery

Factories and their coins have time-limited spending conditions.

The example presented uses a four-week factory lifetime.

The factory operator funds the factory and has a delayed script path that permits the operator to reclaim the relevant output after four weeks.

During that period, users can spend their coins and move their balances into new factories.

If a coin is approaching expiry, a user can perform a self-transfer: the user sends the funds to themselves through a new factory, effectively refreshing the coin's lifetime.

The speaker suggests that users might need to perform this operation approximately every two weeks, although the exact schedule depends on the coin's spending conditions.

#### Two recovery scenarios

The design includes two important scenarios.

1\. Normal operation

The user spends coins before they expire. The old coins are consumed, and new coins are created in a subsequent factory.

The four-week timer therefore does not necessarily mean that a user must withdraw on-chain every four weeks. The user can continue using the protocol by moving coins between factories.

2\. Non-cooperative factory operator

If a factory operator stops responding or refuses to cooperate, the user can reveal the relevant factory contents and use the available recovery paths.

The speaker calls this an unilateral closure or non-cooperative closure.

In the current construction, revealing the factory may require revealing all of its coin commitments, even if the user is interested in only one coin. The speaker acknowledges that this is inefficient.

A more advanced update-and-verify tree could allow a user to reveal and recover only the relevant coin, avoiding the need to expose the entire factory.

The proposed recovery design includes several script paths:

- The recipient can claim the coin during the permitted claim window.
- The sender can recover funds after a relative time delay if the recipient does not claim them.
- The factory operator can reclaim funds after the relevant expiry period, subject to the construction's conditions.

The speaker uses a two-week period to illustrate the sender's refund window and a four-week period to illustrate the operator's expiry path.

These are example parameters rather than universal requirements of the protocol.

#### Why the sender needs a refund path

Suppose Alice sends a coin to Bob, but Bob does not receive or claim it.

The sender should not lose access to the funds indefinitely.

After the specified timeout, Alice should be able to recover the funds, much like a sender recovering an unclaimed Lightning HTLC.

If Bob has already claimed or spent the coin, the relevant conditional spending mechanism prevents Alice from simply reclaiming funds that have already been transferred successfully.

The precise safety of this arrangement depends on the interaction between the claim paths, connector commitments, timeouts, and signatures.

### 12. Lightning interoperability

The protocol is intended to interoperate with Lightning.

Factory operators could add HTLCs or PTLCs to a factory template alongside the coins and connectors.

This allows protocol users to pay Lightning invoices and potentially receive payments from Lightning users.

Consider Alice, who uses the proposed protocol, and Bob, who uses a conventional Lightning wallet.

Alice wants to pay Bob a Lightning invoice worth 21 satoshis.

Suppose Alice has six coins distributed across three factories:

- Two coins associated with factory operator X.
- Two coins associated with factory operator Y.
- Two coins associated with factory operator Z.

Alice can use a multi-part payment approach similar to Lightning's multipath payments, or MPP.

She joins sessions with the relevant factory operators, registers the coins she wants to spend, and arranges for the operators to forward the payment through Lightning.

The factory operators create the necessary conditional payments and forward the funds to Bob.

The protocol can therefore destroy old coins and create new payout coins, or use the coins to pay a Lightning invoice.

The speaker also describes the possibility of receiving Lightning payments into the protocol through nested conditional-payment constructions.

The exact implementation would need to establish how the conditional payments, factory commitments, timeouts, and settlement conditions interact.

### 13. Receiving payments and proof of payment

The proposed receiving mechanism is designed to support asynchronous payments without requiring the receiver to be online when the sender initiates the payment.

The speaker compares the approach to Silent Payments.

A recipient has a known public key. The sender derives a payment-specific key or commitment by combining the recipient's public key with a shared secret and unique information about the payment.

The relevant information includes:

- The factory outpoint or another unique factory identifier.
- A shared secret between the sender and receiver.
- The sender's public key.
- The recipient's public key.
- A unique payment commitment.

The sender uses this information to derive a payment-specific output key or script commitment.

The sender then communicates the relevant commitment to the recipient out of band, for example through a direct message.

The recipient can use that information to locate the appropriate factory and identify the coin that belongs to them.

They can then verify the factory contents and determine the corresponding script or public key.

The construction is intended to provide several benefits:

- Avoiding address reuse.
- Generating unique payment-specific coin identifiers.
- Supporting asynchronous receiving.
- Providing evidence associated with the payment.
- Allowing the receiver to identify their funds without requiring a conventional incoming channel.

The speaker argues that the commitment can also support proof of payment when the recipient claims the relevant coin.

The exact cryptographic details of the key derivation and proof-of-payment construction would need to be specified formally before implementation.

### 14. Optional penalty mechanism for instant settlement

The protocol may also include a penalty mechanism inspired by Lightning.

This is intended to provide stronger settlement assurances for users who want to accept an unconfirmed factory or coin as immediately settled.

Suppose a factory transaction is in the mempool but has not yet been confirmed.

A recipient may wish to accept a payment represented by a coin in that factory.

However, until confirmation, the factory operator could potentially attempt to double-spend the factory transaction.

The proposed penalty mechanism aims to make that behavior costly.

The speaker discusses using a construction involving `XOR` or `OP_CAT` to constrain parts of a signature or nonce to a particular script field. Under the proposed idea, a factory operator who double-spends a factory could expose information that allows affected users to recover funds from previously spent coins.

The intended result is an economic disincentive against double-spending.

The speaker also notes an important limitation: a newly onboarded user may not yet have previously spent coins that could be used for such a penalty.

Therefore, this mechanism would not necessarily provide the same assurances in every situation.

The protocol can still function without this optional mechanism. Users who require immediate settlement may prefer Lightning, while other users may accept a confirmation delay in exchange for a different liquidity model.

The exact feasibility of the penalty construction depends on the cryptographic mechanism and the Bitcoin script capabilities available. The presentation describes it as a design proposal rather than a fully implemented feature.

### 15. Unconfirmed coins and Lightning payments

The speaker also proposes that unconfirmed coins could potentially be used to pay Lightning invoices.

The reasoning is that both the existing coin and the new coin are associated with a two-of-two arrangement involving the factory operator.

If the operator also operates a Lightning node, the same operator could potentially route the Lightning payment.

Under the proposed design, a user might receive an unconfirmed coin and use it to pay a Lightning invoice without waiting for the factory to confirm, provided the operator and payment route accept the relevant settlement conditions.

This does not eliminate the risks associated with unconfirmed transactions. It depends on the factory operator's incentives, the possibility of double-spending, and any penalty or risk-management mechanisms used by the protocol.

### 16. Summary of the proposal

To summarize, the protocol is an attempt to build a Bitcoin Layer 2 with the following characteristics:

- Users can receive Bitcoin without first acquiring inbound liquidity.
- Coins are represented by off-chain commitments nested within shared factory outputs.
- Users spend old coins and create new coins through regularly scheduled factory sessions.
- CoinJoin-like coordination is intended to improve privacy.
- ATLCs and connector outputs link the spending of old coins to the creation of new factories.
- Time-locked script paths provide recovery mechanisms if a recipient or factory operator becomes unresponsive.
- Factory operators provide liquidity and coordinate the system.
- Lightning interoperability allows users to pay Lightning invoices.
- An optional penalty mechanism may improve assurances for accepting unconfirmed payments.
- The design requires covenant-like capabilities that are not currently available on Bitcoin mainnet in the required form.

The proposed architecture introduces trade-offs. Liquidity is less efficiently reused than in bidirectional Lightning channels. Recovery can be expensive if an entire factory must be revealed. Factory transactions must be reliably propagated and confirmed. The privacy, settlement, and recovery mechanisms also require rigorous analysis.

The ultimate objective is to give users a straightforward way to hold, send, and receive Bitcoin non-custodially without the friction associated with inbound liquidity.

Thank you for listening. I’m sure you have plenty of questions, and I’m happy to discuss them.

Thank you. Thank you. Thank you.

## Part 2: Audience Questions and Answers

### Question 1: Is privacy necessary for the protocol to work?

Audience member: Some of the technical details were a little over my head, but I’m curious about one thing. Is privacy necessary for the protocol to work, or is it an additional feature?

Borat: The protocol can work perfectly well without CoinJoin. In fact, the idea evolved over time.

The initial design was more like a Lightning channel-factory construction. Later, it evolved into a CoinJoin-based design.

The underlying protocol could be implemented without the CoinJoin components. I simply thought that adding them would be beneficial.

### Question 2: Why doesn't the factory operator take everyone's money after four weeks?

Audience member: I think I missed an important step. It sounds as though the factory operator can simply wait four weeks and then take everyone's money. Why wouldn't the operator just set up a factory and take the funds?

Borat: Are you asking how the penalty mechanism works for the sender or receiver?

The penalty mechanism is intended to provide assurances for instant settlement. If you're a vendor who requires immediate settlement, you may be better off using Lightning. Lightning is well suited to that use case.

The penalty mechanism is an additional feature for situations where instant settlement is required, but the protocol can work without it.

The four-week timeout exists because the factory design allows multiple channels or coins to be grouped into a shared on-chain structure. Eventually, that structure may need to be revealed or reclaimed, which would create an on-chain footprint.

The proposed one-directional coin design is intended to make liquidity available for subsequent transfers. Assuming the coins in a factory are spent within the four-week period, the factory operator can eventually reclaim the relevant factory output.

Audience member: When you say that the coins are spent, do you mean spent within the factory?

Borat: Yes. Spending the coins within the protocol is an off-chain operation. The factory itself is represented by an on-chain transaction, but the individual coin transfers take place off-chain.

Audience member: So it's essentially a large off-chain CoinJoin?

Borat: Yes, it's an off-chain CoinJoin-like construction.

### Question 3: What happens if the recipient does not respond?

Audience member: What happens if someone claims they didn't receive my message, or simply doesn't respond?

Borat: The construction is intended to be atomic. Suppose I send you a coin through a payment message. If you don't claim it within the specified period, I should eventually be able to recover the funds.

The sender has a refund path, similar to an HTLC timeout in Lightning.

The first two weeks are the recipient's opportunity to claim the coin. During the subsequent period, the sender can recover it if the recipient has not completed the claim.

The exact behavior depends on the coin's script paths and whether the relevant transfer has already been completed.

### Question 4: How many participants can a factory support?

Audience member: How many people do you expect to be in each factory?

Borat: Potentially thousands. If we can implement a more efficient update-and-verify construction, the number could potentially reach millions.

The current design has a significant limitation: revealing the factory may require revealing all its coins. Ideally, we'd use a tree-based construction so that users could recover only the coins they need.

Audience member: Isn't that a major weakness? If a single participant stops responding, wouldn't the whole factory have to be closed on-chain?

Borat: That's a disaster scenario, and I understand the concern. There are similar catastrophic scenarios in other systems, including Lightning, where a channel breach or the publication of an old state can require an on-chain response.

The protocol should provide incentives that discourage the operator from cheating. Even if a coin has a very small value, the owner should theoretically have a recovery path, although claiming a tiny amount may not be economically worthwhile.

Ideally, the protocol would use a more efficient tree construction to avoid forcing everyone to reveal their coins just because one participant needs to recover funds.

### Question 5: How does someone onboard to the protocol for the first time?

Audience member: Let's go back to the beginning. Suppose I have Bitcoin on Layer 1. How do I onboard to the protocol?

Borat: One possibility is to withdraw from an exchange that already supports the protocol.

For example, suppose Bitfinex has already onboarded funds and holds coins within the protocol. A user could withdraw to a compatible wallet by providing the appropriate public key.

The exchange would participate in a factory session and create payout coins for the user. The user would become a co-signer of the new coins, with the corresponding recovery conditions.

The user could then receive, hold, and spend coins without needing to open a conventional Lightning channel.

Audience member: But what if I'm the first person? I have Bitcoin on-chain, and I want to join the protocol. How does that work?

Borat: In that case, you'd need an initial onboarding mechanism.

You could start with an on-chain UTXO and use it to establish the necessary two-of-two arrangement. From there, the funds could participate in the protocol's factory sessions.

The initial construction might resemble a one-time-use channel, although the exact onboarding mechanism remains an implementation detail.

The key point is that someone must initially bring Bitcoin into the system. Once the protocol has users and factory operators, those users can transfer coins within it without requiring a new on-chain transaction for every payment.

Audience member: So someone has to onboard first. The protocol doesn't create Bitcoin out of nothing.

Borat: Correct. The protocol relies on Bitcoin being introduced into the system. The goal is to make subsequent transactions more scalable and convenient.

### Question 6: How does the recipient identify their coin?

Audience member: Let me recap what I understand. The factory creates the coins, and if I want to pay someone, we share some information out of band that lets the recipient identify the coin. The connectors then make the transfer atomic. Is that right?

Borat: Yes, that's the general idea.

The sender communicates the relevant factory information and payment commitment to the recipient. The recipient checks the factory transaction and verifies the coin's contents.

They can calculate the appropriate script or public key and establish that the coin belongs to them.

Audience member: Are the connectors also separate transaction outputs?

Borat: Yes. Connectors are Bitcoin transaction outputs, just like the coin commitments. They are commitments that connect the old and new factory structures.

The difference is that the connectors are intended to be revealed individually, while the current coin construction requires the coins to be revealed together.

### Question 7: How does the XOR penalty mechanism work?

Audience member: You mentioned XOR as part of the penalty mechanism. Could you explain that?

Borat: Imagine that you're receiving a coin worth 1,000 satoshis, but the factory transaction has not yet confirmed.

You might decide to accept the coin as immediately settled. However, the factory operator could potentially double-spend the factory transaction.

The proposed penalty mechanism attempts to make that behavior costly. If the operator double-spends a factory, information exposed through the construction could allow a user to recover funds from previously spent coins.

The idea is to make cheating economically unattractive.

Audience member: So you're using information from an existing transaction and a new transaction to derive the operator's private key or otherwise penalize them?

Borat: That's the intended direction of the construction. It relies on the cryptographic details of the penalty mechanism, including the proposed use of XOR or related script capabilities.

It also depends on the user having previously spent coins that can be used in the penalty arrangement. A newly onboarded user may not have that history yet.

The protocol can still work without this mechanism. It is an additional feature for users who want stronger instant-settlement assurances.

### Question 8: How do transaction fees affect the design?

Audience member: Do transaction fees create problems for this construction?

Borat: Factory transactions have an on-chain cost, but that cost is shared across the participants.

For example, if a factory transaction costs approximately 25,000 satoshis in fees and serves 1,000 participants, the fee contribution averages approximately 25 satoshis per participant, before accounting for liquidity fees and other costs.

The exact figures depend on transaction size, fee rates, and the number of participants.

The protocol is intended to operate as a liquidity network, much like Lightning, although liquidity may be used less efficiently because of the one-directional design.

### Question 9: What happens if the factory operator disappears?

Audience member: Suppose the factory operator disappears and everyone knows the operator is offline. Imagine there are 100 participants. Can any of them close the factory at the current state, or does the entire factory have to be closed?

Borat: Under the current design, you first reveal the relevant factory contents. Then you use the recovery path associated with your coin.

You cannot necessarily claim the funds immediately. The coin's spending conditions may require an additional transaction and a delay before final recovery.

Audience member: Is that a multi-stage process? Does every participant need to sweep their own output?

Borat: Yes, there may be multiple stages.

The current design is less efficient than an ideal tree-based construction. If you want to claim one coin, you may need to reveal all the coins in the factory, then perform the necessary spending operation for your own coin.

A more efficient update-and-verify tree could allow a participant to reveal only the coin they need.

That is one of the design improvements we would like to make.

### Question 10: Does the receiver need to connect to a factory?

Audience member: You said that a receiver needs to connect to a factory. Is that right?

Borat: No, the receiver doesn't necessarily need to connect directly to a particular factory in advance.

Imagine that someone orange-pills you. You download a compatible wallet, and they send you a payment. You don't need to know the factory operator beforehand.

The payment might come from one factory operator while your other coins are associated with different operators. The wallet should be compatible with multiple factories.

The sender tells you which factory contains the payment and provides the information needed to identify your coin. Your wallet then verifies the relevant transaction and coin commitment.

Audience member: So the payment message identifies the factory and the public key I need to recognize?

Borat: Exactly. The message provides the relevant information so the wallet can find and verify the payment.

### Question 11: What happens if the factory transaction is still in the mempool?

Audience member: Is the factory transaction already confirmed on-chain, or is it still in the mempool?

Borat: Some factory transactions would be confirmed, while newer ones might still be in the mempool.

Audience member: If a factory transaction is in the mempool, it could be evicted if the mempool fills up. What happens then?

Also, fee bumping could be a problem. If you change the transaction in a way that changes its transaction ID, you could break the commitments that depend on that ID.

Borat: Correct. Ordinary fee bumping can be problematic if the construction relies on a transaction ID that changes when the transaction is modified.

One possibility is to use a child-pays-for-parent, or CPFP, strategy. The factory could include an additional output that the operator can spend to increase the effective fee rate without modifying the original factory transaction.

That would need to be designed carefully so that the transaction's commitments remain valid.

Audience member: Suppose I receive an unconfirmed coin, use it to pay someone, receive the goods, and then the factory transaction is evicted from the mempool. The payment might never confirm. Isn't that a serious problem?

Borat: Yes. The factory operator must ensure that the transaction has a reasonable chance of being confirmed.

If a user requires strong assurances of immediate settlement, they need a mechanism that addresses the risk of a double-spend or an unconfirmed transaction being dropped.

The optional penalty mechanism is intended to help in certain cases. However, the protocol would also need robust mempool-management strategies and clear rules for accepting unconfirmed coins.

Audience member: So there are still operational challenges around fee management and transaction propagation?

Borat: Yes. Those are important issues that would need to be addressed.

### Question 12: Is this protocol intended for immediate payments or cheaper transfers?

Audience member: It sounds as though the protocol is making a choice between immediate settlement and more efficient liquidity usage. Is that the trade-off?

Borat: The primary motivation is the liquidity problem.

I think of Lightning as a protocol particularly suited to vendors who need immediate settlement and have relatively predictable cash flows. A vendor can acquire liquidity and use it to accept payments.

The proposed protocol is more focused on ordinary users whose incoming payments may be unpredictable. They should be able to receive Bitcoin without first arranging inbound liquidity.

The two protocols have different strengths. The proposed protocol is intended to complement Lightning, not replace it.

Audience member: So Lightning prioritizes instant settlement, while this protocol prioritizes receiving payments without liquidity constraints?

Borat: That's a reasonable way to describe the distinction. The precise trade-offs depend on the implementation, especially the settlement guarantees and liquidity arrangements.

### Question 13: What happens if a user double-spends a coin?

Audience member: If a user tries to double-spend a coin, does the factory operator get the money?

Borat: The distinction is important. The scenario I described earlier concerns the factory operator double-spending a factory transaction, not the user simply trying to spend a coin twice.

Audience member: Could you explain how a normal payment works, starting with a coin in an existing factory?

Borat: Suppose you own Coin 0 in a confirmed factory, and it contains 100 satoshis.

You want to pay someone.

You join a new factory session with the same factory operator, because the coin is associated with that operator through a two-of-two arrangement.

You register Coin 0 as an input. You then register for the new payout coins and any change you need.

The old coin is consumed, and the new coins are created through the factory process.

The ATLC connects the old coin to a connector in the new factory. The user and operator exchange the necessary signatures, and the factory operator broadcasts the new factory transaction.

The new factory represents the payment and any change.

Audience member: Does the user have to use the same operator?

Borat: In the design as presented, yes. The existing coin is associated with a particular factory operator, and that operator participates in authorizing its spending.

The user would join a session with that operator to spend the coin. A different operator could be involved in subsequent arrangements, depending on how the protocol supports transfers between operators, but the initial spending relationship is with the operator associated with the existing coin.

Audience member: So the operator checks that I'm not spending the same coin twice?

Borat: The two-of-two authorization is intended to prevent a user from independently authorizing conflicting spends through the normal protocol path.

The factory operator also needs assurance that the old coin can be claimed under the required conditions after the new factory is created.

### Question 14: What incentive does the factory operator have not to cheat?

Audience member: Suppose I'm the factory operator. What's stopping me from allowing a double-spend if I stand to gain from it?

Borat: The construction is intended to provide a penalty mechanism. If the operator double-spends a factory, users who have the relevant prior spending history may be able to penalize the operator by recovering funds through the proposed cryptographic construction.

However, the penalty mechanism is optional in the broader design, and the precise guarantees depend on its implementation.

Without such a mechanism, users should not automatically treat an unconfirmed factory as fully settled. They need to consider confirmation status and the associated risks.

For example, a vendor can inspect the mempool and assess whether the factory transaction is likely to confirm. If the vendor requires stronger assurances, they can use Lightning or wait for the relevant confirmation conditions to be satisfied.

### Question 15: What exactly do connectors contribute to the penalty and atomicity mechanisms?

Audience member: I already have coins in a confirmed factory. If the factory operator tries to double-spend the factory, is the connector part of the mechanism that lets me recover my funds?

Borat: The connector commits to the transaction ID of the new factory. It links the spending of the old coin to the new factory.

If the factory operator double-spends the factory transaction, the connector commitment should no longer satisfy the required spending construction. That prevents the operator from claiming the old coin through the normal path.

The user can then use the appropriate script path to recover the funds.

The connector is therefore an important part of the atomicity mechanism. It gives the factory operator an assurance that the old coin can be claimed only when the new factory exists in the required form.

Audience member: So, without the connector, the operator could potentially spend the coin without having the required commitment to the new factory?

Borat: The connector is intended to prevent that problem. It links the two sides of the transfer and establishes the conditions under which the operator can claim the old coin.

The connector should not be confused with the optional penalty mechanism, though. They serve related but distinct purposes: the connector supports the atomic transfer construction, while the penalty mechanism is intended to provide additional assurances against certain forms of cheating.

### Closing

Moderator: Shall we continue with the remaining discussion?

Audience: Let's give the speaker a round of applause.

Borat: Thank you, everyone.

 Editorial notes on technical terminology

A few terms in the original speech-to-text transcript require verification against the recording or the speaker's slides before publication:

-ATLC: Retained as the speaker's proposed protocol primitive. Its exact expansion was not clearly established in the source transcript.
- APO, CTV and OP_CAT: Retained as Bitcoin script or covenant-related terminology. Their precise roles in the proposed construction need technical verification.
- PTLC, HTLC, MPP, CPFP and SIGHASH_ALL: Standard Bitcoin and Lightning terminology, retained and normalized where the intended meaning was clear.
- Factory expiry and recovery windows: The four-week factory lifetime and two-week sender-refund window are presented as design examples, not independently verified protocol specifications.
- Cryptographic security claims: The proposed penalty, atomicity, privacy and recovery mechanisms have been described as the speaker's intended design. This transcript should not be interpreted as an independent security audit or proof that those mechanisms work as claimed.


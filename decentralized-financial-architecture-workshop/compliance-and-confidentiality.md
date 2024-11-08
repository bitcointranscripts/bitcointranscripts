---
title: 'Compliance And Confidentiality: Can they co-exist?'
transcript_by: Bryan Bishop
tags:
  - regulation
speakers:
  - Alexander Zaidelson
---
# Introduction

Hi everyone. It's a great pleasure to be here. I'm Alexander Zaidelson, CEO of Beam. I'll be presenting our view on the regulation and how we live with it as a project. I'm not an expert in regulation. Whatever I'm showing here is how we see the landscape from what we understand.

Beam is a confidential transaction. The question is, how can confidential cryptocurrency co-exist with regulation?

# Agenda

What we'll talk about is the high-level regulatory landscape in the way that I see it. It might not be the true picture, but it will at least be from what I have learned. Then how it applies to crypto. Then we'll talk about Beam and Mimblewimble. I'll give a brief introduction to Mimblewimble which we're based on, and how it gives us a way to build an anonymous cryptocurrency. Then we'll talk about how we plan to approach compliance.

# Relevant regulations and regulators

There are many bodies defining regulators globally, in every country. Probalby the ones here are the most relevant. Like FATF, FSB, OECD, IOSCO, FSA, FinCEN, CFTC, SEC, NYDFS.

As far as I can tell, these are some of the key documents for compliance. It started in the 1970s with the Bank Secrecy Act which took away financial privacy and dictated that banks have to disclose certain information, as well as other financial institutions. FATF was an interbody task force defined with finding terrorism funding. It defined something called a "risk-based approach" which in my lay terms says that financial institutions should apply different levels of checks based on the risk presented by a certain customer or a certain transaction. We can constantly adopt this level of scrutiny based on the perceived risks.

Then this year, there was a lot of activity. There was the risk-based approach guidance by FATF document. The other is a FinCEN guidance about the application of regulations to crypto.

# What is required?

The bank secrecy act said that financial institutions have to keep records, and that they have to produce reports about transactions over a certain value. They have to file suspicious activity reports when they see something strange, and all transactions between foreign banks. The FATF risk-based approach I have already explained, where the more risk they perceive, the deeper they need to go in validating a customer and its transaction. The FATF RBA for virtual currencies and FinCEN guidance have a lot of details too.

# Who are the regulated actors?

In the Bank Secrecy Act, the regulated actors are any money service business or any business that deals or exchanges currency, check casher, issuer of traveler's checks, money orders, stored value, etc. etc. All of these entities need to make SARs and have to disclose information and hurt the privacy of their customers.

# What about crypto?

Crypto presents a fundamental challenge to the regulatory framework. In the traditional financial system, everything is centralized and reversible and every transaction-- you can send money or demand it back. There's restrictions, clarity of jurisdiction. But in crypto, it's all very different.

# Who is the regulator talking about in crypto context?

How does this regulation actually apply to crypto? The regulator here looks at four areas: money-service businesses, miners, developers and users.

# Who has regulatory obligations in crypto?

Exchanges, peer-to-peer like localbitcoins or OTC desks, custodial wallets (not your keys, not your coins). Crypto ATMs, DApps, mixers, crypto payment-processors, DEX's that don't auto-execute and take custody in the middle of the trade, ICO issuers who don't register with the SEC, mining pool operators who host all the wallets on behalf of pool members.

Basically, anyone who holds other people's money and transmits it-- even if the holding is for a few seconds. It has to report and do the risk-assessment based approach, and has to follow the AML guidance. Anyone who holds other people's money or transfers from one person to another. Anyone who has a business related to that, too.

# Who is exempt?

Some of the players are exempt. Trading platforms that are p2p and let people execute trades between themselves are exempt. We at Beam are building what we call a bulletin board system where people can publish offers for atomic swaps with bitcoin and beam and others. This is an example of a trading platform where parties settle by themselves. We're not facilitating the trade. We just let people connect with each other. We don't take or hold their money.

Mining pools are exempt unless they hold other people's money, and then there's software wallets which are also exempt. Some ICOs are exempt.

# Developers

To my relief, developers of any of those technologies are normally exepmt from any regulation. In the FATF and FinCEN documents, they mention that developers does not constitute a "VASP"--- or are exempt from BSA obligations. Now, if they run a business then they have to comply. But if they are just developing software, whatever it might be like a mixer or exchange software, then they are exempt. Which makes sense, only the people who are running a business or profiting from it should be held accountable to the regulations.

# What are the CDD/AML applications in crypto?

CDD is customer due diligence. Also some check of source of funds. In crypto, customer due diligence is pretty samiliar to the traditional financial system. Can you provide a passport, or as a company who are the ultimate beneficiary owners? But in crypto, there's another way. There's source of funds and blockchain analysis like with Chainalysis, Elliptic, Scorechain, Coinfirm, Ciphertrace, etc. They provide a way to do massive surveillance on the bitcoin blockchain. My understanding is that these companies have compiled large lists of known good and known bad wallet addresses on the blockchain. When a new transaction comes in, these companies look at the transaction graph and then they try to find some taint or bad addresses in the recent history. This is similar to how 90% of all dollars bills are tainted by cocaine. Once they find something, they raise a flag and their customer (such as a bank) will investigate and maybe decline service to that user. This all works in bitcoin, ethereum, and other blockchains.

# Anonymity

But here comes anonymity. We know today there are several confidential currencies. Beam is one of them. Monero was probably the first one. Zcash, Beam, Grin, zcoin, and there are some smaller projects out there. What the regulator says, and this is what FinCEN says, is that if a money transmitter accepts confidential currency it does not remove their obligation to do AML/KYC/CDD. So the actor accepting confidential cryptocurrency has the same obligations as one accepting regular currency. This causes them a problem because blockchain analysis doesn't work on confidential currencies and the heuristics don't work. That said, KYC/CDD probably works exactly the same way. You as a user register at an exchange, and that exchange can still validate my person in the same fashion regardless of whether I'm trading Beam or Bitcoin.

# The challenge of anonymous coins

But at some point, we see that it might become an issue. Blockchain analysis is not possible. The ban in Japan on confidential coins was not because the regulator wanted to track everything, or they were afraid of money laundering. But rather, it was because there was a big hack on exchanges and this included confidential coins so the government say that there was no way to track those coins. If bitcoin is stolen, at least they can try to retrieve it. But in confidential coins, there's no way you can retrieve stolen funds, so let's just ban them all together.

With the exception of Japan, most exchanges are trading confidential coins just fine right now. But it might become an issue in the future. It's a challenge because a regulator might come and say the AML measures apply to confidential coins aren't enough.

# Beam: a confidential cryptocurrency based on mimblewimble

<http://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2016-11-21-mimblewimble/>

I'll now talk on Beam and talk about how we want to combine confidentiality with potential compliance. So what is beam? It's based on a protocol called mimblewimble. Beam is a currency and a blockchain. There's no addresses. No single entity can be defined as a wallet that you can see on a blockchain. Transactions are confidential, and sender/receiver identities are not available. Amounts are not visible. Also, the blockchain doesn't store the history- not in an encrypted form or otherwise. There's no history on the blockchain.

Beam is built on this mimblewimble protocol where decentralized permissionless deflationary PoW-based currency, very similar to bitcoin in these regards. But it's also confidential.

So how does the Beam blockchain look? It's very simple but here's the idea. The blockchain actually contains just the current state of all the UTXOs. You can see a list of UTXOs that are not yet spent. Every user has keys to his or her safe deposit box. There is no way to look at a safe deposit box and understand who it belongs to or connect that different boxes belong to the same numbers. It all looks like random digital garbage. Only the user with the key can open the box and transact with it.

To build a transaction, Alice takes one of her transactions and starts to communicate with Bob. This is a special thing about the protocol. Transactions are built by two parties cooperating together. They need to talk together to build the transaction. In bitcoin, you can push coins without the other party. But in Beam, the two wallets need to cooperate to build a transaction. Alice takes a UTXO, tells Bob that she wants to send a certain amount. Bob creates a new UTXO for himself with the right values. Alice also can send some coins to change. They both sign the transaction and they prove that the sum of inputs equals the sum of outputs so that there's no inflation in the system, to make sure no new funds are created in the system. We prove that it all sums to zero, then we prove the numbers are all positive. Then this gets sent to the blockchain, miners validate this, and then this becomes a new state of the blockchain.

The mimblewimble blockchain just states the current status of all the UTXOs. You can view the mimblewimble blockchain as one huge transaction from the mined coins to the current status. For each transaction, there is a "transaction kernel" construct which contains the difference between the blinding factors and the signature. This kernel is stored in the blockchain forever. This is how mimblewimble works.

# Beam: A hybrid approach

How can we concile the privacy of a protocol like this, with compliance requirements? How can we present some information to a regulator proving that a transaction has happened or proving source of funds?

We want to combine privacy with opt-in auditability and give the users the choice. The idea is that the users who want to report, or want to have a history, they would willingly create that history that will be stored off-chain. But it will reference the blockchain, or reference a specific transaction kernel and this kernel would contain for example the hash of all the meta data related to a transaction like who sent what to who. It's similar to cash. The private users with small amounts will stay completely private and not need to create the history. Businesses and large accounts will be opt-in auditable.

# Beam and compliance

We identified two kinds of audit trails that we see. One is vertical audit trails, meaning that I show a complete list of transactions and for each transaction I can demonstrate the collateral document. Remember, in mimblewimble, transactions are a two-party interactive protocol. I can demand the second party gives me an invoice. I can prove to an auditor that this particular transaction occurred against this particular individual. There's also horizontal audit trail where, you can show the provenance of funds for AML compliance, showing where a specific coin came from. It creates a history of each coin in a sense.

We envisioned that this functionality would be available not as part of the basic blockchain, but as part of a separate piece of wallet called business wallet which may not be a commercial projcet itself. There's no way to enforce this compliance on anyone, so only users that install this wallet will be able to create this history. The people who don't want to do that will not use this wallet and will not create any history.

# Building blocks

What are the building blocks we envision?

Those business wallets we can each give them an identity. This can be a KYC certificate or a verifiable credential. The wallet can then attach a hash of this identity to every transaction it performs. It's possible to loo kat the blockchain using a special auditor key and find transactions that belong to this particular wallet.

For each transaction, the wallet can also co-sign a set of papers or invoices or contracts whatever's necessary or required. Once we get down to the implement, we'll see what the necessary documents are. The idea is that we can add documentation or proof that the transactions really happened.

All the metadata will be stored offline. In mimblewimble, it's possible to add more than one kernel to the blockchain. These kernels can contain the hashes of all the metadata and it will be possible to prove that certain transactions occurred according to certain rules.

We can chain the history of any particular coin using these techniques. The information will be encrypted so that only a certified and agreed-upon risk assessor will have this information. This information will not be public, and it will be encrypted and only available to people with special keys which could be shared with the owners.

We call this deterministic compliance. This is a far more technical way of doing compliance.

We want to have a co-signed piece of information saying a certain amount was sent at a certain time to another address. In a confidential coin, I might send you some funds, but you might deny that or say it was a different amount. So we need to make a proof-of-payment. Without the three, it's very hard to expect businesses to really use something as a means of payment. Without confidentiality, it's really hard for a business to operate.

# Challenges

We need to minimize disclosure to an absolute minimum. There's also a challenge with the depth of the transaction graph. There's a lot of information required to comply. There's also the issue of transactions between audited and unaudited wallets. In the real world, coffee shops don't need to provide any provenance of funds for this cash they receive in small amounts. The other challenge is the adoption of this whole paradigm by the industry.

# Questions

Q: You said in the beginning that developers aren't regulated. But we've already seen that the SEC sued the developer of Etherdelta last year.

A: He was operating it as well, he was running it as a business from what I understand. Being a developer does not give you immunity.

Q: He was managing the website. Like you said, you're going to facilitate other people's transactions.

A: He was collecting fees. He was running a business. Like 0.2%/trade.

Q: So if you profit from inflation instead of collecting fees, does that make you vulnerable to regulation?

A: It's a good question, but the FinCEN guidance said that people running a marketplace or where people can meet and exchange directly, are exempt. They are exempt from the Banking Secrecy Act requirements. This means that I don't have to do KYC to the customers nor AML. It's not my problem. There might be other issues though. We're just developing software and letting it out there. We hsouldn't be responsible in that case.

Q: What to do about stale keys? The auditor key might get stolen. So the audit key should only be given to the auditor when the auditor asks about a specific transaction, right?

A: The mitigation is that the auditor needs both the kernels (on-chain data) and also off-chain data. So this somewhat mitigates the problem. But yes, if the key gets stolen, and the data stolen, you need to do rotation.

Q: What about real-time monitoring of an exchange's customers and how they are transacting?

A: Internally, an exchange has all of the data anyway. The only problems are about when the coins come in and where they go after withdrawal. I don't think that's a requirement of the regulations really. We let users choose whether they want to submit to this regulation. Once you install the business wallet, and give your key to the auditor, then they can monitor your activity. You can't enforce that; a user could install a standard wallet and do whatever they want.

Q: I am not sure the regulator is comfortable with that choice being available.

A: Our stance is that privacy is a basic human right. It's very hard to say, you can't use confidential coins. How are you going to enforce that? They are confidential. So there's no way to do that really. It won't work. We want to create a system similar to cash where it's my responsibility. Law enforcement is responsible for catching bad guys, regardless of what they do, but not at the cost of privacy for everyone else.

Q: Regulators have different opinions. In that case, we need to talk more.

A: Yeah, they want more control. They would prefer to see everything all the time. We need to find a balance. We think that what we envision is a good balance.

Q: It might be too idealistic, but we want to catch criminals and put them in jail. We don't need to know everything. If we can identify criminals, without knowing the details, that's the best scenario. If there are any solutions for that, to minimize the privacy exposure but still identify criminals. Without active monitoring and surveillance, it's still difficult to catch criminals.

A: I agree it's a philosophical question. Law enforcement needs to find ways to catch criminals without hurting everyone else's privacy. The tech is moving forward and hopefully more privacy is being added. Law enforcement should find other ways to catch criminals.

Q: Well, then regulators will enforce more sanctions and more regulations. We need to discuss better solutions together and find a middle ground. We need to get together to find out how much privacy is needed, agree on a basic concept, and then create a solution together. Not just technology, but also regulations.

A: I think technology is moving faster. They will need to catch up. You can't stop technology.

Q: Yes, you can't stop technology. That's a challenge we are facing.

Q: In Prague, their receipts have an ID for citizens to verify that the restaurants are paying taxes on the bill against a city database later.

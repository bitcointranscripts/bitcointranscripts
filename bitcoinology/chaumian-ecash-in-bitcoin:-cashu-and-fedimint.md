---
title: 'Chaumian eCash in Bitcoin: Cashu & Fedimint'
transcript_by: 'dillamondgoat via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=VwMzNE1D3so'
date: '2022-10-18'
tags:
  - 'ecash'
speakers:
  - 'Adam Gibson'
categories:
  - 'meetup'
body: "## INTRODUCTION\n\nAdam: Hello everyone.\nToday we're talking about Chaumian eCash.\nI'm going to mix up the terms \"mint\" and \"bank\" often because, to me, they are the same thing in this situation.\nThis is going to be a rambling talk.\nI'll try to limit it to no more than an hour or an hour and a half.\nAs we get towards the end of that time, I would expect more of you to ask questions and start talking about it.\nI'm going to get quite theoretical in some parts, but the really interesting questions are more about the practicality of this.\nCryptography is fascinating, but everyone should be interested in the question of whether this is actually useful and how it is useful.\nWe can start discussing that as we get further into it.\nTo start with, we need to have some motivation, so I put this section at the start of my notes.\n\n---\n\n## What is Chaumian Cash?\n\nAdam: These are just notes, not a proper presentation.\nThis is the result of me reading about this stuff for about one week.\nI'm probably going to make some mistakes and there will be some holes in what I say.\nIf anyone knows of mistakes or can correct me, please go ahead.\nFeel free to interrupt at any time, or ask if you're confused.\nWhat is the motivation for having a Chaumian eCash system?\nBefore explaining what it is, I'm going to talk about why it might be useful.\nIt is more scalable and faster.\nMost of you are familiar with the concept that a centralized system is much easier to make scalable and performant.\nWe can have a single database, perhaps replicated like big tech companies, and handle thousands or millions of queries per second.\nEverything is fine because there's no issue of consensus or people falling out of consensus.\nIt should be more scalable if we have a centralized system.\nI've also noted that there are not enough UTXOs.\nDoes anyone know what I mean by that?\n\nAnon: Is it possible to make enough UTXOs for everyone in the world to have one?\n\nAdam: Exactly.\nThat's the basic point.\nThe UTXO, the unspent transaction output in Bitcoin, must be stored in the blockchain.\nEvery node has to have a database of all existing UTXOs to check whether a spending event is valid.\nThere are currently tens of millions of UTXOs.\nHowever, there are not billions of UTXOs.\nIt isn't really feasible for Bitcoin to have billions of UTXOs so that everyone can have one, especially since each person really needs more than one.\nThat's a problem, which is one of the reasons why Lightning exists.\nLightning addresses this scalability issue, but since every Lightning channel needs a UTXO, you almost have the same problem.\nIt's better, and in the future, it could get even better, but it's unlikely we'll ever reach a point where we can have tens or hundreds of billions of Lightning channels.\nIt's not realistic.\nA centralized system can address the scalability problem.\nWhat makes this digital cash system \"eCash\" or \"Chaumian eCash\" is specifically the privacy property.\nIf there's one thing you take away, it's that Chaumian eCash was designed from the start by David Chaum to be untraceable.\nHe literally used the word \"untraceable.\"\nIt would not be politically convenient to tell regulators today that you've invented an untraceable form of digital cash.\nBut back in the 80s when he first came up with the idea, that's what he had in mind.\nIt provides very strong privacy in the sense that the bank or the mint, which owns the token, cannot easily link the money.\nWhen the mint sees money coming in, it can't tell who originally got that money issued.\nThe third point is the security model.\nIt has the same or better theft security model than a Trusted Third Party (TTP), but it is much worse than a blockchain.\nIf this mint is a centralized database, you might think it's already a TTP.\nI'm comparing it with something like Coinbase or a company that stores your Bitcoin.\nIf you give your coins to Coinbase, they are a trusted third party because they hold your coins.\nThis has a similar security model, but it's also a little different.\nThe big difference is that you actually hold the coins yourself.\nIt's a weird gray area.\nYou go to this mint and ask for one coin in exchange for something.\nThey give you one coin and you hold it on your mobile phone or computer.\nThey don't hold it.\nOn the other hand, they control the whole database of the coins.\nThey can decide at any time not to accept your coin or they could create 100 more coins that you don't know about.\nIt's much worse than a blockchain because the Bitcoin model is that you hold the private keys.\nDue to the distributed nature of consensus and proof of work, you believe there's a global immutability being enforced.\nThere isn't another person who can just say your coins don't exist or create a million new ones.\nDoes that make sense so far?\nIf it's so great, why hasn't it been done yet?\nDoes anyone want to take a stab at answering that?\nIf Chaumian eCash is scalable and private, why hasn't it been done?\n\nAnon: I would say it's because it was tied to physical assets like dollars or gold.\nIt creates a centralized target that governments can shut down, which happened with e-gold.\nBitcoin brings something that has value but isn't something you can go and catch.\nThat's why it's interesting to apply this on top of Bitcoin.\n\nAdam: Right. Any other thoughts?\n\nAnon: Is it something to do with Schnorr signatures and their licensing?\n\nAdam: Actually, that was part of my research.\nSeveral cryptographic algorithms, including RSA, had patents around them.\nI suspect that's a small part of the story, but it's not irrelevant that developing these systems was stymied by legal restrictions.\n\nAnon: Didn't Wasabi use something like this in their back end?\nDoes that mean it has been done?\n\nAdam: That's another valid answer.\nIt has been done multiple times in different ways.\nI wouldn't say Wasabi was an implementation of eCash, but it was an implementation of Chaumian blinding.\nIt is very related.\n\nAnon: Does Mercury also have that?\n\nAnon: It has the same token concept.\n\nAdam: There are some gray areas here between tokens and coins.\nWe'll see another one later.\n\nAnon: What's the answer? Why hasn't it been done?\n\nAdam: There's no simple answer, and we'll keep addressing it as we go along.\n\nAnon: Is it fair to say the use cases are more suitable for later adopters rather than earlier adopters because of the inherently centralized aspect?\n\nAdam: The bootstrapping mechanism you have in Bitcoin is difficult in centralized systems.\nThe classic problem is: if I make a new Proof of Stake coin, who has all the coins at the start?\nIf I get them all, it's a poor system.\nCentralization doesn't solve that problem, which is one of the clever things about Bitcoin.\n\n---\n\n## History - David Chaum's original papers: Blind Signatures for Untraceable Payments\n\nAdam: A proper understanding of anything involves studying its history.\nThe concept of digital cash goes back a long way.\nAfter the advent of public key cryptography—whether you attribute it to Clifford Cocks and GCHQ or Whitfield Diffie and the RSA guys in the 70s—we got public key cryptography on computers.\nThe asymmetric nature allowed for high-strength cryptographic primitives without pre-agreeing on secret key material.\nI can make my GPG public key and everyone can verify that I wrote the code.\nChaum was one of the key people in this field.\nHe was a genius in terms of seeing elegant and powerful ways to use these new cryptographic constructions.\nYou know you're going deep into cryptography when you start reading papers that were written on typewriters.\nI recommend reading this paper; it's only a few pages and there's very little mathematics in it.\nHe described his idea in terms of a secret ballot election over the mail.\nHe explains the concept of blinding and how it solves the problem of keeping a ballot secret while verifying it's from a valid voter.\nYou can do that with carbon paper and envelopes.\nInside an envelope, you put a piece of paper.\nYou sign the top of the envelope and that signature carries through onto the carbon paper inside.\nHe explains that we can do the same thing with mathematics.\nHe doesn't even talk about RSA in this version; he just talks about one-way functions.\nHe also anticipates the debates we have today, noting that ordinary users do not want all of their financial information exposed.\nHe anticipated that commerce over these channels would expose tons of information to thieves and people we don't want to know.\nBut he also says this could be exploited by criminals.\nHe suggests these systems can support auditing.\nHe imagined a centralized bank-based system where people keep high privacy, comparing it to physical cash notes.\nHe believed we could ensure criminals don't take advantage because systems can be audited.\nWhenever you have privacy-preserving systems, you can always insert voluntary auditing.\nIf I use a CoinJoin, Confidential Transactions, Zcash, or Monero, there's always a way for me to reveal a particular key to show the tracing of coins.\nChaum was not one of the Cypherpunks.\nThe Cypherpunks started with a bunch of futurists in California who were libertarian-leaning and wanted to minimize state power using cryptography.\nPeople like Jim Bell came up with assassination markets to anonymously pay for someone to be assassinated.\nChaum was outside of that; he was in the camp of cryptographers who believed this would help the human condition but didn't want to challenge state power.\nThe initial presentation of the idea was based on RSA.\nBasically, you can take a signature and multiply it by a number to make it a random number.\nYou can sign with the randomness added and then unblind it.\nThe mint was envisioned as a bank or a trusted institution.\nCrucially, in this model, the transfer of coins has to be mediated by the bank.\n\n---\n\n## How does an eCash Mint/bank work?\n\nAdam: What does it mean that transfers are mediated?\nPerson A has some coins issued.\nYou ask the bank for one eCash dollar.\nTo get that, you deposit something with the bank.\nWhen Person A wants to pay Person B, they send that eCash dollar.\nThis is different from Bitcoin.\nYou have a long string of numbers—a big number—and you give that number to another person.\nThe obvious problem is that data can be copied.\nI can't give you the number 25 and claim I don't own it anymore.\nThis is the double-spending problem.\nAll this talk about double spending in Bitcoin started with the idea of digital cash.\nThis is an online transfer model.\nPerson B accepts that number as money by verifying it with the bank.\nThey send the number to the bank, and the bank checks the database.\nWhat does the bank check?\n\nAnon: It must have a database that 25 equals one dollar.\n\nAdam: Almost.\n\nAnon: They check who had it last so the person hasn't spent it before.\n\nAdam: They check that the coin was never spent before.\nIt's the opposite of Bitcoin in the sense that you have a list of spent coins rather than unspent coins.\nIf they can verify it's a valid signature and it's not on the spent list, they add it to the list and Person B accepts it as money.\nI'm oversimplifying because there is also blinding and signing involved.\nThis model requires the receiver to be online and contact the bank for every transfer.\nChaum, Fiat, and Naor produced another paper addressing this.\nThey suggested a solution based on \"cut and choose,\" a probabilistic cryptographic protocol.\nIt involved generating many possibilities and relying on statistics to ensure the protocol was followed.\nThe problem was the large amount of data and interactivity required.\nThe goal was for Person B to receive something and be assured A wouldn't double spend it.\nBut they could never be fully assured immediately.\nThe idea was that if A tried to double spend, they would actually reveal that they had cheated via this protocol.\nThis enables offline payments based on game theory, but it only works if there are individual identities to blame.\nIf every spend is anonymous, you have no one to blame.\n\n---\n\n## Blind signing\n\nAdam: Let's go into more detail on how this works.\nWhat is a blind digital signature?\nThe person making the signature doesn't know what message they are signing.\nWould you sign something if you didn't know what it was?\nIn this application, you don't know the message.\nImagine Tracy wants one dollar worth of eCash.\nShe has a secret number and wraps it inside a container—an \"envelope.\"\nShe asks the bank to sign it.\nThe bank signs the envelope and gives it back.\nTracy opens the envelope and has her secret number, but the signature has passed through onto that secret number.\nTracy now holds a secret number the bank never saw, plus a signature on it.\nThat is her coin.\n\n---\n\n## Denominations\n\nAdam: Tracy has her secret number signed, but what does it represent?\nDoes it represent 100 dollars or one?\nEach signature corresponds to a specific denomination.\nThe bank has different public keys for different values: a one-dollar public key, a two-dollar key, a four-dollar key, and so on.\nMost original implementations used powers of two.\nIf you want 17 dollars, you ask the bank for a 16-dollar token and a one-dollar token.\nIt's exactly like physical cash.\nIf you have a 16 and a one and you want to pay 13, you have to ask the mint for change.\nYou give them tokens and they give you new tokens, which you re-blind.\nA coin is a bearer instrument.\nIn Bitcoin, you hold private keys that control coins.\nIn eCash, the coins themselves are the value.\n\n---\n\n## Stefan Brands's Paper - Untraceable Online Cash in Wallets with Observers\n\nAdam: In the 90s, Stefan Brands—who was a student of Chaum's—developed a system that was mathematically more elegant.\nAdam Back will never stop talking about Stefan Brands.\nHe used a trick similar to what we see in Discrete Log Contracts (DLCs).\nA signature $\\sigma$ on a message $m$ for a public key $P$ usually involves a nonce $R$.\nIn DLCs, the nonce is fixed in advance.\nIf an oracle makes two signatures for two outcomes with the same nonce, they reveal their private key.\nBrands used a similar algebraic principle.\nIf a person tried to double spend, they would end up revealing a certain key.\nBut this still had the problem that you need an identity to blame.\nIt's difficult to have privacy in a system where all users are listed.\nTo make it offline, there were ideas about tamper-resistant hardware like smart cards.\nIn his paper, Brands described an \"observer\" in the wallet that would prevent double spending.\nIf someone hacked the hardware, they would still be found out via the blame protocol.\n\n---\n\n## Real world instantiations / History of Chaum's eCash via DigiCash Inc.\n\nAdam: The most famous example is DigiCash.\nIn the mid-90s, DigiCash was a company based on Chaum's papers.\nNick Szabo and Zuko Wilcox were involved.\nIt was literally what we discussed: your interface showed your coins in different denominations.\nWhy aren't we all using it?\nSome people confuse it with e-gold or Liberty Reserve, which were shut down.\nDigiCash was more about bankruptcy and internal politics.\nThere is a fascinating article by a Dutch journalist titled \"How DigiCash Blew Everything.\"\nIt describes David Chaum as having legendary suspicion.\nHe reportedly scuppered business deals, including one with Bill Gates, by changing his mind at the last minute.\nUltimately, it was a failure of centralization.\nMoney created by a company is a category error.\nPayment rails are one thing, but creating an actual currency is another.\n\n---\n\n## Laissez-faire city / Digital Monetary Trust\n\nAdam: There were other libertarian experiments like Laissez-Faire City in Puerto Rico.\nThey had the Digital Monetary Trust and an eCash system developed by J. Orlin Grabbe.\nHis article \"The End of Ordinary Money\" is a great read.\nMost of these experiments eventually collapsed.\n\n---\n\n## Open Transactions\n\nAdam: In the early days of Bitcoin, around 2014, people were interested in financial cryptography libraries like Open Transactions.\nThey wanted to do eCash tokens, move Bitcoin around, and use Ricardian contracts.\nProjects like True Ledger and Lucre by Ben Laurie also existed.\nMany people tried, but nobody really succeeded.\nIn the 90s, you would have needed a massive database to control the coins and a constant internet connection, which didn't exist for that kind of traffic.\n\n---\n\n## Hal Finney's RPOW\n\nAdam: We should mention Hal Finney's RPOW (Reusable Proofs of Work).\nIt was a step towards Bitcoin.\nHe suggested that if we had trusted hardware, we could use the work done by the hardware as a currency.\nThis was more of a Cypherpunk attempt to make money independent of the state.\n\n---\n\n## Compact eCash\n\nAdam: In 2006, Lysyanskaya and Camenisch published \"Compact eCash.\"\nThis was a technical improvement to make systems more scalable.\nA whole wallet could be about the same size as one coin.\nIt used bilinear pairings and the strong RSA assumption.\nIt was still in the model of proving double spending after the fact, which requires identities.\n\n---\n\n## Why you need identities to blame?\n\nAdam: What does it mean to blame someone if every event is anonymous?\nIf I pay you for a car with a double-spent coin, you are stuck.\nIf my account is registered and my identity is revealed upon double spending, the bank can block me.\nWithout a trusted third party, you end up back at the distributed system problem that Bitcoin solved.\n\n---\n\n## Matthew Green's eCash blog post 2010\n\nAdam: Matthew Green is a cryptographer at Johns Hopkins.\nIn 2012, he wrote a post about eCash designs.\nHe noted that Bitcoin was interesting but its privacy properties were terrible.\nA year later, he was a key driver behind Zerocoin, which developed into Zcash.\nZcash uses ZK-SNARKs to prove a coin is valid without revealing its source.\n\n---\n\n## Schnorr Blind Signatures\n\nAdam: This gets a bit more technical.\nNadav Kohen has some good write-ups on blind signature protocols for Schnorr.\nIn basic Schnorr, there is a nonce, a challenge, and a response.\nTo blind it, you add a random number to the challenge so the signer cannot see the message.\nIn normal Bitcoin, you don't interact with anyone to sign a transaction.\nBlind signing is intrinsically interactive.\nYou end up with a valid signature $(R, s)$ on your message $m$ which you can unblind.\nHowever, there are serious security concerns like Wagner's attack and the ROS attack.\n\n---\n\n## Wagner's attack & The Birthday Paradox\n\nAdam: The birthday paradox says that in a group of 23 people, there is a 50% chance two share a birthday.\nCollisions are more common than your intuition suggests.\nIn Wagner's attack, instead of finding $A - B = 0$, you find $k$ things that add up to zero.\nThis $k$-sum problem is remarkably easy to solve even for large numbers.\nYou can use this to attack protocols like Schnorr blind signatures.\nIf you do hundreds of signing sessions in parallel, you can crack keys or forge signatures more quickly than expected.\nSpecifically, an attacker might get a mint to output 101 coins from 100 parallel signing sessions.\n\n---\n\n## One-more-forgery EUF-CMA\n\nAdam: In standard signatures, we want EUF-CMA (Existential Unforgeability under Chosen Message Attack).\nThis means you cannot produce a signature without the key, even if you've seen many other signatures.\nIn blind signatures, this doesn't make sense because the signer never chooses the message.\nInstead, we use the \"one-more-forgery\" model.\nThe goal is to ensure you cannot get 11 signatures when the signer thinks they only gave you 10.\n\n---\n\n## Cashu\n\nAdam: Cashu doesn't use Schnorr or RSA.\nThe genesis was a post by David Wagner suggesting a blind eCash scheme using Diffie-Hellman key exchange to avoid RSA patents.\n\n---\n\n## Diffie-Hellman key exchange\n\nAdam: In Diffie-Hellman, Alice has a private key $a$ and public key $A = aG$. Bob has private key $b$ and public key $B = bG$.\nThey can calculate a shared secret:\n$$s = aB = bA = abG$$\nThis principle is used for TLS on the internet (ECDH).\n\n---\n\n## Blind Diffie-Hellman key exchange\n\nAdam: CalleBTC recently created a protocol summary for this.\nYou put your secret in an \"envelope\" by adding an additive tweak $r$.\nThe mint (Bob) multiplies your blinded value by his private key $k$.\nWhen you receive it, you subtract $r \\cdot K$ to unblind it.\nThe result is a value $Z$ that the bank signed.\nThis is reducible to the Computational Diffie-Hellman (CDH) assumption.\nIf you believe you cannot calculate the shared secret without a private key, the system is protected against one-more-forgery.\n\n---\n\n## Privacy Pass\n\nAdam: This is exactly the same logic used in Privacy Pass.\nWhen you use Tor, you encounter captchas constantly.\nPrivacy Pass lets you do a captcha once and receive tokens.\nYou spend these blinded tokens to prove you've done the captcha without revealing your identity.\nCashu and Privacy Pass are both based on CDH.\nCashu is a new project leveraging Lightning.\nIf you want to mint 420 sats, it sends you a Bolt 11 invoice.\nIt's very bare-bones currently, but it's an exciting development.\n\n---\n\n## Fedimint\n\nAdam: Fedimint has been around longer.\nAt its root is a federation of \"guardians.\"\nYou trust a threshold, such as five out of nine people.\nIf one goes rogue or offline, you're okay.\nThe federation controls a multisig that holds the Bitcoin.\nDepositing into that multisig entitles you to eCash tokens.\nTo the user, the interface should be simple and reminiscent of using Lightning.\n\n---\n\n## Threshold Blind Signatures\n\nAdam: Fedimint's innovation is threshold blind signing.\nIf you threshold sign a blinded message without consistency, it fails.\nIf Person A signs $M_1$, Person B signs $M_1$, and Person C signs $M_2$, the user might end up with more coins than issued.\nTo prevent this, the system needs a Byzantine Fault Tolerant (BFT) consensus system, specifically Honey Badger BFT.\n\n---\n\n## BLS signatures\n\nAdam: Fedimint uses BLS signatures rather than Schnorr.\nThey require specific elliptic curves and are deterministic.\nYou can aggregate many signatures into one, which is very compact.\nThe downside is that verification is computationally expensive because it requires \"pairing.\"\n\n---\n\n## Lightning gateways in Fedimint\n\nAdam: A Lightning Gateway is a user of the mint that connects the federation to the outer Lightning Network.\nThey trade \"Fedi Sats\" (tokens) for Bitcoin payments.\nIt's as private as any Lightning payment.\nThis allows users within the federation to pay people on the Lightning Network and vice versa.\n\n---\n\n## Risks and tradeoffs of Fedimint\n\nAdam: The main risk is the federation itself.\nIf a threshold (e.g., five of nine) goes rogue, they can steal the Bitcoin in the multisig.\nThey could also generate infinite eCash tokens.\nCurrently, there is no auditability of the total supply.\nWe want auditability without sacrificing privacy.\nThere are ideas like Merkle trees with Pedersen commitments, but it's a complicated area.\n\n---\n\n## Perfect Privacy\n\nAdam: eCash privacy has a \"perfect\" quality.\nComputational privacy (like Bitcoin keys) can be broken with enough computing power.\nPerfect privacy is like a one-time pad.\nIf I give you my message $M$ plus a random number $R$, you can never find $M$ because there are infinite possible messages with corresponding random numbers.\nThis is a bearer instrument.\nIf you lose your phone, your coins are gone.\nFedimint pitches \"community custody\" where you can ask people you know to help recover funds.\nYou could encrypt your backup with the guardians.\nThat's all we have time for today.\n\nAdam: Thank you."
---

## INTRODUCTION

Adam: Hello everyone.
Today we're talking about Chaumian eCash.
I'm going to mix up the terms "mint" and "bank" often because, to me, they are the same thing in this situation.
This is going to be a rambling talk.
I'll try to limit it to no more than an hour or an hour and a half.
As we get towards the end of that time, I would expect more of you to ask questions and start talking about it.
I'm going to get quite theoretical in some parts, but the really interesting questions are more about the practicality of this.
Cryptography is fascinating, but everyone should be interested in the question of whether this is actually useful and how it is useful.
We can start discussing that as we get further into it.
To start with, we need to have some motivation, so I put this section at the start of my notes.

---

## What is Chaumian Cash?

Adam: These are just notes, not a proper presentation.
This is the result of me reading about this stuff for about one week.
I'm probably going to make some mistakes and there will be some holes in what I say.
If anyone knows of mistakes or can correct me, please go ahead.
Feel free to interrupt at any time, or ask if you're confused.
What is the motivation for having a Chaumian eCash system?
Before explaining what it is, I'm going to talk about why it might be useful.
It is more scalable and faster.
Most of you are familiar with the concept that a centralized system is much easier to make scalable and performant.
We can have a single database, perhaps replicated like big tech companies, and handle thousands or millions of queries per second.
Everything is fine because there's no issue of consensus or people falling out of consensus.
It should be more scalable if we have a centralized system.
I've also noted that there are not enough UTXOs.
Does anyone know what I mean by that?

Anon: Is it possible to make enough UTXOs for everyone in the world to have one?

Adam: Exactly.
That's the basic point.
The UTXO, the unspent transaction output in Bitcoin, must be stored in the blockchain.
Every node has to have a database of all existing UTXOs to check whether a spending event is valid.
There are currently tens of millions of UTXOs.
However, there are not billions of UTXOs.
It isn't really feasible for Bitcoin to have billions of UTXOs so that everyone can have one, especially since each person really needs more than one.
That's a problem, which is one of the reasons why Lightning exists.
Lightning addresses this scalability issue, but since every Lightning channel needs a UTXO, you almost have the same problem.
It's better, and in the future, it could get even better, but it's unlikely we'll ever reach a point where we can have tens or hundreds of billions of Lightning channels.
It's not realistic.
A centralized system can address the scalability problem.
What makes this digital cash system "eCash" or "Chaumian eCash" is specifically the privacy property.
If there's one thing you take away, it's that Chaumian eCash was designed from the start by David Chaum to be untraceable.
He literally used the word "untraceable."
It would not be politically convenient to tell regulators today that you've invented an untraceable form of digital cash.
But back in the 80s when he first came up with the idea, that's what he had in mind.
It provides very strong privacy in the sense that the bank or the mint, which owns the token, cannot easily link the money.
When the mint sees money coming in, it can't tell who originally got that money issued.
The third point is the security model.
It has the same or better theft security model than a Trusted Third Party (TTP), but it is much worse than a blockchain.
If this mint is a centralized database, you might think it's already a TTP.
I'm comparing it with something like Coinbase or a company that stores your Bitcoin.
If you give your coins to Coinbase, they are a trusted third party because they hold your coins.
This has a similar security model, but it's also a little different.
The big difference is that you actually hold the coins yourself.
It's a weird gray area.
You go to this mint and ask for one coin in exchange for something.
They give you one coin and you hold it on your mobile phone or computer.
They don't hold it.
On the other hand, they control the whole database of the coins.
They can decide at any time not to accept your coin or they could create 100 more coins that you don't know about.
It's much worse than a blockchain because the Bitcoin model is that you hold the private keys.
Due to the distributed nature of consensus and proof of work, you believe there's a global immutability being enforced.
There isn't another person who can just say your coins don't exist or create a million new ones.
Does that make sense so far?
If it's so great, why hasn't it been done yet?
Does anyone want to take a stab at answering that?
If Chaumian eCash is scalable and private, why hasn't it been done?

Anon: I would say it's because it was tied to physical assets like dollars or gold.
It creates a centralized target that governments can shut down, which happened with e-gold.
Bitcoin brings something that has value but isn't something you can go and catch.
That's why it's interesting to apply this on top of Bitcoin.

Adam: Right. Any other thoughts?

Anon: Is it something to do with Schnorr signatures and their licensing?

Adam: Actually, that was part of my research.
Several cryptographic algorithms, including RSA, had patents around them.
I suspect that's a small part of the story, but it's not irrelevant that developing these systems was stymied by legal restrictions.

Anon: Didn't Wasabi use something like this in their back end?
Does that mean it has been done?

Adam: That's another valid answer.
It has been done multiple times in different ways.
I wouldn't say Wasabi was an implementation of eCash, but it was an implementation of Chaumian blinding.
It is very related.

Anon: Does Mercury also have that?

Anon: It has the same token concept.

Adam: There are some gray areas here between tokens and coins.
We'll see another one later.

Anon: What's the answer? Why hasn't it been done?

Adam: There's no simple answer, and we'll keep addressing it as we go along.

Anon: Is it fair to say the use cases are more suitable for later adopters rather than earlier adopters because of the inherently centralized aspect?

Adam: The bootstrapping mechanism you have in Bitcoin is difficult in centralized systems.
The classic problem is: if I make a new Proof of Stake coin, who has all the coins at the start?
If I get them all, it's a poor system.
Centralization doesn't solve that problem, which is one of the clever things about Bitcoin.

---

## History - David Chaum's original papers: Blind Signatures for Untraceable Payments

Adam: A proper understanding of anything involves studying its history.
The concept of digital cash goes back a long way.
After the advent of public key cryptography—whether you attribute it to Clifford Cocks and GCHQ or Whitfield Diffie and the RSA guys in the 70s—we got public key cryptography on computers.
The asymmetric nature allowed for high-strength cryptographic primitives without pre-agreeing on secret key material.
I can make my GPG public key and everyone can verify that I wrote the code.
Chaum was one of the key people in this field.
He was a genius in terms of seeing elegant and powerful ways to use these new cryptographic constructions.
You know you're going deep into cryptography when you start reading papers that were written on typewriters.
I recommend reading this paper; it's only a few pages and there's very little mathematics in it.
He described his idea in terms of a secret ballot election over the mail.
He explains the concept of blinding and how it solves the problem of keeping a ballot secret while verifying it's from a valid voter.
You can do that with carbon paper and envelopes.
Inside an envelope, you put a piece of paper.
You sign the top of the envelope and that signature carries through onto the carbon paper inside.
He explains that we can do the same thing with mathematics.
He doesn't even talk about RSA in this version; he just talks about one-way functions.
He also anticipates the debates we have today, noting that ordinary users do not want all of their financial information exposed.
He anticipated that commerce over these channels would expose tons of information to thieves and people we don't want to know.
But he also says this could be exploited by criminals.
He suggests these systems can support auditing.
He imagined a centralized bank-based system where people keep high privacy, comparing it to physical cash notes.
He believed we could ensure criminals don't take advantage because systems can be audited.
Whenever you have privacy-preserving systems, you can always insert voluntary auditing.
If I use a CoinJoin, Confidential Transactions, Zcash, or Monero, there's always a way for me to reveal a particular key to show the tracing of coins.
Chaum was not one of the Cypherpunks.
The Cypherpunks started with a bunch of futurists in California who were libertarian-leaning and wanted to minimize state power using cryptography.
People like Jim Bell came up with assassination markets to anonymously pay for someone to be assassinated.
Chaum was outside of that; he was in the camp of cryptographers who believed this would help the human condition but didn't want to challenge state power.
The initial presentation of the idea was based on RSA.
Basically, you can take a signature and multiply it by a number to make it a random number.
You can sign with the randomness added and then unblind it.
The mint was envisioned as a bank or a trusted institution.
Crucially, in this model, the transfer of coins has to be mediated by the bank.

---

## How does an eCash Mint/bank work?

Adam: What does it mean that transfers are mediated?
Person A has some coins issued.
You ask the bank for one eCash dollar.
To get that, you deposit something with the bank.
When Person A wants to pay Person B, they send that eCash dollar.
This is different from Bitcoin.
You have a long string of numbers—a big number—and you give that number to another person.
The obvious problem is that data can be copied.
I can't give you the number 25 and claim I don't own it anymore.
This is the double-spending problem.
All this talk about double spending in Bitcoin started with the idea of digital cash.
This is an online transfer model.
Person B accepts that number as money by verifying it with the bank.
They send the number to the bank, and the bank checks the database.
What does the bank check?

Anon: It must have a database that 25 equals one dollar.

Adam: Almost.

Anon: They check who had it last so the person hasn't spent it before.

Adam: They check that the coin was never spent before.
It's the opposite of Bitcoin in the sense that you have a list of spent coins rather than unspent coins.
If they can verify it's a valid signature and it's not on the spent list, they add it to the list and Person B accepts it as money.
I'm oversimplifying because there is also blinding and signing involved.
This model requires the receiver to be online and contact the bank for every transfer.
Chaum, Fiat, and Naor produced another paper addressing this.
They suggested a solution based on "cut and choose," a probabilistic cryptographic protocol.
It involved generating many possibilities and relying on statistics to ensure the protocol was followed.
The problem was the large amount of data and interactivity required.
The goal was for Person B to receive something and be assured A wouldn't double spend it.
But they could never be fully assured immediately.
The idea was that if A tried to double spend, they would actually reveal that they had cheated via this protocol.
This enables offline payments based on game theory, but it only works if there are individual identities to blame.
If every spend is anonymous, you have no one to blame.

---

## Blind signing

Adam: Let's go into more detail on how this works.
What is a blind digital signature?
The person making the signature doesn't know what message they are signing.
Would you sign something if you didn't know what it was?
In this application, you don't know the message.
Imagine Tracy wants one dollar worth of eCash.
She has a secret number and wraps it inside a container—an "envelope."
She asks the bank to sign it.
The bank signs the envelope and gives it back.
Tracy opens the envelope and has her secret number, but the signature has passed through onto that secret number.
Tracy now holds a secret number the bank never saw, plus a signature on it.
That is her coin.

---

## Denominations

Adam: Tracy has her secret number signed, but what does it represent?
Does it represent 100 dollars or one?
Each signature corresponds to a specific denomination.
The bank has different public keys for different values: a one-dollar public key, a two-dollar key, a four-dollar key, and so on.
Most original implementations used powers of two.
If you want 17 dollars, you ask the bank for a 16-dollar token and a one-dollar token.
It's exactly like physical cash.
If you have a 16 and a one and you want to pay 13, you have to ask the mint for change.
You give them tokens and they give you new tokens, which you re-blind.
A coin is a bearer instrument.
In Bitcoin, you hold private keys that control coins.
In eCash, the coins themselves are the value.

---

## Stefan Brands's Paper - Untraceable Online Cash in Wallets with Observers

Adam: In the 90s, Stefan Brands—who was a student of Chaum's—developed a system that was mathematically more elegant.
Adam Back will never stop talking about Stefan Brands.
He used a trick similar to what we see in Discrete Log Contracts (DLCs).
A signature $\sigma$ on a message $m$ for a public key $P$ usually involves a nonce $R$.
In DLCs, the nonce is fixed in advance.
If an oracle makes two signatures for two outcomes with the same nonce, they reveal their private key.
Brands used a similar algebraic principle.
If a person tried to double spend, they would end up revealing a certain key.
But this still had the problem that you need an identity to blame.
It's difficult to have privacy in a system where all users are listed.
To make it offline, there were ideas about tamper-resistant hardware like smart cards.
In his paper, Brands described an "observer" in the wallet that would prevent double spending.
If someone hacked the hardware, they would still be found out via the blame protocol.

---

## Real world instantiations / History of Chaum's eCash via DigiCash Inc.

Adam: The most famous example is DigiCash.
In the mid-90s, DigiCash was a company based on Chaum's papers.
Nick Szabo and Zuko Wilcox were involved.
It was literally what we discussed: your interface showed your coins in different denominations.
Why aren't we all using it?
Some people confuse it with e-gold or Liberty Reserve, which were shut down.
DigiCash was more about bankruptcy and internal politics.
There is a fascinating article by a Dutch journalist titled "How DigiCash Blew Everything."
It describes David Chaum as having legendary suspicion.
He reportedly scuppered business deals, including one with Bill Gates, by changing his mind at the last minute.
Ultimately, it was a failure of centralization.
Money created by a company is a category error.
Payment rails are one thing, but creating an actual currency is another.

---

## Laissez-faire city / Digital Monetary Trust

Adam: There were other libertarian experiments like Laissez-Faire City in Puerto Rico.
They had the Digital Monetary Trust and an eCash system developed by J. Orlin Grabbe.
His article "The End of Ordinary Money" is a great read.
Most of these experiments eventually collapsed.

---

## Open Transactions

Adam: In the early days of Bitcoin, around 2014, people were interested in financial cryptography libraries like Open Transactions.
They wanted to do eCash tokens, move Bitcoin around, and use Ricardian contracts.
Projects like True Ledger and Lucre by Ben Laurie also existed.
Many people tried, but nobody really succeeded.
In the 90s, you would have needed a massive database to control the coins and a constant internet connection, which didn't exist for that kind of traffic.

---

## Hal Finney's RPOW

Adam: We should mention Hal Finney's RPOW (Reusable Proofs of Work).
It was a step towards Bitcoin.
He suggested that if we had trusted hardware, we could use the work done by the hardware as a currency.
This was more of a Cypherpunk attempt to make money independent of the state.

---

## Compact eCash

Adam: In 2006, Lysyanskaya and Camenisch published "Compact eCash."
This was a technical improvement to make systems more scalable.
A whole wallet could be about the same size as one coin.
It used bilinear pairings and the strong RSA assumption.
It was still in the model of proving double spending after the fact, which requires identities.

---

## Why you need identities to blame?

Adam: What does it mean to blame someone if every event is anonymous?
If I pay you for a car with a double-spent coin, you are stuck.
If my account is registered and my identity is revealed upon double spending, the bank can block me.
Without a trusted third party, you end up back at the distributed system problem that Bitcoin solved.

---

## Matthew Green's eCash blog post 2010

Adam: Matthew Green is a cryptographer at Johns Hopkins.
In 2012, he wrote a post about eCash designs.
He noted that Bitcoin was interesting but its privacy properties were terrible.
A year later, he was a key driver behind Zerocoin, which developed into Zcash.
Zcash uses ZK-SNARKs to prove a coin is valid without revealing its source.

---

## Schnorr Blind Signatures

Adam: This gets a bit more technical.
Nadav Kohen has some good write-ups on blind signature protocols for Schnorr.
In basic Schnorr, there is a nonce, a challenge, and a response.
To blind it, you add a random number to the challenge so the signer cannot see the message.
In normal Bitcoin, you don't interact with anyone to sign a transaction.
Blind signing is intrinsically interactive.
You end up with a valid signature $(R, s)$ on your message $m$ which you can unblind.
However, there are serious security concerns like Wagner's attack and the ROS attack.

---

## Wagner's attack & The Birthday Paradox

Adam: The birthday paradox says that in a group of 23 people, there is a 50% chance two share a birthday.
Collisions are more common than your intuition suggests.
In Wagner's attack, instead of finding $A - B = 0$, you find $k$ things that add up to zero.
This $k$-sum problem is remarkably easy to solve even for large numbers.
You can use this to attack protocols like Schnorr blind signatures.
If you do hundreds of signing sessions in parallel, you can crack keys or forge signatures more quickly than expected.
Specifically, an attacker might get a mint to output 101 coins from 100 parallel signing sessions.

---

## One-more-forgery EUF-CMA

Adam: In standard signatures, we want EUF-CMA (Existential Unforgeability under Chosen Message Attack).
This means you cannot produce a signature without the key, even if you've seen many other signatures.
In blind signatures, this doesn't make sense because the signer never chooses the message.
Instead, we use the "one-more-forgery" model.
The goal is to ensure you cannot get 11 signatures when the signer thinks they only gave you 10.

---

## Cashu

Adam: Cashu doesn't use Schnorr or RSA.
The genesis was a post by David Wagner suggesting a blind eCash scheme using Diffie-Hellman key exchange to avoid RSA patents.

---

## Diffie-Hellman key exchange

Adam: In Diffie-Hellman, Alice has a private key $a$ and public key $A = aG$. Bob has private key $b$ and public key $B = bG$.
They can calculate a shared secret:
$$s = aB = bA = abG$$
This principle is used for TLS on the internet (ECDH).

---

## Blind Diffie-Hellman key exchange

Adam: CalleBTC recently created a protocol summary for this.
You put your secret in an "envelope" by adding an additive tweak $r$.
The mint (Bob) multiplies your blinded value by his private key $k$.
When you receive it, you subtract $r \cdot K$ to unblind it.
The result is a value $Z$ that the bank signed.
This is reducible to the Computational Diffie-Hellman (CDH) assumption.
If you believe you cannot calculate the shared secret without a private key, the system is protected against one-more-forgery.

---

## Privacy Pass

Adam: This is exactly the same logic used in Privacy Pass.
When you use Tor, you encounter captchas constantly.
Privacy Pass lets you do a captcha once and receive tokens.
You spend these blinded tokens to prove you've done the captcha without revealing your identity.
Cashu and Privacy Pass are both based on CDH.
Cashu is a new project leveraging Lightning.
If you want to mint 420 sats, it sends you a Bolt 11 invoice.
It's very bare-bones currently, but it's an exciting development.

---

## Fedimint

Adam: Fedimint has been around longer.
At its root is a federation of "guardians."
You trust a threshold, such as five out of nine people.
If one goes rogue or offline, you're okay.
The federation controls a multisig that holds the Bitcoin.
Depositing into that multisig entitles you to eCash tokens.
To the user, the interface should be simple and reminiscent of using Lightning.

---

## Threshold Blind Signatures

Adam: Fedimint's innovation is threshold blind signing.
If you threshold sign a blinded message without consistency, it fails.
If Person A signs $M_1$, Person B signs $M_1$, and Person C signs $M_2$, the user might end up with more coins than issued.
To prevent this, the system needs a Byzantine Fault Tolerant (BFT) consensus system, specifically Honey Badger BFT.

---

## BLS signatures

Adam: Fedimint uses BLS signatures rather than Schnorr.
They require specific elliptic curves and are deterministic.
You can aggregate many signatures into one, which is very compact.
The downside is that verification is computationally expensive because it requires "pairing."

---

## Lightning gateways in Fedimint

Adam: A Lightning Gateway is a user of the mint that connects the federation to the outer Lightning Network.
They trade "Fedi Sats" (tokens) for Bitcoin payments.
It's as private as any Lightning payment.
This allows users within the federation to pay people on the Lightning Network and vice versa.

---

## Risks and tradeoffs of Fedimint

Adam: The main risk is the federation itself.
If a threshold (e.g., five of nine) goes rogue, they can steal the Bitcoin in the multisig.
They could also generate infinite eCash tokens.
Currently, there is no auditability of the total supply.
We want auditability without sacrificing privacy.
There are ideas like Merkle trees with Pedersen commitments, but it's a complicated area.

---

## Perfect Privacy

Adam: eCash privacy has a "perfect" quality.
Computational privacy (like Bitcoin keys) can be broken with enough computing power.
Perfect privacy is like a one-time pad.
If I give you my message $M$ plus a random number $R$, you can never find $M$ because there are infinite possible messages with corresponding random numbers.
This is a bearer instrument.
If you lose your phone, your coins are gone.
Fedimint pitches "community custody" where you can ask people you know to help recover funds.
You could encrypt your backup with the guardians.
That's all we have time for today.

Adam: Thank you.

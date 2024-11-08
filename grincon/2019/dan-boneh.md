---
title: Fireside chat with Dan Boneh
transcript_by: Bryan Bishop
tags:
  - cryptography
  - quantum-resistance
speakers:
  - Taariq Lewis
  - Dan Boneh
media: https://www.youtube.com/watch?v=ggvqmb7np9w
date: 2019-01-28
---
TL: I was one of the founders of SF Bitcoin Devs with aantonop. I am also the co-founder of a company called Promise. We sponsor protocols in privacy as well as mimblewimble. If you are mining or actively looking to mine in grin, please say hello to me because we're connected with a lot of mining companies and hosting companies that are looking to host miners very cheaply. I'd love to help. This is the most important panel of the day. There is not going to be another more important panel than my guest. He has been a man of impact and a professor of awesome in cryptography at Stanford. We begged him to give us 30 minutes and to talk about post-quantum crypto and how it impacts coins like grin and other privacy tokens. Please ewlcome Professor Dan Boneh of Stanford University. We're going to ask Dan a bunch of questions.

TL: Dan, you can tell us, and we won't tell anyone else-- did you or one of your students create mimblewimble?

Dan: Thank you, it's a pleasure to be here. I love this area of research because we can deploy new cryptography. Deploying cryptography in blockchain is much easier. This is a fun area. I love it. Hopefully you guys can hire developers out of my classes. My last class had 250 students. It kind of grows with bitcoin's market price fluctuations. I think I'm not going to answer your question, though.

TL: Interesting. Let's talk about an exciting area of science which is essentially quantum cryptography or quantum computing. The question we have is, how long before a quantum computer impacts grin and all cryptography using ECDSA curves? What is quantum computing, how does it impact cryptography?

Dan: Sure, happy ot do that. Most of yo uhave heard of quantum computers. Rather than using classical physics, it uses superposition of particles. You can do certain computations more efficiently in this regime. There's a quadratic speed-up for search problems. The driving force for developing quantum computers is their ability to simulate physics, like for designing drugs or fertilizer or anything like that. These computers are very good at simultaion. That's the business reason to develop them. We need to have good business reasons to make these computers happen.

Dan: So how long until they impact blockchains that use ECDSA? There is a calculation that I would like to take you through. It's simple but maybe optimistic. Let's say Moore's law applies to quantum computers. A couple of years ago, we had 5 qbits. We went to 15, 30, and now we're at 90. If you plot it, it starts to look like Moore's law in number of qubits. The algorithms require 10,000 qubits but that assumes perfect qubits. But what's being built is far from perfect qubits. It requires error correction which adds a lot of overhead. So to break this crypto, because of the error correction, you need like 100 million qubits. Logical qubits are the perfect qubits that don't introduce noise and behave exactly like the algorithm wants to them to behave like. Physical qubits are the ones where you shine a laser at them or hit them with EM radiation and they don't behave in the way you want them to, so error correction is required. If you look at Moore's law in number of qubits, we need like 100 million qubits. RSA requires more qubits, because all of the parameters in RSA are much bigger than ECDSA. When you do Moore's law, so log base 18 of a 100 million, and you get with a doubling of 18 months, you get 30 years if you assume these computers will develop at the same rate as conventional computing.

Most of the rest of the world relies on cryptography for encryption. In 30 years if someone builds a quantum computer, they can decrypt things you said today. For business, there's a good use case to start using post-quantum crypto so that you can have your documents secure for 30-50 years. Banks, governments all want to keep their data secure. For signatures, there's less of a need- it's only in 30 years that someone can break your ECDSA keys if the estimate is correct. So you don't have to worry about that right now.

TL: Are there any five letter agencies that have reached even further than what we know in public?

Dan: We can only speculate what 3 letter or 5 letter agencies are doing. In the Snowden revelations, we found out that there are investments in certain agencies about quantum computing but we have no clue what they are doing.

TL: Let's talk about post-quantum cryptography. You talked about signatures. What are the post-quantum kinds of signatures?

Dan: Literally we could be here for 6 hours talking about quantum computing and what to do about it. The crypto community has been hard at work about defending against quantum computers. In particular, imagine you're facing an adversary that is equipped with a quantum computer. The answer is you move to post-quantum crypto. It's crypto that runs on a classical computer. You continue to use non-quantum computers. But the encryption will be secure even if the adversary is equipped with a quantum computer. So first we have to define a problem that is easy to compute on a classical computer, but breaking it would be difficult even for a quantum computer. So what are those problems? For signatures, there's 3 classes of post-quantum signatures.

Dan: The first one is a hash-based signature like Lamport signatures. A quantum computer is unlikely to effect sha256. If it does, you can move to another hash function. These signatures are believed to be post-quantum secure, but there's a problem: these are really large signatures. SINCS is a multi-signature scheme with signatures that are 30 to 40 kilobytes in size.

TL: Uh, that's big.

Dan: ECDSA signatures are 64 bytes. But these hash-based signatures are around 30 kilobytes. If you shave the parameters a bit, you can get a signature that is maybe a little shorter, but maybe in the 10s of kilobytes. This is useful for software updates. If I want to send you a software update, those are so big anyway that sending an extra 50 kilobytes isn't important. But not so for blockchain.

Dan: Another one is lattice-based signatures. Let me take you back to your linear algebra days, where you were trying to solve a system of linear equations. There are many solutions to these equations. The signature is based on the problem not just finding the solutions ot the system of equations, but finding the solution that is made up of only small numbers. This turns out to be a difficult problem, and we don't even have a good quantum algorithm for that. Well, not yet. That's a good point. Unfortunately, in crypto you can't prove that things are hard. We have a lot of people that try to break them, and then we say it's assumed to be hard. If you want to learn more about that assumption, it's called SIS and you can look that up to see how it worked. For lattices, signatures are about 1 kilobyte or a little less. Still quite expensive compared to 64 byte ECDSA signatures.

Dan: The third category is isogeny cryptography. It's twisted on its head a bit... if you understand the Diffie-Hellman protocol, the buzzword is instead of groups you use group actions. You can use this for signatures. Unfortunately, the best signature scheme we have here is c5-- it's developed in New Zealand and that signature is also around 10 kilobytes. Since we're using group actions not groups, there's less structure, and thus our signatures get bigger as a result.

TL: In 30 years, every blockchain based on ECDSA is going to have to move to this. Everyone is going to have this size problem.

Dan: You guys should be looking to cryptographers and complaining. There's a clear need for a post-quantum signature that is secure and comparable to ECDSA in size, like 64 bytes. We've been working very hard on this. Every scheme we've tried to come up with, we've been able to break them. This is a critical problem for the blockchain community. We've been working on hard on it, it's just hard. It's a hard problem to solve. More people should be working on this. I've been very optimistic about having short signatures based on isogeny because the structure is so similar to elliptic curves. But there's a really fundamental problem making it difficult. It doesn't work yet. We've been trying.

TL: We need not just a small signature size, but we also need things like multisignature, other types of signature features. Which of these post-quantum signature schemes or categories will give us those features we had before with ECDSA?

Dan: That's a great question. One thing you can ask about is verification time. ECDSA is very fast to verify. Can we have post-quantum signatures that are as fast to verify? Hash-based signatures and lattice-based signatures might be large, but they are faster to verify than ECDSA signatures. Isogeny so far, it has some benefits for key exchange, but they are somewhat slower. We're working hard on these problems. The goal is to not just have a short signature thing, but we would also like things like threshold signing. These are all fantastic research problems.

TL: Will grin be able to take advantage of those as we go forward?

Dan: Yes.

TL: When we think of where we are with grin, and in 30 years where we are with grin, will it be that these features come to grin? Or will it require a hard-fork or massive changes based on where we are with grin today?

Dan: Ah, I see. Imagine in 15-20 years we.. and I'm not saying that's the timeline.. but imagine we solve the problem in that timeline. That gets us to the 30 year mark. That's the mark you should be shooting for. That's my estimate, with a grain of salt. Maybe on the internet encryption deployment needs to happen soon. On blockchains, it's easier to deploy because of hard-forks ((what?)). This is the time where you want to be moving aggressively to post-quantum signatures. Also they might patent the scheme. ((boos))

TL: Please don't patent it. Let's talk about some cool ideas in post-quantum cryptography. Let's talk about post-quantum accumulators.

Dan: I guess this is the quantum section. There's lots of things we would like to do, that blockchain wants to use that are non-standard internet crypto. It's more regular crypto. A merkle tree is a kind of accumulator. You can add elements to the accumulator and efficiently prove its membership. It turns out there are accumulators that have better properties than merkle trees. Some of them have more efficient proofs too. These accumulators are based on groups of unknown order like RSA uses the RSA group. Today, it turns out that those are not quantum-secure. The algebraic accumulators we have are not quantum secure. Merkle trees are quantum-secure, but the new accumulators are not. So how do we build post-quantum accumulators?

Dan: There's a new primitive specifically for consensus, called a verifiyable delay function (VDF), which is a way for anyone to genreate a puzzle. A puzzle appears, and it takes a certain amount of time to solve it, even if you have a parallel computer. A miner with more machines wont be able to speed it up. These VDFs are useful for consensus. These are built from groups of unknown order, which of all the ones we have today are all quantum vulnerable. There are so many wonderful problems that we have available to work on. We're working on it. Hopefully we'll solve it in the coming years.

TL: Let's come back to proof-of-work in grin in a quantum world. Do quantum computers impact proof-of-work?

Dan: Right, so. Quantum computers could impact proof-of-work. There's an algorithm that gives a quadratic speedup for any search problem. If you want to solve a PoW work with a difficulty of 2^70, classically it would take 2^70 hashes. Classically we throw a lot of computing power at that, and we solve it in 10 minutes.

Dan: We setup the Stanford Blockchain Center. If you have any crypto questions or want to work with us, please contact us. We set this up so that we can work with projects. I love how these questions are brought up. Every blockchain project I talk to, I find more problems to work on. One question that we had been asked, which is solved now... this was the Handshake project and they had a problem with airdrops. They wanted to airdrop to all github developers. They have ssh keys, either RSA or ECDSA keys. Github makes those public keys public. So you have a community of several hundred thousand developers who have public keys, and you can just do airdrops to those public keys. So that's a cool idea. So the developers get the coins. But what they were worried about was that when a developer withdraws the funds, they wanted no stigma associated with that. How could you withdraw funds without revealing which developer was doing it? So that was a beautiful question. We have a solution to this, we call this private airdrops. This is being deployed in Handshake soon. The idea would be that rather than airdrop to a public key, the airdrop is to a commitment to the public key. So you see a list of commitments, and when someone wants to withdraw the funds, they just prove knowledge of the private key without revealing the actual key used to withdraw funds. So we have a private airdrop system. The beauty of this is that Handshake is making all of this available to anyone, so that any project in the future wanting to do a private airdrop can use this same system. It's a cool way to do airdrops from now on.

TL: How long did it take you to do that solution?

Dan: Well, it was a couple of months.

TL: Great. So now there are private airdrops, that's great. So, you didn't create mimblewimble or grin. But if you were to create a new cryptocurrency, Dan, what would you put in it? Give us some features.

Dan: I'd put in signature aggregation (BLS signatures). Privacy with zero-knowledge. Bulletproofs for sure. And efficient consensus, without burning a lot of energy, like verifiyable delay functions. There's not enough time really.

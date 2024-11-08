---
title: Snarks
transcript_by: Bryan Bishop
speakers:
  - Andrew Miller
  - Madars Virza
  - Andrew Poelstra
  - Bryan Bishop
  - Nathan Wilcox
---
some setup motivating topics:

* practicality
* pcp theorem
* trustless setup
* magic away the trusted setup
* schemes without trusted setup
* pcp theorem is the existent proof that the spherical cow exists.

people:

* Andrew Miller (AM)
* Madars Virza (MV)
* Andrew Poelstra (AP)
* Bryan Bishop (BB)
* Nathan Wilcox
* ZZZZZ: zooko
* gmaxwell's ghost (only in spirit)

SNARKs always require some sort of setup. PCP-based SNARKs can use random oracle assumption instantiated by hash function, sha256 acts as the random oracle. There are linear-PCP based SNARKs, those are the ones implemented and currently most efficient and require some magic numbers and parameters for the system. Needs to be done only once, but it needs to be done, like setting up RSA keys, product of two numbers, you don't want anyone to know what those two numbers. It's more complex than setting up RSA keys.

Is this selecting the ideal elements for greater encoding schemes? Not familiar with multi-linear maps in that detail.

The person has to be trusted by everyone in the system; where are you going to find someone trusted by everyone 20 years down the line. This person doesn't exist. We hope that we can find a number of people that we can trust that at least one person didn't give in. You could have a decentralized setup procedure based on multi-party computation, where n parties participate, everyone learns the public parameters at the end and can go on and use the SNARK. You would have to compromise every single one of them, like in the movies where you need every key to light up a console and it doesn't work without one key.

AM: In other protocols, you need a super majority, and here it's that only 1 person has to be honest.

MV: It's much stronger than 51%. Whatever. 97% attack, whatever. It's vulnerable to 100% attack and nothing else.

AM: You can check after the fact about the correctness; you need actual randomness for your inputs, you also need to securely delete this data. Maybe there's a SNARK setup with a trust door, but maybe it was so diffuse that a secure delete protocol could remove it.

MV: Probably that would totally shoot efficiency down.

RSA UFOs; RSA keys have the- UFOs an unfactorable object, when building accumulators, you want to have the structure of the RSA key that nobody knows the factor of. Zerocoin uses UFOs they want an accumulator and we don't know an efficient multi-party computation to construct them, so one heuristically is to pick a large enough number that it's bound to have prime factors of that size and you hope it's fine.

AM: There's a way to do setup for ZKP systems where there's no trap door, and then there's large factors that nobody knows. Anoncoin tried doing this. They implemented zerocoin and tried to do UFOs as efficiently as they could. I don't know if any of this was good, but they helped popularize the UFO technique, but we don't know how to do this for SNARKs.

MV: You need to have conservative parameters for how .. how to choose conservative parameters? It is fine if many participants have skewed randomness, ideally none of them would have skewed randomness, keys are completely random as long as at least one of them put in real randomness.

AM: how practical are these SNARKs? We think they are super practical, but what did you mean by that?

AP: I didn't look at this 12 months ago, I think it wasn't feasible. The proving time was too long.

AM: Even 12 months ago, depends on the circuits. How long does it take?

AP: We want to replace transactions and transaction verifcation with SNARK-replaced blocks.

AM: Is it right to say that a proof for a sha256 still takes a second on one core?

MV: It should be under a second. It sounds about order of magnitude.

AP: The last numbers I heard were like 15 seconds. So that's huge.

AM: Nope that's off by an order of magnitude.

MV: In the earlier papres, there was a SHA benchmark, it was compiled not to a circuit but to a program in a .. tree. You had a CPU for each of the steps of the program, and that was the circuit. This was TinyRAM.

AM: There's another tool called pinocchio, like tinyram it involves compiling from C to a SNARK, but it takes a different route; with tinyram you compile it to instructions, and the SNARK construction is a virtual machine. With pinocchio it compiles down to a circuit directly. Still that compiler is not nearly as good as composing using something like gadget tools.

MV: If you want the best performance, then you really want to use non-deterministic arithmetic tricks that come from the proof system. Discovering those tricks automatically, it's difficult but we don't have proof for impossibility. With zerocash we have a factor of 2 increase, with pinocchio it would be twice slower.

AM: I like pinocchio as a protoytyper, because without thought you can take C code and get a SNARK circuit out of it. You could optimize to do better.

MV: Gepetto has a new compiler that compiles C to llvm-IR to a circuit.

AM: That probably supercedes pinocchio.

MV: They released binaries for the compiler, but not the source code.

You could plug the circuits into libsnark.

AM: I have done that with libsnark before.

AP: Can we snark EC operations on dedicated circuits?

MV: Elliptic curves are curves usually over some prime field. You want really the prime field to be the native field provided by your proof system. So SNARKs natively can support arithmetic relationsihp checking over some field, but not necessarily the field oyur curve is defined on. If the fields don't match up, you have a simulation overhead penalty, it is possible to do it, but it's 2 or 3 orders of magnitude.

AP: It's going to be coprime they're both huge.

nwilcox: Constraints?

MV: There are some constraints. But what's actually possible and what we did in our Crypto2014 paper is that we have two fields that match up if there's an elliptic field over one curve, there's a number of points and it's prime, and over that you can define another elliptic curve for which one exactly matches the first curve, you can match from the first curve using the second curve. You can keep switching between curves and we keep doing it, we do this for bootstrapping which is unlimited recursive composition. We can support arbitrarily running programs by checking one step at a time, translating the proof using the other curve, checking another step with another curve, it can scale indefinitely, this scales indefinitely.

AP: It means you can run snarks inside snarks. We have a candidate for this. We have both primes about 80 bits.

MV: We have a curve setup for this, at the 80-bit security level. We also have two curves at 128-bit security level that haven't been published, but we have them. The performance is quite a bit slower for them because the way you want to .. the curves, you need to place additional constraints on those primes. And they place constraints on the pairings. And you can have pairings with less security level, so you need to bump up your prime security. If you want 256-bit security, you'll just pay for it.

AM: Gepetto found a pair of curves; the inner curve is the saame one as the original pinocchio curve. And then they have a larger outer curve, and you can do efficient operations in the inner curve. You can have checked SNARK proofs for the inner curv,e but nothing talks to the outer curve so you can have 1 layer. Just two. But that's still helpful for turning your task into a one layer tree.

MV: You can compose a tree of one or two of proofs, with libsnark the cycle of curves you can do arbitrary depths. You pay for this a bit.

nwilcox: How large are the secp256k1 public keys? Can you use snarks to compress a signature by proving that you signed with a public key whose hash is on the blockchain? Or is that bigger than just the public key?

MV: It's probably that the snark proof is going to be bigger than your original signature.

nwilcox: Signature with pubkey though?

MV: It wouldn't save much. However, if you're saying you just want to compress only one signature one public key, but if you want to compress 100 signatures with 100 public keys, you immediately get savings because your SNARK proof is constant size less than 300 bytes. So the numbers come from scale.

nwilcox: MAST?

MV: Not familiar.

AM: Simple concept. If you don't take all the code paths, you don't need to load that chunk of code. This is important when you care about the constant factors. Maybe a scriptpubkey where you want a signature from one of the pubkeys, and maybe you have 20; you don't need to load up all 20 if the merkle branch is the only one you need to care about is the only one you need when checking the MAST root. You usually have much smaller code that runs through it, so you will have loops and you will use most of the code path on your execution, so from that mindpath it doesn't matter that much which is why I think it hasn't been explored. But for scriptpubkey stuff, MAST become smore important because size of the code becomes more important.

nwilcox: So if a spender only specifies a MAST root; if the creator of the txout only specifies a MAST root, and the spender provides a portion of the tree which they can prove they control that branch of the tree, then they can spend without going through other branches of the tree. Perhaps there is a SNARK application if they can prove that they satisfy at least one branch for the given MAST root. But they don't need to reveal which key they used and the set of keys is unknown. So it would provide unlinkability.

MV: This is similar to proof-of-solvency. You want to prove you control X bitcoin; you can have a SNARK proof that the circuit can check that I control that many bitcoin; where they are, the proof doesn't say, it's zero knowledge.

AP: Scales linearly with the size of the input to the program?

MV: The verification time of the proof scales linearly with the size of the statement you are trying to proof. The size of the witness of the statement. You can use tricks, you can publish a hash of the statement, and then the SNARK verifier- unhashing it, like checking non-deterministic or something.

AP: I see.

AM: You only incur the cost of that one hash.

AP: It occurred when you were talking about the MAST. I was thinking you'd gain nothing in that case, oops.

MV: You can merklize the entire blockchain.

AP: Yeah.

AM: What else do you got?

AP: Yeah that was a big one.

MV: We have used hashing of the input to bring down the verification cost and also for other reasons. It's all in libsnark.

AM: Demonstrated?

MV: Academic prototypes.

AM: Do we know anyone who is using snarks in a deployed way?

MV: In theoretical practice, and in practice-practice. I am not aware of large-scale practice-practice deployment. Or any scale practice-practice deployment. I hope however that zerocash will be a practice-practice deployment real soon.

AP: I thought multilinear maps are necessary.

MV: Nope, not at all. You need bilinear groups plus some assumptions. You can do it in the generic group model.

AP: Generic bilinear group is efficient, but not realistic, it's superstrong model. It's not more than that. It's like the whole group in the random oracle.

AM: Hardness assumptions that it relies on?

MV: Computing discrete log in the group is hard, you want assumptions related to-

AM: It's either in one of the groups or the other, like the target group?

MV: You want computing the discrete group is hard in both source and target, because you could use ~ to compute the in the ~. We added a little bit more. Q power assumption

AM: Q Power knowledge assumption?

MV: Yeah. Basically, it says that if I give you a specific set of group elements like all the powers have to be Q plus one except power Q, which you cannot extract back that power Q, and this assumption and related assumptions have been used at least in the early 90s maybe even in the late 80s in academic literature. They haven't been broken, they have been used widely.

AM: Used widely in bileanear group construction?

MV: They have been used without bilinear group construction, like for short signatures.

AM: Do you need some extended form of DDH?

MV: This can be viewed essentially as an extended form of- some extension of DDH. There are a couple of assumptions to add on top of them. I think that in theoretical crypto cirlces they are controversial, while random oracles would be controversial, or generic groups, yeah. I don't know any deployed.

AP: This is several orders of magnitude better than I thought in every dimension.

AM: People are facilitating this; like the libsnark gadget library is good. jsnark alternative to that, which includes some optimizations to that. No good reason that it's in java instead of just using libsnark. It must have been just randomly convenient. Acknus .. Yawn Carlson? Yin Carlson? snarkfront.

AM: Maybe Microsoft Research has people lined up ready to use this in practice.

MV: ABSOLUTELY NOT

REDACTED REDACTED REDACTED

AM: Microsoft Research does lots of optimization of EC even out of SNARKs, it's not strange, it's just something out side of my knowledge.

MV: They used a curve for which EC operations are fast, you can do bit twiddling hacks, they have lots of 0s for certain primes, certain operations are fast because compressed formats and whatnot. For SNARKs there is a problem called polynomial interoperational, which is used using fast fourier transform, if you have arbitrary size, it's actually quite painful or slow, it's much slower than just using power of 2 size. We chose our curve so that FFT part would be fast, and if you look in

You can pick primes so that polynomial interperolation is fast. You can match up curves for bootstrapping, where you have cycles about proofs about proofs about proofs. Another thing is choice of hash function, if you are willing to use lattifce assumption (?), you can have hash functions that are extremely fast, don't use SHA, use knapsack-based hashes. There are a lot of tricks when you go deep enough, and thos etricks can give lots of optimizations.

AM: gmaxwell has an idea of a simplest possible SNARK appslication with bitcoin today, which is where you solve some problem, someone should just do this, it would be the first practical SNARK. You compute a solution to a hard problem, like sudoku or something, perhaps there's another problem though. You have the solution, the problem, you take the hash of the solution, you put hte hash in the bitcoin transaction, then you would have to reveal the solution in the spending transaction. Out-of-band you would provide a SNARK proof, then you could get people to pay you because once they put enough money into it, they need to claim the bounty to reveal the solution. And that's very clever.

MV: Bitcoi naddresses that can be spent if you have a hash collision.

AM: Out of brand proof with SNARK. It's really cool. But sudoku is not a NP-hard problem. It's polynomial-time solvable. Any bogus SNARK thing is also valid because you can't proof knowledge if it's already computable.

MV: I know the private key for the SSL certificate, and that could be a problem because I could prove out of band, for more complex problems, which I know the solution of, I know the private key of, it would be inclined to .. the address.

AP: You're concerned about sudoku because it's not precise?

AM: It doesn't fully exercise.

AP: discrete log RSA factoring are also not NP complete.

AM: It's not ammenable to it, but to do SHA-2 in a SNARK circuit, it's.. same with an RSA key or SSL key.

AP: We think that with a classical computer that you have to do it. We think it's true. Are you talking theoretically or do you mean in practice? Discrete log is not NP-hard, it's BQP. Bounded quantum polynomial.

AM: No polynomial time solution would be satisfactory for me. ... It can't be something be ...

AP: Oh not a security thing, just a triviality of the example.

Hash PCP?

MV: Impossibility result of trustless setup? You can't have NIZKs without some sort of oracle, the attacker could just enumerate over outputs of your proof, and could just give you one that it accepts. You need cryptographic hardness assumption. There are also results in late 90s I could look up reference that you need a common random string for non-interactive zero knowledge, and common random string we can instatiate in practice, sha256 of 0, of 1, that's your random string. Just using SHA as a random oracle. But there are papers and there are impossibility results saying that a common random string is a lowest assumption you can make.

AM: This is a disambiguation thing; in CRS- that's the output of your setup procedure. CRS can mean common random string or common reference string. It could be sampled from a random distribution or even distribution. Common reference string on the other hand has to be some algebraic structure thing, like some RSA thing, has two large prime factors but we don't know it, or in order for trusted setup with SNARK then a trap door. What you're saying is that impossibility results say you need at least a common random string.

MV: There is no impossibility result that SNARKs would require common reference strings. In fact, there are some SNARK constructions known that only require common random string, for those - computationally sound proofs of .. probabilistically checkable proof, and then collision resistant hash function. The PCPs haven't been implemented yet, so the question of deploying them doesn't arise. Part of SCIPR lab that is working on implementing PCPs and I really hope that we have a PCP. PCP constructions are much more sophisticated than underlying mathematics than linear PCP constructions, implementing them also takes more time. For now, multi-party setup seems to be the best thing we can have for SNARKs, and maybe 1 year down the road we will be using PCP-based SNARKs and essentially no trust, assuming that SHA is the random oracle or something we can use to feasibly deploy them.

AP: Lots of research about PCP-based SNARKs?

MV: There are theoretical constructions. There are implementations in LaTeX of those things. The team at SCIPR lab actually has REDACTED. .........  If you had a sufficiently big quantum computer, you wouldn't be able to break PCP-based SNARK, if you had a quantum-safe hash function and you believed there was nothing better than Grover's algorithm which is just square roots, then we have PCP-based SNARKs and they are quantum-safe. We should start a SNARK wiki.

MV: Can I submit pull request corrections?

AM: SNARK wiki is good, also we should have standardized explanations among these as well.

AP: Lamport signature is similar in spirit to PCP-based SNARKs. Everything is sort of hashes and revealing hash preimages.















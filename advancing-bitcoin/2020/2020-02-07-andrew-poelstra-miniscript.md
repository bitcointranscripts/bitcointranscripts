---
title: Miniscript Workshop
speakers:
  - Andrew Poelstra
date: 2020-02-07
transcript_by: Michael Folkson
tags:
  - miniscript
---
Website: https://bitcoin.sipa.be/miniscript/

Workshop repo: https://github.com/apoelstra/miniscript-workshop

Transcript of London Bitcoin Devs Miniscript presentation: https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/

# Part 1

So what we’re going to do, there is a couple of things. We are going to go through the Miniscript website and learn about how Miniscript is constructed, how the type system works, some of the anti-malleability rules. Then we’re going to go to a repo that I created last night, a Git repo with some example programs. We’re going to try to recreate those and try to modify those and learn how to use the rust-miniscript library and some of the capabilities of the library. We are going to encounter a few bugs, we are going to encounter a bunch of limitations which we can discuss and see if people can think of ideas around these limitations. Some of them seem to be computationally intractable, some of them are engineering difficulties, some of them are API questions. With all this said it would be helpful if you all have a Rust toolchain installed. It is very quick if you are willing to run this curl command downloading a shell script and pipe that into sh then you can install Rust this way.

Q - Is there a minimum version because I just got it from the repo?

A - Yeah the minimum version is 1.22 which came out like 2 years ago. 1.37 is plenty.

For a little background about the Rust setup before I jump into the actual thing and start talking about Miniscript. The [rust-miniscript](https://github.com/apoelstra/rust-miniscript) library is part of the [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) family of libraries. These all have pretty aggressive minimum Rust versions. By aggressive I mean aggressive against the Rust community, a very conservative minimum version. They require 1.22. The reason being that Carl (Dong) has a Guix way to build 1.22 from some minimal.. Guix. We can bootstrap Rust 1.22 from the toolchain that we trust where if you’re always tracking the very latest one that would be very difficult. In general the only way to build Rust 1.x is to use 1.x-1. If we went up 15 versions our deterministic bootstrap would have to compile 15… That’s part of the reason. Another part is just trying to be consistent with what is in the Debian repo and then also be conservative and not changing things. With all that said with any version of Rust you can obtain today will work with this. Rust changes fairly quickly but we’re not using… There are a couple of things we need. One is if you want to play along with the Rust stuff though I’ll be doing it on the screen, it is good to grab the toolchain from [rustlang.org](https://www.rust-lang.org/learn/get-started). The Linux instructions are this pipe sh thing. I don’t know how you do it on Mac or Windows, it may be different. The other thing that you guys will probably want is this Git [repo](https://github.com/apoelstra/miniscript-workshop). I don’t know if you can read that URL.

Q - When did you make this repo? A hour ago?

A - The latest commit was one hour ago.

Q - The initial commit was also one hour ago.

A - Whatever. A bunch of it I did last night. I only committed it, I only published an hour ago but it was created a very long time ago.

What’s nice about this repo is the README down here. A couple of useful links. The first I want is the [Miniscript website](https://bitcoin.sipa.be/miniscript/). This is linked to in the Git repo but it is also fairly easy to memorize. Let me give a quick overview of what Miniscript is although I guess I did a talk yesterday and some of you were at the Bitcoin developer [meetup](https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/) on Tuesday where I did a 2 hour detailed thing. Basically what Miniscript is is a subset of Bitcoin Script which we can represent in this nice form. Let me show you an example.

`and_v(or_c(pk(B),or_c(pk(C),v:older(1000))),pk(A))`

Rather than looking like Bitcoin Script. Bitcoin Script is stack based, opcode based and very low level. Here we are encoding spending policies in an obscure looking way. What we have are different key checks, hash preimage checks, timelocks and we can combine these in various ANDs and ORs and thresholds and so forth to compose more expressive spending policies. You can sort of see what is going on. You’ve got these `pk` `pk` with the pubkey signature checks. You have this AND that is a boolean AND and all of the rest of the noise, the `_v` the `v:` stuff like that, those reflect the underlying Bitcoin Script being encoded here. If I click “Analyze” here you can see the actual Bitcoin Script that is represented by this Miniscript.

```
<B> OP_CHECKSIG OP_NOTIF
  <C> OP_CHECKSIG OP_NOTIF
    <e803> OP_CHECKSEQUENCEVERIFY OP_VERIFY
  OP_ENDIF
OP_ENDIF
<A> OP_CHECKSIG
```

The benefits of Miniscript over using the raw Script is that when you have a program structured in this way it is very easy to analyze in a lot of different ways. It is easy given an arbitrary Script to figure out how to construct witnesses for it. In general this is a little bit difficult. Bitcoin Script has a whole bunch of opcodes. Each opcode has requirements for what goes on the stack when you run it. When you compose a whole program out of these you can’t just look at the program and say “To satisfy this Script I need to provide a signature here and a public key here and a hash preimage here. I need to put the number zero here” and so forth. With Miniscript it is very easy to answer questions like this. It is very easy to estimate the witness size if you are doing fee estimation for your transaction. It is very easy to do a bunch of semantic analysis which I think we will also go into.

Q - You call that one Miniscript so the level above is a Policy descriptor language? At least for me I have some confusion about the terminology.

A - That is a good question. This thing I call Miniscript. Miniscript is basically a re-encoding of Script. You have this thing, you can get to that and vice versa. There are different ways of encoding the same thing. They are fairly straightforward. You can write a parser for either of these and a serializer for either of these and they will map back and forth. There is a separate thing called a Policy language which we will get into a little bit later. The Policy language is something like this.

`and(pk(A),or(pk(B),or(9@pk(C),older(1000))))`

You can see it looks very similar to Miniscript with two big differences. One is all of the noise has gone. I no longer `and_v` and different kinds of ORs and ANDs. I no longer have all these wrappers and stuff. I just have ANDs and ORs, pub keys, hashes and timelocks. The other big difference is I’ve got weights. If I have an OR anywhere in a Policy I have different weights I can assign. What this `9` means, this OR is either a pubkey or a timelock of 1000 blocks, there is an implicit `1` here, the `9` there means that the left branch is 9 times as likely as the right branch. Here we’ve got 90\% we’re going to use the left branch, 10\% we’re going to use the right branch. The reason we do that is because policies are not a Bitcoin thing, policies do not correspond to Bitcoin Script, policies are abstract semantic things. If we want to use something like this on the blockchain we need to convert it to Miniscript. The way we do that is by running a compiler which we will also get to if we have time. You can see on Pieter’s website here there is a WebJS compiler that he’s compiled to from the C++. We take this Policy up here, this abstract kind of thing, we compile to Miniscript and you can see you’ve got basically the same thing except all the noise has been added. There is specific choices of what noise to add in what places which corresponds to specific choices of which Script fragments we’re using. Also you can see the probability here. Bitcoin itself has no notion of probabilities. The coins appear on the blockchain, they get spent once, that’s the fact of life. As James (Chiang) was saying you only have these two state transitions, maybe three if you consider… An output is created, it gets confirmed, it gets spent. That is all that happens. There is no notion of probabilities, there is not even a notion of executing, there is not even really a meaning assigned to any Script branches that aren’t taken. So this is all very abstract. We’re going to write some code and we’ll see more concretely what these sort of things mean.

Q - There is a Bitcoin StackExchange [page](https://bitcoin.stackexchange.com/questions/91565/what-does-bitcoin-policy-language-offer-the-developer-that-miniscript-doesnt-w)  answering this question. Sipa answers it and James and Sanket.

A - Write any of these keywords into Google and you’ll find this.

One last thing to say about Policy. Policies in general you would create when you’re trying to design a Script. You write a Policy that actually represents what spending conditions you care about. You run it through this compiler, you get a Miniscript and then you forget the Policy ever existed basically. At least that is the way I think about Miniscript. The Policy is a background thing that is used for the compiler to find an optimal Miniscript. But once I’ve done that I stick with the Miniscript and I forget that it ever came from something more abstract. We’ll see later on when I do want something more abstract it is very easy to obtain. I can just drop a lot of the extra stuff.

Q - Can you verify a Script satisfies a Policy?

A - Yes. Pieter hasn’t implemented this so the website doesn’t have it. Conceptually what you can do is you take this and everything after an underscore or before a colon is either wrappers or somehow specifying the exact Script fragments to be used. If you just throw those away what you will be left with is exactly the same as this Policy although the weights are not… The weights don’t matter of course for semantic reasonings. Absolutely.

In the rust-miniscript library, let me hop over to the rust-miniscript documentation [here](https://docs.rs/miniscript/0.12.0/miniscript/policy/trait.Liftable.html). This is not the most readable description of what is going on here. If you have a Miniscript of some form you can use this function Lift here, you run it through Lift and whatever you started whether it was a Miniscript or a Policy or some other representation of your Script, you run it through here and you get this [object](https://docs.rs/miniscript/0.12.0/miniscript/policy/semantic/enum.Policy.html) called a Semantic Policy, an abstract Policy which corresponds to a Miniscript. It is just the ANDs and ORs and thresholds. You can these are all the different components. An abstract Policy, it might be Unsatisfiable, it might be Trivial, those correspond with the zero OP_RETURN Script. It might be a pubkey hash, it might be a timelock, it might be a hash, an AND, OR or threshold of any of those things. There is not anymore to it then that. If I go instead to the [Miniscript type](https://docs.rs/miniscript/0.12.0/miniscript/policy/semantic/enum.Policy.html) if I can find it. This is what a Miniscript is. It is one of these things. You can see you’ve got `True`, `False`, `Pk`, `PkH`, timelocks and hashes of course but then you’ve got all these different things, `Alt` `Swap`, `Check`, `DupIf`, `Verify`, `Nonzero`, `ZeroNotEqual`. Those are all wrappers. They take some other Miniscript fragment and they put something around it. They add like an OP_VERIFY at the end, they add an IF, ENDIF so you can skip over it by passing zero. They might put an OP_SWAP in front of it so you can move things out the way. It might move something to the altstack, run the contained program and then bring something back to the altstack. Things like this that are important for the Bitcoin Script semantics. Then you’ve got your ANDs, ORs and thresholds. You can see again you’ve got many of these. You’ve got three kinds of ANDs, four kinds of Ors and two kinds of thresholds.

Q - So for reference which of these directly overlap with existing descriptors?

A - That’s a good question. The conceptual answer is that none of this overlaps with descriptors. They have similar names.

Q - It looks like threshold is exactly what you’d pass into `importmulti`? And `PkH`…

A - A descriptor of type `pkh` means that you have the standard DUP HASH whatever scriptPubKey and standard signature scriptSig. That’s a pkh in descriptors. A PkH here corresponds with a Script fragment. It is the same as Script but the point is in Miniscript the PkH is a Script. In a descriptor the pkh specifies where that Script goes and where the witness goes.

Q - No. It is still a Script.

A - It is not still a Script. It corresponds to how you put the Script and the witness into the transaction. That’s all the Script is doing. Let’s go into the descriptor type to separate out what these things are. Miniscript descriptor, [here](https://docs.rs/miniscript/0.12.0/miniscript/descriptor/enum.Descriptor.html) is what a descriptor is. An output descriptor as Andrew (Chow) talked about yesterday is an object you would use in a Bitcoin wallet to specify how a Script is actually used on the blockchain. There are a whole bunch of different kinds of descriptors that we care about. Let me go over the important ones. There is `Pkh` and `Wpkh`. `Pkh` is your standard 1 whatever address where you’ve got a pubkey hash in your scriptPubKey and then to spend the coins you reveal the pubkey, you reveal the signature in your scriptSig and you’re off to the races. `Wpkh` is just a SegWit equivalent of that where you have a witness program which is a zero followed by a 20 byte pubkey hash and then the only witness required is a signature. You might have `Sh` here is pay-to-script-hash. `Wsh` is pay-to-witness-script-hash. Again P2SH to the 3 addresses then there is P2WSH which is the standard SegWit program where you’ve got a program hash, a zero followed by your program hash and your witness goes in your witness field. When you are using Bitcoin today typically the only two descriptors you care about are WPKH which are used for a normal wallet which has keys and you spend using the keys or you might use WSH which is where you’ve got some complicated script and you want to use SegWit. We also have P2SH wrapped WSH which you might use for compatibility reasons with older services or P2SH if you are running an older service.

Q - You can do WSH - PKH in descriptors. That is allowed and there is a test for it. Under this definition that is not a Miniscript?

A - Interesting. Under this definition the PKH will be the Miniscript and the WSH wrapper would be the descriptor.

Q - You can literally do that in descriptors right now.

A - I would claim that to the extent that you can do you’ve already brought part of Miniscript into descriptors.

Q - You’ve just claimed that PKH is not a Miniscript?

A - I’m saying that the `pkh` here and the `PkH` in the Miniscript are different here. But I really think we’re causing semantic confusion by having this argument right now. We can argue offline.

Let me say one last thing. In a year or two when Miniscript is fully implemented into Core we are going to think of Miniscript as being a subset of descriptors. Descriptors describe everything you need to know to be able to spend a Bitcoin output. It tells you is it P2SH, is it a witness-script-hash, whatever. It will also describe in future what the actual Script is and how to satisfy it. Does it one public key, does it have many, does it have timelocks, whatever? What Miniscript is is a subset of these descriptors that encode the Script semantics. Right now there is a thing in Core called descriptors that has a couple of specific things from Miniscript in it but not much else. In the future we will have all of Miniscript in it.

Q - Is this a way to think about this? You think about descriptors as your high level language like a Java. You’ve got your intermediate byte code with Miniscript and then your actual machine code, the descriptor itself. Do you think that is fair or not fair?

A - I would say unfair. Using this analogy Miniscript corresponds to the byte code and then the descriptor part would correspond to the header on your Java program, your JVM version something like that which sets whatever flag you need to run it. Descriptors include a lot of things that are not part of Miniscript. Thing like P2SH. Miniscript has no notion of P2SH because it is just about Bitcoin Scripts.

Q - I think a better way to think about this is that descriptors describe the scriptPubKey and Miniscript describes your redeem script or witness script. The separation is your Miniscript goes in the input, your descriptors go in the outputs.

A - I like that, it is a very practical distinction that will work for anything that you’re doing in real life. But…

Q - You can use Miniscript in scriptPubKeys but why would you?

Q - The descriptors incorporate more of the validation logic and the script engine around it whereas Miniscript is directly…

A - Yes. rust-miniscript does support putting Miniscripts directly in the scriptPubKey using it as a bare type descriptor but you really should never do that. This mostly exists so that I can write tests and not have to WSH wrap all my stuff all the time. Also sometimes I abuse Miniscript in other contexts on Liquid and it is useful to have that bare type so I don’t have to reach through the Bitcoin…

I hope that was more enlightening than not, that discussion between Miniscript and descriptors. I like what Andrew said where your descriptor describes what goes in the output. How do you signal to the Bitcoin verifier where your Script actually is and how that is encoded? The Miniscript goes in your input. The Miniscript of the actual program. So let’s try to make this a little bit more practical. I’m going to switch to the GitHub page unless there are questions?

Q - One thing that confused me yesterday was that Andrew Chow said descriptors describe everything needed to solve them. That sounded like analyzability which is more in the Miniscript realm rather than the descriptor realm?

A - The reason we have a distinction at all is that descriptors are implemented in Core, there is a PR for descriptors. It does include most of Miniscript, it doesn’t include the different ORs and ANDs, it doesn’t include the complicated threshold, it doesn’t include timelocks, it doesn’t include hash preimages. It literally only includes pubkeys and pubkey hashes. The point of descriptors as implemented that way as Andrew talked about in his talk is cleaning up the current Bitcoin wallet model which right now is incoherent. You have the elliptic curve keys and basically any plausible way you could use that elliptic curve key in Bitcoin Core right now will just recognize that as something it controls. Which makes interoperating with Core very difficult. If you are trying to write a wallet that’s using the Core RPC you either have to go whole hog or you can’t. For example if I generate a pubkey and I give you a legacy Bitcoin address, a 1 whatever. And you take the pubkey hash out of that address and then you put that into a WPKH output. You change it from a pubkey hash output to a witness pubkey hash output and now you have some bech32 address. You can send money to that address and my Core wallet will recognize it even though the address I generated was a legacy address. Does that make sense? Which means that if you are writing software that is wrapping the Core wallet and you think “I’m going to check for coins going to my addresses and Core will know exactly the money sent to the address I generated” you’ll be wrong because Core will recognize money sent to other unrelated addresses. You either have to implement this brain damage yourself in your own code or you can use a near future version of Core that uses descriptors where it actually keeps track of what addresses are created and in what way.

Q - One thing is descriptors was an idea Pieter had originally and then Miniscript came out of that so the distinction between them isn’t very strong. They are very related.

A - There wasn’t even a lot of time between these.

Q - It was like 20 hours. It was one day he talked to me in his office about descriptors and the next day… and then Miniscript came from that.

A - I thought there was at least a week. A bit of history. Output descriptors are Pieter Wuille’s brainchild to clean up the Core wallet mess. He came up with this idea, he wrote a gist, he was talking about it on the Bitcoin dev mailing list. A week or two or possibly 20 hours later I flew in to Mountainview to go visit him at the Blockstream office and I said “I’m trying to do some general Bitcoin Script stuff.”

Q - You were trying to finalize a PSBT without implementing…

A - That’s right. Carl Dong has implemented PSBT in rust-bitcoin. He is trying to add special purpose code for CHECKMULTISIG so he can do these PSBT types of CHECKMULTISIG. I nabbed this, I said “I don’t want these specific Script templates in here. This is not some special purpose library for every specific thing that comes into Carl’s head. This is a generic Bitcoin library. I went to Pieter and I said “I need a way to generally model Bitcoin Script.” And he said “What if we extended descriptors to add MULTISIGs and ANDs and ORs and timelocks and hash preimages?” So originally Miniscript was just an extension of descriptors. But what happened was that Miniscript spun out into quite a large research project that survived on its own. The distinction is a practical distinction right now that reflects that these are different projects happening at different times. But they are designed to work together and they are designed to complement each other in a way that there is no clear separation. That’s really where all this confusion is coming from.

Q - So it is all Pieter’s fault?

A - All Pieter’s fault, there we go. No it is largely Satoshi’s fault as always.

Q - The wallet was simple from Satoshi because it was just raw pubkeys. Somebody decided to hash the pubkeys and add SegWit.

Q - That was the mistake.

A - The original and worst brain damage is a long time ago there was what’s called a bare pubkey output where your scriptPubKey just contained a public key and scriptSig operator. Your scriptSig had to have a signature and then when you verified that, signature, public key, CHECKSIG. Then somebody, I think it was Satoshi realized what if we do a 20 byte hash of the public key. Now your output is take that 20 byte hash, hash whatever is on the stack which had better be a public key and check that the public key on the stack hashes to this specific hash. Then do the CHECKSIG. Now when you create an output all you have is this pubkey hash rather than a full pubkey so you’re saving about 10 bytes and then when you spend the coins you have to reveal the public key and then you have to reveal a signature. So spending is a little bit more expensive.

Q - When this was originally known you had uncompressed pubkeys so you’re saving like 40 something bytes.

A - That is an even older Satoshi mistake was allowing OpenSSL to parse public keys without restricting them in any way. We had these things called uncompressed pubkeys. Interestingly originally nobody knew about compressed public keys, somebody found them in the OpenSSL documentation and they were like….

Q - Nobody in Bitcoin or…?

A - Nobody in Bitcoin. Somebody said “Look at this flag. What if we used this flag?”

Q - Can you still pay to a raw uncompressed pubkey?

A - Yes and Core will recognize it. This is where things get really bad. If you ask Core what address corresponds to that it will give you an address.

Q - Not any more.

A - It will give you a legacy address that corresponds with that public key but then if you try to share that with anybody it will do the pubkey hash thing. Core will go from a public key to an address back to a scriptPubKey and it does a round trip.

Q - What do you mean by round trip?

A - I mean if you start with a scriptPubKey which is a bare pubkey, you derive an address from that by doing `listunspent` or whatever and then you try to get a scriptPubKey back from that address you will get a different scriptPubKey. You literally are producing an address that everyone else will interpret as corresponding to a different scriptPubKey. This is accidentally ok because Core doesn’t care about scriptPubKeys.

Q - The Core wallet will sample both?

A - Core munges all the scriptPubKeys into some cloud of nebulous vague Bitcoin-ness in its head. It will appear to work. If you are trying to write libraries or serious software that uses these things and you need to be precise about your scriptPubKeys, where coins are going and where coins are coming from it is very difficult to reproduce.

Q - It is so difficult to reason about. Rather than just upgrading the wallet we decided to shove that old functionality into a box which Andrew did and then build a new one next to it.

Q - It is a box where the legacy stuff can go to die.

Q - Or live forever.

A - In 2020 we will have descriptor wallets which behave the way you expect a Bitcoin wallet to behave. In 2019 I had a descriptor wallet. There was a lot of manual mental paperwork. I shouldn’t say I had software. I was using descriptors.

Q - I was using descriptors in 2019 too.

A lot of the confusion here corresponds to historical confusion and accidents that were made in the design of the Bitcoin Core wallet which in turn were the sole source of the address formats and the interchange formats that we use today. So descriptors clean this up and makes it a much clearer separation. And then Miniscript kind of came out of descriptors, Pieter and I both were doing quite similar things that intersected. You can think of Miniscript as a way of extending descriptors to not only clearly separate out the different address types but we can also use to separate out completely different policies. Suddenly we have this ability to think about multisig and timelocks and all this stuff. And descriptors happen to give us a great framework for that. We extend the descriptor framework from just distinguishing between address types to distinguishing between program types. That’s what Miniscript is. But then Miniscript became something much bigger because in implementing this as I talked about in my talk yesterday we realized there was a lot of sanity checking and a lot of analysis that we wanted to do on Scripts. Once we can support arbitrary Script looking things we realized there are a lot of mistakes it is possible to make. We’ll get into that a little bit in the next ten to fifteen minutes.

# Workshop

Let’s get started with some of the workshop stuff. In my Git repo [here](https://github.com/apoelstra/miniscript-workshop) I have some source code. Let’s go ahead and open some source.

`vim src/01-intro.rs`

[Here](https://github.com/apoelstra/miniscript-workshop/blob/master/src/01-intro.rs) is a simple program that I wrote to demonstrate using the rust-miniscript library. We are using Rust 2018 here, somebody asked about minimum Rust version. You can all clone this repo. You can see I have whole bunch of binaries that correspond to the different things we’ll be doing. The dependencies I’m depending on are the Miniscript crate version 0.12 which is the latest version of Miniscript. For those of you who don’t know Rust I’ve got the Miniscript descriptor. The Miniscript trait uses a descriptor type. Descriptors in rust-miniscript are parameterized by the type of public key. I’ll demonstrate what I mean by that in a second. I’m going to say I want to use the regular Bitcoin public key. A little bit of weirdness which is Rust specific.

`miniscript::bitcoin::PublicKey`

What I’m doing here is I have this Miniscript library, it is called a crate in Rust methodology. The Miniscript crate depends on the rust-bitcoin crate. The Miniscript crate actually reexports the Bitcoin crate that it depends on. If I want to use the Bitcoin crate I can depend on it myself or I can just use the one reexported from Miniscript. The reason I’m doing that is so when Miniscript changes its Bitcoin dependency version and I don’t feel like doing that, all my code that worked with Miniscript will just do the right thing. So you can imagine I’ve got my own Bitcoin specific stuff floating around. I don’t really care what rust-bitcoin version I’m using, there are new versions come out every time I feel like it and usually they are updating things that other people care about and I don’t. The easiest way to make sure I’m always using the version compatible with Miniscript is just using the export. That is a useful trick. Here is a descriptor. It is even a `wshpk` one which is the most confusing thing I could have chosen.

Q - An uncompressed pubkey, that’s not allowed in SegWit? It is not standard in SegWit.

Q - It actually doesn’t compile, the thing you did now. It throws an invalid public key error.

A - Let me go fix this. I was trying to demonstrate something dumb. Although if I did put a valid uncompressed pubkey in there it would actually work even though that is illegal in SegWit. That is a bug in rust-miniscript. Let me quickly file that bug. I think this is instructive. I can wait until the break to file bugs but I think we’re going to find a lot of little stuff like this.

I’ve fixed my descriptor here. What is going on here? I have a descriptor. In my mental model the `wsh` part is the descriptor saying that this program I want to hash it up and throw it into a SegWit output. The `pk` part is actually the program. I have the `pk` and then I’ve got the `020202…`, that is the most easy to remember key that is a valid EC key. I pass this into a descriptor and then here I’m going to compute the `script_pubkey`. Those of you who are familiar with Script can probably read this. I’m pushing a zero byte and then I’m pushing hex 20 which is 32, why am I pushing 20? WSH, thank you. I’m pushing 20, 32 bytes and that’s just a hash of all of this stuff.

Q - Why are you doing WSH of a public key?

A - Because this was the simplest thing. I wanted something that would fit on one line. Let’s change it. First let’s run this program so all my asserts are going to work. Then we can change it and we’ll see what happens.

Q - WPKH would be more obvious.

A - WPKH doesn’t have Miniscript.

Q - You could do WSH - PKH.

A - I could. Let me run through this. Then we’ll change it up to make it more sensible.

The scriptPubKey which as you can see is just a SegWit witness program. You have zero which is a SegWit version and then a 32 byte hash. I can also compute the witness script here. Here is the actual witness program. This is pushing 21 which is hex 33 and then 33 bytes which you can visually see is the public key. Then there are two different ways we can print this. For those familiar with Rust will recognize these as the display trait and the debug trait. If I print something that is using the curly braces that will give a user readable representation. If I print it using the brace with the question mark that prints the debug output that is supposed to have all the information that a programmer would need to see what is in the… Let me run this.

`cargo run —bin intro`

cargo: command not found. How could that be?

`vim ~/ .bashrc`

Let’s check on PATH.

`echo $PATH\`

That’s the problem.

`export PATH=“$HOME/ .cargo/bin:$HOME/bin:$PATH”`

Let me run the program.

`cargo run —bin intro`

This first line is printing the user readable representation. You can see that is identical to what we parsed initially. In the debug representation there is a lot more interesting stuff. A couple of things. The PublicKey part, this is from rust-bitcoin. It is just saying it is the compressed key, the actual EC key underlying it is this giant thing, that’s some uncompressed representation, it is not even the standard one. The debug output is whatever is the easiest to implement. What is interesting though is this stuff, this `K/onduesm`. There is a minor problem, let me fix this. Let me illustrate the problem first. So what do these mean? First off the K. The K is the important thing here. This tells me what type this Miniscript has. There are four kinds of types in Miniscript. Let’s go back to the [website](http://bitcoin.sipa.be/miniscript/). B, V, K and W, what these represent, we call them types, what they effectively represent is calling conventions. The most important one is B, the base. What a B Miniscript is is a Script where if you satisfy it it will take its inputs, pop them off the stack and leave a 1 on the stack if you satisfy it. If you dissatisfy it it will leave a 0 on the stack or possibly abort the Script but it is not going to do anything else. It is not going to let the Script continue without putting anything on the stack. There is a rule in Miniscript which is that the top level Script has to be a B. A Miniscript that you put on the blockchain has to be a B. It may contain subexpressions and stuff and those are not necessarily B, those can be V or K or W. Ks are fragments that leave a key on the stack. We have this type because there are many contexts where we use keys in Miniscript. We use them in the CHECKSIG context, we use it in MULTISIG, CHECKSIGVERIFY and so forth. Interestingly we might also use them in ORs. I will give an example of such a Script. Let me quickly describe and then we’ll come back. Suppose I have two public keys and I want to allow a signature with either one pubkey or the other. One way I can do this is by using the IF opcode. I do IF PUBKEY CHECKSIG ELSE OTHER_PUBKEY CHECKSIG ENDIF. This is wasteful, I’m wasting a byte here. What I can do instead is IF PUBKEY ELSE OTHER_PUBKEY ENDIF and then put the CHECKSIG on the outside. The use of this K type in Miniscript allows us to do that. I can have an IF statement which is like an `or_i` you can see this fragment is a “IF X ELSE Z” and our rules say that if we have an IF statement like this where both X and Z are Ks then the whole expression is itself a K. If both of these leave a K on the stack then the whole thing will leave a K on the stack. Now I can take `or_i` and wrap it in a CHECKSIG and now I have shared a CHECKSIG between two branches. These are the kind of optimizations that Miniscript enables. Going back to the code here you can see we have a problem because this top level Script here is not a B it is a K. That is a bug. This [one](https://github.com/apoelstra/rust-miniscript/issues/71) I filed last night, 17 hours ago. Top level must be B check happens on Miniscript, it does not happen on Descriptor. That is a bug. What about this `onduesm`? These are interesting objects. These are basically type modifiers. K is a base type, K means it leaves a K on the stack. We also have a bunch of other properties about this pk that are interesting. Each of these letters are an individual one. I’m going to highlight a couple of them and then come back. The first one is `o`. This expression always consumes exactly 1 stack element. Why is that an `o`? Because they consume a signature. A public key in Miniscript always consumes a signature which is exactly one stack element. In Miniscript I actually represent that fact, some fragments take one stack element, some take zero or two or more. There are cases where this is important. Let me go down to give an example where this is useful. There is no simple example. Where this is useful is where I use OP_SWAP here. Let me go to a different type fragment that I can more easily justify. `n` is nonzero, this is a cool one. It always consumes at least one nonzero stack element when you’re satisfying a Script. In Bitcoin you can give zero in place of a signature which is just the empty string and this is always an invalid signature. This can never be parsed as a signature. If you want to not provide a signature for some reason, maybe you are doing a 2-of-3 and the third signature check you don’t need, you can just provide an empty string. There are some fragments where you can satisfy them by giving them zero and others where you can’t. A public key check is one where you can’t so we have the `n` type modifier. Where this is useful, I think the coolest one is this `j` wrapper. Suppose I have a fragment `x` here which will never be satisfied by a zero. And suppose `x` is complicated, it might be impossible to dissatisfy or it might require a whole bunch of PUSHes to dissatisfy. I want to make this simpler, I want to change this so I can dissatisfy it by passing a zero. I have a fragment that cannot be satisfied by a zero input and I want to wrap that in such a way so I have the additional property that a zero will dissatisfy it but not do anything else. I can do this with this script fragment. I can pick `SIZE 0NOTEQUAL IF [X] ENDIF`. What this is doing is it looks at the input, if the input is zero it will check this, it will say what is the size? The size is zero. It will run `0NOTEQUAL`. Why do we do this? Here is a fun quiz question for whoever was that my [two hour rant](https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/) about Script the other day. Why can’t I just use the IF opcode here and say “If you give it a zero then don’t run it. If you give something nonzero then do run it”?

Q - Malleability check right?

A - Yes there are two reasons actually. One is the malleability check. There are actually many things you can give the IF that will succeed or fail. This is both sides of malleability checking. The consensus rules do not constrain what you put in a IF. If you are supposed to put a zero there some third party could in principle replace that zero with `0000000` or something like that and that would pass. Actually there are standardness rules against that. There is a rule called MINIMALIF that would prevent that from happening. Suppose I just did IF and we have this MINIMALIF rule that we promise to abide by. If I put something that is nonzero or 1 into an IF… I know it is trying to propagate. The point of this construction is in the case that I’m giving a nonzero output I actually want to pass that to my fragment `X`. Imagine `X` is checking a signature or something. If I just did IF X ENDIF and tried to put a signature there what is going to happen? The signature is not 1. 1 is also not a valid signature. The MINIMALIF rule is going to trigger where you are trying to switch on a signature, this is a malleability vector which it is there are many different signatures, and refuse to propagate. We instead have to somehow translate our input into something zero or one before putting in this IF. Does this make sense?

Q - To make sure it can be composed with another Script fragment?

A - Yes. Even simpler than being composed as a Script fragment is just so that I can use it at all when I’m giving it a nonzero input that isn’t exactly one.

How might we do that? How do you turn something that might be false or true and get that to be exactly zero or one? There are a couple of different ways and they are all broken in different ways. One way is directly running 0NOTEQUAL. Let me pull up my opcode list on rust-bitcoin [here](https://github.com/rust-bitcoin/rust-bitcoin/blob/master/src/blockdata/opcodes.rs). Scroll through to 0NOTEQUAL. This appears to do exactly what I want. Map zero to zero and map everything else to one. So why do I have this SIZE 0NOTEQUAL? Any guesses? 0NOTEQUAL is a numeric opcode. It will fail if you pass anything larger than 4 bytes into it. That’s why so we cannot use 0NOTEQUAL. So somehow we need another mapping that will map zero to zero and will map anything else to something that is smaller than 4 bytes in size. It turns out that OP_SIZE which will give you the size of a stack element will do exactly the right thing.

Q - So OP_SIZE will say that the size of a zero is zero?

A - Yes because zero in Bitcoin is the empty string.

Q - One of those zeros in an empty string. You can have other zeros.

A - Right so that brings us to the second issue. Suppose I was doing something more clever and just trying to use 0NOTEQUAL. Imagine we didn’t have this limit. There are actually a lot of things that are not the empty string which are in fact zero. Then I would be introducing a malleability vector because unlike IF which has a MINIMALIF rule constraining me all of my other opcodes have no such thing. As soon as I do this conversion now I would actually be introducing a malleability vector. I need somehow to enforce it so that there is only one thing that will trigger the zero and cause the IF statement to be skipped. I want this to be exactly the empty string. SIZE 0NOTEQUAL will actually do this.

Q - Negative zero is not…

A - Correct. The canonical negative zero is hex 80. The size of negative zero will be one for the canonical negative zero.

Another thing you might try is OP_NOT OP_NOT in a row. You get the same problem, there’s a malleability vector there. I think OP_NOT is a boolean operator not a numeric operator but I’d have to check the code. I think there are a couple of other ideas but SIZE 0NOTEQUAL is the one that is not a malleability vector. This highlights the benefit of having Miniscript. If you were trying to do cool things with Script this is the kind of thing that might occur to you independently. It did actually, we had this as part of a larger fragment before we realized we could generalize it to this j wrapper.

Q - Not as numeric?

A - If we tried to use NOT it would also fail.

Q - What does the j stand for?

A - It is probably one of Pieter’s six languages. We kind of ran out of letters at this point.

Q - It is either a joke or…

A - Pieter might have an answer for you but we were starting to run out of letters. You can see the a is ALTSTACK, s is SWAP, c is CHECKSIG, v is VERIFY, t is TRUE. They all make sense, is this the only one that doesn’t make sense?

Q - Joker?

A - This is likely and unlikely. We already had n for this form of non-zero. The n wrapper changes the output from something that might be zero or might be gibberish to something that is exactly zero or one. The j wrapper changes the input in the same way. They are both non-zero so I think we took a random letter.

Q - Just zero?

A - Just zero, just one.

This is the kind of thing that might occur to you naturally when you are trying to design Scripts by hand. Maybe you would notice the malleability issues and the numeric limit issues that I just mentioned once or twice. You are not going to notice it every single time. There are thousands of stupid things in Script that you run into in weird dark corners. The nice thing about Miniscript is that we have 38 fragments, this list goes down. You verify that 38 things are sensible. Most of them are really obvious. You can see that if you stick a one on there, is that going to cause a one to be on the stack? Yes. Only a few of them require any deep thought. We can spend all our time reasoning about these fragments. Once we have confirmed that the 38 fragments have… then we’re golden. The last thing I wanted to say. This whole thing started with this type fragment, this type property here, the n nonzero. You can imagine trying to do this wrapper but imagine that X could actually take a zero input and succeed. There are some fragments where this is true. In particular anything that uses a NOTIF but I think we might have removed those. I think the hash preimages, you could have a hash of zero. There are some examples of things that will take zero to be satisfied but I think they are all a bit complicated. If I put this here then suddenly I’m in trouble. I’ve got this X thing that I’m trying to execute. I give it zero in the hope of satisfying it but then the SIZE 0NOTEQUAL IF check catches it….. There is another bonus thing that SIZE does which is duplicate it. My original zero on the stack doesn’t get consumed. My zero gets copied into another zero, 0NOTEQUAL really turns it into a zero. IF consumes it and the original zero carries forward. This whole fragment if we dissatisfy it will leave zero on the stack which means it is a B and also an e and a few other things. If I was trying to satisfy X by giving it zero it wouldn’t work. I’d have undermined my Script, it would no longer be correct.

Q - That’s a really interesting comment in the design of Miniscript. Do you have any design principle about leaving the stack in the same state as the original subexpression before the subexpression was executed? SIZE here is modifying the stack, it is pushing two zeros on the stack. Presumably if you execute all this there will still be a zero on the stack. That seems wonky to me in the sense that there are these internal operations in the subexpression and you are still leaving the stack dirty without purposefully leaving a CHECKSIG or something like that to fail.

A - This intuition is what is captured by the B, V, K and W. These four base types reflect in what way specifically do we dirty the stack with these operations. We only allow ourselves four different ways that were sufficient for our purposes. That’s what the base type means. That’s why they are the base types as that’s the most important thing, is how they dirty the stack because that affects how they can post. Everything else is modifiers to make things continue to be semantically correct.

There we go. That is what the nonzero type property is for. It indicates that this is something I can wrap in a j. There are efficiency reasons I would want to wrap things in j or maybe even correctness reasons. That’s how j works. There are a bunch of things that went into the design of j, some surprising malleability and numeric things. I think we’ll stop here for the break.

BREAK

# Part 2

[Here](https://github.com/apoelstra/miniscript-workshop/blob/master/src/01-intro.rs) is the code that we did before the break. As John points out the scriptPubKey that I’m asserting here is missing a CHECKSIG. Why is that? The reason is that we have this c wrapper here. That takes a K type fragment and it turns it into a B type fragment. It does so by sticking a OP_CHECKSIG at the end of it which takes a key and a signature and turns it into a… Now if I rerun this.

`cargo run —bin intro`

We are going to see this assertion here is going to fail and we are going to see the reason it failed is that an OP_CHECKSIG will appear at the end here. There’s our `ac` right there. Let’s fix the assertion and then we will see down at the bottom, our type checker here, that K has turned into a B. You can see our original thing this `K/onduesm` and then by putting the c wrapper on it we change the type. One more thing I will show you on this before I move to the next example. Suppose that I change that c so that is also a v, v is verify. Miniscript is smart enough to know if you have a CHECKSIG followed by VERIFY to turn it into CHECKSIGVERIFY. CHECKSIGVERIFY I think is a v. I’ve got the v wrapper on the c wrapper. My original thing was a K that outputs a key, the c wrapper turns it into a B and a v wrapper turns it into a V. OP_VERIFY takes a zero or a one and turns that into an abort or a continue.

Q - This is not a valid Miniscript?

A - This is not valid.

Q - Should Miniscript give you an error for doing that?

A - Yes and it will if you try to try to pass the Miniscript into a descriptor…

Q - This is a notable difference from descriptors. The descriptor `pk` will give you the CHECKSIG. That’s going to be a problem for compatibility.

A - It won’t be because the top level `pk` is the descriptor `pk`. It is unfortunately also a bare Miniscript. But bare Miniscript shouldn’t exist.

Q - Does Pieter’s thing support bare Miniscript?

A - No. It also doesn’t support legacy. Pieter’s thing is SegWit.

This is an illustration of the c and the v wrapper and also what the type system does, how that works. One more illustration. Let’s change the v to a j which I think will actually type check. Let’s see what is going on. Let me print out the Miniscript.

`println!(“Script: ()”, my_descriptor.witness_script());`

The reason I’m doing print here so I can see…. I put the j wrapper in place so now we have SIZE 0NOTEQUAL OP_IF going on here. You can see my original fragment, I’ve got the 33 byte key followed by the CHECKSIG and I’ve wrapped that in an IF and then the SIZE check. Let me quickly disable this assertion and we will see what has happened with the types. This still works. The j turns the B into a V. The original thing was B and all this stuff. Once you wrap it in the j wrapper, the OP_IF OP_ENDIF thing we see nothing has changed except the e type modifier has disappeared. We don’t have time to talk about malleability too much but I will quickly say what e means, this is a malleability type modifier. e means there is one canonical way to dissatisfy the fragment. What is interesting is this continues to be true. If you were dissatisfying this for some reason, there is an OR and you need to run it but you don’t want to satisfy it because it is a branch not taken then e tells you can do so in a non-malleable way. This is true for a CHECKSIG kind of thing. There is only one way to dissatisfy it assuming you are in the Policy rules which is provide an empty signature. Invalid signatures are rejected by Policy, I forget the name of this rule. I wish it was consensus but it is not. Then I do the j wrapper and once I’ve done the j wrapper I’ve lost the e fragment. Why would that be? The reason that what e means is there exists some dissatisfaction that’s unique. The j wrapper potentially adds a dissatisfaction. If you pass the zero string this is dissatisfied. The j wrapper doesn’t know that we already have the zero dissatisfaction and that was unique. You can imagine that if rather than a CHECKSIG I had something more complicated, a unique dissatisfaction but that dissatisfaction was not the empty string. Then the whole fragment I could dissatisfy either by passing a zero, in the j wrapper the OP_IF is going to leave zero on the stack which is dissatisfied, or I could pass the canonical dissatisfaction of the inner thing that would be non-zero by assumption. The j would pass, it would pass here and we’d get a regular dissatisfaction. The j wrapper has changed from having a unique dissatisfaction to potentially having a non-unique dissatisfaction. In this case we are actually ok but the type system is not smart enough to detect that which is why this e fragment goes away when we wrap. Does this make sense? This is a subtle thing about building Scripts where you take something that you convince yourself is non-malleable in some sense and then you do something that seems sensible like wrapping it in a IF ENDIF and then guarding the IF so it still works. That something might actually break your malleability assumption. You’re not going to notice. Everything you do has all these weird interactions. The nice thing is that the Miniscript type system will catch this for you. It will say “Wait a minute. You used to have a unique dissatisfaction but when you added this wrapper you added another dissatisfaction. Suddenly your dissatisfaction is not unique anymore.” Which means in the wider thing there is some context where it might be dissatisfied, that’s a malleability vector. Miniscript will detect that and reject my Script or at least flag it as being malleable.

Q - The unique dissatisfaction for a CHECKSIG is zero?

A - Yes it is zero. In this case it is actually ok. I’ve added a zero dissatisfaction but that was already a unique one. This reflects a limitation of the Miniscript type system. In principle we could add another type modifier which says “There is a unique dissatisfaction and the zero dissatisfaction.” Then the j wrapper would be able to detect that and say “If the unique dissatisfaction was zero then preserve this property.” I wonder if it is worth adding that to the language. Would it save space? Maybe, probably. I don’t know. That is something Pieter would have to write a fuzzer for. Importantly what Miniscript is doing here is the same thing.

Let’s move on from the intro Script. Let’s do one more type system illustration and then do satisfaction. Then we’ll do composition.

Q - That’s a change you would introduce to the compiler because all those modifiers are not present in the Policy. If you were to add these modifiers then the compiler would add these and create more optimal Scripts?

A - Maybe the compiler already tries this. The way we implemented the compiler is it does everything you can do and then those type checks. If it is something not sensible it would reject it after the fact. We are not very conscientious about not even trying things because that would require a lot more code. It would only give us a small speed up.

Q - Try everything?

A - We don’t try literally everything. I was pretty crude in what things I implemented. There is a good chance that the compiler would do the right thing. There is also a good chance that it wouldn’t. I don’t even know because my compiler stopped working…. I just blindly ACKed and merged it. That’s not true, I did look to see that it didn’t impact any of the other code. It matches what Pieter did because Sanket and Pieter used Pieter’s tool Branchtopy to produce a hundred billion Policies and compiled it using his compiler and Sanket’s compiler.

Q - …

A - That is in Pieter’s Miniscript.

What is cool is that Pieter knows C++ but not Rust, Sanket knows Rust but not C++ so they are actually unable to copy code from each other. These are two completely independent compilers that nonetheless matched on the output. Let’s move on. [Here](https://github.com/apoelstra/miniscript-workshop/blob/master/src/02-types.rs) is a second example. This illustrates a few more things about the library. I’m going to rush through a little bit because I want to talk about how to satisfy things and I want to talk about how to compile Policies in the next hour. One thing here, I’ve changed the key type just to illustrate that I could do that. There are a few different key types out there that we could use. There is the Bitcoin public key, probably usually what you want to use and that represents just a Bitcoin public key which is a EC key, it might be compressed. We also have this `DummyKey` which is used for testing. This is an object provided by the Miniscript library. This is nice. It parses and serializes the empty string and just creates a single object dummy key. I’ll run this code.

`cargo run —bin types`

Imagine I tried to put something in here like a key or whatever. This is going to fail and say “non empty dummy key”. The only valid dummy key is the empty string. One other key type I’m going to try is string. This is kind of cool.

`”wsh(c:or_i(pk(Andrew), pk(Sanket)))”`

This still works. Now I have a public key and these are just strings. I can no longer translate this into a Bitcoin Script, I lose a lot of functionality but I can parse, serialize and do analysis on these. This is a really useful feature both in testing and storing keys in interesting ways. There is other functionality that I’m not going to go into that allows you to translate all the public keys, we provide a function to translate public keys. In Liquid we actually parse Scripts like this where we use a string representing all the participants. After we have parsed that and done a couple of sanity checks then we look up in our hash table of which peers, which connections, which keys and we translate the string keys into a richer type. We have a bunch of extra errors that we can throw at that point. We turn that into a richer type which either indicates a raw functionary key or one that is tweaked for pay-to-contract hash or whatever. There are a bunch of fairly advanced abilities explored by this library that let you do very rich things with keys. We’re going to stick with dummy keys here. One quick thing that I want to illustrate. I have a more interesting Script here.

`”wsh(c:or_i(pk(), pk()))”`

I’ve got this `or_i` which is the IF ELSE ENDIF thing. I have my c wrapper on the outside of my `or_i`. Let me print out this descriptor.

```
let descriptor = Descriptor:: <miniscript::bitcoin::PublicKey>::from_str(“wsh(c:or_i(pk(020202….), pk(020202…)))”,
)
.unwrap();
println!(“***Witness Script: {}”, descriptor….ss_script());

let ms = Miniscript <DummyKey>::from_str(“c:or_1(pk(),pk())”,
)
.unwrap();
```

We can this Script here. I’ve got this OP_IF key, ELSE key, ENDIF and the CHECKSIG on the outside.

Q - You’re taking advantage of the feature that the Miniscript compiler doesn’t know those two keys are the same. It thinks those are two different keys?

A  - Yes, that’s correct. It is not even the compiler. The entire library assumes these keys are distinct. It makes not attempt to detect duplicate keys. It is potentially useful enough that I don’t want to outright forbid it. But you are on your own as far as malleability analysis. In particular this is malleable. How do you satisfy this? You either provide a zero indicating that you should use the right branch or a one indicating you should use the left branch, followed by a signature. If you try to use this Script the same signature is going to work for both branches. So a third party can take your 0 or 1 and change it to a 1 or 0 and it will continue to be valid. Miniscript thinks this is not malleable because you’ve got an OR of two things that require keys. It actually is because I reuse keys.

One other thing I want to illustrate is I can pull this c inside and now I have two CHECKSIGs.

`“wsh(or_i(c:pk(020202….), c:pk(020202…)))”`

Now I’ve moved the CHECKSIG on the inside and now you can see I’ve got two CHECKSIGs. IF KEY CHECKSIG ELSE KEY CHECKSIG. They are both valid Miniscripts, one of them is a byte shorter. If we were starting with Policies and using the compiler, the compiler would always notice the reuse every time. This is one reason that you might want to use a compiler instead of manually writing Miniscripts. Let’s go back to the start. As I mentioned there is a bug in the library right now that lets us parse descriptors that are not validly typed. I’ll illustrate how it should work. I’m passing a Miniscript rather than a descriptor, I’m going to stick a v in front of here and we’re see it is going to fail.

`”vc:or_i(pk(),pk())”`

There we go. It says “NonTopLevel”, there’s this giant thing here. It tells you what it parsed in what mode. I can see if I’m developing it is not the most nice error messages in the world. “NonTopLevel” means that the top level Script is not a B. Then it actually wrote in detail what it is. I can see first of all that it is a V not a B. I can even see how this happened. I can check through this. Are the keys correctly formed? No I’ve got this `or_i` here and both branches are Ks which is correct. The c wrapper turns it into a B and then the v, wait a minute that’s where I went wrong. With a little bit of thinking I can figure out what went wrong. It is an open API question. How can I produce more useful error messages here? There are lots of ways where the top level will wind up not being a B. Pretty much if you make any mistake anywhere in a Script this will cause a cascade of errors that will propagate up to the top level being wrong. The chances are somewhere along the line there was an actual mistake. I don’t know really how I can be more intelligent about providing guidance to the user here. It may be that you have to do the compiler route where you have people file literally hundreds of bugs about confusing error messages and you have hundreds of heuristics.

If you really want to do bad untyped Miniscript here is the way to do it. You reach deep into the library, you pass it a generic expression, an expression is just a bunch of strings with parentheses lying around them. You can print that expression directly into a Miniscript. This conversion from a tree to a Miniscript, it does not do any type checking. Is this useful ever, it is very unergonomic, it should be because it is a bad thing to do, you shouldn’t do it.

Let’s move on. I’ve been saying that Miniscript can encode Script but up until now I’ve been writing Miniscript in the canonical form and describing what the Script is. If you have an actual Script like this thing, this is a raw Script encoded in hex. I’m going to parse that as a Bitcoin Script and then I’m going to use the Miniscript parse function here to convert that Script to a Miniscript. I’m going to run that.

`cargo run —bin script`

Here is my original Script that’s decoded in a nice way. Doesn’t that look scary? It is like a nested IF. This probably came out of our fuzz tests. There’s a unit test in the Miniscript library called [all_attribute_tests](https://github.com/apoelstra/rust-miniscript/blob/5ba9bfe01780023062576f6fe4ccd2a9ced9c1db/src/miniscript/mod.rs#L451) that I think Sanket produced somehow which will do weird stuff like uuj. Let me quickly check what the u wrapper does. u is unlikely, you take an OR between your thing and zero. Why would you do that? It is basically the same as j. You are taking your dissatisfaction potentially with something complicated and you’re changing to provide a zero for the IF statement. Here rather than using SIZE 0NOTEQUAL we actually require the user put a zero or one in place. It may be surprising that it is ever more efficient to use SIZE 0NOTEQUAL rather than putting a zero or one. Zero is one byte and one is two bytes and SIZE 0NOTEQUAL is always two. But in fact it is. Part of the reason is that these are different constraints. The fact that these are more efficient is a statement about the world that Pieter and I checked. What we’ve done here is something very unrealistic. We’ve taken the u wrapper and then applied it again which you would never do. There is no reason to do that unless you are trying to file a Miniscript error. We parse the Script and we get our Miniscript. Imagine we mess up the Script somehow. Let’s change that `63` to `61`. Now when we parse you can see `InvalidOpcode(OP_NOP)`. `61` is not a valid Miniscript so it won’t parse it. What if instead I manipulate the public key? I’m going to change this `d0` to a `d1` which 50/50 will cause it to fail. Near the end I’ve got these zeros. Let me quickly show you the Script again. I’ve got this OP_0 and OP_0 here which are part of the u wrapper. If I change one of these to a 1… `Unexpected(“\#104”)`. I changed the zero to a one I thought, what could that possibly mean? I’m sorry the one is `0101`.

Q - Isn’t one `51`?

A - Good call. Let’s use `51`. I put `01` which means push one byte and then `68` which is my ENDIF. It was interpreting that as data. Then it was running out and there was no ENDIF. But how that turned into that error message I have no idea.

Q - Isn’t `68` in hexadecimal that `140` whatever?

A - Yeah, I was seeing the push of one. You are saying number `101` to indicate that this was a decimal number, not a hexadecimal number. Another thing Core does wrong is using the same encoding for both.

I have changed the zero to a one. I have OP_PUSHNUM_1. This is actually a valid Miniscript. You can see my u wrapper here is now an `or_i` between this u thing and 1 which is a valid Miniscript. It actually does the right thing. You break things and Miniscript will catch you.

Q - You should change one of those `63` to `62`.

A - Look at that, “InvalidOpcode(OP_VER)”. That’s funny.

 Let me change a `1` to a `2`. “Unexpected(“\#2”)” because the number 2, there is no context in which that should ever appear…

Q - Is it fair to say that if you have the same identity twice in the Script it is something that you would never do?

A - I think so. If you use it twice that may actually do something. If you do `jj` that will actually change the type properties so I can’t promise you that that is useless. I am 95\% sure in every single case it is useless. It will do something but that something will be adding this or losing type properties. The more type properties you have the better. This just came from the fuzz test.

Q - All valid Bitcoin Scripts should be parsable by…?

A - That was the dream. Ultimately we can’t do that. There are a couple of reasons. One is conceptually there are things like Peter Todd’s hash collision bounties. There are not really any way to represent that in Miniscript unless we add it explicitly, hash collision bounty. What does that mean? You can’t think of that as a combination of signature checks and hashlocks or whatever. Maybe you could use hashlocks if we had a notion of equality and inequality. But even those don’t fit into this tree form where you’ve just got a collection of spending conditions in a tree. The goal is that if you have a monotone function of signature checks, hashlocks and timelocks and you have no repeated keys or repeated subexpressions then you can express that as a Miniscript and there will be no more efficient Script that does what you want. I think that is not always true but it is really close to being true. In practice I think it is true.

Q - Is it possible to take a Script then convert it to Miniscript and then find another Script that is more optimal?

A - This happened with Liquid where we were using a opcode to count how many signatures we had. If we had 11 signatures it would be part of our 11-of-15 multisig. If we had 2 it would be part of the 2-of-3 emergency multisig. With Miniscript we originally saved one byte. Then Sanket came in and added these pubkey hashes and we were able to save another couple of dozen bytes by replacing our emergency keys with pubkey hashes. Our CHECKMULTISIG that doesn’t work with hashes, it is like an explicit threshold construction, it turned out that saved us a bunch of bytes. The reason that is efficient is because we never use our emergency keys so there’s no reason to play with them here explicitly. That’s one example. I heard from Ethan Heilman in Boston who has a company called Arwen that does some sort of non-custodial altcoin trading that the HTLC like objects they were using, they found a couple of bytes savings by using the Miniscript compiler. With the Lightning HTLCs we were able to find more efficient versions. That is a little bit academic given it is such an event to change things that are specified in BOLTs. We were able to find more efficient versions of HTLCs. In a lot of cases, even hand rolled Scripts by really smart people.

Q - In our HTLC for Miniscript it did an interesting thing where usually it has 1 or 0, it depends on which branch you select. The Miniscript policy spits out one that just does the signature check first and uses that result to branch what you want to do next. If the signature matches it goes to the redeem and the opposite thing. If the signature doesn’t match it means that you want a refund probably and triggers the timelock.

Q - Your original one was you would branch and then do the signature check?

Q - Yeah. There is a naive version of the HTLC where you let the user decide what you want to do. If you try to interpret whatever is there as a signature, if it works you probably want to redeem, if it doesn’t it is probably the refund back.

A - That’s cute.

Let’s jump ahead. Thomas (Eizinger) wrote a compiler for me which I shamelessly stole. I kept his copyright notes here. This is from the rust-miniscript library and he quickly copied it in during the break. You can see it is wrapping funny because I have a small Terminal here. Here is a HTLC Policy. Actually this is a cool new use of the format macro that I haven’t seen before. You can see the Policy here is the HTLC. You’ve got an OR of two things, you’ve got either a hash preimage of the `secret_hash` and a signature with the `redeem_identity`. Or you have a timelock for the HTLC `expiry` and this `refund_identity`. You can see Thomas has added weights to these saying the first branch is much more likely than the second branch to be taken. That guides the compiler saying the compiler should try to minimize the size of that code at the expense of potentially producing much larger witnesses because probably it will never be taken. So probably the witness size doesn’t matter but the actual code there will always be there so we should minimize that. So what happens? Let me illustrate for people who want to do this at home a few things that we pull in. We pull in this object `Concrete`. There are two types of Policies in rust-miniscript. There are semantic Policies which are the ones you get where you start with a Miniscript and throw away all the extra information. Those are what you use to do analysis and stuff. Then there are concrete Policies and those have weights on the branches. You can always get to a semantic Policy by throwing away information. We have a function called `Lift` that I think we use later on. We’ve imported the `Liftable` trait. We create this concrete Policy, we parse it and you can see it looks kind of like Miniscript. We parse it in the usual way using the `from_str` trait. Then we call this function `htlc_policy.compile`. The compile turns a concrete Policy into a Miniscript. Then we wrap it in a `Wsh` descriptor. The compiler just produces an optimal Script. The compiler does assume it is going to be embedded in WSH by the way. If you compile something and put it into a P2SH it might be slightly suboptimal. The reason is that pre-SegWit it was equally efficient to encode a zero or a one because zero is opcode `00` and a one is opcode `51`. In SegWit a one is slightly more expensive because a zero is `00` and a one is `0101` because they are byte strings rather than opcodes. The compiler takes that into consideration when deciding how to order IF branches and stuff, whether the zero or one will be more likely to be taken. As a result it might make decisions assuming the SegWit case where zero is cheaper that will cascade these decisions that are globally suboptimal if you are not using SegWit. That’s fine. Not using SegWit is a global suboptimality by itself.

Q - And a malleability problem.

A - And it may be a malleability problem. In a lot of cases it is but I forget specifically when. I think a lot of the library disables itself when not using SegWit although I forget. I haven’t thought of this in a while.

Q - I thought you wanted to not use SegWit sometimes?

A - I did but for very simple things. Like only for what Liquid does which is so simple that I could do it even pre-SegWit. It was nothing weird. It was like the j wrapper didn’t quite do the right thing. I really should have documented that somewhere. Obviously I will forget it so why didn’t I write it down?

We call it `htlc_policy.compile`, we parse the Policy, we compile it. The compiler output is going to give us a Miniscript and then we wrap that in the `Wsh` descriptor. Then we print out what the resulting descriptor is and we can see this is a Miniscript. I was wondering what the hell Thomas was talking about, about taking the output of a CHECKSIG and using that to switch. I was like “Miniscript can’t do that”, I forgot. We totally added this `andor` thing which does exactly this. Let me show you on the [website](http://bitcoin.sipa.be/miniscript/) what `andor` looks like. Here it is. It does some predicate and if we scroll down to the type checks the predicate has to have a couple of restrictions. X has to be Bdu. What does this mean? The B means that it will output something nonzero on the stack when it is being satisfied. The u means that that nonzero is going to be one and the d means it is possible to dissatisfy it thereby putting a zero on the stack. These three conditions Bdu tell us that this X here is possible to satisfy or dissatisfy. If you can either satisfy or dissatisfy it in those cases it will output one or zero. That means I can stick the result of that in the IF or NOTIF as the case may be. In the case that it succeeds X, if not it will fail it will be Y, in the case it does not succeed you’ll use Z. Why do we use IF rather than NOTIF? It is to make the parsing easier. If we didn’t use the NOTIF then there would be a parsing ambiguity between this (`or_i`) and this (`andor`). When we see the IF we don’t know whether X is going to appear. There’s a neat fact about parsing Miniscript which is that it is always possible to disambiguate the next thing. There are two exceptions that are easy to deal with. It is always possible to disambiguate what you are doing by doing a one token look ahead and literally looking at what the token is. Whereas if we were using IF here I would have to parse the entire X and look what X was to figure out whether that was something sensible. It would be difficult to distinguish between that (`andor`) and this `and_v`. If I had an IF here then if I saw this I might wonder is this actually the `or_i` and this is part of this X Y `and_v` or is this part of `andor`? You don’t need to follow. The point is that it is difficult to parse. Conveniently Satoshi provided us two IF opcodes. In this case it literally doesn’t matter which one we choose so we use NOTIF in that case but nowhere else. You can see it is here but this is actually just a special case. When we see NOTIF we know we are in `andor` which makes parsing easier.

Going back to our compile HTLC. You can see we are using the `andor` construction. We do the signature check on the `0222……` which is a redeem identity. If the signature check succeeds then we check the hash preimage here. If it fails that means that the left branch of this IF is obviously not going to succeed so we need to do the right branch. If it fails we do the other check.

Q - Is `pkh` used because it is smaller but when you spend it it will be larger?

A - Exactly

Here is a little bit of extra data that Thomas added to this test case. We can use this `lift()` function and what it does is throw away the extra information and gets this pure looking thing. One interesting thing is that when you lift to these abstract Policies all your public keys become pubkey hashes. Why do we do that? Because if you start with a Miniscript that has got a pubkey hash in it it is not necessarily true that you can get a pubkey from it. You need to have some lookup table or something. You can’t undo the hash. In the abstract Policy I didn’t want to distinguish between pubkey and pubkey hash because they are semantically the same sort of thing. Since I can get from a pubkey to a pubkey hash always by hashing it and I can’t go in the other direction I just coerce everything into pubkey hash in the abstract Policies. This is unfortunate. I argued against including pubkey hash in Miniscript for a long time because of this but I’m glad that I didn’t because we obviously save a lot of bytes by doing this. You can see the `script_pubkey`, you can see the `witness_script` here. What is cool up here, let’s print a bit more data. Let me look at what I have for this descriptor. What methods do I [have](https://docs.rs/miniscript/0.12.0/miniscript/descriptor/enum.Descriptor.html)? `max_satisfaction_weight`. Let’s print that out.

`println!(“Max sat weight: {}”, htlc_descriptor.max_satisfaction_weight());`

Q - What is going on here? Are you decompiling to Policy? Are you going to that level of abstraction and then back down?

A - Sort of. It is very similar to decompiling except I am not actually getting the original Policy back because I lose the weights. It is basically decompiling but it is much simpler than decompiling. What I am doing here is a direct mapping from every Miniscript segment corresponding back to something. If I can see `pk` or `pkh` that maps to a `pkh`. If I see any of the three different ANDs that maps to an AND. If I see any of the four different ORs that maps to an OR. If I see an AND OR that maps to a nested AND and OR construction. If I see either of the two thresholds that maps to a `thresh`. It is more like disassembling. I’m not sure what other metaphor. I use the word lift which is a category term. I’m preserving all the semantics whilst mapping into a simpler space. You can do it by hand, you can do it visually if you want. The value in that is that once you have one of these abstract Policies you can do some cool stuff. You can say “What does this Policy look like at time zero?” and any clauses that are timelocked you will just throw away. Maybe it will tell you it is unsatisfiable, maybe it will tell you it is simpler. You could say “What does it look like at time 1000?”. You could ask it the minimum number of keys that you could possibly sign with. There are a number of questions you can ask about the abstract Policies that are more difficult to ask about Miniscript because the Miniscript has so much noise in them.

Q - You are asking the questions at the Policy level? I thought you asked those questions at the Miniscript level.

A - No. The questions you ask at the Miniscript level are things like what is the witness script, what are the costs, how do you make a witness? The things you ask at the Policy level are the semantic things. Can I sign with these keys? Do I need these keys to sign? What does it look like at time zero? What does it do?

Let me quickly grab the `max_satisfaction_weight` right here.

`cargo run —bin compile`

Max satisfaction (Max sat weight) is 292.

Q - The max satisfaction weight is based on the Policy so it would have to bury all the weights or it takes the worst case?

A - It takes the worst case. That satisfaction case takes the worst case. That includes I believe the weight of the witness script and it also includes the worst case witness size.

Q - Is that what we use for fee estimation?

A - Yes this is what we use for fee estimation. Like in Liquid we use that for fee estimation. In principle it is possible to be smarter but it is difficult.

What if I change my Policy and I say that the first branch is actually way more likely than the second branch?

`or(1000\@and(sha256({secret_hash}), pk({redeem_identity})), 1\@and(older({expiry}),pk({refund_identity}))’

That 292 you see, it’s the same. Does it really not matter? I changed the 10 to a 1000. What I wanted to do was change the 1 to 1000.

`or(10\@and(sha256({secret_hash}), pk({redeem_identity})), 1000\@and(older({expiry}),pk({refund_identity}))’

Let’s look at why the assertions are failing.

`cargo run —bin compile`

Here is the descriptor that we get and here is the descriptor that we expected. Here is the original one and here is the new one. You can probably see easier than I can that things have been reordered.

Q - In the Lightning case we check the other signature first and the timelock and only then go to the preimage.

A - That’s what you’d expect. All we are doing is checking the other signature first.

I bet you that the max satisfaction weight if I change it all will be 1 byte larger. Actually it is not the max satisfaction weight that will change, it is going to be the average satisfaction weight. I do know how to get that. We’ll copy and paste the Policy into [Pieter’s website](http://bitcoin.sipa.be/miniscript/) because my byte code won’t help with it. Let me first comment out all these assertions so I can just jump to the max satisfaction weight.

Q - Pieter outputs the average satisfaction?

A - Yes when he is compiling I think.

I run this. `Max sat weight 325` 325? Why would it be that much bigger?

Q - I think it still checks the first signature first and then the other signature check.

Let’s take a look at what changed here although we’ve only got 15 minutes left. What actually changed that would cause the max satisfaction weight to increase? We are still checking the first signature first. Did a pubkey hash turn into a pubkey?

Q - The pubkey hash is still a pubkey hash. You are adding the pubkey when you are satisfying it.

A - But worst case I would still have to do that. In an average case…

Q - You should ask Pieter’s website.

A - Pieter’s website won’t… Just like figuring out the errors when there are type problems it is very difficult to answer questions like this in a nice way. If we trace through this source code and see what is happening my experience is that Miniscript is right and I’m wrong.

Q - The second and third arguments are switched?

A - It looks like the ANDs are maybe nested differently which is surprising.

Q - The confusing part is that the headers are the same, the public keys are the same. If you change the public keys then we should see that actually the public key changes and the branching switches with the preimage.

A - Are the public keys the same? Ok, this problem. We are going to try (changing the `refund_identity` too `03333333`). This is not going to work. Why is there only one public key that appears here?

Q - The other one is hashed. It is the same hash.

A - Ok we can see that a different public key is hashed from the previous case. There we go. Miniscript is always right. Originally the worst case was you’d have to do a public key hash that is expensive and a timelock which is free. Now the worst case is you have to reveal the hash and the public key hash and that is quite an expensive thing.

Isn’t that cool? This stuff is so hard to do by hand. If you have Miniscript to tell you the answer in advance you eventually get it.

Q - With Miniscript you could not only calculate the worst case but the distribution?

A - Yes.

Let me quickly copy the Policy here (into Pieter’s website) and put the Script back. The `secret_hash` is H, D is the `redeem_identity`, the `refund_identity` is F. Let’s hope I didn’t leave too many parenthesis here.

Q - The expiry also still uses curlies.

`or(10\@and(sha256(H),pk(D)),1\@and(older(4444), pk(F)))`

Let’s look at the spending cost analysis. At a worst case, 292. Here it is giving me some averages here. You can see by the fractions this is an average. On average given what we provided it is 212. It is a weighted average of all the different spending paths. If we do the same thing, edit the unlikely one.

`or(10\@and(sha256(H),pk(D)),1000\@and(older(4444), pk(F)))`

Our compilation should do the same thing. Rather than the F being hashed we’re going to see the D gets hashed. Miniscript output from website:

`andor(pk(F), older(4444), and_v(v:pkh(D)),sha256(H)))`

My aggregate spending cost (179.673267). Did that go down? Interesting. That tells you something about the HTLC. If the HTLC worked in the opposite way it would actually be on average cheaper. Unfortunately that is a fact about HTLC and not a Miniscript thing. The fact is that the hash preimage one is the more common one. Any questions before I very quickly run through how to satisfy things?

Q - Does this already work with Tapscript?

A - No it doesn’t. Somebody I think implemented this and forked maybe Pieter’s repo and added a bunch of Tapscript stuff.

Q - With Tapscript would the optimizations change?

A - Yes. At least on the compiler side it would be nontrivial to implement. Elsewhere I think there are a couple of design questions.

Q - The fuzzing repo is designed to crash the compiler?

A - I have a fuzzer that is designed to crash the compiler. Let me go back to my compile Script here.

`vim 06-compile.rs`

I start with the concrete Policy and compile to descriptor and then I lift it in this assertion. I have a fuzz tester that compiles things, it will lift the original Policy and it will lift the compiled Policy and it will make sure that those are equal which means that the compiler has not miscompiled something. I actually have a fuzz tester for the compiler changing the semantics.

Q - You and Pieter also test both implementations?

A - Right. Pieter also generated like 100 billion Policies which he ran the tests on. That was very tiresome. Sometimes we would deviate in like the 15th digit of our estimated weights. Sometimes we would agree but have reordered things in a way that didn’t matter. Eventually we were able to heuristic away all the discrepancies and we got 100 \% matches.

I have fuzz testers for that. I also have fuzz testers where you can parse and reserialize Policies and Miniscripts in the string format. And I can go from Script to Miniscript and back and I think from Miniscript to Script and back. It is always unique. We actually found a lot of cool things, it is pretty aggressive, pretty thorough. Although if you look at the repo there are still a couple of bugs that I think should’ve been caught but weren’t.

`vim 04-satisfy.rs`

So if you are a wallet developer maybe the most useful thing about Miniscript is the ability to satisfy automatically. I’m going to go through this example which I also cribbed from the Miniscript examples. This one I think I wrote. Apologies if anyone in the room wrote it and I’m taking credit. It was me. Thank you Thomas again for that HTLC example. That was really illustrative, really cool. Let’s look at signing. Signing is a bit more involved. Obviously I need a bunch of extra data. Here’s a Bitcoin transaction that I’m making up. It is going to spend this output, the outpoint is the zero outpoint. That is obviously not real. The output is an empty scriptPubKey, that is obviously not real.

Q - It could be?

A - It could be real, it is very unlikely.

Here is a bunch of data, here is a signature, here is the DER point, the public keys. Here is actually the code. I am going to take a descriptor. This is actually something real. This is a witness script hash 2-of-3 multisig.

`wsh(thresh_m(2, {}, {}, {}))`

I parse this descriptor into a Bitcoin pubkey descriptor. I check that the scriptPubKey and stuff are what I expect them to be. The witness Script as you can see make sense. There is an OP_2 followed by 3 pubkey pushes, OP_3 and then CHECKMULTISIG. Then I’m going to try to satisfy this. Here is the actual satisfaction, the 1-of-2. What am I going to do is call the `descriptor.satisfy` function and what I give it is my `tx.input`. What the `satisfy` function is going to is set the scriptSig correctly and it is going to set my witness stack correctly based on whether the descriptor is bare or P2SH or whatever. The `satisfy` function will do the right thing. I also need to give it a set of signatures. This is a cool API thing that I don’t have time to get into. What is this `sigs` variable? The `sigs` variable is actually a hash map from Bitcoin public keys to Bitcoin signatures. The simplest thing to do is literally create a hash map of keys to signatures. I stick the signatures here and then you pass that to the `satisfy` function. But I can do much more interesting things. This will actually take any type of object that implements this satisfier. I can give it a map from keys to signatures, I can give it a map of hashes to preimages. I don’t know how to encode timelocks, I think I have another object that does that. I can also give it lists of these things. I can take a signature… a hash map, point it to those inside a tuple and then I can pass a tuple to this and it will use both of them. I can also create some custom object and implement this trait telling it how to get signatures and how to get hash preimages and stuff like that. This `satisfy` function is extremely flexible but the most straightforward and common way to use it would be to make a standard library hash map, keys to signatures. A `BitcoinSig`, that’s a secp signature and it is a sighash type. As I mentioned in one comment further down by default if you put a signature in that hash map it is just going to use if that is efficient. It doesn’t verify the signatures. The reason being that it can’t verify the signatures without knowing the sighash. If you want to verify your signatures, this is something we have to do in Liquid, I actually have a custom object that implements the satisfier trait. This object knows what transactions are being signed, it knows a whole bunch of things that the functionaries should be doing, it does checks and it will log if anything goes wrong. I included my own satisfier which actually verifies signatures and which will signal if something is wrong.

Q - You could use verify…?

A - You can use verify afterwards. Verifying, like running a Script interpreter? What did you mean by that? There are two things I could do. One is I could verify the signatures outside of Miniscript. Or I could try to run a Script interpreter and check whether the Script succeeds.

Q - rust-bitcoin does not have a Script interpreter.

A - Correct. Or I could use Sanket’s Miniscript interpreter which if I had an extra 3 hours we could play with. I think one straightforward thing to do is just verify the signatures and satisfaction time.

Real quick I will show you what happens here. I am printing the unsigned transaction and the signed transaction.

`cargo run —bin satisfy`

The unsigned transaction you can see is empty, the signed one now has a witness here. A couple of things to notice. It puts the empty PUSH that CHECKMULTISIG requires in the right place. It puts the signatures in place. It orders the signatures correctly, Miniscript does it for you. Somewhere in one of those things is the witness Script. I apologize for the crappy non text output. The reason is that the witness type is a vector of vectors of bytes. By default Rust outputs those in array form. There is a discussion on the rust-bitcoin IRC that we should probably make our own. Two other things to demonstrate if there are no questions. If I insert a third signature here. Then we run the program and we are going to see all these asserts still succeed. I gave it 3 signatures and it only used 2. It is even a bit smarter than this, I gave it 3 signatures and if one of them was a byte longer than the other which happens sometimes randomly, it will drop the expensive one. It will take the shortest signature which is the kind of optimization that was fun to implement with Miniscipt but would not be fun if I was doing it for every individual project. If I give it only one signature it is going to fail because it is a 2-of-3 threshold. You can see `assertion failed`. The satisfy function just returned an error. Let me see what error it returns. Rather than asserting I’m going to unwrap.

`cargo run —bin satisfy`

Ok just `CouldNotSatisfy`. So similar to type checking and similar to that other thing we ran into it is difficult in general to provide useful error messages if the satisfaction fails. In this case we just had a 2-of-3 multisig and only one signature so obviously that is the culprit. But you can imagine I have some complicated tree of different conjunctions and disjunctions. Something fails along the line. Is that supposed to fail? Is it supposed to succeed? Hard to say because maybe there are alternates. Maybe all the different alternates have some things that are possible and others that don’t. Maybe the user was trying to satisfy one branch but they screwed up and almost satisfied another branch. How can the satisfier tell which one was intended? Again I don’t know, these are difficult user experience questions.

Q - You could dump out everything?

A - The problem with dumping out everything is that you get this combinatorial explosion of what everything might mean. One thing I could do is dump every single key and say these keys have signatures, these keys don’t. These hashes have preimages, these hashes don’t. These timelocks are satisfied. That would definitely be more useful than outputting `CouldNotSatisfy`. In general there are combinatorially different branches so it can’t really tell what the intended choice was on every IF statement.

We are at 12:30 and I did at least touch on everything I wanted to touch on. I’ll open the floor to questions or we could do other stuff if you guys want to.

# Q & A

Q - Does this allow you to evaluate the impact of new opcodes? You could implement it in Miniscript and look at how it…?

A - Yes absolutely. If somebody were to implement a new opcode, a new AND or OR construction that is added to Miniscript Pieter and I would run through the first 100 billion Scripts and look at how they compiled this new opcode and how they didn’t. If there was a change, that’s great, that’s a valuable opcode for efficiency reasons even for no other reason, if not maybe that’s telling. We did that actually with a lot of the Miniscript fragments. We would add them and then run the compiler 100 billion times and see whether it actually impacted anything. We found in a few cases that we had fragments that we’d come up with that we thought would be more efficient but turned out never to be. When the compiler showed it never was we did some harder analysis to actually convince ourselves that it wasn’t. We were able to shrink the language quite a bit by doing that and come to the current language. If we added a new opcode and it gave us something new that wasn’t a signature, hash or timelock that would obviously be purely additive functionality. There’s not really anything more we could say other than that.

Q - Could it break Miniscript and make it much harder to implement?

A - Could a new opcode break it?

Q - Only if you use it.

A - By being so valuable that we’d want to use it and then finding that everywhere we tried to had some sort of malleability problem or something silly like that.

Q - There are tonnes of opcodes that we don’t use in Miniscript.

A - A lot of them we really wanted to. OP_ROT as far as I know no one has ever used it. It just rotates the top three stack elements. If it rotated in the other direction than what it does we could use it but it doesn’t. PICK and ROLL, there are a couple of opcodes that we really put a lot of effort into using but couldn’t find an excuse. In essence we learned that a lot of the existing opcodes are not valuable.

Q - Are there any plans to change the Bitcoin virtual machine, remove opcodes or make them more safe?

A - Probably not. If we were to change Bitcoin Script we would definitely use Miniscript to inform the way we think about this, how we think about malleability, where does the existing Script system cause pain for us unnecessarily? The specific design of Miniscript has a lot of weird quirks that are caused by the existing Bitcoin Script. Trying to make Script more directly map to Miniscript is not quite solving the right problem. What we really want is having a Script that maps to a variant of Miniscript that is basically like the Policy language. There are still questions like do we want all the different ORs and ANDs? Do we want an OR where you have to try to fail to satisfy both things where one of them succeeds as well as an OR where you completely skip over something? Do we want both of those necessarily? I don’t know. Pieter and I always go down this rabbit hole and we don’t find any end. My feeling is no. You can learn a lot about how to improve Script but we can’t learn enough that we can actually come up with a proposal that would be complete. We decided in the Taproot, Tapscript design to make almost no changes to Script. The only big thing we did was get rid of CHECKMULTISIG, that does dumb things.

Q - There wasn’t a laundry list of opcodes that you could get rid of in Tapscript?

A - Yes but we didn’t. They aren’t useful for Miniscript but maybe they are useful for something else. We just decided not to.

Q - Maybe they are objectively bad in some sense.

Q - All the objectively bad ones have been removed?

A - I think so yeah. There was some [quadratic delay](https://bitslog.com/2017/04/17/new-quadratic-delays-in-bitcoin-scripts/) that Sergio found, an OP_IF or something. We can’t get rid of OP_IF, we have to keep that one. I don’t think there are any objectively bad ones that we don’t use that we could drop that are still around.

Q - Would Policy language be compatible with something like Simplicity?

A - Yes you could write a Policy in Simplicity.

Q - If you do have these existing Policy languages out there you can switch the compiler back basically and it compiles?

A - Yes and you can even lift from the Simplicity back to your Policy and convince yourself that the Bitcoin Script and Simplicity script are the same. It just occurred to me now that I should definitely implement that.

Q - One interesting thing that Miniscript also takes care of very well is the number encoding. Numbers are encoded in Little Endian in Bitcoin Script. You can try to build your Script itself, it is like a nice foot gun. You just write your number there, the four bytes in Big Endian but actually it is Little Endian for the Bitcoin interpreter and Miniscript takes care of it.

A - Yes I’ve been burned by this a few times. Although it is supposed to also check the range… right now I haven’t implemented that which is a pretty serious bug.

Q - Have you implemented the finalizer yet?

A - Still no. I had a dream, not a literal dream. I was going to get all these pubkeys and build a giant Policy with all of our pubkeys in it somehow. I’d compile that down and then we’d all exchange PSBTs and build a whole transaction on testnet. I’m glad I didn’t attempt to do that. The reason I didn’t is that I’d have to write a bunch of infrastructure to collect public keys, to collect signatures, to collect PSBTs, to parse and validate those. It quickly became a much much larger thing and clearly I wouldn’t have had time so I would’ve felt silly. I still don’t have a PSBT finalizer.

Q - Can you explain what that is?

A - So PSBT is a way for people participating in a transaction to attach data, they basically hang data off the transaction. The finalizer takes all the data, all the signatures, all the hash preimages when it supports that, the timelock data. The finalizer actually builds a witness, an optimal witness out of all the available data and creates a valid transaction. The way a finalizer would work is PSBT. You literally take the unsigned transaction on a PSBT, you iterate through all the inputs, you take all the data out of the PSBT. Actually the way I would do it is implement this satisfier trait. For every input I would call `descriptor.satify`. It would be a trick of lifting the descriptor out of the transaction, I would need a recognize it was hashes or Script hashes. I pull every descriptor out of the transaction. I call `satisfy` passing it a transaction input, the appropriate descriptor and… Then it would parse a PSBT.

Q - You’re 18 months into this project and you still haven’t achieved your original goal?

A - That is correct. If you were at the [Bitcoin Developer meetup](https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/) you know some of the reasons why this is the case. A lot of cool things popped up and a lot of things became difficult.

Q - You said somewhere maybe on a podcast that Miniscript was a rare example of something that you’d completed.

A - Right so there is a goal that we did complete. We did not complete the original goal of writing a finalizer. We absolutely have a complete language that can parse Scripts. We ripped out half the Liquid code and replaced it with Miniscript and it was all the code that I hated. All the witness building, fee estimates and the unit tests were so bad. We accomplished that. There is a practical sense in which it is finished and I can use it for everything I want to do. I feel like the flag to really say it is finished is we have a finalizer and we have a fee estimator that’s smart. Those two things I’ve been dragging my feet on.

Q - How stable is it? Will you change it?

A - I don’t think we are going to change it. It hasn’t changed in a long time, since we added the pubkey hash. Sanket joined, he figured out that the pubkey hash was more efficient and then we kind of had an epiphany where we overhauled the whole type system. I forget how this worked originally. Now we have a mapping between every Miniscript fragment and every Script fragment. Before we had sometimes certain Miniscript fragments would correspond to different Script fragments depending on context. We had this distinction, you could still parse them. We realized this way you could actually parse Miniscripts out of Scripts without knowing the type system. This is a really cool thing. Before we required some type data to even parse. We’ve got the B, V, K, W, we used to have six types and now we have four. We came up with the type versus type modifier distinction. We separated out the correctness types, the six, from the malleability types, the three which made the website a million times simpler. We had two tables instead of one that was horrifying craziness. Now I think we are happy with it. I’m not aware of anything that it can’t do that wouldn’t require a complete overhaul.

Q - This is version 1.0?

A - I think this is 1.0. I think we are at that point. I would just finish those two auxiliary things that I said and write the README for rust-miniscript so that it would be in the rust-bitcoin organization. At some point we should move the definitions from Pieter’s personal website to something that will outlive us. I don’t think it is going to change.

Q - Additive changes maybe?

A - Maybe additive changes. It is certainly going to change for Tapscript. We’ll probably consider Miniscript Tapscript to be…. maybe we could do it purely additively.

Q - Simplicity can be used on Elements but would need a soft fork on mainchain?

A - Yes. For Bitcoin Simplicity would be like another SegWit version that completely replaces the Script interpreter.

Q - Any thoughts on whether that is viable?

A - I think it is viable. I think we have to spend at least probably several years, implementing it is pretty much done, writing tooling around it and demonstrating the value add, demonstrating we can do this kind of proofs and reasoning and that we could validate things in a reasonable amount of time. There is a lot of real world proving that we need to do. For something this big it needs to be completely deployed somewhere that is not Bitcoin for quite a while. We can’t just propose it with some pull requests and expect it to be accepted.

Q - Simplicity is a bit more powerful right?

A - Simplicity is a lot more powerful. Simplicity will let you verify any program execution no matter what the program is. It is not Turing complete but it can verify the execution of anything that is Turing complete. Whereas Miniscript is only limited to sig checks, hash checks and timelocks. In Simplicity you can do covenants say, you can do vaults which is a type of covenant where you require coins only go to a single destination where they have to sit there for a few days or go back. You can do limit orders where you have coins that are only allowed to move if a certain percentage of them go somewhere. You can have oracle inputs that specify what those percentages are, crazy things like that that Miniscript can’t even express. Even if Bitcoin Script was more powerful we couldn’t express those things as monotone functions of spending conditions. Those hash collision checks that Bitcoin Script can do but Miniscript cannot. My feeling is that if you can use Miniscript for what you’re doing you want to use Miniscript even if Simplicity is available. If you want to compile your Miniscript Policy to Simplicity but you don’t want to be using... you don’t have to. You can just do much stronger analysis much more efficiently because it is so simple.

Q - Are you targeting other blockchain backends with Miniscript or Policy language? I guess not Bitcoin derivatives necessarily.

A - The short answer is yes. The long answer is that this might be less efficient because Miniscript has so many weird warts that are Bitcoin Script specific.

Q - How easy would that be if you wanted to implement… on the EVM?

A - Probably not too bad. What you would need to do, all the Script fragments on the website you just replace it with EVM fragments. You’re going to need to rip out all the malleability types and replace it with something different. Maybe you have to replace the other types as well.

Q - It is not like with a traditional compiler you want to be composable so you can switch out whatever target architecture you have. That is still not quite there yet with Miniscript but it is something that you’re thinking about?

A - Yes. I was talking to David Vorick of Siacoin which is a blockchain that does file storage, contract verification. It checks.. and some error encoding but it has no script system. He was asking me if he could implement Miniscript directly, raw Miniscript somehow. I told him the same thing, that you could do that but you probably want to simplify it in some ways. What is cool is that if your script engine is like Miniscript it is much easier to convince yourself that the consensus code is sane versus the Bitcoin stack which is not sane.

Q - For an end user that would just use the Policy description are there any warnings, any gotchas that they should pay attention to?

A - The gotcha is that the compiler might change. Miniscript won’t ever change out from under you. The one guarantee of Miniscript is that any valid Script that is a Miniscript will always be a valid Miniscript, always with the same semantics. With the compiler, it may be that today you compile it and you get a certain Script with a corresponding address. Maybe you upgrade your compiler and get a slightly different Miniscript, we found some other optimization. I can’t promise that won’t happen. You do need to keep around the output of the compiler somewhere even if it might be difficult to recreate later. That’s the caveat, the Policy things don’t hit the blockchain and what is on the blockchain is really what ultimately matters.

Q - This is in terms of optimizations, it would be a nice surprise if it dropped.

A - It would be a nice surprise.

Q - I think Miniscript is quite high level but it is still not very accessible so I’m wondering if there is any work… I think it could be quite easy to make some nice interface.

A - Yes. Stepan (Snigirev) sadly had to do his own session but he was talking to me yesterday. He was planning to decode Miniscript off of the Scripts on his hardware wallet and then lift them to the Policy. Now you have got the tree of ANDs and ORs and display that on the screen. That is still not super user friendly but it is pretty close to directly explaining what is happening in the Script. He has a pretty big screen, he could do a graphical representation or something crazy like that.

Q - The slide you presented yesterday was delineated from the Policy….?

A - If you lift to the abstract Policy language I think that is pretty good. That is something you could probably show to an end user in a lot of cases. I guess there are still keys involved. Maybe you would have to display keys differently and say this belongs to Alice, this belongs to Bob etc.

Q - In a wallet that could be abstracted?

A - Yes. In the wallet it would be abstracted. But you’re right Miniscript itself is not something that you would show to the end user.

Q - Is there a place for resources for learning about the compiler?

A - There is [Pieter’s website](http://bitcoin.sipa.be/miniscript/) of course which describes the whole language. The [rust-miniscript repo](https://github.com/apoelstra/rust-miniscript), first off rust-miniscript has some documentation. It is not great but it is not zero either. In the source code I have an [examples directory](https://github.com/apoelstra/rust-miniscript/tree/master/examples) with a couple of examples of how to use the library. Here is the HTLC thing. Here are some examples for how to use the API. We don’t yet have a good starter from zero, here’s what a Miniscript is, here’s how we do common tasks. You probably want to go to the examples library of rust-miniscript. That is probably the closest thing. We will probably write a blog post or just some better introduction documentation.

Q - You were talking about a BIP the other day?

A - A BIP would be less helpful than documentation.

Q - A BIP would just be Pieter’s website.

A - It would literally be Pieter’s website.

Q - It wouldn’t help you with getting started.

A - We should and we will write a getting started guide.

Q - Does Pieter’s repo have documentation?

A - No it has way less.

This workshop was really helpful for me seeing how to explain from a starting point what sort of things go wrong and what kind of questions people have. This was really helpful for me in figuring that out.

Q - And we found two bugs.

A - Yes and we found two bugs.


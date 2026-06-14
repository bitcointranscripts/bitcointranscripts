---
title: 'Unlocking Expressivity with OP_CAT'
transcript_by: '0tuedon via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=mztdh1J6Lpc'
date: '2024-08-28'
tags:
  - 'op-cat'
  - 'covenants'
  - 'vaults'
  - 'op-checksigfromstack'
  - 'simplicity'
speakers:
  - 'Andrew Poelstra'
  - 'Brandon Black'
  - 'Tyler Whittle'
  - 'Lisa Neigut'
categories:
  - 'Soft Forks'
  - 'Scripts and Addresses'
  - 'Security Enhancements'
source_file: 'https://www.youtube.com/watch?v=mztdh1J6Lpc'
summary: "At Bitcoin 2024 in Nashville, Andrew Poelstra (Blockstream Research), Brandon Black (Swan), and Tyler Whittle (Taproot Wizards) join moderator Lisa Neigut (Base58) to unpack OP_CAT, a soft fork proposal that restores a disabled opcode for concatenating two items on the stack. Because Bitcoin Script operations are reversible during verification, OP_CAT can also be used to split apart and un-hash data. Combined with OP_CHECKSIG, which already hashes the entire spending transaction to check a signature, this lets a script recover its own transaction data and constrain how coins can be spent next - the basic mechanism behind covenants. The panel also explains how OP_CAT enables Merkle-tree lookup tables, letting scripts emulate arbitrary computations such as multiplication by exhaustively tabulating every input/output pair, without needing dedicated opcodes for each operation.\n\nThe panelists walk through concrete use cases: exchange payment pools that let each withdrawing user pick their own feerate, and vaults that give holders a time-delayed window to cancel a transaction if their keys are ever stolen, trading proactive security for reactive security. Much of the discussion frames OP_CAT through harm reduction - because it is a small, broadly (if inefficiently) useful primitive rather than a purpose-built covenant opcode, it doesn't foreclose future, more specific soft forks such as OP_VAULT, and its expressivity is largely unavoidable anyway since other low-level opcodes could emulate it. The panel flags OP_CHECKSIGFROMSTACK as the natural fast-follow needed to unlock rebindable Lightning channels, and pushes back on fears that this added expressivity turns Bitcoin into Ethereum, noting that Bitcoin's UTXO model, block timing, and lack of global state remain unchanged."
---

## Introduction and Panelist Introductions

**Lisa Neigut:** 00:00:00

Should we go ahead and get started?
Hey, good morning everyone! Welcome to, I guess, I think we're the first panel on the open source stage today.
Today we're going to be talking about OP_CAT, which is an opcode proposal for Bitcoin.
I'm niftynei, I'll be moderating the panel today.
I'm the founder of Base58, which is a Bitcoin developer education project.
I'm here today with Tyler Whittle of Taproot Wizards, Brandon Black, also known as reardencode from Swan, and Andrew Poelstra of Blockstream Research.
So before we get started, I'm going to have each of our panelists kind of tell us a little bit about themselves and where they were when they first heard about OP_CAT.
But before we get started, I'd love it if you could raise your hand if you've heard of OP_CAT before, just to kind of get, oh wow, okay.
So speaking to a very knowledgeable audience here, great.
Well, Andrew, do you want to kick it off for us?
Maybe tell us a little bit about what you do at Blockstream Research, and where were you when you first heard about OP_CAT?

**Andrew Poelstra:** 00:01:02

Sure, so yeah, my name is Andrew Poelstra, the director of Blockstream Research, where we work on a couple things.
We work on cryptography, we work on multi-signatures, MuSig2 was something we worked on, FROST, things like that, adapter signatures, all sorts of fun crypto stuff.
We also work on scripting.
We have a programming language called Simplicity that we've been developing, which is a blockchain language which is designed for formal verification.
The other thing that I did, this may be more relevant to this panel, is that I wrote a blog post a couple years ago about how you can use OP_CAT to simulate, or not just simulate, to actually get covenants to simulate transaction introspection and to access transaction data just by combining OP_CAT and Schnorr signatures in a kind of abusive way.
So, and when I first heard of OP_CAT, I don't know, it was probably 2013 or 2014 on Bitcoin talk forums when we were discussing all the disabled opcodes and thinking which ones would be nice to have back.
Of the ones that were disabled, I think Cat was the obvious, the best one.
It got you the most bang for the buck out of all the ones that were disabled.
They're all pretty similar in complexity, all very low complexity.
But Cat did the most stuff, is our feeling.

**Brandon Black:** 00:02:18

Hi, I'm Brandon Black.
I work at Swan on our self-custody vault, which I think is a cool product, so check it out.
In my free-ish time, I work on covenant proposals for Bitcoin.
My story about learning about OP_CAT was that a bunch of us misread his blog post.
And so we thought Cat was like the destroyer of worlds, because it could do magical anything.
It was fortunate that Rijndael, Tyler's coworker, went and actually read his blog post carefully and then tried to do it.
So now we know that Cat is not the destroyer of worlds, although it is still pretty cool.

**Tyler Whittle:** 00:02:53

Hey, everyone.
I'm Tyler Whittle.
I am the head of product at Taproot Wizards.

## OP_CAT and the Power of Covenants

**Tyler Whittle:** 00:02:58

The first time I heard about OP_CAT was when I was reading programming Bitcoin and Jimmy Song told me it was gone forever.
But the second time I heard about it was at the Stanford Blockchain Conference last fall.
And Sam Parker told me we can do OP_CAT.
With just OP_CAT, we were going to do ZK proofs.
And Udi and I laughed at him and said, that's ridiculous.
And here we are today, Waking showing us that we can do that.
So we've come a long way.

**Lisa Neigut:** 00:03:31

That was just about a year ago, right?

**Tyler Whittle:** 00:03:32

Yeah, just about a year ago.

**Lisa Neigut:** 00:03:33

So it's cool that it went from you guys talking about a little over a year ago to now almost everyone in the audience has at least heard of this proposal.
So that's pretty good marketing on someone's part, I think.
So we've talked about, okay, so we've talked about OP_CAT.
I've heard the word Covenant mentioned a few times.
Maybe we could take a few minutes to maybe explain what it does or why this is a proposal that everyone's kind of excited about getting back in.
What's the energy around it?
Tyler, do you want to start?

**Tyler Whittle:** 00:04:00

Sure.
There's a great song.
I recommend everyone go listen to it.
It sings, it's like, O-P-Cat, we want to bring you back.
Two datasets are elements, put it back into the stack.
No, that's what OP_CAT does.
It takes two elements off the stack, smashes them together, and puts them back on.
But I'll defer to my more senior colleagues here to explain how covenants actually work.

**Brandon Black:** 00:04:30

So I'll take the next stab at this.
So don't sing it, but OP_CAT, yeah, puts things together on the stack.
And one thing that's really weird about Bitcoin is that because Bitcoin script is a verification language, any opcode can be run forwards or backwards.
And because of that, you can also take things apart on the stack.
And that's pretty cool.
And then Bitcoin Script already has the ability to hash things.
But because you can go backwards, that means with OP_CAT, you can unconnect things and you can unhash things now.
And then there's one more trick, which is Andrew's trick, which you can use to turn that all into a way to look at the insides of a transaction once you can take things apart and unhash them.
So that's kind of how OP_CAT works, and it's how we get to look inside transactions.
But I want to say one last thing before I pass it over, which is that OP_CAT is also just useful because of the one thing it does, which is put stuff together on the stack.
For example, you can create bonded addresses where they can only be spent once, and if someone tries to double use them, they give away their secret keys using OP_CAT, just because it can take the two parts of a signature and split them apart on the stack.
So we focus a lot on Covenant talking about OP_CAT, but it's also just useful because it puts things together and takes them apart on the stack?

**Andrew Poelstra:** 00:05:48

Yeah, that's a great answer.
That's a great kind of prelude, right?
That's kind of a disconnect between cat is super simple.
It just puts things together, right?

## The Magic of Covenants in Bitcoin Script

**Andrew Poelstra:** 00:05:56

And all of the power that we get.
And the reason is that because in Bitcoin script you're verifying stuff, you can kind of run stuff backwards.
So all of the magic in covenants that we get from Cat, the ability to introspect your transaction and constrain where your coins are going, which is what a covenant is, really the magic is in the existing OP_CHECKSIG opcode, where the OP_CHECKSIG opcode takes three things, right?
It takes a public key, it takes a signature, and it also takes your entire transaction, which it hashes up, and then it checks that there is a valid signature with the given public key on all the transaction data.
And so by running stuff backwards, so to speak, if you can somehow recreate what the OP_CHECKSIG opcode is doing and then figure out its inputs, you can extract, while the public key and signature are not so interesting, but you can extract the transaction data itself from OP_CHECKSIG.
So what Cat gives us is just this tiny bit of extra computational expressivity that allow us to then run the OP_CHECKSIG opcode backwards and get all of the signed transaction data out of there.
And that's what Cat is doing.
When people talk about covenants using cat, that's really what we're doing.
Like, the magic is not in cat.
The magic is in OP_CHECKSIG.
Now, there is some magic in cat, right?
Just concatenating things is pretty cool.
That's what it stands for, concatenation.
You can do Merkle tree lookups.
So you can have a giant tree, basically a lookup table, but a lookup table of millions or billions of elements.
And you put them into the structure called a Merkle tree, where you take all of your individual entries in the lookup table, you hash each one of them, you pair up the hashes, and you hash the pairs of hashes.
And now you have half as many, right?
And you repeat that, you have half as many, you repeat that a few times, eventually you have one hash called the Merkle root, and then it turns out by just selectively revealing a small number of those hashes, you can show that anything you want is in the lookup table, which in turn means, And where cat is used, right, is you're hashing two things together, right?
You take your two hashes, you cat them together, you hash it.
That's how you go down the table.
Then you can really do any computation you want.
You just do the computation for every possible input.
So for a simple function like multiplying two numbers, and you just go through every single 16-bit or 32-bit number, multiply all of them, create this massive table with 2 to the 64 entries, and using OP_CAT, you can do a 2 to the 64-bit lookup, and now you don't even need OP_MUL, right?
Or you don't need Op, you know, multiply in a particular finite field, or OP_FOURIER_TRANSFORM, or whatever weird computation you want to do, if you can exhaustively compute it for every possible input, and you can sometimes, then Cat will let you do it on Bitcoin.

**Tyler Whittle:** 00:08:27

Maybe just bring it back up to a higher level real fast.
Who knows what a covenant is in the audience?
Oh, wow, we're pretty good on covenants.

## Introduction to Covenants in Bitcoin

**Brandon Black:** 00:08:38

Come to my talk later to learn more.

**Tyler Whittle:** 00:08:41

For those who don't just really quickly, a covenant is a way to restrict the future flow of Bitcoin.
So for instance, today, if I send some Bitcoin to Nifty, she can do pretty much whatever she wants with it.
With OP_CAT, we can start doing things like, I could send Bitcoin to Nifty and say, Nifty is only allowed to send that Bitcoin to Brandon or Andrew.
So that's an example of a covenant.
It's something we don't have in Bitcoin today, by and large, that we would like to add in the future because it gets us a lot more functionality and quite honestly I think it really helps improve the store of value use case for Bitcoin.
But I'll pause there.

**Lisa Neigut:** 00:09:23

Yeah, I think that's a great maybe place to take our conversation next is like so we can get all this really interesting stuff like maybe we can do a multiplication now using OP_CAT.
We don't actually have to have an opcode for multiplication, etc.
Which is really fun and exciting I think from like a developer perspective because now we can write more interesting complex contracts than we are currently.
But if we take it up to like the user level, like what is someone who's holding Bitcoin and using Bitcoin?
Like what does OP_CAT mean for like just you know, an average Bitcoin hodler or user of Bitcoin?

**Tyler Whittle:** 00:10:08

Hello?

**Brandon Black:** 00:10:11

I'm saying I think what OP_CAT or any of this does is makes it so we have more freedom in how we use Bitcoin.
Right now, Bitcoin script is kind of actively making it difficult to do things with your Bitcoin that you might want to do, like controlling where it might get spent next under certain conditions.
And so really, OP_CAT is about freedom.

**Andrew Poelstra:** 00:10:33

Yeah, so for the most part, ordinary users don't see Cat.
It's wallet developers who see Cat.
But I guess one specific application that I can think of, which I think Jeremy Rubin came up with, is this concept called payment pools, where if you're an exchange or something that has 1, 000 withdrawals to process, then currently the exchange has to just create a giant transaction with 1, 000 outputs on it.
And the exchange has to choose a fee rate that's going to make all of its users happy.
And the thing is, the fee rate's never going to be high enough for the user who wants their coins immediately.
And it's always going to be higher than most users who aren't too concerned about getting their coins immediately.
Maybe they're willing to wait overnight or something like that.
And the exchange has to pay it.
And it's not really in the exchange's interest to be paying this fee anyway because it's giving the coins to the users.
So with OP_CAT, or with Covenants more generally, one thing you could do is have the exchange send coins to a single Bitcoin output, a pretty small transaction, and that output constrains so that Each user who has coins in their output is able to withdraw their coins and put the rest of the coins back.

## Flexibility in Fee Rates and Vaults

**Andrew Poelstra:** 00:11:35

And then they can set their own fee rate and they can get their coins at their leisure, right?
They can do it on Sunday afternoon when the fee market is pretty cheap.
They can lowball the fees and let it take a month.
You know, it doesn't matter.
The individual users get to choose that.
So then the exchange saves money, the users get more choice, and the incentives are aligned so that the people who want fast transactions are the ones who get fast transactions.

**Tyler Whittle:** 00:11:59

I think one of my favorite use cases that OP_CAT brings about are vaults.
So this is something Rijndael at Taproot Wizards, he's written the perfect vault.
But I think vaults are a really cool use case for anyone who holds Bitcoin and wants to hold it long term.
It is a way to basically give you reactive security rather than proactive security.
So if I add 10 Bitcoin today and you found my seed phrase, it's probably gone.
There's not much I can do about that.
I can fight you in the mempool and RBF it until the miners get all of it.
With something like Vaults, you actually get reactive security such that if you found my secret keys, the best you can do is spin it to a waiting area where I have 30 days to cancel this transaction and now all of a sudden it just makes it a much more compelling way for me to store my Bitcoin.
If you hold ordinals, perhaps you want to do this with your ordinals, anything on the Bitcoin network that you find valuable that you want to hold long term, OP_CAT is going to help make that more secure.

**Lisa Neigut:** 00:13:09

Cool, yeah, okay, that's really a great overview, I think, of some of the things that we're excited about for getting people for OP_CAT.
I think, like, so one of the criticisms that I've heard of OP_CAT is that, you know, you can do interesting things like vaults, or you could do something like multiplication, for example, using OP_CAT, but those are really like complicated scripts that you end up writing that end up being like sort of like an indirect way of accomplishing a similar goal if that makes sense.
So instead of having something like OP_CAT we could have more specific opcodes like an op multiply for example that would work for any number or an OP_VAULT opcode that just does the OP_VAULT thing.
Do we think that you know should we be going for this kind of, like, broad tool that can do all this magic stuff, or should we be trying to get things that actually fit these specific use cases that we're looking to accomplish?

**Andrew Poelstra:** 00:14:03

So, it's a good question, And there's always kind of a trade-off between how specific you want an opcode to be and how complicated it is, like how efficient it should be to use versus how, I guess, general a use case it serves, right?
And this has been a trade-off that's been difficult.
There's been a number of covenant proposals, right, that make this trade-off in different ways, and there's a lot of kind of bike-shedding and people disagreeing fundamentally about how much expressivity we want to get.

## The Benefits of CAT in Bitcoin

**Andrew Poelstra:** 00:14:30

And there's a fear that if we make one of these decisions, if we choose something that does something very narrow, maybe it will do like 90% of what people need it to do.
And that means that if we wanted later to do something different, if we wanted to get that extra 10%, well, getting through the consensus process and producing a new proposal and doing all of the work to get that extra 10% maybe wouldn't be worth it, right?
So there's kind of this almost animosity between different covenant proposals because there's this feeling that it's kind of winner-takes-all.
And the nice thing about Cat is that because it's so bad at all of these different hacks that we've come up with, it's not stepping on anyone's toes.
No one's going to say, like, oh, we shouldn't have real covenants.
We shouldn't have introspection because we already have Cat.
Or we shouldn't, you know, all these crazy indirect things.
If people want to do those, then I guess I'll do them with cat, and they'll be pretty inefficient and pretty awful, and that will be an argument for doing these new things.
So I would say that cat kind of hits this kind of sweet spot way outside of the design area that we are considering for covenants, where it's not even a covenant opcode, and it's not good at any of this covenant stuff.
But it's simple, it will be easy to maintain forever.
It does do a couple things really well.
If you're doing Merkle trees, probably cat, you can't do a whole lot better than just using OP_CAT and no one's gonna regret Having cat on the chain because it's this crufty thing that we later found it could do better But it turns out if we have it Well, then we can do this other stuff But it's not going to get in the way of that other stuff at least as far as the consensus process.

**Brandon Black:** 00:16:03

Yeah, I think that's a great point.
I kind of actually look at it as a stack of harm reduction.
So right now, people are pretty restricted in how they can use Bitcoin, and Cat reduces the harm that we're experiencing now with people inventing, I'm gonna be bad here, I'm gonna say people inventing things like BitVM, which are bad, OP_CAT reduces the harm of that.
And then if we add additional covenant opcodes later, we reduce the harm of OP_CAT.
So we have to pick what level of harm reduction we go for.
And that's kind of where I look at it.
OP_CAT is bad at things, but that's okay.

**Tyler Whittle:** 00:16:33

Yeah, it seems to me that OP_CAT is like the Swiss Army knife.
You know, if you want a screwdriver, a screwdriver is better, but there's a screwdriver on there that'll suffice.
You know, if you need a knife, There are many better knives, but this one is good enough.
And I think what's exciting about it is it kind of introduces this free market back into Bitcoin, right?
Where we don't have to go to bike shed about whether people want to multiply, because we'll find out very quickly, oh okay, the mempool is full of people doing lookup tables with multiplication on it, great.

## The Design Space of Opcodes in Bitcoin

**Tyler Whittle:** 00:17:09

Like, we should probably make this more efficient and bring this into Bitcoin.
And so, what I really like about OP_CAT is it opens up the design space in a way that everyone gets what they want.
And then my hope is that it makes the conversation much easier about some of these future soft forks that might be simple and quick, like many of these things in the great script restoration, fantastic.
If we see those being used all the time, then it's a really easy argument to say, hey guys, let's do the work, let's talk about this one, but it seems like it's pretty clear that there's a benefit to bringing this into Bitcoin.

**Andrew Poelstra:** 00:17:47

Let me build a little bit on Brandon's harm reduction comment.
If you look at the Bitcoin mailing list, I think six months ago there was a post by Ethan Hellman about simulating transaction introspection by using the length of ECDSA signatures to extract a few bits of entropy from the transaction context, like a couple bits at a time.
So, and aside from that, privately I had two separate people who independently came up with an idea where they could maybe emulate OP_CAT by breaking SHA-2.
So, if you think OP_CAT is bad at the things that it does, there are things in Bitcoin today that maybe could be used to do it even worse.
So, yeah, I like that.
We're gradually, you know, making things less bad.

**Lisa Neigut:** 00:18:35

So, I mean, It sounds like if we get OP_CAT, it's like a gateway drug to a lot of other opcodes after that.
I know people are talking about OP_CAT by itself.
Is there anything else that's currently on the table that people are talking about adding along with, or fast follow with OP_CAT that makes it even more powerful?
Or are most of the discussions like, we can get OP_CAT, and then maybe see where to go from there.

**Brandon Black:** 00:19:05

I think there's one thing that's really, really worth doing.
If we're going to do OP_CAT, OP_CAT alone does not let us do rebindable channels for Lightning.
I tried really hard at least and It doesn't seem to have the fundamental piece we need there.
So if we were to do OP_CAT plus OP_CHECKSIGFROMSTACK, that would be a really powerful combination for Bitcoin.
It would get us rebindable channels along with vaults, along with cat VMs, and all that kind of stuff.
So that'd be my comment there.

**Andrew Poelstra:** 00:19:34

Maybe you could do it with BitVM.
But to answer the question that was asked, instead of getting sidetracked, there's five minutes to go.
The way I see it, as far as just pure script extensions, There's OP_CAT, and then there's Rusty's great strip restoration project.
And the funny thing about cat is that it doesn't have to be cat.
We just need a little bit more expressivity in order to do all these things.
And it turns out you can emulate OP_CAT with a whole bunch of other stuff.
So if we had bitwise XOR and shift opcodes that could work on arbitrary length things, turns out you can emulate cat and you can do all this stuff.

## The Excitement of Cat in Bitcoin

**Andrew Poelstra:** 00:20:08

Or if we had a comparison opcode where you had two strings and it just decided whether they were in alphabetical order or not, and as long as it works on arbitrary length strings, or I guess up to 256 bits, you could use that to do OP_CAT and stuff, and therefore do all of these other things.
So it's a bit interesting that cat is kind of one of a large array of choices that are all kind of technically equivalent, but for whatever reason, all the excitement is around cat.
And because this is a consensus protocol, right?
Like, you want to go with this thing that, like, if that's where the excitement is, that is actually an argument that that's the way that you want to focus.

**Tyler Whittle:** 00:20:47

Yeah, I tend to agree with all that.
I think the memetics of cat have something to do with the excitement of cat, I think.
But as like, it's just funny to sit up here and observe us at a metal level from the Bitcoin and be like, we're up here.
It seems like everyone wants cat, but we're also willing to talk about how we can do this with XORs or hacking SHA to, I think, I don't know what the comment is on that, but maybe I'm gonna think on what that means for us as a Bitcoin industry.

**Lisa Neigut:** 00:21:18

Great, So it sounds like we're headed towards a future where cats might be a possible thing on Bitcoin.
Cats are cute and fluffy, but sometimes they have claws.
I feel like there's people that occasionally have pulled out some, you know, they're worried that cat is too powerful and maybe it's gotten, you know, people say, well, it's a small change, you know, it looks like a cute little cat, how much trouble could we get into?
But I have heard some people pushing back that they're worried that all this extra additional expressivity in Bitcoin will lead to unintended consequences which are unforeseeable at our current juncture.
What would you guys say to someone who's got that level of maybe reticence about this proposal?

**Brandon Black:** 00:22:05

I think a lot of the fear around OP_CAT is like, what if we turn Bitcoin into Ethereum?
And I think Bitcoin will never be Ethereum.
It will never be an account-based coin, it will never have callable contracts or global state or built-in token protocols.
And so we can we can rest pretty comfortably that adding more freedom in how people use Bitcoin is not gonna magically transmute Bitcoin into something it's not.
Bitcoin is a UTXO protocol, Bitcoin is a slow methodical every 10 minutes protocol, Bitcoin does not support other tokens, and that is something that is I think pretty basic to what Bitcoin is and is not going to change.
So letting people have more freedom is not going to break that.

**Andrew Poelstra:** 00:22:53

I would also just quickly add that we don't have a lot of different levels of how much additional freedom we can add, right?
Like, Cat is a very simple, very small bit of additional functionality.
And it turns out that just by itself, it kind of crosses the Rubicon of letting you do all of these things, right?

## The Challenges of Expressivity in Programming Languages

**Andrew Poelstra:** 00:23:09

So if you don't want Cat, and you don't want anything comparably expressive to Cat, you're limited to kind of saying, well, for every additional use case, we would need a really narrowly purposed opcode for that specific use case.
And even then, you might slip up and actually somebody like me will write a blog post showing that your crazy, super specific opcode can be abused to do cat, right?
It's just very difficult to avoid this level of expressivity without really doing nothing at all.

**Brandon Black:** 00:23:38

For example, I proved that you could use OP_VAULT, which is meant to be the very specific vault opcode, and you can use that to do recursive data carrying covenants.
So really, what he said is very true.
We are barely preventing a lot of these things as it is.
And so getting a very specific thing in is maybe impossible.

**Tyler Whittle:** 00:23:57

Yeah, my takeaway here is that I think we all seem to want covenants.
And we are all going to continue to work and scrap and find ways to do it.
So I'm excited for some degree of excitement to form around a single one.
I think cat is that thing.
And yeah, I think if you want to look into the potential downsides of cat, actually Brandon has in my opinion the best article on his Twitter that goes into the potential downsides of cat and I think does a really good job of laying out what they are and then Dismantling many of those arguments as they go Great.

**Lisa Neigut:** 00:24:43

Thank you so much y'all for your time and sharing your Experiences with OP_CAT and we've got a few minutes left Maybe as the final words you could tell people where they can find out more about you, your project, or what you've written on OP_CAT.
Cool.

**Andrew Poelstra:** 00:24:57

So I'm not on Twitter, but you can find me on GitHub.
You can see what I'm writing, or you can go on IRC on OFTC or Libera to contact me.
I have a separate project at Cat doing hand-computed cryptography, in particular checksums, Shamir secret sharing, splitting and recovery.
You can go to secretcodex32.com to download the PDF and print your own paper computers to do that.

**Brandon Black:** 00:25:20

Yeah, mostly you can find me on x at reardencode.
And I host a weekly spaces talking about tech.
We talk about all this stuff.
We spent several weeks digging into OP_CAT.
And there's still a few people out there that think you can do some really scary stuff with OP_CAT.
But I'm happy to talk about those things.
And I can go I'll kind of be Socratic to the very bottom of that.
And that's what those spaces are for.
So yeah, join me there.

**Tyler Whittle:** 00:25:48

You can find me on Twitter as well.
I'm Dr. Dow, DR underscore Dow.
And if you want to learn more about how soft forks happen in Bitcoin, I wrote a thing that looks kind of like Candyland that you

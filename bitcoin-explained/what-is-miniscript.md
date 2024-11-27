---
title: What is Miniscript
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=z84_5yhy8fs
tags:
  - bitcoin-core
  - miniscript
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2020-07-31
episode: 4
summary: The podcast episode "What is Miniscript" delves into Miniscript, a simplified version of Bitcoin Script developed by Pieter Wuille, Andrew Poelstra, and Sanket Kanjalkar from Blockstream. Miniscript is described as a template of Bitcoin Script, aimed at making it easier to write, analyze, and reason about Bitcoin smart contracts. The discussion covers the basics of Bitcoin Script, its problems such as complexity and potential for errors, and how Miniscript addresses these issues by providing a standardized way to use a subset of Bitcoin Script's functionality. The episode also introduces the concept of a policy language, a higher-level programming language that can be compiled into Miniscript, facilitating even easier script creation for developers. Additionally, the limitations of Miniscript and its place within the Bitcoin ecosystem are discussed, highlighting its role as a tool for developers rather than a consensus change.
---
Aaron van Wirdum:

Miniscript.
It's a project, I guess that's how I would describe it.
It's a project by a couple of Blockstream engineers, even though it's not an official Blockstream project, but it's Pieter Wuille, Andrew Poelstra.
And then, there was a third name that was as well-known, Sanket Kanjalkar.

Sjors Provoost:

Yeah, I believe he was an intern at Blockstream at the time.

Aaron van Wirdum:

He may have been an intern, yes.
So they developed this idea called Miniscript.
So let's just get into what it is.
Okay.
So to sort of spoil what it is a little bit before we get into that, it's sort of a simplified stripped down version of Bitcoin Script, which is the program language used in Bitcoin.
So far so good?

Sjors Provoost:

Yeah.
Or it's a template, basically.
It's a template of Bitcoin Scripts that you can use.

Aaron van Wirdum:

A template of Bitcoin Script is how you would describe it.
Okay.
So let's get started.
First things first.
scripts, Bitcoin Scripts.

## Bitcoin Script

Sjors Provoost:

I think, two episodes ago, we explained that it was actually good to add constraints to money.

Aaron van Wirdum:

Right, yes.
This was in the Taproot episode.
You explained how actually putting some restraints to money would be a good thing, in the context of Bitcoin.

Sjors Provoost:

Right.
Somebody, if you're sending me money, everybody can see the Bitcoin transaction.
So you want to make sure or in particular, I want to make sure that I'm the only one who can spend it.
So I'm telling you, make this transactions such that it can only be spent by my public key.
And the way that's done is using a script.
Even though it's a very simple script and most people use the same script, it is actually a script.

Aaron van Wirdum:

Yeah, and Script is actually a programming language.
It's a new programming language.
It was introduced in Bitcoin.
Like it didn't exist before, although it resembles something that did exist before, which is called Forth.

Sjors Provoost:

Yes.
It basically, it's pretty horrible.
I mean, it looks like it was just-

Aaron van Wirdum:

It's a horrible programming language.

Sjors Provoost:

I think so, it seems to be cobbled together as an afterthought, but I think it was only later that people realized that you can only change Bitcoin through very carefully grafted soft forks.
So you can't just say, "Oh, let's just start with a draft language," and then clean it up later.
So it's been a complete nightmare to make sure that language doesn't do anything surprising, anything bad.
So a lot of the operations that were part of the language have been removed almost immediately, because they were all sorts of ways that you could just crash a node or do other things.

Aaron van Wirdum:

Right.
These were removed early on.

Sjors Provoost:

I mean, Ethereum had a similar experience in 2015, right?
Where complex programs could do all sorts of unexpected things, but Bitcoin had that in the beginning too.

Aaron van Wirdum:

So just to remind our listeners, what kind of restrictions can they put on a transaction?
What kind of restrictions are we talking about here?

Sjors Provoost:

So the main restriction would be that only the owner of a specific public key can spend this transaction.
I think that's the typical pay to public key hash transaction.
And maybe we want to demonstrate how that works.

Aaron van Wirdum:

Go for it.

Sjors Provoost:

So, it's a stack-based language and a stack like a stack of plates.
You can put plates on it and you can take the top plate off, but generally you don't want to just take a plate out of the middle.
And this is just easy to implement as a programming language in general.
So when people make early computer processors, it was just easier to have a memory where you could only put things on top of it and take the top element off.
You didn't have addresses, like with memory, you have to say which part of the memory do you want, with a stack you just say, put something on it, take something away from it.
So the standard Bitcoin Script reads as follows, it's very beautiful.
It's `OP_DUP` as in double, duplicate, then `OP_HASH160` as in take the 160 SHA hash.
And RIPMED hash, then the public key and then `OP_EQUAL_VERIFY`.

Sjors Provoost:

So it's four elements, duplicate, hash, pubKey, and then Equal Verify.
And if you kind of walk through what that does, let see if where I have it.
So what happens when the blockchain encounters this script, it's going to be in the output of a transaction.
So the output of a transaction shows the script that it's locked with and the amount.
Now, if you want to spend that, what you do is you publish what you want to put on the stack, and then you sign it essentially.
Well, actually you just publish what you want to put on the stack.
And that probably includes a signature.
So when-

Aaron van Wirdum:

By publish, you mean generated new transaction.

Sjors Provoost:

Yeah.
So the input of your transaction.
What that actually looks like is basically, a couple of things that you're putting on the stack.
And what the Bitcoin interpreter will do is it'll see the stuff you put on the stack, and then it starts running the program from the output.
So given your stack, it starts running the program from the output.
So in this case, what you put on the stack is your signature and your public key, because the original script did not have your public key, it had the hash of your public key.
Okay.
So we start with a stack that has two plates.
Plate 1 at the bottom is your signature and on top of that is a plate with your public key.
And then the script says `OP_DUP`.
And what `OP_DUP` does is takes the top element of the stacks, takes the top plate, the public key and duplicates it.
So now you have two plates with a public key at the top of the stack.
And your signature's still at the bottom.
Then the next code, the next instruction is `OP_HASH160`.

Sjors Provoost:

So what this does is it takes the top thing from the stack, which is one of those public keys, it hashes it and then puts the hash on the stack.
So now the stack is-

Aaron van Wirdum:

Oh, you want-

Sjors Provoost:

I'm trying to interrogate you here.

Aaron van Wirdum:

Apparently.
Now the stack is a hash and the public key, I didn't keep up.

Sjors Provoost:

So, at the bottom is the six, still the signature, then there's a public key and then there's the hash of the public key, that's what's on the stack.
So the next operation is pubKeyHash.
So that is the hash of your public key again.
So now the top of the stack is two times the hash of your public key.
And then the next operation is `OP_EQUAL_VERIFY`.
So that basically takes the two things off the top of the stack says, hey, are these the same?
Yes.
So indeed, did you put the hash of your public key?
And then, the last thing that's left on the stack is only again, your signature and your public key, and it calls object six.
So it checks the signature using your public key.
And then, the stack is empty and everything is happy.
That's how the Bitcoin program is run.
And you can do arbitrarily complicated things.

Aaron van Wirdum:

I'm very happy Sjors.

Sjors Provoost:

Yeah.
You can do arbitrarily complicated things that way.

Aaron van Wirdum:

So yeah, so basically this stuff is telling your computer what to do, what to check, see if stuff matches, if it matches it's okay, if it doesn't match, it's not, depending on whether it should match or not.
And that's defined by code-

Sjors Provoost:

But notice that-

Aaron van Wirdum:

That's what we're doing here, right?

Sjors Provoost:

Yeah.
But notice that you don't have to check a signature.

Aaron van Wirdum:

Exactly.

Sjors Provoost:

You could just have a script that says, yeah, it's fine, just take it.

Aaron van Wirdum:

Yes, or you could have a script that says you either need a valid signature or you need 34 invalid signatures.

Sjors Provoost:

You can do very strange things.

Aaron van Wirdum:

You can do weird things.

Sjors Provoost:

Yes, very strange things.

Aaron van Wirdum:

Okay.
So that's kind of the point we're getting at here, I think, right?

Sjors Provoost:

Yes.

Aaron van Wirdum:

The script's language is diverse enough to allow for weird stuff.

Sjors Provoost:

Yeah.
And another question is, if you're are just sending money to yourself, you only need this very simple standard script that everybody's seen a million times.
But let's say you're collaborating, you want to do a Multisig.
Now there's actually an instruction to do Multisig, but let's say that didn't exist.
So one way you could do a Multisig is say the script we just explained with my public key in it or my public key hash.
And then, the script we just explained with your public key hash, just in sequence, right?
So that if that's executed, I will not repeat the process we just did before.
But you essentially start with those two public keys and two signatures on the stack and you run both of these scripts in sequence, and then if both people signed, it's all good.
So you have a poor man's Multisig.

## Problems associated with Bitcoin Script

Sjors Provoost:

But if I'm evil or stupid, I could make this a REKT-man, Multisig, sorry for the joke.
And that is achieved by, in the middle, inserting an op code called `OP_RETURN`.
And the `OP_RETURN` code basically says, all right, stop evaluating this program, you're done.
Now, if I had an electronic lawyer that wanted to check that this Multisig is what it says it does, or in fact, if you had that lawyer, your lawyer might say, "Well, I see that my signature's being checked and whatever the rest of the script does, I don't care, but my signature's being checked, so I'm happy with this," but of course, you shouldn't be happy with this.
So your electronic lawyer should see that `OP_RETURN` statement and warn you.
But the problem is there's a trillion ways in which scripts can go wrong and that is why you need a standardized way of dealing with these scripts.
And that's where Miniscript is-

Aaron van Wirdum:

I'll read a little fragment from Andrew Poelstra, who I interviewed a long time ago when I wrote an article on this.
So the example he gave was, and I'm not going to pretend like I understand everything he said in this quote, but that was sort of the point of the quote for me, that it was exemplifying the complexity of potential ways to mess around with script.
Anyways, so the quote was, "There are op codes of Bitcoin Script, which do really absurd things like interpret a signature as a true false value, branch on that, convert that Boolean to a number and then index into the stack and rearrange the stack based on that number.
And the specific rules for how it does this are super-nuts."
You probably actually follow that perfectly.

Sjors Provoost:

No.

Aaron van Wirdum:

I don't, oh, you don't either.

Sjors Provoost:

I kind of do, but the analogy would be, you have the stack of plates and you take a hammer and you smash one, and then you confuse two and you paint one red and then it still works, if you do it correctly.
It's completely absurd.

Aaron van Wirdum:

Or another analogy I think you gave before this recording, correct me if this is not the right way of explaining this analogy, but it's like you have a contract and it says, you're buying this house and these are all the conditions.
And then there's a small letter, which says, unless there's two commas in a row, somewhere in this contract, in which case all your base are belong to us.

Sjors Provoost:

Exactly.
Except that this will be like the law, right?
So the contract doesn't say that at all.
It's just that the law that's in this country has that stupid rule.
If there are two commas in a contract, you're giving away your money.
Okay, that's the script interpreter of all the consensus rules, which are quite complicated.

Aaron van Wirdum:

Okay.
So I think we've now broken down the problem with scripts.
It's a shitty programming language or at least it's easy to make mistakes or hide bugs in there and make all sorts of complex arrangements that people might or might not notice and then your money goes to places where you don't want it to go.
That's the summary, right?

Sjors Provoost:

Yeah.
And we've seen in other projects how bad things can go if you have a very complicated language that does things you're not completely expecting.

Aaron van Wirdum:

Are you referring to a project that rhymes on methereum?
I think we're on the same page.
Yes.
Okay, so solutions we're getting to the solution part of the story.

## How Miniscript solves Bitcoin Script's problems

Sjors Provoost:

So what you're basically doing, what Miniscript is doing is it's taking certain example scripts, so sequence of op codes, and it lists, I think about 20 of them, 20 templates.

Aaron van Wirdum:

This is Miniscript?

Sjors Provoost:

Yes.
It lists a few dozen templates.
It not use all of the available Bitcoin Script, it uses a subset of it.

Aaron van Wirdum:

Right, right.
So let's say Bitcoin Scripts has 100 tools.
I have no idea if it's-

Sjors Provoost:

Something like that.

Aaron van Wirdum:

Anyway, close to 100, I'm just throwing out a number.
The Miniscript says, okay, let's throw out 80 of these, because these are just got to cause a mess and let's keep 20, and that way it's going to be a little bit simpler for everyone.
Is that right?

Sjors Provoost:

Right.
So if Bitcoin Script uses an alphabet essentially, and Miniscript hasn't set of words.
So it's not a subset of the alphabet, but it's a subset of words.

Aaron van Wirdum:

I see.
Okay.
That's a better analogy.

Sjors Provoost:

So there's certain patterns of op codes that you're allowed to use.
And if you use those patterns in the way they describe.

Aaron van Wirdum:

So this double comma is removed now.
It's not in here anymore.

Sjors Provoost:

Yeah.
There's no double comma, or there is-

Aaron van Wirdum:

That was [crosstalk 00:12:58] anyways.

Sjors Provoost:

But it is used in a very precise way.
So basically, Miniscript.
Yeah, it removes some of the foot guns, but it also allows you to do very cool stuff safely.
In particular, it lets you do things like, AND.
So you can say condition A must be true AND condition B must be true and you can do things like, OR.
And whatever's inside the OR, or inside the AND, can be arbitrarily complex.
So with Bitcoin Script, you have if and else type of statements, but if you're not careful, those if and else statements will not do what you think they're going to do.
So with Miniscript, there is-

Aaron van Wirdum:

Because there's more complexity hidden after the IF for example.

Sjors Provoost:

Yes, exactly.
And the Miniscript basically, the templates make sure that you're only doing things that are actually like doing what you think they're doing.
So they really contain it.
And that allows you to do nice things.
So let's say you're a company and you offer semi-custodial wallet solution, where you have one of the keys of the user and the user has the other has two keys, for example.
So you're not, you don't have a majority of the keys and maybe there's a five-year timeout where you do have control in case the user dies, something like that, right?

Aaron van Wirdum:

Yeah.
Like a Multisig kind of set-up.

Sjors Provoost:

And so, normally when you set up a Multisig, the way you kind of set it up is everybody gives their key, their master key, their expo, for example, and you create a very simple script that has three keys and three people sign.
But the problem is, because you're a big business that offers a service, you have some really complicated internal accounting department and you maybe want have five different signatures by specific people in God knows what complexity, but you don't want to-

Aaron van Wirdum:

Yeah.
You have five members on the board.
You want three of them to sign.
Unless maybe the CEO.

Sjors Provoost:

And especially once we have-

Aaron van Wirdum:

Get some sort of special right from two of the board members and then-

Sjors Provoost:

And there's a code hidden in an envelope inside the nuclear suitcase that has an override.
Exactly.

Aaron van Wirdum:

Exactly.
That's like all sorts of complex stuff you can do with it.
And all the complex stuff should count as one key, like right, that's where you're getting at.
You don't really care how the complex stuff is solved.
That's up to the company.
You figure it out company.
As long as it's just clear to us that it's only one key, however you do it.

Sjors Provoost:

Exactly.
Now the problem with that is if I gave you...
You can do that with script or with Taproot, but how do I, as a customer know, I would have to hire my own electronic lawyer to check that script of yours, that it doesn't have any of these double comma, little gimmicks in it.
And if only there was a way you could check that and Miniscript is done such that you can check that as long as the script that you're getting is compatible with Miniscript, because Miniscript to normal script is two ways.
So you can take any Miniscript, turn it into a normal script.
You can take any normal script and turn it into a Miniscript.
Well, unless it doesn't match, right?
If there's codes in it that don't apply, then it just doesn't compile or doesn't translate.
So, and if you can turn something into Miniscript, then you can analyze it using all sorts of tools that can analyze any Miniscript.

Sjors Provoost:

So what you would have is every wallet out there could have a Miniscript interpreter and the interpreter could show you a little pie chart and saying, you are this one piece of the pie, and there's this other piece of the pie that is really complicated, but you don't have to worry about it.
It's not going to do anything sneaky.

Aaron van Wirdum:

Right.
That's good.

Sjors Provoost:

That's excellent.
Yeah.

Aaron van Wirdum:

One of the things that I, so, I mean, we're making a podcast, so we can't actually see show this, unfortunately, but Poelstra for example, he's drawn this out.
You can actually draw out what a contract would look like.
Apparently that's not really possible with this script.
All this was news to me when I-

Sjors Provoost:

You can, it's just this horrible manual tedious, yeah.
I mean, I imagine the people from Liquid, for example, that have a 13 of five Multisig with all sorts of fallbacks.

Aaron van Wirdum:

Okay.
So, that's probably drawn out at some point.
But with Miniscript, it's actually fairly simple to draw it out.
And you can show this to a CEO who has no idea about scripts or Miniscripts.
You can just look at the picture and figure A, yep, that's sort of what I want the blue and red squares to be.
And if these keys work out like this then seems like a good idea to me.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

So that's actually possible now.

Sjors Provoost:

Yeah.
With Miniscript, but wait, there's more.

Aaron van Wirdum:

There's more.

## Policy Language

Sjors Provoost:

And that's called the policy language.

Aaron van Wirdum:

No, I want to get to, I want to ask you something else first.
With Miniscripts, I do think there are strictly, technically speaking, there are some limitations, like there is stuff you can't do with Miniscripts, right?

Sjors Provoost:

Yes.

Aaron van Wirdum:

But as far as I understand, these are stuff, no one actually does anyways.

Sjors Provoost:

Well, that's not necessarily true.
So the thing is, but this is, we have to go to policy language before I can explain that.

Aaron van Wirdum:

Oh, we do?

Sjors Provoost:

Yes.

Aaron van Wirdum:

Because you have this in mind already.

Sjors Provoost:

So let me just quickly explain-

Aaron van Wirdum:

You got this episode planned out way better than I do.

Sjors Provoost:

Well to understand why you might want to do really complicated stuff, I need to explain what the policy language is.

Aaron van Wirdum:

Okay.
Go for it.

Sjors Provoost:

So a policy language poorly named, or maybe not poorly named is a way to express your intentions.
So for example, say I want two signatures and this can be translated or compiled, I think is the better term too Miniscript.
And the nice thing is in policy language-

Aaron van Wirdum:

So to be clear, the policy language is the stuff like if someone like you Sjors, you're building a wallet.
I don't know you're doing something on your computer, improving Bitcoin, then you're typing.
And the stuff that comes out of your fingers is policy language.
And then, you actually compile that to script later on.

Sjors Provoost:

Yeah.
I mean, you could just write the script directly or you could write the Miniscript directly, but the nice thing about writing the policy language is that you can have a compiler that can be very smart.
So a simple policy language might be just give me two of two signatures.
And the policy language would probably convert that to `OP_MULTISIG` or we'll convert that to Multisig in Miniscript and Multisig in Miniscript is just `OP_MULTISIG`.
So that's super-trivial.

Aaron van Wirdum:

Okay.
So whoever wrote the policy language, and I know Pieter Wuille, for example, wrote the policy language for this.
It was him, it was his brain basically.
He figured out all the best ways to compile this policy language into Miniscript, right?
He must have somehow figured it out then.

Sjors Provoost:

He wrote a compiler.

Aaron van Wirdum:

See, I don't know anything about this stuff.

Sjors Provoost:

That's okay.
So basically, you write a policy language, it's like a higher level programming language.
So if you have a higher level programming language like, I don't know, Basic, you can say go to five.
I don't know if you've ever worked with Basic.

Aaron van Wirdum:

Sure.
I can't code hello world.
Isn't that clear to you by now?

Sjors Provoost:

Well, I mean, hello world-

Aaron van Wirdum:

I've coded hello world once, but that's pretty much how limited I am.

Sjors Provoost:

What language did you code hello world in?

Aaron van Wirdum:

I don't remember.

Sjors Provoost:

That's amazing.
Anyway, so what happens is usually when you see a programmer looking at a screen, you see something that looks like English, with words like four and next and yada yada, but eventually the machine is just reading bits and bytes.

Aaron van Wirdum:

Sure.
No, I understand that part.

Sjors Provoost:

So the bits and bytes are very close to what Bitcoin op codes look like.
They're very low level.
They're very instructions like put this on the stack, take that away from the stack.
And the Miniscript is essentially the same.
It's just only a subset of it, but it's slightly more readable, but it's still extremely low level.
The policy language is slightly higher level.
So what you do is you start at the higher level, which is easier for a programmer to write and then a computer looks at that high level language and says how can I write this into low level machine readable stuff as efficiently as possible?
So in the case of the Multisig thing, I might say, I just want two out of two signatures.
I don't care how you do that.
Then the compiler knows that there are multiple ways to do that.

Aaron van Wirdum:

But how does compiler know this?
I hope there's listeners out there that knows little about this as I do.
So they might learn something.
How does the compiler know this?

Sjors Provoost:

So disclaimer, I don't think I've ever written a compiler.
I'm not that cool.
But generally compilers know, because somebody wrote the compiler.

Aaron van Wirdum:

Well, but that was my point.
It must have come from Pieter Wuille's brain in this case.

Sjors Provoost:

Of course.
Everything comes out of Pieter Wuille's brain.

Aaron van Wirdum:

And there we go.

Sjors Provoost:

But basically, the compiler knows, okay, there's maybe two or three ways to do this, this to execute his intention.
And then, the question is, which of the three of them am I going to pick?
Well, then it depends on the transaction weight and the fees that you might be involved, but also you can tell it, okay.
I think most of the time it's condition A, but only 10% of the time it's condition B.
And then the compiler can try condition A nine times, condition B nine one time and then figure out what the expected fee is.
So it can optimize for typical use cases, worst case scenarios, all these things, and it can then spit out a Bitcoin Script or a Miniscript that then becomes a Bitcoin Script.

Aaron van Wirdum:

Yes.
The compiler figures out the best way to do something.

Sjors Provoost:

And in very practical terms, another thing it could do, I don't know if it can already do that is you have SegWit scripts now, but we'll have hopefully half Taproot, which can put things in a Merkle tree.
So your compiler could figure out where to put stuff in the Merkle tree.
You don't have to worry about how to build the Merkle tree.

Aaron van Wirdum:

Right, yes.

Sjors Provoost:

So it can do all sorts of things.
So you started the policy language and then you write Miniscript and that goes into whatever-

Aaron van Wirdum:

Okay.
So that's what a compiler is.
A policy language you use, you put it into the compiler and then Miniscripts comes out of it, which is in a way script.

Sjors Provoost:

Yes.
I think the technical term for going from Miniscript to script is trans-piling, which basically is like a one-on-one thing you can do in two directions.
So you can go from Miniscript to script, from script to Miniscript, but you cannot go back to a policy language.
Well, you can guess the policy language.

## Miniscript Limitations

Aaron van Wirdum:

You can.
Yeah, I guess so.
Yes.
I understand that.
And then getting back to, are we ready to go back to my question about limitations?

Sjors Provoost:

Absolutely.

Aaron van Wirdum:

So now there are some limitations when you're using, I guess, this policy language or Miniscripts in general.
But these are limitations that no one actually suffers from is, is how I understood it.

Sjors Provoost:

Not necessarily.
I mean, ideally yes, but in practice, some scripts are, some policies might be very complicated and there would be infinite ways to execute these in Bitcoin Scripts.
And because of all these weird double comma foot guns that are in Bitcoin Script, sometimes that's an advantage.
Sometimes you can write something really efficiently in Bitcoin Script, that is just really horrible, if you objectively look at it, but it is really fast or really fee-efficient.
And in fact, I believe Lightning uses that the way they sometimes deal with time locks or with hashes or nonces.
There's some tricks in Lightning I believe that you cannot do a Miniscript or at least you could not do a Miniscript, maybe you can now.
So there are some optimizations where like what Poelstra said, "Oh, you do some weird switching of the stack and you interpret things, not the way they were," you put a public key on it, but you interpret it as a number, those kind of weird tricks.

Sjors Provoost:

Those might be very hard to reason about, but a human might be able to do it, but the Miniscript compiler would not do it, which means you end up with longer, potentially longer Lightning scripts, if you do not have all the whistles and bells in it.
So it's possible that Miniscript would be expanded if there is some other optimal way to do it.
But you have to be careful, because if you...
You really want to make sure there's nothing in Miniscript that brings back those scary properties of the underlying language.

Aaron van Wirdum:

Well, and to be clear, in cases, this isn't clear to anyone, Miniscripts is an addition to what there is already, like script is going nowhere, Bitcoin still use script, and that's the way it's going to be.
It's just, this is an extra tool for people who want to use that.

Sjors Provoost:

And in fact, it's not a consensus change at all.

Aaron van Wirdum:

No, it's nothing in that.

Sjors Provoost:

It's a tool that you can use or not use.
Don't worry.
It's not Blockstream dominating the scripts here.

Aaron van Wirdum:

Okay.
So we mentioned Pieter Wuille has this policy language.
I know this is very fresh and you probably haven't looked at it very much, but [inaudible 00:25:22] also wrote a policy language, you haven't studied that yet, I think not.

Sjors Provoost:

I have not yet.
So I thought that would be a cliffhanger.

Aaron van Wirdum:

That would be a cliffhanger, you like the cliffhanger.
So that will be a cliffhanger for another episode.

Sjors Provoost:

Or never.

Aaron van Wirdum:

Or maybe we will have the one of those [inaudible 00:25:36].

Sjors Provoost:

But I can tell you from what I know about the policy language is that you're still some steps away from having a practical tool where you and I can set up a very complicated Multisig wallet.
There's all sorts of questions you want to answer like, how exactly do you do this setup?
What are you emailing to each other?
Are you emailing your keys or are you emailing something a little bit more abstract that you agree on first and then you exchange keys?
Those very practical things that are not solved inside a Miniscript.

Aaron van Wirdum:

Let me at least mention it's called Minsc.
So it's policy language, it's called Minsc.
Okay, I'm afraid we can't give you any more info about Minsc yet.

Sjors Provoost:

Well, I know Minsk with a K is a city.

Aaron van Wirdum:

Maybe one day.

Sjors Provoost:

I think it's with a C.

Aaron van Wirdum:

Minsc with a C.
Yeah, that's some extra info.
All right, Sjors, is this the end of our episode?
Did we cover everything we needed to cover from Miniscripts?

Sjors Provoost:

I hope so.

Aaron van Wirdum:

It was maybe slightly messy.
So let's sum it up.
Miniscripts is a subsection.
No, you called it a template.

Sjors Provoost:

Yes.
It's a template of script pieces.

Aaron van Wirdum:

Even this summary is getting messy now.

Sjors Provoost:

So basically, Bitcoin Script is like an alphabet essentially, just different letters that have different meanings.
And you could see Miniscript is a set of words.
Not really words, because you can put things between the words, but maybe words and brackets and commas.
That's what Miniscript is.
And then the policy language is the thing that can be converted to Miniscript.
It's a bit more high level.

Aaron van Wirdum:

And there are several of those apparently by now.

Sjors Provoost:

Yes, because yeah, exactly, because Miniscript, it has to be set in stone, I guess sort of, because you want to do all the safety checks on it, but then just like you can have different programming language, you can have different policy languages.

Aaron van Wirdum:

Yes.
So if you're into Bitcoin programming, this is what you want to study.
This what you want to look at.

Sjors Provoost:

If you're into Bitcoin programming the rabbit hole is massive and pick something.
There's a talk by Andrew Poelstra.

Aaron van Wirdum:

That is probably pretty good though, right?

Sjors Provoost:

Yeah.
But so there's a talk by Andrew Poelstra from Advancing Bitcoin, not the conference, but the meet up before it, the BitDevs London, where he talks for two hours about all the problems with regular script and why he hates things.
And that's just, he said he was going to do it in 20 minutes and I think he still didn't cover everything.
I don't think that's the best place to start.

Aaron van Wirdum:

He's still on stage.

Sjors Provoost:

He's still on stage out there just going through it.

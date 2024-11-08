---
title: Everything Is Broken
transcript_by: Bryan Bishop
speakers:
  - Cory Fields
---
This is a clickbaity title, I realize. But the reason I say it is because it's become a mantra for at least myself but for the people who hear me banging my hands on the desk all the time. I am Cory Fields and I work here at the MIT DCI. I am also a Bitcoin Core developer. I am less active these days there because I have been spending some time looking at some higher layer stuff.

"Everything is broken" to me is a sentiment that most bitcoin developers feel to some extent. When talking with Michael recently, he was saying yeah of course everything is broken.

# Disclaimer

I want to give a quick disclaimer. I will be speaking ill of some things and development processes. I am not trying to say that Bitcoin Core does not work well, but I think it's state of the art and goes to extreme length to do things as safely and securely and non-broken as possible. But I want to talk about how bad the state of development is for insanely secure software.

# How might bitcoin die?

A few years ago at the MIT bitcoin club, I was asked how bitcoin might die. There's a few common answers, like 51% attacks, protocol flaws like SHA256 or ECDSA being broken, or maybe government intervention or bitcoin scripts that could mint unlimited amounts of money. What happens if China decides they are really really done with all the bitcoin? My answer though is that the most likely sudden death scenario for a cryptocurrency like bitcoin is an accidental bug that gets introduced internal to the system.

# Two really nasty bugs as motivation

The reason I say that, and I think Ethan is going to go into this into more detail later, and I have been involved in these really nasty bugs and so have others in this room. I am not going to go into the specifics of them; but I think both of these bugs in 2018 had the potential to bring down these respective currencies. There was a Bitcoin Cash bug that I found and disclosed and it kicked off a discussion about responsible disclosure in these systems and how to do it generally. I was a little smug for a few months until we were effected by a similar bug in Bitcoin Core which potentially would allow for money printing out of thin air. It really, it's really important to step back and ask number one how do these things happen but how do we prevent them in the future?

# Bitcoin inherits all bugs in the stack

This illustrates why everything is broken. Bitcoin developers and developers of other critical pieces of software don't just get to deal with the code you're looking at. When you review a pull request for Bitcoin Core, it's not just the C++ code alone you have to consider. There's nothing in isolation in the system and it's terrifying.

There are dependencies, like openssl. Bitcoin Core depends on openssl and this has bit us in the ass in the past. There was a potential fork and we came together quickly to mitigate it, but that was a potential bitcoin doomsday scenario simply by the fact that we were relying on openssl.

We have seen bugs in libc/libstdc++ implementation, or threading issues-- we couldn't migrate from one version of C++98 to C++11 because of some issues there. There's also compiler bugs: Bitcoin Core has exposed miscompilation bugs in gcc. You have perfectly valid C++/C code and it turns into assembly that doesn't do what you think it's going to do.

We have had kernel bugs like socket allocation and socket reuse; CPU bugs like Spectre and Meltdown and we have to consider the sidechannels and be very mindful of the way we develop around all of these issues. There's also random entropy source issues. It's an ongoing question.

When you want to put a substantial change into Bitcoin Core, this is the stack of questions we have to look at it. It's daunting at times because especially for developers-- some developers know code really well, but have no idea how a compiler works. It requires a lot of collaboration to try to get a lot of this stuff right.

# Bitcoin requires better

I think this illustrates the exact problem when I say software development in general is broken. This is "goto fail", it was an iOS bug a few years ago. You can look at the code, and with or without the highlight it's not hard at all to see what went wrong here. But I would argue that the developer that wrote this didn't make a mistake. I don't think it's a developer bug. Instead, the system let down the developer. In every way, this code should not have been able to ship. It should have been caught by  a linter, the compiler should have complained, a reviewer should have complained. I would go further and say, this code should not be allowed to-- - this code should not exist and should not be allowed to exist.

# Mozilla and Rust

Rust is a drum that I have been banging a whole lot lately. In a lot of ways, rust feels like a solution to a lot of these problems. It's architectured in a way that learns from the past, and it's new and better. But I want to focus on rust the idea.

For those who aren't familiar, Rust is a programming language that came out of-- it was started by some Mozilla developers 12-13 years ago. Around 10 years ago, it became an official Mozilla project. Recall that the internet 10-15 years ago was a buggy crashy place, and that's not to say it's not like that anymore, but it was worse back then. As a developer, you get tired of chasing a null pointer dereference all day every day, or track down your data races.

I think what's interesting about rust is that the Mozilla Foundation and the people involved had the idea to say, well we're working on this stuff and fixing it now, but let's look way out and see how can we avoid these issues completely.

# The 10 year project

The bug I highlighted previously is not possible in rust. Everyone in this room knows why goto is so scary. It's not robust. You can say it's useful, but you can't say it's robust. I am of the opinion that we're at a critical moment where we have this ability to look at bitcoin and bitcoin development like Mozilla looked at Firefox and said well we're chasing the same bugs and the same problems all the time-- what's our 10 year solution to these problems? What's the way out of these problems? We can add more people, but again adding more developers does not make better faster code. It's just not how it works. It's a matter of improving the tooling and the language.

I think of this as a spectrum-- on one side you have general and on the other side now we have ASICs and custom mining hardware and hardware wallets. Will we ever run Bitcoin Core or whatever the bitcoin software is, on a dedicated piece of hardware where only htat hardware will run the consensus algorithm? I think that's absurd, but I think it's interesting to consider. Does it make sense to push in that direction? Should we push towards more custom more domain specific so that we can guarantee--- general purpose code and general purpose hardware have tradeoffs that we don't want to trade with.

# Next steps: The rustening is happening

Rust is a cool language, and it's not surprising to me that bitcoin developers have shifted somewhat to primarily working with rust. This is because rust is a language that provides certain guarantees that C++ doesn't. Bitcoin Core is currently written in C++. It's important to look way way forward and see how can we move away from some of these problems. Also, let's use the 10 year foresight that Mozilla has put in place--- they have solved many of these problems for the rest of us.

There's currently a pull request from Jeremy Rubin for getting rust code into Bitcoin Core. The idea is that, Matt has written a whole lot of things to try to take advantage of this. The idea is that if there are segments of code, new code that we can add that is sandboxable from the C++ code, then why not start with something that gives us better guarantees? There are technical problems with this, and social problems with this, but I think it's clear that this is the direction that things are going.

I think this discussion is going to be kicked off very soon, as far as what the directions are, and there's a lot of open questions about what rust and bitcoin would look like together.

# Let's fix what's broken

This is a very condensed version of my overall rant. There's a much longer one that is essentially that the idea-- or at least one idea I had to move forward is to try to take advantage of this stuff and rust and the progress that the projects are using, what's interesting is that other things just fix themselves. The idea of just going and contributing to rust at the moment or the rust language at the moment could potentially end up fixing bitcoin. Lots of bitcoin contributors contribute to upstream libraries like gcc or openssl or binutils. I think it's time for us to do that but apply a rigorous researchy type of approach to it.

If that resonates to you, email me at coryf@mit.edu -- it tends to resonate with bitcoin developers. In the last week or so, some people I have been speaking with and these projects have potential to get kicked off. I think this is a good time to begin to collaborate on what is the 10 year project? If that's interesting to you, then come talk with me, otherwise we'll just live with everything broken for a while.

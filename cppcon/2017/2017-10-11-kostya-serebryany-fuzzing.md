---
title: 'Fuzz or lose: why and how to make fuzzing a standard practice for C++'
transcript_by: Michael Folkson
date: 2017-10-11
tags:
  - developer-tools
speakers:
  - Kostya Serebryany
media: https://www.youtube.com/watch?v=k-Cv8Q3zWNQ
---
Slides: https://github.com/CppCon/CppCon2017/blob/master/Demos/Fuzz%20Or%20Lose/Fuzz%20Or%20Lose%20-%20Kostya%20Serebryany%20-%20CppCon%202017.pdf

Paper on “The Art, Science and Engineering of Fuzzing”: https://arxiv.org/pdf/1812.00140.pdf

## Intro

Good afternoon and thank you for coming for the last afternoon session. I appreciate that you are tired. I hope to wake you up a little bit. My name is Kostya, I work at Google. I am going to talk about fuzzing today.

## Agenda

I hope to explain to you why we should be doing fuzzing. We will have several case studies related to fuzzing. I will discuss continuous and automated fuzzing which is a kind of magic. I will cover some of the challenges we face with adoption of fuzzing. I will not cover any deep technical details today. This is just a half hour talk. Your questions after the talk about any kind of detail are very welcome.

## Testing vs Fuzzing

So what is fuzzing? Let’s first discuss what is testing. In most cases testing your API means that you feed a fixed number of fixed inputs into your API and observe the behavior. On the contrary fuzzing is a process where you are feeding an infinite amount of generated inputs into your API. That’s it.

## Types of fuzzing engines

There are lots of different strategies for doing fuzzing or ways for generating test inputs automatically for your API. I am mostly working on so-called coverage guided fuzzing but this is all irrelevant for today’s talk. Today’s talk covers fuzzing in general.

## Why Fuzz C++ code?

So why would you fuzz C++ code? Please wake up.

## Hackers love C / C++

One of the reasons why you would want your C++ code is because hackers love C and C++. The problem with this is that the hackers love C++ and C for different reasons. Not for the same reasons as you love C++. This animated gif shows you how fuzzing can find the Heartbleed bug in five seconds. For those of you who don’t remember Heartbleed is a bug that shocked the industry and the internet about three years ago. I presented [this](https://www.youtube.com/watch?v=qTkYDA0En6U) at CppCon two years ago.

## Did he just say C / C++?

Did I hear any boos in the audience? Did I really say C / C++ at a C++ conference? Boo anyone?

## C++ inherited memory safety bugs from C

Yes I did say C / C++ because C++ unfortunately inherited a bunch of problems from the C language. The major one in my view is the set of memory safety bugs such as buffer overflows, use-after-frees, use of uninitialized memory and so on. Every time I say something like this “C++ inherited blah blah blah” I hear boos.

## “Modern C++” doesn’t have memory safety problems

I hear “Modern C++ doesn’t have those things.” I heard this when C++ 11 appeared, when C++ 13 appeared and I keep hearing it. I have a few things to say about modern C++. Let me just say one thing.

## Can you spot the bug?

This is modern C++. The class called `std::string_view` has just appeared in C++ 17. Who can spot the bug in this code snippet? Quite a few of you can spot the bug but quite a few of you cannot or are sleeping.

## Finding security bugs in C++17 code since 2011

That is a buffer overflow. We are creating a temporary object which is a result of concatenating two strings. We take the reference to the temporary object in the `string_view` then the object is destroyed. Then we use the reference to the destroyed object. Oops. Any kind of sane memory error detection tool for C++ would report this bug if you execute this code while testing with this memory safety tool.

## Even trickier

Things get a little bit more sophisticated if you just remove a few characters from this example. Instead of using “Hellooooo” with many o’s, you use “Helloo” with just a few o’s and it will become a different bug. At least as it is implemented in lib C++ because this is now a short string optimization, no heap memory is involved. It is still a bug but slightly different.

## Let’s fuzz some modern C++

So modern C++ you said. Let’s fuzz some really modern C++.

## https://github.com/google/woff2

I don’t have anything written in C++ 17 because the standard is two days old. But I have something written in C++ 11. This is a relatively small library called woff2 which handles web fonts. I would say that 50 percent of you have woff2 in your pocket, in your phone. It is a C++ 11 library. The team follows a strict coding style for C++ 11. The team uses code review. The team has unit tests. The units tests are running on continuous integration. The code uses STL containers, iterators, namespaces and even bells and whistles.

It didn’t help. When we started fuzzing this code we almost immediately found a buffer overflow which is a write of 12 kilobytes outside of the buffer. Just imagine this thing is running on your mobile phone and is processing data that you receive from the internet, from untrusted sources. You probably care about fuzzing. Do you agree?

## Woff2 Fuzz Target

Now let me show you how much effort you spent to find those memory issues involved. This was not the only memory issue involved. This snippet of code, we call it the fuzz target, is a single function that consumes an array of bytes and that uses this array of bytes to feed them into the API you want to fuzz. I want to emphasize this is all the effort required to fuzz that library and to find bugs in it.

## How to use libFuzzer

We found it was libFuzzer. You can find it with many other fuzzing engines the same way. Let me just show you how easy it is to do things with libFuzzer. Suppose you have this fuzz target in a separate file `fuzz.cpp` and you have all other files of your API somewhere else. All you need to do is get fresh clang, this is all pretty new development, compile all the code including the fuzz target with a couple of special switches. `-fsanitize=address` gives you memory safety checking and `fuzzer` gives you instrumentation required for coverage guided fuzzing and it also adds some library and link time. Then you want to create a directory `mkdir SEED_CORPUS_DIR (add samples here)` where you will put some samples for the inputs of your API. Then you just run the resulting binary on this directory `./a.out SEED_CORPUS_DIR`. This is it. I hope I convinced you that fuzzing is pretty simple.

## Fuzz Target

A few words about the concept of a fuzz target as we understand it. A fuzz target in our current definition is a function with a fixed signature that consumes an array of bytes. Inside that function you use the array of bytes with your API in whatever way you want to. The fuzz target should be tolerable to any kind of data. Any kind of crash or abort or searching failure or timeout or out of memory should be considered a bug. If not I would say that you code is not really an API. This fuzz target should be single process. It should be ideally deterministic. If you need randomness get the random bits from the input. Preferably it should not modify global state although we can tolerate this. The smaller the target is, the more efficient the fuzzing will be. Although we can fuzz arbitrarily large targets if we have enough CPU power.

## Security + Stability > Memory Safety

So far we have discussed mostly memory safety bugs but stability and security of an application, not necessarily a C++ application, is much more than just memory safety.

## https://svn.boost.org/trac10/ticket/12818 (regex)

Let me give you another example which I hope is suitable for a C++ conference. Eight months ago my colleague Dmitry Vyukov submitted a single ticket against a Boost regex library. This is literally the ticket. In just half an hour Dmitry found memory safety issues of different kinds, assertion failures, segmentation faults, infinite loops, a bunch of memory leaks and so on.

This is the effort he needed to spend to fuzz Boost regex and find those couple of dozen libraries. These are just half a dozen lines that have no complicated logic in them. All you do is take the data provided by the fuzzing engine and you feed it into your API. This is what you get, that many bugs.

## boost::regex bugs were fixed

I am very grateful to the Boost developers for fixing all of those bugs very promptly. This is great. Not all of the developers who get reports from us fix their bugs. Boost did. But the problem was continuous fuzzing was never set up. I want to emphasize that continuous fuzzing is much stronger than just fuzzing for reasons I hope you understand. These are the same reasons why testing is not enough and continuous testing is much better.

## boost::regex added to OSS-Fuzz 5 days ago

I have added boost::regex to the continuous fuzzing source which I am going to talk about in the next slide. It happened last Thursday evening because I was preparing my slides and I realized that something is missing on this slide. On Saturday 5 bugs appeared on the continuous fuzzing service in Boost. On Sunday evening two more popped up and one of them was actually a memory safety bug in Boost, stack buffer overflow. If anyone here is from Boost I will try to catch you tomorrow at the Boost dinner so that we can fuzz more of Boost.

## OSS-Fuzz: Fuzzing as a Service

A few words about the continuous fuzzing service I mentioned. The service is called OSS-Fuzz. We launched it in December last year. The project is a collaboration between quite a few different teams at Google. The project provides continuous and automated fuzzing of open source projects on Google hardware. It uses two different fuzzing engines right now, libFuzzer and AFL. More fuzzing engines are in the pipeline. The service also uses the sanitizers ASan, MSan and UBSan to find bugs at runtime. This project is available to what we call important open source projects. It is provided for free. We haven’t built this from scratch. Instead we reuse the same infrastructure that we have been using for the last two years to fuzz the components of the Chromium browser.

## OSS-Fuzz: 2000+ bugs in 60+ OSS projects

This slide shows some of our trophies. In less than a year the service has provided 2000 bugs for more than 60 open source projects. This is the slide from months ago. Now the numbers are even better. As you can see there is a usual set of suspects. Memory safety bugs, buffer overflows and use-after-frees. But there are lots of other types of bugs like out-of-memory, timeouts, leaks. The largest section comes from the tool called UBSan, Undefined Behavior Sanitizer. These are basically signed integer overflows and shifts by large numbers like shifting left by 1000.

## What if my code is not open source?

Someone at the conference has already asked me “What if I don’t have an open source project? What if my project is closed source?” In the current form the service is only provided for open source projects. We also don’t accept toy projects. The project has to be significant. All the tools used by the service are open sourced. Most of them are part of the clang LLVM toolchain. They are fully separated on Linux and Mac. I want to thank the Apple developers for helping me to port these tools for Mac. On Windows they kind of work. If you are in the Windows ecosystem there is a [service](https://www.microsoft.com/en-us/security-risk-detection/) provided by Microsoft. Take a look at that one.

## Structure-aware fuzzing

Back to fuzzing. The examples I have shown so far, OpenSSL, Webfonts and Boost regex. Those consume pretty simple data formats. To some extent these are bags of bytes. Not just bags of bytes but not very complex. Not every API written in C++ consumes simple data types. In many cases fuzzing complex data types is very inefficient because the fuzzer creates invalid inputs very frequently and nothing interesting happens.

## Case study: let’s fuzz a C++ compiler (Clang)

Let’s do another case study. Let’s fuzz something that consumes a very, very complicated input. Do you know anything that is more complicated than C++? I don’t. If we can fuzz a C++ compiler I am pretty sure we can fuzz everything.

## Fuzzing a C++ compiler: naive

Let’s take a look. A compiler is typically a series of building blocks. Roughly speaking it consists of a lexer, parser, optimizer and code generator. We first started fuzzing clang as a thing that consumes a bag of bytes. We found an enormous amount of interesting things. For example if you give the compiler these four bytes it will do a heap buffer overflow. There are quite a few of those. I have shown only the ones that fit on the slide. We have got use-after-frees, we’ve got infinite CPU and RAM consumption. All of those don’t really look like C++ code. Would you agree? The first one maybe but the second and third one… Maybe this is C++ 20, not C++ 17. This was annoying because yes we were finding bugs in the compiler but we weren’t going anywhere deep into the compiler. We wanted to get into the code gen. We started fuzzing the C++ compiler in a structure aware manner such that we know that we are fuzzing C++ or a subset of C++.

## Fuzzing a C++ compiler: structure-aware

This is what we got. We have implemented the toy prototype for fuzzing where we know that the input is C++. This input that triggers an infinite loop in LLVM, it actually looks like C++. It is a subset of C but this is my toy prototype. All of the bugs we found this way, and we found a few, they trigger something inside the deepest levels of the compiler namely optimizer and code generator.

## Structure-aware fuzzing with libFuzzer

How do we do this? We need to provide a little bit of help to the fuzzer by implementing what we call a custom mutator. Most of the fuzzing engines typically mutate the day to day, consume in some trivial way like byte flipping and bit flipping. Instead we need to provide a function that takes the bag of bytes, parsing it into an abstract syntax tree or some other structure, implements one single mutation on that tree and feeds it back to the target that we want to fuzz. We also have a support [library](https://github.com/google/libprotobug-mutator) that does all of the above on the protobufs. A protobuf is a library that provides AST serialization and deserialization. We then hooked this library into clang so that we can fuzz C++ not protobufs. I won’t go into more details now but this was really simple and all of this code is in the LLVM trunk now so you can have a look.

## Fuzzing can find logical bugs too!

By the way fuzzing also finds logical bugs. This is mostly important for things like cryptography, compression, rendering of any kind. It is very easy when you have two implementations of the same thing. Suppose you have a reference implementation of some code or crypto primitive and an optimizer implementation. You want to verify on every input they produce the same result. All we need to do is to implement a fuzz target that would call both versions of the provided input and verify that the output is correct. We have found quite a few bugs this way in cryptographic code. Here is one example (CVE-2017-3732, a carry propagating bug in OpenSSL).

## Useful?

Raise your hand if you think fuzzing is useful. Thank you.

## Simple?

Now raise your hand if you think it is simple. I haven’t convinced you that this is simple.

## Simple + Useful != Widely Used

Simple plus useful is not necessarily widely used. This is my pain point. I want fuzzing to be widely used because it helps get rid of bugs.

## Adoption at Google

At Google we have reached quite good adoption of fuzzing. Not good enough, we are still working on it but we have several thousand fuzz targets across our server side code and Chromium and open source projects developed by Google. This number is growing. We achieve this because there are several things about Google infrastructure that are critical here. First of all we control the build system. Building all those things is trivial. It is one flag. We have built automated bug finding, automated reporting, automated tracking. We have held several events, FuzzIts, Fuzzathons, Fuzzing weeks. Most importantly we advertised fuzzing in our toilets worldwide three times and I’m not kidding.

## Adoption elsewhere: YMMV

What about adoption outside of Google? Here it varies between the teams. I’ve just heard from one of the large C++ companies here at CppCon that they are using libFuzzer. Thank you guys but I want everyone here to use libFuzzer if it is applicable to your code.

## Fuzz-Driven Development

I started my career as a C++ developer 19 years ago. One of my first managers told me “No question. Tests are for students. Students have plenty of time for tests. We are serious developers, we are developing a production thing and don’t have time for tests.” It was before Kent Beck declared his test-driven development. Even now I see many projects and products that don’t really use tests. However this has changed dramatically. How many of you actually write tests for C++ code? If I asked this 15 years ago most of the audience wouldn’t raise their hands. But we need to go further, testing is not enough. In our experience testing finds roughly 10 percent of the bugs and 80 percent of the bugs are found by fuzzing. The remaining 10 percent are not found by fuzzing or testing, they are found in production by users. I want to proclaim fuzz-driven development. This is where all of the tests are essentially fuzz targets. The continuous integration system does continuous fuzzing. By the way this is not specific to C++ in any way. The people in the [Rust community](https://github.com/rust-fuzz) are already doing it very successfully. Despite the fact that Rust is a memory safe language they do find lots of interesting bugs. Most of them are not memory safety issues.

## We need to make Fuzzing simpler

We need to make fuzzing to make it more widely adopted. We’ll probably have to change the language, the IDEs, the compilers, the build system and whatever it takes to make it super easy. We need to make fuzzing as easy as putting one word in one place in your program.

## Proposal: C++ attribute

Here is my proposal that is not tested and not implemented but I want something like this to happen. Suppose that somewhere in your application you have an API function that consumes data. We want to slap an attribute on that function and have it fuzzed automatically by the build system, IDE, CI or whatever you have. `Data` and `Size` are not really C++. You would probably agree. We may want something more C++, maybe allow strings as parameters or maybe allow vectors of simple types as parameters. Or maybe allow any kind of types. But for any kind of types it becomes a little bit tricky because the fuzzer needs to know how to serialize and deserialize this data and optionally how to mutate this data. Then we will have to provide more stuff there.

## C++ Memory Safety > Fuzzing

I have mostly talked about memory safety and fuzzing. Unfortunately C++ memory safety is more than fuzzing. You will never solve all the memory safety bugs in your application with fuzzing. We need to do something else and I can see the two most important areas other than fuzzing. First of all we do need to have support from hardware vendors and I call this idea “Hardware-assisted memory safety.” Good news is that one vendor has implemented and shipped hardware with a very useful memory safety feature. Unfortunately I guess almost nobody here uses SPARC. Does anyone? If you are using SPARC you have a very useful memory safety feature but I don’t have SPARC. All other vendors have tried to implement something useful for memory safety and failed so far. We as a C++ community to put pressure on hardware vendors here. The second large area of improvement, we need to have something that will be a statically verifiable safe subset of C++ that would provide some guarantees of memory safety. I don’t know if this is C++ core guidelines like in the talk this morning or if it is something else. But we have to come up with it. Of course it will help only newly developed code, old code will have to do fuzzing, hardware assistance and bells and whistles.

## Summary

To summarize my talk today. Fuzzing C++ code is very useful because it prevents bugs. You agreed with me. It is also simple. I hope you agree once you try it. We must make it even more simple and make it widely adopted. Otherwise it won’t be useful for the entire C++ community. This is all of my talk. If you have questions please use the mic.

## Q&A

Q - Do you have something to simplify test cases as much as possible while still showing some bugs?

A - Can we simplify the cases generated by fuzzing? Yes most of the fuzzing engines provide some way to minimize the test input. Both libFuzzer and AFL have such switches. The examples for the naive clang fuzzing are minimized. You cannot remove any bytes from them. The examples for structure-aware fuzzing for clang are also minimized. The tools are not able to remove anything from them while keeping the bug.

Q - Are you guys fuzzing the Chromium embedded framework as well as Chrome itself?

A - Do we fuzz the Chromium embedded framework? I frankly don’t know. My team provides the tools and the service and the Chromium team fuzzes their own code. I don’t know the answer. I know that the Chromium project has several hundred fuzz targets across the codebase.

Q - As far as detecting the actual problems, the dereference of null pointers and overflows, is that all handled by the analyzers that go with the compiler or does your set up also include things that handle that detection?

A - The question is who actually finds the bugs. The fuzzing provides inputs that trigger interesting parts of code. They hopefully trigger the bugs but we need to somehow detect them. We use the sanitizers ASan (address sanitizer), MSan (memory sanitizer), UBSan. These are the dynamic bug detection tools that work together with fuzzing tools in the same process. You can use other tools available on your platform. In Microsoft you will probably use Application Verifier or Page Heap or other things.

Q - How difficult would it be to have a fuzzer to present the same kind of sequence of events to show the errors it is reporting?

A - How do fuzzing results compare to static analysis results? Fuzzing results are much better because with fuzzing you can have a reproducer that triggers the bug. You can rerun it, you can replay it, you can collect the trace from debugging, you can step by step it, this is what static analysis tools don’t provide at all or provide in a less usable way. In this sense fuzzing is superior to static analysis. I believe so.


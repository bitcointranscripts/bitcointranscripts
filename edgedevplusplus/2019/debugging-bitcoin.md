---
title: Debugging Bitcoin
transcript_by: Bryan Bishop, Michael Folkson
tags:
  - developer-tools
speakers:
  - Fabian Jahr
media: https://www.youtube.com/watch?v=8bea0bdoFG0
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/debugging-bitcoin
---
Slides: https://telaviv2019.bitcoinedge.org/files/debugging-tools-for-bitcoin-core.pdf

Debugging Bitcoin Core: https://github.com/fjahr/debugging_bitcoin

https://twitter.com/kanzure/status/1171024515490562048

# Introduction

I am going to talk about debugging Bitcoin. Of course if you want to contribute to Bitcoin there are a lot of conceptual things that you have to understand in order to do that. Most of the talks here today and tomorrow are about that. But actually writing code or fixing stuff, you will also have to learn some things on a practical level. That is what this talk is about. Even if you have a very good understanding already of how Bitcoin works on a conceptual level you can still run into these things that can block your process.

# Welcome to Bitcoin

Welcome to Bitcoin. You are a junior Bitcoin Core developer and you have to take your first steps. That is what this talk is for. I’ll talk first about preparation that you are going to need in order to log or debug stuff from Bitcoin. Then we are going to talk about some tools. Tools for segfaults, I am going to touch on briefly.

# Part 1: Preparations

First of all some hints on preparations. I really recommend you to install [ccache](https://github.com/bitcoin/bitcoin/blob/master/doc/productivity.md#cache-compilations-with-ccache). Ccache is a tool that is caching things that you have already compiled. This is going to speed up your process a lot when you are developing. You don’t waste time on it. Another thing that you should definitely do is set compiler flags and optimizations to zero.

`./configure CXXFLAGS="-O0 -g" CFLAGS="-O0 -g”`

Otherwise the debugging tools I am going to show you are not really going to work for you. They are going to work technically but you are not going to be able to recognize your code from it. I have an example of that later in the slides. I am going to hint at it but just make sure you do these things when you follow the further steps.

# Logging

We are going to start with logging. You can find all the information I am going to talk about by Googling or by reading README files on Bitcoin Core. Something that you are going to see recommended when you want to log something out of the code is this function `LogPrintf`. Let’s say you are starting out and you want to log something because you want to see whatever you edited in the code is actually doing something. You put this `LogPrintf` in, you compile, it works.

`LogPrintf(“\@\@\@\@\@\@“);`

You run `src/bitcoind -regtest` and it should run by this point where the `LogPrintf` is. This is logging to the `debug.log` file. But actually it is not working. You can see I am grepping for these \@ signs.

`cat ~/Library/Application\ Support/Bitcoin/debug.log | grep \@\@\@`

Nothing is coming out. There is a problem here that you should be able to see from the slide. Does anyone see what the problem is? The problem is we are running regtest which you probably do if you are on your local environment. But this `debug.log` file is the mainnet `debug.log` file. This is the first hint of the main message of my talk. There are different environments, different contexts that you have to be aware of when you are developing locally. It is going to happen to you that you are going to be in the wrong context. You will forget where you are. When you `grep` for something, you do some fuzzy matching or so, you are going to miss something and you won’t see it. You have to check again. Am I in the right folder? Am I in the right file?

# Being in the right environment

If you are running something in regtest then here you need to find the `debug.log` file that is in the `regtest` folder and then you will see the output.

`regtest/debug.log`

# Logging from unit tests

(Run `src/test/test_bitcoin` directly with `--log-level=all`)

Moving onto unit tests I am going to go through logging and debugging. First running it yourself, then running unit tests, then running functional tests. With unit tests you cannot use `LogPrintf()`. Instead unit tests are running with Boost. You have to use these `BOOST_TEST_MESSAGE`. There is not really much more to it. You cannot run the normal bitcoind. There is another executable that is compiled just for the unit tests. That is `src/test/test_bitcoin`. You have to run that with `--log-level=all`. Then you are going to see all these messages.

# Unit test logging in action

You can see that here as an example. There are other examples of these `BOOST_TEST_MESSAGE`. You can do these with asserts and so on. They are going to come out in the output as you can see there.

# Logging from functional tests

Logging from the functional test, especially if you already have some experience with Python this is really simple. This is not a compiled language so you don’t have to think about so many steps there. You just use this `self.log.info` method. You’ll see this all over the functional tests. This is probably not going to be hard for you.

`self.log.info(“foo”)`

Another thing that you have to think of though is you have to run the test directly and not through the test harness, `test_runner.py`. The test runner is not printing out these messages.

# Using a debugger

How many here know what a debugger is? I’m going to run through it very quickly. Most people use debuggers like gdb or lldb. Maybe you are using it in a IDE or something like that. These are tools that everyone can use and that I have seen be used very commonly by Bitcoin developers. With these you start an executable through the debugger. You set breakpoints and then as you run the code the code runs into these breakpoints. You can inspect variables and step through lines of the code.

# Debugger from own environment

`lldb src/bitcoind`

`(lldb) b blockchain.cpp:123`

`(lldb) run -regtest`

This is straightforward if you know how to use gdb or lldb. When you use the bitcoind executable directly you just run bitcoind that you built with lldb. I am using MacOS. For MacOS lldb is definitely better. You can use gdb, gdb is better on Linux. It depends on your system. The two are very similar, just minor differences in the calls when you are inspecting stuff. You can set a breakpoint here in any file. You can also specify function names or something like that. Then your run the file with the parameters that you need and you will see the results that you want.

# Also works for unit tests

It kind of works the same way for unit tests as well. The only thing that you have to remember is that you use the `test_bitcoin` executable and not bitcoind. Here you can see it in the example. You set a breakpoint in some file you are going to run into and then you run it. It is going to stop at the breakpoint.

# Should be easy for functional tests…

For functional tests, the logging was at least for me the easiest. Running functional tests and then running a debugger is pretty simple. You use pdb. That is the same as gdb but working for Python.

`import pdb; pdb.set_trace()`

You put this `import pdb` and then `pdb.set_trace()` into the code. It is going to stop there. I understood all of these things but then I had this idea that I wanted to inspect the C++ code that was being executed by the functional tests. This is where it gets really interesting. This is the most interesting thing I can teach you today. How do you get into debugging the C++ code?

# Where is the bitcoind process?

The problem here is that the functional test which is Python code is launching and executing a bitcoind instance. This uses a temp folder as its datadir. It is hidden away from you. You cannot really interact with it in an easy way. To get in there you need a game plan. We are going to go through that game plan.

# Gameplan

First of all what you need to do is run the functional test (not using `test_runner.py` that is going to start the bitcoind process for you. Then you have to stop this test. For that we are going to use pdb.

`pdb.set_trace()`

Then we have to find the bitcoind process that we were running with the functional test and attach to that process using lldb. We have to let that process continue (`continue` in pdb) and it will run into our lldb breakpoint. One thing that we are also going to need to change is the timeout because functional tests have a timeout of 60 seconds. That is not going to give you a lot of time to debug if you keep that in place.

# Demo time!

That is something that I would like to show you here as a demo. First of all up here you can see that I have changed `rpc_timeout` from 60 seconds to 600. That should give us a little bit more time. Down here what we are looking at is the `getblockchaininfo` test. Everyone who has ever run a node for themselves and checked that they are syncing fine, that `getblockchaininfo` call is probably what they run. I have put in the pdb `set_trace` here. That is what we are going to run first. We have run into the `set_trace` from pdb. We have to know what process we want to attach to. This is critical because some tests are running more than one instance. How we can find that out is if you look at the test on `self` you have this array of nodes. We only have one node in this test but if you have several ones then you need to know which node you want to attach to. Then you can look at `process.pid` and that is going to give you the PID number that you want to inspect. Take that number and put it in here. Now lldb is attaching to this process in particular. We can set the breakpoints. This process is not running both from pdb and from lldb. I can set these breakpoints on it now. Here I can let it continue from the lldb side but it is still not really running because pdb is still blocking it. We can unblock it. Now we’ve run into that point here. Here we can inspect this. I am not going to show you everything, all the calls you can do with this. Now you can interact with this with lldb. What is really neat about this is that oftentimes you have these complicated setups of things that you want to inspect with Bitcoin. You don’t want to run through these things by hand all the time. Typically you can write a functional test which is going to be useful for you anyway. Then you can have the functional test always bring you to that setup point and inspect the things you need to.

I’ll repeat what I did. First of all we ran into this `pdb.set_trace()`. Then we jumped into the pdb breakpoint and we went over to lldb. We attached to the process with lldb, we set a breakpoint, let that process continue, let that process continue in pdb and then we run into the breakpoint with lldb.

# Debugging contexts

As I said in the beginning my main point here was when you are logging and debugging with Bitcoin especially in the beginning there are lots of different contexts that you have to be aware of. You have to check if something is not working whether you are in the right file or in the right context. You need to use the right tool for the job. This is another overview.

See slide: https://telaviv2019.bitcoinedge.org/files/debugging-tools-for-bitcoin-core.pdf

# Segfault tools

Need to activate with `ulimit -c unlimited` and then run in same terminal session
Run program with segfault
Find core dump in `/cores/*`
Make sure to clean up afterwards

One more thing that I am not going to talk about in detail is if you are facing segfaults. I am not an expert on these tools yet but something for you to consider as well. You can use Core dumps if you are facing segfaults. For that to work, at least on MacOS, you have to specifically enable them using this `ulimit` call. You run the program and then you will find these Core dumps in your `/cores` folder. You need to make sure that you cleanup afterwards because these are huge files. You can clutter your disk pretty quickly.

# Valgrind

Inspections, used similar to lldb
`valgrind --leak-check=yes src/bitcoind -regtest`

Another tool is Valgrind where you can run leak checks with it. This works similar to lldb.

# Debugging Bitcoin Core doc

https://github.com/fjahr/debugging_bitcoin

I promised I was going to give you something at the end. Here is a link to a doc I have created. This has everything that you have seen here in this talk and even more information. I know it is hard to grasp everything in this talk. You are going to need these tools when you run into problems. Most of this information you can find in READMEs in Bitcoin but it is scattered over 5 or 6 different README files in Core. Check this file out, read through it, see if it is helpful for you and happy to take feedback. Any questions?

# Q&A

Q - What is the `enable-debug` config option?

A - You mean in the compilation step? It is also turning off optimizations. I think it is not setting `O0`. I am not sure exactly what it says. I think it is working fine but some people mentioned that they were having problems with it. I also remember it wasn’t working for me initially. I found out that setting `O0` is the cleanest way to disable optimizations so that is what I am using. It is basically doing the same thing.


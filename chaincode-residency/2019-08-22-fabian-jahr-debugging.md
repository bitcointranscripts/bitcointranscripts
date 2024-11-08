---
title: Debugging Bitcoin Core
transcript_by: Michael Folkson
tags:
  - bitcoin-core
  - developer-tools
speakers:
  - Fabian Jahr
date: 2019-08-22
media: https://www.youtube.com/watch?v=6aPSCDAiqVI
aliases:
  - /chaincode-labs/chaincode-residency/2019-08-22-fabian-jahr-debugging/
---
Slides: <https://residency.chaincode.com/presentations/Debugging_Bitcoin.pdf>

Repo: <https://gist.github.com/fjahr/2cd23ad743a2ddfd4eed957274beca0f>

<https://twitter.com/kanzure/status/1165266077615632390>

# Introduction

I’m talking about debugging Bitcoin and that means to me using loggers and debugging tools to work with Bitcoin and this is especially useful for somebody who is a beginner with Bitcoin development. Or even a beginner for C++ which I considered myself a couple of weeks ago actually. I’m going to tell the story of a fictional beginner to Bitcoin development. This disclaimer, while you may think you recognize some names just assume everything is made up because I made it all up.

# Welcome to Bitcoin

You’re starting out with Bitcoin as a junior and you start on your first day and you get some assignments, some very basic stuff. You just try to find your way around the codebase, logging, you look around and see `LogPrintf`, something that looks useful. Also `cout`, that’s something you find. You do that and you also found that there is a debug.log file and after running Bitcoin yourself you try to grep the debug.log file but you don’t find any of the strings that you thought you were logging. What is really going on here? You think I will just ask in a chat because it is my first day so somebody can help me out.

# Let’s ask in the chat

You ask very nicely “Hey the logging is not working.” A helpful senior developer comes along and answers you in the chat “Have you forgotten to recompile?” You probably did but after you recompile you still don’t see the logs. You tell him “Of course I did not forget to recompile. Any other ideas why this could not work?” The senior developer is very helpful so he reminds you that there are different environments that you run Bitcoin in and if you looked at the paths closely that I just showed we were actually in mainnet and not in regtest which you probably mostly use when you’re developing locally. That’s the first thing that you have to keep in mind. That is the overarching message from this talk. As a beginner you have to remember that there are different environments in terms of tests and running Bitcoin. If you don’t find what you’re looking for or it doesn’t work in terms of debugging you are normally in the wrong place or looking in the wrong place. Or just using something that is logging to the wrong place or something like that.

# Helpful senior dev is helpful

What the developer said was right. We actually see that the logging to `std::out` is showing and `std::out` does the `LogPrintf` but the `std::out` does not show up in debug.log but at least we find the `LogPrintf`in the debug.log that is in regtest here. That sounds great. You make your first pull request and you get some feedback.

# Moving on to unit tests

You are asked to add some unit tests. You also learnt from your mistake earlier and don’t want to embarrass yourself again in the chat so this time you Google and there is another senior developer Andrew, he actually wrote some very informative message on the StackExchange. You can see there if I want to do unit tests then I have to use this other binary, this test binary. I’m also using Boost here as the testing framework so I have to use these BOOST_TEST_MESSAGEs and I also have to remember this `--log_level=all`. You try this out and this is pretty straightforward.

# That was kind of easy

It works as you would expect. You are using this test_bitcoin here, this is just to choose a particular test run with `--log_level=all` and this Boost message comes out here as you expect. Unit tests are pretty straightforward. We think what is something more we can do? We’ve heard of these debuggers so let’s try that out.

# What about using a debugger?

Just to remind you what a debugger actually is if anyone doesn’t know, what we’re using here is gdb or lldb. I have a Mac, lldb works a little bit better here. If you are Linux you probably use gdb but it doesn’t really matter because they are almost the same, just a few different commands. A debugger is when you start an executable you can set some breakpoints in a program and then as you run the program it stops at the points where you set breakpoints. Then you can inspect variables and you can step through the commands line by line. It is very helpful especially as a beginner to understand how to use this because it accelerates your learning. It also helps you be much more productive.

# This is pretty cool!

If you use this with test_bitcoin it works very straightforward. You use lldb to run test_bitcoin. It is not running yet, it is actually lldb running with test_bitcoin as a target. Then you can set b, a breakpoint and you run giving here any parameters you would normally hand to test_bitcoin. You’re stopping at the point where you set the breakpoint. This is really good. Then you also want to add some functional tests.

# Should not be too hard for functional tests

This was very straightforward with the unit tests so this should just work very easily. Functional tests, a global definition, are tests that are executed from the view of the user. We are basically describing how a user or several users might behave and this is then running a RPC, from the view of the CLI. These are implemented in Python in Bitcoin and if you look in the Python code you can just use `self.log.debug` and you can use pdb which is a debugging tool in Python. This works very easily but if you then want to look from the C++ code or if you want to use gdb or lldb in the C++ code then it gets a little bit more tricky. The Python is running bitcoind in the background and there is not a really easy way to get to it.

# But where is the executable?

That means this is not straightforward, we need a game plan. Let’s get together and I’ll tell you the gameplan.

# Gameplan

The first thing we are going to do is run the functional test and let it start the bitcoind process. Then we need to stop the functional test because we want to get to the bitcoind process. For that we want to set pdb, we use pdb to stop that. We have to find the bitcoind process which is technically running but not doing anything because the functional test is not doing anything. We have to attach to it using lldb, we have to set the breakpoint and at that point we can use pdb and tell it to continue. Then the C++ code is actually going to run into the breakpoint that we set with the lldb. Optionally we want to change the 60 second timeout that is running on the functional test. We do the pdb to stop the functional test, we run the functional test here. We go to the other tab, we run lldb with hopefully the right PID. We set the breakpoint on the function or the line or whatever we want. We let the bitcoind process continue. Then we let the Python functional test continue and then we are stopping at the right point.

# Major key to success: Context awareness

I was saying in the beginning my main message here is context awareness. When you’re starting out there are several contexts; the unit tests, the functional tests, running bitcoind yourself. You want to log from the tests, you want to log from bitcoind, from C++ code, from Python code. You have to have a mental map of where you are and where you have to look to get the output that you need.

# Debugging contexts

I actually have in the end document that you can look at the different dimensions of test driver, bitcoind context and are you doing things manually using the CLI for example? Are you running unit tests, are you running functional tests?

# Things left out

Some things that are left out for debugging in general. Mostly you find these in the READMEs, it is really important to install ccache and also to remove parts from the compiler that you don’t need like the GUI for example if you are not a GUI developer. Disable optimizations as well so the compiler doesn’t remove all the symbol names and so on, otherwise you can’t really see anything. I also left out segfault tools because it is a different category of stuff that you might need to debug. I was focusing on things that also could help beginners that maybe don’t have a huge bug that they need to work on but instead they want to look around in the code and see what is happening. All this stuff is also in the document. If you feel like this is something that is going to help you, you also cannot keep things in your head maybe, here I have written a pretty long GitHub markdown file where I’m describing all the different commands that are in here. It is still a work in progress so maybe it is not ideal but I’m looking for feedback. It is maybe something that can go, or at least parts of it, into the Bitcoin READMEs. This is optimized for Mac so if you have to adapt something for Linux it shouldn’t be hard but I would be grateful if you give me some feedback on that. I can add these commands to the README.


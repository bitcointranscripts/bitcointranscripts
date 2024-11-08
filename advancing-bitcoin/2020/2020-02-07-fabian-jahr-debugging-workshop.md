---
title: Debugging Bitcoin Core Workshop
speakers:
  - Fabian Jahr
date: 2020-02-07
transcript_by: Michael Folkson
tags:
  - bitcoin-core
  - developer-tools
---
Fabian presentation at Bitcoin Edge Dev++ 2019: https://diyhpl.us/wiki/transcripts/scalingbitcoin/tel-aviv-2019/edgedevplusplus/debugging-bitcoin/

Debugging Bitcoin Core doc: https://github.com/fjahr/debugging_bitcoin

Debugging Bitcoin Core Workshop: https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386

## Introduction

First of all welcome to the debugging Bitcoin Core workshop. Everything I know more or less about using a debugger to learn from Bitcoin Core and to fix problems in Bitcoin Core. I didn’t go with traditional slides because I want to teach you how to use this tool, the debugger, in the context of Bitcoin Core. You may not need it in the next week but maybe you will need in three weeks. If you have forgotten about what we did here I hope you can go back to this document, look at it and use these instructions again. That’s why I structured it as a gist. [This](https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386) will stay up and will be something that you can use later on. We will learn how to use these tools. I am personally using lldb because I am on MacOS. People on Linux can install lldb but it may not be so great. gdb is also available, it has been around much longer than lldb. It is supposed to be an improved version of it. I am showing different versions of the commands so you should be able to follow using gdb in the same way. I’m using lldb but if you are using gdb and you run into any problems I will come around and help you out. We will try to figure it out. I’ll show you some basic commands and how to use them in the context of Bitcoin Core. Then I have exercises. These exercises are more drills, they are not super exciting. The point is you are using the tools. I will give you an exercise where you could find the answer to this exercise by just looking at the file in the code. I thought if I edit the code and give you a specific version that you have to fix we would all be sitting and compiling a lot. I didn’t really want to do that because that is usually where the workshop breaks and everyone is sitting compiling, different things go on for different people. We will all do this on master and look at the code. At the same time if you have something that you think is more interesting than the exercise I give you, if you have something that you want to debug, a different part of the code, please go ahead and explore. I will still come around and help you out if you have any problems. I structured for this two hours. Now we have three hours so there is a lot more time to dig into stuff as much as you want. We stay high level. You can use debuggers to dig much deeper into the code.

## Why debugging with lldb and gdb?

First of all what is a debugger? A debugger is an app that you use to debug another app. There is really not that much more to it. Stepping through the code. You do that by setting breakpoints at which execution of the program stops. Then you can go through the execution of the program step by step. You can evaluate things that are happening. You can look at variables, what their contents is. You can run expressions, add variables if you want. You can look through backtrace, backtrace is the set of functions that are executing at the moment. Why does this matter to me? I come from higher level programming languages than C++. My first professional job as a programmer was using Ruby. There it was typical to jump into pry. Pry was the debugger. You also have to interact with the interactive Ruby shell. pdb is the comparable tool in Python. I was using this almost every day as I was figuring out stuff in Ruby. When I went into C++, mostly motivated by Bitcoin Core, it felt like there was no tool. Then I discovered gdb and lldb. Most people are not really using that to the extent that I would’ve thought in Bitcoin Core development. I have met quite a few people who are contributing to Bitcoin Core and they think it is too much work to use these tools. They don’t use it very often. They rather rely on print statements or something like that. Or stare at the code until it renders. That’s valid, these people are still productive but for me I wanted to have this tool in my toolchain. It is not something I use every day but I use it quite frequently, mostly when I get stuck. If I can figure out a problem within a few minutes by looking at the code and reading through it but often I will stay confused about the code. Jumping into the debugger is another way for me to explore it and get a better understanding of what is happening. That is why it is a very useful tool. It has definitely helped me in different situations. Whether you are a complete beginner, you have never contributed any code to Bitcoin Core or if you already have some contributions but you are not using a debugger very often, this will help you adopt it.

## Why use the plain CLI interface?

We will use lldb and gdb with the plain CLI interface. I personally do this as well. The reason for this is that I generally like being on the command line. I also try to keep my setup as simple as possible. I like it to be portable. If I am on a machine that I haven’t set up myself and customized a lot usually I will still be able to find my way round. I also use Vim, it is on almost every machine. I have some custom commands but I try to keep them to a minimum because I like to be able to jump onto other people’s machine and I like pair programming. When I get the chance to collaborate with somebody, using their keyboard, that is still possible. There are some GUIs for lldb and gdb that are presenting the content in a nicer form. I looked into these but there was no obvious first choice that jumped out at me. Mostly the products that I saw there, there were no commits for multiple years. I thought I’d stick to the simplest version that I can think of. That is what we are going to use today. Nevertheless out of the box lldb and gdb also offer a GUI mode. This is displaying the stuff a little bit differently. You cannot run the same commands in there. There is an overview of information that is hiding behind commands. I will show that briefly and you can play around with it as well. In lldb you just have to type `gui`. I’ll show it but it hasn’t been that helpful for me. The preparations that hopefully everyone has run by now.

`./configure --enable-debug` aka `-O0 -ggdb3`

You build Bitcoin Core the same way as described in the documentation. But you have to configure with this option `--enable-debug`. What this means is that you pass in the flags `-O0` and `-ggdb3` to the compiler. There are no optimizations. `-O0` means leaving out optimizations. Typically it is compiled with `-O2` I think. Why do we not want optimizations? Because the compiler removes information from the code and also restructures the code in a way that makes it more efficient to run it in a general sense. If you were to run this `--enable-debug` as a full node you would see some degraded performance. What we want to do is look at the code. That’s why you want to have as much information available as possible. We set optimizations to zero and this other instruction is keeping around some additional information that you can access when you are doing debugging.

## Useful commands

https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386#useful-commands

I’ll talk you through a couple of commands. These are the commands that I have been using mostly. I have presented them in this compressed [table](https://gist.github.com/fjahr/5bf65daaf9ff189a0993196195005386#useful-commands). There are a lot more commands available in lldb and gdb. At the end here I have a full map of commands that lists the commands that are available on gdb and lldb at the same time. You can explore these as well. For the exercises and for getting started this list will suffice. I will show some things demonstrating it. Then you can go back to this list and use these. First of all when you do stuff with the debugger you first have to load the program that you want to inspect. We do that in the command line by typing:

`lldb /path/to/foo.app`

You supply it the path to the executable that you are using. If you are in the Bitcoin Core folder that would be `src/….` Then you interact with the breakpoints. As I mentioned a breakpoint is a point you set in the code. It can be on a function but it can also be on a specific line. There are different ways to do that. You can set these with different commands. After supplying this command `lldb /path/to/foo.app` you will be on an interactive shell that lets you interact with lldb and set breakpoints. If you have already set some breakpoints you can use the `breakpoint list` command to get a list of all the breakpoints that were set. You can set breakpoints by supplying the name of the file. `breakpoint set -f foo.c -l 12` foo.c is just a stupid example and then the line, this means you set a breakpoint on this specific line in that specific file. This is the most precise way. You can also set a breakpoint on a name. `breakpoint set -n foo` That would typically be a name of a function or so. I do this for convenience quite often. It is dangerous because this will set it on every function that has that name in the whole codebase. If you want to be precise you should go with the other option but if you know that there is only one name or you are running lldb in a controlled environment and you know you aren’t going to hit any other functions doing other stuff then you can use it. There are three or four other ways to set breakpoints in that table. You can also delete breakpoints. `breakpoint delete 1`. You can also disable and reenable breakpoints. I don’t really do this that much because I usually set a breakpoint, hit it, look around and then I will shut down the process. Take some code, maybe recompile it and then start over. The options are there to do much more expansive digging around. Using different breakpoints, listing them, enabling them, disabling them. I just haven’t done this extensively myself. This is interesting but I also haven’t used much. `watch set var global` You can set watchpoints. This is a breakpoint that activates if you write to a specific variable. If you are interested in when globals change, when are they written to, you can set watchpoints on globals. Then after you’ve set different breakpoints and any watchpoints then you will run the executable. Up until this point the bitcoind process that you started, the program that you loaded up here, that has not been running. `run` is the command that you use to start your process. This is also the point where you add arguments to that running bitcoind process. There are different ways to supply the args. This is the one I use, naming them just like you would when running bitcoind in general, naming them here after `run`. Another way to load a program is by attaching to already running programs. This will be interesting when we look at how to attach to a bitcoind that is being run by a functional app. This is super helpful. Something that I haven’t used myself yet but is super interesting is that you can name the process and then let lldb wait for it. This can be interesting if you a have a third party app that is launching bitcoind for you in a specific way. There are these projects like Node Launcher from Pierre Rochard that launch Bitcoin for you and manage it for you. In this context this can be something that is useful to use. When you are hitting a breakpoint you can inspect a program. I have some more instructions on it down here. When you are finished with inspecting then you will use `continue` to let your program run on if you are interested in that. We have different `step` instructions. There are different naming for these. Stepping in means that if you are on a line that has a function call then you will step into that function. You are in function foo and that has a function bar, you are on that line. If you step in that context you will get into function bar. When you `step-over` or `next` then you will just go to the next line in function foo and you will not get into function bar.

Q - It will execute the function all the way through? If you do `step-over` it will execute those lines or it will just ignore them?

A - It will execute bar completely.

Q - There are better tools these days, GUI based. Why are you using such primitive things?

A - I tried to explain at the beginning. I haven’t found any tools that make me happy that are GUI based. What tools do you like to use?

Q - Visual Studio

Q - Is it open source?

A - I have never found any that made me happy in a short amount of time. I like these simple tools. I am not telling anyone to go that route. This is the way that I work and by keeping the workshop the same way everyone doesn’t have to install these tools.

Q - What are the advantages other than it being a GUI?

A - With a GUI I can hover my mouse over it and see its value. I can do everything that is being described there much much quicker when I’ve got tools designed for a human. That’s why GUIs were invented.

If we do `step-over` then the function `bar` will execute normally but then will go down to the next line. We also have `step-out` or `finish` which means we will leave `foo` and go into the function that was calling `foo`. This is a good example of showing the difference between lldb and gdb. gdb has been around for a long time but it is kind of inconsistent with these commands. It is using the `step` command for stepping in, the `next` command for stepping over and the `finish` command for stepping out. I like them and I use them in lldb because they are aliases in lldb. But at the same time they are not very precise. That’s why lldb was created, to clean this up. lldb has primary commands `thread step-in`, `thread step-over` and `thread step-out` which are much more precise. They are showing what they are doing but you also have the gdb aliases in lldb. In this case I prefer them and I use them. Then interacting with threads, there are not many points where I’ve interacted with threads. Unfortunately this has also created some problems for me. In one of the exercises I will give you a hint where you step over something because the reason there are some problems with thread is Boost used as a library and I think this is confusing the debugging process. You can look at the different threads and you can jump around between them but it is not something I am going to touch on. There are different commands in the full list.

Q - I just tried to compile with the `-O0` parameter and it says it is an unrecognized option.

A - You ran `./config --enable-debug aka -O0 -ggdb3`? This is to explain what `enable-debug` is doing in the configuration process.

Q - They are parameters for `enable-debug`?

A - The rest is just an explanation of what it stands for. What `enable-debug` does is it sets flags for the compiler that are optimizations `0` and `gdb3`. That is what used internally. I just put it there as an explanation of what is really going on, what this `enable-debug` is doing. You only need `enable-debug` when you run it.

You can print variables which is one of the main things that you are probably going to do when you are using a debugger. In lldb you have to make a distinction between a stack frame variable and a global variable. Whereas with gdb there is no distinction. You use `p` for both. You can interact with environment variables, I haven’t been using that much. You can evaluate expressions. This is something that I use a lot. If you want to execute a function and see what the function returns or if you want to set a variable to a specific value that is what you do with `expr`. It means run this line of code right now and then you go on. You can also look up symbol information if you have problems with variables that are coming from other libraries.

## Misc tips

Then I have some general tips. If you are running lldb and you find these commands to be a little too much to type you can abbreviate them and effectively do a regex match on it. The shortest match to these commands can be what you want. If you want to set a breakpoint you can also do `br s` and it will do the same thing. I like to type them out but if you want to optimize your workflow and not type as much you can do this. You can set a `/.lldbinit` file if you want. That is how you customize your environment. For example you can customize how variables are printed out. I haven’t used it yet but it is something that you can dig into if you find yourself using the debugger more and more and want to customize your environment. One detail that irritated me when I got started using a debugger is if you get into a loop and the loop is very long there is no clear instruction of how to get out of that loop. There isn’t a break out of loop command in lldb or gdb. The way we solve this is if you have a breakpoint in that loop you first set a breakpoint behind that loop and then step out of that breakpoint.

## Exercises

Now we are finally at the exercises. I will do a small demo on how to start a debugger for this first exercise. You can explore these as much as you want. Then after some time I will walk around. Then we’ll do the second part which is where we use the debugger with functional tests.

I just want to bitcoind in a very standard way and then interact with it through the RPC. I will do `lldb src/bitcoind`. The program has loaded. I have set my parameters in my configuration file so I don’t have to change anything. It is already configured to be regtest. If you don’t have regtest configured then you can set `-regtest`. I do `run`, it is running and you get the output in the standard way. Here I can interact with it. I’ll set a breakpoint.

`breakpoint set -name getblockchaininfo`

This is kind of sloppy. I am not using the file and the line right now, just for demonstration purposes. I run it. The process is running now and the breakpoint is set but nothing will be happening yet.

`bitcoin-cli getblockchaininfo`

Now it is going to run into the breakpoint and I am at the beginning of `getblockchaininfo`. Now you can interact with it. Look at these exercises. I have given you some small ideas to look at, try out and dig in.

Q - You hit the breakpoint and you are at some line in the code. I want to see the code around that line.

A - You see a very small window here. What you maybe need is that GUI that I mentioned. Going to the GUI you just type `gui`. Here you cannot interact with it. You can run expressions here. That’s why I don’t use it. I switch back to a window where I have the code open anyway. I have that in a parallel window.

Q - If you `enable-debug` and you’re on MacOS it will automatically use lldb?

A - lldb is just a program. That has nothing to do with Bitcoin. You can still run lldb on bitcoind without `enable-debug`, it is just that the output is not going to be very useful.

First I am starting bitcoind with lldb.

`lldb src/bitcoind`

I have seen many of using `-name` so maybe this time I will use the file and the line. If you have a good idea of where you are and where you want to go I would use the file and the line. I am here in the RPC `blockchain.cpp` file and I want to get into this `getblockchaininfo` function

Q - What is your editor?

A - Vim

I want to be on this line. The following lines are interesting to me.

`breakpoint set -f rpc/blockchain.cpp -l 1255`

Now I can `run`.

Q - What is the command for gdb for `breakpoint`? It says undefined command.

A - `break`

Now I am calling `getblockchainfo`. I use `step-over` to get to a line that is interesting to me. Let’s say I want to go to `getblockhash`. Down here I would do `step-in` because I want to see where this is coming from. Here I would do `step` and I get into `getblockhash`. I can see that I’m in `CBlockIndex` and this is returning `phashBlock` from within that class. This is all I wanted you to do for this first exercise. Using `step-over` to go through different lines in `getblockchaininfo` and then step into some of those functions that I did there, step further inside to see where the values are coming from. Just to get used to this navigation with lldb.

Q - Each time you hit a breakpoint you are just scanning with your eyes to see if there is a keyword that’s interesting?

A - When you get into problems where you don’t understand anymore what is going on in the code just from reading the code that’s when you can use the debugger. It is hard to artificially create exercises… You will find this out by just navigating the files.

Q - How do I see the value of a variable?

A - `target variable` is for globals and `frame variable` is for stack frame.

So this is pretty basic things that we have done so far. Driving the bitcoind through interactions with bitcoin-cli. There are very few cases where I would do this because they are usually very basic things that are happening. It gets much more interesting if you are using tests and you want to inspect what is going on.

## Using debugging with unit tests

Unit tests basically work the same way in terms of using the debugger. But with functional tests it is much more interesting. With the unit tests you start the debugger in the same way as you were doing it up here with the CLI. The one thing that we have to be aware of is that the tests have their own executable. Instead of bitcoind you have to provide this `test_bitcoin` file. That is where the unit tests are built. You can still set breakpoints anywhere in the unit tests exactly the same way as you were doing with bitcoind. The tests will execute. If you want to run a specific test, which is usually the case, you can certify that with this parameter `--log_level=all --run_test=*/lthash_tests`. You can go to the unit test [documentation](https://github.com/bitcoin/bitcoin/tree/master/src/test) on how to run the tests. It is not that different from bitcoind and interacting with the CLI.

## Using debugging with functional tests

What is much more interesting is the functional tests, what I am debugging most frequently. Usually when you are investigating stuff in Bitcoin it is not just things that are very simple it is that there are very complex steps that happened before and you get into a state that you want to investigate. We looked at regtest and generating 100 blocks, that is not that interesting. What is much more interesting is if you have a large P2P network and you want to see how the nodes are interacting with each other. If you have a full mempool and transactions get evicted from the mempool you don’t want to have to write a script to get your Bitcoin node to your point. Luckily there are already functional tests that do that for you. If you want to inspect the state of the system then I would recommend that you find the functional test that is bringing the system to that point and then inspect the system when it is being run by that functional test.

Q - Functional tests are integration tests?

A - They are named functional tests in Bitcoin.

The functional tests are written in Python. It is under `/tests` in the repo. You will find a bunch of Python tests. There’s also the test framework. That’s the first step that we will do together because it is something that you have to do if you want to do anything with these functional tests. There’s this file `test/functional/test_framework/test_framework.py`. In there on line 99 there’s a RPC timeout specified. What happens is this test framework when it is running the tests, it is writing them to the RPC just like a user would and there is a timeout specified. Usually when you are running the functional tests you are running the whole test suite. There’s over 100 tests. You don’t want to have this test running forever. There’s a timeout of 60 seconds, no test will ever run over 60 seconds. What we are going to do is stop the functional test from running, then go into the node that is under the test and do some stuff in there. We are probably not going to be able to do that in 60 seconds. That is why we have to extend that timeout. I would like you to go to the functional test framework and change this parameter. I’ve changed it to 6000. Please upgrade that to a higher number because you don’t want the test to timeout. Then your node will crash and you will have to start over.

I mentioned we have these Python functional tests. These are driving the nodes through the RPC just like a user would. What we want to do is inspect these nodes that are running through the Python test and be able to debug them inside. The main thing we have to do is get access to that bitcoind process that is being run by the functional test. The functional test is not waiting for us by itself, we have to stop the functional test first. It is not finishing before we can connect to that bitcoind process. The way we are going to do that is to insert this line `import pdb; pdb.set_trace()` which is going to import pdb and then use `set_trace` to set a breakpoint in this functional test. It is like inception. We are first setting a breakpoint in the Python program in order to stop it so that we can then set a breakpoint in bitcoind. I am going to do a demo in a moment. You first insert this line in the Python test that you want to inspect. Then you run that test manually, run that file. That file is going to stop at the line where you have inserted this `import pdb` statement. Then you have an interactive shell there and you can interact with the test. The test should have nodes already that are inside this test and by using `process.pid` you can get to the process of that specific node. Please remember that if you have several nodes that are being tested in say a P2P test they will be under different numbers. You will have an array with maybe five or six nodes and you have to look at the test and see which is the node that you want to attach to, that you want to look into to observe the stuff that you are interested in. We have the process ID now at this point. Now we can start lldb and then we can attach to this process ID that we have seen running there. `12345` is the example here. Then we can do whatever we want to do in there. We can set breakpoints. You will be familiar with what you are seeing because it will look just like before. You can set a breakpoint and then let that process continue. At that point maybe you expect something to happen but nothing is going to happen because the process is still stopped from the functional test. You also have to tell pdb to continue with the functional test. At that point the functional test is going to run and it should run into the breakpoint that you set before.

This is one of the functional tests. I am going to test `getblockchaininfo` again. Here is a functional test for `getblockchaininfo`. There is a specific setup in this test and I want to save myself from doing that manually. In here I would specify the line that I described before. I manually edited this Python file here, very simple. Now I will run that file from the console. It should stop at some point. Now we’ve run into that pdb breakpoint that I set a second ago. I can look here for the PID of the node. This is an array. If there are going to be several nodes that are being tested this array will have more than one object in it. This one is simple, it just has one. I will do `process.pid` and this is going to give me the PID of the process that is running in the background that is being executed by the test. I grab this PID and launch lldb. I want to attach to this node that is running there. `attach --pid 12345` We have now loaded this bitcoind process that is running in the background. Now I can set my breakpoint. `breakpoint set -name getblockchaininfo` Then I will `continue`. At this point the process is being stopped twice. Once it is stopped in Python and once it is stopped in C++ or lldb. I do `continue`. It is still stopped in Python which confused me like ten times at the beginning. Type `continue` again and now we are in that breakpoint I set. This node is being run by the functional test. If there had been a million steps before in the functional test this will be the node that went through the million steps. You can now interact with the node. This is the magic. It is a lot of steps. Unless you guys have questions now give it a try. The steps are in the document and if you get stuck anywhere let me know.

Q - You have 6000 seconds to figure out what is wrong?

A - You have 6000 seconds from the point where you start the functional test, the Python file. It is a general constraint that the testing framework sets on the functional tests. Nobody should ever want to run a functional test that takes longer than 60 seconds or an arbitrary number. We don’t want that to restrict our debugging.

Q - Does it matter which specific file it would set the `import pdb`?

A - I wanted to test `getblockchaininfo`. The functional tests are instructions on what is being run on this pdb file. Usually you will have some question about the specific state or something that happens in Bitcoin. Then I would suggest that you look for a functional test that is bringing the node into that state. Maybe you want to test mempool eviction. For that you need to have a full mempool so the cheapest transaction gets pushed out the mempool. To do that manually you would have to write a whole bunch of scripts or do a lot of typing in the console. You can look for a test that is doing exactly that for you and then you stop that test and insert the pdb stop in there and execute that test. You could also run the full functional test suite but you would have to wait longer.


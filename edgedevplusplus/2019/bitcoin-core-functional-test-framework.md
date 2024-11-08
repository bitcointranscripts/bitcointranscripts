---
title: Bitcoin Core Functional Test Framework
transcript_by: Bryan Bishop, Michael Folkson
speakers:
  - Fabian Jahr
date: 2019-09-10
tags:
  - bitcoin-core
  - developer-tools
media: https://www.youtube.com/watch?v=gr75ubfNQ20
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/bitcoin-core-functional-test-framework
---
Slides: https://telaviv2019.bitcoinedge.org/files/test-framework-in-bitcoin-core.pdf

https://twitter.com/kanzure/status/1171357556519952385

## Introduction

I am pretty sure you can tell but I am not James (Chiang). I am taking over the functional testing framework talk from James. He has already given several great talks. I took over this talk at very short notice from James. I’d like to give a hands on talk.

## Content

This is a brief introduction into the functional testing framework. I will explain what the functional testing framework actually is. Then what it is in a test that uses the functional testing framework. We will look at a short example. Then I give some additional hints.

## What are functional tests?

Where are we in Bitcoin Core right now? What are functional tests? A functional test in general is defined as a test that tests functionalities or features of software from a user’s perspective. That means you are testing the full stack. In Bitcoin it is a bit hard to define. I think you have to extend the definition from other software projects because you also have to think about the whole network. Another way of thinking about it is is that nodes that you interact with in the network are also users who are using their own node. You have to look at features from your own perspective but also from the network’s perspective. It tests the full stack. One other thing that results out of that is usually these tests are pretty slow. If you run the functional testing framework, the full functional testing suite, you will see it takes pretty long. In general they take longer than unit tests. That is why you should pay some attention to how you write the tests and how many you write. Oftentimes I see people deferring to writing functional tests because they are Python tests. That is often easier to write for some people. A hint to keep in mind.

## When do you add/edit functional tests?

When do you add or edit functional tests? Usually when you want to test for features. Features that take multiple layers of the stack. This can be almost anything in Bitcoin. It is not something where you would add or edit a functional test if you implement something new. It is when you don’t really add something new, when you do a refactoring, you don’t really change any functionality that the user sees or that the user would notice.

## Where are the files?

I talked about this yesterday in my debugging talk. You have to be aware of where you actually are. If you do any search for test files you are probably going to encounter a unit testing file instead of a functional testing file. You always have to watch the path. You need to be in the test folder but not the test folder that is under the src directory. There you find files that are following a naming scheme. You first have an area prefix and then you have the name of the test. The areas are mempool, mining, P2P, RPC, wallet. These speak for themselves. There is also a single test that has the prefix `tool_` which is testing the wallet tool functionality. This is a different executable from bitcoind. There are the interface tools which test the REST interface and the ZMQ interface. The feature prefix which just tests other full features that you can’t stick into a category with wallet, mining or mempool.

## Running tests

How are you running the tests? First of all you can run these tests directly like any other Python file by specifying the path.

`test/functional/feature_rbf.py`

This is also very helpful because you see all the `self.log.info` outputs in stdout then. But you can also run the tests through test harness and that is very helpful if you want to run all the tests in one time, the full functional test suite.

`test/functional/test_runner.py feature_rbf.py/`

Or if you want to do some pattern matching on the names. You want to run all the wallet tests.

`test/functional/test_runner.py test/functional/wallet\*`

You will not see those INFO log outputs that you might need. You can also provide several options that might be helpful for you. The one I find myself using frequently is `--trace-rpc` which is showing you in stdout all of the RPC inputs and outputs. `--nocleanup` is another one that can be quite useful. It is not cleaning up all the log files. There are also other ways to get the log files which I will show you later.

## test/test_framework/\* (selection)

What is actually in the framework? The framework is what you can find under the test_framework folder in the test folder. This is a collection of files that have helpful functionalities that help you to write a test. Everything that you might want to reuse, what a typical software framework does. I am listing a selection of files you can find in there. There are double as many files but the other ones are not so important at least for you if you are starting out right now. First there is `util.py` which has asserts and other helpful functions that you cannot really stick into a different category. Then there is the `test_framework.py` file. This is the most important file that you are going to use in every test. This implements the `BitcoinTestFramework` class and every test is a subclass of the `BitcoinTestFramework` class. We have `key.py` which has helpers for ECC math, `script.py` that has helpers for generating transaction scripts, `blocktools.py` help you to create blocks and transactions, `mininode.py` helps you with introspections and helpers for P2P connectivity.

## Documentation and logs

What is in a test? We will look at an example in a moment. I am just going to go over some things that you will see in general and are useful to follow. You will see documentation and logs in the test. You should see that every time. You will see docstrings at the beginning of every class and every important function. You will see comments and you will also see these `self.log.info()` outputs. I think it is very important that you write these not just for others but also for yourself. As you will see in the examples in a moment the function names are pretty descriptive so you can just follow the function names and see what is really going on. Oftentimes you write 20-30 lines of setup for this to get the network to the exact state that you want and it is not easy to find out what was really the intention of all the setup. It really helps to put in some logs or some comments in there to describe what you are actually doing and why you are doing it.

## Test class

You will find the test class. Usually you name the class as the name of the test. Then you subclass the `BitcoinTestFramework` and you do a couple of overrides depending on what you are going to need in the test. The two functions that are going to see overriding almost every test is one setting the `test_params` by overriding `set_test_params()`. Then you will see `run_test()` which is the implementation of the test. There are other functionalities that you can override but you can see these for yourself in the `test_framework/test_framework.py` file.

## Node calls

`self.nodes[0] .add_p2p_connection(BaseNode())`

In every test what you are going to see is calls on the nodes. You will typically have an array of nodes on `self` and then you will refer to these nodes by just giving them a number but you can also alias them if you want. Then you are going to do calls on them. These can either be helper calls or just RPC calls. RPC calls are not redefined in the functional test framework, instead they are just thrown over to the actual node that is running in the background. These are going to be regtest nodes so you can use regtest RPC commands like `generate()` for example. Other helpers that you are going to use quite often are `wait` functions e.g. `waitforblockheight()`which are going to implement simple wait functionality so you don’t have to worry about race conditions.

## P2P introspection

Another thing that you are going to need frequently is P2P introspection. Oftentimes you will have a node where you are testing something on but you want to make sure that first of all the network is synced up to that node or your node has to sync up to the network. Or just the block has been sent, stuff like that. There are a couple of ways to do this. Often you will see `sync_all()` or `sync_blocks()` which are functions that are doing a wait for you until everything is synced up. They are going to fail the test if they don’t. You can also go deeper and subclass the `P2PInterface` class and redefine hooks on this. For example `on_block()` functions that you can override and act on these events when this node or this `P2PInterface` receives a block.

## Example

I’ll show you a simple example.

https://github.com/bitcoin/bitcoin/blob/master/test/functional/rpc_blockchain.py

I like to look at `getblockchaininfo`. I hope many of you are running your own full node. If you are running your full node the first RPC command that everyone is running is `getblockchaininfo`. That’s typically what people know. We are looking here at the test file that is testing this among other RPC commands. First up here you see the docstring which is describing what this is actually testing, a bunch of RPCs. You can see the imports. It is very important we don’t do any wildcard imports. We name every class and every function that we are importing. That is something that was changed recently because there are lots of functions and classes in this test framework. It can be confusing. Make sure you follow this. Otherwise you will be yelled at by people if you want to contribute. Here we see the name of the actual test. This is a subclass of `BitcoinTestFramework` and this is overriding the `set_test_params` function. Here we are setting up a clean chain. We need one node. Then we go into the `run_test` which is the actual test. This is then calling for organizational purposes several functions that we have refactored out into their own functions. We are going to the `getblockchaininfo` function. Here we see another `self.log.info` which is showing what function we are at. We define an array of keys that we want to test for. Then this is the point where we are calling this RPC command.

`res = self.nodes[0].getblockchaininfo()`

We are getting the result. The rest of the test is some asserts on the result of this RPC call. Since we are pretty late I will keep going. You can check out all these tests for yourself. They are pretty easy to follow.

## Hints

`import pdb; pdb.set_trace()`

I will give you some hints. One thing I talked about in my other talk, debugging and logging, you can use pdb for the Python part of the functional tests for debugging. Refer to my other talk for the rest of the functionality if you want to get into debugging the bitcoind instance. Another thing that is really helpful is that you can look at all these logs with `combine_logs.py`. When your test is failing you will get a helpful last line output which gives you a line that looks like this.

`'/var/folders/9z/n7rz_6cj3bq__11k5kcrsvvm0000gn/T/bitcoin_func_test_7n eje5nv’`

You can copy and paste this line and it is going to give you an aggregated log of all the logs of all the nodes of all the RPCs you are running in the test. You can pretty easily inspect there what has been going wrong. That is very helpful and intuitive.

## Get started!

I really like to give these hands on talks because I want to encourage people to contribute. You don’t have any excuses now. You can read these two README files.

`test/README.md`

`test/functional/README.md`

There is the functional test README file but there is also the general test README file that has some information that is still relevant for the functional stuff. You can look at this example test.

`test/functional/example_test.py`

It is not really doing much. It does similar stuff to the `getblockchaininfo` test that I showed you. It has more comments. That is maybe helpful for some people. Oftentimes I find people have a hard time finding the first to do. You can go on GitHub and select the label “tests”. There are labels for open issues. When I did this slide there were 39 issues with the label “Tests”. Not all of them are going to be functional tests. I can speak from experience. My first contribution was also a functional test.

https://github.com/bitcoin/bitcoin/issues?q=is%3Aissue+is%3Aopen+label%3Atests+label%3A%22good+first+issue%22

Another way if you don’t find issues that you feel are right for you, you can help improve the test coverage. If you go to Marco’s website here you can see helpful statistics on test coverage on Bitcoin. You can go in here and look at specific files, look at code paths that are maybe not tested yet. Oftentimes this will be error cases. These can be valuable to test. Maybe you can write a test for those.

https://marcofalke.github.io/btc_cov/

## Q&A

Q - The test coverage will be referring to unit tests rather than functional tests?

A - There are two outputs here. One is just unit tests. The first one is unit tests and the other one is unit tests and functional test coverage. The second statistics are going to be everything that is not tested by any test. If you look in the functional test README there is also a way to generate your own coverage reports with the functional tests. I haven’t done that but that should be the output of coverage of the functional tests.

Q - The first test that you wrote was a functional test. I’m assuming it would be easier to write a unit test than a functional test? Perhaps the unit testing is stronger than the functional testing?

A - I have to be honest, I wasn’t looking out for it at that point. It was an issue that I had. It was a test that was flaky on MacOS. I saw then that there was an issue that was open for about a year. I wrote something so that this test is skipped in certain cases. For all the MacOS people who are developing on Bitcoin they just don’t see this test randomly failing. It is an issue that is between Python and MacOS. Bitcoin doesn’t really concern itself with that stuff. There was no better option than skip this test in this case. If you look at the [code](https://github.com/bitcoin/bitcoin/pull/16445) that I wrote for this, everyone here could have done this. It is an example. Especially if you are struggling with C++ still then looking into functional tests is a great way to learn about Bitcoin but also to get your first contribution.


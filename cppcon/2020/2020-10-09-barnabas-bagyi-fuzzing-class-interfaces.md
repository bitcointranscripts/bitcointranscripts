---
title: Fuzzing Class Interfaces for Generating and Running Tests with libFuzzer
transcript_by: Michael Folkson
tags:
  - developer-tools
speakers:
  - Barnabás Bágyi
date: 2020-10-09
media: https://www.youtube.com/watch?v=TtPXYPJ5_eE
---
Slides: https://github.com/CppCon/CppCon2020/blob/main/Presentations/fuzzing_class_interfaces_for_generating_and_running_tests_with_libfuzzer/fuzzing_class_interfaces_for_generating_and_running_tests_with_libfuzzer__barnab%C3%A1s_b%C3%A1gyi__cppcon_2020.pdf

LibFuzzer: https://llvm.org/docs/LibFuzzer.html

LibFuzzer tutorial: https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md

## Intro

Hello everyone. My name is Barnabas Bagyi. I am a C++ developer currently working at Ericsson with some previous experience in the automative industry. I will be talking about fuzzing class interfaces for generating and running tests with [libFuzzer](https://llvm.org/docs/LibFuzzer.html). This was also the topic of my Masters thesis that I recently finished. My invaluable professor and supervisor Zoltan Porkolab came up with the base idea of it.

## Overview

Before we get into it let me present the outline of what is to come. I will start by showing through an example what is missing from the current testing ecosystem and why we should not be satisfied by using only unit tests to test our classes even though they are great too. After a brief introduction of fuzzing in general and playing with a buzzer we will go through the design of using this to create a newer testing method which is meant to test our classes based on their interfaces only. Then we will finish off seeing the results we’ve achieved with this interface fuzzer in two brief case studies.

## Let’s follow the design and testing of a (container) class

Let’s start by following the design and testing of a container class and see where it takes us.

## The (simplified) container vision

Let’s suppose that we would like to implement a double ended queue similar to `std::deque`. This container works by having vectors of static size arrays, one vector in fact, and if it needs to grow in either direction it can increase the size of the main vector.

This is how the interface of set class looks like. It is not templated for the sake of simplicity. We have our `push_back` and `pop_back` methods. We can query the element on the back. We can also do the same things on the front as well. We of course can also access the number of elements currently contained within.

## Example Unit Test Case

Now let’s pretend that we finish the implementation of the class and are very eager to test it out. Let’s see if it works or not. What we would do is write unit tests for it just like the one on the screen. I have used Google Test for the sake of this example but I imagine all unit test frameworks to be quite similar. This test is great because we are only testing a small part of the software in isolation. This makes it far easier to find the root cause of an issue if we encounter any. One very important observation for the sake of this talk is the structure of the unit test. It is practically a list of method calls with state essentials in between them. But the million dollar question when it comes to unit tests is when to stop testing. How many test cases are enough? Maybe we should try similar for the front methods as well and that’s it.

## Possible undetected bugs

Of course that wouldn’t be enough. There are a lot of possible undedicated bugs which we need to care about. In the following slides I have drawn the arrays to have only 3 elements but in reality they tend to have 16 or so. The main vulnerability of this container is the management of the arrays contained within the vector. Or maybe creating one is done well but when we have to destruct an array we somehow fail. We cause a memory leak. Or it is also possible that after the destruction of any array we leave the object in an invalid state. That might be only discovered after recreating the previous destructed array leading to a crash for example. What’s particularly hideous about this case is that covering it gives us zero additional lines of code coverage. It is very easy to forget about.

## Too many states

We see that white box testing is very hard. Let’s try the black box approach where we don’t care about the implementation. How can we proceed after a queue is constructed? First we have 3 methods we can use, we have 3 legal options. Because the queue is empty we either increase it to one or we just query the size of it. If we decide to call a `push_front` the number of possibilities explode showing 7 new ones. Here we have lots of possibilities. Maybe we call `pop_front`, we return to the `deque` having zero elements and having 3 different options again. But if we call a `push_back` again it reveals the same 7 possibilities like before. What we can observe from this tree is that the number of total paths that we can take is exponential with regards to the number of method calls we would like to do. This practically means that exhaustive testing is impossible. We simply cannot possibly test all the method combinations above a certain amount of calls. There is just too much.

Another thing which complicates it is that we still need to pay attention to the preconditions. We can’t exhaustively test every single combination. We have to care about the method calls being legal as well. Black box testing exhaustively is not very feasible and white box testing is not ideal because at least in my experience most bugs arise from situations the developers don’t think of. But if a situation does not come to mind how would I include it in the test case? This is why white box testing is not enough. My supervisor has a great saying that I really like. That’s “The difference between monkeys and programmers is that monkeys know when they should be using tools.” He tries to convince me and everyone else to be a bit more like monkeys and try using tools when you need to. For this tool we should first agree on a set of requirements that the tool needs to fulfill in order to help us with our problem. A disclaimer. Let me mention again that I am not trying to say that unit tests are not worth doing. I am saying that we would need to supplement them with something.

## What we would need

What we would need is something to combat the exponential growth that we face. A good idea might be automatic test generation. With automatic test generation we could test way more test cases than manually. Of course we still couldn’t test all of them, far from it. But it would still be far more. We could generate test cases like this with two `push_back`, one after the other. Or we could generate a `push_back` and a `pop_front` afterwards. Or a `pop_front` and a `push_back`. If we are trying to generate test cases based on the interface of the class by itself `pop_front` looks legal because we have no idea when we can call `pop_front`. The interface does not really contain at least from a C++ language sense it doesn’t. But of course we shouldn’t be ok with it. It is not a valid test case. It is a waste of time to run it.

A second good requirement would be filtering out invalid method calls. How would we want to use this tool? A great way of using it would be to just run random unit tests for example while the CI/CD machine is idle. Let’s not rest it too much. Being able to generate a test case and then run it right afterwards seems a quite sane requirement. We should add it to the list. On the other hand we would also like to be able to persist test cases. Maybe we run this test case discovery for a long time. We find a great amount of good test cases, we would want to persist it later. If a new commit comes we can just rerun the same test for regression testing. This is another thing that we would want to keep in mind. But of course we don’t want to save literally every single test case that the automatic generation creates. That would be simply way too much, a waste of space on the computer. That’s mostly because these are automatically generated test cases, it doesn’t matter how smart the generation is, there would be some redundant test cases like the two on the slide right now. Both of them are only calling the `size` method on an empty container. The `size method` is also a constant method. We expect it to not change the container’s state. Persisting only one of them would be ideal. Of course we can choose to persist the smaller one. But all of this means nothing if we are just generating the same 3 or 4 test cases all the time. We are not even calling some methods. We want to achieve a high combined coverage. And now comes the question, what kinds of issues would we like to catch. Of course finding crashes is great. It is relatively easy to find them because if we run them they crash. It is a great identification of an error. But it would be great if we could detect other things, other undefined behavior or even logical errors as well. Those who are familiar with fuzzing might realize that it fits most of the criteria that we established. We will go to a slide in a minute to see that I’m not lying about it but first let’s quickly refresh our knowledge about fuzzing.

## What is this fuzzing?

https://diyhpl.us/wiki/transcripts/cppcon/2017/2017-10-11-kostya-serebryany-fuzzing/

If you would like to see a talk focused on fuzzing only I recommend the [one](https://diyhpl.us/wiki/transcripts/cppcon/2017/2017-10-11-kostya-serebryany-fuzzing/ at the bottom of the slide.

## Fuzzing in general

Let’s see how a general template of a fuzzer looks like. The main act of fuzzing is done by the fuzzer engine. What this fuzzer engine does is generate a string which is used an argument to the test subject, the target function. This is the function that fuzzing is meant to test. If the function is run and the function fails we can raise the error. We can see that we’ve caught a bug. But if it does not fail, the fuzzer engine can just retry with a newly generated string. Although this method may look quite simplistic it is a great method. It is time proven, it has found thousands of crashes in reputable repositories.

## LLVM/Clang libFuzzer

The fuzzer engine that I have decided to use is LLVM/Clang libFuzzer. Let me highlight the differences between the general engine and the fuzzer. First of all libFuzzer maintains a test case set which is called the Corpus. The Corpus consists of only test cases that were deemed interesting by libFuzzer. We can think of interesting as something revealing new coverage. But it can also mean other things like leading to a new result. libFuzzer does not generate the string absolutely randomly. It uses the previously generated strings and combines them with different mutation algorithms. The reason being that interesting test cases more likely will combine into new interesting test cases. libFuzzer uses this function that the user has to define as a target. Of course we can call our own target function from it so it is not a big difference. If the fuzzing fails we raise an error in the same way as we would in a general engine. But if we do not find an error we store the previous string if it was interesting into the Corpus and then retry.

## Fuzzing example

Let’s see libFuzzer in action. Here our fuzzing target first checks whether the received string is at least two characters long and then indexes into them. After that it also indexes into a third character without checking the newer size requirements. That sounds like a bug. If the comparison holds we have a nested crash where we somehow index into a new pointer thinking that it is an array of at least size 5. Now what we have to do to use libFuzzer is we only have to `-fsanitize=fuzzer` as a compile (clang) argument. We didn’t even declare a `main` function but that is totally fine since libFuzzer will link its own `main` together with our binary automatically. This `main` is what implements the libFuzzer engine and we repeatedly call our target function. After running the binary we can see the segmentation fault on address 4 which most likely corresponds to the inner most issue within our code, the new pointer reference.

## Clang Sanitizers

Kostya Serebryany on “Sanitize your C++ code”: https://www.youtube.com/watch?v=V2_80g0eOMc

This is not all that clang can give to us. Clang also has other useful tools that we can use namely sanitizers. Sanitizers are compiler built in error detectors with relatively small runtime cost. Relatively meaning between 2 and 6 times the runtime increase per sanitizer enabled. There are multiple different sanitizers available. Let’s see which ones. `AddressSanitizer` checks things like use-after-free and double-free. `MemorySanitizer` mostly cares about uninitialized reads. `UndefinedBehaviorSanitizer` detects overflows, divide by zero and a number of other undefined behaviors that we may encounter. Lastly `ThreadSanitizer` is all about finding data races. This can be turned on by enumerating the sanitizer with commas between. After the `-fsanitize` flag.

`clang -g -fsanitize=fuzzer,memory target.cpp`

One thing to keep in mind is that address and memory sanitizer both try to hijack the location functions and so they are not compatible with each other. If you would like some additional information on sanitizers I recommend checking out the [talk](https://www.youtube.com/watch?v=V2_80g0eOMc) at the bottom of the slide.

## Fuzzing example - UBSanitizer

Now after discussing the sanitizers let’s read the error message on the previous fuzzing example a bit more carefully. The UBSanitizer was the sanitizer that caught the segmentation fault. We can see that is what it says on the bottom of the slide. But I didn’t include it in the `-fsanitize` flag so what is happening here? What is happening here is that it is included by default with libFuzzer. That’s the secret. Let’s see whether we can actually catch the first bug in our code, the part when we are not checking whether the data is at least 3 characters long. As you can see MemorySanitizer is the sanitizer for checking uses of uninitialized values and it indeed does catch the bug. This is great. These are perfect tools that we can use to supplement our vision.

## What we would need (again)

So let’s get back to this slide as I promised. Now we can verify that fuzzing indeed does generate test cases automatically. Of course the second point (filtering out invalid method calls) does not really make sense when it comes to fuzzing. Fuzzing is all about testing string interfaces. It has no concept of method calls at all. Fuzzing runs test cases on the fly, every single fuzzer as far as I know. libFuzzer maintains the Corpus as a directory on the filesystem so persisting test cases is also taken care of. libFuzzer also has the ability of rerunning tests from a previously generated Corpus. Filtering redundant test cases is also done by libFuzzer by simply not even saving them onto the Corpus directory. Of course the fuzzer also can achieve great coverage, as I already mentioned fuzzing is a great tool for that. What about finding more things than just crashes? We’ve seen that sanitizers work with libFuzzer so we can find more than just crashes but logical errors seem a bit our of reach for fuzzing. Even still fuzzing seems pretty great. It fits most of our criteria, let’s try to adapt it.

## How does fuzzing help us? We won’t be testing just string interfaces

But how? Because fuzzing is for string interfaces and we don’t have that. What should we do?

## Transforming libFuzzer to an Interface Fuzzer

This is how fuzzing looks like. What we have to do is sometimes take the string and transform it into something which we can use to test the fuzzed class. What we have to do is somehow interpret the generated fuzzed string as a method call list. Afterwards we can just call the method call list one after the other on the fuzzed class. Of course we would have reflection, it would be a great candidate for implementing something like this. If we could somehow query the methods that the class has and then use it afterwards. But reflection is pretty far away at the moment, at least as far as I know. Instead what we have to do is use some user code to generate an interface description. Now what the interpreter can do is use that interface description to interpret the string and generate the method call list in the end.

## Interface Description

What do I mean by interface description? First of all I implemented the prototype of this outline tool which has the name `Autotest`. I am not exactly sold on it but this is what came to mind first. This is how the interface description looks. I have chosen snake_case for user code and PascalCase, camelCase for the library itself to easier differentiate what we have to do and what is already written for us. What we can see is that the interface description is just a bunch of method names one after the other. Some of them have `CONST_FUN`  macros, some of them only have a `FUN` macro. If you ever use Google Mock it may look quite familiar to you. Does it actually convey all the information that we need? Of course it shows us that we have `size` which is a constant function, we have `pop_back` which is not a constant function. This is not enough. We have to be able to define the preconditions. Otherwise how can we know which one we can call with an empty container?

Here what we can do is define lambda which signifies that the object is not empty. It takes the constant reference of the object and returns whether it is empty or not quite easily. This lambda or any other factor taking the reference of a class and returning a bool can be used to define the precondition of a method. This is great. Now we’ve fuzzed the place where we would like to call invalid methods because we can define every single precondition that we would have like this. But the other problem is that how should we know that `push_back` has arguments? For that I have created a definition for “argument placeholder” which is holds the place for an argument. The interface description is complete. Now we can move onto the next part, the interpretation part, with the generated… on the right. What this table does is maps integers to the methods of the class. This is very important for us.

## Interpreting the Generated Strings

How does the interpretation actually work? Let’s suppose that we get the data shown here from the fuzzer as a fuzzed string. What we would do is take the first byte of it, interpret it as the ordinal number of the method to be called and then we call that method. The number zero was `size`. The number 6 is `push_front`. We have a problem here because it needs an argument. It had an argument placeholder defined which symbolized an integer. What we could try to do is take the next 4 bytes within the string, interpret it as an integer, of course assuming an integer is 32 bits at the moment, and we can use that result as a parameter. We can continue this process with 1 being `d.back`. Now there are a lot of edge cases here. We can have an integer that is too big as a method ordinal number. What if we get 121 at the first byte of the data generated? What if we have only 1 byte remaining and we want to generate an integer for an argument of a previous method that is just now being called? Of course these are things that we can reasonably work through. We can just write some code and handle these edge cases. But the great thing is we don’t really have to because libFuzzer has the utilities that we need here.

## libFuzzers FuzzedDataProvider

Namely what I am talking about is `FuzzedDataProvider`. This class is defined specifically for consuming the first string and interpreting it as different bytes. In this example shown, first it is used to generate an integer between 0 and 255 as the age of a person. Why I’ve specifically chosen this example is that the data that it is trying to generate fits in one byte. The range from 0 to 255 fits in one byte. Even though we are generating an integer `FuzzedDataProvider` is smart and realizes that the range we want to cover only needs one byte. It only eats one byte from the input. This is not all that it can do. It can also pick values from an array. It can generate floating point numbers, it can generate fixed or random size strings from a bigger string, a substring if you will. This is a neat tool in my opinion. Its flexibility and ease of use is the reason why I’ve implemented argument placeholders as functions taking a reference of FuzzedDataProvider and returning an instance of the type that we want to place hold for. This means that it can be easily extended by anyone if a type that your method might take is not supported by default by the auto test library.

## Crashes are not Enough

We are at the place where we can safely generate test cases which have only valid method calls and roughly look like those on the slide right now. But are we satisfied? What if we have bugs that are not revealed by crashes? Of course we have sanitizers but something catching actual logical errors might also be great.

## Invariants

What we can take to try to help us with this problem is invariants. An invariant is a condition which is always true as long as the object is in a valid state. It should be true from the construction of the object until the destruction of it. A method on the interface of the class can always expect it to be true when it runs and even if the invariant might be broken while the method runs, it must hold once the method returns again. How can we use this invariant to easily check for logical errors? We already observed that unit tests are method calls with state insertions in between. On the left we have the unit test example from the start of my talk. What we can do is take the generated test case and inject invariant checks between each method call that we have. It seems easy enough and might actually work. But of course even though it looks great sadly it is not as strong as manual assertions in unit tests. Of course we have no chance of replacing unit tests. We can only add another tool to the testing toolkit that we have.

## Let’s put it to the test

So let’s put it to the test. Let’s see how this method actually performs.

## Case Study 1: Simplified Deque

The first data structure I have tested it on is a single-ended deque. It is a single ended variant of the data structure I introduced at the start of the presentation although it is simplified to be way easier to implement. The main issues are the same as the ones we had with the actual deque class. It still has to manage a growing vector of arrays which can be a real source of problems. Autotest manages to consistently achieve 100 percent code coverage within seconds on this class. We can see the interface of the class on this slide. It is fairly similar to the standard interface. It has only one end and it is templated. It has some trickier methods like a universal reference in `emplace_back`.

This is how all the test code looks like. This is every single character that I had to write for testing this class, this container that I’ve written. First let’s see whether the container is empty. Afterwards we have an enumeration of the methods just like we have seen before. We have `emplace_back` which has the placeholder for an integral argument which is of type `int`. We have `pop_back` which requires the container not to be empty. We have `back` which also requires the container not to be empty both in constant and in non-constant forms. And we have a `size` method. I was pretty happy about how it turned out.

## Case Study 2: Robin-hood Hash Map

The second example is a bit more complicated. I have chosen a state of the art hash map implementation which is one of the fastest ones according to the measurements that I’ve seen. A Robin-hood hash map is a header only library which is over 2000 lines long. When I started fuzzing, it didn’t have a satisfying result. It was fluctuating between 88 percent and 93 percent code coverage reached within a minute. I wasn’t really happy about this fluctuation. After some investigation what I found is that the 5 percent code which was only hit sometimes needed the container to be really, really big. What I did was I fine-tuned the fuzzing parameters. Thankfully for libFuzzer, how much the maximum length of a generated string rose with the amount of time that libFuzzer is running, can be customized. I modified the value to grow faster and after that it managed to hit 93 percent coverage all the time. After that I assumed the remaining 7 percent, maybe we can do something else to reach that too, but I found that it wasn’t really possible because all of it was explicitly instantiated template functions and a few lines of code which needed the container to be obscenely large. I was fine with not hitting any of that.

I ultimately broke the implementation of the hash map test into two parts. This first part is the setup. Here the argument placeholders are defined which we will use in the second slide. We can see that it has a `to_res` which will be used to resize and rehash the container to have a size between 1 and 10,000. The `integralRange` on the right is defined as a function taking the start and finish of the range, and returning a function taking a fuzz data provider which will return the actual generated integer that we want to use there. `to_res` is just an argument placeholder. This stands for everything else in the slide. All three things are just argument placeholders. `randomString` is also implemented the same way. In `key_val` what we can see is an actual custom return argument placeholder when we use preexisting placeholders, namely `randomString` and combine them to create a random string pair, which is the `robin_hood` pair, not `std` pair.

Now what we can do with these argument placeholders is we can declare methods like this. This is pretty boring, exactly the same as it was in the previous slide only with different methods. We have an `insert` which takes a pair of strings and inserts the key value pair into the map. We also have `emplace` where we construct the pair `emplace`. We also have `count` which counts the keys, `contains` which checks whether the key is in there and so on. I am not listing the amount of user code that was necessary to implement this interface fuzzing as a user. It is very, very small. I am happy how it turned out from an interface standpoint to be honest. Even though I couldn’t leave out these `AUTOTEST` mock rules which I tried really hard but didn’t succeed.

## Summary

So let’s sum up what happened in the last 40 minutes. We encountered a problem of not having mass testing tools. The solution we tried was adapting existing fuzzing methodology. To do this we first created a way to describe the interface of the class that we want to test. Afterwards we interpreted the fuzz string as a method list and excluded the invalid test cases from it. We then executed the interpreted test case. What is great about this solution is that it works well with the same sanitizers that libFuzzer can be used with. The first results of the prototype seem pretty promising. These were the ones I mentioned in the case study section. If you would like to take a look at this prototype feel free to look at it on my [GitLab](https://gitlab.com/wilzegers/autotest/).

## Future work

The question is where to go from here. A great idea would be to test it on non-container classes which might pose additional challenges with the argument values meaning more than in the case of the containers. Of course this prototype, while it seems to work well enough, also needs a pretty big refactoring because I am really hoping that nobody will look at the code itself. The most important future work I have right now is to answer any questions you may have about the presentation. Hopefully I will be live in a moment.


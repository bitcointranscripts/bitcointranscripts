---
title: Going Beyond Coverage-Guided Fuzzing with Structured Fuzzing
transcript_by: Michael Folkson
tags:
  - developer-tools
speakers:
  - Jonathan Metzman
date: 2019-08-07
media: https://www.youtube.com/watch?v=TtPXYPJ5_eE
---
Location: Black Hat USA 2019

Blackhat: https://www.blackhat.com/us-19/briefings/schedule/#going-beyond-coverage-guided-fuzzing-with-structured-fuzzing-16110

Slides: https://i.blackhat.com/USA-19/Wednesday/us-19-Metzman-Going-Beyond-Coverage-Guided-Fuzzing-With-Structured-Fuzzing.pdf

## Intro

Hi everyone. Thanks for coming to my talk. As I was introduced I’m Jonathan Metzman. I’m here to talk about how you can get more bugs with coverage guided fuzzing by adding structure awareness to your fuzzers.

## Unstructured Fuzzing = Magic

I first got into fuzzing while I was in college through AFL. I started using AFL to find bugs in my school projects and later I moved onto finding bugs in real software like sqlite with AFL. I was really amazed by how well AFL worked because I didn’t really know much about how AFL worked at the time. I didn’t know much about the software I was finding bugs in with AFL. But it still worked so well. I thought what could be better than this tool that gives us bugs for free?

I think the answer to that has got to be structured fuzzing, otherwise I wouldn’t be giving this talk. But unfortunately structured fuzzing doesn’t actually give you bugs for free. It forces you to think about the format that you are fuzzing. Because of that thought process and the effort you put into it you’ll end up finding more bugs. Let’s fast forward a few years to when I started working at Google. I wrote a structured fuzzer for a graphics library used in Chrome. You can see part of the header file of that fuzzer on the screen. As you can probably guess it took quite a bit of effort to write that fuzzer. I think the effort paid off in the end because the fuzzer found around ten vulnerabilities in the library that weren’t found with unstructured fuzzers like AFL. Today I want to teach you more about this technique, structured fuzzing, and convince you why it is sometimes worth it to pay more when you could pay less.

## Bio

First, a little bit about myself. I work at Google mainly on fuzzing Chrome but we also develop fuzzer tools that are used by other open source projects. One of these is called [oss-fuzz](https://github.com/google/oss-fuzz). One of the unofficial roles I’ve taken on in Chrome security is getting people to write structured fuzzers for Chrome. They have been such a big win for us there and I’m hoping today I could do the same for you and they will be a big win for you all as well.

## What is Structured Fuzzing?

Let’s define what I mean by structured fuzzing and see how it evolved. The first generation of fuzzers were completely black box. They knew nothing about the target they were fuzzing. They were also actually structure unaware which means that they knew nothing about the format that they were supposed to be mutating or generating. They were pretty rudimentary, they were similar to piping bytes from /dev/urandom to a UNIX utility, completely unaware. The next generation of fuzzers improved on the effectiveness of the first generation by being structure aware. They were still black box but this was probably based on the realization that if you are fuzzing something like a HTML renderer you are more likely to find bugs if you give it inputs that look something like HTML rather than just nonsense from /dev/urandom/. I think the current generation of fuzzers that most people are using are coverage guided and unstructured. This is the technique that AFL pioneered and sparked this fuzzing revolution that we are in currently. The reason why AFL has had such a large effect and this technique as well, is because unstructured fuzzing allows people to use it without actually understanding much about the format that they are actually fuzzing. But because it is coverage guided the fuzzer generates progressively more interesting inputs and that’s why it is actually fairly good at finding bugs. Coverage guided fuzzing is such a big advance in fuzzing that I’m going to assume we are talking about coverage guided fuzzing throughout the rest of the talk. I’m going to refer to this as unstructured fuzzing. I think the next generation of fuzzers will build off of these advances in coverage guided fuzzing but they will also be structure aware. This is what I call structured fuzzing. By being structure aware I mean things like they won’t do the general purpose mutations that AFL does on inputs. They will do format specific ones like they will delete expressions from Javascript programs, they won’t just flip bits.

## Why Structured Fuzzing?

Why use structured fuzzing? At the end of the day I think it is only worth using a new fuzzing technique if it helps you find more bugs. That is exactly what structured fuzzing can do for you. Let me first demonstrate that structured fuzzing can help you find more bugs and explain why it will help you find more bugs.

To do this I want to start by sharing a story about how structured fuzzing found bugs in sqlite that weren’t found with unstructured fuzzing. I mentioned fuzzing sqlite in the earlier slide, one of the first projects I would fuzz with AFL was sqlite. I guess that sqlite might be one of the most well fuzzed projects in the world. One of the groups that fuzzes sqlite is my team at Google. We fuzz sqlite through oss-fuzz and we’ve been doing it for years through libFuzzer and AFL. I’d say that over the years we’ve probably thrown tens of billions of test cases at sqlite that were created by AFL and libFuzzer. You would think that with all these attempts and all this time AFL and libFuzzer would have found most of the bugs in sqlite. But obviously that is not true. One of my co-workers last fall, Matthew Denton, wrote a structured fuzzer for sqlite. This fuzzer would generate SQL statements to be executed by sqlite. It immediately started finding vulnerabilities that weren’t found by AFL and libFuzzer including this heap buffer overflow that you see on the screen.

## More Bugs: The Data

That’s just an anecdote. We actually have data to support the use of structured fuzzing as well. In Chrome probably around 50 vulnerabilities have been found using structured fuzzing in the past two years. Some of these were cases like the previous one where there was an unstructured fuzzer and then the structured fuzzer beat the unstructured fuzzer in finding bugs. But actually there are other cases where structured fuzzing allowed a researcher to fuzz code that they couldn’t fuzz with unstructured fuzzing. I will explain more about how that works later on. Although I will only be discussing structured fuzzing in the context of libFuzzer today it is worth noting that outside of this context there is a lot of data to support the use of structured fuzzing as well. I think the most notable of these is [syzkaller](https://github.com/google/syzkaller) which for those of you who haven’t heard of it is a structured fuzzing framework for the Linux kernel that has found over a thousand vulnerabilities in just the past couple of years.

## Fuzz Where (you think) the Bugs are

Why does structured fuzzing help you find more bugs? There are many reasons but I think they all really boil down to the fact that structured fuzzing gives you the researcher more power to fuzz what you want. It lets you fuzz where you think the bugs are going to be.

Levels of Fuzzing: https://blog.regehr.org/archives/1039

Let’s see how this compares to unstructured fuzzing at a high level. If we are fuzzing something like V8 which is Chrome’s Javascript engine there is a range of possible places where bugs can occur. On one end of the spectrum you’ve got bugs like parser bugs and on the other end you have things like JIT miscompiles where you have to run Javascript code to trigger those bugs. What an unstructured fuzzer like AFL would do if you were using it to fuzz V8 is it would take Javascript programs and it would pick random bytes in those programs and change them to arbitrary values. If we have an `else` keyword in our program AFL might do something like add a zero in the middle of our `else` keyword (`el0se`). This is going to fail parsing. `el0se` is not valid Javascript code anymore. This is the problem with using unstructured fuzzing sometimes. So many of the test cases are going to fail parsing that while you might have an easy time finding these parser bugs you are going to have a much harder time finding these bugs that exist higher up the stack, at a higher level of abstraction. To focus on finding these bugs that live at this higher level of abstraction with structured fuzzing we can constrain our input so that all of our inputs to the target obey certain constraints. With the structured fuzzer we can make it so that every test case we create is syntactically valid Javascript. We can be sure that all of these end up getting executed. This is what I mean by fuzzing where you think bugs are. You are basically focusing the fuzzer’s efforts on a certain subspace of the range of possible inputs that you think is most likely to trigger bugs. It is also worth nothing that in V8 in particular and I think it is true for most programs, most bugs tend to live at these higher levels of abstraction and not just at the parsing level. By doing this we are really finding more bugs.

Another way that controlling your input space with structured fuzzing can help with fuzzing efficiency is you can avoid fuzzing certain code that makes it harder to find bugs. Recently I was writing a structured fuzzer that produced Javascript code. One of the problems this fuzzer had was that it immediately started producing infinite loops. We don’t want to execute infinite loops when we are fuzzing a Javascript engine like V8 because it is a huge waste of time. We’ll never be able to reach code that comes after the infinite loop. Instead we will just keep trying the same thing over and over again expecting to find a bug. The simple solution with structured fuzzing is constraining the input space so that now instead of just generating syntactically valid Javascript I am only going to generate syntactically valid Javascript where every loop is bounded. This obviously solves the infinite loop problem that we have. You can apply this to other sorts of issues you might face when fuzzing. You could do the same to ensure that your Javascript code doesn’t throw any uncaught exceptions for example.

I think the real power with structured fuzzing is not in avoiding fuzzing certain things but it is in making the fuzzer cover code that you want to be tested and you want to find bugs in. A good example of this was a fuzzer that I was recently writing for pdfium, which is Chrome’s pdf reader. The way I wrote this fuzzer was I would run the fuzzer for a little bit and then generate a coverage report using Clang’s coverage tools and see what code wasn’t being covered. As you can see on this slide there is a coverage report that shows that pdfium’s barcode feature isn’t being covered at all. There is a simple reason for this. It is because I had no idea that pdfs actually support barcodes, that is a feature that I have. Apparently that is a thing. The solution here was to expand the input space to get the fuzzer to produce pdfs that contain barcodes. Then I ran another coverage report afterwards and confirmed that I’m indeed covering the code I wanted to cover, the barcode feature. This workflow is something you only really get with structured fuzzing. With an unstructured fuzzer you could sort of get it by giving seed inputs and hoping that it can derive similar inputs from there. But it is not a tight feedback loop like you have here. Here with structured fuzzing you are almost becoming part of the fuzzer where you see code that isn’t being covered and you make a decision whether you think it is worth covering that code. Then you make the fuzzer cover that code. That’s a point I want to emphasize here. We are making a trade-off with structured fuzzing where we are trading some of our time and effort in order to find more bugs. You’ll have to decide if you think it is worth covering one feature or another feature. Or covering a feature more thoroughly. Or maybe you can get bugs more cheaply by teaching the fuzzer about another feature. You’ll notice I’m not covering the barcode feature fully in this second coverage report and that’s because I’ve decided that I could probably get more bugs by teaching the fuzzer about a new feature. I have already gotten bugs out of this barcode thing I did.

## Going Beyond an Array of Bytes

Ned Williamson on Attacking Chrome IPC: https://media.ccc.de/v/35c3-9579-attacking_chrome_ipc

The last way I’m going to cover that structured fuzzing can help you fuzz where you think bugs are is structured fuzzing can make it easier to fuzz code that doesn’t just accept an array of bytes. A good example of this that I want to use to illustrate this point is a fuzzer written by a co-worker of mine, Ned Williamson. This fuzzer was for a Chrome feature that had a number of APIs that the fuzzer was trying to find bugs in. You’ll notice that none of these APIs just accept a blob of bytes like unstructured fuzzers produce. There is also no place in Chrome where you can just shove in a blob of bytes and get these functions exercised. So what the fuzzer did was it structured each of its inputs so that each input represented a function call to make and the arguments to pass to those functions. Obviously this input can’t be directly used in fuzzing. There is nothing in Chrome that understands what this means. So the fuzzer had to interpret these inputs. If the input is telling me to call `DoRequest` I am going to call `DoRequest` and pass in the specified arguments.

## Why Structured Fuzzing?

To summarize why you should use structured fuzzing, you should use it because it will help you find more bugs. It can help you find more bugs because it gives you the researcher more power into fuzzing what you want. Also because it allows you to fuzz more things. In particular it allows you to fuzz code that doesn’t accept an array of bytes.

## How?

Now that I am done selling structured fuzzing to you all I want to give you very practical advice on how you can write a structured fuzzer. I’ll cover three techniques that you can use for writing a structured fuzzer with libFuzzer. libFuzzer for those of you who don’t know is a coverage guided fuzzer much like AFL. It is probably the main fuzzer that we use in Chrome and OSS-Fuzz.

## Custom Mutators

The first way you can write a structured fuzzer with libFuzzer is by defining a libFuzzer custom mutator. These work pretty much as you might expect. You simply define this function and libFuzzer when mutating test cases will call this function to mutate test cases rather than its default mutator. So if we’re fuzzing Javascript instead of using the default mutator to do stupid things like bit flipping libFuzzer will call your custom mutator that can do things like parse the Javascript, build and do intelligent mutations. It is a lot of work but this technique is pretty powerful.

## Libprotobuf-mutator

There is an easier way though and that’s where libprotobuf-mutator comes in. libprotobuf-mutator will handle mutation for you and you only have to work around there. Let me explain what I mean here. libprotobuf-mutator is a custom mutator for protobuf, just like the custom mutators we just discussed. Protobuf is a data format like JSON but with types. What can you do, the insight here is that you can use protobuf to define a spec or schema for the inputs you want libFuzzer to mutate. If you see on the slide we have an `AddExpression` defined in protobuf. In this simple case we’ll have two operands that are both integers but protobuf is rich enough that you can make each operand an int or a float or another expression even. It gives you the tools that you probably want from this case. libprotobuf-mutator will then create a test case based on the spec for you. As we see here we’ve got two operands, 10 and 9. That’s basically exactly what we intended. We saw before you can’t feed this to anything unless it accepts protobuf. It is not useful for fuzzing something like V8. What we do is we have our interpreter for this and our interpreter will just convert from this intermediate format into the target format Javascript. It will take both operands, convert them to strings and add a plus sign in between them. libprotobuf-mutator is extremely effective. All of the fuzzers that I’ve covered today have used this technique. This includes everything from… to the AppCache fuzzer. The AppCache fuzzer was used in an exploit that had a sandbox escape and everything. Completely owning Chrome with the vulnerability found by the AppCache fuzzer. The libprotobuf-mutator was again used by co-worker Ned to find the vulnerability in the iOS kernel that was used in the iOS 12.2 jailbreak. You can use it to find some pretty nice bugs. It is a technique that I would recommend in most cases for writing a structured fuzzer.

## Converting to a LibFuzzer Custom Mutator

The last option you have is one that is a pretty exciting area for future work. I don’t have fantastic results from it so far. I’ll just explain it and give some tips on how you might be able to do it. Imagine you have a black box fuzzer, something like a Python script that can mutate HTML files that you then feed to Chrome and try to get crashes. You could convert this into a libFuzzer custom mutator to add the power of the coverage guided fuzzing to this black box fuzzer that you have. Some of the challenges that you might encounter when doing this that you might have to overcome. If you imagine how this fuzzer works, you’ll have a corpus of test cases and your fuzzer will pick one at random, mutate it and that gets fed to your target. If it were a custom mutator what would happen is pretty much the same but there is a last step at the end where the test case will be added back to the corpus. This could present a problem for some fuzzers because they can’t actually mutate their own outputs sometimes. They are not used to being run in a loop. I was recently converting a font mutator into a libFuzzer custom mutator. The problem there was this font mutator would parse what it expected to be semi valid fonts, mutate them and then feed to the target. Once it was mutated it sometimes wouldn’t be able to parse those mutated outputs again. In that case you could just fall back to the libFuzzer’s default mutator or maybe even improve your mutator. The other problem you might have to overcome is that sometimes these tools aren’t written to be fast enough to run in this coverage guided fuzzing loop. Coverage guided fuzzing works best when it is quick. You might need to improve the speed there. The final thing you might need to work on is the fact that many of these mutators are written in languages other than C++. To call it from a custom mutator you need to use whatever language the fuzzer is written in. It probably has some interface like maybe JNI for calling that code from C++.

## How: Three Options

To summarize how you can write a structured fuzzer using libFuzzer, your first option is to use a libFuzzer custom mutator. The second option, the one I recommend in most cases, is to use libprotobuf-mutator. The third thing you can do which is pretty exciting is taking an existing black box fuzzer you have and converting it to a libFuzzer custom mutator to get the power of coverage guided fuzzing added to your fuzzer.

## Conclusion

To summarize what we went over in this talk. You should use structured fuzzing because it will help you find more bugs. More bugs is really the bottom line here. To write a structured fuzzer with libFuzzer you can use either libFuzzer’s custom mutator feature or libprotobuf-mutator.

## Links

I have some links at the end of the slides if anyone wants to check the slides afterwards and do further reading. I’ll take questions now if anyone has them.

Structure-Aware Fuzzing with libFuzzer: https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md

libprotobuf-mutator: https://github.com/google/libprotobuf-mutator

Fuzzing sqlite: https://source.chromium.org/chromium/chromium/src/+/master:third_party/sqlite/fuzz/?q=sqlite%20fuzzer&ss=chromium

## Q&A

Q - You talk about writing new fuzzers from scratch. Last year there was a fuzzer released which does all this. Are you aware of afl-smart?

A - I have heard of afl-smart. I skimmed the paper, it seemed to me that it was a similar idea to libprotobuf-mutator. You are defining a schema.

Q - You define the files where you have the grammar and you also have all of the advantages of afl with the speed and efficiency. You can make it structure aware by defining the grammar by yourself. You pay by investing time in defining grammar but it has really good results in real life.

A - I am a bit familiar with the work. I know the people who did it produced pretty good work on afl. I was pretty impressed with the results and I think it is pretty comparable to libprotobuf-mutator.

Q - I was curious if you were using it?

A - We are not using it but I’m currently exploring ways to view this better. That is definitely one of the things I am going to be looking at. Protobuf wasn’t designed for making fuzzer grammar. I think the fact that protobuf might not have all these features might be a good thing. The conversion and interpreting, you have unlimited power. Everyone knows how to write C++ already so you don’t need to learn a new format to write these effectively. I’m definitely going to be taking a look at that.

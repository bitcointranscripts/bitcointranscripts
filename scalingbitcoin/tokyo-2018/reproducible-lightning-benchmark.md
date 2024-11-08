---
title: Reproducible Lightning Benchmark
transcript_by: Bryan Bishop
tags:
  - lightning
  - developer-tools
speakers:
  - Nicolas Dorier
---
<https://github.com/dgarage/LightningBenchmarks>

<https://twitter.com/kanzure/status/1048760545699016705>

# Introduction

Thanks for the introduction, Jameson. I feel like a rock star now. So yeah, I won't introduce myself. I call myself a code monkey the reason is that a lot of the talks in scaling bitcoin can surprise people but I understood very few of them. The reason is that I am more of an application developer. Basically, I try to understand a lot of the talks but if it's too complex then I just wait until some crypto guy makes a proof-of-concept, then I just make something in C# that other people can use.

This talk is about doing different technologies that developers are using to try to make it more easy to get a benchmark. It turns out that I did it for a specific need on lightning. Maybe it will give a good idea for other projects. As you see, there's a link to my github page, it's not a paper. I was quite surprised I was accepted to Scaling Bitcoin, because I had no paper. It's about this talk.

# Lightning network performance

I was asked to tell you about lightning performance. Actually, it's a very wide question. I tried to reformulate it a little bit. How fast can Alice pay Bob? How fast can Alice pay Bob through Carol? How fast Alices can pay Bob? These various scenario questions. There's also the scalability in terms of users. I think there was a calculation from Tadge Dryja about 15 million people using lightning assuming they have like 2 channels per year or something. I tried to narrow down the questions.

I found some quick numbers for c-lightning like 34 payments/second for Alice-Bob, and if I add Carol then it dropped to 12 payments/second, and then it dropped a little bit for the other scenario. It was not really that interesting, "he can process 34 payments/second"... These numbers are mostly irrelevant. It's irrelevant, but it might be interesting to developers. Most people don't care about how fast the peers can pay each other. But it might be interesting for some specific needs like lightning network implementers and services relying on micropayments. It's nice to have something you could quickly pop up and check the numbers. In the future, I hope we will see micropayment services. Right now everything is focused on mirroring what already exists like get an invoice then pay the invoice. I think lightning unlocks potential applications for micropayments, like paying microsatoshis or satoshis every few seconds. I am hoping one of these services will appear at some point, technically speaking it's not impossible.

The routing problem might not be relevant for micropayments because you can directly talk with the node you're paying without having the routing problems.

# Reframing the objective

It can still be interesting. I tried to reframe the objective. Let's try to make a framework for benchmarking things more easily and have a way to reproduce the results. Really, it's messy right now for benchmarks. We make a piece of code, we open an issue, we put printf everywhere in the code, then we remove printf in the code later. Nobody knows about performance instrumentation tools and they just do it manually instead. And people just ask for benchmark numbers and then they are happy, but really it needs to be reproducible and testable.

# Reproducible benchmarks

I tried to simplify it a little bit. There are two types of things I want to consider- the bench producer and the bench reproducer. You create code to make the benchmark, and then the reproducer can replay the benchmark. You get a number of artifacts rom the bench producer, and the reproducer can get the benchmark and then runs it exactly the same way on his machine.

I glued docker, git and dotnet together. I'll go into more detail about that. The basic idea is that your benchmark should be easily-- if you want to create a benchmark, you clone the benchmark repository, you create your own branch, if you want to create a benchmark on c-lightning then you modify the code of c-lightning and you have a code for publishing this docker image or building this docker image on your local machine. After this, you can run the benchmark. I'm really relying on docker. As a benchmark producer, you create an image, then oyu push it, and then you run the benchmark.

Because it's docker, it means that publishing the result is as easy as pushing the image you created and pushing the branch with your benchmark. From a reproduction perspective, just pull the repo, checkout the branch, run the command, and then analyze the results.

By doing this, I found some small bugs in c-lightning.

There's a script called run.sh, when you have a script, you can run run.sh which you can run. The way it is working is it just runs your code. The red and blue types like your own code that you can customize yourself. It's doing the-- generating a docker-compose file, running the docker-compose command, setting up your environment, and for your test you have four Alices that connect to one Bob and then you create the docker environment corresponding to that topology. Your benchmark will run after the containers are initialized. It will run a few hundred times and record the results.

I call docker-compose from my source code to setup the test environment and configure docker-compose.

I also have a concurrency parameter, and then multiple benchmarks can be parameterized and run multiple times with different values for the concurrency parameter. Each time, it runs 100 times, and each run it does 100 payments for this particular case.

I have a docker-compose template for actors in yaml.

Once you run it, there are many charts that are generated that try to help you to make sense of what's going on. Once I did that, by chance I found a bug in the c-lightning code. The more payments there are, the longer it takes to make a new payment.



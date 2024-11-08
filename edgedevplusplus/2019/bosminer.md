---
title: Challenges of developing bOSminer from scratch in Rust
transcript_by: Bryan Bishop
tags:
  - mining
speakers:
  - Jan Čapek
media: https://www.youtube.com/watch?v=hqxuWFpQlqY
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/bosminer
---
<https://braiins-os.org/>

<https://twitter.com/kanzure/status/1171331418716278785>

notes from slides: <https://docs.google.com/document/d/1ETKx8qfml2GOn_CBXhe9IZzjSv9VnXLGYfQb3nD3N4w/edit?usp=sharing>

# Introduction

Good morning everyone. My task is to talk about the challenges we faced while we were implementing a replacement for the cgminer software. We're doing it in rust. Essentially, I would like to cover a little bit of the history and to give some credit to ck for his hard work.

# cgminer

cgminer used to be a CPU miner that has been functionally removed a long time ago. It was open-source, you could run it on your own machine. The next stage of evolving cgminer was when GPU mining stepped in. We started to see a little bit of disappearing of the open-source parts of the miner. It was still a miner, but a driver for specific GPU hardware. Each GPU had special pieces of GPU kernel that someone would develop, and only sometimes they would be open-source. You were pretty much stuck with whatever it was.

The next evolution of cgminer history was that people started to use FPGAs to mine bitcoin. This was similar to the GPU times where different people were developing different bitstreams to do sha256 and find blocks. There were some people doing open-source, and some people weren't.

Then ASICs happened. These devices are embedded devices so basically they have an architecture where, you have a control board running some form of linux as manufacturers usually do. Then there's some hashing boards hashboards that do the bitcoin mining work. Usually the CPU that is running on the control board also has an FPGA part. So something like, you saw in the previous slide, like FPGA mining. But in this case, the FPGA is being used to drive the hashboards doing the real-time part. Sometimes it's challenging to feed the chips with new mining work at the right times. So you can write some small code for the FPGA to do that. The operating system on the control board is just making sure there's enough work or jobs for the FPGA. Manufacturers started shifting logic out of cgminer into the FPGA on their board.

A very specific example is the well-known ASICboost for Antminer s9 where the FPGA was between the CPU and the hasboards, in order to enable the asicboost functionality. The manufacturer was basically not allowing us to use the asicboost because the code in the controller was intentionally wrong. It wasn't documented. You had the cgminer sources; it wouldn't do anything though- it would just generate bad solutions. Then the control board is running something else that isn't that interesting.

We need an FPGA and a microcontroller to drive hashboards these days. The cgminer became a pile of code that is a stupid frontend for the FPGAs. There are some mining devices without FPGAs and they are trying to drive the hashboards with UART. But the question is, are they open-source too?

Coming back to the ASIC architecture, it also turns out that at this point you don't need-- or the cgminer itself isn't enough to run the whole system because it's running some linux. So you need drivers, bootloaders, etc., to run it. These are also closed source, usually. Even if the manufacturer says they're complying with the GPL, well if you go collect the pieces, it's pretty hard to get this running as a full system image.

# Lack of open-source today

The lack of open-source today, and things like Antbleed miner backdoors, not being able to use asicboost, etc. Let's do something about this. Obviously the problem is that we have different kinds of mining devices but the manufacturers usually take the cgminers and they would not publish their changes back which is also a violation of the GPL. There was a tweet from someone who said he got uninterested in cgminer development when he found out that manufacturers wouldn't contribute. There's all sorts of different formatting and batching, it's just not possible to have a single codebase for all the hardware devices. But we should have it, right? When we want to run a full node, you go with Bitcoin Core which represents the bitcoin full node. If you want to build an embedded device based on Linux, you go to kernel.org and download linux. But there's no single source for getting source code and building a mining device.

So we started the braiins firmware for mining devices. We decided to write our software in rust. I wanted to share a few experiences about this.

# Why rust?

Why did we decide to go with rust? We had some experience with embedded development. The situation is not entirely pleasant when dealing with limited resources on these small chips. Even in cgminer, there's a lot of race conditions and it's just buggy. It basically runs by accident or good timing. You can try to debug cgminer, but you just can't do it. It has specific timing issues, and if you don't, then it crashes.

We chose rust because of its memory safety properties. Usually there's a saying that, if it compiles in rust, then it runs and it's correct. So you really want to focus on your logical bugs, you don't want to spend your time on segfaults and race conditions. The compiler just won't let you produce something with race conditions. This was a challenge to write rust initially, but it pays off.

The second reason why we chose rust is because of the wonderful ecosystem. I don't think there's a compiled language for a strongly typed language today that has no runtime. That's an important thing. Rust has no runtime, no virtual machine doing memory management. Everything is statically compiled. It's much more lightweight than C++. It's very suitable for embedded devices.

At the same time, with rust, if something compiles for a device, then chances are that you can reuse that component on the server side. That's great, right? We just don't want to duplicate code. Why would I reimplement the protocol on both ends? I want to share one code base for the host and the embedded code base, for testing but also production.

The rust packaging system allows you to use different versions of the same package at the same time. In the C or C++ development world, like libtool and all this old mess-- can you do that? I don't think I would be able to easily run two versions of the same library in my compiled image.

Last but not least, the rust suite comes with a nice test harness. Developers don't like to write tests. Are there any test cases in the current cgminers that the manufacturers would contribute? I want to run "make test" and make sure my device does what it's supposed to do; but no, they don't do that.

I was contacted about a year ago by a manufacturer-- they asked us, could we provide them with a special mining node so that they can do testing and manufacturing? I asked them, why don't you run the tests with the connectivity? You don't need to connect your miners to the pool, you can make them work on dummy jobs or something. You want to have solid testbase in your project, and that's also what you get with rust.

Lastly, it's beautiful. There are companies already out there, like Microsoft, Amazon and others, who are heavily investing in development of rust. We thought it would be a good idea to choose a technology that has some future. Also, we're lazy and we really want to do code reuse.

# Hiring rust developers

The first challenge was finding people who would be knowledgeable in rust or would be willing to learn with rust. We also tried finding people who would be interested. We're based in Czech Republic. There's not that many rust developers there. It's growing and people are interested, and if someone wants to be present in the industry and wants to be developing software using some typed language like rust does, there's-- but--- ... So we basically built a team in-house from people who were just interested in rust. It took 2-3 months to be able to say that we're productive enough in the codebase in terms of generating lines of code.

# Multi-threading vs async

Designing the software, unless you do some hello world thing, you come to the point where you have to divide your computation into tasks. You have two ways, usually. You either have to do multi-threading or you can write async co-routines. Multi-threading is well established in the industry. Usually you have libraries to create threads and synchronize them. This codebase is very solid in rust. However, multi-threading doesn't scale if you're receiving many requests on your network, and having a lot of threads slows you down because it's a full task in the operating system sharing the address space. It becomes very heavy. With the async approach, we have people around from nodejs and it's easier to find developers that think in terms of async programming. You have n tasks you're mapping to n threads. This is done somewhere in the background by the run time. If you choose the right runtime suitable for your application, then I think the async approach pays off in the long run. There's one drawback to the async part, which is that it's invasive to your software design. Once you start using async, it contaminates everything and protrudes through the layers. So you have to be ready for that, and you have to rethink some parts of the design.

The challenge was that at the time we made the decision, rust was not quite there yet with the async framework and all this stuff.

<https://areweasyncyet.rs/>

This website summarizes the current state of current rsync nightly-- it's v1.39, already, it's almost async. There's a few things missing. If you want to design an interface, it's called a trait. If some of the methods of the interface are async, then this is not possible in rust today. This is one of the limitations. This limits your design patterns. But the standard library already matured enough, all the async keywords are stable. So we thought it was a good idea to take the async path.

# Architecture

At the top, you see the mining pool. Then there's some frontend for the mining pool. There's something that persists mining jobs, feeding the work to the backend, and then give it to the hardware, and then the hashboards. We also have a box here for stratum v2. "Mining work" is the thing that the hardware is able to understand. Technically the firmware on the Antminer s9 is translating stratum v1 json into some binary that the hashboard understands. Why would you put such logic into a hardware controller? You could always just intercept the wires and see what's going on, so I'm not sure why they decided to do it that way.

The whole architecture is just a bunch of plumbing. In rust, it's channels. You're sending objects, and you're receiving objects back. You have to start thinking about this design pattern. You have two components that need to talk with each other. If the component is shared by multiple other components, then you can't just do an API where you need to do locking. Bloating your code with locks is doable, but you want to think in the real-time way. In real-time applications, you have channels that connecting your tasks, and the task workers wait for something to arrive. It's nothing surprising, just a common way to do it.

# Challenge: rust on hardware devices

We wanted to make sure we could easily compile to an ARM board. Cross-compiling environments will do this. This is really well supported in the rust ecosystem. You install your compiler, and then you install your target backend. In case your target backend is somewhat exotic, or doesn't have a C library, then you can define your own target and it will work well with the whole ecosystem because now the packaging system is able to--- for...

The second hcallenge is that when you do an embedded application, you usually have IO pins that are memory mapped and you want to access those pins in a safe way. There's a guy who writes blogs on rust and how to do it in the valid domain in a safe way. While researching what he was working on, we discovered ther was a tool called svd-to-rust. SVD is a standard from the ARM embedded processors community, which defines the registers. Any manufacturer that produces such a chip should produce an SVD file, which is a hardware descriptor of your chip. With this SVD file, it's usually recognized by different IDEs. We were able to define our own SVD for our FPGA as well. We were able to generate safe rust code that allows accessing registers.

Well, what's so challenging about accessing registers? You want to be safe, even at the bit level. You want to make sure that your application can't access reserved bits in the IO registers.

At some stage, these hardware devices are running linux. You have to have some source of interrupts. Writing kernel drivers is probably not the right way. It's kind of overkill. You just pipe your FPGA part to drive the hashboards, and you just want to get some notifications. In linux framework, there's userIO and there's a rust binding for this interface. Unfortunately, the UIO interface is not async. This is going to be a very common pattern that you'll run across; you find a good library and it's not async.

There are two ways to deal with this. With the async approach, you can always have a runtime framework which you usually have to use to run the whole async application, which can dedicate specific threads for the parts of your application that are not async. For this specific case where we needed to do the UIO, we actually went the UIO thing, and we have implemented an async extension because we think it's beneficial for the whole ecosystem.

# Other challenges

When you're new to the rust ecosystem, you basically feel that the amount of packages available since they are centralized on craits.io, you can't decide which ones to use or which ones are the best or the most standard. We made a few decisions in this area. This might also change.

First, the first thing you're going to face is logging. Doing logs right is a challenge. Doing them in an async way is challenging. Doing them in a structured way is challenging. We found a framework called s-log which fulfills all of these criteria.

The other issue you want to deal with is error handling. This is still an open issue. There's a lot of development in rust for error handling. The standard library has some approach, obviously, to deal with errors, but it's not very comfortable. We found two crates.

We found a bitcoin-hashes library was useful. It is stable and mature.

You also need to communicate on the network level with some serialization framework. Currently the standard in rust is called stardev which either allows you to use existing backends and formats like json, or you can write your own backends. Very comfortable. The only limitation is that you're mapping your own model... into... and then, stardust's model. The problem is that if your model has types that are not easily mappable into the stardust model, then you're going to hit a wall a little bit but there are ways around it.

The last and important thing is to choose an async framework. The standard is really tokio. But the problem is that latest tokio is not compatible with latest rust. They made a new alpha a few weeks ago with rust async support. Tokio is using other crates like m.io that does the abstraction for your operating system and when you talk with specific devices. Tokio is open-source. Everything here, these crates are all open-source. I'm just talking about, what are other people in the ecosystem choosing?

# More challenges

We're running the rust code on the ARM CPU. We have some FPGA part running a really lightweight driver to talk to the hashboards. The rust is just feeding this part with the work, not jobs.

# Timeline of moving from cgminer to bosminer

bOSminer, startum v2 simulator, ii-stratum-proxy.  We wrote a startum simulator and can simulate a pool and a mining device. We're planning to add a proxy as well. We want to simulate different scenarois where you are trying to translate between various protocols. ii-stratum-proxy is a simple proxy written in rust to translate stratum v2 to stratum v1 so that you can connect the miners to an actual pool.

# Demo time

Let's see if we can do a demo. Unfortunately, the university is filtering stratum. I tried 3333. Maybe it's doing that for a good reason.

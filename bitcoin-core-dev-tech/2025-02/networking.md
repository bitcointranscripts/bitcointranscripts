---
title: "Low Level Networking"
tags: ['bitcoin-core', 'p2p']
date: 2025-02-27
---

## context

Httpserver and p2p code have different event handling loops, p2p event handling
lives in cconman, and http event handling uses libevent.

vasild opens pr to split the higher level p2p logic in cconmann and the
event/sockets handling into sockman

Because libevent lacks support for unix sockets and that's needed for stratum
v2, pinheadmz has been evaluating dropping the libevent dependency from
httpserver, and has recently been investigating reusing the event handling logic
from vasild's conman sockman split,

Big open question: How to kill libevent? No great replacement? We can take on a
new dependency or ship something ourselves, pinheadmz has been rewriting from
scratch

Wanted unix sockets for jsonrpc for stratum v2 but not supported by libbevent,
but it doesn't support and is not maintained, pinheadmz wrote http server from
scratch that reuses sockman handling, and performance is just bad, tried using
flamegraphs to measure the issue....

The nice thing about libevent is how cross platform the api's it supports.

## Summary of multi-plexing io

Generally for sockets and files you can do async or sync, e.g. tcp you are
sending a bunch of data, like 1gb 64k at tim, every call to write is blocking,
using call that returns how many bytes were written, tight loop sending over and
over.

All mechanisms of doing async sending/receiving are platform-specific, no
generic way of finding out that a socket is ready.

Generic multiplex mechanisms:

### select

select for windows is kind of dumb, b/c every  loop you have to add the sockets
to the wait list again, so you have to iterate through a map every time.

The way `select` works is you have a tight loop where you first let the os know
which sockets you're interested in, call `select` passing this setup structure,
select will wake up or timeout and then you iterate through the list again to
see why you woke up, handle it and repeat. By default, only 1024 handles are
allowed.

- heres all the sockets im interested, wanna know which are ready to
  write/read/error
- call select, pass structure with all sockets
- either wake up or timeout
- iterate through the list again to see WHY you woke up
- has hard limit of fiel descriptors

### poll

In poll you create a list of things you want to watch and it creates on entry
per thing you want to watch.

### platform specific

epoll for linux, kqueue for bsd's, windows has two, an old one, problem with
these platform specific ones is that they are version dependent, so very hard to
use, one can google "can epoll be used safely" to find funny rants that prove
there is no way to use epoll that is guaranteed bc of the number of states being
too difficult to enumerate.

Epoll is supposed to allow you to have multiple waiting threads e.g. 1k peers,
10 worker threads servicing 10% of peers, not something we do but something we
could do.

Would be nice, but too challenging to use these api's correctly on our own.

What we could do on our networking layer is, e.g. check what's available and try
to use platform-specific api's that are most performant, and no we have
reimplemented libevent, and it's going to suck, because we don't have the long
tail of 20 years of bugs, so really uncommon to implement this yourself.

Big libs are libevent, libev, and libuv, and most projects use one of those,
presenter is of the opinion that attempting to reuse our own socket code is a
bad idea because it's not great code and it's tailored to all of our old use
cases and not necessarily our future ones, it would be ideal to replace with one
of the implementations that's maintained and well-implemented.

sockman is very opinionated, operated on these old consturcts (select,
single-thread etc)

### Questions

1. How to replace libevent for our httpserver,
    - One participant points out that http server has two parts:
        - Libevent event loop handling
        - and http server implementation, which we don't care about most of. So
    maybe do the http part on our own, and reuse sockman

2. How can we have generic socket handling code?

Big wins we could have with something more modern, io_uring on linux, it has two
circular buffers and there are few necesarry copy ops, kernel hands you mapped
memory that is atomic,  command queue and a memory buffer, zero copy operations
and zero context switch operations, this would massively improve performance in
our P2P code, presenter would rather do the sockman implementation the nicest
way the first time around, C++-26 includes functionality that encapsulates these
interfaces easily, and is io_uring paradigm compatible. alternative is switching
depency to libev or libuv.

In the past boost was future C++ staging ground, now nvidia has a c++20
implementation of this C++26 execution api, that we could plug in now and switch
to the standard interface later.

https://github.com/NVIDIA/stdexec

Before libevent, httpserver used boost async io interface, we are going in
circles which is kind of funny.

Rocksdb people experimenting with io_uring for multithreaded reading from disk,
just to demonstrate how parallelizable the IO model of io_uring.

Someone else said that the io_uring paradigm is generic enough to fit all io,
submission queue and data queue which are atomic and shared between kernelspace
and userspace so zero copy and context switching ops.

Also, if you look io_uring wikipedia, 60% of kernel vulns in the last couple
years have come from it, is this inehrent, or part of the complexity of
implementing?

Some suggestion that our use case is pretty simple and we won't hit the complex
edge cases of io_uring.

## Should net processing be multi threaded?

One participant suggested that our networking code has to modify some global
state, and that is inherent, and we could not benefit much from multithreaded.

We have two threads, network thread that does sending and receiving between us
and kernel of buffers, and the net_processing thread that processes these
buffers and modifies our state.

## conclusion

A number of participants are of the view that httpserver and p2p event handling
are different enough that we shouldn't reuse.

Someone says that we should just do select and poll based event handling in both
and forced to have some duplicate stuff in sockman and our http server.

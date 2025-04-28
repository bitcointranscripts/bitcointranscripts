---
title: Experimental Binaries
tags:
  - bitcoin-core
  - build-system
date: 2025-02-27
---

Multiprocess / IPC / Stratum V2 could be a good candidate for an experimental
binary

These are experimental features and perhaps releasing experimental features in
non-experimental binaries is what we are after. Disabled by a flag.

To be hosted on our website bitcoincore.org it must be guix buildable.

Auto-update is not a feature that would be considered allowable as an
experimental feature. The experimental thing has to fit with our existing
security expectations.

The experimental binaries can be another guix target.

With multiprocess, other projects can make their own experimental projects by
just downloading and talking to bitcoind over a socket.

Is it ok that the experimental binary has code and features that haven’t had the
same amount of scrutiny as the normal binaries. There has to be some thought
into how this is communicated.

The experimental binaries could be deployed in a subdirectory of the main
binaries.

Should we ship things that we know don't work correctly? Will most likely
involve a judgement call.

A risk is that some people like miners might start relying on the experimental
binaries and if the experimental feature fails this might cause problems when we
pull the binary. Although the feeling is that miners are very risk averse and
will most likely not run experimental binaries.

Experimental binaries break the cycle of chicken and egg of big new features
like Stratum V2.

For mutli-process the process would be to move libmultiprocess from depends into
a subtree and enable guix to build it.

For the new QML based frontend, at least at first, it could bundle bitcoind and
ship it’s own binaries to get initial feedback. This would both allow feedback
on the UI itself but also it would be a consumer of the IPC interface of
multiprocess and so validate that.

If we want people to test these features, we need to have people be able to
download it. Undecided if the experimental binaries are in the same tar ball or
not.

There were not many objections to experimental binaries but there were questions
on how much they would be trusted, especially by miners and also worry that they
might get relied upon as it can be hard to take back something once it’s
released.

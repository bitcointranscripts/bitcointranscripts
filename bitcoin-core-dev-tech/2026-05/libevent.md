---
title: Libevent Session
tags:
  - bitcoin-core
  - networking
date: 2026-05-08
---

Transcript #1

Issue: https://github.com/bitcoin/bitcoin/issues/31194

CI failures: known issue.
CLI #34342: replace libevent with http server.
diff between PRs?
this adds a server to the CLI
which goes first? no conflict, doesn't matter.
CLI is smaller.
the way it is now, fine if both are merged, and include removal of
libevent in release,
imagine there's overlap, but its not that important.

doublecheck what expectations are for the C interface?
do not expose RPC publicly
it used to be black and white, rest could be exposed but read only
then rpc whitelisting, still unsafe for internet
previously, easily crash libevent, 10 years old.

implementing our own HTTP server if goal is not public.
REST exposed is still problematic

good reviews happening! almost there.

need to check that things that depend on core don't crash (LND)

***

Transcript #2

Issue: https://github.com/bitcoin/bitcoin/issues/31194

- zipkin working on it for ~2 years. initial PRs were refactors
  removing smaller usages.
- biggest effort is replacing the HTTP server in
  https://github.com/bitcoin/bitcoin/pull/35182. Look for backstory in
  old PR - #32061, it was 100 comments and hard to keep track of.
- there's a lite HTTP client in
  https://github.com/bitcoin/bitcoin/pull/34342 for using libevent in
  CLI. The initial approach was by filling in/using headers from zipkin
  PR but no good solution on how it was shared (1/3rd code shared) but
  didn't like how it looked.
- CLI looks more realistic that it goes in first and now they are
  independent. Didn't want it to be blocked on the server PR. would be
  fine with both merged. Unify header handling in the next release.

- comments: HTTP client + server - there gotta be some overlap.
  surprised that CLI is using libevent

- people's expectation on RPC interface? do not expose RPC publicly.
  put it behind nginx.
  - you can drain the wallet/stop node - you need to whitelist.
- REST is not safe for the internet either.
  - REST interface = a few years ago you could crash it when exposing
    it to internet.
  - Send invalid hash and it would crash. It's been fixed.
  - Not designed for exposing it to the internet.
- libevent - from 5 or 6 years ago, you can do a couple of 100 requests
  and crash it. There's a fix for it but it never got released in
  libevent even though they merged it. implementing your own HTTP server
  is doable is if it's not public.

- both are getting good reviews. next release version merge hopefully.
- full removal - fanquake's PR is a minor cleanup. will automatically go
  in. already in a pretty good place.
- zipkin is doing lot of downstream testing

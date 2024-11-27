---
title: Multi_index Replacement
tags:
  - bitcoin-core
date: 2024-10-17
additional_resources:
  - title: 'tmi: Tiny Multi-Index'
    url: https://github.com/theuni/tmi/
---
Mostly looking for concept ACKs/NACKs

Q: Why would anyone be opposed?
A: Boost pretty much just works and we'd be replacing it with something custom and untested.
Follow-up Q: But is there any reason to believe that our testing/fuzzing would be insufficient?
A: Nope.
Q: What is the status?
A: A full drop-in replacement for the subset of boost has been written. It currently passes all tests and meets or beats our existing benchmarks.

Current repo is unreadable/unreviewable, but is sufficient as a drop-in replacement for boost: [https://github.com/theuni/tmi/](https://github.com/theuni/tmi/). Please don’t bother with code-review or testing yet. It’s a POC and it’s ugly.

Q: How many lines of code?
A: Somewhere around 3500. Roughly matches the number of *headers* that boost requires for multi_index (not a joke). Boost was written a long time ago, modern c++ makes the metaprogramming much simpler.

General consensus: Dislike for Boost, agree with removal goal, no NACKs.

Main concerns at this point: Should I follow the boost api? Or should we invent our own? And if using the boost api, does the whole thing need to be implemented?

Q: What would be the benefit of rolling our own?
A: Certain optimizations are possible if we loosen some restrictions that we don't require (iterator validity, erase return type, etc). I've also been asking around "what do you wish boost::multi_index could do but currently can't, and a few feature requests so far would require diverging from the api.

Comment: It would make testing/benching/comparing much easier to stick with the api. It would make sense to stick with it initially, then maybe diverge once more confident. No need to implement complex features we don’t use, they could be added piecemeal in the future.

General agreement with the above.

Ok, I was mostly looking for opposition and I'm not finding much.
Moving forward I'll continue to stick with the subset of boost that we use, which will allow us to do 1:1 tests and benchmarks.

Output:
Next step is to do a major cleanup for readability and documentation, and start on a test/benchmark suite. Thanks for the input!

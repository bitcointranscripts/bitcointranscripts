---
title: Kernel
tags:
  - bitcoin-core
  - build-system
date: 2024-04-10
---
The kernel project is just about done with its first stage (separating the validation logic into a separate library), so a discussion about the second stage of the project, giving the library a usable external API was held. Arguments around two questions were collected and briefly debated.

1. Should a C API for the kernel library be developed with the goal of eventually shipping with releases?
    - There are a bunch of tools that can translate C++ headers, but they have
    downsides due to the name mangling. This especially makes dynamic loading of
    a C++ library hard, so having a C header is easier and therefore preferable,
    even though it requires a translation layer to the existing C++ code.
2. Should we introduce tools using the kernel?
    - A reindex tool using the kernel seems useful and falls more in line with other projects that ship separate database salvage/utility tools
    - A reindexer for discovering keys of silent payment wallets would be nice too
    - A separate benchmark binary for the kernel also seems useful and could be a way to get more type safe languages into the repository. It would also be useful to have a benchmark to gauge the overhead of using the API vs using the internal kernel interface within node code. Could also potentially show inefficient translation routines.
    - Generally there seems to be some curiosity of what these tools could achieve, and judgement on whether they should live within the repository / be shipped can be given at a later point in time.

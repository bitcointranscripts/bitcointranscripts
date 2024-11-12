---
title: Flamegraphs
tags:
  - bitcoin-core
  - developer-tools
date: 2024-10-17
additional_resources:
  - title: 'Updated version of the flamegraph guide'
    url: https://github.com/davidgumberg/prnotes/blob/master/profiling/flamegraphs.md
---
Demo'ed a new (~4 years old) script available in the Linux kernel's perf tool
for easily recording and generating flamegraphs in a single shot. (`perf script
flamegraph`) The main interest of the demo was to show how easy and low overhead
flamegraph recording is using the perf tool now, and to show some of the small
configuration issues / gotchas in setting up with bitcoin core, namely compiling
with `-fno-omit-frame-pointer`, and getting an html template dependency on
Debian. Working on an updated version of the flamegraph guide we link to in the
developer notes.
([https://github.com/davidgumberg/prnotes/blob/master/profiling/flamegraphs.md](https://github.com/davidgumberg/prnotes/blob/master/profiling/flamegraphs.md))

One advantage of this script compared to the traditional method of doing a perf
recording and then using the `flamegraph.pl` script to generate a flamegraph
from this recording, is that we can record extremely long running processes
(>48h) and the output is a `flamegraph.html` that is under 20MiB instead of a
more than 100 GiB perf recording that takes hours to convert.

One attendee asked whether stack tracing was being done for our dependencies,
and I did not have a good answer, and realized that absence of samples in
dependencies was a shortcoming of the method I was using to generate
flamegraphs, this can probably be solved by passing the same "-fno-omit-pointer"
when building from the `deps` folder, but further investigation is needed.

Another attendee asked whether this method could be used for generating short
recordings of already running processes and I demonstrated how this can be done,
they suggested that it might be useful to occasionally grab short flamegraph
profiles in monitoring tools.

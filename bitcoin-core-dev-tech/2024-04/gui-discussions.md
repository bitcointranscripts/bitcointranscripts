---
title: GUI Discussions
tags:
  - bitcoin-core
  - ux
date: 2024-04-10
---
## QML GUI

[Slides](https://github.com/kouloumos/bitcointranscripts/blob/temp_core_dev_slides/bitcoin-core-dev-tech/2024-04/files/2024-04-gui-qml-berlin-coredev.pdf)

Q&A

* Current GUI and QML progress seems slow?
* Code review / build system involvement? Will there be a test suite?
    * Test suite yes, No fuzzing planned
* Why not RPC based?
    * RPC not currently capable of building this UI on top of
* Is there a QML dependency graph?
    * More dependencies required for sure
    * May have to abandon depends approach
* Blocking calls historically an issue
    * A consideration, but more to talk about here

## Integrated GUI Cost/Benefit

[Slides](https://github.com/kouloumos/bitcointranscripts/blob/temp_core_dev_slides/bitcoin-core-dev-tech/2024-04/files/2024-04-CoreDev-integrated-gui.pdf)

Discussion

* If other wallets and GUIs are having issues building on Core, we should address that
    * Dog fooding within the current GUI could be a good way to discover that as opposed to Core GUI having privileged access
    * Sparrow, Specter are not trying to be Bitcoin Core GUIs they are external wallets.
* Discussions about nuances around Bitcoin Core GUI frontend vs being a wallet frontend
* Core GUI is mostly wallet, few node UI features
* Considerations of additional work for the build system contributors
* Examples of the project’s toolchain bumps being held back by qt, dependencies
    * QML potentially worse. C++20 problem for android
    * If you have a GUI at all, there will be dependencies
* Maybe use Bitcoin Core master as a github sub tree project dependency
    * Separate release schedules between GUI and Core
        * Do most users run on Window/Mac + GUI or Linux variants?
            * If GUI users then separate release processes, that might hold up new network features
    * Or, could pull in Core build via guix build processes
    * Is making Bitcoin Core a dependency of the GUI a good idea?

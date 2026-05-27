---
title: QML GUI Update
tags:
  - bitcoin-core
  - gui
  - qml
date: 2026-05-05
---

- A lot has been done in the QML GUI after a break
  - Possible to release as a full replacement to the previous GUI
    - Could be potentially done by release 0.33
  - Roughly 110 items to complete
    - Smaller and more advanced features
    - Build features
  - Every main feature has parody
  - Some features have a chance to be implemented properly the second
    time around
  - Could be implemented in the current guix scripts
  - June should have unsigned builds posted at bitcoin core app website
    for testing
  - A full replacement would be available thereafter
  - Getting into the next round of design
  - Big reason for productivity is because of AI
    - LLMs are great at QML
    - Figma to screens are easier than ever
    - Ask agent to compare actual to target screenshot
      - Only a few rounds to converge
  - Desktop feels second class to the mobile
    - Two screens are problematic: settings and transaction history
    - Another round to do those improvements
  - Is there any incremental PRs that can be done?
    - Separate repository at first
    - When there is a massive PR it will have already been "pre reviewed"
      in separate repository
  - Removing C++ models, then QT subdirectory
  - Two GUIs in parallel probably not possible
  - Static builds do not use entire QT framework
    - There are dozens of sub-models
    - Downloaded and built separately
  - QT5 -> QT6
    - No extra dependencies
  - Support for wayland requires openGL
  - Some work to separate GUI and non-GUI guix prefix
    - Considered as a separate project
    - Even now there is a single guix prefix for building and signing
      but they do not need to be combined
  - There is a project board with 110 items to check out

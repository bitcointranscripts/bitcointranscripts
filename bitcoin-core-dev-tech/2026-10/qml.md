---
title: QML GUI
tags:
  - bitcoin-core
date: 2026-10-13
---

## Project status and the staging branch

Let’s talk about the state of QML first.

We have a preview app at [bitcoincore.app](https://bitcoincore.app). It builds from our latest development branch, and we have been getting great feedback.

The main thing I want feedback on is the tracking issue, specifically the staging branch. We currently have two parallel tracks.

In the `gui-qml` project, the `qt6` branch has all the latest development, but it contains about 1,600 commits. We cannot simply merge that. There is a lot of noise and code churn.

That is how the original Qt implementation was merged.

It was a different time. One of the worst consequences is that `git blame` is not useful for understanding that original code.

We are rebuilding the history in the staging branch, compressing it into perhaps 40–50 commits. The tracking issue provides a map. We are working on the development branch and filling out that map. Once all nine chunks are in place, the staging branch will have all the core features, and we can move toward submitting the work.

During the staging process, we will have both the existing Qt GUI and the QML GUI, until we get to the end.

## Test coverage

Test coverage is a major focus. We currently have about 40,000 lines of code and 45,000 lines of tests. Every new feature comes with tests, and every bug fix comes with regression tests.

**Why does it need so much test code?**

There are three kinds of tests, arranged roughly as a testing pyramid.

At the bottom are unit tests, with full unit-test coverage for the module. Then there are integration tests that run a mock node and test the QML layer. There are also integration tests that run the node inside the process.

The QML layer implements the GUI and has its own engine. It can run independently of the C++ interaction, so we have a layer of tests specifically for GUI behavior.

There is also a test bridge, configured to run only on regtest, that exposes an RPC port. It gives the tests access to the QML engine so they can inspect the UI state and perform end-to-end validation against the release binary.

For those tests, we will target basic, representative user scenarios. We will also cover things that need multiple processes, such as interactions with peers, and directory or platform-specific behavior.

We do not want to use end-to-end tests too much. They are complicated and harder to maintain. They should cover things that really need that interaction, but the capability is there.

To return to the question of why there are so many tests: I see it the other way around. Existing Bitcoin Core tests can touch very large amounts of code.

**How much of this is testing actual GUI code?**

It is very intentionally GUI code.

**Things like directory handling are already tested by the utility code.**

We have onboarding features that load and check directories, as well as loading dialogs. The GUI also has custom settings processing and uses particular directories. We need to test that the GUI represents and handles those things as intended.

Core already tests the low-level processing. These tests are for the custom GUI behavior, not for retesting Bitcoin Core functionality. The concern is valid, but the tests are intentional.

## Test stability and Qt compatibility

**How stable is walking through the QML document? Is it something like traversing an HTML document?**

QML testing is inherently multithreaded, so there is some nondeterminism. We try to make the tests as event-driven as possible, rather than relying on timing.

There is also the question of selectors: how you reference an element, whether by identifier or coordinates. The tests use a view with a tree-based hierarchy. That structure is stable.

**Does it change between QML versions?**

No, those are internal identifiers.

We maintain compatibility across a range of Qt versions, starting with Qt 6.2. There are a couple of places where we use different code paths to support that range.

QML is essentially a large tree of objects, and you can query the whole tree.

## Size and scope of the integration

**How big is stage one?**

Just six commits, and those should probably be collapsed a little.

The complete staging branch will contain a larger series of commits: roughly 90,000 lines, about half of which are tests. It is organized into chunks, but the eventual pull request to Bitcoin Core will be a single PR.

**Are there changes elsewhere that reviewers should watch for—for example, in validation?**

We have very intentionally made no changes below the interfaces.

The final commit removes the current Qt GUI subdirectory.

**Is there a reason to remove it?**

We do not want to maintain two GUIs.

**Could that be abrupt?**

We will communicate it more publicly. With support extending two versions back, users will have a few versions available during the transition.

## Review and feature parity

**What sort of review are you looking for?**

All kinds of feedback are welcome: code structure, design, and so on.

**Do we need to do design review now?**

We will be opinionated about the design.

**What about feature parity?**

We are nearly there, except for some edge cases, such as creating an empty wallet and perhaps exporting watch-only wallets.

We estimate feature parity at more than 92%. It is extremely close. Just because a feature is not in the staging branch does not mean we are not going to implement it. We intend to close the gap enough to be satisfactory.

We took screenshots of every screen in the existing Qt GUI and compared them with the QML GUI, so we have a basis for assessing parity.

## Why rebuild the history?

**What is the purpose of the staging chunks? I thought those were how you planned to submit the work to Core.**

The chunks are a mental map of how to build up the application: foundations, settings, onboarding, node functionality, and then wallet functionality.

The final PR is an atomic swap. The staging branch is our internal focal point.

About a year ago, we faced the question of how to move from Qt 5 to Qt 6. We chose the simple approach of using the main repository as a subtree. That is why the `qt6` development branch is not directly mergeable into the main repository, and why we need the staging branch. It lets us rewrite the commit history into something more reviewable.

That process has been useful. It has made us revisit earlier decisions. For example, if we implemented something and improved it later, we can squash those changes together.

Review of the main PR should focus on high-level questions: have we resolved main-thread blocking, are the build and CI packages right, and are the tests free of flakiness?

**Have you consulted others about the test framework and how it runs within the functional test framework?**

We have received advice not to overload the end-to-end tests.

## GUI demonstration

We have three tabs: Activity, Send, and Receive. There is a pending section for transactions that are in flight and not yet confirmed.

*[A demonstration followed. The source notes do not capture its full contents.]*

## Accessibility and the design workflow

**What about screen readers and accessibility?**

We need to spend some time on that.

There is a group of users we should make sure we continue to support.

One related topic, perhaps outside the scope of this conversation, is the designers’ workflow. They work with sketches in Figma and have their own documented standards: standard elements, how to combine them, and how to keep the GUI consistent over time.

**What is the workflow for adding something to the new GUI? Does that process still need to be worked out?**

The ideal approach is to involve designers, work from a Figma sketch, and then implement that in Core.

They have their own GitHub repository and issues. We need to work together.

Large changes are relatively rare, so the process might be somewhat ad hoc. For smaller changes, one suggestion was to use an LLM with existing elements as a reference.

## External signers, appearance, and transaction display

**Is external-signer support still available?**

Yes, it is under Settings. It needs a proper home.

**Should it be part of onboarding?**

That is good feedback. It probably deserves an onboarding page.

Another useful property is that QML and Qt Quick are designed for both desktop and mobile systems. If we reintroduce mobile support, the framework can adapt to it.

**Is light mode supported?**

Yes.

**Why are some entries in Activity gray and others white?**

The display distinguishes cases such as replaced transactions, UTXO splits, self-sends, and consolidations.

**Is the logic for identifying those transactions already in Core?**

We add transaction-processing logic for that. Our transaction processing is somewhat complex.

## Where new GUI work should go

**If I want to make a GUI change now, should I make it in the current GUI?**

Focus on the new one.

**How far along is packaging for macOS, Windows, and Linux? Is it integrated into Guix builds?**

Yes, it uses the same build setup.

The staging work includes the build integration. Each chunk is verified to be buildable.

## Timeline, dependencies, and remaining work

**What is the expected timeline?**

We would like the PR to be open before the end of the year. Version 33 would be great, but that is not up to us.

**Are there blockers?**

There are no blockers as such—just work to do. There is threading work, and some test-framework work to make sure everything is aligned properly.

The main dependency concern was that QML requires additional dependencies. These are not arbitrary third-party libraries; they are additional Qt 6 modules.

The discussion mentioned GUI, networking, testing, QML, and graphical-effects modules. Some networking functionality is used for wallet-related Bitcoin URI handling—BIP 21—and it was suggested that this could potentially be replaced.

To be clear, our priorities are threading, getting the test framework into the shape we want—including moving some tests to the appropriate layer—fixing crashes and bugs, and closing the feature-parity gap.
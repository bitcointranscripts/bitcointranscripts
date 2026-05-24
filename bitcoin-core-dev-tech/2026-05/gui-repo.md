---
title: GUI Repo
tags:
  - bitcoin-core
  - gui
date: 2026-05-08
---

## Background

What was the rationale for having two separate GitHub repos?
(<https://github.com/bitcoin/bitcoin/> + <https://github.com/bitcoin-core/gui/>)

- Were we going to decouple GUI from Node?
- People who just want to focus on the GUI/non-GUI could work with less
  distraction for either side.
- Rationale was to separate issue + PR management.
- One hypothesis before it happened was that GUI review activity might increase.
- [#19071](https://github.com/bitcoin/bitcoin/pull/19071) was the issue for the
  split.

## Friction in current setup

Doesn't preclude splitting out the GUI.

Some like that it introduces friction, others do not. Some do not agree that
distinct repos leads to friction.

- Contributing has friction when you are changing files both under /qt/ and
  outside /qt/.
- Friction consists of forcing separation of wallet / rpc changes from gui for
  adding a wallet feature. GUI may only be adding something trivial like a
  checkbox.

Disagreement on whether lack of review is due to having multiple repositories.

Current setup means maintainers can forget merging to both repos.

There are many GUI issues open, why are people not reviewing them?

- Extra bit of friction
- Weird, the project has many different repos (so the situation is not that
  different from libmultiprocess)
- People subscribe to specific repos when they feel it's relevant
- Separate projects have different sets of people

Putting the cart before the horse with current approach of separate GitHub repo
but essentially the same Git repo.

Even if we have full repo/module separation we would still need stubs in the
lower level node repo for the UI.

Adding things to lower level repo would then need to justify the extension of
the interface, independent of any specific UI.

## QML future

Do we think the two mirrored repos would help once we go to QML?

Good to re-evaluate now.

Why are the current GUI contributors not on QML? Or other way.

For the wider community it seems like the focus was moved away from GUI.

Maybe we could revisit this after QML is merged?

- Possibly included in v33.
- Expecting PR to the main repo to be up before v32 but *not merged*.
- It will be a huge number of commits like CMake, many of them already reviewed
  in separate QML repo, map between current QT Widgets workflow and QML
  (parity), onboarding, wallet creation, etc.

We can then involve QML contributors more in the discussion.

Beyond different sets of notifications there are few benefits.

What is the benefit of the separation for those subscribing to all repos? None
really, information flow is the same.

Would it be possible to have QML as a subtree?

### How QML Design is done

Currently design is done in Figma. So that work doesn't happen on GitHub. That's
where designers are interacting. When a feature is implemented the designers
review it on GitHub. Now we are at the stage where we have a secondary feedback
and the pressure is to push designers to modify the QML directly rather than
making the devs do it.

Do we want to merge now or after/when the QML merge happens?

Do we archive the GUI repo right now?

We can close a lot of QT Widgets issues after QML is merged.

## Agreement/outcome

Agreement on archiving the GUI repo when QML lands.

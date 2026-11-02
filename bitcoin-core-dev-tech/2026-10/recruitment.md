---
title: Bitcoin Core Developer Recruitment
tags:
  - bitcoin-core
date: 2026-10-12
---

## What does Bitcoin Core need from new contributors?

### Motivation and independence

The discussion emphasized several qualities that recruitment programs could look for:

- **Intrinsic motivation:** Why does someone want to contribute to Bitcoin Core?
- **Self-direction and initiative:** Bitcoin Core is not a conventional job with a manager assigning tasks.
- **Practical experience:** Contributors who actively use the software are more likely to identify meaningful problems.
- **Communication skills:** Contributors need to explain technical ideas and feedback effectively, particularly in pull request discussions.
- **Independent judgment:** Contributors should understand and question the reasoning behind an approach, rather than simply accepting it and fixing isolated bugs.

### Code review skills

Finding a problem is only the first step. LLMs can help identify issues, but proposing a sound solution requires further understanding and judgment.

Reviewers should consider whether the overall approach is appropriate, not just whether its implementation contains bugs. Contributors should also write review comments in their own voice.

New contributors do not need to comment on PRs immediately. Reading existing PRs and following their discussions is a useful learning activity in its own right. An open question was how recruitment programs could teach contributors to progress from observing discussions to communicating useful feedback.

## Onboarding through practical use

### Start with the software

Ideas drawn from a recent ₿trust session included actively using Bitcoin Core, reporting issues, and setting up a Signet node to experiment with its functionality.

Other suggested exercises were to:

- Keep a journal of experiences, observations, bugs, and questions.
- Set up Bitcoin Core on an unfamiliar machine.
- Experiment with the GUI.
- Explore a new use case.
- Use mutation testing to investigate test coverage.
- Read ongoing PR discussions to learn how development and review work.

The emphasis was on developing familiarity and discovering concrete problems before immediately assigning implementation tasks.

### Organize learning around realistic use cases

The issues contributors encounter depend heavily on how they use the software. Relevant perspectives include Lightning Network operators, wallet and GUI users, and enterprise or high-volume node operators.

Some problems only emerge under particular workloads—for example, a node slowing down while processing a large volume of transactions.

One proposal was to categorize Bitcoin Core use cases and build onboarding paths around them. Rather than asking contributors to explore randomly, programs could provide realistic scenarios that expose different parts of the software.

Personal interests could also guide participation. Someone frustrated by aspects of the GUI, for example, could be directed toward reviewing QML work.

## Recruitment challenges

Several questions remained open:

- How should programs assess a candidate’s motivation and suitability for self-directed work?
- How should the project respond to “fly-by” contributors submitting AI-generated contributions?
- Which junior tasks remain useful and educational when AI tools are widely available?
- How can contributors be encouraged to move beyond finding problems toward proposing sound solutions?
- How can programs attract developers from the Rust ecosystem?

Participants also noted that developers interested in Bitcoin need not contribute directly to Bitcoin Core. Adjacent projects and interface consumers can provide valuable entry points.

## Internships and mentorship

One approach was to identify work that established contributors want completed but lack time to pursue. An intern could take on a complementary component—for example, implementing a frontend while a mentor works on the backend.

A project’s educational value need not depend on whether it is eventually merged. Independently implementing silent payments, perhaps in another language, was suggested as a way to learn the protocol and its design.

## Potential projects

| Project | Suggested scope |
|---|---|
| Multiprocess Bitcoin Core | Build a Rust sidecar using the Chain interface. Other implementation languages could also be suitable. |
| OpenRPC and interface consumers | Build tools that consume Bitcoin Core interfaces, potentially using OpenRPC. |
| CoreCheck | Mentioned as a potential internship project; no further scope was recorded. |
| Silent payments | Test wallet functionality or implement the protocol in another language as a learning exercise. |
| Fee-rate abstraction | Work on `CFeeRate` and related fee-rate interfaces. |
| Chunk-based fee estimation | Explore abstractions for retrieving chunk information and supporting chunk-based policy or fee estimation. Mentioned in connection with Summer of Bitcoin. |
| RPC fee-rate cleanup | Improve consistency and fee-rate handling across RPC interfaces. |
| Transaction size abstractions | Introduce clearer abstractions for size, virtual size, and weight, drawing comparisons with `Txid`/`Wtxid` distinctions and `CAmount`. |
| Wallet tool or offline signer | Begin with a standalone offline signing tool, potentially connecting it to a node later. |
| GUI and QML | Explore and review GUI development, particularly for contributors interested in user experience. |
| Signet exploration | Set up a node, exercise features, identify issues, and investigate bugs. |
| Mutation testing | Introduce deliberate changes and examine whether tests detect them, developing an understanding of coverage and expected behavior. |

## Possible approaches for recruitment programs

The discussion suggested several complementary approaches:

- **Usage-first onboarding:** Begin with hands-on use and realistic scenarios.
- **Review-first learning:** Read and understand existing PRs before participating actively in review.
- **Project-based learning:** Offer scoped projects that teach architecture, interfaces, and underlying concepts, even if the result is not merged.
- **Mentored complementary work:** Match interns with contributors whose projects can be divided into manageable components.
- **Adjacent ecosystem contributions:** Use Rust projects, multiprocess interfaces, external tools, and related Bitcoin software as entry points.

These approaches need not form a single mandatory progression. Different contributors may benefit from different starting points.

## Questions and potential follow-up

Further work could include:

- Defining candidate-selection criteria around motivation, initiative, communication, and technical judgment.
- Developing an approach to low-effort or AI-generated contributions.
- Identifying junior-friendly tasks suited to an AI-assisted development environment.
- Organizing onboarding exercises by use case.
- Finding contributors willing to mentor interns or delegate complementary work.
- Assessing proposed projects for scope, difficulty, mentorship availability, and upstream value.
- Exploring recruitment pathways from adjacent communities, particularly Rust developers.
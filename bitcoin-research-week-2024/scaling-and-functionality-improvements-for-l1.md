---
title: Scaling and Functionality Improvements for L1
date: 2024-11-19
---

## What would it take to get everyone in the world using Bitcoin?

- **Can’t fit every payment on-chain, so need something else:**

  - Lightning Network, shared UTXOs, sidechains.

- **Q: Are we talking about payments or other functionality?**

  - Mostly payments.

- **Layer 2 vs. Sidechain:**

  - Layer 2 vs. Layer 1: Layer 2 attempts scalability improvements by introducing data availability attacks.
  - In Ethereum: not exactly. Rollups store data on L1.
  - **State diffs vs. storing all transactions:**
    - Rollup definition: don’t execute on-chain, store what is needed to enable another operator to take over, and include a mechanism for validating on-chain (optimistic or zk).

- **Not enough blockspace for everyone to have their own Lightning channel → Shared UTXOs:**

  - **Ark - Virtual UTXOs:**
    - Ark service provider (ASP):
      - Sets up a tree of pre-signed transactions with not-yet-existing UTXOs.
      - Timeout mechanism: the ASP can take the root UTXOs after a set period (e.g., a month).
        - Collaborative ASP: “Give me a new VTXO.”
        - Non-collaborative ASP: “Materialize my branch on-chain.”
    - Discussion on how Ark works and potential griefing methods. General confusion among participants about Ark mechanics.
  - Lightning, BitVM, Ark, etc. add liveness assumptions, requiring the ability to get a transaction on-chain within a specific time frame.

- (Note from the notetaker):

  - _Please avoid using the term “trustless.” Instead, define actual security assumptions._
  - _Avoid vague accusations like “that’s centralized.” Specify the powers operators have._

- **Suggestion:** Increase witness size to mimic Ethereum’s blob space.

  - Doesn’t increase computational load but allows storing more L2 data.

- **Data availability possibilities:**

  - Just need to be able to restore the state.
  - Compress state and prove it can be decompressed.
  - E.g., 12 bytes per transaction (assuming keys are published elsewhere).

- **BitVM:**

  - Essentially a way to emulate `OP_ZKP`.
  - For sidechains: Requires a light-client of the sidechain in the main chain.
    - BitVM can verify the sidechain proposal but not prove it’s the canonical chain.
    - Examples: merge-mining, certificates, Bitcoin-based proof of stake.

- **Q: Is there any Bitcoin scaling solution that doesn’t benefit from covenants?**

  - Even Lightning benefits (e.g., LN-Symmetry).
  - Could also use `ANYPREVOUT` for LN-Symmetry?
    - Does `ANYPREVOUT` enable covenants?

- **Why does Lightning not solve scaling?**

  1. Not enough UTXOs for every user.
  2. Channel factories, Ark, etc., face the same n-of-n pre-signed transaction problem.

## Covenants discussion

- **Which one?**

  - Arguments for:
    - `OP_CAT`
    - Introspection opcodes.
  - **Thought experiment: 50 years from now, we’ve figured it all out, what covenants exist?**
    - Seems like `OP_CAT` will be enabled no matter what (in addition to other stuff)

- **Preferred roadmap:**

  - Person 1: `OP_CAT`, `OP_MUL`.
  - Person 2: `OP_CAT`, `OP_MUL`, `OP_CTV`. If flexible, GSR.
    - Possible additions: `OP_VAULT`, `OP_PAIR`, or fast hash functions if people are doing huge ZKPs.

- **CTV vs. TXHASH:**

  - Some prefer `TXHASH` over `CTV`.

- **General considerations:**
  - Opening the door to rollups, tokens, etc.:
    - Many features emulate `OP_CAT` (`OP_AND`, `OP_SUBSTR`, etc.).
    - Some hacking around `OP_TXHASH` is possible.
    - Seems like scaling requires opening the door?
  - **Conservative approach:**
    - `CTV` seems to be the least controversial update aiding scaling.

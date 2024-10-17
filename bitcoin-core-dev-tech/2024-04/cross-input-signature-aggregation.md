---
title: Cross Input Signature Aggregation
tags:
  - bitcoin-core
  - cisa
date: 2024-04-08
---
- cisaresearch.org, put together by fjahr
  - Documents progress of half and full agg (theory, implementation and deployment)
  - Provides collection of CISA-related resources (ML posts, papers, videos/podcasts,
    etc.)
Should provide guidance for further development/open todos for contributors to grab
- HRF announces CISA Research Fellowship
  - Seeks to answer questions how CISA will affect privacy, cost-savings, and much more
    during a four-month period for a total of .5BTC
  - More: 
https://nostr.com/note1h4fdw5ttqmjwf3eqr0s5lqzjhdvwcayl0hrfnv726cw4eeag6phs9xszpw
Will coordinate with them to align cisaresearch.org with their initiative to prevent duplicate work
- Recap half vs. full agg
  - Half agg
    - Proven secure
    - No cost savings in terms of verification, batch verification necessary (draft PR: https://github.com/bitcoin/bitcoin/pull/29491)
    - tx level
      - keep only r of original (r,s) signature in half-agged sig
      - aggregate s values
      - signature size reduced from n_input*64B to n_input*32B + 32B (aggregated s)
    - block level
      - aggregate s of all txs
      - can be stored in block's coinbase witness
  - Full agg
    - Security proof outstanding
    - Protocol under development
    - Requires interactivity
      - Can you merge interactivity of full agg into coinjoin?
        - Probably (might involve more rounds though)
      - Tadge's remarks on interactivity from Tabconf (https://www.youtube.com/watch?v=uI15RKnyX_E)
        - Cost of interactivity has been mispriced
        - Should get rid of interactivity when possible
    - signature size reduced from n_input*64B to 64B
- Update from Tim/Nick
  - Full agg: no real updates since BTC Azores
  - Half agg
    - Minor changes since BTC Azores
    - Three implementations available C, Python, hacspec/Rust
    - No concrete proposals to use it
- Potential BIP for half agg deployment
  - No reasons not to work on it
    - If you look at coinjoin, full agg would be best but half agg could save block space now and coinjoin's are just one part of the ecosystem
  - Should apply half agg at the block level, as more savings
  - Who is aggregating? Users or miners?
    - Can miner aggregation be a problem for users? For what transactions don't we want
      aggregation?
      - Adaptor signatures
      - Hypothesis: Can still use adaptor signature for script path (only aggregate key
        path spends, not script path spends)
  - Does half agg require consensus change?
    - Yes, needs new SegWit version
    - CISA improvement maybe too small to justify soft fork, so maybe package it with
      "next cool thing"
      - expected (maximum) weight improvement: 7.6% (15.2%)
      - expected (maximum) size improvement: 20.6% (41.2%)
      - details: https://github.com/BlockstreamResearch/cross-input-aggregation/blob/master/savings.org
  - Issue: block reorg
    - Cannot insert tx of reorged block into mempool, as s values are missing
    - Potential workaround: Include s values *with* (not in) block
      - s values required to accept block
      - s values stored until block buried deep enough so reorg is no concern
      - pro: faster IDB, can fit more data in block, con: blocks effectively >1MB (to xfer)
  - Issue: lowers dust threshold
    - Makes it slightly cheaper to sweep dust
    - Won't work for existing dust outputs

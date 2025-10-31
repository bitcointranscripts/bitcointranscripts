---
title: CISA FullAgg BIP
tags:
  - bitcoin-core
  - cisa
date: 2025-10-23
---

* Aggregation modes
  * Half-agg (32b + n*32b, non-interactive)
    * People sometimes think there is a big performance impact too, but we get most of that from batch validation without a soft fork
    * Full-agg (64b constant, interactive e.g. DahLIAS)
      * Additional verification time, per blockspace, due to smaller sizes
* Focus on tx-wide (vs block-wide. Tx-wide being widely used would mean block-wide could become mostly obsolete)
  * Tapscript upgrade issue
    * Problematic and collides with the OP_SUCCESS opcode
  * Hypothetical Witness v3 script: OP_CHECKAGGSIGADD OP_SUCCESSx OP_CHECKAGGSIGADD
    * When you redefine OP_SUCCESSx after CISA activation you could end up with different counters (see above) and this could result in a chain split.
      * Might need to change how OP_SUCCESSx works. No good solutions
        * Have next script versions use OP NOP as upgrade mechanism
        * Restriction on script and OP_CHECKAGGSIGADD to not have OP_SUCCESSx
  * Keypath spend aggregation is the focus currently. Punting on scriptpath for now. (like BIP341 vs 342 (tapscript issue above). Focus on “341” for now)
    * Payjoin and Coinjoin use cases work with this already so it is useful alone
    * Still hopeful we might still find a cleverer solution for the script problem
* Half? Full? Why not both?
  * For tx-wide aggregation, the plan is to do both
  * Half agg gives a nice default state that all transactions can profit from
  * Full agg gives maximum savings
  * Conversations revealed no clear favor between the two in the community, asking for “the other one” might turn out to be a bigger blocker 
  * Additional complexity seems manageable
  * Downside is an additional fingerprinting vector
* BIPs
  * Half-agg ~90% complete
  * Full-agg ~50% complete
  * Tx-wide Keypath -> rough drafts to be discussed next
  * Tx-wide Scriptpath -> ? (see issues above)
* Witness flexibility options, what is allowed and not allowed
  * One agg mode, one sighash (or only default)
  * One agg mode, flexible sighash (drafted) ←- simpler and preferred for coinjoin use cases. L2 use cases less considered currently
  * One of each agg mode, one sighash (or only default)
  * One of each agg mode, flexible sighash (drafted)
  * Multiples of full agg, one half-agg, one sighash (or only default)
  * Multiples of full agg, one half-agg, flexible sighash
* Things to consider
  * Flexibility for use-cases
  * Complexity to implement and maintain
  * Privacy implications
  * Other
    * Disable BIP340 Schnorr signatures entirely? Since they are similar sized. Simpler.
      * Can still opt out using the script path
      * What about adaptor signatures?
        * Could potentially do adaptor signatures with full aggregation
    * Privacy impact of coinjoins that use multiple rounds with mixing half and full agg
    * Consider whether tx-wide aggregation would preclude block-wide aggregation in the future

cisa-playground:
[https://github.com/fjahr/cisa-playground](https://github.com/fjahr/cisa-playground)

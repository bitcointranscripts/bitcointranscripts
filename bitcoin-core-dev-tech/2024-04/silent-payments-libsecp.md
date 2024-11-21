---
title: Silent Payments Libsecp Module
tags:
  - bitcoin-core
  - silent-payments
  - libsecp256k1
date: 2024-04-08
---
- High level vs low level API:
    - Low level API could be more useful for multi-party SP implementation 
    - High level API is safer as it avoid managing SP state and staging secret data
    - Rough consensus that high level API is preferable

- Responsibility of grouping and sorting recipients by scan key. Client vs library? 
    - We need to assert grouping in the lib anyway to avoid catastrophic failure
    - So it just makes sense for the lib to take care of the grouping
    - Why we need grouping in the first place?
        - This is for the case when a tx contains more than one output to the same SP address
        - The goal is to prevent 3rd parties from determining SP transaction and reverse engineering the recipient address from tx outputs using brute force
        - Need to have different shared secret, so salting shared secret with incremental k=0,1,2,33

- Problem: How the client map result value from the lib back to the passed input? The order of outputs could be different from passed recipients because of sorting and grouping.
    - Current solution: single struct used for in- and out- parameters
    - Alternative1: include index of the input parameter in the output
    - Alternative2: pass through client defined  ID associated with the input
    - Alternative3 (not ideal, but preferred): hide the index unraveling within the function 
        - Limitation: we need to allocate arrays at compiler time, but we the size is only available at runtime. So it's not possible to copy the data into a new array, we have to do it in place.
        - Workaround: Can have an un-initialized filed in a struct
        - Recipient will need to copy the data before passing to the module because the module will sort the input and thus modify it.
        - Nice to have: we can sort back the input array to restore the original order, paying the price of another sort

- Sending API:
    - Can use the concept of "examples" in libsecp to demonstrate how to use the SP module 
    - Is sending performance constrained?
        - Could be for exchanges
        - Asking HW to do more ECDH is not great 
    - Conclusion: just adding extra output parameter and "dummy" index (alternative 3 above) to the recipient addresses struct 

- Receiving API:
    - Can be used only when we have access to the whole tx
    - Currently we compute shared secret using a separate function
    - Proposed alternative:
        - Just pass the list of pub keys and the shared secrete is calculated internally
        - Instead of the list it could be a summed up pub keys. That would benefit light client nodes because they can get it from the index from a full node.
        - Also full node can use the summing function for the index, even if they don't scan for SP txs itself, but just serve the index.

- Labels
    - Look up function callback
        - Useful for scanning performance for the use-cases  with large amounts of labels 
        - The callback should return associated label tweak if label is found
        - Do callbacks introduce performance issues with language bindings? Seems to work well in Bitcoin core
        - Possible to pass "null" in place of callback if the client don't want to implement labels
        - Void* parameter is there to have context passed in to the callback. This is best practice
    - preserving and returning label metadata to the caller to save cost of expensive lookup
        - Maybe need to add a Boolean for that purpose to be able to signal "label not found" 
        - Also set pubkey to an invalid key
    - Light client 
        - Use lower level function to be able to check utxo against the filter

---
title: Py-bitcoinkernel demo
tags:
  - bitcoin-core
  - libbitcoinkernel
date: 2025-02-26
---

## Transcript

No transcript of the conversation.

## Demo

The purpose of this demo was to showcase the [py-bitcoinkernel](https://github.com/stickies-v/py-bitcoinkernel/) Python libbitcoinkernel wrapper, with the specific focus on showing that this library makes it very low-barrier to explore and interact with the libbitcoinkernel interface. Specifically, on most platforms, the library can be installed from [PyPI](https://pypi.org/project/py-bitcoinkernel/) without dependencies, and basic interactions only take a few lines of code.

### Wrapped demo

The below script was demoed to show the "wrapped" version of the library. Wrapped means that the pure C api is abstracted away into Pythonic classes, functions, iterators, ...

```python
DATA_DIR="/tmp/bitcoin/signet/"  # Copy the contents of a real signet datadir to DATA_DIR
  
  
import pbk  
  
log = pbk.LoggingConnection()  
  
chainman = pbk.load_chainman(DATA_DIR, pbk.ChainType.SIGNET)  
for idx in pbk.block_index_generator(chainman, start=-10):  
    undo = chainman.read_block_undo_from_disk(idx)  
    max_output = 0  
    for tx in undo.iter_transactions():  
        max_output = max([output.amount for output in tx.iter_outputs()] + [max_output])  
    print(f"Block {idx.height} spends a max output amount of {max_output}")
```

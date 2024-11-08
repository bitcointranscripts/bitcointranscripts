---
title: The Future of Hardware Wallets
transcript_by: Bryan Bishop
tags:
  - hardware wallet
speakers:
  - Stepan Snigirev
media: https://www.youtube.com/watch?v=OxX_LFgdYa0
---
D419 C410 1E24 5B09 0D2C 46BF 8C3D 2C48 560E 81AC

<https://twitter.com/kanzure/status/1137663515957837826>

## Introduction

We are making a secure hardware platform for developers so that they can build their own hardware wallets. Today I want to talk about certain challenges for hardware wallets, what we're missing, and how we can get better.

## Current capabilities of hardware wallets

Normally, hardware wallets keep keys reasonably secret and are able to spend coins or sign transactions. All the inputs have to be ours, that's the usual constraint. Then we can have an arbitrary list of outputs including a change output that belongs to the user. We can receive funds, so we can show an address on the hardware wallet. And these hardware wallets can do multisig. Some wallets do or don't support multisig. Also, hardware wallets can do shitcoins.

## Nice to have features

It would be nice if hardware wallets had support for coinjoin, lightning, custom scripts and sidechains. Right now, you can't do coinjoins with hardware wallets. Lightning is awesome but tricky. With coinjoin, the trick is that we have a bunch of inputs and a bunch of outputs. After the last talk, you're probably all already experts in coinjoin. The crucial thing about coinjoin is that they have external inputs. In hardware wallets, a naieve implementation of coinjoin will allow coinjoins to steal your coins. I will be focusing on lightning and coinjoin for now.

## Coinjoin

I can probably skip this slide since you know the concept. We first need to register the coin inputs to the coinjoin server. Then we sign a coinjoin transaction, and retry if someone else in the protocol fails. The signature is returned to the server so that the server can broadcast the coinjoin transaction. Sometimes a coinjoin transaction fails to get completely signed because one of the users is doing a denial of service attack or otherwise. It's common from the user's perspective to retry with the same inputs or same amounts.

## Coinjoin attack

Say we're a malicious wallet. I am not a coinjoin server, but a client application. I can put two identical user inputs, which is usually common in coinjoin, and you put them in the inputs and you put only one user output and then the others are other outputs. How can the hardware wallet decide if the input belongs to the user or not? Right now there's no way. So we trust the software to mark the input needed to sign. The attack is to mark only one of the user inputs as mine, and then the hardware wallet signs it and we get the signature for the first input. The software wallet then pretends the coinjoin transaction failed, and sends to the hardware transaction the same transaction but marking the second input as ours. So the hardware wallet doesn't have a way to determine which inputs were his. You could do SPV proofs to proof that an input is yours. We need a reliable way to determine if the input belongs to the hardware wallet or not. Trezor is working on this with achow101.

## Hardware wallet proof of (non) ownership

<https://github.com/satoshilabs/slips/blob/slips-19-20-coinjoin-proofs/slip-0019.md>

We could make a proof for every input, and we need to sign this proof with a key. The idea is to prove that you can spend and prove that... it can commit to the whole coinjoin transaction to prove to the server that this is owned, and it helps the server defend against denial of service attacks because now the attacker has to spend his own UTXOs. The proof can only be signed by the hardware wallet itself. You also have a unique transaction identifier.. It's sign(UTI||proof\_body, input\_key). They can't take this proof and send it to another coinjoin round. This technique proves that we own the input. The problem arises from the fact that we have this crazy derivation path.  Use the unique identity key, which can be a normal bitcoin key with a fixed derivation path.  The proof body will be HMAC(id\_key, txid || vout). This can be wallet-specific and the host may collect them for UTXOs. You can't fake this because the hardware wallet is the only thing that can generate this proof.

This could be extend to multisig or even MuSig key aggregation.

## Beyond p2wpkh

We can replace the signature with a witness in the previous scheme. We sign it with multiple co-signers. We combine the signatures into the witness, and then everyone can verify that all participants in the coinjoin transaction that yeah this guy has enough keys to sign this input. The proof body can be hmac(id\_key1, txid || vout) || hmac(id\_key2, txid || vout). You just concatenate all the proofs together.

## Challenges

What if we have Schnorr signatures? We could use key aggregation, so our signature will be from a single key. But this will be larger. It's a leak of privacy for coinjoin to do that. Every participant will see that you have a 3x larger proof, and then on another coinjoin round you might see another input with the same big thing so it breaks some privacy. Schnorr and taproot might be able to make fixed-sized proofs.

In order to verify the signature, you need to know the public key, to know the public key you need to know the scriptpubkey, and you nee dto make sure the transaction hashes to the txid that you used in the input. It requires verification of the scripts on the hardware wallet, which is currently not available anywhere, and it's problematic because if there's a bug then you would be able to generate a proof that is valid on a hardware wallet but not valid for coinjoin transactions.

For single key use case, I think we're ready to deploy it and run it and use coinjoin on hardware wallets.

## Lightning on hardware wallets

We need to be connected all the time in order to route lightning payments and also receive lightning payments and maybe send. There are timelocks everywhere. We need to react in a timely manner. We also need to monitor the blockchain because we need to know if the channel is still open, or closed, or an error.

There's a bunch of secrets in the lightning protocol. There's on-chain keys, channel keys, and revocation secrets. There's the keys used to fund the channels, the keys used to update the channel, and revocation secrets that we give out to other parties every time when we invalidate previous state such that they can punish us if we misbehave and vice-versa. And there's some keys for where we will store our bitcoin when we close the channel either cooperatively or unilaterally.

Imagine we have a hardware wallet that can store all of these keys. Is that enough for security? Well, not really. If you're using a hardware wallet, then we assume our node is hacked. The attacker can open a channel with us, send a funded transaction, we send back a commitment transaction and we start to think the channel is open. On hardware wallets, we tend to have limited information about the lbockchain. So we think the channel is open, but the attacker uses this virtual non-existing channel to route through us. He transfers bitcoin to us, we automatically forward it through our real channels and real bitcoin and then we lose bitcoin. So we need a proof that the channel is open. It's an SPV proof that the transaction is included in the blockchain. However, this is insufficient. The attacker can open the channel, show us the proof, and then instantly close it. So the attacker just waits until the channel doesn't exist. So we need to pass all the blocks to the hardware wallet. We don't have a way to prove that a transaction is not included in a block; we could use a bloom filter I guess but people don't like SPV and lite clients. But such a filter would help with hardware wallets so that we don't have to parse the whole block and see if it was closed or not. So we do need block parsing.

What if the attacker starts delaying the blockchain? He is sending the blocks with a certain delay and builds up this delay up to one of the locktimes. As the hardware wallet sees the past, the attacker can do the same attack again using the closed channel that is still open in the past in the mind of the hardware wallet. In the hardware wallet, we need to add a real-time clock. It's good that we have timestamps in bitcoin blocks, which are defined within a certain range of +/- 2 hours. If we see that blocks are delayed by more than 2 hours, then we can notify the user and stop signing things and stop routing transactions.

Finally, it would be nice to have a backup communication channel if the attacker tries to completely disconnect our hardware wallet. Watchtowers could work, or any kind of notification to the user that something is going wrong here.

## Trusted nodes and initial hardware support

We can limit the behavior of the node to eliminate routing. We can only send and receive. The only way to lose the funds is routing through the nodes with the lightning payment. What we can enforce is to get a message signed on the hardware wallet with the key that we used to open the channel, and this message can be verified-- all hardware wallets support message signing, like "yes, I do want to send 1 millicoin with the payment hash of blah". Then you send it together with your other offers, your trusted node verifies it and then routes the payment. You can still receive payments without interacting with the hardware wallet. The trusted node can route the incoming receive request.

You can sign a message and define the limit, like "please route payments up to this amount x" and the trusted node can enforce that at most you will lose that amount you specified. It still relies on the trusted node to behave properly, but at least I would say that there is some additional security that we can gain.

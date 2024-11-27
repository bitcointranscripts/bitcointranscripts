---
title: Payjoin
tags:
  - bitcoin-core
  - payjoin
  - wallet
date: 2024-10-15
---
Should Payjoin be introduced into Bitcoin Core wallet? Not a strong yes, but no direct objections.

## Effect on Existing Wallet Users

Would require user interaction, so if the user doesn't initiate Payjoin, the corresponding code path wouldn’t be invoked.

## HTTP

Does Payjoin require HTTPS to be re-introduced?
No, Payjoin uses Oblivious HTTP.
Uses HTTP with an encrypted payload. Could use existing crypto modules in Bitcoin.
HTTP in Bitcoin Core is a larger topic, so the implementation of HTTP for Payjoin should align with the larger usage of HTTP.
For Payjoin, would Bitcoin Core need to be an HTTP server, or just client?  Just client.

## Security

Concerns were expressed about ensuring safety when parsing (HTTP) responses.

## Other

Are there any other potential uses for OHTTP outside of Payjoin? Nothing concrete was identified.

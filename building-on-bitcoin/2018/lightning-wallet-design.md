---
title: Designing Lightning Wallets for the Bitcoin Users
transcript_by: Bryan Bishop
tags:
  - lightning
  - ux
speakers:
  - Patricia Estevao
media: https://www.youtube.com/watch?v=S2TgCUU_WDo
---
Good morning everyone. Thank you for being here. Thank you to the organizers for this event. My talk is about designing lightning wallets for bitcoin users. I am talking about UX. But really, UX is a lot more than what wallets look like. It's from bip39 and making backups much easier, to anything you cna imagine, to make it easier for bitcoin to use bitcoin.

I am Patricia Estevao.
https://patestevao.com/

patestevao

https://patestevao.gitbooks.io/lightning-network-ux-research/

The potential of lightning is not a given. We need to work towards that direction. I've published preliminary research on the UX of bitcoin lightning network. The research is at that link there. It's also on my website.

I decided to talk today about design of lightning wallets. We should preserve the mental model that the user already has of a lightning bitcoin wallet or a regular bitcoin wallet. I will also be developing some wireframes  of a lightning bitcoin wallet.  We wont see any defined style elements here, no fonts or colors or anything like that.

First, when I am talking about design, I like to talk about design usability in bitcoin. Why should we care about usability? I'm not worried about having the coolest interface to make snapchat users switch to snapchat bitcoin interfaces. Usability is about how easy it is to do something. That's the definition of usability. How easy is it to do something? If people don't know how to use the systems they are using, then they are more likely to make mistakes and in bitcoin mistakes are translated into irreversible financial loss and privacy loss.

If we want to make those revolutionary things happen, like releasing people from fiat, then we need to build usable interfaces for them.

There has been some effort for bitcoin interfaces to make them more usable. Users have a mental model of a bitcoin wallet. This mental model simply translates to saying they have a representation in their mind of how bitcoin wallets work. That representation whether accurate or not, will define their expectations when interacting with a lightning wallet. How do we introduce a lightning network wallet that can easily be used by people already using bitcoin wallets?

Lightning is a complex technology built on top of bitcoin. There's new concepts and new techniques.  Let's not get ahead of ourselves. If they are interested in learning about this comple stuf,f then they should read about it. Remove unnecessary complexities and don't break the users' mental model.

A lightning-enabled bitcoin wallet does not need to break a user's mental model of how a bitcoin wallet works.

This is a familiar concept of what a payment page looks like for a bitcoin user. They expect to see an address, amount, and label field for organizational purposes.

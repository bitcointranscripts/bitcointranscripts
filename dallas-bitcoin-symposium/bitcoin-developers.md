---
title: Bitcoin Developers
transcript_by: Bryan Bishop
speakers:
  - Justin Moon
---
# Introduction

I am going to talk about a programmer's perspective. As investors, you might find this interesting, but at the same time it's not entirely actionable. As a programmer, the bitcoin ecosystem is very attractive. This is true of cryptocurrencies in general. I'll make a distinction for bitcoin at the end. One of the interesting things is that you see some of the most talented hackers in the world are extremely attracted to bitcoin. I think that's an interesting thing you should pay attention to. I think there's something there. I am going to try to keep my talk simple, and talk about what is bitcoin.

# What is bitcoin?

Bitcoin is a computer network. What is a computer network? It's a set of computers connected together for the purpose of sharing resources. The resource that bitcoin shares is a ledger. You could look at it as one giant file, which would fill up this laptop's hard drive. It's like a huge spreadsheet. It's kind of a circular thing. What's in the ledger? Well, the capital B bitcoin network has this ledger, and inside of it, it keeps track of this little unit it defines called "bitcoin" with lower case b. It's a weird circular things, it's a ledger that keeps track of itself that only exists in this context. It's just a ledger.

These networked computers agree to a protocol, which is a set of rules about what you can do and can't do. An example of a rule is that there's only ever 21 million bitcoin. Every block, there is a fixed supply that is created. Every four years, that supply rate gets cut in half, until the rate hits 1 satoshi and after 1 satoshi it goes to 0 satoshi in four years. It's a rule about how to assign new coins to new owners and how to bring coins into existence.

Bitcoin programmers write computer programs that follow the protocol rules and provide some function. They might try to improve or update the rules, too. There's a few types of programmers. A researcher is someone who thinks about the incentives in all the pieces of the software ecosystem, and thinks of new cryptographic constructions that might bring more privacy or maybe improve the speed of validating bitcoin transactions because when you start your node it takes a few days to sync the first time. That's more of a researcher point of view. They also try to break things; researchers try to break everything, which is different from every day life... that's what Dhruv is trying to do all day long, just breaking things all day. This gives you confidence that the network is secure, there's many experts, and "the biggest bug bounty program" ever.

Another class of programmers are the protocol developers. These are the programmers that write the rules that enforce the network rules. You have to take these abstract rules and put it into code; sometimes bugs occur when we think the rules we thought we have behave a little differently from what the code is. This is why it is important to have good protocol developers, because the cost of these bugs is really high.

Application developers make applications that work with bitcoin. This coldcard here could store $1 billion of crypto. You don't want to do that, but you could. There were two people involved in making this device. One does the busines stuff, and one person writes the software. It's one software developer, and one person can make basically a Swiss bank on this tiny $100 piece of hardware. From a programming point of view, that's very different from working at a Wall Street bank where you're just a cog in the machine. Here, you can make a big impact. For a talented programmer, bitcoin is clearly one way to do that.

Then there's second-layer protocol developers, you may have heard of lightning network. If we end up with a world with lots of bitcoin banks, you could have a protocol where each bank is able to prove that they are not fractionally reserved.

# Different from the legacy systems

I previously worked with a startup that was working with the Visa/Mastercard network. Permissionless innovation is a big deal. To do anything interesting with Visa or Mastercard, it would take at least 6 months of business development. The people who are good at doing product development may not be good at business development. So if they just work on bitcoin directly, then they can move faster. It's similar to mineral rights here in texas. If you own the land, you can drill, and you don't have to ask permission. It's the same way in bitcoin programming.

# Different from other cryptocurrencies

What makes bitcoin different from (colloquially) shitcoins? Well, bitcoin focuses on making the base technology as resilient as possible. There's like 2 trillion bits in the bitcoin ledger, and if you get just one of those wrong, then you can have the network completely split in half. That's really bad when that happens. It's one of those Hindenbugs. It's really important to reduce the chances of that. Also, the people who are working on the bitcoin network are often doing it on a volunteer basis, but on other networks that raised hundreds of millions of dollars, those developers might be paid and might have less noble motivations. Also, bitcoin lacks a decision maker. The network/protocol rules only change with overwhelming support of the entirety of the bitcoin community. It is much more important to kill bad bills than to pass good ones. This is because bitcoin works, and it doesn't need to change a lot. This makes it very different from other coins.

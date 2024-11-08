---
title: C-Lightning API
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
speakers:
  - Christian Decker
date: 2018-10-24
media: https://www.youtube.com/watch?v=l8OLD7or0DA
aliases:
  - /chaincode-labs/chaincode-residency/2018-10-24-christian-decker-c-lightning-api/
---
Location: Chaincode Labs Lightning Residency 2018

<https://twitter.com/kanzure/status/1232313790311436290>

# Intro

Good morning from the last day of presentations. I’m Chris still. Today I will be talking to you about c-lightning, how to develop on it, how to extend it, adapt it to your needs and how to customize it so it fits into whatever you are trying to do. Not whatever we thought you might want to do.

# Goals

First of all the goals of c-lightning are basically to be fast and lightweight. We want you to be able to deploy this on Raspberry Pis, on big beefy server machines, on your laptops, wherever you sort of have a stable connection. There you give the best utility to the rest of the network. We want c-lightning to be flexible and customizable because we don’t think that we will guess the exact configuration that you will need. We want to give you the tools to adapt it to your own needs. We want to optimize for power users. There’s plenty of options for Lightning nodes to run on home devices, on mobile phones. While we can do that we will know how to optimize for that. We want to be the server backend running big services on top of this.

# TL;DR I want my node now

After this slide you can probably stop listening because that is all you need to know. We provide a PPA for Ubuntu and Debian based systems. All you need to do is just add the repository `lightningnetwork`, do an `apt-get update` and install `lightningd`.

```
sudo add-apt-repository ppa:lightningnetwork/ppa
sudo apt-get update
sudo apt-get install lightningd
```

Then you can start lightningd. Notice that by default we still have the testnet as the network configuration. We also encourage people to enable `log-level=debug` because that gives us loads of information should anything go wrong. We can help you try to debug whatever happened.

`lightningd —network=bitcoin —log-level=debug`

If you can also pipe this output into a file because it scrolls by really fast. It is useful to have if you need help debugging. There’s loads of information there. Don’t be scared if some messages say this and this died. That is just a terminology, it is not bad, it is just a process terminating. We have had loads of these reports. To talk to lightningd just use the command line client `lightning-cli`.

`lightning-cli getinfo`

`lightning-cli help` will give you all the possible JSON RPC calls that you can invoke with this. You should be ok.

Q - It does not include bitcoind as a dependency?

A - It does not currently include bitcoind as a dependency. If you have a running bitcoind and you are caught up this process should take you about 30 seconds on top, 5 seconds below and the last one is about 10 milliseconds. It should be ok to get started.

Q - It searches for a running bitcoind instance on your system and then reads the Bitcoin conf?

A - Indeed it does. What we basically use in the background is bitcoin-cli. If you can talk to bitcoind using bitcoin-cli then you are golden. If you don’t have a running bitcoind on the same machine you can also tell lightningd to reach out to some other node using the RPC `connect` command line option. There you can basically have for your organization one central bitcoind and have hundreds of Lightning nodes talk to them.

Q - RPC connect with bitcoin-cli?

A - What you need to do is on the lightningd command line specify `—bitcoin-rpcconnect=ip:port` or `ip` if you use the default port. What we do basically is we just hand those back to bitcoin-cli when we call it.

# Architecture

Now that we know how to run it, let’s talk about how we can actually build stuff on top of it. The architecture of c-lightning is a bit special. Each individual box here is a different process. On the left side we have the channeld processes and onchaind processes, each of them take care of one channel. If a channel should ever catch the rest of the program should still go on. If you wanted you could actually separate them into separate security policies using SELinux or AppArmor just to be bolt them down to what you feel comfortable with. The master daemon takes care of managing the state across all of these daemons. It is the process that you start. It is also the process that will start all of the other processes. No need to think about this in day-to-day usage. It gives us a lot of flexibility. On the right hand side we have the gossipd and hsmd. gossipd is the place where we store information about the network, our local view of the network. We receive gossip messages, process them and apply them to our local view. When we need to make a routing decision we just ask for it “Hey how do I get from A to B.” hsmd is what happens the private keys. Currently it is not really a hsm, it is just called that because it is aspirational. Eventually we want to have a hsm. What this allows us is to have the key management separate from the main daemon. The main daemon doesn’t know any private information about that node. We can actually start moving the hsmd around. We could move it into an actual physical HSM. We could move it onto your phone. You could host lightningd on some third party service provider. It won’t be able to do anything and it will talk to your phone which holds the actual private keys for example. Now we have the newest addition which are plugins. Plugins are basically just tiny scripts that talk JSON-RPC over standard input and standard output. You can write them in whatever language you want. They are a bit more integrated than the JSON-RPC interface in that they get notifications and push notifications whenever something happens. We can also reach out to them to change the normal flow of operations.

Q - What plugins currently exist?

A - A hello world plugin because I am still developing the plugin infrastructure. Wait two weeks and then it will actually be working. Everything else is working right now.

Q - Can you talk about the decision to separate all these n channeld instances rather than just having one channeld instance that maintains the state for all your channels? Can you also talk about control flow throughout the c-lightning instance. From what I can tell peer-to-peer messages come in through gossipd, master acts like some sort of controller, routes to the appropriate channel instance, maybe signs something via hsmd. Does that get pretty complex to maintain?

A - The questions are twofold. One is why did we decide to go for a multi-daemon architecture and the second one is how does the flow actually work? The decision for multi-daemon architecture is so that we can easily swap out individual parts. It is a separation of concerns. We want to have the channeld only take care and only access information that is relevant for the operation of channeld. We want to have the hsmd which takes care of all things private key and gossipd is also a specialized daemon that only has access to the stuff that it needs. First of all for us it is a simplification because we don’t need to deal with the complexity of having multiple things running in the same process. It is a security concern because you can have these in separate memory spaces. You could potentially move them onto different machines as well. Thirdly we can actually separate them into their own runtimes using SELinux or AppArmor or you could even Dockerize them if you wanted. Not that Docker is particularly good at security.

Q - The first question was more directed towards the specific channeld instances. Is this just so you can have different security policies for the channels that you have open? I understand separation of concerns for the wider application but specific channels themselves?

A - The question is why one channeld per channel. First of all it is a security concern in our case because these daemons talk to live traffic on the network. If there is some way to crash this daemon we wanted to crash that one daemon and not the entire thing. It just makes life cycle management easier because this daemon is alive, I want to kill that connection, kill that daemon. It is rather simple and really nice because the whole process is one state machine for the channel, no handling of multiple channels in there. It is very simple. About the control flow. What we do internally is file descriptor passing. If a peer connects to a daemon called connect daemon the connect daemon will pass it off to a separate daemon which initiates the transport layer security handshake. Then passes it off to channeld.

Q - What daemon is specifically connected to the outside network, is it gossipd or is it master?

A - Connected to the outside world are two daemons, three if you count handshaked but we’re merging that one in. There is an additional daemon called connectd, that is only there to listen for incoming connections. As soon as an incoming connection is made it hands the file descriptor for the connection up to the master daemon. The master daemon does not touch it in any way. The master daemon spawns a channeld and passes the file descriptor over. The only things in this pattern that actually talks to the outside world are the channeld’s on the left hand side.

Q - What is the responsibility of gossipd if it is not the thing that is managing…

A - gossipd is there as a central store for network information.

Q - There were plans to externalize the gossip so that separate Lightning daemons could utilize the same gossipd?

A - The question is whether we have plans to externalize gossipd. gossipd is external currently. It currently starts a new gossipd for each c-lightning instance but you could potentially merge that into one big gossipd if you run hundreds of c-lightning nodes. You can also just have a small stub that talks to a centralized server. That gets rid of a lot of duplication in your infrastructure because gossipd is actually the thing that uses the most memory in all of this. It is only scarcely used. You could potentially just centralize that and have it talk to some routing service that is external.

# JSON-RPC Interface

(UNIX Socket exposed at `\$HOME/.lightning/lightning-rpc`)

What I didn’t mention too much is we have a JSON-RPC. Why JSON? It is really easy, it is human readable. I can go onto a shell and start typing stuff into socket and be done with it. It is a UNIX socket so we don’t expose that over the network. That is a conscious decision because we don’t pretend to know what your authentication scheme is or your preferred transport layer is, your preferred way of interacting with the RPC is. We just have this really simple UNIX socket that you can then use to build a service on top that integrates with your infrastructure, that does whatever authentication you do, that does whatever logging you want to do and we don’t have to guess what you want to do. The easiest way to use it is the lightning-cli. That is a small wrapper around socat with some string manipulation. `lightning-cli help` and `lightning-cli getinfo` will give you all the information you need. One thing that we copied from bitcoind is that `help` will also connect to the daemon. If the daemon is not running `lightning-cli help` will do nothing. If you install from the PPA we have man pages for most of the commands. `lightning-cli help` followed by the command you want to use will pop up the man page on the shell and you will be able to get all the information that you need. If we didn’t write a man page you will get a short blurb that will still tell you what to do. It won’t be as extensive as the man page.

Q - Is there anything that is preferable to develop a plugin over the CLI?

A - With respect to plugin versus CLI, as long as whatever we do fits into your model and the automated way of interacting with c-lightning, accepting payments, creating invoices and all of that stuff, works for you don’t write a plugin. Just be a JSON-RPC client. If you want to customize how c-lightning interacts with the rest of the world and you don’t want to have a separate thing that you need to make sure runs you can write a plugin and have this slightly more tight integration with c-lightning.

JSON-RPC clients, we have the [Python JSON-RPC client](https://pypi.org/project/pylightning) which is the most up to date. It is also what we use for testing internally. This will actually be always on par with the c-lightning implementation. We have the [Javascript client](https://github.com/ElementsProject/lightning-charge) which is part of Lightning Charge. Lightning Charge is basically one of these services that expose the JSON-RPC over the network. It is a NodeJS service that exposes both a JSON-RPC over HTTP as well as a REST over HTTP service. If you feel more comfortable with REST you can use that. If you feel more comfortable with JSON-RPC you can take the library part of Lightning Charge. I have written a tiny [Go wrapper](https://github.com/cdecker/kugelblitz) that is so out of date that I feel awkward just talking about it. If you really just want to hack with c-lightning there is also the option of using socat on the shell. Mind you, you will have to write JSON messages and valid JSON-RPC calls but you could potentially run stuff from the shell as well.

# Invoicing/Receiving Payments

`lightning-cli invoice [msatoshi][label][description]`

Just really quick, going through the invoices flow, invoicing and receiving payments. To receive a payment you first of all have to create an invoice by specifying the amount in millisatoshis you’d like to receive, a label and a description. The label has to be unique. The reason why we have the label in there is because we don’t want to force you to have whatever external system track what invoice matches what shopping cart for example. If you are using WooCommerce which is a popular shopping plugin for Wordpress, what you could do there is have the label be the numeric id of the shopping cart that matches this invoice. This is a way for you to later be able to associate an incoming payment with whatever you wanted to have paid for. The description is what will end up in the invoice. That is you telling the customer I just bought 3 baseball caps and a coffee. It is not necessary but it is always nice to tell people what they bought.

```
lightning-cli listinvoices
lightning-cli waitinvoice [label]
lightning-cli waitanyinvoice [last-pay-index]
```

To wait for invoices we have the `lightning-cli listinvoices`. That’s just basically a huge list of all invoices. Or you could also specify a label in which case it will just show this one invoice. We have ‘waitinvoice’ followed by label if you want to wait for a specific invoice to be paid. That’s a way to do it. If you have a lot of pending invoices you are probably better off with the `waitanyinvoice` which gives you the next invoice that is completed after the `last-pay-index`. What you can do is I receive a payment, this payment has a payment index and in the meantime more payments come in and then if you just want the next one you can add the `last-pay-index` which will give you the next one. If there has already been a next invoice that has been paid you will get that one. If there was no next payment then this will block until an invoice is paid. This is just acting as a message queue for you to consume invoices that have been paid.

`lightning-cli delexpiredinvoice [maxexpiry]`

Finally some housekeeping. Delete expired invoices if your invoice has expired and hasn’t been paid. Just delete it, you don’t have to keep it around. There is also an autodelayed expired invoices which allows you to delete after a certain amount of time. Depending on what kind of statistics you want to run against this it might not be a good idea to autodelete.

# Sending payments

`lightning-cli pay [bolt11]`

Sending is way more interesting. There is the `lightning-cli pay` command where you give a BOLT 11 string and you are done, hopefully. What that will do is find a path, try a path, check if the attempt failed. If it failed, retry. If it succeeded we go back and say “Hey it succeeded and here’s what I tried.” The output is rather large because it will tell you each payment attempt, what path it tried to use and what the error messages were. You can probably cut out 90\% of the output there.

Q - The `last-pay-index`. How do I know the `last-pay-index`? If I do `listinvoices` it doesn’t tell me what index?

A - The question is where do I get the `last-pay-index` from? The `last-pay-index` is one of the fields returned by `waitanyinvoice`. So `waitanyinvoice` will actually tell you here’s an invoice that was paid and if you want to continue without skipping any received invoices please use this last pay index next. From there you can then incrementally consume this queue and be sure that you don’t skip any payment.

Q - It is just an arbitrary order then?

A - The order is actually the order in which we process the incoming payments. This does not match the database id of the invoice but it is a field that enumerates in which order we receive them and therefore in which order we should return them as well.

Q - What is the experience when running `waitinvoice` from the shell? It is idle until the payment is received?

A - Yes. The `waitanyinvoice` will block the command until it has something to return. There is also a variant where you can specify a timeout saying “Hey I would like to wait for 5 minutes. If nothing comes in give me back control over my shell and I will be doing something else then. The same is true for the JSON-RPC. It will also block until something was received or a timeout expired.

So `pay` is automated, it is magic, it might not be what you want to use. If you want to have more control over what happens.

```
lightning-cli getroute [destination][msatoshi][riskfactor]
lightning-cli sendpay [route][payment_hash]
lightning-cli waitsendpay [payment_hash]
```

For example if you want to create a special route that drops off more money like Rene did a few days ago you can use `getroute` and that will give you a JSON description of the path that the payment might take. You can actually edit that however you’d like. Be careful if you reduce the fee amounts or something like that. The forwarding node might not forward it anymore. You can do fun stuff like concatenate two routes from A to B and then B to A and create circles and all of that fun stuff. If you really want to do that there are really nice things we can do with this like lotteries over Lightning. Have me trigger some coin flip on a gambling service and then getting the payout in the form of a Lightning payment. `sendpay` will actually take the route that you just created with `getroute` and given a payment hash will attempt to pay that route with that payment hash. And `waitsendpay` is again a way for you to wait for this payment to succeed.

Q - Is routes a list of…?

A - Routes is a list of dicts and the dict contains the CLTV that should be applied at that place, the amount of satoshis that should be forwarded and which channel to use obviously. That’s basically what the onion looks like when you receive it and decrypt it and now need to forward it. What CLTV should I use, how many satoshis should I forward and which channel of my five should I use?

Q - Is that the same format that’s in BOLT 11 for invoices?

A - I don’t think so, no because BOLT 11 uses binary encoding for this and this uses a JSON format.

Q - Same data contents?

A - It should have the same data contents… Actually no because BOLT 11 will tell you the deltas for each of them whilst this one will tell you the exact amounts. It will actually tell you if I want a fee of 1 satoshi and you forward 1001 satoshis, I will forward 1000. It basically has the absolute amounts for value transferred whereas the format in the BOLT 11 invoice will tell you this node would charge such and such proportional fee and such and such base fee.

`lightning-cli listpayments`

# Subdaemons

Subdaemons, this is the interesting part. Subdaemons are tightly integrated. They talk binary protocol with the main daemon. They allow you fun stuff like replacing how we talk to Bitcoin for example. You can use bitcoind, Neutrino, spruned. My Neutrino implementation isn’t quite done yet but eventually we will have one I promise. You can also talk to a central bitcoind instead of having each c-lightning be sitting right next to bitcoind which allows you to scale up the number of c-lightning nodes without having this huge impact. Routing service, as we mentioned before for all of your Lightning daemons you can centralize the gossip. That gives you a better view of what the network looks like because you get feedback from failures and successes for all of your Lightning daemons. It saves you again on infrastructure by keeping what is memory heavy in a separate centralized repository. With the hsm we can have actual hardware wallets. We can move the hsmd around, on your phone have somebody else take care of connectivity, running c-lightning and your phone having the control over private keys. This makes for a real nice onboarding story where you go to some service, you just want to dip your toe into using c-lightning, they will take care of everything. You can then upgrade to taking care of your own private keys. Then you can upgrade to moving that c-lightning daemon to your home, running it on a Raspberry Pi somewhere. Finally the extreme case is running everything on your phone. Whatever you choose that suits your needs you can do it.

# Plugins (tbd)

Plugins, this is very much work in progress. Since I pitched plugins as a solution for everything this week I thought I might quickly talk about them. Plugins are basically just a two way street between c-lightning and some external process. You can write a plugin in whatever language you want. It receives incoming messages, both JSON-RPC calls and JSON-RPC notifications via standard input. It writes out the JSON-RPC response to standard output. Initially we probably want to make this as read only as possible. Basically c-lightning will send out notifications for state changes in c-lightning and the plugin can then reach around and talk to the JSON-RPC interface to enact some changes. The autopilot is a good example of this where you basically read the current state, how many connections do I have, how many connections would I want to have? Get notifications for disconnects and connects. If I deviate from my desired state I will just call `connect` or `close` or whatever. The next step is payment logic where we have interactions with the control flow of c-lightning. Let’s say if you have an incoming payment but don’t want to acknowledge that one yet because you don’t know whether you can deliver the service or good. You should be able to hold on to that HTLC until you have verified that the delivery works. Once I have the HTLC I can actually make sure that I will get the money eventually but I am not sure that I can deliver the service or good that I’m trying to. Once I’ve verified that I can then accept or reject. That makes refunds a lot easier because we don’t accept payments which we can’t deliver on. Short circuit payments, if you have multiple nodes in a route or the next hop is your own node you could say “Hey I know this node. No need to talk to it.” It will just give me whatever I need. We had a good example of how to load balance over any number of c-lightning nodes so that you can have a virtual node and any number of border nodes that will pretend to talk to this virtual node. The border nodes will terminate that payment and is indifferent which one of these border nodes who talk to the virtual node will receive the payment. Finally external continuations is basically what we could do for cross-chain atomic swaps. If I receive a Bitcoin payment and I don’t know how to forward Litecoin I could tell that to a plugin. The plugin knows my Litecoin c-lightning sits over there so I will just inject this payment as a continuation into another daemon. And of course whatever you can come up with. Plugins should enable you to do loads of stuff and will gradually open up the flexibility of plugins. If you have a use case please come forward and we can talk about enabling that in the library. That’s it from me.


---
title: Getting Started With C-Lightning
transcript_by: Michael Folkson
speakers: ['Rusty Russell']
tags: ['lightning', 'c-lightning']
date: 2019-07-31
---

Getting started with c-lightning

video: <https://www.youtube.com/watch?v=fab4P3BIZxk>

<https://twitter.com/kanzure/status/1231946205380403200>

# Introduction

Hi everyone. We’re actually a couple of minutes early and I think we are going to give a couple of minutes past before we actually start because I think some people will probably be running late particularly with the change in times we had to make after this was announced. While we are waiting it would be interesting to find out a little bit about the attendees’ backgrounds and what they hope to get out of this. There’s a chat window where you can type stuff. Today’s presentation is going to be about half an hour of content but I’m hoping for plenty of questions so you can direct where I should spend the most time. If you ask questions in the chat box then we have a couple of editors, Mario and Daniel will be sorting the questions to direct through to me if we get flooded by them. So I thought what we’d do today is we’d start from nothing. We will start with a new machine, in my case this is a Ubuntu machine we’re running on. We’re going to grab the Lightning source, we’re going to build it, we’re going to set it up, we’re going to set up a little test network and we are going to write a plugin. So basically it is going to start from an empty directory and work our way through to the end there. I think that is useful. We’re going to play around a little bit with c-lightning and give you a feel for how Lightning works and how our implementation works and get you comfortable with the commands. From there we can take any questions you want. Feel free to interrupt during the time with questions because I think that will help again. I should warn you in advance that it is 5:30 in the morning here in Australia. If my typing is worse than usual that is probably why. I’m going to share my emacs screen now. You can see on the screen my cheat sheet of what we’re going to do. 

I will actually open a shell here. The first thing I am going to do is a git clone.

`git clone https://github.com/ElementsProject/lightning.git`

This is basically grabbing the source from where it is hosted on GitHub. We’re getting the whole thing. That’s created a directory called lightning.

`cd lightning`

Normally what you’d do first is you’d look at docs/INSTALL.md which basically walks you through all the requirements. In particular you would usually do the installation line that you can see here. This is my development machine so I have all these prerequisites installed. Let’s assume I have typed that and all those packages have installed. You will also need a copy of bitcoind although you don’t need it synced to the main chain. You obviously would want that for production but for testing that’s completely unnecessary. You just need it installed somewhere. Now we’ve done that you basically just configure and build.

`./configure && make`

The reason that I prefer to grab from Git rather than taking from our prepackaged releases, there are a couple of reasons. The first is that that gives you the very latest bug fixes and latest features. In particular when you are writing plugins we are still flushing out a lot of the plugin APIs. If you are on the latest version you are going to get the new hotness with all the richness that you can create with plugins. We found that to be quite useful. The other reason is that frankly it is really useful to have people testing the latest Git release. It means that you get fixes and updates faster if you find something or if you want something enhanced. Frequently you’ll find there might be some feature that would’ve made things easier for you. You can submit an issue on GitHub or even a pull request if you are feeling adventurous. That can be quite a fast loop to get updates out. We definitely like our testers to be on the latest Git. There we have, we have built c-lightning. If is fairly straightforward. The normal first thing to do is to run lightningd. You can do `sudo make install` at this point or if you set up your permissions you don’t need `sudo`. You can also just run lightningd for test reasons out of the directory. I don’t install lightningd on my machine because of course I am developing all the time, I don’t want to get confused with an old version that is installed somewhere. You can run lightningd.

`./lightningd/lightningd`

The first thing it will do is create a default directory, the `.lightning` directory but it will immediately complain if Bitcoin is not running, it can’t reach bitcoind. Normally at this point we would run bitcoind and connect Lightning to it. But there is a cheat way of doing this. I’m going to show this to you. In the contrib directory there is a script called `startup_regtest.sh`

`ls -l contrib/`

Now regtest mode for Bitcoin is a special mode where it is trivial to generate blocks. It is a great test mode for trying out things. We use it so much that one of the core contributors, Lisa created a helper script here that basically sets up your bitcoind and sets up two Lightning nodes connected to it so that you can run simple tests. You do need to set a couple of environment variables. You need to tell it where your Lightning source is, the path to lightningd and you need to tell it where your Bitcoin directory is. Then you source that and it will create a couple of commands.

`export PATH_TO_LIGHTNING=pwd; export PATH_TO_BITCOIN=~/.bitcoin; . contrib/startup_regtest.sh`

Then you source that and it will create a couple of commands. The most important is the `start_ln` command. It actually starts up two Lightning nodes and if necessary starts up bitcoind. We now have two Lightning nodes running and it gives us a couple of convenience commands. You can see here.

`alias`

It gives us `l1-cli` which points at the first lightningd and `l2-cli` so we can control both of them at once. What it has actually done behind the scenes is create these directories `l1-regtest` and `l2-regtest` in `tmp`. That’s where c-lightning lives in this case. You can see there is the config file, we have a `gossip_store` with no gossip in it as there’s no Lightning Network yet. We have a database file the `lightningd.sqlite3` and of course we have the log. If we look at the config, it creates a very simple config.

`cat /tmp/l1-regtest/config`

It tells it it is on the regtest network, it starts it up as a daemon, it sets the log level to debug. That is useful if you are doing testing but it does produce a very verbose log and of course it tells it where to put that log. I should point out at this point that there is a man page which describes all the options that you could possibly put in your config option. Normally you can just type `man lightningd-config` but because I haven’t installed it I need to use the `-l` flag to point it at the raw file.

`man -l doc/lightningd-config.5`

Here is the lightningd man page which tells you in more detail than you could ever want all the options and bling that you can add to your Lightning node. I do want to highlight the very first option in the man page. This is `allow-deprecated-apis`. By default when you start up c-lightning you get all the APIs including the deprecated ones. We do give at least six months notice before we deprecate APIs if we are changing them. But if you set that `allow-deprecated-apis` to false when you are testing, that ensures you don’t accidentally use some API that is about to go away. I do recommend when you are developing a plugin to set `allow-deprecated-apis` to false and make sure you don’t accidentally stumble over that. There’s our options. Let’s start a channel. What we’re going to do is create a channel between the two test Lightning nodes. In order to that we need some Bitcoin. Fortunately that is really easy to do in regtest mode. We get a new address.

`bitcoin-cli -regtest getnewaddress`

Then we simply tell it to generate to address, 101 blocks to that address.

`bitcoin-cli -regtest generatetoaddress 101 [2NGUJuNTKAD….]`

There you go. We’ve just mined 101 blocks on regtest. That was easy. If we get our balance.

`bitcoin-cli -regtest getbalance`

We now are the proud owner of 50 test Bitcoins. The reason we had to generate 101 blocks is when you mine a block in Bitcoin it takes 100 blocks before you can actually spend it. We need to get that into c-lightning.

`l1-cli newaddr`

This is giving us a Bitcoin address, a modern SegWit style Bitcoin address. We can tell bitcoind to send to that address we’ve got. Let’s send 10 Bitcoin.

`bitcoin-cli -regtest sendtoaddress [copy l1 new address] 10`

Of course it has created that transaction. We need to mine a block so that it is confirmed. Let’s generate another block.

`bitcoin-cli -regtest generatetoaddress 1 [2NGUJuNTKAD…..]`

We should be able to see that in listfunds.

`l1-cli listfunds`

The issue here is of course that lightningd asks bitcoind every 60 seconds or so what is going on in the network, have new blocks appeared. It can take up to the worst case of 60 seconds before we will see the funds appear. There we go. Here we have 10^9 or a billion satoshis. Inside the Lightning Network we denominate everything in millisatoshis so we have a trillion millisatoshis to play with and that should be plenty. If we switch back to our plan. Let’s look at `l2-cli` our other node.

`l2-cli getinfo`

Here’s the node. It has created a random id and a random alias for it. c-lightning by default chooses NSA style names for its aliases but you can customize that of course in the config file. Let’s connect the two. If we tell `l1-cli` to connect to that id.

`l1-cli connect [add id] localhost:9090`

Normally you can just tell it to connect to an id and the gossip network will have spread all the information about where nodes are and how to connect to them. In our case we haven’t set up the network yet so we need to explicitly tell it where to connect to. There we are. It is connected to the other node. Now we can fund a channel.  Let’s spend some of our millisatoshis. We could also do it in BTC or in sats. In this case we will do it in msats.

`l1-cli fundchannel [add id] 100000000msat`

Again we have to wait for a confirmation so we just generate another block.

`bitcoin-cli -regtest generatetoaddress 1 [2NGUJuNTKAD…..]`

If we ask `l1-cli` and we tell it to list peers we can see that this is the first peer that we’re connected to and the channel is awaiting lock-in. It could take a little bit for it to see the confirmation.

`l1-cli listpeers`

In regtest mode c-lightning defaults to only requiring one confirmation for channels to be confirmed. If you are playing on the real network the default is 6 to make sure that the transaction is well confirmed before you can use the channel. There we go. We are now in status channel normal, our funding transaction is locked in and we’ve got a fully functional channel. We’ve got a channel between the two but let’s check that it works. In the Lightning world payments are done by presenting invoices. We use the invoice command. On `l2` we are going to tell it to generate an invoice. An invoice requires three things. It obviously requires an amount although that is optional, you can create an any amount invoice if you want to. It also requires a label. A label must be unique and the reason that the label exists and is unique has to do with robustness. Because we are developing c-lightning as a basis for a robust server side implementation of Lightning particularly it is important that you handle cases where your higher level, say your web store submits a request to create an invoice but the power goes out just after you submitted that request. Now you don’t know whether or not it has processed that invoice or not when it comes back up. By having a unique label that means that you can actually check if that label exists. Then you have definitely created the invoice. If it doesn’t you can create it again. We can call the label anything, we call it `label-1`. We also add a description. The description is human readable and it is something like “Payment for test”. 

`l2-cli invoice 11111111msat label-1 “Payment for test”`

There we go. We have this `bolt11` string which is the important information in this. You’ll notice that we also have a warning about capacity that “No channels have sufficient incoming capacity” to pay this invoice. That isn’t strictly true. Obviously we have an incoming channel and we should be able to pay it. In this case what it is strictly saying is we don’t have a public channel that is incoming. With the Lightning protocol it takes six blocks before you are allowed to announce to the world that you have a channel, it has to be that deeply confirmed. We don’t want to see channels that are likely to be re-orged out. We don’t actually have a public channel at this point. In fact c-lightning is even a bit smarter that even once we did have a public channel it would notice that there are no other public channels to that node. It is unlikely that in a real network that anyone would be able to use that channel to pay us so it would still give a capacity warning. We can ignore the capacity warning for now. There are a couple of ways we can use this invoice. We can pay it immediately but we can also decode it. There are two ways to decode it. There is a command called `decodepay`. You give it the invoice and it breaks it down into all the parts and decodes it for you.

`l1-cli decodepay [add Lightning invoice]`

You can see the network it is on which is regtest in this case. You can see the time it was created, that is a UNIX timestamp and the expiry. In this case we default to having invoice expiry of 7 days so you can pay that any time in the next 7 days. It shows the payee which is `l2` our second node, the amount and that description that we put in, “Payment for test” appears in the invoice. The invoice is a signed contract, it is digitally signed, that says “If you pay me this amount for this thing I’m describing then I will give you a receipt that proves that you paid it. In particular I will give you the secret that hashes to that payment hash there.” The idea being that if somebody can produce that preimage they can prove that this invoice was paid and therefore you owe them whatever it was you described. There’s our invoice, it seems good. Let’s get `l1` to pay it. 

`l1-cli pay [add Lightning invoice]`

Just like that and there we go, we’ve made a payment. Obviously with two nodes directly connected on the same machine the payment is almost instant. If we ask `l1` for `listpays` we can see all the things that it has paid, in this case the one thing.

`l1-cli listpays`

Importantly you can see status complete here. We’ve got the payment preimage, that secret that we swapped for the millisats. There’s the amount we sent and there’s the invoice that we paid. If we ask `l2` we can also do `listinvoices`.

`l2-cli listinvoices`

It shows us the other side. Here’s the invoice, the status is now paid and it shows us things like the millisatoshis received because you can actually overpay an invoice. Sometimes that is important if you are trying to add some noise into the payment amount to make it more difficult to trace where the payment is going. You can actually add a little bit of noise. You do get an amount received field. You can tell when it is paid, you can see the description and when it would have expired. There is also a `waitinvoice` command that will basically wait for an invoice to be paid if you are trying to do backend work that will wait for the next invoice to be paid. Then you can do `listinvoices` after that. We have a working channel and we’ve made a successful payment, that is pretty cool. At this point we’re ready to make our first plugin. I should point out that there is a `help` command.

`l1-cli help`

help basically does what you expect. It lists all the different commands that are available in c-lightning. It is grouped into categories, bitcoin, channels, things like that. There are a few developer commands. If you built your test node with the enable developer configure option you’ll end up with a lot more developer options that are all extremely dangerous but are great for testing obscure scenarios. Shall I pause before we dive in to building our first plugin and see if there are any questions that people want answered.

Q - Can you adjust the default config on mainnet to below 6 blocks?

A - You can. If you look in the lightningd config you can alter that to be lower or higher if you want. But the protocol rules, nobody will accept an announcement of a channel less than 6 blocks old. A peer and I can agree that the channel is ready earlier. Of course both sides have to agree. If you are saying “I want 3 confirms” and they say “I want 6 confirms” you’re going to have to wait 6 confirms before your channel is really open. The broader network won’t accept an announcement of a channel less than 6. If you are looking at receiving incoming payments it is going to be difficult to do until they are 6 deep anyway. 

Q - How do you overpay an invoice?

A - This is a good question. You can actually do it manually. There are ways to create a payment manually which I’m not going to go into now. The `pay` command does it all for you. It looks up the route, creates the route, figures out how to pay. You can actually create a manual payment using one of the lower level commands and actually tell it explicitly how much to pay on each hop. That way you can actually overpay a payment. The spec says that you have to allow them to overpay by a factor of 2. You should reject if it is more than that. I figure if it is more than a factor of 2 it probably means that they’ve done 	some terrible error like they’ve put in satoshis instead of millisatoshis or god forbid Bitcoin instead of millisatoshis. You are probably not doing them a favor by accepting gross overpayment. In fact c-lightning itself will fuzz the amounts. That was accidentally disabled in the last couple of releases but it will be coming back. Mainly because amounts tend to be a round number and if they are a round number it becomes a lot easier for you to make a good guess as an intermediary on where that amount is going, how many hops away you can kind of guess. I know what fees everyone charges so I can guess that it is 3 hops away from me so I can guess perhaps where it is going. If you fuzz the amount a tiny bit users don’t really care. We’re talking about fuzzing by like 0.1\% things like that. But it just masks the length of the path effectively. That’s the reason that we overpay on fees.	 Did that answer those questions?

Q - Plugins seem to go in their own category in help?

A - Yes. Plugins all get grouped together and we did wonder whether plugins should have their own individual categories. In fact you can add categories and plugins could advertise theirs as their own category. If you have a plugin that has lots of options it can actually create its own category and help automatically. By default when a plugin offers an option it goes straight in under plugins.

Now we’ve got a feel for how this works and how to drive c-lightning and the average flow that you’d get. We’re actually going to do what everyone does when they write their first plugin and that is copy from `contrib/plugins/helloworld.py`. This is actually not that simple a plugin anymore but we’re going to delete most of it and save it here. This plugin is written in Python. The Python infrastructure for plugins is pretty mature. It is shipped as part of the `pylightning` library with c-lightning so it is well maintained and it is up to date. It uses a fairly simple method. You create decorators here. You say “I have this plugin method hello”. It takes an optional name, it has this default. The documentation strings become the help in the messages. Basically the function returns something and that gets turned into a JSON response. In this case the plugin also has an option called greeting that defaults to hello. That is our plugin. This is an important step. If we don’t make it executable it will refuse to run.

`chmod a+x helloworld.py`

Let’s go into our `l1` config and add it as a plugin.

`plugin=/home/rusty/text/webinar/lightning-2019-07/helloworld.py`

There is also a plugin dir, a config option which basically says “Scan this directory for things that look like plugins.” But you can also just use `plugin` to specify an exact file. As of about 3 days ago there is actually dynamic plugin support. I decided not to do that because literally while I was testing this I found another bug which is now fixed. It is still a little bit bleeding edge but it will be in the next release. You can dynamically add and remove plugins. One reason that we didn’t dynamically add it is that I want it here in the config so it is persistent. We will do this the old fashioned way. We will add our plugin. We will switch back to shell. We’ve got our plugin and we will stop our nodes and start them again.

`stop_ln`

`start_ln`

Because I didn’t do a `make install` it couldn’t actually find the plugin directory. Let’s kill everything.

`stop_ln`

We will export the Python path. This hack will allow Python to find the plugin directory.

`export PYTHONPATH=‘pwd’/contrib/pylightning`

`start_ln`

There we go.

`l1-cli help`

We should see underneath plugins, we now have this, `hello`. It has integrated the plugin into the help. It has taken the argument name here, `name` and made that an optional parameter. You can tell it is optional because it has a default.

`l1-cli hello`

It is “Hello world”. We can give it a name, “hello everyone!”.

`l1-cli hello everyone!`

That’s our plugin in action. Now you also noticed that added an option. If I run lightningd and I give it the `lightning-dir` pointed at the right place.

`./lightningd/lightningd —lightning-dir /tmp/l1-regtest/ —help`

You’ll see down the bottom here it has got a new argument `—greeting`. That means I can use `—greeting` on the command line when I start it. It also means that I can put it in the `config` file. In our config file we could put `greeting =` some other greeting. This shows you how integrated plugins are. From a user point of view there is no difference between c-lightning itself and the plugins that surround it. This is really important. It means we can concentrate on making c-lightning the most solid and robust base that we can. We can do more flexible and extensible things on top of it. In fact the `pay` command itself that you saw me use earlier is in fact a plugin. It was originally part of c-lightning and we moved it out. It does actually do some quite complicated things. It made more sense to be a plugin. It is a plugin written in C but there is no reason that it couldn’t be written in Python as well. It also means that you could write your own `pay` plugin which may have different characteristics. There’s our greeting, there’s our plugin working. That’s a pretty boring plugin. It works but it doesn’t do anything interesting. We’re going to make it a bit more interesting. We’re going to use the Lightning Millisatoshi plugin. This is the thing that handles all the msat, handles parsing of millisatoshis. I strongly recommend that you do something like this whatever language you implement your plugin in because consistent handling of financial amounts has been a bug that has bitten pretty much everyone in Bitcoin. It has certainly bitten us before. I have funded channels by the wrong amount in early versions of c-lightning because the channel funding was in satoshis not millisatoshis which is one of the reasons that we changed everything to be consistent. If you have consistent money handling it just makes things a lot easier. We are going to call our plugin method `balance`. We’re going to write a balance routine which prints our balance. We change the name, we say “This gives you your node balance.” You don’t need an option anymore. We’re going to do a RPC call. A very common thing for plugins to do is to actually call back into c-lightning to get information out again. Of course plugins can also call other plugins and build on those. We are going to give two parts to our balance. We are going to give an onchain balance which is how many funds you’ve got on the Bitcoin chain and also a Lightning balance, how many funds you’ve got available in channels. If we do a `listfunds` you can see it looks like this.

`l1-cli listfunds`

It lists the outputs and it lists the channels. What we want to do is we want to iterate through those outputs and we want to add up these amount msat values which shows how much money we’ve got. Where the output is in status `confirmed`. Then for our online funds, our Lightning funds we want to iterate through our channels and we want to look at the `our_amount_msat` field here which shows how much we are holding in the channel. To save me typing I have done this before. It works something like this. I call this reply. You can see that it is basically summing up those fields where the status is confirmed. The default if there is nothing is millisatohis of zero. Similarly for the Lightning amounts and then we `return reply`. If I haven’t some horrible typo I should simply be able to restart.

`stop_ln`

`start_ln`

`l1-cli balance`

Great, so we got an error. This is an opportunity to show you what happens when you get an error. You look in the log. We’ve got the final line of the Python error but if we look in the log.

`~text/webinar/lightning-2019-07/lightning/tmp-l1-regtest/log`

Down the bottom you’ll see the full traceback. Anything that your plugin spits out to standard error gets logged as coming from your plugin. Basically we can see on line 12 of our plugin Rusty made a typo. 

`funds = plugin.rpc.listfunds()`

`stop_ln`

`start_ln`

Let’s try balance.

`l1-cli balance`

There we go. It has given us our balance and we’ve written our first plugin. That is pretty nice. If we do `help`.

`l1-cli help balance`

It actually tries to look up a man page for that. The first thing when you ask for help with a command it refers you to the man page which is more detailed. If that fails it falls back to asking lightningd. We can see that this is our comment, we can see our category and the verbose description which is the same as the existing description. That is a pretty horrible output. We can neaten it a little bit by changing it to `Millisatoshi(0)).to_approx_str()`. This gives a three decimal place approximation. Let’s do that.

`stop_ln`

`start_ln`

And get our balance.

`l1-cli balance`

That is a little bit prettier. It has done some rounding. We’ve got a prettier output at that point. That may be readable to you and me. We’ve got 10 Bitcoin and we know that’s a lot but it is not all that useful. Really what we should be doing is giving some sort of fiat representation as well. Fortunately this is Python so it is surprisingly easy to do. We are going to import a couple of packages that do the magic for us.

```
import requests
import json
```

We are going to call out to one of the places that will offer a API that does this, bitcoinaverage.com for example has an API that converts. 

`def balance (plugin, currency=‘USD’, prefix=‘USD \$’):`

This basically just gets the Bitcoin price and from there we need to float that. We convert to BTC, turn it to a float, multiply by `fiat_per_btc`. I’ve put it into a format that starts with a prefix so it looks pretty. Again we will do the same thing for our Lightning balance. If I haven’t made any typos let’s see if this works.

`stop_ln`

`start_ln`

It started, that’s always a plus. If you’ve got any gross typos in your Python it won’t get to that point.

`l1-cli balance`

I messed up. I deleted the line where I did this `reply = {}`

`stop_ln`

`start_ln`

`l1-cli balance`

There we go. We have our onchain and Lightning balance. That means that I’m test rich. This is of course test USD not real USD so I’m afraid I don’t have \$100,000 dollars on my laptop. That pause is where it is doing the web request. Obviously this is a very naive plugin, it is going to do a web request every time I ask for the balance. You probably want to poll it over some longer period in practice to avoid that delay. Let’s try changing the currency. If I want to feel richer I can do in Australian dollars.

`l1-cli balance currency=AUD prefix=‘AUD \$’`

There we go. We feel even richer now. I have \$12 on Lightning and 138,000 made up Australian dollars. I think that emphasizes to you why plugins exist. Plugins can do things like web requests, serve web pages, do AI, deep learning, whatever it is that they need to do which isn’t really stuff that we want in a robust core of our implementation and yet are really important and really usable. This was the reason that we decided to implement this whole plugin infrastructure, that you can go away in any language that you choose: C, Go, Python obviously,  I believe someone has done some work in Javascript to write plugins. You can obviously create your own infrastructure that builds whatever you want using a fairly simple API on top of c-lightning itself and interacts. That API is becoming richer all the time as people come up with new things that they want to do and we expose more functionality to plugins. I know that was quite a blast so I’m going to go back and pause for a moment. I might stop screen sharing and return to video. It was cool to see me typing in emacs for all that time, hope you are still awake. Let’s start at the top.

Q - Is it possible to pay an invoice with many payments?

A - It is interesting actually, that was what I was working on just before. There is an update required to the specification to allow you to use multiple payments in parallel to pay something, we now call it multipart payments. It used to go by the name AMP. We love our energy and Lightning puns hence the name AMP, atomic multipath payment. That is something that is coming in the new revision of the spec. It has been drafted and I expect implementations to start reaching fairly soon. Obviously then both ends will have to support it. The end receiving the payment and the end sending the payment will both have to support multipart payments. That is certainly something that we’ve seen is important for people to be able to split their payments into multiple parts. At the moment it needs to be a single payment that covers the whole amount but fairly soon in the next few months we will start to see it rolling out that you can pay it in multiple parts.

Q - Can you expand on how a plugin could call AI?

A - Basically there is already a plugin called `autopilot` that is designed in theory to maintain your channels for you. It can choose which nodes it should connect to, which nodes it should open channels with, how much fees it should charge for those channels for things routing through, when it should close them down etc. That is an infinite problem. You could certainly do any number of backend processing for that kind of thing. That is an example of a plugin that could use AI. At a higher level it depends entirely on what your application is. It could be arbitrarily complicated.

Q - Can you build full smart contracts in LN using plugins?

A - Anything that Lightning Network can do you can pretty much access using plugins. You can certainly do some really interesting things with plugins and I think we are going to see more people explore that. In terms of smart contracts it is probably too vague for me to answer in this forum. If you have specific idea I would happy to answer whether that is possible.

Q - The network won’t accept below 6 blocks. Is that a c-lightning software requirement or a spec requirement?

A - It is a spec requirement. In the spec you don’t accept announcements of channels that are less than 6 blocks old. It is simply for the robustness of the network.

Q - I recall Christian showing a `getroute` method. Is it still possible to simulate routing in regtest?

A - Yes I’ve only set up two nodes but you can set up a lot more nodes. My laptop should be able to handle a couple of hundred nodes pretty easily now. You could actually create a massive number of nodes and actually connect them to each other. There is actually a cheat way of doing it. You can have a canned set of announcements that you can feed into a node that tells it about this entire network out there that exists. It just happens that it is not connected to it. For things like simulating routing which is what we did with the million channels project we actually created this whole canned blockchain as if it had been created by 300,000 nodes. All the gossip messages that you would send, you’d connect to this network, you’d get all these gossip messages and you’d find out about these million channels that were out there. That’s how we did that. That is all done in regtest.

Q - How many channels can be opened between two nodes?

A - In c-lightning we only implemented a single channel between two nodes rather than implementing multiple channels. The reason is that it is important for the spec that you can upgrade an existing channel. At the moment in version 1.0 there was no mechanism to upgrade a channel. You’d create a channel, if you wanted to increase the size you would tear that channel down and create a new one. This is obviously suboptimal. One of the things in 1.1 is this ability to upgrade a channel on the fly. You can add funds, you can remove funds from a channel as well. You can pay someone onchain for a channel that is between the two of us where we could put some money into cold storage whatever it is. We could also bring money on and add to the channel. That’s where we see the Lightning Network going. That’s obviously something that we want to do. Resources are finite so because we haven’t had that in the meantime a number of people have gone and implemented multiple channels. Multiple channels are less efficient than having single channel. We really want to spend the engineering effort on getting that channel upgrade, splice in and splice out of existing channels working, rather than spending time implementing multiple channels. I know unfortunately it has taken longer than we would hope. In the long run that is how we will have multiple channel support. Also from the point of view of the network itself it is healthier for the network if you open channels to multiple different people rather than putting multiple channels into a single party because it makes the network more robust. And it is a better experience for you because now you are no longer relying on a single counterparty, you are reaching out to multiple people. One advantage that it has had of forcing you to have a single channel per peer is to think harder about your peer selection so that people have connections to more peers rather than doubling down on the same single point of failure.

Q - Multipath or multipart?

A - Both. If we are talking about payments that can be split into multiple parts, those parts will ideally go down different paths. There is very little point in having multiple on exactly the same path. You’d want it to go all the way around.

Q - In what order are we getting these features: spliced channels, watchtowers, coinjoin, channel factories?

A - Spliced channels requires more specification work. That is not actively being worked on because there is a whole heap of other things in the spec that are even more important that are ahead of it. I can’t even give a vague estimation for that. Watchtowers, some implementations already have watchtower support. I’m not incredibly delighted. The watchtowers at the moment are a little bit simplistic and I would like them to get more sophisticated. On the c-lightning side, watchtowers are really important if you are mobile app and stuff like that. If you are light client you may be less reliable. On the server side watchtowers are probably such a high priority for us because we tend to be talking about deployed infrastructure. You are not going to have a one week downtime. Watchtowers are definitely coming in general. I hope to see an open specification for watchtowers. If not I’ll have to write one so we can all interoperate and we can all share watchtower infrastructure. Ideally the purpose of watchtowers is not that they do anything but they have to exist. A watchtower is a fallback so if you and I have a channel you are not going to broadcast an old state that is in your favor because for all you know I’m using a watchtower and the watchtower will penalize even if I’m not online. The watchtowers need to exist but because you don’t know if I’m using a watchtower or not they have a preventative power just by existing. It is interesting game theory that you need watchtowers to exist, to be out there but you don’t need a huge number of them. You just need them to be reliable enough to discourage these kind of cheating attempts. coinjoin channel opening, oh wow. In 0.7.1 the last release of c-lightning we actually changed the infrastructure to separate channel openings so you can actually fund a channel from an external wallet which opens the door to doing things like a coinjoin directly into a Lightning channel. As far as I know nobody has implemented that but that’s the perfect kind of thing to write a plugin for. This is where we increasingly see ourselves implementing infrastructure at the low level and letting people implement plugins that use it to do really cool things. I would love to see a coinjoin channel opening. Somebody also has a demo of doing single transaction, multiple channel opening which would have been really useful for me the other day when I was trying to open a whole heap of channels for test purposes. The classic example of where we had to implement the infrastructure to open things up so plugins could go on and do interesting things like coinjoins. In what order they are going to appear? Watchtowers are there today so they’re first. Coinjoin channel opening, it depends on when somebody writes the plugin. Spliced channels is probably a little bit further down the road.

Q - When are we going to see advanced MPP?

A - There is no advantage to advanced MPP, in fact I think it is a bad idea. The problem with advanced MPP ideas is that you no longer get a receipt. You no longer have the invoice connection. When you make a normal payment you present me with an invoice, I get the preimage which is a cryptographic receipt which shows, and I can prove to the world, that someone paid this invoice. That’s not so important today because the Lightning Network is small and we all kind of trust each other. But when you look at real commerce, when you start using this thing in anger and between untrusted parties which is what it is designed to do, having that cryptographic receipt and invoice becomes incredibly important. There is no third party sitting between you and the vendor. You need someway of proving that the payment has been made and what the payment was for. Invoices are incredibly important in the long term health of the Lightning Network. The problem with the atomic multipart payments as originally proposed was that there is no longer invoice connection. Instead of them revealing the secret to you in return for a payment so that you can use that secret to prove that you paid, you actually provide them with the secret. This loses the ability to prove that you paid at all. That is ok on the current network but I think in the long run that is the wrong way to go. I think actually basic MPP is more powerful in many ways. There’s actually very little reason to do anything more “advanced” because you lose abilities rather than gain them. The thing you do gain however, to be fair, is you obscure the different payments. If somebody sees two parts of the payment they can tell this is actually the same payment at the moment. If you naively split it then they can tell that the payment hash is the same. They know this is the same payment going through. It gives you less ability to obfuscate your payments by splitting them up into different amounts. That itself is solved by another change that is coming, not even in spec 1.1 perhaps 2.0. Scriptless scripts allow you to decorrelate payments altogether. That is even more ambitious and that requires Bitcoin changes such as Taproot and things. There is another step beyond that where we get an even more powerful ability to obscure payments. At the moment anyone on the payment path can tell that it is the same payment going through. If you see two points on the path you can tell that’s the same payment trivially. Decorrelating that is also important. If we get that we no longer need these other techniques anyway. So Base AMP is actually quite a powerful technique.

Q - How far away are we from being able to transact Liquid tokens via c-lightning?

A - This is a really good question. Christian has done the leg work to integrate Elements into c-lightning but he did for L-BTC. It is very simple. It basically changes the internal formats to the Elements format obviously. The transaction format for Liquid Elements is different. It has confidential transactions, that needs to be handled. That work has been done. We can now do Lightning L-BTC. The next step is to do assets. When you’re doing Tether it is an asset on L-BTC and we don’t have a timeline for that work. It is obviously seen as something that we want to do but it is not something that is an immediate concern. In practice Liquid offers people fast enough things that they don’t really need what people see as the killer app of Lightning, that incredibly fast settlement. It is not too bad on Liquid. At some point obviously, this is an exciting area and something we definitely want to do which is tie the two together. One of the reasons that there is 3 people at Blockstream working on Lightning, there are two reasons really. It is an interesting complement to Liquid and we see that in the long term, the ability to atomic swap in and out of Liquid was mentioned in the original Elements paper that I think is really powerful. But also because this is bringing the whole community forward. We do a lot of work on specification itself and editing that and making sure that all the implementations play nicely together, that we all move forward together. We get the best ideas we can. That for me is incredibly exciting. We play both parts and sometimes it is not more spec work and low level work and stuff like that. Sometimes it is more complementary with what we are doing. At the moment there is a huge burst of spec activity. We are mainly focused on all the stuff that is in 1.1, all these cool new features that everybody wants, making sure that they are spec’ed reliably and they interoperate and are all robust.

Q - Autopilot scares me 

A - It scares me too, I tried using it the other day but I tried to neuter it so it didn’t do anything. I wanted it for advice. I think at this stage autopilots are much better in that mode. I’ve got some funds, I want to open a channel, where do you think I should open? Have it tell you where it thinks you should go. Maybe poke around, take a look and maybe that’s ok. The idea of autopilot taking all my funds, even though this is my testnet node and that’s what the funds are for. I’d hate to come up one day and discover that it has wildly created and torn down channels because it has gone haywire and I’ve lost all my Bitcoin to fees. I also am nervous about autopilots. On small levels like doing auto-rebalancing much better. At the moment most of our plugins head towards at least by default being more conservative. They’ll give you a suggestion and you’ll go and do it manually. If you want to close that loop by writing a cron job that every minute asks for suggestions and implements whatever it says then that is up to you. This is a disclaimer that I should have made at the beginning. Lightning is still alpha or beta software depending on where you are on spectrum. You should never put more money than you’re prepared to lose into your Lightning node. Over the last few months with the price increase I am probably guilty of doing that myself at the moment. Fundamentally this is software, software breaks, stuff happens and I really want your bug reports but I don’t want your tears. Small amounts of money, good. Playing around is great but putting your life savings into a Lightning node is not going to end well so just be warned.

I hope you’ve enjoyed this. I know it will be uploaded to YouTube afterwards. Thank you everyone for the excellent questions. I think that really helped. We should definitely do this again.


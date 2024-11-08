---
title: JSON Interface with c-lightning and Writing Extensions
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
speakers:
  - Rusty Russell
date: 2019-04-06
media: https://www.youtube.com/watch?v=sNB1N7FyMHA
---
<https://twitter.com/kanzure/status/1230892247345852416>

## Intro

Ok I have `top` running. We have a plan and we’re going to start from zero. We’re going to clone c-lightning, we’re going to compile it, we’re going to set up a test node. I’m assuming Bitcoin is already installed. We’re going to talk a little about configuring it and stuff like that. All this stuff is useful to see somebody else do. It is documented but it is nice to see someone actually go through it. Then we’re basically going to create a little project. We’re going to create two of these nodes, we’re going to get them to talk to each other so we’ve got a play area to play with. We’re going to stumble across a bug and show you what to do when you hit a bug in c-lightning. We’re going to deep dive into that. We’re going to talk a little bit about JSON and stuff like that. That’s the first half. It is all that infrastructure stuff and setting up and how things work. Then we’re going to write our plugin, the world’s stupidest plugin. Once we’ve got as far as we can with the world’s dumbest plugin and we have an idea of how plugins work, we’re going to step up and write a real plugin, deliberately leaving it a bit unfinished so you get an idea of things that you could do with plugins. I would encourage you to ask questions on the way through particularly if I go through something too fast. We’ve got fifty minutes so hopefully we can get through most of this. I’m going to go into my temp directory.

`cd /tmp`

`git clone https://github.com/ElementsProject/lightning.git`

As a general rule, with c-lightning we do do releases but it is always more fun to run on master. It should be reasonably stable. I tend to run my nodes on master or pretty close to simply because I like the extra testing. If you’re doing development it is nice to be on master. We’ve got Lightning, it’s master version.

`git describe`

We’re 81 commits past 0.7.0. This is the latest and greatest.

`less doc/INSTALL.md`

If we look at the docs it has a lot of stuff including install. It basically tells you how to install on Ubuntu. You install all these things. You obviously need Bitcoin. If you’re doing development you might want to install these things too so you probably do want to do that. Obviously this is my development machine so everything is already installed. It will then tell you to configure and make. I would recommend enabling developer.

`./configure —enable-developer`

That adds a whole heap of dev options which can let you do weird and wonderful things to lightningd. We run our configuration step, that takes a few seconds and then we build.

`make -j7`

This will build the whole project, it’s not all that big so it shouldn’t take that long. It does have some external dependencies which it will pull in. That is what takes a lot of the time from the very first build. While that is building we’ll talk about how we’re going to do this. By default when you run c-lightning it operates out of your home directory in a .lightning directory. Since we want to run multiple copies we’re going to force it to operate out of temporary directories for the moment so we can run two of them at once. The way c-lightning is designed is there’s a central daemon and a whole heap of subdaemons. This is done for security because each peer gets its own daemon after the initial handshake. Should anything go wrong with a specific peer they can only mess themselves up, they can’t mess up the other peers at least in theory. We get some increased isolation from that model. That’s why when you see c-lightning running you’ll see some subdaemons running. I’ll show you that as well. We’ll also fire off one daemon per client that is connected. They are pretty lightweight so it doesn’t actually make a difference. You can still have thousands of peers without a huge problem. We can see it all building here, it is pretty verbose. Because we’ve enabled development we’ve got a whole heap of debug options sitting in there as well. Maybe I should have used one of my build machines that’s faster than my laptop for this. It won’t actually take too long. While it is doing that we’ll create some infrastructure. As he says that it’s finished.

`make install`

That will install a… bin by default. I’ve set up permissions on my machines so that you don’t have to be root to write in there. All those Lightning things are enabled. The first thing we need to do is run bitcoind. bitcoind has a regtest option which is basically a limited test network. That’s great for testing on your local machine.

`bitcoind -regtest &`

We fire that up and make a couple of directories. Let’s call them l1 and l2 for our daemons and then we run lightningd.

`mkdir /tmp/l1 /tmp/l2`

`lightningd —network=regtest —lightning-dir=/tmp/l1 &`

That’s lightningd firing up. It is spitting out a whole heap of stuff. It has chosen itself a random secret and a public key and derived a NSA style codename from it. If you are on the developer version the name of your node also gets appended to the version you’re running. If you don’t enable developer and configure you’ll just get a random name. One thing people often do…. It has populated the /tmp/l1 directory at this point. It is having trouble with fee estimation as you can tell. That will happen because regtest doesn’t do fee estimation and nothing is happening.

`ls -l /tmp/l1/`

If you look in tmp/l1 it has created a store where it holds all the gossip which just has a header at the moment because there is no gossip on the network. The hsm_secret is the secret that you need to keep secret because from that is derived all the stuff that your node signs. That 32 bytes is important to back up and something that you’d expect to see. It creates a pid file that shows that it is running. It creates a database, sqlite3 database which is pretty standard. It has the lightning-rpc socket and this socket is basically how the command line tool talks to lightningd and how any other tool that you write will talk to lightningd. If we look at the tree, I told you before that it is a heap of subdaemons.

`pstree -p $(cat /tmp/l1/lightning-regtest.pid)`

Here you can see lightningd and there’s lightning_connectd. That’s the one that is responsible for when you ask a connection to come out and when somebody connects in. It sorts out the handshake, who they are and figures out what daemon to hand them to. There’s gossipd which is responsible for all the gossip. It controls routing, it controls gossip about chatting about routing to other nodes and things like pings and stuff all go through gossipd. There’s the hsmd which is the hardware security module that controls all the secrets. It does all the signing, all the cryptographic operations that require knowledge of the secret keys. There is a pay. There is one plugin that we ship by default called pay that implements the pay command which is important.

Q - What’s the advantage of using regtest over testnet?

A - Testnet you can’t control. With regtest I can generate a block whenever I need. I can tell bitcoind generate a new block which is great for testing stuff. With testnet other people can create blocks, it can be significantly more difficult to create a block. People can create blocks randomly outside your control, can fork the network, all those sorts of things. When you want that level of control you do regtest and it’s your private testnet. I tend to test on regtest and then I jump onto the live network. Testing on testnet, it can be interesting if you’re trying to do big tests between remote people on different implementations. But for testing one implementation regtest is way easier.

Let’s run lightning-cli now. I’ll just clear out the spam.

`lightning-cli --lightning-dir=/tmp/li getinfo`

I have to tell it what lightning dir to talk to because it will put it in the wrong place by default. This is the information about our node. You can see its ID here, that’s its public key. We have the alias. Each node gets an alias and a color. You can choose those, you can copy other people. There is no security around that at all. The color by default as you can tell is red, green, blue and it is taken from the first three bytes of your ID. We’ve chosen how many peers we have, how many channels which are all zero. The addresses that we advertise to the network, which is currently none. The bindings which is where we’re listening to which is basically ipv4 and ipv6 localhost. The default Lightning port is 9735 which is actually the unicode codepoint for the lightning symbol. That’s the port that we self assign for the Lightning protocol. The version, the block height we’re on, regtest is 333 blocks in, what network we’re on, how many fees we’ve collected. That’s a nice summary of how your node is going. This is going to be really painful to type so let’s create some aliases.

`alias l1=‘lightning-cli —lightning-dir=/tmp/l1`

`alias l2=‘lightning-cli —lightning-dir=/tmp/l2`

That’s going to make our life just a little bit easier. We should pimp our node a little bit.

`l1 stop`

We will stop our node and we will edit the config file. We might as well tell it that we’re going to be in regtest. We will tell it that we want log-level debug. Log-level debug is really spammy but it is good for trying to figure out what is going on. We’ll also tell it to log into a file rather than spamming our console.

```
echo network=regtest >> /tmp/l1/config
echo log-level=debug >> /tmp/l1/config
echo log-file=/tmp/l1/log >> /tmp/l1/config
echo rgb=ff000 >> /tmp/l1/config
```
Let’s set the color. Anyone have a suggestion for what color they want? Everyone likes red right? All red, no green, no blue. And an alias? Up to 32 bytes, can be UTF-8. Anyone want to type a suggestion for an alias name? Satoshi, ok. Not very original but you win by being first.

`echo alias=‘satoshi’ >> /tmp/l1/config`

There is a really important option which you should always run when you’re developing against this stuff which is to disable deprecated APIs. Our JSON API changes sometimes and what happens is we give at least one major version 6-12 months before we remove old options so that your users don’t get screwed over when they upgrade. When you’re developing you should always disable all the deprecated APIs to make sure you’re not accidentally using one. By allow-deprecated-apis=false it gets rid of any JSON APIs and other APIs that are now deprecated. You should always put that in your config when you’re doing testing.

`echo allow-deprecated-apis=false >> /tmp/l1/config`

So let’s restart our node. We no longer need any of these options except to tell it where the configuration directory is. It is much quieter now which is nice.

`lightningd —lightning-dir=/tmp/l1 &`

`l1 getinfo`

We’ve got our alias as expected and our color. That’s all pretty good. I will note that there are actually some pretty good manual pages.

`man lightningd-config`

If it is not installed correctly you’ll need to do:

`man -l ~/devel/cvs/lightning/doc/`

This documents all the options that you can use. I talked about the difference before between addresses and bind addresses. This is something that people get confused over so I want to address it now. When you gossip on the network and tell people about your node you give them the address to connect to. By default lightningd tries to guess what that is. It binds to port 9735 and tries to work out if it is a public IP address or a private IP address, a loopback or anything else. If it looks public it decides to advertise that by default. But you can have weird set ups of proxies and NAT and everything else in which case you need to specify explicitly what addresses you want. There are three ways of doing it. One is to say address = IP address, port or Tor address or something like that. That is the address to bind to but also if it is not obviously wrong, like it’s a loopback address, that’s also the address that you should advertise. There’s also an explicit way of saying “No bind to this address and advertise this other address.” You can specify bind addresses and advertised addresses separately if they’re completely different. You could say “Announce this address but bind to these addresses.” You can have multiple of those. As soon as you specify any of those, it turns off the automatic address. You won’t get it binding to port 9735 at all. You can turn autolisten back on. Sometimes you might want that. You can also set the proxy if you’re using Tor and stuff like that. There’s a whole heap of options in there that you can read at your leisure. Let’s start another peer.

`lightningd —lightning-dir=/tmp/l2 &`

We’ll watch it fail and it fails because it is by default trying to use the same port. We obviously need a separate port for that. There is an extension. Instead of binding to a IP address you can tell it to bind to a file. That means that you’ll have to be on this machine to even connect to it as a peer which can be really useful. At this point we’ll see a bug.

`lightningd —lightning-dir=/tmp/l2 —addr=/tmp/l2/peer`

When something bad happens you’ll see a backtrace like this. These are the things that you usually send on our bugtracker or come to IRC and say “Hey Rusty. Look at this pastebin with the bug that we’ve found.” I found this the other day whilst testing. I am going to briefly show you if you’ve got a bug and you want to chase it down, how we do that. If you remember, we built this with developer options so we can add to this. Then you can tell it what daemon to debug.

`lightningd —lightning-dir=/tmp/l2 —addr=/tmp/l2/peer —dev-debugger=connectd`

What it will do is by default it runs up its own terminal with gdb in it to attach to that daemon just after it has started up. Because Ubuntu tries to be secure you have to do this.

`echo 0 | sudo dd of=/proc/sys/kernel/yarn…..e_scope`

This time gdb will mange to connect. So gdb is connected. It failed for a different reason because we didn’t have the port that we told it to use.

`rm /tmp/l2/peer`

`lightningd —lightning-dir=/tmp/l2 —addr=/tmp/l2/peer —dev-debugger=connectd`

Here we can see it aborted. Here is the line where it aborted, line 997. We can poke around and see what’s wrong. That’s supposed to be false and it’s true. As it happens this is because I used an unsupported option and this is a bug that I have a fix pending for but I deliberately didn’t fix it so that we could look at how you would track down this kind of thing. This allows you to open it in debugger, you can do all kinds of things like look around the source files, go up a level and see what’s being called and stuff like that. In this case the workaround is easy. We do bind address. The reason it is asserting is because it is trying to advertise this address but this is a local address. This should never happen. It is a bug. A bind address does what we want.

`rm -f /tmp/l2/peer; lightningd —lightning-dir=/tmp/l2 —bind-addr=/tmp/l2/peer`

It is upset about bitcoind. The reason that happened is because we didn’t tell it what network to use. It was trying to connect to the testnet network.

`rm -f /tmp/l2/peer; lightningd —lightning-dir=/tmp/l2 —network=regtest —bind-addr=/tmp/l2/peer &`

There we go, we’ve got a juniorset, that’s our second node.

`l1 getinfo`

 We have two nodes now. As you can see l2’s binding address is a local socket there. Now let’s connect them together. We can tell l1 to connect. In order to connect to a node you need to know its keys so you can do a cryptographic handshake. We say connect to that @ the filename which in this case is a local socket rather than an IP address.

`l1 connect 2019-04-07T01:23:19.754Z`

That’s connected.

`l1 listpeers`

We can see it is connected to l2 and l2 is connected to l1. If you ask each one it is connected to the other one. So this is pretty low level. This format here is JSON, the Javascript Object Notation. We’re going to get spammed by l2. Let me restart that. Let’s rerun l2 with a log option to kill that.

`rm -f /tmp/l2/peer; lightningd —lightning-dir=/tmp/l2 —network=regtest —bind-addr=/tmp/l2/peer —log-file=/tmp/l2/log &`

Now let’s look at listpeers.

`l2 listpeers`

It is currently disconnected. Let’s connect again.

`l1 connect 02c3f6c70fa61f5032f9ac5ec28185cf233d62cd99d71fdf364a899d623313e42e@/tmp/l2/peer`

`l1 listpeers`

Ok this is JSON. JSON is pretty simple key-value pairs. We have open curlies for objects and we have square brackets for arrays. It is pretty easy to deal with in almost every language. That’s why we use it. The real reason we use it is that bitcoind uses JSON, not because it was a deep choice where we considered all the options. That was what bitcoind did. We’ve fired up our peers and connected. Let’s create our first plugin. I’m going to do something really dumb that you should never do which is create a plugin in shell. That’s just because this is a really cheap demo.

`cat > /tmp/plugin.sh`

Whatever it gets it will put into plugin.log. We need to make it executable.

`chmod a+x /tmp/plugin.sh`

That’s the world’s stupidest plugin. Now let’s stop l1.

`l1 stop`

You can either specify a plugin directory and it will look for everything that is executable that looks like a plugin in that directory and fire it off or you can specify a specific plugin which is what we’ll do here.

`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.sh`

The old one has died. Let’s look in /tmp/l1/log.

`cat /tmp/l1/log`

It hasn’t done anything yet, that’’s strange. Let’s do pstree.

`pstree`

I’ve got a lot of crap. We told it to dump stuff in plugin.log. It has sent this JSON message to our plugin. Our plugin of course is stupid and doesn’t respond. What will in fact happen is that after 60 seconds it will give up on the plugin and refuse to start. Plugins have to respond to `getmanifest` and `getmanifest` is where the plugin says “Here is what I support.” There’s the failure. plugin.sh failed to respond to `getmanifest` in time and something is badly broken. `getmanifest` should be really fast. We know what it is going to send us for `getmanifest` and we can follow our slightly ridiculous example a little further. We can actually respond to `getmanifest`. We’re going to do this and then abandon this really stupid plugin.

`vi /tmp/plugin.sh`

We need to get the ID. Every JSON RPC command has an ID. We read whatever they send us until we get an ID line and they go “Ok that’s great I will respond with that ID.” In response to the stuff that it has asked us we tell it what options we support. In this case `dumboption` and what methods we supply and we call it `dumbmethod`. Anything else it sends we put into the log again. Let’s do `--help`.

Here it lists all the options that lightningd takes and you can see down the bottom it has added `dumboption`. It has queried our plugin and our plugin has gone “Yeah we’ve got an option called dumboption.” It gets integrated into the help message. It also adds a new method called `dumbmethod`.

`l1 dumb method`

It hangs because our plugin is complete crap and doesn’t answer anything.

`cat /tmp/plugin.log`

There’s the rest of the `getmanifest`. We sent back a joke manifest. Then it said to initialize ourselves and then it has handed us this dumb method and it is waiting for a response which is obviously never going to come. The reason I like introducing plugins at the really low level is if you try to debug something because it is going terribly wrong you will see this JSON flying back and forth. You’ll see it in the logs, you can log it out of your own daemon, stuff like that. You will get exposed at that level, to the JSON that is going past and it is nice to see. If you manage to screw up and produce something you can’t parse you can look at it and see what is going wrong. The other interesting thing here is that when your plugin gets initialized, it goes through and asks all the plugins what they support so it can build up options and then it initializes them all. It tells it what directory you are operating from and where the RPC file is to connect in if the plugin itself wants to make JSON queries to the Lightning daemon. You get those two by default and usually you read those out. At this point it is time to stop playing around and write a real plugin. The standard way to write a real plugin is to take the contrib plugins, hello world plugin and make it your own.

`cp contrib/plugins/helloworld.py /tmp/plugin.py`

In this case we will call it `plugin.py` and this uses the Python library so you need pylightning installed. You can either `pip3 install pylightning` or you can install it directly like this.

`cd contrib/pylightning && python3 setup.py develop`

That installs it locally so you’ve got a local version of it running. Now let’s `l1 stop`.

`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py`

This is the default hello world plugin that will run in the background.

`l1 help`

Here you go. You can see it has got a hello, that’s the hello plugin. It just provides a hello function that echos back what you want. This is important. From a user point of view plugins are part of c-lightning. They have exactly the same power that anything has that is built into c-lightning. In fact that is one of the reasons we’ve moved pay out. Over time we are going to move more stuff out to plugins. In particular we are going to enhance the RPC API so plugins can do more powerful things. That is something that is actively going on now in development which is why it is good to look at master. But it also means that if you are writing a plugin and you want something, it is a really good time to ask us and say “Hey I wish I had a plugin that could do this. Could you add a RPC call?” We could discuss what’s the best API because we are going to have to support it for a while. To make plugins more powerful, eventually most of the power of c-lightning is going to move out to plugins.

We’ve got this little plugin in Python which is probably the easiest way to write a plugin.

`vi /tmp/plugin.py`

Basically `from lightning import Plugin` it starts up a plugin and you have these annotators that say what methods you have. That’s the hello method, that’s the documentation. It gets a greeting option and it basically just prints it straight back. Here’s what happens when it initializes, it doesn’t do anything apart from print out hello world. You can also have subscriptions. Subscriptions are basically things that you tell in your manifest, you say “Hey lightningd I want to know when these things happen” and it will call you and notify you. Currently there are connect and disconnect. There are a lot of others coming. It’ll show you what happens when peers connect and you can whatever you want there. We don’t really need those subscriptions, we can delete them. Here’s an option for example `—greeting` defaults to hello and tells you the greeting it should use. You can run `lightningd —greeting`. Anything that you can specify in the command line you can also specify in that config file. Instead of `—greeting` you would just `greeting=config file`. One of the coolest things about Python is you can do this.

```import threading```

We want to do a web service. We want to provide a web API. I completely cut and pasted this from the really good documentation for Flask.

`app = Flask(_names__)`

Flask is basically a web server inside of Python programs. I turned debugging off.

`app.debug = False`

Then you tell it what to serve. You annotate again.

Inside our thread when we get emitted we will start the Flask thread as daemon.

`threading.Thread(target=app.run, daemon=True).start()`

That turns it into a web server. Remember we made it executable, we copied it from the hello world thing which is already executable. You can run plugins manually. This is actually how they get done by lightningd. For debugging it is really cool to run them manually.

Q - Are the processes for plugins running throughout the lifetime of lightningd or are they invoked in a new process each time there’s an event?

A - The processes for plugins are connected to the lifetime of lightningd. lightningd will start them up and will shut them down, kill them off which is really useful for a whole heap of things. It means lightningd is in control and if they obey the directory you can run up multiple lightningd’s and they should all live happily in their own directories and things. They can have their own configuration file. There are two ways to write a plugin. One is it could have its own config file in a format that it wants. The other way is to just tell lightningd what options it wants and then lightningd will do the parsing for it and hand those options through. It depends how sophisticated your plugin is but certainly I prefer the integrated approach at least to start with for plugins which is what I’ve done here.

Q - Is there anything for community plugins to get rated on trustworthiness?

A - There is actually a Lightning plugins [repo](https://github.com/lightningd/plugins) that contains a few plugins that people have written but we haven’t formally gone through as far as doing community vetting for plugins and stuff. That kind of thing will come with more security later on. As things get more sophisticated there will be more vetting of plugins and things. For the moment, you run a plugin, you’ve got like 3 testnet Bitcoin and someone compromises it. That’s ok. We’re still at the reckless phase of Lightning. Obviously caveat emptor. If you’ve got a serious amount of money on your node you should be reading through the plugins if you’re downloading and running. Because you can specify a plugin directory you can just drop them in a plugin directory and in fact there are options you can specify to blacklist particular plugins and not start those up. You can specify multiple directories. I expect there to be a lot of growth in plugins and I expect people from this call to write plugins and go “I can’t do something because there is not a powerful enough API.” So we will add that pretty much on demand.

Let’s run this up manually. In this case we are lightningd invoking our plugin. We need to hand it that string which was the JSON string about `getmanifest`. We need to ask it to `getmanifest`. Here’s one we printed earlier so we’ll just cut and paste that in. There you go. It gave us the manifest. It is telling us everything about itself. Then we need to tell it to init. We also had one of those because we spat out what we got given before. Here we go. It has actually dumped a log, it is actually using the logging stuff to dump a backtrace because obviously I committed a typo somewhere. That was my fault. That thing I cut and pasted in was not the correct value. I fed it a dumboption here which it didn’t say it was interested in so naturally the plugin freaked out. Let’s try that again. Here’s your `getmanifest` call and here is your options call. I will skip the bit that you wouldn’t want and give you that bit. Now Flask printed out some crap and it says it is running on localhost.

`127.0.0.1:5000`

There we go. There’s our plugin running a web server inside it. We can debug it that way and tell that it works. There is a trick on the Python plugin stuff if we take out `autopatch=True`. The example does this. You probably shouldn’t do it anymore. There is an environment variable when lightningd runs, it tells it to autopatch, otherwise it doesn’t. That’s why instead of a standard backtrace we got it in log format. The Python plugin infrastructure actually captures everything your plugin writes out and turns it into a log message. That’s not so useful if you are running it manually. Turning off autopatch makes that better. It seems to kind of work. Let’s run l2.

`l1 stop`

If we run up our plugin now, it should be running.

`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py &`

It seems to be running too which is good.

`cat /tmp/l1/log`

If we look into l1 log… Flask is actually logging to standard output which is getting turned into a log message which comes through here. We can see our GET request. That works pretty nicely for us. Obviously we can control logging levels and stuff like that. We’re doing debugging logging so we’re getting pretty much everything that the plugin prints out at this point. We should probably do something a bit more useful than printing out hello world. What we’re going to do is when they hit that URL we are going to give them an invoice. Instead of that hello world function we are going to do something a bit better. This function here prints hello world. Let’s do something a bit more ambitious. When you create an invoice, people often ask this, there’s this label field that has to be set and has to be unique from the invoice. You have to set that, you are responsible for setting it. The reason that exists is that there is a race condition. If you say to lightningd “create this invoice” and something goes wrong you then have to know whether or not the invoice actually got created before it died when the machine caught on fire or not. By forcing that uniqueness constraint it means that if you retry it will say “No that already exists, you can’t do it.” That is why you have to provide a unique label. It is for robustness. For little things like this we don’t care so we’ve just grabbed 8 bytes of randomness and we’ve thrown that in as the label in hex. Let’s do that. We’ll stop 1 and restart it.

`l1 stop`
`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py &`

Something bad went wrong. Let’s look in our log.

`less /tmp/l1/log`

Here we go. We have got the Python backtrace “name secrets is not defined.” Rusty screwed up and didn’t do the `import secrets` line at the top. That wasn’t the bug I expected to hit. Let’s do that again. This is the bug that I expected to hit.

`l1 stop`
`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py &`

We run it up again, we hit reload, we get an internal server error and we’ll get a more useful bug report from the logs.

`less /tmp/l1/log`

This line here is the important one. “TypeError: invoice() missing 1 required positional argument: ‘description’”. We didn’t provide description to the invoice and you have to do a description. The description gets embedded in the invoice and it describes what you’re offering the person if they pay. The spec says, it is completely unforceable, it is supposed to be descriptive. It should describe what they’re getting. If you’re selling shoes over the internet it should be “Shipping shoes to blah, to this address” or “This many shoes” or whatever it is you are doing. It does have a link limit of 640 characters but that should be enough to provide a comprehensive summary. Let’s fix our plugin. Because the plugin is already running we have to restart every time. Let’s put a description in.

`description= “Get a better description”`

Let’s do the stop and start dance again.

`l1 stop`
`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py &`

This time it was supposed to work. Let me check the logs. I did actually fix this and then I rebooted my machine and lost the fix.

`vi /tmp/plugin.py`

`return invoice[‘bolt11’]`

This returns a struct. We just want the BOLT 11 part of the invoice.

`l1 stop`
`lightningd —lightning-dir=/tmp/l1 —plugin=/tmp/plugin.py &`

There we go. It has created this massive long invoice. You can tell that it is `lnbcrt`, `bcrt` is the regtest network. Let’s decode that. There’s a cool tool called `bolt11-cli decode`.

`devtools/bolt11-cli decode [add invoice]`

Here we can see what currency, timestamp, when it expires, who it pays to which is our node, payment hash, how long it has got, `min_final_cltv_expiry` is how many blocks you need to have remaining on the payment when it occurs, how much it is for. 24 millisatoshi. This is redundant, we also print it out as msat format. And a description that we put in and finally the signature which proves that this node indeed issued the invoice. That is pretty straightforward. Of course we want to test that we can actually pay it. We’ve only got five minutes to go so I am going to very quickly run through this. Let’s do our connect, we may have already been connected.

`l1 connect 02c3f6c70fa61…/tmp/l2/peer`

 Let’s get an address from l2.

`l2 newaddr`

Bech32 address, that’s fine. Now you need to do bitcoin-cli.

`bitcoin-cli -regtest sendtoaddress bcrt1qmgk…. 10`

Send ourselves 10 Bitcoin, there we go. We need to mine that. Bitcoin regtest, you can tell it to mine however many blocks. For regtest we do everything with one confirmation because that is enough.

`bitcoin-cli -regtest generatetoaddress 1 ‘bitcoin-cli -regtest getnewaddress’`

There we go. We get it to generate something. Now if we do list funds. After l2 has caught up, it calls every 30 seconds or so. It will eventually catch up with blocks.

`l2 listfunds`

`l2 getinfo`

There we go, cool. We’ve got a confirmed payment, the value in millisatoshi is a crap load because it is 10 Bitcoin. Now l2 has funds. l2 needs to fund the channel.

`l2 fundchannel 02e20e8b7058…. 0.042btc`

Because this is on regtest it can’t estimate fees so we need to give it a fee rate.

`l2 fundchannel 02e20e8b7058…. 0.042btc 253perkw`

That was a minimum fee. Then we need to generate another block in order to get that mined. So we generate another block in bitcoind.

`bitcoin-cli -regtest generatetoaddress 1 ‘bitcoin-cli -regtest getnewaddress’`

`l2 listpeers`

It has got more information than you’d ever want to know. The `listpeers` has a channel and it is awaiting lockin. It is polling bitcoind every 60 seconds to say “Hey has anything come through?” There we go, funding is locked. Now we should be able to pay that invoice.

`l2 pay lnbcrt240p1pw2j….`

There we go. It is complete.

`l1 listinvoices`

We see our invoice. You can see an earlier one that I made in testing. This invoice is paid, the amount, description, everything we want to know about it. What I wanted to do with this was something more interesting. We are pretty much on our time limit. So instead of showing you I will upload this. I’ll tweet out the URL. I actually extended it to rather than just producing an invoice for 24 millisatoshis, it actually embedded in the payment preimage 24 bytes of text directly paying for 24 bytes of text. The way payments work is the invoice promises them to give them a secret if they pay. That secret is normally a random number. In this case I used 8 bytes of randomness and the other 24 bytes, it is a 32 byte secret, I actually put a text field in there. This is a cute way of rather than having to separately deliver something you can deliver it as part of the invoice flow. Now 32 bytes is enough to hold a secret key for example. It could be that you give them a file and when they pay they will get the decryption key. The decryption key will be the preimage, that secret that you promised them. In this case I used 8 bytes of randomness to make it harder to guess and then 24 bytes of some text. That could be done for some kind of pay to reveal text kind of thing. In fact I wrote a plugin to do that for you, to do the URL query so it added a getword, you just did `blah l2 getword`. The plugin itself then reached out to the URL that you gave it, fetched the invoice, checked it was a sane amount and paid it. I can upload those plugins somewhere if people want. I think we’ve hit time. Did anyone want to ask any specific questions before we wrap up?

## Q&A

Q - What languages are supported to write plugins in? Shell scripts or Python?

A - Do not write them in shell, no. Python is good. The pay plugin is written in C. There’s a lib plugin for C. There is also some Go. niftynei has written some Go infrastructure so you can write it in Go. I didn’t do that because I’m not a Go person, I’m more comfortable with Python. But anything that can understand JSON you can write so any language would work.

Q - C\#?

A - If somebody wants to go and do C\#. The problem is that c-lightning itself runs on UNIX based systems only so we don’t have any Windows support so C\## is not exactly top of our list.

Q - It is possible to do something like HODL invoices in c-lightning using the plugin infrastructure today?

A - Yes. This was always something that we wanted to do. For those not familiar, HODL invoices are what Lightning Labs call them but basically it is adjusting time delivery system. You send out all these invoices and when they come to pay it you go “Do I actually have the thing they are paying for or do I reject at this point?” For some models that is much better than reserving when you send out the invoice. Even though the invoices have an expiry you may well want to send out a whole heap of invoices expecting only a small number of them to come back. You don’t want to hold stock based on the invoices but actual payment. It can be bad UX because of course they get an invoice, they go to pay it and you go “Sorry no that didn’t work.” We have a thing in plugins which I didn’t show here called hooks. A hook is like a notification except the whole thing is waiting on the plugin getting back to you to say “Yes it’s good” or “No it’s not good.” Subscriptions are for notifications where you get told stuff is happening but hooks are actually blocking. A hook on payment receipt is really important for this. You’d write a plugin that registers with that hook and when it actually comes in it goes “Should I actually honor this payment now?” Yes it matches the invoice but maybe there is some other reason that I don’t want to. That would allow you to HODL invoices. Maybe you’d just hold off for a while until something else is lined up. For a complex system that is actually quite important. You may have a whole CMS system around it.

Q - .NET Core run on Linux?

A - Yes. .NET Core can definitely run on Linux. You could do C\## on Linux. It is just a question of it wasn’t the most popular language for people to use on Linux. That is why there’s no C\## plugin. It would be pretty easy to write. If you can speak JSON you handle those bits, you handle the registration for them and it is pretty easy. It is pretty easy to write in any language natively but it is nice if you’ve got a library that does all that infrastructure for you and registers your options and does all that stuff rather than having to do it manually.

Q - Thank you so much Rusty. This was fantastic. If people want to reach out to you and ask you more questions where they can find you?

A - \@rusty_twit on Twitter is usually the best way of doing it. We also hang out on both the \#lightning-dev and \#c-lightning IRC channels on Freenode. \#lightning-dev is generally for general Lightning development discussion and protocol discussion and \#c-lightning is specifically for c-lightning questions. Of course my email is pretty easy to Google as well. rusty at blockstream.com or rusty at rustcorp.com.au.


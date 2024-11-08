---
title: Bitcoin CLI and Regtest
speakers:
  - Richard Bondi
date: 2018-08-17
transcript_by: Michael Folkson
tags:
  - bitcoin-core
  - developer-tools
media: https://www.youtube.com/watch?v=sbupEpL6-J4
---
Clone this repo to follow along: <https://github.com/austin-bitcoin-developers/regtest-dev-environment>

<https://twitter.com/kanzure/status/1161266116293009408>

## Intro

So the goal here as Justin said is to get the regtest environment set up. The advantages he mentioned, there is also the advantage that you can mine your own coins at will so you don’t have to mess around with testnet faucets. You can generate blocks as well so you don’t have to wait for six confirmations or whatever or even the ten minutes. You get confirmations right away and that’s one of the things we will be going through. Bitcoin Core is what we are going to be using. Does anybody not have it installed yet? We’ll go through and I’ll show everything with my setup I got here. You can follow along. Also there is this repository here, if you can download this repository that would be helpful. Once you’ve got Bitcoin Core set up you run some scripts that will set up three nodes in regtest mode. So you’re going to be running three nodes on your laptop which starts with zero blocks. You’ve got a clean blockchain and if it starts… you can delete it. You don’t really have to worry about resources. It is one of the advantages of regtest. I guess we can start cloning the repo. Shall I just dive in and start demonstrating?

## Demo

In the repository we’ve got some scripts. First off we want to do the run script which will get us up and running and get all three nodes if we have our configurations set. I’m going to crank it up here. If you guys are ready you can try to crank it up. If you have problems we can stop and try to figure out what they are.

`./run.sh`

We’ll show the scripts as we go through, that’s a good idea.

Q - Is it just like a bash script?

A - Yeah. If you are on Windows you can just change it too .bat. It is just command line. This is assuming you have bitcoind in your PATH. The Bitcoin version number, however you set it up, if you do the default install it is going to be bitcoin, the version number, .bin. If you have that in your PATH you get that up and running.

Q - For those who don’t know what is bitcoind?

A - bitcoind is the Bitcoin daemon which is your node implementation. It is kind of a black box that communicates to the other nodes and sends transactions, receives transactions, it is your full node.

Q - You can think of it basically as the client you would see in Bitcoin Core but without a head? It is just running on the server.

A - Yeah

Q - So what do these commands do?

A - The -regtest is obviously regtest which will mean you don’t connect to mainnet or testnet. You’ve got your own local environment. The -daemon at the end means it is going to run in the background. You see Bitcoin server starting and I still have my command prompt. If you try to use this without the daemon you’d be locked there and your console would be locked up.

Q - What about the datadir?

A - We have Alice and then we have a data directory of Bob. The top one doesn’t have one because it goes to the default. Whenever you install it it should be home/user/.bitcoin/bitcoin.conf That’s why there’s not one there. Alice, we’ll look at her. Really secure passwords, don’t try to steal any money from Alice here. We set up some unique ports for it and we’re adding nodes to it so she can talk to Bob and she can talk to the default regtest node.

Q - So this is just a bitcoind configuration file?

A - It is bitcoin.conf for bitcoind. Or if you run Bitcoin-Qt it will look at the same one.

Q - So how are Alice and Bob are different?

A - They have different ports. These are just random numbers, they just had to be unique. So you can see Bob is 18446, the default port for regtest is 18444, this is 18445. And then the same thing for the RPC ports. There’s a default of 18443, there’s this random thing that Justin made up and then Bob has another random thing that Justin made up.

Q - Ok so when it says `port=` that it is what Alice is running and then the other two are how to connect to these other two peers? It is a way of bootstrapping our little mini network of 3?

A - Right.

So if I go back to my command prompt. I’m up and running.

Q - You only actually really need to add one of them and you will discover the other peers, `addnode` is a luxury?

A - There is no peer discovery in regtest. That is true if you’re on testnet but not on regtest. No peer discovery, that’s one of the limitations. You trade being able to mine coins at will for not having peer discovery. You do have pretty much most of the other features, there may be a few that are missing.

Q - You can also right now confirm that it is working by looking in the Alice and Bob directories? You’ll have chainstate…

A - Sure. I have a regtest directory that started up. I deleted these before I started. But what we really want to do is verify through the CLI or through some of these other tools that we want to look at.

We’ve got aliases.sh, is a convenient script. We don’t have to type port 99 whatever for Alice and port 99 whatever for Bob. We can just create these aliases. Right now I’ve got the default. The -regtest gets us on the network and I want to put in a command.

`bitcoin-cli -regtest getpeerinfo`

You’ve got id 2 and their address.

Q - What command did you do?

A - getpeerinfo. This is a way to see exactly who we’re talking to and some additional information. We’re running the same client so they’ll all have the same version and a lot of the same information. The main thing is we’ve got the address, here’s the port we’re connected on.

Q - That’s the peer?

A - Yeah these are the peers. We actually have our own little network here. Other than verifying that there is something in those folders we can verify that yeah we are communicating.

That was from your default point of view. We also want to have a point of view from Alice and Bob. That’s where the aliases come in. Let me pull that up. The Bitcoin CLI, there’s your port, there’s your data directory. The port in this is your RPC port. Now you can type in `alice-cli` instead of typing `bitcoin-cli -port=9334 -datadir=alice` each time, we have a shortcut.

`source aliases.sh`

Now I can do the same thing.

`alice-cli getpeerinfo`

Now I have Alice’s point of view of the network. Same thing for Bob.

`bob-cli getpeerinfo`

It is really hard to follow in the CLI but we have a solution to that, don’t worry. So let’s see how we’re doing cash wise.

`bitcoin-cli -regtest getbalance`

Ok no money, sad state of affairs. But we don’t have to mess with testnet faucets, we can generate our own. There is a command called generate so we use that and then the number of blocks you want to generate.

`bitcoin-cli -regtest generate 1`

So we generate a block. There’s the hash of the block we generated. Kind of unexciting, nothing but a coinbase in there but that’s the way things work.

Q - If only you could find a way to sneak that into the real chain.

A - No I’ve got something. Hang tight, I’ve got you covered. You don’t need a real chain, that’s the whole point of this. If you could get up and running this fast but the world don’t work that way.

So I generated a block, I want to get my balance again.

`bitcoin-cli -regtest getbalance`

Oh no I’m still broke. What happened? You need 100 blocks before you can claim your mined coins. We’re simulating mining, we’re still simulating the same way. I want to generate another 100.

`bitcoin-cli -regtest generate 100`

Now I’ve got whole bunch of very exciting blocks with just a coinbase transaction but now I have a balance of 50. The very first one matured more than 100 blocks so we’re set. So ready to start spreading out the wealth here. So I’m getting an address for Alice so I can send Alice some coins.

`alice-cli getnewaddress`

Q - Regtest addresses start with a 2?

A - They start with m or n if it is the old legacy address. They start with 2 if it is a SegWit address. If it is a bech32 it starts with btr I think fir regtest mode.

So we’ve got an address for Alice, we want to spend Alice some coins.

Q - What’s her balance?

A - Sure why not. We know it is zero but it is good to confirm.

`alice-cli getbalance`

I need an address and an amount, let’s give her 10.

`bitcoin-cli -regtest sendtoaddress [insert address] 10`

So there’s a transaction hash which returns from that command. Let’s check Alice’s balance.

`alice-cli getbalance`

It is zero. Why? There has been no mining. We can tell that it happened though.

`alice-cli listunspent 0`

The first parameter of that is the minimum number of confirmations. So if we say zero we can verify that Alice did receive that transaction, it is just not available. See the zero confirmations? We see the same transaction ID, we see the same 10 Bitcoins that we sent to her.

Q - What is it querying to figure out what her unspent is with zero confirmations?

A - listunspent was the command. If you do listunspent without any parameters it is not going to include the zero confirmations. So you have several parameters. You’ve got min confirmations, max confirmations, you can filter out by addresses. Where it says safe at the bottom you can include unsafe which it defaults to true I believe anyway. You can pass another object to it to get minimum amount, I want to see all unspent transactions over 2 Bitcoin or I want to see all unspent transactions under 5 Bitcoin or whatever.

Q - What’s the data store where that is stored in? For unspent? Unspent would not be in the blockchain?

A - Everything is the blockchain. From Alice’s perspective the Bitcoin daemon has a wallet built into it and the listunspent is looking at Alice’s wallet.

Q - So she is looking at her local mempool?

A - It would be her local mempool but it would be any addresses in her wallet that have outputs in that mempool. Once it is mined it is not in the mempool, it is part of the blockchain.

So let’s generate 1.

`bitcoin-cli -regtest generate 1`

Now Alice can get her balance.

`alice-cli getbalance`

There’s her 10 coins.

Q - The default should have 100?

A - It had 50 and sent 10. It should have 40 minus a fee so 39.9 something.

Q - But we got a new block mature?

A - That’s true, plus the 50. You’re right.

`bitcoin-cli -regtest getbalance`

The original 50, the recently mined 50 minus the 10 sent to Alice minus a transaction fee.

Q - The fee is autogenerated? Who is coming up with the transaction fee here in this regtest?

A - Everybody has their own wallet. Regtest has a wallet, Alice has a wallet, Bob has a wallet.

Q - It is a default fee setting?

A - Their wallet comes up with the fee, each individual wallet. We’re too early in the game to really be optimizing fees. Once you get a thousand blocks in or whatever, I’m not sure what the exact number is.

Q - Who received the fee?

A - The miner.

Q - Is the miner the default in this case or do you have a fourth party?

A - You’re right. I have to wait 100 blocks to get that back. If we mine 100 blocks we should have an even number.

If we generate 100 blocks.

`bitcoin-cli -regtest generate 100`

Even number, so they got the fee. That’s what we’re looking for. That’s the beauty of regtest, you don’t have to worry about it. Just make more, we’re worse than the Fed here. That’s pretty basic unexciting stuff.

Q - Can you send more coins to Alice, send her like 10 more and run that query with a minimum zero confirmations? Would it add the mempool and the amount on the blockchain? The total would include the 10 coins that haven’t been mined?

A - Yes. Let’s do it.

I need another address from Alice.

`alice-cli getnewaddress`

We’re going to send another 10.

`bitcoin-cli -regtest sendtoaddress  [insert address] 10`

So I’ve got a transaction.

`alice-cli listunspent`

If I do that I’m not going to get the new 10. I’ve only got one transaction with 101 confirmations now. But if I do the minimum with a zero…

`alice-cli listunspent 0`

I’ve got the two transactions.

`nodes-debug`

It came up on this screen, it is so small I can’t see it. What I did was develop a tool that allows you to connect to multiple nodes and it has some convenient features for working with the commands so you don’t have to be clumsy working with the CLI. We can do some of the same things.

Q - We should all be getting the exact same results as you down to the signatures? My transaction IDs don’t match yours. On the command line output, it is deterministic, we should be getting the same results? I think Bitcoin Core uses deterministic k values now so the signatures should be duplicated.

A - We’ve got three different configurations. I wouldn’t expect the same results but you may be right. If you installed on mainnet you’re not going to generate from the same seed.

Q - What does regtest do for mining? Is there any difficulty?

A - No it is instant. If I generate 100 you saw how quickly that came up. It is just simulated, it is not a real thing.

Q - Can you get the proof, the string that is hashed? Even zero difficulty actually has some difficulty. Satoshi made a really weird choice. But it is trivial.

You saw how I was struggling with the commands. I wrote this to get some auto completion and you get some parameter help.

`getbestblockhash`

Q - Can you pull the GitHub repo real quick?

A - It is on the README. https://github.com/rsbondi/nodes-debug.git

I’m going to get that block.

`getblock [insert block hash]`

Q - On the left you execute commands and on the right you get the outputs?

We want to look at the block, we want to look at the difficulty, chainwork. It is really difficult, look at all those zeros. It is fake, it doesn’t mean anything.

Q - Right above that line it shows the difficulty, e^(-10)?

A - That’s really easy then. Why does it have all the zeros? That’s the amount of work, that’s not the hash. It should be pretty easy, they generate instantly.

We’ll do the same thing here. We’ll come back to Alice and list the unspent. I don’t have to type in order, I can just use the shortcut `lisu` it jumps up the `listunspent`. It makes it a little bit easier. What are my parameters? Look at that, the first one is min confirmations, I put a zero there. The next one is max confirmations, 9999. That last one, `query_options`, it doesn’t tell us much about it. But you don’t have to go into the help you just hover over it. Now you get the full help. This is pointed all out in the RPC server. Whatever version you’re on this is going to work. It is optional, use it if you like. I made it because it helped me a tonne, just to not have to go back and forth looking stuff up. Let’s send Bob some money. He’s been left out here. Bob needs to get an address first.

`getnewaddress`

`sendtoaddress “[insert address]” 5`

It is a little different here from the CLI, the strings you don’t need the quotes. Here you do because it is Javascript and I didn’t want to figure out how to parse it. How much do we want to send Bob, we’ll send 5, we’ll keep most of the wealth to ourselves. We’ve got that transaction, we can look at that if we want to. Somebody tell me how do I see that that transaction came through to Bob?

`listunspent 0`

There we go, zero confirmations.

Q - How did you add Alice and Bob? I got an error message when I tried adding them. Was there an easy way to add those?

A - I already had them set up. You have the Add Node button here. You need the config file because that is your user credentials. It pulls that from there.

Q - Could you try deleting one and adding one in real time?

A - Sure why not. Let’s look at Bob’s configuration first. Edit Node and then copy this. I’m going to delete Bob and add him back. Put in the config path. I know we don’t need the host, I don’t think we need the port either. It should get that from the config. There he is, he’s up and talking.

Q - You didn’t have to put in the port?

A - No because that’s in the config. If you have the config and you have that configured in there and you’re not just pulling it up from the command line, bitcoind, it’s already there. You always need the config because that’s where your credentials are.

Ok so what we’ve done is pretty boring, send to address, the address and the amount. Let’s do it by hand. I’ll use the same address. Not good practice but alright. Create raw transaction, what parameters do I need here? I need some unspent outputs. Why doesn’t Alice have any money? We need to mine the block. She sent some money and it sends the whole Bitcoin not part of it. Let’s generate one. Notice I called this Regpool, that’s my mining node.

Regpool - `generate 1`

Alice - `listunspent`

Alice has money again. Let’s take that first one. I need an array of an object and I need a txid and a vout. I’ll grab those right from here.

Q - So you’re constructing a transaction from transaction inputs?

A - From unspent outputs. I’m telling it for my input I want to use that transaction, index number 0, it should be that top one with the 10 coins in.

Another thing I can do multiple lines, I just can’t have spaces between the multiple lines. That’s my first parameter. Now I need someone to send it to. Let’s go get Bob, an object with an address and an amount.

Bob - `getnewaddress`

We’ll send 5 again. There’s our transaction we created.

Regpool - `createrawtransaction [{“txid”: “[add transaction ID]”, “vout”: 0}] {“[add address]”: 5}`

So what do you think is going to happen if I try to send that?

Q - You generated a new address for Bob and plugged it in as the output right?

A - Yeah

No it is not going to work because we have not signed the transaction. This will give you more flexibility if you’re creating transactions and you want to create them by hand. This is the way to do it. You have more flexibility than to just send to address, you can include your own scripts and all kind of things. I don’t think we’re going to get into that today. I want to sign the transaction.

`signrawtransaction “[add result hex string]”`

So now I have a signed transaction. Let’s send that baby. The next thing is `sendrawtransaction` and then all you really need is a string.

`sendrawtransaction “[add result hex string]”`

Q - The `createrawtransaction` has an input and then the second thing is an output?

A - Right. The output is the address I’m sending to and the amount, it is an object. I can have multiple addresses. The address is the key and the amount is the value. It is a JSON object, a key-value, address-amount.

Q - The unspent transaction output is 10?

A - Right. We can spend it, we’re going to throw 5 coins away as a fee. Or are we? Absurdly high fee, it won’t let me do that. Thank you Bitcoin RPC, you just saved me 5 Bitcoin.

Q - Can you JSON out to show a full transaction? Can you decode rawtx?

A - Sure. This is the one we tried to send.

`decoderawtransaction  “[add result hex string]”`

There’s what it looks like decoded. The signature is in the witness data.

So what Alice needs to do is get a change address, `getrawchangeaddress` with no parameters.

`getrawchangeaddress`

This is why almost all transactions have two outputs. It is because the likelihood that you’re going to be spending exactly whatever output is very low so 224 bytes is the normal.

I added the rest of the 10 minus a miner fee. Now I can recreate a transaction.

Alice - `createrawtransaction [{“txid”: “[add transaction ID]”, “vout”: 0}] {“[add address_1]”: 5, “[add address_2]”: 4.99999 }`

Q - So the second address is Alice?

A - That’s Alice’s change. 5 going to Bob, 4.99999 going back to Alice, at her new change address that we just created.

I’m not sure what the difference is between change address versus address. I know in HD it is m/0/0/0/1 for the change address and m/0/0/0/0 for the main address.

Q - Does `getrawchangeaddress` have a different HD?

A - I don’t know Bitcoin Core’s implementation well but if you’re using the HD feature of Bitcoin Core it does not use the BIP32 default. It uses hardened derivation for every address, it is not compatible with your Trezor or whatever.

If you had a HD wallet like I said that derivation path would end in 0 and 1 for the change address.

I’m creating the transaction, I want to sign it.

`signrawtransaction “[add result hex string]”`

There’s my signed transaction, I want to send that as a raw transaction.

`sendrawtransaction “[add result hex string]”`

There’s my transaction ID. I guess I’ll keep going. I also have a simulate script (simulate.js) in here. What this does is randomly creates transactions of random amounts from your main regtest node. I’ve set it to five minutes, I think I’ll bump it down to show it’ll mine a block in five minutes.

`node simulate.js`

I just created a transaction, it has created some random transactions. If you also want to run this script you’ll be generating transactions. We’ll go more than five minutes, that’s fine. Randomly generating, we’re going to mine every five minutes. So you’re going to get more of a real world simulation where there’s a lot more transactions and you go and analyze a lot better. I’ll show you. Here’s a script I wrote for connecting directly to the network. I’m not going through the RPC, I’m TCP/IPing into one of the nodes, making a connection, doing the handshake, version, verack, inventory message and all that. You’ll be able to see that here, this is just for demonstration purposes.

`node peers.js`

I connected, I did my handshake, now I’m waiting. I have that other one running in the background. I should eventually see transactions coming in. I sent a `getdata` command, I got an inventory message saying there’s a transaction. I said I don’t have that one send it to me. I sent the `getdata` command and then I got a response. If you’re developing and connecting it is handy for that. If I go back to Regpool now I’ve got an additional peer. I can troubleshoot my code now that my version is working. If you’re writing code to connect to a peer that’s a handy way.

Q - Do you make the handshake in raw hex?

A - It is raw. This is all Javascript. I just went through the spec and it said here’s the handshake. All the messages have the magic bytes, then it has the message header which is always in the same format. Then it has a payload. I just went through and read all that and experimented and saw what came back.

Q - We did that in Jimmy Song’s class.

A - I’ve been going through his book and doing everything in Javascript so that I can do it rather than just copying the Python code and tweaking it. Javascript wouldn’t be my first choice but it is what I know and it was the fastest way to learn.

That’s part of the development environment. I wanted you to get set up, it is optional. You can actually see transactions coming in.

Q - What file is that in the repository?

A - It is a different repo, the one that’s actually connecting directly. The idea is to simulate. If you connected directly and there was no simulation you’d just be sitting at a blank screen. You’d get a ping, you’d get a pong. That’s a bunch of random stuff I go through for my own education. I wanted to share it. If things work for me and you prefer Javascript over Python. If you’re not a Python guy and you prefer Javascript there’s another alternative. You can go through and read that. You can try running these scripts just to play with them and tweak them a little bit. Or just to watch the network. You can put breakpoints in your code and see something didn’t happen. The whole idea is to have a troubleshooting tool.

Let’s go back to this guy. I’m pretty sure I mined a block by now. Let’s find out.

Regpool - `getblock [add getbestblockhash result]`

It has been more than five minutes. Now I have a block that looks more like a block, it is not just a coinbase transaction. So now if I want to start parsing blocks I have something to work with. I have another test script, just me playing around here. It is doing a whole bunch of things but one of the things is calculating a Merkle root, I’ll leave that at the end. I have an example from Andreas’ book here. I can go back to the block I just created. Here is what the Merkle root should be. I’ll put that in there. I’m just `console.log`ing out. I’m calculating a root and print out what it is and it should match. I’ll grab all these guys and paste them in there. I’ll take Andreas’ sample out, put it in that. Now if I go and run that.

`node main.js`

It is doing a bunch of other things. I’ve got some stuff I should have commented out. I’m experimenting with compact blocks, there’s something after the Merkle root. It looks like it matches. That’s another advantage of the simulation. You can have blocks with data in them. It would take you a while to type in Alice sending to Bob and Bob sending to Alice and do that all day long and then try to generate a block. It is just another tool to help help you. That was the whole point. To have a useful local environment where you’re not on the blockchain, you don’t have to worry about syncing every time, every time you close your laptop and come back up.

## Q&A

Q - How does the random simulator work?

A - It is just talking to the RPC server and it is sending commands, that simple `sendtoaddress`. It is picking a random amount and creating that.

Q - Are they all valid transactions?

A - Yeah. Let me pull up the code (simulate.js). I’m going to generate a random amount between 0 and 2 and we’ll get a new address. I’m in my own local environment. I’m sending all money back to myself. From Bob’s and Alice’s perspective they don’t know that. It looks like somebody creating transactions and sending them on the network. I get a new address, I send to address and then I give it that random amount. Then I send. I have a timer here so that every five minutes it is going to mine.

Q - You’ve got transactions that you’re spitting out and you’ve got blocks that you’re spitting out?

A - Right. If you were in there doing Bob and Alice while that was running those would be there too. But that way you have a mining thing. It is closer to real world.

Q - Can regtest open up to the network? Can you make a port available on the internet and then just connect to a bunch…

A - You have the magic bytes, that determines your network. That’s the very first thing of every message. So every message starts with the magic bytes. There’s three different ones.

Q - If Michael and I wanted to be on the same regtest network? It is probably a networking challenge?

A - You could just open up a port? I don’t know. That would be a good idea but I don’t know. You wouldn’t have to download testnet.

You could test the UI and stuff. You could have cooperative development and have the same… You don’t really need to do that. You can run them separately, you don’t have to see exactly the same numbers.


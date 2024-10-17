---
title: Peer-to-peer Encryption
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=jvFdPwssv_E
tags:
  - bitcoin-core
  - v2-p2p-transport
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2023-04-24
episode: 77
summary: In this episode of Bitcoin, Explained, Aaron and Sjors discuss BIP 324, the proposal by Dhruv, Pieter Wuille and Tim Ruffing to add peer-to-peer (P2P) encryption to the Bitcoin protocol. They explain why this is needed, how it would work, and which problems it would, and wouldn’t solve.
---
Aaron van Wirdum: 

Sjros, you were just telling me that one of the reasons you came up with the topic for this episode, which is BIP324, a peer-to-peer encryption, is because you had a call with other Bitcoin developers about this.
Since when do Bitcoin Core developers call?
I know Bitcoin developers as IRC wizards, and they're on a call now?
That sounds like Ethereum, Bitcoin Cash type of communication.
What's going on?

Sjors Provoost:

The idea would be to put these calls on some sort of podcast or feed.
The OpTech folks are organizing it.
That's basically just a short lecture by the people who are working on a project.

Aaron van Wirdum:

Is it educational?

Sjors Provoost:

Yes, but then of course the idea is to get some feedback from people and to encourage them to start reviewing it.

Aaron van Wirdum:

Is it like online BitDevs?

Sjors Provoost:

Yes, maybe you could see it as an online socratic small seminar with fewer people talking.

Aaron van Wirdum:

Is this new?

Sjors Provoost:

I think it's very new.
At least, I was only invited very recently, who knows?
Maybe it's a third level Illuminati.

Aaron van Wirdum:

Yes, it's like this invite-only thing where you enter the inner ring.

Sjors Provoost:

The Bilderberg.
Exactly.

## Peer-to-peer encryption

Aaron van Wirdum:

Business today is BIP324, peer-to-peer encryption.
A little bit of background on this.
This used to be called BIP151.
It used to be Jonas Schelli’s project.
Jonas Schelli retired as a Bitcoin Core developer and the project is now led by Dhruv, Pieter Wuille a.k.a. Sipa and Tim Ruffing.
They picked up the project from Jonas when he left and they rebranded it or renamed it or they got a new BIP.
Now it's BIP324.
Do you know why?

Sjors Provoost:

I think it's because enough of the things about the proposal have changed that it was worth just giving it a whole new BIP number.

Aaron van Wirdum:

Do you know why 324?

Sjors Provoost:

No.

Aaron van Wirdum:

That will require you to get into Luke Dashjr's mind.
I think there's a logic to the numbers somewhere in his brain, but I don't think anyone else in the world knows it.

Sjors Provoost:

We did an episode about the coin improvement process basically, but we did not go into numerology for the same reason we didn't go into numerology for ordinals.

Aaron van Wirdum:

Okay, so what we're talking about is encrypting communication between Bitcoin nodes.
Right now, nodes send three things between each other, which are blocks, transactions, and each other's IP addresses, IP addresses of other nodes.
They do all of this unencrypted.
Now, the idea is to encrypt this.
That's the very short, sort of bird's-eye thing.

Sjors Provoost:

Exactly.
Remember the days when HTTPS was considered a feature?
When websites would say, 'Oh my God, we have an HTTPS certificate.'
Before that time, you could just eavesdrop on anything you were doing at a webshop.
Bitcoin Core nodes still use that old method.
There's reasons it's not using HTTPS, but it is nice to have some sort of encryption and that's what we'll get into.

Aaron van Wirdum:

What's the problem Bitcoin developers are trying to solve? 

Sjors Provoost:

They are spying on us…
Basically, the problem is that Bitcoin nodes are talking to each other in a way that anybody with access to the network can eavesdrop on it.
Especially, people with physical access to the network, so they could have a machine on the wire.
This could be somebody monitoring your home, this could be your internet provider monitoring all their customers, this could be a spy agency monitoring all the internet companies, even without the internet companies knowing that this is happening.
And they can basically see exactly which node is sending which transaction to which other node, if they wanted to.
I don't know if they're doing that.
Maybe they really don't care.
I haven't seen any evidence that they're doing it.
If you look at things like ChainAnalysis, they're already doing a lot of work just the hard way.
As far as I know, ChainAnalysis is not getting data from the spy agencies.

Aaron van Wirdum:

What if they do?
All the data is public anyways.
It's all going on the blockchain anyways.

Sjors Provoost:

What's on the blockchain is public, but the question which IP address created the transaction is definitely not public or not supposed to be public, but it is if you look at the transaction.
If I make a transaction on my node and I send it to the nodes around me, then a spy agency that can see all the internet traffic would be able to see basically this transaction exactly where it started, and that of course would be very interesting information for them.
Right now, the only companies that do this are chain analytics companies, and they have to do it the hard way.
They have to make lots of connections to lots of different nodes and monitor it that way.
None of what we're going to discuss is going to make that impossible.
The idea of just looking at the whole network and seeing what's going on, that's the thing we want to prevent.

Aaron van Wirdum:

I'm gonna try an example.
If I send a Bitcoin transaction, I spend my own bitcoin, that transaction would have to originate from my node.
In that case, my internet service provider would see that, 'Oh, look! That transaction came from Aaron's node, these must be Aaron's bitcoin.'
And that's the type of spying we're talking about.
If that connection from me to the network would be encrypted, they wouldn't see that that specific transaction originated from me.
It's the same for miners who create blocks.
We’d like miners to be anonymous on the network, and if an ISP knows where blocks originate, they know where the miner is, right? 

Sjors Provoost:

Yes.
In a perfect world, they would not be able to do that.
This proposal will not get us to the perfect world, but it will get us to a slightly better world.
There's the privacy issue.
The other issue is censorship potentially because this internet provider that saw that transaction coming from you might also think, 'We don't like this guy.
We're gonna block just his transactions, not everything else.' And they can do that too.
They can get in the middle of the communication between our nodes and they can select, 'If you listen to it, let everything through, except one or two things that they don't like to let through.' 

Aaron van Wirdum:

These are sort of two sides of the same coin.
If there's no privacy, that would allow specific censorship.
If all Bitcoin data looks the same, they can't single out transactions, and therefore, they also can't block certain transactions.

Sjors Provoost:

Yes, and then the third category would be things like eclipse attacks.
We had an episode about eclipse attacks very early on, which basically boils down to showing one thing to one node and showing other things to other nodes, and the companies that are operating the internet have some power to do that.

Aaron van Wirdum:

We've now covered the problem we're trying to solve with peer-to-peer encryption.
What is the solution?
The solution is to encrypt data.
Is it that simple?

Sjors Provoost:

Yes, pretty much.
That's at least the beginning of the cat and mouse game.
The beginning of cat and mouse game is to say we're going to encrypt all the data so that when somebody's looking at our internet connection, all they see is noise.
They cannot read the individual transactions.
They don't even know at first glance what is a transaction and what is not.

Aaron van Wirdum:

More concretely, how does it work?

Sjors Provoost:

The idea is that when you connect to another peer, you do a handshake with that peer, and that handshake basically creates an encrypted connection between the two of you.

## Protocol handshake

Aaron van Wirdum:

What is a handshake? 

Sjors Provoost:

The handshake is basically saying, 'Here's my key,' and then you say, 'Here's my key.'
There's a little bit more to it, of course, but the general idea is they called a Diffie-Hellman key exchange, if you Google that, you'll find it.
We've talked about it in other podcasts too.
It basically means, I get your public key, you get my public key, and we can combine those keys into a shared key - a key that both of us know.

Aaron van Wirdum:

Do you want to try to explain how this works? 

Sjors Provoost:

No.

Aaron van Wirdum:

I can give it a try.
Basically, you got a mathematical one-way function.
You take a number, you put it through a one-way function, you get a different number.

Sjors Provoost:

It's not really a one-way function because theoretically you can go both ways.
In practice, you can't.

Aaron van Wirdum:

No, you don't even know where I'm going with my explanation.

Sjors Provoost:

Well, we talked about hash functions in another episode.
Those are actually one-way functions.
There is no way back.

Aaron van Wirdum:

But that's how you derive a public key from a private key, right? 

Sjors Provoost:

No.

Aaron van Wirdum:

Well, it’s definitely a one-way function from a private key to a public key.

Sjors Provoost:

No, it's a two-way function.
The thing is just that the way back is so difficult that in practice, you can never go back.
That's what we hope in theory.
But a hash function is really one-way.

Aaron van Wirdum:

Why are you saying that's not a one-way function?

Sjors Provoost:

Because you can go both ways in theory.
Mathematically speaking, it just goes both ways.

Aaron van Wirdum:

Is this what we discussed and I forgot about it?
Did you explain what the difference is?

Sjors Provoost:

I think, I did.
A hash function is really one-way, and a public key from a private key to a public key is easier than from a public key to a private key.
It goes both ways, but the toll on the way back is very high.

Aaron van Wirdum:

Okay, you excuse me if I call it the one-way function for now.

Sjors Provoost:

A one-way-ish function.

Aaron van Wirdum:

I still think it's a one-way function, but alright.
So, you have a number, you put it through a one-way-ish function, you get a different number.
If you do it twice, you get a different number again.
So what is a public key? It's basically a number put through one one-way function.
Now, I take your public key - that's your secret number put through one one-way function - and then I'll multiply it with my own secret number.
What we get is a mix of two secret numbers and one one-way function.
And you can do the same thing.
You could take your private key and then you have your secret number and my public key, so that's my private number.
Now, you've got to mix again of two private numbers plus one-way function.
The reason no one else can do it is because then the only way they could do it is take two public keys, so now they get a mix of two private numbers plus two one-way functions, so you get a different number.
That's basically it, right? 

Sjors Provoost:

Yes, I'm not sure if that made a lot of sense.

Aaron van Wirdum:

I'm not sure if people can follow the audio, but I think it's correct.
I think this is the simplest way of explaining it.

Sjors Provoost:

It basically boils down to I know my private key, you know your private key, we don't want to share our own private keys, so I give you my public key, you give me your public key, and we do the math, and basically now we have a shared key.

Aaron van Wirdum:

That's Diffie-Hellman, and that's what Bitcoin nodes would use.
Does it mean that every Bitcoin node has a public key? 

Sjors Provoost:

No, that's a big distinction.
We are not doing identity here, because that would actually be kind of controversial.
Every node should look like every other node.

Aaron van Wirdum:

Is this a big or maybe the biggest difference compared to BIP151?

Sjors Provoost:

No, it also made a distinction between these two things, but maybe the distinction was done in a slightly different way, but the idea is always that these are separate things.

Aaron van Wirdum:

So what then happens instead is, every time a node tries to connect to another node, they go for handshake, which means at that point they generate a new key pair.

Sjors Provoost:

Yes, they do it for every connection.
If I connect to you, and then somebody else connects to you, they're all going to see a different key.
You're not going to present yourself as the same identity.

Aaron van Wirdum:

Yes, I'm going to generate keys for every new connection, and then establish a new Diffie-Hellman secure connection based on every new key and with every new node.

Sjors Provoost:

Exactly.

## Man in the middle attack

Aaron van Wirdum:

Okay, that's how it works.
Does that solve the problem that we discussed in the first part of the episode?

Sjors Provoost:

It's always a cat and mouse game.
But right now, what happens if somebody is just passively listening to our traffic, all they see in this example would be somebody sending a public key and somebody else sending a public key, and after that you see noise because I have no idea what the rest of the traffic is because it's encrypted.
You could say that that's a good start because now at least they won't be able to tell which transactions are which, but they could still get in the middle.
Because when I connect to you and you connect to me, how do I actually know that it was you? I don't because we don't have identity.
So, you don't have a public public key, you don't have something on your website that says it's me, I just have your IP address, and besides, I'm connecting to random nodes on the internet anyway as a Bitcoin node.
The man in the middle attack is still possible, but this is called an active attack.
If the government or whatever wants to see our traffic, they would have to do it in such a way that I think I'm connecting to you, but I'm really connecting to this government server, and then the government server connects to you and pretends it's coming from me.
That way, I'm doing a Diffie-Hellman exchange with the government, and you're doing a Diffie-Hellman exchange with the government.
This proposal contains a countermeasure to that risk, which is that we could get on a phone call, and we could look up 'session ID'.
The session ID is just basically saying, 'Well, okay, we have a connection session, and if that number is the same, we know we are directly connected to each other.
If the number is different, that means somebody is in between us.'

Aaron van Wirdum:

I got the first part.
I don't think I need to repeat that.
That was pretty straightforward.
I think people will probably know what a man in the middle attack is even the name reveals it.

Sjors Provoost:

Yes, in this case, I was making a government in the middle attack.

Aaron van Wirdum:

Then you said one of the ways to solve it is...

Sjors Provoost:

You're not preventing it.
But first of all, it's more expensive because the government, or whoever is eavesdropping, can no longer just listen.
They don't just put their ears on the cable, they have to actually install a computer that actually does all the handshaking.
It takes some CPU power and much more work.
And if they do it, because of this session ID, if we communicate outside of the protocol, we can compare nodes, and then we can see that there's somebody in between.
Very similar to how it works with Signal.
If you add somebody as a contact on Signal, you show each other a QR code, and that is really a way to see that, okay, my Signal app is actually connected directly to your Signal app, and there's nobody in between.
You have to do in-person or on the phone.

Aaron van Wirdum:

A serial number kind of thing.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

This sounds like a theoretical thing because no one's actually going to get on the phone to see if we have the same Bitcoin node serial number.

Sjors Provoost:

The good thing here is that if the government wants to surveil everyone, then there's going to be some people that will do this, and then they can actually say, hey, this is happening, and then they can make a bunch of noise.
This is relying on an incentive for governments to not get caught doing this.
It's A) more work, and B) they would not be able to do it undetected.
Right now, they can do it undetected.

Aaron van Wirdum:

It sounds like if a government really wants to spy on you, your node, your node traffic or an ISP, they would still be able to do that, however, it would require more resources.
Right now, they don't need to do anything extra, they're just kind of spying on you by default, the only thing that they've got to do is point their eyeball towards the data, and then they can see what's going on.
And if this peer-to-peer encryption would be deployed, they would actually have to install stuff, sync the blockchain…

Sjors Provoost:

Maybe not sync the blockchain, but they definitely have to do some work there and you would be able to see that it's happening.

Aaron van Wirdum:

Then potentially, if people would actually get on the phone call, which is something that you might do…

Sjors Provoost:

Again, only if a small number of people have to do this to catch them.
Of course we're still not in paradise, because we just said that when the government's looking at our connection, all they're seeing is noise, but it does turn out the cat and mouse game doesn't end there.
Noise still has patterns to it.
For example, if I'm sending you a transaction, that's a very small little thing.
If I'm sending you a block, that tends to be a bigger thing.
And those blocks also are all sent around the same time.
So the government might be running their own node, they say, 'Oh, there's a new block coming in, and right around that time, there's a lot of noise on all these different connections.
Well, what would that be?' Then at least they'll know that these people are running a Bitcoin node, also because they're all running on Port 8333, which is a bit obvious.
But it's already an improvement.
Port 8333 is something you can change, but right now, whatever port you're running on, the first thing you say when you connect to another node is the word 'Bitcoin.'
An ISP just has to listen for the word Bitcoin on any connection and then know that it's Bitcoin.
And with this, they would not.

Aaron van Wirdum:

Wait, maybe there's something worth pointing out.
Why wouldn't that still be the first word? You first need to know if you're talking with another Bitcoin node, right? 

Sjors Provoost:

Yes.
We should probably go into more detail about the handshake.
Instead of saying, 'Hello, I'm a Bitcoin node.
Would you like to talk to me?', I'm going to send you somewhere between 64 bytes and 2.5 kilobytes of what looks like completely random data.
And then you will send me also completely random data between 64 bytes and 2.5 kilobytes.
Part of this data that looks like noise is your public key.
In fact, it's the start of the data.
The first 64 bytes are going to be your public key, and the other way around.
The rest is called garbage.
There's a little trick that I take the first 64 bytes, and I know it's a public key, and then I'm going to treat it as a public key, I'm going to treat it as a Diffie-Hellman exchange, and that actually allows me to also read this garbage that you're sending me.
And then I know, we're done with the handshake and we do our usual protocol.
An outside observer will just see randomness but you will actually know that it's a public key.

Aaron van Wirdum:

What's in the rest of the stuff?

Sjors Provoost:

Garbage, literally random stuff or zeros.

Aaron van Wirdum:

I thought you said that you can decrypt the rest.

Sjors Provoost:

Yes, my understanding is that you can still decrypt the garbage and check that it is nothing.
Basically, you write a piece of empty text, and you encrypt it.
If I decrypt it and see an empty text, then I know you actually encrypted it.
It wasn't real garbage.
The reason we don't do it more simply is because if I just sent you 64 bytes and you just sent me 64 bytes, then any government can see, 'oh well, a Bitcoin node is anything that sends 64 bytes and then replies with 64 bytes'.
To make that more difficult, this garbage is added so the packages can be larger or smaller, there has to be a way for you to know when the garbage ends and when the real communication starts.

Aaron van Wirdum:

What's the goal here? I thought the goal was not necessarily to hide that you are a Bitcoin node that is doing bitcoiny stuff, but I thought the goal was to hide what bitcoiny stuff exactly.

Sjors Provoost:

The goal in the long run is to make it possible to completely hide that you're doing bitcoin stuff.

Aaron van Wirdum:

In the long run?
What else would be necessary for that?
That's not what we are now.

## Traffic shaping

Sjors Provoost:

No.
The general thing that you're gonna need for that is called traffic shaping, which means that instead of sending your data the most efficient way possible, e.g. I need to send you a block, I'm just going to send you one megabyte as fast as I can, you're going to make it look like something else.
Instead of sending you the block very quickly, I'm going to send it very slowly, and instead of sending you individual transactions, maybe I'm always going to send you 10 bytes per minute.
Sometimes those 10 bytes are empty, sometimes those 10 bytes are actual things.
It’s just going to look like something else.
Maybe I'm going to send a signal to you looking like a YouTube video.
That's basically the goal.
Bitcoin Core might not be doing that itself, maybe there would be some additional software that's doing that on top of Bitcoin Core, but in order to do that, it has to have very moldable material, like clay, it has to be able to change everything, it has to be able to make messages longer, make them shorter, well not too much shorter.
The function of this garbage in the beginning is to have an extra space that you could use if you needed in order to hide what you're trying to do.
Beyond that, you don't have to send everything at once.
In the future, you should be able to send 10 bytes and then nothing, and then 10 bytes and then another 10 bytes so that even the handshake would be broken up into smaller pieces, or made part of a bigger piece, whatever is necessary to hide from the sensors.

Aaron van Wirdum:

Okay.
That's the long-term plan.
For now, if this peer-to-peer encryption is implemented, ISPs and spies can still see that you are a Bitcoin node communicating with other Bitcoin nodes, but they can't see what you're communicating exactly, right? That's what we would be with this proposal.

Sjors Provoost:

Yes.
They already have to start doing some homework.
The great firewall of China should have no problem doing this, it's kind of their job, but your average home internet provider might not be used to this.

Aaron van Wirdum:

Let's say this is deployed and you send this BLOB.
Apparently, it's a public key and some nonsense, but I'm not upgraded yet.
What happens then?

Sjors Provoost:

There's two steps here.
One is that you can use the DNS seeds that we've talked about in one of the first episodes to find other peers that have this feature enabled.
However, you cannot really trust DNS seeds, and more importantly, somebody can mess with the information provided that way.
First of all, you'll try to connect to peers that can actually support it but then what happens is basically, you send your 64 bytes, if the peer that you're talking to does not understand this protocol, it will just hang up.
It's like, 'This is not a valid Bitcoin connection. Bye.'
Then the protocol will just try again using the original protocol.
It tries the new protocol immediately.
If it fails, it falls back to the old protocol.

Aaron van Wirdum:

Would my node still pick up the phone the second time?

Sjors Provoost:

Yes.
It's better than the other way around because if you do the other way around, saying, 'Hey, I know you're a Bitcoin node, but let's do the secret handshake now,' then you've kind of already ruined it because you've just told all the spies that you're a Bitcoin node.
That's why it's good to be able to immediately try the new way, and the only thing that happens is you get disconnected.
There's some subtlety there, nodes from version 22 and older give you a little bit of punishment for doing this, but more recent nodes have already anticipated that this protocol is coming, and they will not punish you for that.
They'll just disconnect but you can reconnect.

## Encryption vs. Authentication

Sjors Provoost:

I wrote about BIP151 in 2016, there was some controversy about it, and this had to do with the authentification.
How was that solved?
What's going on with that?

Sjors Provoost:

There are really two things: there is encryption and there's authentication.
Encryption is just the idea that we're hiding what's in the messages, but I can do that with anyone.
Authentication is saying, "Okay, I know that I'm connecting to this specific person" and that was controversial because if you start working with nodes that have an identity, and you say, "I'm only going to allow people from the KYC whitelisted node list or something like that to connect to me," that's kind of where you don't want to go.
That said, that's exactly how Lightning works, and it has not ended the world yet.

Aaron van Wirdum:

I guess on Lighting, it's also a little bit less crucial?

Sjors Provoost:

Well, on Lightning you need reputation.
They kind of need this concept of identity in order to have some reputation not too much but a little bit.
That's one of the reasons why they need the way they do it.
But on Bitcoin, in this proposal, there is no identity and there's also no authentication.
However, it can be built on top of it.
That's just not part of the proposal, but the proposal does make it possible.
Let’s say you're running a server park yourself with a bunch of Bitcoin nodes, and you only want to connect them to your own nodes, then you might be able to build something on top of this system that will let you do that.
But the sequence would be this: so another node from the Internet connects to you that will always work with this new protocol, and then once you've done that, you can say, "Okay, now I'm going to have some other messages with that node that does the authentication part." So you call a node, you answer the phone, you say, "What's the secret password?" And if they don't give the right answer, you hang up.
That's kind of the analogy.

Aaron van Wirdum:

Does this resolve the controversy? Is there still any conversation left as far as you know?

Sjors Provoost:

I'm not sure.
You can still make the argument at any step that makes authentication slightly easier is bad.
Then again, you can also make the argument that some risk might be warranted, given that it's also bad when governments can spy on all the nodes.
That discussion could still be had.
In any case, this proposal itself does not do authentication.
As we said before, if I connect to multiple nodes, we'll see a different public key for me.
There's no shared identity.
Of course, they’ll all know my IP address.

Aaron van Wirdum:

Is there anything else on the technical side of this proposal that we haven't discussed?

Sjors Provoost:

One minor detail might be fun to mention is the way the public keys are exchanged in the beginning.
As you know, the public key is created from the private key, but the way you do that normally, if you look at a public key, you can recognize that it is a public key.
And the reason is because it's like 64 or 32 bytes.
If you see something on the internet, you see these 64 bytes and if you see lots of public keys, you'll notice that you don't see all the possible numbers randomly.
It doesn't look random.
It looks like you're only using half the numbers, because roughly half the numbers are real public key if you have a random number, and the other half are not a real public key.
That creates a pattern that you don't want, because then again, the eavesdroppers will just look at a connection and see, half the time it's a public key, half the time it's not, so it's probably Bitcoin.
And so, there's one little ingredient there that converts your public key to a different format that does look completely random.
That's one of the little innovations that goes into the implementation.
That way, the entire handshake looks like completely random data rather than a public key followed by random data.

Aaron van Wirdum:

Where is this project?
What's the status now? When can we expect it in Bitcoin Core, if ever? 

Sjors Provoost:

It's not a consensus change, so you can already run it if you want to.

Aaron van Wirdum:

Is the code ready? 

Sjors Provoost:

It's testable.
I don't know if you want to use it on your main node.
You can look at bip324.com, which has an overview of the open pull requests, and it also links to one pull request that has the whole thing.
Other than that, you can wait.
I'm going to guess it's going to be in a future release.
It depends on how many people get excited about something at the same time that tends to speed up review, so maybe it's going to go faster now, but maybe not.

Aaron van Wirdum:

Thanks, Sjors.
That was clear enough for me, hopefully for our dear listeners as well.

Sjors Provoost:

I can also do a shout out to Stephan Livera’s podcast, episode 433, where he has all of the authors on the call also explaining conceptually why it's cool and that could make a nice addition to this episode.

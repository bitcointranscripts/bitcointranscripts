---
title: Bitcoin Was Under ATTACK!
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=XmKfOCUdH8k
tags:
  - bitcoin-core
  - security-problems
  - p2p
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2021-11-11
episode: 49
summary: "Hosts Aaron van Wirdum and Sjors Provoost finally met in Utrecht again to record Bitcoin, Explained. In this episode, they discuss a recent attack on the Bitcoin network, where some nodes were flooding peers with fake IP-addresses.\n \nAs previously discussed in episode 13, Bitcoin nodes connect to peers on the network through IP-addresses, which they learn from their existing peers. Nodes on the network essentially share the IP-addresses of other nodes.\n \nRecently, however, some Bitcoin nodes shared large amounts of IP-addresses that weren’t associated with real Bitcoin nodes at all. While this attack did not do very much damage, it did waste resources from nodes on the network. On top of that, Aaron and Sjors explain, the attack could offer the attacker insight into Bitcoin’s network topology by analyzing how the fake IP-addresses spread through the network.\n \nFinally, Aaron and Sjors discuss how the attack was solved by rate limiting the amount of IP-addresses than any node will allow its peers to be shared. Further, they consider how in free and open source software development, fixing problems is not always as straightforward as it may seem…"
---
Sjors Provoost:

Say, did you know that Bitcoin was attacked?

Aaron van Wirdum:

Oh, that's a much better angle.

Sjors Provoost:

And that the media is hiding this from us because they haven't been talking about it.
It's a cover up.

Aaron van Wirdum:

Yeah.
We have a-

Sjors Provoost:

We're going to bring the truth.

Aaron van Wirdum:

We're going to bring you the truth on this episode on the attack that was happening on Bitcoin, it was the attack of the fake peers.

Sjors Provoost:

The attack of the fake peers, yes.

Aaron van Wirdum:

It almost sounds like a movie title even.

Sjors Provoost:

Yeah.
I mean there's David Gerard's book, you know, Attack of the 50 Foot Blockchain, but this is the attack of the fake peers, yep.

## The attack of fake peers

Aaron van Wirdum:

All right, so Sjors, I think I'm just going to give you the stage on this one.
What was the attack?
What is that attack of the fake peers?
What happened, Sjors?

Sjors Provoost:

Well, it was a cold day in July.
No.
So somewhere in July.

Aaron van Wirdum:

So it must have been in the Netherlands if it was cold.

Sjors Provoost:

Exactly.
Somewhere in July, what people started noticing, people who are running nodes, is that sort of random people were connecting to them.
Now, of course this happens all the time, but these random people that were connecting to them would connect to them and then send, I think it was 500 messages and each of those 500 messages would contain 10 addresses that were supposed to represent other nodes in the network.
And that's quite unusual.

Aaron van Wirdum:

Yeah, so when you say addresses, you mean IP addresses in this context?

Sjors Provoost:

Yes, that's right.
So they would connect you and say, hey did you know about these 10 IP addresses?
And did you know about these 10 IP addresses?
And they would just do that 500 times and then they would disconnect.
And that's a bit weird.

Aaron van Wirdum:

So maybe before we move on, we should take a small step back, which is we discussed this in previous episodes.
You are our library guy.
So maybe you know which episodes these were, but we discussed in previous episodes how nodes essentially bootstrap to the network.
That is how do Bitcoin nodes find other Bitcoin nodes, right?

Sjors Provoost:

We discussed it in episode 13 and we talked about, yeah, so the node starts up and it usually looks at a DNS seed, say hey, tell me something.
If there's like five or six DNS seeds of people who are...
It's not really trusted, but it is definitely not untrusted either.
They get a list of nodes to connect to and then your node will just randomly try a couple and others and others.

Aaron van Wirdum:

Yeah, and now you're using the word node, but these are also IP addresses, right?

Sjors Provoost:

Yes.

Aaron van Wirdum:

So you start with a small group of IP addresses and then from there, the nodes you connect to, they will share more IP addresses of other nodes with you and that's how you connect to more nodes and that's sort of how the network forms, right?
So there are messages between nodes sharing IP addresses about other nodes.

Sjors Provoost:

That's right.

Aaron van Wirdum:

And it's these messages that you just explained were being spoofed.
Is that the right way to put it?

Sjors Provoost:

Well the messages are real, but the contents was nonsense.
So, indeed, a node would connect you and they would send you a bunch of addresses, but it turns out those addresses were just random numbers.
So an IP address is just a number, but one to 255 and then another number one to 255, et cetera.
Four numbers usually with IPv4.
And yeah, those numbers were just randomly generated.
So if you were to map them out, you would see they were all over the spectrum and that's not actually what the internet looks like because a lot of IP addresses are not used at all.
And so it included IP addresses that just cannot exist.
So clearly they were artificial IP addresses and the problem with that is that then the odds of there actually being a node there is not that good, right?
Because if you're just making up a random IP address, then there might not be a node there.
The whole point of gossiping the nodes is that you get actual nodes.
Because you could just try random IP addresses yourself if you wanted to.

Aaron van Wirdum:

Right.
So there were nodes on the network that were sharing random IP addresses with other nodes on the network.
And that's what we're defining as an attack here because the IP addresses that they were sharing were just random numbers and they didn't actually point you to a real Bitcoin node, right?

Sjors Provoost:

Yeah.
And apparently according to the people who did some research on it, it happened on a fairly large scale.
So, these people were connecting to lots and lots and lots of nodes in the network.
At least to the nodes that are listening because one of the things is if you're starting a node, you might not be listening to the outside world.
It depends.
Especially if you're behind a router, it's not always the case.
But if your node is listening to the outside world, then what it does is it actually tells its peers its own IP address.
So, the first time you connect to another node, you're saying, hey, by the way this is my IP address, please spread the word.

Aaron van Wirdum:

Do you say it's yours?
Or do you just give an IP address that is yours?

Sjors Provoost:

I think you just give one.

Aaron van Wirdum:

Right.

Sjors Provoost:

And the other node doesn't really know.
But you can give up to 10 and that's kind of the mechanism that this attack is exploiting is kind of saying, hello, here's 10 IP addresses and the usual assumption is if that's a new node then, you know, the first one is probably that node.
So they were kind of abusing the way that nodes used to introduce themselves to the network because once your address has been gossiped around, then people can connect to you and give you good stuff.

## The attack severity

Aaron van Wirdum:

All right.
So I'm running a listening node.
I don't think I actually am, but as a matter of example, Sjors, I'm running a listening node.
Now, there is this other node that we just explained that is sharing random IP addresses.
So it's sharing that with my node and we just defined this as an attack.
Why are we defining this as an attack?
What's the problem for me or for my nodes?
How am I a victim of what's going on?

Sjors Provoost:

Well, it's not a big problem for your node in reality.
So, it's kind of a mild attack you could say, at least in terms of, it's not an attack that would kill your node in any way.
It would just get these IP addresses and then, you know, we talked about in earlier episodes, I think anyway, when a node gets a list of IP addresses, it puts them in a bunch of buckets and shuffles them around and makes sure that it doesn't listen too much to the same source.
And so, you already have lots of IP addresses from earlier from honest nodes.
So most likely it won't bother you too much.
You might connect to a few nodes that don't exist, you know, you're just wasting some of your time, but not a huge amount.

Aaron van Wirdum:

But I would connect to these IP addresses?

Sjors Provoost:

Eventually yes.

Aaron van Wirdum:

Or would my node just notice that these aren't nodes and just disconnect immediately?

Sjors Provoost:

Well, but that process takes time, right?

Aaron van Wirdum:

Okay yeah.
That's what I'm asking, yeah.

Sjors Provoost:

Your node is keeping a list of IP addresses that it could potentially connect to if it needs more connections.

Aaron van Wirdum:

Got it.
So basically-

Sjors Provoost:

And then it will go through that list that is a useless list basically.

Aaron van Wirdum:

Right.
So it's wasting some of my resources?
It's wasting some of my resources because my node is storing IP addresses that aren't real Bitcoin node IP addresses.
So I guess that's a little bit of waste there.
And then once in a while, I'll try to connect with the node and that's a little bit of bandwidth waste and that's sort of it?

Sjors Provoost:

Yeah.
So, at the individual level this is not really, you know, you could call it an attack.
It's like a kid throwing a little pebble at you.
You could tell the kid, hey you're attacking me and you could shoot the kid, but usually we just keep walking.

Aaron van Wirdum:

Got it.

Sjors Provoost:

And nobody noticed it, right?
Most people who are not actively looking at their node would have not even known that this attack happened.
So that's good.

Aaron van Wirdum:

So then why would an attack, I think that's the next question, why would an attacker even bother then?
Because clearly someone was bothering to do that.
So what is the potential benefit of this type of attack?

Sjors Provoost:

So there's two people who wrote a paper, Matthias Gutmann and Max Baumstark link to it in the show nodes from, I believe, the Council Institute of Technology.
And the department is the Institute of Information Security and Dependability.
And I guess that might give a little hint.
So what they're guessing is that this attacker was not so much trying to destroy the network as they were trying to map the network to get a sense of how well nodes are connected to each other.
And the reason they can do that is because when you receive these 10 IP addresses, you will forward some of them to some of your peers, but not all of them.
So you get some exponential decay where you sent them to your neighbors and their neighbors send some of them to their neighbors.
And so if you're the attacker and you're also just running regular nodes, then eventually you'll hear some of the echo of your own attack, basically, because your peers will eventually relay it back to you.
And by looking at this echo, you can determine a little bit of what the network looks like, the shape of it, how well connected it is, how robust it is.

Aaron van Wirdum:

Right.
So, in the same way that individual transactions, for example, make their way through the network by nodes forwarding the transaction to other nodes.
They are also forwarding these IP addresses to other nodes.
So if you keep track of how the IP addresses are shared over the network, you learn something about how nodes connect to each other, which nodes connect to each other, in what order they connect to each other, that kind of stuff?

Sjors Provoost:

Roughly.
Though, not precisely.

Aaron van Wirdum:

Yeah and you can potentially use that to analyze the actual transactions as well?
So if you want to learn something about where transactions originate, for example.

Sjors Provoost:

I don't think you can with this type of attack, that's at least what I've been told.
But at least you can get a general sense of the shape, or maybe the robustness of the network.
So, that's useful information if you want to attack in the future perhaps.
Or, you know, more likely my guess would be maybe it was just research people doing research, right?
Some academic research, trying to find out what the network looks like.

Aaron van Wirdum:

Right.

Sjors Provoost:

And maybe they will publish a paper next year.

Aaron van Wirdum:

So, what it does is it helps you map the network and for whatever reason you want to do that, we don't know that, but it helps you map the network, it helps you figure out who's connecting to who?

Sjors Provoost:

Yeah, but there are some defense mechanisms in nodes already to make it not too easy to use this information.
So, for example, one thing is if you're telling a node a bunch of IP addresses, it's not immediately going to connect to all of them because that would be kind of obvious.
And it doesn't relay all of them and there is some time delay in when it relays some of them.
So, it makes it very difficult to say specifically which node connects to which node connects to which node.

Aaron van Wirdum:

And are these defense mechanisms specifically for this type of attack then?

Sjors Provoost:

That's my guess, but I'm not sure.

Aaron van Wirdum:

And have they've been in Bitcoin Core for a long time or are they new?

Sjors Provoost:

I think they get incrementally added.
I guess when people do these types of attacks, then people like Greg Maxwell and Pieter Wuille will look at it and be like, well maybe we can add this little defense.

Aaron van Wirdum:

Ah, I see.
So, these are attacks that have been happening more often over the past couple of years?

Sjors Provoost:

I think so.
Not this specific type of attack.

Aaron van Wirdum:

But these general types of IP sharing attacks?

Sjors Provoost:

I think just probing the network in weird ways.
But it's not really my area of expertise so I can't really tell much more about that than this vague answer that I just gave you that it does seem that people are probing the Bitcoin network.

Aaron van Wirdum:

Fair enough.

Sjors Provoost:

Often probably just for research, but who knows, you know, there might be some evil army out there that's looking for a way.

## Countermeasures 

Aaron van Wirdum:

So, is there a solution, is there a definitive solution?
Is this even a concern that developers feel deserves a solution?

Sjors Provoost:

So, there is indeed a counter measure that's been added.

Aaron van Wirdum:

This was already-

Sjors Provoost:

Like you said it wasn't a...
Yeah, so that's kind of the cliffhanger we can end on but first let me explain what the counter measure is.
The counter measure basically says that normally when people are acting nice, they will connect to you and they'll send you one IP address, namely their own and then occasionally they'll send you some other IP addresses, but not very frequently.
And the people have measured the average speed.
I think it's once every 20 seconds on average or something like that.
And so the is defense mechanism-

Aaron van Wirdum:

Once in every 20 seconds an average node will share an IP address with a peer?

Sjors Provoost:

Yeah.
It might be a different number but anyway, there's some average number.

Aaron van Wirdum:

Something in that ballpark?

Sjors Provoost:

Yeah.
And so you can use that by introducing sort of a rate limiter.
So a rate limiter basically says, okay, when a new node connects to me, I'll allow it to send me one address immediately and then I'm going to allow it every 20 seconds up to one address.
So it just tracks how many seconds have gone by, and if it's sending too many addresses, it'll just ignore the new ones that will go over this rate limit.
So you don't get punished for it, but this way when somebody connects to you and send a fire hose of addresses to you, you just ignore all of them.
Except the first one.
Now, there are cases when nodes actually want to receive addresses from their peer and there's a special message from that.
So, if somebody connects to you and you say, please tell me addresses, give me up to a thousand, then of course you will not rate limit the response.
You'll make sure that they can actually give you those addresses, but if it's unsolicited, then you rate limit it.

Aaron van Wirdum:

Sure, so it's rate limited unless you override that limit.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

Simple enough.

Sjors Provoost:

And that pretty much gets rid of this attack.
Now, the interesting part is that apparently this-

Aaron van Wirdum:

Is the cliffhanger?

Sjors Provoost:

This is the cliffhanger.

Aaron van Wirdum:

Nice.

Sjors Provoost:

This fix was added before the attack happened.
A few weeks before, or even just one week before.

Aaron van Wirdum:

So the fix was added in Bitcoin Core?

Sjors Provoost:

Yeah.
So not released, it was just in the...
No, it wasn't even merged.
So it was an open pull request.

Aaron van Wirdum:

Right.

Sjors Provoost:

So that means a proposed change to Bitcoin Core.
And it was open, and then I think a week later or so that attack happened and it was then merged like a couple weeks later, but it's been released now in version 22.0.

Aaron van Wirdum:

Right.
So the problem was anticipated, a solution was developed and before the solution was actually deployed, the problem was abused.

Sjors Provoost:

So it almost sounds like somebody saw the solution and thought maybe I can do this attack.
Right?
Or perhaps somebody was already planning this attack and then thought, oh shit, I better do it now because it won't be possible anymore soon.

Aaron van Wirdum:

Yeah that's an interesting point about open source development in general.
Now, this is a very innocent example, but we've seen other examples of this.
I remember, you know, back in the Bitcoin Unlimited days, if you remember that, where they had this alternative implementation that had a bug in it, and then it was basically the bug was fixed, but before the fix was deployed, the bug was-

Sjors Provoost:

It was exploited by somebody, yeah.

Aaron van Wirdum:

Exploited and it brought down all the Bitcoin Unlimited nodes at that time.

Sjors Provoost:

Yeah, so around 2013 on Bitcoin something similar didn't happen, but could have happened where I think the OpenSSL library basically was made stricter in its software by saying, okay, the signatures have to be, I don't know, some positive number or not a negative number.
Some constraints on the signatures was made because otherwise OpenSSL would be unpredictable or something like that.
And it was presented as just a nice cleanup software, but it was actually also a patch for a security vulnerability where somebody could have posted a slightly different kind of signature and caused a fork because some nodes would accept it and other nodes would not accept it.

Aaron van Wirdum:

This is a very interesting problem.
I think it has happened a few times before, and it seems like the overall solution from Bitcoin Core developers is to pretend that it's not a big deal until people have actually downloaded and used the software, and then later they'll reveal that it was actually a much bigger problem that they-

Sjors Provoost:

At least in those examples, that that seems to have happened, yeah.
And that's of course not ideal because in open source development, you want to be very transparent about things you're changing because, you know, if you're being not transparent about fixing a critical bug, then maybe you're also not transparent about adding inflation.
Right?
So, it's a delicate balance.

Aaron van Wirdum:

Well, that's another example actually.
There was also the inflation bug a couple years ago and that was another example where the fix was presented as something very unimportant.

Sjors Provoost:

Well no, it was presented as important, but it was not the full truth.
It was presented as this will crash your node this bug, and we fixed a bug that can crash your node.
And that was true, it could crash your node, but it could also create inflation.
Which was a bit more important and that was of course not announced.
Because somebody could have done that in that window of opportunity.

Aaron van Wirdum:

It's an interesting problem.
Anyways, back to the fake peers attack.
The fake peers attack happened as we discussed after a fix was actually written but not deployed yet.
But now the fix is deployed.
It was deployed in Bitcoin Core 22?

Sjors Provoost:

Yeah, so anybody's who is running Bitcoin Core 22 won't have this problem and anybody who doesn't still doesn't really have the problem.

Aaron van Wirdum:

Got it.
I think that covers it all, Sjors, for now.

Sjors Provoost:

I think so too.
So in that case, thank you for listening to Bitcoin Explained.

Aaron van Wirdum:

There you go.


---
title: Rusty Russell, Joe Netti
transcript_by: Michael Folkson
speakers:
  - Rusty Russell
  - Joe Netti
date: 2019-08-12
---
Stephan Livera podcast with Rusty Russell and Joe Netti - August 12th 2019

Podcast: https://stephanlivera.com/episode/98/

Stephan Livera:	Rusty and Joe, welcome to the show.

Joe Netti:	Hi. How’s it going?

Rusty Russell:	Hey, Stephan. Good to be back.

Stephan Livera:	Thanks for rejoining me, Rusty, and thanks for joining me, Joe. So, just a quick intro just for the listeners. Joe, do you want to start?

Joe Netti:	Yeah, sure. So, I got into Bitcoin in around 2013, and took me a while to learn what it was about, and then I just kept diving deeper. Now, I go to school at RIT in New York studying computer science, and this past spring I did an internship at Blockstream where I was with the Lightning team, with Rusty and with others, working on Million Channels Projects and some plugins and Lightning, and that’s where I am today, just interested in Lightning and Bitcoin and all that jazz.

Stephan Livera:	Yeah, it must be awesome to be interning at Blockstream. Rusty, look, I think all my listeners know who you are, but maybe just take a minute. Just for the ones who don’t know you, just take a minute and tell us what you’re working on these days and what’s your role.

Rusty Russell:	Yeah, so, I guess, mostly I’m known for my work on the Lightning implementation, c-lightning, and the spec efforts. So, like obviously, all the implementations we work together to try create specification, which really, I mean, I consider more important than the implementation, right? Code, you can throw away, but you’re stuck with whatever you agreed with to interoperate, right? So, that’s what I see as my main role is to ship at that spec process and bring everyone together on that, and that’s obviously pretty exciting. Lots of lots of great stuff coming down the pipe there.

Rusty Russell:	Also, I’ve got the team at Blockstream, three of us now, doing the c-lightning implementation and a whole heap of other people. It’s an open source project. We get a lot of cool contributions, single drive-bys, and more significant contributions. In fact, they name you at the releases, which we’ve got a release coming out tomorrow. Well, actually, one of them come out tomorrow, so the rest come out next week. The release gets named by whoever’s done the most contributions in the last cycle or who hasn’t already named it, so it’s always fun to see who’s going to get to name the release. We have a stave for our release names, but that’s an open secret among people who’ve named it already.

Rusty Russell:	So, yeah, my job’s to shepherd those two projects mainly and just random things with Blockstream and everything else. So, there’s always a whole heap of stuff going on. The first intern I have had was Joe, actually, which has set me up. I think I’m really well, like my expectations are really high for what interns should do, because Joe did amazing work on the Million Channels Project, but he also, in his copious spare time that that left him somehow.

Rusty Russell:	He also did great GraphQL plugin stuff for us. That’s really exciting, obviously, that you’ll be hearing more about in the future as well, I expect. So, yeah, I guess that’s me, and that’s us, and how things are working.

Stephan Livera:	Sure. Great. Yeah, that’s awesome. So, look, and the topic or our theme for today is the million channel experiment. So, let’s start with a little bit of what spurred this experiment.

Rusty Russell:	Cool. So, the backstory is… Now, we’ve seen this sort of explosive growth in the Lightning Network. It went from it doesn’t know it’s in 2018 that it started on mainnet, and it kept growing, and we’ve seen some teeny problems with scalability issues a couple points, and there was this idea. “What we should do is we should simulate an endgame, like what it’ll look in a million channels,” which is a normal… It sounded like a big number at the time. It’s actually not such a big number now. I think we’re around a 20th of that now.

Rusty Russell:	So, at the time, it was like, “Wow. Wonder 100 times bigger, what will things look like?” I had this idea, never had time to implement it. Ended up putting it in a blog post, going like, “Hey. It’d be really cool to do this Million Channels Project where we simulate what the network might look like if we scaled it up. We had a million channels and however many nodes that is and everything else. Then we could basically simulate that and throw some existing software at it, and let’s watch it fall over and die.”

Rusty Russell:	Obviously, you find out that, that way, what was going to happen when we got that big because it’s like the whole idea with implementations has been where there’s been so much stuff to do that optimizing hasn’t necessarily bubbled to the top, except as you need to put out fires, right? So, to try to get ahead of that, the idea for Million Channels Project was to create this real stress test, this genuine thing. Then when Joe came along as an intern, he was really excited about it and saying, “Right,” and then he basically took that between his teeth and ran with it.

Stephan Livera:	Awesome. So, Joe, let’s hear from you a little bit. What was your experience like with setting up and taking part in this, and as I understand, you took a snapshot of the current Lightning Network, and you used that to help inform this project?

Joe Netti:	Mm-hmm (affirmative). Yeah, it’s really cool. All right, so basically, it started as a very open-ended project. There’s quite a lot we could do. We could make a regtest network. We could simulate it to as precise as we want it to, so it was very open-ended, and I had to define what I wanted to do. So, it took me a while to dance around, to understand what the current properties of the snapshot of Lightning Network was and then make an algorithm that would make a larger also accurate Lightning Network. Should I go into the properties right now, about what I learned about the snapshot and stuff?

Stephan Livera:	Yeah, sure. Let’s do that. Do you want to maybe tell us what is regtest mode as well?

Joe Netti:	Sure, yeah. So, regtest is something that a lot of Bitcoin developers use to test their applications. Instead of using the main chain, they use this very lightweight local chain and tool called regtest mode in bitcoind on Bitcoin Core. It allows you to make blocks with… that you’d basically have no difficulty, so you could just mine blocks, you can just make transactions, and you can make a fake chain so that you can test your application.

Joe Netti:	Since the Million Channels Project made a large-scale Lighting Network, each channel in Lightning Network also has funding transactions. So, well, I made a regtest replica of all of those funding transactions, basically a fake chain with blocks with all these funding transactions that matched what the Lightning Network was, and that was pretty cool.

Rusty Russell:	Which was much cheaper than giving him a million dollars to do it on the real chain.

Joe Netti:	Exactly. Exactly.

Stephan Livera:	Let’s talk a little bit about the gossip of Lightning nodes. So, how do Lightning nodes gossip to each other right now?

Rusty Russell:	So, basically, you’ve got two parts of the Million Channels Project. We want to step back a bit. One is this. You obviously need a blockchain because what happens is, as a layer two thing, you need a layer one. When a node says, “Hey, I’ve got this channel. You actually check on the blockchain that actually exists.” So, you do need the two parts, so you have this regtest fake blockchain, but you also have all these gossip messages, and the gossip messages are basically, “Hey, here’s this new channel, and I can prove it, right? I can prove that I own this channel.” That basically tells you where in the Bitcoin blockchain to find the transaction that hasn’t been spent yet. It is the right size.

Rusty Russell:	You go, “Yeah, cool. I believe you. You two definitely have this channel. Good.” That’s the channel announcement. There’s a channel update, which is basically, “Hey, I decided I’m going to charge this amount of fees and stuff like that,” and you have two of those. You have one for each direction because I control my half of the channel; you control your half. “Oh, cool. I’m going to start charging these fees on stuff going through my half of the channel my duration,” right?

Rusty Russell:	I know you have node announcements. So, nodes basically announce stuff like, “Hey, here’s where you can reach me. Here’s my IP address. Here’s where you can access me on Tor. Here’s my favorite color, and here’s my alias.” We literally have these two fields in there, which people love, right? They’re completely from one sense. They’re completely useless in one sense, like you can call it your node something, and I can see it on explorers, and I can call my node exactly the same thing, and no one will be able to distinguish, right?

Rusty Russell:	There’s this public key that can distinguish them, but the node name, anyone can make up, right? So, they’re not secure. They’re just for fun, but it proved to be like a really useful thing. But the node now really is for advertising where how you can connect to a node and stuff like that if you want to establish the right channel.

Rusty Russell:	So, you have all this gossip, right? You basically have this, “What did it turn out to be? Do you know? Is it like 70 megabytes or something?” Basically, just this fire hose. Here’s everything about the network once.

Stephan Livera:	731.

Joe Netti:	And more than 730. Yeah, 730 megabytes.

Rusty Russell:	730, yeah. Yeah, it’s a chunk of data, right? That is basically think it like this new node going up, going, “Hi. I’m new on the network,” connects to one of these other nodes. Here’s why. Here’s the million channels that you don’t know about and just would throw 730 megabytes at it of this entire description of the entire network. So, you can see the kind of things that we’re dealing with when you’re looking at, “Wow, okay, that’s fun for an implementation to handle that.” So, yeah, that’s the gossip, right?

Rusty Russell:	There’s this pre-canned gossip, which is basically like, “Here is the description as if you had connected to a new node,” and it was going to tell you everything about it. This is it, and it’s 731 megabytes, right? It’s a chunk.

Joe Netti:	Yeah, can I add to that?

Stephan Livera:	Yeah, sure. Go for it.

Rusty Russell:	Yeah.

Joe Netti:	So, basically, you can split the million channels into three parts. You can see it as taking a snapshot and making a larger simulated network, and then the second part is making the regtest data, and then the third part is making the gossip data. Rusty just described the gossip part of that. So that’s literally channel announcements, channel update messages, and node announcements.

Rusty Russell:	Yeah, so I know you’re probably going to segue into this, but this is where Joe and I intersects, right? He produced this massive… “Here’s 730 megabytes, Rusty,” and I tried to feed it into c-lightning and watched it like slow to a crawl. I remember the first time Joe tried to feed it in. He was like, “Well, it’s been running all night, and it hasn’t even [inaudible 00:10:47] yet.”

Joe Netti:	Oh, man that was horrible, yeah.

Rusty Russell:	Yeah, yeah, like there were just some dumb stuff that we completely hadn’t looked at. What are we doing with this significant amount of data here? So, there was a whole heap of iterations of trying to get this all manageable, because on the scale of over 20… At the time, like it was almost 50 times what we were dealing with, and a whole heap of stuff that dumb things we were doing that we have to go through and revise that.

Rusty Russell:	So, for me, the exciting part was actually taking this massive gossip output he produced and trying to cram it into one of my nodes and watch it fail in different ways.

Joe Netti:	Yeah. It was crazy how many iterations there were with Rusty’s optimizations. There was a wave of optimizations and a second wave and third wave. It just kept coming.

Rusty Russell:	Yeah, but it was never fast enough, right?

Joe Netti:	True.

Stephan Livera:	So, in order to create that estimate as well, so as part of the regtest part of this experimental project, you had to create all the funding transactions, which is when somebody is starting and opening a lightning channel. So, what was your process there around trying to simulate that?

Joe Netti:	Yeah, so that wasn’t that bad. Basically, I just grabbed the Python library that allowed you to make scripts and custom scripts and stuff. I just made a bunch of two-to-one multi-sig transactions, which have helped the funding transactions and then just basically made a bunch of… spent a bunch of coin bases to a bunching funded funding transactions, and that’s it, and that was it, yeah. The hardest part… That wasn’t that hard. The harder part was… Actually, I will mention this.

Joe Netti:	The Python library I was using was so slow with signatures that I didn’t want to rewrite it in different language after I already wrote it. So, I just ended up doing this massive threading thing where, well a really paralyzed thing where I just made a bunch of signatures paralyzed because it was just so slow. So that was funny, but yeah.

Rusty Russell:	Also was funny that you ran out of money, right?

Joe Netti:	Oh my God. That was [crosstalk 00:13:12].

Rusty Russell:	To actually create the-

Joe Netti:	Yeah. So, it’s a weird quirk in regtest mode.

Rusty Russell:	Who knew, right?

Joe Netti:	So, you know the Bitcoin halving, there’s every, like I think around two year is a halving. Well, in regtest mode, since they want developers to be able to experiment with what happens when there’s a halving, they have halvings every like 250 blocks or so, and that’s nothing. I didn’t want to have developers that are using Million Channels Project to have to go in and recompile Bitcoin Core… change parameter, recompile Bitcoin Core. So, we had to actually scale down all the channel capacities set by a factor of… I don’t know, like 10,000 or something like that, so they would actually wouldn’t run out of money. That was dumb, but it’s pretty cool.

Rusty Russell:	There were literally not enough regtest Bitcoins because it halves too fast, and this is something we just didn’t even realize playing around with it, and then Joe’s like, “I’m out of money.” I’m like, “How are you out of money?” Yeah, literally, because you run out of block rewards too fast. So, there were some quirks in there of like trying to simulate this massive network. So, it ended up like this model train version where it’s scaled down, but the math doesn’t matter, right? Who cares, right? One Bitcoin is one bitcoin. It’s all the same, but it was just an added hurdle in there that Joe discovered.

Joe Netti:	I like that model train example. That’s basically what we’re doing is making a mini example of what Lightning Network could be.

Stephan Livera:	Yeah, and as part of that then, you’ve got this power law distribution, which you used to model all that out as well in terms of how many nodes there are, how many channels those nodes have, and what is the capacity of those channels. Can you comment a little on that?

Joe Netti:	Yeah, definitely. So, there is about four properties of the Lightning Network that I thought would last in the future, and that’s what we’re doing. We’re going to predict what Lightning Network’s going to be and take away the properties that are fundamental to how this network will work. One of them is that there’s a power law distribution, and a power law is basically, like you can imagine, like a hockey stick. There’s a power law distribution of the number of channels across nodes.

Joe Netti:	So what I mean by that is around 20% of the nodes will have one channel only. Around 10% might have two channels. Around maybe 5% will have three channels and so on. It gets less and less and less in a power law distribution. You could search that up. That’s cool. It shows that there might be long-term hubs where there’s a small amount of nodes that have a lot of channels. Maybe it could be like a thousand channels maybe and then most nodes only have one to five. So, I try to get that property into the simulation. On top of that, there’s a second property.

Rusty Russell:	Certainly, to be fair, we’re seeing that today, right? So, we have a certain number of whales. We have a whole heap of minnows. We have a whole heap of range in between, but that is definitely the way of the network. This is a lot of things, right? So, Joe… He’s got his power law. He describes a lot of natural networks that occur. You end up with a certain number of huge things and a small number of large things and then like in a whole heap of minnows, and that’s definitely what we see today. I think Joe latched on that as like, “Okay, that’s pretty well established. That’s going to continue.”

Joe Netti:	Right, exactly, and not only with number of channels. It’s also true with the amount of Bitcoin that is held by each node. There’s some small amount of nodes that have just a ton of Bitcoin in their channels and then some nodes that have a very small amount of Bitcoin in their channels, and it follows the same distribution, which is also the second property that’s modeled in this new network.

Stephan Livera:	Right. You’ve got your Bitrefills and your LNbigs of the world.

Joe Netti:	LNbigs.

Stephan Livera:	And then you’ve got… Yeah. I’m also interested to talk a little bit about routing. Now, Rusty, I’ve seen some… You had a few blog posts talking about this, and I think back in the earlier days, you were talking about how you had this approach of Bellman-Ford-Gibson. Maybe we’ll just start with a few basic points around routing. What are some of the things that we should think about there and what were some of the decisions made around know what algorithm to use?

Rusty Russell:	Cool, so, yeah. First, when we talk about routing and for privacy reasons, the sender decides where the routing’s is right, so we look through and go, “Okay.” You decide how to get the payment to the recipient. It’s also because you’re paying fees at each point, right? So, you have to know what fees you’re going to have to pay. So, you preload that into your payment. But also, each layer basically unwraps it and then, “Oh. Okay, so that’s who’s going next.” The hops on the path can only see where it just came from, where this was sending to.

Rusty Russell:	So, that provides anonymity for the sender, and it provides obfuscation for the receiver, right? The receiver doesn’t know where the sender came from. The sender obviously knows where the receiver is, but the sender, no. In order to make that work really well, you have to have a fixed-sized thing that’s going through, obviously, if you decrypted it, took the head off, and sent the rest of it along. It would get smaller. The message would get smaller.

Rusty Russell:	If you went, so if you did it naively, and you be like, “Look at the size. Well, I reckon the next hop is the last one,” right? Which would obviously leak too much information, so you have to pick a number. How big is this? You’re going to pad it as you go through, but all of them need to be the same size, so that’s a good number. We chose 20 because, well, it’d cost us this much for each hop. We multiply it out. We want to be able to fit it in one TCP packet in 300 bytes, but let’s go for 20.

Rusty Russell:	Interestingly, even in the Million Channels Project, this was not an issue. Even with a million channels, you didn’t need to use 20 hops. I don’t think… Joe, did we actually measure the worst case, which, from the furthest two points?

Joe Netti:	Yeah, I don’t think we did, but I highly doubt it actually reached 20.

Rusty Russell:	Yeah, we might’ve been able to find some perverse thing that maybe thought close, but generally, no. You didn’t need anything like this. So that shows that, and that we… The 20 was way more than we probably needed. Interestingly, we just merged in the spec change of variable onion. So we’ve actually bumped that number up. Rather than each one being fixed, we now go for a variable-sized chunk that you take. So, we still got the same total, but actually, you can squeeze things in a little bit more, and you could probably get to 24. The reason you do that was actually the reverse that we want to cram more information in for some hops.

Rusty Russell:	But as a side effect, we can actually probably get out to maybe 28, I think, is the new reasonable… but we don’t need it, right? Even for the 10 Million Channels Project, I think we’re still going to be good for 20 hops. That’s why we have that kind of limit there.

Joe Netti:	Yeah, part of reason why I think we’re also good is just if this power law thing continues, then there’s going to be these hubs. Basically, some nodes will have a lot of channels, and that’ll help us not reach this 20 whatever limit right.

Stephan Livera:	Right, so we’ve got this idea then that more hops can theoretically give you more privacy, but that’s additional packing of fake layers, as you mentioned, the padding, and then if it’s less hops, then theoretically it’s cheaper because you’re going less hops in the route. Rusty, can you also chat about how I think in the earlier days, there was that concept of potentially having negative cost for rebalancing and then that being removed from the spec?

Rusty Russell:	Yeah, so it didn’t make it into the spec 1.1, but it was originally this idea of, “Hey, you can offer people money to use your routes,” right? Andreas Antonopoulos said this really good analogy of a channel, like a PVC pipe with peanuts in it, right? All the peanuts started on my end, and I send peanuts across to your end. I like this because it just shows that whole channel balance problem, right? I mean, if you don’t have any peanuts in the pipe, you can’t send any more to me.

Rusty Russell:	So, you do want to keep your channels balanced, and there was this idea that, “Well, what I could do is I could provide negative fees by just basically paying other people to balance the channel for me.” If you use this channel, I will actually pay you to send some money through because I want you to balance. Christian Decker points out that that doesn’t actually make sense because you could do that yourself by routing round in a circle.

Rusty Russell:	You go, “Well, I can push out through that node and around through that node and back to that node, and then I can push payments around to rebalance my own channels.” If it’s expensive for me to do that, so if that actually starts making sense, you go, “Well, then other people will start routing through that way anyway.” So, it turns out there isn’t actually a huge demand for providing this kind of liquidity because you can do it yourself.

Rusty Russell:	The other thing is that, ideally, you don’t think negative. You just seem to be cheaper than everyone else. Now, at the moment, we’re seeing ridiculously cheap fees for routing of a light network. It’s probably not sustainable. I expect long term, they will go up just simply you can’t charge like a millionth plus one satoshi for a payment. At one millionth, it’s just not enough to keep the lights on. So, I expect those numbers to creep up. People want reliable nodes. They want them to be on all the time. They want them to have high availability, lots of capacity. That number is going to have to increase.

Rusty Russell:	Once that has increased, then you don’t need to go negative. You can just go, “Well, I’m just going to go really cheap,” and people will start funding through this. Also, from a technical perspective, it turns out the number of algorithms break down if you have negative fees, right? Your algorithms really want to start routing… Use your 20 hops to go round in a circle as many times as you can to go through that negative fee one to collect as much money as you can. You have these really weird situations where the ideal is strange.

Rusty Russell:	So, negative fees actually just from a computer science point of view becomes difficult. That didn’t make it into the spec, there wasn’t enough conviction that it needed to go in, and I doubt at this stage it’s going to. Of course, you could always implant negative fees on top, like I promise that if you try to use it. So, what happens is when you actually send a payment, you say, “Here’s the fee I’m prepared to pay.” Now, normally, that would match what they advertise, right? They’ll be like, “Well, yeah. I said you had to pay 0.1% plus 10 satoshis,” and that’s what you’ve done.

Rusty Russell:	If you don’t know, they can choose to accept it anyway. They go, “Oh, you’re overpaying me on fees, but that’s cool. I’m happy with that,” or you’re paying less. So, you could have some external thing where someone advertises, “Hey.” They tweet out, “Hey, if you route through here, I will accept negative fees. I will actually pay you to do this.” If that becomes a popular, then we’ll make it a mainstream thing. I can put in the gossip algorithm and make it all work, but we haven’t seen a huge demand for that at the moment.

Stephan Livera:	Great. Joe, did you want to comment a little bit around the differences that you see between the Bellman-Ford-Gibson versus the Dijkstra algorithm?

Joe Netti:	I don’t have too much to add to that.

Stephan Livera:	Okay, sure. Rusty, did you want to comment a little on that as well?

Rusty Russell:	Yeah. Okay, so we went for this superb elegant algorithm that basically will give you the best at the cheapest route for every possible distance. So, because you’ve got this in this hard limit, like it doesn’t matter how cheap a route is. It’ll take you 21 hops to get there. As I said, normally, we don’t hit that, but it’s quite possible if somebody could deliberately force you into that by creating this long chain of nodes that just designed to mess with your implementation.

Rusty Russell:	They’ll create a long line of channels that goes like just this whole loop that’s like 20 long. That’s free, right? The computer science, like your dumb routing algorithm is just going to fall down that hole all the time, and they’re going to keep trying to route through that. They go, “Oh, but wait. It’s the cheapest, but I can’t use it because now, it’s 21 hops,” right? So you do have to be robust. You have that kind of adversarial behavior even though it, quote, “never happens.”

Rusty Russell:	So, Bellman-Ford-Gibson is incredibly elegant and will give you the best answer for every possible distance, right? Like for zero to 20, it’ll say, “It’s not possible to get there in less than five hops, and here’s the… ” Look at the [inaudible 00:26:00]. Cool, even in seven hops, and that’s cheapest. If it goes this path. Great. It gives the answer all at once, but it’s relatively slow, and the Million Channels Project, it really starts to divide us. Actually, that’s starting to hurt.

Rusty Russell:	Okay, so we have to do something less than perfect, and you have a lot of wiggle room here because basically these are so low, but you don’t actually need the cheapest path, right? You need something competitive. But if you’re paying an extra 10 millisatoshis, nobody cares. They really don’t care, right? To remember, like if Bitcoin hits a million dollars, then one satoshi is one cent. So, at that point when Bitcoin has like totally mooned, and a satoshi is worth a cent, a millisatoshi is still a fraction of a cent, right? Nobody cares.

Rusty Russell:	So, you can do a whole heap of approximations, and there’s this great algorithm called Djikstra. It’s really fast, but it doesn’t handle… it falls off a cliff if you have more than… If you have some kind of length limit. So, what you do is you run that, and most the time there’s no adversarial network. Nobody’s doing any crazy stuff, and you’ve got your answer. But then if it doesn’t work, you still have to fall back on something that can handle the hard cases, and that basically cut through a lot of the stuff that we were doing. It meant that we had a much faster competitive routing algorithm.

Rusty Russell:	There’s more room to go there, right? It’s just completely generic. Most of the time you’re asking the same question, which is how do I get from my node to somewhere else? You’re asking the same question over and over again. So, you can engage in all of the stuff. We can get smarter. There’s already been some talk of, “How do we handle really massive rates of queries?” I did a measurement recently on the current one on my Raspberry Pi. It takes on average, if I pick two random nodes, to get a route between them.

Rusty Russell:	To get an answer back, it takes an average of 300 milliseconds, right? That’s on my little Raspberry Pi. It’s this tiny little Pi 2 B computer. It was the previous generation of Raspberry Pi. So, I run that just so I can do these kind of tests. Now, a third of a second’s not fast, but it’s not slow either, right? That’s acceptable in your mobile phone. So, your cellphone, you hit route, it takes 30 seconds to figure it out. That’s okay, but we can definitely get more aggressive, and we can do even more stuff on top of that.

Rusty Russell:	There’s been talk of what do we do because what happens if that first route fails? You have to find another one that goes around that bit. Yeah, we can do a whole episode on the fun of routing algorithms, but basically, yeah. This was one of the great outcomes of this project. So, yeah, this really is going to be a problem here. We really can do better. There was no immediate intent to do it today, but Joe threw this stuff at me, and I’m like, “We’ve got to get that on this, right? We can’t take 10 seconds to route through this thing. We’ve got to cut loss of seconds.

Rusty Russell:	So, the numbers are in the blog post, and yeah, Dijkstra was a big improvement although we have to have this fallback approach. To handle hard cases.

Stephan Livera:	Right, and as I understand, with the routing algorithm using Dijkstra, is that something at a specification level or is that more of a c-lightning level?

Rusty Russell:	Yeah, more of a c-lightning level. I mean, yeah, you pick how… You’ve got the graph. You’ve got the map. You figure out how to get there, right? It’s more freeing in a way. I don’t have to ask anyone else. I can just go and go, “Okay, let’s try this and do stuff.” But yeah, some of that knowledge, of course, is shared between all of the teams though. So, even that implementation details stuff, we do talk all the time about. “Hey, how are you guys solving this? How are you doing this one?” So, there’s a lot of informal communication, but it doesn’t have to be at a spec level.

Stephan Livera:	Let’s talk a little bit then. So, you mentioned there around the RasPi and trying to make it work for the RasPi. Versus routing from a desktop-level PC. How do you think about that? Is it going to be most… Do you think most users are going to be out on a mobile, and they’re going to have to route from a mobile? Or is it more like that mobile is connected back to their, say, their desktop PC, so therefore, they can let the desktop PC do the heavy lifting?

Rusty Russell:	I think it’s clear that we’re headed… We’re an all mobile world now, right? So, you really do have to fit into that form factor. But also we have a user who was complaining about performance issues, and I was like, “What’s your platform?” He’s like, “Well, I’ve got this little Raspberry Pi, and I’ve got this external hard drive I plugged in.”

Stephan Livera:	I’m thinking, “Wow, that is like… “

Rusty Russell:	It’s not even an SSD. It’s spinning rust. The Raspberry Pi has this really crappy USB port list of the three they do. So, yeah, it’s like, “Wow. Okay, so that’s as slow as you can get.” So I went out and got one, and I installed c-lightning on it because if we’ve got users who are running this, I want to make sure that it’s usable, right? You can look it up on explorers, and Raspberry Pi is the… Raspberry Pi here, it has one channel open for the moment.

Rusty Russell:	So, this was exactly what was kind of the point, right? Can we get both scale up and scale down? Let’s take the Million Channels Project and put it on the crappiest hardware we can find because if your cellphone could handle a million channels on the Lightning Network, then I think we’ve certainly buried a lot of FUD about scalability in Lightning Network, right? The answer is we made it work, but we didn’t make it fast.

Rusty Russell:	So, yes, it works. We got it on there. It does not run out of memory anymore. It gives you answers slowly, and it does right. You can actually use it, which is amazing, but it is not a pleasant experience, so there’s another level there. The other level is like, “Do we do all this optimization?” But then Joe comes along and goes, “Oh, cool. Here’s the 10 Million Channel Project,” or the Million Nodes Project or something and pushes the envelope again. So, we do this optimization. We end up still as slow as we are just doing 10 times as much work, or then we go, “No, a Million Channel Project’s where it’s at, and we’ll keep working on that and optimize it to the point where your cellphone will handle it comfortably.”

Rusty Russell:	I don’t know. Optimization’s this thing where you can keep refining and speeding up, and you can keep doing that pretty much forever. So, at some point, you’ve got to actually ship. We got to work. We’ve got reasonably happy, and we’re done. Here are the numbers, right? They’re not pretty. It does work. It’s not fast, but it was important to us that we made some inroads on there because I think that’s… We are headed into a totally mobile world, and we’re going to need to do that.

Rusty Russell:	Now, this is, of course, a full Lightning node, right? It’s not clear that your Lightning… As you mentioned, maybe you’re connecting back to up to a full node somewhere. You’re not doing all the work on your cellphone, and I think that is probably more realistic, but it’s certainly, hey, we’re geeks, right? It’s fun to go, “Can we do this?” The answer was, “Yes, we can.”

Stephan Livera:	There are also some of these other ideas being thrown around on the Lightning-dev mailing list and other potential routing schemes. Did you want to touch on some of those, what are they, and what are your thoughts on those? So, I’ve seen here ant routing and some of the others. Did you want to touch on those?

Joe Netti:	Yeah. This is still very experimental, but basically the idea is like, for example, these beacons for example. What if we could make a routing scheme where instead of needing the entire network graph, because that could be a lot of data. We saw that with a million channels that could be like 700 megabytes of data. Instead of doing that, what if you just have the part of the network that allows you to reach these beacons. Then if the person that you’re trying to send money to can also reach a beacon, then you could pretty much, like basically a node that you can both reach, then you can do this routing between them, and that’s a possibility.

Joe Netti:	There’s other possibilities too. Then there’s also like BGP, which is the internet protocol. I don’t think that would ever work because… But there’s approaches like with BGP maybe that are ideas of how routing could work, but I don’t think that it could work with Lightning Network because it just changes too fast. You can’t store a routing table of all these routes if the network is changing so fast that all these update messages would have to be passed from the network. It just wouldn’t make any sense.

Joe Netti:	There’s privacy concerns with BGP, and that leads to like ant routing. What if you just send these encrypted blobs? That’s confusing. It’s very experimental, but it’s basically like adding these extra data bits that allows you to find a route in real time by these encrypted blobs being traversed from the network. It’s cool, but it’s very, again, experimental.

Rusty Russell:	Yeah, I think Joe covered that pretty well. Yeah, there are subsets of schemes where you’re like, “Well, what if we don’t have to put the whole thing? What if we can have some subset of knowledge, or you can find out?” Now, the problem is with subsets, you’re going to be less efficient, but maybe that’s okay. Who’s in the subset? Who’s in the magic group of beacons? Who becomes a beacon? Who are these landmarks that everyone uses? Because they’re going to get more payments than… Not landscapes. You have this fairness issue as well.

Rusty Russell:	How do you select them? Stuff like that. There are potentially some ways around that, but other schemes where you ask for directions, and then you immediately hit privacy problems, right? You go, “How do we get a payment to Joe of 0.013 Bitcoin? What’s the cheapest way? Oh no reason. I’m just asking for a friend.” You’re obviously leaking some data there. So, there’s some things where you can combine these approaches and stuff. But what we’re doing is like the naivest… You know everything on the network. You’ve got the entire map. Go find a route, right?

Rusty Russell:	But these schemes are much more like, “Okay, so if we fall off the edge of the cliff there, we go, ‘No, no. 10 million channels, way too many. You can’t keep that on your cellphone. What’s our fallback?’ So there’s a whole area of research on what cool things we can do with that, which I think is interesting. Also, you look at it. You go, “Cool,” and even if you can handle it all, the one gig download to get the map on your phone. It’s pretty significant, right? That’s a big ask.

Rusty Russell:	Now, we can squeeze that data down somewhat. Taproot and Schnorr actually help us a little bit. We can do some pretty cool stuff, but it’d still be that order of magnitude, right? So, it’ll be more than 100 meg of data to pull down to know the entire thing, so that you’re like, “Well, okay, maybe that’s the issue. Maybe it’s not that you can’t compute it on your cellphone. Maybe you just don’t want to swallow that fire hose when you start up.” So, yeah, there are definitely alternate approaches to how you can do things. Yeah, it is a fun area.

Joe Netti:	And to add real quick, like you could even have approaches where there’s a Lightning app, and instead of finding the route yourself, you query some centralized server that has the whole map, and they find it and tell you what route to take. But then there’s privacy concerns with that, and you don’t really if they’re including their own nodes in your route to make more money and stuff like that.

Stephan Livera:	They could opportunistically try and route it through their own, their mates’ channels kind of thing?

Joe Netti:	Right.

Rusty Russell:	Yeah, yeah. Wow, that’s expensive. What a surprise again.

Stephan Livera:	So, Joe, I think you were also interested to talk about this idea of will Lightning routing inevitably become hub and spoke.

Joe Netti:	Right, yeah. I mean, it might already be slowly becoming hub and spoke, but I think that really depends on what we choose the routing protocol to be in the future, and yeah, it’s really dependent on where we move forward. I mean, we can see it already a little bit with where’s the money at. Well, it’s this hockey stick and also how many channels do… Here’s an example. This is another property that I found in the snapshot of the network. If you look at… How do I explain this?

Joe Netti:	Okay, so if you rank channels of a node from greatest capacity to least, you see pretty much a positive relationship between the capacity of that channel and the total capacity of all the channels of that node that that’s connected to. So, essentially what that means is that when people are… It says minus that channel’s capacity. So, basically, what this means is that when people are connecting to nodes with a lot of capacity. That’s all it means. They put more money into nodes that have more capacity, and that shows that people are doing this hub thing already. So, I don’t know. There’s a lot of question marks, but yeah.

Rusty Russell:	So, just think about it like if you try to connect to Bitrefill, which is one of the big… I mean, they’re a vendor like they were fairly, as a result, naturally, they’ve become this kind of hub. But on mainnet, they won’t even talk to you unless you’ve got like 0.16 Bitcoin. It’s like you need to actually open a big channel, otherwise they won’t even let you open one.

Rusty Russell:	So, they’ve actually explicitly said, “We only want big channels,” right? So that’s definitely accelerating that trend, but just as a user, you’re like, “Well, I don’t open a couple of channels.” Well, look, I’ll open up to Joe, but my main one is going to be a big one to LNBIG nodes, because they’re really well connected. They’re up all the time. Joe’s flaky. He likes to sleep and stuff like that. Turns his phone sometimes.

Joe Netti:	Yes I love to sleep.

Rusty Russell:	So this happens, right? So, people will naturally buy it towards that. Now, there’re a couple things that are fighting against that. We’re pushing back particularly with AMP, interestingly, so this idea that at the moment to send a big payment, you need to send it down a single channel. So payments are like these monolithic blobs, and this idea that we can split them into multiple parts and still have the properties that we want from payments. It’s really cool. There’s a couple of spec proposals that are right in the pipeline now.

Rusty Russell:	I am really hoping to get it into the 0.73. release at least as an experimental feature that you can break up payments into little parts. Now, at that point, big channels are nowhere near as useful as they are today. Today, you need a big channel because you want bigger payments. You want to make a $100 payment, you’re going to need a $100 channel. Two $50 channels are not going to cut it for you. With AMP, not a problem. You split it, right? So, it reduces some of that pressure to make really big channels with big players, and it allows the network to diversify a bit more, so that’s useful as well, I think.

Rusty Russell:	There’s also things like… Just naturally, we’re seeing growth of the network. So, LNBIG jumped on, so this was somebody who altruistically decided they basically wants to support infrastructure for the network because they’ve created this network of like, I don’t know, 60 nodes or something each with massive capacity that were basically all connected to each other, and you can connect into that, and you can route anywhere. They’ve been stable. They’ve been useful and everything else.

Rusty Russell:	But even so, the growth of the network has dwarfed them. While they’re still there, and they’re still important, we’re not safer when you take those nodes away. We’re still good, right? So, they haven’t become… Maybe they’ve been important in the growth of the network absolutely, and they’ve pushed things up a notch, but they are grown around, which is great to see. These two factors mean that, I think, I’m reasonably confident that we’re not going to end up hub-and-spoke-y more than the power law naturally would suggest, right?

Rusty Russell:	So, definitely, that property’s going to be there. There’s going to be some big ones, going to be some small ones, but I think we’re going to see the needle swing back a bit just because of the technical nature of stuff, things coming down the pipe.

Stephan Livera:	Fantastic. Let’s talk now about the results of the Million Channel Project. So, maybe, Joe, you can tell us a little bit about the final. What was the simulated size in terms of nodes and channels and so on.

Joe Netti:	First off, one of the big results is that we optimized c-lightning. I mean, Rusty did optimised c-lightning like crazy. If you look at the blog post, there’s a nice graph that shows… the before and after of some calls, API calls, and then shortest path, and Rusty optimized it crazy. Then also, I’m trying to pull up here the… Okay, yep, simulated size. So, we got close to a million channels. It’s like 998,000 channels, 94,000 nodes, and the gossip was 731 megabytes, and then the total Bitcoin, except this is scaled down. This is actually scaled down and regtest, but the total Bitcoin is 17,300, fake Bitcoin, of course. I wish I had that much. But yeah, that’s basically the end result of that.

Rusty Russell:	Yeah, it’s interesting. Less than 100,000 nodes making those million channels, out of which, 20,000 were just one channel, right? So that power law again. A fifth of the nodes only had one channel. But then there are the whales who made up for it.

Joe Netti:	Yeah, and that matches what we see right now, so that’s why it’s like that.

Stephan Livera:	Yeah, so in terms of making it work on the RasPi 3, what was required there?

Rusty Russell:	Other than going to buy myself a Raspberry Pi and hooking it up, which is always fun. The main thing is that it’s memory-constrained, right? So, it has two gigabytes, so you could give it some swap, but even so, right? Just keeping the whole million channels in memory was originally… Space wasn’t something that we’d really optimized for, and originally, we basically pulled that 731 megabytes, that whole store of all gossip we’ve ever received. We would just pull that all into memory and leave it there rather leave it on disk.

Rusty Russell:	So, immediately, what happened is my RasPi ran out of memory, and it crashed badly. So, there’re a couple things here. One is like, “Okay, well, you should give it some meaningful message when it runs out of memory. There should be something said rather than just dying randomly.” So, there are some fix-ups in that. But the other thing is even if you ask them to list all the channels, we have a good old tool that you can use to talk to c-lightning, and you go, “Okay, cool. Give me the channel list,” right? It was speaking back a million channels except it was two billion because it prints out… Each direction is like a separate half. So, it’s this massive fire hose.

Rusty Russell:	Then that tool would crash because it would try to load up. It would basically take a response, try to format it all for you, but it couldn’t even fit in memory, right? So, all these things are making it more graceful with handling these kind of things that we never hit in real life yet, but inevitably we will. A lot of it was just shrinking things down to fit inside the Raspberry Pi. We’ve done a lot of optimization already, but my laptop has eight gig of RAM. It had no problems. You shrink down to these little machines, and you go, “Okay, well, we’re going to have to actually squeeze things here as well.”

Rusty Russell:	So, there’s another round of optimization just to get it to run at all in that environment. So, yeah, a lot of cool stuff came out of that. We now keep the gossip on disk, and we just basically hand around, “Here’s where it is. You can go get it yourself.” We used to have this gossip daemon that took care of all the gossip. So, when someone connected in, and they want to know something, the little daemon would talk to them, would talk to the gossip daemon. It’d go cool this is what they want to know, and we shuffle this data back and forth.

Rusty Russell:	We went, “Well, actually, now, we’re putting it all on disk, let’s have the daemon just look at the disk itself, grab that the file and just start spreading it out,” and that’s actually a huge win itself both because now we don’t have all this memory. No one’s loading up and keeping it in memory, but also just the speed, the scalability that we can do with that is actually pretty nice. So, that work went in.

Rusty Russell:	While it makes it work on the Raspberry Pi, it lifted everything across the board, right? It makes it faster on my sample nodes and stuff like that. The other thing that c-lightning does really badly is that it’s really chatty. It used to be up until the latest release. Every time we connect to someone, it said, “Cool. Give us all the gossip. Tell us everything,” right? It works. You never miss anything, but basically you ask for this fire hose every time.

Rusty Russell:	So when your node restarts, and you’ve got 100 channels, tell me everything you know, and there would be a lot of stress at that point on this central daemon to digest all this stuff. God forbid, you’re talking another c-lightning node because it would also ask you, “Can you please tell me everything you know,” and we would then just feed it everything.

Rusty Russell:	So, in the last release we got a little bit smarter with that. Obviously, if we’re up to date within the last 24 hours, we go cool, just give us the last 24 hours, and we asked that from a handful of nodes like we’ll ask for eight, and beyond that we just don’t worry at all. We have come this high, medium, low. Actually, sorry. It’s three nodes. We asked for it. You give me everything in the last 24 hours. We go “cool”. You just gave me everything from now, and if we’ve got more than a week, the rest of it just don’t tell me any gossip. I’ve got enough gossip.

Rusty Russell:	If we detect something weird, we go, “Hold on. We didn’t know about that channel when we should have.” Then we go back and we pick someone randomly and we go cool, and you tell me everything, and we go back and grab the law, but that’s just way friendlier on the network as a whole. But I didn’t want to do that before I did the million channels optimization because the fact that we were so dumb about it stretched this stuff really nicely.

Rusty Russell:	I want to make it fast, make it work. We actually uncovered a bug in lnd’s implementation because my node was so slow because I run with a whole deal of extra debugging checks that when we ask them to connect the channel, we were also asking for all the gossip. We didn’t get their message, their reply through all the gossip that they were sending us until it was too late. It would time out on us. So, we uncovered a number of bugs with the way we handle gossip.

Rusty Russell:	So, yeah, there’s been a whole heap of work on this, and again, this is an ongoing thing. There will be more gossip optimizations coming in 0.7.3, so it does keep us ahead. Every so often, you go back to Million Channels Project and go, “Okay, so how are we performing today?” We don’t keep measuring this stuff. Inevitably, you put some things in. You didn’t realize how bad it is going to effect them in channel’s case. So, we tightened the screws once. You do have to go back and check every so often that you keep yourself honest.

Stephan Livera:	Excellent. Let’s talk a bit about ideas for future work. Maybe, Joe, did you want to touch on if there’s any ideas on what could be a good project or good ideas to look out for next time?

Joe Netti:	Yeah, so the Million Channels Project can always be expanded. For example, the properties of the Lightning Network, like the power law distribution, stuff like that. They weren’t really that important in optimizing c-lightning. They weren’t really that used that much, but they would be important if we are testing different routing protocols. So, there could be a way to use the Million Channels Project to compare different routing protocols and see which one fares better, and then it’s really important if we have an accurate topology and an accurate channel capacities. So, that’s interesting.

Rusty Russell:	Yeah, so I’m interested to see how well it tracks, like as we do get to a million channels, how accurate was this simulation? I mean, we obviously extrapolated, right?

Joe Netti:	Right, exactly. Yeah.

Rusty Russell:	There’ll probably be changes. It’ll be really interesting to see the real Million Channels Project, where like now, it really is a million channels. How close did we get, right?

Joe Netti:	Yeah, that’d be really cool too. This is cool too. I didn’t mention this, but I compared the actual Lightning Network in January to the actual Lightning Network in May, and it does the properties that I grabbed out of it still hold. They held in the data in January and the data in May. That’s pretty cool. So, maybe they’ll keep holding. I don’t know.

Stephan Livera:	Also, Joe, I think you were chatting before. You had a few thoughts around the micro and macro purposes of Bitcoin and economics. What were your thoughts there?

Joe Netti:	Yeah, I have a side hobby or passion of economics. You can see in the Million Channels Project, but I know that a lot of your listeners are Austrian based, so that’s why I wanted to talk about economics a little bit. I split economics into macro and micro like most economists do, but I define it a little bit differently, and I view the purpose of micro as guiding rational action towards some goal for individuals and for companies. So, for example, that’s game theory, like utility functions, stuff like that.

Joe Netti:	Then I view macro as predicting or forecasting the future changes in economic outcomes based on changes in policy and changes in technology, et cetera. So that includes econometrics. That includes, I would even say, a little bit of behavioral econ because you got to know how people are actually going to react to a certain policy in the real world of biases and stuff. This is a recent discovery, like basically, micro is for guiding individual action. Macro is for forecasting, and I think that’s pretty cool.

Stephan Livera:	Right, okay. Yeah, so I mean, for me, I think it’s… I guess comparing against an Austrian framework, it’s like we’re thinking more about the decisions that are made by individuals, and then in a macro sense it’s like what are the impacts that that has at this. If you’re considering what all these different individuals are doing, what’s the impact that that does to the broader world and the broader economy?

Joe Netti:	Exactly, right.

Stephan Livera:	But yeah, thanks for sharing that. Rusty, I’d be also interested just to discuss if you’ve got anything you wanted to share around what’s coming with c-lightning in the new version.

Rusty Russell:	Oh, yeah. So, always, always heaps of stuff. There’s inevitable bug fixes and optimizations and stuff. We’ve had a lot of excitement around plugins. So, the idea with c-lightning is basically we want to build this space. We want to build a really solid implementation that does all the things we expect from a node, particularly aiming at the server side, right? So that’s my background. It’s Blockstream’s interest.

Rusty Russell:	You want to set up a store that accepts Lightning. Okay, so this is the kind of infrastructure you want, but there’s a whole other really cool stuff we want to build on top, and we went, “Well, these ideas started coming out if you want to do it.” We’re like, “We really don’t want that in our code base. It’s kind of boutique to these people. It’s really cool. We’re not sure, people use it, we’d have to support it and everything else.”

Rusty Russell:	So, we ended coming with this plugin idea where basically people write plugins the same way they write plugins for web browsers and stuff to do ad blocking or turn the screen upside down and stuff. So, c-lightning has been really aggressive doing a lot of infrastructure work to grow that plugin infrastructure, so that plugins can do more and more invasive and interesting stuff. With each release, we see more capability built for plugins, and the plugins also lag a bit because someone actually has to then go and use them.

Rusty Russell:	We’ve got a database hook that went in the last release, which means that you can do live backups. So, if you want to do multi-site backups for your c-lightning node, which is important because obviously there’s real money involved if you want to… Backups are important. Don’t be like me. Back up your stuff. I have a test node that’s completely not backed up that I use for test payments. But in some of this robust scenario, you’re going to be doing backups. You want backups across multiple sites in real time and stuff like that.

Rusty Russell:	So, now, there’s that infrastructure that goes in, but there’s also some really cool infrastructure for expanding things and doing experimental things. The other thing that we’re seeing come through is we had this big spec meeting in Adelaide in November of last year, and we drew a roadmap of what’s going to be involved in 1.1, or maybe I might even call It 2.0, a Lightning spec. Everyone came in with all these ideas, and we fleshed out this rough map of stuff that definitely should be in 1.1.

Rusty Russell:	Now, we’re going through the phase of actually doing the hard work of writing it all down, specing it all out, writing test vectors, making sure everyone’s on the same page and all the details. A lot of bikeshedding, a lot of finagling the details, but that’s really started to come to a head now. A lot of stuff’s getting agreed. People got distracted. There’s so much stuff to work on outside this even just in the 1.0 spec. So, just recently in the last few meetings… We have a meeting every couple of weeks. We’ve had sort of the floodgates and a whole heap of stuff go in, so you’ll see excitement ramp up in implementations as well as they start to implement these features.

Rusty Russell:	I talked about AMP, for example, a multi-part payment idea. That is definitely something that I want to get back to. We’ve got a spec proposal out. We want to implement it. The rule is that you’ve got to have two implementations that can interoperate before it can go into the spec, finally, right? We approve it, like we had some good idea, but it’s pending testing, and it takes two people. Separate people have to implement it, make sure they work together, and then we can like go, “Cool,” and that’s saved us a number of times just because you’ve got to implement your wow.

Rusty Russell:	If we chose this way instead of that way, this would be so much easier. So, that’s the way things go forward, and we’re going to see that in the implementations in the next few months as we ramp up. We also have the Lightning Conference, so there’s this conference. It’s really a Lightning developer conference. So, previously, we’ve had these summits, which are about developing the Lightning spec, right? The protocol, and we get into deep in the weeds of actually how Lightning implementations work. So people who write Lightning implementations there.

Rusty Russell:	The Lightning Conference is more like people using Lightning. Developers one layer up are using Lightning to build their stuff and do cool things on top of that, and there’s a great community of Lightning makers out there. There have been meetups and everything, and we thought, “It’s time take it to the next level.” So, all the teams are basically going to be in Berlin at the Lightning Conference, thelightningconference.com. I’m really excited about that because that’s always fun, right?

Rusty Russell:	You meet a lot of people doing really interesting things with Lightning, but also all the devs are going to be there. It’s going to be like an ad-hoc spec meeting. We’re going to thrash out all this stuff. So, yeah, and Berlin’s always a fun city, so that’s coming up as well. Inevitably, that will change like it’ll be before and after that meeting. There’ll probably be some stuff come out of that that will completely change our priorities, right?

Rusty Russell:	People might say, “Wow. This is really important,” and be like, “We didn’t even think of that.” That happens always when we talk to users about their pain points and things. So, I’m really looking forward to that experience, and that’s definitely going to accelerate things. Just generally, this whole ecosystem is snowballing. So, on the one hand, it’s frustratingly slow. On the other hand, it’s day to day, and it is really exciting because stuff happens all the time.

Rusty Russell:	But when you think about it, we’re basically trying to build a whole new industry here, right? There’s no micropayment industry because there are no micropayments in the world. We don’t have the ability to send one cent around the world until Lightning, so we’ve built this thing, and it takes time for people to… Maybe there was someone out there who had this fantastic idea five years ago, but they couldn’t do it because they couldn’t send one cent. It didn’t make sense. They would skirt it, right?

Rusty Russell:	It takes time for those ideas to converge and to get those ideas and be like, “Hey, cool. We can actually do this now. We’ve got the capability. We’ve got this instantly settled, transferable, of value, of small amounts, really cheaply. What can we do with that now?” This industry will take… I mean, this is a long process to build a whole new industry around this, but it’s definitely happening, and that’s exciting to me, and that is definitely going to continue, and I expect we’ll see this kind of like… This slow, steady technical growth.

Rusty Russell:	But then at some point, it kicks up where it says there’s some ridiculous killer app. There’s probably something that Stephan and I will sit here and go, “That is the stupidest idea ever,” right? But it’ll be amazingly successful. They’ll be flying corporate jets and stuff.

Joe Netti:	hHshtag CryptoKitties.

Rusty Russell:	Yeah, right. It will be something that kids are into these days, and we’ll be sitting there going, “But that’s just the dumbest thing I’ve ever heard,” right? So, there’ll be something. There’ll be some killer app at some point, and in retrospect, it’ll be obvious. But from this point of view, it’s totally not, and I’m definitely looking forward to seeing that happening, but you can’t control the timeline on these things. You’ve got to have the infrastructure ready. You’ve got to have all the capability. You’ve got to have the experience.

Rusty Russell:	People are getting accustomed to how these things work and building all these examples and doing some real stuff on it, and that infrastructure is basically is required before you can have that amazing growth on top of it. So, we’re still in that early infrastructure days, and while it’s exciting for those inside of it, it hasn’t really got outside that bubble even though the bubble is growing. At some point, I expect it will explode on the world stage, and suddenly people will be like, “Wow,” and I’ll be like, “I’ve been working on this stuff for years now.”

Rusty Russell:	They’ll be like, “No. It’s only been like two weeks ago.” I’m, “No. Actually, we worked on this for a while.” So, that’s definitely something to look forward to if you look further, but making solid predictions about it is impossible.

Stephan Livera:	Yeah, look that’s great. I think that’s pretty much all I was going to touch on for this episode. So, thank you both for joining me, and look, before we let you go, let’s hear from both of you on where the listeners can find you and follow your work. So, Joe, let’s start with you. Where can the listeners find you?

Joe Netti:	Sure. I’m on Twitter with Joe Netti. J-O-E. N-E-T-T-I. Also, on GitHub, nettijoe96, and that’s it. That’s about it.

Stephan Livera:	Great. And Rusty, as for you?

Rusty Russell:	Yeah, so, rustyrussell on GitHub, and @rusty_twit on Twitter, but Google will find me as well. So, it’s pretty easy. Always like hearing from people too, so reach out.

Stephan Livera:	Fantastic, and I’ll obviously put the link to The Million Channel blog post as well in the show notes. So, look, Rusty and Joe, thank you both for joining me today.

Joe Netti:	Thank you for having me on.

Rusty Russell:	Thanks, Stephan.

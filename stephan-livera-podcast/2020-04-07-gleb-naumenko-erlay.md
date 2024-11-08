---
title: erlay Bitcoin transaction relay
transcript_by: Stephan Livera
speakers:
  - Gleb Naumenko
date: 2020-04-07
media: https://stephanlivera.com/download-episode/1909/164.mp3
---
podcast: https://stephanlivera.com/episode/164/

Stephan Livera:

Gleb Naumenko of Chaincode Labs joins me in this episode to talk about erlay.

Gleb. Welcome to the show, mate.

Gleb Naumenko:

Hey, nice to be here.

Stephan Livera:

So Gleb, let’s hear a bit about your story. I know you’re working at Chaincode labs, you’re working on erlay and a range of other things as well. Tell us a little bit about yourself and how you got into Bitcoin development.

Gleb Naumenko:

So I never had the real job. My first job, I got on my third year undergrad, started working on Bitcoin exchanges and wallets, stuff like that, in Ukraine for two years. And then I moved on to do masters in Canada and that’s where my supervisor was like, you’re interested in Bitcoin by just looking at my CV and like, do I want to do something related to that? And that’s how we started. And that’s erlay. Eventually became my master’s project.

Stephan Livera:

What was it that got you interested into this whole area,tThis whole topic of transaction relay?

Gleb Naumenko:

My supervisor wasn’t invited to this conference called Scaling Bitcoin in 2017 in Stanford. But she didn’t want to go and she suggested to me to go, I was very happy. It’s like a free trip. I’ll see all the developers. Yeah, I was a hungry student and yeah, going from Canada to Stanford was great. That was my first time visiting the States. So yeah, I agreed. And when I came it was like I had no idea about Bitcoin core development or the industry I thought. So there was this SegWit BCH to discussion. I thought SegWit2x is like SegWit, but better. So I thought why people don’t like to X. I don’t understand that. And I will say, I remember talking to Suhas about this at Stanford, but yeah, apart from that I was sort of inspired like it was, it looked so cool.

Gleb Naumenko:

I, before going there, I was afraid that Bitcoin core development is like very toxic. Nobody allows new ideas, nobody welcomes new contributors. But after going there, I was much happier and I wanted to become a contributor too. So when I came back, I started just searching for problems and looking at the software and the protocols, how it works. And it looked like a lot of people looked at at attacks on mining or optimizing mining people worked on the wallet. Segwit was obviously a big topic of development at that time, but transaction stuff was like the way peer-to-peer layer was not very well developed at the time. I guess Matt Corallo did a lot. He did compact blocks which relays blocks in the network much faster and that’s super important. But particularly inter transactions it was then something, nobody really looked much. So I decided to start there and find a problem, then try to come up with a solution. Yeah.

Stephan Livera:

Yeah. That’s an interesting approach. It’s that you were looking for other areas like where’s the blue ocean instead of the thing that everybody else is already looking at. So how did you go about learning more about transaction relay within Bitcoin and how did you come across that problem?

Gleb Naumenko:

I mean, honestly for me it feels like the most interest in part of the code, the way nodes talk to each other because it’s at the same time it’s very high level in a way that I can explain it to whoever, to my brother, to my mom. I can draw on paper arrows between nodes and at the same time, even though it’s very high level, it’s like right here and finding attacks on it is so cool. Like, okay, so what about a bad person does this and that and now the transaction is censored and just cannot be propagated in the network because somebody sent their own messages. So it’s not like 51% attack where somebody sends her a transaction by inaudible. A lot of hash rates. It just finding a vulnerability in the network protocol and explaining it. And that felt very cool. So for me, learning it was easy because I just like drawing how yeah, how things happened on paper and understand that that were high level. Then you look at the code and confirm your observations. Maybe write some tests. Yeah. So that was a natural fit to me in a way.

Stephan Livera:

Can you give us just a high level background? How do Bitcoin nodes work now from a transaction life cycle perspective? Can you just talk us through the basic steps there?

Gleb Naumenko:

Yeah. So imagine you’re the best Bitcoin user. So you have your hardware wallet and you have a node which you run at home because you’re a responsible user. So you sign a transaction on your hardware wallet and send it from your hardware wallet to the Bitcoin node running at home. You’re node will validate it. So it will look at the current blockchain. It knows about a check that you’re spending, the coins that exist, the signature is correct. And then it will send, it will announce the transaction by hash to all the peers that is connected to your home node usually connected to at least 10 peers, eight of which used for a transaction relay. So, which will announce a hash to eight peers. Just sent the hash of a transaction to them. Those guys will look in their local database and since they don’t find the transaction there. They will ask you for the full transaction. This is made for efficiency. So that’s so that we don’t send transaction body at once and don’t waste a lot of bandwidth. That was the first optimization done to this feature. I don’t know, more than five years ago, I think. So they will ask for transactions by hash and then you will send a whole transaction and at that point the same happens on their side. They validate, check all the rows they announced to their peers and that’s how transaction gets to miners and eventually appears in a block.

Stephan Livera:

Awesome. And so the Bitcoin network depends on connectivity between the nodes. And so what does that mean? Like why is that important for the Bitcoin network?

Gleb Naumenko:

Yeah. So as I said, when you started that node at home, you connect to 10 peers, one could think why not connect to one? The answer is if one node is bad, if they want to lie to you, they would be able to do this if your connection is exclusive. So, for example, they can double spend you, they can feed you the invalid blockchain, the fake Bitcoin blockchain, where they pretend to pay you. Let’s say you accept payments and sell something. So they pretend they paid you while on the real chain, which is much more difficult to construct and where real miners are. They didn’t. So that’s,effectively a double spend and they take care good and then they go away without paying you. So to prevent that, we connect to more than one. And the number eight was chosen randomly. I think when Satoshi wrote the code.

Stephan Livera:

I guess walking that through that example. So let’s say I was malicious and you only connected to me and I said, Oh, Hey, Gleb, I’ll, you know, pay me some what would it be? So basically it would be, I pay you some Bitcoin and you send me a good, right? Like you’re selling me a book, you know, whatever. And so in that example, I would basically send the transaction to you. Send you a block that looks like I’ve paid you. But in reality, you, because you don’t have enough connections to the outside world and you’re only connected through me, then that’s where the malicious aspect could come in. And where I would receive, you know, that whatever the physical good was from you or the service from you and get it for free because I could then, unbeknownst to you, but to the outside world, actually spend that away back to myself or just have never spent it to you on the real chain. Is that roughly what would happen there?

Gleb Naumenko:

So obviously the construction blocks is expensive. It takes a lot of hash rate. So you would have to so this is called an eclipse attack where you eclipse the victim’s view of the network by your malicious fake view. So you’ll start feeding the fake blockchain to the victim. So in order to make this practical, ideally you an attacker eclipses the victim from the very beginning because if they do from the very beginning, they can make the blockchain so that producing blocks is cheap. You mentioned just reversing back in time where blocks were created on Satoshi’s computer on a inaudible note, CPU or graphics card, whatever, what was used at that time and just feeding victim just that, like pretending that’s entire blockchain or creating a lot of cheap blocks on top of it without any ASICs or with one ASIC so that will make it an attack much easier.

Gleb Naumenko:

And then yeah, they feed you a block with transaction included in it so this is just one problem. There are other problems with this called eclipse attack. They can trivially censor transactions. So if you send transaction to the attacker, tried to submit your transaction, they can just drop it on the floor so it never confirmed the real network. So they can prevent you from transacting and obviously you can detect that quite fast. But there are some interesting attacks we will announce soon we found on lightning. And where in the lightning network, sometimes it’s, it’s critical to submit a transaction timely because there are this time locks and punishment period. So if you’re late, you’re screwed. And the attacker can steal your funds. So if they can send her your for an hour, that can go right to protect bad. That’s the second example of an attack. A third thing I may think of when somebody is eclipsed, it’s very trivial about the spy because if a victim is connected to you exclusively, you see all the messages come in from them. And if you can also the other nodes in the network, you can notice that some transactions are

Stephan Livera:

Yeah, sorry you might have cut out for a second there, but you were saying that if you were only connected to one person and then they were able to see all the messages that you’re sending, then?

Gleb Naumenko:

Yeah. So by, looking at the messages coming from the victim and by looking at the other public notes in the network, they can notice that some transactions are coming from, the victim first. So that would be the victims transactions. Obviously this is called first spy estimator technique and that becomes where retrieval when there is one connection to the attacker. So it’s very easy to map a transaction. So address from address A to address B, X amount of Bitcoin to map this information to the IP address of the node. The transaction is coming from, the victim’s node. So an attacker in this case can tell that, Oh these guy in New York at this address just just submitted a transaction saying mining is running from Iran or something or whatever.

Stephan Livera:

And how about now if we change that example just slightly, what if the user is attempting to use something like a VPN or they are using Tor, the onion router to try and mask their traffic? How does it change in that example where you’re still only connected to one node?

Gleb Naumenko:

All right, so it’s really different tradeoffs. So for example, in the case of VPN, or in the case of Tor, you’re really only protected from your internet provider. So your home ISP, they cannot finds you. But all this attacks I was talking about this, those are my favorite attacks because they are purely Bitcoin protocol layer. So they work, it’s not, it’s not part of the internet infrastructure, it’s just part of the Peer to peer layer. So you can think of that internet infrastructure is underlined, but peer to peer layer is on top and we’re attacking peer to peer layer, so this things doesn’t surely help against those. They help against infrastructure it does, against your government spys on you. So if you are in some Asian country and you’re using American VPN, unless they cooperate together, Asian country government cannot spy on you if you configure everything securely. So, these are real different things.

Stephan Livera:

Yup. Yeah. Just wanted to clarify that and make it clear that these are in some ways different things and so it’s different things to mitigate against other yeah, different components that might mitigate against different attacks, let’s say. And so I guess the underlying lesson or message there is that even if you are using some of these anonymization or pseudonymous techniques, like using a VPN or using Tor, it’s still important that you are connected to multiple different nodes such that you aren’t only doxing or only giving a transaction through one specific node because then they can start to infer things from you about who you are or what you’re transacting on the Bitcoin network. Right?

Gleb Naumenko:

Yes. So there is another interesting trade-off. This is like nobody really talks about this but connecting to too many nodes is also bad because you don’t want everybody in the network to hear from you either. So we should find this sweet spot. Like I would say from 8 to, I don’t know, maybe 30 nodes is something reasonable because like just to be clear, there are 10,000 reachable notes in the network. So 10,000 nodes which run publicly and can access, be accessible from any part of the world. You can connect to them. So out of that 10,000 we choose like at least 8. And I think that’s a reasonable bound because if you connect to everybody, all of them and everybody connects to all of them, you become susceptible to other things.

Stephan Livera:

Right. And as I understand, that’s also one of the, so there’s that concept of the spy node that tries to aggressively connect to every possible node and then using that to try to identify where on the network a transaction originated from based on the timings and where it first saw it. And then that was the thing that Dandelion was the idea of Dandelion was born to try and counter against that. Now, as I understand, Dandelion has some other tradeoffs that hasn’t quite made it into Bitcoin core yet. Could you just spell it out a little bit around that and the thinking on that?

Gleb Naumenko:

Yeah. So we were talking about eclipse attacks before where somebody owns your blockchain view or your connection effectively to the network. This is some other research area, which is basically, we can call it transaction origin inference attack. So to find out where a transaction is coming from, what’s the first node to have some transaction because then you can deanonymise people. So yes, you’re exactly right. The most obvious and the most easy approach is to connect to everybody for an attacker to connect to everybody and try to observe messages and try to infer the timing analysis. See where at what time the transaction, the messages are coming from first. That’s the most widely used and discussed approach. So the Dandelion was this research idea first and then it was actually proposed as a PR for Dandelion instead of for relaying a transaction to everybody as I explained, which is called flooding.

Gleb Naumenko:

Because you send to everybody, you know, you have 8 connections you send to all of them in Dandelion first you send to just 1 random node out of 8 and that random node sends to one node again, so that there is this, on average 10 hops. They call it a stem phase, like in a Dandelion, that kind of flower, 10 hops stem. And after that those 10 hops at the 10th node, it starts to flood. That’s why using the same technique, it will probably look like that 10th node is the source of the transaction, which is obviously wrong. So that’s how at the high level it is supposed to work. The problem with Dandelion is that there’s this trade off so far. The problem is we can either make it less effective so that an attacker can find an easy way to highjack it to prevent it from working to deanonymise stuff.

Gleb Naumenko:

Dandelion is used for, or it will require too many resources a node will consume. So I know it will have to spend much more extra RAM memory and maybe bandwidth to so because Dandelion is not like, it’s not even the perfect solution. It’s only an attempt. It’s called like a heuristic and attempt to make something more private without really a good proven guarantees. This tradeoff was never in favor of Dandelion. So we are still open to try to make it possible. But so far we spent, like Bitcoin core developers spent a bit of time trying to make it happen and this shaved off becomes more and more clear and challenging. So that’s we are now looking at probably other solutions to this problem.

Stephan Livera:

And so bringing it back then too erlay and transaction relay just in general. So the Bitcoin network has this INV message flooding and that could be explained as being high fault tolerance, but poor bandwidth efficiency. So what is fault tolerance?

Gleb Naumenko:

Yeah. INV it stands for inventory. And so this hash announcement to explain, do you see a transaction? You first announced it by a hash to your peers. It is a high fault tolerant. Because you announce it to all peers, you know, so it’s like the best efforts you don’t trust a single peer when you’re relaying your transaction you send to everybody. So that’s why it’s high full tolerance at the same time because everybody receives it. Probably they’re not like and they do the same. Everybody receives it 8 times if you think, because they have eight peers and you send to them and imagine the first peer sends to some far peer in South America and South American peer sends to the second peer he already sent to so that that guy at that point receives it second time, like the same hash which is not necessary and that’s why it is high fault tolerant but it spends a lot of bandwidth. Everybody receives everything eight times.

Stephan Livera:

Yup. And so it just becomes a very costly from a network perspective. Would that be fair to say as the network grows? Right.

Gleb Naumenko:

So there are two aspects to this. First, every node spends, a bit like the, the most conservative full node which relays transactions spends 30 gig of bandwidth a month, which I guess alrigth for Western countries, but if you’re on mobile internet or if you’re in developing markets or elsewhere, it’s going to be problematic. So of the 30 gigabytes, half of them is just this hash announcements. 90% of each is a duplicate. So I got the hash part of this transaction. And that will get it from my other peer too, for the second time. So all those duplicates consider effectively almost half of their bandwidth it spends. Ideally we can get rid of them.

Stephan Livera:

I see. And then, so I guess this is where erlay comes in. What are some of the, you know, can you just give us a high level, what is erlay what are some of the benefits of it?

Gleb Naumenko:

Yeah, so erlay is a way to relay transactions without sending those hashes to everybody. Instead of this, you’ve got a transaction, you will forward it to only subset of your peers, not to eight or not to all of them because you also have inbound peers. Maybe if you’re running a reachable node, you have eight outbound, eight to 10 depends on which pass you around. And you have inbound peers. So you will send only to outbound. And with inbound you will not send it to them by hash, but you will do very efficient mathematic and coding thing to exchange your transactions with them. So it’s much more efficient. You’re not announcing everything by hash right way, you’re constructing this we call it sketch of all that you have and send it to them and they will try to look at that sketch and tried to see what exactly their local view is missing and the requests on what’s needed.

Gleb Naumenko:

That’s, affected how erlay it works. And two main achievements is that you remember that 30 gig of bandwidth a month with erlay it will be only 18 instead of third year. This first achievement, the second one is before erlay. Since you’re relaying your announcements through all connections you have it poorly scales with the original protocol portal, the scales with connectivity. So if I want to increase connections from eight to 16 you’ll spend twice as much as bandwidth. And meaning that instead of a 30 gig of bandwidth a month, you will spend 45 because it used to be 15 for INVs and 15 for everything else. And now it’s 30 for INVs, 15 for everything else, 45 in total. With erlay the cost, if you increase connections from 8 to 16 will remain almost the same. So instead of 18 you will spend 19 gig a month, which is super cool. And we have one to increase connectivity as a, as we explained in the beginning, connectivity gives you a high fault tolerance, meaning more security to rely less on the those eight connections you have. Cause if you have 16 now maybe 15 can be bad, but if the 16th is good, you’re fine.

Stephan Livera:

Gotcha. And then in terms of the costs, as I understand, it will slow down the propagation speed of a transaction. So can you just outline a little bit around what that cost would be?

Gleb Naumenko:

Yeah. So once you send your transaction from your mobile wallet to your local node, it will take right now almost a bit less than four seconds to send it to every node in the network. So in four seconds, every node will know about your transaction as long as it is valid and yeah.

Stephan Livera:

And so how would that change in the erlay model?

Gleb Naumenko:

Yeah. So four seconds is primarily, it’s not because the internet is slow if because of the internet, the speed is just like less than a second. But we add some artificial delay to make it, to make to add randomness to the process of relay. And so that the observations the spy is making it’s worse. There is some noise. So let’s say you’re node got a transaction and instead of relaying it right away at some random time, within two seconds before relaying it forward so that that’s where four seconds is coming from. It’s not, it’s not just internet, it’s also our Bitcoin layer on purpose delayed, for protection, for privacy protection. And with erlay it will take instead of four seconds, it will take almost six according to the experiments I made and according to different measurements I took and what it really means in the broader context, we believe this is totally fine because usually what matters for a payment receiver or whoever we will be looking for a transaction is through there. They will probably want at least one confirmation in the blockchain and one block takes 10 minutes. So that two seconds difference in the context of 10 minutes is not a big deal. We believe that’s why this is why we accepted this latency increase. It’s possible to make erlay four seconds or even less, but it’s probably going to be as efficient. It will cost a little more bandwidth. So we took this trade off.

Stephan Livera:

Yup. I see. And just for clarity for listeners, it’s, I guess it’s when you’ve broadcast the transaction, but it is not yet confirmed. It’s, sitting there in the mempool and so on. What you’re talking about here, Gleb is saying that that transaction you wouldn’t, you might not see it in your mempool for the six seconds. That’s how to understand it, right? Yes. So can you just tell us a little bit about some of the new messages and what’s needed to make this work? Right. So in the past it was INV and then getTX. And now you’re introducing a few more messages into the protocol and that’s how this reconciliation protocol works, right?

Gleb Naumenko:

Yeah. So reconciliation is this process of efficient comparing sets. It’s really just two different sets of numbers. And we think instead of just numbers, we use this, we use transaction hash transaction ID’s, which stand for it’s transaction hash but shortened. We made it short because that’s first that’s an easy way to save a bit bandwidth right away just because transaction hashes are too long for no real reason. In this case they can be shorter because the attack is not that, it’s still difficult to fake them. And second, this reconciliation process is efficient set comparison is just very intensive math so it better operates over small numbers. So let’s first give a, I think it’s more interesting to try to explain what happens under the hood. Let’s say you have 10 transactions and I have 10 transactions and nine of them are same, but you have one new transaction and I have one new transaction and they are different.

Gleb Naumenko:

So let’s say the ID of your new transaction is 11, and the ID of my new transaction is 12. What’s the how many numbers like that. Like let’s say of the order of 100, we should send to help each other to find the missing transactions. And the obvious approach to this is, you send me all your numbers. So all of your ID’s, like 1,2,3,4, up to 11. I look at them, I remove what I already know. And they send you back the one you’re missing, but the cost of that would be what, transmitting 12 messages, right? So you send me all yours. Well, I have one or something and I send you one back with this efficient reconciliation math, which is based on ironically something called BCH codes. Yeah it’s the library minisketch we wrote with Pieter and Greg to make this math work with this math, we can exchange this missing transactions, sending just two numbers and that’s super like you’re almost theoretically not possible to do better.

Gleb Naumenko:

Then just sending two numbers. It’s almost, imagine you got lucky, so I found out randomly out of my 10 transaction, which one you’re missing and send it to you and you send to me, what you found you’re lucky to find. And, but there is math we found which makes this possible without guessing, with almost 100% chance of success. So all the protocol messages, or the new protocol messages introduced are basically to facilitate exchanging of those. So we use sketches for that. So you take your list of transactions or transaction IDs and do your compute a sketch of them. So your computer’s shortened representation of them, like very compressed and just basically we’re sending those sketches back and forth is what I introduced. There are I think five new messages in the peer to peer layer. So it’s quite a lot we had probably 20 before and after this there will be 25 but, but I think it’s not a big deal because, because this like just it’s not really limited.

Stephan Livera:

Yup. And in terms of changes to the Bitcoin to Bitcoin core, this would not be considered a consensus change. Right. So it’s not that it needs like some big soft fork and so on. Right. It’s something that can be implemented without like that level of a kind of community adoption or whatever. Can you tell us a little bit about that process though in terms of what stage in proposal is at and so on and other feedback and so on?

Gleb Naumenko:

Yeah. Yes it doesn’t need any hard forks or soft forks. I am running in it right now with my nodes. So I have ten nine like from like avant-garde nodes which talk to external world but support erlay but don’t do erlay with external world. And I have one node which purely talks just erlay to those 10 so, and I’m just looking at how efficient in terms of bandwidth is that finance, I’m just confirming all the measurements I had before with that. So it works today. It will get better. It scales better with the adoption. So the more reachable nodes run it, the better it is for everyone. More efficient, but you will see improvements if at least one of your peers are running erlay. It’s already going to be better than, than before. Yeah, in terms of the process. I mean I think I did my best to make it happen.

Gleb Naumenko:

I gave a lot of talks on it. I wrote a lot of analysis. I published code a month ago. We got some initial attention, but right now there is some slow down maybe because of Corona Virus maybe because my code is based on some changes which are not yet adopted. So Suhas a suggested to use. It’s very technical thing suggested to use WTXID. So witness transaction ID’s, which include the witness thing where you compute the transaction ID, which should have happened right after SegWit but nobody really bothered. So my changes right now are based on those. Just when you’re announcing a transaction, you’re not announcing by plain ID but announce the ID, which includes the witness. And I hope that once that is merged, which seems to be very soon, like I hope it gets merged in April. Then after that, I hope there will more attention to the code review or I’ll just start nudging people and, yeah.

Stephan Livera:

Yeah. I think from a recent Socratic seminar, I think there was a pull request by Suhas in relation to the witness TX ID. Would you mind just explaining a little bit around so, you know, most of us in the Bitcoin world we’re used to searching a TX ID, a transaction ID. Could you just spell out what the differences are between say the transaction ID and the witness transaction ID and then what you’re talking about for erlay, which is a short transaction ID?

Gleb Naumenko:

Oh yeah. Witness transaction ID is not really very different, it’s just, so transaction ID is always hash you cantake all the content of your transaction. Like, source, destination amounts? Well, it’s in very simplistic terms, but yeah, and you hash them and hash is really compression. So it takes some data and you make a much smaller data out of it. And that’s small enough to use it as an identifier. The one you can read, you can compare. And we used to I’m not even sure what blockchain explorers are currently using. They’re probably using WTX they use for post SegWit transactions because those are not malleable or, Yeah, there are, I guess they’re using WTX IDs and, but this is specifically a PR related to peers to peer how nodes talk to each other. People don’t care about that.

Gleb Naumenko:

You can only see it if you look at your logs. So yes. So that’s, the difference between the two and in erlay we just take well in the, because we decided to base it on, Suha’s PR to compute a short ID, we just take the WTX ID and cut it, well actually not, it’s not that simple. We, yeah, we make it a little shorter and then we use some salting and technique. Salt is where you add something to the initial data to make hash different for every connection so that if somebody can grind two transactions, to different transactions, which map to the same short ID, they cannot attack the system. This is called the collision. When somebody can map, can find data which commits to the same hash. So to prevent that, the common technique is salt, to add some, static data to the initial one. So that’s an attacker. It’s very difficult to grant them a forever connection cause every connection will have different inaudible. So yeah, it’s again, it’s where technical erlay, just just make this little thing again, the goal was to cut some bandwidth basically for free because it’s easy just to make transaction identifiers used, smaller and to allow efficient math to work faster.

Stephan Livera:

Cool. And so the hope then is that once that WTXID PR is merged into Bitcoin core, then you’re hoping for some additional review and getting erlay merged into Bitcoin core and then it would just be in future version of Bitcoin core. Could you just also spell out how it would work between the nodes that don’t support erlay yet? Would it just be some kind of version signaling and saying, Oh no, I can’t speak erlay. You need to speak the old language with me?

Gleb Naumenko:

Well, yeah erlay node will simply the first thing it will send it, will see that it will try to establish a erlay reconciliation protocol, like it will just send, I want to talk to you in erlay and if the node doesn’t respond. Then the new node will fall back to the existing protocol. That’s how we do. That’s how we will do WTXID. It’s like, then, you know, they’ll ask the counterparty, can you talk WTXID for relay. And if they never respond, it will use the old ones and the same we do for compact blocks. It’s a very efficient protocol to relay blocks across the network. It’s the same thing. It’s how we negotiate features. Yeah.

Stephan Livera:

Awesome. And yeah, so listeners, if you haven’t already, I recommend checking out the episode, Matt Corallo on the Chaincode podcast where he spoke about that in a bit more detail around how compact blocks and FIBRE and so on. Some of these things work. So that’s good info there. So look, I guess that’s kind of the erlay stuff. So let’s talk a bit more broadly around Bitcoin. Do you have any other things that you see that you would like to see improvement on in terms of Bitcoin core code base? Or are there, there any other things that you’re thinking about in terms of like security or performance?

Gleb Naumenko:

Yes, there are several topics I’ve been trying to push forward slowly for a bit, but I think it just takes like there should be a leader. These features, it’s often like there shouldn’t be, yeah. Somebody who just talks about this over and over again and I’m yet to, I want to get done with erlay and then just start with a new big feature in the, in the meantime, I’m just focusing on small things. I have a PR to, to make address relay better. So IP address, every node, every day, every node will announce their own IP address to the network so that we know about each other so that if the connection is dropped, we can connect to somebody else. So that’s a little broken right now because of the relay to addresses to the nodes, which will never really forward namely SPV clients because SPV clients are limited.

Gleb Naumenko:

They won’t obviously relay, they don’t care about your address, IP address, but will still send to them. And because of that, it’s how it’s a bit broken because it’s really slower than expected. Across the network. I’m looking at how to make like network privacy a bit better. How to protect privacy leak in terms of when a new node starts, how to talk less to the DNS server, which helps you to find out about the new nodes every time you started a new fresh node, you first learn your peers from the DNS seed. And I recently submit suggest that they change how to talk to them less so that’s part of internet, doesn’t learn about new nodes that easily. The topics I’m gonna be looking at probably may be with a denial of service protection.

Gleb Naumenko:

So right now, there are ways to just exhaust all the resources of a victim node. If you’re running an if you’re running like on a reachable IP address I can probably just make your node much work much more slowly remotely or just like exhaust your CPU or Ram. So I’m going to start looking into that at and suggest some fundamental change to make it better. There are good protections right now, but some of them are just not really effective. And there shouldn’t be a big solution to that. So basically to protect nodes from being exhausted by, by malicious actors.

Stephan Livera:

Right. And I’ve heard historically, and maybe this is still true, that it’s possible to craft these like malicious blocks and so on that will basically chew up the resources of the node that receives it.

Gleb Naumenko:

Yeah. Yeah. There was a really great discussion a month or two ago on, on different Socratic seminars. And there was a suggestion from a Bcoin guys from purse.io implementation of Bitcoin is JavaScript. They really ran through this problem with constructing fake blocks. And yeah, so there’s developments in that side, but there is like, there is like a really fundamental way how to solve the, the issue with denial of services. I want to try to make it happen and see how difficult it is.

Stephan Livera:

And looking more now at the application level of, you know, Bitcoin applications, things like wallets and so on. Are there any things that you see there that, you know, what’s your sense there? Are there things that, what’s most needed?

Gleb Naumenko:

I’m just gettingexcited, I opened my first PR to rust-lightning just an hour ago. It’s work in progress, but I’m like, I just started writing tests to understand the codebase. So at Chaincode labs since summer, it was me and Antoine Riard. And we tried to combine my knowledge of Bitcoin, peer to peer and his knowledge of lightning stuff together. And we found, mostly him, he finds some attack and I’m trying to look deep into it, to look how much does it cost to actually execute it to think about like how to deviate, how to protect from it. He also takes part in that too. So I’m just now slowly migrating into lightning it seems. To lightning protocol development to Lightning infrastructure stuff. We’ll see how that works out at the end.

Gleb Naumenko:

But, that’s it seems like that’s where I’m moving. I hope the issues with Bitcoin will be over soon. I really hope. And in two years I will resolve all my to do list about Bitcoin vulnerabilities on the peer to peer layer they’re not that big, but there are still like privacy leaks here and there. Small things, especially with the address relay with the IP because you can track how those messages propagated to the network and then see who’s connected to who. I think and yeah, and I hope I’ll be able to slowly move to lightning to like protocol and infrastructure stuff to some ideas on top of Bitcoin. So there are like for example, cool stuff I’m interested in is how to, so let’s say I have a messenger, but I don’t want to verify everybody by SIM cards and I want to protect from bots.

Gleb Naumenko:

I don’t want people to use to abuse my messenger. So instead I can ask people to prove that they had Bitcoin sometimes before 2017 let’s say, but in a private way. So not just to commit to a particular, UTXO and say, this is my UTXO I can prove it to you, cause that’s not private. That’s not good and people won’t use it. But if I can find a way to make this private with some zero knowledge proofs, I think this is super cool. And a messenger is just really, and it’s a broader topic of sybil defense. So how do I prevent somebody from having multiple identities and abusing it? And that can be useful in various ways. You can build, a separate, peer to peer network for Bitcoin where you can allow people only who can prove some ownership, you can solve some issues with coinjoins where it’s very cheap to sybil attack coinjoin.

Gleb Naumenko:

It’s very cheap to pretend that you’re an honest participant of a coinjoin while you’re a spy and just overwhelm all the coinjoins with spy addresses so that you can infer all the honest people who tried to get anonymised. So that’s, yeah, that stuff. I’m interested and then I hope I’ll, I’ll have to learn some cryptography. I’ve been putting that aside for a while and yeah, I’m excited about that too. With applications, like applications applications, it’s, it’s like I think we are in very early days. I’m glad that some businesses that are exploring all this stuff, what really makes sense to me is I think video games on lightning is super cool. I think they choirs where you can like do shooter, where you shoot somebody and then you collect Satoshi from them cause you shoot them. I think that’s going to be a big deal.

Gleb Naumenko:

I don’t know.

Stephan Livera:

Like lightnite.

Gleb Naumenko:

Like yeah I would, I would be so happy to play that if I was like, I don’t know, 15 or something. And it’s like, yeah it’s so true though and it’s going to be not decentralized or whatever. It’s just much more fun. Like I don’t know even just simple gambling like poker or whatever, just over lightning I think. I think that’s a super cool niche. So I’m looking forward to those cause that was and other application layer is definitely exchanges without KYC. So like Hodlhodl or bisq in the states, I’m in New York right now and I have hard times buying Bitcoin. I don’t want IRS or whatever to like, I don’t want to have any evidence that I touched Bitcoin at all. And, and there is like, no good way to really purchase bitcoin without KYC right now. And I hope there will be creative solutions like using some gifts cards like like this prepaid debit cards. I think, yeah, that’s something I’m looking forward to.

Stephan Livera:

Yeah. So as I understand there are, I guess there’s different things here. There’s things like purse and so on that I think you can do something like that where you put up gift cards and people can pay Bitcoin to, you know, use the gift cards and things like that. And then bisq and hodlhodl and things like that where obviously you can do cash trades and so on. Obviously you still have to meet someone in person. That person has to, you know, obviously see you and that can be a bit more challenging. And then also they offer some of those platforms offer as well, like bank transfer means. But even then the challenges dealing with, you know, scamming people. And so on. And again, there are counter measures against these things. But again, nothing’s perfect. I guess

Gleb Naumenko:

The worst thing for like if you talk about bank transfers, I’m just, you don’t know who’s on the other side, what if it’s some terrorist and you’re sending your like transfer to them and now your bank account is banned forever, they actually would freeze your existing funds. Like no matter how much you send, they freeze entire account, best-case, worst case they put you in jail cause they transacted with some terrorists. So, that’s really what, what worries me most in this tense.

Stephan Livera:

Right? Yeah. And I guess it’s, it’s just not an easy problem to solve, but I guess people can do like say have a bank account open that is only for, you know, Bitcoin trades and use that only to kind of segregate away from the rest of their financial transactions with their normal bank. Maybe that’s one way. Although imperfect, obviously.

Gleb Naumenko:

Yeah assuming first they don’t put you in jail. And second, the taxation agency cannot access your bank transactions. Cause that’s also like not that difficult to trace. It’s probably easier to trace than Bitcoin and yeah, just by looking at Towson home and I didn’t know.

Stephan Livera:

Yeah, of course, of course. I mean you basically have to assume that those, any federal government agency or taxation agency who asks for it, will get it basically. So that you just have to basically assume that but it’s not an easy, it’s not an easy thing. So what about when you were talking about the coinjoin stuff and proving that you own a bitcoins and so on, is that also, is there any relevance there with you know, join markets PoDLE proof of I think it’s proof of discrete log equivalence.

Gleb Naumenko:

Yeah. Yeah, not quite, I think PoDLE works well, first of all, it’s much more practical. It doesn’t require fancy cryptography. It’s a super neat trick. Like, it’s really cool, but it’s nothing. It’s like for this stuff I’m talking about, you really need like zero knowledge proofs. It’s funny, I remember this, this was my impression from learning poodle. Unfortunately I don’t remember the data. It was a proposal to compare like the actual properties. I can only compare, I cannot really recall my conclusion. I think with the poodle really works are very specific, quite enjoy and like,

Stephan Livera:

Right. Yeah. And as I understand some of the lightning devs are also looking at that as well for things like dual funded, channel opening and things like that.

Gleb Naumenko:

Yeah. That’s super cool. Yeah. I hope, I’m really hoping to find ways to participate in lightning more and more because it seems to get more stable so that it’s possible to contribute and yet a lot of unexplored stuff and yeah, just a good time to be there too.

Stephan Livera:

So from a lightning perspective, what are some of your favorite applications or lightning wallets? I presume you’re using, you’ve, you’ve tried out a bunch of the lightning wallets?

Gleb Naumenko:

So actually I’m just starting with lightning. It’s sort of, it was similar with Bitcoin. I think I started to work on Bitcoin before I got excited about the money and the censorship resistance part. I started because it looks like cool research problems. Like just something interesting to contribute to, good community and a lot to learn about in terms of technology and new ideas you can apply it’s the same with lightning. I’m learning protocol first and then I will converge to wallets and stuff. I got my first lightning coins a month ago or no, I think it’s more like 4 months. So did you know this Keybase messenger and they had the stellar airdrop and I just converted that to lightning immediately when I got it, that was my first lightning and there was, I don’t remember the name of the service, but it’s somebody in New York that built it and yeah, I used it. I used Wallet of Satoshi on iPhone. I think it’s custodial but, but yeah, whatever. I just wanted my free airdrop lightning. So yeah. So I’m sticking to that right now as I said, I’ll go learn more protocol first and then I’ll switch to better tools I guess.

Stephan Livera:

Yeah. And as you mentioned you’re mostly looking at Rust-lightning right now. Yeah.

Gleb Naumenko:

That’s my application. Well it’s interesting when I was mentioning attacks with Antoine so to research those to see how easy it is to use those. We actually were looking at like LND and neutrino clients and ACINQ, scala thing , just because those are the most popular right now. So if you wanted to justify some attack and some counter measures, we want to look at those. So I’m quite familiar with those codebases too. But as a contributor I’m started looking at rust-lightning and yeah, I just, I learned a bit of rust last month and yeah, just trying to apply my knowledge and learn more on rust-lightning.

Stephan Livera:

And so previously have you mostly been doing like Python and C++?

Gleb Naumenko:

Right? Yeah, exactly. Because I was more like researching. So do experiments in python just try to simulate the networks. Our network is 60,000 nodes and you cannot have a real like copy of that. So you might get like much simpler python representation of them and they talk to each other and then you measure stuff and just statistics too. And then once I need to make a change to Bitcoin for I do C++. Yeah. But I did everything I did. Like I didn’t do like crazy functional languages. I didn’t do Haskell, but I was, I was programming since I was like 12, I think. So it’s been more than 10 years now and I did a lot of not so good, but, enough to get familiar with them.

Stephan Livera:

All right, well look, I guess if you’ve got any call outs that you wanted our listeners to consider, or if there’s anyone, if there’s any particular review or support that you want to shout out for, maybe now’s the time.

Gleb Naumenko:

Yeah. Okay. I just, I just wanted to tell our listeners that right now it’s really a good time to start looking into Bitcoin closer from whatever aspect of it makes you curious, but on my example, I just started contributing so randomly and it was very smooth. I’m not a perfect programmer. I never was into Google and I didn’t know. I think it’s so good time to start looking at it. Even if you have a full time job on the weekends, even if you don’t code, I think you can contribute. Amiti wrote recently a really good article on how to start contributing to Bitcoin core. There are all this other projects you can learn the code right away. I’m sure like if you have some kind of technical education that is doable. Even if you’re not having technical education you can do it. I have friends who started to contributing and at least looking into open source code and reviewing code without any prior knowledge and yeah, I hope more people are joining us in building these cool things

Stephan Livera:

So glad. If listeners want to follow you online or you know, see what you’re saying. Where can they follow you?

Gleb Naumenko:

Well, my Twitter handle is @tomatodread and yeah, I guess that’s it. My DM’s are open. I’m always open for research, collaborations, ideas, how to make Bitcoin core, or other projects better. I’m open to yeah, all sorts of working together. Like I’m super positive about different experiences and just I am, and I want to help everybody to get up to speed, to join and to contribute.

Stephan Livera:

Well, thanks for joining me, Gleb.

Gleb Naumenko:

Thank you. That was great!

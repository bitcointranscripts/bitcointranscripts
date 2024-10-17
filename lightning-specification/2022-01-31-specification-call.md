---
title: Lightning Specification Meeting - Agenda 0955
transcript_by: Michael Folkson
tags:
  - lightning
date: 2022-01-31
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/955>

# Bitcoin Core funding a transaction without looking at ancestors

I have something that I wanted to ask of our implementers who implemented a wallet. It is tangentially related to Lightning especially for anchor outputs. I realized recently that when you ask Bitcoin Core to fund a transaction at a given fee rate it is not going to look at the ancestors and it is not going to take the ancestor’s fee rate into account. If it adds ancestors that are unconfirmed the actual fee rate that you get is usually much lower than you’d expect if your ancestors have low fee rates. If you implemented this for anchor outputs, for anchor outputs once you start spending a lot of unconfirmed inputs to a bunch of transactions you are going to have trees of unconfirmed transactions. If you really want to get the fee rate for the whole package to get your transactions integrated, have you implemented something to look at the ancestors? How do you decide on how to set the fee rate?

No. We’ve just set the fee rate based on the fee rate for that transaction. You mean children that will increase its package fee rate or its ancestors?

Ancestors. If your ancestors have a low fee rate and you are trying to set a high fee rate the fee rate as evaluated by the miners will be much lower than what you think. You don’t understand why your transaction is not being confirmed.

That’s true. Your feedback loop is still the same, increase the fee rate.

You may even want to not spend that specific unconfirmed output because it is a long chain of other ancestors that have a low fee rate. You may want to use another one.

I don’t think we’ll end up with long chains because we won’t use unconfirmed outputs by default anyway unless they overwrite it. To a certain extent.

Then your UTXOs can easily be exhausted if you have to bump many HTLCs and you bump them independently instead of batching them together. That is something that concerns me.

You should batch them together.

Your HTLCs?

If you are bumping.

You can only do that if the timeouts of the HTLCs match.

I guess to some extent.

You can batch them but you might have to pull them apart again.

My feedback on merging the HTLCs is more that every time one of them is spent by your peer then you have to re-batch the whole thing with the remaining HTLCs. Against a malicious attacker I am not sure it works better than just doing a big tree of unconfirmed.

You mean rolling HTLCs into some CTV type thing?

If you are trying to fund a transaction and you are picking unconfirmed ancestors and those ancestors have a lower fee rate than what you are trying to set on the children… In lnd for example, are you using the ancestor graph to estimate the right fee rate that it should set so that the whole ancestor set has the fee rate that you want? Or are you just considering this transaction in isolation?

We have a `bumpfee` command, a CPFP. That command assumes the caller has done the ancestor graph traversal. But then we have some internal stuff. For example when we are doing breaches we then compute the full ancestor graph internally. This is in relation to anchor stuff?

Yeah exactly. Bitcoin Core does not work the ancestor graph. I cannot do it myself because I don’t know what inputs it is going to add.

Raw sending, gotcha. We have our own wallet which means that certain things are opaque but it lets us to do things like this more easily because we know exactly… I think we have a to do to make one of the fee bumping calls a little bit easier to use. Right now it requires the caller to say “This should be the actual effective fee rate” and therefore should be higher than whatever they input there.

# Clarify the sighash types for HTLC Success and Timeout transactions

<https://github.com/lightning/bolts/pull/954>

It read as being optional but you must use it? Only one party needs to use it. The other party can just do SIGHASH_ALL.

The PR is just pointing to something that we already have specified somewhere.

The PR is just pointing out that you have to, not that you can.

It was clear elsewhere but it wasn’t clear reading this part of the spec that it was required.

Almost a typo fix. Or a clarification fix.

# Making gossip private using ZKPs

<https://github.com/lightning/bolts/issues/955#issuecomment-1026027048>

Great investigation by Arik on this. This is maybe super heavy weight. Are we ready to go into SNARK land? As an engineer it is cool but do we want to do nothing but SNARKs?

Arik’s last comment is the killer. We spoke to a tonne of people, looked at a bunch of stuff and there is nothing that has a mature implementation that we can take and use.

I think Bastien’s point is also very true. There is so much research being done right now that it is still changing at a very fast pace. Maybe something will come up eventually where the STARK land and PLONK land which are the ones that don’t require trusted setups will have somewhat more acceptable proof sizes and verification times. However even though I think the math behind all this is so fascinating and I would love to understand it better I also think that it is somewhat opaque. One of the beautiful aspects of Bitcoin is that it is extremely easy to understand.

Worst case it is a denial of service issue. Especially with trusted setup. Worst case it is a denial of service issue against you by all of the implementation developers who are conspiring to denial of service attack you. They all write the code and are conspiring. We could probably do worse if we all wanted to conspire together and screw users over.

I will note that with the verification times you don’t want the actual anti DOS measure to be effectively a DOS.

That’s a good point. Laolu also pointed to the log scaling ring signatures which I was asking some folks about. No one is even trying to work on implementing that. Unless we all wanted to each hire somebody and have them work full time on this for a year or two, that doesn’t seem realistic.

Even something like STARKs still requires pretty large machines to do the proving stuff. We could run but it is still faraway. Things are still evolving pretty rapidly. Every single month a new paper or a new modification comes out, they are still chasing each other.

Was there some research on attacking all those schemes?

There’s a tonne of those. I think the problem is more that they are so busy working on coming up with a clever proof system that they don’t actually ever spend the time to implement and productionize the previous proof system.

And the benchmarks are usually micro benchmarks which means Python linter extrapolation or something.

They are too busy coming up with new proof systems. The proof may be right but they can’t productionize the implementation. There are no implementations that you’d want to trust.

To address the ring signatures, whether it is [Borromean ring signatures](https://github.com/Blockstream/borromean_paper/blob/master/borromean_draft_0.01_9ade1e49.pdf) or log scale signatures or maybe even constant size signatures which I guess is not possible quite yet. Given the Taproot channel opening mechanism it will need to be possible to have them be linearly aggregatable such that no one individual is actually able to create a ring signature but when you combine the ring signature components it will work seamlessly. I don’t know if we have a Schnorr based ring signature proof aggregation thing.

I don’t think so. Schnorr based ring signatures do exist, that is what CT uses, but as far as aggregating them I am not sure that is possible. We could do BLS but we have some constraints if we are making it Bitcoin like at least. We could hope for the ZK rollup team to produce something that is usable, there are at least 2 or 3 of them that exist but they are still working on getting things to production.

I guess there’s a midpoint. The idea that we start doing proofs of nodes and then a node having proven some thing then can advertise a certain amount of channels and invert the proofs. If we are going to go to ZK that makes it a bit more lightweight because there are fewer nodes than channels. You probably don’t need as many proofs and they won’t change as frequently. The other discussion that we had, we could go for that kind of scheme and extend it to ZK later. But the question was how much anonymity does it actually buy you? If you prove that you own the UTXOs for a million satoshis, or have control of a signature for a million satoshis you could advertise 5 million sats worth of channels. If you do a naive implementation how much does that gain your anonymity set? That’s a question that is not that easy to answer. I was planning on looking through my node and trying to map all the UTXOs that it has ever produced. If it naively the first time I opened a channel revealed that but didn’t reveal the rest of it how much anonymity would I have gained? I do not know the answer to that but it means delving into a lot of logs to pull out UTXO set graphs and things. It is an interesting question. Would it gain us anything? It seems like it would gain us something but maybe I’m wrong. Maybe you’d end up re-advertising new UTXOs as channels close and you’d burn through all your UTXOs. Unless the magnification factor that you were allowed was so big that your DOS measures become weaker and weaker.

I feel like one of the big questions there is what is the ratio of a user’s balance that is actually in channels. Most users running lnd or c-lightning or whatever have half of their balance never actually go in channels. They just have it be onchain and then you have some pretty easy solutions here. But I would assume that that is very not the case.

Easy solutions for what?

If you are proving balance and not necessarily proving channels you could always segment your UTXOs. “Here’s my onchain UTXO, I am not going to touch this for a while”. As long as users aren’t actually using all of their onchain balance in channels all the time, opening and closing channels and whatever, then you could use that as your proof UTXO. But it is a waste of liquidity. My intuition, this is a question for you guys who have hobbyist users, no one actually does that and no one has spare funds onchain with which to do that.

lnd does. We haven’t figured out the UX as you can confuse people with error messages. We require a certain balance per channel to be onchain for anchor fee bumping. It is not a great solution, people get angry about it, some people turn it off. It is up to 100K satoshi total. Take every channel and then we have some ceiling. People like Breez had a bunch of private channels. This gets into another point, something I’ve been meaning to write up, is the reusability ok here? These things wouldn’t be encumbered for any other purpose. Bitfinex or whoever could just publish “I have 1000 BTC routing capacity”. Is that ok or do we want to bind the contents more directly. It is bound right now with the way the muiltisig works. That’s another open question. I am still not so sure on this leverage thing as well. Maybe it is useful. The other question I have is mapping it to the channel graph, I probably need to think about that a little bit more. At least right now we have a very explicit graph structure. This one would be “You can connect me with this certain budget allotment” or something like that.

You’d still require nodes to sign that “Yes I have a channel with this person” and you’d both cross-sign it. You’d still have that graph structure, maybe I didn’t quite understand your last point there.

Yeah but you could make it up.

It is more fluid basically. This one is static and in the chain. This pubkey claims those things. Maybe it is a good thing. You could reorganize your advertised graph on the fly. It seems like that’s possible with this. You could make just-in-time channels or something like that.

It is different and it does open the door to trust channels where you don’t really have a channel. You just have some relationship which simulates a channel, whatever. You do need some leverage though. What actually happens is, you end up using your first channel, you use the signature for that UTXO to advertise the rest of it. How you negotiate that with your peer, handwave, handwave. You won’t have enough onchain unless your leverage factor is massive, no one does that. Usually a node will dox one of its channels and ideally not the others. Hopefully a long-lived one so it doesn’t have to keep advertising every time. But you’d lose some things. You do lose the ability to auto-detect closes. You are going to have to have a close message “This channel is gone” because you don’t have the UTXO. You do lose the direct graph which is definitely true. Anything that breaks chain analysis is going to lose the direct graph. We are kind of gone there already. I don’t think it is too bad, we need to figure out what the numbers are. How bad is it? If you and I have a channel, which of us is going to use the UTXO to advertise for stuff? We can’t both. Do we flip a coin? How does that work? There are definitely some questions. If we have a counter does it go both to our counters? Both sides have to sign off on it, you can’t go completely rogue without having a graph that is somewhat believable. I would love someone to run with the numbers and try to figure out a scheme that doesn’t suck. The other thing is that is kind of cute is you can go for further obfuscation if you can lease out UTXOs to somebody else. If I can give roasbeef a signature on a random UTXO that I have sitting around for a month for some trivial fee. That obfuscates the graph further because then his node goes “I’ve got this UTXO” but actually it doesn’t.

But then I can buy an important looking node of yours.

You kind of always could. You still have to have other people who are advertising the same channel. You can’t just say “I have a million BTC to Bitfinex”. They would need to be in on it too.

They would need to cross-sign.

It opens a bit of a can of worms. I think anything we can do that messes up chain analysis kind of has the same can of worms. We are no longer bound directly to the UTXO set which means we can do some funny things.

I was going to do a straw man write up of what a basic one would look like. Put it on the table and examine it. Do you require the top level be a MuSig aggregated thing or not? I’m interested to see what the size of that would look like.

I think the bigger question is how much privacy does it provide? Your point about what do you require on the UTXO feeds into that in a very big way. If you say “I don’t require anything about the UTXO”, the user deposits one Bitcoin into their Lightning node, the Lightning node immediately creates a UTXO, signs a message with it, announces the node and then the user over the next week or month goes and opens channels. There are different strategies you could have if you don’t add that requirement that I think you would want to study at the same time as you study the privacy question. But the privacy question is the one that needs really careful study. Are we getting any benefit from this?

If you advertise immediately “I have 1 BTC”, you open a channel and then you have to re-advertise because you spent the UTXO. “I have this other one”. It becomes very obvious what you are doing if you did that. If you always advertised your change UTXO and you are opening channels you gain nothing. You have literally told them every single move you’ve made.

If you have a change UTXO on the side as a side effect of opening the first channel or doing a first deposit or something like that.

I think you’d only do it when you’ve got a channel open because it doesn’t make sense until then. You gain maybe something. You could advertise the channel or the change. Either one would work. I was assuming it was going to be all MuSig and all Taproot. Maybe you would allow an old style 2-of-2 so you could advertise using an existing channel. Somebody should write up a straw man and see what it looks like.

I was going to take a stab at the basic gossip one. I think I 80 percent understand what you and Matt have in mind but it would be good to get fully synced up.

I can write that up.

It is definitely smaller. If you assume that we are doing handwave Taproot. If that [message signing BIP](https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki), that one that people keep talking about gets finalized then just using that would also help. Rather than everyone having a boutique signing thing.

I think that was more for user facing encoding stuff.

If it were standard we could just use it and sign this message, whatever that is.

# lnprototest

Late last year we had that mixup, I want to make sure that doesn’t happen again. We were discussing picking up Decker’s [old beta test](https://github.com/cdecker/lightning-integration), the thing we use to say we’re compatible. But Matt pointed out there is [lnprototest](https://github.com/rustyrussell/lnprototest) as well. I was thinking we should move one of them to the Lightning repo, collaborate and try to improve it. We want to run it in our CI. What’s the difference between lnprototest and cdecker’s old one? One is newer or the lnprototest is more specific?

lnprototest is definitely the newer one. The integration testing that I did initially proved to be very flaky and really slow. Even the parts that we were able to cover were a tiny part of the specification. We only have a very coarse grained interface. lnprototest attempts to build an authoritative implementation that is not a standalone implementation but will walk you through different scenarios that correspond to the specification. I think it is much easier. Instead of having this complete graph of n implementations trying to work against n other implementations we have a star like structure with lnprototest in the middle. That is a scripted system that tries to adhere as closely as possible to the specification itself. It does adhere exactly to the specification as far as we know. We test every implementation against that one and should get into a situation where we end up agreeing on the specification at least. For a discrepancy we can always go and look at what the specification says and add details.

I wrote lnprototest because we want to test stuff that is really hard to test real implementations. Sending unknown packets and stuff like that, sending it in weird orders and all this other stuff. One of the problems with lnprototest is that it has only been testing c-lightning. I don’t know how many specific assumptions there are in there. There has been some slow work to make it more general. We have a new person starting, Alex, and I am aiming him in the direction of lnprototest. The idea is it reaches into your implementation, rips out your secrets so it can do magic. It used to be you had to set up a specific private key for your node and give it a particular ID. The current implementation for c-lightning actually does that but the code is written so that it can take anything. The idea is it reaches into your randomly setup node, grabs your secret, figures out your node ID, your private key and all that stuff. You can feed it backwards. It doesn’t actually require a specific thing, it is just our implementation forces everything. But that is dumb. It should reach in and grab all the information it needs. It is a minimal Python implementation, designed to be quite readable. It does enough so that you can feed packets and figure out what the state is. You end up saying “Send this, send this, send this. Expect this.”

Does this require us to have a Python implementation of all the BOLTs stuff in order to have fidelity during testing?

That is what took me so long. It is basically an implementation of the BOLTs. It doesn’t do all the state management. You obviously do that by sending packets and checking what should happen. It does have enough primitive helpers to make it not as painful as you’d think. You can go “Either this or this should happen and will walk through all the paths and try to brute force its way through a graph”. You can just write tests that are dumb, “Run this and you should get this”. It is pretty nice. But again somebody has got to sit down and write all the damn tests for stuff. That takes time. There is always something else on fire. It would be nice to move more effort in that direction.

I just need to get a little more familiar with it. We may have someone coming in to do general open source platform maintenance stuff. Maybe this could be in their wheelhouse. I see it has this DSL kind of thing, “Expect message. Send message”. I definitely can see how it can be super flaky on our Travis CI containers. Definitely something we need to get better at.

It is really good for new stuff too. If you are hacking up some new protocol then it is nice, you can write a clean test for it and we started doing some more development that way. You can test stupid corner cases that don’t really happen. You reconnect at this point and you restart, it should all come back. That is a pretty good strength of it.

The initial point is this [clightning.py](https://github.com/rustyrussell/lnprototest/blob/master/lnprototest/clightning/clightning.py). If we were to create something similar for lnd. We could make some special branch to do the dev stuff. I don’t think we have anything like that right now. Or when we initialize the node we could feed that through or something.

You shouldn’t have to now. It used to be that it was nailed in, it will be this node ID that I am talking to. Now it is the other way round. In this case the lnd driver would tell it “Here is the node ID, here’s all the stuff that you need”. You should write it so that it reaches in and grabs that information out of the node. I haven’t because the old style was a node ID, a private key of `01010101` etc but that is a relic.

Now I know this is the new way I am going to check this out.

I tried it at some point and it didn’t build. I believe that was fixed.

There was some weird dependency thing and you were on some weird platform.

I was on PowerPC, it blew up, it didn’t work. I think the dependencies were removed and I never got back around to reusing it. I should do that at some point.

We are trying to disentangle all of our Python dependencies anyway. If you find anything just tell us and we’ll do our best to disentangle it. We have some weird inter dependencies at the moment which are strange.

# Route blinding inclusion in offers

The current version of offers requires route blinding support as a first class thing that you have to support before you can do offers because you need to provide a blinded route as the only way. We were thinking the majority of the work of all these things between route blinding, onion messages and offers is going to be route blinding because we have to update all kinds of stuff. We would really like to ship offers and messages quicker. Messages obviously we could ship but we’d like to ship offers quicker. I know you had stripped down offers a little bit to make it quicker to implement. The question was should that go further and also allow hints like we do have currently without necessarily doing a full route blinded hint?

Good question. The reason I didn’t do route blinded hints… Ideally it would be a nice world where everyone uses all private nodes. I could be using route blinding because it is none of your business what my node ID is. So someone like Strike or an exchange can’t just go “No we’re not supporting route blinding and I am going to blacklist you”. It is nice to go “90 percent of the nodes are going to give you that so you can’t just rule it out”. That’s the motivation for doing route blinding. That said I haven’t actually implemented it. It is sitting there in the spec, “Handwave you should use route blinding”. Obviously I have implemented the part for messages because you need to do that to get the replies. I had an implementation for payments, it has not been updated. It is really nice to have an implementation of route blinding. That also gives you vendor privacy in general. We could cut it out altogether and then go “Only public nodes can use it” but that sucks in a different way.

Let’s not do that.

We could just import the route.

I think what you would do is you would add the normal blinding and then you’d immediately deprecate it. “Here’s your unblinded hints. It is deprecated, you should not use this but we understand that this will be probably be used for the next however many months or years”.

In which case it is like “Let’s just steal as much as we can from BOLT 11 and whack that straight in there”.

What parts are for route blinding? For payments the payment path maybe hard but the crypto part…

Are you talking about the requirement to add the route blind in the base invoice?

The only way to specify a last hop is via blinding. I don’t think the crypto part is the hard part because the crypto part is the same as the messages part. Presumably we would have that. More updating the router and figuring out the multi last hops to get to. That is not that bad. Changing the onion parsing and handling code for the forwarding and all that stuff. It is doable but it is a good chunk of work to get right and to handle all the different places that that touches. The nice thing about BOLT 12 and onion messages is it is basically all new code and it is segmented in a corner. You don’t have to touch any of the existing stuff or think about it.

We haven’t integrated route blinding in eclair all the way to payments either. We have done it for onion messages and offers. I agree that there may be some things here that will take more time than expected.

It seems interesting to me that we’re spending a lot of time investigating the SNARK stuff or hiding UTXOs whereas when you look at the current way that people are figuring out where Lightning payments are going it is a pretty strong indication that it is coming from invoices. Removing route blinding as an expediency thing seems like it definitely is pushing back a major improvement in privacy stuff.

I can’t speak for other implementations but at least in terms of our roadmap I don’t know that it would push it back so much as avoid delaying offers to have it. Adding non-blinded paths is hopefully no amount of extra work versus “Yes we will work on route blinding, it is a priority and will be a priority but we can potentially ship offers quicker if we don’t require it on Day 1 and we instead add it later”.

You are talking about the AOPP thing?

The fact that you can have an offer without a blinded route seems problematic. The fact that you are making it an option.

You are absolutely correct. I am not entirely comfortable with it either but pragmatism. Offers makes the world better and so I want to get it out there. Also more eyes on it will mean when we enhance it it will improve more. People are currently using invoices for tracking nodes and doing chain analysis. We should get people away from that one step at a time. At this point offers has been delayed so much that I’m much more accepting to this idea of taking shortcuts unlike 12 months ago. I share your discomfort. I understand what you are saying.

On the side I have been looking at trying to add an upfront server establishment to onion messages to allow people to pay for that bandwidth ahead of time. It just adds an initial HTLC roundtrip. This also lets the receiver not establish the circuit. I think right now they can be unsolicited blasts. I’m not sure API wise how you are handling that. It can be a two phase thing similar to the forwarding path thing where you pay for this thing and then you include this secret in the onion message and I know this is the proper route. I was going to write that up. It is a super lofty thing. If we have an option to deploy it with a meatier thing that’s the design I think. That would address a lot of my apprehensions with it, adding that in there and people can turn it on or off. It shouldn’t be that different. This is just adding an initial setup phase and everything else should be the same. That is my understanding, just me thinking in the shower.

Pre-pay for bandwidth is kind of cool. I think what will happen is we will end up with a relatively aggressively rate limited free onion message network. You can’t send decent bandwidth across it. Then nodes will be like “I’ll take your money and then I will give you a nominal number of tokens. You can reuse that.” That’s cool because your accounting on that can be really loose. You end up with a metering problem, you spend so much time metering that it is not worth metering anymore. You’ve made it exponentially more expensive. But if you’ve pre-paid then you can just swap the metering. You’ve pre-paid for a million packets or something and I don’t even need to do a database commit. Worst case I crash and it is error in your favor. I haven’t subtracted the last five, who cares? That’s nice. If you are trying to do something more complicated where you are associating a payment with each packet then it becomes nasty because both sides have to do database commits. Ideally a pre-pay with some kind of Chaumian thing. I can pre-pay but then I can trade them with other people and stuff like that is even cooler.

It is very much half baked right now. I’d be super happy to have that option.

I know Lightning node operators are getting eager for yield. I can see a future in which they offer all kinds of random services. “I’ll do some storage and some bandwidth” and whatever else. If we build a system where people can pay for stuff like that in general.

Umbrel pays for itself or something. That’s the dream. Put Bitcoin in the box and it makes more Bitcoin.

Turn the handle and out come your Bitcoin.

I don’t know if I believe in that dream but I believe the dream that there will be enough people who believe in that dream and make a really good network for the rest of us to use.

# Web socket support

I built the whole LDK thing into WASM and have the whole API exposed in Javascript for some completely unknown reason, people seem to want this. The question I have, the problem is I’ve been informed browsers seem to want to require web socket to be over SSL if you are on a SSL site. This makes your existing gossip method for web sockets not very useful because no one can say “Actually here’s the hostname with the SSL certificate that you can connect to for web sockets”.

Connecting to a raw IP address and just asking for an encrypted web socket is apparently too hard for modern browsers.

Do you want to lean on the existing DNS hostname thing? Do you want to change it to have a different hostname for web sockets which probably makes some sense, if you are going to have a SSL cert then maybe you are going to have a separate hostname. Or Cloudflare or something completely bonkers and privacy destroying.

You would need a SSL cert for the port as well, the port that they advertised. Wouldn’t the SSL cert that you need to connect to need to be the host and the port that you are connecting to? You can’t just go “I’ve got a SSL cert for this host and I am going to connect to a random port”. I don’t think that works.

I think the ports just do whatever. We do stuff and don’t specify the port. lnd has a Let’s Encrypt thing for your gRPC API that we do. It just accepts it and that works. That is a super good point I totally ignored. We use web sockets for some stuff but it is gRPC web which is still using TLS anyway. It has always been there so I forgot about it.

If you need it try to use it and see if it works? The web socket port advertisement is already a hack. It says “Try this port for web sockets” but you may have a Tor endpoint that may not support it. They end up having to work through.

The problem is you have to specify the hostname. You have to have a way to get the hostname. We can continue with the current design and say “I’m advertising the hostname and I add this extra bit that says there is also a web socket on that same hostname”. Or we could say “I’m advertising a hostname but here’s the web socket thing which is a different hostname because that hostname has to support TLS”. I didn’t want to deal with TLS. I don’t know if that should be separate or whether we’re ok just leaving it. I don’t know.

What is the behavior you see if you try a web socket in the browser? It doesn’t work or it complains?

My understanding, I’ve been told, is web browsers are all about “Everything should be TLS and if your website was loaded over TLS you can’t load resources over non-TLS”. It will block you if you try to load something from non-TLS and you are on a TLS site. It makes sense but it is annoying because we already have authentication in our protocol.

There might be a header field to disable it in HTTP.

You mean including non-TLS resources into a TLS session?

Mixed content?

I’m pretty sure all the browsers are TLS or die.

I think with mixed content the user has to click the button that says mixed content is ok on this page.

They gradually got more anal about this over time.

# Miscellaneous

I continue to work on Taproot stuff. I think I will finish the base implementation this week and then do onchain from there. I’ll look at t-bast’s initial doc.

Where are you on anchor outputs? We are going to make a release of eclair tomorrow and we are activating anchor outputs by default now. lnd activated it a while ago.

This is with zero fee HTLC.

Yeah.

We won’t be doing that until next version is my plan. This version I foolishly started a restructure and Humpty Dumpty is bleeding out on the floor for the while. Hopefully the CI is happy again this weekend. I am hoping that that will close out this release. I am release captain for this one. That is when I will be pinging t-bast going “How did you solve this fee problem? How did you solve this horrible complicated construction problem?” We are going to get into that too.

Are you doing reserve like we do in lnd or is it “We’ll get it when we get it”?

We can’t do reserve because we use bitcoind. If we lost the UTXO nothing would prevent the user from unlocking them directly from bitcoin-cli. What we did is now we have a new event stream with a new log file that is only for node operator important stuff. There is one event saying “We see that given your channels you may be low on UTXOs if everything closes or many of them close at the fee rate of today. Maybe you should preemptively add new UTXOs.” We are just annoying the users. If they don’t automatically get funds from elsewhere and send them back to their wallet they will be too late. It is really far from perfect but I don’t think there is a good solution there. Otherwise you would have to lock a lot of UTXOs just in case. You would have to guess the future fee rates.

We picked 10K per channel. It is a magic number. Fees are low right now thankfully but in the future we will need to do something. It definitely annoys users as well. They are like “I want to fund all”. We do a sneaky thing where if they do send all we’ll send a change address back to ourselves. It is not perfect but at least it will do the thing. Definitely looking for other ideas on that.

You need “all y’all” for actually all.

For real, for real.

We were planning on doing the same thing. Having a UTXO reserve possibly force closing a channel if we need more funds. Try a mutual close. The assumption that all your peers don’t go bad at once. But if you’ve got network connectivity issues that heuristic could fail really badly as you try to close all your channels.

Or if you have a bad DB upgrade all of your channels close and you had HTLCs in there, you have to claim everything at once, it is a nightmare. We are releasing production support for Postgres with a migration tool. We have tested that a lot because we really didn’t want this to fail and have people have all their channels fail at the same time.

We had a migration tool but we held it back, we should test this thing first.

We never supported migration, just no. People have done it manually… If it breaks you get to keep both the pieces.

One thing that we did that helped make us confident about it, we had been running for almost a year a node in a dual mode where we would write to sqlite as the primary and replicate everything to Postgres. Every time we would startup we would compare the two and verify that everything was right. We would also do dry runs of our migration tool. After many months of having everything go green we figured that we should have covered hopefully many cases. There should not be surprises in the wild but we’ll see.

In our case we have the problem that people have ancient DBs that have been running since 0.6. If you look through the codebase you’re like “That could never happen” but you need to look through the old codebase when that field didn’t exist. That makes me really nervous with migration tools. I have one of those nodes.

We have frozen our migration tool to only work with the current versions of the DB of all the table that we release today. If later someone takes a master branch it is just going to fail at the beginning of the migration and not start the node saying “There’s a version mismatch. The migration tool needs to be upgraded”. Hopefully people will not run on master too much and run into that. But if they do they are going to have issues. Hopefully people either decide to migrate right now when they do the upgrade or never and just start with Postgres from the start. I expect we will have to spend time doing support on that.

The other thing I find is that our CI for Postgres is really slow. Postgres is fast once it is up but setup time is ridiculous. Our CI runs for Postgres are longer than others at the moment.

Same, we added it recently in a very naive mode but it takes a little bit more time. We’ll go into more sql over time. Our database bolt can’t really keep up. I don’t know how Kubernetes works because bolt is s\*\*\* and etcd is s\*\*\* and somehow people run these massive Kubernetes clusters. I don’t understand it. We are divesting in etcd and some other things.

Do you plan on going beyond implementing the key, value store in Postgres in lnd?

Yes I think we’ll abstract this at the object level and have pure SQL stuff for things like invoices, payments, whatever else. Leave a bunch of the random key, value stuff there. It would be a hybrid thing over time. Because otherwise it is super scary to rip everything out and go pure SQL. I’m trying to do a more progressive migration, probably payments, invoices first. That is the thing that really bloats lnd. We keep around every single state of every single commitment transaction with every single HTLC which is why we have linear growth in state. It is the simple thing to do.

Makes sense. I was wondering why you were leaving all of that power of SQL on the table.

It was just the initial attempt. We are looking into that, a bigger thing. I think we have a basic invoice SQL table on the side. Definitely on the roadmap.

A while ago I hang out with Matt, he was telling me about this wild just-in-time UTXO scheme that Antoine was dreaming up for the anchor output problem. I was going to ask him where they ended up.

There’s an [issue](https://github.com/lightningdevkit/rust-lightning/issues/989) on the LDK or rust-lightning repo where Antoine started a big description of all the ideas he had. They haven’t made progress on it and thus far they haven’t decided exactly what they wanted to do.

Something, something full RBF, all our problems go away.

It sounds like both ACINQ and lnd have decided to go for the reserve requirement strategy.

lnd does reserve, ACINQ will call you if there’s an issue.

Thanks y’all. I’ll maybe try to confirm Matt’s HTTP web socket thing. What he is saying makes sense but maybe it just works.

The web socket stuff, because we are doing our own crypto underneath we are like “We don’t care. Give us a web socket”. It turns out that is against the mantra of most modern browsers. “We are going to tell you what to do”.

Worst case we’ll just have more crypto.

You can use a proxy. You can grab a web socket proxy and it will talk stuff for you. You have got traffic analysis privacy then. There are public ones out there. We could also all run one and do it that way. It would be nice if the browser got out the way and let us do our own stuff.

In browser land if you don’t have a domain name you are a nobody. You don’t exist without a domain name.

[ln.dev](https://ln.dev/) and just hand out names.

It resolves a static page for what it is worth.

900 a year? I don’t know.

Last thing, it looks like someone is sweeping anchor stuff. They have made some money (70 dollars) out of it. In 0.14 we realized that in certain cases we don’t sweep the anchor output. They are cleaning up for us. Someone noticed the design and realized they could get free money. Cleaning up the UTXO set.

When the anchor outputs first showed up they all had 330 satoshis. It was right around the same time I was testing the Pickhardt payments prioritization code using probes. I got s\*\*\* from half the community because they thought that those were HTLCs that I created. And I had torn down their channels. Should have known that before. I spent a couple of hours trying to debug whose HTLC leaked there.


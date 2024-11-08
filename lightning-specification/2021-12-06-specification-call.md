---
title: Lightning Specification Meeting - Agenda 0943
transcript_by: Michael Folkson
tags:
  - lightning
date: 2021-12-06
---
Name: Lightning specification call

Topic: Agenda below

Location: Google Meet

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/943>

The conversation has been anonymized by default to protect the identities of the participants. Those who have given permission for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

# Add payment metadata to payment request

<https://github.com/lightning/bolts/pull/912>

In theory you could have an invoice that is so large that it forces you to use a direct payment. But that is a pretty bad theoretical case. We could make some handwavey comment that users should be aware that it has to go in the onion so it should be of limited length. But that is like saying “Don’t do anything stupid”.

I asked on the issue before the meeting, is there any concern with someone who is making a repeated payment who tries to detect the length of the route in use by varying the payment data length over time across various retries?

How would they be able to do that, because of the payment secret thing?

As long as you know when a payment failed. If you have the ability to send someone ten invoices and have them try them in order and detect which ones fail then you would have the ability to figure out the length of the path they are using, at least currently.

You mean the recipient is de-anonymizing the sender? Not an intermediate node?

Basically, yes.

Maybe an intermediate option is to limit it to a large number just to prevent that.

That was basically what I was suggesting, limit it to something. I don’t know if you need 700, limit it to 256 or something.

640 is traditional.

420.

I would make it longer than 28 because that seems really small. There might be some applications that are excluded by that. I think it is already quite exotic what you described. You are able to supply multiple invoices that are all attempted and you are going to derive something out of it about the distance. I would pick a large value.

Note that any amount we limit it to is basically plus 32 because you can always use the payment secret as well.

There are other fields that are always there. What’s the minimum for a direct payment?

That attack already exists because I can hand you a fake route hint of arbitrary length that you have to use to make the payment, therefore leaving less room in the onion.

This is true.

Shall I add a comment to the PR that you have to be aware that it needs to fit in the onion including the route?

Yeah.

I did also comment on the PR. I think if we do that then we should at least also say that a payer must not limit the length except when they create the onion ie if someone knows they are well connected node they can just use a larger value. The payer must not apply any concrete limits.

To prevent the opposite thing, people limiting more than necessary.

Yes, exactly.

Let’s add that, let’s implement it and let’s do compatibility testing again.

# Advertize compression algorithms in init

<https://github.com/lightning/bolts/pull/825>

Let’s move onto the next one, the compression algorithm support thing. It is an old one, it was removing the dependency on zlib for implementations that did not want to support it. At the same time make it flexible enough to add new encodings or new compression algorithms if we ever need to. Make sure that this is also something that is more general than gossip queries if we ever need to. We can do it for free even though I’m sure we’ll ever use it. Basically you send a bitfield in a TLV in your init saying “Here are the compression algorithms I support”. People for gossip queries only use the things that both you and I support. We have tested with Matt on testnet and it worked great with LDK and eclair. It is not very hard to implement.

It is so much easier to implement zlib than it is to actually implement this.

It adds a bit of complexity. It is still one feature. It is not very hard.

I think what happens in the long term, we will end up using Minisketch for gossip I’m pretty sure. This becomes less important. I am happy to take your advice. If having implemented it if you are happy with the complexity of it sure.

I find it simple but it provides extension points that I think we don’t really need. But maybe we never use them so it is fine. I agree that the next changes we will make to gossip queries or to gossiping overall will be mostly a complete rewrite using something like Minisketch. We will change everything so we will throw this away. But I can understand that if LDK needs something to start with…

There are a lot of nodes on the network that already use non-zlib. In general it isn’t really an issue if you connect to enough nodes to get one that will send you uncompressed data. Given that I am not sure which nodes it is. Does lnd send uncompressed data by default or something?

It did for a while. We do a heuristic where we look at the compressed length and we go “It is not worth compressing” which is probably a waste of time. We’ve compressed it already, we should probably just use it. We do go “That didn’t win so we won’t bother”. If you ask for enough you’ll get compressed data.

It seems like less complexity than that. My point there was that it seems there are a number of nodes on the network that need this basically.

I think everyone has implemented decompression, I think some people haven’t implemented compression so that is what you are seeing. Implementing decompression is the easier part. The compression involves heuristics, you’ve got to fit it in a message and you’re like “I don’t know how much it is going to compress until I compress it” and stuff like that.

Interestingly we do already have these hooks. We already have the compression flag stuff. At least on the LDK end I just reuse those enums for compression because they happen to line up, at least currently.

Basically I think the state of this PR is we know we can do it, it is not too hard but do we really want to do it? Do we need it?

It is going to be quite a while before we rewrite stuff and not everyone wants the zlib dependency because zlib has not had the best history of ensuring its decompression library is safe.

It is just you, everyone else is happy with it, everyone else is stuck with it is the truth. zlib has a bad name but those are in the past. It has been pretty thoroughly vetted now. zlib is a lot smaller. The main issue with zlib was the whole explosive compression thing where you could really cram a lot of data in if people made assumptions about how much they could get out. Which is why the spec went through and figured out the maximum realistic size. If you get more than that you just throw it away. I don’t know. Shying away from zlib because it has bugs, if you can’t trust zlib who can you trust?

There is just not enough data in the network graph right now to care and so it is very easy to say “We can avoid bugs by simply not compressing because we don’t care and eventually we will move to something that is substantially more proficient than any of this anyway”.

I do buy that argument.

But then if we do that it is maybe not worth integrating this PR and instead phasing out zlib.

You mean drop zlib entirely? We could do that. I have a feeling that is not going to fly mostly with y’all on the mobile side. I know mobile using this stuff is important assuming you are doing graph sync on mobile.

We don’t care for Phoenix because there’s no graph sync. I don’t think eclair mobile even has the zlib part. Maybe but I’m not sure. I will ask Breez to see if they care and if they extensively use zlib.

Going back to first principles I’d be quite happy to just drop zlib. I would want to check some numbers but that is simple. I could do that commit. And it is perfectly backwards compatible. Stop compressing, keep decompressing and then at some point turn off decompression.

I’ll try to get in touch with a few wallets. See if they are using it, if they even know if they are using it or not. And if they can measure the difference between the two and see if they really need it. Maybe they’ll say that the fact that it uses more battery is more of an issue for them than the fact that it uses more bandwidth. I don’t even know if it is something that is important for them.

You are just not going to download the graph fast enough on mobile to want to do that anyway. At least not from a peer-to-peer node.

Eugene is saying that lnd doesn’t even have a config option for zlib by default. Unless Breez forked it they couldn’t be using zlib at all. I’ll check with the Breez team and if they are not using it I guess we can go and start deprecating it. At least open a PR and tell the mailing list and see if anyone says that they absolutely want to keep it.

# Dynamic DNS support in gossip messages

<https://github.com/lightning/bolts/pull/911>
<https://github.com/lightning/bolts/pull/917>

I guess the second one we don’t even need to talk about it because nothing has changed since last time. There is an eclair implementation and there is an ongoing c-lightning one but it is not ready yet. But the DNS one I haven’t done it on eclair at all. I don’t know if anyone else has worked on it?

911 we have merged at least as an experimental option. DNS support we have. We can put DNS fields in advertizements, it seems to work pretty much as you’d expect. It is a fairly straightforward change. 911 we have implemented, we should probably get someone else to implement it as well. There is a draft PR for 917, the init message change. Without Michael (Schmoock) here I don’t know what the status is but I can look at it.

I think it is not filtering local addresses yet. But apart from that he has the TLV and I tested that the TLV decodes fine on the eclair side. But he doesn’t yet filter local addresses.

That’s weird because we have that code already. That’s how we decide whether or not by default we advertize our own address. He probably just hasn’t hooked it up.

I think we can discuss these two when there is momentum in the implementations.

They are completely independent. I guess it would be nice if somebody implemented DNS, at least the lookup side.

One question on DNS. Punycode or UTF-8? It should be specified.

Interestingly in the offers spec we add a UTF-8 type to the fundamental types which is basically a byte string. It gives you a nice hint that something should be in an array of UTF-8. It might be useful to pull that in. It should be specified.

I vaguely prefer that this be ASCII and Punycode, DNS anyway. Things that do DNS tend to do the reverse resolution fairly well. I’m ok being overruled. It is just easier to walk a string and check that it is ASCII than it is to walk a string and check that it is UTF-8 with no control characters.

What’s the worst that can happen with UTF-8? It is ourself announcing and as far as I can see the only thing that we could get tricked into is trying to resolve this kind of stuff. It is not like the human is going to read it and get tricked by characters that look alike.

Ultimately when you do the resolution you convert it to ASCII and Punycode anyway. If you are looking to do that you might as well just do that upfront. Most of the DNS applications that I’ve seen will do that reverse resolution for you if you want it.

Is that true?

I know at least in some web browsers if you type in the Punycode it will show it to you as the UTF-8 as long as the TLD is one of the internationalized ones. At least this used to be true.

I think there are some domains you won’t be able to reach if you can’t do Unicode but I could be wrong on that.

No everything gets converted to ASCII. You take the UTF-8, you convert it to ASCII with this weird prefix, accent dash dash or something like that, I forget what the actual prefix is. You encode the UTF-8 as ASCII and then you do the resolution.

I am not a Punycode expert but that means that Punycode by definition is at least as long as UTF-8 right? Would that be an argument? It is gossip data that has to be replicated on each individual node so any byte we can save there might be a massive win for us. If we have to have some sort of tiebreaker.

It is only an extra byte or two. Obviously I prefer ASCII for everything because it is easier than trying to think about attack scenarios but if someone feels very strongly about byte length I’m ok with that too.

I guess I would prefer ASCII as well because it is just simpler. People can just find an ASCII hostname, there is no good reason to have something that is not ASCII for Lightning nodes.

If people insist on having weird hostnames they will shoot themselves in the foot by them paying the cost to advertize that. Probably going to stick with ASCII myself.

Everyone pays the price because it is gossiped. To be honest I just looked up Punycode, I had completely forgotten that existed. I am a little bit horrified. I remember before UTF-8 ruled the world. A certain amount of PTSD. I would say yes, it is ASCII due to DNS limitations, that is fine.

Alright, I will comment on the PR.

And make sure you put a link to the Wikipedia Punycode article so people can share the horror if they haven’t been exposed before.

And encode the link in Punycode itself.

Yeah, do that.

To one of internationalized versions.

# BLIPs

<https://github.com/lightning/blips>
<https://github.com/lightning/blips/pull/4>

I am ambivalent about whether they should go in together or go in separate. Whichever allows us to get this stuff merged before the year ends is what I’m in favor of.

Maybe separate is a good idea. The one I opened will be updated very often. Every time someone adds a BLIP they will have to open this table of things that they want to reserve. Whereas they should not open things about the meta process of adding a BLIP.

Agreed, I think that makes sense.

Keeping the two separate I think makes sense. I haven’t read the latest version of BLIP 1 since it has moved to the new repo. I need to do that right now.

I listed in the initial commit the changes that I made. One was per Matt’s feedback out of this specific mandatory universality section requesting the proposals discuss why the given features are not intended to be universal. That’s a must now. Add a little bit more detail around what ranges of feature bits and TLVs belong here. Between 100 and 1000 for experimentation on feature bits and then TLVs above 65, 536. Then a couple of links and stuff. Otherwise I think it is largely the same that we were close to having consensus on in the previous repo.

I guess it sounds like a good start to me. I think we will probably change some of those as we go, as we learn how people write BLIPs and what are the pain points. I think we should start with something as small and simple as we can. And then make it evolve as we learn more about the process. That looks good enough.

This looks good to me. I’m sure we are going to have some level of friction over the status field. The BIP process uses them for a little bit of pseudo inside baseball sometimes. I have a feeling that we are going to want to revisit these as we go but that is ok. I don’t think we need to figure that out now.

I think in general having this as a starting point and continually iterating on it as people start using the process makes a lot of sense.

I agree. I will do a real review this week. It is a conceptual ACK from me at least.

I will do the same for yours. For PR 4.

# Route blinding

<https://github.com/lightning/bolts/pull/765>

There has been a new review on route blinding. There has been a complete compatibility test between c-lightning and eclair on the latest version of onion messages. Did anyone have time to look at the route blinding one? My main feedback from the last meeting, I was asking what parts I should remove to get a first version in. Mostly probably the parts about the payments and I should keep only the parts that are library cryptographic utilities that are being used by onion messages. Should I keep it in the proposal document where it is not specified yet and we can iterate on it? I updated the test vectors as well and I think they should be easier for you to work with and build upon for onion messages.

Great. We have had route blinding for payments for well over a year as an experimental option. Basically unused except for the test code because there was no good way to specify it. When we tried to revise it to the latest thing we hit those issues that I commented on the PR. But it works really well for the onion message as a base and we have interop testing so I am tempted to leave it there in the proposal document but just not in the spec.

That sounds good to me. I didn’t put anything in the BOLTs related to messages, I left it in the proposal. I think the only important parts to discuss are the potential unblinding attacks that you would do by probing fees, probing CLTV expiry delta. It is basically things that we recommend implementations do like use the same CLTV expiry delta across the whole route. Use something that is different from the public values but maybe higher, same for the fees. I am not sure how to best convey those in the spec.

While I can specify that you should use the same value across you can always ignore those values and choose to probe the differences. The ultimate answer is you put it in the encrypted TLV, you put “By the way please enforce this value” so they can’t play with it.

That makes it bigger.

Perfect is the enemy of the good, yeah. That is another thing that can potentially be added later. I think for now a graph is relatively homogenous anyway so you wouldn’t get all that much data. Although you would get some doing those games. We have a way of fixing it later if we want.

What would you tell an intermediate node that is inside the blinded route when they receive a payment that they should forward and the fee is not enough or the CLTV is not enough? What error should they answer?

They have to fail. We have an error that we return from anywhere in the blinded tunnel, in that TLV we return the same error. In fact our implementation, if it was blinded we always reply with the same error. You’ll actually see it from the entrance to that TLV scheme and you’ll never see an error from the middle. That’s partially to protect against this attack. Although it is not perfect because you can still do success or failure tests. You get one bit of information out but you can’t tell exactly where it comes from. I’ll have to look up the code to see what we do but we have a specific error, I think we added an error for it. It has been a while, I’ll have to look.

From a honest sender’s point of view if you get such an error that tells you something wrong happened inside the blinded route, maybe it is fees, maybe it is CLTV expiry delta, should you just retry by raising everything for every blinded hop so that you have a chance of success? I think you should because there is a chance that your payment will go through. This is why it makes it better compared to rendezvous, you can retry, still use that blinded route and adapt to dynamic fees changing.

That is really hard to know. Your chances of success at that stage have surely dropped significantly. It is really up to the person handing you the route to have done that padding if any for you. If they haven’t maybe you could retry but you don’t actually know what is going on. It could be that there’s temporary disconnect in the route, it is not working anymore. That’s possibly the more likely case. It just won’t work. In which case you are kind of out of luck at that point. Unless they hand you multiple encrypted routes which is allowed in the spec but we haven’t implemented it.

I think that makes sense from the recipient’s point of view. Especially if you have multiple entry points. Just give most of them in the invoice. The idea is the same way you do route hints, you’d now use these. You can hand out multiple. The case where you don’t allow it… For payments it is a little bit different. For onion messages you only give a single reply path but the idea is you will resend if it doesn’t work and maybe try a different reply path.

Even from a payment’s point of view as a recipient if you are not well connected at all, you just have one entry point, since it is blinded you can still make it look like you have many entry points and provide many fake route hints. I think it is a good idea to have this option.

I agree. That’s for payments. We’d need to test that. But for onion messages this route blinding works really well.

I saw that Tim made a comment about typo. Do you know if he has some time available to review the crypto? I discussed it with Jonas Nick in El Salvador. He said it could be on his list because he didn’t realize it was a requirement for offers. They have so much to do already, I’m not sure if they will find the time to take a look at it.

I will beg and see what happens.

Sounds good.

# Onion messages

<https://github.com/lightning/bolts/pull/759>

On onion messages what is the status? We have two implementations that support it that are compatible. I know that since Matt has been reviewing it actively we should wait for more feedback. We can just not touch it anymore because we know that we are compatible but still wait for more feedback?

It is up to you what you want to do. I am not going to have time in the next two weeks to do it. I am hoping I will be able to make it my holiday project and find some time over the end of December. But we have been pretty swamped. I would say don’t spend too much time worrying about waiting for me. I hope to have time to do it at the end of this month but there’s never any promises there.

Whether it is merged or not it doesn’t stop us from continuing our work on offers. We are actively working on offers. It doesn’t change much for us if it is merged or if we just wait a month or two before we merge it.

Your plan is to do the route blinding PR first right because it depends on some of those commits at least? Is that correct?

Yes, exactly.

I am tempted to merge route blinding and onions because we have our interoperability test and we can say they are not going to change. Having changed this multiple times it is not actually that bad to change in practice. What you do is deprecate the old ones, you assign a new message number and you can do anything you want in the new onions. You can support both, it is a bit of a dance but if we were to find some issue… It doesn’t hurt anyone who doesn’t use it for a start. If we find there is some crypto issue, we should really do it this way instead then we can bump the message number by 2 and do our variation of the scheme there. It is not that bad. I do like the idea of merging it in because that fires the starting gun for people to go “We should really implement this now or at least look at it”. I vote that we merge those two having passed interop test.

There is just one thing that your comment made me think about. If it is true if we are only using route blinding and onion messages it is really easy to move to a different version where we for example change the internals of route blinding. But if you start using it for payments in invoices then you must specify some kind of versioning for this route blinding scheme? If we want to be able to move to a new one?

Not if we do it in BOLT 12. You’d use a modern message to request the invoice. Then you go “You’re speaking the modern message so I’ll give you a modern TLV”. You can switch the whole basis across because I’ve done this once already. If they ask to use the old onion message we’ll give them an old TLV, an old invoice. It is not pretty, it is layering violation but it does work. This then beds that down, the next thing to do is the route blinding for payments. That is something we can look at as well. I’m not going to commit to two weeks.

A new guy, lightning-developer started reviewing route blinding and onion messages so we can give him a few days or weeks before we merge. Depending on his feedback we merge these two.

ACK.

# Warning messages

<https://github.com/lightning/bolts/pull/834>

Let’s finalize warning messages I guess. There’s not much to say.

We had some argument last week but Rusty has not updated the PR it looks like. We are waiting on that.

You are ok to re-add that Rusty? The `O0` errors.

Yes. I will re-add zeros.

I’ll re-read it again and ACK it. We can finally get this merged since it is already live in 3 implementations.

lnd doesn’t.

LDK, c-lightning and eclair.

We never merged it. I have tested it with Rusty but we haven’t merged the PR.

# Clarify channel_reestablish requirements

<https://github.com/lightning/bolts/pull/932>

I created an issue to make it more clear. And I opened issues on lnd and c-lightning related to that.

<https://github.com/lightning/bolts/issues/934>

It makes sense but I don’t know what we actually do in practice.

I haven’t tested again. He was pretty sure lnd does automatically close before receiving.. but c-lightning he was not entirely sure. We started to implement a new mode for node operators of big nodes who are actively monitoring their node and don’t want to take any risks. They can configure this new strategy when we detect that we are late and the other guy says we are late, we print a big log in a specific log file and send a notification on Telegram or something to the node operator. Give them an opportunity to fix it before they lose thousands of channels. If they messed up something with TLV or.. We then realized it didn’t make sense to implement it right now because our peers would close anyway regardless of what we did.

It makes sense. I see that Eugene confirms that lnd does close. Is there a plan to fix that? I opened an [issue](https://github.com/lightningnetwork/lnd/issues/6017) on the lnd repo about that.

I saw the issue, no plan currently. But that doesn’t mean it won’t happen.

# Simplified update and PTLCs

<https://github.com/lightning/bolts/pull/867>

One thing I wanted to discuss is the simplified update because it is related to something I [posted](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-December/003377.html) on the mailing list today. The reason I’m bringing this one up again is I started looking into PTLCs recently and what was the way we could get a minimal version of PTLCs with a minimal set of changes to the existing protocol and transaction format. I discussed it with AJ who agrees that his proposal is a more long term thing. We should start with getting PTLCs on top of the existing structure. But actually there is one roadblock, there is one thing that PTLCs completely change compared to payment secrets. I posted that on the mailing list today and I have a detailed article on it. With a payment secret and preimage, when someone spends a HTLC success or claims a HTLC success you discover the secret by just watching the witness of the script. But with PTLCs it is different. When someone claims a PTLC success you don’t discover anything, the only way to discover it is if you had received an adaptor signature before. That means you have to receive adaptor signatures before you can sign your commitment. Worse than that it also means that when the remote commitment is published you cannot directly claim from it. You have to go through a pre-signed transaction that gave the other guy the opportunity to have an adaptor signature so that they are able to discover the secret when you claim it. We don’t have the easy structure that we had where I only sign things that go to your transactions, you only sign mine and I don’t need to give you signatures for anything from my local commitment. But now we do. I think that the current protocol of commit sig, revoke and ack, commit sig, revoke and ack doesn’t fit that model well. I think it is time to change it. If we change it we should try to find something that is somewhat similar to what we have so it is not too much of a complex change. Something that is compatible probably with an option simplified commitment and that works for both HTLCs and this first version of PTLCs. My mail to the mailing list was a call to action to protocol designers to propose some things without proposing something too complex or too different from what we have.

I haven’t worked on option simplified commitment in a while. An option simplified commitment is literally a subset of what we have now which is nice. It is significantly simpler. It doesn’t win you much in code until you remove the old version of course. You still have to support the whole state machine. One thing about is option simplified commitment that is worth noting, at the moment there are some things that you have to tell your peer to never send you because you don’t ever want to see them in your commitment message because to fail a HTLC you have to go through a whole cycle. If you switch to option simplified commitment it is actually easy to NACK a commitment without changing the state machine. They send you the commitment signed and you go “No I told you I don’t want that”. They go round again. That means you never have to give any explicit limits to your peer which is really good because that has been a source of all kinds of channel breaking bugs. Your peer thinks they can do something, you think they shouldn’t do it and they do it. The other reason I want option simplified commitment is there is a simple extension to it that we can do later that allows you to NACK a commitment signed. Then you don’t have any restrictions on your peer. You send me whatever you want, I’ll just NACK the ones I don’t like. I’ll instant fail HTLCs for you. I really want option simplified commitment for that because it simplifies the thing further as well. The more I think about it the more I really like this idea. I hadn’t realized the PTLC thing. There’s that and an extra round trip. I guess we will discuss it on the mailing list.

At least one I guess. That’s the hard part. If we didn’t have to have a new pre-signed transaction for the case where the remote commitment is published it would be fine. We’d just send adaptor signatures before our commitment signed but in the other direction. If I want to send you my commitment signed you would just have to send me all your adaptor signatures before and I can do the same. Now there’s also a pre-signed transaction in the remote commit and we have to both share this new signature for that but also a new adaptor signature for that before. That makes it a bit messy. That is why it is a bit hard to find the right way to translate what we have today into something that works for this case and is not a complete mess where people will get confused between what is in my transaction, what is in yours, what’s an adaptor signature. That is some whiteboard design.

I guess we will have to discuss that on the mailing list. I do like option simplified commitment. I think in practice it doesn’t actually slow things down very much because you just end up batching more as things go back.

Especially since what we realized with PTLCs, in a way you have to do some kind of simplified commitment. You cannot really stream in both directions because before sending your commit sig you have to wait for the other guy to send something. That is why I thought about option simplified commitment and making sure that they would work together. I think option simplified commitment, if we have drafted the rest, can be a good first step towards the protocol change for PTLCs.

Yes. The other thing about option simplified commitment is it makes update a lot easier. At the moment the channel update proposal uses this quiescent state where you have to make sure that nobody has got anything in flight. That is always true in option simplified commitment. At the beginning of your turn by definition it is static. That is why the spec is written in the twisted way it is. You have to be quiescent, you are always quiescent at the beginning. Any significant changes are much easier in this model. It is my fault because a certain person encouraged me to write the optimal algorithm in the first place and I should have pushed back and said “No let’s start with something simple like this”. This was my original scheme by the way. A simplex rather than a duplex protocol but lessons learned, I’ll take that one. Playing with implementations of this is probably useful too.

I think it is important to start thinking right now about how we could do PTLCs and not paint ourselves in a corner with a protocol change that would make it harder to do PTLCs than what we could ideally do. I would really like to have PTLCs in 2022, at least a first version of it.


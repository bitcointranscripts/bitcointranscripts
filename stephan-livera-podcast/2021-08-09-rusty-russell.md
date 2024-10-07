---
title: Lightning Offers / BOLT12 -The next big thing in Lightning?
transcript_by: Stephan Livera
speakers:
  - Rusty Russell
date: 2021-08-09
media: https://www.youtube.com/watch?v=KqKzOVH8W9g
---
podcast: https://stephanlivera.com/episode/298/

Stephan Livera:

Rusty welcome back to the show.

Rusty Russell:

Thanks. It’s always good to be here, Stephan.

Stephan Livera:

So Rusty, I know you’ve been making progress on this whole offers idea. Now you’ve mentioned this on the show in the past. And in fact, I recall at the Lightning conference and I think it was October, 2019 is when you actually first put this idea out there into the wild. So do you want to tell us a little bit about how this idea started and where it’s evolved from?

Rusty Russell:

Yeah, absolutely. So early on, we had Bolt 11, which is the current specification that describes those strings that you use to pay invoices, right? And such with lnbc1. So that’s that. I came up with that in the really early days of lightning, because we needed some way of presenting, like here, send me some money. You guys here’s here’s the thing, right? but it was pretty primitive and quite limited. And so we, along with thinking about what’s the next step, like where do we go from here? And I procrastinated for a few years and finally we had LN Conf, what am I going to talk about? Okay, great. I’ll get this ball rolling. And we’ll talk about, talk about this stuff and see what people are interested in, but the ecosystem had grown, right?

Rusty Russell:

It wasn’t just like the three, three companies kind of implementing stuff and nobody else cared, right? So that was the intro. We got along really good feedback at the time. The main question is like, when can we have it? Well we’ve got to come actually spec it out and flesh it out a bit. So I had half of the spec written and then kind of dropped the ball and when September came and in 2020, oh no, this is it. It’s been almost a year now, right? So let’s get it out. So September the first the first complete spec dropped and there’s been a number of revisions since then, as people can feedback and work on it. But the way this stuff normally works is that you kind of, the spec comes out and nobody really cares the implementers kind of get together and to have us implement it once we’re both happy with it we now set the world, right, cool.

Rusty Russell:

I’ve got a new feature. You should all come on board, but this one’s a bit different, right? Because all of those effects, all the wallets and affects everything else. It’s pretty big. It’s a pretty big deal. So you know, and all the other implementers are a busy, right? And I’ve got better things to do than implement this crazy thing that that’s kind of far out in the future. So it didn’t have that kind of urgency. So having realized that this wasn’t going to go to that standard way. Okay, well, let’s try the other way, which is to talk to the broader community about, Hey, we here’s Offers. What do you want from it? What, what here’s the thing it’s implemented and see linings is the second release that we’ll have offers in, right? So it’s actually been out there for a while in an experimental mode for people to play with.

Rusty Russell:

But without the awareness that, Hey, this is something you should look at because now’s the time to get in and tell us what’s broken. What you like about it, what enhancements, it needs, stuff like that. Some of them will come in future versions, but let’s get the ball rolling and go this way. So I created Bolt12.org which is like a website kind of summarizes it. And that really seems to have caught people’s attention and people who wouldn’t normally sit down and like read, okay, I’m not read 1200 lines of the spec. No, no, that’s great. Can, can kind of get a summary of, of what the hell is this. So what’s this about? and this led to this kind of feedback and excitement, which is great. And I’ve already had some really good feedback from developers. Of course it is it’s a big thing to implement. Right? Well, authors understand that the format, and in some ways it’s more complicated than what they’ve had to do before, because it puts, it has more capabilities. You can do more stuff, right? So we’re going through that right now. In fact in the last couple of weeks has really picked up, so it was really good timing to be on your podcast.

Stephan Livera:

So, so let’s rewind back a step and then just give us a bit of an overview. What is office like what, what is an offer compared to just doing a standard Lightning invoice? So I guess just the listening to, when you, maybe you’ve never used the lightning network, you might’ve had a phone wallet and you might’ve scanned that invoice, and then you might’ve scanned and maybe you might’ve seen it written out as lnbc, blah, blah, blah, blah, blah. What’s offers. What does that?

Rusty Russell:

Yeah. So basically you scan the QR code, make the payment, right? But that QR code that you scan which is actually just a string Lnbc something is a Bolt 11 invoice and it’s single use, right? it says here send me this money and I’ll send you the secret that maps to this, this hash, right? and so it’s single use deal, right? So I’m supposed to prepare one for everyone who might see that. So you come to me, I you hit order on my webpage, whatever you should, I should give you a fresh invoice, right? Absolutely not reusable. I mean, you can send them out on Twitter, but it’s a really bad idea because once that secret is out there, anyone who has the secret can collect the money, right? So it’s a single use thing, right?

Rusty Russell:

It’s a one time thing. And that’s to do with the way the lighting network works since the way that the Bitcoin protocol allows us to enforce that. So there’s a single use, but that’s really kind of pretty primitive. Right? You want something that you can just print statically on your webpage and anyone just goes and uses it, right? And everything else. So the way we do this is you actually reach through the lightning network. When you see an offer, it just tells you, okay, here’s the description, here’s everything. And you reach out and get the real invoice from that. And then of course, it gives you a unique invoice that you pay, right? So it is kind of a two-step, which makes it in theory a little bit slow, but in practice, you kind of have to probe the network a little bit these days to figure out who’s live, what’s working everything else.

Rusty Russell:

And Hey, you might as well send a real message. Right? So you ended up kind of fishing the offer and then you go, cool. Well, I, I know that I’ve got the invoice now I know this path work let’s use that for payment, right? So it actually works surprisingly well. But this two-step, it lets you do a whole pile of things that we couldn’t do before, right? So firstly, it can be a static thing so that you know, you could get it painted on your mural that you want donations for to slap it on your webpage. You don’t have to have any dynamic content, which is much, much simpler. It is you know, it provides some, some stuff that, that I actually really like, which is more advanced features that I think we’re going to love in the future.

Rusty Russell:

One of these is this idea of a payer key, right? So at the moment I, I pay my invoice and I, the secret and I can prove to anyone, Hey, here’s the invoice signed by Stephan’s node. And here’s the pre-image so I can prove that somebody paid this, the problem is I can’t prove that I paid it, right? in fact, Stephan could, can always fake that. You could say, yeah, uncle. So pretty much just so you can yet, I don’t know here, this was totally paid. So if I post the promote, see Stephan, I did pay you and anyone else can go, no, see I paid you to right now. It was me. It was me, right? Yeah. It’s kind of like one Brian, is

Stephan Livera:

So only uniquely you could prove it and not other people.

Rusty Russell:

All right. So we want this way to say, I can prove it. So I actually throw up, pay a key when I go, cool. Can you give me an invoice and put this, pay a key in there? And that’s obviously a key that only I have the secret to. And you, you, you saw an invoice and invoice contains the pack. This is, this is, this is the person. This is, this is the identifier, the person who did it. And so later on, if I want to, I can prove, obviously I own the payer key. I prove I paid it. I can prove I held the payer key. Well, obviously it was me, right? And nobody can fake that. You can’t even fake it even as the vendor, right? So I go, I had this kind of unique proof which is, which is really a nice feature to have.

Rusty Russell:

And there’s, there’s a whole pile of other things that we can do. One of the things people are really excited about is this idea of recurrence, right? So an offer can say, Hey, fetch an invoice, but you should fetch invoice regularly. Right? You should do it once a minute, or you should do it once a month, right? And this is the patreon kind of model, right? Where, Hey, here’s an offer to sponsor me. And you know, it’s like five bucks a month or whatever, right? And interestingly, when you start talking about recurrence scenarios where that’s really exciting and vendors would love recurrence. They love it in credit cards. But obviously everyone hates it in credit cards because, you have to ask them to stop pulling money out of you, right? Which creates a really perverse incentive, but in the Lightning world, there’s no pool.

Rusty Russell:

It’s always push. So you’re you sign up and call the ALP once a month, but you want to stop paying it. You just tell them to stop paying it. It’s done right. There is no pull, right? So it makes it, I mean, it makes it convenient, which is good, but it leaves the user in control. And this whole thing about sovereign control of your money is really, really a fundamental Bitcoin principle that this is perfectly compatible with. So I’m actually really excited about that as well. But you know, so when you start talking about recurrence, you start going well, pre, hyperbitcoinization. You don’t actually want recurrence in a certain number of sets. Right? Most people want recurrence and some currency, right? So you can do that as well in offers. So you can actually have an offer to like, Hey, pay me five USD right now.

Rusty Russell:

You know, how does anyone know what that means? Well, what happens is when you request the invoice, you get an actual number of sats, right? The invoice is literally for bitcoin the pecan invoice. So at that point for occurrences becomes really important. So one month I fetch it and cool, and I pay you to pay subsets. Next month I won’t fetches it again. And notice this, this has numbers change. Now my wallet is going to need some way of checking D is this saying the exchange rate is yeah. What the exchange rate is, because remember I’ll not be in Australian dollars. So I mean, never seen this USD amount, my wallet, the first time I have gone cool. Stephan wants, and I said, a five years, day, month, it presents me “Hey, Stephan wants like eight Australian pesos a month.”

Rusty Russell:

Right. and I go, yeah. Plus 10%. Yeah. That’s great. And so then it gets the next invoice from you and it goes, huh? That’s within the range is authorized because you said, yeah, still there. Good. Or it comes up as, hold on, wait. Now that, that seems a bit high. And then it’s gonna have to probably use again, you want to keep paying this because Stephan seems to be ripping you off, right? Asking for a little bit more than the exchange rate. It could be using a dodgy exchange rate. You could be trying to tweak things. And of course there’s a security problem. Like how do you trust the exchange rates? The only mitigating factor of that is Walt’s already do it, right? Practice. Every wall is converting to the exchange rate. You know, you can have some sanity checks in there.

Rusty Russell:

Right. You know, Hey, well, it’s Bitcoin might really dumped because it seems to be really like, you don’t care. Like if you asked me for less money than I expected, I’m like, yeah, cool. Whatever, if you think that’s five bucks, great go for it. But if on the upside you probably want to have some control. So there’s going to be some UX issues around that, but it is critical. And in the normal cases, this is the kind of thing that people are really, really looking for. So yeah, that’s an exciting thing about offers. There’s some little stuff in offers as well. It’s like, well, you can add a payer note, right? Which is, has no real purpose. Other than if I’m sending you like, Hey, I really love it podcast. You know, that was fantastic. So you can see the payer notes coming in and they get, they get put in the invoices, which is pretty nice.

Rusty Russell:

There’s we talked about this proof, this, Hey, I got the payer key and everything else in Bolt 11, you can kind of prove that you paid an invoice as I had before, but in order to show that it was really an invoice from Stephan and just make it up, it has your signature on it, but the signature signs, the whole thing. So I have to give you the entire, here’s the whole Bolt 11 string that I paid, and that could contain some, some personal information that I may not particularly like a node ID could contain a node ID. It could contain all kinds of things. So one of the things we did in Bolt 12 is it actually signs this Merkle tree, which is a fancy way of saying that you can hide some of the pieces in it and still check the [inaudible], which is valid. So I can prove, I can show you here’s the payer key, his you know, here’s Stephan’s node ID, here’s a signature and all those pieces, and here’s the description of what he promised, but I’m not gonna show you the rest, right? I’ll just give you a proof of that. So it’s a nice little design tweaks of things that we learned through experience of stuff that we wanted in both lemon. And it was taunting around to

Stephan Livera:

Get, yeah. Yeah. There’s some examples that I can even come to mind already. So as an example, let’s say some Lightning podcast, he wants to do a lightning Patrion using an offer, hypothetically like I’m imagining, right? And he wants to have a little chat community only for people who’ve paid. And that’s where again, payment proof could come into that and say, oh, see, you’re allowed into the chat group because you, you made your payment for the month or whatever. Like, just as an example, right? Yeah. That’s one example that

Rusty Russell:

That’s an easy thing to do to use that payer key because I won’t be the only person who has it. Now the other case where the payer key comes in incredibly important is for refunds, right? So the way the state of the art in refunds is pretty much, you know the vendor says, oh crap, sorry, we didn’t have your thing. It turns out that this happens, right? and so you send them an invoice to get your refund back. Now that has a couple of problems. One is that if you’ve already leaked your your payments here, somehow that then how do they know? Right. The other problem is that every note on the, on the route potentially has your payment secret. Although that solves with PTLCs it is potentially a problem. Or is it the payer key? I can prove that it’s me.

Rusty Russell:

Right? In fact, there is a specific offer flow for what we call a send invoice offer. So most offers are like, cool, awesome. My invoice. And you can pay me. There’s also the reverse case. You’re like, cool. Actually I want to send you some money, right? and there’s a specific refund field that says, Hey, actually, I want to send this guy some money, right? So present the package, presented to your signs at the sign, the request with your payer key and put that in an invoice, right? So through the network, again, your wallet goes cool. Sends it, gets the invoice back, right? Sorry. You said the last of the invoice back to you, you send me the money. Now this introduces another problem that we have today with the manual kind of flows that we have, which is that when I send you an invoice, I’m telling you what my note is now, normally this is we have this asymmetry in the lightning network where vendors are known.

Rusty Russell:

They didn’t really have no note. If you want to send to someone, you need to know where they are, but they don’t know who’s paying. And that’s a real feature. That’s an incredibly important privacy feature. Why do they get to actually have the money? They call that money in the huddle hands. So they don’t need identity information in this case, right? They don’t have the credit system. It’s that? It’s a payment system. So they’ve settled. They’ve got your money. That’s fine. They don’t need to know where it came from. But then of course you need to dock yourself to get a refund at the moment, which is really bad. Right? So you want your money back. Well, I’m afraid you’re going to have to tell me what you notice. So and this is why it’s really important that we have blinded paths inside of offers, right? So you basically go, here’s an invoice, but I haven’t told you what my note of it is. I’ve given you this blinded path, right? That you can stick in London and send it out on the network and then we’ll get to me, but you don’t know where it’s actually going.

Stephan Livera:

Oh, that’s crazy. That’s cool. That’s cool. It kind of reminds me of like the whole trampoline routing idea, right?

Rusty Russell:

Yep. So, and the normal cases would be used for refunds, but it’s also important if for some reason you’re a vendor Stephan wants to pay him back for beer or whatever, and send me five bucks. And I don’t really want to give you my node ID. I can give you — an I can say here’s, here’s the thing, here’s the invoice. It has applied to path in it. All right. Even though my note is actually public, you wouldn’t know that, oh, you’ve got to use that blinded path to pay that, pay that invoice. So, yeah.

Stephan Livera:

So then I guess I’m curious then how does your node know how to pay over? Like, I’m a bit curious about how the blinded path works. Could you just elaborate a bit on like how the other guy picks it up, actually picks up that payment? Like, how do you, how does it go? You know…

Rusty Russell:

That’s right. So in the invoice, it says, use blinded path to pay me, right? And I’ve made up my node ID, right? Technically I don’t have to, but presumably have right. I’ve just, well, I’ve met at a random node ID. Here you go. And use this path to pay me. And very carefully in the spec. It says that if someone tries to pay that, make that payment directly, pretend you have no idea what they’re talking about, right? because of course, I don’t want you to prove the network. And I wonder if that was a Rusty, you, if that’s Rusty’s note, I’ll try paying it directly. So, and similarly, the other way, if you try to use this blooded puff, anything else I will go, oh, no, I have no idea what you’re talking about. So you can’t go the other way later on and go, huh?

Rusty Russell:

I thought invoice from Rusty. And now let’s try using that own blinded bath and see if that’s actually the same note, right? So there is some separation of concerns. Thanks. But yeah, basically I give you these, this blind path that you can stick it in the onion and send the message that way. Now we already have something to step back a bit we already have something called Ella URL, right? Which does a lot of these things. It has the static property and everything else, but LN URL basically is a web web layer thing. You know, you have a website of a kinks at rail on the rail and you get the invoice in a way you go. And it has some other cool features too. But in this particular case, I really like it being built into the lightning network, right? You’re not actually doing web connection. You don’t need to set up a web server. You don’t need a TLS certificate and all those things to make the web secure. We already have this lightning protocol that you’re relying on for your payments. So let’s just send messages through that. And this, this is basically completely web, but completely lightning native and gives you that, that same experience, which I think is really a key feature as we want to grow.

Stephan Livera:

Right. Yeah. And so I guess putting it into practice and there might be different wallets, and if anything, the walls might support both. They might support L and URL and office for all we know. And it will just have to sort of see what the market chooses over time, what the entrepreneurs and the users.

Rusty Russell:

Yeah. One of the, one of the first requests I had actually. So Jessica, who does the Spock wallet has been he’s got he’s, he’s basically hacking at the moment on a release that will have office support. And one of the first things he said is, I want one QR code. It’s got the, could have LN URL and an offer in there, right? Which means we’re probably gonna make an L on UL and Jameel for in there. It’s, it’s going to be a bit bigger than you’d like, but one of the cute things is that that offers actually smaller than invoices today. Right? And this was, this actually came back from the moonwalk developers who were talking to me about offers and they went in developing countries, a QR code is a resize is a real issue.

Rusty Russell:

Right. screens are really crappy cameras and put, the camera might be bad. That’s right. You really want there’s like, get it down. Like, come on. I’m like, wow. The biggest thing in the offer was the signature. Right? Originally it had a signature fully signed. When I thought about it really hard. I went actually we don’t need the signature. If you can’t validate the offer, when you go to request the invoice, the invoice is signed, right? Which is what you really care about. So we made the, in the list version of the spec, we actually made the signature optional. We may actually eliminate it altogether and it just don’t even bother. Which makes it a pretty tight invoice, right? And has subscription has node ID? My husband, the fields, like a vendor may have some recurrence information.

Rusty Russell:

You know, I might have a bypass. I mean, he can certainly get bigger, but the minimum size is actually pretty tight and it makes a, a nice you know, pretty easy to scan QR code and you can jam a lot more things in there. Of course, when you get the real invoice that goes over the whilst you don’t care, right? Yeah. That could be huge. You could have a whole kinds of options. and that doesn’t matter anymore, but that office size is actually pretty critical. Yeah. That was great feedback that, that I wouldn’t have thought.

Stephan Livera:

Yeah, of course. I, and certainly, I mean, and that reminds me of how I like Nicholas Bertie would tell us about how, when he went to El Salvador, Arizona, he was learning things that he had never learned because he was previously remote from the location and didn’t understand on the, on the ground, in the real world, what’s the, what are they seeing? So I guess, what am I look like then? I mean, I guess what I sort of speculating a little bit, but maybe it would be like another tab inside your wallet. And it would be like, okay, here’s your office. And if you’ve got recurring things going on and okay, I’m donating to this person or that person, and then you can enable and disable them as you choose.

Rusty Russell:

Yeah, absolutely. That is that definitely UX flow. So the UX flows like scan. And if it’s a simple offer, it would just go pay it right into same as the way it does now that tells you the amount and you go, yes. If it’s recurring, it’s gonna ask you, oh, by the way, this, this wants now paint, once a month, I get called on a problem. It goes into like your recurring tab, all the outstanding things that you just you’re stringing SATs out for, right? So you can go through what the hell is that? No wonder. I forgot. I forgot Stephan. So you know, you basically just have the summary of all your payments going on and what’s happened to those successful the way that it works. I mean, recurrence is a bit difficult to kind of the spec covers the whole, all the cases you know, per minute is pretty straightforward.

Rusty Russell:

Per set. Number of seconds is pretty easy, but if somebody wants to be paid first of the month, right? That’s not a regular occurrence, but it’s a really natural thing to do. So the spec does support them. It supports the guys, what did you say? I want play it on 31st of every month. Well, there isn’t a 30 and ever, what does that mean? I mean, so that’s all well-defined when can you pay? Right. So I want to be paid the pay. I want to be paid the first of every month, but can you pay 10 months in advance? And the answer is, no, you basically have to have paid the previous one to get the invoice to the next one. Right? You can’t just skip. there is a setting that says, this is actually a fixed start and you can start any time, but generally you have to pay the first one, if we can get the, get the invoice of the second one, right?

Rusty Russell:

And keep going, and you, by default can only pay in the previous period or the next period, right? So I can grab the first one. So it says once a month, I can grab the first one you pay it instantly. That’s great. Now I can either immediately grab the second one or I can kind of second month halfway through, I can grab it. But you can actually specify that the invoice, I’m not actually here’s the window, but you can pay this, this, this, this, this is like the, which sense to go outside that. Yeah. And of course, if you, so let’s talk a little

Stephan Livera:

Bit. Yeah. I’m curious as well. How it would work in the case of like a failure. So let’s say there’s a payment failure. What now would they retry? Or how would it, how would it work then? Right.

Rusty Russell:

So I mean, that, that, that’s a really good UX question, right? So it depends on what the span is like if, if I’m suddenly paying once a month, right? I basically got a two month window to pay this thing. My wife probably doesn’t want to play at the beginning, but maybe five days for the end of the month and wants to kind of okay. It’s time to pay now. And if it fails then to try to get into it Rouse you know, it might be after a few times, if if things are getting dicey, then you pop up a thing like, Hey, hold on, we’re actually, this is stuck. we haven’t been able to pay this. You know, the note is down, it’s been down for the industry. So if you’re trying to pay every minute, then you’ve got less leeway to kind of do that.

Rusty Russell:

Right. And you, you’re going to want something that’s pretty reliable. Our fetch invoice implementation it’s the lighting is pretty, pretty simplistic. It basically goes, huh, I think I can find a route. So it tries once and it doesn’t get to reply to, it gives up after 30 seconds, which is kind of dumb. But one thing that it does do by default is that because not all the networks support these onion messages yet. If a compounded route, it’ll just do a direct connection, right? Which is terrible for privacy, right? you’re just going connect. Can I have, can I have this invoice please? Oh, no reason. Because by connecting, you’re revealing your node ID and everything else. And that can be disabled, but by default for bootstrapping, this is obviously an experimental feature and C-Lightning it certainly makes it convenient to bootstrap the network that way.

Rusty Russell:

So connecting and just, Hey, give you this invoices is easy. And as the net network upgrades, we’ll get more, you know we’ll be able to just route these things through and we’ll do it intelligently. We’ll retry and we’ll do a few more you know, maybe, maybe we’ll try a few things at once and stuff like that. So just you know, we have to note this gap between like the ideal situation and what is in real world experimental implementation today. Yeah. It’s definitely a better, but yeah. I would expect that, you know what, we’ll do the retrying stuff and all those things. Yeah. Gotcha. But you know, just behind the scenes, cause this is that happens, right? Of course.

Stephan Livera:

And then how about from an availability point of view? So as an example, if that is a mobile wallet and he lost his connection to the internet, and now he can’t serve you the invoice, like, I guess these are some of these little practical, real world examples where people might have to figure something out in terms of how to do it or to wake it up, to receive the payment. Yeah. But remember

Rusty Russell:

They already needed to receive the payment, right? So it already needs to make it up. So when you’re up to serve the invoice, I’m usually I mean the default invoice timeout out, see learning, if I recall correctly is ridiculously low. Now, if it comes from an offer, because they’ve just asked for the invoice, the minimum, they’re gonna pay it now, right? What are you doing? Right. Well, you ask them for an invoice and then waiting two days, right? So you’ve worked me up for this let’s let’s, I’ll say, wait for 60 seconds come and kind of hit me with, hit me with the invoice, right? maybe with the payment, right? So so that’s they can get pretty tough. So usually it’s back to back and that’s part of the point, right? Is that by requesting the offer, I’m also like, or by request the invoice for the offer, I’m kind of waking up to know Nicole, I’m ready. And I’ll find some pilots through to you. So I’m like, cool. That’s that’s up candidate for me to use for payments.

Stephan Livera:

Yeah. Yeah. Well, okay. Here’s another example. What about if there was a insufficient capacity and you know, that that user is on, say a Phoenix or a moon or a breeze and they need like an on the fly channel, I guess that would all just be handled as a normal flow, right? Just a normal payment being made there’s insufficient capacity to receive okay. On the flat channel creation, something like that, maybe. Yeah.

Rusty Russell:

That works exactly the way it does today, which is actually pretty well on those products, right? They, they do pretty good dynamic balancing and stuff like that. You know, obviously more intelligent pay routing will help there as well. We’ve got lightning where nice work on stuff like that, but making more intelligent use of the channels that we have rather than just throwing more capacity indefinitely. But definitely that, that’s something that and to some extent, now there’s a little bit of anticipation as possible, right? You know, I’ve just issued this invoice crap. I they won’t be able to pay that because I don’t have capacity. Let’s, let’s do something. Yeah, right? you know, you know, you could see a future, a vendor where it was not going right. You know it probably wouldn’t be a single case, but you start seeing liquidity drop and you’d start going.

Rusty Russell:

Okay, well, let’s go out and get some more incoming. And I point here at like, Lisa’s work on the dual funding at Bozeman stuff is obviously goes really, really well with this model where in the next, C-Lightning release, which is probably going to be released by the time people hear this podcast. Cause it’s due in a couple of days from today. It has this experimental support for these dual funding ads, so that you basically advertise the liquidity and you go, cool. I will provide liquidity for you for a certain number, right? And you’ll be able to reach out and kind of add liquidity on the fly that way, which I think is pretty important in a completely distributed open way.

Stephan Livera:

Yeah. Cool. So I guess maybe just to explain to the listeners, if you knew, essentially when you want to receive on Lightning, you need some incoming capacity and there are different ways. This is being solved. So as we mentioned, say the Phoenix, moon and breeze, they like open a channel on the fly, but another way for example, Lightning loop, ah, sorry, lightning the channel market the the pool pool, sorry. That’s one way. And then another way in the seat Lightning world is this idea of advertising for liquidity. And then you might and then the wallet might intelligently decide, oh, I need some liquidity or, or another way is maybe while it’s building some kind of interaction with LSPs Lightning service providers, and you have a relation with the bit refills or someone else and say, oh, I need, I need to take some payment. I need some capacity, Hey, let me buy a channel off you, you know? And so that’s maybe,

Rusty Russell:

Yeah. So just one, one thing I want to clarify here is C-Lightning is the first implementation of the liquidity advertisements, but it’s the spec so that this is a draft that’s in the specification process. And the way the specification process works is you need two implementations that they both work together. And I’ve gone through all the, before it gets finalized. So it hasn’t been finalized in the spec. We’re just the first ones to implement it. So then we see this as the way the way these things happen in the future is that there’s this open marketplace. You know, we have already had this gossip network where no talk about themselves, cause it’s all just cute nicknames, favorite color, that kind of thing. They’ll also, they also can put in there now I also supply liquidity at these rights, right?

Rusty Russell:

So then you can connect to them and go, cool. I’ll put some funds in, I’ll cover your costs that you’ve established and everything else. And you can evaluate, Hey sure, this business cheaper, but this bed’s business better connected. So actually I’m better off how you channel to them or more to really well connected to them, but not so well connected to you. So that’s, that’s, I kind of have a personal load to say only you will have all the information that you need to make that call of like, how do you judge the market, right? And it will vary. We’ve definitely seen a competitive, I want to say competitive sport emerge and running profitable liquidity, providing lighting notes, right? So I expect that this kind of open marketplace will take it to the next level with that, right? People really trying to optimize their nose to provide this service that anyone can rent can at least liquidly for, I should let Lisa talk about who did the ads, but one of the really cool things that it is, it’s a standard contract for one month.

Rusty Russell:

So if you bond liquidity for me the thing is that I can open a channel with you and promise the world, but at the end of the day, I don’t have to route anything through to you. Right? So one thing that, that incentivizes me to do that rather than just take your money and close the channel again and run away is that my channel is actually time locked for a month. So the terms of the offer that I’m making I will talk my liquidity for a month. I might still close the channel, but if I do my, my the money coming back to me is deferred for a full month, right? So that’s a stock that at that time that will reduce as we go through. So I’m committed at this point. So I can’t just take your money and run. I mean, I, I can, but it costs me if there’s no benefit, I might as well just keep routing for you’re making routing phase. And one of the other key things that happens is that I promise to you in a way that is signed by my node, what the maximum routing fee, I will charge people to get funds into you.

Stephan Livera:

Yeah. Because otherwise you could jack up your rates crazy high.

Rusty Russell:

Yeah. That’s right. Here’s some liquidity, but it’s going to cost everyone 5% to use it, right? Which, which on the lightning network to be clear is, is astronomically large, right? you know, and that’s fine as long as you’ve agreed that to that upfront, right? now at the moment, there’s no enforcement system. I mean, at the end of the day, you can charge people what you want and what can I do, right? You know? But the protocol does include a sign message where you promise that from this block height to this book, basically there’s one month period, because again, build a periods of like based on one month you will not have the base fee or proportionally more than this amount. So if you did, I can actually broadcast that on the network. Okay. Stephan’s being an, right?

Rusty Russell:

So, so let’s not use him as a liquidity provider because he doesn’t, doesn’t keep his right at the very least, or even like not, we’re not going to run through him. Well, we’re going to ignore as he keeps claiming he wants 5%. Well, look, we’re going to pretend that he’s just on the cap. I’m going to pretend you said that, right? And we’ll try. And if you reject it well, that’s up to you. So that that’s like a nice defense mechanism for the network, but that again is not yet implemented. We have the messages, but we don’t send them out if you try to choose a, so that’s really important. Part of market design is making sure that there aren’t hidden ways that you can try to gouge people like everything should be disclosed upfront. And something that you can prove if someone’s misbehaving, right, the best way to do things is to make sure that no one can misbehave, but if they can misbehave, the second best thing is always to have this, this way that you can, you can publicize that.

Rusty Russell:

Right. And prove to everyone, Hey, you made this promise and you he didn’t. Yeah. So I expect this to create a really healthy dynamic market for providing liquidity for Lightning, which we’ve seen a lot of people jump on trying to do this. So the game is out there who are optimizing their nodes and figuring out all their rates will absolutely love this functionality and creating this open competitive marketplace. So I think that’s actually going to be huge. And for the end user, for most of us who are not there kind of you know pimping on nodes all the time, it’s going to be just really good to have all these people competing to provide us. Luckily. Yeah, that’s right. So when you start taking your lightning donations, Stephan on your podcast and it takes off, right? And you’ve got all these people there’ll be liquidity providers like bending over backwards to get that liquidity to you so that you can get your money, right? Which is ultimately where we’d wanna be.

Stephan Livera:

And I think it’s really interesting as well, because if we go back years and years ago one of the old school things people used to do was just have a Bitcoin address public and say, oh, if you want to donate to me, I mean, people even do this now, but obviously there’s better awareness now about why address reuse is bad. And obviously it’s a bad privacy practice to tie up a Bitcoin address to your real-world identity. And so this is like a potentially a new way that people can achieve something similar, right? Because, and I think I understand where maybe some people who were more old time Bitcoiners were like, oh, I remember those days when you could just pay to an address. And I could just put it up there and it was cheap enough. I mean, and okay, fine. Even as we speak, now, it is relatively achieved.

Stephan Livera:

Like it’s like one or two that’s provide, but of course, we’re assuming it’s going to, it’s going to go up, but this is another way that maybe using offers. People can have whatever and that they can be a Twitch streamer or they can just have a website and they could be out in the real world. They could literally be out in the real world with a stole and be like, oh, here’s my little LN offers QR code. And then it’s kind of bringing back that old thing, but in a new way, that’s more scalable technologically advanced. So that’s an interesting point. I just wanted to highlightning for listeners out there also just to kind of make it practical in your mind, you’re listening. And you’re like, oh, okay. This offers thing, but what would it be in practice? You know?

Rusty Russell:

Yeah, this is absolutely true. So one of the one of the people who approached me off to the LN first talked about this with somebody who, a company that produces those barcodes at supermarkets, right? And they want to right. You know, they’re like, how would we do how would we do lightning on this? And they could, in theory, like you scan it, you pay it. And they refresh the display and they put in a new invoice. The problem with that is one invoice is a reasonably large, and it’s kind of nice to offer as a smaller secondly, these things are battery operated and they use eating displays. So they don’t use any power when they’re not updating, but it’s actually quite expensive to update them. Which is normally great, cause it’s only happened to change prices, but if they were doing that every time somebody tried to scan the item a lot.

Rusty Russell:

Yeah, right? So offers kind of solve that. But you know, a low-tech way you know, this is where you get your donation tattoo, right? You get your offer tattooed on your arms so people can just scan it and send you money you know, or static webpage. Right? So this is the donation play at case. Now, [inaudible] already had an experimental offer up. So you can feed the chickens through an offer. The downside of that is that with offers being experimental, the spec has been updated. And in fact, they’re using the previous version of C-Lightning and it’s incompatible with the latest offers. So that’s in the new version C-Lightning. and so this, this is actually only, I want to emphasize to everyone is that this is still a draft. Is this experimental it’s a little bit reckless, right?

Rusty Russell:

So, so, you know be part of the experiment and absolutely if you have feedback and we’ve got great food, but you know, if you’re using the, so your, your wall development stuff and you come across a video, why did you do it this way? Right. Maybe there’s a good reason. Maybe we just didn’t think of it. So this is the, now is the time for people to play with it and experiment with it and come back and go, no, this sucks on the counter side, because that is still happening and still get the Greer draft, hasn’t been fully ratified until we’ve got two independent implementable implementations that work together and all the walls authors have gone give, given the thumbs up. And we’re pretty happy with all the trade-offs. You know, things could change, which means offers as they are today. You know, we could change something and we can’t make any promises because we want it we obviously want the best technological solution when we, when we get there, right? So the trade off of that is that the early early people are taking kind of a risk that, Hey, you may have to make a new offer because we change a format or something becomes compulsory. It was whatever.

Stephan Livera:

And as you rightly say on the website, don’t get your offer tattoos because

Rusty Russell:

You’re not getting a tattoo yet. Okay. Plan for it show, but don’t get it until tell us back to actually ratified. Do not, do not go for the tattoo. Yeah.

Stephan Livera:

And so I think this is also very practical in for that use case where someone wants to take donations where previously, if somebody wanted to take donations and let’s say they’re living under an authoritarian regime or whatever, I would have had to tell them, Hey, get samurai wallet and instill paintings and hope that everyone who pays you uses that, or install BTC pay server, which is again, quite a big lift for people. Obviously the BTC pace of it works pretty much for everyone, but it takes, it’s a lot of technical ability and skill. Whereas this potentially could just be like, download a mobile app, set up your office, QR, share the QR and dunk. Yup.

Rusty Russell:

Look, Hey, sneak, sneak the QR code out on a postcard or something, and everyone considered donations, right? that is definitely, definitely in my mind, a huge step up that you don’t need a web server. You don’t need all this infrastructure that you can just do this or offers is, is, is definitely what we’re aiming for, right? So, yeah, I think it’s, I think it’s a game changer but you know, this, this requires more authors to go and implement it. I mean it’s been interesting stepping through a, an, a dove going through spark and the changes that he’s had, like had to think about what’s the UX flow. Like how do we keep it simple? You know, what, what are the trade-offs with this? Oh, now we’ve got to have persistent storage. We’ve got to remember the recurring ones and stuff.

Rusty Russell:

In fact, now he’s pushed off doing the first release is not going to have recurring offer support, right? But you know, we, we’ve had to have these discussions about, wow, cause this is a whole new side of functionality for the wallet to remember these things, to wake up on time, to pay the new one. And then what happens as you say, like, what happens if that fails or you can’t fetch it cause it’s flying and you know, how do we retry? And you know, there’s this whole, this, this is a step up for all authors. Right? it also means, and I think this is a direction that wallets are gonna go right. Is they’re going to actually start speaking the Lightning protocol natively now in a step in that direction underneath the covers, this Bolt 12th string that starts with the LNO one that, that offer is actually exactly the same format that we speak to each other peer to peer on the lightning network, right? It is just a lightning network message encapsulated in this, you know BEC 32 looking and coding, right? So it’s really nice letters and numbers, right? But you kind of like we leading leading wallet authors to like, well, if you can decode and encode these, you actually now can speak the Latino. It pretty much just need a few different messages and you know, a little bit of crypto and you can talk to lightning notes and stuff. So it’s kind of

Stephan Livera:

What I’m reminded of. You know, Samuel L. Jackson is like Lightning. That’s right. This is

Rusty Russell:

The way it’s going to be, right? I think Walter, author’s going to start, right? She reached out natively on the lighten network and start talking to things. In fact, one of the hacks, I have fussy lining Washington school of hack. It’s an, a proposed spec update is and this will hopefully be in the next version of lending, is this thing called web sockets, right? So it’s actually really hard to speak lightning natively from a browser, right? Because browsers generally open right. Raw connections to people. They they, they speak web stuff, right? But there is a web statical, web sockets, anybody see, you can’t get like a web thing and you actually own upgrade this to a web socket. And it becomes a web socket. It’s actually pretty easy. And so I wrote a modification to C-Lightning, if you connect to us and you’re not dancing to speaking of lightning, but you, then we try, maybe you’re trying to open a web socket.

Rusty Russell:

And we have a little proxy that kind of just speaks enough web socket to got to that. And then you talk to us over the web socket, use the same crypto and everything else as if you were sending it raw, but you’re just doing it from a webpage, right? And that opens the ability for anyone to speak to a lightning node, right? From, from anywhere Android apps, everything else. This is all for for most people as a, probably be pretty obscure. But if you’re a web developer, you’re like, cool, I know web service, that’s easy. So if we give people the ability to connect to the lightning network in more ways, it means they can do more cool stuff. And like network potentially it’s a payment network, but it’s also a communications network, right? It’s this network of all these nodes talking to each other, it’s got good security properties, it’s got some interesting other properties and it is growing so potentially allowing more people to connect to it feeds that growth and allows us to do some more interesting things that I’m terrible at predicting the future, but I’m sure people will see this, oh, I have this great thing that I can now do with the lightning network.

Rusty Russell:

So I’m really looking forward to it.

Stephan Livera:

Yeah. That’s cool. Yeah. And I’m also wondering, are there any impacts in terms of people out there who might be more concerned with say censorship resistance or privacy? Is there any impacts there if, if they’re using offers as versus some other method?

Rusty Russell:

Yeah. So privacy, the fact that offers have this blinded path thing means that you get a lot better privacy. And even as I said before not just as a mom, there’s no vendor privacy and Burton selling problems with the nudity. So blinded, pause kind of fixes that. But even if you don’t care about that case, the refund flow where you are the vendor, because they’re trying to send you money. Obviously that’s a big hole at the moment, right? So you’re great. You’re obviously sending these, you know these payments and as the network grows your anonymity set becomes bigger and yeah, we get more confident of things like that and techniques to improve privacy continue. But but in it, and you hit this brick wall, when they go, oh, we want to give you a refund. You don’t want my money. I don’t want my privacy. That is a terrible, terrible trade-off that day, that decision. So definitely definitely that, that helps as well. Yeah. Yeah. So

Stephan Livera:

We could basically see this being used. I mean, would you just see it being used, like anyone who can use it would use it then, because it’s smaller. And basically, even in the standard case, like, even if you’re not doing the whole donation example, you are literally just a normal person who doesn’t care. Who’s not like that strongly concerned about privacy and so on, but you’re just paying a merchant and you would just use offers because it’s just more convenient to do it that way. Right?

Rusty Russell:

Yeah. Eventually this, this will become the standard is the way I see it. You know, we will just use your office for everything and you’ll scan it and there’ll be the sooner, eventually we drop Bolt 11 compatibility, you go, whoa, well that’s old school let’s well, why are you doing that? So yeah, we, we, we’ll just, it’ll all be offers. You can have a single use offer and C-Lightning. So it’ll only get basically you know, it’ll only, you can actually meant one multiple invoices from it. Because you know, you may request an invoice and they’re not going to reply. So you met, you didn’t need to support that, but then once you pay it, that’s it golf has done. That’s really important for the send off send money case where you’re, it’s an offer to send you money.

Rusty Russell:

Obviously you only want to do that once, right? kind of important. But a classic example, there’s ATM’s right. So ATM at the moment at Lightning ATM, it’s like, well, you have to give them an invoice to get your money this way. No, no. They would flash up an offer. You scan it and goes, oh, that’s a send invoice offer. So cool. I would have send them the invoice and they’ll send me the money, right? Yeah. Gotcha. It’s the same format. It just has different fields. Hey, actually, I’m not, I’m trying to get money from you. I’m trying to send you money. So you send me an invoice and I will still pay it, right? And obviously that’s just by default. So that’s already supported in, C-Lightning and pretty straightforward. So yeah, this is a push side of offers, which for ATM is really logical for refunds and very similar in those things.

Stephan Livera:

Yeah. Yeah. And so that, I guess compares with, say LN URL where people might be using that right now to do this kind of L and URL pay. Or I know there are other forms of LN URL such as authenticate or channel are the ones which I varying support, but I guess then the idea here is office is kind of operating at a more protocol level and you don’t need a web server for that. That’s probably the key differentiators there for people to think about. And we may be in a world where we’re using both for some time. It may just be like that.

Rusty Russell:

Absolutely. And that’s why I think they encoding the the step where we include one in the other. So you can have a combo, right? Is there are two QR codes, oh need to speak off of the, but you know, that’s terrible, right? Sort

Stephan Livera:

Of like a compatibility layout, like wrapped SegWit 3 addresses.

Rusty Russell:

Absolutely. You know, we do these things all the time, even though we don’t think that they’re the ultimate protocol solutions, just because it does simplify that transition, right? We’re not in the days anymore with a lot of network as this kind of fun thing where there’s like five friends using it and we can just go, oh, cool. Everyone upgrade and it’ll change right now. It’s like, okay, we’ve got a plan this right there are wallets coming out all the time. They haven’t heard it like, wow, okay. This is this new lightning war, right? This is a whole ecosystem now. So it is a bigger deal to make these upgrades. On the other hand, the biggest growth is ahead of us. So now’s the time to do it, right? It’s only going to get more difficult to change into three years time. So, yeah. And that’s true of anything, but I think for something like offers, it’s really important that we kind of get the ball rolling now and get that feedback and make sure it’s the best that we can. It can be and they go, right? We’re ready now. Here’s 1.0. Let’s go.

Stephan Livera:

Yeah. Yeah. That’s excellent. So I’m curious as well, do you have any thoughts in terms of the growth of the network? I mean, we’re seeing, I mean, it probably wasn’t that long ago. I think Christian deck around this desk back in, was it September, October, 2019. And there were maybe six or 7,000 Lightning nodes on the network then, and as we speak today, it’s over 20,000. So do you have any views on where the network is going and you know, how that growth is coming?

Rusty Russell:

Look. That number is the one that excites me right now, the [inaudible] like that, right? That the number of, and not even the capacity of the lightning network, cause that’s kind of that that’s you know…

Stephan Livera:

Over the conversation about TVO and it’s a bit nonsense. Yeah, no, no, no.

Rusty Russell:

What’s interesting to me is like, how many users are we looking at now? Some people, liquidity providers are running multiple nodes for various reasons and I get that. But that headline number of kind of what going up is, is a really nice thing to focus on, right? So how many nodes are we seeing in the network and you know, not all the nodes in public but looking at that growth. And we see obviously I think running Phoenix seeing, seeing great user growth we can tell, cause keep making bigger and bigger channels. I made a 10 BTC channel the other day. It’s like, well, they’re doing that. They’re not doing that for fun, right? They’re doing that because they need the liquidity because of all their users, right? So we are definitely saying, you know throughout the industry, we were seeing this growth going on, this, this, this this broad user base.

Rusty Russell:

And I think that’s that that’s incredibly exciting, right? Because you know, I’ve been in this for six years, right? So read the, read the Lightning paper originally no one had a plan to implement it. So blockchain said, Hey, Rusty, you should, you’re joining bloodstream. You should, you should go implement the lightning network. And so we had the first implementation, we did the spec process. We kind of grown from there. There’s been lightning labs was founded the icy people kind of pivoted to doing, doing learning stuff. And it’s great. So from these humble beginnings and there was always a thing of like, what if we build this fence, we could see it, right? We were like, this is going to be amazing. What if you build it and then no one else sees it, right? It’s too hard.

Rusty Russell:

Why would I do that? Nobody has a big client anyway. So why would I use it to spend staff or, or or bit kinds of saving technology. So why would I spend it? And it’s like maybe and that, that became a big, big thing. It’s like, well, maybe we’ll build this fantastic thing and they won’t come, right? And they’ll never, let me see you going, we could have changed the well, but it never quite caught people’s imagination. And so it’s been really exciting and things like big on beach and El Salvador and stuff to see people go, yeah, no, this really does. We get it right. This really does solve a problem. And you know, I think our tendency in the Bitcoin world, as, as kind of reaction to the low levels of hype that you see in crap coins and other random scams is to kind of really not over promise.

Rusty Russell:

Right. You know, it’s a bit of a delicate balance, but you know, we prefer to produce code and stuff that works and then have people discover it and go, well, this is fantastic rather than going out and evangelizing, right? It’s always pretty uncomfortable to evangelize stuff to people. Cause you don’t want, you start to sound a little bit like my coin is the greatest thing ever and you should invest, right? So in fact the number of we talk about Lightning the early days people would you’d have serious people go. So how do I invest? I’m like It’s not that kind of project?…

Rusty Russell:

Then lightning selling lightning spot, this was a running joke for a long time, right? that just, you know so we tend to know the natural engineering responses to light, just put your head down and kind of go and do stuff, but you do occasionally wonder, Hey, is she is this ever going to really take off? And it’s been fantastic to see people actually go, yeah, this is fantastic. We are using it every day. People like Jack mellows close building products that I had never conceived of on top of the base layer, this is the most amazing thing ever. and doing that next level stuff on top of this open network we’re building is, is just an amazing, amazing feeling. But also I’ve been a bit of like, you get a chance to take a victory, victory, lap, and pat on the back, like we’re doing well.

Rusty Russell:

And you’ve got a whole country who be using Lightning. Yeah. And then you like it, you hit download, right? That’s it. But we’ve got so much stuff we still got to do there’s, this is really Greenfield stuff. There is a whole pile of things that opportunities that we haven’t touched a technology that we want to improve. You know, this is definitely going to keep me busy for the next decade, right? There’s, there’s so much cool stuff to do at the base layer so that people can do these amazing things that they building on top, right? Yeah. But it is, it is, it is great to do that. You know, every time you use the line that way he gives me a bit of a thrill, like, holy. It’s just like, wow, that was amazing, right? I actually had to, I had to, I sold some Bitcoin recently because I wanted to buy a coffee machine.

Rusty Russell:

This was a big thing. Like Bitcoin hit 50 K. I was like, all right, that’s it. I’m going to buy my ridiculous coffee machine. Cause I have these 5:30 AM, Lightning spec calls, a spec spec online meetings. And I’m like, not, I need a decent coffee, like a really nice Italian espresso machine. And I was like I’ve been kind of a hit 50 K man. I’m going to go sell some, sell some SATs and I’m going to get it right. But that, that funny happened. And I’m like, wow, okay. It actually happened. I’m going to do it. I tried to ask them if they’d take Bitcoin, they wouldn’t sell it. Okay. I have to sell some SAS. I sent people like a thousand bucks of the lightning network and it just worked just like, wow, I just sent it, it worked, it was done. And I’m like, holy crap. That was, that was amazing, right? I mean, we never it was originally always thinking about like really small amounts, everything wrong. Well, I’ll try it. Wow. It just worked, right? Did you go

Stephan Livera:

In and check if it was like an MPP and all that?

Rusty Russell:

Yeah, well that’s right. And I looked at it and split it all and it all kind of went pretty well. Wow. Okay. Now for that, interestingly, I pushed a whole pot of SATs out to my Phoenix wallet and use Phoenix to pay it. So they had to worry about the liquidity getting to the other side, but it just I was like, Hey, that was, it was just such a smooth experience. And obviously so fast having done like local Bitcoins trades where you’re waiting for confirmations and stuff like that. And these, and then paying fees on top just to send it peer to peer and have it done was like, whoa. Okay. And even me, I’ve been waiting on this thing to actually do it was a whole nother level. So yeah, it is a real thrill to use it and yes.

Rusty Russell:

My travel plans include going to El Salvador at some point outside fortress Australia to you know, just to get that whole, yeah. Let’s just, let’s just see this in action natively. I’m preaching the truth about both 12, but, you know just to go in and actually have that day-to-day experience is, is, is amazing for somebody who’s been so deep in the weeds for so long trying to get this stuff full what’s. And we always look at the problems and stuff like that to have a moment of kind of like, oh man, that just worked. And that was amazing. Is, is it really is a thrill.

Stephan Livera:

Yeah. Especially for listeners who might have only, just recently learned about Bitcoin enLightning, if you had joined and tried to use lightning three years ago, or you would’ve seen it, you might’ve failed, hit payment failures on a $50 or a hundred dollar payment. Now, easily people are doing thousand dollar payments on the Latin U network.

Rusty Russell:

And we’ve got Renee Renee out there doing some fantastic research on basically how to push the boundaries of that. You know, we’re, we’re really excited about pushing, putting some of that stuff in because if you do, if you try to hit an edge case where you’re really trying to there’s, there’s two cases where we suck. One is where we really haven’t to split in a specific way in order to get it through because it’s only just possible. Well often give up before we hit we’ll time out, look, I mean, I know we’ve spent too long on this one go away, but other cases where it’s actually impossible, we will bang our heads against all kinds of stupid possibilities we’re coming back and Renee’s work is much more like a, Nope, it’s not possible. Nope. It’s not gonna happen.

Rusty Russell:

Right. We were underneath the point at one and lot faster, right? We need to fix this. You know, you need some more liquidity, you don’t have enough funds or they don’t have enough liquidity. Someone needs to be fixed. So fairly fast, but also managing those edge cases. And one of the things we’re seeing at the moment is people shouting a at of liquidity. But using it more efficiently is going to be really key as well. But then again, I’m pulling back in this mode of going, oh, here are all these problems and stuff, but yeah, look at how far we’ve come. You know, when the first lightning payment I made to sell a cat pitcher to to Christian deco back in the day, right? That I was like, wow, we got it to work between two PS, you know? And then routing payments with async through through multiple node implementations was a huge breakthrough back in the day. And now just say, cool, no problem. I’ll throw a thousand dozen bucks worth across, across the network. And it just frigging works is it is a pretty nice. Yeah,

Stephan Livera:

I’m also curious as well. So one of the, I guess, speculations out there is that lightning adoption would really be driven if we were to hit a high fee environment. So basically when we pay our Bitcoin fee having to put up, attach a fee for the minor right now, that’s quite low that obviously if we’re bullish on become where we’re expecting number to go up in fair price terms and in sat terms. So I’m curious your view on that and would, how, how would lightning respond in a high fee environment? Yeah,

Rusty Russell:

So that’s a really good question. So and to some extent it’s like the weather, right? We don’t have a huge amount of control over it. So we’re just kinda gonna make sure that we are prepared for the worst and just go over that we’ll find out when it happens, right? You know, I like a low-fee environment, right? It makes it really easy to open channels and do these other things, which is fantastic. But yeah, look, we, in a higher fee environment, you might start to get more conservative with clothing channels, right? So generally and this has been a true trend over the time originally, like, C-Lightning was like, we’re very much following the spec and you disobey this backwards, closed channel on you. That was our answer. Everything we don’t like, you, you close channel, right? you know, send us something weird.

Rusty Russell:

We close the channel. And increasingly we get more forgiving. It’s like, okay, well, we’re going to give you some, some breathing room that because you know, people get upset when channels close. Cause you know, they lose liquidity. They’ve gotta kind of go again. And they get the fees, right? so we’ve gotten more forgiving over time. It may, we may eventually get to the point where we go, oh, you did something I don’t like, but it’s not worth me closing the channel over and do that constantly stick. You don’t want it to absolutely. You can kind of live it. If someone get away with everything. Cause you terrified of closing the channel, the end of the day, you got to go to chain to enforce your rights. But you know, there is a level there where you go, ah maybe, maybe this isn’t so important.

Rusty Russell:

We see stuff like channel coming out where you can basically have multiple channels on top of channels so that you have this base layer and then you operate on top as definitely mitigation via fees. And I think research into that will only really kind of implementation will only get driven when we’re in a higher fee environment. When people are like, yeah, cool. We really want this now. You know, as I said before, there’s so much to do in lightning that we’re driven by pain, right? You know, excitement and pain, right? And so this is really cool. We have to do this or like, oh crap. You know, we really hurting, we have to do this. So I imagine a fee environment will drive more innovation and things like channel factories and things like that, so that we can get to so that we can, we can, we can try to work around that.

Rusty Russell:

But fundamentally there is this conflict. If you think of like, Bitcoin is your, your arbiter in this case, right? So learning works really well. When something goes wrong, we go back to Bitcoin and go fix it, right? And we’ve got all these contracts signed, we’ve got everything signed dumping on Bitcoin that will enforce it, right? But that’s expensive, right? So we’re always going to have this tension where in a perfect world it would be ideally and enforcing everything else. But at some point you go, well, actually it was 20 SATs dude. I’ll just let it go. It’s, it’s not worth enforcing. You know, and this statistically there’ll be some people who go, no, it’s principal, man. I’m going to, I’m going to enforce it to get my 20 sites back. But there will be cases where it’s just like that that’s just kind of a cost of doing cause they’re doing this and that’s just physical, physical reality is that sometimes it’s not worth enforcing the theoretical rights that you have because the costs are ridiculous and we’re going to see this layering.

Rusty Russell:

And you know I’ve I certainly hope that we never see Bitcoin fees hit the point where it becomes untenable to board people onto the lightning network, right? So there’s that happy medium where fees are high enough that you don’t just use it casually, but not so ridiculously high that, that you go, well, I can’t join the line that way now because I have to use someone else’s channel. I can’t, I can’t self custody. So but again, it’s like whether we don’t have a huge amount of control over that, one thing we can do of course is try to aggressively squeeze more transactions into blocks, right? That’s going to kind of use the stuff that we’ve got better. And that’s something that’s happening in a taproot and stuff like that. It’s all about squeezing more stuff in and I’ve always been a longterm advocate of a block list increase at some point, but you know, it, that is a much longer term deal.

Rusty Russell:

You know, you would have to be very conservative increase. And you know, we’ve never had a heartfelt before, so it would have to be decade in the making of this would be a huge deal. We’d get one shot at it. We’d have to give at least five years upgrade I mean, it would be a massive undertaking across the industry. And so we would need to have broad agreement. And we’ll probably only have board agreement after we’ve had use of pain, right? At some point we go, right? Okay. So fees are higher, they’re staying high, we’re shorter. You have to support the network, but they are getting uncomfortable. Is it time to stop talking about this again? And because of the previous experience with Yola block size increases and there’s a natural reaction against there are a number of people like we would never going to increase the block size.

Rusty Russell:

I think that’s probably perhaps a little bit too much as well. So that’s a whole conversation that we have to have. But look even today, like I know we can take a lot of the pressure off the block size thing, so that can’t continue indefinitely, right? Cause, cause we will grow, we will get more of this stuff, but you know, it, it, it changes. It really does seem to have changed the number as far as how far out before fees go up, right? We’re going to see if we can see a lot more growth in Bitcoin before we see fees skyrocket, which I think is fantastic. Yeah.

Stephan Livera:

Interesting points. So there I’m reminded here as well. So the number of people throw around is something between a hundred million to 200 million ish. That’s not how many people who hold some Bitcoin today in the world, out of the 8 billion humans on earth, right now, many of those are not custodial. As in many of them are custodial users. They’re not holding their own keys, but of course over time, people will sort of come down the rabbit hole and learn and they will start, want to use the chain and then boom, there’s going to be all this demand coming. And so I think the projection, I can’t recall who made this projection, but someone said, we might be looking at 1 billion users in 20, like in five years. And so that’s kind of crazy when you start thinking about that, because if we were to hit a five or a 10 X, let’s say we hit like a 10 X in a year or two or whatever like that, even that would start closing a lot of on chain impact.

Stephan Livera:

Right. Because then you’re, you’re, you’re going to have to be more careful about who you open the channel with, because maybe they’re not as trustworthy a partner or because you’re now you’re like, okay, my cost back then when fees were one set, but I can open channels to whoever. And I mean, it’s obviously there’s still some risks, but it was less because but now if the fees were to be like, okay, Bitcoin price goes to 300,000 and the setup fee is a hundred sets per bite. Boom. All of a sudden you’re paying a lot to open and close channels. Right? Yeah.

Rusty Russell:

So yeah, there’s, there’s a couple of interesting things here. Basically. It’s also a trustworthy is reliability, right? Punter reliability is kind of important, right? If they’re not there all the time that eventually like it’s you’re going to have to close. Now one of the changes that has gone through that, that L and D have have implemented, and the rest of us have kind of been lagging on having experimental implementation, but it definitely needs work. And it’s aligning point, we can write a flightning fully in the spec, is this, this zero feet anchor output idea where basically you lowball the fee for your commitment transaction. So if I have to unilaterally close at the moment, we need to make sure it definitely closes. So we use this high rate fee, there’s a trick, we actually use this. We can use a lower fee, but then we can use a child with we create a child at the time that pushes that in to the blockchain.

Rusty Russell:

So kind of all the fees are loaded in the child or the RBF. Yeah. What to do child pays for parents there. Sorry. Yeah. Gotcha. Because we kind of, we Stephanie and I negotiated this ages ago, he’s gone away. I can’t get a signature to RBF it. So I really need it because if I go mutual close, that’s fantastic. But if I can’t and I need to go on chain, use the child to push this in. And that lets us decide on fees and how urgent things at the time, rather than trying to guess the future. So that, that is actually a big improvement that very much driven by fees increasing and people going, wow, that cost me a lot to close that channel unilaterally. Did I really want to do that? So using child pays for parent is an obvious extension that is requires original amount of engineering and everything else.

Rusty Russell:

It requires more engineering for us to implement it properly because you then need to be able, you need to have some funds to create a child transaction, right? So LND already kind of sequester some of the funds out. So they’ve always got a UTXOs they can use, but what if a lot of these happen at once and you’ve got to kind of use the change of one to pay for the other and you know, you can, you can get quite complicated and it really, you need to be juggling a lot of things in order to get that right. And Allergan does visit. You need to start making decisions on, well, because you can do this you can, you can, I’ll be off the child. So he puts the child in ah, I didn’t go in. Maybe I’ll maybe I’ll push a bit harder.

Rusty Russell:

Right. Well maybe I don’t care. Maybe I’m like, okay. So I’m unilaterally closing this this channel was Stephan because he’d been offline for a month, but you know what? I haven’t had my funds for a month. There’s no issues. He’s in flight. There’s nothing urgent about this. I can low ball and just wait. And you know, what, if I want to open a new channel, I can use the new channel open to push the elbow through. You can sort of batch things up in a way. Yeah. Batch things up and do batch openings and stuff like that. We already support that in NC lining. So you can basically be multi opens at once. I did a test on Testnet where I tried to open the channel with every test that note at once. Most of them failed because Fesnet knows people like throw away all the time, but you know open something like a hundred channels in a single transaction.

Rusty Russell:

And so we’ll see more of that where people are batching and stuff, but it doesn’t really help for the single node user. You’ve got a couple of challenges. You can’t really do a huge number of tricks for that. Maybe you can do that one transaction rather than two, but you know we are this is again, make things more efficient and squeeze things in, but at some point really high fees are going to hit us. And so we’re hoping that we keep that under control while we grow the lightning network. And once you’re on board, then the cases where you have to close as reliability goes up, as people get better at this. And frankly as people use the lightning network more and this stuff gets more polished reliability is definitely been improving and I expect it to continue to improve, but yeah, they’ll be the case where yeah, I had a channel of Stephan’s phone, he dropped in a lake and that part of the boating accident and I’m going to have to unilaterally close and you know, that sucks. So there will definitely be on chain activity. But the idea is to like keep it to a minimum, right?

Stephan Livera:

And I’m curious as well. So we were talking a little bit about channel factories and this idea of not just to have two channels, that it could be 10 people in a channel or a hundred people in a channel. Do you believe that? Let’s say we got any press out at some point in the next few years, five years, 10 years. I don’t know. So any prevalent and we get L2 and we stopped doing all the channel factory stuff. Would you believe we would still need a block size increase even then even with channel factories?

Rusty Russell:

So the problem is if you don’t have blocks, that’s increased and you push people towards more custodial solutions. That’s just like if you can’t go on chain, you end up in a custodial solution. So that’s the tension. At some point, if you can’t fit everything on chain, you’re pushing people away from using Bitcoin. And that that’s that’s something that happy medium where there’s the minimum. There’s an internal factors to kind of a middle ground. You have some group that have at least reliability concerns, right? Everyone’s going to be alive and active or available. Or if you do some clever and of em scheme, you have to have a trust issue then, right? Because what if all the 10 of you in the group any nine can vote on staff and change stuff? Well, now you’ve got this problem because they might screw you over.

Rusty Russell:

So either way you’re pushing people into a model that you know, is either has a reliability problem or has a trust issue. And it’s not, it’s fine for those things to exist. But if that becomes a primary use case, well, the only way you can afford to use Bitcoin in Lightning as if in one of these commune style, trust things, then you really kind of take you’ve taken away. People’s self sovereignty again. So there’s definitely a tension there. Now on the other hand in practice, will we see families with their funds in that kind of system? Totally. That that could well happen, right? You end up with aggregating at some small level of community or something like that. But at the end of the day, people will want to hold their own phones. Now maybe, Hey, maybe the cold storage is to learn and they have that one UTXO and yeah, it cost them 50 bucks to open it.

Rusty Russell:

But you know, it’s sitting there for long-term storage. And then they have their community channel and that works on people we’ll work around it. And I’m increasingly convinced that people are finding lending so useful that they will figure out all these things if they have to, but I’d prefer not to push them into that model and have some happy medium where you call it, you can have this community thing there’s other thing, but and this, this channel factory and everything else but it’s, it’s, it’s also reachable for everyone to have oh, the majority of people to have a UTXO that they can

Stephan Livera:

Yeah, so that might be a big disagreement in the, in the 10 years. So in 10 years time, there might be those who say, no, people should just use custodial and then there’ll be, there’ll be people who say, no, we demand that every person will be able to have their own UTXO. And there could also be, as, as you rightly were saying, there is a even in that in-between like, let me walk back a second. The concern is more that not everyone on earth of the 8 billion of us can have a UTXO, literally just physically cannot happen. And so even if we did say everyone’s on channel factories, then you might be in a situation where all your funds are hot. All your money is hot. Like your life savings is hot funds on a phone or on something. And so you could maybe there would be an argument there around that. I don’t know maybe, but I also think there’ll just be a lot of people using custodial. So but I guess that’s a, that’s an argument to be had in like 10 years time or something.

Rusty Russell:

Oh yeah. Look, and our job Stephan is to make sure that the ramp down. So if you want to come custodial to like more, self-sovereign some of that to make that smooth and gentle a transition as possible, right? The more people that we can get called or you can hold her and stuff, his here’s an easy way of doing it looking for the great trade offs, right? Where we can make it safer. That’s everything custodial, but not like color of broken glass kind of painful to do. Is it, that is the Bitcoin battle, right? To get people to actually use it not just hold it in some indirect sense, but to actually be have Bitcoin have the keys is, is I think the defining Bitcoin battle, if we fail at that, then we haven’t won, right?

Rusty Russell:

If we don’t actually have people controlling around Bitcoin you know, we’ve got some nice monetary properties, perhaps although those can then be raided by the custody or those going to be raised by the custodians as well. So we haven’t really achieved unless we’ve got a significant portion of people who actually holding Bitcoin as such. So and I think, again, this is an argument we’re going to have, there’s a lot of nuance around this, right? There’s no, obviously correct answer. But there’s going to have a gradiation of different, of different answers, I think.

Stephan Livera:

Right? Yeah. So it’ll be interesting to see how that happens. Who knows. Maybe there’ll be some other technology that comes out and sort of helps in some way with all of this, but I think probably a good spot to finish up here, Rusty. So for any listeners who want, who want to help out, or what sort of feedback you’re looking for on offers and how can anyone get involved?

Rusty Russell:

Right. So the Bolt12.org is the kind of go-to place for stuff, and I’ll be gathering resources there. It has a link to the text of the spec is not that unreadable, right? If you’re a technical person, you can already do that. Oh, cool. That makes sense. I always welcome questions. I’m pretty accessible on Twitter. My email is pretty, well-known Rusty@blockstream.com. @Rusty_twit on Twitter. Reach out to me any questions and if you’re a wallet dev or something like that, then please definitely reach out to me and ping me and talk to me about your interest in everything else. I’m thinking about actually running a series of seminars on Bolt12 to actually run people through the technical stuff, right? If they’re there, what does, they’re kind of interested? What do they have to do? Like, so I want to do Bolt 12. How do I do it? Right. What steps do I need and stuff like that. So I’m looking at maybe doing that, that in a few weeks time and just, yeah, some live, live interaction with people on the, on the questions and stuff like that. Bit of a review club football 12. It will be useful too.

Stephan Livera:

Fantastic. Well, I enjoyed chatting with you Rusty as always. So thanks for joining me.

Rusty Russell:

Thank you, Stephan.

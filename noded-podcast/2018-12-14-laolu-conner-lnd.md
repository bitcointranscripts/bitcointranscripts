---
title: Lightning Labs and LND
transcript_by: Michael Folkson
tags:
  - lightning
  - lnd
speakers:
  - Olaoluwa Osuntokun
  - Conner Fromknecht
date: 2018-12-14
episode: 36
media: https://noded.org/podcast/noded-0360-with-olaoluwa-osuntokun-and-conner-fromknecht/
---
<https://twitter.com/kanzure/status/1089187758931890178>


Pierre: Welcome to the Noded Bitcoin podcast. This is episode 36. We’re joined with Laolu and Conner from Lightning Labs as well as my co-host Michael Goldstein. How’s it going guys?

roasbeef: Not bad

Pierre: So I listened to Laolu on Stephan Livera’s podcast and I would encourage any of our listeners to go listen to that first so that they can hear all about some of the latest developments in lightning. I remember you covered AMP and various other topics including Neutrino. I’ll try not to bring those topics up although we can maybe go deeper on them. We’ll try to cover some new ground. What I feel like was not covered in the Stephan Livera interview was Laolu’s background, his software engineering career and what led him to his end… obviously the same for you Conner. Your involvement in lightning. Let’s start off with that. Where did you guys go to college?

roasbeef: I went to school at UC Santa Barbara (UCSB).

bitconner: I went to MIT. Started there for undergrad and then did my Masters there too.

roasbeef: Yeah I did the same thing at UCSB.

Pierre: And what were your Masters in?

roasbeef: Mine was in applied cryptography. I ended up working in symmetric search, like encrypted search. How to make the index and use symmetric crypto on it to have an index that provides privacy… information retrieval on top of it.

Pierre: Awesome. What year was this in?

roasbeef: This for me was 2015, 2016 my Masters degree. It was kind of like a five year thing, overlapping junior year and senior year. There was a lot of craziness but I got out of there.

Pierre: So were you already involved with Bitcoin when you were in grad school?

roasbeef: Yes. At that point I’d started to do Bitcoin development already. I’d met people doing internships in San Francisco, at Bitcoin Devs meetups here in SF. I wasn’t as heavily involved. My year of grad school is when I started working on Lightning actually. That’s when I wrote the Sphinx implementation which is onion routing in Lightning. I started doing stuff for the mailing list, things like that. At that point I was getting more and more involved. I was like “I’m ready to do this vs anything else. So let me go all in.”

Pierre: What got you interested in Lightning and Bitcoin in general?

roasbeef: For me, initially I remember I was taking this wireless networking course  focusing on things like gradient networking, wire piping things like that. There was a course where we were talking about vehicular mobile adhoc networks. I had this idea. What if you could use Bitcoin to pay these cars to do passerby or whatever or pay to get into toll gates? I started working on payment channels at that point but I didn’t really know enough yet to make the situation worthwhile. I was working on something similar to duplex where you’ve got two different payment channels in either direction. The paper came out in 2014, 2015 and I was like “this is way better than what I’m working on, let me just scrap this, read this and go meet these people in SF”. I met Joseph, Tadge and everyone else in SF during meetups and it went from there. I was like “this is better than I’m working on, let me go work with these people”.

Pierre: Awesome. Just had to set aside your ego.

roasbeef: I was like “let me throw my shit out”. This is way better. My code wasn’t even that great at that point. I didn’t know what to next. I didn’t have the entire Bitcoin programming model in my head yet. So I couldn’t really progress. Over time I did more and more small stuff so I had that to do large projects in Bitcoin at that point.

Pierre: Ethereum was growing at that time. What made it so that you weren’t interested in working on Ethereum scaling or Ethereum related projects?

roasbeef: I think it was just way too early then. At that point I was dubious if it would go forth. I didn’t really want to be involved in the token sale or whatever else. The main thing was that I went to these Bitcoin meetups in SF, they were like 20th and Mission. I was doing internships at Google at that point and they were actually every week, that was the cool thing. I met people every single week. I met bluematt for the first time, I met a bunch of other developers. Me being able to talk to them at those meetups would help me accelerate my progress in Bitcoin because you can actually ask questions versus trolling on IRC or something. That made a big difference.

bitconner: The other thing at the time was that Ethereum was ramping up right around the time Scaling Bitcoin started. For me, I had been tracking Bitcoin for a long time even up to that point but I was really starting to get down into the nitty gritty of what issues we were facing and what tradeoffs. After really internalizing what in theory sounded like a great idea, when you actually look at the fundamental tradeoffs, this is going to be in no way better in terms of scalability than what we already have. In fact it goes in the opposite direction. I remember the choice was like how do you optimize what is already slim, robust and powerful and make that…

Pierre: Do you want to elaborate on what the fundamental tradeoffs of Bitcoin because I think this often goes undiscussed?

bitconner: I think at the end of the day it’s like you can always trade what I call instantaneous scalability for long term scalability. Normally this is mostly a reference to initial block download versus TPS. You can tune any blockchain to have more TPS instantaneously but that adds up because it is like the integral of all these blocks basically in terms of the amount of storage you need for these nodes and the amount of bandwidth to download across them and CPU time. Really Bitcoin was going in the right direction in terms of making those tradeoffs which is why to this day I still love and am passionate about this project because I think a lot of the people in this space share those values. I think that’s probably the gist of the tradeoffs at least in terms of the scalability debates.

roasbeef: Tadge had this thing, it was kind of his bathtub. On one side everybody could verify it with a blockchain with no throughput and once the blockchain got super massive there were only a few people who could verify it. There were a bunch of nuances in terms of the security model which aren’t as highlighted or enumerated. People say this is equivalent but it’s like it’s not really equivalent because you have all these additional assumptions on top of the base assumptions for Bitcoin itself. Referring back to the other thing, Conner and I actually met at Scaling Bitcoin, Hong Kong.

bitconner: No, Montreal, the first one. I met you and Elizabeth there.

Pierre: On that note Conner, how did you end up in Montreal, what was your backstory before that?

bitconner: I got into Bitcoin 2012ish and started learning about it a lot more. I was on Reddit every single day just like learning as much as I could. I studied it for a long time in college and ended up doing my Masters in decentralized systems and applied cryptography. My thesis was on decentralized public key infrastructures. I had been really ramping up and exploring what you could actually do with Bitcoin, blockchain technology but also keeping in mind the tradeoffs I had been learning about through mostly Reddit at the time. I really started to ramp up my deeper understanding when I got talking to people at Scaling Bitcoin. The way I ended up there was the DCI a week before the first conference was like “Hey would you like to go up to Montreal to this conference because I’d got involved in the Bitcoin club and DCI”. They sent me up there on short notice and I had a great time, met a lot of people, met Laolu. I really got into the crux of what the huge debate and tradeoffs were.

roasbeef: I think Montreal was interesting because it was the first time many people met anybody else. I met Gavin, sipa, sipa wasn’t there but a bunch of other people at that point in hallway discussions. I was like “wow people exist”.

bitconner: One of the big takeaways is that’s nice to put an IRC handle to someone’s face

roasbeef: People aren’t dicks in person

Pierre: I definitely agree with that sentiment because we know a bunch of people on Twitter and it is always completely different when you meet them in person. Your interactions with them afterwards are different as well now you’ve met in person.

bitstein: The nametags need to have the Twitter avatar on it. Even more than people’s handles, it’s the avatar you know people by.

roasbeef: When you’re scrolling you detect the avatar very quickly. You scan it and you’re like what’s that? I haven’t changed mine for a bit now.

Pierre: So Conner, with your discussions in Montreal, what made you decide that Lighting was an exciting project to work on?

bitconner: It just became quickly apparent that due to those limitations, stuffing more transactions onchain, even if you can optimize the size of a transaction, something like that, is never going to be the best you can do in terms of scalability. In my opinion, the way you get these things to scale is to not think about every transaction onchain as one transaction. That single transaction onchain needs to represent hundreds, thousands, millions of offchain transactions. To some extent exchanges do this, they batch a bunch of trades and people withdrawing and depositing. Lighting works in a similar way where you have your balance and then you make a bunch of offchain transactions that could correspond to a couple of thousand real time, in meatspace transactions. Then you settle back to the chain with only a single transaction. In that case, the transaction is like 500 bytes but it is now a thousand transactions that are enabled in meatspace. You’re talking like sub-byte transactions when you amortize that.

Pierre: You’ll hear people go even further than that and turn it into a criticism that all the transactions are going to be on Lightning, all the payments are going to be on Lightning and so there’s not going to be any onchain transactions at all. The blocks will not continue to be produced. What do you guys make of that?

roasbeef: I think that’s incorrect.

bitconner: There’s still a market for block space.

roasbeef: People are still going to be opening and closing channels. We’ll have things like splicing. There will be other cool protocols you can do as far as HTLC encrypt and things like that. At the end of the day, if lightning is successful you will have more activity on Bitcoin than ever before. There maybe new users to Bitcoin that are drawn in because of Lightning. All of a sudden they can do something new with their coins they couldn’t do beforehand. It could be the case that there is now even more activity, more total transactions in the system itself.

Pierre: In the long run you don’t think that the lightning network could become perfectly circular in its flows which would make it such that there are no new coins that need to be added.

roasbeef: I think it will get there but at some point merchants are going to want to withdraw to cold storage or going the other way. I think there always will be inflows and outflows at the on and offchain layer.

bitconner: I think you can establish a fairly central core that doesn’t need to leave the network but there will definitely be flows that are unidirectional as well in terms of total aggregate payments. So those will need to be recycled some way whether it is offchain, onchain it is unclear. It will strike a balance for how to do that because if everyone does move lightning and block space is totally empty why not just make an onchain transaction if it’s so cheap? Those things balance out to some equilibrium.

roasbeef: When you start to do more involved batching you can open and close more channels with a single transaction. One transaction can open 50 channels and maybe close 2 of them. I think people will get more and more efficient with their space as well in the future. With a transaction, I actually did twenty things on the network and then I move on, I’m done for the day.

Pierre: On the other end of the spectrum in terms of criticism, it’s like what if Laolu is right and this creates even more demand for transactions onchain? We have a block weight limit so there’s no way everyone can get onboarded onto Lightning because look at these calculations that I made. What do you make of that?

roasbeef: There will always be limitations at the base layer but maybe in the future people can have different things like dynamic block sizes where you have a mechanism that can update itself programmatically. Even then if you’re working towards slightly different trust models there are ways where you can create channels offchain rather than just onchain. I gave a talk about this at Scaling Bitcoin. We have some ideas on this different trust model where you allow people to create channels offchain so you can onboard people onto Lightning without having onchain transactions. In the end I think in the future there will be some sort of dynamic block size. There will always be a limitation. You can’t just crank it to a 11 and think there’s no consequences.

bitconner: At the end of the day, if you’ve already squeezed out all the performance you can get via Lightning and there’s still a constraint at the base layer, that could maybe be justification for making other decisions around block size. The wrong thing in my opinion would be to increase the block size because there’s pressure now and not build out the technology that could relieve that. If you’ve already built that out and there’s still issues down the road that’s more justification to pursue that. I think we’re quite a way off on that front.

roasbeef: Or sidechains or something.

bitconner: At that point you’re not also storing those transactions that you let in just to relieve the pressure. That would’ve grown the database much faster than the rate at which it is now.

roasbeef: My node has probably done 2 or 3000 transactions, updates etc. That wasn’t onchain, no-one knew about that. That was pretty dope.

bitconner: I asked Alex to tell us how many channel updates Y’alls had done and it was almost 400,000.

Pierre: Maybe we can get it to a million with this node launcher I’ve been getting people onboarded to. We can increase the amount of load on Alex’s server. He doesn’t share any of that money with Lightning Labs right? All of that Y’alls money goes directly into his back pocket.

roasbeef: Yeah he’s the CEO of Y’alls, he handles that.

Pierre: Maybe he’ll help out Lightning Labs with some funding in the future. It is going to be a giant media empire, bigger than Reddit. Michael - did you have some questions? I was going to look at the audience questions.

bitstein: We do have some good audience questions. I think go down some of the list. There’s one from BillyBTC. How often can we expect additions to be made to the Lightning Network BOLT specifications and how likely is it for BOLTs, current or future, to change after being accepted?

Pierre: Do you guys want to explain what BOLTs are -BOLT 1.0 and then 1.1 now?

bitconner: The BOLT specification is a collaborative effort by primarily Blockstream, ACINQ and Lighting Labs. There’s other people too. Matt Corallo is pretty heavily involved. There’s a group called ptarmigan that’s starting to work on it as well. So really it is a collaborative place for us to write down in detail how these protocols should interact with each other. That gives you a base to go off in terms of what can I expect from my peers? How should I be sending messages, formatting them, all those things. Really that just minimally defines the actual interface between two nodes. It tells you nothing about how to actually build these on the back end. There’s a lot of gaps you’ve got to fill on that front. It sort of defines this minimal intersection of how do we need to communicate with each other in order to accomplish this task say opening a channel or sending a payment. In my experience in the last year and a half, BOLTs get updated fairly frequently either just because we realize there are edge cases that we should account for, document and specify. There’s some slight improvements that we think we can make. I think down the road some of them will solidify quite a bit. Some of them are pretty solidified as is. The transport mechanism BOLT. There are parts of it that are ossified, in a good way because we haven’t had a need to change them. Overall I’d say there’s definitely more to come because there’s a lot of new features and it would be nice to start adding those as standalone documents.

roasbeef: We’ve basically been modifying these ones rather than making new documents. I think that’s because it is in Git and it’s pretty easy for us to modify something. Most of the changes that were in 1.0 were things that we realized were issues when we were trying to do implementations. You have the spec but once you start to do the implementations yourself on the live network you figure out that fees can be a pain or there’s a problem vector or we should be using encrypted… or something like that. They are added on after the fact. Now we have BOLT 1.1 coming out which is going to be the next version. One thing we said in 1.1 was that it wasn’t going to include any soft forks. It is meant to be a more immediate thing. Things around dual funding, splicing, things like that. BOLT 2.0 or 1.2 will maybe have soft forks like taproot or whatever else. That maybe more radically redesigned, more of the protocol. This is more of an incremental step, a bunch of cool things like AMP will really make a big difference before we start rolling stuff out in 2019.

bitstein: In Bitcoin, there’s this feeling of over time we do want to ossify the protocol. Maybe there will be additional things but we want something that’s here to stay for the next thousand years or whatever. Do you think Lightning is going to have a similar trajectory or do you think it’s going to always continue to have that fast paced new features and all of that?

bitconner: I think there’s a pretty good likelihood for the near future that it will continue to be a very fast paced development cycle just because there are a number of things in the protocol where we know today that this can be better. Either they’re enabled by soft forks in the future or we can do them now. The protocol we have right now is working with today’s Bitcoin but as Bitcoin continues to evolve and opens up new doors we’ll continue to update the Lightning protocol to take advantage of those features as well. I don’t foresee it ossifying any time soon. Even the basic mechanics of getting a preimage for a payment hash is likely to change in the future because you’ll probably get a secret key to a pubkey when we move to…correlation and Schnorr based scriptless script channels. Even the most basic fundamental piece of Lightning itself today is probably going to be modified in the future.

roasbeef: We can be a lot more nimble because we don’t really require global consensus or global updates because I update my node and you update your node. But one example is something like AMP. We can do this today without modifying anything because it’s a purely end-to-end protocol. We have a bunch of little hooks in there that we can do to… a lot more quickly. But even beyond that because there’s the network layer and onion routing things like that, many things are decoupled from Bitcoin itself. We have a lot of researchers working on different routing protocols and whatever else that can be implemented without any changes in Bitcoin. We can move more quickly because we don’t require global upgrading. But there are some upgrades that will modify or restrict your actual set of possible paths. If we move to Schnorr for HTLCs then at that point, every single person in the path needs to have that update. But there could be a flag where people support both and later on they only support one of them. The most aggressive upgrade is like a slow motion soft fork in Lightning.

bitstein: So that would basically be I have my node open and I have decided to support both types of signatures but over x amount of time I just notice the network traffic for the one type of signature has gone to close enough to zero so it’s not worth it anymore for me to have it. Therefore I then move to Schnorr only.

bitconner: There will be an incentive to do that as well because the Schnorr based or ECDSA scriptless script variants will actually induce smaller fees onchain. The witnesses you need are smaller. The witnesses and scripts are quite a bit smaller. There is a financial incentive for people to upgrade as well so that’s kind of nice.

roasbeef: The other thing is that in future it will be even more of a thing where you can blend in with the rest of the anonymity set of the actual chain. If everyone is using taproot… In the normal case I just have a… key. At that point a channel open and a channel close don’t look like anything different versus a regular payment onchain which I think is pretty cool.

Pierre: Awesome. We’ve another question here which I also would have this question from Matthew R. He was really enjoying the history, we got up to Scaling Bitcoin Montreal, he would love to hear more; when they met and what led to them starting working at Lightning Labs and the story of Lightning Labs up until now.

roasbeef: I guess it was after Scaling Bitcoin, Hong Kong in December I met and hung a lot more with Joseph, Elizabeth and Tadge. I was really interested in working on this stuff. At that point I was interning at Google and at one point I was deciding which of them I wanted to do: Google and be there full time or go to Bitcoin instead. I had Google FOMO as I’d miss everything internally at Google. Eventually I had more and more… well I’m never going to be able to do this again so I have to go forwards with this thing. Lightning Labs was created in 2016 or so and at that point I ended up graduating at UCSB and I started working that summer. We eventually got Conner onboard in 2017. He was working on some other project at that time. We talked him up enticing him to join the company and then we got him on at that point. I probably skipped some details in between. That’s kind of like the timeline. I was hanging out with Joseph, Tadge and Elizabeth Stark more and more during the summer. They really convinced me that this was something I was going to be able to do and I felt that this was the opportunity to do so especially given I was fresh out of school and if it failed I’d just go back to Google and have a cushy job.

Pierre: That explains why you have so many Google related technologies in lnd whether it’s Go, protobufs, gRPC.

bitstein: If I remember correctly, the idea of macaroons also had come from Google hadn’t it? Or was it Mozilla?

roasbeef: They published the paper. They actually use macaroons a lot under the seam with things like Gmail in place of cookies. Whenever you share something on Google Photos you basically give access to an album. You give a macaroon for that album that can access anything else.

bitstein: Can you explain macaroons to the audience and also what is that used for in Lightning?

roasbeef: They say they are cookies but better. A macaroon is like an authentication token. It is kind of like a bearer credential and the main thing is its capabilities. It can act as a control…. ACL which uses a list of users where Bob can action directly y and do whatever else. Instead a macaroon gives you the actual credential to say “Hey you can access this thing”. Think about it like a private key. A private key is kind of like a bearer credential, you have a private key to access your funds. A macaroon is kind of like the same thing. They are pretty simple in their design because they’re based on this HMAC. You have this root key and from that root key you derive the macaroon. You can do things like take a macaroon and make it more restrictive. I can give you something that says “you can read this directory at 2pm every day”. You can also pass them on. Let’s say I want to give the application only access to my graph data, I’d get a macaroon to go act as one particular call. Even further than that, I could say you go act as the data of all of the edges. Basically, the uses in lnd are authentication on the RPC system because they’re pretty flexible. The main thing is you can have a system running lnd, give each component the minimal amount of permission it needs to accomplish its task. With the payment server, we have an invoice macaroon that lets it make invoices, list transactions, maybe make new addresses but it can’t do anything else. This lets you do cool things in your application that is pretty secure. One thing I’ve seen is Joule. With Joule you give it its macaroon and right now it takes everything when in the future it can be a lot more granular. In the future it could give every single site their own macaroon. Every single site has a macaroon in local storage. Because of that the macaroon ensures the website only does 2 BTC a day or a different time of day. The other cool thing is that you can revoke the macaroon at any given time. Now every single website has a very specific macaroon. You can ensure you have the capabilities parallel for everything else. You can also revoke those pretty easily. I think it is a pretty cool model unlike MetaMask which gives them everything. This basically says you can make a transaction up to 10,000 satoshis once a day only to these endpoints. It is a pretty cool thing as far as authentication within lnd. Right now we have three macaroons; we have the admin, read-only and invoice. Later on we’re going to have this thing called macaroon bakery so you can make custom macaroons or “bake” custom macaroons. This will basically let you do anything. I need a macaroon that says you can access the thing at 10pm over localhost only with these two calls and at most 2%.

bitstein: Extremely granular.

roasbeef: Yeah super, super granular.

bitconner: One thing as well is that they’re also hierarchical. If I have a read macaroon I can hand out or sub-delegate even granular tasks on my own. I don’t need the original person. If I have the read one I’m allowed to read anything but if I have microservices that only need to access certain things I can be like you can read the channel graph, you can read channel balance, you can read this. Those subsystems can continue to do the same thing. You can really lock down your permissions quite nicely.

roasbeef: It is kind of like a Merkle tree. You can basically never go back up once you have a macaroon to make it more powerful but you can trade it more and more as you go down.

bitstein: So is this something that can also be used in lieu of things like API keys? Because your API keys when you get it, you get the full range of stuff.

bitconner: They’re like API keys but with cryptography behind them and permissions.

roasbeef: Let’s say I have some API that’s maybe doing translation of a language or something like that. I could send the payment over Lightning and the preimage is the macaroon all of a sudden. Now I have the receipt, you send the invoice to me. The cool thing about that is now you don’t know who actually paid for that API key. You can present that to the service and they can use that as regular authentication to move forward. That’s a really cool loop made with the Lightning API, that’s the power of our micropayments.

bitstein: That’s really awesome. I was introduced to the idea of macaroons back in 2016 because someone was working on this project of using macaroons to control access to a Git repository. You might be able to read one branch, write to another branch etc etc. I thought that was really cool. Perhaps there’s some Lightning thing you can do there to help pay for various open source software. At the time there was not nearly as much infrastructure to be playing with.

roasbeef: The library that we use is part of a standard. If anyone has a JS library, they use the exact same standard for the macaroon. They can also… and validate them which is pretty cool.

bitstein: What is this library?

roasbeef: The one we use is called go-macaroons. There’s a macaroon mailing list where they talk about different standards in terms of serialization, how to do validation, things like that.

bitconner: Macaroon wizards?

roasbeef: If you read the paper, it is very close to this in the paper. It gives a pretty good overview. It is really in depth but it is pretty cool to see how it is being used. It is a very powerful credential based system. The main thing is the least authority principle. You should only have the authorities that you need minimally to complete a task which helps restrict capabilities of particular servers. If a payment server gets popped, it can’t really drain all your funds because it can only get invoices and nothing else which is pretty cool from a security standpoint.

Pierre: I feel like every layer and every little subcomponent of the Lightning project broadly speaking, every little part has a huge amount of runway for improvements. A long list of to dos and really awesome features that are going to get developed over the coming years. It is very exciting. It shows that there’s room for a lot of developers to come in. Do you guys want to talk about the developer pipeline?

roasbeef: There’s a bunch of different levels. Obviously there’s protocol level which requires you to have a lot more advanced Bitcoin knowledge and protocol knowledge. There’s also a lot of things like lnd itself. You could look at our issues on GitHub, there’s a beginner tag. There’s things like add a RPC call or maybe people want to pass their pubkey in this call or whatever else. Even those are a big help because there’s a lot of other tasks to do and once you do those you can continue to do larger and larger tasks, kind of like level up in a sense. Be more of a potential contributor. We’ve had people that started on very small tasks and eventually we hired them. This guy’s really killing it.

bitconner: It is a really good way to get involved with the codebase too. The codebase at this point is pretty huge on its own. There’s a lot to navigate and there’s lots of intricacies, nuances, stuff like that. Doing that is a really good way to dip your feet in and start interacting with us, get feedback on coding style, all these things. It’s onwards and upwards from there.

roasbeef: There’s other tools that people are building as well which are really important. People are building different front ends like the node launcher for example or people are building their own things like rebalancing scripts where you have something that does rebalancing. The cool thing with that is that I can make a macaroon for a rebalancer that says that you can send payments but they must start and end at A. All of a sudden they can’t be sent anywhere else so I can have a very fine-grained compartmentalized capabilities for them. A bunch of different tools people are making, a bunch of different apps, mobile games and Unity plugins. There’s a tonne of developer activity, it’s impressive, it’s hard to keep up because I see new shit everyday which is pretty dope.

Pierre: I think that part of the credit for that goes to the really nice gRPC API setup. This is the first time that I had used gRPC but basically it allows you to autogenerate client and server code based off a specification. As someone, I’m not a Golang person, I’m like a Python person and it was really easy to get started with the API. I think that has been the experience of a lot of developers, whether it’s like Javascript of whatever other language is supported by gRPC.

bitconner: I think there’s like ten of them. Ten or eleven.

roasbeef: There’s one for OCaml. It’s not officially supported but someone just made one.

bitconner: I really love gRPC because it really decouples what we feel like is best for developing our software in from what you end up wanting to use it in. Or just more of a microservices architecture and setting it up so lnd is a control plain for your money. It can be accessed however you want to using the same macaroon certificate approach on all those infrastructures.

roasbeef: One of the cool things about gRPC is that you can embed directly in your business logic. I’m doing my payment site and they’re all fully integrated, it’s like a normal Python object. We also have pretty good documentation. We had an intern last year, Max Fang, shout out to Max Fang for making the docs. That’s api.lightning.community. That’s pretty cool rendering. We also have… anytime we push to Git to modify the proto files, our generation rerenders that automatically which is pretty dope. Shout out to Wilmer for writing that.

bitconner: Another thing that’s really cool also is the idea of wrapping the RPC protocol. You could have someone that wraps the RPC so you don’t have to deal with the raw RPC calls but it looks like a native library. That’s something that the community could help build out. You could have one for Go that does streaming updates and just sends the updates over the channel. I started working on this at one point but there’s too much stuff to do so I never finished it.

roasbeef: There’s lightingj which is kind of like that. It is like a higher level Java integration.

bitconner: …. has LN service that is like Javascript.

roasbeef: I think it wraps….

bitconner: I think that would be really cool because working with gRPC is a little verbose.

roasbeef: In Go but maybe in other languages.

bitconner: Getting that wrapped up really nicely, people would want to work on projects, I think it would be really interesting too.

roasbeef: A bigger thing is that you can get really good streaming updates which I think is pretty important. Whenever you create something with Lightning you want to have that very, very fast callback to rerender the UI which is a really big part of the user experience. Whenever you have anything like a callback or sending over… , you can have very good streaming support for notifications.

bitconner: We would like to eliminate all uses of long polling especially from the… because you feel the lag as a user. You push the button and a second later it updates. It’s like what? It should be responsive.

roasbeef: The best thing is when people do those side by side demos like Y’alls. You click it and Y’alls opens before the app which shows how quick it can be in the best case.

Pierre: How do you guys balance your time between helping people get on the Lightning Network and helping them with bugs that they’re experiencing versus developing the future?

roasbeef: It can be a difficult balancing act. Early on we invested a lot in developer community on our Slack. We can educate the first ten or twenty people and they will go themselves to educate more users. Initially I would wake up and there would be hundreds of Slack messages, I would reply to all of them. Now I wake up and most of them are responded to because there are people in the community now that know a lot of stuff themselves. When we went to Berlin Hack Day in Germany, the knowledge I thought was insane.

bitconner: That was one of my favorite events.

roasbeef: They were asking really good questions. I was like “wow these guys have learnt all this knowledge and caught up super quickly”. I thought that was really impressive. I think it is one of those things where the community gives within itself and grows because everyone wants to have more knowledge. We also have a lot more contributors on GitHub doing like issues or helping review or whatever else.

bitconner: Overall I’ve been really impressive with the quality of the conversations and the help on the Slack. I think the Slack is approaching 3000?

roasbeef: I think it’s past 3000. Maybe it is almost 4000 devs now.

bitconner: There’s a lot of people there. There’s probably someone who has had your issue or knows what to do or is keeping up. Issues can be kind of tough. Sometimes you’ve got to balance… you’ve got to really apply a prioritization strategy. All our issues are tagged with P1 through P4. Is this a critical bug or a really obscure edge case?

roasbeef: Our lowest tier is P4 which is “noted”.

bitconner: Then also in addition to that, the number of contributors is going up. There are probably like five core people that are employed by Lightning Labs that work on lnd. We’re starting to see, especially in the last four or five months, a lot of new contributors that regularly contribute, review and help with all those things. It’s really exciting to see that pick up as well.

roasbeef: The other thing is that with a PR, we can be slow sometimes because there’s a lot of things you rely on like a PR is difficult to review or if it has the proper testing. We’re not as slow as bitcoind but they’re slow with good reason because of the level of security.

bitconner: To some extent too, we have a goal to keep our number of issues under 100.

roasbeef: It’s 162 right now.

bitconner: That was the goal. Now it’s up to 160. That’s not because the review is slowing down, it’s because aggregate bandwidth is increasing. There is a lot of turnover, we do get a lot of stuff reviewed and merged.

roasbeef: The other thing is that some of the issues are future requests or they’re issues by us requesting things. In terms of like bugs, bugs are maybe 10-20% of the issues.

Pierre: How are going to scale up the developer involvement from here to go 10x, to attack all these features?

bitconner: Get more people excited.

roasbeef: I think that comes with developers stepping up to be contributors and doing more substantial work. Maybe they need a feature in lnd for their application or they’re scratching their own itch which is something we see a lot. Someone is like I’m writing a mobile application, I need to control the exponential backup for connecting peers, they can add that in. Obviously there are growing pains as far as too many PRs or whatever else. Right now, PRs are growing by a good bit. I think maybe we’ll hunker down and review these things, release and close out.

bitconner: There are some PRs which are made against super old versions of lnd where that subsystem might not even exist anymore.

roasbeef: There are some from like March 2017 that are just sitting there. Maybe I’ll post or just close it.

Pierre: We talked about the massive growth in developers and people building applications with lnd. As far as the users, do you feel that lnd is mature enough now to have way more users than it currently has or do you want to see that continuing to grow at the same pace as the software matures.

roasbeef: I think the userbase is growing as fast as we’re getting cool applications that people are using a lot. For example, there’s a site called Microservice Task on lnd, I can’t remember the name of it. They’re seeing a bunch flying off the shelf very quickly. I feel that one of the big things that will reach the users of lnd once we get there, is making Neutrino mainnet which is hopefully early next year.

bitconner: Two weeks.

roasbeef: At that point you don’t need 100 GB to spin up your node. We’re actually getting the sync time very fast. Right now, if you have an ok internet connection it can take one or two minutes on mainnet. It’s basically you click it, you walk away, you’re back and boom you’re set.

bitconner: Or by the time you write down your seed which is what you should be doing.

roasbeef: That’s one of our goals. Basically by the time you’ve finished writing down your seed, lnd should be synced, ready with Neutrino. I think we’re pretty close on that.

Pierre: Awesome

bitconner: We were in Japan doing some tests. We’d get on the Airbnb wifi and Laolu would be like “what’s the speed?”.

roasbeef: From Australia which has the craziest ping time.

bitconner: We were also hitting SF servers so that round trip was like…. I see what Rusty has to deal with all the time and it’s amazing he’s still able to make Hangouts.

Pierre: I was surprised that our Hangout with the c-lightning worked out so well. They had surprisingly good internet quality and it’s better than Michael’s in Austin.

roasbeef: I have really bad internet in SF. I have like 3MB data in SF. I come from the office and upload binaries because otherwise it takes forever.

Pierre: It’s funny too because in my view after spending the last couple of weeks helping people sync their full Bitcoin node, bandwidth is a major constraint. I think there’s a lot of improvements that will be made there. I’ve got fiber installed recently and that allows me to do initial block download which is constrained by my hardware, not by my bandwidth. For most other people, you’re seeing a 3MB download, that’s going to be a bandwidth constraint not a hardware constraint for the initial sync. As fiber gets deployed more widely, I think it will become more palatable to do a block weight limit increase but until then stick to building on offchain.

bitconner: On top of that, latency is also a pretty big killer too because if you’re saturating your bandwidth there’s probably no amount of optimization you can do past that point. You’re kind of stuck but if latency is your issue that just means you need to do more pipelining, more everything else. That’s like an algorithmic thing that’s for the most part solvable. Then if you’re saturating your bandwidth now you’re running into issues. That can be a real killer if every round trip you’re doing half a million of these to sync the blockchain and every one is half a second. That’s a killer

Pierre: Another big question that I’ve been getting asked a lot is about Tor and using your lnd node with Tor so that your external IP address is a Tor address and you don’t have to deal with any concerns about exposing your home IP address to the public internet. I tried setting it up and I got it sort of set up for Bitcoin Core but it seems like a pretty involved process right now. Is it the case that for people at home, maybe you shouldn’t need to expose your external IP and you should be able to run it privately? If you have no ambition of routing payments for everyone else so it’s ok to not be public. Is that a good read on that or am I missing something?

bitconner: It really depends on your use case. You can also do Tor in outbound or inbound. Making Tor on an outbound connection is I’m going to use Tor to connect to someone else and inbound is I’m a hidden service, I want you to connect to me via Tor. lnd supports both at the moment, I think Wilmer did that integration. When he made that PR and I tested it out, it’s pretty much as simple as running the Tor daemon and then starting lnd.

roasbeef: lnd is pretty easy because we do make it plug and play. If Tor is active and you have the flags set, it will do everything for you manually. If you’re doing more advanced stuff, you may need to reconfigure Tor itself. I think bitcoind has that as well but up to Tor v2 whereas Tor v3 is a different version of the protocol that has better crypto involved in it. The cool thing is that for the Neutrino one, if you run Neutrino with Tor it makes sure all that traffic is… over Tor 2. I think it is a big deal because one of the things as well is that... get past NAT traversals, some people may not have a static IP for accepting inbound connections from the network. Whereas if you have a Tor service, people can connect to you over Tor which is good because you can have more connections with the network, make sure things are more robust.

Pierre: If you’re trying to receive a payment do you need to expose your external IP or can you just have a route hint in the payment request which makes it such that you’ll receive the payment anyway.

bitconner: The only person that needs to know your IP is all your direct peers. Someone else connecting who wants to send a payment to you, if it’s like a routed payment, they don’t need to know your IP, they just need to know your pubkey and the nodes will figure it out. It’s only the nodes that you immediately connect to that may need to know your IP because if you’re a private, unadvertised node which means all of your channels are unadvertised then you may not have a public IP that people can connect to. When you make a connection on the first time to this node they only see the inbound port basically. They don’t have an address to dial you back at, you can only connect to them. For certain applications like a mobile phone or if you want your node at home to be more private you can do that, they’ll still have your IP but they won’t be able to connect back to you.

Pierre: Gotcha. Is Tor possible on mobile?

bitconner: I’ve heard rumors that there’s some iOS ways to do Tor.

roasbeef: It’s possible on mobile.

bitconner: I don’t know how easy it is to bundle in with the daemon as well.

roasbeef: There’s two aspects. One you can use a Tor wrapper native to that platform like on iOS or you can embed the Tor daemon in a Go package with a little bit more room for building. It’s possible.

bitconner: Alternatively we can build out HORNET and that can be used as an anonymous protocol and we’re done.

roasbeef: It’s possible as well. Likely a later version will have that more advanced future for users. It’s possible.

Pierre: Let’s take another question from our audience here. This one is a common question because in other parts of “crypto world” there are altcoins where you can do staking and then you get a percentage revenue from staking. People have projected this onto Bitcoin, onto Lightning Network where you’re going to be able to do staking with Lightning Network and then you’ll get a return from routing payments. So the question is, will collecting fees provide enough incentive for others to set up Lightning Network nodes or will they be too negligible and inconsistent to matter?

roasbeef: I’d say it depends. I think right now there are a few nodes earning because they’re a little more educated in terms of where to open the channels and good at managing channels. It’s not really the case where we can open channels, set and forget and be earning good revenue. Maybe… earns enough every month to pay for Netflix which is a pretty good benchmark. Right now, the velocity of payments in the network isn’t super high right now. There are points where it is idle but there maybe a point in the future where it can’t just stop... every single time. It has to have more and more payments in the network to have more potential to earn revenue. The fee structure is a base fee and a percentage fee. Right now it’s not that mature in terms of the fee market on Lightning itself, people are running with the default fees which is 0.0001%, something like that. Maybe in the future we’ll have more advantages in terms of the nodes, they’re managing it better or rebalancing their channels and it’ll be a little bit more interesting at that point. It’s a little bit too early right now but you have very low entry because anyone can start up a node.

bitconner: It also depends on your costs. If you’re running on Digital Ocean, that’s not free but if you’re running on your Raspberry Pi in your house you have a better shot but even then like Laolu said, you’re going to need some velocity. Then there’s the question of I’m running on a Raspberry Pi, do I want to put enough capital so that I can make non-negligible fees or do I want to put a million dollars on a Raspberry Pi which I do not recommend anyone do. Please do not do that. You’ve got to pick the right trade-off of how much capital I’m putting up, where I’m putting it, what is the stability, reliability of that node and the durability.

roasbeef: I feel like some nodes are over-capitalized in terms of risk, reward. If you have twenty million on the network, the fees aren’t substantial, maybe you should be putting the money elsewhere. That would be a little more balanced. When things are a lot more robust we’ll have a much higher velocity of payments on the network.

bitconner: If Lighting does end up providing more of a streaming interface where you stream payments for an Uber or a movie, your payment velocity will be higher and more consistent. If you get a payday everyday instead of once a month, then fees routing nodes… it’s more consistent and uniform. The volume and the stability of the income may level off and become something you can rely on.

roasbeef: There may be some services you can offer along with your node. For example, you could have a watchtower as well, you could earn some fees every single update. I think other things will arise like that too. It’ll be like a multi-layered thing. You have regular Lightning channels, you have other services, maybe there are other things like different types of matchmaking or whatever else.

bitconner: In that sense, routing is one service you offer if you’re putting up your capital for that. But if you have a watchtower or some other Lightning incentivized protocol then your node will already be online, Lightning compatible and can accept payments, you’re in a position to help bolster that infrastructure.

Pierre: It seems like you’re saying with Alex you can set yourself up to be a big router if you have a service that is popular and that people want to connect to directly.

roasbeef: If you have a service or something that I did back in the day, if you position yourself when new services come up you’re the first channel to establish that service, that’s an early mover advantage. I think right now it is in the state that you need a lot more manual monitoring and updates of your node but in the future we’ll have better tools to reduce the burden on managing your node. Things like having a cool monitoring.. that shows graphs, your channels, you can do analysis on your fee projections and whatever else in the future. All that will come. For now, it is looking at the logs on IRC or Slack.

bitconner: Someone needs to make a version of Lightning Tycoon where you click and drag. This channel is getting bad, tear that down, build a new one.

Pierre: I’m glad you guys are fans of Railroad Tycoon. I played Railroad Tycoon 3 a lot.

bitconner: I’ve been playing Rollercoaster Tycoon.

Pierre: Awesome. So here’s another question. I don’t know if this question makes sense. Is there any risk to the Lightning Network of being brought down by coordinated DDOS attack on Lightning Network nodes.

roasbeef: To attack every single node? You could do the same for Bitcoin perhaps.

bitconner: Almost any internet facing service can suffer from a DDOS attack. It’s not necessarily being inherently specific to Lightning that would cause that. Asymmetric resource usage or something. Sure they probably could I would imagine. I think one thing that would really help with that is general information around routing node people to set up basic anti DOS measures like setting your IP tables on your nodes. Best practices around those will develop. I think rompert had some pretty good tips to set up your node and make it a little more DOS resistant. lnd has some pretty basic DOS measures in it already and that will continue to expand in the next year or so. It is on our book to flush out a full fledged DOS awareness, protection, resource management so the daemon itself can be aware of what resources its using. Bandwidth, CPU all those things. I think it will get harder and harder as time goes on but you can never rule it out because if every Raspberry Pi in the world was suddenly start making requests to one lightning node, there’s nothing you can do about it.

roasbeef: I think we’re dead in the sea. It’s unlikely you take down every single node in the network and that’s why I can diverge channels across different nodes. If the top 100 go down there should be other nodes sitting there waiting to set up channels. As a random operator, you can say if these hundred nodes go down I will have the channel that has the… to send the payment. You can open channels yourself where if the network does go down I will be the person that everyone is counting on, not explicitly but you become last few channels to get back up and make new channels to address those needs.

Pierre: Interesting. So you’re saying the same applies for Bitcoin. Bitcoin has had a lot of acrimony in its past yet we haven’t really seen someone try that kind of attack of DOSing every single Bitcoin node.

roasbeef: Not every node is even listening. I could have a bunch of nodes that are connected amongst themselves that aren’t listening. I can also do things like a private peer that just communicates with a particular node. The only DOS thing that I’ve seen is like Bcash falling over because they can’t handle the load.

bitconner: DOSing themselves

roasbeef: There hasn’t really been any major thing. There have been some misses in the past, some things that could’ve been bad. So far, it’s been pretty robust.

Pierre: It’s funny that on the previous Q&A podcast that Michael and I did. We were hypothesizing this idea of having shadow lightning networks between friends that are essentially a web of trust within the shadows of the Lightning Network.

roasbeef: Exactly. It could be a thing where half my connections are from the open web and the other half are people I actually know on IRC. They make a stronger… in terms of people who I’m exposing IP or hidden service address to.

bitconner: There’s also the possibility that on the public network I could advertise a channel for 1BTC between Laolu and I but then I could actually have eight other private channels between Laolu and I which I’m actually using… so you could actually have a whole shadow channel in a sense too. I use the 1BTC channel to signal routing policies and whatever but I actually have 9BTC bandwidth between us.

Pierre: Interesting, that’s fascinating.

roasbeef: That’s kind of like subnets on the internet or autonomous servers. You’ll see similar things in the future where one node has a whole shadow network that isn’t announced to other people. Or within a organization they have a bunch of private channels to the wider area you expose a few public channels.

bitconner: One of the nice things about that is I’m only advertising one routing policy and every node only needs in essence to have one edge advertised even though there could be three or four channels backing it onchain that don’t need to be advertised. That helps a little bit with that approach in terms of the router state that each node needs to keep because the packets that the node sends for the advertised channel work just as well on the unadvertised ones.

Pierre: Right, fascinating. And then one of the other things we discussed was how having web of trust peers would avoid the issue of them force closing a channel on you or even cooperatively closing a channel so your channels can have more age and have a Lindy effect for routing.

roasbeef: You can maybe have a lower CSV value. If I have a channel with Conner I can have a lower CSV value because I have more protection against him cheating me or trying to do a breach. Businesses may have different parameters as far as public channels to themselves versus parameters on x people on the greater network.

Pierre: This leads me to the next question from @cart852. Do I need to close my payment channels to upgrade my lnd software in the future.

bitconner: Typically no. Most of the changes are backwards compatible with channels. I don’t think we’ve had a release where you’ve needed to close channels necessarily.

roasbeef: No

bitconner: Typically any upgrades that can be done…. A lot of changes are done outside channels. There’s a lot of stuff going on in terms of how we manage wallet software, gossip messages, routing tables, stuff like that. Not every update necessarily touches your actual channel data. Those channels should continue to work as well in the future. There could be a point in time… it really depends if you pull in a new feature, a brand new channel design. If you want to move to an eltoo channel or you have one that is now capable of doing 2PECDSA or a Schnorr variant of Lightning. All of those would require you to upgrade those channels just because they have fundamental different channel designs, different keys, stuff like that. For the most part, for the current design I haven’t seen a reason why you’d need to close them out.

roasbeef: Maybe in the early, early days when things were a lot more in flux but right now things are a lot more stable. You shouldn’t need to close channels.

Pierre: Awesome. The next question is from…. I’ve heard something about identities on the Lightning Network but haven’t looked into it, that you could attach an identity to your node. Is that correct and could it be used instead of an account name plus password in some cases.

bitconner: You can set an alias on your node but no you shouldn’t use them as an authentication mechanism or even a reliable identity system in any case because they’re not authenticated in anyway. There’s no global consensus on node announcements so he could say Roasbeef, I could say Roasbeef, I could say Not Roasbeef tomorrow and I can just sign a note and change it. They’re totally mutable, they’re not unique. You’re putting a lot of faith in those aliases. They should be treated as maybe. It really should say maybe or probably not.

bitstein: Mine is going to say Real Roasbeef

roasbeef: The one thing is that there is this system in lnd where you can sign a message with your node pubkey which you can use to authenticate your node which could be used for some sort of authentication. It’s not really this is Blah, it is this is that user identified by that pubkey.

bitconner: You can still always trust the pubkeys because the aliases have no authentication.

Pierre: Gotcha. So we’re coming up on a hour here. This has been a fascinating conversation. Is there something you guys want to shill or promote?

roasbeef: Run lnd, I don’t know.

bitconner: There will be a bunch of new features coming out early next year. We’ve been working a lot on the watchtower protocols, getting those flushed out, starting to test it out. I just ran it with an in-memory database on my node last night, checking out that everything is working properly, as we expect. So should be going through review on that in the next couple of months. So maybe people on Slack, be looking to test that out if you guys are interested. It’ll need some testers.

Pierre: How do you get on the Lightning Labs Slack?

bitconner: There’s an invite link somewhere.

roasbeef: There’s a link in the README of the lnd GitHub. It’s kind of tucked away but developers you should be able to find it. There’s also IRC #lnd on Freenode, those are places that we’re hanging out.

bitconner: It’s the lnd community Slack.

Pierre: Gotcha, awesome. If you’re a Go developer, definitely go check out Lightning on GitHub and see if there’s any pull requests or issues you want to help out with. You mentioned there’s 170 issues that need some attention.

roasbeef: Some of them are bugs, some of them are feature requests. Add a new call or do whatever else. There’s a tonne of stuff to do.

bitconner: There’s an equal number of PRs to review.

roasbeef: There’s some contribution guidelines that are worth checking out that we’re updating right now.

Pierre: Not all of them require a Masters in cryptography or that level of background knowledge right? There’s a few that a Go hacker…

roasbeef: Yeah. The thing is that Go is pretty easy to learn if you know Python or C it is pretty similar because it’s a pretty small language. Go from there, there’s a lot of small tasks as well like add new CLI command or something like that.

bitconner: If you’re looking to contribute, use the Makefile. That’ll save you a lot of time.

roasbeef: We can work on the docs there too.

Pierre: Any parting thoughts? We should follow you on Twitter @roasbeef and @bitconner. Is there a preferred way of communicating with you guys if people have questions?

roasbeef: Twitter or IRC is what I’m usually on.


---
title: The Present and Future of the Lightning Network
transcript_by: Bryan Bishop
tags:
  - lightning
  - lnd
  - c-lightning
speakers:
  - Will O'Beirne
  - Lisa Neigut
  - Alex Bosworth
  - Leigh Cuen
date: 2019-05-11
media: https://youtu.be/OzpfiieV5C4
---
LC: Can everyone hear me now? Alright, alright.

WO: It's getting some good usage. A lot of those are businesses. Definitely it's in the early stage. Elizabeth talked about this. There's a lot of things that are mostly for fun, it's not really at ecommerce yet.

LC: That's for lnd?

WO: Sure, and I think Lisa can talk about c-lightning.

LC: I like these different implementations for LN. Lisa, what about c-lightning development right now?

LN: I think a lot more stuff has been built for lnd for liquidity projects. We're trying to make more accessible for people to build their tools for c-lightning. One of the ways we've been doing that is the c-lightning 0.6 release in Apirl or MArch with the new plugin system which allows third-party developers to build kind of in-process applications as plugins. It gives you more access to customizing the node.

LC: What about dual-channel funding?

LN: That's spec work, yeah. The dual funding proposal came up in back in November. We had a meeting in Australia and we had a few things we wanted to see in the spec in the future. Right now, dual funding would be you open a channel and both sides would have the opportunity to contribute funds if they would like to. This would hopefully lead to a more balanced network topology.

LC: And also close in channels as well? How might that add a dynamic of positiona lvalue to the network?

AB: Inbound liquidity is not all created equal. Someone might say you have 1 BTC of inbound liquidity, but if that liquidity is only in your corner of the network.... and if you're a routing node, if everyone shares similar common inbound liquidity, then you're really not bridging anybody, and the way you add value to the network is bridging people together as a router.

LC: What lightning usage do you expect will increase?

LN: I think more vendors will come online.

LC: What kind of vendors?

LN: The examples I find most interesting is..... basically he opened a node to sell t-shirts and swag online. He began accepting lightning payments. I think that's a good example of where vendors is going to be coming from. It's going to be existing vendors that you can buy stuff from immediately.

LC: Alex?

AB: I am excited about bringing exchange flows into the lightning network. Right now it's poorly capitalized compared to the billions of dollars flowing through exchanges. We've taken some first steps for bringing some of that activity in to that network.

WO: I think exchanges are a good use case, yeah. I think we're going to be strictly in the toy phase right now. A lot of you want to hold bitcoin since the market price is going up. I love the vendor use case, and I think lightning is in an interesting position where technology gets interest before the tech is there. People don't really want to spend bitcoin right now. Once it gets stable and people can think about it.... I think in the next year, we're going to be seeing more use cases.

LC: Lisa, how do you think the lightning network is going to impact the cypherpunk movement and culture more broadly?

LN: I'm hesitant to answer for the cypherpunk community because I am not sure I am in touch with that community. But I understand some of the ethos, like giving power to people so that they can transact peer-to-peer instead of only authorized vendors. I think lightning has new potential to enable people to transact globally. It's super easy to just send a payment directly and you don't have to involve middlemen. One thing that Ireally like about lightning is like keeping in the forefront of their minds and they are adding payments to the system is the ability to ..... and that's like, there's definitely this ability for you to go out and buy something and not have that show up anywhere on any report. I heard from a friend that payment systems traditionally, like credit cards, they have an idea of where... so like anytime you use a credit card, it's attached to you, and they can see whether you wnat this or not, you can see where money is going. If you're a trader, I could see how you would want that information so that you can buy Macy's stock or something. But this is a development that will improve privacy.

LC: What about user intentions? Alex, do you think the lightning network has a ethos? Is it being used in a way that is not designed to be used?

AB: I think the ethos is driving development right now. When we are working on lnd, we're thinking about what we want to see happening. We're saying, let's make it impossible for censorship to happen.

WO: ....

LC: Lisa, what do you think?

LN: .. we're adding this capability to the clients, that let you hold on to HTLCs to basically, when you make a payment and send it to an HTLC and then you have an opportunity to accept it and pull the money through. In c-lightning, we're adding the ability to hold on to a payment that you got from a vendor, so at some point in the future, you have a certain amount of time before that payment expires, and that payment... but when you send that payment, until it gets accepted at the vendor, all the money along the path to the vendor is locked up, it's kind of an escrow until that payment gets through. So this locks up the money along the route. As a network effect, if this occurs many times, then it makes the liquidity of the network harder to come by because it's all locked up. I think there's application developers and protocol developers need to keep this in mind and how it works.

LC: I know you guys are working on tools and implementations. Is there anything in particular, Alex, that you admire about Lisa's work, or c-lightnign versus lnd?

AB: I like the thinking about the spec. I think that's really powerful in lightning, we're all developing a spec or standard. There's different groups and people involved that are all collaborating on BOLTs. That's what I really like about c-lightning.

WO: I like that c-lightning is language agnostic. I've seen so many lightning applications and tools. I like that people can have hteir own tools to build on lightning. This is going to encompass the whole development community and not specifically one language.

LC: What about standards beyond BOLTs?

WO: I talked about WebLN just a few minutes ago. It's not part of the lightning network baseline spec. It's not a BIP because I don't believe in standards processes. I think lightning is layer 2. The further we get away from baseline tech, ... the stakes aren't quite so high, so lnd and c-lightning are on a monthly basis, and bitcoin is once every quarter, and it takes a long time. I look at this as a way to improve on the user experience and keep it to just those developers.

LC: Is there a project that you're really excited about?

WO: Your twitch channel? That's a brilliant marketing strategy.

LN: I'm really excited about the plugins for c-lightning. It's not the most exciting new stuff in the lightning space, but in the c-lightning world it's pretty exciting. We had someone working on autopilot which was fun. The rebalancer is going to be fun, and it will help with payments routing. We also added an invoice payment mechanism that you can do with circular blue htings. There's existing ways to move funds around and the stuff in the plugin system or lnd and see how it lets people do stuff. I'm excited to see that coming up.

LC: Alex, what are you excited about?

AB: I think the whole idea of .. is goin to be really important for bitcoin. It's also a question in terms of lightning... releasing a node into the world that has.. and people can, it's a public node and people can see it. It has a public key... making these very accessible, I think it's going to be more important to bitcoin than lightning.

LC: What about you?

WO: I can't think of anything more cypherpunk than everyone having their own servers that they can give permissioned access to. I talked about these macroons. The baker is the idea of being able to take these macaroons that have various ACLs, and to me, that is driven from-- the system--- or if someone gives a credit card number they can charge it all day long. But the idea here is to give specific permissions and possibly also limiting the amount of payment, and we can replace subscription fees. Some of you might have a gym membership and you have had trouble canceling the membership. But this shouldn't be possible in lightning. Being able to force companies to respect users like this is super exciting to me. You're going to see more people programming nodes in ways that you didn't even initially think of. I think the use cases are so powerful for freeing us from corporate tyranny.

LC: What should we keep in mind?

WO: I think the end goal for all of us is spending bitcoin. Sometimes we need to check ourselves and understand, it's a big money shift. It started in mindset and store-of-value, and it will be shifting back to payments at some point. I think it's important to be sober about who is using this. I'm excited about being able to use lightning apps that have been built by people around the world without having to send your payments through them.

LC: Alex?

AB: I'm pessimistic about merchant adoption just because in a lot of cases, it's not so useful. If I wanted to describe to someone who was not in this space why they should start using lightning or accepting lightning, well what's the point? It's not selling it. If you're talking about micropayments, it's only possible with the lightning network. .... Someone is offering 2% on all purchases that use lightning. Square gives me $1 for every coffee I pay with bitcoin or something.

LN: I think small vendors have been having trouble with payment processors, like censorship issues. In terms of driving adoption, I think vendors will drive it to some extent. Credit cards don't serve all vendors. Also, payment processor fees can be kind of high. There's a possibility that vendors will drive this for consumers.

WO: I did a t-shirt sale a month ago. As a small vendor, the experience for me setting that up, I can't go to Square and setup a partnership. Maybe I can use their API but they will take 3% off the top and then pass that to customers... But it was easy to do this with lightning as a one-off. I think we often focus on replacing current infrastructure with new technology, but the cool thing to think about is the new use cases that you can get out of this technology. But this is hard because it requires new thinking.



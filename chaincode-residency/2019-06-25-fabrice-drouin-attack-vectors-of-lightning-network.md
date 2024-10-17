---
title: Attack Vectors of Lightning Network
transcript_by: Gijs van Dam
tags:
  - security-problems
  - lightning
speakers:
  - Fabrice Drouin
date: 2019-06-25
media: https://youtu.be/R5cSrftd8nc
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-fabrice-drouin-attack-vectors-of-lightning-network/
---
Location: Chaincode Residency – Summer 2019

## Introduction

All right so I'm going to introduce really quickly attack vectors on Lightning. I focus on first what you can do with the Lightning protocol, but I will mostly speak about how attacks will probably happen in real life. It's probably not going to be direct attacks on the protocol itself.

## Denial of Service

So the basic attacks you can have when you're running lightning nodes are denial of service attacks basically. Lightning nodes are servers that accept incoming tcp connections, you can just overflow the servers with connections and that's something that is extremely hard to fight. Basically fighting low level connection DDoS  is really expensive. You can use services like Cloudflare but it's very expensive and if you don't what's going to happen is your host your hosting provider will eventually disconnect you from the network there's no route to you because DDoS attack against you will have an impact on everyone else in the same data centers and you will be effectively disconnected so that's really really hard to fight.

There's an ongoing DDos attack against electrum servers, I don't know if you have heard of it. They are blacklisting I think 150,000 IPs right now, but it's a battle that is really hard to fight. Something that is really easy to do with lightning but it's a bit costly is to just lock up channels. You have limitations in lightning. You can't have more than, you can't have too many pending payments and the amounts of your pending payments is also limited, so you can just lock up channels. You can just send HTLC's without preimages and after a while, channels will not accept more pending payments. However, this is not free. So can you tell me why it's not really free to do that?


Audience Member: You also lock up your own channels.

Fabrice: Yes so it's,...It can be really annoying and if you choose really long routes you can lock up to ten times your funds or even 20 times your funds but it's expensive for you. You need money to do that, but it can be really annoying.

Audience Member: But there is an asymmetry going on right? It's pay 1...the benefit is 20 times.


Fabrice: Yes, but 20 times not that much so you can't really perform a large scale attack with this type of locking up funds.

Audience Member: But potentially (inaudible)

Fabrice: Yes.

Audience Member: But if you're locking it up, eventually you'll get it back (inaudible)

Fabrice: Yes but it can still be a bit annoying. There's also resource usage attacks. If you look at the type of queries that Lightning nodes are supposed to serve, some of these queries can be quite expensive and especially the syncing your routing table is really expensive and using range queries can also be a bit expensive. So if you connect to a node you request routing table dump, you disconnect, you try again, you disconnect, try again, this can be really annoying for the serving node. So that could also be used to just lock up resources on your servers.

## Preimage reuse

Something that is really bad, but it's something that happens with most protocols is reusing random byte use. If you pay once, suppose Alice buys something from Carol, she pays once and for some reason Carol's website is not too good, it's reusing the same preimage. So now Alice will see... We try to pay a second time but if someone has seen that preimage, if Bob knows the preimage of a payment it's supposed to relay, it will not relay it, it will send back the preimage. This is really bad because Alice will have a valid proof of payment. She will have a payment request signed by Carol. She will have the matching preimage so she can go to Carol and say I've paid you, give me whatever you are supposed to send. It looks pretty bad and there are many, many ways you can end up with bad random generators, many ways you can end up with reusing a value that is supposed to be random. And if you try to be clever, if you try to come up with a nice scheme for generating payment hashes and payment preimages, this is a bug that you could actually hit and it's really bad.

## Probing Attacks

There are probing attacks. I think this is a topic of one of the next talks so I won't dive into it but basically with lightning, you can do probing attacks because you can use the fact that: no, it will not behave in the same way if they are the destination for a payment or if they're not. So using different error types that are returned. They help you learn who is supposed to be the final destination of a payment. You can also try to guess the balance of specific nodes using other kinds of probing attacks. So they are tedious to set up, but it works because nodes will not behave in the same way if they are or are not the destination of a payment.

## Publishing Revoked States

A very simple way of attacking lightning nodes is just to try to cheat and publish revoked states as we've seen if you do that there's a window, a time window during which the other node can steal all your funds so this is an open question for you, something you have to think about: How do you prevent someone from using the revocation key and steal all your funds if you're trying to cheat.  We'll get back to this later but suppose you want to cheat. What could you do to prevent the other guy from punishing you, if you provision old states?

One of the things that we've done with a mobile app to fight this is to use really long CLTV delays, long penalty windows, but it's bad UX because it means because of our problem your funds are locked up for up to two weeks and if you're flying for a really long time like if you take a month off to go hiking in Nepal or whatever then you need to close all the channels otherwise you may lose them.

## Watchtower

So watchtowers, I think we've described how they work, but the consensus now, even though not everybody might agree with it, is that the penalty idea may not have been such a good idea after all and I don't think anyone is actually trying to cheat right now. So the few penalties transactions that have been published were published because someone messed up with an old backup and were punished for making mistakes but not punished because they were actually trying to be evil. So Eltoo -  that's my opinion - is a bit better. But I understand why some people still want the ability to punish bad actors.

## "Lightning Node" Attack Surface

But honestly I don't think that attacks against Lightning nodes will attack the protocol. I used to work for a security company for some time. My first year was in the defense industry and then the security industry. We still work with security consultants and basically if someone was to attack Lightning they would not attack the Lightning protocol, they will attack the implementations. That's what is really likely to happen.

Have some of you worked with security companies or pen systems? So there's one thing that is really funny with these guys: you can work on building things or you can work on attacking things, but you don't do both at the same time. So pen testers and white hats, very often they are developers, but they will not work on building and defending on the same project. So you choose a team to work on building something and the team to work on attacking the same thing but they're not the same people. It's like, I think, American football, but I don't know that much about football, but you have defense teams and attack teams and they're not the same guys. Maybe people can play defense and attack but not in the same games and with security companies and pen testers it's the same.

Guys will sometimes build things or sometimes they will attack things but they won't do the same type of work at the same time because the mental switch is really difficult to do even for really experienced pen testers. So what this means, and that's bad news for us, is: Teams that build things are really bad at understanding how to defend their software against attacks. You need to bring in people who would just look at it and try to break it. When you're building something, even if you're very careful, you think about what is supposed to happen, but when you're attacking things, your state of mind, your vision is very different.

You all know the five-dollar wrench attack, okay, and it's something that you see in many actual attacks against systems: physical or software attacks. For example this door, I don't know what kind of lock it has but suppose it's a really, really fancy lock, very expensive it's almost impossible to open. But the door is plain wood, it'll probably take 20 seconds to just cut a hole into it, it wouldn't be too noisy and then you're in. And the fact that the lock is super strong and impossible to defeat doesn't really matter because it's just plain wood and that's basically what happens with most actual attacks on things and the fact that software is open source is not always a good point because it means that it's very easy to study the source code and find issues. And that's... Every pen tester we've met has told us the same thing: being open source is not a silver bullet. It doesn't give you magical powers. What it means is these people can actually look at what you're doing and understand weaknesses and then will not attack you right away. They will wait and see if it's worth it. So I think I'm not saying open source is bad. Everything we do is open source, but I'm saying that the feeling that is everywhere that because it's open source it's safe because people look at it, it's not that true. There were huge bugs in openSSL. Some of them have been there for a long time and no one saw them. There was a really funny bug, I think it was in Ubuntu a few years ago, where you would hit backspace like twenty or thirty times and you would just bypass login checks.

There was another one, I think it was also Linux. You would remove the hard drive and basically you would bypass login checks because there was no more password to check against. So being open source is not always a silver bullet. For example there's an ongoing debate when it comes to hardware wallets: Is it better to have open source firmware or to use secure elements? If you use secure elements you can't have open source firmware. You have to sign NDA's and I think you can't publish. So on one side you have Ledger and the firmware is not open source. On the other side you have, I think, Trezor, it's open source. Which is better? It's really hard to tell.

Audience Member: Multisig!

Fabrice: Yeah but I personally think that using secure elements is probably today a bit safer than relying on open source firmware.

Audience Member: The problem in closed source is then you get to a situation like two months ago that almost all the ssd's out there were faking about encryption. Everyone thought they were doing disk encryption, but it was all fake. The ssd's lied about their encryption and didn't really encrypt anything. Samsung, Corsair and all of the huge companies lied about the encryption. It wasn't encrypting anything. So Trezor might do the same. It might not even be an HSM really.

Fabrice: You mean Ledger.

Audience Member: Ledger!

Fabrice: Yes I'm not saying: because it's closed source it's better. But I'm saying that secure elements are probably extremely safe today there are no publicly known attacks against secure elements and it's a trade-off between being really opened and being really closed but for example what I think that I found really funny is almost every pen tester I've talked to says that Chrome is much much safer than Firefox. If you worry about security you should use Chrome. It's bad, it's Google, it spies on you and everything, but there are very few zero days against Chrome and people found a zero day against Firefox, I think, one or two weeks ago. So It's not something you want to hear but if you really worry about security maybe right now - and it's sad - but Chrome is a better choice than Firefox or (inaudible)

There is one thing that, so what I'm saying is, if you want to think about how to secure Lightning nodes, how to attack Lightning: look at the implementations, look at how they run, look at where they run, which cloud provider they are using. This is what people are going to attack. They will not attack...They will find a subtle flaw in a protocol or whatever. They will just find bugs or remote exploits or other flaws in your implementation and this is what will be attacked.

The wallets you use... so if you are running a Lightning node you have a hot wallet because you need to be able to open channels. And then you have the actual Lightning wallet. It's another kind of hot wallet with different constraints. A lot of people are thinking about using HSMs to protect the Bitcoin wallets and the Lightning wallets and protecting the Bitcoin wallet is fairly difficult because the problem is automation. You know how the hardware wallets work: You send a transaction to the hardware wallet. It will display the address you want to send money to and if the address is right you will press a button and it will sign the transaction and return it back to you. This is fine if you manually interact with your wallet but what if you want to automate things?

Suppose you're in a big service you need to sign like big transactions all the time? How do you.. you won't have people clicking on buttons every time you want to send something, so you end up with another issue: It's very easy to over-engineer security solutions but if it's impossible to steal your keys but it's very easy to get your system to sign anything, then you don't have any kind of security. So if you focus on protecting keys but you forget that what you need to protect is the ability of people to use your keys, to get your system to sign, then you're missing the point and you're not that safe. And it's a problem with a lot of bitcoin applications and it's something that all hardware wallet vendors are working on but it's really hard because there are very few things you can check when you're signing bitcoin transactions. Lightning is a bit different. There is something you can do that will prevent, should prevent people from stealing from you. So what that is, is when you are relaying payments you can try checking that for every outgoing payment there is a matching incoming payment. But to do this you need to understand what's going on, which is a bit hard.

## "Eclipse" Attack

There's something else, I think it was an attack that was described by Stepan Snigirev one or two weeks ago and I want you to think about it. So I'm Bob in the middle and I'm relaying payments and Stepan says: “What happens if the channel between Alice and Bob is closed but Bob doesn't know it? Basically what happens if you manage to stop blocks from the Bitcoin blockchain to get to Bob. You blind him and he is not seeing that the funding transaction of his channel with Alice has been spent. So the attack is Bob does not know that the upstream channel on the left is closed. He will keep on relaying payments. So do you think it is actually a problem or not? Do you think it is safe or do you think Bob is losing money because he's paying on this side and on this side where the channel is closed, so...

Audience Member: Wouldn't they have to be making it so that Carol couldn't see that, because Carol determines the route?

Fabrice: No, no, no. Basically Alice has managed to stop blocks from getting to Bob, so Bob doesn't see what's going on on the Blockchain. It doesn't see new bloks coming in. So he thinks, Bob thinks that the channel from Alice to Bob is still open. So what Alice is doing now she's sending payment to Carol through Bob and basically Bob will relay payments but it doesn't have actual incoming payments because that channel doesn't exist anymore. But is it really bad?

Audience Member: Bob would have to be offline longer than for the timeout of the channel to expire, right?

Audience Member: I don't see Carol, unless (inaudible)  Carol conspires like, they just keep sending payments. Like they can make it so Bob is sending payments to Carol but he cannot get them from Alice anymore.

Fabrice: I can leave this as an open question because I think there's a session on DDoS attacks against Lightning nodes, but basically…

Audience Member: In order for Alice to (inaudible) the HTLC Alice has to revoke the old state, no?

Fabrice: Ah yes, you are getting there! So what happens if you try to use a channel that is closed but you don't know it?

Audience Member: You can't claim.

Fabrice: OK, I'll let you think about it and we will come back to this during the next session. Basically the question is: Alice,...the channel between Alice and Bob is closed. Bob doesn't know it, so he keeps on relaying payments from that channel to other channels. Is Bob losing money or not?

Audience Member: Depends if the timeout (inaudible)

Fabrice: It is not a question of time limits.

Audience Member: I think it is a question of time.

Fabrice: It is not just that.

Audience Member: (inaudible) can be kept for like two weeks or whatever, like the revocation…

Audience Member: He is putting HTLC's into a commitment transaction that cannot go on-chain anymore because it's already… (inaudible)

Fabrice: OK, I'll give you the answer later. OK, so the question is: Is Bob losing money or not? So you have to choose "Yes, Bob is losing money" or "No, Bob is actually not losing money"

Audience Members: No. Yes! Both. It depends. Maybe? Schrödinger's channel.

Audience Member: Wouldn't happen with Eltoo.

Fabrice: There is something I'd like to mention…

Audience Member: It would happen with Eltoo.

Fabrice: Again when we think about security and what to do to protect things, very often we get the wrong picture. Speaking to actual pen testers is really enlightening because they have a completely different thought process and they look at things in a way that's completely different. So one of the things that happened a few months ago was a successful phishing attack against Electrum servers and it does not target the Electrum protocol at all.

Audience Member: inaudible

Fabrice: Yes, what it does is... and it's something that everyone should be worried about because it's really easy to overlook this. Basically Electrum displays error messages to the users and error messages come from the servers you are connected to. And some guy said okay I'm going to display a message that says: "You need to upgrade. Go to that link". And that's what people did. And you download a really bad Electrum client and your money's gone. And it's really hard to fight because the server, the actual Electrum client, is showing you a message that says: "Go to that link and upgrade". So you trust it. Especially if you don't, not be an expert. You do what it says you click on that link and your money is gone.

Audience Member: How do you show error messages in the onions that are being returned?

Fabrice: It's an open question but basically when you design stuff that is supposed to be used by anyone, what do you do with inputs that you have no control over? What do you do with messages that you will see? What do you do with error messages that you will see? What do you send as an error message? If you have a crash or an exception do you basically take the stack trace and the error message and send it to your peers saying: “Okay this here is all I got or do you convert and sanitize everything? And that's a very simple way of attacking software. You cause it to fail. You send it garbage and you look at what it returns. And in some cases it will return a lot of information that you can use later. It's a bit like… Does everyone know what side-channel attacks are? Okay. But if I asked you to write software to compare two strings, what you would come up with will probably be very weak for a security point of view because you will stop as soon as one of the characters is not the same. Which is really bad from a security point of view. And that's what I was trying to say when I said that when you're building things, your state of mind, even if you're really careful, is not necessarily good for security. Which is why it's good to have people who are not trying to build anything, they are just going to look at how to break what you are doing. And to really work they have to be a different team. It can't be the same guys.

And think about this one: There's no channel between Alice and Bob. Bob is relaying payments. Is Bob losing money or not?

Audience Member: Yes.

Fabrice: I'll give you the answer later. Okay that's it for me. Questions?

Audience Member: Where's the next hardware store? I need a wrench.

Fabrice: OK, Thank you.

Adam Jonas: We're a little tight so we'll bump it to the afternoon. Maybe we can do a discussion now? Does that work?

So we are actually done with the presentations for today. We are just going to be discussion-based and exercise-based for the rest of the day. Just want to show you your groups so that we're prepared. So it's three different groups and it looks like this... cool? Everybody got that? Yep. And the first assignment for the next let's say 10 minutes or so is to get together with your group and we have two asks from you: What are the hot wallet risks? Just in Lightning generally? And then denial of service attacks: why don't we talk about, so like, why don't we actually put together some lists of what we should be concerned about and then we'll convene again as a group and talk about it. Cool? Feel free to get out of the room. We'll see you in about ten minutes.

Audience Member: All the groups talk about the same thing?

Adam Jonas: Yeah, all the groups talk about the same thing.

Audience Member: Jonas, how do you plan to do this with the cost and price questions? Every group gets a different topic, or…? Because we could boil it down to three. I mean (inaudible)

Adam Jonas: Yeah, put it down to three and have each one (inaudible) section.

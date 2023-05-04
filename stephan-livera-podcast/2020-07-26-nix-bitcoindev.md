---
title: A Security Focused Bitcoin Node
transcript_by: Stephan Livera
categories: ['podcast']
date: 2020-07-26
media: https://stephanlivera.com/download-episode/2348/195.mp3
---
podcast: https://stephanlivera.com/episode/195/

Stephan Livera:

nix-bitcoindev Welcome to the show.

Nixbitcoin:

Hello. Thank you for having me.

Stephan Livera:

So nix-bitcoin Dev obviously as you’re under a pseudonym don’t dox anything about yourself, but can you just tell us a little bit in terms of like what you’re interested in about Bitcoin and is it the computer science aspects or what aspects of it interest you?

Nixbitcoin:

So I came into Bitcoin pretty much from the privacy angle because I’ve always pretty much since I’ve touched a computer, I’ve thought it’s really like an extension of the human brain. So it deserves the same protection security wise as the content in your brain, which is absolute. So that’s really the angle I came into Bitcoin from where I saw, wow, this is this kind of money that if we use it properly, it can guarantee the, that level of privacy in our financial transactions. And obviously a great part of privacy on Bitcoin is running your own node and having your own hardware. And so I’ve been really private always for something like Nix-Bitcoin. And when I saw Jonas Nick working on it, I immediately saw the power in this platform. We’ll get into that later with NixOS and that’s kind of where I started in program with him. And it’s been a really interesting trip from there.

Stephan Livera:

Great. So let’s start with, what is nix-bitcoin?

Nixbitcoin:

What is nix-bitcoin? It uses NixOS which is this novel approach to a Linux distribution to ship a deterministic and reproducible Bitcoin node to users. NixOS is basically the it’s a purely functional operating system. So what that means is that it builds the entire operating system from the source code of every application of the Linux kernel. And turns that into a gigantic formula, which will result in the same system every single time it’s deployed.

Stephan Livera:

One of the interesting things when I was looking into NixOS is I guess one of the ways nix distinguishes itself is around its package management and how a new configuration cannot overwrite a previous one. Can you expand a little bit on that? Why is that important? Why does that matter?

Nixbitcoin:

Well, starting from being purely functional. What that means is it instead of doing package management and the way that traditional Linux operating systems do it, where they download binaries, it takes this approach where it links different kinds of different kinds of program source code together, and then builds those on top of each other. And how that pertains to what you said about versions is that you can always roll back to that previous version where the formula resulted in that source code building on top of each other. You can always go back to that and you can always start from that again. And that’s where the atomic nature of NixOS comes from. And we use that. That’s one of the greatest features that make Nix-Bitcoin so special is that it will, if you had a sane configuration at some point that works, you can always go back to that. It, you can’t really fuck up – I don’t know if I’m allowed to swear on your show but you can’t mess up your system. You cannot, you can always roll back to the last previous functionally functional state.

Stephan Livera:

And so I suppose this helps us in the way that we have, I guess if I’m understanding you it’s that we have more surety that we’re running the right code, right? And that’s, I guess that’s coming, tying back to the reproducible aspect you were touching on earlier, right?

Nixbitcoin:

Exactly, that’s one aspect and security is at the heart of nix-bitcoin, but security doesn’t really help you when your node is broken or it’s not working. So from the very start, that’s the number one priority and NixOS is strong in both aspects. And that allows us to make nix-bitcoins strong in both aspects.

Stephan Livera:

Then I presume the idea is that you would install NixOS and then you would install this Nix-Bitcoin. And it’s like a, is it kind of like a scripted set of packages that all install together? Or can you tell a bit about how it works?

Nixbitcoin:

That’s exactly we’re different from the other node projects is that it’s not a bunch of scripts on top of each other. It’s, the way it works is you don’t need NixOS installed on your local system on your workstation, where you’re deploying from, you only need NixOS installed on the hardware or cloud wherever you want to deploy to. So that, that machine runs NixOS and from your whatever, even Mac works, but from your Linux computer, you can just download the GitHub repo execute Nix shell that puts you inside of a command line environment with everything you need. And then all you need to really do is do some settings and configuration.nix And then deploy. And every time you deploy with that configuration and that state of the repository you’ll get the exact same node.

Stephan Livera:

I see. Okay. So is it kind of, again, I’m not a developer, but is it kind of like a VM in some ways, then you’re kind of running this little VM on your machine, and that is its own little contained –

Nixbitcoin:

That’s possible. That’s not the way I use it, but that is possible to deploy to a, VM your own machine, but where I think it really makes sense is to deploy it to a standalone device to a standalone device in the cloud or physically, but that’s always running that’s what, how I use it, but it’s possible if you want to play around with it to deploy it to a virtual machine, that virtual machine would kind of be exactly that, a virtual machine, the same way that a dedicated devices, which is running NixOS and then receives your, it’s difficult to explain. I didn’t understand for so long, even while I was working on it, how NixOS, really the magic of it is that it’s this new approach, a dysfunctional approach, functional programming approach to systems management, where it builds an entire system, basically mathematically to deploy to either any machine that’s running NixOS.

Stephan Livera:

I guess the idea is this is something that people could take an old laptop and then run Nix-Bitcoin on it. And that’s their way of running their whole stock of Bitcoin software and not just, you know, Bitcoin core, but also running Electrum rust server and so on. Or they could put it onto a dedicated PC box that they keep in their house or like on a VPS, as you mentioned, like an external server, virtual private server.

Nixbitcoin:

That’s right now we use it I use it myself. Jonas uses it. Jonas’ brother with Donner lab, their entire backend is built with Nix-Bitcoin. I don’t know if you know about his project, but they’re gaming with lightning doing gaming on lightning. So it really works in a range of set-ups and we’ve had a lot of just drive by contributors deploying to virtual machines, or even NixOS containers on their own machine just to play around with it. So this is why, when I think when Jonas saw NixOS, so as he saw that it was a perfect opportunity for a Bitcoin node because it’s, so it’s gives you the structure that you can always deploy that you can deploy onto a range of devices with.

Stephan Livera:

Maybe we’re sort of covering back over what you mentioned earlier, but what’s the benefit of say nix-bitcoin, over somebody who is, let’s say they’re using Qubes OS, or they’re using Debian or Ubuntu, which are other well Ubuntu and Debian, and which are some of the well known Linux flavours?

Nixbitcoin:

So when you install a Debian system, you have so many packages, you, and that’s one of the more minimal distributions. You have Python, you have sometimes even a print server stuff that you’ll never need with a Bitcoin node. You deploy onto that machine that has so much attack surface that is completely unnecessary. What NixOS does is it really just deploys a system that has a Bitcoin node and through that functional set up the functional approach that NixOS has it will just deploy with the dependencies you absolutely need, based on your exact setup, that’s benefit. Number one, is that kind of security and benefit number two is that you can always deploy back to old states, new states disable features that go really deep into the system. So for example we’re working on this huge project for the last two months that basically built this Linux kernel feature called network namespaces deep into Nix-Bitcoin, that every service that runs on your machine runs inside its own Linux network namespace, and with another distribution, it would be extremely difficult to switch between that kind of a setup and a setup without network namespaces, you’d have to have very complicated shell scripts, very complicated logic to roll back and forth with NixOS, it’s just switching one option, and that’s it.

Nixbitcoin:

And you can always go back and forth, back and forth and experiment around and always return to a working state.

Stephan Livera:

In order to install nix-bitcoin, does the user have to be using some flavor of Linux, or can they, I guess they can use it on a Mac or a windows as well. How would that, how would that work?

Nixbitcoin:

I think a Mac is possible, Mac works windows I’ve not tried it. I, we have had no interest in doing that. But I think that the way where this project is going is definitely making it accessible to everybody on a wide range of platforms and basically putting all that logic, all the NixOS stuff inside the box itself. And then you’ll never have to worry about having another laptop where Nix is properly installed and running and that you’ve properly secured. I think that’s, we’ve often talked about that and it would also build on the machine. So you’d never have an issue with compiling Linux software on windows, for example.

Stephan Livera:

Let’s talk a little bit about the target market or the target audience. Who is nix-bitcoin for?

Nixbitcoin:

Right now it’s for, Linux Bitcoin developers who are using it to deploy their own nodes and for the startup and that’s using it. And it’s really in the beginning steps, we’ve done so much right at the foundation level. We’ve spent so much work really going in depth on all these Linux options. Wow, you can do this with systemD you can do this security feature. You can use a hardened kernel all this stuff that nobody else worries about. We’ve spent all the time worrying about that. So that’s why it’s really useful for us at the moment, but I think that slowly as we build out the foundation, which is very strong, we can focus on making it available, and you’ll see that in the next year, really coming into being able to be used by people basically familiar with the Linux command line. And I hope if we get more attention, then also we can have the resources to make this graphical that everybody can use it. And I hope that you also will be able to use it. And I’m actually very confident that we’ll get there.

Stephan Livera:

Right. I see. And so I guess, just for listeners to characterize this we would say this is very early stage, and you need to be more highly technically proficient before it gets down to the, let’s say the tech savvy Bitcoin level. And then the next level beyond that, which is the, you know, the average, kind of just the average tech savvy person. Who’s maybe not that into Bitcoin, but they can sort of figure it out. It’s, we’re nowhere near that level yet, but just too.

Nixbitcoin:

But the level we’re on is what’s really important. What’s been important to me is that the software works, the software is secure in the greatest extent that we’ve been able to make it. So, and that it’s actually really, I use it every day with basically I don’t know if you’ve ever used it spark wallet, which is a front end for.

Stephan Livera:

C-lightning.

Nixbitcoin:

C lightning. And I make all my lightning payments like that. So it’s actually, it’s really a living piece of software, but that magic, that beauty will take it’s time to spread because there a kind of hurdle. And sometimes when people hear NixOS, they think, Oh, I’ve never used that. It’s really complicated, but the way it’s already at this moment is that you really just need to drop into a Nix shell with one command and then edit your configuration file, which is a text file, uncomment a few things that you want, what kind of services you want and then just deploy. And that’s. So I think we’re really it’s at a good point. It’s not super finicky, it’s functional, and now we’re taking it one step at a time to make it available.

Stephan Livera:

You were touching on this a little bit before, but it might be useful for listeners just to understand where Nix Bitcoin is sort of situated. If you could help us understand the difference between nix-bitcoin and some of the popular well-known plug and play Bitcoin node, such as, you know, myNode, nodl, RaspiBlitz or Ronin Dojo some of those, how would you distinguish Nix-Bitcoin from those? Is it mainly the security, reproducibility aspects of it? Or is there anything else in particular?

Nixbitcoin:

I think security and reproducibility are two aspects that we can’t talk enough about because that’s really what you want is you want to enter your node every day and see that your money is still there. You want to never have a broken node with your funds gone. And you reproducibility also means that we can implement all these really cool features that users need. And especially startups, merchants need we can get into that later, but when it comes to, at this point, at this point, now what makes us different is that is really the security aspect. And the fact that we’re building on NixOS which allows us to do many more things in the future. And I’ve taken a look at a bunch of these these other node projects, like myNode.

Nixbitcoin:

And I’ve seen a lot of really quick programming, like setting every service to run under the same user and a lot of this stuff. That’s, I think really justifiably focused on quickly making it usable by the consumer market. But that’s not what we’re about. We’re not about cutting corners and running every service under the same user with no hardening options without our hardened kernel. That’s just, non-optional because again, I came at this from the privacy angle, from the security angle and that’s for a bitcoiner. And for enterprises, that’s something that it’s a nonstarter to not have that. So and Ronin Dojo is, I listened to your episode with Samourai, the Samourai cofounder, and it seems to me that it’s only focused on being a backend for your Samourai, wallet, whereas we can be a backend for Electrum for C-lighting for LND for JoinMarket, for Samourai, for wasabi. And that’s where we’re going, is being, as it says in the Twitter bio being a purely functional Bitcoin ecosystem, which uses this foundation to basically offer any kind of functionality that needs a backend, which pretty much has everything to do with Bitcoin that you want to preserve your privacy and security with.

Stephan Livera:

I see. Yeah. And so I guess it just depends what kind of user you are, for instance, you might be a user who is using a plug and play node mainly for the Electrum Rust server aspect. And it’s not necessarily holding your keys. It’s just hold, it’s just doing the Electrum server aspect and you might hold the keys on a hardware wallet, or you might have some multisignature let’s say, so then maybe you’ve got a different you’re running on a, you’re kind of using a different model to think about your security. Although obviously there’s still risks with that anyway. And I suppose

Nixbitcoin:

The Electrum server knows a bunch of your addresses, for example. So that’s something privacy related. Also the Electrum server, you want to be able to that it’s running at all times. And so it really, even a simple setup like that benefits from what we’ve built into nix-bitcoin.

Stephan Livera:

Of course. Right. no, and that totally makes sense to me. And also it’s worthwhile considering if you are running lightning or if you are using JoinMarket CoinJoining, or even Samourai Whirlpool CLI CoinJoining you have effectively, it’s kind of like the keys are hot. And so then you have to think about security for that too.

Nixbitcoin:

JoinMarket is really a great, great piece of software. And it’s the best example for something that you want to be on a secure hot machine. We have a PR up right now, that’s we’re reviewing at the moment and I’ve been running it on my node for the last couple of weeks without any issues. And I’m, every time I open up the node, I’m really satisfied with the way that nix-bitcoin secure secures my funds, which if you go onto the joint market order books, some people have a thousand Bitcoins in there that’s, you know, that’s really a huge risk they’re taking security wise. And so I think there’s definitely a place for a security and minimalist node like ours

Stephan Livera:

A little bit more in detail about the security hardening that’s available with nix-bitcoin. So as a quick example, I’ve noticed on the Twitter feed, you were chatting a little bit about access through an SSH. Could you outline a little bit around?

Nixbitcoin:

That’s kind of, that’s a bit of a joke at the moment because really the management interface right now is the command line. So that SSH is the way into that command line on a remote machine. And SSH really is a great piece of software that offers a lot of security. So it’s kind of a, meme that, you know my SSH keys are on a Trezor hardware wallets. So that’s really his strong level of security to enter your node remotely with. But I think that as the project continues, we’ll have some kind of management interface that’s not the command line exactly for the reason that we want to deliver this kind of security and and just the thought we’ve put into every single option and every single setting that’s possible with nix-Bitcoin, we, we want to have that, that power available to a wide range of people.

Nixbitcoin:

So that security feature is something great for developers like myself, but I think we can deliver the same security, even in a web interface with something like U2F, which also works with the Trezor hardware wallet. But regarding the general security principles of nix-bitcoin, I think it really starts with minimalism that you have a node that only has the software you really need, and that’s not possible with a general Linux distribution. At least not in a way where you’re not going to break it at some point when you start De-installing a bunch of packages. That’s what I used to do with Debian is really try to on install everything that I could. And at some point that would result in a completely broken system. So I’ve been around Debian, I’ve been around normal Linux distributions, and there’s been nothing that comes close to NixOS on the minimalism aspect, because it really has a kind of formula where it goes through and calculates what you need and builds only that. So nothing will ever come close to NixOS on that aspect. And when you don’t have something, if something isn’t there, then you can’t attack that. So that’s number one is the minimalism. Then number two, I’d say is really the reproducibility of the code. Not only all the higher level stuff like Bitcoin and C-lightning and LND, which we always, we have these scripts where we verify the hash.

Nixbitcoin:

With the developers GPG key. So we’re really focused on not getting bad software into, I’m not getting, not getting bad Bitcoin software into our project, but then even the entire stack, the Linux kernel, everything under that is also reproducible with NixOS, so you know, that you have the exact same system that everybody else has. And then so reproducibility, I think, has been a topic that people have been talking about recently because it’s so important for Bitcoin for something that completely relies on its security assumption on the security of the individual machines, where Bitcoin is installed. So that’s number two, I’d say then number three, it’s close between defense in depth and kind of the compartmentalization, I’ll start with the compartmentalization that we built into nix-bitcoin. So every service that we have runs in its own little box.

Nixbitcoin:

So that’s what we do with system D. We put every service in its own little box under its own user. It can only see its own directory and now even with network namespaces, it can’t even scope out your entire network. It can only scope out its own network and its little Linux namespace and the ones that we’ve allowed it to see and outside processes outside of that network namespace also can’t look inside. So that’s where we spend a lot of time. It’s really taking these services apart, putting them in different boxes and then saying, okay, where do they need to connect? What did they actually need to see? And only that is allowed. And that offers a great deal of security because now the programs like spark wallet that connect to your C-lightning, they’ll never see JoinMarket. They’ll never see Electrum, they’ll never see Bitcoind.

Nixbitcoin:

So that’s, that’s something that every time I opened my box, I’m really happy about. And then finally defense in depth, which means putting up multiple walls. So we have users, we isolate by users. We isolate with system D we isolate on the network level. We really try to have multiple lines of defense. And right now we’re reviewing something that I think Jonas and me think could be security relevant. And we realized that because of the compartmentalization we’ve built in, it’s actually not that big of a security issue because we’ve spent all this time putting up multiple defenses. It’s actually being caught, we think by one line of our defense. So we’ll be putting out a fix for that in the next few days. And also probably talking to other projects about this.

Stephan Livera:

Yeah. Interesting. And so some of what you were spelling out there, it kind of reminds me of when people talk about Qubes OS as well, where the idea is each like, like each application is like its own little VM and that way it’s kind of firewalled off from the rest of the system.

Nixbitcoin:

So I think Qubes is actually really interesting to start off on because that’s a perfect explanation of where NixOS is great. So Qubes, I use personally on my laptop, I love it. It’s offers so much. I recommend every developer who is working on security, critical stuff to install it because you don’t want to have something malicious on your system, which is able to compromise your signing keys or put in some, some bad code into your repositories. But it could never be used for a Bitcoin node because if you’ve ever set it up, you need to spend a lot of time setting up the individual VMs making sure that you allow all these firewall rules and you have to do that all manually and doing that every time is it’s unfeasible. And what we’ve done with nix-bitcoin is basically written these text files, these code files, where you just deploy from those and you’ll get the same system with those, all those settings. Pre-Installed every time you deploy it and even on multiple machines that you’ve deployed on, you’ll get the exact same state. So Qubes is a perfect example of how security can get in the way of functionality. And we can have both with nix-bitcoin.

Stephan Livera:

I was looking through, and you mentioned that you’ve got Tor, clearnet, and Wireguard, can you outline a little bit about the ways that the nix-bitcoin talks to the outside world?

Nixbitcoin:

Yeah, that’s really interesting. And that’s been a huge kind of construction site at the moment. It’s really something that we’ve been thinking about deeply is what, how do we want to expose these individual services to the bad, bad outside internet world? And right now we’re Tor by default. It’s really the only perfectly supported way is Tor at the moment. It’s really what I use and what I think before we get, come up with a really good that’s where we want to steer the users towards. I know that in an enterprise setting like with Donner Lab, it’s not that easy to use Tor because of the latency. So they’ve built their own WireGuard systems stuff with with nix-bitcoin. So if I can just quickly explain what wireguard is, it’s this new VPN client server, both sides, this tunnel that’s built right into the Linux kernel.

Nixbitcoin:

That is a, to a degree, a real, just, it’s a completely different level of simplicity compared to OpenVPN. And which allows you to have these tunnels across the internet that are effect are authenticated with a public private key pair. And you can just make this tunnel from any box to any other box and pass network traffic. So that’s something really interesting for nix-bitcoin and clearnet is, as we all know, it’s the base layer and it’s really usable. And we also want to make that accessible. So the plan at the moment is to take the network namespaces that we’ve built. And on top of that for every network namespace, give these three, four options how you want people to be able to connect into we want them to, by default be accessible through Tor version three and services, and then we want them to be easily accessible through a wire guard tunnel, where it just shows you the QR code, and you can enter that on your phone or whatever device you’re connecting from. And we want to make it accessible through Clearnet with automatic transport layer security like you know, with that green lock in your browser that just has secured the entire internet so beautifully in the last year, few years.

Stephan Livera:

When we’re chatting about this I guess there’s probably two main areas that the Bitcoin person is thinking about. So one might be, they are out and about, and they’re on their mobile phone and let’s say they’re running, you know spark wallet or Zeus wallet. And they want to connect back to their own C-lightning, I think right now a lot of people would just do that through a Tor because, you know, it might be a bit simpler and they don’t want to expose their home, you know, IP and so on.

Nixbitcoin:

Yeah. You don’t want to worry about all that NAT stuff. And Tor just completely gets rid of all that NAT translation networking stuff. That is really hard to understand, to be honest. So Tor has a wide range of of benefits in the consumer space, but sorry, I interrupted, just wanted to throw that quickly in there. What I love about it. Yeah,

Stephan Livera:

Of course. That’s fine. Yeah, no, that’s, that’s, I think that’s totally right. And so I think the downside then is that it can be a bit slower and sometimes it’s not as reliable. So then if you’re out and about, and you want to check your lightning channels, and then it takes a bit of time to load up, and sometimes it’s a little buggy because again, things are early then that, you know, can be, it’s not as smooth as a you know, customer experience. And so what some other people are doing is they’re doing like a VPN style set up. And I suppose this is where let’s say the wireguard set up, might be a little bit more amenable to that. I’ve also noticed some of the Nodl users, they like to use zerotier, which is more, as I understand, that’s more like a VPN style set up. So could you just tell us a little bit about your thoughts there, and it is, wireguard going to be something a little bit easier to manage there for the, you know, just think the typical Bitcoin HODLer who wants to manage his lightning channels.

Nixbitcoin:

Yeah. So Wireguard and zerotier or both DPN solutions why our guard has just gotten a lot of positive attention recently and has been put right in the Linux kernel, which means that it’s it’s really well vetted and a great piece of software. So zerotier and wireguard and have the same functionality. But I think that wireguard is much better. And in terms of the pure technology you said that the usual you know, HODLer, would he just see the QR code in his interface, install the wireguard app and just scan and that would make it so that he can connect to his own home address at home with almost no latency and without worrying about networking stuff and actually providing a reasonable degree of privacy as well in the process.

Nixbitcoin:

And the great benefit that I see VPNs have is that they have such wide support on all different kinds of devices. So Android iOS, everything has wireguard in their app store which you can’t say about Tor, you know, Apple puts up a lot of barriers to to cross app communication. So you don’t have a Tor daemon in the Apple app store. And which means that every app needs to package Tor itself and a lot of apps haven’t done that. So VPNs are something we need to have and we will have quite soon, and we’ve chosen wireguard. Zero tier I’m not so hot about.

Stephan Livera:

Cool correctly. I think Zap the iPhone has the Tor built into it.

Nixbitcoin:

We were actually involved in that discussion from the very beginning. I think that when we tried to implement LND on our node, that’s something we thought about it in the very beginning. And it turns out that now beautifully Tor, does work and it works with nix-bitcoin.

Stephan Livera:

Okay, great. So what about in the case where someone is a merchant and they want to expose their BTC pay server and they don’t want to necessarily open up unnecessarily the security risk there. How does a nix-bitcoin user handle that?

Nixbitcoin:

So for the user, it’s really great to be running with Tor or wireguard, he or she limits the exposure of their node towards a bunch of these privacy risks and makes it easier to deploy across NAT. And they get access to this really refined project where you have continuous integration, a bunch of automated tests that make sure it’s working at every point with every configuration and when something doesn’t work they file a bug report and it gets fixed. And the merchant that uses the same platform actually benefits from that too, because now they’re using something that’s been tested in such a wide range of setups for a bunch of different users that have all tried, just entropy wise, a bunch of different stuff, and it’s been fixed refined, and they benefit from this and the user benefits also from the enterprise that has resources to make everything better. So I think it’s really powerful to put these two projects together, merchants and consumer like we’re doing, and when it comes to a merchant, the way they would be able to use nix-bitcoin is to put it on a secure server in a secure data center somewhere. And I use a wireguard tunnel to expose just their BTCPay server to their main eCommerce shop and Voila. Now they have a secure backend for all their Bitcoin circular economy transactions.

Stephan Livera:

In that example, then they have not exposed their nix-bitcoin directly, it’s going via their public website. Or can you outline a little bit about that?

Nixbitcoin:

Yeah, it’s going via their public website. I don’t think it’s a good idea to put a big website on a web server that has so many different people coming in I’m on the same server as a Bitcoin node with potentially even hot funds when it comes to lightning. So either the merchant would have a separate BTCPay server instance, which then wire guard to communicate with the individual services like between Bitcoind and lightning network daemon On the network level, just a wireguard tunnel, taking that connection on their local machine to the connection on their secure server, or they’ve also run a BTCPay server inside nix-bitcoin, and just expose that, you know, port four 43 or 80, the HTTP port to the outside world with the wire guard tunnel to a wire guard server that’s publicly reachable and they can forward traffic to that from their website.

Stephan Livera:

Okay, great. And so just speaking about nix-bitcoin just more broadly and just generally around the question of difficulty of use. So how do you see that kind of improving over time?

Nixbitcoin:

That’s the central piece here for getting it into the hands of users. I think it’s gonna improve but we want to improve it without compromising these fundamentals we’ve built in. So we want users to build their own software from source code. We want it to stay reproducible. We want it to remain so compromising a password, which is commonplace at this point is not gonna lose you, your funds all this stuff we want to maintain while making a nix-bitcoin more usable. And that’s a real challenge, but I think that we’ll find an elegant way to do that by. And one facet of that is moving everything to the node itself. So it builds the software deploys to itself. That’s something we’re working on. It’s actually not that difficult to do with NixOS and then the second aspect would be to expose some kind of management interface potentially through a standalone app that authenticates itself with a locally stored key or a web interface where we would definitely use something like a U2F which is in my opinion, the best two factor solution, because it uses this hardware token that you physically have to depress.

Nixbitcoin:

And that hardware token also verifies that it’s communicating with the proper website. So you can’t really be phished anymore. And that’s, that would be one option. Or we make the, even the web interface behind the wireguard tunnel, where you need to authenticate to the wire guard tunnel with a key first, before you’re allowed to communicate even with the web interface. So those are the avenues with which we can work. I think that once we move out of the stage, which is the next stage of that stage, the next stage being unix familiar command line, familiar crowd, once we get to that stage and start moving out of that, we’ll pick a final path, but it’s much more difficult to get the fundamentals right, to go into depth on all these manuals, the C lightning manual, the LND manual, the Bitcoin manual, find all the different options that work together, how they work together and packaging that all for the user to be able to use easily.

Nixbitcoin:

And that’s the real ease of use we’re focusing on at the moment. And then, you know, that graphical stuff is just one more step from there, but getting the foundation right is what allows you to make it easy to use for everybody. And I’m really excited by the way of getting software into it, like CoinJoin software, wasabi Samourai, so people can use this wallet while they’re walking around. They can connect to their own little nix-bitcoin node that’s hosted on their own server at home. And just enjoy this kind of privacy and security that they are entitled to. This is what, how the world was meant to be the private information is supposed to be private and the secure funds are supposed to be secure against anyone. And that’s kind of the world we’re moving towards by making everybody have an easy way to deploy a node in their home.

Stephan Livera:

There are lots of different node options, and obviously people have varying levels of technical ability to read the code and verify for themselves. Is there anything that you guys could do or the project could do to make it like to mitigate that users having to trust the developers aspect? Because, you know, hypothetically, if there were some malicious code and the user just clicks update without knowing, and in fairness, this is a risk across, you know, many things in the Bitcoin world, but do you have any thoughts on mitigating that risk?

Nixbitcoin:

First of all, the risk is less with nix-bitcoin because we are actually because of NixOS every Nix, every nix-bitcoin node out there is running the same software and that’s verifiable because of the reproducibility. So that’s a really strong defense number one against us inserting malicious code or stuff upstream getting compromised because once we’ve pinned the hash, once we verified that the software’s good ourselves, within the hash, it’s going to be the same software that everybody’s using. So that’s number one, how we’re defending against this right now. And then when it comes to trusting us, we have a completely open development process. Unlike some other node projects, which are closed source at the moment and want to publish their source code once it’s ready, namely, that would be nodl. That’s not the approach we’re taking, because if it’s not good enough to be out in the open, it’s definitely not good enough for people to risk their privacy and their security with something, things that are so precious.

Nixbitcoin:

I don’t think you should ever risk those with proprietary software. And so our development process is completely open everything’s happening on github. People can see our discussions, our different approaches everything’s on GitHub. And the stuff that isn’t on github is in our public IRC channel. And then going further from that something I’m really excited about is either we want to release software with some kind of multisig setup where Jonas, I, and some other developers have to sign every single release and the user verifies that client side, or I have not really communicated this with the other developers yet, but I’m looking into Frank Brown’s codechain approach, which makes it impossible to target a backdoor to one person. Even if you have the signing keys. So you need to backdoor everybody with the same source code, if you want, if you’re compromised.

Nixbitcoin:

And that’s a much better security assumption, because people are going to realize that when it’s deployed to everybody. So when it comes, I think you’re based in Australia, right? They have this bill there, which can force developers to put in targeted back doors. And I think we’re going to see that rolled out across the Western world. I’m not looking forward to it, but I think it’s gonna slowly be creeping in. And that’s where something like codechain comes in, where we can’t target a backdoor to one user. We have to target a backdoor to every user. And that’s going to get noticed very quickly because we have technical users who are going to notice that.

Stephan Livera:

One other question, is like a natural kind of dichotomy here where sometimes certain projects appeal more to a very technical user, but then once, like a lot of newbie users turn up, the more technical ones lose interest. Is that something you might foresee here? Or is it more just like you see this as, like, this is going to be part of the underlying infrastructure and therefore there are going to be a lot of people who maintain interest.

Nixbitcoin:

No, I don’t, I don’t think that’s ever going to happen because the technical users benefit from normal users in the same exact way that normal users benefit from technical users because normal users are using Android 5.0, and they’re doing some weird stuff and they’re you know, actually using this in the world. So they’re going to find a bunch of bugs that technical users are never going to find. So I’m really looking forward to the influx of newbies because they’re gonna really use this project in a bunch of different ways and are going to make it really start to live. That’s something I wasn’t impressed with the Samourai cofounder interview, where he kept on focusing on the user. And that’s what we’re building software for is a user. You can build the most beautiful piece of software like nix-bitcoin is, if nobody’s using it and it’s really not alive. And so I don’t think first of all, I’m looking forward to users of all different backgrounds coming towards nix-bitcoin. And then I also think that everybody’s going to benefit from it, and we’re going to have a really well tested, refined node set up that, you know, whether it’s an enterprise, a startup like Donner lab or normal users, or guys developers themselves, we’re all gonna benefit from this one tested and refined project.

Stephan Livera:

Gotcha. right. Just a small correction that believe you’re referring to Zelko, so he’s not actually a Samourai co-founder. He’s actually more like a community member. That’s a small thing. But to the broader point about you know, nix-bitcoin and having a range of users certainly take that point. I guess it’s interesting though, because I’m sure you’ve probably seen there’s like a famous XKCD comic about how there’s 14 standards and people say, Oh, what we need is one standard to unify them all. And then the next panel is, Oh, now there’s now there’s 15 standards!

Nixbitcoin:

Yeah, of course that’s always the risk. But with NixOS we’re building on an infrastructure that’s being used already, so we’re not really going out there and reinventing the wheel, we’re just using the wheel how it’s meant to be used. And, well, I think this standard is going to be the one because it’s usable for all use cases. So underlying infrastructure, yes, it has the potential, but we’re also happy about every user that finds benefits, be it a, an enterprise or a developer or whoever, you know, we don’t need to take over everything to make a difference and to be really happy about building good software.

Stephan Livera:

Right.Yeah. It just needs to hit a certain level of users such that it kind of sustains and is you know, commonly thought of as a common, you know, group, if you will. So even now, if people talk about different discussions around, Oh, okay. How many people are running nodes? And if it’s kind of one of the ones that people think of commonly, then I guess that’s, kind of at least a good sign that people are thinking, okay, there’s a good bunch of users out there who are on this particular package they’re on this particular, you know, software stack. Right. so let’s talk a little bit about the development and the community aspects of it. So obviously it’s quite small right now, as I gather from you what are the main ways of collaboration I presume? I mean, you’ve got a github. You mentioned an IRC, are those the main ways you’d like people who want to contribute to come and chat with you and to participate?

Nixbitcoin:

Yeah. Github is really great because it’s become this focal point for development. So get hub is really strong. We’ve seen IRC, I really personally like IRC, but I think that to be realistic, not a lot of regular people are, going around IRC. So I’m open to expanding our communication infrastructure and what I’m really also planning myself to do is releasing a bunch of YouTube videos and easy tutorials. You know, it’s communication. It’s one way, but it’s going to make it a lot easier for people to start it up. And they’re going to see that it’s actually not as difficult as they probably expect. It’s just basically three or four commands and you’re there. And so to go back to your original question github is probably the best way of communication around software development when it comes to support. We have limited resources because we’re not really, we don’t really have a business model yet, but when there is a business model or if there is a business model, then we’ll find a way we’ll make a way for users to get in touch with us easily.

Stephan Livera:

I see, and I guess one other question around, if somebody wants to do, let’s say nix-bitcoin on a Raspberry Pi or on one, on one of those single board computer style things, that’s something that the project works with or supports, is it?

Nixbitcoin:

Yeah. That’s, that’s how we use it right now. Is on single board computers not right now the Raspberry Pi, but I’m pretty sure it works. We should try that too, but the APU PC engines single board machines they’re really fun because they are more powerful, they can take an SSD without, you know, using a USB cable or something. And when people have asked what kind of hardware to use, I’ve always recommended that, but it works on a Raspberry Pi and it works in the cloud also, which is how Donner Lab is using it.

Stephan Livera:

Last topic was just around hardware and where we’re going with some of that. So there is a little bit more chatter and talk about the idea of moving towards open hardware. And so here, some of the things you might hear people talk about you know, RISC-V reduced instruction set something, that I can’t remember exactly what it stands for. And some other people talk about Raptor computing and things like that. Basically the idea is trying to move towards these more open hardware methods as a way to also, you know for security reasons. So do you have any thoughts on that, on what is like an optimal, or if someone’s more concerned about that, what sort of hardware should they be looking to run nix-bitcoin on?

Nixbitcoin:

So the APU is also already pretty good because it has a core boot open source firmware. So you kind of already have a good level of hardware security with that. Different kinds of architectures, like open power 9, which tap which Talos uses and from Raptor uses RISC-V. They’re really in the beginning right now. So I don’t know if a normal user is going to be really happy with that yet, you’re going to run into a lot of issues with compiling software, just stuff that you don’t want to deal with. And enterprise also there, you know, it’s probably best for developers at the moment, but that’s something that’s getting better every day. Right now I’d recommend to get a APU or some kind of other core booted device, and then follow the install manual.

Nixbitcoin:

We have some tips on how to further harden your hardware on a firmware level, deactivating some features that have recently been used to do exploits, but, you know, with the hardening we built in, you always have to think about how is somebody going to attack you. And they don’t have a lot of attack surface with us. You know, there’s no browser running that you’re browsing on different websites with, there’s really no way to deliver an exploit properly. And even where there would be, you have a bunch of different, you have new walls, you have different kind of walls and security around that, which make it even more difficult. So chaining a bunch of exploits. And then leaving, you know, using a hardware vulnerability at the moment is outside of our threat model because the people who have that threat model it’s wow, you’ve really done a lot of work to get yourself there.

Stephan Livera:

I see, makes sense.

Nixbitcoin:

And another topic maybe before we close is a business model. That’s, you know, something, I think that every good project that wants to survive at some point it needs to have. And I think we’re still on that front looking for something that is as elegant as, as the CoinJoin model, which is one of the best business models probably out there. Making money on a service on a feed that also serves a security function as a denial of service protection inside the service. So it’s really extremely elegant, and that would be something interesting for nix-bitcoin, if we can offer some kind of service, like let’s say managing a lightning node, that’s something complicated and you often have to make decisions about, okay, who are you gonna open a channel with? How are you going to balance that?

Nixbitcoin:

And are you going to establish yourself as a really good routing node? And maybe we could have some kind of API with logic running on a backend where people are call it are submitting some data and asking for the best possible decision. And we charge them on on the lightning network on every request. That’s something just that came to mind recently, but that would be a business model that could sustain nix-bitcoin or just selling pre-installed hardware. But that comes with a bunch of security risks as well, which we would need probably we would want to mitigate before we start shipping hardware with pre-installed software on it.

Stephan Livera:

Yep. So it sounds like you could either sell the pre-installed box basically, or you might try to do something more like a red hat model where you are the consultant and the software is free, but if they want additional technical support, then that’s where that’s where they would pay for it.

Nixbitcoin:

Or something like, yeah, next cloud, which is a great example. It’s open to every user, but as soon as an enterprise wants it, and they have a lot of specific needs to them, as soon as that happens, they need to charge, but they need to pay for consulting and for subscription and stuff like that. So that’s a way to monetize software, but I think right now it’s really going good as an open source free software project. And we’ve never compromised security or our values in order to make this a super profitable project, because it will, it can succeed in its limited way even as free software project.

Stephan Livera:

Excellent. Well, look, I think that’s all the questions I had. So nix-bitcoin, do you want to just let the listeners know where they can find you?

Nixbitcoin:

nix-bitcoin was a name that I adapted specifically for this project. So there might be a bunch of confused people around that. That’s why recently I’ve changed the name to the nix-bitcoin Dev and it’s, you know, for me reaching me is not really that important with the Twitter project and with a project it has own Twitter and on GitHub for Nix is the organization. And then nix-bitcoin is the repo always good place to submit stuff. And then IRC is at the moment, our communication way and yeah, Twitter also as a communication, both sided, through messages or posts. And we’d be happy to have you at this point. Maybe it’s a bit too early if you’re not. If you’re not super interested in figuring out a bunch of low level stuff, but you’ll see a bunch of, you’ll see YouTube videos, you’ll see guides coming out that are gonna make it really accessible. And then communication will also scale with them.

Stephan Livera:

Excellent. Well, thanks very much for joining me.

Nixbitcoin:

Thank you for having me. It was a pleasure and. I look forward to hearing the podcast and other podcasts.
